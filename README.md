# Computer Vision: From Foundations to Frontier (2026)

A practitioner-first, 20-chapter book covering modern computer vision —
classical → CNN → ViT → foundation models → multimodal → embodied AI.

> **Author:** Milan Amrut Joshi
> **Status:** Pre-launch (Week 0)
> **Target completion:** First draft in 8 weeks
> **Stack:** Python 3.12, PyTorch 2.x, Hugging Face, Ultralytics, OpenCV, ONNX/TensorRT

---

## Why this book

By 2026 the CV landscape has structurally shifted three ways most existing books miss:

1. **Frozen foundation backbones** (DINOv3, SAM 3) replace task-specific training for most use cases.
2. **Vision-Language-Action models** (RT-2, OpenVLA, π0, Helix) collapse perception + reasoning + control into one architecture.
3. **Visual agents** (Claude Computer Use, GPT-4o vision agents) make vision the input layer of autonomous workflows.

This book covers the full arc with code that runs on a 2026 laptop and ships to production.

---

## Repository structure

```
.
├── README.md                       # This file
├── BOOK_OUTLINE.md / .docx / .pdf  # Authoritative 20-chapter outline
├── LESSON_PLANS.md                 # Detailed per-chapter ordered TOCs (defs/concepts/theory/code/notebook cells)
├── WRITING_PLAN.xlsx               # 8-week schedule + daily tracker
├── CHAPTER_TEMPLATE.md             # The structure every chapter follows
├── requirements.txt                # Pinned Python dependencies (Colab-compatible)
├── chapters/                       # One folder per chapter — README + draft prose
│   ├── ch01-landscape/
│   ├── ch02-pixel-ops/
│   ...
│   └── ch20-mlops-future/
├── notebooks/                      # One notebook per chapter (runnable on Colab T4)
├── figures/                        # Generated figures, organized by chapter
├── case-studies/                   # End-to-end production case studies
├── references/
│   ├── published_book_repos.md     # GitHub repos of major CV books to learn from
│   ├── kaggle_resources.md         # Datasets, notebooks, GPU strategy per chapter
│   ├── youtube_and_courses.md      # Curated video courses (Stanford, MIT, Roboflow, ...)
│   └── papers_per_chapter.md       # Canonical papers, organized by chapter
├── kaggle/                         # Kaggle workspace strategy + notebook templates
└── .github/workflows/              # CI: notebook smoke-test, link-check
```

---

## Quick start

```bash
# Clone
git clone https://github.com/<your-username>/computer-vision-book.git
cd computer-vision-book

# Install
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Open a chapter notebook
jupyter lab notebooks/ch01_landscape.ipynb
```

Or one-click on Kaggle: each notebook in `notebooks/` has a Kaggle badge that
opens it in a Kaggle T4 runtime with the dataset pre-attached.

---

## Three-tier compute strategy

| Tier | Use for | Cost |
|---|---|---|
| **Local** (laptop CPU/GPU) | Reading, debugging small models, OpenCV, classical features (Ch 1-4) | Free |
| **Kaggle** (T4 ×2 / P100, 30h/week) | Training/fine-tuning per chapter, all hands-on notebooks | Free |
| **Colab Pro / a paid GPU** | Diffusion fine-tuning (Ch 12), 3DGS (Ch 16), VLA (Ch 17), edge benchmarks (Ch 19) | Paid |

See [`references/kaggle_resources.md`](references/kaggle_resources.md) for the
per-chapter dataset slugs and free-tier strategy.

---

## License

- **Code:** MIT (see `LICENSE`)
- **Prose & figures:** CC BY-NC-SA 4.0

Use the code freely; cite the book if you reuse the prose.

---

## Acknowledgments

This outline draws on Stanford CS231n, MIT 6.S058, Stanford CME296, and the
published-book repos catalogued in [`references/published_book_repos.md`](references/published_book_repos.md).
