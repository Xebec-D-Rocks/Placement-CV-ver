#!/usr/bin/env python3
"""
CoalGuard Fixed Presentation - 10-20-30 compliant, landscape 16:9, real screenshots
"""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Theme
BG_DARK = RGBColor(15, 22, 32)
BG_PANEL = RGBColor(22, 32, 44)
BG_CARD = RGBColor(28, 40, 54)
BORDER = RGBColor(42, 55, 70)
MUTED = RGBColor(147, 164, 184)
TEXT = RGBColor(230, 237, 243)
ACCENT = RGBColor(62, 166, 255)
ACCENT2 = RGBColor(51, 194, 129)
LOW = RGBColor(51, 194, 129)
MEDIUM = RGBColor(230, 194, 41)
HIGH = RGBColor(239, 138, 60)
CRITICAL = RGBColor(239, 68, 68)
WHITE = RGBColor(255,255,255)

OUT = Path(__file__).parent / "CoalGuard_SIH26024_Presentation.pptx"
REAL = Path(__file__).parent / "docs" / "presentation_assets" / "real"

# Ensure 16:9 landscape
prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)
prs.core_properties.title = "CoalGuard — SIH 2026 PSID 26024"
prs.core_properties.subject = "AI-Based Smart Governance & Compliance Monitoring for Coal Mines"
prs.core_properties.author = "CoalGuard Team"

def set_bg(slide, color=BG_DARK):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def shape(slide, left, top, width, height, fill=None, line=None, lw=1, radius=False):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, left, top, width, height)
    shp.line.fill.background()
    if fill:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    else:
        shp.fill.background()
    if line:
        shp.line.color.rgb = line
        shp.line.width = Pt(lw)
    else:
        shp.line.fill.background()
    if radius:
        try: shp.adjustments[0]=0.08
        except: pass
    return shp

def textbox(slide, left, top, width, height, text, size=18, color=TEXT, bold=False, align=PP_ALIGN.LEFT, name="Calibri", italic=False, line_spacing=None):
    tx = slide.shapes.add_textbox(left, top, width, height)
    tf = tx.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.italic = italic
    p.font.name = name
    p.alignment = align
    p.line_spacing = Pt(line_spacing or size*1.2)
    return tx

def add_bullets(slide, left, top, width, height, bullets, size=14, color=MUTED, bold_prefix=False, bullet_char="•"):
    tx = slide.shapes.add_textbox(left, top, width, height)
    tf = tx.text_frame
    tf.word_wrap = True
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i==0 else tf.add_paragraph()
        # bold prefix before colon if exists
        if bold_prefix and ":" in b:
            pre, post = b.split(":",1)
            # we can't have mixed formatting easily, so keep whole bullet but make first part bold via run
            p.text = ""
            run1 = p.add_run()
            run1.text = bullet_char + "  " + pre.strip() + ":"
            run1.font.size = Pt(size)
            run1.font.color.rgb = TEXT
            run1.font.bold = True
            run1.font.name = "Calibri"
            run2 = p.add_run()
            run2.text = post
            run2.font.size = Pt(size)
            run2.font.color.rgb = color
            run2.font.name = "Calibri"
        else:
            p.text = bullet_char + "  " + b
            p.font.size = Pt(size)
            p.font.color.rgb = color
            p.font.name = "Calibri"
        p.space_after = Pt(6)
        p.line_spacing = Pt(size*1.3)
    return tx

def add_image_contain(slide, img_path, left, top, width, height, border_color=BORDER):
    # container with border
    shape(slide, left-Pt(1), top-Pt(1), width+Pt(2), height+Pt(2), fill=BG_PANEL, line=border_color, lw=1, radius=True)
    if img_path and Path(img_path).exists():
        slide.shapes.add_picture(str(img_path), left, top, width=width, height=height)
    else:
        textbox(slide, left, top+height/2-Inches(0.2), width, Inches(0.4), "[screenshot missing]", 10, MUTED, align=PP_ALIGN.CENTER)

def add_image_cover(slide, img_path, left, top, width, height):
    # Add image with exact cover (distortion if aspect mismatched) but we use viewport 16:9 which matches slide 16:9
    shape(slide, left-Pt(1), top-Pt(1), width+Pt(2), height+Pt(2), fill=BG_PANEL, line=BORDER, lw=1, radius=True)
    if img_path and Path(img_path).exists():
        # Use width only to preserve aspect, then center vertically if needed
        from PIL import Image
        im = Image.open(img_path)
        iw, ih = im.size
        aspect = iw/ih
        target_aspect = width / height
        # we want to fill width, height auto
        if abs(aspect - target_aspect) < 0.15:
            slide.shapes.add_picture(str(img_path), left, top, width=width, height=height)
        else:
            # preserve aspect by fitting inside
            if aspect > target_aspect:
                # wider - fit width
                pic = slide.shapes.add_picture(str(img_path), left, top, width=width)
                # center vertically
                pic.top = int(top + (height - pic.height)/2)
            else:
                pic = slide.shapes.add_picture(str(img_path), left, top, height=height)
                pic.left = int(left + (width - pic.width)/2)
    else:
        textbox(slide, left, top+height/2-Inches(0.2), width, Inches(0.4), "[Image not found]", 10, MUTED, align=PP_ALIGN.CENTER)

# Common paths
dash_top = REAL / "dashboard_viewport.png"
dash_mid = REAL / "dashboard_viewport_mid.png"
dash_bottom = REAL / "dashboard_viewport_bottom.png"
mines_vp = REAL / "mines_viewport.png"
detail_vp = REAL / "mine_detail_viewport.png"
api_vp = REAL / "api_docs_viewport.png"
admin_vp = REAL / "admin_viewport.png"
dash_authed = REAL / "dashboard_authed_viewport.png"

# Fallback to older if viewport not exists
if not dash_top.exists():
    dash_top = REAL / "07_dashboard_authed.png"
if not mines_vp.exists():
    mines_vp = REAL / "02_mines_list.png"

