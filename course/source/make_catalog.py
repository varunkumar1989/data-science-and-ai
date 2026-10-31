"""Write course/catalog.json: tracks, lessons, page and PDF links, used by skillnavora.in to list the handbook."""
import json, os, re, sys, html, glob, yaml
sys.path.insert(0, os.path.dirname(__file__))
from build import TRACKS
ROOT = os.path.join(os.path.dirname(__file__), "..")
jobs = json.load(open(os.path.join(os.path.dirname(__file__), "pdf_jobs.json")))
pdf_for = {src: dst for src, dst, _ in jobs}
lessons = sorted(os.listdir(os.path.join(ROOT, "lessons")))
cat = {"title": "SkillNavora Data Science & AI Handbook", "complete_pdf": "pdf/SkillNavora_Data_Science_AI_Complete_Handbook.pdf", "tracks": []}
for t in TRACKS:
    ls = []
    for f in lessons:
        if not f.startswith(t["id"] + "-") or not re.match(rf"{re.escape(t['id'])}-\d\d-", f): continue
        page = "lessons/" + f; doc = open(os.path.join(ROOT, page), encoding="utf-8").read()
        title = re.sub(r"\s*·.*$", "", re.search(r"<title>(.*?)</title>", doc).group(1)).strip()
        n = int(f.split("-")[len(t["id"].split("-"))]); pdf = pdf_for.get(page) or ""
        src = glob.glob(os.path.join(os.path.dirname(__file__), "lessons", t["id"], f"{n:02d}-*.md"))
        m = re.search(r"^live:\s*\"?(.*?)\"?\s*$", open(src[0], encoding="utf-8").read(), re.M) if src else None; live = m.group(1) if m else ""
        ls.append({"n": n, "num": n, "title": html.unescape(title), "page": page, "file": f, "track": t["id"], "pdf": os.path.basename(pdf), "pdf_path": pdf, "live": live})
    if not ls: continue
    track_pdf = next((d for s, d in pdf_for.items() if s == f"print/track-{t['id']}.html"), None)
    cat["tracks"].append({"id": t["id"], "name": t["name"], "color": t["color"], "desc": t["desc"], "lessons": ls, "pdf": track_pdf, "track_pdf": os.path.basename(track_pdf or ""), "extra": bool(t.get("extra"))})
cat["lesson_count"] = sum(len(t["lessons"]) for t in cat["tracks"])
json.dump(cat, open(os.path.join(ROOT, "catalog.json"), "w"), indent=1, ensure_ascii=False)
print(cat["lesson_count"], "lessons in", len(cat["tracks"]), "tracks")
