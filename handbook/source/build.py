"""Builds the handbook site (site/index.html) and the four print HTML files used for the PDFs."""
import os, re, json, html, glob, sys, urllib.parse

HB = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HB, "site")
ONLINE = os.environ.get("HB_URL", "").strip()          # public URL of the interactive version (set after first publish)
TITLE = "Data Science & AI Handbook"
PROGRAMME = "AnalytixLabs · Advanced Certification in Data Science & AI (IIT), June 2026 batch"

# ------------------------------------------------------------------ code highlighting
KW = {
 "python": r"def|return|if|elif|else|for|while|in|not|and|or|import|from|as|with|class|try|except|finally|lambda|True|False|None|break|continue|pass|is|yield|raise|global",
 "sql": r"SELECT|FROM|WHERE|GROUP|BY|ORDER|HAVING|JOIN|LEFT|RIGHT|FULL|INNER|OUTER|CROSS|ON|AS|AND|OR|NOT|IN|IS|NULL|LIKE|BETWEEN|CASE|WHEN|THEN|ELSE|END|DISTINCT|TOP|UNION|ALL|INTERSECT|EXCEPT|WITH|OVER|PARTITION|ROWS|PRECEDING|FOLLOWING|CURRENT|ROW|UNBOUNDED|CREATE|TABLE|VIEW|PROCEDURE|ALTER|DROP|TRUNCATE|INSERT|INTO|VALUES|UPDATE|SET|DELETE|PRIMARY|KEY|FOREIGN|REFERENCES|DEFAULT|CHECK|IDENTITY|DECLARE|BEGIN|EXEC|USE|DATABASE|ADD|COLUMN|OFFSET|FETCH|NEXT|ONLY|EXISTS|ASC|DESC|LIMIT|UNPIVOT|FOR|INT|VARCHAR|DATE|DECIMAL|MONEY|BIGINT|WINDOW|USING|ROLLUP|CUBE",
 "dax": r"VAR|RETURN|TRUE|FALSE",
 "tableau": r"IF|THEN|ELSEIF|ELSE|END|CASE|WHEN|FIXED|INCLUDE|EXCLUDE|AND|OR|NOT",
 "m": r"let|in|each|type|true|false|null",
 "bash": r"git|conda|pip|heroku|az|python|docker|cd",
}
def highlight(code, lang):
    code = html.unescape(code)
    lang = (lang or "").lower()
    if lang in ("text", "html", "excel", "") :
        if lang == "excel":
            pat = re.compile(r'(?P<s>"[^"\n]*")|(?P<f>\b[A-Z][A-Z0-9.]+(?=\())|(?P<n>\b\d+(?:\.\d+)?\b)')
        else:
            return html.escape(code)
    else:
        com = {"python": r"#[^\n]*", "sql": r"--[^\n]*|/\*[\s\S]*?\*/", "dax": r"--[^\n]*|//[^\n]*", "tableau": r"//[^\n]*",
               "m": r"//[^\n]*", "bash": r"#[^\n]*"}.get(lang, r"#[^\n]*")
        flags = re.I if lang == "sql" else 0
        pat = re.compile(rf"(?P<c>{com})|(?P<s>'''[\s\S]*?'''|\"[^\"\n]*\"|'[^'\n]*')|(?P<k>\b(?:{KW.get(lang, 'zzzz')})\b)|(?P<f>\b[A-Za-z_][A-Za-z0-9_.]*(?=\())|(?P<n>\b\d+(?:\.\d+)?\b)", flags)
    out, pos = [], 0
    for m in pat.finditer(code):
        out.append(html.escape(code[pos:m.start()]))
        cls = {"c": "hl-c", "s": "hl-s", "k": "hl-k", "f": "hl-f", "n": "hl-n"}[m.lastgroup]
        out.append(f'<span class="{cls}">{html.escape(m.group())}</span>')
        pos = m.end()
    out.append(html.escape(code[pos:]))
    return "".join(out)

def hl_blocks(s):
    def rep(m):
        lang = m.group(1) or ""
        return f'<pre><code class="{lang}">{highlight(m.group(2), lang)}</code></pre>'
    return re.sub(r'<pre><code(?: class="([a-z]+)")?>([\s\S]*?)</code></pre>', rep, s)

def links(s):
    s = re.sub(r"\[\[yt:([^\]]+)\]\]", lambda m: f'<a class="yt" target="_blank" rel="noopener" href="https://www.youtube.com/results?search_query={urllib.parse.quote_plus(m.group(1))}">YouTube: {html.escape(m.group(1))}</a>', s)
    s = re.sub(r"\[\[doc:([^|\]]+)\|([^\]]+)\]\]", lambda m: f'<a class="doc" target="_blank" rel="noopener" href="{m.group(2)}">{html.escape(m.group(1))}</a>', s)
    return s

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("&", "and")).strip("-")

