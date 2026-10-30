---
num: 1
title: "Descriptive Statistics: Centre, Spread, Shape and Relationships"
live: "Python class 14"
updated: "pandas 3 · SciPy 1.1x"
level: Beginner
duration: 100 min
summary: Describe data with numbers before modelling it. Types of data and measurement scales, mean, median and mode, range, variance, standard deviation, IQR and coefficient of variation, percentiles and z-scores, skewness and kurtosis, covariance and correlation (Pearson and Spearman), all on the house-price and HR datasets.
datasets: [house_prices.csv, hr_employees.csv]
outcomes:
  - Classify variables as categorical (nominal, ordinal) or numeric (discrete, continuous; interval, ratio)
  - Compute and interpret mean, median, mode, weighted mean and trimmed mean
  - Compute and interpret range, IQR, variance, standard deviation and coefficient of variation
  - Use percentiles and z-scores and describe skewness and kurtosis
  - Measure association with covariance, Pearson and Spearman correlation, and explain why correlation is not causation
---

## Statistics in data science

**Descriptive statistics** summarise the data you have. **Inferential statistics** use a sample to draw conclusions about a larger population (next lessons). Machine learning builds on both.

```python fig: The statistics roadmap for this track.
dg.flow(["Describe\n(this lesson)", "Probability &\ndistributions", "Sampling\n& CLT", "Hypothesis\ntests", "A/B tests", "Models\n(ML)"], title="From description to prediction")
```

## Types of data

```python fig: Variable types decide which statistics and charts make sense.
dg.tree("Variable", {"Categorical (qualitative)": ["Nominal: city, gender", "Ordinal: rating 1–5, education"], "Numeric (quantitative)": ["Discrete: bedrooms, calls", "Continuous: price, time"]}, title="Types of data")
```

| Scale | Has order? | Equal intervals? | True zero? | Example | Allowed statistics |
|---|---|---|---|---|---|
| Nominal | No | – | – | City | Mode, counts |
| Ordinal | Yes | No | – | Satisfaction 1–4 | Median, percentiles |
| Interval | Yes | Yes | No | Temperature °C | Mean, sd (no ratios) |
| Ratio | Yes | Yes | Yes | Income, price | Everything, including ratios |

## Measures of centre

```python run
import pandas as pd, numpy as np
from scipy import stats
h = pd.read_csv("house_prices.csv")
p = h["price_lakh"]
print(f"mean {p.mean():.1f} | median {p.median():.1f} | mode (rounded to 10) {(p.round(-1)).mode()[0]:.0f} | trimmed mean 10% {stats.trim_mean(p, 0.1):.1f}")
print("bedrooms mode:", h["bedrooms"].mode().tolist(), "| city mode:", h["city"].mode()[0])
w = pd.DataFrame({"city_avg_price": [62, 88, 75], "houses": [100, 20, 50]})
print("simple mean of city averages:", w.city_avg_price.mean().round(1), "| weighted mean:", np.average(w.city_avg_price, weights=w.houses).round(1))
```

| Measure | Use when | Sensitive to outliers? |
|---|---|---|
| Mean | Symmetric numeric data; totals matter | Yes |
| Median | Skewed data (income, prices), ordinal data | No |
| Mode | Categories, most common value | No |
| Trimmed mean | Want a mean but robust to extremes | Less |
| Weighted mean | Groups of different sizes | Depends |

```python run
salaries = pd.Series([40, 42, 45, 47, 50, 52, 55, 60, 65, 900])      # one CEO in thousands
print(f"mean {salaries.mean():.1f}K vs median {salaries.median():.1f}K: one extreme value moves the mean, not the median")
```

## Measures of spread

```python run
def spread(x):
    q1, q3 = x.quantile([.25, .75])
    return pd.Series({"range": x.max() - x.min(), "IQR": q3 - q1, "variance": x.var(), "std": x.std(), "CV_%": 100 * x.std() / x.mean(), "MAD": (x - x.median()).abs().median()})
print(pd.DataFrame({"price_lakh": spread(p), "area_sqft": spread(h["area_sqft"].dropna()), "age_years": spread(h["age_years"])}).round(1))
```

