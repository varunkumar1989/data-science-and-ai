---
num: 6
title: "A/B Testing and Experimentation: Design, Power, Analysis and Pitfalls"
live: "ML class 2 (case study)"
updated: "statsmodels 0.1x · SciPy 1.1x"
level: Intermediate
duration: 120 min
summary: Run product experiments the way data teams at e-commerce and fintech companies do. Choose a metric and guardrails, size the test with power analysis, randomise, analyse conversion and revenue with z-tests, t-tests and bootstrap intervals, check sample-ratio mismatch, avoid peeking and novelty effects, and write the decision memo, using a new-checkout experiment.
datasets: [ab_test.csv]
outcomes:
  - Design an experiment with a hypothesis, primary metric, guardrail metrics and randomisation unit
  - Compute the required sample size with power analysis and a minimum detectable effect
  - Analyse conversion (two-proportion z-test) and revenue per user (Welch t-test and bootstrap)
  - Check sample-ratio mismatch and recognise peeking, novelty and network effects
  - Write a launch/no-launch recommendation with uncertainty and business impact
---

## What is an A/B test?

A **randomised controlled experiment**: users are randomly split into **control (A)** and **treatment (B)**; the only systematic difference is the change you test, so differences in outcomes are **caused** by the change (up to chance, which statistics quantifies).

```python fig: The experiment lifecycle.
dg.flow(["Hypothesis\n& metrics", "Power &\nsample size", "Randomise\n& launch", "Run full\nduration\n(no peeking)", "Analyse:\nSRM, effect,\nCI, guardrails", "Decide &\ndocument"], title="A/B test lifecycle")
```

> **Case.** An online store tests a **new one-page checkout (B)** against the current checkout (A). 4,000 users were split 50/50.
> **Hypothesis:** the new checkout increases the purchase conversion rate.
> **Primary metric:** conversion = purchasers ÷ users. **Secondary:** revenue per user, average order value. **Guardrails:** refund rate, page load time, support tickets.

| Design choice | Good practice |
|---|---|
| Randomisation unit | User (not session or page view), so one person sees one version |
| Split | 50/50 maximises power |
| Duration | At least one full business cycle (1–2 weeks, including weekends); fixed in advance |
| Metric | Defined before launch; one primary metric |
| Population | Who is eligible (new users only? all platforms?) |

## Sample size and power

Before launching: how many users do we need to detect the smallest effect worth acting on (the **minimum detectable effect**, MDE)?

```python run
import numpy as np, pandas as pd
from scipy import stats
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize
base = 0.10
for target in (0.11, 0.12, 0.13):
    h = proportion_effectsize(target, base)                       # Cohen's h
    n = NormalIndPower().solve_power(effect_size=h, alpha=0.05, power=0.8, ratio=1, alternative="two-sided")
    print(f"detect {base:.0%} → {target:.0%} (+{(target - base) / base:.0%} relative): {int(np.ceil(n)):,} users per group")
```

Small lifts need very large samples. With 2,000 users per group, this test can reliably detect a lift from about 10% to 13%, not smaller ones.

```python fig: Power curves: the chance of detecting a true lift grows with sample size and effect size.
import matplotlib.pyplot as plt
ns = np.arange(200, 20001, 200)
fig, ax = plt.subplots(figsize=(8.5, 3.3))
for t, c in [(0.11, "#C4B5FD"), (0.12, "#7C3AED"), (0.13, "#DB2777")]:
    ax.plot(ns, NormalIndPower().power(proportion_effectsize(t, base), ns, 0.05), color=c, lw=2, label=f"10% → {t:.0%}")
ax.axhline(0.8, ls="--", color="#555"); ax.text(15500, 0.82, "80% power", color="#555")
ax.set_xlabel("users per group"); ax.set_ylabel("power"); ax.legend(frameon=False); ax.spines[["top", "right"]].set_visible(False)
```

## Analysis step 1: sanity checks

```python run
ab = pd.read_csv("ab_test.csv")
counts = ab.group.value_counts().sort_index(); print(counts.to_dict())
srm = stats.chisquare(counts.values)                                 # expected 50/50
print(f"sample-ratio mismatch test p = {srm.pvalue:.3f} → {'OK' if srm.pvalue > 0.01 else 'INVESTIGATE: randomisation or logging problem'}")
print("duplicate users:", ab.user_id.duplicated().sum(), "| missing:", ab.isna().sum().sum())
```

A **sample-ratio mismatch (SRM)** (for example 52/48 when you planned 50/50, with p < 0.01) signals a bug in assignment or tracking; do not trust results until it is explained.

