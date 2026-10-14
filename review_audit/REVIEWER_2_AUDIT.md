# MSBA-Net: Reviewer #2 Individual Verification Audit
**Document ID:** `review_audit/REVIEWER_2_AUDIT.md`  
**Audit Date:** October 13, 2026  
**Auditor:** Antigravity Autonomous Research Audit Engine  
**Paper Title:** *MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation*  

---

## Summary of Reviewer #2 Verification

| Comment ID | Topic | Manuscript Location | Verification Status | Primary Finding / Required Action |
| :--- | :--- | :--- | :--- | :--- |
| **R2.1** | Ground Truth Origin | Sec V.A (L287) | **VERIFIED — CORRECTION REQUIRED** | Manuscript falsely claims 1,800 real NEU images; data is 100% procedurally synthesized in `dataset.py`. Disclose procedural synthesis honestly. |
| **R2.2** | Reproducible Protocol | Sec V.A, `dataset.py` | **VERIFIED — CORRECTION REQUIRED** | Procedural dataset uses 700 train / 150 val samples (not 1,260/270/270). Training loader shuffles RNG across epochs. Disclose exact counts and seed behavior. |
| **R2.3** | Baseline Fairness | Table 2, Sec II, Sec V | **VERIFIED — CORRECTION REQUIRED** | GNA-PSC, MixSegNet, EF2Net, DAMF-Net, and DMS-UNet were NEVER trained or evaluated in this codebase. They are literature citations; label them explicitly as such. |
| **R2.4** | Percentage Calculations | Table 2, L314 | **VERIFIED — CORRECTION REQUIRED** | Reported improvements (+13.51%, +2.81%, +4.08%) are absolute differences in percentage points (pp), NOT relative percentages. Define formulas and state both. |
| **R2.5** | Bibliography Metadata | `references.bib` | **VERIFIED — CORRECTION REQUIRED** | 10+ references have fabricated publication years in keys or wrong venues/authors. Table 2 venues and L96–L105 author attributions are severely corrupted. |
| **R2.6** | Novelty of MSFP/BAS/BGFF | Sec I, II, IV | **VERIFIED — CORRECTION REQUIRED** | Code uses standard Conv2d (not depthwise separable). Clarify that architectural integration of multi-dilation + edge gating is the contribution, not basic operators. |
| **R2.7** | Component Ablations | Table 4, Table 5 | **EVIDENCE UNAVAILABLE / NEW EXPERIMENT REQUIRED** | Only 3 checkpoints exist (`UNet`, `UNet++`, `MSBANet`). Intermediate ablation configurations (+MSFP alone, loss variants) have no saved weights or logs. |
| **R2.8** | Statistical Variation | Table 2, Table 3 | **VERIFIED — CORRECTION REQUIRED** | Results represent single-seed runs (seed 42). Disclose absence of multi-run standard deviations as an experimental limitation. |
| **R2.9** | Robustness Evaluation | Sec VI.A, Fig 4 | **VERIFIED — CORRECTION REQUIRED** | Discrepancy between code parameters and text ($\sigma=18$ vs 25, linear 0.45 vs $\gamma=1.8$). Manuscript falsely claims MSBA-Net beat baselines under low contrast; U-Net and U-Net++ actually outperformed MSBA-Net! |
| **R2.10** | Runtime & Model Size | Sec V.H, Table 1 | **VERIFIED — CORRECTION REQUIRED** | Real MSBANet has 8.65M parameters (not 9.38M). TensorRT FP16 benchmarks (88.5 FPS) have no reproducible code or logs on disk. Disclose verified PyTorch profile. |
| **R2.11** | Industrial Deployment | Abstract, Sec I, VI | **VERIFIED — CORRECTION REQUIRED** | No mill-floor or line-scan hardware validation exists. Tone down production-line claims to laboratory/simulated benchmarking and design considerations. |
| **R2.12** | IEEE Template Artifacts | Preamble, Headers | **VERIFIED — CORRECTION REQUIRED** | Remove placeholder DOI, generic IEEE Transactions header, and Volume 4 2016 footer. |
| **R2.13** | Figure/Table Integrity | Figs 1–4, Tabs 1–5 | **VERIFIED — CORRECTION REQUIRED** | Fig 2 caption falsely labels columns as DMS-UNet/DAMF-Net. Fig 3 caption claims 100 epochs vs 12 plotted. Table 1 channels/params/epochs contradict code. |
| **R2.14** | Complete Proofreading | Full Manuscript | **VERIFIED — CORRECTION REQUIRED** | Execute comprehensive proofread ensuring complete cross-consistency among text, math, code, figures, and tables. |

