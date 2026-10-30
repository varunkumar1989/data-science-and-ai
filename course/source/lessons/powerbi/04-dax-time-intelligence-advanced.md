---
num: 4
title: DAX Time Intelligence, Ranking, Parameters & Dynamic Measures
live: "Power BI classes 3–4"
updated: "Power BI Desktop 2026 (field parameters, calculation groups, visual calculations)"
level: Advanced
duration: 150 min
summary: Make dashboards answer "compared with when?". Build year-to-date, month-to-date, same-period-last-year, month-on-month and year-on-year measures, rolling averages, rankings with RANKX and TOPN, what-if parameters, field parameters and dynamic measure switching, and know visual calculations and calculation groups.
datasets: [adventure_cycles/fact_sales.csv, adventure_cycles/dim_product.csv, adventure_cycles/dim_date.csv]
outcomes:
  - Explain what time intelligence needs (a marked date table) and use TOTALYTD, DATESYTD, SAMEPERIODLASTYEAR, DATEADD and PARALLELPERIOD
  - Build YoY %, MoM %, YTD, rolling 3-month and running-total measures
  - Rank items with RANKX and show the Top N with TOPN, including an "Others" bucket
  - Create what-if parameters and dynamic measure switching with field parameters
  - Describe calculation groups, visual calculations and DAX query view, and when to use them
---

## What time intelligence needs

Time-intelligence functions move or expand the **date filter**: "this year to date", "the same period last year". They only work when:

1. You have a **date table** with every date (Lesson 2),
2. it is **marked as a date table**, and
3. it is **related** to the fact table's date column.

Always use the **date table's** `Date` column inside time functions, never the fact table's date.

```python fig: Time intelligence changes the date filter, then CALCULATE re-evaluates the measure. SAMEPERIODLASTYEAR shifts the selected dates back exactly one year.
dg.flow(["Visual filter: Mar 2025", "SAMEPERIODLASTYEAR shifts dates", "Date filter becomes Mar 2024", "Total Sales evaluated for Mar 2024"], colors=[dg.VIO, dg.GOLD, dg.CORAL, dg.TEAL], title="How CALCULATE + time intelligence works")
```

## Core measures

```dax
Total Sales = SUM ( fact_sales[sales_amount] )

-- Cumulative totals
Sales YTD = TOTALYTD ( [Total Sales], dim_date[date] )
Sales QTD = TOTALQTD ( [Total Sales], dim_date[date] )
Sales MTD = TOTALMTD ( [Total Sales], dim_date[date] )
-- Indian financial year ending 31 March:
Sales FYTD = TOTALYTD ( [Total Sales], dim_date[date], "31-3" )

-- Previous periods
Sales LY    = CALCULATE ( [Total Sales], SAMEPERIODLASTYEAR ( dim_date[date] ) )
Sales PM    = CALCULATE ( [Total Sales], DATEADD ( dim_date[date], -1, MONTH ) )
Sales PQ    = CALCULATE ( [Total Sales], DATEADD ( dim_date[date], -1, QUARTER ) )

-- Growth
YoY %  = DIVIDE ( [Total Sales] - [Sales LY], [Sales LY] )
MoM %  = DIVIDE ( [Total Sales] - [Sales PM], [Sales PM] )
YoY Δ  = [Total Sales] - [Sales LY]
```

| Function | Returns | Notes |
|---|---|---|
| `TOTALYTD ( expr, dates, [year_end] )` | Year-to-date total | Shortcut for `CALCULATE ( expr, DATESYTD ( dates ) )` |
| `DATESYTD / DATESQTD / DATESMTD` | The date set from the period start to the last visible date | Use inside CALCULATE |
| `SAMEPERIODLASTYEAR ( dates )` | The selected dates shifted back one year | Needs continuous dates |
| `DATEADD ( dates, n, interval )` | Shift by n days, months, quarters or years | Month/quarter shifts handle month-end well |
| `PARALLELPERIOD ( dates, n, interval )` | The **full** period shifted (full month, quarter, year) | |
| `DATESBETWEEN ( dates, start, end )` | Custom ranges | |
| `DATESINPERIOD ( dates, end, -n, interval )` | Rolling window ending at `end` | Rolling 3/12 months |
| `PREVIOUSMONTH / PREVIOUSQUARTER / PREVIOUSYEAR` | Whole previous period | |
| `EOMONTH`, `EDATE`, `DATEDIFF` | Date arithmetic | |

Let's compute what these measures return for our data (monthly sales, year-to-date, last year and YoY):

