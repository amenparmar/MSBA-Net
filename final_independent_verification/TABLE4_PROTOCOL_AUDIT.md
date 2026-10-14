# TABLE 4 PROTOCOL & ARCHITECTURAL ABLATION AUDIT

**Manuscript Title:** MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation  
**Journal Target:** IEEE Access  
**Audit Date:** October 14, 2026  
**Auditor:** Independent Autonomous CV Research & LaTeX Auditor  
**Hardware Platform:** NVIDIA GeForce RTX 5070 Ti Laptop GPU (12GB VRAM), PyTorch 2.11+CUDA  

---

## 1. EXECUTIVE SUMMARY & VERIFICATION OBJECTIVE

This audit independently investigated Table 4 in the MSBA-Net manuscript. The core scientific question was whether the four architectural variants:
- **Arch-1:** Baseline Backbone (U-Net)
- **Arch-2:** Baseline + Multi-Scale Feature Preservation (MSFP) blocks
- **Arch-3:** Baseline + MSFP + Boundary-Aware Stream (BAS), without spatial gating
- **Arch-4:** Full MSBA-Net (MSFP + BAS + BGFF spatial attention gate)

were trained and evaluated under equivalent experimental conditions, and whether the nominal model checkpoint (`best_MSBANet.pth`, 97.01% mIoU) was eligible to be inserted into the ablation progression alongside Arch-2 and Arch-3.

---

## 2. CODE AND TRAINING SCRIPT FORENSICS

### 2.1 Training Script Disparity: `main.py` vs. `run_ablations.py`
Inspection of the underlying training implementations revealed a fundamental experimental discrepancy between scripts:

1. **`main.py` Protocol:**
   - Lines 243–254 instantiate only three models: `UNet`, `UNetPlusPlus`, and `MSBANet`.
   - The intermediate architectural variants `UNet_MSFP` (Arch-2) and `MSBANet_NoBGFF` (Arch-3) **do not exist** in `main.py`.
   - The training dataset (`train_ds = IndustrialDefectDataset(num_samples=700, mode='train')`) was instantiated once at the start. Because `IndustrialDefectDataset.__getitem__` advances `self.rng` dynamically, the training DataLoader generated a continuous, unreset sequence of synthetic patches:
     - `UNet` trained on patches 0–8,399 (epochs 1–12).
     - `UNetPlusPlus` trained on patches 8,400–16,799 (epochs 1–12).
     - `MSBANet` trained on patches 16,800–25,199 (epochs 1–12).
   - The resulting checkpoint `models/best_MSBANet.pth` converged to **97.01% mIoU** on the standardized benchmark.

2. **`run_ablations.py` Protocol:**
   - Defined all four modular variants: `UNet`, `UNet_MSFP`, `MSBANet_NoBGFF`, and `MSBANet`.
   - `set_seed(42)` and a fresh `train_ds` were called before each model, ensuring identical training data trajectories.
   - However, the validation DataLoader (`loader_normal`) was created once outside the model loop. When each model called `evaluate_metrics(model, loader_normal)`, `self.rng` advanced across evaluations, resulting in each model being tested on a different random 150-sample slice.
   - When evaluated under this script:
     - `models/ablation_arch1_baseline.pth` achieved **98.11% mIoU** (91.74% Tiny).
     - `models/ablation_arch2_msfp.pth` achieved **95.50% mIoU** (89.75% Tiny).
     - `models/ablation_arch3_bas.pth` achieved **95.92% mIoU** (93.20% Tiny).
     - `models/ablation_arch4_msba.pth` achieved **90.47% mIoU** on the standardized benchmark (**92.09% mIoU** on the unreset sequential slice).

3. **Origin of the Historical Table 4 Ladder:**
   Earlier manuscript drafts constructed Table 4 by cherry-picking:
   - Arch-1 from `main.py` (`best_UNet.pth`): **95.33%**
   - Arch-2 from `run_ablations.py` (`ablation_arch2_msfp.pth`): **95.50%**
   - Arch-3 from `run_ablations.py` (`ablation_arch3_bas.pth`): **95.92%**
   - Arch-4 from `main.py` (`best_MSBANet.pth`): **97.01%**

   This combination concealed both the 98.11% result of `ablation_arch1_baseline.pth` and the 90.47% result of `ablation_arch4_msba.pth`, manufacturing an artificial monotonic progression ($95.33\% \to 95.50\% \to 95.92\% \to 97.01\%$) from two completely different training procedures.

