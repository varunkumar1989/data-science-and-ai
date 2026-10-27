---
num: 13
title: "Logistic Regression: Probabilities, Odds Ratios and Credit-Risk Scoring"
live: "Python class 16 · ML class 4"
updated: "statsmodels 0.1x · scikit-learn 1.7+"
level: Intermediate
duration: 120 min
summary: Classify with probabilities. The sigmoid and log-odds, maximum likelihood and log loss, fitting logistic regression with statsmodels (inference, odds ratios) and scikit-learn (pipelines, regularisation), thresholds and decisions, multiclass logistic regression, and scoring new applicants in the Bank Loans case study.
datasets: [bank_loans.csv]
outcomes:
  - Explain why linear regression fails for binary targets and how the sigmoid fixes it
  - Interpret coefficients as log-odds and odds ratios
  - Fit, evaluate and regularise logistic regression in statsmodels and scikit-learn
  - Choose a probability threshold from business costs
  - Score new applicants and explain a prediction
---

## The case: who will default?

A bank has 700 past borrowers with a known outcome (`default` = 1 if they failed to repay) and 150 new applicants with unknown outcomes. Features: age, education level (`ed` 1–5), years with current employer (`employ`), years at current address (`address`), income (thousands), debt-to-income ratio % (`debtinc`), credit-card debt and other debt (thousands).

```python run
import pandas as pd, numpy as np
b = pd.read_csv("bank_loans.csv")
known, new = b[b.default.notna()].copy(), b[b.default.isna()].copy()
known["default"] = known.default.astype(int)
print(len(known), "labelled |", len(new), "new applicants | default rate", round(known.default.mean(), 3))
print(known.groupby("default")[["age", "employ", "address", "income", "debtinc", "creddebt", "othdebt"]].mean().round(2))
```

Defaulters are younger, have shorter employment and address histories, and much higher debt-to-income ratios.

## Why not linear regression?

A straight line predicts values below 0 and above 1, which are not probabilities. **Logistic regression** passes a linear score through the **sigmoid**:

$$p = P(y = 1 \mid x) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x_1 + \dots + \beta_k x_k)}}$$

Equivalently, the **log-odds** (logit) is linear in the features:

$$\log\frac{p}{1-p} = \beta_0 + \beta_1 x_1 + \dots + \beta_k x_k$$

```python fig: Linear regression vs logistic regression on default vs debt-to-income: the sigmoid keeps predictions between 0 and 1.
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression
xx = np.linspace(0, 45, 200)[:, None]
lin = LinearRegression().fit(known[["debtinc"]], known.default); lg = LogisticRegression().fit(known[["debtinc"]], known.default)
fig, ax = plt.subplots(figsize=(8.5, 3.3))
ax.scatter(known.debtinc, known.default + np.random.default_rng(0).uniform(-.03, .03, len(known)), s=6, color="#C4B5FD")
ax.plot(xx, lin.predict(pd.DataFrame(xx, columns=["debtinc"])), color="#E2A400", lw=2, label="linear regression")
ax.plot(xx, lg.predict_proba(pd.DataFrame(xx, columns=["debtinc"]))[:, 1], color="#7C3AED", lw=2.5, label="logistic regression")
ax.axhline(0, color="#999", lw=.6); ax.axhline(1, color="#999", lw=.6); ax.set_xlabel("debt-to-income %"); ax.set_ylabel("P(default)"); ax.legend(frameon=False); ax.spines[["top", "right"]].set_visible(False)
```

## Fitting and interpreting with statsmodels

Logistic regression is fitted by **maximum likelihood**: choose coefficients that make the observed outcomes most probable, equivalently minimising **log loss** (cross-entropy).

```python run
import statsmodels.formula.api as smf
m = smf.logit("default ~ age + ed + employ + address + income + debtinc + creddebt + othdebt", data=known).fit(disp=0)
print(m.summary2().tables[1][["Coef.", "Std.Err.", "P>|z|"]].round(4))
print(f"pseudo R² (McFadden) {m.prsquared:.3f} | log-likelihood {m.llf:.1f}")
```

```python run
odds = pd.DataFrame({"odds_ratio": np.exp(m.params), "ci_low": np.exp(m.conf_int()[0]), "ci_high": np.exp(m.conf_int()[1]), "p": m.pvalues}).drop("Intercept").round(3)
print(odds.sort_values("odds_ratio"))
```

