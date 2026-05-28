import React from "react";
import MathText from "@/components/MathText";
import { X } from "lucide-react";

const LETTERS = ["A", "B", "C", "D"];

const SimilarBlock = ({ items, onClose }) => {
  if (!items?.length) return null;
  return (
    <div className="mt-6 border-t border-edge pt-5" data-testid="similar-block">
      <div className="flex items-center justify-between">
        <h3 className="font-heading text-lg font-semibold text-ink">Same-lesson practice (similar)</h3>
        <button onClick={onClose} className="p-1 rounded hover:bg-sand" aria-label="close"><X size={16} /></button>
      </div>
      <div className="space-y-4 mt-3">
        {items.map((it, i) => (
          <details key={i} className="card-surface p-4" data-testid={`similar-item-${i}`}>
            <summary className="cursor-pointer text-ink"><MathText text={it.question} /></summary>
            <ol className="mt-3 space-y-1.5">
              {(it.options || []).map((o, oi) => (
                <li key={oi} className="text-sm text-ink flex gap-2">
                  <span className="font-mono text-xs bg-sand border border-edge px-2 rounded">{LETTERS[oi]}</span>
                  <span><MathText text={o} /></span>
                </li>
              ))}
            </ol>
            <div className="text-sm text-success mt-3">Answer: <MathText text={it.answer} /></div>
            <div className="text-xs text-muted2 mt-2">Steps:</div>
            <ol className="mt-1 space-y-1">
              {(it.solution_steps || []).map((s, si) => (
                <li key={si} className="text-sm text-ink">
                  <span className="font-mono text-xs mr-2">{si + 1}</span>
                  <MathText text={s} />
                </li>
              ))}
            </ol>
          </details>
        ))}
      </div>
    </div>
  );
};

export default SimilarBlock;
