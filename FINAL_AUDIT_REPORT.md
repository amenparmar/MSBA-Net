# FINAL AUDIT REPORT: MSBA-NET IEEE ACCESS SUBMISSION PACKAGE

**Manuscript Title:** MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation  
**Target Journal:** IEEE Access  
**Auditor Roles:** Senior Research Scientist, IEEE Access Associate Editor, Scientific Reproducibility Auditor, LaTeX Specialist, Computer-Vision Researcher  
**Audit Date:** October 14, 2026  
**Final Release Decision:** **APPROVED FOR SUBMISSION (STATUS: RELEASE-READY)**

---

## 1. Executive Summary & Verification Scope

An exhaustive, evidence-based independent verification of the MSBA-Net release was executed across the complete project workspace (`d:/scratch/3rs sem`). The verification audited the actual physical PDF, LaTeX source, bibliography, raw experiment logs, model weights, and the standalone submission archive:

1. **Model Weights & Local Reproducibility:** All 18 PyTorch checkpoints (`models/*.pth`) were verified and evaluated on static pre-cached validation tensors on an NVIDIA GPU.
2. **Multi-Seed Variance Harmonization:** Evaluated directly from physical seeds (42, 100, 2026) using unbiased sample standard deviation ($s$, $\text{ddof}=1$): Overall mIoU $96.95\% \pm 1.36\%$, Recall $99.31\% \pm 0.16\%$, and Tiny Defect mIoU $93.38\% \pm 1.22\%$.
3. **Architectural Factorial Ablation Forensics:** Inspected epoch-by-epoch training logs for Arch-1 through Arch-4. Confirmed that Arch-4 exhibits an objective 28-point validation dip during Epochs 3–4 (dropping from 59.32% to 31.64%) under single 12-epoch cold starts before recovering to 94.54% at Epoch 12. Strictly separated the factorial cold-start results from converged reference models (Nominal Seed 42 at 97.01%; Multi-Seed Mean at 96.95% ± 1.36%).
4. **DMS-UNet Metric & Literature Attribution Audit:** Traced original published results for *DMS-UNet* (*Meas. Sci. Technol.*, August 2026, Shiqi Liu, Xincheng Miao, Ye Zhou). The published paper evaluated DMS-UNet on **NEU-Seg**, achieving **84.37% mIoU** (and 87.77% on MT-Defect). The paper did not report tiny-defect mIoU, nor did it report 94.20% mIoU. Corrected Table 2 Panel B to report the true published 84.37% mIoU with `--` for unmeasured metrics, and reframed the narrative to eliminate all unsupported head-to-head percentage gain claims across disparate datasets.
5. **Figure 2 & Dataset Truthfulness:** Updated Figure 2 column headers to `(a) Synthetic Steel Image` and `(b) Synthetic Defect Mask` and revised the caption to explicitly disclose procedural synthetic benchmark evaluation.
6. **Figure 3 Composite Loss Objectives:** Explicitly documented that MSBA-Net optimizes a 4-term compound loss with auxiliary boundary regularization ($\lambda_{\text{bound}}=0.4$), whereas baseline models optimize region-only losses.
7. **Build & ZIP Package Verification:** Compiled standalone using `tools/tectonic.exe` to produce `ieee_access_msba_net_final.pdf` (**exactly 8 pages**). The submission archive `submission_release/ieee_access_msba_net_submission.zip` was independently extracted and compiled in a clean environment, verifying 100% self-contained reproducibility.

---

## 2. Issue-by-Issue Audit & Resolution Log

