---
num: 14
title: "Classification Metrics: Confusion Matrix, Precision, Recall, ROC, PR and Business Value"
live: "ML class 7"
updated: "scikit-learn 1.7+"
level: Intermediate
duration: 110 min
summary: Measure classifiers properly. The confusion matrix, accuracy and why it misleads, precision, recall, specificity, F1 and F-beta, ROC curves and AUC, precision-recall curves, log loss and calibration, lift and gains charts, choosing thresholds by cost or capacity, and multiclass averaging, using the telecom churn model.
datasets: [telecom_churn.csv]
outcomes:
  - Build and read a confusion matrix and compute accuracy, precision, recall, specificity and F1
  - Plot and interpret ROC and precision-recall curves and their AUCs
  - Check probability calibration and log loss
  - Choose thresholds by cost, capacity (top-k) or target recall, and present gains/lift
  - Use macro, weighted and micro averages for multiclass problems
---

## The confusion matrix

```python run
import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, fbeta_score, classification_report
tc = pd.read_csv("telecom_churn.csv")
X = tc.drop(columns=["customer_id", "churn", "total_charges"]); y = (tc.churn == "Yes").astype(int)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=1)
pre = ColumnTransformer([("n", StandardScaler(), ["senior_citizen", "tenure_months", "monthly_charges", "support_calls"]), ("c", OneHotEncoder(), ["contract", "internet_service", "payment_method"])])
model = Pipeline([("pre", pre), ("lr", LogisticRegression(max_iter=1000))]).fit(Xtr, ytr)
proba = model.predict_proba(Xte)[:, 1]; pred = (proba >= 0.5).astype(int)
tn, fp, fn, tp = confusion_matrix(yte, pred).ravel()
print(pd.DataFrame([[tn, fp], [fn, tp]], index=["actual: stay", "actual: churn"], columns=["pred: stay", "pred: churn"]))
```

```python fig: The four outcomes of a binary classifier.
dg.cards([("True positive (TP)", "Actual churner, predicted churn: caught"), ("False negative (FN)", "Actual churner, predicted stay: missed (Type II)"), ("False positive (FP)", "Stayer predicted to churn: false alarm (Type I)"), ("True negative (TN)", "Stayer predicted to stay")], cols=2, title="Confusion matrix outcomes")
```

## Metrics from the matrix

| Metric | Formula | Question it answers |
|---|---|---|
| **Accuracy** | (TP + TN) / all | How often is the model right overall? |
| **Precision** | TP / (TP + FP) | Of those we flagged, how many were churners? |
| **Recall** (sensitivity, TPR) | TP / (TP + FN) | Of all churners, how many did we catch? |
| **Specificity** (TNR) | TN / (TN + FP) | Of all stayers, how many did we leave alone? |
| **F1** | 2·P·R / (P + R) | Balance of precision and recall |
| **F-beta** | weights recall β times as much | β = 2 when misses are costlier |

```python run
print(f"accuracy {accuracy_score(yte, pred):.3f} | precision {precision_score(yte, pred):.3f} | recall {recall_score(yte, pred):.3f} | specificity {tn / (tn + fp):.3f}")
print(f"F1 {f1_score(yte, pred):.3f} | F2 {fbeta_score(yte, pred, beta=2):.3f} | baseline accuracy (always 'stay') {1 - yte.mean():.3f}")
print(classification_report(yte, pred, target_names=["stay", "churn"], digits=3))
```

Accuracy barely beats the "nobody churns" baseline, while recall shows the model misses more than half of the churners at the default 0.5 threshold.

| Which metric matters? | Example |
|---|---|
| Recall | Cancer screening, fraud, churn (missing a positive is costly) |
| Precision | Spam filter (do not hide real mail), expensive interventions |
| Balance (F1) | Both errors matter similarly |
| Specificity | Avoiding false alarms for the majority |

## Threshold-free view: ROC and PR curves

