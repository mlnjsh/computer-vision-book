# Detailed Lesson Plans — Computer Vision: From Foundations to Frontier (2026)

Per-chapter ordered TOCs showing **definitions → concepts → theory → code → notebook cells → exercises**.
Use as the daily writing roadmap — each `**[TYPE]**` row is one writeable unit.

**Section type legend:**
`HOOK` motivating story · `DEF` definitions · `CONCEPT` intuition · `THEORY` math
`CODE` inline snippet · `NB` notebook cell · `FIG` figure · `PROD` production note
`EX` exercise · `READ` external reading

---

## Chapter 1 — The 2026 Computer Vision Landscape

**Reading:** 35–45 min · **Notebook:** ~20 min on T4 · **Difficulty:** ★☆☆☆☆ · **Words:** ~2,800

**Prereqs:** Python + NumPy. No prior CV.
**You'll be able to:**
- Place any CV paper into one of four eras (classical / CNN / ViT / foundation+multimodal).
- Pick the right tool for a problem from a 4-way decision tree (SIFT vs YOLO vs SAM 3 vs VLM).
- Run one canonical model from each era and compare outputs on the same image.
- Use the book's running case-study dataset locally and on Kaggle.

### Detailed TOC
1.0 **[HOOK]** *"What can a single Claude Vision call replace from a 2018 OpenCV pipeline?"* — show a 30-line script that replaces 200 lines.
1.1 **[DEF]** Image, pixel, channel, tensor, feature, label, prediction, model, inference.
1.2 **[CONCEPT]** The CV pipeline: acquisition → preprocessing → modeling → evaluation → deployment.
1.3 **[CONCEPT]** The four eras with one canonical model each: SIFT (2004), AlexNet (2012), ViT (2021), SAM 3 + Claude Vision (2025).
1.4 **[THEORY]** Why each era ended — the data, compute, or architecture trigger.
1.5 **[DEF]** Foundation model, frozen backbone, zero-shot, multimodal, agent.
1.6 **[CONCEPT]** Decision tree: when to use classical / supervised / foundation / VLM / agent.
1.7 **[NB]** Cells 1–7 — run YOLO26, SAM 3, CLIP, and Claude Vision on the same image.
1.8 **[FIG]** Side-by-side era comparison + cost/latency/accuracy chart.
1.9 **[PROD]** Cost-of-inference table: $/1M images per model class.
1.10 **[EX]** Pick a CV problem from your work, place it on the 4-era chart, justify.
1.11 **[READ]** Stanford CS231n L1 + LeCun's "deep learning era" timeline.

### Notebook cells (`notebooks/ch01_landscape.ipynb`)
1. Environment detect (Kaggle / Colab / local) + dataset path resolver.
2. Load a busy street-scene image (case-study dataset).
3. Run YOLO26 detection → save `figures/ch01/fig_yolo.png`.
4. Run SAM 3 with text prompt "all the cars" → save mask overlay.
5. Run CLIP zero-shot classification across 10 candidate labels.
6. Call Claude Vision with the image; ask for structured JSON description.
7. Build the 4-panel comparison figure → `fig_landscape_comparison.png`.

### Glossary additions
ViT, SAM, CLIP, VLM, foundation model, frozen backbone, zero-shot, prompt engineering for vision, multimodal, agent.

### References
- Dosovitskiy et al. 2021 (ViT); Kirillov et al. 2023 (SAM); Liu et al. 2022 (ConvNeXt).
- Stanford CS231n L1 video; Two Minute Papers SAM 3 review.

---

## Chapter 2 — Image Fundamentals and Pixel-Level Operations

**Reading:** 50–60 min · **Notebook:** ~25 min · **Difficulty:** ★☆☆☆☆ · **Words:** ~3,000

**Prereqs:** Ch 1.
**You'll be able to:**
- Convert between RGB / HSV / LAB / grayscale and explain when each is preferred.
- Build a robust document preprocessor (cleanup → binarize → deskew) in pure OpenCV.
- Apply Gaussian, median, and bilateral filters and predict each one's effect on edges.
- Detect edges with Sobel / Canny / Laplacian and tune their hyperparameters.

### Detailed TOC
2.0 **[HOOK]** A scanned receipt with shadows + glare → show how 30 lines of OpenCV beat a generic "remove shadow" web app.
2.1 **[DEF]** Image as a tensor (H × W × C), bit depth, dynamic range, sampling, quantization.
2.2 **[CONCEPT]** Color spaces and when to use them: RGB (default), HSV (color thresholding), LAB (perceptual), YCbCr (video / JPEG), grayscale (most CV ops).
2.3 **[FIG]** Same image in 5 color spaces side-by-side.
2.4 **[DEF]** Histogram, CDF, equalization, CLAHE.
2.5 **[CODE]** `cv2.equalizeHist` vs `cv2.createCLAHE`.
2.6 **[THEORY]** Convolution as a sliding kernel; relationship to correlation; padding modes.
2.7 **[DEF]** Kernel, stride, padding, separable filter.
2.8 **[CONCEPT]** Filter taxonomy: smoothing (Gaussian, box, median, bilateral) → sharpening (unsharp mask) → edge (Sobel, Laplacian, Canny).
2.9 **[CODE]** Each filter in one line of OpenCV; visualize on the same input.
2.10 **[THEORY]** Canny algorithm (gradient → non-max suppression → hysteresis).
2.11 **[DEF]** Thresholding: global (Otsu), adaptive (mean, Gaussian), color thresholding.
2.12 **[CONCEPT]** Morphology: erosion, dilation, opening, closing, top-hat, black-hat.
2.13 **[NB]** Document-cleanup pipeline — 8 cells.
2.14 **[PROD]** When OpenCV beats deep learning: low-data, predictable lighting, latency-critical.
2.15 **[EX]** Build a license-plate-isolator from a parked-car photo.
2.16 **[READ]** Tomasi & Manduchi 1998 (bilateral filter); Canny 1986.

### Notebook cells (`notebooks/ch02_pixel_ops.ipynb`)
1. Setup + load TextOCR sample receipt.
2. Convert to grayscale + histogram before/after.
3. CLAHE for local contrast.
4. Bilateral filter (preserves edges).
5. Adaptive thresholding.
6. Morphological cleanup (open then close).
7. Deskew via `cv2.minAreaRect` of the largest contour.
8. Save the final clean PNG → `figures/ch02/fig_doc_pipeline.png`.

### Glossary additions
Channel, kernel, stride, padding, CLAHE, Otsu's method, dilation, erosion, opening, closing.

### References
Canny 1986; Tomasi & Manduchi 1998; OpenCV docs (filtering chapter).

---

## Chapter 3 — Classical Feature Engineering: SIFT, ORB, and Geometry

**Reading:** 50 min · **Notebook:** ~30 min · **Difficulty:** ★★☆☆☆ · **Words:** ~3,000

**Prereqs:** Ch 2.
**You'll be able to:**
- Detect keypoints with Harris and FAST and explain the cornerness measure.
- Match SIFT/ORB descriptors with FLANN + Lowe's ratio test.
- Estimate a homography with RANSAC and stitch a panorama from 3 photos.
- Decide when classical features are still the right call in 2026.

