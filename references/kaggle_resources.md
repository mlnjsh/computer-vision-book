# Kaggle Resources

Free GPU strategy for the entire book — Kaggle's T4×2 / P100 with 30 hrs/week
free is enough for ~80% of the hands-on projects.

## Setup (one-time)

1. Generate API token: kaggle.com → Account → Create New API Token → save `kaggle.json`
2. Place in `~/.kaggle/kaggle.json` (Linux/Mac) or `C:\Users\<you>\.kaggle\kaggle.json` (Windows)
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