| Coefficient | Odds ratio e^β | Reading |
|---|---|---|
| β = 0 | 1 | No association |
| β > 0 | > 1 | Higher odds of default per unit |
| β < 0 | < 1 | Lower odds of default per unit |

For example, the odds ratio of about 0.85 for `employ` means each extra year with the current employer multiplies the odds of default by 0.85 (about 15% lower odds), holding the other variables constant. The odds ratio of about 1.38 for `creddebt` means each extra unit of card debt (₹1,000s) multiplies the odds by 1.38, and each extra point of debt-to-income raises the odds by about 11%. Age, education, income and other debt are not significant once the others are included.

:::note Odds are not probabilities
Odds = p / (1 − p). A probability of 0.2 is odds of 0.25 ("1 to 4"). An odds ratio describes a *multiplicative* change in odds; the change in probability depends on where you start.
:::

A reduced model keeps the significant predictors (a common credit-scoring practice: fewer, stable variables):

```python run
m2 = smf.logit("default ~ employ + address + debtinc + creddebt", data=known).fit(disp=0)
print(m2.params.round(3).to_dict(), "| AIC full", round(m.aic, 1), "vs reduced", round(m2.aic, 1))
```

Lower AIC is better (it balances fit and complexity), so the four-variable model is preferred.

## scikit-learn pipeline with regularisation

```python run
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, accuracy_score, log_loss, classification_report
feats = ["age", "ed", "employ", "address", "income", "debtinc", "creddebt", "othdebt"]
X, y = known[feats], known.default
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=7)
for C in (0.01, 0.1, 1, 100):
    pipe = make_pipeline(StandardScaler(), LogisticRegression(C=C, max_iter=1000))
    cv = cross_val_score(pipe, Xtr, ytr, cv=5, scoring="roc_auc").mean()
    print(f"C = {C:<5} 5-fold ROC-AUC {cv:.3f}")
clf = make_pipeline(StandardScaler(), LogisticRegression(C=1, max_iter=1000)).fit(Xtr, ytr)
proba = clf.predict_proba(Xte)[:, 1]
print(f"\ntest: ROC-AUC {roc_auc_score(yte, proba):.3f} | accuracy {accuracy_score(yte, clf.predict(Xte)):.3f} | log loss {log_loss(yte, proba):.3f}")
print(classification_report(yte, clf.predict(Xte), target_names=["repaid", "default"], digits=3))
```

`C` is the inverse regularisation strength (lesson 12). Standardised coefficients from the pipeline are comparable across features:

```python run
print(pd.Series(clf[-1].coef_[0], index=feats).round(3).sort_values().to_dict())
```

## Choosing the threshold

`predict` uses a 0.5 threshold, but the right cut-off depends on costs. Suppose a missed defaulter costs the bank ₹50,000 and rejecting a good customer loses ₹10,000 of profit.

```python run
from sklearn.metrics import confusion_matrix
cost_fn, cost_fp = 50_000, 10_000
rows = []
for t in np.arange(0.1, 0.91, 0.1):
    tn, fp, fn, tp = confusion_matrix(yte, (proba >= t).astype(int)).ravel()
    rows.append({"threshold": round(t, 1), "approved": tn + fn, "defaults_caught": tp, "defaults_missed": fn, "good_rejected": fp, "cost_₹_lakh": (fn * cost_fn + fp * cost_fp) / 1e5})
th = pd.DataFrame(rows); print(th.to_string(index=False))
print("lowest-cost threshold:", th.loc[th["cost_₹_lakh"].idxmin(), "threshold"])
```

When missing a defaulter is five times as costly as rejecting a good customer, the best threshold is well below 0.5. Lesson 14 formalises this with precision, recall and ROC curves.

## Scoring new applicants

```python run
final = make_pipeline(StandardScaler(), LogisticRegression(C=1, max_iter=1000)).fit(X, y)          # refit on all labelled data
new["p_default"] = final.predict_proba(new[feats])[:, 1].round(3)
best_t = th.loc[th["cost_₹_lakh"].idxmin(), "threshold"]
new["decision"] = np.where(new.p_default >= best_t, "decline / review", "approve")
print(new.decision.value_counts().to_dict())
print(new.sort_values("p_default", ascending=False)[["customer_id", "age", "employ", "debtinc", "creddebt", "p_default", "decision"]].head(5).to_string(index=False))
```

