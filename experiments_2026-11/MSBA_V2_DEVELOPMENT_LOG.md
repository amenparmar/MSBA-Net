# MSBA-Net v2: development log (2026-11-18)

The author asked overnight for the model to be improved ("go whatever you think is right ... I want my model to be best overall").

## Rules
- Every design choice was made on **validation** data only.
- Test scores were read only after a design was fixed.
- Every variant tried is listed below, including the failures, so the paper can report the search honestly.

## Motivation
MSBA-Net's full-resolution decoder gives it an advantage on tiny defects. On NEU-Seg, however, it lost to the models that aggregate wide or global context: HRNet-W18, SegFormer-B1 and DeepLabv3+. Every v2 candidate adds a context module to MSBA-Net and keeps the rest of the author's network unchanged (`msba_v2.py`). With the module set to identity, the output is identical to `MSBANet`; this was checked.

## Variants tried (validation scores)

| Variant | What it adds | Params (M) | NEU-Seg val s42 | NEU-Seg val s100 | KolektorSDD2 val s42 | Decision |
|---|---|---|---|---|---|---|
| MSBA-Net (author) | none | 8.65 | 77.26 | 77.35 | 51.50 | baseline |
| v2a | dilated context (rates 1, 2, 4, 8) + image pooling on the 1/16 bottleneck | 10.88 | 78.27 | 78.34 | 56.89 | kept, superseded by v2c |
| v2b | 2 transformer blocks on the bottleneck | 10.51 | 77.32 | not run | 45.55 | rejected |
| **v2c** | **v2a + a dilated-context module on the 1/8 encoder feature** | **11.44** | **78.50** | **78.66** | (stage 3) | **selected** (best mean NEU-Seg val, 78.58) |
| v2d | v2a with two stacked bottleneck modules | 13.11 | 78.79 | 78.22 | not run | rejected (mean 78.51, larger) |

Reference validation scores, NEU-Seg s42 / s100:

| Model | s42 | s100 |
|---|---|---|
| HRNet-W18 | 78.94 | 79.08 |
| DeepLabv3+ | 78.40 | 78.06 |
| SegFormer-B1 | 78.24 | 78.19 |
| U-Net | 76.25 | 76.03 |

## Test results of v2a (design fixed before test was read)

**NEU-Seg test mIoU, 3 seeds:** 79.71 ± 0.15.

| v2a vs. | Difference | p |
|---|---|---|
| MSBA-Net | +0.90 | 0.004 |
| U-Net | +2.06 | <0.001 |
| U-Net++ | +1.89 | <0.001 |
| Attention U-Net | +2.12 | 0.003 |
| DeepLabv3+ | −0.19 | 0.215 (n.s.) |
| SegFormer-B1 | −0.28 | 0.172 (n.s.) |
| HRNet-W18 | −0.93 | 0.006 |

**Synthetic, 5 seeds:**

| Condition | v2a | vs MSBA-Net | vs U-Net | vs Attention U-Net |
|---|---|---|---|---|
| Normal | 99.79 ± 0.07 | +0.01 | | |
| Tiny defects | 98.47 ± 0.28 | −0.04 (same) | +0.93 (p = 0.003) | +0.91 (p = 0.013) |

**KolektorSDD2, s42:** val 56.89, the best of all models, but test IoU 39.68 (MSBA-Net 40.12, U-Net 41.02), with 13 of 30 small defects found. The validation set has only 26 defective images, so validation on this dataset is noisy. More seeds are needed.

## Test results of v2c (the selected model; design fixed before test was read)

**NEU-Seg test mIoU, 3 seeds:** **80.31 ± 0.17** (per seed: 80.16 / 80.28 / 80.50). Paired t-tests, not yet Holm-corrected:

| v2c vs. | Difference | p |
|---|---|---|
| HRNet-W18 | −0.33 | 0.041 |
| SegFormer-B1 | +0.32 | 0.003 |
| DeepLabv3+ | +0.42 | 0.055 |
| v2a | +0.60 | 0.049 |
| MSBA-Net | +1.51 | 0.004 |
| U-Net++ | +2.50 | 0.003 |
| U-Net | +2.67 | 0.002 |
| Attention U-Net | +2.73 | 0.001 |

**Synthetic, 5 seeds:** paired-test p-values in parentheses.

| Condition | v2c | vs MSBA-Net | vs U-Net | vs Attention U-Net | vs HRNet / SegFormer / DeepLabv3+ |
|---|---|---|---|---|---|
| Normal | 99.81 ± 0.03 | +0.03 (0.314) | +0.24 (0.040) | +0.26 (0.033) | +31 to +43 |
| Tiny defects | 98.52 ± 0.22 | +0.01 (0.951) | +0.99 (0.008) | +0.97 (0.001) | +16 to +31 |

Under blur and noise (no augmentation), v2c is as weak as MSBA-Net.

The architecture search stopped after four variants (v2a to v2d) to limit selection effects.

## Diagnostic ablations on KolektorSDD2 (s42)
The false blobs are predicted components that touch no ground truth.

| Variant | Val | Test IoU | False blobs | Small found / 30 |
|---|---|---|---|---|
| MSBA-Net | 51.50 | 40.12 | 282 | 18 |
| without BGFF (Arch3) | 52.48 | 38.95 | 109 | 14 |
| without boundary loss | 51.36 | 40.33 | 74 | 19 |

A minimum-component-area filter, chosen on validation and applied to every model, removes most false blobs: MSBA-Net 282 → 49 with no small defect lost (`ksdd2_postproc.json`).

## Protocol notes for the paper
- **U-Net++ on KolektorSDD2** used gradient accumulation (2 × 8). It needs 13 GB at batch 16 × 672 × 256 and the GPU has 12 GB. BatchNorm and Dice therefore see 8 images at a time, so this run is not exactly equivalent to batch 16.
- **KolektorSDD2 training data on the GPU** is stored as uint8 (`compact=True`). This was verified to give a bit-exact round trip.
- **The seed-42 v2a, v2b and ablation runs on KolektorSDD2 were run while other configurations were also being tried.** They must be listed as development runs.
