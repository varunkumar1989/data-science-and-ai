---
num: 7
title: GROUP BY, HAVING, CASE WHEN, ROLLUP, CUBE & COALESCE
live: "SQL class 4 · SQL–Power BI bridge"
updated: "SQL Server 2022, 2026"
level: Intermediate
duration: 130 min
summary: Turn rows into business summaries. Group with GROUP BY, filter groups with HAVING, create conditional columns and buckets with CASE WHEN, pivot data with conditional aggregation, and add subtotals and grand totals with ROLLUP, CUBE and GROUPING SETS, cleaning the labels with COALESCE and GROUPING().
datasets: [superstore_sales.csv, hr_employees.csv]
outcomes:
  - Summarise data by one or more columns with GROUP BY and aggregate functions
  - Filter groups with HAVING and explain WHERE vs HAVING
  - Create conditional columns and buckets with CASE WHEN … THEN … ELSE … END
  - Build pivot-style reports with conditional aggregation
  - Add subtotals and grand totals with ROLLUP, CUBE and GROUPING SETS, and label them with COALESCE and GROUPING()
---

## GROUP BY: one row per group

`GROUP BY` collapses rows that share the same value(s) into one row, and aggregate functions summarise each group. It is the SQL version of a pivot table (Excel Lesson 8) and of `groupby()` in pandas.

```python fig: GROUP BY region: rows with the same region are collected into one group, then SUM is computed for each group.
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(10, 3.6)); ax.axis("off"); ax.set_xlim(0, 10.5); ax.set_ylim(0, 4.2)
rows = [("North", 120), ("South", 80), ("North", 60), ("West", 90), ("South", 40), ("North", 30)]
cols = {"North": dg.VIO, "South": dg.TEAL, "West": dg.CORAL}
for i, (r, v) in enumerate(rows):
    y = 3.5 - i * .55
    ax.add_patch(Rectangle((.3, y), 1.4, .5, fc=dg.SOFT[cols[r]], ec="#ccc")); ax.text(.4, y + .25, r, va="center")
    ax.add_patch(Rectangle((1.7, y), 1.0, .5, fc="white", ec="#ccc")); ax.text(2.6, y + .25, v, va="center", ha="right")
ax.text(1.5, 4.15, "superstore rows", ha="center", weight="bold")
ax.annotate("", xy=(4.6, 2.2), xytext=(3.0, 2.2), arrowprops=dict(arrowstyle="-|>", lw=2, color="#888")); ax.text(3.8, 2.45, "GROUP BY region", ha="center", fontsize=9.5)
tot = {"North": 210, "South": 120, "West": 90}
for i, (r, v) in enumerate(tot.items()):
    y = 2.9 - i * .7
    ax.add_patch(Rectangle((5.0, y), 1.6, .6, fc=dg.SOFT[cols[r]], ec=cols[r], lw=1.5)); ax.text(5.1, y + .3, r, va="center", weight="bold")
    ax.add_patch(Rectangle((6.6, y), 1.3, .6, fc="white", ec=cols[r], lw=1.5)); ax.text(7.8, y + .3, v, va="center", ha="right", weight="bold")
ax.text(6.45, 3.75, "SUM(sales) per group", ha="center", weight="bold")
fig
```

```sql run
SELECT region,
       COUNT(DISTINCT order_id)              AS orders,
       ROUND(SUM(sales), 0)                  AS sales,
       ROUND(SUM(profit), 0)                 AS profit,
       ROUND(100.0 * SUM(profit) / SUM(sales), 1) AS margin_pct
FROM superstore
GROUP BY region
ORDER BY sales DESC;
```

### Grouping by several columns

```sql run rows=12
SELECT category,
       sub_category,
       COUNT(*)              AS lines,
       ROUND(SUM(sales), 0)  AS sales,
       ROUND(SUM(profit), 0) AS profit
FROM superstore
GROUP BY category, sub_category
ORDER BY category, sales DESC;
```

### Grouping by an expression

```sql run
SELECT YEAR(order_date)       AS order_year,
       COUNT(DISTINCT order_id) AS orders,
       ROUND(SUM(sales), 0)   AS sales
FROM superstore
GROUP BY YEAR(order_date)
ORDER BY order_year;
```

