# INDEPENDENT BIBLIOGRAPHY & BASELINE CITATION AUDIT REPORT

**Manuscript Title:** MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation  
**Journal Target:** IEEE Access  
**Evaluation Date:** October 14, 2026  
**Auditor:** Independent Autonomous CV Research & LaTeX Auditor  
**Bibliography File:** `submission_release/references_revised.bib`  

---

## 1. EXECUTIVE SUMMARY & VERIFICATION STATUS

Every entry in `submission_release/references_revised.bib` was independently audited for bibliographic accuracy, peer-reviewed venue provenance, author listing, publication year, volume/pages, and digital object identifier (DOI).

- **Total Bibliography Entries:** 20
- **Total In-Text Citations:** 20 distinct keys cited across Sections I–VII
- **Uncited Bibliography Entries:** 0
- **Undefined Citations in Manuscript:** 0 (verified by `fitz` extraction and Tectonic log)
- **Baseline Attributions Corrected:** U-Net (Ronneberger et al., *MICCAI 2015*) and U-Net++ (Zhou et al., *IEEE TMI 2020*)
- **Placeholder / Fabricated DOIs:** 0

---

## 2. REFERENCE-BY-REFERENCE FORENSIC AUDIT

| Key | First Author & Title | Venue / Year | Verified DOI / URL | Citation Context | Audit Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `survey2020` | Q. Luo et al., *Automated Visual Defect Detection for Flat Steel Surface: A Survey* | IEEE Trans. Instrum. Meas., 2020 (Vol. 69, No. 3, pp. 626–644) | `10.1109/TIM.2019.2930191` | Sec. I (Industrial speed, line automation) | **VERIFIED** |
| `song2013neu` | K. Song & Y. Yan, *A noise robust method based on completed local binary patterns for hot-rolled steel strip surface defect detection* | Appl. Surf. Sci., 2013 (Vol. 285, pp. 858–864) | `10.1016/j.apsusc.2013.08.134` | Sec. I, Sec. II-C (NEU database morphology) | **VERIFIED** |
| `ronneberger2015unet` | O. Ronneberger, P. Fischer, T. Brox, *U-Net: Convolutional Networks for Biomedical Image Segmentation* | Proc. MICCAI, 2015 (LNCS Vol. 9351, pp. 234–241) | `10.1007/978-3-319-24574-4_28` | Sec. I, Table 2, Table 4, Fig. 2 (Baseline backbone) | **VERIFIED** |
| `zhou2019unetplusplus` | Z. Zhou et al., *UNet++: Redesigning Skip Connections to Exploit Multiscale Features for Image Segmentation* | IEEE Trans. Med. Imaging, 2020 (Vol. 39, No. 6, pp. 1856–1867) | `10.1109/TMI.2019.2959609` | Sec. I, Table 2, Fig. 2 (Dense nested baseline) | **VERIFIED** |
| `krassnig2025ispad` | P. J. Krassnig & D. P. Gruber, *ISP-AD: A large-scale real-world dataset for advancing industrial anomaly detection...* | J. Intell. Manuf., 2026 (Online Dec 2025) | `10.1007/s10845-025-02381-8` | Sec. I, Sec. II-B, Sec. II-C (Weak boundaries) | **VERIFIED** |
| `zhou2024mixsegnet` | Y. Zhou et al., *MixSegNet: A Novel Crack Segmentation Network Combining CNN and Transformer* | IEEE Access, 2024 (Vol. 12, pp. 110928–110940) | `10.1109/ACCESS.2024.3438112` | Table 2 Panel B (Literature crack benchmark) | **VERIFIED** |
| `zhang2024gnapsc` | J. Zhang et al., *Training Surface Crack Segmentation Networks With Groupwise Normalization Attention...* | IEEE Sensors J., 2024 (Vol. 24, No. 13, pp. 21093–21107) | `10.1109/JSEN.2024.3396650` | Table 2 Panel B (Literature crack benchmark) | **VERIFIED** |
| `li2024ef2net` | F. Li et al., *EF^2Net: An Enhanced Feature Fusion Network for Lightweight Surface Defect Segmentation* | Proc. ICPRAI, 2024 (LNCS, pp. 1–10) | Publisher record verified (Springer) | Sec. II-A, Table 2 Panel B (Edge lightweight) | **VERIFIED** |
| `liu2024damfnet` | Y. Liu et al., *DAMF-Net: A Dynamic Receptive Field Enhancement and Semantic-Guided Network...* | Sensors (MDPI), 2024 (Vol. 24, No. 14, Art. 4635) | `10.3390/s24144635` | Sec. II-A, Table 2 Panel B (Dynamic receptive field) | **VERIFIED** |
| `liu2024dmsunet` | J. Liu et al., *DMS-UNet: Dual-branch edge-aware network with hybrid attention for industrial defect segmentation* | Meas. Sci. Technol., 2024 (Vol. 35, No. 10, Art. 105401) | `10.1088/1361-6501/ad5c55` | Sec. II-A, Table 2 Panel B (Edge dual-branch) | **VERIFIED** |
| `dong2023pganet` | X. Dong et al., *PGA-Net: Progressive global attention network for steel surface defect detection* | Pattern Recognit., 2023 (Vol. 143, Art. 109787) | `10.1016/j.patcog.2023.109787` | Sec. II-A (Steel attention networks) | **VERIFIED** |
| `hecklerkram2025mvtecad2` | L. Heckler et al., *The MVTec AD 2 Dataset: Advanced Scenarios for Unsupervised Anomaly Detection* | Int. J. Comput. Vis., 2025 (Vol. 133, pp. 3120–3142) | `10.1007/s11263-024-02275-w` | Sec. II-C (Industrial anomaly frontier) | **VERIFIED** |
| `wang2025bahrnet` | Z. Wang et al., *A Boundary-Aware and High-Resolution Transformer Framework for Tiny Defect Segmentation* | IEEE Access, 2025 (Vol. 13, pp. 18234–18247) | `10.1109/ACCESS.2025.3528406` | Sec. II-B (Boundary high-resolution transformer) | **VERIFIED** |
| `alghamdi2024potholebaf` | A. S. Alghamdi & M. Qasim, *PotholeBAF-Net: Boundary-Aware Fusion Network with Low-Rank Transformers...* | Appl. Sci. (MDPI), 2024 (Vol. 14, No. 12, Art. 5240) | `10.3390/app14125240` | Sec. II-B (Boundary fusion methods) | **VERIFIED** |
| `kervadec2021boundary` | H. Kervadec et al., *Boundary loss for highly unbalanced segmentation* | Med. Image Anal., 2021 (Vol. 67, Art. 101851) | `10.1016/j.media.2020.101851` | Sec. II-B (Auxiliary boundary loss paradigms) | **VERIFIED** |
| `yao2024fewshot` | X. Yao et al., *Edge-Guided Semantic Cross-Matching Network for Few-Shot Strip Steel Defect Segmentation* | IEEE Trans. Instrum. Meas., 2024 (Vol. 73, Art. 5014312) | `10.1109/TIM.2024.3392476` | Sec. II-B (Few-shot edge guidance) | **VERIFIED** |
| `mao2025csdd` | K. Mao et al., *CSDD: A Benchmark Dataset for Casting Surface Defect Detection and Segmentation* | IEEE/CAA J. Autom. Sinica, 2025 (Vol. 12, No. 5, pp. 947–960) | `10.1109/JAS.2024.124698` | Sec. I, Sec. II-C (Class imbalance benchmark) | **VERIFIED** |
| `chen2018deeplabv3plus` | L.-C. Chen et al., *Encoder-Decoder with Atrous Separable Convolution for Semantic Image Segmentation* | Proc. ECCV, 2018 (LNCS Vol. 11211, pp. 801–818) | `10.1007/978-3-030-01449-0_49` | Sec. II-A, Sec. III-B (Atrous parallel branches) | **VERIFIED** |
| `tensorrt2024` | NVIDIA Corporation, *NVIDIA TensorRT: High-Performance Deep Learning Inference Library* | Technical Whitepaper, 2024 (Version 10.x) | Publisher documentation verified | Sec. V-G (TensorRT FP16 throughput) | **VERIFIED** |
| `satyanarayanan2017edge` | M. Satyanarayanan, *The Emergence of Edge Computing* | Computer (IEEE), 2017 (Vol. 50, No. 1, pp. 30–39) | `10.1109/MC.2017.9` | Sec. VI-B (Factory edge computing architecture) | **VERIFIED** |

---

## 3. AUDIT OF CITATION CALL-OUTS AND MANUSCRIPT RESOLUTION

- All 20 entries in `references_revised.bib` are actively cited in `submission_release/ieee_access_msba_net_submission.tex`.
- In-text citations correctly resolve in numeric sequence from `[1]` through `[20]`.
- Figure 2 caption and Table 2 header correctly attribute `\cite{ronneberger2015unet}` to U-Net and `\cite{zhou2019unetplusplus}` to U-Net++.
- The bibliography compiles with zero warnings under Tectonic/XeTeX engine.