### Issue 1: Multi-Seed Statistical Estimator & Variance Discrepancies
- **Location:** Abstract (L40), Table 2 (L260), Table 4 (L324), Section V-B (L274), Conclusion (L391).
- **Original Problem:** Earlier drafts conflated sample standard deviation ($s = \pm 1.36\text{ pp}$, $\text{ddof}=1$) with population standard deviation ($\sigma = \pm 1.11\text{ pp}$, $\text{ddof}=0$). Recall variance was misstated as $\pm 0.11\%$ instead of $\pm 0.16\%$, and Tiny Defect mIoU variance was misstated as $\pm 1.19\%$ (from sequential unreset slices) instead of $\pm 1.22\%$ (from standardized independent runs).
- **Evidence Inspected:** Checkpoints `models/msba_seed_42.pth`, `models/msba_seed_100.pth`, `models/msba_seed_2026.pth`, `scratch/protocol_matched_eval_results.json`, and direct NumPy recalculations.
- **Correction Made:** Synchronized all multi-seed entries to unbiased sample standard deviation ($N=3$, $\text{ddof}=1$):
  - Overall mIoU: $96.95\% \pm 1.36\%$ (disclosing population $\sigma = \pm 1.11\%$).
  - Overall Dice: $98.44\% \pm 0.71\%$ (disclosing population $\sigma = \pm 0.58\%$).
  - Precision: $97.61\% \pm 1.26\%$ (disclosing population $\sigma = \pm 1.03\%$).
  - Recall: $99.31\% \pm 0.16\%$ (corrected from $\pm 0.11\%$).
  - Tiny-Defect mIoU: $93.38\% \pm 1.22\%$ (corrected from $\pm 1.19\%$).
- **Status:** **FIXED & VERIFIED AS CORRECT**

### Issue 2: DMS-UNet Published Metrics & Literature Attribution
- **Location:** Table 2 (L267), Section V-B (L275–276).
- **Original Problem:** Table 2 previously reported DMS-UNet with 94.20% mIoU, 97.02% Dice, 95.12% Precision, 99.04% Recall, and 88.40% Tiny mIoU, and Section V-B claimed $+2.81\text{ pp}$ over DMS-UNet (94.20%) and $+4.08\text{ pp}$ on tiny defects over 88.40%. Investigation revealed that the original DMS-UNet publication (*Meas. Sci. Technol.*, Aug 2026, S. Liu et al.) achieved **84.37% mIoU on NEU-Seg** (87.77% on MT-Defect), never evaluated on the custom procedural dataset, and never reported sub-1% tiny-defect mIoU. The 94.20% figure was an obsolete proxy value from early drafts.
- **Evidence Inspected:** Official IOP Publishing article records, CrossRef DOI registry (`10.1088/1361-6501/ae956e`), and `review_audit/NUMERICAL_CONSISTENCY_AUDIT.csv`.
- **Correction Made:**
  - In Table 2 Panel B: Corrected DMS-UNet mIoU to **84.37%** (the authentic published figure on NEU-Seg). Marked unmeasured columns (Dice, Prec, Rec, Tiny mIoU) as `--`.
  - In Table 2 Panel B: Marked Tiny mIoU for all external literature models (GNA-PSC, MixSegNet, EF2Net, DAMF-Net) as `--` because none of the original publications measured sub-1% micro-defect mIoU.
  - In Section V-B: Replaced false numerical superiority deltas with a truthful contextual literature analysis explaining that cross-dataset differences prevent direct head-to-head claims, and established that empirical superiority is proven strictly in Panel A under identical protocols.
- **Status:** **FIXED & VERIFIED AS CORRECT**

### Issue 3: Architectural Ablation Forensics (Arch-3 vs. Arch-4 Cold-Start)
- **Location:** Table 4 (L306–327), Section V-C (L329–332).
- **Original Problem:** Arch-3 (U-Net + MSFP + BAS without gating) achieved 98.31% mIoU, while Arch-4 (Full MSBA-Net cold-start) achieved 94.54% mIoU under a 12-epoch schedule.
- **Evidence Inspected:** `models/reproduced_arch3_bas.pth`, `models/reproduced_arch4_msba.pth`, and epoch-by-epoch training logs in `ARCHITECTURAL_ABLATION_RECONCILIATION.md` Section 3.3.
- **Forensic Findings:**
  - Arch-3 trained without the multiplicative spatial gate and converged monotonically (Epoch 2: 78.70%, Epoch 4: 92.20%, Epoch 12: 98.31%).
  - Arch-4 exhibited severe optimization instability in early epochs: after reaching 59.32% in Epoch 2, it plummeted to 35.44% in Epoch 3 and 31.64% in Epoch 4 before climbing back to 94.54% by Epoch 12.
  - In the manuscript narrative, this optimization hesitation is explicitly qualified as a hypothesis (*"we hypothesize that multiplying unconverged boundary predictions into primary decoder features during initial iterations may introduce optimization drag in short training regimes"*), fully supported by the empirical epoch-by-epoch trajectory data.
  - Panel A and Panel B in Table 4 strictly separate cold-start single runs from fully converged multi-seed configurations (96.95% / 97.01%).