```python run
import pandas as pd
D = "adventure_cycles/"
f = pd.read_csv(D + "fact_sales.csv", parse_dates=["order_date"]); p = pd.read_csv(D + "dim_product.csv")
f["ym"] = f.order_date.dt.to_period("M")
mth = f.groupby("ym").sales_amount.sum().to_frame("Total Sales")
mth["Sales PM"] = mth["Total Sales"].shift(1)
mth["MoM %"] = (mth["Total Sales"] / mth["Sales PM"] - 1) * 100
mth["Sales LY"] = mth["Total Sales"].shift(12)
mth["YoY %"] = (mth["Total Sales"] / mth["Sales LY"] - 1) * 100
mth["Sales YTD"] = mth.groupby(mth.index.year)["Total Sales"].cumsum()
out = mth[mth.index.year == 2025].copy()
out["Total Sales"] = (out["Total Sales"] / 1e6).round(1); out["Sales LY"] = (out["Sales LY"] / 1e6).round(1); out["Sales YTD"] = (out["Sales YTD"] / 1e6).round(1)
out[["Total Sales", "Sales LY", "YoY %", "MoM %", "Sales YTD"]].round(1).rename_axis("2025 month")
```

(Values in ₹ million.) In a Power BI matrix with `dim_date[month]` on rows and these measures in the Values area you would see exactly this.

```python fig: Monthly sales for 2025 against the same month in 2024, with year-to-date sales on the right axis. This is the classic "this year vs last year" chart.
import matplotlib.pyplot as plt, numpy as np
cur = mth[mth.index.year == 2025]["Total Sales"].values / 1e6; ly = mth[mth.index.year == 2024]["Total Sales"].values / 1e6
ytd = np.cumsum(cur)
fig, ax = plt.subplots(figsize=(10, 3.9)); x = np.arange(12); w = .38
ax.bar(x - w / 2, ly, w, color="#C9C3E6", label="2024"); ax.bar(x + w / 2, cur, w, color=dg.VIO, label="2025")
ax.set_xticks(x); ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]); ax.set_ylabel("Sales (₹ million)")
ax2 = ax.twinx(); ax2.plot(x, ytd, color=dg.CORAL, marker="o", lw=2, label="2025 YTD"); ax2.set_ylabel("YTD (₹ million)"); ax2.grid(False)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, ncol=3, loc="upper left"); ax.set_title("2025 vs 2024 and 2025 YTD")
fig
```

:::mistake Common time-intelligence bugs
- **Date table not marked / has gaps**: `SAMEPERIODLASTYEAR` returns blank or wrong values.
- **Using the fact table's date column** in the function: use `dim_date[date]`.
- **Comparing partial periods**: the current month has data for 10 days, last year's month has 31, so YoY looks terrible. Compare "to date" with `DATESYTD` and `SAMEPERIODLASTYEAR`, or restrict to complete months.
- **Fiscal year**: pass `"31-3"` as the year-end argument to `TOTALYTD`, and create `Fiscal Year` and `Fiscal Quarter` columns in the date table.
- **Showing a "last year" value in months with no data** (future months): wrap with `IF ( [Total Sales] <> BLANK (), … )`.
:::

## Rolling windows and running totals

```dax
-- Rolling 3-month sales ending at the last visible date
Sales Rolling 3M =
CALCULATE ( [Total Sales], DATESINPERIOD ( dim_date[date], MAX ( dim_date[date] ), -3, MONTH ) )

-- Rolling 3-month average of monthly sales (average over the months in the window)
Avg Monthly Sales R3M =
DIVIDE ( [Sales Rolling 3M], 3 )      -- valid once three full months exist in the window

-- Running total across all dates up to the current one
Sales Running Total =
CALCULATE ( [Total Sales], FILTER ( ALL ( dim_date[date] ), dim_date[date] <= MAX ( dim_date[date] ) ) )
```

In SQL this was `SUM() OVER (ORDER BY … ROWS BETWEEN …)` (SQL Lesson 12). DAX does the same thing by redefining the date filter.

```python run
mth["Rolling 3M"] = mth["Total Sales"].rolling(3).sum()
mth["Rolling 3M avg"] = mth["Total Sales"].rolling(3).mean()
(mth[["Total Sales", "Rolling 3M", "Rolling 3M avg"]].tail(6) / 1e6).round(1).rename_axis("month (₹ million)")
```

## Ranking: RANKX and TOPN

```dax
-- Rank of each product category by sales within the current context
Category Rank = RANKX ( ALL ( dim_product[category] ), [Total Sales], , DESC, DENSE )

-- Show only the top 5 products: sales of a product if it is in the top 5, else blank
Top 5 Product Sales =
VAR top5 = TOPN ( 5, ALL ( dim_product[product] ), [Total Sales], DESC )
RETURN CALCULATE ( [Total Sales], KEEPFILTERS ( top5 ) )

-- Everything outside the top 5, as one "Others" value
Others Sales = [Total Sales] - [Top 5 Product Sales]
```

