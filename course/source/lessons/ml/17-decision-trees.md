---
num: 17
title: "Decision Trees: Splits, Impurity, Pruning and Interpretable Rules"
live: "ML track (added)"
updated: "scikit-learn 1.7+"
level: Intermediate
duration: 110 min
summary: Learn the model behind random forests and gradient boosting. How trees split data with Gini impurity, entropy and variance reduction, growing and visualising a tree, reading it as business rules, controlling overfitting with depth, minimum leaf size and cost-complexity pruning, regression trees, feature importance and the strengths and weaknesses of single trees.
datasets: [hr_employees.csv, house_prices.csv]
outcomes:
  - Explain recursive binary splitting and compute Gini impurity and entropy by hand
  - Train, plot and read a decision tree classifier as IF-THEN rules
  - Control overfitting with max_depth, min_samples_leaf and ccp_alpha pruning
  - Build a regression tree and explain its step-shaped predictions
  - Describe tree feature importance and the instability of single trees
---

## How a tree decides

A **decision tree** asks a sequence of yes/no questions about the features. Each question splits the data into two purer groups; leaves give the prediction (majority class or average value). It is a flowchart learned from data.

```python fig: A decision tree is a learned flowchart of questions.
dg.tree("Overtime = Yes?", {"Yes": ["Job satisfaction ≤ 2?", "→ yes: high risk", "→ no: medium risk"], "No": ["Job satisfaction ≤ 2?", "→ yes: medium risk", "→ no: low risk"]}, title="Attrition tree (simplified)")
```

## Measuring purity

At each node the algorithm tries every feature and threshold and picks the split that most reduces **impurity**.

$$\text{Gini} = 1 - \sum_k p_k^2 \qquad \text{Entropy} = -\sum_k p_k \log_2 p_k$$

```python run
import numpy as np, pandas as pd
def gini(p): p = np.asarray(p); return 1 - (p ** 2).sum()
def entropy(p): p = np.asarray([x for x in p if x > 0]); return float(-(p * np.log2(p)).sum()) + 0.0
for dist in ([0.5, 0.5], [0.8, 0.2], [1.0, 0.0]): print(dist, "Gini", round(gini(dist), 3), "| entropy", round(entropy(dist), 3))
hr = pd.read_csv("hr_employees.csv"); hr["left"] = (hr.attrition == "Yes").astype(int)
def split_gain(df, mask):
    parent = gini([1 - df.left.mean(), df.left.mean()])
    l, r = df[mask], df[~mask]
    child = sum(len(s) / len(df) * gini([1 - s.left.mean(), s.left.mean()]) for s in (l, r))
    return parent - child
for name, mask in [("overtime == Yes", hr.overtime == "Yes"), ("job_satisfaction <= 2", hr.job_satisfaction <= 2), ("years_at_company <= 1", hr.years_at_company <= 1), ("department == Sales", hr.department == "Sales")]:
    print(f"{name:24s} Gini decrease {split_gain(hr, mask):.4f}")
```

The split with the largest decrease (information gain) wins; then the process repeats inside each child (**recursive binary splitting**) until a stopping rule is met. Regression trees use variance (MSE) reduction instead.

## Training and reading a tree

```python run
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score
X = pd.get_dummies(hr[["age", "years_at_company", "monthly_income", "job_satisfaction", "distance_from_home_km", "performance_rating", "overtime", "department"]], drop_first=True).astype(float)
y = hr.left
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)
small = DecisionTreeClassifier(max_depth=3, min_samples_leaf=40, random_state=0).fit(Xtr, ytr)
print(export_text(small, feature_names=list(X.columns), show_weights=True, decimals=1))
print(f"test AUC {roc_auc_score(yte, small.predict_proba(Xte)[:, 1]):.3f} | accuracy {accuracy_score(yte, small.predict(Xte)):.3f}")
```

```python fig: The depth-3 tree. Each box shows the split, Gini impurity, sample count and class mix; darker colours are purer.
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(13, 5))
plot_tree(small, feature_names=list(X.columns), class_names=["stay", "leave"], filled=True, rounded=True, fontsize=7, impurity=True, proportion=False, ax=ax)
```

Each path from root to leaf is an **IF-THEN rule** that managers can read and challenge, which is a big advantage of small trees.

## Overfitting and how to stop it

