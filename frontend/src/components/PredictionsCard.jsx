import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import http from "@/lib/api";
import { TrendingUp, Zap, Share2, Loader2 } from "lucide-react";
import { toast } from "sonner";

const PredictionsCard = () => {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    http.get("/predictions")
      .then((r) => setData(r.data))
      .catch((err) => console.error("predictions fetch failed:", err))
      .finally(() => setLoading(false));
  }, []);

  const drill = async (topic) => {
    try {
      const { data: exam } = await http.post("/exams/start", { mode: "quick", topic });
      navigate(`/exams/${exam.exam_id}/run`);
    } catch (err) {
      console.error("drill start failed:", err);
    }
  };

  const shareWhatsApp = () => {
    if (!data?.items?.length) return;
    const lines = data.items.map(
      (it, i) => `${i + 1}. ${it.subtopic_name} (${it.frequency_pct}%)`
    );
    const msg = encodeURIComponent(
      `🎯 *Top 5 likely topics for WAEC Further Maths* (based on ${data.papers_analysed} past papers)\n\n${lines.join("\n")}\n\nPrep smart with WAEC Elective Math AI 👉 ${window.location.origin}`
    );
    window.open(`https://wa.me/?text=${msg}`, "_blank");
    toast.success("Opening WhatsApp…");
  };

  if (loading) {
    return (
      <div className="card-surface p-6 flex items-center gap-2 text-muted2" data-testid="predictions-loading">
        <Loader2 className="animate-spin" size={18} /> Analysing past papers…
      </div>
    );
  }
  if (!data?.items?.length) return null;

  return (
    <div className="card-surface p-6" data-testid="predictions-card">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center gap-2">
          <TrendingUp size={18} className="text-terracotta" />
          <span className="overline">Likely on the next WAEC</span>
        </div>
        <button
          onClick={shareWhatsApp}
          className="btn-ghost inline-flex items-center gap-1.5 text-xs"
          data-testid="predictions-share-btn"
        >
          <Share2 size={12} /> Share on WhatsApp
        </button>
      </div>
      <p className="text-sm text-muted2 mt-2">
        Based on subtopic frequency across {data.papers_analysed} scraped WAEC papers ({data.sample_size} questions).
      </p>
      <ol className="mt-4 space-y-2.5" data-testid="predictions-list">
        {data.items.map((it, i) => (
          <li
            key={it.subtopic}
            className="flex items-center gap-3"
            data-testid={`prediction-${i + 1}`}
          >
            <span className="font-heading text-xl text-terracotta w-6 text-right">{i + 1}.</span>
            <div className="flex-1 min-w-0">
              <div className="text-ink font-medium truncate">{it.subtopic_name}</div>
              <div className="text-xs text-muted2">{it.topic_name} · {it.appearances} appearances</div>
            </div>
            <div className="hidden sm:block flex-shrink-0 w-24 h-2 rounded-full bg-edge/40 overflow-hidden">
              <div
                className="h-full bg-terracotta"
                style={{ width: `${Math.min(100, it.frequency_pct * 4)}%` }}
              />
            </div>
            <span className="text-sm font-mono text-terracotta w-12 text-right">{it.frequency_pct}%</span>
            <button
              onClick={() => drill(it.topic)}
              className="btn-ghost inline-flex items-center gap-1 text-xs"
              data-testid={`prediction-drill-${i + 1}`}
              title="Drill 10 questions on this topic"
            >
              <Zap size={12} /> Drill
            </button>
          </li>
        ))}
      </ol>
    </div>
  );
};

export default PredictionsCard;
