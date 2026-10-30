---
num: 1
title: Getting Started with Power BI & Your First HR Report
live: "Power BI class 1"
updated: "Power BI Desktop 2026 (Copilot, Fabric, PBIP)"
level: Beginner
duration: 120 min
summary: Understand what Power BI is and how its parts fit together, install Power BI Desktop, tour the three views, follow the ETL and analytics stages, and build a complete first report on HR data: cards, bar and column charts, a donut, slicers, a year column with DAX, groups and small multiples.
datasets: [hr_employees.csv]
outcomes:
  - Describe Power BI Desktop, the Service and Mobile, and how data flows between them
  - Explain ETL and the stages of the data-analytics process, and map them to Power BI tools
  - Navigate Report, Table and Model views, and the Fields, Visualizations and Filters panes
  - Load a CSV, check data types and build cards, bar/column charts, a matrix, a donut and slicers
  - Add a calculated column with DAX (YEAR), create data groups, and use small multiples
---

## What is Power BI?

**Power BI** is Microsoft's business-intelligence platform: it connects to data, cleans and models it, and turns it into interactive reports and dashboards that people can share. In 2026 it is part of **Microsoft Fabric**, Microsoft's all-in-one analytics platform, and it is one of the most requested tools in analyst job posts, alongside Excel, SQL and Tableau.

```python fig: The Power BI components. You build in Desktop, publish to the Service, and consume on the web or mobile.
dg.flow(["Data sources: Excel, CSV, SQL, web, cloud", "Power BI Desktop (build: connect, model, visualise)", "Power BI Service (share: workspaces, refresh, apps)", "Mobile & web (consume, alerts, Copilot)"], colors=[dg.SKY, dg.GOLD, dg.VIO, dg.TEAL], title="Power BI architecture")
```

| Component | What it is | Who uses it |
|---|---|---|
| **Power BI Desktop** | Free Windows application to build data models and reports (`.pbix`) | Analysts, developers |
| **Power BI Service** (app.powerbi.com) | Cloud site to publish, share, schedule refresh, create dashboards and apps | Analysts and report consumers |
| **Power BI Mobile** | iOS/Android apps to view reports and get alerts | Managers on the go |
| **Power BI Report Builder** | Paginated, print-ready reports (invoices, statements) | Report developers |
| **On-premises data gateway** | Secure bridge so the cloud can refresh data from your own servers | Admins |
| **Power BI Report Server** | Self-hosted option for organisations that cannot use the cloud | IT |
| **Copilot** | AI assistant that writes DAX, builds report pages and summarises insights (needs a Fabric/Premium capacity) | Everyone |

:::tip Report vs dashboard
In Power BI a **report** is one or more pages of interactive visuals built on a data model. A **dashboard** (Service only) is a single page of **pinned tiles** from different reports. Many teams use reports only, or share them as an **app**.
:::

### Licences in brief

| Licence | Use |
|---|---|
| Power BI Desktop | Free: build and save locally |
| Free (Service) | Personal use in "My workspace"; cannot share with others |
| **Pro** | Publish and share with other Pro users (about US$14 per user per month) |
| **Premium Per User / Fabric capacity** | Larger models, AI features, share with free users |