### Detailed TOC
3.0 **[HOOK]** A no-internet drone using ORB-SLAM at 60 FPS on a CPU — why classical features still ship.
3.1 **[DEF]** Keypoint, descriptor, scale-space, repeatability, distinctiveness.
3.2 **[THEORY]** Harris cornerness from the second-moment matrix; eigenvalue intuition.
3.3 **[CONCEPT]** Detector zoo: Harris (corners), FAST (speed), DoG/Hessian (blobs), MSER.
3.4 **[CODE]** `cv2.cornerHarris` and `cv2.FastFeatureDetector_create`.
3.5 **[DEF]** Descriptor properties: rotation, scale, illumination, affine invariance.
3.6 **[THEORY]** SIFT pipeline: scale-space → orientation → 128-D histogram-of-gradients.
3.7 **[CONCEPT]** ORB = oriented FAST + rotated BRIEF; binary descriptors and Hamming distance.
3.8 **[CODE]** Compute SIFT and ORB descriptors and visualize keypoints.
3.9 **[DEF]** Brute-force vs FLANN matcher; Lowe's ratio test.
3.10 **[CONCEPT]** RANSAC: robust estimation under high outlier rates.
3.11 **[THEORY]** Homography matrix (3×3, 8 DoF); when it applies (planar scene or pure rotation).
3.12 **[NB]** Panorama stitching pipeline — 9 cells.
3.13 **[CONCEPT]** Hough transforms: line, circle, generalized.
3.14 **[CODE]** Detect coins via `cv2.HoughCircles`.
3.15 **[PROD]** Where SIFT/ORB still win: SLAM, AR markers, low-data domains, deterministic pipelines.
3.16 **[EX]** Build a logo-detector that finds your university logo on web pages without training.
3.17 **[READ]** Lowe 2004 (SIFT); Rublee 2011 (ORB); Fischler & Bolles 1981 (RANSAC).

### Notebook cells (`notebooks/ch03_classical_features.ipynb`)
1. Load 3 overlapping photos.
2. Detect ORB keypoints in each → visualize.
3. Match descriptors pair-wise with BFMatcher + ratio test.
4. Estimate pairwise homographies with RANSAC.
5. Warp + blend into a panorama.
6. Compare ORB vs SIFT runtime + match count.
7. Coin-counting demo with HoughCircles.
8. Logo template-matching demo.
9. Save panorama → `figures/ch03/fig_panorama.png`.

### Glossary additions
Keypoint, descriptor, scale-space, FLANN, Lowe's ratio test, homography, RANSAC, Hough transform, MSER.

### References
Lowe 2004; Rublee et al. 2011; Fischler & Bolles 1981; Bay et al. 2006 (SURF).

---

## Chapter 4 — Camera Geometry, Calibration, and Stereo Vision

**Reading:** 50 min · **Notebook:** ~30 min · **Difficulty:** ★★★☆☆ · **Words:** ~3,200

**Prereqs:** Ch 3 + linear algebra (matrices, eigenvectors).
**You'll be able to:**
- Calibrate a webcam with a checkerboard and recover intrinsics + distortion.
- Read a 3×4 projection matrix and identify intrinsics vs extrinsics.
- Compute a disparity map from a stereo pair and convert to depth.

### Detailed TOC
4.0 **[HOOK]** Why your phone's portrait mode draws ovals around heads — bad stereo math.
4.1 **[DEF]** World, camera, image coordinates; rigid transforms; homogeneous coordinates.
4.2 **[THEORY]** Pinhole projection: P = K [R | t]; what each entry means.
4.3 **[DEF]** Intrinsics (fx, fy, cx, cy, skew); extrinsics (R, t); 6-DoF pose.
4.4 **[CONCEPT]** Lens distortion: radial (k1, k2, k3) and tangential (p1, p2).
4.5 **[THEORY]** Zhang's calibration method (multiple checkerboard views).
4.6 **[NB]** Calibrate a webcam — 6 cells.
4.7 **[DEF]** Epipolar geometry: epipole, epipolar line, fundamental matrix F, essential matrix E.
4.8 **[CONCEPT]** Stereo rectification — making epipolar lines horizontal.
4.9 **[THEORY]** Disparity → depth: Z = f·B/d; baseline trade-offs.
4.10 **[CODE]** OpenCV StereoSGBM disparity map.
4.11 **[FIG]** Disparity colormap on the KITTI sample.
4.12 **[CONCEPT]** Bridge: where this hands off to neural depth (MiDaS, Depth Anything v2, Ch 16).
4.13 **[PROD]** Calibration drift in production; periodic recalibration; thermal expansion.
4.14 **[EX]** Estimate the focal length of a phone camera from object width + distance.
4.15 **[READ]** Hartley & Zisserman ch 6–9; Zhang 2000.

### Notebook cells (`notebooks/ch04_camera_geometry.ipynb`)
1. Capture / load 15 checkerboard images.
2. Detect corners with `cv2.findChessboardCorners`.
3. Calibrate with `cv2.calibrateCamera`; print K, distortion.
4. Undistort an image; show before/after.
5. Load a KITTI stereo pair.
6. Compute SGBM disparity → depth map.
7. Save figure `fig_depth_kitti.png`.

### Glossary additions
Intrinsics, extrinsics, projection matrix, fundamental matrix, essential matrix, epipolar line, disparity, baseline, rectification, lens distortion.

### References
Hartley & Zisserman (book); Zhang 2000; OpenCV calib3d docs.

---

## Chapter 5 — Convolutional Neural Networks: From LeNet to ConvNeXt

**Reading:** 60 min · **Notebook:** ~30 min · **Difficulty:** ★★☆☆☆ · **Words:** ~3,200

**Prereqs:** Ch 1; basic neural-network knowledge (forward/backward pass).
**You'll be able to:**
- Implement ResNet-18 from scratch in PyTorch in <100 lines.
- Reproduce a CIFAR-10 baseline (~92% top-1) on Kaggle T4 in under 30 minutes.
- Pick the right CNN family for given (data, latency, hardware) constraints.

### Detailed TOC
5.0 **[HOOK]** A 2012 paper that ended a decade of feature-engineering — what AlexNet actually changed.
5.1 **[DEF]** Neuron, layer, weight, bias, activation, loss; chain rule recap.
5.2 **[CONCEPT]** Why convolutions: parameter sharing, translation equivariance, locality.
5.3 **[THEORY]** Convolution forward/backward; receptive field growth; padding/stride math.
5.4 **[DEF]** Pooling (max / avg / global avg), batch norm, ReLU/GELU/SiLU.
5.5 **[CODE]** A 5-layer CNN in 30 lines of PyTorch.
5.6 **[CONCEPT]** Family tree of CNNs as a single narrative.
5.7 **[CONCEPT]** LeNet (1998): the template; AlexNet (2012): scale + ReLU + dropout.
5.8 **[CONCEPT]** VGG (2014): depth via 3×3 stacks; GoogLeNet/Inception: multi-scale modules.
5.9 **[THEORY]** ResNet (2015): why skip connections actually help (gradient flow, identity mapping).
5.10 **[NB]** Implement ResNet-18 from scratch — 8 cells.
5.11 **[CONCEPT]** DenseNet (concat reuse), EfficientNet (compound scaling), MobileNet (depthwise separable).
5.12 **[CONCEPT]** ConvNeXt (2022): "modernized ResNet" — what it borrowed from ViT.
5.13 **[CODE]** Use `timm.create_model('convnext_tiny.fb_in22k', pretrained=True)`.
5.14 **[PROD]** Latency vs accuracy frontier — choose model by hardware target.
5.15 **[EX]** Modify ResNet-18 → ResNet-26 by adding two blocks; verify accuracy gain on CIFAR-10.
5.16 **[READ]** He et al. 2016; Liu et al. 2022 (ConvNeXt).

### Notebook cells (`notebooks/ch05_cnns.ipynb`)
1. Load CIFAR-10.
2. Augmentation pipeline (RandomCrop + flip + normalize).
3. Implement BasicBlock with skip connection.
4. Implement ResNet-18 by stacking 4 stages of BasicBlocks.
5. Training loop with `torch.optim.SGD` + cosine schedule.
6. Evaluate top-1; should reach ~92% in 30 epochs.
7. Compare against `torchvision.models.resnet18(pretrained=True)` + linear probe.
8. Save best weights.

### Glossary additions
Receptive field, depthwise separable conv, residual block, batch norm, GELU, compound scaling.

