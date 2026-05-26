import React, { useState } from "react";
import { ChevronDown, Delete, X } from "lucide-react";

/**
 * Compact math keypad — inserts LaTeX/SymPy-friendly tokens at the textarea cursor.
 *
 * Usage:
 *   const ref = useRef(null);
 *   <textarea ref={ref} ... />
 *   <MathKeypad targetRef={ref} value={value} onChange={setValue} />
 */

// A key inserts `text`; if `cursorOffset` provided, the caret lands at insertPos + cursorOffset
// (useful for templates like `\frac{|}{}` → cursor between the braces).
const K = (label, text, cursorOffset = null) => ({ label, text, cursorOffset });

const SECTIONS = {
  basic: {
    label: "Basics",
    rows: [
      [K("7", "7"), K("8", "8"), K("9", "9"), K("÷", "/"), K("(", "("), K(")", ")")],
      [K("4", "4"), K("5", "5"), K("6", "6"), K("×", "*"), K("xⁿ", "^"), K("√", "sqrt(", 5)],
      [K("1", "1"), K("2", "2"), K("3", "3"), K("−", "-"), K("=", "="), K("π", "pi")],
      [K("0", "0"), K(".", "."), K(",", ", "), K("+", "+"), K("x", "x"), K("y", "y")],
    ],
  },
  calculus: {
    label: "Calculus",
    rows: [
      [K("d/dx", "d/dx ", 0), K("∫", "integrate "), K("∫ₐᵇ", "from a to b "),
       K("lim", "limit("), K("∞", "oo"), K("e^", "exp(")],
      [K("sin", "sin("), K("cos", "cos("), K("tan", "tan("),
       K("ln", "ln("), K("log", "log("), K("|x|", "Abs(")],
      [K("dx", " dx"), K("dy", " dy"), K("dθ", " dtheta"),
       K("²", "^2"), K("³", "^3"), K("ⁿ", "^n")],
    ],
  },
  algebra: {
    label: "Algebra",
    rows: [
      [K("frac", "\\frac{}{}", -4), K("nCr", "binomial(n,r)"), K("nPr", "factorial(n)/factorial(n-r)"),
       K("|x|", "Abs("), K("⌊x⌋", "floor("), K("⌈x⌉", "ceiling(")],
      [K("α", "alpha"), K("β", "beta"), K("θ", "theta"),
       K("≤", "<="), K("≥", ">="), K("≠", "!=")],
      [K("±", " ± "), K("Σ", "Sum("), K("Π", "Product("),
       K("→", " -> "), K("⇒", " ⇒ "), K("∈", " in ")],
    ],
  },
  vectors: {
    label: "Vectors",
    rows: [
      [K("â", "hat(a)"), K("b̂", "hat(b)"), K("|v|", "Abs("),
       K("·", " * "), K("×", " cross "), K("→AB", " AB ")],
      [K("i", "i"), K("j", "j"), K("k", "k"),
       K("(x,y)", "(,)"), K("[x;y]", "Matrix([[x],[y]])"), K("[a b]", "Matrix([[a,b]])")],
    ],
  },
};

const MathKeypad = ({ targetRef, value, onChange, defaultOpen = false }) => {
  const [open, setOpen] = useState(defaultOpen);
  const [tab, setTab] = useState("basic");

  const insert = (text, cursorOffset = null) => {
    const el = targetRef?.current;
    if (!el) {
      onChange((value || "") + text);
      return;
    }
    const start = el.selectionStart ?? value.length;
    const end = el.selectionEnd ?? value.length;
    const next = (value || "").slice(0, start) + text + (value || "").slice(end);
    onChange(next);
    // restore caret on next tick
    requestAnimationFrame(() => {
      el.focus();
      const newPos = cursorOffset !== null
        ? start + text.length + cursorOffset
        : start + text.length;
      try { el.setSelectionRange(newPos, newPos); } catch (_) { /* noop */ }
    });
  };

  const backspace = () => {
    const el = targetRef?.current;
    if (!el) return onChange((value || "").slice(0, -1));
    const start = el.selectionStart ?? value.length;
    const end = el.selectionEnd ?? value.length;
    if (start === end && start > 0) {
      const next = value.slice(0, start - 1) + value.slice(end);
      onChange(next);
      requestAnimationFrame(() => {
        el.focus();
        try { el.setSelectionRange(start - 1, start - 1); } catch (_) { /* noop */ }
      });
    } else if (start !== end) {
      const next = value.slice(0, start) + value.slice(end);
      onChange(next);
      requestAnimationFrame(() => {
        el.focus();
        try { el.setSelectionRange(start, start); } catch (_) { /* noop */ }
      });
    }
  };

  const clear = () => { onChange(""); targetRef?.current?.focus(); };

  return (
    <div className="mt-3" data-testid="math-keypad">
      <div className="flex items-center gap-2">
        <button
          type="button"
          onClick={() => setOpen((o) => !o)}
          className="px-3 py-1.5 rounded-lg border border-edge text-xs font-medium text-ink hover:border-terracotta/50 hover:bg-terracotta/5 inline-flex items-center gap-1.5"
          data-testid="math-keypad-toggle"
          aria-expanded={open}
        >
          <ChevronDown
            size={14}
            className={`transition-transform ${open ? "rotate-180" : ""}`}
          />
          {open ? "Hide" : "Show"} math keyboard
        </button>
        {open && (
          <>
            <button
              type="button"
              onClick={backspace}
              className="px-2.5 py-1.5 rounded-lg border border-edge text-xs text-muted2 hover:text-error hover:border-error/40 inline-flex items-center gap-1"
              data-testid="math-keypad-backspace"
              aria-label="Backspace"
            >
              <Delete size={14} />
            </button>
            <button
              type="button"
              onClick={clear}
              className="px-2.5 py-1.5 rounded-lg border border-edge text-xs text-muted2 hover:text-error hover:border-error/40 inline-flex items-center gap-1"
              data-testid="math-keypad-clear"
            >
              <X size={12} /> Clear
            </button>
          </>
        )}
      </div>

      {open && (
        <div className="mt-3 card-surface p-3 sm:p-4 border" data-testid="math-keypad-panel">
          {/* Tab strip */}
          <div className="flex gap-1.5 overflow-x-auto pb-2" role="tablist">
            {Object.entries(SECTIONS).map(([id, s]) => (
              <button
                key={id}
                type="button"
                onClick={() => setTab(id)}
                role="tab"
                aria-selected={tab === id}
                data-testid={`math-keypad-tab-${id}`}
                className={`px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap transition
                  ${tab === id
                    ? "bg-terracotta text-white"
                    : "border border-edge text-muted2 hover:text-ink hover:border-terracotta/30"}`}
              >
                {s.label}
              </button>
            ))}
          </div>

          {/* Keys grid */}
          <div className="mt-3 space-y-1.5">
            {SECTIONS[tab].rows.map((row, ri) => (
              <div key={`row-${ri}`} className="grid grid-cols-6 gap-1.5">
                {row.map((k, ki) => (
                  <button
                    key={`k-${ri}-${ki}-${k.label}`}
                    type="button"
                    onClick={() => insert(k.text, k.cursorOffset)}
                    data-testid={`math-key-${k.label}`}
                    className="py-2.5 rounded-lg border border-edge bg-surface text-sm font-mono text-ink hover:bg-terracotta/10 hover:border-terracotta/50 active:scale-95 transition"
                  >
                    {k.label}
                  </button>
                ))}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default MathKeypad;
