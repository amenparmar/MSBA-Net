"""
generate_msba_presentation.py
Official generator for MSBA-Net Presentation (11 slides).
Fully editable PowerPoint elements, NotebookLM technical aesthetic, zero text overflows, pristine typography.
"""

import os, sys
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_TICK_MARK, XL_LABEL_POSITION

# -------------------------------------------------------------
# CONSTANTS & PALETTE
# -------------------------------------------------------------
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

FONT_PRIMARY = "Segoe UI"
FONT_HEADING = "Segoe UI"

COLOR_BG = RGBColor(248, 247, 243)         # #F8F7F3 Off-white
COLOR_NAVY = RGBColor(11, 25, 44)          # #0B192C Deep Navy
COLOR_NAVY_LIGHT = RGBColor(30, 41, 59)    # #1E293B Dark Slate
COLOR_SLATE = RGBColor(71, 85, 105)        # #475569 Secondary Slate
COLOR_MUTED = RGBColor(148, 163, 184)      # #94A3B8 Muted Line
COLOR_BORDER = RGBColor(15, 23, 42)        # #0F172A Crisp Card Border
COLOR_CARD_WHITE = RGBColor(255, 255, 255) # Pure White
COLOR_CARD_ALT = RGBColor(246, 248, 250)   # Clean Ice Gray

# Accents
COLOR_AMBER = RGBColor(217, 119, 6)        # #D97706 Muted Amber / Highlight
COLOR_AMBER_BG = RGBColor(254, 243, 199)   # #FEF3C7 Soft Amber
COLOR_GREEN = RGBColor(5, 150, 105)        # #059669 Emerald / Results
COLOR_GREEN_BG = RGBColor(209, 250, 229)   # #D1FAE5 Soft Green
COLOR_BLUE = RGBColor(37, 99, 235)         # #2563EB Blue
COLOR_BLUE_BG = RGBColor(219, 234, 254)    # #DBEAFE Soft Blue
COLOR_PURPLE = RGBColor(124, 58, 237)      # #7C3AED BGFF Purple
COLOR_PURPLE_BG = RGBColor(243, 232, 255)  # #F3E8FF Soft Purple
COLOR_RED = RGBColor(220, 38, 38)          # #DC2626 Failure/Degradation
COLOR_RED_BG = RGBColor(254, 226, 226)     # #FEE2E2 Soft Red

GRID_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "scratch", "notebooklm_bg.png")
SLIDE10_QUAL_PATH = os.path.join(os.path.dirname(__file__), "scratch", "slide10_qualitative.png")

# -------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------
def set_slide_background(slide):
    """Sets subtle technical grid background."""
    if os.path.exists(GRID_IMAGE_PATH):
        slide.shapes.add_picture(GRID_IMAGE_PATH, Inches(0), Inches(0), SLIDE_WIDTH, SLIDE_HEIGHT)
    else:
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = COLOR_BG

def add_clean_paragraph(text_frame, text, font_name=FONT_PRIMARY, font_size=Pt(8.5), bold=False, color=COLOR_SLATE, alignment=PP_ALIGN.LEFT, space_after=Pt(2)):
    """Safely adds paragraph(s) to a text frame with explicit font properties and ensures word wrap."""
    text_frame.word_wrap = True
    lines = str(text).split("\n")
    p = None
    for idx, line in enumerate(lines):
        if len(text_frame.paragraphs) == 1 and text_frame.paragraphs[0].text == "":
            p = text_frame.paragraphs[0]
        else:
            p = text_frame.add_paragraph()
        p.text = line
        p.font.name = font_name
        p.font.size = font_size
        p.font.bold = bold
        p.font.color.rgb = color
        p.alignment = alignment
        p.space_after = space_after if idx == len(lines) - 1 else Pt(1)
    return p

def add_header(slide, category_tag, title_text, subtitle_text):
    """Adds a standard NotebookLM-styled header."""
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.32), Inches(11.7), Inches(1.15))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    add_clean_paragraph(tf, category_tag.upper(), font_size=Pt(9.0), bold=True, color=COLOR_AMBER, space_after=Pt(2))
    add_clean_paragraph(tf, title_text, font_name=FONT_HEADING, font_size=Pt(21), bold=True, color=COLOR_NAVY, space_after=Pt(2))
    add_clean_paragraph(tf, subtitle_text, font_size=Pt(11.5), bold=False, color=COLOR_SLATE, space_after=Pt(0))

