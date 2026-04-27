# Chapter 10: Self-Supervised Vision: From SimCLR to DINOv3

> **Status:** 📋 Not started  ·  **Target words:** ~3,000  ·  **Hands-on:** Use frozen DINOv3 features as a backbone for downstream segmentation with a 90% data reduction vs supervised

## Outline (4-5 lines)
Why labels became the bottleneck. Contrastive (SimCLR, MoCo, BYOL), masked image modeling (MAE, SimMIM), and the DINO line — DINO → DINOv2 → DINOv3 (single frozen backbone outperforms specialists on dense prediction).

## Learning Outcomes
*(to be expanded during drafting — list 3-4 concrete things the reader can do after this chapter)*
- [ ]
- [ ]
- [ ]

## Topics Covered
*(replace with bullet list of the section headings you'll write)*
- [ ]

## Hands-On Project
**Use frozen DINOv3 features as a backbone for downstream segmentation with a 90% data reduction vs supervised**

- Notebook: [`../../notebooks/ch10_self-supervised.ipynb`](../../notebooks/)
- Case study: [`../../case-studies/ch10/`](../../case-studies/)
- Figures: [`../../figures/ch10/`](../../figures/)

## Datasets (Kaggle)
- `mateuszbuda/lgg-mri-segmentation` — `kaggle datasets download -d mateuszbuda/lgg-mri-segmentation`

## Reference GitHub Repos
- https://github.com/facebookresearch/dinov2
- https://github.com/facebookresearch/mae
- https://github.com/facebookresearch/moco-v3

## Papers / Reading
*(populated during research phase — add 5-10 canonical papers + 2-3 blog posts)*
- [ ]

## Draft Checklist
- [ ] Outline finalized
- [ ] Notebook runs end-to-end on Colab T4
- [ ] All figures generated and saved to `figures/ch10/`
- [ ] Prose draft (~3,000 words)
- [ ] Code blocks tested and pinned
- [ ] References + further reading section
- [ ] Self-edit pass (clarity, voice consistency)
- [ ] Technical reviewer feedback incorporated
