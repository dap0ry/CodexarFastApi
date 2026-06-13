import ast
from datetime import datetime
from typing import List

import httpx

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

import app.core.database as database
from app.core.security import get_current_user
from app.core.roles import require_moderator
from app.core.compare import compare_result, compare_config_from_dict
from app.core.config import JUDGE0_KEY, JUDGE0_SELF_URL
from app.models.exercise import SolveRequest

router = APIRouter()


# ── Exercise creation schema ──────────────────────────────────────────────────

class TestCaseIn(BaseModel):
    input: str
    expected_output: str


class I18nFields(BaseModel):
    es: str = ""
    en: str = ""
    zh: str = ""

class ExerciseCreate(BaseModel):
    title: str
    description: str
    difficulty: int   # ELO rating: 800 | 1000 | 1200 | 1400 | 1600 | 1800 | 2000 | 2200 | 2400 | 2600 | 3000 | 3500
    category: str
    test_cases: List[TestCaseIn]
    stub_python: str = ""
    stub_cpp:    str = ""
    stub_java:   str = ""
    stub_go:     str = ""
    stub_csharp: str = ""
    title_i18n:       I18nFields | None = None
    description_i18n: I18nFields | None = None

# ─────────────────────────────────────────────
#  Judge0 config
# ─────────────────────────────────────────────
# Priority: self-hosted (JUDGE0_SELF_URL) > RapidAPI (JUDGE0_KEY) > public CE
_JUDGE0_PUBLIC_URL = "https://ce.judge0.com/submissions"
_JUDGE0_RAPID_URL  = "https://judge0-ce.p.rapidapi.com/submissions"

if JUDGE0_SELF_URL:
    JUDGE0_URL     = f"{JUDGE0_SELF_URL.rstrip('/')}/submissions"
    JUDGE0_HEADERS: dict = {}
elif JUDGE0_KEY:
    JUDGE0_URL     = _JUDGE0_RAPID_URL
    JUDGE0_HEADERS = {"X-RapidAPI-Host": "judge0-ce.p.rapidapi.com", "X-RapidAPI-Key": JUDGE0_KEY}
else:
    JUDGE0_URL     = _JUDGE0_PUBLIC_URL
    JUDGE0_HEADERS = {}

# Supported languages
JUDGE0_LANG = {
    "Python": 71,   # Python 3.8.1
    "C++":    54,   # GCC 9.2.0
    "Java":   62,   # Java (OpenJDK 13.0.1)
}


# ─────────────────────────────────────────────
#  Helpers: Python value → language literal
# ─────────────────────────────────────────────

def _to_cpp(val):
    if isinstance(val, bool): return "true" if val else "false"
    if isinstance(val, int): return str(val)
    if isinstance(val, float): return str(val)
    if isinstance(val, str): return f'"{val}"'
    if isinstance(val, list):
        return "{" + ", ".join(_to_cpp(x) for x in val) + "}"
    return str(val)

def _to_java(val):
    if isinstance(val, bool): return "true" if val else "false"
    if isinstance(val, int): return str(val)
    if isinstance(val, float): return str(val)
    if isinstance(val, str): return f'"{val}"'
    if isinstance(val, list):
        inner = ", ".join(_to_java(x) for x in val)
        if not val: return "new int[]{}"
        if isinstance(val[0], list):
            # 2D array: determine element type from first non-empty inner list
            first_inner = next((x for x in val if x), None)
            if first_inner and isinstance(first_inner[0], str): return f"new String[][]{{{inner}}}"
            return f"new int[][]{{{inner}}}"
        if isinstance(val[0], int): return f"new int[]{{{inner}}}"
        if isinstance(val[0], str): return f"new String[]{{{inner}}}"
        return f"new Object[]{{{inner}}}"
    return str(val)

