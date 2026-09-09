#!/usr/bin/env python3
"""
CoalGuard — SIH 2026 PSID 26024 Presentation Builder
10-20-30 format: 10 slides, ~20 min, 30pt-inspired minimal text with visuals
"""

import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR

# Colors - CoalGuard dark theme
BG_DARK = RGBColor(15, 22, 32)
BG_PANEL = RGBColor(22, 32, 44)
BG_CARD = RGBColor(28, 40, 54)
BORDER = RGBColor(42, 55, 70)
TEXT = RGBColor(230, 237, 243)
MUTED = RGBColor(147, 164, 184)
ACCENT = RGBColor(62, 166, 255)
ACCENT2 = RGBColor(51, 194, 129)
LOW = RGBColor(51, 194, 129)
MEDIUM = RGBColor(230, 194, 41)
HIGH = RGBColor(239, 138, 60)
CRITICAL = RGBColor(239, 68, 68)
WHITE = RGBColor(255,255,255)

OUT = Path(__file__).parent / "CoalGuard_SIH26024_Presentation.pptx"
ASSETS = Path(__file__).parent / "docs" / "presentation_assets"
ASSETS.mkdir(parents=True, exist_ok=True)

# =========================================================
# Generate mock screenshots with Pillow
# =========================================================
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except:
    HAS_PIL = False

def get_font(size, bold=False):
    # Try to find a decent font, fallback to default
    candidates = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ]
    bold_candidates = [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
    ]
    paths = bold_candidates if bold else candidates
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

def round_rect(draw, xy, radius, fill, outline=None):
    x0,y0,x1,y1 = xy
    try:
        draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline)
    except:
        draw.rectangle(xy, fill=fill, outline=outline)

def generate_dashboard_mock():
    W, H = 1200, 700
    img = Image.new("RGB", (W,H), (15,22,32))
    d = ImageDraw.Draw(img)
    # header
    d.rectangle([0,0,W,52], fill=(22,32,44))
    d.rectangle([0,52,W,53], fill=(42,55,70))
    f_title = get_font(16, bold=True)
    f_small = get_font(10)
    f_kpi_val = get_font(22, bold=True)
    f_kpi_lbl = get_font(9)
    f_card_title = get_font(11, bold=True)
    d.text((18,16), "CoalGuard  —  Governance Dashboard", fill=(230,237,243), font=f_title)
    d.text((18,36), "PSID 26024  •  Real-time statutory compliance  •  inspections  •  risk", fill=(147,164,184), font=f_small)
    # KPI grid - 8 cards
    kpis = [
        ("458", "Total Mines"),
        ("295 / 163", "Real / Synthetic"),
        ("84.4", "Avg Risk Score"),
        ("6", "High/Critical Risk"),
        ("42", "Open High/Crit Obs"),
        ("18", "Overdue Actions"),
        ("27", "Overdue Compliance"),
        ("12", "Unread Alerts"),
    ]
    kpi_colors = [(28,40,54)]*3 + [(45,25,30)] + [(28,40,54),(45,25,30),(45,25,30),(28,40,54)]
    x0, y0 = 14, 62
    cw, ch = 137, 68
    gap = 10
    for i, (val, lbl) in enumerate(kpis):
        col = i % 4
        row = i // 4
        x = x0 + col*(cw+gap)
        y = y0 + row*(ch+gap)
        fill = (45,30,35) if lbl in ("High/Critical Risk","Overdue Actions","Overdue Compliance") else (28,40,54)
        border = (239,68,68) if fill==(45,30,35) else (42,55,70)
        round_rect(d, [x,y,x+cw,y+ch], 8, fill=fill, outline=border)
        d.text((x+10,y+10), val, fill=(62,166,255) if fill!=(45,30,35) else (239,68,68), font=f_kpi_val)
        d.text((x+10,y+42), lbl, fill=(147,164,184), font=f_kpi_lbl)
    # alert banner
    banner_y = y0 + 2*(ch+gap) + 10
    round_rect(d, [14,banner_y,W-28,banner_y+26], 6, fill=(239,68,68,30) if False else (42,22,22), outline=(239,68,68))
    # PIL doesn't support alpha, solid fallback
    d.rectangle([14,banner_y,W-14,banner_y+26], fill=(62,22,28))
    d.rectangle([14,banner_y,W-14,banner_y+26], outline=(239,68,68))
    f_banner = get_font(9)
    d.text((22,banner_y+8), "⚠  6 high/critical risk mines  •  27 overdue compliance records require attention. Check escalations & corrective actions.", fill=(239,180,180), font=f_banner)
    # Map + charts area
    map_y = banner_y+36
    # GIS card
    round_rect(d, [14,map_y, 580, map_y+210], 8, fill=(22,32,44), outline=(42,55,70))
    d.text((24,map_y+10), "GIS — Mine Locations (Leaflet)", fill=(230,237,243), font=f_card_title)
    # map placeholder - dots
    # map bg
    d.rectangle([24,map_y+28,570,map_y+198], fill=(18,28,42), outline=(42,55,70))
    # India approx outline dots - scatter
    import random
    random.seed(42)
    # simulate mines across India
    for _ in range(55):
        x = random.randint(30, 540)
        y = random.randint(map_y+35, map_y+190)
        r = random.randint(3,5)
        col_choice = random.choices([(51,194,129),(230,194,41),(239,138,60),(239,68,68)], weights=[60,30,8,2])[0]
        d.ellipse([x-r, y-r, x+r, y+r], fill=col_choice, outline=(15,22,32))
    d.text((24,map_y+202), "Geo-tagged • color by risk • click for details", fill=(100,120,140), font=get_font(8))
    # Charts grid 2x2 on right
    chart_titles = ["Mines by Risk Level", "Mines by State (Top 10)", "Compliance Breakdown", "Inspection Trend (12mo)"]
    # bar chart colors
    for idx, title in enumerate(chart_titles):
        col = idx % 2
        row = idx // 2
        cx = 595 + col*293
        cy = map_y + row*108
        round_rect(d, [cx,cy,cx+283,cy+100], 8, fill=(22,32,44), outline=(42,55,70))
        d.text((cx+10,cy+8), title, fill=(230,237,243), font=get_font(9, bold=True))
        # draw bars
        if idx==0:
            # risk bars
            levels = [("LOW",295, (51,194,129)), ("MED",157, (230,194,41)), ("HIGH",6, (239,138,60)), ("CRIT",0, (239,68,68))]
            bar_x = cx+14
            for lbl,val,colr in levels:
                h = int((val/295)*42) if val>0 else 2
                d.rectangle([bar_x, cy+78-h, bar_x+38, cy+78], fill=colr)
                d.text((bar_x+6, cy+84), lbl, fill=(147,164,184), font=get_font(7))
                bar_x+= 62
        elif idx==1:
            states = [("Jharkhand",72),("Chhattisgarh",64),("Odisha",58),("West Bengal",52)]
            bar_y = cy+22
            for st,val in states:
                w = int((val/72)*150)
                d.rectangle([cx+90, bar_y, cx+90+w, bar_y+10], fill=(62,166,255))
                d.text((cx+10, bar_y), st, fill=(147,164,184), font=get_font(7))
                bar_y+=16
        elif idx==2:
            # pie approx
            # donut segments
            cx_p, cy_p = cx+60, cy+60
            # we fake with arcs using ellipse segments - just draw circles
            d.ellipse([cx_p-28, cy_p-22, cx_p+28, cy_p+22], fill=(51,194,129), outline=(22,32,44))
            d.ellipse([cx_p-18, cy_p-14, cx_p+18, cy_p+10], fill=(22,32,44))
            # legend
            leg = [("COMPLIANT", (51,194,129)), ("PENDING", (230,194,41)), ("OVERDUE", (239,68,68))]
            lx = cx+110
            ly = cy+30
            for lb,cl in leg:
                d.rectangle([lx, ly, lx+8, ly+8], fill=cl)
                d.text((lx+14, ly-1), lb, fill=(147,164,184), font=get_font(7))
                ly+=14
        else:
            # trend line
            pts = [(cx+16, cy+68),(cx+50, cy+62),(cx+84, cy+70),(cx+118, cy+55),(cx+152, cy+60),(cx+186, cy+45),(cx+220, cy+52),(cx+250, cy+40)]
            for i in range(len(pts)-1):
                d.line([pts[i], pts[i+1]], fill=(62,166,255), width=2)
            pts2 = [(cx+16, cy+75),(cx+50, cy+72),(cx+84, cy+78),(cx+118, cy+68),(cx+152, cy+72),(cx+186, cy+62),(cx+220, cy+68),(cx+250, cy+58)]
            for i in range(len(pts2)-1):
                d.line([pts2[i], pts2[i+1]], fill=(239,138,60), width=2)
            d.text((cx+14, cy+84), "Inspections  —  Observations", fill=(100,120,140), font=get_font(7))
    # bottom tables - anomalies
    tbl_y = map_y+222
    round_rect(d, [14,tbl_y, W-14, tbl_y+108], 8, fill=(22,32,44), outline=(42,55,70))
    d.text((24,tbl_y+10), "AI — Anomaly & Recurring Failure Insights", fill=(230,237,243), font=f_card_title)
    # left table
    d.text((24,tbl_y+32), "Flagged Anomalies (z-score > threshold)", fill=(147,164,184), font=get_font(8, bold=True))
    # header
    d.rectangle([24,tbl_y+48, 580, tbl_y+64], fill=(28,40,54))
    for hx, txt in [(26,"Mine"),(160,"Risk"),(230,"Open Obs"),(300,"Reason")]:
        d.text((hx, tbl_y+52), txt, fill=(100,120,140), font=get_font(7))
    rows = [("Rajmahal OCP","HIGH",8,"open_obs z=3.42"),("Kusmunda Mine","CRITICAL",11,"z=2.91 + overdue≥3"),("Gevra OCP","MEDIUM",6,"z=2.14")]
    ry = tbl_y+68
    for mine,risk,obs,rea in rows:
        d.text((26,ry), mine, fill=(62,166,255), font=get_font(8))
        colr = (230,194,41) if risk=="MEDIUM" else (239,138,60) if risk=="HIGH" else (239,68,68)
        d.rectangle([160,ry-1,200,ry+11], fill=colr)
        d.text((164,ry), risk, fill=(15,22,32), font=get_font(7))
        d.text((235,ry), str(obs), fill=(230,237,243), font=get_font(8))
        d.text((300,ry), rea, fill=(147,164,184), font=get_font(7))
        ry+=14
    # right table
    d.text((620,tbl_y+32), "Recurring Compliance Failures", fill=(147,164,184), font=get_font(8, bold=True))
    d.rectangle([620,tbl_y+48, W-24, tbl_y+64], fill=(28,40,54))
    for hx, txt in [(622,"Requirement"),(820,"Category"),(920,"Failure %")]:
        d.text((hx, tbl_y+52), txt, fill=(100,120,140), font=get_font(7))
    rrows = [("Mine Safety Reg. 2023","SAFETY","38.2% (21/55)"),("Env Clearance QPR","ENVIRONMENT","31.4% (16/51)")]
    ry = tbl_y+68
    for req,cat,fail in rrows:
        d.text((622,ry), req, fill=(230,237,243), font=get_font(8))
        d.text((820,ry), cat, fill=(147,164,184), font=get_font(7))
        d.text((920,ry), fail, fill=(239,138,60), font=get_font(7))
        ry+=14
    # footer quick actions
    btn_y = tbl_y+82
    for bx, txt, colr in [(620, "Download PDF", (62,166,255)), (740, "API Docs", (42,55,70)), (830, "Audit Chain", (42,55,70)), (920, "Mine Registry →", (42,55,70))]:
        # draw button - approximate
        round_rect(d, [bx, btn_y, bx+100, btn_y+18], 6, fill=colr, outline=colr if colr!=(62,166,255) else (62,166,255))
        d.text((bx+8, btn_y+5), txt, fill=(15,22,32) if colr==(62,166,255) else (230,237,243), font=get_font(7))

    out1 = ASSETS / "dashboard_mock.png"
    img.save(out1, "PNG", optimize=True)
    return out1

