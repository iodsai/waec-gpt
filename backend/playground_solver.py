"""Equation playground — general-purpose SymPy solver with worked steps.

Operations supported:
  - solve: solve equation(s) for a variable
  - differentiate: dy/dx of an expression
  - integrate: indefinite/definite integral
  - simplify: simplify an expression
  - factor: factor a polynomial
  - expand: expand a product/power
  - evaluate: numerically evaluate
  - auto: detect from the input
"""

from sympy import (
    sympify, Eq, solve, simplify, symbols, Symbol,
    diff, integrate, expand, factor, together, latex,
    N as sym_N, S, lambdify as sym_lambdify,
)
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application,
    convert_xor,
)
import re

TRANSFORMS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


def _clean(expr: str) -> str:
    """Normalise common LaTeX / typed math notations into SymPy-parseable strings."""
    expr = (expr or "").strip().strip("$").strip()
    # Common symbol replacements
    expr = expr.replace("\\times", "*").replace("×", "*")
    expr = expr.replace("÷", "/").replace("\\div", "/")
    expr = expr.replace("\\cdot", "*").replace("·", "*")
    expr = expr.replace("π", "pi").replace("\\pi", "pi")
    expr = expr.replace("∞", "oo").replace("\\infty", "oo")
    # LaTeX commands
    expr = re.sub(r"\\frac\{([^}]+)\}\{([^}]+)\}", r"((\1)/(\2))", expr)
    expr = re.sub(r"\\sqrt\{([^}]+)\}", r"sqrt(\1)", expr)
    expr = re.sub(r"\\(sin|cos|tan|log|ln|exp)\b", r"\1", expr)
    expr = re.sub(r"\\(left|right)", "", expr)
    # Drop remaining braces (after fracs are handled)
    expr = expr.replace("{", "(").replace("}", ")")
    return expr.strip()


def _parse(expr: str):
    return parse_expr(expr, transformations=TRANSFORMS, evaluate=False)


def _detect_operation(raw: str) -> str:
    """Heuristically pick an operation when the caller passes 'auto'."""
    s = raw.lower()
    if any(k in s for k in ("d/dx", "dy/dx", "differentiate", "derivative")):
        return "differentiate"
    if any(k in s for k in ("integrate", "∫", "\\int")):
        return "integrate"
    if any(k in s for k in ("factor",)):
        return "factor"
    if any(k in s for k in ("expand",)):
        return "expand"
    if any(k in s for k in ("simplify",)):
        return "simplify"
    # Default heuristic: presence of '=' → solve; else simplify
    if "=" in raw:
        return "solve"
    return "simplify"


def _strip_op_keywords(raw: str) -> str:
    """Remove operation hint words so we can keep what's left as the expression."""
    s = raw
    for kw in ("differentiate", "derivative of", "d/dx", "dy/dx",
              "integrate", "integral of", "∫", "\\int",
              "factor", "expand", "simplify"):
        s = re.sub(re.escape(kw), "", s, flags=re.IGNORECASE)
    return s.strip()


def solve_general(raw: str, operation: str = "auto", variable: str = "x") -> dict:
    """Main entry point. Returns a JSON-friendly dict."""
    if not raw or not raw.strip():
        return _err("Empty input.")
    try:
        op = operation if operation and operation != "auto" else _detect_operation(raw)
        rest = _strip_op_keywords(raw)
        cleaned = _clean(rest)
        var = symbols(variable)

        if op == "solve":
            return _do_solve(cleaned, var, variable)
        if op == "differentiate":
            return _do_diff(cleaned, var, variable)
        if op == "integrate":
            return _do_integrate(cleaned, var, variable)
        if op == "factor":
            return _do_factor(cleaned, var)
        if op == "expand":
            return _do_expand(cleaned, var)
        if op == "simplify":
            return _do_simplify(cleaned, var)
        if op == "evaluate":
            return _do_evaluate(cleaned)
        return _err(f"Unknown operation: {op}")
    except Exception as e:
        return _err(str(e))


def _ok(operation: str, input_latex: str, result_latex: str, steps: list, extra: dict | None = None):
    out = {
        "ok": True,
        "operation": operation,
        "input_latex": input_latex,
        "result_latex": result_latex,
        "steps": steps,
        "error": None,
    }
    if extra:
        out.update(extra)
    return out


def _err(msg: str):
    return {
        "ok": False,
        "operation": None,
        "input_latex": None,
        "result_latex": None,
        "steps": [],
        "error": msg,
    }


def _do_solve(cleaned: str, var, variable: str):
    if "=" in cleaned:
        lhs, rhs = cleaned.split("=", 1)
        lhs_p, rhs_p = _parse(lhs), _parse(rhs)
    else:
        lhs_p, rhs_p = _parse(cleaned), S.Zero
    eq = Eq(lhs_p, rhs_p)
    sols = solve(eq, var)
    sols_simplified = [simplify(s) for s in sols] if sols else []
    steps = [
        f"Start with the equation: {latex(eq)}",
        f"Rearrange to standard form: {latex(Eq(simplify(lhs_p - rhs_p), 0))}",
    ]
    if not sols:
        steps.append("No solution found in the real numbers.")
        result_latex = "\\text{No solution}"
    else:
        steps.append(f"Solve for ${variable}$ using SymPy's algebraic solver.")
        result_pieces = [latex(s) for s in sols_simplified]
        result_latex = f"{variable} = " + ",\\quad {variable} = ".join(result_pieces).replace("{variable}", variable)
        steps.append(f"Solution{'s' if len(sols_simplified) > 1 else ''}: ${result_latex}$")
    return _ok("solve", latex(eq), result_latex, steps, {"solutions": [str(s) for s in sols_simplified]})


