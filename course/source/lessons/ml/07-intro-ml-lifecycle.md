---
num: 7
title: "Introduction to Machine Learning: Types, Business Framing and the ML Lifecycle"
live: "ML classes 3–4"
updated: "scikit-learn 1.7+ · 2026 practice"
level: Beginner
duration: 100 min
summary: What machine learning is and is not, how it differs from rules and statistics, supervised vs unsupervised vs reinforcement learning, regression vs classification vs clustering, turning a business problem into an ML problem, the end-to-end ML lifecycle (CRISP-DM to MLOps), linear vs non-linear models and link functions, and where GenAI fits.
datasets: [house_prices.csv, telecom_churn.csv]
outcomes:
  - Define machine learning and distinguish it from rule-based systems and classical statistics
  - Classify problems as supervised (regression, classification), unsupervised (clustering, dimensionality reduction) or reinforcement learning
  - Translate a business question into target, features, unit of prediction, metric and decision
  - Describe each stage of the ML lifecycle and common failure points
  - Explain linear vs non-linear models, link functions, and when not to use ML
---

## What is machine learning?

> "A computer program is said to learn from experience E with respect to some task T and performance measure P if its performance at T, as measured by P, improves with experience E." (Tom Mitchell)

Instead of writing rules by hand, we give the computer **examples** (data) and let an algorithm **learn the rules** (a model) that map inputs to outputs.

```python fig: Traditional programming vs machine learning.
dg.compare("Traditional programming", ["Input: data + rules (written by people)", "Output: answers", "if income < 25,000 and debt > 40%: reject", "Breaks when patterns change or are complex"], "Machine learning", ["Input: data + known answers (labels)", "Output: rules (a model)", "model.fit(X_train, y_train)", "Adapts by retraining; finds complex patterns"], title="Rules vs learning")
```

| | Statistics | Machine learning |
|---|---|---|
| Main goal | Inference: understand relationships, test hypotheses | Prediction: accurate outputs on new data |
| Typical question | "Does overtime increase attrition, and by how much?" | "Which employees are likely to leave next quarter?" |
| Model choice | Interpretable, with assumptions | Whatever predicts best (with interpretability as needed) |
| Validation | p-values, confidence intervals | Held-out test data, cross-validation |

They overlap heavily: linear and logistic regression belong to both.

## Types of machine learning

```python fig: The main families of machine learning.
dg.tree("Machine learning", {"Supervised (labelled)": ["Regression: price, demand", "Classification: churn, fraud, spam"], "Unsupervised (no labels)": ["Clustering: segments", "Dimensionality reduction: PCA", "Anomaly detection"], "Reinforcement": ["Agent + rewards: games, robotics, ads bidding"], "Self-supervised / GenAI": ["LLMs, embeddings (GenAI track)"]}, title="ML landscape")
```

| Problem | Target type | Example | Algorithms (this track) |
|---|---|---|---|
| **Regression** | Number | House price, delivery time, demand | Linear, Ridge/Lasso, trees, boosting |
| **Classification** | Category | Churn yes/no, loan default, spam | Logistic, KNN, trees, RF, boosting, SVM, NB |
| **Clustering** | None | Customer segments | K-means, hierarchical, DBSCAN |
| **Dimensionality reduction** | None | Compress 50 features to 5 | PCA |
| **Time-series forecasting** | Number over time | Next month's sales | Seasonal naive, ETS, ARIMA, ML with lags |
| **Recommendation / ranking** | Ranked list | Products to show | Collaborative filtering, learning to rank |

```python run
import pandas as pd
h = pd.read_csv("house_prices.csv"); tc = pd.read_csv("telecom_churn.csv")
print("Regression target:", "price_lakh", "| examples:", h.price_lakh.head(3).tolist(), "| features:", [c for c in h.columns if c not in ("house_id", "price_lakh")])
print("Classification target: churn", tc.churn.value_counts().to_dict(), "| features:", [c for c in tc.columns if c not in ("customer_id", "churn")])
```

**Vocabulary:** a row is an **observation/sample**; input columns are **features** (X, predictors, independent variables); the column to predict is the **target** (y, label, dependent variable); the learned function is the **model**; using it on new data is **inference/prediction**.

## From business problem to ML problem