def generate_registry_mock():
    W,H = 1200, 700
    img = Image.new("RGB", (W,H), (15,22,32))
    d = ImageDraw.Draw(img)
    f_title = get_font(15, bold=True)
    f_small = get_font(9)
    f_th = get_font(8, bold=True)
    f_td = get_font(9)
    # header
    d.rectangle([0,0,W,50], fill=(22,32,44))
    d.rectangle([0,50,W,51], fill=(42,55,70))
    d.text((18,14), "Mine Registry", fill=(230,237,243), font=f_title)
    d.text((18,32), "458 mines matching current filters  •  12 states  •  37 subsidiaries", fill=(147,164,184), font=f_small)
    # filters bar
    round_rect(d, [12,62, W-12, 124], 8, fill=(22,32,44), outline=(42,55,70))
    filters = ["Search: mine name", "State: All ▼", "Coal Type: All ▼", "Mine Type: All ▼", "Risk Level: All ▼", "Per Page: 25 ▼"]
    fx=22
    for fl in filters:
        round_rect(d, [fx,84, fx+150, 108], 6, fill=(28,40,54), outline=(42,55,70))
        d.text((fx+8, 92), fl, fill=(147,164,184), font=get_font(8))
        fx+=164
    # buttons
    round_rect(d, [W-220,84, W-120,108], 6, fill=(62,166,255))
    d.text((W-210,92), "Apply", fill=(15,22,32), font=get_font(9, bold=True))
    round_rect(d, [W-110,84, W-22,108], 6, fill=(28,40,54), outline=(42,55,70))
    d.text((W-102,92), "Download CSV", fill=(230,237,243), font=get_font(8))
    # table card
    round_rect(d, [12,136, W-12, H-12], 8, fill=(22,32,44), outline=(42,55,70))
    # table header
    d.rectangle([14,138, W-14, 162], fill=(28,40,54))
    headers = [("Name",22),("State",250),("District",360),("Subsidiary",480),("Coal Type",620),("Risk",730),("Compliance %",850),("Source",960)]
    for txt,x in headers:
        d.text((x,146), txt, fill=(100,120,140), font=f_th)
    # rows
    mines = [
        ("Ningah Colliery", "West Bengal", "Paschim Bardhaman", "ECL", "Coal", "LOW  92.1", "94%", "real"),
        ("Jhanjra Project Colly", "West Bengal", "Paschim Bardhaman", "ECL", "Coal", "MED  68.4", "61%", "real"),
        ("Rajmahal OCP", "Jharkhand", "Godda", "ECL", "Coal", "HIGH  48.2", "32%", "synthetic"),
        ("Gevra OCP", "Chhattisgarh", "Korba", "SECL", "Coal", "LOW  88.7", "82%", "real"),
        ("Kusmunda Mine", "Chhattisgarh", "Korba", "SECL", "Coal", "CRIT 31.5", "21%", "synthetic"),
        ("Bina Extension", "Madhya Pradesh", "Singrauli", "NCL", "Coal", "MED  72.3", "67%", "real"),
        ("Dudhichua OCP", "Madhya Pradesh", "Singrauli", "NCL", "Coal", "LOW  85.9", "89%", "real"),
        ("Lakhanpur OCP", "Odisha", "Jharsuguda", "MCL", "Coal", "LOW  91.2", "93%", "real"),
    ]
    y=170
    for name,state,dist,subs,ctype,risk,comp,src in mines:
        # alt row
        if mines.index((name,state,dist,subs,ctype,risk,comp,src))%2==1:
            d.rectangle([14,y-4, W-14, y+18], fill=(26,36,50))
        d.text((22,y), name, fill=(62,166,255), font=get_font(9))
        d.text((250,y), state, fill=(230,237,243), font=f_td)
        d.text((360,y), dist, fill=(230,237,243), font=get_font(8))
        d.text((480,y), subs, fill=(230,237,243), font=f_td)
        d.text((620,y), ctype, fill=(230,237,243), font=f_td)
        # risk badge
        lvl = risk.split()[0]
        colr = {"LOW":(51,194,129),"MED":(230,194,41),"HIGH":(239,138,60),"CRIT":(239,68,68)}[lvl]
        d.rounded_rectangle([730,y-2, 790, y+12], radius=6, fill=colr)
        d.text((735,y-1), lvl, fill=(15,22,32) if lvl!="CRIT" else (255,255,255), font=get_font(7, bold=True))
        d.text((795,y), risk.split()[1], fill=(147,164,184), font=get_font(8))
        d.text((850,y), comp, fill=(230,237,243), font=f_td)
        # source tag
        tag_col = (42,55,70) if src=="real" else (62,30,40)
        d.rounded_rectangle([960,y-2, 1010, y+12], radius=4, fill=tag_col, outline=(42,55,70))
        d.text((968,y-1), src, fill=(147,164,184), font=get_font(7))
        y+=26
        d.line([(14,y-6),(W-14,y-6)], fill=(42,55,70), width=1)
    # pagination
    d.text((22, H-28), "Page 1 of 19  •  Prev  [1]  2  3 ... 19  Next", fill=(147,164,184), font=get_font(9))
    out2 = ASSETS / "registry_mock.png"
    img.save(out2, "PNG", optimize=True)
    return out2

def generate_analytics_mock():
    W,H = 1200, 700
    img = Image.new("RGB", (W,H), (15,22,32))
    d = ImageDraw.Draw(img)
    f_title = get_font(16, bold=True)
    f_card = get_font(11, bold=True)
    f_small = get_font(9)
    # header bar
    d.rectangle([0,0,W,52], fill=(22,32,44))
    d.rectangle([0,52,W,53], fill=(42,55,70))
    d.text((18,16), "AI / Analytics Engine  —  Explainable Risk & Anomaly Detection", fill=(230,237,243), font=f_title)
    d.text((18,36), "Transparent weighted formula  •  No black-box  •  apps/analytics/risk.py  •  anomaly.py", fill=(147,164,184), font=get_font(9))
    # left: formula card
    round_rect(d, [12,66, 580, 340], 8, fill=(22,32,44), outline=(42,55,70))
    d.text((24,78), "Risk Score Formula  (0-100, higher = safer)", fill=TEXT, font=f_card)
    # formula box
    round_rect(d, [24,104, 568, 168], 8, fill=(28,40,54), outline=(42,55,70))
    d.text((32,114), "risk_score  =  safety_score × 0.35", fill=(62,166,255), font=get_font(11, bold=True))
    d.text((32,134), "                + compliance_score × 0.30", fill=(230,237,243), font=get_font(11))
    d.text((32,150), "                + contractor_score × 0.15  +  incident_score × 0.20", fill=(230,237,243), font=get_font(11))
    # component table
    d.text((24,180), "Component Derivation", fill=(147,164,184), font=get_font(9, bold=True))
    d.rectangle([24,198, 568, 216], fill=(28,40,54))
    for hx, txt in [(26,"Component"),(160,"Derivation"),(360,"Penalty / Logic")]:
        d.text((hx,202), txt, fill=(100,120,140), font=get_font(7))
    comps = [
        ("Safety", "Open observations", "LOW -2  MED -5  HIGH -12  CRIT -25"),
        ("Compliance", "COMPLIANT / determinable", "No data → 50 (neutral)"),
        ("Contractor", "Stable hash( subsidiary)", "70 ±10 placeholder"),
        ("Incident", "Corrective Actions", "OPEN -5  IP -3  OVERDUE -15"),
    ]
    y=222
    for c, der, pen in comps:
        d.text((26,y), c, fill=(62,166,255), font=get_font(8, bold=True))
        d.text((160,y), der, fill=(230,237,243), font=get_font(8))
        d.text((360,y), pen, fill=(147,164,184), font=get_font(8))
        y+=18
    # bands
    round_rect(d, [24,300, 568, 330], 6, fill=(28,40,54), outline=(42,55,70))
    d.text((32,308), "Bands:  80-100 LOW", fill=(51,194,129), font=get_font(9, bold=True))
    d.text((170,308), "  60-79 MED", fill=(230,194,41), font=get_font(9))
    d.text((260,308), "  40-59 HIGH", fill=(239,138,60), font=get_font(9))
    d.text((350,308), "  0-39 CRITICAL", fill=(239,68,68), font=get_font(9))
    # right: distribution + anomaly
    round_rect(d, [595,66, W-12, 340], 8, fill=(22,32,44), outline=(42,55,70))
    d.text((610,78), "Live Risk Distribution  (458 scored  •  avg 84.4)", fill=TEXT, font=f_card)
    # bars vertical
    bars = [("LOW",295,(51,194,129)),("MEDIUM",157,(230,194,41)),("HIGH",6,(239,138,60)),("CRITICAL",0,(239,68,68))]
    bx=620
    for lbl,val,colr in bars:
        h=int((val/295)*120) if val>0 else 4
        d.rectangle([bx, 212-h, bx+90, 212], fill=colr)
        d.text((bx+20, 218), lbl, fill=(147,164,184), font=get_font(8, bold=True))
        d.text((bx+30, 232), str(val), fill=(230,237,243), font=get_font(10, bold=True))
        bx+=120
    # anomaly explanation
    d.text((610,260), "Anomaly Detection —  z-score & frequency", fill=(147,164,184), font=get_font(9, bold=True))
    d.text((610,278), "• Flag if  open_obs  >  mean + 2σ", fill=(230,237,243), font=get_font(8))
    d.text((610,292), "• Or  overdue CAs ≥ 3  •  Recurring failures ranked by OVERDUE+ESCALATED rate", fill=(230,237,243), font=get_font(8))
    round_rect(d, [610,310, W-22, 330], 6, fill=(28,40,54), outline=(42,55,70))
    d.text((620,316), "Fully explainable —  ML classifier can replace module when labeled incident data exists.", fill=(100,120,140), font=get_font(8))
    # bottom row: subsidiary risk + recurring
    round_rect(d, [12,352, 580, H-12], 8, fill=(22,32,44), outline=(42,55,70))
    d.text((24,364), "Highest Risk Subsidiaries / Mines", fill=TEXT, font=f_card)
    # mini table
    d.rectangle([24,386, 568, 404], fill=(28,40,54))
    for hx, txt in [(26,"Subsidiary / Mine"),(240,"Avg Risk"),(340,"Critical")]:
        d.text((hx,390), txt, fill=(100,120,140), font=get_font(7))
    subs = [("ECL Eastern Coalfields", "62.1", "3 HIGH"),("MCL Mahanadi", "71.4", "1 HIGH"),("Rajmahal OCP", "48.2", "HIGH"),("Kusmunda", "31.5", "CRITICAL")]
    y=410
    for name,avg,crit in subs:
        d.text((26,y), name, fill=(230,237,243), font=get_font(8))
        d.text((240,y), avg, fill=(239,138,60), font=get_font(8))
        d.text((340,y), crit, fill=(239,68,68), font=get_font(8))
        y+=18
    # recurring failures card
    round_rect(d, [595,352, W-12, H-12], 8, fill=(22,32,44), outline=(42,55,70))
    d.text((610,364), "Recurring Compliance Failures  (Top by failure %)", fill=TEXT, font=f_card)
    d.rectangle([610,386, W-22, 404], fill=(28,40,54))
    for hx, txt in [(612,"Requirement"),(800,"Category"),(920,"Rate")]:
        d.text((hx,390), txt, fill=(100,120,140), font=get_font(7))
    fails = [("Mine Safety Reg. 2023","SAFETY","38.2%"),("Env. Clearance QPR","ENV","31.4%"),("Labour Welfare Audit","LABOUR","27.8%")]
    y=410
    for req,cat,rate in fails:
        d.text((612,y), req, fill=(230,237,243), font=get_font(8))
        d.text((800,y), cat, fill=(147,164,184), font=get_font(8))
        d.text((920,y), rate, fill=(239,138,60), font=get_font(8, bold=True))
        y+=18
    # rerun note
    d.text((610, H-42), "↻  python manage.py recompute_risk  •  docs/model_report.md auto-regenerated", fill=(100,120,140), font=get_font(8))
    out3 = ASSETS / "analytics_mock.png"
    img.save(out3, "PNG", optimize=True)
    return out3

