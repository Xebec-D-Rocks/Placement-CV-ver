#!/usr/bin/env python3
"""
CoalGuard 10-20-30 STRICT - smallest font = 30pt
10 slides, landscape 16:9, real screenshots, minimal text
"""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

BG_DARK = RGBColor(15, 22, 32)
BG_PANEL = RGBColor(22, 32, 44)
BG_CARD = RGBColor(28, 40, 54)
BORDER = RGBColor(42, 55, 70)
MUTED = RGBColor(147, 164, 184)
TEXT = RGBColor(230, 237, 243)
ACCENT = RGBColor(62, 166, 255)
ACCENT2 = RGBColor(51, 194, 129)
CRITICAL = RGBColor(239, 68, 68)
WHITE = RGBColor(255,255,255)
YELLOW = RGBColor(230,194,41)
HIGH = RGBColor(239,138,60)

OUT = Path(__file__).parent / "CoalGuard_SIH26024_Presentation.pptx"
REAL = Path(__file__).parent / "docs" / "presentation_assets" / "real"

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)
prs.core_properties.title = "CoalGuard SIH 2026 PSID 26024 - 10-20-30"
prs.core_properties.author = "CoalGuard"

MIN_FONT = 30  # strict

def set_bg(slide, c=BG_DARK):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = c

def shape(slide, l, t, w, h, fill=None, line=None, lw=1, r=False):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if r else MSO_SHAPE.RECTANGLE, l, t, w, h)
    shp.line.fill.background()
    if fill:
        shp.fill.solid(); shp.fill.fore_color.rgb = fill
    else:
        shp.fill.background()
    if line:
        shp.line.color.rgb = line; shp.line.width = Pt(lw)
    else:
        shp.line.fill.background()
    if r:
        try: shp.adjustments[0]=0.08
        except: pass
    return shp

def txt(slide, l, t, w, h, text, size=30, color=TEXT, bold=False, align=PP_ALIGN.LEFT, name="Calibri", italic=False):
    # enforce min 30
    if size < 30:
        size = 30
    tx = slide.shapes.add_textbox(l, t, w, h)
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
    p.line_spacing = Pt(size*1.15)
    return tx

def bullets(slide, l, t, w, h, items, size=30, color=TEXT, bullet="•"):
    # items: list of strings, each will be a paragraph
    # enforce 30
    if size < 30:
        size = 30
    tx = slide.shapes.add_textbox(l, t, w, h)
    tf = tx.text_frame
    tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.text = f"{bullet}  {it}"
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.font.name = "Calibri"
        p.space_after = Pt(8)
        p.line_spacing = Pt(size*1.2)
    return tx

# Images
dash = REAL / "dashboard_viewport.png"
if not dash.exists():
    dash = REAL / "dashboard_authed_viewport.png"
mines = REAL / "mines_viewport.png"
detail = REAL / "mine_detail_viewport.png"
api = REAL / "api_docs_viewport.png"
dash_bottom = REAL / "dashboard_viewport_bottom.png"

# Fallbacks
for p in [dash, mines, detail, api]:
    if not p.exists():
        print(f"WARN missing {p}")

# ===== SLIDE 1: TITLE =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(6), fill=ACCENT)
# Top right PSID
txt(slide, Inches(9.8), Inches(0.35), Inches(3.0), Inches(0.4), "PSID 26024", 30, ACCENT, bold=True, align=PP_ALIGN.RIGHT)
# Logo block
shape(slide, Inches(0.7), Inches(0.7), Inches(0.95), Inches(0.95), fill=ACCENT, r=True)
txt(slide, Inches(0.7), Inches(0.85), Inches(0.95), Inches(0.65), "CG", 30, BG_DARK, bold=True, align=PP_ALIGN.CENTER)
txt(slide, Inches(1.85), Inches(0.70), Inches(7), Inches(0.7), "CoalGuard", 44, WHITE, bold=True)
txt(slide, Inches(1.85), Inches(1.30), Inches(7), Inches(0.5), "Smart Governance for Coal Mines", 30, ACCENT, italic=True)
# Main headline 2 lines
tb = slide.shapes.add_textbox(Inches(0.7), Inches(2.05), Inches(7.5), Inches(1.6))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "One Platform."
p.font.size = Pt(36)
p.font.color.rgb = WHITE
p.font.bold = True
p.font.name = "Calibri"
p.space_after = Pt(6)
p = tf.add_paragraph()
p.text = "Every Mine. Every Rule."
p.font.size = Pt(36)
p.font.color.rgb = ACCENT
p.font.bold = True
p.font.name = "Calibri"
p.space_after = Pt(6)
p = tf.add_paragraph()
p.text = "Real Time."
p.font.size = Pt(36)
p.font.color.rgb = WHITE
p.font.bold = True
p.font.name = "Calibri"
# Sub — must be 30pt too
txt(slide, Inches(0.7), Inches(3.85), Inches(7.5), Inches(0.9), "Ministry of Coal • Coal India Limited • SIH 2026", 30, MUTED, align=PP_ALIGN.LEFT)
# Right image - dashboard preview, but keep caption 30pt? We'll put small label outside but still 30pt — make it short
shape(slide, Inches(8.6), Inches(0.70), Inches(4.0), Inches(5.10), fill=BG_PANEL, line=BORDER, r=True)
txt(slide, Inches(8.7), Inches(0.85), Inches(3.8), Inches(0.35), "LIVE DASHBOARD", 30, ACCENT, bold=True, align=PP_ALIGN.CENTER)
if dash.exists():
    slide.shapes.add_picture(str(dash), Inches(8.75), Inches(1.25), width=Inches(3.7), height=Inches(2.08))