# ===== SLIDE 1: TITLE =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(4), fill=ACCENT)
textbox(slide, Inches(0.7), Inches(0.45), Inches(12), Inches(0.25), "MINISTRY OF COAL  •  COAL INDIA LIMITED  •  SIH 2026  •  PSID 26024", 9, MUTED, align=PP_ALIGN.RIGHT)
# Logo
shape(slide, Inches(0.7), Inches(0.85), Inches(0.68), Inches(0.68), fill=ACCENT, radius=True)
textbox(slide, Inches(0.7), Inches(0.95), Inches(0.68), Inches(0.45), "CG", 22, BG_DARK, bold=True, align=PP_ALIGN.CENTER)
textbox(slide, Inches(1.55), Inches(0.85), Inches(7), Inches(0.45), "CoalGuard", 32, WHITE, bold=True)
textbox(slide, Inches(1.55), Inches(1.30), Inches(7), Inches(0.30), "AI-Based Smart Governance & Compliance Monitoring for Coal Mines", 12, MUTED, italic=True)
shape(slide, Inches(0.7), Inches(1.72), Inches(2.2), Inches(0.32), fill=BG_PANEL, line=BORDER, radius=True)
textbox(slide, Inches(0.7), Inches(1.75), Inches(2.2), Inches(0.32), "SOFTWARE  •  SMART AUTOMATION", 8, ACCENT, bold=True, align=PP_ALIGN.CENTER)
# Headline
tb = slide.shapes.add_textbox(Inches(0.7), Inches(2.25), Inches(7.2), Inches(1.4))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "One Platform to Govern"
p.font.size = Pt(34)
p.font.color.rgb = WHITE
p.font.bold = True
p.font.name = "Calibri"
p.space_after = Pt(4)
p = tf.add_paragraph()
p.text = "Every Mine. Every Rule."
p.font.size = Pt(34)
p.font.color.rgb = ACCENT
p.font.bold = True
p.font.name = "Calibri"
p.space_after = Pt(4)
p = tf.add_paragraph()
p.text = "Every Field Report — in Real Time."
p.font.size = Pt(24)
p.font.color.rgb = WHITE
p.font.bold = False
p.font.name = "Calibri"
textbox(slide, Inches(0.7), Inches(3.85), Inches(7.2), Inches(0.7), "Centralized, AI-enabled, paperless governance for 459 mines — integrating compliance, inspections, contractors & field reporting into a single real-time ecosystem.", 13, MUTED)
# Stats
stats = [("459", "Real Mines"), ("200", "Scored Live"), ("12", "States"), ("6", "High-Risk Flagged")]
sx = Inches(0.7)
for v,lbl in stats:
    shape(slide, sx, Inches(4.75), Inches(1.55), Inches(0.85), fill=BG_PANEL, line=BORDER, radius=True)
    textbox(slide, sx, Inches(4.82), Inches(1.55), Inches(0.45), v, 26, ACCENT, bold=True, align=PP_ALIGN.CENTER)
    textbox(slide, sx, Inches(5.25), Inches(1.55), Inches(0.22), lbl, 8, MUTED, align=PP_ALIGN.CENTER)
    sx += Inches(1.75)
# Right visual - screenshot card (dashboard viewport)
shape(slide, Inches(8.4), Inches(0.85), Inches(4.2), Inches(5.25), fill=BG_PANEL, line=BORDER, radius=True)
textbox(slide, Inches(8.55), Inches(0.95), Inches(3.9), Inches(0.22), "LIVE DASHBOARD PREVIEW  •  REAL SCREENSHOT", 7, ACCENT, bold=True, align=PP_ALIGN.CENTER)
if dash_top.exists():
    # show dashboard viewport image in right card
    slide.shapes.add_picture(str(dash_top), Inches(8.55), Inches(1.22), width=Inches(3.9), height=Inches(2.2))
else:
    shape(slide, Inches(8.55), Inches(1.22), Inches(3.9), Inches(2.2), fill=BG_CARD, line=BORDER, radius=True)
# caption
textbox(slide, Inches(8.55), Inches(3.50), Inches(3.9), Inches(0.45), "Governance Dashboard — 8 live KPIs, Leaflet GIS (459 mines), Chart.js analytics. http://127.0.0.1:8001/", 7, MUTED, align=PP_ALIGN.CENTER)
# Feature pills
feats = ["Real-time KPIs", "Leaflet GIS", "AI Risk Engine", "Offline Mobile", "Blockchain Audit", "OCR Paperless"]
fy = Inches(4.05)
for i, f in enumerate(feats):
    r = i // 3
    c = i % 3
    x = Inches(8.55) + c*Inches(1.28)
    y = fy + r*Inches(0.34)
    shape(slide, x, y, Inches(1.22), Inches(0.28), fill=BG_CARD, line=BORDER, radius=True)
    textbox(slide, x, y+Inches(0.04), Inches(1.22), Inches(0.20), "✓  " + f, 7, TEXT, align=PP_ALIGN.CENTER)
shape(slide, Inches(8.55), Inches(4.85), Inches(3.9), Inches(0.55), fill=BG_CARD, line=BORDER, radius=True)
textbox(slide, Inches(8.55), Inches(4.90), Inches(3.9), Inches(0.20), "LIVE NOW →  localhost:8001  •  /  •  /mines/  •  /api/docs/  •  /health/", 7, ACCENT, align=PP_ALIGN.CENTER)
textbox(slide, Inches(8.55), Inches(5.12), Inches(3.9), Inches(0.20), "Run:  start_coalguard.bat  or  run_local.bat  (no Docker)", 7, MUTED, align=PP_ALIGN.CENTER)
textbox(slide, Inches(0.7), Inches(6.95), Inches(11.9), Inches(0.20), "Team CoalGuard  •  Built for SIH 2026  •  Dataset: shitalgaikwad123/indian-coal-mines-dataset-january-20211 (Kaggle)  •  10 • 20 • 30  — 10 slides • 20 min • 30pt clarity", 7, RGBColor(90,107,125), align=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 1 — 2 min: Introduce CoalGuard as direct answer to PSID 26024. Point to live screenshot on right (real dashboard). Highlight 459 mines scale. Set expectation: live demo included."

# ===== SLIDE 2: PROBLEM =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(4), fill=CRITICAL)
textbox(slide, Inches(0.7), Inches(0.40), Inches(4), Inches(0.25), "02 — THE PROBLEM", 9, CRITICAL, bold=True)
textbox(slide, Inches(0.7), Inches(0.70), Inches(11.9), Inches(0.50), "Coal Governance Today: Fragmented, Delayed, Opaque", 28, WHITE, bold=True)
textbox(slide, Inches(0.7), Inches(1.22), Inches(11.9), Inches(0.35), "Operations across subsidiaries, mines, contractors & regulators still run on spreadsheets, paper & siloed reports — creating gaps HQ only discovers at audit.", 13, MUTED)
# 6 challenges - larger fonts, 2x3 grid but with bigger cards
chals = [
    ("Data\nInconsistency", "Multiple versions of truth", CRITICAL),
    ("Delayed\nDecisions", "Days-weeks field → HQ lag", CRITICAL),
    ("Limited\nTransparency", "No real-time view for regulators", CRITICAL),
    ("Compliance\nGaps", "Missed due dates, weak follow-up", CRITICAL),
    ("Duplication", "Repeated manual entry", MUTED),
    ("Weak Field\nMonitoring", "Unverifiable field reports", MUTED),
]
for i, (title, desc, col) in enumerate(chals):
    r = i // 3
    c = i % 3
    x = Inches(0.7) + c*Inches(4.1)
    y = Inches(1.75) + r*Inches(1.35)
    shape(slide, x, y, Inches(3.9), Inches(1.15), fill=BG_PANEL, line=col, lw=1.2, radius=True)
    # number
    circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, x+Inches(0.18), y+Inches(0.20), Inches(0.42), Inches(0.42))
    circ.fill.solid()
    circ.fill.fore_color.rgb = col
    circ.line.fill.background()
    textbox(slide, x+Inches(0.18), y+Inches(0.24), Inches(0.42), Inches(0.34), str(i+1), 14, WHITE, bold=True, align=PP_ALIGN.CENTER)
    textbox(slide, x+Inches(0.70), y+Inches(0.14), Inches(3.0), Inches(0.50), title, 13, WHITE, bold=True)
    textbox(slide, x+Inches(0.70), y+Inches(0.66), Inches(3.0), Inches(0.30), desc, 11, MUTED)
