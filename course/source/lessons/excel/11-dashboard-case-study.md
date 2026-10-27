---
num: 11
title: "Interactive Dashboard: Superstore Case Study"
live: "Live classes 8–9"
updated: "Excel for Microsoft 365, 2026"
level: Intermediate–Advanced
duration: 150 min
summary: Build a complete, interactive sales dashboard from the Superstore data, from business questions and KPIs to pivot charts, slicers, a timeline, KPI cards and a dynamic title. Then protect it (sheet, workbook, allowed ranges), document it with comments and notes, and audit formulas with Evaluate Formula.
datasets: [superstore_sales.csv]
outcomes:
  - Turn a business brief into KPIs and questions before building anything
  - Prepare data, create one pivot per visual and connect them with slicers and a timeline
  - Build KPI cards and a dynamic title with GETPIVOTDATA and TEXT
  - Lay out a clean dashboard and apply design rules
  - Protect sheets and workbooks, use comments and notes, and audit formulas with Evaluate Formula
---

## The brief

:::case Superstore sales review
The Head of Sales wants a one-page Excel dashboard to review performance for 2023–2025. They want to see, at a glance: total sales, profit, profit margin and orders; how sales are trending; which regions, categories and sub-categories perform best and worst; and the effect of discounts on profit. They want to filter by year, region and segment. The dashboard will be emailed every month, so it must be protected against accidental changes.
:::

### Step 0: questions and KPIs first

| KPI / question | Calculation | Visual |
|---|---|---|
| Total sales | Sum of sales | KPI card |
| Total profit and margin | Sum of profit; profit ÷ sales | KPI cards |
| Number of orders | Distinct count of order_id | KPI card |
| Sales trend | Sales by month | Line chart |
| Regional performance | Sales and profit by region | Bar chart |
| Product mix | Sales by category and sub-category | Bar chart / treemap |
| Discount impact | Profit by discount level | Column chart |
| Filters | Year, Region, Segment | Timeline + slicers |

Agreeing on this table before building saves hours of rework. It is also your "requirements document" in interviews.

Here is the finished result we are aiming for (drawn from the real data):

```python fig: The finished Superstore dashboard: KPI cards on top, trend and breakdown charts below, slicers on the left.
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
s = pd.read_csv("superstore_sales.csv", parse_dates=["order_date"])
fig = plt.figure(figsize=(12, 7.2)); fig.patch.set_facecolor("#F4F2FA")
fig.text(.02, .955, "Superstore Sales Dashboard · 2023–2025 · All regions", fontsize=15, weight="bold", color=dg.INK)
# slicer panel
ax0 = fig.add_axes([.015, .05, .13, .84]); ax0.axis("off"); ax0.set_xlim(0, 1); ax0.set_ylim(0, 1)
for title, items, y0 in [("Year", ["2023", "2024", "2025"], .97), ("Region", ["East", "North", "South", "West"], .66), ("Segment", ["Consumer", "Corporate", "Home Office"], .27)]:
    ax0.text(.05, y0, title, weight="bold", fontsize=10, color=dg.INK)
    for i, it in enumerate(items):
        ax0.add_patch(FancyBboxPatch((.05, y0 - .085 - i * .07), .9, .055, boxstyle="round,pad=0.005,rounding_size=0.01", fc=dg.VIO, ec=dg.VIO)); ax0.text(.5, y0 - .058 - i * .07, it, ha="center", va="center", color="white", fontsize=8.5)
tot_s, tot_p, n_o = s.sales.sum(), s.profit.sum(), s.order_id.nunique()
cards = [("Total sales", f"₹{tot_s / 1e7:,.2f} Cr"), ("Total profit", f"₹{tot_p / 1e7:,.2f} Cr"), ("Profit margin", f"{tot_p / tot_s:.1%}"), ("Orders", f"{n_o:,}")]
for i, (lab, val) in enumerate(cards):
    ax = fig.add_axes([.165 + i * .205, .78, .19, .135]); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.0,rounding_size=0.06", fc="white", ec="#E3DFF0"))
    ax.text(.08, .7, lab, fontsize=9.5, color="#5F5A78"); ax.text(.08, .3, val, fontsize=17, weight="bold", color=dg.INK)
ax1 = fig.add_axes([.19, .44, .46, .28]); m = s.set_index("order_date").resample("MS").sales.sum() / 1e5
ax1.plot(m.index, m.values, color=dg.VIO, lw=2); ax1.fill_between(m.index, m.values, color=dg.VIO, alpha=.08); ax1.set_title("Monthly sales (₹ lakh)", fontsize=10.5, loc="left")
ax2 = fig.add_axes([.71, .44, .27, .28]); r = s.groupby("region")[["sales", "profit"]].sum() / 1e5
ax2.barh(r.index, r.sales, color="#C9C3E6", label="Sales"); ax2.barh(r.index, r.profit, color=dg.VIO, label="Profit"); ax2.set_title("Region (₹ lakh)", fontsize=10.5, loc="left"); ax2.legend(fontsize=8)
ax3 = fig.add_axes([.19, .07, .46, .28]); sc = s.groupby("sub_category").sales.sum().sort_values() / 1e5
ax3.barh(sc.index, sc.values, color=[dg.VIO if v > sc.quantile(.75) else "#C9C3E6" for v in sc.values]); ax3.set_title("Sales by sub-category (₹ lakh)", fontsize=10.5, loc="left"); ax3.tick_params(labelsize=8)
ax4 = fig.add_axes([.71, .07, .27, .28]); d = s.groupby("discount").profit.sum() / 1e5
ax4.bar([f"{x:.0%}" for x in d.index], d.values, color=[dg.TEAL if v > 0 else dg.CORAL for v in d.values]); ax4.axhline(0, color="#777", lw=.8); ax4.set_title("Profit by discount (₹ lakh)", fontsize=10.5, loc="left"); ax4.tick_params(labelsize=8)
fig
```