## Analysis step 2: conversion rate

```python run
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep
g = ab.groupby("group").agg(users=("user_id", "size"), buyers=("converted", "sum"))
g["conversion"] = g.buyers / g.users
print(g)
z, p = proportions_ztest(g.buyers.values[::-1], g.users.values[::-1])          # B vs A
lo, hi = confint_proportions_2indep(g.buyers.iloc[1], g.users.iloc[1], g.buyers.iloc[0], g.users.iloc[0], compare="diff")
pa, pb = g.conversion.iloc[0], g.conversion.iloc[1]
print(f"absolute lift {100 * (pb - pa):.2f} pts (95% CI {100 * lo:.2f} to {100 * hi:.2f}) | relative lift {(pb - pa) / pa:.1%} | z = {z:.2f}, p = {p:.5f}")
```

## Analysis step 3: revenue per user and order value

```python run
a, b = ab[ab.group == "A_control"], ab[ab.group == "B_new_checkout"]
for name, col, fa, fb in [("revenue per user", "order_value", a, b), ("average order value (buyers)", "order_value", a[a.converted == 1], b[b.converted == 1])]:
    t = stats.ttest_ind(fb[col], fa[col], equal_var=False)
    print(f"{name:30s} A {fa[col].mean():8.1f} | B {fb[col].mean():8.1f} | diff {fb[col].mean() - fa[col].mean():7.1f} | Welch p = {t.pvalue:.4f}")
rng = np.random.default_rng(0)
boot = [rng.choice(b.order_value.values, len(b)).mean() - rng.choice(a.order_value.values, len(a)).mean() for _ in range(5000)]
print(f"bootstrap 95% CI for revenue-per-user difference: {np.percentile(boot, 2.5):.1f} to {np.percentile(boot, 97.5):.1f}")
```

Revenue per user mixes conversion and order size and has many zeros and a long tail; Welch's t-test (thanks to the CLT) and the bootstrap both work at this sample size.

```python fig: Conversion rate with 95% confidence intervals for each variant.
from statsmodels.stats.proportion import proportion_confint
fig, ax = plt.subplots(figsize=(6, 3))
for i, (name, row) in enumerate(g.iterrows()):
    l, u = proportion_confint(row.buyers, row.users, method="wilson")
    ax.errorbar(i, row.conversion * 100, yerr=[[100 * (row.conversion - l)], [100 * (u - row.conversion)]], fmt="o", ms=10, capsize=8, color=["#C4B5FD", "#7C3AED"][i], lw=2)
ax.set_xticks([0, 1], ["A: current", "B: new checkout"]); ax.set_xlim(-.6, 1.6); ax.set_ylabel("conversion %"); ax.spines[["top", "right"]].set_visible(False)
```

## Analysis step 4: business impact

```python run
monthly_users = 300_000
extra_buyers = monthly_users * (pb - pa)
extra_rev = monthly_users * (b.order_value.mean() - a.order_value.mean())
print(f"at {monthly_users:,} users/month: about {extra_buyers:,.0f} extra orders and ₹{extra_rev / 1e5:,.1f} lakh extra revenue per month")
print(f"conservative (lower CI bound of conversion lift): {monthly_users * lo:,.0f} extra orders")
```

## Pitfalls

| Pitfall | What goes wrong | Fix |
|---|---|---|
| **Peeking** | Checking daily and stopping at the first p < 0.05 inflates false positives to 20–30% | Fix the sample size; or use sequential tests / always-valid p-values |
| Too many metrics | Some will be "significant" by chance | One primary metric; adjust others (lesson 5) |
| Novelty / primacy effects | Users react to change itself, then revert | Run longer; analyse by week |
| SRM | Broken randomisation or logging | Chi-square check before analysis |
| Network effects | Treated users affect control users (marketplaces, social) | Cluster or geo randomisation |
| Simpson's paradox | Mix of segments differs between periods | Randomise; compare within segments |
| Underpowered tests | "No effect" just means "too small a test" | Power analysis first; report CIs |
| HARKing | Choosing the hypothesis after seeing results | Pre-register the plan |

```python run
rng = np.random.default_rng(11); false_wins = 0
for sim in range(400):                                         # A/A tests: there is NO real difference
    xa, xb = rng.random(4000) < 0.10, rng.random(4000) < 0.10
    for day in range(1, 15):                                   # peek every "day" (≈285 users per group per day)
        n = day * 285
        if proportions_ztest([xa[:n].sum(), xb[:n].sum()], [n, n])[1] < 0.05: false_wins += 1; break
print(f"stopping at the first significant daily peek: {false_wins / 400:.0%} false positives (should be 5%)")
```

