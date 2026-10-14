import torch
import torch.nn as nn
import torch.nn.functional as F

class DiceLoss(nn.Module):
    def __init__(self, smooth=1.0):
        super().__init__()
        self.smooth = smooth
        
    def forward(self, logits, targets):
        probs = torch.sigmoid(logits)
        probs_flat = probs.view(-1)
        targets_flat = targets.view(-1)
        
        intersection = (probs_flat * targets_flat).sum()
        dice = (2.0 * intersection + self.smooth) / (probs_flat.sum() + targets_flat.sum() + self.smooth)
        return 1.0 - dice


class FocalLoss(nn.Module):
    def __init__(self, alpha=0.75, gamma=2.0):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        
    def forward(self, logits, targets):
        bce = F.binary_cross_entropy_with_logits(logits, targets, reduction='none')
        probs = torch.sigmoid(logits)
        p_t = probs * targets + (1 - probs) * (1 - targets)
        alpha_factor = self.alpha * targets + (1 - self.alpha) * (1 - targets)
        modulating_factor = (1.0 - p_t) ** self.gamma
        loss = alpha_factor * modulating_factor * bce
        return loss.mean()


class CompositeLoss(nn.Module):
    """
    Composite Loss for Small and Low-Contrast Defect Segmentation:
    L_total = L_BCE + 1.0 * L_Dice + 0.5 * L_Focal + lambda_b * L_Boundary
    """
    def __init__(self, lambda_dice=1.0, lambda_focal=0.5, lambda_boundary=0.4):
        super().__init__()
        self.bce = nn.BCEWithLogitsLoss()
        self.dice = DiceLoss()
        self.focal = FocalLoss()
        self.lambda_dice = lambda_dice
        self.lambda_focal = lambda_focal
        self.lambda_boundary = lambda_boundary
        
    def forward(self, pred_mask, target_mask, pred_boundary=None, target_boundary=None):
        l_bce = self.bce(pred_mask, target_mask)
        l_dice = self.dice(pred_mask, target_mask)
        l_focal = self.focal(pred_mask, target_mask)
        
        total_loss = l_bce + self.lambda_dice * l_dice + self.lambda_focal * l_focal
        
        if pred_boundary is not None and target_boundary is not None:
            l_bound_bce = self.bce(pred_boundary, target_boundary)
            l_bound_dice = self.dice(pred_boundary, target_boundary)
            l_bound = l_bound_bce + l_bound_dice
            total_loss = total_loss + self.lambda_boundary * l_bound
            
        return total_loss


# =========================================================================
# Metrics Suite
# =========================================================================
def calculate_metrics(pred_logits, targets, threshold=0.5):
    """
    Computes standard semantic segmentation metrics:
    - IoU (Intersection over Union)
    - Dice / F1-Score
    - Precision
    - Recall
    - Pixel Accuracy
    """
    probs = torch.sigmoid(pred_logits)
    preds = (probs > threshold).float()
    
    preds_flat = preds.view(-1)
    targets_flat = targets.view(-1)
    
    tp = (preds_flat * targets_flat).sum().item()
    fp = (preds_flat * (1.0 - targets_flat)).sum().item()
    fn = ((1.0 - preds_flat) * targets_flat).sum().item()
    tn = ((1.0 - preds_flat) * (1.0 - targets_flat)).sum().item()
    
    eps = 1e-7
    iou = (tp + eps) / (tp + fp + fn + eps)
    dice = (2.0 * tp + eps) / (2.0 * tp + fp + fn + eps)
    precision = (tp + eps) / (tp + fp + eps)
    recall = (tp + eps) / (tp + fn + eps)
    acc = (tp + tn) / (tp + tn + fp + fn + eps)
    
    return {
        'iou': iou,
        'dice': dice,
        'precision': precision,
        'recall': recall,
        'accuracy': acc
    }
