# Chapter 9: Vision Transformers and Hybrid Architectures

> **Status:** 📋 Not started  ·  **Target words:** ~3,000  ·  **Hands-on:** Train ViT-Small on ImageNette and compare its attention maps to a ResNet-50's class activation maps

> 📘 **Detailed lesson plan:** see [`LESSON.md`](LESSON.md) for the ordered TOC, definitions, theory, notebook cells, and exercises.

## Outline (4-5 lines)
Attention from scratch, then ViT (patches, positional encoding, [CLS] token), DeiT (data-efficient training), Swin (hierarchical + shifted windows), MaxViT, and the new Mamba/SSM-based vision models (VMamba, Vision-Mamba). When transformers beat CNNs and when they lose.

## Learning Outcomes
*(to be expanded during drafting — list 3-4 concrete things the reader can do after this chapter)*
- [ ]
- [ ]
- [ ]

## Topics Covered
*(replace with bullet list of the section headings you'll write)*
- [ ]

## Hands-On Project
**Train ViT-Small on ImageNette and compare its attention maps to a ResNet-50's class activation maps**

- Notebook: [`../../notebooks/ch09_vit.ipynb`](../../notebooks/)
- Case study: [`../../case-studies/ch09/`](../../case-studies/)
- Figures: [`../../figures/ch09/`](../../figures/)

## Datasets (Kaggle)
- `ambityga/imagenet100` — `kaggle datasets download -d ambityga/imagenet100`
- `lukemelas/imagenette` — `kaggle datasets download -d lukemelas/imagenette`

## Reference GitHub Repos
- https://github.com/google-research/vision_transformer
- https://github.com/microsoft/Swin-Transformer
- https://github.com/huggingface/pytorch-image-models

## Papers / Reading
*(populated during research phase — add 5-10 canonical papers + 2-3 blog posts)*
- [ ]

## Draft Checklist
- [ ] Outline finalized
- [ ] Notebook runs end-to-end on Colab T4
- [ ] All figures generated and saved to `figures/ch09/`
- [ ] Prose draft (~3,000 words)
- [ ] Code blocks tested and pinned
- [ ] References + further reading section
- [ ] Self-edit pass (clarity, voice consistency)
- [ ] Technical reviewer feedback incorporated