def _to_go(val):
    if isinstance(val, bool): return "true" if val else "false"
    if isinstance(val, int): return str(val)
    if isinstance(val, float): return str(val)
    if isinstance(val, str): return f'"{val}"'
    if isinstance(val, list):
        inner = ", ".join(_to_go(x) for x in val)
        if not val: return "[]int{}"
        if isinstance(val[0], list):
            first_inner = next((x for x in val if x), None)
            if first_inner and isinstance(first_inner[0], str): return f"[][]string{{{inner}}}"
            return f"[][]int{{{inner}}}"
        if isinstance(val[0], int): return f"[]int{{{inner}}}"
        if isinstance(val[0], str): return f"[]string{{{inner}}}"
        return f"[]interface{{}}{{{inner}}}"
    return str(val)

def _to_cs(val):
    if isinstance(val, bool): return "true" if val else "false"
    if isinstance(val, int): return str(val)
    if isinstance(val, float): return str(val)
    if isinstance(val, str): return f'"{val}"'
    if isinstance(val, list):
        inner = ", ".join(_to_cs(x) for x in val)
        if not val: return "new int[]{}"
        if isinstance(val[0], list):
            first_inner = next((x for x in val if x), None)
            if first_inner and isinstance(first_inner[0], str): return f"new string[][]{{{inner}}}"
            return f"new int[][]{{{inner}}}"
        if isinstance(val[0], int): return f"new int[]{{{inner}}}"
        if isinstance(val[0], str): return f"new string[]{{{inner}}}"
        return f"new object[]{{{inner}}}"
    return str(val)


def _canonical(val) -> str:
    """Convert any Python value to a language-agnostic canonical string for comparison."""
    if val is None:                return "None"
    if isinstance(val, bool):      return "True" if val else "False"
    if isinstance(val, float):
        # Preserve .0 for whole floats (e.g. median 2.0), trim trailing zeros otherwise
        if val == int(val):        return str(int(val)) + ".0"
        return str(val)
    if isinstance(val, int):       return str(val)
    if isinstance(val, str):       return val          # plain content, no quotes
    if isinstance(val, (list, tuple)):
        return "[" + ",".join(_canonical(x) for x in val) + "]"
    return str(val)


def _normalize(s: str) -> str:
    """
    Normalize output strings for robust comparison.
    Tries to parse the string as a Python literal and canonicalize it.
    Falls back to stripping spaces if parsing fails.
    """
    s = s.strip()
    # Fast path for booleans (some languages print lowercase)
    if s.lower() == "true":  return "True"
    if s.lower() == "false": return "False"
    # None / null variants
    if s in ("None", "null", "nil", "__NONE__"): return "None"
    # Try to parse as Python literal → canonical form
    try:
        val = ast.literal_eval(s)
        return _canonical(val)
    except Exception:
        # Not a parseable literal: just strip spaces (works for plain ints/strings)
        return s.replace(" ", "")


# ─────────────────────────────────────────────
#  Program builders (combined: all test cases)
# ─────────────────────────────────────────────

def _build_cpp(user_code: str, all_args: list) -> str:
    calls = []
    for args in all_args:
        cpp_args = ", ".join(_to_cpp(a) for a in args)
        calls.append(f"    cout << pyRepr(solve({cpp_args})) << \"\\n\";")
    calls_str = "\n".join(calls)

    return f"""#include <bits/stdc++.h>
using namespace std;

{user_code}

template<typename T>
string pyRepr(T v) {{ return to_string(v); }}
template<>
string pyRepr<bool>(bool v) {{ return v ? "True" : "False"; }}
template<>
string pyRepr<string>(string v) {{ return v; }}
template<>
string pyRepr<vector<int>>(vector<int> v) {{
    string s = "[";
    for (int i = 0; i < (int)v.size(); i++) {{
        if (i) s += ", ";
        s += to_string(v[i]);
    }}
    return s + "]";
}}
template<>
string pyRepr<vector<string>>(vector<string> v) {{
    string s = "[";
    for (int i = 0; i < (int)v.size(); i++) {{
        if (i) s += ", ";
        s += v[i];
    }}
    return s + "]";
}}
template<>
string pyRepr<double>(double v) {{
    ostringstream ss;
    ss << v;
    string s = ss.str();
    if (s.find('.') == string::npos) s += ".0";
    return s;
}}

int main() {{
{calls_str}
    return 0;
}}
"""


