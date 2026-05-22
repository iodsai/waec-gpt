import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import http from "@/lib/api";
import MathText from "@/components/MathText";
import { Trophy, CheckCircle2, XCircle, ChevronLeft } from "lucide-react";

const ExamReport = () => {
  const { examId } = useParams();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    http.get(`/exams/${examId}`).then((r) => setReport(r.data)).finally(() => setLoading(false));
  }, [examId]);

  if (loading) return <div className="p-10 text-muted2">Loading report…</div>;
  if (!report) return <div className="p-10 text-muted2">Report not found.</div>;

  const mins = Math.floor(report.time_taken_seconds / 60);
  const secs = report.time_taken_seconds % 60;
  const scoreColor = report.score_percent >= 70 ? "text-success" :
                     report.score_percent >= 40 ? "text-warning" : "text-error";

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid="exam-report-page">
      <Link to="/exams" className="inline-flex items-center gap-2 text-sm text-muted2 hover:text-terracotta" data-testid="back-to-exams">
        <ChevronLeft size={16} /> All exams
      </Link>

      <div className="card-surface p-8 mt-4 relative overflow-hidden">
        <div className="flex items-center gap-3">
          <Trophy className="text-terracotta" size={28} />
          <span className="overline">Exam Report</span>
        </div>
        <h1 className="font-heading text-4xl font-bold text-ink mt-3">
          You scored <span className={scoreColor}>{report.score_percent}%</span>
        </h1>
        <p className="text-muted2 mt-1">
          {report.correct} / {report.total_questions} correct · {mins}m {secs}s · {report.mode === "mock" ? "Full Mock" : "Quick Drill"}
        </p>
      </div>

      {/* SUBTOPIC BREAKDOWN */}
      <div className="mt-8">
        <h2 className="font-heading text-2xl font-semibold text-ink">Performance by subtopic</h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3 mt-4">
          {Object.entries(report.by_subtopic).map(([k, v]) => (
            <div key={k} className="card-surface p-4" data-testid={`report-subtopic-${k}`}>
              <div className="text-sm font-medium text-ink">{v.name}</div>
              <div className="text-xs text-muted2">{v.correct}/{v.total}</div>
              <div className="mt-2 h-2 bg-sand rounded-full overflow-hidden">
                <div className="h-full bg-terracotta" style={{ width: `${v.accuracy}%` }} />
              </div>
              <div className="text-xs text-muted2 mt-1">{v.accuracy}%</div>
            </div>
          ))}
        </div>
      </div>

      {/* DETAIL */}
      <div className="mt-10">
        <h2 className="font-heading text-2xl font-semibold text-ink">Question-by-question review</h2>
        <div className="space-y-3 mt-4">
          {report.detail.map((d, i) => (
            <details key={d.question_id} className="card-surface p-5 group" data-testid={`report-q-${i + 1}`}>
              <summary className="cursor-pointer flex items-start gap-3 list-none">
                {d.correct ? <CheckCircle2 className="text-success mt-0.5 flex-shrink-0" size={18} /> : <XCircle className="text-error mt-0.5 flex-shrink-0" size={18} />}
                <div className="flex-1 min-w-0">
                  <div className="text-xs text-muted2">Q{i + 1} · {d.subtopic_name}</div>
                  <div className="text-ink mt-0.5 truncate"><MathText text={d.question} /></div>
                </div>
                <span className={`tag ${d.correct ? "!bg-success/10 !text-success" : "!bg-error/10 !text-error"}`}>
                  {d.correct ? "Correct" : (d.selected ? "Wrong" : "Skipped")}
                </span>
              </summary>
              <div className="mt-4 pt-4 border-t border-edge text-sm">
                <div className="text-muted2">You chose: <span className="text-ink"><MathText text={d.selected || "—"} /></span></div>
                <div className="text-muted2 mt-1">Correct answer: <span className="text-success font-medium"><MathText text={d.correct_answer} /></span></div>
                <div className="font-heading text-ink mt-3">Worked solution</div>
                <ol className="mt-2 space-y-1.5">
                  {d.solution_steps.map((s, j) => (
                    <li key={j} className="flex gap-2 text-ink">
                      <span className="font-mono text-xs bg-sand border border-edge px-2 rounded-md flex-shrink-0">{j + 1}</span>
                      <span><MathText text={s} /></span>
                    </li>
                  ))}
                </ol>
              </div>
            </details>
          ))}
        </div>
      </div>

      <div className="mt-10 flex justify-center gap-3">
        <Link to="/exams" className="btn-ghost" data-testid="report-new-exam">Take another exam</Link>
        <Link to="/dashboard" className="btn-primary" data-testid="report-dashboard">Back to dashboard</Link>
      </div>
    </div>
  );
};

export default ExamReport;
