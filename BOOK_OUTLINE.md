# Computer Vision: From Foundations to Frontier (2026)
## A 20-Chapter Modern Book — Outline & Writing Plan

**Author:** Milan Amrut Joshi
**Target length:** ~60,000 words / ~280 pages / ~3,000 words per chapter
**Companion:** GitHub repo with one runnable Colab notebook + one production case study per chapter
**Stack defaults:** Python 3.12, PyTorch 2.x, Hugging Face, Ultralytics, OpenCV, ONNX/TensorRT
**Positioning:** Practitioner-first. Theory deep enough to debug. Every chapter ends in working code.

---

## Why this book, why now

By 2026 the CV landscape has structurally shifted three ways most existing books miss:
1. **Frozen foundation backbones** (DINOv3, SAM 3) replace task-specific training for most use cases.
2. **Vision-Language-Action models** (RT-2, OpenVLA, π0, Helix) collapse perception + reasoning + control into one architecture.
3. **Visual agents** (Claude Computer Use, GPT-4o vision agents) make vision the input layer of autonomous workflows.

This book covers the full arc — classical → CNN → ViT → foundation models → multimodal → embodied — with code that runs on a 2026 laptop and ships to production.

---

## Table of Contents

### Part I — Foundations (Chapters 1–4)

**Chapter 1 — The 2026 Computer Vision Landscape**
A grounded tour of where CV is in 2026: from the OpenCV era to foundation models. Maps the pipeline (acquisition → preprocessing → modeling → deployment), introduces the four eras (classical, CNN, ViT, foundation/multimodal), and frames the rest of the book. Reader leaves with a mental model of when to reach for SIFT vs YOLO vs SAM 3 vs a VLM, and sets up the running case-study dataset used through the book.

**Chapter 2 — Image Fundamentals and Pixel-Level Operations**
Pixels, color spaces (RGB/HSV/LAB/YCbCr), sampling, quantization, histograms, and convolution from first principles. Covers filtering, blurring, sharpening, denoising (Gaussian, bilateral, non-local means), edge detection (Sobel, Canny, Laplacian), thresholding (Otsu, adaptive), and morphology. Hands-on: build a document-cleanup preprocessor in pure OpenCV that survives uneven lighting.

**Chapter 3 — Classical Feature Engineering: SIFT, ORB, and Geometry**
Why classical features still matter in 2026 (SLAM, panorama, low-data domains). Covers Harris/FAST corners, SIFT/SURF/ORB/BRIEF descriptors, FLANN matching, RANSAC homography, Hough transforms, contour analysis, and template matching. Hands-on: stitch a multi-image panorama and build a logo-detector with feature matching — no neural networks.

**Chapter 4 — Camera Geometry, Calibration, and Stereo Vision**
Pinhole and fisheye camera models, intrinsics/extrinsics, lens distortion, calibration with checkerboards, epipolar geometry, stereo rectification, disparity maps, and the math of triangulation. Bridges classical CV to modern depth estimation. Hands-on: calibrate a webcam and reconstruct a scene's depth map from a stereo pair using OpenCV's StereoSGBM.

---

### Part II — Deep Learning for Vision (Chapters 5–8)

**Chapter 5 — Convolutional Neural Networks: From LeNet to ConvNeXt**
The CNN family tree as a single story: LeNet → AlexNet → VGG → Inception → ResNet → DenseNet → EfficientNet → MobileNet → ConvNeXt. Builds intuition for why each design choice (skip connections, bottleneck blocks, depthwise separables, modern normalizations) was a real fix to a real problem. Hands-on: implement a ResNet-18 from scratch in PyTorch and reproduce a CIFAR-10 result.

**Chapter 6 — Training Modern Vision Models in Practice**
The unglamorous-but-decisive chapter: data loaders, Albumentations augmentation pipelines, mixup/cutmix, label smoothing, optimizers (SGD vs AdamW vs Lion), schedulers (cosine, one-cycle), mixed precision, gradient checkpointing, multi-GPU with PyTorch Lightning, and experiment tracking with Weights & Biases. Hands-on: fine-tune a timm model on a custom dataset and beat a published baseline through training tricks alone.

