---
num: 10
title: Charts and Advanced Charts
live: "Live classes 7–8"
updated: "Excel for Microsoft 365, 2026"
level: Intermediate
duration: 130 min
summary: Choose the right chart for every question, build and format column, bar, line, area, pie, scatter and combo charts, add sparklines, and create the advanced business charts taught in class: thermometer, Pareto, population pyramid and waterfall, plus histogram, box plot, treemap and funnel.
datasets: [superstore_sales.csv, hr_employees.csv]
outcomes:
  - Pick the right chart type from the question you want to answer
  - Insert, edit and format charts quickly (elements, axes, labels, colours, templates)
  - Build combo charts with a secondary axis and add sparklines
  - Build thermometer, Pareto, population pyramid and waterfall charts step by step
  - Use the newer statistical and hierarchy charts and apply chart design best practices
---

## Start with the question, not the chart

```python fig: Choose a chart by the question you are answering.
dg.cards([("Comparison", "Column or bar chart. Which region sells most?"), ("Trend over time", "Line or area chart. How did sales move month by month?"),
          ("Part of a whole", "Pie/doughnut (≤ 5 parts), stacked bar, treemap. What share is Technology?"), ("Relationship", "Scatter or bubble chart. Do discounts reduce profit?"),
          ("Distribution", "Histogram or box plot. How are order values spread?"), ("Contribution / flow", "Waterfall, Pareto, funnel. What drove the change in profit?")], cols=3, title="Chart chooser")
```

## Creating and editing a chart

:::steps The fast way
1. Select the data **including headers** (or a summary table / pivot table). For a quick chart press `Alt + F1` (embedded) or `F11` (new chart sheet).
2. Or use **Insert → Recommended Charts** to preview options.
3. Click the chart: three buttons appear at its top-right: **Chart Elements** (+), **Chart Styles** (brush) and **Chart Filters** (funnel).
4. **Chart Design** tab: Switch Row/Column, Select Data, Change Chart Type, Move Chart, Quick Layout.
5. **Format** pane: double-click any element (axis, series, label) or press `Ctrl + 1` with it selected.
:::

| Element | Good practice |
|---|---|
| **Title** | Say the insight: "Technology drives 77% of sales", not "Sales by Category" |
| **Axes** | Start bar/column axes at zero; format numbers (K, L, %); remove unnecessary decimals |
| **Gridlines** | Light grey or none |
| **Data labels** | Use them instead of an axis when there are few bars |
| **Legend** | Only if there is more than one series; better: label lines directly |
| **Colour** | One highlight colour for the point you want to make, grey for the rest |
| **Template** | Right-click → Save as Template to reuse your style |

## The core chart types

Here are the core charts built from Superstore data. The Excel steps follow each one.

```python fig: Column (comparison), line (trend), clustered and stacked bar (comparison of parts), and scatter (relationship).
import pandas as pd, matplotlib.pyplot as plt, numpy as np
s = pd.read_csv("superstore_sales.csv", parse_dates=["order_date"])
fig, axs = plt.subplots(2, 2, figsize=(11, 7))
r = s.groupby("region")["sales"].sum().sort_values(ascending=False) / 1e5
axs[0, 0].bar(r.index, r.values, color=[dg.VIO] + ["#C9C3E6"] * 3); axs[0, 0].set_title("Column: sales by region (₹ lakh)")
for i, v in enumerate(r.values): axs[0, 0].text(i, v + 5, f"{v:,.0f}", ha="center", fontsize=9)
m = s.set_index("order_date").resample("QS")["sales"].sum() / 1e5
axs[0, 1].plot(m.index, m.values, marker="o", color=dg.TEAL, lw=2); axs[0, 1].set_title("Line: quarterly sales (₹ lakh)")
cs = s.pivot_table(index="segment", columns="category", values="sales", aggfunc="sum") / 1e5
cs.plot.barh(stacked=True, ax=axs[1, 0], color=[dg.CORAL, dg.GOLD, dg.VIO], width=.6); axs[1, 0].set_title("Stacked bar: category mix by segment"); axs[1, 0].legend(fontsize=8, loc="lower right")
smp = s.sample(600, random_state=1)
axs[1, 1].scatter(smp.discount * 100 + np.random.default_rng(1).normal(0, .8, len(smp)), smp.profit / 1000, s=10, alpha=.5, color=dg.SKY)
axs[1, 1].axhline(0, color="#999", lw=1); axs[1, 1].set_xlabel("Discount %"); axs[1, 1].set_ylabel("Profit (₹ '000)"); axs[1, 1].set_title("Scatter: discount vs profit")
fig
```

