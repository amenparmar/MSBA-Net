# MSBA-Net: Baseline Manuscript and Artifact Inventory
**Document ID:** `review_audit/BASELINE_INVENTORY.md`  
**Audit Date:** October 13, 2026  
**Auditor:** Antigravity Autonomous Research Audit Engine  
**Paper Title:** *MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation*  
**Authors:** Amen Parmar (Graduate Student Member, IEEE), Amit Kumar Bairwa (Senior Member, IEEE), Varun Kumar (Member, IEEE)  
**Affiliation:** Department of Computer Science and Engineering, Manipal University Jaipur, Jaipur, Rajasthan 303007, India  
**Target Venue:** IEEE Access  

---

## 1. Executive Identification of Authoritative Sources

| Artifact Category | Primary Workspace Path | Compiled Output / Reference | Verified Status & Integrity |
| :--- | :--- | :--- | :--- |
| **Active LaTeX Manuscript** | `ieee_access_msba_net.tex` (46,151 bytes) | `ieee_access_msba_net.pdf` (1,208,155 bytes) | Master working source; uses `ieeeaccess.cls` |
| **Secondary Entrypoint** | `main.tex` (46,746 bytes) | Identical body to `ieee_access_msba_net.tex` | Differs only in Abstract wording (earlier expanded draft) |
| **Legacy / Draft Source** | `access.tex` (45,709 bytes) | `access.log` | Contains older corrupted/placeholder bib items |
| **Conference Version** | `icaiit2026_defect_paper.tex` (39,530 bytes) | `icaiit2026_defect_paper.pdf` | ICAIIT 2026 conference variant |
| **Bibliography Source** | `references.bib` (6,094 bytes) | 18 `@article` / `@inproceedings` entries | Critical metadata discrepancies identified |
| **Core Architecture Code** | `models.py` (11,484 bytes) | Implements `ConvBlock`, `UNet`, `UNetPlusPlus`, `MSBANet` | Uses standard convs instead of depthwise separable convs |
| **Dataset & Synthesis Code** | `dataset.py` (10,478 bytes) | `IndustrialDefectDataset` class | Procedural synthetic generator; NO raw NEU image files on disk |
| **Loss & Metric Code** | `losses.py` (3,702 bytes) | `CompositeLoss`, `calculate_metrics` | Loss weights differ between code, paper, and figure |
| **Pipeline & Training Code**| `main.py` (14,715 bytes) | 12 epochs training script | Trains UNet, UNet++, MSBANet; generates figures |
| **Metric Verification Script**| `verify_metrics.py` (3,344 bytes) | Re-evaluates saved weights | Generates `results/verified_benchmark_metrics.json` |
| **Saved Model Weights** | `models/` directory | `best_MSBANet.pth` (34.7 MB), `best_UNet.pth` (31.1 MB), `best_UNetPlusPlus.pth` (36.7 MB) | Weights verified; only 3 models exist |
| **Saved Metric Results** | `results/` directory | `benchmark_metrics.json`, `verified_benchmark_metrics.json` | Ground truth numerical record of experiments |
| **Publication Figures** | `figures/` directory | `fig1_architecture.png`, `fig2_visual_comparison.png`, `fig3_loss_curves.png`, `fig4_degraded_benchmark.png` | Identified critical caption and labeling discrepancies |

---

## 2. Model Implementation Inventory & Parameter Verification

Architectural implementations in `models.py` were independently executed and evaluated on PyTorch:

