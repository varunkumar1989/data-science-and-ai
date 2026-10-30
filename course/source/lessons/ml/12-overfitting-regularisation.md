---
num: 12
title: "Overfitting, Polynomial Regression and Regularisation (Ridge, Lasso, Elastic Net)"
live: "ML class 6"
updated: "scikit-learn 1.7+"
level: Intermediate
duration: 110 min
summary: See overfitting and underfitting happen, learn the bias-variance trade-off with polynomial regression, and control model complexity with L2 (Ridge), L1 (Lasso) and Elastic Net penalties, including choosing the penalty strength with cross-validation, feature selection with Lasso, and learning curves.
datasets: [house_prices.csv, hr_employees.csv]
outcomes:
  - Recognise underfitting and overfitting from train vs test errors and plots
  - Explain the bias-variance trade-off and how model complexity affects it
  - Fit polynomial regression and control its degree
  - Apply Ridge, Lasso and Elastic Net and tune alpha with RidgeCV/LassoCV
  - Use learning and validation curves to decide between more data and a different model
---

## Underfitting and overfitting

```python fig: Polynomial models of degree 1, 4 and 15 on the same noisy data. Degree 1 underfits, degree 4 fits well, degree 15 chases noise.
import numpy as np, matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, RidgeCV, LassoCV
from sklearn.pipeline import make_pipeline
rng = np.random.default_rng(1)
x = np.sort(rng.uniform(0, 1, 15)); y = np.sin(2 * np.pi * x) + rng.normal(0, .25, 15)      # only 15 training points
xs = np.linspace(0, 1, 300)
fig, axes = plt.subplots(1, 3, figsize=(11.5, 3))
for ax, d, t in zip(axes, (1, 4, 15), ("underfit (high bias)", "good fit", "overfit (high variance)")):
    m = make_pipeline(PolynomialFeatures(d), StandardScaler(), LinearRegression()).fit(x[:, None], y)
    ax.scatter(x, y, s=14, color="#7C3AED"); ax.plot(xs, m.predict(xs[:, None]), color="#DB2777", lw=2); ax.plot(xs, np.sin(2 * np.pi * xs), color="#999", ls="--", lw=1)
    ax.set_ylim(-2.2, 2.2); ax.set_title(f"degree {d}: {t}", fontsize=10, weight="bold"); ax.set_xticks([]); ax.set_yticks([])
```

| | Underfitting | Good fit | Overfitting |
|---|---|---|---|
| Training error | High | Low | Very low |
| Test error | High | Low | High |
| Cause | Model too simple, missing features | | Model too complex, too little data, leakage |
| Fix | More features, more flexible model, less regularisation | | More data, simpler model, regularisation, feature selection, early stopping |

## The bias-variance trade-off

**Bias** is the error from wrong assumptions (a line for a curve). **Variance** is the error from sensitivity to the particular training sample. Total expected error = bias² + variance + irreducible noise.

```python run
from sklearn.metrics import mean_squared_error
x_test = rng.uniform(0, 1, 500); y_test = np.sin(2 * np.pi * x_test) + rng.normal(0, .25, 500)
for d in (1, 2, 3, 4, 6, 9, 12, 15):
    m = make_pipeline(PolynomialFeatures(d), StandardScaler(), LinearRegression()).fit(x[:, None], y)
    tr = mean_squared_error(y, m.predict(x[:, None])); te = mean_squared_error(y_test, m.predict(x_test[:, None]))
    print(f"degree {d:2d}: train MSE {tr:7.3f} | test MSE {te:10.3f}")
```

```python fig: As complexity grows, training error keeps falling while test error falls then rises: the sweet spot is in between.
ds = range(1, 16); tr_e, te_e = [], []
for d in ds:
    m = make_pipeline(PolynomialFeatures(d), StandardScaler(), LinearRegression()).fit(x[:, None], y)
    tr_e.append(mean_squared_error(y, m.predict(x[:, None]))); te_e.append(mean_squared_error(y_test, m.predict(x_test[:, None])))
fig, ax = plt.subplots(figsize=(8, 3.2)); ax.plot(ds, tr_e, "o-", color="#7C3AED", label="training error"); ax.plot(ds, te_e, "o-", color="#DB2777", label="test error")
ax.set_yscale("log"); ax.set_xlabel("polynomial degree (model complexity)"); ax.set_ylabel("MSE (log)"); ax.legend(frameon=False); ax.spines[["top", "right"]].set_visible(False)
```

## Regularisation

Instead of choosing fewer features by hand, add a **penalty** on large coefficients to the cost:

