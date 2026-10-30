---
num: 12
title: "Window Functions II: Running Totals, LEAD, LAG & Frames"
live: "SQL class 5–6"
updated: "SQL Server 2022, 2026"
level: Advanced
duration: 130 min
summary: Build time-series analytics in SQL. Use window frames (ROWS BETWEEN) for running totals and moving averages, LAG and LEAD for month-on-month and year-on-year growth, FIRST_VALUE and LAST_VALUE, cumulative percentages, PERCENT_RANK, CUME_DIST and PERCENTILE_CONT, and gaps-and-islands patterns.
datasets: [superstore_sales.csv, daily_sales.csv]
outcomes:
  - Define a window frame with ROWS BETWEEN and explain the default frame when ORDER BY is present
  - Calculate running totals, moving averages and cumulative shares
  - Compare each row with the previous or next row using LAG and LEAD (MoM, YoY, gaps)
  - Use FIRST_VALUE, LAST_VALUE and NTH_VALUE, PERCENT_RANK, CUME_DIST and PERCENTILE_CONT
  - Solve streak and gap problems with ROW_NUMBER differences
---

## Window frames

Inside `OVER`, `ORDER BY` defines the order and an optional **frame** defines *which rows around the current row* the function uses.

```sql
SUM(x) OVER (PARTITION BY p ORDER BY d
             ROWS BETWEEN <start> AND <end>)
```

| Frame boundary | Meaning |
|---|---|
| `UNBOUNDED PRECEDING` | From the first row of the partition |
| `n PRECEDING` | n rows before the current row |
| `CURRENT ROW` | The current row |
| `n FOLLOWING` | n rows after |
| `UNBOUNDED FOLLOWING` | To the last row of the partition |

```python fig: Frames relative to the current row (highlighted). A running total uses everything up to the current row; a 3-row moving average uses the previous two rows plus the current one.
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, axs = plt.subplots(3, 1, figsize=(9.5, 4.6), sharex=True)
titles = ["ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW  (running total)", "ROWS BETWEEN 2 PRECEDING AND CURRENT ROW  (3-row moving average)", "ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING  (centred window)"]
frames = [(0, 4), (2, 4), (3, 5)]
for ax, t, (a, b) in zip(axs, titles, frames):
    ax.set_xlim(-.3, 8.3); ax.set_ylim(0, 1); ax.axis("off"); ax.set_title(t, fontsize=9.5, loc="left")
    for i in range(8):
        inframe = a <= i <= b
        ax.add_patch(Rectangle((i, .1), .9, .7, fc=dg.SOFT[dg.VIO] if inframe else "white", ec=dg.VIO if inframe else "#CCC", lw=1.8 if inframe else 1))
        ax.text(i + .45, .45, f"row {i + 1}", ha="center", va="center", fontsize=9, weight="bold" if i == 4 else "normal", color=dg.INK)
    ax.add_patch(Rectangle((4, .1), .9, .7, fill=False, ec=dg.CORAL, lw=2.6))
fig
```