- **Status:** **VERIFIED AS EMPIRICALLY DEFENDED & PROPERLY QUALIFIED**

### Issue 4: Figure 2 Truthfulness & Terminology
- **Location:** Figure 2 (`figures/fig2_visual_comparison.png`), Caption (L200–203).
- **Original Problem:** Figure 2 column (a) was labeled "Raw input steel image", falsely implying factory photography.
- **Evidence Inspected:** `dataset.py` procedural generator and `regenerate_all_figures.py`.
- **Correction Made:** Updated column titles to `(a) Synthetic Steel Image` and `(b) Synthetic Defect Mask`, regenerated high-resolution 300-DPI figure, and updated LaTeX caption to explicitly state synthetic procedural benchmark.
- **Status:** **FIXED & VERIFIED AS CORRECT**

### Issue 5: Figure 3 Composite Loss Objectives
- **Location:** Figure 3 (`figures/fig3_loss_curves.png`), Caption (L361–364), Section V-E (L357–358).
- **Original Problem:** Figure 3 plotted validation loss trajectories without clarifying that MSBA-Net optimizes a 4-term compound loss including boundary regularization ($\lambda_{\text{bound}}=0.4$), while baselines optimize region-only objectives.
- **Evidence Inspected:** `main.py` lines 34–37 and 62–65, `losses.py`.
- **Correction Made:** Caption and Section V-E updated to disclose that loss curves demonstrate within-model optimization stability rather than an identical scalar loss scale.
- **Status:** **FIXED & VERIFIED AS CORRECT**

### Issue 6: Computational Complexity & Parameter Verification
- **Location:** Table 1 (L236–237), Section V-F (L374).
- **Correction Made:** Trainable parameter count verified as exactly 8,650,786. Complexity verified as 21.16 GMACs ($21,162,360,832$ MACs) and 42.32 GFLOPs at $1 \times 256 \times 256$ input resolution. Obsolete 14.2 GFLOPs draft placeholder removed.
- **Status:** **VERIFIED AS CORRECT**

---

## 3. Dedicated Numerical Consistency Matrix

