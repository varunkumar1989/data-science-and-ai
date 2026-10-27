import asyncio, os
from playwright.async_api import async_playwright
HB = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.join(HB, "site"); OUT = os.path.join(SITE, "pdf"); os.makedirs(OUT, exist_ok=True)
import json
JOBS = json.load(open(os.path.join(HB, "pdf_jobs.json")))
FOOT = '<div style="font:8px Inter,Arial,sans-serif;color:#7A839A;width:100%;padding:0 13mm;display:flex;justify-content:space-between"><span>{t}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for src, dst, t in JOBS:
            pg = await b.new_page()
            await pg.goto("file://" + os.path.join(SITE, src), wait_until="load")
            await pg.wait_for_timeout(500)
            await pg.pdf(path=os.path.join(OUT, dst), format="A4", print_background=True, display_header_footer=True,
                         header_template="<span></span>", footer_template=FOOT.format(t=t), margin={"top": "14mm", "bottom": "15mm", "left": "13mm", "right": "13mm"})
            await pg.close(); print("wrote", dst)
        await b.close()
asyncio.run(main())
