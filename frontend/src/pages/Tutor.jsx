import React, { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import http from "@/lib/api";
import MathText from "@/components/MathText";
import MathKeypad from "@/components/MathKeypad";
import { Send, Sparkles, Loader2, FunctionSquare, Check, X } from "lucide-react";
import { toast } from "sonner";

const SUGGESTED = [
  "Differentiate $y = (2x+1)^3$ step by step.",
  "Find $\\int_0^2 (3x^2 + 2)\\,dx$ and explain.",
  "Two vectors $\\vec{a}=3\\mathbf{i}+4\\mathbf{j}$, $\\vec{b}=\\mathbf{i}-2\\mathbf{j}$ — find the angle between them.",
  "Spearman's rank correlation with $\\sum d^2 = 20$, $n=8$ — calculate $r_s$.",
];

const BG = "https://static.prod-images.emergentagent.com/jobs/6b12fdb0-d53c-4163-bc29-3a0f2edc149a/images/4ede2bc38f55d9e0217bb938345dfc325f3e5cfc08e89a27dc85d90cd289e6d5.png";

const Tutor = () => {
  const location = useLocation();
  const navigate = useNavigate();
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

  // Auto-send a prompt passed in via location.state (e.g. from /playground)
  useEffect(() => {
    if (historyLoading) return;
    const auto = location.state?.autoSend;
    if (!auto) return;
    // clear so refresh doesn't re-send
    navigate(location.pathname, { replace: true, state: null });
    send(auto);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [historyLoading]);

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

  const [verifyOpen, setVerifyOpen] = useState(false);
  const [verifyEq, setVerifyEq] = useState("");
  const [verifyAns, setVerifyAns] = useState("");
  const [verifyResult, setVerifyResult] = useState(null);
  const [verifying, setVerifying] = useState(false);
  const verifyEqRef = useRef(null);

  const resetSession = () => {
    const id = crypto.randomUUID();
    localStorage.setItem("waec_tutor_session", id);
    window.location.reload();
  };

  const runVerify = async () => {
    if (!verifyEq.trim()) { toast.error("Enter an equation."); return; }
    setVerifying(true); setVerifyResult(null);
    try {
      const { data } = await http.post("/solver/verify", {
        equation: verifyEq, claimed_answer: verifyAns.trim() || null, variable: "x",
      });
      setVerifyResult(data);
    } catch (e) {
      toast.error("Verification failed");
    } finally {
      setVerifying(false);
    }
  };

  const openVerifyModal = () => {
    setVerifyEq(""); setVerifyAns(""); setVerifyResult(null);
    setVerifyOpen(true);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-12 py-8 flex flex-col h-[calc(100vh-4rem)]" data-testid="tutor-page">
      <div className="flex items-end justify-between gap-3 flex-shrink-0">
        <div>
          <span className="overline">AI Math Tutor · Gemini 3 Flash</span>
          <h1 className="font-heading text-3xl sm:text-4xl font-bold text-ink mt-2 flex items-center gap-3">
            Ask anything about WAEC Further Maths. <Sparkles className="text-terracotta" />
          </h1>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={openVerifyModal} className="btn-ghost text-sm inline-flex items-center gap-2" data-testid="verify-sympy-btn">
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
              <p className="text-muted2 text-sm mt-1">Pick a prompt or type your own Further Maths question.</p>
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

      {/* SymPy Verify Modal */}
      {verifyOpen && (
        <div className="fixed inset-0 bg-black/40 grid place-items-center z-50 px-4" data-testid="verify-modal" onClick={() => setVerifyOpen(false)}>
          <div className="bg-surface rounded-2xl border border-edge p-6 max-w-lg w-full" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center gap-2">
              <FunctionSquare className="text-terracotta" />
              <h3 className="font-heading text-xl font-semibold text-ink">Verify with SymPy</h3>
              <button onClick={() => setVerifyOpen(false)} className="ml-auto p-1 rounded hover:bg-sand" aria-label="close" data-testid="verify-close">
                <X size={18} />
              </button>
            </div>
            <p className="text-sm text-muted2 mt-2">Enter an algebraic equation in <code className="text-xs bg-sand px-1 rounded">x</code>. Use <code className="text-xs bg-sand px-1 rounded">^</code> for powers (e.g. <code className="text-xs bg-sand px-1 rounded">x^2 - 5x + 6 = 0</code>).</p>

            <div className="mt-4">
              <label className="text-sm font-medium text-ink">Equation</label>
              <input
                ref={verifyEqRef}
                value={verifyEq} onChange={(e) => setVerifyEq(e.target.value)}
                placeholder="2x + 7 = 19"
                data-testid="verify-equation-input"
                className="mt-1 w-full px-4 py-3 rounded-xl border border-edge bg-surface font-mono focus:outline-none focus:ring-2 focus:ring-terracotta/30"
                autoFocus
              />
              <MathKeypad targetRef={verifyEqRef} value={verifyEq} onChange={setVerifyEq} />
            </div>
            <div className="mt-3">
              <label className="text-sm font-medium text-ink">Your answer <span className="text-muted2 font-normal">(optional)</span></label>
              <input
                value={verifyAns} onChange={(e) => setVerifyAns(e.target.value)}
                placeholder="6"
                data-testid="verify-answer-input"
                className="mt-1 w-full px-4 py-3 rounded-xl border border-edge bg-surface font-mono focus:outline-none focus:ring-2 focus:ring-terracotta/30"
              />
            </div>

            <button onClick={runVerify} disabled={verifying} className="btn-primary mt-5 w-full inline-flex items-center justify-center gap-2 disabled:opacity-60" data-testid="verify-run-btn">
              {verifying ? <><Loader2 className="animate-spin" size={16} /> Verifying…</> : "Verify"}
            </button>

            {verifyResult && (
              <div className="mt-5 p-4 rounded-xl bg-sand/60 border border-edge" data-testid="verify-result">
                {!verifyResult.ok ? (
                  <div className="text-error text-sm">
                    <X size={14} className="inline" /> Couldn't parse equation: <code>{verifyResult.error}</code>
                  </div>
                ) : (
                  <>
                    <div className="text-xs text-muted2">Solutions</div>
                    <div className="font-heading text-lg text-ink mt-0.5">
                      {verifyResult.solutions.length ? `x = ${verifyResult.solutions.join(",  ")}` : "no real solution"}
                    </div>
                    {verifyResult.matches_claim === true && (
                      <div className="mt-3 text-success text-sm flex items-center gap-1.5">
                        <Check size={14} /> Your answer matches a SymPy solution.
                      </div>
                    )}
                    {verifyResult.matches_claim === false && (
                      <div className="mt-3 text-error text-sm flex items-center gap-1.5">
                        <X size={14} /> Your answer does not match.
                      </div>
                    )}
                    {verifyResult.interpreted && (
                      <div className="mt-2 text-xs text-muted2">Interpreted as: <code className="bg-surface px-1.5 rounded">{verifyResult.interpreted}</code></div>
                    )}
                  </>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Tutor;
