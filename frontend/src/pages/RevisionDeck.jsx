import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import http from "@/lib/api";
import { toast } from "sonner";
import MathText from "@/components/MathText";
import { Bookmark, BookmarkX, FileText, Loader2 } from "lucide-react";

const RevisionDeck = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const { data } = await http.get("/bookmarks");
      setItems(data.items || []);
    } catch (err) {
      console.error("Failed to load revision deck:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const remove = async (qid) => {
    try {
      await http.post("/bookmarks/toggle", { question_id: qid });
      setItems((xs) => xs.filter((x) => x.question_id !== qid));
      toast.success("Removed from revision deck");
    } catch (err) {
      console.error("remove failed:", err);
      toast.error("Could not remove");
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-12 py-10" data-testid="revision-deck-page">
      <span className="overline">Your saved questions</span>
      <h1 className="font-heading text-4xl font-bold text-ink mt-2">Revision deck</h1>
      <p className="text-muted2 mt-2">
        Questions you've bookmarked for later. Perfect for one-day-before-exam drilling.
      </p>

      {loading ? (
        <div className="mt-10 flex items-center gap-2 text-muted2" data-testid="deck-loading">
          <Loader2 className="animate-spin" size={18} /> Loading your deck…
        </div>
      ) : items.length === 0 ? (
        <div className="card-surface p-10 text-center mt-8" data-testid="deck-empty">
          <Bookmark className="mx-auto text-terracotta" size={32} />
          <h2 className="font-heading text-xl text-ink mt-3">No saved questions yet</h2>
          <p className="text-muted2 text-sm mt-2 max-w-md mx-auto">
            Tap "Save" on any past question to add it here. Build your personal exam-prep deck.
          </p>
          <Link to="/past-questions" className="btn-primary mt-5 inline-flex items-center gap-2" data-testid="deck-browse-btn">
            <FileText size={16} /> Browse past questions
          </Link>
        </div>
      ) : (
        <div className="card-surface divide-y divide-edge mt-6" data-testid="deck-list">
          {items.map((q) => (
            <div key={q.question_id} className="px-5 py-4 flex items-center gap-4" data-testid={`deck-item-${q.question_id}`}>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap mb-1.5">
                  <span className="tag">{q.subtopic_name}</span>
                  <span className="tag">WAEC {q.year}</span>
                  <span className="tag !text-terracotta">{q.difficulty}</span>
                  {q.question_type === "theory" && (
                    <span className="tag !bg-moss/10 !text-moss !border-moss/30">Theory</span>
                  )}
                </div>
                <div className="text-sm text-ink line-clamp-2"><MathText text={q.question} /></div>
              </div>
              <Link
                to={`/past-questions?topic=${encodeURIComponent(q.topic_name?.toLowerCase().split(" ")[0] || "")}`}
                className="btn-ghost text-sm whitespace-nowrap"
                data-testid={`deck-open-${q.question_id}`}
              >
                Open
              </Link>
              <button
                onClick={() => remove(q.question_id)}
                className="p-2 rounded-lg border border-edge text-error/80 hover:bg-error/10"
                data-testid={`deck-remove-${q.question_id}`}
                aria-label="Remove bookmark"
              >
                <BookmarkX size={14} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RevisionDeck;
