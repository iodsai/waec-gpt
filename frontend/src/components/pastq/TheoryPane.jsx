import React, { useState } from "react";
import http from "@/lib/api";
import { toast } from "sonner";
import MathText from "@/components/MathText";
import { Send, Wand2 } from "lucide-react";

const TheoryPane = ({ question, onGenerateSimilar, similarLoading }) => {
  const [answer, setAnswer] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);

  const submit = async () => {
    if (!answer.trim()) {
      toast.error("Write your answer before submitting.");
      return;
    }
    setSubmitting(true);
    try {
      const { data } = await http.post("/attempts", { question_id: question.id, selected: answer.trim() });
      setResult(data);
      toast.success("Answer submitted. Compare it with the examiner solution.");
    } catch (e) {
      toast.error("Could not submit answer.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="mt-5" data-testid="theory-question">
      {!result ? (
        <div className="space-y-4">
          <label className="block">
            <span className="text-sm font-semibold text-ink">Your written answer</span>
            <textarea
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              rows={8}
              className="mt-2 w-full rounded-xl border border-edge bg-surface px-4 py-3 text-ink outline-none focus:border-terracotta"
              placeholder="Show your working here before checking the examiner solution."
              data-testid="theory-answer-input"
            />
          </label>
          <button
            onClick={submit}
            disabled={submitting}
            className="btn-primary w-full inline-flex items-center justify-center gap-2 disabled:opacity-60"
            data-testid="submit-theory-answer-btn"
          >
            <Send size={16} /> {submitting ? "Submitting..." : "Submit answer and check solution"}
          </button>
        </div>
      ) : (
        <div className="p-5 rounded-xl bg-sand/60 border border-edge" data-testid="solution-block">
          <div className="rounded-lg border border-edge bg-surface p-4">
            <div className="text-sm font-semibold text-ink">Your submitted answer</div>
            <p className="text-sm text-muted2 whitespace-pre-wrap mt-2">{answer}</p>
          </div>
          <div className="text-sm text-muted2 mt-4">Final answer:</div>
          <div className="font-heading text-lg text-success mt-1">
            <MathText text={result.correct_answer} />
          </div>
          <h3 className="font-heading text-lg font-semibold text-ink mt-4">Worked solution</h3>
          <ol className="mt-3 space-y-2 list-none">
            {result.solution_steps.map((s, i) => (
              <li key={`tstep-${i}`} className="flex gap-3 text-ink" data-testid={`solution-step-${i}`}>
                <span className="font-mono text-xs bg-surface border border-edge px-2 py-0.5 rounded-md h-6 flex-shrink-0">Step {i + 1}</span>
                <span><MathText text={s} /></span>
              </li>
            ))}
          </ol>
          <div className="mt-4 rounded-lg border border-terracotta/30 bg-terracotta/5 p-4">
            <div className="font-heading font-semibold text-ink">Self-marking guide</div>
            <p className="text-sm text-muted2 mt-2">
              Award yourself credit only if your working reaches the same final answer and uses valid set notation, correct region placement and clear reasoning.
            </p>
          </div>
          <button
            onClick={onGenerateSimilar}
            className="btn-secondary mt-5 text-sm inline-flex items-center gap-2"
            data-testid="generate-similar-btn"
            disabled={similarLoading}
          >
            <Wand2 size={14} /> {similarLoading ? "Generating..." : "Generate similar"}
          </button>
        </div>
      )}
    </div>
  );
};

export default TheoryPane;