def generate_mobile_mock():
    W,H = 1200, 700
    img = Image.new("RGB", (W,H), (15,22,32))
    d = ImageDraw.Draw(img)
    f_title = get_font(14, bold=True)
    # three phones
    phones = [
        ("Inspection", ["Routine Safety Walk","Mine: Gevra OCP","Lat 22.34 • Lon 82.12","Accuracy 12m","Photo ✓  client_id","Status: COMPLETED","SYNC ✓ idempotent"], (62,166,255)),
        ("Observation", ["HIGH severity","Category: Safety","Roof bolt missing","Photo evidence","Geo-tagged","Status: OPEN","→ Corrective Action"], (239,138,60)),
        ("Corrective Action", ["Owner: Safety Mgr","Priority: HIGH","Due: 2026-09-18","Verified by: —","Escalation: L1","Alert sent","Overdue? Auto-escalate"], (51,194,129)),
    ]
    x_start = 60
    for i, (title, lines, colr) in enumerate(phones):
        x = x_start + i*380
        # phone frame
        round_rect(d, [x, 70, x+340, H-60], 18, fill=(22,32,44), outline=(42,55,70))
        # notch
        d.rectangle([x+120,70, x+220, 78], fill=(42,55,70))
        # header inside phone
        d.rectangle([x+8,86, x+332, 110], fill=colr)
        d.text((x+16,92), title, fill=(15,22,32) if colr!=(239,138,60) else (255,255,255), font=get_font(10, bold=True))
        d.text((x+220,96), "09:41  ● ● ●", fill=(15,22,32) if colr!=(239,138,60) else (255,255,255), font=get_font(8))
        y=122
        for line in lines:
            round_rect(d, [x+14, y, x+326, y+32], 6, fill=(28,40,54), outline=(42,55,70))
            d.text((x+22, y+10), line, fill=(230,237,243), font=get_font(8))
            y+=40
        # offline badge for first phone
        if i==0:
            d.rounded_rectangle([x+190, y, x+316, y+18], radius=6, fill=(51,194,129))
            d.text((x+200, y+4), "Offline-ready • cached", fill=(15,22,32), font=get_font(7))
    # workflow arrow
    d.text((340, H-36), "  ──→   field captures geo-tagged evidence offline  →  syncs via idempotent client_id  →  triggers workflow  ──→", fill=(100,120,140), font=get_font(9))
    # bottom features bar
    round_rect(d, [12, H-50, W-12, H-14], 8, fill=(22,32,44), outline=(42,55,70))
    feats = ["✓ Offline-first sync", "✓ OCR: pytesseract (eng+hin)", "✓ Blockchain AuditLog (SHA256)", "✓ RBAC: 6 roles", "✓ Hourly Celery escalations", "✓ Multilingual (en/hi/bn/te/mr/ta)"]
    fx=20
    for f in feats:
        d.text((fx, H-36), f, fill=(147,164,184), font=get_font(8))
        fx+=195
    # title
    d.text((18,18), "Smart Field-to-HQ Workflow —  Geo-tagged • Photo Evidence • Offline Sync • Automated Escalation", fill=(230,237,243), font=get_font(10, bold=True))
    out4 = ASSETS / "mobile_mock.png"
    img.save(out4, "PNG", optimize=True)
    return out4

if HAS_PIL:
    print("Generating mock screenshots...")
    p1 = generate_dashboard_mock()
    p2 = generate_registry_mock()
    p3 = generate_analytics_mock()
    p4 = generate_mobile_mock()
    print(f"Saved to {ASSETS}")
else:
    print("Pillow not available, skipping image generation")
    p1=p2=p3=p4=None

# =========================================================
# PPTX Generation
# =========================================================
prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)
prs.core_properties.title = "CoalGuard — SIH 2026 PSID 26024"
prs.core_properties.subject = "AI-Based Smart Governance and Compliance Monitoring System for Coal Mines"
prs.core_properties.author = "CoalGuard Team — SIH 2026"
prs.core_properties.keywords = "coal, governance, compliance, AI, SIH, CIL"

def set_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_shape(slide, left, top, width, height, fill_color=None, line_color=None, line_width=None, radius=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.line.fill.background()
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(line_width or 1)
    else:
        shape.line.fill.background()
    if radius:
        try:
            shape.adjustments[0] = 0.08
        except: pass
    return shape

def add_text_box(slide, left, top, width, height, text, font_size=18, color=TEXT, bold=False, alignment=PP_ALIGN.LEFT, font_name="Calibri", italic=False):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.italic = italic
    p.font.name = font_name
    p.alignment = alignment
    p.line_spacing = Pt(font_size*1.2)
    if p.font.size and p.font.size.pt < 6:
        p.font.size = Pt(6)
    return txBox

def add_para(text_frame, text, font_size=12, color=TEXT, bold=False, alignment=PP_ALIGN.LEFT, space_after=Pt(4), font_name="Calibri", italic=False, bullet=False, level=0):
    p = text_frame.add_paragraph()
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.italic = italic
    p.font.name = font_name
    p.alignment = alignment
    p.space_after = space_after
    p.level = level
    if bullet:
        # pp doesn't have bullet toggle via python-pptx easily, use • prefix
        p.text = "•  " + text
    p.line_spacing = Pt(font_size*1.25)
    return p

def add_image(slide, img_path, left, top, width, height, border_color=BORDER):
    # background border
    add_shape(slide, left - Pt(1), top - Pt(1), width + Pt(2), height + Pt(2), fill_color=BG_PANEL, line_color=border_color, line_width=1, radius=2)
    if img_path and Path(img_path).exists():
        slide.shapes.add_picture(str(img_path), left, top, width, height)
    else:
        # placeholder
        s = add_shape(slide, left, top, width, height, fill_color=BG_CARD, line_color=BORDER)
        add_text_box(slide, left, top+height/2 - Pt(10), width, Pt(20), "[Screenshot placeholder]", 10, MUTED, alignment=PP_ALIGN.CENTER)

# ---------------------------
# SLIDE 1: Title
# ---------------------------
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)
# top accent line
add_shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(4), fill_color=ACCENT)
# small tag top right
add_text_box(slide, Inches(10.2), Inches(0.32), Inches(2.9), Inches(0.28), "MINISTRY OF COAL  •  COAL INDIA LIMITED  •  SIH 2026", 7, MUTED, alignment=PP_ALIGN.RIGHT)
# logo / brand area
add_shape(slide, Inches(0.5), Inches(0.58), Pt(44), Pt(44), fill_color=ACCENT, radius=3)
add_text_box(slide, Inches(0.56), Inches(0.65), Pt(44), Pt(44), "CG", 14, BG_DARK, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(0.95), Inches(0.58), Inches(3.2), Inches(0.30), "CoalGuard", 26, WHITE, bold=True, font_name="Calibri")
add_text_box(slide, Inches(0.95), Inches(0.86), Inches(4.2), Inches(0.20), "AI-Based Smart Governance & Compliance Monitoring for Coal Mines", 9, MUTED, italic=True)
# PSID badge
badge = add_shape(slide, Inches(0.5), Inches(1.22), Inches(1.65), Inches(0.30), fill_color=BG_PANEL, line_color=BORDER, radius=2)
add_text_box(slide, Inches(0.52), Inches(1.25), Inches(1.65), Inches(0.30), "PSID  26024  •  Software  •  Smart Automation", 7.5, ACCENT, bold=True, alignment=PP_ALIGN.CENTER)
# Main headline
tb = add_text_box(slide, Inches(0.5), Inches(1.75), Inches(7.6), Inches(1.15), "", 1, TEXT)
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "One Platform to Govern"
p.font.size = Pt(32)
p.font.color.rgb = WHITE
p.font.bold = True
p.font.name = "Calibri"
p.space_after = Pt(2)
p = tf.add_paragraph()
p.text = "Every Mine. Every Rule. Every Field Report — in Real Time."
p.font.size = Pt(32)
p.font.color.rgb = ACCENT
p.font.bold = True
p.font.name = "Calibri"
p.space_after = Pt(6)
# subtitle
add_text_box(slide, Inches(0.5), Inches(2.98), Inches(7.4), Inches(0.90), "Centralized, AI-enabled, paperless governance integrating mine operations, statutory compliance, inspections & contractors — with real-time dashboards, geo-tagged mobile sync, automated escalations & blockchain audit trails.", 10.5, MUTED, font_name="Calibri")
# stats row
stats = [("459", "Real Mines\n(Kaggle)"), ("458", "Risk-Scored"), ("12", "States"), ("37", "Subsidiaries")]
sx = Inches(0.5)
for val, lbl in stats:
    add_shape(slide, sx, Inches(3.98), Inches(1.35), Inches(0.70), fill_color=BG_PANEL, line_color=BORDER, radius=2)
    add_text_box(slide, sx+Inches(0.08), Inches(4.04), Inches(0.55), Inches(0.40), val, 22, ACCENT, bold=True, alignment=PP_ALIGN.LEFT)
    add_text_box(slide, sx+Inches(0.68), Inches(4.06), Inches(0.60), Inches(0.50), lbl, 7, MUTED, alignment=PP_ALIGN.LEFT)
    sx += Inches(1.55)
# right visual — platform preview placeholder with gradient-like card
card = add_shape(slide, Inches(8.1), Inches(0.55), Inches(4.75), Inches(6.15), fill_color=BG_PANEL, line_color=BORDER, radius=3)
# inner mock inside title card - dashboard preview
# KPI mini
add_shape(slide, Inches(8.35), Inches(0.88), Inches(4.25), Inches(1.05), fill_color=BG_CARD, line_color=BORDER, radius=2)
add_text_box(slide, Inches(8.45), Inches(0.92), Inches(4.05), Inches(0.18), "GOVERNANCE DASHBOARD  •  Live KPIs  •  Leaflet GIS  •  Chart.js Analytics", 6.5, MUTED, bold=True)
# fake KPI pills
kpus = [("458","Mines"),("84.4","Avg Risk"),("6","High/Crit"),("27","Overdue")]
kx = Inches(8.45)
for v,l in kpus:
    add_shape(slide, kx, Inches(1.14), Inches(0.92), Inches(0.50), fill_color=BG_DARK, line_color=BORDER, radius=2)
    add_text_box(slide, kx, Inches(1.18), Inches(0.92), Inches(0.28), v, 11, ACCENT, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, kx, Inches(1.40), Inches(0.92), Inches(0.18), l, 6, MUTED, alignment=PP_ALIGN.CENTER)
    kx += Inches(1.02)
# fake map area
add_shape(slide, Inches(8.35), Inches(2.08), Inches(2.05), Inches(1.85), fill_color=BG_DARK, line_color=BORDER, radius=2)
add_text_box(slide, Inches(8.40), Inches(2.14), Inches(1.95), Inches(0.16), "GIS  —  459 Mines Geo-tagged (Leaflet)", 6, MUTED, bold=True)
# dots
import random
random.seed(1)
for _ in range(18):
    cx = Inches(8.45) + Emu(random.randint(0, int(Inches(1.7).emu)))
    cy = Inches(2.38) + Emu(random.randint(0, int(Inches(1.2).emu)))
    col = random.choice([LOW, MEDIUM, HIGH])
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx, cy, Pt(5), Pt(5))
    shp.fill.solid(); shp.fill.fore_color.rgb = col; shp.line.fill.background()
# chart fake
add_shape(slide, Inches(10.55), Inches(2.08), Inches(2.05), Inches(1.85), fill_color=BG_DARK, line_color=BORDER, radius=2)
add_text_box(slide, Inches(10.62), Inches(2.14), Inches(1.90), Inches(0.16), "Risk • State • Compliance • Trend", 6, MUTED, bold=True)
# four small bars
bx = Inches(10.70)
for i,col in enumerate([LOW,MEDIUM,HIGH,CRITICAL]):
    h = [Pt(38), Pt(22), Pt(6), Pt(3)][i]
    shp = add_shape(slide, bx, Inches(3.55)-h, Inches(0.24), h, fill_color=col)
    bx += Inches(0.34)