def wrap_tables(s):
    return s

# ------------------------------------------------------------------ modules + sessions
def load(path):
    raw = open(path).read()
    meta = json.loads(re.search(r"<!--meta (.*?) -->", raw).group(1))
    meta["tabs"] = [(m.group(1), hl_blocks(links(m.group(2))))
                    for m in re.finditer(r'<div data-tab="([^"]+)">([\s\S]*?)\n</div>\s*(?=<div data-tab=|\Z)', raw)]
    return meta
MOD_ORDER = ["m1_building_blocks", "m1b_bb_ml", "m2_python", "m3_dva", "m4_ml", "m5_mlops", "m6_genai", "m7_powerbi", "m8_tableau"]
MODULES = [load(os.path.join(HB, "content", n + ".html")) for n in MOD_ORDER]
for i, m in enumerate(MODULES, 1):
    m["num"] = f"{i:02d}"; m["kind"] = "COURSE HANDBOOK"
SESSIONS = [load(f) for f in sorted(glob.glob(os.path.join(HB, "sessions", "s*.html")))]
for m in SESSIONS: m["kind"] = "LEARNING SESSION"
ALL = MODULES + SESSIONS
print("modules:", [(m["id"], len(m["tabs"])) for m in MODULES]); print("sessions:", [(m["id"], len(m["tabs"])) for m in SESSIONS])

# ------------------------------------------------------------------ cases
ORDER = [("Python for Data Science", ["py_basic", "py_pandas90", "py_retail", "py_credit", "py_insurance", "py_viz", "py_hypothesis", "py_ecom"]),
         ("Excel (Data Visualization & Analytics)", ["xl_sports", "xl_complaints"]),
         ("SQL (Data Visualization & Analytics)", ["sql_retail", "sql_mobile"]),
         ("Tableau", ["tb_laptops", "tb_sports"])]
NOTES = {
 ("tb_laptops", "2"): "Average price falls from about 499 in January to about 379 in December, with ups and downs between months. Plan pricing month by month rather than with one annual price.",
 ("py_hypothesis", "4"): "The averages run against the claim: medium-priority jobs (2.50 days) finish faster on average than high-priority jobs (3.02 days), and the ANOVA finds no significant difference. The prioritisation system is not working as intended. Completion times are right-skewed (means far above medians), so also confirm with a Kruskal–Wallis test.",
 ("py_credit", "4c"): None,
}
CASES = {}
for f in glob.glob(os.path.join(HB, "solved", "*.json")):
    d = json.load(open(f)); CASES[d["cid"]] = d
for (cid, num), note in NOTES.items():
    for it in CASES[cid]["items"]:
        if it["num"] == num:
            it["note"] = note
TOOLBADGE = {"py": "Python", "xl": "Excel", "sql": "SQL", "tb": "Tableau"}

def case_q_list(d):
    return '<ol class="qlist">' + "".join(f'<li><b>{html.escape(str(i["num"]))}</b>{html.escape(i["text"])}</li>' for i in d["items"] if not i["hidden"]) + "</ol>"

def case_answers(d):
    out = []
    for i in d["items"]:
        if i["hidden"]: continue
        lang = i.get("lang") or "python"
        label = {"python": "Python", "sql": "T-SQL (SQL Server)", "excel": "Excel steps / formulas", "tableau": "Tableau steps"}.get(lang, lang)
        h = [f'<div class="ans" id="ans-{d["cid"]}-{slug(str(i["num"]))}"><h4><span class="qn">{html.escape(str(i["num"]))}</span><span>{html.escape(i["text"])}</span></h4>']
        h.append(f'<div class="lang">{label}</div><pre><code class="{lang}">{highlight(html.escape(i["code"]), lang)}</code></pre>')
        res = []
        if i["stdout"]:
            txt = html.escape(i["stdout"])
            txt = re.sub(r"^(Answer[^\n]*)$", r'<span class="answer-line">\1</span>', txt, flags=re.M)
            res.append(f'<pre class="out">{txt}</pre>')
        if i["table"]:
            res.append(f'<div class="twrap">{i["table"]}</div>')
        for im in i["imgs"]:
            res.append(f'<figure><img loading="lazy" src="{im}" alt="Chart for question {html.escape(str(i["num"]))}"></figure>')
        if res:
            src = "Result on the real case data" if lang in ("python", "sql") else "Expected result (computed from the case data, use it to check your work)"
            h.append(f'<div class="lang">{src}</div>' + "".join(res))
        if i.get("note"):
            h.append(f'<div class="note">{i["note"]}</div>')
        if i["err"]:
            h.append(f'<div class="warn">{html.escape(i["err"])}</div>')
        h.append("</div>")
        out.append("".join(h))
    return "".join(out)

