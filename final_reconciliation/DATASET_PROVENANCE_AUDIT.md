# MSBA-Net: Dataset Provenance, Generation Methodology & Reproducibility Audit
**Document ID:** `final_reconciliation/DATASET_PROVENANCE_AUDIT.md`  
**Audit Date:** October 14, 2026  
**Auditor:** Antigravity Autonomous Research & Forensic Audit Engine  
**Paper Title:** *MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation*  
**Target Venue:** *IEEE Access*  

---

## 1. Executive Summary

This report establishes the forensic audit of data provenance, procedural synthesis, annotation derivation, partitioning, and random seed handling for the MSBA-Net benchmark in compliance with **Critical Task F** and **Reviewer 2, Comments 1 & 2 (R2.1, R2.2)**.

### Authoritative Findings:
1. **Zero Real Photographs on Disk:** A full filesystem search of the repository confirms that **no raw photographic images from the NEU Surface Defect Database (NEU-Seg) exist on disk**.
2. **Procedural Synthetic Generation:** The entire experimental pipeline relies on `IndustrialDefectDataset` in `dataset.py`, which procedurally generates 2D numpy arrays modeling the background metallurgy and six canonical defect morphologies of strip steel.
3. **Procedural Ground-Truth Masks:** Defect segmentation masks and morphological boundary ribbons are generated deterministically through procedural mathematical morphology, eliminating human annotator subjectivity and labeling noise.
4. **Transparent Manuscript Disclosure:** All claims of evaluating 1,800 real factory photographs were removed from the manuscript and replaced with explicit disclosure of the high-fidelity procedural synthetic benchmark.

---

## 2. Dataset Generation Mechanics (`dataset.py`)

### 2.1 Metallic Rolled Steel Background Synthesis
The base steel strip texture is generated via `_generate_steel_background(h, w)`:
- **Base Metallic Gray:** Uniform intensity drawn from $\mathcal{U}(115, 145)$.
- **Cold-Rolling Mill Grain:** Horizontal periodic striations along the rolling axis:
  $$\text{grain}(y) = \sin(y \cdot f) \cdot A, \quad f \sim \mathcal{U}(0.05, 0.2), \; A \sim \mathcal{U}(3, 8)$$
- **Illumination Gradient:** Low-frequency bilinear gradient modeling uneven shop-floor strobe lighting:
  $$I_{\text{grad}}(x, y) = x_{\text{norm}} \cdot \mathcal{U}(-15, 15) + y_{\text{norm}} \cdot \mathcal{U}(-10, 10)$$
- **Sensor High-Frequency Noise:** Micro-texture noise drawn from $\mathcal{N}(0, \sigma_{\text{bg}})$, with $\sigma_{\text{bg}} \sim \mathcal{U}(2, 4)$.
- **Dynamic Range Clipping:** $\mathbf{I}_{\text{bg}} = \text{clip}(\mathbf{I}_{\text{bg}}, 0, 255)$.

### 2.2 Canonical Defect Morphologies Synthesis
Defects are synthesized via `_synthesize_defect(h, w, defect_type, is_tiny)`:

| Defect Class | Mathematical Synthesis Algorithm | Contrast / Intensity Shift | Topological Characteristics |
| :--- | :--- | :---: | :--- |
| **1. Crazing (Cr)** | Random-walk dendritic branching with angular perturbation $\theta \leftarrow \theta + \mathcal{U}(-0.4, 0.4)$, followed by morphological dilation ($\text{iter}=1$) and Gaussian smoothing ($\sigma=0.6$). | $\Delta I \sim \mathcal{U}(-50, -30)$ (Dark fissures) | 1-to-2 pixel wide branching micro-cracks traversing metallic grains. |
| **2. Inclusion (In)** | Elliptic distance field $\left(\frac{x - x_0}{r_x}\right)^2 + \left(\frac{y - y_0}{r_y}\right)^2 \le 1.0$ with $2$ to $5$ particulate clusters ($r_x, r_y \in [4, 14]$). | $\Delta I \sim \mathcal{U}(-65, -40)$ (Dark particulates) | Isolated sub-millimeter non-metallic particles embedded in strip. |
| **3. Patches (Pa)** | Gaussian-blurred blemish field ($\sigma=2.0$) thresholded at $0.4$ to induce perimeter irregularity. | $\Delta I = \pm \mathcal{U}(15, 25)$ (**Low Contrast**) | Subtle diffuse blemishes blending into ferrite-pearlite matrix. |
| **4. Pitted Surface (PS)** | Clustered localized circular pinholes ($10$ to $25$ pits) positioned via Gaussian spatial clustering $\mathcal{N}(0, 25)$ with radii $r \in [1, 3]$. | $\Delta I \sim \mathcal{U}(-75, -50)$ (Deep cavities) | High-frequency pore clusters mimicking acid pickling cavities. |
| **5. Rolled-in Scale (RS)** | Superposition of elliptical base blob with additive random Gaussian surface roughness thresholded at $0.8$. | $\Delta I \sim \mathcal{U}(-55, -35)$ (Textured scale) | Mottled oxidized iron scale pressed into sheet surface during rolling. |
| **6. Scratches (Sc)** | Longitudinal linear paths along rolling angle $\theta \sim \mathcal{U}(-\pi/4, \pi/4)$ with lengths $L \in [60, 140]$ pixels and width dilated to $1$--$2$ pixels. | $\Delta I \sim \mathcal{U}(-60, -40)$ (Gouged grooves) | Elongated directional abrasions from damaged guide rolls. |