# Scale panel bottom
shape(slide, Inches(0.7), Inches(4.70), Inches(12.0), Inches(2.05), fill=BG_PANEL, line=BORDER, radius=True)
textbox(slide, Inches(0.9), Inches(4.85), Inches(11.6), Inches(0.22), "SCALE OF REAL DATA WE INGESTED  •  Indian Coal Mines Dataset — Jan 2021 (Kaggle via kagglehub)", 8, ACCENT, bold=True)
stats2 = [("459", "Mines"), ("12", "States"), ("52", "Districts"), ("37", "Owners"), ("459", "Geocoded"), ("200", "Demo Seeded")]
sx = Inches(0.9)
for v,l in stats2:
    shape(slide, sx, Inches(5.15), Inches(1.75), Inches(0.65), fill=BG_DARK, line=BORDER, radius=True)
    textbox(slide, sx, Inches(5.20), Inches(1.75), Inches(0.35), v, 20, ACCENT, bold=True, align=PP_ALIGN.CENTER)
    textbox(slide, sx, Inches(5.50), Inches(1.75), Inches(0.22), l, 8, MUTED, align=PP_ALIGN.CENTER)
    sx += Inches(1.92)
textbox(slide, Inches(0.9), Inches(5.95), Inches(11.6), Inches(0.45), "Result →  Data inconsistency  •  Duplication  •  Compliance gaps undetected  •  Corrective actions slip overdue  •  HQ blindsided until escalation. PSID 26024 asks for an integrated smart governance platform to fix exactly this.", 10, MUTED)
textbox(slide, Inches(0.7), Inches(6.85), Inches(11.9), Inches(0.20), "“Need for integrated smart governance… transparency, accountability, sustainability & digital governance.” — PSID 26024, Ministry of Coal / CIL", 9, MUTED, italic=True, align=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 2 — 2 min: Diagnose pain with 6 challenges. Ground in real data scale (459-row Kaggle). Emphasize manual/paper root cause."

# ===== SLIDE 3: SOLUTION =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(4), fill=ACCENT)
textbox(slide, Inches(0.7), Inches(0.40), Inches(4), Inches(0.25), "03 — OUR SOLUTION", 9, ACCENT, bold=True)
textbox(slide, Inches(0.7), Inches(0.70), Inches(11.9), Inches(0.50), "CoalGuard — One Ecosystem, Zero Silos", 28, WHITE, bold=True)
textbox(slide, Inches(0.7), Inches(1.22), Inches(11.9), Inches(0.35), "Centralized, AI-enabled platform that integrates every mine-level activity into a single paperless, real-time command centre — from field capture to Ministry dashboard.", 13, MUTED)
# Core
shape(slide, Inches(5.45), Inches(1.95), Inches(2.4), Inches(1.35), fill=ACCENT, radius=True)
textbox(slide, Inches(5.45), Inches(2.15), Inches(2.4), Inches(0.35), "CoalGuard", 22, BG_DARK, bold=True, align=PP_ALIGN.CENTER)
textbox(slide, Inches(5.45), Inches(2.50), Inches(2.4), Inches(0.35), "Central Platform", 12, BG_DARK, align=PP_ALIGN.CENTER)
textbox(slide, Inches(5.45), Inches(2.85), Inches(2.4), Inches(0.20), "Django 5.1  •  Postgres 17  •  Redis 7", 7, RGBColor(30,60,90), align=PP_ALIGN.CENTER)
pillars = [
    ("Compliance\nTracking", "Safety / Env / Labour / Prod", Inches(2.2), Inches(1.85), ACCENT2),
    ("Inspections &\nObservations", "Geo-tagged • Photo • Severity", Inches(8.7), Inches(1.85), HIGH),
    ("Corrective\nActions", "Owner • Priority • Verify", Inches(1.2), Inches(3.55), CRITICAL),
    ("Field Mobile\nSync", "Offline • client_id • Photo", Inches(9.9), Inches(3.55), ACCENT),
    ("GIS &\nDashboards", "Leaflet • Chart.js • Risk", Inches(5.6), Inches(3.65), MEDIUM),
]
for t, sub, x, y, col in pillars:
    shape(slide, x, y, Inches(1.85), Inches(1.15), fill=BG_PANEL, line=col, lw=1.2, radius=True)
    textbox(slide, x, y+Inches(0.14), Inches(1.85), Inches(0.42), t, 11, WHITE, bold=True, align=PP_ALIGN.CENTER)
    textbox(slide, x, y+Inches(0.62), Inches(1.85), Inches(0.35), sub, 8, MUTED, align=PP_ALIGN.CENTER)
# Workflow steps bottom
textbox(slide, Inches(0.7), Inches(5.15), Inches(11.9), Inches(0.22), "FIELD  →  PLATFORM  →  HQ  — Every step geo-tagged, time-stamped, hash-audited", 9, ACCENT, bold=True, align=PP_ALIGN.CENTER)
flows = ["Field\nInspection", "Observation\nby Severity", "Corrective\nAction", "Auto\nEscalation", "Dashboards\n& Reports", "Blockchain\nAudit"]
fx = Inches(0.7)
for i, f in enumerate(flows):
    shape(slide, fx, Inches(5.45), Inches(1.85), Inches(0.75), fill=BG_PANEL, line=BORDER, radius=True)
    circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, fx+Inches(0.70), Inches(5.52), Inches(0.42), Inches(0.42))
    circ.fill.solid(); circ.fill.fore_color.rgb = ACCENT; circ.line.fill.background()
    textbox(slide, fx+Inches(0.70), Inches(5.58), Inches(0.42), Inches(0.30), str(i+1), 10, BG_DARK, bold=True, align=PP_ALIGN.CENTER)
    textbox(slide, fx, Inches(5.98), Inches(1.85), Inches(0.40), f, 8, MUTED, align=PP_ALIGN.CENTER)
    if i<5:
        textbox(slide, fx+Inches(1.85), Inches(5.78), Inches(0.30), Inches(0.20), "→", 14, MUTED, align=PP_ALIGN.CENTER)
    fx+=Inches(2.05)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 3 — 1.5 min: Position as unified answer. Walk 5 pillars and field→HQ flow. Stress paperless + real-time."

