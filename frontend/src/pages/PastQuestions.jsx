import React, { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import http from "@/lib/api";
import MathText from "@/components/MathText";
import { toast } from "sonner";
import { Filter, CheckCircle2, XCircle, Sparkles } from "lucide-react";

const DIFFICULTIES = [
  { id: "", name: "All difficulties" },
  { id: "easy", name: "Easy" },
  { id: "medium", name: "Medium" },
  { id: "hard", name: "Hard" },
];

const PastQuestions = () => {
  const [params, setParams] = useSearchParams();
  const [topics, setTopics] = useState(null);
  const [years, setYears] = useState([]);
  const [questions, setQuestions] = useState([]);
  const [active, setActive] = useState(null); // QuestionDetail
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [selectedOption, setSelectedOption] = useState(null);
  const [result, setResult] = useState(null); // { correct, correct_answer, solution_steps }

  const subtopic = params.get("subtopic") || "";
  const year = params.get("year") || "";
  const difficulty = params.get("difficulty") || "";

  useEffect(() => {
    Promise.all([http.get("/topics"), http.get("/years")])
      .then(([t, y]) => { setTopics(t.data); setYears(y.data); });
  }, []);

  useEffect(() => {
    setLoading(true);
    const q = {};
    if (subtopic) q.subtopic = subtopic;
    if (year) q.year = year;
    if (difficulty) q.difficulty = difficulty;
    http.get("/questions", { params: q })
      .then((r) => setQuestions(r.data))
      .finally(() => setLoading(false));
  }, [subtopic, year, difficulty]);

  const updateFilter = (key, val) => {
    const next = new URLSearchParams(params);
    if (val) next.set(key, val); else next.delete(key);
    setParams(next, { replace: true });
  };

  const openQuestion = async (id) => {
    setSelectedOption(null); setResult(null);
    const { data } = await http.get(`/questions/${id}`);
    setActive(data);
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
    if (!subtopic || !topics) return "All subtopics";
    return topics.subtopics.find((s) => s.id === subtopic)?.name || "All subtopics";
  }, [subtopic, topics]);

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
          value={subtopic} onChange={(e) => updateFilter("subtopic", e.target.value)}
          data-testid="filter-subtopic-select"
          className="px-3 py-2 rounded-lg border border-edge bg-surface text-sm focus:outline-none focus:ring-2 focus:ring-terracotta/30"
        >
          <option value="">All subtopics</option>
          {topics?.subtopics?.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
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
