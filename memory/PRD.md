# WAEC Math AI — Product Requirements (Living Doc)

## Original Problem Statement
> "I have uploaded two documents based on https://app.mathgpt.ai/. The intention is to create an intelligent math system for WAEC — the west african examination council, with self-paced learning and solved past questions based on which we can predict and solve similar questions or give similar practice questions to students to practice for help. Read all the attached files and let me know what you think."

## Vision
An AI-powered, mobile-first math learning platform purpose-built for West African secondary-school students (SS1–SS3) preparing for the WAEC examination — inspired by MathGPT but localised to the WAEC syllabus and examiner style.

## User Personas
- **Primary** — SS1–SS3 student (age 14–18) in Nigeria / Ghana / West Africa, mobile-first, self-paced, exam-focused.
- **Secondary** — Teachers wanting to direct students to verified worked solutions; parents tracking progress.

## Core Requirements (static)
1. Topic-organized lessons with notes and worked examples (KaTeX math).
2. Solved WAEC past questions browser — filterable by subtopic / year / difficulty, with step-by-step solutions.
3. AI math tutor — answers any algebra question in WAEC examiner style, step by step.
4. Authentication (email/password, JWT) with progress tracking.
5. Mobile-first, distinct African-modernity aesthetic (terracotta + moss, NOT purple AI slop).

## Architecture (V1)
- **Backend**: FastAPI + MongoDB (`motor`), JWT auth (`bcrypt` + `pyjwt`), AI via `emergentintegrations` → Gemini 3 Flash (`gemini-3-flash-preview`).
- **Frontend**: React 19 + Tailwind + shadcn, `react-katex` for math, `sonner` for toasts.
- **All API routes**: prefixed `/api`. Token stored in `localStorage` (`waec_token`).

## Implemented — V1 (2026-02-22)
- ✅ Auth: register / login / me / JWT-protected routes
- ✅ Demo user auto-seed: `student@waec.com` / `Student@123`
- ✅ 50 WAEC-style algebra questions seeded across 8 subtopics, each with multi-step worked solution
- ✅ 8 subtopic lessons (notes + worked example) — Linear, Quadratic, Simultaneous, Indices, Logarithms, Variation, Sequences & Series, Inequalities
- ✅ Past Questions browser with filters (subtopic, year, difficulty) + attempt submission
- ✅ Progress dashboard — accuracy, totals, per-subtopic stats, recent attempts (with rendered math)
- ✅ AI Tutor chat (Gemini 3 Flash) with persistent per-session history, KaTeX rendering inline + block
- ✅ Earthy "African modernity" design — terracotta (#D95D39) + moss (#2A4B46) + warm sand
- ✅ Tested: 19/19 backend + 8/8 frontend flows pass

## Prioritized Backlog
### P0 — must-have for next phase
- Expand syllabus beyond algebra: Trigonometry, Geometry, Statistics, Calculus, Vectors (lessons + 50 questions per topic)
- Full WAEC past-paper ingestion pipeline (real years 2010–2024)
- Exam-simulator mode with timer, auto-grading, performance report

### P1 — should-have
- Similar-question generator (Gemini) — given a question, produce N analogous practice items
- Weak-topic detector + personalised daily plan
- SymPy-backed step-by-step equation solver (free-form input)
- Public share / "Send to friend" for a question
- Streaks + achievements (gamification)

### P2 — nice-to-have
- Audio narration of solutions
- Teacher accounts & class dashboards
- Offline mode (PWA)
- Stripe / Paystack subscription (Premium tier with unlimited tutor messages)

## Known Limitations (V1)
- Algebra-only content.
- Questions are original WAEC-style examples, not actual WAEC past-paper transcriptions.
- AI tutor occasionally takes 5–15s for complex problems (Gemini latency).
