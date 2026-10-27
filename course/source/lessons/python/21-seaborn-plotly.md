---
num: 21
title: "Data Visualisation II: Seaborn Statistical Charts and Interactive Plotly"
live: "Python class 16"
updated: "Seaborn 0.13 · Plotly 6"
level: Intermediate
duration: 100 min
summary: Make statistical charts quickly with Seaborn (distributions, categorical comparisons, relationships, correlation heatmaps, pair plots and facets) using the HR attrition data, and build interactive charts and simple dashboards with Plotly Express and Streamlit.
datasets: [hr_employees.csv, telecom_churn.csv]
outcomes:
  - Use Seaborn's figure-level and axes-level functions with hue, col and row
  - Compare distributions across groups with histplot, kdeplot, boxplot, violinplot and countplot
  - Show relationships with scatterplot, regplot, heatmaps of correlations and pairplot
  - Build interactive charts with Plotly Express and know when to use Streamlit
  - Turn charts into a clear data story
---

## Seaborn in one idea

Seaborn works directly with **long DataFrames**: you name the columns for `x`, `y`, `hue` (colour), `col`/`row` (small multiples), and it groups, aggregates and adds legends for you.

```python run
import pandas as pd, numpy as np, seaborn as sns, matplotlib.pyplot as plt
hr = pd.read_csv("hr_employees.csv")
hr["left"] = (hr["attrition"] == "Yes").astype(int)
print(hr.shape, f"attrition rate {hr.left.mean():.1%}", sns.__version__)
print(hr.groupby("overtime")["left"].mean().round(3).to_dict(), hr.groupby("department")["left"].mean().round(3).sort_values().to_dict())
```

| Question | Seaborn function |
|---|---|
| Distribution of one variable | `histplot`, `kdeplot`, `ecdfplot` |
| Distribution by group | `boxplot`, `violinplot`, `stripplot`, `boxenplot` |
| Counts of categories | `countplot` |
| Average per category (with CI) | `barplot`, `pointplot` |
| Two numeric variables | `scatterplot`, `regplot`, `lmplot`, `jointplot` |
| Many variables | `pairplot`, `heatmap` of `df.corr()` |
| Small multiples | `displot`, `catplot`, `relplot` with `col=`/`row=` |

## Distributions

```python fig: Income distribution for leavers vs stayers: leavers cluster at lower incomes.
sns.set_theme(style="white", palette=["#7C3AED", "#DB2777"])
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6))
sns.histplot(data=hr, x="monthly_income", hue="attrition", stat="density", common_norm=False, element="step", bins=30, ax=a1)
sns.boxplot(data=hr, x="attrition", y="monthly_income", hue="attrition", ax=a2, width=.5, legend=False)
a1.set_title("Income density by attrition", loc="left", weight="bold"); a2.set_title("Income by attrition", loc="left", weight="bold")
sns.despine()
```

`common_norm=False` scales each group separately, so a small group (leavers) is not dwarfed by a big one.

```python fig: Violin plots combine a box plot with the distribution shape; split by overtime.
fig, ax = plt.subplots(figsize=(9, 3.6))
sns.violinplot(data=hr, x="department", y="age", hue="overtime", split=True, inner="quart", ax=ax, palette=["#C4B5FD", "#DB2777"])
ax.set_title("Age by department and overtime", loc="left", weight="bold"); sns.despine()
```

## Categorical comparisons

```python fig: Attrition rate by overtime and job satisfaction. Bars show the mean with a 95% confidence interval.
fig, ax = plt.subplots(figsize=(8, 3.6))
sns.barplot(data=hr, x="job_satisfaction", y="left", hue="overtime", errorbar=("ci", 95), ax=ax, palette=["#C4B5FD", "#7C3AED"])
ax.set_ylabel("attrition rate"); ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
ax.set_title("Overtime raises attrition at every satisfaction level", loc="left", weight="bold"); sns.despine()
```

```python run
print((hr.pivot_table(index="job_satisfaction", columns="overtime", values="left", aggfunc="mean") * 100).round(1))
```

## Relationships and correlation

```python fig: Correlation heatmap of numeric HR variables (Pearson r). Only the lower triangle is shown.
num = hr[["age", "years_at_company", "monthly_income", "job_satisfaction", "distance_from_home_km", "performance_rating", "left"]]
corr = num.corr().round(2)
mask = np.triu(np.ones_like(corr, dtype=bool))
fig, ax = plt.subplots(figsize=(7, 5.2))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1, center=0, linewidths=.5, ax=ax, cbar_kws={"shrink": .7})
ax.set_title("Correlation matrix", loc="left", weight="bold")
```

```python run
print(corr["left"].drop("left").sort_values())
```

Correlation measures **linear** association between −1 and +1. It does not prove causation, and it can miss non-linear patterns: always look at the scatter too.

```python fig: regplot adds a fitted line with a confidence band; lmplot repeats it per group.
fig, ax = plt.subplots(figsize=(8, 3.6))
sns.regplot(data=hr.sample(500, random_state=1), x="age", y="monthly_income", scatter_kws=dict(s=8, alpha=.4, color="#7C3AED"), line_kws=dict(color="#DB2777"), ax=ax)
ax.set_title("Income rises with age", loc="left", weight="bold"); sns.despine()
```

## Pair plots and facets

```python fig: A pair plot shows every pairwise scatter and each distribution, coloured by churn (telecom data).
tc = pd.read_csv("telecom_churn.csv")
g = sns.pairplot(tc[["tenure_months", "monthly_charges", "support_calls", "churn"]].sample(600, random_state=0), hue="churn", palette=["#C4B5FD", "#DB2777"], plot_kws=dict(s=10, alpha=.6), height=2.1)
```

