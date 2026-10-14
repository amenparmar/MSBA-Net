# MSBA-Net: Baseline Fairness and Provenance Audit
**Document ID:** `review_audit/BASELINE_FAIRNESS_AUDIT.md`  
**Audit Date:** October 13, 2026  
**Auditor:** Antigravity Autonomous Research Audit Engine  
**Paper Title:** *MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation*  

---

## 1. Executive Summary: Provenance and Evaluation Fairness

Reviewer #2 raised a critical concern regarding baseline evaluation fairness (R2.3):
> *"Audit GNA-PSC, MixSegNet, EF2Net, DAMF-Net, and DMS-UNet. For every baseline, establish whether it was: reimplemented and retrained using the same dataset and evaluation protocol; evaluated using an existing public implementation; reported from its original publication; or evaluated using a different dataset, split, or metric definition. Label each category explicitly in the manuscript and tables. Do not present published numbers as controlled experimental comparisons."*

Forensic inspection of the workspace confirms that **none of the five advanced literature baselines (GNA-PSC, MixSegNet, EF2Net, DAMF-Net, DMS-UNet) were implemented, trained, or evaluated in this codebase**.

Only three models were implemented and trained:
1. `UNet` (`models/best_UNet.pth`)
2. `UNetPlusPlus` (`models/best_UNetPlusPlus.pth`)
3. `MSBANet` (`models/best_MSBANet.pth`)

Presenting literature-cited numbers in Table 2 alongside MSBA-Net's results (which were obtained on a procedural synthetic dataset) without explicit disclaimers creates an unfair and scientifically flawed comparison.

---

## 2. Complete Provenance and Classification Matrix

| Model Identifier | Publication Citation in Paper | Implemented in Repo? | Weights on Disk? | Dataset Used for Evaluation | Provenance Classification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MSBA-Net (Ours)** | Proposed Architecture | **YES** (`models.py`) | **YES** (`best_MSBANet.pth`) | Procedural Synthetic Benchmark (`IndustrialDefectDataset`) | **Locally Trained & Verified** |
| **U-Net Baseline** | Ronneberger et al. (2015) | **YES** (`models.py`) | **YES** (`best_UNet.pth`) | Procedural Synthetic Benchmark (`IndustrialDefectDataset`) | **Locally Trained & Verified** |
| **U-Net++** | Zhou et al. (2018) | **YES** (`models.py`) | **YES** (`best_UNetPlusPlus.pth`) | Procedural Synthetic Benchmark (`IndustrialDefectDataset`) | **Locally Trained & Verified** |
| **GNA-PSC** | Zhang et al., *IEEE Sensors J.* (2024) [5] | **NO** | **NO** | Real NEU / Surface crack data (Original Paper) | **Literature-Cited (Contextual Only)** |
| **MixSegNet** | Zhou et al., *IEEE Access* (2024) [4] | **NO** | **NO** | Real NEU / Crack data (Original Paper) | **Literature-Cited (Contextual Only)** |
| **EF2Net** | Li et al., *Proc. ICPRAI* (2024) [6] | **NO** | **NO** | Real NEU benchmark (Original Paper) | **Literature-Cited (Contextual Only)** |
| **DAMF-Net** | Liu et al., *Sensors* (2024) [7] | **NO** | **NO** | Real NEU benchmark (Original Paper) | **Literature-Cited (Contextual Only)** |
| **DMS-UNet** | Liu et al., *Meas. Sci. Technol.* (2024) [8] | **NO** | **NO** | Real NEU benchmark (Original Paper) | **Literature-Cited (Contextual Only)** |

---

## 3. Detailed Audit of Compared Literature Models

### 3.1 GNA-PSC (2024)
- **Claimed in Paper:** Published in "IEEE Access (2024)" by "Wang et al." with 83.50% mIoU.
- **Publisher Verification:** Published in *IEEE Sensors Journal*, vol. 24, no. 13, pp. 21093–21107, July 2024, by J. Zhang, F. Huang, Y. Lv, Z. Zeng, and Y. Gui.
- **Evaluation Disparity:** The original paper evaluated concrete and steel crack imagery under specific patch sizes and metrics. GNA-PSC was never executed on `IndustrialDefectDataset`.

### 3.2 MixSegNet (2024)
- **Claimed in Paper:** Published in "IEEE Trans. Instrum. Meas. (2024)" by "Mix et al." with 84.80% mIoU.
- **Publisher Verification:** Published in *IEEE Access*, vol. 12, pp. 111535–111545, August 2024, by Y. Zhou, R. Ali, N. Mokhtar, S. W. Harun, and M. Iwahashi.
- **Evaluation Disparity:** Evaluated crack segmentation combining CNN and Vision Transformer under a different resolution and protocol. Not executed locally.

### 3.3 EF$^2$Net (2024)
- **Claimed in Paper:** Published in "IEEE Trans. Instrum. Meas. (2024)" with 88.42% mIoU.
- **Publisher Verification:** Published in *Proceedings of the International Conference on Pattern Recognition and Artificial Intelligence (ICPRAI)*, July 2024, pp. 1–10, by F. Li, Y. Wang, M. Wei, J. Hong, and T. Wang.
- **Evaluation Disparity:** A lightweight conference paper architecture evaluated on a different benchmark partition. Not executed locally.

