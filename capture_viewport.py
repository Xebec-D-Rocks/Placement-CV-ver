from pathlib import Path
base = "http://127.0.0.1:8001"
out_dir = Path("docs/presentation_assets/real")
out_dir.mkdir(parents=True, exist_ok=True)
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=2)  # 2x for crisp
    page = context.new_page()

    def shot(url, filename, wait=3500):
        print(f"-> {url} -> {filename}")
        page.goto(url, wait_until="networkidle", timeout=15000)
        page.wait_for_timeout(wait)
        page.evaluate("window.scrollTo(0,0)")
        page.wait_for_timeout(500)
        path = out_dir / filename
        page.screenshot(path=str(path), full_page=False)
        print(f"   saved {path.stat().st_size} bytes")
        return path

    # Dashboard top viewport (KPIs + map + first charts)
    shot(f"{base}/", "dashboard_viewport.png", wait=4500)
    # Scroll a bit to capture middle charts
    page.evaluate("window.scrollTo(0, 900)")
    page.wait_for_timeout(800)
    page.screenshot(path=str(out_dir / "dashboard_viewport_mid.png"))
    print("mid saved")
    page.evaluate("window.scrollTo(0, 1800)")
    page.wait_for_timeout(800)
    page.screenshot(path=str(out_dir / "dashboard_viewport_bottom.png"))
    print("bottom saved")

    # Mines viewport
    shot(f"{base}/mines/", "mines_viewport.png", wait=2500)
    # Mine detail viewport
    shot(f"{base}/mines/1/", "mine_detail_viewport.png", wait=2500)
    # API docs viewport (Swagger)
    shot(f"{base}/api/docs/", "api_docs_viewport.png", wait=3500)
    # Admin
    shot(f"{base}/admin/", "admin_viewport.png", wait=2500)
    # Login as admin then capture authed dashboard viewport again crisp
    page.goto(f"{base}/admin/login/?next=/", wait_until="networkidle")
    page.fill('input[name="username"]', "admin")
    page.fill('input[name="password"]', "Admin@123")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1500)
    shot(f"{base}/", "dashboard_authed_viewport.png", wait=4500)
    shot(f"{base}/mines/", "mines_authed_viewport.png", wait=2500)
    browser.close()

print("viewport captures done")
from PIL import Image
for f in sorted(out_dir.glob("*viewport*.png")):
    im = Image.open(f)
    print(f.name, im.size, f.stat().st_size)