## Step 1: prepare the data

1. Import `superstore_sales.csv` with **Data → From Text/CSV** (Power Query, Lesson 12), or open it and convert the range to a Table named `tblSales` (`Ctrl + T`).
2. Add helper columns that the pivots will need:

| Column | Formula (structured reference) | Why |
|---|---|---|
| `year` | `=YEAR([@order_date])` | Year slicer (or use a Timeline) |
| `month` | `=TEXT([@order_date],"mmm")` | Labels |
| `margin` | `=[@profit]/[@sales]` | Row-level margin for analysis |
| `discount_band` | `=IFS([@discount]=0,"0%",[@discount]<=0.2,"1–20%",TRUE,">20%")` | Simpler grouping |
| `days_to_ship` | `=[@ship_date]-[@order_date]` | Operations KPI |

3. Check data quality: blanks (`COUNTBLANK`), duplicates of `row_id`, negative quantities, dates outside 2023–2025.

```python run
s.describe(include="all").T[["count", "unique", "min", "max"]].head(12)
```

## Step 2: one pivot table per visual

Create a sheet called **Calc** (it will be hidden later). Insert one pivot table for each chart, all from `tblSales` so they share **one pivot cache**:

| Pivot | Rows | Values | Notes |
|---|---|---|---|
| P1 KPIs | (none) | Sum of sales, Sum of profit, Distinct count of order_id | Tick "Add this data to the Data Model" to get Distinct Count |
| P2 Trend | order_date grouped by Years + Months | Sum of sales | Line chart |
| P3 Region | region | Sum of sales, Sum of profit | Bar chart |
| P4 Sub-category | sub_category | Sum of sales (sorted) | Bar chart |
| P5 Discount | discount | Sum of profit | Column chart |

Give each pivot a meaningful name (PivotTable Analyze → PivotTable Name: `ptTrend`, `ptRegion` …). Names make GETPIVOTDATA formulas and maintenance easier.

## Step 3: pivot charts

Click each pivot → PivotTable Analyze → **PivotChart** → choose the type → cut and paste the chart onto a sheet called **Dashboard**.

Clean each chart:

- Right-click the field buttons → **Hide All Field Buttons on Chart**.
- Delete gridlines and legends that are not needed; add data labels where there are few bars.
- Apply the same font and a two-colour palette (one highlight, one neutral).
- Write insight titles, for example "Technology drives most sales" or "Discounts above 20% destroy profit".

## Step 4: slicers and a timeline that control everything

1. Select any pivot → PivotTable Analyze → **Insert Slicer** → tick `region` and `segment`.
2. **Insert Timeline** → `order_date` → switch the timeline to **YEARS**.
3. Right-click each slicer → **Report Connections** → tick **all five** pivots. Now one click filters every chart and KPI.
4. Format slicers: Slicer tab → Columns = 1 or 2, a matching style, size them to align with the grid.

:::warn Report Connections are greyed out?
Slicers can only connect pivots that share the same pivot cache (or the same Data Model). If you built a pivot from a different range, rebuild it from `tblSales`.
:::

## Step 5: KPI cards and a dynamic title

KPI cards are simply cells or shapes linked to the KPI pivot. `GETPIVOTDATA` keeps returning the right number even when slicers change the pivot.

```xl title="Calc sheet: KPI formulas (values shown for the unfiltered data)"
KPI{h}|Formula{h}|Value{h}
Total sales|'=GETPIVOTDATA("Sum of sales",Calc!$A$3)|201413569{;#,##0}
Total profit|'=GETPIVOTDATA("Sum of profit",Calc!$A$3)|18352164{;#,##0}
Profit margin|'=C3/C2|=C3/C2{;0.0%}
Orders|'=GETPIVOTDATA("Distinct Count of order_id",Calc!$A$3)|3200{;#,##0}
Sales label|'="₹"&TEXT(C2/10^7,"0.00")&" Cr"|="₹"&TEXT(C2/10^7,"0.00")&" Cr"
```

Let's verify these numbers with pandas:

```python run
print(f"Sales  : {s.sales.sum():,.0f}")
print(f"Profit : {s.profit.sum():,.0f}")
print(f"Margin : {s.profit.sum() / s.sales.sum():.1%}")
print(f"Orders : {s.order_id.nunique():,}")
```

To show a KPI card on the dashboard: Insert → Shapes → Rounded Rectangle, click the shape, type `=Calc!C6` in the **formula bar**, and press Enter. The shape now displays the live value.

**Dynamic title**: build the title text in a cell and link a text box to it:

```excel
="Superstore Sales Dashboard · " & TEXTJOIN(", ", TRUE, Calc!H2:H5)
```

where `H2:H5` is a small pivot with `region` in Rows that is also connected to the slicers, so it lists only the selected regions.

## Step 6: layout and design rules

```python fig: A simple dashboard grid. Most important information top-left; filters on one side; consistent spacing.
dg.layers([("Row 1", "Title · data date · 4 KPI cards (sales, profit, margin, orders)"), ("Row 2", "Trend over time (wide) · regional comparison"),
           ("Row 3", "Product breakdown · discount impact"), ("Side panel", "Timeline (years) · Region slicer · Segment slicer · notes")], title="Dashboard layout")
```

1. **Z-pattern**: people read top-left first: put the headline KPIs there.
2. **Align to the grid**: hold `Alt` while dragging or resizing a chart to snap it to cell borders; set every chart to the same height.
3. **Limit colours**: one brand colour, one highlight, red only for bad news.
4. **Remove clutter**: View → untick Gridlines and Headings; hide the Calc sheet (right-click tab → Hide).
5. **Label the date and the source**: "Data: Superstore orders, Jan 2023 – Dec 2025. Refreshed 05-Jan-2026."
6. **Test it**: click every slicer combination; check that totals match the raw data.

## Step 7: protect the dashboard