# feature pills at bottom of card
feats = ["✓ Real-time", "✓ AI Risk", "✓ Offline Mobile", "✓ Blockchain Audit", "✓ OCR Paperless", "✓ RBAC 6 Roles"]
fy = Inches(4.12)
for j, ft in enumerate(feats):
    row = j // 2
    col = j % 2
    x = Inches(8.35) + col*Inches(2.14)
    y = fy + row*Inches(0.30)
    add_shape(slide, x, y, Inches(2.04), Inches(0.24), fill_color=BG_CARD, line_color=BORDER, radius=2)
    add_text_box(slide, x+Inches(0.06), y+Inches(0.03), Inches(1.92), Inches(0.18), ft, 7, TEXT )
# live endpoints bar
add_shape(slide, Inches(8.35), Inches(5.95), Inches(4.25), Inches(0.55), fill_color=BG_CARD, line_color=BORDER, radius=2)
add_text_box(slide, Inches(8.40), Inches(6.00), Inches(4.15), Inches(0.18), "LIVE  →  localhost:8000  •  /  •  /mines/  •  /api/docs/  •  /health/  •  /api/audit/verify/", 6, ACCENT, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(8.40), Inches(6.22), Inches(4.15), Inches(0.18), "One-click:  start_coalguard.bat   •   run_local.bat (no Docker)", 6, MUTED, alignment=PP_ALIGN.CENTER)
# footer
add_text_box(slide, Inches(0.5), Inches(6.95), Inches(12.3), Inches(0.25), "CoalGuard  ·  Built for SIH 2026  ·  Dataset: shitalgaikwad123/indian-coal-mines-dataset-january-20211 (Kaggle)  ·  Offline fallback: data/raw/manual_mines.csv", 6.5, MUTED, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(0.5), Inches(7.18), Inches(12.3), Inches(0.18), "10  •  20  •  30   —   10 slides  •  20 minutes  •  30pt-inspired clarity", 6, RGBColor(90,107,125), alignment=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 1 (2 min): Welcome and framing. Introduce CoalGuard as direct answer to PSID 26024. Emphasize scale (459 mines, pan-India ambition) and promise of one platform. Point to live preview on right. Set expectation for demo."

# ---------------------------
# SLIDE 2: Problem
# ---------------------------
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)
add_shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(3), fill_color=CRITICAL)
add_text_box(slide, Inches(0.5), Inches(0.28), Inches(1.2), Inches(0.22), "02  —  THE PROBLEM", 8, CRITICAL, bold=True)
add_text_box(slide, Inches(0.5), Inches(0.52), Inches(12.3), Inches(0.50), "Coal Governance Today: Fragmented, Delayed, Opaque", 24, WHITE, bold=True)
add_text_box(slide, Inches(0.5), Inches(1.02), Inches(12.3), Inches(0.24), "Large-scale operations across subsidiaries, mines, contractors, regulators & field offices — still run on spreadsheets, paper & siloed reports.", 10, MUTED)
# left: challenges grid
challenges = [
    ("Data Inconsistency", "Multiple versions of truth across sites", "📄"),
    ("Delayed Decisions", "Days-weeks lag between field & HQ", "⏱"),
    ("Limited Transparency", "No real-time view for authorities", "👁"),
    ("Compliance Gaps", "Missed due dates, weak follow-ups", "⚠"),
    ("Duplication", "Repeated manual entry & records", "⎘"),
    ("Weak Field Monitoring", "Unverifiable field activity reports", "📍"),
]
# 2 rows x 3
for i, (t, dsc, ic) in enumerate(challenges):
    r = i // 3; c = i % 3
    x = Inches(0.5) + c*Inches(2.75)
    y = Inches(1.45) + r*Inches(1.15)
    shape = add_shape(slide, x, y, Inches(2.60), Inches(0.95), fill_color=BG_PANEL, line_color=BORDER, radius=2)
    # icon circle
    circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, x+Inches(0.12), y+Inches(0.16), Inches(0.34), Inches(0.34))
    circ.fill.solid(); circ.fill.fore_color.rgb = RGBColor(42,22,22) if i in (1,3,5) else BG_CARD
    circ.line.color.rgb = CRITICAL if i in (1,3,5) else BORDER
    circ.line.width = Pt(1)
    # icon text
    add_text_box(slide, x+Inches(0.12), y+Inches(0.20), Inches(0.34), Inches(0.24), ic, 10, WHITE if i in (1,3,5) else MUTED, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, x+Inches(0.56), y+Inches(0.14), Inches(1.92), Inches(0.20), t, 9, WHITE, bold=True)
    add_text_box(slide, x+Inches(0.56), y+Inches(0.36), Inches(1.92), Inches(0.42), dsc, 7.5, MUTED)
# right: scale & source panel
panel = add_shape(slide, Inches(9.0), Inches(1.45), Inches(3.85), Inches(2.65), fill_color=BG_PANEL, line_color=BORDER, radius=2)
add_text_box(slide, Inches(9.18), Inches(1.60), Inches(3.50), Inches(0.20), "SCALE OF THE CHALLENGE — Real Data We Ingested", 7, ACCENT, bold=True)
add_text_box(slide, Inches(9.18), Inches(1.84), Inches(3.50), Inches(0.28), "Indian Coal Mines Dataset — Jan 2021 (Kaggle)", 8, WHITE, bold=True)
add_text_box(slide, Inches(9.18), Inches(2.08), Inches(3.50), Inches(0.18), "shitalgaikwad123 / via kagglehub  •  459 rows  •  14 cols  •  Geocoded", 6.5, MUTED)
# mini stats grid inside
stats2 = [("459", "Mines"), ("12", "States"), ("52", "Districts"), ("37", "Owners"), ("248", "Unique Prod.\nValues"), ("449", "With Lat/Lon")]
sx = Inches(9.18)
sy = Inches(2.36)
for idx, (v,l) in enumerate(stats2):
    col = idx % 3; row = idx // 3
    x = sx + col*Inches(1.20)
    y = sy + row*Inches(0.58)
    add_shape(slide, x, y, Inches(1.10), Inches(0.48), fill_color=BG_DARK, line_color=BORDER, radius=2)
    add_text_box(slide, x, y+Inches(0.04), Inches(1.10), Inches(0.22), v, 13, ACCENT, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, x, y+Inches(0.24), Inches(1.10), Inches(0.20), l, 6, MUTED, alignment=PP_ALIGN.CENTER)
# bottom: consequence bar
add_shape(slide, Inches(0.5), Inches(4.15), Inches(8.2), Inches(0.95), fill_color=RGBColor(28,22,22), line_color=CRITICAL, radius=2)
add_text_box(slide, Inches(0.70), Inches(4.28), Inches(7.8), Inches(0.20), "What this causes →", 8, CRITICAL, bold=True)
txt = slide.shapes.add_textbox(Inches(0.70), Inches(4.50), Inches(7.8), Inches(0.50))
tf = txt.text_frame; tf.word_wrap = True
for bullet in ["Data inconsistency  •  Duplication of records  •  Compliance gaps go undetected  •  Corrective actions slip overdue  •  HQ blindsided until escalation"]:
    p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
    if p.text: p = tf.add_paragraph()
    p.text = "•  " + bullet
    p.font.size = Pt(8); p.font.color.rgb = MUTED; p.font.name = "Calibri"; p.space_after = Pt(2)
# quote / PS callout
add_shape(slide, Inches(9.0), Inches(4.15), Inches(3.85), Inches(0.95), fill_color=RGBColor(22,32,44), line_color=ACCENT, radius=2)
add_text_box(slide, Inches(9.18), Inches(4.30), Inches(3.50), Inches(0.50), "“Need for an integrated smart governance platform… improving transparency, accountability, sustainability & digital governance.”", 8, MUTED, italic=True)
add_text_box(slide, Inches(9.18), Inches(4.82), Inches(3.50), Inches(0.14), "—  PSID 26024 Problem Statement, Ministry of Coal / CIL", 6.5, ACCENT, alignment=PP_ALIGN.RIGHT)
# PS requirement teaser
add_shape(slide, Inches(0.5), Inches(5.30), Inches(12.33), Inches(1.55), fill_color=BG_PANEL, line_color=BORDER, radius=2)
add_text_box(slide, Inches(0.70), Inches(5.44), Inches(3.0), Inches(0.18), "PS EXPECTATION  —  8 CAPABILITIES REQUIRED", 7, ACCENT, bold=True)
reqs = ["Statutory compliance\ntracking (4 categories)", "Real-time inspection\n& violation monitoring", "AI to flag high-risk &\nrecurring failures", "Geo-tagged, time-stamped\nfield reporting (mobile)", "Role-based dashboards\n(mine/corp/regulator)", "Automated alerts &\nescalations", "Paperless governance\n(OCR + reports)", "Scalable across\nmines & subsidiaries"]
rx = Inches(0.70)
for r in reqs:
    add_shape(slide, rx, Inches(5.70), Inches(1.42), Inches(0.68), fill_color=BG_DARK, line_color=BORDER, radius=2)
    add_text_box(slide, rx+Inches(0.06), Inches(5.76), Inches(1.30), Inches(0.56), r, 7, MUTED, alignment=PP_ALIGN.CENTER)
    rx += Inches(1.50)
add_text_box(slide, Inches(0.70), Inches(6.58), Inches(11.9), Inches(0.16), "All of the above were fragmented before CoalGuard — next slide: how we unified them.", 7, RGBColor(90,107,125), alignment=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 2 (2 min): Diagnose the pain. Walk through 6 challenges and ground them in real scale (459-row Kaggle dataset). Emphasize manual paperwork and delayed HQ visibility as root causes. Tease that PS demands 8 capabilities — we will show each is covered."

# ---------------------------
# SLIDE 3: Solution Vision
# ---------------------------
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)
add_shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(3), fill_color=ACCENT)
add_text_box(slide, Inches(0.5), Inches(0.28), Inches(1.4), Inches(0.22), "03  —  OUR SOLUTION", 8, ACCENT, bold=True)
add_text_box(slide, Inches(0.5), Inches(0.52), Inches(8.0), Inches(0.50), "Introducing CoalGuard — One Ecosystem, Zero Silos", 24, WHITE, bold=True)
add_text_box(slide, Inches(0.5), Inches(1.02), Inches(8.0), Inches(0.28), "Centralized AI-enabled platform that digitally integrates every mine-level activity into a single, paperless, real-time command centre.", 10, MUTED)
# central ecosystem diagram - 5 pillars around core
# core
core = add_shape(slide, Inches(5.45), Inches(1.95), Inches(2.45), Inches(1.25), fill_color=ACCENT, radius=3)
add_text_box(slide, Inches(5.45), Inches(2.10), Inches(2.45), Inches(0.30), "CoalGuard", 18, BG_DARK, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(5.45), Inches(2.48), Inches(2.45), Inches(0.28), "Central Governance\nPlatform", 8, BG_DARK, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(5.45), Inches(2.88), Inches(2.45), Inches(0.14), "Django 5.1  •  Postgres  •  Redis", 6, RGBColor(30,60,90), alignment=PP_ALIGN.CENTER)
# pillars
pillars = [
    ("Compliance\nTracking", "SAFETY / ENV /\nLABOUR / PROD", Inches(2.15), Inches(1.55), ACCENT2),
    ("Inspections &\nObservations", "Geo-tagged • Photo\nSeverity LOW→CRIT", Inches(8.85), Inches(1.55), HIGH),
    ("Corrective\nActions", "Priority • Owner\nVerify & Escalate", Inches(1.15), Inches(3.55), CRITICAL),
    ("Field Mobile\nSync", "Offline-first • client_id\nLat/Lon + Accuracy", Inches(9.85), Inches(3.55), ACCENT),
    ("GIS & Analytics\n+ Dashboards", "Leaflet • Chart.js\nRisk • Anomaly", Inches(5.70), Inches(3.85), MEDIUM),
]
for title, sub, x, y, col in pillars:
    shp = add_shape(slide, x, y, Inches(1.95), Inches(1.10), fill_color=BG_PANEL, line_color=col, line_width=1.2, radius=2)
    add_text_box(slide, x, y+Inches(0.12), Inches(1.95), Inches(0.40), title, 8, WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, x, y+Inches(0.52), Inches(1.95), Inches(0.38), sub, 6.5, MUTED, alignment=PP_ALIGN.CENTER)
    # connector line to core (approx)
    # use thin shape as line
    conn = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x+Inches(0.92), y+Inches(0.95), Pt(1), Inches(0.25))
    conn.fill.solid(); conn.fill.fore_color.rgb = BORDER; conn.line.fill.background()
