---
num: 16
title: "pandas I: Series, DataFrames, Reading Data, Selecting and Filtering"
live: "Python class 12"
updated: "pandas 2.3 / 3.0"
level: Intermediate
duration: 120 min
summary: Meet the most-used data library. Create Series and DataFrames, read CSV and Excel files, inspect data with head, info and describe, select columns and rows with loc and iloc, filter with conditions and query, sort, add columns and save results, using the Superstore sales data.
datasets: [superstore_sales.csv, employees_small.csv]
outcomes:
  - Create Series and DataFrames and explain the index
  - Read CSV and Excel files with the right options and write results back out
  - Inspect a dataset with shape, dtypes, head, info, describe and value_counts
  - Select with [], loc and iloc and filter rows with boolean conditions, isin, between and query
  - Sort, rank, add and rename columns, and avoid the SettingWithCopy pitfall
---

## Series and DataFrame

**pandas** gives Python spreadsheet-like tables. A **Series** is one labelled column; a **DataFrame** is a table of Series sharing one **index** (row labels).

```python fig: A DataFrame is a set of Series (columns) that share an index (row labels).
dg.cards([("Index", "Row labels: 0, 1, 2 … or order_id, dates"), ("Columns", "Each column is a Series with one dtype"), ("Values", "The underlying NumPy / Arrow arrays")], title="Anatomy of a DataFrame")
```

```python run
import pandas as pd, numpy as np
pd.set_option("display.max_columns", 20); pd.set_option("display.width", 160)   # show wide tables in full
s = pd.Series([120, 95, 140], index=["North", "South", "East"], name="sales")
print(s, s["South"], s.max(), s.idxmax(), sep="\n")
df = pd.DataFrame({"city": ["Pune", "Delhi", "Kochi"], "sales": [120, 95, 140], "target": [100, 110, 130]})
df["hit"] = df["sales"] >= df["target"]
print(df)
print(df.shape, list(df.columns), df.index, df.dtypes.to_dict(), pd.__version__)
```

## Reading data

```python run
s = pd.read_csv("superstore_sales.csv", parse_dates=["order_date", "ship_date"])
print(s.shape)
print(s.head(3).T)
```

| Option | Use |
|---|---|
| `sep=";"` | Other delimiters (`"\t"` for TSV) |
| `usecols=[...]` | Read only some columns (faster, less memory) |
| `dtype={"pin": str}` | Keep leading zeros and IDs as text |
| `parse_dates=[...]` | Convert date columns |
| `na_values=["NA", "-"]` | Extra markers for missing |
| `nrows=1000`, `chunksize=100_000` | Sample or stream big files |
| `encoding="latin-1"` | Fix decode errors in older files |

Other readers: `pd.read_excel("file.xlsx", sheet_name="Sales")` (needs `openpyxl`), `pd.read_json`, `pd.read_parquet`, `pd.read_sql` (Lesson 23), `pd.read_html`, `pd.read_clipboard`.

## Inspecting data

Run these five on every new dataset:

```python run
print(s.info(memory_usage="deep"))
```

```python run
print(s.describe(include="number").round(1).T)
print(s["region"].value_counts(), s["category"].value_counts(normalize=True).round(3), sep="\n")
print(s["customer_id"].nunique(), "customers |", s["order_date"].min().date(), "to", s["order_date"].max().date())
print(s.isna().sum().sum(), "missing cells |", s.duplicated().sum(), "duplicate rows")
```

## Selecting columns and rows

```python run
print(s["sales"].head(3).tolist())                     # one column -> Series
print(s[["order_id", "region", "sales"]].head(3))      # list of columns -> DataFrame
print(s.loc[0, "customer_name"], s.iloc[0, 6])         # loc = labels, iloc = positions
print(s.loc[0:2, "region":"product_id"])                # loc slices INCLUDE the end label
print(s.iloc[0:2, 10:12])                               # iloc slices EXCLUDE the end, like Python
```

| Tool | Selects by | Example |
|---|---|---|
| `df["col"]` / `df[["a","b"]]` | Column names | `s["sales"]` |
| `df.loc[rows, cols]` | **Labels** and boolean masks | `s.loc[s.profit < 0, ["order_id", "profit"]]` |
| `df.iloc[rows, cols]` | **Integer positions** | `s.iloc[:5, :3]` |
| `df.at[r, c]` / `df.iat[i, j]` | One value, fast | `s.at[0, "sales"]` |

## Filtering rows

```python run
loss = s[s["profit"] < 0]
print(len(loss), "loss-making lines")
tech_south = s[(s["category"] == "Technology") & (s["region"] == "South")]            # & | ~ need brackets
print(len(tech_south), round(tech_south["sales"].sum() / 1e6, 2), "M")
print(s[s["city"].isin(["Pune", "Kochi"])]["city"].value_counts().to_dict())
print(len(s[s["discount"].between(0.1, 0.2)]), len(s[s["product_name"].str.contains("Chair")]))
print(s.query("region == 'West' and sales > 50000 and discount == 0")[["order_id", "sales"]].head(3))
big = 50000
print(len(s.query("sales > @big")))                        # @ refers to a Python variable
```

## Sorting and ranking

```python run
top = s.sort_values("sales", ascending=False)[["order_id", "product_name", "sales"]].head(5)
print(top)
print(s.sort_values(["region", "profit"], ascending=[True, False]).groupby("region").head(1)[["region", "product_name", "profit"]])
print(s.nlargest(3, "profit")[["product_name", "profit"]], s.nsmallest(2, "profit")[["product_name", "profit"]], sep="\n")
```