$$\text{Ridge (L2):}\; J = \text{MSE} + \alpha\sum_j w_j^2 \qquad \text{Lasso (L1):}\; J = \text{MSE} + \alpha\sum_j |w_j|$$

**Elastic Net** mixes both (`l1_ratio`). Larger α means stronger shrinkage, simpler models, more bias and less variance. Always **scale features** first, so the penalty treats them fairly.

```python run
for name, model in [("no penalty", LinearRegression()), ("Ridge α=0.01", Ridge(alpha=0.01)), ("Lasso α=0.001", Lasso(alpha=0.001, max_iter=100000))]:
    m = make_pipeline(PolynomialFeatures(15), StandardScaler(), model).fit(x[:, None], y)
    coefs = m[-1].coef_
    print(f"degree-15 {name:12s} test MSE {mean_squared_error(y_test, m.predict(x_test[:, None])):9.3f} | largest |coef| {np.abs(coefs).max():12.1f} | zero coefs {(np.abs(coefs) < 1e-8).sum():2d} of {len(coefs)}")
```

The same degree-15 model becomes well behaved once its coefficients are penalised. **Lasso** sets some coefficients exactly to zero (automatic feature selection); **Ridge** shrinks all of them smoothly and handles correlated features well.

```python fig: Coefficient paths: as α grows, Ridge shrinks every coefficient gradually while Lasso drops features to exactly zero one by one.
import pandas as pd
hr = pd.read_csv("hr_employees.csv")
Xh = pd.get_dummies(hr[["age", "years_at_company", "job_satisfaction", "distance_from_home_km", "performance_rating", "overtime", "department"]], drop_first=True).astype(float)
yh = np.log(hr.monthly_income)
Xs = StandardScaler().fit_transform(Xh); alphas = np.logspace(-4, 1, 60)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.4))
a1.plot(alphas, [Ridge(alpha=a * 1000).fit(Xs, yh).coef_ for a in alphas]); a1.set_title("Ridge (L2)", loc="left", weight="bold")
a2.plot(alphas, [Lasso(alpha=a / 10, max_iter=20000).fit(Xs, yh).coef_ for a in alphas]); a2.set_title("Lasso (L1)", loc="left", weight="bold")
for a in (a1, a2): a.set_xscale("log"); a.set_xlabel("α (penalty strength)"); a.axhline(0, color="#999", lw=.8); a.spines[["top", "right"]].set_visible(False)
```

## Choosing α with cross-validation

```python run
from sklearn.model_selection import train_test_split, cross_val_score
h = pd.read_csv("house_prices.csv").dropna(subset=["area_sqft"])
pps = h.price_lakh * 1e5 / h.area_sqft; h = h[pps.between(pps.median() / 3, pps.median() * 3)]
X = pd.get_dummies(h.drop(columns=["house_id", "price_lakh"]), columns=["city"], drop_first=True).astype(float); yv = h.price_lakh
Xtr, Xte, ytr, yte = train_test_split(X, yv, test_size=0.2, random_state=0)
poly = lambda est: make_pipeline(PolynomialFeatures(2, include_bias=False), StandardScaler(), est)
models = {"linear (degree 2)": poly(LinearRegression()), "RidgeCV": poly(RidgeCV(alphas=np.logspace(-3, 3, 30))),
          "LassoCV": poly(LassoCV(cv=5, random_state=0, max_iter=50000)), "ElasticNet": poly(ElasticNet(alpha=0.05, l1_ratio=0.5, max_iter=50000))}
for name, m in models.items():
    m.fit(Xtr, ytr); cv = cross_val_score(m, Xtr, ytr, cv=5, scoring="neg_root_mean_squared_error").mean()
    extra = f" | α = {m[-1].alpha_:.4g}" if hasattr(m[-1], "alpha_") else ""
    nz = f" | non-zero coefs {(m[-1].coef_ != 0).sum()} of {len(m[-1].coef_)}"
    print(f"{name:18s} CV RMSE {-cv:6.2f} | test RMSE {mean_squared_error(yte, m.predict(Xte)) ** .5:6.2f}{extra}{nz}")
```

With about 900 training rows and 54 polynomial features, all models perform similarly here; Lasso reaches the same accuracy with far fewer terms. Regularisation matters most when features are many relative to rows, or strongly correlated.

## Learning curves: more data or a better model?