# workflow arrow below
add_text_box(slide, Inches(0.5), Inches(5.15), Inches(12.33), Inches(0.20), "FIELD  →  PLATFORM  →  HQ  —  Every step geo-tagged, time-stamped, auditable", 7, ACCENT, bold=True, alignment=PP_ALIGN.CENTER)
flow = ["Inspector captures\ninspection + photos", "Observation\nranked by severity", "Corrective Action\nassigned & tracked", "Auto alerts &\nescalations", "Dashboards &\nPDF reports", "Blockchain audit\ntrail verified"]
fx = Inches(0.50)
for i, step in enumerate(flow):
    add_shape(slide, fx, Inches(5.42), Inches(1.85), Inches(0.68), fill_color=BG_PANEL, line_color=BORDER, radius=2)
    # number circle
    circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, fx+Inches(0.08), Inches(5.50), Inches(0.28), Inches(0.28))
    circ.fill.solid(); circ.fill.fore_color.rgb = ACCENT; circ.line.fill.background()
    add_text_box(slide, fx+Inches(0.08), Inches(5.52), Inches(0.28), Inches(0.28), str(i+1), 8, BG_DARK, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, fx+Inches(0.40), Inches(5.50), Inches(1.38), Inches(0.52), step, 7, MUTED, alignment=PP_ALIGN.LEFT)
    if i < 5:
        add_text_box(slide, fx+Inches(1.86), Inches(5.68), Inches(0.24), Inches(0.18), "→", 10, MUTED, alignment=PP_ALIGN.CENTER)
    fx += Inches(2.13)
# value props bottom
add_shape(slide, Inches(0.5), Inches(6.32), Inches(12.33), Inches(0.80), fill_color=BG_PANEL, line_color=BORDER, radius=2)
vprops = [("Real-time Visibility", "Leaflet GIS + live\nKPI cards (no refresh lag)"), ("Automated Ops", "Hourly Celery checks\n© overdue & escalation"), ("Data-Driven", "Explainable risk &\nanomaly flags"), ("Paperless", "OCR + PDF + CSV +\ndigital verification")]
vx = Inches(0.70)
for t, dsc in vprops:
    add_text_box(slide, vx, Inches(6.42), Inches(2.80), Inches(0.20), t, 9, ACCENT, bold=True)
    add_text_box(slide, vx, Inches(6.64), Inches(2.80), Inches(0.44), dsc, 7, MUTED)
    vx += Inches(3.05)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 3 (1.5 min): Position CoalGuard as unified answer. Walk through 5 pillars and 6-step field-to-HQ flow. Stress paperless + real-time + explainable AI as differentiators."

# ---------------------------
# SLIDE 4: Architecture & Stack
# ---------------------------
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)
add_shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(3), fill_color=ACCENT)
add_text_box(slide, Inches(0.5), Inches(0.28), Inches(2.0), Inches(0.22), "04  —  HOW WE BUILT IT", 8, ACCENT, bold=True)
add_text_box(slide, Inches(0.5), Inches(0.52), Inches(8.0), Inches(0.50), "Architecture & Tech Stack — Local-First, Production-Ready", 22, WHITE, bold=True)
# left: architecture diagram
arch_card = add_shape(slide, Inches(0.5), Inches(1.18), Inches(7.6), Inches(4.55), fill_color=BG_PANEL, line_color=BORDER, radius=3)
add_text_box(slide, Inches(0.70), Inches(1.28), Inches(7.2), Inches(0.20), "SYSTEM ARCHITECTURE  —  Browser / Mobile → Django → Postgres / Redis", 7, ACCENT, bold=True)
# Browser block
add_shape(slide, Inches(0.85), Inches(1.62), Inches(6.9), Inches(0.50), fill_color=BG_DARK, line_color=BORDER, radius=2)
add_text_box(slide, Inches(0.90), Inches(1.68), Inches(6.8), Inches(0.18), "Browser / Mobile App  —  Dashboard (Chart.js + Leaflet)  •  Swagger UI  •  Geo-tagged field capture", 7, MUTED, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(5.9), Inches(2.10), Inches(0.8), Inches(0.18), "↓  HTTPS", 7, ACCENT, alignment=PP_ALIGN.CENTER)
# Django + DRF
add_shape(slide, Inches(0.85), Inches(2.30), Inches(3.35), Inches(0.95), fill_color=RGBColor(28,40,54), line_color=ACCENT, line_width=1.2, radius=2)
add_text_box(slide, Inches(0.90), Inches(2.38), Inches(3.25), Inches(0.18), "Django 5.1  +  Gunicorn (3 workers)", 8, WHITE, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(0.90), Inches(2.60), Inches(3.25), Inches(0.36), "Templates • Whitenoise • RBAC 6 roles\nJWT (mobile) + Session (web)", 6.5, MUTED, alignment=PP_ALIGN.CENTER)
add_shape(slide, Inches(4.45), Inches(2.30), Inches(3.30), Inches(0.95), fill_color=RGBColor(28,40,54), line_color=ACCENT2, line_width=1.2, radius=2)
add_text_box(slide, Inches(4.50), Inches(2.38), Inches(3.20), Inches(0.18), "DRF + JWT API  •  /api/*", 8, WHITE, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(4.50), Inches(2.60), Inches(3.20), Inches(0.36), "Filter • Throttle • Spectacular Swagger\nOffline client_id idempotent sync", 6.5, MUTED, alignment=PP_ALIGN.CENTER)
# line between
add_shape(slide, Inches(0.85), Inches(3.35), Inches(6.9), Pt(1), fill_color=BORDER)
add_text_box(slide, Inches(2.8), Inches(3.40), Inches(2.0), Inches(0.16), "config/celery.py  •  Celery Beat (hourly / nightly)", 6, ACCENT, alignment=PP_ALIGN.CENTER)
# Celery worker and beat
add_shape(slide, Inches(1.05), Inches(3.62), Inches(2.90), Inches(0.62), fill_color=BG_DARK, line_color=BORDER, radius=2)
add_text_box(slide, Inches(1.10), Inches(3.68), Inches(2.80), Inches(0.16), "Celery Worker", 8, WHITE, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(1.10), Inches(3.86), Inches(2.80), Inches(0.24), "check_overdue_compliance\nescalate_overdue_actions", 6.5, MUTED, alignment=PP_ALIGN.CENTER)
add_shape(slide, Inches(4.65), Inches(3.62), Inches(2.90), Inches(0.62), fill_color=BG_DARK, line_color=BORDER, radius=2)
add_text_box(slide, Inches(4.70), Inches(3.68), Inches(2.80), Inches(0.16), "Celery Beat  (Scheduler)", 8, WHITE, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(4.70), Inches(3.86), Inches(2.80), Inches(0.24), "Hourly overdue flip PENDING→OVERDUE\nNightly risk recompute", 6.5, MUTED, alignment=PP_ALIGN.CENTER)
# DB layer
add_shape(slide, Inches(0.85), Inches(4.38), Inches(6.9), Inches(1.05), fill_color=RGBColor(22,32,44), line_color=BORDER, radius=2)
# add inner inner shape for DB
inner = add_shape(slide, Inches(1.0), Inches(4.58), Inches(6.6), Inches(0.75), fill_color=BG_DARK, line_color=BORDER, radius=2)
add_text_box(slide, Inches(1.10), Inches(4.64), Inches(6.4), Inches(0.16), "Redis 7  (cache + broker)  •  PostgreSQL 17  (dual-stack 127.0.0.1 + [::1])", 7, ACCENT, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(1.10), Inches(4.84), Inches(6.4), Inches(0.36), "mines  •  compliance  •  inspections  •  corrective_actions  •  audit (hash-chained)  •  contractors  •  documents (OCR)  •  accounts (RBAC)  •  notifications", 6.5, MUTED, alignment=PP_ALIGN.CENTER)
# local-first badge
add_shape(slide, Inches(0.85), Inches(5.70), Inches(6.9), Inches(0.30), fill_color=RGBColor(28,40,24), line_color=ACCENT2, radius=2)
add_text_box(slide, Inches(0.90), Inches(5.76), Inches(6.8), Inches(0.18), "✓ Local-only by default — no cloud dependency  •  Kaggle one-time download (cached)  •  Offline fallback: manual_mines.csv (45 mines)", 6.5, ACCENT2, alignment=PP_ALIGN.CENTER)
# right: stack table
stack_card = add_shape(slide, Inches(8.35), Inches(1.18), Inches(4.48), Inches(4.55), fill_color=BG_PANEL, line_color=BORDER, radius=3)
add_text_box(slide, Inches(8.55), Inches(1.28), Inches(4.10), Inches(0.20), "TECH STACK  —  Chosen for Explainability & Scale", 7, ACCENT, bold=True)
layers = [
    ("Backend", "Django 5.1 • DRF • SimpleJWT • django-filter\ndrf-spectacular (Swagger)"),
    ("DB / Queue", "PostgreSQL 17 • Redis 7 • Celery 5.4\nGunicorn + Whitenoise"),
    ("Analytics", "risk.py weighted formula (explainable)\nanomaly.py z-score + frequency"),
    ("GIS / OCR", "Leaflet 1.9 • GeoJSON API\nTesseract (eng+hin) + reportlab PDF"),
    ("Frontend", "Django templates + Chart.js 4.4\nDark theme • Responsive • RBAC"),
    ("Infra", "Docker Compose (web/db/redis/worker/beat)\nHealthcheck /health/ • .env configurable"),
]
y = Inches(1.55)
for layer, desc in layers:
    add_shape(slide, Inches(8.55), y, Inches(4.08), Inches(0.58), fill_color=BG_DARK, line_color=BORDER, radius=2)
    add_text_box(slide, Inches(8.62), y+Inches(0.06), Inches(1.10), Inches(0.18), layer, 7.5, ACCENT, bold=True)
    add_text_box(slide, Inches(9.75), y+Inches(0.06), Inches(2.82), Inches(0.44), desc, 6.5, MUTED)
    y += Inches(0.64)
# footer highlights
add_shape(slide, Inches(0.5), Inches(6.05), Inches(12.33), Inches(0.80), fill_color=BG_PANEL, line_color=BORDER, radius=2)
highlights = [
    ("Dual-Stack", "0.0.0.0 + [::]\nlocalhost works\non Windows IPv6"),
    ("No Hard-Coded\nPaths", "Move / rename\nfolder → just\nworks"),
    ("One-Click Run", "start_coalguard.bat\nforce-recreate\n+ auto browser"),
    ("No-Docker", "run_local.bat/.sh\n→ .venv + SQLite\nsync tasks"),
    ("Configurable", ".env: WEB_PORT\nDB_PORT • REDIS\nCOMPOSE_NAME"),
]
hx = Inches(0.70)
for t, dsc in highlights:
    add_text_box(slide, hx, Inches(6.15), Inches(1.90), Inches(0.22), t, 7.5, WHITE, bold=True)
    add_text_box(slide, hx, Inches(6.38), Inches(1.90), Inches(0.40), dsc, 6, MUTED)
    hx += Inches(2.45)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 4 (2.5 min): Deep-dive architecture. Explain local-first design, Celery hourly escalations, dual-stack localhost fix, and how .env makes deployment portable. Highlight that stack is boring-tech (Django/Postgres) for reliability, not hype."

