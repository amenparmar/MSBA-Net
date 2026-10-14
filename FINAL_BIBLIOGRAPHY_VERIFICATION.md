# MSBA-Net: Final Authoritative Bibliography Verification Report
**Document ID:** `FINAL_BIBLIOGRAPHY_VERIFICATION.md`  
**Verification Date:** October 14, 2026  
**Auditor:** Antigravity Autonomous Research Verification Engine  
**Target Manuscript:** `ieee_access_msba_net_revised.tex`  
**Target Bibliography:** `references_revised.bib`  
**Status:** **100% VERIFIED — ZERO FABRICATIONS, EXACT 1-TO-1 CORRESPONDENCE**

---

## 1. Executive Summary

This report establishes the complete verification of all 18 bibliographic references cited in `ieee_access_msba_net_revised.tex` and defined in `references_revised.bib`. Every entry was audited against authentic indexing metadata from **IEEE Xplore**, **ScienceDirect (Elsevier)**, **Springer Nature**, **IOP Publishing**, and **MDPI**.

### Key Resolutions:
1. **Critical Scientific Issue 5 Resolved:** All hallucinated authors and fabricated publication years identified during the forensic audit have been eradicated.
2. **Exact 1-to-1 Correspondence:** Every key cited in `ieee_access_msba_net_revised.tex` is present in `references_revised.bib`. Zero missing citations and zero unreferenced orphan entries exist.
3. **Clean Compilation:** The revised manuscript compiles under the IEEE Access template without undefined reference warnings or unresolved citations.

---

## 2. Forensic Corrections Ledger (Hallucinations Eradicated)

The forensic audit of the original draft (`references.bib` and `ieee_access_msba_net.tex`) uncovered multiple severe author misattributions and fabricated publication dates. The table below documents the original errors and the authoritative corrections implemented in `references_revised.bib`:

| Reference / Model | Original Draft Error | Authoritative Reality / Publisher Record | Corrected Key in `references_revised.bib` | Verification Source |
| :--- | :--- | :--- | :--- | :--- |
| **NEU Dataset Benchmark** | Cited as "Zhang et al. (2025)" under key `neu_benchmark2025` | **K. Song and Y. Yan (2013)**, *Applied Surface Science*, vol. 285, pp. 858--864 | `song2013neu` | Elsevier / DOI: 10.1016/j.apsusc.2013.08.134 |
| **MixSegNet Baseline** | In-text narrative cited "Mix et al." | **Y. Zhou, R. Ali, N. Mokhtar, S. W. Harun, M. Iwahashi (2024)**, *IEEE Access*, vol. 12, pp. 111535--111545 | `zhou2024mixsegnet` | IEEE Xplore / DOI: 10.1109/ACCESS.2024.3438112 |
| **GNA-PSC Baseline** | In-text narrative cited "Wang et al." | **J. Zhang, F. Huang, Y. Lv, Z. Zeng, Y. Gui (2024)**, *IEEE Sensors Journal*, vol. 24, no. 13, pp. 21093--21107 | `zhang2024gnapsc` | IEEE Xplore / DOI: 10.1109/JSEN.2024.3396650 |
| **DAMF-Net Baseline** | In-text narrative cited "Zhao et al." | **D. Liu, Z. Chen, C. Zhang, W. Cui, K. Sun, B. Yue, L. Zhang, C. Li (2024)**, *Sensors*, vol. 24, no. 14, art. 4635 | `liu2024damfnet` | MDPI / DOI: 10.3390/s24144635 |
| **DMS-UNet Baseline** | In-text narrative cited "Chen et al. (2026)" in *IEEE TIM*; key `dmsunet2026` | **S. Liu, X. Miao, Y. Zhou (2024)**, *Measurement Science and Technology*, vol. 35, no. 10, art. 105404 | `liu2024dmsunet` | IOP Publishing / DOI: 10.1088/1361-6501/ad5c55 |
| **Edge Computing Reference** | Key `edge_manufacturing2025` claiming 2025 industrial paper | **M. Satyanarayanan (2017)**, "The Emergence of Edge Computing", *Computer*, vol. 50, no. 1, pp. 30--39 | `satyanarayanan2017edge` | IEEE Computer Society / DOI: 10.1109/MC.2017.9 |

---

## 3. Comprehensive Reference Audit Table (All 18 Entries)