**Chapter 7 — Object Detection: From R-CNN to YOLO26 and DETR**
Two-stage (R-CNN, Fast/Faster R-CNN) vs single-stage (SSD, RetinaNet, focal loss) vs anchor-free (FCOS, CenterNet) vs transformer-based (DETR, DINO-DETR, RT-DETR) vs the YOLO family through YOLOv8/YOLO11/YOLOv12/YOLO26 (NMS-free, end-to-end, edge-friendly). Covers mAP/IoU/PR-curve evaluation honestly. Hands-on: train YOLO26 on a custom Roboflow dataset and benchmark it against RT-DETR on the same task.

**Chapter 8 — Image Segmentation: U-Net to SAM 3 and Grounding DINO**
Semantic vs instance vs panoptic segmentation. Walks through FCN, U-Net, DeepLab (atrous + ASPP), Mask R-CNN, Mask2Former, then jumps to the foundation-model era: SAM 1/2/3 (clicks, boxes, masks, **and concepts via text in SAM 3**), Grounding DINO + SAM for open-vocabulary segmentation. Hands-on: build a zero-shot "segment anything I describe" pipeline with SAM 3 + Grounding DINO and deploy it as a Gradio app.

---

### Part III — Modern Architectures and Foundation Models (Chapters 9–12)

**Chapter 9 — Vision Transformers and Hybrid Architectures**
Attention from scratch, then ViT (patches, positional encoding, [CLS] token), DeiT (data-efficient training), Swin (hierarchical + shifted windows), MaxViT, and the new Mamba/SSM-based vision models (VMamba, Vision-Mamba). Discusses when transformers beat CNNs (data-rich, large-context) and when they lose (small-data, latency-sensitive). Hands-on: train a ViT-Small on ImageNette and compare its attention maps to a ResNet-50's class activation maps.

**Chapter 10 — Self-Supervised Vision: From SimCLR to DINOv3**
Why labels became the bottleneck and how self-supervision broke it. Covers contrastive (SimCLR, MoCo, BYOL), masked image modeling (MAE, SimMIM), and the DINO line (DINO → DINOv2 → **DINOv3**, the 2025 model where a single frozen backbone outperforms specialists on dense prediction). Hands-on: extract DINOv3 features and use them as a frozen backbone for a downstream segmentation task with a 90% data reduction vs supervised baseline.

**Chapter 11 — CLIP and Vision-Language Pretraining**
Contrastive language-image pretraining as a paradigm shift. Walks through CLIP, OpenCLIP, SigLIP, EVA-CLIP, and the open-vocabulary tasks they unlock: zero-shot classification, image-text retrieval, semantic search, and grounded detection. Covers prompt engineering for vision (templates, ensembles) and FAISS for billion-scale retrieval. Hands-on: build a "search your photo library by natural language" app with CLIP + FAISS that runs on a laptop.

**Chapter 12 — Generative Vision: GANs, VAEs, and the Diffusion Era**
GAN dynamics (mode collapse, Wasserstein loss), the VAE latent space, then the diffusion takeover: DDPM, score-based models, classifier-free guidance, latent diffusion, **Stable Diffusion 3.5, Flux, SDXL**, ControlNet, IP-Adapter, and LoRA fine-tuning. Practical recipes for inpainting, super-resolution, and style transfer that ship to production. Hands-on: fine-tune SDXL with LoRA on a personal dataset and chain it with ControlNet for conditioned generation.

---

### Part IV — Multimodal, Video, and 3D (Chapters 13–16)

**Chapter 13 — Vision-Language Models: The Multimodal Stack**
Anatomy of a modern VLM: vision encoder + projector + LLM decoder. Covers LLaVA, Qwen2.5-VL, InternVL, **Florence-2 / Florence-3**, Gemma 3 Vision, and the closed frontier (GPT-4o, **Claude Vision (Sonnet 4.6, Opus 4.7)**, Gemini 2.5 Pro). When to fine-tune vs prompt vs use the API. Honest cost/latency/accuracy comparison table. Hands-on: build a chart-and-document Q&A system using the Claude Vision API + a local Qwen2.5-VL fallback.

