---
num: 23
title: "Clustering II and Dimensionality Reduction: Hierarchical, DBSCAN, Gaussian Mixtures, PCA, t-SNE and UMAP"
live: "ML track (added)"
updated: "scikit-learn 1.7+"
level: Advanced
duration: 120 min
summary: Go beyond K-means. Agglomerative hierarchical clustering with dendrograms and linkage choices, density-based DBSCAN for irregular shapes and outliers, Gaussian mixture models with soft assignments, and dimensionality reduction with PCA (explained variance, loadings, compression), plus t-SNE and UMAP for visualisation, applied to video-game sales and HR data.
datasets: [video_game_sales.csv, hr_employees.csv]
outcomes:
  - Build and read a dendrogram and choose a linkage method
  - Use DBSCAN to find irregular clusters and noise points, and tune eps and min_samples
  - Fit Gaussian mixture models and use soft cluster probabilities and BIC
  - Apply PCA, read explained variance and loadings, and use PCA before modelling
  - Know when to use t-SNE or UMAP and their pitfalls
---

## Hierarchical clustering

**Agglomerative** clustering starts with every point as its own cluster and repeatedly merges the two closest clusters. The full merge history is a tree, the **dendrogram**: cut it at a height to get clusters, with no need to fix k in advance.

```python run
import pandas as pd, numpy as np, matplotlib.pyplot as plt
pd.set_option("display.width", 160); pd.set_option("display.max_columns", 20)
vg = pd.read_csv("video_game_sales.csv")
pub = vg.groupby("genre").agg(titles=("name", "nunique"), na=("na_sales", "sum"), eu=("eu_sales", "sum"), jp=("jp_sales", "sum"), other=("other_sales", "sum"), total=("global_sales", "sum"))
shares = pub[["na", "eu", "jp", "other"]].div(pub.total, axis=0).round(3)                 # regional mix per genre
print(shares.join(pub[["titles", "total"]].round(1)).sort_values("total", ascending=False).head(6))
```

```python fig: Dendrogram of game genres by regional sales mix (Ward linkage). Cutting where the vertical gaps are largest suggests the number of clusters.
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.preprocessing import StandardScaler
Zs = StandardScaler().fit_transform(shares)
L = linkage(Zs, method="ward")
fig, ax = plt.subplots(figsize=(10, 3.6))
dendrogram(L, labels=shares.index.tolist(), leaf_rotation=45, leaf_font_size=9, color_threshold=0.6 * L[:, 2].max(), ax=ax)
ax.set_ylabel("merge distance"); ax.spines[["top", "right"]].set_visible(False)
```

```python run
shares["cluster"] = fcluster(L, t=3, criterion="maxclust")
print(shares.groupby("cluster")[["na", "eu", "jp", "other"]].mean().round(2), "\n", shares.groupby("cluster").apply(lambda g: g.index.tolist(), include_groups=False).to_dict())
```

Three clear groups appear: role-playing games sell about 40% of units in Japan, fighting and puzzle games about 27%, and the other genres are driven by North America and Europe with only 13–15% in Japan. A publisher could use this to plan regional launches and marketing budgets.

| Linkage | Merges clusters with… | Behaviour |
|---|---|---|
| Ward | Smallest increase in within-cluster variance | Compact, similar-size clusters (default choice) |
| Complete | Smallest maximum pairwise distance | Compact clusters, sensitive to outliers |
| Average | Smallest average distance | Balanced |
| Single | Smallest minimum distance | Long "chains"; finds odd shapes but chains noise |

Hierarchical clustering is ideal for small datasets (hundreds to a few thousand items) where the tree itself is informative: product taxonomies, store groupings, gene families. It is O(n²) in memory, so not for millions of rows.

## DBSCAN: density-based clusters and noise

**DBSCAN** groups points that are densely packed (at least `min_samples` neighbours within distance `eps`) and labels isolated points as **noise** (−1). It finds clusters of any shape and does not need k.

