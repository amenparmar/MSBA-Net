import os
import sys
import json
import csv
import time
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader

sys.path.insert(0, r"d:\scratch\3rs sem")
from dataset import IndustrialDefectDataset
from models import ConvBlock, MultiScaleFeaturePreservation, BoundaryAwareFusion, UNet, MSBANet
from losses import CompositeLoss, calculate_metrics

# -------------------------------------------------------------------------
# Define Modular Ablation Architectures
# -------------------------------------------------------------------------
class UNet_MSFP(nn.Module):
    """Ablation Architecture 2: Baseline Backbone + MSFP Blocks in Encoder."""
    def __init__(self, in_channels=1, num_classes=1, base_ch=32):
        super().__init__()
        self.enc1 = ConvBlock(in_channels, base_ch)
        self.msfp1 = MultiScaleFeaturePreservation(base_ch)
        
        self.enc2 = ConvBlock(base_ch, base_ch * 2)
        self.msfp2 = MultiScaleFeaturePreservation(base_ch * 2)
        
        self.enc3 = ConvBlock(base_ch * 2, base_ch * 4)
        self.msfp3 = MultiScaleFeaturePreservation(base_ch * 4)
        
        self.enc4 = ConvBlock(base_ch * 4, base_ch * 8)
        self.msfp4 = MultiScaleFeaturePreservation(base_ch * 8)
        
        self.bottleneck = ConvBlock(base_ch * 8, base_ch * 16)
        
        self.up4 = nn.ConvTranspose2d(base_ch * 16, base_ch * 8, kernel_size=2, stride=2)
        self.dec4 = ConvBlock(base_ch * 16, base_ch * 8)
        
        self.up3 = nn.ConvTranspose2d(base_ch * 8, base_ch * 4, kernel_size=2, stride=2)
        self.dec3 = ConvBlock(base_ch * 8, base_ch * 4)
        
        self.up2 = nn.ConvTranspose2d(base_ch * 4, base_ch * 2, kernel_size=2, stride=2)
        self.dec2 = ConvBlock(base_ch * 4, base_ch * 2)
        
        self.up1 = nn.ConvTranspose2d(base_ch * 2, base_ch, kernel_size=2, stride=2)
        self.dec1 = ConvBlock(base_ch * 2, base_ch)
        
        self.out_conv = nn.Conv2d(base_ch, num_classes, kernel_size=1)
        
    def forward(self, x):
        e1 = self.msfp1(self.enc1(x))
        e2 = self.msfp2(self.enc2(F.max_pool2d(e1, 2)))
        e3 = self.msfp3(self.enc3(F.max_pool2d(e2, 2)))
        e4 = self.msfp4(self.enc4(F.max_pool2d(e3, 2)))
        
        b = self.bottleneck(F.max_pool2d(e4, 2))
        
        d4 = self.dec4(torch.cat([self.up4(b), e4], dim=1))
        d3 = self.dec3(torch.cat([self.up3(d4), e3], dim=1))
        d2 = self.dec2(torch.cat([self.up2(d3), e2], dim=1))
        d1 = self.dec1(torch.cat([self.up1(d2), e1], dim=1))
        
        out = self.out_conv(d1)
        return out, None