def case_header(d):
    return (f'<p class="lead">{html.escape(d["brief"])}</p>'
            f'<div class="grid2"><div class="card"><h4>Data</h4><p>{html.escape(d["data_desc"])}</p></div>'
            f'<div class="card"><h4>Tool and module</h4><p>{html.escape(d["tool"])}<br><span class="muted">{html.escape(d["module"])}</span></p></div></div>')

# ------------------------------------------------------------------ site
def nav():
    h = ['<div class="nav">', '<div class="nav-group">Start</div>', '<a href="#home" data-r="home"><span class="n">⌂</span>Home &amp; study plan</a>',
         '<div class="nav-group">Course handbooks</div>']
    for m in MODULES:
        h.append(f'<a href="#{m["id"]}" data-r="{m["id"]}"><span class="n">{m["num"]}</span>{html.escape(m["title"])}</a>')
    h.append('<div class="nav-group">Learning sessions (basic → advanced)</div>')
    for m in SESSIONS:
        t = re.sub(r"\s*\(.*?\)", "", m["title"])
        h.append(f'<a href="#{m["id"]}" data-r="{m["id"]}"><span class="n">{m["num"]}</span>{html.escape(t)}</a>')
    h.append('<div class="nav-group">Case studies</div><a href="#cases" data-r="cases"><span class="n">★</span>All case studies</a><div class="sub">')
    for g, ids in ORDER:
        for cid in ids:
            t = re.sub(r"^[^:]+:\s*", "", CASES[cid]["title"])
            h.append(f'<a href="#case/{cid}" data-r="case/{cid}">{html.escape(t[:46])}</a>')
    h.append('</div><div class="nav-group">Files</div><a href="#downloads" data-r="downloads"><span class="n">⬇</span>PDFs &amp; Excel workbook</a></div>')
    return "".join(h)

def module_page(m):
    tb = "".join(f'<button type="button" data-tab="{html.escape(t)}">{html.escape(t)}</button>' for t, _ in m["tabs"])
    body = "".join(f'<div class="tab" data-name="{html.escape(t)}">{c}</div>' for t, c in m["tabs"])
    return (f'<section class="page" id="p-{m["id"]}" data-page="{m["id"]}"><div class="crumb">{m["kind"]} {m["num"]}</div>'
            f'<div class="mhead"><div class="ic">{m["icon"]}</div><div><h1>{html.escape(m["title"])}</h1><p>{html.escape(m["sub"])}</p>'
            f'<p class="courses">{html.escape(m["courses"])}</p></div></div><div class="tabbar">{tb}</div>{body}<div class="tabnav"></div></section>')

def case_page(cid):
    d = CASES[cid]
    nq = len([i for i in d["items"] if not i["hidden"]])
    return (f'<section class="page" id="p-case-{cid}" data-page="case/{cid}"><div class="crumb">CASE STUDY · {html.escape(d["module"].upper())}</div>'
            f'<h1>{html.escape(d["title"])}</h1><div class="tabbar"><button type="button" data-tab="Case study">Case study ({nq} questions)</button>'
            f'<button type="button" data-tab="Resolution">Resolution &amp; answers</button></div>'
            f'<div class="tab" data-name="Case study">{case_header(d)}<h3>Questions</h3>{case_q_list(d)}'
            f'<p class="tip">Try each question yourself first, then open <a href="#case/{cid}/Resolution">Resolution &amp; answers</a> to compare.</p></div>'
            f'<div class="tab" data-name="Resolution">{case_header(d)}{case_answers(d)}</div><div class="tabnav"></div></section>')

def cases_index():
    h = ['<section class="page" id="p-cases" data-page="cases"><div class="crumb">CASE STUDIES</div><h1>Case studies and resolutions</h1>',
         '<p class="lead">Every case study from the LMS "Case Study &amp; Assignments" section that could be downloaded, solved on the real data. '
         'Each case has two tabs: the <b>Case study</b> (brief and questions) and the <b>Resolution</b> (code, outputs, charts and insights).</p>',
         '<div class="note-box">Not included: the two Power BI case studies (download failed twice) and items with no material (Generative AI and Power BI Services had only an image each). '
         'The ML, ML Ops and Building Blocks courses list no case studies on the LMS.</div>']
    for g, ids in ORDER:
        h.append(f"<h3>{html.escape(g)}</h3><div class='cgrid'>")
        for cid in ids:
            d = CASES[cid]; nq = len([i for i in d["items"] if not i["hidden"]])
            imgs = sum(len(i["imgs"]) for i in d["items"])
            h.append(f'<a class="ccard" href="#case/{cid}"><span class="badge">{TOOLBADGE[cid.split("_")[0]]}</span><b>{html.escape(d["title"])}</b>'
                     f'<small>{nq} questions{f" · {imgs} charts" if imgs else ""}</small></a>')
        h.append("</div>")
    h.append("</section>")
    return "".join(h)