(Prices change; check Microsoft's current pricing page.)

## Installing Power BI Desktop

:::steps Install
1. **Easiest:** open the **Microsoft Store**, search "Power BI Desktop" and click Install (it updates itself every month).
2. Or download it from the Microsoft Power BI website → Download → Power BI Desktop.
3. Requirements: Windows 10/11 (64-bit), 4 GB+ RAM (8 GB+ recommended). **There is no Mac version**: Mac users can use the Service in a browser, a Windows virtual machine, or Windows 365.
4. Start the app and sign in with a work or school account (optional for building locally).
:::

## The three views

```python fig: The Power BI Desktop window: left rail with three views, canvas in the middle, panes on the right.
dg.window("Power BI Desktop — HR_Report.pbix", [("Left rail", "Report view · Table view · Model view (+ DAX query view)"), ("Ribbon", "Home · Insert · Modeling · View · Optimize · Help"),
          ("Canvas (centre)", "The report page where you place visuals"), ("Filters pane", "Visual-level · Page-level · All-pages filters"),
          ("Visualizations pane", "Chart types, field wells (Axis, Values, Legend…) and Format"), ("Data pane (Fields)", "Tables and columns; drag fields to the canvas"), ("Page tabs (bottom)", "Page 1 · Page 2 · + new page")], width=9.4, accent="#E2A400")
```

| View | Icon | Use it to |
|---|---|---|
| **Report** | bar chart | Design the report pages |
| **Table** (Data) | grid | Inspect the data and create calculated columns and measures |
| **Model** | diagram | See and edit **relationships** between tables |
| **DAX query view** | `{ }` | Run DAX queries and test measures |

## ETL and the analytics process

**ETL** = **E**xtract (get data from sources), **T**ransform (clean and reshape it), **L**oad (store it in the model). In Power BI, Extract and Transform are done in **Power Query**, and Load puts the result into the data model. (You met Power Query in Excel Lesson 12: it is the same engine.)

```python fig: The data analytics stages, mapped to Power BI.
dg.flow(["1. Ask the question", "2. Get data (Power Query)", "3. Clean & shape (Power Query)", "4. Model (relationships)", "5. Analyse (DAX)", "6. Visualise (Report)", "7. Share & act (Service)"], colors=dg.PAL, title="From question to decision", w=12)
```

Always start with the **question**: "Why are people leaving?" decides which data and visuals you need. The worst Power BI reports are tours of every chart type with no question.

## Your first report: HR attrition

:::case The brief
HR wants a one-page report on the company's 1,500 employees: how many there are, how many left (attrition), where attrition is highest, and whether overtime, job satisfaction or income play a role. Use `hr_employees.csv`.
:::

The data (first rows):

```python run
import pandas as pd
hr = pd.read_csv("hr_employees.csv", parse_dates=["hire_date"])
print(hr.shape)
hr.head(5)
```

### Step 1: get the data

:::steps Load the CSV
1. Home → **Get data → Text/CSV** → choose `hr_employees.csv`.
2. The preview shows the columns and detected data types. Click **Transform Data** (not Load) to check types in Power Query.
3. Confirm: `age`, `years_at_company`, `monthly_income`, `job_satisfaction`, `performance_rating` are whole numbers; `hire_date` is **Date**; the rest are text.
4. Home → **Close & Apply**.
:::

In the Data pane you now see the table `hr_employees` with a **Σ** next to numeric fields (they can be summed) and no symbol next to text fields.

### Step 2: KPI cards

Drag fields onto the canvas, then choose the **Card** visual:

- **Employees** = Count of `emp_id`
- **Attrition (leavers)**: use a measure (Lesson 3 explains measures): `Leavers = CALCULATE ( COUNTROWS ( hr_employees ), hr_employees[attrition] = "Yes" )`
- **Attrition %** = `DIVIDE ( [Leavers], COUNTROWS ( hr_employees ) )`, formatted as a percentage
- **Average monthly income** = Average of `monthly_income`

```python run
n = len(hr); leavers = (hr.attrition == "Yes").sum()
print(f"Employees      : {n:,}")
print(f"Leavers        : {leavers:,}")
print(f"Attrition %    : {leavers / n:.1%}")
print(f"Avg income (₹) : {hr.monthly_income.mean():,.0f}")
```

### Step 3: bar, column and donut charts

- **Clustered bar chart**: Y-axis `department`, X-axis = `Attrition %` → ranks departments.
- **Clustered column chart**: X-axis `job_satisfaction`, Y-axis `Attrition %`.
- **Donut chart**: Legend `attrition`, Values = count of `emp_id`.
- **Matrix**: Rows `department`, Columns `overtime`, Values `Attrition %` (turns into a heat map with conditional formatting, Lesson 5).
- **Slicers**: `gender`, `education`, `city`.

```python fig: The finished HR page, drawn from the real data: KPI cards, attrition by department, by satisfaction and overtime, and the leaver/stayer donut.
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
hr["left"] = (hr.attrition == "Yes").astype(int)
fig = plt.figure(figsize=(12, 6.6)); fig.patch.set_facecolor("#F4F2FA")
fig.text(.02, .95, "HR Attrition Overview", fontsize=16, weight="bold", color=dg.INK)
cards = [("Employees", f"{len(hr):,}"), ("Leavers", f"{hr.left.sum():,}"), ("Attrition %", f"{hr.left.mean():.1%}"), ("Avg monthly income", f"₹{hr.monthly_income.mean():,.0f}")]
for i, (l, v) in enumerate(cards):
    ax = fig.add_axes([.02 + i * .245, .78, .225, .12]); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.06", fc="white", ec="#E3DFF0")); ax.text(.07, .68, l, fontsize=9.5, color="#5F5A78"); ax.text(.07, .25, v, fontsize=17, weight="bold", color=dg.INK)
a1 = fig.add_axes([.07, .09, .26, .58]); d = hr.groupby("department").left.mean().sort_values() * 100
a1.barh(d.index, d.values, color=[dg.CORAL if v == d.max() else "#C9C3E6" for v in d.values]); a1.set_title("Attrition % by department", fontsize=10.5, loc="left")
for i, v in enumerate(d.values): a1.text(v + .3, i, f"{v:.1f}%", va="center", fontsize=8.5)
a2 = fig.add_axes([.42, .09, .24, .58]); s = hr.groupby("job_satisfaction").left.mean() * 100
a2.bar(s.index.astype(str), s.values, color=dg.VIO); a2.set_title("Attrition % by job satisfaction (1 = low)", fontsize=10.5, loc="left")
for i, v in enumerate(s.values): a2.text(i, v + .5, f"{v:.0f}%", ha="center", fontsize=8.5)
a3 = fig.add_axes([.73, .36, .24, .31]); o = hr.groupby("overtime").left.mean() * 100
a3.bar(["No overtime", "Overtime"], o.values, color=[dg.TEAL, dg.CORAL], width=.55); a3.set_title("Attrition % by overtime", fontsize=10.5, loc="left")
for i, v in enumerate(o.values): a3.text(i, v + .5, f"{v:.0f}%", ha="center", fontsize=8.5)
a4 = fig.add_axes([.74, .04, .22, .26]); a4.pie([hr.left.sum(), len(hr) - hr.left.sum()], colors=[dg.CORAL, "#C9C3E6"], wedgeprops=dict(width=.42), startangle=90, labels=["Left", "Stayed"], textprops=dict(fontsize=8.5)); a4.set_title("Leavers vs stayers", fontsize=10.5, loc="left")
fig
```

### Step 4: a calculated column with DAX

We want to see joining trends by year, but the table has only `hire_date`. Add a **calculated column**: Table view (or Modeling) → **New column**:

```dax
Hire Year = YEAR ( hr_employees[hire_date] )
```

A calculated column is evaluated **row by row when the data loads** and stored in the model, just like a new column in Excel. Now a line/column chart of **headcount by hire year** works:

```python run
hr["hire_year"] = hr.hire_date.dt.year
by_year = hr.groupby("hire_year").agg(hired=("emp_id", "count"), left=("left", "sum"))
by_year["attrition_%"] = (by_year.left / by_year.hired * 100).round(1)
by_year.tail(8)
```

### Step 5: data groups and bins

Groups combine values into custom categories, such as the "age band" below, without changing the source data:

- **Bins** (numbers): right-click the field → **New group** → Group type *Bin* → bin size 5 → creates `age (bins)`.
- **List groups** (text): select several values → right-click → **Group** → rename, for example group *Mumbai* and *Pune* as "Maharashtra".

For flexible logic, a calculated column is more transparent:

```dax
Age Band =
SWITCH (
    TRUE (),
    hr_employees[age] < 25, "Under 25",
    hr_employees[age] < 35, "25–34",
    hr_employees[age] < 45, "35–44",
    "45 and over"
)
```

```python run
bands = pd.cut(hr.age, [0, 24, 34, 44, 120], labels=["Under 25", "25–34", "35–44", "45 and over"])
hr.groupby(bands, observed=False).agg(employees=("emp_id", "count"), attrition_pct=("left", lambda s: round(s.mean() * 100, 1)))
```

### Step 6: small multiples

**Small multiples** split one visual into a grid of identical mini-charts by a field. Drag `department` into the visual's **Small multiples** well: you get one small column chart of attrition by satisfaction for every department. This lets you compare patterns across groups at a glance without a cluttered legend.

```python fig: Small multiples: attrition % by overtime for each department. The same pattern repeats everywhere, which says overtime is a company-wide issue, not a one-department issue.
depts = sorted(hr.department.unique())
fig, axs = plt.subplots(2, 3, figsize=(10, 4.4), sharey=True)
for ax, dpt in zip(axs.ravel(), depts):
    x = hr[hr.department == dpt].groupby("overtime").left.mean() * 100
    ax.bar(x.index, x.values, color=[dg.TEAL, dg.CORAL], width=.55); ax.set_title(dpt, fontsize=10)
    for i, v in enumerate(x.values): ax.text(i, v + 1, f"{v:.0f}%", ha="center", fontsize=8)
fig.suptitle("Attrition % with and without overtime, by department", fontsize=11.5, weight="bold"); fig.tight_layout()
fig
```

### What does the report tell us?

```python run
t = hr.groupby("overtime").left.agg(["count", "mean"]); t["mean"] = (t["mean"] * 100).round(1)
t.columns = ["employees", "attrition_%"]
print(t.to_string()); print()
low = hr[hr.job_satisfaction <= 2].left.mean() * 100; high = hr[hr.job_satisfaction >= 3].left.mean() * 100
print(f"Attrition for satisfaction 1–2: {low:.1f}%   vs   3–4: {high:.1f}%")
```

Insight sentences for a manager: *overtime workers leave far more often than others; low satisfaction scores go with higher attrition; Sales has the highest attrition among departments*. Notice the careful wording: these are **associations** in the data, not proof of cause. (The ML track shows how to test them properly.)

## Good habits from day one

1. **Name things clearly**: `Attrition %`, not `Measure 3`; rename pages ("HR Overview").
2. **Put measures in a dedicated table** later (Lesson 3) and format them (percentage, thousands separator).
3. **Check data types** in Power Query before loading.
4. **One idea per page**; the title should say the insight.
5. **Save often** (`.pbix`), and use clear version names.
6. **Do not use pie charts** with many slices; prefer bars (ranked) and use donuts only for 2–3 parts.

:::new Power BI in 2026
- **Copilot** can create a report page from a prompt ("Build an attrition overview for HR"), write DAX measures and summarise a page. It needs a paid Fabric/Premium capacity and your data to be well-modelled and named.
- **Power BI Project (PBIP)** format stores the report as text files, so teams can use **Git** and code review.
- **TMDL** (Tabular Model Definition Language) and **DAX query view** make models easier to script and test.
- **Direct Lake** (Fabric) reads Delta tables directly with import-like speed.
(See Lesson 6.)
:::

## Summary

:::key
- Power BI = Desktop (build) + Service (share) + Mobile (consume), now inside Microsoft Fabric.
- ETL: **Extract and Transform in Power Query, Load into the model**; analytics stages run from question to decision.
- Three views: **Report**, **Table**, **Model**; build with the Fields, Visualizations and Filters panes.
- A **card** shows a KPI; bar/column charts compare categories; a donut shows 2–3 parts; a matrix is a pivot table; slicers filter.
- A DAX **calculated column** (`YEAR`, `SWITCH`) is computed row by row at load time; **groups/bins** categorise without changing the data; **small multiples** repeat a chart per category.
:::

:::quiz
Q: In Power BI, where do you perform the Extract and Transform steps of ETL?
- Report view
* Power Query
- The Service
- The Model view
> Power Query connects to sources and transforms data; Close & Apply loads it into the model.

Q: Which view shows relationships between tables?
- Report view
- Table view
* Model view
- Filters pane
> Relationships are created and edited in Model view.

Q: Power BI Desktop is available for:
- Windows and Mac
* Windows only
- Mac only
- Browsers only
> Desktop is Windows-only; Mac users use the Service or a Windows virtual machine.

Q: What does a calculated column do?
- Runs only when a slicer changes
* Computes a value for every row when the data is loaded and stores it in the model
- Replaces a measure
- Changes the source file
> Calculated columns are row-by-row and stored; measures calculate on the fly.

Q: Which visual repeats the same chart for every value of a field?
- Matrix
- Slicer
* Small multiples
- Card
> Small multiples create a grid of mini-charts split by a category.

Q: Which licence do you need to share a report with colleagues who also have Pro licences?
- None, Desktop is enough
- Free Service licence
* Power BI Pro (or Premium Per User)
- Gateway licence
> Sharing in the Service requires Pro for creators and viewers (unless the workspace is on Premium/Fabric capacity).
:::

:::exercise Build the HR page
Build the page shown above in Power BI Desktop with `hr_employees.csv`. Then add: (1) a slicer for `city` and `gender`; (2) a matrix of attrition % by `job_title` and `education`; (3) an `Age Band` column and a column chart of attrition % by band; (4) a title text box that states your main finding.
???
(1) Slicer visual, fields `city`, `gender` (Format → Slicer settings → Style: Tile or Dropdown). (2) Matrix: Rows `job_title`, Columns `education`, Values `Attrition %` (turn on Cell elements → Background colour for a heat map). (3) Use the `SWITCH` formula in this lesson; chart X-axis `Age Band`, Y-axis `Attrition %`; sort the axis in the right order using a sort-by-column. (4) Insert → Text box, for example "Overtime is linked to about 15 more attrition points company-wide." Verify the claim against your visuals before you publish.
:::

:::interview Questions you may be asked
**Q: What is the difference between Power BI Desktop and Service?**
Desktop is the free authoring tool for models and reports on Windows; the Service is the cloud platform to publish, share, refresh on a schedule, build dashboards and apps, and apply security.

**Q: What is ETL and where is it done in Power BI?**
Extract, Transform, Load: Power Query connects to sources and applies transformation steps; the result is loaded into the VertiPaq in-memory model.

**Q: Calculated column vs measure?**
A calculated column is evaluated per row at refresh time and stored (uses memory); a measure is evaluated at query time in the current filter context (uses CPU). Use measures for aggregations such as sums and ratios.

**Q: Report vs dashboard?**
A report is multi-page and interactive, built on one model. A dashboard is a single page of pinned tiles from several reports, available only in the Service.
:::
