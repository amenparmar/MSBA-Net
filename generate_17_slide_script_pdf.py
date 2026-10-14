"""
generate_17_slide_script_pdf.py
Generates the official Presentation Script & Examiner Viva Guide PDF for the 17-Slide MSBA-Net Presentation.
Output: MSBA-Net_Presentation_Script_Amen_Parmar.pdf
"""

import os
import subprocess
import fitz  # PyMuPDF

HTML_PATH = os.path.abspath("scratch/speaker_script_17.html")
PDF_PATH = os.path.abspath("MSBA-Net_Presentation_Script_Amen_Parmar.pdf")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>MSBA-Net Presentation Script & Viva Guide (17 Slides) — Amen Parmar</title>
<style>
  @page {
    size: A4;
    margin: 16mm 18mm 18mm 18mm;
    @bottom-right {
      content: counter(page);
    }
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1E293B;
    background-color: #FFFFFF;
    line-height: 1.5;
    font-size: 9.5pt;
    margin: 0;
    padding: 0;
  }

  /* Document Header */
  .doc-header {
    border-bottom: 2px solid #0B192C;
    padding-bottom: 12px;
    margin-bottom: 18px;
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
    margin-bottom: 6px;
  }
  .doc-title {
    font-size: 15pt;
    font-weight: 800;
    color: #0B192C;
    line-height: 1.25;
    margin: 0 0 6px 0;
  }
  .doc-subtitle {
    font-size: 10pt;
    color: #475569;
    font-weight: 600;
    margin: 0 0 10px 0;
  }
  .meta-grid {
    display: table;
    width: 100%;
    margin-top: 8px;
    font-size: 8.8pt;
    background: #F8F9FA;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 8px 12px;
  }
  .meta-row {
    display: table-row;
  }
  .meta-cell {
    display: table-cell;
    padding: 3px 6px;
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
    font-size: 12pt;
    font-weight: 800;
    color: #0B192C;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 1.5px solid #CBD5E1;
    padding-bottom: 4px;
    margin-top: 20px;
    margin-bottom: 12px;
  }

  /* Slide Script Card */
  .slide-box {
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    background: #FFFFFF;
    margin-bottom: 14px;
    page-break-inside: avoid;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
  }
  .slide-header {
    background: #F8F9FA;
    border-bottom: 1px solid #CBD5E1;
    padding: 6px 12px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    display: table;
    width: 100%;
    box-sizing: border-box;
  }
  .slide-title-wrap {
    display: table-cell;
    vertical-align: middle;
  }
  .slide-num {
    font-size: 8pt;
    font-weight: 700;
    color: #D97706;
    text-transform: uppercase;
  }
  .slide-title {
    font-size: 10.5pt;
    font-weight: 800;
    color: #0B192C;
    margin: 1px 0 0 0;
  }
  .slide-time {
    display: table-cell;
    vertical-align: middle;
    text-align: right;
    font-size: 8pt;
    font-weight: 700;
    color: #059669;
    white-space: nowrap;
  }
  .slide-body {
    padding: 10px 14px;
  }
  .cues-box {
    background: #F1F5F9;
    border-left: 3px solid #2563EB;
    padding: 5px 10px;
    margin-bottom: 8px;
    font-size: 8.2pt;
    color: #334155;
    border-radius: 0 4px 4px 0;
  }
  .cues-title {
    font-weight: 700;
    color: #1E293B;
  }
  .script-label {
    font-size: 8pt;
    font-weight: 700;
    text-transform: uppercase;
    color: #64748B;
    letter-spacing: 0.5px;
    margin-bottom: 3px;
  }
  .script-text {
    font-size: 9pt;
    color: #0B192C;
    text-align: justify;
    line-height: 1.5;
    margin: 0;
  }
  .script-text p {
    margin: 0 0 6px 0;
  }
  .script-text p:last-child {
    margin-bottom: 0;
  }
  .transition-box {
    margin-top: 6px;
    padding: 4px 8px;
    background: #EFF6FF;
    border-left: 3px solid #3B82F6;
    font-size: 7.8pt;
    color: #1E40AF;
    border-radius: 0 4px 4px 0;
  }

  /* Q&A Section */
  .qa-card {
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    background: #FFFFFF;
    margin-bottom: 10px;
    page-break-inside: avoid;
    padding: 9px 12px;
  }
  .qa-q {
    font-size: 9.5pt;
    font-weight: 700;
    color: #0B192C;
    margin: 0 0 4px 0;
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
    line-height: 1.46;
    margin: 0;
    text-align: justify;
  }
  .qa-key {
    margin-top: 4px;
    font-size: 7.8pt;
    font-weight: 700;
    color: #059669;
  }

  .page-break {
    page-break-before: always;
  }

  .footer-note {
    font-size: 7.8pt;
    color: #64748B;
    text-align: center;
    margin-top: 14px;
    border-top: 1px solid #E2E8F0;
    padding-top: 6px;
  }
