#!/usr/bin/env python3
"""Render a single XHS vertical HTML page into a high-res PNG.

Usage:
    python3 render.py <input.html> <output.png> [width] [height] [scale]

Defaults: 1080x1440 CSS px (3:4), device scale factor 2 -> 2160x2880 PNG.
The HTML page MUST be exactly width x height and fill the viewport.

Chromium discovery order:
    1. $CHROMIUM_PATH environment variable (e.g. export CHROMIUM_PATH=/usr/bin/chromium)
    2. Common browser binaries found on PATH (chromium, chrome, google-chrome, ...)
    3. Well-known install paths for Linux / macOS / Windows
    4. Playwright's own bundled Chromium (fallback; run `playwright install chromium` if missing)
"""
import os
import sys
import asyncio
import pathlib
import shutil
import platform

from playwright.async_api import async_playwright


def find_chromium() -> str | None:
    """Return a usable Chromium executable path, or None to use Playwright bundled one."""
    candidates: list[str] = []

    env = os.environ.get("CHROMIUM_PATH")
    if env:
        candidates.append(env)

    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome", "msedge"):
        found = shutil.which(name)
        if found:
            candidates.append(found)

    system = platform.system()
    if system == "Linux":
        candidates += [
            "/usr/local/bin/chromium",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
            "/snap/bin/chromium",
        ]
    elif system == "Darwin":
        candidates += [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        ]
    elif system == "Windows":
        candidates += [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ]

    for c in candidates:
        if c and os.path.isfile(c):
            return c
    return None


async def render(html_path: str, out_png: str, width: int = 1080, height: int = 1440, scale: int = 2):
    url = pathlib.Path(html_path).resolve().as_uri()
    executable = find_chromium()
    launch_kwargs = {"args": ["--no-sandbox", "--force-color-profile=srgb"]}
    if executable:
        launch_kwargs["executable_path"] = executable
    async with async_playwright() as p:
        browser = await p.chromium.launch(**launch_kwargs)
        page = await browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=scale)
        await page.goto(url, wait_until="networkidle")
        try:
            await page.evaluate("document.fonts.ready")
        except Exception:
            pass
        await page.wait_for_timeout(400)
        await page.screenshot(path=out_png, omit_background=False, full_page=False)
        await browser.close()
    print(f"OK -> {out_png} ({width*scale}x{height*scale})")


if __name__ == "__main__":
    html = sys.argv[1]
    out = sys.argv[2]
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 1080
    h = int(sys.argv[4]) if len(sys.argv) > 4 else 1440
    s = int(sys.argv[5]) if len(sys.argv) > 5 else 2
    asyncio.run(render(html, out, w, h, s))
