"""Hub page, search index, print books and PDF job list."""
import os, json, html, re

esc = lambda s: html.escape(str(s))

# Live class tracker: what was taught live, mapped to the handbook lessons that cover it (and extend it).
LIVE = [
    ("Data Visualization & Analytics 2026 (Excel)", [
        ("Class 1", "Programme introduction and orientation", ["excel-01"]),
        ("Class 2", "Basics of Excel, terminology, shortcuts, properties, data types, data validation, formatting, number and custom number formatting, conditional and custom conditional formatting, first worksheet", ["excel-01", "excel-02", "excel-03"]),
        ("Class 3", "Formulas vs functions; aggregate (SUM, COUNT, COUNTA, COUNTBLANK, AVERAGE, MIN, MAX, SMALL, LARGE); text (LEFT, RIGHT, MID, CONCAT, TEXTJOIN, LOWER, UPPER, PROPER, LEN, TRIM, FIND, SEARCH, TEXT); logical (AND, OR, NOT); Text to Columns; IF", ["excel-04", "excel-05"]),
        ("Class 4", "Doubts; IF, IFS, nested IF; array functions; sorting and level-wise sorting; filtering; remove duplicates; UNIQUE(); SUMPRODUCT; VLOOKUP, HLOOKUP, XLOOKUP", ["excel-05", "excel-06"]),
        ("Class 5", "Reverse lookup, INDEX, MATCH, INDEX + MATCH, CHOOSE, VLOOKUP with CHOOSE; pivot tables, pivot cache, pivot areas, filtering, grand total", ["excel-06", "excel-07"]),
        ("Class 6", "Pivot refresh vs Refresh All, groups and bins, grand and sub totals, expand/collapse, MoM and YoY, calculated fields; Video Game Sales case study", ["excel-07"]),
        ("Class 7", "Running totals, slicers, value field settings; date and time functions; number functions", ["excel-07", "excel-08"]),
        ("Class 8", "Named ranges (static and dynamic); thermometer, Pareto, population pyramid and waterfall charts; Superstore case study begins", ["excel-08", "excel-09"]),
        ("Class 9", "Superstore dashboard; protected sheet and workbook; Power Pivot; Power Query Editor; comments; descriptive statistics with Analysis ToolPak; Evaluate Formula", ["excel-09", "excel-10"]),
    ]),
    ("SQL", [
        ("SQL 1", "SQL basics, terminology, ER diagrams, relationship types, keys (primary, foreign, super, candidate, alternate, composite), DDL/DML/DCL/TCL, installing SSMS", ["sql-01", "sql-02"]),
        ("SQL 2", "Properties of SQL, data types, variables and naming rules, operators, comments, Excel vs SQL; CREATE, ALTER, DROP, TRUNCATE; INSERT, DELETE, SELECT; DELETE vs DROP vs TRUNCATE", ["sql-03", "sql-04"]),
        ("SQL 3", "Constraints; aliases with AS; SELECT, WHERE, ORDER BY; IN, NOT IN, LIKE, NOT LIKE, IS NULL, IS NOT NULL", ["sql-04", "sql-05"]),
        ("SQL 4", "GROUP BY and HAVING; aggregate, text, date and number functions; DATEPART(); CASE WHEN; case study with joins; UNION ALL, UNION, INTERSECT, EXCEPT; subqueries", ["sql-06", "sql-07", "sql-08", "sql-09", "sql-10"]),
        ("SQL 5", "End-to-end case study; OFFSET FETCH; window functions; OVER, PARTITION BY; RANK, DENSE_RANK, ROW_NUMBER; aggregate windows; LEAD and LAG; CTEs, views, stored procedures", ["sql-11", "sql-12", "sql-13", "sql-15"]),
        ("SQL + Power BI bridge", "ROLLUP, CUBE and COALESCE()", ["sql-07"]),
    ]),
    ("Power BI", [
        ("Power BI 1", "Components and views, installing Power BI Desktop, ETL, analytics stages; HR data analysis; visuals and formatting; YEAR() DAX column; data groups", ["powerbi-01", "powerbi-02"]),
        ("Power BI 2", "Small multiples; DAX measures and columns; cards and matrix; filters on cards; chart formatting; images", ["powerbi-03", "powerbi-04"]),
        ("Power BI 3", "Adventure Works case study; hierarchies; custom tooltips; KPIs, cards and gauges; visual, page and report filters; edit interactions; custom themes; conditional formatting; marking a date table", ["powerbi-05", "powerbi-06"]),
        ("Power BI 4", "Parameters and dynamic measures; Q&A; forecasting; buttons and bookmarks; drill-through, include/exclude; import vs DirectQuery; display folders", ["powerbi-06", "powerbi-07"]),
    ]),
    ("Data Visualization & Analytics with AI", [
        ("DVA + AI 1", "Unpivot columns in Power Query; GenAI basics; prompt engineering; AI vs GenAI vs Agentic AI", ["ai-analytics-01", "ai-analytics-02"]),
        ("DVA + AI 2", "AI in SQL; installing Docker; Metabase and MinusX", ["ai-analytics-03"]),
        ("DVA + AI 3", "Gemini in Excel, Copilot for Excel, office agents", ["ai-analytics-04"]),
    ]),
    ("Python", [
        ("Python 1", "Course intro, properties of Python, installations, Jupyter notebooks, intro to programming", ["python-01"]),
        ("Python 2", "Type conversion, print(), f-strings, .format(), input()", ["python-02", "python-03"]),
        ("Python 3", "Control flow: if/elif/else, while loops", ["python-04", "python-05"]),
        ("Python 4", "for loops, intro to OOP, string methods, indexing and slicing", ["python-05", "python-03", "python-11"]),
        ("Python 5", "Data structures: lists, dictionaries, tuples, sets", ["python-06", "python-07", "python-08"]),
        ("Python 6", "User-defined functions, lambda, map() and filter()", ["python-09", "python-10"]),
        ("Python 7", "File handling, modules and packages", ["python-12", "python-13"]),
        ("Python 8", "NumPy arrays", ["python-15"]),
        ("Python 9", "pandas DataFrames: subsetting, reordering, renaming, dropping, sorting, filtering", ["python-16"]),
        ("Python 10", "Type conversion, univariate analysis, aggregate functions, missing values", ["python-17", "python-18"]),
        ("Python 11", "Joining datasets, groupby and pivot_table", ["python-18"]),
        ("Python 12", "Visualisation in Python", ["python-20", "python-21", "python-22"]),
        ("Python 13", "Dates in Python, outlier treatment, connecting to SQL databases", ["python-19", "python-17", "python-23"]),
        ("Python 14", "Matplotlib subplots, probability distributions, normal distribution, inferential statistics, CLT", ["python-20", "ml-01", "ml-02", "ml-03"]),
        ("Python 15", "Sampling, CLT, hypothesis testing; z, t, chi-square and ANOVA", ["ml-03", "ml-04", "ml-05"]),
        ("Python 16", "Intro to ML and statistical modelling; linear and logistic regression", ["ml-07", "ml-10", "ml-13"]),
    ]),
    ("Machine Learning", [
        ("ML 1", "Hypothesis testing, CLT, parametric vs non-parametric tests, hypothesis-testing case study", ["ml-03", "ml-04", "ml-05"]),
        ("ML 2", "Tests in the case study, p-value, alpha, critical value, one-tailed vs two-tailed", ["ml-04", "ml-06"]),
        ("ML 3", "Conclusion of hypothesis testing; intro to ML; business problem types; business to statistics problem; types of ML systems", ["ml-05", "ml-07"]),
        ("ML 4", "Life cycle of analytics and ML projects; linear vs non-linear models; linear equations and link functions", ["ml-07", "ml-08", "ml-13"]),
        ("ML 5", "Gradient descent for linear regression in Python", ["ml-11"]),
        ("ML 6", "Pre-processing: missing values, outliers, categorical encoding; overfitting and underfitting; heuristic segmentation (RFM)", ["ml-09", "ml-15", "ml-22"]),
        ("ML 7", "KNN classifier and regressor, GridSearchCV, Bank Loans case study, classification metrics", ["ml-16", "ml-15", "ml-14"]),
    ]),
]


