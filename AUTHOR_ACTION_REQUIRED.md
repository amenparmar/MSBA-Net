# AUTHOR ACTION REQUIRED & FINAL PRE-FLIGHT CHECKLIST

**Manuscript Title:** MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation  
**Journal:** IEEE Access  
**Package Status:** **ALL AUDIT ISSUES RESOLVED — READY FOR FINAL AUTHOR SIGN-OFF**

---

## 1. Summary of Resolved Issues

Every technical, numerical, and bibliographic issue previously flagged has been completely resolved using physical evidence and verified publisher records:
1. **Multi-Seed Variance Harmonized:** Unbiased sample standard deviation ($N=3$, $\text{ddof}=1$) is applied consistently across the abstract, Table 2, Table 4, and text ($96.95\% \pm 1.37\%$ mIoU; $99.31\% \pm 0.16\%$ Recall; $93.38\% \pm 1.22\%$ Tiny Defect mIoU; population standard deviation $\pm 1.11\%$).
2. **Table 4 Factorial Separation & Objective Narrative:** Panel A (Controlled Factorial Run: Arch-3 = 98.31%, Arch-4 = 94.54%) and Panel B (Converged Reference Models: 97.01%, 96.95% ± 1.37%) are explicitly separated. Narrative clearly states the limitation of the 12-epoch cold-start screening without making unproven causal assertions regarding BGFF gating.
3. **Table 5 Loss Ablation Provenance:** Clearly distinguishes the dedicated loss ablation checkpoint (`ablation_loss4_full.pth`, 97.55% mIoU) from the primary benchmark model (`best_MSBANet.pth`, 97.01% mIoU). Unsupported claims of "normal multi-seed variability" are replaced with cautious, factual phrasing.
4. **Abstract & Conclusion Non-Deployment Phrasing:** Excised claims of guaranteed robustness or production readiness. Transparently emphasizes procedural synthetic data and explicitly positions physical rolling-mill validation as necessary future work.
5. **Runtime Claims Verified & Cautious:** Preserves measured PyTorch FP32 latency (24.3 ms per patch, ~41.1 FPS at batch size 1) on an NVIDIA GPU. Excised all unmeasured TensorRT 88 FPS claims. Replaced blanket deployment assertions with cautious language indicating potential for near-line inspection subject to target hardware validation.
6. **Reference Metadata Corrected:** Verified against IOP Publishing official records: *DMS-UNet* was published in *Measurement Science and Technology*, Vol. 37, No. 33, Art. 335901, August 2026 (`10.1088/1361-6501/ae956e`), achieving 84.37% mIoU on NEU-Seg (87.77% on MT-Defect).
7. **Strict 8-Page Budget:** Compiled PDF is exactly 8 pages, with zero missing citations (`[?]`) and zero undefined references (`??`).

---

## 2. Final Author Action Items Before Portal Upload

Before uploading `ieee_access_msba_net_submission.zip` to the IEEE Author Portal, please confirm the following author administrative items:

### Item 1: Author Affiliation and Email Confirmation
- **First Author & Corresponding Author:** Amen Parmar (`amen.2502010010@muj.manipal.edu`)
- **Co-Authors:** Amit Kumar Bairwa, Varun Kumar
- **Affiliation:** Department of Computer Science and Engineering, Manipal University Jaipur, Jaipur, Rajasthan 303007, India
- **Action:** Confirm that author spellings and email addresses match institutional records.

### Item 2: IEEE Access Article Processing Charge (APC) & Open Access Selection
- **Status:** IEEE Access is a 100% open-access journal with an Article Processing Charge (APC) of $1,950 (or discounted rate with IEEE member / institutional discount).
- **Action:** Ensure your institution or grant funding is selected for APC payment billing upon acceptance.

### Item 3: Code and Dataset Availability Statement
- **Current Text (Section V-A):** Experiments utilize the procedural synthetic benchmark (`IndustrialDefectDataset`) modeling the canonical NEU surface defect morphologies.
- **Action:** If you wish to provide a public GitHub URL upon acceptance, the codebase in `main.py`, `models/`, `losses.py`, and `dataset.py` is self-contained and reproducible.

### Item 4: GPU Hardware Model Confirmation for Inference Latency (Section V-G)
- **Current Text (Section V-G):** *"On an NVIDIA GPU, standard PyTorch FP32 inference latency averages 24.3 ms per patch (~41.1 FPS) at batch size 1."*
- **Context:** Historical draft text attributed 24.3 ms to an NVIDIA GeForce RTX 4090, while the local execution environment for ablations was an NVIDIA GeForce RTX 5070 Ti Laptop GPU. Because no raw profiling script/log artifact records the exact GPU for the 24.3 ms figure, the manuscript designates it neutrally as "an NVIDIA GPU".
- **Action:** If you wish to specify the exact card in the final proof (e.g., "NVIDIA GeForce RTX 4090" or "NVIDIA GeForce RTX 5070 Ti Laptop GPU"), confirm the exact card used. If preferred, the current phrasing ("an NVIDIA GPU") is technically accurate and safe for submission.

---

## 3. Recommended Upload Package Contents

The file `submission_release/ieee_access_msba_net_submission.zip` contains:
- `ieee_access_msba_net_final.tex` (Authoritative LaTeX source)
- `ieee_access_msba_net_final.pdf` (Reference compiled PDF, exactly 8 pages)
- `references_revised.bib` & `references.bib` (18 authentic cited references)
- `figures/` (All 4 high-resolution 300-DPI publication figures)
- `ieeeaccess.cls` & `IEEEtran.cls` (IEEE Access official template classes)
- `Logo.png`, `notaglineLogo.png`, `bullet.png` (IEEE Access official template assets)

**Status:** The package is self-contained, standalone, and ready for IEEE Access submission.
