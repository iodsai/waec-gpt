import React, { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import http from "@/lib/api";
import MathText from "@/components/MathText";
import LessonVisual from "@/components/LessonVisual";
import { ArrowLeft, BookOpen, CheckCircle2, ChevronRight, Lightbulb, ListChecks, Lock, Target, TriangleAlert } from "lucide-react";

const sectionSlug = (value = "") => value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");

const BulletList = ({ items = [] }) => {
  if (!items.length) return null;
  return (
    <ul className="space-y-2">
      {items.map((item, i) => (
        <li key={`${item}-${i}`} className="flex items-start gap-2 text-sm text-ink">
          <CheckCircle2 size={15} className="text-success mt-0.5 shrink-0" />
          <span><MathText text={item} /></span>
        </li>
      ))}
    </ul>
  );
};

const RichCard = ({ title, children, icon: Icon = Lightbulb }) => (
  <div className="card-surface p-6">
    <div className="flex items-center gap-2">
      <Icon size={18} className="text-terracotta" />
      <h2 className="font-heading text-xl font-semibold text-ink">{title}</h2>
    </div>
    <div className="mt-4">{children}</div>
  </div>
);

const normalizeAnswer = (value = "") => String(value)
  .toLowerCase()
  .replace(/\$|\\|\{|\}|\(|\)|\.|,/g, "")
  .replace(/\s+/g, " ")
  .trim();

const answerMatches = (student, expected) => {
  const s = normalizeAnswer(student);
  const e = normalizeAnswer(expected);
  if (!s || !e) return false;
  if (s === e) return true;
  return e.length > 12 && (s.includes(e) || e.includes(s));
};

const progressKey = (sectionKey, item, index) => `waec_lesson_checkpoint:${sectionKey}:${index}:${item.question || item.problem || item.title || "item"}`;

const InteractivePracticePanel = ({ item, index, sectionKey, label = "Checkpoint", onAnswered }) => {
  const key = progressKey(sectionKey, item, index);
  const [value, setValue] = useState("");
  const [state, setState] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem(key) || "null");
    } catch {
      return null;
    }
  });
  const options = item.options || [];
  const expected = item.answer || (item.solution || []).join(" ");
  const isObjective = options.length > 0;
  const isLongAnswer = !isObjective && normalizeAnswer(expected).length > 42;

  const submit = () => {
    const trimmed = value.trim();
    if (!trimmed) return;
    const correct = isLongAnswer ? null : answerMatches(trimmed, expected);
    const payload = { submitted: true, value: trimmed, correct, at: new Date().toISOString() };
    setState(payload);
    localStorage.setItem(key, JSON.stringify(payload));
    onAnswered?.(payload);
  };

  const reset = () => {
    setValue("");
    setState(null);
    localStorage.removeItem(key);
    onAnswered?.(null);
  };

  return (
    <div className="rounded-xl border border-edge bg-surface p-4" data-testid={`interactive-checkpoint-${index}`}>
      <div className="text-xs uppercase tracking-[0.18em] text-terracotta font-bold">{label} {index + 1}</div>
      <div className="text-sm font-medium text-ink mt-2"><MathText text={item.question || item.problem} /></div>

      {!state?.submitted && (
        <div className="mt-3 space-y-3">
          {isObjective ? (
            <div className="grid gap-2">
              {options.map((option, oi) => (
                <button
                  key={`${option}-${oi}`}
                  type="button"
                  onClick={() => setValue(option)}
                  className={`text-left rounded-lg border px-3 py-2 text-sm ${value === option ? "border-terracotta bg-terracotta/5 text-ink" : "border-edge bg-paper text-muted2 hover:text-ink"}`}
                >
                  <span className="font-heading font-bold mr-2">{String.fromCharCode(65 + oi)}</span>
                  <MathText text={option} />
                </button>
              ))}
            </div>
          ) : (
            <textarea
              value={value}
              onChange={(e) => setValue(e.target.value)}
              rows={3}
              className="w-full rounded-lg border border-edge bg-paper px-3 py-2 text-sm text-ink outline-none focus:border-terracotta"
              placeholder="Type your answer before revealing the model solution..."
            />
          )}
          <button type="button" onClick={submit} disabled={!value.trim()} className="btn-primary text-sm disabled:opacity-50">
            Check answer
          </button>
        </div>
      )}

      {state?.submitted && (
        <div className="mt-3 rounded-lg border border-edge bg-sand/40 p-3">
          <div className={`text-sm font-heading font-semibold ${state.correct === true ? "text-success" : state.correct === false ? "text-error" : "text-terracotta"}`}>
            {state.correct === true ? "Correct. Move forward." : state.correct === false ? "Not quite. Compare your answer and try again." : "Submitted. Compare your reasoning with the model answer."}
          </div>
          <div className="text-sm text-muted2 mt-2">Your answer: <MathText text={state.value} /></div>
          {expected && <div className="text-sm text-ink mt-2">Model answer: <MathText text={expected} /></div>}
          {item.solution?.length > 0 && <div className="mt-3"><BulletList items={item.solution} /></div>}
          <div className="flex flex-wrap gap-2 mt-3">
            <button type="button" onClick={reset} className="btn-ghost text-sm">Try again</button>
          </div>
        </div>
      )}
    </div>
  );
};

