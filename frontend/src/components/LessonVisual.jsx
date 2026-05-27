import React, { useId } from "react";

const vennConfig = {
  set_a: { left: true, overlap: true, right: false, outside: false, label: "Set A" },
  complement_a: { left: false, overlap: false, right: true, outside: true, label: "Complement of A" },
  disjoint: { left: false, overlap: false, right: false, outside: false, label: "Disjoint sets" },
  subset: { subset: true, label: "B is a proper subset of A" },
  intersection: { left: false, overlap: true, right: false, outside: false, label: "A intersection B" },
  union: { left: true, overlap: true, right: true, outside: false, label: "A union B" },
  difference: { left: true, overlap: false, right: false, outside: false, label: "A minus B" },
};

const Fill = ({ active, children }) => (
  <g className={active ? "text-warning" : "text-transparent"}>{children}</g>
);

const TwoSetVenn = ({ variant = "union", title, caption }) => {
  const uid = useId().replace(/:/g, "");
  const cfg = vennConfig[variant] || vennConfig.union;
  if (cfg.subset) {
    return (
      <div className="rounded-xl border border-edge bg-surface p-4">
        <svg viewBox="0 0 360 190" className="w-full h-auto" role="img" aria-label={title || cfg.label}>
          <rect x="8" y="8" width="344" height="174" rx="14" fill="#F9F7F1" stroke="#E2DCD0" />
          <text x="24" y="34" fontSize="18" fill="#1A1C1A">U</text>
          <circle cx="132" cy="96" r="64" fill="none" stroke="#1A1C1A" strokeWidth="2" />
          <circle cx="132" cy="96" r="33" fill="#E8B253" fillOpacity="0.75" stroke="#1A1C1A" strokeWidth="2" />
          <text x="124" y="104" fontSize="20" fill="#1A1C1A">B</text>
          <text x="124" y="172" fontSize="20" fill="#1A1C1A">A</text>
          <text x="220" y="86" fontSize="16" fill="#1A1C1A">B subset A</text>
          <text x="220" y="110" fontSize="16" fill="#1A1C1A">B is inside A</text>
        </svg>
        {(title || caption) && (
          <div className="mt-3">
            {title && <div className="font-heading font-semibold text-ink">{title}</div>}
            {caption && <p className="text-sm text-muted2 mt-1">{caption}</p>}
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-edge bg-surface p-4">
      <svg viewBox="0 0 420 220" className="w-full h-auto" role="img" aria-label={title || cfg.label}>
        <rect x="8" y="8" width="404" height="204" rx="14" fill={cfg.outside ? "#E8B253" : "#F9F7F1"} fillOpacity={cfg.outside ? "0.55" : "1"} stroke="#E2DCD0" />
        <text x="24" y="36" fontSize="18" fill="#1A1C1A">U</text>
        {variant === "disjoint" ? (
          <>
            <circle cx="140" cy="108" r="58" fill="none" stroke="#1A1C1A" strokeWidth="2" />
            <circle cx="280" cy="108" r="58" fill="none" stroke="#1A1C1A" strokeWidth="2" />
          </>
        ) : (
          <>
            <defs>
              <clipPath id={`clip-left-${uid}`}>
                <circle cx="172" cy="108" r="62" />
              </clipPath>
              <clipPath id={`clip-right-${uid}`}>
                <circle cx="248" cy="108" r="62" />
              </clipPath>
            </defs>
            <Fill active={cfg.left}>
              <circle cx="172" cy="108" r="62" fill="currentColor" fillOpacity="0.75" />
            </Fill>
            <Fill active={cfg.right}>
              <circle cx="248" cy="108" r="62" fill="currentColor" fillOpacity="0.75" />
            </Fill>
            <Fill active={cfg.overlap}>
              <circle cx="248" cy="108" r="62" fill="currentColor" fillOpacity="0.85" clipPath={`url(#clip-left-${uid})`} />
            </Fill>
            <circle cx="172" cy="108" r="62" fill="none" stroke="#1A1C1A" strokeWidth="2" />
            <circle cx="248" cy="108" r="62" fill="none" stroke="#1A1C1A" strokeWidth="2" />
          </>
        )}
        <text x="160" y="190" fontSize="20" fill="#1A1C1A">A</text>
        <text x="246" y="190" fontSize="20" fill="#1A1C1A">B</text>
        <text x="300" y="92" fontSize="16" fill="#1A1C1A">{cfg.label}</text>
      </svg>
      {(title || caption) && (
        <div className="mt-3">
          {title && <div className="font-heading font-semibold text-ink">{title}</div>}
          {caption && <p className="text-sm text-muted2 mt-1">{caption}</p>}
        </div>
      )}
    </div>
  );
};

const LessonVisual = ({ block }) => {
  if (!block) return null;
  if (block.type === "venn") {
    return <TwoSetVenn variant={block.variant} title={block.title} caption={block.caption} />;
  }
  return (
    <div className="rounded-xl border border-edge bg-sand/50 p-4">
      <div className="font-heading font-semibold text-ink">{block.title || "Visual"}</div>
      {block.caption && <p className="text-sm text-muted2 mt-1">{block.caption}</p>}
    </div>
  );
};

export default LessonVisual;
