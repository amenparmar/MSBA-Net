import torch
import torch.nn as nn
import torch.nn.functional as F

class ConvBlock(nn.Module):
    """Standard double convolution block with BatchNorm and LeakyReLU."""
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_ch),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(out_ch, out_ch, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_ch),
            nn.LeakyReLU(0.1, inplace=True)
        )
    def forward(self, x):
        return self.conv(x)


# =========================================================================
# Baseline 1: Standard U-Net
# =========================================================================
class UNet(nn.Module):
    def __init__(self, in_channels=1, num_classes=1, base_ch=32):
        super().__init__()
        self.enc1 = ConvBlock(in_channels, base_ch)
        self.enc2 = ConvBlock(base_ch, base_ch * 2)
        self.enc3 = ConvBlock(base_ch * 2, base_ch * 4)
        self.enc4 = ConvBlock(base_ch * 4, base_ch * 8)
        
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
        e1 = self.enc1(x)
        e2 = self.enc2(F.max_pool2d(e1, 2))
        e3 = self.enc3(F.max_pool2d(e2, 2))
        e4 = self.enc4(F.max_pool2d(e3, 2))
        
        b = self.bottleneck(F.max_pool2d(e4, 2))
        
        d4 = self.dec4(torch.cat([self.up4(b), e4], dim=1))
        d3 = self.dec3(torch.cat([self.up3(d4), e3], dim=1))
        d2 = self.dec2(torch.cat([self.up2(d3), e2], dim=1))
        d1 = self.dec1(torch.cat([self.up1(d2), e1], dim=1))
        
        out = self.out_conv(d1)
        return out, None # None for boundary compatibility


# =========================================================================
# Baseline 2: U-Net++ (Nested and Dense Skip Connections)
# =========================================================================
class UNetPlusPlus(nn.Module):
    def __init__(self, in_channels=1, num_classes=1, base_ch=32):
        super().__init__()
        nb = [base_ch, base_ch*2, base_ch*4, base_ch*8, base_ch*16]
        
        self.conv0_0 = ConvBlock(in_channels, nb[0])
        self.conv1_0 = ConvBlock(nb[0], nb[1])
        self.conv2_0 = ConvBlock(nb[1], nb[2])
        self.conv3_0 = ConvBlock(nb[2], nb[3])
        self.conv4_0 = ConvBlock(nb[3], nb[4])
        
        self.conv0_1 = ConvBlock(nb[0] + nb[1], nb[0])
        self.conv1_1 = ConvBlock(nb[1] + nb[2], nb[1])
        self.conv2_1 = ConvBlock(nb[2] + nb[3], nb[2])
        self.conv3_1 = ConvBlock(nb[3] + nb[4], nb[3])
        
        self.conv0_2 = ConvBlock(nb[0]*2 + nb[1], nb[0])
        self.conv1_2 = ConvBlock(nb[1]*2 + nb[2], nb[1])
        self.conv2_2 = ConvBlock(nb[2]*2 + nb[3], nb[2])
        
        self.conv0_3 = ConvBlock(nb[0]*3 + nb[1], nb[0])
        self.conv1_3 = ConvBlock(nb[1]*3 + nb[2], nb[1])
        
        self.conv0_4 = ConvBlock(nb[0]*4 + nb[1], nb[0])
        
        self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        self.final = nn.Conv2d(nb[0], num_classes, kernel_size=1)
        
    def forward(self, x):
        x0_0 = self.conv0_0(x)
        x1_0 = self.conv1_0(F.max_pool2d(x0_0, 2))
        x0_1 = self.conv0_1(torch.cat([x0_0, self.up(x1_0)], 1))
        
        x2_0 = self.conv2_0(F.max_pool2d(x1_0, 2))
        x1_1 = self.conv1_1(torch.cat([x1_0, self.up(x2_0)], 1))
        x0_2 = self.conv0_2(torch.cat([x0_0, x0_1, self.up(x1_1)], 1))
        
        x3_0 = self.conv3_0(F.max_pool2d(x2_0, 2))
        x2_1 = self.conv2_1(torch.cat([x2_0, self.up(x3_0)], 1))
        x1_2 = self.conv1_2(torch.cat([x1_0, x1_1, self.up(x2_1)], 1))
        x0_3 = self.conv0_3(torch.cat([x0_0, x0_1, x0_2, self.up(x1_2)], 1))
        
        x4_0 = self.conv4_0(F.max_pool2d(x3_0, 2))
        x3_1 = self.conv3_1(torch.cat([x3_0, self.up(x4_0)], 1))
        x2_2 = self.conv2_2(torch.cat([x2_0, x2_1, self.up(x3_1)], 1))
        x1_3 = self.conv1_3(torch.cat([x1_0, x1_1, x1_2, self.up(x2_2)], 1))
        x0_4 = self.conv0_4(torch.cat([x0_0, x0_1, x0_2, x0_3, self.up(x1_3)], 1))
        
        out = self.final(x0_4)
        return out, None


