import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import http from "@/lib/api";
import { ArrowLeft, ChevronRight, FileText, Sparkles } from "lucide-react";

const TopicDetail = () => {
  const { topicId } = useParams();
  const [topic, setTopic] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    http.get("/topics").then((r) => {
      setTopic((r.data.topics || []).find((t) => t.id === topicId));
    }).finally(() => setLoading(false));
  }, [topicId]);

  if (loading) return <div className="p-10 text-muted2">Loading…</div>;
  if (!topic) return <div className="p-10 text-muted2">Topic not found.</div>;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid={`topic-detail-${topicId}`}>
      <Link to="/topics" className="inline-flex items-center gap-2 text-sm text-muted2 hover:text-terracotta" data-testid="back-to-topics">
        <ArrowLeft size={16} /> All topics
      </Link>
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mt-4">
        <div>
          <span className="overline">Topic</span>
          <h1 className="font-heading text-4xl font-bold text-ink mt-2">{topic.name}</h1>
          <p className="text-muted2 mt-2 max-w-2xl">{topic.description}</p>
        </div>
        <div className="flex gap-2">
          <Link to={`/past-questions?topic=${topic.id}`} className="btn-ghost inline-flex items-center gap-2" data-testid="cta-questions">
            <FileText size={16} /> Past questions
          </Link>
          <Link to={`/exams?topic=${topic.id}`} className="btn-primary inline-flex items-center gap-2" data-testid="cta-exam">
            <Sparkles size={16} /> Start exam
          </Link>
        </div>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-8">
        {topic.subtopics?.map((s) => (
          <Link key={s.id} to={`/lessons/${s.id}`} className="card-surface p-5 block group" data-testid={`subtopic-${s.id}`}>
            <div className="flex items-center justify-between">
              <div className="font-heading text-lg font-semibold text-ink group-hover:text-terracotta">{s.name}</div>
              <ChevronRight className="text-muted2 group-hover:text-terracotta" size={18} />
            </div>
            <div className="text-sm text-muted2 mt-1">Notes & worked examples →</div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default TopicDetail;
