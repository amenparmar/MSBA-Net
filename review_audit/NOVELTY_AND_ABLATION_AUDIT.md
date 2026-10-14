# MSBA-Net: Architectural Novelty and Component Ablation Audit
**Document ID:** `review_audit/NOVELTY_AND_ABLATION_AUDIT.md`  
**Audit Date:** October 13, 2026  
**Auditor:** Antigravity Autonomous Research Audit Engine  
**Paper Title:** *MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation*  

---

## 1. Executive Summary: Novelty Claims vs Scientific Literature

Reviewer #2 raised two interconnected concerns regarding architectural claims and ablation rigor:
- **R2.6 (Novelty):** Clearly delineate what is adapted from prior art vs what is genuinely novel; avoid claiming basic operators (dilated conv, attention gating, edge loss) as standalone novel inventions.
- **R2.7 (Ablation Studies):** Verify whether existing ablation experiments isolate individual components and whether reported intermediate configurations are supported by reproducible checkpoints and logs.

Forensic analysis of the codebase reveals that:
1. **Implementation vs Mathematical Narrative:** The manuscript repeatedly claims that MSFP uses *dilated depthwise separable convolutions*. In `models.py`, the actual implementation uses **standard 2D convolutions (`nn.Conv2d`)**.
2. **Missing Ablation Evidence:** While `models/` contains checkpoints for `best_UNet.pth`, `best_UNetPlusPlus.pth`, and `best_MSBANet.pth`, **zero checkpoints or training logs exist for the intermediate ablation configurations** reported in Table 4 ("+ MSFP Blocks", "+ BAS Boundary Stream") and Table 5 (loss component ablations).

---

## 2. Architectural Novelty Deconstruction Against Prior Art

| Architectural Component | Claimed Novelty in Manuscript | Actual Code Implementation (`models.py`) | Prior Art in Literature | Genuine Scientific Contribution |
| :--- | :--- | :--- | :--- | :--- |
| **Multi-Scale Feature Preservation (MSFP)** | "Four parallel dilated depthwise separable convolutional streams ($r \in \{1, 2, 4\}$)" | 4 parallel standard Conv2d branches (1x1, 3x3 $r=1$, 3x3 $r=2$, 3x3 $r=4$) + 1x1 fuse + residual shortcut | ASPP (Chen et al., ECCV 2018), RFBNet (Liu et al., ECCV 2018), TridentNet (Li et al., ICCV 2019) | Embedding parallel multi-dilation branches with residual identity inside *every early encoder stage* to prevent $<1\%$ hairline crack features from vanishing before pooling. |
| **Auxiliary Boundary-Aware Stream (BAS)** | "Dedicated boundary stream extracting high-resolution contour cues from shallow encoder layers" | 2-stage transpose convolution decoder merging Stage 3, Stage 2, and Stage 1 features to predict 1-ch boundary contour | Gated-SCNN (Takikawa et al., ICCV 2019), BASNet (Qin et al., CVPR 2019), Edge-Aware UNet | Lightweight auxiliary boundary prediction directly off shallow encoder features without instantiating an expensive secondary full-depth decoder. |
| **Boundary-Guided Feature Fusion (BGFF)** | "Spatial attention gating network to regulate main segmentation decoder representations" | 1x1 Conv + Sigmoid gate $\mathbf{G} \in [0, 1]$, modulating decoder via $\tilde{\mathbf{F}} = \text{Conv}((1 + \mathbf{G}) \odot \mathbf{F})$ | Attention U-Net (Oktay et al., MIDL 2018), Reverse Attention (Chen et al., ECCV 2018) | Coupling predicted morphological boundary probabilities directly into the primary segmentation decoder via residual multiplicative gating $(1 + \mathbf{G}) \odot \mathbf{F}$. |
| **Composite Loss Formulation** | "Adaptive four-part composite loss ($\mathcal{L}_{\text{BCE}} + \mathcal{L}_{\text{Dice}} + \mathcal{L}_{\text{Focal}} + \mathcal{L}_{\text{bound}}$)" | Weighted sum of BCE, Soft Dice, Focal, and Edge boundary losses | Boundary Loss (Kervadec et al., MedIA 2021), Focal Loss (Lin et al., ICCV 2017) | Multi-objective optimization balancing extreme spatial foreground imbalance ($>98\%$ background) with perimeter gradient penalties. |

### 2.1 Scientific Framing Recommendation
- **What should NOT be claimed as novel:** Dilated convolutions, depthwise separable convolutions, spatial attention gates, and morphological boundary supervision are well-established primitives in computer vision. Claiming these operations as independent mathematical inventions is scientifically indefensible.
- **What SHOULD be claimed as novel:** The **systematic architectural integration** of multi-rate dilated residual blocks across early encoder stages coupled with an auxiliary boundary stream that actively modulates primary decoder features via residual spatial gating $(1 + \mathbf{G}) \odot \mathbf{F}$ specifically tuned for micro-scale and low-contrast steel flaws.

---

## 3. Forensic Audit of Existing Ablation Experiments

### 3.1 Architectural Ablation (Table 4) Audit
Table 4 in `ieee_access_msba_net.tex` reports:
- Baseline Backbone: 94.10% mIoU, 96.90% Dice, 84.60% Tiny mIoU, 7.76M Params
- + MSFP Blocks: 95.85% mIoU, 97.88% Dice, 89.65% Tiny mIoU, 8.42M Params
- + BAS Boundary Stream: 96.48% mIoU, 98.21% Dice, 91.20% Tiny mIoU, 9.15M Params
- + BGFF Gate (MSBA-Net): 97.01% mIoU, 98.48% Dice, 92.48% Tiny mIoU, 9.38M Params

