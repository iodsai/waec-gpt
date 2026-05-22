import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import http from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { BookOpen, Sparkles, FileText, TrendingUp, Target, Trophy, Compass } from "lucide-react";
import MathText from "@/components/MathText";

const Dashboard = () => {
  const { user } = useAuth();
  const [topicsData, setTopicsData] = useState([]);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([http.get("/topics"), http.get("/progress")])
      .then(([t, p]) => { setTopicsData(t.data.topics || []); setProgress(p.data); })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-10 text-muted2" data-testid="dashboard-loading">Loading dashboard…</div>;

  const acc = progress?.accuracy || 0;
  const total = progress?.total_attempts || 0;
  const correct = progress?.correct || 0;
  const availableTopics = topicsData.filter((t) => t.status === "available");
  const totalSubtopics = availableTopics.reduce((acc, t) => acc + (t.subtopics?.length || 0), 0);
  const coveredSubtopics = Object.keys(progress?.by_subtopic || {}).length;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid="dashboard-page">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <span className="overline">Welcome back</span>
          <h1 className="font-heading text-4xl sm:text-5xl font-bold text-ink mt-2 tracking-tight">
            Hello, {user?.name?.split(" ")[0] || "Scholar"}.
          </h1>
          <p className="text-muted2 mt-2">Pick a subtopic, attempt a past question, or ask the AI tutor.</p>
        </div>
        <div className="flex flex-wrap gap-3">
          <Link to="/tutor" className="btn-ghost inline-flex items-center gap-2" data-testid="dashboard-cta-tutor">
            <Sparkles size={18} /> Ask AI Tutor
          </Link>
          <Link to="/exams" className="btn-secondary inline-flex items-center gap-2" data-testid="dashboard-cta-exams">
            <Trophy size={18} /> Exam mode
          </Link>
          <Link to="/past-questions" className="btn-primary inline-flex items-center gap-2" data-testid="dashboard-cta-practice">
            <FileText size={18} /> Practice now
          </Link>
        </div>
      </div>

      {/* STATS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mt-10">
        <div className="card-surface p-6" data-testid="stat-accuracy">
          <div className="flex items-center justify-between">
            <span className="overline">Accuracy</span>
            <Target size={18} className="text-moss" />
          </div>
          <div className="font-heading text-5xl font-bold text-ink mt-3">{acc}%</div>
          <div className="text-xs text-muted2 mt-1">{correct} of {total} correct</div>
        </div>
        <div className="card-surface p-6" data-testid="stat-attempts">
          <div className="flex items-center justify-between">
            <span className="overline">Total attempts</span>
            <TrendingUp size={18} className="text-terracotta" />
          </div>
          <div className="font-heading text-5xl font-bold text-ink mt-3">{total}</div>
          <div className="text-xs text-muted2 mt-1">Keep going — daily practice wins WAEC.</div>
        </div>
        <div className="card-surface p-6" data-testid="stat-subtopics">
          <div className="flex items-center justify-between">
            <span className="overline">Subtopics covered</span>
            <BookOpen size={18} className="text-moss" />
          </div>
          <div className="font-heading text-5xl font-bold text-ink mt-3">
            {coveredSubtopics}<span className="text-muted2 text-2xl"> / {totalSubtopics}</span>
          </div>
          <div className="text-xs text-muted2 mt-1">Across {availableTopics.length} live topics.</div>
        </div>
      </div>

      {/* TOPIC GRID */}
      <div className="mt-12">
        <div className="flex items-end justify-between">
          <div>
            <h2 className="font-heading text-2xl font-semibold text-ink">Your topics</h2>
            <p className="text-muted2 text-sm mt-1">Open a topic to explore its subtopics, lessons, and past questions.</p>
          </div>
          <Link to="/topics" className="text-sm text-terracotta hover:underline inline-flex items-center gap-1" data-testid="dashboard-all-topics">
            <Compass size={14} /> All topics
          </Link>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-5">
          {availableTopics.map((t, i) => {
            const tstat = progress?.by_topic?.[t.id];
            return (
              <Link key={t.id} to={`/topics/${t.id}`} data-testid={`topic-card-${t.id}`}
                className="card-surface p-6 group block" style={{ animationDelay: `${i * 50}ms` }}>
                <div className="flex items-center justify-between">
                  <h3 className="font-heading text-xl font-semibold text-ink group-hover:text-terracotta">{t.name}</h3>
                  <span className="tag">{t.question_count} Q</span>
                </div>
                <p className="text-sm text-muted2 mt-1 line-clamp-2">{t.description}</p>
                <div className="mt-4 flex items-center justify-between text-xs">
                  {tstat ? (
                    <>
                      <span className="tag !text-success !bg-success/10">{tstat.accuracy}% accuracy</span>
                      <span className="text-muted2">{tstat.total} attempts</span>
                    </>
                  ) : (
                    <>
                      <span className="tag">New</span>
                      <span className="text-muted2">No attempts yet</span>
                    </>
                  )}
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      {/* RECENT */}
      {progress?.recent_attempts?.length > 0 && (
        <div className="mt-12">
          <h2 className="font-heading text-2xl font-semibold text-ink">Recent attempts</h2>
          <div className="mt-4 card-surface divide-y divide-edge">
            {progress.recent_attempts.map((r) => (
              <div key={r.id} className="px-5 py-3 flex items-center justify-between gap-3" data-testid={`recent-attempt-${r.id}`}>
                <div className="min-w-0 flex-1">
                  <div className="text-sm text-ink truncate">
                    <MathText text={r.question_text || "Question"} />
                  </div>
                  <div className="text-xs text-muted2 mt-0.5">
                    {r.subtopic_name} · selected: <MathText text={r.selected} />
                  </div>
                </div>
                <span className={`tag ${r.correct ? "!bg-success/10 !text-success" : "!bg-error/10 !text-error"}`}>
                  {r.correct ? "Correct" : "Wrong"}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
