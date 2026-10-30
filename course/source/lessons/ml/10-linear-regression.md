---
num: 10
title: "Linear Regression: Fitting, Interpreting, Assumptions and Diagnostics"
live: "Python class 16 · ML class 4"
updated: "statsmodels 0.1x · scikit-learn 1.7+"
level: Intermediate
duration: 130 min
summary: Predict a number and explain it. Simple and multiple linear regression with ordinary least squares, interpreting coefficients, dummy variables and log targets, R², adjusted R², RMSE and MAE, the LINE assumptions and residual diagnostics, multicollinearity and VIF, outliers and influence, with statsmodels for inference and scikit-learn for prediction on the house-price data.
datasets: [house_prices.csv]
outcomes:
  - Fit simple and multiple linear regression with statsmodels and scikit-learn
  - Interpret intercepts, slopes, dummy variables and log-transformed coefficients
  - Evaluate models with R², adjusted R², MAE, RMSE and MAPE on test data
  - Check linearity, independence, normality and equal variance of residuals
  - Detect multicollinearity with VIF and influential points with Cook's distance
---

## Simple linear regression

Find the straight line that best predicts *y* from *x*:

$$\hat y = \beta_0 + \beta_1 x$$

**Ordinary least squares (OLS)** chooses β₀ and β₁ to minimise the **sum of squared residuals**, where a residual is actual − predicted.

```python run
import pandas as pd, numpy as np
import statsmodels.formula.api as smf
h = pd.read_csv("house_prices.csv").dropna(subset=["area_sqft"])
pps = h.price_lakh * 1e5 / h.area_sqft                          # price per sq ft
h = h[pps.between(pps.median() / 3, pps.median() * 3)]          # drop 4 impossible prices (data-entry errors found in EDA)
print(len(h), "houses")
m1 = smf.ols("price_lakh ~ area_sqft", data=h).fit()
print(m1.params.round(4).to_dict(), "| R² =", round(m1.rsquared, 3))
b0, b1 = m1.params
print(f"price ≈ {b0:.2f} + {b1:.4f} × area → each extra 100 sq ft adds about ₹{100 * b1:.1f} lakh")
print("prediction for 1,500 sq ft:", round(m1.predict(pd.DataFrame({"area_sqft": [1500]}))[0], 1), "lakh")
```

```python fig: The least-squares line and the residuals (vertical distances) it minimises, for 40 sample houses.
import matplotlib.pyplot as plt
s = h.sample(40, random_state=3)
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.scatter(h.area_sqft, h.price_lakh, s=5, color="#DDD6FE")
pred = b0 + b1 * s.area_sqft
ax.vlines(s.area_sqft, pred, s.price_lakh, color="#DB2777", lw=1, alpha=.8); ax.scatter(s.area_sqft, s.price_lakh, s=16, color="#7C3AED", zorder=3)
xs = np.array([h.area_sqft.min(), h.area_sqft.max()]); ax.plot(xs, b0 + b1 * xs, color="#1F1B2E", lw=2)
ax.set_xlabel("area (sq ft)"); ax.set_ylabel("price (₹ lakh)"); ax.spines[["top", "right"]].set_visible(False)
```

## Multiple linear regression

```python run
m2 = smf.ols("price_lakh ~ area_sqft + bedrooms + bathrooms + age_years + distance_to_center_km + parking + C(city)", data=h).fit()
print(m2.summary().tables[1])
print(f"R² {m2.rsquared:.3f} | adjusted R² {m2.rsquared_adj:.3f} | F-test p {m2.f_pvalue:.1e} | n = {int(m2.nobs)}")
```

### Reading the output

| Column | Meaning |
|---|---|
| `coef` | Change in predicted price for +1 unit of the feature, **holding the others constant** |
| `std err` | Uncertainty of the coefficient |
| `t`, `P>|t|` | Test of H₀: coefficient = 0 |
| `[0.025 0.975]` | 95% confidence interval |
| `C(city)[T.X]` | Dummy variable: difference from the **reference city** (the first alphabetically) |

```python run
coef = m2.params; ci = m2.conf_int()
for f in ["area_sqft", "age_years", "distance_to_center_km", "parking"]:
    print(f"{f:22s} {coef[f]:+8.3f} lakh per unit (95% CI {ci.loc[f, 0]:+.3f} to {ci.loc[f, 1]:+.3f}), p = {m2.pvalues[f]:.3g}")
ref = sorted(h.city.unique())[0]
print(f"city effects vs {ref}:", {k.split('T.')[1][:-1]: round(v, 1) for k, v in coef.items() if k.startswith("C(city)")})
```

Coefficients are **associations conditional on the other features**, not proof that renovating (changing age) would cause that price change.

### Log target: percentage effects