def add_card(slide, x, y, w, h, bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.2), shape_type=MSO_SHAPE.ROUNDED_RECTANGLE):
    """Draws a clean, outlined card shape (editable in PPTX)."""
    shape = slide.shapes.add_shape(shape_type, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = border_width
    else:
        shape.line.fill.background()
    return shape

def add_pill_badge(slide, x, y, w, h, text, text_color=COLOR_NAVY, bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, font_size=Pt(8.5)):
    """Creates a pill-shaped badge with centered bold text."""
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    pill.fill.solid()
    pill.fill.fore_color.rgb = bg_color
    pill.line.color.rgb = border_color
    pill.line.width = Pt(1.0)
    tf = pill.text_frame
    tf.word_wrap = False
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_PRIMARY
    p.font.bold = True
    p.font.size = font_size
    p.font.color.rgb = text_color
    return pill

def set_speaker_note(slide, note_text):
    """Embeds the official presentation script into slide notes."""
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = note_text.strip()

# -------------------------------------------------------------
# SLIDE 1: TITLE SLIDE
# -------------------------------------------------------------
def build_slide_1(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)

    # Left Card
    card_left = add_card(slide, Inches(0.8), Inches(0.8), Inches(7.5), Inches(5.9), bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.5))
    add_pill_badge(slide, Inches(1.2), Inches(1.15), Inches(3.4), Inches(0.35), "M.TECH RESEARCH SEMINAR | IEEE ACCESS 2026", text_color=COLOR_AMBER, bg_color=COLOR_AMBER_BG, border_color=COLOR_AMBER, font_size=Pt(9.0))

    tb_title = slide.shapes.add_textbox(Inches(1.2), Inches(1.65), Inches(6.7), Inches(1.8))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    add_clean_paragraph(tf_t, "MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation", font_name=FONT_HEADING, font_size=Pt(20.5), bold=True, color=COLOR_NAVY)

    tb_sub = slide.shapes.add_textbox(Inches(1.2), Inches(3.60), Inches(6.7), Inches(0.45))
    tf_s = tb_sub.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
    add_clean_paragraph(tf_s, "Deep Learning-Based Steel Surface Defect Segmentation", font_size=Pt(13.5), bold=True, color=COLOR_AMBER)

    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(4.15), Inches(6.7), Inches(0.02))
    div.fill.solid()
    div.fill.fore_color.rgb = COLOR_MUTED
    div.line.fill.background()

    tb_meta = slide.shapes.add_textbox(Inches(1.2), Inches(4.30), Inches(6.7), Inches(2.2))
    tf_m = tb_meta.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_top = tf_m.margin_right = tf_m.margin_bottom = 0

    add_clean_paragraph(tf_m, "Author & Presenter:", font_size=Pt(9.5), bold=True, color=COLOR_SLATE, space_after=Pt(2))
    add_clean_paragraph(tf_m, "Amen Parmar  |  M.Tech (AIML)  |  Roll No: 2502010010", font_size=Pt(12.5), bold=True, color=COLOR_NAVY, space_after=Pt(4))
    add_clean_paragraph(tf_m, "Co-authors: Amit Kumar Bairwa, Varun Kumar", font_size=Pt(10.0), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(3))
    add_clean_paragraph(tf_m, "Department of Computer Science and Engineering", font_size=Pt(9.5), bold=False, color=COLOR_SLATE, space_after=Pt(1))
    add_clean_paragraph(tf_m, "Manipal University Jaipur, Jaipur, Rajasthan, India", font_size=Pt(9.5), bold=False, color=COLOR_SLATE, space_after=Pt(0))

    # Right Conceptual Diagram Card
    card_right = add_card(slide, Inches(8.6), Inches(0.8), Inches(3.9), Inches(5.9), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER, border_width=Pt(1.5))

    tb_dt = slide.shapes.add_textbox(Inches(8.8), Inches(1.1), Inches(3.5), Inches(0.35))
    tf_dt = tb_dt.text_frame
    add_clean_paragraph(tf_dt, "INSPECTION PIPELINE OVERVIEW", font_size=Pt(10.0), bold=True, color=COLOR_NAVY, alignment=PP_ALIGN.CENTER)

    # Step 1: Raw Steel Strip
    s1 = add_card(slide, Inches(9.0), Inches(1.55), Inches(3.1), Inches(1.05), bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.2))
    tb_s1 = slide.shapes.add_textbox(Inches(9.1), Inches(1.62), Inches(2.9), Inches(0.90))
    tf_s1 = tb_s1.text_frame
    tf_s1.margin_left = tf_s1.margin_top = tf_s1.margin_right = tf_s1.margin_bottom = 0
    add_clean_paragraph(tf_s1, "1. Raw Steel Strip", font_size=Pt(10.5), bold=True, color=COLOR_NAVY, space_after=Pt(2))
    add_clean_paragraph(tf_s1, "256x256 Grayscale • Optical Surface", font_size=Pt(8.5), bold=False, color=COLOR_SLATE, space_after=Pt(1))
    add_clean_paragraph(tf_s1, "Sub-1% Micro & Low-Contrast Defect", font_size=Pt(8.5), bold=False, color=COLOR_SLATE, space_after=Pt(0))

    arr1 = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(10.35), Inches(2.68), Inches(0.4), Inches(0.32))
    arr1.fill.solid()
    arr1.fill.fore_color.rgb = COLOR_AMBER
    arr1.line.fill.background()

    # Step 2: MSBA-Net Dual Stream
    s2 = add_card(slide, Inches(9.0), Inches(3.08), Inches(3.1), Inches(1.25), bg_color=COLOR_BLUE_BG, border_color=COLOR_BLUE, border_width=Pt(1.2))
    tb_s2 = slide.shapes.add_textbox(Inches(9.1), Inches(3.15), Inches(2.9), Inches(1.10))
    tf_s2 = tb_s2.text_frame
    tf_s2.margin_left = tf_s2.margin_top = tf_s2.margin_right = tf_s2.margin_bottom = 0
    add_clean_paragraph(tf_s2, "2. MSBA-Net Architecture", font_size=Pt(10.5), bold=True, color=COLOR_BLUE, space_after=Pt(2))
    add_clean_paragraph(tf_s2, "• MSFP: Multi-Scale Feature Dilations", font_size=Pt(8.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_s2, "• BAS: High-Res Boundary Stream", font_size=Pt(8.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_s2, "• BGFF: Spatial Attention Feature Fusion", font_size=Pt(8.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    arr2 = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(10.35), Inches(4.40), Inches(0.4), Inches(0.32))
    arr2.fill.solid()
    arr2.fill.fore_color.rgb = COLOR_GREEN
    arr2.line.fill.background()

    # Step 3: Segmentation Mask
    s3 = add_card(slide, Inches(9.0), Inches(4.80), Inches(3.1), Inches(1.05), bg_color=COLOR_GREEN_BG, border_color=COLOR_GREEN, border_width=Pt(1.2))
    tb_s3 = slide.shapes.add_textbox(Inches(9.1), Inches(4.88), Inches(2.9), Inches(0.90))
    tf_s3 = tb_s3.text_frame
    tf_s3.margin_left = tf_s3.margin_top = tf_s3.margin_right = tf_s3.margin_bottom = 0
    add_clean_paragraph(tf_s3, "3. Pixel Defect Mask", font_size=Pt(10.5), bold=True, color=COLOR_GREEN, space_after=Pt(2))
    add_clean_paragraph(tf_s3, "Precise Boundary Contours", font_size=Pt(8.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_s3, "97.01% mIoU • 92.48% Tiny mIoU", font_size=Pt(8.5), bold=True, color=COLOR_NAVY, space_after=Pt(0))

    add_pill_badge(slide, Inches(8.9), Inches(6.05), Inches(3.3), Inches(0.35), "Sub-Millimeter Micro-Defect Localization", text_color=COLOR_NAVY, bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, font_size=Pt(9.0))

    set_speaker_note(slide, """SLIDE 1 — TITLE (45–60 seconds)
Speaker Script:
"Good morning, respected members of the evaluation committee, professors, and fellow scholars. My name is Amen Parmar, M.Tech student in Artificial Intelligence and Machine Learning at Manipal University Jaipur, Roll Number 2502010010.

Today, I am honored to present our research paper titled: 'MSBA-Net: Multi-Scale Feature Enhancement and Boundary-Aware Learning for Small and Low-Contrast Steel Surface Defect Segmentation', co-authored with Dr. Amit Kumar Bairwa and Dr. Varun Kumar.

In modern manufacturing, hot and cold rolled steel represents the backbone of critical industries from automotive to infrastructure. However, automated visual defect segmentation on steel strips faces fundamental optical and geometric challenges: defects are frequently microscopic—occupying less than one percent of an image—and their boundaries blend continuously into the textured metal background.

In this presentation, I will walk you through how our proposed architecture, MSBA-Net, solves these challenges through parallel multi-scale feature preservation and explicit boundary-guided attention. Let us examine the industrial motivation behind this work."
""")

# -------------------------------------------------------------
# SLIDE 2: MOTIVATION & PROBLEM
# -------------------------------------------------------------
def build_slide_2(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Industrial Problem & Motivation", "Why Steel Surface Defect Segmentation?", "Automated optical inspection must reliably catch microscopic flaws moving at high strip speeds.")

    start_x = Inches(0.8)

    # 1. Industrial Flow Chain (5 connected steps)
    steps = [
        ("High-Speed Rolling", "Strips move at 15–20 m/s"),
        ("Surface Inspection", "Line-scan optical sensors"),
        ("Micro & Faint Defects", "Sub-1% area, low contrast"),
        ("Difficult Segmentation", "Extreme class imbalance"),
        ("Risk of Missed Flaws", "Catastrophic failure in use")
    ]
    card_w = Inches(2.15)
    gap = Inches(0.24)
    y_chain = Inches(1.55)
    h_chain = Inches(0.82)

    for i, (title, desc) in enumerate(steps):
        x = start_x + i * (card_w + gap)
        bg = COLOR_AMBER_BG if i == 2 or i == 4 else COLOR_CARD_WHITE
        bc = COLOR_AMBER if i == 2 or i == 4 else COLOR_BORDER
        add_card(slide, x, y_chain, card_w, h_chain, bg_color=bg, border_color=bc, border_width=Pt(1.2))

        tb = slide.shapes.add_textbox(x + Inches(0.10), y_chain + Inches(0.08), card_w - Inches(0.20), h_chain - Inches(0.16))
        tf = tb.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        add_clean_paragraph(tf, f"{i+1}. {title}", font_size=Pt(9.5), bold=True, color=COLOR_NAVY, space_after=Pt(2))
        add_clean_paragraph(tf, desc, font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(0))

        if i < 4:
            arr = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x + card_w + Inches(0.04), y_chain + Inches(0.28), Inches(0.16), Inches(0.24))
            arr.fill.solid()
            arr.fill.fore_color.rgb = COLOR_MUTED
            arr.line.fill.background()

    # 2. Key Facts Dashboard (4 Cards)
    y_facts = Inches(2.48)
    h_facts = Inches(1.28)
    w_fact = Inches(2.78)
    gap_fact = Inches(0.20)
    facts = [
        ("15 – 20 m/s", "STRIP SPEED", "Production lines run at 54–72 km/h; inspection algorithms must complete inference in <25 ms.", COLOR_BLUE, COLOR_BLUE_BG),
        ("< 1% Area", "MICRO-DEFECTS", "Hairline crazing and tiny pit depressions occupy less than 1% of total image pixels.", COLOR_RED, COLOR_RED_BG),
        ("Low Contrast", "SUBTLE GRADIENTS", "Weak intensity transitions between defect contours and ambient steel roll textures.", COLOR_AMBER, COLOR_AMBER_BG),
        ("> 98% Normal", "CLASS IMBALANCE", "Over 98% of captured pixels are defect-free steel, causing severe gradient bias in training.", COLOR_GREEN, COLOR_GREEN_BG)
    ]

    for i, (num, label, desc, col, col_bg) in enumerate(facts):
        x = start_x + i * (w_fact + gap_fact)
        add_card(slide, x, y_facts, w_fact, h_facts, bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.2))
        add_pill_badge(slide, x + Inches(0.12), y_facts + Inches(0.10), Inches(1.35), Inches(0.24), label, text_color=col, bg_color=col_bg, border_color=col, font_size=Pt(8.0))

        tb = slide.shapes.add_textbox(x + Inches(0.12), y_facts + Inches(0.38), w_fact - Inches(0.24), Inches(0.85))
        tf = tb.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        add_clean_paragraph(tf, num, font_name=FONT_HEADING, font_size=Pt(14), bold=True, color=COLOR_NAVY, space_after=Pt(2))
        add_clean_paragraph(tf, desc, font_size=Pt(7.8), bold=False, color=COLOR_SLATE, space_after=Pt(0))

    # 3. Steel Strip Defect Gallery (6 categories)
    y_gal = Inches(3.88)
    h_gal = Inches(2.82)
    w_full = Inches(11.73)
    add_card(slide, start_x, y_gal, w_full, h_gal, bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER, border_width=Pt(1.2))

    tb_gtitle = slide.shapes.add_textbox(start_x + Inches(0.20), y_gal + Inches(0.10), w_full - Inches(0.4), Inches(0.28))
    tf_gt = tb_gtitle.text_frame
    add_clean_paragraph(tf_gt, "SIX CORE INDUSTRIAL DEFECT CATEGORIES ON STEEL STRIP SURFACES (NEU BENCHMARK)", font_size=Pt(9.5), bold=True, color=COLOR_NAVY, space_after=Pt(0))

    defects = [
        ("Crazing (Cr)", "Network of micro-cracks", "Hairline cracks vanish during downsampling."),
        ("Inclusion (In)", "Non-metallic particles", "Elongated flaws with subtle edge contrast."),
        ("Patches (Pa)", "Plate surface peeling", "Irregular contours merge with metal texture."),
        ("Pitted Surface (PS)", "Cavity pit clusters", "Dense clusters of tiny sub-1% depressions."),
        ("Rolled-in Scale (RS)", "Oxide scale pressed in", "Fish-scale sheets with irregular boundaries."),
        ("Scratches (Sc)", "Longitudinal abrasions", "High-aspect-ratio grooves along rolling line.")
    ]
    w_d = Inches(1.82)
    gap_d = Inches(0.12)
    y_d = y_gal + Inches(0.40)
    h_d = Inches(2.28)

    for i, (d_name, d_sub, d_chal) in enumerate(defects):
        xd = start_x + Inches(0.18) + i * (w_d + gap_d)
        add_card(slide, xd, y_d, w_d, h_d, bg_color=COLOR_CARD_WHITE, border_color=COLOR_MUTED, border_width=Pt(1.0))

        tb_d = slide.shapes.add_textbox(xd + Inches(0.08), y_d + Inches(0.10), w_d - Inches(0.16), h_d - Inches(0.20))
        tf_d = tb_d.text_frame
        tf_d.margin_left = tf_d.margin_top = tf_d.margin_right = tf_d.margin_bottom = 0

        add_clean_paragraph(tf_d, d_name, font_size=Pt(9.5), bold=True, color=COLOR_NAVY, space_after=Pt(2))
        add_clean_paragraph(tf_d, d_sub, font_size=Pt(8.0), bold=True, color=COLOR_AMBER, space_after=Pt(4))
        add_clean_paragraph(tf_d, "Morphological Challenge:", font_size=Pt(7.5), bold=True, color=COLOR_SLATE, space_after=Pt(2))
        add_clean_paragraph(tf_d, f"• {d_chal}", font_size=Pt(7.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(4))
        add_clean_paragraph(tf_d, "Dataset Volume:", font_size=Pt(7.5), bold=True, color=COLOR_SLATE, space_after=Pt(1))
        add_clean_paragraph(tf_d, "300 images (50 test)", font_size=Pt(7.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    set_speaker_note(slide, """SLIDE 2 — MOTIVATION & PROBLEM (60–75 seconds)
Speaker Script:
"To understand why this research is vital, let us examine the reality of a modern steel production plant.

In hot and cold strip mills, continuous steel strips travel beneath optical inspection systems at staggering speeds of 15 to 20 meters per second—that is up to 72 kilometers per hour. At these velocities, manual visual inspection by human operators is physically impossible. Inspection must be fully automated, operating at real-time speeds with zero margin for error.

However, automated visual inspection faces three severe obstacles:
First, micro-scale defects such as hairline crazing cracks or tiny pit depressions frequently occupy less than 1% of the entire image area.
Second, defects exhibit very low intensity contrast against the ambient rolled metal texture. The transition zone between normal steel and defective steel is often just a gradual gradient of a few gray levels.
Third, more than 98% of all image pixels belong to defect-free steel, creating an overwhelming class imbalance.

At the bottom of the slide, you see the six major defect categories defined in the NEU benchmark: crazing, inclusions, patches, pitted surfaces, rolled-in scale, and scratches. If a segmentation model misses a tiny hairline crack or mistakes an inclusion for normal steel, that defective coil is shipped to an automotive or aerospace customer, leading to catastrophic structural failure during stamping or welding.

Therefore, robust, pixel-accurate segmentation of micro and low-contrast flaws is an urgent industrial necessity."
""")

# -------------------------------------------------------------
# SLIDE 3: KEY CHALLENGES & RESEARCH GAP
# -------------------------------------------------------------
def build_slide_3(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Research Challenges & Architectural Gap", "Why Existing Segmentation Methods Struggle", "Standard deep convolutional networks suffer catastrophic feature loss on industrial surfaces.")

    start_x = Inches(0.8)
    w_card = Inches(3.72)
    gap_card = Inches(0.28)
    y_card = Inches(1.65)
    h_card = Inches(3.35)

    challenges = [
        ("1. MICRO-SCALE DEFECTS", "Hairline cracks and tiny defects disappear during downsampling.", [
            "Consecutive max-pooling downsamples feature maps by 16x or 32x.",
            "Sub-1% area defects (crazing, pits) shrink into sub-pixel representations.",
            "By the bottleneck stage, high-frequency spatial details are erased.",
            "Result: Severe false negatives on the smallest, most critical flaws."
        ], COLOR_RED, COLOR_RED_BG),
        ("2. LOW-CONTRAST BOUNDARIES", "Weak intensity differences make defect edges difficult to distinguish.", [
            "Rolling processes produce natural surface texture and reflection gradients.",
            "Defect perimeters lack sharp grayscale edges, creating ambiguous zones.",
            "Standard networks lack explicit edge supervision, relying purely on area loss.",
            "Result: Predicted masks bleed into normal steel or produce blurry contours."
        ], COLOR_AMBER, COLOR_AMBER_BG),
        ("3. OPTICAL DEGRADATION", "Noise, blur, and low contrast severely reduce segmentation quality.", [
            "Rolling environments suffer from mechanical vibrations and strip flutter.",
            "Line-scan cameras capture defocus blur, high-ISO noise, and uneven lighting.",
            "Conventional CNNs trained on pristine data degrade severely in plant trials.",
            "Result: Fragile deployments that trigger excessive false alarms."
        ], COLOR_BLUE, COLOR_BLUE_BG)
    ]

    for i, (title, sub, bullets, col, col_bg) in enumerate(challenges):
        x = start_x + i * (w_card + gap_card)
        add_card(slide, x, y_card, w_card, h_card, bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.2))
        add_pill_badge(slide, x + Inches(0.2), y_card + Inches(0.18), Inches(2.2), Inches(0.28), title, text_color=col, bg_color=col_bg, border_color=col, font_size=Pt(8.5))

        tb = slide.shapes.add_textbox(x + Inches(0.2), y_card + Inches(0.52), w_card - Inches(0.4), h_card - Inches(0.60))
        tf = tb.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        add_clean_paragraph(tf, f'"{sub}"', font_size=Pt(10.0), bold=True, color=COLOR_NAVY, space_after=Pt(6))
        for b in bullets:
            add_clean_paragraph(tf, f"• {b}", font_size=Pt(8.3), bold=False, color=COLOR_SLATE, space_after=Pt(3))

    # Bottom Diagnostic Flow & Solution Gap
    y_bot = Inches(5.15)
    h_bot = Inches(1.68)
    w_full = Inches(11.73)
    add_card(slide, start_x, y_bot, w_full, h_bot, bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER, border_width=Pt(1.2))

    tb_fail = slide.shapes.add_textbox(start_x + Inches(0.3), y_bot + Inches(0.15), Inches(5.5), Inches(1.35))
    tf_f = tb_fail.text_frame
    add_clean_paragraph(tf_f, "EXISTING CNN PIPELINE BOTTLENECK:", font_size=Pt(9.5), bold=True, color=COLOR_RED, space_after=Pt(4))
    add_clean_paragraph(tf_f, "Standard Downsampling (Pooling / Striding)", font_size=Pt(8.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(2))
    add_clean_paragraph(tf_f, "        ↓", font_size=Pt(8.5), bold=True, color=COLOR_MUTED, space_after=Pt(2))
    add_clean_paragraph(tf_f, "Feature Dilution & Blurry Boundary Representations", font_size=Pt(8.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(2))
    add_clean_paragraph(tf_f, "        ↓", font_size=Pt(8.5), bold=True, color=COLOR_MUTED, space_after=Pt(2))
    add_clean_paragraph(tf_f, "High False Alarms + Undetected Sub-1% Micro-Cracks", font_size=Pt(8.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    div_v = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, start_x + Inches(5.9), y_bot + Inches(0.15), Inches(0.02), Inches(1.35))
    div_v.fill.solid()
    div_v.fill.fore_color.rgb = COLOR_MUTED
    div_v.line.fill.background()

    tb_sol = slide.shapes.add_textbox(start_x + Inches(6.2), y_bot + Inches(0.15), Inches(5.2), Inches(1.35))
    tf_s = tb_sol.text_frame
    add_clean_paragraph(tf_s, "THE ARCHITECTURAL RESEARCH GAP:", font_size=Pt(9.5), bold=True, color=COLOR_GREEN, space_after=Pt(4))
    add_clean_paragraph(tf_s, "Industrial defect segmentation fundamentally requires:", font_size=Pt(8.5), bold=False, color=COLOR_NAVY, space_after=Pt(3))
    add_clean_paragraph(tf_s, "1. Multi-Scale Feature Preservation (MSFP) to retain fine crack textures across receptive fields without spatial downsampling loss.", font_size=Pt(8.2), bold=False, color=COLOR_SLATE, space_after=Pt(3))
    add_clean_paragraph(tf_s, "2. Boundary-Aware Guidance (BAS + BGFF) with explicit edge supervision to guide decoder feature maps along subtle perimeters.", font_size=Pt(8.2), bold=False, color=COLOR_SLATE, space_after=Pt(0))

    set_speaker_note(slide, """SLIDE 3 — KEY CHALLENGES & RESEARCH GAP (60–75 seconds)
Speaker Script:
"Why do standard, general-purpose deep learning segmentation models fail on steel surface defect inspection? As shown on this slide, there are three primary failure modes.

The first challenge is Micro-Scale Defects. General segmentation backbones—like U-Net, DeepLab, or FPN—rely on aggressive downsampling through successive pooling or strided convolutions to expand receptive fields. When an input image is downsampled 16 or 32 times, a defect occupying less than 1% of the surface area—such as a fine crazing crack or small pit—literally vanishes. By the time features reach the bottleneck, its spatial footprint is reduced to a fraction of a single feature cell.

The second challenge is Low-Contrast Boundaries. Defect borders on rolled steel do not exhibit sharp, distinct edges; they blend into rolling stripes and ambient lighting gradients. Conventional architectures supervise only region overlap; they do not explicitly model boundary contours. As a consequence, decoder outputs leak across boundaries, resulting in blurry, imprecise defect masks.

The third challenge is Optical Degradation. Under real shop-floor conditions, mechanical vibrations cause optical defocus blur, line-scan cameras introduce high-ISO sensor noise, and illumination varies unpredictably.

As summarized at the bottom: standard CNN pipelines dilute fine features and smear boundaries. To close this gap, what is needed is a dedicated dual strategy: Multi-Scale Feature Preservation to protect fine crack details, coupled with an explicit Boundary-Aware Stream to guide contour delineation. This brings us directly to our proposed solution: MSBA-Net."
""")

# -------------------------------------------------------------
# SLIDE 4: PROPOSED SOLUTION / CORE IDEA
# -------------------------------------------------------------
def build_slide_4(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Proposed Methodology", "MSBA-Net: The Proposed Solution", "A dual-stream collaborative architecture engineered to decouple scale diversity and boundary localization.")

    start_x = Inches(0.8)
    add_card(slide, start_x, Inches(1.65), Inches(11.73), Inches(4.50), bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.5))

    # Step 1: Input Box (Top Center)
    c_in = add_card(slide, Inches(4.9), Inches(1.85), Inches(3.5), Inches(0.65), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER, border_width=Pt(1.2))
    tb_in = slide.shapes.add_textbox(Inches(5.0), Inches(1.95), Inches(3.3), Inches(0.45))
    tf_in = tb_in.text_frame
    add_clean_paragraph(tf_in, "INPUT STEEL SURFACE IMAGE (256 × 256 × 1)", font_size=Pt(10.0), bold=True, color=COLOR_NAVY, alignment=PP_ALIGN.CENTER)

    # Dual Fork Arrows from under Input Box
    arr_f1 = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(3.5), Inches(2.55), Inches(0.35), Inches(0.28))
    arr_f1.fill.solid()
    arr_f1.fill.fore_color.rgb = COLOR_GREEN
    arr_f1.line.fill.background()

    arr_f2 = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(9.5), Inches(2.55), Inches(0.35), Inches(0.28))
    arr_f2.fill.solid()
    arr_f2.fill.fore_color.rgb = COLOR_AMBER
    arr_f2.line.fill.background()

    # Stream 1: MSFP (Left Card)
    add_card(slide, Inches(1.3), Inches(2.88), Inches(4.5), Inches(1.45), bg_color=COLOR_GREEN_BG, border_color=COLOR_GREEN, border_width=Pt(1.5))
    tb_msfp = slide.shapes.add_textbox(Inches(1.45), Inches(2.95), Inches(4.2), Inches(1.30))
    tf_msfp = tb_msfp.text_frame
    add_clean_paragraph(tf_msfp, "STREAM 1: MULTI-SCALE FEATURE PRESERVATION (MSFP)", font_size=Pt(10.0), bold=True, color=COLOR_GREEN, space_after=Pt(3))
    add_clean_paragraph(tf_msfp, "• Parallel Dilated Depthwise Convolutions (r = 1, 2, 4)", font_size=Pt(8.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(2))
    add_clean_paragraph(tf_msfp, "• Multiple receptive fields (3x3, 5x5, 9x9) without spatial downsampling", font_size=Pt(8.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(2))
    add_clean_paragraph(tf_msfp, "• Simultaneously preserves sub-1% cracks and extended patches", font_size=Pt(8.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(2))
    add_clean_paragraph(tf_msfp, "• Residual identity connections retain fine textural details", font_size=Pt(8.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    # Stream 2: BAS (Right Card)
    add_card(slide, Inches(7.5), Inches(2.88), Inches(4.5), Inches(1.45), bg_color=COLOR_AMBER_BG, border_color=COLOR_AMBER, border_width=Pt(1.5))
    tb_bas = slide.shapes.add_textbox(Inches(7.65), Inches(2.95), Inches(4.2), Inches(1.30))
    tf_bas = tb_bas.text_frame
    add_clean_paragraph(tf_bas, "STREAM 2: BOUNDARY-AWARE STREAM (BAS)", font_size=Pt(10.0), bold=True, color=COLOR_AMBER, space_after=Pt(3))
    add_clean_paragraph(tf_bas, "• Taps early, high-resolution encoder features (Stages 1, 2, 3)", font_size=Pt(8.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(2))
    add_clean_paragraph(tf_bas, "• Dedicated boundary extraction head with deep edge supervision", font_size=Pt(8.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(2))
    add_clean_paragraph(tf_bas, "• Morphological gradient ground truth: B_GT = (M ⊕ K3) - (M ⊖ K3)", font_size=Pt(8.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(2))
    add_clean_paragraph(tf_bas, "• Prevents high-frequency edge attenuation caused by deep pooling", font_size=Pt(8.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    # Convergence Arrows
    arr_c1 = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(3.5), Inches(4.38), Inches(0.35), Inches(0.26))
    arr_c1.fill.solid()
    arr_c1.fill.fore_color.rgb = COLOR_PURPLE
    arr_c1.line.fill.background()

    arr_c2 = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(9.5), Inches(4.38), Inches(0.35), Inches(0.26))
    arr_c2.fill.solid()
    arr_c2.fill.fore_color.rgb = COLOR_PURPLE
    arr_c2.line.fill.background()

    # Step 3: Fusion BGFF (Bottom Center)
    add_card(slide, Inches(3.4), Inches(4.68), Inches(6.5), Inches(0.68), bg_color=COLOR_PURPLE_BG, border_color=COLOR_PURPLE, border_width=Pt(1.5))
    tb_bgff = slide.shapes.add_textbox(Inches(3.5), Inches(4.72), Inches(6.3), Inches(0.58))
    tf_bgff = tb_bgff.text_frame
    add_clean_paragraph(tf_bgff, "BOUNDARY-GUIDED FEATURE FUSION (BGFF)", font_size=Pt(10.0), bold=True, color=COLOR_PURPLE, alignment=PP_ALIGN.CENTER, space_after=Pt(2))
    add_clean_paragraph(tf_bgff, "Spatial Attention Gate: A_spat = σ(Conv1x1([F_bound; F_dec])) • Modulates decoder features along boundary zones", font_size=Pt(8.5), bold=False, color=COLOR_NAVY_LIGHT, alignment=PP_ALIGN.CENTER, space_after=Pt(0))

    arr_out = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(6.45), Inches(5.40), Inches(0.35), Inches(0.24))
    arr_out.fill.solid()
    arr_out.fill.fore_color.rgb = COLOR_GREEN
    arr_out.line.fill.background()

    # Step 4: Final Mask Card
    add_card(slide, Inches(4.6), Inches(5.68), Inches(4.1), Inches(0.38), bg_color=COLOR_GREEN_BG, border_color=COLOR_GREEN, border_width=Pt(1.2))
    tb_mk = slide.shapes.add_textbox(Inches(4.7), Inches(5.72), Inches(3.9), Inches(0.30))
    tf_mk = tb_mk.text_frame
    add_clean_paragraph(tf_mk, "FINAL DEFECT SEGMENTATION MASK (256 × 256)", font_size=Pt(9.5), bold=True, color=COLOR_GREEN, alignment=PP_ALIGN.CENTER, space_after=Pt(0))

    # Bottom Takeaway Card
    add_card(slide, start_x, Inches(6.25), Inches(11.73), Inches(0.60), bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER, border_width=Pt(1.2))
    tb_tk = slide.shapes.add_textbox(start_x + Inches(0.2), Inches(6.35), Inches(11.33), Inches(0.40))
    tf_tk = tb_tk.text_frame
    add_clean_paragraph(tf_tk, "CORE TAKEAWAY: Preserve Fine Features Across Scales (MSFP)  +  Explicitly Guide Edge Contours (BAS & BGFF)  +  Combat >98% Background Imbalance", font_size=Pt(9.5), bold=True, color=COLOR_NAVY, alignment=PP_ALIGN.CENTER, space_after=Pt(0))

    set_speaker_note(slide, """SLIDE 4 — PROPOSED SOLUTION / CORE IDEA (50–65 seconds)
Speaker Script:
"To overcome the limitations of classical and standard deep learning models, we propose MSBA-Net—Multi-Scale Feature Enhancement and Boundary-Aware Network.

The core philosophy of MSBA-Net is decoupling: rather than forcing a single convolutional backbone to simultaneously resolve broad defect contexts and razor-sharp boundaries, we formulate a dual-stream collaborative architecture.

As illustrated in this conceptual diagram:
When a 256 by 256 grayscale steel image enters the network, it is processed across two complementary streams:
First, Stream 1—Multi-Scale Feature Preservation, or MSFP. Embedded inside the encoder stages, MSFP uses parallel dilated depthwise convolutions with dilation rates 1, 2, and 4. This captures multiple receptive fields simultaneously, ensuring that tiny hairline cracks and broad surface patches are captured without downsampling resolution loss.

Second, Stream 2—the Boundary-Aware Stream, or BAS. Instead of discarding early high-resolution features, BAS taps Stages 1, 2, and 3, passing them to a dedicated boundary prediction head supervised by explicit morphological ground-truth contours.

Finally, in the decoder stage, our Boundary-Guided Feature Fusion module—BGFF—uses spatial attention gating to fuse the learned boundary confidence directly into the decoder representations.

The resulting takeaway is clear: we preserve fine features across scales, guide boundaries with explicit edge priors, and tame background class imbalance. Now, let us examine the complete architecture in detail."
""")

# -------------------------------------------------------------
# SLIDE 5: MSBA-NET ARCHITECTURE (HERO FLOWCHART - SEPARATE TEXTBOXES)
# -------------------------------------------------------------
def build_slide_5(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Detailed System Architecture", "Overall Architecture of MSBA-Net", "Hierarchical multi-scale encoder, auxiliary boundary stream, and boundary-guided attention gating.")

    start_x = Inches(0.8)
    add_card(slide, start_x, Inches(1.65), Inches(11.73), Inches(5.25), bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.5))

    # --- TOP ROW: AUXILIARY BOUNDARY STREAM (BAS) ---
    add_card(slide, Inches(4.3), Inches(1.85), Inches(1.75), Inches(0.78), bg_color=COLOR_AMBER_BG, border_color=COLOR_AMBER, border_width=Pt(1.4))
    tb_b = slide.shapes.add_textbox(Inches(4.35), Inches(1.90), Inches(1.65), Inches(0.68))
    tf_b = tb_b.text_frame
    add_clean_paragraph(tf_b, "BAS Stream", font_size=Pt(9.5), bold=True, color=COLOR_AMBER, space_after=Pt(1))
    add_clean_paragraph(tf_b, "Edge Extraction", font_size=Pt(8.0), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_b, "64 ch, Up-Conv", font_size=Pt(8.0), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    arr_b1 = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(6.12), Inches(2.15), Inches(0.25), Inches(0.18))
    arr_b1.fill.solid()
    arr_b1.fill.fore_color.rgb = COLOR_AMBER
    arr_b1.line.fill.background()

    add_card(slide, Inches(6.42), Inches(1.85), Inches(1.75), Inches(0.78), bg_color=COLOR_RED_BG, border_color=COLOR_RED, border_width=Pt(1.4))
    tb_bh = slide.shapes.add_textbox(Inches(6.47), Inches(1.90), Inches(1.65), Inches(0.68))
    tf_bh = tb_bh.text_frame
    add_clean_paragraph(tf_bh, "Boundary Head", font_size=Pt(9.5), bold=True, color=COLOR_RED, space_after=Pt(1))
    add_clean_paragraph(tf_bh, "Contour Prediction", font_size=Pt(8.0), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_bh, "1 x 256 x 256 (P_bound)", font_size=Pt(8.0), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    arr_b2 = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(8.24), Inches(2.15), Inches(0.65), Inches(0.18))
    arr_b2.fill.solid()
    arr_b2.fill.fore_color.rgb = COLOR_PURPLE
    arr_b2.line.fill.background()

    add_card(slide, Inches(8.95), Inches(1.85), Inches(1.65), Inches(0.78), bg_color=COLOR_PURPLE_BG, border_color=COLOR_PURPLE, border_width=Pt(1.4))
    tb_bg = slide.shapes.add_textbox(Inches(9.00), Inches(1.90), Inches(1.55), Inches(0.68))
    tf_bg = tb_bg.text_frame
    add_clean_paragraph(tf_bg, "BGFF Gate", font_size=Pt(9.5), bold=True, color=COLOR_PURPLE, space_after=Pt(1))
    add_clean_paragraph(tf_bg, "Spatial Attention", font_size=Pt(8.0), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_bg, "64 x 128 x 128", font_size=Pt(8.0), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    add_card(slide, Inches(10.75), Inches(1.85), Inches(1.55), Inches(0.78), bg_color=COLOR_RED_BG, border_color=COLOR_RED, border_width=Pt(1.2))
    tb_sup = slide.shapes.add_textbox(Inches(10.80), Inches(1.90), Inches(1.45), Inches(0.68))
    tf_sup = tb_sup.text_frame
    add_clean_paragraph(tf_sup, "Loss Supervision", font_size=Pt(9.0), bold=True, color=COLOR_RED, space_after=Pt(1))
    add_clean_paragraph(tf_sup, "0.3 L_BCE + 0.3 L_Dice", font_size=Pt(7.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_sup, "+ 0.2 L_Focal + 0.2 L_bound", font_size=Pt(7.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    # --- MIDDLE ROW: MAIN BACKBONE PIPELINE ---
    y_mid = Inches(2.95)
    h_mid = Inches(0.82)

    add_card(slide, Inches(1.05), y_mid, Inches(1.25), h_mid, bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER, border_width=Pt(1.2))
    tb_in = slide.shapes.add_textbox(Inches(1.10), y_mid + Inches(0.06), Inches(1.15), h_mid - Inches(0.12))
    tf_in = tb_in.text_frame
    add_clean_paragraph(tf_in, "Input Image", font_size=Pt(9.5), bold=True, color=COLOR_NAVY, space_after=Pt(1))
    add_clean_paragraph(tf_in, "Steel Surface", font_size=Pt(7.5), bold=False, color=COLOR_SLATE, space_after=Pt(1))
    add_clean_paragraph(tf_in, "1 x 256 x 256", font_size=Pt(7.5), bold=False, color=COLOR_SLATE, space_after=Pt(0))

    arr_m0 = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(2.35), y_mid + Inches(0.30), Inches(0.20), Inches(0.18))
    arr_m0.fill.solid()
    arr_m0.fill.fore_color.rgb = COLOR_BLUE
    arr_m0.line.fill.background()

    add_card(slide, Inches(2.60), y_mid, Inches(1.45), h_mid, bg_color=COLOR_BLUE_BG, border_color=COLOR_BLUE, border_width=Pt(1.4))
    tb_e1 = slide.shapes.add_textbox(Inches(2.65), y_mid + Inches(0.06), Inches(1.35), h_mid - Inches(0.12))
    tf_e1 = tb_e1.text_frame
    add_clean_paragraph(tf_e1, "Encoder Stage 1", font_size=Pt(9.5), bold=True, color=COLOR_BLUE, space_after=Pt(1))
    add_clean_paragraph(tf_e1, "+ MSFP Block 1", font_size=Pt(7.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_e1, "32 x 256 x 256", font_size=Pt(7.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    arr_m1 = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(4.10), y_mid + Inches(0.30), Inches(0.20), Inches(0.18))
    arr_m1.fill.solid()
    arr_m1.fill.fore_color.rgb = COLOR_BLUE
    arr_m1.line.fill.background()

    add_card(slide, Inches(4.35), y_mid, Inches(1.45), h_mid, bg_color=COLOR_BLUE_BG, border_color=COLOR_BLUE, border_width=Pt(1.4))
    tb_e2 = slide.shapes.add_textbox(Inches(4.40), y_mid + Inches(0.06), Inches(1.35), h_mid - Inches(0.12))
    tf_e2 = tb_e2.text_frame
    add_clean_paragraph(tf_e2, "Encoder Stage 2", font_size=Pt(9.5), bold=True, color=COLOR_BLUE, space_after=Pt(1))
    add_clean_paragraph(tf_e2, "+ MSFP Block 2", font_size=Pt(7.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_e2, "64 x 128 x 128", font_size=Pt(7.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    arr_m2 = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(5.85), y_mid + Inches(0.30), Inches(0.20), Inches(0.18))
    arr_m2.fill.solid()
    arr_m2.fill.fore_color.rgb = COLOR_BLUE
    arr_m2.line.fill.background()

    add_card(slide, Inches(6.10), y_mid, Inches(1.45), h_mid, bg_color=COLOR_BLUE_BG, border_color=COLOR_BLUE, border_width=Pt(1.4))
    tb_e3 = slide.shapes.add_textbox(Inches(6.15), y_mid + Inches(0.06), Inches(1.35), h_mid - Inches(0.12))
    tf_e3 = tb_e3.text_frame
    add_clean_paragraph(tf_e3, "Encoder Stage 3", font_size=Pt(9.5), bold=True, color=COLOR_BLUE, space_after=Pt(1))
    add_clean_paragraph(tf_e3, "+ MSFP Block 3", font_size=Pt(7.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_e3, "128 x 64 x 64", font_size=Pt(7.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    arr_m3 = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(7.60), y_mid + Inches(0.30), Inches(0.20), Inches(0.18))
    arr_m3.fill.solid()
    arr_m3.fill.fore_color.rgb = COLOR_NAVY
    arr_m3.line.fill.background()

    add_card(slide, Inches(7.85), y_mid, Inches(1.35), h_mid, bg_color=COLOR_CARD_ALT, border_color=COLOR_NAVY, border_width=Pt(1.4))
    tb_bot = slide.shapes.add_textbox(Inches(7.90), y_mid + Inches(0.06), Inches(1.25), h_mid - Inches(0.12))
    tf_bot = tb_bot.text_frame
    add_clean_paragraph(tf_bot, "Bottleneck", font_size=Pt(9.5), bold=True, color=COLOR_NAVY, space_after=Pt(1))
    add_clean_paragraph(tf_bot, "Dilated Context", font_size=Pt(7.5), bold=False, color=COLOR_SLATE, space_after=Pt(1))
    add_clean_paragraph(tf_bot, "256 x 32 x 32", font_size=Pt(7.5), bold=False, color=COLOR_SLATE, space_after=Pt(0))

    arr_m4 = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(9.25), y_mid + Inches(0.30), Inches(0.20), Inches(0.18))
    arr_m4.fill.solid()
    arr_m4.fill.fore_color.rgb = COLOR_AMBER
    arr_m4.line.fill.background()

    add_card(slide, Inches(9.50), y_mid, Inches(1.35), h_mid, bg_color=COLOR_AMBER_BG, border_color=COLOR_AMBER, border_width=Pt(1.4))
    tb_dec = slide.shapes.add_textbox(Inches(9.55), y_mid + Inches(0.06), Inches(1.25), h_mid - Inches(0.12))
    tf_dec = tb_dec.text_frame
    add_clean_paragraph(tf_dec, "Decoder (Up2)", font_size=Pt(9.5), bold=True, color=COLOR_AMBER, space_after=Pt(1))
    add_clean_paragraph(tf_dec, "Concat + Conv", font_size=Pt(7.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_dec, "64 x 128 x 128", font_size=Pt(7.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    arr_m5 = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(10.90), y_mid + Inches(0.30), Inches(0.20), Inches(0.18))
    arr_m5.fill.solid()
    arr_m5.fill.fore_color.rgb = COLOR_GREEN
    arr_m5.line.fill.background()

    add_card(slide, Inches(11.15), y_mid, Inches(1.20), h_mid, bg_color=COLOR_GREEN_BG, border_color=COLOR_GREEN, border_width=Pt(1.4))
    tb_out = slide.shapes.add_textbox(Inches(11.20), y_mid + Inches(0.06), Inches(1.10), h_mid - Inches(0.12))
    tf_out = tb_out.text_frame
    add_clean_paragraph(tf_out, "Output Mask", font_size=Pt(9.5), bold=True, color=COLOR_GREEN, space_after=Pt(1))
    add_clean_paragraph(tf_out, "Defect Prediction", font_size=Pt(7.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_out, "1 x 256 x 256", font_size=Pt(7.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    # --- BOTTOM PANEL: DETAILED STRUCTURE OF MSFP BLOCK ---
    y_panel = Inches(4.00)
    h_panel = Inches(2.70)
    add_card(slide, Inches(1.05), y_panel, Inches(11.20), h_panel, bg_color=COLOR_CARD_ALT, border_color=COLOR_GREEN, border_width=Pt(1.4))

    tb_mp = slide.shapes.add_textbox(Inches(1.25), y_panel + Inches(0.08), Inches(10.8), Inches(0.25))
    tf_mp = tb_mp.text_frame
    add_clean_paragraph(tf_mp, "DETAILED STRUCTURE OF MULTI-SCALE FEATURE PRESERVATION (MSFP) BLOCK", font_size=Pt(9.5), bold=True, color=COLOR_GREEN, space_after=Pt(0))

    b_w = Inches(2.05)
    b_gap = Inches(0.14)
    b_y = y_panel + Inches(0.42)
    b_h = Inches(2.14)

    branches = [
        ("Branch 1: Projection", "1 × 1 Conv (C / 4)", "Receptive Field: 1 x 1", "Direct linear feature transfer with minimal parameter overhead.", COLOR_NAVY, COLOR_CARD_WHITE),
        ("Branch 2: Micro Defect", "DConv 3 × 3, r = 1", "Receptive Field: 3 x 3", "Captures localized hairline cracks, fine crazing, and sub-1% pit pixels.", COLOR_GREEN, COLOR_GREEN_BG),
        ("Branch 3: Medium Defect", "DConv 3 × 3, r = 2", "Receptive Field: 5 x 5", "Captures inclusions, localized patches, and moderate textural flaws.", COLOR_AMBER, COLOR_AMBER_BG),
        ("Branch 4: Macro Defect", "DConv 3 × 3, r = 4", "Receptive Field: 9 x 9", "Captures broad patches, rolled-in scale sheets, and surrounding context.", COLOR_BLUE, COLOR_BLUE_BG),
        ("Feature Aggregation", "Concat + 1x1 + Residual", "Output Channels: C", "Combines C/4 branches into C channels + residual identity addition.", COLOR_PURPLE, COLOR_PURPLE_BG)
    ]

    for i, (b_name, b_sub, b_rf, b_desc, col, col_bg) in enumerate(branches):
        bx = Inches(1.22) + i * (b_w + b_gap)
        add_card(slide, bx, b_y, b_w, b_h, bg_color=col_bg, border_color=col, border_width=Pt(1.2))

        tb_b = slide.shapes.add_textbox(bx + Inches(0.08), b_y + Inches(0.08), b_w - Inches(0.16), b_h - Inches(0.16))
        tf_b = tb_b.text_frame
        tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0

        add_clean_paragraph(tf_b, b_name, font_size=Pt(9.0), bold=True, color=col, space_after=Pt(2))
        add_clean_paragraph(tf_b, b_sub, font_size=Pt(8.0), bold=True, color=COLOR_NAVY, space_after=Pt(2))
        add_clean_paragraph(tf_b, b_rf, font_size=Pt(7.8), bold=True, color=COLOR_NAVY_LIGHT, space_after=Pt(3))
        add_clean_paragraph(tf_b, b_desc, font_size=Pt(7.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    set_speaker_note(slide, """SLIDE 5 — MSBA-NET ARCHITECTURE (75–90 seconds)
Speaker Script:
"This slide presents the architectural schematic of MSBA-Net, faithfully recreated from Figure 1 of our paper.

Let us trace the information flow through the system:
At the middle row, the input grayscale image passes into a four-stage hierarchical encoder. Rather than standard convolutional layers that rapidly lose resolution, each encoder stage incorporates our Multi-Scale Feature Preservation (MSFP) block.

Notice the auxiliary branch at the top row: the Boundary-Aware Stream (BAS). BAS branches off early from Stages 1 and 2, where high-resolution structural gradients are still preserved. Instead of allowing downsampling to discard these contours, BAS processes them through up-convolutions into a dedicated Boundary Head that outputs a 256x256 boundary probability map.

This learned boundary representation then feeds directly into the BGFF—Boundary-Guided Feature Fusion—spatial attention gate. During decoder upsampling, BGFF generates a spatial attention map that weights decoder features according to boundary certainty. This directly modulates decoder features, sharpening defect contours while suppressing ambient background metal texture.

At the bottom panel, we detail the internal anatomy of an MSFP block. Within each stage, input features are partitioned into four parallel paths:
- Branch 1 applies a 1x1 projection.
- Branch 2 applies dilated depthwise convolution with dilation rate r=1, yielding a 3x3 receptive field for hairline micro-cracks.
- Branch 3 uses dilation r=2, creating a 5x5 receptive field for inclusions and pit clusters.
- Branch 4 uses dilation r=4, creating a 9x9 receptive field for broad patches and rolled-in scale.

These branches are concatenated and projected via a 1x1 convolution, followed by a residual identity addition. This design guarantees multi-receptive field coverage with zero gridding artifacts and lightweight computation."
""")

# -------------------------------------------------------------
# SLIDE 6: THREE KEY COMPONENTS (MSFP, BAS, BGFF)
# -------------------------------------------------------------
def build_slide_6(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Core Methodological Innovations", "Three Key Components: MSFP, BAS, and BGFF", "Detailed mathematical intuition and mechanics of each specialized module.")

    start_x = Inches(0.8)
    w_card = Inches(3.72)
    gap_card = Inches(0.28)
    y_card = Inches(1.65)
    h_card = Inches(5.25)

    # Component A: MSFP
    add_card(slide, start_x, y_card, w_card, h_card, bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.5))
    add_pill_badge(slide, start_x + Inches(0.2), y_card + Inches(0.18), Inches(3.3), Inches(0.30), "A. MULTI-SCALE PRESERVATION (MSFP)", text_color=COLOR_GREEN, bg_color=COLOR_GREEN_BG, border_color=COLOR_GREEN, font_size=Pt(8.5))

    tb_A = slide.shapes.add_textbox(start_x + Inches(0.2), y_card + Inches(0.55), w_card - Inches(0.4), h_card - Inches(1.30))
    tf_A = tb_A.text_frame
    tf_A.margin_left = tf_A.margin_top = tf_A.margin_right = tf_A.margin_bottom = 0

    add_clean_paragraph(tf_A, "Mathematical Formulation:", font_size=Pt(9.5), bold=True, color=COLOR_NAVY, space_after=Pt(3))
    add_clean_paragraph(tf_A, "X_MSFP = Concat(B_1, B_2, B_3, B_4)", font_size=Pt(8.5), bold=True, color=COLOR_GREEN, space_after=Pt(1))
    add_clean_paragraph(tf_A, "B_k = DConv_{3x3, r_k}(X_{in, k}),  r_k ∈ {1, 2, 4}", font_size=Pt(8.5), bold=True, color=COLOR_GREEN, space_after=Pt(8))

    add_clean_paragraph(tf_A, "Functional Mechanics:", font_size=Pt(9.0), bold=True, color=COLOR_NAVY, space_after=Pt(3))
    add_clean_paragraph(tf_A, "• Parallel Dilated Depthwise Convolutions:", font_size=Pt(8.2), bold=True, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_A, "  Receptive fields expand to 3x3, 5x5, 9x9 without decimation.", font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(4))
    add_clean_paragraph(tf_A, "• Hairline Micro-Crack Preservation:", font_size=Pt(8.2), bold=True, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_A, "  r=1 branch preserves 1–2 pixel crack details faithfully.", font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(4))
    add_clean_paragraph(tf_A, "• Broad Metallurgical Patch Coverage:", font_size=Pt(8.2), bold=True, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_A, "  r=4 branch retains surrounding industrial texture.", font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(4))
    add_clean_paragraph(tf_A, "• Zero Gridding Artifacts:", font_size=Pt(8.2), bold=True, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_A, "  Dilations kept within {1, 2, 4} for smooth contiguous sampling.", font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(0))

    y_tk = y_card + h_card - Inches(0.72)
    h_tk = Inches(0.58)

    add_card(slide, start_x + Inches(0.15), y_tk, w_card - Inches(0.30), h_tk, bg_color=COLOR_GREEN_BG, border_color=COLOR_GREEN, border_width=Pt(1.0))
    tb_tka = slide.shapes.add_textbox(start_x + Inches(0.20), y_tk + Inches(0.04), w_card - Inches(0.40), h_tk - Inches(0.08))
    tf_tka = tb_tka.text_frame
    add_clean_paragraph(tf_tka, "Key Takeaway: Captures fine details and broader context simultaneously without downsampling loss.", font_size=Pt(7.8), bold=True, color=COLOR_GREEN, space_after=Pt(0))

    # Component B: BAS
    cB_x = start_x + w_card + gap_card
    add_card(slide, cB_x, y_card, w_card, h_card, bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.5))
    add_pill_badge(slide, cB_x + Inches(0.2), y_card + Inches(0.18), Inches(3.3), Inches(0.30), "B. BOUNDARY-AWARE STREAM (BAS)", text_color=COLOR_AMBER, bg_color=COLOR_AMBER_BG, border_color=COLOR_AMBER, font_size=Pt(8.5))

    tb_B = slide.shapes.add_textbox(cB_x + Inches(0.2), y_card + Inches(0.55), w_card - Inches(0.4), h_card - Inches(1.35))
    tf_B = tb_B.text_frame
    tf_B.margin_left = tf_B.margin_top = tf_B.margin_right = tf_B.margin_bottom = 0

    add_clean_paragraph(tf_B, "Mathematical Formulation:", font_size=Pt(9.5), bold=True, color=COLOR_NAVY, space_after=Pt(3))
    add_clean_paragraph(tf_B, "B_GT = (M_GT ⊕ K_3) - (M_GT ⊖ K_3)", font_size=Pt(8.5), bold=True, color=COLOR_AMBER, space_after=Pt(1))
    add_clean_paragraph(tf_B, "K_3: 3x3 structuring element;  L_bound = BCE(P_bound, B_GT)", font_size=Pt(8.5), bold=True, color=COLOR_AMBER, space_after=Pt(8))

    add_clean_paragraph(tf_B, "Functional Mechanics:", font_size=Pt(9.0), bold=True, color=COLOR_NAVY, space_after=Pt(3))
    add_clean_paragraph(tf_B, "• Taps Shallow Encoder Stages:", font_size=Pt(8.2), bold=True, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_B, "  Stages 1 and 2 retain pristine high-frequency edge gradients.", font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(4))
    add_clean_paragraph(tf_B, "• Bilinear Feature Realignment:", font_size=Pt(8.2), bold=True, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_B, "  Intermediate channels projected and aligned to 256x256.", font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(4))
    add_clean_paragraph(tf_B, "• Morphological Edge Ground Truth:", font_size=Pt(8.2), bold=True, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_B, "  Exact 1-pixel boundary contours via dilation minus erosion.", font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(4))
    add_clean_paragraph(tf_B, "• Explicit Edge Supervision:", font_size=Pt(8.2), bold=True, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_B, "  Compels network to maintain sharp boundary gradients.", font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(0))

    add_card(slide, cB_x + Inches(0.15), y_tk, w_card - Inches(0.30), h_tk, bg_color=COLOR_AMBER_BG, border_color=COLOR_AMBER, border_width=Pt(1.0))
    tb_tkb = slide.shapes.add_textbox(cB_x + Inches(0.20), y_tk + Inches(0.04), w_card - Inches(0.40), h_tk - Inches(0.08))
    tf_tkb = tb_tkb.text_frame
    add_clean_paragraph(tf_tkb, "Key Takeaway: Preserves high-frequency contour information that standard downsampling obliterates.", font_size=Pt(7.8), bold=True, color=COLOR_AMBER, space_after=Pt(0))

    # Component C: BGFF
    cC_x = start_x + 2 * (w_card + gap_card)
    add_card(slide, cC_x, y_card, w_card, h_card, bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.5))
    add_pill_badge(slide, cC_x + Inches(0.2), y_card + Inches(0.18), Inches(3.3), Inches(0.30), "C. FEATURE FUSION (BGFF)", text_color=COLOR_PURPLE, bg_color=COLOR_PURPLE_BG, border_color=COLOR_PURPLE, font_size=Pt(8.5))

    tb_C = slide.shapes.add_textbox(cC_x + Inches(0.2), y_card + Inches(0.55), w_card - Inches(0.4), h_card - Inches(1.35))
    tf_C = tb_C.text_frame
    tf_C.margin_left = tf_C.margin_top = tf_C.margin_right = tf_C.margin_bottom = 0

    add_clean_paragraph(tf_C, "Mathematical Formulation:", font_size=Pt(9.5), bold=True, color=COLOR_NAVY, space_after=Pt(3))
    add_clean_paragraph(tf_C, "A_spat = σ(Conv_{1x1}([F_bound; F_dec]))", font_size=Pt(8.5), bold=True, color=COLOR_PURPLE, space_after=Pt(1))
    add_clean_paragraph(tf_C, "F_out = F_dec ⊙ (1 + A_spat)", font_size=Pt(8.5), bold=True, color=COLOR_PURPLE, space_after=Pt(8))

    add_clean_paragraph(tf_C, "Functional Mechanics:", font_size=Pt(9.0), bold=True, color=COLOR_NAVY, space_after=Pt(3))
    add_clean_paragraph(tf_C, "• Spatial Attention Gating:", font_size=Pt(8.2), bold=True, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_C, "  Computes dynamic boundary saliency weights across pixels.", font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(4))
    add_clean_paragraph(tf_C, "• Boundary Feature Recalibration:", font_size=Pt(8.2), bold=True, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_C, "  Features along defect perimeters receive boosted attention.", font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(4))
    add_clean_paragraph(tf_C, "• Background Noise Suppression:", font_size=Pt(8.2), bold=True, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_C, "  Uniform steel areas receive neutral weight (1.0).", font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(4))
    add_clean_paragraph(tf_C, "• Eliminates Border Bleeding:", font_size=Pt(8.2), bold=True, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_C, "  Prevents decoder masks from leaking into surrounding steel.", font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(0))

    add_card(slide, cC_x + Inches(0.15), y_tk, w_card - Inches(0.30), h_tk, bg_color=COLOR_PURPLE_BG, border_color=COLOR_PURPLE, border_width=Pt(1.0))
    tb_tkc = slide.shapes.add_textbox(cC_x + Inches(0.20), y_tk + Inches(0.04), w_card - Inches(0.40), h_tk - Inches(0.08))
    tf_tkc = tb_tkc.text_frame
    add_clean_paragraph(tf_tkc, "Key Takeaway: Uses learned boundary information to guide decoder features for razor-sharp boundaries.", font_size=Pt(7.8), bold=True, color=COLOR_PURPLE, space_after=Pt(0))

    set_speaker_note(slide, """SLIDE 6 — HOW MSFP + BAS + BGFF WORK (60–75 seconds)
Speaker Script:
"Let us now look deeper into the mathematical intuition behind the three key innovations: MSFP, BAS, and BGFF.

First, Section A: Multi-Scale Feature Preservation.
In standard CNNs, expanding the receptive field requires aggressive spatial pooling, which destroys micro-features. In MSFP, we partition channels into parallel branches using dilated depthwise convolutions with rates 1, 2, and 4. Branch 2, with r=1, has a 3x3 receptive field—ideal for localized hairline cracks. Branch 3, with r=2, achieves a 5x5 field for pit depressions. Branch 4, with r=4, spans 9x9 pixels to capture extended patches. We intentionally cap the dilation rate at 4 to prevent gridding artifacts.

Second, Section B: the Boundary-Aware Stream (BAS).
How do we teach the network where boundaries lie? We compute the morphological gradient of the binary ground-truth mask using a 3x3 structuring element: dilation minus erosion. This isolates a sharp, 1-pixel-wide edge contour. The BAS stream is trained with a dedicated boundary cross-entropy loss, compelling the early encoder features to retain high-frequency contour gradients.

Third, Section C: Boundary-Guided Feature Fusion (BGFF).
Knowing where the boundary is not enough; we must inject that knowledge into the decoder. BGFF takes the boundary feature map and the decoder feature map, concatenates them, and applies a 1x1 convolution followed by a sigmoid activation. This yields a spatial attention map, A_spat. We modulate the decoder features through residual attention: F_out = F_dec multiplied by 1 plus A_spat. This selectively amplifies features along uncertain defect boundaries while suppressing noise from uniform steel background.

Together, these three components establish a synergistic loop: MSFP preserves scale diversity, BAS extracts boundaries, and BGFF guides the final segmentation."
""")

# -------------------------------------------------------------
# SLIDE 7: TRAINING & LOSS FUNCTION
# -------------------------------------------------------------
def build_slide_7(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Optimization & Loss Function", "Training Strategy: Region + Boundary Supervision", "A composite objective engineered to combat severe class imbalance and edge ambiguity.")

    start_x = Inches(0.8)

    # 1. Training Flow Diagram (5 horizontal steps)
    steps = [
        ("Input Image", "256x256 Grayscale"),
        ("MSBA-Net", "Dual-Stream Forward"),
        ("Dual Predictions", "P_seg + P_bound"),
        ("Composite Loss", "0.3+0.3+0.2+0.2"),
        ("AdamW Update", "Backprop & Optimize")
    ]
    w_s = Inches(2.15)
    gap_s = Inches(0.24)
    y_s = Inches(1.65)
    h_s = Inches(0.90)

    for i, (title, desc) in enumerate(steps):
        x = start_x + i * (w_s + gap_s)
        bg = COLOR_AMBER_BG if i == 3 else COLOR_CARD_WHITE
        bc = COLOR_AMBER if i == 3 else COLOR_BORDER
        add_card(slide, x, y_s, w_s, h_s, bg_color=bg, border_color=bc, border_width=Pt(1.2))

        tb = slide.shapes.add_textbox(x + Inches(0.10), y_s + Inches(0.12), w_s - Inches(0.20), h_s - Inches(0.24))
        tf = tb.text_frame
        add_clean_paragraph(tf, f"{i+1}. {title}", font_size=Pt(9.5), bold=True, color=COLOR_NAVY, space_after=Pt(2))
        add_clean_paragraph(tf, desc, font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(0))

        if i < 4:
            arr = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x + w_s + Inches(0.04), y_s + Inches(0.30), Inches(0.16), Inches(0.24))
            arr.fill.solid()
            arr.fill.fore_color.rgb = COLOR_MUTED
            arr.line.fill.background()

    # 2. Main Composite Equation Card
    y_eq = Inches(2.72)
    h_eq = Inches(0.95)
    add_card(slide, start_x, y_eq, Inches(11.73), h_eq, bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER, border_width=Pt(1.4))

    tb_eq = slide.shapes.add_textbox(start_x + Inches(0.2), y_eq + Inches(0.12), Inches(11.33), Inches(0.75))
    tf_eq = tb_eq.text_frame
    add_clean_paragraph(tf_eq, "COMPOSITE REGION-EDGE SUPERVISION OBJECTIVE FUNCTION", font_size=Pt(9.5), bold=True, color=COLOR_SLATE, alignment=PP_ALIGN.CENTER, space_after=Pt(3))
    add_clean_paragraph(tf_eq, "L_total  =  0.3 · L_BCE  +  0.3 · L_Dice  +  0.2 · L_Focal  +  0.2 · L_bound", font_name=FONT_HEADING, font_size=Pt(17.5), bold=True, color=COLOR_NAVY, alignment=PP_ALIGN.CENTER, space_after=Pt(0))

    # 3. Four Loss Cards
    y_four = Inches(3.82)
    h_four = Inches(1.90)
    w_four = Inches(2.78)
    gap_four = Inches(0.20)

    loss_cards = [
        ("0.3 · L_BCE", "Binary Cross Entropy", "Pixel Classification", [
            "Evaluates individual pixel log-likelihood.",
            "Provides smooth gradient signal early in training.",
            "Calibrates baseline probabilistic distribution."
        ], COLOR_BLUE, COLOR_BLUE_BG),
        ("0.3 · L_Dice", "Soft Dice Loss", "Region Overlap", [
            "Directly optimizes area intersection over union.",
            "Inherently resilient to class scale differences.",
            "Penalizes global mask mismatch independent of defect size."
        ], COLOR_GREEN, COLOR_GREEN_BG),
        ("0.2 · L_Focal", "Focal Loss (γ=2, α=0.25)", "Hard Mining", [
            "Dynamically down-weights easy background pixels.",
            "Focuses gradients heavily on hard defect samples.",
            "Crucial for tiny hairline cracks (<1% surface area)."
        ], COLOR_AMBER, COLOR_AMBER_BG),
        ("0.2 · L_bound", "Boundary Loss", "Edge Accuracy", [
            "Supervises the Boundary-Aware Stream (BAS).",
            "Calculated against morphological boundary ground truth B_GT.",
            "Enforces razor-sharp contours and stops perimeter leakage."
        ], COLOR_RED, COLOR_RED_BG)
    ]

    for i, (weight, name, role, details, col, col_bg) in enumerate(loss_cards):
        x = start_x + i * (w_four + gap_four)
        add_card(slide, x, y_four, w_four, h_four, bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.2))
        add_pill_badge(slide, x + Inches(0.15), y_four + Inches(0.12), Inches(1.4), Inches(0.26), role.upper(), text_color=col, bg_color=col_bg, border_color=col, font_size=Pt(8.0))

        tb = slide.shapes.add_textbox(x + Inches(0.15), y_four + Inches(0.42), w_four - Inches(0.3), h_four - Inches(0.50))
        tf = tb.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        add_clean_paragraph(tf, weight, font_name=FONT_HEADING, font_size=Pt(13.0), bold=True, color=COLOR_NAVY, space_after=Pt(2))
        add_clean_paragraph(tf, name, font_size=Pt(8.5), bold=True, color=col, space_after=Pt(4))
        for d in details:
            add_clean_paragraph(tf, f"• {d}", font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(2))

    # 4. Bottom Callout: Extreme Imbalance Rationale
    y_call = Inches(5.88)
    add_card(slide, start_x, y_call, Inches(11.73), Inches(0.95), bg_color=COLOR_AMBER_BG, border_color=COLOR_AMBER, border_width=Pt(1.4))

    tb_call = slide.shapes.add_textbox(start_x + Inches(0.2), y_call + Inches(0.10), Inches(11.33), Inches(0.80))
    tf_call = tb_call.text_frame
    add_clean_paragraph(tf_call, "WHY THIS COMPOSITE FORMULATION?  —  MITIGATING SEVERE CLASS IMBALANCE", font_size=Pt(9.5), bold=True, color=COLOR_AMBER, space_after=Pt(3))
    add_clean_paragraph(tf_call, "In industrial steel inspection, >98% of pixels belong to defect-free steel. Using standard Cross-Entropy alone causes the network to collapse into predicting 100% background. By balancing BCE (smooth gradients), Dice (region overlap), Focal Loss (hard-pixel mining), and Boundary Loss (contour sharpness), MSBA-Net forces the gradient to prioritize faint, microscopic anomalies without false alarms.", font_size=Pt(8.5), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    set_speaker_note(slide, """SLIDE 7 — TRAINING & LOSS FUNCTION (60–75 seconds)
Speaker Script:
"Optimization in industrial surface defect segmentation is challenging due to the extreme class imbalance. In our dataset, more than 98% of all pixels are defect-free steel. If you train a standard model using standard cross-entropy loss, the network rapidly discovers a trivial local minimum: predict everything as background, and you instantly achieve 98% accuracy, while completely missing the defects.

To prevent this failure, we formulated a compound region-edge loss function:
L_total equals 0.3 L_BCE plus 0.3 L_Dice plus 0.2 L_Focal plus 0.2 L_bound.

Let us examine each component:
- Binary Cross Entropy provides well-conditioned, stable pixel classification gradients during the early epochs.
- Soft Dice Loss optimizes the intersection-over-union directly, ensuring that small defect regions contribute equally to the gradient regardless of background volume.
- Focal Loss, with gamma=2 and alpha=0.25, dynamically suppresses the gradient from easy, well-classified background pixels, channeling the learning capacity entirely toward hard, ambiguous defect samples.
- Finally, Boundary Loss explicitly penalizes discrepancies between the BAS prediction and the morphological edge ground truth.

Notice the loss weights: 0.3 for BCE, 0.3 for Dice, 0.2 for Focal, and 0.2 for Boundary. This balance guarantees that region detection and edge localization receive equal priority, entirely avoiding gradient vanishing on sub-1% micro-defects."
""")

# -------------------------------------------------------------
# SLIDE 8: DATASET & EXPERIMENTAL SETUP
# -------------------------------------------------------------
def build_slide_8(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Experimental Methodology", "Experimental Setup & NEU Benchmark", "Standardized industrial dataset, defect taxonomy, and modern training configuration.")

    start_x = Inches(0.8)

    # Left Container: Dataset & Defect Categories
    w_left = Inches(6.80)
    add_card(slide, start_x, Inches(1.65), w_left, Inches(5.25), bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.5))
    add_pill_badge(slide, start_x + Inches(0.2), Inches(1.85), Inches(3.2), Inches(0.28), "DATASET: NEU DEFECT DATABASE", text_color=COLOR_BLUE, bg_color=COLOR_BLUE_BG, border_color=COLOR_BLUE, font_size=Pt(8.5))

    tb_ds = slide.shapes.add_textbox(start_x + Inches(0.2), Inches(2.20), w_left - Inches(0.4), Inches(1.2))
    tf_ds = tb_ds.text_frame
    add_clean_paragraph(tf_ds, "1,800 Images  •  256 × 256 Grayscale  •  6 Defect Classes", font_name=FONT_HEADING, font_size=Pt(13.0), bold=True, color=COLOR_NAVY, space_after=Pt(3))
    add_clean_paragraph(tf_ds, "Split Protocol: 70% Train (1,260)  |  15% Val (270)  |  15% Test (270)", font_size=Pt(8.5), bold=False, color=COLOR_SLATE, space_after=Pt(1))
    add_clean_paragraph(tf_ds, "Original resolution 200x200 resized to 256x256. Partitioned with fixed random seeds for strict reproducibility.", font_size=Pt(8.5), bold=False, color=COLOR_SLATE, space_after=Pt(0))

    # 6 Defect Categories (2 rows x 3 cols)
    defects = [
        ("Crazing (Cr)", "Network of micro-cracks", "300 images (50 test)"),
        ("Inclusion (In)", "Non-metallic impurities", "300 images (50 test)"),
        ("Patches (Pa)", "Plate surface peeling", "300 images (50 test)"),
        ("Pitted Surface (PS)", "Dense cavity clusters", "300 images (50 test)"),
        ("Rolled-in Scale (RS)", "Oxide scale pressed in", "300 images (50 test)"),
        ("Scratches (Sc)", "Longitudinal abrasions", "300 images (50 test)")
    ]
    w_sub = Inches(2.05)
    h_sub = Inches(1.30)
    gap_x = Inches(0.12)
    gap_y = Inches(0.15)
    y_start_def = Inches(3.65)

    for i, (name, desc, count) in enumerate(defects):
        row = i // 3
        col = i % 3
        xd = start_x + Inches(0.2) + col * (w_sub + gap_x)
        yd = y_start_def + row * (h_sub + gap_y)
        add_card(slide, xd, yd, w_sub, h_sub, bg_color=COLOR_CARD_ALT, border_color=COLOR_MUTED, border_width=Pt(1.0))

        tb_d = slide.shapes.add_textbox(xd + Inches(0.08), yd + Inches(0.08), w_sub - Inches(0.16), h_sub - Inches(0.16))
        tf_d = tb_d.text_frame
        add_clean_paragraph(tf_d, name, font_size=Pt(9.5), bold=True, color=COLOR_NAVY, space_after=Pt(2))
        add_clean_paragraph(tf_d, desc, font_size=Pt(8.0), bold=True, color=COLOR_AMBER, space_after=Pt(6))
        add_clean_paragraph(tf_d, f"Volume: {count}", font_size=Pt(8.0), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    # Right Container: Training Protocol & Hardware Setup
    x_right = start_x + w_left + Inches(0.28)
    w_right = Inches(4.65)
    add_card(slide, x_right, Inches(1.65), w_right, Inches(5.25), bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.5))
    add_pill_badge(slide, x_right + Inches(0.2), Inches(1.85), Inches(3.2), Inches(0.28), "COMPUTE & HYPERPARAMETERS", text_color=COLOR_GREEN, bg_color=COLOR_GREEN_BG, border_color=COLOR_GREEN, font_size=Pt(8.5))

    tb_hw = slide.shapes.add_textbox(x_right + Inches(0.2), Inches(2.25), w_right - Inches(0.4), Inches(4.50))
    tf_hw = tb_hw.text_frame

    hw_items = [
        ("Framework & Library", "PyTorch 2.1 (CUDA 12.1)"),
        ("Hardware Accelerator", "NVIDIA RTX 4090 GPU (24GB VRAM)"),
        ("Training Epochs", "100 Epochs (Convergence ~75)"),
        ("Batch Size", "16 Images per mini-batch"),
        ("Optimization Algorithm", "AdamW (β1=0.9, β2=0.999, wd=1e-4)"),
        ("Learning Rate Schedule", "Initial 1×10⁻³ with Cosine Annealing (η_min = 1×10⁻⁶)"),
        ("Model Parameters", "9.38 Million Parameters"),
        ("Computational FLOPs", "14.2 GFLOPs (Lightweight Edge Footprint)"),
        ("Inference Speed", "41.1 FPS (PyTorch FP32) / 88.5 FPS (TensorRT)")
    ]

    for title, val in hw_items:
        add_clean_paragraph(tf_hw, title, font_size=Pt(8.5), bold=True, color=COLOR_NAVY, space_after=Pt(1))
        col = COLOR_GREEN if "FPS" in val or "Parameters" in val else COLOR_SLATE
        add_clean_paragraph(tf_hw, val, font_size=Pt(8.0), bold=False, color=col, space_after=Pt(4))

    set_speaker_note(slide, """SLIDE 8 — DATASET & EXPERIMENTAL SETUP (60–75 seconds)
Speaker Script:
"To evaluate our architecture, we benchmarked MSBA-Net on the widely recognized NEU Surface Defect Database developed by Northeastern University.

The dataset contains 1,800 grayscale images spanning six typical steel strip defect categories: crazing, inclusions, patches, pitted surfaces, rolled-in scale, and scratches, with 300 images per category. The original 200 by 200 pixel images are bilinearly interpolated to 256 by 256. We applied a standard 70-15-15 split: 1,260 images for training, 270 for validation, and 270 for unbiased test evaluation.

Looking at the right side of the slide, all experiments were conducted in PyTorch 2.1 on an NVIDIA RTX 4090 GPU with 24 gigabytes of VRAM. Training was run for 100 epochs using the AdamW optimizer with an initial learning rate of 1 times 10 to the minus 3 and cosine annealing decay down to 1 times 10 to the minus 6, with a batch size of 16.

From an engineering perspective, efficiency is just as critical as accuracy. MSBA-Net maintains a compact footprint of only 9.38 million parameters and 14.2 GFLOPs. On our RTX 4090 hardware, it achieves 41.1 frames per second in standard FP32 PyTorch and 88.5 frames per second under TensorRT FP16 quantization—easily surpassing the 30 FPS threshold required for real-time factory line deployment."
""")

# -------------------------------------------------------------
# SLIDE 9: RESULTS & COMPARISON (CLEAN COLUMN CHART & LEGIBLE LABELS)
# -------------------------------------------------------------
def build_slide_9(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Experimental Results", "Performance on the NEU Benchmark", "MSBA-Net outperforms 2024–2026 base models across all segmentation metrics.")

    start_x = Inches(0.8)

    # 1. Three Large Metric Cards (Top)
    w_m = Inches(3.72)
    gap_m = Inches(0.28)
    y_m = Inches(1.65)
    h_m = Inches(1.35)

    metrics = [
        ("97.01%", "OVERALL mIoU", "+2.81% over 2026 DMS-UNet (94.20%)\nState-of-the-art segmentation accuracy", COLOR_GREEN, COLOR_GREEN_BG),
        ("98.48%", "DICE COEFFICIENT", "+1.46% over previous benchmark\nExceptional region overlap & mask continuity", COLOR_BLUE, COLOR_BLUE_BG),
        ("92.48%", "TINY-DEFECT mIoU", "+4.08% improvement on sub-1% area flaws\nDirect proof of micro-feature preservation", COLOR_AMBER, COLOR_AMBER_BG)
    ]

    for i, (val, label, desc, col, col_bg) in enumerate(metrics):
        x = start_x + i * (w_m + gap_m)
        add_card(slide, x, y_m, w_m, h_m, bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.2))
        add_pill_badge(slide, x + Inches(0.15), y_m + Inches(0.12), Inches(1.6), Inches(0.26), label, text_color=col, bg_color=col_bg, border_color=col, font_size=Pt(8.0))

        tb = slide.shapes.add_textbox(x + Inches(0.15), y_m + Inches(0.42), w_m - Inches(0.3), Inches(0.85))
        tf = tb.text_frame
        add_clean_paragraph(tf, val, font_name=FONT_HEADING, font_size=Pt(22), bold=True, color=col, space_after=Pt(2))
        add_clean_paragraph(tf, desc, font_size=Pt(8.5), bold=False, color=COLOR_SLATE, space_after=Pt(0))

    # 2. Native PowerPoint Clustered Column Chart (Bottom Left)
    w_chart = Inches(6.80)
    h_bot = Inches(3.70)
    y_bot = Inches(3.15)
    add_card(slide, start_x, y_bot, w_chart, h_bot, bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.2))

    tb_ct = slide.shapes.add_textbox(start_x + Inches(0.2), y_bot + Inches(0.15), w_chart - Inches(0.4), Inches(0.3))
    tf_ct = tb_ct.text_frame
    add_clean_paragraph(tf_ct, "mIoU (%) COMPARISON ACROSS SOTA BENCHMARKS", font_size=Pt(10.0), bold=True, color=COLOR_NAVY, space_after=Pt(0))

    chart_data = CategoryChartData()
    chart_data.categories = ['GNA-PSC', 'MixSegNet', 'EF²Net', 'DAMF-Net', 'DMS-UNet', 'MSBA-Net']
    chart_data.add_series('mIoU (%)', (83.50, 84.80, 88.42, 91.65, 94.20, 97.01))

    chart_shape = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, start_x + Inches(0.2), y_bot + Inches(0.45), w_chart - Inches(0.4), h_bot - Inches(0.55), chart_data
    )
    chart = chart_shape.chart
    chart.has_legend = False

    plot = chart.plots[0]
    plot.has_data_labels = True
    data_labels = plot.data_labels
    data_labels.font.name = FONT_PRIMARY
    data_labels.font.size = Pt(9.0)
    data_labels.font.bold = True
    data_labels.font.color.rgb = COLOR_NAVY
    data_labels.position = XL_LABEL_POSITION.OUTSIDE_END

    series = plot.series[0]
    for idx, pt in enumerate(series.points):
        pt.format.fill.solid()
        if idx == 5:
            pt.format.fill.fore_color.rgb = COLOR_GREEN
        elif idx == 4:
            pt.format.fill.fore_color.rgb = COLOR_BLUE
        else:
            pt.format.fill.fore_color.rgb = COLOR_MUTED

    # 3. Benchmark Table & Insights (Bottom Right)
    x_tbl = start_x + w_chart + Inches(0.28)
    w_tbl = Inches(4.65)
    add_card(slide, x_tbl, y_bot, w_tbl, h_bot, bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.2))

    tb_tt = slide.shapes.add_textbox(x_tbl + Inches(0.2), y_bot + Inches(0.15), w_tbl - Inches(0.4), Inches(0.3))
    tf_tt = tb_tt.text_frame
    add_clean_paragraph(tf_tt, "BENCHMARK PERFORMANCE COMPARISON", font_size=Pt(10.0), bold=True, color=COLOR_NAVY, space_after=Pt(0))

    rows = 7
    cols = 4
    table_shape = slide.shapes.add_table(rows, cols, x_tbl + Inches(0.2), y_bot + Inches(0.50), w_tbl - Inches(0.4), Inches(1.95))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(1.50)
    tbl.columns[1].width = Inches(0.90)
    tbl.columns[2].width = Inches(0.90)
    tbl.columns[3].width = Inches(0.95)

    headers = ["Model", "mIoU", "Dice", "Tiny mIoU"]
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.name = FONT_PRIMARY
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_CARD_WHITE
        p.alignment = PP_ALIGN.CENTER

    data = [
        ("GNA-PSC (2024)", "83.50%", "88.20%", "72.40%"),
        ("MixSegNet (2024)", "84.80%", "91.50%", "76.10%"),
        ("EF²Net (2024)", "88.42%", "93.85%", "81.25%"),
        ("DAMF-Net (2025)", "91.65%", "95.60%", "85.70%"),
        ("DMS-UNet (2026)", "94.20%", "97.02%", "88.40%"),
        ("MSBA-Net (Ours)", "97.01%", "98.48%", "92.48%")
    ]

    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = tbl.cell(i + 1, j)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_GREEN_BG if i == 5 else (COLOR_CARD_ALT if i % 2 == 1 else COLOR_CARD_WHITE)
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_PRIMARY
            p.font.size = Pt(8.0)
            p.font.bold = (i == 5 or j == 0)
            p.font.color.rgb = COLOR_GREEN if i == 5 else COLOR_NAVY
            if j > 0:
                p.alignment = PP_ALIGN.CENTER

    tb_in = slide.shapes.add_textbox(x_tbl + Inches(0.2), y_bot + Inches(2.55), w_tbl - Inches(0.4), Inches(1.05))
    tf_in = tb_in.text_frame
    add_clean_paragraph(tf_in, "Key Industrial Findings:", font_size=Pt(8.5), bold=True, color=COLOR_NAVY, space_after=Pt(2))
    add_clean_paragraph(tf_in, "• Precision: 97.57%  |  Recall: 99.41%  (Near-zero missed defects)", font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(1))
    add_clean_paragraph(tf_in, "• Highest Class Accuracy: Patches (97.85%) & Inclusions (97.15%)", font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(1))
    add_clean_paragraph(tf_in, "• Tiny Defects (<1% Area): 92.48% (+4.08% over 2026 state-of-the-art)", font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(1))
    add_clean_paragraph(tf_in, "• Tiny defects = morphological regions occupying <1% image area.", font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(0))

    set_speaker_note(slide, """SLIDE 9 — RESULTS & COMPARISON (60–75 seconds)
Speaker Script:
"Now, let us turn to the core quantitative results. How does MSBA-Net perform against the state-of-the-art?

As shown in both the bar chart and the benchmark table, MSBA-Net establishes new state-of-the-art performance across all evaluation metrics on the NEU dataset.
Our model achieves:
- An overall mean Intersection-over-Union (mIoU) of 97.01%, representing a 2.81% improvement over the most recent 2026 base paper, DMS-UNet, which attained 94.20%.
- A Dice Similarity Coefficient of 98.48%, indicating exceptional region overlap and continuous mask coherence.
- And most importantly, a Tiny-Defect mIoU of 92.48%.

Let me highlight why this Tiny-Defect mIoU number is the most crucial result of this entire research. In our paper, we define tiny defects as connected morphological regions occupying less than 1% of the entire image area. While previous models like GNA-PSC and MixSegNet drop down to the 70s on tiny defects, and DMS-UNet reaches 88.40%, MSBA-Net maintains 92.48%—a massive 4.08% improvement.

Furthermore, our model achieves a Precision of 97.57% and a Recall of 99.41%. In industrial steel manufacturing, high Recall is non-negotiable: a missed defect can cause catastrophic failure in an automobile body panel. A recall of 99.41% means that practically no true metallurgical defects escape detection."
""")

# -------------------------------------------------------------
# SLIDE 10: ABLATION + QUALITATIVE RESULTS
# -------------------------------------------------------------
def build_slide_10(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Validation & Analysis", "Why Does MSBA-Net Work?", "Component-wise ablation study and qualitative visual evidence from the research paper.")

    start_x = Inches(0.8)

    # LEFT HALF: Ablation Analysis (Width: 5.6")
    w_left = Inches(5.60)
    add_card(slide, start_x, Inches(1.65), w_left, Inches(5.25), bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.5))
    add_pill_badge(slide, start_x + Inches(0.2), Inches(1.85), Inches(2.8), Inches(0.28), "COMPONENT ABLATION STUDY", text_color=COLOR_AMBER, bg_color=COLOR_AMBER_BG, border_color=COLOR_AMBER, font_size=Pt(8.5))

    tb_at = slide.shapes.add_textbox(start_x + Inches(0.2), Inches(2.22), w_left - Inches(0.4), Inches(0.28))
    tf_at = tb_at.text_frame
    add_clean_paragraph(tf_at, "INCREMENTAL COMPONENT CONTRIBUTIONS", font_size=Pt(9.5), bold=True, color=COLOR_NAVY, space_after=Pt(0))

    rows = 5
    cols = 5
    table_shape = slide.shapes.add_table(rows, cols, start_x + Inches(0.2), Inches(2.55), w_left - Inches(0.4), Inches(1.70))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.10)
    tbl.columns[1].width = Inches(0.75)
    tbl.columns[2].width = Inches(0.75)
    tbl.columns[3].width = Inches(0.80)
    tbl.columns[4].width = Inches(0.80)

    headers = ["Configuration", "mIoU", "Dice", "Tiny mIoU", "Params"]
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.name = FONT_PRIMARY
        p.font.size = Pt(8.0)
        p.font.bold = True
        p.font.color.rgb = COLOR_CARD_WHITE
        p.alignment = PP_ALIGN.CENTER

    ablation_data = [
        ("Baseline Backbone", "94.10%", "96.90%", "84.60%", "7.76M"),
        ("+ MSFP Blocks", "95.85%", "97.88%", "89.65%", "8.42M"),
        ("+ BAS Boundary Stream", "96.48%", "98.21%", "91.20%", "9.15M"),
        ("+ BGFF Gate (Full MSBA)", "97.01%", "98.48%", "92.48%", "9.38M")
    ]

    for i, row in enumerate(ablation_data):
        for j, val in enumerate(row):
            cell = tbl.cell(i + 1, j)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_GREEN_BG if i == 3 else (COLOR_CARD_ALT if i % 2 == 1 else COLOR_CARD_WHITE)
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_PRIMARY
            p.font.size = Pt(8.0)
            p.font.bold = (i == 3 or j == 0)
            p.font.color.rgb = COLOR_GREEN if i == 3 else COLOR_NAVY
            if j > 0:
                p.alignment = PP_ALIGN.CENTER

    # Ablation Insights
    tb_ai = slide.shapes.add_textbox(start_x + Inches(0.2), Inches(4.38), w_left - Inches(0.4), Inches(2.40))
    tf_ai = tb_ai.text_frame
    tf_ai.margin_left = tf_ai.margin_top = tf_ai.margin_right = tf_ai.margin_bottom = 0

    add_clean_paragraph(tf_ai, "Key Ablation Takeaways:", font_size=Pt(9.5), bold=True, color=COLOR_NAVY, space_after=Pt(3))
    add_clean_paragraph(tf_ai, "1. MSFP Drives Micro-Defect Recovery (+5.05% Tiny mIoU):", font_size=Pt(8.5), bold=True, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_ai, "Integrating MSFP blocks provides the single largest jump for tiny defects (84.60% → 89.65%), proving parallel dilated kernels prevent hairline cracks from vanishing.", font_size=Pt(8.2), bold=False, color=COLOR_SLATE, space_after=Pt(6))
    add_clean_paragraph(tf_ai, "2. BAS + BGFF Synergy Eliminates Boundary Bleeding:", font_size=Pt(8.5), bold=True, color=COLOR_NAVY_LIGHT, space_after=Pt(1))
    add_clean_paragraph(tf_ai, "Adding explicit boundary supervision (+0.63% mIoU) and attention gating (+0.53% mIoU) drives Tiny mIoU past 92%, confirming boundary confidence sharpens edge delineation.", font_size=Pt(8.2), bold=False, color=COLOR_SLATE, space_after=Pt(0))

    # RIGHT HALF: Qualitative Results (Width: 5.85")
    x_right = start_x + w_left + Inches(0.28)
    w_right = Inches(5.85)
    add_card(slide, x_right, Inches(1.65), w_right, Inches(5.25), bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.5))
    add_pill_badge(slide, x_right + Inches(0.2), Inches(1.85), Inches(3.2), Inches(0.28), "QUALITATIVE VISUAL PROGRESSION", text_color=COLOR_GREEN, bg_color=COLOR_GREEN_BG, border_color=COLOR_GREEN, font_size=Pt(8.5))

    if os.path.exists(SLIDE10_QUAL_PATH):
        slide.shapes.add_picture(SLIDE10_QUAL_PATH, x_right + Inches(0.15), Inches(2.25), w_right - Inches(0.3), Inches(3.75))

    tb_qc = slide.shapes.add_textbox(x_right + Inches(0.2), Inches(6.10), w_right - Inches(0.4), Inches(0.65))
    tf_qc = tb_qc.text_frame
    add_clean_paragraph(tf_qc, "Takeaway: MSFP preserves fine structures; BAS + BGFF improve boundary localization. Baseline suffers from fragmented cracks and edge leaks; MSBA-Net matches ground truth continuously.", font_size=Pt(8.0), bold=True, color=COLOR_GREEN, space_after=Pt(0))

    set_speaker_note(slide, """SLIDE 10 — ABLATION + QUALITATIVE RESULTS (60–75 seconds)
Speaker Script:
"Why does MSBA-Net work so effectively? On this slide, we provide both rigorous ablation evidence and qualitative visual proof.

Looking at the ablation table on the left:
Starting from our Baseline Backbone without MSFP or BAS, the model achieves 94.10% mIoU, but only 84.60% on tiny defects.
When we insert our Multi-Scale Feature Preservation (MSFP) blocks, overall mIoU climbs by 1.75% to 95.85%, but tiny-defect mIoU surges by an astonishing 5.05% to 89.65%. This confirms our fundamental thesis: parallel dilated depthwise convolutions effectively rescue micro-scale features from disappearing.

Next, when we introduce the Boundary-Aware Stream (BAS), mIoU rises further to 96.48%, and tiny mIoU reaches 91.20%.
Finally, adding the BGFF spatial attention gate completes MSBA-Net, achieving our peak 97.01% mIoU and 92.48% tiny-defect mIoU, with only a modest 1.62M parameter increase over baseline.

Now, examine the qualitative visual comparisons on the right, directly from Figure 2 of our paper across four defect classes: crazing, inclusion, patches, and pitted surfaces:
- In row 1, crazing: the baseline U-Net produces a fragmented, incomplete mask with an IoU of 82.9%. In contrast, MSBA-Net traces the exact defect contour, achieving 86.7% and continuous coverage.
- In row 2, thin inclusions: the baseline exhibits noticeable edge bleeding into the background steel, whereas MSBA-Net adheres tightly to the true morphological boundary.
- For patches and pitted surfaces, MSBA-Net achieves 100% IoU match with ground truth.

This visual progression clearly demonstrates that MSFP protects fine structural details, while BAS and BGFF ensure sharp, leak-free boundary localization."
""")

# -------------------------------------------------------------
# SLIDE 11: ROBUSTNESS, CONCLUSION & FUTURE WORK
# -------------------------------------------------------------
def build_slide_11(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, "Summary & Future Outlook", "Conclusion & Future Directions", "Key findings, factory stress-test limitations, and industrial deployment roadmap.")

    start_x = Inches(0.8)

    # 1. Top Section: Three Key Findings Cards
    w_k = Inches(3.72)
    gap_k = Inches(0.28)
    y_k = Inches(1.65)
    h_k = Inches(1.25)

    findings = [
        ("1. HIGH ACCURACY", "97.01% mIoU  |  98.48% Dice", "SOTA defect segmentation accuracy on NEU benchmark, outperforming all 2024–2026 base models.", COLOR_GREEN, COLOR_GREEN_BG),
        ("2. MICRO-PRESERVATION", "92.48% Tiny-Defect mIoU", "Exceptional localization of flaws occupying <1% area, closing the industrial safety gap.", COLOR_BLUE, COLOR_BLUE_BG),
        ("3. REAL-TIME POTENTIAL", "41.1 FPS (FP32) | 88.5 FPS (FP16)", "Sub-25 ms latency on RTX 4090, comfortably exceeding real-time 30 FPS factory requirements.", COLOR_AMBER, COLOR_AMBER_BG)
    ]

    for i, (title, num, desc, col, col_bg) in enumerate(findings):
        x = start_x + i * (w_k + gap_k)
        add_card(slide, x, y_k, w_k, h_k, bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.2))
        add_pill_badge(slide, x + Inches(0.15), y_k + Inches(0.10), Inches(2.0), Inches(0.24), title, text_color=col, bg_color=col_bg, border_color=col, font_size=Pt(8.0))

        tb = slide.shapes.add_textbox(x + Inches(0.15), y_k + Inches(0.38), w_k - Inches(0.3), Inches(0.78))
        tf = tb.text_frame
        add_clean_paragraph(tf, num, font_name=FONT_HEADING, font_size=Pt(13.0), bold=True, color=COLOR_NAVY, space_after=Pt(2))
        add_clean_paragraph(tf, desc, font_size=Pt(8.0), bold=False, color=COLOR_SLATE, space_after=Pt(0))

    # 2. Middle Section: Robustness & Degradation Stress-Test
    y_r = Inches(3.02)
    h_r = Inches(1.70)
    add_card(slide, start_x, y_r, Inches(11.73), h_r, bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.4))

    tb_rt = slide.shapes.add_textbox(start_x + Inches(0.2), y_r + Inches(0.12), Inches(11.3), Inches(0.28))
    tf_rt = tb_rt.text_frame
    add_clean_paragraph(tf_rt, "SIMULATED SHOP-FLOOR DEGRADATION STRESS-TEST (HONEST LIMITATION REPORTING)", font_size=Pt(9.5), bold=True, color=COLOR_RED, space_after=Pt(0))

    rob_items = [
        ("Low Contrast (γ = 1.8)", "39.67% mIoU", "Moderate Degradation", "Simulates diffuse lighting shifts or vapor fog. MSBA-Net maintains reasonable defect localization.", COLOR_AMBER, COLOR_AMBER_BG),
        ("Defocus Blur (σ = 3.0)", "26.29% mIoU", "Severe Blur", "Simulates mechanical strip vibration and flutter. High-frequency boundary cues are partially attenuated.", COLOR_AMBER, COLOR_AMBER_BG),
        ("Gaussian Noise (σ = 25)", "2.33% mIoU", "Complete Breakdown", "High-ISO thermal sensor noise annihilates the 1–2 pixel intensity gradients required by boundary convolution.", COLOR_RED, COLOR_RED_BG)
    ]
    w_ri = Inches(3.60)
    gap_ri = Inches(0.24)
    y_ri = y_r + Inches(0.45)
    h_ri = Inches(1.10)

    for i, (title, num, status, desc, col, col_bg) in enumerate(rob_items):
        xi = start_x + Inches(0.2) + i * (w_ri + gap_ri)
        add_card(slide, xi, y_ri, w_ri, h_ri, bg_color=col_bg, border_color=col, border_width=Pt(1.2))

        tb_ri = slide.shapes.add_textbox(xi + Inches(0.08), y_ri + Inches(0.08), w_ri - Inches(0.16), h_ri - Inches(0.16))
        tf_ri = tb_ri.text_frame
        add_clean_paragraph(tf_ri, f"{title}:  {num}", font_size=Pt(10.0), bold=True, color=col, space_after=Pt(2))
        add_clean_paragraph(tf_ri, f"Status: {status}", font_size=Pt(8.0), bold=True, color=COLOR_NAVY, space_after=Pt(2))
        add_clean_paragraph(tf_ri, desc, font_size=Pt(7.8), bold=False, color=COLOR_NAVY_LIGHT, space_after=Pt(0))

    # 3. Bottom Section: Future Work (3-Step Horizontal Flow)
    y_fw = Inches(4.85)
    h_fw = Inches(1.25)
    add_card(slide, start_x, y_fw, Inches(11.73), h_fw, bg_color=COLOR_CARD_ALT, border_color=COLOR_BORDER, border_width=Pt(1.4))

    tb_fwt = slide.shapes.add_textbox(start_x + Inches(0.2), y_fw + Inches(0.10), Inches(11.3), Inches(0.25))
    tf_fwt = tb_fwt.text_frame
    add_clean_paragraph(tf_fwt, "FUTURE RESEARCH ROADMAP (3-PHASE EXTENSION)", font_size=Pt(9.5), bold=True, color=COLOR_NAVY, space_after=Pt(0))

    fw_steps = [
        ("1. Temporal Line-Scan Attention", "Extend 2D spatial segmentation to spatio-temporal video streams across moving strip coils."),
        ("2. Self-Supervised Pre-Training", "Pre-train on massive unlabeled industrial steel imagery via masked autoencoders (MAE)."),
        ("3. 8-Bit Edge Quantization", "Deploy INT8 quantized weights on embedded edge controllers (NVIDIA Jetson / FPGA boards).")
    ]
    w_fws = Inches(3.50)
    gap_fws = Inches(0.35)
    y_fws = y_fw + Inches(0.38)
    h_fws = Inches(0.75)

    for i, (f_title, f_desc) in enumerate(fw_steps):
        xf = start_x + Inches(0.2) + i * (w_fws + gap_fws)
        add_card(slide, xf, y_fws, w_fws, h_fws, bg_color=COLOR_CARD_WHITE, border_color=COLOR_BORDER, border_width=Pt(1.0))

        tb_f = slide.shapes.add_textbox(xf + Inches(0.08), y_fws + Inches(0.06), w_fws - Inches(0.16), h_fws - Inches(0.12))
        tf_f = tb_f.text_frame
        add_clean_paragraph(tf_f, f_title, font_size=Pt(9.0), bold=True, color=COLOR_BLUE, space_after=Pt(2))
        add_clean_paragraph(tf_f, f_desc, font_size=Pt(7.5), bold=False, color=COLOR_SLATE, space_after=Pt(0))

        if i < 2:
            arr = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, xf + w_fws + Inches(0.08), y_fws + Inches(0.25), Inches(0.18), Inches(0.22))
            arr.fill.solid()
            arr.fill.fore_color.rgb = COLOR_BLUE
            arr.line.fill.background()

    # 4. Sign-Off Banner
    y_end = Inches(6.22)
    h_end = Inches(0.65)
    add_card(slide, start_x, y_end, Inches(11.73), h_end, bg_color=COLOR_GREEN_BG, border_color=COLOR_GREEN, border_width=Pt(1.4))
    tb_end = slide.shapes.add_textbox(start_x + Inches(0.2), y_end + Inches(0.12), Inches(11.33), Inches(0.40))
    tf_end = tb_end.text_frame
    add_clean_paragraph(tf_end, "Thank You for Your Time & Attention!  —  Questions & Discussion Welcome", font_name=FONT_HEADING, font_size=Pt(12.0), bold=True, color=COLOR_GREEN, alignment=PP_ALIGN.CENTER, space_after=Pt(0))

    set_speaker_note(slide, """SLIDE 11 — ROBUSTNESS, CONCLUSION & FUTURE WORK (60–75 seconds)
Speaker Script:
"In conclusion, let us summarize the key achievements, discuss real-world factory limitations honestly, and look at the path ahead.

Our key findings are threefold:
First, MSBA-Net establishes a new benchmark on the NEU steel surface defect database, achieving 97.01% mIoU and 98.48% Dice.
Second, it solves the micro-defect dilemma, delivering 92.48% mIoU on flaws occupying less than 1% area.
Third, it demonstrates real-time inference capability, clocking 41.1 FPS in PyTorch FP32 and 88.5 FPS under TensorRT FP16 on an NVIDIA RTX 4090.

However, as researchers, we must be completely transparent about physical operational boundaries. In Section V of our paper, we subjected MSBA-Net to simulated factory degradations:
- Under low contrast (gamma=1.8), the model retains 39.67% mIoU.
- Under defocus blur (sigma=3.0), it retains 26.29% mIoU.
- However, under severe Gaussian sensor noise (sigma=25), performance drops precipitously to 2.33% mIoU.
This collapse is not a flaw in the network architecture; it is an information-theoretic limitation: high-frequency random thermal noise completely obliterates the subtle 1-to-2 pixel intensity gradients required for boundary convolution. This yields a critical engineering lesson: deploying AI models on hot rolling lines requires active LED shrouding, sealed camera housings, and low-noise sensors.

Looking to the future, our roadmap focuses on three directions:
1. Incorporating temporal attention across continuous line-scan video frames.
2. Self-supervised pre-training on massive uncurated steel coils via masked autoencoders.
3. 8-bit edge quantization for direct deployment on embedded industrial controllers.

Thank you very much for your time and kind attention. I will now be delighted to answer any questions from the committee."
""")

# -------------------------------------------------------------
# MAIN PIPELINE
# -------------------------------------------------------------
def main():
    prs = pptx.Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    print("Building Slide 1: Title...")
    build_slide_1(prs)
    print("Building Slide 2: Motivation & Problem...")
    build_slide_2(prs)
    print("Building Slide 3: Challenges & Research Gap...")
    build_slide_3(prs)
    print("Building Slide 4: Proposed Solution...")
    build_slide_4(prs)
    print("Building Slide 5: MSBA-Net Architecture...")
    build_slide_5(prs)
    print("Building Slide 6: Key Components (MSFP, BAS, BGFF)...")
    build_slide_6(prs)
    print("Building Slide 7: Training & Loss Function...")
    build_slide_7(prs)
    print("Building Slide 8: Dataset & Experimental Setup...")
    build_slide_8(prs)
    print("Building Slide 9: Results & Benchmark Comparison...")
    build_slide_9(prs)
    print("Building Slide 10: Ablation & Qualitative Progression...")
    build_slide_10(prs)
    print("Building Slide 11: Robustness, Conclusion & Future Work...")
    build_slide_11(prs)

    output_filename = "MSBA-Net_Amen_Parmar_Presentation.pptx"
    prs.save(output_filename)
    print(f"SUCCESS: Generated {output_filename} with {len(prs.slides)} slides!")

if __name__ == "__main__":
    main()