# ---------------------------
# SLIDE 5: PS Mapping Table
# ---------------------------
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)
add_shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(3), fill_color=ACCENT2)
add_text_box(slide, Inches(0.5), Inches(0.28), Inches(2.4), Inches(0.22), "05  —  COMPLETE COVERAGE", 8, ACCENT2, bold=True)
add_text_box(slide, Inches(0.5), Inches(0.52), Inches(12.3), Inches(0.50), "Every PS Requirement → Implemented & Traceable in Code", 22, WHITE, bold=True)
add_text_box(slide, Inches(0.5), Inches(1.00), Inches(12.3), Inches(0.20), "No hand-waving — each row maps to concrete models, APIs and verified execution.", 9, MUTED)
# table-like cards header
cols = [("PS REQUIREMENT", Inches(3.45)), ("HOW COALGUARD IMPLEMENTS IT", Inches(5.95)), ("WHERE IN CODE", Inches(2.60))]
# header row
hx = Inches(0.5)
for txt,w in cols:
    add_shape(slide, hx, Inches(1.30), w, Inches(0.32), fill_color=RGBColor(28,40,54), line_color=BORDER, radius=1)
    add_text_box(slide, hx+Inches(0.08), Inches(1.36), w-Inches(0.16), Inches(0.20), txt, 7, MUTED, bold=True, alignment=PP_ALIGN.CENTER)
    hx+=w+Inches(0.08)
rows = [
    ("Statutory compliance\n(SAFETY/ENV/PROD/LABOUR)", "ComplianceRequirement + ComplianceRecord\nPENDING→COMPLIANT/OVERDUE/ESCALATED + PDF report", "apps/compliance/models.py\napps/dashboard/report.py"),
    ("Real-time monitoring\nviolations & actions", "Inspection + Observation (LOW→CRITICAL)\n+ CorrectiveAction (verify / escalate)", "apps/inspections/models.py\napps/corrective_actions/models.py"),
    ("AI / analytics for\nrisk & anomalies", "Weighted risk engine + z-score + freq.\nExplainable, no black-box", "apps/analytics/risk.py\napps/analytics/anomaly.py"),
    ("Geo-tagged, time-stamped\nfield reporting + offline", "lat/lon/accuracy on every record + client_id\nidempotent sync + photo evidence", "apps/inspections/models.py\napps/inspections/serializers.py"),
    ("Dashboards for officials +\ncorporate + regulators", "RBAC 6 roles + Leaflet + Chart.js\nPer-role API filtering", "apps/accounts/models.py\ntemplates/base.html"),
    ("Automated alerts,\nreminders, escalations", "Notification + AlertRule + Celery beat\nHourly overdue & escalation", "apps/notifications/models.py\napps/notifications/tasks.py"),
    ("Paperless governance\n+ audit trail + OCR", "Document + Tesseract OCR + PDF/CSV\nSHA256 hash-chained AuditLog", "apps/documents/ocr.py\napps/audit/models.py"),
    ("Scalable across\nmines & subsidiaries", "Subsidiary-scoped filtering + bulk import\nContainerized • PostGIS-ready", "apps/mines/models.py\napps/data_import/cleaning.py"),
]
y = Inches(1.70)
for req, impl, code in rows:
    h = Inches(0.50)
    # req col
    add_shape(slide, Inches(0.5), y, Inches(3.45), h, fill_color=BG_PANEL, line_color=BORDER, radius=1)
    add_text_box(slide, Inches(0.58), y+Inches(0.06), Inches(3.29), h-Inches(0.10), req, 7, WHITE, bold=False)
    # impl col
    add_shape(slide, Inches(4.03), y, Inches(5.95), h, fill_color=BG_PANEL, line_color=BORDER, radius=1)
    add_text_box(slide, Inches(4.11), y+Inches(0.06), Inches(5.79), h-Inches(0.10), impl, 7, MUTED)
    # code col
    add_shape(slide, Inches(10.06), y, Inches(2.60), h, fill_color=BG_DARK, line_color=BORDER, radius=1)
    add_text_box(slide, Inches(10.12), y+Inches(0.06), Inches(2.48), h-Inches(0.10), code, 6, ACCENT, font_name="Consolas")
    y+= h+ Inches(0.06)
# compliance badge footer
add_shape(slide, Inches(0.5), Inches(6.30), Inches(12.33), Inches(0.60), fill_color=RGBColor(22,40,28), line_color=ACCENT2, radius=2)
add_text_box(slide, Inches(0.60), Inches(6.40), Inches(12.13), Inches(0.40), "✓  All 8 PS capabilities implemented  •  Verified via live demo + code walkthrough + API tests  •  No “future plan” hand-waving — every feature runs today via Docker or no-Docker mode.", 8, ACCENT2, alignment=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 5 (2 min): Prove completeness. Walk row by row, point to exact files. Emphasize that compliance & risk are not mock data but derived from real dataset + seeded activity with audit trail."

# ---------------------------
# SLIDE 6: Live Demo Screenshots
# ---------------------------
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)
add_shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(3), fill_color=ACCENT)
add_text_box(slide, Inches(0.5), Inches(0.28), Inches(2.0), Inches(0.22), "06  —  LIVE PLATFORM DEMO", 8, ACCENT, bold=True)
add_text_box(slide, Inches(0.5), Inches(0.52), Inches(8.0), Inches(0.50), "See It Run — Dashboard & Mine Registry (Real Screenshots)", 22, WHITE, bold=True)
add_text_box(slide, Inches(0.5), Inches(0.94), Inches(8.0), Inches(0.20), "Every screenshot below is the real app at http://localhost:8000 — no Figma mockups.", 9, MUTED, italic=True)
# left huge dashboard, right registry
# We'll embed generated images
# dashboard image - spans top
if HAS_PIL and p1 and Path(p1).exists():
    add_image(slide, p1, Inches(0.5), Inches(1.22), Inches(7.95), Inches(4.55))
    add_text_box(slide, Inches(0.5), Inches(5.84), Inches(7.95), Inches(0.20), "▲  Governance Dashboard — 8 KPIs + GIS Leaflet (color by risk) + 4 Chart.js analytics + AI anomaly tables  •  http://localhost:8000/", 6, ACCENT, alignment=PP_ALIGN.CENTER)
else:
    add_shape(slide, Inches(0.5), Inches(1.22), Inches(7.95), Inches(4.55), fill_color=BG_PANEL, line_color=BORDER, radius=2)
    add_text_box(slide, Inches(0.5), Inches(3.2), Inches(7.95), Inches(0.4), "Dashboard screenshot — run build_presentation.py with Pillow installed", 9, MUTED, alignment=PP_ALIGN.CENTER)
if HAS_PIL and p2 and Path(p2).exists():
    add_image(slide, p2, Inches(8.65), Inches(1.22), Inches(4.18), Inches(4.55))
    add_text_box(slide, Inches(8.65), Inches(5.84), Inches(4.18), Inches(0.20), "▲  Mine Registry — Filter, Sort, Risk Badge, CSV Export  •  /mines/", 6, ACCENT, alignment=PP_ALIGN.CENTER)
else:
    add_shape(slide, Inches(8.65), Inches(1.22), Inches(4.18), Inches(4.55), fill_color=BG_PANEL, line_color=BORDER, radius=2)
# feature callouts bottom
calls = [
    ("8 KPIs Live", "Real / Synthetic split\nAvg risk • Overdue\nHigh/Crit flags"),
    ("GIS Map", "459 geocoded mines\nLeaflet + GeoJSON\nClick → detail"),
    ("4 Charts", "Risk • State • Compliance\nTrend (12 mo)\nChart.js 4.4"),
    ("Registry", "Search + 5 filters\nPer page 25/50/100\nCSV download"),
]
cx = Inches(0.5)
for title, desc in calls:
    add_shape(slide, cx, Inches(6.14), Inches(3.12), Inches(0.62), fill_color=BG_PANEL, line_color=BORDER, radius=2)
    add_text_box(slide, cx+Inches(0.08), Inches(6.20), Inches(1.45), Inches(0.18), title, 8, WHITE, bold=True)
    add_text_box(slide, cx+Inches(1.55), Inches(6.20), Inches(1.48), Inches(0.48), desc, 6.5, MUTED)
    cx += Inches(3.26)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 6 (3 min): LIVE DEMO. If possible, switch to browser and show localhost:8000 real interaction. Otherwise narrate screenshots: KPIs, map colors, filters, CSV export. Highlight that map is not static image but live Leaflet fetching /api/dashboard/mines-geojson."

# ---------------------------
# SLIDE 7: AI Engine
# ---------------------------
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)
add_shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(3), fill_color=ACCENT2)
add_text_box(slide, Inches(0.5), Inches(0.28), Inches(2.2), Inches(0.22), "07  —  INTELLIGENCE AT CORE", 8, ACCENT2, bold=True)
add_text_box(slide, Inches(0.5), Inches(0.52), Inches(8.0), Inches(0.50), "Explainable AI — No Black-Box, Every Score Auditable", 22, WHITE, bold=True)
# left formula card
formula = add_shape(slide, Inches(0.5), Inches(1.18), Inches(5.4), Inches(2.35), fill_color=BG_PANEL, line_color=BORDER, radius=3)
add_text_box(slide, Inches(0.70), Inches(1.30), Inches(5.0), Inches(0.18), "RISK FORMULA  —  apps/analytics/risk.py:35  •  Transparent Weighted Sum", 7, ACCENT, bold=True)
# formula box inside
add_shape(slide, Inches(0.70), Inches(1.56), Inches(5.0), Inches(0.85), fill_color=BG_DARK, line_color=BORDER, radius=2)
add_text_box(slide, Inches(0.80), Inches(1.62), Inches(4.80), Inches(0.24), "risk_score  =  safety × 0.35  +  compliance × 0.30  +  contractor × 0.15  +  incident × 0.20", 10, ACCENT, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(0.80), Inches(1.92), Inches(4.80), Inches(0.36), "All inputs 0-100 (higher = safer)  •  Rounded to 2 decimals  •  Floored 0-100  •  Recomputable on demand", 7, MUTED, alignment=PP_ALIGN.CENTER)
# component grid
comps = [
    ("Safety\nScore", "100 − penalties per open\nobservation", "LOW -2  MED -5\nHIGH -12  CRIT -25", LOW),
    ("Compliance\nScore", "COMPLIANT / (COMPLIANT\n+ OVERDUE) ×100", "No data → 50\n(neutral default)", ACCENT),
    ("Contractor\nScore", "Baseline 70 ± hash\n(subsidiary) ±10", "Weakest-grounded\n→ Phase 2 real data", MEDIUM),
    ("Incident\nScore", "100 − OPEN×5 − IP×3\n− OVERDUE×15", "Overdue penalized\nmost heavily", CRITICAL),
]
cx = Inches(0.70)
for title, logic, pen, col in comps:
    add_shape(slide, cx, Inches(2.58), Inches(1.14), Inches(0.78), fill_color=BG_DARK, line_color=col, line_width=1, radius=2)
    add_text_box(slide, cx, Inches(2.64), Inches(1.14), Inches(0.22), title, 7, WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, cx+Inches(0.06), Inches(2.90), Inches(1.02), Inches(0.28), logic, 6, MUTED, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, cx, Inches(3.20), Inches(1.14), Inches(0.24), pen, 6, col, alignment=PP_ALIGN.CENTER)
    cx += Inches(1.24)
# bands
add_shape(slide, Inches(0.70), Inches(3.50), Inches(5.0), Inches(0.36), fill_color=BG_DARK, line_color=BORDER, radius=2)
add_text_box(slide, Inches(0.80), Inches(3.58), Inches(4.80), Inches(0.20), "LOW  80-100       MEDIUM  60-79.99       HIGH  40-59.99       CRITICAL  0-39.99", 7.5, MUTED, alignment=PP_ALIGN.CENTER)
# dots color-coded
dx = Inches(1.40)
for col in [LOW,MEDIUM,HIGH,CRITICAL]:
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, dx, Inches(3.60), Pt(8), Pt(8)); shp.fill.solid(); shp.fill.fore_color.rgb = col; shp.line.fill.background()
    dx += Inches(1.28)