def _do_diff(cleaned: str, var, variable: str):
    expr = _parse(cleaned)
    der = simplify(diff(expr, var))
    steps = [
        f"Differentiate $f({variable}) = {latex(expr)}$ with respect to ${variable}$.",
        f"Apply standard differentiation rules (power, product, chain, etc.).",
        f"Simplify the result: $\\frac{{d}}{{d{variable}}}\\left({latex(expr)}\\right) = {latex(der)}$",
    ]
    return _ok("differentiate", latex(expr), latex(der), steps)


def _do_integrate(cleaned: str, var, variable: str):
    # Support 'a..b' definite bounds like '0..pi'
    bounds = None
    m = re.search(r"\bfrom\s+([^\s]+)\s+to\s+([^\s]+)\b", cleaned, flags=re.IGNORECASE)
    if m:
        bounds = (m.group(1), m.group(2))
        cleaned = re.sub(r"\bfrom\s+[^\s]+\s+to\s+[^\s]+\b", "", cleaned, flags=re.IGNORECASE).strip()
    expr = _parse(cleaned)
    if bounds:
        a, b = _parse(bounds[0]), _parse(bounds[1])
        antider = simplify(integrate(expr, var))
        val = simplify(integrate(expr, (var, a, b)))
        steps = [
            f"Find the antiderivative of ${latex(expr)}$.",
            f"$\\int {latex(expr)} \\, d{variable} = {latex(antider)} + C$",
            f"Evaluate from ${latex(a)}$ to ${latex(b)}$:",
            f"$\\int_{{{latex(a)}}}^{{{latex(b)}}} {latex(expr)} \\, d{variable} = {latex(val)}$",
        ]
        return _ok("integrate", latex(expr), latex(val), steps)
    antider = simplify(integrate(expr, var))
    steps = [
        f"Integrate ${latex(expr)}$ with respect to ${variable}$.",
        f"Apply the appropriate integration rule.",
        f"$\\int {latex(expr)} \\, d{variable} = {latex(antider)} + C$",
    ]
    return _ok("integrate", latex(expr), f"{latex(antider)} + C", steps)


def _do_factor(cleaned: str, var):
    expr = _parse(cleaned)
    factored = factor(expr)
    steps = [
        f"Start with ${latex(expr)}$.",
        f"Find common structure / roots.",
        f"Factored form: ${latex(factored)}$",
    ]
    return _ok("factor", latex(expr), latex(factored), steps)


def _do_expand(cleaned: str, var):
    expr = _parse(cleaned)
    expanded = expand(expr)
    steps = [
        f"Start with ${latex(expr)}$.",
        f"Multiply out brackets and combine like terms.",
        f"Expanded form: ${latex(expanded)}$",
    ]
    return _ok("expand", latex(expr), latex(expanded), steps)


def _do_simplify(cleaned: str, var):
    expr = _parse(cleaned)
    simp = simplify(expr)
    # If simplification didn't change anything, try together() to combine fractions
    if simp == expr:
        simp = together(simp)
    steps = [
        f"Start with ${latex(expr)}$.",
        f"Combine like terms and reduce.",
        f"Simplified: ${latex(simp)}$",
    ]
    return _ok("simplify", latex(expr), latex(simp), steps)


def _do_evaluate(cleaned: str):
    expr = _parse(cleaned)
    val = sym_N(expr, 8)
    steps = [
        f"Start with ${latex(expr)}$.",
        f"Numerically evaluate to 8 significant figures.",
        f"Result: ${latex(val)}$",
    ]
    return _ok("evaluate", latex(expr), latex(val), steps)


def graph_function(raw: str, variable: str = "x", x_min: float = -10.0, x_max: float = 10.0,
                   samples: int = 200) -> dict:
    """Sample a function over [x_min, x_max] and return points + the LaTeX of the expression.
    Returns: { ok, latex, points: [{x, y}], asymptotes_clipped: bool, error }
    """
    if not raw or not raw.strip():
        return {"ok": False, "points": [], "latex": None, "error": "Empty expression."}
    try:
        # Allow forms like "y = x^2 + 1" or "f(x) = sin(x)"
        rest = raw
        if "=" in rest:
            rest = rest.split("=", 1)[1]
        cleaned = _clean(rest)
        expr = _parse(cleaned)
        var = symbols(variable)
        try:
            f = sym_lambdify(var, expr, modules=["math"])
        except Exception as e:
            return {"ok": False, "points": [], "latex": latex(expr), "error": f"Could not turn into a function: {e}"}

        step = (x_max - x_min) / max(2, samples - 1)
        points = []
        clipped = False
        for i in range(samples):
            xv = x_min + step * i
            try:
                yv = f(xv)
                if isinstance(yv, complex):
                    yv = yv.real if abs(yv.imag) < 1e-9 else None
                if yv is None or yv != yv or yv == float("inf") or yv == float("-inf"):
                    points.append({"x": round(xv, 6), "y": None})
                    continue
                # Clip extreme magnitudes for sane axis scaling
                if abs(yv) > 1e6:
                    clipped = True
                    yv = 1e6 if yv > 0 else -1e6
                points.append({"x": round(xv, 6), "y": round(float(yv), 6)})
            except Exception:
                points.append({"x": round(xv, 6), "y": None})
        return {
            "ok": True,
            "latex": latex(expr),
            "points": points,
            "asymptotes_clipped": clipped,
            "error": None,
        }
    except Exception as e:
        return {"ok": False, "points": [], "latex": None, "error": str(e)}
