import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import http from "@/lib/api";
import { Repeat2, Loader2, Sparkles, CheckCircle2 } from "lucide-react";

const ReviewCard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);

  useEffect(() => {
    http.get("/srs/stats")
      .then((r) => setStats(r.data))
      .catch((err) => console.error("srs stats failed:", err))
      .finally(() => setLoading(false));
  }, []);

  const startReview = async () => {
    if (!stats?.due_now) return;
    setStarting(true);
    try {
      const { data } = await http.get("/srs/due", { params: { limit: 20 } });
      if (!data.items.length) {
        setStarting(false);
        return;
      }
      const ids = data.items.map((x) => x.question_id);
      const exam = await http.post("/exams/start", {
        mode: "quick", question_ids: ids,
      });
      navigate(`/exams/${exam.data.exam_id}/run`);
    } catch (err) {
      console.error("review start failed:", err);
      setStarting(false);
    }
  };

  if (loading) {
    return (
      <div className="card-surface p-5 flex items-center gap-2 text-muted2" data-testid="srs-loading">
        <Loader2 className="animate-spin" size={16} /> Checking your review deck…
      </div>
    );
  }

  if (!stats || (stats.total === 0 && stats.due_now === 0)) {
    return (
      <div className="card-surface p-5 border border-moss/20" data-testid="srs-empty">
        <div className="flex items-center gap-2">
          <Sparkles size={16} className="text-moss" />
          <span className="overline">Spaced repetition</span>
        </div>
        <p className="text-sm text-ink mt-2">
          Practise some questions — anything you get wrong is auto-saved for review at
          smart intervals (1d, 3d, 7d, 14d, 30d).
        </p>
      </div>
    );
  }

  const ready = stats.due_now > 0;
  return (
    <div
      className={`card-surface p-5 border ${ready ? "border-terracotta/30 bg-terracotta/5" : "border-edge"}`}
      data-testid="srs-card"
    >
      <div className="flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center gap-2">
          <Repeat2 size={16} className="text-terracotta" />
          <span className="overline">Spaced repetition</span>
        </div>
        <span className="text-xs text-muted2 font-mono">{stats.total} cards in deck</span>
      </div>

      {ready ? (
        <>
          <div className="font-heading text-2xl font-semibold text-ink mt-3" data-testid="srs-due-count">
            {stats.due_now} {stats.due_now === 1 ? "card" : "cards"} due now
          </div>
          <p className="text-sm text-muted2 mt-1">
            Re-attempt these — getting them right today locks the concept in for longer.
          </p>
          <button
            onClick={startReview}
            disabled={starting}
            className="btn-primary mt-4 inline-flex items-center gap-2 disabled:opacity-60"
            data-testid="srs-start-btn"
          >
            {starting ? <Loader2 size={14} className="animate-spin" /> : <Repeat2 size={14} />}
            Start review
          </button>
        </>
      ) : (
        <>
          <div className="font-heading text-xl text-ink mt-3 inline-flex items-center gap-2">
            <CheckCircle2 size={18} className="text-success" /> All caught up
          </div>
          <p className="text-sm text-muted2 mt-1">
            No cards due right now. Come back later — new questions you get wrong join the deck automatically.
          </p>
        </>
      )}
    </div>
  );
};

export default ReviewCard;
