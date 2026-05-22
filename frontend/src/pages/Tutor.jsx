import React, { useEffect, useRef, useState } from "react";
import http from "@/lib/api";
import MathText from "@/components/MathText";
import { Send, Sparkles, Loader2, FunctionSquare, Check, X } from "lucide-react";
import { toast } from "sonner";

const SUGGESTED = [
  "Solve 3(x − 2) + 5 = 2x + 4 step by step.",
  "Explain the quadratic formula with a worked example.",
  "What is the difference between AP and GP?",
  "Evaluate log₂ 32 and explain.",
];

const BG = "https://static.prod-images.emergentagent.com/jobs/6b12fdb0-d53c-4163-bc29-3a0f2edc149a/images/4ede2bc38f55d9e0217bb938345dfc325f3e5cfc08e89a27dc85d90cd289e6d5.png";

const Tutor = () => {
  const [sessionId] = useState(() => {
    const existing = localStorage.getItem("waec_tutor_session");
    if (existing) return existing;
    const id = crypto.randomUUID();
    localStorage.setItem("waec_tutor_session", id);
    return id;
  });
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(true);
  const endRef = useRef(null);

  useEffect(() => {
    http.get(`/tutor/history/${sessionId}`)
      .then((r) => setMessages(r.data || []))
      .finally(() => setHistoryLoading(false));
  }, [sessionId]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const send = async (text) => {
    const msg = (text ?? input).trim();
    if (!msg || loading) return;
    setInput("");
    const userMsg = { id: `u-${Date.now()}`, role: "user", content: msg };
    setMessages((m) => [...m, userMsg]);
    setLoading(true);
    try {
      const { data } = await http.post("/tutor/chat", { session_id: sessionId, message: msg });
      setMessages((m) => [...m, { id: `a-${Date.now()}`, role: "assistant", content: data.reply }]);
    } catch (e) {
      toast.error(e?.response?.data?.detail || "AI tutor is unavailable. Try again.");
      setMessages((m) => m.filter((x) => x.id !== userMsg.id));
    } finally {
      setLoading(false);
    }
  };

  const onKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  const resetSession = () => {
    const id = crypto.randomUUID();
    localStorage.setItem("waec_tutor_session", id);
    window.location.reload();
  };

  const verifyEquation = async () => {
    const eq = window.prompt(
      "Enter an algebraic equation to verify (e.g. 2x + 7 = 19, or x^2 - 5x + 6 = 0).\nOptionally append `; answer=…` to check a specific answer.",
      ""
    );
    if (!eq?.trim()) return;
    let equation = eq, claimed = null;
    const m = eq.match(/^(.+?);\s*answer\s*=\s*(.+)$/i);
    if (m) { equation = m[1]; claimed = m[2]; }
    try {
      const { data } = await http.post("/solver/verify", { equation, claimed_answer: claimed, variable: "x" });
      if (!data.ok) { toast.error("Couldn't parse equation: " + data.error); return; }
      const sols = data.solutions.join(", ") || "no real solution";
      let msg = `Verified by SymPy ✓\nSolutions: x = ${sols}`;
      if (data.matches_claim === true) msg += `\nClaim ${claimed} ✓ matches`;
      else if (data.matches_claim === false) msg += `\nClaim ${claimed} ✗ does NOT match`;
      toast.success(msg, { duration: 8000 });
    } catch (e) {
      toast.error("Verification failed");
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-12 py-8 flex flex-col h-[calc(100vh-4rem)]" data-testid="tutor-page">
      <div className="flex items-end justify-between gap-3 flex-shrink-0">
        <div>
          <span className="overline">AI Math Tutor · Gemini 3 Flash</span>
          <h1 className="font-heading text-3xl sm:text-4xl font-bold text-ink mt-2 flex items-center gap-3">
            Ask anything about WAEC algebra. <Sparkles className="text-terracotta" />
          </h1>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={verifyEquation} className="btn-ghost text-sm inline-flex items-center gap-2" data-testid="verify-sympy-btn">
            <FunctionSquare size={14} /> Verify with SymPy
          </button>
          <button onClick={resetSession} className="btn-ghost text-sm" data-testid="reset-session-btn">New chat</button>
        </div>
      </div>

      {/* CHAT AREA */}
      <div
        className="flex-1 mt-6 card-surface overflow-hidden flex flex-col relative"
        style={{ backgroundImage: `url(${BG})`, backgroundSize: "cover", backgroundBlendMode: "overlay", backgroundColor: "rgba(255,255,255,0.92)" }}
      >
        <div className="flex-1 overflow-y-auto p-6 space-y-4" data-testid="chat-messages">
          {historyLoading && <div className="text-sm text-muted2 text-center">Loading conversation…</div>}

          {!historyLoading && messages.length === 0 && (
            <div className="text-center py-10">
              <Sparkles className="mx-auto text-terracotta" size={28} />
              <h3 className="font-heading text-xl text-ink mt-3 font-semibold">Start a conversation</h3>
              <p className="text-muted2 text-sm mt-1">Pick a prompt or type your own algebra question.</p>
              <div className="grid sm:grid-cols-2 gap-2 mt-5 max-w-xl mx-auto">
                {SUGGESTED.map((s, i) => (
                  <button key={i} onClick={() => send(s)} className="text-left text-sm bg-surface border border-edge rounded-xl px-4 py-3 hover:border-terracotta/50 transition" data-testid={`suggested-prompt-${i}`}>
                    <MathText text={s} />
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((m) => (
            <div key={m.id} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`} data-testid={`message-${m.role}`}>
              <div className={`max-w-[85%] rounded-2xl px-5 py-3 ${
                m.role === "user"
                  ? "bg-terracotta text-white rounded-tr-sm"
                  : "bg-sand text-ink rounded-tl-sm border border-edge"
              }`}>
                <div className="text-xs opacity-70 mb-1">{m.role === "user" ? "You" : "AI Tutor"}</div>
                <div className="leading-relaxed whitespace-pre-wrap break-words">
                  <MathText text={m.content} />
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start" data-testid="ai-typing">
              <div className="bg-sand text-ink rounded-2xl rounded-tl-sm border border-edge px-5 py-3 flex items-center gap-2">
                <Loader2 size={16} className="animate-spin text-terracotta" />
                <span className="text-sm text-muted2">Thinking through it…</span>
              </div>
            </div>
          )}

          <div ref={endRef} />
        </div>

        {/* INPUT */}
        <div className="border-t border-edge bg-surface p-3 flex items-end gap-2 flex-shrink-0">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={onKey}
            rows={1}
            placeholder="Type your math question… (Shift+Enter for new line)"
            data-testid="tutor-input"
            className="flex-1 resize-none px-4 py-3 rounded-xl border border-edge bg-surface focus:outline-none focus:ring-2 focus:ring-terracotta/30 max-h-32"
          />
          <button
            onClick={() => send()}
            disabled={loading || !input.trim()}
            data-testid="tutor-send-btn"
            className="btn-primary flex-shrink-0 disabled:opacity-50"
            aria-label="Send message"
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Tutor;
