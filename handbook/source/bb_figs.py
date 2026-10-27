"""Statistics and maths illustrations for the Building Blocks handbook (generated data, labelled)."""
import os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
DS = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(DS, "site", "img", "bb"); os.makedirs(D, exist_ok=True)
NAVY, AMBER, TEAL, RED, PURP, GREY = "#1F3864", "#E9A23B", "#2E8B8B", "#C8553D", "#6A4C93", "#8C8C8C"
plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 140, "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titleweight": "bold", "axes.prop_cycle": matplotlib.cycler(color=[NAVY, AMBER, TEAL, RED, PURP])})
def save(n): plt.tight_layout(); plt.savefig(os.path.join(D, n + ".png"), bbox_inches="tight", facecolor="white"); plt.close("all")
rng = np.random.default_rng(7)

# skewness
fig, ax = plt.subplots(1, 3, figsize=(13, 3.3))
for a, data, t in [(ax[0], -rng.gamma(2, 2, 5000) + 20, "Left (negative) skew\nmean < median"), (ax[1], rng.normal(10, 2, 5000), "Symmetric\nmean ≈ median ≈ mode"),
                   (ax[2], rng.gamma(2, 2, 5000), "Right (positive) skew\nmean > median  e.g. salaries")]:
    a.hist(data, bins=50, color="#B7C6E2"); a.axvline(np.mean(data), color=RED, lw=2, label=f"mean {np.mean(data):.1f}")
    a.axvline(np.median(data), color=NAVY, lw=2, ls="--", label=f"median {np.median(data):.1f}"); a.set_title(t); a.set_yticks([]); a.legend(frameon=False, fontsize=8)
save("skew")

# boxplot anatomy
d = np.concatenate([rng.normal(50, 8, 200), [92, 96, 8]]); q1, med, q3 = np.percentile(d, [25, 50, 75]); iqr = q3 - q1
fig, ax = plt.subplots(figsize=(9, 2.8)); ax.boxplot(d, orientation="horizontal", widths=.45, patch_artist=True, boxprops=dict(facecolor="#E8EEF9"))
for x, lab in [(q1, f"Q1 = {q1:.0f}"), (med, f"Median = {med:.0f}"), (q3, f"Q3 = {q3:.0f}"), (q1 - 1.5 * iqr, "Q1 − 1.5·IQR"), (q3 + 1.5 * iqr, "Q3 + 1.5·IQR")]:
    ax.annotate(lab, (x, 1.25), ha="center", fontsize=8.5, color=NAVY)
ax.annotate("outliers", (94, 1.08), ha="center", fontsize=8.5, color=RED); ax.annotate("outlier", (8, 1.08), ha="center", fontsize=8.5, color=RED)
ax.set_yticks([]); ax.set_ylim(.6, 1.45); ax.set_title(f"Box plot anatomy (generated exam scores): IQR = Q3 − Q1 = {iqr:.0f}"); save("boxplot")

# correlation
fig, ax = plt.subplots(1, 4, figsize=(14, 3.1)); x = rng.normal(0, 1, 150)
for a, r, t in zip(ax, [.95, .6, 0, -.85], ["Strong positive", "Moderate positive", "No correlation", "Strong negative"]):
    y = r * x + np.sqrt(1 - r ** 2) * rng.normal(0, 1, 150); a.scatter(x, y, s=10, color=NAVY, alpha=.7)
    a.set_title(f"{t}\nr = {np.corrcoef(x, y)[0, 1]:.2f}"); a.set_xticks([]); a.set_yticks([])
save("correlation")

# distributions
fig, ax = plt.subplots(1, 4, figsize=(14, 3.1))
k = np.arange(0, 11); ax[0].bar(k, stats.binom.pmf(k, 10, .3), color=NAVY); ax[0].set_title("Binomial (n=10, p=0.3)\n# buyers out of 10 visitors")
k = np.arange(0, 15); ax[1].bar(k, stats.poisson.pmf(k, 4), color=AMBER); ax[1].set_title("Poisson (λ=4)\n# calls per minute")
xx = np.linspace(-.2, 1.2, 300); ax[2].plot(xx, stats.uniform.pdf(xx), color=TEAL, lw=2); ax[2].fill_between(xx, stats.uniform.pdf(xx), color=TEAL, alpha=.2); ax[2].set_title("Uniform (0,1)\nrandom number")
xx = np.linspace(-4, 4, 300); ax[3].plot(xx, stats.norm.pdf(xx), color=RED, lw=2); ax[3].fill_between(xx, stats.norm.pdf(xx), color=RED, alpha=.15); ax[3].set_title("Normal (0,1)\nheights, measurement error")
for a in ax: a.set_yticks([])
save("distributions")

# confidence intervals
mu, sig, n = 100, 15, 30; fig, ax = plt.subplots(figsize=(9, 4)); miss = 0
for i in range(25):
    s = rng.normal(mu, sig, n); m = s.mean(); h = 1.96 * s.std(ddof=1) / np.sqrt(n); bad = not (m - h <= mu <= m + h); miss += bad
    ax.plot([m - h, m + h], [i, i], color=RED if bad else NAVY, lw=2); ax.plot(m, i, "o", color=RED if bad else NAVY, ms=4)
ax.axvline(mu, color=AMBER, ls="--", lw=2, label="true mean μ = 100"); ax.set_yticks([]); ax.legend(frameon=False, loc="lower right")
ax.set_title(f"25 samples, 25 different 95% confidence intervals: {25 - miss} contain μ (red ones miss)"); save("ci")