```python run
for depth in (1, 2, 3, 5, 8, 12, None):
    m = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(Xtr, ytr)
    print(f"max_depth={str(depth):4s} leaves {m.get_n_leaves():4d} | train AUC {roc_auc_score(ytr, m.predict_proba(Xtr)[:, 1]):.3f} | test AUC {roc_auc_score(yte, m.predict_proba(Xte)[:, 1]):.3f}")
```

An unrestricted tree keeps splitting until leaves are pure: perfect on training data, poor on new data. Notice also that attrition is hard to predict from these few HR fields (the best test AUC is only about 0.6). That is common with people data: many reasons for leaving (a new offer, a manager, family) are not in the database. A good analyst says so rather than overselling the model.

| Hyperparameter | Effect |
|---|---|
| `max_depth` | Maximum number of questions on a path |
| `min_samples_split` | A node needs this many rows to split |
| `min_samples_leaf` | Every leaf keeps at least this many rows (smooths probabilities) |
| `max_leaf_nodes` | Cap on the number of leaves |
| `ccp_alpha` | Cost-complexity pruning: removes branches that add little |
| `class_weight="balanced"` | Gives the minority class more weight |

### Cost-complexity pruning

```python run
from sklearn.model_selection import cross_val_score, StratifiedKFold
path = DecisionTreeClassifier(random_state=0).cost_complexity_pruning_path(Xtr, ytr)
alphas = path.ccp_alphas[::max(1, len(path.ccp_alphas) // 25)]
cv = StratifiedKFold(5, shuffle=True, random_state=0)
scores = [cross_val_score(DecisionTreeClassifier(ccp_alpha=a, random_state=0), Xtr, ytr, cv=cv, scoring="roc_auc").mean() for a in alphas]
best_a = alphas[int(np.argmax(scores))]
pruned = DecisionTreeClassifier(ccp_alpha=best_a, random_state=0).fit(Xtr, ytr)
print(f"best ccp_alpha {best_a:.5f} | leaves {pruned.get_n_leaves()} | CV AUC {max(scores):.3f} | test AUC {roc_auc_score(yte, pruned.predict_proba(Xte)[:, 1]):.3f}")
```

## Feature importance

```python run
imp = pd.Series(pruned.feature_importances_, index=X.columns).sort_values(ascending=False)
print(imp[imp > 0].round(3).to_dict())
```

Importance = total impurity decrease contributed by each feature (normalised to sum to 1). It is quick but biased towards continuous features with many possible split points; check with permutation importance (lesson 27).

## Regression trees

```python fig: A regression tree predicts the average price in each leaf, giving step-shaped predictions (depth 2 vs depth 5).
from sklearn.tree import DecisionTreeRegressor
h = pd.read_csv("house_prices.csv").dropna(subset=["area_sqft"]); h = h[h.price_lakh.between(5, 300)]
xs = np.linspace(h.area_sqft.min(), h.area_sqft.max(), 400)[:, None]
fig, ax = plt.subplots(figsize=(8.5, 3.4)); ax.scatter(h.area_sqft, h.price_lakh, s=4, color="#DDD6FE")
for d, c in [(2, "#7C3AED"), (5, "#DB2777")]:
    t = DecisionTreeRegressor(max_depth=d).fit(h[["area_sqft"]], h.price_lakh); ax.plot(xs, t.predict(pd.DataFrame(xs, columns=["area_sqft"])), color=c, lw=2, label=f"depth {d}")
ax.set_xlabel("area (sq ft)"); ax.set_ylabel("price (₹ lakh)"); ax.legend(frameon=False); ax.spines[["top", "right"]].set_visible(False)
```

```python run
from sklearn.metrics import mean_absolute_error
hf = ["area_sqft", "bedrooms", "bathrooms", "age_years", "distance_to_center_km", "parking"]
Htr, Hte, htr, hte = train_test_split(pd.get_dummies(h[hf + ["city"]]).astype(float), h.price_lakh, test_size=0.2, random_state=0)
for d in (3, 6, 10, None):
    t = DecisionTreeRegressor(max_depth=d, min_samples_leaf=5, random_state=0).fit(Htr, htr)
    print(f"depth {str(d):4s} test MAE {mean_absolute_error(hte, t.predict(Hte)):.2f} lakh")
```