### References
LeNet (LeCun 1998); AlexNet 2012; ResNet 2016; ConvNeXt 2022; EfficientNet 2019.

---

## Chapter 6 — Training Modern Vision Models in Practice

**Reading:** 55 min · **Notebook:** ~45 min · **Difficulty:** ★★☆☆☆ · **Words:** ~3,000

**Prereqs:** Ch 5.
**You'll be able to:**
- Beat a published CIFAR-100 baseline using only training tricks (no architecture changes).
- Configure mixed precision, gradient accumulation, and `torch.compile` correctly.
- Set up a W&B sweep and pick LR + weight decay from the result.

### Detailed TOC
6.0 **[HOOK]** "Bag of Tricks" — same architecture, +4 points top-1 from training changes alone.
6.1 **[CONCEPT]** Loss landscape intuition; sharp vs flat minima; why batch size matters.
6.2 **[DEF]** Optimizer family: SGD-momentum, Adam, AdamW, Lion; when to pick each.
6.3 **[THEORY]** AdamW vs Adam — decoupled weight decay; why this matters.
6.4 **[CONCEPT]** LR schedulers: cosine, one-cycle, warmup-then-cosine.
6.5 **[CODE]** `torch.optim.lr_scheduler.OneCycleLR` setup.
6.6 **[DEF]** Augmentation taxonomy: pixel-level (color jitter, blur), spatial (crop, flip, affine), mix (mixup, cutmix, mosaic).
6.7 **[CODE]** Albumentations pipeline for classification + detection.
6.8 **[CONCEPT]** Label smoothing, soft targets, knowledge distillation as regularizers.
6.9 **[THEORY]** AMP: FP16/BF16 numerics; loss scaling; what breaks in pure FP16.
6.10 **[CODE]** `torch.cuda.amp.autocast` + `GradScaler`; gradient checkpointing.
6.11 **[CONCEPT]** Multi-GPU: DDP basics; when to use DeepSpeed/FSDP.
6.12 **[CODE]** PyTorch Lightning skeleton for the same training loop.
6.13 **[NB]** Beat a baseline notebook — 9 cells.
6.14 **[CONCEPT]** Reproducibility: seeds, deterministic CUDA, dataloader workers.
6.15 **[PROD]** Hyperparameter sweeps with W&B; how to budget GPU hours.
6.16 **[EX]** Run a sweep over (LR, wd, augmentation strength) and beat the timm baseline by ≥1%.
6.17 **[READ]** He et al. 2019 (Bag of Tricks); Loshchilov & Hutter 2019 (AdamW).

### Notebook cells (`notebooks/ch06_training.ipynb`)
1. Setup + load Animal Faces (HQ).
2. timm baseline (`resnet50.a1_in1k`, no tricks).
3. Add Albumentations stronger pipeline.
4. Add mixup + cutmix.
5. Add label smoothing.
6. AdamW + OneCycleLR.
7. AMP + grad checkpointing.
8. W&B sweep config.
9. Compare baseline vs tricks final accuracy.

### Glossary additions
Mixed precision, gradient accumulation, gradient checkpointing, mixup, cutmix, label smoothing, EMA weights, LR warmup, DDP.

### References
He et al. 2019; Loshchilov & Hutter 2019; Smith 2018 (one-cycle); Tan & Le 2019.

---

## Chapter 7 — Object Detection: From R-CNN to YOLO26 and DETR

**Reading:** 65 min · **Notebook:** ~60 min · **Difficulty:** ★★★☆☆ · **Words:** ~3,300

**Prereqs:** Ch 5–6.
**You'll be able to:**
- Train YOLO26 on a custom Roboflow dataset and reach a publishable mAP.
- Compare anchor-based, anchor-free, and DETR-style detectors fairly.
- Read a PR curve and explain mAP@.5 vs mAP@.5:.95.

### Detailed TOC
7.0 **[HOOK]** A drone delivery startup that ditched a 200ms 2-stage pipeline for a 12ms YOLO26.
7.1 **[DEF]** Detection task: bounding box, class label, confidence; vs classification + localization vs segmentation.
7.2 **[DEF]** IoU, AP, mAP, mAP@.5, mAP@.5:.95, COCO format.
7.3 **[CONCEPT]** Two-stage detectors: region proposal + classification (R-CNN family).
7.4 **[CONCEPT]** Single-stage: predict everywhere at once (SSD, RetinaNet, YOLO).
7.5 **[THEORY]** Focal loss — why class imbalance breaks single-stage; the down-weighting fix.
7.6 **[DEF]** Anchor box; anchor-based vs anchor-free (FCOS, CenterNet).
7.7 **[CONCEPT]** DETR (2020): set prediction with transformers; bipartite matching loss; the slow-convergence problem.
7.8 **[CONCEPT]** DINO-DETR / RT-DETR: how they fixed DETR's training cost.
7.9 **[CONCEPT]** YOLO line: YOLOv1 → v3 → v5 → v8 → v11 → v12 → YOLO26.
7.10 **[CONCEPT]** YOLO26's NMS-free, end-to-end design — why it matters for edge.
7.11 **[CODE]** Train YOLO26 in 8 lines via Ultralytics.
7.12 **[NB]** Custom Roboflow dataset training + RT-DETR comparison — 10 cells.
7.13 **[CONCEPT]** NMS, soft-NMS, end-to-end (DETR-style) — when each is right.
7.14 **[CONCEPT]** Honest evaluation: per-class AP, small/medium/large, hard/easy.
7.15 **[FIG]** PR curves for YOLO26 vs RT-DETR on the same eval set.
7.16 **[PROD]** Throughput vs latency: batch size effects, INT8 quantization preview (full coverage in Ch 19).
7.17 **[EX]** Add a confusion-matrix-driven hard-example mining pass; remeasure mAP.
7.18 **[READ]** Ren et al. 2015 (Faster R-CNN); Lin et al. 2017 (focal loss); Carion et al. 2020 (DETR); Lyu et al. 2023 (RT-DETR).

### Notebook cells (`notebooks/ch07_detection.ipynb`)
1. Roboflow dataset download (YOLO format).
2. Visualize 9 samples.
3. Train `YOLO('yolo26n.pt')` for 50 epochs.
4. Eval on val: mAP, PR curves.
5. Train RT-DETR on the same data.
6. Side-by-side mAP + latency.
7. Inference video on a held-out clip.
8. Per-class AP table.
9. Confusion matrix.
10. Save best.pt + ONNX export (for Ch 19).

### Glossary additions
Anchor, IoU, mAP, focal loss, NMS, soft-NMS, set prediction, bipartite matching, FPN, PAN.

### References
Faster R-CNN; RetinaNet; YOLOv3 paper + YOLO26 tech notes; DETR; RT-DETR.

---

## Chapter 8 — Image Segmentation: U-Net to SAM 3 and Grounding DINO

**Reading:** 60 min · **Notebook:** ~40 min · **Difficulty:** ★★★☆☆ · **Words:** ~3,200

**Prereqs:** Ch 7.
**You'll be able to:**
- Train a U-Net for medical segmentation and beat a published Dice baseline.
- Use SAM 3 with text prompts for zero-shot open-vocabulary segmentation.
- Decide between SAM 3, Grounding DINO + SAM, and Mask2Former for a given task.