**Chapter 14 — Document AI and Visual Agents**
The most underrated commercial CV application in 2026. Covers OCR (PaddleOCR, Tesseract, Donut), layout analysis (LayoutLMv3, Doctr), table extraction, structured-output VLMs, and the new visual agent loop: screenshot → reason → click. Walks through Claude Computer Use and OpenAI's vision agent pattern. Hands-on: build an invoice-extraction-to-database pipeline and a simple browser-automation agent driven by vision.

**Chapter 15 — Video Understanding: Action, Tracking, and VideoMAE**
Temporal modeling: optical flow (Lucas-Kanade, RAFT), 3D CNNs (I3D, SlowFast), VideoMAE, video-language models. Tracking pipeline: SORT → DeepSORT → ByteTrack → BoT-SORT → SAM 2 for video. Action recognition, temporal action detection, and video-text retrieval. Hands-on: build a sports-analytics pipeline that detects, tracks, and counts players' actions in a clip.

**Chapter 16 — 3D Vision: Depth, NeRF, and Gaussian Splatting**
Monocular depth (MiDaS, Depth Anything v2, Marigold), point clouds (PointNet, PointTransformer), structure-from-motion (COLMAP), NeRF and its descendants (Instant-NGP, Mip-NeRF), and **3D Gaussian Splatting** — the 2024-2026 dominant scene representation for real-time photoreal rendering. Bridges to SLAM and AR/VR. Hands-on: capture a scene with a phone, train a 3DGS model in Nerfstudio, and render a fly-through.

---

### Part V — Frontiers and Production (Chapters 17–20)

**Chapter 17 — Vision-Language-Action Models for Robotics and Embodied AI**
The category that didn't exist in 2023 and is now the most exciting in CV. Covers the VLA paradigm (vision encoder + language model + action decoder), RT-1/RT-2, **OpenVLA**, **π0** (Pi-Zero, diffusion-based continuous control), **Helix** (Figure AI humanoid), and the Open X-Embodiment dataset. Discusses the pose estimation stack (OpenPose, MediaPipe, SMPL) as the bridge from pixels to actions. Hands-on: run OpenVLA in simulation on a manipulation task and visualize its attention over the scene.

**Chapter 18 — Domain-Specific Vision: Medical, Autonomous, Geospatial, Agricultural**
How CV is applied where it actually generates revenue. Medical imaging (MONAI, nnU-Net, SAM-Med, regulatory considerations), autonomous driving (BEV perception, BEVFormer, lane detection, sensor fusion, nuScenes), satellite/geospatial (Segment Geospatial, foundation models for Earth observation), and agriculture (DINOv3 + YOLO26 for weed detection — a real 2026 paper). Hands-on: train a domain model in MONAI on a public chest-X-ray dataset and a BEV perception toy example.

**Chapter 19 — Optimization and Edge Deployment**
Making models run fast on real hardware. Quantization (PTQ, QAT, INT8, FP16, FP8), pruning (structured/unstructured), knowledge distillation, ONNX export, runtime engines (ONNX Runtime, TensorRT, OpenVINO, Apple CoreML, TFLite, NVIDIA Triton), and edge platforms (Jetson Orin, Raspberry Pi 5 + Hailo, mobile NPUs). Honest benchmarks across the stack. Hands-on: take the YOLO26 from Chapter 7, quantize to INT8, export to TensorRT, and deploy on a Jetson Orin Nano with measured latency.

**Chapter 20 — MLOps, Responsible AI, and the Future of Computer Vision**
The end-to-end production loop: data versioning (DVC), label management (Label Studio, Roboflow), active learning, drift detection, model monitoring, A/B testing for vision, CI/CD with MLflow/W&B. Responsible AI: bias auditing, explainability (Grad-CAM, SHAP, Captum), privacy (federated learning, differential privacy for vision), and legal frontiers (EU AI Act, content provenance / C2PA). Closes with a forward-looking section: where CV is heading by 2028 (unified VLA agents, neural rendering as default, on-device foundation models). Capstone: ship the running case-study pipeline end-to-end as a monitored production service.

