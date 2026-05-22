import React, { useEffect, useState, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";
import http from "@/lib/api";
import MathText from "@/components/MathText";
import { toast } from "sonner";
import { Timer, Send, ChevronLeft, ChevronRight, AlertTriangle } from "lucide-react";

const ExamRun = () => {
  const { examId } = useParams();
  const navigate = useNavigate();
  const [exam, setExam] = useState(null);
  const [idx, setIdx] = useState(0);
  const [answers, setAnswers] = useState({});
  const [remaining, setRemaining] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [confirmSubmit, setConfirmSubmit] = useState(false);
  const submittedRef = useRef(false);

  useEffect(() => {
    const cached = sessionStorage.getItem(`exam-${examId}`);
    if (!cached) { toast.error("Exam session not found"); navigate("/exams"); return; }
    const data = JSON.parse(cached);
    setExam(data);
    const elapsed = Math.floor((Date.now() - new Date(data.started_at).getTime()) / 1000);
    setRemaining(Math.max(0, data.duration_seconds - elapsed));
  }, [examId, navigate]);

  // submit handler defined first so the timer can use it
  const submit = async () => {
    if (submittedRef.current) return;
    submittedRef.current = true;
    setSubmitting(true);
    try {
      await http.post(`/exams/${examId}/submit`, { answers });
      sessionStorage.removeItem(`exam-${examId}`);
      navigate(`/exams/${examId}/report`);
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Failed to submit");
      submittedRef.current = false;
    } finally {
      setSubmitting(false);
    }
  };

  // countdown
  useEffect(() => {
    if (!exam) return;
    const t = setInterval(() => {
      setRemaining((s) => {
        if (s <= 1) {
          clearInterval(t);
          toast.warning("Time's up! Submitting...");
          submit();
          return 0;
        }
        return s - 1;
      });
    }, 1000);
    return () => clearInterval(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [exam]);

  if (!exam) return <div className="p-10 text-muted2">Loading exam…</div>;
  const q = exam.questions[idx];
  const total = exam.questions.length;
  const mm = String(Math.floor(remaining / 60)).padStart(2, "0");
  const ss = String(remaining % 60).padStart(2, "0");
  const answeredCount = Object.keys(answers).length;

  const setAns = (val) => setAnswers((a) => ({ ...a, [q.id]: val }));

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-12 py-6" data-testid="exam-run-page">
      {/* Sticky header */}
      <div className="sticky top-16 z-30 bg-paper/95 backdrop-blur border-b border-edge -mx-4 px-4 py-3 mb-6 flex items-center justify-between gap-4">
        <div>
          <div className="text-xs text-muted2">{exam.mode === "mock" ? "Full Mock" : "Quick Drill"} · Q {idx + 1} / {total}</div>
          <div className="text-sm text-ink">Answered {answeredCount} / {total}</div>
        </div>
        <div className={`flex items-center gap-2 font-mono text-2xl font-bold ${remaining < 60 ? "text-error" : "text-ink"}`} data-testid="exam-timer">
          <Timer size={20} /> {mm}:{ss}
        </div>
        <button onClick={() => setConfirmSubmit(true)} className="btn-primary inline-flex items-center gap-2" data-testid="open-submit-btn">
          <Send size={16} /> Submit
        </button>
      </div>

      <div className="card-surface p-7" data-testid="exam-current-question">
        <div className="flex items-center gap-2 flex-wrap mb-3">
          <span className="tag">{q.subtopic_name}</span>
          <span className="tag">{q.topic_name}</span>
        </div>
        <h2 className="font-heading text-2xl font-semibold text-ink leading-snug">
          <MathText text={q.question} />
        </h2>
        <div className="mt-5 space-y-2">
          {q.options.map((opt, i) => {
            const letter = ["A", "B", "C", "D", "E"][i];
            const chosen = answers[q.id] === opt;
            return (
              <button key={i} onClick={() => setAns(opt)} data-testid={`exam-option-${letter}`}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl border text-left transition
                ${chosen ? "border-terracotta bg-terracotta/5" : "border-edge hover:border-terracotta/40"}`}>
                <span className="font-mono text-sm w-6 h-6 grid place-items-center rounded-md bg-sand text-ink">{letter}</span>
                <span className="text-ink"><MathText text={opt} /></span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Question navigation */}
      <div className="mt-5 flex items-center justify-between gap-3">
        <button onClick={() => setIdx((i) => Math.max(0, i - 1))} disabled={idx === 0} className="btn-ghost inline-flex items-center gap-2 disabled:opacity-50" data-testid="prev-q-btn">
          <ChevronLeft size={16} /> Previous
        </button>
        <div className="flex flex-wrap gap-1 justify-center">
          {exam.questions.map((qq, i) => (
            <button key={qq.id} onClick={() => setIdx(i)} data-testid={`q-nav-${i + 1}`}
              className={`w-9 h-9 rounded-lg text-sm font-medium border transition
              ${i === idx ? "border-terracotta bg-terracotta text-white" :
                answers[qq.id] ? "border-success/30 bg-success/10 text-success" : "border-edge bg-surface text-muted2 hover:border-terracotta/40"}`}>
              {i + 1}
            </button>
          ))}
        </div>
        <button onClick={() => setIdx((i) => Math.min(total - 1, i + 1))} disabled={idx === total - 1} className="btn-ghost inline-flex items-center gap-2 disabled:opacity-50" data-testid="next-q-btn">
          Next <ChevronRight size={16} />
        </button>
      </div>

      {/* Submit confirm modal */}
      {confirmSubmit && (
        <div className="fixed inset-0 bg-black/40 grid place-items-center z-50 px-4" data-testid="submit-modal">
          <div className="bg-surface rounded-2xl border border-edge p-6 max-w-md w-full">
            <AlertTriangle className="text-warning" />
            <h3 className="font-heading text-xl font-semibold text-ink mt-3">Submit your exam?</h3>
            <p className="text-sm text-muted2 mt-2">You've answered <strong>{answeredCount} of {total}</strong> questions. Unanswered questions count as wrong.</p>
            <div className="flex gap-2 mt-5 justify-end">
              <button onClick={() => setConfirmSubmit(false)} className="btn-ghost" data-testid="cancel-submit">Keep practising</button>
              <button onClick={submit} disabled={submitting} className="btn-primary" data-testid="confirm-submit">
                {submitting ? "Submitting…" : "Submit now"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExamRun;
