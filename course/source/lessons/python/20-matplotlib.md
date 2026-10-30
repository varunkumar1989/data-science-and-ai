---
num: 20
title: "Data Visualisation I: Matplotlib and Choosing the Right Chart"
live: "Python class 16"
updated: "Matplotlib 3.10"
level: Intermediate
duration: 110 min
summary: Pick the right chart for the question and build it with Matplotlib's object-oriented API. Line, bar, histogram, scatter, box and pie charts, subplots, annotations, styling and saving, plus design rules that make charts honest and readable.
datasets: [superstore_sales.csv, house_prices.csv]
outcomes:
  - Choose a chart type from the analytical question (trend, comparison, distribution, relationship, composition)
  - Build charts with fig, ax = plt.subplots() and customise titles, labels, ticks, legends and colours
  - Combine several charts with subplots and annotate key points
  - Plot directly from pandas and save figures at publication quality
  - Apply design rules: start bars at zero, remove clutter, label directly, use colour with purpose
---

## Choose the chart from the question

```python fig: Start from the question, not the chart type.
dg.cards([("Trend over time", "Line chart (area for cumulative)"), ("Compare categories", "Bar / column chart, sorted"), ("Distribution", "Histogram, box plot, violin"), ("Relationship", "Scatter (+ trend line), heatmap of correlations"), ("Part of a whole", "Stacked bar; pie only for 2–4 parts"), ("Geography", "Map / choropleth")], title="Which chart?")
```

## The object-oriented API

Matplotlib has two styles. Use the **object-oriented** one: create a **Figure** (the canvas) and one or more **Axes** (plots), then call methods on the axes.