class MSBANet_NoBGFF(nn.Module):
    """Ablation Architecture 3: MSFP + BAS Stream, but without BGFF Spatial Attention Gate."""
    def __init__(self, in_channels=1, num_classes=1, base_ch=32):
        super().__init__()
        self.enc1 = ConvBlock(in_channels, base_ch)
        self.msfp1 = MultiScaleFeaturePreservation(base_ch)
        
        self.enc2 = ConvBlock(base_ch, base_ch * 2)
        self.msfp2 = MultiScaleFeaturePreservation(base_ch * 2)
        
        self.enc3 = ConvBlock(base_ch * 2, base_ch * 4)
        self.msfp3 = MultiScaleFeaturePreservation(base_ch * 4)
        
        self.enc4 = ConvBlock(base_ch * 4, base_ch * 8)
        self.msfp4 = MultiScaleFeaturePreservation(base_ch * 8)
        
        self.bottleneck = ConvBlock(base_ch * 8, base_ch * 16)
        
        # Auxiliary Boundary Stream
        self.b_up3 = nn.ConvTranspose2d(base_ch * 4, base_ch * 2, kernel_size=2, stride=2)
        self.b_conv3 = ConvBlock(base_ch * 4, base_ch * 2)
        self.b_up2 = nn.ConvTranspose2d(base_ch * 2, base_ch, kernel_size=2, stride=2)
        self.b_conv2 = ConvBlock(base_ch * 2, base_ch)
        self.b_head = nn.Conv2d(base_ch, 1, kernel_size=1)
        
        # Main Decoder
        self.up4 = nn.ConvTranspose2d(base_ch * 16, base_ch * 8, kernel_size=2, stride=2)
        self.dec4 = ConvBlock(base_ch * 16, base_ch * 8)
        
        self.up3 = nn.ConvTranspose2d(base_ch * 8, base_ch * 4, kernel_size=2, stride=2)
        self.dec3 = ConvBlock(base_ch * 8, base_ch * 4)
        
        self.up2 = nn.ConvTranspose2d(base_ch * 4, base_ch * 2, kernel_size=2, stride=2)
        self.dec2 = ConvBlock(base_ch * 4, base_ch * 2)
        
        self.up1 = nn.ConvTranspose2d(base_ch * 2, base_ch, kernel_size=2, stride=2)
        self.dec1 = ConvBlock(base_ch * 2, base_ch)
        
        # Output directly from d1 without bg_fusion
        self.seg_head = nn.Conv2d(base_ch, num_classes, kernel_size=1)
        
    def forward(self, x):
        e1 = self.msfp1(self.enc1(x))
        e2 = self.msfp2(self.enc2(F.max_pool2d(e1, 2)))
        e3 = self.msfp3(self.enc3(F.max_pool2d(e2, 2)))
        e4 = self.msfp4(self.enc4(F.max_pool2d(e3, 2)))
        
        b = self.bottleneck(F.max_pool2d(e4, 2))
        
        # BAS
        b_feat2 = self.b_conv3(torch.cat([self.b_up3(e3), e2], dim=1))
        b_feat1 = self.b_conv2(torch.cat([self.b_up2(b_feat2), e1], dim=1))
        pred_boundary = self.b_head(b_feat1)
        
        # Main Decoder
        d4 = self.dec4(torch.cat([self.up4(b), e4], dim=1))
        d3 = self.dec3(torch.cat([self.up3(d4), e3], dim=1))
        d2 = self.dec2(torch.cat([self.up2(d3), e2], dim=1))
        d1 = self.dec1(torch.cat([self.up1(d2), e1], dim=1))
        
        pred_mask = self.seg_head(d1)
        return pred_mask, pred_boundary


# -------------------------------------------------------------------------
# Training and Evaluation Helper Functions
# -------------------------------------------------------------------------
def set_seed(seed=42):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def train_one_model(model, train_loader, val_loader, criterion, device, epochs=12, has_boundary=False, save_path=None):
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    best_val_iou = 0.0
    
    for epoch in range(1, epochs + 1):
        model.train()
        for batch in train_loader:
            images = batch['image'].to(device)
            masks = batch['mask'].to(device)
            boundaries = batch['boundary'].to(device)
            
            optimizer.zero_grad()
            pred_mask, pred_boundary = model(images)
            
            if has_boundary and pred_boundary is not None:
                loss = criterion(pred_mask, masks, pred_boundary, boundaries)
            else:
                loss = criterion(pred_mask, masks)
                
            loss.backward()
            optimizer.step()
        scheduler.step()
        
        # Validation
        model.eval()
        total_iou = 0.0
        n_batches = 0
        with torch.no_grad():
            for batch in val_loader:
                images = batch['image'].to(device)
                masks = batch['mask'].to(device)
                pred_mask, _ = model(images)
                m = calculate_metrics(pred_mask, masks)
                total_iou += m['iou']
                n_batches += 1
        avg_iou = total_iou / n_batches
        if avg_iou > best_val_iou:
            best_val_iou = avg_iou
            if save_path:
                torch.save(model.state_dict(), save_path)
    return best_val_iou