For simple Top N visuals, you do not need DAX: in the **Filters pane**, choose the visual's field → Filter type **Top N** → Show items Top 5 → By value `Total Sales` → Apply filter. Use DAX when the Top N must respond to slicers in a custom way or you need an "Others" bar.

```python run
prod_sales = f.merge(p, on="product_key").groupby(["category", "product"]).sales_amount.sum().sort_values(ascending=False)
top5 = prod_sales.head(5)
print((top5 / 1e6).round(1).to_string())
print(f"\nTop 5 total : {top5.sum() / 1e6:,.1f} M   |   Others: {(prod_sales.sum() - top5.sum()) / 1e6:,.1f} M   |   Top 5 share: {top5.sum() / prod_sales.sum():.1%}")
```

## Parameters

### What-if parameter

**Modeling → New parameter → Numeric range**: name `Price Change %`, from −20 to +20, increment 1, default 0, and tick **Add slicer**. Power BI creates a table and a measure `Price Change % Value`. Use it in your own measure to simulate:

```dax
Simulated Sales = [Total Sales] * ( 1 + [Price Change % Value] / 100 )
Simulated Profit = [Simulated Sales] - [Total Cost]
```

Dragging the slicer instantly shows what profit would be with a 5% price increase (ignoring demand changes: always say so on the page).

```python run
base_sales, base_cost = f.sales_amount.sum(), f.total_cost.sum()
rows = [(chg, base_sales * (1 + chg / 100) / 1e6, (base_sales * (1 + chg / 100) - base_cost) / 1e6) for chg in (-10, -5, 0, 5, 10)]
pd.DataFrame(rows, columns=["Price change %", "Simulated sales (₹ M)", "Simulated profit (₹ M)"]).round(1)
```

### Power Query parameters

**Home → Manage parameters** creates parameters used inside queries, for example `StartDate` or a `ServerName`. Use them to switch between a test and a production database, or to filter large tables at load time. In the Service, parameters can be changed in dataset settings.

## Dynamic measure switching

A very popular pattern: a slicer that lets users choose which measure the chart shows (Sales, Profit, Orders).

**The modern way: Field parameters.** Modeling → **New parameter → Fields**: add `Total Sales`, `Total Profit`, `Orders`; tick **Add slicer**. Power BI creates a table with the three measures; use that table's field on a chart's axis or values and the slicer swaps the measure. A field parameter can also switch **axis** fields (Category, Country, Year).

**The classic way: a disconnected table + SWITCH.**

```dax
-- Table "Measure Selector" (Enter data): columns Measure Name, Sort
Selected Measure =
SWITCH (
    SELECTEDVALUE ( 'Measure Selector'[Measure Name], "Sales" ),
    "Sales",  [Total Sales],
    "Profit", [Total Profit],
    "Orders", [Orders]
)
```

Format strings can be dynamic too (Power BI 2024+ "dynamic format string"): thousands for sales, percentage for margin.

## KPI visuals and forecasting

