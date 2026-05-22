import React, { useEffect, useState } from "react";
import http from "@/lib/api";
import { toast } from "sonner";
import MathText from "@/components/MathText";
import { Download, CheckSquare, Square, Loader2, ExternalLink, Save } from "lucide-react";

const SUBTOPICS_FLAT = [
  "measures-of-location", "measures-of-spread", "correlation", "probability", "perms-combinations",
  "limits", "differentiation", "applications-differentiation", "integration", "applications-integration",
  "vector-algebra-2d", "vectors-3d", "magnitude-direction", "scalar-product", "vectors-applications",
];

const WaecImport = () => {
  const [papers, setPapers] = useState([]);
  const [selected, setSelected] = useState("");
  const [extracting, setExtracting] = useState(false);
  const [preview, setPreview] = useState(null); // { paper_url, year, questions: [{question, options, answer, ...}] }
  const [saving, setSaving] = useState(false);
  const [included, setIncluded] = useState({}); // idx -> bool

  useEffect(() => {
    http.get("/admin/import/papers").then((r) => {
      setPapers(r.data.papers);
      if (r.data.papers?.length) setSelected(r.data.papers[0].url);
    }).catch(() => toast.error("Could not load paper list"));
  }, []);

  const extract = async () => {
    const paper = papers.find((p) => p.url === selected);
    if (!paper) return;
    setExtracting(true);
    setPreview(null);
    try {
      const { data } = await http.post("/admin/import/extract", {
        paper_url: paper.url, year: paper.year, max_questions: 13,
      }, { timeout: 600000 }); // up to 10 min
      setPreview(data);
      // include all by default
      const inc = {};
      (data.questions || []).forEach((_, i) => { inc[i] = true; });
      setIncluded(inc);
      toast.success(`Extracted ${data.questions?.length || 0} questions`);
    } catch (e) {
      toast.error(e?.response?.data?.detail || e?.message || "Extraction failed");
    } finally {
      setExtracting(false);
    }
  };

  const updateField = (i, key, val) => {
    setPreview((p) => {
      const next = { ...p, questions: [...p.questions] };
      next.questions[i] = { ...next.questions[i], [key]: val };
      return next;
    });
  };

  const saveAll = async () => {
    if (!preview) return;
    const chosen = preview.questions.filter((_, i) => included[i]);
    if (!chosen.length) { toast.error("Pick at least one question to save"); return; }
    // normalise keys: subtopic falls back to subtopic_guess, etc.
    const payload = chosen.map((q) => ({
      subtopic: q.subtopic || q.subtopic_guess,
      difficulty: q.difficulty || q.difficulty_guess,
      question_type: q.question_type || (q.options?.length ? "objective" : "theory"),
      question: q.question,
      options: q.options || [],
      answer: q.answer,
      solution_steps: q.solution_steps,
      source_url: q.source_url,
    }));
    setSaving(true);
    try {
      const { data } = await http.post("/admin/import/save", {
        paper_url: preview.paper_url, year: preview.year, questions: payload,
      });
      toast.success(`Saved ${data.saved} questions`);
      setPreview(null);
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Save failed");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="card-surface p-6 mt-8" data-testid="waec-import-block">
      <div className="flex items-center gap-2">
        <Download className="text-terracotta" size={20} />
        <h2 className="font-heading text-2xl font-semibold text-ink">Import WAEC past paper</h2>
      </div>
      <p className="text-sm text-muted2 mt-1">
        Pick a paper from waeconline.org.ng — the system scrapes each question, uses Gemini Vision to read inline math
        images, auto-generates 4-option MCQ format, and lets you review before saving.
      </p>

      <div className="mt-5 flex flex-col sm:flex-row gap-3">
        <select
          value={selected} onChange={(e) => setSelected(e.target.value)}
          data-testid="import-paper-select"
          className="flex-1 px-3 py-2 rounded-lg border border-edge bg-surface text-sm"
        >
          {papers.map((p) => (
            <option key={p.url} value={p.url}>{p.label}</option>
          ))}
        </select>
        <button onClick={extract} disabled={extracting} data-testid="import-extract-btn"
          className="btn-primary inline-flex items-center gap-2 disabled:opacity-60">
          {extracting ? <><Loader2 className="animate-spin" size={16} /> Extracting…</> : <><Download size={16} /> Extract</>}
        </button>
      </div>
      {extracting && (
        <p className="text-xs text-muted2 mt-3">⏳ This takes ~30-90 seconds. The scraper fetches each question, downloads inline math images, and asks Gemini Vision to convert it to MCQ format.</p>
      )}

      {preview && (
        <div className="mt-8" data-testid="import-preview">
          <div className="flex items-center justify-between flex-wrap gap-3">
            <div>
              <h3 className="font-heading text-xl font-semibold text-ink">Preview: {preview.questions.length} questions</h3>
              <p className="text-xs text-muted2">Year {preview.year} · uncheck any you don't want to save · edit answer/subtopic inline.</p>
            </div>
            <button onClick={saveAll} disabled={saving} className="btn-secondary inline-flex items-center gap-2" data-testid="import-save-btn">
              <Save size={16} /> {saving ? "Saving…" : `Save ${Object.values(included).filter(Boolean).length} selected`}
            </button>
          </div>

          <div className="space-y-3 mt-5">
            {preview.questions.map((q, i) => (
              <div key={i} className={`border rounded-xl p-5 transition ${included[i] ? "border-edge bg-surface" : "border-edge/40 bg-sand/30 opacity-60"}`}
                   data-testid={`import-q-${i}`}>
                <div className="flex items-start gap-3">
                  <button onClick={() => setIncluded((m) => ({ ...m, [i]: !m[i] }))} className="mt-1 text-terracotta" data-testid={`import-toggle-${i}`}>
                    {included[i] ? <CheckSquare size={20} /> : <Square size={20} />}
                  </button>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap text-xs text-muted2">
                      <span className="tag">Q{i + 1}</span>
                      <span className={`tag ${q.question_type === "theory" ? "!bg-moss/10 !text-moss" : "!bg-terracotta/10 !text-terracotta"}`}>
                        {q.question_type === "theory" ? "Theory" : "Objective"}
                      </span>
                      {q.source_url && (
                        <a href={q.source_url} target="_blank" rel="noreferrer" className="text-terracotta hover:underline inline-flex items-center gap-1">
                          source <ExternalLink size={11} />
                        </a>
                      )}
                    </div>
                    <div className="mt-2 text-ink font-medium leading-relaxed">
                      <MathText text={q.question} />
                    </div>
                    {q.question_type !== "theory" && (q.options || []).length > 0 && (
                      <div className="grid sm:grid-cols-2 gap-2 mt-3">
                        {(q.options || []).map((opt, j) => (
                          <div key={j} className={`flex items-center gap-2 px-3 py-2 rounded-lg border ${opt === q.answer ? "border-success bg-success/10" : "border-edge"}`}>
                            <span className="font-mono text-xs text-muted2">{["A","B","C","D"][j]}</span>
                            <span className="text-sm text-ink"><MathText text={opt} /></span>
                          </div>
                        ))}
                      </div>
                    )}
                    <div className="grid sm:grid-cols-3 gap-3 mt-4 text-sm">
                      <div>
                        <label className="text-xs font-medium text-muted2">Subtopic</label>
                        <select value={q.subtopic || q.subtopic_guess || "linear-equations"}
                          onChange={(e) => updateField(i, "subtopic", e.target.value)}
                          data-testid={`import-subtopic-${i}`}
                          className="mt-0.5 w-full px-2 py-1.5 rounded-md border border-edge bg-surface text-sm">
                          {SUBTOPICS_FLAT.map((s) => <option key={s} value={s}>{s}</option>)}
                        </select>
                      </div>
                      <div>
                        <label className="text-xs font-medium text-muted2">Difficulty</label>
                        <select value={q.difficulty || q.difficulty_guess || "medium"}
                          onChange={(e) => updateField(i, "difficulty", e.target.value)}
                          data-testid={`import-difficulty-${i}`}
                          className="mt-0.5 w-full px-2 py-1.5 rounded-md border border-edge bg-surface text-sm">
                          <option>easy</option><option>medium</option><option>hard</option>
                        </select>
                      </div>
                      <div>
                        <label className="text-xs font-medium text-muted2">Answer (must match an option)</label>
                        <input value={q.answer || ""} onChange={(e) => updateField(i, "answer", e.target.value)}
                          data-testid={`import-answer-${i}`}
                          className="mt-0.5 w-full px-2 py-1.5 rounded-md border border-edge bg-surface text-sm" />
                      </div>
                    </div>
                    <details className="mt-3 text-sm text-muted2">
                      <summary className="cursor-pointer text-ink/80">View AI worked solution ({q.solution_steps?.length || 0} steps)</summary>
                      <ol className="mt-2 space-y-1">
                        {(q.solution_steps || []).map((s, si) => (
                          <li key={si} className="flex gap-2">
                            <span className="font-mono text-xs">{si + 1}.</span>
                            <span><MathText text={s} /></span>
                          </li>
                        ))}
                      </ol>
                    </details>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default WaecImport;