## Beyond the classic test

- **CUPED / regression adjustment:** use pre-experiment behaviour as a covariate to cut variance (and required sample size) by 20–50%.
- **Bayesian A/B testing:** reports "probability that B beats A" and expected loss; intuitive for stakeholders.
- **Multi-armed bandits:** shift traffic to the winning variant during the test (good for short campaigns, worse for clean inference).
- **Quasi-experiments** when you cannot randomise: difference-in-differences, synthetic control, regression discontinuity, propensity matching.
- Platforms: Optimizely, Statsig, GrowthBook, Eppo, LaunchDarkly, Firebase A/B Testing.

## The decision memo

:::key
**Experiment:** new one-page checkout, 4,000 users, 50/50, no sample-ratio mismatch.
**Result:** conversion rose from 9.9% to 13.7% (+3.75 points, 95% CI about +1.7 to +5.8; p < 0.001). Revenue per user rose from about ₹138 to ₹203, and buyers' average order value also rose.
**Guardrails:** check refunds, load time and support tickets before rollout.
**Decision:** launch B to all users, with a 5% holdout for four weeks to confirm the effect lasts.
:::

## Summary

:::key
- Randomisation makes A/B tests causal; define the hypothesis, one primary metric, guardrails and the duration before launch.
- Power analysis sets the sample size for a minimum detectable effect; small lifts need large samples.
- Check sample-ratio mismatch first; analyse conversion with a two-proportion z-test and revenue with Welch's t-test or the bootstrap; report CIs and business impact.
- Avoid peeking, metric fishing and underpowered tests; consider CUPED, Bayesian methods and quasi-experiments where appropriate.
:::

:::quiz
Q: Why randomise users into A and B?
* So the only systematic difference between groups is the change being tested
- To make the test faster
- To increase conversion
- To avoid statistics
> Randomisation balances all other factors on average.

Q: What does a power analysis give you before the test?
- The p-value
* The sample size needed to detect a given minimum effect with a chosen probability
- The winner
- The conversion rate
> Typical settings: α = 0.05, power = 0.8.

Q: The planned split was 50/50 but you observe 53/47 with SRM p < 0.001. What do you do?
- Report the result
* Investigate the assignment or logging bug before trusting the results
- Increase α
- Remove users until it is 50/50
> SRM invalidates naive analysis.

Q: Why is stopping as soon as p < 0.05 ("peeking") a problem?
* It inflates the false-positive rate well above 5%
- It wastes traffic
- It makes p-values larger
- It is fine
> Use fixed horizons or sequential methods.

Q: Which test suits comparing conversion rates of A and B?
- Paired t-test
* Two-proportion z-test (or chi-square)
- ANOVA
- Pearson correlation
> Conversion is a proportion.

Q: A test with 300 users per group shows no significant difference. Best conclusion?
- The change has no effect
* The test may be underpowered; look at the confidence interval for the plausible range of effects
- Launch anyway
- The metric is wrong
> Absence of evidence is not evidence of absence.
:::

:::exercise Practice
(1) Compute the users per group needed to detect a lift from 13.7% to 15% conversion. (2) Analyse average order value among buyers with a Mann-Whitney test as well. (3) Simulate an A/A test 1,000 times with a fixed horizon and confirm about 5% false positives. (4) Draft a one-paragraph memo for the case where the result had been p = 0.20.
???
```python
print(NormalIndPower().solve_power(proportion_effectsize(0.15, 0.137), alpha=0.05, power=0.8))
print(stats.mannwhitneyu(b[b.converted == 1].order_value, a[a.converted == 1].order_value))
fp = np.mean([proportions_ztest([(rng.random(4000) < .1).sum(), (rng.random(4000) < .1).sum()], [4000, 4000])[1] < .05 for _ in range(1000)]); print(fp)
# Memo: "No significant difference (p = 0.20); CI ranges from −x to +y points, so we cannot rule out a meaningful lift. Extend the test to N users or test a bolder change."
```
:::

:::interview Questions you may be asked
**Q: How would you design an A/B test for a new recommendation widget?**
State the hypothesis and primary metric (e.g. revenue per user), guardrails (latency, returns), randomise by user, size it with power analysis, run full weeks, check SRM, analyse with CIs, and decide with business impact.

**Q: Your test is significant on day 3. Do you stop?**
No: stopping early inflates false positives and novelty effects can fade; finish the planned duration or use a sequential design.

**Q: What if you cannot randomise?**
Use quasi-experimental methods: difference-in-differences with a comparison group, synthetic control, regression discontinuity or matching, and state the assumptions.
:::
