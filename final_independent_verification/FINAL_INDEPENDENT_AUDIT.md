# FINAL INDEPENDENT AUDIT REPORT — IEEE ACCESS SUBMISSION GATE

**Manuscript Title:** MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation  
**Journal Target:** IEEE Access  
**Evaluation Date:** October 14, 2026  
**Auditor:** Independent Autonomous CV Research, PyTorch Auditor & LaTeX Specialist  
**Workspace:** `d:/scratch/3rs sem`  
**Authoritative Source:** `submission_release/ieee_access_msba_net_submission.tex`  
**Authoritative PDF:** `submission_release/ieee_access_msba_net_submission.pdf`  
**Authoritative Bibliography:** `submission_release/references_revised.bib`  
**Authoritative Archive:** `submission_release/ieee_access_msba_net_submission.zip`  

---

## 1. AUDIT MANDATE & INDEPENDENT VERIFICATION METHODOLOGY

This audit was conducted strictly against the physical source code, model checkpoints, training logs, and compiled PDF on disk. Prior audit summaries, claimed release gates, and recommendations were treated as unverified claims until confirmed by direct execution and cryptographic hashing.

### Audit Principles Enforced:
1. **Zero Fabrication:** No experimental metric, baseline score, variance number, or publication metadata was invented or assumed.
2. **Preservation of Research Record:** Original manuscript drafts (`ieee_access_msba_net.tex`, `references.bib`, `ieee_access_msba_net_final.tex`) and all 18 PyTorch model checkpoints were preserved unchanged. Rollback capability is 100% maintained.
3. **Strict Experimental Control:** Checkpoint substitutions between disparate training scripts were rejected. All reported numbers reflect protocol-matched evaluations on standardized, pre-cached static tensors.
4. **Honesty on Negative Findings:** MSBA-Net's observed disadvantages under low contrast (39.67% vs 50.26% for U-Net++) and optical blur (26.29% vs 39.12% for U-Net++) are faithfully reported and scientifically analyzed.

---

## 2. INDEPENDENT VERIFICATION FINDINGS ACROSS ALL CRITICAL PILLARS

### 2.1 Pillar A: Table 4 Architectural Progression & Protocol Reconciliation
- **Discrepancy Uncovered:** In earlier drafts, Table 4 combined Arch-1 and Arch-4 from `main.py` (95.33% and 97.01%) with Arch-2 and Arch-3 from `run_ablations.py` (95.50% and 95.92%), concealing the fact that the actual Arch-4 ablation checkpoint (`ablation_arch4_msba.pth`) attained 90.47% mIoU, while the Arch-1 ablation model reached 98.11% mIoU.
- **Rerun Evidence:** When retrained under strictly identical, pre-cached, zero-drift conditions (`scratch/reproduce_architectural_ablation.py` on RTX 5070 Ti GPU):
  - Arch-1 (U-Net Baseline): 96.94% mIoU (88.27% Tiny mIoU)
  - Arch-2 (Base + MSFP): 97.89% mIoU (93.18% Tiny mIoU — **+4.91 pp boost**)
  - Arch-3 (Base + MSFP + BAS): 98.31% mIoU (93.48% Tiny mIoU — **+5.21 pp boost**)
  - Arch-4 (Full MSBA-Net cold-start): 94.54% mIoU (92.98% Tiny mIoU)
- **Scientific Resolution:** Table 4 was restructured into Panel A (Controlled Factorial Ablation, reporting 94.54%) and Panel B (Converged Reference Models, reporting 97.01% nominal and $96.95\% \pm 1.36\%$ multi-seed). The cold-start gating drag is physically explained in Section V-C without concealing non-monotonic results.

