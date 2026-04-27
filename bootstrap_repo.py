"""Bootstrap the book repository: chapters/, notebooks/, figures/, case-studies/,
references/, kaggle/, plus README, requirements, .gitignore, LICENSE, and CI.

Run once: python bootstrap_repo.py
Idempotent — safe to re-run; existing files are NOT overwritten unless --force.
"""
import sys, io, os, argparse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

ROOT = Path(__file__).parent.resolve()

# (number, slug, title, outline, hands_on, kaggle_slugs, github_refs)
CHAPTERS = [
    (1, "ch01-landscape", "The 2026 Computer Vision Landscape",
     "A grounded tour of where CV is in 2026: from the OpenCV era to foundation models. Maps the pipeline (acquisition → preprocessing → modeling → deployment), introduces the four eras (classical, CNN, ViT, foundation/multimodal), and frames the rest of the book. Reader leaves with a mental model of when to reach for SIFT vs YOLO vs SAM 3 vs a VLM.",
     "Mental-model diagram + framework benchmark (run YOLO26, SAM 3, CLIP, Claude Vision on the same image)",
     ["awsaf49/coco-2017-dataset"],
     ["ultralytics/ultralytics", "facebookresearch/dinov2", "facebookresearch/segment-anything-2"]),
    (2, "ch02-pixel-ops", "Image Fundamentals and Pixel-Level Operations",
     "Pixels, color spaces (RGB/HSV/LAB/YCbCr), sampling, quantization, histograms, and convolution from first principles. Filtering, denoising, edge detection (Sobel, Canny, Laplacian), thresholding (Otsu, adaptive), and morphology.",
     "Document-cleanup preprocessor in pure OpenCV that survives uneven lighting",
     ["robikscube/textocr-text-extraction-from-images-dataset", "shaunthesheep/microsoft-catsvsdogs-dataset"],
     ["opencv/opencv", "spmallick/learnopencv"]),
    (3, "ch03-classical-features", "Classical Feature Engineering: SIFT, ORB, and Geometry",
     "Why classical features still matter in 2026 (SLAM, panorama, low-data domains). Harris/FAST corners, SIFT/SURF/ORB/BRIEF descriptors, FLANN matching, RANSAC homography, Hough transforms, contour analysis, template matching.",
     "Stitch a multi-image panorama and build a logo-detector with feature matching — no neural networks",
     ["balraj98/stanford-background-dataset"],
     ["opencv/opencv", "colmap/colmap"]),
    (4, "ch04-camera-geometry", "Camera Geometry, Calibration, and Stereo Vision",
     "Pinhole and fisheye camera models, intrinsics/extrinsics, lens distortion, calibration with checkerboards, epipolar geometry, stereo rectification, disparity maps, triangulation. Bridges classical CV to modern depth estimation.",
     "Calibrate a webcam and reconstruct a scene's depth map from a stereo pair using OpenCV's StereoSGBM",
     ["soumikrakshit/kitti-dataset"],
     ["opencv/opencv", "colmap/colmap"]),
    (5, "ch05-cnns", "Convolutional Neural Networks: From LeNet to ConvNeXt",
     "The CNN family tree as a single story: LeNet → AlexNet → VGG → Inception → ResNet → DenseNet → EfficientNet → MobileNet → ConvNeXt. Builds intuition for why each design choice was a real fix to a real problem.",
     "Implement a ResNet-18 from scratch in PyTorch and reproduce a CIFAR-10 result",
     ["valentynsichkar/cifar10-preprocessed", "ambityga/imagenet100"],
     ["pytorch/vision", "huggingface/pytorch-image-models", "facebookresearch/ConvNeXt"]),
    (6, "ch06-training", "Training Modern Vision Models in Practice",
     "The unglamorous-but-decisive chapter: data loaders, Albumentations, mixup/cutmix, label smoothing, optimizers (SGD/AdamW/Lion), schedulers, mixed precision, gradient checkpointing, multi-GPU with PyTorch Lightning, experiment tracking with Weights & Biases.",
     "Fine-tune a timm model on a custom dataset and beat a published baseline through training tricks alone",
     ["andrewmvd/animal-faces", "ambityga/imagenet100"],
     ["huggingface/pytorch-image-models", "albumentations-team/albumentations", "Lightning-AI/pytorch-lightning"]),
    (7, "ch07-detection", "Object Detection: From R-CNN to YOLO26 and DETR",
     "Two-stage (R-CNN family) vs single-stage (SSD, RetinaNet) vs anchor-free (FCOS, CenterNet) vs transformer-based (DETR, DINO-DETR, RT-DETR) vs the YOLO family through YOLOv8/YOLO11/YOLOv12/YOLO26 (NMS-free, end-to-end, edge-friendly).",
     "Train YOLO26 on a custom Roboflow dataset and benchmark it against RT-DETR on the same task",
     ["awsaf49/coco-2017-dataset", "andrewmvd/dog-and-cat-detection"],
     ["ultralytics/ultralytics", "facebookresearch/detectron2", "lyuwenyu/RT-DETR", "open-mmlab/mmdetection"]),
    (8, "ch08-segmentation", "Image Segmentation: U-Net to SAM 3 and Grounding DINO",
     "Semantic vs instance vs panoptic. FCN, U-Net, DeepLab (atrous + ASPP), Mask R-CNN, Mask2Former, then the foundation-model era: SAM 1/2/3 (clicks, boxes, masks, and concepts via text in SAM 3), Grounding DINO + SAM for open-vocabulary segmentation.",
     "Zero-shot 'segment anything I describe' Gradio app with SAM 3 + Grounding DINO",
     ["awsaf49/coco-2017-dataset", "mateuszbuda/lgg-mri-segmentation"],
     ["facebookresearch/segment-anything-2", "IDEA-Research/Grounded-SAM-2", "facebookresearch/Mask2Former"]),
    (9, "ch09-vit", "Vision Transformers and Hybrid Architectures",
     "Attention from scratch, then ViT (patches, positional encoding, [CLS] token), DeiT (data-efficient training), Swin (hierarchical + shifted windows), MaxViT, and the new Mamba/SSM-based vision models (VMamba, Vision-Mamba). When transformers beat CNNs and when they lose.",
     "Train ViT-Small on ImageNette and compare its attention maps to a ResNet-50's class activation maps",
     ["ambityga/imagenet100", "lukemelas/imagenette"],
     ["google-research/vision_transformer", "microsoft/Swin-Transformer", "huggingface/pytorch-image-models"]),
    (10, "ch10-self-supervised", "Self-Supervised Vision: From SimCLR to DINOv3",
     "Why labels became the bottleneck. Contrastive (SimCLR, MoCo, BYOL), masked image modeling (MAE, SimMIM), and the DINO line — DINO → DINOv2 → DINOv3 (single frozen backbone outperforms specialists on dense prediction).",
     "Use frozen DINOv3 features as a backbone for downstream segmentation with a 90% data reduction vs supervised",
     ["mateuszbuda/lgg-mri-segmentation"],
     ["facebookresearch/dinov2", "facebookresearch/mae", "facebookresearch/moco-v3"]),
    (11, "ch11-clip", "CLIP and Vision-Language Pretraining",
     "Contrastive language-image pretraining as a paradigm shift. CLIP, OpenCLIP, SigLIP, EVA-CLIP, and the open-vocabulary tasks they unlock: zero-shot classification, image-text retrieval, semantic search, grounded detection. Prompt engineering for vision and FAISS for billion-scale retrieval.",
     "Build a 'search your photo library by natural language' app with CLIP + FAISS that runs on a laptop",
     ["adityajn105/flickr8k", "hsankesara/flickr-image-dataset"],
     ["openai/CLIP", "mlfoundations/open_clip", "facebookresearch/faiss"]),
    (12, "ch12-diffusion", "Generative Vision: GANs, VAEs, and the Diffusion Era",
     "GAN dynamics, VAE latents, then the diffusion takeover: DDPM, score-based models, classifier-free guidance, latent diffusion, Stable Diffusion 3.5, Flux, SDXL, ControlNet, IP-Adapter, LoRA. Practical recipes for inpainting, super-resolution, and style transfer.",
     "Fine-tune SDXL with LoRA on a personal dataset and chain with ControlNet for conditioned generation",
     ["splcher/animefacedataset", "jessicali9530/celeba-dataset"],
     ["huggingface/diffusers", "Stability-AI/StableDiffusion", "lllyasviel/ControlNet", "black-forest-labs/flux"]),
    (13, "ch13-vlm", "Vision-Language Models: The Multimodal Stack",
     "Anatomy of a modern VLM: vision encoder + projector + LLM decoder. LLaVA, Qwen2.5-VL, InternVL, Florence-2/3, Gemma 3 Vision, and the closed frontier (GPT-4o, Claude Vision, Gemini 2.5 Pro). When to fine-tune vs prompt vs use the API.",
     "Chart-and-document Q&A system using the Claude Vision API + a local Qwen2.5-VL fallback",
     ["dansbecker/imagenet-test"],
     ["haotian-liu/LLaVA", "QwenLM/Qwen2.5-VL", "OpenGVLab/InternVL", "anthropics/anthropic-sdk-python"]),
    (14, "ch14-document-ai-agents", "Document AI and Visual Agents",
     "OCR (PaddleOCR, Tesseract, Donut), layout analysis (LayoutLMv3, Doctr), table extraction, structured-output VLMs, and the new visual agent loop: screenshot → reason → click. Walks through Claude Computer Use and OpenAI's vision agent pattern.",
     "Invoice-extraction-to-database pipeline + a simple browser-automation agent driven by vision",
     ["urbikn/sroie-datasetv2", "robikscube/textocr-text-extraction-from-images-dataset"],
     ["PaddlePaddle/PaddleOCR", "microsoft/unilm", "clovaai/donut", "anthropics/anthropic-quickstarts"]),
    (15, "ch15-video", "Video Understanding: Action, Tracking, and VideoMAE",
     "Optical flow (Lucas-Kanade, RAFT), 3D CNNs (I3D, SlowFast), VideoMAE, video-language models. Tracking pipeline: SORT → DeepSORT → ByteTrack → BoT-SORT → SAM 2 for video. Action recognition and video-text retrieval.",
     "Sports-analytics pipeline that detects, tracks, and counts players' actions in a clip",
     ["matteomedioli/youtube8m"],
     ["MCG-NJU/VideoMAE", "ifzhang/ByteTrack", "facebookresearch/segment-anything-2"]),
    (16, "ch16-3d-gaussian-splatting", "3D Vision: Depth, NeRF, and Gaussian Splatting",
     "Monocular depth (MiDaS, Depth Anything v2, Marigold), point clouds (PointNet, PointTransformer), structure-from-motion (COLMAP), NeRF and descendants (Instant-NGP, Mip-NeRF), and 3D Gaussian Splatting — the dominant scene representation for real-time photoreal rendering.",
     "Capture a scene with a phone, train a 3DGS model in Nerfstudio, render a fly-through",
     ["soumikrakshit/kitti-dataset"],
     ["nerfstudio-project/nerfstudio", "graphdeco-inria/gaussian-splatting", "DepthAnything/Depth-Anything-V2", "colmap/colmap"]),
    (17, "ch17-vla-robotics", "Vision-Language-Action Models for Robotics and Embodied AI",
     "The category that didn't exist in 2023 and is now the most exciting in CV. The VLA paradigm (vision encoder + language model + action decoder), RT-1/RT-2, OpenVLA, π0 (diffusion-based continuous control), Helix (Figure AI humanoid), Open X-Embodiment dataset.",
     "Run OpenVLA in simulation on a manipulation task and visualize attention over the scene",
     [],
     ["openvla/openvla", "google-deepmind/open_x_embodiment", "huggingface/lerobot"]),
    (18, "ch18-domains", "Domain-Specific Vision: Medical, Autonomous, Geospatial, Agricultural",
     "Medical imaging (MONAI, nnU-Net, SAM-Med, regulatory considerations), autonomous driving (BEV perception, BEVFormer, lane detection, sensor fusion, nuScenes), satellite/geospatial (Segment Geospatial), and agriculture (DINOv3 + YOLO26 for weed detection — a real 2026 paper).",
     "Train a domain model in MONAI on a public chest-X-ray dataset and a BEV perception toy example",
     ["nih-chest-xrays/data", "kmader/skin-cancer-mnist-ham10000"],
     ["Project-MONAI/MONAI", "MIC-DKFZ/nnUNet", "fundamentalvision/BEVFormer", "opengeos/segment-geospatial"]),
    (19, "ch19-edge-deployment", "Optimization and Edge Deployment",
     "Quantization (PTQ, QAT, INT8, FP16, FP8), pruning, knowledge distillation, ONNX export, runtime engines (ONNX Runtime, TensorRT, OpenVINO, CoreML, TFLite, Triton), edge platforms (Jetson Orin, Raspberry Pi 5 + Hailo, mobile NPUs).",
     "Take YOLO26 from Ch7, quantize to INT8, export to TensorRT, deploy on Jetson Orin Nano with measured latency",
     [],
     ["onnx/onnx", "NVIDIA/TensorRT", "openvinotoolkit/openvino", "triton-inference-server/server"]),
    (20, "ch20-mlops-future", "MLOps, Responsible AI, and the Future of Computer Vision",
     "Data versioning (DVC), label management (Label Studio, Roboflow), active learning, drift detection, model monitoring, A/B testing for vision, CI/CD with MLflow/W&B. Responsible AI: bias auditing, explainability (Grad-CAM, SHAP, Captum), privacy, EU AI Act, C2PA. Closes with a forward-looking section.",
     "End-to-end production capstone: ship the running case-study pipeline as a monitored production service",
     [],
     ["mlflow/mlflow", "iterative/dvc", "HumanSignal/label-studio", "pytorch/captum", "slundberg/shap"]),
]

