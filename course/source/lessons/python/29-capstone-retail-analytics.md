---
num: 29
title: "Python Capstone: End-to-End Retail Sales Analytics Project"
live: "Python capstone"
updated: "pandas 3 · Matplotlib 3.10 · openpyxl"
level: Advanced
duration: 180 min
summary: Bring the whole Python track together on the Superstore data. Structure a project, build a validated data pipeline, compute KPIs, growth and Pareto analysis, cohort retention and discount impact, create a chart pack and an Excel report, and write the README and executive summary you can put in your portfolio.
datasets: [superstore_sales.csv, customers.csv, products.csv]
outcomes:
  - Organise an analysis as a reproducible project with functions, checks and outputs
  - Build a load → validate → transform pipeline with assertions
  - Analyse KPIs, growth, Pareto concentration, cohorts and discount effects
  - Produce a multi-sheet Excel report and a chart pack
  - Write an executive summary and a portfolio-ready README
---

## The brief

> The sales director of an Indian office-supplies retailer asks: **How did 2025 go, where do we make and lose money, how loyal are our customers, and what should we change in 2026?** Deliver a short report with charts and an Excel workbook her team can filter.

```python fig: Capstone pipeline.
dg.flow(["Load", "Validate", "Transform\n& enrich", "Analyse:\nKPIs, Pareto,\ncohorts, discounts", "Visualise", "Report:\nExcel + summary"], title="Project pipeline")
```

Project layout (Lesson 13): `data/raw`, `src/` (functions below), `notebooks/` (exploration), `reports/` (outputs), `README.md`.

## 1. Load and validate

```python run
import pandas as pd, numpy as np, matplotlib.pyplot as plt
pd.set_option("display.max_columns", 20); pd.set_option("display.width", 160)

def load(path="superstore_sales.csv"):
    df = pd.read_csv(path, parse_dates=["order_date", "ship_date"])
    return df

def validate(df):
    checks = {
        "row_id unique": df["row_id"].is_unique,
        "no missing values": df.isna().sum().sum() == 0,
        "sales positive": (df["sales"] > 0).all(),
        "discount between 0 and 1": df["discount"].between(0, 1).all(),
        "ship after order": (df["ship_date"] >= df["order_date"]).all(),
        "quantity 1-20": df["quantity"].between(1, 20).all(),
    }
    for name, ok in checks.items(): print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    assert all(checks.values()), "validation failed"
    return df

s = validate(load())
print(s.shape, s.order_date.min().date(), "→", s.order_date.max().date())
```

## 2. Transform and enrich

```python run
def enrich(df):
    out = df.copy()
    out["year"] = out.order_date.dt.year
    out["month"] = out.order_date.dt.to_period("M")
    out["margin_pct"] = 100 * out.profit / out.sales
    out["ship_days"] = (out.ship_date - out.order_date).dt.days
    out["discount_band"] = pd.cut(out.discount, [-0.01, 0, 0.1, 0.2, 1], labels=["0%", "1–10%", "11–20%", ">20%"])
    return out
s = enrich(s)
print(s[["order_id", "year", "month", "sales", "profit", "margin_pct", "discount_band"]].head(3))
```

## 3. Headline KPIs and growth

```python run
def kpis(df):
    g = df.groupby("year").agg(sales=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique"), customers=("customer_id", "nunique"), units=("quantity", "sum"))
    g["margin_%"] = 100 * g.profit / g.sales
    g["aov"] = g.sales / g.orders
    g["sales_growth_%"] = 100 * g.sales.pct_change()
    g["profit_growth_%"] = 100 * g.profit.pct_change()
    return g
k = kpis(s)
view = k.assign(sales=k.sales / 1e6, profit=k.profit / 1e6, aov=k.aov / 1e3).round(1)
view.columns = ["sales ₹M", "profit ₹M", "orders", "customers", "units", "margin %", "AOV ₹K", "sales growth %", "profit growth %"]
print(view)
```

```python fig: Monthly sales and profit, 2023–2025, with 3-month rolling averages.
m = s.groupby("month")[["sales", "profit"]].sum() / 1e6
m.index = m.index.to_timestamp()
fig, ax = plt.subplots(figsize=(10, 3.6))
ax.bar(m.index, m.sales, width=20, color="#DDD6FE", label="monthly sales")
ax.plot(m.index, m.sales.rolling(3).mean(), color="#7C3AED", lw=2.2, label="sales, 3-month avg")
ax.plot(m.index, m.profit.rolling(3).mean(), color="#DB2777", lw=2.2, label="profit, 3-month avg")
ax.set_ylabel("₹ million"); ax.legend(frameon=False, ncol=3, loc="upper left"); ax.spines[["top", "right"]].set_visible(False)
ax.set_title("Sales and profit both grew each year; profit grew faster", loc="left", weight="bold")
```

## 4. Where we make and lose money