### 2.2 Pillar B: Multi-Seed Statistical Reporting
- **Recalculation:** Direct evaluation of `msba_seed_42.pth` (98.14%), `msba_seed_100.pth` (95.46%), and `msba_seed_2026.pth` (97.25%) yields:
  - Mean mIoU: **96.95%**
  - Unbiased Sample Standard Deviation ($ddof=1$): **1.36 pp** (1.3650 pp)
  - Population Standard Deviation ($ddof=0$): **1.11 pp** (1.1145 pp)
  - Tiny Defect Mean ($<1\%$ area): **93.38%** ($s = 1.22\text{ pp}$)
- **Cross-File Harmonization:** The unbiased sample standard deviation convention ($96.95\% \pm 1.36\%$, $N=3$) is consistently used across the Abstract, Table 2, Table 4, results, discussion, and conclusion. Drifting sequential validation slice numbers ($97.33\% \pm 1.17\%$) have been completely removed.

### 2.3 Pillar C: Dataset Provenance & Claim Boundary
- **Code Audit of `dataset.py`:** Confirmed that `IndustrialDefectDataset` procedurally synthesizes metallic background grain and defect patterns modeled after the NEU database. It does not load physical factory camera photographs.
- **Textual Audit:** All claims of "real-world factory validation" or "production-line deployment" have been removed. The synthetic-to-real domain gap is explicitly disclosed in Section V-A and Section VII.
- **Negative Findings:** MSBA-Net's low-contrast disadvantage (39.67% mIoU) and motion-blur disadvantage (26.29% mIoU) are faithfully reported, and the requirement for plant-level engineering controls (pulsed strobe lighting, air-knife oil mist barriers) is explicitly detailed.

### 2.4 Pillar D: Bibliography and Baseline Citations
- **Attributions Corrected:** U-Net is cited as Ronneberger et al. (*MICCAI 2015*, `ronneberger2015unet`), and U-Net++ is cited as Zhou et al. (*IEEE TMI 2020*, `zhou2019unetplusplus`). Song & Yan (2013) is restricted to the NEU defect morphology survey.
- **Citation Completeness:** 100% of the 20 bibliography entries in `references_revised.bib` are actively cited in the manuscript text (0 uncited, 0 missing).
- **Metadata Compliance:** Retracted the placeholder string `10.1109/ACCESS.2026.MSBANET` and restored official template macro `\doi{10.1109/ACCESS.2017.DOI}`.

### 2.5 Pillar E: Submission Package & Standalone Compilation
- **Archive Cleanliness:** `submission_release/ieee_access_msba_net_submission.zip` contains exactly 12 required files (source, PDF, bib, class styles, template logos, and 4 high-resolution figures). Zero private checkpoints or temporary logs are present.
- **Clean Isolated Compilation:** Extraction into an isolated directory (`scratch/clean_zip_verify/`) and compilation via `tools/tectonic.exe` completed with **Exit Code 0**, generating an exact **8-page PDF** with zero unresolved citations (`[?]`) and zero undefined cross-references (`??`).

---

## 3. AUDIT SUMMARY TABLE OF ARTIFACTS

| Authoritative File | Size (Bytes) | SHA-256 Checksum | Verification Status |
| :--- | :---: | :--- | :---: |
| `submission_release/ieee_access_msba_net_submission.tex` | 41,844 | `f0032efe999014d76d53343c790f3f099330e71844aa506cd2d69d49f21a3840` | **VERIFIED** |
| `submission_release/ieee_access_msba_net_submission.pdf` | 1,321,517 | `5dbad96976828f509c1a064d022e09179dfc158435b815cd3677d110d18f079b` | **VERIFIED (8 Pages)** |
| `submission_release/references_revised.bib` | 6,890 | `6042b9ff9150b1e6dfccbfe2c2413dacb5da9d05e3042c5ce6b6236080e28e7e` | **VERIFIED (20 Entries)** |
| `submission_release/ieee_access_msba_net_submission.zip` | 2,503,082 | `6493296a823f4b081460e88c4efbc7fdfc863b914167796feee0636e6e74affc` | **VERIFIED (Tested Clean)** |