# (path, content) — top-level files
def chapter_readme(num, slug, title, outline, hands_on, kaggle_slugs, github_refs):
    kaggle_lines = "\n".join(f"- `{k}` — `kaggle datasets download -d {k}`" for k in kaggle_slugs) or "- (no Kaggle dataset for this chapter — uses local/synthetic data)"
    gh_lines = "\n".join(f"- https://github.com/{r}" for r in github_refs)
    return f"""# Chapter {num}: {title}

> **Status:** 📋 Not started  ·  **Target words:** ~3,000  ·  **Hands-on:** {hands_on}

## Outline (4-5 lines)
{outline}

## Learning Outcomes
*(to be expanded during drafting — list 3-4 concrete things the reader can do after this chapter)*
- [ ]
- [ ]
- [ ]

## Topics Covered
*(replace with bullet list of the section headings you'll write)*
- [ ]

## Hands-On Project
**{hands_on}**

- Notebook: [`../../notebooks/ch{num:02d}_{slug.split("-",1)[1]}.ipynb`](../../notebooks/)
- Case study: [`../../case-studies/ch{num:02d}/`](../../case-studies/)
- Figures: [`../../figures/ch{num:02d}/`](../../figures/)

## Datasets (Kaggle)
{kaggle_lines}

## Reference GitHub Repos
{gh_lines}

## Papers / Reading
*(populated during research phase — add 5-10 canonical papers + 2-3 blog posts)*
- [ ]

## Draft Checklist
- [ ] Outline finalized
- [ ] Notebook runs end-to-end on Colab T4
- [ ] All figures generated and saved to `figures/ch{num:02d}/`
- [ ] Prose draft (~3,000 words)
- [ ] Code blocks tested and pinned
- [ ] References + further reading section
- [ ] Self-edit pass (clarity, voice consistency)
- [ ] Technical reviewer feedback incorporated
"""