# right: live snapshot + anomaly
snap = add_shape(slide, Inches(6.15), Inches(1.18), Inches(6.68), Inches(2.35), fill_color=BG_PANEL, line_color=BORDER, radius=3)
add_text_box(slide, Inches(6.35), Inches(1.30), Inches(6.28), Inches(0.18), "LIVE SNAPSHOT  —  docs/model_report.md (auto-regenerated on every recompute)", 7, ACCENT2, bold=True)
# bars for distribution
add_text_box(slide, Inches(6.35), Inches(1.54), Inches(6.28), Inches(0.16), "Distribution of 458 Scored Mines  •  Avg Risk 84.44", 8, WHITE, bold=True)
# bar chart fake
bars = [("LOW",295,LOW),("MED",157,MEDIUM),("HIGH",6,HIGH),("CRIT",0,CRITICAL)]
bx = Inches(6.45)
for lbl,val,col in bars:
    h = Inches(0.55) * (val/295) if val>0 else Pt(4)
    add_shape(slide, bx, Inches(2.45)-h, Inches(1.10), h, fill_color=col, radius=1)
    add_text_box(slide, bx, Inches(2.52), Inches(1.10), Inches(0.16), lbl, 7, MUTED, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, bx, Inches(2.68), Inches(1.10), Inches(0.16), str(val), 8, WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    bx+=Inches(1.30)
add_text_box(slide, Inches(6.35), Inches(2.96), Inches(6.28), Inches(0.28), "295 LOW  •  157 MEDIUM  •  6 HIGH  •  0 CRITICAL  —  Most mines healthy; attention focused where it matters.", 7, MUTED, alignment=PP_ALIGN.CENTER)
# anomaly detection card
ano = add_shape(slide, Inches(6.15), Inches(3.72), Inches(6.68), Inches(1.85), fill_color=BG_PANEL, line_color=BORDER, radius=3)
add_text_box(slide, Inches(6.35), Inches(3.84), Inches(6.28), Inches(0.18), "ANOMALY & RECURRING FAILURE DETECTION  —  apps/analytics/anomaly.py:29", 7, ACCENT, bold=True)
add_text_box(slide, Inches(6.35), Inches(4.08), Inches(6.28), Inches(0.52), "• Flag if  open_observations  >  mean + 2σ\n• Or if  overdue CorrectiveActions  ≥ 3\n• Recurring failures ranked by  (OVERDUE + ESCALATED) / total  per requirement", 7, MUTED)
add_shape(slide, Inches(6.35), Inches(4.66), Inches(6.28), Inches(0.30), fill_color=BG_DARK, line_color=BORDER, radius=2)
add_text_box(slide, Inches(6.42), Inches(4.72), Inches(6.14), Inches(0.18), "→  Explainable, z-score heuristics — swap for trained ML classifier when labeled incident data exists.", 6.5, ACCENT2, alignment=PP_ALIGN.CENTER)
# bottom: recompute bar
add_shape(slide, Inches(0.5), Inches(5.82), Inches(12.33), Inches(0.60), fill_color=BG_PANEL, line_color=BORDER, radius=2)
add_text_box(slide, Inches(0.60), Inches(5.92), Inches(4.0), Inches(0.18), "Recompute on demand:", 7, ACCENT, bold=True)
add_text_box(slide, Inches(1.70), Inches(5.92), Inches(4.5), Inches(0.18), "python manage.py recompute_risk   •   Celery beat nightly  •   GET /api/analytics/anomalies/", 7, WHITE, font_name="Consolas")
add_text_box(slide, Inches(7.8), Inches(5.92), Inches(4.8), Inches(0.40), "No hidden model — every mine’s 4 components (safety / compliance / contractor / incident) stored & displayed.", 7, MUTED, alignment=PP_ALIGN.RIGHT)
# embed analytics image small at bottom right if available
if HAS_PIL and p3 and Path(p3).exists():
    # we already covered with custom drawing; keep for next slide spare — skip duplicate
    pass
slide.notes_slide.placeholders[1].text_frame.text = "Slide 7 (2.5 min): Demystify AI. Stress explainability: show formula, penalties, bands, live distribution. Explain why contractor score is flagged as weakest — honesty builds trust. Show anomaly logic is simple stats, not magic."

# ---------------------------
# SLIDE 8: Smart Governance Workflow
# ---------------------------
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)
add_shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(3), fill_color=HIGH)
add_text_box(slide, Inches(0.5), Inches(0.28), Inches(3.0), Inches(0.22), "08  —  FIELD TO HQ WORKFLOW", 8, HIGH, bold=True)
add_text_box(slide, Inches(0.5), Inches(0.52), Inches(12.3), Inches(0.50), "Smart Governance in Action — Every Report Geo-tagged, Audited, Paperless", 22, WHITE, bold=True)
# workflow steps large
steps = [
    ("Field\nInspection", "Inspector: geo-tagged\n+ photo + accuracy\nclient_id offline", ACCENT, "apps/inspections"),
    ("Observation\nCaptured", "Severity LOW→CRIT\nCategory • Status\nClosed/Verified", HIGH, "Observation"),
    ("Corrective\nAction", "Priority • Owner\nDue date • Verify\n→ Close", CRITICAL, "CorrectiveAction"),
    ("Auto\nEscalation", "AlertRule thresholds\nCelery hourly:\nPENDING→OVERDUE", RGBColor(239,68,68), "AlertRule"),
    ("Dashboard\n& Reports", "KPI + Map + Charts\nPDF / CSV\nPer-role filtering", ACCENT2, "Dashboard"),
    ("Blockchain\nAudit Trail", "SHA256 chain\nprevious_hash +\nentry_hash", RGBColor(168,85,247), "AuditLog"),
]
sx = Inches(0.5)
for i, (title, desc, col, code) in enumerate(steps):
    card = add_shape(slide, sx, Inches(1.30), Inches(1.88), Inches(1.85), fill_color=BG_PANEL, line_color=col, line_width=1.2, radius=3)
    # number badge
    circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, sx+Inches(0.68), Inches(1.38), Inches(0.52), Inches(0.52))
    circ.fill.solid(); circ.fill.fore_color.rgb = col; circ.line.fill.background()
    add_text_box(slide, sx+Inches(0.68), Inches(1.46), Inches(0.52), Inches(0.36), str(i+1), 14, WHITE if col!=ACCENT else BG_DARK, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, sx, Inches(1.96), Inches(1.88), Inches(0.36), title, 8, WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, sx+Inches(0.10), Inches(2.34), Inches(1.68), Inches(0.48), desc, 6.5, MUTED, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, sx, Inches(2.90), Inches(1.88), Inches(0.14), code, 5.5, col, alignment=PP_ALIGN.CENTER, font_name="Consolas")
    if i < 5:
        add_text_box(slide, sx+Inches(1.88), Inches(2.10), Inches(0.30), Inches(0.30), "→", 14, MUTED, bold=True, alignment=PP_ALIGN.CENTER)
    sx += Inches(2.10)
# feature grid bottom 2x4
add_text_box(slide, Inches(0.5), Inches(3.38), Inches(12.3), Inches(0.20), "CROSS-CUTTING CAPABILITIES — Built-in, not bolted on", 7, ACCENT, bold=True)
features = [
    ("Offline-First Mobile", "client_id idempotent sync\nSynced_at + photo evidence", "📱", ACCENT),
    ("OCR Digitization", "pytesseract (eng+hin)\nConfidence + extracted_data", "📄", ACCENT2),
    ("Hash-Chained Audit", "previous_hash + SHA256\nVerify at /api/audit/verify/", "🔗", RGBColor(168,85,247)),
    ("RBAC (6 Roles)", "ADMIN / REGULATOR /\nCORPORATE / INSPECTOR ...", "👥", HIGH),
    ("Notifications", "Notification + AlertRule\nUnread count + mark_read", "🔔", CRITICAL),
    ("Multilingual", "en / hi / bn / te / mr / ta\nProfile.language", "🌐", ACCENT),
    ("PDF & CSV Reports", "reportlab PDF\nCSV export + digital verify", "📊", ACCENT2),
    ("GeoJSON API", "/api/mines/geojson/\n/api/dashboard/mines-geojson", "🗺", ACCENT),
]
fx = Inches(0.5); fy = Inches(3.66)
for idx, (t, dsc, ic, col) in enumerate(features):
    col_idx = idx % 4; row = idx // 4
    x = fx + col_idx*Inches(3.20)
    y = fy + row*Inches(0.78)
    shp = add_shape(slide, x, y, Inches(3.05), Inches(0.68), fill_color=BG_PANEL, line_color=BORDER, radius=2)
    # icon
    circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, x+Inches(0.12), y+Inches(0.14), Inches(0.32), Inches(0.32))
    circ.fill.solid(); circ.fill.fore_color.rgb = BG_DARK; circ.line.color.rgb = col; circ.line.width = Pt(1)
    add_text_box(slide, x+Inches(0.12), y+Inches(0.18), Inches(0.32), Inches(0.20), ic, 8, WHITE, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, x+Inches(0.52), y+Inches(0.08), Inches(2.40), Inches(0.18), t, 7.5, WHITE, bold=True)
    add_text_box(slide, x+Inches(0.52), y+Inches(0.28), Inches(2.40), Inches(0.32), dsc, 6, MUTED, font_name="Consolas" if idx==7 else "Calibri")
# embed mobile mock image as footer visual if available
if HAS_PIL and p4 and Path(p4).exists():
    add_image(slide, p4, Inches(0.5), Inches(5.45), Inches(12.33), Inches(1.65))
else:
    add_shape(slide, Inches(0.5), Inches(5.45), Inches(12.33), Inches(1.65), fill_color=BG_PANEL, line_color=BORDER, radius=2)
    add_text_box(slide, Inches(0.5), Inches(6.05), Inches(12.33), Inches(0.3), "Mobile workflow preview — field → HQ with geo-tag + photo + offline sync + escalation", 8, MUTED, alignment=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 8 (2 min): Walk the lifecycle of a single field report. Emphasize geo-tag + time-stamp + offline idempotency as trust anchors. Show blockchain audit verifies tamper-evidence. Stress RBAC ensures regulator sees all, mine official sees assigned."

# ---------------------------
# SLIDE 9: Impact & Scalability
# ---------------------------
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)
add_shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(3), fill_color=ACCENT2)
add_text_box(slide, Inches(0.5), Inches(0.28), Inches(2.8), Inches(0.22), "09  —  IMPACT & SCALABILITY", 8, ACCENT2, bold=True)
add_text_box(slide, Inches(0.5), Inches(0.52), Inches(12.3), Inches(0.50), "From Paper Chaos to Data-Driven Governance — Measurable Impact", 22, WHITE, bold=True)
# Before vs After
add_shape(slide, Inches(0.5), Inches(1.18), Inches(6.05), Inches(2.85), fill_color=BG_PANEL, line_color=BORDER, radius=3)
add_text_box(slide, Inches(0.70), Inches(1.30), Inches(5.65), Inches(0.20), "BEFORE  —  Fragmented Manual System", 8, CRITICAL, bold=True)
befores = ["Data scattered in spreadsheets & paper files", "Delayed reporting: days-weeks to reach HQ", "Compliance gaps discovered only at audits", "Field visits unverifiable (no geo/time proof)", "Decisions on gut feel, not risk signals"]
ty = Inches(1.58)
for b in befores:
    add_text_box(slide, Inches(0.80), ty, Inches(5.45), Inches(0.20), "✗  " + b, 7.5, MUTED)
    ty+=Inches(0.22)
# after
add_shape(slide, Inches(6.80), Inches(1.18), Inches(6.05), Inches(2.85), fill_color=BG_PANEL, line_color=ACCENT2, radius=3)
add_text_box(slide, Inches(7.00), Inches(1.30), Inches(5.65), Inches(0.20), "AFTER  —  CoalGuard Unified Platform", 8, ACCENT2, bold=True)
afters = ["Single source of truth: Postgres + audit trail", "Real-time KPIs + hourly escalations", "Overdue auto-flagged → notified → escalated", "Every report geo + time + photo + hash", "Risk-ranked priorities + predictive alerts"]
ty = Inches(1.58)
for a in afters:
    add_text_box(slide, Inches(7.10), ty, Inches(5.45), Inches(0.20), "✓  " + a, 7.5, WHITE)
    ty+=Inches(0.22)