Trees cannot extrapolate: a house bigger than any in the training data gets the price of the largest leaf.

## Strengths and weaknesses

| Strengths | Weaknesses |
|---|---|
| Easy to explain as rules; visual | Unstable: small data changes give a different tree |
| No scaling needed; handles mixed types | Overfits without limits |
| Captures non-linearity and interactions automatically | Step-shaped, no extrapolation |
| Fast to train and predict | Single trees are usually less accurate than ensembles |

```python run
for seed in range(3):
    Xs, _, ys, _ = train_test_split(Xtr, ytr, train_size=0.8, random_state=seed)
    t = DecisionTreeClassifier(max_depth=2, random_state=0).fit(Xs, ys)
    print(f"sample {seed}: root split on '{X.columns[t.tree_.feature[0]]}' at {t.tree_.threshold[0]:.1f}, second-level splits on {[X.columns[f] for f in t.tree_.feature[1:] if f >= 0]}")
```

Instability is exactly what **random forests** exploit: average many different trees and the noise cancels out (next lesson).

## Summary

:::key
- Trees split recursively on the feature/threshold that most reduces impurity (Gini, entropy) or variance (regression).
- Small trees are readable IF-THEN rules; unrestricted trees overfit badly.
- Control complexity with max_depth, min_samples_leaf and ccp_alpha pruning, chosen by cross-validation.
- Impurity-based importance is quick but biased; trees need no scaling but cannot extrapolate.
- Single trees are unstable; ensembles (random forests, boosting) fix this.
:::

:::quiz
Q: What is the Gini impurity of a node with 50% stay and 50% leave?
- 0
* 0.5
- 1
- 0.25
> 1 − (0.5² + 0.5²) = 0.5, the maximum for two classes.

Q: An unrestricted tree has train AUC 1.0 and test AUC 0.6. Why?
* It overfits: leaves memorise individual training rows
- It underfits
- The data are scaled wrongly
- Gini is the wrong criterion
> Limit depth or prune.

Q: Do decision trees need feature scaling?
- Yes, always
* No: splits depend on thresholds, not distances
- Only for regression
- Only with entropy
> Monotonic transformations do not change splits.

Q: What does `min_samples_leaf=40` do?
* Prevents leaves with fewer than 40 training rows
- Limits the tree to 40 leaves
- Uses 40 features
- Builds 40 trees
> It smooths predictions and reduces overfitting.

Q: Why can't a regression tree predict prices above the training maximum?
* Predictions are averages of training targets in each leaf
- It has a bug
- Prices must be scaled
- Trees only classify
> No extrapolation.

Q: Which weakness of single trees do random forests address?
* High variance / instability
- Lack of scaling
- Inability to handle categories
- Slowness
> Averaging many trees reduces variance.
:::

:::exercise Practice
(1) Train a tree on the telecom churn data with depth 3 and write its rules as three bullet points for the retention team. (2) Tune `max_depth` and `min_samples_leaf` with GridSearchCV. (3) Compare the test AUC of the pruned tree with logistic regression.
???
```python
tc = pd.read_csv("telecom_churn.csv"); Xc = pd.get_dummies(tc.drop(columns=["customer_id", "churn", "total_charges"]), drop_first=True).astype(float); yc = (tc.churn == "Yes").astype(int)
t3 = DecisionTreeClassifier(max_depth=3, min_samples_leaf=50).fit(Xc, yc); print(export_text(t3, feature_names=list(Xc.columns)))
from sklearn.model_selection import GridSearchCV
g = GridSearchCV(DecisionTreeClassifier(random_state=0), {"max_depth": [2, 3, 4, 5, 6, 8], "min_samples_leaf": [5, 20, 50, 100]}, cv=5, scoring="roc_auc").fit(Xc, yc); print(g.best_params_, g.best_score_)
```
:::

:::interview Questions you may be asked
**Q: How does a decision tree choose a split?**
It evaluates candidate thresholds on every feature and picks the one with the largest impurity reduction (Gini or entropy for classification, variance for regression), then repeats recursively.

**Q: Gini vs entropy?**
Both measure impurity and usually give similar trees; Gini is slightly faster, entropy comes from information theory.

**Q: How do you prevent a tree from overfitting?**
Limit depth, require minimum samples per leaf/split, cap leaves, prune with cost-complexity, or use ensembles.
:::