const WorkedExamplePanel = ({ example, index }) => (
  <div className="rounded-xl border border-edge bg-sand/40 p-5">
    <div className="flex items-center gap-2 flex-wrap">
      <span className="tag">{example.level || `example ${index + 1}`}</span>
      <h4 className="font-heading text-base font-semibold text-ink">{example.title}</h4>
    </div>
    {example.problem && <p className="text-sm text-ink mt-3"><MathText text={example.problem} /></p>}
    {example.visual_blocks?.length > 0 && (
      <div className="grid md:grid-cols-2 gap-4 mt-4">
        {example.visual_blocks.map((block, i) => (
          <div key={`${block.type}-${block.variant || "example"}-${i}`} className={block.type === "venn3_variables" ? "md:col-span-2 max-w-2xl mx-auto w-full" : ""}>
            <LessonVisual block={block} />
          </div>
        ))}
      </div>
    )}
    {example.steps?.length > 0 && (
      <ol className="mt-4 space-y-2">
        {example.steps.map((step, idx) => (
          <li key={`${step}-${idx}`} className="flex gap-3 text-sm text-ink">
            <span className="font-heading text-terracotta font-bold">{idx + 1}</span>
            <span><MathText text={step} /></span>
          </li>
        ))}
      </ol>
    )}
    {example.answer && <div className="mt-4 rounded-lg bg-success/10 text-success px-4 py-2 text-sm font-medium"><MathText text={example.answer} /></div>}
    {example.examiner_tip && (
      <div className="mt-4 rounded-lg border border-terracotta/30 bg-terracotta/5 px-4 py-3 text-sm text-ink">
        <div className="font-heading font-semibold text-terracotta">Chief Examiner Tip</div>
        <div className="mt-1"><MathText text={example.examiner_tip} /></div>
      </div>
    )}
  </div>
);

const PracticePanel = ({ item, index }) => (
  <div className="rounded-xl border border-edge bg-surface p-4">
    <div className="text-xs uppercase tracking-[0.18em] text-terracotta font-bold">Practice {index + 1}</div>
    <div className="text-sm font-medium text-ink mt-2"><MathText text={item.question || item.problem} /></div>
    {item.solution?.length > 0 && <div className="mt-3"><BulletList items={item.solution} /></div>}
    {item.answer && <div className="text-sm text-muted2 mt-3">Answer: <MathText text={item.answer} /></div>}
  </div>
);

const LockedBlock = ({ children }) => (
  <div className="mt-5 rounded-xl border border-edge bg-sand/40 p-5 text-muted2 flex items-start gap-3">
    <Lock size={18} className="text-terracotta shrink-0 mt-0.5" />
    <div className="text-sm">{children}</div>
  </div>
);

const SectionCard = ({ section, index, subtopicId, challenge = false }) => (
  <Link
    to={`/lessons/${subtopicId}/sections/${sectionSlug(section.title)}`}
    target="_blank"
    rel="noreferrer"
    className={`card-surface p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 group ${challenge ? "border-terracotta/40 bg-sand/50" : ""}`}
    data-testid={`lesson-section-link-${index}`}
  >
    <div className="flex gap-4">
      <span className="font-heading text-terracotta font-bold text-2xl">{String(index + 1).padStart(2, "0")}</span>
      <div>
        <div className="flex items-center gap-2 flex-wrap">
          <h3 className="font-heading text-xl font-semibold text-ink group-hover:text-terracotta">{section.title}</h3>
          {challenge && <span className="tag !text-terracotta">WAEC+ challenge</span>}
        </div>
        {section.intro && <p className="text-sm text-muted2 mt-1 line-clamp-2"><MathText text={section.intro} /></p>}
        <div className="flex flex-wrap gap-2 mt-3">
          {section.visual_blocks?.length > 0 && <span className="tag">{section.visual_blocks.length} visuals</span>}
          {section.examples?.length > 0 && <span className="tag">{section.examples.length} examples</span>}
          {section.practice?.length > 0 && <span className="tag">{section.practice.length} practice</span>}
          {section.diagnostic_checks?.length > 0 && <span className="tag">{section.diagnostic_checks.length} diagnostics</span>}
        </div>
      </div>
    </div>
    <span className="btn-secondary inline-flex items-center gap-2 justify-center shrink-0">
      Open unit <ChevronRight size={16} />
    </span>
  </Link>
);