### Detailed TOC
8.0 **[HOOK]** "Segment all the trees in this satellite image" — 0 labels, 30 seconds.
8.1 **[DEF]** Semantic vs instance vs panoptic segmentation.
8.2 **[DEF]** Pixel accuracy, Dice, IoU per class, mIoU, PQ (panoptic quality).
8.3 **[CONCEPT]** FCN: classification → dense prediction by removing the final FC.
8.4 **[CONCEPT]** U-Net: encoder–decoder with skip connections; why it's still the medical default.
8.5 **[NB]** Train U-Net on LGG MRI segmentation — 8 cells.
8.6 **[CONCEPT]** DeepLab family: atrous convolutions and ASPP for multi-scale context.
8.7 **[CONCEPT]** Mask R-CNN: detection + per-RoI mask head (instance segmentation).
8.8 **[CONCEPT]** Mask2Former: unified architecture for semantic / instance / panoptic via masked attention.
8.9 **[CONCEPT]** SAM 1 (clicks/boxes) → SAM 2 (video) → SAM 3 (concepts via text).
8.10 **[THEORY]** SAM's promptable architecture; how text-conditioned masks work in SAM 3.
8.11 **[CONCEPT]** Grounding DINO + SAM: text → boxes → masks pipeline.
8.12 **[CODE]** 12-line zero-shot "segment anything I describe" inference.
8.13 **[NB]** Build a Gradio app — 6 cells.
8.14 **[PROD]** Latency: SAM ViT-H is slow; SAM 2 / SAM 3 distilled variants for production.
8.15 **[EX]** Replace a 50-image-trained U-Net with frozen DINOv3 + linear head; compare Dice (forward link to Ch 10).
8.16 **[READ]** Ronneberger et al. 2015; Kirillov et al. 2023 (SAM); SAM 2 (Ravi 2024); SAM 3 tech report.

### Notebook cells (`notebooks/ch08_segmentation.ipynb`)
1. Load LGG MRI dataset.
2. U-Net implementation in 60 lines.
3. Train + validate Dice ~0.85.
4. Visualize predictions vs ground truth.
5. Compare against `segmentation_models_pytorch` U-Net.
6. Load SAM 3; run with text prompt "tumor".
7. Run Grounding DINO → SAM pipeline on a satellite image.
8. Build Gradio app exposing SAM 3 + Grounding DINO.

### Glossary additions
Dice, IoU per class, mIoU, panoptic quality, atrous/dilated conv, ASPP, mask head, prompt-conditioned segmentation.

### References
U-Net; DeepLab v3+; Mask R-CNN; Mask2Former; SAM / SAM 2 / SAM 3; Grounding DINO.

---

## Chapter 9 — Vision Transformers and Hybrid Architectures

**Reading:** 60 min · **Notebook:** ~40 min · **Difficulty:** ★★★★☆ · **Words:** ~3,200

**Prereqs:** Ch 5; basic transformer / attention familiarity.
**You'll be able to:**
- Implement self-attention from scratch in <50 lines and explain QKV.
- Train ViT-Small on Imagenette and visualize attention rollouts.
- Pick between ViT, Swin, and Mamba-Vision for a given (data, latency) regime.

### Detailed TOC
9.0 **[HOOK]** A 2021 paper proving you don't need convolutions to beat ResNet — and what changed since.
9.1 **[DEF]** Token, query, key, value, attention score, attention map.
9.2 **[THEORY]** Scaled dot-product attention: softmax(QKᵀ/√d)V — derivation and intuition.
9.3 **[CODE]** Multi-head attention in 40 lines (no imports beyond torch).
9.4 **[DEF]** Patch embedding, class token ([CLS]), positional encoding (learned vs sinusoidal vs RoPE).
9.5 **[CONCEPT]** ViT architecture: split → embed → stack of transformer blocks → classifier head.
9.6 **[CONCEPT]** DeiT: data-efficient training via distillation from a CNN teacher.
9.7 **[CONCEPT]** Swin: hierarchical features + shifted windows for local attention.
9.8 **[CONCEPT]** MaxViT: alternating local + global attention; how it bridges CNN and ViT.
9.9 **[CONCEPT]** Mamba/SSM-based vision (VMamba, Vision-Mamba): linear-time alternative to attention.
9.10 **[NB]** Train ViT-Small on Imagenette + attention map visualization — 9 cells.
9.11 **[FIG]** Attention rollout heatmaps vs Grad-CAM heatmaps for the same image.
9.12 **[CONCEPT]** When ViT wins (large data, long range, multi-task) vs loses (low data, low latency).
9.13 **[PROD]** Linear scaling on token count; flash attention as the default in 2026.
9.14 **[EX]** Reduce ViT-Small to 3 layers and measure how much accuracy drops; compare to ResNet-3-block.
9.15 **[READ]** Dosovitskiy et al. 2021; Liu et al. 2021 (Swin); Touvron et al. 2021 (DeiT); Zhu et al. 2024 (Vision Mamba).

### Notebook cells (`notebooks/ch09_vit.ipynb`)
1. Implement scaled dot-product attention.
2. Implement MultiHeadAttention.
3. Implement PatchEmbed + ViT block.
4. Train ViT-Small on Imagenette.
5. Compute attention rollout for 6 sample images.
6. Compute Grad-CAM on a `resnet50` for the same images.
7. Side-by-side heatmap figure.
8. Evaluate Swin-Tiny baseline.
9. Save model + attention maps.

### Glossary additions
QKV, attention score, attention rollout, patch embedding, class token, positional encoding, RoPE, shifted-window attention, flash attention.

### References
ViT 2021; DeiT; Swin; MaxViT; Vision Mamba.

---

## Chapter 10 — Self-Supervised Vision: From SimCLR to DINOv3

**Reading:** 55 min · **Notebook:** ~45 min · **Difficulty:** ★★★★☆ · **Words:** ~3,000

**Prereqs:** Ch 9.
**You'll be able to:**
- Explain the four families of SSL: contrastive, distillation (BYOL/DINO), masked image modeling, joint-embedding.
- Use frozen DINOv3 as a feature extractor and beat a supervised baseline with 10× less labels.

### Detailed TOC
10.0 **[HOOK]** A medical-imaging team that beat a fully-labeled SOTA using DINOv3 + 50 labels.
10.1 **[DEF]** Self-supervised learning, pretext task, downstream task, linear probe, k-NN evaluation.
10.2 **[CONCEPT]** Why labels became the bottleneck — economics + long tail.
10.3 **[CONCEPT]** Contrastive (SimCLR, MoCo): pull positives, push negatives.
10.4 **[THEORY]** InfoNCE loss; the role of temperature; large batch / memory bank tricks.
10.5 **[CONCEPT]** BYOL: no negatives, just stop-gradient + EMA target.
10.6 **[CONCEPT]** Masked image modeling: MAE, SimMIM — predict masked patches.
10.7 **[CONCEPT]** DINO line: self-distillation with no labels; DINOv2 scaling; DINOv3's frozen-backbone leap.
10.8 **[CODE]** Extract DINOv3 features in 8 lines via HF Transformers.
10.9 **[NB]** Frozen DINOv3 + linear classifier vs full fine-tune — 9 cells.
10.10 **[CONCEPT]** When SSL features beat ImageNet supervised features (long tail, dense prediction, OOD).
10.11 **[PROD]** Storing and indexing SSL features for retrieval (FAISS preview, Ch 11).
10.12 **[EX]** Take 5% of the LGG MRI labels from Ch 8; show DINOv3 frozen + linear ≥ 95% of full-supervision Dice.
10.13 **[READ]** Chen et al. 2020 (SimCLR); Grill et al. 2020 (BYOL); He et al. 2022 (MAE); Oquab et al. 2024 (DINOv2); Meta DINOv3 tech report 2025.

### Notebook cells (`notebooks/ch10_self_supervised.ipynb`)
1. Setup; load LGG MRI subset.
2. Extract DINOv3 features (frozen backbone).
3. Train a 2-layer MLP head → record Dice.
4. Compare to: ImageNet-supervised ResNet50 frozen + MLP head.
5. Compare to: from-scratch U-Net trained on the full data.
6. SSL retrieval demo: query an image, retrieve top-5 from feature index.
7. Visualize PCA of DINOv3 features colored by class.
8. Sample-efficiency curve: Dice vs label fraction.
9. Save the experiment summary table.

