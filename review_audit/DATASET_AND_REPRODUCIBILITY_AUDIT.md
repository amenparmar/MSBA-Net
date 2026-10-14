# MSBA-Net: Dataset and Reproducibility Forensic Audit
**Document ID:** `review_audit/DATASET_AND_REPRODUCIBILITY_AUDIT.md`  
**Audit Date:** October 13, 2026  
**Auditor:** Antigravity Autonomous Research Audit Engine  
**Paper Title:** *MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation*  

---

## 1. Executive Summary: Physical Dataset Truth vs Manuscript Representation

A foundational finding of this audit is a severe divergence between the experimental narrative presented in the manuscript and the physical implementation in the repository:

| Dataset Dimension | Narrative Claim in Manuscript (`ieee_access_msba_net.tex`) | Physical Reality in Workspace (`dataset.py`, `main.py`) | Scientific Integrity Assessment |
| :--- | :--- | :--- | :--- |
| **Dataset Source** | Benchmark NEU Surface Defect Database (1,800 real industrial grayscale photographs) | 100% Procedural Synthetic Dataset generated on the fly via NumPy and SciPy | **CRITICAL DISCREPANCY:** Zero physical image files or annotation files from the NEU benchmark exist on disk. |
| **Image Resolution** | $200 \times 200$ original resized to $256 \times 256$ pixels | Directly synthesized at $256 \times 256$ pixels in NumPy array memory | Resizing pipeline is non-existent because generation natively outputs $256 \times 256$. |
| **Partitioning Counts**| 70% Train (1,260), 15% Val (270), 15% Test (270) | `num_samples=700` (Train), `num_samples=150` (Val/Test) | Train count is 700 (claimed 1,260); test count is 150 (claimed 270). |
| **Ground Truth Masks**| Standard human-annotated defect masks from NEU-Seg benchmark | Procedurally generated binary masks computed via random walks, ellipses, and thresholded noise | Masks reflect mathematical equations rather than physical optical defect boundaries. |
| **Defect Classes** | Six canonical classes (Cr, In, Pa, PS, RS, Sc) | Six procedurally modeled classes mimicking canonical defect morphologies | Morphologies mimic the topological traits of NEU classes, but are synthetic. |

> [!IMPORTANT]
> **Core Audit Finding:** MSBA-Net was **never trained on real photographs from the NEU Surface Defect Database**. It was trained on an algorithmic procedural simulator (`IndustrialDefectDataset`). Presenting results as if they were derived from the standard NEU benchmark constitutes a major scientific discrepancy that must be corrected by transparently disclosing the procedural synthetic benchmark.

---

## 2. Forensic Code Analysis of `IndustrialDefectDataset` (`dataset.py`)

The file `dataset.py` contains 218 lines of highly structured procedural image generation code. The pipeline operates in four distinct stages:

### 2.1 Metallic Rolling Surface Synthesis (`_generate_steel_background`)
The background metallic matrix is synthesized using a combination of base intensity, directional grain, lighting gradients, and micro-texture:
1. **Base Intensity:** Uniformly sampled between $115$ and $145$ grayscale value:
   $$\mathbf{I}_{\text{base}} = \text{Uniform}(115, 145)$$
2. **Horizontal Rolling Grain:** Simulates continuous strip roll texture with frequency $\omega \in [0.05, 0.2]$:
   $$\mathbf{G}(y) = \sin(y \cdot \omega) \times \text{Uniform}(3, 8)$$
3. **Shop-Floor Illumination Gradient:** Simulates non-uniform lighting across the line-scan field of view:
   $$\mathbf{L}(x, y) = x \cdot \text{Uniform}(-15, 15) + y \cdot \text{Uniform}(-10, 10)$$
4. **High-Frequency Micro-Texture Noise:** Normal Gaussian noise with $\sigma \in [2, 4]$:
   $$\mathbf{N}_{\text{texture}} \sim \mathcal{N}(0, \sigma^2)$$
   $$\mathbf{I}_{\text{bg}} = \text{clip}\left(\mathbf{I}_{\text{base}} + \mathbf{G} + \mathbf{L} + \mathbf{N}_{\text{texture}}, 0, 255\right)$$

### 2.2 Defect Pattern Synthesis (`_synthesize_defect`)
Defect masks $\mathbf{Y}_{\text{mask}}$ and intensity modulation layers $\mathbf{I}_{\text{defect}}$ are synthesized per class:
- **Crazing (Cr):** 3 to 6 branching dendritic random walks of length 30–80 pixels, dilated by 1 iteration to produce 1–2 pixel wide dark cracks ($\Delta I \in [-50, -30]$) followed by a Gaussian blur ($\sigma = 0.6$).
- **Inclusion (In):** 2 to 5 small elliptic particles ($r_x \in [4, 10], r_y \in [5, 14]$) with dark contrast ($\Delta I \in [-65, -40]$).
- **Patches (Pa):** Diffuse elliptic blemishes ($r \in [15, 35]$) blurred with Gaussian filter ($\sigma = 2.0$) with very low contrast ($\Delta I = \pm [15, 25]$), simulating oxidized sheen.
- **Pitted Surface (PS):** Clusters of 10 to 25 pinhole craters ($r \in [1, 3]$) with dark cores ($\Delta I \in [-75, -50]$).
- **Rolled-in Scale (RS):** Mottled irregular scale indentations ($r \in [12, 35]$) thresholded with normal noise ($\Delta I \in [-55, -35]$).
- **Scratches (Sc):** Directional linear gouges oriented at $\theta \in [-\pi/4, \pi/4]$ of length 60–140 pixels dilated by 1 iteration ($\Delta I \in [-60, -40]$).

