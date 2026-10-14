# MSBA-Net: Model Architecture, Parameter Count & Complexity Verification
**Document ID:** `final_reconciliation/MODEL_ARCHITECTURE_VERIFICATION.md`  
**Audit Date:** October 14, 2026  
**Auditor:** Antigravity Autonomous Research & Forensic Audit Engine  
**Paper Title:** *MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation*  
**Target Venue:** *IEEE Access*  

---

## 1. Executive Summary

This report establishes the complete structural verification of MSBA-Net as implemented in `models.py` in compliance with **Critical Task E**, **Issue 4**, and **Reviewer 2, Comment 10 (R2.10)**.

### Architectural Reality Confirmed:
1. **Total Trainable Parameters:** **8,650,786 (8.650786 Million)**. The original manuscript claim of 9.38 Million parameters was an unverified draft approximation.
2. **Encoder Channel Progression:** **$\{32, 64, 128, 256\}$** with base channel $C=32$, rather than $\{64, 128, 256, 512\}$.
3. **Bottleneck Dimension:** **512 Channels** at $16 \times 16$ spatial resolution ($32 \times 32$ pooling depth).
4. **Computational Complexity ($256 \times 256 \times 1$ Input):**
   - **FLOPs (Floating Point Operations):** **42.32 GFLOPs** ($42,324,721,664$ FLOPs).
   - **MACs (Multiply-Accumulate Operations):** **21.16 GMACs** ($21,162,360,832$ MACs).
   - *Baseline U-Net Complexity:* 27.29 GFLOPs / 13.64 GMACs.

---

## 2. Layer-by-Layer Submodule Parameter Breakdown

Computed via PyTorch parameter traversal on instantiated `MSBANet(in_channels=1, num_classes=1, base_ch=32)`:

| Component Category | Submodule Name | Layer Specification / Input $\to$ Output Shape | Parameter Count | Subtotal Parameters |
| :--- | :--- | :--- | :---: | :---: |
| **Encoder Stage 1** | `enc1` | ConvBlock: $1 \to 32 \to 32$ ($3 \times 3$ convs, BN, ReLU) | 9,632 | |
| | `msfp1` | MultiScaleFeaturePreservation ($32 \to 32$, $r \in \{1, 2, 4\}$) | 8,320 | **17,952 (0.018M)** |
| **Encoder Stage 2** | `enc2` | ConvBlock: $32 \to 64 \to 64$ ($3 \times 3$ convs, BN, ReLU) | 55,552 | |
| | `msfp2` | MultiScaleFeaturePreservation ($64 \to 64$, $r \in \{1, 2, 4\}$) | 33,024 | **88,576 (0.089M)** |
| **Encoder Stage 3** | `enc3` | ConvBlock: $64 \to 128 \to 128$ ($3 \times 3$ convs, BN, ReLU) | 221,696 | |
| | `msfp3` | MultiScaleFeaturePreservation ($128 \to 128$, $r \in \{1, 2, 4\}$) | 131,584 | **353,280 (0.353M)** |
| **Encoder Stage 4** | `enc4` | ConvBlock: $128 \to 256 \to 256$ ($3 \times 3$ convs, BN, ReLU) | 885,760 | |
| | `msfp4` | MultiScaleFeaturePreservation ($256 \to 256$, $r \in \{1, 2, 4\}$) | 525,312 | **1,411,072 (1.411M)** |
| **Bottleneck** | `bottleneck` | ConvBlock: $256 \to 512 \to 512$ ($3 \times 3$ convs, BN, ReLU) | 3,540,992 | **3,540,992 (3.541M)** |
| **Auxiliary Stream (BAS)**| `b_up3` | ConvTranspose2d: $128 \to 64$ ($2 \times 2$, stride 2) | 32,832 | |
| | `b_conv3` | ConvBlock: $128 \to 64 \to 64$ ($3 \times 3$ convs, BN, LeakyReLU) | 110,848 | |
| | `b_up2` | ConvTranspose2d: $64 \to 32$ ($2 \times 2$, stride 2) | 8,224 | |
| | `b_conv2` | ConvBlock: $64 \to 32 \to 32$ ($3 \times 3$ convs, BN, LeakyReLU) | 27,776 | |
| | `b_head` | Conv2d: $32 \to 1$ ($1 \times 1$ conv) | 33 | **179,713 (0.180M)** |
| **Main Decoder** | `up4` | ConvTranspose2d: $512 \to 256$ ($2 \times 2$, stride 2) | 524,544 | |
| | `dec4` | ConvBlock: $512 \to 256 \to 256$ ($3 \times 3$ convs, BN, ReLU) | 1,770,496 | |
| | `up3` | ConvTranspose2d: $256 \to 128$ ($2 \times 2$, stride 2) | 131,200 | |
| | `dec3` | ConvBlock: $256 \to 128 \to 128$ ($3 \times 3$ convs, BN, ReLU) | 442,880 | |
| | `up2` | ConvTranspose2d: $128 \to 64$ ($2 \times 2$, stride 2) | 32,832 | |
| | `dec2` | ConvBlock: $128 \to 64 \to 64$ ($3 \times 3$ convs, BN, ReLU) | 110,848 | |
| | `up1` | ConvTranspose2d: $64 \to 32$ ($2 \times 2$, stride 2) | 8,224 | |
| | `dec1` | ConvBlock: $64 \to 32 \to 32$ ($3 \times 3$ convs, BN, ReLU) | 27,776 | **3,048,800 (3.049M)** |
| **Spatial Fusion (BGFF)** | `bg_fusion` | BoundaryAwareFusion: Conv2d, BN, Sigmoid, ConvBlock ($32 \to 32$) | 10,368 | **10,368 (0.010M)** |
| **Segmentation Head** | `seg_head` | Conv2d: $32 \to 1$ ($1 \times 1$ conv) | 33 | **33 (0.000M)** |
| **TOTAL MODEL** | **MSBANet** | **Complete Network Forward Path** | **8,650,786** | **8,650,786 (8.65M)** |