def home():
    card = lambda m: (f'<a class="mod" href="#{m["id"]}"><div class="ic">{m["icon"]}</div><div><span class="num">{m["kind"]} {m["num"]}</span><b>{html.escape(m["title"])}</b>'
                      f'<span>{html.escape(m["sub"])}</span></div></a>')
    nq = sum(len([i for i in d["items"] if not i["hidden"]]) for d in CASES.values())
    nimg = sum(len(i["imgs"]) for d in CASES.values() for i in d["items"])
    ndg = len(glob.glob(os.path.join(SITE, "img", "*", "*.png")))
    ntabs = sum(len(m["tabs"]) for m in ALL)
    online = f'<a class="chip" href="{ONLINE}" target="_blank" rel="noopener">🔗 Online version</a>' if ONLINE else ""
    return f'''<section class="page" id="p-home" data-page="home">
<div class="hero"><div class="crumb" style="color:#F4C77D">DATA SCIENCE &amp; AI</div><h1>{TITLE}</h1>
<p>{PROGRAMME}. Course handbooks class by class (Building Blocks Class 1 onwards), {len(SESSIONS)} basic-to-advanced learning sessions written for non-technical learners, every case study solved on real data, an Excel practice workbook, and clickable PDFs.</p>
<div class="chips"><span class="chip">{len(MODULES)} course handbooks</span><span class="chip">{len(SESSIONS)} learning sessions</span><span class="chip">{len(CASES)} case studies · {nq} answers</span><a class="chip" href="#downloads">⬇ PDFs + Excel</a>{online}</div></div>
<div class="stats"><div class="stat"><b>{ntabs}</b><span>topic tabs</span></div><div class="stat"><b>{len(CASES)}</b><span>case studies solved</span></div><div class="stat"><b>{nq}</b><span>questions answered</span></div><div class="stat"><b>{ndg}</b><span>charts and diagrams</span></div></div>
<h2>Course handbooks</h2><p class="muted">Follow the AnalytixLabs course order. Building Blocks is organised exactly by class: Building Blocks · Class 1, Class 2, Class 3…</p><div class="mods">{"".join(card(m) for m in MODULES)}</div>
<h2>Learning sessions: basic to advanced</h2><p class="muted">Self-contained guides for non-technical learners that fill gaps beyond the course, each with its own PDF.</p><div class="mods">{"".join(card(m) for m in SESSIONS)}</div>
<h2>How to use this handbook</h2>
<div class="grid3"><div class="card"><h4>1. Learn</h4><p>Start with Building Blocks Class 1 and move tab by tab. Use the learning sessions when a topic needs more depth.</p></div>
<div class="card"><h4>2. Practise</h4><p>Use the Excel workbook and the case studies; attempt first, then open the Resolution tab.</p></div>
<div class="card"><h4>3. Revise</h4><p>Interview Q&amp;A tabs, the Interview session, and the PDFs for offline revision.</p></div></div>
<h2>Suggested 8-week plan</h2>
<table class="tbl"><thead><tr><th>Week</th><th>Learn</th><th>Practise</th></tr></thead><tbody>
<tr><td>1</td><td><a href="#m1">Building Blocks Classes 1–5</a> · <a href="#s1">Advanced Excel</a> levels 1–4</td><td>Excel workbook sheets 01–12</td></tr>
<tr><td>2</td><td><a href="#m1">Building Blocks Classes 6–8</a> · <a href="#m1b">Building Blocks ML Classes 1–5</a></td><td><a href="#case/xl_sports">Excel Sportsmen</a> · <a href="#case/sql_retail">SQL Retail</a></td></tr>
<tr><td>3</td><td><a href="#m1b">Building Blocks ML Classes 6–10</a> · <a href="#s2">SQL session</a></td><td><a href="#case/sql_mobile">SQL Mobile</a> · Excel sheets 13–18</td></tr>
<tr><td>4</td><td><a href="#m2">Python</a> · <a href="#s5">Python session</a></td><td><a href="#case/py_basic">Python basics</a> · <a href="#case/py_pandas90">90 pandas exercises</a></td></tr>
<tr><td>5</td><td><a href="#m3">DVA</a> · <a href="#m7">Power BI</a> · <a href="#s3">Power BI session</a></td><td><a href="#case/xl_complaints">Excel Complaints</a> · <a href="#case/py_retail">Retail</a></td></tr>
<tr><td>6</td><td><a href="#m8">Tableau</a> · <a href="#s4">Tableau session</a> · <a href="#s12">Storytelling</a></td><td><a href="#case/tb_laptops">Laptops</a> · <a href="#case/tb_sports">Sports Equipment</a></td></tr>
<tr><td>7</td><td><a href="#ml">ML Classes 1–7</a> · <a href="#s6">ML session</a> · <a href="#m5">ML Ops</a></td><td><a href="#case/py_hypothesis">Hypothesis testing</a> · <a href="#case/py_insurance">Insurance</a> · <a href="#case/py_ecom">E-commerce</a></td></tr>
<tr><td>8</td><td><a href="#m6">GenAI</a> · <a href="#s7">AI &amp; agents</a> · <a href="#s8">Tools</a> · <a href="#s11">Automation</a> · <a href="#s10">Reverse engineering</a></td><td><a href="#s9">Interview Q&amp;A</a></td></tr>
</tbody></table>
<p class="muted">Sources: AnalytixLabs LMS class titles and downloadable materials; vendor documentation and release notes (Microsoft, Tableau, OpenAI, Anthropic, Google); video channels including Simplilearn linked in each Resources tab. Case-study questions are summarised in our own words; sample data in the Excel workbook is fictional.</p>
</section>'''

