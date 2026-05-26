# WAEC Elective Math AI — Product Requirements (Living Doc)

## Original Problem Statement
> "I have uploaded two documents based on https://app.mathgpt.ai/. The intention is to create an intelligent math system for WAEC — the west african examination council, with self-paced learning and solved past questions based on which we can predict and solve similar questions or give similar practice questions to students to practice."

## Vision
AI-powered, mobile-first **WAEC Further Mathematics (Elective)** learning platform purpose-built for West African senior-secondary science students preparing for the WAEC Elective Maths exam. Inspired by MathGPT, tailored to the WAEC Further Maths syllabus and examiner style.

## User Personas
- **Primary** — SS2 / SS3 science students writing WAEC Elective Maths (Further Maths).
- **Admin / Teacher** — adds real past-paper questions via the import pipeline.

## Core Requirements (static)
1. Topic-organised lessons (notes + worked examples) with KaTeX rendering.
2. Solved WAEC Further Maths past questions browser — filterable by topic/subtopic/year/difficulty.
3. AI Math Tutor — Gemini 3 Flash chat, step-by-step working in WAEC examiner style.
4. SymPy verification — inline modal to check student equations.
5. AI Similar-question generator — produce analogous practice items.
6. Exam-simulator — Quick Drill (10 Q / 5 min) + Full Mock (40 Q / 60 min) with timer + report.
7. Admin tools — manual question entry + Gemini Vision image extraction + WAEC past-paper scraper (from waeconline.org.ng/Further/).
8. Authentication (email/password JWT) with progress tracking + role flag (`is_admin`).
9. Mobile-first "African Modernity" earthy palette (terracotta + moss + warm sand).

## Architecture
- **Backend**: FastAPI + MongoDB (Motor), JWT (bcrypt + pyjwt), SymPy for solver, `emergentintegrations` → Gemini 3 Flash for tutor / similar / vision-extract.
- **Frontend**: React 19 + Tailwind + shadcn + react-katex + sonner + Lucide.
- All API routes under `/api`. JWT stored in `localStorage` as `waec_token`.

## Implemented

### V3 — Further Maths Pivot ✅ (current)
- **Branding**: WAEC Elective Math AI.
- **Topics (8 live, full syllabus)**:
  - ✅ Statistics & Probability (5 subtopics, 106 Q + lessons)
  - ✅ Calculus (5 subtopics, 110 Q + lessons)
  - ✅ Vectors (5 subtopics, 122 Q + lessons)
  - ✅ Sets & Logic (5 subtopics, 50 Q + lessons)
  - ✅ Surds & Polynomials (5 subtopics, 50 Q + lessons)
  - ✅ Sequences & Binomial (5 subtopics, 50 Q + lessons)
  - ✅ Matrices & Determinants (5 subtopics, 50 Q + lessons)
  - ✅ Mechanics (5 subtopics, 50 Q + lessons)
- **Total bank**: ~700+ questions (588 seed + 188 from 2010-2018 batch + 88 from 2019-2023 batch).
- **Scraper**: 29 Further Maths papers indexed; admin can preview-import per paper.
- **Batch importer** ✅ — background job processes a year-range; live progress UI in admin; orphaned-job recovery on backend restart.
  - 2026-02-22: 2010-2018 batch → 16 papers, 188 questions, 0 errors.
  - 2026-02-22: 2019-2023 batch → 7/9 papers, 88 questions saved.
- **PastQuestions.jsx refactored** ✅ — split into `ObjectivePane`, `TheoryPane`, `SimilarBlock` child components.
- **SymPy verify**: inline modal in Tutor.
- **Exam hydration warning**: fixed.
- **Theory question support**: schema exists, exam sampler excludes theory, accuracy stats exclude reveals.
- **Validation**: 37/37 backend pytest pass (+1 intentional skip) + frontend flows verified.

### V1/V2 (deprecated/dropped)
- General Maths content (Algebra/Trig/Geometry seed + 62 real waeconline imports) — DROPPED in pivot.

## Backlog
### P0
- (none — all P0 items closed in 2026-02-22 session)

### P1
- Paystack subscription (₦1,500/mo "Elective Pro") — unlimited tutor + full mock access.
- Streaks + leaderboards (gamification).
- Personalised daily study plan from weak-topic detection ("Weak-spot radar" widget).
- Retry the 2 failed scraper papers (WASSCE School 2023, WASSCE Private 2nd 2019 — Gemini occasionally returns array shape).

### P2
- PWA offline mode.
- Teacher classroom dashboards.
- Export progress to PDF / share to WhatsApp.

## Known limitations
- AI similar-question / vision-extract latency: 5-20s (Gemini).
- Theory-question rendering path implemented but unused in V3 seed (only used after admin import).
