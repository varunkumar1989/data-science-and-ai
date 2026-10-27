import re, sys, glob, html
h = open(glob.glob(f"../lessons/{sys.argv[1]}*.html")[0]).read()
n = int(sys.argv[2]) if len(sys.argv) > 2 else 260
for i, part in enumerate(h.split('<div class="output">')[1:]):
    end = min([x for x in (part.find('<div class="code">'), part.find("<h2"), part.find("<h3"), part.find("<p>"), part.find('<div class="co '), part.find("<figure")) if x > 0] or [len(part)])
    t = html.unescape(re.sub(r"<[^>]+>", " ", part[:end])); print(f"[{i}]", re.sub(r"\s+", " ", t)[:n])
