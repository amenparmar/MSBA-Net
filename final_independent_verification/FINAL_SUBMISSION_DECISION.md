# FINAL SUBMISSION DECISION — IEEE ACCESS SUBMISSION GATE

**Manuscript Title:** MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation  
**Journal Target:** IEEE Access  
**Evaluation Date:** October 14, 2026  
**Auditor:** Independent Autonomous CV Research, PyTorch Auditor & LaTeX Specialist  

---

## FINAL DECISION: **SUBMIT**

All material scientific, experimental, architectural, statistical, bibliographic, and submission-packaging requirements have been independently verified against the physical code, checkpoints, and logs on disk. Zero material discrepancies remain unresolved.

---

## 1. CRITICAL AUDIT CRITERIA & EVIDENCE SUMMARY

### 1.1 Architectural Ablation Integrity (Table 4)
- **Status:** **RESOLVED & VERIFIED**
- **Evidence:** The historical conflation between `main.py` and `run_ablations.py` has been eliminated. Table 4 is structured into two strictly controlled panels:
  - **Panel A (Controlled Factorial Ablation):** Arch-1 (96.94%), Arch-2 (97.89%, +4.91 pp on tiny flaws), Arch-3 (98.31%), and Arch-4 cold-start (94.54%).
  - **Panel B (Converged Reference Models):** Nominal MSBA-Net (97.01%) and Multi-Seed Mean ($96.95\% \pm 1.36\%$).
- No cherry-picking, no hidden negative results, and no fabricated monotonic progression.

### 1.2 Multi-Seed Statistical Reporting
- **Status:** **RESOLVED & VERIFIED**
- **Evidence:** Protocol-matched three-seed mean of **96.95% mIoU** with unbiased sample standard deviation (**$\pm 1.36\text{ pp}$**, $N=3, ddof=1$) is reported consistently across the Abstract, Table 2, Table 4, results, discussion, and conclusion. Population standard deviation ($\pm 1.11\text{ pp}$) is explicitly documented where comparative convention is discussed. Drifting sequential validation slice artifacts ($97.33\% \pm 1.17\%$) have been completely removed.

### 1.3 Synthetic Benchmark & Claim Scoping
- **Status:** **RESOLVED & VERIFIED**
- **Evidence:** Procedural synthetic nature of `IndustrialDefectDataset` is plainly disclosed in Section V-A and Section VII. All claims of physical factory camera photographs or production-line deployment have been excised. Negative findings under low contrast (39.67% mIoU) and optical blur (26.29% mIoU) are faithfully reported, and plant-level engineering controls (pulsed strobe lighting, air-knife oil mist barriers) are specified.

### 1.4 Bibliographic & Template Compliance
- **Status:** **RESOLVED & VERIFIED**
- **Evidence:** Original U-Net (Ronneberger et al., *MICCAI 2015*) and U-Net++ (Zhou et al., *IEEE TMI 2020*) citations verified. 100% of the 20 bibliography entries in `references_revised.bib` are actively cited in the text (0 uncited, 0 missing). Placeholder string `10.1109/ACCESS.2026.MSBANET` retracted and restored to official submission placeholder `\doi{10.1109/ACCESS.2017.DOI}`.

### 1.5 Submission Archive & Standalone Compilation
- **Status:** **RESOLVED & VERIFIED**
- **Evidence:** `submission_release/ieee_access_msba_net_submission.zip` contains exactly 12 necessary source files, figures, styles, and bibliography with zero internal checkpoint or log contamination. Extraction into an isolated directory and fresh compilation via `tools/tectonic.exe` completed with **Exit Code 0**, producing an exact **8-page camera-ready PDF** with zero unresolved citations (`[?]`) and zero undefined cross-references (`??`).

---

## 2. AUTHORITATIVE SUBMISSION ARTIFACTS

| Artifact | Location | Size | SHA-256 Checksum |
| :--- | :--- | :---: | :--- |
| **LaTeX Source** | `submission_release/ieee_access_msba_net_submission.tex` | 41,844 bytes | `f0032efe999014d76d53343c790f3f099330e71844aa506cd2d69d49f21a3840` |
| **Compiled PDF** | `submission_release/ieee_access_msba_net_submission.pdf` | 1,321,517 bytes | `5dbad96976828f509c1a064d022e09179dfc158435b815cd3677d110d18f079b` |
| **Bibliography** | `submission_release/references_revised.bib` | 6,890 bytes | `6042b9ff9150b1e6dfccbfe2c2413dacb5da9d05e3042c5ce6b6236080e28e7e` |
| **Submission ZIP** | `submission_release/ieee_access_msba_net_submission.zip` | 2,503,082 bytes | `6493296a823f4b081460e88c4efbc7fdfc863b914167796feee0636e6e74affc` |

---

## 3. FINAL ACTION FOR THE CORRESPONDING AUTHOR

The submission package is mathematically, experimentally, and bibliographically defensible. The corresponding author may proceed immediately to upload:
$$\mathbf{submission\_release/ieee\_access\_msba\_net\_submission.zip}$$
to the *IEEE Access* ScholarOne Manuscripts portal.