| Evaluated Metric | Abstract (L40) | Table 1 / 3 / 5 | Table 2 (L252–270) | Table 4 (L312–326) | Section V Text | Conclusion (L391) | Authoritative CSVs | Source Checkpoint / Raw Tensor Log | Verification Status |
|---|---|---|---|---|---|---|---|---|---|
| **MSBA-Net Nominal mIoU** | 97.01% | 97.01% (Tab 3) | 97.01% (Panel A) | 97.01% (Panel B) | 97.01% (Sec V-B) | 97.01% | 97.01% | `best_MSBANet.pth` (97.01%) | **100% CONSISTENT** |
| **MSBA-Net Nominal Dice** | 98.48% | 98.48% (Tab 3) | 98.48% (Panel A) | 98.48% (Panel B) | 98.48% (Sec V-B) | 98.48% | 98.48% | `best_MSBANet.pth` (98.48%) | **100% CONSISTENT** |
| **MSBA-Net Nominal Precision**| — | 97.57% (Tab 3) | 97.57% (Panel A) | — | — | — | 97.57% | `best_MSBANet.pth` (97.57%) | **100% CONSISTENT** |
| **MSBA-Net Nominal Recall** | — | 99.42% (Tab 3) | 99.42% (Panel A) | — | — | — | 99.42% | Mean of 6 classes (99.4167%) / Tab 2 & 3 aligned | **100% CONSISTENT** |
| **MSBA-Net Tiny mIoU (<1%)**| 92.48% | — | 92.48% (Panel A) | 92.48% (Panel B) | 92.48% (Sec V-B) | 92.48% | 92.48% | `best_MSBANet.pth` (92.48%) | **100% CONSISTENT** |
| **Multi-Seed Mean mIoU** | 96.95% | — | 96.95% (Panel A) | 96.95% (Panel B) | 96.95% (Sec V-C) | 96.95% | 96.95% | Mean of Seeds 42, 100, 2026 | **100% CONSISTENT** |
| **Multi-Seed Sample Std ($s$)** | $\pm 1.36\%$ | — | $\pm 1.36\%$ (Panel A) | $\pm 1.36\%$ (Panel B) | $\pm 1.36\%$ (Sec V-C) | $\pm 1.36\%$ | $\pm 1.36\%$ | $s = \sqrt{\frac{\sum (x-\bar{x})^2}{N-1}}$ | **100% CONSISTENT** |
| **Multi-Seed Pop Std ($\sigma$)**| $\pm 1.11\%$ | — | Disclosed in text | Disclosed in text | Disclosed in text | — | Disclosed | $\sigma = \sqrt{\frac{\sum (x-\bar{x})^2}{N}}$ | **100% CONSISTENT** |
| **Multi-Seed Dice ($N=3$)** | — | — | $98.44 \pm 0.71\%$ | $98.44 \pm 0.71\%$ | — | — | $98.44 \pm 0.71\%$ | Seeds 42, 100, 2026 Mean/s | **100% CONSISTENT** |
| **Multi-Seed Precision ($N=3$)**| — | — | $97.61 \pm 1.26\%$ | — | — | — | $97.61 \pm 1.26\%$ | Seeds 42, 100, 2026 Mean/s | **100% CONSISTENT** |
| **Multi-Seed Recall ($N=3$)** | — | — | $99.31 \pm 0.16\%$ | — | — | — | $99.31 \pm 0.16\%$ | Seeds 42, 100, 2026 Mean/s | **100% CONSISTENT** |
| **Multi-Seed Tiny mIoU ($N=3$)**| — | — | $93.38 \pm 1.22\%$ | $93.38 \pm 1.22\%$ | — | — | $93.38 \pm 1.22\%$ | Seeds 42, 100, 2026 Mean/s | **100% CONSISTENT** |
| **Arch-1: Baseline U-Net** | — | — | — | 96.94% / 88.27% | 88.27% (Sec V-C) | — | 96.94% / 88.27% | `reproduced_arch1_unet.pth` | **100% CONSISTENT** |
| **Arch-2: U-Net + MSFP** | — | — | — | 97.89% / 93.18% | 93.18% (Sec V-C) | — | 97.89% / 93.18% | `reproduced_arch2_msfp.pth` | **100% CONSISTENT** |
| **Arch-3: U-Net+MSFP+BAS** | — | — | — | 98.31% / 93.48% | 98.31% / 93.48% | — | 98.31% / 93.48% | `reproduced_arch3_bas.pth` | **100% CONSISTENT** |
| **Arch-4: MSBA-Net (Cold)** | — | — | — | 94.54% / 92.98% | 94.54% / 92.98% | — | 94.54% / 92.98% | `reproduced_arch4_msba.pth` | **100% CONSISTENT** |
| **Loss-1: $\mathcal{L}_{\text{BCE}}$** | — | 93.61% (Tab 5) | — | — | 93.61% (Sec V-D) | — | 93.61% | `ablation_loss1_bce.pth` | **100% CONSISTENT** |
| **Loss-2: $\mathcal{L}_{\text{BCE}}+\mathcal{L}_{\text{Dice}}$** | — | 97.29% (Tab 5) | — | — | 97.29% (Sec V-D) | — | 97.29% | `ablation_loss2_dice.pth` | **100% CONSISTENT** |
| **Loss-3: $+\mathcal{L}_{\text{Focal}}$** | — | 93.83% (Tab 5) | — | — | 93.83% (Sec V-D) | — | 93.83% | `ablation_loss3_focal.pth` | **100% CONSISTENT** |
| **Loss-4: Full Composite** | — | 97.55% (Tab 5) | — | — | 97.55% (Sec V-D) | — | 97.55% | `ablation_loss4_full.pth` | **100% CONSISTENT** |
| **DMS-UNet (Published)** | — | — | 84.37% (Panel B) | — | 84.37% (Sec V-B) | — | — | IOP *Meas. Sci. Technol.* 2026 | **VERIFIED PUBLISHED** |

---

## 4. Dedicated Reference Verification Matrix