---

## Detailed Item-by-Item Verification

### R2.1 — Segmentation Annotations and Ground Truth Provenance
- **Manuscript Location:** Section V.A (Lines 287–289).
- **Physical Evidence:**
  The manuscript states:
  > "All experimental evaluations are performed on the standard NEU surface defect database benchmark [2], comprising 1,800 grayscale images ($200 \times 200$ pixels) across six defect categories... partitioned into 70% training (1,260 images), 15% validation (270 images), and 15% testing (270 images)..."
  *Physical Workspace Audit:*
  - Search of entire disk confirms that **zero real NEU raw image files or mask files exist in the project**.
  - File `dataset.py` defines `class IndustrialDefectDataset(Dataset)`, which procedurally generates metallic grain textures (`_generate_steel_background`) and defect masks (`_synthesize_defect`) on the fly using NumPy and SciPy.
  - The masks used to train `models/best_MSBANet.pth`, `best_UNet.pth`, and `best_UNetPlusPlus.pth` were generated procedurally by mathematical equations (random walks, dilated lines, ellipses, and Gaussian blobs).
  - Baselines GNA-PSC, MixSegNet, EF2Net, DAMF-Net, and DMS-UNet were **never evaluated on these masks**.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. The manuscript must be completely transparent: disclose that the experimental study evaluates model architectures on a high-fidelity procedural synthetic industrial steel surface defect benchmark modeled after NEU defect morphologies, rather than falsely claiming access to real partitioned NEU-Seg images.

---

### R2.2 — Reproducible Dataset Protocol and Leakage Audit
- **Manuscript Locations:** Section V.A, `dataset.py`, `main.py`.
- **Physical Evidence:**
  1. *Actual Sample Counts:* `train_ds = IndustrialDefectDataset(num_samples=700, mode='train')` and `val_ds = IndustrialDefectDataset(num_samples=150, mode='val')`. The claimed 1,260 / 270 / 270 split does not exist in code.
  2. *Random State Behavior:* In `dataset.py` line 34, `self.rng = np.random.RandomState(seed if mode == 'train' else seed + 1000)`.
  3. *Leakage / Epoch Mutation:* In `main.py`, `train_loader` uses `shuffle=True`. In `__getitem__`, `self.rng` is invoked multiple times per sample. Because the loader shuffles sample access order each epoch, the random state trajectory mutates every epoch, meaning `idx=0` receives different procedural backgrounds and flaws in epoch 1 vs epoch 2.
  4. *Validation Integrity:* `val_loader` uses `shuffle=False`, ensuring deterministic validation samples across runs given seed 1042.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Correct the dataset protocol narrative to reflect exact sample numbers (700 train, 150 validation), document procedural generation parameters, and confirm image-level partition independence.

---

