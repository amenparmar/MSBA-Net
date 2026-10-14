# IEEE ACCESS FORMATTING AND METADATA AUDIT REPORT

**Project:** MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation  
**Target Journal:** IEEE Access  
**Audit Date:** October 14, 2026  
**Auditor:** Antigravity Autonomous Scientific Publishing & Formatting Specialist  

---

## 1. ANALYSIS OF PUBLICATION METADATA & TEMPLATE PLACEHOLDERS

An inspection of `ieee_access_msba_net_final.pdf` identified three metadata elements that warranted rigorous verification against official IEEE Access author guidelines:

### 1.1 The History String (`Date of publication xxxx 00, 0000...`)
- **Inspection Finding:** Line 22 contains:
  `\history{Date of publication xxxx 00, 0000, date of current version xxxx 00, 0000.}`
- **Classification:** **Official IEEE Access Template Placeholder (Mandatory for Initial Submission)**.
- **Verification against IEEE Access Guidelines:**
  The official IEEE Access template (`IEEEaccess_template.tex`) explicitly provides:
  `\history{Date of publication xxxx 00, 0000, date of current version xxxx 00, 0000.}`
  Authors are strictly instructed **not** to invent submission dates, acceptance dates, or publication dates. IEEE publishing operations will insert actual calendar dates upon acceptance during production layout.
- **Audit Decision:** Retain the official submission-stage placeholder formatting.

---

### 1.2 The Fabricated DOI (`10.1109/ACCESS.2026.MSBANET`)
- **Inspection Finding:** Line 23 contains:
  `\doi{10.1109/ACCESS.2026.MSBANET}`
- **Classification:** **Manuscript Author Error (Fabricated DOI Identifier)**.
- **Verification against IEEE Access Guidelines:**
  Digital Object Identifiers (DOIs) are legally registered through Crossref and assigned strictly by the IEEE Periodicals Production Department upon article acceptance and registration. Authors **cannot** register or assign their own DOI. The official IEEE Access template placeholder is:
  `\doi{10.1109/ACCESS.2017.DOI}`
- **Audit Decision:** **Retract the fabricated DOI `10.1109/ACCESS.2026.MSBANET`** and restore the official IEEE Access submission-stage placeholder `10.1109/ACCESS.2017.DOI`.

---

### 1.3 The Footer (`VOLUME 4, 2016`)
- **Inspection Finding:** Running footer on all odd and even pages displays `VOLUME 4, 2016`.
- **Classification:** **Publisher-Controlled Class File Default (`ieeeaccess.cls`)**.
- **Source Code Verification in `ieeeaccess.cls`:**
  Lines 357–358 and 422–427 of `ieeeaccess.cls` contain:
  ```latex
  \def\thevol{4}
  \def\theyear{2016}
  ...
  \hbox to \textwidth{{\footervolfont VOLUME\ \thevol, 2016}\hfill\mbox{}}
  ```
  The string `VOLUME 4, 2016` is hardcoded directly into the official `ieeeaccess.cls` distribution provided by IEEE. Authors submitting to IEEE Access submit source packages with the standard class file; the IEEE compositor overwrites `\thevol` and the publication year during production.
- **Audit Decision:** Retain standard class compliance without patching system macros.

---

## 2. AUTHOR METADATA, AFFILIATIONS, AND CONTACT VERIFICATION

The manuscript front matter was verified for full compliance with IEEE Access author guidelines:

1. **Title:**
   `MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation`
   - Formatted in `\title{...}` with standard capitalization.

2. **Authors & Memberships:**
   - `\uppercase{Amen Parmar}\authorrefmark{1}, \IEEEmembership{Graduate Student Member, IEEE}`
   - `\uppercase{Amit Kumar Bairwa}\authorrefmark{1}, \IEEEmembership{Senior Member, IEEE}`
   - `\uppercase{Varun Kumar}\authorrefmark{1}, \IEEEmembership{Member, IEEE}`
   - Formatted using official `\uppercase{}` and `\authorrefmark{}` commands.

3. **Institutional Affiliation:**
   - `\address[1]{Department of Computer Science and Engineering, Manipal University Jaipur, Jaipur, Rajasthan 303007, India}`
   - Contains complete department, university, city, state, postal code, and country.

4. **Corresponding Author:**
   - `\corresp{Corresponding author: Amen Parmar (email: amen.parmar@jaipur.manipal.edu).}`
   - Standard IEEE format with complete email address.

5. **Running Headers:**
   - `\markboth{Parmar \headeretal: MSBA-Net for Small and Low-Contrast Defect Segmentation}{Parmar \headeretal: MSBA-Net for Small and Low-Contrast Defect Segmentation}`
   - Header is under 60 characters, avoids math, and uses standard `\headeretal` macro.

6. **Abstract & Keywords:**
   - Abstract: Unstructured single paragraph, 228 words (well within the IEEE Access 250-word limit), containing zero citations or mathematical notation that cannot stand alone.
   - Index Terms (Keywords): Alphabetical order, title case, containing 7 terms drawn from IEEE taxonomy.

---

## 3. DOCUMENT STRUCTURE AND PAGE LAYOUT AUDIT

- **Page Budget:** Exactly 8 pages in two-column format.
- **Figures:**
  - Figure 1 (`fig1_architecture.png`): Top of Page 2 (`figure*`, span two columns). Caption matches architecture.
  - Figure 2 (`fig2_visual_comparison.png`): Top of Page 5 (`figure*`, span two columns). Qualitative comparison across 4 morphologies with clean attribution citations.
  - Figure 3 (`fig3_loss_curves.png`): Single column (`figure`), Page 6. Loss curves.
  - Figure 4 (`fig4_degraded_benchmark.png`): Single column (`figure`), Page 6. Degradation bar chart.
- **Tables:**
  - Table 1 (Table \ref{tab:hyperparameters}): Single column, Page 5. Hyperparameter and complexity specifications.
  - Table 2 (Table \ref{tab:benchmark}): Span two columns (`table*`), Page 6. Controlled baselines (Panel A) and literature benchmarks (Panel B).
  - Table 3 (Table \ref{tab:classwise}): Single column, Page 6. Classwise performance breakdown.
  - Table 4 (Table \ref{tab:ablation}): Single column, Page 7. Architectural ablation progression.
  - Table 5 (Table \ref{tab:loss_ablation}): Single column, Page 7. Composite loss formulation ablation.
- **Section Structure:** Follows standard IEEE Access technical article organization (I. Introduction, II. Related Work, III. Proposed MSBA-Net Architecture, IV. Multi-Component Loss Formulation, V. Experimental Results & Analysis, VI. Limitations and Robustness Under Industrial Degradation, VII. Conclusion and Future Work, References).
- **Ending Tag:** Ends with mandatory `\EOD` macro before `\end{document}`.
