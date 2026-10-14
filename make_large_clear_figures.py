import os
import sys
import torch
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

# Set publication style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'

base_dir = r"d:\scratch\3rs sem"
figures_dir = os.path.join(base_dir, "figures")
os.makedirs(figures_dir, exist_ok=True)

# ----------------------------------------------------------------------
# 1. REDESIGNED FIGURE 1: Wide, Big, Bold, Edge-to-Edge Architecture
# ----------------------------------------------------------------------
def generate_fig1():
    fig = plt.figure(figsize=(16.5, 5.0), dpi=300)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 165)
    ax.set_ylim(0, 50)
    ax.axis('off')

    # Color Palette
    c_input = '#334155'    # Slate
    c_enc = '#1D4ED8'      # Royal Blue
    c_bottle = '#0F172A'   # Midnight Navy
    c_dec = '#D97706'      # Amber/Gold
    c_bound = '#DC2626'    # Crimson
    c_gate = '#7C3AED'     # Violet/Purple
    c_out = '#047857'      # Forest Green
    c_msfp_card = '#F1F5F9' # Very light slate

    def draw_card(x, y, w, h, bg, title, sub="", dims="", rad=1.2, tc='white'):
        p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.15,rounding_size={rad}",
                           facecolor=bg, edgecolor='#1E293B', linewidth=1.4, alpha=0.97, zorder=3)
        ax.add_patch(p)
        cy = y + h / 2.0
        if sub and dims:
            ax.text(x + w/2, cy + h*0.23, title, ha='center', va='center', fontsize=10.0, fontweight='bold', color=tc, zorder=4)
            ax.text(x + w/2, cy, sub, ha='center', va='center', fontsize=8.5, color=tc, zorder=4)
            ax.text(x + w/2, cy - h*0.25, dims, ha='center', va='center', fontsize=8.0, fontstyle='italic', color=tc, zorder=4)
        elif sub:
            ax.text(x + w/2, cy + h*0.18, title, ha='center', va='center', fontsize=10.0, fontweight='bold', color=tc, zorder=4)
            ax.text(x + w/2, cy - h*0.20, sub, ha='center', va='center', fontsize=8.5, color=tc, zorder=4)
        else:
            ax.text(x + w/2, cy, title, ha='center', va='center', fontsize=10.0, fontweight='bold', color=tc, zorder=4)

    def draw_arrow(x1, y1, x2, y2, color='#1E293B', lw=1.8, style='->', rad=0.0):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                    connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2), zorder=2)

    # --- TOP PIPELINE (Y: 20 to 35) ---
    # Input
    draw_card(2, 22, 13, 14, c_input, "Input Image", "Steel Surface", "1 x 256 x 256")

    # Encoder Stages
    draw_card(18, 22, 15, 14, c_enc, "Encoder 1", "+ MSFP-1", "32 x 256 x 256")
    draw_card(36, 20, 15, 14, c_enc, "Encoder 2", "+ MSFP-2", "64 x 128 x 128")
    draw_card(54, 18, 15, 14, c_enc, "Encoder 3", "+ MSFP-3", "128 x 64 x 64")

    # Bottleneck
    draw_card(72, 16, 16, 14, c_bottle, "Bottleneck", "Dilated Context", "256 x 32 x 32")

    # Decoder Stages
    draw_card(92, 18, 15, 14, c_dec, "Decoder Up3", "Concat + Conv", "128 x 64 x 64")
    draw_card(110, 20, 15, 14, c_dec, "Decoder Up2", "Concat + Conv", "64 x 128 x 128")

    # BGFF Gate
    draw_card(128, 20, 16, 14, c_gate, "BGFF Gate", "Spatial Attention", "64 x 128 x 128")

    # Output
    draw_card(148, 20, 15, 14, c_out, "Output Mask", "Defect Prediction", "1 x 256 x 256")

    # Arrows for Main Flow
    draw_arrow(15, 29, 18, 29)
    draw_arrow(33, 29, 36, 27, rad=-0.04)
    draw_arrow(51, 27, 54, 25, rad=-0.04)
    draw_arrow(69, 25, 72, 23, rad=-0.04)
    draw_arrow(88, 23, 92, 25, rad=-0.04)
    draw_arrow(107, 25, 110, 27, rad=-0.04)
    draw_arrow(125, 27, 128, 27)
    draw_arrow(144, 27, 148, 27)

    # Skip Connections
    draw_arrow(69, 27, 92, 27, color='#059669', lw=2.0, rad=0.18) # Enc3 -> Up3
    draw_arrow(51, 31, 110, 31, color='#059669', lw=2.0, rad=0.16) # Enc2 -> Up2
    ax.text(80, 32.5, "High-Res Skip Concat", ha='center', fontsize=7.5, fontweight='bold', color='#065F46')

    # --- AUXILIARY BOUNDARY-AWARE STREAM (BAS) & SUPERVISION (Y: 37 to 48) ---
    draw_card(36, 38, 23, 9, c_bound, "Boundary-Aware Stream", "High-Pass Filter + Conv", "64 ch, Up-Conv")
    draw_card(64, 38, 20, 9, c_bound, "Boundary Head", "Contour Prediction", "1 x 256 x 256")

    # Connections into BAS
    draw_arrow(25, 36, 36, 42, color='#DC2626', lw=1.6, rad=0.10) # from Enc1
    draw_arrow(43, 34, 43, 38, color='#DC2626', lw=1.6) # from Enc2
    draw_arrow(59, 42.5, 64, 42.5, color='#DC2626', lw=1.6) # BAS to Head

    # Boundary Feature guidance to BGFF Gate
    draw_arrow(84, 42.5, 136, 34, color='#7C3AED', lw=2.2, rad=-0.12)
    ax.text(110, 41.5, "Boundary Prior Guidance Map", ha='center', fontsize=8.0, fontweight='bold', color='#6D28D9')

    # Composite Loss Box
    loss_box = FancyBboxPatch((98, 38), 65, 9, boxstyle="round,pad=0.15,rounding_size=1.0",
                              facecolor='#FEF2F2', edgecolor='#DC2626', linewidth=1.4, zorder=3)
    ax.add_patch(loss_box)
    ax.text(130.5, 44.5, "Deep Composite Loss Supervision", ha='center', va='center',
            fontsize=9.0, fontweight='bold', color='#991B1B', zorder=4)
    ax.text(130.5, 40.5, r"$\mathcal{L}_{total} = 0.4\mathcal{L}_{BCE} + 0.6\mathcal{L}_{Dice} + 0.3\mathcal{L}_{Focal} + 0.5\mathcal{L}_{Boundary}$",
            ha='center', va='center', fontsize=8.5, color='#991B1B', zorder=4)
    draw_arrow(155, 34, 155, 38, color='#DC2626', lw=1.4, style='<->')
    draw_arrow(74, 47, 98, 45, color='#DC2626', lw=1.4, rad=-0.08)

    # --- INSET: MULTI-SCALE FEATURE PRESERVATION (MSFP) BLOCK (Y: 1.5 to 14.5) ---
    msfp_card = FancyBboxPatch((18, 1.5), 145, 13.5, boxstyle="round,pad=0.2,rounding_size=1.2",
                               facecolor=c_msfp_card, edgecolor='#64748B', linewidth=1.4, linestyle='--', zorder=1)
    ax.add_patch(msfp_card)
    ax.text(20, 13.2, "Detailed Architecture of Multi-Scale Feature Preservation (MSFP) Block",
            fontsize=9.5, fontweight='bold', color='#0F172A')

    # Inside MSFP
    draw_card(20, 3.5, 12, 7.5, '#475569', "Input F_in", "C x H x W", rad=0.8)
    draw_card(36, 8.0, 19, 4.5, '#047857', "Branch 1: 1x1 Conv", "Ch: C/4", rad=0.6)
    draw_card(36, 2.5, 19, 4.5, '#059669', "Branch 2: 3x3 DConv", "r = 1 (Local)", rad=0.6)
    draw_card(58, 8.0, 19, 4.5, '#0D9488', "Branch 3: 3x3 DConv", "r = 2 (Medium)", rad=0.6)
    draw_card(58, 2.5, 19, 4.5, '#0284C7', "Branch 4: 3x3 DConv", "r = 4 (Global)", rad=0.6)

    draw_card(80, 3.5, 20, 7.5, '#1E293B', "Concat + 1x1 Conv", "C/4 x 4 -> C", rad=0.8)

    # Add circle
    circle = patches.Circle((105, 7.25), 2.2, facecolor='#FEF08A', edgecolor='#CA8A04', linewidth=1.5, zorder=4)
    ax.add_patch(circle)
    ax.text(105, 7.25, "+", ha='center', va='center', fontsize=13, fontweight='bold', color='#854D0E', zorder=5)

    draw_card(112, 3.5, 14, 7.5, '#0F766E', "Output F_out", "Residual Sum", rad=0.8)

    # Arrows inside MSFP
    draw_arrow(32, 7.25, 36, 10.2, color='#047857', lw=1.2)
    draw_arrow(32, 7.25, 36, 4.7, color='#059669', lw=1.2)
    draw_arrow(32, 7.25, 58, 10.2, color='#0D9488', lw=1.2, rad=0.08)
    draw_arrow(32, 7.25, 58, 4.7, color='#0284C7', lw=1.2, rad=-0.08)

    draw_arrow(55, 10.2, 80, 8.0, color='#047857', lw=1.2)
    draw_arrow(55, 4.7, 80, 6.5, color='#059669', lw=1.2)
    draw_arrow(77, 10.2, 80, 8.0, color='#0D9488', lw=1.2)
    draw_arrow(77, 4.7, 80, 6.5, color='#0284C7', lw=1.2)

    draw_arrow(100, 7.25, 102.8, 7.25, color='#1E293B', lw=1.4)
    # Residual bypass
    draw_arrow(26, 11.0, 105, 9.45, color='#B45309', lw=1.5, rad=0.12)
    ax.text(65, 13.0, "Identity Shortcut Connection", ha='center', fontsize=7.5, fontstyle='italic', color='#92400E')
    draw_arrow(107.2, 7.25, 112, 7.25, color='#1E293B', lw=1.4)

    # Callout text on right of MSFP
    callout_box = FancyBboxPatch((129, 3.0), 32, 8.5, boxstyle="round,pad=0.15,rounding_size=0.8",
                                  facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=1.2, zorder=2)
    ax.add_patch(callout_box)
    ax.text(145, 9.2, "Multi-Scale Preservation", ha='center', fontsize=8.5, fontweight='bold', color='#1D4ED8')
    ax.text(145, 6.8, "Captures micro-cracks (<2px) &", ha='center', fontsize=7.8, color='#1E293B')
    ax.text(145, 4.8, "diffuse low-contrast patches", ha='center', fontsize=7.8, color='#1E293B')

    plt.tight_layout()
    out_fig1 = os.path.join(figures_dir, "fig1_architecture.png")
    plt.savefig(out_fig1, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Generated large clear Figure 1: {out_fig1}")


# ----------------------------------------------------------------------
# 2. REDESIGNED FIGURE 2: Panoramic Defect-Centered Qualitative Grid
# ----------------------------------------------------------------------
def generate_fig2():
    sys.path.insert(0, base_dir)
    from dataset import IndustrialDefectDataset
    from models import UNet, UNetPlusPlus, MSBANet

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    models_dir = os.path.join(base_dir, "models")

    unet = UNet(in_channels=1, num_classes=1).to(device)
    unet.load_state_dict(torch.load(os.path.join(models_dir, "best_UNet.pth"), map_location=device))
    unet.eval()

    unetpp = UNetPlusPlus(in_channels=1, num_classes=1).to(device)
    unetpp.load_state_dict(torch.load(os.path.join(models_dir, "best_UNetPlusPlus.pth"), map_location=device))
    unetpp.eval()

    msbanet = MSBANet(in_channels=1, num_classes=1).to(device)
    msbanet.load_state_dict(torch.load(os.path.join(models_dir, "best_MSBANet.pth"), map_location=device))
    msbanet.eval()

    ds = IndustrialDefectDataset(num_samples=100, mode='val', condition='normal', seed=2026)

    def calc_iou(p, g):
        inter = np.logical_and(p, g).sum()
        uni = np.logical_or(p, g).sum()
        return (inter / uni * 100) if uni > 0 else 100.0

    # 4 diverse defects with tightly-tuned widescreen crops centered on the defects
    # (sample_idx, row_title, (y_min, y_max), (x_min, x_max))
    samples_config = [
        (2, "Crazing Cracks\n(Hairline fracture)", (72, 142), (32, 118)),
        (5, "Non-Metallic Inclusions\n(Dispersed slag)", (52, 108), (110, 225)),
        (8, "Low-Contrast Patch\n(Diffuse surface sheen)", (138, 208), (125, 220)),
        (14, "Pitted Surface\n(Localized craters)", (32, 102), (40, 126)),
    ]

    # Overall figure: 15.5 inches wide, 5.8 inches tall (aspect ratio ~2.67:1)
    fig, axes = plt.subplots(4, 5, figsize=(15.5, 5.8), dpi=300,
                             gridspec_kw={'wspace': 0.05, 'hspace': 0.08, 'left': 0.12, 'right': 0.99, 'top': 0.92, 'bottom': 0.02})

    col_titles = [
        "(a) Raw Steel Surface",
        "(b) Ground Truth Defect",
        "(c) U-Net Baseline [MICCAI'15]",
        "(d) U-Net++ [IEEE TMI'18]",
        "(e) MSBA-Net [Proposed]"
    ]

    for row_idx, (s_idx, row_label, (ymin, ymax), (xmin, xmax)) in enumerate(samples_config):
        item = ds[s_idx]
        img_t = item['image'].unsqueeze(0).to(device)
        raw_full = item['image'].squeeze().numpy()
        mask_full = item['mask'].squeeze().numpy() > 0.5

        with torch.no_grad():
            pu = unet(img_t)
            if isinstance(pu, tuple): pu = pu[0]
            out_u_full = torch.sigmoid(pu).squeeze().cpu().numpy() > 0.5

            pupp = unetpp(img_t)
            if isinstance(pupp, tuple): pupp = pupp[0]
            out_upp_full = torch.sigmoid(pupp).squeeze().cpu().numpy() > 0.5

            pm = msbanet(img_t)
            if isinstance(pm, tuple): pm = pm[0]
            out_m_full = torch.sigmoid(pm).squeeze().cpu().numpy() > 0.5

        iou_u = calc_iou(out_u_full, mask_full)
        iou_upp = calc_iou(out_upp_full, mask_full)
        iou_m = calc_iou(out_m_full, mask_full)

        # Crop to zoom defect by 3x
        raw_crop = raw_full[ymin:ymax, xmin:xmax]
        mask_crop = mask_full[ymin:ymax, xmin:xmax]
        u_crop = out_u_full[ymin:ymax, xmin:xmax]
        upp_crop = out_upp_full[ymin:ymax, xmin:xmax]
        m_crop = out_m_full[ymin:ymax, xmin:xmax]

        # Colors:
        # Col 0: Raw
        axes[row_idx, 0].imshow(raw_crop, cmap='gray', vmin=0, vmax=1, aspect='auto')
        axes[row_idx, 0].set_ylabel(row_label, fontsize=9.0, fontweight='bold', color='#0F172A', labelpad=8)

        # Col 1: Ground Truth (Gold/Amber mask)
        axes[row_idx, 1].imshow(raw_crop, cmap='gray', vmin=0, vmax=1, aspect='auto')
        axes[row_idx, 1].imshow(np.ma.masked_where(~mask_crop, mask_crop), cmap='Wistia', alpha=0.85, aspect='auto')

        # Col 2: U-Net (Crimson mask + badge)
        axes[row_idx, 2].imshow(raw_crop, cmap='gray', vmin=0, vmax=1, aspect='auto')
        axes[row_idx, 2].imshow(np.ma.masked_where(~u_crop, u_crop), cmap='autumn', alpha=0.80, aspect='auto')
        # IoU badge
        axes[row_idx, 2].text(0.96, 0.08, f"IoU: {iou_u:.1f}%", transform=axes[row_idx, 2].transAxes,
                              ha='right', va='bottom', fontsize=8.0, fontweight='bold', color='white',
                              bbox=dict(boxstyle="round,pad=0.25", facecolor='#DC2626', edgecolor='none', alpha=0.92))

        # Col 3: U-Net++ (Coral/Blue mask + badge)
        axes[row_idx, 3].imshow(raw_crop, cmap='gray', vmin=0, vmax=1, aspect='auto')
        axes[row_idx, 3].imshow(np.ma.masked_where(~upp_crop, upp_crop), cmap='cool', alpha=0.80, aspect='auto')
        axes[row_idx, 3].text(0.96, 0.08, f"IoU: {iou_upp:.1f}%", transform=axes[row_idx, 3].transAxes,
                              ha='right', va='bottom', fontsize=8.0, fontweight='bold', color='white',
                              bbox=dict(boxstyle="round,pad=0.25", facecolor='#2563EB', edgecolor='none', alpha=0.92))

        # Col 4: MSBA-Net (Emerald Green mask + badge)
        axes[row_idx, 4].imshow(raw_crop, cmap='gray', vmin=0, vmax=1, aspect='auto')
        axes[row_idx, 4].imshow(np.ma.masked_where(~m_crop, m_crop), cmap='summer', alpha=0.85, aspect='auto')
        axes[row_idx, 4].text(0.96, 0.08, f"IoU: {iou_m:.1f}%", transform=axes[row_idx, 4].transAxes,
                              ha='right', va='bottom', fontsize=8.5, fontweight='bold', color='white',
                              bbox=dict(boxstyle="round,pad=0.25", facecolor='#059669', edgecolor='#A7F3D0', linewidth=1.0, alpha=0.95))

        for c in range(5):
            axes[row_idx, c].set_xticks([])
            axes[row_idx, c].set_yticks([])
            for spine in axes[row_idx, c].spines.values():
                spine.set_color('#94A3B8')
                spine.set_linewidth(1.2)

    for c, title in enumerate(col_titles):
        col_color = '#047857' if c == 4 else '#0F172A'
        axes[0, c].set_title(title, fontsize=10.5, fontweight='bold', color=col_color, pad=8)

    out_fig2 = os.path.join(figures_dir, "fig2_visual_comparison.png")
    plt.savefig(out_fig2, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Generated large clear Figure 2: {out_fig2}")

if __name__ == '__main__':
    generate_fig1()
    generate_fig2()
