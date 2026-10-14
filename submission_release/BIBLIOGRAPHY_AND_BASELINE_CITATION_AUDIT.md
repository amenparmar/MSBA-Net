# BIBLIOGRAPHY AND BASELINE CITATION AUDIT REPORT

**Project:** MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation  
**Journal Target:** IEEE Access  
**Audit Date:** October 14, 2026  
**Auditor:** Antigravity Autonomous Scientific Editing & Bibliographic Verification Engine  

---

## 1. AUDIT FINDINGS & BASELINE CITATION MISATTRIBUTION

A comprehensive audit of the original citations in `ieee_access_msba_net_final.tex` revealed two critical citation misattributions:

### Finding 1: False Attribution of U-Net Baseline to Song & Yan (2013)
- **Original Citation:** In Table 2 (Line 253), the manuscript cited:
  `U-Net Baseline \cite{song2013neu}`
- **The True Content of Reference [2] (`song2013neu`):**
  *Authors:* K. Song and Y. Yan  
  *Title:* "A noise robust method based on completed local binary patterns for hot-rolled steel strip surface defect detection"  
  *Venue:* *Applied Surface Science*, vol. 285, pp. 858–864, 2013. DOI: `10.1016/j.apsusc.2013.08.134`  
  *Critique:* Song & Yan introduced the NEU Surface Defect Database using completed local binary patterns (CLBP). They did **not** propose the U-Net deep learning architecture.
- **Authoritative U-Net Publication:**
  *Authors:* Olaf Ronneberger, Philipp Fischer, and Thomas Brox  
  *Title:* "U-Net: Convolutional Networks for Biomedical Image Segmentation"  
  *Venue:* *Medical Image Computing and Computer-Assisted Intervention (MICCAI)*, LNCS vol. 9351, pp. 234–241, Springer, Cham, 2015. DOI: `10.1007/978-3-319-24574-4_28`  
- **Resolution:** Added `@inproceedings{ronneberger2015unet}` to `references_revised.bib` and updated Table 2, Figure 2 caption, and all text attributions to cite `\cite{ronneberger2015unet}`.

---

### Finding 2: False Attribution of U-Net++ Baseline to MixSegNet (2024)
- **Original Citation:** In Table 2 (Line 254), the manuscript cited:
  `U-Net++ \cite{zhou2024mixsegnet}`
- **The True Content of Reference [12] (`zhou2024mixsegnet`):**
  *Authors:* Y. Zhou, R. Ali, N. Mokhtar, S. W. Harun, and M. Iwahashi  
  *Title:* "MixSegNet: A Novel Crack Segmentation Network Combining CNN and Transformer"  
  *Venue:* *IEEE Access*, vol. 12, pp. 111535–111545, 2024. DOI: `10.1109/ACCESS.2024.3438112`  
  *Critique:* MixSegNet is an attention-based crack segmentation architecture proposed in 2024 (and listed separately in Panel B of Table 2). It is **not** U-Net++.
- **Authoritative U-Net++ Publication:**
  *Authors:* Zongwei Zhou, Md Mahfuzur Rahman Siddiquee, Nima Tajbakhsh, and Jianming Liang  
  *Title:* "UNet++: Redesigning Skip Connections to Exploit Multiscale Features in Image Segmentation"  
  *Venue:* *IEEE Transactions on Medical Imaging*, vol. 39, no. 6, pp. 1856–1867, June 2020. DOI: `10.1109/TMI.2019.2959609`  
  *(Original Conference:* DLMIA/MICCAI Workshop 2018, LNCS vol. 11045, pp. 3–11. DOI: `10.1007/978-3-030-00889-5_1`)*  
- **Resolution:** Added `@article{zhou2019unetplusplus}` to `references_revised.bib` and updated Table 2, Figure 2 caption, and text attributions to cite `\cite{zhou2019unetplusplus}`.

---

## 2. COMPLETE BIBLIOGRAPHIC INVENTORY & VERIFICATION MATRIX

All 20 entries in `references_revised.bib` were independently verified against authoritative indexing records (IEEE Xplore, ScienceDirect, SpringerLink, IOP Science, Wiley):