```python fig: Facets (small multiples) with catplot: churn rate by contract type, split by internet service.
tc["churned"] = (tc["churn"] == "Yes").astype(int)
g = sns.catplot(data=tc, x="contract", y="churned", col="internet_service", kind="bar", height=3, aspect=1, color="#7C3AED", errorbar=None, order=["Month-to-month", "One year", "Two year"])
g.set_axis_labels("", "churn rate"); g.set_xticklabels(rotation=20)
```

```python run
print((tc.pivot_table(index="contract", columns="internet_service", values="churned", aggfunc="mean") * 100).round(1))
```

## Interactive charts with Plotly Express

Plotly makes charts you can hover, zoom and filter in a browser or notebook. The syntax mirrors Seaborn:

```python
import plotly.express as px
fig = px.scatter(tc, x="tenure_months", y="monthly_charges", color="churn",
                 hover_data=["contract", "payment_method"], opacity=.6,
                 title="Churn by tenure and charges")
fig.show()                         # interactive in notebooks
fig.write_html("churn.html")       # share as a standalone web page

px.line(monthly_df, x="month", y="sales", color="category")
px.bar(region_df, x="region", y="sales", text_auto=".2s")
px.histogram(hr, x="monthly_income", color="attrition", barmode="overlay")
px.choropleth(...)                 # maps
```

### A mini dashboard app with Streamlit

```python
# app.py  ->  run with:  streamlit run app.py
import streamlit as st, pandas as pd, plotly.express as px
df = pd.read_csv("telecom_churn.csv")
contract = st.sidebar.multiselect("Contract", df.contract.unique(), default=list(df.contract.unique()))
d = df[df.contract.isin(contract)]
st.title("Churn dashboard")
st.metric("Churn rate", f"{(d.churn == 'Yes').mean():.1%}")
st.plotly_chart(px.histogram(d, x="tenure_months", color="churn", barmode="overlay"))
```

Streamlit turns a Python script into a web app with filters, which is useful for sharing analyses and ML demos (see the GenAI track for chat apps).

## From charts to a data story

```python fig: The story arc: context, finding, evidence, recommendation.
dg.flow(["Context:\nabout 1 in 4\nemployees leave", "Finding:\novertime\nstaff leave more", "Evidence:\nchart + numbers", "So what:\ncost of attrition", "Action:\nreview overtime\npolicy"], title="Data storytelling")
```

1. **One message per chart**, written as the title.
2. Show the comparison that proves it (overtime vs not), not every chart you made.
3. Quantify impact (people, ₹, %).
4. End with a recommendation and its owner.

## Summary

:::key
- Seaborn plots long DataFrames by column name with `hue`, `col` and `row`; it sits on Matplotlib, so you can still style the axes.
- Distributions: `histplot` (with `common_norm=False`), `kdeplot`, `boxplot`, `violinplot`; categories: `countplot`, `barplot` with confidence intervals.
- Relationships: `scatterplot`, `regplot`, `pairplot`, correlation `heatmap` (correlation ≠ causation).
- Facets (`catplot`, `relplot`, `displot`) create small multiples.
- Plotly Express gives interactive charts; Streamlit turns scripts into dashboards. Tell a story: one message per chart.
:::

:::quiz
Q: What does `hue="attrition"` do in Seaborn?
- Changes the theme
* Colours the marks by the attrition category
- Filters to attrition = Yes
- Adds a title
> `col=` would create separate panels instead.

Q: Which chart shows the mean per category with a confidence interval?
- countplot
* barplot
- histplot
- heatmap
> `countplot` shows counts.

Q: A correlation of −0.8 means…
- No relationship
* A strong negative linear relationship
- One variable causes the other to fall
- A weak relationship
> Correlation does not imply causation.

Q: Which function creates small multiples of bar charts?
- barplot
* catplot(kind="bar", col=...)
- heatmap
- pairplot
> Figure-level functions accept `col` and `row`.

Q: What is the main advantage of Plotly over Matplotlib?
- Faster to print
* Interactive hover, zoom and filtering in the browser
- More chart types for PDFs
- No code needed
> Export with `write_html`.

Q: Why use `common_norm=False` in a histplot with hue?
* So each group's density is scaled to its own size and small groups stay visible
- To remove the legend
- To use counts
- To normalise to 100
> Otherwise the larger group dominates.
:::

:::exercise Seaborn practice (telecom_churn.csv)
(1) Histogram of `monthly_charges` by churn. (2) Box plot of `tenure_months` by contract. (3) Churn rate by payment method, sorted. (4) Correlation heatmap of numeric columns plus `churned`. (5) Write three insight titles from what you see.
???
```python
sns.histplot(tc, x="monthly_charges", hue="churn", common_norm=False, stat="density")
sns.boxplot(tc, x="contract", y="tenure_months")
order = tc.groupby("payment_method")["churned"].mean().sort_values(ascending=False).index
sns.barplot(tc, x="payment_method", y="churned", order=order, errorbar=None)
sns.heatmap(tc.select_dtypes("number").corr(), annot=True, fmt=".2f", cmap="RdBu_r", center=0)
# e.g. "Month-to-month customers churn far more", "Churners have short tenure", "Churn rises with support calls"
```
:::

:::interview Questions you may be asked
**Q: How would you visualise the relationship between a categorical and a numeric variable?**
Box or violin plots per category (distribution), or bar/point plots of the mean with confidence intervals.

**Q: How do you show correlations among many numeric variables?**
A correlation heatmap (masked upper triangle) followed by scatter plots for the interesting pairs; a pair plot for a handful of variables.

**Q: How do you present findings to non-technical stakeholders?**
Lead with the recommendation, show one clear chart per point with an insight title, quantify impact, and keep methods in an appendix.
:::
