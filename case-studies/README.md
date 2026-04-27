# Case Studies

One end-to-end case study per chapter, in `chXX/`. Each case study includes:

- `README.md` — problem statement, success metric, decisions made
- `data/` — pointers to data sources (no raw data committed)
- `train.py` / `eval.py` — runnable scripts, not notebooks
- `serve.py` — minimal serving (FastAPI / Gradio)
- `Dockerfile` — reproducible environment
- `metrics.json` — final metrics for grading

These are the "how does this look in production?" companions to the chapter
notebooks. Notebooks teach; case studies ship.