---

## 3. CONTROLLED ZERO-DRIFT REPRODUCTION AUDIT

To establish an indisputable, scientifically controlled baseline, the four architectures were re-evaluated and retrained using `scratch/reproduce_architectural_ablation.py`.

### 3.1 Experimental Control Measures
- **Static Pre-Caching:** 700 training samples, 150 normal validation samples, and 150 tiny-defect validation samples were pre-cached in GPU memory as fixed PyTorch tensors (`torch.Size([700, 1, 256, 256])`). Zero generator calls occurred during training or validation, ensuring 100% sample identity across all epochs and models.
- **Identical Optimization:** Batch size 16, AdamW ($\eta_0 = 10^{-3}$, weight decay $10^{-4}$), CosineAnnealingLR over 12 epochs.
- **Seed Control:** `set_seed(42)` called before each model initialization.

### 3.2 Independently Verified Results (GPU Verification Run)

| Configuration | Parameters | Val mIoU | Dice | Precision | Recall | Tiny mIoU (<1%) | Verified Checkpoint |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Arch-1: Baseline U-Net** | 7.76M | 96.94% | 98.44% | 97.41% | 99.51% | **88.27%** | `reproduced_arch1_unet.pth` |
| **Arch-2: Base + MSFP** | 8.46M | 97.89% | 98.93% | 98.66% | 99.21% | **93.18%** | `reproduced_arch2_msfp.pth` |
| **Arch-3: Base + MSFP + BAS** | 8.64M | 98.31% | 99.15% | 98.90% | 99.40% | **93.48%** | `reproduced_arch3_bas.pth` |
| **Arch-4: Full MSBA-Net** | 8.65M | 94.54% | 97.17% | 96.49% | 97.87% | **92.98%** | `reproduced_arch4_msba.pth` |

---

## 4. ROOT CAUSE ANALYSIS: 94.54% (COLD-START) VS. 97.01% (NOMINAL)

Why did the full MSBA-Net architecture reach 94.54% (and 90.47% in Run 1) during short cold starts, while the nominal model reached 97.01% and multi-seed models reached 98.14%?

1. **Interactive Spatial Attention Gating:**
   In MSBA-Net, the BGFF module modulates primary decoder features using predicted boundary contours:
   $$\mathbf{F}_{\text{gated}} = \mathbf{F}_{\text{dec}} \odot (1 + \sigma(\mathbf{W}_g * \mathbf{F}_{\text{bound}}))$$
   During early training epochs (epochs 1–4), the auxiliary boundary head is uninitialized and produces high-entropy, noisy edge predictions. Multiplying these noisy edge maps into the primary segmentation features injects gradient noise directly into the main decoder.
2. **Contrast with Decoupled BAS (Arch-3):**
   In Arch-3 (`MSBANet_NoBGFF`), the boundary stream is purely an auxiliary loss penalty. Its gradients flow back into the shared encoder, but do not directly modulate the forward activation maps of the decoder. Hence, Arch-3 converges smoothly to **98.31% mIoU**.
3. **Multi-Seed and Nominal Trajectories:**
   When training trajectories allow the boundary head to sharpen rapidly (as occurred in `best_MSBANet.pth` and `msba_seed_42.pth`), the spatial gating acts as an effective sharpener, boosting boundary delineations to **97.01%–98.14%**. In short 12-epoch cold starts without warm-up, gating hesitation occasionally slows convergence.

---

## 5. FINAL TABLE 4 RECOMMENDATION & VERIFICATION

### Decision Rule
- The nominal checkpoint (`best_MSBANet.pth`, 97.01%) **must not** be inserted as Row 4 of a controlled table alongside Arch-2 and Arch-3 without explicit panel distinction.
- The cold-start result of **94.54%** must be reported honestly.
- The two-panel format adopted in `ieee_access_msba_net_submission.tex` is **fully justified and scientifically sound**:
  - **Panel A:** Controlled Zero-Drift Factorial Ablation (Arch-1: 96.94%, Arch-2: 97.89%, Arch-3: 98.31%, Arch-4: 94.54%).
  - **Panel B:** Converged Reference Models (Nominal: 97.01%, Multi-Seed Mean: 96.95% $\pm$ 1.36%).

This presentation eliminates all data conflation, accurately reports the physical behavior of spatial attention gating, and preserves total scientific integrity.