def _build_java(user_code: str, all_args: list) -> str:
    calls = []
    for args in all_args:
        java_args = ", ".join(_to_java(a) for a in args)
        calls.append(f"        System.out.println(pyRepr(solve({java_args})));")
    calls_str = "\n".join(calls)

    return f"""import java.util.*;
public class Main {{
    {user_code}

    static String pyRepr(int v) {{ return Integer.toString(v); }}
    static String pyRepr(long v) {{ return Long.toString(v); }}
    static String pyRepr(double v) {{
        if (v == (long)v) return Long.toString((long)v) + ".0";
        return Double.toString(v);
    }}
    static String pyRepr(boolean v) {{ return v ? "True" : "False"; }}
    static String pyRepr(String v) {{ return v; }}
    static String pyRepr(int[] v) {{
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < v.length; i++) {{
            if (i > 0) sb.append(", ");
            sb.append(v[i]);
        }}
        return sb.append("]").toString();
    }}
    static String pyRepr(String[] v) {{
        return "[" + String.join(", ", v) + "]";
    }}

    public static void main(String[] args) {{
{calls_str}
    }}
}}
"""


def _build_go(user_code: str, all_args: list) -> str:
    calls = []
    for args in all_args:
        go_args = ", ".join(_to_go(a) for a in args)
        calls.append(f'\tfmt.Println(pyRepr(solve({go_args})))')
    calls_str = "\n".join(calls)

    return f"""package main

import (
\t"fmt"
\t"strconv"
\t"strings"
)

{user_code}

func pyRepr(v interface{{}}) string {{
\tswitch val := v.(type) {{
\tcase int:
\t\treturn strconv.Itoa(val)
\tcase bool:
\t\tif val {{ return "True" }}
\t\treturn "False"
\tcase string:
\t\treturn val
\tcase []int:
\t\tparts := make([]string, len(val))
\t\tfor i, x := range val {{ parts[i] = strconv.Itoa(x) }}
\t\treturn "[" + strings.Join(parts, ", ") + "]"
\tcase []string:
\t\treturn "[" + strings.Join(val, ", ") + "]"
\tcase float64:
\t\tif val == float64(int(val)) {{ return strconv.Itoa(int(val)) + ".0" }}
\t\treturn strconv.FormatFloat(val, 'f', -1, 64)
\tdefault:
\t\treturn fmt.Sprintf("%v", v)
\t}}
}}

func main() {{
{calls_str}
}}
"""


def _build_cs(user_code: str, all_args: list) -> str:
    calls = []
    for args in all_args:
        cs_args = ", ".join(_to_cs(a) for a in args)
        calls.append(f"        Console.WriteLine(PyRepr(Solve({cs_args})));")
    calls_str = "\n".join(calls)

    return f"""using System;
using System.Collections.Generic;
using System.Linq;

class Solution {{
    {user_code}

    static string PyRepr(int v) => v.ToString();
    static string PyRepr(long v) => v.ToString();
    static string PyRepr(double v) => (v == (long)v) ? ((long)v).ToString() + ".0" : v.ToString();
    static string PyRepr(bool v) => v ? "True" : "False";
    static string PyRepr(string v) => v;
    static string PyRepr(int[] v) => "[" + string.Join(", ", v) + "]";
    static string PyRepr(string[] v) => "[" + string.Join(", ", v) + "]";

    static void Main() {{
{calls_str}
    }}
}}
"""