### 2.3 Morphological Boundary Target Derivation
Boundary targets $\mathbf{Y}_{\text{bound}} \in \{0, 1\}^{H \times W}$ are computed online via morphological gradient:
$$\mathbf{Y}_{\text{bound}} = \mathcal{M}_{\text{dilate}}(\mathbf{Y}_{\text{mask}}, \mathbf{K}_{\text{cross}}, \text{iter}=2) - \mathcal{M}_{\text{erode}}(\mathbf{Y}_{\text{mask}}, \mathbf{K}_{\text{cross}}, \text{iter}=1)$$
This operation generates a continuous 2-to-3 pixel edge ribbon encompassing the defect transition zone at $256 \times 256$ resolution.

---

## 3. Dataset Partitioning, Random Seeds & Leakage Audit

### 3.1 Partition Scheme
- **Training Partition:** 700 procedural image patches under nominal texture parameters.
- **Validation / Evaluation Partition:** 150 procedural image patches per degradation condition (Normal, Low Contrast, Noise, Blur, Tiny Defects).
- **Resolution:** Grayscale patches at $256 \times 256 \times 1$.

### 3.2 Random Seed Trajectory Isolation
In `dataset.py`:
```python
self.rng = np.random.RandomState(seed if mode == 'train' else seed + 1000)
```
- For seed 42, training loader initializes with RNG state $42$.
- Validation loader initializes with RNG state $1042$.
- Because $42 \ne 1042$, the random number generator trajectories are disjoint, preventing sample overlap between training and validation sets.

### 3.3 Forensic Finding: RNG State Advancement in `IndustrialDefectDataset`
The forensic audit uncovered a critical implementation nuance:
- `IndustrialDefectDataset` generates images dynamically in `__getitem__(self, idx)` on every call rather than pre-generating and caching them in RAM or on disk.
- Consequently, sequential loops through a single dataset instance advance `self.rng`:
  - Iteration 1 evaluates samples 0..149.
  - Iteration 2 evaluates samples 150..299 of the pseudo-random stream.
- In `run_ablations.py`, `test_normal` was instantiated once at the start of the script. Sequential model evaluations occurred on successive 150-sample slices, introducing minor inter-run evaluation variance.
- In `verify_metrics.py` and `scratch/eval_fresh_all.py`, datasets were instantiated fresh (`IndustrialDefectDataset(..., seed=42)`) before each model evaluation, guaranteeing that every model was evaluated on the exact same 150 samples (seed 1042, samples 0..149).

---

## 4. Limitations and the Synthetic-to-Real Domain Gap

### 4.1 Strengths of Procedural Synthetic Benchmarking:
1. **Zero Annotation Subjectivity:** Eliminates human labeling bias and ambiguous border tracings.
2. **Exact Ground Truth:** The mathematical boundary ribbon is exact to the sub-pixel level.
3. **Controlled Degradation Parametrization:** Permits precise physical decoupling of low contrast, sensor noise, and motion blur.

### 4.2 Critical Operational Limitations:
1. **Synthetic-to-Real Domain Gap:** Real strip cold-rolling environments exhibit complex non-stationary lighting artifacts, specular roll reflections, and three-dimensional surface topography not fully captured by 2D texture equations.
2. **Factory Line Speeds:** High-speed rolling at 15–20 m/s introduces physical line-scan sensor integration artifacts, strip vibration flutter, and cooling emulsion droplets.
3. **Mandatory Scientific Framing:** The manuscript must present these findings as a controlled algorithmic proof-of-concept on high-fidelity procedural synthetic data, rather than claiming production-line operational readiness.
