import React, { useState } from "react";
import http from "@/lib/api";
import { toast } from "sonner";
import MathText from "@/components/MathText";
import {
  Calculator, Play, Loader2, AlertTriangle, Sparkles, History, Wand2,
} from "lucide-react";

const OPERATIONS = [
  { id: "auto", label: "Auto-detect", hint: "We figure out what to do" },
  { id: "solve", label: "Solve", hint: "Solve for a variable" },
  { id: "differentiate", label: "Differentiate", hint: "Compute dy/dx" },
  { id: "integrate", label: "Integrate", hint: "Find the antiderivative" },
  { id: "factor", label: "Factor", hint: "Factor a polynomial" },
  { id: "expand", label: "Expand", hint: "Multiply out brackets" },
  { id: "simplify", label: "Simplify", hint: "Reduce to simplest form" },
  { id: "evaluate", label: "Evaluate", hint: "Numerical value" },
];

const EXAMPLES = [
  { op: "solve",         text: "x^2 - 5x + 6 = 0",      label: "Quadratic" },
  { op: "differentiate", text: "sin(x) * x^2",          label: "Product rule" },
  { op: "integrate",     text: "3x^2 + 2x",             label: "Power integration" },
  { op: "integrate",     text: "x^2 from 0 to 3",       label: "Definite integral" },
  { op: "factor",        text: "x^3 - 6x^2 + 11x - 6",  label: "Cubic factor" },
  { op: "expand",        text: "(2x + 1)^3",            label: "Binomial expand" },
  { op: "simplify",      text: "(x^2 - 1)/(x - 1)",     label: "Simplify rational" },
  { op: "evaluate",      text: "pi * 2.5^2",            label: "Area of circle" },
];

