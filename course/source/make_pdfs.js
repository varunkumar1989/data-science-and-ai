// Prints every page listed in pdf_jobs.json to PDF with clickable links, bookmarks (outline) and page numbers.
// Usage: node make_pdfs.js [filter]
const path = require("path"), fs = require("fs");
let pw; try { pw = require("playwright"); } catch (e) { pw = require("/opt/node-tools/node_modules/playwright"); }
const ROOT = path.resolve(__dirname, "..");
const jobs = JSON.parse(fs.readFileSync(path.join(__dirname, "pdf_jobs.json"), "utf8"));
const filt = process.argv[2] || "";
const FOOT = t => `<div style="font:7.5px Inter,Arial,sans-serif;color:#7A759A;width:100%;padding:0 13mm;display:flex;justify-content:space-between"><span>${t.replace(/&/g, "&amp;").replace(/</g, "&lt;")}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`;
(async () => {
  const b = await pw.chromium.launch();
  const ctx = await b.newContext();
  for (const [src, dst, t] of jobs) {
    if (filt && !src.includes(filt) && !dst.includes(filt)) continue;
    const out = path.join(ROOT, dst); fs.mkdirSync(path.dirname(out), { recursive: true });
    const pg = await ctx.newPage();
    await pg.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
    await pg.goto("file://" + path.join(ROOT, src), { waitUntil: "load" });
    await pg.evaluate(() => { document.querySelectorAll("details").forEach(d => d.open = true); document.querySelectorAll('img[loading="lazy"]').forEach(i => i.loading = "eager"); });
    await pg.waitForFunction(() => [...document.images].every(i => i.complete), null, { timeout: 60000 }).catch(() => {});
    await pg.pdf({ path: out, format: "A4", printBackground: true, displayHeaderFooter: true, outline: true, tagged: true,
      headerTemplate: "<span></span>", footerTemplate: FOOT(t), margin: { top: "13mm", bottom: "15mm", left: "13mm", right: "13mm" } });
    await pg.close(); console.log("pdf", dst);
  }
  await b.close();
})();
