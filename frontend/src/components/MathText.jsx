import React from "react";
import { InlineMath, BlockMath } from "react-katex";

/**
 * Render text containing inline math wrapped in $...$ and block math in $$...$$.
 * Also supports basic newlines (preserves paragraph spacing).
 */
const MathText = ({ text, className = "" }) => {
  if (!text) return null;

  const renderPlain = (value, keyPrefix) => {
    const lines = value.split("\n");
    return lines.map((line, li) => {
      const boldParts = line.split(/(\*\*[^*]+\*\*)/g);
      return (
        <React.Fragment key={`${keyPrefix}-line-${li}`}>
          {boldParts.map((part, pi) => {
            if (part.startsWith("**") && part.endsWith("**")) {
              return <strong key={`${keyPrefix}-b-${li}-${pi}`}>{part.slice(2, -2)}</strong>;
            }
            return <React.Fragment key={`${keyPrefix}-t-${li}-${pi}`}>{part}</React.Fragment>;
          })}
          {li < lines.length - 1 ? <br /> : null}
        </React.Fragment>
      );
    });
  };

  // Split by $$...$$ blocks first
  const blockParts = text.split(/(\$\$[^$]+\$\$)/g);
  return (
    <span className={className}>
      {blockParts.map((bp, bi) => {
        if (bp.startsWith("$$") && bp.endsWith("$$")) {
          const expr = bp.slice(2, -2).trim();
          try {
            return <BlockMath key={`b-${bi}`} math={expr} />;
          } catch {
            return <span key={`b-${bi}`}>{bp}</span>;
          }
        }
        // Inline split by $...$
        const inlineParts = bp.split(/(\$[^$\n]+\$)/g);
        return (
          <React.Fragment key={`f-${bi}`}>
            {inlineParts.map((ip, ii) => {
              if (ip.startsWith("$") && ip.endsWith("$") && ip.length > 2) {
                const expr = ip.slice(1, -1);
                try {
                  return <InlineMath key={`i-${bi}-${ii}`} math={expr} />;
                } catch {
                  return <span key={`i-${bi}-${ii}`}>{ip}</span>;
                }
              }
              return renderPlain(ip, `t-${bi}-${ii}`);
            })}
          </React.Fragment>
        );
      })}
    </span>
  );
};

export default MathText;