- **KPI visual**: needs a value (indicator), a trend axis (date) and a target (for example last year's sales). Colours show good/bad.
- **Gauge**: current vs target; min/max/target set in the format pane.
- **Forecasting**: in a **line chart** with a date axis, Analytics pane → **Forecast** → set forecast length (for example 6 months), confidence interval (95%) and seasonality (12 points). Power BI uses exponential smoothing (ETS). It is a quick what-comes-next view, not a replacement for proper forecasting models (ML track).
- **Analytics pane** also offers constant lines, average, min/max, percentile lines, trend lines, and **anomaly detection**.

## Newer DAX features worth knowing

| Feature | What it is |
|---|---|
| **Calculation groups** | A reusable "time-intelligence switcher": define `Current`, `YTD`, `LY`, `YoY %` once and apply them to every measure (created in Tabular Editor or in the model view in recent versions) |
| **Visual calculations** | DAX written **inside a visual** that can refer to other fields in the visual (running sum, moving average, % of parent) with simple functions such as `RUNNINGSUM`, `MOVINGAVERAGE`, `PREVIOUS`, `FIRST` |
| **DAX query view** | `EVALUATE` queries to test and debug measures; Copilot can write DAX here |
| **User-defined functions (DAX UDFs)** | Reusable functions defined with the `FUNCTION` keyword (preview) |
| **INFO.\* functions** | Query model metadata (`INFO.TABLES()`, `INFO.MEASURES()`) |

```dax
-- Visual calculation (typed in the visual's formula bar)
Running Sales = RUNNINGSUM ( [Total Sales] )
Moving Avg 3  = MOVINGAVERAGE ( [Total Sales], 3 )
```

:::ai Do it with AI
Copilot can write time-intelligence measures from a sentence ("Show sales year to date versus last year"). It works best if the date table is marked, columns and tables have clear names, and you add **descriptions** to measures (Model view → Properties). Check the generated DAX uses your `dim_date[date]` (not the fact table's date), and confirm one value by hand.
:::

## Summary

:::key
- Time intelligence needs a **continuous, marked date table**, related to the fact; always reference the date table's column.
- `TOTALYTD`, `SAMEPERIODLASTYEAR`, `DATEADD`, `PARALLELPERIOD`, `DATESINPERIOD` build YTD, last-year, MoM, YoY and rolling windows; `DIVIDE ( current − previous, previous )` gives growth.
- `RANKX` ranks, `TOPN` selects the top items (add an "Others" measure); the Filters-pane **Top N** is the no-code route.
- **What-if parameters** simulate scenarios; **field parameters** let users switch measures or axes; the disconnected table + `SWITCH` pattern does the same in older models.
- Know calculation groups, visual calculations and the DAX query view for advanced work.
:::

:::quiz
Q: Which measure shows year-to-date sales?
- `SUM ( fact_sales[sales_amount] )`
* `TOTALYTD ( [Total Sales], dim_date[date] )`
- `SAMEPERIODLASTYEAR ( [Total Sales] )`
- `RANKX ( dim_date, [Total Sales] )`
> TOTALYTD accumulates from the start of the year to the current date.

Q: SAMEPERIODLASTYEAR returns blank for every month. What should you check first?
- The theme
* That the date table is continuous, marked as a date table and related to the fact
- The colour of the visual
- The number of slicers
> Time intelligence relies on a valid date table.

Q: Which formula gives month-on-month growth?
- `[Total Sales] - [Sales PM]`
* `DIVIDE ( [Total Sales] - [Sales PM], [Sales PM] )`
- `SUM ( [Sales PM] ) / [Total Sales]`
- `DATEADD ( [Total Sales], -1, MONTH )`
> Growth rate = (current − previous) ÷ previous, using DIVIDE.

Q: What does a field parameter let users do?
- Change the report theme
* Switch which measures or fields a visual shows with a slicer
- Refresh the data
- Create relationships
> Field parameters create a slicer that swaps fields in visuals.

Q: In the Indian financial year (April–March), how do you build YTD sales?
- `TOTALYTD ( [Total Sales], dim_date[date] )` always works
* `TOTALYTD ( [Total Sales], dim_date[date], "31-3" )`
- `DATESMTD`
- `PARALLELPERIOD ( … )`
> The third argument sets the year-end date.

Q: What is the correct way to compute "Others" after a Top 5?
- Add a second visual
* Total sales minus the Top 5 measure
- Use FILTER ALL
- Use PREVIOUSMONTH
> Others = overall total − Top N total.
:::

:::exercise Time-intelligence measures
For Adventure Cycles write measures for: (1) sales for the last 12 months ending at the selected date; (2) YoY % by category; (3) the best month of each year; (4) a what-if parameter "Discount %" from 0 to 30 that reduces `Total Sales` and shows simulated profit margin.
???
```dax
-- (1)
Sales L12M = CALCULATE ( [Total Sales], DATESINPERIOD ( dim_date[date], MAX ( dim_date[date] ), -12, MONTH ) )
-- (2) put dim_product[category] on rows and dim_date[year] on columns
YoY % = DIVIDE ( [Total Sales] - [Sales LY], [Sales LY] )
-- (3)
Best Month =
VAR t = ADDCOLUMNS ( VALUES ( dim_date[month] ), "@s", [Total Sales] )
RETURN MAXX ( TOPN ( 1, t, [@s], DESC ), dim_date[month] )
-- (4)  parameter table 'Discount %' with measure [Discount % Value]
Simulated Margin = DIVIDE ( [Total Sales] * ( 1 - [Discount % Value] / 100 ) - [Total Cost], [Total Sales] * ( 1 - [Discount % Value] / 100 ) )
```
Validate (2) and (3) against pandas group-bys.
:::

:::interview Questions you may be asked
**Q: What do you need for time-intelligence functions to work?**
A date table with continuous dates covering the data, marked as a date table, related to the fact table by date.

**Q: How would you calculate YoY growth?**
`Sales LY = CALCULATE ( [Total Sales], SAMEPERIODLASTYEAR ( dim_date[date] ) )` then `YoY % = DIVIDE ( [Total Sales] - [Sales LY], [Sales LY] )`.

**Q: How can users choose which metric a chart shows?**
Field parameters (modern) or a disconnected table with a `SWITCH ( SELECTEDVALUE (…), … )` measure.

**Q: How do you show Top N plus an "Others" bar?**
A Top N measure using TOPN/KEEPFILTERS and an Others measure = total − Top N.
:::