def build(lessons, rendered, by_track, G):
    ROOT, TRACKS, TITLE, BRAND, AUTHOR, VERSION, UPDATED, BUILD_VER, REPO, SITE, ARTIFACT = (G[k] for k in ("ROOT", "TRACKS", "TITLE", "BRAND", "AUTHOR", "VERSION", "UPDATED", "BUILD_VER", "REPO", "SITE", "ARTIFACT"))
    core = [L for L in lessons if not next(t for t in TRACKS if t["id"] == L.track).get("extra")]
    HEAD, topbar, FOOT, inline_md = G["HEAD"], G["topbar"], G["FOOT"], G["inline_md"]
    byid = {L.id: L for L in lessons}
    total_words = sum(c["words"] for c in rendered.values()); n_img = sum(len(c["imgs"]) for c in rendered.values()); n_q = sum(len(c["quiz"]) for c in rendered.values())
    # ---------------------------------------------------------- search index
    idx = [dict(i=L.id, t=L.title, k=next(t["short"] for t in TRACKS if t["id"] == L.track), f="lessons/" + L.file, s=rendered[L.id]["search"][:1500]) for L in lessons]
    open(os.path.join(ROOT, "assets", "search-index.js"), "w").write("window.SN_INDEX=" + json.dumps(idx, ensure_ascii=False) + ";")
    # ---------------------------------------------------------- hub page
    stat = lambda n, l: f'<div class="stat"><b>{n}</b><span>{l}</span></div>'
    tr_cards = []
    for t in TRACKS:
        Ls = by_track[t["id"]]
        if not Ls or t.get("extra"): continue   # "Other programs" guides live on skillnavora.in, not in this handbook
        tpdf = f"pdf/tracks/{track_pdf_name(t, TRACKS)}"
        rows = "".join(f'<li><a href="lessons/{L.file}" data-lid="{L.id}"><span class="n">{L.num:02d}</span><span class="tt">{esc(L.title)}'
                       + (f'<em class="lv">● {esc(L.meta["live"])}</em>' if L.meta.get("live") else "") + '</span></a>'
                       f'<a class="pdf" href="pdf/{L.track}/{L.pdf}" download title="Download PDF">PDF</a></li>' for L in Ls)
        tr_cards.append(f'''<section class="track" id="t-{t["id"]}" style="--tc:{t["color"]}"><div class="track-h"><div><div class="kick">Track {TRACKS.index(t) + 1} · {len(Ls)} lessons</div><h2>{esc(t["name"])}</h2><p>{esc(t["desc"])}</p></div>
<div class="track-a"><a class="btn" href="lessons/{Ls[0].file}">Start lesson 1 →</a><a class="btn ghost" href="{tpdf}" download>⬇ Track PDF</a><div class="prog" data-track="{t["id"]}" data-n="{len(Ls)}"><i></i><span>0 / {len(Ls)} done</span></div></div></div>
<ol class="lessons">{rows}</ol></section>''')
    live_rows = []
    for course, items in LIVE:
        live_rows.append(f'<tr class="lgrp"><td colspan="3">{esc(course)}</td></tr>')
        for cls, topics, ids in items:
            links = " ".join(f'<a href="lessons/{byid[i].file}">{esc(byid[i].title)}</a>' for i in ids if i in byid)
            live_rows.append(f"<tr><td><b>{esc(cls)}</b></td><td>{esc(topics)}</td><td class='ll'>{links}</td></tr>")
    practice = "".join(f'<div class="pcard" style="--tc:{t["color"]}"><b>{esc(t["short"])}</b><ul>' + "".join(f'<li><a target="_blank" rel="noopener" href="{u}">{esc(n)} ↗</a></li>' for n, u in t["practice"]) + "</ul></div>" for t in TRACKS)
    ds = []
    for f, d in DATASETS:
        p = os.path.join(ROOT, "datasets", f)
        if os.path.exists(p):
            import pandas as pd
            n = len(pd.read_csv(p))
            ds.append(f'<tr><td><a href="datasets/{f}" download>{esc(f)}</a></td><td>{n:,}</td><td>{esc(d)}</td></tr>')
    pdfs = "".join(f'<li><a href="pdf/tracks/{track_pdf_name(t, TRACKS)}" download>{esc(t["name"])}</a><small>{len(by_track[t["id"]])} lessons</small></li>' for t in TRACKS if by_track[t["id"]])
    art = f'<a class="btn ghost light" href="{ARTIFACT}" target="_blank" rel="noopener">Interactive version ↗</a>' if ARTIFACT else ""
    hub = HEAD.format(title=f"{TITLE} · {BRAND}", desc="Complete Data Science & AI handbook: Excel, SQL, Power BI, Python, statistics, machine learning, generative and agentic AI. Class-wise lessons with PDFs, quizzes and practice.", r="", v=BUILD_VER, bodycls="hub") + topbar("", "") + f'''
<section class="hero"><div class="hero-in"><div class="kick light">AI-First Data Engineer · Data Science & AI</div><h1>{TITLE}</h1>
<p>Every class, explained simply. {len(core)} lessons across Excel, SQL, Power BI, Python, statistics, machine learning, generative AI and agentic AI, with real outputs, diagrams, quizzes, practice files and a downloadable PDF for each lesson.</p>
<div class="hero-a"><a class="btn light" href="lessons/{lessons[0].file}">Start learning →</a><a class="btn ghost light" href="#downloads">⬇ Complete handbook PDF</a><a class="btn ghost light" href="#live">Live class tracker</a>{art}</div>
<div class="stats">{stat(len(core), "lessons")}{stat(len([t for t in TRACKS if by_track[t["id"]] and not t.get("extra")]), "tracks")}{stat(f"{n_img}+", "diagrams and charts")}{stat(n_q, "quiz questions")}{stat(f"{total_words // 1000}k", "words")}</div>
<div class="by">Created by <b>{AUTHOR}</b> · Version {VERSION} · Updated {UPDATED}</div></div></section>
<main class="hubmain">
<section class="how"><div class="hstep"><b>1</b><span>Pick your track or follow the live class tracker.</span></div><div class="hstep"><b>2</b><span>Read the lesson, run the examples and look at every chart.</span></div><div class="hstep"><b>3</b><span>Take the quiz, solve the exercises, then practise online.</span></div><div class="hstep"><b>4</b><span>Download the PDF to revise offline and tick the lesson complete.</span></div></section>
<nav class="tnav">{"".join(f'<a href="#t-{t["id"]}" style="--tc:{t["color"]}">{esc(t["short"])}<small>{len(by_track[t["id"]])}</small></a>' for t in TRACKS if by_track[t["id"]] and not t.get("extra"))}</nav>
{"".join(tr_cards)}
<section class="block" id="live"><h2>Live class tracker</h2><p>What each live class covered, and the handbook lessons that explain it in detail. Lessons go further than the class, with the latest 2026 features.</p>
<div class="tblwrap"><table class="tbl live">{"".join(live_rows)}</table></div></section>
<section class="block" id="practice"><h2>Practice hub</h2><p>Every lesson ends with a quiz and exercises. For more practice, these free sites have exercises, quizzes and coding challenges. Links open the original site.</p><div class="pgrid">{practice}</div></section>
<section class="block" id="datasets"><h2>Practice datasets</h2><p>All datasets are fictional and generated for this handbook, so you can share and reuse them freely. Download a CSV and follow along in Excel, SQL, Power BI or Python.</p>
<div class="tblwrap"><table class="tbl"><tr><th>File</th><th>Rows</th><th>What it contains</th></tr>{"".join(ds)}</table></div></section>
<section class="block" id="downloads"><h2>Downloads</h2><div class="dl"><div><h3>Complete handbook</h3><p>All {len(lessons)} lessons (1,211 pages) in four PDF parts, one per group of tracks.</p><a class="btn" href="pdf/SkillNavora_Data_Science_AI_Complete_Handbook_Part1.pdf" download style="margin:0 6px 6px 0">⬇ Part 1: Excel, SQL, Power BI, AI (497 pages)</a><a class="btn" href="pdf/SkillNavora_Data_Science_AI_Complete_Handbook_Part2.pdf" download style="margin:0 6px 6px 0">⬇ Part 2: Python (300 pages)</a><a class="btn" href="pdf/SkillNavora_Data_Science_AI_Complete_Handbook_Part3.pdf" download style="margin:0 6px 6px 0">⬇ Part 3: Statistics &amp; ML (277 pages)</a><a class="btn" href="pdf/SkillNavora_Data_Science_AI_Complete_Handbook_Part4.pdf" download style="margin:0 6px 6px 0">⬇ Part 4: GenAI &amp; Career (149 pages)</a></div>
<div><h3>Track PDFs</h3><ul class="pdfl">{pdfs}</ul></div><div><h3>Lesson PDFs and workbooks</h3><p>Every lesson has its own PDF (the “PDF” link next to it). Excel lessons also include a practice workbook with live formulas.</p><a class="btn ghost" href="{REPO}" target="_blank" rel="noopener">Source on GitHub ↗</a></div></div></section>
</main>''' + FOOT.format(brand=BRAND, title=TITLE, author=AUTHOR, ver=VERSION, upd=UPDATED, r="", v=BUILD_VER)
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(hub)
    # ---------------------------------------------------------- print books
    jobs = []
    for L in lessons:
        jobs.append([f"lessons/{L.file}", f"pdf/{L.track}/{L.pdf}", f"{BRAND} · {TITLE} · {next(t['short'] for t in TRACKS if t['id'] == L.track)} Lesson {L.num}: {L.title}"])
    for t in TRACKS:
        Ls = by_track[t["id"]]
        if not Ls: continue
        fn = f"track-{t['id']}.html"
        open(os.path.join(ROOT, "print", fn), "w", encoding="utf-8").write(book(t["name"], f"Track {TRACKS.index(t) + 1}", t["desc"], [(t, Ls)], rendered, G, color=t["color"]))
        jobs.append([f"print/{fn}", f"pdf/tracks/{track_pdf_name(t, TRACKS)}", f"{BRAND} · {TITLE} · {t['name']}"])
    groups = [(t, by_track[t["id"]]) for t in TRACKS if by_track[t["id"]] and not t.get("extra")]
    open(os.path.join(ROOT, "print", "complete.html"), "w", encoding="utf-8").write(book(TITLE, "Complete handbook", f"{len(core)} lessons across Excel, SQL, Power BI, AI for analytics, Python, statistics and machine learning, generative and agentic AI, and career preparation.", groups, rendered, G, color="#6C4CF5", complete=True))
    jobs.append(["print/complete.html", "pdf/SkillNavora_Data_Science_AI_Complete_Handbook.pdf", f"{BRAND} · {TITLE} · Complete handbook"])
    json.dump(jobs, open(os.path.join(ROOT, "source", "pdf_jobs.json"), "w"), indent=0)


