# Notebooks

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