</style>
</head>
<body>

<!-- DOCUMENT HEADER -->
<div class="doc-header">
  <div class="doc-badge">M.Tech (AIML) Research Seminar Presentation Script &amp; Viva Guide</div>
  <h1 class="doc-title">MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation</h1>
  <div class="doc-subtitle">Complete Defense Presentation Script (17 Slides), Spoken Transitions, and Examiner Viva Q&amp;A</div>

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
      <div class="meta-cell meta-label">Affiliation:</div>
      <div class="meta-cell meta-val">Department of Computer Science and Engineering, Manipal University Jaipur</div>
    </div>
    <div class="meta-row">
      <div class="meta-cell meta-label">Target Duration:</div>
      <div class="meta-cell meta-val"><strong>10 – 12 Minutes</strong> (~40–50 seconds per slide) + Committee Discussion</div>
    </div>
  </div>
</div>

<!-- ========================================== -->
<!-- SLIDE-BY-SLIDE SCRIPT (17 SLIDES) -->
<!-- ========================================== -->
<div class="section-heading">Part 1: Slide-by-Slide Spoken Script (17 Slides)</div>

<!-- SLIDE 1 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 1 of 17</div>
      <div class="slide-title">Title Slide — Introduction &amp; Credentials</div>
    </div>
    <div class="slide-time">Target: 35–45 sec | Cumulative: 0:00 – 0:45</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Clean open title slide; author credentials, paper co-authors, Manipal University Jaipur affiliation, and subtle NEU defect teaser on right.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Good morning, respected committee members, faculty advisors, and esteemed examiners. My name is Amen Parmar, Roll Number 2502010010, pursuing my M.Tech in Artificial Intelligence and Machine Learning in the Department of Computer Science and Engineering at Manipal University Jaipur.</p>
      <p>Today, I have the honor of presenting our research paper titled: <strong>'MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation'</strong>, co-authored with Dr. Amit Kumar Bairwa and Dr. Varun Kumar.</p>
      <p>This work proposes a boundary-preserving deep semantic segmentation architecture engineered specifically for the challenging conditions of industrial metallurgical visual inspection."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 2:</strong> "To begin, allow me to outline the primary research objectives that motivated our work."
    </div>
  </div>
</div>

