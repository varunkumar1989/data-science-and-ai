---
num: 22
title: "Exploratory Data Analysis (EDA) Case Study: Telecom Customer Churn"
live: "Python class 17"
updated: "pandas 3 · Seaborn 0.13"
level: Intermediate
duration: 150 min
summary: Run a complete, structured EDA on 3,000 telecom customers. Frame the question, check data quality, do univariate, bivariate and segment analysis, engineer features, quantify revenue at risk and finish with findings and recommendations: the template you will reuse for every dataset and for the ML churn model.
datasets: [telecom_churn.csv]
outcomes:
  - Follow a repeatable EDA checklist from question to recommendation
  - Check data quality and consistency between related columns
  - Analyse univariate distributions and bivariate relationships with the target
  - Build segments and quantify business impact (revenue at risk)
  - Write findings as clear, numbered insights with actions
---

## The EDA checklist

```python fig: A structured EDA moves from the business question to actions.
dg.flow(["1 Question\n& metric", "2 Data\nquality", "3 Univariate", "4 Bivariate\nvs target", "5 Segments\n& features", "6 Impact", "7 Findings &\nactions"], title="EDA workflow")
```

**Business question.** A telecom operator loses customers every month. *Which customers churn, why, and where should retention money go first?* **Target:** `churn` (Yes/No). **Metric:** churn rate = churned ÷ customers.

## 1. Load and first look

```python run
import pandas as pd, numpy as np, seaborn as sns, matplotlib.pyplot as plt
pd.set_option("display.max_columns", 20); pd.set_option("display.width", 160)
tc = pd.read_csv("telecom_churn.csv")
tc["churned"] = (tc["churn"] == "Yes").astype(int)
print(tc.shape); print(tc.head(3))
print(tc.dtypes.astype(str).to_dict())
print(f"Overall churn rate: {tc.churned.mean():.1%} ({tc.churned.sum()} of {len(tc)})")
```

## 2. Data quality

```python run
print("missing:", tc.isna().sum().sum(), "| duplicate ids:", tc.customer_id.duplicated().sum())
print(tc.describe().round(1).T[["min", "50%", "max", "mean"]])
for c in ["contract", "internet_service", "payment_method"]: print(c, tc[c].value_counts().to_dict())
gap = tc.total_charges - tc.tenure_months * tc.monthly_charges        # consistency check between columns
print("total_charges − tenure × monthly: median", round(gap.median(), 1), "| 95% within ±", round(gap.abs().quantile(.95), 0))
print("tenure 0 customers:", (tc.tenure_months == 0).sum())
```

No missing values or duplicate IDs. `total_charges` roughly equals tenure × monthly charges (small gaps from price changes), so the columns are consistent. A few customers have tenure 0 (new joiners), which is valid.

## 3. Univariate analysis

```python fig: Distributions of the numeric variables. Tenure is spread across 0–72 months; monthly charges have a bump of low-price plans.
fig, axes = plt.subplots(1, 4, figsize=(12, 2.8))
for ax, col, color in zip(axes, ["tenure_months", "monthly_charges", "total_charges", "support_calls"], ["#7C3AED", "#DB2777", "#0E9F8E", "#E2A400"]):
    if col == "support_calls": ax.bar(*np.unique(tc[col], return_counts=True), color=color)
    else: ax.hist(tc[col], bins=30, color=color, alpha=.85)
    ax.set_title(col, fontsize=10, weight="bold"); ax.spines[["top", "right"]].set_visible(False); ax.set_yticks([])
```

## 4. Bivariate: each driver vs churn

```python run
def churn_by(col):
    g = tc.groupby(col, observed=True)["churned"].agg(customers="size", churn_rate="mean")
    g["churn_rate"] = (100 * g.churn_rate).round(1); g["lift"] = (g.churn_rate / (100 * tc.churned.mean())).round(2)
    return g
for col in ["contract", "internet_service", "payment_method", "senior_citizen"]: print(churn_by(col), "\n")
```

**Lift** = segment churn ÷ overall churn. Lift 1.4 means 40% more likely to churn than average.

