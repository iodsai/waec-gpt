import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import http from "@/lib/api";
import MathText from "@/components/MathText";
import { ArrowLeft, ChevronRight } from "lucide-react";

const Lessons = () => {
  const { subtopicId } = useParams();
  const [topics, setTopics] = useState(null);
  const [lesson, setLesson] = useState(null);
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
  }, [subtopicId]);

  // INDEX VIEW
  if (!subtopicId) {
    const availableTopics = (topics || []).filter((t) => t.status === "available");
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid="lessons-index">
        <span className="overline">All lessons</span>
        <h1 className="font-heading text-4xl font-bold text-ink mt-2">Choose a subtopic</h1>
        <p className="text-muted2 mt-2">Each subtopic includes notes and at least one worked example.</p>
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
                    <div className="text-sm text-muted2 mt-2">Open notes & worked examples →</div>
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (loading) return <div className="p-10 text-muted2" data-testid="lesson-loading">Loading lesson…</div>;
  if (!lesson) return <div className="p-10 text-muted2" data-testid="lesson-not-found">Lesson not found.</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid="lesson-detail">
      <Link to="/lessons" className="inline-flex items-center gap-2 text-sm text-muted2 hover:text-terracotta" data-testid="lesson-back">
        <ArrowLeft size={16} /> All subtopics
      </Link>
      <span className="overline mt-6 block">Algebra · Lesson</span>
      <h1 className="font-heading text-4xl font-bold text-ink mt-2">{lesson.title}</h1>
      <p className="text-lg text-muted2 mt-3 leading-relaxed">
        <MathText text={lesson.summary} />
      </p>

      <div className="mt-10 space-y-8">
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
      </div>

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