<!-- SLIDE 2 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 2 of 17</div>
      <div class="slide-title">Objective — Core Research Goals</div>
    </div>
    <div class="slide-time">Target: 40–50 sec | Cumulative: 0:45 – 1:30</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> 4 clean academic bullet points + bottom focus callout pill.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Our primary objective is to develop an effective deep semantic segmentation framework tailored specifically for small and low-contrast steel surface defects.</p>
      <p>Specifically, our goals are fourfold:
      First, to preserve fine-grained structural defect features that are commonly lost during conventional downsampling and pooling stages.
      Second, to improve spatial boundary localization and eliminate border bleeding around faint, low-contrast, and blurred defect contours.
      Third, to address the severe foreground-background class imbalance where defects occupy less than one percent of the surface.
      And fourth, to rigorously validate the proposed MSBA-Net on the benchmark NEU surface defect database against existing state-of-the-art models.</p>
      <p>Our central focus is achieving accurate pixel-level segmentation of microscopic defects without sacrificing boundary contour precision."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 3:</strong> "Now let us examine the industrial background and why automated visual inspection is vital in steel manufacturing."
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- SLIDE 3 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 3 of 17</div>
      <div class="slide-title">Brief Overview — Industrial Background</div>
    </div>
    <div class="slide-time">Target: 40–50 sec | Cumulative: 1:30 – 2:15</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> 4 background bullets on left; actual Crazing raw image and defect mask from NEU benchmark on right.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"In continuous hot and cold rolling steel mills, automated visual inspection is critical for quality assurance. Undetected surface defects can lead to catastrophic structural failure during automotive stamping or heavy structural construction.</p>
      <p>However, industrial steel defects present extreme imaging difficulties. As shown in the sample on the right, defects such as hairline crazing cracks frequently occupy less than 1% of the total image area.</p>
      <p>Furthermore, gray-level intensity contrast between the defect and the surrounding rolled steel is exceptionally subtle. Conventional encoder-decoder networks struggle here because successive pooling operations wash away these fine spatial gradients, resulting in missed micro-flaws."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 4:</strong> "Let us now formalize the core technical problem statement."
    </div>
  </div>
</div>

<!-- SLIDE 4 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 4 of 17</div>
      <div class="slide-title">Problem Statement — Technical Obstacles</div>
    </div>
    <div class="slide-time">Target: 45–55 sec | Cumulative: 2:15 – 3:05</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> 4 focused problem bullets + red warning summary pill at bottom.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"We identify four critical technical obstacles that plague metallurgical defect segmentation:</p>
      <p>First, micro-scale flaw size: defects frequently occupy less than 1% of the total image area—under 655 pixels at standard 256×256 resolution. Standard receptive fields aggregate background metal texture, diluting tiny defect signals.</p>
      <p>Second, low-contrast boundaries: intensity transitions between defect perimeters and steel textures are often as small as 5 to 15 gray levels, causing severe border bleeding.</p>
      <p>Third, downsampling feature loss: repeated striding in deep backbones destroys high-frequency spatial gradients before reaching deep layers.</p>
      <p>And fourth, extreme class imbalance: over 98% of pixels belong to defect-free steel background, heavily biasing standard loss gradients away from small defects."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 5:</strong> "Having identified these challenges, let us look at the research gap in existing approaches."
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- SLIDE 5 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 5 of 17</div>
      <div class="slide-title">Research Gap — Limitations &amp; The Research Need</div>
    </div>
    <div class="slide-time">Target: 40–50 sec | Cumulative: 3:05 – 3:55</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Two clean columns: Limitations of Existing Methods (left) vs The Unmet Research Need (right) + bottom research need banner.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"When we survey existing segmentation models like standard U-Net, DeepLab, or generic industrial CNNs, we observe critical research gaps.</p>
      <p>First, existing models sacrifice fine spatial details for broad semantic context through aggressive downsampling. Second, boundary information is treated only implicitly through standard skip connections, causing blurred contours. And third, while models report acceptable overall mIoU, performance on tiny defects degrades by 10% to 25%, masking failures on safety-critical flaws.</p>
      <p>This establishes our clear research need: we require a lightweight framework that simultaneously achieves multi-scale feature preservation at native resolution and explicit boundary guidance to sharpen defect contours."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 6:</strong> "To fulfill this research need, we propose our novel architecture: MSBA-Net."
    </div>
  </div>
</div>

