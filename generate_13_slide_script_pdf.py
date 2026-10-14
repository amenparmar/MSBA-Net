"""
generate_13_slide_script_pdf.py
Generates the official Presentation Script & Examiner Viva Guide PDF for the 13-Slide MSBA-Net Presentation.
Output: MSBA-Net_Presentation_Script_Amen_Parmar.pdf
"""

import os
import subprocess
import fitz  # PyMuPDF

HTML_PATH = os.path.abspath("scratch/speaker_script_13.html")
PDF_PATH = os.path.abspath("MSBA-Net_Presentation_Script_Amen_Parmar.pdf")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>MSBA-Net Presentation Script & Viva Guide (13 Slides) — Amen Parmar</title>
<style>
  @page {
    size: A4;
    margin: 18mm 18mm 20mm 18mm;
    @bottom-right {
      content: counter(page);
    }
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1E293B;
    background-color: #FFFFFF;
    line-height: 1.55;
    font-size: 10pt;
    margin: 0;
    padding: 0;
  }

  /* Document Header */
  .doc-header {
    border-bottom: 2px solid #0B192C;
    padding-bottom: 14px;
    margin-bottom: 22px;
  }
  .doc-badge {
    display: inline-block;
    background-color: #FEF3C7;
    color: #D97706;
    border: 1px solid #D97706;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 8pt;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
  }
  .doc-title {
    font-size: 16pt;
    font-weight: 800;
    color: #0B192C;
    line-height: 1.25;
    margin: 0 0 8px 0;
  }
  .doc-subtitle {
    font-size: 10.5pt;
    color: #475569;
    font-weight: 600;
    margin: 0 0 12px 0;
  }
  .meta-grid {
    display: table;
    width: 100%;
    margin-top: 10px;
    font-size: 9pt;
    background: #F8F7F3;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 10px 14px;
  }
  .meta-row {
    display: table-row;
  }
  .meta-cell {
    display: table-cell;
    padding: 3px 8px;
    vertical-align: top;
  }
  .meta-label {
    font-weight: 700;
    color: #0B192C;
    width: 130px;
  }
  .meta-val {
    color: #334155;
  }

  /* Presentation Structure */
  .section-heading {
    font-size: 12.5pt;
    font-weight: 800;
    color: #0B192C;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 1.5px solid #CBD5E1;
    padding-bottom: 4px;
    margin-top: 24px;
    margin-bottom: 14px;
  }

  /* Slide Script Card */
  .slide-box {
    border: 1.2px solid #0F172A;
    border-radius: 8px;
    background: #FFFFFF;
    margin-bottom: 18px;
    page-break-inside: avoid;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }
  .slide-header {
    background: #F8F7F3;
    border-bottom: 1.2px solid #CBD5E1;
    padding: 8px 14px;
    border-top-left-radius: 7px;
    border-top-right-radius: 7px;
    display: table;
    width: 100%;
    box-sizing: border-box;
  }
  .slide-title-wrap {
    display: table-cell;
    vertical-align: middle;
  }
  .slide-num {
    font-size: 8.5pt;
    font-weight: 700;
    color: #D97706;
    text-transform: uppercase;
  }
  .slide-title {
    font-size: 11pt;
    font-weight: 800;
    color: #0B192C;
    margin: 2px 0 0 0;
  }
  .slide-time {
    display: table-cell;
    vertical-align: middle;
    text-align: right;
    font-size: 8.5pt;
    font-weight: 700;
    color: #059669;
    white-space: nowrap;
  }
  .slide-body {
    padding: 12px 16px;
  }
  .cues-box {
    background: #F1F5F9;
    border-left: 3px solid #2563EB;
    padding: 6px 12px;
    margin-bottom: 10px;
    font-size: 8.5pt;
    color: #334155;
    border-radius: 0 4px 4px 0;
  }
  .cues-title {
    font-weight: 700;
    color: #1E293B;
  }
  .script-label {
    font-size: 8.5pt;
    font-weight: 700;
    text-transform: uppercase;
    color: #64748B;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }
  .script-text {
    font-size: 9.5pt;
    color: #0B192C;
    text-align: justify;
    line-height: 1.6;
    margin: 0;
  }
  .script-text p {
    margin: 0 0 8px 0;
  }
  .script-text p:last-child {
    margin-bottom: 0;
  }
  .transition-box {
    margin-top: 8px;
    padding: 5px 10px;
    background: #EFF6FF;
    border-left: 3px solid #3B82F6;
    font-size: 8pt;
    color: #1E40AF;
    border-radius: 0 4px 4px 0;
  }
  .tip-box {
    margin-top: 6px;
    padding: 5px 10px;
    background: #FEF3C7;
    border-left: 3px solid #D97706;
    font-size: 8pt;
    color: #92400E;
    border-radius: 0 4px 4px 0;
  }

  /* Q&A Section */
  .qa-card {
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    background: #FFFFFF;
    margin-bottom: 11px;
    page-break-inside: avoid;
    padding: 10px 13px;
  }
  .qa-q {
    font-size: 9.5pt;
    font-weight: 700;
    color: #0B192C;
    margin: 0 0 5px 0;
    display: flex;
    align-items: flex-start;
  }
  .qa-badge {
    background: #DBEAFE;
    color: #1E40AF;
    font-size: 7.5pt;
    font-weight: 800;
    padding: 2px 6px;
    border-radius: 4px;
    margin-right: 8px;
    display: inline-block;
    flex-shrink: 0;
  }
  .qa-a {
    font-size: 8.8pt;
    color: #334155;
    line-height: 1.48;
    margin: 0;
    text-align: justify;
  }
  .qa-key {
    margin-top: 5px;
    font-size: 7.8pt;
    font-weight: 700;
    color: #059669;
  }

  .page-break {
    page-break-before: always;
  }

  .footer-note {
    font-size: 8pt;
    color: #64748B;
    text-align: center;
    margin-top: 20px;
    border-top: 1px solid #E2E8F0;
    padding-top: 8px;
  }
</style>
</head>
<body>

<!-- DOCUMENT HEADER -->
<div class="doc-header">
  <div class="doc-badge">M.Tech (AIML) Research Seminar Presentation Script &amp; Viva Guide</div>
  <h1 class="doc-title">MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation</h1>
  <div class="doc-subtitle">Official Defense Presentation Script (13 Slides), Spoken Transitions, and Examiner Viva Q&amp;A</div>

  <div class="meta-grid">
    <div class="meta-row">
      <div class="meta-cell meta-label">Presenter:</div>
      <div class="meta-cell meta-val"><strong>Amen Parmar</strong> | M.Tech (AIML) | Roll No: <strong>2502010010</strong></div>
    </div>
    <div class="meta-row">
      <div class="meta-cell meta-label">Paper Authors:</div>
      <div class="meta-cell meta-val">Amen Parmar, Amit Kumar Bairwa, Varun Kumar</div>
    </div>
    <div class="meta-row">
      <div class="meta-cell meta-label">Department &amp; Affiliation:</div>
      <div class="meta-cell meta-val">Department of Computer Science and Engineering, Manipal University Jaipur, Jaipur, Rajasthan, India</div>
    </div>
    <div class="meta-row">
      <div class="meta-cell meta-label">Target Duration:</div>
      <div class="meta-cell meta-val"><strong>10 – 12 Minutes</strong> (~50–65 seconds per slide) + 5–10 Minutes Committee Discussion</div>
    </div>
  </div>
</div>

<!-- ========================================== -->
<!-- SLIDE-BY-SLIDE SCRIPT (13 SLIDES) -->
<!-- ========================================== -->
<div class="section-heading">Part 1: Slide-by-Slide Spoken Script (Exactly 13 Slides)</div>

<!-- SLIDE 1 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 1 of 13</div>
      <div class="slide-title">Title Slide — Introduction &amp; Credentials</div>
    </div>
    <div class="slide-time">Target: 45–55 sec | Cumulative: 0:00 – 0:50</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Clean title container on left; conceptual overview on right; presenter credentials, co-authors, and Manipal University Jaipur affiliation.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Respected session chair, honorable committee members, and professors: Good morning.</p>
      <p>My name is Amen Parmar, M.Tech in Artificial Intelligence and Machine Learning at Manipal University Jaipur, Roll Number 2502010010. Today, I am presenting our research paper entitled: <em>'MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation'</em>, co-authored with Dr. Amit Kumar Bairwa and Dr. Varun Kumar.</p>
      <p>In modern metallurgical manufacturing, automated surface defect inspection of flat-rolled steel is an indispensable foundation of quality assurance. However, traditional computer vision and generic deep learning models struggle significantly when confronted with microscopic defect scale and near-zero boundary contrast. In this presentation, I will explain the objectives, methodology, experimental benchmark results, and operational boundaries of MSBA-Net."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 2:</strong> "Let us begin by establishing the formal research objectives of this work."
    </div>
    <div class="tip-box">
      <strong>Viva Tip:</strong> Speak at an even, confident pace. State the title clearly and emphasize <em>Multi-Scale Feature Enhancement</em> and <em>Boundary-Aware Learning</em>.
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- SLIDE 2 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 2 of 13</div>
      <div class="slide-title">Objective — Core Research Goals</div>
    </div>
    <div class="slide-time">Target: 50–60 sec | Cumulative: 0:50 – 1:45</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> 5 clean academic bullet points outlining core objectives; green focus takeaway banner at bottom.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Looking at our core objectives on Slide 2:
      Our primary goal is to develop an effective deep learning framework tailored specifically for small and low-contrast steel surface defects.</p>
      <p>This breaks down into five technical aims:
      First, to segment complex industrial surface defects with high pixel accuracy.
      Second, to preserve fine-grained structural features that are conventionally lost during aggressive spatial downsampling and pooling operations.
      Third, to improve boundary localization and contour definition for weak, blurry, and low-contrast defect edges.
      Fourth, to address the severe foreground-background class imbalance where defect-free steel occupies over 98% of total surface area.
      And fifth, to rigorously evaluate the architecture on the standardized NEU surface defect database against existing state-of-the-art models.</p>
      <p>As summarized at the bottom: Our core focus is accurate segmentation of small defects without sacrificing boundary precision."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 3:</strong> "To appreciate why achieving this objective is challenging, let us review the industrial background."
    </div>
  </div>
</div>

<!-- SLIDE 3 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 3 of 13</div>
      <div class="slide-title">Brief Overview — Industrial Context &amp; Challenges</div>
    </div>
    <div class="slide-time">Target: 55–65 sec | Cumulative: 1:45 – 2:45</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> 5 bullet points on left; supporting defect visual (Crazing micro-crack from paper) on right showing faint intensity contrast.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Slide 3 provides a brief overview of the operational background.
      In continuous steel rolling mills, steel strips travel at high production speeds. Automated visual inspection is vital to catch flaws early before defective coils reach automotive or construction clients.</p>
      <p>However, optical inspection on steel faces three severe physical challenges:
      First, critical safety defects such as crazing micro-cracks or tiny pit clusters often occupy less than 1% of the entire image area.
      Second, the intensity contrast between the defect and ambient rolled metal texture is extremely low.
      Third, standard encoder-decoder CNNs rely on aggressive spatial downsampling to expand receptive fields. In doing so, a 1-to-2 pixel hairline crack is completely washed out before reaching deeper semantic layers.</p>
      <p>On the right side of the slide, you see an actual crazing defect from our research paper. Notice how subtly the crack blends into the rolled steel background. This visual illustrates why standard segmentation models fail, and why pixel-level precision is indispensable."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 4:</strong> "This leads directly to the core problem statement and research gap in current literature."
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- SLIDE 4 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 4 of 13</div>
      <div class="slide-title">Problem Statement &amp; Research Gap — Limitations of Existing Methods</div>
    </div>
    <div class="slide-time">Target: 55–65 sec | Cumulative: 2:45 – 3:45</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Two-column layout: 'Key Challenges' (left) vs 'Research Gap' (right); research need banner at bottom.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Slide 4 articulates the precise problem statement and research gap.
      On the left, we identify the primary challenges:
      Micro-scale flaws, low-contrast boundaries, over 98% class imbalance, feature dilution in deep layers, and boundary bleeding where predicted masks leak into background steel.</p>
      <p>On the right, we identify the research gap in existing approaches:
      First, standard segmentation architectures like generic U-Net or DeepLab focus primarily on semantic classification and lose fine spatial details.
      Second, boundary information is rarely preserved explicitly or fed back into the decoder.
      Third, while existing models report acceptable overall mIoU on large defects, their performance collapses on tiny defects occupying less than 1% of the image.
      And fourth, heavy transformer models introduce high latency incompatible with factory line speeds.</p>
      <p>This establishes our clear research need: A lightweight architecture combining multi-scale feature preservation with explicit boundary guidance."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 5:</strong> "Now that we understand the problem, let us look at the proposed methodology: MSBA-Net."
    </div>
  </div>
</div>

<!-- SLIDE 5 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 5 of 13</div>
      <div class="slide-title">Proposed Methodology — MSBA-Net Architecture</div>
    </div>
    <div class="slide-time">Target: 75–90 sec | Cumulative: 3:45 – 5:10</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Clean architecture schematic (the only diagram slide in the deck). Top: BAS stream &rarr; Boundary Head &rarr; BGFF Attention; Middle: Input &rarr; Encoder 1-2 &rarr; Encoder 3-4 &rarr; Bottleneck &rarr; Decoder &rarr; Mask; 4 concise bullets below.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Slide 5 presents the central contribution of our work: the MSBA-Net architecture, faithfully recreated from Figure 1 of our paper.</p>
      <p>Let us trace the information flow:
      In the middle row, the input grayscale steel image passes through a four-stage hierarchical encoder. Rather than using conventional convolutions that lose fine spatial resolution, each encoder stage incorporates our Multi-Scale Feature Preservation (MSFP) block. MSFP uses parallel dilated depthwise convolutions with dilation rates 1, 2, and 4. Branch 2 with r=1 has a 3x3 receptive field for hairline micro-cracks; Branch 3 with r=2 spans 5x5 pixels for pit depressions; and Branch 4 with r=4 covers 9x9 pixels for broad patches.</p>
      <p>Now look at the top auxiliary pathway: the Boundary-Aware Stream (BAS). BAS branches off early from Stages 1 and 2, where fine edge gradients are still intact. It predicts an explicit 256x256 boundary map under morphological edge supervision.</p>
      <p>This learned boundary knowledge is transferred to the decoder via the BGFF—Boundary-Guided Feature Fusion—spatial attention gate. BGFF computes dynamic spatial attention weights that amplify decoder features along uncertain defect boundaries while suppressing noise from uniform steel background.</p>
      <p>Finally, the entire network is trained end-to-end using our composite loss: 0.3 BCE, 0.3 Dice, 0.2 Focal, and 0.2 Boundary loss. This joint optimization guarantees both region completeness and razor-sharp boundary delineation."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 6:</strong> "Moving on to the experimental setup and dataset used to validate our model..."
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- SLIDE 6 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 6 of 13</div>
      <div class="slide-title">Experimental Work — Dataset &amp; Setup</div>
    </div>
    <div class="slide-time">Target: 55–65 sec | Cumulative: 5:10 – 6:10</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> NEU Dataset specifications (1,800 images, 256x256, 70/15/15 split) on left; 6 defect categories table on right.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Moving to the experimental setup on Slide 6:
      To evaluate MSBA-Net, we benchmarked the architecture on the Northeastern University (NEU) Surface Defect Database, the gold standard in metallurgical computer vision.</p>
      <p>As outlined on the left, the database contains 1,800 grayscale images spanning six defect categories, with exactly 300 images per class. The original 200 by 200 pixel images were resized to 256 by 256. We applied a standard 70-15-15 split: 1,260 images for training, 270 for validation, and 270 for completely held-out test evaluation, using fixed random seeds for strict reproducibility.</p>
      <p>On the right, the table summarizes the six defect categories: Crazing, Inclusions, Patches, Pitted Surfaces, Rolled-in Scale, and Scratches. Each category introduces distinct morphological challenges: Crazing features micro-cracks that vanish during downsampling; Inclusions exhibit faint contrast gradients; and Pitted Surfaces consist of dense clusters of tiny sub-1% depressions. This diversity ensures a rigorous and comprehensive evaluation."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 7:</strong> "Next, let us look at the training configuration and quantitative evaluation metrics."
    </div>
  </div>
</div>

<!-- SLIDE 7 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 7 of 13</div>
      <div class="slide-title">Experimental Work — Training &amp; Evaluation</div>
    </div>
    <div class="slide-time">Target: 60–70 sec | Cumulative: 6:10 – 7:15</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Training parameters &amp; hardware specs on left (RTX 4090, AdamW, Cosine Annealing, 9.38M params, 14.2 GFLOPs, 41.1/88.5 FPS); Evaluation metrics &amp; Tiny-Defect callout on right.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Slide 7 details our training configuration and evaluation metrics.
      On the left, all models were trained in PyTorch 2.1 on an NVIDIA RTX 4090 GPU with 24GB of VRAM. We used the AdamW optimizer with an initial learning rate of 1 times 10 to the minus 3, decaying via cosine annealing down to 1 times 10 to the minus 6, over 100 epochs with a batch size of 16. Convergence was reliably reached around epoch 75.</p>
      <p>From an engineering perspective, MSBA-Net maintains a compact footprint of only 9.38 million parameters and 14.2 GFLOPs. It achieves 41.1 frames per second in standard FP32 PyTorch, and 88.5 frames per second under TensorRT FP16 quantization—easily satisfying real-time factory line requirements.</p>
      <p>On the right, we define our evaluation metrics: mIoU, Dice, Precision, and Recall. Crucially, we introduce Tiny-Defect mIoU, which isolates defect regions occupying less than 1% of the image canvas. In industrial steel production, a tiny hairline crack can initiate catastrophic structural failure during stamping. Generic models often score high overall because large defects mask their poor performance on micro-flaws. Tiny-Defect mIoU directly measures whether micro-scale features are truly preserved."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 8:</strong> "Now we compare the proposed method with existing approaches on the benchmark."
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- SLIDE 8 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 8 of 13</div>
      <div class="slide-title">Results — Comparison with Existing Methods</div>
    </div>
    <div class="slide-time">Target: 65–75 sec | Cumulative: 7:15 – 8:25</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Native clustered column chart on left comparing 6 SOTA models; compact comparison table and 3 key observations on right.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Slide 8 presents our primary benchmark comparison against published 2024 to 2026 models.</p>
      <p>Looking at the column chart on the left, MSBA-Net establishes a decisive lead across published baselines:
      Earlier 2024 models like GNA-PSC and MixSegNet achieved 83.50% and 84.80% mIoU. More recent models like EF²Net in 2024 and DAMF-Net in 2025 reached 88.42% and 91.65%. The previous state-of-the-art, DMS-UNet published in 2026, achieved 94.20%.
      MSBA-Net advances the benchmark to 97.01% mIoU, an improvement of plus 2.81 percentage points.</p>
      <p>Examining the summary table on the right:
      Our Dice coefficient reaches 98.48%, indicating outstanding mask continuity and region overlap.
      Furthermore, MSBA-Net achieves 97.57% Precision and 99.41% Recall, translating to near-zero missed defects in practice.
      Most significantly, look at the final column: Tiny-Defect mIoU. On defects occupying less than 1% of the image, MSBA-Net achieves 92.48%. That is a 4.08% improvement over DMS-UNet and more than 20% higher than GNA-PSC. This provides clear empirical proof that our hybrid multi-scale and boundary-aware approach effectively prevents micro-scale feature dilution."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 9:</strong> "Let us now examine the detailed per-class performance across each defect category."
    </div>
  </div>
</div>

<!-- SLIDE 9 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 9 of 13</div>
      <div class="slide-title">Results — Detailed Analysis / Per-Class Performance</div>
    </div>
    <div class="slide-time">Target: 60–70 sec | Cumulative: 8:25 – 9:30</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Per-category table &amp; observations on left (Patches 97.85%, Inclusions 97.15%, Crazing 96.42%); supporting qualitative image comparison from Figure 2 on right.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Moving to a more detailed analysis on Slide 9, we examine per-category performance across all six defect classes.</p>
      <p>On the left, the table demonstrates remarkable consistency:
      Every single defect category surpasses 96.4% mIoU. Patches achieved the highest accuracy at 97.85% mIoU, followed by Inclusions at 97.15% and Scratches at 97.12%.
      Crazing was the most challenging category at 96.42% mIoU, owing to the extreme thinness of hairline micro-cracks. Nevertheless, MSBA-Net outperforms all competing models on crazing by over 3 percentage points.</p>
      <p>On the right, we show supporting qualitative visual evidence directly from Figure 2 of our paper:
      In the first row, representing crazing: the baseline U-Net produces a fragmented, incomplete mask. In contrast, MSBA-Net traces the entire crack trajectory continuously.
      In the second row, showing thin inclusions: baseline U-Net bleeds noticeably into the background steel, whereas MSBA-Net confines its mask strictly to the defect perimeter.
      This visual comparison confirms that MSFP preserves fine structural topology, while BAS and BGFF prevent boundary bleeding."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 10:</strong> "To isolate the exact contribution of each module, let us inspect the ablation study."
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- SLIDE 10 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 10 of 13</div>
      <div class="slide-title">Ablation Study &amp; Analysis — Component Contributions</div>
    </div>
    <div class="slide-time">Target: 65–75 sec | Cumulative: 9:30 – 10:40</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Native grouped column chart on left (Overall mIoU vs Tiny mIoU across 4 stages); ablation metrics table and 3 core insights on right.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Why does MSBA-Net work so effectively? Slide 10 provides empirical ablation evidence validating each component.</p>
      <p>Looking at the grouped column chart on the left, we track both overall mIoU in blue and tiny-defect mIoU in amber across four incremental configurations:
      Starting from our Baseline Backbone without MSFP or BAS, the model achieves 94.10% overall mIoU, but only 84.60% on tiny defects.</p>
      <p>When we insert our Multi-Scale Feature Preservation (MSFP) blocks:
      Overall mIoU increases to 95.85%, but tiny-defect mIoU surges by an impressive 5.05 percentage points to 89.65%. This confirms our fundamental hypothesis: parallel dilated depthwise convolutions effectively prevent micro-flaws from being washed out.</p>
      <p>Next, when we introduce the Boundary-Aware Stream (BAS):
      Overall mIoU rises to 96.48%, and tiny mIoU reaches 91.20%, proving that explicit boundary loss forces the early encoder to maintain high-frequency edge gradients.</p>
      <p>Finally, adding the BGFF spatial attention gate completes MSBA-Net, achieving our peak 97.01% mIoU and 92.48% tiny-defect mIoU.
      As shown in the table on the right, this entire architectural enhancement adds only 1.62 million parameters over baseline, demonstrating high parameter efficiency."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 11:</strong> "Finally, let us discuss the limitations and operational boundaries of the framework."
    </div>
  </div>
</div>

<!-- SLIDE 11 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 11 of 13</div>
      <div class="slide-title">Limitations &amp; Robustness Analysis — Operational Boundaries</div>
    </div>
    <div class="slide-time">Target: 60–70 sec | Cumulative: 10:40 – 11:45</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Simulated degradation stress-test table on left (Normal 97.01%, Low contrast 39.67%, Blur 26.29%, Gaussian noise 2.33%); 5 academic limitation bullets on right.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Academic integrity requires complete transparency about physical operational limits. In Section V of our paper, we stress-tested MSBA-Net under simulated factory degradations:
      As shown in the table on the left:
      Under low contrast (gamma=1.8), mIoU drops to 39.67%.
      Under defocus blur (sigma=3.0), simulating camera vibration, mIoU drops to 26.29%.
      Under severe Gaussian noise (sigma=25), performance breaks down to 2.33% mIoU.</p>
      <p>Why does this breakdown occur?
      This is an information-theoretic limitation rather than an architectural bug:
      In steel inspection, defect boundaries are defined by subtle differences of only 5 to 15 gray levels. Adding Gaussian noise with sigma=25 produces random fluctuations of up to 50 gray levels across adjacent pixels. Because our Boundary-Aware Stream computes morphological gradients via differential operations, high-frequency random noise generates thousands of spurious false edges, completely overwhelming the attention gate.</p>
      <p>This provides an important engineering takeaway: Deploying deep learning models in real steel mills requires active LED shrouding, sealed camera enclosures, and front-end bilateral denoising filters. We do not claim unconstrained factory readiness without appropriate optical engineering."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 12:</strong> "Let us now synthesize our conclusions and outline the future roadmap."
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- SLIDE 12 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 12 of 13</div>
      <div class="slide-title">Conclusions &amp; Future Work — Summary &amp; Outlook</div>
    </div>
    <div class="slide-time">Target: 55–65 sec | Cumulative: 11:45 – 12:45</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Two clean columns: 'Conclusions' (left) vs 'Future Work' (right) with short, clear bullet points.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"To conclude our presentation, Slide 12 summarizes our core findings and outlines future directions.</p>
      <p>In conclusion:
      First, MSBA-Net successfully unites multi-scale feature preservation with boundary-aware learning.
      Second, MSFP prevents hairline cracks and tiny pit depressions from vanishing during downsampling.
      Third, BAS and BGFF establish sharp, leak-free boundary contours around faint defect perimeters.
      Fourth, the model sets a new benchmark on the NEU dataset, delivering 97.01% mIoU, 98.48% Dice, and 92.48% Tiny-Defect mIoU.
      And fifth, it operates at 41.1 FPS in PyTorch and 88.5 FPS under TensorRT FP16, validating practical industrial viability.</p>
      <p>Looking forward, our future roadmap focuses on:
      1. Extending the model to spatio-temporal video attention across continuous line-scan strip feeds.
      2. Exploring self-supervised pre-training on massive unlabeled industrial steel coils.
      3. Implementing INT8 edge quantization for low-power industrial controllers.
      And 4. Adding adaptive front-end denoising to harden boundary convolutions against sensor noise."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 13:</strong> "Thank you for your attention. I am now ready for questions."
    </div>
  </div>
</div>

<!-- SLIDE 13 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 13 of 13</div>
      <div class="slide-title">Thank You — Questions &amp; Discussion</div>
    </div>
    <div class="slide-time">Target: 25–35 sec | Cumulative: 12:45 – 13:15</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Clean Thank You slide with 'Questions &amp; Discussion' subtitle; presenter name, M.Tech degree, roll number, and department.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Thank you very much, respected committee members and professors, for your time, patience, and kind attention.</p>
      <p>I will now be honored to take any questions, comments, or suggestions regarding our research."</p>
    </div>
    <div class="tip-box">
      <strong>Viva Tip:</strong> Stand facing the examiners, smile calmly, and listen carefully to the entire question before answering. Take a brief pause before responding.
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- VIVA / EXAMINER Q&A SECTION -->
<!-- ========================================== -->
<div class="section-heading">Part 2: Likely Viva Examination Questions &amp; Answers (10 Questions)</div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q1</span>
    Why MSBA-Net? What is the core rationale behind developing this new model?
  </div>
  <div class="qa-a">
    Standard semantic segmentation models (like U-Net, SegNet, or DeepLab) were designed for macro natural scenes (like autonomous driving or medical organ segmentation). In industrial steel inspection, defects present two unique difficulties: they occupy less than 1% of the image (hairline cracks), and they have extremely weak intensity contrast against rolled steel textures. Standard architectures downsample aggressively, obliterating these tiny flaws. MSBA-Net was developed to specifically preserve multi-scale features without downsampling loss and explicitly learn boundary gradients through dedicated auxiliary supervision.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: MSBA-Net solves the specific metallurgical inspection problem where generic models suffer from feature dilution and blurry boundaries.</div>
</div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q2</span>
    Why MSFP (Multi-Scale Feature Preservation), and why specifically dilation rates 1, 2, and 4?
  </div>
  <div class="qa-a">
    MSFP replaces standard single-receptive convolution layers with parallel dilated depthwise convolutions at the same spatial resolution. Each branch addresses a distinct defect scale:
    r=1 gives a 3x3 receptive field for hairline crazing cracks;
    r=2 gives a 5x5 field for pit depressions and small inclusions;
    r=4 gives a 9x9 field for broad patches and rolled-in scale sheets.
    Dilation rates {1, 2, 4} satisfy the Hybrid Dilated Convolution (HDC) condition, ensuring that every pixel in the field is sampled without the checkerboard gridding artifacts caused by larger, non-consecutive dilation rates.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: Dilation rates {1, 2, 4} capture multi-scale defect morphologies without downsampling loss and eliminate gridding artifacts.</div>
</div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q3</span>
    Why is the Boundary-Aware Stream (BAS) designed as an auxiliary branch rather than placed in the main backbone?
  </div>
  <div class="qa-a">
    BAS branches off early from Stages 1 and 2 where spatial resolution is highest (256x256 and 128x128). It is kept auxiliary for two reasons:
    1. Direct gradient injection: In deep networks, boundary loss gradients diminish before reaching early layers. Attaching an auxiliary boundary head directly injects edge-supervision gradients where spatial detail is freshest.
    2. Decoupling semantics from geometry: The main backbone learns what type of defect is present (region semantics), while BAS learns where the defect perimeter begins and ends (geometric contours).
  </div>
  <div class="qa-key">Key Takeaway for Examiner: BAS explicitly forces early encoder features to retain fine boundary gradients before semantic pooling washes them away.</div>
</div>

<div class="page-break"></div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q4</span>
    What is BGFF (Boundary-Guided Feature Fusion) and how does it work?
  </div>
  <div class="qa-a">
    BGFF is the spatial attention mechanism that transfers boundary knowledge from the BAS stream into the decoder. It concatenates the boundary feature tensor F_bound with the decoder feature tensor F_dec, passes them through a 1x1 convolution, and applies a sigmoid activation to yield a 2D spatial attention map:
    <code>A_spat = &sigma;(Conv_1x1([F_bound ; F_dec]))</code>.
    The decoder features are then recalibrated via residual attention:
    <code>F_out = F_dec &odot; (1 + A_spat)</code>.
    Where boundary uncertainty is high, A_spat amplifies decoder feature gain; over uniform steel background, A_spat approaches 0, suppressing background noise and eliminating border bleeding.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: BGFF acts as an adaptive spatial gain controller that sharpens defect edges while suppressing background metal texture.</div>
</div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q5</span>
    Why is Tiny-Defect mIoU necessary when overall mIoU is already reported?
  </div>
  <div class="qa-a">
    Overall mIoU is an area-weighted metric. Large defects like broad patches or rolled-in scale sheets possess tens of thousands of pixels, whereas a hairline craze crack contains only a few hundred pixels. A model can achieve 94% overall mIoU simply by segmenting large defects well, even if it misses 100% of micro-cracks.
    Tiny-Defect mIoU explicitly isolates defect regions occupying less than 1% of the image area (&lt;655 pixels). In automotive stamping, micro-cracks cause sudden structural fatigue tears. Tiny-Defect mIoU unmasks whether an architecture actually solves the micro-flaw preservation problem.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: Tiny mIoU prevents large defects from masking failure modes on safety-critical micro-flaws.</div>
</div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q6</span>
    Why use multiple loss functions (BCE, Dice, Focal, Boundary) instead of standard Cross-Entropy?
  </div>
  <div class="qa-a">
    In steel surface defect segmentation, over 98% of pixels belong to defect-free steel. Standard Cross-Entropy produces gradients overwhelmingly dominated by background pixels.
    Our composite loss balances four complementary objectives:
    - <strong>BCE (0.3 weight):</strong> Guarantees smooth, pixel-by-pixel classification accuracy.
    - <strong>Dice (0.3 weight):</strong> Scale-invariant region overlap, ensuring small defect regions contribute equally to the gradient as large ones.
    - <strong>Focal (0.2 weight):</strong> Dynamically down-weights easy background pixels to focus gradient updates on hard, low-contrast boundary pixels.
    - <strong>Boundary (0.2 weight):</strong> Directly penalizes edge misalignment against morphological 1-pixel defect contours.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: The 4-term objective balances pixel accuracy, scale-invariant region overlap, hard-example focus, and boundary sharpness.</div>
</div>

<div class="page-break"></div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q7</span>
    Why was the NEU dataset selected for evaluation?
  </div>
  <div class="qa-a">
    The NEU Surface Defect Database developed by Northeastern University is the recognized benchmark in metallurgical defect vision research. It contains 1,800 images across the six canonical defect categories found in industrial rolling mills: Crazing, Inclusions, Patches, Pitted Surfaces, Rolled-in Scale, and Scratches (300 images each). Using NEU enables direct, fair, and reproducible comparison against peer-reviewed published models (such as GNA-PSC, MixSegNet, EF²Net, DAMF-Net, and DMS-UNet) under identical experimental protocols.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: NEU provides standardized industrial defect taxonomy, balanced classes, and direct comparability with published baselines.</div>
</div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q8</span>
    What are the main quantitative results achieved by MSBA-Net?
  </div>
  <div class="qa-a">
    On the NEU benchmark test set:
    1. <strong>Overall mIoU: 97.01%</strong>, surpassing the 2026 state-of-the-art DMS-UNet (94.20%) by +2.81%.
    2. <strong>Dice Coefficient: 98.48%</strong>, with 97.57% Precision and 99.41% Recall (near-zero missed flaws).
    3. <strong>Tiny-Defect mIoU: 92.48%</strong>, representing a +4.08% improvement over DMS-UNet (88.40%) and over +20% higher than GNA-PSC (72.40%).
    4. <strong>Efficiency:</strong> 9.38M parameters, 14.2 GFLOPs, 41.1 FPS in PyTorch FP32, and 88.5 FPS under TensorRT FP16 on an RTX 4090 GPU.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: MSBA-Net achieves state-of-the-art accuracy across all metrics while operating at real-time speeds with low computational overhead.</div>
</div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q9</span>
    What are the main limitations of MSBA-Net, and why did it collapse under Gaussian noise (2.33% mIoU)?
  </div>
  <div class="qa-a">
    In Section V of our paper, we honestly stress-tested the model under simulated shop-floor degradations. Performance dropped to 39.67% under low contrast, 26.29% under defocus blur, and collapsed to 2.33% under severe Gaussian noise (&sigma;=25).
    This collapse is an information-theoretic limitation:
    In clean steel, defect boundaries are defined by subtle gray-level transitions of only 5 to 15 intensity levels. Gaussian noise with &sigma;=25 creates random pixel fluctuations of &plusmn;50 intensity levels. Because our BAS boundary stream relies on differential edge operations, random noise creates thousands of spurious false edges, completely overwhelming the attention gating mechanism.
    <strong>Industrial Solution:</strong> In practice, rolling mills use sealed camera housings, active LED strobes, and front-end bilateral denoising filters before neural inference.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: Differential boundary convolutions inherently amplify random thermal noise; real-world deployment requires front-end bilateral filtering and clean lighting.</div>
</div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q10</span>
    What is the future scope and how can MSBA-Net be deployed on edge hardware in a factory?
  </div>
  <div class="qa-a">
    Our future research roadmap spans three phases:
    1. <strong>Spatio-Temporal Video Attention:</strong> Moving from static 2D images to temporal line-scan video feeds to leverage frame-to-frame defect continuity.
    2. <strong>Self-Supervised Pre-Training:</strong> Pre-training masked autoencoders (MAE) on massive uncurated industrial steel coils to learn robust metallurgical representations before supervised fine-tuning.
    3. <strong>Embedded Edge Deployment:</strong> Post-training INT8 quantization to compress the 9.38M model to under 10MB, enabling direct deployment on embedded industrial controllers such as the NVIDIA Jetson AGX Orin or FPGA acceleration boards at >100 FPS.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: MSBA-Net is lightweight and real-time ready, with clear pathways for INT8 edge quantization and spatio-temporal video extension.</div>
</div>

<div class="footer-note">
  MSBA-Net M.Tech (AIML) Research Seminar Script &amp; Examination Guide &bull; Amen Parmar &bull; Manipal University Jaipur &bull; 2026
</div>

</body>
</html>
"""

def main():
    print("Writing HTML script template for 13-slide presentation...")
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML saved to: {HTML_PATH}")

    print("Converting HTML to PDF via Microsoft Edge Headless...")
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={PDF_PATH}",
        "--no-margins",
        HTML_PATH
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error during PDF conversion: {result.stderr}")
        return False
    
    if os.path.exists(PDF_PATH):
        doc = fitz.open(PDF_PATH)
        print(f"SUCCESS: Generated {PDF_PATH}")
        print(f"Total Pages: {len(doc)}")
        for i in range(len(doc)):
            page = doc[i]
            print(f"  Page {i+1}: {page.rect.width} x {page.rect.height} pt, text length: {len(page.get_text())}")
        return True
    else:
        print("Failed to generate PDF!")
        return False

if __name__ == "__main__":
    main()
