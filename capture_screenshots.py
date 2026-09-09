import os, time
from pathlib import Path

out_dir = Path("docs/presentation_assets/real")
out_dir.mkdir(parents=True, exist_ok=True)
base = "http://127.0.0.1:8001"

from playwright.sync_api import sync_playwright

# Use 1920x1080 viewport, scaled
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    page = context.new_page()

    # Common: wait for network idle and charts
    def shot(url, filename, wait=3000, full=False):
        print(f" -> {url} -> {filename}")
        page.goto(url, wait_until="networkidle", timeout=15000)
        # wait for JS charts/map to render
        page.wait_for_timeout(wait)
        # scroll to top
        page.evaluate("window.scrollTo(0,0)")
        page.wait_for_timeout(500)
        path = out_dir / filename
        page.screenshot(path=str(path), full_page=full)
        print(f"   saved {path} ({path.stat().st_size} bytes)")
        return path

    # 1 Dashboard (full page to capture KPIs + map + charts)
    shot(f"{base}/", "01_dashboard.png", wait=4000, full=True)
    # 2 Mine registry full
    shot(f"{base}/mines/", "02_mines_list.png", wait=2500, full=True)
    # 3 Mine detail - pick first mine id
    # get first mine id via API
    import json, urllib.request
    try:
        with urllib.request.urlopen(f"{base}/api/mines/?page_size=1") as r:
            data = json.loads(r.read())
            # DRF pagination
            first_id = data["results"][0]["id"] if "results" in data else data[0]["id"] if data else 1
    except Exception as e:
        print("api mines failed", e)
        first_id = 1
    print(f"first mine id {first_id}")
    shot(f"{base}/mines/{first_id}/", "03_mine_detail.png", wait=2500, full=True)
    # 4 API docs swagger
    shot(f"{base}/api/docs/", "04_api_docs.png", wait=3500, full=False)
    # 5 Admin login
    shot(f"{base}/admin/login/?next=/admin/", "05_admin_login.png", wait=2000, full=False)
    # 6 Health + audit verify (json views)
    shot(f"{base}/health/", "06_health.png", wait=1500, full=False)
    # 7 Try dashboard with authenticated view: login as admin
    # do login via request to get nice view? Use page to login
    page.goto(f"{base}/admin/login/?next=/", wait_until="networkidle")
    page.fill('input[name="username"]', "admin")
    page.fill('input[name="password"]', "Admin@123")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1500)
    # now dashboard as admin should show user in header
    shot(f"{base}/", "07_dashboard_authed.png", wait=3500, full=True)
    shot(f"{base}/mines/", "08_mines_authed.png", wait=2500, full=True)
    # 9 API audit verify json
    page.goto(f"{base}/api/audit/verify/", wait_until="networkidle")
    page.wait_for_timeout(1500)
    page.screenshot(path=str(out_dir / "09_audit_verify.png"))

    browser.close()

print("Done. Files in", out_dir)
for f in sorted(out_dir.glob("*.png")):
    print(f.name, f.stat().st_size)
