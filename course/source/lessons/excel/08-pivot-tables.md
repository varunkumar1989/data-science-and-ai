---
num: 8
title: Pivot Tables from Basic to Advanced
live: "Live classes 5–7"
updated: "Excel for Microsoft 365, 2026"
level: Intermediate
duration: 150 min
summary: Summarise thousands of rows in seconds. Build pivot tables, understand the pivot cache and the four areas, change value field settings, show values as % of total, MoM and YoY change and running totals, group dates and numbers into bins, add calculated fields, slicers and timelines, and solve the Video Game Sales case study.
datasets: [superstore_sales.csv, video_game_sales.csv]
outcomes:
  - Build a pivot table and explain the pivot cache, the four areas and Refresh vs Refresh All
  - Change the summary function and number format, and show values as % of total, % of row and running totals
  - Calculate month-on-month (MoM) and year-on-year (YoY) change
  - Group dates by year, quarter and month, group items manually, and group numbers into bins
  - Add calculated fields, slicers, timelines and pivot charts, and answer a full case study
---

## What a pivot table does

A pivot table **groups** rows by one or more fields and **summarises** a number for each group (sum, count, average…). It is the fastest way to answer "how much, by what?" questions, with no formulas.

```python fig: A pivot table turns thousands of order lines into a compact summary: rows grouped by Region, columns by Category, values summed.
import pandas as pd, matplotlib.pyplot as plt
s = pd.read_csv("superstore_sales.csv")
pv = s.pivot_table(index="region", columns="category", values="sales", aggfunc="sum") / 1e5
fig, axs = plt.subplots(1, 2, figsize=(11, 3.6), gridspec_kw={"width_ratios": [1.1, 1]})
raw = s[["order_id", "region", "category", "sales"]].head(9)
axs[0].axis("off"); axs[0].set_title(f"Raw data: {len(s):,} rows", fontsize=11)
t = axs[0].table(cellText=raw.values, colLabels=raw.columns, loc="center", cellLoc="left"); t.auto_set_font_size(False); t.set_fontsize(8); t.scale(1, 1.25)
axs[1].axis("off"); axs[1].set_title("Pivot: sum of sales (₹ lakh)", fontsize=11)
cells = [[r] + [f"{v:,.1f}" for v in pv.loc[r]] + [f"{pv.loc[r].sum():,.1f}"] for r in pv.index] + [["Grand Total"] + [f"{v:,.1f}" for v in pv.sum()] + [f"{pv.values.sum():,.1f}"]]
t2 = axs[1].table(cellText=cells, colLabels=["Region"] + list(pv.columns) + ["Total"], loc="center", cellLoc="right"); t2.auto_set_font_size(False); t2.set_fontsize(9); t2.scale(1, 1.6)
for (r, c), cell in t2.get_celld().items():
    if r == 0: cell.set_facecolor("#E6E0FF")
    if r == len(cells): cell.set_text_props(weight="bold")
fig
```

## Creating a pivot table

:::steps Step by step
1. Make sure the data is **structured** (Lesson 1): one header row, no blank rows, no merged cells. Ideally convert it to a Table (`Ctrl + T`) so new rows are included automatically.
2. Click any cell in the data → **Insert → PivotTable** (or `Alt, N, V`).
3. Choose **New Worksheet** → OK. An empty pivot appears with the **PivotTable Fields** pane on the right.
4. Drag fields into the four areas: drag `region` to **Rows**, `category` to **Columns**, `sales` to **Values**.
5. Right-click any number → **Number Format** → `#,##0` so the format sticks when the pivot refreshes.
:::

```python fig: The PivotTable Fields pane: a list of fields at the top, four areas at the bottom.
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(8.6, 4.4)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 5.2)
ax.add_patch(FancyBboxPatch((.2, .2), 9.6, 4.8, boxstyle="round,pad=0.02,rounding_size=0.08", fc="white", ec="#BFBFBF"))
ax.text(.45, 4.7, "PivotTable Fields", weight="bold", fontsize=11)
for i, f in enumerate(["☐ order_date", "☑ region", "☑ category", "☐ segment", "☐ sub_category", "☑ sales", "☐ profit"]):
    ax.text(.55, 4.3 - i * .3, f, fontsize=9.5, family="DejaVu Sans")
areas = [("Filters", ["segment"], 5.0, 2.55), ("Columns", ["category"], 7.45, 2.55), ("Rows", ["region"], 5.0, .35), ("Σ Values", ["Sum of sales"], 7.45, .35)]
for name, items, x, y in areas:
    ax.add_patch(FancyBboxPatch((x, y), 2.25, 2.0, boxstyle="round,pad=0.02,rounding_size=0.06", fc="#F7F5FF", ec=dg.VIO))
    ax.text(x + .12, y + 1.75, name, weight="bold", color=dg.VIO, fontsize=10)
    for j, it in enumerate(items):
        ax.add_patch(FancyBboxPatch((x + .12, y + 1.15 - j * .45), 2.0, .38, boxstyle="round,pad=0.01,rounding_size=0.04", fc="white", ec="#BBB")); ax.text(x + .22, y + 1.34 - j * .45, it, fontsize=9.3, va="center")
ax.text(.45, 1.6, "Drag fields between\nthe four areas →", fontsize=10, color="#555")
fig
```

