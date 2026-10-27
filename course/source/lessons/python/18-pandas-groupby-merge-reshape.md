---
num: 18
title: "pandas III: GroupBy, Pivot Tables, Merge/Join and Reshape (melt/unpivot)"
live: "Python class 14"
updated: "pandas 2.3 / 3.0"
level: Intermediate
duration: 120 min
summary: Summarise and combine data. Use groupby with agg, transform and filter, build pivot tables and crosstabs, join tables with merge (inner, left, right, outer, anti), stack with concat, and reshape between wide and long with melt, pivot, stack and unstack.
datasets: [superstore_sales.csv, products.csv, customers.csv]
outcomes:
  - Apply split-apply-combine with groupby, named aggregations and multiple keys
  - Use transform for group-level columns and filter for group-level conditions
  - Build pivot_table and crosstab summaries with totals and percentages
  - Join DataFrames with merge, choose the join type, and validate the result
  - Reshape wide ↔ long with melt (unpivot) and pivot, and combine with concat
---

## Split–apply–combine

`groupby` **splits** rows into groups, **applies** a calculation to each group, and **combines** the results. It is SQL's `GROUP BY` and Excel's PivotTable.

```python fig: groupby splits rows by key, applies an aggregation per group, and combines the answers.
dg.flow(["All rows", "Split by\nregion", "Apply\nsum(sales)", "Combine\n4 rows"], title="Split → apply → combine")
```

```python run
import pandas as pd, numpy as np
pd.set_option("display.max_columns", 20); pd.set_option("display.width", 160)
s = pd.read_csv("superstore_sales.csv", parse_dates=["order_date"])
print(s.groupby("region")["sales"].sum().sort_values(ascending=False))
print(s.groupby(["region", "category"])["profit"].sum().round(0).unstack())
```

### Named aggregations

```python run
summary = (s.groupby("category")
             .agg(orders=("order_id", "nunique"), lines=("row_id", "size"), sales=("sales", "sum"),
                  profit=("profit", "sum"), avg_discount=("discount", "mean"), max_line=("sales", "max"))
             .assign(margin_pct=lambda d: (100 * d.profit / d.sales).round(1))
             .sort_values("sales", ascending=False))
print(summary.round(2))
print(s.groupby("segment", as_index=False)["sales"].agg(["sum", "mean", "median", "count"]).round(0))
```

Common aggregations: `sum`, `mean`, `median`, `min`, `max`, `count` (non-null), `size` (rows), `nunique`, `std`, `first`, `last`, or your own function.

### transform and filter

`transform` returns a value **for every row** (the group result broadcast back), perfect for "share of group" and group-wise filling. `filter` keeps whole groups that meet a condition.

```python run
s["region_sales"] = s.groupby("region")["sales"].transform("sum")
s["share_of_region_%"] = (100 * s["sales"] / s["region_sales"]).round(3)
s["rank_in_region"] = s.groupby("region")["sales"].rank(ascending=False, method="first").astype(int)
print(s.loc[s.rank_in_region <= 2, ["region", "product_name", "sales", "share_of_region_%", "rank_in_region"]].sort_values(["region", "rank_in_region"]))
loyal = s.groupby("customer_id").filter(lambda g: g["order_id"].nunique() >= 8)
print(loyal["customer_id"].nunique(), "customers placed 8+ orders")
```

## Pivot tables and crosstabs

```python run
s["year"] = s["order_date"].dt.year
pt = pd.pivot_table(s, values="sales", index="category", columns="year", aggfunc="sum", margins=True, margins_name="Total")
print((pt / 1e6).round(2))
print(pd.crosstab(s["segment"], s["ship_mode"], normalize="index").mul(100).round(1))       # row %
```

## Merging (joins)

Real analysis needs several tables. `pd.merge` (or `df.merge`) joins on key columns like SQL joins.

```python fig: Join types: which rows survive.
dg.joins_panel(("inner", "left", "right", "full"), labels=["inner", "left", "right", "outer"])
```

```python run
orders = pd.DataFrame({"order_id": [1, 2, 3, 4], "cust": ["C1", "C2", "C2", "C9"], "amount": [500, 250, 900, 120]})
cust = pd.DataFrame({"cust": ["C1", "C2", "C3"], "name": ["Asha", "Ravi", "Meera"], "city": ["Pune", "Delhi", "Kochi"]})
for how in ["inner", "left", "right", "outer"]:
    print(how, "->", len(orders.merge(cust, on="cust", how=how)), "rows")
print(orders.merge(cust, on="cust", how="left", indicator=True))
anti = orders.merge(cust, on="cust", how="left", indicator=True).query("_merge == 'left_only'")
print("orders with unknown customer:", anti["order_id"].tolist())
```

| Argument | Use |
|---|---|
| `on="key"` / `on=["a", "b"]` | Same column name(s) in both |
| `left_on=`, `right_on=` | Different key names |
| `how=` | `inner`, `left`, `right`, `outer`, `cross` |
| `suffixes=("_x", "_y")` | Clashing column names |
| `indicator=True` | Adds `_merge` to see where each row came from |
| `validate="many_to_one"` | Raises an error if the key is not unique on the right |

### A real three-table join

```python run
products = pd.read_csv("products.csv"); customers = pd.read_csv("customers.csv")
lines = s[["order_id", "customer_id", "product_id", "sales", "quantity"]]
full = (lines.merge(products[["product_id", "list_price"]], on="product_id", how="left", validate="many_to_one")
             .merge(customers[["customer_id", "city", "segment"]], on="customer_id", how="left", validate="many_to_one"))
print(len(lines), len(full), full["list_price"].isna().sum(), "unmatched products")
full["realised_vs_list_%"] = (100 * full["sales"] / (full["list_price"] * full["quantity"])).round(1)
print(full.groupby("segment")["realised_vs_list_%"].mean().round(1))
```