*Evidence Verification:*
1. **Baseline Backbone:** In `models/best_UNet.pth`, the actual trained U-Net baseline achieved **95.33% mIoU**, not 94.10%. Table 4 under-reports the baseline by -1.23 pp.
2. **Intermediate Configurations:** Search of `models/` reveals that **no checkpoints exist for "+ MSFP alone" or "+ MSFP + BAS alone"**.
3. **Parameter Counts:**
   - Real Baseline (UNet): 7,762,465 (7.76M) — Matches Table 4 row 1.
   - Real UNet++: 9,159,105 (9.16M) — Corresponds to Table 4 row 3 ("+ BAS").
   - Real MSBA-Net: 8,650,786 (8.65M) — **Contradicts Table 4 row 4 (9.38M)**.

### 3.2 Composite Loss Ablation (Table 5) Audit
Table 5 in `ieee_access_msba_net.tex` reports:
- $\mathcal{L}_{\text{BCE}}$ only: 93.85% mIoU, 96.83% Dice, 88.40% Boundary Prec
- $\mathcal{L}_{\text{BCE}} + \mathcal{L}_{\text{Dice}}$: 95.33% mIoU, 97.60% Dice, 91.20% Boundary Prec
- $\mathcal{L}_{\text{BCE}} + \mathcal{L}_{\text{Dice}} + \mathcal{L}_{\text{Focal}}$: 96.12% mIoU, 98.02% Dice, 93.15% Boundary Prec
- Full Composite Loss: 97.01% mIoU, 98.48% Dice, 97.57% Boundary Prec

*Evidence Verification:*
1. **Missing Intermediate Weights:** No checkpoints or training logs exist for $\mathcal{L}_{\text{BCE}}$ only, $+ \mathcal{L}_{\text{Dice}}$, or $+ \mathcal{L}_{\text{Focal}}$.
2. **Metric Copy-Paste Anomaly:** In the final row, Boundary Precision is reported as **97.57%**. This value is identical to the overall segmentation Precision in Table 2 and Table 3. In `losses.py`, boundary precision is not separately calculated by `calculate_metrics()`.

---

## 4. Controlled Component-Ablation Experiment Specification

To place the ablation findings on rigorous, defensible ground without fabricating numbers, the following controlled experimental protocol is designed:

### 4.1 Architectural Component Factorial Study
| Run ID | Configuration | MSFP Module | BAS Edge Stream | BGFF Gate | Target Evaluation |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Arch-1** | Baseline Backbone | $\times$ | $\times$ | $\times$ | Isolate stage-wise convolutional baseline |
| **Arch-2** | + MSFP | $\checkmark$ | $\times$ | $\times$ | Isolate multi-rate dilation micro-crack preservation |
| **Arch-3** | + MSFP + BAS (Loss Only)| $\checkmark$ | $\checkmark$ | $\times$ | Isolate boundary supervision without spatial gating |
| **Arch-4** | MSBA-Net (Full Architecture)| $\checkmark$ | $\checkmark$ | $\checkmark$ | Evaluate full network with boundary gating |

### 4.2 Composite Loss Factorial Study
| Run ID | Loss Combination | $\mathcal{L}_{\text{BCE}}$ | $\mathcal{L}_{\text{Dice}}$ | $\mathcal{L}_{\text{Focal}}$ | $\mathcal{L}_{\text{bound}}$ | Target Objective |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Loss-1** | BCE Only | $1.0$ | $0.0$ | $0.0$ | $0.0$ | Standard pixel-level cross-entropy baseline |
| **Loss-2** | BCE + Soft Dice | $1.0$ | $1.0$ | $0.0$ | $0.0$ | Evaluate regional overlap regularization |
| **Loss-3** | BCE + Dice + Focal | $1.0$ | $1.0$ | $0.5$ | $0.0$ | Evaluate hard-mining class balance regularization |
| **Loss-4** | Full Composite Loss | $1.0$ | $1.0$ | $0.5$ | $0.4$ | Evaluate full boundary-supervised objective |

### 4.3 Computational Resource Requirements
- **Dataset:** `IndustrialDefectDataset` ($700$ training images, $150$ validation images, $256 \times 256$ resolution).
- **Optimization:** AdamW ($\text{lr} = 1 \times 10^{-3}$, weight decay $= 1 \times 10^{-4}$), Cosine Annealing, batch size $16$, $12$ epochs per run.
- **Compute Time:** Approximately $45–60$ seconds per training run on an NVIDIA RTX 4090 GPU (or $\sim 3–4$ minutes on CPU).
- **Total Experiment Budget:** $6$ additional training runs $\approx 5–6$ minutes total GPU compute time.

---

## 5. Audit Compliance Determination

- **Current Status:** **EVIDENCE UNAVAILABLE / NEW EXPERIMENT REQUIRED**.
- **Action Plan:**
  1. Until fresh ablation training runs are executed, Table 4 and Table 5 must be clearly labeled as preliminary exploratory runs.
  2. The paper narrative must replace the copy-pasted boundary precision (97.57%) with genuine segmentation metrics.
  3. Narrative novelty claims must be revised to emphasize architectural integration and multi-rate feature preservation rather than claiming standard convolutional operators as novel inventions.