def _build_python(user_code: str, all_args: list) -> str:
    """
    Each test case is wrapped in try/except so a crash on case N
    doesn't silently eat the output for cases N+1, N+2, ...
    Output format per case:
    - Normal return  → str(value)   e.g. "6" / "True" / "[1,2,3]"
    - None return    → "__NONE__"   (user forgot `return`)
    - Exception      → "__ERR__:<msg>"
    flush=True ensures output is captured even in Piston's piped environment.
    """
    calls = []
    for args in all_args:
        py_args = ", ".join(repr(a) for a in args)
        calls.append(
            f"    try:\n"
            f"        _r = solve({py_args})\n"
            f"        print('__NONE__' if _r is None else ('__EMPTY__' if _r == '' else str(_r)), flush=True)\n"
            f"    except Exception as _e:\n"
            f"        print(f'__ERR__:{{_e}}', flush=True)\n"
        )
    calls_str = "\n".join(calls)
    return f"import sys\nsys.stdout.reconfigure(line_buffering=True)\n\n{user_code}\n\nif __name__ == '__main__':\n{calls_str}\n"


BUILDERS = {"Python": _build_python, "C++": _build_cpp, "Java": _build_java, "Go": _build_go, "C#": _build_cs}


# ─────────────────────────────────────────────
#  Judge0 runner
# ─────────────────────────────────────────────

