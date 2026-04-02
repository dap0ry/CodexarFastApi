import ast
import sys
import io
import httpx

from fastapi import APIRouter, HTTPException, Depends

import app.core.database as database
from app.core.security import get_current_user
from app.models.exercise import SolveRequest

router = APIRouter()

PISTON_URL = "https://emkc.org/api/v2/piston/execute"
PISTON_LANG = {"C++": "c++", "Java": "java", "Go": "go", "C#": "csharp"}


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
        if isinstance(val[0], int): return f"new int[]{{{inner}}}"
        if isinstance(val[0], str): return f"new string[]{{{inner}}}"
        return f"new object[]{{{inner}}}"
    return str(val)


def _normalize(s: str) -> str:
    s = s.strip()
    if s.lower() == "true": return "True"
    if s.lower() == "false": return "False"
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
    static string PyRepr(bool v) => v ? "True" : "False";
    static string PyRepr(string v) => v;
    static string PyRepr(int[] v) => "[" + string.Join(", ", v) + "]";
    static string PyRepr(string[] v) => "[" + string.Join(", ", v) + "]";

    static void Main() {{
{calls_str}
    }}
}}
"""


BUILDERS = {"C++": _build_cpp, "Java": _build_java, "Go": _build_go, "C#": _build_cs}
FILE_NAMES = {"C++": "main.cpp", "Java": "Main.java", "Go": "main.go", "C#": "solution.cs"}


# ─────────────────────────────────────────────
#  Piston runner
# ─────────────────────────────────────────────

async def _run_with_piston(language: str, user_code: str, test_cases: list) -> dict:
    # Parse all test inputs as Python literals first
    all_args = []
    for i, tc in enumerate(test_cases):
        try:
            raw = f"({tc['input']},)"
            parsed = ast.literal_eval(raw)
            if not isinstance(parsed, tuple):
                parsed = (parsed,)
            all_args.append(parsed)
        except Exception as e:
            return {"correct": False, "message": f"Error en caso {i+1}: input inválido ({e})", "failed_case": i+1}

    # Build combined program
    try:
        full_code = BUILDERS[language](user_code, all_args)
    except Exception as e:
        return {"correct": False, "message": f"Error generando programa: {e}", "failed_case": 0}

    # Call Piston
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(PISTON_URL, json={
                "language": PISTON_LANG[language],
                "version": "*",
                "files": [{"name": FILE_NAMES[language], "content": full_code}]
            })
        data = resp.json()
    except Exception:
        return {"correct": False, "message": "El ejecutor de código no está disponible. Inténtalo de nuevo."}

    # Compilation error
    compile_info = data.get("compile", {})
    if compile_info and compile_info.get("code", 0) != 0:
        err = (compile_info.get("stderr") or compile_info.get("output") or "").strip()[:400]
        return {"correct": False, "message": f"Error de compilación:\n{err}", "failed_case": 0}

    # Runtime error
    run_info = data.get("run", {})
    if run_info.get("code", 0) != 0:
        err = (run_info.get("stderr") or run_info.get("output") or "").strip()[:400]
        return {"correct": False, "message": f"Error de ejecución:\n{err}", "failed_case": 0}

    # Compare line by line
    lines = [l.strip() for l in run_info.get("stdout", "").split("\n") if l.strip()]
    for i, tc in enumerate(test_cases):
        expected = str(tc["expected_output"]).strip()
        actual = lines[i] if i < len(lines) else ""
        if _normalize(actual) != _normalize(expected):
            return {
                "correct": False,
                "message": f"Caso {i+1} fallido",
                "failed_case": i+1,
                "input": tc["input"],
                "expected": expected,
                "got": actual
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

    exercises_cursor = database.db.exercises.find()
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

<<<<<<< Updated upstream
    # Only Python execution supported for now
    if body.language != "Python":
        if body.save:
            user = await database.db.users.find_one({"email": email})
            solved_ids = user.get("solved_exercises", []) if user else []
            if exercise_id not in solved_ids:
                difficulty = ex.get("difficulty", "Normal")
                elo_gain = 1 if difficulty == "Fácil" else (5 if difficulty == "Difícil" else 2)

                await database.db.users.update_one(
                    {"email": email},
                    {
                        "$addToSet": {"solved_exercises": exercise_id},
                        "$inc": {"elo": elo_gain}
                    }
                )
                # Record solver in exercise
                ex_has_first = ex.get("first_solver_email")
                update_ex = {"$addToSet": {"solvers": email}}
                if not ex_has_first:
                    update_ex["$set"] = {"first_solver_email": email}
                await database.db.exercises.update_one({"_id": oid}, update_ex)
            return {"correct": True, "message": "¡Ejercicio guardado correctamente!"}
        return {"correct": True, "message": f"Verificación manual para {body.language}. Haz clic en Guardar si tu solución es correcta."}
=======
    # ── Python: run locally with exec() ──
    if body.language == "Python":
        user_code = body.code
        for i, tc in enumerate(test_cases):
            test_input_str = tc["input"]
            expected_str = str(tc["expected_output"]).strip()

            exec_globals = {}
            try:
                exec(compile(user_code, "<solution>", "exec"), exec_globals)
            except Exception as e:
                return {"correct": False, "message": f"Error de compilación: {str(e)}", "failed_case": i + 1}
>>>>>>> Stashed changes

            solve_fn = exec_globals.get("solve")
            if not solve_fn or not callable(solve_fn):
                return {"correct": False, "message": "No se encontró la función `solve` en tu código.", "failed_case": 0}

            try:
                args_raw = f"({test_input_str},)"
                parsed_args = ast.literal_eval(args_raw)
                if not isinstance(parsed_args, tuple):
                    parsed_args = (parsed_args,)
            except Exception as e:
                return {"correct": False, "message": f"Error procesando caso {i+1}: {str(e)}", "failed_case": i + 1}

            try:
                result = solve_fn(*parsed_args)
            except Exception as e:
                return {"correct": False, "message": f"Error en caso {i+1}: {str(e)}", "failed_case": i + 1, "input": test_input_str, "expected": expected_str}

            actual_str = str(result).strip()
            if actual_str.lower() == "true": actual_str = "True"
            if actual_str.lower() == "false": actual_str = "False"
            if actual_str.replace(" ", "") != expected_str.replace(" ", ""):
                return {"correct": False, "message": f"Caso {i+1} fallido", "failed_case": i + 1, "input": test_input_str, "expected": expected_str, "got": actual_str}

        result_ok = True

    # ── Other languages: run via Piston API ──
    else:
        if body.language not in PISTON_LANG:
            return {"correct": False, "message": f"Lenguaje no soportado: {body.language}"}

        piston_result = await _run_with_piston(body.language, body.code, test_cases)
        if not piston_result["correct"]:
            return piston_result
        result_ok = True

    # ── All tests passed: optionally save ──
    if result_ok and body.save:
        user = await database.db.users.find_one({"email": email})
        solved_ids = user.get("solved_exercises", []) if user else []
        if exercise_id not in solved_ids:
            difficulty = ex.get("difficulty", "Normal")
            elo_gain   = 1 if difficulty == "Fácil" else (5 if difficulty == "Difícil" else 2)
            coins_gain = 10 if difficulty == "Fácil" else (50 if difficulty == "Difícil" else 25)

            await database.db.users.update_one(
                {"email": email},
                {"$addToSet": {"solved_exercises": exercise_id}, "$inc": {"elo": elo_gain, "coins": coins_gain}}
            )
            ex_fresh = await database.db.exercises.find_one({"_id": oid})
            has_first = ex_fresh.get("first_solver_email") if ex_fresh else None
            update_ex = {"$addToSet": {"solvers": email}}
            if not has_first:
                update_ex["$set"] = {"first_solver_email": email}
            await database.db.exercises.update_one({"_id": oid}, update_ex)

        return {"correct": True, "message": "¡Ejercicio guardado correctamente! ✓"}

    return {"correct": True, "message": "¡Todos los casos de prueba superados! Puedes guardar tu solución."}
