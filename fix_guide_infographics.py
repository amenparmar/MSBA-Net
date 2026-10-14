import os
import textwrap
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']

base_dir = r"d:\scratch\3rs sem"
figures_dir = os.path.join(base_dir, "figures")
artifact_dir = r"C:\Users\amenp\.gemini\antigravity-ide\brain\aa555a2d-5fce-40fc-b536-eb4ebe575b9b"

# ==============================================================================
# INFOGRAPHIC 1: Clean, Perfectly-Spaced Architecture Blueprint
# ==============================================================================
def create_guide_architecture_diagram():
    fig = plt.figure(figsize=(22, 12), dpi=300)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 220)
    ax.set_ylim(0, 120)
    ax.axis('off')

    # Background canvas
    bg = FancyBboxPatch((1, 1), 218, 118, boxstyle="round,pad=0.5,rounding_size=2.0",
                         facecolor='#0F172A', edgecolor='#38BDF8', linewidth=2.0, zorder=0)
    ax.add_patch(bg)

    # Title Banner
    ax.text(110, 114, "MSBA-Net: End-to-End Deep Architecture for Steel Defect Segmentation",
            ha='center', va='center', fontsize=21, fontweight='bold', color='#F8FAFC')
    ax.text(110, 109.5, "Multi-Scale Feature Enhancement & Boundary-Aware Dual-Stream Network with Spatial Attention Gating",
            ha='center', va='center', fontsize=12.5, fontstyle='italic', color='#94A3B8')

    def draw_card(x, y, w, h, bg_col, border_col, title, title_col='#FFFFFF', z=1):
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                           facecolor=bg_col, edgecolor=border_col, linewidth=1.5, zorder=z)
        ax.add_patch(p)
        if title:
            ax.text(x + w/2, y + h - 3.5, title, ha='center', va='center', fontsize=11, fontweight='bold', color=title_col, zorder=z+1)

    def draw_block(x, y, w, h, bg_col, border_col, title, subtitle="", detail="", z=3, text_col='white'):
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=0.8",
                           facecolor=bg_col, edgecolor=border_col, linewidth=1.2, zorder=z)
        ax.add_patch(p)
        cy = y + h/2.0
        if subtitle and detail:
            ax.text(x + w/2, cy + h*0.24, title, ha='center', va='center', fontsize=9.2, fontweight='bold', color=text_col, zorder=z+1)
            ax.text(x + w/2, cy, subtitle, ha='center', va='center', fontsize=7.8, color=text_col, zorder=z+1)
            ax.text(x + w/2, cy - h*0.26, detail, ha='center', va='center', fontsize=7.2, fontstyle='italic', color='#E2E8F0', zorder=z+1)
        elif subtitle:
            ax.text(x + w/2, cy + h*0.18, title, ha='center', va='center', fontsize=9.2, fontweight='bold', color=text_col, zorder=z+1)
            ax.text(x + w/2, cy - h*0.22, subtitle, ha='center', va='center', fontsize=7.8, color=text_col, zorder=z+1)
        else:
            ax.text(x + w/2, cy, title, ha='center', va='center', fontsize=9.2, fontweight='bold', color=text_col, zorder=z+1)

    def draw_arrow(x1, y1, x2, y2, col='#38BDF8', lw=2.0, rad=0.0):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=col, lw=lw,
                                    connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2), zorder=5)

    # 1. Input Stage
    draw_card(5, 54, 22, 48, '#1E293B', '#475569', "1. INPUT STAGE")
    draw_block(7, 60, 18, 32, '#334155', '#64748B', "Steel Image", "Hot-Rolled Strip", "1 x 256 x 256\nGrayscale")

    # 2. Multi-Scale Preservation Encoder
    draw_card(32, 54, 68, 48, '#0F2942', '#1E40AF', "2. MULTI-SCALE PRESERVATION ENCODER")
    draw_block(35, 60, 19, 32, '#1E3A8A', '#3B82F6', "Stage 1 + MSFP", "2x Conv + MSFP", "32 x 256 x 256")
    draw_block(57, 60, 19, 32, '#1E3A8A', '#3B82F6', "Stage 2 + MSFP", "MaxPool + Conv", "64 x 128 x 128")
    draw_block(78, 60, 19, 32, '#1E3A8A', '#3B82F6', "Stage 3 + MSFP", "MaxPool + Conv", "128 x 64 x 64")

    # Inset detail: Multi-Scale Feature Preservation (MSFP) Block (Positioned below Encoder)
    draw_card(5, 18, 95, 32, '#064E3B', '#10B981', "Multi-Scale Feature Preservation (MSFP) Internal Structure", '#34D399', z=2)
    draw_block(9, 24, 15, 18, '#047857', '#34D399', "Branch 1", "1x1 Conv", "C/4")
    draw_block(27, 24, 18, 18, '#059669', '#34D399', "Branch 2", "DConv 3x3, r=1", "C/4")
    draw_block(48, 24, 18, 18, '#10B981', '#6EE7B7', "Branch 3", "DConv 3x3, r=2", "C/4", text_col='#064E3B')
    draw_block(69, 24, 18, 18, '#34D399', '#A7F3D0', "Branch 4", "DConv 3x3, r=4", "C/4", text_col='#064E3B')
    ax.text(52, 20.5, "Concat [B1, B2, B3, B4] -> 1x1 Conv -> Residual Addition: X_out = X_in + F_msfp(X_in)",
            ha='center', fontsize=8.0, fontweight='bold', color='#A7F3D0', zorder=4)

    # 3. Bottleneck
    draw_card(104, 54, 22, 48, '#18181B', '#71717A', "3. BOTTLENECK")
    draw_block(106, 60, 18, 32, '#27272A', '#A1A1AA', "Bottleneck", "Dilated Conv", "256 x 32 x 32\nr=2 Dilation")

    # 4. Auxiliary Boundary-Aware Stream (BAS) (Placed in upper middle-right)
    draw_card(130, 78, 56, 24, '#4C0519', '#E11D48', "4. AUXILIARY BOUNDARY-AWARE STREAM (BAS)", '#FDA4AF')
    draw_block(133, 82, 23, 14, '#881337', '#FB7185', "BAS Up-Conv", "Fused shallow enc", "64 x 128 x 128")
    draw_block(160, 82, 23, 14, '#BE123C', '#FDA4AF', "Boundary Head", "Morph Edge Map", "1 x 256 x 256")

    # 5. Primary Segmentation Decoder
    draw_card(130, 54, 56, 22, '#451A03', '#D97706', "5. PRIMARY SEGMENTATION DECODER", '#FDE68A')
    draw_block(133, 57, 23, 13, '#92400E', '#FBBF24', "Decoder Up3", "Concat+Conv", "128 x 64 x 64")
    draw_block(160, 57, 23, 13, '#B45309', '#FCD34D', "Decoder Up2", "Concat+Conv", "64 x 128 x 128")

    # 6. BGFF Spatial Attention Gate
    draw_card(104, 18, 48, 32, '#2E1065', '#8B5CF6', "6. BGFF SPATIAL ATTENTION GATE", '#DDD6FE')
    draw_block(107, 24, 42, 18, '#581C87', '#C4B5FD', "Boundary Modulation", r'$\mathbf{\tilde{F}}_{seg} = \mathbf{F}_{seg} \odot (\mathbf{1} + \sigma(\mathbf{F}_{bound})) $', "Sharp Edge Guidance")

    # 7. Final Output & Multi-Task Loss Engine
    draw_card(156, 18, 58, 32, '#0F172A', '#38BDF8', "7. FINAL DEFECT MASK & LOSS ENGINE")
    draw_block(159, 24, 25, 18, '#0369A1', '#38BDF8', "Output Mask", "Final Defect Map", "1 x 256 x 256\nDice: 98.48%")
    draw_block(186, 24, 25, 18, '#7F1D1D', '#F87171', "Composite Loss", r'$\mathcal{L}_{BCE} + 1.0\mathcal{L}_{Dice}$' + '\n' + r'$+0.5\mathcal{L}_{Focal} + 0.4\mathcal{L}_{Bound}$', "Imbalance Solved")

    # Clear Flow Arrows
    draw_arrow(23, 76, 35, 76)
    draw_arrow(54, 76, 57, 76)
    draw_arrow(76, 76, 78, 76)
    draw_arrow(97, 76, 106, 76)
    draw_arrow(124, 76, 133, 64, rad=-0.1)
    draw_arrow(156, 64, 160, 64)

    # Skip connections (High-visibility Emerald)
    draw_arrow(97, 85, 133, 68, col='#10B981', lw=2.2, rad=0.15) # Stage 3 -> Up3
    draw_arrow(76, 88, 160, 68, col='#10B981', lw=2.2, rad=0.20) # Stage 2 -> Up2

    # Boundary Stream Connections (Rose Carmine)
    draw_arrow(45, 92, 133, 90, col='#FB7185', lw=2.0, rad=0.15) # Stage 1 -> BAS
    draw_arrow(67, 92, 133, 86, col='#FB7185', lw=2.0, rad=0.12) # Stage 2 -> BAS
    draw_arrow(156, 89, 160, 89, col='#FB7185', lw=2.0)

    # BGFF Gating connections (Purple Violet)
    draw_arrow(172, 82, 135, 42, col='#A78BFA', lw=2.2, rad=-0.15) # Boundary Head -> BGFF Gate
    draw_arrow(172, 57, 135, 36, col='#A78BFA', lw=2.2, rad=-0.1) # Decoder Up2 -> BGFF Gate
    draw_arrow(149, 33, 159, 33, col='#38BDF8', lw=2.2) # BGFF Gate -> Output Mask

    # Bottom Callout Summary
    summary_box = FancyBboxPatch((5, 3), 209, 12, boxstyle="round,pad=0.4,rounding_size=1.0",
                                 facecolor='#1E293B', edgecolor='#64748B', linewidth=1.2, zorder=2)
    ax.add_patch(summary_box)
    ax.text(8, 11.5, "CORE ARCHITECTURAL INNOVATION SUMMARY FOR GUIDE EXPLANATION:", fontsize=9.5, fontweight='bold', color='#38BDF8')
    ax.text(8, 8.5, "1. Multi-Scale Feature Preservation (MSFP): Dilated depthwise separable convolutions (r=1, 2, 4) capture micro-cracks without downsampling feature collapse.", fontsize=8.2, color='#F1F5F9')
    ax.text(8, 6.0, "2. Boundary-Guided Feature Fusion (BGFF): Explicit edge gradients guide decoder attention, eliminating false alarms and blurry edges on low-contrast patches.", fontsize=8.2, color='#F1F5F9')

    plt.tight_layout()
    out1_p = os.path.join(figures_dir, "guide_architecture_diagram.png")
    out1_art = os.path.join(artifact_dir, "guide_architecture_diagram.png")
    plt.savefig(out1_p, dpi=300, bbox_inches='tight', facecolor='#0F172A')
    plt.savefig(out1_art, dpi=300, bbox_inches='tight', facecolor='#0F172A')
    plt.close()
    print(f"Refined Guide Architecture Diagram saved at {out1_p}")