### Glossary additions
Pretext task, linear probe, InfoNCE, EMA target, stop-gradient, masked image modeling, frozen backbone, joint-embedding.

### References
SimCLR; MoCo v3; BYOL; MAE; DINO; DINOv2; DINOv3.

---

## Chapter 11 — CLIP and Vision-Language Pretraining

**Reading:** 45 min · **Notebook:** ~30 min · **Difficulty:** ★★★☆☆ · **Words:** ~2,800

**Prereqs:** Ch 9; basic transformer NLP knowledge helpful.
**You'll be able to:**
- Run zero-shot classification with CLIP across arbitrary class lists.
- Build a "search by language" image search with FAISS that runs on a laptop.
- Distinguish CLIP, OpenCLIP, SigLIP, EVA-CLIP and pick one.

### Detailed TOC
11.0 **[HOOK]** "Find every photo with a red bicycle on the left" — across 100K personal photos in 200 ms.
11.1 **[DEF]** Image encoder, text encoder, joint embedding space, cosine similarity.
11.2 **[CONCEPT]** Contrastive language-image pretraining: paired (image, caption) data at scale.
11.3 **[THEORY]** CLIP loss: symmetric InfoNCE over image-text pairs in a batch.
11.4 **[CONCEPT]** Why CLIP unlocks zero-shot classification (class names → text embeddings → cosine search).
11.5 **[CODE]** Zero-shot classify in 6 lines via `open_clip`.
11.6 **[CONCEPT]** Prompt engineering for vision: templates ("a photo of a {}"), ensembles, label tweaking.
11.7 **[CONCEPT]** Variants: OpenCLIP (open data), SigLIP (sigmoid loss, simpler), EVA-CLIP (scaled vision encoder).
11.8 **[CONCEPT]** Image-text retrieval; image-image retrieval via shared space.
11.9 **[CODE]** FAISS index basics: IndexFlatIP, IndexIVFPQ.
11.10 **[NB]** Photo library search app — 8 cells.
11.11 **[CONCEPT]** Where CLIP fails (compositional, fine-grained, OCR text); the SigLIP fixes.
11.12 **[PROD]** Quantizing CLIP for on-device search (Ch 19 preview).
11.13 **[EX]** Build a CLIP-based content-moderation classifier with custom prompt templates.
11.14 **[READ]** Radford et al. 2021 (CLIP); Zhai et al. 2023 (SigLIP); Sun et al. 2023 (EVA-CLIP).

### Notebook cells (`notebooks/ch11_clip.ipynb`)
1. Setup; load Flickr8k.
2. Compute image embeddings with `open_clip` ViT-B/32.
3. Build a FAISS index.
4. Query by text prompt; show top-5 results.
5. Query by example image (image-image retrieval).
6. Prompt ensembling for zero-shot Imagenette classification.
7. Compare CLIP vs SigLIP zero-shot accuracy.
8. Save the index for re-use.

### Glossary additions
Joint embedding space, cosine similarity, prompt template, prompt ensemble, FAISS, IVFPQ.

### References
CLIP; OpenCLIP; SigLIP; EVA-CLIP; FAISS docs.

---

## Chapter 12 — Generative Vision: GANs, VAEs, and the Diffusion Era

**Reading:** 75 min · **Notebook:** ~75 min · **Difficulty:** ★★★★★ · **Words:** ~3,500

**Prereqs:** Ch 9; comfort with probabilistic notation.
**You'll be able to:**
- Explain DDPM forward + reverse processes and the link to score matching.
- Fine-tune SDXL with LoRA on a custom dataset and chain it with ControlNet.
- Pick between Stable Diffusion 3.5, Flux, and SDXL for a given budget.

### Detailed TOC
12.0 **[HOOK]** A side-by-side: 2014 GAN faces vs 2025 Flux faces.
12.1 **[DEF]** Generative model, prior, posterior, likelihood, evidence.
12.2 **[CONCEPT]** GAN: generator + discriminator minimax; mode collapse; non-saturating loss.
12.3 **[CONCEPT]** Wasserstein GAN; StyleGAN architectural innovations.
12.4 **[CONCEPT]** VAE: encoder + decoder + KL regularization; latent space.
12.5 **[THEORY]** Forward diffusion: q(x_t|x_{t-1}) Gaussian noise schedule.
12.6 **[THEORY]** Reverse process: learn p_θ(x_{t-1}|x_t); ε-prediction parameterization.
12.7 **[THEORY]** DDPM training objective as MSE on predicted noise.
12.8 **[DEF]** Score function ∇log p(x); score matching ↔ diffusion duality.
12.9 **[CONCEPT]** DDIM: deterministic sampler; classifier-free guidance.
12.10 **[CONCEPT]** Latent diffusion (Stable Diffusion): VAE encode → diffusion in latent → decode.
12.11 **[CONCEPT]** Modern open models: SD 3.5, Flux (rectified flow), SDXL — strengths & costs.
12.12 **[CONCEPT]** ControlNet: adding conditioning (depth/pose/canny) without retraining the base.
12.13 **[CONCEPT]** IP-Adapter: image prompts; LoRA: cheap fine-tuning.
12.14 **[NB]** SDXL LoRA fine-tune + ControlNet chain — 12 cells.
12.15 **[CONCEPT]** Inpainting, super-resolution, style transfer with diffusion.
12.16 **[PROD]** Inference cost; T2I latency budgets; safety / NSFW filters.
12.17 **[EX]** Chain Depth-Anything (Ch 16) → ControlNet-Depth → SDXL for pose-preserving redress.
12.18 **[READ]** Ho et al. 2020 (DDPM); Song et al. 2021 (score-based); Rombach et al. 2022 (LDM); Zhang et al. 2023 (ControlNet); Hu et al. 2021 (LoRA).

### Notebook cells (`notebooks/ch12_diffusion.ipynb`)
1. Setup `diffusers`, model download.
2. Run base SDXL on a few prompts.
3. Run with negative prompts and CFG sweep.
4. Prepare a 20-image personal dataset.
5. LoRA training config (rank=16, AdamW, 500 steps).
6. Run LoRA fine-tune.
7. Generate with the LoRA loaded.
8. Load Canny ControlNet; run conditioning.
9. Load Depth ControlNet (Depth Anything v2).
10. Inpainting demo.
11. Comparison grid: base / LoRA / LoRA+ControlNet.
12. Save figure `fig_diffusion_grid.png`.

### Glossary additions
ε-prediction, classifier-free guidance, denoising step, latent diffusion, rectified flow, ControlNet, IP-Adapter, LoRA, schedule (DDPM/DDIM).

### References
DDPM; DDIM; Score-Based Generative Modeling; Latent Diffusion; SDXL; ControlNet; LoRA.

---

## Chapter 13 — Vision-Language Models: The Multimodal Stack

**Reading:** 55 min · **Notebook:** ~30 min · **Difficulty:** ★★★☆☆ · **Words:** ~3,200

**Prereqs:** Ch 11; basic LLM/prompt familiarity.
**You'll be able to:**
- Describe a modern VLM as `vision encoder + projector + LLM decoder`.
- Build a chart-and-document Q&A app using Claude Vision + a local Qwen2.5-VL fallback.
- Pick between fine-tune / prompt / API for a given problem.