```python fig: Framing comes before algorithms.
dg.flow(["Business goal:\nreduce churn", "Decision:\nwho gets a\nretention offer?", "Prediction:\nP(churn in\nnext 30 days)", "Data: unit,\nfeatures,\nlabel, window", "Metric:\nrecall@top 10%,\nprofit", "Action &\nmeasurement\n(A/B test)"], title="Framing an ML problem")
```

| Question | Churn example |
|---|---|
| What decision will the prediction change? | Which 10% of customers receive a ₹200 retention offer |
| Unit of prediction | One customer, scored monthly |
| Target definition | Cancelled within 30 days after the scoring date |
| Features (only information available **at prediction time**) | Tenure, contract, charges, support calls in the previous 90 days |
| Success metric | Recall in the top 10%, net profit of the campaign |
| Baseline | Current rule: target month-to-month customers with 3+ calls |
| Constraints | Explainability for the retention team, privacy, weekly batch scoring |

:::warning Data leakage
Using information that would not be available at prediction time (for example "number of cancellation calls" recorded **after** the customer decided to leave) gives brilliant test scores and useless production models. Define a clear cut-off date for features and a later window for the label.
:::

### When not to use ML

Simple rules work; there is little data or no labels; mistakes are unacceptable and must be explained exactly; the pattern changes faster than you can retrain; or nobody will act on the predictions. Always compare with a simple baseline.

## The ML lifecycle

```python fig: CRISP-DM extended with MLOps: an iterative cycle, not a straight line.
dg.cycle(["Business\nunderstanding", "Data\nunderstanding\n(EDA)", "Data\npreparation", "Modelling", "Evaluation", "Deployment", "Monitoring\n& retraining"], title="ML project lifecycle")
```

| Stage | Key work | Typical tools |
|---|---|---|
| Business understanding | Goal, decision, metric, baseline, constraints | Workshops, documents |
| Data understanding | Sources, EDA, quality, label definition | SQL, pandas, plots (Python track) |
| Data preparation | Cleaning, encoding, scaling, feature engineering, train/test split | pandas, scikit-learn pipelines |
| Modelling | Train candidate models, tune hyperparameters | scikit-learn, XGBoost, LightGBM |
| Evaluation | Test-set metrics, error analysis, fairness, business value | metrics, SHAP |
| Deployment | Batch scoring or API, integration with apps | FastAPI, Docker, cloud ML platforms |
| Monitoring | Data drift, performance decay, retraining | MLflow, Evidently, dashboards |

In practice, most time goes to framing, data preparation and deployment, not to choosing algorithms.

## Linear vs non-linear models and link functions

A **linear model** predicts with a weighted sum of features:

$$\hat y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots + \beta_p x_p$$

**Generalised linear models** pass that linear score through a **link function** so the output fits the target type:

| Target | Model | Link (inverse) | Output |
|---|---|---|---|
| Any real number | Linear regression | Identity | ŷ = score |
| Probability (0–1) | Logistic regression | Logit ⇄ sigmoid 1/(1 + e^(−score)) | P(y = 1) |
| Count (0, 1, 2…) | Poisson regression | Log ⇄ exp(score) | Expected count |

```python fig: The same linear score through three link functions: identity (regression), sigmoid (classification probability) and exp (counts).
import numpy as np, matplotlib.pyplot as plt
z = np.linspace(-6, 6, 300)
fig, axes = plt.subplots(1, 3, figsize=(11, 2.8))
for ax, (y, t, c) in zip(axes, [(z, "identity: linear regression", "#7C3AED"), (1 / (1 + np.exp(-z)), "sigmoid: logistic regression", "#DB2777"), (np.exp(z / 2), "exp: Poisson regression", "#0E9F8E")]):
    ax.plot(z, y, color=c, lw=2.2); ax.set_title(t, fontsize=10, weight="bold"); ax.set_xlabel("linear score β·x"); ax.spines[["top", "right"]].set_visible(False)
```

**Non-linear models** (decision trees, random forests, gradient boosting, KNN, neural networks) capture thresholds and interactions automatically, usually at the cost of interpretability.

