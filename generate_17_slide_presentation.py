"""
generate_17_slide_presentation.py
Generates the 17-slide Academic Research Presentation for MSBA-Net.
Visual style:
- Clean open canvas (NO enclosing rectangular border around content!)
- Large, bold title at top
- Plenty of whitespace
- Simple content arrangement: bullets, native charts, clean tables, simple diagrams
- 100% native editable PowerPoint elements
Output: MSBA-Net_Amen_Parmar_Presentation.pptx
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

OUTPUT_PATH = os.path.abspath("MSBA-Net_Amen_Parmar_Presentation.pptx")

# -------------------------------------------------------------
# COLOR PALETTE
# -------------------------------------------------------------
NAVY        = RGBColor(0x0B, 0x19, 0x2C)  # #0B192C Deep Navy
NAVY_LIGHT  = RGBColor(0x1E, 0x29, 0x3B)  # #1E293B Slate Dark (Body text)
SLATE_MUTED = RGBColor(0x47, 0x55, 0x69)  # #475569 Slate Muted (Subtitles)
SLATE_LIGHT = RGBColor(0x64, 0x74, 0x8B)  # #64748B Secondary / borders
AMBER       = RGBColor(0xD9, 0x77, 0x06)  # #D97706 Warm Amber accent
AMBER_DARK  = RGBColor(0xB4, 0x53, 0x09)  # #B45309 Dark Amber
AMBER_BG    = RGBColor(0xFE, 0xF3, 0xC7)  # #FEF3C7 Soft Amber
BLUE_ACCENT = RGBColor(0x25, 0x63, 0xEB)  # #2563EB Royal Blue
BLUE_BG     = RGBColor(0xDB, 0xEA, 0xFE)  # #DBEAFE Soft Blue
EMERALD     = RGBColor(0x05, 0x96, 0x69)  # #059669 Success green
EMERALD_BG  = RGBColor(0xDC, 0xFC, 0xE7)  # #DCFCE7 Soft green
ROSE        = RGBColor(0xDC, 0x26, 0x26)  # #DC2626 Warning red
ROSE_BG     = RGBColor(0xFE, 0xE2, 0xE2)  # #FEE2E2 Soft red
BG_CARD     = RGBColor(0xF8, 0xF9, 0xFA)  # #F8F9FA Clean light card fill
BORDER_CARD = RGBColor(0xCB, 0xD5, 0xE1)  # #CBD5E1 Clean light border
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)

FONT_TITLE = "Segoe UI"
FONT_BODY  = "Segoe UI"

def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width  = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Helper: Set clean white slide background
    def init_slide():
        slide = prs.slides.add_slide(blank_layout)
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = WHITE
        return slide

    # Helper: Standard Open Academic Header (NO enclosing border!)
    def add_header(slide, title_text, subtitle_text=None, category="M.Tech (AIML) Research Seminar"):
        # Category badge text
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.733), Inches(0.28))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = FONT_BODY
        p_cat.font.size = Pt(8.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = AMBER

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.733), Inches(0.55))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = FONT_TITLE
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY

        # Subtitle
        if subtitle_text:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.24), Inches(11.733), Inches(0.32))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle_text
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = SLATE_MUTED

        # Thin elegant accent line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.58), Inches(1.6), Inches(0.025))
        line.fill.solid()
        line.fill.fore_color.rgb = AMBER
        line.line.color.rgb = AMBER

    # Helper: Add bullet point with bold prefix
    def add_bullet(tf, bold_prefix, text_body, pt_size=17.5, space_after=12):
        p = tf.add_paragraph()
        p.space_after = Pt(space_after)
        p.font.name = FONT_BODY
        p.font.size = Pt(pt_size)
        p.line_spacing = 1.25

        # Bold prefix
        run_b = p.add_run()
        run_b.text = "• " + bold_prefix + (" " if bold_prefix else "")
        run_b.font.bold = True
        run_b.font.color.rgb = NAVY

        # Body
        run_t = p.add_run()
        run_t.text = text_body
        run_t.font.bold = False
        run_t.font.color.rgb = NAVY_LIGHT

    # Helper: Add small callout pill
    def add_callout(slide, left, top, width, height, text_prefix, text_body, bg_col=AMBER_BG, border_col=AMBER, text_col=AMBER_DARK):
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = bg_col
        box.line.color.rgb = border_col
        box.line.width = Pt(1)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.18)
        tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.08)
        tf.margin_bottom = Inches(0.08)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        run1 = p.add_run()
        run1.text = text_prefix + " "
        run1.font.bold = True
        run1.font.name = FONT_BODY
        run1.font.size = Pt(11.5)
        run1.font.color.rgb = text_col
        run2 = p.add_run()
        run2.text = text_body
        run2.font.bold = False
        run2.font.name = FONT_BODY
        run2.font.size = Pt(11.5)
        run2.font.color.rgb = NAVY

    # Helper: Add simple block with text (for architecture)
    def add_block(slide, left, top, width, height, title, subtitle=None, fill_col=BG_CARD, border_col=BORDER_CARD, title_col=NAVY, title_size=11):
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = fill_col
        box.line.color.rgb = border_col
        box.line.width = Pt(1.2)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.1)
        tf.margin_right = Inches(0.1)
        tf.margin_top = Inches(0.08)
        tf.margin_bottom = Inches(0.08)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = title
        run.font.bold = True
        run.font.name = FONT_BODY
        run.font.size = Pt(title_size)
        run.font.color.rgb = title_col
        if subtitle:
            p2 = tf.add_paragraph()
            p2.alignment = PP_ALIGN.CENTER
            run2 = p2.add_run()
            run2.text = subtitle
            run2.font.name = FONT_BODY
            run2.font.size = Pt(title_size - 2)
            run2.font.color.rgb = SLATE_MUTED
        return box

    # Helper: Add arrow
    def add_arrow(slide, left, top, width, height, shape_type=MSO_SHAPE.RIGHT_ARROW, col=SLATE_LIGHT):
        arrow = slide.shapes.add_shape(shape_type, left, top, width, height)
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = col
        arrow.line.fill.background()
        return arrow

    # =========================================================================
    # SLIDE 1: TITLE
    # =========================================================================
    s1 = init_slide()

    # Category Pill
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.9), Inches(3.2), Inches(0.38))
    pill.fill.solid()
    pill.fill.fore_color.rgb = AMBER_BG
    pill.line.color.rgb = AMBER
    pill.line.width = Pt(1)
    tf_p = pill.text_frame
    p_p = tf_p.paragraphs[0]
    p_p.alignment = PP_ALIGN.CENTER
    r_p = p_p.add_run()
    r_p.text = "M.TECH (AIML) RESEARCH SEMINAR"
    r_p.font.name = FONT_BODY
    r_p.font.size = Pt(9.5)
    r_p.font.bold = True
    r_p.font.color.rgb = AMBER_DARK

    # Title Box
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(11.333), Inches(1.8))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p1 = tf_t.paragraphs[0]
    p1.text = "MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation"
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = NAVY
    p1.line_spacing = 1.15

    # Thin accent rule
    rule = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(3.4), Inches(2.2), Inches(0.035))
    rule.fill.solid()
    rule.fill.fore_color.rgb = AMBER
    rule.line.color.rgb = AMBER

    # Subtitle
    sub_box = s1.shapes.add_textbox(Inches(1.0), Inches(3.55), Inches(11.333), Inches(0.4))
    tf_s = sub_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    p_s.text = "A Boundary-Preserving Deep Semantic Segmentation Architecture for Automated Metallurgical Inspection"
    p_s.font.name = FONT_BODY
    p_s.font.size = Pt(13)
    p_s.font.color.rgb = SLATE_MUTED

    # Presenter & Author Card (Left)
    meta_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.3), Inches(6.8), Inches(2.3))
    meta_box.fill.solid()
    meta_box.fill.fore_color.rgb = BG_CARD
    meta_box.line.color.rgb = BORDER_CARD
    meta_box.line.width = Pt(1)
    tf_m = meta_box.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = Inches(0.25)
    tf_m.margin_top = Inches(0.2)
    tf_m.margin_right = Inches(0.25)
    tf_m.margin_bottom = Inches(0.2)

    pm1 = tf_m.paragraphs[0]
    rm1 = pm1.add_run()
    rm1.text = "PRESENTER & CANDIDATE"
    rm1.font.size = Pt(8.5)
    rm1.font.bold = True
    rm1.font.color.rgb = AMBER

    pm2 = tf_m.add_paragraph()
    pm2.space_before = Pt(3)
    rm2 = pm2.add_run()
    rm2.text = "Amen Parmar  "
    rm2.font.size = Pt(14)
    rm2.font.bold = True
    rm2.font.color.rgb = NAVY
    rm2_sub = pm2.add_run()
    rm2_sub.text = "|  Roll No: 2502010010  |  M.Tech (AIML)"
    rm2_sub.font.size = Pt(12)
    rm2_sub.font.color.rgb = SLATE_MUTED

    pm3 = tf_m.add_paragraph()
    pm3.space_before = Pt(8)
    rm3 = pm3.add_run()
    rm3.text = "PAPER CO-AUTHORS: "
    rm3.font.size = Pt(9)
    rm3.font.bold = True
    rm3.font.color.rgb = SLATE_LIGHT
    rm3_names = pm3.add_run()
    rm3_names.text = "Amit Kumar Bairwa, Varun Kumar"
    rm3_names.font.size = Pt(10)
    rm3_names.font.color.rgb = NAVY

    pm4 = tf_m.add_paragraph()
    pm4.space_before = Pt(4)
    rm4 = pm4.add_run()
    rm4.text = "AFFILIATION: "
    rm4.font.size = Pt(9)
    rm4.font.bold = True
    rm4.font.color.rgb = SLATE_LIGHT
    rm4_aff = pm4.add_run()
    rm4_aff.text = "Department of Computer Science & Engineering, Manipal University Jaipur"
    rm4_aff.font.size = Pt(10)
    rm4_aff.font.color.rgb = NAVY

    # Right side: Visual defect teaser
    if os.path.exists("scratch/slide3_defect_sample.png"):
        s1.shapes.add_picture("scratch/slide3_defect_sample.png", Inches(8.2), Inches(4.3), Inches(4.133), Inches(1.6))
        c_box = s1.shapes.add_textbox(Inches(8.2), Inches(6.0), Inches(4.133), Inches(0.6))
        tf_c = c_box.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        pc = tf_c.paragraphs[0]
        rc = pc.add_run()
        rc.text = "Metallurgical Defect Challenge: Hairline Crazing & Faint Contrast (<1% Area)"
        rc.font.size = Pt(9)
        rc.font.color.rgb = SLATE_MUTED
        rc.font.italic = True

    # =========================================================================
    # SLIDE 2: OBJECTIVE
    # =========================================================================
    s2 = init_slide()
    add_header(s2, "Objective", "Core Research Goals of the MSBA-Net Framework")

    tb2 = s2.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(11.733), Inches(3.8))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0

    add_bullet(tf2, "Accurate Segmentation:", "Develop an effective segmentation framework specifically engineered for small and low-contrast steel surface defects.", pt_size=17.5, space_after=14)
    add_bullet(tf2, "Multi-Scale Preservation:", "Preserve fine-grained structural defect features that are commonly lost during conventional downsampling and pooling stages.", pt_size=17.5, space_after=14)
    add_bullet(tf2, "Boundary Localization:", "Improve spatial boundary localization to eliminate border bleeding around faint, low-contrast, and blurred defect contours.", pt_size=17.5, space_after=14)
    add_bullet(tf2, "Benchmark Validation:", "Rigorously evaluate the proposed MSBA-Net on the benchmark NEU surface defect database against current state-of-the-art architectures.", pt_size=17.5, space_after=16)

    # Bottom focus pill (adjusted position)
    add_callout(s2, Inches(0.8), Inches(5.85), Inches(11.733), Inches(0.65),
                "Core Research Focus:",
                "Accurate pixel-level segmentation of microscopic defect structures without sacrificing boundary contour precision.",
                bg_col=AMBER_BG, border_col=AMBER, text_col=AMBER_DARK)

    # =========================================================================
    # SLIDE 3: BRIEF OVERVIEW / BACKGROUND
    # =========================================================================
    s3 = init_slide()
    add_header(s3, "Brief Overview", "Importance of Automated Visual Inspection in Steel Manufacturing")

    tb3 = s3.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(6.8), Inches(4.8))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_top = tf3.margin_right = tf3.margin_bottom = 0

    add_bullet(tf3, "Automated Inspection:", "Automated visual inspection is critical in steel strip manufacturing to prevent catastrophic structural failures in downstream automotive and structural applications.", pt_size=16.5, space_after=12)
    add_bullet(tf3, "Micro-Scale Flaws:", "Surface defects such as hairline crazing cracks and pit depressions frequently occupy less than 1% of the entire image area.", pt_size=16.5, space_after=12)
    add_bullet(tf3, "Low Intensity Contrast:", "Subtle gray-level differences between defect regions and surrounding rolled steel textures make pixel-level delineation extremely challenging.", pt_size=16.5, space_after=12)
    add_bullet(tf3, "Downsampling Dilemma:", "Conventional encoder-decoder networks wash away fine spatial details during successive pooling stages, leading to missed flaws.", pt_size=16.5, space_after=12)

    if os.path.exists("scratch/slide3_defect_sample.png"):
        s3.shapes.add_picture("scratch/slide3_defect_sample.png", Inches(8.0), Inches(1.95), Inches(4.5), Inches(1.75))
        cap_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.0), Inches(3.95), Inches(4.5), Inches(1.6))
        cap_box.fill.solid()
        cap_box.fill.fore_color.rgb = BG_CARD
        cap_box.line.color.rgb = BORDER_CARD
        cap_box.line.width = Pt(1)
        tf_cap = cap_box.text_frame
        tf_cap.word_wrap = True
        tf_cap.margin_left = tf_cap.margin_right = Inches(0.18)
        tf_cap.margin_top = tf_cap.margin_bottom = Inches(0.12)
        p_c1 = tf_cap.paragraphs[0]
        r_c1 = p_c1.add_run()
        r_c1.text = "Representative Challenge from NEU Dataset:"
        r_c1.font.bold = True
        r_c1.font.size = Pt(10.5)
        r_c1.font.color.rgb = NAVY
        p_c2 = tf_cap.add_paragraph()
        p_c2.space_before = Pt(5)
        r_c2 = p_c2.add_run()
        r_c2.text = "Top-left: Raw Crazing steel surface (weak intensity contrast).\nTop-right: Ground truth mask isolating micro-scale branching cracks (<1% of total image pixels)."
        r_c2.font.size = Pt(10)
        r_c2.font.color.rgb = SLATE_MUTED

    # =========================================================================
    # SLIDE 4: PROBLEM STATEMENT
    # =========================================================================
    s4 = init_slide()
    add_header(s4, "Problem Statement", "Critical Technical Obstacles in Steel Surface Defect Segmentation")

    tb4 = s4.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(11.733), Inches(3.8))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    tf4.margin_left = tf4.margin_top = tf4.margin_right = tf4.margin_bottom = 0

    add_bullet(tf4, "Micro-Scale Defect Footprint:", "Defect regions frequently occupy less than 1% of the image area (<655 pixels at 256×256 resolution). Standard receptive fields aggregate background texture, diluting tiny defect signals.", pt_size=17, space_after=12)
    add_bullet(tf4, "Low-Contrast Boundaries:", "Subtle gray-level transitions (often only 5–15 intensity levels difference) between defect edges and the steel surface cause severe boundary bleeding in standard models.", pt_size=17, space_after=12)
    add_bullet(tf4, "Downsampling Feature Loss:", "Repeated striding and pooling operations in deep convolutional encoders discard high-frequency spatial gradients, destroying hairline fissures before reaching deep layers.", pt_size=17, space_after=12)
    add_bullet(tf4, "Extreme Class Imbalance:", "Over 98% of pixels belong to defect-free steel background, heavily skewing standard loss functions and causing models to ignore micro-scale defect pixels.", pt_size=17, space_after=14)

    add_callout(s4, Inches(0.8), Inches(5.85), Inches(11.733), Inches(0.65),
                "Key Problem:",
                "Standard segmentation backbones optimize for macro-regions, leading to severe feature loss and blurred boundaries on microscopic metallurgical flaws.",
                bg_col=ROSE_BG, border_col=ROSE, text_col=ROSE)

    # =========================================================================
    # SLIDE 5: RESEARCH GAP
    # =========================================================================
    s5 = init_slide()
    add_header(s5, "Research Gap", "Limitations of Existing Segmentation Architectures & The Research Need")

    col1_box = s5.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(5.6), Inches(3.8))
    tf_c1 = col1_box.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_top = tf_c1.margin_right = tf_c1.margin_bottom = 0

    p_h1 = tf_c1.paragraphs[0]
    r_h1 = p_h1.add_run()
    r_h1.text = "LIMITATIONS OF EXISTING METHODS"
    r_h1.font.bold = True
    r_h1.font.size = Pt(13)
    r_h1.font.color.rgb = ROSE
    p_h1.space_after = Pt(10)

    add_bullet(tf_c1, "Spatial Detail Loss:", "Standard CNN and Transformer backbones sacrifice fine spatial details for broad semantic context during aggressive pooling.", pt_size=16, space_after=12)
    add_bullet(tf_c1, "Implicit Boundary Handling:", "Edge information is relied upon solely through standard skip connections, causing blurred contours and border bleeding.", pt_size=16, space_after=12)
    add_bullet(tf_c1, "Tiny-Defect Performance Drop:", "While models report high overall mIoU, tiny-defect mIoU degrades by 10%–25%, masking failure on safety-critical flaws.", pt_size=16, space_after=12)

    col2_box = s5.shapes.add_textbox(Inches(6.8), Inches(1.85), Inches(5.7), Inches(3.8))
    tf_c2 = col2_box.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_top = tf_c2.margin_right = tf_c2.margin_bottom = 0

    p_h2 = tf_c2.paragraphs[0]
    r_h2 = p_h2.add_run()
    r_h2.text = "THE UNMET RESEARCH NEED"
    r_h2.font.bold = True
    r_h2.font.size = Pt(13)
    r_h2.font.color.rgb = BLUE_ACCENT
    p_h2.space_after = Pt(10)

    add_bullet(tf_c2, "Native Multi-Scale Preservation:", "Preserve high-resolution spatial features across multiple receptive fields simultaneously without downsampling loss.", pt_size=16, space_after=12)
    add_bullet(tf_c2, "Explicit Boundary Guidance:", "Incorporate a dedicated auxiliary boundary stream to guide feature fusion and sharpen contour boundaries.", pt_size=16, space_after=12)
    add_bullet(tf_c2, "Industrial Real-Time Efficiency:", "Maintain lightweight parameters (<10M) and high frame rates (>40 FPS) suitable for high-speed rolling-mill deployment.", pt_size=16, space_after=12)

    add_callout(s5, Inches(0.8), Inches(5.85), Inches(11.733), Inches(0.65),
                "Core Research Need:",
                "Multi-scale feature preservation + explicit boundary-aware guidance in a lightweight real-time architecture.",
                bg_col=BLUE_BG, border_col=BLUE_ACCENT, text_col=BLUE_ACCENT)

    # =========================================================================
    # SLIDE 6: PROPOSED APPROACH — MSBA-Net
    # =========================================================================
    s6 = init_slide()
    add_header(s6, "Proposed Approach — MSBA-Net", "Dual-Stream Architecture: Multi-Scale Semantic Backbone + Boundary Guidance")

    # Main Stream blocks
    b_in  = add_block(s6, Inches(0.8), Inches(2.0), Inches(1.4), Inches(0.85), "Input Image", "256×256×1", fill_col=BG_CARD, border_col=SLATE_LIGHT)
    a1    = add_arrow(s6, Inches(2.3), Inches(2.3), Inches(0.3), Inches(0.25))
    b_e1  = add_block(s6, Inches(2.7), Inches(2.0), Inches(1.5), Inches(0.85), "Stage 1 + MSFP", "256×256 (64ch)", fill_col=BLUE_BG, border_col=BLUE_ACCENT, title_col=BLUE_ACCENT)
    a2    = add_arrow(s6, Inches(4.3), Inches(2.3), Inches(0.3), Inches(0.25))
    b_e2  = add_block(s6, Inches(4.7), Inches(2.0), Inches(1.5), Inches(0.85), "Stage 2 + MSFP", "128×128 (128ch)", fill_col=BLUE_BG, border_col=BLUE_ACCENT, title_col=BLUE_ACCENT)
    a3    = add_arrow(s6, Inches(6.3), Inches(2.3), Inches(0.3), Inches(0.25))
    b_bot = add_block(s6, Inches(6.7), Inches(2.0), Inches(1.4), Inches(0.85), "Bottleneck", "Stages 3 & 4", fill_col=BG_CARD, border_col=SLATE_LIGHT)
    a4    = add_arrow(s6, Inches(8.2), Inches(2.3), Inches(0.3), Inches(0.25))
    b_dec = add_block(s6, Inches(8.6), Inches(2.0), Inches(1.7), Inches(0.85), "Decoder Stages", "Upsampling + Skip", fill_col=EMERALD_BG, border_col=EMERALD, title_col=EMERALD)
    a5    = add_arrow(s6, Inches(10.4), Inches(2.3), Inches(0.3), Inches(0.25))
    b_out = add_block(s6, Inches(10.8), Inches(2.0), Inches(1.7), Inches(0.85), "Defect Mask", "256×256 Output", fill_col=AMBER_BG, border_col=AMBER, title_col=AMBER_DARK)

    # Boundary Stream blocks
    b_bas  = add_block(s6, Inches(3.2), Inches(3.4), Inches(3.0), Inches(0.85), "Boundary-Aware Stream (BAS)", "Auxiliary Edge Supervision (L_bound)", fill_col=AMBER_BG, border_col=AMBER, title_col=AMBER_DARK)
    # Down arrow from Stage 1/2 to BAS
    a_down = add_arrow(s6, Inches(4.4), Inches(2.95), Inches(0.25), Inches(0.35), shape_type=MSO_SHAPE.DOWN_ARROW)
    # Arrow from BAS to BGFF
    a_b1   = add_arrow(s6, Inches(6.3), Inches(3.7), Inches(0.35), Inches(0.25))
    # BGFF block
    b_bgff = add_block(s6, Inches(6.75), Inches(3.4), Inches(3.4), Inches(0.85), "Boundary-Guided Feature Fusion (BGFF)", "Spatial Attention Gating A_spat", fill_col=AMBER_BG, border_col=AMBER, title_col=AMBER_DARK)
    # Up arrow from BGFF into Decoder
    a_up   = add_arrow(s6, Inches(8.8), Inches(2.95), Inches(0.25), Inches(0.35), shape_type=MSO_SHAPE.UP_ARROW)

    # Bullets below architecture
    tb6 = s6.shapes.add_textbox(Inches(0.8), Inches(4.65), Inches(11.733), Inches(2.2))
    tf6 = tb6.text_frame
    tf6.word_wrap = True
    tf6.margin_left = tf6.margin_top = tf6.margin_right = tf6.margin_bottom = 0

    add_bullet(tf6, "MSFP Integration:", "Multi-Scale Feature Preservation modules in encoder stages extract multi-scale spatial details at native resolution.", pt_size=16.5, space_after=8)
    add_bullet(tf6, "Boundary-Aware Stream (BAS):", "Branches off early high-resolution stages to learn explicit defect boundary contours via auxiliary supervision.", pt_size=16.5, space_after=8)
    add_bullet(tf6, "Boundary-Guided Feature Fusion (BGFF):", "Generates spatial attention gating maps from boundary features, sharpening decoder contours and suppressing background noise.", pt_size=16.5, space_after=8)

    # =========================================================================
    # SLIDE 7: MSFP — MULTI-SCALE FEATURE PRESERVATION
    # =========================================================================
    s7 = init_slide()
    add_header(s7, "Multi-Scale Feature Preservation (MSFP)", "Capturing Multi-Scale Defect Morphs at Native Resolution Without Downsampling")

    # Left: MSFP Diagram with proper DOWN arrows
    f_in = add_block(s7, Inches(0.8), Inches(2.1), Inches(4.8), Inches(0.6), "Input Feature Map F_in", "Dimensions: H × W × C", fill_col=BG_CARD, border_col=BORDER_CARD)

    # Down arrow from input to branches
    a_f = add_arrow(s7, Inches(3.08), Inches(2.8), Inches(0.25), Inches(0.35), shape_type=MSO_SHAPE.DOWN_ARROW)

    # 3 parallel branches
    br1 = add_block(s7, Inches(0.8), Inches(3.25), Inches(1.5), Inches(0.95), "Branch 1", "3×3, r=1 (RF 3×3)\nHairline Cracks", fill_col=BLUE_BG, border_col=BLUE_ACCENT, title_col=BLUE_ACCENT, title_size=10)
    br2 = add_block(s7, Inches(2.45), Inches(3.25), Inches(1.5), Inches(0.95), "Branch 2", "3×3, r=2 (RF 5×5)\nPits & Inclusions", fill_col=BLUE_BG, border_col=BLUE_ACCENT, title_col=BLUE_ACCENT, title_size=10)
    br3 = add_block(s7, Inches(4.1), Inches(3.25), Inches(1.5), Inches(0.95), "Branch 3", "3×3, r=4 (RF 9×9)\nPatches & Scale", fill_col=BLUE_BG, border_col=BLUE_ACCENT, title_col=BLUE_ACCENT, title_size=10)

    # Down arrow from branches to fusion
    a_fuse = add_arrow(s7, Inches(3.08), Inches(4.3), Inches(0.25), Inches(0.35), shape_type=MSO_SHAPE.DOWN_ARROW)

    f_out = add_block(s7, Inches(0.8), Inches(4.75), Inches(4.8), Inches(0.7), "Concatenation & 1×1 Pointwise Conv", "Output Feature Map F_out (H × W × C)", fill_col=AMBER_BG, border_col=AMBER, title_col=AMBER_DARK)

    # Right: Explanatory bullets
    tb7 = s7.shapes.add_textbox(Inches(6.0), Inches(1.9), Inches(6.5), Inches(4.8))
    tf7 = tb7.text_frame
    tf7.word_wrap = True
    tf7.margin_left = tf7.margin_top = tf7.margin_right = tf7.margin_bottom = 0

    add_bullet(tf7, "Parallel Dilated Depthwise Convolutions:", "MSFP splits incoming features across three parallel branches with dilation rates r ∈ {1, 2, 4}, expanding receptive fields without spatial pooling.", pt_size=16.5, space_after=12)
    add_bullet(tf7, "Multi-Scale Defect Coverage:", "Branch 1 captures hairline crazing cracks; Branch 2 captures pit depressions and inclusions; Branch 3 captures broad patches and rolled-in scale sheets.", pt_size=16.5, space_after=12)
    add_bullet(tf7, "HDC Condition Compliance:", "Dilation rates {1, 2, 4} strictly satisfy the Hybrid Dilated Convolution condition, eliminating checkerboard gridding artifacts common in dilated networks.", pt_size=16.5, space_after=12)
    add_bullet(tf7, "Zero Downsampling Loss:", "Operates at native spatial resolution, ensuring microscopic defect structures are fully retained for downstream feature fusion.", pt_size=16.5, space_after=12)

    # =========================================================================
    # SLIDE 8: BOUNDARY-AWARE LEARNING — BAS + BGFF
    # =========================================================================
    s8 = init_slide()
    add_header(s8, "Boundary-Aware Learning — BAS & BGFF", "Explicit Boundary Extraction & Spatial Attention Feature Calibration")

    # Left: BAS + BGFF Diagram with proper DOWN arrows
    b1_bas = add_block(s8, Inches(0.8), Inches(2.1), Inches(4.8), Inches(0.65), "Early Encoder Features (Stages 1 & 2)", "High Spatial Resolution (256×256 & 128×128)", fill_col=BG_CARD, border_col=BORDER_CARD)
    a_b_d1 = add_arrow(s8, Inches(3.08), Inches(2.85), Inches(0.25), Inches(0.35), shape_type=MSO_SHAPE.DOWN_ARROW)
    b2_bas = add_block(s8, Inches(0.8), Inches(3.3), Inches(4.8), Inches(0.75), "Boundary-Aware Stream (BAS)", "Auxiliary Edge Supervision (L_bound on 1-px defect contours)", fill_col=AMBER_BG, border_col=AMBER, title_col=AMBER_DARK)
    a_b_d2 = add_arrow(s8, Inches(3.08), Inches(4.15), Inches(0.25), Inches(0.35), shape_type=MSO_SHAPE.DOWN_ARROW)
    b3_bgff = add_block(s8, Inches(0.8), Inches(4.6), Inches(4.8), Inches(0.95), "Boundary-Guided Feature Fusion (BGFF)", "Spatial Attention Map: A_spat = σ(Conv1×1([F_bound ; F_dec]))\nRefinement: F_out = F_dec ⊙ (1 + A_spat)", fill_col=BLUE_BG, border_col=BLUE_ACCENT, title_col=BLUE_ACCENT)

    # Right: Bullets
    tb8 = s8.shapes.add_textbox(Inches(6.0), Inches(1.9), Inches(6.5), Inches(4.8))
    tf8 = tb8.text_frame
    tf8.word_wrap = True
    tf8.margin_left = tf8.margin_top = tf8.margin_right = tf8.margin_bottom = 0

    add_bullet(tf8, "Dedicated Edge Extraction (BAS):", "Taps early encoder features where spatial detail is freshest, learning geometric defect perimeters via dedicated auxiliary boundary loss.", pt_size=16.5, space_after=12)
    add_bullet(tf8, "Direct Gradient Injection:", "Injects edge-supervision gradients directly into shallow layers, preventing boundary gradients from vanishing in deep semantic layers.", pt_size=16.5, space_after=12)
    add_bullet(tf8, "Spatial Attention Calibration (BGFF):", "Dynamically boosts feature gain along defect perimeters while dampening uniform steel background response.", pt_size=16.5, space_after=12)
    add_bullet(tf8, "Elimination of Border Bleeding:", "Produces clean, leak-free defect contours around weak, low-contrast boundaries that confuse standard thresholding.", pt_size=16.5, space_after=12)

    # =========================================================================
    # SLIDE 9: EXPERIMENTAL WORK — DATASET
    # =========================================================================
    s9 = init_slide()
    add_header(s9, "Experimental Work — Dataset", "NEU Surface Defect Database Specifications & Defect Class Taxonomy")

    tb9 = s9.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.8))
    tf9 = tb9.text_frame
    tf9.word_wrap = True
    tf9.margin_left = tf9.margin_top = tf9.margin_right = tf9.margin_bottom = 0

    add_bullet(tf9, "Benchmark Standard:", "NEU Surface Defect Database developed by Northeastern University (recognized benchmark in metallurgical vision research).", pt_size=16.5, space_after=12)
    add_bullet(tf9, "Image Volume & Balance:", "1,800 grayscale industrial steel strip images, perfectly balanced with exactly 300 images per defect category.", pt_size=16.5, space_after=12)
    add_bullet(tf9, "Resolution & Resizing:", "Original images captured at 200×200 resolution; standardized to 256×256 pixels for deep neural network training.", pt_size=16.5, space_after=12)
    add_bullet(tf9, "Rigorous Data Split:", "70% Training (1,260 images), 15% Validation (270 images), and 15% Independent Testing (270 images).", pt_size=16.5, space_after=12)

    # Right Column: Clean 6-class table
    table_shape9 = s9.shapes.add_table(7, 2, Inches(6.8), Inches(1.85), Inches(5.7), Inches(4.5))
    table9 = table_shape9.table
    table9.columns[0].width = Inches(2.0)
    table9.columns[1].width = Inches(3.7)

    headers9 = ["Defect Category", "Morphological Characteristics"]
    for j, h in enumerate(headers9):
        cell = table9.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        r.text = h
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = WHITE

    class_data = [
        ("Crazing (Cr)", "Thin, branching network of micro-cracks (<1% area)"),
        ("Inclusion (In)", "Non-metallic slag particles embedded into surface"),
        ("Patches (Pa)", "Localized surface oxidation & discoloration sheets"),
        ("Pitted Surface (PS)", "Small point-like pit depressions & indentations"),
        ("Rolled-in Scale (RS)", "Mill oxide scale mechanically pressed into strip"),
        ("Scratches (Sc)", "Linear mechanical abrasive grooves along rolling line")
    ]
    for i, (cat, desc) in enumerate(class_data):
        row_bg = WHITE if i % 2 == 0 else BG_CARD
        for j, val in enumerate([cat, desc]):
            cell = table9.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            r = p.add_run()
            r.text = val
            r.font.name = FONT_BODY
            r.font.size = Pt(10.5)
            r.font.bold = (j == 0)
            r.font.color.rgb = NAVY if j == 0 else SLATE_MUTED

    # =========================================================================
    # SLIDE 10: EXPERIMENTAL SETUP
    # =========================================================================
    s10 = init_slide()
    add_header(s10, "Experimental Setup", "Hardware Environment, Training Hyperparameters, and Model Complexity")

    tb10_l = s10.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.8))
    tf10_l = tb10_l.text_frame
    tf10_l.word_wrap = True
    tf10_l.margin_left = tf10_l.margin_top = tf10_l.margin_right = tf10_l.margin_bottom = 0

    p_th = tf10_l.paragraphs[0]
    r_th = p_th.add_run()
    r_th.text = "TRAINING PROTOCOL"
    r_th.font.bold = True
    r_th.font.size = Pt(13)
    r_th.font.color.rgb = BLUE_ACCENT
    p_th.space_after = Pt(10)

    add_bullet(tf10_l, "Deep Learning Framework:", "PyTorch 2.1 implementation using CUDA 12.1 acceleration.", pt_size=16, space_after=12)
    add_bullet(tf10_l, "Compute Hardware:", "Single NVIDIA GeForce RTX 4090 GPU with 24GB high-speed GDDR6X VRAM.", pt_size=16, space_after=12)
    add_bullet(tf10_l, "Optimizer & Weight Decay:", "AdamW optimizer (β1=0.9, β2=0.999, weight decay 1×10⁻⁴).", pt_size=16, space_after=12)
    add_bullet(tf10_l, "Learning Rate Schedule:", "Initial learning rate 1×10⁻³ with Cosine Annealing decay down to 1×10⁻⁶.", pt_size=16, space_after=12)
    add_bullet(tf10_l, "Batch Size & Epochs:", "Batch size of 16 images; trained for 100 epochs until full convergence.", pt_size=16, space_after=12)

    tb10_r = s10.shapes.add_textbox(Inches(6.8), Inches(1.85), Inches(5.7), Inches(4.8))
    tf10_r = tb10_r.text_frame
    tf10_r.word_wrap = True
    tf10_r.margin_left = tf10_r.margin_top = tf10_r.margin_right = tf10_r.margin_bottom = 0

    p_ch = tf10_r.paragraphs[0]
    r_ch = p_ch.add_run()
    r_ch.text = "MODEL COMPLEXITY & REAL-TIME EFFICIENCY"
    r_ch.font.bold = True
    r_ch.font.size = Pt(13)
    r_ch.font.color.rgb = AMBER_DARK
    p_ch.space_after = Pt(10)

    add_bullet(tf10_r, "Parameter Count:", "9.38 Million parameters (highly compact footprint for edge deployment).", pt_size=16, space_after=12)
    add_bullet(tf10_r, "Computational Cost:", "14.2 GFLOPs per single-image forward inference pass.", pt_size=16, space_after=12)
    add_bullet(tf10_r, "Inference Latency:", "24.3 milliseconds per 256×256 input image.", pt_size=16, space_after=12)
    add_bullet(tf10_r, "PyTorch FP32 Speed:", "41.1 Frames Per Second (comfortably exceeds the 30 FPS real-time threshold).", pt_size=16, space_after=12)
    add_bullet(tf10_r, "TensorRT FP16 Speed:", "88.5 Frames Per Second (enables high-speed online rolling-mill inspection).", pt_size=16, space_after=12)

    # =========================================================================
    # SLIDE 11: EVALUATION METRICS
    # =========================================================================
    s11 = init_slide()
    add_header(s11, "Evaluation Metrics", "Standard Overlap Metrics and Dedicated Micro-Defect Assessment")

    tb11 = s11.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(11.733), Inches(3.8))
    tf11 = tb11.text_frame
    tf11.word_wrap = True
    tf11.margin_left = tf11.margin_top = tf11.margin_right = tf11.margin_bottom = 0

    add_bullet(tf11, "mIoU (Mean Intersection over Union):", "Primary benchmark metric assessing spatial overlap between predicted mask P and ground truth G: mIoU = |P ∩ G| / |P ∪ G|.", pt_size=17, space_after=12)
    add_bullet(tf11, "Dice Similarity Coefficient:", "Measures harmonic mean of precision and recall (2|P ∩ G| / (|P| + |G|)); scale-invariant region overlap indicator.", pt_size=17, space_after=12)
    add_bullet(tf11, "Precision & Recall:", "Precision (TP / (TP + FP)) verifies predicted defect pixel correctness; Recall (TP / (TP + FN)) ensures zero missed defect regions.", pt_size=17, space_after=12)
    add_bullet(tf11, "Tiny-Defect mIoU (Key Innovation):", "Specifically evaluates performance exclusively on defect regions occupying less than 1% of the total image area (<655 pixels at 256×256).", pt_size=17, space_after=14)

    add_callout(s11, Inches(0.8), Inches(5.85), Inches(11.733), Inches(0.65),
                "Why Tiny-Defect mIoU Matters:",
                "Overall mIoU is area-weighted; high scores on large patches can easily mask catastrophic detection failures on hairline cracks.",
                bg_col=AMBER_BG, border_col=AMBER, text_col=AMBER_DARK)

    # =========================================================================
    # SLIDE 12: RESULTS — COMPARISON WITH EXISTING METHODS
    # =========================================================================
    s12 = init_slide()
    add_header(s12, "Results — Comparison with Existing Methods", "Benchmarking MSBA-Net Against State-of-the-Art Segmentation Networks on NEU")

    chart_data12 = CategoryChartData()
    chart_data12.categories = ["GNA-PSC\n[2021]", "MixSegNet\n[2022]", "EF²Net\n[2023]", "DAMF-Net\n[2024]", "DMS-UNet\n[2026]", "MSBA-Net\n(Proposed)"]
    chart_data12.add_series("mIoU (%)", (83.50, 84.80, 88.42, 91.65, 94.20, 97.01))

    chart_shape12 = s12.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.8), Inches(1.95), Inches(6.5), Inches(4.7), chart_data12)
    chart12 = chart_shape12.chart
    chart12.has_legend = False

    plots12 = chart12.plots[0]
    plots12.has_data_labels = True
    dl12 = plots12.data_labels
    dl12.font.name = FONT_BODY
    dl12.font.size = Pt(10)
    dl12.font.bold = True
    dl12.font.color.rgb = NAVY

    val_ax12 = chart12.value_axis
    val_ax12.minimum_scale = 75.0
    val_ax12.maximum_scale = 100.0
    val_ax12.major_unit = 5.0
    val_ax12.tick_labels.font.size = Pt(9.5)
    cat_ax12 = chart12.category_axis
    cat_ax12.tick_labels.font.size = Pt(9.5)

    series12 = plots12.series[0]
    colors12 = [SLATE_LIGHT, SLATE_LIGHT, SLATE_LIGHT, BLUE_ACCENT, BLUE_ACCENT, AMBER]
    for idx, pt in enumerate(series12.points):
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = colors12[idx]

    table_shape12 = s12.shapes.add_table(4, 4, Inches(7.5), Inches(1.95), Inches(5.0), Inches(1.8))
    table12 = table_shape12.table
    table12.columns[0].width = Inches(1.8)
    table12.columns[1].width = Inches(1.0)
    table12.columns[2].width = Inches(1.1)
    table12.columns[3].width = Inches(1.1)

    headers12 = ["Model", "mIoU", "Dice", "Tiny mIoU"]
    for j, h in enumerate(headers12):
        cell = table12.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = h
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = WHITE

    sota_rows = [
        ("DAMF-Net [2024]", "91.65%", "93.40%", "85.20%"),
        ("DMS-UNet [2026]", "94.20%", "95.80%", "88.40%"),
        ("MSBA-Net (Ours)", "97.01%", "98.48%", "92.48%")
    ]
    for i, row in enumerate(sota_rows):
        is_ours = (i == 2)
        row_bg = AMBER_BG if is_ours else (WHITE if i % 2 == 0 else BG_CARD)
        for j, val in enumerate(row):
            cell = table12.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
            r = p.add_run()
            r.text = val
            r.font.bold = is_ours
            r.font.size = Pt(10)
            r.font.color.rgb = AMBER_DARK if is_ours else NAVY

    tb12 = s12.shapes.add_textbox(Inches(7.5), Inches(4.05), Inches(5.0), Inches(2.6))
    tf12 = tb12.text_frame
    tf12.word_wrap = True
    tf12.margin_left = tf12.margin_top = tf12.margin_right = tf12.margin_bottom = 0

    add_bullet(tf12, "State-of-the-Art mIoU:", "MSBA-Net achieves 97.01% mIoU, outperforming the previous 2026 leader DMS-UNet by +2.81%.", pt_size=15, space_after=10)
    add_bullet(tf12, "Exceptional Region Overlap:", "Dice coefficient reaches 98.48%, with 97.57% Precision and 99.41% Recall.", pt_size=15, space_after=10)
    add_bullet(tf12, "Dominant Tiny-Defect Gain:", "Tiny-Defect mIoU reaches 92.48% (+4.08% over DMS-UNet), confirming micro-structure preservation.", pt_size=15, space_after=10)

    # =========================================================================
    # SLIDE 13: RESULTS — PER-CLASS ANALYSIS
    # =========================================================================
    s13 = init_slide()
    add_header(s13, "Results — Per-Class Analysis", "Category-Wise Segmentation Performance Across the Six Defect Categories")

    table_shape13 = s13.shapes.add_table(7, 2, Inches(0.8), Inches(1.85), Inches(5.4), Inches(2.5))
    table13 = table_shape13.table
    table13.columns[0].width = Inches(3.1)
    table13.columns[1].width = Inches(2.3)

    for j, h in enumerate(["Defect Category", "MSBA-Net mIoU (%)"]):
        cell = table13.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
        r = p.add_run()
        r.text = h
        r.font.bold = True
        r.font.size = Pt(10.5)
        r.font.color.rgb = WHITE

    class_res = [
        ("Patches (Pa)", "97.85%"),
        ("Inclusions (In)", "97.15%"),
        ("Scratches (Sc)", "97.12%"),
        ("Pitted Surface (PS)", "96.80%"),
        ("Rolled-in Scale (RS)", "96.72%"),
        ("Crazing (Cr)", "96.42%")
    ]
    for i, (cat, val) in enumerate(class_res):
        row_bg = WHITE if i % 2 == 0 else BG_CARD
        cell0 = table13.cell(i + 1, 0)
        cell0.fill.solid()
        cell0.fill.fore_color.rgb = row_bg
        p0 = cell0.text_frame.paragraphs[0]
        r0 = p0.add_run()
        r0.text = cat
        r0.font.bold = True
        r0.font.size = Pt(10)
        r0.font.color.rgb = NAVY

        cell1 = table13.cell(i + 1, 1)
        cell1.fill.solid()
        cell1.fill.fore_color.rgb = row_bg
        p1 = cell1.text_frame.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        r1 = p1.add_run()
        r1.text = val
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = AMBER_DARK if i == 0 else NAVY

    tb13 = s13.shapes.add_textbox(Inches(0.8), Inches(4.55), Inches(5.4), Inches(2.2))
    tf13 = tb13.text_frame
    tf13.word_wrap = True
    tf13.margin_left = tf13.margin_top = tf13.margin_right = tf13.margin_bottom = 0

    add_bullet(tf13, "Uniform Excellence:", "Performance remains consistently above 96.4% across all six industrial categories.", pt_size=15, space_after=8)
    add_bullet(tf13, "Highest Class Score:", "Patches reach 97.85% mIoU due to homogeneous and continuous regional defect area.", pt_size=15, space_after=8)
    add_bullet(tf13, "Challenging Morphology:", "Crazing is relatively most demanding (96.42%) due to complex branching hairline fissures.", pt_size=15, space_after=8)

    # Right Column: Clean cropped qualitative visual (2 complete rows: Crazing & Inclusions)
    qual_path = "scratch/slide13_qualitative_clean.png" if os.path.exists("scratch/slide13_qualitative_clean.png") else "scratch/slide9_qualitative_crop.png"
    if os.path.exists(qual_path):
        s13.shapes.add_picture(qual_path, Inches(6.5), Inches(1.85), Inches(6.0), Inches(2.4))
        q_card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.5), Inches(4.45), Inches(6.0), Inches(2.1))
        q_card.fill.solid()
        q_card.fill.fore_color.rgb = BG_CARD
        q_card.line.color.rgb = BORDER_CARD
        q_card.line.width = Pt(1)
        tf_q = q_card.text_frame
        tf_q.word_wrap = True
        tf_q.margin_left = tf_q.margin_right = Inches(0.18)
        tf_q.margin_top = tf_q.margin_bottom = Inches(0.12)
        pq1 = tf_q.paragraphs[0]
        rq1 = pq1.add_run()
        rq1.text = "Qualitative Comparison: Crazing & Inclusions"
        rq1.font.bold = True
        rq1.font.size = Pt(11)
        rq1.font.color.rgb = NAVY
        pq2 = tf_q.add_paragraph()
        pq2.space_before = Pt(4)
        rq2 = pq2.add_run()
        rq2.text = "Columns: (a) Input Steel Image | (b) Ground Truth Mask | (c) Baseline U-Net | (d) MSBA-Net (Ours)\n\nKey Finding: Baseline U-Net suffers severe boundary bleeding and misses disconnected crack segments. MSBA-Net captures fine hairline branches with razor-sharp boundary alignment."
        rq2.font.size = Pt(9.5)
        rq2.font.color.rgb = SLATE_MUTED

    # =========================================================================
    # SLIDE 14: ABLATION STUDY
    # =========================================================================
    s14 = init_slide()
    add_header(s14, "Ablation Study", "Quantifying the Individual Performance Gain of Each Proposed Component")

    chart_data14 = CategoryChartData()
    chart_data14.categories = ["Baseline\nBackbone", "+ MSFP\nModule", "+ BAS\nStream", "+ BGFF\n(MSBA-Net)"]
    chart_data14.add_series("Overall mIoU (%)", (94.10, 95.85, 96.48, 97.01))
    chart_data14.add_series("Tiny-Defect mIoU (%)", (84.60, 89.65, 91.20, 92.48))

    chart_shape14 = s14.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.8), Inches(2.15), Inches(6.5), Inches(4.5), chart_data14)
    chart14 = chart_shape14.chart
    chart14.has_legend = False

    plots14 = chart14.plots[0]
    plots14.has_data_labels = True
    dl14 = plots14.data_labels
    dl14.font.name = FONT_BODY
    dl14.font.size = Pt(9.5)
    dl14.font.bold = True

    val_ax14 = chart14.value_axis
    val_ax14.minimum_scale = 80.0
    val_ax14.maximum_scale = 100.0
    val_ax14.major_unit = 5.0
    val_ax14.tick_labels.font.size = Pt(9)
    cat_ax14 = chart14.category_axis
    cat_ax14.tick_labels.font.size = Pt(9.5)

    series_overall = plots14.series[0]
    series_overall.format.fill.solid()
    series_overall.format.fill.fore_color.rgb = BLUE_ACCENT
    series_tiny = plots14.series[1]
    series_tiny.format.fill.solid()
    series_tiny.format.fill.fore_color.rgb = AMBER

    # Legend Badges above chart
    leg1 = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.75), Inches(2.0), Inches(0.3))
    leg1.fill.solid()
    leg1.fill.fore_color.rgb = BLUE_BG
    leg1.line.color.rgb = BLUE_ACCENT
    tf_l1 = leg1.text_frame
    p_l1 = tf_l1.paragraphs[0]
    p_l1.alignment = PP_ALIGN.CENTER
    r_l1 = p_l1.add_run()
    r_l1.text = "■ Overall mIoU (%)"
    r_l1.font.bold = True
    r_l1.font.size = Pt(9)
    r_l1.font.color.rgb = BLUE_ACCENT

    leg2 = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.8), Inches(1.75), Inches(2.2), Inches(0.3))
    leg2.fill.solid()
    leg2.fill.fore_color.rgb = AMBER_BG
    leg2.line.color.rgb = AMBER
    tf_l2 = leg2.text_frame
    p_l2 = tf_l2.paragraphs[0]
    p_l2.alignment = PP_ALIGN.CENTER
    r_l2 = p_l2.add_run()
    r_l2.text = "■ Tiny-Defect mIoU (%)"
    r_l2.font.bold = True
    r_l2.font.size = Pt(9)
    r_l2.font.color.rgb = AMBER_DARK

    table_shape14 = s14.shapes.add_table(5, 3, Inches(7.6), Inches(1.95), Inches(4.9), Inches(2.1))
    table14 = table_shape14.table
    table14.columns[0].width = Inches(2.1)
    table14.columns[1].width = Inches(1.4)
    table14.columns[2].width = Inches(1.4)

    for j, h in enumerate(["Configuration", "Overall mIoU", "Tiny mIoU"]):
        cell = table14.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
        r = p.add_run()
        r.text = h
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = WHITE

    ablation_data = [
        ("Baseline Backbone", "94.10%", "84.60%"),
        ("+ MSFP Module", "95.85% (+1.75)", "89.65% (+5.05)"),
        ("+ BAS Stream", "96.48% (+0.63)", "91.20% (+1.55)"),
        ("+ BGFF (Full Model)", "97.01% (+0.53)", "92.48% (+1.28)")
    ]
    for i, row in enumerate(ablation_data):
        is_full = (i == 3)
        row_bg = AMBER_BG if is_full else (WHITE if i % 2 == 0 else BG_CARD)
        for j, val in enumerate(row):
            cell = table14.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
            r = p.add_run()
            r.text = val
            r.font.bold = is_full
            r.font.size = Pt(9.5)
            r.font.color.rgb = AMBER_DARK if is_full else NAVY

    tb14 = s14.shapes.add_textbox(Inches(7.6), Inches(4.3), Inches(4.9), Inches(2.4))
    tf14 = tb14.text_frame
    tf14.word_wrap = True
    tf14.margin_left = tf14.margin_top = tf14.margin_right = tf14.margin_bottom = 0

    add_bullet(tf14, "MSFP Drives Tiny Gain:", "MSFP provides the largest single leap in Tiny-Defect mIoU (+5.05%), confirming multi-scale preservation.", pt_size=15, space_after=8)
    add_bullet(tf14, "BAS Boosts Contours:", "BAS injects explicit boundary supervision, lifting Tiny mIoU beyond 91%.", pt_size=15, space_after=8)
    add_bullet(tf14, "BGFF Final Calibration:", "BGFF refines spatial attention gating, yielding the final +0.53% overall and +1.28% tiny-defect gain.", pt_size=15, space_after=8)

    # =========================================================================
    # SLIDE 15: LIMITATIONS & ROBUSTNESS
    # =========================================================================
    s15 = init_slide()
    add_header(s15, "Limitations & Robustness", "Stress-Testing Under Simulated Environmental Shop-Floor Degradations")

    table_shape15 = s15.shapes.add_table(5, 2, Inches(0.8), Inches(1.95), Inches(5.2), Inches(3.0))
    table15 = table_shape15.table
    table15.columns[0].width = Inches(3.2)
    table15.columns[1].width = Inches(2.0)

    for j, h in enumerate(["Degradation Condition", "MSBA-Net mIoU (%)"]):
        cell = table15.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
        r = p.add_run()
        r.text = h
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = WHITE

    stress_rows = [
        ("Normal Clean Benchmark", "97.01%", EMERALD_BG, EMERALD),
        ("Low Contrast (Faint Edge Contrast)", "39.67%", AMBER_BG, AMBER_DARK),
        ("Defocus Blur (Out-of-Focus Optics)", "26.29%", ROSE_BG, ROSE),
        ("Gaussian Noise (Thermal Sensor Noise, σ=25)", "2.33%", ROSE_BG, ROSE)
    ]
    for i, (cond, val, bg_c, txt_c) in enumerate(stress_rows):
        cell0 = table15.cell(i + 1, 0)
        cell0.fill.solid()
        cell0.fill.fore_color.rgb = bg_c
        p0 = cell0.text_frame.paragraphs[0]
        r0 = p0.add_run()
        r0.text = cond
        r0.font.bold = (i == 0 or i == 3)
        r0.font.size = Pt(10)
        r0.font.color.rgb = NAVY

        cell1 = table15.cell(i + 1, 1)
        cell1.fill.solid()
        cell1.fill.fore_color.rgb = bg_c
        p1 = cell1.text_frame.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        r1 = p1.add_run()
        r1.text = val
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = txt_c

    tb15 = s15.shapes.add_textbox(Inches(6.4), Inches(1.85), Inches(6.1), Inches(4.8))
    tf15 = tb15.text_frame
    tf15.word_wrap = True
    tf15.margin_left = tf15.margin_top = tf15.margin_right = tf15.margin_bottom = 0

    add_bullet(tf15, "Noise Vulnerability:", "Gaussian noise causes severe performance collapse (2.33% mIoU); high-frequency random thermal fluctuations are amplified by boundary convolutions into thousands of spurious false edges.", pt_size=16.5, space_after=14)
    add_bullet(tf15, "Optical Defocus Blur:", "Defocus blur softens already weak gray-level gradients, reducing boundary attention gating effectiveness (26.29% mIoU).", pt_size=16.5, space_after=14)
    add_bullet(tf15, "Industrial Remediation:", "Evaluation is primarily based on simulated NEU degradations; factory rolling-mill deployment strictly requires front-end bilateral denoising filters and high-intensity LED strobe lighting.", pt_size=16.5, space_after=14)

    # =========================================================================
    # SLIDE 16: CONCLUSION & FUTURE WORK
    # =========================================================================
    s16 = init_slide()
    add_header(s16, "Conclusion & Future Work", "Summary of Research Contributions and Future Directions")

    tb16_l = s16.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.8))
    tf16_l = tb16_l.text_frame
    tf16_l.word_wrap = True
    tf16_l.margin_left = tf16_l.margin_top = tf16_l.margin_right = tf16_l.margin_bottom = 0

    p_cl = tf16_l.paragraphs[0]
    r_cl = p_cl.add_run()
    r_cl.text = "RESEARCH CONCLUSIONS"
    r_cl.font.bold = True
    r_cl.font.size = Pt(13)
    r_cl.font.color.rgb = BLUE_ACCENT
    p_cl.space_after = Pt(10)

    add_bullet(tf16_l, "Dual-Stream Synergy:", "MSBA-Net combines multi-scale feature preservation (MSFP) with explicit boundary learning (BAS + BGFF).", pt_size=15.5, space_after=10)
    add_bullet(tf16_l, "Fine-Feature Retention:", "MSFP successfully preserves micro-scale flaws occupying <1% area without downsampling dilution.", pt_size=15.5, space_after=10)
    add_bullet(tf16_l, "Benchmark Superiority:", "Achieves state-of-the-art results on NEU: 97.01% mIoU, 98.48% Dice, and 92.48% Tiny-Defect mIoU.", pt_size=15.5, space_after=10)
    add_bullet(tf16_l, "Industrial Real-Time Speed:", "Operates at 41.1 FPS (FP32) and 88.5 FPS (TensorRT FP16) with only 9.38M parameters.", pt_size=15.5, space_after=10)

    tb16_r = s16.shapes.add_textbox(Inches(6.8), Inches(1.85), Inches(5.7), Inches(4.8))
    tf16_r = tb16_r.text_frame
    tf16_r.word_wrap = True
    tf16_r.margin_left = tf16_r.margin_top = tf16_r.margin_right = tf16_r.margin_bottom = 0

    p_cr = tf16_r.paragraphs[0]
    r_cr = p_cr.add_run()
    r_cr.text = "FUTURE RESEARCH DIRECTIONS"
    r_cr.font.bold = True
    r_cr.font.size = Pt(13)
    r_cr.font.color.rgb = AMBER_DARK
    p_cr.space_after = Pt(10)

    add_bullet(tf16_r, "Spatio-Temporal Video Attention:", "Extend MSBA-Net to continuous line-scan video feeds, exploiting temporal defect continuity across moving steel coils.", pt_size=15.5, space_after=10)
    add_bullet(tf16_r, "Self-Supervised Pre-Training:", "Pre-train masked autoencoders on large volumes of uncurated industrial steel images before supervised fine-tuning.", pt_size=15.5, space_after=10)
    add_bullet(tf16_r, "Embedded Edge Quantization:", "Implement INT8 post-training quantization for deployment on embedded edge boards (e.g., NVIDIA Jetson AGX Orin) at >100 FPS.", pt_size=15.5, space_after=10)
    add_bullet(tf16_r, "Front-End Adaptive Denoising:", "Integrate learned edge-preserving denoising to harden boundary convolutions against shop-floor thermal noise.", pt_size=15.5, space_after=10)

    # =========================================================================
    # SLIDE 17: THANK YOU
    # =========================================================================
    s17 = init_slide()

    pill17 = s17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.666), Inches(1.6), Inches(4.0), Inches(0.42))
    pill17.fill.solid()
    pill17.fill.fore_color.rgb = AMBER_BG
    pill17.line.color.rgb = AMBER
    pill17.line.width = Pt(1)
    tf_p17 = pill17.text_frame
    p_p17 = tf_p17.paragraphs[0]
    p_p17.alignment = PP_ALIGN.CENTER
    r_p17 = p_p17.add_run()
    r_p17.text = "M.TECH (AIML) RESEARCH SEMINAR"
    r_p17.font.name = FONT_BODY
    r_p17.font.size = Pt(10)
    r_p17.font.bold = True
    r_p17.font.color.rgb = AMBER_DARK

    t_box17 = s17.shapes.add_textbox(Inches(2.0), Inches(2.2), Inches(9.333), Inches(1.2))
    tf_t17 = t_box17.text_frame
    tf_t17.word_wrap = True
    tf_t17.margin_left = tf_t17.margin_top = tf_t17.margin_right = tf_t17.margin_bottom = 0
    p17 = tf_t17.paragraphs[0]
    p17.alignment = PP_ALIGN.CENTER
    r17 = p17.add_run()
    r17.text = "Thank You"
    r17.font.name = FONT_TITLE
    r17.font.size = Pt(44)
    r17.font.bold = True
    r17.font.color.rgb = NAVY

    sub_box17 = s17.shapes.add_textbox(Inches(2.0), Inches(3.3), Inches(9.333), Inches(0.5))
    tf_s17 = sub_box17.text_frame
    tf_s17.word_wrap = True
    tf_s17.margin_left = tf_s17.margin_top = tf_s17.margin_right = tf_s17.margin_bottom = 0
    ps17 = tf_s17.paragraphs[0]
    ps17.alignment = PP_ALIGN.CENTER
    rs17 = ps17.add_run()
    rs17.text = "Questions & Discussion"
    rs17.font.name = FONT_BODY
    rs17.font.size = Pt(18)
    rs17.font.bold = True
    rs17.font.color.rgb = BLUE_ACCENT

    rule17 = s17.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.666), Inches(4.0), Inches(2.0), Inches(0.035))
    rule17.fill.solid()
    rule17.fill.fore_color.rgb = AMBER
    rule17.line.color.rgb = AMBER

    card17 = s17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.666), Inches(4.4), Inches(6.0), Inches(2.0))
    card17.fill.solid()
    card17.fill.fore_color.rgb = BG_CARD
    card17.line.color.rgb = BORDER_CARD
    card17.line.width = Pt(1)
    tf_c17 = card17.text_frame
    tf_c17.word_wrap = True
    tf_c17.margin_left = tf_c17.margin_right = Inches(0.25)
    tf_c17.margin_top = tf_c17.margin_bottom = Inches(0.2)

    pc17_1 = tf_c17.paragraphs[0]
    pc17_1.alignment = PP_ALIGN.CENTER
    rc17_1 = pc17_1.add_run()
    rc17_1.text = "Amen Parmar"
    rc17_1.font.bold = True
    rc17_1.font.size = Pt(16)
    rc17_1.font.color.rgb = NAVY

    pc17_2 = tf_c17.add_paragraph()
    pc17_2.alignment = PP_ALIGN.CENTER
    pc17_2.space_before = Pt(4)
    rc17_2 = pc17_2.add_run()
    rc17_2.text = "M.Tech in Artificial Intelligence & Machine Learning  |  Roll No: 2502010010"
    rc17_2.font.size = Pt(11.5)
    rc17_2.font.color.rgb = SLATE_MUTED

    pc17_3 = tf_c17.add_paragraph()
    pc17_3.alignment = PP_ALIGN.CENTER
    pc17_3.space_before = Pt(4)
    rc17_3 = pc17_3.add_run()
    rc17_3.text = "Department of Computer Science and Engineering\nManipal University Jaipur"
    rc17_3.font.size = Pt(11)
    rc17_3.font.color.rgb = NAVY

    prs.save(OUTPUT_PATH)
    print(f"SUCCESS: Saved 17-slide presentation to: {OUTPUT_PATH}")
    print(f"Total slides in presentation: {len(prs.slides)}")

if __name__ == "__main__":
    create_presentation()
