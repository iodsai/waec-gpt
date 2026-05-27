import React, { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import http from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { CheckCircle2, ExternalLink, ShieldAlert, XCircle } from "lucide-react";

const CHECK_LABELS = [
  ["has_lesson", "Lesson"],
  ["has_objectives", "Objectives"],
  ["has_prerequisites", "Prerequisites"],
  ["has_visuals", "Visuals"],
  ["has_rich_examples", "Examples"],
  ["has_word_problems", "Word problems"],
  ["has_applications", "Applications"],
  ["has_common_mistakes", "Mistakes"],
  ["has_quick_checks", "Quick checks"],
];

const CheckPill = ({ ok, label }) => (
  <span className={`tag ${ok ? "!bg-success/10 !text-success" : "!bg-error/10 !text-error"}`}>
    {ok ? <CheckCircle2 size={12} /> : <XCircle size={12} />} {label}
  </span>
);

const LessonAudit = () => {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    if (!user?.is_admin) {
      setLoading(false);
      return;
    }
    http.get("/admin/lesson-audit")
      .then((r) => setData(r.data))
      .finally(() => setLoading(false));
  }, [user]);

  const items = useMemo(() => {
    const rows = data?.items || [];
    if (filter === "all") return rows;
    return rows.filter((row) => !row.checks?.[filter]);
  }, [data, filter]);

  if (!user?.is_admin) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-20 text-center">
        <ShieldAlert className="mx-auto text-error" size={36} />
        <h1 className="font-heading text-3xl font-bold text-ink mt-3">Admin only</h1>
        <p className="text-muted2 mt-2">Use admin credentials to review lesson readiness.</p>
      </div>
    );
  }

  if (loading) return <div className="p-10 text-muted2">Loading lesson audit...</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid="lesson-audit-page">
      <span className="overline">Admin audit</span>
      <h1 className="font-heading text-4xl font-bold text-ink mt-2">Lesson completeness</h1>
      <p className="text-muted2 mt-2 max-w-3xl">
        Use this before rewriting lessons. A complete self-paced lesson should teach from zero, show visuals, solve examples, include word problems, connect to applications and check understanding.
      </p>

      <div className="grid sm:grid-cols-2 lg:grid-cols-5 gap-4 mt-8">
        <div className="card-surface p-5">
          <div className="overline">Syllabus items</div>
          <div className="font-heading text-4xl font-bold text-ink mt-2">{data?.summary?.total || 0}</div>
        </div>
        <div className="card-surface p-5">
          <div className="overline">Full standard</div>
          <div className="font-heading text-4xl font-bold text-success mt-2">{data?.summary?.full_standard || 0}</div>
        </div>
        <div className="card-surface p-5">
          <div className="overline">Need visuals</div>
          <div className="font-heading text-4xl font-bold text-terracotta mt-2">{data?.summary?.needs_visuals || 0}</div>
        </div>
        <div className="card-surface p-5">
          <div className="overline">Need word problems</div>
          <div className="font-heading text-4xl font-bold text-terracotta mt-2">{data?.summary?.needs_word_problems || 0}</div>
        </div>
        <div className="card-surface p-5">
          <div className="overline">Average readiness</div>
          <div className="font-heading text-4xl font-bold text-moss mt-2">{data?.summary?.average_readiness || 0}%</div>
        </div>
      </div>

      <div className="card-surface p-3 flex flex-wrap gap-2 mt-8">
        <button onClick={() => setFilter("all")} className={`px-3 py-2 rounded-lg text-sm font-heading font-semibold ${filter === "all" ? "bg-terracotta text-white" : "hover:bg-sand text-muted2"}`}>
          All
        </button>
        {CHECK_LABELS.map(([key, label]) => (
          <button key={key} onClick={() => setFilter(key)} className={`px-3 py-2 rounded-lg text-sm font-heading font-semibold ${filter === key ? "bg-terracotta text-white" : "hover:bg-sand text-muted2"}`}>
            Missing {label}
          </button>
        ))}
      </div>

      <div className="mt-6 space-y-4">
        {items.map((row) => (
          <div key={row.syllabus_id} className="card-surface p-5" data-testid={`audit-row-${row.syllabus_id}`}>
            <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-4">
              <div>
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="overline">{row.section}</span>
                  <span className={`tag ${row.readiness === 100 ? "!text-success !bg-success/10" : "!text-terracotta !bg-terracotta/10"}`}>
                    {row.readiness}% ready
                  </span>
                  <span className="tag">{row.standard}</span>
                </div>
                <h2 className="font-heading text-xl font-semibold text-ink mt-3">{row.title}</h2>
                <p className="text-sm text-muted2 mt-1">{row.topic_name} - {row.subtopic_name || "No subtopic mapped"}</p>
              </div>
              <div className="flex flex-wrap gap-2 shrink-0">
                {row.lesson_path && (
                  <Link to={row.lesson_path} className="btn-ghost !px-3 !py-2 text-sm inline-flex items-center gap-1">
                    Open lesson <ExternalLink size={13} />
                  </Link>
                )}
                {row.practice_path && (
                  <Link to={row.practice_path} className="btn-ghost !px-3 !py-2 text-sm">
                    Practice
                  </Link>
                )}
              </div>
            </div>
            <div className="mt-4 flex flex-wrap gap-2">
              {CHECK_LABELS.map(([key, label]) => (
                <CheckPill key={key} ok={row.checks?.[key]} label={label} />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LessonAudit;