CHAPTER_TEMPLATE = """# Chapter Template

Every chapter follows this structure. Copy this when starting a new chapter.

## 1. Hook (≈ 200 words)
A concrete real-world problem or surprising result that motivates the chapter.

## 2. Mental Model (≈ 300 words)
The picture the reader should hold in their head before any code.

## 3. Theory You Need to Debug (≈ 600 words)
Just enough math/intuition to reason about failures. Skip rigorous derivations
unless they're load-bearing for understanding the model.

## 4. Code Walkthrough (≈ 1,200 words)
Working code, explained block by block. Notebook is the source of truth — prose
references cells from the notebook in `notebooks/chXX_*.ipynb`.

## 5. Production Note (≈ 300 words)
What changes when this leaves a notebook. Latency, memory, failure modes,
monitoring, common bugs in deployment.

## 6. Exercises (3-5)
- Stretch: extend the project to a new domain
- Diagnostic: break the model in a specific way and explain why
- Synthesis: combine with a previous chapter's technique

## 7. References & Further Reading
- 5-10 canonical papers
- 2-3 blog posts / videos (LearnOpenCV, Stanford CS231n, Two Minute Papers)
- 1-2 GitHub repos to clone and read
"""


README = """# Computer Vision: From Foundations to Frontier (2026)

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
├── BOOK_OUTLINE.md / .docx / .pdf  # Authoritative outline
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
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
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
"""