- **Variance** = average squared distance from the mean; **standard deviation** (sd) = its square root, in the original units.
- pandas `.std()` uses the **sample** formula (divide by *n − 1*, Bessel's correction); NumPy `np.std` defaults to population (*n*).
- **Coefficient of variation** (CV = sd ÷ mean) compares spread across variables with different units.
- **IQR** (Q3 − Q1) is the spread of the middle 50%, robust to outliers.

$$s = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar x)^2}$$

## Percentiles, z-scores and the five-number summary

```python run
print(p.quantile([0, .1, .25, .5, .75, .9, 1]).round(1).to_dict())
z = (p - p.mean()) / p.std()
print(f"a ₹150 lakh house has z = {(150 - p.mean()) / p.std():.2f} | {(z.abs() > 2).mean():.1%} of houses are beyond ±2 sd")
print(f"percentile rank of ₹150 lakh: {stats.percentileofscore(p, 150):.1f}")
```

A **z-score** says how many standard deviations a value is from the mean: it puts different variables on one scale (used in standardisation for ML).

## Shape: skewness and kurtosis

```python fig: Right-skewed (income), roughly symmetric (age) and the mean/median positions.
import matplotlib.pyplot as plt
hr = pd.read_csv("hr_employees.csv")
fig, axes = plt.subplots(1, 2, figsize=(10, 3.3))
for ax, col, c in zip(axes, ["monthly_income", "age"], ["#7C3AED", "#0E9F8E"]):
    x = hr[col]; ax.hist(x, bins=30, color=c, alpha=.35)
    ax.axvline(x.mean(), color="#DB2777", lw=2, label=f"mean {x.mean():,.0f}"); ax.axvline(x.median(), color="#333", ls="--", lw=2, label=f"median {x.median():,.0f}")
    ax.set_title(f"{col}: skew {x.skew():.2f}", loc="left", weight="bold"); ax.legend(frameon=False, fontsize=8); ax.spines[["top", "right"]].set_visible(False); ax.set_yticks([])
```

```python run
for col in ["monthly_income", "age", "years_at_company", "distance_from_home_km"]:
    x = hr[col]; print(f"{col:24s} skew {x.skew():6.2f} | excess kurtosis {x.kurt():6.2f} | mean {x.mean():10,.1f} | median {x.median():10,.1f}")
print("log(income) skew:", round(np.log(hr.monthly_income).skew(), 2))
```

| Skewness | Shape | Mean vs median |
|---|---|---|
| ≈ 0 | Symmetric | Mean ≈ median |
| > 0 | Right (positive) skew, long right tail | Mean > median |
| < 0 | Left skew | Mean < median |

**Kurtosis** describes tail heaviness (excess kurtosis 0 = normal; positive = more extreme values). A log transform often makes right-skewed money variables more symmetric.

## Relationships: covariance and correlation

```python run
num = h[["price_lakh", "area_sqft", "bedrooms", "age_years", "distance_to_center_km"]].dropna()
print("covariance price-area:", round(num.price_lakh.cov(num.area_sqft), 1), "(units: lakh × sq ft, hard to interpret)")
print(num.corr().round(2)["price_lakh"].sort_values(ascending=False))
print("Spearman (rank):", num.corr(method="spearman").round(2)["price_lakh"].drop("price_lakh").to_dict())
r, pval = stats.pearsonr(num.area_sqft, num.price_lakh); print(f"Pearson r = {r:.3f}, p-value = {pval:.1e}")
```

- **Pearson r** measures linear association (−1 to +1). Rough guide: |r| < 0.3 weak, 0.3–0.7 moderate, > 0.7 strong.
- **Spearman ρ** correlates ranks: robust to outliers and captures monotonic non-linear relations.
- **Cramér's V** (categorical × categorical) and point-biserial (binary × numeric) cover other pairs.