| Model Identifier | Architectural Description in Manuscript | Actual Implementation in Code | Implemented Parameter Count | Manuscript Claimed Parameters | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MSBANet** | 4-Stage Encoder + MSFP (dilations 1,2,4) + BAS + BGFF Gate | `ConvBlock` + `MultiScaleFeaturePreservation` (standard Conv2d) + BAS + BGFF | **8,650,786 (8.65 M)** | **9.38 M** (Table 1, Table 4, Section V.H) | **DISCREPANCY:** Under-reported in implementation by 0.73M vs manuscript |
| **UNet** | Standard U-Net baseline | 4-level encoder/decoder with transpose convs | **7,762,465 (7.76 M)** | **7.76 M** (Table 4 Baseline Backbone) | **VERIFIED MATCH** |
| **UNetPlusPlus**| Nested dense skip U-Net++ | 5-level dense nested feature aggregation | **9,159,105 (9.16 M)** | Not explicitly declared as UNet++; used as proxy for DMS-UNet | **VERIFIED MATCH** with Table 4 "+ BAS" row (9.15M) |
| **GNA-PSC** | Groupwise Normalization Attention + PSC | **NOT IMPLEMENTED** | None | 83.50% mIoU (Cited from literature) | **EVIDENCE UNAVAILABLE** |
| **MixSegNet** | CNN-Transformer hybrid | **NOT IMPLEMENTED** | None | 84.80% mIoU (Cited from literature) | **EVIDENCE UNAVAILABLE** |
| **EF2Net** | Enhanced feature fusion network | **NOT IMPLEMENTED** | None | 88.42% mIoU (Cited from literature) | **EVIDENCE UNAVAILABLE** |
| **DAMF-Net** | Dynamic receptive field + adaptive fusion | **NOT IMPLEMENTED** | None | 91.65% mIoU (Cited from literature) | **EVIDENCE UNAVAILABLE** |
| **DMS-UNet** | Dual-branch edge-aware network | **NOT IMPLEMENTED** | None | 94.20% mIoU (Cited from literature) | **EVIDENCE UNAVAILABLE**; UNet++ used as visual substitute |

---

## 3. Dataset & Ground-Truth Annotation Inventory

| Dataset Dimension | Claim in Manuscript (`ieee_access_msba_net.tex`) | Physical Reality in Workspace (`dataset.py`) | Discrepancy Analysis |
| :--- | :--- | :--- | :--- |
| **Data Source** | Benchmark NEU Surface Defect Database (1,800 real images) | Procedural synthetic texture generator in NumPy/SciPy | **CRITICAL DISCREPANCY:** Zero real NEU images exist in workspace. All images are dynamically synthesized. |
| **Data Partitioning** | 70% Train (1,260), 15% Val (270), 15% Test (270) | `num_samples=700` (Train), `num_samples=150` (Val/Test) | Sample sizes differ (700 train vs 1,260 claimed; 150 test vs 270 claimed). |
| **Ground Truth Masks**| Standard manual human annotations from NEU-Seg benchmark | Procedurally generated synthetic shapes (cracks, ellipses, blobs) via `_synthesize_defect()` | Ground truth is generated via algorithmic math, not annotated raw steel photos. |
| **Boundary Masks** | Derived via $3 \times 3$ flat structuring element | Derived via `ndimage.binary_dilation(iterations=2)` and `binary_erosion(iterations=1)` with default connectivity 1 | Default connectivity produces a cross (not square), and 2+1 iterations yield a 3-pixel ribbon. |

---

## 4. Numerical Results Extraction & Comparison Matrix

Extracted from `results/verified_benchmark_metrics.json` vs Manuscript narrative and tables:

| Model / Condition | Metric | Verified Evidence (`verified_benchmark_metrics.json`) | Manuscript Table 2 / Narrative Claim | Discrepancy |
| :--- | :--- | :--- | :--- | :--- |
| **MSBA-Net (Normal)** | mIoU | **97.01%** | **97.01%** (Table 2, Abstract) | Exact Match |
| **MSBA-Net (Normal)** | Dice | **98.48%** | **98.48%** (Table 2, Abstract) | Exact Match |
| **MSBA-Net (Normal)** | Precision | **97.57%** | **97.57%** (Table 2) | Exact Match |
| **MSBA-Net (Normal)** | Recall | **99.41%** | **99.41%** (Table 2) | Exact Match |
| **MSBA-Net (Tiny)** | $\text{mIoU}_{\text{tiny}}$ | **92.48%** | **92.48%** (Table 2, Abstract) | Exact Match |
| **UNet (Normal)** | mIoU | **95.33%** | 94.10% (Table 4 Baseline Backbone) | Discrepancy: Table 4 reports 94.10%, verified is 95.33% |
| **UNetPlusPlus (Normal)**| mIoU | **94.13%** | 94.20% (Cited as DMS-UNet in Table 2) | Proxied in figures; UNet++ achieved 94.13% |
| **MSBA-Net (Low-Contrast)**| mIoU | **39.67%** | Line 417: "retains 39.67% mIoU, outperforming baseline models" | **FALSE CLAIM:** UNet achieved **44.51%** and UNet++ achieved **50.26%**. MSBA-Net performed WORSE than baselines! |
| **MSBA-Net (Sensor Noise)**| mIoU | **2.33%** | Line 417: "MSBA-Net registering 2.33% mIoU" | Exact Match (model collapses under noise) |
| **MSBA-Net (Motion Blur)**| mIoU | **26.29%** | Line 417: "MSBA-Net attains 26.29% mIoU" | Exact Match; UNet was 33.51%, UNet++ was 39.12% |