### R2.3 — Baseline Evaluation Fairness
- **Manuscript Locations:** Table 2, Section II, Section V.B.
- **Physical Evidence:**
  Audit of all 5 literature baselines in Table 2:
  1. **GNA-PSC (2024):** No code, no weights, no logs exist. Reported mIoU (83.50%) is cited from literature.
  2. **MixSegNet (2024):** No code, no weights, no logs exist. Reported mIoU (84.80%) is cited from literature.
  3. **EF2Net (2024):** No code, no weights, no logs exist. Reported mIoU (88.42%) is cited from literature.
  4. **DAMF-Net (2025):** No code, no weights, no logs exist. Reported mIoU (91.65%) is cited from literature.
  5. **DMS-UNet (2026):** No code, no weights, no logs exist. Reported mIoU (94.20%) is cited from literature.
  *Fairness Violation:*
  MSBA-Net was evaluated on the local procedural dataset (achieving 97.01%), while the 5 compared models were tested in their original published papers on different real datasets under unknown splits and metric implementations. Comparing these directly without labeling them as cited literature numbers creates an unfair and scientifically invalid comparison.
  Furthermore, in Figure 2 and Figure 4, U-Net++ was visually substituted and relabeled as "DMS-UNet [2026]".
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Table 2 must be partitioned into two distinct blocks: (a) Locally Trained & Controlled Baselines (U-Net, U-Net++, MSBA-Net), and (b) Published Literature Benchmarks (cited for contextual reference with explicit protocol disclaimers). Relabeling in figures must be eliminated.

---

### R2.4 — Table 2 Percentage Improvement Calculations
- **Manuscript Locations:** Table 2, Abstract, Section V.B (Lines 314–315).
- **Physical Evidence:**
  The manuscript reports improvements as:
  - "+13.51% mIoU over GNA-PSC (83.50%)"
  - "+12.21% mIoU over MixSegNet (84.80%)"
  - "+8.59% mIoU over EF2Net (88.42%)"
  - "+5.36% mIoU over DAMF-Net (91.65%)"
  - "+2.81% mIoU over DMS-UNet (94.20%)"
  - "+4.08% mIoU on tiny defects over DMS-UNet (88.40%)"
  - "+16.38% mIoU on tiny defects over MixSegNet (76.10%)"
  *Mathematical Audit:*
  These values are strictly **absolute differences in percentage points (pp)**:
  $$\Delta_{\text{abs}} = M_{\text{MSBA}} - M_{\text{baseline}}$$
  For example, $97.01 - 94.20 = 2.81\text{ pp}$, and $92.48 - 88.40 = 4.08\text{ pp}$.
  However, the manuscript writes "\%" rather than "percentage points" or "pp", leading readers to confuse them with **relative percentage improvements**:
  $$\Delta_{\text{rel}} = \frac{M_{\text{MSBA}} - M_{\text{baseline}}}{M_{\text{baseline}}} \times 100\%$$
  - Over GNA-PSC: $\Delta_{\text{rel}} = \frac{13.51}{83.50} \times 100\% = \mathbf{+16.18\%}$
  - Over MixSegNet: $\Delta_{\text{rel}} = \frac{12.21}{84.80} \times 100\% = \mathbf{+14.40\%}$
  - Over EF2Net: $\Delta_{\text{rel}} = \frac{8.59}{88.42} \times 100\% = \mathbf{+9.71\%}$
  - Over DAMF-Net: $\Delta_{\text{rel}} = \frac{5.36}{91.65} \times 100\% = \mathbf{+5.85\%}$
  - Over DMS-UNet: $\Delta_{\text{rel}} = \frac{2.81}{94.20} \times 100\% = \mathbf{+2.98\%}$
  - Tiny defects over DMS-UNet: $\Delta_{\text{rel}} = \frac{4.08}{88.40} \times 100\% = \mathbf{+4.62\%}$
  - Tiny defects over MixSegNet: $\Delta_{\text{rel}} = \frac{16.38}{76.10} \times 100\% = \mathbf{+21.52\%}$
  - Tiny defects over GNA-PSC: $\Delta_{\text{rel}} = \frac{20.08}{72.40} \times 100\% = \mathbf{+27.73\%}$
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Explicitly state whether gains are absolute percentage points (pp) or relative percentage improvements (%), and define both formulas in Section V.B.