# ===== SLIDE 4: ARCHITECTURE =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(4), fill=ACCENT)
textbox(slide, Inches(0.7), Inches(0.40), Inches(4), Inches(0.25), "04 — HOW WE BUILT IT", 9, ACCENT, bold=True)
textbox(slide, Inches(0.7), Inches(0.70), Inches(11.9), Inches(0.50), "Architecture — Local-First, Production-Ready", 28, WHITE, bold=True)
# Left architecture card
shape(slide, Inches(0.7), Inches(1.35), Inches(7.6), Inches(4.35), fill=BG_PANEL, line=BORDER, radius=True)
textbox(slide, Inches(0.9), Inches(1.50), Inches(7.2), Inches(0.22), "SYSTEM ARCHITECTURE — Browser / Mobile → Django → Redis / Postgres", 8, ACCENT, bold=True)
shape(slide, Inches(0.9), Inches(1.85), Inches(7.2), Inches(0.55), fill=BG_DARK, line=BORDER, radius=True)
textbox(slide, Inches(0.9), Inches(1.95), Inches(7.2), Inches(0.35), "Browser / Mobile  —  Dashboard (Chart.js + Leaflet)  •  Swagger UI  •  Field Capture", 9, MUTED, align=PP_ALIGN.CENTER)
shape(slide, Inches(0.9), Inches(2.65), Inches(3.45), Inches(1.05), fill=BG_CARD, line=ACCENT, lw=1.2, radius=True)
textbox(slide, Inches(0.9), Inches(2.78), Inches(3.45), Inches(0.22), "Django 5.1 + Gunicorn", 10, WHITE, bold=True, align=PP_ALIGN.CENTER)
textbox(slide, Inches(0.9), Inches(3.02), Inches(3.45), Inches(0.48), "Whitenoise  •  RBAC 6 roles\nJWT (mobile) + Session (web)", 8, MUTED, align=PP_ALIGN.CENTER)
shape(slide, Inches(4.65), Inches(2.65), Inches(3.45), Inches(1.05), fill=BG_CARD, line=ACCENT2, lw=1.2, radius=True)
textbox(slide, Inches(4.65), Inches(2.78), Inches(3.45), Inches(0.22), "DRF + JWT API  •  /api/*", 10, WHITE, bold=True, align=PP_ALIGN.CENTER)
textbox(slide, Inches(4.65), Inches(3.02), Inches(3.45), Inches(0.48), "Filter • Throttle • Swagger\nclient_id idempotent sync", 8, MUTED, align=PP_ALIGN.CENTER)
shape(slide, Inches(0.9), Inches(3.85), Inches(7.2), Inches(0.02), fill=BORDER)
textbox(slide, Inches(0.9), Inches(3.92), Inches(7.2), Inches(0.20), "config/celery.py  •  Celery Beat (hourly / nightly)", 8, ACCENT, align=PP_ALIGN.CENTER)
shape(slide, Inches(1.05), Inches(4.18), Inches(3.2), Inches(0.65), fill=BG_DARK, line=BORDER, radius=True)
textbox(slide, Inches(1.05), Inches(4.24), Inches(3.2), Inches(0.20), "Celery Worker", 9, WHITE, bold=True, align=PP_ALIGN.CENTER)
textbox(slide, Inches(1.05), Inches(4.45), Inches(3.2), Inches(0.30), "check_overdue_compliance", 7, MUTED, align=PP_ALIGN.CENTER)
shape(slide, Inches(4.15), Inches(4.18), Inches(3.2), Inches(0.65), fill=BG_DARK, line=BORDER, radius=True)
textbox(slide, Inches(4.15), Inches(4.24), Inches(3.2), Inches(0.20), "Celery Beat", 9, WHITE, bold=True, align=PP_ALIGN.CENTER)
textbox(slide, Inches(4.15), Inches(4.45), Inches(3.2), Inches(0.30), "Hourly PENDING→OVERDUE", 7, MUTED, align=PP_ALIGN.CENTER)
shape(slide, Inches(0.9), Inches(4.95), Inches(7.2), Inches(0.50), fill=BG_DARK, line=BORDER, radius=True)
textbox(slide, Inches(0.9), Inches(5.05), Inches(7.2), Inches(0.30), "Postgres 17  •  Redis 7  —  mines • compliance • inspections • audit (hash-chained) • contractors • docs", 7, MUTED, align=PP_ALIGN.CENTER)
# Right stack
shape(slide, Inches(8.6), Inches(1.35), Inches(4.0), Inches(4.35), fill=BG_PANEL, line=BORDER, radius=True)
textbox(slide, Inches(8.8), Inches(1.50), Inches(3.6), Inches(0.22), "STACK — Explainability > Hype", 8, ACCENT, bold=True)
stack = [
    ("Backend", "Django 5.1 • DRF • JWT\ndrf-spectacular"),
    ("DB/Queue", "Postgres 17 • Redis 7\nCelery 5.4 + Gunicorn"),
    ("Analytics", "risk.py weighted sum\nanomaly.py z-score"),
    ("GIS/OCR", "Leaflet 1.9 • GeoJSON\nTesseract + reportlab"),
    ("Frontend", "Templates + Chart.js 4.4\nDark • Responsive"),
    ("Infra", "Docker Compose\n• .env • healthcheck"),
]
y = Inches(1.80)
for k,v in stack:
    shape(slide, Inches(8.8), y, Inches(3.6), Inches(0.60), fill=BG_DARK, line=BORDER, radius=True)
    textbox(slide, Inches(8.85), y+Inches(0.08), Inches(1.10), Inches(0.20), k, 8, ACCENT, bold=True)
    textbox(slide, Inches(9.95), y+Inches(0.08), Inches(1.40), Inches(0.44), v, 7, MUTED)
    y+=Inches(0.65)
