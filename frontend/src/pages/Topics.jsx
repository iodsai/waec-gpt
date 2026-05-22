import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import http from "@/lib/api";
import * as Icons from "lucide-react";
import { ChevronRight, Lock } from "lucide-react";

const Topics = () => {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    http.get("/topics").then((r) => setTopics(r.data.topics)).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-10 text-muted2">Loading topics…</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid="topics-page">
      <span className="overline">Syllabus</span>
      <h1 className="font-heading text-4xl font-bold text-ink mt-2">All WAEC Math topics</h1>
      <p className="text-muted2 mt-2">All 8 WAEC Further Maths syllabus topics now live — over 580 practice questions.</p>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5 mt-8">
        {topics.map((t) => {
          const Ico = Icons[t.icon] || Icons.BookOpen;
          const available = t.status === "available";
          const inner = (
            <div className={`card-surface p-6 h-full ${available ? "group" : "opacity-70"}`} data-testid={`topic-card-${t.id}`}>
              <div className="flex items-center justify-between">
                <div className={`w-12 h-12 rounded-xl grid place-items-center ${available ? "bg-terracotta/10 text-terracotta" : "bg-sand text-muted2"}`}>
                  <Ico size={22} />
                </div>
                {available ? (
                  <ChevronRight className="text-muted2 group-hover:text-terracotta" size={18} />
                ) : (
                  <span className="tag !text-muted2 flex items-center gap-1"><Lock size={12} /> Coming soon</span>
                )}
              </div>
              <h3 className="font-heading text-xl font-semibold text-ink mt-4">{t.name}</h3>
              <p className="text-sm text-muted2 mt-1">{t.description}</p>
              {available && (
                <div className="mt-4 flex flex-wrap gap-2">
                  <span className="tag">{t.question_count} questions</span>
                  <span className="tag">{t.subtopics?.length || 0} subtopics</span>
                </div>
              )}
            </div>
          );
          return available ? (
            <Link key={t.id} to={`/topics/${t.id}`}>{inner}</Link>
          ) : (
            <div key={t.id}>{inner}</div>
          );
        })}
      </div>
    </div>
  );
};

export default Topics;