def track_pdf_name(t, TRACKS):
    return f"Track_{TRACKS.index(t) + 1:02d}_" + re.sub(r"[^A-Za-z0-9]+", "_", t["name"]).strip("_") + ".pdf"


DATASETS = [
    ("superstore_sales.csv", "Retail orders 2023–2025 across Indian cities: dates, ship mode, customer, segment, region, product, category, sales, quantity, discount, profit"),
    ("customers.csv", "Customer master: id, name, segment, city, state, region"), ("products.csv", "Product master: id, category, sub-category, name, list price"),
    ("video_game_sales.csv", "Fictional game titles with platform, year, genre, publisher and regional sales (millions)"),
    ("hr_employees.csv", "1,500 employees: department, role, education, hire date, income, satisfaction, overtime, rating, attrition"),
    ("employees_small.csv", "20-row employee table used in the Excel and SQL basics lessons"), ("lookup_products.csv", "6-row product table used in the Excel lookup lesson"), ("reps_small.csv", "8-row sales reps table used in the Excel sorting, filtering and dynamic array lesson"),
    ("bank_loans.csv", "Loan applicants: age, education, employment and address years, income, debt ratios, default flag (last 150 rows are new applicants)"),
    ("house_prices.csv", "Homes in four cities: area, rooms, age, distance to centre, parking, price in lakh (with some missing values and outliers)"),
    ("retail_transactions.csv", "Invoices per customer for RFM segmentation"), ("telecom_churn.csv", "Subscribers with tenure, contract, service, charges, support calls and churn"),
    ("daily_sales.csv", "Daily units sold 2022–2025 with trend, seasonality and weekend effect"), ("ab_test.csv", "A/B test of a new checkout: group, converted, order value"),
    ("delivery_times.csv", "Delivery minutes in two cities (two-sample t-test)"), ("channel_survey.csv", "Age group vs preferred shopping channel (chi-square test)"),
    ("diet_study.csv", "Weight loss under three diets (ANOVA)"), ("product_reviews.csv", "Short product reviews with rating and sentiment label (NLP)"), ("customer_reviews.csv", "3,000 realistic e-commerce reviews with stars, sentiment, negation and mixed opinions (text classification)"),
    ("adventure_cycles/fact_sales.csv", "Power BI case study fact table: order date, product, customer, territory, quantity, sales, cost"),
    ("adventure_cycles/dim_product.csv", "Power BI case study: product dimension"), ("adventure_cycles/dim_customer.csv", "Power BI case study: customer dimension"),
    ("adventure_cycles/dim_territory.csv", "Power BI case study: territory dimension"), ("adventure_cycles/dim_date.csv", "Power BI case study: date table"),
]