PDFS = [("Data_Science_AI_Complete_Handbook.pdf", "Complete Handbook", "Everything: all course handbooks and all learning sessions, with a clickable table of contents."),
        ("Building_Blocks_Handbook.pdf", "Building Blocks Handbook", "Building Blocks Essentials Class 1–8 and Building Blocks of ML & Applied AI Class 1–10, with diagrams and real examples."),
        ("ML_Class_1-7_Illustrated_Notes.pdf", "ML Classes 1–7: Illustrated Notes", "Hypothesis testing to KNN with charts and worked Python, including the Bankloans case."),
        ("Case_Studies.pdf", "Case Studies (questions)", "All solved case studies: brief, data and questions."),
        ("Case_Study_Resolutions.pdf", "Case Study Resolutions", "Code, outputs, charts and insights for every question.")]
def session_pdf(m): return f'Session_{m["num"]}_' + re.sub(r"[^A-Za-z0-9]+", "_", re.sub(r"\s*\(.*?\)", "", m["title"])).strip("_") + ".pdf"
def downloads():
    cardf = lambda f, t, d: f'<div class="dlc"><b>📄 {t}</b><span>{d}</span><div class="btns"><a class="btn" href="pdf/{f}">Open PDF</a><a class="btn ghost" href="pdf/{f}" data-save>Download</a></div></div>'
    main = "".join(cardf(f, t, d) for f, t, d in PDFS)
    sess = "".join(cardf(session_pdf(m), f'{m["num"]} · {html.escape(m["title"])}', html.escape(m["sub"])) for m in SESSIONS)
    xl = ('<div class="dlc"><b>📗 Excel Basic-to-Advanced workbook</b><span>22 sheets: one per topic (environment, references, formats, number, text, date, aggregate, logical, lookup, '
          'conditional formatting, validation, sort &amp; filter, pivot, what-if, dynamic arrays, Power Query, charts, dashboard case study, automation &amp; AI) with 1,593 live formulas on 400 sample orders.</span>'
          '<div class="btns"><a class="btn" href="files/Excel_Basic_to_Advanced.xlsx" data-save>Download .xlsx</a></div></div>')
    return (f'<section class="page" id="p-downloads" data-page="downloads"><div class="crumb">FILES</div><h1>PDFs &amp; Excel workbook</h1>'
            f'<p class="lead">Offline copies of everything in this handbook. Every table of contents entry and cross-reference inside the PDFs is clickable.</p>'
            f'<h3>Handbooks and case studies</h3><div class="dl">{main}{xl}</div><h3>Learning session PDFs</h3><div class="dl">{sess}</div></section>')

