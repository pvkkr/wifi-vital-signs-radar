"""
WiFi Vital Signs Radar - Simple, Clean Viva Presentation Generator
Focuses on clear, bold, concise slides with zero complicated clutter.
Authors: P. Venkata Kishor Kumar Reddy, K. Kamalesh, T. Perumal
Affiliation: KL University
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_simple_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    NAVY = RGBColor(15, 23, 42)         # #0F172A
    WHITE = RGBColor(255, 255, 255)
    BLUE = RGBColor(2, 132, 199)        # #0284C7
    LIGHT_BLUE = RGBColor(240, 249, 255)
    GRAY_BG = RGBColor(248, 250, 252)   # #F8FAFC
    CARD_BORDER = RGBColor(226, 232, 240)
    DARK_TEXT = RGBColor(30, 41, 59)
    MUTED_TEXT = RGBColor(100, 116, 139)
    GREEN = RGBColor(16, 185, 129)      # #10B981
    RED = RGBColor(225, 29, 72)         # #E11D48

    def add_top_bar(slide, title, category="WIFI VITAL SIGNS RADAR"):
        # Header background
        h_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        h_shape.fill.solid()
        h_shape.fill.fore_color.rgb = NAVY
        h_shape.line.fill.background()

        tf = h_shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.8)
        tf.margin_top = Inches(0.18)

        p0 = tf.paragraphs[0]
        p0.text = category.upper()
        p0.font.name = "Arial"
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = BLUE

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = "Arial"
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = WHITE

        # Accent line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
        line.fill.solid()
        line.fill.fore_color.rgb = BLUE
        line.line.fill.background()

    def add_card(slide, left, top, width, height, bg=WHITE, border=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = border
        card.line.width = Pt(1.5)
        return card

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    # Left accent bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.15), Inches(5.1))
    bar.fill.solid()
    bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()

    # Title text
    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.0), Inches(2.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "IOT & BIOMEDICAL VIVA PRESENTATION 2026"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = BLUE

    p = tf1.add_paragraph()
    p.text = "Contactless WiFi Vital Signs Radar"
    p.font.name = "Arial"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p = tf1.add_paragraph()
    p.text = "Measuring Heartbeat & Respiration using 2.4 GHz WiFi (NodeMCU + ESP32)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(148, 163, 184)

    # Team Card
    tc = add_card(s1, Inches(1.2), Inches(4.0), Inches(6.8), Inches(2.3), bg=RGBColor(30, 41, 59), border=BLUE)
    tcf = tc.text_frame
    tcf.margin_left = Inches(0.3)
    tcf.margin_top = Inches(0.25)

    p = tcf.paragraphs[0]
    p.text = "PROJECT TEAM MEMBERS"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = BLUE

    members = [
        "• P. Venkata Kishor Kumar Reddy (Lead Project Developer)",
        "• K. Kamalesh (Co-Developer)",
        "• T. Perumal (Co-Developer)"
    ]
    for m in members:
        p = tcf.add_paragraph()
        p.text = m
        p.font.name = "Segoe UI"
        p.font.size = Pt(14)
        p.font.bold = "Lead" in m
        p.font.color.rgb = WHITE if "Lead" in m else RGBColor(226, 232, 240)

    # University Card
    uc = add_card(s1, Inches(8.3), Inches(4.0), Inches(4.2), Inches(2.3), bg=RGBColor(30, 41, 59), border=CARD_BORDER)
    ucf = uc.text_frame
    ucf.margin_left = Inches(0.3)
    ucf.margin_top = Inches(0.25)

    p = ucf.paragraphs[0]
    p.text = "INSTITUTION"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GREEN

    p = ucf.add_paragraph()
    p.text = "KL University (KLEF)"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p = ucf.add_paragraph()
    p.text = "Dept. of ECE & CSE\nVaddeswaram, Andhra Pradesh"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: The Core Concept (Simple & Direct)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_top_bar(s2, "The Core Question: Can WiFi Track Your Heartbeat?")

    card_s2_left = add_card(s2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    tf2_l = card_s2_left.text_frame
    tf2_l.margin_left = Inches(0.3)
    tf2_l.margin_top = Inches(0.4)

    p = tf2_l.paragraphs[0]
    p.text = "Yes, Completely Contactless!"
    p.font.name = "Arial"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = BLUE

    bullets2_l = [
        "No electrodes attached to the chest.",
        "No finger pulse clips or smartwatches.",
        "Patient touches zero wires and zero sensors.",
        "Works purely through invisible 2.4 GHz WiFi waves bouncing off the chest wall."
    ]
    for b in bullets2_l:
        p = tf2_l.add_paragraph()
        p.text = "✔  " + b
        p.font.name = "Segoe UI"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(12)

    card_s2_right = add_card(s2, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), bg=LIGHT_BLUE, border=BLUE)
    tf2_r = card_s2_right.text_frame
    tf2_r.margin_left = Inches(0.4)
    tf2_r.margin_top = Inches(0.4)

    p = tf2_r.paragraphs[0]
    p.text = "Key Project Achievements"
    p.font.name = "Arial"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RED

    achievements = [
        ("Ground Truth Test:", "64 BPM (Finger Sensor) vs. 65 BPM (WiFi Radar)"),
        ("Accuracy:", "98.5% (~1 BPM difference)"),
        ("Hardware Cost:", "Under $10 (1 NodeMCU + 1 ESP32)"),
        ("Real-Time Speed:", "60 FPS live PyQt5 desktop dashboard")
    ]
    for title, desc in achievements:
        p = tf2_r.add_paragraph()
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = MUTED_TEXT
        p.space_before = Pt(10)

        p = tf2_r.add_paragraph()
        p.text = desc
        p.font.name = "Arial"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 3: Why Existing Devices Fall Short
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_top_bar(s3, "Problem Statement: Why Traditional Sensors Fail")

    cols = [
        ("1. ECG Adhesive Gels", RED, [
            "Causes skin rashes & allergic irritation.",
            "Trailing wires limit patient movement.",
            "Requires medical staff to apply properly."
        ]),
        ("2. Finger Clips & Watches", BLUE, [
            "Clips easily slip off when moving in bed.",
            "Smartwatches need daily battery charging.",
            "Loose contact causes false alarms in sleep."
        ]),
        ("3. Hospital mmWave Radar", GREEN, [
            "Evaluation boards cost $200 – $400.",
            "Requires specialized expensive antennas.",
            "Not available in ordinary homes."
        ])
    ]

    for i, (title, color, items) in enumerate(cols):
        c = add_card(s3, Inches(0.8 + i * 4.0), Inches(1.5), Inches(3.7), Inches(5.4))
        ctf = c.text_frame
        ctf.margin_left = Inches(0.3)
        ctf.margin_top = Inches(0.3)

        p = ctf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(16)

        for item in items:
            p = ctf.add_paragraph()
            p.text = "• " + item
            p.font.name = "Segoe UI"
            p.font.size = Pt(14)
            p.font.color.rgb = DARK_TEXT
            p.space_before = Pt(12)

    # =========================================================================
    # SLIDE 4: How It Works (The Simple Science)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_top_bar(s4, "How It Works: Simple Physics in 3 Steps")

    steps_s4 = [
        ("Step 1: Chest Wall Micro-Movement", 
         "• Every breath moves the chest forward by 5 mm to 12 mm.\n• Every heartbeat pushes the chest skin forward by just 0.2 mm to 0.5 mm (ballistocardiogram)."),
        ("Step 2: WiFi Waves Bounce Off Chest",
         "• Standard 2.4 GHz WiFi carrier wavelength is 12.2 cm.\n• Micro-movements shift the reflected WiFi wave slightly, changing signal phase and amplitude."),
        ("Step 3: ESP32 Captures CSI Matrix",
         "• Unlike crude RSSI (1 number), CSI provides 16 distinct subcarrier channels.\n• Captures 80 packets per second to detect the heartbeat pulse cleanly!")
    ]

    for i, (stitle, sbody) in enumerate(steps_s4):
        c = add_card(s4, Inches(0.8), Inches(1.5 + i * 1.8), Inches(11.7), Inches(1.6))
        ctf = c.text_frame
        ctf.margin_left = Inches(0.3)
        ctf.margin_top = Inches(0.18)

        p = ctf.paragraphs[0]
        p.text = stitle
        p.font.name = "Arial"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = BLUE

        p = ctf.add_paragraph()
        p.text = sbody
        p.font.name = "Segoe UI"
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 5: Hardware Setup (Under $10)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_top_bar(s5, "Hardware Setup: Built With Low-Cost Off-The-Shelf IoT")

    # Left: Transmitter
    c_tx = add_card(s5, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    tx_f = c_tx.text_frame
    tx_f.margin_left = Inches(0.3)
    tx_f.margin_top = Inches(0.3)

    p = tx_f.paragraphs[0]
    p.text = "Transmitter: NodeMCU ESP8266 ($3.50)"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_after = Pt(14)

    tx_pts = [
        "Power: Powered from any simple USB power bank.",
        "Role: Fires 80 WiFi beacon packets every second.",
        "RF Boost: Set to +20.5 dBm maximum power to overpower room WiFi routers.",
        "Channel: Locked strictly to Channel 11 (2.462 GHz)."
    ]
    for pt in tx_pts:
        p = tx_f.add_paragraph()
        p.text = "• " + pt
        p.font.name = "Segoe UI"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(10)

    # Right: Receiver
    c_rx = add_card(s5, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    rx_f = c_rx.text_frame
    rx_f.margin_left = Inches(0.3)
    rx_f.margin_top = Inches(0.3)

    p = rx_f.paragraphs[0]
    p.text = "Receiver: ESP32 Dev Module ($4.50)"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = GREEN
    p.space_after = Pt(14)

    rx_pts = [
        "Connection: Plugged into laptop USB port.",
        "Role: Captures raw Channel State Information (CSI) from incoming WiFi packets.",
        "Filter: Rejects faint signals from far away hallway routers.",
        "Data Stream: Streams 16 subcarriers over Serial at 115200 baud to the PC."
    ]
    for pt in rx_pts:
        p = rx_f.add_paragraph()
        p.text = "• " + pt
        p.font.name = "Segoe UI"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 6: Desk Placement (Fresnel Zone Geometry)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_top_bar(s6, "Physical Desk Placement: 40 cm Distance")

    c_g1 = add_card(s6, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), bg=NAVY, border=BLUE)
    g1_tf = c_g1.text_frame
    g1_tf.margin_left = Inches(0.3)
    g1_tf.margin_top = Inches(0.3)

    p = g1_tf.paragraphs[0]
    p.text = "RADAR DESK GEOMETRY"
    p.font.name = "Arial"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = BLUE

    diagram = """
    [ NodeMCU TX ]                   [ ESP32 RX ]
    (Power Bank)                    (Into Laptop)
        [■]                             [■]
         |                               |
         | <────── 80 cm to 1.0 m ─────> |
         \\                               /
          \\     (   SUBJECT SEATED   )  /
           \\    (  Chest Level 1.0m  ) /
            \\   (   30 to 50 cm away )/
             -------------------------
    """
    p = g1_tf.add_paragraph()
    p.text = diagram
    p.font.name = "Consolas"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(148, 163, 184)
    p.space_before = Pt(10)

    c_g2 = add_card(s6, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    g2_tf = c_g2.text_frame
    g2_tf.margin_left = Inches(0.3)
    g2_tf.margin_top = Inches(0.3)

    p = g2_tf.paragraphs[0]
    p.text = "Simple Placement Rules"
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(14)

    rules = [
        "1. Distance: Place NodeMCU and ESP32 about 1 meter apart on a table.",
        "2. Seating: Sit comfortably 30 cm to 50 cm away from the line between them.",
        "3. Height: Keep both antennas roughly at chest height (around 1 meter).",
        "4. Posture: Sit naturally, relax, and breathe normally!"
    ]
    for r in rules:
        p = g2_tf.add_paragraph()
        p.text = r
        p.font.name = "Segoe UI"
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(12)

    # =========================================================================
    # SLIDE 7: Signal Processing Pipeline (Simple & Clear)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_top_bar(s7, "Signal Processing: Isolating Heartbeat from Noise")

    dsp_steps_simple = [
        ("1. Pick Best Subcarrier", "Automatically selects the cleanest of the 16 WiFi channels showing maximum chest reflection."),
        ("2. Cancel Ceiling Fan Noise", "Hostel ceiling fans spin at 300 RPM. We subtract common-mode room flicker across all channels."),
        ("3. Extract Breathing Wave", "Butterworth bandpass filter (0.10 to 0.45 Hz) extracts slow, deep chest expansions."),
        ("4. Extract Heartbeat Pulse", "We subtract the breathing wave and filter (0.80 to 2.00 Hz) to isolate tiny heartbeat ripples (48 - 120 BPM).")
    ]

    for i, (head, body) in enumerate(dsp_steps_simple):
        card = add_card(s7, Inches(0.8), Inches(1.5 + i * 1.35), Inches(11.7), Inches(1.2))
        ctf = card.text_frame
        ctf.margin_left = Inches(0.3)
        ctf.margin_top = Inches(0.18)

        p = ctf.paragraphs[0]
        p.text = head
        p.font.name = "Arial"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = BLUE

        p = ctf.add_paragraph()
        p.text = body
        p.font.name = "Segoe UI"
        p.font.size = Pt(13.5)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 8: Live Software Dashboard
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_top_bar(s8, "Live Software Dashboard: Real-Time 60 FPS GUI")

    img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "gui_screenshot.png")
    if os.path.exists(img_path):
        s8.shapes.add_picture(img_path, Inches(0.8), Inches(1.5), Inches(7.5), Inches(5.4))

    dash_card = add_card(s8, Inches(8.5), Inches(1.5), Inches(4.0), Inches(5.4))
    dtf = dash_card.text_frame
    dtf.margin_left = Inches(0.3)
    dtf.margin_top = Inches(0.3)

    p = dtf.paragraphs[0]
    p.text = "Dashboard Highlights"
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.space_after = Pt(12)

    gui_pts = [
        "Built with PyQt5 and PyQtGraph for smooth 60 FPS plotting.",
        "Live HUD Cards: Shows Heart Rate (BPM), Breathing (RPM), and Signal Quality (SQI %).",
        "4 Live Graphs: Raw CSI, Respiration wave, Heartbeat pulse, and Frequency spectrum.",
        "1-Click CSV Record: Saves clinical data for doctors."
    ]
    for pt in gui_pts:
        p = dtf.add_paragraph()
        p.text = "✔ " + pt
        p.font.name = "Segoe UI"
        p.font.size = Pt(13.5)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 9: Validation Results (64 vs 65 BPM Proof)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_top_bar(s9, "Experimental Results: 64 vs 65 BPM Ground Truth Proof")

    # Big Proof Card
    proof_card = add_card(s9, Inches(0.8), Inches(1.5), Inches(11.7), Inches(2.2), bg=LIGHT_BLUE, border=BLUE)
    ptf = proof_card.text_frame
    ptf.margin_left = Inches(0.4)
    ptf.margin_top = Inches(0.2)

    p = ptf.paragraphs[0]
    p.text = "LIVE SIDE-BY-SIDE VALIDATION TEST"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = BLUE

    p = ptf.add_paragraph()
    p.text = "Finger Pulse Sensor: 64 BPM   |   WiFi CSI Radar: 65 BPM"
    p.font.name = "Arial"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RED

    p = ptf.add_paragraph()
    p.text = "🎯 Difference: Only 1 BPM  |  Accuracy: ~98.5% Agreement!"
    p.font.name = "Segoe UI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GREEN

    # Bottom 3 Stat Cards
    stat_boxes = [
        ("Resting Heart Rate", "±1 BPM Error", "Validated against medical fingertip pulse oximeter."),
        ("Breath-Hold Detection", "< 1.8 Seconds", "Instantly detects when a person holds their breath (sleep apnea)."),
        ("Signal Quality (SQI)", "> 90% Clean", "Maintained in normal hostel room with spinning ceiling fan.")
    ]

    for i, (title, value, desc) in enumerate(stat_boxes):
        box = add_card(s9, Inches(0.8 + i * 4.0), Inches(4.0), Inches(3.7), Inches(2.9))
        btf = box.text_frame
        btf.margin_left = Inches(0.3)
        btf.margin_top = Inches(0.25)

        p = btf.paragraphs[0]
        p.text = title.upper()
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = MUTED_TEXT

        p = btf.add_paragraph()
        p.text = value
        p.font.name = "Arial"
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = BLUE

        p = btf.add_paragraph()
        p.text = desc
        p.font.name = "Segoe UI"
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 10: Conclusion & Summary
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    bg10 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg10.fill.solid()
    bg10.fill.fore_color.rgb = NAVY
    bg10.line.fill.background()

    card_s10 = add_card(s10, Inches(1.8), Inches(1.2), Inches(9.733), Inches(5.1), bg=RGBColor(30, 41, 59), border=BLUE)
    tf10 = card_s10.text_frame
    tf10.margin_left = Inches(0.5)
    tf10.margin_top = Inches(0.4)

    p = tf10.paragraphs[0]
    p.text = "PROJECT SUMMARY & VIVA CONCLUSION"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = BLUE

    p = tf10.add_paragraph()
    p.text = "Contactless WiFi Vital Signs Radar"
    p.font.name = "Arial"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_after = Pt(10)

    concl_pts = [
        "✔ 100% Contactless: Zero wires, zero skin patches, zero patient discomfort.",
        "✔ Under $10 Budget: Uses low-cost NodeMCU and ESP32 IoT microcontrollers.",
        "✔ Proven Accuracy: 64 BPM vs 65 BPM (~98.5% clinical agreement).",
        "✔ Complete Delivery: 60 FPS live GUI, full research paper, and open-source code."
    ]
    for pt in concl_pts:
        p = tf10.add_paragraph()
        p.text = pt
        p.font.name = "Segoe UI"
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_before = Pt(6)

    p = tf10.add_paragraph()
    p.text = "GitHub Repository: https://github.com/pvkkr/wifi-vital-signs-radar"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = GREEN
    p.space_before = Pt(14)

    p = tf10.add_paragraph()
    p.text = "Presented by: P. Venkata Kishor Kumar Reddy, K. Kamalesh, T. Perumal | KL University"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(148, 163, 184)

    # Save to simple presentation filename
    simple_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "WiFi_Vital_Signs_Radar_Presentation_Simple.pptx")
    prs.save(simple_file)
    print(f"[SUCCESS] Simple Presentation saved to: {simple_file}")

    # Also try to save to main file if not locked
    main_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "WiFi_Vital_Signs_Radar_Presentation.pptx")
    try:
        prs.save(main_file)
        print(f"[SUCCESS] Updated main presentation: {main_file}")
    except PermissionError:
        print(f"[NOTICE] Main file is currently open in PowerPoint. Saved as: {simple_file}")

if __name__ == "__main__":
    build_simple_deck()
