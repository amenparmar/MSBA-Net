# FINAL MANUSCRIPT CHANGELOG: AUDIT & SUBMISSION REVISION

**Document:** `submission_release/FINAL_MANUSCRIPT_CHANGELOG.md`  
**Manuscript Target:** IEEE Access  
**Base Document:** `ieee_access_msba_net_final.tex` (SHA-256: `0dfa8769f549bbbb...`)  
**Submission Document:** `ieee_access_msba_net_submission.tex`  
**Audit Date:** October 14, 2026  
**Auditor:** Antigravity Autonomous Scientific Editing & Forensic Audit Team  

---

## 1. SUMMARY OF REVISIONS

| Change ID | Location in Manuscript | Previous State / Draft Value | Revised Submission State | Scientific Rationale & Regulatory Basis |
| :---: | :--- | :--- | :--- | :--- |
| **CHG-01** | Preamble (Line 23) | `\doi{10.1109/ACCESS.2026.MSBANET}` | `\doi{10.1109/ACCESS.2017.DOI}` | **DOI Retraction:** Authors cannot invent or assign DOIs. Retracted fabricated string and restored official IEEE Access submission placeholder. |
| **CHG-02** | Abstract (Line 40) | `$96.95\% \pm 1.11\%$ mIoU` | `$96.95\% \pm 1.36\%$ mIoU` | **Statistical Reporting Standardization:** Replaced population standard deviation ($\sigma=\pm 1.11\%$) with unbiased sample standard deviation ($s=\pm 1.36\%$, $N=3$, $ddof=1$). |
| **CHG-03** | Figure 2 Caption (Line 197)| `(c) U-Net baseline [MICCAI'15], (d) U-Net++ baseline [IEEE TMI'18]` | `(c) U-Net baseline \cite{ronneberger2015unet}, (d) U-Net++ baseline \cite{zhou2019unetplusplus}` | **Baseline Citation Correction:** Converted plain-text strings into verified formal bibliographic citations. |
| **CHG-04** | Table 2 Panel A (Line 253) | `U-Net Baseline \cite{song2013neu}` | `U-Net Baseline \cite{ronneberger2015unet}` | **Baseline Attribution Correction:** Song & Yan (2013) is the NEU dataset paper, not U-Net. Cites original Ronneberger et al. (MICCAI 2015). |
| **CHG-05** | Table 2 Panel A (Line 254) | `U-Net++ \cite{zhou2024mixsegnet}` | `U-Net++ \cite{zhou2019unetplusplus}` | **Baseline Attribution Correction:** MixSegNet (2024) is a crack transformer, not U-Net++. Cites original Zhou et al. (IEEE TMI 2020 / DLMIA 2018). |
| **CHG-06** | Table 2 Panel A (Line 256) | `Mean \pm Std ($N=3$): 96.95 \pm 1.11` | `Mean \pm Sample Std ($N=3$): 96.95 \pm 1.36` | **Statistical Reporting Standardization:** Updated Table 2 multi-seed aggregate to sample standard deviation ($96.95\% \pm 1.36\%$). |
| **CHG-07** | Table 4 (Line 312) | `Arch-1: Baseline (U-Net)` | `Arch-1: Baseline U-Net \cite{ronneberger2015unet}` | **Citation Completeness:** Added formal citation to baseline row in architectural ablation table. |
| **CHG-08** | Table 4 (Line 316) | `Multi-Seed ($N=3$): 96.95 \pm 1.11` | `Multi-Seed ($N=3$): 96.95 \pm 1.36` | **Statistical Harmonization:** Aligned Table 4 multi-seed entry to sample standard deviation. |
| **CHG-09** | Section V.D (Line 321) | Discussed 96.95% without reproduction disclosure | Added reproduction findings (88.27% to 93.18% Tiny mIoU; gating hesitation discussion) | **Reproduction Disclosure:** Added empirical verification details from zero-drift reproduction run (`ARCHITECTURAL_ABLATION_REPRODUCED.csv`). |
| **CHG-10** | Conclusion (Line 379) | `$96.95\% \pm 1.11\%$ across seeds` | `$96.95\% \pm 1.36\%$ across seeds` | **Global Consistency:** Synchronized conclusion statistical reporting with abstract and tables. |
| **CHG-11** | `references_revised.bib` | Missing original U-Net and U-Net++ entries | Added `ronneberger2015unet` and `zhou2019unetplusplus` | **Bibliography Expansion:** Added 2 verified entries (total: 20 references), 100% bidirectional citation resolution. |

---

## 2. PRESERVATION OF ROLLBACK CAPABILITY

- Original uncorrected source `ieee_access_msba_net.tex` and `references.bib` are frozen in the workspace root and `original_backup/`.
- Prior working revision `ieee_access_msba_net_final.tex` and `ieee_access_msba_net_final.pdf` remain completely intact.
- The new release candidate is isolated in `ieee_access_msba_net_submission.tex` and mirrored in `submission_release/`.
