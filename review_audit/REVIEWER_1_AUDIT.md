# MSBA-Net: Reviewer #1 Individual Verification Audit
**Document ID:** `review_audit/REVIEWER_1_AUDIT.md`  
**Audit Date:** October 13, 2026  
**Auditor:** Antigravity Autonomous Research Audit Engine  
**Paper Title:** *MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation*  

---

## Summary of Reviewer #1 Verification

| Comment ID | Topic | Manuscript Location | Verification Status | Primary Finding / Required Action |
| :--- | :--- | :--- | :--- | :--- |
| **R1.1** | Grammar and Proofreading | Manuscript-wide | **VERIFIED — CORRECTION REQUIRED** | Broken LaTeX tag `item {Optical...}` at L64, 4 misattributed author names in Sec II, awkward/colloquial phrasing in Sec I, V, VI, VII. |
| **R1.2** | Abstract Repetition | Abstract (L38–L40) | **VERIFIED — CORRECTION REQUIRED** | Repetitive description of BAS and BGFF mechanisms present in earlier draft; condensation required while clearly distinguishing BAS supervision from BGFF gating. |
| **R1.3** | Defect Terminology | Abstract, Sec I, III, V | **VERIFIED — CORRECTION REQUIRED** | Inconsistent mix of "micro-fabric aberration", "tiny micro-defects", "micro-cracks". Standardize to "micro-scale defects" (<1% area) and "hairline crazing cracks". |
| **R1.4** | Mathematical Notation | Sec III, IV (Eq 1–22) | **VERIFIED — CORRECTION REQUIRED** | $\mathbf{K}_3$ used before definition; convolution $*_{k\times k}^r$ claims depthwise separable but code uses standard Conv2d; symbol collision between loss weight $\alpha$ and Focal factor $\alpha_t$. |
| **R1.5** | Equation (8) Receptive Field | Sec IV.A, Eq (8) | **VERIFIED — CORRECTION REQUIRED** | Eq (8) computes kernel dilated footprint span ($R_k = k + (k-1)(r-1)$), not cumulative network receptive field. Re-derive and contextualize mathematically. |
| **R1.6** | Structuring Element $\mathbf{K}_3$ | Sec III.B, Eq (1) | **VERIFIED — CORRECTION REQUIRED** | Paper claims $3 \times 3$ square yielding 2-px ribbon. Code in `dataset.py` uses `ndimage` default (cross) with 2 dilations + 1 erosion (3-px ribbon). Align text and document resolution justification. |
| **R1.7** | Random Seed Control | Sec V.A, `main.py` | **VERIFIED — CORRECTION REQUIRED** | PyTorch and NumPy set to seed 42 in `main.py`, but Python `random` unseeded, cuDNN deterministic flag unset. Disclose exact reproducibility controls truthfully. |
| **R1.8** | Table 2 DMS-UNet mIoU | Table 2, Sec II, Sec V | **VERIFIED — CORRECTION REQUIRED** | DMS-UNet (94.20%) was published in *Meas. Sci. Technol.* (Aug 2024) by S. Liu et al., NOT *IEEE TIM* (2026) by Chen et al. Result is cited, not reproduced. |
| **R1.9** | Table 3 Decimal Formatting | Table 3, Table 4 | **VERIFIED — CORRECTION REQUIRED** | Table 3 Overall Mean Recall has rounding error (reported 99.41%, exact arithmetic mean is 99.42%). Table 4 column $\text{mIoU}_{\text{tiny}}$ lacks `(\%)` unit. |
| **R1.10** | Figure 2 Readability | Fig 2, Caption (L280) | **VERIFIED — CORRECTION REQUIRED** | Caption claims columns (c) and (d) are DMS-UNet and DAMF-Net, but image actually depicts U-Net and U-Net++. Correct caption and column headers. |
| **R1.11** | Figure 3 Training/Val Curves | Fig 3, Caption (L396) | **VERIFIED — CORRECTION REQUIRED** | Caption claims "across 100 epochs" and "mIoU trajectories", but plot shows only validation loss across 12 epochs. Harmonize caption and display curves. |
| **R1.12** | Conclusion Simplification | Sec VII (L424) | **VERIFIED — CORRECTION REQUIRED** | Section repeats numerical metrics already presented in Results; awkward phrasing ("forfeiture of spatial characteristics"). Rewrite with technical focus. |
| **R1.13** | Future Work Grounding | Sec VII (L426) | **VERIFIED — CORRECTION REQUIRED** | Future work should directly address verified empirical limitations: synthetic-to-real domain transfer, noise breakdown (2.33% mIoU), and edge hardware constraints. |
| **R1.14** | IEEE Access Formatting | Preamble, Headers | **VERIFIED — CORRECTION REQUIRED** | Placeholder DOI (`10.1109/ACCESS.2017.DOI`) and generic template header `Author \headeretal: Preparation of Papers...` must be cleaned. |