<!-- SLIDE 6 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 6 of 17</div>
      <div class="slide-title">Proposed Approach — MSBA-Net Architecture</div>
    </div>
    <div class="slide-time">Target: 50–60 sec | Cumulative: 3:55 – 4:55</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Clean editable dual-stream flowchart: Main Backbone (top) with MSFP modules, Bottleneck, Decoder; Auxiliary Boundary Stream (bottom) with BAS and BGFF gating into decoder.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Slide 6 presents the overarching architecture of MSBA-Net. The framework adopts a dual-stream design combining a multi-scale semantic backbone with a dedicated boundary-aware pathway.</p>
      <p>Along the main stream, the input image passes through Encoder Stages 1 through 4. Crucially, Stages 1 and 2 incorporate our Multi-Scale Feature Preservation (MSFP) modules to capture multi-scale spatial details without downsampling loss.</p>
      <p>In parallel, the auxiliary Boundary-Aware Stream (BAS) branches off early high-resolution stages. It explicitly learns defect boundary contours under direct boundary supervision. The extracted boundary features then enter our Boundary-Guided Feature Fusion (BGFF) module, which applies spatial attention gating to sharpen decoder features and eliminate background bleeding.</p>
      <p>With only 9.38M parameters, MSBA-Net remains compact and achieves real-time inference speeds."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 7:</strong> "Let us now dive deeper into the first core innovation: the MSFP module."
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- SLIDE 7 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 7 of 17</div>
      <div class="slide-title">Multi-Scale Feature Preservation (MSFP)</div>
    </div>
    <div class="slide-time">Target: 45–55 sec | Cumulative: 4:55 – 5:45</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Diagram showing input feature map splitting across 3 parallel dilated branches (r=1, 2, 4) and 1×1 fusion, with 4 explanatory bullets on right.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Slide 7 details our Multi-Scale Feature Preservation (MSFP) module. Standard pooling operations reduce spatial dimensions, permanently discarding hairline crack features. MSFP solves this by operating entirely at native spatial resolution.</p>
      <p>As shown in the diagram, incoming feature map F_in is split across three parallel dilated depthwise convolution branches with dilation rates r ∈ {1, 2, 4}:
      Branch 1 with r=1 provides a 3×3 receptive field, capturing fine hairline crazing cracks;
      Branch 2 with r=2 provides a 5×5 field for pit depressions and small inclusions;
      And Branch 3 with r=4 provides a 9×9 field for broad patches and rolled-in scale sheets.</p>
      <p>Crucially, dilation rates {1, 2, 4} strictly satisfy the Hybrid Dilated Convolution (HDC) condition, ensuring continuous pixel coverage without the checkerboard gridding artifacts common in dilated networks. The branches are concatenated and fused via 1×1 pointwise convolution."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 8:</strong> "Next, let us examine our second core innovation: the Boundary-Aware Stream and BGFF module."
    </div>
  </div>
</div>

<!-- SLIDE 8 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 8 of 17</div>
      <div class="slide-title">Boundary-Aware Learning — BAS &amp; BGFF</div>
    </div>
    <div class="slide-time">Target: 45–55 sec | Cumulative: 5:45 – 6:35</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Flow diagram showing early features entering BAS under auxiliary boundary loss, followed by BGFF spatial attention gating; 4 bullets on right.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Slide 8 illustrates our boundary-aware learning mechanism, comprising the Boundary-Aware Stream (BAS) and Boundary-Guided Feature Fusion (BGFF).</p>
      <p>BAS taps early encoder features from Stages 1 and 2 where spatial resolution is highest (256×256 and 128×128). An auxiliary boundary loss supervises BAS directly against 1-pixel morphological defect contours, injecting edge gradients directly into shallow layers before deep semantic pooling can wash them out.</p>
      <p>The resulting boundary tensor F_bound enters BGFF, where it is concatenated with decoder features F_dec. A 1×1 convolution and sigmoid activation produce a 2D spatial attention map A_spat. Decoder features are then recalibrated via residual attention: F_out = F_dec ⊙ (1 + A_spat).</p>
      <p>Along defect perimeters, attention gain is amplified, producing razor-sharp contours. Over uniform steel background, attention drops to zero, effectively suppressing false-positive border bleeding."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 9:</strong> "Now let us turn to the experimental validation, beginning with the benchmark dataset."
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- SLIDE 9 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 9 of 17</div>
      <div class="slide-title">Experimental Work — Dataset Specifications</div>
    </div>
    <div class="slide-time">Target: 40–50 sec | Cumulative: 6:35 – 7:20</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Dataset specifications bullets on left; clean 6-row table showing all defect classes and their morphological characteristics on right.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"For experimental validation, we evaluated MSBA-Net on the NEU Surface Defect Database developed by Northeastern University, the recognized benchmark in metallurgical vision research.</p>
      <p>The database comprises 1,800 grayscale industrial images, perfectly balanced with exactly 300 images across each of the six canonical industrial defect categories shown in the table on the right: Crazing, Inclusions, Patches, Pitted Surfaces, Rolled-in Scale, and Scratches.</p>
      <p>Original 200×200 images were standardized to 256×256 pixels. We adopted a standard, non-overlapping split of 70% for training (1,260 images), 15% for validation (270 images), and 15% for independent testing (270 images) under identical protocols as published literature."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 10:</strong> "Next, let us look at our training setup and computational complexity."
    </div>
  </div>