# Footer highlights - larger fonts
shape(slide, Inches(0.7), Inches(5.95), Inches(11.9), Inches(1.05), fill=BG_PANEL, line=BORDER, radius=True)
highs = [("Dual-Stack", "localhost works on IPv6"), ("No Hard Paths", "Move folder → works"), ("One-Click", "start_coalguard.bat"), ("No-Docker", "run_local.bat + SQLite"), ("Configurable", "WEB_PORT via .env")]
hx = Inches(0.9)
for t,d in highs:
    textbox(slide, hx, Inches(6.10), Inches(2.1), Inches(0.22), t, 9, WHITE, bold=True, align=PP_ALIGN.CENTER)
    textbox(slide, hx, Inches(6.35), Inches(2.1), Inches(0.40), d, 8, MUTED, align=PP_ALIGN.CENTER)
    hx+=Inches(2.30)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 4 — 2 min: Explain local-first, dual-stack fix, Celery hourly jobs. Boring-tech for reliability."

# ===== SLIDE 5: PS MAPPING =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(4), fill=ACCENT2)
textbox(slide, Inches(0.7), Inches(0.40), Inches(5), Inches(0.25), "05 — COMPLETE COVERAGE", 9, ACCENT2, bold=True)
textbox(slide, Inches(0.7), Inches(0.70), Inches(11.9), Inches(0.50), "Every PS Requirement → Built & Traceable", 28, WHITE, bold=True)
textbox(slide, Inches(0.7), Inches(1.22), Inches(11.9), Inches(0.25), "No hand-waving — each row maps to concrete models, APIs and live execution.", 11, MUTED)
# Header
cols = [(Inches(0.7), Inches(3.3), "PS REQUIREMENT"), (Inches(4.1), Inches(6.0), "HOW COALGUARD IMPLEMENTS"), (Inches(10.3), Inches(2.3), "WHERE IN CODE")]
for x,w,t in cols:
    shape(slide, x, Inches(1.55), w, Inches(0.38), fill=BG_CARD, line=BORDER, radius=True)
    textbox(slide, x, Inches(1.62), w, Inches(0.24), t, 8, MUTED, bold=True, align=PP_ALIGN.CENTER)
rows = [
    ("Statutory compliance\nSAFETY/ENV/PROD/LABOUR", "ComplianceRequirement + Record\nPENDING→OVERDUE/ESCALATED + PDF", "apps/compliance/\nmodels.py"),
    ("Real-time monitoring\nviolations & actions", "Inspection + Observation (LOW→CRIT)\n+ CorrectiveAction verify/close", "apps/inspections/\nmodels.py"),
    ("AI for risk &\nrecurring failures", "Weighted risk + z-score + freq.\nExplainable, no black-box", "apps/analytics/\nrisk.py"),
    ("Geo-tagged field\nreporting + offline", "lat/lon/accuracy + client_id\nphoto + idempotent sync", "apps/inspections/\nserializers.py"),
    ("Role dashboards\nmine/corp/regulator", "RBAC 6 roles + Leaflet + Chart.js\nPer-role filtering", "apps/accounts/\nmodels.py"),
    ("Alerts, reminders\nescalations", "Notification + AlertRule + Beat\nhourly overdue & escalate", "apps/notifications/\ntasks.py"),
    ("Paperless + OCR\n+ audit trail", "Document OCR + PDF/CSV\nSHA256 hash-chained AuditLog", "apps/documents/\nocr.py"),
    ("Scalable across\nmines/subsidiaries", "Subsidiary scoping + bulk import\nContainerized, PostGIS-ready", "apps/mines/\nmodels.py"),
]
y = Inches(2.00)
for req, imp, code in rows:
    shape(slide, Inches(0.7), y, Inches(3.3), Inches(0.58), fill=BG_PANEL, line=BORDER, radius=True)
    textbox(slide, Inches(0.75), y+Inches(0.08), Inches(3.2), Inches(0.42), req, 8, WHITE)
    shape(slide, Inches(4.1), y, Inches(6.0), Inches(0.58), fill=BG_PANEL, line=BORDER, radius=True)
    textbox(slide, Inches(4.15), y+Inches(0.08), Inches(5.9), Inches(0.42), imp, 8, MUTED)
    shape(slide, Inches(10.3), y, Inches(2.3), Inches(0.58), fill=BG_DARK, line=BORDER, radius=True)
    textbox(slide, Inches(10.35), y+Inches(0.08), Inches(2.2), Inches(0.42), code, 7, ACCENT, name="Consolas")
    y+=Inches(0.63)
