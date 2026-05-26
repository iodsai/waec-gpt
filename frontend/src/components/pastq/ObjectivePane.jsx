import React, { useState } from "react";
import http from "@/lib/api";
import { toast } from "sonner";
import MathText from "@/components/MathText";
import { CheckCircle2, XCircle, Wand2 } from "lucide-react";

const LETTERS = ["A", "B", "C", "D", "E"];

const ObjectivePane = ({ question, onTryAgain, onGenerateSimilar, similarLoading }) => {
  const [selected, setSelected] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);

  const submit = async () => {
    if (!selected) { toast.error("Please select an option."); return; }
    setSubmitting(true);
    try {
      const { data } = await http.post("/attempts", { question_id: question.id, selected });
      setResult(data);
      if (data.correct) toast.success("Correct! Well done.");
      else toast.error("Not quite — see the worked solution below.");
    } catch (e) {
      toast.error("Could not submit attempt.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <>
      <div className="mt-5 space-y-2" data-testid="answer-options">
        {question.options.map((opt, idx) => {
          const letter = LETTERS[idx];
          const chosen = selected === opt;
          const showCorrect = result && opt === result.correct_answer;
          const showWrong = result && chosen && !result.correct;
          return (
            <button
              key={idx}
              disabled={!!result}
              onClick={() => setSelected(opt)}
              data-testid={`option-${letter}`}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl border text-left transition
                ${chosen ? "border-terracotta bg-terracotta/5" : "border-edge hover:border-terracotta/40"}
                ${showCorrect ? "!border-success !bg-success/10" : ""}
                ${showWrong ? "!border-error !bg-error/10" : ""}
              `}
            >
              <span className="font-mono text-sm w-6 h-6 grid place-items-center rounded-md bg-sand text-ink">{letter}</span>
              <span className="text-ink"><MathText text={opt} /></span>
              {showCorrect && <CheckCircle2 className="ml-auto text-success" size={18} />}
              {showWrong && <XCircle className="ml-auto text-error" size={18} />}
            </button>
          );
        })}
      </div>

      {!result ? (
        <button
          onClick={submit}
          disabled={submitting}
          className="btn-primary mt-6 w-full disabled:opacity-60"
          data-testid="submit-answer-btn"
        >
          {submitting ? "Submitting…" : "Submit answer"}
        </button>
      ) : (
        <div className="mt-6 p-5 rounded-xl bg-sand/60 border border-edge" data-testid="solution-block">
          <div className="flex items-center gap-2">
            {result.correct ? (
              <><CheckCircle2 className="text-success" /> <span className="font-heading font-semibold text-success">Correct</span></>
            ) : (
              <><XCircle className="text-error" /> <span className="font-heading font-semibold text-error">Incorrect</span></>
            )}
            <span className="text-sm text-muted2 ml-auto">Answer: <MathText text={result.correct_answer} /></span>
          </div>
          <h3 className="font-heading text-lg font-semibold text-ink mt-4">Step-by-step solution</h3>
          <ol className="mt-3 space-y-2 list-none">
            {result.solution_steps.map((s, i) => (
              <li key={i} className="flex gap-3 text-ink" data-testid={`solution-step-${i}`}>
                <span className="font-mono text-xs bg-surface border border-edge px-2 py-0.5 rounded-md h-6 flex-shrink-0">Step {i + 1}</span>
                <span><MathText text={s} /></span>
              </li>
            ))}
          </ol>
          <button onClick={onTryAgain} className="btn-ghost mt-5 text-sm" data-testid="try-again-btn">
            Try this question again
          </button>
          <button
            onClick={onGenerateSimilar}
            className="btn-secondary mt-5 ml-2 text-sm inline-flex items-center gap-2"
            data-testid="generate-similar-btn"
            disabled={similarLoading}
          >
            <Wand2 size={14} /> {similarLoading ? "Generating…" : "Generate similar"}
          </button>
        </div>
      )}
    </>
  );
};

export default ObjectivePane;