# =========================================================================
# Proposed: MSBA-Net (Multi-Scale Feature Enhancement & Boundary-Aware Network)
# =========================================================================
class MultiScaleFeaturePreservation(nn.Module):
    """
    Multi-Scale Feature Preservation (MSFP) Block.
    Employs parallel dilated depthwise separable convolutions with dilation rates
    r in {1, 2, 4} to maintain multi-receptive field context and prevent subtle
    crack and inclusion features from vanishing during spatial downsampling.
    """
    def __init__(self, channels):
        super().__init__()
        self.branch1 = nn.Sequential(
            nn.Conv2d(channels, channels // 4, kernel_size=1, bias=False),
            nn.BatchNorm2d(channels // 4),
            nn.ReLU(inplace=True)
        )
        self.branch2 = nn.Sequential(
            nn.Conv2d(channels, channels // 4, kernel_size=3, padding=1, dilation=1, bias=False),
            nn.BatchNorm2d(channels // 4),
            nn.ReLU(inplace=True)
        )
        self.branch3 = nn.Sequential(
            nn.Conv2d(channels, channels // 4, kernel_size=3, padding=2, dilation=2, bias=False),
            nn.BatchNorm2d(channels // 4),
            nn.ReLU(inplace=True)
        )
        self.branch4 = nn.Sequential(
            nn.Conv2d(channels, channels // 4, kernel_size=3, padding=4, dilation=4, bias=False),
            nn.BatchNorm2d(channels // 4),
            nn.ReLU(inplace=True)
        )
        self.fuse = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=1, bias=False),
            nn.BatchNorm2d(channels),
            nn.ReLU(inplace=True)
        )
        
    def forward(self, x):
        b1 = self.branch1(x)
        b2 = self.branch2(x)
        b3 = self.branch3(x)
        b4 = self.branch4(x)
        out = torch.cat([b1, b2, b3, b4], dim=1)
        return x + self.fuse(out)


class BoundaryAwareFusion(nn.Module):
    """
    Boundary-Guided Spatial Attention Gate.
    Injects high-frequency boundary contour information into main decoder features,
    sharpening ambiguous and low-contrast defect transitions.
    """
    def __init__(self, seg_ch, bound_ch):
        super().__init__()
        self.gate_conv = nn.Sequential(
            nn.Conv2d(bound_ch, seg_ch, kernel_size=1, bias=False),
            nn.BatchNorm2d(seg_ch),
            nn.Sigmoid()
        )
        self.out_conv = nn.Sequential(
            nn.Conv2d(seg_ch, seg_ch, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(seg_ch),
            nn.LeakyReLU(0.1, inplace=True)
        )
        
    def forward(self, f_seg, f_bound):
        gate = self.gate_conv(f_bound)
        modulated = f_seg * (1.0 + gate)
        return self.out_conv(modulated)


class MSBANet(nn.Module):
    """
    Proposed MSBA-Net Architecture:
    1. Multi-scale feature enhancement preserving micro-scale defect signatures.
    2. Boundary-aware auxiliary stream predicting edge contours.
    3. Boundary-guided feature modulation sharpening low-contrast boundaries.
    """
    def __init__(self, in_channels=1, num_classes=1, base_ch=32):
        super().__init__()
        # Encoder stages
        self.enc1 = ConvBlock(in_channels, base_ch)
        self.msfp1 = MultiScaleFeaturePreservation(base_ch)
        
        self.enc2 = ConvBlock(base_ch, base_ch * 2)
        self.msfp2 = MultiScaleFeaturePreservation(base_ch * 2)
        
        self.enc3 = ConvBlock(base_ch * 2, base_ch * 4)
        self.msfp3 = MultiScaleFeaturePreservation(base_ch * 4)
        
        self.enc4 = ConvBlock(base_ch * 4, base_ch * 8)
        self.msfp4 = MultiScaleFeaturePreservation(base_ch * 8)
        
        # Bottleneck
        self.bottleneck = ConvBlock(base_ch * 8, base_ch * 16)
        
        # Auxiliary Boundary Stream Decoder
        self.b_up3 = nn.ConvTranspose2d(base_ch * 4, base_ch * 2, kernel_size=2, stride=2)
        self.b_conv3 = ConvBlock(base_ch * 4, base_ch * 2)
        self.b_up2 = nn.ConvTranspose2d(base_ch * 2, base_ch, kernel_size=2, stride=2)
        self.b_conv2 = ConvBlock(base_ch * 2, base_ch)
        self.b_head = nn.Conv2d(base_ch, 1, kernel_size=1)
        
        # Main Segmentation Decoder
        self.up4 = nn.ConvTranspose2d(base_ch * 16, base_ch * 8, kernel_size=2, stride=2)
        self.dec4 = ConvBlock(base_ch * 16, base_ch * 8)
        
        self.up3 = nn.ConvTranspose2d(base_ch * 8, base_ch * 4, kernel_size=2, stride=2)
        self.dec3 = ConvBlock(base_ch * 8, base_ch * 4)
        
        self.up2 = nn.ConvTranspose2d(base_ch * 4, base_ch * 2, kernel_size=2, stride=2)
        self.dec2 = ConvBlock(base_ch * 4, base_ch * 2)
        
        self.up1 = nn.ConvTranspose2d(base_ch * 2, base_ch, kernel_size=2, stride=2)
        self.dec1 = ConvBlock(base_ch * 2, base_ch)
        
        # Boundary-guided fusion module at fine resolution
        self.bg_fusion = BoundaryAwareFusion(base_ch, base_ch)
        
        self.seg_head = nn.Conv2d(base_ch, num_classes, kernel_size=1)
        
    def forward(self, x):
        # Encoder with multi-scale feature preservation
        e1 = self.msfp1(self.enc1(x))
        e2 = self.msfp2(self.enc2(F.max_pool2d(e1, 2)))
        e3 = self.msfp3(self.enc3(F.max_pool2d(e2, 2)))
        e4 = self.msfp4(self.enc4(F.max_pool2d(e3, 2)))
        
        b = self.bottleneck(F.max_pool2d(e4, 2))
        
        # Auxiliary Boundary Stream (extracting fine contour details from shallow/mid features)
        b_feat2 = self.b_conv3(torch.cat([self.b_up3(e3), e2], dim=1))
        b_feat1 = self.b_conv2(torch.cat([self.b_up2(b_feat2), e1], dim=1))
        pred_boundary = self.b_head(b_feat1)
        
        # Main Segmentation Stream
        d4 = self.dec4(torch.cat([self.up4(b), e4], dim=1))
        d3 = self.dec3(torch.cat([self.up3(d4), e3], dim=1))
        d2 = self.dec2(torch.cat([self.up2(d3), e2], dim=1))
        d1 = self.dec1(torch.cat([self.up1(d2), e1], dim=1))
        
        # Boundary-Guided Modulation
        d1_refined = self.bg_fusion(d1, b_feat1)
        pred_mask = self.seg_head(d1_refined)
        
        return pred_mask, pred_boundary
