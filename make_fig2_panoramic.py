import os, sys, torch, numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

base_dir = r"d:\scratch\3rs sem"
figures_dir = os.path.join(base_dir, "figures")
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

samples_config = [
    (2, "Crazing (Cr)", (76, 136), (8, 148)),
    (5, "Inclusions (In)", (50, 110), (100, 240)),
    (8, "Patches (Pa)", (142, 202), (85, 225)),
    (14, "Pitted Surface (PS)", (36, 96), (18, 158)),
]

# 16.5 x 5.0 inches -> Aspect ratio 3.30
fig, axes = plt.subplots(4, 5, figsize=(16.5, 5.0), dpi=300,
                         gridspec_kw={'wspace': 0.04, 'hspace': 0.10, 'left': 0.13, 'right': 0.99, 'top': 0.91, 'bottom': 0.03})

col_titles = [
    "(a) Raw Steel Surface",
    "(b) Ground Truth Defect",
    "(c) Stage-wise Baseline",
    "(d) Edge-Aware Baseline [2026]",
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

    raw_crop = raw_full[ymin:ymax, xmin:xmax]
    mask_crop = mask_full[ymin:ymax, xmin:xmax]
    u_crop = out_u_full[ymin:ymax, xmin:xmax]
    upp_crop = out_upp_full[ymin:ymax, xmin:xmax]
    m_crop = out_m_full[ymin:ymax, xmin:xmax]

    # Col 0: Raw
    axes[row_idx, 0].imshow(raw_crop, cmap='gray', vmin=0, vmax=1, aspect='auto')
    axes[row_idx, 0].set_ylabel(row_label, fontsize=9.5, fontweight='bold', color='#0F172A',
                                 rotation=0, ha='right', va='center', labelpad=12)

    # Col 1: Ground Truth
    axes[row_idx, 1].imshow(raw_crop, cmap='gray', vmin=0, vmax=1, aspect='auto')
    axes[row_idx, 1].imshow(np.ma.masked_where(~mask_crop, mask_crop), cmap='Wistia', alpha=0.85, aspect='auto')

    # Col 2: U-Net
    axes[row_idx, 2].imshow(raw_crop, cmap='gray', vmin=0, vmax=1, aspect='auto')
    axes[row_idx, 2].imshow(np.ma.masked_where(~u_crop, u_crop), cmap='autumn', alpha=0.80, aspect='auto')
    axes[row_idx, 2].text(0.96, 0.08, f"IoU: {iou_u:.1f}%", transform=axes[row_idx, 2].transAxes,
                          ha='right', va='bottom', fontsize=8.2, fontweight='bold', color='white',
                          bbox=dict(boxstyle="round,pad=0.25", facecolor='#DC2626', edgecolor='none', alpha=0.92))

    # Col 3: U-Net++
    axes[row_idx, 3].imshow(raw_crop, cmap='gray', vmin=0, vmax=1, aspect='auto')
    axes[row_idx, 3].imshow(np.ma.masked_where(~upp_crop, upp_crop), cmap='cool', alpha=0.80, aspect='auto')
    axes[row_idx, 3].text(0.96, 0.08, f"IoU: {iou_upp:.1f}%", transform=axes[row_idx, 3].transAxes,
                          ha='right', va='bottom', fontsize=8.2, fontweight='bold', color='white',
                          bbox=dict(boxstyle="round,pad=0.25", facecolor='#2563EB', edgecolor='none', alpha=0.92))

    # Col 4: MSBA-Net
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
print(f"Generated widescreen Figure 2: {out_fig2}")
