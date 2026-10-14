"""
generate_script_pdf.py
Generates the comprehensive, professional Presentation Script & Viva Q&A PDF for MSBA-Net.
Output: MSBA-Net_Presentation_Script_Amen_Parmar.pdf
"""

import os
import subprocess
import fitz  # PyMuPDF

HTML_PATH = os.path.abspath("scratch/speaker_script.html")
PDF_PATH = os.path.abspath("MSBA-Net_Presentation_Script_Amen_Parmar.pdf")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>MSBA-Net Presentation Script & Viva Guide — Amen Parmar</title>
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
    font-size: 17pt;
    font-weight: 800;
    color: #0B192C;
    line-height: 1.25;
    margin: 0 0 8px 0;
  }
  .doc-subtitle {
    font-size: 11pt;
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
    font-size: 13pt;
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
    font-size: 11.5pt;
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
  .tip-box {
    margin-top: 8px;
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
    margin-bottom: 14px;
    page-break-inside: avoid;
    padding: 12px 14px;
  }
  .qa-q {
    font-size: 10pt;
    font-weight: 700;
    color: #0B192C;
    margin: 0 0 6px 0;
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
    font-size: 9pt;
    color: #334155;
    line-height: 1.55;
    margin: 0;
    text-align: justify;
  }
  .qa-key {
    margin-top: 6px;
    font-size: 8pt;
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
  <div class="doc-badge">M.Tech (AIML) Research Paper Presentation Script & Viva Guide</div>
  <h1 class="doc-title">MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation</h1>
  <div class="doc-subtitle">Official Defense Presentation Script, Slide-by-Slide Timing, and Examiner Viva Q&amp;A</div>

  <div class="meta-grid">
    <div class="meta-row">
      <div class="meta-cell meta-label">Presenter:</div>
      <div class="meta-cell meta-val"><strong>Amen Parmar</strong> | M.Tech (AIML) | Registration / Roll No: <strong>2502010010</strong></div>
    </div>
    <div class="meta-row">
      <div class="meta-cell meta-label">Paper Authors:</div>
      <div class="meta-cell meta-val">Amen Parmar, Amit Kumar Bairwa, Varun Kumar</div>
    </div>
    <div class="meta-row">
      <div class="meta-cell meta-label">Affiliation:</div>
      <div class="meta-cell meta-val">Department of Computer Science and Engineering, Manipal University Jaipur, Jaipur, Rajasthan, India</div>
    </div>
    <div class="meta-row">
      <div class="meta-cell meta-label">Target Duration:</div>
      <div class="meta-cell meta-val"><strong>10 – 12 Minutes</strong> (approx. 55–75 seconds per slide) + 5–10 Minutes Committee Q&amp;A</div>
    </div>
  </div>
</div>

<!-- ========================================== -->
<!-- SLIDE-BY-SLIDE SCRIPT -->
<!-- ========================================== -->
<div class="section-heading">Part 1: Slide-by-Slide Spoken Script (11 Slides)</div>

<!-- SLIDE 1 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 1 of 11</div>
      <div class="slide-title">Title Slide — Introduction & Overview</div>
    </div>
    <div class="slide-time">Target: 45–55 sec | Elapsed: 0:00 – 0:50</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Title banner on left; 3-stage visual diagram on right (Raw Steel Strip &rarr; Micro-Defect Region &rarr; Pixel-Level Binary Mask); author &amp; department details.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Respected session chair, esteemed members of the evaluation committee, and fellow scholars: Good morning.</p>
      <p>My name is Amen Parmar, M.Tech in Artificial Intelligence and Machine Learning at Manipal University Jaipur, Roll Number 2502010010. Today, I am honored to present our research paper entitled: <em>'MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation'</em>, co-authored with Dr. Amit Kumar Bairwa and Dr. Varun Kumar.</p>
      <p>Automated surface quality inspection of flat-rolled steel is an indispensable foundation of modern metallurgy, automotive manufacturing, and structural engineering. In this presentation, I will introduce MSBA-Net—a specialized deep neural architecture specifically engineered to conquer the two most obstinate failure modes in industrial optical inspection: microscopic defect scale and near-zero boundary contrast. Over the next eleven minutes, I will outline the industrial problem, walk you through our architectural design, examine our experimental benchmark results on the NEU database, and share transparent insights from our shop-floor stress testing."</p>
    </div>
    <div class="tip-box">
      <strong>Viva Delivery Tip:</strong> Stand tall, maintain eye contact with all committee members, speak at a calm 130 words per minute, and emphasize the dual keywords: <em>Multi-Scale Feature Enhancement</em> and <em>Boundary-Aware Learning</em>.
    </div>
  </div>
</div>

<!-- SLIDE 2 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 2 of 11</div>
      <div class="slide-title">Motivation & Problem — Why Steel Surface Defect Segmentation?</div>
    </div>
    <div class="slide-time">Target: 60–75 sec | Elapsed: 0:50 – 2:00</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> 5-stage industrial operational chain; 4 numerical fact cards (15–20 m/s strip speed, &lt;1% micro-defect area, low contrast gradients, &gt;98% normal background pixels); gallery of 6 NEU defect categories.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"To appreciate why this research is vital, let us examine the harsh operational realities of a high-speed continuous casting and hot-strip rolling mill.</p>
      <p>Steel strips travel beneath optical inspection cameras at blistering line speeds between 15 and 20 meters per second—that is up to 72 kilometers per hour. At such velocities, manual human visual inspection is physically impossible. Quality assurance must rely entirely on automated line-scan optical systems operating in real time.</p>
      <p>However, automated vision systems face four profound challenges, summarized in our dashboard:
      First, line velocity demands inference latencies well below 25 milliseconds.
      Second, the defects of highest safety consequence—such as hairline crazing cracks or microscopic pit clusters—occupy less than 1% of the entire image canvas.
      Third, defect perimeters exhibit extremely faint, gradual intensity transitions against the textured steel background, meaning edge contrast is remarkably low.
      Fourth, over 98% of all captured pixels are completely defect-free steel, creating overwhelming foreground-background class imbalance.</p>
      <p>At the bottom of the slide, you see the six primary defect classes from the NEU benchmark: Crazing, Inclusions, Patches, Pitted Surfaces, Rolled-in Scale, and Scratches. If an automated algorithm misses a sub-1% hairline crack, that steel coil will be shipped to an automotive stamping plant, where it will undergo deep drawing, suffer sudden catastrophic structural tear, and cause millions of dollars in mechanical failure. Precise, pixel-level defect segmentation is therefore an imperative safety requirement."</p>
    </div>
    <div class="tip-box">
      <strong>Viva Delivery Tip:</strong> Highlight the contrast between 'fast line speeds' and 'sub-1% flaw size' to establish why conventional generic segmentation models fail.
    </div>
  </div>
</div>

<!-- SLIDE 3 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 3 of 11</div>
      <div class="slide-title">Key Challenges & Research Gap — Why Existing Methods Struggle</div>
    </div>
    <div class="slide-time">Target: 55–65 sec | Elapsed: 2:00 – 3:00</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> 3 large diagnostic cards (Micro-Scale Defects, Low-Contrast Boundaries, Optical Degradation); Downsampling Dilemma flowchart vs Architectural Requirements.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Why can we not simply deploy a standard off-the-shelf semantic segmentation network like U-Net, DeepLabV3+, or SegNet? Slide 3 answers this fundamental question by diagnosing the core architectural bottlenecks.</p>
      <p>Standard deep CNNs are designed around successive pooling and strided convolutions to expand receptive fields for macro-scene understanding. But in steel surface inspection, this downsampling hierarchy creates a fatal dilemma:
      By the time an image passes through four downsampling stages—reducing spatial resolution by a factor of 16—a hairline craze crack that was originally 2 pixels wide is reduced to a fractional spatial artifact. It is completely obliterated from the feature map. This is what we define as <em>feature dilution</em>.</p>
      <p>Simultaneously, standard cross-entropy loss functions treat all pixels uniformly. Because background steel accounts for over 98% of the image, the network's optimization gradient is completely dominated by uniform steel metal, leaving the weak, low-contrast boundary gradients unattended. The consequence is severe boundary bleeding, fragmented crack masks, and missed sub-1% flaws.</p>
      <p>This establishes our clear research gap: We need an architecture that preserves micro-scale spatial resolution across multiple scales simultaneously, while explicitly supervising high-frequency boundary contours through dedicated guidance."</p>
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- SLIDE 4 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 4 of 11</div>
      <div class="slide-title">Proposed Solution — MSBA-Net Overview</div>
    </div>
    <div class="slide-time">Target: 55–65 sec | Elapsed: 3:00 – 4:00</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> 3-part conceptual system diagram: Input &rarr; MSFP (Green) + BAS (Orange) &rarr; BGFF (Purple) &rarr; Decoder &rarr; Binary Mask; Core Takeaway banner at bottom.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"To address this research gap, we introduce MSBA-Net—Multi-Scale Feature Enhancement and Boundary-Aware Network.</p>
      <p>As illustrated in this conceptual diagram, our framework is founded upon three tightly coupled architectural pillars that work in complete synergy:</p>
      <p>First, <strong>MSFP—Multi-Scale Feature Preservation</strong>: Integrated directly into the encoder hierarchy, MSFP replaces standard convolutions with parallel dilated depthwise convolution branches. This preserves fine 1-to-2 pixel crack details while simultaneously capturing macro-level patch context without requiring destructive spatial downsampling.</p>
      <p>Second, <strong>BAS—Boundary-Aware Stream</strong>: An auxiliary stream that branches off early from high-resolution encoder features. BAS explicitly extracts high-frequency structural contours and predicts a dedicated boundary probability map under direct morphological edge supervision.</p>
      <p>Third, <strong>BGFF—Boundary-Guided Feature Fusion</strong>: A spatial attention gating mechanism that bridges the boundary stream and the decoder. BGFF takes the learned boundary features to dynamically compute spatial attention weights, amplifying decoder features along uncertain defect margins while suppressing noise from uniform steel textures.</p>
      <p>In short: MSFP preserves fine features, BAS extracts boundaries, and BGFF guides decoder reconstruction. Let us now examine the exact architectural implementation."</p>
    </div>
  </div>
</div>

<!-- SLIDE 5 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 5 of 11</div>
      <div class="slide-title">MSBA-Net Architecture — Complete System Schematic</div>
    </div>
    <div class="slide-time">Target: 75–90 sec | Elapsed: 4:00 – 5:25</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Fully editable architectural schematic (Figure 1 recreation). Top row: BAS stream &rarr; Boundary Head &rarr; BGFF Gate &rarr; Loss Supervision; Middle row: 4-stage MSFP Encoder &rarr; Bottleneck &rarr; Decoder &rarr; Output Mask; Bottom panel: 5-branch breakdown of MSFP block (1x1 projection, r=1, r=2, r=4, residual aggregation).
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"This slide presents the complete architectural schematic of MSBA-Net, faithfully recreated from Figure 1 of our paper.</p>
      <p>Let us trace the forward data path:
      In the middle row, the input 256x256 grayscale steel image enters a four-stage hierarchical encoder. Crucially, each encoder stage incorporates an MSFP block. Notice how the channel dimensions evolve from 32 in Stage 1, to 64 in Stage 2, 128 in Stage 3, and 256 at the dilated bottleneck, while maintaining spatial feature integrity.</p>
      <p>Now observe the auxiliary top row: the Boundary-Aware Stream (BAS). Rather than waiting for deeper layers where spatial detail is lost, BAS taps features directly from Stages 1 and 2 where pristine 256x256 and 128x128 resolution remains intact. BAS processes these features through up-convolutions and a dedicated Boundary Head, generating a full-resolution 256x256 boundary probability map, denoted as P_bound.</p>
      <p>This boundary representation feeds directly into the BGFF gate, which generates a 64x128x128 spatial attention tensor. During decoder upsampling, this attention tensor modulates the skip-connection features before they enter the final decoding layers, ensuring that decoder reconstructions are strictly focused on boundary margins.</p>
      <p>At the bottom panel, we detail the internal anatomy of each MSFP block:
      Input channels are split into four parallel paths:
      Branch 1 applies a 1x1 convolution for linear feature transfer.
      Branch 2 uses a 3x3 dilated convolution with dilation rate r=1, yielding a 3x3 receptive field tailored for hairline crazing.
      Branch 3 uses dilation r=2, expanding the receptive field to 5x5 for inclusions and pit clusters.
      Branch 4 uses dilation r=4, creating a 9x9 receptive field to capture broad rolled-in scale sheets.
      Finally, all branches are concatenated, projected back to C channels, and combined with an identity residual connection. This multi-receptive design captures every defect scale without gridding artifacts or excessive FLOPs."</p>
    </div>
    <div class="tip-box">
      <strong>Viva Delivery Tip:</strong> Point clearly to the top branch (BAS) and the bottom panel (MSFP branches) to demonstrate mastery of how the parallel streams interact.
    </div>
  </div>
</div>

<!-- SLIDE 6 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 6 of 11</div>
      <div class="slide-title">Three Key Components — Mathematical Intuition of MSFP, BAS, BGFF</div>
    </div>
    <div class="slide-time">Target: 70–80 sec | Elapsed: 5:25 – 6:40</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> 3 parallel cards: Card A (MSFP mathematical formula, parallel depthwise mechanics, r=1/2/4); Card B (BAS mathematical morphological gradient formula, 1-pixel edge ground truth, explicit supervision); Card C (BGFF spatial attention equation, residual modulation formula, border bleeding prevention).
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Let us now examine the mathematical mechanics governing our three core components, shown on Slide 6.</p>
      <p>In Section A, we formulate the Multi-Scale Feature Preservation block:
      Each sub-branch B_k applies a dilated depthwise convolution with dilation rate r_k belonging to the set {1, 2, 4}. By mathematically capping the maximum dilation rate at 4 and employing consecutive rates {1, 2, 4}, we satisfy the Hybrid Dilated Convolution condition, strictly preventing the checkerboard gridding artifacts that plague standard dilated architectures. The branches are concatenated and aggregated through a residual identity addition.</p>
      <p>In Section B, how do we mathematically define and teach boundary awareness?
      Rather than relying on noisy Canny edge filters, we generate ground-truth boundary targets B_GT directly from binary segmentation masks M_GT using mathematical morphology:
      B_GT equals the morphological dilation of M_GT by a 3x3 structuring element K_3, minus the morphological erosion of M_GT by K_3.
      This isolates an exact, clean, one-pixel-wide closed contour enclosing each defect. The BAS boundary head is then trained against this target using a dedicated binary cross-entropy boundary loss, forcing early representations to preserve high-frequency edge gradients.</p>
      <p>In Section C, we examine Boundary-Guided Feature Fusion (BGFF):
      To inject boundary awareness into the decoder, BGFF concatenates the boundary feature map F_bound with the decoder feature map F_dec. A 1x1 convolution and sigmoid function produce a spatial attention map A_spat:
      A_spat = &sigma;(Conv_1x1([F_bound ; F_dec])).
      We then recalibrate decoder features via residual attention:
      F_out = F_dec &odot; (1 + A_spat).
      Where boundary uncertainty is high, A_spat approaches 1, boosting feature gain; over uniform steel background, A_spat is near 0, preserving neutral identity features. This mathematically eliminates border bleeding into background metal."</p>
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- SLIDE 7 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 7 of 11</div>
      <div class="slide-title">Training & Loss Function — Composite Region + Boundary Optimization</div>
    </div>
    <div class="slide-time">Target: 55–65 sec | Elapsed: 6:40 – 7:40</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> End-to-end training pipeline diagram; composite loss formula with exact weights: L_total = 0.3 L_BCE + 0.3 L_Dice + 0.2 L_Focal + 0.2 L_bound; 4 component explanation cards; Callout on &gt;98% background pixel imbalance.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Slide 7 details our optimization strategy. A sophisticated architecture requires an equally principled objective function.</p>
      <p>Because over 98% of image pixels belong to defect-free steel, standard cross-entropy training causes the optimization gradient to be swamped by trivial background pixels. To overcome this, we formulate a composite four-term loss function with balanced weighting:
      L_total = 0.3 L_BCE + 0.3 L_Dice + 0.2 L_Focal + 0.2 L_bound.</p>
      <p>Each term plays a dedicated, indispensable role:
      - <strong>Binary Cross-Entropy (0.3 weight)</strong> guarantees pixel-level classification accuracy across all coordinates.
      - <strong>Dice Loss (0.3 weight)</strong> optimizes spatial region overlap and ensures global mask continuity, making the loss invariant to defect scale.
      - <strong>Focal Loss (0.2 weight)</strong> applies a dynamic focusing parameter &gamma;=2.0 that down-weights easy, well-classified background pixels and forces gradients to focus on hard, low-contrast boundary pixels.
      - <strong>Boundary Loss (0.2 weight)</strong> provides explicit contour supervision to the BAS auxiliary head, punishing edge misalignment.</p>
      <p>This 4-term formulation ensures simultaneous region-level completeness and perimeter-level sharpness, stabilizing training across all defect categories."</p>
    </div>
  </div>
</div>

<!-- SLIDE 8 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 8 of 11</div>
      <div class="slide-title">Experimental Setup — NEU Benchmark & Hardware Configuration</div>
    </div>
    <div class="slide-time">Target: 60–70 sec | Elapsed: 7:40 – 8:45</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Left panel: NEU database overview (1,800 images, 256x256, 70/15/15 split) with 6 defect class cards (300 images each); Right panel: Compute &amp; Hyperparameter dashboard (PyTorch 2.1, RTX 4090, 100 epochs, AdamW, Cosine Annealing, 9.38M params, 14.2 GFLOPs, 41.1/88.5 FPS).
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"To rigorously benchmark MSBA-Net, we conducted comprehensive experiments on the Northeastern University (NEU) Surface Defect Database, the gold standard in metallurgical vision research.</p>
      <p>As summarized on the left, the dataset comprises 1,800 grayscale images spanning six distinct defect categories: crazing, inclusions, patches, pitted surfaces, rolled-in scale, and scratches, with exactly 300 images per class. The original 200x200 images are standardized to 256x256 resolution. We adopted a strict 70-15-15 partition: 1,260 images for training, 270 for validation, and 270 for completely held-out test evaluation, using fixed random seeds for strict reproducibility.</p>
      <p>Looking at the right dashboard, all models were trained in PyTorch 2.1 on an enterprise workstation equipped with an NVIDIA RTX 4090 GPU with 24 gigabytes of VRAM. Training was conducted for 100 epochs using the AdamW optimizer with an initial learning rate of 1 times 10 to the minus 3, scheduled via Cosine Annealing down to 1 times 10 to the minus 6, with a mini-batch size of 16. Convergence was reliably reached by epoch 75.</p>
      <p>From an industrial deployment standpoint, computational efficiency is paramount. MSBA-Net maintains an impressively compact footprint: only 9.38 million parameters and 14.2 GFLOPs. On our RTX 4090 hardware, it achieves 41.1 frames per second in standard FP32 PyTorch, and 88.5 frames per second under TensorRT FP16 quantization—comfortably exceeding the 30 FPS threshold required for real-time steel mill integration."</p>
    </div>
  </div>
</div>

<!-- SLIDE 9 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 9 of 11</div>
      <div class="slide-title">Results & Comparison — SOTA Performance on the NEU Benchmark</div>
    </div>
    <div class="slide-time">Target: 70–80 sec | Elapsed: 8:45 – 10:00</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> 3 large top metric cards (97.01% mIoU, 98.48% Dice, 92.48% Tiny mIoU); Native Clustered Column Chart comparing 6 state-of-the-art models (GNA-PSC, MixSegNet, EF²Net, DAMF-Net, DMS-UNet, MSBA-Net); Detailed comparative performance table.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Slide 9 presents our headline experimental results, benchmarking MSBA-Net against recent 2024 to 2026 published baselines.</p>
      <p>Looking at our three primary metric cards at the top:
      First, MSBA-Net achieves an overall mean Intersection-over-Union (mIoU) of <strong>97.01%</strong>, surpassing the previous 2026 state-of-the-art, DMS-UNet at 94.20%, by a decisive margin of <strong>+2.81%</strong>.
      Second, our Dice Similarity Coefficient reaches <strong>98.48%</strong>, an improvement of <strong>+1.46%</strong>, confirming near-flawless mask continuity and spatial overlap.
      Third, and most importantly: on <em>Tiny Defects</em>—defined strictly as defect regions occupying less than 1% of total image area—MSBA-Net achieves a remarkable <strong>92.48% mIoU</strong>. That is a massive <strong>+4.08% improvement</strong> over DMS-UNet (88.40%) and over +20% superior to GNA-PSC (72.40%).</p>
      <p>Examining the column chart and benchmark table below:
      Earlier 2024 models such as GNA-PSC (83.50%) and MixSegNet (84.80%) struggled with feature resolution trade-offs. Even advanced attention models like EF²Net (88.42%) and DAMF-Net (91.65%) suffered noticeable edge degradation on micro-cracks.
      Furthermore, MSBA-Net achieves 97.57% Precision and 99.41% Recall, translating to near-zero missed defects in industrial practice. Per-category analysis reveals that broad patches and inclusions achieved over 97% mIoU. These quantitative results confirm that our hybrid architectural strategy delivers superior accuracy across the board."</p>
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- SLIDE 10 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 10 of 11</div>
      <div class="slide-title">Validation & Analysis — Component Ablation & Qualitative Visual Progression</div>
    </div>
    <div class="slide-time">Target: 70–80 sec | Elapsed: 10:00 – 11:15</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> Left panel: Component-wise ablation study table (Baseline &rarr; +MSFP &rarr; +BAS &rarr; +BGFF) with two takeaway bullets; Right panel: Publication-grade qualitative comparison from Figure 2 across Crazing, Inclusions, Patches, Pitted Surfaces (Raw Steel, Ground Truth, Baseline U-Net, MSBA-Net).
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"Why does MSBA-Net perform so exceptionally well? Slide 10 provides both empirical ablation evidence and qualitative visual proof directly from the research paper.</p>
      <p>Looking at the ablation table on the left:
      Starting from our Baseline Backbone without MSFP or BAS, the model achieves 94.10% mIoU, but only 84.60% on tiny defects.
      When we insert our Multi-Scale Feature Preservation (MSFP) blocks, overall mIoU climbs to 95.85%, but tiny-defect mIoU surges by a massive <strong>+5.05%</strong> to 89.65%. This empirically verifies our hypothesis: parallel dilated convolutions are the primary mechanism that prevents microscopic flaws from vanishing during feature propagation.
      Next, incorporating the Boundary-Aware Stream (BAS) raises mIoU to 96.48% and pushes tiny mIoU to 91.20%, proving that explicit boundary loss forces the network to retain high-frequency contours.
      Finally, adding the BGFF spatial attention gate completes MSBA-Net, achieving our peak 97.01% mIoU and 92.48% tiny mIoU, with only a modest 1.62 million parameter addition over baseline.</p>
      <p>Now examine the qualitative visual comparisons on the right, taken from Figure 2 of our paper:
      - In row 1, crazing: Baseline U-Net produces a broken, fragmented crack mask with only 82.9% IoU. MSBA-Net traces the exact hairline trajectory, matching ground truth continuously at 86.7% IoU.
      - In row 2, thin inclusions: Baseline exhibits severe boundary bleeding into background steel, while MSBA-Net adheres precisely to the morphological contour.
      - For patches and pitted surfaces, MSBA-Net delivers a perfect 100% IoU match with ground truth.
      This qualitative evidence conclusively demonstrates that MSFP preserves fine topology while BAS and BGFF prevent boundary leakage."</p>
    </div>
  </div>
</div>

<!-- SLIDE 11 -->
<div class="slide-box">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <div class="slide-num">Slide 11 of 11</div>
      <div class="slide-title">Conclusion & Future Directions — Findings, Stress Testing & Roadmap</div>
    </div>
    <div class="slide-time">Target: 65–75 sec | Elapsed: 11:15 – 12:25</div>
  </div>
  <div class="slide-body">
    <div class="cues-box">
      <span class="cues-title">Visual Cues:</span> 3 summary cards (High Accuracy, Micro-Preservation, Real-Time Potential); Middle section: Shop-floor degradation stress-test (Low contrast 39.67%, Blur 26.29%, Gaussian noise 2.33%); Bottom section: 3-phase future roadmap (Temporal line-scan attention &rarr; Self-supervised pre-training &rarr; 8-bit edge deployment); Final sign-off banner.
    </div>
    <div class="script-label">Speaker Script:</div>
    <div class="script-text">
      <p>"To conclude our presentation, Slide 11 summarizes our core contributions, honestly reviews factory operational boundaries, and outlines future research.</p>
      <p>Our key findings are threefold:
      First, MSBA-Net establishes a new state of the art on the NEU steel surface defect benchmark, achieving 97.01% mIoU and 98.48% Dice.
      Second, it successfully bridges the micro-defect safety gap, reaching 92.48% mIoU on flaws occupying less than 1% area.
      Third, it maintains a real-time footprint of 41.1 FPS in PyTorch FP32 and 88.5 FPS under TensorRT FP16.</p>
      <p>However, true academic rigor demands that we report operational limitations with complete transparency. In Section V of our paper, we stress-tested MSBA-Net under simulated shop-floor degradations:
      - Under low optical contrast (gamma=1.8), the model demonstrates solid resilience, retaining 39.67% mIoU.
      - Under severe defocus blur (sigma=3.0), simulating mechanical camera vibration, performance drops to 26.29% mIoU.
      - Under high Gaussian sensor noise (sigma=25), performance breaks down to 2.33% mIoU.
      This breakdown is an information-theoretic reality: high-frequency random thermal noise completely obliterates the subtle 1-to-2 pixel gray-level transitions upon which boundary convolutions depend. This provides a crucial engineering takeaway for metallurgical plants: deploying deep learning on hot rolling lines requires active LED strobing, sealed dust housings, and low-noise sensor hardware.</p>
      <p>Looking ahead, our three-phase roadmap focuses on:
      1. Extending 2D spatial segmentation to spatio-temporal video attention across continuous line-scan coils.
      2. Self-supervised pre-training on massive uncurated steel imagery via masked autoencoders.
      3. INT8 quantization for embedded deployment on NVIDIA Jetson and FPGA controllers.</p>
      <p>Thank you very much for your time, patience, and kind attention. I welcome all questions and feedback from the committee."</p>
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- ========================================== -->
<!-- VIVA / EXAMINER Q&A SECTION -->
<!-- ========================================== -->
<div class="section-heading">Part 2: Comprehensive Examiner Viva Q&amp;A (10 Questions &amp; Answers)</div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q1</span>
    Why was the Multi-Scale Feature Preservation (MSFP) block necessary instead of standard convolutional layers?
  </div>
  <div class="qa-a">
    In standard CNNs (such as vanilla U-Net or FCN), expanding the effective receptive field to understand defect context requires repeated spatial downsampling (via max-pooling or strided convolutions). While this captures macro-level context, it destroys spatial resolution: a hairline craze crack or small pit depression occupying only 1 to 3 pixels is completely filtered out after two downsampling stages (4x decimation).
    <br><br>
    The MSFP block solves this by executing multiple dilated depthwise convolutions in parallel at the same spatial resolution. Each branch possesses a different receptive field (3x3, 5x5, 9x9), allowing the network to capture broad textural context and localized micro-features simultaneously without sacrificing feature grid density.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: Parallel multi-receptive coverage preserves fine spatial resolution that pooling operations destroy.</div>
</div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q2</span>
    Why did you specifically choose dilation rates of 1, 2, and 4 in the MSFP block, rather than larger rates like 8 or 16?
  </div>
  <div class="qa-a">
    Dilation rates of {1, 2, 4} were chosen based on the Hybrid Dilated Convolution (HDC) principle and the physical dimensions of steel surface defects:
    <br>
    1. <strong>Preventing the Gridding Effect:</strong> Standard dilated convolutions with large, identical dilation rates (e.g., r=8, 16) suffer from severe "gridding artifacts" (the checkerboard problem), where a large fraction of pixel inputs are skipped and never sampled. Consecutive rates {1, 2, 4} ensure that every pixel in the 9x9 field is sampled without gaps.
    <br>
    2. <strong>Physical Defect Scale:</strong> On 256x256 images, the largest defect structures (rolled-in scale sheets or broad patches) are well-covered by a 9x9 to 15x15 receptive field across hierarchical stages. Dilation rates above 4 would capture irrelevant background steel, diluting the localized feature representation.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: Dilation rates {1, 2, 4} satisfy HDC conditions to eliminate gridding artifacts while matching real defect dimensions.</div>
</div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q3</span>
    What is the Boundary-Aware Stream (BAS) and why is it structured as an auxiliary branch rather than inside the main backbone?
  </div>
  <div class="qa-a">
    The Boundary-Aware Stream (BAS) is a specialized auxiliary pathway that branches off early from Stages 1 and 2 of the encoder. Its purpose is to explicitly extract, preserve, and supervise high-frequency morphological edge contours.
    <br><br>
    It is kept as an auxiliary stream for two architectural reasons:
    <br>
    1. <strong>Directing Gradients to Early Layers:</strong> In deep networks, boundary loss gradients often diminish before reaching early layers. By attaching an auxiliary boundary prediction head directly to early features, we inject explicit edge-supervision gradients right where spatial resolution is highest.
    <br>
    2. <strong>Disentangling Semantics from Geometry:</strong> The main backbone focuses on region semantics (what type of defect is present), while the BAS branch focuses exclusively on geometric contours (where the defect begins and ends).
  </div>
  <div class="qa-key">Key Takeaway for Examiner: BAS explicitly forces early encoder features to retain fine boundary gradients that are otherwise washed out by semantic pooling.</div>
</div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q4</span>
    What is Boundary-Guided Feature Fusion (BGFF) and how does its spatial attention gating work?
  </div>
  <div class="qa-a">
    Boundary-Guided Feature Fusion (BGFF) is the bridging mechanism that transfers learned boundary knowledge from the BAS stream into the decoder. Merely predicting a boundary map is insufficient; that information must actively modulate decoder reconstruction.
    <br><br>
    BGFF concatenates the boundary feature tensor F_bound with the decoder feature tensor F_dec, passes them through a 1x1 convolution, and applies a sigmoid activation &sigma; to produce a 2D spatial attention weight map:
    <br>
    <code>A_spat = &sigma;(Conv_1x1([F_bound ; F_dec]))</code>
    <br>
    The decoder features are then modulated through residual attention:
    <br>
    <code>F_out = F_dec &odot; (1 + A_spat)</code>
    <br>
    Along ambiguous defect perimeters where boundary probability is elevated, A_spat approaches 1.0, boosting decoder feature gain. Over uniform steel background, A_spat drops to 0, ensuring background noise is suppressed and eliminating border bleeding.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: BGFF acts as an adaptive spatial gain controller that sharpens defect edges while suppressing background steel texture.</div>
</div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q5</span>
    Why did you employ a composite loss function combining BCE, Dice, Focal, and Boundary losses?
  </div>
  <div class="qa-a">
    No single loss function can solve all aspects of steel surface defect segmentation:
    <br>
    - <strong>Binary Cross-Entropy (L_BCE):</strong> Optimizes smooth pixel-by-pixel classification accuracy, but suffers severe gradient dilution when background pixels dominate (&gt;98%).
    - <strong>Dice Loss (L_Dice):</strong> Optimizes set-level intersection-over-union. It is scale-invariant, ensuring that small defect regions contribute equally to the gradient as large regions. However, Dice loss alone produces noisy, jagged contours.
    - <strong>Focal Loss (L_Focal):</strong> Dynamically down-weights easily classified background steel pixels via <code>(1 - p_t)^&gamma;</code> (with &gamma;=2.0), compelling the optimizer to concentrate on hard, ambiguous, low-contrast boundary pixels.
    - <strong>Boundary Loss (L_bound):</strong> Directly penalizes the Euclidean/morphological distance between predicted defect contours and true 1-pixel boundary perimeters.
    <br>
    The composite formula <code>0.3 L_BCE + 0.3 L_Dice + 0.2 L_Focal + 0.2 L_bound</code> balances region completeness, foreground-background imbalance, hard-example focus, and boundary sharpness.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: The 4-term loss balances pixel classification, region overlap, class imbalance, and edge localization into a unified objective.</div>
</div>

<div class="page-break"></div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q6</span>
    How were the loss weights (0.3, 0.3, 0.2, 0.2) determined, and is the model sensitive to them?
  </div>
  <div class="qa-a">
    The loss weights were established through empirical cross-validation during hyperparameter tuning. In our preliminary experiments:
    <br>
    - Giving excessive weight to Boundary Loss (&gt;0.4) caused the network to prioritize boundary edges over internal mask completeness, creating hollow, donut-shaped defect masks.
    - Giving excessive weight to BCE (&gt;0.5) led to background dominance, where tiny craze cracks were suppressed to minimize false positives.
    - An equal weighting of 0.3/0.3 for region metrics (BCE and Dice) paired with 0.2/0.2 for fine-tuning terms (Focal and Boundary) yielded optimal convergence stability and maximum mIoU across all six defect categories.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: 0.3/0.3 establishes balanced region coverage, while 0.2/0.2 provides fine edge and hard-sample refinement without gradient distortion.</div>
</div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q7</span>
    What is the NEU dataset, and why is it considered the standard benchmark for steel surface defect segmentation?
  </div>
  <div class="qa-a">
    The NEU Surface Defect Database was collected by Northeastern University and is the most widely cited open benchmark in metallurgical computer vision.
    <br><br>
    It contains 1,800 grayscale industrial images (300 per class) covering the six dominant morphological defect families found in real rolling mills: Crazing (micro-cracks), Inclusions (embedded foreign particles), Patches (flaking surface metal), Pitted Surfaces (oxidation cavities), Rolled-in Scale (pressed oxide sheets), and Scratches (longitudinal abrasions).
    <br><br>
    Using NEU enables direct, fair, and reproducible comparison against previously published architectures (e.g., GNA-PSC, MixSegNet, EF²Net, DAMF-Net, and DMS-UNet) under identical evaluation protocols.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: NEU provides standardized industrial defect taxonomy, balanced classes, and direct comparability with peer-reviewed SOTA models.</div>
</div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q8</span>
    What is the difference between mIoU and Tiny-Defect mIoU, and why is Tiny-Defect mIoU so critical?
  </div>
  <div class="qa-a">
    <strong>mIoU (Mean Intersection-over-Union):</strong> Measures the average area overlap across all test images regardless of defect size:
    <br>
    <code>mIoU = (1/N) &sum; [ |P &cap; Y| / |P &cup; Y| ]</code>
    <br>
    Because larger defects (like patches or rolled-in scale sheets) possess hundreds of thousands of pixels, high performance on large defects can artificially mask poor performance on tiny defects.
    <br><br>
    <strong>Tiny-Defect mIoU:</strong> We explicitly isolate the sub-population of defect connected components that occupy <em>less than 1% of total image area</em> (&lt;655 pixels in a 256x256 image).
    <br><br>
    This metric is crucial because microscopic flaws—such as hairline crazing or early pit corrosion—are the primary initiators of fatigue failure in downstream automotive manufacturing. While DMS-UNet achieves 94.20% overall mIoU, its tiny-defect mIoU is only 88.40%. MSBA-Net reaches <strong>92.48% Tiny mIoU</strong> (+4.08%), proving that our architecture preserves fine features that other models lose.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: Tiny mIoU unmasks whether a model actually detects micro-cracks or merely scores high on large, easy defect sheets.</div>
</div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q9</span>
    Why did MSBA-Net performance collapse under simulated Gaussian noise (2.33% mIoU)? Isn't that a serious limitation?
  </div>
  <div class="qa-a">
    We intentionally included and highlighted this result in Section V of our paper to maintain complete scientific integrity.
    <br><br>
    The drop to 2.33% under severe Gaussian noise (&sigma;=25) is an <em>information-theoretic</em> limitation rather than an architectural bug:
    1. In clean steel images, defect boundaries are defined by subtle gray-level differences of only 5 to 15 intensity levels against ambient metal texture.
    2. Adding zero-mean Gaussian noise with a standard deviation of &sigma;=25 produces pixel value perturbations of up to &plusmn;50 intensity levels across adjacent pixels.
    3. Because our BAS stream computes morphological gradients via differential operations, high-frequency random noise generates thousands of spurious false edges across the entire image. The boundary stream is overwhelmed by noise, causing spatial attention gating to fail.
    <br><br>
    <strong>Practical Engineering Remedy:</strong> In real rolling mills, camera enclosures are protected by pressurized air purges, stabilized LED stroboscopic illumination, and low-noise sensor sensors. Furthermore, simple bilateral filtering or denoising autoencoder pre-processing completely mitigates this sensitivity before inference.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: Differential boundary convolutions inherently amplify high-frequency random noise; real-world deployment requires clean optical lighting or front-end bilateral filtering.</div>
</div>

<div class="qa-card">
  <div class="qa-q">
    <span class="qa-badge">Q10</span>
    What are the primary computational limitations of MSBA-Net, and how can it be deployed on edge devices in a factory?
  </div>
  <div class="qa-a">
    MSBA-Net was engineered specifically for edge practicality:
    <br>
    - <strong>Parameter Footprint:</strong> 9.38 Million parameters (only +1.62M over baseline U-Net).
    - <strong>Computational FLOPs:</strong> 14.2 GFLOPs at 256x256 resolution.
    - <strong>Latency:</strong> 41.1 FPS in PyTorch FP32 on an RTX 4090 (24.3 ms per image), and 88.5 FPS under TensorRT FP16 (11.3 ms per image).
    <br><br>
    For production shop-floor deployment on moving strip mills:
    1. <strong>INT8 Quantization:</strong> Post-training quantization reduces memory footprint from ~38MB to under 10MB, enabling direct deployment on embedded industrial controllers such as the NVIDIA Jetson AGX Orin or industrial FPGA accelerators.
    2. <strong>Pruning Auxiliary BAS at Inference:</strong> If inference speed must be maximized, the auxiliary boundary head loss can be detached post-training, keeping only the spatial attention gate.
    3. <strong>Spatio-Temporal Extension:</strong> On continuous line-scan video feeds, temporal attention can correlate defect continuity across consecutive frame slices to eliminate transient sensor flickers.
  </div>
  <div class="qa-key">Key Takeaway for Examiner: At 14.2 GFLOPs and 88.5 FPS (TensorRT), MSBA-Net is already real-time ready, with clear INT8 quantization pathways for embedded edge hardware.</div>
</div>

<div class="footer-note">
  MSBA-Net Presentation Script &amp; Viva Examination Guide &bull; Amen Parmar &bull; M.Tech (AIML) &bull; Manipal University Jaipur &bull; 2026
</div>

</body>
</html>
"""

def main():
    print("Writing HTML script template...")
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
