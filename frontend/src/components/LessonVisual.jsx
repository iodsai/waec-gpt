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

const RegionLabel = ({ x, y, children }) => (
  <text x={x} y={y} textAnchor="middle" dominantBaseline="middle" fontSize="18" fontWeight="800" fill="#1A1C1A">
    {children}
  </text>
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

const TwoSetVariables = ({ title, caption, labels = {} }) => (
  <div className="rounded-xl border border-edge bg-surface p-4">
    <svg viewBox="0 0 420 230" className="w-full h-auto" role="img" aria-label={title || "Two-set variable Venn diagram"}>
      <rect x="14" y="14" width="392" height="190" rx="14" fill="#F9F7F1" stroke="#E2DCD0" />
      <text x="34" y="44" fontSize="17" fontWeight="700" fill="#1A1C1A">U</text>
      <circle cx="178" cy="112" r="70" fill="#E8B253" fillOpacity="0.28" stroke="#1A1C1A" strokeWidth="2.2" />
      <circle cx="242" cy="112" r="70" fill="#E8B253" fillOpacity="0.28" stroke="#1A1C1A" strokeWidth="2.2" />
      <SetLabel x={128} y={55}>{labels.leftSet || "A"}</SetLabel>
      <SetLabel x={292} y={55}>{labels.rightSet || "B"}</SetLabel>
      <RegionLabel x={158} y={114}>{labels.leftOnly || "x"}</RegionLabel>
      <RegionLabel x={210} y={114}>{labels.overlap || "18"}</RegionLabel>
      <RegionLabel x={262} y={114}>{labels.rightOnly || "y"}</RegionLabel>
      {labels.outside && <RegionLabel x={348} y={174}>{labels.outside}</RegionLabel>}
    </svg>
    <VisualCaption title={title} caption={caption} />
  </div>
);

const ThreeSetMask = ({ id, include = [], exclude = [] }) => {
  const circles = {
    a: { cx: 160, cy: 112, r: 64 },
    b: { cx: 260, cy: 112, r: 64 },
    c: { cx: 210, cy: 176, r: 64 },
  };
  return (
    <mask id={id}>
      <rect x="0" y="0" width="420" height="290" fill="black" />
      {include.map((key) => <circle key={`inc-${key}`} {...circles[key]} fill="white" />)}
      {exclude.map((key) => <circle key={`exc-${key}`} {...circles[key]} fill="black" />)}
    </mask>
  );
};

const ThreeSetRegion = ({ maskId }) => (
  <rect x="20" y="22" width="380" height="242" rx="14" fill="#E8B253" fillOpacity="0.76" mask={`url(#${maskId})`} />
);

const TripleIntersection = ({ uid, muted = false }) => (
  <g clipPath={`url(#clip-3a-${uid})`}>
    <g clipPath={`url(#clip-3b-${uid})`}>
      <circle cx="210" cy="176" r="64" fill={muted ? "#F9F7F1" : "#E8B253"} fillOpacity={muted ? "1" : "0.92"} />
    </g>
  </g>
);

const SetLabel = ({ x, y, children }) => (
  <g>
    <text x={x} y={y} textAnchor="middle" fontSize="18" fontWeight="800" fill="#1A1C1A">{children}</text>
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
      <svg viewBox="0 0 420 290" className="w-full h-auto" role="img" aria-label={title || "Three-set Venn diagram"}>
        <defs>
          <clipPath id={`clip-3a-${uid}`}><circle cx="160" cy="112" r="64" /></clipPath>
          <clipPath id={`clip-3b-${uid}`}><circle cx="260" cy="112" r="64" /></clipPath>
          {Object.entries(regionMasks).map(([name, cfg]) => (
            <ThreeSetMask key={name} id={mask(name)} include={cfg.include} exclude={cfg.exclude} />
          ))}
          <ThreeSetMask id={mask("exactly_one_all_a")} include={["a"]} exclude={["b", "c"]} />
          <ThreeSetMask id={mask("exactly_one_all_b")} include={["b"]} exclude={["a", "c"]} />
          <ThreeSetMask id={mask("exactly_one_all_c")} include={["c"]} exclude={["a", "b"]} />
        </defs>

        <rect x="20" y="22" width="380" height="242" rx="14" fill="#F9F7F1" stroke="#E2DCD0" />
        <text x="38" y="52" fontSize="17" fontWeight="700" fill="#1A1C1A">U</text>

        {variant === "neither_all" && (
          <>
            <rect x="20" y="22" width="380" height="242" rx="14" fill="#E8B253" fillOpacity="0.5" />
            <circle cx="160" cy="112" r="64" fill="#F9F7F1" />
            <circle cx="260" cy="112" r="64" fill="#F9F7F1" />
            <circle cx="210" cy="176" r="64" fill="#F9F7F1" />
          </>
        )}

        {variant === "not_all_three" && (
          <>
            <rect x="20" y="22" width="380" height="242" rx="14" fill="#E8B253" fillOpacity="0.5" />
            <TripleIntersection uid={uid} muted />
          </>
        )}

        {variant === "triple_intersection" && <TripleIntersection uid={uid} />}

        {variant === "at_least_two" && (
          <>
            <g clipPath={`url(#clip-3a-${uid})`}><circle cx="260" cy="112" r="64" fill="#E8B253" fillOpacity="0.78" /></g>
            <g clipPath={`url(#clip-3a-${uid})`}><circle cx="210" cy="176" r="64" fill="#E8B253" fillOpacity="0.78" /></g>
            <g clipPath={`url(#clip-3b-${uid})`}><circle cx="210" cy="176" r="64" fill="#E8B253" fillOpacity="0.78" /></g>
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

        <circle cx="160" cy="112" r="64" fill="none" stroke="#1A1C1A" strokeWidth="2.2" />
        <circle cx="260" cy="112" r="64" fill="none" stroke="#1A1C1A" strokeWidth="2.2" />
        <circle cx="210" cy="176" r="64" fill="none" stroke="#1A1C1A" strokeWidth="2.2" />
        <SetLabel x={119} y={58}>A</SetLabel>
        <SetLabel x={301} y={58}>B</SetLabel>
        <SetLabel x={210} y={258}>C</SetLabel>
      </svg>
      <VisualCaption title={title} caption={caption} />
    </div>
  );
};

const ThreeSetVariables = ({ title, caption, labels = {} }) => (
  <div className="rounded-xl border border-edge bg-surface p-4">
    <svg viewBox="0 0 520 390" className="w-full h-auto" role="img" aria-label={title || "Three-set variable Venn diagram"}>
      <rect x="24" y="28" width="472" height="328" rx="16" fill="#F9F7F1" stroke="#E2DCD0" />
      <text x="48" y="62" fontSize="18" fontWeight="800" fill="#1A1C1A">U</text>

      <circle cx="205" cy="155" r="92" fill="#E8B253" fillOpacity="0.14" stroke="#1A1C1A" strokeWidth="2.4" />
      <circle cx="315" cy="155" r="92" fill="#E8B253" fillOpacity="0.14" stroke="#1A1C1A" strokeWidth="2.4" />
      <circle cx="260" cy="245" r="92" fill="#E8B253" fillOpacity="0.14" stroke="#1A1C1A" strokeWidth="2.4" />

      <SetLabel x={145} y={73}>{labels.leftSet || "P"}</SetLabel>
      <SetLabel x={375} y={73}>{labels.rightSet || "C"}</SetLabel>
      <SetLabel x={260} y={345}>{labels.bottomSet || "B"}</SetLabel>

      <RegionLabel x={165} y={158}>{labels.leftOnly || "x"}</RegionLabel>
      <RegionLabel x={355} y={158}>{labels.rightOnly || "y"}</RegionLabel>
      <RegionLabel x={260} y={296}>{labels.bottomOnly || "z"}</RegionLabel>

      <RegionLabel x={260} y={132}>{labels.leftRight || "9"}</RegionLabel>
      <RegionLabel x={216} y={217}>{labels.leftBottom || "11"}</RegionLabel>
      <RegionLabel x={304} y={217}>{labels.rightBottom || "7"}</RegionLabel>
      <RegionLabel x={260} y={192}>{labels.allThree || "5"}</RegionLabel>
      {labels.outside && <RegionLabel x={440} y={314}>{labels.outside}</RegionLabel>}
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
  if (block.type === "venn3") {
    return <ThreeSetVenn variant={block.variant} title={block.title} caption={block.caption} />;
  }
  if (block.type === "venn_variables") {
    return <TwoSetVariables title={block.title} caption={block.caption} labels={block.labels || {}} />;
  }
  if (block.type === "venn3_variables") {
    return <ThreeSetVariables title={block.title} caption={block.caption} labels={block.labels || {}} />;
  }
  return (
    <div className="rounded-xl border border-edge bg-sand/50 p-4">
      <div className="font-heading font-semibold text-ink"><MathText text={block.title || "Visual"} /></div>
      {block.caption && <p className="text-sm text-muted2 mt-1"><MathText text={block.caption} /></p>}
    </div>
  );
};

export default LessonVisual;
