import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { ArrowRight, CheckCircle2, MessagesSquare, FileText, BookOpen, Sparkles, GraduationCap } from "lucide-react";

const HERO_IMG =
  "https://static.prod-images.emergentagent.com/jobs/6b12fdb0-d53c-4163-bc29-3a0f2edc149a/images/735327ee4f38ab1ad84004ebb6ec9e2343847ff1cc5974441c267b040fc9b3b7.png";
const STUDENT_IMG =
  "https://images.unsplash.com/photo-1620829813573-7c9e1877706f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NzB8MHwxfHNlYXJjaHwxfHxhZnJpY2FuJTIwc3R1ZGVudCUyMHN0dWR5aW5nJTIwdGFibGV0fGVufDB8fHx8MTc3OTQ1OTg2N3ww&ixlib=rb-4.1.0&q=85";

const Landing = () => {
  const { user } = useAuth();
  return (
    <div className="bg-paper" data-testid="landing-page">
      {/* HERO */}
      <section className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 pt-14 pb-20 lg:pt-20 lg:pb-32">
        <div className="grid lg:grid-cols-12 gap-10 items-center">
          <div className="lg:col-span-7">
            <span className="overline" data-testid="hero-overline">For WAEC SS1 – SS3 Students</span>
            <h1 className="font-heading mt-3 text-4xl sm:text-5xl lg:text-6xl font-bold leading-[1.05] text-ink tracking-tight">
              Master WAEC Algebra,<br className="hidden sm:block" />
              <span className="text-terracotta">step by step.</span>
            </h1>
            <p className="mt-6 text-lg text-muted2 max-w-xl leading-relaxed">
              Self-paced lessons, decades of solved WAEC past questions, and an AI tutor
              that explains every working — in plain English, like a great teacher would.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link
                to={user ? "/dashboard" : "/register"}
                className="btn-primary inline-flex items-center gap-2"
                data-testid="hero-cta-start"
              >
                Start practising free <ArrowRight size={18} />
              </Link>
              <Link to="/login" className="btn-ghost" data-testid="hero-cta-login">
                I already have an account
              </Link>
            </div>
            <div className="mt-8 flex flex-wrap gap-6 text-sm text-muted2">
              <div className="flex items-center gap-2"><CheckCircle2 size={16} className="text-success" /> 50+ solved questions</div>
              <div className="flex items-center gap-2"><CheckCircle2 size={16} className="text-success" /> 8 algebra subtopics</div>
              <div className="flex items-center gap-2"><CheckCircle2 size={16} className="text-success" /> AI step-by-step solver</div>
            </div>
          </div>

          <div className="lg:col-span-5 relative">
            <div className="relative rounded-3xl overflow-hidden border border-edge">
              <img src={HERO_IMG} alt="Student studying for WAEC math" className="w-full h-[420px] object-cover" />
              <div className="absolute inset-0 bg-gradient-to-r from-black/55 via-black/15 to-transparent" />
              <div className="absolute bottom-5 left-5 right-5 text-white">
                <div className="font-heading text-xl font-semibold leading-tight">Built for West African students.</div>
                <div className="text-sm opacity-90">WAEC examiner-style explanations, mobile-first.</div>
              </div>
            </div>
            <div className="hidden lg:block absolute -bottom-6 -left-6 bg-surface border border-edge rounded-2xl p-4 shadow-sm w-48">
              <div className="text-[10px] uppercase tracking-[0.2em] text-muted2 font-medium">Pass rate target</div>
              <div className="font-heading text-3xl text-ink mt-1">A1</div>
              <div className="text-xs text-muted2">Aim higher with daily practice.</div>
            </div>
          </div>
        </div>
      </section>

      {/* FEATURES BENTO */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 pb-24">
        <div className="grid md:grid-cols-6 gap-5">
          <div className="md:col-span-3 card-surface p-7" data-testid="feature-lessons">
            <BookOpen className="text-terracotta" size={26} />
            <h3 className="font-heading mt-4 text-2xl font-semibold text-ink">Topic-organised lessons</h3>
            <p className="mt-2 text-muted2">Linear & quadratic equations, indices, logarithms, variation, sequences, inequalities — with notes and worked examples.</p>
          </div>
          <div className="md:col-span-3 card-surface p-7" data-testid="feature-past-questions">
            <FileText className="text-moss" size={26} />
            <h3 className="font-heading mt-4 text-2xl font-semibold text-ink">Solved WAEC past questions</h3>
            <p className="mt-2 text-muted2">Filter by subtopic, year, and difficulty. Each question opens to a clean, step-by-step solution.</p>
          </div>
          <div className="md:col-span-4 card-surface p-7 relative overflow-hidden" data-testid="feature-ai-tutor">
            <Sparkles className="text-terracotta" size={26} />
            <h3 className="font-heading mt-4 text-2xl font-semibold text-ink">AI Math Tutor (Gemini 3 Flash)</h3>
            <p className="mt-2 text-muted2 max-w-lg">Ask any algebra question. The tutor explains in WAEC examiner style, with numbered steps and beautifully rendered formulas.</p>
            <div className="mt-5 bg-sand/70 border border-edge rounded-xl p-4 max-w-md">
              <div className="text-xs text-muted2">You</div>
              <div className="text-sm text-ink">Solve $2x + 7 = 19$.</div>
              <div className="text-xs text-muted2 mt-3">AI Tutor</div>
              <div className="text-sm text-ink"><strong>Step 1:</strong> Subtract 7 → $2x = 12$. <strong>Step 2:</strong> Divide by 2 → $x = 6$.</div>
            </div>
          </div>
          <div className="md:col-span-2 card-surface p-7" data-testid="feature-progress">
            <GraduationCap className="text-moss" size={26} />
            <h3 className="font-heading mt-4 text-2xl font-semibold text-ink">Track your progress</h3>
            <p className="mt-2 text-muted2">See accuracy by subtopic. Spot weaknesses early and focus practice.</p>
          </div>
        </div>
      </section>

      {/* TESTIMONIAL / IMAGE */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 pb-24">
        <div className="grid lg:grid-cols-12 gap-8 items-center">
          <div className="lg:col-span-5">
            <img src={STUDENT_IMG} alt="Student on tablet" className="w-full h-[360px] object-cover rounded-3xl border border-edge" />
          </div>
          <div className="lg:col-span-7">
            <span className="overline">Why WAEC Math AI</span>
            <h2 className="font-heading mt-3 text-3xl lg:text-4xl font-semibold text-ink">
              Practice past questions. Learn the working. Get ready.
            </h2>
            <p className="mt-4 text-muted2 leading-relaxed text-lg max-w-2xl">
              West African students rely on past questions — but answers without explanations don't teach.
              We pair each question with a clear, numbered, examiner-style solution, and let you ask
              follow-ups to a patient AI tutor that never gets tired.
            </p>
            <div className="mt-6 grid sm:grid-cols-2 gap-3 max-w-xl">
              {["Solve any algebra question on the fly", "Step-by-step worked solutions", "Filter past questions by year", "Personal accuracy tracking"].map((t) => (
                <div key={t} className="flex items-start gap-2 text-sm text-ink">
                  <CheckCircle2 size={18} className="text-success mt-0.5 flex-shrink-0" /> {t}
                </div>
              ))}
            </div>
            <div className="mt-7">
              <Link to={user ? "/dashboard" : "/register"} className="btn-secondary inline-flex items-center gap-2" data-testid="bottom-cta">
                <MessagesSquare size={18} /> Try the AI tutor now
              </Link>
            </div>
          </div>
        </div>
      </section>

      <footer className="border-t border-edge bg-paper">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 py-10 flex flex-col sm:flex-row justify-between gap-4 text-sm text-muted2">
          <div>© {new Date().getFullYear()} WAEC Math AI · Built for West African scholars.</div>
          <div className="flex gap-5">
            <span>Algebra V1</span>
            <span>Powered by Gemini 3 Flash</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