## Adding, changing and removing columns

```python run
e = pd.read_csv("employees_small.csv", parse_dates=["join_date"])
e["bonus"] = e["salary"] * 0.1                                         # vectorised arithmetic
e["band"] = np.where(e["salary"] >= 100000, "Senior", "Standard")      # IF
e["grade"] = pd.cut(e["salary"], bins=[0, 70000, 100000, np.inf], labels=["C", "B", "A"])   # bins
e["tenure_yrs"] = ((pd.Timestamp("2025-10-27") - e["join_date"]).dt.days / 365.25).round(1)
e = e.assign(name_upper=e["name"].str.upper()).rename(columns={"rating": "perf"}).drop(columns=["name_upper"])
e["salary_rank"] = e["salary"].rank(ascending=False, method="dense").astype(int)
print(e.head(6))
```

:::warning SettingWithCopyWarning
`sub = df[df.x > 0]; sub["y"] = 1` may warn because `sub` might be a view. Use `df.loc[df.x > 0, "y"] = 1` to change the original, or `sub = df[df.x > 0].copy()` for an independent table. pandas 3 makes copy-on-write the default, which removes the ambiguity.
:::

## Saving results

```python run
out = s.groupby("region", as_index=False)["sales"].sum()
out.to_csv("region_sales.csv", index=False)
print(open("region_sales.csv").read())
import os; os.remove("region_sales.csv")
```

Also: `to_excel("out.xlsx", sheet_name="Summary", index=False)`, `to_parquet` (fast, typed, compressed), `to_json(orient="records")`, `to_sql`.

## pandas vs Excel vs SQL

| Task | Excel | SQL | pandas |
|---|---|---|---|
| Filter | AutoFilter | `WHERE` | `df[df.x > 5]` / `query` |
| New column | Formula | `SELECT a*b AS c` | `df["c"] = df.a * df.b` |
| Sort | Sort | `ORDER BY` | `sort_values` |
| Lookup | XLOOKUP | `JOIN` | `merge` (Lesson 18) |
| Pivot | PivotTable | `GROUP BY` | `groupby`, `pivot_table` (Lesson 18) |

## Summary

:::key
- A DataFrame is a table of Series sharing an index; read files with `read_csv`/`read_excel` and the right options.
- Inspect first: `shape`, `info()`, `describe()`, `value_counts()`, `isna().sum()`, `duplicated().sum()`.
- Select with `[]` (columns), `loc` (labels, end-inclusive) and `iloc` (positions, end-exclusive).
- Filter with boolean masks using `&`, `|`, `~` and brackets, plus `isin`, `between`, `str.contains`, `query`.
- Add columns with vectorised maths, `np.where`, `pd.cut`; use `.loc` or `.copy()` to avoid SettingWithCopy issues.
:::

:::quiz
Q: What does `s[["region", "sales"]]` return?
- A Series
* A DataFrame with two columns
- A list
- An error
> Double brackets pass a list of columns.

Q: Which is end-inclusive?
* `df.loc[0:2]`
- `df.iloc[0:2]`
- Both
- Neither
> `loc` uses labels and includes the end label.

Q: Which filter is correct?
- `df[df.a > 1 and df.b < 5]`
* `df[(df.a > 1) & (df.b < 5)]`
- `df[df.a > 1 & df.b < 5]`
- `df.where(a > 1, b < 5)`
> Use `&` with brackets around each condition.

Q: How do you keep leading zeros in a PIN or ID column when reading?
- `parse_dates`
* `dtype={"pin": str}`
- `usecols`
- `index_col`
> Otherwise pandas reads it as a number.

Q: Which command shows column types and non-null counts?
- `describe()`
* `info()`
- `head()`
- `shape`
> `describe()` gives statistics.

Q: How do you reference a Python variable inside `query`?
- `{var}`
* `@var`
- `$var`
- `var()`
> `df.query("sales > @big")`.
:::

:::exercise pandas practice (Superstore)
(1) How many orders (unique `order_id`) are there? (2) Show the 5 most profitable sub-categories by total profit. (3) Filter Consumer-segment orders in 2025 with discount above 20%. (4) Add `margin_pct` and list the 3 lowest-margin product names among lines with sales above 20,000. (5) Save the Technology rows to `tech.csv`.
???
```python
print(s["order_id"].nunique())
print(s.groupby("sub_category")["profit"].sum().nlargest(5))
f = s[(s.segment == "Consumer") & (s.order_date.dt.year == 2025) & (s.discount > 0.2)]; print(len(f))
s["margin_pct"] = 100 * s.profit / s.sales
print(s[s.sales > 20000].nsmallest(3, "margin_pct")[["product_name", "margin_pct"]])
s[s.category == "Technology"].to_csv("tech.csv", index=False)
```
:::

:::interview Questions you may be asked
**Q: loc vs iloc?**
`loc` selects by label (and boolean masks), end-inclusive; `iloc` selects by integer position, end-exclusive.

**Q: How do you find and handle duplicates?**
`df.duplicated(subset=[...]).sum()` to count, `drop_duplicates(subset=..., keep="first")` to remove, after deciding which columns define a duplicate.

**Q: How do you read a file that does not fit in memory?**
`usecols` and `dtype` to shrink it, `chunksize` to stream it, or use DuckDB/Polars/Parquet.
:::
