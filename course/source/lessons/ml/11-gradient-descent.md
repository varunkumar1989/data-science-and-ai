---
num: 11
title: "Gradient Descent: How Models Learn (Built from Scratch in NumPy)"
live: "ML class 5"
updated: "NumPy 2 · scikit-learn 1.7+"
level: Intermediate
duration: 110 min
summary: Understand the optimisation engine behind linear regression, logistic regression and neural networks. Cost functions, gradients and the update rule, implementing batch gradient descent for linear regression in NumPy, the learning rate, feature scaling, stochastic and mini-batch variants, convergence checks, and comparison with the closed-form OLS solution and scikit-learn's SGDRegressor.
datasets: [house_prices.csv]
outcomes:
  - Define a cost function (MSE) and explain what its gradient tells us
  - Implement batch gradient descent for linear regression with NumPy
  - Choose a learning rate and diagnose divergence and slow convergence with cost curves
  - Explain why feature scaling speeds up gradient descent
  - Compare batch, stochastic and mini-batch gradient descent and use SGDRegressor
---

## Learning = minimising a cost

A model has **parameters** (weights). Learning means finding the weights that make a **cost function** as small as possible. For linear regression the usual cost is the **mean squared error**:

$$J(\mathbf{w}, b) = \frac{1}{2n}\sum_{i=1}^{n}\left(\hat y_i - y_i\right)^2, \qquad \hat y_i = \mathbf{w}\cdot\mathbf{x}_i + b$$

(The ½ simply makes the derivative tidier.) OLS has a formula for the minimum, but most models (logistic regression, neural networks) do not, so we **search** for it.

## The idea: walk downhill

Imagine standing on a foggy hillside: feel the slope under your feet and step downhill; repeat until the ground is flat. The **gradient** is the slope; we step in the opposite direction.

$$w \leftarrow w - \alpha\,\frac{\partial J}{\partial w}, \qquad b \leftarrow b - \alpha\,\frac{\partial J}{\partial b}$$

α is the **learning rate** (step size). For linear regression the gradients are:

$$\frac{\partial J}{\partial \mathbf{w}} = \frac{1}{n}\,X^{T}(\hat{\mathbf{y}} - \mathbf{y}) \qquad \frac{\partial J}{\partial b} = \frac{1}{n}\sum_{i}(\hat y_i - y_i)$$

```python fig: Gradient descent on a one-parameter cost curve: each step moves against the slope; steps shrink as the slope flattens near the minimum.
import numpy as np, matplotlib.pyplot as plt
J = lambda w: (w - 3) ** 2 + 1; dJ = lambda w: 2 * (w - 3)
w, path = -2.0, []
for _ in range(9): path.append(w); w -= 0.25 * dJ(w)
ws = np.linspace(-3, 8, 200)
fig, ax = plt.subplots(figsize=(8, 3.3)); ax.plot(ws, J(ws), color="#1F1B2E")
ax.plot(path, [J(p) for p in path], "o-", color="#DB2777", ms=6); ax.annotate("start", (path[0], J(path[0])), textcoords="offset points", xytext=(8, 0))
ax.annotate("minimum", (3, 1), textcoords="offset points", xytext=(-10, -18), color="#7C3AED"); ax.set_xlabel("weight w"); ax.set_ylabel("cost J(w)"); ax.spines[["top", "right"]].set_visible(False)
```

## Implementation in NumPy

```python run
import pandas as pd
h = pd.read_csv("house_prices.csv").dropna(subset=["area_sqft"])
pps = h.price_lakh * 1e5 / h.area_sqft; h = h[pps.between(pps.median() / 3, pps.median() * 3)]
feats = ["area_sqft", "bedrooms", "bathrooms", "age_years", "distance_to_center_km"]
X_raw = h[feats].to_numpy(float); y = h.price_lakh.to_numpy(float)
mu, sd = X_raw.mean(axis=0), X_raw.std(axis=0); X = (X_raw - mu) / sd          # standardise features

def gradient_descent(X, y, lr=0.1, epochs=300):
    n, p = X.shape; w, b = np.zeros(p), 0.0; history = []
    for _ in range(epochs):
        y_hat = X @ w + b
        err = y_hat - y
        history.append((err ** 2).mean() / 2)                                   # cost J
        w -= lr * (X.T @ err) / n                                               # gradient step for weights
        b -= lr * err.mean()                                                    # gradient step for bias
    return w, b, history

w, b, hist = gradient_descent(X, y)
print("cost: start", round(hist[0], 1), "→ after 10", round(hist[9], 1), "→ end", round(hist[-1], 2))
print("weights (per 1 sd of each feature):", dict(zip(feats, w.round(2).tolist())), "| bias", round(b, 2))
```

