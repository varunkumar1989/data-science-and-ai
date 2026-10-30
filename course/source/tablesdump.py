import re, sys, glob, html
f = glob.glob(f"../lessons/{sys.argv[1]}*.html")[0]; h = open(f).read()
for i, t in enumerate(re.findall(r'<div class="xl">(.*?)</table>', h, re.S)):
    if len(sys.argv) > 2 and str(i) not in sys.argv[2].split(","): continue
    title = re.search(r'</span>(.*?)</div>', t); print(f"--- [{i}]", html.unescape(title.group(1)) if title else "")
    for row in re.findall(r"<tr>(.*?)</tr>", t, re.S)[1:]:
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)]
        print(" | ".join(cells))