### Detailed TOC
13.0 **[HOOK]** A receipts-to-spreadsheet pipeline that took 3 months to build with OCR + rules vs 1 day with Claude Vision.
13.1 **[CONCEPT]** Anatomy of a VLM: vision encoder → projector (MLP/Q-Former) → LLM decoder.
13.2 **[CONCEPT]** Open VLMs: LLaVA, Qwen2.5-VL, InternVL, Florence-2/3, Gemma 3 Vision.
13.3 **[CONCEPT]** Closed frontier: GPT-4o, Claude Vision (Sonnet 4.6, Opus 4.7), Gemini 2.5 Pro.
13.4 **[CODE]** Run Qwen2.5-VL locally in 12 lines.
13.5 **[CODE]** Call Claude Vision API with structured output.
13.6 **[CONCEPT]** Prompt patterns: zero-shot, few-shot with images, JSON schema.
13.7 **[CONCEPT]** When to fine-tune vs prompt vs use the API — a decision matrix.
13.8 **[CONCEPT]** VLM fine-tuning: LoRA on the projector + parts of the LLM.
13.9 **[NB]** Doc-and-chart Q&A app — 9 cells.
13.10 **[CONCEPT]** Cost / latency / accuracy: honest comparison table on the same eval set.
13.11 **[CONCEPT]** Failure modes: hallucinated text in low-res, count errors, position errors.
13.12 **[PROD]** Fallback chains: API → local model when API fails or for PII.
13.13 **[EX]** Build a 3-document benchmark and compare 4 VLMs head-to-head.
13.14 **[READ]** LLaVA; Qwen2.5-VL; Florence-2; Anthropic Vision API guide.

### Notebook cells (`notebooks/ch13_vlm.ipynb`)
1. Setup; load Qwen2.5-VL-7B (4-bit).
2. Run image captioning on 5 charts.
3. Set up Anthropic SDK; call Claude Vision.
4. Define a JSON schema for chart extraction.
5. Run Claude with structured output.
6. Compare answers between Qwen2.5-VL and Claude.
7. Build a fallback chain wrapper.
8. Latency / cost table.
9. Gradio UI showing both side by side.

### Glossary additions
Projector / Q-Former, instruction-tuning for VLMs, structured output, image-text interleaving.

### References
LLaVA; Qwen2.5-VL; Florence-2; Anthropic Vision API docs.

---

## Chapter 14 — Document AI and Visual Agents

**Reading:** 50 min · **Notebook:** ~40 min · **Difficulty:** ★★★☆☆ · **Words:** ~2,800

**Prereqs:** Ch 13.
**You'll be able to:**
- Build an invoice-extraction pipeline with PaddleOCR + a structured-output VLM.
- Build a small browser-automation agent that uses screenshots to drive clicks.
- Reason about safety/audit for visual agents.

### Detailed TOC
14.0 **[HOOK]** A finance team that automated 80% of expense-report review with a 100-line agent.
14.1 **[DEF]** Document AI: OCR, layout, table, key-value extraction, form understanding.
14.2 **[CONCEPT]** Classical OCR: Tesseract; modern: PaddleOCR (multi-language).
14.3 **[CONCEPT]** Layout-aware models: LayoutLMv3 (text + layout + image).
14.4 **[CONCEPT]** End-to-end VLM-style: Donut (OCR-free).
14.5 **[CODE]** PaddleOCR call; bounding boxes + text.
14.6 **[CONCEPT]** Table extraction: lattice vs stream; modern transformer-based extractors.
14.7 **[NB]** Invoice → database — 8 cells.
14.8 **[CONCEPT]** Visual agents: the screenshot → reason → action loop.
14.9 **[CONCEPT]** Anthropic Computer Use; OpenAI vision agent pattern.
14.10 **[CODE]** A 50-line browser-automation agent (screenshot + click action).
14.11 **[CONCEPT]** Safety: action sandboxing, approval gates, audit logs, prompt injection via images.
14.12 **[PROD]** Cost shape: agents are 10–100× chattier than chat — budget accordingly.
14.13 **[EX]** Add a "review queue" UX: agent flags unsure invoices for human approval.
14.14 **[READ]** LayoutLMv3; Donut; PaddleOCR docs; Anthropic Computer Use guide.

### Notebook cells (`notebooks/ch14_document_ai_agents.ipynb`)
1. Load SROIE invoice dataset.
2. PaddleOCR text extraction.
3. Send raw text + image to Claude with JSON schema.
4. Parse output → SQLite.
5. Eval extraction accuracy on 50 invoices.
6. Set up Playwright browser env.
7. Implement screenshot → Claude → action loop.
8. Demo: agent fills a form on a sandbox page.

### Glossary additions
OCR, layout-aware model, key-value extraction, screenshot agent, action sandboxing, prompt injection via images.

### References
LayoutLMv3; Donut; PaddleOCR; Anthropic Computer Use.

---

## Chapter 15 — Video Understanding: Action, Tracking, and VideoMAE

**Reading:** 55 min · **Notebook:** ~50 min · **Difficulty:** ★★★★☆ · **Words:** ~3,000

**Prereqs:** Ch 7; Ch 9.
**You'll be able to:**
- Compute optical flow with RAFT and use it as a feature.
- Track multi-object scenes with ByteTrack and SAM 2.
- Recognize actions with VideoMAE and explain when temporal modeling is needed.

### Detailed TOC
15.0 **[HOOK]** A sports-analytics startup that replaced 5 hand-tuned pipelines with one VideoMAE backbone.
15.1 **[DEF]** Frame, clip, temporal stride, temporal receptive field.
15.2 **[CONCEPT]** Optical flow basics: brightness constancy; LK; modern dense flow (RAFT).
15.3 **[CODE]** Run RAFT on two consecutive frames.
15.4 **[CONCEPT]** Architectures: 2D + LSTM, 3D CNN (I3D), two-stream (RGB + flow), SlowFast, VideoMAE.
15.5 **[CONCEPT]** VideoMAE: masked spatiotemporal tubes; why it dominates SOTA.
15.6 **[CONCEPT]** Tracking taxonomy: detect-then-track (SORT, DeepSORT, ByteTrack, BoT-SORT) vs end-to-end (TrackFormer).
15.7 **[CONCEPT]** SAM 2 for video segmentation: memory bank for object persistence.
15.8 **[NB]** Sports-analytics pipeline — 10 cells.
15.9 **[CONCEPT]** Action recognition vs temporal action detection.
15.10 **[CONCEPT]** Video-language: video QA, video retrieval; recent VideoLLaMA.
15.11 **[PROD]** Latency budgets: 30 FPS = 33 ms/frame; what fits.
15.12 **[EX]** Add a "highlight reel" generator: detect goals + cut clips around them.
15.13 **[READ]** Carreira & Zisserman 2017 (I3D); Feichtenhofer 2019 (SlowFast); Tong 2022 (VideoMAE); Zhang 2022 (ByteTrack); SAM 2.

### Notebook cells (`notebooks/ch15_video.ipynb`)
1. Load a sports clip.
2. RAFT optical flow on a sample.
3. YOLO26 + ByteTrack player tracking.
4. SAM 2 segmenting tracked players.
5. VideoMAE inference on 16-frame windows for action labels.
6. Per-player action timeline.
7. Goal detection rule on top.
8. Generate a highlights cut.
9. Export annotated video.
10. Save figure `fig_action_timeline.png`.

### Glossary additions
Optical flow, dense flow, two-stream, SlowFast, VideoMAE, ByteTrack, BoT-SORT, memory bank, temporal action detection.

### References
I3D; SlowFast; VideoMAE; ByteTrack; SAM 2; RAFT.

---

## Chapter 16 — 3D Vision: Depth, NeRF, and Gaussian Splatting

**Reading:** 65 min · **Notebook:** ~75 min · **Difficulty:** ★★★★★ · **Words:** ~3,200

**Prereqs:** Ch 4; Ch 9.
**You'll be able to:**
- Run monocular depth (Depth Anything v2) and decide when it's enough.
- Capture a phone scene and train a 3D Gaussian Splatting reconstruction in Nerfstudio.
- Explain why 3DGS displaced NeRF for most production use.