| Area | What it does | Example |
|---|---|---|
| **Rows** | One row per unique value | Region, Category, Order Date |
| **Columns** | One column per unique value | Year, Segment |
| **Values** | The numbers being summarised | Sum of Sales, Count of Order ID |
| **Filters** | Filter the whole pivot by a field | Segment = Corporate |

## The pivot cache, Refresh and Refresh All

A pivot table does not read your sheet directly. When you create it, Excel copies the data into a hidden **pivot cache**, and the pivot reads from that cache. This is why pivots are fast, and also why they do **not** update automatically when the data changes.

```python fig: Every pivot reads from a cache. Pivots made from the same data share one cache.
dg.flow(["Source data (sheet or Table)", "Pivot cache (hidden copy)", "Pivot 1 · Pivot 2 · Pivot chart"], subs=["You edit this", "Updated only on Refresh", "Read from the cache"], colors=[dg.SKY, dg.GOLD, dg.VIO])
```

| Action | Shortcut | Effect |
|---|---|---|
| **Refresh** | `Alt + F5` | Re-reads the source into this pivot's cache. Every pivot that **shares the same cache** updates too |
| **Refresh All** | `Ctrl + Alt + F5` | Refreshes every pivot cache, query and data connection in the workbook |
| **Change Data Source** | PivotTable Analyze tab | Point the pivot to a bigger range (unnecessary if the source is a Table) |
| **Refresh on open** | PivotTable Options → Data | Refreshes automatically when the file opens |

:::tip Use a Table as the source
If the source is a Table, new rows are included the next time you refresh. If the source is a fixed range like `A1:R6324`, new rows below are ignored until you change the data source.
:::

## Value field settings

Click a field in Values → **Value Field Settings** (or right-click a number).

### Summarize values by

Sum, Count, Average, Max, Min, Product, Count Numbers, StdDev, Var. Text fields in Values are counted automatically. **Distinct Count** appears only when the pivot is added to the **Data Model** (tick "Add this data to the Data Model" when creating it; Lesson 12).

### Show values as

This tab turns a plain sum into an analytical view without writing formulas.

| Show values as | Answers | Example |
|---|---|---|
| % of Grand Total | What share of the whole? | Furniture = 22% of all sales |
| % of Column Total | Share within each column | Within 2025, North = 31% |
| % of Row Total | Mix within each row | In the West, 46% of sales are Technology |
| % of Parent Row Total | Share within a parent group | Each sub-category's share of its category |
| Difference From (previous) | Change from the previous item | MoM or YoY change in ₹ |
| % Difference From (previous) | Growth rate | MoM % or YoY % |
| Running Total In | Cumulative total | Year-to-date sales |
| Rank Largest to Smallest | Position | Top-selling region = 1 |
| Index | Relative importance | Above 1 = over-represented |

Here are three of these views on the Superstore data (computed with pandas to show the exact numbers a pivot would give):

```python run
import pandas as pd
s = pd.read_csv("superstore_sales.csv", parse_dates=["order_date"])
pv = s.pivot_table(index="region", columns="category", values="sales", aggfunc="sum")
pct_total = (pv / pv.values.sum() * 100).round(1)
pct_row = (pv.div(pv.sum(axis=1), axis=0) * 100).round(1)
print("Sum of sales (₹):"); print(pv.round(0).astype(int).to_string())
print("\n% of grand total:"); print(pct_total.to_string())
print("\n% of row total (category mix inside each region):"); print(pct_row.to_string())
```

## MoM and YoY

**Month-on-month (MoM)** compares each month with the previous month; **year-on-year (YoY)** compares a period with the same period last year (which removes seasonality, such as the festive Q4 peak).

