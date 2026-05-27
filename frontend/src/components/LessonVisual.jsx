import React, { useId } from "react";
import MathText from "@/components/MathText";

const vennConfig = {
  disjoint: { left: false, overlap: false, right: false },
  intersection: { left: false, overlap: true, right: false },
  union: { left: true, overlap: true, right: true },
  difference: { left: true, overlap: false, right: false },
  exactly_one: { left: true, overlap: false, right: true },
};

const Fill = ({ active, children }) => (
  <g className={active ? "text-warning" : "text-transparent"}>{children}</g>
);

const VisualCaption = ({ title, caption }) => (
  (title || caption) ? (
    <div className="mt-3">
      {title && <div className="font-heading font-semibold text-ink"><MathText text={title} /></div>}
      {caption && <p className="text-sm text-muted2 mt-1"><MathText text={caption} /></p>}
    </div>
  ) : null
);

const SingleSet = ({ title, caption }) => (
  <div className="rounded-xl border border-edge bg-surface p-4">
    <svg viewBox="0 0 360 200" className="w-full h-auto" role="img" aria-label={title || "Set diagram"}>
      <rect x="8" y="8" width="344" height="184" rx="14" fill="#F9F7F1" stroke="#E2DCD0" />
      <text x="24" y="36" fontSize="18" fill="#1A1C1A">U</text>
      <circle cx="180" cy="104" r="58" fill="#E8B253" fillOpacity="0.75" stroke="#1A1C1A" strokeWidth="2" />
      <text x="174" y="111" fontSize="21" fill="#1A1C1A">A</text>
    </svg>
    <VisualCaption title={title} caption={caption} />
  </div>
);

const ComplementA = ({ title, caption }) => (
  <div className="rounded-xl border border-edge bg-surface p-4">
    <svg viewBox="0 0 360 200" className="w-full h-auto" role="img" aria-label={title || "Complement diagram"}>
      <rect x="8" y="8" width="344" height="184" rx="14" fill="#E8B253" fillOpacity="0.55" stroke="#E2DCD0" />
      <text x="24" y="36" fontSize="18" fill="#1A1C1A">U</text>
      <circle cx="180" cy="104" r="58" fill="#F9F7F1" stroke="#1A1C1A" strokeWidth="2" />
      <text x="174" y="111" fontSize="21" fill="#1A1C1A">A</text>
      <text x="246" y="54" fontSize="18" fill="#1A1C1A">A'</text>
    </svg>
    <VisualCaption title={title} caption={caption} />
  </div>
);

const Subset = ({ title, caption }) => (
  <div className="rounded-xl border border-edge bg-surface p-4">
    <svg viewBox="0 0 360 200" className="w-full h-auto" role="img" aria-label={title || "Subset diagram"}>
      <rect x="8" y="8" width="344" height="184" rx="14" fill="#F9F7F1" stroke="#E2DCD0" />
      <text x="24" y="36" fontSize="18" fill="#1A1C1A">U</text>
      <circle cx="150" cy="104" r="66" fill="none" stroke="#1A1C1A" strokeWidth="2" />
      <circle cx="150" cy="104" r="34" fill="#E8B253" fillOpacity="0.75" stroke="#1A1C1A" strokeWidth="2" />
      <text x="144" y="112" fontSize="21" fill="#1A1C1A">B</text>
      <text x="144" y="180" fontSize="21" fill="#1A1C1A">A</text>
      <text x="235" y="94" fontSize="16" fill="#1A1C1A">B subset A</text>
      <text x="235" y="119" fontSize="16" fill="#1A1C1A">B is inside A</text>
    </svg>
    <VisualCaption title={title} caption={caption} />
  </div>
);

const Neither = ({ title, caption }) => (
  <div className="rounded-xl border border-edge bg-surface p-4">
    <svg viewBox="0 0 360 200" className="w-full h-auto" role="img" aria-label={title || "Neither diagram"}>
      <rect x="8" y="8" width="344" height="184" rx="14" fill="#E8B253" fillOpacity="0.55" stroke="#E2DCD0" />
      <text x="24" y="36" fontSize="18" fill="#1A1C1A">U</text>
      <circle cx="154" cy="106" r="56" fill="#F9F7F1" />
      <circle cx="206" cy="106" r="56" fill="#F9F7F1" />
      <circle cx="154" cy="106" r="56" fill="none" stroke="#1A1C1A" strokeWidth="2" />
      <circle cx="206" cy="106" r="56" fill="none" stroke="#1A1C1A" strokeWidth="2" />
      <text x="149" y="179" fontSize="20" fill="#1A1C1A">A</text>
      <text x="204" y="179" fontSize="20" fill="#1A1C1A">B</text>
    </svg>
    <VisualCaption title={title} caption={caption} />
  </div>
);

const TwoSetVenn = ({ variant = "union", title, caption }) => {
  const uid = useId().replace(/:/g, "");
  const cfg = vennConfig[variant] || vennConfig.union;

  if (variant === "set_a") return <SingleSet title={title} caption={caption} />;
  if (variant === "complement_a") return <ComplementA title={title} caption={caption} />;
  if (variant === "subset") return <Subset title={title} caption={caption} />;
  if (variant === "neither") return <Neither title={title} caption={caption} />;

  return (
    <div className="rounded-xl border border-edge bg-surface p-4">
      <svg viewBox="0 0 360 200" className="w-full h-auto" role="img" aria-label={title || "Venn diagram"}>
        <rect x="8" y="8" width="344" height="184" rx="14" fill="#F9F7F1" stroke="#E2DCD0" />
        <text x="24" y="36" fontSize="18" fill="#1A1C1A">U</text>
        {variant === "disjoint" ? (
          <>
            <circle cx="128" cy="106" r="50" fill="none" stroke="#1A1C1A" strokeWidth="2" />
            <circle cx="232" cy="106" r="50" fill="none" stroke="#1A1C1A" strokeWidth="2" />
          </>
        ) : (
          <>
            <defs>
              <clipPath id={`clip-left-${uid}`}>
                <circle cx="154" cy="106" r="56" />
              </clipPath>
            </defs>
            <Fill active={cfg.left}>
              <circle cx="154" cy="106" r="56" fill="currentColor" fillOpacity="0.75" />
            </Fill>
            <Fill active={cfg.right}>
              <circle cx="206" cy="106" r="56" fill="currentColor" fillOpacity="0.75" />
            </Fill>
            <Fill active={cfg.overlap}>
              <circle cx="206" cy="106" r="56" fill="currentColor" fillOpacity="0.85" clipPath={`url(#clip-left-${uid})`} />
            </Fill>
            <circle cx="154" cy="106" r="56" fill="none" stroke="#1A1C1A" strokeWidth="2" />
            <circle cx="206" cy="106" r="56" fill="none" stroke="#1A1C1A" strokeWidth="2" />
          </>
        )}
        <text x="149" y="179" fontSize="20" fill="#1A1C1A">A</text>
        <text x="204" y="179" fontSize="20" fill="#1A1C1A">B</text>
      </svg>
      <VisualCaption title={title} caption={caption} />
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
      <div className="font-heading font-semibold text-ink"><MathText text={block.title || "Visual"} /></div>
      {block.caption && <p className="text-sm text-muted2 mt-1"><MathText text={block.caption} /></p>}
    </div>
  );
};

export default LessonVisual;