```python fig: Monthly Superstore sales: a line chart shows the trend and the seasonal peaks.
import pandas as pd, matplotlib.pyplot as plt
s = pd.read_csv("superstore_sales.csv", parse_dates=["order_date"])
m = s.set_index("order_date")["sales"].resample("ME").sum() / 1e6
fig, ax = plt.subplots(figsize=(9, 3.6))
ax.plot(m.index, m.values, color="#7C3AED", lw=2, marker="o", ms=3)
ax.set_title("Monthly sales, 2023–2025", loc="left", fontsize=13, weight="bold")
ax.set_ylabel("₹ million"); ax.set_ylim(0)
ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="y", alpha=.3)
peak = m.idxmax(); ax.annotate(f"Peak {m.max():.1f}M\n{peak:%b %Y}", xy=(peak, m.max()), xytext=(-90, -10), textcoords="offset points", arrowprops=dict(arrowstyle="->", color="#555"))
```

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(9, 3.6))   # one figure, one axes
ax.plot(x, y)                              # draw
ax.set_title("..."); ax.set_xlabel("..."); ax.set_ylabel("...")
fig.savefig("chart.png", dpi=200, bbox_inches="tight")
plt.show()                                 # in scripts; notebooks display automatically
```

| Element | Method |
|---|---|
| Title, axis labels | `ax.set_title`, `ax.set_xlabel`, `ax.set_ylabel` |
| Limits, ticks | `ax.set_ylim(0)`, `ax.set_xticks`, `ax.tick_params(rotation=45)` |
| Legend | `label="..."` in the plot call, then `ax.legend()` |
| Grid, spines | `ax.grid(axis="y")`, `ax.spines[["top","right"]].set_visible(False)` |
| Text, arrows | `ax.text`, `ax.annotate` |
| Reference lines | `ax.axhline(y)`, `ax.axvline(x)`, `ax.axvspan` |
| Number format | `ax.yaxis.set_major_formatter(...)` |

## Bar charts

```python fig: Sorted horizontal bars make category comparisons easy; one highlight colour draws the eye.
cat = s.groupby("sub_category")["profit"].sum().sort_values() / 1e6
colors = ["#DB2777" if v < 0 else "#C4B5FD" for v in cat.values]
colors[-1] = "#7C3AED"
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(cat.index, cat.values, color=colors)
ax.axvline(0, color="#333", lw=.8)
for y, v in enumerate(cat.values): ax.text(v + (0.15 if v >= 0 else -0.15), y, f"{v:.1f}", va="center", ha="left" if v >= 0 else "right", fontsize=8)
ax.set_title("Profit by sub-category (₹ million): Copiers lead, Tables and Bookcases lose money", loc="left", fontsize=11, weight="bold")
ax.spines[["top", "right"]].set_visible(False); ax.set_xlabel("₹ million")
```

Grouped and stacked bars compare two dimensions:

```python fig: Sales by region and category, as grouped bars (compare within region) and stacked bars (compare totals).
import numpy as np
pv = s.pivot_table(index="region", columns="category", values="sales", aggfunc="sum") / 1e6
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6))
x = np.arange(len(pv)); w = .26; pal = ["#7C3AED", "#DB2777", "#0E9F8E"]
for i, c in enumerate(pv.columns): a1.bar(x + (i - 1) * w, pv[c], w, label=c, color=pal[i])
a1.set_xticks(x, pv.index); a1.set_title("Grouped", loc="left", weight="bold"); a1.legend(frameon=False, fontsize=8)
bottom = np.zeros(len(pv))
for i, c in enumerate(pv.columns): a2.bar(pv.index, pv[c], bottom=bottom, color=pal[i], label=c); bottom += pv[c].values
a2.set_title("Stacked", loc="left", weight="bold")
for a in (a1, a2): a.spines[["top", "right"]].set_visible(False); a.set_ylabel("₹ million")
```

## Distributions: histogram and box plot

```python fig: House prices are right-skewed: the mean sits above the median. Box plots compare distributions across cities.
h = pd.read_csv("house_prices.csv")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6), gridspec_kw={"width_ratios": [1, 1.2]})
a1.hist(h["price_lakh"], bins=30, color="#C4B5FD", edgecolor="white")
a1.axvline(h.price_lakh.mean(), color="#DB2777", lw=2, label=f"mean {h.price_lakh.mean():.0f}")
a1.axvline(h.price_lakh.median(), color="#7C3AED", lw=2, ls="--", label=f"median {h.price_lakh.median():.0f}")
a1.set_title("Price distribution (₹ lakh)", loc="left", weight="bold"); a1.legend(frameon=False)
order = h.groupby("city")["price_lakh"].median().sort_values().index
a2.boxplot([h.loc[h.city == c, "price_lakh"] for c in order], tick_labels=order, patch_artist=True, boxprops=dict(facecolor="#EDE9FE"), medianprops=dict(color="#7C3AED", lw=2), flierprops=dict(markersize=2))
a2.tick_params(axis="x", rotation=30); a2.set_title("Price by city (sorted by median)", loc="left", weight="bold")
for a in (a1, a2): a.spines[["top", "right"]].set_visible(False)
```

Bins matter: too few hide the shape, too many look noisy. Try `bins="auto"` or a few values.

## Relationships: scatter

```python fig: Larger houses cost more (r ≈ 0.8); colour shows a third variable, the distance to the centre.
hh = h.dropna(subset=["area_sqft"])
fig, ax = plt.subplots(figsize=(8, 4))
sc = ax.scatter(hh.area_sqft, hh.price_lakh, c=hh.distance_to_center_km, cmap="viridis_r", s=10, alpha=.7)
b, a0 = np.polyfit(hh.area_sqft, hh.price_lakh, 1); xs = np.linspace(hh.area_sqft.min(), hh.area_sqft.max(), 50)
ax.plot(xs, a0 + b * xs, color="#DB2777", lw=2, label="least-squares line")
fig.colorbar(sc, ax=ax, label="km from centre"); ax.legend(frameon=False)
ax.set_xlabel("area (sq ft)"); ax.set_ylabel("price (₹ lakh)"); ax.spines[["top", "right"]].set_visible(False)
```

## Part of a whole

```python fig: Pie charts work for a few parts; the donut variant leaves room for a label.
seg = s.groupby("segment")["sales"].sum()
fig, ax = plt.subplots(figsize=(4.2, 4.2))
ax.pie(seg, labels=seg.index, autopct="%1.0f%%", startangle=90, counterclock=False, colors=["#7C3AED", "#C4B5FD", "#DB2777"], wedgeprops=dict(width=.42, edgecolor="white"))
ax.set_title("Sales by segment", weight="bold")
```

For more than 4 parts, or to compare parts across groups, use (stacked) bars.

## Plotting from pandas

DataFrames and Series have `.plot()`, a quick wrapper around Matplotlib that returns an `ax` you can keep styling.

```python fig: One line of pandas plotting, then a little Matplotlib styling.
ax = (s.assign(year=s.order_date.dt.year).pivot_table(index="year", columns="category", values="sales", aggfunc="sum") / 1e6).plot(kind="bar", figsize=(7, 3.4), color=["#7C3AED", "#DB2777", "#0E9F8E"], rot=0)
ax.set_ylabel("₹ million"); ax.set_title("Sales by year and category", loc="left", weight="bold"); ax.spines[["top", "right"]].set_visible(False); ax.legend(frameon=False)
```

`kind=` can be `line`, `bar`, `barh`, `hist`, `box`, `scatter` (with `x=`, `y=`), `area`, `pie`.

## Subplots dashboards and saving

```python
fig, axes = plt.subplots(2, 2, figsize=(11, 7), constrained_layout=True)
axes[0, 0].plot(...); axes[0, 1].barh(...); axes[1, 0].hist(...); axes[1, 1].scatter(...)
fig.suptitle("Sales overview", fontsize=15, weight="bold")
fig.savefig("overview.png", dpi=200, bbox_inches="tight")   # also .svg / .pdf for crisp vector output
```

## Design rules that make charts honest

| Rule | Why |
|---|---|
| Bars start at zero | Truncated bars exaggerate differences |
| Sort categories by value | Faster comparison |
| Title states the insight | "Tables lose money" beats "Profit by sub-category" |
| Label directly, remove chart junk | Fewer eye movements |
| One highlight colour, grey for context | Colour carries meaning |
| Colour-blind safe palettes (viridis, Okabe-Ito) | About 1 in 12 men are colour-blind |
| Same scale when comparing panels | Avoid misleading comparisons |
| Avoid 3-D and dual axes when possible | They distort perception |

## Summary

:::key
- Pick the chart from the question: trend → line, comparison → sorted bar, distribution → histogram/box, relationship → scatter, composition → stacked bar (pie only for a few parts).
- Use `fig, ax = plt.subplots()` and style the axes: titles, labels, limits, spines, legends, annotations.
- `plt.subplots(rows, cols)` builds small multiples; `fig.savefig(..., dpi=200, bbox_inches="tight")` exports.
- pandas `.plot()` is a fast start that returns a Matplotlib axes.
- Honest design: zero-based bars, sorted categories, insight titles, purposeful colour.
:::

:::quiz
Q: Which chart best shows a trend over 36 months?
- Pie
* Line
- Histogram
- Box plot
> Lines connect ordered time points.

Q: Which chart shows the distribution of one numeric variable?
- Scatter
* Histogram
- Pie
- Stacked bar
> Box and violin plots also work.

Q: What does `fig, ax = plt.subplots(1, 2)` create?
- One chart
* One figure with two axes side by side
- Two separate windows
- A 2 × 2 grid
> `ax` becomes an array of two axes.

Q: Why should bar charts start at zero?
- Matplotlib requires it
* Bar length encodes value; a cut axis exaggerates differences
- It looks better
- It saves space
> Line charts can zoom; bars should not.

Q: When is a pie chart acceptable?
- For 12 categories
* For a few parts of one whole, when exact comparison is not needed
- For trends
- Never
> Otherwise use bars.

Q: How do you save a sharp image without cut-off labels?
- `plt.show()`
* `fig.savefig("c.png", dpi=200, bbox_inches="tight")`
- Screenshot
- `fig.close()`
> SVG/PDF give vector output.
:::

:::exercise Chart practice
(1) Line chart of monthly profit with a horizontal line at zero. (2) Sorted horizontal bar of sales by state (top 10). (3) Histogram of `discount`. (4) Scatter of `discount` vs `profit` (what do you see?). (5) A 2 × 2 dashboard of these four charts saved as PNG.
???
```python
mp = s.set_index("order_date")["profit"].resample("ME").sum()
fig, axes = plt.subplots(2, 2, figsize=(11, 7), constrained_layout=True)
axes[0, 0].plot(mp.index, mp / 1e6); axes[0, 0].axhline(0, color="grey")
st = s.groupby("state")["sales"].sum().nlargest(10).sort_values(); axes[0, 1].barh(st.index, st / 1e6)
axes[1, 0].hist(s.discount, bins=9)
axes[1, 1].scatter(s.discount, s.profit, s=4, alpha=.3)   # profit falls as discount rises
fig.savefig("dashboard.png", dpi=150, bbox_inches="tight")
```
:::

:::interview Questions you may be asked
**Q: How do you choose a chart?**
Start from the question (trend, comparison, distribution, relationship, composition), the number of variables and the audience, then remove anything that does not help the message.

**Q: What makes a chart misleading?**
Truncated bar axes, inconsistent scales, 3-D effects, cherry-picked ranges, dual axes with arbitrary scaling, and areas that do not match values.

**Q: Matplotlib vs Seaborn vs Plotly?**
Matplotlib is the low-level foundation with full control; Seaborn adds statistical charts with good defaults on top; Plotly makes interactive web charts.
:::