REQUIREMENTS = """# Pinned dependencies — 2026-04 snapshot
# Each chapter may pin overrides in chapters/chXX-*/requirements.txt if needed.

# Core
numpy>=1.26,<2.2
scipy>=1.13
pandas>=2.2
matplotlib>=3.8
seaborn>=0.13
pillow>=10.3
scikit-image>=0.23
scikit-learn>=1.5
tqdm>=4.66

# Computer vision
opencv-python>=4.10
opencv-contrib-python>=4.10
albumentations>=1.4
imageio>=2.34

# Deep learning core
torch>=2.4
torchvision>=0.19
torchaudio>=2.4
timm>=1.0
pytorch-lightning>=2.3

# Hugging Face stack
transformers>=4.45
diffusers>=0.30
accelerate>=0.34
datasets>=2.20
peft>=0.12
safetensors>=0.4

# Detection / segmentation
ultralytics>=8.3            # YOLO11/12/26
supervision>=0.23           # Roboflow's annotator/IoU/tracker utilities

# CLIP / retrieval
open-clip-torch>=2.26
faiss-cpu>=1.8              # use faiss-gpu if available

# OCR / Document AI
paddleocr>=2.8
pytesseract>=0.3.10

# Experiment tracking
wandb>=0.18
tensorboard>=2.17

# Notebook / app
jupyterlab>=4.2
ipywidgets>=8.1
gradio>=4.40
streamlit>=1.38

# API SDKs
anthropic>=0.34
openai>=1.40

# Utilities
einops>=0.8
rich>=13.7
python-dotenv>=1.0
"""


GITIGNORE = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
env/
build/
dist/
*.egg-info/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Jupyter
.ipynb_checkpoints/
*-checkpoint.ipynb

# Data — never commit raw datasets
data/
datasets/
*.zip
*.tar
*.tar.gz
*.h5
*.npz
!notebooks/data/sample/   # tiny samples allowed for unit-testing notebooks

# Model weights — never commit large binaries
*.pt
*.pth
*.ckpt
*.safetensors
*.onnx
*.bin
weights/
checkpoints/

# Generated figures (keep source, regenerate)
figures/**/*.png
figures/**/*.jpg
figures/**/*.svg
!figures/**/README.md

# IDE
.idea/
.vscode/
*.swp
.DS_Store

# Env / secrets
.env
.env.*
!.env.example
*.pem
kaggle.json

# Logs
logs/
*.log
wandb/
mlruns/

# OS
Thumbs.db
ehthumbs.db

# Build artifacts of the book itself
_build/
*.aux
*.toc
*.out
"""


LICENSE = """MIT License

Copyright (c) 2026 Milan Amrut Joshi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

---

