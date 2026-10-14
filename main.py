import os
import json
import time
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from dataset import IndustrialDefectDataset
from models import UNet, UNetPlusPlus, MSBANet
from losses import CompositeLoss, calculate_metrics

def set_seed(seed=42):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def train_epoch(model, dataloader, optimizer, criterion, device, is_msba=False):
    model.train()
    total_loss = 0.0
    metrics_acc = {'iou': 0.0, 'dice': 0.0, 'precision': 0.0, 'recall': 0.0, 'accuracy': 0.0}
    
    for batch in dataloader:
        images = batch['image'].to(device)
        masks = batch['mask'].to(device)
        boundaries = batch['boundary'].to(device)
        
        optimizer.zero_grad()
        pred_mask, pred_boundary = model(images)
        
        if is_msba:
            loss = criterion(pred_mask, masks, pred_boundary, boundaries)
        else:
            loss = criterion(pred_mask, masks)
            
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        batch_m = calculate_metrics(pred_mask, masks)
        for k in metrics_acc:
            metrics_acc[k] += batch_m[k]
            
    n = len(dataloader)
    return total_loss / n, {k: v / n for k, v in metrics_acc.items()}

@torch.no_grad()
def evaluate(model, dataloader, criterion, device, is_msba=False):
    model.eval()
    total_loss = 0.0
    metrics_acc = {'iou': 0.0, 'dice': 0.0, 'precision': 0.0, 'recall': 0.0, 'accuracy': 0.0}
    
    for batch in dataloader:
        images = batch['image'].to(device)
        masks = batch['mask'].to(device)
        boundaries = batch['boundary'].to(device)
        
        pred_mask, pred_boundary = model(images)
        if is_msba:
            loss = criterion(pred_mask, masks, pred_boundary, boundaries)
        else:
            loss = criterion(pred_mask, masks)
            
        total_loss += loss.item()
        batch_m = calculate_metrics(pred_mask, masks)
        for k in metrics_acc:
            metrics_acc[k] += batch_m[k]
            
    n = len(dataloader)
    return total_loss / n, {k: v / n for k, v in metrics_acc.items()}

def plot_architecture_diagram(save_path):
    """Generates clean publication-ready Figure 1 architectural schematic."""
    fig, ax = plt.subplots(figsize=(12, 4.2), dpi=300)
    ax.axis('off')
    
    # Title
    ax.text(0.5, 0.95, "MSBA-Net: Multi-Scale Feature Enhancement & Boundary-Aware Dual-Head Architecture",
            ha='center', va='top', fontsize=11, fontweight='bold', family='serif')
    
    # Colors
    c_enc = '#2b5c8f'
    c_msfp = '#2e8b57'
    c_dec = '#8b4513'
    c_bound = '#b22222'
    c_fuse = '#4b0082'
    
    # Box helper
    def draw_box(x, y, w, h, text, color, text_color='white', fontsize=8):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03",
                                      facecolor=color, edgecolor='black', linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center',
                fontsize=fontsize, color=text_color, fontweight='bold', family='serif', multialignment='center')

    # Input
    draw_box(0.02, 0.40, 0.10, 0.25, "Input Image\n(1 x 256 x 256)\nSteel Sheet", '#555555')
    
    # Encoder stages
    draw_box(0.16, 0.55, 0.12, 0.22, "Stage 1 Conv\n+ MSFP Block 1\n(32 ch, 256x256)", c_enc)
    draw_box(0.31, 0.45, 0.12, 0.22, "Stage 2 Conv\n+ MSFP Block 2\n(64 ch, 128x128)", c_enc)
    draw_box(0.46, 0.35, 0.12, 0.22, "Stage 3 Conv\n+ MSFP Block 3\n(128 ch, 64x64)", c_enc)
    draw_box(0.61, 0.25, 0.12, 0.22, "Bottleneck\n(256 ch, 32x32)", '#1c3144')
    
    # Auxiliary Boundary Head
    draw_box(0.35, 0.12, 0.18, 0.18, "Boundary Stream\nAuxiliary Conv\n(64 ch -> 32 ch)", c_bound)
    draw_box(0.57, 0.08, 0.14, 0.15, "Boundary Head\nLoss: L_bound\n(Edge Contour)", '#d9534f')
    
    # Decoder stages
    draw_box(0.76, 0.35, 0.11, 0.20, "Decoder Up3\n(128 ch, 64x64)", c_dec)
    draw_box(0.76, 0.60, 0.11, 0.20, "Decoder Up2\n(64 ch, 128x128)", c_dec)
    
    # Fusion gate
    draw_box(0.74, 0.08, 0.13, 0.18, "Boundary-Guided\nSpatial Gate\n(BGFF Module)", c_fuse)
    
    # Final segmentation
    draw_box(0.89, 0.45, 0.10, 0.25, "Output Mask\nDefect Mask\n(1 x 256 x 256)", '#1b7a43')
    
    # Arrows
    arrow_kw = dict(arrowstyle="->", lw=1.5, color='black')
    ax.annotate("", xy=(0.16, 0.62), xytext=(0.12, 0.52), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.31, 0.56), xytext=(0.28, 0.62), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.46, 0.46), xytext=(0.43, 0.52), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.61, 0.36), xytext=(0.58, 0.42), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.76, 0.40), xytext=(0.73, 0.36), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.81, 0.60), xytext=(0.81, 0.55), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.89, 0.57), xytext=(0.87, 0.65), arrowprops=arrow_kw)
    
    # Boundary branch arrows
    ax.annotate("", xy=(0.35, 0.21), xytext=(0.22, 0.55), arrowprops=dict(arrowstyle="->", lw=1.2, color=c_bound, linestyle='--'))
    ax.annotate("", xy=(0.57, 0.15), xytext=(0.53, 0.18), arrowprops=dict(arrowstyle="->", lw=1.2, color=c_bound))
    ax.annotate("", xy=(0.74, 0.15), xytext=(0.71, 0.15), arrowprops=dict(arrowstyle="->", lw=1.2, color=c_fuse))
    ax.annotate("", xy=(0.80, 0.60), xytext=(0.80, 0.26), arrowprops=dict(arrowstyle="->", lw=1.2, color=c_fuse, linestyle='--'))
    
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved {save_path}")

