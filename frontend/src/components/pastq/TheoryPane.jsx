import React, { useState } from "react";
import http from "@/lib/api";
import { toast } from "sonner";
import MathText from "@/components/MathText";
import { Wand2 } from "lucide-react";

const TheoryPane = ({ question, onGenerateSimilar, similarLoading }) => {
  const [result, setResult] = useState(null);

  const reveal = async () => {
    try {
      const { data } = await http.post("/attempts", { question_id: question.id, selected: "—" });
      setResult(data);
    } catch (e) {
      toast.error("Could not load solution");
    }
  };

  return (
    <div className="mt-5" data-testid="theory-question">
      {!result ? (
        <button onClick={reveal} className="btn-primary w-full" data-testid="reveal-solution-btn">
          Reveal worked solution
        </button>
      ) : (
        <div className="p-5 rounded-xl bg-sand/60 border border-edge" data-testid="solution-block">
          <div className="text-sm text-muted2">Final answer:</div>
          <div className="font-heading text-lg text-success mt-1">
            <MathText text={result.correct_answer} />
          </div>
          <h3 className="font-heading text-lg font-semibold text-ink mt-4">Worked solution</h3>
          <ol className="mt-3 space-y-2 list-none">
            {result.solution_steps.map((s, i) => (
              <li key={i} className="flex gap-3 text-ink" data-testid={`solution-step-${i}`}>
                <span className="font-mono text-xs bg-surface border border-edge px-2 py-0.5 rounded-md h-6 flex-shrink-0">Step {i + 1}</span>
                <span><MathText text={s} /></span>
              </li>
            ))}
          </ol>
          <button
            onClick={onGenerateSimilar}
            className="btn-secondary mt-5 text-sm inline-flex items-center gap-2"
            data-testid="generate-similar-btn"
            disabled={similarLoading}
          >
            <Wand2 size={14} /> {similarLoading ? "Generating…" : "Generate similar"}
          </button>
        </div>
      )}
    </div>
  );
};

export default TheoryPane;