---

### R2.5 — Bibliography Verification Against Publisher Records
- **Manuscript Location:** Section References, `references.bib`.
- **Physical Evidence:**
  Every reference was audited against publisher DOI databases:
  1. `survey2024`: Key says 2024, but paper was published in **March 2020** (IEEE TIM, vol. 69, no. 3, pp. 626–644).
  2. `neu_benchmark2025`: Key says 2025, but paper by Song & Yan was published in **November 2013** (*Appl. Surf. Sci.*, vol. 285, pp. 858–864). Text claims "Zhang et al. 2025", which is completely false!
  3. `ispad2025`: Published Jan 2026 by P. J. Krassnig & D. P. Gruber (*J. Intell. Manuf.*). Text falsely claims "Li et al. 2025".
  4. `mixsegnet2024`: Published Aug 2024 in *IEEE Access* (vol. 12, pp. 111535–111545) by Y. Zhou et al. Table 2 falsely claims venue is *IEEE TIM*; text falsely claims "Mix et al.".
  5. `gnapsc2024`: Published Jul 2024 in *IEEE Sensors J.* (vol. 24, no. 13) by J. Zhang et al. Table 2 falsely claims venue is *IEEE Access*; text falsely claims "Wang et al.".
  6. `ef2net2024`: Published in *Proc. ICPRAI 2024* (conference) by F. Li et al. Table 2 falsely claims venue is *IEEE TIM*.
  7. `damfnet2025`: Published Jul 2024 in *Sensors* (vol. 24, no. 14, p. 4635) by D. Liu et al. Table 2 falsely claims venue is *IEEE Trans. Ind. Inform. 2025*; text falsely claims "Zhao et al.".
  8. `dmsunet2026`: Published Aug 2024 in *Meas. Sci. Technol.* (vol. 35, no. 10, p. 105404) by S. Liu, X. Miao, Y. Zhou. Table 2 falsely claims *IEEE TIM 2026*; text falsely claims "Chen et al. 2026".
  9. `tmcnet2025`: Published Nov 2023 in *Pattern Recognition* (vol. 143, p. 109787) by J. Dong et al. Key says 2025.
  10. `compositeloss2024`: Published Jan 2021 in *Med. Image Anal.* (vol. 67, p. 101851) by H. Kervadec et al. Key says 2024.
  11. `fewshot_steel2026`: Published Apr 2024 in *IEEE TIM* (vol. 73) by Z. Yao et al. Key says 2026; text falsely claims "Feng et al. 2026".
  12. `dilated_multiscale2024`: Landmark DeepLabv3+ paper published in **ECCV 2018** by L.-C. Chen et al. Key says 2024.
  13. `edge_manufacturing2025`: Landmark paper published in **Computer 2017** by M. Satyanarayanan. Key says 2025.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Total overhaul of bibliography metadata, citation keys, in-text author citations, and Table 2 publication venue columns.

---

### R2.6 — Novelty of MSFP, BAS, and BGFF Modules
- **Manuscript Locations:** Section I.C, Section II, Section IV.
- **Physical Evidence:**
  - *MSFP Block:* Code in `models.py` uses standard 2D convolutions (`Conv2d`), not depthwise separable convolutions. Parallel dilated convolutions are well-established primitives (ASPP, RFBNet). The architectural novelty is the multi-branch dilation structure ($r \in \{1, 2, 4\}$) integrated residually inside each encoder stage to preserve fine high-frequency crack signatures.
  - *BAS Stream:* Edge supervision using morphological gradients has precedents in medical and crack imaging (BASNet, Gated-SCNN). The novelty is early multi-scale extraction without an expensive auxiliary decoder.
  - *BGFF Gate:* Spatial attention gating has precedents in Attention U-Net. The novelty is the specific $(1 + \mathbf{G}) \odot \mathbf{F}$ residual modulation directly connecting boundary probabilities into the primary segmentation decoder.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Re-frame claims from claiming that dilated convolutions or edge losses are fundamentally novel to highlighting the specific architectural integration and spatial attention coupling.