```python fig: K-means vs DBSCAN on non-spherical data with outliers: DBSCAN follows the shapes and marks outliers (grey).
from sklearn.datasets import make_moons
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
rng = np.random.default_rng(0)
Xm, _ = make_moons(400, noise=.06, random_state=0); Xm = np.vstack([Xm, rng.uniform([-1.5, -1], [2.5, 1.5], (25, 2))])
fig, axes = plt.subplots(1, 2, figsize=(10, 3.4))
for ax, (name, model) in zip(axes, [("K-means (k=2)", KMeans(2, n_init=10, random_state=0)), ("DBSCAN (eps=0.15, min_samples=8)", DBSCAN(eps=.15, min_samples=8))]):
    lab = model.fit_predict(Xm); cols = np.array(["#7C3AED", "#DB2777", "#0E9F8E", "#E2A400"])
    ax.scatter(Xm[:, 0], Xm[:, 1], c=np.where(lab < 0, "#BBBBBB", cols[lab % 4]), s=10); ax.set_title(name, fontsize=10, weight="bold"); ax.set_xticks([]); ax.set_yticks([])
```

```python run
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import silhouette_score
d8 = np.sort(NearestNeighbors(n_neighbors=8).fit(Xm).kneighbors(Xm)[0][:, -1])
print("8th-neighbour distance percentiles (pick eps near the 'knee'):", np.percentile(d8, [50, 80, 90, 95]).round(3))
for eps in (0.08, 0.12, 0.15, 0.25):
    lab = DBSCAN(eps=eps, min_samples=8).fit_predict(Xm)
    print(f"eps {eps}: clusters {len(set(lab)) - (-1 in lab)} | noise points {(lab == -1).sum()}")
```

Tuning: set `min_samples` ≈ 2 × number of features (or more for noisy data); choose `eps` from the "knee" of the sorted k-nearest-neighbour distance plot. DBSCAN struggles when clusters have very different densities (HDBSCAN, available as `sklearn.cluster.HDBSCAN`, handles that).

**Uses:** geographic hotspots (delivery addresses, crime), anomaly detection (noise points), sensor data, irregular customer groups.

## Gaussian mixture models

A **GMM** assumes the data come from a mix of k Gaussian (bell-shaped) clusters, which may be elongated and of different sizes. Each point gets a **probability** of belonging to each cluster (soft clustering).

```python run
from sklearn.mixture import GaussianMixture
hr = pd.read_csv("hr_employees.csv")
Xh = StandardScaler().fit_transform(np.c_[hr.age, np.log(hr.monthly_income), hr.years_at_company])
bics = {k: round(GaussianMixture(k, covariance_type="full", random_state=0).fit(Xh).bic(Xh), 1) for k in range(1, 7)}
print("BIC by k (lower is better):", bics)
g = GaussianMixture(min(bics, key=bics.get), covariance_type="full", random_state=0).fit(Xh)
probs = g.predict_proba(Xh)
hr["gmm"] = probs.argmax(1); hr["certainty"] = probs.max(1).round(2)
print(hr.groupby("gmm").agg(n=("age", "size"), age=("age", "median"), income=("monthly_income", "median"), years=("years_at_company", "median"), attrition=("attrition", lambda s: round((s == "Yes").mean(), 3))))
print("share of employees assigned with < 70% certainty:", round((hr.certainty < 0.7).mean(), 3))
```

GMMs choose k with **BIC/AIC**, give uncertainty for borderline points, and are also used for anomaly detection (low likelihood = unusual).

## Dimensionality reduction: PCA

**Principal component analysis** finds new axes (principal components) that are uncorrelated linear combinations of the original features, ordered by how much variance they explain. Keeping the first few compresses the data with minimal information loss.