:::mistake The default frame trap
When `ORDER BY` is present and no frame is written, SQL Server uses `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. `RANGE` treats rows with the **same ORDER BY value** as peers and includes them all, which gives surprising results with ties, and `LAST_VALUE` then returns the current row's value. For running totals always write `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` explicitly; it is also much faster.
:::

## Running totals

First build the monthly sales table, then add a running (cumulative) total and a share:

```sql run rows=14
WITH monthly AS (
    SELECT YEAR(order_date) AS yr, MONTH(order_date) AS mth, SUM(sales) AS sales
    FROM superstore
    GROUP BY YEAR(order_date), MONTH(order_date)
)
SELECT yr, mth,
       ROUND(sales, 0) AS sales,
       ROUND(SUM(sales) OVER (PARTITION BY yr ORDER BY mth
                              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 0) AS ytd_sales,
       ROUND(100.0 * SUM(sales) OVER (PARTITION BY yr ORDER BY mth
                              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                   / SUM(sales) OVER (PARTITION BY yr), 1)                          AS ytd_pct_of_year
FROM monthly
ORDER BY yr, mth;
```

`PARTITION BY yr` restarts the running total every January (year-to-date). The percentage uses a second window (the whole year) as the denominator.

## Moving averages

A moving average smooths noisy data and shows the trend. Here is the 7-day average of daily units sold:

```sql run rows=8
SELECT date, units_sold,
       ROUND(AVG(units_sold * 1.0) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 1) AS avg_7_day
FROM daily_sales
WHERE date >= '2025-11-01'
ORDER BY date;
```

```python fig: Daily units sold and the 7-day and 28-day moving averages (last 6 months of 2025). The weekly pattern (weekend peaks) disappears in the averages; the 28-day line shows the trend.
import pandas as pd, matplotlib.pyplot as plt
d = pd.read_csv("daily_sales.csv", parse_dates=["date"]).set_index("date")
d["ma7"] = d.units_sold.rolling(7).mean(); d["ma28"] = d.units_sold.rolling(28).mean()
x = d["2025-07-01":]
fig, ax = plt.subplots(figsize=(10, 3.8)); ax.plot(x.index, x.units_sold, color="#C9C3E6", lw=1, label="Daily")
ax.plot(x.index, x.ma7, color=dg.VIO, lw=2, label="7-day average"); ax.plot(x.index, x.ma28, color=dg.CORAL, lw=2.4, label="28-day average"); ax.legend(ncol=3); ax.set_ylabel("Units sold"); ax.set_title("Moving averages smooth the noise")
fig
```

The first six rows of a 7-row window have fewer than seven rows available: SQL averages whatever exists (partial windows). Check `COUNT(*) OVER (...)` if you need to exclude them.

## LAG and LEAD: compare with previous and next rows

| Function | Returns |
|---|---|
| `LAG(col, n, default)` | The value n rows **before** the current row (default n = 1) |
| `LEAD(col, n, default)` | The value n rows **after** |

```sql run rows=12
WITH monthly AS (
    SELECT YEAR(order_date) * 100 + MONTH(order_date) AS ym, SUM(sales) AS sales
    FROM superstore
    GROUP BY YEAR(order_date) * 100 + MONTH(order_date)
)
SELECT ym,
       ROUND(sales, 0)                                               AS sales,
       ROUND(LAG(sales)  OVER (ORDER BY ym), 0)                      AS prev_month,
       ROUND(100.0 * (sales - LAG(sales) OVER (ORDER BY ym)) / LAG(sales) OVER (ORDER BY ym), 1) AS mom_pct,
       ROUND(LAG(sales, 12) OVER (ORDER BY ym), 0)                   AS same_month_last_year,
       ROUND(100.0 * (sales - LAG(sales, 12) OVER (ORDER BY ym)) / LAG(sales, 12) OVER (ORDER BY ym), 1) AS yoy_pct,
       ROUND(LEAD(sales) OVER (ORDER BY ym), 0)                      AS next_month
FROM monthly
ORDER BY ym;
```

- **MoM** compares with `LAG(sales, 1)`; **YoY** compares with `LAG(sales, 12)` when there is exactly one row per month. This is the SQL equivalent of the pivot table's "Difference From" settings (Excel Lesson 8).
- The first row has no previous value, so `LAG` returns NULL (or the default you supply: `LAG(sales, 1, 0)`).

:::warn Gaps in the data
`LAG(sales, 12)` assumes every month exists. If a month has no sales it also has no row, so LAG(12) points at the wrong month. Build a calendar table (a list of every month) and LEFT JOIN the sales onto it first.
:::

### Time between events

"How many days passed between each customer's consecutive orders?"

```sql run
WITH o AS (
    SELECT customer_id, order_date,
           LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order
    FROM orders
)
SELECT COUNT(*)                                          AS repeat_orders,
       ROUND(AVG(DATEDIFF(day, prev_order, order_date) * 1.0), 1) AS avg_days_between_orders,
       MIN(DATEDIFF(day, prev_order, order_date))        AS shortest_gap,
       MAX(DATEDIFF(day, prev_order, order_date))        AS longest_gap
FROM o
WHERE prev_order IS NOT NULL;
```

## FIRST_VALUE, LAST_VALUE, NTH_VALUE

```sql run rows=8
SELECT department, emp_id, monthly_income,
       FIRST_VALUE(emp_id) OVER (PARTITION BY department ORDER BY monthly_income DESC)               AS top_earner,
       LAST_VALUE(emp_id)  OVER (PARTITION BY department ORDER BY monthly_income DESC
                                 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)             AS lowest_earner,
       monthly_income - FIRST_VALUE(monthly_income) OVER (PARTITION BY department ORDER BY monthly_income DESC) AS gap_to_top
FROM employees
ORDER BY department, monthly_income DESC;
```

`LAST_VALUE` needs the explicit full frame (`UNBOUNDED FOLLOWING`); with the default frame it just returns the current row.

## Distribution functions

| Function | Meaning |
|---|---|
| `PERCENT_RANK()` | (rank − 1) ÷ (rows − 1): 0 for the lowest, 1 for the highest |
| `CUME_DIST()` | Share of rows with a value ≤ the current one |
| `PERCENTILE_CONT(p) WITHIN GROUP (ORDER BY x) OVER (…)` | Interpolated percentile (e.g. median at p = 0.5) |
| `PERCENTILE_DISC(p) …` | An actual value from the data |

```sql run
SELECT DISTINCT department,
       ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY monthly_income) OVER (PARTITION BY department), 0) AS median_income,
       ROUND(AVG(monthly_income) OVER (PARTITION BY department), 0)                                          AS mean_income