Prices are right-skewed and effects are often multiplicative. Modelling log(price) turns coefficients into approximate percentage effects.

```python run
m3 = smf.ols("np.log(price_lakh) ~ np.log(area_sqft) + bedrooms + bathrooms + age_years + distance_to_center_km + parking + C(city)", data=h).fit()
print(f"elasticity: +1% area → +{m3.params['np.log(area_sqft)']:.2f}% price | each year of age → {100 * (np.exp(m3.params['age_years']) - 1):+.2f}% | R² (log scale) {m3.rsquared:.3f}")
```

## Evaluating predictions

```python run
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
train, test = train_test_split(h, test_size=0.2, random_state=0)
fit = smf.ols("price_lakh ~ area_sqft + bedrooms + bathrooms + age_years + distance_to_center_km + parking + C(city)", data=train).fit()
p_train, p_test = fit.predict(train), fit.predict(test)
for name, yt, yp in [("train", train.price_lakh, p_train), ("test", test.price_lakh, p_test)]:
    print(f"{name:5s} R² {r2_score(yt, yp):.3f} | MAE {mean_absolute_error(yt, yp):.2f} | RMSE {mean_squared_error(yt, yp) ** 0.5:.2f} | MAPE {100 * mean_absolute_percentage_error(yt, yp):.1f}%")
```

| Metric | Formula idea | Read as |
|---|---|---|
| **MAE** | mean \|error\| | Typical error in target units; robust |
| **RMSE** | √mean(error²) | Penalises large errors more |
| **MAPE** | mean \|error\| / actual | Percentage error; unstable near 0 |
| **R²** | 1 − SSE/SST | Share of variance explained (0–1 on test; can be negative) |
| **Adjusted R²** | R² penalised for number of features | Compare models with different feature counts |

Similar train and test scores mean the model generalises; a large gap signals overfitting.

## Assumptions (LINE) and diagnostics

| Assumption | Meaning | Check | If violated |
|---|---|---|---|
| **L**inearity | Mean of y is linear in features | Residuals vs fitted: no curve | Transform, add polynomial terms, use trees |
| **I**ndependence | Errors not related to each other | Durbin-Watson ≈ 2; study design | Time-series models, clustered errors |
| **N**ormality | Residuals ~ normal | Q-Q plot, histogram | Matters for small-sample inference; transform y |
| **E**qual variance | Constant spread of residuals | Residuals vs fitted: no funnel; Breusch-Pagan | log(y), robust (HC3) standard errors |

```python fig: Residual diagnostics for the multiple regression. Left: residuals vs fitted values. Right: Q-Q plot of residuals.
from scipy import stats
res, fitted = m2.resid, m2.fittedvalues
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.4))
a1.scatter(fitted, res, s=6, color="#7C3AED", alpha=.5); a1.axhline(0, color="#DB2777")
a1.set_xlabel("fitted price"); a1.set_ylabel("residual"); a1.set_title("Residuals vs fitted", loc="left", weight="bold")
(osm, osr), (sl, ic, _) = stats.probplot(res); a2.scatter(osm, osr, s=6, color="#7C3AED"); a2.plot(osm, sl * osm + ic, color="#DB2777")
a2.set_title("Normal Q-Q of residuals", loc="left", weight="bold")
for a in (a1, a2): a.spines[["top", "right"]].set_visible(False)
```

```python run
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
bp = het_breuschpagan(m2.resid, m2.model.exog)
print(f"Breusch-Pagan p = {bp[1]:.2e} ({'unequal variance (heteroscedastic)' if bp[1] < 0.05 else 'equal variance OK'}) | Durbin-Watson {durbin_watson(m2.resid):.2f} | residual skew {stats.skew(m2.resid):.2f}")
robust = smf.ols(m2.model.formula, data=h).fit(cov_type="HC3")
print("area_sqft p-value: ordinary", f"{m2.pvalues['area_sqft']:.2e}", "| robust HC3", f"{robust.pvalues['area_sqft']:.2e}")
```

## Multicollinearity

When features are strongly correlated with each other, coefficients become unstable and hard to interpret (predictions can still be fine).

```python run
from statsmodels.stats.outliers_influence import variance_inflation_factor
Xv = h[["area_sqft", "bedrooms", "bathrooms", "age_years", "distance_to_center_km", "parking"]].assign(const=1.0)
vif = pd.Series([variance_inflation_factor(Xv.values, i) for i in range(Xv.shape[1] - 1)], index=Xv.columns[:-1]).round(2)
print(vif.sort_values(ascending=False).to_dict())
print(h[["area_sqft", "bedrooms", "bathrooms"]].corr().round(2))
```

**VIF** above about 5–10 signals a problem. Fixes: drop or combine correlated features, use regularisation (Ridge, lesson 12), or PCA.

