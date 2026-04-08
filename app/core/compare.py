"""
compare.py — Motor de comparación robusto para el judge de Codexar.

Características:
  - Comparación profunda de estructuras anidadas (listas de listas, mixtas)
  - Tolerancia configurable para floats  (evita el 0.1+0.2 != 0.3)
  - Comparación sin orden (ignore_order)
  - Equivalencias cross-language: True/true, None/null/nil, "a"/'a'
  - Múltiples outputs válidos       (valid_outputs)
  - Validadores personalizados por problema  (validator)
  - API limpia: compare_result() devuelve (ok, got_display, expected_display)

Integración en exercises.py:
    from app.core.compare import compare_result, compare_config_from_dict

    ok, got_str, exp_str = compare_result(
        got_raw      = actual_line,
        expected_raw = tc["expected_output"],
        input_args   = parsed_args,
        config       = compare_config_from_dict(ex.get("compare_config")),
    )
"""

import ast
import math
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


# ═══════════════════════════════════════════════════════════════════════════════
#  CompareConfig — configuración por ejercicio
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CompareConfig:
    # [2,1] == [1,2]  — útil en problemas donde el orden de la respuesta no importa
    ignore_order: bool = False

    # Tolerancia para floats: abs(got - expected) <= float_tolerance
    # Default 1e-9 cubre errores de aritmética de punto flotante.
    # Usa 1e-6 si el problema permite ±1e-6 de error (típico en geometría/física).
    float_tolerance: float = 1e-9

    # Lista de outputs igualmente válidos.
    # Si got coincide con CUALQUIERA → correcto.
    # Ejemplo: {"valid_outputs": ["[0,1]", "[1,0]"]}
    valid_outputs: list = field(default_factory=list)

    # Validador personalizado: callable o clave de string (ver _VALIDATORS).
    # Firma: validator(got: Any, expected: Any, input_args: tuple) -> bool
    # Cuando se define, SOBRESCRIBE toda la lógica de comparación estándar.
    validator: Optional[Any] = None  # Callable | str | None


# ═══════════════════════════════════════════════════════════════════════════════
#  Registro de validadores con nombre (almacenables en MongoDB como string)
# ═══════════════════════════════════════════════════════════════════════════════

_VALIDATORS: dict[str, Callable] = {}


def register_validator(name: str):
    """Decorador para registrar un validador con clave de string."""
    def decorator(fn: Callable) -> Callable:
        _VALIDATORS[name] = fn
        return fn
    return decorator


@register_validator("two_sum")
def _val_two_sum(got: Any, expected: Any, args: tuple) -> bool:
    """
    Two Sum: got=[i,j] tal que nums[i]+nums[j]==target e i!=j.
    Ignora qué índices específicos devuelve; valida la restricción.
    Ejercicio típico donde hay múltiples respuestas válidas.
    """
    try:
        nums, target = args[0], args[1]
        i, j = int(got[0]), int(got[1])
        return i != j and nums[i] + nums[j] == target
    except Exception:
        return False


@register_validator("any_permutation")
def _val_any_permutation(got: Any, expected: Any, args: tuple) -> bool:
    """got es cualquier permutación de expected."""
    if not isinstance(got, list) or not isinstance(expected, list):
        return False
    if len(got) != len(expected):
        return False
    try:
        return sorted(got) == sorted(expected)
    except TypeError:
        # Elementos no comparables directamente → comparación profunda sin orden
        return _unordered_equal(list(got), list(expected), CompareConfig())


@register_validator("sorted_equal")
def _val_sorted_equal(got: Any, expected: Any, args: tuple) -> bool:
    """Compara got y expected después de ordenar ambos."""
    try:
        return sorted(got) == sorted(expected)
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════════════════════════
#  API pública
# ═══════════════════════════════════════════════════════════════════════════════

def compare_result(
    got_raw:      str,
    expected_raw: str,
    input_args:   tuple = (),
    config:       Optional[CompareConfig] = None,
) -> tuple[bool, str, str]:
    """
    Compara got vs expected de forma robusta.

    Parámetros:
        got_raw      — string bruto producido por el ejecutor (stdout line)
        expected_raw — string del campo expected_output del test case
        input_args   — tupla de argumentos parseados (para validadores custom)
        config       — CompareConfig (None → defaults)

    Retorna:
        (is_correct: bool, got_display: str, expected_display: str)
    """
    cfg = config or CompareConfig()

    # Parsear strings a valores Python
    got      = _parse(got_raw)
    expected = _parse(expected_raw)

    # ── Múltiples outputs válidos ────────────────────────────────────────────
    if cfg.valid_outputs:
        for valid_raw in cfg.valid_outputs:
            valid_val = _parse(str(valid_raw))
            if _deep_equal(got, valid_val, cfg):
                return True, _display(got), _display(expected)
        return False, _display(got), _display(expected)

    # ── Validador personalizado ──────────────────────────────────────────────
    validator = cfg.validator
    if isinstance(validator, str):
        validator = _VALIDATORS.get(validator)
    if callable(validator):
        try:
            ok = bool(validator(got, expected, input_args))
        except Exception:
            ok = False
        return ok, _display(got), _display(expected)

    # ── Comparación estándar profunda ────────────────────────────────────────
    ok = _deep_equal(got, expected, cfg)
    return ok, _display(got), _display(expected)


