# Published Book Repos to Learn From

Curated GitHub repos of well-regarded computer-vision and deep-learning books.
Use these as **references**, not templates — study how they structure code,
explain concepts, and balance theory vs practice.

## Modern Computer Vision (PyTorch-first)

- **Modern Computer Vision with PyTorch (2nd ed., 2024)** — V Kishore Ayyadevara, Yeshwanth Reddy
  https://github.com/PacktPublishing/Modern-Computer-Vision-with-PyTorch-2E
  *Closest in spirit to this book — covers detection, segmentation, GANs, RL, transformers.*

- **Modern Computer Vision with PyTorch (1st ed., 2020)** — same authors
  https://github.com/PacktPublishing/Modern-Computer-Vision-with-PyTorch
  *Older but excellent code organization for chapters and projects.*

- **PyTorch Computer Vision Cookbook** — Michael Avendi
  https://github.com/PacktPublishing/PyTorch-Computer-Vision-Cookbook

- **Deep Learning for Computer Vision (Practitioner's Guide)** — Adrian Rosebrock
  *PyImageSearch — paid, but his free posts at https://pyimagesearch.com are gold*

## Hugging Face / Transformer-Era

- **Natural Language Processing with Transformers** — Tunstall, von Werra, Wolf
  https://github.com/nlp-with-transformers/notebooks
  *NLP-focused but the chapter structure is the gold standard for HF-stack books.*

- **Generative Deep Learning (2nd ed.)** — David Foster
  https://github.com/davidADSP/Generative_Deep_Learning_2nd_Edition
  *GANs, VAEs, diffusion — direct reference for our Ch 12.*

## Foundational ML / Vision

- **Hands-On Machine Learning (3rd ed.)** — Aurélien Géron
  https://github.com/ageron/handson-ml3
  *CV chapters (14, 15, 16) are excellent narrative templates.*

- **Dive into Deep Learning (d2l)** — Zhang, Lipton, Li, Smola
  https://github.com/d2l-ai/d2l-en
  *Open-source book; one of the best CV chapters online.*

- **Practical Machine Learning for Computer Vision (O'Reilly)** — Lakshmanan, Görner, Gillard
  https://github.com/GoogleCloudPlatform/practical-ml-vision-book
  *Production-flavored — useful reference for our Ch 19, 20.*

## Repos that aren't books but read like books

- **LearnOpenCV** — Satya Mallick
  https://github.com/spmallick/learnopencv
  *Hundreds of standalone tutorial notebooks. Best practical CV resource on GitHub.*

- **Microsoft Computer Vision Recipes**
  https://github.com/microsoft/computervision-recipes
  *Production-grade reference implementations for classification, detection, segmentation, action recognition.*

- **Awesome Vision-Language Models**
  https://github.com/gokayfem/awesome-vlm-architectures
  *Living survey of VLM architectures — keep up to date with our Ch 13.*

- **Awesome Embodied VLA / VLN**
  https://github.com/jonyzhang2023/awesome-embodied-vla-va-vln
  *Curated SOTA for our Ch 17.*

## Frontier model repos (study the official implementations)

- **DINOv2 / DINOv3** — https://github.com/facebookresearch/dinov2
- **SAM 2** — https://github.com/facebookresearch/segment-anything-2
- **Grounded SAM 2** — https://github.com/IDEA-Research/Grounded-SAM-2
- **Ultralytics YOLO (8/11/12/26)** — https://github.com/ultralytics/ultralytics
- **Hugging Face Diffusers** — https://github.com/huggingface/diffusers
- **OpenVLA** — https://github.com/openvla/openvla
- **Nerfstudio** — https://github.com/nerfstudio-project/nerfstudio
- **3D Gaussian Splatting** — https://github.com/graphdeco-inria/gaussian-splatting

## How to use these

1. **Clone the closest analog** (Modern Computer Vision with PyTorch 2E) and skim its repo structure
2. **Don't copy code** — copy *structure*: how chapters split into files, how notebooks open, how data is organized
3. **For each frontier model**, clone the official repo and run the demo before writing about it