def plot_visual_comparisons(models, test_loader, device, save_path):
    """Generates Figure 2: Visual segmentation comparison across 4 difficult defect cases."""
    for m in models.values():
        m.eval()
        
    batch = next(iter(test_loader))
    images = batch['image'].to(device)
    masks = batch['mask'].to(device)
    
    num_samples = 4
    fig, axes = plt.subplots(num_samples, 5, figsize=(10, 8.2), dpi=300)
    
    cols = ['Input Steel Image', 'Ground Truth', 'U-Net Baseline', 'U-Net++', 'Proposed MSBA-Net']
    for j, col_name in enumerate(cols):
        axes[0, j].set_title(col_name, fontsize=10, fontweight='bold', family='serif')
        
    for i in range(num_samples):
        img_np = images[i, 0].cpu().numpy()
        gt_np = masks[i, 0].cpu().numpy()
        
        with torch.no_grad():
            p_unet, _ = models['UNet'](images[i:i+1])
            p_unetpp, _ = models['UNetPlusPlus'](images[i:i+1])
            p_msba, _ = models['MSBANet'](images[i:i+1])
            
            p_unet_m = (torch.sigmoid(p_unet)[0, 0].cpu().numpy() > 0.5).astype(np.float32)
            p_unetpp_m = (torch.sigmoid(p_unetpp)[0, 0].cpu().numpy() > 0.5).astype(np.float32)
            p_msba_m = (torch.sigmoid(p_msba)[0, 0].cpu().numpy() > 0.5).astype(np.float32)
            
        axes[i, 0].imshow(img_np, cmap='gray')
        axes[i, 1].imshow(gt_np, cmap='inferno')
        axes[i, 2].imshow(p_unet_m, cmap='inferno')
        axes[i, 3].imshow(p_unetpp_m, cmap='inferno')
        axes[i, 4].imshow(p_msba_m, cmap='inferno')
        
        for j in range(5):
            axes[i, j].axis('off')
            
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved {save_path}")

def plot_loss_curves(loss_history, save_path):
    """Generates Figure 3: Training & Validation Loss curves."""
    fig, ax = plt.subplots(figsize=(6.5, 3.8), dpi=300)
    epochs = range(1, len(loss_history['UNet']['train']) + 1)
    
    ax.plot(epochs, loss_history['UNet']['val'], 'r--', lw=1.8, label='U-Net (Val)')
    ax.plot(epochs, loss_history['UNetPlusPlus']['val'], 'b-.', lw=1.8, label='U-Net++ (Val)')
    ax.plot(epochs, loss_history['MSBANet']['val'], 'g-', lw=2.2, label='MSBA-Net [Proposed] (Val)')
    
    ax.set_xlabel('Training Epochs', fontsize=10, family='serif')
    ax.set_ylabel('Composite Validation Loss', fontsize=10, family='serif')
    ax.set_title('Convergence Dynamics Across Segmentation Architectures', fontsize=10, fontweight='bold', family='serif')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(frameon=True, fontsize=9)
    
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved {save_path}")

def plot_degradation_benchmark(robustness_results, save_path):
    """Generates Figure 4: Condition degradation benchmark bar chart."""
    conditions = ['Normal', 'Low Contrast', 'Sensor Noise', 'Motion Blur', 'Tiny Defects']
    x = np.arange(len(conditions))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(7.2, 3.8), dpi=300)
    
    unet_ious = [robustness_results['UNet'][c.lower().replace(' ', '_')]['iou'] * 100 for c in conditions]
    unetpp_ious = [robustness_results['UNetPlusPlus'][c.lower().replace(' ', '_')]['iou'] * 100 for c in conditions]
    msba_ious = [robustness_results['MSBANet'][c.lower().replace(' ', '_')]['iou'] * 100 for c in conditions]
    
    ax.bar(x - width, unet_ious, width, label='U-Net Baseline', color='#d9534f', edgecolor='black')
    ax.bar(x, unetpp_ious, width, label='U-Net++', color='#337ab7', edgecolor='black')
    ax.bar(x + width, msba_ious, width, label='MSBA-Net [Proposed]', color='#5cb85c', edgecolor='black')
    
    ax.set_ylabel('mIoU Score (%)', fontsize=10, family='serif')
    ax.set_title('Segmentation Robustness Under Challenging Industrial Imaging Conditions', fontsize=10, fontweight='bold', family='serif')
    ax.set_xticks(x)
    ax.set_xticklabels(conditions, fontsize=9, family='serif')
    ax.set_ylim(40, 100)
    ax.grid(axis='y', linestyle=':', alpha=0.6)
    ax.legend(frameon=True, fontsize=9)
    
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved {save_path}")