| Protection | Where | What it does |
|---|---|---|
| **Lock / unlock cells** | `Ctrl + 1` → Protection → Locked | All cells are locked by default; **unlock** the input cells users may change. Locking only takes effect when the sheet is protected |
| **Hide formulas** | `Ctrl + 1` → Protection → Hidden | Formula bar shows nothing for those cells once the sheet is protected |
| **Protect Sheet** | Review → Protect Sheet | Prevents editing locked cells; tick what users may still do: **Use PivotTable & PivotChart**, **Edit objects** (needed for slicers), sort, filter, format |
| **Allow Edit Ranges** | Review → Allow Edit Ranges | Lets specific ranges be edited, optionally with their own password |
| **Protect Workbook** | Review → Protect Workbook | Protects the **structure**: no adding, deleting, renaming, moving or unhiding sheets |
| **Encrypt with password** | File → Info → Protect Workbook → Encrypt | Password needed to **open** the file |
| **Mark as Final** | File → Info → Protect Workbook | A read-only hint (not security) |

:::steps Protect so slicers still work
1. Unlock any cells users need to type in (for example a target input).
2. Review → **Protect Sheet** → tick "Select unlocked cells", "Use PivotTable & PivotChart" and "Edit objects" → set a password.
3. Review → **Protect Workbook** (structure) so the hidden Calc sheet cannot be unhidden.
4. Test with a colleague before emailing.
:::

:::warn Sheet protection is not strong security
Sheet and structure passwords stop accidents, not determined users. Never rely on them to protect confidential data: use file encryption, SharePoint permissions or share only what is needed (for example a PDF export).
:::

## Comments and notes

| Feature | Insert | Use |
|---|---|---|
| **Note** (old "comment") | Review → Notes → New Note (`Shift + F2`) | A sticky note explaining a cell: "Target approved by CFO on 12-Jan" |
| **Comment** (threaded) | Review → New Comment (`Ctrl + Alt + M`) | A conversation: @mention a colleague, reply, resolve |

Notes are best for permanent documentation; comments for review discussions. Add a small **"How to use"** note on the dashboard explaining the slicers and data date.

## Auditing formulas: Evaluate Formula and friends

When a KPI looks wrong, use **Formulas → Formula Auditing**:

| Tool | What it shows |
|---|---|
| **Evaluate Formula** | Steps through a formula one calculation at a time: press Evaluate to see each part replaced by its value |
| **Trace Precedents / Dependents** | Arrows to the cells a formula uses, or that use it |
| **Show Formulas** (`` Ctrl + ` ``) | Every formula instead of its result |
| **Error Checking** | Walks through cells with errors and suggests fixes |
| **Watch Window** | Keeps an eye on key cells while you work elsewhere |
| `F9` inside the formula bar | Select part of a formula and press F9 to see its value (press Esc to undo) |

```python fig: Evaluate Formula replaces one part at a time until only the result remains.
dg.vflow(['=IF(C3/C2>0.1,"Healthy","Review")', '=IF(18352164/201413569>0.1,"Healthy","Review")', '=IF(0.0911>0.1,"Healthy","Review")', '=IF(FALSE,"Healthy","Review")', '"Review"'],
         title="Evaluate Formula, step by step", width=7.8)
```

## Delivering the dashboard

- **Refresh**: Data → Refresh All before sending.
- **Export**: File → Export → PDF (select the Dashboard sheet, landscape, fit to one page) for people who only need to read it.
- **Share live**: save to OneDrive/SharePoint and share a link; viewers can use slicers in Excel for the web.
- **Automate**: Power Query + Refresh All, or Office Scripts / Power Automate to refresh and email on a schedule.

:::ai Do it with AI
Copilot in Excel can draft the analysis: *"Summarise sales and profit by region and category, identify the three biggest loss-making sub-categories, and suggest charts for a dashboard."* Use its suggestions as a starting point, then build the final dashboard deliberately: you are responsible for every number on it.
:::

## Insights from the case

```python run
sub = s.groupby("sub_category")[["sales", "profit"]].sum()
sub["margin"] = (sub.profit / sub.sales * 100).round(1)
print("Loss-making sub-categories:\n", sub[sub.profit < 0].round(0).to_string())
disc = s.groupby(pd.cut(s.discount, [-0.01, 0, 0.2, 1], labels=["0%", "1–20%", ">20%"]), observed=False)[["sales", "profit"]].sum()
disc["margin %"] = (disc.profit / disc.sales * 100).round(1)
print("\nMargin by discount band:\n", disc.round(0).to_string())
```

A good dashboard closes with 3–4 written insights, for example:

1. Technology generates about three quarters of sales and most of the profit; furniture is unprofitable overall.
2. Tables and Bookcases lose money; both are heavily discounted.
3. Order lines with discounts above 20% lose money almost every time: review the discount policy.
4. Sales peak every October–December (festive season); plan stock and staffing accordingly.

## Summary

:::key
- Start with the brief, KPIs and questions; then data prep; then one pivot per visual.
- Build all pivots from one Table so they share a cache and can be connected to slicers and a timeline (Report Connections).
- KPI cards use GETPIVOTDATA; shapes can display a cell's value by typing `=Cell` in the formula bar.
- Design: top-left headline KPIs, aligned grid, few colours, insight titles, data date and source.
- Protect: unlock inputs, Protect Sheet (allow PivotTables and objects), Protect Workbook structure; use encryption for real security.
- Audit with Evaluate Formula, Trace Precedents/Dependents, Show Formulas and the Watch Window.
:::

:::quiz
Q: Why should all dashboard pivots be built from the same Table?
- It makes the file smaller only
* So they share one pivot cache and can all be connected to the same slicers
- Pivot charts require it
- It is needed for conditional formatting
> Slicers can only control pivots that share a cache (or data model).

Q: After protecting the sheet, slicers stop working. What did you forget?
- To unlock the slicer cells
* To allow "Use PivotTable & PivotChart" and "Edit objects" in Protect Sheet
- To protect the workbook structure
- To refresh the pivots
> Slicers are objects that change pivots, so both permissions must be allowed.

Q: Which tool lets you see each step of a complex formula's calculation?
- Trace Dependents
* Evaluate Formula
- Watch Window
- Name Manager
> Evaluate Formula replaces one part at a time with its value.

Q: What does Protect Workbook (structure) prevent?
- Opening the file without a password
- Editing any cell
* Adding, deleting, renaming, moving, hiding or unhiding sheets
- Using slicers
> Structure protection guards the sheets, not the cells.

Q: How do you count distinct orders in a pivot table?
- Count of order_id
* Add the data to the Data Model and use Distinct Count
- Sum of order_id
- Use a calculated field
> Distinct Count is available only for Data Model pivots.

Q: What is the difference between a note and a comment in Microsoft 365?
* Notes are simple sticky notes; comments are threaded conversations with replies and mentions
- They are identical
- Comments cannot be printed
- Notes can only be added to formulas
> Use notes for documentation and comments for review discussions.
:::

:::exercise Build it yourself
Build the dashboard in this lesson from `superstore_sales.csv`. Then add: (1) a **Ship mode** slicer; (2) a KPI card for **average days to ship**; (3) a chart of the top 10 customers by sales that responds to all slicers; (4) sheet protection that still allows slicers.
???
(1) Insert Slicer → ship_mode → Report Connections → all pivots.
(2) Add `days_to_ship` to tblSales; add Average of days_to_ship to the KPI pivot; link a shape to its GETPIVOTDATA cell.
(3) New pivot from tblSales: Rows customer_name, Values Sum of sales, Value Filter Top 10; PivotChart (bar); connect to the slicers.
(4) Review → Protect Sheet with "Use PivotTable & PivotChart" and "Edit objects" ticked; protect workbook structure.
:::

:::interview Questions you may be asked
**Q: Walk me through how you would build an Excel dashboard.**
Clarify the audience and questions; define KPIs; clean and structure the data as a Table; create one pivot per visual; build pivot charts; connect slicers and a timeline; add KPI cards with GETPIVOTDATA; design the layout; validate numbers against the source; protect and share.

**Q: How do you make sure dashboard numbers are correct?**
Reconcile totals with the raw data (SUM vs pivot), test filters, check distinct counts, use Evaluate Formula and trace precedents for KPI formulas, and have a second person review.

**Q: Excel dashboard or Power BI?**
Excel for small data, quick turnaround and audiences who live in Excel; Power BI for larger data, many users, scheduled refresh, row-level security and richer interactivity.
:::