```python fig: Left: the ROC curve plots recall (TPR) against the false-positive rate at every threshold. Right: the precision-recall curve focuses on the positive class, more informative when positives are rare.
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score
fpr, tpr, thr = roc_curve(yte, proba); prec, rec, pthr = precision_recall_curve(yte, proba)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.8))
a1.plot(fpr, tpr, color="#7C3AED", lw=2.5, label=f"logistic AUC = {roc_auc_score(yte, proba):.3f}"); a1.plot([0, 1], [0, 1], ls="--", color="#999", label="random = 0.5")
i = np.argmin(abs(thr - 0.5)); a1.plot(fpr[i], tpr[i], "o", color="#DB2777", ms=8, label="threshold 0.5")
a1.set_xlabel("false-positive rate (1 − specificity)"); a1.set_ylabel("true-positive rate (recall)"); a1.legend(frameon=False, fontsize=8)
a2.plot(rec, prec, color="#0E9F8E", lw=2.5, label=f"AP = {average_precision_score(yte, proba):.3f}"); a2.axhline(yte.mean(), ls="--", color="#999", label=f"random = {yte.mean():.2f}")
a2.set_xlabel("recall"); a2.set_ylabel("precision"); a2.legend(frameon=False, fontsize=8)
for a in (a1, a2): a.spines[["top", "right"]].set_visible(False)
```

```python run
print(f"ROC-AUC {roc_auc_score(yte, proba):.3f} | average precision (PR-AUC) {average_precision_score(yte, proba):.3f} | churn base rate {yte.mean():.3f}")
```

**ROC-AUC** is the probability that a randomly chosen churner gets a higher score than a randomly chosen stayer (0.5 = random, 1 = perfect). It does not depend on the threshold or on class balance. **Average precision** summarises the PR curve; its random baseline equals the positive rate, so it reveals weakness on rare classes that ROC-AUC can hide.

## Probability quality: log loss and calibration

If the model says 30%, do about 30% of those customers churn?

```python fig: Calibration curve: points near the diagonal mean predicted probabilities can be trusted as probabilities.
from sklearn.calibration import calibration_curve
fr, mp = calibration_curve(yte, proba, n_bins=8, strategy="quantile")
fig, ax = plt.subplots(figsize=(4.8, 3.8)); ax.plot(mp, fr, "o-", color="#7C3AED", lw=2); ax.plot([0, 1], [0, 1], ls="--", color="#999")
ax.set_xlabel("mean predicted probability"); ax.set_ylabel("observed churn rate"); ax.spines[["top", "right"]].set_visible(False)
```

```python run
from sklearn.metrics import log_loss, brier_score_loss
print(f"log loss {log_loss(yte, proba):.3f} (always predicting the base rate: {log_loss(yte, np.full(len(yte), ytr.mean())):.3f}) | Brier score {brier_score_loss(yte, proba):.3f}")
```

Calibration matters when probabilities feed decisions (expected loss = P(default) × amount). Tree ensembles and SVMs are often poorly calibrated; fix with `CalibratedClassifierCV` (isotonic or sigmoid).

## Choosing the threshold

### By cost

```python run
value_saved, offer_cost = 3000, 500           # a retained churner is worth ₹3,000; each offer costs ₹500
rows = []
for t in np.round(np.arange(0.1, 0.81, 0.05), 2):
    p = proba >= t; tp_ = (p & (yte == 1)).sum(); n_off = p.sum()
    rows.append({"threshold": t, "offers": n_off, "churners_reached": tp_, "precision": round(tp_ / max(n_off, 1), 3), "recall": round(tp_ / yte.sum(), 3), "profit_inr": int(tp_ * value_saved * 0.4 - n_off * offer_cost)})   # 40% of reached churners accept
res = pd.DataFrame(rows); print(res.to_string(index=False))
print("most profitable threshold:", res.loc[res.profit_inr.idxmax(), "threshold"])
```

### By capacity: top-k, gains and lift

The retention team can call only 10% of customers per month. Rank by probability and take the top 10%.

```python run
order = np.argsort(-proba); ys = yte.to_numpy()[order]
deciles = np.array_split(ys, 10)
gains = pd.DataFrame({"decile": range(1, 11), "churn_rate": [d.mean() for d in deciles]})
gains["cum_%_of_churners"] = (100 * np.cumsum([d.sum() for d in deciles]) / ys.sum()).round(1)
gains["lift"] = (gains.churn_rate / ys.mean()).round(2); gains["churn_rate"] = gains.churn_rate.round(3)
print(gains.to_string(index=False))
```

Calling the top 10% reaches 2.8 times as many churners as random calls (the lift in the first decile), and the top 30% of scores contain about two-thirds of all churners. Gains and lift tables are how marketing and collections teams read models.

### By target recall