:::steps MoM % in a pivot
1. Put `order_date` in Rows and group it by **Years** and **Months** (see Grouping below).
2. Add `sales` to Values **twice**.
3. On the second copy: Value Field Settings → Show Values As → **% Difference From** → Base field: `order_date` (Months) → Base item: **(previous)**.
4. Rename the field "MoM %".
:::

```python run
m = s.set_index("order_date").resample("MS")["sales"].sum().to_frame("sales")
m["MoM %"] = (m.sales.pct_change() * 100).round(1)
m["YoY %"] = (m.sales.pct_change(12) * 100).round(1)
m.index = m.index.strftime("%b-%Y")
m.tail(8)
```

```python fig: Monthly sales with YoY growth. The festive season (Oct–Dec) peaks every year, so YoY is a fairer comparison than MoM.
import matplotlib.pyplot as plt
ms = s.set_index("order_date").resample("MS")["sales"].sum() / 1e5
fig, ax = plt.subplots(figsize=(10, 3.8))
for y, c in zip([2023, 2024, 2025], [dg.SKY, dg.TEAL, dg.VIO]):
    d = ms[ms.index.year == y]; ax.plot(d.index.month, d.values, marker="o", color=c, label=str(y), lw=2)
ax.set_xticks(range(1, 13)); ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
ax.set_ylabel("Sales (₹ lakh)"); ax.set_title("Monthly sales by year"); ax.legend(ncol=3)
fig
```

In formulas, the same calculations are: MoM % `=(C3-C2)/C2`, YoY % `=(C14-C2)/C2` when months are listed one per row.

## Grouping

### Group dates

Right-click a date in Rows → **Group** → choose Years, Quarters, Months (and Days, Hours if needed). Excel 365 groups dates automatically when you drag a date field to Rows; you can ungroup with right-click → Ungroup.

:::tip Indian financial year
Pivot grouping uses calendar quarters (Jan–Mar = Q1). For an April–March financial year, add helper columns to the data first: `FY = YEAR(date)+(MONTH(date)>=4)` and `FQ = "Q"&ROUNDUP(MOD(MONTH(date)-4,12)+1)/3,0)`, or use `CHOOSE` (Lesson 7), and put those in the pivot.
:::

### Group items manually

Select several labels (hold `Ctrl`) → right-click → **Group**. Excel creates a new field such as `Product2` with a group called `Group1`; rename it (for example "Low Sales Products"). This is how you combine the three lowest-selling products into one line, or merge small cities into "Others".

### Groups vs bins

| | Groups | Bins |
|---|---|---|
| What | Segregate items into chunks based on a common behaviour or criteria | Split a **numeric** field into equal-width intervals |
| Size | Can be any size | Every bin has the same width |
| Works on | Text, dates and numbers | Numbers |
| Example | "Metro" vs "Non-metro" cities | Order value 0–5,000, 5,000–10,000 … |

To bin numbers: put the number field (for example `sales`) in **Rows** → right-click → Group → Starting at 0, Ending at 50,000, By 5,000. Then put `order_id` in Values as a Count.

```python run
bins = pd.cut(s.sales, range(0, 55000, 5000), right=False)
dist = s.groupby(bins, observed=False).size().to_frame("Count of order lines")
dist.index = [f"{int(i.left):,}–{int(i.right - 1):,}" for i in dist.index]
dist
```

Most order lines are small; a few very large ones (machines, copiers) form the long tail. This is a frequency distribution, the pivot-table version of a histogram (Lesson 10).

## Layout, subtotals and grand totals

The **Design** tab controls how the pivot looks:

| Setting | Options | Tip |
|---|---|---|
| **Report Layout** | Compact (default), Outline, **Tabular** | Tabular + **Repeat All Item Labels** gives a flat table you can copy and reuse |
| **Subtotals** | Don't show, at bottom, at top | Turn off for exports |
| **Grand Totals** | On for rows/columns, off | Off when sharing a percentage view |
| **Blank Rows** | Insert after each item | Easier to read printed reports |
| **Expand / Collapse** | `+`/`−` buttons, or right-click → Expand/Collapse entire field | Drill from Category down to Sub-category |
| **Show Details** | Double-click any number | Opens a new sheet with the rows behind that number: great for auditing |

**Parent total**: when two fields are in Rows (Category → Sub-category), "% of Parent Row Total" shows each sub-category's share of its own category.

## Sorting and filtering inside a pivot

