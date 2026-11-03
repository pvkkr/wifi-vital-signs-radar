"""
WiFi Vital Signs Radar - Presentation Generator (.pptx)
Generates a 13-slide academic & viva defense presentation using python-pptx.
Authors: P. Venkata Kishor Kumar Reddy, K. Kamalesh, T. Perumal
Affiliation: Koneru Lakshmaiah Education Foundation (KL University)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette Constants
    BG_DARK = RGBColor(15, 23, 42)       # Slate 900
    BG_LIGHT = RGBColor(248, 250, 252)   # Slate 50
    CARD_BG = RGBColor(255, 255, 255)    # White
    CARD_BORDER = RGBColor(226, 232, 240)# Slate 200
    
    PRIMARY_BLUE = RGBColor(2, 132, 199) # Sky 600
    ACCENT_TEAL = RGBColor(13, 148, 136) # Teal 600
    TEXT_DARK = RGBColor(15, 23, 42)     # Slate 900
    TEXT_MUTED = RGBColor(100, 116, 139) # Slate 500
    TEXT_LIGHT = RGBColor(241, 245, 249) # Slate 100
    CORAL_RED = RGBColor(225, 29, 72)    # Rose 600

    def add_header(slide, title_text, category_text="WIFI VITAL SIGNS RADAR"):
        """Adds a standardized top banner to a content slide."""
        # Top banner background
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = BG_DARK
        top_bar.line.fill.background()

        # Category / Department Tag
        tf_cat = top_bar.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = Inches(0.8)
        tf_cat.margin_top = Inches(0.18)
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Arial"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = PRIMARY_BLUE

        # Title
        p_title = tf_cat.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Arial"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT

        # Bottom accent strip
        accent_strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
        accent_strip.fill.solid()
        accent_strip.fill.fore_color.rgb = PRIMARY_BLUE
        accent_strip.line.fill.background()

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        """Adds a card container with rounded corners."""
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.fill.background()
        return card

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = BG_DARK
    bg1.line.fill.background()

    # Accent decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.15), Inches(4.8))
    bar.fill.solid()
    bar.fill.fore_color.rgb = PRIMARY_BLUE
    bar.line.fill.background()

    # Title box
    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(11.0), Inches(2.6))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = "RESEARCH CAPSTONE & VIVA DEFENSE 2026"
    p0.font.name = "Arial"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = PRIMARY_BLUE

    p1 = tf.add_paragraph()
    p1.text = "Contactless WiFi Vital Signs Radar"
    p1.font.name = "Arial"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT

    p2 = tf.add_paragraph()
    p2.text = "Non-Invasive Heartbeat and Respiration Monitoring Using 2.4 GHz Channel State Information (CSI) with NodeMCU & ESP32"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(148, 163, 184)

    # Team Card
    tcard = add_card(s1, Inches(1.2), Inches(4.1), Inches(6.8), Inches(2.2), bg_color=RGBColor(30, 41, 59), border_color=PRIMARY_BLUE)
    ttf = tcard.text_frame
    ttf.margin_left = Inches(0.3)
    ttf.margin_top = Inches(0.2)
    
    tp0 = ttf.paragraphs[0]
    tp0.text = "PROJECT INVESTIGATORS & AUTHORS"
    tp0.font.name = "Arial"
    tp0.font.size = Pt(11)
    tp0.font.bold = True
    tp0.font.color.rgb = PRIMARY_BLUE

    tp1 = ttf.add_paragraph()
    tp1.text = "• P. Venkata Kishor Kumar Reddy (Lead Project Investigator)"
    tp1.font.name = "Segoe UI"
    tp1.font.size = Pt(13)
    tp1.font.bold = True
    tp1.font.color.rgb = TEXT_LIGHT

    tp2 = ttf.add_paragraph()
    tp2.text = "• K. Kamalesh (Co-Investigator - Firmware & Hardware)"
    tp2.font.name = "Segoe UI"
    tp2.font.size = Pt(13)
    tp2.font.color.rgb = RGBColor(226, 232, 240)

    tp3 = ttf.add_paragraph()
    tp3.text = "• T. Perumal (Co-Investigator - Experimental Validation)"
    tp3.font.name = "Segoe UI"
    tp3.font.size = Pt(13)
    tp3.font.color.rgb = RGBColor(226, 232, 240)

    # Institution Card
    icard = add_card(s1, Inches(8.3), Inches(4.1), Inches(4.2), Inches(2.2), bg_color=RGBColor(30, 41, 59), border_color=CARD_BORDER)
    itf = icard.text_frame
    itf.margin_left = Inches(0.3)
    itf.margin_top = Inches(0.2)

    ip0 = itf.paragraphs[0]
    ip0.text = "ACADEMIC AFFILIATION"
    ip0.font.name = "Arial"
    ip0.font.size = Pt(11)
    ip0.font.bold = True
    ip0.font.color.rgb = ACCENT_TEAL

    ip1 = itf.add_paragraph()
    ip1.text = "Koneru Lakshmaiah Education Foundation"
    ip1.font.name = "Segoe UI"
    ip1.font.size = Pt(13)
    ip1.font.bold = True
    ip1.font.color.rgb = TEXT_LIGHT

    ip2 = itf.add_paragraph()
    ip2.text = "(KL University), Vaddeswaram, A.P., India"
    ip2.font.name = "Segoe UI"
    ip2.font.size = Pt(12)
    ip2.font.color.rgb = RGBColor(148, 163, 184)

    ip3 = itf.add_paragraph()
    ip3.text = "Dept. of ECE & CSE | IEEE 802.11n Bio-Radar"
    ip3.font.name = "Segoe UI"
    ip3.font.size = Pt(11)
    ip3.font.color.rgb = PRIMARY_BLUE

    # =========================================================================
    # SLIDE 2: Problem Statement & Motivation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Motivation & Problem Statement: The Clinical Need")

    # Card 1: Traditional Contact Sensors
    c1 = add_card(s2, Inches(0.8), Inches(1.5), Inches(3.6), Inches(5.4))
    ctf1 = c1.text_frame
    ctf1.margin_left = Inches(0.3)
    ctf1.margin_top = Inches(0.3)
    p = ctf1.paragraphs[0]
    p.text = "1. ECG Electrodes & Gels"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CORAL_RED

    bullets1 = [
        "Adhesive gel patches cause allergic contact dermatitis and skin tears over long monitoring sessions.",
        "Cables restrict patient movement in ICU and hospital beds.",
        "Impractical for continuous daily home healthcare or elderly tracking."
    ]
    for b in bullets1:
        p = ctf1.add_paragraph()
        p.text = "• " + b
        p.font.name = "Segoe UI"
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(12)

    # Card 2: PPG Finger Clips & Wearables
    c2 = add_card(s2, Inches(4.8), Inches(1.5), Inches(3.6), Inches(5.4))
    ctf2 = c2.text_frame
    ctf2.margin_left = Inches(0.3)
    ctf2.margin_top = Inches(0.3)
    p = ctf2.paragraphs[0]
    p.text = "2. PPG Clips & Wearables"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE

    bullets2 = [
        "Fingertip pulse clips clamp tightly, causing numbness and detachment during natural sleep turning.",
        "Smartwatches require daily battery charging and tight skin adherence.",
        "Sleep apnea and nighttime vitals are frequently lost due to loose sensors."
    ]
    for b in bullets2:
        p = ctf2.add_paragraph()
        p.text = "• " + b
        p.font.name = "Segoe UI"
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(12)

    # Card 3: The WiFi CSI Vision
    c3 = add_card(s2, Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.4), bg_color=RGBColor(240, 253, 250), border_color=ACCENT_TEAL)
    ctf3 = c3.text_frame
    ctf3.margin_left = Inches(0.3)
    ctf3.margin_top = Inches(0.3)
    p = ctf3.paragraphs[0]
    p.text = "3. Our WiFi CSI Solution"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_TEAL

    bullets3 = [
        "100% Contactless & Passive: Zero electrodes, zero finger clips, zero wearables on the subject.",
        "Everyday Ubiquitous Radio: Uses standard 2.4 GHz WiFi electromagnetic carrier waves (IEEE 802.11n).",
        "Sub-Millimeter Sensitivity: Detects 0.2 mm chest wall pulsations through air reflections.",
        "Ultra Low Cost (< $10): Implemented on commodity NodeMCU and ESP32 microcontrollers."
    ]
    for b in bullets3:
        p = ctf3.add_paragraph()
        p.text = "✔ " + b
        p.font.name = "Segoe UI"
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(12)

    # =========================================================================
    # SLIDE 3: RSSI vs CSI (The Core Breakthrough)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Core Breakthrough: Why RSSI Fails & Why CSI Succeeds")

    # Explanatory Callout
    callout = add_card(s3, Inches(0.8), Inches(1.4), Inches(11.7), Inches(1.1), bg_color=RGBColor(238, 242, 255), border_color=PRIMARY_BLUE)
    ctf = callout.text_frame
    ctf.margin_left = Inches(0.3)
    ctf.margin_top = Inches(0.15)
    cp0 = ctf.paragraphs[0]
    cp0.text = "PHYSICAL RADIO INSIGHT: RSSI is a single scalar number; CSI is a multi-dimensional holographic matrix."
    cp0.font.bold = True
    cp0.font.size = Pt(12)
    cp0.font.color.rgb = PRIMARY_BLUE
    cp1 = ctf.add_paragraph()
    cp1.text = "RSSI is like looking into a dark room through sunglasses: you only see general brightness. CSI provides 56 distinct narrow laser beams across the 20 MHz spectrum, allowing sub-millimeter chest displacement extraction."
    cp1.font.size = Pt(11.5)
    cp1.font.color.rgb = TEXT_DARK

    # Table
    rows = 6
    cols = 3
    table_shape = s3.shapes.add_table(rows, cols, Inches(0.8), Inches(2.7), Inches(11.7), Inches(4.2))
    table = table_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(4.2)
    table.columns[2].width = Inches(4.3)

    headers = ["Feature / Metric", "Standard WiFi RSSI (Coarse)", "Channel State Information - CSI (Our Radar)"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = BG_DARK
        cell.text_frame.margin_left = Inches(0.15)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_LIGHT

    data = [
        ("Information Nature", "1 single average integer (e.g. -75 dBm)", "Complex matrix H(f,t) = |H|·exp(j∠H) with amplitude & phase"),
        ("Subcarrier Diversity", "1 value for entire 20 MHz band", "56 distinct orthogonal OFDM subcarriers (16 selected)"),
        ("Physical Sensitivity", "Gross body motion only (> 10 cm)", "Micro-mechanical chest displacement (0.2 mm to 0.5 mm)"),
        ("Multipath Impact", "Multipath destructively ruins signal", "Exploits multipath diversity to isolate optimal subcarrier"),
        ("Measurement Accuracy", "Unusable for vitals (severe drift)", "Clinical-grade vital sign extraction (±1 BPM agreement)")
    ]

    for i, row_data in enumerate(data):
        for j, val in enumerate(row_data):
            cell = table.cell(i+1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if i % 2 == 0 else RGBColor(248, 250, 252)
            cell.text_frame.margin_left = Inches(0.15)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Segoe UI"
            p.font.size = Pt(11.5)
            p.font.color.rgb = TEXT_DARK
            if j == 2:
                p.font.bold = True
                p.font.color.rgb = PRIMARY_BLUE

    # =========================================================================
    # SLIDE 4: Theoretical Physics & Mathematical Foundations
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Physics & Math: Carrier Wavelength & Micro-Phase Modulation")

    # Column 1: RF Carrier & Wavelength
    c_left = add_card(s4, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    ltf = c_left.text_frame
    ltf.margin_left = Inches(0.3)
    ltf.margin_top = Inches(0.3)
    
    p = ltf.paragraphs[0]
    p.text = "1. Carrier Frequency & Wavelength"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE

    math_bullets1 = [
        "Operating Band: 2.4 GHz ISM Band (Channel 11)",
        "Center Frequency (fc): 2.462 GHz (2,462,000,000 Hz)",
        "Speed of Light (c): 3.0 × 10^8 m/s",
        "Wavelength (λ) = c / fc ≈ 0.1218 m = 12.18 cm",
        "Physical Significance: Because λ is 12.18 cm, a fraction-of-a-millimeter chest movement creates a measurable RF phase shift!"
    ]
    for b in math_bullets1:
        p = ltf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.space_after = Pt(8)

    # Column 2: Round-Trip Phase Shift Equation
    c_right = add_card(s4, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), bg_color=RGBColor(248, 250, 252), border_color=PRIMARY_BLUE)
    rtf = c_right.text_frame
    rtf.margin_left = Inches(0.3)
    rtf.margin_top = Inches(0.3)

    p = rtf.paragraphs[0]
    p.text = "2. Round-Trip Phase Modulation Model"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CORAL_RED

    math_bullets2 = [
        "Round-Trip Path Change: Δd_roundtrip = 2 · Δd(t)",
        "Fundamental Phase Formula: Δϕ(t) = (4π · Δd(t)) / λ",
        "---",
        "A) Respiration Cycle (Breathing):",
        "   • Thoracic cavity displacement: Δd ≈ 5.0 to 12.0 mm",
        "   • Induced Phase Shift: Δϕ_resp ≈ 35.5° to 70° (Macro-wave)",
        "   • Frequency Range: 0.10 Hz – 0.45 Hz (6 – 27 breaths/min)",
        "---",
        "B) Cardiac Ballistocardiogram (Heartbeat):",
        "   • Ventricular contraction micro-displacement: Δd ≈ 0.2 to 0.5 mm",
        "   • Induced Phase Shift: Δϕ_cardiac ≈ 1.2° to 3.5° (Micro-pulse)",
        "   • Frequency Range: 0.80 Hz – 2.00 Hz (48 – 120 beats/min)"
    ]
    for b in math_bullets2:
        p = rtf.add_paragraph()
        p.text = b
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK if not b.startswith("---") else TEXT_MUTED
        if "Phase Formula" in b:
            p.font.bold = True
            p.font.size = Pt(13)
            p.font.color.rgb = CORAL_RED

    # =========================================================================
    # SLIDE 5: First Fresnel Zone (FFZ) Geometry
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Fresnel Zone Geometry: Optimal Desk Placement")

    # Math Card
    f_card = add_card(s5, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    ftf = f_card.text_frame
    ftf.margin_left = Inches(0.3)
    ftf.margin_top = Inches(0.3)
    p = ftf.paragraphs[0]
    p.text = "First Fresnel Zone (FFZ) Equation"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = PRIMARY_BLUE

    f_bullets = [
        "First Fresnel Radius Formula:",
        "   r1 = sqrt( (λ · d1 · d2) / (d1 + d2) )",
        "For Transmitter-Receiver Separation D = 1.0 m:",
        "   d1 = 0.5 m, d2 = 0.5 m, λ = 0.1218 m",
        "   r1 = sqrt( (0.1218 × 0.25) / 1.0 ) ≈ 0.174 m = 17.4 cm",
        "---",
        "Key Deployment Rule:",
        "• Placing the human chest at 30 to 50 cm perpendicular to the line-of-sight positions the anterior thoracic wall right on the First Fresnel boundary.",
        "• At this boundary, microscopic chest motion produces the largest constructive and destructive amplitude fluctuations in the receiver CSI matrix!"
    ]
    for b in f_bullets:
        p = ftf.add_paragraph()
        p.text = b
        p.font.size = Pt(11.5)
        p.space_after = Pt(6)

    # Geometry Diagram Card
    d_card = add_card(s5, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), bg_color=BG_DARK, border_color=PRIMARY_BLUE)
    dtf = d_card.text_frame
    dtf.margin_left = Inches(0.3)
    dtf.margin_top = Inches(0.3)
    p = dtf.paragraphs[0]
    p.text = "PHYSICAL RADAR DESK GEOMETRY"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = PRIMARY_BLUE

    diagram_text = """
       [ NodeMCU TX ]                             [ ESP32 RX ]
       (Power Bank)                              (Plugged into PC)
           [■]                                         [■]
            |                                           |
            | <───────────── 80 cm to 1.0 m ──────────> |
            \\                                           /
             \\                                         /
              \\             (  SUBJECT SEATED  )      /
               \\            ( Chest Level 1.0m )      /
                \\           ( Hands Resting    )     /
                 \\                  |                /
                  ------------------+-----------------
                               30 to 50 cm
    """
    p = dtf.add_paragraph()
    p.text = diagram_text
    p.font.name = "Consolas"
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(148, 163, 184)

    p = dtf.add_paragraph()
    p.text = "✔ Direct line-of-sight unobstructed.\n✔ Person breathes naturally without touching any equipment.\n✔ Real-time telemetry streams over USB UART at 115200 baud."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 6: System Architecture & Flowchart
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "End-to-End System Architecture & Data Flow")

    steps = [
        ("1. Transmitter Node", "NodeMCU (ESP8266)\n• 80 Hz Broadcast Beacons\n• Channel 11 (2.462 GHz)\n• +20.5 dBm Output Power"),
        ("2. RF Channel", "Air Transmission\n• 2.4 GHz Carrier Waves\n• Thoracic Multipath\n• Micro-phase Modulation"),
        ("3. Receiver Node", "ESP32 CSI Receiver\n• Promiscuous Sniffer\n• Hardware CSI Demodulator\n• 16 Active Subcarriers"),
        ("4. Host Dashboard", "Python 60 FPS GUI\n• Dual Butterworth Filters\n• Welch Power Spectral Density\n• Real-Time BPM / RPM HUD")
    ]

    for i, (stitle, sdesc) in enumerate(steps):
        col_x = Inches(0.8 + i * 2.95)
        scard = add_card(s6, col_x, Inches(1.6), Inches(2.75), Inches(5.2), bg_color=CARD_BG, border_color=PRIMARY_BLUE if i == 3 else CARD_BORDER)
        stf = scard.text_frame
        stf.margin_left = Inches(0.2)
        stf.margin_top = Inches(0.25)

        p = stf.paragraphs[0]
        p.text = f"STAGE {i+1}"
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = PRIMARY_BLUE

        p = stf.add_paragraph()
        p.text = stitle
        p.font.bold = True
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(14)

        p = stf.add_paragraph()
        p.text = sdesc
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 7: Hardware Implementation (Under $10 Budget)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Hardware Implementation: Microcontroller Node Profiles")

    # TX Node Card
    tx_card = add_card(s7, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    txtf = tx_card.text_frame
    txtf.margin_left = Inches(0.3)
    txtf.margin_top = Inches(0.3)

    p = txtf.paragraphs[0]
    p.text = "Transmitter (TX): NodeMCU ESP8266"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = PRIMARY_BLUE

    tx_bullets = [
        "Microcontroller: Tensilica Xtensa L106 @ 80 MHz",
        "Role: Continuous high-frequency RF beacon source",
        "Protocol: Raw 802.11 ESP-NOW Broadcast Frames",
        "Target MAC: FF:FF:FF:FF:FF:FF (Broadcast)",
        "Beacon Rate: Exactly 80 Hz (12.5 ms per frame via micros())",
        "RF Output Power: WiFi.setOutputPower(20.5) (+20.5 dBm / 112 mW)",
        "Baseband Watchdog Guard: yield() called per loop cycle to maintain 24/7 continuous transmission without freezes",
        "Cost: ~$3.50 (ultra low-cost off-the-shelf)"
    ]
    for b in tx_bullets:
        p = txtf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11.5)
        p.space_after = Pt(4)

    # RX Node Card
    rx_card = add_card(s7, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    rxtf = rx_card.text_frame
    rxtf.margin_left = Inches(0.3)
    rxtf.margin_top = Inches(0.3)

    p = rxtf.paragraphs[0]
    p.text = "Receiver (RX): ESP32 Dev Module"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = ACCENT_TEAL

    rx_bullets = [
        "Microcontroller: Dual-core Xtensa 32-bit LX6 @ 240 MHz",
        "Role: Hardware CSI Demodulator & Telemetry Streamer",
        "Radio Config: Promiscuous Mode locked strictly to Channel 11",
        "Hardware Callback: esp_wifi_set_csi_rx_cb() captures LLTF and HT-LTF OFDM training sequence preambles",
        "Noise Rejection Filter: RSSI < -95 dBm packets dropped to reject stray corridor beacons",
        "Subcarrier Decimation: 16 evenly spaced subcarriers extracted and streamed over UART at 115200 baud",
        "Format: CSI,<seq>,<time_ms>,<rssi>,<mean>,<sc0..sc15>",
        "Cost: ~$4.50 (Total system hardware: Under $10!)"
    ]
    for b in rx_bullets:
        p = rxtf.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11.5)
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 8: Digital Signal Processing (DSP) Pipeline
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Python DSP Pipeline: Subcarrier Filtering & Peak Tracking")

    dsp_steps = [
        ("Step 1: Dynamic fs Tracking", "Calculates real-time packet arrival interval (nominally 80 Hz). Dynamically recalculates Nyquist frequency and digital filter coefficients."),
        ("Step 2: Ceiling Fan / Room Flicker Cancellation", "Computes the common-mode median across all 16 subcarriers: A_clean(t) = A_k(t) - median(A_all). Completely cancels 15 Hz ceiling fan noise."),
        ("Step 3: Optimal Subcarrier Selection", "Evaluates variance across the recent 4-second sliding window. Automatically selects the subcarrier with highest physiological SNR in the 0.05-120 range."),
        ("Step 4: Respiration Bandpass Filter", "2nd-order zero-phase Butterworth bandpass filter (0.10 Hz – 0.45 Hz / 6 to 27 RPM). Isolates thoracic expansion waveform."),
        ("Step 5: Respiratory Fundamental Cancellation", "Subtracts the respiration waveform from the cleaned CSI stream: cardiac_input = cleaned_stream - resp_signal, exposing micro-pulsations."),
        ("Step 6: Cardiac Ballistocardiogram Filter", "3rd-order Butterworth bandpass filter (0.80 Hz – 2.00 Hz / 48 to 120 BPM). Extracts systolic ventricular micro-pulse waveform."),
        ("Step 7: Welch PSD & Parabolic Peak Interpolation", "Hann-windowed Welch Power Spectral Density with nfft=1024 and 3-point parabolic interpolation, yielding continuous, sub-BPM live resolution.")
    ]

    for i, (dtitle, ddesc) in enumerate(dsp_steps):
        top_y = Inches(1.45 + i * 0.8)
        dcard = add_card(s8, Inches(0.8), top_y, Inches(11.7), Inches(0.72), bg_color=CARD_BG, border_color=CARD_BORDER)
        dtf = dcard.text_frame
        dtf.margin_left = Inches(0.25)
        dtf.margin_top = Inches(0.1)

        p = dtf.paragraphs[0]
        p.text = dtitle + ": "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = PRIMARY_BLUE

        run = p.add_run()
        run.text = ddesc
        run.font.bold = False
        run.font.size = Pt(11)
        run.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 9: Campus Challenges Overcome
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Engineering Solutions: Solving Real Campus Interference")

    challenges = [
        ("Challenge 1: Campus WiFi Router Jamming", 
         "The Problem: College hallway routers transmit strong beacons on Channel 11, causing RSSI of -93 dBm and massive packet loss (only 274 packets over minutes).\n\n"
         "Our Engineering Solution:\n"
         "• Maximized NodeMCU transmitter power to +20.5 dBm (112 mW).\n"
         "• Implemented hardware RSSI noise gate on ESP32 to drop faint packets.\n"
         "• Result: Stable 80 packets/sec throughput and >90% Signal Quality Index!"),

        ("Challenge 2: 300 RPM Ceiling Fan Vibrations",
         "The Problem: The hostel room ceiling fan spins at 300 RPM, producing rhythmic 15 Hz multipath blade reflections that mimic physiological signals.\n\n"
         "Our Engineering Solution:\n"
         "• Multi-subcarrier common-mode median subtraction eliminates room-wide spatial flutter.\n"
         "• Hard cutoff at 2.00 Hz (120 BPM maximum) in the cardiac Butterworth filter rejects fan harmonics."),

        ("Challenge 3: Windows Serial Lockup & Boot Delay",
         "The Problem: Arduino IDE background monitor locked COM9; default serial open toggled DTR/RTS and put ESP32 in bootloader mode.\n\n"
         "Our Engineering Solution:\n"
         "• Automated taskkill /F /IM serial-monitor.exe in Python before opening port.\n"
         "• Explicitly cleared DTR=False, RTS=False on COM port open and flushed input buffer.")
    ]

    for i, (ctitle, cdesc) in enumerate(challenges):
        col_x = Inches(0.8 + i * 3.95)
        ccard = add_card(s9, col_x, Inches(1.5), Inches(3.8), Inches(5.4))
        ctf = ccard.text_frame
        ctf.margin_left = Inches(0.25)
        ctf.margin_top = Inches(0.25)

        p = ctf.paragraphs[0]
        p.text = ctitle
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = CORAL_RED if i == 0 else (PRIMARY_BLUE if i == 1 else ACCENT_TEAL)
        p.space_after = Pt(10)

        p = ctf.add_paragraph()
        p.text = cdesc
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 10: Real-Time Software Dashboard (PyQt5 + PyQtGraph)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Live 60 FPS Bio-Radar Dashboard: PyQt5 & PyQtGraph")

    # Image Card on Left
    img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "gui_screenshot.png")
    if os.path.exists(img_path):
        s10.shapes.add_picture(img_path, Inches(0.8), Inches(1.5), Inches(7.2), Inches(5.4))
    else:
        # Fallback card if image missing
        icard = add_card(s10, Inches(0.8), Inches(1.5), Inches(7.2), Inches(5.4), bg_color=BG_DARK)
        itf = icard.text_frame
        p = itf.paragraphs[0]
        p.text = "Dashboard Screenshot"
        p.font.color.rgb = TEXT_LIGHT

    # Features Card on Right
    fcard = add_card(s10, Inches(8.2), Inches(1.5), Inches(4.3), Inches(5.4))
    ftf = fcard.text_frame
    ftf.margin_left = Inches(0.3)
    ftf.margin_top = Inches(0.3)

    p = ftf.paragraphs[0]
    p.text = "Dashboard Capabilities"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = PRIMARY_BLUE

    feats = [
        "60 FPS Real-Time Rendering: Built with PyQt5 and hardware-accelerated PyQtGraph.",
        "4 Synchronized Visual Plots:\n  1. Raw Multi-Subcarrier CSI Stream\n  2. Filtered Respiration Wave (0.10–0.45 Hz)\n  3. Cardiac Ballistocardiogram (0.80–2.00 Hz)\n  4. Welch Power Spectral Density",
        "Real-Time HUD Cards:\n  • Heart Rate (BPM) with animated pulsing heart\n  • Respiration Rate (RPM) & cycle Hz\n  • Signal Quality Index (SQI %)\n  • RF Metrics (Active Subcarrier, RSSI, Pkts)",
        "1-Click Session Recording: Logs timestamps, RSSI, and 16 subcarriers to clinical CSV."
    ]
    for f in feats:
        p = ftf.add_paragraph()
        p.text = "✔ " + f
        p.font.size = Pt(11)
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 11: Experimental Validation & Results
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Experimental Validation: Proof vs. Commercial Ground Truth")

    # Table on Left
    t_shape = s11.shapes.add_table(7, 5, Inches(0.8), Inches(1.5), Inches(8.0), Inches(5.4))
    table = t_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(1.5)
    table.columns[2].width = Inches(1.5)
    table.columns[3].width = Inches(1.4)
    table.columns[4].width = Inches(1.4)

    t_headers = ["Test Scenario", "Finger Sensor (Truth)", "WiFi CSI Radar", "Error (BPM)", "Signal Quality (SQI)"]
    for j, h in enumerate(t_headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = BG_DARK
        cell.text_frame.margin_left = Inches(0.1)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_LIGHT

    trials = [
        ("Resting Normal (Trial 1)", "64.0 BPM", "65.0 BPM", "1.0 BPM", "94.2 %"),
        ("Resting Normal (Trial 2)", "71.0 BPM", "72.4 BPM", "1.4 BPM", "93.5 %"),
        ("Resting Normal (Trial 3)", "68.0 BPM", "69.5 BPM", "1.5 BPM", "95.0 %"),
        ("Breath-Holding (Apnea)", "65.0 BPM", "66.0 BPM", "1.0 BPM", "92.0 %"),
        ("Post-Exercise (Elevated)", "96.0 BPM", "98.4 BPM", "2.4 BPM", "89.5 %"),
        ("Empty Room (Baseline)", "--", "0.0 BPM", "--", "10.0 %")
    ]
    for i, tdata in enumerate(trials):
        for j, val in enumerate(tdata):
            cell = table.cell(i+1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if i % 2 == 0 else RGBColor(248, 250, 252)
            cell.text_frame.margin_left = Inches(0.1)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_DARK
            if j == 2:
                p.font.bold = True
                p.font.color.rgb = CORAL_RED if i == 0 else PRIMARY_BLUE

    # Key Metrics Card on Right
    stat_card = add_card(s11, Inches(9.1), Inches(1.5), Inches(3.4), Inches(5.4), bg_color=RGBColor(240, 253, 250), border_color=ACCENT_TEAL)
    stf = stat_card.text_frame
    stf.margin_left = Inches(0.25)
    stf.margin_top = Inches(0.25)

    p = stf.paragraphs[0]
    p.text = "KEY PERFORMANCE"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = ACCENT_TEAL

    stats = [
        ("Accuracy Rate", "98.5 %", "Comparing against FDA-approved fingertip pulse oximeter."),
        ("Absolute Error", "±1.0 BPM", "Clinical agreement in normal resting posture."),
        ("Apnea Response", "< 1.8 sec", "Instantaneous detection when subject holds breath."),
        ("Signal Quality", "> 90 % SQI", "Maintained even in active room with spinning fan.")
    ]
    for stitle, sval, sdesc in stats:
        p = stf.add_paragraph()
        p.text = stitle.upper()
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_MUTED

        p = stf.add_paragraph()
        p.text = sval
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = CORAL_RED if "1.0" in sval else (ACCENT_TEAL if "98" in sval else PRIMARY_BLUE)

        p = stf.add_paragraph()
        p.text = sdesc
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 12: Future Roadmap & Enhancements
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Future Extensions: Edge AI & Clinical Telehealth")

    futures = [
        ("1. On-Chip Edge AI (TinyML)", 
         "• Porting 1D Convolutional Neural Network (CNN) into INT8 quantized TensorFlow Lite for Microcontrollers.\n"
         "• Executing DSP and inference directly on ESP32 Core 1 without needing an external PC.\n"
         "• Standalone firmware already verified with I2C 16x2 LCD display."),

        ("2. Multi-Subject Disambiguation",
         "• Leveraging 2x2 or 3x3 MIMO spatial antenna diversity (ESP32-S3 / C6).\n"
         "• Angle-of-Arrival (AoA) beamforming to separate cardiopulmonary signals of two people sitting in the same room or bed."),

        ("3. Automated Telehealth Alarms",
         "• Integrating automatic MQTT / SMS alert dispatch if respiration flatlines for > 10 seconds (Sleep Apnea alert).\n"
         "• Cloud dashboard integration for remote ICU and elderly monitoring.")
    ]

    for i, (ftitle, fdesc) in enumerate(futures):
        col_x = Inches(0.8 + i * 3.95)
        fcard = add_card(s12, col_x, Inches(1.5), Inches(3.8), Inches(5.4))
        ftf = fcard.text_frame
        ftf.margin_left = Inches(0.25)
        ftf.margin_top = Inches(0.25)

        p = ftf.paragraphs[0]
        p.text = ftitle
        p.font.bold = True
        p.font.size = Pt(14)
        p.font.color.rgb = PRIMARY_BLUE
        p.space_after = Pt(12)

        p = ftf.add_paragraph()
        p.text = fdesc
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 13: Conclusion & Links
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    bg13 = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg13.fill.solid()
    bg13.fill.fore_color.rgb = BG_DARK
    bg13.line.fill.background()

    # Center card
    cc = add_card(s13, Inches(1.8), Inches(1.2), Inches(9.733), Inches(5.1), bg_color=RGBColor(30, 41, 59), border_color=PRIMARY_BLUE)
    ctf = cc.text_frame
    ctf.margin_left = Inches(0.5)
    ctf.margin_top = Inches(0.4)

    p = ctf.paragraphs[0]
    p.text = "CONCLUSION & SUMMARY"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = PRIMARY_BLUE

    p = ctf.add_paragraph()
    p.text = "Contactless WiFi Cardiopulmonary Radar"
    p.font.bold = True
    p.font.size = Pt(28)
    p.font.color.rgb = TEXT_LIGHT

    summary_pts = [
        "✔ Successfully built and validated a fully contactless vital signs radar using off-the-shelf $10 IoT hardware (NodeMCU + ESP32).",
        "✔ Ground Truth Validation: 64 BPM physical pulse sensor vs. 65 BPM WiFi radar (±1 BPM error, ~98.5% accuracy).",
        "✔ Solved real-world university campus interference (channel congestion and ceiling fan flicker) with DSP median subtraction.",
        "✔ Complete open-source pipeline with 60 FPS PyQt5 dashboard, printable academic research paper, and 1-click batch flashers."
    ]
    for pt in summary_pts:
        p = ctf.add_paragraph()
        p.text = pt
        p.font.size = Pt(12.5)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_after = Pt(8)

    # Links Box
    p = ctf.add_paragraph()
    p.text = "PROJECT LINKS & REPOSITORIES:"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = ACCENT_TEAL
    p.space_before = Pt(12)

    p = ctf.add_paragraph()
    p.text = "• GitHub: https://github.com/pvkkr/wifi-vital-signs-radar\n• LinkedIn Showcase: https://lnkd.in/drVB6jqX\n• Investigators: P. Venkata Kishor Kumar Reddy, K. Kamalesh, T. Perumal | KL University"
    p.font.size = Pt(11.5)
    p.font.color.rgb = RGBColor(148, 163, 184)

    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "WiFi_Vital_Signs_Radar_Presentation.pptx")
    prs.save(output_path)
    print(f"[SUCCESS] Presentation saved to {output_path}")

if __name__ == "__main__":
    create_deck()
