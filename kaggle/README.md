# Kaggle Workspace

Strategy for using Kaggle as the primary compute + dataset host for the book.

## Three uses of Kaggle in this book

1. **Free GPUs** — T4×2 or P100, 30 hrs/week. Covers ~80% of hands-on projects.
2. **Public datasets** — every chapter pins a Kaggle dataset slug for reproducibility.
3. **Public notebooks** — each chapter notebook is also published as a public
   Kaggle notebook (free CDN, audience-building, forces quality).

## Daily workflow

```
local laptop                  Kaggle / Colab
─────────────────             ─────────────────
write prose          ←→       run the notebook
edit notebook        →        push via Kaggle API
                              get GPU minutes used
git commit & push    ←        download trained weights
```

## File layout

```
kaggle/
├── README.md            # this file
├── kernel-metadata/     # one JSON per chapter for `kaggle kernels push`
│   └── ch01.json
└── notebook-template.ipynb
```

## Publishing a notebook to Kaggle

```bash
# One-time
pip install kaggle
mkdir -p ~/.kaggle && cp kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json

# Per notebook
cp notebooks/ch07_detection.ipynb kaggle/staging/kernel-metadata.json # edit fields
kaggle kernels push -p kaggle/staging
```

## Compute budget

See [`../references/kaggle_resources.md`](../references/kaggle_resources.md) for the
per-chapter GPU-hour estimates and which 3 chapters (12, 16, 17) probably need
paid Colab Pro.