FROM employees
ORDER BY department;
```

In SQL Server, `PERCENTILE_CONT` is a window function (needs `OVER`); PostgreSQL uses it as an aggregate (`GROUP BY`). Mean above median is the signature of a right-skewed distribution (Statistics, ML track).

## Cumulative share: the Pareto in SQL

Which products produce the first 80% of sales?

```sql run rows=8
WITH p AS (
    SELECT product_id, SUM(sales) AS sales FROM order_items GROUP BY product_id
), c AS (
    SELECT product_id, sales,
           SUM(sales) OVER (ORDER BY sales DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) * 1.0 / SUM(sales) OVER () AS cum_share,
           ROW_NUMBER() OVER (ORDER BY sales DESC) AS rnk
    FROM p
)
SELECT COUNT(*) AS products_for_80pct_of_sales,
       (SELECT COUNT(*) FROM p)  AS total_products
FROM c
WHERE cum_share <= 0.8;
```

## Gaps and islands: streaks

A classic: find runs of consecutive days. The trick is that `date − ROW_NUMBER()` is **constant within a streak**.

```sql run
WITH days AS (
    SELECT DISTINCT order_date AS d FROM orders WHERE order_date >= '2025-12-01'
), g AS (
    SELECT d, DATEADD(day, -ROW_NUMBER() OVER (ORDER BY d), d) AS grp FROM days
)
SELECT MIN(d) AS streak_start, MAX(d) AS streak_end, COUNT(*) AS days_in_streak
FROM g
GROUP BY grp
ORDER BY streak_start;
```

Each group of consecutive order days becomes one row: all of December 2025 had orders every day, so there is a single streak. The same pattern finds consecutive login days, uninterrupted employment spells and missing-sequence ranges.

## Summary

:::key
- **Frames** (`ROWS BETWEEN … AND …`) choose the rows around the current row; always write `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` for running totals (the default RANGE frame includes ties).
- Running totals, YTD, cumulative % and moving averages use aggregate functions with frames.
- `LAG`/`LEAD` read the previous/next row (MoM, YoY, time between events); fill calendar gaps first.
- `FIRST_VALUE`/`LAST_VALUE` need an explicit full frame for LAST_VALUE.
- `PERCENT_RANK`, `CUME_DIST`, `PERCENTILE_CONT` describe position and median within a distribution.
- Gaps and islands: `value − ROW_NUMBER()` is constant within a consecutive run.
:::

:::quiz
Q: Which frame gives a 3-month moving average (current and two previous rows)?
- `ROWS BETWEEN 3 PRECEDING AND CURRENT ROW`
* `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`
- `ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING`
- `RANGE 3`
> Two preceding rows plus the current row make three rows.

Q: What does `LAG(sales, 12) OVER (ORDER BY ym)` return for monthly data?
- Sales 12 months in the future
* Sales for the same month last year (if no month is missing)
- The 12th highest sales
- The average of 12 months
> LAG reads n rows back; with one row per month that is 12 months earlier.

Q: Why does LAST_VALUE often return the current row's value?
* The default frame ends at the current row, so you must extend it to UNBOUNDED FOLLOWING
- LAST_VALUE is broken in SQL Server
- It only works with PARTITION BY
- ORDER BY is missing
> Specify ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING.

Q: How do you restart a running total every year?
- ORDER BY year
* PARTITION BY year in the OVER clause
- GROUP BY year only
- Use LAG
> Each partition has its own running total.

Q: In the gaps-and-islands trick, what stays constant inside a streak of consecutive dates?
- The date
- The row number
* The date minus its ROW_NUMBER
- The count
> Both increase by 1 per row, so their difference is constant.

Q: Mean income is much higher than median income. What does that suggest?
- Symmetric data
* A right-skewed distribution with a few very high values
- Missing data
- A data error
> A long right tail pulls the mean above the median.
:::

:::exercise Time-series practice
(1) Monthly sales per region with MoM %; (2) for each customer, the days since their previous order and a flag for "returned within 30 days"; (3) a 3-month moving average of sales by category; (4) the month when cumulative 2025 sales first exceeded ₹5 crore.
???
```sql
-- (1)
WITH m AS (SELECT region, YEAR(order_date)*100+MONTH(order_date) AS ym, SUM(sales) AS sales FROM superstore GROUP BY region, YEAR(order_date)*100+MONTH(order_date))
SELECT region, ym, ROUND(sales,0) AS sales,
       ROUND(100.0*(sales - LAG(sales) OVER (PARTITION BY region ORDER BY ym)) / LAG(sales) OVER (PARTITION BY region ORDER BY ym), 1) AS mom_pct FROM m ORDER BY region, ym;
