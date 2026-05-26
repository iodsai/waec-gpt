import React, { useEffect, useState, useRef, useCallback } from "react";
import http from "@/lib/api";
import { toast } from "sonner";
import { Layers, Play, Loader2, CheckCircle2, AlertTriangle, Clock } from "lucide-react";

const BatchImport = () => {
  const [yearFrom, setYearFrom] = useState(2010);
  const [yearTo, setYearTo] = useState(2018);
  const [maxQ, setMaxQ] = useState(13);
  const [starting, setStarting] = useState(false);
  const [activeJob, setActiveJob] = useState(null);
  const [recent, setRecent] = useState([]);
  const pollRef = useRef(null);

  const loadJobs = useCallback(async () => {
    try {
      const { data } = await http.get("/admin/import/batch");
      const jobs = data.jobs || [];
      setRecent(jobs);
      const running = jobs.find((j) => j.status === "running");
      if (running) setActiveJob(running);
    } catch (err) {
      console.error("Failed to load batch jobs:", err);
    }
  }, []);

  useEffect(() => {
    loadJobs();
    return () => { if (pollRef.current) clearInterval(pollRef.current); };
  }, [loadJobs]);

  useEffect(() => {
    if (activeJob?.status === "running") {
      pollRef.current = setInterval(async () => {
        try {
          const { data } = await http.get(`/admin/import/batch/${activeJob.id}`);
          setActiveJob(data);
          if (data.status === "completed") {
            clearInterval(pollRef.current);
            toast.success(`Batch import done — ${data.total_saved} questions saved.`);
            loadJobs();
          }
        } catch (err) {
          console.error("Job polling error:", err);
        }
      }, 5000);
      return () => clearInterval(pollRef.current);
    }
  }, [activeJob?.id, activeJob?.status, loadJobs]);

  const start = async () => {
    if (yearFrom > yearTo) { toast.error("Year-from must be ≤ year-to"); return; }
    setStarting(true);
    try {
      const { data } = await http.post("/admin/import/batch", {
        year_from: Number(yearFrom), year_to: Number(yearTo),
        max_questions_per_paper: Number(maxQ),
      });
      toast.success(`Started batch — ${data.total_papers} papers queued`);
      const job = await http.get(`/admin/import/batch/${data.job_id}`);
      setActiveJob(job.data);
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Could not start batch");
    } finally {
      setStarting(false);
    }
  };

  const pct = activeJob && activeJob.total_papers
    ? Math.round(((activeJob.progress_index || 0) / activeJob.total_papers) * 100)
    : 0;

  return (
    <div className="card-surface p-6 mt-8" data-testid="batch-import-block">
      <div className="flex items-center gap-2">
        <Layers className="text-terracotta" size={20} />
        <h2 className="font-heading text-2xl font-semibold text-ink">Batch import (background)</h2>
      </div>
      <p className="text-sm text-muted2 mt-1">
        Queue a range of years and let the server scrape + convert every paper in the background. Auto-saves accepted questions.
        Each paper takes ~30-90s; the 2010-2018 range (~16 papers) needs ~15-25 minutes.
      </p>

      <div className="mt-5 grid sm:grid-cols-4 gap-3">
        <div>
          <label className="text-xs font-medium text-muted2">Year from</label>
          <input type="number" value={yearFrom} onChange={(e) => setYearFrom(e.target.value)}
            data-testid="batch-year-from"
            className="mt-0.5 w-full px-3 py-2 rounded-lg border border-edge bg-surface text-sm" />
        </div>
        <div>
          <label className="text-xs font-medium text-muted2">Year to</label>
          <input type="number" value={yearTo} onChange={(e) => setYearTo(e.target.value)}
            data-testid="batch-year-to"
            className="mt-0.5 w-full px-3 py-2 rounded-lg border border-edge bg-surface text-sm" />
        </div>
        <div>
          <label className="text-xs font-medium text-muted2">Q / paper</label>
          <input type="number" value={maxQ} onChange={(e) => setMaxQ(e.target.value)}
            data-testid="batch-max-q"
            className="mt-0.5 w-full px-3 py-2 rounded-lg border border-edge bg-surface text-sm" />
        </div>
        <div className="flex items-end">
          <button onClick={start} disabled={starting || activeJob?.status === "running"}
            data-testid="batch-start-btn"
            className="btn-primary inline-flex items-center gap-2 disabled:opacity-60 w-full justify-center">
            {starting ? <><Loader2 className="animate-spin" size={16} /> Starting…</>
              : activeJob?.status === "running" ? "Running…" : <><Play size={16} /> Start batch</>}
          </button>
        </div>
      </div>

      {activeJob && (
        <div className="mt-6 border border-edge rounded-xl p-4 bg-sand/30" data-testid="batch-active-job">
          <div className="flex items-center justify-between flex-wrap gap-2">
            <div className="flex items-center gap-2">
              {activeJob.status === "running"
                ? <Loader2 className="animate-spin text-terracotta" size={18} />
                : <CheckCircle2 className="text-success" size={18} />}
              <span className="font-medium text-ink">
                {activeJob.status === "running" ? "Running" : "Completed"} —
                years {activeJob.year_from}-{activeJob.year_to}
              </span>
            </div>
            <span className="text-xs text-muted2 font-mono">{activeJob.id?.slice(0, 8)}…</span>
          </div>
          <div className="mt-3 h-2 bg-edge/40 rounded-full overflow-hidden">
            <div className="h-full bg-terracotta transition-all" style={{ width: `${pct}%` }} />
          </div>
          <div className="mt-2 flex items-center justify-between text-xs text-muted2">
            <span>Paper {activeJob.progress_index || 0} / {activeJob.total_papers}</span>
            <span>Saved: <strong className="text-ink">{activeJob.total_saved || 0}</strong> · Extracted: {activeJob.total_extracted || 0}</span>
          </div>
          {activeJob.current_paper && activeJob.status === "running" && (
            <p className="text-xs text-ink/70 mt-2 flex items-center gap-1">
              <Clock size={12} /> Now: {activeJob.current_paper} ({activeJob.current_year})
            </p>
          )}
          {!!activeJob.errors?.length && (
            <div className="mt-3 text-xs text-error bg-error/5 rounded p-2 border border-error/20">
              <AlertTriangle size={12} className="inline mr-1" />
              {activeJob.errors.length} error(s): {activeJob.errors.slice(-2).join(" · ")}
            </div>
          )}
          {!!activeJob.papers_done?.length && (
            <details className="mt-3 text-xs text-muted2">
              <summary className="cursor-pointer text-ink/80">Papers done ({activeJob.papers_done.length})</summary>
              <ul className="mt-2 space-y-1 font-mono">
                {activeJob.papers_done.map((p) => (
                  <li key={`${p.year}-${p.url || p.label}`}>✓ {p.label} ({p.year}) — saved {p.saved}/{p.extracted}</li>
                ))}
              </ul>
            </details>
          )}
        </div>
      )}

      {!!recent.length && (
        <details className="mt-4 text-sm text-muted2">
          <summary className="cursor-pointer text-ink/80">Recent batch jobs ({recent.length})</summary>
          <div className="mt-2 space-y-1">
            {recent.slice(0, 5).map((j) => (
              <div key={j.id} className="flex items-center justify-between text-xs font-mono py-1 border-b border-edge/40">
                <span>{j.year_from}-{j.year_to}</span>
                <span className={j.status === "completed" ? "text-success" : "text-terracotta"}>{j.status}</span>
                <span>saved {j.total_saved}/{j.total_extracted}</span>
              </div>
            ))}
          </div>
        </details>
      )}
    </div>
  );
};

export default BatchImport;