</div>

<!-- SLIDE 10 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 10 of 17</div>
      <div class="slide-title">Experimental Setup — Training &amp; Complexity</div>
    </div>
    <div class="slide-time">Target: 40–50 sec | Cumulative: 7:20 – 8:05</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Two-column layout: Training Protocol on left (PyTorch, RTX 4090, AdamW, Cosine Annealing); Model Complexity on right (9.38M params, 14.2 GFLOPs, 41.1/88.5 FPS).
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Slide 10 outlines our experimental training configuration and model complexity profile.</p>
      <p>Training was implemented in PyTorch 2.1 on a single NVIDIA GeForce RTX 4090 GPU with 24GB VRAM. We used the AdamW optimizer with initial learning rate 1×10⁻³ and Cosine Annealing decay down to 1×10⁻⁶ over 100 epochs with batch size 16.</p>
      <p>In terms of computational efficiency, MSBA-Net contains only 9.38 Million parameters and requires 14.2 GFLOPs per forward pass. Latency is just 24.3 milliseconds, achieving 41.1 FPS in PyTorch FP32 and 88.5 FPS under TensorRT FP16 quantization. This comfortably exceeds the 30 FPS threshold required for real-time rolling-mill line-scan deployment."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 11:</strong> "Before discussing results, let us review the evaluation metrics used."
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- SLIDE 11 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 11 of 17</div>
      <div class="slide-title">Evaluation Metrics — Dedicated Micro-Defect Assessment</div>
    </div>
    <div class="slide-time">Target: 40–50 sec | Cumulative: 8:05 – 8:50</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> 4 clean metric bullets (mIoU, Dice, Precision/Recall, Tiny-Defect mIoU) + bottom callout pill explaining why Tiny-Defect mIoU is essential.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Slide 11 defines the evaluation metrics used in our paper.</p>
      <p>We report Mean Intersection over Union (mIoU) as our primary benchmark metric, along with the Dice similarity coefficient to measure region overlap, and Precision and Recall to evaluate false positives versus missed detections.</p>
      <p>Crucially, we introduce Tiny-Defect mIoU as an essential metric. Because overall mIoU is area-weighted, large defects like broad patches can easily mask complete segmentation failures on hairline cracks. Tiny-Defect mIoU specifically evaluates performance exclusively on defect regions occupying less than 1% of the image area—under 655 pixels—providing an unvarnished assessment of micro-flaw preservation."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 12:</strong> "Let us now examine the quantitative results and compare MSBA-Net with existing methods."
    </div>
  </div>
</div>