def book(title, kicker, desc, groups, rendered, G, color, complete=False):
    TITLE, BRAND, AUTHOR, VERSION, UPDATED, BUILD_VER, SITE = (G[k] for k in ("TITLE", "BRAND", "AUTHOR", "VERSION", "UPDATED", "BUILD_VER", "SITE"))
    inline_md = G["inline_md"]
    n = sum(len(Ls) for _, Ls in groups)
    toc = []
    for t, Ls in groups:
        if complete: toc.append(f'<li class="tg"><a href="#T-{t["id"]}">{esc(t["name"])}</a></li>')
        toc += [f'<li><a href="#L-{L.id}"><span>{L.num:02d}</span>{esc(L.title)}</a></li>' for L in Ls]
    parts = [f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{esc(title)} · {BRAND}</title><link rel="stylesheet" href="../assets/course.css?v={BUILD_VER}"></head><body class="book">
<section class="cover" style="--tc:{color}"><div class="cv-brand"><img src="../assets/logo.svg" alt="">Skill<em>Navora</em></div><div class="cv-k">{esc(kicker)}</div><h1>{esc(title)}</h1><p>{esc(desc)}</p>
<div class="cv-m"><span>{n} lessons</span><span>Version {VERSION}</span><span>Updated {UPDATED}</span></div><div class="cv-by">Created by <b>{AUTHOR}</b><br>{SITE.replace("https://", "")}</div></section>
<section class="btoc"><h2>Contents</h2><p class="muted">Every entry is a clickable link. The PDF also has bookmarks for each lesson and section.</p><ol class="tocl{' two' if n > 12 else ''}">{"".join(toc)}</ol></section>''']
    for t, Ls in groups:
        if complete:
            parts.append(f'<section class="tdiv" id="T-{t["id"]}" style="--tc:{t["color"]}"><div class="k">Track {G["TRACKS"].index(t) + 1}</div><h1>{esc(t["name"])}</h1><p>{esc(t["desc"])}</p><ol>' + "".join(f"<li>{esc(L.title)}</li>" for L in Ls) + "</ol></section>")
        for L in Ls:
            c = rendered[L.id]; m = L.meta
            out = "".join(f"<li>{inline_md(o)}</li>" for o in m.get("outcomes", []))
            tags = (f'<span class="tag live">● {esc(m["live"])}</span>' if m.get("live") else "") + (f'<span class="tag new">✦ {esc(m["updated"])}</span>' if m.get("updated") else "")
            parts.append(f'''<article class="lesson-art bk" id="L-{L.id}"><div class="lhead" style="--tc:{t["color"]}"><div class="kick">{esc(t["name"])} · Lesson {L.num}</div><h1>{esc(L.title)}</h1>
<p class="sum">{inline_md(m.get("summary", ""))}</p><div class="tags">{tags}<span class="tag">{esc(m.get("level", ""))}</span><span class="tag">⏱ {esc(m.get("duration", ""))}</span></div></div>
<div class="outcomes"><div><b>By the end of this lesson you can</b><ul>{out}</ul></div></div><div class="content">{c["html"]}</div></article>''')
    parts.append("</body></html>")
    h = "".join(parts)
    # ids must be unique across the book: prefix heading ids with lesson id
    out, cur = [], ""
    for chunk in re.split(r'(<article class="lesson-art bk" id="L-[^"]+")', h):
        mm = re.match(r'<article class="lesson-art bk" id="L-([^"]+)"', chunk)
        if mm: cur = mm.group(1); out.append(chunk); continue
        if cur:
            chunk = re.sub(r'(<h[2-4] id=")([^"]+)"', lambda x: f'{x.group(1)}{cur}-{x.group(2)}"', chunk)
            chunk = re.sub(r'href="#([^"L][^"]*)"', lambda x: f'href="#{cur}-{x.group(1)}"', chunk)
        out.append(chunk)
    return "".join(out)
