import React, { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import http from "@/lib/api";
import { toast } from "sonner";
import MathText from "@/components/MathText";
import ObjectivePane from "@/components/pastq/ObjectivePane";
import TheoryPane from "@/components/pastq/TheoryPane";
import SimilarBlock from "@/components/pastq/SimilarBlock";
import { Filter, Sparkles } from "lucide-react";

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
  const [active, setActive] = useState(null);
  const [loading, setLoading] = useState(true);
  const [similar, setSimilar] = useState(null); // { loading, items }
  const [reloadKey, setReloadKey] = useState(0); // forces pane remount on "try again"

  const topic = params.get("topic") || "";
  const subtopic = params.get("subtopic") || "";
  const year = params.get("year") || "";
  const difficulty = params.get("difficulty") || "";

  useEffect(() => {
    Promise.all([http.get("/topics"), http.get("/years")]).then(([t, y]) => {
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
    setSimilar(null);
    const { data } = await http.get(`/questions/${id}`);
    setActive(data);
    setReloadKey((k) => k + 1);
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
                {q.question_type === "theory" && (
                  <span className="tag !bg-moss/10 !text-moss !border-moss/30">Theory</span>
                )}
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
                {active.question_type === "theory" && (
                  <span className="tag !bg-moss/10 !text-moss !border-moss/30">Theory</span>
                )}
              </div>
              <h2 className="font-heading text-2xl font-semibold text-ink mt-4 leading-snug">
                <MathText text={active.question} />
              </h2>

              {active.question_type === "theory" ? (
                <TheoryPane
                  key={reloadKey}
                  question={active}
                  onGenerateSimilar={generateSimilar}
                  similarLoading={!!similar?.loading}
                />
              ) : (
                <ObjectivePane
                  key={reloadKey}
                  question={active}
                  onTryAgain={() => openQuestion(active.id)}
                  onGenerateSimilar={generateSimilar}
                  similarLoading={!!similar?.loading}
                />
              )}

              {similar && !similar.loading && (
                <SimilarBlock items={similar.items} onClose={() => setSimilar(null)} />
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PastQuestions;
