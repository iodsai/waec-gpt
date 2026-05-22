# WAEC Math AI — Product Requirements (Living Doc)

## Original Problem Statement
> "I have uploaded two documents based on https://app.mathgpt.ai/. The intention is to create an intelligent math system for WAEC — the west african examination council, with self-paced learning and solved past questions based on which we can predict and solve similar questions or give similar practice questions to students to practice for help."

## Vision
AI-powered, mobile-first math learning platform purpose-built for West African secondary-school students (SS1–SS3) preparing for WAEC. Inspired by MathGPT but tailored to the WAEC syllabus and examiner style.

## User Personas
- **Student** (primary) — SS1–SS3, age 14–18, mobile-first, exam-focused.
- **Teacher / content team** — needs an admin interface to add real past-paper questions.
- **Parent** — tracks progress.

## Core Requirements (static)
1. Topic-organised lessons (notes + worked examples) with KaTeX rendering.
2. Solved WAEC past questions browser — filterable by topic/subtopic/year/difficulty.
3. AI Math Tutor — Gemini 3 Flash chat, step-by-step working in WAEC examiner style.
4. SymPy verification — programmatic check of equations / claimed answers.
5. AI Similar-question generator — given a question, produce analogous practice items.
6. Exam-simulator — Quick Drill (10 Q, 5 min) + Full Mock (40 Q, 60 min) with timer, auto-grade, and report.
7. Admin tools — manual question entry + Gemini Vision image extraction.
8. Authentication (email/password JWT) with progress tracking + role flag (`is_admin`).
9. Mobile-first design with the "African Modernity" earthy palette (terracotta + moss + warm sand) — distinctly *not* purple AI slop.

## Architecture
- **Backend**: FastAPI + MongoDB (Motor), JWT (bcrypt + pyjwt), SymPy for solver, `emergentintegrations` → Gemini 3 Flash for tutor / similar / vision-extract.
- **Frontend**: React 19 + Tailwind + shadcn + react-katex + sonner + Lucide.
- All API routes under `/api`. JWT stored in `localStorage` as `waec_token`.

## Implemented

### V1 — 2026-02-22 ✅
- Auth (student demo seeded), 8 algebra subtopics, 50 algebra Q's, attempts, progress dashboard, AI Tutor (Gemini 3 Flash), KaTeX everywhere.

### V2 — 2026-02-22 ✅ (this session)
- **Topic system**: 6 topics modeled (Algebra, Trigonometry, Geometry, Statistics, Calculus, Vectors) — 3 live, 3 Coming Soon.
- **Trigonometry**: 5 subtopics, full lessons + 25 questions (years 2016-2023).
- **Geometry**: 5 subtopics, full lessons + 25 questions (years 2016-2023).
- **Algebra expanded**: +30 questions spanning years 2010-2024 → 80 algebra questions total.
- **Exam simulator**: Quick Drill (10 Q, 5 min) + Full Mock (40 Q, 60 min). Topic-scoped or mixed. Timer auto-submits. Report shows score, time, per-subtopic accuracy, per-question review with worked solutions. Exam attempts also recorded into the regular attempts collection so dashboard accuracy reflects practice.
- **SymPy verify** (`/api/solver/verify`): parses LaTeX-ish equations, solves with SymPy, can verify a claimed answer.
- **Similar-question generator** (`/api/questions/{id}/similar`): Gemini 3 Flash produces N analogous questions with full options + worked solutions.
- **Admin role**: `is_admin` flag on users; admin-only routes (`/api/admin/questions` CRUD + `/api/admin/questions/extract`).
- **Image extraction**: Gemini Vision endpoint accepts multipart image → parsed JSON (question/options/answer/subtopic_guess/difficulty/steps).
- **Admin UI** (`/admin`): manual form + image upload + admin-added list with delete.
- **Topics overview** (`/topics`) + topic detail (`/topics/:topicId`).
- **PastQuestions**: added topic filter, "Generate similar" CTA, topic+subtopic cascade.
- **Tutor**: "Verify with SymPy" button.

## Backlog
### P0
- Real WAEC past papers — scrape from URL when user provides source, or admin team uploads images via existing Vision pipeline.
- Statistics, Calculus, Vectors syllabi (50 Q + lessons each).
- Replace tutor `window.prompt` with inline modal for SymPy verify.

### P1
- Subscription tier (Paystack ₦1,500/mo "WAEC Pro") for unlimited tutor + mock exam access.
- Streaks + leaderboards (gamification).
- Personalised daily study plan from weak-topic detection.
- Audio narration of solutions.

### P2
- PWA offline mode.
- Teacher classroom dashboards.
- Export progress to PDF / share to WhatsApp.

## Known limitations
- Trig/Geometry questions are original WAEC-style, not real past-paper transcriptions — real papers can be added via admin Vision pipeline.
- AI tutor / similar generation latency: 5–20s (Gemini).
- Image extraction quality depends on image clarity & Gemini Vision parsing.