def evaluate_metrics(model, test_loader, device):
    model.eval()
    total_metrics = {'iou': 0.0, 'dice': 0.0, 'precision': 0.0, 'recall': 0.0, 'accuracy': 0.0}
    num_batches = 0
    with torch.no_grad():
        for batch in test_loader:
            images = batch['image'].to(device)
            masks = batch['mask'].to(device)
            pred_mask, _ = model(images)
            m = calculate_metrics(pred_mask, masks)
            for k in total_metrics:
                total_metrics[k] += m[k]
            num_batches += 1
    return {k: round((v / num_batches) * 100.0, 2) for k, v in total_metrics.items()}


# -------------------------------------------------------------------------
# Main Ablation Runner
# -------------------------------------------------------------------------
def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"=== Running Controlled Reproducible Ablation Study on {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}) ===")
    
    models_dir = r"d:\scratch\3rs sem\models"
    review_dir = r"d:\scratch\3rs sem\review_audit"
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(review_dir, exist_ok=True)
    
    # Common test loaders (Normal and Tiny Defects)
    test_normal = IndustrialDefectDataset(num_samples=150, mode='val', condition='normal', seed=42)
    test_tiny = IndustrialDefectDataset(num_samples=150, mode='val', condition='tiny_defects', seed=42)
    
    loader_normal = DataLoader(test_normal, batch_size=16, shuffle=False)
    loader_tiny = DataLoader(test_tiny, batch_size=16, shuffle=False)
    
    ablation_records = []
    
    # ---------------------------------------------------------------------
    # 1. Architectural Component Ablations (Seed = 42)
    # ---------------------------------------------------------------------
    print("\n--- Part A: Architectural Factorial Ablation ---")
    arch_configs = [
        ("Arch-1: Baseline Backbone (U-Net)", UNet(base_ch=32), False,
         CompositeLoss(lambda_dice=1.0, lambda_focal=0.5, lambda_boundary=0.0), "ablation_arch1_baseline.pth"),
        ("Arch-2: Baseline + MSFP Blocks", UNet_MSFP(base_ch=32), False,
         CompositeLoss(lambda_dice=1.0, lambda_focal=0.5, lambda_boundary=0.0), "ablation_arch2_msfp.pth"),
        ("Arch-3: Baseline + MSFP + BAS (No Gate)", MSBANet_NoBGFF(base_ch=32), True,
         CompositeLoss(lambda_dice=1.0, lambda_focal=0.5, lambda_boundary=0.4), "ablation_arch3_bas.pth"),
        ("Arch-4: Full MSBA-Net (MSFP+BAS+BGFF)", MSBANet(base_ch=32), True,
         CompositeLoss(lambda_dice=1.0, lambda_focal=0.5, lambda_boundary=0.4), "ablation_arch4_msba.pth")
    ]
    
    for name, model, has_bound, criterion, ckpt_name in arch_configs:
        set_seed(42)
        train_ds = IndustrialDefectDataset(num_samples=700, mode='train', condition='normal', seed=42)
        val_ds = IndustrialDefectDataset(num_samples=150, mode='val', condition='normal', seed=42)
        tr_loader = DataLoader(train_ds, batch_size=16, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=16, shuffle=False)
        
        ckpt_path = os.path.join(models_dir, ckpt_name)
        model.to(device)
        criterion.to(device)
        
        t0 = time.time()
        print(f"Training [{name}]...")
        train_one_model(model, tr_loader, val_loader, criterion, device, epochs=12, has_boundary=has_bound, save_path=ckpt_path)
        dt = time.time() - t0
        
        # Load best weights and evaluate
        model.load_state_dict(torch.load(ckpt_path, map_location=device))
        res_norm = evaluate_metrics(model, loader_normal, device)
        res_tiny = evaluate_metrics(model, loader_tiny, device)
        n_params = sum(p.numel() for p in model.parameters())
        
        print(f" -> Completed in {dt:.1f}s | Normal mIoU: {res_norm['iou']:.2f}% | Dice: {res_norm['dice']:.2f}% | Tiny mIoU: {res_tiny['iou']:.2f}% | Params: {n_params/1e6:.2f}M")
        
        ablation_records.append({
            'Category': 'Architectural Ablation',
            'Configuration': name,
            'Seed': 42,
            'mIoU (%)': res_norm['iou'],
            'Dice (%)': res_norm['dice'],
            'Precision (%)': res_norm['precision'],
            'Recall (%)': res_norm['recall'],
            'Tiny mIoU (%)': res_tiny['iou'],
            'Parameters': f"{n_params/1e6:.2f}M",
            'Checkpoint': ckpt_name
        })

    # ---------------------------------------------------------------------
    # 2. Loss Function Component Ablations (MSBA-Net, Seed = 42)
    # ---------------------------------------------------------------------
    print("\n--- Part B: Loss Formulation Factorial Ablation ---")
    loss_configs = [
        ("Loss-1: L_BCE Only", CompositeLoss(lambda_dice=0.0, lambda_focal=0.0, lambda_boundary=0.0), False, "ablation_loss1_bce.pth"),
        ("Loss-2: L_BCE + L_Dice", CompositeLoss(lambda_dice=1.0, lambda_focal=0.0, lambda_boundary=0.0), False, "ablation_loss2_dice.pth"),
        ("Loss-3: L_BCE + L_Dice + L_Focal", CompositeLoss(lambda_dice=1.0, lambda_focal=0.5, lambda_boundary=0.0), False, "ablation_loss3_focal.pth"),
        ("Loss-4: Full Composite (BCE+Dice+Focal+Bound)", CompositeLoss(lambda_dice=1.0, lambda_focal=0.5, lambda_boundary=0.4), True, "ablation_loss4_full.pth")
    ]
    
    for name, criterion, has_bound, ckpt_name in loss_configs:
        set_seed(42)
        model = MSBANet(base_ch=32).to(device)
        criterion.to(device)
        
        train_ds = IndustrialDefectDataset(num_samples=700, mode='train', condition='normal', seed=42)
        val_ds = IndustrialDefectDataset(num_samples=150, mode='val', condition='normal', seed=42)
        tr_loader = DataLoader(train_ds, batch_size=16, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=16, shuffle=False)
        
        ckpt_path = os.path.join(models_dir, ckpt_name)
        t0 = time.time()
        print(f"Training [{name}] on MSBA-Net...")
        train_one_model(model, tr_loader, val_loader, criterion, device, epochs=12, has_boundary=has_bound, save_path=ckpt_path)
        dt = time.time() - t0
        
        model.load_state_dict(torch.load(ckpt_path, map_location=device))
        res_norm = evaluate_metrics(model, loader_normal, device)
        res_tiny = evaluate_metrics(model, loader_tiny, device)
        n_params = sum(p.numel() for p in model.parameters())
        
        print(f" -> Completed in {dt:.1f}s | Normal mIoU: {res_norm['iou']:.2f}% | Dice: {res_norm['dice']:.2f}% | Tiny mIoU: {res_tiny['iou']:.2f}%")
        
        ablation_records.append({
            'Category': 'Loss Formulation Ablation',
            'Configuration': name,
            'Seed': 42,
            'mIoU (%)': res_norm['iou'],
            'Dice (%)': res_norm['dice'],
            'Precision (%)': res_norm['precision'],
            'Recall (%)': res_norm['recall'],
            'Tiny mIoU (%)': res_tiny['iou'],
            'Parameters': f"{n_params/1e6:.2f}M",
            'Checkpoint': ckpt_name
        })

    # ---------------------------------------------------------------------
    # 3. Multi-Seed Statistical Variance Evaluation (MSBA-Net)
    # ---------------------------------------------------------------------
    print("\n--- Part C: Multi-Seed Statistical Variance Evaluation ---")
    seeds = [42, 100, 2026]
    seed_records = []
    
    for s in seeds:
        set_seed(s)
        model = MSBANet(base_ch=32).to(device)
        criterion = CompositeLoss(lambda_dice=1.0, lambda_focal=0.5, lambda_boundary=0.4).to(device)
        
        train_ds = IndustrialDefectDataset(num_samples=700, mode='train', condition='normal', seed=s)
        val_ds = IndustrialDefectDataset(num_samples=150, mode='val', condition='normal', seed=s)
        tr_loader = DataLoader(train_ds, batch_size=16, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=16, shuffle=False)
        
        ckpt_path = os.path.join(models_dir, f"msba_seed_{s}.pth")
        t0 = time.time()
        print(f"Training MSBA-Net under Seed [{s}]...")
        train_one_model(model, tr_loader, val_loader, criterion, device, epochs=12, has_boundary=True, save_path=ckpt_path)
        dt = time.time() - t0
        
        model.load_state_dict(torch.load(ckpt_path, map_location=device))
        res_norm = evaluate_metrics(model, loader_normal, device)
        res_tiny = evaluate_metrics(model, loader_tiny, device)
        
        print(f" -> Seed {s} ({dt:.1f}s) | mIoU: {res_norm['iou']:.2f}% | Dice: {res_norm['dice']:.2f}% | Tiny mIoU: {res_tiny['iou']:.2f}%")
        seed_records.append(res_norm)
        
        ablation_records.append({
            'Category': 'Multi-Seed Variance',
            'Configuration': f"MSBA-Net (Seed {s})",
            'Seed': s,
            'mIoU (%)': res_norm['iou'],
            'Dice (%)': res_norm['dice'],
            'Precision (%)': res_norm['precision'],
            'Recall (%)': res_norm['recall'],
            'Tiny mIoU (%)': res_tiny['iou'],
            'Parameters': f"{sum(p.numel() for p in model.parameters())/1e6:.2f}M",
            'Checkpoint': f"msba_seed_{s}.pth"
        })
        
    # Compute mean and std
    m_ious = [r['iou'] for r in seed_records]
    m_dices = [r['dice'] for r in seed_records]
    m_precs = [r['precision'] for r in seed_records]
    m_recs = [r['recall'] for r in seed_records]
    
    print("\n=== MULTI-SEED AGGREGATE SUMMARY (N = 3 Seeds) ===")
    print(f"mIoU:      {np.mean(m_ious):.2f}% +/- {np.std(m_ious):.2f}% (Range: {np.min(m_ious):.2f}% - {np.max(m_ious):.2f}%)")
    print(f"Dice:      {np.mean(m_dices):.2f}% +/- {np.std(m_dices):.2f}% (Range: {np.min(m_dices):.2f}% - {np.max(m_dices):.2f}%)")
    print(f"Precision: {np.mean(m_precs):.2f}% +/- {np.std(m_precs):.2f}%")
    print(f"Recall:    {np.mean(m_recs):.2f}% +/- {np.std(m_recs):.2f}%")
    
    ablation_records.append({
        'Category': 'Multi-Seed Aggregate',
        'Configuration': "MSBA-Net Mean +/- Std (N=3)",
        'Seed': '42, 100, 2026',
        'mIoU (%)': f"{np.mean(m_ious):.2f} +/- {np.std(m_ious):.2f}",
        'Dice (%)': f"{np.mean(m_dices):.2f} +/- {np.std(m_dices):.2f}",
        'Precision (%)': f"{np.mean(m_precs):.2f} +/- {np.std(m_precs):.2f}",
        'Recall (%)': f"{np.mean(m_recs):.2f} +/- {np.std(m_recs):.2f}",
        'Tiny mIoU (%)': "-",
        'Parameters': "8.65M",
        'Checkpoint': "All Seeds"
    })
    
    # Save CSV
    out_csv = os.path.join(review_dir, "ABLATION_RESULTS.csv")
    keys = list(ablation_records[0].keys())
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(ablation_records)
    print(f"\nSuccessfully wrote verified results to {out_csv}")

if __name__ == '__main__':
    main()
