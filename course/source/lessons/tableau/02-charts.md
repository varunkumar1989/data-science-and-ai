---
num: 2
title: "Charts in Tableau: From Bar and Line to Maps, Dual Axis, Histograms and Pareto"
updated: "Tableau Desktop / Tableau Public 2026"
level: Beginner
duration: 150 min
summary: Build every core chart in Tableau and know when to use each: bar, stacked and side-by-side bars, line and area, pie and donut, treemap, highlight table, scatter plot, histogram with bins, box plot, filled and symbol maps, dual-axis combo charts, bullet charts and a Pareto chart, all on the Superstore India data.
datasets: [superstore_sales.csv]
outcomes:
  - Choose the right chart for comparison, trend, part-to-whole, distribution, relationship and geography questions
  - Build bar, line, area, pie, donut, treemap and highlight-table views
  - Create bins and histograms, box plots and scatter plots with trend lines
  - Map states with geographic roles, and combine two measures with dual and blended axes
  - Build a bullet chart and a Pareto (80/20) chart
---

## Choose the chart from the question

```python fig: Match the business question to the chart family.
dg.cards([("Compare", "Bar, side-by-side bar, bullet. 'Which region sells most?'"), ("Trend", "Line, area, dual-axis. 'How did sales move by month?'"), ("Part-to-whole", "Stacked bar, treemap, pie/donut (few slices). 'What share is Technology?'"), ("Distribution", "Histogram, box plot. 'How big is a typical order?'"), ("Relationship", "Scatter with trend line. 'Do discounts hurt profit?'"), ("Geography", "Filled or symbol map. 'Which states lead?'")], title="Question → chart", cols=3)
```

All examples below use the Superstore India data. The tables show the numbers your Tableau view should display, computed here with pandas so you can check your work.

```python run
import pandas as pd, numpy as np
df = pd.read_csv("superstore_sales.csv", parse_dates=["order_date"])
df["year"] = df.order_date.dt.year
print(len(df), "order lines,", df.order_id.nunique(), "orders,", df.customer_id.nunique(), "customers")
```

## Bar charts

| Variant | Build | Use |
|---|---|---|
| Bar | Dimension on Rows, measure on Columns | Ranking categories |
| Stacked bar | Add a second dimension to **Color** | Total and composition |
| Side-by-side bar | Second dimension on Columns *before* the measure (or Show Me → side-by-side) | Comparing subgroups directly |
| 100% stacked | Stacked bar + Quick Table Calculation → **Percent of Total** (compute using the colour dimension) | Mix comparisons |

```python run
seg = pd.crosstab(df.category, df.segment, values=df.sales, aggfunc="sum") / 1e7
seg.round(2)
```

```python fig: Stacked bar: Sales by Category, coloured by Segment (₹ crore).
import pandas as pd, matplotlib.pyplot as plt
d = pd.read_csv("superstore_sales.csv"); t = pd.crosstab(d.category, d.segment, values=d.sales, aggfunc="sum") / 1e7
t = t.loc[t.sum(axis=1).sort_values().index]
import numpy as np
fig, ax = plt.subplots(figsize=(8, 2.9)); cols = ["#4E79A7", "#F28E2B", "#E15759"]
left = np.zeros(len(t))
for c, col in zip(t.columns, cols):
    ax.barh(t.index, t[c], left=left, color=col, label=c); left += t[c].values
ax.legend(ncol=3, loc="lower right", frameon=False, fontsize=9); ax.set_xlabel("Sales (₹ crore)"); ax.spines[["top", "right"]].set_visible(False)
fig
```

## Line and area charts

Put a **continuous** date (green MONTH(Order Date)) on Columns and Sales on Rows for one timeline. Put **YEAR** on Color and a **discrete** MONTH on Columns to compare the same months across years (seasonality).

```python run
pv = df.pivot_table(index=df.order_date.dt.month, columns="year", values="sales", aggfunc="sum") / 1e5
pv.index.name = "month"
pv.round(1).head(6)
```