JS = r"""
(function(){
  var pages = {}; document.querySelectorAll('.page').forEach(function(p){ pages[p.dataset.page] = p; });
  function setTab(page, name){
    var tabs = page.querySelectorAll('.tab'); if (!tabs.length) return;
    var found = null; tabs.forEach(function(t){ if (t.dataset.name === name) found = t; });
    if (!found) found = tabs[0];
    tabs.forEach(function(t){ t.classList.toggle('on', t === found); });
    page.querySelectorAll('.tabbar button').forEach(function(b){ b.classList.toggle('on', b.dataset.tab === found.dataset.name); b.setAttribute('aria-selected', b.dataset.tab === found.dataset.name); });
    var list = Array.prototype.slice.call(tabs), i = list.indexOf(found), nav = page.querySelector('.tabnav');
    if (nav) { var base = '#' + page.dataset.page + '/';
      nav.innerHTML = (i > 0 ? '<a href="' + base + encodeURIComponent(list[i-1].dataset.name) + '">← ' + list[i-1].dataset.name + '</a>' : '<span></span>') +
                      (i < list.length - 1 ? '<a href="' + base + encodeURIComponent(list[i+1].dataset.name) + '">' + list[i+1].dataset.name + ' →</a>' : '<span></span>'); }
  }
  function route(){
    var h = decodeURIComponent((location.hash || '#home').slice(1)), key = h, tab = null;
    var m = h.match(/^(case\/[a-z0-9_]+)(?:\/(.*))?$/) || h.match(/^([a-z0-9]+)(?:\/(.*))?$/);
    if (m) { key = m[1]; tab = m[2] || null; }
    if (!pages[key]) key = 'home';
    Object.keys(pages).forEach(function(k){ pages[k].classList.toggle('on', k === key); });
    setTab(pages[key], tab);
    document.querySelectorAll('.nav a').forEach(function(a){ a.classList.toggle('on', a.dataset.r === key); });
    var t = document.querySelector('.top b'); if (t) { var h1 = pages[key].querySelector('h1'); t.textContent = h1 ? h1.textContent : ''; }
    document.title = (pages[key].querySelector('h1') || {}).textContent + ' · Data Science & AI Handbook';
    document.body.classList.remove('menu'); window.scrollTo(0, 0);
  }
  document.addEventListener('click', function(e){
    var b = e.target.closest('.tabbar button');
    if (b) { var p = b.closest('.page'); location.hash = '#' + p.dataset.page + '/' + encodeURIComponent(b.dataset.tab); }
    if (e.target.closest('[data-menu]')) document.body.classList.toggle('menu');
  });
  window.addEventListener('hashchange', route);
  // search
  var idx = [];
  document.querySelectorAll('.page').forEach(function(p){
    var h1 = (p.querySelector('h1') || {}).textContent || '';
    var tabs = p.querySelectorAll('.tab');
    if (!tabs.length) idx.push({h: '#' + p.dataset.page, t: h1, s: '', x: p.textContent.toLowerCase()});
    tabs.forEach(function(t){ idx.push({h: '#' + p.dataset.page + '/' + encodeURIComponent(t.dataset.name), t: t.dataset.name, s: h1, x: t.textContent.toLowerCase()}); });
  });
  var box = document.getElementById('q'), res = document.getElementById('hits');
  if (box) box.addEventListener('input', function(){
    var q = box.value.trim().toLowerCase(); if (q.length < 2) { res.hidden = true; return; }
    var hits = idx.filter(function(r){ return r.x.indexOf(q) > -1 || r.t.toLowerCase().indexOf(q) > -1; }).slice(0, 12);
    res.innerHTML = hits.length ? hits.map(function(r){ return '<a href="' + r.h + '">' + r.t + (r.s ? ' <small>· ' + r.s + '</small>' : '') + '</a>'; }).join('') : '<a>No match</a>';
    res.hidden = false;
  });
  if (res) res.addEventListener('click', function(){ res.hidden = true; box.value = ''; });
  // theme
  var tb = document.getElementById('theme');
  if (tb) tb.addEventListener('click', function(){ var r = document.documentElement, d = r.getAttribute('data-theme');
    var dark = d ? d === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches; r.setAttribute('data-theme', dark ? 'light' : 'dark'); });
  route();
})();
"""

