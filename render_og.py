#!/usr/bin/env python3
"""Render assets/img/og-cover.svg -> og-cover.png (1200x630) for social previews. Needs playwright + chromium."""
import asyncio, os, sys
from playwright.async_api import async_playwright

img_dir = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "assets/img")

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        await pg.goto("file://" + os.path.join(img_dir, "og-cover.svg"))
        await pg.screenshot(path=os.path.join(img_dir, "og-cover.png"))
        await b.close()

asyncio.run(main())
