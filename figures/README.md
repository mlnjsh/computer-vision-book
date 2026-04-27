# Figures

One subfolder per chapter (`figures/chXX/`). Generated figures are gitignored
(see `.gitignore`); the **source** (Python/Matplotlib script or PNG export
spec) is committed.

Pattern for each figure:

```
figures/ch07/
├── README.md             # list of figures + what they show
├── fig_yolo_evolution.py  # the script that generates it
└── data/                 # tiny inputs needed (if any)
```

To rebuild all figures:

```bash
make figures
# or, per chapter
python figures/ch07/fig_yolo_evolution.py
```

This keeps the repo small while making every figure reproducible.
