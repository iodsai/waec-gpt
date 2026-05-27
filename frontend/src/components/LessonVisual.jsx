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

const ThreeSetMask = ({ id, include = [], exclude = [] }) => {
  const circles = {
    a: { cx: 142, cy: 92, r: 58 },
    b: { cx: 218, cy: 92, r: 58 },
    c: { cx: 180, cy: 144, r: 58 },
  };
  return (
    <mask id={id}>
      <rect x="0" y="0" width="420" height="260" fill="black" />
      {include.map((key) => <circle key={`inc-${key}`} {...circles[key]} fill="white" />)}
      {exclude.map((key) => <circle key={`exc-${key}`} {...circles[key]} fill="black" />)}
    </mask>
  );
};

const ThreeSetRegion = ({ maskId }) => (
  <rect x="10" y="10" width="400" height="230" rx="14" fill="#E8B253" fillOpacity="0.78" mask={`url(#${maskId})`} />
);

const TripleIntersection = ({ uid, muted = false }) => (
  <g clipPath={`url(#clip-3a-${uid})`}>
    <g clipPath={`url(#clip-3b-${uid})`}>
      <circle cx="180" cy="144" r="58" fill={muted ? "#F9F7F1" : "#E8B253"} fillOpacity={muted ? "1" : "0.9"} />
    </g>
  </g>
);

const ThreeSetVenn = ({ variant = "union_all", title, caption }) => {
  const uid = useId().replace(/:/g, "");
  const mask = (name) => `${name}-${uid}`;
  const regionMasks = {
    union_all: { include: ["a", "b", "c"], exclude: [] },
    a_only: { include: ["a"], exclude: ["b", "c"] },
    b_only: { include: ["b"], exclude: ["a", "c"] },
    c_only: { include: ["c"], exclude: ["a", "b"] },
    a_complement_intersect_b_union_c: { include: ["b", "c"], exclude: ["a"] },
  };

  return (
    <div className="rounded-xl border border-edge bg-surface p-4">
      <svg viewBox="0 0 420 260" className="w-full h-auto" role="img" aria-label={title || "Three-set Venn diagram"}>
        <defs>
          <clipPath id={`clip-3a-${uid}`}><circle cx="142" cy="92" r="58" /></clipPath>
          <clipPath id={`clip-3b-${uid}`}><circle cx="218" cy="92" r="58" /></clipPath>
          {Object.entries(regionMasks).map(([name, cfg]) => (
            <ThreeSetMask key={name} id={mask(name)} include={cfg.include} exclude={cfg.exclude} />
          ))}
          <ThreeSetMask id={mask("exactly_one_all_a")} include={["a"]} exclude={["b", "c"]} />
          <ThreeSetMask id={mask("exactly_one_all_b")} include={["b"]} exclude={["a", "c"]} />
          <ThreeSetMask id={mask("exactly_one_all_c")} include={["c"]} exclude={["a", "b"]} />
        </defs>

        <rect x="10" y="10" width="400" height="230" rx="14" fill="#F9F7F1" stroke="#E2DCD0" />
        <text x="28" y="39" fontSize="18" fill="#1A1C1A">U</text>

        {variant === "neither_all" && (
          <>
            <rect x="10" y="10" width="400" height="230" rx="14" fill="#E8B253" fillOpacity="0.55" />
            <circle cx="142" cy="92" r="58" fill="#F9F7F1" />
            <circle cx="218" cy="92" r="58" fill="#F9F7F1" />
            <circle cx="180" cy="144" r="58" fill="#F9F7F1" />
          </>
        )}

        {variant === "not_all_three" && (
          <>
            <rect x="10" y="10" width="400" height="230" rx="14" fill="#E8B253" fillOpacity="0.55" />
            <TripleIntersection uid={uid} muted />
          </>
        )}

        {variant === "triple_intersection" && <TripleIntersection uid={uid} />}

        {variant === "at_least_two" && (
          <>
            <g clipPath={`url(#clip-3a-${uid})`}><circle cx="218" cy="92" r="58" fill="#E8B253" fillOpacity="0.78" /></g>
            <g clipPath={`url(#clip-3a-${uid})`}><circle cx="180" cy="144" r="58" fill="#E8B253" fillOpacity="0.78" /></g>
            <g clipPath={`url(#clip-3b-${uid})`}><circle cx="180" cy="144" r="58" fill="#E8B253" fillOpacity="0.78" /></g>
          </>
        )}

        {variant === "exactly_one_all" && (
          <>
            <ThreeSetRegion maskId={mask("exactly_one_all_a")} />
            <ThreeSetRegion maskId={mask("exactly_one_all_b")} />
            <ThreeSetRegion maskId={mask("exactly_one_all_c")} />
          </>
        )}

        {regionMasks[variant] && <ThreeSetRegion maskId={mask(variant)} />}

        <circle cx="142" cy="92" r="58" fill="none" stroke="#1A1C1A" strokeWidth="2" />
        <circle cx="218" cy="92" r="58" fill="none" stroke="#1A1C1A" strokeWidth="2" />
        <circle cx="180" cy="144" r="58" fill="none" stroke="#1A1C1A" strokeWidth="2" />
        <text x="105" y="58" fontSize="20" fill="#1A1C1A">A</text>
        <text x="250" y="58" fontSize="20" fill="#1A1C1A">B</text>
        <text x="180" y="219" fontSize="20" fill="#1A1C1A">C</text>
      </svg>
      <VisualCaption title={title} caption={caption} />
    </div>
  );
};

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
  if (block.type === "venn3") {
    return <ThreeSetVenn variant={block.variant} title={block.title} caption={block.caption} />;
  }
  return (
    <div className="rounded-xl border border-edge bg-sand/50 p-4">
      <div className="font-heading font-semibold text-ink"><MathText text={block.title || "Visual"} /></div>
      {block.caption && <p className="text-sm text-muted2 mt-1"><MathText text={block.caption} /></p>}
    </div>
  );
};

export default LessonVisual;
