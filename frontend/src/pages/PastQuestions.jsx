import React, { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import http from "@/lib/api";
import MathText from "@/components/MathText";
import { toast } from "sonner";
import { Filter, CheckCircle2, XCircle, Sparkles, Wand2, X } from "lucide-react";

const DIFFICULTIES = [
  { id: "", name: "All difficulties" },
  { id: "easy", name: "Easy" },
  { id: "medium", name: "Medium" },
  { id: "hard", name: "Hard" },
];

const PastQuestions = () => {
  const [params, setParams] = useSearchParams();
  const [topics, setTopics] = useState([]);
  const [years, setYears] = useState([]);
  const [questions, setQuestions] = useState([]);
  const [active, setActive] = useState(null); // QuestionDetail
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [selectedOption, setSelectedOption] = useState(null);
  const [result, setResult] = useState(null); // { correct, correct_answer, solution_steps }
  const [similar, setSimilar] = useState(null); // { loading, items }

  const topic = params.get("topic") || "";
  const subtopic = params.get("subtopic") || "";
  const year = params.get("year") || "";
  const difficulty = params.get("difficulty") || "";

  useEffect(() => {
    Promise.all([http.get("/topics"), http.get("/years")])
      .then(([t, y]) => {
        setTopics((t.data.topics || []).filter((x) => x.status === "available"));
        setYears(y.data);
      });
  }, []);

  useEffect(() => {
    setLoading(true);
    const q = {};
    if (topic) q.topic = topic;
    if (subtopic) q.subtopic = subtopic;
    if (year) q.year = year;
    if (difficulty) q.difficulty = difficulty;
    http.get("/questions", { params: q })
      .then((r) => setQuestions(r.data))
      .finally(() => setLoading(false));
  }, [topic, subtopic, year, difficulty]);

  const updateFilters = (updates) => {
    const next = new URLSearchParams(params);
    for (const [key, val] of Object.entries(updates)) {
      if (val) next.set(key, val); else next.delete(key);
    }
    setParams(next, { replace: true });
  };

  const updateFilter = (key, val) => updateFilters({ [key]: val });

  const openQuestion = async (id) => {
    setSelectedOption(null); setResult(null); setSimilar(null);
    const { data } = await http.get(`/questions/${id}`);
    setActive(data);
  };

  const generateSimilar = async () => {
    if (!active) return;
    setSimilar({ loading: true, items: [] });
    try {
      const { data } = await http.post(`/questions/${active.id}/similar`, { n: 3 });
      setSimilar({ loading: false, items: data.items });
    } catch (e) {
      setSimilar(null);
      toast.error(e?.response?.data?.detail || "Could not generate similar questions");
    }
  };

  const submit = async () => {
    if (!selectedOption) { toast.error("Please select an option."); return; }
    setSubmitting(true);
    try {
      const { data } = await http.post("/attempts", { question_id: active.id, selected: selectedOption });
      setResult(data);
      if (data.correct) toast.success("Correct! Well done.");
      else toast.error("Not quite — see the worked solution below.");
    } catch (e) {
      toast.error("Could not submit attempt.");
    } finally {
      setSubmitting(false);
    }
  };

  const subtopicLabel = useMemo(() => {
    if (!subtopic) return "All subtopics";
    for (const t of topics) {
      const s = (t.subtopics || []).find((x) => x.id === subtopic);
      if (s) return s.name;
    }
    return subtopic;
  }, [subtopic, topics]);

  const availableSubtopics = useMemo(() => {
    if (!topic) return topics.flatMap((t) => t.subtopics || []);
    return topics.find((t) => t.id === topic)?.subtopics || [];
  }, [topic, topics]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid="past-questions-page">
      <span className="overline">WAEC past questions</span>
      <h1 className="font-heading text-4xl font-bold text-ink mt-2">Solved past questions browser</h1>
      <p className="text-muted2 mt-2">Filter, attempt, and review fully worked solutions.</p>

      {/* FILTERS */}
      <div className="mt-6 card-surface p-5 flex flex-col sm:flex-row gap-4 items-stretch sm:items-center">
        <div className="flex items-center gap-2 text-sm text-muted2 sm:mr-2">
          <Filter size={16} /> Filters
        </div>
        <select
          value={topic} onChange={(e) => updateFilters({ topic: e.target.value, subtopic: "" })}
          data-testid="filter-topic-select"
          className="px-3 py-2 rounded-lg border border-edge bg-surface text-sm focus:outline-none focus:ring-2 focus:ring-terracotta/30"
        >
          <option value="">All topics</option>
          {topics.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
        </select>
        <select
          value={subtopic} onChange={(e) => updateFilter("subtopic", e.target.value)}
          data-testid="filter-subtopic-select"
          className="px-3 py-2 rounded-lg border border-edge bg-surface text-sm focus:outline-none focus:ring-2 focus:ring-terracotta/30"
        >
          <option value="">All subtopics</option>
          {availableSubtopics.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
        </select>
        <select
          value={year} onChange={(e) => updateFilter("year", e.target.value)}
          data-testid="filter-year-select"
          className="px-3 py-2 rounded-lg border border-edge bg-surface text-sm focus:outline-none focus:ring-2 focus:ring-terracotta/30"
        >
          <option value="">All years</option>
          {years.map((y) => <option key={y} value={y}>{y}</option>)}
        </select>
        <select
          value={difficulty} onChange={(e) => updateFilter("difficulty", e.target.value)}
          data-testid="filter-difficulty-select"
          className="px-3 py-2 rounded-lg border border-edge bg-surface text-sm focus:outline-none focus:ring-2 focus:ring-terracotta/30"
        >
          {DIFFICULTIES.map((d) => <option key={d.id} value={d.id}>{d.name}</option>)}
        </select>
        <div className="text-sm text-muted2 sm:ml-auto" data-testid="results-count">
          {loading ? "Loading…" : `${questions.length} question${questions.length === 1 ? "" : "s"}`}
        </div>
      </div>

      <div className="grid lg:grid-cols-12 gap-6 mt-8">
        {/* LIST */}
        <div className="lg:col-span-5 space-y-3" data-testid="questions-list">
          {questions.length === 0 && !loading && (
            <div className="card-surface p-6 text-muted2">No questions match your filters.</div>
          )}
          {questions.map((q) => (
            <button
              key={q.id}
              onClick={() => openQuestion(q.id)}
              data-testid={`question-item-${q.id}`}
              className={`w-full text-left card-surface p-5 hover:!border-terracotta/50 ${active?.id === q.id ? "!border-terracotta" : ""}`}
            >
              <div className="flex items-center gap-2 flex-wrap mb-2">
                <span className="tag">{q.subtopic_name}</span>
                <span className="tag">{q.year}</span>
                <span className="tag !text-terracotta">{q.difficulty}</span>
              </div>
              <div className="text-ink"><MathText text={q.question} /></div>
            </button>
          ))}
        </div>

        {/* DETAIL */}
        <div className="lg:col-span-7 lg:sticky lg:top-20 self-start">
          {!active ? (
            <div className="card-surface p-10 text-center text-muted2" data-testid="question-empty-state">
              <Sparkles className="mx-auto text-terracotta" />
              <p className="mt-3">Select a question on the left to see options and the worked solution.</p>
            </div>
          ) : (
            <div className="card-surface p-7" data-testid="question-detail">
              <div className="flex items-center gap-2 flex-wrap">
                <span className="tag">{active.subtopic_name}</span>
                <span className="tag">WAEC {active.year}</span>
                <span className="tag !text-terracotta">{active.difficulty}</span>
              </div>
              <h2 className="font-heading text-2xl font-semibold text-ink mt-4 leading-snug">
                <MathText text={active.question} />
              </h2>

              <div className="mt-5 space-y-2" data-testid="answer-options">
                {active.options.map((opt, idx) => {
                  const letter = ["A", "B", "C", "D", "E"][idx];
                  const chosen = selectedOption === opt;
                  const showCorrect = result && opt === result.correct_answer;
                  const showWrong = result && chosen && !result.correct;
                  return (
                    <button
                      key={idx}
                      disabled={!!result}
                      onClick={() => setSelectedOption(opt)}
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
                  <button
                    onClick={() => openQuestion(active.id)}
                    className="btn-ghost mt-5 text-sm"
                    data-testid="try-again-btn"
                  >
                    Try this question again
                  </button>
                  <button
                    onClick={generateSimilar}
                    className="btn-secondary mt-5 ml-2 text-sm inline-flex items-center gap-2"
                    data-testid="generate-similar-btn"
                    disabled={similar?.loading}
                  >
                    <Wand2 size={14} /> {similar?.loading ? "Generating…" : "Generate similar"}
                  </button>
                </div>
              )}

              {similar && !similar.loading && similar.items?.length > 0 && (
                <div className="mt-6 border-t border-edge pt-5" data-testid="similar-block">
                  <div className="flex items-center justify-between">
                    <h3 className="font-heading text-lg font-semibold text-ink">AI-generated practice (similar)</h3>
                    <button onClick={() => setSimilar(null)} className="p-1 rounded hover:bg-sand" aria-label="close"><X size={16} /></button>
                  </div>
                  <div className="space-y-4 mt-3">
                    {similar.items.map((it, i) => (
                      <details key={i} className="card-surface p-4" data-testid={`similar-item-${i}`}>
                        <summary className="cursor-pointer text-ink"><MathText text={it.question} /></summary>
                        <ol className="mt-3 space-y-1.5">
                          {(it.options || []).map((o, oi) => (
                            <li key={oi} className="text-sm text-ink flex gap-2">
                              <span className="font-mono text-xs bg-sand border border-edge px-2 rounded">{["A","B","C","D"][oi]}</span>
                              <span><MathText text={o} /></span>
                            </li>
                          ))}
                        </ol>
                        <div className="text-sm text-success mt-3">Answer: <MathText text={it.answer} /></div>
                        <div className="text-xs text-muted2 mt-2">Steps:</div>
                        <ol className="mt-1 space-y-1">
                          {(it.solution_steps || []).map((s, si) => (
                            <li key={si} className="text-sm text-ink"><span className="font-mono text-xs mr-2">{si + 1}</span><MathText text={s} /></li>
                          ))}
                        </ol>
                      </details>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PastQuestions;