def compare_config_from_dict(d: Optional[dict]) -> CompareConfig:
    """
    Construye un CompareConfig desde un dict plano (almacenado en MongoDB).

    Ejemplo de campo compare_config en exercises_data.py:
        "compare_config": {
            "ignore_order":    True,
            "float_tolerance": 1e-6,
            "validator":       "two_sum",
            "valid_outputs":   ["[0,1]", "[1,0]"],
        }
    """
    if not d:
        return CompareConfig()
    return CompareConfig(
        ignore_order    = bool(d.get("ignore_order", False)),
        float_tolerance = float(d.get("float_tolerance", 1e-9)),
        valid_outputs   = list(d.get("valid_outputs", [])),
        validator       = d.get("validator"),   # str key → lookup en _VALIDATORS
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  Parsing — string → valor Python
# ═══════════════════════════════════════════════════════════════════════════════

def _parse(s: Any) -> Any:
    """
    Convierte el output bruto del ejecutor a un valor Python tipado.

    Orden de intentos:
      1. Marcadores internos del harness (__NONE__, __ERR__:...)
      2. Bool cross-language   (true/false/True/False)
      3. None cross-language   (None/null/nil)
      4. ast.literal_eval      (int, float, list, tuple, string con comillas)
      5. float()               (para "2.0", "3.14" sin comillas extra)
      6. Devuelve como string  (caso final: plain strings tipo "BANC", "Par")
    """
    if not isinstance(s, str):
        return s  # Ya es un valor Python

    s = s.strip()

    # Marcadores del harness Python
    if s == "__NONE__":
        return None
    if s.startswith("__ERR__:"):
        return s  # Propagado upstream, no debería llegar aquí

    # Bool cross-language
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False

    # None cross-language
    if s.lower() in ("none", "null", "nil"):
        return None

    # Python literal (int, float, list, tuple, str con comillas, nested)
    try:
        return ast.literal_eval(s)
    except Exception:
        pass

    # Float sin comillas ni literal reconocible (ej: "2.0" ya cubierto arriba,
    # pero por si acaso llega algo como "inf" o "nan")
    try:
        f = float(s)
        return f
    except ValueError:
        pass

    # Fallback: plain string
    return s


# ═══════════════════════════════════════════════════════════════════════════════
#  Deep equality
# ═══════════════════════════════════════════════════════════════════════════════

def _deep_equal(a: Any, b: Any, cfg: CompareConfig) -> bool:
    """
    Compara a y b recursivamente aplicando la configuración.
    """
    # ── None ────────────────────────────────────────────────────────────────
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False

    # ── Bool — antes que int (bool es subclase de int en Python) ────────────
    bool_a = _to_bool(a)
    bool_b = _to_bool(b)
    both_bool = (bool_a is not None) and (bool_b is not None)
    either_bool = (bool_a is not None) or (bool_b is not None)

    if both_bool:
        return bool_a == bool_b
    if either_bool:
        # Uno es bool y el otro no — no son iguales
        return False

    # ── Números con tolerancia ───────────────────────────────────────────────
    num_a = _to_float(a)
    num_b = _to_float(b)
    if num_a is not None and num_b is not None:
        if math.isnan(num_a) and math.isnan(num_b):
            return True
        if math.isinf(num_a) or math.isinf(num_b):
            return num_a == num_b
        return abs(num_a - num_b) <= cfg.float_tolerance

    # ── Listas / tuplas ──────────────────────────────────────────────────────
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            return False
        if cfg.ignore_order:
            return _unordered_equal(list(a), list(b), cfg)
        return all(_deep_equal(x, y, cfg) for x, y in zip(a, b))

    # ── Strings ──────────────────────────────────────────────────────────────
    if isinstance(a, str) and isinstance(b, str):
        return a.strip() == b.strip()

    # ── Último recurso: comparar como string ─────────────────────────────────
    return str(a).strip() == str(b).strip()


def _unordered_equal(a: list, b: list, cfg: CompareConfig) -> bool:
    """
    Compara dos listas sin importar el orden.
    Cada elemento de `a` debe emparejar con exactamente uno de `b`.
    O(n²) — suficiente para los tamaños típicos de un judge.
    """
    matched = [False] * len(b)
    for elem_a in a:
        found = False
        for j, elem_b in enumerate(b):
            if not matched[j] and _deep_equal(elem_a, elem_b, cfg):
                matched[j] = True
                found = True
                break
        if not found:
            return False
    return all(matched)


# ═══════════════════════════════════════════════════════════════════════════════
#  Type coercion helpers
# ═══════════════════════════════════════════════════════════════════════════════

def _to_bool(v: Any) -> Optional[bool]:
    """Convierte a bool si el valor es inequívocamente booleano. Si no, None."""
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        low = v.strip().lower()
        if low == "true":  return True
        if low == "false": return False
    return None


def _to_float(v: Any) -> Optional[float]:
    """Convierte a float si el valor es numérico. Bool excluido."""
    if isinstance(v, bool):
        return None  # bool es subclase de int, no queremos 1.0 == True
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v.strip())
        except ValueError:
            pass
    return None


# ═══════════════════════════════════════════════════════════════════════════════
#  Display — valor Python → string para la UI
# ═══════════════════════════════════════════════════════════════════════════════

def _display(v: Any) -> str:
    """
    Convierte un valor Python a un string legible para mostrar en la UI.
    Consistent con lo que los usuarios esperan ver (igual que Python repr
    pero sin comillas en strings planos y con floats legibles).
    """
    if v is None:
        return "None"
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, float):
        if math.isnan(v):   return "NaN"
        if math.isinf(v):   return "Inf" if v > 0 else "-Inf"
        # Entero exacto → mostrar .0 para que quede claro que es float
        if v == int(v):     return str(int(v)) + ".0"
        return str(v)
    if isinstance(v, int):
        return str(v)
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(_display(x) for x in v) + "]"
    if isinstance(v, str):
        return v   # plain, sin comillas extras
    return str(v)