-- (2)
WITH o AS (SELECT customer_id, order_date, LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev FROM orders)
SELECT customer_id, order_date, DATEDIFF(day, prev, order_date) AS days_since_prev,
       CASE WHEN DATEDIFF(day, prev, order_date) <= 30 THEN 1 ELSE 0 END AS within_30_days FROM o WHERE prev IS NOT NULL;
-- (3)
WITH m AS (SELECT category, YEAR(order_date)*100+MONTH(order_date) AS ym, SUM(sales) AS sales FROM superstore GROUP BY category, YEAR(order_date)*100+MONTH(order_date))
SELECT category, ym, AVG(sales) OVER (PARTITION BY category ORDER BY ym ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS ma3 FROM m;
-- (4)
WITH m AS (SELECT MONTH(order_date) AS mth, SUM(sales) AS sales FROM superstore WHERE YEAR(order_date) = 2025 GROUP BY MONTH(order_date)),
     c AS (SELECT mth, SUM(sales) OVER (ORDER BY mth ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum FROM m)
SELECT TOP 1 mth FROM c WHERE cum > 50000000 ORDER BY mth;
```
:::

:::interview Questions you may be asked
**Q: How do you calculate a running total in SQL?**
`SUM(x) OVER (ORDER BY d ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`, optionally partitioned.

**Q: How do you calculate month-on-month growth?**
Aggregate to months, then `(sales − LAG(sales) OVER (ORDER BY month)) / LAG(sales) OVER (ORDER BY month)`; use `LAG(…, 12)` for YoY.

**Q: ROWS vs RANGE in a window frame?**
ROWS counts physical rows; RANGE includes all rows with the same ORDER BY value as the current row (peers). ROWS is predictable and faster.

**Q: How would you find consecutive login days?**
Gaps and islands: `date − ROW_NUMBER() OVER (PARTITION BY user ORDER BY date)` as a group key, then GROUP BY it.
:::