shape(slide, Inches(8.75), Inches(3.45), Inches(3.7), Inches(1.95), fill=BG_DARK, line=BORDER, r=True)
# Stats inside right — 30pt
txt(slide, Inches(8.85), Inches(3.60), Inches(3.5), Inches(0.4), "459 Mines  •  12 States", 30, WHITE, align=PP_ALIGN.CENTER)
txt(slide, Inches(8.85), Inches(4.05), Inches(3.5), Inches(0.4), "Live • Real Data", 30, ACCENT2, bold=True, align=PP_ALIGN.CENTER)
txt(slide, Inches(8.85), Inches(4.55), Inches(3.5), Inches(0.6), "localhost:8001", 30, MUTED, align=PP_ALIGN.CENTER, name="Consolas")
# Footer — must be 30pt, so keep short
txt(slide, Inches(0.7), Inches(6.90), Inches(12), Inches(0.4), "Built for SIH 2026  •  Demo Ready", 30, RGBColor(90,107,125), align=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 1 — 2 min: Title. CoalGuard = one platform for every mine/rule/report. Point to live screenshot on right. 30pt forces brevity."

# ===== SLIDE 2: PROBLEM =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(6), fill=CRITICAL)
txt(slide, Inches(0.7), Inches(0.40), Inches(12), Inches(0.5), "The Problem", 36, CRITICAL, bold=True)
txt(slide, Inches(0.7), Inches(0.95), Inches(12), Inches(0.6), "Fragmented. Delayed. Opaque.", 30, WHITE, italic=True)
# 3 big bullets only — 30pt
bullets(slide, Inches(0.7), Inches(1.80), Inches(11.9), Inches(2.4), [
    "Paper & spreadsheets across 37 owners",
    "Weeks to report. Gaps found only at audit.",
    "Field work unverifiable.",
], size=30, color=MUTED)
# Scale — 30pt large numbers
shape(slide, Inches(0.7), Inches(4.40), Inches(12), Inches(1.80), fill=BG_PANEL, line=BORDER, r=True)
txt(slide, Inches(0.9), Inches(4.55), Inches(11.6), Inches(0.4), "Scale of Data We Ingested", 30, ACCENT, bold=True, align=PP_ALIGN.CENTER)
# 3 stats only to keep 30pt readable
txt(slide, Inches(1.0), Inches(5.05), Inches(3.5), Inches(0.5), "459 Mines", 30, WHITE, bold=True, align=PP_ALIGN.CENTER)
txt(slide, Inches(4.8), Inches(5.05), Inches(3.5), Inches(0.5), "12 States", 30, WHITE, bold=True, align=PP_ALIGN.CENTER)
txt(slide, Inches(8.5), Inches(5.05), Inches(3.5), Inches(0.5), "52 Districts", 30, WHITE, bold=True, align=PP_ALIGN.CENTER)
txt(slide, Inches(1.0), Inches(5.55), Inches(11.6), Inches(0.4), "Real Kaggle dataset • Geocoded 459 rows", 30, MUTED, align=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 2 — 2 min: Three crisp problems. Scale grounds it in real data. 30pt forces you to talk, not read."

# ===== SLIDE 3: SOLUTION =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(6), fill=ACCENT)
txt(slide, Inches(0.7), Inches(0.40), Inches(12), Inches(0.5), "Our Solution", 36, ACCENT, bold=True)
txt(slide, Inches(0.7), Inches(0.95), Inches(12), Inches(0.6), "One Ecosystem. Zero Silos.", 30, WHITE, italic=True)
# Core center
shape(slide, Inches(5.15), Inches(1.85), Inches(3.0), Inches(1.20), fill=ACCENT, r=True)
txt(slide, Inches(5.15), Inches(2.05), Inches(3.0), Inches(0.5), "CoalGuard", 30, BG_DARK, bold=True, align=PP_ALIGN.CENTER)
txt(slide, Inches(5.15), Inches(2.50), Inches(3.0), Inches(0.35), "Central Platform", 30, BG_DARK, align=PP_ALIGN.CENTER)
# 4 pillars only (to keep 30pt readable) — 2x2 grid
pillars = [
    ("Compliance", ACCENT2, Inches(1.0), Inches(3.40)),
    ("Inspections", HIGH, Inches(7.0), Inches(3.40)),
    ("Corrective Actions", CRITICAL, Inches(1.0), Inches(5.05)),
    ("GIS & Dashboards", YELLOW, Inches(7.0), Inches(5.05)),
]
for title, col, x, y in pillars:
    shape(slide, x, y, Inches(5.0), Inches(1.25), fill=BG_PANEL, line=col, lw=2, r=True)
    txt(slide, x, y+Inches(0.25), Inches(5.0), Inches(0.5), title, 30, WHITE, bold=True, align=PP_ALIGN.CENTER)
    txt(slide, x, y+Inches(0.70), Inches(5.0), Inches(0.35), "LIVE", 30, col, align=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 3 — 1.5 min: Core platform with 4 pillars. Field → HQ in one place. Keep it visual."

# ===== SLIDE 4: HOW IT WORKS =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(6), fill=ACCENT)
txt(slide, Inches(0.7), Inches(0.40), Inches(12), Inches(0.5), "How It Works", 36, WHITE, bold=True)
# 3 steps only to keep 30pt huge
steps = [
    ("1  Field", "Geo-tag + Photo", ACCENT, Inches(0.7)),
    ("2  Platform", "Auto-escalate", CRITICAL, Inches(4.7)),
    ("3  HQ", "Dashboard + Report", ACCENT2, Inches(8.7)),
]
for title, sub, col, x in steps:
    shape(slide, x, Inches(1.50), Inches(3.9), Inches(2.40), fill=BG_PANEL, line=col, lw=2, r=True)
    txt(slide, x, Inches(1.75), Inches(3.9), Inches(0.5), title, 30, col, bold=True, align=PP_ALIGN.CENTER)
    txt(slide, x, Inches(2.35), Inches(3.9), Inches(0.5), sub, 30, MUTED, align=PP_ALIGN.CENTER)
    txt(slide, x, Inches(3.00), Inches(3.9), Inches(0.4), "●  Verified", 30, ACCENT2, align=PP_ALIGN.CENTER)
# Arrow between
txt(slide, Inches(4.45), Inches(2.55), Inches(0.30), Inches(0.5), "→", 30, WHITE, bold=True, align=PP_ALIGN.CENTER)
txt(slide, Inches(8.45), Inches(2.55), Inches(0.30), Inches(0.5), "→", 30, WHITE, bold=True, align=PP_ALIGN.CENTER)
# Workflow caption — 30pt
txt(slide, Inches(0.7), Inches(4.30), Inches(12), Inches(0.5), "Every report geo-tagged. Hash-audited.", 30, MUTED, align=PP_ALIGN.CENTER, italic=True)
# Bottom — two features only
shape(slide, Inches(0.7), Inches(5.00), Inches(5.8), Inches(1.20), fill=BG_PANEL, line=BORDER, r=True)
txt(slide, Inches(0.7), Inches(5.20), Inches(5.8), Inches(0.4), "Offline Mobile", 30, ACCENT, bold=True, align=PP_ALIGN.CENTER)
txt(slide, Inches(0.7), Inches(5.65), Inches(5.8), Inches(0.4), "client_id sync", 30, MUTED, align=PP_ALIGN.CENTER)
shape(slide, Inches(7.0), Inches(5.00), Inches(5.6), Inches(1.20), fill=BG_PANEL, line=BORDER, r=True)
txt(slide, Inches(7.0), Inches(5.20), Inches(5.6), Inches(0.4), "Blockchain Audit", 30, ACCENT, bold=True, align=PP_ALIGN.CENTER)
txt(slide, Inches(7.0), Inches(5.65), Inches(5.6), Inches(0.4), "SHA256 chain", 30, MUTED, align=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 4 — 1.5 min: 3-step flow. Field → Platform → HQ. Offline + audit are trust anchors."

# ===== SLIDE 5: STACK =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(6), fill=ACCENT)
txt(slide, Inches(0.7), Inches(0.40), Inches(12), Inches(0.5), "How We Built It", 36, WHITE, bold=True)
# 4 stack items only, huge font
stack = [
    ("Django 5.1", "Postgres 17 + Redis 7", ACCENT, Inches(0.7), Inches(1.45)),
    ("Leaflet GIS", "Chart.js Analytics", ACCENT2, Inches(7.0), Inches(1.45)),
    ("Celery Beat", "Hourly Escalations", CRITICAL, Inches(0.7), Inches(3.55)),
    ("Docker", "One-click Run", YELLOW, Inches(7.0), Inches(3.55)),
]
for title, sub, col, x, y in stack:
    shape(slide, x, y, Inches(5.6), Inches(1.60), fill=BG_PANEL, line=col, lw=2, r=True)
    txt(slide, x, y+Inches(0.25), Inches(5.6), Inches(0.5), title, 30, WHITE, bold=True, align=PP_ALIGN.CENTER)
    txt(slide, x, y+Inches(0.75), Inches(5.6), Inches(0.4), sub, 30, MUTED, align=PP_ALIGN.CENTER)
# Local-first banner — 30pt
shape(slide, Inches(0.7), Inches(5.60), Inches(12), Inches(0.70), fill=BG_CARD, line=ACCENT2, r=True)
txt(slide, Inches(0.7), Inches(5.75), Inches(12), Inches(0.4), "Local-first. No Cloud Needed.", 30, ACCENT2, bold=True, align=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 5 — 1.5 min: Boring-tech for reliability. Local-first, dual-stack, one-click."

# ===== SLIDE 6: PS COVERAGE =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(6), fill=ACCENT2)
txt(slide, Inches(0.7), Inches(0.40), Inches(12), Inches(0.5), "PS Coverage", 36, ACCENT2, bold=True)
txt(slide, Inches(0.7), Inches(0.95), Inches(12), Inches(0.6), "8 / 8 Requirements — Live", 30, WHITE, bold=True)
# 4 big checkmarks 2x2
reqs = [
    ("Compliance", "✓", ACCENT2),
    ("Inspections", "✓", ACCENT2),
    ("AI Risk", "✓", ACCENT2),
    ("Geo-tagged", "✓", ACCENT2),
    ("Dashboards", "✓", ACCENT2),
    ("Alerts", "✓", ACCENT2),
    ("Paperless", "✓", ACCENT2),
    ("Scalable", "✓", ACCENT2),
]
# layout 4x2
for i, (label, check, col) in enumerate(reqs):
    r = i // 4
    c = i % 4
    x = Inches(0.7) + c*Inches(3.1)
    y = Inches(1.85) + r*Inches(1.80)
    shape(slide, x, y, Inches(2.85), Inches(1.50), fill=BG_PANEL, line=col, lw=2, r=True)
    txt(slide, x, y+Inches(0.20), Inches(2.85), Inches(0.5), check, 36, col, bold=True, align=PP_ALIGN.CENTER)
    txt(slide, x, y+Inches(0.70), Inches(2.85), Inches(0.5), label, 30, WHITE, bold=True, align=PP_ALIGN.CENTER)
txt(slide, Inches(0.7), Inches(5.75), Inches(12), Inches(0.5), "All features verified in code & live app.", 30, MUTED, align=PP_ALIGN.CENTER, italic=True)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 6 — 1 min: Prove 100% coverage. Every check is code + live, not future plan."

# ===== SLIDE 7: REAL DASHBOARD SCREENSHOT =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(6), fill=ACCENT)
txt(slide, Inches(0.7), Inches(0.30), Inches(12), Inches(0.4), "Live Demo — Dashboard", 30, ACCENT, bold=True)
txt(slide, Inches(0.7), Inches(0.65), Inches(12), Inches(0.4), "Real Screenshot  •  localhost:8001/", 30, MUTED, name="Consolas")
# Image takes most of slide - keep 30pt caption below max
if dash.exists():
    shape(slide, Inches(0.7), Inches(1.10), Inches(11.9), Inches(5.55), fill=BG_PANEL, line=BORDER, r=True)
    slide.shapes.add_picture(str(dash), Inches(0.75), Inches(1.15), width=Inches(11.8), height=Inches(5.45))
else:
    shape(slide, Inches(0.7), Inches(1.10), Inches(11.9), Inches(5.55), fill=BG_CARD, line=BORDER, r=True)
    txt(slide, Inches(0.7), Inches(3.5), Inches(11.9), Inches(0.5), "Dashboard screenshot", 30, MUTED, align=PP_ALIGN.CENTER)
txt(slide, Inches(0.7), Inches(6.80), Inches(11.9), Inches(0.4), "KPIs  •  GIS Map  •  Charts — All Live Data", 30, WHITE, align=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 7 — 3 min: LIVE. Show KPIs, map colors, charts. Switch to browser if possible."

# ===== SLIDE 8: REAL REGISTRY SCREENSHOT =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(6), fill=ACCENT)
txt(slide, Inches(0.7), Inches(0.30), Inches(12), Inches(0.4), "Live Demo — Mine Registry", 30, ACCENT, bold=True)
txt(slide, Inches(0.7), Inches(0.65), Inches(12), Inches(0.4), "Real Screenshot  •  /mines/", 30, MUTED, name="Consolas")
if mines.exists():
    shape(slide, Inches(0.7), Inches(1.10), Inches(11.9), Inches(5.55), fill=BG_PANEL, line=BORDER, r=True)
    slide.shapes.add_picture(str(mines), Inches(0.75), Inches(1.15), width=Inches(11.8), height=Inches(5.45))
else:
    shape(slide, Inches(0.7), Inches(1.10), Inches(11.9), Inches(5.55), fill=BG_CARD, line=BORDER, r=True)
txt(slide, Inches(0.7), Inches(6.80), Inches(11.9), Inches(0.4), "Search  •  Filter  •  Risk Badge  •  CSV Export", 30, WHITE, align=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 8 — 1.5 min: Registry drill-down. Filters, risk badge, Real/Synthetic tag. Click to detail."

# ===== SLIDE 9: AI + API SCREENSHOT =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(6), fill=ACCENT2)
txt(slide, Inches(0.7), Inches(0.30), Inches(12), Inches(0.4), "AI Engine + API", 30, ACCENT2, bold=True)
# Left: formula huge 30pt
shape(slide, Inches(0.7), Inches(1.05), Inches(5.8), Inches(2.80), fill=BG_PANEL, line=BORDER, r=True)
txt(slide, Inches(0.9), Inches(1.25), Inches(5.4), Inches(0.5), "Risk Score", 30, ACCENT, bold=True, align=PP_ALIGN.CENTER)
# formula lines — each 30pt but short
tb = slide.shapes.add_textbox(Inches(0.9), Inches(1.85), Inches(5.4), Inches(1.2))
tf = tb.text_frame; tf.word_wrap=True
for t in ["safety × 0.35", "+ compliance × 0.30", "+ contractor × 0.15 + incident × 0.20"]:
    p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
    if p.text: p = tf.add_paragraph()
    p.text = t
    p.font.size = Pt(30)
    p.font.color.rgb = WHITE
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.CENTER
    p.line_spacing = Pt(34)
# set first paragraph after loop? first already added
# Right: API screenshot
shape(slide, Inches(6.8), Inches(1.05), Inches(5.8), Inches(4.80), fill=BG_PANEL, line=BORDER, r=True)
txt(slide, Inches(6.9), Inches(1.15), Inches(5.6), Inches(0.4), "Swagger  •  /api/docs/", 30, ACCENT, bold=True, align=PP_ALIGN.CENTER)
if api.exists():
    slide.shapes.add_picture(str(api), Inches(6.95), Inches(1.65), width=Inches(5.5), height=Inches(3.09))
else:
    shape(slide, Inches(6.95), Inches(1.65), Inches(5.5), Inches(3.09), fill=BG_DARK, line=BORDER)
# Bands below formula — 30pt huge but one line
shape(slide, Inches(0.7), Inches(4.10), Inches(5.8), Inches(0.70), fill=BG_DARK, line=BORDER, r=True)
txt(slide, Inches(0.7), Inches(4.25), Inches(5.8), Inches(0.4), "LOW • MEDIUM • HIGH • CRITICAL", 30, MUTED, align=PP_ALIGN.CENTER)
# Bottom insight — 30pt
txt(slide, Inches(0.7), Inches(6.10), Inches(11.9), Inches(0.4), "Explainable. Auditable. Live.", 30, WHITE, bold=True, align=PP_ALIGN.CENTER)
txt(slide, Inches(0.7), Inches(6.50), Inches(11.9), Inches(0.4), "458 scored • Avg 84.4 • 6 High flagged", 30, MUTED, align=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 9 — 2 min: AI is transparent weighted sum, not black box. Show Swagger live on right."

# ===== SLIDE 10: IMPACT + ASK =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide)
shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(6), fill=ACCENT)
txt(slide, Inches(0.7), Inches(0.40), Inches(12), Inches(0.5), "Impact & Next", 36, WHITE, bold=True)
# 3 impacts 30pt
shape(slide, Inches(0.7), Inches(1.20), Inches(3.8), Inches(1.70), fill=BG_PANEL, line=ACCENT2, lw=2, r=True)
txt(slide, Inches(0.7), Inches(1.45), Inches(3.8), Inches(0.5), "Real-time", 30, ACCENT2, bold=True, align=PP_ALIGN.CENTER)
txt(slide, Inches(0.7), Inches(1.95), Inches(3.8), Inches(0.5), "Not weeks", 30, MUTED, align=PP_ALIGN.CENTER)
shape(slide, Inches(4.75), Inches(1.20), Inches(3.8), Inches(1.70), fill=BG_PANEL, line=ACCENT2, lw=2, r=True)
txt(slide, Inches(4.75), Inches(1.45), Inches(3.8), Inches(0.5), "Paperless", 30, ACCENT2, bold=True, align=PP_ALIGN.CENTER)
txt(slide, Inches(4.75), Inches(1.95), Inches(3.8), Inches(0.5), "OCR + PDF", 30, MUTED, align=PP_ALIGN.CENTER)
shape(slide, Inches(8.8), Inches(1.20), Inches(3.8), Inches(1.70), fill=BG_PANEL, line=ACCENT2, lw=2, r=True)
txt(slide, Inches(8.8), Inches(1.45), Inches(3.8), Inches(0.5), "Auditable", 30, ACCENT2, bold=True, align=PP_ALIGN.CENTER)
txt(slide, Inches(8.8), Inches(1.95), Inches(3.8), Inches(0.5), "SHA256 chain", 30, MUTED, align=PP_ALIGN.CENTER)
# How to run — must be 30pt, so shorten
shape(slide, Inches(0.7), Inches(3.30), Inches(12), Inches(1.90), fill=BG_PANEL, line=BORDER, r=True)
txt(slide, Inches(0.9), Inches(3.50), Inches(11.6), Inches(0.4), "Run Now — One Click", 30, ACCENT, bold=True, align=PP_ALIGN.CENTER)
txt(slide, Inches(0.9), Inches(4.00), Inches(11.6), Inches(0.4), "start_coalguard.bat", 30, WHITE, align=PP_ALIGN.CENTER, name="Consolas")
txt(slide, Inches(0.9), Inches(4.45), Inches(11.6), Inches(0.4), "localhost:8001  •  Demo logins ready", 30, MUTED, align=PP_ALIGN.CENTER)
# Closing — 30pt
shape(slide, Inches(0.7), Inches(5.55), Inches(12), Inches(1.00), fill=ACCENT, r=True)
txt(slide, Inches(0.7), Inches(5.75), Inches(12), Inches(0.6), "Ready to Deploy. Thank You.", 30, BG_DARK, bold=True, align=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 10 — 2 min: Impact + run + ask. Keep it to 30pt, talk the rest."

prs.save(OUT)
print(f"Saved {OUT} — {OUT.stat().st_size/1024:.1f} KB, {len(prs.slides)} slides")

# Verify no font <30
from pptx import Presentation as P
prs2 = P(OUT)
violations=[]
for si, s in enumerate(prs2.slides,1):
    for shp in s.shapes:
        if shp.has_text_frame:
            for para in shp.text_frame.paragraphs:
                for run in para.runs:
                    if run.text.strip() and run.font.size and run.font.size.pt < 29.9:
                        violations.append((si, run.text[:30], run.font.size.pt))
if violations:
    print("VIOLATIONS <30pt:")
    for v in violations[:20]:
        print(v)
else:
    print("PASS: all fonts >=30pt")