:::warn The golden rule of GROUP BY
Every column in `SELECT` must either be **in the GROUP BY** or **inside an aggregate function**. `SELECT region, city, SUM(sales) FROM superstore GROUP BY region` fails in SQL Server: "Column 'city' is invalid in the select list because it is not contained in either an aggregate function or the GROUP BY clause." Which city should it show for the North group? SQL refuses to guess.
:::

## HAVING: filtering groups

`WHERE` filters **rows before** grouping; `HAVING` filters **groups after** aggregation.

```sql run
SELECT city,
       COUNT(DISTINCT order_id) AS orders,
       ROUND(SUM(profit), 0)    AS profit
FROM superstore
WHERE category = 'Furniture'          -- 1. keep only furniture rows
GROUP BY city                         -- 2. one row per city
HAVING SUM(profit) < 0                -- 3. keep only loss-making cities
ORDER BY profit;
```

| | WHERE | HAVING |
|---|---|---|
| Runs | Before GROUP BY | After GROUP BY |
| Filters | Individual rows | Groups |
| Can use aggregates | No | Yes |
| Example | `WHERE region = 'West'` | `HAVING COUNT(*) > 100` |
| Performance | Reduces rows early (faster) | Applied to fewer, summarised rows |

:::tip Filter as early as possible
Put conditions that do not need aggregates in `WHERE`, not `HAVING`: `HAVING region = 'West'` works but makes the database group every region first and discard most of them.
:::

## CASE WHEN: conditional columns

`CASE` is SQL's IF/IFS (Excel Lesson 5). It returns a value for the first condition that is true.

```sql
CASE
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    ELSE default_result          -- optional; without ELSE, unmatched rows get NULL
END
```

```sql run rows=8
SELECT order_id, sales, discount, profit,
       CASE
           WHEN discount = 0    THEN 'No discount'
           WHEN discount <= 0.2 THEN 'Up to 20%'
           ELSE 'Above 20%'
       END AS discount_band,
       CASE WHEN profit < 0 THEN 'Loss' ELSE 'Profit' END AS result
FROM superstore
ORDER BY row_id;
```

The **simple** form compares one expression with values:

```sql
CASE ship_mode
    WHEN 'Same Day'    THEN 1
    WHEN 'First Class' THEN 2
    ELSE 3
END
```

### CASE inside GROUP BY: buckets

```sql run
SELECT CASE
           WHEN discount = 0    THEN '0%'
           WHEN discount <= 0.2 THEN '1–20%'
           ELSE '>20%'
       END                                        AS discount_band,
       COUNT(*)                                   AS lines,
       ROUND(SUM(sales), 0)                       AS sales,
       ROUND(SUM(profit), 0)                      AS profit,
       ROUND(100.0 * SUM(profit) / SUM(sales), 1) AS margin_pct
FROM superstore
GROUP BY CASE
             WHEN discount = 0    THEN '0%'
             WHEN discount <= 0.2 THEN '1–20%'
             ELSE '>20%'
         END
ORDER BY discount_band;
```

The same insight as the Excel crosstab and dashboard: discounts above 20% turn the margin sharply negative.

### Conditional aggregation: pivoting with CASE

Put `CASE` inside an aggregate to turn row values into columns, which is how analysts build pivot-style reports in SQL:

```sql run
SELECT region,
       ROUND(SUM(CASE WHEN category = 'Furniture'       THEN sales ELSE 0 END), 0) AS furniture,
       ROUND(SUM(CASE WHEN category = 'Office Supplies' THEN sales ELSE 0 END), 0) AS office_supplies,
       ROUND(SUM(CASE WHEN category = 'Technology'      THEN sales ELSE 0 END), 0) AS technology,
       ROUND(SUM(sales), 0)                                                        AS total
FROM superstore
GROUP BY region
ORDER BY region;
```

```sql run
SELECT department,
       COUNT(*)                                                 AS employees,
       SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END)        AS leavers,
       ROUND(100.0 * SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS attrition_pct,
       ROUND(AVG(CASE WHEN overtime = 'Yes' THEN 1.0 ELSE 0 END) * 100, 1)              AS overtime_pct
FROM employees
GROUP BY department
ORDER BY attrition_pct DESC;
```

`AVG(CASE WHEN … THEN 1.0 ELSE 0 END)` is a neat way to get a percentage of rows meeting a condition.

