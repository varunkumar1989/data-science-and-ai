---
num: 4
title: "Filters, Parameters, Sets, Groups and Hierarchies in Tableau"
updated: "Tableau Desktop / Tableau Public 2026"
level: Intermediate
duration: 120 min
summary: Control what a view shows and let users interact with it. Learn every filter type and where it sits in the order of operations, context filters and Top N, groups, hierarchies, bins, sets (fixed, conditional, top) and combined sets, and parameters for dynamic Top N, measure swapping and what-if analysis.
datasets: [superstore_sales.csv]
outcomes:
  - Use dimension, measure, date, context, data-source and table-calculation filters correctly
  - Build hierarchies and groups, and explain groups vs sets
  - Create fixed, conditional and Top N sets and use IN/OUT in calculations
  - Create parameters for Top N, measure selection and what-if discount scenarios
  - Combine filters, sets and parameters into interactive views
---

## Filters

| Filter | How | Notes |
|---|---|---|
| **Dimension** filter | Drag a dimension to Filters → General / Wildcard / Condition / Top tabs | e.g. Region = South |
| **Measure** filter | Drag a measure to Filters → choose aggregation → range | e.g. SUM(Profit) < 0 (loss-making items) |
| **Date** filter | Relative dates (last 3 months), range of dates, or discrete years/months | Relative dates update automatically |
| **Context** filter | Right-click a filter → Add to Context (grey pill) | Runs first; Top N and FIXED LODs respect it |
| **Data source** filter | Data Source page → Filters → Add | Applies to every sheet; good for security and speed |
| **Extract** filter | When creating an extract | Shrinks the extract itself |
| **Table-calc** filter | Filter on a table calc such as `LAST()=0` or rank | Hides marks without changing other calculations |

**Show Filter** (right-click the pill → Show Filter) puts an interactive control on the sheet: single value list, dropdown, multiple values, slider, wildcard match. **Apply to Worksheets → All Using This Data Source / Selected Worksheets** makes one filter drive several sheets on a dashboard.

```python run
import pandas as pd, numpy as np
df = pd.read_csv("superstore_sales.csv", parse_dates=["order_date"])
loss = df.groupby("sub_category").profit.sum().sort_values()
print("Loss-making sub-categories (measure filter SUM(Profit) < 0):")
print((loss[loss < 0] / 1e5).round(1))
```

### Top N and context

Top N is computed **after** context filters but **before** ordinary dimension filters. So "Top 5 products **in the South**" needs the Region filter in context; otherwise Tableau finds the national Top 5 first and then keeps only those that happen to be in the South.

```python run
top_all = df.groupby("product_name").sales.sum().nlargest(5)
south = df[df.region == "South"]
top_south = south.groupby("product_name").sales.sum().nlargest(5)
print("National top 5:", list(top_all.index))
print("South top 5 (Region in context):", list(top_south.index))
print("Overlap:", len(set(top_all.index) & set(top_south.index)), "of 5")
```

## Hierarchies, groups and bins

- **Hierarchy**: drag Sub-Category onto Category in the Data pane → name it "Product hierarchy". A **+** on the pill drills down. Date fields have a built-in Year → Quarter → Month → Day hierarchy.
- **Group**: select marks or right-click a field → Create → Group, e.g. group Indian states into "North-East". A group is a new dimension; its members are fixed.
- **Bins**: equal-width buckets of a measure (Lesson 2).

## Sets

A **set** is a subset of a dimension that is either **IN** or **OUT**.

| Set type | Created by | Example |
|---|---|---|
| Fixed (manual) | Select members | Six key accounts |
| Conditional | Condition tab, e.g. SUM(Profit) > 0 | Profitable customers |
| Top | Top tab, e.g. Top 10 by SUM(Sales) | Top 10 customers |
| Combined | Two sets → Create Combined Set (union, intersection, difference) | Top customers who are also unprofitable |

Use a set on **Color** to show IN vs OUT, on Filters to keep only members, or in calculations: `IF [Top Customers] THEN [Sales] END`. **Set actions** (Lesson 6) let users change a set by clicking marks.

```python run
cust = df.groupby("customer_id").agg(sales=("sales", "sum"), profit=("profit", "sum"))
top10 = cust.sales.nlargest(10).index
in_set = cust.index.isin(top10)
print(f"Top 10 customers (IN): {cust.sales[in_set].sum() / cust.sales.sum():.1%} of sales")
unprofitable = cust.index[cust.profit < 0]
print("Customers in Top 10 AND unprofitable (combined set, intersection):", len(set(top10) & set(unprofitable)))
print("All unprofitable customers:", len(unprofitable), "of", len(cust))
```

