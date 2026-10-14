# MSBA-Net: IEEE Access LaTeX Project for Overleaf

This repository contains the complete, ready-to-compile LaTeX source files for the paper:
**"MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation"**

---

## 🚀 How to Open in Overleaf

1. Go to [Overleaf](https://www.overleaf.com) and log in.
2. Click **New Project** $\rightarrow$ **Upload Project**.
3. Upload the `.zip` archive.
4. Overleaf will automatically detect `main.tex` as the root document and compile the manuscript.
5. Click **Recompile** if not triggered automatically.

---

## ⚙️ Overleaf Compiler Recommendations

- **Compiler:** `pdfLaTeX` (Default) or `XeLaTeX`
- **TeX Live Version:** `2022`, `2023`, or `2024`
- **Main Document:** `main.tex` (or `ieee_access_msba_net.tex`)

---

## 📁 Project Directory Structure

```text
├── main.tex                    # Primary LaTeX entry point (auto-detected by Overleaf)
├── ieee_access_msba_net.tex     # Full IEEE Access manuscript source
├── ieeeaccess.cls              # Official IEEE Access LaTeX document class
├── IEEEtran.cls                # Base IEEE Transactions class loaded by ieeeaccess
├── Logo.png                    # IEEE Access header logo
├── notaglineLogo.png           # IEEE Access alternate header logo
├── bullet.png                  # IEEE Access blue square bullet for author bios & sections
├── references.bib              # Complete BibTeX bibliography (18 citations)
├── figures/                    # High-resolution publication figures
│   ├── fig1_architecture.png           # MSBA-Net architecture diagram
│   ├── fig2_visual_comparison.png      # Qualitative defect segmentation results
│   ├── fig3_loss_curves.png            # Training/validation convergence plots
│   ├── fig4_degraded_benchmark.png      # Factory degradation stress-test plots
│   ├── guide_architecture_diagram.png  # Detailed network flow overview
│   └── guide_project_summary.png       # Comprehensive project summary
└── conference_icaiit_version/  # ICAIIT 2026 conference versions of the manuscript
    ├── icaiit2026_defect_paper.tex
    ├── icaiit2026_defect_camera_ready.tex
    └── icaiit2026_defect_blind_submission.tex
```

---

## 👥 Authors
- **Amen Parmar** (Department of Computer Science and Engineering, Manipal University Jaipur)
- **Amit Kumar Bairwa** (Department of Computer Science and Engineering, Manipal University Jaipur)
- **Varun Kumar** (Department of Computer Science and Engineering, Manipal University Jaipur)