```python fig: Anscombe's quartet: four datasets with the same mean, variance and correlation (r ≈ 0.82) but completely different shapes. Always plot your data.
import seaborn as sns
a = pd.DataFrame({"dataset": np.repeat(list("ABCD"), 11),
    "x": [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5] * 3 + [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8],
    "y": [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68, 9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74, 7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73, 6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]})
fig, axes = plt.subplots(1, 4, figsize=(12, 2.8), sharey=True)
for ax, (k, d) in zip(axes, a.groupby("dataset")):
    ax.scatter(d.x, d.y, color="#7C3AED", s=18); b, c0 = np.polyfit(d.x, d.y, 1); xs = np.array([3, 20]); ax.plot(xs, c0 + b * xs, color="#DB2777")
    ax.set_title(f"{k}: r = {np.corrcoef(d.x, d.y)[0, 1]:.2f}", fontsize=10); ax.spines[["top", "right"]].set_visible(False)
```

:::warning Correlation is not causation
Ice-cream sales and drowning both rise in summer (a **confounder**: temperature). Correlation can also come from reverse causation, selection bias or chance. Only experiments or careful causal methods show cause.
:::

## Summary

:::key
- Know the variable type and scale first: it decides valid statistics.
- Centre: mean (sensitive), median (robust), mode (categories); use weighted means for groups of different sizes.
- Spread: range, IQR (robust), variance and sd (sample uses n − 1), CV to compare variables.
- Shape: skewness (mean vs median), kurtosis (tails); log transforms reduce right skew.
- z-scores standardise; percentiles rank. Correlation (Pearson linear, Spearman rank) measures association, not causation; always plot.
:::

:::quiz
Q: Which is the best measure of centre for household income?
- Mean
* Median
- Mode
- Range
> Income is right-skewed; the median resists extremes.

Q: In a right-skewed distribution, which is usually true?
* Mean > median
- Mean < median
- Mean = median
- Mode > mean
> The long right tail pulls the mean up.

Q: Why does the sample standard deviation divide by n − 1?
- To make it larger for fun
* To correct the bias from estimating the mean from the same sample (Bessel's correction)
- Because n is unknown
- It is a convention with no reason
> It gives an unbiased variance estimate.

Q: A z-score of −1.5 means…
* The value is 1.5 standard deviations below the mean
- The value is negative
- The value is in the 15th percentile exactly
- An error
> z = (x − mean) / sd.

Q: Which correlation suits a monotonic but non-linear relationship?
- Pearson
* Spearman
- Covariance
- None
> Spearman uses ranks.

Q: What does Anscombe's quartet teach?
- Correlation proves causation
* Identical summary statistics can hide very different patterns, so plot the data
- Means are useless
- Outliers never matter
> Visualise before you summarise.
:::

:::exercise Practice (hr_employees.csv)
(1) Mean, median and sd of `monthly_income` by department; which department is most variable (CV)? (2) The 90th percentile of income. (3) The share of employees beyond ±3 sd of income. (4) Pearson and Spearman correlation between age and income. (5) Classify each column by type and scale.
???
```python
g = hr.groupby("department")["monthly_income"].agg(["mean", "median", "std"]); g["cv"] = g["std"] / g["mean"]; print(g.sort_values("cv"))
print(hr.monthly_income.quantile(.9))
zi = (hr.monthly_income - hr.monthly_income.mean()) / hr.monthly_income.std(); print((zi.abs() > 3).mean())
print(hr[["age", "monthly_income"]].corr().iloc[0, 1], hr[["age", "monthly_income"]].corr("spearman").iloc[0, 1])
# gender, department, city: nominal; education, job_satisfaction, performance_rating: ordinal; age, income: ratio
```
:::

:::interview Questions you may be asked
**Q: Mean vs median: when do you report each?**
Median for skewed data or outliers (income, house prices, delivery times); mean for symmetric data or when totals matter.

**Q: What does a standard deviation of 0 mean?**
All values are identical.

**Q: Correlation is 0. Are the variables independent?**
Not necessarily: Pearson only captures linear relationships; a perfect U-shape can have r = 0.
:::