---

## Detailed Item-by-Item Verification

### R1.1 — Grammar, Proofreading, and Technical Phrasing
- **Manuscript Locations:** Lines 62, 63, 64, 79, 96, 98, 100, 105, 317, 412, 424.
- **Physical Evidence:**
  1. *Line 64 Syntax Error:* `item {Optical Noise Resilience Issues:}` completely misses the leading `\` and `\textbf{}` command. This causes an unformatted bullet in LaTeX compilation.
  2. *Line 62 Unidiomatic Phrasing:* "Micro-fabric elements such as craze cracks... occupy less than 0.5\%-1.0\% of the overall visual taken by the camera."
  3. *Line 63 Colloquial Phrasing:* "...therefore leading to the result that all pixels are overpunished in regard to trenches and cracks."
  4. *Line 79 Tense Inconsistency:* "We have developed a spatial attention gating network..." mixed with present tense "We formulate...", "We construct...".
  5. *Literature Attribution Errors:*
     - L96: "Mix et al. publish their work [4]" $\rightarrow$ MixSegNet [4] was authored by Y. Zhou, R. Ali, N. Mokhtar, S. W. Harun, and M. Iwahashi.
     - L96: "Wang et al. [5]" $\rightarrow$ GNA-PSC [5] was authored by J. Zhang, F. Huang, Y. Lv, Z. Zeng, and Y. Gui.
     - L98: "Zhao et al. created DAMF-Net" $\rightarrow$ DAMF-Net [7] was authored by D. Liu, Z. Chen, C. Zhang, et al.
     - L98: "Chen et al. [8] designed DMS-UNet" $\rightarrow$ DMS-UNet [8] was authored by S. Liu, X. Miao, and Y. Zhou.
     - L100: "Zhang et al. in 2024" $\rightarrow$ PotholeBAF-Net [12] was authored by M. M. Alghamdi and Y. Qasim.
  6. *Line 317 Defect Naming:* "hard-to-find surface areas" used for low-contrast Patches.
  7. *Line 412 Punctuation:* Run-on sentence with space before period: `...under unfavorable shop conditions.\cite{neu_benchmark2025, ispad2025}.`.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Complete copyediting pass required to correct syntax errors, fix author attributions, and raise technical register.

---

### R1.2 — Abstract Repetition
- **Manuscript Location:** Abstract (Lines 38–40).
- **Physical Evidence:**
  In earlier compilation artifacts (`scratch/paper_text.txt` lines 11–27), the abstract literally contained two consecutive duplicate blocks describing the Boundary-Aware Stream (BAS) and Boundary-Guided Feature Fusion (BGFF). In `ieee_access_msba_net.tex`, the text was partially consolidated, but still contains overlapping phrasing where the distinct functional role of BAS (supervisory edge contour generator) and BGFF (decoder spatial attention gate) is repeated in adjacent sentences.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Rewrite abstract into a single cohesive, high-impact paragraph of $\sim$180–200 words clearly separating BAS and BGFF roles.

---

### R1.3 — Defect Terminology Standardization
- **Manuscript Locations:** Abstract, Section I, Section III, Section V.
- **Physical Evidence:**
  The manuscript alternates arbitrarily among "micro-fabric aberration", "micro-scale flaws", "tiny micro-scale flaws", "micro-cracks", "tiny defects", and "small defects".
  In metallurgy and IEEE instrumentation standards:
  - "Micro-fabric" refers to crystal grain microstructure (metallography), not macroscopic surface defect flaws.
  - "Small defects" / "micro-scale defects" must be mathematically anchored to area occupancy: $|\mathcal{S}_{\text{defect}}| / (H \times W) < 0.01$ (occupying $<1\%$ of image area).
  - Crack flaws must be termed "hairline crazing cracks" or "fine dendritic fissures".
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Replace all unscientific terms (especially "micro-fabric aberration") with standardized industrial terminology.

---

### R1.4 — Mathematical Notation and Symbol Audit
- **Manuscript Locations:** Section III.B (Eq 1–3), Section IV.A (Eq 4–9), Section IV.C (Eq 15–17), Section IV.D (Eq 18–22).
- **Physical Evidence:**
  1. *Eq (1):* Structuring element $\mathbf{K}_3$ is introduced in Eq (1) without prior definition; its definition only appears at line 123.
  2. *Eq (4)–(7):* Notation $*_{k\times k}^r$ is declared as "depthwise separable convolution", but in `models.py` lines 132–151, the implementation uses standard `nn.Conv2d`. The notation must match the true architecture.
  3. *Eq (16):* $\tilde{\mathbf{F}}_{\text{seg}} = \text{ConvBlock}(\mathbf{F}_{\text{seg}, 1} \odot (\mathbf{1} + \mathbf{G}_{\text{bound}}))$. The spatial gate $\mathbf{G}_{\text{bound}} \in [0, 1]^{1 \times H \times W}$ is broadcast across channels $C$ of $\mathbf{F}_{\text{seg}, 1} \in \mathbb{R}^{C \times H \times W}$. In formal mathematics, channel broadcasting should be explicitly denoted.
  4. *Eq (18) vs Eq (21) Symbol Collision:* Eq (18) defines composite loss with weight $\alpha = 0.3$. Eq (21) defines Focal loss with class balance factor $\alpha_t = 0.25$ and focusing parameter $\gamma = 2.0$, colliding with composite weight $\gamma = 0.2$.
  5. *Loss Weights Discrepancy:*
     - Manuscript L187: $\alpha = 0.3, \beta = 0.3, \gamma = 0.2, \lambda = 0.2$.
     - Code `losses.py` L41: $\lambda_{\text{dice}} = 1.0, \lambda_{\text{focal}} = 0.5, \lambda_{\text{boundary}} = 0.4$ (with implicit BCE weight 1.0).
     - Figure 1 L114: $0.4\mathcal{L}_{\text{BCE}} + 0.6\mathcal{L}_{\text{Dice}} + 0.3\mathcal{L}_{\text{Focal}} + 0.5\mathcal{L}_{\text{Boundary}}$.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Reconcile loss weighting notations, eliminate symbol collisions, and define all mathematical terms before first use.

---

### R1.5 — Equation (8) and Receptive Field Derivation
- **Manuscript Location:** Section IV.A, Equation (8).
- **Physical Evidence:**
  Equation (8) states:
  $$R_k = k + (k - 1)(r - 1)$$
  For $k=3$ and $r \in \{1, 2, 4\}$:
  - $r = 1 \implies 3 + 2(0) = 3$
  - $r = 2 \implies 3 + 2(1) = 5$
  - $r = 4 \implies 3 + 2(3) = 9$
  *Mathematical Verification:* This formula computes the *dilated kernel footprint span* $k_{\text{eff}} = (k - 1)r + 1$ of a single layer.
  *Discrepancy:* In convolution arithmetic (e.g., Dumoulin & Visin, 2016), the *cumulative receptive field* of a convolutional network at stage $l$ with cumulative stride $S_{l-1}$ and prior receptive field $RF_{in}$ is:
  $$RF_{out} = RF_{in} + (k_{\text{eff}} - 1) \times S_{l-1}$$
  At Stage 1 ($S=1$), preceding double $3\times 3$ ConvBlock gives $RF_{in} = 5$. With $r=4$ ($k_{\text{eff}}=9$), the true receptive field reaches $5 + (9 - 1) = 13$, not 9. At Stage 4 ($S=8$), the receptive field spans over 100 pixels.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Clarify in the narrative that Equation (8) provides the layer-wise dilated kernel footprint $k_{\text{eff}}$, and provide the exact cumulative receptive field expansion formula.

---

### R1.6 — Boundary-Target Structuring Element Justification
- **Manuscript Location:** Section III.B, Equation (1).
- **Physical Evidence:**
  The manuscript states that a $3 \times 3$ square structuring element $\mathbf{K}_3$ produces a crisp 2-pixel wide boundary ribbon.
  In `dataset.py` lines 160–162:
  ```python
  dilated = ndimage.binary_dilation(mask, iterations=2)
  eroded = ndimage.binary_erosion(mask, iterations=1)
  boundary = (dilated.astype(np.float32) - eroded.astype(np.float32))
  ```
  `scipy.ndimage.binary_dilation` defaults to connectivity 1 (cross structuring element), and 2 dilations + 1 erosion produce a 3-pixel wide gradient ribbon.
  *Scientific Justification:* On $256 \times 256$ defect images where hairline cracks are 1–3 pixels wide, a 2-to-3 pixel boundary target provides the ideal supervisory ribbon. A single-pixel ribbon has zero tolerance for sub-pixel boundary ambiguity and creates extreme class imbalance. A ribbon larger than 5 pixels would fully subsume micro-defects (<1% area), destroying the topological distinction between defect core and boundary.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Reconcile code and text description of the morphological structuring element and explicitly document the resolution-based scientific justification.

---

### R1.7 — Random Seed Documentation
- **Manuscript Location:** Section V.A.
- **Physical Evidence:**
  In `main.py` lines 15–20:
  ```python
  def set_seed(seed=42):
      np.random.seed(seed)
      torch.manual_seed(seed)
      if torch.cuda.is_available():
          torch.cuda.manual_seed_all(seed)
  ```
  In `dataset.py` line 34: `seed=42` (`seed` for train, `seed + 1000` for val).
  In `verify_metrics.py` line 66: `seed=42`.
  In `make_fig2_panoramic.py` line 26: `seed=2026`.
  *Missing Controls:*
  - Python's standard library `random` module was NOT seeded.
  - PyTorch cuDNN determinism was NOT configured (`torch.backends.cudnn.deterministic = True` and `torch.backends.cudnn.benchmark = False` were omitted).
  - No physical NEU images were split; procedural generation was governed by `np.random.RandomState`.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Disclose the exact seeds used (42 for training/val, 2026 for qualitative visualization) and explicitly report the absence of cuDNN deterministic flags rather than asserting full deterministic reproduction.

---

### R1.8 — Table 2 and DMS-UNet mIoU Provenance
- **Manuscript Locations:** Table 2, Abstract, Section II.A, Section V.B.
- **Physical Evidence:**
  Table 2 lists DMS-UNet with 94.20% mIoU, 97.02% Dice, 95.12% Precision, 99.04% Recall, 88.40% Tiny mIoU, citing venue as "IEEE Trans. Instrum. Meas. (2026)".
  Inspection of `references.bib` reveals:
  ```bibtex
  @article{dmsunet2026,
    author={Liu, S. and Miao, X. and Zhou, Y.},
    journal={Measurement Science and Technology},
    title={{DMS-UNet}: Dual-branch edge-aware network with hybrid attention for steel defect segmentation},
    year={2024},
    volume={35},
    number={10},
    pages={105404},
    month={Aug.},
    doi={10.1088/1361-6501/ad5c55}
  }
  ```
  *Discrepancies Found:*
  1. Venue in Table 2 is incorrect (published in *Measurement Science and Technology*, not *IEEE TIM*).
  2. Publication year is 2024, not 2026.
  3. Authors in Section II.A L98 ("Chen et al.") are incorrect (actual authors: S. Liu, X. Miao, Y. Zhou).
  4. In this repository, DMS-UNet was NOT trained or evaluated. The 94.20% value is cited from the original paper.
  5. In Figure 2 and Figure 4, U-Net++ (which achieved 94.13% mIoU) was substituted and relabeled as DMS-UNet.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Correct publication venue, year, and author names. Explicitly label Table 2 entries as literature-cited vs locally evaluated.

---

### R1.9 — Table 3 Decimal Precision and Formatting
- **Manuscript Locations:** Table 3, Table 4.
- **Physical Evidence:**
  Table 3 lists class-wise metrics across 6 defect classes:
  - Crazing: Rec = 99.54%
  - Inclusion: Rec = 99.22%
  - Patches: Rec = 99.43%
  - Pitted Surface: Rec = 99.57%
  - Rolled-in Scale: Rec = 99.60%
  - Scratches: Rec = 99.14%
  *Arithmetic Verification:*
  $$\text{Mean Recall} = \frac{99.54 + 99.22 + 99.43 + 99.57 + 99.60 + 99.14}{6} = \frac{596.50}{6} = 99.4167\%$$
  Rounded to 2 decimal places, this is **99.42%**, but Table 3 reports **99.41%**.
  *Table 4 Formatting:* Column header $\mathbf{mIoU}_{\mathbf{tiny}}$ lacks unit `(\%)`, whereas other columns have `(\%)`.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Fix the rounding discrepancy (99.42%) and standardize table column headers.

---

### R1.10 — Figure 2 Visual Readability and Provenance
- **Manuscript Location:** Figure 2, Caption (Line 280).
- **Physical Evidence:**
  Caption in `ieee_access_msba_net.tex` line 280 states:
  "Columns display: (a) Input raw patch, (b) Ground truth annotation, (c) DMS-UNet (2026 baseline), (d) DAMF-Net (2025 baseline), and (e) Proposed MSBA-Net."
  However, inspection of `make_large_clear_figures.py` and `make_fig2_panoramic.py` confirms that the image actually renders:
  - Column (c): `best_UNet.pth` (U-Net Baseline)
  - Column (d): `best_UNetPlusPlus.pth` (U-Net++)
  - Column (e): `best_MSBANet.pth` (MSBA-Net)
  Neither DMS-UNet nor DAMF-Net models exist in the repository.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Update Figure 2 caption and column titles to truthfully state that columns display U-Net and U-Net++, eliminating false attribution to DMS-UNet and DAMF-Net.

---

### R1.11 — Figure 3 Convergence Curves
- **Manuscript Location:** Figure 3, Caption (Line 396).
- **Physical Evidence:**
  Caption states: "Training and validation loss and mIoU convergence trajectories across 100 epochs, demonstrating stable and monotonic optimization."
  Actual code (`main.py` lines 260–285, `generate_professional_figures.py` lines 238–281):
  1. Models were trained for **12 epochs**, not 100 epochs.
  2. Figure 3 plots ONLY validation loss. No training loss curve is displayed.
  3. No mIoU convergence trajectory is displayed.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Reconcile Figure 3 caption with actual plotted curves (validation loss across 12 epochs) and eliminate unsupported claims of 100-epoch training and mIoU curves.

---

### R1.12 — Conclusion Streamlining
- **Manuscript Location:** Section VII (Lines 424–425).
- **Physical Evidence:**
  The conclusion merely re-lists numbers from Table 2: "(mIoU = 97.01\%, Dice = 98.48\%, and micro-defects = 92.48\%)" and contains awkward phrasing: "the model acts to prevent the forfeiture of spatial characteristics from micro-cracks" and "Intensive experimentation in bad conditions allowed establishing operational limits in reality."
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Rewrite conclusion to focus on architectural contributions (MSFP multi-dilation preserving micro-features, BAS-BGFF spatial gating) and honest discussion of operational boundaries.

---

### R1.13 — Future Work Grounding
- **Manuscript Location:** Section VII (Line 426).
- **Physical Evidence:**
  The current future work suggests spatio-temporal attention, masked autoencoder pre-training, and Jetson AGX Orin quantization.
  While valid, it fails to connect to the actual severe empirical failure discovered in Section VI: MSBA-Net collapses to **2.33% mIoU under sensor noise** and drops to **39.67% under low contrast** (performing worse than U-Net at 44.51% and U-Net++ at 50.26%).
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Re-frame future work to explicitly target the demonstrated noise-sensitivity limitation, synthetic-to-real transfer, and real plant deployment.

---

### R1.14 — IEEE Formatting and Template Cleanliness
- **Manuscript Locations:** Lines 22, 33–34, 55.
- **Physical Evidence:**
  1. Line 22: `\doi{10.1109/ACCESS.2017.DOI}` is a template placeholder.
  2. Lines 33–34: `\markboth {Author \headeretal: Preparation of Papers for IEEE TRANSACTIONS and JOURNALS}...` is unedited template placeholder text.
  3. Line 46: `\titlepgskip=-15pt` is an ad-hoc layout hack.
  4. Footer contains template artifact `VOLUME 4, 2016`.
- **Verdict:** **VERIFIED — CORRECTION REQUIRED**. Clean all template artifacts in accordance with official IEEE Access submission guidelines.