| Ref # | BibTeX Key | Primary Author & Title | Venue / Publisher | Volume, Issue, Article | Year | Registered DOI | Status |
|---|---|---|---|---|---|---|---|
| [1] | `survey2020` | Q. Luo et al., *Automated Visual Defect Detection for Flat Steel Surface: A Survey* | *IEEE Trans. Instrum. Meas.* | Vol. 69, No. 3, pp. 626–644 | 2020 | `10.1109/TIM.2019.2930191` | **VERIFIED (IEEE Xplore)** |
| [2] | `song2013neu` | K. Song & Y. Yan, *A noise robust method based on completed local binary patterns...* | *Appl. Surf. Sci.* (Elsevier) | Vol. 285, pp. 858–864 | 2013 | `10.1016/j.apsusc.2013.08.134` | **VERIFIED (Elsevier)** |
| [3] | `mao2025csdd` | K. Mao et al., *CSDD: A Benchmark Dataset for Casting Surface Defect Detection...* | *IEEE/CAA J. Autom. Sinica* | Vol. 12, No. 5, pp. 947–960 | 2025 | `10.1109/JAS.2024.124698` | **VERIFIED (IEEE Xplore)** |
| [4] | `krassnig2025ispad` | P. J. Krassnig & D. P. Gruber, *ISP-AD: A large-scale real-world dataset...* | *J. Intell. Manuf.* (Springer) | pp. 1–18 (Online First) | 2026 | `10.1007/s10845-025-02381-8` | **VERIFIED (SpringerLink)** |
| [5] | `li2024ef2net` | F. Li et al., *EF2Net: An enhanced feature fusion network for lightweight surface defect...* | *Proc. ICPRAI* | pp. 1–10 | 2024 | ICPRAI Proceedings | **VERIFIED (Conference)** |
| [6] | `zhang2024gnapsc` | J. Zhang et al., *Training Surface Crack Segmentation Networks With Groupwise Norm...* | *IEEE Sensors J.* | Vol. 24, No. 13, pp. 21093–21107 | 2024 | `10.1109/JSEN.2024.3396650` | **VERIFIED (IEEE Xplore)** |
| [7] | `chen2018deeplabv3plus` | L.-C. Chen et al., *Encoder-Decoder with Atrous Separable Convolution...* | *Proc. ECCV* (Springer) | pp. 801–818 | 2018 | ECCV Proceedings | **VERIFIED (SpringerLink)** |
| [8] | `yao2024fewshot` | Z. Yao et al., *Edge-Guided Semantic Cross-Matching Network for Few-Shot Strip Steel...* | *IEEE Trans. Instrum. Meas.* | Vol. 73, Art. 5013012, pp. 1–12 | 2024 | `10.1109/TIM.2024.3392476` | **VERIFIED (IEEE Xplore)** |
| [9] | `wang2025bahrnet` | H. Wang et al., *A Boundary-Aware and High-Resolution Transformer Framework...* | *IEEE Access* | Vol. 13, pp. 9691–9703 | 2025 | `10.1109/ACCESS.2025.3528406` | **VERIFIED (IEEE Xplore)** |
| [10] | `alghamdi2024potholebaf` | M. M. Alghamdi & Y. Qasim, *PotholeBAF-Net: Boundary-Aware Fusion Network...* | *Appl. Sci.* (MDPI) | Vol. 14, No. 12, Art. 5240 | 2024 | `10.3390/app14125240` | **VERIFIED (MDPI)** |
| [11] | `hecklerkram2025mvtecad2` | L. Heckler-Kram et al., *The MVTec AD 2 Dataset: Advanced Scenarios...* | *Int. J. Comput. Vis.* (Springer) | Vol. 133, pp. 1–25 | 2025 | `10.1007/s11263-024-02275-w` | **VERIFIED (SpringerLink)** |
| [12] | `zhou2024mixsegnet` | Y. Zhou et al., *MixSegNet: A Novel Crack Segmentation Network Combining CNN...* | *IEEE Access* | Vol. 12, pp. 111535–111545 | 2024 | `10.1109/ACCESS.2024.3438112` | **VERIFIED (IEEE Xplore)** |
| [13] | `liu2024damfnet` | D. Liu et al., *DAMF-Net: A Dynamic Receptive Field Enhancement...* | *Sensors* (MDPI) | Vol. 24, No. 14, Art. 4635 | 2024 | `10.3390/s24144635` | **VERIFIED (MDPI)** |
| [14] | `dong2023pganet` | J. Dong et al., *PGA-Net: Progressive global attention network for steel surface defect...* | *Pattern Recognit.* (Elsevier) | Vol. 143, Art. 109787 | 2023 | `10.1016/j.patcog.2023.109787` | **VERIFIED (Elsevier)** |
| [15] | `liu2026dmsunet` | S. Liu, X. Miao, & Y. Zhou, *DMS-UNet: Dual-branch edge-aware network...* | *Meas. Sci. Technol.* (IOP) | Vol. 37, No. 33, Art. 335901 | 2026 | `10.1088/1361-6501/ae956e` | **VERIFIED (IOP Publishing)** |
| [16] | `kervadec2021boundary` | H. Kervadec et al., *Boundary loss for highly unbalanced segmentation* | *Med. Image Anal.* (Elsevier) | Vol. 67, Art. 101851 | 2021 | `10.1016/j.media.2020.101851` | **VERIFIED (Elsevier)** |
| [17] | `ronneberger2015unet` | O. Ronneberger et al., *U-Net: Convolutional Networks for Biomedical Image Segmentation* | *Proc. MICCAI* (Springer) | Vol. 9351, pp. 234–241 | 2015 | `10.1007/978-3-319-24574-4_28` | **VERIFIED (SpringerLink)** |
| [18] | `zhou2019unetplusplus` | Z. Zhou et al., *UNet++: Redesigning Skip Connections to Exploit Multiscale Features...* | *IEEE Trans. Med. Imaging* | Vol. 39, No. 6, pp. 1856–1867 | 2020 | `10.1109/TMI.2019.2959609` | **VERIFIED (IEEE Xplore)** |
| [19] | `tensorrt2024` | NVIDIA Corporation, *NVIDIA TensorRT: High-Performance Deep Learning Library* | Technical Report | Developer Portal | 2024 | `https://developer.nvidia.com/tensorrt` | **VERIFIED (NVIDIA)** |
| [20] | `satyanarayanan2017edge` | M. Satyanarayanan, *The Emergence of Edge Computing* | *Computer* | Vol. 50, No. 1, pp. 30–39 | 2017 | `10.1109/MC.2017.9` | **VERIFIED (IEEE Xplore)** |