- **Sort**: right-click a value → Sort → Largest to Smallest.
- **Label filter**: Row Labels drop-down → Label Filters → Begins with, contains …
- **Value filter / Top 10**: Row Labels drop-down → Value Filters → **Top 10** → change to Top 5 Items by Sum of sales. This is how you answer "Find the top 5 categories".
- **Slicers**: PivotTable Analyze → **Insert Slicer** → pick fields (Region, Segment). Slicers are clickable buttons that filter the pivot and show what is selected. Right-click a slicer → **Report Connections** to control several pivots with one slicer (they must share the same cache).
- **Timeline**: Insert Timeline on a date field to filter by years, quarters, months or days with a slider.

## Calculated fields

A **calculated field** creates a new value field from other fields in the pivot: PivotTable Analyze → Fields, Items & Sets → **Calculated Field**.

Example: `Profit Margin = profit / sales`, formatted as a percentage.

:::warn Calculated fields work on totals
Excel calculates the field on the **sums**: Profit Margin for the North = total North profit ÷ total North sales. That is correct for ratios. But a calculated field like `=quantity * price` would multiply the *sum* of quantity by the *sum* of price, which is wrong. Add such row-level calculations as a new column in the source data instead.
:::

```python run
pm = s.groupby("category")[["sales", "profit"]].sum()
pm["Profit Margin"] = (pm.profit / pm.sales * 100).round(1).astype(str) + "%"
pm.round(0)
```

## GETPIVOTDATA and pivot charts

When you type `=` and click a cell inside a pivot, Excel writes `GETPIVOTDATA`, for example `=GETPIVOTDATA("sales",$A$3,"region","North")`. It keeps returning North's sales even if the pivot layout changes. Turn it off in PivotTable Analyze → Options → Generate GetPivotData if you prefer normal references.

**PivotChart** (PivotTable Analyze → PivotChart) creates a chart linked to the pivot: filtering the pivot or clicking a slicer updates the chart. This is the basis of the dashboard in Lesson 11.

## Case study: Video Game Sales (regional sales trends)

You are an analyst at a game publisher. The file `video_game_sales.csv` has 2,400 fictional titles with platform, release year, genre, publisher and sales in millions of units by region: North America (`na_sales`), Europe (`eu_sales`), Japan (`jp_sales`), other regions and global. Answer the questions with pivot tables. The answers below were computed from the file so you can check your pivots.

```python run
g = pd.read_csv("video_game_sales.csv")
print(g.shape); g.head(4)
```

:::case Q1. Which genres sell the most worldwide?
Pivot: Rows = genre, Values = Sum of global_sales, sorted largest to smallest.
:::

```python run
q1 = g.pivot_table(index="genre", values="global_sales", aggfunc="sum").sort_values("global_sales", ascending=False)
q1["% of total"] = (q1.global_sales / q1.global_sales.sum() * 100).round(1)
q1.round(1).head(6)
```

:::case Q2. Who are the top 5 publishers, and how many titles did each release?
Pivot: Rows = publisher, Values = Sum of global_sales and Count of name; Value Filter → Top 5 by global sales.
:::

```python run
q2 = g.groupby("publisher").agg(global_sales=("global_sales", "sum"), titles=("name", "count")).sort_values("global_sales", ascending=False).head(5)
q2["sales per title"] = (q2.global_sales / q2.titles).round(2)
q2.round(1)
```

:::case Q3. How does regional preference differ by genre?
Pivot: Rows = genre, Values = Sum of na_sales, eu_sales, jp_sales, other_sales; Show Values As → **% of Row Total**.
:::

```python run
reg = ["na_sales", "eu_sales", "jp_sales", "other_sales"]
q3 = g.groupby("genre")[reg].sum()
q3 = (q3.div(q3.sum(axis=1), axis=0) * 100).round(1).sort_values("jp_sales", ascending=False)
q3.head(6)
```

```python fig: Regional mix by genre (% of each genre's sales). Role-Playing and Puzzle games lean much more on Japan than Shooter or Sports titles do.
import matplotlib.pyplot as plt
ax = q3.sort_values("jp_sales").plot.barh(stacked=True, figsize=(9.5, 4.6), color=[dg.VIO, dg.TEAL, dg.CORAL, dg.GOLD], width=.75)
ax.set_xlabel("% of genre sales"); ax.legend(["North America", "Europe", "Japan", "Other"], ncol=4, loc="upper center", bbox_to_anchor=(.5, 1.12)); ax.set_xlim(0, 100)
```

:::case Q4. How have sales changed over the years?
Pivot: Rows = year, Values = Sum of global_sales, plus a second copy shown as % Difference From (previous) for YoY growth. Insert a PivotChart (line).
:::

```python run
q4 = g.pivot_table(index="year", values="global_sales", aggfunc="sum")
q4["YoY %"] = (q4.global_sales.pct_change() * 100).round(1)
q4.round(1).tail(8)
```