```python fig: A linear model draws one straight boundary; a non-linear model can bend around the data.
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
X, y = make_moons(400, noise=.25, random_state=0)
xx, yy = np.meshgrid(np.linspace(-1.6, 2.6, 300), np.linspace(-1.2, 1.7, 300))
fig, axes = plt.subplots(1, 2, figsize=(10, 3.3))
for ax, m, t in [(axes[0], LogisticRegression(), "Linear (logistic regression)"), (axes[1], RandomForestClassifier(200, max_depth=6, random_state=0), "Non-linear (random forest)")]:
    m.fit(X, y); Z = m.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    ax.contourf(xx, yy, Z, alpha=.18, cmap="PuRd"); ax.scatter(X[:, 0], X[:, 1], c=y, cmap="PuRd", s=10, edgecolor="none")
    ax.set_title(f"{t}: accuracy {m.score(X, y):.0%}", fontsize=10, weight="bold"); ax.set_xticks([]); ax.set_yticks([])
```

## Overfitting and generalisation (preview)

A model must work on **new** data. Memorising the training set (overfitting) fails in production; being too simple (underfitting) misses real patterns. We therefore always evaluate on data the model has not seen (lessons 8 and 15).

## Where does GenAI fit?

Large language models are trained with self-supervised learning on huge text corpora, then adapted with instruction tuning and reinforcement learning from human feedback. In analytics they **complement** classical ML: LLMs read and write text, code and SQL; classical models remain best for structured, tabular prediction (churn, credit risk, demand), where gradient boosting usually wins. The GenAI track covers LLMs, RAG and agents.

## Summary

:::key
- ML learns rules from data; statistics focuses on inference, ML on prediction, with much overlap.
- Supervised (regression, classification), unsupervised (clustering, PCA, anomalies), reinforcement and self-supervised (LLMs) learning.
- Frame first: decision, unit, target and time windows, leak-free features, metric, baseline.
- Lifecycle: business → data → preparation → modelling → evaluation → deployment → monitoring, iteratively.
- Linear models use link functions (identity, sigmoid, exp); non-linear models capture thresholds and interactions.
:::

:::quiz
Q: Predicting next month's sales in rupees is…
* Regression
- Classification
- Clustering
- Reinforcement learning
> The target is a number.

Q: Grouping customers into segments without labels is…
- Supervised learning
* Unsupervised learning (clustering)
- Regression
- A/B testing
> No target column.

Q: What is data leakage?
* Using information in training that would not be available at prediction time
- Losing data in a crash
- Sharing data publicly
- Missing values
> It inflates test scores.

Q: Which link function does logistic regression use to output a probability?
- Identity
* Sigmoid (inverse of the logit)
- Exponential
- Square root
> It maps any score to 0–1.

Q: Which stage often takes the most time in real ML projects?
- Picking the algorithm
* Data understanding and preparation
- Writing the final slide
- Installing Python
> Data work dominates.

Q: When might you NOT use ML?
* When a simple rule works well or nobody will act on predictions
- When you have lots of data
- When the pattern is complex
- When predictions save money
> Start with a baseline.
:::

:::exercise Frame these problems
For each, state the ML type, target, unit, two leak-free features, the metric and the action: (1) predicting loan default at application; (2) forecasting daily units for each store; (3) grouping 5,000 products by sales pattern; (4) flagging suspicious card transactions in real time.
???
(1) Classification; default within 12 months; applicant; income, debt-to-income; recall/precision at the approval threshold and expected loss; approve/decline/price. (2) Regression/forecasting; units per store-day; store-day; lagged sales, calendar/holidays; MAPE/WAPE; stock orders. (3) Clustering; none; product; weekly sales profile, price; silhouette + business sense; assortment strategy. (4) Classification (imbalanced); fraud label; transaction; amount vs customer average, merchant risk; precision/recall at alert capacity; block or step-up authentication.
:::

:::interview Questions you may be asked
**Q: Explain machine learning to a non-technical person.**
Instead of writing rules ourselves, we show the computer many past examples with the right answers, and it learns patterns it can apply to new cases, like an employee learning from experience.

**Q: Supervised vs unsupervised learning?**
Supervised learning uses labelled examples to predict a target; unsupervised learning finds structure such as groups or compressed representations without labels.

**Q: How do you start an ML project?**
Clarify the business decision and success metric, define the target and prediction time, check data availability and leakage, set a simple baseline, then iterate on models.
:::
