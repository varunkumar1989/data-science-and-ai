"""Write course/catalog.json: tracks, lessons, page and PDF links, used by skillnavora.in to list the handbook."""
import json, os, re, sys, yaml
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
        page = "lessons/" + f; html = open(os.path.join(ROOT, page), encoding="utf-8").read()
        title = re.sub(r"\s*·.*$", "", re.search(r"<title>(.*?)</title>", html).group(1)).strip()
        ls.append({"n": int(f.split("-")[len(t["id"].split("-"))]), "title": title, "page": page, "pdf": pdf_for.get(page)})
    if not ls: continue
    track_pdf = next((d for s, d in pdf_for.items() if s == f"print/track-{t['id']}.html"), None)
    cat["tracks"].append({"id": t["id"], "name": t["name"], "color": t["color"], "desc": t["desc"], "lessons": ls, "pdf": track_pdf})
cat["lesson_count"] = sum(len(t["lessons"]) for t in cat["tracks"])
json.dump(cat, open(os.path.join(ROOT, "catalog.json"), "w"), indent=1, ensure_ascii=False)
print(cat["lesson_count"], "lessons in", len(cat["tracks"]), "tracks")