shape(slide, Inches(0.7), Inches(7.15), Inches(11.9), Inches(0.35), fill=RGBColor(22,40,28), line=ACCENT2, radius=True)
textbox(slide, Inches(0.7), Inches(7.22), Inches(11.9), Inches(0.22), "✓  All 8 capabilities live today — verified via running app, API tests and code walkthrough.", 10, ACCENT2, bold=True, align=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 5 — 1.5 min: Prove completeness row by row. Reference exact files."

# ===== SLIDE 6: LIVE DASHBOARD SCREENSHOT =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(4), fill=ACCENT)
textbox(slide, Inches(0.7), Inches(0.40), Inches(5), Inches(0.25), "06 — LIVE PLATFORM DEMO", 9, ACCENT, bold=True)
textbox(slide, Inches(0.7), Inches(0.70), Inches(11.9), Inches(0.50), "Dashboard — Real Screenshot (Not a Mockup)", 26, WHITE, bold=True)
textbox(slide, Inches(0.7), Inches(1.18), Inches(11.9), Inches(0.25), "Captured from running app at http://127.0.0.1:8001/  •  Dark theme, real data, live APIs", 10, MUTED, italic=True)
# Large screenshot - viewport 16:9 fits nicely
if dash_authed.exists():
    img_path = dash_authed
else:
    img_path = dash_top
# Container 16:9 -> width 11.9 height 6.69 at 16:9 but slide leaves 0.7 margin; use height 5.3 to leave caption
shape(slide, Inches(0.7), Inches(1.55), Inches(11.9), Inches(5.30), fill=BG_PANEL, line=BORDER, radius=True)
# add image covering exactly
slide.shapes.add_picture(str(img_path), Inches(0.72), Inches(1.57), width=Inches(11.86), height=Inches(5.26))
# Caption bar below image
shape(slide, Inches(0.7), Inches(6.90), Inches(11.9), Inches(0.40), fill=BG_PANEL, line=BORDER, radius=True)
textbox(slide, Inches(0.7), Inches(6.95), Inches(11.9), Inches(0.30), "8 KPIs  •  Leaflet GIS (459 mines color-coded by risk)  •  4 Chart.js analytics  •  AI anomaly tables  •  Real-time via /api/dashboard/*", 9, MUTED, align=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 6 — 2.5 min: LIVE demo. If possible switch to browser. Narrate KPIs, map colors, charts. Highlight this is real screenshot from viewport, not Figma."

# ===== SLIDE 7: MINE REGISTRY SCREENSHOT =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(4), fill=ACCENT)
textbox(slide, Inches(0.7), Inches(0.40), Inches(5), Inches(0.25), "07 — MINE REGISTRY + DETAIL", 9, ACCENT, bold=True)
textbox(slide, Inches(0.7), Inches(0.70), Inches(11.9), Inches(0.50), "Registry & Detail — Real Screenshots", 26, WHITE, bold=True)
textbox(slide, Inches(0.7), Inches(1.18), Inches(6), Inches(0.25), "Filter, sort, risk badge, CSV export — all live.", 10, MUTED, italic=True)
textbox(slide, Inches(7.0), Inches(1.18), Inches(5.6), Inches(0.25), "Click any mine → risk breakdown + compliance + observations", 10, MUTED, italic=True, align=PP_ALIGN.RIGHT)
# Two screenshots side by side, but make them large
shape(slide, Inches(0.7), Inches(1.55), Inches(7.8), Inches(5.00), fill=BG_PANEL, line=BORDER, radius=True)
if mines_vp.exists():
    slide.shapes.add_picture(str(mines_vp), Inches(0.72), Inches(1.57), width=Inches(7.76), height=Inches(4.36))
else:
    textbox(slide, Inches(0.7), Inches(3.5), Inches(7.8), Inches(0.5), "Mine list screenshot missing", 10, MUTED, align=PP_ALIGN.CENTER)
textbox(slide, Inches(0.7), Inches(6.00), Inches(7.8), Inches(0.40), "Mine Registry — Search + 5 filters (state, coal type, mine type, risk, per-page) • Sortable • CSV", 8, ACCENT, align=PP_ALIGN.CENTER)
shape(slide, Inches(8.8), Inches(1.55), Inches(3.8), Inches(5.00), fill=BG_PANEL, line=BORDER, radius=True)
if detail_vp.exists():
    slide.shapes.add_picture(str(detail_vp), Inches(8.82), Inches(1.57), width=Inches(3.76), height=Inches(2.11))
    # add second smaller caption for detail: maybe show cropped compliance part if needed - use same image but zoomed? We'll just place same but add overlay text
    shape(slide, Inches(8.82), Inches(3.80), Inches(3.76), Inches(1.65), fill=BG_DARK, line=BORDER, radius=True)
    textbox(slide, Inches(8.90), Inches(3.85), Inches(3.60), Inches(0.25), "Mine Detail: Risk Components", 8, WHITE, bold=True)
    textbox(slide, Inches(8.90), Inches(4.10), Inches(3.60), Inches(1.20), "• Risk score 0-100 + level LOW→CRITICAL\n• Safety / Compliance / Contractor / Incident breakdown\n• Compliance records + inspections + observations list\n• Geo-tag + subsidiary scoping", 7, MUTED)
else:
    textbox(slide, Inches(8.8), Inches(3.5), Inches(3.8), Inches(0.5), "Detail screenshot missing", 10, MUTED, align=PP_ALIGN.CENTER)
textbox(slide, Inches(8.8), Inches(6.00), Inches(3.8), Inches(0.40), "Detail View — /mines/<id>/", 8, ACCENT, align=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 7 — 1.5 min: Show registry filtering and drill-down. Mention Real/Synthetic tag and is_synthetic flag."

# ===== SLIDE 8: AI ENGINE =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(4), fill=ACCENT2)
textbox(slide, Inches(0.7), Inches(0.40), Inches(5), Inches(0.25), "08 — INTELLIGENCE AT CORE", 9, ACCENT2, bold=True)
textbox(slide, Inches(0.7), Inches(0.70), Inches(11.9), Inches(0.50), "Explainable AI — No Black Box", 26, WHITE, bold=True)
# Formula card left
shape(slide, Inches(0.7), Inches(1.45), Inches(5.8), Inches(2.05), fill=BG_PANEL, line=BORDER, radius=True)
textbox(slide, Inches(0.9), Inches(1.60), Inches(5.4), Inches(0.22), "RISK FORMULA — apps/analytics/risk.py:35", 8, ACCENT, bold=True)
shape(slide, Inches(0.9), Inches(1.90), Inches(5.4), Inches(0.80), fill=BG_DARK, line=BORDER, radius=True)
textbox(slide, Inches(0.9), Inches(2.00), Inches(5.4), Inches(0.60), "risk =  safety×0.35  +  compliance×0.30  +  contractor×0.15  +  incident×0.20", 13, ACCENT, bold=True, align=PP_ALIGN.CENTER)
textbox(slide, Inches(0.9), Inches(2.55), Inches(5.4), Inches(0.20), "All 0-100 (higher = safer)  •  Floored & rounded  •  Recomputable on demand", 8, MUTED, align=PP_ALIGN.CENTER)
# Components 2x2 grid larger fonts
comps = [
    ("Safety", "100 − open obs penalties\nLOW -2  MED -5  HIGH -12  CRIT -25", LOW),
    ("Compliance", "COMPLIANT / determinable ×100\nNo data → 50 neutral", ACCENT),
    ("Contractor", "Baseline 70 ± hash(subsidiary)\nWeakest → Phase 2 real data", MEDIUM),
    ("Incident", "100 − OPEN×5 − IP×3 − OVERDUE×15", CRITICAL),
]
cx = Inches(0.9)
cy = Inches(2.85)
for i, (t, dsc, col) in enumerate(comps):
    x = Inches(0.9) + (i%2)*Inches(2.85)
    y = Inches(2.80) + (i//2)*Inches(0.95)
    shape(slide, x, y, Inches(2.75), Inches(0.80), fill=BG_DARK, line=col, lw=1.2, radius=True)
    textbox(slide, x, y+Inches(0.08), Inches(2.75), Inches(0.22), t, 11, col, bold=True, align=PP_ALIGN.CENTER)
    textbox(slide, x, y+Inches(0.32), Inches(2.75), Inches(0.40), dsc, 8, MUTED, align=PP_ALIGN.CENTER)
# Bands
shape(slide, Inches(0.9), Inches(4.80), Inches(5.4), Inches(0.35), fill=BG_DARK, line=BORDER, radius=True)
textbox(slide, Inches(0.9), Inches(4.85), Inches(5.4), Inches(0.25), "LOW 80-100   •   MEDIUM 60-80   •   HIGH 40-60   •   CRITICAL 0-40", 9, MUTED, align=PP_ALIGN.CENTER)
# Right: live distribution screenshot (use mid viewport which shows charts)
shape(slide, Inches(6.8), Inches(1.45), Inches(5.8), Inches(3.70), fill=BG_PANEL, line=BORDER, radius=True)
textbox(slide, Inches(7.0), Inches(1.60), Inches(5.4), Inches(0.22), "LIVE DISTRIBUTION — Real Dashboard Analytics (cropped)", 8, ACCENT2, bold=True)
if dash_mid.exists():
    slide.shapes.add_picture(str(dash_mid), Inches(7.0), Inches(1.90), width=Inches(5.4), height=Inches(3.04))
else:
    shape(slide, Inches(7.0), Inches(1.90), Inches(5.4), Inches(3.04), fill=BG_DARK, line=BORDER)
    textbox(slide, Inches(7.0), Inches(3.2), Inches(5.4), Inches(0.4), "Dashboard analytics screenshot", 9, MUTED, align=PP_ALIGN.CENTER)
# Anomaly bottom
shape(slide, Inches(6.8), Inches(5.30), Inches(5.8), Inches(1.50), fill=BG_PANEL, line=BORDER, radius=True)
textbox(slide, Inches(7.0), Inches(5.45), Inches(5.4), Inches(0.22), "ANOMALY DETECTION — apps/analytics/anomaly.py", 8, ACCENT, bold=True)
add_bullets(slide, Inches(7.0), Inches(5.70), Inches(5.4), Inches(0.95), ["Flag if open_obs > mean + 2σ", "Or overdue CorrectiveActions ≥ 3", "Recurring failures by (OVERDUE+ESCALATED)/total"], size=9, color=MUTED)
shape(slide, Inches(0.7), Inches(6.85), Inches(11.9), Inches(0.35), fill=BG_DARK, line=BORDER, radius=True)
textbox(slide, Inches(0.7), Inches(6.90), Inches(11.9), Inches(0.25), "Snapshot: 458 scored • Avg 84.4 • 295 LOW • 157 MEDIUM • 6 HIGH  —  Run: python manage.py recompute_risk", 8, MUTED, align=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 8 — 2 min: Explain formula and why explainable matters for regulators. Show real charts from dashboard mid viewport."

# ===== SLIDE 9: WORKFLOW + API SCREENSHOT =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(4), fill=HIGH)
textbox(slide, Inches(0.7), Inches(0.40), Inches(5), Inches(0.25), "09 — FIELD TO HQ + API", 9, HIGH, bold=True)
textbox(slide, Inches(0.7), Inches(0.70), Inches(8), Inches(0.50), "Workflow & Paperless Governance", 26, WHITE, bold=True)
# Workflow steps top
steps = [
    ("Inspection\nGeo-tag + Photo", "client_id\nidempotent", ACCENT),
    ("Observation\nLOW→CRIT", "Category\nStatus", HIGH),
    ("Corrective\nAction", "Owner • Due\nVerify", CRITICAL),
    ("Auto\nEscalation", "Hourly Beat\nAlertRule", CRITICAL),
    ("Dashboard\n& Reports", "PDF • CSV\nPer-role", ACCENT2),
    ("Blockchain\nAudit", "SHA256 chain\nVerify API", RGBColor(168,85,247)),
]
fx = Inches(0.7)
for i, (t, dsc, col) in enumerate(steps):
    shape(slide, fx, Inches(1.45), Inches(1.85), Inches(1.05), fill=BG_PANEL, line=col, lw=1.2, radius=True)
    circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, fx+Inches(0.70), Inches(1.55), Inches(0.42), Inches(0.42))
    circ.fill.solid(); circ.fill.fore_color.rgb = col; circ.line.fill.background()
    textbox(slide, fx+Inches(0.70), Inches(1.61), Inches(0.42), Inches(0.30), str(i+1), 10, WHITE, bold=True, align=PP_ALIGN.CENTER)
    textbox(slide, fx, Inches(2.02), Inches(1.85), Inches(0.28), t, 8, WHITE, bold=True, align=PP_ALIGN.CENTER)
    textbox(slide, fx, Inches(2.32), Inches(1.85), Inches(0.30), dsc, 7, MUTED, align=PP_ALIGN.CENTER)
    if i<5:
        textbox(slide, fx+Inches(1.85), Inches(1.95), Inches(0.28), Inches(0.20), "→", 12, MUTED, align=PP_ALIGN.CENTER)
    fx+=Inches(2.05)
# Bottom: API screenshot large
shape(slide, Inches(0.7), Inches(2.75), Inches(7.2), Inches(4.35), fill=BG_PANEL, line=BORDER, radius=True)
textbox(slide, Inches(0.9), Inches(2.90), Inches(6.8), Inches(0.22), "API DOCS — REAL SWAGGER UI at /api/docs/  •  JWT + Session • Filter • Throttle", 8, ACCENT, bold=True)
if api_vp.exists():
    slide.shapes.add_picture(str(api_vp), Inches(0.9), Inches(3.18), width=Inches(6.8), height=Inches(3.82))
else:
    shape(slide, Inches(0.9), Inches(3.18), Inches(6.8), Inches(3.82), fill=BG_DARK, line=BORDER)
# Features card right
shape(slide, Inches(8.2), Inches(2.75), Inches(4.4), Inches(4.35), fill=BG_PANEL, line=BORDER, radius=True)
textbox(slide, Inches(8.4), Inches(2.90), Inches(4.0), Inches(0.22), "PAPERLESS & GOVERNANCE FEATURES", 8, ACCENT, bold=True)
feats = [
    "Document OCR — pytesseract (eng+hin) + confidence",
    "PDF via reportlab + CSV export per mine",
    "Blockchain AuditLog — previous_hash + SHA256",
    "Verify at /api/audit/verify/  •  append-only admin",
    "RBAC 6 roles — ADMIN/REGULATOR/CORP/INSPECTOR...",
    "Notifications — AlertRule + hourly Celery",
    "Multilingual — en/hi/bn/te/mr/ta + locale",
    "Offline sync — client_id, photo, accuracy_m",
]
add_bullets(slide, Inches(8.4), Inches(3.15), Inches(4.0), Inches(3.80), feats, size=8, color=MUTED)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 9 — 1.5 min: Walk lifecycle. Show Swagger is live, not diagram. Emphasize paperless + audit + OCR."

# ===== SLIDE 10: IMPACT & ROADMAP =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(4), fill=ACCENT)
textbox(slide, Inches(0.7), Inches(0.40), Inches(5), Inches(0.25), "10 — IMPACT & NEXT", 9, ACCENT, bold=True)
textbox(slide, Inches(0.7), Inches(0.70), Inches(11.9), Inches(0.50), "Ready Today. Scalable Tomorrow.", 28, WHITE, bold=True)
# Before/After
shape(slide, Inches(0.7), Inches(1.35), Inches(5.85), Inches(2.20), fill=BG_PANEL, line=CRITICAL, radius=True)
textbox(slide, Inches(0.9), Inches(1.50), Inches(5.45), Inches(0.22), "BEFORE — Manual, Siloed", 9, CRITICAL, bold=True)
add_bullets(slide, Inches(0.9), Inches(1.75), Inches(5.45), Inches(1.65), ["Spreadsheets & paper files", "Days-weeks reporting lag", "Gaps found only at audit", "Field unverifiable", "Gut-feel decisions"], size=9, color=MUTED)
shape(slide, Inches(7.0), Inches(1.35), Inches(5.6), Inches(2.20), fill=BG_PANEL, line=ACCENT2, radius=True)
textbox(slide, Inches(7.2), Inches(1.50), Inches(5.2), Inches(0.22), "AFTER — CoalGuard Unified", 9, ACCENT2, bold=True)
add_bullets(slide, Inches(7.2), Inches(1.75), Inches(5.2), Inches(1.65), ["Single source of truth + audit trail", "Real-time KPIs + hourly escalations", "Overdue auto-flag → notified → escalated", "Every report geo/time/photo/hash", "Risk-ranked, data-driven priorities"], size=9, color=TEXT)
# KPIs impact
kpis = [("real-time", "Reporting", ACCENT), ("70% ↓", "Paperwork*", ACCENT2), ("459", "Mines mapped", WHITE), ("6", "High-risk flagged", HIGH), ("100%", "Audit verifiable", ACCENT)]
kx = Inches(0.7)
for v,lbl,col in kpis:
    shape(slide, kx, Inches(3.75), Inches(2.15), Inches(0.75), fill=BG_PANEL, line=col, lw=1.2, radius=True)
    textbox(slide, kx, Inches(3.82), Inches(2.15), Inches(0.35), v, 16, col, bold=True, align=PP_ALIGN.CENTER)
    textbox(slide, kx, Inches(4.18), Inches(2.15), Inches(0.20), lbl, 7, MUTED, align=PP_ALIGN.CENTER)
    kx+=Inches(2.35)
textbox(slide, Inches(0.7), Inches(4.60), Inches(11.9), Inches(0.15), "*projected vs manual baseline — architecture is what scales; data is pluggable.", 7, RGBColor(90,107,125), align=PP_ALIGN.CENTER)
# Roadmap + Run
shape(slide, Inches(0.7), Inches(4.85), Inches(5.85), Inches(2.15), fill=BG_PANEL, line=BORDER, radius=True)
textbox(slide, Inches(0.9), Inches(5.00), Inches(5.45), Inches(0.22), "HOW TO RUN — One-Click, No Cloud", 8, ACCENT, bold=True)
textbox(slide, Inches(0.9), Inches(5.25), Inches(5.45), Inches(0.30), "1  Double-click  start_coalguard.bat  → builds, migrates, seeds, opens browser", 8, WHITE, name="Consolas")
textbox(slide, Inches(0.9), Inches(5.55), Inches(5.45), Inches(0.30), "2  Browse  http://127.0.0.1:8001/  •  /mines/  •  /api/docs/  •  /health/", 8, WHITE, name="Consolas")
textbox(slide, Inches(0.9), Inches(5.85), Inches(5.45), Inches(0.30), "3  Login  admin/Admin@123  •  inspector/Inspector@123  •  regulator/Regulator@123", 7, MUTED, name="Consolas")
textbox(slide, Inches(0.9), Inches(6.15), Inches(5.45), Inches(0.30), "No-Docker:  run_local.bat  → .venv + SQLite + sync Celery", 7, ACCENT, name="Consolas")
shape(slide, Inches(7.0), Inches(4.85), Inches(5.6), Inches(2.15), fill=BG_PANEL, line=BORDER, radius=True)
textbox(slide, Inches(7.2), Inches(5.00), Inches(5.2), Inches(0.22), "ROADMAP — Post-MVP (Out of Scope)", 8, HIGH, bold=True)
add_bullets(slide, Inches(7.2), Inches(5.25), Inches(5.2), Inches(1.40), ["PostGIS + GeoDjango heatmap & radius search", "ML classifier replaces weighted formula", "PWA + WatermelonDB background sync", "Multilingual LLM/RAG over compliance corpus"], size=8, color=MUTED)
# Closing
shape(slide, Inches(0.7), Inches(7.15), Inches(11.9), Inches(0.25), fill=ACCENT, radius=True)
textbox(slide, Inches(0.7), Inches(7.18), Inches(11.9), Inches(0.20), "CoalGuard is Ready to Deploy — Not Slideware.  Thank You — Questions & Live Demo at localhost:8001", 10, BG_DARK, bold=True, align=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 10 — 2 min: Contrast before/after, quantify, show run steps, roadmap. Close with vision: indigenous e-governance for every Indian coal mine."

prs.save(OUT)
print(f"Saved {OUT} — {OUT.stat().st_size/1024:.1f} KB, {len(prs.slides)} slides")
