import React, { useEffect, useState } from "react";
import { useNavigate, useSearchParams, Link } from "react-router-dom";
import http from "@/lib/api";
import { toast } from "sonner";
import { Timer, Trophy, Sparkles } from "lucide-react";

const Exams = () => {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const initialTopic = params.get("topic") || "mixed";
  const [mode, setMode] = useState("quick");
  const [topic, setTopic] = useState(initialTopic);
  const [topics, setTopics] = useState([]);
  const [starting, setStarting] = useState(false);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    Promise.all([http.get("/topics"), http.get("/exams")]).then(([t, h]) => {
      setTopics((t.data.topics || []).filter((x) => x.status === "available"));
      setHistory(h.data || []);
    });
  }, []);

  const start = async () => {
    setStarting(true);
    try {
      const { data } = await http.post("/exams/start", {
        mode, topic: topic === "mixed" ? null : topic,
      });
      sessionStorage.setItem(`exam-${data.exam_id}`, JSON.stringify(data));
      navigate(`/exams/${data.exam_id}/run`);
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Could not start exam");
    } finally {
      setStarting(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid="exams-page">
      <span className="overline">Exam mode</span>
      <h1 className="font-heading text-4xl font-bold text-ink mt-2">Test yourself under timed conditions</h1>
      <p className="text-muted2 mt-2">Pick a mode and topic. The clock starts the moment you begin.</p>

      <div className="grid lg:grid-cols-2 gap-5 mt-8">
        <button onClick={() => setMode("quick")} data-testid="mode-quick"
          className={`text-left card-surface p-7 transition ${mode === "quick" ? "!border-terracotta ring-2 ring-terracotta/20" : ""}`}>
          <div className="flex items-center justify-between">
            <Timer className="text-terracotta" size={26} />
            <span className="tag">5 min · 10 Q</span>
          </div>
          <h3 className="font-heading text-2xl font-semibold text-ink mt-4">Quick Drill</h3>
          <p className="text-muted2 text-sm mt-2">10 questions, 5 minutes. Perfect for daily warm-up.</p>
        </button>
        <button onClick={() => setMode("mock")} data-testid="mode-mock"
          className={`text-left card-surface p-7 transition ${mode === "mock" ? "!border-terracotta ring-2 ring-terracotta/20" : ""}`}>
          <div className="flex items-center justify-between">
            <Trophy className="text-moss" size={26} />
            <span className="tag">60 min · 40 Q</span>
          </div>
          <h3 className="font-heading text-2xl font-semibold text-ink mt-4">Full Mock Exam</h3>
          <p className="text-muted2 text-sm mt-2">40 questions, 60 minutes. WAEC-style timed mock with full breakdown.</p>
        </button>
      </div>

      <div className="card-surface p-6 mt-6 flex flex-col sm:flex-row gap-4 sm:items-end justify-between">
        <div>
          <label className="text-sm font-medium text-ink">Topic scope</label>
          <select
            value={topic} onChange={(e) => setTopic(e.target.value)} data-testid="exam-topic-select"
            className="mt-1 block w-full sm:w-72 px-4 py-3 rounded-xl border border-edge bg-surface focus:outline-none focus:ring-2 focus:ring-terracotta/30"
          >
            <option value="mixed">All topics (mixed)</option>
            {topics.map((t) => <option key={t.id} value={t.id}>{t.name} ({t.question_count})</option>)}
          </select>
        </div>
        <button onClick={start} disabled={starting} className="btn-primary inline-flex items-center gap-2" data-testid="start-exam-btn">
          <Sparkles size={18} /> {starting ? "Starting…" : "Start exam"}
        </button>
      </div>

      {history.length > 0 && (
        <div className="mt-12">
          <h2 className="font-heading text-2xl font-semibold text-ink">Your past exams</h2>
          <div className="mt-4 card-surface divide-y divide-edge">
            {history.map((h) => (
              <Link key={h.id} to={`/exams/${h.id}/report`} className="flex items-center justify-between gap-4 px-5 py-4 hover:bg-sand/40" data-testid={`exam-history-${h.id}`}>
                <div>
                  <div className="font-medium text-ink">{h.mode === "mock" ? "Full Mock" : "Quick Drill"} · {h.topic || "mixed"}</div>
                  <div className="text-xs text-muted2">{new Date(h.submitted_at).toLocaleString()} · {h.total_questions} Q · {Math.round(h.time_taken_seconds/60)} min</div>
                </div>
                <span className={`tag ${h.score >= 70 ? "!bg-success/10 !text-success" : h.score >= 40 ? "!bg-warning/15 !text-warning" : "!bg-error/10 !text-error"}`}>
                  {h.score}%
                </span>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Exams;
