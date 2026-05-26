import React, { useMemo, useState } from "react";
import MathText from "@/components/MathText";
import { Search, Printer, BookOpen } from "lucide-react";

const FORMULAS = [
  // ============ STATISTICS & PROBABILITY ============
  { topic: "Statistics & Probability", formulas: [
    { name: "Mean (ungrouped)", latex: "\\bar{x} = \\frac{\\sum x_i}{n}" },
    { name: "Mean (grouped)", latex: "\\bar{x} = \\frac{\\sum f x}{\\sum f}" },
    { name: "Variance", latex: "\\sigma^2 = \\frac{\\sum (x - \\bar{x})^2}{n}" },
    { name: "Standard deviation", latex: "\\sigma = \\sqrt{\\frac{\\sum (x - \\bar{x})^2}{n}}" },
    { name: "Pearson correlation", latex: "r = \\frac{n\\sum xy - \\sum x \\sum y}{\\sqrt{[n\\sum x^2 - (\\sum x)^2][n\\sum y^2 - (\\sum y)^2]}}" },
    { name: "Spearman rank correlation", latex: "\\rho = 1 - \\frac{6 \\sum d^2}{n(n^2 - 1)}" },
    { name: "Probability (independent)", latex: "P(A \\cap B) = P(A) \\cdot P(B)" },
    { name: "Conditional probability", latex: "P(A | B) = \\frac{P(A \\cap B)}{P(B)}" },
    { name: "Permutation", latex: "{}^nP_r = \\frac{n!}{(n-r)!}" },
    { name: "Combination", latex: "{}^nC_r = \\binom{n}{r} = \\frac{n!}{r!(n-r)!}" },
  ]},

  // ============ CALCULUS ============
  { topic: "Calculus", formulas: [
    { name: "Derivative (power rule)", latex: "\\frac{d}{dx}(x^n) = nx^{n-1}" },
    { name: "Derivative of sin/cos", latex: "\\frac{d}{dx}(\\sin x) = \\cos x, \\quad \\frac{d}{dx}(\\cos x) = -\\sin x" },
    { name: "Derivative of exp/log", latex: "\\frac{d}{dx}(e^x) = e^x, \\quad \\frac{d}{dx}(\\ln x) = \\frac{1}{x}" },
    { name: "Product rule", latex: "(uv)' = u'v + uv'" },
    { name: "Quotient rule", latex: "\\left(\\frac{u}{v}\\right)' = \\frac{u'v - uv'}{v^2}" },
    { name: "Chain rule", latex: "\\frac{dy}{dx} = \\frac{dy}{du} \\cdot \\frac{du}{dx}" },
    { name: "Stationary points", latex: "\\frac{dy}{dx} = 0; \\text{ max if } \\frac{d^2y}{dx^2} < 0, \\text{ min if } > 0" },
    { name: "Integration (power)", latex: "\\int x^n \\, dx = \\frac{x^{n+1}}{n+1} + C, \\; n \\neq -1" },
    { name: "Integration of 1/x", latex: "\\int \\frac{1}{x} \\, dx = \\ln|x| + C" },
    { name: "Definite integral", latex: "\\int_a^b f(x) \\, dx = F(b) - F(a)" },
    { name: "Area under curve", latex: "A = \\int_a^b y \\, dx" },
    { name: "Volume of revolution", latex: "V = \\pi \\int_a^b y^2 \\, dx" },
    { name: "Limit definition", latex: "\\lim_{x \\to a} f(x) = L" },
  ]},

  // ============ VECTORS ============
  { topic: "Vectors", formulas: [
    { name: "Magnitude (2D)", latex: "|\\vec{a}| = \\sqrt{a_1^2 + a_2^2}" },
    { name: "Magnitude (3D)", latex: "|\\vec{a}| = \\sqrt{a_1^2 + a_2^2 + a_3^2}" },
    { name: "Unit vector", latex: "\\hat{a} = \\frac{\\vec{a}}{|\\vec{a}|}" },
    { name: "Dot product", latex: "\\vec{a} \\cdot \\vec{b} = a_1 b_1 + a_2 b_2 + a_3 b_3 = |\\vec{a}||\\vec{b}|\\cos\\theta" },
    { name: "Angle between vectors", latex: "\\cos\\theta = \\frac{\\vec{a} \\cdot \\vec{b}}{|\\vec{a}||\\vec{b}|}" },
    { name: "Perpendicular condition", latex: "\\vec{a} \\cdot \\vec{b} = 0" },
    { name: "Parallel condition", latex: "\\vec{a} = k\\vec{b}" },
    { name: "Position vector (midpoint)", latex: "\\vec{m} = \\frac{\\vec{a} + \\vec{b}}{2}" },
    { name: "Position vector (ratio)", latex: "\\vec{p} = \\frac{n\\vec{a} + m\\vec{b}}{m+n}" },
  ]},

  // ============ SETS & LOGIC ============
  { topic: "Sets & Logic", formulas: [
    { name: "Union cardinality", latex: "n(A \\cup B) = n(A) + n(B) - n(A \\cap B)" },
    { name: "Triple union", latex: "n(A \\cup B \\cup C) = n(A)+n(B)+n(C) - n(A\\cap B) - n(A\\cap C) - n(B\\cap C) + n(A\\cap B\\cap C)" },
    { name: "De Morgan's Laws", latex: "(A \\cup B)' = A' \\cap B', \\quad (A \\cap B)' = A' \\cup B'" },
    { name: "Implication equivalence", latex: "p \\rightarrow q \\equiv \\neg p \\lor q" },
    { name: "Contrapositive", latex: "p \\rightarrow q \\equiv \\neg q \\rightarrow \\neg p" },
  ]},

  // ============ SURDS & POLYNOMIALS ============
  { topic: "Surds & Polynomials", formulas: [
    { name: "Surd multiplication", latex: "\\sqrt{a} \\cdot \\sqrt{b} = \\sqrt{ab}" },
    { name: "Rationalise denominator", latex: "\\frac{1}{a + \\sqrt{b}} = \\frac{a - \\sqrt{b}}{a^2 - b}" },
    { name: "Difference of squares", latex: "a^2 - b^2 = (a+b)(a-b)" },
    { name: "Sum/diff of cubes", latex: "a^3 \\pm b^3 = (a \\pm b)(a^2 \\mp ab + b^2)" },
    { name: "Remainder theorem", latex: "f(x) \\div (x-a) \\Rightarrow \\text{remainder} = f(a)" },
    { name: "Factor theorem", latex: "(x-a) \\text{ is a factor of } f(x) \\iff f(a) = 0" },
    { name: "Quadratic formula", latex: "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}" },
    { name: "Sum/product of roots", latex: "\\alpha + \\beta = -\\frac{b}{a}, \\quad \\alpha\\beta = \\frac{c}{a}" },
  ]},

  // ============ SEQUENCES & BINOMIAL ============
  { topic: "Sequences & Binomial", formulas: [
    { name: "AP n-th term", latex: "T_n = a + (n-1)d" },
    { name: "AP sum", latex: "S_n = \\frac{n}{2}[2a + (n-1)d] = \\frac{n}{2}(a + l)" },
    { name: "GP n-th term", latex: "T_n = ar^{n-1}" },
    { name: "GP sum", latex: "S_n = \\frac{a(r^n - 1)}{r - 1}, \\quad r \\neq 1" },
    { name: "GP sum to infinity", latex: "S_\\infty = \\frac{a}{1 - r}, \\; |r| < 1" },
    { name: "Binomial theorem", latex: "(a+b)^n = \\sum_{k=0}^{n} \\binom{n}{k} a^{n-k} b^k" },
    { name: "Binomial coefficient", latex: "\\binom{n}{k} = \\frac{n!}{k!(n-k)!}" },
  ]},

  // ============ MATRICES ============
  { topic: "Matrices", formulas: [
    { name: "2×2 determinant", latex: "\\det\\begin{pmatrix}a & b\\\\c & d\\end{pmatrix} = ad - bc" },
    { name: "2×2 inverse", latex: "A^{-1} = \\frac{1}{\\det A} \\begin{pmatrix}d & -b\\\\-c & a\\end{pmatrix}" },
    { name: "Singular matrix", latex: "\\det A = 0 \\iff A \\text{ is singular (no inverse)}" },
    { name: "Scalar multiple (det)", latex: "\\det(kA) = k^n \\det A \\; (n \\times n)" },
    { name: "Product determinant", latex: "\\det(AB) = \\det A \\cdot \\det B" },
    { name: "Cramer's rule", latex: "x_i = \\frac{\\det A_i}{\\det A}" },
  ]},

  // ============ MECHANICS ============
  { topic: "Mechanics", formulas: [
    { name: "Velocity", latex: "v = u + at" },
    { name: "Displacement (1)", latex: "s = ut + \\tfrac{1}{2}at^2" },
    { name: "Displacement (2)", latex: "s = \\tfrac{1}{2}(u + v)t" },
    { name: "Velocity squared", latex: "v^2 = u^2 + 2as" },
    { name: "Newton's 2nd law", latex: "F = ma" },
    { name: "Weight", latex: "W = mg" },
    { name: "Work done", latex: "W = Fs" },
    { name: "Kinetic energy", latex: "KE = \\tfrac{1}{2}mv^2" },
    { name: "Potential energy", latex: "PE = mgh" },
    { name: "Power", latex: "P = \\frac{W}{t} = Fv" },
    { name: "Momentum", latex: "p = mv" },
    { name: "Impulse", latex: "J = Ft = \\Delta p" },
  ]},
];