<!-- SLIDE 12 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 12 of 17</div>
      <div class="slide-title">Results — Comparison with Existing Methods</div>
    </div>
    <div class="slide-time">Target: 50–60 sec | Cumulative: 8:50 – 9:45</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Native editable column chart of 6 models on left; compact comparison table and 3 key observations on right (97.01% mIoU, 98.48% Dice, 92.48% Tiny mIoU).
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Slide 12 benchmarks MSBA-Net against leading published steel defect segmentation architectures on the NEU test set.</p>
      <p>As shown in the bar chart on the left, MSBA-Net establishes a new state-of-the-art benchmark, reaching 97.01% mIoU. This outperforms the previous 2026 leader, DMS-UNet at 94.20%, by a decisive margin of +2.81%, and surpasses DAMF-Net (91.65%) by +5.36%.</p>
      <p>Looking at the table on the right, Dice coefficient reaches 98.48%, with 97.57% Precision and 99.41% Recall, confirming near-zero missed defects.</p>
      <p>Most impressively, Tiny-Defect mIoU reaches 92.48%—a +4.08% improvement over DMS-UNet and more than 20% higher than earlier models like GNA-PSC (72.40%). This validates that our architectural enhancements directly solve the micro-defect preservation challenge."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 13:</strong> "Let us now inspect per-class performance across individual defect categories."
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- SLIDE 13 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 13 of 17</div>
      <div class="slide-title">Results — Per-Class Analysis</div>
    </div>
    <div class="slide-time">Target: 45–55 sec | Cumulative: 9:45 – 10:35</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Clean per-class table on left; clean 2-row qualitative visual comparison (Crazing &amp; Inclusions) on right comparing Input, GT, Baseline, and MSBA-Net.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Slide 13 breaks down segmentation performance across the six individual defect categories.</p>
      <p>Performance remains exceptionally consistent, exceeding 96.4% across all six classes: Patches achieved the highest score at 97.85%, followed by Inclusions at 97.15%, Scratches at 97.12%, Pitted Surfaces at 96.80%, Rolled-in Scale at 96.72%, and Crazing at 96.42%.</p>
      <p>Patches perform highest because of continuous, homogeneous defect regions. Crazing is relatively the most challenging due to complex branching hairline fissures.</p>
      <p>The qualitative comparison on the right highlights this clearly: while baseline U-Net suffers severe boundary bleeding and fails on disconnected fissures, MSBA-Net traces fine branching cracks with razor-sharp boundary alignment."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 14:</strong> "To confirm that each proposed module contributes to this success, let us examine the ablation study."
    </div>
  </div>
</div>

<!-- SLIDE 14 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 14 of 17</div>
      <div class="slide-title">Ablation Study &amp; Analysis</div>
    </div>
    <div class="slide-time">Target: 45–55 sec | Cumulative: 10:35 – 11:25</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Native grouped bar chart on left (Overall vs Tiny mIoU across 4 configurations); progression table and 3 takeaways on right.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Slide 14 presents our systematic ablation study, evaluating the progressive contribution of each architectural component.</p>
      <p>Starting with our Baseline Backbone, the model achieves 94.10% overall mIoU, but only 84.60% on Tiny-Defect mIoU.
      When we add the MSFP module, overall mIoU increases to 95.85% (+1.75%), while Tiny-Defect mIoU leaps by a massive +5.05% to 89.65%. This proves that multi-scale dilated convolutions at native resolution are the primary driver of micro-defect retention.</p>
      <p>Next, incorporating the Boundary-Aware Stream (BAS) lifts overall mIoU to 96.48% and Tiny mIoU to 91.20% (+1.55%), confirming the benefit of explicit edge supervision.</p>
      <p>Finally, adding Boundary-Guided Feature Fusion (BGFF) delivers our full MSBA-Net model at 97.01% overall mIoU and 92.48% Tiny mIoU, validating that each proposed component provides a statistically verified, cumulative gain."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 15:</strong> "Next, we present an honest analysis of model limitations and robustness."
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- SLIDE 15 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 15 of 17</div>
      <div class="slide-title">Limitations &amp; Robustness Analysis</div>
    </div>
    <div class="slide-time">Target: 45–55 sec | Cumulative: 11:25 – 12:15</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Stress-test degradation table on left (Normal 97.01%, Low contrast 39.67%, Blur 26.29%, Gaussian noise 2.33%); 3 academic limitation bullets on right.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Slide 15 provides an honest academic evaluation of model limitations under simulated shop-floor optical and sensor degradations.</p>
      <p>While MSBA-Net excels on clean benchmark imagery, performance degrades significantly under severe environmental stress: mIoU drops to 39.67% under low contrast, 26.29% under optical defocus blur, and collapses to 2.33% under severe Gaussian noise (σ=25).</p>
      <p>This collapse is an inherent information-theoretic property: in clean steel, defect boundaries are defined by subtle transitions of only 5 to 15 intensity levels. Severe Gaussian noise creates random pixel fluctuations of ±50 gray levels. Because our BAS boundary stream relies on differential edge operations, random noise creates thousands of spurious false edges, overwhelming the attention gating mechanism.</p>
      <p>Consequently, real-world rolling-mill deployment strictly requires front-end bilateral denoising filters, sealed camera enclosures, and high-frequency LED strobe illumination."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 16:</strong> "Finally, let us summarize our conclusions and future research directions."
    </div>
  </div>