const statusStyle = {
  mastered: "!bg-success/10 !text-success",
  developing: "!bg-terracotta/10 !text-terracotta",
  review: "!bg-error/10 !text-error",
  not_started: "",
};

const SetsLearningEngine = ({ mastery, courseName = "Sets", testId = "sets-learning-engine" }) => {
  const courseLower = courseName.toLowerCase();
  if (!mastery) {
    return (
      <div className="card-surface p-6 flex items-center gap-3 text-muted2" data-testid={`${testId}-loading`}>
        <Target size={18} className="text-terracotta" /> Loading {courseName} mastery engine...
      </div>
    );
  }
  const next = mastery.summary?.next_module;
  const modules = mastery.modules || [];
  return (
    <div className="card-surface p-6" data-testid={testId}>
      <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-5">
        <div>
          <span className="overline">Learning engine</span>
          <h2 className="font-heading text-2xl font-semibold text-ink mt-2">Teach, diagnose, remediate, retest</h2>
          <p className="text-sm text-muted2 mt-2 max-w-2xl">
            This panel watches your {courseName} attempts, finds weak modules and mistake patterns, then sends you back to the right lesson section and a fresh retest.
          </p>
        </div>
        <div className="rounded-xl border border-edge bg-sand/40 p-4 min-w-[220px]">
          <div className="text-xs uppercase tracking-[0.18em] text-muted2 font-bold">Mastery</div>
          <div className="font-heading text-3xl font-bold text-ink mt-1">
            {mastery.summary.modules_mastered}/{mastery.summary.total_modules}
          </div>
          <div className="text-sm text-muted2">{mastery.summary.average_mastery}% average attempted accuracy</div>
        </div>
      </div>

      <div className="grid md:grid-cols-4 gap-3 mt-5">
        <Link to="#guided-sections" className="rounded-xl border border-edge bg-surface p-4 hover:border-terracotta/40">
          <div className="font-heading font-semibold text-ink">1. Teach</div>
          <p className="text-sm text-muted2 mt-1">Open the module lesson and examples.</p>
        </Link>
        <Link to={mastery.diagnostic.path} className="rounded-xl border border-edge bg-surface p-4 hover:border-terracotta/40">
          <div className="font-heading font-semibold text-ink">2. Diagnose</div>
          <p className="text-sm text-muted2 mt-1">Take a mixed {courseName} diagnostic.</p>
        </Link>
        <Link to={next?.lesson_path || "#guided-sections"} className="rounded-xl border border-edge bg-surface p-4 hover:border-terracotta/40">
          <div className="font-heading font-semibold text-ink">3. Remediate</div>
          <p className="text-sm text-muted2 mt-1">{mastery.summary.next_action}</p>
        </Link>
        <Link to={next?.retest_path || mastery.diagnostic.path} className="rounded-xl border border-edge bg-surface p-4 hover:border-terracotta/40">
          <div className="font-heading font-semibold text-ink">4. Retest</div>
          <p className="text-sm text-muted2 mt-1">Try fresh questions for the weak module.</p>
        </Link>
      </div>

      <div className="mt-5 grid md:grid-cols-2 gap-3">
        {modules.map((module) => (
          <div key={module.module} className="rounded-xl border border-edge bg-surface p-4" data-testid={`${courseLower}-module-mastery-${module.module}`}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="text-xs uppercase tracking-[0.18em] text-terracotta font-bold">Module {module.module}</div>
                <div className="font-heading font-semibold text-ink mt-1">{module.title}</div>
              </div>
              <span className={`tag ${statusStyle[module.status] || ""}`}>{module.status.replace("_", " ")}</span>
            </div>
            <div className="text-sm text-muted2 mt-2">
              {module.attempts ? `${module.correct}/${module.attempts} correct (${module.accuracy}%)` : "No diagnostic attempts yet"}
            </div>
            {module.weak_tags?.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-3">
                {module.weak_tags.map((tag) => <span key={tag.tag} className="tag !text-error">{tag.tag}</span>)}
              </div>
            )}
            <p className="text-sm text-ink/80 mt-3">{module.remediation}</p>
            <div className="flex flex-wrap gap-2 mt-4">
              <Link className="btn-ghost text-sm" to={module.lesson_path}>Review</Link>
              <Link className="btn-secondary text-sm" to={module.retest_path}>Retest</Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const LessonSection = ({ section, index, sectionKey, onCompletionChange }) => {
  const requiredStart = useMemo(() => section.diagnostic_checks || [], [section]);
  const requiredQuiz = useMemo(() => section.module_quiz || [], [section]);
  const checkpointComplete = useCallback((items, prefix) => items.length === 0 || items.every((item, i) => {
    try {
      return JSON.parse(localStorage.getItem(progressKey(`${sectionKey}:${prefix}`, item, i)) || "null")?.submitted;
    } catch {
      return false;
    }
  }), [sectionKey]);
  const [startUnlocked, setStartUnlocked] = useState(() => checkpointComplete(requiredStart, "start"));
  const [quizComplete, setQuizComplete] = useState(() => checkpointComplete(requiredQuiz, "quiz"));
  const refresh = useCallback(() => {
    const start = checkpointComplete(requiredStart, "start");
    const quiz = checkpointComplete(requiredQuiz, "quiz");
    setStartUnlocked(start);
    setQuizComplete(quiz);
    onCompletionChange?.(requiredQuiz.length ? quiz : start);
  }, [checkpointComplete, onCompletionChange, requiredQuiz, requiredStart]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const contentUnlocked = startUnlocked;

  return (
  <section className="card-surface p-7" data-testid={`lesson-section-${index}`}>
    <div className="flex items-start gap-4">
      <span className="font-heading text-terracotta font-bold text-2xl">{String(index + 1).padStart(2, "0")}</span>
      <div>
        <div className="flex items-center gap-2">
          <BookOpen size={18} className="text-terracotta" />
          <h2 className="font-heading text-2xl font-semibold text-ink">{section.title}</h2>
          {section.track === "challenge" && <span className="tag !text-terracotta">WAEC+ challenge</span>}
        </div>
        {section.intro && <p className="text-muted2 mt-2 leading-relaxed"><MathText text={section.intro} /></p>}
      </div>
    </div>

    {section.diagnostic_checks?.length > 0 && (
      <div className="mt-5 rounded-xl border border-edge bg-surface p-5">
        <h3 className="font-heading font-semibold text-ink">Before you start</h3>
        <div className="grid md:grid-cols-2 gap-3 mt-3">
          {section.diagnostic_checks.map((item, i) => (
            <InteractivePracticePanel key={`${item.question}-${i}`} item={item} index={i} sectionKey={`${sectionKey}:start`} label="Start check" onAnswered={refresh} />
          ))}
        </div>
      </div>
    )}

    {!contentUnlocked && (
      <LockedBlock>Answer the start check above to unlock the explanation, examples and practice for this unit.</LockedBlock>
    )}

    {contentUnlocked && section.key_points?.length > 0 && (
      <div className="mt-5">
        <h3 className="font-heading font-semibold text-ink">Key ideas</h3>
        <div className="mt-3"><BulletList items={section.key_points} /></div>
      </div>
    )}

    {contentUnlocked && section.visual_blocks?.length > 0 && (
      <div className="mt-5">
        <h3 className="font-heading font-semibold text-ink">Visual guide</h3>
        <div className="grid md:grid-cols-2 gap-4 mt-3">
          {section.visual_blocks.map((block, i) => (
            <LessonVisual key={`${block.type}-${block.variant}-${i}`} block={block} />
          ))}
        </div>
      </div>
    )}

    {contentUnlocked && section.formulas?.length > 0 && (
      <div className="mt-5 rounded-xl bg-ink text-white p-5 space-y-3">
        <h3 className="font-heading font-semibold">Formulas to know</h3>
        {section.formulas.map((formula, i) => (
          <div key={`${formula.name}-${i}`} className="text-sm">
            <div className="font-semibold text-warning">{formula.name}</div>
            <div className="mt-1"><MathText text={formula.expression} /></div>
            {formula.meaning && <div className="text-white/75 mt-1"><MathText text={formula.meaning} /></div>}
          </div>
        ))}
      </div>
    )}

    {contentUnlocked && section.examples?.length > 0 && (
      <div className="mt-5 space-y-4">
        <h3 className="font-heading font-semibold text-ink">Solved examples</h3>
        {section.examples.map((example, i) => (
          <WorkedExamplePanel key={`${example.title}-${i}`} example={example} index={i} />
        ))}
      </div>
    )}

    {contentUnlocked && section.practice?.length > 0 && (
      <div className="mt-5 grid md:grid-cols-2 gap-4">
        {section.practice.map((item, i) => (
          <InteractivePracticePanel key={`${item.question || item.problem}-${i}`} item={item} index={i} sectionKey={`${sectionKey}:practice`} label="Practice" />
        ))}
      </div>
    )}

    {contentUnlocked && section.module_quiz?.length > 0 && (
      <div className="mt-5 rounded-xl border border-edge bg-surface p-5">
        <h3 className="font-heading font-semibold text-ink">Module mastery check</h3>
        <p className="text-sm text-muted2 mt-1">Answer these to unlock the next section. If you miss two or more, review the examples above before continuing.</p>
        <div className="grid md:grid-cols-2 gap-3 mt-3">
          {section.module_quiz.map((item, i) => (
            <InteractivePracticePanel key={`${item.question}-${i}`} item={item} index={i} sectionKey={`${sectionKey}:quiz`} label="Mastery check" onAnswered={refresh} />
          ))}
        </div>
        {quizComplete && <div className="mt-4 rounded-lg bg-success/10 text-success px-4 py-2 text-sm font-medium">Section unlocked. You can move to the next unit.</div>}
      </div>
    )}

    {contentUnlocked && section.practice_ladder?.length > 0 && (
      <div className="mt-5 space-y-4">
        <h3 className="font-heading font-semibold text-ink">Challenge ladder</h3>
        {section.practice_ladder.map((group, i) => (
          <div key={`${group.level}-${i}`} className="rounded-xl border border-edge bg-sand/40 p-4">
            <div className="font-heading font-semibold text-ink">{group.level}</div>
            {group.description && <p className="text-sm text-muted2 mt-1"><MathText text={group.description} /></p>}
            <div className="grid md:grid-cols-2 gap-3 mt-3">
              {(group.items || []).map((item, idx) => (
                <InteractivePracticePanel key={`${item.question}-${idx}`} item={item} index={idx} sectionKey={`${sectionKey}:ladder:${i}`} label={group.level || "Challenge"} />
              ))}
            </div>
          </div>
        ))}
      </div>
    )}

    {contentUnlocked && section.examiner_notes?.length > 0 && (
      <div className="mt-5 rounded-xl border border-terracotta/30 bg-terracotta/5 p-5">
        <h3 className="font-heading font-semibold text-ink">Examiner notes</h3>
        <div className="mt-3"><BulletList items={section.examiner_notes} /></div>
      </div>
    )}

    {contentUnlocked && section.applications?.length > 0 && (
      <div className="mt-5">
        <h3 className="font-heading font-semibold text-ink">Applications</h3>
        <div className="grid md:grid-cols-2 gap-3 mt-3">
          {section.applications.map((app, i) => (
            <div key={`${app.title}-${i}`} className="rounded-xl border border-edge bg-sand/40 p-4">
              <div className="font-heading font-semibold text-ink">{app.title}</div>
              <p className="text-sm text-muted2 mt-1"><MathText text={app.body} /></p>
            </div>
          ))}
        </div>
      </div>
    )}
  </section>
  );
};

const Lessons = () => {
  const { subtopicId, sectionSlug: activeSectionSlug } = useParams();
  const [topics, setTopics] = useState(null);
  const [lesson, setLesson] = useState(null);
  const [masteryEngine, setMasteryEngine] = useState(null);
  const [activeComplete, setActiveComplete] = useState(true);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    http.get("/topics").then((r) => setTopics(r.data.topics || []));
  }, []);

  useEffect(() => {
    if (!subtopicId) { setLesson(null); setLoading(false); return; }
    setLoading(true);
    http.get(`/lessons/${subtopicId}`)
      .then((r) => setLesson(r.data))
      .catch(() => setLesson(null))
      .finally(() => setLoading(false));
    if (subtopicId === "set-operations") {
      http.get("/sets/mastery")
        .then((r) => setMasteryEngine({ data: r.data, courseName: "Sets", testId: "sets-learning-engine" }))
        .catch(() => setMasteryEngine(null));
    } else if (subtopicId === "propositional-logic" || subtopicId === "truth-tables") {
      http.get("/logic/mastery")
        .then((r) => setMasteryEngine({ data: r.data, courseName: "Logic", testId: "logic-learning-engine" }))
        .catch(() => setMasteryEngine(null));
    } else {
      setMasteryEngine(null);
    }
  }, [subtopicId]);

  const activeSectionForProgress = activeSectionSlug
    ? (lesson?.lesson_sections || []).find((section) => sectionSlug(section.title) === activeSectionSlug)
    : null;

  useEffect(() => {
    if (!activeSectionSlug || !activeSectionForProgress) {
      setActiveComplete(true);
      return;
    }
    const quiz = activeSectionForProgress.module_quiz || [];
    if (!quiz.length) {
      setActiveComplete(true);
      return;
    }
    const key = `${subtopicId}:${activeSectionSlug}:quiz`;
    const done = quiz.every((item, i) => {
      try {
        return JSON.parse(localStorage.getItem(progressKey(key, item, i)) || "null")?.submitted;
      } catch {
        return false;
      }
    });
    setActiveComplete(done);
  }, [activeSectionSlug, activeSectionForProgress, subtopicId]);

  if (!subtopicId) {
    const availableTopics = (topics || []).filter((t) => t.status === "available");
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid="lessons-index">
        <span className="overline">All lessons</span>
        <h1 className="font-heading text-4xl font-bold text-ink mt-2">Choose a subtopic</h1>
        <p className="text-muted2 mt-2">Each subtopic includes notes and worked examples. Rich lessons can also include visuals, applications and quick checks.</p>
        <div className="space-y-10 mt-8">
          {availableTopics.map((t) => (
            <div key={t.id}>
              <h2 className="font-heading text-2xl font-semibold text-ink">{t.name}</h2>
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
                {(t.subtopics || []).map((s) => (
                  <Link key={s.id} to={`/lessons/${s.id}`} className="card-surface p-6 block group" data-testid={`lesson-card-${s.id}`}>
                    <div className="flex items-center justify-between">
                      <div className="font-heading text-xl font-semibold text-ink group-hover:text-terracotta">{s.name}</div>
                      <ChevronRight className="text-muted2 group-hover:text-terracotta" size={18} />
                    </div>
                    <div className="text-sm text-muted2 mt-2">Open lesson and worked examples</div>
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (loading) return <div className="p-10 text-muted2" data-testid="lesson-loading">Loading lesson...</div>;
  if (!lesson) return <div className="p-10 text-muted2" data-testid="lesson-not-found">Lesson not found.</div>;

  const topicName = (topics || []).find((t) => t.id === lesson.topic)?.name || lesson.topic || "Lesson";
  const activeSection = activeSectionForProgress;
  const coreSections = (lesson.lesson_sections || []).filter((section) => section.track !== "challenge");
  const challengeSections = (lesson.lesson_sections || []).filter((section) => section.track === "challenge");
  const hasRichContent = [
    "objectives", "prerequisites", "visual_blocks", "lesson_sections", "worked_examples",
    "word_problems", "applications", "common_mistakes", "quick_checks",
  ].some((key) => lesson[key]?.length);

  if (activeSectionSlug) {
    if (!activeSection) {
      return (
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-12 py-10">
          <Link to={`/lessons/${subtopicId}`} className="inline-flex items-center gap-2 text-sm text-muted2 hover:text-terracotta">
            <ArrowLeft size={16} /> Back to {lesson.title}
          </Link>
          <div className="card-surface p-7 mt-8 text-muted2">Lesson section not found.</div>
        </div>
      );
    }

    const activeIndex = (lesson.lesson_sections || []).findIndex((section) => sectionSlug(section.title) === activeSectionSlug);
    const previous = lesson.lesson_sections?.[activeIndex - 1];
    const next = lesson.lesson_sections?.[activeIndex + 1];

    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid="lesson-section-detail">
        <Link to={`/lessons/${subtopicId}`} className="inline-flex items-center gap-2 text-sm text-muted2 hover:text-terracotta">
          <ArrowLeft size={16} /> Back to {lesson.title} sections
        </Link>
        <span className="overline mt-6 block">{topicName} - {lesson.title}</span>
        <h1 className="font-heading text-4xl font-bold text-ink mt-2">{activeSection.title}</h1>
        {activeSection.intro && <p className="text-lg text-muted2 mt-3 leading-relaxed"><MathText text={activeSection.intro} /></p>}

        <div className="mt-8">
          <LessonSection
            section={activeSection}
            index={activeIndex}
            sectionKey={`${subtopicId}:${activeSectionSlug}`}
            onCompletionChange={setActiveComplete}
          />
        </div>

        <div className="mt-8 flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between">
          {previous ? (
            <Link className="btn-secondary inline-flex items-center gap-2 justify-center" to={`/lessons/${subtopicId}/sections/${sectionSlug(previous.title)}`}>
              <ArrowLeft size={16} /> Previous
            </Link>
          ) : <div />}
          {next ? (
            activeComplete ? (
            <Link className="btn-primary inline-flex items-center gap-2 justify-center" to={`/lessons/${subtopicId}/sections/${sectionSlug(next.title)}`}>
              Next section <ChevronRight size={16} />
            </Link>
            ) : (
              <button type="button" disabled className="btn-primary inline-flex items-center gap-2 justify-center opacity-50 cursor-not-allowed">
                Complete mastery check to unlock <ChevronRight size={16} />
              </button>
            )
          ) : (
            <Link className="btn-primary inline-flex items-center gap-2 justify-center" to={`/past-questions?subtopic=${lesson.subtopic_id}`}>
              Practise questions <ChevronRight size={16} />
            </Link>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid="lesson-detail">
      <Link to="/lessons" className="inline-flex items-center gap-2 text-sm text-muted2 hover:text-terracotta" data-testid="lesson-back">
        <ArrowLeft size={16} /> All subtopics
      </Link>
      <span className="overline mt-6 block">{topicName} - Lesson</span>
      <h1 className="font-heading text-4xl font-bold text-ink mt-2">{lesson.title}</h1>
      <p className="text-lg text-muted2 mt-3 leading-relaxed">
        <MathText text={lesson.summary} />
      </p>

      {hasRichContent && (
        <div className="mt-8 grid md:grid-cols-2 gap-4">
          {lesson.objectives?.length > 0 && (
            <RichCard title="What you will learn" icon={ListChecks}>
              <BulletList items={lesson.objectives} />
            </RichCard>
          )}
          {lesson.prerequisites?.length > 0 && (
            <RichCard title="Before you start" icon={Lightbulb}>
              <BulletList items={lesson.prerequisites} />
            </RichCard>
          )}
        </div>
      )}

      {(subtopicId === "set-operations" || subtopicId === "propositional-logic" || subtopicId === "truth-tables") && (
        <div className="mt-8">
          <SetsLearningEngine mastery={masteryEngine?.data} courseName={masteryEngine?.courseName || "Course"} testId={masteryEngine?.testId || "learning-engine"} />
        </div>
      )}

      {lesson.visual_blocks?.length > 0 && (
        <div className="mt-10">
          <h2 className="font-heading text-2xl font-semibold text-ink">Visual explanation</h2>
          <div className="grid md:grid-cols-2 gap-4 mt-4">
            {lesson.visual_blocks.map((block, i) => (
              <LessonVisual key={`${block.type}-${block.variant}-${i}`} block={block} />
            ))}
          </div>
        </div>
      )}

      {lesson.lesson_sections?.length > 0 && (
        <div id="guided-sections" className="mt-10 space-y-6">
          <div>
            <span className="overline">Guided sections</span>
            <h2 className="font-heading text-2xl font-semibold text-ink mt-2">Learn this topic step by step</h2>
            <p className="text-muted2 mt-2">Open one unit at a time. Each section has its own explanations, diagrams, examples and practice.</p>
          </div>
          <div className="grid gap-4">
            {coreSections.map((section) => (
              <SectionCard
                key={section.title}
                section={section}
                index={(lesson.lesson_sections || []).findIndex((item) => item.title === section.title)}
                subtopicId={subtopicId}
              />
            ))}
          </div>
          {challengeSections.length > 0 && (
            <div className="mt-10">
              <span className="overline">Optional track</span>
              <h2 className="font-heading text-2xl font-semibold text-ink mt-2">WAEC+ Challenge Track</h2>
              <p className="text-muted2 mt-2">For highly motivated students: proof, logic, combinatorial counting and examiner-level reasoning beyond ordinary textbook drills.</p>
              <div className="grid gap-4 mt-4">
                {challengeSections.map((section) => (
                  <SectionCard
                    key={section.title}
                    section={section}
                    index={(lesson.lesson_sections || []).findIndex((item) => item.title === section.title)}
                    subtopicId={subtopicId}
                    challenge
                  />
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {lesson.lesson_sections?.length ? null : <div className="mt-10 space-y-8">
        {lesson.notes.map((n, i) => (
          <div key={i} className="card-surface p-7" data-testid={`lesson-note-${i}`}>
            <div className="flex items-baseline gap-3">
              <span className="font-heading text-terracotta font-bold text-2xl">{String(i + 1).padStart(2, "0")}</span>
              <h3 className="font-heading text-xl font-semibold text-ink">{n.heading}</h3>
            </div>
            <div className="mt-3 text-ink leading-relaxed text-base">
              <MathText text={n.body} />
            </div>
          </div>
        ))}
      </div>}

      {!lesson.lesson_sections?.length && lesson.worked_examples?.length > 0 && (
        <div className="mt-10">
          <h2 className="font-heading text-2xl font-semibold text-ink">Worked examples</h2>
          <div className="space-y-4 mt-4">
            {lesson.worked_examples.map((ex, i) => (
              <div key={`${ex.title}-${i}`} className="card-surface p-6">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="tag">{ex.level || "example"}</span>
                  <h3 className="font-heading text-lg font-semibold text-ink">{ex.title}</h3>
                </div>
                {ex.problem && <p className="text-ink mt-3"><MathText text={ex.problem} /></p>}
                {ex.steps?.length > 0 && (
                  <ol className="mt-4 space-y-2">
                    {ex.steps.map((step, idx) => (
                      <li key={`${step}-${idx}`} className="flex gap-3 text-sm text-ink">
                        <span className="font-heading text-terracotta font-bold">{idx + 1}</span>
                        <span><MathText text={step} /></span>
                      </li>
                    ))}
                  </ol>
                )}
                {ex.answer && <div className="mt-4 rounded-lg bg-success/10 text-success px-4 py-2 text-sm font-medium"><MathText text={ex.answer} /></div>}
              </div>
            ))}
          </div>
        </div>
      )}

      {!lesson.lesson_sections?.length && lesson.word_problems?.length > 0 && (
        <div className="mt-10">
          <h2 className="font-heading text-2xl font-semibold text-ink">Word problems</h2>
          <div className="grid gap-4 mt-4">
            {lesson.word_problems.map((problem, i) => (
              <div key={`${problem.title}-${i}`} className="card-surface p-6">
                <span className="tag">{problem.level || "practice"}</span>
                <h3 className="font-heading text-lg font-semibold text-ink mt-3">{problem.title}</h3>
                <p className="text-sm text-ink mt-2"><MathText text={problem.problem} /></p>
                {problem.solution?.length > 0 && <div className="mt-4"><BulletList items={problem.solution} /></div>}
              </div>
            ))}
          </div>
        </div>
      )}

      {(lesson.applications?.length > 0 || lesson.common_mistakes?.length > 0 || lesson.quick_checks?.length > 0) && (
        <div className="mt-10 grid lg:grid-cols-3 gap-4">
          {lesson.applications?.length > 0 && (
            <RichCard title="Applications" icon={Lightbulb}>
              <div className="space-y-3">
                {lesson.applications.map((app, i) => (
                  <div key={`${app.title}-${i}`}>
                    <div className="font-heading font-semibold text-ink">{app.title}</div>
                    <p className="text-sm text-muted2 mt-1"><MathText text={app.body} /></p>
                  </div>
                ))}
              </div>
            </RichCard>
          )}
          {lesson.common_mistakes?.length > 0 && (
            <RichCard title="Common mistakes" icon={TriangleAlert}>
              <BulletList items={lesson.common_mistakes} />
            </RichCard>
          )}
          {lesson.quick_checks?.length > 0 && (
            <RichCard title="Quick checks" icon={ListChecks}>
              <div className="space-y-3">
                {lesson.quick_checks.map((check, i) => (
                  <div key={`${check.question}-${i}`} className="text-sm">
                    <div className="font-medium text-ink"><MathText text={check.question} /></div>
                    {check.answer && <div className="text-muted2 mt-1">Answer: <MathText text={check.answer} /></div>}
                  </div>
                ))}
              </div>
            </RichCard>
          )}
        </div>
      )}

      <div className="mt-10 card-surface p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="font-heading text-lg font-semibold text-ink">Ready to practise?</div>
          <div className="text-sm text-muted2">Attempt WAEC past questions on this subtopic.</div>
        </div>
        <Link
          to={`/past-questions?subtopic=${lesson.subtopic_id}`}
          className="btn-primary inline-flex items-center gap-2"
          data-testid="lesson-cta-practice"
        >
          Practice {lesson.title} <ChevronRight size={18} />
        </Link>
      </div>
    </div>
  );
};

export default Lessons;
