import os
import sys
import torch
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import scipy.ndimage as ndimage

# Set publication font
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'

base_dir = r"d:\scratch\3rs sem"
figures_dir = os.path.join(base_dir, "figures")
os.makedirs(figures_dir, exist_ok=True)

# ----------------------------------------------------------------------
# 1. FIGURE 1: MASTER ARCHITECTURE DIAGRAM (Wide, Edge-to-Edge, Large Text)
# ----------------------------------------------------------------------
def generate_fig1():
    fig = plt.figure(figsize=(16.8, 5.0), dpi=300)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 168)
    ax.set_ylim(0, 50)
    ax.axis('off')

    # Color Palette
    c_input = '#334155'    # Slate
    c_enc = '#1D4ED8'      # Royal Blue
    c_bottle = '#0F172A'   # Midnight Navy
    c_dec = '#D97706'      # Amber/Gold
    c_bound = '#B91C1C'    # Deep Crimson
    c_gate = '#6D28D9'     # Violet/Purple
    c_out = '#047857'      # Forest Green
    c_msfp_card = '#F8FAFC' # Very light slate

    def draw_card(x, y, w, h, bg, title, sub="", dims="", rad=1.2, tc='white', title_fs=10.5, sub_fs=8.8, dims_fs=8.2):
        p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.15,rounding_size={rad}",
                           facecolor=bg, edgecolor='#1E293B', linewidth=1.4, alpha=0.97, zorder=3)
        ax.add_patch(p)
        cy = y + h / 2.0
        if sub and dims:
            ax.text(x + w/2, cy + h*0.23, title, ha='center', va='center', fontsize=title_fs, fontweight='bold', color=tc, zorder=4)
            ax.text(x + w/2, cy, sub, ha='center', va='center', fontsize=sub_fs, color=tc, zorder=4)
            ax.text(x + w/2, cy - h*0.25, dims, ha='center', va='center', fontsize=dims_fs, fontstyle='italic', color=tc, zorder=4)
        elif sub:
            ax.text(x + w/2, cy + h*0.18, title, ha='center', va='center', fontsize=title_fs, fontweight='bold', color=tc, zorder=4)
            ax.text(x + w/2, cy - h*0.20, sub, ha='center', va='center', fontsize=sub_fs, color=tc, zorder=4)
        else:
            ax.text(x + w/2, cy, title, ha='center', va='center', fontsize=title_fs, fontweight='bold', color=tc, zorder=4)

    def draw_arrow(x1, y1, x2, y2, color='#1E293B', lw=1.8, style='->', rad=0.0):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                    connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2), zorder=2)

    # --- TOP PIPELINE (Y: 20 to 35) ---
    # Input
    draw_card(1, 21, 13.5, 14.5, c_input, "Input Image", "Steel Surface", "1 x 256 x 256")

    # Encoder Stages
    draw_card(17, 21, 15.5, 14.5, c_enc, "Encoder 1", "+ MSFP-1", "32 x 256 x 256")
    draw_card(35, 19, 15.5, 14.5, c_enc, "Encoder 2", "+ MSFP-2", "64 x 128 x 128")
    draw_card(53, 17, 15.5, 14.5, c_enc, "Encoder 3", "+ MSFP-3", "128 x 64 x 64")

    # Bottleneck
    draw_card(71.5, 15, 17, 14.5, c_bottle, "Bottleneck", "Dilated Context", "256 x 32 x 32")

    # Decoder Stages
    draw_card(92, 17, 15.5, 14.5, c_dec, "Decoder Up3", "Concat + Conv", "128 x 64 x 64")
    draw_card(110.5, 19, 15.5, 14.5, c_dec, "Decoder Up2", "Concat + Conv", "64 x 128 x 128")

    # BGFF Gate
    draw_card(129, 19, 16.5, 14.5, c_gate, "BGFF Gate", "Spatial Attention", "64 x 128 x 128")

    # Output
    draw_card(149, 19, 17.5, 14.5, c_out, "Output Mask", "Defect Prediction", "1 x 256 x 256")

    # Arrows for Main Flow
    draw_arrow(14.5, 28, 17, 28)
    draw_arrow(32.5, 28, 35, 26, rad=-0.04)
    draw_arrow(50.5, 26, 53, 24, rad=-0.04)
    draw_arrow(68.5, 24, 71.5, 22, rad=-0.04)
    draw_arrow(88.5, 22, 92, 24, rad=-0.04)
    draw_arrow(107.5, 24, 110.5, 26, rad=-0.04)
    draw_arrow(126, 26, 129, 26)
    draw_arrow(145.5, 26, 149, 26)

    # Skip Connections
    draw_arrow(68.5, 26, 92, 26, color='#059669', lw=2.2, rad=0.18) # Enc3 -> Up3
    draw_arrow(50.5, 30.5, 110.5, 30.5, color='#059669', lw=2.2, rad=0.16) # Enc2 -> Up2
    ax.text(80, 32.5, "High-Res Skip Concat", ha='center', fontsize=8.2, fontweight='bold', color='#065F46')

    # --- AUXILIARY BOUNDARY-AWARE STREAM (BAS) & SUPERVISION (Y: 37 to 48.5) ---
    draw_card(35, 38, 25, 9.5, c_bound, "Boundary-Aware Stream", "High-Pass Gradient Extr.", "64 ch, Up-Conv")
    draw_card(64, 38, 21, 9.5, c_bound, "Boundary Head", "Contour Prediction", "1 x 256 x 256")

    # Connections into BAS
    draw_arrow(24, 35.5, 35, 42.5, color='#DC2626', lw=1.8, rad=0.10) # from Enc1
    draw_arrow(42, 33.5, 42, 38, color='#DC2626', lw=1.8) # from Enc2
    draw_arrow(60, 42.5, 64, 42.5, color='#DC2626', lw=1.8) # BAS to Head

    # Boundary Feature guidance to BGFF Gate
    draw_arrow(85, 42.5, 137, 33.5, color='#7C3AED', lw=2.4, rad=-0.12)
    ax.text(111, 42.0, "Boundary Prior Guidance Map", ha='center', fontsize=8.8, fontweight='bold', color='#5B21B6')

    # Composite Loss Box
    loss_box = FancyBboxPatch((98, 38), 68.5, 9.5, boxstyle="round,pad=0.15,rounding_size=1.0",
                              facecolor='#FEF2F2', edgecolor='#DC2626', linewidth=1.5, zorder=3)
    ax.add_patch(loss_box)
    ax.text(132, 44.5, "Deep Composite Loss Supervision", ha='center', va='center',
            fontsize=9.8, fontweight='bold', color='#991B1B', zorder=4)
    ax.text(132, 40.5, r"$\mathcal{L}_{\mathrm{total}} = 0.4\mathcal{L}_{\mathrm{BCE}} + 0.6\mathcal{L}_{\mathrm{Dice}} + 0.3\mathcal{L}_{\mathrm{Focal}} + 0.5\mathcal{L}_{\mathrm{Boundary}}$",
            ha='center', va='center', fontsize=9.2, color='#991B1B', zorder=4)
    draw_arrow(157.5, 33.5, 157.5, 38, color='#DC2626', lw=1.6, style='<->')
    draw_arrow(74.5, 47.5, 98, 45, color='#DC2626', lw=1.6, rad=-0.08)

    # --- INSET: MULTI-SCALE FEATURE PRESERVATION (MSFP) BLOCK (Y: 1.0 to 14.5) ---
    msfp_card = FancyBboxPatch((17, 1.0), 149.5, 13.8, boxstyle="round,pad=0.2,rounding_size=1.2",
                               facecolor=c_msfp_card, edgecolor='#475569', linewidth=1.5, linestyle='--', zorder=1)
    ax.add_patch(msfp_card)
    ax.text(19, 13.2, "Detailed Structure of Multi-Scale Feature Preservation (MSFP) Block",
            fontsize=10.0, fontweight='bold', color='#0F172A')

    # Inside MSFP
    draw_card(19, 3.2, 13, 8.0, '#475569', "Input F_in", "C x H x W", rad=0.8, title_fs=9.5, sub_fs=8.2)
    draw_card(36, 7.8, 20, 4.8, '#047857', "Branch 1: 1x1 Conv", "Ch: C/4", rad=0.6, title_fs=9.2, sub_fs=7.8)
    draw_card(36, 2.2, 20, 4.8, '#059669', "Branch 2: 3x3 DConv", "r = 1 (Local)", rad=0.6, title_fs=9.2, sub_fs=7.8)
    draw_card(60, 7.8, 20, 4.8, '#0D9488', "Branch 3: 3x3 DConv", "r = 2 (Medium)", rad=0.6, title_fs=9.2, sub_fs=7.8)
    draw_card(60, 2.2, 20, 4.8, '#0284C7', "Branch 4: 3x3 DConv", "r = 4 (Global)", rad=0.6, title_fs=9.2, sub_fs=7.8)

    draw_card(84, 3.2, 21, 8.0, '#1E293B', "Concat + 1x1 Conv", "C/4 x 4 -> C", rad=0.8, title_fs=9.5, sub_fs=8.2)

    circle = patches.Circle((110, 7.2), 2.4, facecolor='#FEF08A', edgecolor='#CA8A04', linewidth=1.6, zorder=4)
    ax.add_patch(circle)
    ax.text(110, 7.2, "+", ha='center', va='center', fontsize=14, fontweight='bold', color='#854D0E', zorder=5)

    draw_card(117, 3.2, 15, 8.0, '#0F766E', "Output F_out", "Residual Sum", rad=0.8, title_fs=9.5, sub_fs=8.2)

    draw_arrow(32, 7.2, 36, 10.2, color='#047857', lw=1.3)
    draw_arrow(32, 7.2, 36, 4.6, color='#059669', lw=1.3)
    draw_arrow(32, 7.2, 60, 10.2, color='#0D9488', lw=1.3, rad=0.08)
    draw_arrow(32, 7.2, 60, 4.6, color='#0284C7', lw=1.3, rad=-0.08)

    draw_arrow(56, 10.2, 84, 8.0, color='#047857', lw=1.3)
    draw_arrow(56, 4.6, 84, 6.4, color='#059669', lw=1.3)
    draw_arrow(80, 10.2, 84, 8.0, color='#0D9488', lw=1.3)
    draw_arrow(80, 4.6, 84, 6.4, color='#0284C7', lw=1.3)

    draw_arrow(105, 7.2, 107.6, 7.2, color='#1E293B', lw=1.6)
    draw_arrow(25.5, 11.2, 110, 9.6, color='#B45309', lw=1.6, rad=0.12)
    ax.text(68, 13.0, "Identity Shortcut Connection", ha='center', fontsize=8.2, fontstyle='italic', color='#92400E')
    draw_arrow(112.4, 7.2, 117, 7.2, color='#1E293B', lw=1.6)

    callout_box = FancyBboxPatch((134, 2.5), 31, 9.2, boxstyle="round,pad=0.15,rounding_size=0.8",
                                  facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=1.3, zorder=2)
    ax.add_patch(callout_box)
    ax.text(149.5, 9.2, "Multi-Scale Preservation", ha='center', fontsize=9.2, fontweight='bold', color='#1D4ED8')
    ax.text(149.5, 6.7, "Captures micro-cracks (<2px) &", ha='center', fontsize=8.2, color='#1E293B')
    ax.text(149.5, 4.6, "diffuse low-contrast patches", ha='center', fontsize=8.2, color='#1E293B')

    plt.tight_layout()
    out_fig1 = os.path.join(figures_dir, "fig1_architecture.png")
    plt.savefig(out_fig1, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Generated Figure 1: {out_fig1}")


# ----------------------------------------------------------------------
# 2. FIGURE 2: MASTER QUALITATIVE COMPARISON WITH ACCURATE DYNAMIC CROPPING
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

    # 4 distinct morphological defect categories
    defect_rows = [
        (0, "Crazing Cracks", "(Dendritic micro-crack)"),
        (1, "Inclusion", "(Particulate oxide slag)"),
        (2, "Low-Contrast Patch", "(Diffuse surface mark)"),
        (3, "Pitted Surface", "(Clustered pinholes)"),
    ]

    fig, axes = plt.subplots(4, 5, figsize=(16.8, 5.0), dpi=300,
                             gridspec_kw={'wspace': 0.04, 'hspace': 0.09, 'left': 0.13, 'right': 0.99, 'top': 0.91, 'bottom': 0.02})

    col_titles = [
        "(a) Raw Steel Surface",
        "(b) Ground Truth Defect",
        "(c) U-Net Baseline [MICCAI'15]",
        "(d) U-Net++ [IEEE TMI'18]",
        "(e) MSBA-Net [Proposed]"
    ]

    for row_idx, (s_idx, r_title1, r_title2) in enumerate(defect_rows):
        item = ds[s_idx]
        img_t = item['image'].unsqueeze(0).to(device)
        raw_full = item['image'].squeeze().numpy()
        mask_full = item['mask'].squeeze().numpy() > 0.5

        with torch.no_grad():
            pu = unet(img_t); pu = pu[0] if isinstance(pu, tuple) else pu
            out_u_full = torch.sigmoid(pu).squeeze().cpu().numpy() > 0.5

            pupp = unetpp(img_t); pupp = pupp[0] if isinstance(pupp, tuple) else pupp
            out_upp_full = torch.sigmoid(pupp).squeeze().cpu().numpy() > 0.5

            pm = msbanet(img_t); pm = pm[0] if isinstance(pm, tuple) else pm
            out_m_full = torch.sigmoid(pm).squeeze().cpu().numpy() > 0.5

        iou_u = calc_iou(out_u_full, mask_full)
        iou_upp = calc_iou(out_upp_full, mask_full)
        iou_m = calc_iou(out_m_full, mask_full)

        # Dynamic defect-centered cropping
        ys, xs = np.where(mask_full)
        if len(ys) > 0:
            cy = int(np.mean(ys))
            cx = int(np.mean(xs))
        else:
            cy, cx = 128, 128

        # Each crop has height = 70, width = 145 (aspect ratio ~2.07:1)
        half_h, half_w = 35, 72
        ymin = max(0, min(256 - 70, cy - half_h))
        ymax = ymin + 70
        xmin = max(0, min(256 - 145, cx - half_w))
        xmax = xmin + 145

        raw_crop = raw_full[ymin:ymax, xmin:xmax]
        mask_crop = mask_full[ymin:ymax, xmin:xmax]
        u_crop = out_u_full[ymin:ymax, xmin:xmax]
        upp_crop = out_upp_full[ymin:ymax, xmin:xmax]
        m_crop = out_m_full[ymin:ymax, xmin:xmax]

        # Horizontal Row Title on Left
        axes[row_idx, 0].text(-0.06, 0.62, r_title1, transform=axes[row_idx, 0].transAxes,
                              ha='right', va='center', fontsize=9.6, fontweight='bold', color='#0F172A')
        axes[row_idx, 0].text(-0.06, 0.30, r_title2, transform=axes[row_idx, 0].transAxes,
                              ha='right', va='center', fontsize=8.0, fontstyle='italic', color='#475569')

        # Col 0: Raw
        axes[row_idx, 0].imshow(raw_crop, cmap='gray', vmin=0, vmax=1, aspect='auto')

        # Col 1: Ground Truth (Gold/Amber mask)
        axes[row_idx, 1].imshow(raw_crop, cmap='gray', vmin=0, vmax=1, aspect='auto')
        axes[row_idx, 1].imshow(np.ma.masked_where(~mask_crop, mask_crop), cmap='Wistia', alpha=0.85, aspect='auto')

        # Col 2: U-Net (Crimson mask + badge)
        axes[row_idx, 2].imshow(raw_crop, cmap='gray', vmin=0, vmax=1, aspect='auto')
        axes[row_idx, 2].imshow(np.ma.masked_where(~u_crop, u_crop), cmap='autumn', alpha=0.80, aspect='auto')
        axes[row_idx, 2].text(0.96, 0.08, f"IoU: {iou_u:.1f}%", transform=axes[row_idx, 2].transAxes,
                              ha='right', va='bottom', fontsize=8.2, fontweight='bold', color='white',
                              bbox=dict(boxstyle="round,pad=0.25", facecolor='#DC2626', edgecolor='none', alpha=0.92))

        # Col 3: U-Net++ (Coral/Blue mask + badge)
        axes[row_idx, 3].imshow(raw_crop, cmap='gray', vmin=0, vmax=1, aspect='auto')
        axes[row_idx, 3].imshow(np.ma.masked_where(~upp_crop, upp_crop), cmap='cool', alpha=0.80, aspect='auto')
        axes[row_idx, 3].text(0.96, 0.08, f"IoU: {iou_upp:.1f}%", transform=axes[row_idx, 3].transAxes,
                              ha='right', va='bottom', fontsize=8.2, fontweight='bold', color='white',
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
    print(f"Generated Figure 2: {out_fig2}")

if __name__ == '__main__':
    generate_fig1()
    generate_fig2()