```python run
sub = s[s.year == 2025].groupby(["category", "sub_category"]).agg(sales=("sales", "sum"), profit=("profit", "sum"), avg_disc=("discount", "mean"))
sub["margin_%"] = (100 * sub.profit / sub.sales).round(1)
sub = sub.sort_values("profit")
print((sub.assign(sales=sub.sales / 1e6, profit=sub.profit / 1e6)).round(2))
```

```python run
db = s.groupby("discount_band", observed=True).agg(lines=("row_id", "size"), sales=("sales", "sum"), profit=("profit", "sum"))
db["margin_%"] = (100 * db.profit / db.sales).round(1); db["share_of_lines_%"] = (100 * db.lines / db.lines.sum()).round(1)
print(db.assign(sales=(db.sales / 1e6).round(1), profit=(db.profit / 1e6).round(2)))
```

```python fig: Margin by discount band: deep discounts turn profitable lines into losses.
fig, ax = plt.subplots(figsize=(7, 3.2))
ax.bar(db.index.astype(str), db["margin_%"], color=["#0E9F8E" if v > 0 else "#DB2777" for v in db["margin_%"]])
ax.axhline(0, color="#333", lw=.8); ax.set_ylabel("margin %"); ax.set_xlabel("discount band"); ax.spines[["top", "right"]].set_visible(False)
for i, v in enumerate(db["margin_%"]): ax.text(i, v + (1 if v >= 0 else -3), f"{v:.1f}%", ha="center", fontsize=9)
```

## 5. Customer concentration (Pareto)

```python run
cust = s.groupby("customer_id")["sales"].sum().sort_values(ascending=False)
cum = cust.cumsum() / cust.sum()
top20 = int(len(cust) * 0.2)
print(f"{len(cust)} customers | top 20% ({top20}) bring {cum.iloc[top20 - 1]:.0%} of sales | customers needed for 50% of sales: {(cum < 0.5).sum() + 1}")
```

```python fig: Pareto curve of customer sales.
fig, ax = plt.subplots(figsize=(7, 3.4))
x = np.arange(1, len(cum) + 1) / len(cum) * 100
ax.plot(x, cum.values * 100, color="#7C3AED", lw=2.2); ax.plot([0, 100], [0, 100], ls="--", color="#999", lw=1)
ax.axvline(20, color="#DB2777", lw=1); ax.text(21, 10, f"top 20% → {cum.iloc[top20 - 1]:.0%} of sales", color="#DB2777")
ax.set_xlabel("% of customers (ranked by sales)"); ax.set_ylabel("% of sales"); ax.spines[["top", "right"]].set_visible(False)
```

## 6. Cohort retention

A **cohort** groups customers by the month (here: quarter) of their first purchase; retention tracks how many buy again later.

```python run
s["quarter"] = s.order_date.dt.to_period("Q")
first = s.groupby("customer_id")["quarter"].min().rename("cohort")
c = s.join(first, on="customer_id")
c["age_q"] = (c.quarter - c.cohort).apply(lambda d: d.n)
active = c.groupby(["cohort", "age_q"])["customer_id"].nunique().unstack()
retention = (active.div(active[0], axis=0) * 100).round(0)
print(active[0].rename("cohort size").head(6).to_dict())
print(retention.iloc[:6, :8])
```

```python fig: Quarterly cohort retention (% of each cohort buying in later quarters).
import seaborn as sns
fig, ax = plt.subplots(figsize=(9, 3.6))
sns.heatmap(retention.iloc[:6, 1:9], annot=True, fmt=".0f", cmap="Purples", cbar=False, ax=ax)
ax.set_xlabel("quarters since first purchase"); ax.set_ylabel("first-purchase quarter")
```

## 7. Operations: shipping

```python run
ship = s.groupby("ship_mode").agg(lines=("row_id", "size"), avg_days=("ship_days", "mean"), sales=("sales", "sum"))
ship["share_%"] = (100 * ship.lines / ship.lines.sum()).round(1)
print(ship.round(1).sort_values("avg_days"))
reg = s[s.year == 2025].groupby("region").agg(sales=("sales", "sum"), profit=("profit", "sum"))
reg["margin_%"] = (100 * reg.profit / reg.sales).round(1); print((reg.assign(sales=reg.sales / 1e6, profit=reg.profit / 1e6)).round(2))
```

## 8. Excel report for the business

```python run
from pathlib import Path
out = Path("reports"); out.mkdir(exist_ok=True)
with pd.ExcelWriter(out / "sales_review_2025.xlsx", engine="openpyxl") as xw:
    view.to_excel(xw, sheet_name="KPIs")
    sub.reset_index().to_excel(xw, sheet_name="Sub-category 2025", index=False)
    db.reset_index().to_excel(xw, sheet_name="Discount bands", index=False)
    retention.reset_index().astype(str).to_excel(xw, sheet_name="Cohort retention", index=False)
    s[s.year == 2025].drop(columns=["month", "quarter"]).to_excel(xw, sheet_name="Data 2025", index=False)
import openpyxl
wb = openpyxl.load_workbook(out / "sales_review_2025.xlsx")
for ws in wb.worksheets:
    ws.freeze_panes = "B2"; ws.auto_filter.ref = ws.dimensions
    for col in ws.columns: ws.column_dimensions[col[0].column_letter].width = 16
wb.save(out / "sales_review_2025.xlsx")
print(wb.sheetnames, f"{(out / 'sales_review_2025.xlsx').stat().st_size / 1e6:.1f} MB")
import shutil; shutil.rmtree(out)
```