### Explaining one decision

```python run
one = new.sort_values("p_default", ascending=False).iloc[0]
z = (one[feats].astype(float) - final[0].mean_) / final[0].scale_
contrib = pd.Series(z.values * final[-1].coef_[0], index=feats).sort_values(ascending=False)
print(f"{one.customer_id}: P(default) {one.p_default:.2f}; log-odds contributions:", contrib.round(2).to_dict())
```

Each contribution is a coefficient × the applicant's standardised value: positive values push towards default. This additive explanation is a big reason banks like logistic regression (and regulators require explanations of adverse decisions).

## Multiclass logistic regression

With more than two classes, scikit-learn fits a **multinomial** (softmax) model automatically: one score per class, converted to probabilities that sum to 1.

```python run
from sklearn.datasets import load_iris
iris = load_iris(as_frame=True)
mc = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(iris.data, iris.target)
print(mc.predict_proba(iris.data.iloc[[0, 60, 120]]).round(3), "| classes:", iris.target_names.tolist())
```

## Summary

:::key
- Logistic regression models log-odds as linear in the features and maps them to probabilities with the sigmoid; it is fitted by maximum likelihood (log loss).
- e^β is an odds ratio: > 1 raises, < 1 lowers the odds per unit, holding other features constant.
- statsmodels gives inference (p-values, CIs, AIC); scikit-learn gives pipelines, regularisation (C) and deployment.
- Choose the probability threshold from business costs, not by default 0.5.
- Coefficient × standardised value gives a transparent explanation of each prediction.
:::

:::quiz
Q: What does the sigmoid function do?
* Maps any real number to a probability between 0 and 1
- Squares the errors
- Selects features
- Scales the data
> 1 / (1 + e^(−z)).

Q: An odds ratio of 1.38 for card debt means…
* Each extra unit of card debt multiplies the odds of default by 1.38
- Default probability rises by 1.38 points
- Card debt causes default
- 80% of customers default
> Multiplicative change in odds.

Q: Which loss does logistic regression minimise?
- Mean squared error
* Log loss (cross-entropy)
- Hinge loss
- MAE
> Equivalent to maximising the likelihood.

Q: Missing a defaulter costs 5× more than rejecting a good customer. The best threshold is probably…
* Below 0.5
- Exactly 0.5
- Above 0.5
- Irrelevant
> Flag more applicants to avoid expensive misses.

Q: In scikit-learn, LogisticRegression(C=0.01) means…
* Strong regularisation
- No regularisation
- 1% threshold
- 1% of the data
> C is the inverse of the penalty strength.

Q: Why do banks favour logistic regression for credit scoring?
* It is accurate, stable and each decision can be explained by additive contributions
- It is the newest algorithm
- It never makes mistakes
- It needs no data
> Explainability is a regulatory requirement.
:::

:::exercise Practice
(1) Fit a logistic regression for HR attrition with `overtime`, `job_satisfaction`, `years_at_company` and `monthly_income`. Report odds ratios. (2) What is the predicted probability for an employee with overtime, satisfaction 1, 1 year at the company and ₹50,000 income? (3) Find the threshold that maximises F1 on a validation split.
???
```python
hr = pd.read_csv("hr_employees.csv"); hr["left"] = (hr.attrition == "Yes").astype(int)
ma = smf.logit("left ~ C(overtime) + job_satisfaction + years_at_company + I(monthly_income / 10000)", data=hr).fit(disp=0)
print(np.exp(ma.params).round(3))
print(ma.predict(pd.DataFrame({"overtime": ["Yes"], "job_satisfaction": [1], "years_at_company": [1], "monthly_income": [50000]})))
from sklearn.metrics import f1_score
ts = np.linspace(.05, .95, 19); print(max(ts, key=lambda t: f1_score(yte, proba >= t)))
```
:::

:::interview Questions you may be asked
**Q: Why is it called regression if it classifies?**
It regresses the log-odds on the features; classification happens when you apply a threshold to the predicted probability.

**Q: How do you interpret a logistic regression coefficient?**
A one-unit increase in the feature changes the log-odds by β, i.e. multiplies the odds by e^β, holding other features constant.

**Q: What are the assumptions of logistic regression?**
Independent observations, a linear relationship between features and log-odds, little multicollinearity, no extreme outliers, and enough events per variable.
:::