async def _run_with_judge0(language: str, user_code: str, test_cases: list, compare_cfg=None) -> dict:
    # ── 1. Parse all test inputs ───────────────────────────────────────────
    all_args = []
    for i, tc in enumerate(test_cases):
        try:
            raw    = f"({tc['input']},)"
            parsed = ast.literal_eval(raw)
            if not isinstance(parsed, tuple):
                parsed = (parsed,)
            all_args.append(parsed)
        except Exception as e:
            return {
                "correct": False,
                "message": f"Input inválido en caso {i+1}: {e}",
                "failed_case": i + 1,
                "input": tc["input"],
                "expected": str(tc["expected_output"]),
                "got": "(input no parseable)",
            }

    # ── 2. Build full program ──────────────────────────────────────────────
    try:
        full_code = BUILDERS[language](user_code, all_args)
    except Exception as e:
        return {"correct": False, "message": f"Error generando programa: {e}", "failed_case": 0}

    # ── 3. Call Judge0 API ─────────────────────────────────────────────────
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{JUDGE0_URL}?base64_encoded=false&wait=true",
                json={
                    "source_code": full_code,
                    "language_id": JUDGE0_LANG[language],
                    "stdin":       "",
                },
                headers={**JUDGE0_HEADERS, "Content-Type": "application/json"},
            )
        data = resp.json()
    except Exception as e:
        return {"correct": False, "message": f"El ejecutor de código no está disponible. Inténtalo de nuevo. ({e})"}

    # ── 4. Judge0 status handling ──────────────────────────────────────────
    status    = data.get("status", {})
    status_id = status.get("id", 0)

    stdout          = data.get("stdout") or ""
    stderr          = data.get("stderr") or ""
    compile_output  = data.get("compile_output") or ""

    # Status 6 = Compilation Error
    if status_id == 6:
        err = compile_output.strip()[:600] or stderr.strip()[:600]
        return {"correct": False, "message": f"Error de compilación:\n{err}", "failed_case": 0}

    # Status 5 = Time Limit Exceeded
    if status_id == 5:
        return {"correct": False, "message": "Tiempo límite de ejecución excedido"}

    # Status 7–12 = Runtime errors (SIGSEGV, SIGABRT, NZEC, etc.)
    if 7 <= status_id <= 12:
        err = (stderr or compile_output).strip()[:600]
        desc = status.get("description", "Runtime Error")
        return {
            "correct":     False,
            "message":     f"{desc}:\n{err}" if err else desc,
            "failed_case": 1,
            "input":       test_cases[0]["input"] if test_cases else "",
            "expected":    str(test_cases[0]["expected_output"]) if test_cases else "",
            "got":         "(sin salida)",
        }

    # ── 5. Parse stdout into one line per test case ────────────────────────
    lines = [l.strip() for l in stdout.split("\n") if l.strip()]

    # ── 6. Compare case by case ────────────────────────────────────────────
    for i, tc in enumerate(test_cases):
        expected_raw = str(tc["expected_output"]).strip()
        actual_raw   = lines[i] if i < len(lines) else ""

        # ── 6a. Python harness error markers ──────────────────────────────
        if actual_raw.startswith("__ERR__:"):
            err_msg = actual_raw[8:]
            return {
                "correct":     False,
                "message":     f"Excepción en caso {i+1}: {err_msg}",
                "failed_case": i + 1,
                "input":       tc["input"],
                "expected":    expected_raw,
                "got":         f"Error: {err_msg}",
            }

        # ── 6b. Missing return (Python __NONE__ marker) ────────────────────
        if actual_raw == "__NONE__":
            return {
                "correct":     False,
                "message":     f"Caso {i+1}: la función no devuelve nada (¿olvidaste return?)",
                "failed_case": i + 1,
                "input":       tc["input"],
                "expected":    expected_raw,
                "got":         "None (sin return)",
            }

        # ── 6c. Empty string return (legitimate) ──────────────────────────
        if actual_raw == "__EMPTY__":
            actual_raw = ""

        # ── 6d. No output for this case ────────────────────────────────────
        elif not actual_raw:
            err_hint = stderr.strip()[:300] if stderr.strip() else "el programa no produjo salida"
            return {
                "correct":     False,
                "message":     f"Error de ejecución en caso {i+1}: {err_hint}",
                "failed_case": i + 1,
                "input":       tc["input"],
                "expected":    expected_raw,
                "got":         "(sin salida)",
            }

        # ── 6e. Deep comparison via compare.py ────────────────────────────
        ok, got_display, exp_display = compare_result(
            got_raw      = actual_raw,
            expected_raw = expected_raw,
            input_args   = all_args[i],
            config       = compare_cfg,
        )
        if not ok:
            return {
                "correct":     False,
                "message":     f"Caso {i+1} fallido",
                "failed_case": i + 1,
                "input":       tc["input"],
                "expected":    exp_display,
                "got":         got_display,
            }

    # ── 7. All passed ──────────────────────────────────────────────────────
    if not lines and test_cases:
        err_hint = (stderr or compile_output).strip()[:300] or "el programa no produjo salida"
        return {
            "correct":     False,
            "message":     f"Error de ejecución: {err_hint}",
            "failed_case": 1,
            "input":       test_cases[0]["input"],
            "expected":    str(test_cases[0]["expected_output"]),
            "got":         "(sin salida)",
        }

    return {"correct": True, "message": "¡Todos los casos de prueba superados!"}


# ─────────────────────────────────────────────
#  Routes
# ─────────────────────────────────────────────

@router.get("/api/exercises")
async def get_exercises(email: str = Depends(get_current_user)):
    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    solved_ids = set(user.get("solved_exercises", []))
    friends_emails = set(user.get("friends", []))

    exercises_cursor = database.db.exercises.find({"tournament_only": {"$ne": True}})
    exercises = []
    async for ex in exercises_cursor:
        ex_id = str(ex["_id"])
        ex["id"] = ex_id
        del ex["_id"]
        ex["solved"] = ex_id in solved_ids
        ex.pop("test_cases", None)
        ex.pop("stub", None)

        first_solver_email = ex.pop("first_solver_email", None)
        if first_solver_email:
            fs_user = await database.db.users.find_one({"email": first_solver_email}, {"username": 1, "avatar": 1})
            ex["first_solver"] = {"username": fs_user.get("username") if fs_user else "?", "avatar": fs_user.get("avatar") if fs_user else None}
        else:
            ex["first_solver"] = None

        solvers_list = ex.pop("solvers", [])
        if friends_emails and solvers_list:
            friends_solved_emails = [e for e in solvers_list if e in friends_emails]
            if friends_solved_emails:
                friends_solved = []
                cursor = database.db.users.find({"email": {"$in": friends_solved_emails}}, {"username": 1, "avatar": 1})
                async for fu in cursor:
                    friends_solved.append({"username": fu.get("username"), "avatar": fu.get("avatar")})
                ex["friends_solved"] = friends_solved
            else:
                ex["friends_solved"] = []
        else:
            ex["friends_solved"] = []

        exercises.append(ex)
    return exercises