| Chart | Excel path | Use when |
|---|---|---|
| Clustered column / bar | Insert → Column or Bar | Comparing categories; use **bar** when labels are long or there are many categories |
| Stacked / 100% stacked | Same menu | Showing parts of a total across groups |
| Line | Insert → Line (with markers) | Trends over time; up to ~5 lines |
| Area | Insert → Line → Area | Cumulative trends; volume over time |
| Pie / doughnut | Insert → Pie | 2–5 parts of a whole that add to 100% |
| Scatter (XY) | Insert → Scatter | Relationship between two numbers; add a **trendline** (right-click series → Add Trendline, tick Display R²) |
| Bubble | Insert → Scatter → Bubble | Scatter with a third measure as bubble size |

:::mistake Chart crimes to avoid
3D charts, pie charts with 10 slices, two different units on one axis, truncated bar axes that exaggerate differences, rainbow colours, and charts without units. If you need to squint, the chart has failed.
:::

## Combo charts and the secondary axis

When two measures have very different scales (sales in lakhs and profit margin in %), plot one as columns and the other as a line on a **secondary axis**.

:::steps Build a combo chart
1. Make a summary table: Month, Sales, Margin %.
2. Select it → Insert → **Combo Chart** → Create Custom Combo Chart.
3. Sales: Clustered Column. Margin %: Line with Markers, tick **Secondary Axis**.
4. Add axis titles so readers know which axis belongs to which series.
:::

```python fig: Combo chart: monthly sales (columns, left axis) and profit margin (line, right axis) for 2025.
d = s[s.order_date.dt.year == 2025].groupby(s.order_date.dt.month)[["sales", "profit"]].sum()
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(d.index, d.sales / 1e5, color="#C9C3E6", label="Sales (₹ lakh)"); ax.set_ylabel("Sales (₹ lakh)")
ax2 = ax.twinx(); ax2.plot(d.index, d.profit / d.sales * 100, color=dg.CORAL, marker="o", lw=2.2, label="Margin %"); ax2.set_ylabel("Profit margin %"); ax2.grid(False)
ax.set_xticks(range(1, 13)); ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]); ax.set_title("2025: sales vs margin")
fig.legend(loc="upper left", bbox_to_anchor=(.08, .92), fontsize=9)
fig
```

## Sparklines

Sparklines are tiny charts **inside a cell**: Insert → **Sparklines** → Line, Column or Win/Loss. Select the data range (for example 12 months in a row) and the location cell. Use **Sparkline → Show → High Point / Low Point** to mark extremes. They are ideal in dashboard tables, one row per product or region.

## Thermometer chart (target vs actual)

A thermometer shows progress towards a single target, such as "₹ 7.4 crore of the ₹ 9 crore annual target".

```xl title="Thermometer data"
Metric{h}|Value{h}
Target|900{;#,##0}
Achieved|742{;#,##0}
% achieved|=B3/B2{;0.0%}
```

:::steps Build it
1. Select only the **% achieved** cell (and its label) → Insert → **Clustered Column**.
2. Format the vertical axis: Minimum **0**, Maximum **1** (100%). Delete the horizontal axis and gridlines.
3. Format the series: Gap Width **0%** so the column fills the width; choose a strong fill colour.
4. Optional: add a second series with value 1 (100%) on the secondary axis, no fill and a thick border to draw the "glass" of the thermometer; set the secondary axis to 0–1 as well.
5. Resize the chart to be tall and narrow; add a data label showing 82.4%.
:::