### Detailed TOC
16.0 **[HOOK]** A real-estate listing in 2025 that became "walk through the house" via 3DGS.
16.1 **[DEF]** Depth, point cloud, voxel, mesh, signed distance function (SDF), radiance field.
16.2 **[CONCEPT]** Monocular depth: MiDaS, Depth Anything v2, Marigold (diffusion-based depth).
16.3 **[CODE]** 8-line Depth Anything v2 inference on an arbitrary image.
16.4 **[CONCEPT]** Point cloud processing: PointNet → PointTransformer.
16.5 **[CONCEPT]** Structure-from-motion: COLMAP pipeline (feature → match → bundle adjust).
16.6 **[CONCEPT]** NeRF: a neural function from (x, y, z, θ, φ) → (RGB, σ); volumetric rendering.
16.7 **[CONCEPT]** NeRF descendants: Instant-NGP (hash grids), Mip-NeRF (anti-aliasing).
16.8 **[CONCEPT]** 3D Gaussian Splatting: explicit ellipsoids; differentiable rasterization; real-time.
16.9 **[THEORY]** Splatting math: covariance projection, alpha compositing, densification rules.
16.10 **[NB]** Phone-capture to 3DGS fly-through — 10 cells.
16.11 **[CONCEPT]** SLAM connection: Gaussian-SLAM, NeRF-SLAM (Ch 17 preview).
16.12 **[CONCEPT]** Where each 3D rep wins: NeRF (smooth interp), 3DGS (real-time), point clouds (LiDAR), meshes (game engines).
16.13 **[PROD]** GPU memory and storage for 3DGS scenes; LoD strategies.
16.14 **[EX]** Mask out a moving person in your capture; retrain 3DGS for a clean static scene.
16.15 **[READ]** Mildenhall 2020 (NeRF); Müller 2022 (Instant-NGP); Kerbl 2023 (3DGS); Yang 2024 (Depth Anything v2).

### Notebook cells (`notebooks/ch16_3d_gaussian_splatting.ipynb`)
1. Setup; install Nerfstudio + gsplat.
2. Phone-capture data layout (50 images).
3. Run COLMAP via Nerfstudio CLI.
4. Train Splatfacto for 7K iterations.
5. Render fly-through.
6. Export ply + viewer.
7. Run Depth Anything v2 on a single shot for comparison.
8. Compare 3DGS render vs Instant-NGP on the same scene.
9. Compare GPU memory + time.
10. Save fly-through MP4.

### Glossary additions
Radiance field, volumetric rendering, hash grid, Gaussian splat, densification, novel-view synthesis, SfM, MVS.

### References
NeRF; Instant-NGP; 3DGS; Mip-NeRF; Depth Anything v2; COLMAP.

---

## Chapter 17 — Vision-Language-Action Models for Robotics and Embodied AI

**Reading:** 60 min · **Notebook:** ~60 min · **Difficulty:** ★★★★★ · **Words:** ~3,300

**Prereqs:** Ch 13; basic RL helpful but not required.
**You'll be able to:**
- Describe the VLA paradigm and the trade-off between discrete-token and continuous-action outputs.
- Run OpenVLA in a simulator and visualize its attention.
- Reason about safety and OOD generalization for embodied agents.

### Detailed TOC
17.0 **[HOOK]** Figure AI's Helix folding laundry — what's in the model that wasn't possible 18 months ago.
17.1 **[DEF]** Embodied AI; VLA = Vision-Language-Action; policy; demonstration; teleop.
17.2 **[CONCEPT]** Pose estimation as the bridge: OpenPose, MediaPipe, SMPL, hand pose.
17.3 **[CONCEPT]** Sim-to-real and domain randomization (briefly).
17.4 **[CONCEPT]** Open X-Embodiment dataset: cross-embodiment data at scale.
17.5 **[CONCEPT]** RT-1, RT-2: VLM tokens → discrete action tokens.
17.6 **[CONCEPT]** OpenVLA (open weights, 7B): trained on Open-X; outperforms RT-2 on many tasks.
17.7 **[CONCEPT]** π0 (Physical Intelligence): diffusion-based continuous action; high-frequency control.
17.8 **[CONCEPT]** Helix (Figure AI): generalist humanoid VLA with high-frequency upper-body control.
17.9 **[CODE]** Load OpenVLA via HF; run a single inference call (image + text → action).
17.10 **[NB]** OpenVLA in simulation — 10 cells.
17.11 **[CONCEPT]** Safety: action constraints, collision checks, human override; OOD detection.
17.12 **[PROD]** Latency budgets: 30 Hz vs 100 Hz vs 1 kHz control; where each VLA family fits.
17.13 **[CONCEPT]** Open problems: long-horizon tasks, dexterity, generalization across embodiments.
17.14 **[EX]** Plot success rate vs action-noise; identify the failure mode.
17.15 **[READ]** RT-2 (Brohan 2023); OpenVLA (Kim 2024); π0 (Black 2024); Helix tech report.

### Notebook cells (`notebooks/ch17_vla_robotics.ipynb`)
1. Setup; install openvla + simulator (LIBERO).
2. Load LIBERO-Spatial task.
3. Run OpenVLA zero-shot evaluation.
4. Visualize attention rollouts over scene.
5. Inject Gaussian noise on actions; measure success rate degradation.
6. Compare with a behavior-cloning baseline.
7. Tweak text instruction; show command-following.
8. Per-task success table.
9. Render a successful rollout MP4.
10. Save the experiment report.

### Glossary additions
Embodied AI, VLA, policy, behavior cloning, action token, discrete vs continuous action heads, teleop, sim-to-real, OOD.

### References
RT-2; OpenVLA; π0; Helix; Open X-Embodiment.

---

## Chapter 18 — Domain-Specific Vision: Medical, Autonomous, Geospatial, Agricultural

**Reading:** 60 min · **Notebook:** ~50 min · **Difficulty:** ★★★☆☆ · **Words:** ~3,000

**Prereqs:** Ch 7, 8, 10.
**You'll be able to:**
- Train a MONAI-based chest-X-ray model and report calibration honestly.
- Read a BEV perception architecture and understand sensor-fusion at a high level.
- Apply geospatial CV (segment-geospatial, Earth foundation models) to satellite imagery.

### Detailed TOC
18.0 **[HOOK]** A 2026 weed-detection paper combining DINOv3 + YOLO26 — your book's domain example written by someone else.
18.1 **[CONCEPT]** Why domain matters: data shift, label noise, regulatory, deployment constraints.
18.2 **[CONCEPT]** Medical: MONAI ecosystem; nnU-Net's "no manual tuning" recipe.
18.3 **[CONCEPT]** Medical regulatory: FDA SaMD basics; documentation; calibration vs accuracy.
18.4 **[NB]** Chest-X-ray classification with MONAI — 7 cells.
18.5 **[CONCEPT]** Autonomous driving: perception stack (detection, segmentation, depth, BEV).
18.6 **[CONCEPT]** BEV transformations; BEVFormer architecture; lift-splat-shoot.
18.7 **[CONCEPT]** Sensor fusion: camera + LiDAR + radar; late vs mid vs early fusion.
18.8 **[CONCEPT]** Lane detection, drivable-area segmentation, occupancy grids.
18.9 **[NB]** Toy BEV perception demo — 5 cells.
18.10 **[CONCEPT]** Geospatial: segment-geospatial; SAM-style foundation models for Earth observation.
18.11 **[CODE]** Segment a satellite tile of farmland in 6 lines.
18.12 **[CONCEPT]** Agriculture: weed/disease detection; UAV imagery; the DINOv3 + YOLO26 pattern.
18.13 **[PROD]** Deploying domain models: edge constraints (Ch 19), data-pipeline failure modes.
18.14 **[EX]** Replace MONAI U-Net with SAM 3 + Grounding DINO zero-shot; report Dice gap.
18.15 **[READ]** nnU-Net (Isensee 2021); BEVFormer (Li 2022); segment-geospatial docs; arXiv 2603.00160.