```python fig: Learning curves for a degree-2 Ridge model on house prices: the training and validation errors converge as data grows, so more data would help little; a more flexible model or better features would help more.
from sklearn.model_selection import learning_curve
sizes, tr_s, va_s = learning_curve(poly(Ridge(alpha=1)), Xtr, ytr, cv=5, scoring="neg_root_mean_squared_error", train_sizes=np.linspace(.1, 1, 8), shuffle=True, random_state=0)
fig, ax = plt.subplots(figsize=(8, 3.2))
ax.plot(sizes, -tr_s.mean(1), "o-", color="#7C3AED", label="training RMSE"); ax.plot(sizes, -va_s.mean(1), "o-", color="#DB2777", label="validation RMSE")
ax.set_xlabel("training examples"); ax.set_ylabel("RMSE (₹ lakh)"); ax.legend(frameon=False); ax.spines[["top", "right"]].set_visible(False)
```

| Learning-curve pattern | Diagnosis | Action |
|---|---|---|
| Both errors high and close | High bias (underfitting) | More features, more complex model |
| Big gap: low train, high validation | High variance (overfitting) | More data, regularisation, simpler model |
| Gap closing as data grows | Variance falling | Collect more data |

## Regularisation beyond linear models

| Model | Regularisation knobs |
|---|---|
| Logistic regression | `C` = 1/α (smaller C = stronger penalty), `penalty="l1"/"l2"/"elasticnet"` |
| Decision trees | `max_depth`, `min_samples_leaf`, pruning (`ccp_alpha`) |
| Random forests / boosting | Tree depth, number of trees, learning rate, subsampling |
| Neural networks | Weight decay (L2), dropout, early stopping, data augmentation |
| KNN | Larger k = smoother |

## Summary

:::key
- Underfitting: high error everywhere (bias). Overfitting: low training error, high test error (variance).
- Polynomial features add flexibility; the degree controls the bias-variance trade-off.
- Ridge (L2) shrinks coefficients; Lasso (L1) zeroes some (feature selection); Elastic Net combines them. Scale features first.
- Pick α by cross-validation (RidgeCV, LassoCV, GridSearchCV).
- Learning curves tell you whether more data or a different model will help.
:::

:::quiz
Q: Training error 2%, test error 25%. Diagnosis?
- Underfitting
* Overfitting (high variance)
- Perfect model
- Data too large
> The model memorised the training data.

Q: Which penalty can set coefficients exactly to zero?
- Ridge (L2)
* Lasso (L1)
- No penalty
- Both equally
> L1 performs feature selection.

Q: What happens as α increases in Ridge regression?
* Coefficients shrink, bias rises and variance falls
- Coefficients grow
- The model overfits more
- Nothing
> Stronger penalty = simpler model.

Q: Why scale features before regularisation?
* So the penalty treats all coefficients fairly regardless of units
- To speed up printing
- To remove outliers
- It is optional
> Otherwise large-unit features are under-penalised.

Q: In logistic regression in scikit-learn, a smaller C means…
* Stronger regularisation
- Weaker regularisation
- More features
- No effect
> C is the inverse of α.

Q: Learning curves show training and validation errors both high and close together. What helps?
- More data
* A more flexible model or better features
- Stronger regularisation
- Fewer features
> This is high bias.
:::

:::exercise Practice
(1) Plot validation curves (`validation_curve`) of Ridge alpha for the house data. (2) Fit `LogisticRegressionCV` with L1 penalty on the HR attrition data: which features survive? (3) Compare degree 1, 2 and 3 polynomial Ridge models with 5-fold CV.
???
```python
from sklearn.model_selection import validation_curve
from sklearn.linear_model import LogisticRegressionCV
al = np.logspace(-3, 3, 13)
tr_, va_ = validation_curve(poly(Ridge()), Xtr, ytr, param_name="ridge__alpha", param_range=al, cv=5, scoring="neg_root_mean_squared_error")
yb = (hr.attrition == "Yes").astype(int)
lr1 = LogisticRegressionCV(penalty="l1", solver="saga", Cs=10, cv=5, max_iter=5000).fit(StandardScaler().fit_transform(Xh), yb)
print(Xh.columns[lr1.coef_[0] != 0].tolist())
for d in (1, 2, 3): print(d, cross_val_score(make_pipeline(PolynomialFeatures(d, include_bias=False), StandardScaler(), Ridge(1)), Xtr, ytr, cv=5, scoring="r2").mean())
```
:::

:::interview Questions you may be asked
**Q: Explain the bias-variance trade-off.**
Simple models have high bias (systematic error) and low variance; complex models have low bias but high variance (sensitivity to the training sample). We choose complexity that minimises total error on new data.

**Q: L1 vs L2 regularisation?**
L2 shrinks coefficients towards zero and handles correlated features; L1 can set coefficients exactly to zero, selecting features; Elastic Net combines both.

**Q: How do you detect overfitting?**
Compare training and validation/test performance (large gap), use cross-validation, and inspect learning curves.
:::