The PROSE and FIGURES of this book are licensed separately under
CC BY-NC-SA 4.0. See https://creativecommons.org/licenses/by-nc-sa/4.0/
"""


PUBLISHED_BOOK_REPOS = """# Published Book Repos to Learn From

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
"""


KAGGLE_RESOURCES = """# Kaggle Resources

Free GPU strategy for the entire book — Kaggle's T4×2 / P100 with 30 hrs/week
free is enough for ~80% of the hands-on projects.

## Setup (one-time)

1. Generate API token: kaggle.com → Account → Create New API Token → save `kaggle.json`
2. Place in `~/.kaggle/kaggle.json` (Linux/Mac) or `C:\\Users\\<you>\\.kaggle\\kaggle.json` (Windows)
3. `chmod 600 ~/.kaggle/kaggle.json`
4. Test: `kaggle datasets list`

## Per-chapter dataset slugs

| Ch | Project | Kaggle slug |
|---|---|---|
| 1 | Landscape benchmark | `awsaf49/coco-2017-dataset` |
| 2 | Document cleanup | `robikscube/textocr-text-extraction-from-images-dataset` |
| 3 | Panorama / logo detection | `balraj98/stanford-background-dataset` |
| 4 | Stereo / depth | `soumikrakshit/kitti-dataset` |
| 5 | ResNet-18 on CIFAR | `valentynsichkar/cifar10-preprocessed` |
| 6 | Training tricks | `andrewmvd/animal-faces` |
| 7 | YOLO26 vs RT-DETR | `andrewmvd/dog-and-cat-detection` |
| 8 | SAM 3 + Grounding DINO | `mateuszbuda/lgg-mri-segmentation` |
| 9 | ViT vs ResNet attention | `lukemelas/imagenette` |
| 10 | DINOv3 frozen backbone | `mateuszbuda/lgg-mri-segmentation` |
| 11 | CLIP photo search | `adityajn105/flickr8k` |
| 12 | SDXL LoRA fine-tune | `splcher/animefacedataset` |
| 13 | VLM doc Q&A | (use Anthropic-provided sample charts) |
| 14 | Document AI / agent | `urbikn/sroie-datasetv2` |
| 15 | Sports analytics | (YouTube-8M sample / your own clip) |
| 16 | 3DGS fly-through | `soumikrakshit/kitti-dataset` |
| 17 | OpenVLA simulation | (uses Open X-Embodiment from HF Hub) |
| 18 | Medical imaging | `nih-chest-xrays/data` |
| 19 | Edge deployment | (uses Ch7 weights — no separate dataset) |
| 20 | MLOps capstone | (combines Ch7 + Ch11 datasets) |

## Per-chapter notebook strategy

Each chapter notebook lives in `../notebooks/chXX_*.ipynb` and includes:

```python
# Cell 1 — Kaggle / Colab detection + dataset download
import os
IS_KAGGLE = os.path.exists('/kaggle')
IS_COLAB = 'google.colab' in str(get_ipython())

if IS_KAGGLE:
    DATA = '/kaggle/input/<dataset-slug>'
elif IS_COLAB:
    !pip install kaggle -q
    !mkdir -p ~/.kaggle && cp /content/drive/MyDrive/kaggle.json ~/.kaggle/
    !kaggle datasets download -d <dataset-slug> -p /content/data --unzip
    DATA = '/content/data'
else:
    DATA = '../data'
```

## Free-tier budget per chapter (T4×2)

| Difficulty | Ch | Approx GPU hrs |
|---|---|---|
| ⭐ | 1, 2, 3 | <1 hr |
| ⭐⭐ | 4, 5, 6, 11 | 1-2 hrs |
| ⭐⭐⭐ | 7, 8, 9, 13, 14, 18 | 2-4 hrs |
| ⭐⭐⭐⭐ | 10, 15, 19 | 4-6 hrs |
| ⭐⭐⭐⭐⭐ | 12, 16, 17 | 6+ hrs (may need Colab Pro) |

Total estimated GPU time: ~70 hrs across 20 chapters → fits in ~3 weeks of
Kaggle's 30 hrs/week allotment.

## Publish notebooks back to Kaggle