const Playground = () => {
  const [expression, setExpression] = useState("");
  const [operation, setOperation] = useState("auto");
  const [variable, setVariable] = useState("x");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]); // last 5 in-session solves

  const submit = async (overrideExpr, overrideOp) => {
    const ex = (overrideExpr ?? expression).trim();
    const op = overrideOp ?? operation;
    if (!ex) {
      toast.error("Type a math expression or equation first.");
      return;
    }
    setLoading(true);
    setResult(null);
    try {
      const { data } = await http.post("/playground/solve", {
        expression: ex, operation: op, variable: variable || "x",
      });
      setResult(data);
      if (data.ok) {
        setHistory((h) => [{ expression: ex, op, result: data }, ...h].slice(0, 5));
      } else {
        toast.error(data.error || "Could not solve that expression.");
      }
    } catch (err) {
      console.error("playground solve failed:", err);
      toast.error("Solver hit an error.");
    } finally {
      setLoading(false);
    }
  };

  const loadExample = (ex) => {
    setExpression(ex.text);
    setOperation(ex.op);
    submit(ex.text, ex.op);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid="playground-page">
      <div className="flex items-center gap-2">
        <Calculator size={18} className="text-terracotta" />
        <span className="overline">Equation playground</span>
      </div>
      <h1 className="font-heading text-4xl font-bold text-ink mt-2">
        Solve <span className="text-terracotta">anything.</span>
      </h1>
      <p className="text-muted2 mt-2 max-w-2xl">
        Type any equation or expression, pick what to do — and we'll show the worked solution.
        Powered by SymPy; LaTeX rendered via KaTeX.
      </p>

      {/* INPUT */}
      <div className="card-surface p-6 mt-8">
        <label className="overline" htmlFor="expr-input">Expression</label>
        <textarea
          id="expr-input"
          value={expression}
          onChange={(e) => setExpression(e.target.value)}
          placeholder="e.g.  x^2 - 5x + 6 = 0   ·   integrate sin(x)   ·   d/dx(x^3 + 2x)"
          rows={3}
          data-testid="playground-input"
          className="mt-2 w-full px-4 py-3 rounded-lg border border-edge bg-surface text-base font-mono focus:outline-none focus:ring-2 focus:ring-terracotta/30"
          onKeyDown={(e) => {
            if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) submit();
          }}
        />

        <div className="mt-4 grid sm:grid-cols-3 gap-3">
          <div>
            <label className="overline" htmlFor="op-select">Operation</label>
            <select
              id="op-select"
              value={operation}
              onChange={(e) => setOperation(e.target.value)}
              data-testid="playground-op-select"
              className="mt-1 w-full px-3 py-2.5 rounded-lg border border-edge bg-surface text-sm focus:outline-none focus:ring-2 focus:ring-terracotta/30"
            >
              {OPERATIONS.map((o) => (
                <option key={o.id} value={o.id}>{o.label} — {o.hint}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="overline" htmlFor="var-input">Variable</label>
            <input
              id="var-input"
              type="text"
              value={variable}
              onChange={(e) => setVariable(e.target.value.trim() || "x")}
              data-testid="playground-var-input"
              className="mt-1 w-full px-3 py-2.5 rounded-lg border border-edge bg-surface text-sm font-mono focus:outline-none focus:ring-2 focus:ring-terracotta/30"
            />
          </div>
          <div className="flex items-end">
            <button
              onClick={() => submit()}
              disabled={loading}
              className="btn-primary w-full inline-flex items-center justify-center gap-2 disabled:opacity-60"
              data-testid="playground-solve-btn"
            >
              {loading ? <Loader2 className="animate-spin" size={16} /> : <Play size={16} />}
              {loading ? "Solving…" : "Solve"}
            </button>
          </div>
        </div>

        {/* QUICK EXAMPLES */}
        <div className="mt-5">
          <div className="text-xs text-muted2 mb-2 flex items-center gap-1.5">
            <Sparkles size={12} /> Try one of these
          </div>
          <div className="flex flex-wrap gap-2" data-testid="playground-examples">
            {EXAMPLES.map((ex) => (
              <button
                key={`${ex.op}-${ex.text}`}
                onClick={() => loadExample(ex)}
                className="px-3 py-1.5 rounded-full border border-edge text-xs text-ink hover:border-terracotta/50 hover:bg-terracotta/5 transition"
                data-testid={`playground-example-${ex.op}`}
              >
                {ex.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* RESULT */}
      {result && result.ok && (
        <div className="card-surface p-6 mt-6" data-testid="playground-result">
          <div className="flex items-center justify-between flex-wrap gap-2">
            <span className="overline">{result.operation}</span>
            <span className="text-xs text-muted2 font-mono">solved by SymPy</span>
          </div>

          <div className="mt-4">
            <div className="text-xs text-muted2 uppercase tracking-wide">Input</div>
            <div className="mt-1 text-lg text-ink overflow-x-auto">
              <MathText text={`$$${result.input_latex}$$`} />
            </div>
          </div>

          <div className="mt-5">
            <div className="text-xs text-muted2 uppercase tracking-wide">Result</div>
            <div
              className="mt-1 text-2xl text-terracotta overflow-x-auto"
              data-testid="playground-result-latex"
            >
              <MathText text={`$$${result.result_latex}$$`} />
            </div>
          </div>

          <h3 className="font-heading text-lg font-semibold text-ink mt-6">Worked steps</h3>
          <ol className="mt-3 space-y-2">
            {result.steps.map((s, i) => (
              <li
                key={`step-${i}`}
                className="flex gap-3 text-ink"
                data-testid={`playground-step-${i}`}
              >
                <span className="font-mono text-xs bg-sand border border-edge px-2 py-0.5 rounded-md h-6 flex-shrink-0">
                  Step {i + 1}
                </span>
                <span className="overflow-x-auto"><MathText text={s} /></span>
              </li>
            ))}
          </ol>
        </div>
      )}

      {result && !result.ok && (
        <div
          className="card-surface p-6 mt-6 border border-error/30 bg-error/5"
          data-testid="playground-error"
        >
          <div className="flex items-center gap-2 text-error">
            <AlertTriangle size={18} />
            <span className="font-medium">Couldn't parse that.</span>
          </div>
          <p className="text-sm text-ink mt-2 font-mono">{result.error}</p>
          <p className="text-xs text-muted2 mt-3">
            Tip: use <code className="px-1 bg-sand rounded">x^2</code> for powers,
            <code className="px-1 bg-sand rounded ml-1">*</code> for multiplication, and put one
            equation per line.
          </p>
        </div>
      )}

      {/* HISTORY */}
      {history.length > 1 && (
        <div className="mt-8" data-testid="playground-history">
          <div className="flex items-center gap-2 text-muted2 mb-3">
            <History size={14} /> <span className="overline">Recent in this session</span>
          </div>
          <div className="space-y-2">
            {history.slice(1).map((h, i) => (
              <button
                key={`hist-${i}`}
                onClick={() => { setExpression(h.expression); setOperation(h.op); setResult(h.result); }}
                className="w-full text-left px-4 py-2.5 rounded-lg border border-edge bg-surface hover:border-terracotta/40 transition flex items-center gap-3"
                data-testid={`playground-history-${i}`}
              >
                <Wand2 size={12} className="text-terracotta flex-shrink-0" />
                <span className="text-xs font-mono text-muted2 uppercase">{h.op}</span>
                <span className="text-sm text-ink font-mono truncate flex-1">{h.expression}</span>
                <span className="text-xs text-muted2">→</span>
                <span className="text-sm text-terracotta truncate max-w-[40%]">
                  <MathText text={`$${h.result.result_latex}$`} />
                </span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Playground;