:::warning Row explosion
If the key is duplicated on **both** sides, a merge multiplies rows (many-to-many). Always compare row counts before and after, and use `validate=` to catch it.
:::

## concat: stacking tables

```python run
jan = pd.DataFrame({"store": ["A", "B"], "sales": [100, 80]}); feb = pd.DataFrame({"store": ["A", "C"], "sales": [120, 60]})
print(pd.concat([jan.assign(month="Jan"), feb.assign(month="Feb")], ignore_index=True))    # rows (UNION ALL)
print(pd.concat([jan.set_index("store"), feb.set_index("store")], axis=1, keys=["Jan", "Feb"]))   # columns, aligned on index
```

## Reshaping: wide ↔ long

**Wide** tables are easy to read (one column per month); **long** (tidy) tables are easy to analyse and chart (one row per observation). `melt` is pandas' **unpivot** (the same as Power Query's "Unpivot columns").

```python fig: melt turns columns into rows; pivot turns rows into columns.
dg.compare("Wide", ["region | Jan | Feb | Mar", "North | 10 | 12 | 9", "South | 8 | 11 | 14", "Readable report layout"], "Long (tidy)", ["region | month | sales", "North | Jan | 10", "North | Feb | 12 … (6 rows)", "Best for groupby, charts, models"], title="melt ⇄ pivot")
```

```python run
wide = pd.DataFrame({"region": ["North", "South"], "Jan": [10, 8], "Feb": [12, 11], "Mar": [9, 14]})
long = wide.melt(id_vars="region", var_name="month", value_name="sales")
print(long)
back = long.pivot(index="region", columns="month", values="sales")[["Jan", "Feb", "Mar"]]
print(back)
st = back.stack(); print(st.head(3)); print(st.unstack().equals(back))
```

`pivot` requires unique index/column pairs; `pivot_table` aggregates duplicates.

```python run
monthly = (s.assign(month=s.order_date.dt.to_period("M").astype(str))
             .pivot_table(index="month", columns="category", values="sales", aggfunc="sum").tail(3) / 1e6).round(2)
print(monthly)
print(monthly.reset_index().melt(id_vars="month", var_name="category", value_name="sales_m").head(4))
```

## Summary

:::key
- `groupby(keys).agg(name=(col, func))` builds clean summaries; `transform` returns group values per row; `filter` keeps whole groups.
- `pivot_table` (with `margins=True`) and `crosstab` (with `normalize`) mirror Excel PivotTables.
- `merge(on=, how=)` joins tables; check row counts, use `indicator=True` for anti-joins and `validate=` to prevent row explosions.
- `concat` stacks rows (or aligns columns).
- `melt` = unpivot (wide → long); `pivot`/`pivot_table` = long → wide; `stack`/`unstack` move index levels.
:::

:::quiz
Q: Which returns one value per original row?
- `groupby().agg()`
* `groupby().transform()`
- `groupby().size()`
- `pivot_table()`
> transform broadcasts the group result back to each row.

Q: Which merge keeps every order even when the customer is missing?
- inner
* left (orders on the left)
- right
- cross
> Unmatched customer columns become NaN.

Q: How do you find rows in A with no match in B?
- inner merge
* left merge with `indicator=True` and keep `_merge == "left_only"`
- outer merge without indicator
- concat
> This is an anti-join.

Q: What does `melt` do?
- Pivots long to wide
* Unpivots wide columns into rows (long format)
- Merges tables
- Deletes columns
> `pivot` goes the other way.

Q: A merge produced more rows than the left table. Most likely cause?
- A bug in pandas
* Duplicate keys on the right side
- Missing values
- Wrong dtype
> Use `validate="many_to_one"` to catch this.

Q: How do you add a grand-total row and column to a pivot table?
- `totals=True`
* `margins=True`
- `sum=True`
- `fill_value=0`
> `margins_name` changes the label.
:::

:::exercise GroupBy and merge practice
(1) Sales and profit by year and region, with margin %. (2) For each customer, the share of their spend in each category (use `transform`). (3) Top product per sub-category by profit. (4) Customers in `customers.csv` with no orders (anti-join). (5) Melt the year columns of a category × year pivot back to long format.
???
```python
yr = s.groupby(["year", "region"]).agg(sales=("sales", "sum"), profit=("profit", "sum"))
yr["margin_%"] = (100 * yr.profit / yr.sales).round(1); print(yr)
cc = s.groupby(["customer_id", "category"])["sales"].sum().reset_index()
cc["share"] = cc.sales / cc.groupby("customer_id")["sales"].transform("sum")
top = s.groupby(["sub_category", "product_name"])["profit"].sum().reset_index().sort_values("profit").groupby("sub_category").tail(1)
no_orders = customers.merge(s[["customer_id"]].drop_duplicates(), how="left", indicator=True).query("_merge == 'left_only'")
print(len(no_orders))
pt = s.pivot_table(index="category", columns="year", values="sales", aggfunc="sum")
print(pt.reset_index().melt(id_vars="category", var_name="year", value_name="sales"))
```
:::

:::interview Questions you may be asked
**Q: Difference between `agg` and `transform`?**
`agg` reduces each group to one row; `transform` returns an output aligned to the original rows.

**Q: How would you compute each product's share of its category's sales?**
`df.sales / df.groupby("category").sales.transform("sum")`.

**Q: merge vs join vs concat?**
`merge` joins on columns (SQL-style); `join` is a shortcut that joins on the index; `concat` stacks along an axis without matching keys.

**Q: What is tidy data?**
Each variable is a column, each observation a row, each value a cell; long format produced by `melt` is tidy.
:::
