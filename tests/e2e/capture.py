"""Capture a running fixture and assert CTA/state behavior; does not judge aesthetics."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--url", default="http://127.0.0.1:8765")
parser.add_argument("--out", required=True, type=Path)
args = parser.parse_args()
args.out.mkdir(parents=True, exist_ok=False)
results = []
with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    for name, width, height in (("desktop", 1280, 800), ("mobile", 390, 844)):
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        response = page.goto(args.url, wait_until="networkidle")
        assert response and response.ok, "page must load successfully"
        page.evaluate("document.fonts.ready")
        assert page.locator("#start").is_visible(), "primary action must be visible"
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "horizontal overflow"
        page.screenshot(path=str(args.out / f"{name}-initial.png"), full_page=True)
        page.locator("#start").click()
        assert page.locator("#status").inner_text() == "专注已开始", "started status must appear"
        assert page.locator("#start").is_disabled(), "duplicate start must be prevented"
        page.screenshot(path=str(args.out / f"{name}-started.png"), full_page=True)
        assert not errors, errors
        results.append({"viewport": [width, height], "cta_and_state": "pass",
                        "overflow": "pass", "page_errors": errors})
        page.close()
    browser.close()
(args.out / "functional-results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2))
print("PASS capture and functional checks; visual review is NOT VERIFIED.")