```python run
tc["tenure_band"] = pd.cut(tc.tenure_months, [0, 6, 12, 24, 48, 72], include_lowest=True, labels=["0–6", "7–12", "13–24", "25–48", "49–72"])
tc["calls_band"] = pd.cut(tc.support_calls, [-1, 0, 1, 2, 3, 10], labels=["0", "1", "2", "3", "4+"])
tc["charge_band"] = pd.qcut(tc.monthly_charges, 4, labels=["Q1 low", "Q2", "Q3", "Q4 high"])
for col in ["tenure_band", "calls_band", "charge_band"]: print(churn_by(col), "\n")
```

```python fig: Churn rate by the four strongest drivers. The dashed line is the overall rate.
fig, axes = plt.subplots(1, 4, figsize=(12.5, 3.2), sharey=True)
overall = 100 * tc.churned.mean()
for ax, col in zip(axes, ["contract", "tenure_band", "calls_band", "internet_service"]):
    g = churn_by(col)["churn_rate"]
    ax.bar(g.index.astype(str), g.values, color=["#DB2777" if v > overall else "#C4B5FD" for v in g.values])
    ax.axhline(overall, ls="--", color="#555", lw=1); ax.set_title(col, fontsize=10, weight="bold"); ax.tick_params(axis="x", rotation=25, labelsize=8)
    ax.spines[["top", "right"]].set_visible(False)
axes[0].set_ylabel("churn rate %")
```

### Numeric drivers

```python run
print(tc.groupby("churn")[["tenure_months", "monthly_charges", "total_charges", "support_calls"]].median())
print(tc[["tenure_months", "monthly_charges", "support_calls", "senior_citizen", "churned"]].corr()["churned"].drop("churned").round(3).sort_values())
```

## 5. Segments: interactions matter

```python run
seg = tc.pivot_table(index="contract", columns="tenure_band", values="churned", aggfunc="mean", observed=True).mul(100).round(1)
print(seg)
cnt = tc.pivot_table(index="contract", columns="tenure_band", values="churned", aggfunc="size", observed=True)
print(cnt)
```

```python fig: Churn rate (%) by contract and tenure: new month-to-month customers are the hot spot.
fig, ax = plt.subplots(figsize=(7.5, 3))
sns.heatmap(seg, annot=True, fmt=".0f", cmap="RdPu", cbar_kws={"label": "churn %"}, ax=ax, linewidths=.5)
ax.set_xlabel("tenure (months)"); ax.set_ylabel("")
```

```python run
hot = tc[(tc.contract == "Month-to-month") & (tc.tenure_months <= 12)]
fiber_calls = tc[(tc.internet_service == "Fiber") & (tc.support_calls >= 3)]
for name, d in [("Month-to-month, tenure ≤ 12", hot), ("Fiber with 3+ support calls", fiber_calls)]:
    print(f"{name:32s} customers {len(d):4d} | churn {d.churned.mean():.1%} | lift {d.churned.mean() / tc.churned.mean():.2f}")
```

## 6. Business impact: revenue at risk

```python run
tc["monthly_revenue_lost"] = tc.monthly_charges * tc.churned
lost = tc.monthly_revenue_lost.sum()
print(f"Monthly revenue of churned customers: {lost:,.0f}  ({lost / tc.monthly_charges.sum():.1%} of all monthly revenue)")
imp = tc.groupby("contract").agg(churners=("churned", "sum"), revenue_lost=("monthly_revenue_lost", "sum"))
imp["share_of_loss_%"] = (100 * imp.revenue_lost / lost).round(1)
print(imp.round(0))
```

Revenue numbers here are in the data's currency units per month; multiply by expected remaining lifetime to estimate lifetime value lost.

## 7. Findings and recommendations

:::key
1. **About 1 in 4 customers churn** (25.7%), taking 27.9% of monthly revenue with them.
2. **Contract is the strongest driver**: month-to-month churn is about 36%, against about 7% on two-year contracts, and month-to-month customers account for 77% of the monthly revenue lost.
3. **The first year is critical**: churn is above 40% in the first 12 months and falls steadily with tenure.
4. **Support calls signal risk**: churn roughly doubles from 0 calls (about 19%) to 3 or more calls (about 36–44%).
5. **Fiber customers churn more** (about 32% against 22% on DSL), which is consistent with price or service-quality issues.
6. Payment method and senior status make only small differences.
:::