### Check against the exact OLS solution

```python run
X1 = np.c_[np.ones(len(X)), X]
theta = np.linalg.lstsq(X1, y, rcond=None)[0]                                   # closed form (normal equation)
print("OLS bias", theta[0].round(2), "weights", theta[1:].round(2))
print("max difference from gradient descent:", np.abs(theta[1:] - w).max().round(4))
w_orig = w / sd; b_orig = b - (w_orig * mu).sum()                              # convert back to original units
print(f"per sq ft: {w_orig[0]:.4f} lakh (≈ ₹{w_orig[0] * 1e5:,.0f}) | per year of age: {w_orig[3]:.3f} lakh")
```

Gradient descent reached the same answer as the exact formula. The **normal equation** θ = (XᵀX)⁻¹Xᵀy is fine for a few thousand features, but gradient descent scales to millions of rows and parameters and to models without closed-form solutions.

## The learning rate

```python fig: Cost curves for different learning rates: too small is slow, a good rate converges quickly, too large diverges.
fig, ax = plt.subplots(figsize=(8.5, 3.4))
for lr, c in [(0.005, "#C4B5FD"), (0.05, "#7C3AED"), (0.5, "#0E9F8E"), (1.95, "#E2A400"), (2.05, "#DB2777")]:
    _, _, hh = gradient_descent(X, y, lr=lr, epochs=60)
    ax.plot(hh, color=c, lw=2, label=f"α = {lr}")
ax.set_yscale("log"); ax.set_ylim(10, 1e5); ax.set_xlabel("epoch"); ax.set_ylabel("cost (log scale)"); ax.legend(frameon=False, ncol=5, fontsize=8); ax.spines[["top", "right"]].set_visible(False)
```

| Symptom | Cause | Fix |
|---|---|---|
| Cost falls very slowly | α too small | Increase α (×3 steps: 0.001, 0.003, 0.01…) |
| Cost goes up or oscillates, becomes NaN | α too large | Decrease α |
| Cost flattens high | Stuck / underfitting / unscaled features | Scale features, more epochs, better model |

Plot the cost every time: it should go down and flatten.

## Why scale features?

```python run
best = ((X1 @ theta - y) ** 2).mean() / 2                                     # the lowest possible cost (OLS)
with np.errstate(all="ignore"):
    for name, Xs, lr in [("raw features", X_raw, 1e-7), ("raw features", X_raw, 1e-6), ("standardised", X, 0.1)]:
        _, _, hh = gradient_descent(Xs, y, lr=lr, epochs=300)
        gap = "diverged" if not np.isfinite(hh[-1]) or hh[-1] > 1e6 else f"{100 * (hh[-1] / best - 1):.1f}% above the optimum"
        print(f"{name:13s} lr={lr:<6} cost after 300 epochs: {gap}")
```

With raw features, area (hundreds to thousands) and bedrooms (1–5) differ hugely in scale, so the cost surface is a long narrow valley: a learning rate small enough for area is far too small for bedrooms. Standardising makes the valley round, so one learning rate suits all weights.

## Batch, stochastic and mini-batch

| Variant | Gradient from | Pros | Cons |
|---|---|---|---|
| Batch GD | All n rows each step | Smooth, exact | Slow for big data |
| Stochastic GD (SGD) | One random row | Fast updates, escapes shallow minima | Noisy |
| Mini-batch GD | 32–1,024 rows | Best of both; GPU friendly | Batch size to tune |

```python run
def minibatch_gd(X, y, lr=0.05, epochs=20, batch=32, seed=0):
    rng = np.random.default_rng(seed); n, p = X.shape; w, b = np.zeros(p), 0.0; costs = []
    for _ in range(epochs):
        idx = rng.permutation(n)
        for start in range(0, n, batch):
            j = idx[start:start + batch]; err = X[j] @ w + b - y[j]
            w -= lr * X[j].T @ err / len(j); b -= lr * err.mean()
        costs.append(((X @ w + b - y) ** 2).mean() / 2)
    return w, b, costs
wm, bm, cm = minibatch_gd(X, y)
print("mini-batch cost per epoch:", [round(float(c), 1) for c in cm[:5]], "...", round(float(cm[-1]), 2), "| weights close to OLS:", np.allclose(wm, theta[1:], atol=0.5))
```

