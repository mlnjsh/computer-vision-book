# Chapter 18: Domain-Specific Vision: Medical, Autonomous, Geospatial, Agricultural

> **Status:** 📋 Not started  ·  **Target words:** ~3,000  ·  **Hands-on:** Train a domain model in MONAI on a public chest-X-ray dataset and a BEV perception toy example

## Outline (4-5 lines)
Medical imaging (MONAI, nnU-Net, SAM-Med, regulatory considerations), autonomous driving (BEV perception, BEVFormer, lane detection, sensor fusion, nuScenes), satellite/geospatial (Segment Geospatial), and agriculture (DINOv3 + YOLO26 for weed detection — a real 2026 paper).

## Learning Outcomes
*(to be expanded during drafting — list 3-4 concrete things the reader can do after this chapter)*
- [ ]
- [ ]
- [ ]

## Topics Covered
*(replace with bullet list of the section headings you'll write)*
- [ ]

## Hands-On Project
**Train a domain model in MONAI on a public chest-X-ray dataset and a BEV perception toy example**

- Notebook: [`../../notebooks/ch18_domains.ipynb`](../../notebooks/)
- Case study: [`../../case-studies/ch18/`](../../case-studies/)
- Figures: [`../../figures/ch18/`](../../figures/)

## Datasets (Kaggle)
- `nih-chest-xrays/data` — `kaggle datasets download -d nih-chest-xrays/data`
- `kmader/skin-cancer-mnist-ham10000` — `kaggle datasets download -d kmader/skin-cancer-mnist-ham10000`

## Reference GitHub Repos
- https://github.com/Project-MONAI/MONAI
- https://github.com/MIC-DKFZ/nnUNet
- https://github.com/fundamentalvision/BEVFormer
- https://github.com/opengeos/segment-geospatial

## Papers / Reading
*(populated during research phase — add 5-10 canonical papers + 2-3 blog posts)*
- [ ]

## Draft Checklist
- [ ] Outline finalized
- [ ] Notebook runs end-to-end on Colab T4
- [ ] All figures generated and saved to `figures/ch18/`
- [ ] Prose draft (~3,000 words)
- [ ] Code blocks tested and pinned
- [ ] References + further reading section
- [ ] Self-edit pass (clarity, voice consistency)
- [ ] Technical reviewer feedback incorporated