```python fig: Thermometer chart: 82.4% of the annual target achieved.
fig, ax = plt.subplots(figsize=(2.6, 4.6))
ax.bar([0], [1], width=.6, color="white", edgecolor=dg.INK, lw=2); ax.bar([0], [742 / 900], width=.6, color=dg.CORAL)
ax.set_ylim(0, 1.05); ax.set_xlim(-.6, .6); ax.set_xticks([]); ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
ax.text(0, 742 / 900 + .03, "82.4%", ha="center", weight="bold"); ax.set_title("Annual target", fontsize=11); ax.grid(False)
fig
```

## Pareto chart (the 80/20 rule)

The Pareto principle says that roughly 80% of effects come from 20% of causes: a few sub-categories drive most sales, a few complaint types cause most tickets. A Pareto chart shows sorted bars plus a **cumulative %** line.

```python run
pareto = s.groupby("sub_category")["sales"].sum().sort_values(ascending=False).to_frame()
pareto["share %"] = (pareto.sales / pareto.sales.sum() * 100).round(1)
pareto["cumulative %"] = pareto["share %"].cumsum().round(1)
pareto["sales"] = (pareto.sales / 1e5).round(1)
pareto.rename(columns={"sales": "sales (₹ lakh)"})
```

:::steps Build it in Excel
1. Summarise sales by sub-category (pivot or SUMIFS) and **sort largest to smallest**.
2. Add `Cumulative %`: in C2 `=SUM($B$2:B2)/SUM($B$2:$B$13)`, copy down.
3. Select the three columns → Insert → **Combo**: Sales = Clustered Column, Cumulative % = Line on the **Secondary Axis**.
4. Set the secondary axis maximum to 100%. Optionally add a horizontal 80% reference line.
5. Excel 2016+ also has a built-in **Insert → Statistical → Pareto** chart that sorts and accumulates for you from raw data.
:::

```python fig: Pareto chart of sales by sub-category. Copiers, Machines and Phones alone make up 76% of sales; adding Tables passes the 80% line.
fig, ax = plt.subplots(figsize=(10.5, 4.3))
ax.bar(pareto.index, pareto["sales (₹ lakh)"] if "sales (₹ lakh)" in pareto else pareto.sales, color=[dg.VIO if c <= 81 else "#C9C3E6" for c in pareto["cumulative %"]])
ax.set_ylabel("Sales (₹ lakh)"); ax.tick_params(axis="x", rotation=45)
ax2 = ax.twinx(); ax2.plot(pareto.index, pareto["cumulative %"], color=dg.CORAL, marker="o", lw=2); ax2.set_ylim(0, 105); ax2.axhline(80, ls="--", color="#999", lw=1); ax2.set_ylabel("Cumulative %"); ax2.grid(False)
ax.set_title("Pareto: a few sub-categories drive most sales")
fig
```

## Population pyramid

A population pyramid compares two groups (typically male and female) across age bands, with one group's bars going left and the other's going right. In business it works for any two-sided comparison: this year vs last year by product, or two regions by age band.

```python run
hr = pd.read_csv("hr_employees.csv")
hr["age_band"] = pd.cut(hr.age, [20, 25, 30, 35, 40, 45, 50, 55, 60], labels=["21-25", "26-30", "31-35", "36-40", "41-45", "46-50", "51-55", "56-60"])
pyr = hr.pivot_table(index="age_band", columns="gender", values="emp_id", aggfunc="count", observed=False)
pyr["Male (negative)"] = -pyr["Male"]
pyr
```

:::steps Build it
1. Count employees by age band and gender (pivot table or COUNTIFS).
2. Make the male counts **negative** (`=-C2`) in a helper column so they plot to the left.
3. Select age bands, the negative male column and the female column → Insert → **Clustered Bar**.
4. Format series: Series Overlap **100%**, Gap Width **10–30%**.
5. Format the horizontal axis numbers with the custom format `#,##0;#,##0` so negative values show without a minus sign.
6. Vertical axis → Labels → Label Position: **Low** so the age labels sit on the left edge.
:::

```python fig: Population pyramid of the 1,500 employees in the HR dataset.
fig, ax = plt.subplots(figsize=(8.5, 4.4))
ax.barh(pyr.index.astype(str), -pyr["Male"], color=dg.SKY, label="Male"); ax.barh(pyr.index.astype(str), pyr["Female"], color=dg.CORAL, label="Female")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{abs(int(v))}")); ax.axvline(0, color="#666", lw=1)
ax.set_title("Employees by age band and gender"); ax.legend(loc="lower right"); ax.set_xlabel("Employees")
fig
```

