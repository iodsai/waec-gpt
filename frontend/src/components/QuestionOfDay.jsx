import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import http from "@/lib/api";
import MathText from "@/components/MathText";
import { toast } from "sonner";
import { Sun, CheckCircle2, XCircle, Loader2 } from "lucide-react";

const LETTERS = ["A", "B", "C", "D"];

const QuestionOfDay = () => {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    http.get("/question-of-the-day")
      .then((r) => setData(r.data))
      .catch((err) => console.error("qotd fetch failed:", err))
      .finally(() => setLoading(false));
  }, []);

  const submit = async () => {
    if (!selected) { toast.error("Pick an answer first."); return; }
    setSubmitting(true);
    try {
      const r = await http.post("/attempts", {
        question_id: data.question.id, selected,
      });
      setResult(r.data);
      if (r.data.correct) toast.success("Nice! +1 to your streak.");
    } catch (err) {
      console.error("qotd submit failed:", err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="card-surface p-6 flex items-center gap-2 text-muted2" data-testid="qotd-loading">
        <Loader2 className="animate-spin" size={18} /> Loading today's challenge…
      </div>
    );
  }
  if (!data?.question) return null;

  const q = data.question;
  const done = !!result || data.already_attempted;

  return (
    <div className="card-surface p-6 border border-marigold/30 bg-marigold/5" data-testid="qotd-card">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center gap-2">
          <Sun size={18} className="text-marigold" />
          <span className="overline">Question of the day</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="tag">{q.subtopic_name}</span>
          <span className="tag">WAEC {q.year}</span>
          {done && (
            <span className={`tag ${data.attempt_correct || result?.correct ? "!text-success" : "!text-error"}`}>
              {data.attempt_correct || result?.correct ? "Completed ✓" : "Attempted"}
            </span>
          )}
        </div>
      </div>
      <div className="font-heading text-xl text-ink mt-3 leading-snug">
        <MathText text={q.question} />
      </div>

      {!done ? (
        <>
          <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-2" data-testid="qotd-options">
            {q.options.map((opt, idx) => {
              const chosen = selected === opt;
              return (
                <button
                  key={`qotd-opt-${idx}`}
                  onClick={() => setSelected(opt)}
                  data-testid={`qotd-option-${LETTERS[idx]}`}
                  className={`text-left px-4 py-2.5 rounded-xl border text-sm transition
                    ${chosen ? "border-terracotta bg-terracotta/10" : "border-edge hover:border-terracotta/40"}`}
                >
                  <span className="font-mono text-xs mr-2">{LETTERS[idx]}</span>
                  <MathText text={opt} />
                </button>
              );
            })}
          </div>
          <button
            onClick={submit}
            disabled={submitting || !selected}
            className="btn-primary mt-4 disabled:opacity-60"
            data-testid="qotd-submit-btn"
          >
            {submitting ? "Submitting…" : "Lock in answer"}
          </button>
        </>
      ) : (
        <div className="mt-4 flex items-center gap-3 text-sm">
          {(result?.correct ?? data.attempt_correct) ? (
            <CheckCircle2 className="text-success" size={18} />
          ) : (
            <XCircle className="text-error" size={18} />
          )}
          <span className="text-ink">
            {result ? (
              <>Answer: <strong><MathText text={result.correct_answer} /></strong></>
            ) : (
              <>You already attempted today's question. Come back tomorrow!</>
            )}
          </span>
          {result && (
            <button
              onClick={() => navigate(`/past-questions?topic=${q.topic}`)}
              className="btn-ghost text-xs ml-auto"
              data-testid="qotd-explore-btn"
            >
              Explore similar →
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default QuestionOfDay;