:::note Groups vs sets
A **group** combines members into new categories (many buckets, fixed). A **set** splits a dimension into IN/OUT, can be dynamic (conditional or Top N) and can be changed by users with set actions.
:::

## Parameters

A **parameter** is a single user-controlled value (number, string, date or list) that does nothing until a calculation, filter or reference line uses it. Right-click → **Show Parameter**.

### 1. Dynamic Top N

1. Create parameter **Top N** (integer, range 5–20, step 5).
2. Product Name filter → Top tab → By field → Top **[Top N]** by SUM(Sales).
3. Show the parameter: users choose 5, 10, 15 or 20.

### 2. Measure swap

```
// Parameter "Choose measure": list of strings Sales, Profit, Quantity
CASE [Choose measure]
WHEN "Sales" THEN SUM([Sales])
WHEN "Profit" THEN SUM([Profit])
WHEN "Quantity" THEN SUM([Quantity])
END
```

Put this calculated field on the axis; one chart now shows whichever measure the user picks. Use a dynamic title: `<Parameters.Choose measure> by Region`.

### 3. What-if: extra discount

```
// Parameter "Extra discount" : float 0.00–0.20
[Sales] * (1 - [Extra discount])                     // projected sales
[Profit] - [Sales] * [Extra discount]                // projected profit
```

```python run
for extra in (0, .05, .10):
    proj_profit = (df.profit - df.sales * extra).sum()
    print(f"extra discount {extra:.0%}: projected profit ₹{proj_profit / 1e7:.2f} crore")
```

With margins around 9%, a further 10% discount turns the whole business loss-making. That is exactly the kind of insight a what-if parameter makes obvious to a manager.

:::new Dynamic parameters and zone visibility
Parameters can refresh their list and default value from a field when the workbook opens (*When workbook opens → value of field*). Combined with **dynamic zone visibility** (show or hide a dashboard container based on a boolean field or parameter), they power menus and drill-in panels without bookmarks.
:::

## Summary

:::key
- Pick the right filter level: data source → context → dimension → measure → table calc.
- Top N and FIXED LODs ignore normal dimension filters unless those filters are in context.
- Groups make fixed buckets; sets make IN/OUT subsets that can be dynamic and combined.
- Parameters are user inputs: wire them into filters, calculations, titles and reference lines.
:::

:::quiz
Q: You need "Top 10 products within the selected region". What must you do?
* Add the Region filter to context
- Use a measure filter
- Use a group
- Hide the other regions
> Top N runs before normal dimension filters.

Q: Which object can a user change by clicking marks on a dashboard?
* A set (through a set action)
- A group
- A bin
- A hierarchy
> Set actions update set membership.

Q: A parameter on its own does nothing. Why?
* It must be referenced by a calculation, filter or reference line
- It needs an extract
- It must be added to context
- It only works on Tableau Server
> Parameters are inputs that something must use.

Q: Which filter applies to every sheet using the data source and is good for row-level restrictions?
* Data source filter
- Table-calculation filter
- Measure filter
- Page shelf
> Data source filters run near the start for all sheets.

Q: Which set type keeps the 10 largest customers by sales, updating as data changes?
* Top set
- Fixed set
- Group
- Combined set
> The Top tab makes a dynamic set.

Q: Which calculation swaps the measure shown in a chart?
* A CASE on a string parameter returning SUM([Sales]), SUM([Profit]) or SUM([Quantity])
- A FIXED LOD
- A group
- A data source filter
> The parameter value chooses the branch.
:::

:::exercise Practice
Build: (1) a dynamic Top N products chart with a parameter and Region in context; (2) a Top 20 customers set shown on Color in a scatter of Sales vs Profit; (3) a measure-swap chart with a dynamic title; (4) a what-if discount parameter showing projected profit by Category.
???
Follow the three parameter recipes. For (2): Customer Name on Detail, SUM(Sales) and SUM(Profit) on the axes, the Top 20 set on Color. For (4): a "Projected profit" calculated field `SUM([Profit]) - SUM([Sales]) * [Extra discount]` by Category with the parameter shown as a slider.
:::

:::interview Questions you may be asked
**Q: Difference between a set and a group?**
A group merges members into new categories and is static; a set divides members into IN/OUT, can be conditional or Top N, can be combined with other sets and changed through set actions.

**Q: What is a context filter and when do you use it?**
A filter that runs before other dimension filters, Top N filters and FIXED LODs. Use it for dependent Top N, to make FIXED LODs respect a filter, and to speed up large workbooks by reducing the data early.

**Q: Parameter vs filter?**
A filter removes data; a parameter is a single input value that you can use anywhere: in calculations, Top N, reference lines, titles, or to swap measures and dimensions.
:::
