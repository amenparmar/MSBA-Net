# SUBMISSION PACKAGE INTEGRITY & COMPILATION AUDIT REPORT

**Manuscript Title:** MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation  
**Journal Target:** IEEE Access  
**Evaluation Date:** October 14, 2026  
**Auditor:** Independent Autonomous CV Research & LaTeX Auditor  
**Submission Package:** `submission_release/ieee_access_msba_net_submission.zip`  

---

## 1. ARCHIVE CONTENTS & CLEANLINESS AUDIT

The submission archive `submission_release/ieee_access_msba_net_submission.zip` was inspected to verify that it contains all necessary source files, figures, styles, and bibliography for independent compilation, while strictly omitting internal scratch scripts, PyTorch model checkpoints, or audit logs:

| File Path in ZIP | Size (Bytes) | Compressed Size | Function / Category | Audit Status |
| :--- | :---: | :---: | :--- | :---: |
| `ieee_access_msba_net_submission.tex` | 41,844 | 13,959 | Primary LaTeX Source | **VERIFIED** |
| `ieee_access_msba_net_submission.pdf` | 1,321,517 | 1,220,105 | Authoritative Reference PDF | **VERIFIED** |
| `references_revised.bib` | 6,890 | 2,597 | Verified BibTeX Bibliography | **VERIFIED** |
| `ieeeaccess.cls` | 42,974 | 8,504 | Official IEEE Access Document Class | **VERIFIED** |
| `IEEEtran.cls` | 281,957 | 68,203 | IEEE Bibliography Style / Trans Class | **VERIFIED** |
| `bullet.png` | 430 | 435 | IEEE Access Template Layout Graphic | **VERIFIED** |
| `Logo.png` | 9,705 | 9,701 | IEEE Access Header Banner Graphic | **VERIFIED** |
| `notaglineLogo.png` | 3,150 | 3,117 | IEEE Access Secondary Graphic | **VERIFIED** |
| `figures/fig1_architecture.png` | 541,875 | 513,675 | Figure 1: Architectural Schematic | **VERIFIED** |
| `figures/fig2_visual_comparison.png` | 337,084 | 302,464 | Figure 2: Visual Comparison (3x zoom) | **VERIFIED** |
| `figures/fig3_loss_curves.png` | 230,289 | 217,754 | Figure 3: Convergence Dynamics | **VERIFIED** |
| `figures/fig4_degraded_benchmark.png` | 153,751 | 141,067 | Figure 4: Degradation Benchmark | **VERIFIED** |

- **Total Uncompressed Size:** 2,971,466 bytes
- **Total Compressed ZIP Size:** 2,503,082 bytes
- **Contamination Check:** Passed. Zero `.pth` checkpoint files, zero scratch scripts, zero `.log` or `.aux` files included.

---

## 2. INDEPENDENT CLEAN COMPILATION TEST

### Test Execution
1. Extracted `submission_release/ieee_access_msba_net_submission.zip` into an isolated clean directory: `scratch/clean_zip_verify/`.
2. Removed the packaged PDF `ieee_access_msba_net_submission.pdf` to ensure the compilation was performed 100% from source files.
3. Executed compilation using `tools/tectonic.exe`:
   ```bash
   tools/tectonic.exe ieee_access_msba_net_submission.tex
   ```

### Compilation Results
- **Exit Code:** `0` (Success)
- **Document Length:** Exactly **8 pages**
- **Undefined Citations (`[?]`):** `0`
- **Undefined Cross-References (`??`):** `0`
- **Overfull / Underfull Table Alignment Errors:** `0`
- **Figure Ingestion:** All four figures successfully rendered into pages 2, 5, 7, and 7.

---

## 3. FRESH FILE CHECKSUMS (SHA-256)

| Authoritative File | Size (Bytes) | SHA-256 Checksum |
| :--- | :---: | :--- |
| `submission_release/ieee_access_msba_net_submission.tex` | 41,844 | `f0032efe999014d76d53343c790f3f099330e71844aa506cd2d69d49f21a3840` |
| `submission_release/ieee_access_msba_net_submission.pdf` | 1,321,517 | `5dbad96976828f509c1a064d022e09179dfc158435b815cd3677d110d18f079b` |
| `submission_release/references_revised.bib` | 6,890 | `6042b9ff9150b1e6dfccbfe2c2413dacb5da9d05e3042c5ce6b6236080e28e7e` |
| `submission_release/ieee_access_msba_net_submission.zip` | 2,503,082 | `6493296a823f4b081460e88c4efbc7fdfc863b914167796feee0636e6e74affc` |