```python run
target = 0.80
i = np.where(rec >= target)[0][-1]
print(f"to catch {target:.0%} of churners use threshold {pthr[min(i, len(pthr) - 1)]:.3f} → precision {prec[i]:.3f}")
```

## Multiclass metrics

```python run
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
w = load_wine(); Xa, Xb, ya, yb = train_test_split(w.data, w.target, test_size=0.4, stratify=w.target, random_state=0)
pw = RandomForestClassifier(200, random_state=0).fit(Xa, ya).predict(Xb)
print(confusion_matrix(yb, pw))
for avg in ("macro", "weighted", "micro"): print(f"{avg:8s} F1 {f1_score(yb, pw, average=avg):.3f}")
```

**Macro** averages classes equally (rare classes count as much as common ones); **weighted** weights by class size; **micro** pools all decisions (equals accuracy for single-label problems).

## Summary

:::key
- Confusion matrix: TP, FP, FN, TN. Accuracy misleads on imbalanced data; compare with the majority baseline.
- Precision = how many flagged are right; recall = how many positives are caught; F1/F-beta balance them.
- ROC-AUC ranks quality independent of threshold; PR-AUC (average precision) is better for rare positives.
- Check log loss and calibration when probabilities drive decisions.
- Choose thresholds by cost, capacity (top-k, gains, lift) or target recall; use macro/weighted averages for multiclass.
:::

:::quiz
Q: Fraud is 1% of transactions. A model that predicts "not fraud" for everything has accuracy…
- 1%
- 50%
* 99%, which is useless
- Undefined
> That is why accuracy misleads on imbalanced data.

Q: Recall answers which question?
* Of all actual positives, how many did we catch?
- Of all flagged cases, how many are right?
- How many negatives were correct?
- How confident is the model?
> TP / (TP + FN).

Q: A spam filter must not hide real emails. Which metric should be high?
* Precision for the spam class
- Recall for the spam class
- Specificity only for spam
- None
> False positives (real mail marked spam) are costly.

Q: ROC-AUC = 0.80 means…
* A random positive gets a higher score than a random negative 80% of the time
- 80% accuracy
- 80% recall
- 80% precision
> It measures ranking quality.

Q: Which curve is more informative when positives are very rare?
- ROC
* Precision-recall
- Calibration
- Learning curve
> PR focuses on the positive class.

Q: The retention team can call only 10% of customers. What should you report?
* Precision/recall and lift in the top 10% of scores
- Overall accuracy
- R²
- Number of features
> Evaluate where decisions are actually made.
:::

:::exercise Practice
(1) Train a random forest on the same split and compare ROC-AUC, average precision and lift in the top decile with logistic regression. (2) Calibrate the forest with `CalibratedClassifierCV` and compare Brier scores. (3) Find the threshold that maximises F2.
???
```python
from sklearn.calibration import CalibratedClassifierCV
rf = Pipeline([("pre", pre), ("rf", RandomForestClassifier(400, min_samples_leaf=10, random_state=0))]).fit(Xtr, ytr)
pr = rf.predict_proba(Xte)[:, 1]; print(roc_auc_score(yte, pr), average_precision_score(yte, pr))
top = np.argsort(-pr)[:len(pr) // 10]; print("lift", yte.to_numpy()[top].mean() / yte.mean())
cal = Pipeline([("pre", pre), ("cal", CalibratedClassifierCV(RandomForestClassifier(400, min_samples_leaf=10, random_state=0), cv=5, method="isotonic"))]).fit(Xtr, ytr)
print(brier_score_loss(yte, pr), brier_score_loss(yte, cal.predict_proba(Xte)[:, 1]))
ts = np.linspace(.05, .9, 35); print(max(ts, key=lambda t: fbeta_score(yte, proba >= t, beta=2)))
```
:::

:::interview Questions you may be asked
**Q: Precision vs recall: give an example where each matters more.**
Recall for disease screening or fraud (missing a case is costly); precision for spam filtering or expensive manual reviews (false alarms are costly).

**Q: Why can a model with 95% accuracy be bad?**
With 95% negatives, predicting all negatives gives 95% accuracy and catches no positives; look at recall, precision, PR-AUC and the confusion matrix.

**Q: How do you choose a classification threshold?**
From business costs and constraints: expected profit, team capacity (top-k), or a required recall/precision, validated on held-out data.
:::
