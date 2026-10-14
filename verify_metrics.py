import os
import sys
import json
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

# Add 3rs sem to path
sys.path.insert(0, r"d:\scratch\3rs sem")
from dataset import IndustrialDefectDataset
from models import UNet, UNetPlusPlus, MSBANet
from losses import calculate_metrics

def evaluate_model_on_dataset(model, dataloader, device):
    model.eval()
    total_metrics = {'iou': 0.0, 'dice': 0.0, 'precision': 0.0, 'recall': 0.0, 'accuracy': 0.0}
    num_batches = 0
    with torch.no_grad():
        for batch in dataloader:
            images = batch['image'].to(device)
            masks = batch['mask'].to(device)
            outputs = model(images)
            if isinstance(outputs, tuple):
                outputs = outputs[0]
            metrics = calculate_metrics(outputs, masks)
            for k in total_metrics:
                total_metrics[k] += metrics[k]
            num_batches += 1
    return {k: round((total_metrics[k] / num_batches) * 100.0, 2) for k in total_metrics}

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Executing Verification on Device: {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")

    base_dir = r"d:\scratch\3rs sem"
    models_dir = os.path.join(base_dir, "models")
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    # 1. Instantiate models and load actual checkpoints
    model_classes = {
        'UNet': UNet(in_channels=1, num_classes=1),
        'UNetPlusPlus': UNetPlusPlus(in_channels=1, num_classes=1),
        'MSBANet': MSBANet(in_channels=1, num_classes=1)
    }

    loaded_models = {}
    for name, model in model_classes.items():
        ckpt_path = os.path.join(models_dir, f"best_{name}.pth")
        if not os.path.exists(ckpt_path):
            raise FileNotFoundError(f"Checkpoint not found: {ckpt_path}")
        state_dict = torch.load(ckpt_path, map_location=device)
        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()
        loaded_models[name] = model
        print(f"Loaded weights for {name} from {ckpt_path}")

    # 2. Define test condition regimes
    condition_names = ['normal', 'low_contrast', 'noise', 'blur', 'tiny_defects']
    verified_results = {}
    print("\n--- Running Inference & Metric Computation Across Checkpoints ---")
    for model_name, model in loaded_models.items():
        verified_results[model_name] = {}
        for cond in condition_names:
            test_ds = IndustrialDefectDataset(num_samples=150, img_size=(256, 256), mode='val', condition=cond, seed=42)
            loader = DataLoader(test_ds, batch_size=16, shuffle=False)
            res = evaluate_model_on_dataset(model, loader, device)
            verified_results[model_name][cond] = res
            print(f"[{model_name:<12}] {cond:<14} -> mIoU: {res['iou']:>6.2f}% | Dice: {res['dice']:>6.2f}% | Prec: {res['precision']:>6.2f}% | Rec: {res['recall']:>6.2f}% | Acc: {res['accuracy']:>6.2f}%")

    out_json = os.path.join(results_dir, "verified_benchmark_metrics.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(verified_results, f, indent=2)
    print(f"\nSuccessfully saved verified metrics to {out_json}")

if __name__ == '__main__':
    main()
