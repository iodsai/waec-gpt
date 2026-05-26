import React from "react";
import http from "@/lib/api";
import { toast } from "sonner";
import { Bookmark, BookmarkCheck } from "lucide-react";

const BookmarkButton = ({ questionId, bookmarked, onChange }) => {
  const toggle = async () => {
    try {
      const { data } = await http.post("/bookmarks/toggle", { question_id: questionId });
      onChange?.(data.bookmarked);
      toast.success(data.bookmarked ? "Added to revision deck" : "Removed from revision deck");
    } catch (err) {
      console.error("Bookmark toggle failed:", err);
      toast.error("Could not update bookmark");
    }
  };
  return (
    <button
      onClick={toggle}
      data-testid="bookmark-btn"
      aria-label={bookmarked ? "Remove bookmark" : "Add bookmark"}
      className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-sm transition
        ${bookmarked
          ? "border-terracotta bg-terracotta/10 text-terracotta"
          : "border-edge text-muted2 hover:border-terracotta/40 hover:text-terracotta"}`}
    >
      {bookmarked ? <BookmarkCheck size={14} /> : <Bookmark size={14} />}
      {bookmarked ? "Saved" : "Save"}
    </button>
  );
};

export default BookmarkButton;