---

### R2.7 — Ablation Studies Verification
- **Manuscript Locations:** Table 4 (Architectural Ablation), Table 5 (Loss Ablation).
- **Physical Evidence:**
  - In `models/`, the ONLY existing saved weights are:
    1. `best_UNet.pth`
    2. `best_UNetPlusPlus.pth`
    3. `best_MSBANet.pth`
  - There are NO saved weights or training logs for:
    - Baseline Backbone + MSFP alone
    - Baseline Backbone + MSFP + BAS alone
    - $\mathcal{L}_{\text{BCE}}$ only
    - $\mathcal{L}_{\text{BCE}} + \mathcal{L}_{\text{Dice}}$
    - $\mathcal{L}_{\text{BCE}} + \mathcal{L}_{\text{Dice}} + \mathcal{L}_{\text{Focal}}$
  - In Table 5, the "Boundary Prec (%)" for Full Composite Loss is reported as **97.57%**, which is identical to the overall segmentation Precision in Table 2!
- **Verdict:** **EVIDENCE UNAVAILABLE / NEW EXPERIMENT REQUIRED**. The intermediate rows of Tables 4 and 5 cannot be verified from disk. They must be explicitly disclosed as unverified historical exploratory runs, or new controlled experiments must be conducted.

---

### R2.8 — Statistical Variation and Error Margins
- **Manuscript Locations:** Table 2, Table 3.
- **Physical Evidence:**
  Inspection of `main.py`, `verify_metrics.py`, and `results/verified_benchmark_metrics.json` confirms that all reported metrics originate from a **single evaluation run using seed 42**.
  No repeated runs across independent random seeds were recorded, and no standard deviations or 95% confidence intervals are reported.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Disclose transparently that reported metrics represent single-seed evaluation and note multi-seed statistical confidence testing as recommended future evaluation protocol.

---

### R2.9 — Robustness Evaluation Protocol and Discrepancies
- **Manuscript Locations:** Section VI.A (Lines 414–418), Figure 4.
- **Physical Evidence:**
  1. *Parameter Discrepancy:*
     - Low contrast: Code uses linear scaling `(img - mean) * 0.45 + mean`. Manuscript claims $\gamma = 1.8$.
     - Sensor noise: Code uses `rng.normal(0, 18.0)`. Manuscript claims Gaussian noise with $\sigma = 25$.
     - Defocus blur: Code uses PIL `GaussianBlur(radius=2.5)`. Manuscript claims Gaussian blur $\sigma = 3.0$.
  2. *False Narrative Claim:*
     Line 417 states: "Under low contrast, MSBA-Net retains 39.67% mIoU, outperforming baseline models under challenging illumination."
     Physical inspection of `results/verified_benchmark_metrics.json` reveals:
     - **UNet:** Low-contrast mIoU = **44.51%**
     - **UNetPlusPlus:** Low-contrast mIoU = **50.26%**
     - **MSBANet:** Low-contrast mIoU = **39.67%**
     **MSBA-Net performed substantially WORSE than both U-Net (-4.84 pp) and U-Net++ (-10.59 pp) under low contrast!**
     Similarly, on motion blur:
     - UNet = 33.51%, UNet++ = 39.12%, MSBANet = 26.29% (MSBA-Net was lowest).
     Only on Normal (97.01%) and Tiny Defects (92.48%) did MSBA-Net outperform baselines.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Correct degradation parameter descriptions in text and retract the false claim that MSBA-Net outperformed baselines under low contrast and blur. Present the true empirical failure modes honestly as factory optical boundaries.

---