```python fig: Discrete month on Columns, Year on Color: each year is a line, so seasonality is easy to compare.
import pandas as pd, matplotlib.pyplot as plt
d = pd.read_csv("superstore_sales.csv", parse_dates=["order_date"])
p = d.pivot_table(index=d.order_date.dt.month, columns=d.order_date.dt.year, values="sales", aggfunc="sum") / 1e5
fig, ax = plt.subplots(figsize=(8, 3))
for y, col in zip(p.columns, ["#4E79A7", "#F28E2B", "#E15759"]): ax.plot(p.index, p[y], marker="o", ms=3.5, color=col, label=str(y))
ax.set_xticks(range(1, 13)); ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], fontsize=9)
ax.set_ylabel("Sales (₹ lakh)"); ax.legend(frameon=False, ncol=3, fontsize=9); ax.spines[["top", "right"]].set_visible(False)
fig
```

An **area chart** is the same view with Mark type = Area; stack a dimension on Color to show how the total is built up.

## Part-to-whole: pie, donut, treemap

- **Pie**: Mark type Pie, dimension on Color, measure on **Angle**. Use for 2–5 slices only.
- **Donut**: two pies on a dual axis. Put `AVG(0)` (type `avg(0)` on Rows) twice, make the second smaller and white, turn on dual axis, and put the total on the inner label.
- **Treemap**: dimension on **Detail/Label**, measure on **Size** and **Color**. Good for many categories (e.g. the 13 sub-categories).

```python run
sub = (df.groupby("sub_category").agg(sales=("sales", "sum"), profit=("profit", "sum")) / 1e5).sort_values("sales", ascending=False)
sub["margin %"] = (sub.profit / sub.sales * 100).round(1)
sub.round(1).head(8)
```

## Highlight table (heat map)

Category on Rows, YEAR on Columns, Sales on **Text** and **Color**, Mark type **Square**. Tableau shades each cell, so high and low cells stand out without reading every number.

## Distribution: histogram and box plot

:::steps Histogram of order value
1. Right-click **Sales** → Create → **Bins**; set the bin size (e.g. ₹10,000). A new dimension "Sales (bin)" appears.
2. Drag **Sales (bin)** to Columns and **CNT(Sales)** (or Number of Records) to Rows.
3. Or select Sales and pick the histogram in Show Me: it creates the bins for you.
:::

```python run
bins = pd.cut(df.sales, bins=[0, 5000, 10000, 20000, 50000, 100000, df.sales.max()], right=False)
print(bins.value_counts().sort_index())
print("median line value: ₹", round(df.sales.median()), "| mean: ₹", round(df.sales.mean()))
```

The mean is well above the median: a few large orders pull it up (right skew). A **box plot** (Show Me → box-and-whisker) shows the median, quartiles and outliers per category at a glance.

## Relationship: scatter plot

Put SUM(Sales) on Columns, SUM(Profit) on Rows and **Sub-Category** on Detail: one dot per sub-category. Add **Analytics pane → Trend Line** (linear) and hover it to read R² and the p-value.

```python run
s = df.groupby("sub_category")[["sales", "profit", "discount"]].agg({"sales": "sum", "profit": "sum", "discount": "mean"})
print("correlation sales vs profit across sub-categories:", round(s.sales.corr(s.profit), 2))
print("correlation avg discount vs profit margin:", round(s.discount.corr(s.profit / s.sales), 2))
```

## Maps

1. Make sure **State** has the geographic role *State/Province* (and the country is India: Map → Edit Locations).
2. Double-click State: Tableau adds Latitude/Longitude (generated) and draws a **symbol map**. Change Mark type to **Map** for a **filled (choropleth) map**.
3. Put Sales on Color for a filled map, or on Size for a symbol map. Use Profit on Color with a diverging palette (orange-blue) to show loss-making states.

```python run
st = (df.groupby("state")[["sales", "profit"]].sum() / 1e5).round(1).sort_values("sales", ascending=False)
st.head(6)
```

:::tip Indian maps
Tableau's built-in geocoding knows Indian states and many districts and cities. If a name does not match (old spellings, "Orissa" vs "Odisha"), use **Map → Edit Locations** to match it, or join a custom latitude/longitude file.
:::

## Dual-axis and combo charts

Show two measures with different scales, e.g. Sales as bars and Profit margin as a line:

1. Continuous MONTH(Order Date) on Columns; SUM(Sales) and the margin calculation on Rows.
2. Right-click the second pill → **Dual Axis**. Set the Marks card for Sales to **Bar** and for margin to **Line**.
3. Right-click the right axis → **Synchronize Axis** only when both measures share units (Sales and Profit); never synchronise ₹ with %.

A **blended axis** (drag a second measure onto the *existing* axis until the double-ruler icon shows) puts two measures with the same unit on one axis, using Measure Names on Color.