```python fig: PCA finds the direction of greatest variance (PC1) and the next orthogonal direction (PC2).
from sklearn.decomposition import PCA
rng2 = np.random.default_rng(3); a = rng2.normal(0, 1, 300); pts = np.c_[a, 0.6 * a + rng2.normal(0, .35, 300)]
p2 = PCA(2).fit(pts)
fig, ax = plt.subplots(figsize=(5.5, 3.8)); ax.scatter(*pts.T, s=8, color="#C4B5FD")
for vec, var, c, lab in zip(p2.components_, p2.explained_variance_, ["#7C3AED", "#DB2777"], ["PC1", "PC2"]):
    ax.annotate("", xy=p2.mean_ + vec * 2 * np.sqrt(var), xytext=p2.mean_, arrowprops=dict(arrowstyle="->", color=c, lw=2.5)); ax.text(*(p2.mean_ + vec * 2.3 * np.sqrt(var)), lab, color=c, weight="bold")
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
```

```python run
num = hr[["age", "years_at_company", "monthly_income", "job_satisfaction", "distance_from_home_km", "performance_rating"]].assign(monthly_income=np.log(hr.monthly_income))
pca = PCA().fit(StandardScaler().fit_transform(num))
ev = pd.Series(pca.explained_variance_ratio_, index=[f"PC{i + 1}" for i in range(len(num.columns))])
print("explained variance:", ev.round(3).to_dict(), "| cumulative:", ev.cumsum().round(3).tolist())
load = pd.DataFrame(pca.components_[:3].T, index=num.columns, columns=["PC1", "PC2", "PC3"]).round(2)
print(load)
```

**Reading loadings:** PC1 loads heavily on years at company and income (and partly age), so it is a "seniority" axis. Later components capture what is left (satisfaction, distance, rating), which are nearly uncorrelated with each other, so each needs its own component.

```python run
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
digits = load_digits()
p = PCA().fit(digits.data); k95 = int(np.searchsorted(np.cumsum(p.explained_variance_ratio_), 0.95) + 1)
print(f"digits: {digits.data.shape[1]} pixel features → {k95} components keep 95% of the variance")
for n in (5, 15, k95, 64):
    s = cross_val_score(make_pipeline(StandardScaler(), PCA(n), LogisticRegression(max_iter=3000)), digits.data, digits.target, cv=5).mean()
    print(f"  {n:2d} components → logistic regression accuracy {s:.3f}")
```

| PCA is useful for | Caution |
|---|---|
| Compressing many correlated features | Scale features first |
| Removing multicollinearity before linear models | Components are harder to explain |
| Visualising high-dimensional data in 2-D | Linear only; captures variance, not class separation |
| Speeding up distance-based models | Fit PCA on training data only (inside the pipeline) |

## t-SNE and UMAP for visualisation

**t-SNE** and **UMAP** are non-linear methods that place similar points close together in 2-D. They make beautiful maps of embeddings, images and text.

```python fig: Handwritten digits (64 features) projected to 2-D by PCA and by t-SNE. t-SNE separates the digit groups much more clearly.
from sklearn.manifold import TSNE
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.9))
for ax, (name, emb) in zip(axes, [("PCA", PCA(2).fit_transform(digits.data)), ("t-SNE", TSNE(2, perplexity=30, init="pca", random_state=0).fit_transform(digits.data))]):
    sc = ax.scatter(emb[:, 0], emb[:, 1], c=digits.target, cmap="tab10", s=4); ax.set_title(name, weight="bold"); ax.set_xticks([]); ax.set_yticks([])
fig.colorbar(sc, ax=axes, ticks=range(10), shrink=.8)
```

Pitfalls: distances between far-apart groups and cluster sizes in t-SNE plots are not meaningful; results change with perplexity and random seed; do not cluster on t-SNE output. UMAP (`pip install umap-learn`) is faster and preserves more global structure. Both are mainly for **looking**, not for features in production models.

## Choosing a method

