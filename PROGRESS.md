# Progress Log — Computer Vision Book

> **Last session:** 2026-04-27 · **Status:** Pre-launch (Week 0) complete · **Next session:** Resume here.

## ✅ Completed

### Day 1 — 2026-04-27 (Pre-launch)

**Planning & outline**
- [x] Read Northwestern course proposal; expanded 10 modules → 20 book chapters
- [x] Researched 2026 CV landscape (Stanford CS231n/CME296, MIT 6.S058, frontier models, books)
- [x] `BOOK_OUTLINE.md` — 20-chapter outline with 4-5 line outlines per chapter, 5 parts, 8-week schedule
- [x] `BOOK_OUTLINE.docx` + `BOOK_OUTLINE.pdf` — typeset versions
- [x] `WRITING_PLAN.xlsx` — 6-sheet workbook (Overview / Chapter Plan / Daily Schedule / Daily Routine / Risks / Word Tracker), pre-filled dates from 2026-04-27

**Repo bootstrap**
- [x] GitHub repo created: https://github.com/mlnjsh/computer-vision-book (public)
- [x] `bootstrap_repo.py` generates 20 chapter folders + scaffolding (idempotent)
- [x] Top-level: `README.md`, `CHAPTER_TEMPLATE.md`, `requirements.txt` (April-2026 pinned), `LICENSE` (MIT/CC), `CONTRIBUTING.md`, `.gitignore`
- [x] `references/` — published_book_repos.md, kaggle_resources.md, youtube_and_courses.md, papers_per_chapter.md
- [x] `kaggle/README.md` — workspace + free-tier compute strategy
- [x] `.github/workflows/smoke-test.yml` — notebook lint CI
- [x] Per-chapter `chapters/chXX-*/README.md` with draft checklist, datasets, GitHub refs

**Detailed lesson plans**
- [x] `LESSON_PLANS.md` — master file with ordered, typed TOCs for all 20 chapters
- [x] Section type system: `[HOOK]/[DEF]/[CONCEPT]/[THEORY]/[CODE]/[NB]/[FIG]/[PROD]/[EX]/[READ]`
- [x] Per-chapter `chapters/chXX-*/LESSON.md` (auto-split via `split_lesson_plans.py`)
- [x] `LESSON_PLANS.docx` — color-coded badges, 819 paragraphs, 62 KB
- [x] All chapter READMEs link to their LESSON.md

**Commits pushed (4 total)**
```
15d497b  Add LESSON_PLANS.docx (Word version) + generator
7fbf8c8  Add detailed per-chapter lesson plans
7b9261e  Untrack Office lock files; ignore ~$* pattern
95872b0  Bootstrap book repo: 20 chapters, scaffolding, references
```

---

## 🟡 Open Decisions (answer before drafting starts)

These five calls cascade through every chapter. Make them before Week 1 drafting:

1. **Framework strategy** — PyTorch-only (recommended) vs PyTorch + TensorFlow appendix.
2. **Math depth** — "enough to debug" (recommended, practitioner audience) vs "rigorous derivations" (academic).
3. **Running case-study dataset** — recommend pairing MS-COCO (general) with a domain set from your real work (EY frog SDM, TAHMO, medical, agriculture). Tell me which.
4. **Pedagogical pattern** — problem-first (default `[HOOK]` opens every chapter) vs definition-first.
5. **THEORY granularity** — single `[THEORY]` tag (current) vs `[THEORY-light]` + `[THEORY-deep]` so readers can skip deep math.

Bonus: **swap in your own papers** from Kaggle / EY / TAHMO work into Chapters 6 (Training), 10 (Self-Supervised), 18 (Domains) — see `references/papers_per_chapter.md`.

---

## ▶️ Tomorrow — Pick One to Drive

| Option | Effort | Output |
|---|---|---|
| **(a) Draft Chapter 1 prose** | 3 hrs | `chapters/ch01-landscape/draft.md` — atoms 1.0–1.11 written |
| **(b) Build Chapter 1 notebook** | 2 hrs | `notebooks/ch01_landscape.ipynb` — 7 cells, runs on T4 |
| **(c) Push 20 Kaggle notebook stubs** | 1 hr | 20 public Kaggle URLs the book can reference |
| **(d) Generate `LESSON_PLANS.pdf`** | 30 min | PDF parity with the .md/.docx versions |
| **(e) Answer the 5 open decisions above** | 15 min | Unblocks all chapter drafting |

**Recommended order: (e) → (b) → (a)** — answering decisions first prevents rewriting; notebook-first means prose is written around working code.

---

## 📂 Where things live

```
C:\Users\Milan Amrut Joshi\Desktop\Computer_Vision\
├── BOOK_OUTLINE.{md,docx,pdf}    ← 20-chapter outline
├── LESSON_PLANS.{md,docx}        ← detailed per-chapter TOCs
├── WRITING_PLAN.xlsx             ← 8-week schedule, daily tracker, word counter
├── PROGRESS.md                   ← this file
├── README.md                     ← repo overview
├── chapters/chXX-*/              ← README + LESSON per chapter
├── notebooks/                    ← (empty — will be filled chapter by chapter)
├── figures/chXX/                 ← figure scripts go here
├── case-studies/chXX/            ← end-to-end production case studies
├── references/                   ← books / Kaggle / YouTube / papers
├── kaggle/                       ← Kaggle workspace strategy
└── *.py                          ← bootstrap + generators (re-runnable)
```

**GitHub:** https://github.com/mlnjsh/computer-vision-book

---

## 🔧 Re-run anything

```bash
# Regenerate outline files
python generate_book_outline_docx.py
python generate_book_outline_pdf.py
python generate_writing_plan_xlsx.py

# Regenerate lesson plans
python generate_lesson_plans_docx.py     # rebuilds LESSON_PLANS.docx from .md
python split_lesson_plans.py             # rebuilds chapters/*/LESSON.md from master
python link_lessons_to_readmes.py        # keeps README→LESSON links in sync

# Re-bootstrap (idempotent — won't overwrite existing files unless --force)
python bootstrap_repo.py
```

---

## 📅 Schedule reality check

Per `WRITING_PLAN.xlsx`:

| Week | Dates (from 2026-04-27) | Chapters | Status |
|---|---|---|---|
| **0** | Apr 27 – May 02 | Pre-launch | ✅ done |
| 1 | May 04 – May 09 | Ch 1, Ch 2 | pending |
| 2 | May 11 – May 16 | Ch 3, Ch 4 | pending |
| 3 | May 18 – May 23 | Ch 5, Ch 6 | pending |
| 4 | May 25 – May 30 | Ch 7, Ch 8 + mid-book pass | pending |
| 5 | Jun 01 – Jun 06 | Ch 9, Ch 10 | pending |
| 6 | Jun 08 – Jun 13 | Ch 11, Ch 12, Ch 13 | pending |
| 7 | Jun 15 – Jun 20 | Ch 14, Ch 15, Ch 16 | pending |
| 8 | Jun 22 – Jun 27 | Ch 17, Ch 18, Ch 19, Ch 20 + cross-pass | pending |
| 9 | Jun 29 – Jul 04 | Buffer / revision | pending |

**Hardest chapters (★★★★★):** 12 Diffusion, 16 3D Gaussian Splatting, 17 VLA. Pre-research one week ahead of writing them.
