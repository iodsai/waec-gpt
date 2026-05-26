import React, { useState, useRef } from "react";
import http from "@/lib/api";
import { toast } from "sonner";
import MathText from "@/components/MathText";
import MathKeypad from "@/components/MathKeypad";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine,
} from "recharts";
import { LineChart as LineIcon, Play, Loader2, AlertTriangle, Plus, Trash2 } from "lucide-react";

const COLOURS = ["#C9613B", "#3E7A60", "#D8A35A", "#5A6CC9", "#A24F88"];

const EXAMPLES = [
  { label: "Parabola", expression: "x^2 - 4" },
  { label: "Cubic", expression: "x^3 - 3x" },
  { label: "Sine", expression: "sin(x)" },
  { label: "Exp", expression: "exp(x/3)" },
  { label: "Rational", expression: "1/(x-1)" },
];

const Grapher = () => {
  const [expression, setExpression] = useState("");
  const [variable, setVariable] = useState("x");
  const [xMin, setXMin] = useState(-10);
  const [xMax, setXMax] = useState(10);
  const [series, setSeries] = useState([]); // array of { id, latex, points, color, expr }
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const inputRef = useRef(null);

  const plot = async (exprOverride) => {
    const ex = (exprOverride ?? expression).trim();
    if (!ex) { toast.error("Type a function first."); return; }
    setLoading(true); setError(null);
    try {
      const { data } = await http.post("/playground/graph", {
        expression: ex, variable: variable || "x",
        x_min: Number(xMin), x_max: Number(xMax), samples: 200,
      });
      if (!data.ok) {
        setError(data.error || "Could not plot that expression.");
        return;
      }
      setSeries((prev) => [
        ...prev,
        {
          id: `s-${Date.now()}`,
          expr: ex,
          latex: data.latex,
          points: data.points,
          color: COLOURS[prev.length % COLOURS.length],
          clipped: data.asymptotes_clipped,
        },
      ]);
      setExpression(""); // ready for another
      if (data.asymptotes_clipped) toast.info("Steep regions clipped for display.");
    } catch (err) {
      console.error("plot failed:", err);
      setError("Server error while plotting.");
    } finally {
      setLoading(false);
    }
  };

  const remove = (id) => setSeries((s) => s.filter((x) => x.id !== id));
  const clearAll = () => setSeries([]);

  // Build a unified dataset for Recharts: { x, y0, y1, y2... }
  const chartData = (() => {
    if (!series.length) return [];
    const len = series[0].points.length;
    const data = [];
    for (let i = 0; i < len; i++) {
      const row = { x: series[0].points[i].x };
      series.forEach((s, si) => { row[`y${si}`] = s.points[i]?.y ?? null; });
      data.push(row);
    }
    return data;
  })();

  return (
    <div data-testid="grapher-block">
      <div className="card-surface p-6">
        <label htmlFor="grapher-input" className="overline">Function</label>
        <textarea
          id="grapher-input"
          ref={inputRef}
          value={expression}
          onChange={(e) => setExpression(e.target.value)}
          placeholder="e.g.   x^2 - 4   ·   sin(x)   ·   2*exp(-x/3) * cos(x)"
          rows={2}
          data-testid="grapher-input"
          className="mt-2 w-full px-4 py-3 rounded-lg border border-edge bg-surface text-base font-mono focus:outline-none focus:ring-2 focus:ring-terracotta/30"
          onKeyDown={(e) => { if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) plot(); }}
        />
        <MathKeypad targetRef={inputRef} value={expression} onChange={setExpression} />

        <div className="mt-4 grid sm:grid-cols-4 gap-3">
          <div>
            <label className="overline" htmlFor="grapher-xmin">x min</label>
            <input id="grapher-xmin" type="number" value={xMin}
              onChange={(e) => setXMin(e.target.value)}
              data-testid="grapher-xmin"
              className="mt-1 w-full px-3 py-2 rounded-lg border border-edge bg-surface text-sm font-mono" />
          </div>
          <div>
            <label className="overline" htmlFor="grapher-xmax">x max</label>
            <input id="grapher-xmax" type="number" value={xMax}
              onChange={(e) => setXMax(e.target.value)}
              data-testid="grapher-xmax"
              className="mt-1 w-full px-3 py-2 rounded-lg border border-edge bg-surface text-sm font-mono" />
          </div>
          <div>
            <label className="overline" htmlFor="grapher-var">Variable</label>
            <input id="grapher-var" type="text" value={variable}
              onChange={(e) => setVariable(e.target.value.trim() || "x")}
              data-testid="grapher-var"
              className="mt-1 w-full px-3 py-2 rounded-lg border border-edge bg-surface text-sm font-mono" />
          </div>
          <div className="flex items-end">
            <button onClick={() => plot()} disabled={loading}
              className="btn-primary w-full inline-flex items-center justify-center gap-2 disabled:opacity-60"
              data-testid="grapher-plot-btn">
              {loading ? <Loader2 className="animate-spin" size={16} /> : <Plus size={16} />}
              {loading ? "Plotting…" : (series.length ? "Add to plot" : "Plot")}
            </button>
          </div>
        </div>

        <div className="mt-5 flex flex-wrap gap-2">
          <span className="text-xs text-muted2 mr-1 self-center">Try:</span>
          {EXAMPLES.map((ex) => (
            <button key={ex.label} onClick={() => plot(ex.expression)}
              className="px-3 py-1.5 rounded-full border border-edge text-xs text-ink hover:border-terracotta/50 hover:bg-terracotta/5"
              data-testid={`grapher-example-${ex.label.toLowerCase()}`}>
              {ex.label}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="card-surface p-5 mt-4 border border-error/30 bg-error/5" data-testid="grapher-error">
          <div className="flex items-center gap-2 text-error">
            <AlertTriangle size={16} /> <span className="font-medium">Couldn't plot</span>
          </div>
          <p className="text-sm font-mono mt-2 text-ink">{error}</p>
        </div>
      )}

      {series.length > 0 && (
        <div className="card-surface p-6 mt-4" data-testid="grapher-chart-block">
          <div className="flex items-center justify-between flex-wrap gap-2 mb-4">
            <div className="flex items-center gap-2">
              <LineIcon size={16} className="text-terracotta" />
              <span className="overline">Graph</span>
            </div>
            <button onClick={clearAll}
              className="btn-ghost inline-flex items-center gap-1.5 text-xs text-error"
              data-testid="grapher-clear-btn">
              <Trash2 size={12} /> Clear all
            </button>
          </div>
          <div className="h-72 sm:h-96 w-full" data-testid="grapher-chart">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E7E1D5" />
                <XAxis dataKey="x" type="number" domain={[Number(xMin), Number(xMax)]}
                  stroke="#6E6657" tick={{ fontSize: 11 }} />
                <YAxis stroke="#6E6657" tick={{ fontSize: 11 }} domain={["auto", "auto"]} />
                <ReferenceLine x={0} stroke="#6E6657" strokeWidth={1} />
                <ReferenceLine y={0} stroke="#6E6657" strokeWidth={1} />
                <Tooltip contentStyle={{ background: "#FAF7F0", border: "1px solid #E7E1D5", borderRadius: 8 }} />
                {series.map((s, si) => (
                  <Line key={s.id} type="monotone" dataKey={`y${si}`}
                    stroke={s.color} strokeWidth={2} dot={false}
                    connectNulls={false} name={s.expr} />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>

          <ul className="mt-4 space-y-2">
            {series.map((s) => (
              <li key={s.id} className="flex items-center gap-3 text-sm"
                data-testid={`grapher-series-${s.id}`}>
                <span className="w-3 h-3 rounded-sm flex-shrink-0" style={{ background: s.color }} />
                <span className="text-ink overflow-x-auto"><MathText text={`$y = ${s.latex}$`} /></span>
                <button onClick={() => remove(s.id)}
                  className="ml-auto p-1.5 rounded hover:bg-error/10 text-muted2 hover:text-error"
                  aria-label="Remove" data-testid={`grapher-remove-${s.id}`}>
                  <Trash2 size={12} />
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Grapher;