### R2.10 — Runtime, Model Size, and FLOPs Audit
- **Manuscript Location:** Section V.H (Line 408), Table 1.
- **Physical Evidence:**
  1. *Model Parameter Audit:*
     Executed PyTorch parameter calculation directly on implementations:
     - `MSBANet`: **8,650,786 parameters (8.65 Million)**
     - `UNet`: **7,762,465 parameters (7.76 Million)**
     - `UNetPlusPlus`: **9,159,105 parameters (9.16 Million)**
     The manuscript claims MSBA-Net has **9.38 Million** parameters. This is a discrepancy of 0.73M parameters.
  2. *Channel Configuration in Table 1:*
     Table 1 claims encoder channels are $C \in \{64, 128, 256, 512\}$. In reality, `models.py` uses `base_ch=32`, with channels $\{32, 64, 128, 256\}$, and bottleneck 512.
  3. *TensorRT Benchmarks:*
     The manuscript reports TensorRT 10.0 FP16 throughput of 88.5 FPS (11.3 ms). No TensorRT conversion script, serialized `.engine`/`.plan` file, or execution logs exist in the repository.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Correct parameter count to 8.65M, correct encoder channel progression in Table 1 to $\{32, 64, 128, 256\}$, and clarify that TensorRT latency is an estimated theoretical benchmark or remove the unsupported claim.

---

### R2.11 — Industrial Deployment Claims
- **Manuscript Locations:** Abstract, Section I, Section VI.B.
- **Physical Evidence:**
  The manuscript frequently asserts readiness for continuous steel rolling lines operating at velocities exceeding 15–20 m/s.
  However, no on-site physical factory testing, embedded Jetson integration, or line-scan hardware trials were conducted. All findings are derived from desktop GPU inference on procedurally synthesized images.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Tone down factory deployment claims, reframing them as simulated engineering feasibility analyses and operational boundary investigations.

---

### R2.12 — IEEE Template Artifacts
- **Manuscript Locations:** Lines 22, 33–34, 55.
- **Physical Evidence:**
  The manuscript contains unedited IEEE Access template boilerplates:
  - Line 22: `\doi{10.1109/ACCESS.2017.DOI}`
  - Lines 33–34: `\markboth {Author \headeretal: Preparation of Papers for IEEE TRANSACTIONS and JOURNALS}...`
  - Page footer on compiled PDF page 1: `VOLUME 4, 2016`
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Remove template placeholders and ensure strict compliance with clean IEEE Access manuscript guidelines.

---

### R2.13 — Figure and Table Consistency
- **Manuscript Locations:** Figures 1–4, Tables 1–5.
- **Physical Evidence:**
  1. *Fig 1:* Loss formula in graphic ($0.4, 0.6, 0.3, 0.5$) conflicts with manuscript L187 ($0.3, 0.3, 0.2, 0.2$) and `losses.py` ($1.0, 1.0, 0.5, 0.4$).
  2. *Fig 2:* Caption claims columns (c) and (d) are DMS-UNet and DAMF-Net, but image renders U-Net and U-Net++.
  3. *Fig 3:* Caption claims 100 epochs and mIoU trajectories, but image plots 12 epochs of validation loss.
  4. *Fig 4:* U-Net++ is labeled as "DMS-UNet [2026]".
  5. *Table 1:* Lists epochs=100 (actual 12), channels 64–512 (actual 32–256), parameters 9.38M (actual 8.65M).
  6. *Table 2:* Literature numbers mixed with local procedural numbers without disclaimers.
  7. *Table 3:* Rounding error on recall (99.41% vs 99.42%).
  8. *Table 4 & 5:* Unverified intermediate ablation rows.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Synchronize all figures, captions, tables, and narrative with the physical code and data.

---

### R2.14 — Complete Manuscript Proofreading
- **Manuscript Location:** Entire manuscript.
- **Physical Evidence:**
  Identified pervasive cross-document inconsistencies among narrative claims, mathematical formulas, table values, figure captions, and bibliography metadata.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Full proofreading and harmonization pass required across all sections.
