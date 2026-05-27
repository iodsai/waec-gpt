import React, { useEffect, useState } from "react";
import http from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { toast } from "sonner";
import MathText from "@/components/MathText";
import { Link } from "react-router-dom";
import { Upload, Save, Image as ImageIcon, Trash2, ShieldAlert, ClipboardCheck } from "lucide-react";
import WaecImport from "@/components/WaecImport";
import BatchImport from "@/components/BatchImport";

const blankQuestion = {
  topic: "algebra", subtopic: "linear-equations", year: 2024,
  difficulty: "medium", question: "", options: ["", "", "", ""],
  answer: "", solution_steps: [""],
};

const Admin = () => {
  const { user } = useAuth();
  const [topics, setTopics] = useState([]);
  const [form, setForm] = useState(blankQuestion);
  const [savingId, setSavingId] = useState(null);
  const [extracting, setExtracting] = useState(false);
  const [list, setList] = useState([]);
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    http.get("/topics").then((r) => setTopics((r.data.topics || []).filter((t) => t.status === "available")));
    if (user?.is_admin) http.get("/admin/questions").then((r) => setList(r.data));
  }, [user]);

  if (!user?.is_admin) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-20 text-center" data-testid="admin-forbidden">
        <ShieldAlert className="mx-auto text-error" size={36} />
        <h1 className="font-heading text-3xl font-bold text-ink mt-3">Admin only</h1>
        <p className="text-muted2 mt-2">Use admin credentials to access this page.</p>
        <p className="text-xs text-muted2 mt-1 font-mono">admin@waec.com / Admin@123</p>
      </div>
    );
  }

  const subtopicsFor = (tid) => topics.find((t) => t.id === tid)?.subtopics || [];

  const updateOption = (i, val) => {
    setForm((f) => { const o = [...f.options]; o[i] = val; return { ...f, options: o }; });
  };

  const updateStep = (i, val) => {
    setForm((f) => { const s = [...f.solution_steps]; s[i] = val; return { ...f, solution_steps: s }; });
  };

  const handleExtract = async (file) => {
    if (!file) return;
    setExtracting(true);
    try {
      const fd = new FormData();
      fd.append("image", file);
      const { data } = await http.post("/admin/questions/extract", fd, { headers: { "Content-Type": "multipart/form-data" } });
      const sub = data.subtopic_guess || "linear-equations";
      // map subtopic to topic
      let parentTopic = "algebra";
      for (const t of topics) {
        if ((t.subtopics || []).some((s) => s.id === sub)) { parentTopic = t.id; break; }
      }
      setForm({
        topic: parentTopic,
        subtopic: sub,
        year: form.year || 2024,
        difficulty: data.difficulty_guess || "medium",
        question: data.question || "",
        options: (data.options && data.options.length === 4) ? data.options : ["", "", "", ""],
        answer: data.answer || "",
        solution_steps: data.solution_steps?.length ? data.solution_steps : [""],
      });
      toast.success("Extracted! Review and save.");
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Extraction failed");
    } finally {
      setExtracting(false);
    }
  };

  const save = async () => {
    if (!form.question.trim() || !form.answer.trim()) {
      toast.error("Question and answer are required");
      return;
    }
    setSavingId("new");
    try {
      const { data } = await http.post("/admin/questions", {
        ...form,
        year: Number(form.year),
        options: form.options.filter((o) => o.trim()),
        solution_steps: form.solution_steps.filter((s) => s.trim()),
      });
      toast.success("Question added (" + data.id.slice(0, 8) + "…)");
      setForm(blankQuestion);
      const r = await http.get("/admin/questions");
      setList(r.data);
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Could not save");
    } finally {
      setSavingId(null);
    }
  };

  const remove = async (id) => {
    if (!window.confirm("Delete this question?")) return;
    try {
      await http.delete(`/admin/questions/${id}`);
      setList((l) => l.filter((x) => x.id !== id));
      toast.success("Deleted");
    } catch (e) {
      toast.error("Could not delete");
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid="admin-page">
      <span className="overline">Admin</span>
      <h1 className="font-heading text-4xl font-bold text-ink mt-2">Add WAEC question</h1>
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mt-2">
        <p className="text-muted2">Import real past papers from waeconline.org.ng, paste / type a question manually, or upload an image and let AI extract it.</p>
        <Link to="/admin/lesson-audit" className="btn-ghost inline-flex items-center gap-2 text-sm self-start sm:self-auto">
          <ClipboardCheck size={16} /> Lesson audit
        </Link>
      </div>

      <WaecImport />
      <BatchImport />

      <div className="grid lg:grid-cols-3 gap-6 mt-8">
        {/* Image extract */}
        <div className="card-surface p-6 lg:col-span-1" data-testid="admin-extract-block">
          <ImageIcon className="text-terracotta" />
          <h3 className="font-heading text-lg font-semibold text-ink mt-3">AI image extraction</h3>
          <p className="text-sm text-muted2 mt-1">Upload a screenshot or photo of a WAEC question. Gemini Vision parses it into the form.</p>
          <label className="mt-4 block border-2 border-dashed border-edge rounded-xl p-6 text-center cursor-pointer hover:border-terracotta/50">
            <Upload className="mx-auto text-muted2" />
            <div className="text-sm text-ink mt-2">{extracting ? "Extracting…" : "Click to upload image"}</div>
            <input
              type="file" accept="image/*" hidden
              data-testid="admin-image-input"
              onChange={(e) => handleExtract(e.target.files?.[0])} disabled={extracting}
            />
          </label>
        </div>

        {/* Form */}
        <div className="card-surface p-6 lg:col-span-2" data-testid="admin-form">
          <div className="grid sm:grid-cols-3 gap-4">
            <div>
              <label className="text-sm font-medium">Topic</label>
              <select value={form.topic} onChange={(e) => setForm({ ...form, topic: e.target.value, subtopic: subtopicsFor(e.target.value)[0]?.id || "" })}
                data-testid="admin-topic-select"
                className="mt-1 w-full px-3 py-2 rounded-lg border border-edge bg-surface">
                {topics.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
              </select>
            </div>
            <div>
              <label className="text-sm font-medium">Subtopic</label>
              <select value={form.subtopic} onChange={(e) => setForm({ ...form, subtopic: e.target.value })}
                data-testid="admin-subtopic-select"
                className="mt-1 w-full px-3 py-2 rounded-lg border border-edge bg-surface">
                {subtopicsFor(form.topic).map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
              </select>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="text-sm font-medium">Year</label>
                <input type="number" value={form.year} onChange={(e) => setForm({ ...form, year: e.target.value })}
                  data-testid="admin-year-input"
                  className="mt-1 w-full px-3 py-2 rounded-lg border border-edge bg-surface" />
              </div>
              <div>
                <label className="text-sm font-medium">Difficulty</label>
                <select value={form.difficulty} onChange={(e) => setForm({ ...form, difficulty: e.target.value })}
                  data-testid="admin-difficulty-select"
                  className="mt-1 w-full px-3 py-2 rounded-lg border border-edge bg-surface">
                  <option>easy</option><option>medium</option><option>hard</option>
                </select>
              </div>
            </div>
          </div>

          <div className="mt-4">
            <label className="text-sm font-medium">Question (LaTeX in $...$)</label>
            <textarea rows={3} value={form.question} onChange={(e) => setForm({ ...form, question: e.target.value })}
              data-testid="admin-question-input"
              className="mt-1 w-full px-3 py-2 rounded-lg border border-edge bg-surface font-mono text-sm" />
            {form.question && <div className="mt-2 p-2 bg-sand/60 rounded text-sm"><MathText text={form.question} /></div>}
          </div>

          <div className="mt-4 grid sm:grid-cols-2 gap-3">
            {form.options.map((opt, i) => (
              <div key={i}>
                <label className="text-sm font-medium">Option {["A", "B", "C", "D"][i]}</label>
                <input value={opt} onChange={(e) => updateOption(i, e.target.value)}
                  data-testid={`admin-option-${i}`}
                  className="mt-1 w-full px-3 py-2 rounded-lg border border-edge bg-surface" />
              </div>
            ))}
          </div>

          <div className="mt-4">
            <label className="text-sm font-medium">Correct answer (exact match to one option)</label>
            <input value={form.answer} onChange={(e) => setForm({ ...form, answer: e.target.value })}
              data-testid="admin-answer-input"
              className="mt-1 w-full px-3 py-2 rounded-lg border border-edge bg-surface" />
          </div>

          <div className="mt-4">
            <label className="text-sm font-medium">Solution steps (one per line)</label>
            <textarea rows={4} value={form.solution_steps.join("\n")} onChange={(e) => setForm({ ...form, solution_steps: e.target.value.split("\n") })}
              data-testid="admin-steps-input"
              className="mt-1 w-full px-3 py-2 rounded-lg border border-edge bg-surface font-mono text-sm" />
          </div>

          <button onClick={save} disabled={savingId === "new"} className="btn-primary mt-5 inline-flex items-center gap-2" data-testid="admin-save-btn">
            <Save size={16} /> {savingId ? "Saving…" : "Save question"}
          </button>
        </div>
      </div>

      <div className="mt-12">
        <div className="flex items-center justify-between">
          <h2 className="font-heading text-2xl font-semibold text-ink">All questions ({list.length})</h2>
          <button onClick={() => setShowAll((s) => !s)} className="text-sm text-terracotta hover:underline">{showAll ? "Show admin-added only" : "Show all"}</button>
        </div>
        <div className="card-surface divide-y divide-edge mt-4">
          {list
            .filter((q) => showAll || q.source === "admin")
            .slice(0, 50).map((q) => (
            <div key={q.id} className="px-5 py-3 flex items-center gap-3" data-testid={`admin-q-row-${q.id}`}>
              <div className="flex-1 min-w-0">
                <div className="text-sm text-ink truncate"><MathText text={q.question} /></div>
                <div className="text-xs text-muted2 mt-0.5">{q.topic} · {q.subtopic} · {q.year} · {q.difficulty} · {q.source || "seed"}</div>
              </div>
              <button onClick={() => remove(q.id)} className="p-2 rounded-lg border border-edge text-error/80 hover:bg-error/10" data-testid={`admin-delete-${q.id}`}>
                <Trash2 size={14} />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Admin;
