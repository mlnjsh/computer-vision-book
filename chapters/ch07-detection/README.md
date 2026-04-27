# Chapter 7: Object Detection: From R-CNN to YOLO26 and DETR

> **Status:** 📋 Not started  ·  **Target words:** ~3,000  ·  **Hands-on:** Train YOLO26 on a custom Roboflow dataset and benchmark it against RT-DETR on the same task

> 📘 **Detailed lesson plan:** see [`LESSON.md`](LESSON.md) for the ordered TOC, definitions, theory, notebook cells, and exercises.

## Outline (4-5 lines)
Two-stage (R-CNN family) vs single-stage (SSD, RetinaNet) vs anchor-free (FCOS, CenterNet) vs transformer-based (DETR, DINO-DETR, RT-DETR) vs the YOLO family through YOLOv8/YOLO11/YOLOv12/YOLO26 (NMS-free, end-to-end, edge-friendly).

## Learning Outcomes
*(to be expanded during drafting — list 3-4 concrete things the reader can do after this chapter)*
- [ ]
- [ ]
- [ ]

## Topics Covered
*(replace with bullet list of the section headings you'll write)*
- [ ]

## Hands-On Project
**Train YOLO26 on a custom Roboflow dataset and benchmark it against RT-DETR on the same task**

- Notebook: [`../../notebooks/ch07_detection.ipynb`](../../notebooks/)
- Case study: [`../../case-studies/ch07/`](../../case-studies/)
- Figures: [`../../figures/ch07/`](../../figures/)

## Datasets (Kaggle)
- `awsaf49/coco-2017-dataset` — `kaggle datasets download -d awsaf49/coco-2017-dataset`
- `andrewmvd/dog-and-cat-detection` — `kaggle datasets download -d andrewmvd/dog-and-cat-detection`

## Reference GitHub Repos
- https://github.com/ultralytics/ultralytics
- https://github.com/facebookresearch/detectron2
- https://github.com/lyuwenyu/RT-DETR
- https://github.com/open-mmlab/mmdetection

## Papers / Reading
*(populated during research phase — add 5-10 canonical papers + 2-3 blog posts)*
- [ ]

## Draft Checklist
- [ ] Outline finalized
- [ ] Notebook runs end-to-end on Colab T4
- [ ] All figures generated and saved to `figures/ch07/`
- [ ] Prose draft (~3,000 words)
- [ ] Code blocks tested and pinned
- [ ] References + further reading section
- [ ] Self-edit pass (clarity, voice consistency)
- [ ] Technical reviewer feedback incorporated