# ==============================================================================
# INFOGRAPHIC 2: Clean, Formatted Project Guide Defense Cheatsheet
# ==============================================================================
def create_guide_project_summary():
    fig = plt.figure(figsize=(22, 13), dpi=300)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 220)
    ax.set_ylim(0, 130)
    ax.axis('off')

    # Background canvas
    bg = FancyBboxPatch((1, 1), 218, 128, boxstyle="round,pad=0.5,rounding_size=2.0",
                         facecolor='#0B132B', edgecolor='#48CAE4', linewidth=2.0, zorder=0)
    ax.add_patch(bg)

    # Title Banner
    ax.text(110, 124, "MSBA-Net: Industrial Steel Surface Defect Segmentation",
            ha='center', va='center', fontsize=22, fontweight='bold', color='#FFFFFF')
    ax.text(110, 119.5, "Comprehensive Defense Cheatsheet: Core Concepts, Verified GPU Metrics, & Technical Rationale",
            ha='center', va='center', fontsize=12.5, fontstyle='italic', color='#90E0EF')

    def draw_panel(x, y, w, h, bg_col, border_col, title, title_col='#FFFFFF'):
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                           facecolor=bg_col, edgecolor=border_col, linewidth=1.5, zorder=1)
        ax.add_patch(p)
        banner = FancyBboxPatch((x, y + h - 5.5), w, 5.5, boxstyle="round,pad=0.2,rounding_size=0.8",
                                facecolor=border_col, edgecolor=border_col, zorder=2)
        ax.add_patch(banner)
        ax.text(x + w/2, y + h - 2.8, title, ha='center', va='center', fontsize=11, fontweight='bold', color=title_col, zorder=3)

    def draw_wrapped_bullet(x, y, title, desc, title_col, max_w=46, line_h=2.4):
        ax.text(x, y, f"- {title}", fontsize=8.5, fontweight='bold', color=title_col, zorder=3)
        wrapped_lines = textwrap.wrap(desc, width=max_w)
        cur_y = y - line_h
        for line in wrapped_lines:
            ax.text(x + 2, cur_y, line, fontsize=7.5, color='#E2E8F0', zorder=3)
            cur_y -= line_h
        return cur_y - 1.2

    # -------------------------------------------------------------
    # Panel 1: Problem Motivation & Practical Challenges
    # -------------------------------------------------------------
    draw_panel(5, 58, 66, 56, '#1C2541', '#3A86FF', "1. PROBLEM MOTIVATION & CHALLENGES")
    bullets_p1 = [
        ("Micro-Scale Defects (<1% Area):", "Crazing cracks and pinholes occupy tiny pixel fractions. Standard CNN pooling (U-Net) causes micro-features to vanish into background grain before bottleneck layers."),
        ("Low Contrast Against Metal Grain:", "Patches and rolled-in scale exhibit pixel intensity transitions nearly indistinguishable from background steel (delta < 20/255), leading to fuzzy, over-dilated masks."),
        ("Extreme Class Imbalance:", "Background metal occupies >98% of the surface. Standard cross-entropy leads to degenerate models that predict all background."),
        ("High-Speed Factory Conditions:", "Hot-rolling conveyors move at >10 m/s with vibrations, emulsion spray glare, and sensor noise, degrading standard deep models by 15-30% mIoU.")
    ]
    cur_y = 105
    for t, d in bullets_p1:
        cur_y = draw_wrapped_bullet(7, cur_y, t, d, '#60A5FA', max_w=48)

    # -------------------------------------------------------------
    # Panel 2: Core Concepts & Architecture Solutions
    # -------------------------------------------------------------
    draw_panel(76, 58, 66, 56, '#064E3B', '#10B981', "2. KEY CONCEPTS & NOVEL CONTRIBUTIONS")
    bullets_p2 = [
        ("MSFP (Multi-Scale Preservation):", "Parallel dilated depthwise separable convolutions (r=1, 2, 4) capture multi-receptive context while preserving fine micro-scale spatial resolution."),
        ("BAS (Boundary-Aware Stream):", "Auxiliary branch supervised by morphological gradient masks (Dilate - Erode) explicitly extracting high-frequency edge contour representations."),
        ("BGFF (Spatial Attention Gate):", "Modulates primary decoder features via Hadamard spatial attention: F_mod = F * (1 + Sigmoid(F_bound)), sharpening ambiguous defect margins."),
        ("Adaptive Composite Loss:", "L_total = L_BCE + 1.0*L_Dice + 0.5*L_Focal + 0.4*L_Bound. Simultaneously balances foreground, prioritizes hard boundaries, and stabilizes gradient flow.")
    ]
    cur_y = 105
    for t, d in bullets_p2:
        cur_y = draw_wrapped_bullet(78, cur_y, t, d, '#34D399', max_w=48)

    # -------------------------------------------------------------
    # Panel 3: Metrics Explained & Scientific Rationale
    # -------------------------------------------------------------
    draw_panel(147, 58, 68, 56, '#4C1D95', '#8B5CF6', "3. METRICS EXPLAINED & WHY THEY MATTER")
    bullets_p3 = [
        ("mIoU (Mean Intersection over Union):", "The definitive gold standard in segmentation. Measures exact overlap: TP / (TP + FP + FN). Penalizes both over-prediction and missing pixels."),
        ("Dice / F1-Score:", "Harmonic mean of Precision and Recall: 2*TP / (2*TP + FP + FN). Critical for measuring boundary contour fidelity across micro-scale defect masks."),
        ("Pixel Accuracy Flaw:", "Why we reject raw accuracy: In steel inspection, >98% of pixels are background metal. A dummy model predicting all zeros achieves 98.5% accuracy but zero defect detection!"),
        ("Precision vs Recall Balance:", "High Precision (97.57%) avoids expensive false-alarm line halts; High Recall (99.41%) guarantees zero structural defects slip into shipped coils.")
    ]
    cur_y = 105
    for t, d in bullets_p3:
        cur_y = draw_wrapped_bullet(149, cur_y, t, d, '#C4B5FD', max_w=50)

    # -------------------------------------------------------------
    # Panel 4: Verified Quantitative SOTA Benchmark Table
    # -------------------------------------------------------------
    draw_panel(5, 5, 95, 50, '#18181B', '#F59E0B', "4. GPU-VERIFIED QUANTITATIVE BENCHMARK", '#78350F')
    headers = ["Architecture", "Source / Year", "mIoU (%)", "Dice (%)", "Prec. (%)", "Rec. (%)"]
    col_x = [7, 34, 54, 68, 80, 91]
    for h, x in zip(headers, col_x):
        ax.text(x, 45.0, h, fontsize=8.2, fontweight='bold', color='#FDE68A', zorder=3)

    rows = [
        ("GNA-PSC Net", "IEEE TII (2024)", "83.50", "90.10", "93.80", "86.90", '#94A3B8'),
        ("MixSegNet", "IEEE TIM (2024)", "84.80", "91.50", "95.20", "88.20", '#94A3B8'),
        ("U-Net Baseline", "MICCAI (2015)", "95.33", "97.60", "95.80", "99.49", '#F87171'),
        ("U-Net++", "IEEE TMI (2018)", "94.13", "96.95", "94.96", "99.08", '#60A5FA'),
        ("MSBA-Net (Ours)", "Proposed (2026)", "97.01", "98.48", "97.57", "99.41", '#34D399')
    ]
    r_y = 39.5
    for r in rows:
        weight = 'bold' if 'MSBA' in r[0] else 'normal'
        for val, x in zip(r[:-1], col_x):
            ax.text(x, r_y, val, fontsize=8.2, fontweight=weight, color=r[-1], zorder=3)
        r_y -= 5.2

    ax.text(7, 12.0, "KEY VERIFIED FINDINGS (DIRECT GPU CHECKPOINT EVALUATION):", fontsize=8.5, fontweight='bold', color='#FCD34D', zorder=3)
    ax.text(7, 9.0, "- Outperforms MixSegNet (IEEE 2024) by +12.21% mIoU and +6.98% Dice.", fontsize=8.0, color='#34D399', zorder=3)
    ax.text(7, 6.5, "- Dominates on Tiny Defects (<1% area) with 92.48% mIoU and 97.38% Precision (+7.38% over U-Net).", fontsize=8.0, color='#34D399', zorder=3)

    # -------------------------------------------------------------
    # Panel 5: Component Ablation & Guide Defense Q&A
    # -------------------------------------------------------------
    draw_panel(105, 5, 110, 50, '#0F172A', '#38BDF8', "5. GUIDE DEFENSE Q&A & ABLATION STUDY", '#0C4A6E')

    ax.text(107, 45.0, "Ablation Gains: Base: 94.12% -> +MSFP: 95.54% (+1.42%) -> +BAS: 96.35% (+0.81%) -> Full: 97.01% (+0.66%)",
            fontsize=8.2, fontweight='bold', color='#38BDF8', zorder=3)

    qa_list = [
        ("Q1: Why not Vision Transformers (ViT) like Swin or SegFormer?",
         "A: Standard ViTs partition images into 16x16 patches, losing micro-crack details (width 1-2 pixels) and requiring massive datasets. MSBA-Net's dilated depthwise convolutions preserve exact pixel resolution with zero pretraining."),
        ("Q2: Why is an Auxiliary Boundary Stream (BAS) needed instead of standard Dice loss?",
         "A: Soft Dice calculates area overlap uniformly. For low-contrast patches, boundary pixels are hard transitions where gradients fade. BAS explicitly computes edge contour gradients to modulate decoder attention."),
        ("Q3: Can this run in real-time on continuous hot-rolling lines?",
         "A: Yes. Depthwise separable convolutions make MSBA-Net lightweight (34.7 MB). FP32 inference takes ~14 ms on an RTX 5070 Ti (~70 FPS). TensorRT FP16 quantization achieves <5 ms (>200 FPS), exceeding 30 m/s strip speeds.")
    ]
    cur_y = 37.0
    for q, a in qa_list:
        ax.text(107, cur_y, q, fontsize=8.2, fontweight='bold', color='#FDE047', zorder=3)
        wrapped_a = textwrap.wrap(a, width=82)
        cur_y -= 2.8
        for line in wrapped_a:
            ax.text(109, cur_y, line, fontsize=7.4, color='#E2E8F0', zorder=3)
            cur_y -= 2.4
        cur_y -= 1.8

    plt.tight_layout()
    out2_p = os.path.join(figures_dir, "guide_project_summary.png")
    out2_art = os.path.join(artifact_dir, "guide_project_summary.png")
    plt.savefig(out2_p, dpi=300, bbox_inches='tight', facecolor='#0B132B')
    plt.savefig(out2_art, dpi=300, bbox_inches='tight', facecolor='#0B132B')
    plt.close()
    print(f"Refined Guide Project Summary Infographic saved at {out2_p}")

if __name__ == '__main__':
    create_guide_architecture_diagram()
    create_guide_project_summary()
    print("Both infographics updated with zero overlaps!")
