import os
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from PIL import Image, ImageFilter
import scipy.ndimage as ndimage

class IndustrialDefectDataset(Dataset):
    """
    Industrial Steel Surface Defect Segmentation Dataset.
    Synthesizes and loads high-fidelity realistic steel surface textures with authentic
    defect morphologies modeled after the benchmark NEU Surface Defect Database (NEU-Seg).
    
    Supports 6 defect categories:
    1. Crazing (micro-cracks with branching)
    2. Inclusion (small isolated particulate defects)
    3. Patches (low-contrast surface blemishes)
    4. Pitted Surface (clusters of tiny localized pinholes)
    5. Rolled-in Scale (textured oxide scale indentations)
    6. Scratches (directional linear surface gouges)
    
    Also provides a factory degradation suite for robustness evaluation:
    - Normal
    - Low Contrast
    - Sensor Noise
    - Motion Blur
    - Tiny Defects (<1% image area)
    """
    def __init__(self, num_samples=600, img_size=(256, 256), mode='train', condition='normal', seed=42):
        self.num_samples = num_samples
        self.img_size = img_size
        self.mode = mode
        self.condition = condition
        self.rng = np.random.RandomState(seed if mode == 'train' else seed + 1000)
        self.defect_types = ['crazing', 'inclusion', 'patches', 'pitted_surface', 'rolled_in_scale', 'scratches']
        
    def __len__(self):
        return self.num_samples
        
    def _generate_steel_background(self, h, w):
        """Generates realistic metallic rolled steel texture with grain and non-uniform lighting."""
        # Base metal gray intensity
        base_val = self.rng.uniform(115, 145)
        bg = np.full((h, w), base_val, dtype=np.float32)
        
        # Horizontal rolling grain / lines
        freq = self.rng.uniform(0.05, 0.2)
        y_coords = np.arange(h)[:, None]
        grain = np.sin(y_coords * freq) * self.rng.uniform(3, 8)
        bg += grain
        
        # Random low-frequency illumination gradient (non-uniform lighting across strip)
        x_grad = np.linspace(-1, 1, w)[None, :] * self.rng.uniform(-15, 15)
        y_grad = np.linspace(-1, 1, h)[:, None] * self.rng.uniform(-10, 10)
        bg += x_grad + y_grad
        
        # High-frequency micro-texture noise
        noise = self.rng.normal(0, self.rng.uniform(2, 4), (h, w))
        bg += noise
        
        return np.clip(bg, 0, 255)

    def _synthesize_defect(self, h, w, defect_type, is_tiny=False):
        """Synthesizes defect pattern and corresponding binary mask."""
        mask = np.zeros((h, w), dtype=np.float32)
        defect_layer = np.zeros((h, w), dtype=np.float32)
        
        cx = self.rng.randint(w // 4, 3 * w // 4)
        cy = self.rng.randint(h // 4, 3 * h // 4)
        
        if defect_type == 'crazing' or is_tiny:
            # Fine dendritic micro-cracks
            num_cracks = self.rng.randint(1, 3) if is_tiny else self.rng.randint(3, 6)
            for _ in range(num_cracks):
                curr_x, curr_y = cx + self.rng.randint(-20, 20), cy + self.rng.randint(-20, 20)
                curr_x = np.clip(curr_x, 10, w - 10)
                curr_y = np.clip(curr_y, 10, h - 10)
                length = self.rng.randint(15, 35) if is_tiny else self.rng.randint(30, 80)
                angle = self.rng.uniform(0, 2 * np.pi)
                for _ in range(length):
                    angle += self.rng.uniform(-0.4, 0.4)
                    curr_x += np.cos(angle)
                    curr_y += np.sin(angle)
                    ix, iy = int(round(curr_x)), int(round(curr_y))
                    if 0 <= ix < w and 0 <= iy < h:
                        mask[iy, ix] = 1.0
                        defect_layer[iy, ix] = self.rng.uniform(-50, -30) # Dark crack
            # Slight dilation for 1-2 pixel width
            mask = ndimage.binary_dilation(mask, iterations=1).astype(np.float32)
            defect_layer = ndimage.gaussian_filter(defect_layer, sigma=0.6)
            
        elif defect_type == 'inclusion':
            # Small particulate inclusion
            num_inc = 1 if is_tiny else self.rng.randint(2, 5)
            for _ in range(num_inc):
                rx = self.rng.randint(2, 4) if is_tiny else self.rng.randint(4, 10)
                ry = self.rng.randint(2, 5) if is_tiny else self.rng.randint(5, 14)
                ox, oy = cx + self.rng.randint(-30, 30), cy + self.rng.randint(-30, 30)
                y_idx, x_idx = np.ogrid[:h, :w]
                dist = ((x_idx - ox) / rx) ** 2 + ((y_idx - oy) / ry) ** 2
                cur_m = (dist <= 1.0).astype(np.float32)
                mask = np.maximum(mask, cur_m)
                defect_layer[cur_m > 0] = self.rng.uniform(-65, -40)
                
        elif defect_type == 'patches':
            # Low-contrast diffuse blemishes
            rx = self.rng.randint(6, 12) if is_tiny else self.rng.randint(15, 35)
            ry = self.rng.randint(6, 12) if is_tiny else self.rng.randint(15, 35)
            y_idx, x_idx = np.ogrid[:h, :w]
            dist = ((x_idx - cx) / rx) ** 2 + ((y_idx - cy) / ry) ** 2
            cur_m = (dist <= 1.0).astype(np.float32)
            # Add boundary irregularity
            cur_m = ndimage.gaussian_filter(cur_m, sigma=2.0) > 0.4
            mask = cur_m.astype(np.float32)
            contrast_shift = self.rng.choice([-1, 1]) * self.rng.uniform(15, 25) # low contrast!
            defect_layer[mask > 0] = contrast_shift
            
        elif defect_type == 'pitted_surface':
            # Clusters of small pinholes
            num_pits = self.rng.randint(3, 6) if is_tiny else self.rng.randint(10, 25)
            for _ in range(num_pits):
                px = int(cx + self.rng.normal(0, 10 if is_tiny else 25))
                py = int(cy + self.rng.normal(0, 10 if is_tiny else 25))
                pr = self.rng.randint(1, 3)
                if 0 <= px < w and 0 <= py < h:
                    y_idx, x_idx = np.ogrid[:h, :w]
                    pit_m = (((x_idx - px)**2 + (y_idx - py)**2) <= pr**2).astype(np.float32)
                    mask = np.maximum(mask, pit_m)
                    defect_layer[pit_m > 0] = self.rng.uniform(-75, -50)
                    
        elif defect_type == 'rolled_in_scale':
            # Irregular mottled oxidized scale
            rx, ry = self.rng.randint(12, 28), self.rng.randint(15, 35)
            y_idx, x_idx = np.ogrid[:h, :w]
            blob = (((x_idx - cx) / rx) ** 2 + ((y_idx - cy) / ry) ** 2 <= 1.0).astype(np.float32)
            roughness = self.rng.normal(0, 0.4, (h, w))
            blob = (blob + roughness) > 0.8
            mask = blob.astype(np.float32)
            defect_layer[mask > 0] = self.rng.uniform(-55, -35)
            
        else: # scratches
            # Directional linear scratches
            num_scratches = 1 if is_tiny else self.rng.randint(1, 3)
            for _ in range(num_scratches):
                angle = self.rng.uniform(-np.pi/4, np.pi/4) # mostly longitudinal
                length = self.rng.randint(25, 50) if is_tiny else self.rng.randint(60, 140)
                sx, sy = cx + self.rng.randint(-20, 20), cy + self.rng.randint(-20, 20)
                for step in range(-length // 2, length // 2):
                    ix = int(sx + step * np.cos(angle))
                    iy = int(sy + step * np.sin(angle))
                    if 0 <= ix < w and 0 <= iy < h:
                        mask[iy, ix] = 1.0
                        defect_layer[iy, ix] = self.rng.uniform(-60, -40)
            mask = ndimage.binary_dilation(mask, iterations=1).astype(np.float32)
            
        return mask, defect_layer

    def _compute_boundary(self, mask):
        """Extracts boundary contour of mask using morphological gradient."""
        dilated = ndimage.binary_dilation(mask, iterations=2)
        eroded = ndimage.binary_erosion(mask, iterations=1)
        boundary = (dilated.astype(np.float32) - eroded.astype(np.float32))
        return np.clip(boundary, 0, 1.0)

    def _apply_degradation(self, img, condition):
        """Applies realistic industrial imaging degradations."""
        if condition == 'normal':
            return img
        elif condition == 'low_contrast':
            # Severe contrast attenuation simulating ambient glare/reflection
            mean_val = np.mean(img)
            return np.clip((img - mean_val) * 0.45 + mean_val, 0, 255)
        elif condition == 'noise':
            # High sensor noise
            noise = self.rng.normal(0, 18.0, img.shape)
            return np.clip(img + noise, 0, 255)
        elif condition == 'blur':
            # Motion blur from rapid industrial rolling line
            pil_im = Image.fromarray(img.astype(np.uint8))
            blurred = pil_im.filter(ImageFilter.GaussianBlur(radius=2.5))
            return np.array(blurred, dtype=np.float32)
        elif condition == 'tiny_defects':
            return img
        return img

    def __getitem__(self, idx):
        h, w = self.img_size
        defect_type = self.defect_types[idx % len(self.defect_types)]
        is_tiny = (self.condition == 'tiny_defects') or (self.rng.uniform() < 0.2 and self.mode == 'train')
        
        # 1. Background
        bg = self._generate_steel_background(h, w)
        
        # 2. Defect
        mask, defect_layer = self._synthesize_defect(h, w, defect_type, is_tiny=is_tiny)
        
        # Combine
        img = np.clip(bg + defect_layer, 0, 255)
        
        # 3. Apply condition degradation
        img = self._apply_degradation(img, self.condition)
        
        # 4. Compute boundary
        boundary = self._compute_boundary(mask)
        
        # Normalize to [0, 1] tensor
        img_tensor = torch.from_numpy(img / 255.0).float().unsqueeze(0) # (1, H, W)
        mask_tensor = torch.from_numpy(mask).float().unsqueeze(0)        # (1, H, W)
        boundary_tensor = torch.from_numpy(boundary).float().unsqueeze(0)# (1, H, W)
        
        return {
            'image': img_tensor,
            'mask': mask_tensor,
            'boundary': boundary_tensor,
            'defect_type': defect_type,
            'condition': self.condition
        }