:::case Q5. Which platform leads in each region?
Pivot: Rows = platform, Values = the four regional sales columns; sort each column, or use conditional formatting → Top 1 per column.
:::

```python run
q5 = g.groupby("platform")[reg].sum().round(1)
q5.loc["Leader"] = q5.idxmax()
q5
```

:::key Insights to present
Write 3–5 sentences of insight, not just tables. For example: which genres to prioritise for the Japanese market, which publishers are efficient (high sales per title), and how platform transitions show in the year trend. Keep every number traceable to a pivot.
:::

## Summary

:::key
- Pivot tables summarise structured data by dragging fields into **Rows, Columns, Values and Filters**.
- They read from a **pivot cache**: Refresh updates one cache; Refresh All updates everything. Use a Table as the source.
- Value Field Settings: change the function (Sum, Count, Average…) and **Show Values As** (% of total, % of row, difference from previous, running total, rank).
- MoM = change from the previous month; YoY = change from the same period last year.
- Group dates (years/quarters/months), group items manually, and group numbers into equal **bins**.
- Calculated fields work on totals, so use them for ratios like margin; add row-level maths to the source data.
- Slicers and timelines make pivots interactive; double-click a number to see the rows behind it.
:::

:::quiz
Q: You add 500 rows to the source range, but the pivot does not change. Why?
- Pivot tables only read the first 1,000 rows
* The pivot reads from its cache, which updates only when you refresh (and the range must include the new rows)
- The new rows need a pivot formula
- Pivot tables cannot be updated
> Refresh re-reads the source. If the source is a fixed range, also change the data source, or use a Table.

Q: Which "Show Values As" option gives month-on-month growth?
- % of Grand Total
- Running Total In
* % Difference From → (previous)
- Rank Largest to Smallest
> % Difference From the previous item compares each month with the one before it.

Q: What is the main difference between groups and bins?
* Bins are equal-width numeric intervals; groups can be any size and any data type
- Groups only work with dates
- Bins only work with text
- There is no difference
> Bins split numbers into equal intervals. Groups are custom collections of items.

Q: A calculated field `Revenue = Qty * Price` gives inflated numbers. Why?
- Calculated fields cannot multiply
* It multiplies the sum of Qty by the sum of Price for each group
- The pivot needs refreshing
- Price must be in Rows
> Calculated fields work on aggregated values. Compute Qty × Price in the source data instead.

Q: How do you see the individual rows behind a number in a pivot table?
- Press F9
* Double-click the number (Show Details)
- Use GETPIVOTDATA
- Insert a slicer
> Double-clicking opens a new sheet with the underlying records.

Q: Two pivots were built from the same data. You click Refresh on one. What happens to the other?
* It also updates, because they share the same pivot cache
- Nothing; you must refresh it separately
- It is deleted
- It shows an error
> Pivots from the same source share a cache; refreshing the cache updates all of them.
:::

:::exercise Superstore pivots
Build pivot tables from `superstore_sales.csv` to answer: (1) sales and profit by category and sub-category, with profit margin; (2) yearly sales by region with YoY %; (3) the 5 cities with the highest profit; (4) the number of order lines by discount (0%, 10%, … 40%) and their total profit.
???
(1) Rows: category, sub_category; Values: Sum of sales, Sum of profit; Calculated Field `Margin = profit/sales` formatted as %.
(2) Rows: region; Columns: order_date grouped by Years; Values: Sum of sales, plus a second copy shown as % Difference From (previous) Years.
(3) Rows: city; Values: Sum of profit; Value Filters → Top 10 → Top 5 Items by Sum of profit.
(4) Rows: discount; Values: Count of order_id and Sum of profit. You will see profit turn negative at the higher discount levels, matching the Lesson 5 crosstab.
:::

:::interview Questions you may be asked
**Q: What is a pivot cache and why does it matter?**
A hidden copy of the source data that pivots read from. It makes pivots fast and lets several pivots share data, but pivots only update on refresh, and many separate caches make files large.

**Q: How do you show each item's share of the total in a pivot?**
Value Field Settings → Show Values As → % of Grand Total (or % of Column/Row Total).

**Q: How would you count unique customers in a pivot?**
Create the pivot with "Add this data to the Data Model" ticked, then choose Distinct Count in Value Field Settings.

**Q: When would you use formulas (SUMIFS) instead of a pivot?**
When the report needs a fixed layout, mixes data from several sources, or must update without refreshing; pivots are better for exploration and flexible summaries.
:::