def main():
    set_seed(42)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"=== Running on {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}) ===")
    
    # 1. Datasets and Loaders
    print("Initializing datasets...")
    train_ds = IndustrialDefectDataset(num_samples=700, mode='train', condition='normal')
    val_ds = IndustrialDefectDataset(num_samples=150, mode='val', condition='normal')
    
    train_loader = DataLoader(train_ds, batch_size=16, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=16, shuffle=False, num_workers=0)
    
    # 2. Setup Models
    models = {
        'UNet': UNet(in_channels=1, num_classes=1, base_ch=32).to(device),
        'UNetPlusPlus': UNetPlusPlus(in_channels=1, num_classes=1, base_ch=32).to(device),
        'MSBANet': MSBANet(in_channels=1, num_classes=1, base_ch=32).to(device)
    }
    
    criterion = CompositeLoss(lambda_dice=1.0, lambda_focal=0.5, lambda_boundary=0.4).to(device)
    
    loss_history = {name: {'train': [], 'val': []} for name in models}
    
    epochs = 12
    print(f"\nTraining all models for {epochs} epochs...")
    
    for name, model in models.items():
        print(f"\n--- Training {name} ---")
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
        best_val_iou = 0.0
        
        is_msba = (name == 'MSBANet')
        
        for epoch in range(1, epochs + 1):
            t0 = time.time()
            tr_loss, tr_m = train_epoch(model, train_loader, optimizer, criterion, device, is_msba)
            val_loss, val_m = evaluate(model, val_loader, criterion, device, is_msba)
            scheduler.step()
            dt = time.time() - t0
            
            loss_history[name]['train'].append(tr_loss)
            loss_history[name]['val'].append(val_loss)
            
            if val_m['iou'] > best_val_iou:
                best_val_iou = val_m['iou']
                torch.save(model.state_dict(), f"models/best_{name}.pth")
                
            print(f"Epoch [{epoch:02d}/{epochs:02d}] ({dt:.1f}s) - Loss: {tr_loss:.4f} | Val IoU: {val_m['iou']*100:.2f}% | Val Dice: {val_m['dice']*100:.2f}%")

    # Load best weights
    for name, model in models.items():
        model.load_state_dict(torch.load(f"models/best_{name}.pth"))
        model.eval()

    # 3. Robustness Stress Testing Across 5 Conditions
    conditions = ['normal', 'low_contrast', 'noise', 'blur', 'tiny_defects']
    robustness_results = {name: {} for name in models}
    
    print("\n=== Robustness Stress-Testing Under Challenging Factory Conditions ===")
    for cond in conditions:
        print(f"\nEvaluating Condition: [{cond.upper()}]")
        test_ds = IndustrialDefectDataset(num_samples=150, mode='val', condition=cond)
        test_loader = DataLoader(test_ds, batch_size=16, shuffle=False, num_workers=0)
        
        for name, model in models.items():
            is_msba = (name == 'MSBANet')
            _, metrics = evaluate(model, test_loader, criterion, device, is_msba)
            robustness_results[name][cond] = metrics
            print(f"  {name:15s} -> mIoU: {metrics['iou']*100:.2f}% | Dice: {metrics['dice']*100:.2f}% | Prec: {metrics['precision']*100:.2f}% | Rec: {metrics['recall']*100:.2f}%")

    # Save metrics JSON
    with open("results/benchmark_metrics.json", "w") as f:
        json.dump(robustness_results, f, indent=2)
    print("\nSaved results/benchmark_metrics.json")

    # 4. Generate Publication Figures
    print("\nGenerating Figures in figures/ ...")
    plot_architecture_diagram("figures/fig1_architecture.png")
    test_normal = IndustrialDefectDataset(num_samples=20, mode='val', condition='normal')
    test_loader_samples = DataLoader(test_normal, batch_size=4, shuffle=False)
    plot_visual_comparisons(models, test_loader_samples, device, "figures/fig2_visual_comparison.png")
    plot_loss_curves(loss_history, "figures/fig3_loss_curves.png")
    plot_degradation_benchmark(robustness_results, "figures/fig4_degraded_benchmark.png")
    
    print("\n=== ALL PIPELINE EXECUTION & PLOTTING COMPLETE! ===")

if __name__ == '__main__':
    main()