def site():
    css = open(os.path.join(HB, "style.css")).read()
    pages = home() + "".join(module_page(m) for m in ALL) + cases_index() + "".join(case_page(c) for _, ids in ORDER for c in ids) + downloads()
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Data Science &amp; AI Handbook</title><meta name="description" content="Data Science and AI handbook: course notes class by class, learning sessions, solved case studies, Excel workbook and PDFs.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<div class="top"><button type="button" data-menu aria-label="Open menu">☰ Menu</button><b></b></div>
<div class="app"><aside class="side"><div class="brand"><div class="logo">DS</div><div><b>Data Science &amp; AI</b><small>Handbook · course + sessions</small></div></div>
<input id="q" class="search" type="search" placeholder="Search topics, functions…" aria-label="Search"><div id="hits" class="hits" hidden></div>
{nav()}<div style="padding:16px 10px 0"><button id="theme" class="iconbtn" type="button">◐ Light / dark</button></div></aside>
<main class="main">{pages}</main></div><script>{JS}</script></body></html>'''
    open(os.path.join(SITE, "index.html"), "w").write(doc)
    print("site/index.html", len(doc) // 1024, "KB")

# ------------------------------------------------------------------ print documents
PRINT_CSS = """
@page{size:A4;margin:14mm 13mm 15mm}
body{background:#fff!important;font-size:10.6pt;line-height:1.5}
:root{--bg:#fff}
.page,.tab{display:block!important}
.pcover{height:262mm;display:flex;flex-direction:column;justify-content:center;padding:0 14mm;background:linear-gradient(160deg,#1F3864,#2C4C86);color:#fff;margin:0;border-radius:6mm;break-after:page}
.pcover h1{color:#fff;font-size:30pt;margin:0 0 6mm;line-height:1.1} .pcover p{color:#DCE4F5;font-size:12pt;max-width:150mm}
.pcover .k{color:#F4C77D;font-weight:800;letter-spacing:.14em;font-size:10pt}
.pcover a{color:#F4C77D}
.toc{break-after:page} .toc h2{margin-top:0} .toc ol{padding-left:0;list-style:none} .toc li{margin:1.6mm 0;font-size:11pt}
.toc li a{display:flex;color:#1A2233;font-weight:600} .toc li a::after{content:"";flex:1;border-bottom:1px dotted #B8C0D2;margin:0 2mm 1.2mm} .toc li.sub{padding-left:7mm;font-size:10pt} .toc li.sub a{font-weight:500;color:#4A5470}
.psec{break-before:page;display:block} .mtitle{border-bottom:3px solid #E9A23B;padding-bottom:3mm;margin-bottom:4mm}
.mtitle h1{margin:0;font-size:22pt} .mtitle .k{color:#E9A23B;font-weight:800;letter-spacing:.12em;font-size:9pt}
h2.tabh{font-size:15pt;color:#1F3864;border-left:5px solid #E9A23B;padding-left:3mm;margin-top:8mm;break-after:avoid}
h3{break-after:avoid} figure,.tbl tr,.ans h4,.card,.steps>div,.qa details{break-inside:avoid}
pre{white-space:pre-wrap;word-break:break-word;font-size:8.6pt;break-inside:auto}
.qa details>*{display:block} .qa summary::-webkit-details-marker{display:none}
.tbl{box-shadow:none;font-size:9.4pt} .card,figure,.ans,.stat{box-shadow:none}
figure img{max-height:120mm;width:auto}
.online{font-size:9pt;color:#7A839A} .online a{color:#2C4C86}
.tabnav,.tabbar,.side,.top{display:none!important}
.grid2,.prompts,.dl,.cgrid{grid-template-columns:repeat(2,minmax(0,1fr))!important}
.grid3,.cycle,.levels,.flowchart .fr{grid-template-columns:repeat(3,minmax(0,1fr))!important}
.joins{grid-template-columns:repeat(4,minmax(0,1fr))!important}
.tbl{display:table!important} h1{font-size:22pt}
"""
def plink(s, prefix_map):
    """Rewrite in-site hash links for a print document."""
    def rep(m):
        target = html.unescape(urllib.parse.unquote(m.group(1)))
        parts = target.split("/")
        if parts[0] == "case":
            cid = parts[1]
            if "case" in prefix_map: return f'href="#{prefix_map["case"]}-{cid}"'
            return f'href="{ONLINE}#case/{cid}"' if ONLINE else 'href="#"'
        if parts[0] == "cases":
            return f'href="{ONLINE}#cases"' if ONLINE else 'href="#"'
        mid = parts[0]
        if mid in prefix_map.get("mods", ()):
            return f'href="#{mid}--{slug(parts[1])}"' if len(parts) > 1 else f'href="#{mid}"'
        return f'href="{ONLINE}#{urllib.parse.quote(target)}"' if ONLINE else 'href="#"'
    return re.sub(r'href="#([^"]*)"', rep, s)

def print_doc(title, kicker, sub, toc, body, name):
    css = open(os.path.join(HB, "style.css")).read()
    online = f'<p style="margin-top:8mm">Interactive version (every tab clickable): <a href="{ONLINE}">{ONLINE}</a></p>' if ONLINE else ""
    doc = f'''<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>{css}{PRINT_CSS}</style></head><body data-theme="light">