:::note The PIVOT operator
SQL Server also has a `PIVOT` operator:
```sql
SELECT region, [Furniture], [Office Supplies], [Technology]
FROM (SELECT region, category, sales FROM superstore) AS src
PIVOT (SUM(sales) FOR category IN ([Furniture], [Office Supplies], [Technology])) AS p;
```
Conditional aggregation is more flexible (several measures, any conditions) and works in every database, so most analysts prefer it. `UNPIVOT` does the reverse, like Power Query's Unpivot (Excel Lesson 12).
:::

## Subtotals and grand totals: ROLLUP, CUBE, GROUPING SETS

### ROLLUP

`GROUP BY ROLLUP (a, b)` returns the groups for `(a, b)`, **subtotals** for each `a`, and a **grand total**. Subtotal rows show NULL in the rolled-up columns.

```sql run rows=20
SELECT region,
       category,
       ROUND(SUM(sales), 0) AS sales
FROM superstore
GROUP BY ROLLUP (region, category)
ORDER BY region, category;
```

### Cleaning the labels with COALESCE and GROUPING()

NULLs in subtotal rows are confusing. `COALESCE` replaces them with a label. If the data itself could contain NULL categories, use `GROUPING(col)`, which returns 1 only on rows where the column was rolled up:

```sql run rows=20
SELECT CASE WHEN GROUPING(region) = 1 THEN 'All regions' ELSE region END            AS region,
       CASE WHEN GROUPING(category) = 1 THEN 'Subtotal' ELSE category END            AS category,
       ROUND(SUM(sales), 0)                                                          AS sales
FROM superstore
GROUP BY ROLLUP (region, category)
ORDER BY GROUPING(region), region, GROUPING(category), category;
```

The simple version used in class, `COALESCE(region, 'All regions')`, gives the same labels when the data has no real NULLs.

### CUBE

`CUBE (a, b)` returns **every combination** of subtotals: by `(a, b)`, by `a`, by `b`, and the grand total. Use it when you need totals in both directions, like a pivot table with row and column grand totals.

```sql run rows=25
SELECT COALESCE(segment, 'All segments')  AS segment,
       COALESCE(region, 'All regions')    AS region,
       COUNT(DISTINCT order_id)           AS orders
FROM superstore
GROUP BY CUBE (segment, region)
ORDER BY GROUPING(segment), segment, GROUPING(region), region;
```

### GROUPING SETS

`GROUPING SETS` lists exactly the groupings you want in one query:

```sql run
SELECT COALESCE(category, '—')   AS category,
       COALESCE(ship_mode, '—')  AS ship_mode,
       ROUND(SUM(sales), 0)      AS sales
FROM superstore
GROUP BY GROUPING SETS ((category), (ship_mode), ())
ORDER BY category, ship_mode;
```

This returns totals by category, totals by ship mode and the grand total, without the category × ship mode detail.

| Syntax | Groupings produced for (a, b) |
|---|---|
| `GROUP BY a, b` | (a, b) |
| `ROLLUP (a, b)` | (a, b), (a), () |
| `CUBE (a, b)` | (a, b), (a), (b), () |
| `GROUPING SETS ((a), (b), ())` | exactly (a), (b), () |

:::tip Bridge to Power BI
Power BI matrices compute these subtotals automatically, but ROLLUP/CUBE are perfect when you must deliver a fixed report table from SQL, feed a paginated report, or check that a dashboard's totals are right.
:::

## A complete analysis query

Question: *"For 2025, show each sub-category's sales, profit and margin, a performance label, and only sub-categories with at least ₹10 lakh sales, best margin first."*

```sql run
SELECT sub_category,
       ROUND(SUM(sales), 0)                          AS sales,
       ROUND(SUM(profit), 0)                         AS profit,
       ROUND(100.0 * SUM(profit) / SUM(sales), 1)    AS margin_pct,
       CASE
           WHEN SUM(profit) < 0                       THEN 'Loss-making'
           WHEN 100.0 * SUM(profit) / SUM(sales) < 8  THEN 'Low margin'
           ELSE 'Healthy'
       END                                           AS status
FROM superstore
WHERE order_date >= '2025-01-01' AND order_date < '2026-01-01'
GROUP BY sub_category
HAVING SUM(sales) >= 1000000
ORDER BY margin_pct DESC;
```

## Summary

