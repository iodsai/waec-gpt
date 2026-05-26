"""Tests for the equation playground solver."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from playground_solver import solve_general


def test_solve_quadratic():
    r = solve_general("x^2 - 5*x + 6 = 0", "solve")
    assert r["ok"]
    sols = sorted(r["solutions"])
    assert sols == ["2", "3"]


def test_differentiate_polynomial():
    r = solve_general("x^3 + 2*x", "differentiate")
    assert r["ok"]
    assert "3 x^{2}" in r["result_latex"]


def test_integrate_definite():
    r = solve_general("x^2 from 0 to 3", "integrate")
    assert r["ok"]
    assert r["result_latex"] == "9"


def test_integrate_indefinite():
    r = solve_general("3*x^2", "integrate")
    assert r["ok"]
    assert "x^{3}" in r["result_latex"]
    assert "C" in r["result_latex"]


def test_factor_cubic():
    r = solve_general("x^3 - 6*x^2 + 11*x - 6", "factor")
    assert r["ok"]
    # Factors should each appear
    assert "x - 1" in r["result_latex"]
    assert "x - 2" in r["result_latex"]
    assert "x - 3" in r["result_latex"]


def test_expand_binomial():
    r = solve_general("(x + 1)^3", "expand")
    assert r["ok"]
    assert "x^{3}" in r["result_latex"]
    assert "3 x^{2}" in r["result_latex"]


def test_simplify_rational():
    r = solve_general("(x^2 - 1)/(x - 1)", "simplify")
    assert r["ok"]
    # Either "x + 1" or order swapped
    assert "x" in r["result_latex"]


def test_auto_detect_solve():
    r = solve_general("2*x + 1 = 5", "auto")
    assert r["ok"]
    assert r["operation"] == "solve"
    assert r["solutions"] == ["2"]


def test_auto_detect_simplify():
    r = solve_general("2*x + 3*x", "auto")
    assert r["ok"]
    assert r["operation"] == "simplify"


def test_evaluate_pi():
    r = solve_general("pi * 2.5^2", "evaluate")
    assert r["ok"]
    val = float(r["result_latex"])
    assert 19.5 < val < 19.7  # pi * 6.25 ≈ 19.6349...


def test_invalid_input():
    r = solve_general("xyz === 5", "solve")
    assert not r["ok"]
    assert r["error"] is not None


def test_latex_input():
    r = solve_general("\\frac{x^2 + 2x + 1}{x + 1}", "simplify")
    assert r["ok"]