## Waterfall chart

A waterfall shows how a starting value becomes an ending value through positive and negative steps: revenue to profit, last year's sales to this year's, or budget to actual.

```xl title="Waterfall data: from revenue to net profit (₹ lakh)"
Step{h}|Amount{h}
Revenue|1200
Cost of goods|-640
Gross profit|=B2+B3
Marketing|-120
Salaries|-210
Other income|35
Net profit|=B4+B5+B6+B7
```

:::steps Build it (Excel 2016 and later)
1. Select the table → Insert → **Waterfall** (Insert → Charts → Waterfall, Funnel…).
2. Click the **Gross profit** bar twice (to select only that point) → right-click → **Set as total**. Do the same for **Net profit**. Totals then start from zero instead of floating.
3. Colour increases, decreases and totals differently (Format Data Point) and add data labels.
:::

In older Excel versions you build the same chart as a **stacked column** with an invisible "base" series, an "up" series and a "down" series computed with formulas.

```python fig: Waterfall from revenue to net profit. Totals are anchored at zero; increases are green and decreases are red.
steps = [("Revenue", 1200, "t"), ("Cost of goods", -640, "d"), ("Gross profit", 560, "t"), ("Marketing", -120, "d"), ("Salaries", -210, "d"), ("Other income", 35, "u"), ("Net profit", 265, "t")]
fig, ax = plt.subplots(figsize=(10, 4.2)); run = 0
for i, (lab, v, k) in enumerate(steps):
    if k == "t": base, h, c = 0, v, dg.VIO; run = v
    else: base, h, c = (run + v, -v, "#D9534F") if v < 0 else (run, v, "#2E9E6B"); run += v
    ax.bar(i, h, bottom=base, color=c, width=.6); ax.text(i, base + h + 15, f"{v:+,}" if k != "t" else f"{v:,}", ha="center", fontsize=9.5)
ax.set_xticks(range(len(steps))); ax.set_xticklabels([x[0] for x in steps]); ax.set_ylabel("₹ lakh"); ax.set_title("From revenue to net profit")
fig
```

## Statistical and hierarchy charts (Excel 2016+)

| Chart | Insert path | Shows | Example question |
|---|---|---|---|
| **Histogram** | Insert → Statistical → Histogram | Frequency distribution; set bin width in Format Axis | How are order values distributed? |
| **Box & Whisker** | Insert → Statistical → Box and Whisker | Median, quartiles and outliers by group | Do salaries vary more in Sales than in IT? |
| **Treemap** | Insert → Hierarchy → Treemap | Nested rectangles sized by value | Category → sub-category share of sales |
| **Sunburst** | Insert → Hierarchy → Sunburst | Rings for hierarchy levels | Region → state → city |
| **Funnel** | Insert → Waterfall → Funnel | Drop-off between stages | Visitors → sign-ups → orders |
| **Filled map** | Insert → Maps | Values by country or state | Sales by state (needs internet) |

```python fig: Histogram of order-line sales values and box plots of monthly income by department (HR data).
fig, axs = plt.subplots(1, 2, figsize=(11, 4))
axs[0].hist(s.sales.clip(upper=60000) / 1000, bins=24, color=dg.TEAL, edgecolor="white"); axs[0].set_title("Histogram: order-line sales (₹ '000)"); axs[0].set_xlabel("₹ '000 (values above 60k grouped at the end)")
order = hr.groupby("department").monthly_income.median().sort_values().index
axs[1].boxplot([hr.loc[hr.department == d, "monthly_income"] / 1000 for d in order], tick_labels=order, patch_artist=True, boxprops=dict(facecolor="#E6E0FF", color=dg.VIO), medianprops=dict(color=dg.CORAL, lw=2))
axs[1].set_title("Box plot: monthly income by department (₹ '000)"); axs[1].tick_params(axis="x", rotation=20)
fig
```

## Dynamic charts

Charts become interactive when their source updates:

- **Table source**: new rows are added to the chart automatically.
- **Named range / dynamic named range** (Lesson 9) as the series values: `=Book1.xlsx!SalesLast12`.
- **Drop-down + formulas**: a Data Validation drop-down picks a region, formulas (XLOOKUP/FILTER) pull that region's numbers into a helper table, and the chart reads the helper table.
- **Pivot charts + slicers** (Lesson 8) for click-to-filter dashboards (Lesson 11).

:::new Charts in Excel 365 (2026)
Copilot can suggest and insert charts from a sentence ("show monthly sales by region as a line chart"), and **Analyze Data** (Home → Analyze Data) proposes ready-made pivot charts with insights. Python in Excel can create seaborn or matplotlib charts inside the grid with `=PY()`.
:::

## Summary

:::key
- Choose the chart from the question: comparison (bar/column), trend (line), part-of-whole (pie for ≤5, stacked bar, treemap), relationship (scatter), distribution (histogram, box), contribution (waterfall, Pareto).
- Titles should state the insight; start bar axes at zero; use one highlight colour.
- Combo charts with a secondary axis show two measures of different scales.
- **Thermometer**: one % column, axis 0–100%, gap width 0.
- **Pareto**: sorted bars + cumulative % line on a secondary axis; look for the ~80% point.
- **Population pyramid**: one series negative, overlap 100%, custom format `#,##0;#,##0`.
- **Waterfall**: Insert → Waterfall, then "Set as total" for subtotal bars.
:::

:::quiz
Q: Which chart best shows how monthly revenue changed over two years?
- Pie
* Line
- Treemap
- Scatter
> Lines show trends over time.

Q: In a Pareto chart, what does the line represent?
- The average value
* The cumulative percentage of the total
- The target
- The trend
> The line accumulates each bar's share to show where ~80% is reached.

Q: How do you make the male bars go to the left in a population pyramid?
* Make the male values negative and format the axis to hide the minus sign
- Use a pie chart
- Reverse the category order
- Put males on a secondary axis
> Negative values plot to the left; `#,##0;#,##0` shows them as positive numbers.

Q: In Excel's waterfall chart, why must Gross profit be "Set as total"?
- To change its colour
* So it starts from zero instead of floating on the previous step
- To hide it
- To make it a line
> Totals should be anchored to the axis; otherwise Excel treats them as another step.

Q: When should you use a secondary axis?
- Whenever there are two series
* When two series have very different scales or units, such as sales and margin %
- When the chart is a pie
- Never
> A secondary axis lets both series be readable; label both axes clearly.

Q: Which chart shows median, quartiles and outliers for several groups?
- Histogram
* Box and whisker
- Funnel
- Sunburst
> Box plots summarise distributions and highlight outliers.
:::

:::exercise Build four charts from Superstore
(1) A Pareto chart of profit by sub-category (watch out for negative profit: what does it mean?). (2) A combo chart of quarterly sales (columns) and order count (line, secondary axis). (3) A waterfall from 2024 total sales to 2025 total sales, with one step per region showing the change. (4) A box plot of discount by category.
???
(1) Sort profit descending; negative sub-categories (such as Tables and Bookcases here) reduce the cumulative total, so the cumulative line rises above 100% and then falls; a Pareto chart works best on positive values, so plot losses separately.
(2) Pivot by quarter with Sum of sales and Count of order_id → Combo chart with the count on the secondary axis.
(3) Table: 2024 total; North change; South change; East change; West change; 2025 total. Insert → Waterfall; set the first and last bars as totals.
(4) Select category and discount columns → Insert → Box and Whisker.
:::

:::interview Questions you may be asked
**Q: How do you choose a chart type?**
From the question: comparison, trend, composition, relationship, distribution or contribution. Then simplify: remove clutter, highlight the key point and write an insight title.

**Q: What is a Pareto analysis used for?**
To find the vital few causes (products, customers, complaint types) that produce most of the effect, so that effort is focused where it matters.

**Q: How would you show actual vs target for 10 sales reps?**
A bar chart of actuals with a target marker (a line or a thin overlapping bar per rep), or a bullet chart; a thermometer works for one overall target.
:::