@router.get("/api/exercises/solved")
async def get_solved_exercises(email: str = Depends(get_current_user)):
    user = await database.db.users.find_one({"email": email})
    if not user:
        return []
    return user.get("solved_exercises", [])


@router.get("/api/exercises/random")
async def get_random_exercise(email: str = Depends(get_current_user)):
    import random as _random
    exercises = []
    async for ex in database.db.exercises.find():
        exercises.append(ex)
    if not exercises:
        raise HTTPException(status_code=404, detail="No hay ejercicios disponibles")
    ex = dict(_random.choice(exercises))
    user = await database.db.users.find_one({"email": email})
    solved_ids = set(user.get("solved_exercises", [])) if user else set()
    ex["id"] = str(ex["_id"])
    del ex["_id"]
    ex["solved"] = ex["id"] in solved_ids
    return ex


@router.get("/api/exercises/catalog")
async def get_exercise_catalog(email: str = Depends(get_current_user)):
    """Lightweight exercise list for tournament exercise picker."""
    cursor = database.db.exercises.find(
        {"tournament_only": {"$ne": True}},
        {"title": 1, "difficulty": 1, "category": 1, "title_i18n": 1},
    ).sort("difficulty", 1)
    result = []
    async for ex in cursor:
        result.append({
            "id": str(ex["_id"]),
            "title": ex.get("title", ""),
            "title_i18n": ex.get("title_i18n"),
            "difficulty": ex.get("difficulty", 800),
            "category": ex.get("category", ""),
        })
    return result