### Notebook cells (`notebooks/ch18_domains.ipynb`)
1. Load NIH ChestX-ray14 subset.
2. MONAI DenseNet-121 fine-tune.
3. Calibration plot (reliability diagram).
4. Compare to SAM 3 + linear probe.
5. Load a nuScenes mini sample.
6. Toy BEVFormer-style transformation.
7. Visualize BEV grid.
8. segment-geospatial farmland segmentation.
9. Save reports.

### Glossary additions
MONAI, nnU-Net, BEV, lift-splat-shoot, sensor fusion, occupancy grid, calibration, reliability diagram, geospatial foundation model.

### References
MONAI; nnU-Net; BEVFormer; segment-geospatial; arXiv 2603.00160.

---

## Chapter 19 — Optimization and Edge Deployment

**Reading:** 50 min · **Notebook:** ~40 min · **Difficulty:** ★★★★☆ · **Words:** ~2,800

**Prereqs:** Ch 7 weights; access to a Jetson or CPU edge.
**You'll be able to:**
- Quantize a model to INT8 and verify accuracy degradation is acceptable.
- Export to ONNX → TensorRT and benchmark latency on Jetson Orin Nano.
- Pick the right runtime per platform (TensorRT / OpenVINO / CoreML / TFLite).

### Detailed TOC
19.0 **[HOOK]** A startup that cut inference cost 12× by going INT8 + TensorRT — and the bug they hit doing it.
19.1 **[CONCEPT]** Why edge: latency, privacy, cost, offline.
19.2 **[DEF]** PTQ vs QAT; INT8, FP16, FP8, BF16; calibration set.
19.3 **[THEORY]** Quantization error; per-tensor vs per-channel; symmetric vs asymmetric.
19.4 **[CONCEPT]** Pruning: structured (channels) vs unstructured; magnitude vs movement.
19.5 **[CONCEPT]** Knowledge distillation: teacher → student; logit / feature distillation.
19.6 **[CONCEPT]** ONNX as the lingua franca; opset versioning gotchas.
19.7 **[CODE]** Export YOLO26 → ONNX in 3 lines.
19.8 **[CONCEPT]** Runtime engines: TensorRT (NVIDIA), OpenVINO (Intel), CoreML (Apple), TFLite (mobile), Triton (server).
19.9 **[CONCEPT]** Edge platforms: Jetson Orin (Nano/NX/AGX), Raspberry Pi 5 + Hailo, mobile NPUs.
19.10 **[NB]** YOLO26 INT8 → TensorRT → Jetson Orin Nano — 8 cells.
19.11 **[CONCEPT]** Honest benchmarks: throughput, P50/P95/P99 latency, watts, cost.
19.12 **[PROD]** Common edge bugs: dynamic shapes, fp16 overflow, custom ops missing.
19.13 **[EX]** Quantize a CLIP ViT-B/32 to INT8; measure retrieval-recall@10 drop.
19.14 **[READ]** Jacob et al. 2018 (PTQ); Hinton et al. 2015 (distillation); TensorRT docs.

### Notebook cells (`notebooks/ch19_edge_deployment.ipynb`)
1. Load YOLO26 best.pt from Ch 7.
2. Calibration set selection.
3. PTQ to INT8 in PyTorch.
4. ONNX export.
5. TensorRT engine build.
6. Latency benchmark on T4.
7. Latency benchmark on Jetson Orin Nano (instructions; user runs locally).
8. Record P50/P95/P99 and watts.

### Glossary additions
PTQ, QAT, calibration set, per-channel quantization, structured pruning, distillation, ONNX, opset, TensorRT engine, dynamic shapes.

### References
Jacob 2018; Hinton 2015; ONNX docs; TensorRT samples.

---

## Chapter 20 — MLOps, Responsible AI, and the Future of Computer Vision

**Reading:** 60 min · **Notebook:** ~40 min · **Difficulty:** ★★★☆☆ · **Words:** ~3,000

**Prereqs:** Any deployable model (Ch 7 or Ch 19 outputs).
**You'll be able to:**
- Set up data versioning (DVC), experiment tracking (W&B/MLflow), and drift detection.
- Run a Grad-CAM/SHAP analysis and write a Model Card.
- Reason about EU AI Act categorization for a vision system.

### Detailed TOC
20.0 **[HOOK]** A model that hit 99% offline and silently failed 18% of the time in production — the monitoring that would have caught it.
20.1 **[CONCEPT]** End-to-end production loop: data → label → train → eval → ship → monitor → re-label.
20.2 **[CONCEPT]** Data versioning with DVC; why folders + Git aren't enough.
20.3 **[CONCEPT]** Label management: Label Studio, Roboflow Annotate; QA workflows.
20.4 **[CONCEPT]** Active learning: uncertainty / disagreement / coreset selection.
20.5 **[CONCEPT]** Drift detection: population stability, embedding drift, performance proxies.
20.6 **[CONCEPT]** Model monitoring: input distribution, prediction distribution, latency SLIs.
20.7 **[CONCEPT]** A/B testing for vision: shadow, dark-launch, canary.
20.8 **[CONCEPT]** CI/CD for ML: MLflow / W&B / DVC pipelines; reproducibility.
20.9 **[NB]** Production capstone — 10 cells.
20.10 **[CONCEPT]** Explainability: Grad-CAM, integrated gradients, SHAP, Captum.
20.11 **[CONCEPT]** Bias auditing: subgroup performance, fairness metrics, datasheet for datasets.
20.12 **[CONCEPT]** Privacy: federated learning, differential privacy for vision.
20.13 **[CONCEPT]** Legal frontier: EU AI Act risk categorization, content provenance / C2PA.
20.14 **[CONCEPT]** Looking forward: by 2028 — unified VLA agents, neural rendering as default, on-device foundation models.
20.15 **[EX]** Pick one model from Ch 7/8/13. Write its Model Card + run a fairness slice.
20.16 **[READ]** Sculley 2015 (Hidden Tech Debt); Gebru 2018 (Datasheets); Mitchell 2019 (Model Cards); EU AI Act.

### Notebook cells (`notebooks/ch20_mlops_capstone.ipynb`)
1. Set up DVC for the case-study dataset.
2. Set up MLflow tracking server.
3. Train + log a YOLO26 (re-run from Ch 7).
4. Grad-CAM saliency maps with `pytorch-grad-cam`.
5. SHAP value computation on classifier outputs.
6. Subgroup-slice fairness eval.
7. Build drift-detection script (KS-test on embeddings).
8. Write Model Card markdown.
9. FastAPI serving + Prometheus metrics.
10. Final capstone diagram + executive summary.

### Glossary additions
Data versioning, drift, dark-launch, canary, Grad-CAM, integrated gradients, datasheet, model card, federated learning, differential privacy, EU AI Act, C2PA.

### References
Sculley 2015; Selvaraju 2017 (Grad-CAM); Gebru 2018; Mitchell 2019; EU AI Act text; C2PA spec.

---

## How to use these lesson plans

**Daily:** open the chapter you're drafting, work top-to-bottom through the typed sections.
Each `[HOOK]/[DEF]/[CONCEPT]/[THEORY]/[CODE]/[NB]/[PROD]/[EX]/[READ]` is one writable unit
(~150–250 words for prose units; 1–3 cells for notebook units).

**Weekly:** check off completed sections in `chapters/chXX/README.md`. The draft checklist
in each chapter README mirrors the section list here.

**Cross-chapter:** the **forward links** (e.g., Ch 8 → Ch 10 frozen-backbone exercise,
Ch 10 → Ch 11 retrieval, Ch 12 → Ch 16 ControlNet-Depth, Ch 17 → Ch 19 edge VLA)
are intentional. Preserve them so the book reads as a single arc, not 20 islands.