**Recommendations.** (a) Offer month-to-month customers in their first year an incentive to move to an annual plan. (b) Trigger a proactive call after the second support ticket. (c) Investigate Fiber service quality and pricing. (d) Build a churn-score model (ML track, capstone) to rank customers each month and measure the retention campaign with an A/B test.

:::note EDA is not causal proof
These are associations. Contract and churn are related, but customers who intend to leave may simply choose month-to-month plans. Experiments (A/B tests) or careful causal methods are needed before claiming that a change will cause lower churn.
:::

## Automated profiling tools

Libraries such as **ydata-profiling** (`ProfileReport(df)`), **sweetviz** and **D-Tale** generate an EDA report in one line, and AI assistants (Lesson ai-analytics) can draft charts. Use them for a quick first scan, then do the focused, question-driven analysis above.

## Summary

:::key
- EDA follows a checklist: question → quality → univariate → bivariate → segments → impact → findings.
- Check consistency between related columns, not just missing values.
- Compare churn rate and lift by category; band numeric variables with `cut`/`qcut`.
- Interactions (contract × tenure) reveal hot spots that single variables hide.
- Quantify impact in money and end with specific, owned recommendations; remember that association is not causation.
:::

:::quiz
Q: What is "lift" in segment analysis?
- The number of customers in a segment
* Segment rate divided by the overall rate
- The difference between two means
- A chart type
> Lift 2 = twice as likely as average.

Q: Why band tenure into groups?
- pandas needs it
* To compare churn rates across ranges and spot non-linear patterns
- To delete outliers
- To save memory
> `pd.cut` for fixed edges, `qcut` for equal-sized groups.

Q: Which finding came from an interaction analysis?
- Overall churn is 25.7%
* New month-to-month customers have the highest churn
- Fiber churns more
- No missing values
> It combines two variables.

Q: Why check `total_charges` against tenure × monthly charges?
* To verify consistency between related columns
- To compute churn
- To fill missing values
- To make a chart
> Inconsistent columns hint at data errors.

Q: What should an EDA conclude with?
- All charts produced
* Numbered findings with quantified impact and recommendations
- The raw data
- A model
> Stakeholders act on findings, not charts.

Q: Can EDA alone prove that a two-year contract reduces churn?
- Yes
* No, it shows association; experiments or causal methods are needed
- Only with a heatmap
- Only if r > 0.5
> Self-selection can explain the pattern.
:::

:::exercise Extend the case study
(1) Compute churn by payment method within month-to-month customers only. (2) Find the 10 highest-revenue customers at risk (month-to-month, tenure ≤ 12, 2+ support calls). (3) Plot churn rate against monthly charge deciles. (4) Write a five-bullet executive summary.
???
```python
print(tc[tc.contract == "Month-to-month"].groupby("payment_method").churned.mean().round(3))
risk = tc[(tc.contract == "Month-to-month") & (tc.tenure_months <= 12) & (tc.support_calls >= 2) & (tc.churned == 0)]
print(risk.nlargest(10, "monthly_charges")[["customer_id", "monthly_charges", "support_calls"]])
dec = tc.groupby(pd.qcut(tc.monthly_charges, 10), observed=True).churned.mean()
dec.plot(marker="o")
```
:::

:::interview Questions you may be asked
**Q: Walk me through how you would do EDA on a new dataset.**
Clarify the question and target, check quality (types, missing, duplicates, ranges, consistency), look at each variable, compare each variable against the target, explore interactions and segments, quantify impact, and summarise findings with next steps.

**Q: How do you decide which variables matter most for churn?**
Compare churn rates/lift by category, correlations and group medians for numeric variables, then confirm with a model (feature importance) and, for causality, with experiments.

**Q: Which chart would you use to show churn by two categorical variables?**
A heatmap of churn rates (with counts available) or grouped bars.
:::