---

## 2-Month Writing Schedule (8 Weeks, ~3,000 Words/Chapter)

**Assumptions:** ~2 hours of focused writing/day (≈1,500 words on a good day) + 1 hour code/figures, 6 days/week. Each chapter = 2 days draft + 0.5 day code/notebook + 0.5 day figures/edit ≈ 3 working days. 20 chapters × 3 days = 60 working days = 10 weeks at the full quality bar; the 8-week plan below uses parallelism (research one chapter while drafting the previous) to compress.

### Week 0 — Pre-launch (3 days)
- Set up GitHub repo with `chapters/`, `notebooks/`, `figures/`, `case-studies/` directories
- Pick the running case-study dataset that threads through all chapters (recommendation: a multi-domain dataset like Roboflow 100, or pair MS-COCO + a custom domain set)
- Draft a chapter template (intro hook → mental model → theory → code walkthrough → production note → exercises → references)
- Block writing time on the calendar (same hours every day = 90% of the win)

### Week 1 — Part I, the Foundations (4 chapters)
- **Day 1–3:** Ch 1 (Landscape) — lower difficulty, gets the muscle warmed up
- **Day 4–5:** Ch 2 (Pixel ops) — heavy on code, low on theory
- **Day 6:** Catch-up + Ch 3 outline + research

### Week 2 — Finish Part I + start Part II
- **Day 1–3:** Ch 3 (Classical features) — panorama notebook is the hands-on
- **Day 4–6:** Ch 4 (Camera geometry) — math-heavy, do figures early

### Week 3 — Part II, Deep Learning Core (chapters 5–6)
- **Day 1–3:** Ch 5 (CNNs) — implement ResNet-18 notebook first, write around it
- **Day 4–6:** Ch 6 (Training tricks) — your strength domain (Kaggle competition experience), should write fast

### Week 4 — Part II, Detection & Segmentation (chapters 7–8)
- **Day 1–3:** Ch 7 (Detection) — YOLO26 + RT-DETR benchmark notebook
- **Day 4–6:** Ch 8 (Segmentation) — SAM 3 + Grounding DINO Gradio app

**Mid-book milestone (end of Week 4):** Half the book drafted. Take a half-day to skim Chapters 1–8 for voice consistency and make a list of cross-references to weave back in during revision.

### Week 5 — Part III, Modern Architectures (chapters 9–10)
- **Day 1–3:** Ch 9 (ViTs) — attention map figures matter most here
- **Day 4–6:** Ch 10 (Self-supervised, DINOv3) — frozen-backbone notebook

### Week 6 — Part III continued + Part IV starts (chapters 11–13)
- **Day 1–2:** Ch 11 (CLIP) — FAISS retrieval app (relatively quick chapter)
- **Day 3–4:** Ch 12 (Generative/Diffusion) — needs the most figures of any chapter
- **Day 5–6:** Ch 13 (VLMs) — Claude Vision app + Qwen2.5-VL fallback notebook

### Week 7 — Part IV finish + Part V starts (chapters 14–17)
- **Day 1:** Ch 14 (Document AI + Visual Agents) — fast, you've shipped these
- **Day 2–3:** Ch 15 (Video) — sports-analytics demo
- **Day 4–5:** Ch 16 (3D / Gaussian Splatting) — phone-capture-to-NeRF notebook
- **Day 6:** Ch 17 (VLA) outline + research, draft started

### Week 8 — Finish Part V (chapters 17–20) + integration
- **Day 1–2:** Ch 17 (VLA) finish — OpenVLA simulation walkthrough
- **Day 3:** Ch 18 (Domain applications) — leverage your existing work (medical, agriculture from EY, etc.)
- **Day 4:** Ch 19 (Edge deployment) — Jetson Orin benchmarks
- **Day 5:** Ch 20 (MLOps + Future) — capstone integration
- **Day 6:** Cross-chapter pass — fix forward references, deduplicate, tighten transitions