:::key
- `GROUP BY` makes one row per group; every selected column must be grouped or aggregated.
- `WHERE` filters rows before grouping; `HAVING` filters groups after (can use aggregates).
- `CASE WHEN … THEN … ELSE … END` creates conditional columns and buckets; without ELSE, unmatched rows are NULL.
- Conditional aggregation (`SUM(CASE WHEN … THEN x ELSE 0 END)`) pivots rows into columns and computes percentages.
- `ROLLUP` adds hierarchical subtotals + grand total; `CUBE` adds all combinations; `GROUPING SETS` picks exactly the groupings you need.
- Label subtotal rows with `COALESCE` or, more robustly, `GROUPING()`.
:::

:::quiz
Q: Why does `SELECT region, city, SUM(sales) FROM superstore GROUP BY region` fail?
- SUM needs a WHERE clause
* city is neither grouped nor aggregated
- region must be aggregated
- GROUP BY needs ORDER BY
> Every selected column must appear in GROUP BY or in an aggregate.

Q: Which clause keeps only customers with more than 10 orders?
- `WHERE COUNT(order_id) > 10`
* `HAVING COUNT(DISTINCT order_id) > 10`
- `ORDER BY COUNT(*) > 10`
- `GROUP BY COUNT(*) > 10`
> Conditions on aggregates go in HAVING.

Q: What does a CASE expression return when no WHEN matches and there is no ELSE?
- 0
- An empty string
* NULL
- An error
> Without ELSE, unmatched rows return NULL.

Q: `GROUP BY ROLLUP (region, category)` produces which groupings?
* (region, category), (region), and the grand total
- Every combination including (category) alone
- Only the grand total
- Only (region, category)
> ROLLUP is hierarchical; CUBE would also include (category).

Q: What does `AVG(CASE WHEN attrition = 'Yes' THEN 1.0 ELSE 0 END)` compute?
- The number of leavers
* The share (proportion) of employees who left
- The average salary of leavers
- NULL
> The average of 1s and 0s is the proportion of 1s.

Q: Which function tells you that a row is a subtotal created by ROLLUP?
- COALESCE
- ISNULL
* GROUPING
- NULLIF
> GROUPING(col) returns 1 when col was aggregated away in that row.
:::

:::exercise HR summary
Using the `employees` table (HR data): (1) headcount, average monthly income and attrition % by department and gender, only for groups with at least 30 employees; (2) a column per education level showing headcount, one row per department; (3) average income by job satisfaction (1–4) with a grand total row using ROLLUP.
???
```sql
-- (1)
SELECT department, gender, COUNT(*) AS headcount,
       ROUND(AVG(monthly_income * 1.0), 0) AS avg_income,
       ROUND(100.0 * SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS attrition_pct
FROM employees GROUP BY department, gender HAVING COUNT(*) >= 30 ORDER BY department, gender;
-- (2)
SELECT department,
       SUM(CASE WHEN education = 'Diploma'    THEN 1 ELSE 0 END) AS diploma,
       SUM(CASE WHEN education = 'Bachelor''s' THEN 1 ELSE 0 END) AS bachelors,
       SUM(CASE WHEN education = 'Master''s'   THEN 1 ELSE 0 END) AS masters,
       SUM(CASE WHEN education = 'PhD'        THEN 1 ELSE 0 END) AS phd
FROM employees GROUP BY department;
-- (3)
SELECT COALESCE(CAST(job_satisfaction AS VARCHAR(5)), 'All') AS satisfaction,
       ROUND(AVG(monthly_income * 1.0), 0) AS avg_income
FROM employees GROUP BY ROLLUP (job_satisfaction) ORDER BY GROUPING(job_satisfaction), job_satisfaction;
```
Note the doubled apostrophe in `'Bachelor''s'`: that is how you write a quote inside a SQL string.
:::

:::interview Questions you may be asked
**Q: WHERE vs HAVING?**
WHERE filters rows before aggregation and cannot use aggregate functions; HAVING filters groups after GROUP BY and can.

**Q: How do you pivot rows to columns in SQL?**
Conditional aggregation `SUM(CASE WHEN col = 'X' THEN value END)` per output column, or SQL Server's PIVOT operator.

**Q: What are ROLLUP and CUBE?**
GROUP BY extensions that add subtotal and grand-total rows: ROLLUP follows the column hierarchy; CUBE produces all combinations. GROUPING() identifies the subtotal rows.

**Q: Write a query to find the second-highest salary per department.**
Use DENSE_RANK() in a subquery/CTE (Lesson 11): `WHERE rnk = 2`.
:::
