# Contributing

This is a single-author book project (Milan Amrut Joshi). Contributions are
welcome in three forms:

## 1. Errata
- Open an issue with the chapter, page/section, and the correction
- Or submit a PR editing the chapter README directly

## 2. Code improvements
- Notebooks must continue to run end-to-end on Kaggle T4 ×2
- Pin dependency versions in the notebook's first cell
- Strip outputs before committing: `nbstripout notebooks/*.ipynb`

## 3. New examples
- A great way to extend a chapter is a new "case study" in `case-studies/chXX/`
- Follow the structure described in `case-studies/README.md`

## Style
- Code: `ruff format`, line length 100
- Prose: practitioner voice, sentence-level edits welcome but please don't
  restructure chapters without discussion (open an issue first)