| Data / goal | Method |
|---|---|
| Numeric, roughly round clusters, large n | K-means (MiniBatchKMeans for very large) |
| Small n, want a hierarchy | Agglomerative + dendrogram |
| Odd shapes, outliers, unknown k | DBSCAN / HDBSCAN |
| Overlapping, elliptical clusters, need probabilities | Gaussian mixture |
| Mixed numeric + categorical | K-prototypes, Gower distance + hierarchical |
| Too many correlated features | PCA first |
| Visualise embeddings | UMAP, t-SNE |

## Summary

:::key
- Agglomerative clustering merges closest clusters; the dendrogram shows structure at every level; Ward linkage is the usual default.
- DBSCAN finds dense regions of any shape and labels noise; tune eps with a k-distance plot.
- Gaussian mixtures give soft, probabilistic clusters of different shapes; choose k with BIC.
- PCA creates uncorrelated components ordered by explained variance; read loadings to name them; fit inside pipelines.
- t-SNE and UMAP are for visualisation; distances and sizes in their plots can mislead.
:::

:::quiz
Q: What does a dendrogram show?
* The order and distance at which clusters merge
- Feature importance
- The elbow curve
- Class probabilities
> Cut it to choose clusters.

Q: Which method labels outliers as noise?
- K-means
* DBSCAN
- PCA
- Ward linkage
> Label −1.

Q: What does a Gaussian mixture give that K-means does not?
* Probabilities of belonging to each cluster and elliptical cluster shapes
- Faster training
- A dendrogram
- No need to scale
> Soft assignments.

Q: PC1 explains 45% of the variance. What does that mean?
* The first component captures 45% of the total variance in the (scaled) features
- 45% accuracy
- 45% of rows
- 45% of features are removed
> Components are ordered by variance explained.

Q: Why scale features before PCA?
* Otherwise features with large units dominate the components
- PCA requires normal data
- To remove outliers
- It is not needed
> Variance depends on units.

Q: Can you trust the distance between two far-apart clusters in a t-SNE plot?
- Yes
* No, global distances and cluster sizes are not reliable in t-SNE
- Only with perplexity 5
- Only for text
> Use it to look, not to measure.
:::

:::exercise Practice
(1) Cluster video-game platforms by regional mix with hierarchical clustering. (2) Run DBSCAN on standardised RFM features from the previous lesson: how many customers are noise? (3) Use PCA to reduce the telecom churn features to 3 components and compare logistic-regression AUC before and after.
???
```python
gen = vg.groupby("platform")[["na_sales", "eu_sales", "jp_sales", "other_sales"]].sum(); gs = gen.div(gen.sum(1), axis=0)
print(dict(zip(gs.index, fcluster(linkage(StandardScaler().fit_transform(gs), "ward"), 3, "maxclust"))))
tx = pd.read_csv("retail_transactions.csv", parse_dates=["invoice_date"]); snap = tx.invoice_date.max() + pd.Timedelta(days=1)
rf = tx.groupby("customer_id").agg(r=("invoice_date", lambda d: (snap - d.max()).days), f=("invoice_no", "nunique"), m=("amount", "sum"))
lab = DBSCAN(eps=0.5, min_samples=8).fit_predict(StandardScaler().fit_transform(np.log1p(rf))); print((lab == -1).sum())
```
:::

:::interview Questions you may be asked
**Q: K-means vs hierarchical vs DBSCAN?**
K-means: fast, needs k, round clusters. Hierarchical: no k upfront, a full tree, small data. DBSCAN: arbitrary shapes and noise detection, needs density parameters and struggles with varying densities.

**Q: What is PCA and when would you use it?**
A linear transformation to uncorrelated components ordered by variance; used to compress correlated features, remove multicollinearity, speed up models and visualise data.

**Q: How do you interpret principal components?**
Through their loadings: the weight of each original feature in the component, naming it after the features with the largest absolute weights.
:::