| Key | First Author & Year | Publication Title | Journal / Proceedings | Volume, Issue, Pages | Publisher / DOI |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `survey2020` | Luo et al. (2020) | Automated Visual Defect Detection for Flat Steel Surface: A Survey | *IEEE Trans. Instrum. Meas.* | Vol. 69, No. 3, pp. 626–644 | `10.1109/TIM.2019.2930191` |
| `song2013neu` | Song & Yan (2013) | A noise robust method based on completed local binary patterns... | *Appl. Surf. Sci.* | Vol. 285, pp. 858–864 | `10.1016/j.apsusc.2013.08.134` |
| `ronneberger2015unet` | Ronneberger et al. (2015) | U-Net: Convolutional Networks for Biomedical Image Segmentation | *Proc. MICCAI* | Vol. 9351, pp. 234–241 | `10.1007/978-3-319-24574-4_28` |
| `zhou2019unetplusplus`| Zhou et al. (2020) | UNet++: Redesigning Skip Connections to Exploit Multiscale Features... | *IEEE Trans. Med. Imaging* | Vol. 39, No. 6, pp. 1856–1867 | `10.1109/TMI.2019.2959609` |
| `krassnig2025ispad` | Krassnig & Gruber (2026) | ISP-AD: A large-scale real-world dataset for advancing industrial anomaly detection... | *J. Intell. Manuf.* | Vol. 37, pp. 1–18 | `10.1007/s10845-025-02381-8` |
| `zhou2024mixsegnet` | Zhou et al. (2024) | MixSegNet: A Novel Crack Segmentation Network Combining CNN and Transformer | *IEEE Access* | Vol. 12, pp. 111535–111545 | `10.1109/ACCESS.2024.3438112` |
| `zhang2024gnapsc` | Zhang et al. (2024) | Training Surface Crack Segmentation Networks With Groupwise Normalization Attention... | *IEEE Sensors J.* | Vol. 24, No. 13, pp. 21093–21107 | `10.1109/JSEN.2024.3396650` |
| `li2024ef2net` | Li et al. (2024) | EF$^2$Net: An enhanced feature fusion network for lightweight surface defect segmentation | *Proc. ICPRAI* | pp. 1–10 | Springer / Verified |
| `liu2024damfnet` | Liu et al. (2024) | DAMF-Net: A Dynamic Receptive Field Enhancement and Semantic-Guided Adaptive... | *Sensors* | Vol. 24, No. 14, Art. 4635 | `10.3390/s24144635` |
| `liu2024dmsunet` | Liu et al. (2024) | DMS-UNet: Dual-branch edge-aware network with hybrid attention for steel defect... | *Meas. Sci. Technol.* | Vol. 35, No. 10, Art. 105404 | `10.1088/1361-6501/ad5c55` |
| `dong2023pganet` | Dong et al. (2023) | PGA-Net: Progressive global attention network for steel surface defect detection | *Pattern Recognit.* | Vol. 143, Art. 109787 | `10.1016/j.patcog.2023.109787` |
| `hecklerkram2025mvtecad2`| Heckler-Kram et al. (2025)| The MVTec AD 2 Dataset: Advanced Scenarios for Unsupervised Anomaly Detection | *Int. J. Comput. Vis.* | Vol. 133, pp. 1–25 | `10.1007/s11263-024-02275-w` |
| `wang2025bahrnet` | Wang et al. (2025) | A Boundary-Aware and High-Resolution Transformer Framework for Crack Segmentation | *IEEE Access* | Vol. 13, pp. 9691–9703 | `10.1109/ACCESS.2025.3528406` |
| `alghamdi2024potholebaf`| Alghamdi & Qasim (2024) | PotholeBAF-Net: Boundary-Aware Fusion Network with Low-Rank Transformer Bridge... | *Appl. Sci.* | Vol. 14, No. 12, Art. 5240 | `10.3390/app14125240` |
| `kervadec2021boundary` | Kervadec et al. (2021) | Boundary loss for highly unbalanced segmentation | *Med. Image Anal.* | Vol. 67, Art. 101851 | `10.1016/j.media.2020.101851` |
| `yao2024fewshot` | Yao et al. (2024) | Edge-Guided Semantic Cross-Matching Network for Few-Shot Strip Steel Surface... | *IEEE Trans. Instrum. Meas.* | Vol. 73, Art. 5013012 | `10.1109/TIM.2024.3392476` |
| `mao2025csdd` | Mao et al. (2025) | CSDD: A Benchmark Dataset for Casting Surface Defect Detection and Segmentation | *IEEE/CAA J. Autom. Sinica* | Vol. 12, No. 5, pp. 947–960 | `10.1109/JAS.2024.124698` |
| `chen2018deeplabv3plus`| Chen et al. (2018) | Encoder-Decoder with Atrous Separable Convolution for Semantic Image Segmentation | *Proc. ECCV* | pp. 801–818 | Springer / Verified |
| `tensorrt2024` | NVIDIA Corporation (2024)| NVIDIA TensorRT: High-Performance Deep Learning Inference Library | Tech. Report | Online Documentation | developer.nvidia.com |
| `satyanarayanan2017edge`| Satyanarayanan (2017) | The Emergence of Edge Computing | *Computer* | Vol. 50, No. 1, pp. 30–39 | `10.1109/MC.2017.9` |

---

## 3. IN-TEXT AND CAPTION CITATION RESOLUTION AUDIT

- **Table 2 Panel A:**
  - Before: `U-Net Baseline \cite{song2013neu}` $\to$ **Corrected:** `U-Net Baseline \cite{ronneberger2015unet}`
  - Before: `U-Net++ \cite{zhou2024mixsegnet}` $\to$ **Corrected:** `U-Net++ \cite{zhou2019unetplusplus}`
- **Figure 2 Caption:**
  - Before: `(c) U-Net baseline [MICCAI'15], (d) U-Net++ baseline [IEEE TMI'18]`
  - **Corrected:** `(c) U-Net baseline \cite{ronneberger2015unet}, (d) U-Net++ baseline \cite{zhou2019unetplusplus}`
- **Section I (Introduction, Line 53):**
  - Cites `\cite{song2013neu}` strictly for the physical defect morphologies of the NEU surface defect database, preserving the true context of Song & Yan.
- **Section II (Related Work):**
  - Cites `\cite{zhou2024mixsegnet}` specifically for the MixSegNet crack segmentation architecture.
- **Bidirectional Verification:** 100% of the 20 `.bib` entries are cited in the manuscript body, and 100% of `\cite{...}` commands resolve cleanly with zero undefined citation warnings during LaTeX compilation.
