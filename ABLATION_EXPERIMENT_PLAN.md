# MSBA-Net: Reproducible Ablation Experiment Plan
**Document ID:** `review_audit/ABLATION_EXPERIMENT_PLAN.md`  
**Execution Date:** October 13, 2026  
**Hardware Environment:** NVIDIA GeForce RTX 5070 Ti Laptop GPU (CUDA 13.0, PyTorch 2.11)  
**Evaluation Target:** Resolve Reviewer #2 Comment 7 (R2.7) and Reviewer #2 Comment 8 (R2.8)  

---

## 1. Objective and Scientific Hypothesis

The objective of this controlled ablation study is to independently isolate and quantify the empirical contributions of:
1. **Multi-Scale Feature Preservation (MSFP) Block:** Evaluates whether parallel multi-rate dilated branches ($r \in \{1, 2, 4\}$) prevent feature vanishing on sub-1% micro-scale defects.
2. **Auxiliary Boundary-Aware Stream (BAS):** Evaluates whether explicit edge supervision via morphological gradient loss enhances contour localization.
3. **Boundary-Guided Feature Fusion (BGFF) Gate:** Evaluates whether residual multiplicative spatial gating $((1 + \mathbf{G}) \odot \mathbf{F})$ effectively sharpens indistinct low-contrast defect transitions.
4. **Composite Loss Terms:** Evaluates the relative contributions of Binary Cross-Entropy ($\mathcal{L}_{\text{BCE}}$), Soft Dice ($\mathcal{L}_{\text{Dice}}$), Focal Loss ($\mathcal{L}_{\text{Focal}}$), and Boundary Loss ($\mathcal{L}_{\text{bound}}$).
5. **Statistical Stability:** Evaluates mean $\pm$ standard deviation across 3 independent random seeds ($42, 100, 2026$) to address statistical variation (R2.8).

---

## 2. Experimental Configurations

### Part A: Architectural Factorial Configurations
All models share identical encoder base channels ($C \in \{32, 64, 128, 256\}$, bottleneck $512$), input resolution ($256 \times 256$), and decoder topology:

| Config ID | Model Designation | MSFP Blocks | BAS Stream | BGFF Gate | Loss Function | Checkpoint Output |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Arch-1** | Baseline Backbone (U-Net) | $\times$ | $\times$ | $\times$ | Composite Loss ($\lambda_b=0$) | `models/ablation_arch1_baseline.pth` |
| **Arch-2** | Baseline + MSFP | $\checkmark$ | $\times$ | $\times$ | Composite Loss ($\lambda_b=0$) | `models/ablation_arch2_msfp.pth` |
| **Arch-3** | Baseline + MSFP + BAS (No Gating) | $\checkmark$ | $\checkmark$ | $\times$ | Full Composite Loss | `models/ablation_arch3_bas.pth` |
| **Arch-4** | Full MSBA-Net (MSFP + BAS + BGFF)| $\checkmark$ | $\checkmark$ | $\checkmark$ | Full Composite Loss | `models/ablation_arch4_msba.pth` |

### Part B: Composite Loss Component Configurations
Evaluated on the full MSBA-Net architecture with fixed random seed ($42$):

| Config ID | Loss Formulation | $\lambda_{\text{bce}}$ | $\lambda_{\text{dice}}$ | $\lambda_{\text{focal}}$ | $\lambda_{\text{boundary}}$ | Checkpoint Output |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Loss-1** | $\mathcal{L}_{\text{BCE}}$ Only | $1.0$ | $0.0$ | $0.0$ | $0.0$ | `models/ablation_loss1_bce.pth` |
| **Loss-2** | $\mathcal{L}_{\text{BCE}} + \mathcal{L}_{\text{Dice}}$ | $1.0$ | $1.0$ | $0.0$ | $0.0$ | `models/ablation_loss2_bce_dice.pth` |
| **Loss-3** | $\mathcal{L}_{\text{BCE}} + \mathcal{L}_{\text{Dice}} + \mathcal{L}_{\text{Focal}}$ | $1.0$ | $1.0$ | $0.5$ | $0.0$ | `models/ablation_loss3_bce_dice_focal.pth` |
| **Loss-4** | Full Composite Loss | $1.0$ | $1.0$ | $0.5$ | $0.4$ | `models/ablation_loss4_full.pth` |

### Part C: Multi-Seed Statistical Variance
- **Model:** Full MSBA-Net (Arch-4 / Loss-4)
- **Seeds Tested:** $42$, $100$, $2026$
- **Target Metrics:** Mean $\pm$ Standard Deviation for Overall mIoU, Dice, Precision, Recall, and Tiny Defect mIoU ($\text{mIoU}_{\text{tiny}}$).

---

## 3. Strict Experimental Controls and Protocol

1. **Dataset & Split:** `IndustrialDefectDataset` ($700$ training images, $150$ validation images per condition, $256 \times 256 \times 1$).
2. **Optimizer & Schedule:** AdamW ($\text{lr} = 1 \times 10^{-3}$, weight decay $= 1 \times 10^{-4}$), CosineAnnealingLR decay over $12$ epochs.
3. **Batch Size:** $16$ patches per mini-batch.
4. **Evaluation Set:** Independent, deterministic evaluation on $150$ validation samples using seed $1042$ (Normal condition) and Tiny Defect condition ($|\mathcal{S}| < 0.01$).
5. **Metric Calculation:** Computed strictly using `losses.calculate_metrics()` over whole evaluation passes (IoU, Dice, Precision, Recall, Accuracy).
6. **Integrity Rule:** Results will be written to `review_audit/ABLATION_RESULTS.csv` strictly from executed code runs. Zero numbers will be fabricated.
