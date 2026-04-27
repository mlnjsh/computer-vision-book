"""Generate the book outline as a Word document."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


CHAPTERS = [
    ("Part I — Foundations", None, None),
    ("Chapter 1", "The 2026 Computer Vision Landscape",
     "A grounded tour of where CV is in 2026: from the OpenCV era to foundation models. Maps the pipeline (acquisition → preprocessing → modeling → deployment), introduces the four eras (classical, CNN, ViT, foundation/multimodal), and frames the rest of the book. Reader leaves with a mental model of when to reach for SIFT vs YOLO vs SAM 3 vs a VLM, and sets up the running case-study dataset used through the book."),
    ("Chapter 2", "Image Fundamentals and Pixel-Level Operations",
     "Pixels, color spaces (RGB/HSV/LAB/YCbCr), sampling, quantization, histograms, and convolution from first principles. Covers filtering, blurring, sharpening, denoising (Gaussian, bilateral, non-local means), edge detection (Sobel, Canny, Laplacian), thresholding (Otsu, adaptive), and morphology. Hands-on: build a document-cleanup preprocessor in pure OpenCV that survives uneven lighting."),
    ("Chapter 3", "Classical Feature Engineering: SIFT, ORB, and Geometry",
     "Why classical features still matter in 2026 (SLAM, panorama, low-data domains). Covers Harris/FAST corners, SIFT/SURF/ORB/BRIEF descriptors, FLANN matching, RANSAC homography, Hough transforms, contour analysis, and template matching. Hands-on: stitch a multi-image panorama and build a logo-detector with feature matching — no neural networks."),
    ("Chapter 4", "Camera Geometry, Calibration, and Stereo Vision",
     "Pinhole and fisheye camera models, intrinsics/extrinsics, lens distortion, calibration with checkerboards, epipolar geometry, stereo rectification, disparity maps, and the math of triangulation. Bridges classical CV to modern depth estimation. Hands-on: calibrate a webcam and reconstruct a scene's depth map from a stereo pair using OpenCV's StereoSGBM."),

    ("Part II — Deep Learning for Vision", None, None),
    ("Chapter 5", "Convolutional Neural Networks: From LeNet to ConvNeXt",
     "The CNN family tree as a single story: LeNet → AlexNet → VGG → Inception → ResNet → DenseNet → EfficientNet → MobileNet → ConvNeXt. Builds intuition for why each design choice (skip connections, bottleneck blocks, depthwise separables, modern normalizations) was a real fix to a real problem. Hands-on: implement a ResNet-18 from scratch in PyTorch and reproduce a CIFAR-10 result."),
    ("Chapter 6", "Training Modern Vision Models in Practice",
     "The unglamorous-but-decisive chapter: data loaders, Albumentations augmentation pipelines, mixup/cutmix, label smoothing, optimizers (SGD vs AdamW vs Lion), schedulers (cosine, one-cycle), mixed precision, gradient checkpointing, multi-GPU with PyTorch Lightning, and experiment tracking with Weights & Biases. Hands-on: fine-tune a timm model on a custom dataset and beat a published baseline through training tricks alone."),
    ("Chapter 7", "Object Detection: From R-CNN to YOLO26 and DETR",
     "Two-stage (R-CNN, Fast/Faster R-CNN) vs single-stage (SSD, RetinaNet, focal loss) vs anchor-free (FCOS, CenterNet) vs transformer-based (DETR, DINO-DETR, RT-DETR) vs the YOLO family through YOLOv8/YOLO11/YOLOv12/YOLO26 (NMS-free, end-to-end, edge-friendly). Covers mAP/IoU/PR-curve evaluation honestly. Hands-on: train YOLO26 on a custom Roboflow dataset and benchmark it against RT-DETR on the same task."),
    ("Chapter 8", "Image Segmentation: U-Net to SAM 3 and Grounding DINO",
     "Semantic vs instance vs panoptic segmentation. Walks through FCN, U-Net, DeepLab (atrous + ASPP), Mask R-CNN, Mask2Former, then jumps to the foundation-model era: SAM 1/2/3 (clicks, boxes, masks, and concepts via text in SAM 3), Grounding DINO + SAM for open-vocabulary segmentation. Hands-on: build a zero-shot 'segment anything I describe' pipeline with SAM 3 + Grounding DINO and deploy it as a Gradio app."),

    ("Part III — Modern Architectures and Foundation Models", None, None),
    ("Chapter 9", "Vision Transformers and Hybrid Architectures",
     "Attention from scratch, then ViT (patches, positional encoding, [CLS] token), DeiT (data-efficient training), Swin (hierarchical + shifted windows), MaxViT, and the new Mamba/SSM-based vision models (VMamba, Vision-Mamba). Discusses when transformers beat CNNs (data-rich, large-context) and when they lose (small-data, latency-sensitive). Hands-on: train a ViT-Small on ImageNette and compare its attention maps to a ResNet-50's class activation maps."),
    ("Chapter 10", "Self-Supervised Vision: From SimCLR to DINOv3",
     "Why labels became the bottleneck and how self-supervision broke it. Covers contrastive (SimCLR, MoCo, BYOL), masked image modeling (MAE, SimMIM), and the DINO line (DINO → DINOv2 → DINOv3, the 2025 model where a single frozen backbone outperforms specialists on dense prediction). Hands-on: extract DINOv3 features and use them as a frozen backbone for a downstream segmentation task with a 90% data reduction vs supervised baseline."),
    ("Chapter 11", "CLIP and Vision-Language Pretraining",
     "Contrastive language-image pretraining as a paradigm shift. Walks through CLIP, OpenCLIP, SigLIP, EVA-CLIP, and the open-vocabulary tasks they unlock: zero-shot classification, image-text retrieval, semantic search, and grounded detection. Covers prompt engineering for vision (templates, ensembles) and FAISS for billion-scale retrieval. Hands-on: build a 'search your photo library by natural language' app with CLIP + FAISS that runs on a laptop."),
    ("Chapter 12", "Generative Vision: GANs, VAEs, and the Diffusion Era",
     "GAN dynamics (mode collapse, Wasserstein loss), the VAE latent space, then the diffusion takeover: DDPM, score-based models, classifier-free guidance, latent diffusion, Stable Diffusion 3.5, Flux, SDXL, ControlNet, IP-Adapter, and LoRA fine-tuning. Practical recipes for inpainting, super-resolution, and style transfer that ship to production. Hands-on: fine-tune SDXL with LoRA on a personal dataset and chain it with ControlNet for conditioned generation."),

    ("Part IV — Multimodal, Video, and 3D", None, None),
    ("Chapter 13", "Vision-Language Models: The Multimodal Stack",
     "Anatomy of a modern VLM: vision encoder + projector + LLM decoder. Covers LLaVA, Qwen2.5-VL, InternVL, Florence-2 / Florence-3, Gemma 3 Vision, and the closed frontier (GPT-4o, Claude Vision Sonnet 4.6/Opus 4.7, Gemini 2.5 Pro). When to fine-tune vs prompt vs use the API. Honest cost/latency/accuracy comparison table. Hands-on: build a chart-and-document Q&A system using the Claude Vision API + a local Qwen2.5-VL fallback."),
    ("Chapter 14", "Document AI and Visual Agents",
     "The most underrated commercial CV application in 2026. Covers OCR (PaddleOCR, Tesseract, Donut), layout analysis (LayoutLMv3, Doctr), table extraction, structured-output VLMs, and the new visual agent loop: screenshot → reason → click. Walks through Claude Computer Use and OpenAI's vision agent pattern. Hands-on: build an invoice-extraction-to-database pipeline and a simple browser-automation agent driven by vision."),
    ("Chapter 15", "Video Understanding: Action, Tracking, and VideoMAE",
     "Temporal modeling: optical flow (Lucas-Kanade, RAFT), 3D CNNs (I3D, SlowFast), VideoMAE, video-language models. Tracking pipeline: SORT → DeepSORT → ByteTrack → BoT-SORT → SAM 2 for video. Action recognition, temporal action detection, and video-text retrieval. Hands-on: build a sports-analytics pipeline that detects, tracks, and counts players' actions in a clip."),
    ("Chapter 16", "3D Vision: Depth, NeRF, and Gaussian Splatting",
     "Monocular depth (MiDaS, Depth Anything v2, Marigold), point clouds (PointNet, PointTransformer), structure-from-motion (COLMAP), NeRF and its descendants (Instant-NGP, Mip-NeRF), and 3D Gaussian Splatting — the 2024-2026 dominant scene representation for real-time photoreal rendering. Bridges to SLAM and AR/VR. Hands-on: capture a scene with a phone, train a 3DGS model in Nerfstudio, and render a fly-through."),

    ("Part V — Frontiers and Production", None, None),
    ("Chapter 17", "Vision-Language-Action Models for Robotics and Embodied AI",
     "The category that didn't exist in 2023 and is now the most exciting in CV. Covers the VLA paradigm (vision encoder + language model + action decoder), RT-1/RT-2, OpenVLA, π0 (Pi-Zero, diffusion-based continuous control), Helix (Figure AI humanoid), and the Open X-Embodiment dataset. Discusses the pose estimation stack (OpenPose, MediaPipe, SMPL) as the bridge from pixels to actions. Hands-on: run OpenVLA in simulation on a manipulation task and visualize its attention over the scene."),
    ("Chapter 18", "Domain-Specific Vision: Medical, Autonomous, Geospatial, Agricultural",
     "How CV is applied where it actually generates revenue. Medical imaging (MONAI, nnU-Net, SAM-Med, regulatory considerations), autonomous driving (BEV perception, BEVFormer, lane detection, sensor fusion, nuScenes), satellite/geospatial (Segment Geospatial, foundation models for Earth observation), and agriculture (DINOv3 + YOLO26 for weed detection — a real 2026 paper). Hands-on: train a domain model in MONAI on a public chest-X-ray dataset and a BEV perception toy example."),
    ("Chapter 19", "Optimization and Edge Deployment",
     "Making models run fast on real hardware. Quantization (PTQ, QAT, INT8, FP16, FP8), pruning (structured/unstructured), knowledge distillation, ONNX export, runtime engines (ONNX Runtime, TensorRT, OpenVINO, Apple CoreML, TFLite, NVIDIA Triton), and edge platforms (Jetson Orin, Raspberry Pi 5 + Hailo, mobile NPUs). Honest benchmarks across the stack. Hands-on: take the YOLO26 from Chapter 7, quantize to INT8, export to TensorRT, and deploy on a Jetson Orin Nano with measured latency."),
    ("Chapter 20", "MLOps, Responsible AI, and the Future of Computer Vision",
     "The end-to-end production loop: data versioning (DVC), label management (Label Studio, Roboflow), active learning, drift detection, model monitoring, A/B testing for vision, CI/CD with MLflow/W&B. Responsible AI: bias auditing, explainability (Grad-CAM, SHAP, Captum), privacy (federated learning, differential privacy for vision), and legal frontiers (EU AI Act, content provenance / C2PA). Closes with a forward-looking section: where CV is heading by 2028 (unified VLA agents, neural rendering as default, on-device foundation models). Capstone: ship the running case-study pipeline end-to-end as a monitored production service."),
]


def add_horizontal_line(paragraph):
    p = paragraph._p
    pPr = p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '8')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '4A4A4A')
    pBdr.append(bottom)
    pPr.append(pBdr)


def main():
    doc = Document()

    # Default font
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)

    # Title page
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run('Computer Vision')
    run.font.size = Pt(36)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1F, 0x3A, 0x68)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sub.add_run('From Foundations to Frontier')
    r.font.size = Pt(20)
    r.font.italic = True
    r.font.color.rgb = RGBColor(0x4A, 0x4A, 0x4A)

    sub2 = doc.add_paragraph()
    sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = sub2.add_run('A 20-Chapter Modern Book — Outline & Writing Plan')
    r2.font.size = Pt(14)
    r2.font.color.rgb = RGBColor(0x4A, 0x4A, 0x4A)

    doc.add_paragraph()
    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for line in [
        ('Author: Milan Amrut Joshi', True),
        ('Target length: ~60,000 words / ~280 pages / ~3,000 words per chapter', False),
        ('Companion: GitHub repo with one runnable Colab notebook + production case study per chapter', False),
        ('Stack defaults: Python 3.12, PyTorch 2.x, Hugging Face, Ultralytics, OpenCV, ONNX/TensorRT', False),
        ('Positioning: Practitioner-first. Theory deep enough to debug. Every chapter ends in working code.', False),
    ]:
        run = meta.add_run('\n' + line[0])
        run.font.size = Pt(11)
        if line[1]:
            run.font.bold = True

    doc.add_page_break()

    # Why this book
    h = doc.add_heading('Why this book, why now', level=1)
    h.runs[0].font.color.rgb = RGBColor(0x1F, 0x3A, 0x68)
    p = doc.add_paragraph(
        'By 2026 the CV landscape has structurally shifted three ways most existing books miss:')
    items = [
        'Frozen foundation backbones (DINOv3, SAM 3) replace task-specific training for most use cases.',
        'Vision-Language-Action models (RT-2, OpenVLA, π0, Helix) collapse perception + reasoning + control into one architecture.',
        'Visual agents (Claude Computer Use, GPT-4o vision agents) make vision the input layer of autonomous workflows.',
    ]
    for it in items:
        doc.add_paragraph(it, style='List Number')
    doc.add_paragraph(
        'This book covers the full arc — classical → CNN → ViT → foundation models → multimodal → embodied — with code that runs on a 2026 laptop and ships to production.')

    doc.add_page_break()

    # Table of Contents (manual)
    h = doc.add_heading('Table of Contents', level=1)
    h.runs[0].font.color.rgb = RGBColor(0x1F, 0x3A, 0x68)
    for entry in CHAPTERS:
        label, title_text, _ = entry
        if title_text is None:
            p = doc.add_paragraph()
            r = p.add_run(label)
            r.font.bold = True
            r.font.size = Pt(13)
            r.font.color.rgb = RGBColor(0x1F, 0x3A, 0x68)
        else:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.7)
            r = p.add_run(f'{label}  ·  {title_text}')
            r.font.size = Pt(11)

    doc.add_page_break()

    # Chapter content
    for entry in CHAPTERS:
        label, title_text, body = entry
        if title_text is None:
            # Part heading
            doc.add_page_break()
            h = doc.add_heading(label, level=1)
            h.alignment = WD_ALIGN_PARAGRAPH.CENTER
            h.runs[0].font.color.rgb = RGBColor(0x1F, 0x3A, 0x68)
            add_horizontal_line(h)
        else:
            p = doc.add_paragraph()
            r = p.add_run(label)
            r.font.bold = True
            r.font.size = Pt(13)
            r.font.color.rgb = RGBColor(0x1F, 0x3A, 0x68)

            p2 = doc.add_paragraph()
            r2 = p2.add_run(title_text)
            r2.font.bold = True
            r2.font.size = Pt(14)
            r2.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

            body_p = doc.add_paragraph(body)
            body_p.paragraph_format.space_after = Pt(14)

    # Schedule overview
    doc.add_page_break()
    h = doc.add_heading('2-Month Writing Schedule (8 Weeks)', level=1)
    h.runs[0].font.color.rgb = RGBColor(0x1F, 0x3A, 0x68)
    doc.add_paragraph(
        'Assumptions: ~2 hours of focused writing/day (≈1,500 words on a good day) + 1 hour code/figures, 6 days/week. Each chapter ≈ 3 working days. Parallelism (researching one chapter while drafting the previous) compresses 60 working days into 8 calendar weeks. See WRITING_PLAN.xlsx for the day-by-day grid.'
    )

    schedule = [
        ('Week 0 (Pre-launch)', 'Set up GitHub repo, pick running case-study dataset, draft chapter template, block writing hours.'),
        ('Week 1', 'Ch 1 (Landscape) → Ch 2 (Pixel ops) → outline Ch 3.'),
        ('Week 2', 'Ch 3 (Classical features, panorama) → Ch 4 (Camera geometry, stereo).'),
        ('Week 3', 'Ch 5 (CNNs ResNet-18) → Ch 6 (Training tricks).'),
        ('Week 4', 'Ch 7 (YOLO26 + RT-DETR) → Ch 8 (SAM 3 + Grounding DINO). Mid-book consistency pass.'),
        ('Week 5', 'Ch 9 (ViTs) → Ch 10 (DINOv3, frozen-backbone notebook).'),
        ('Week 6', 'Ch 11 (CLIP + FAISS) → Ch 12 (Diffusion, hardest figures) → Ch 13 (VLMs + Claude Vision).'),
        ('Week 7', 'Ch 14 (Document AI / agents) → Ch 15 (Video) → Ch 16 (3DGS) → start Ch 17.'),
        ('Week 8', 'Ch 17 (VLA) → Ch 18 (Domains) → Ch 19 (Edge) → Ch 20 (MLOps + Future). Cross-chapter pass.'),
        ('Week 9 (buffer)', 'Full read-through, technical reviewer feedback, polish figures, write Preface.'),
    ]
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Light Grid Accent 1'
    hdr = table.rows[0].cells
    hdr[0].text = 'Week'
    hdr[1].text = 'Focus'
    for run in hdr[0].paragraphs[0].runs + hdr[1].paragraphs[0].runs:
        run.font.bold = True
    for week, focus in schedule:
        row = table.add_row().cells
        row[0].text = week
        row[1].text = focus

    # Open decisions
    doc.add_page_break()
    h = doc.add_heading('Open Decisions', level=1)
    h.runs[0].font.color.rgb = RGBColor(0x1F, 0x3A, 0x68)
    decisions = [
        ('Single framework or both?', 'PyTorch-only is faster to write and matches modern research; including TensorFlow/Keras doubles code maintenance but widens audience. Recommended: PyTorch-only with one TF appendix.'),
        ('Math depth?', '"Understand enough to debug" (recommended, practitioner audience) vs "rigorous derivations" (academic audience). Pick one and hold the line.'),
        ('Running case-study dataset?', 'Recommend pairing MS-COCO (general) with a domain set you already know (medical, agriculture from EY, frog SDM) so domain examples come from real work.'),
    ]
    for q, a in decisions:
        p = doc.add_paragraph()
        r = p.add_run(q)
        r.font.bold = True
        r.font.size = Pt(12)
        doc.add_paragraph(a)

    out = 'BOOK_OUTLINE.docx'
    doc.save(out)
    print(f'Wrote {out}')


if __name__ == '__main__':
    main()