## 9. Executive summary (template)

Write the summary **from the numbers above**; every claim should point to a table or chart.

:::key
Fill each line from your outputs:
1. **Growth**: 2025 sales of ₹__M (+__% on 2024), profit ₹__M (+__%), margin __%.
2. **Profit engines**: __ and __ deliver __% of profit; __ and __ lose money.
3. **Discounts**: lines discounted above 20% have a __% margin, against __% at no discount.
4. **Customers**: the top 20% of customers bring __% of sales, and __% of a cohort is still buying a year later.
5. **Actions for 2026**: cap discounts on __; review pricing of __; a loyalty programme for the top customers; a retention push in the first quarter after a customer's first purchase.
:::

## 10. README for your portfolio

```text
# Superstore India: 2025 Sales Review (Python)
**Question:** How did 2025 perform, where is profit made and lost, how loyal are customers?
**Data:** 6,323 order lines, 2023–2025 (synthetic, modelled on the Superstore dataset).
**Tools:** pandas, Matplotlib, Seaborn, openpyxl.
**Method:** validation checks → enrichment → KPIs, Pareto, cohort retention, discount analysis.
**Key findings:** (3–5 bullets with numbers)
**Recommendations:** (3 bullets)
**How to run:** `pip install -r requirements.txt && python src/run_report.py`
**Repo:** data/ · src/ · notebooks/ · reports/ · README.md
```

## Summary

:::key
- A project is a pipeline: load → validate (assertions) → enrich → analyse → visualise → report.
- KPI tables with growth, sub-category profitability, discount bands, Pareto concentration and cohort retention answer most retail questions.
- `pd.ExcelWriter` + openpyxl create business-ready, filterable workbooks.
- Finish with an executive summary tied to numbers and a portfolio README.
:::

:::quiz
Q: Why put validation checks at the start of the pipeline?
* To stop early if the data breaks assumptions, rather than producing wrong results
- To make the code longer
- Because pandas requires it
- To speed up loading
> Assertions make failures loud.

Q: What does a Pareto analysis of customers show?
- Average sales
* How concentrated sales are among the top customers
- Retention over time
- Discount impact
> Often a minority of customers brings most of the revenue.

Q: What is a cohort in retention analysis?
* Customers grouped by the period of their first purchase
- Customers in the same city
- All customers
- Products in a category
> Retention follows each cohort over time.

Q: Which tool writes several sheets to one Excel file?
- `df.to_csv`
* `pd.ExcelWriter`
- `openpyxl.load_workbook` only
- `df.to_json`
> Then format with openpyxl.

Q: What belongs in an executive summary?
- All code
* Key numbers, findings and recommended actions
- Raw data
- Library versions
> Lead with the answer.

Q: Why write analysis steps as functions?
* They can be tested, re-run on new data and reused
- They run faster in all cases
- Notebooks forbid loops
- To avoid variables
> Reproducibility matters.
:::

:::exercise Extend the capstone
(1) Add product-level ABC analysis (A = top 80% of sales). (2) Compute RFM scores for 2025 customers (see ML track lesson on segmentation). (3) Turn the chart cells into a function that saves PNGs to `reports/`. (4) Publish the project on GitHub with the README template and one chart in the README.
???
```python
prod = s.groupby("product_name")["sales"].sum().sort_values(ascending=False)
share = prod.cumsum() / prod.sum()
abc = pd.cut(share, [0, .8, .95, 1], labels=["A", "B", "C"]); print(abc.value_counts())
snap = s.order_date.max() + pd.Timedelta(days=1)
rfm = s[s.year == 2025].groupby("customer_id").agg(R=("order_date", lambda d: (snap - d.max()).days), F=("order_id", "nunique"), M=("sales", "sum"))
rfm["score"] = pd.qcut(-rfm.R, 4, labels=False) + pd.qcut(rfm.F.rank(method="first"), 4, labels=False) + pd.qcut(rfm.M, 4, labels=False)
print(rfm.sort_values("score", ascending=False).head())
```
:::

:::interview Questions you may be asked
**Q: Walk me through a project you are proud of.**
Use STAR: the business situation and question, your task, the actions (data, cleaning, analysis, tools), and the result with numbers and what changed. Keep it to two minutes and be ready to go deeper on any step.

**Q: How do you make sure your numbers are right?**
Validation checks, reconciling totals with a trusted source, spot-checking individual records, peer review, and versioned, re-runnable code.

**Q: What would you do next with more time?**
Automate the refresh (schedule + Parquet/database), add a dashboard, build a churn or demand-forecast model, and run an experiment on discount policy.
:::