---

## 3. Submodule Architectural Mechanics

### 3.1 Multi-Scale Feature Preservation (MSFP) Block
Let feature tensor at stage $l$ be $\mathbf{X}_l \in \mathbb{R}^{C_l \times H_l \times W_l}$.
Channels are divided into four parallel branches $\mathbf{B}_1, \mathbf{B}_2, \mathbf{B}_3, \mathbf{B}_4 \in \mathbb{R}^{(C_l/4) \times H_l \times W_l}$:
1. Branch 1: Pointwise bottleneck projection $\mathbf{W}_1 *_{1\times 1} \mathbf{X}_l$.
2. Branch 2: Standard dilated branch $\mathbf{W}_2 *_{3\times 3}^{r=1} \mathbf{X}_l$ (padding $p=1$, footprint $3 \times 3$).
3. Branch 3: Medium dilated branch $\mathbf{W}_3 *_{3\times 3}^{r=2} \mathbf{X}_l$ (padding $p=2$, footprint $5 \times 5$).
4. Branch 4: Wide dilated branch $\mathbf{W}_4 *_{3\times 3}^{r=4} \mathbf{X}_l$ (padding $p=4$, footprint $9 \times 9$).
- **Effective Dilated Footprint Span:**
  $$k_{\text{eff}} = k + (k - 1)(r - 1) = (k - 1)r + 1$$
- **Cumulative Receptive Field Recurrence:**
  $$RF_l = RF_{l-1} + (k_{\text{eff}} - 1) \cdot S_{l-1}$$
  where $S_{l-1} = 2^{l-1}$ is cumulative preceding stride.
- **Fusion and Residual Connection:**
  $$\mathbf{X}_l^{\text{MSFP}} = \mathbf{X}_l + \text{ReLU}\left(\text{BN}\left(\mathbf{W}_{\text{fuse}} *_{1\times 1} [\mathbf{B}_1, \mathbf{B}_2, \mathbf{B}_3, \mathbf{B}_4]\right)\right)$$

### 3.2 Auxiliary Boundary-Aware Stream (BAS)
- Receives multi-level features: $\mathbf{X}_1^{\text{MSFP}}$ ($256 \times 256$, 32 ch), $\mathbf{X}_2^{\text{MSFP}}$ ($128 \times 128$, 64 ch), $\mathbf{X}_3^{\text{MSFP}}$ ($64 \times 64$, 128 ch).
- Reconstructs high-resolution contour field:
  $$\mathbf{F}_{\text{bound}, 2} = \text{ConvBlock}\left(\left[\text{Up}_{2\times}(\mathbf{X}_3^{\text{MSFP}}), \mathbf{X}_2^{\text{MSFP}}\right]\right) \in \mathbb{R}^{64 \times 128 \times 128}$$
  $$\mathbf{F}_{\text{bound}, 1} = \text{ConvBlock}\left(\left[\text{Up}_{2\times}(\mathbf{F}_{\text{bound}, 2}), \mathbf{X}_1^{\text{MSFP}}\right]\right) \in \mathbb{R}^{32 \times 256 \times 256}$$
- **Auxiliary Output:** $\hat{\mathbf{Y}}_{\text{bound}} = \sigma(\mathbf{W}_{\text{out}}^{\text{bound}} *_{1\times 1} \mathbf{F}_{\text{bound}, 1})$.

### 3.3 Boundary-Guided Feature Fusion (BGFF) Module
- **Spatial Gate Generation:**
  $$\mathbf{G}_{\text{bound}} = \sigma\left(\text{BN}\left(\mathbf{W}_g *_{1\times 1} \mathbf{F}_{\text{bound}, 1}\right)\right) \in [0, 1]^{1 \times 256 \times 256}$$
- **Residual Multiplicative Modulation:**
  $$\tilde{\mathbf{F}}_{\text{seg}} = \text{ConvBlock}\left(\mathbf{F}_{\text{seg}, 1} \odot (\mathbf{1} + \mathbf{G}_{\text{bound}})\right) \in \mathbb{R}^{32 \times 256 \times 256}$$
- **Segmentation Output:** $\hat{\mathbf{Y}}_{\text{mask}} = \sigma(\mathbf{W}_{\text{out}}^{\text{seg}} *_{1\times 1} \tilde{\mathbf{F}}_{\text{seg}})$.

---

## 4. Inference Latency & Computational Profiling

Measured on an NVIDIA GPU (FP32 precision, batch size 1, $256 \times 256$ input):
- **PyTorch FP32 Latency:** 24.3 ms per patch ($\sim$41.1 FPS).
- **TensorRT FP16 Projection:** Theoretical throughput estimate $\sim$88 FPS (satisfying near-line cold-rolling monitoring requirements).
- **FLOPs / MACs Convention:**
  - 42.32 GFLOPs (counting adds and multiplies as 2 FLOPs).
  - 21.16 GMACs (counting multiply-accumulate pairs as 1 MAC).
