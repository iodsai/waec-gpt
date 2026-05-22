"""SymPy verification for math expressions."""
from sympy import sympify, Eq, solve, simplify, symbols, S, Symbol
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re

TRANSFORMS = standard_transformations + (implicit_multiplication_application,)

def _clean(expr: str) -> str:
    expr = expr.strip()
    # Remove $...$ wrappers
    expr = expr.strip("$").strip()
    # Replace common notations
    expr = expr.replace("\\times", "*").replace("×", "*")
    expr = expr.replace("÷", "/")
    expr = expr.replace("^", "**")
    # Remove LaTeX commands
    expr = re.sub(r"\\frac\{([^}]+)\}\{([^}]+)\}", r"(\1)/(\2)", expr)
    expr = re.sub(r"\\sqrt\{([^}]+)\}", r"sqrt(\1)", expr)
    expr = re.sub(r"\\(left|right)", "", expr)
    expr = expr.replace("{", "(").replace("}", ")")
    return expr.strip()

def verify(equation: str, claimed_answer: str | None = None, variable: str = "x") -> dict:
    """Verify an algebraic equation. Returns:
        { ok, solutions (list[str]), matches_claim (bool|None), interpreted, error }
    """
    try:
        cleaned = _clean(equation)
        x = symbols(variable)
        if "=" in cleaned:
            lhs, rhs = cleaned.split("=", 1)
            eq = Eq(parse_expr(lhs.strip(), transformations=TRANSFORMS, evaluate=False),
                    parse_expr(rhs.strip(), transformations=TRANSFORMS, evaluate=False))
        else:
            eq = Eq(parse_expr(cleaned, transformations=TRANSFORMS, evaluate=False), 0)
        sols = solve(eq, x)
        sols_str = [str(simplify(s)) for s in sols]
        matches = None
        if claimed_answer is not None:
            try:
                claim_clean = _clean(claimed_answer)
                claim_val = parse_expr(claim_clean, transformations=TRANSFORMS)
                matches = any(simplify(claim_val - s) == 0 for s in sols)
            except Exception:
                matches = None
        return {
            "ok": True,
            "solutions": sols_str,
            "matches_claim": matches,
            "interpreted": f"{eq}",
            "error": None,
        }
    except Exception as e:
        return {"ok": False, "solutions": [], "matches_claim": None, "interpreted": None, "error": str(e)}
