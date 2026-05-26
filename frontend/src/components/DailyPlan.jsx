import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import http from "@/lib/api";
import { Target, Zap, Compass, Loader2, TrendingUp } from "lucide-react";

const KIND_STYLES = {
  weak:   { icon: Target,    accent: "text-error",      ring: "border-error/20",      tag: "!bg-error/10 !text-error" },
  medium: { icon: TrendingUp, accent: "text-terracotta", ring: "border-terracotta/20", tag: "!bg-terracotta/10 !text-terracotta" },
  new:    { icon: Compass,   accent: "text-moss",       ring: "border-moss/20",       tag: "!bg-moss/10 !text-moss" },
};

const PlanCard = ({ card, onDrill, drillingKind }) => {
  const style = KIND_STYLES[card.kind] || KIND_STYLES.new;
  const Icon = style.icon;
  const isDrilling = drillingKind === card.kind;
  return (
    <div className={`card-surface p-5 border ${style.ring}`} data-testid={`plan-card-${card.kind}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Icon size={16} className={style.accent} />
          <span className="overline">{card.label}</span>
        </div>
        {card.accuracy !== null && (
          <span className={`tag ${style.tag}`} data-testid={`plan-acc-${card.kind}`}>
            {card.accuracy}%
          </span>
        )}
      </div>
      <div className="font-heading text-xl font-semibold text-ink mt-3 leading-snug" data-testid={`plan-sub-${card.kind}`}>
        {card.subtopic_name}
      </div>
      <div className="text-xs text-muted2 mt-0.5">{card.topic_name}</div>
      <p className="text-sm text-ink/80 mt-3 leading-relaxed">{card.message}</p>
      <button
        onClick={() => onDrill(card)}
        disabled={isDrilling}
        className="btn-primary mt-4 w-full inline-flex items-center justify-center gap-2 disabled:opacity-60"
        data-testid={`plan-drill-${card.kind}`}
      >
        {isDrilling ? <Loader2 size={14} className="animate-spin" /> : <Zap size={14} />}
        Drill 10
      </button>
    </div>
  );
};

const DailyPlan = () => {
  const navigate = useNavigate();
  const [cards, setCards] = useState([]);
  const [message, setMessage] = useState(null);
  const [loading, setLoading] = useState(true);
  const [drillingKind, setDrillingKind] = useState(null);

  useEffect(() => {
    http.get("/progress/daily-plan")
      .then((r) => { setCards(r.data.cards || []); setMessage(r.data.message); })
      .catch((err) => console.error("daily-plan fetch failed:", err))
      .finally(() => setLoading(false));
  }, []);

  const drill = async (card) => {
    setDrillingKind(card.kind);
    try {
      const { data: exam } = await http.post("/exams/start", { mode: "quick", topic: card.topic });
      navigate(`/exams/${exam.exam_id}/run`);
    } catch (err) {
      console.error("Drill start failed:", err);
      setDrillingKind(null);
    }
  };

  if (loading) {
    return (
      <div className="card-surface p-6 flex items-center gap-3 text-muted2" data-testid="daily-plan-loading">
        <Loader2 className="animate-spin" size={18} /> Building today's plan…
      </div>
    );
  }

  if (!cards.length) {
    return (
      <div className="card-surface p-6" data-testid="daily-plan-empty">
        <div className="flex items-center gap-2 text-muted2">
          <Compass size={18} /> {message || "Try a few questions to unlock your daily plan."}
        </div>
      </div>
    );
  }

  return (
    <div data-testid="daily-plan">
      <div className="flex items-end justify-between mb-4">
        <div>
          <h2 className="font-heading text-2xl font-semibold text-ink">Today's plan</h2>
          <p className="text-muted2 text-sm mt-1">
            A three-step drill tailored to where you are right now.
          </p>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {cards.map((c) => (
          <PlanCard key={c.kind} card={c} onDrill={drill} drillingKind={drillingKind} />
        ))}
      </div>
    </div>
  );
};

export default DailyPlan;