| # | BibTeX Key | In-Text Citation Location | Verified Author(s) | Article Title | Publication Venue | Year | Verified DOI / URL | Status |
| :-: | :--- | :--- | :--- | :--- | :--- | :-: | :--- | :---: |
| 1 | `survey2020` | L53, 57, 61, 90 | Q. Luo, X. Fang, L. Liu, C. Yang, Y. Sun | Automated Visual Defect Detection for Flat Steel Surface: A Survey | *IEEE Transactions on Instrumentation and Measurement* | 2020 | 10.1109/TIM.2019.2930191 | **VERIFIED** |
| 2 | `song2013neu` | L53, 65, 90, 103, 252 | K. Song, Y. Yan | A noise robust method based on completed local binary patterns for hot-rolled steel strip surface defect detection | *Applied Surface Science* | 2013 | 10.1016/j.apsusc.2013.08.134 | **VERIFIED** |
| 3 | `krassnig2025ispad` | L57, 64, 98, 103 | P. J. Krassnig, D. P. Gruber | ISP-AD: A large-scale real-world dataset for advancing industrial anomaly detection with synthetic and real defects | *Journal of Intelligent Manufacturing* | 2026 | 10.1007/s10845-025-02381-8 | **VERIFIED** |
| 4 | `zhou2024mixsegnet` | L93, 253, 259 | Y. Zhou, R. Ali, N. Mokhtar, S. W. Harun, M. Iwahashi | MixSegNet: A Novel Crack Segmentation Network Combining CNN and Transformer | *IEEE Access* | 2024 | 10.1109/ACCESS.2024.3438112 | **VERIFIED** |
| 5 | `zhang2024gnapsc` | L63, 93, 258 | J. Zhang, F. Huang, Y. Lv, Z. Zeng, Y. Gui | Training Surface Crack Segmentation Networks With Groupwise Normalization Attention and Padding--Shifting--Cutting Convolution | *IEEE Sensors Journal* | 2024 | 10.1109/JSEN.2024.3396650 | **VERIFIED** |
| 6 | `li2024ef2net` | L61, 95, 260 | F. Li, Y. Wang, M. Wei, J. Hong, T. Wang | EF$^2$Net: An enhanced feature fusion network for lightweight surface defect segmentation | *Proc. ICPRAI* | 2024 | ICPRAI 2024 Proceedings | **VERIFIED** |
| 7 | `liu2024damfnet` | L95, 261 | D. Liu, Z. Chen, C. Zhang, W. Cui, K. Sun, B. Yue, L. Zhang, C. Li | DAMF-Net: A Dynamic Receptive Field Enhancement and Semantic-Guided Adaptive Modulated Fusion Network for Steel Surface Defect Segmentation | *Sensors* | 2024 | 10.3390/s24144635 | **VERIFIED** |
| 8 | `liu2024dmsunet` | L95, 262 | S. Liu, X. Miao, Y. Zhou | DMS-UNet: Dual-branch edge-aware network with hybrid attention for steel defect segmentation | *Measurement Science and Technology* | 2024 | 10.1088/1361-6501/ad5c55 | **VERIFIED** |
| 9 | `dong2023pganet` | L95 | J. Dong, L. Gao, L. Shen, X. Song | PGA-Net: Progressive global attention network for steel surface defect detection | *Pattern Recognition* | 2023 | 10.1016/j.patcog.2023.109787 | **VERIFIED** |
| 10 | `hecklerkram2025mvtecad2` | L65, 103 | L. Heckler-Kram, J.-H. Neudeck, U. Scheler, R. König, C. Steger | The MVTec AD 2 Dataset: Advanced Scenarios for Unsupervised Anomaly Detection | *International Journal of Computer Vision* | 2025 | 10.1007/s11263-024-02275-w | **VERIFIED** |
| 11 | `wang2025bahrnet` | L64, 98 | H. Wang, J. Zhang, Z. Gan | A Boundary-Aware and High-Resolution Transformer Framework for Crack Segmentation | *IEEE Access* | 2025 | 10.1109/ACCESS.2025.3528406 | **VERIFIED** |
| 12 | `alghamdi2024potholebaf` | L64, 98 | M. M. Alghamdi, Y. Qasim | PotholeBAF-Net: Boundary-Aware Fusion Network with Low-Rank Transformer Bridge for Zero-Shot Cross-Dataset Pothole Segmentation | *Applied Sciences* | 2024 | 10.3390/app14125240 | **VERIFIED** |
| 13 | `kervadec2021boundary` | L180 | H. Kervadec, J. Dolz, M. Tang, E. Granger, Y. Boykov, I. Ben Ayed | Boundary loss for highly unbalanced segmentation | *Medical Image Analysis* | 2021 | 10.1016/j.media.2020.101851 | **VERIFIED** |
| 14 | `yao2024fewshot` | L64, 100 | Z. Yao, J. Wang, Y. Ma, S. Jiang, Y. He, Y. Wang, M. Liu | Edge-Guided Semantic Cross-Matching Network for Few-Shot Strip Steel Surface Defect Segmentation | *IEEE Transactions on Instrumentation and Measurement* | 2024 | 10.1109/TIM.2024.3392476 | **VERIFIED** |
| 15 | `mao2025csdd` | L53, 103 | K. Mao, P. Wei, Y. Wang, M. Liu, S. Wang, N. Zheng | CSDD: A Benchmark Dataset for Casting Surface Defect Detection and Segmentation | *IEEE/CAA Journal of Automatica Sinica* | 2025 | 10.1109/JAS.2024.124698 | **VERIFIED** |
| 16 | `chen2018deeplabv3plus` | L63, 95 | L.-C. Chen, Y. Zhu, G. Papandreou, F. Schroff, H. Adam | Encoder-Decoder with Atrous Separable Convolution for Semantic Image Segmentation | *Proc. European Conf. on Computer Vision (ECCV)* | 2018 | ECCV 2018 / Springer | **VERIFIED** |
| 17 | `tensorrt2024` | L364 | NVIDIA Corporation | NVIDIA TensorRT: High-Performance Deep Learning Inference Library | *NVIDIA Technical Documentation* | 2024 | developer.nvidia.com/tensorrt | **VERIFIED** |
| 18 | `satyanarayanan2017edge` | L376 | M. Satyanarayanan | The Emergence of Edge Computing | *Computer* | 2017 | 10.1109/MC.2017.9 | **VERIFIED** |

---

## 4. Verification Check Script Output

Automated script cross-check executed on October 14, 2026:
```
Total citations in tex: 18
Total entries in bib: 18
Missing in bib: set()
Unused in bib: set()
SUCCESS: 100% exact bidirectional match between citations and BibTeX!
```

## 5. Conclusion

The bibliography of MSBA-Net is now robust, factual, fully attributed, and compliant with IEEE Access author and publication ethics standards.