### 2.3 Morphological Boundary Target Computation (`_compute_boundary`)
Lines 158–163 compute the boundary ribbon:
```python
def _compute_boundary(self, mask):
    dilated = ndimage.binary_dilation(mask, iterations=2)
    eroded = ndimage.binary_erosion(mask, iterations=1)
    boundary = (dilated.astype(np.float32) - eroded.astype(np.float32))
    return np.clip(boundary, 0, 1.0)
```
- By default in SciPy, `ndimage.binary_dilation` uses `structure=None` (connectivity 1, corresponding to a 4-connected cross).
- Applying 2 dilation iterations followed by 1 erosion iteration generates a 3-pixel wide asymmetrical boundary ribbon around the defect perimeter.

### 2.4 Industrial Degradation Stress-Testing (`_apply_degradation`)
Lines 165–185 implement four degradation transforms:
1. **Low Contrast:** $\mathbf{I}' = (\mathbf{I} - \mu) \times 0.45 + \mu$ (linear attenuation by factor $0.45$).
2. **Sensor Noise:** $\mathbf{I}' = \mathbf{I} + \mathcal{N}(0, 18.0^2)$.
3. **Motion Blur:** PIL Gaussian blur with radius $r = 2.5$.
4. **Tiny Defects:** Restricts synthesized defect dimensions ($r \in [2, 5]$, length $15–35$), ensuring $|\mathcal{S}| < 0.01 \times (H \times W)$.

---

## 3. Dataset Partitioning, Random Seeds, and Data Leakage Audit

### 3.1 Sample Sizes and Split
In `main.py` lines 243–244:
- `train_ds = IndustrialDefectDataset(num_samples=700, mode='train', condition='normal')`
- `val_ds = IndustrialDefectDataset(num_samples=150, mode='val', condition='normal')`
- In `verify_metrics.py` line 66:
  `test_ds = IndustrialDefectDataset(num_samples=150, mode='val', condition=cond, seed=42)`

### 3.2 Random Seed Protocol
In `dataset.py` line 34:
```python
self.rng = np.random.RandomState(seed if mode == 'train' else seed + 1000)
```
- For `mode='train'`, the seed is $42$.
- For `mode='val'`, the seed is $42 + 1000 = 1042$.
- Because independent `RandomState` instances are used with completely distinct initial seeds ($42$ vs $1042$), the random sequences between training and validation are mathematically independent.

### 3.3 Dynamic Procedural Generation and Leakage Assessment
- **Image-Level Leakage:** Because training samples and validation samples are generated from different initial seeds and never share deterministic trajectories, there is **zero direct image duplication or exact feature leakage** between training and validation sets.
- **Epoch-Wise Dynamics:** In `main.py`, `train_loader` uses `shuffle=True`. As samples are requested in different order across epochs, `self.rng` advances along its random walk. Consequently, the network sees slightly different background textures and defect positions in each epoch. This acts as an implicit infinite-augmentation procedural generator.
- **Validation Determinism:** In `main.py` and `verify_metrics.py`, `val_loader` uses `shuffle=False`. Therefore, the 150 validation samples are generated in the exact same deterministic order on every evaluation run.

---

## 4. Ground Truth Mask Properties and Evaluation Suitability

1. **Topological Precision:** The procedurally synthesized masks are mathematically exact ($\mathbf{Y} \in \{0, 1\}$), with no human annotation noise, label ambiguity, or subjective boundary discrepancies.
2. **Area Distribution:** In the "tiny defects" regime, defect pixel count satisfies $|\mathcal{S}| \in [45, 600]$ pixels out of $256 \times 256 = 65,536$ pixels ($0.06\% \text{ to } 0.91\%$), strictly adhering to the $<1\%$ micro-scale definition.
3. **Suitability for Benchmarking:** While the procedural dataset provides a rigorous testbed for evaluating the mathematical capacity of deep architectures to preserve fine dendritic cracks and sharp boundaries, **it does not evaluate robustness against real physical mill anomalies, such as heavy oil droplets, camera sensor compression artifacts, or rolling chatter marks**.

---

## 5. Mandatory Manuscript Corrections and Remediation Plan

To uphold rigorous scientific integrity, the manuscript must be updated with the following corrections:

1. **Accurate Description of Benchmark:** Replace all claims that the paper evaluated the real NEU-Seg photographic database with an honest, transparent statement:
   > *"To evaluate the mathematical limits of micro-crack preservation and boundary delineation under controlled conditions, evaluations are performed on a high-fidelity procedural industrial steel surface defect benchmark (`IndustrialDefectDataset`) modeled after the morphological defect classes of the NEU database."*
2. **Correct Sample Numbers:** Update Section V.A from "1,800 images partitioned 1,260 / 270 / 270" to the actual numbers: **700 procedural training samples and 150 validation/test samples per condition**.
3. **Disclose Seed Setup:** Report seeds $42$ (training) and $1042$ (validation), noting that independent `RandomState` instances prevent data leakage.
4. **Acknowledge Real-World Gap:** Clearly describe the domain gap between synthetic procedural textures and production-line hot-rolled strip steel, framing physical mill deployment as essential future work.