# z-score
xx = np.linspace(-4, 4, 400); fig, ax = plt.subplots(figsize=(8.5, 3)); ax.plot(xx, stats.norm.pdf(xx), color=NAVY)
m = xx <= 1.5; ax.fill_between(xx[m], stats.norm.pdf(xx[m]), color=AMBER, alpha=.6)
ax.text(-.4, .15, f"P(Z ≤ 1.5) = {stats.norm.cdf(1.5):.4f}", fontweight="bold"); ax.set_yticks([])
ax.set_title("z = (x − mean) / SD.  Score 80 with mean 65, SD 10 → z = 1.5 → better than 93.3% of students"); save("zscore")

# maths: vectors
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
a_, b_ = np.array([3, 1]), np.array([1, 2])
for v, c, l in [(a_, NAVY, "a = [3, 1]"), (b_, AMBER, "b = [1, 2]"), (a_ + b_, RED, "a + b = [4, 3]")]:
    ax[0].quiver(0, 0, *v, angles="xy", scale_units="xy", scale=1, color=c, label=l, width=.012)
ax[0].quiver(*a_, *b_, angles="xy", scale_units="xy", scale=1, color=AMBER, alpha=.4, width=.01)
ax[0].set_xlim(-.5, 5); ax[0].set_ylim(-.5, 4); ax[0].grid(alpha=.3); ax[0].legend(frameon=False); ax[0].set_aspect("equal"); ax[0].set_title("Vector addition (tip-to-tail)")
ax[1].scatter([25, 32, 47, 51, 38], [3.1, 4.5, 8.2, 9.0, 6.1], s=60, color=NAVY)
for i, (x_, y_) in enumerate(zip([25, 32, 47, 51, 38], [3.1, 4.5, 8.2, 9.0, 6.1])): ax[1].annotate(f"customer {i+1}\n[{x_}, {y_}]", (x_, y_), fontsize=7.5, xytext=(4, 4), textcoords="offset points")
ax[1].set_xlabel("age"); ax[1].set_ylabel("income (₹ lakh)"); ax[1].set_title("Each row of data is a vector (a point in space)"); save("vectors")

# functions
x = np.linspace(-3, 3, 300); fig, ax = plt.subplots(1, 5, figsize=(16, 3))
for a, y, t in [(ax[0], 2 * x + 1, "Linear y = 2x + 1"), (ax[1], x ** 2, "Quadratic y = x²"), (ax[2], np.exp(x), "Exponential y = eˣ"),
                (ax[3], np.log(np.linspace(.05, 6, 300)), "Logarithm y = ln x"), (ax[4], 1 / (1 + np.exp(-2 * x)), "Sigmoid 1/(1+e⁻ᶻ)")]:
    xs = np.linspace(.05, 6, 300) if "ln" in t else x
    a.plot(xs, y, lw=2.2, color=NAVY); a.axhline(0, color=GREY, lw=.6); a.axvline(0, color=GREY, lw=.6); a.set_title(t)
save("functions")

# derivative tangent
x = np.linspace(-1, 4, 300); f = lambda t: (t - 1.5) ** 2 + 1
fig, ax = plt.subplots(figsize=(8, 3.6)); ax.plot(x, f(x), color=NAVY, lw=2)
for x0, c in [(0, RED), (1.5, TEAL), (3.2, AMBER)]:
    s = 2 * (x0 - 1.5); xt = np.linspace(x0 - .8, x0 + .8, 10); ax.plot(xt, f(x0) + s * (xt - x0), color=c, lw=2, label=f"at x={x0}: slope = {s:+.1f}"); ax.plot(x0, f(x0), "o", color=c)
ax.legend(frameon=False); ax.set_title("Derivative = slope of the tangent. Slope 0 at the minimum (x = 1.5)"); save("derivative")

# matrix heat (data as matrix)
fig, ax = plt.subplots(figsize=(7, 3)); M = np.array([[25, 3.1, 2], [32, 4.5, 5], [47, 8.2, 1], [51, 9.0, 7]])
ax.imshow((M - M.mean(0)) / M.std(0), cmap="Blues"); ax.set_xticks(range(3)); ax.set_xticklabels(["age", "income", "visits"]); ax.set_yticks(range(4)); ax.set_yticklabels([f"cust {i+1}" for i in range(4)])
for i in range(4):
    for j in range(3): ax.text(j, i, M[i, j], ha="center", va="center", fontsize=11, fontweight="bold", color=NAVY)
ax.set_title("A dataset is a matrix X (4 rows × 3 features)"); save("matrix")

# chart chooser mini
fig, ax = plt.subplots(1, 5, figsize=(16, 3)); cats = ["N", "S", "E", "W"]; v = [42, 31, 27, 18]
ax[0].bar(cats, v, color=NAVY); ax[0].set_title("Column: compare")
ax[1].plot(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], [20, 24, 23, 29, 33, 31], "o-", color=AMBER); ax[1].set_title("Line: trend")
ax[2].pie(v, labels=cats, autopct="%1.0f%%", colors=[NAVY, AMBER, TEAL, RED]); ax[2].set_title("Pie: share (≤5 parts)")
ax[3].scatter(rng.normal(50, 10, 60), rng.normal(50, 10, 60), s=10, color=TEAL); ax[3].set_title("Scatter: relationship")
ax4 = ax[4]; ax4.bar(cats, v, color=NAVY); a2 = ax4.twinx(); a2.plot(cats, np.cumsum(v) / sum(v) * 100, "o-", color=RED); a2.set_ylim(0, 105); ax4.set_title("Combo/Pareto: 2 measures")
save("chart_types")
print("bb figs:", sorted(os.listdir(D)))