</div>

<!-- SLIDE 16 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 16 of 17</div>
      <div class="slide-title">Conclusion &amp; Future Work</div>
    </div>
    <div class="slide-time">Target: 45–55 sec | Cumulative: 12:15 – 13:05</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Two clean columns: Research Conclusions (left) vs Future Research Directions (right).
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"To conclude our presentation:
      First, MSBA-Net successfully unites multi-scale feature preservation (MSFP) with boundary-aware learning (BAS + BGFF).
      Second, MSFP preserves micro-scale flaws occupying less than 1% area without downsampling dilution.
      Third, the architecture establishes a new state-of-the-art benchmark on the NEU dataset, delivering 97.01% mIoU, 98.48% Dice, and 92.48% Tiny-Defect mIoU.
      And fourth, it operates at 41.1 FPS in PyTorch FP32 and 88.5 FPS under TensorRT FP16 with only 9.38M parameters, validating real-time industrial viability.</p>
      <p>Our future research directions include:
      1. Extending MSBA-Net to continuous line-scan video feeds using spatio-temporal video attention.
      2. Self-supervised pre-training on large uncurated industrial steel coils.
      3. Implementing INT8 post-training quantization for deployment on embedded edge boards like NVIDIA Jetson AGX Orin.
      And 4. Integrating adaptive front-end denoising to harden boundary convolutions against sensor noise."</p>
    </div>
    <div class="transition-box">
      <strong>Spoken Transition to Slide 17:</strong> "Thank you for your attention. I am now ready for questions."
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- SLIDE 17 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 17 of 17</div>
      <div class="slide-title">Thank You — Questions &amp; Discussion</div>
    </div>
    <div class="slide-time">Target: 25–35 sec | Cumulative: 13:05 – 13:35</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Minimal, open Thank You slide with 'Questions &amp; Discussion' subtitle; candidate name, M.Tech degree, roll number, and department.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Thank you very much, respected committee members and professors, for your time, patience, and kind attention.</p>
      <p>I would be delighted and honored to take any questions, comments, or constructive suggestions regarding our research."</p>
    </div>
  </div>
</div>

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
    MSFP replaces standard single-receptive convolution layers with parallel dilated depthwise convolutions at native spatial resolution. Each branch addresses a distinct defect scale:
    r=1 gives a 3×3 receptive field for hairline crazing cracks;
    r=2 gives a 5×5 field for pit depressions and small inclusions;
    r=4 gives a 9×9 field for broad patches and rolled-in scale sheets.
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
    BAS branches off early from Stages 1 and 2 where spatial resolution is highest (256×256 and 128×128). It is kept auxiliary for two reasons:
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
    BGFF is the spatial attention mechanism that transfers boundary knowledge from the BAS stream into the decoder. It concatenates the boundary feature tensor F_bound with the decoder feature tensor F_dec, passes them through a 1×1 convolution, and applies a sigmoid activation to yield a 2D spatial attention map:
    <code>A_spat = σ(Conv_1×1([F_bound ; F_dec]))</code>.
    The decoder features are then recalibrated via residual attention:
    <code>F_out = F_dec ⊙ (1 + A_spat)</code>.
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
    In Section V of our paper, we honestly stress-tested the model under simulated shop-floor degradations. Performance dropped to 39.67% under low contrast, 26.29% under defocus blur, and collapsed to 2.33% under severe Gaussian noise (σ=25).
    This collapse is an information-theoretic limitation:
    In clean steel, defect boundaries are defined by subtle gray-level transitions of only 5 to 15 intensity levels. Gaussian noise with σ=25 creates random pixel fluctuations of ±50 intensity levels. Because our BAS boundary stream relies on differential edge operations, random noise creates thousands of spurious false edges, completely overwhelming the attention gating mechanism.
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
    print("Writing HTML script template for 17-slide presentation...")
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