For each chapter, after the notebook runs, publish it to Kaggle as a public
notebook. This:
- Doubles as a free CDN for the book's Colab links
- Builds an audience before the book launches
- Forces notebook quality (Kaggle's review surfaces issues)

Workflow:
```bash
kaggle kernels init -p notebooks/ch01_landscape.ipynb
# edit kernel-metadata.json: title, slug, gpu, datasets
kaggle kernels push -p notebooks/
```
"""


YOUTUBE_AND_COURSES = """# YouTube Courses and Online Resources

## University courses (free, current 2026)

| Course | Institution | Why it matters |
|---|---|---|
| [CS231n — Deep Learning for Computer Vision](https://cs231n.stanford.edu/) | Stanford (Spring 2026) | The canonical CV course. Lectures on YouTube. |
| [CME296 — Diffusion & Large Vision Models](https://www.youtube.com/watch?v=tr-CUpw--ck) | Stanford (Spring 2026) | Direct reference for our Ch 12. |
| [6.S058 — Introduction to Computer Vision](https://introtocv.github.io/) | MIT (Spring 2026) | Modern overview, ViT-aware. |
| [6.7960 — Deep Learning](https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/) | MIT | Strong transformer treatment. |
| [Foundations of Computer Vision](https://visionbook.mit.edu/) | MIT (free book) | Excellent reference for chapter structure. |
| [CSE493G1 — Deep Learning for CV](https://courses.cs.washington.edu/courses/cse493g1/) | UW (Spring 2026) | Project-heavy CS231n alternative. |

## YouTube channels

| Channel | Why subscribe |
|---|---|
| [Stanford Online](https://www.youtube.com/@stanfordonline) | CS231n lecture playlists |
| [LearnOpenCV](https://www.youtube.com/@LearnOpenCV) | Practical CV tutorials, modern models |
| [Roboflow](https://www.youtube.com/@Roboflow) | Hands-on detection/segmentation walkthroughs |
| [Two Minute Papers](https://www.youtube.com/@TwoMinutePapers) | Stay current on releases |
| [Yannic Kilcher](https://www.youtube.com/@YannicKilcher) | Deep paper walkthroughs |
| [3Blue1Brown](https://www.youtube.com/@3blue1brown) | Math intuition |
| [DeepFindr](https://www.youtube.com/@DeepFindr) | Diffusion model deep dives |

## Roboflow / OpenCV / Hugging Face official courses

- [Roboflow Computer Vision Course](https://blog.roboflow.com/best-computer-vision-courses/)
- [OpenCV University](https://opencv.org/courses/)
- [Hugging Face Computer Vision Course](https://huggingface.co/learn/computer-vision-course)
- [Hugging Face Diffusion Course](https://huggingface.co/learn/diffusion-course)

## Per-chapter video pairings

| Ch | Lecture/video pairing |
|---|---|
| 1 | CS231n L1 (overview) + Two Minute Papers SAM 3 review |
| 2-4 | LearnOpenCV classical tutorials |
| 5 | CS231n L5-L9 (CNN evolution) |
| 6 | fast.ai Practical DL Lesson 5-7 |
| 7 | Roboflow YOLO26 walkthrough + Yannic on RT-DETR |
| 8 | LearnOpenCV SAM 2/3 + Roboflow Grounded SAM |
| 9 | CS231n L11 (Transformers) |
| 10 | Yannic on DINOv2/v3 |
| 11 | Yannic on CLIP |
| 12 | CME296 lecture series (the entire course) |
| 13 | LearnOpenCV LLaVA + Anthropic Vision API tutorials |
| 14 | Anthropic Computer Use demos |
| 15 | LearnOpenCV ByteTrack + SAM 2 video |
| 16 | LearnOpenCV 3DGS + Two Minute Papers Gaussian Splatting |
| 17 | Yannic on RT-2 / OpenVLA |
| 18 | MONAI tutorials |
| 19 | NVIDIA DLI Jetson tutorials |
| 20 | Made With ML MLOps course |
"""


PAPERS_PER_CHAPTER = """# Papers Per Chapter

Canonical papers to cite in each chapter. Aim for 5-10 per chapter; the
critical ones are starred (★).

## Ch 1 — Landscape
- ★ A ConvNet for the 2020s (ConvNeXt) — Liu et al. 2022
- ★ An Image is Worth 16x16 Words (ViT) — Dosovitskiy et al. 2021
- ★ Segment Anything (SAM) — Kirillov et al. 2023

## Ch 2 — Pixel ops
- A Computational Approach to Edge Detection — Canny 1986
- Bilateral Filtering for Gray and Color Images — Tomasi & Manduchi 1998

## Ch 3 — Classical features
- ★ Distinctive Image Features from Scale-Invariant Keypoints (SIFT) — Lowe 2004
- ORB: an efficient alternative to SIFT or SURF — Rublee et al. 2011
- Random Sample Consensus (RANSAC) — Fischler & Bolles 1981

## Ch 4 — Camera geometry
- Multiple View Geometry in Computer Vision — Hartley & Zisserman (book)
- A Flexible New Technique for Camera Calibration — Zhang 2000

## Ch 5 — CNNs
- ★ Gradient-Based Learning Applied to Document Recognition (LeNet) — LeCun 1998
- ★ ImageNet Classification with Deep CNNs (AlexNet) — Krizhevsky 2012
- ★ Deep Residual Learning (ResNet) — He et al. 2016
- A ConvNet for the 2020s (ConvNeXt) — Liu et al. 2022
- EfficientNet — Tan & Le 2019

## Ch 6 — Training
- ★ Adam — Kingma & Ba 2015
- AdamW — Loshchilov & Hutter 2019
- Mixup — Zhang et al. 2018
- Cutmix — Yun et al. 2019
- Bag of Tricks — He et al. 2019

## Ch 7 — Detection
- ★ Faster R-CNN — Ren et al. 2015
- ★ YOLOv3 — Redmon & Farhadi 2018
- ★ DETR — Carion et al. 2020
- RT-DETR — Lyu et al. 2023
- YOLO26 (Ultralytics technical report 2025)

## Ch 8 — Segmentation
- ★ U-Net — Ronneberger et al. 2015
- ★ Mask R-CNN — He et al. 2017
- DeepLab v3+ — Chen et al. 2018
- Mask2Former — Cheng et al. 2022
- ★ SAM 2 — Ravi et al. 2024
- SAM 3 (Meta tech report 2025)
- Grounding DINO — Liu et al. 2023

## Ch 9 — ViT
- ★ ViT — Dosovitskiy et al. 2021
- DeiT — Touvron et al. 2021
- Swin — Liu et al. 2021
- Vision Mamba — Zhu et al. 2024

## Ch 10 — Self-supervised
- ★ SimCLR — Chen et al. 2020
- BYOL — Grill et al. 2020
- MAE — He et al. 2022
- ★ DINOv2 — Oquab et al. 2024
- DINOv3 — Meta 2025

## Ch 11 — CLIP
- ★ Learning Transferable Visual Models from Natural Language Supervision (CLIP) — Radford et al. 2021
- SigLIP — Zhai et al. 2023
- EVA-CLIP — Sun et al. 2023

## Ch 12 — Diffusion
- ★ DDPM — Ho et al. 2020
- ★ Latent Diffusion (Stable Diffusion) — Rombach et al. 2022
- Classifier-Free Guidance — Ho & Salimans 2022
- ControlNet — Zhang et al. 2023
- LoRA — Hu et al. 2021
- SDXL — Podell et al. 2023

## Ch 13 — VLMs
- ★ LLaVA — Liu et al. 2023
- Florence-2 — Xiao et al. 2024
- InternVL 2 — Chen et al. 2024
- Qwen2.5-VL — Alibaba 2025
- Anthropic Vision API technical notes

## Ch 14 — Document AI
- ★ LayoutLMv3 — Huang et al. 2022
- Donut — Kim et al. 2022
- PaddleOCR technical report

## Ch 15 — Video
- ★ I3D — Carreira & Zisserman 2017
- SlowFast — Feichtenhofer et al. 2019
- VideoMAE — Tong et al. 2022
- ByteTrack — Zhang et al. 2022

## Ch 16 — 3D
- ★ NeRF — Mildenhall et al. 2020
- Instant-NGP — Müller et al. 2022
- ★ 3D Gaussian Splatting — Kerbl et al. 2023
- Depth Anything v2 — Yang et al. 2024

## Ch 17 — VLA
- ★ RT-2 — Brohan et al. 2023
- ★ OpenVLA — Kim et al. 2024
- π0 — Black et al. 2024 (Physical Intelligence)
- Helix — Figure AI 2025

## Ch 18 — Domains
- ★ nnU-Net — Isensee et al. 2021
- BEVFormer — Li et al. 2022
- DINOv3 + YOLO26 for Weed Detection (arXiv 2603.00160)

## Ch 19 — Edge
- Quantization-Aware Training — Jacob et al. 2018
- Knowledge Distillation — Hinton et al. 2015
- TensorRT technical documentation

## Ch 20 — MLOps / Responsible AI
- Hidden Technical Debt in ML Systems — Sculley et al. 2015
- ★ Grad-CAM — Selvaraju et al. 2017
- Datasheets for Datasets — Gebru et al. 2018
- Model Cards for Model Reporting — Mitchell et al. 2019
"""


KAGGLE_README = """# Kaggle Workspace

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
"""


CI_WORKFLOW = """name: smoke-test

on:
  pull_request:
    paths:
      - 'notebooks/**'
      - 'requirements.txt'
  push:
    branches: [main]
    paths:
      - 'notebooks/**'
      - 'requirements.txt'

jobs:
  lint-notebooks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
      - name: Install lint tools
        run: |
          pip install nbqa ruff nbstripout
      - name: Strip outputs (notebooks should be committed without outputs)
        run: |
          find notebooks -name '*.ipynb' -print0 | xargs -0 -I {} nbstripout --check {}
      - name: Ruff on notebook code cells
        run: |
          nbqa ruff notebooks/ --select=E,F,W --ignore=E501
"""


CASE_STUDIES_README = """# Case Studies

One end-to-end case study per chapter, in `chXX/`. Each case study includes:

- `README.md` — problem statement, success metric, decisions made
- `data/` — pointers to data sources (no raw data committed)
- `train.py` / `eval.py` — runnable scripts, not notebooks
- `serve.py` — minimal serving (FastAPI / Gradio)
- `Dockerfile` — reproducible environment
- `metrics.json` — final metrics for grading

These are the "how does this look in production?" companions to the chapter
notebooks. Notebooks teach; case studies ship.
"""


FIGURES_README = """# Figures

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
"""


NOTEBOOKS_README = """# Notebooks

One Jupyter notebook per chapter, named `chXX_<slug>.ipynb`. Every notebook:

1. Detects Kaggle / Colab / local and downloads the right dataset
2. Pins library versions in the first cell
3. Runs end-to-end on a Kaggle T4 ×2 in < 30 minutes (exceptions noted in chapter README)
4. Saves figures to `../figures/chXX/`
5. Saves trained weights / artifacts to a local `weights/` (gitignored)

Notebook list:

| Ch | Notebook | GPU hrs (est) |
|---|---|---|
| 1  | ch01_landscape.ipynb              | <1 |
| 2  | ch02_pixel_ops.ipynb              | <1 |
| 3  | ch03_classical_features.ipynb     | <1 |
| 4  | ch04_camera_geometry.ipynb        | 1 |
| 5  | ch05_cnns.ipynb                   | 1 |
| 6  | ch06_training.ipynb               | 2 |
| 7  | ch07_detection.ipynb              | 3 |
| 8  | ch08_segmentation.ipynb           | 2 |
| 9  | ch09_vit.ipynb                    | 2 |
| 10 | ch10_self_supervised.ipynb        | 4 |
| 11 | ch11_clip.ipynb                   | 1 |
| 12 | ch12_diffusion.ipynb              | 6+ (Colab Pro) |
| 13 | ch13_vlm.ipynb                    | API only |
| 14 | ch14_document_ai_agents.ipynb     | 2 |
| 15 | ch15_video.ipynb                  | 4 |
| 16 | ch16_3d_gaussian_splatting.ipynb  | 6+ (Colab Pro) |
| 17 | ch17_vla_robotics.ipynb           | 6+ (Colab Pro) |
| 18 | ch18_domains.ipynb                | 3 |
| 19 | ch19_edge_deployment.ipynb        | 2 + edge device |
| 20 | ch20_mlops_capstone.ipynb         | 2 |

Total: ~50 GPU-hours across 20 chapters.
"""


CONTRIBUTING = """# Contributing

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
"""


def write(path: Path, content: str, force=False):
    if path.exists() and not force:
        print(f'  skip (exists): {path.relative_to(ROOT)}')
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    print(f'  wrote: {path.relative_to(ROOT)}')
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--force', action='store_true', help='Overwrite existing files')
    args = p.parse_args()
    force = args.force

    print('Bootstrapping repo at', ROOT)
    print()

    # Top-level files
    write(ROOT / 'README.md', README, force)
    write(ROOT / 'CHAPTER_TEMPLATE.md', CHAPTER_TEMPLATE, force)
    write(ROOT / 'requirements.txt', REQUIREMENTS, force)
    write(ROOT / '.gitignore', GITIGNORE, force)
    write(ROOT / 'LICENSE', LICENSE, force)
    write(ROOT / 'CONTRIBUTING.md', CONTRIBUTING, force)

    # references/
    write(ROOT / 'references' / 'published_book_repos.md', PUBLISHED_BOOK_REPOS, force)
    write(ROOT / 'references' / 'kaggle_resources.md', KAGGLE_RESOURCES, force)
    write(ROOT / 'references' / 'youtube_and_courses.md', YOUTUBE_AND_COURSES, force)
    write(ROOT / 'references' / 'papers_per_chapter.md', PAPERS_PER_CHAPTER, force)

    # kaggle/
    write(ROOT / 'kaggle' / 'README.md', KAGGLE_README, force)

    # CI
    write(ROOT / '.github' / 'workflows' / 'smoke-test.yml', CI_WORKFLOW, force)

    # Top-level READMEs for the four required directories
    write(ROOT / 'notebooks' / 'README.md', NOTEBOOKS_README, force)
    write(ROOT / 'figures' / 'README.md', FIGURES_README, force)
    write(ROOT / 'case-studies' / 'README.md', CASE_STUDIES_README, force)

    # Chapter folders + READMEs + figures/chXX + case-studies/chXX
    for num, slug, title, outline, hands_on, kaggle_slugs, github_refs in CHAPTERS:
        ch_dir = ROOT / 'chapters' / slug
        write(ch_dir / 'README.md',
              chapter_readme(num, slug, title, outline, hands_on, kaggle_slugs, github_refs),
              force)
        # Per-chapter figures placeholder
        write(ROOT / 'figures' / f'ch{num:02d}' / 'README.md',
              f'# Figures — Chapter {num}: {title}\n\n*(populate with `fig_*.py` scripts during drafting)*\n',
              force)
        # Per-chapter case-study placeholder
        write(ROOT / 'case-studies' / f'ch{num:02d}' / 'README.md',
              f'# Case Study — Chapter {num}: {title}\n\n**Hands-on:** {hands_on}\n\n*(populate during drafting; see ../README.md for structure)*\n',
              force)

    print()
    print(f'✓ Bootstrapped {len(CHAPTERS)} chapter folders + scaffolding.')
    print()
    print('Next steps:')
    print('  1. git init && git add . && git commit -m "Bootstrap book repo"')
    print('  2. gh repo create computer-vision-book --public --source=. --push')


if __name__ == '__main__':
    main()