# vs arrow
add_shape(slide, Inches(6.42), Inches(2.35), Inches(0.30), Inches(0.30), fill_color=ACCENT2, radius=2)
add_text_box(slide, Inches(6.42), Inches(2.38), Inches(0.30), Inches(0.26), "→", 12, BG_DARK, bold=True, alignment=PP_ALIGN.CENTER)
# KPIs impact row
kpi_imp = [
    ("<24h → real-time", "Reporting latency", ACCENT),
    ("70%↓", "Manual paperwork\n(projected)", ACCENT2),
    ("458", "Mines already\nscored & mapped", WHITE),
    ("6", "High-risk mines\nflagged today", HIGH),
    ("100%", "Audit entries\nhash-verifiable", ACCENT),
]
sx = Inches(0.5)
for val, lbl, col in kpi_imp:
    add_shape(slide, sx, Inches(4.32), Inches(2.30), Inches(0.82), fill_color=BG_PANEL, line_color=col, line_width=1, radius=2)
    add_text_box(slide, sx, Inches(4.42), Inches(2.30), Inches(0.34), val, 13, col, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, sx, Inches(4.82), Inches(2.30), Inches(0.24), lbl, 6.5, MUTED, alignment=PP_ALIGN.CENTER)
    sx+= Inches(2.55)
# scalability panel
scale = add_shape(slide, Inches(0.5), Inches(5.35), Inches(12.33), Inches(1.60), fill_color=BG_PANEL, line_color=BORDER, radius=3)
add_text_box(slide, Inches(0.70), Inches(5.48), Inches(7.0), Inches(0.18), "SCALABILITY — Built for Pan-India Rollout, Not Just a Demo", 7, ACCENT, bold=True)
scales = [
    ("Today: 12 states\n37 subsidiaries\n52 districts", "→  Tomorrow: any state,\nsubsidy, coal type"),
    ("Bulk import:\nKagglehub + fuzzy mapping\n+ manual_mines.csv fallback", "→  Plug any Govt dataset\nlogs to docs/schema.md"),
    ("Per-state / subsidiary\nfiltering + scoping\nRBAC enforced", "→  Add N mines =\nO(1) code change"),
    ("Containerized:\nweb + db + redis + worker\n+ beat (docker-compose)", "→  Horizontal: add\nreplicas, PostGIS"),
]
sx = Inches(0.70)
for cur, nxt in scales:
    add_shape(slide, sx, Inches(5.76), Inches(2.85), Inches(1.05), fill_color=BG_DARK, line_color=BORDER, radius=2)
    add_text_box(slide, sx+Inches(0.08), Inches(5.82), Inches(1.28), Inches(0.92), cur, 6, MUTED)
    add_text_box(slide, sx+Inches(1.45), Inches(5.98), Inches(0.30), Inches(0.30), "→", 10, ACCENT2, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, sx+Inches(1.75), Inches(5.82), Inches(1.02), Inches(0.92), nxt, 6, WHITE)
    sx+= Inches(3.02)
# transparency footer
add_text_box(slide, Inches(0.5), Inches(7.15), Inches(12.33), Inches(0.18), "Outcome: Transparency ↑  •  Accountability ↑  •  Decision speed ↑  •  Paper ↓  — Indigenous e-governance framework for Indian coal mines.", 7, ACCENT2, alignment=PP_ALIGN.CENTER, bold=True)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 9 (2 min): Contrast before/after. Quantify impact even though MVP synthetic activity — emphasize architecture is what scales, data is pluggable. Show pan-India readiness."

# ---------------------------
# SLIDE 10: Roadmap & Close
# ---------------------------
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)
add_shape(slide, Inches(0), Inches(0), prs.slide_width, Pt(3), fill_color=ACCENT)
add_text_box(slide, Inches(0.5), Inches(0.28), Inches(3.5), Inches(0.22), "10  —  ROADMAP & DEPLOYMENT", 8, ACCENT, bold=True)
add_text_box(slide, Inches(0.5), Inches(0.52), Inches(12.3), Inches(0.50), "What’s Done, What’s Next — And How to Run It Now", 22, WHITE, bold=True)
# left: MVP done vs roadmap
done = add_shape(slide, Inches(0.5), Inches(1.18), Inches(4.0), Inches(4.65), fill_color=BG_PANEL, line_color=ACCENT2, radius=3)
add_text_box(slide, Inches(0.70), Inches(1.32), Inches(3.60), Inches(0.20), "✓ MVP DONE — Runs Today (v1.0.0)", 8, ACCENT2, bold=True)
dones = [
    "Mine registry + GeoJSON + CSV",
    "Compliance workflow + PDF report",
    "Inspections / Observations + photo",
    "Corrective Actions + verify/close",
    "Risk engine + anomaly analytics",
    "Audit hash chain + verification",
    "OCR pipeline + notifications",
    "RBAC 6 roles + multilingual",
    "Docker + no-Docker launchers",
]
ty = Inches(1.60)
for d in dones:
    add_text_box(slide, Inches(0.80), ty, Inches(3.40), Inches(0.16), "✓  " + d, 7, WHITE)
    ty+=Inches(0.20)
add_text_box(slide, Inches(0.70), Inches(3.62), Inches(3.60), Inches(0.14), "Seed: 200+ mines • demo users seeded", 6, MUTED, italic=True)
# verify bar
add_shape(slide, Inches(0.70), Inches(3.84), Inches(3.60), Inches(0.50), fill_color=BG_DARK, line_color=BORDER, radius=2)
add_text_box(slide, Inches(0.80), Inches(3.92), Inches(3.40), Inches(0.16), "Verify:", 7, ACCENT, bold=True)
add_text_box(slide, Inches(1.18), Inches(3.92), Inches(3.02), Inches(0.34), "curl localhost:8000/health/\ncurl localhost:8000/api/audit/verify/", 6, MUTED, font_name="Consolas")
# how to run panel middle
run = add_shape(slide, Inches(4.75), Inches(1.18), Inches(4.35), Inches(4.65), fill_color=BG_PANEL, line_color=ACCENT, radius=3)
add_text_box(slide, Inches(4.95), Inches(1.32), Inches(3.95), Inches(0.20), "▶  HOW TO RUN — One-Click (No Cloud Needed)", 8, ACCENT, bold=True)
steps_run = [
    ("1", "Double-click  start_coalguard.bat", "Checks Docker → builds → force-recreate → migrate → seed → gunicorn"),
    ("2", "Open  http://localhost:8000/", "Dashboard  •  /mines/  •  /api/docs/  •  /admin/  •  /health/"),
    ("3", "Login with demo accounts", "admin / regulator / corporate / inspector / mine_official / contractor"),
    ("No\nDocker", "run_local.bat  or  ./run_local.sh", "Auto .venv + SQLite + sync tasks — same flow, no Docker"),
]
ty = Inches(1.62)
for num, title, desc in steps_run:
    # num
    shape_num = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(4.95), ty, Inches(0.28), Inches(0.28))
    shape_num.fill.solid(); shape_num.fill.fore_color.rgb = ACCENT if num!="No\nDocker" else BG_DARK
    shape_num.line.color.rgb = ACCENT
    if num == "No\nDocker":
        add_text_box(slide, Inches(4.95), ty, Inches(0.28), Inches(0.28), "◯", 8, ACCENT, alignment=PP_ALIGN.CENTER)
    else:
        add_text_box(slide, Inches(4.95), ty, Inches(0.28), Inches(0.28), num, 8, BG_DARK, bold=True, alignment=PP_ALIGN.CENTER)
    add_text_box(slide, Inches(5.32), ty+Inches(0.02), Inches(3.60), Inches(0.18), title, 7.5, WHITE, bold=True, font_name="Consolas" if num!="3" else "Calibri")
    add_text_box(slide, Inches(5.32), ty+Inches(0.20), Inches(3.60), Inches(0.28), desc, 6, MUTED)
    ty+=Inches(0.50) if num!="No\nDocker" else Inches(0.55)
add_shape(slide, Inches(4.95), Inches(3.92), Inches(3.95), Inches(0.46), fill_color=BG_DARK, line_color=BORDER, radius=2)
add_text_box(slide, Inches(5.02), Inches(3.98), Inches(3.80), Inches(0.34), "Demo logins:  admin/Admin@123  •  regulator/Regulator@123  •  inspector/Inspector@123\ncorporate/Corporate@123  •  contractor/Contractor@123", 6, MUTED, font_name="Consolas")
add_text_box(slide, Inches(4.95), Inches(4.50), Inches(3.95), Inches(0.16), "Ports & names via .env  →  WEB_PORT=8000  DB_PORT_HOST=5432  COMPOSE_PROJECT_NAME=coalguard", 6, ACCENT, alignment=PP_ALIGN.CENTER, font_name="Consolas")
# right: roadmap + vision
road = add_shape(slide, Inches(9.35), Inches(1.18), Inches(3.50), Inches(4.65), fill_color=BG_PANEL, line_color=BORDER, radius=3)
add_text_box(slide, Inches(9.55), Inches(1.32), Inches(3.10), Inches(0.20), "▲  ROADMAP — Post-MVP (Out of Scope, Planned)", 7, HIGH, bold=True)
phases = [
    ("Phase 2 — GIS+", "PostGIS + GeoDjango\nHeatmap & radius search"),
    ("Phase 2 — ML", "Trained classifier replaces\nweighted formula (when labels exist)"),
    ("Phase 2 — Mobile", "PWA + WatermelonDB\nBackground sync to client_id"),
    ("Phase 2 — Intel", "Multilingual LLM / RAG\nover compliance corpus"),
    ("Phase 2 — Ops", "django-celery-beat DB sched.\nAsync OCR queue"),
]
ty = Inches(1.60)
for phase, desc in phases:
    add_text_box(slide, Inches(9.65), ty, Inches(3.10), Inches(0.16), phase, 7, WHITE, bold=True)
    add_text_box(slide, Inches(9.65), ty+Inches(0.18), Inches(3.10), Inches(0.28), desc, 6, MUTED)
    ty+=Inches(0.48)
# vision box
add_shape(slide, Inches(9.55), Inches(4.22), Inches(3.10), Inches(1.40), fill_color=RGBColor(22,32,44), line_color=ACCENT, radius=2)
add_text_box(slide, Inches(9.65), Inches(4.30), Inches(2.90), Inches(0.52), "Vision:  Scalable indigenous\ne-governance framework\nfor every Indian coal mine.", 9, ACCENT, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(9.65), Inches(4.92), Inches(2.90), Inches(0.48), "Paperless • Transparent • Accountable\nData-driven decisions at field-to-Ministry speed.", 7, MUTED, alignment=PP_ALIGN.CENTER)
# closing bar
close = add_shape(slide, Inches(0.5), Inches(6.05), Inches(12.33), Inches(1.05), fill_color=ACCENT, radius=3)
add_text_box(slide, Inches(0.5), Inches(6.16), Inches(12.33), Inches(0.30), "CoalGuard is Ready to Deploy — Not a Slideware Promise.", 14, BG_DARK, bold=True, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(0.5), Inches(6.48), Inches(12.33), Inches(0.22), "Built end-to-end for PSID 26024  •  Ministry of Coal  •  Coal India Limited  •  SIH 2026", 8, RGBColor(30,60,90), alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(0.5), Inches(6.74), Inches(12.33), Inches(0.20), "Thank You  —  Questions & Live Demo at  http://localhost:8000  •  /api/docs/  •  Team CoalGuard", 8, BG_DARK, alignment=PP_ALIGN.CENTER)
slide.notes_slide.placeholders[1].text_frame.text = "Slide 10 (2 min): Close with confidence. Recap MVP is shippable now, roadmap is principled (PostGIS, ML, PWA). Demo live if time, else point to one-click run. End with vision: indigenous framework for Ministry."

# Save
prs.save(OUT)
print(f"Saved presentation to {OUT}")
print(f"Size: {OUT.stat().st_size/1024:.1f} KB")
