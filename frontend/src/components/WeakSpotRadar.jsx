import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import http from "@/lib/api";
import { Target, Zap, Compass, Loader2 } from "lucide-react";

const WeakSpotRadar = () => {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [drilling, setDrilling] = useState(false);

  useEffect(() => {
    http.get("/progress/weak-spot")
      .then((r) => setData(r.data))
      .catch((err) => console.error("weak-spot fetch failed:", err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="card-surface p-6 flex items-center gap-3 text-muted2" data-testid="weak-spot-loading">
        <Loader2 className="animate-spin" size={18} /> Analysing your practice…
      </div>
    );
  }

  if (!data || data.kind === "none") {
    return (
      <div className="card-surface p-6" data-testid="weak-spot-empty">
        <div className="flex items-center gap-2 text-muted2">
          <Compass size={18} /> {data?.message || "Try a few questions to unlock your weak-spot radar."}
        </div>
      </div>
    );
  }

  const isExplore = data.kind === "explore";
  const Icon = isExplore ? Compass : Target;
  const accent = isExplore ? "text-moss" : "text-terracotta";

  const drill10 = async () => {
    setDrilling(true);
    try {
      // Use quick exam mode filtered by the weak topic
      const { data: exam } = await http.post("/exams/start", {
        mode: "quick",
        topic: data.topic,
      });
      navigate(`/exams/${exam.exam_id}/run`);
    } catch (err) {
      setDrilling(false);
      console.error("Drill start failed:", err);
    }
  };

  return (
    <div className="card-surface p-6" data-testid="weak-spot-radar">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Icon size={18} className={accent} />
          <span className="overline">{isExplore ? "Explore next" : "Weak-spot radar"}</span>
        </div>
        {!isExplore && (
          <span className="tag !bg-error/10 !text-error" data-testid="weak-spot-accuracy">
            {data.accuracy}% on {data.total_attempts}
          </span>
        )}
      </div>
      <div className="font-heading text-2xl font-semibold text-ink mt-3" data-testid="weak-spot-subtopic">
        {data.subtopic_name}
      </div>
      <div className="text-xs text-muted2 mt-1">{data.topic_name}</div>
      <p className="text-sm text-ink/80 mt-3">{data.message}</p>
      <button
        onClick={drill10}
        disabled={drilling}
        className="btn-primary mt-5 inline-flex items-center gap-2 disabled:opacity-60"
        data-testid="weak-spot-drill-btn"
      >
        {drilling ? <Loader2 size={16} className="animate-spin" /> : <Zap size={16} />}
        Drill 10 questions
      </button>
    </div>
  );
};

export default WeakSpotRadar;