## Outliers and influential points

```python run
infl = m2.get_influence(); cooks = infl.cooks_distance[0]
top = np.argsort(cooks)[-3:][::-1]
print("largest Cook's distances:", cooks[top].round(3), "| threshold 4/n =", round(4 / len(h), 4))
print(h.iloc[top][["city", "area_sqft", "bedrooms", "price_lakh"]])
```

Investigate influential points: data errors should be fixed; genuine extremes may need robust methods (Huber regression) or separate treatment.

## scikit-learn version

```python run
from sklearn.linear_model import LinearRegression
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
feats = ["area_sqft", "bedrooms", "bathrooms", "age_years", "distance_to_center_km", "parking", "city"]
pipe = make_pipeline(make_column_transformer((OneHotEncoder(drop="first"), ["city"]), remainder="passthrough"), LinearRegression())
pipe.fit(train[feats], train.price_lakh)
print(f"sklearn test R² {pipe.score(test[feats], test.price_lakh):.3f} (same model as statsmodels: {np.isclose(pipe.score(test[feats], test.price_lakh), r2_score(test.price_lakh, p_test))})")
```

Use **statsmodels** for inference (p-values, CIs, diagnostics) and **scikit-learn** for prediction pipelines, cross-validation and deployment.

## Summary

:::key
- OLS minimises squared residuals; coefficients are the change in y per unit of x, holding other features constant.
- Dummy variables compare categories with a reference; log targets give percentage effects.
- Evaluate on test data with MAE, RMSE, MAPE and R²; adjusted R² penalises extra features.
- Check LINE assumptions with residual plots, Q-Q plots, Breusch-Pagan and Durbin-Watson; use robust standard errors or transformations when needed.
- VIF detects multicollinearity; Cook's distance finds influential points. Coefficients show association, not causation.
:::

:::quiz
Q: What does OLS minimise?
- The sum of absolute errors
* The sum of squared residuals
- The number of features
- The p-values
> Hence "least squares".

Q: The coefficient of `age_years` is −0.6. Interpretation?
* Each additional year of age is associated with ₹0.6 lakh lower price, holding other features constant
- Older houses cost 60% less
- Age causes prices to fall
- Age is not significant
> Conditional association, in target units.

Q: Residuals fan out as fitted values grow. Which assumption is violated?
- Linearity
- Independence
* Equal variance (homoscedasticity)
- Normality only
> Try log(y) or robust standard errors.

Q: What does a VIF of 12 indicate?
* Strong multicollinearity with other features
- A great feature
- Non-normal residuals
- An outlier
> Coefficients become unstable.

Q: Test R² is 0.90 and train R² is 0.91. What does that suggest?
* The model generalises well (no strong overfitting)
- Severe overfitting
- Data leakage for sure
- Underfitting
> Similar scores on unseen data are good news.

Q: Why use a log target for prices?
* Prices are skewed and effects are multiplicative; coefficients become percentage effects
- To make R² larger always
- Because statsmodels requires it
- To remove outliers
> It also stabilises variance.
:::

:::exercise Practice
(1) Add `area_sqft:C(city)` interaction: does the price per sq ft differ by city? (2) Compare test MAE of the plain and log-target models (back-transform with `np.exp`). (3) Remove the feature with the highest VIF and compare adjusted R². (4) Plot actual vs predicted on the test set.
???
```python
mi = smf.ols("price_lakh ~ area_sqft * C(city) + bedrooms + bathrooms + age_years + distance_to_center_km + parking", data=h).fit()
print(mi.params.filter(like="area_sqft:"))
lg = smf.ols("np.log(price_lakh) ~ area_sqft + bedrooms + bathrooms + age_years + distance_to_center_km + parking + C(city)", data=train).fit()
print(mean_absolute_error(test.price_lakh, np.exp(lg.predict(test))), mean_absolute_error(test.price_lakh, p_test))
m_novif = smf.ols("price_lakh ~ area_sqft + bathrooms + age_years + distance_to_center_km + parking + C(city)", data=h).fit(); print(m_novif.rsquared_adj, m2.rsquared_adj)
plt.scatter(test.price_lakh, p_test, s=6); plt.plot([0, 300], [0, 300])
```
:::

:::interview Questions you may be asked
**Q: What are the assumptions of linear regression?**
Linearity, independence of errors, normality of residuals (for inference), equal variance of residuals, and no perfect multicollinearity.

**Q: R² vs adjusted R²?**
R² never decreases when you add features; adjusted R² penalises the number of features, so it can drop when a feature adds little.

**Q: How do you interpret a coefficient in a log-log model?**
As an elasticity: a 1% change in x is associated with a β% change in y.
:::