const FormulaSheet = () => {
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return FORMULAS;
    return FORMULAS.map((g) => ({
      ...g,
      formulas: g.formulas.filter(
        (f) => f.name.toLowerCase().includes(q) || f.latex.toLowerCase().includes(q)
      ),
    })).filter((g) => g.formulas.length > 0);
  }, [query]);

  const totalCount = filtered.reduce((acc, g) => acc + g.formulas.length, 0);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid="formula-sheet-page">
      <div className="flex items-start justify-between gap-4 flex-wrap print:hidden">
        <div>
          <div className="flex items-center gap-2">
            <BookOpen size={18} className="text-terracotta" />
            <span className="overline">Quick reference</span>
          </div>
          <h1 className="font-heading text-4xl font-bold text-ink mt-2">Formula sheet</h1>
          <p className="text-muted2 mt-2">
            Every formula you need for WAEC Further Maths. Searchable, printable, screenshot-friendly.
          </p>
        </div>
        <button
          onClick={() => window.print()}
          className="btn-secondary inline-flex items-center gap-2"
          data-testid="formula-print-btn"
        >
          <Printer size={16} /> Print / save PDF
        </button>
      </div>

      <div className="mt-6 print:hidden">
        <div className="relative max-w-md">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted2" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search formulas (e.g. 'derivative', 'binomial', 'dot')"
            data-testid="formula-search"
            className="w-full pl-9 pr-3 py-2.5 rounded-lg border border-edge bg-surface text-sm focus:outline-none focus:ring-2 focus:ring-terracotta/30"
          />
        </div>
        {query && (
          <p className="text-xs text-muted2 mt-2" data-testid="formula-results-count">
            {totalCount} {totalCount === 1 ? "result" : "results"} matching "{query}"
          </p>
        )}
      </div>

      <div className="mt-8 space-y-10 print:space-y-6">
        {filtered.map((group) => (
          <section key={group.topic} data-testid={`formula-group-${group.topic.toLowerCase().replace(/\s+/g, "-")}`}>
            <h2 className="font-heading text-2xl font-semibold text-ink mb-4 print:text-xl">
              {group.topic}
            </h2>
            <div className="grid sm:grid-cols-2 gap-3 print:grid-cols-2 print:gap-2">
              {group.formulas.map((f) => (
                <div
                  key={`${group.topic}-${f.name}`}
                  className="card-surface p-4 print:border print:shadow-none"
                  data-testid={`formula-${f.name.toLowerCase().replace(/\s+/g, "-")}`}
                >
                  <div className="text-xs text-muted2 uppercase tracking-wide">{f.name}</div>
                  <div className="mt-2 text-ink overflow-x-auto">
                    <MathText text={`$$${f.latex}$$`} />
                  </div>
                </div>
              ))}
            </div>
          </section>
        ))}

        {filtered.length === 0 && (
          <div className="text-center py-16 text-muted2" data-testid="formula-empty">
            No formulas match "{query}". Try a different keyword.
          </div>
        )}
      </div>
    </div>
  );
};

export default FormulaSheet;
