# FINAL TARGETED CORRECTIONS CHANGELOG — MSBA-Net (IEEE ACCESS)

**Date:** October 14, 2026  
**Manuscript Title:** MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation  
**Journal Target:** IEEE Access (Regular Paper, 8-page limit)  

---

## 1. Targeted Manuscript Corrections Summary

| ID | Location | Original Text / Claim | Corrected Manuscript Text | Scientific Rationale |
|:---|:---|:---|:---|:---|
| **TC-01** | **Section V-A** (Page 5, Left Column) | "...ensuring that no spatial flaw trajectories or texture seeds recur in the validation set." | "...synthesized using decoupled pseudorandom number streams (`\texttt{np.random.RandomState}` with reserved partition seeds) to minimize pattern recurrence." | **Scientific Honesty & Procedural Accuracy:** Code inspection of `dataset.py` confirmed `self.rng = np.random.RandomState(seed if mode == 'train' else seed + 1000)`. Decoupled seed streams draw independently from the parametric distribution, minimizing recurrence, but do not provide an explicit geometric deduplication algorithm or mathematical guarantee against all possible visual similarity. |
| **TC-02** | **Section V-E** (Page 7, Left Column) | "The 0.54 percentage-point difference reflects routine variation between independent training runs under stochastic optimization." | "The 0.54-percentage-point difference occurs between two independently trained checkpoints. Because the experiments use separate training runs, the difference cannot be attributed to a specific factor from these results alone." | **Causal Restraint:** Replaced unsupported causal assertion ("routine variation") with cautious scientific phrasing recognizing that the difference occurs between separate runs and cannot be causally attributed to a specific factor from these scores alone. |
| **TC-03** | **Section V-E** (Page 7, Left Column) | `checkpoint \texttt{ablation_loss4_full.pth}` (caused overfull hbox of 17.4 pt) | `checkpoint \texttt{ablation\_\allowbreak loss4\_\allowbreak full.pth}` | **Typographic Precision:** Allowed hyphenation break on underscore for long file identifier, resolving an overfull hbox warning and ensuring clean margin alignment. |
| **TC-04** | **Section VI-B** (Page 8, Left Column) | "...including pressurized air-knife enclosures to repel rolling oil mists, high-intensity pulsed LED strobe arrays to maintain contrast ($\Delta I > 30/255$), and mechanical strip tension stabilizers to eliminate optical defocus flutter \cite{satyanarayanan2017edge}." | "...would likely require plant-level engineering controls, such as pressurized air-knife enclosures to repel rolling oil mists, high-intensity pulsed illumination to preserve perimeter contrast, and mechanical strip stabilization to mitigate optical defocus flutter." | **Citation & Claim Remediation:** Removed reference [19] (`satyanarayanan2017edge`), which pertains to edge computing and does not substantiate air knives or strip tensioners. Removed the ungrounded contrast threshold ($\Delta I > 30/255$). Phrased as a cautious engineering recommendation rather than a sourced empirical claim. |
| **TC-05** | **Bibliography** (`.bib` & Page 8) | Contained unused/unsupported entries (`satyanarayanan2017edge`, `tensorrt2024`, duplicate `liu2024dmsunet`). | Cleaned bibliography to exactly 18 authentic peer-reviewed references matching 1-to-1 with manuscript citations. | **Bibliographic Integrity:** Preserves strictly authentic citations, eliminating all unverified or out-of-scope entries. |

---

## 2. Synchronized File Inventory & SHA-256 Checksums

All source, document, and archive files have been synchronized across `submission_release/` and the project root:

- **Authoritative LaTeX Source (46,815 bytes):**
  - `submission_release/ieee_access_msba_net_revised.tex`
  - `submission_release/ieee_access_msba_net_final.tex`
  - `submission_release/ieee_access_msba_net_submission.tex`
  - `ieee_access_msba_net_revised.tex`
  - `ieee_access_msba_net_final.tex`
  - `ieee_access_msba_net_submission.tex`  
  *SHA-256:* `fa3698c57c53f9a04f29dc56349ab38e63af76dd6bedddaf74061727e8d5ea7a`

- **Authoritative Compiled PDF (1,332,638 bytes, Exactly 8 Pages):**
  - `submission_release/ieee_access_msba_net_revised.pdf`
  - `submission_release/ieee_access_msba_net_final.pdf`
  - `submission_release/ieee_access_msba_net_submission.pdf`
  - `ieee_access_msba_net_revised.pdf`
  - `ieee_access_msba_net_final.pdf`
  - `ieee_access_msba_net_submission.pdf`  
  *SHA-256:* `192136744f58c87c03c74f4bc0237c05c7d5fec94c71394187e196fac2a6634b`

- **Authoritative BibTeX Database (6,408 bytes, 18 Authentic Entries):**
  - `submission_release/references_revised.bib`
  - `submission_release/references.bib`
  - `references_revised.bib`
  - `references.bib`  
  *SHA-256:* `99d0781a14e07a57f2fc5eb9dba1350c3a7fd149858495081b1fcc66a6eb2b57`

- **Submission Archive (7,054,646 bytes):**
  - `submission_release/ieee_access_msba_net_submission.zip`  
  *SHA-256:* `b8b91a27053feb4e8b0f862b6a2d99040534740de730bf8eafcf0134b4b15c01`