@router.get("/api/exercises/{exercise_id}")
async def get_exercise(exercise_id: str, email: str = Depends(get_current_user)):
    from bson import ObjectId
    try:
        oid = ObjectId(exercise_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de ejercicio inválido")
    ex = await database.db.exercises.find_one({"_id": oid})
    if not ex:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    user = await database.db.users.find_one({"email": email})
    solved_ids = set(user.get("solved_exercises", [])) if user else set()

    ex["id"] = str(ex["_id"])
    del ex["_id"]
    ex["solved"] = ex["id"] in solved_ids
    return ex


@router.post("/api/exercises/{exercise_id}/solve")
async def solve_exercise(exercise_id: str, body: SolveRequest, email: str = Depends(get_current_user)):
    from bson import ObjectId
    try:
        oid = ObjectId(exercise_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de ejercicio inválido")
    ex = await database.db.exercises.find_one({"_id": oid})
    if not ex:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    test_cases = ex.get("test_cases", [])
    if not test_cases:
        raise HTTPException(status_code=400, detail="Este ejercicio no tiene casos de prueba configurados")

    # ── All languages: run via Judge0 API (no exec() on server) ──
    if body.language not in JUDGE0_LANG:
        return {"correct": False, "message": f"Lenguaje no soportado: {body.language}"}

    # Build CompareConfig from exercise data (optional field, defaults to standard comparison)
    compare_cfg = compare_config_from_dict(ex.get("compare_config"))

    piston_result = await _run_with_judge0(body.language, body.code, test_cases, compare_cfg)
    if not piston_result["correct"]:
        return piston_result
    result_ok = True

    # ── All tests passed: optionally save ──
    if result_ok and body.save:
        user = await database.db.users.find_one({"email": email})
        solved_ids = user.get("solved_exercises", []) if user else []
        already_solved = exercise_id in solved_ids

        # Always update lang_stats when solved correctly (regardless of whether already solved)
        await database.db.users.update_one(
            {"email": email},
            {"$inc": {f"lang_stats.{body.language}": 1}}
        )

        if not already_solved:
            difficulty = ex.get("difficulty", 1200)
            def _coins_reward(d):
                if d < 1000:   return 10
                if d < 1200:   return 20
                if d < 1400:   return 30
                if d < 1600:   return 50
                if d < 1800:   return 80
                if d < 2000:   return 120
                if d < 2400:   return 180
                if d < 3000:   return 250
                if d < 3500:   return 350
                return 500
            coins_gain = _coins_reward(difficulty if isinstance(difficulty, int) else 1200)

            await database.db.users.update_one(
                {"email": email},
                {
                    "$addToSet": {"solved_exercises": exercise_id},
                    "$inc": {"coins": coins_gain}
                }
            )
            ex_fresh = await database.db.exercises.find_one({"_id": oid})
            has_first = ex_fresh.get("first_solver_email") if ex_fresh else None
            update_ex = {"$addToSet": {"solvers": email}}
            if not has_first:
                update_ex["$set"] = {"first_solver_email": email}
            await database.db.exercises.update_one({"_id": oid}, update_ex)

        return {"correct": True, "message": "¡Ejercicio guardado correctamente! ✓"}

    return {"correct": True, "message": "¡Todos los casos de prueba superados! Puedes guardar tu solución."}


# ─────────────────────────────────────────────
#  Create exercise (moderator / admin)
# ─────────────────────────────────────────────

@router.post("/api/exercises/create")
async def create_exercise(body: ExerciseCreate, creator: dict = Depends(require_moderator)):
    VALID_DIFFICULTIES = {800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 3000, 3500}
    if body.difficulty not in VALID_DIFFICULTIES:
        raise HTTPException(status_code=400, detail=f"Dificultad inválida. Opciones: {sorted(VALID_DIFFICULTIES)}")
    if len(body.test_cases) < 1:
        raise HTTPException(status_code=400, detail="Se requiere al menos un caso de prueba")

    doc = {
        "title":       body.title.strip(),
        "description": body.description.strip(),
        "difficulty":  body.difficulty,
        "category":    body.category.strip(),
        "test_cases":  [{"input": tc.input.strip(), "expected_output": tc.expected_output.strip()} for tc in body.test_cases],
        "stub": {
            "python": body.stub_python,
            "cpp":    body.stub_cpp,
            "java":   body.stub_java,
            "go":     body.stub_go,
            "csharp": body.stub_csharp,
        },
        "created_by":  creator.get("username", ""),
        "created_at":  datetime.utcnow(),
        "solvers":     [],
    }
    if body.title_i18n:
        doc["title_i18n"] = body.title_i18n.model_dump()
    if body.description_i18n:
        doc["description_i18n"] = body.description_i18n.model_dump()
    result = await database.db.exercises.insert_one(doc)
    return {"message": "Ejercicio creado correctamente", "id": str(result.inserted_id)}


# ─────────────────────────────────────────────
#  User exercise submission (pending approval)
# ─────────────────────────────────────────────

@router.post("/api/exercises/submit")
async def submit_exercise(body: ExerciseCreate, email: str = Depends(get_current_user)):
    """Any authenticated user can submit an exercise for review (max 3 pending at once)."""
    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Mods/admins bypass → go straight to approved
    role = user.get("role", "user")
    if role in ("moderator", "admin"):
        doc = {
            "title":       body.title.strip(),
            "description": body.description.strip(),
            "difficulty":  body.difficulty,
            "category":    body.category.strip(),
            "test_cases":  [{"input": tc.input.strip(), "expected_output": tc.expected_output.strip()} for tc in body.test_cases],
            "stub": {"python": body.stub_python, "cpp": body.stub_cpp, "java": body.stub_java, "go": body.stub_go, "csharp": body.stub_csharp},
            "created_by":  user.get("username", ""),
            "created_at":  datetime.utcnow(),
            "solvers":     [],
            "status":      "approved",
        }
        result = await database.db.exercises.insert_one(doc)
        return {"message": "Ejercicio publicado directamente.", "id": str(result.inserted_id)}

    # Count pending submissions
    pending_count = await database.db.pending_exercises.count_documents(
        {"submitted_by": user.get("username", ""), "status": "pending"}
    )
    if pending_count >= 3:
        raise HTTPException(status_code=400, detail="Ya tienes 3 ejercicios pendientes de revisión. Espera a que sean aprobados o rechazados.")

    VALID_DIFFICULTIES = {800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 3000, 3500}
    if body.difficulty not in VALID_DIFFICULTIES:
        raise HTTPException(status_code=400, detail=f"Dificultad inválida. Opciones: {sorted(VALID_DIFFICULTIES)}")
    if len(body.test_cases) < 1:
        raise HTTPException(status_code=400, detail="Se requiere al menos un caso de prueba")

    doc = {
        "title":         body.title.strip(),
        "description":   body.description.strip(),
        "difficulty":    body.difficulty,
        "category":      body.category.strip(),
        "test_cases":    [{"input": tc.input.strip(), "expected_output": tc.expected_output.strip()} for tc in body.test_cases],
        "stub": {"python": body.stub_python, "cpp": body.stub_cpp, "java": body.stub_java, "go": body.stub_go, "csharp": body.stub_csharp},
        "submitted_by":  user.get("username", ""),
        "submitted_at":  datetime.utcnow(),
        "status":        "pending",
    }
    result = await database.db.pending_exercises.insert_one(doc)
    return {"message": "Ejercicio enviado para revisión.", "id": str(result.inserted_id)}


# ─────────────────────────────────────────────
#  List pending exercises (mod/admin only)
# ─────────────────────────────────────────────

@router.get("/api/exercises/pending")
async def list_pending_exercises(moderator: dict = Depends(require_moderator)):
    from bson import ObjectId
    cursor = database.db.pending_exercises.find({"status": "pending"}).sort("submitted_at", -1)
    docs = await cursor.to_list(length=100)
    result = []
    for doc in docs:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        result.append(doc)
    return result


# ─────────────────────────────────────────────
#  Approve / Reject pending exercise
# ─────────────────────────────────────────────

@router.post("/api/exercises/pending/{pending_id}/approve")
async def approve_exercise(pending_id: str, moderator: dict = Depends(require_moderator)):
    from bson import ObjectId
    try:
        oid = ObjectId(pending_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    pending = await database.db.pending_exercises.find_one({"_id": oid})
    if not pending:
        raise HTTPException(status_code=404, detail="Ejercicio pendiente no encontrado")

    # Move to exercises collection
    exercise_doc = {k: v for k, v in pending.items() if k not in ("_id", "status", "submitted_by", "submitted_at")}
    exercise_doc["created_by"] = pending.get("submitted_by", "")
    exercise_doc["created_at"] = pending.get("submitted_at", datetime.utcnow())
    exercise_doc["solvers"] = []
    await database.db.exercises.insert_one(exercise_doc)

    # Mark as approved and remove from pending
    await database.db.pending_exercises.delete_one({"_id": oid})
    return {"message": "Ejercicio aprobado y publicado."}


@router.post("/api/exercises/pending/{pending_id}/reject")
async def reject_exercise(pending_id: str, moderator: dict = Depends(require_moderator)):
    from bson import ObjectId
    try:
        oid = ObjectId(pending_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    result = await database.db.pending_exercises.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Ejercicio pendiente no encontrado")
    return {"message": "Ejercicio rechazado y eliminado."}
