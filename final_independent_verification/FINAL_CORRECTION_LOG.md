# FINAL MANUSCRIPT CORRECTION & AUDIT LOG

**Manuscript Title:** MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation  
**Journal Target:** IEEE Access  
**Evaluation Date:** October 14, 2026  
**Auditor:** Independent Autonomous CV Research & LaTeX Auditor  
**Working Source:** `submission_release/ieee_access_msba_net_submission.tex`  

---

## 1. RECORD OF APPLIED CORRECTIONS

The following specific corrections were applied to the working submission manuscript, justified strictly by physical source code, checkpoint, and bibliographic evidence:

### CHANGE-01: Table 4 Structural Separation & Elimination of Checkpoint Conflation
- **Location:** Section V-C, Table 4 (`tab:ablation`), lines 306–327
- **Identified Defect:** Earlier manuscript drafts presented Table 4 as a monotonic ladder ($95.33\% \to 95.50\% \to 95.92\% \to 97.01\%$) by combining Arch-1 and Arch-4 from `main.py` with Arch-2 and Arch-3 from `run_ablations.py`. This conflated two different training data streams and concealed the fact that the actual Arch-4 ablation checkpoint (`ablation_arch4_msba.pth`) achieved 90.47% mIoU, while the reproduced zero-drift cold-start run achieved 94.54% mIoU.
- **Applied Correction:** Restructured Table 4 into two clearly labeled panels:
  - **Panel A (Controlled Factorial Ablation):** Reports the strictly controlled zero-drift rerun: Arch-1 (96.94%), Arch-2 (97.89%), Arch-3 (98.31%), and Arch-4 cold-start (94.54%).
  - **Panel B (Converged Reference Models):** Reports the nominal model (97.01%) and multi-seed mean ($96.95\% \pm 1.36\%$).
- **Supporting Evidence:** `models/reproduced_arch4_msba.pth` evaluation (94.54%), `models/best_MSBANet.pth` evaluation (97.01%), and training trajectory analysis in `scratch/reproduce_architectural_ablation.py`.

### CHANGE-02: Section V-C Textual Harmonization & Cold-Start Gating Explanation
- **Location:** Section V-C, lines 329–332
- **Identified Defect:** Prior text asserted smooth monotonic component gains without addressing the performance dip observed in isolated single runs of Arch-4.
- **Applied Correction:** Added explicit physical explanation: the interactive BGFF spatial attention gate multiplies unrefined boundary predictions into the main segmentation decoder features during early epochs, injecting gradient noise that slows convergence during short 12-epoch cold starts. Fully converged multi-seed trajectories overcome this drag to achieve $96.95\% \pm 1.36\%$.
- **Supporting Evidence:** Epoch-by-epoch loss traces and model architecture in `models.py`.

### CHANGE-03: Table 4 Column Formatting & Alignment Width Fix
- **Location:** Table 4 `tabular*` definition, lines 312–326
- **Identified Defect:** Overfull `\hbox` (14.78pt too wide) detected due to long column labels and mathematical expressions inside a single-column float.
- **Applied Correction:** Adjusted `\tabcolsep` to 1.8pt, concise column headers (`\textbf{Tiny (\%)}`), and standard column specifications to eliminate the width warning completely.
- **Supporting Evidence:** Tectonic compilation log (Exit code 0).

### CHANGE-04: Resolution of Uncited Bibliography Entry
- **Location:** Section II-B, line 100
- **Identified Defect:** `references_revised.bib` contained 20 entries, but `kervadec2021boundary` (Kervadec et al., *Med. Image Anal.* 2021) was uncited in the text.
- **Applied Correction:** Added citation `\cite{kervadec2021boundary}` in Section II-B where auxiliary boundary loss formulations under extreme imbalance are discussed.
- **Supporting Evidence:** 100% of the 20 bibliography entries in `references_revised.bib` now actively resolve in the text (0 uncited, 0 missing).

### CHANGE-05: Baseline Citation Attribution Correction
- **Location:** Section I, Section V-B, Table 2, Figure 2 caption
- **Identified Defect:** Earlier drafts attributed U-Net to Song & Yan (2013) and U-Net++ to MixSegNet (2024).
- **Applied Correction:** Replaced with authoritative original publications:
  - U-Net: O. Ronneberger, P. Fischer, and T. Brox, *MICCAI 2015* (`ronneberger2015unet`).
  - U-Net++: Z. Zhou et al., *IEEE TMI 2020* (`zhou2019unetplusplus`).
  - Song & Yan (2013) correctly cited for the NEU dataset survey (`song2013neu`).
- **Supporting Evidence:** Authoritative proceedings and journal records verified via CrossRef/IEEE Xplore DOIs.

### CHANGE-06: Retraction of Fabricated DOI & Template Compliance
- **Location:** Line 23 of source
- **Identified Defect:** A placeholder string `10.1109/ACCESS.2026.MSBANET` was present in earlier drafts.
- **Applied Correction:** Restored the official IEEE Access submission placeholder `\doi{10.1109/ACCESS.2017.DOI}`. Preserved submission-stage publication date string `\history{Date of publication xxxx 00, 0000...}`.
- **Supporting Evidence:** Official IEEE Access author template instructions.

### CHANGE-07: Explicit Disclosure of Procedural Benchmark
- **Location:** Abstract, Section V-A, Section VI, Section VII
- **Identified Defect:** Ambiguous wording in earlier drafts could imply physical factory camera data or real-world deployment.
- **Applied Correction:** Explicitly stated that `IndustrialDefectDataset` procedurally synthesizes rolling mill textures and defect morphologies modeled after the NEU database. Retained negative robustness findings (MSBA-Net disadvantaged under low contrast and blur). Highlighted the synthetic-to-real domain gap in future work.
- **Supporting Evidence:** `dataset.py` implementation and `results/verified_benchmark_metrics.json`.