### Week 9 (optional buffer / revision sprint)
- Read the whole manuscript in one sitting (1.5 days)
- Address chapter-level feedback from 2–3 technical reviewers
- Polish figures, code, and references
- Write Preface, "How to Use This Book," and chapter dependency graph

### Daily routine that makes this work
- **Morning (90 min):** drafting prose — no research, no rabbit holes
- **Midday (60 min):** code/notebook for the current chapter
- **Evening (30 min):** outline tomorrow's section + collect 2–3 references — so you start the next morning without blank-page friction

### Risks and mitigations
- **Diffusion (Ch 12), VLA (Ch 17), and 3DGS (Ch 16)** are the technically hardest chapters — schedule them in your peak weeks (5–7), not the last week
- **Code that breaks across library upgrades** — pin every dependency in `requirements.txt` per chapter, snapshot a Colab-compatible environment
- **"Just one more reference" trap** — close research at 30 min for any chapter; what you don't have is footnoted for the revision pass
- **Energy dip in Week 5** is statistically common — pre-block a no-meetings, single-coffee-shop day to break it

---

## Resources Mined for This Outline

### Courses (current 2026)
- Stanford CS231n (Spring 2026) — Deep Learning for Computer Vision
- Stanford CME296 (Spring 2026) — Diffusion & Large Vision Models
- MIT 6.S058 (Spring 2026) — Introduction to Computer Vision
- MIT "Foundations of Computer Vision" (visionbook.mit.edu)
- UW CSE493G1 (Spring 2026) — Deep Learning for Computer Vision

### Books surveyed (2024–2026)
- O'Reilly: Practical Machine Learning for Computer Vision (Lakshmanan et al.)
- O'Reilly: Hands-On Computer Vision with TensorFlow 2
- Packt: Modern Computer Vision with PyTorch (V. Kishore Ayyadevara)
- Springer: Advanced Methods and Deep Learning in Computer Vision

### Modern model references (2025–2026)
- DINOv3 (Meta, 2025) — single frozen backbone for dense prediction
- SAM 3 (Meta, 2025) — concept-promptable segmentation across image+video+text
- YOLO26 (Ultralytics, 2025) — NMS-free end-to-end real-time detection
- Florence-2 / Florence-3 (Microsoft) — unified vision foundation model
- Stable Diffusion 3.5, Flux, SDXL, ControlNet, IP-Adapter
- Claude Vision (Sonnet 4.6, Opus 4.7), GPT-4o, Gemini 2.5 Pro
- OpenVLA, π0, Helix (Figure AI), RT-2 — Vision-Language-Action models
- 3D Gaussian Splatting + Nerfstudio + gsplat
- VLM-3R (CVPR 2026) — VLMs augmented with 3D reconstruction

### YouTube + GitHub
- Stanford CS231n 2025 lecture playlist
- LearnOpenCV (Satya Mallick) — practical tutorials
- Roboflow YouTube — hands-on detection/segmentation walkthroughs
- Two Minute Papers — keep current on releases
- GitHub: kuzand/Computer-Vision-Video-Lectures, gokayfem/awesome-vlm-architectures, jonyzhang2023/awesome-embodied-vla-va-vln, IDEA-Research/Grounded-SAM-2

---

## Open decisions for the author

Three calls that should be made before Week 1 begins, because they cascade through every chapter:

1. **Single framework or both?** PyTorch-only is faster to write and matches modern research; including TensorFlow/Keras doubles code maintenance but widens the audience. Recommended: PyTorch-only with one TF appendix.
2. **Math depth?** "Understand enough to debug" (recommended for practitioner audience) vs "rigorous derivations" (academic audience). Pick one and hold the line.
3. **Running case-study dataset?** Recommend: pair MS-COCO (general) with a domain set you already know well (medical, agriculture from EY, frog SDM) so domain examples come from real work rather than fabricated demos.