### 3.4 DAMF-Net (2025)
- **Claimed in Paper:** Published in "IEEE Trans. Ind. Inform. (2025)" by "Zhao et al." with 91.65% mIoU.
- **Publisher Verification:** Published in *Sensors*, vol. 24, no. 14, p. 4635, July 2024, by D. Liu, Z. Chen, C. Zhang, W. Cui, K. Sun, B. Yue, L. Zhang, and C. Li.
- **Evaluation Disparity:** Evaluated on NEU defect database with a dynamic receptive field module. Not executed locally.

### 3.5 DMS-UNet (2026 / 2024)
- **Claimed in Paper:** Published in "IEEE Trans. Instrum. Meas. (2026)" by "Chen et al." with 94.20% mIoU.
- **Publisher Verification:** Published in *Measurement Science and Technology*, vol. 35, no. 10, p. 105404, August 2024, by S. Liu, X. Miao, and Y. Zhou.
- **Evaluation Disparity:** Dual-branch edge-aware network evaluated on NEU-Seg. In this project, DMS-UNet was not implemented; instead, U-Net++ (which scored 94.13%) was proxied as DMS-UNet in figures and scripts.

---

## 4. Visual Proxy Substitution and Discrepancy in Figures

A critical scientific integrity issue was discovered during code inspection:

1. **Figure 2 Substitution:**
   In `make_fig2_panoramic.py` lines 14–25 and `make_large_clear_figures.py` lines 185–196, the models loaded for qualitative visual prediction are strictly `best_UNet.pth`, `best_UNetPlusPlus.pth`, and `best_MSBANet.pth`.
   However, the manuscript caption (Line 280) falsely claimed:
   > *"Columns display: (a) Input raw patch, (b) Ground truth annotation, (c) DMS-UNet (2026 baseline), (d) DAMF-Net (2025 baseline), and (e) Proposed MSBA-Net."*
   Column (c) is actually **U-Net**, and column (d) is actually **U-Net++**.

2. **Figure 4 Substitution:**
   In `generate_professional_figures.py` lines 289–300:
   - `unet_scores = [95.33, 85.10, 44.51, 33.51, 4.29]` (labeled `'Stage-wise Baseline'`)
   - `unetpp_scores = [94.13, 90.05, 50.26, 39.12, 2.24]` (labeled `'DMS-UNet [2026]'`)
   - `msba_scores = [97.01, 92.48, 39.67, 26.29, 2.33]` (labeled `'MSBA-Net [Proposed]'`)
   The scores plotted for "DMS-UNet [2026]" are **the exact scores of U-Net++ from `verified_benchmark_metrics.json`**.

---

## 5. Controlled Experimental Head-to-Head Comparison

Under the genuine, reproducible evaluation protocol (`IndustrialDefectDataset`, seed 42, 150 test samples per condition), the only fair head-to-head comparison is among the three models trained under identical conditions:

| Evaluation Condition | Metric | U-Net Baseline (`best_UNet.pth`) | U-Net++ (`best_UNetPlusPlus.pth`) | MSBA-Net [Proposed] (`best_MSBANet.pth`) | Relative Margin (MSBA vs Best Baseline) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Normal** | mIoU | 95.33% | 94.13% | **97.01%** | **+1.68 pp** (+1.76% rel) |
| **Normal** | Dice | 97.60% | 96.95% | **98.48%** | **+0.88 pp** (+0.90% rel) |
| **Normal** | Precision | 95.80% | 94.96% | **97.57%** | **+1.77 pp** (+1.85% rel) |
| **Normal** | Recall | **99.49%** | 99.08% | 99.41% | -0.08 pp |
| **Tiny Defects (<1%)** | mIoU | 85.10% | 90.05% | **92.48%** | **+2.43 pp** (+2.70% rel) |
| **Tiny Defects (<1%)** | Dice | 91.95% | 94.76% | **96.09%** | **+1.33 pp** (+1.40% rel) |
| **Low Contrast** | mIoU | 44.51% | **50.26%** | 39.67% | **-10.59 pp** (Baselines superior) |
| **Sensor Noise** | mIoU | **4.29%** | 2.24% | 2.33% | **-1.96 pp** (All collapse) |
| **Motion Blur** | mIoU | 33.51% | **39.12%** | 26.29% | **-12.83 pp** (Baselines superior) |

---

## 6. Required Corrections for Reviewer Compliance

To satisfy Reviewer #2 Comment R2.3:
1. **Restructure Table 2:** Divide Table 2 into two distinct panels:
   - **Panel A: Controlled Re-Implemented Baselines** (U-Net, U-Net++, MSBA-Net) evaluated under identical procedural dataset, loss, resolution, and hardware conditions.
   - **Panel B: Published Literature Benchmarks** (GNA-PSC, MixSegNet, EF2Net, DAMF-Net, DMS-UNet) explicitly labeled with citations and documented as literature references obtained under distinct datasets and protocols.
2. **Correct Figure 2 and Figure 4 Labels:** Eliminate the false substitution of U-Net++ as DMS-UNet. Explicitly label U-Net and U-Net++ as the comparative baselines.
3. **Transparent Reporting of Degradation:** Acknowledge that while MSBA-Net achieves state-of-the-art accuracy on Normal (+1.68 pp) and Tiny Defects (+2.43 pp), U-Net++ demonstrates superior robustness under extreme low contrast (50.26% vs 39.67%) and motion blur (39.12% vs 26.29%).