## Bullet chart (actual vs target)

Select a measure and a target (e.g. Sales and a target field) → Show Me → **Bullet graph**. The bar is the actual, the reference line is the target, and the shaded bands are % of target (60%, 80%). If the bars and lines come out the wrong way round, right-click the axis → **Swap Reference Line Fields**.

## Pareto chart (80/20)

:::steps Build a Pareto of products
1. Product Name on Columns sorted by SUM(Sales) descending; SUM(Sales) on Rows as bars.
2. Drag SUM(Sales) to Rows again → Quick Table Calculation → **Running Total**, then Edit Table Calculation → *Add secondary calculation* → **Percent of Total**.
3. Make it dual axis; set the second mark to Line; add a reference line at 80%.
4. Optional: replace Product Name on Columns with a table calc `INDEX()/SIZE()` so the x-axis reads "% of products".
:::

```python run
p = df.groupby("product_name").sales.sum().sort_values(ascending=False)
cum = p.cumsum() / p.sum()
n80 = int((cum < .8).sum()) + 1
print(f"{n80} of {len(p)} products ({n80 / len(p):.0%}) make 80% of sales")
```

Sales are concentrated: about a quarter of the products bring in 80% of sales, close to the classic 80/20 rule. Those top products deserve the best stock availability and marketing. A Pareto chart shows how concentrated a business really is, so you can judge whether a "focus on the top products" strategy makes sense.

## Summary

:::key
- Pick the chart from the question: compare, trend, part-to-whole, distribution, relationship, geography.
- Continuous dates draw timelines; discrete dates compare periods.
- Bins create histograms; the Analytics pane adds trend lines, reference lines and box plots.
- Assign geographic roles before mapping; use filled maps for rates and symbol maps for totals.
- Dual axis combines two marks (bar + line); synchronise only when units match.
:::

:::quiz
Q: Which chart best shows how a single order-value variable is distributed?
* Histogram
- Pie chart
- Treemap
- Line chart
> Histograms show distributions; create bins first.

Q: How do you get Profit as a line on top of Sales bars with its own scale?
* Put both on Rows, use Dual Axis, set one mark to Bar and the other to Line
- Put Profit on Color
- Use a blended axis
- Synchronise the axes
> Dual axis gives two independent axes and separate mark types.

Q: Which is the right way to show 13 sub-categories as a part-to-whole?
* Treemap or sorted bar chart
- Pie chart with 13 slices
- Scatter plot
- Line chart
> Pies stop being readable beyond about five slices.

Q: You want each year as its own line to compare seasonality. What goes on Columns?
* Discrete MONTH(Order Date)
- Continuous MONTH(Order Date)
- YEAR(Order Date) only
- Sales
> Discrete month gives Jan–Dec headers; Year goes on Color.

Q: What does the Pareto line show?
* The running total of sales as a percent of the grand total
- Profit margin
- Average sales
- The number of orders
> Running total + percent of total secondary calculation.

Q: When should you synchronise a dual axis?
* When both measures share the same unit and scale makes sense
- Always
- When one is in ₹ and the other in %
- Never
> Synchronising ₹ with % distorts the chart.
:::

:::exercise Practice
Build: (1) a side-by-side bar of Sales by Region and Segment; (2) a filled map of Profit by State with a diverging palette; (3) a histogram of Sales with ₹10,000 bins; (4) a dual-axis chart of monthly Sales (bars) and Profit (line); (5) a Pareto chart of sub-categories with an 80% reference line.
???
Use the steps in each section. For the map, set Profit on Color → Edit Colors → Orange-Blue Diverging, centre 0. For the Pareto use Running Total + Percent of Total, compute using Sub-Category, then Analytics → Reference Line → Constant 0.8 on the line axis.
:::

:::interview Questions you may be asked
**Q: Dual axis vs blended axis?**
A dual axis gives two independent axes (left and right) and allows different mark types; a blended axis puts several measures on one shared axis (same unit) using Measure Names/Values.

**Q: How do you build a Pareto chart in Tableau?**
Sort the dimension by the measure, show bars, add the measure again with a Running Total table calculation and a secondary Percent of Total, make it dual axis as a line, and add an 80% reference line.

**Q: Filled map or symbol map?**
Filled maps suit rates and ratios (profit margin by state) because area does not scale with value; symbol maps with size suit totals (sales by city).
:::