<div class="pcover"><div class="k">{html.escape(kicker)}</div><h1>{html.escape(title)}</h1><p>{sub}</p><p style="margin-top:10mm;font-size:10pt">{PROGRAMME}</p>{online}</div>
<div class="toc"><h2>Contents</h2><ol>{toc}</ol></div>{body}</body></html>'''
    doc = doc.replace('<html><head>', '<html data-theme="light"><head>')
    open(os.path.join(SITE, name), "w").write(doc)

def module_print(m, mods):
    out = [f'<section class="psec" id="{m["id"]}"><div class="mtitle"><div class="k">{m["kind"]} {m["num"]}</div><h1>{m["icon"]} {html.escape(m["title"])}</h1><p>{html.escape(m["sub"])}</p><p class="courses">{html.escape(m["courses"])}</p>']
    if ONLINE: out.append(f'<p class="online">Open this module online: <a href="{ONLINE}#{m["id"]}">{ONLINE}#{m["id"]}</a></p>')
    out.append("</div>")
    for t, c in m["tabs"]:
        c2 = c.replace("<details>", "<details open>")
        out.append(f'<h2 class="tabh" id="{m["id"]}--{slug(t)}">{html.escape(t)}</h2>{plink(c2, {"mods": mods})}')
    out.append("</section>")
    return "".join(out)

def toc_for(ms):
    return "".join(f'<li><a href="#{m["id"]}">{m["num"]} · {html.escape(m["title"])}</a></li>' +
                   "".join(f'<li class="sub"><a href="#{m["id"]}--{slug(t)}">{html.escape(t)}</a></li>' for t, _ in m["tabs"]) for m in ms)
def build_prints():
    jobs = []
    ids = [m["id"] for m in ALL]
    toc = '<li style="margin-top:2mm"><b>Course handbooks</b></li>' + toc_for(MODULES) + '<li style="margin-top:4mm"><b>Learning sessions</b></li>' + toc_for(SESSIONS)
    print_doc(TITLE, "COMPLETE HANDBOOK", "Course handbooks: Building Blocks (Class 1 onwards) · Building Blocks of ML &amp; Applied AI · Python · Data Visualization &amp; Analytics · ML &amp; Text Mining · ML Ops · Generative AI · Power BI · Tableau<br><br>Learning sessions: Advanced Excel · SQL · Power BI · Tableau · Python · Machine Learning · AI &amp; Agents · Tools · Interview Q&amp;A · Reverse Engineering · Automation · Storytelling",
              toc, "".join(module_print(m, ids) for m in ALL), "print_complete.html"); jobs.append(("print_complete.html", PDFS[0][0], TITLE))
    bb = MODULES[:2]
    print_doc("Building Blocks Handbook", "BUILDING BLOCKS ESSENTIALS · BUILDING BLOCKS OF ML & APPLIED AI",
              "Building Blocks · Class 1 to Class 8 (Excel, RDBMS, DDL, SELECT &amp; joins, SQL Server setup, Statistics 1–3) and Building Blocks ML · Class 1 to Class 10 (programming, Statistics 1–4, Mathematics 1–5), with diagrams, real-world examples and the 2025–26 updates.",
              toc_for(bb), "".join(module_print(m, [x["id"] for x in bb]) for m in bb), "print_bb.html"); jobs.append(("print_bb.html", PDFS[1][0], "Building Blocks Handbook"))
    ml = [m for m in MODULES if m["id"] == "ml"][0]
    print_doc("ML Classes 1–7: Illustrated Notes", "MACHINE LEARNING, TEXT MINING & INTRO TO AI", "Hypothesis testing · CLT · p-values · ML problem types · project life cycle · link functions · gradient descent · pre-processing · over/underfitting · RFM · KNN · GridSearchCV · classification metrics · Bankloans case",
              "".join(f'<li><a href="#ml--{slug(t)}">{html.escape(t)}</a></li>' for t, _ in ml["tabs"]), module_print(ml, ["ml"]), "print_ml.html"); jobs.append(("print_ml.html", PDFS[2][0], "ML Classes 1–7"))
    for m in SESSIONS:
        name = f'print_{m["id"]}.html'
        print_doc(m["title"], f'LEARNING SESSION {m["num"]}', html.escape(m["sub"]), "".join(f'<li><a href="#{m["id"]}--{slug(t)}">{html.escape(t)}</a></li>' for t, _ in m["tabs"]),
                  module_print(m, [m["id"]]), name); jobs.append((name, session_pdf(m), f'Session {m["num"]} · {m["title"]}'))
    toc, body, body2 = [], [], []
    for g, cids in ORDER:
        toc.append(f'<li style="margin-top:4mm"><b>{html.escape(g)}</b></li>')
        for cid in cids:
            d = CASES[cid]
            toc.append(f'<li class="sub"><a href="#c-{cid}">{html.escape(d["title"])}</a></li>')
            body.append(f'<section class="psec" id="c-{cid}"><div class="mtitle"><div class="k">{html.escape(g.upper())}</div><h1>{html.escape(d["title"])}</h1></div>{case_header(d)}<h3>Questions</h3>{case_q_list(d)}</section>')
            body2.append(f'<section class="psec" id="r-{cid}"><div class="mtitle"><div class="k">{html.escape(g.upper())} · RESOLUTION</div><h1>{html.escape(d["title"])}</h1></div>{case_header(d)}{case_answers(d)}</section>')
    toc_s = "".join(toc)
    print_doc("Case Studies", "PRACTICE QUESTIONS", "Every downloadable case study from the LMS, summarised with its data and questions. Attempt them first; answers are in the Case Study Resolutions PDF.", toc_s, "".join(body), "print_cases.html"); jobs.append(("print_cases.html", PDFS[3][0], "Case Studies"))
    print_doc("Case Study Resolutions", "ANSWERS, CODE AND CHARTS", "Every question solved on the real case data: code (Python, T-SQL, Excel or Tableau steps), outputs, charts and business insights.", toc_s.replace('href="#c-', 'href="#r-'), "".join(body2), "print_resolutions.html"); jobs.append(("print_resolutions.html", PDFS[4][0], "Case Study Resolutions"))
    json.dump(jobs, open(os.path.join(HB, "pdf_jobs.json"), "w"), indent=1)
    print("print docs written:", len(jobs))

if __name__ == "__main__":
    site(); build_prints()