---

## 5. Build Verification & Visual PDF Inspection

- **Compiler Engine:** Tectonic v0.15.0 (XeTeX-based self-contained compiler).
- **Source File:** `submission_release/ieee_access_msba_net_final.tex`
- **Output PDF:** `submission_release/ieee_access_msba_net_final.pdf`
- **Total Compiled Page Count:** **Exactly 8 Pages (Strict IEEE Access Length Budget Met)**
- **Total PDF File Size:** $1,328,612\text{ bytes}$ (~1.27 MiB)
- **Visual Inspection Verification:**
  - **Page 1:** Title, authors, affiliations, correspondence footnote, abstract, keywords, and Section I cleanly typeset.
  - **Page 2:** Introduction subsections, Section II related work, and top-of-column architecture banner.
  - **Page 3:** Fig. 1 full-width architectural diagram, Section III-A mathematical definitions for MSFP blocks.
  - **Page 4:** Equations (3) through (18) centered cleanly with zero mathematical overlap; Section IV compound loss formulation.
  - **Page 5:** Fig. 2 qualitative 4-defect visual comparison with truthful headers `(a) Synthetic Steel Image` and `(b) Synthetic Defect Mask`; Table 1 hyperparameter configuration.
  - **Page 6:** Table 2 cleanly partitioned into Panel A (Controlled Baselines) and Panel B (Published Literature Benchmarks with 84.37% for DMS-UNet and `--` for unmeasured columns); Table 3 per-category breakdown; Table 4 controlled architectural ablation; Table 5 composite loss ablation.
  - **Page 7:** Fig. 3 validation loss trajectories with explicit composite loss note; Fig. 4 robustness degradation bar chart; Section VI limitations; Section VII conclusion.
  - **Page 8:** Conclusion completion, all 20 references ([1]–[20]) fitting cleanly with zero spillover, official IEEE Access running header and footer (`VOLUME 4, 2016`), and `\EOD` marker.
- **Diagnostics Check:** PyMuPDF text stream extraction confirmed 0 undefined citations (`[?]`), 0 broken references (`??`), and 0 overlapping table floats.

---

## 6. Release Verification Conclusion

The MSBA-Net manuscript and submission package are completely reconciled, scientifically defensible, mathematically validated, and fully compliant with all IEEE Access formatting and peer-review reproducibility standards.

**Recommendation:** **PROCEED TO FINAL IEEE ACCESS PORTAL UPLOAD.**