---

## 5. Figures and Equations Inventory

1. **Figure 1 (`fig1_architecture.png`):**
   - Shows MSBA-Net architecture with MSFP block inset, BAS stream, BGFF gate, and supervision loss box.
   - Discrepancy in loss box text: Displays $\mathcal{L}_{total} = 0.4\mathcal{L}_{BCE} + 0.6\mathcal{L}_{Dice} + 0.3\mathcal{L}_{Focal} + 0.5\mathcal{L}_{Boundary}$, whereas manuscript text specifies $\alpha=0.3, \beta=0.3, \gamma=0.2, \lambda=0.2$, and code uses $1.0, 1.0, 0.5, 0.4$.
2. **Figure 2 (`fig2_visual_comparison.png`):**
   - Shows 4 defect rows across 5 columns.
   - Column headers in image: `(a) Raw Steel Surface`, `(b) Ground Truth Defect`, `(c) U-Net Baseline [MICCAI'15]`, `(d) U-Net++ [IEEE TMI'18]`, `(e) MSBA-Net [Proposed]`.
   - **Severe Discrepancy:** Caption in `ieee_access_msba_net.tex` line 280 states columns display: `(c) DMS-UNet (2026 baseline)`, `(d) DAMF-Net (2025 baseline)`, which does NOT match the generated figure or the underlying code.
3. **Figure 3 (`fig3_loss_curves.png`):**
   - Displays validation loss curves across 12 epochs.
   - **Severe Discrepancy:** Caption in `ieee_access_msba_net.tex` line 396 states: "across 100 epochs, demonstrating stable and monotonic optimization" and mentions mIoU trajectories which are absent.
4. **Figure 4 (`fig4_degraded_benchmark.png`):**
   - Displays bar chart comparing conditions: Normal, Tiny Defects, Low Contrast, Motion Blur, Sensor Noise.
   - In `generate_professional_figures.py`, U-Net++ was relabeled as `DMS-UNet [2026]`.
5. **Equations:**
   - Equation (1): Morphological boundary definition using structuring element $\mathbf{K}_3$.
   - Equations (4)–(7): MSFP parallel branches. Text claims depthwise separable convs; code implements standard convs.
   - Equation (8): Receptive field formula $R_k = k + (k-1)(r-1)$. Formula represents kernel dilated footprint span, not cumulative network receptive field.
   - Equation (18): Loss weighting parameters $\alpha=0.3, \beta=0.3, \gamma=0.2, \lambda=0.2$. Symbol collision between loss weight $\alpha$ and Focal loss balancing parameter $\alpha_t=0.25$.

---

## 6. Genuinely Conducted vs Cited Experiments Determination

- **Genuinely Conducted Experiments:**
  1. Training of `UNet`, `UNetPlusPlus`, and `MSBANet` on synthetic procedural dataset (`IndustrialDefectDataset`) for 12 epochs under seed 42.
  2. Evaluation of these 3 models under 5 conditions (normal, low_contrast, noise, blur, tiny_defects) saved in `verified_benchmark_metrics.json`.
  3. Inference qualitative masks for Figure 2 using procedural generator.
- **Cited / Literature / Proxy Numbers (NOT Conducted in Repository):**
  1. GNA-PSC (83.50% mIoU, 88.20% Dice, etc.) — cited from literature.
  2. MixSegNet (84.80% mIoU, 91.50% Dice, etc.) — cited from literature.
  3. EF2Net (88.42% mIoU, 93.85% Dice, etc.) — cited from literature.
  4. DAMF-Net (91.65% mIoU, 95.60% Dice, etc.) — cited from literature.
  5. DMS-UNet (94.20% mIoU, 97.02% Dice, etc.) — cited from literature; U-Net++ used as proxy in figures.
  6. Intermediate Ablation Checkpoints (Table 4 "+ MSFP", "+ BAS") — no checkpoints or training logs exist.
  7. Loss Component Ablations (Table 5 BCE only, BCE+Dice, BCE+Dice+Focal) — no checkpoints or training logs exist.
  8. TensorRT FP16 benchmarking (88.5 FPS, 11.3 ms) — no TensorRT code or logs exist.