Deep learning uses mini-batch gradient descent with improved optimisers: **momentum** (keeps velocity), **RMSProp** and **Adam** (adaptive learning rates per parameter), plus learning-rate schedules.

## scikit-learn: SGDRegressor

```python run
from sklearn.linear_model import SGDRegressor, LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
Xtr, Xte, ytr, yte = train_test_split(h[feats], y, test_size=0.2, random_state=0)
sgd = make_pipeline(StandardScaler(), SGDRegressor(learning_rate="invscaling", eta0=0.01, max_iter=2000, tol=1e-6, random_state=0)).fit(Xtr, ytr)
ols = make_pipeline(StandardScaler(), LinearRegression()).fit(Xtr, ytr)
print(f"test R²: SGDRegressor {sgd.score(Xte, yte):.4f} | LinearRegression {ols.score(Xte, yte):.4f} | SGD epochs used {sgd[-1].n_iter_}")
```

`SGDRegressor`/`SGDClassifier` also support `partial_fit` for data that arrives in streams or does not fit in memory, and penalties (L2, L1, elastic net) for regularisation.

## Where gradient descent appears

Logistic regression (minimising log loss, lesson 13), neural networks and LLMs (backpropagation computes gradients for billions of weights, lesson 26), gradient boosting (fits each new tree to the gradient of the loss, lesson 19), and matrix factorisation in recommenders.

## Summary

:::key
- Learning = minimising a cost function; gradient descent repeatedly steps against the gradient: w ← w − α·∂J/∂w.
- For linear regression: gradient = Xᵀ(ŷ − y)/n; it converges to the same solution as OLS.
- The learning rate controls step size: too small is slow, too large diverges; always plot the cost.
- Scale features so one learning rate suits all weights.
- Batch, stochastic and mini-batch variants trade accuracy of each step for speed; Adam and momentum power deep learning.
:::

:::quiz
Q: In the update w ← w − α·∂J/∂w, what is α?
* The learning rate (step size)
- The gradient
- The cost
- The bias
> It is a hyperparameter you choose.

Q: The cost increases every epoch and becomes NaN. Most likely cause?
- Learning rate too small
* Learning rate too large
- Too much data
- Features are scaled
> Steps overshoot the minimum.

Q: Why standardise features before gradient descent?
* Features on very different scales create a narrow valley that slows convergence
- To change the final OLS solution
- To remove outliers
- It is required by NumPy
> Scaling makes one learning rate work for all weights.

Q: What does mini-batch gradient descent use for each update?
- All rows
- One row
* A small random subset of rows
- Only the test set
> Common sizes: 32–512.

Q: Gradient descent and the normal equation on the same linear regression should give…
* Approximately the same weights
- Completely different weights
- The same only without scaling
- No relation
> Both minimise the same convex cost.

Q: Which algorithm fits each new tree to the gradient of the loss?
- K-means
* Gradient boosting
- KNN
- PCA
> Hence the name.
:::

:::exercise Practice
(1) Add an early-stopping rule: stop when the cost improves by less than 0.001. How many epochs are needed at α = 0.1? (2) Implement gradient descent for a model with only `area_sqft` and plot the fitted line. (3) Try mini-batch sizes 8, 64 and 512 and compare the final cost after 10 epochs.
???
```python
def gd_early(X, y, lr=0.1, tol=1e-3, max_epochs=10_000):
    n, p = X.shape; w, b = np.zeros(p), 0.0; prev = np.inf
    for e in range(max_epochs):
        err = X @ w + b - y; cost = (err ** 2).mean() / 2
        if prev - cost < tol: return w, b, e
        prev = cost; w -= lr * X.T @ err / n; b -= lr * err.mean()
    return w, b, max_epochs
print(gd_early(X, y)[2])
w1, b1, _ = gradient_descent(X[:, [0]], y)
for bs in (8, 64, 512): print(bs, minibatch_gd(X, y, batch=bs, epochs=10)[2][-1])
```
:::

:::interview Questions you may be asked
**Q: Explain gradient descent intuitively.**
Start with random weights, compute how wrong the model is, find the direction that reduces the error fastest (the negative gradient), take a small step, and repeat until the error stops falling.

**Q: Batch vs stochastic gradient descent?**
Batch uses all data per step (stable, slow); stochastic uses one example (fast, noisy); mini-batch is the practical compromise.

**Q: Can gradient descent get stuck?**
For convex costs like linear and logistic regression there is one global minimum. For neural networks it can land in local minima or saddle points; momentum, Adam and random restarts help.
:::
