# Hypothesis Testing & P-Values in Python

### A Beginner-Friendly, End-to-End Guide for Data Scientists

**What you'll be able to do after reading this:**

- Explain in plain English what a hypothesis test and a p-value actually are (and what they are _not_).
- Write a null hypothesis (H₀) and an alternative hypothesis (H₁) for a real business question.
- Run the four most common tests in Python: one-sample t-test, two-sample t-test, two-proportion z-test, chi-square test.
- Read and interpret the graphs that make tests intuitive.
- Break down every formula piece by piece.
- Apply tests to real company decisions (A/B tests, churn, quality control, marketing, risk).

**Setup:** everything below needs only three libraries.

```bash
pip install numpy scipy matplotlib pandas
```

---

## Table of Contents

1. [The Big Idea: Testing a Claim](#1-the-big-idea)
2. [Null and Alternative Hypotheses](#2-hypotheses)
3. [The Test Statistic and the Sampling Distribution](#3-test-statistic)
4. [What a P-Value Really Is](#4-p-value)
5. [Alpha, Type I & Type II Errors, and Power](#5-errors-power)
6. [The Core Formulas, Broken Down](#6-formulas)
7. [Hands-On in Python: The Running Example](#7-running-example)
8. [Graph 1: The Null Distribution and the P-Value Area](#8-graph1)
9. [Graph 2: One-Tailed vs Two-Tailed Tests](#9-graph2)
10. [Graph 3: t-Distribution vs Normal Distribution](#10-graph3)
11. [Graph 4: How Sample Size Changes the P-Value](#11-graph4)
12. [Graph 5: Type I/II Errors and Statistical Power](#12-graph5)
13. [Graph 6: A/B Test — Two-Proportion z-Test](#13-graph6)
14. [Graph 7: Permutation Test (assumption-free alternative)](#14-graph7)
15. [Graph 8: Multiple Testing and False Discoveries](#15-graph8)
16. [Chi-Square Test: Categorical Data](#16-chi-square)
17. [Confidence Intervals and Effect Size (the "so what?")](#17-ci-effect-size)
18. [Assumption Checks](#18-assumptions)
19. [Company Use Cases](#19-use-cases)
20. [Common Pitfalls](#20-pitfalls)
21. [Decision Cheat Sheet & Glossary](#21-cheat-sheet)

---

<a name="1-the-big-idea"></a>

## 1. The Big Idea

Imagine your company's coffee-delivery app promises a **30-minute average delivery**. One Monday you measure 40 orders and the average is 32.1 minutes. Two explanations exist:

1. **Nothing is wrong.** The true average is still 30; this week's sample just happened to be a bit slow. (Random chance.)
2. **Something changed.** The true average really is above 30. (A real effect.)

Hypothesis testing is a **formal procedure for choosing between these two explanations**, by asking:

> _"If explanation 1 (nothing is wrong) were true, how surprising would my data be?"_

If the data would be very surprising under "nothing is wrong", we lean toward "something changed". The p-value is precisely that "how surprising" number.

**Analogy — the courtroom.**

- The defendant is **innocent until proven guilty** → H₀ ("no effect") is assumed true until evidence is strong.
- The prosecution presents evidence → your **data**.
- "Guilty beyond reasonable doubt" → your **significance threshold (α)**.
- A jury never says "innocent" — it says "not guilty" (insufficient evidence). Similarly, a test never _proves_ H₀; it only fails to reject it.

---

<a name="2-hypotheses"></a>

## 2. Null and Alternative Hypotheses

**Null hypothesis (H₀)** — the boring, "no change, no difference, no effect" statement. _We always start by assuming it is true._

**Alternative hypothesis (H₁ or Hₐ)** — the claim you hope is true: there _is_ a difference or effect.

### Example translations

| Business question                                         | H₀ (null)                     | H₁ (alternative)           |
| --------------------------------------------------------- | ----------------------------- | -------------------------- |
| Is our delivery slower than promised?                     | μ = 30 min                    | μ ≠ 30 min (two-tailed)    |
| Is the new checkout page better?                          | p_new = p_old                 | p_new > p_old (one-tailed) |
| Do different regions return products equally often?       | distributions are independent | they are associated        |
| Does the new drug lower blood pressure more than placebo? | μ_drug = μ_placebo            | μ_drug < μ_placebo         |

### Two-tailed vs one-tailed

- **Two-tailed (non-directional):** H₁ says "different" (≠). Rejection region is split across _both_ tails. This is the **default and safest** choice.
- **One-tailed (directional):** H₁ says "greater than" or "less than". All α sits in one tail, so it is easier to pass — but you must justify the direction **before** seeing the data, and you cannot detect a surprise in the opposite direction.

**Rule for beginners:** use two-tailed unless you have a strong, pre-registered reason not to.

---

<a name="3-test-statistic"></a>

## 3. The Test Statistic and the Sampling Distribution

We can't compare a raw average (32.1 minutes) to a threshold directly, because the scale matters: is 2.1 minutes a lot when deliveries vary by ±1 minute? Or when they vary by ±20 minutes?

So we **standardise**. A **test statistic** measures:

$$\text{test statistic} = \frac{\text{signal (how far our data is from H₀)}}{\text{noise (how much random variation we expect)}}$$

That ratio has a name in every test:

- **z** or **t** for means and proportions ("how many standard errors away?")
- **χ²** (chi-square) for counts/categories
- **F** for comparing several group means at once (ANOVA)

The **sampling distribution** is the probability distribution of that statistic _if H₀ were true and we repeated the experiment thousands of times_. It is the ruler we measure our result against.

**Key mental model:** imagine running your experiment 10,000 times in a parallel universe where nothing changed. Some runs give a slightly high average, some slightly low, most near the truth. That cloud of outcomes is the sampling distribution. If your one real result sits far out in the tail of that cloud, "nothing changed" becomes hard to believe.

---

<a name="4-p-value"></a>

## 4. What a P-Value Really Is

> **P-value = the probability of observing a test statistic at least as extreme as the one we got, _assuming H₀ is true_.**

Symbolically, for a two-tailed test:

$$p = 2 \times P(T \ge |t_{\text{obs}}| \mid H_0)$$

**Reading it in words:** "If there really were no effect, how often would random luck alone produce a difference this big or bigger?" A small p-value means the data are **inconsistent with H₀**.

### Interpretation table

| p-value   | Plain-English reading                                                          |
| --------- | ------------------------------------------------------------------------------ |
| p = 0.45  | Very compatible with "no effect". Nothing to see.                              |
| p = 0.08  | Slightly surprising, but within normal luck. Do not claim a win.               |
| p = 0.03  | Surprising enough (under the 0.05 rule) to act — but a 3% chance we're fooled. |
| p = 0.001 | Very hard to explain by luck alone. Strong evidence.                           |

### What a p-value is **NOT** (the four classic mistakes)

1. ❌ **It is not the probability that H₀ is true.** It is computed _assuming_ H₀ is true. It cannot then be the chance H₀ is true.
2. ❌ **It is not the probability the result happened "by chance".** Every result has _some_ randomness in it.
3. ❌ **It is not the size of the effect.** A tiny, useless effect can have p = 0.0001 if n is huge.
4. ❌ **p = 0.03 does not mean the result is 97% likely to replicate.** With small samples, replication rates are far lower than 1 − p.

**Also:** "p < 0.05" means _statistically significant_, not _practically important_. Always report the effect size and confidence interval alongside it (Section 17).

---

<a name="5-errors-power"></a>

## 5. Alpha, Type I & Type II Errors, and Power

Because we decide from a **sample**, not the whole population, two mistakes are possible:

|                                   | Reality: H₀ true (no effect)          | Reality: H₁ true (real effect)                                |
| --------------------------------- | ------------------------------------- | ------------------------------------------------------------- |
| **Test says "reject H₀"**         | **Type I error (α)** = false positive | ✅ Correct — True Positive (**Power = 1 − β**)                |
| **Test says "fail to reject H₀"** | ✅ Correct — True Negative            | **Type II error (β)** = false negative (missed a real effect) |

- **α (significance level)** — the false-positive rate you are willing to accept. Convention: 0.05 (5%). You choose it _before_ the test. It defines the **rejection region**.
- **β** — the false-negative rate. Typically 0.10–0.20.
- **Power (1 − β)** — the chance of detecting a real effect. Industry target is **80%**.

**The four levers of power** (memorise these):

1. **Bigger effect** → easier to detect.
2. **Bigger sample** → easier to detect.
3. **Less noise (smaller variance)** → easier to detect.
4. **Higher α** (e.g. 0.10 instead of 0.05) → easier to detect, but more false positives.

**Sample size formula** for comparing two means (equal groups):

$$n_{\text{per group}} = \frac{2\,(z_{1-\alpha/2} + z_{1-\beta})^2 \cdot \sigma^2}{\Delta^2}$$

Broken down:

- `z_{1-α/2}` = 1.96 at α = 0.05 — the "significance" part.
- `z_{1-β}` = 0.84 at 80% power — the "detection" part.
- `σ²` = variance of your metric (the noise).
- `Δ` = the minimum effect you care about (the signal).
- Note the **square**: halving Δ quadruples the sample you need. This is why "we only care about tiny differences" is an expensive sentence.

---

<a name="6-formulas"></a>

## 6. The Core Formulas, Broken Down

### 6.1 One-sample z-test (population σ known)

$$z = \frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}}$$

| Piece    | Meaning                       | Intuition                                  |
| -------- | ----------------------------- | ------------------------------------------ |
| `x̄`      | sample mean                   | our evidence                               |
| `μ₀`     | hypothesised mean under H₀    | the claim we're testing                    |
| `x̄ − μ₀` | **signal**                    | how far we are from the claim              |
| `σ`      | population standard deviation | the natural noise of one observation       |
| `√n`     | square root of sample size    | averaging n things shrinks noise this much |
| `σ/√n`   | **standard error (SE)**       | noise of the _mean_, not of one value      |
| `z`      | ratio                         | "how many standard errors away from H₀"    |

### 6.2 One-sample t-test (population σ unknown — the realistic case)

$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}, \qquad df = n - 1$$

- `s` = **sample** standard deviation (we estimate σ from data — this uncertainty is why we use t instead of z).
- `df` (degrees of freedom) = how many independent pieces of information remain after estimating the mean. With n data points and 1 estimated mean, you have n − 1 left. _Lower df → fatter tails → harder to reach significance._

### 6.3 Two-sample t-test (Welch's version — compares two group means)

$$t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{\dfrac{s_1^2}{n_1} + \dfrac{s_2^2}{n_2}}}$$

- Numerator: **difference between group means** (signal).
- Denominator: standard error of that difference — **the two uncertainties add** because each mean is estimated with error. You combine variances by _adding_ them, then take the square root (Pythagoras-style).
- Welch's version doesn't assume equal variances, so it's the safe default (`scipy.stats.ttest_ind(..., equal_var=False)`).

### 6.4 Two-proportion z-test (the A/B test workhorse)

$$z = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{\hat{p}(1-\hat{p})\left(\dfrac{1}{n_1} + \dfrac{1}{n_2}\right)}}, \qquad \hat{p} = \frac{x_1 + x_2}{n_1 + n_2}$$

- `p̂₁`, `p̂₂` = observed conversion rates of the two groups.
- Numerator: **lift** (e.g. 12.5% − 9.2% = 3.3 percentage points).
- `p̂` = **pooled** rate — the best estimate of the single "true" rate _if H₀ is true_.
- `p̂(1 − p̂)` = variance of a single Bernoulli trial (a click is 0 or 1). It peaks at p̂ = 0.5 and shrinks near 0 or 1.
- `1/n₁ + 1/n₂` = uncertainty grows when either sample is small.

### 6.5 Chi-square test of independence (categorical data)

$$\chi^2 = \sum_{i,j} \frac{(O_{ij} - E_{ij})^2}{E_{ij}}, \qquad E_{ij} = \frac{(\text{row } i \text{ total}) \times (\text{column } j \text{ total})}{N}$$

- `O` = observed count in a cell; `E` = count expected if the two variables were unrelated.
- `(O − E)²` — squared so that + and − deviations don't cancel.
- `÷ E` — a deviation of 10 out of an expected 20 is much more meaningful than 10 out of 10,000. Dividing standardises.
- `Σ` — sum over every cell. Bigger χ² = observed and expected disagree a lot = variables are associated.
- `df = (rows − 1) × (cols − 1)`.

### 6.6 Effect size: Cohen's d

$$d = \frac{\bar{x}_1 - \bar{x}_2}{s_{\text{pooled}}}$$

A **unit-free** version of the difference: "how many standard deviations apart are the groups?" Rules of thumb: 0.2 small, 0.5 medium, 0.8 large. Unlike p-values, _d_ doesn't grow just because you collected more data.

### 6.7 Confidence interval for a mean

$$\bar{x} \pm t^* \cdot \frac{s}{\sqrt{n}}$$

- `t*` = critical value from the t-distribution (≈ 2.0 for 95% with moderate n).
- The interval gives a **range of plausible values** for the true mean — far more informative than a yes/no p-value. If the interval contains μ₀, the two-tailed p-value will be > 0.05 (they always agree).

---

<a name="7-running-example"></a>

## 7. Hands-On in Python: The Running Example

**Scenario.** _BrewBuddy_, a coffee-delivery app, advertises "**30-minute average delivery**". You pull a random sample of **40** recent orders.

```python
# ============================================================
# 0. Setup — run this first
# ============================================================
import numpy as np                      # arrays + fast math (our simulated data)
import matplotlib.pyplot as plt         # plotting
from scipy import stats                 # statistical tests and distributions

np.random.seed(42)                      # freeze randomness so results are reproducible
plt.rcParams["figure.figsize"] = (10, 6)   # default size for every figure
plt.rcParams["axes.grid"] = True            # light grid lines help read values
plt.rcParams["grid.alpha"] = 0.3

print("numpy:", np.__version__, "| scipy:", stats.__name__)
```

**What each line does:**

- `np.random.seed(42)` — every "random" draw afterwards follows the same sequence, so you get _exactly_ the numbers printed in this tutorial.
- `plt.rcParams` — global styling so we don't repeat `grid=True, figsize=(10,6)` in every plot.
- The `print` confirms your environment loaded correctly.

```python
# ============================================================
# 1. The data: 40 delivery times (minutes)
# ============================================================
delivery_times = np.array([
    28.4, 33.1, 35.2, 27.9, 31.0, 36.5, 29.8, 34.4, 30.2, 32.7,
    26.8, 38.1, 31.9, 29.5, 33.8, 30.6, 35.9, 28.9, 32.2, 27.4,
    34.9, 31.3, 30.1, 36.0, 29.1, 33.5, 32.8, 28.2, 35.1, 30.9,
    31.7, 26.5, 37.2, 29.9, 34.0, 32.5, 30.4, 33.0, 28.7, 31.6
])
# Why a NumPy array and not a list? Arrays support .mean(), .std(),
# and vectorised math, which we need for every calculation below.

n      = len(delivery_times)              # sample size = 40
x_bar  = delivery_times.mean()            # sample mean  (~32.1 min)
s      = delivery_times.std(ddof=1)       # sample std dev; ddof=1 = "divide by n-1"
mu0    = 30.0                             # the advertised average (H0 value)
alpha  = 0.05                             # significance level we chose UP FRONT

print(f"n = {n}")
print(f"sample mean        = {x_bar:.3f} min")
print(f"sample std dev (s) = {s:.3f} min")
print(f"H0 hypothesised mu = {mu0} min")
print(f"observed gap       = {x_bar - mu0:+.3f} min")
```

**Why `ddof=1`?** `np.std` by default divides by _n_, giving the **population** standard deviation. With a sample, dividing by _n − 1_ gives an unbiased estimate — that is the _s_ in our t-formula. Forgetting this is a classic beginner bug.

```python
# ============================================================
# 2. Compute the t statistic by hand (then verify with scipy)
# ============================================================
se      = s / np.sqrt(n)                  # standard error of the mean
t_obs   = (x_bar - mu0) / se              # the test statistic
df      = n - 1                           # degrees of freedom

# Two-tailed p-value: 2 x area to the RIGHT of |t_obs| in a t-distribution
p_value = 2 * (1 - stats.t.cdf(abs(t_obs), df))

print(f"standard error (SE) = {se:.4f}")
print(f"t statistic         = {t_obs:.4f}")
print(f"degrees of freedom  = {df}")
print(f"p-value (two-tailed)= {p_value:.4f}")

# --- cross-check with scipy's ready-made test -------------------------------
t_scipy, p_scipy = stats.ttest_1samp(delivery_times, popmean=mu0)
print(f"\nscipy: t = {t_scipy:.4f}, p = {p_scipy:.4f}")
```

**Line-by-line:**

- `se = s / np.sqrt(n)` → 5.40 / √40 = **0.854**. This is the "typical wobble" of an average of 40 orders.
- `t_obs = (32.1 − 30) / 0.854` = **2.459**. Our sample mean sits ~2.46 standard errors above the advertised value.
- `stats.t.cdf(abs(t_obs), df)` → the area _below_ 2.459 in a t(39) curve. `1 −` that gives the right-tail area; `× 2` gives both tails.
- **Output ~ p = 0.0185.** In words: _if deliveries really averaged 30 minutes, only ~1.85% of random samples of 40 would average 32.1 minutes or more extreme._ Under our 0.05 rule → **reject H₀**.
- The scipy one-liner confirms the hand calculation — always a good habit for your first few tests.

**The confidence interval:**

```python
t_star  = stats.t.ppf(1 - alpha/2, df)     # critical value ~2.023 for df=39
ci_low  = x_bar - t_star * se
ci_high = x_bar + t_star * se
print(f"95% CI for true mean delivery time: [{ci_low:.2f}, {ci_high:.2f}] min")
# -> [30.37, 33.83]  — the whole interval is above 30, agreeing with p < 0.05
```

---

<a name="8-graph1"></a>

## 8. Graph 1: The Null Distribution and the P-Value Area

This single figure contains the entire logic of a p-value.

```python
# ============================================================
# Figure 1 — Null distribution, rejection region, and p-value
# ============================================================
z_obs = t_obs                    # we re-use our observed statistic (2.459)

x = np.linspace(-4, 4, 2000)                       # 2000 evenly spaced x-values
y = stats.norm.pdf(x, loc=0, scale=1)              # standard normal density

z_crit = stats.norm.ppf(1 - alpha/2)               # ~1.96, the critical value
p_two  = 2 * (1 - stats.norm.cdf(abs(z_obs)))      # the p-value again

fig, ax = plt.subplots()
ax.plot(x, y, color="navy", lw=2, label="Null distribution  N(0, 1)")

# --- the two rejection regions (5% of the total area, split 2.5% each) -------
ax.fill_between(x, y, where=(x <= -z_crit), color="red", alpha=0.30)
ax.fill_between(x, y, where=(x >=  z_crit), color="red", alpha=0.30,
                label=f"Rejection regions (total α = {alpha})")

# --- the p-value: everything at least as extreme as our result --------------
ax.fill_between(x, y, where=(x >=  z_obs), color="darkorange", alpha=0.60)
ax.fill_between(x, y, where=(x <= -z_obs), color="darkorange", alpha=0.60,
                label=f"p-value area = {p_two:.4f}")

ax.axvline( z_obs, color="darkorange", lw=2, ls="--")
ax.axvline(-z_obs, color="darkorange", lw=2, ls="--")

ax.annotate(f"observed\nz = {z_obs:.2f}", xy=(z_obs, 0.14),
            xytext=(z_obs + 0.35, 0.28),
            arrowprops=dict(arrowstyle="->", color="darkorange"), color="darkorange")

ax.set_title("Figure 1 — If H0 were true, where would our result fall?")
ax.set_xlabel("z-score  (standard errors from the null mean)")
ax.set_ylabel("Probability density")
ax.legend(loc="upper left", fontsize=9)
plt.tight_layout()
plt.savefig("fig1_null_distribution.png", dpi=150)
plt.show()
```

### How to read Figure 1

- **The navy bell curve** is the _sampling distribution under H₀_: what results look like if the average really is 30 minutes. Its peak at x = 0 is the most likely outcome (you measure exactly 30). The curve height is _density_ — probability per unit of x.
- **The red tails** are the **rejection regions**: the 5% of outcomes we've pre-declared "too unlikely to be luck". The left tail is 2.5% (deliveries suspiciously _fast_) and the right tail is 2.5% (_slow_) — that's the two-tailed split.
- **The orange tails** are the **p-value**: everything at or beyond ±2.459. Its area is 0.0185. Notice it is _smaller_ than the red region — that's the visual meaning of "p < α".
- **The dashed vertical lines** mark our observed statistic. Because they land _inside_ the red/orange zone, the test rejects H₀.
- **Key visual insight:** as the orange region expands toward the centre, the p-value grows. If our observed z had been 0.5, the orange area would cover nearly the whole curve — a huge p-value — and we would shrug.

---

<a name="9-graph2"></a>

## 9. Graph 2: One-Tailed vs Two-Tailed Tests

```python
# ============================================================
# Figure 2 — Where does the 5% go? One tail vs two tails
# ============================================================
x  = np.linspace(-4, 4, 2000)
y  = stats.norm.pdf(x)
zc2 = stats.norm.ppf(1 - alpha/2)     # 1.96 for two-tailed
zc1 = stats.norm.ppf(1 - alpha)       # 1.645 for one-tailed

fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)

# --- LEFT: two-tailed -------------------------------------------------------
axes[0].plot(x, y, color="navy", lw=2)
axes[0].fill_between(x, y, where=(x <= -zc2), color="red", alpha=0.35)
axes[0].fill_between(x, y, where=(x >=  zc2), color="red", alpha=0.35)
axes[0].axvline(zc2, color="black", ls=":")
axes[0].set_title(f"Two-tailed: α/2 = 2.5% in each tail\ncritical z = {zc2:.3f}")

# --- RIGHT: one-tailed (upper) ---------------------------------------------
axes[1].plot(x, y, color="navy", lw=2)
axes[1].fill_between(x, y, where=(x >= zc1), color="red", alpha=0.35)
axes[1].axvline(zc1, color="black", ls=":")
axes[1].set_title(f"One-tailed (greater): 5% in one tail\ncritical z = {zc1:.3f}")

for a in axes:
    a.set_xlabel("z-score")
axes[0].set_ylabel("Probability density")
plt.tight_layout()
plt.savefig("fig2_one_vs_two_tailed.png", dpi=150)
plt.show()
```

### The data points here

- Both panels use the **same total α = 5%**. The only difference is _distribution of the error budget_.
- In the right panel the boundary slides from 1.96 down to **1.645**, so a result of, say, z = 1.80 becomes significant. That's the one-tailed "advantage".
- The cost: a one-tailed test **cannot detect an effect in the opposite direction**. If the new feature _hurt_ conversion, a "greater than" test would call it "not significant" rather than "significantly bad" — dangerous in product decisions where harm matters as much as gain.
- **Business consequence:** guardrail metrics (revenue, churn, latency) should always be two-tailed, because you care about damage in both directions.

---

<a name="10-graph3"></a>

## 10. Graph 3: t-Distribution vs Normal Distribution

```python
# ============================================================
# Figure 3 — Why small samples need the t-distribution
# ============================================================
x = np.linspace(-4, 4, 1000)

fig, ax = plt.subplots()
for df_, colour in [(2, "tab:red"), (5, "tab:orange"), (30, "tab:green")]:
    ax.plot(x, stats.t.pdf(x, df_), color=colour, lw=2, label=f"t-distribution, df={df_}")
ax.plot(x, stats.norm.pdf(x), color="black", lw=2, ls="--", label="Standard normal (z)")

ax.fill_between(x, stats.t.pdf(x, 2), where=(x >= 2), color="tab:red", alpha=0.15)
ax.set_title("Figure 3 — Fatter tails with fewer data points (df = n − 1)")
ax.set_xlabel("Test statistic value")
ax.set_ylabel("Probability density")
ax.legend()
plt.tight_layout()
plt.savefig("fig3_t_vs_normal.png", dpi=150)
plt.show()

# A practical consequence: the same t = 2.0 gives different p-values
for d in [2, 5, 30, 1000]:
    print(f"df = {d:>5}:  p(two-tailed) for t=2.0 is "
          f"{2*(1-stats.t.cdf(2.0, d)):.4f}")
```

### What to notice

- **The curves are all centred at 0** with the same bell shape — they differ only in **tail thickness**.
- **df = 2 (red)** has very heavy tails: with only 3 data points, extreme values are common, so we demand more evidence. At t = 2.0 with df = 2, p ≈ 0.18 → not significant. With df = 1000, that same t = 2.0 gives p ≈ 0.046 → significant.
- **df = 30 (green) already hugs the black dashed normal curve** almost exactly. This is the famous "n ≥ 30" rule of thumb: beyond that, t and z are nearly identical.
- **Business consequence:** never run a t-test on 4 users and celebrate p = 0.04. The t-distribution is already punishing you, but the estimate is still fragile — check the confidence interval width too.

---

<a name="11-graph4"></a>

## 11. Graph 4: How Sample Size Changes the P-Value

This is the single most important figure for avoiding bad business decisions.

```python
# ============================================================
# Figure 4 — Same effect, more data, smaller p
# ============================================================
observed_effect = 1.5          # our sample mean is 1.5 min above the null
sigma           = 5.0          # per-order standard deviation (the noise)
n_grid          = np.arange(5, 1005, 5)
se_grid         = sigma / np.sqrt(n_grid)
t_grid          = observed_effect / se_grid
p_grid          = 2 * (1 - stats.t.cdf(np.abs(t_grid), df=n_grid - 1))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: standard error shrinks like 1/sqrt(n)
axes[0].plot(n_grid, se_grid, color="teal", lw=2)
axes[0].set_title("Left — Noise falls as 1/√n (law of diminishing returns)")
axes[0].set_xlabel("Sample size (n)")
axes[0].set_ylabel("Standard error = σ/√n")

# Right: p-value collapses with n
axes[1].plot(n_grid, p_grid, color="purple", lw=2)
axes[1].axhline(alpha, color="red", ls="--", label="α = 0.05")
n_needed = n_grid[np.argmax(p_grid < alpha)]
axes[1].axvline(n_needed, color="grey", ls=":", label=f"significant from n ≈ {n_needed}")
axes[1].set_ylim(0, 1)
axes[1].set_title("Right — Same 1.5-min effect, ever-smaller p-value")
axes[1].set_xlabel("Sample size (n)")
axes[1].set_ylabel("p-value (two-tailed)")
axes[1].legend()

plt.tight_layout()
plt.savefig("fig4_sample_size_effect.png", dpi=150)
plt.show()
```

### Reading the two panels

- **Left panel (teal curve).** Each dot is the standard error you'd get at that sample size. It drops steeply at first and then flattens — going from n = 5 to n = 50 cuts noise by ~68%, but from n = 500 to n = 1000 only by ~29%. Doubling your sample _never_ halves your p-value; it divides the SE by √2.
- **Right panel (purple curve).** The effect is **identical (1.5 minutes)** at every point on the x-axis. Yet the p-value sweeps from ≈1.0 (n = 5, no idea) through 0.05 around n ≈ 130 and approaches 0 as n grows.
- **The grey dotted line** shows where significance is reached. Before it: "we can't tell". After it: "we're confident the effect is real".
- **The red dashed line** is α. The crossing point is the p-value's only yes/no behaviour.
- **⚠️ The trap:** because p shrinks with n even when the effect is trivial, "p < 0.05" alone tells you _nothing_ about whether the change is worth shipping. A 1.5-minute delivery delay is significant at n = 100,000 and still might be operationally irrelevant. **Always pair p with effect size and cost/benefit.**

---

<a name="12-graph5"></a>

## 12. Graph 5: Type I/II Errors and Statistical Power

```python
# ============================================================
# Figure 5 — Two worlds: H0 true vs H1 true, and what we can detect
# ============================================================
x       = np.linspace(-5, 7, 2000)
mu_alt  = 2.0                    # true effect, in standard-error units
z_crit  = stats.norm.ppf(1 - alpha)   # 1.645 (one-tailed for a cleaner picture)

h0 = stats.norm.pdf(x, 0, 1)          # world where H0 holds
h1 = stats.norm.pdf(x, mu_alt, 1)     # world where H1 holds

power  = 1 - stats.norm.cdf(z_crit - mu_alt)      # area of h1 right of crit
beta   = stats.norm.cdf(z_crit - mu_alt)          # area of h1 left of crit

fig, ax = plt.subplots()
ax.plot(x, h0, color="navy",  lw=2, label="H0 true (no effect)")
ax.plot(x, h1, color="green", lw=2, label="H1 true (real effect)")

# alpha: false positive — H0 world, right of the critical value
ax.fill_between(x, h0, where=(x >= z_crit), color="red",   alpha=0.45,
                label=f"α = {alpha}  (false positive)")
# beta: false negative — H1 world, left of the critical value
ax.fill_between(x, h1, where=(x <= z_crit), color="orange", alpha=0.45,
                label=f"β = {beta:.2f}  (missed effect)")
# power: H1 world, right of the critical value
ax.fill_between(x, h1, where=(x >= z_crit), color="green",  alpha=0.30,
                label=f"Power = {power:.2f}  (correctly detect)")

ax.axvline(z_crit, color="black", ls="--", lw=1.5)
ax.text(z_crit + 0.05, 0.30, "decision threshold", rotation=90, fontsize=9)
ax.set_title("Figure 5 — The four outcomes of a hypothesis test")
ax.set_xlabel("Test statistic")
ax.set_ylabel("Probability density")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("fig5_power.png", dpi=150)
plt.show()
```

### Decoding the colours

- **Navy curve** = the world where the null is true. **Red sliver** = the 5% of that world where we'd wrongly declare a winner → **Type I error (α)**. This is a "false alarm": we ship a feature that does nothing.
- **Green curve** = the world where the new feature genuinely works (effect size = 2 standard errors). It's shifted right.
- **Orange area** = the part of the green world that falls _left_ of the threshold → **Type II error (β)**. Here we'd miss a real improvement. In a business, that's a missed opportunity: the better variant is declared a loser.
- **Green shaded area** = **power** = 1 − β ≈ 0.65 in this example. Only a 65% chance of catching the effect. The standard target is 80%, which requires either a bigger sample or a bigger effect.
- **The dashed line** is the decision threshold. Everything hinges on it: move it left and you gain power but also gain false positives. You can't escape the trade-off — you can only budget it.
- **How the graph shifts:** increasing n narrows _both_ bumps (they become spikier), pushing them apart and shrinking the overlap — that's how you buy power. Increasing the true effect moves the green curve right — power rises. Changing α slides the threshold.

---

<a name="13-graph6"></a>

## 13. Graph 6: A/B Test — Two-Proportion z-Test

**Scenario.** _BrewBuddy_ tests a redesigned "Checkout" button. 1,000 users see the control, 1,000 see the variant.

```python
# ============================================================
# 6.1 The A/B test numbers
# ============================================================
n_control, conv_control = 1000, 92      # old button
n_variant, conv_variant = 1000, 125     # new button

p_control = conv_control / n_control    # 0.092  (9.2%)
p_variant = conv_variant / n_variant    # 0.125  (12.5%)
lift_abs  = p_variant - p_control       # +0.033 = +3.3 percentage points
lift_rel  = lift_abs / p_control        # +0.359 = +35.9% relative lift

# --- pooled proportion: what the rate would be if H0 were true --------------
p_pool = (conv_control + conv_variant) / (n_control + n_variant)

# --- two-proportion z-test -------------------------------------------------
se_diff = np.sqrt(p_pool * (1 - p_pool) * (1/n_control + 1/n_variant))
z_ab    = (p_variant - p_control) / se_diff
p_ab    = 2 * (1 - stats.norm.cdf(abs(z_ab)))

print(f"control rate : {p_control:.3%}")
print(f"variant rate : {p_variant:.3%}")
print(f"absolute lift: {lift_abs:+.3%}   relative lift: {lift_rel:+.1%}")
print(f"pooled rate  : {p_pool:.4f}")
print(f"SE of diff   : {se_diff:.5f}")
print(f"z statistic  : {z_ab:.4f}")
print(f"p-value      : {p_ab:.4f}")

# --- 95% CI for the difference (UNPOOLED SE - the correct choice for a CI) --
se_unpooled = np.sqrt(p_control*(1-p_control)/n_control
                      + p_variant*(1-p_variant)/n_variant)
z_star = stats.norm.ppf(1 - alpha/2)
ci = (lift_abs - z_star*se_unpooled, lift_abs + z_star*se_unpooled)
print(f"95% CI for lift: [{ci[0]:+.3%}, {ci[1]:+.3%}]")
```

**Interpreting each output:**

- `p_pool = 0.1085` — if the button made no difference, both groups share one true rate: 217 conversions out of 2,000 users.
- `se_diff = 0.0139` — the typical random wobble in a difference of two rates with ~1,000 users each is about **1.4 percentage points**.
- `z_ab = 2.373` — our observed 3.3-point lift is 2.37 standard errors from zero.
- `p_ab ≈ 0.0177` — under H₀, only ~1.8% of experiments would produce a gap this large. **Reject H₀: the new button works.**
- **CI ≈ [+0.6 pp, +6.0 pp]** — even the pessimistic end is positive, so the improvement is credible. Reporting _this range_ is far more useful to a product manager than "p < 0.05".

**Note on two different standard errors:** we use the **pooled** SE when computing the _test statistic_ (because H₀ says the rates are equal) and the **unpooled** SE when building the _confidence interval_ (because we no longer assume equality). Mixing them up is a common, subtle error.

**Shortcut with statsmodels:**

```python
# from statsmodels.stats.proportion import proportions_ztest
# counts = np.array([conv_variant, conv_control])
# nobs   = np.array([n_variant,  n_control])
# z, p   = proportions_ztest(counts, nobs, alternative="two-sided")
```

### Figure 6: visualising the A/B test

```python
# ============================================================
# Figure 6 — A/B test: two views of the same result
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

# --- LEFT: bar chart with 95% confidence intervals -------------------------
groups = ["Control\n(old button)", "Variant\n(new button)"]
rates  = [p_control, p_variant]
errs   = [z_star*np.sqrt(p*(1-p)/n) for p, n in
          [(p_control, n_control), (p_variant, n_variant)]]

bars = axes[0].bar(groups, rates, yerr=errs, capsize=8,
                   color=["silver", "steelblue"], edgecolor="black")
axes[0].set_ylabel("Conversion rate")
axes[0].set_title("Left — Conversion rate with 95% CI error bars")
for bar, r in zip(bars, rates):
    axes[0].text(bar.get_x() + bar.get_width()/2, r + 0.006,
                 f"{r:.2%}", ha="center", fontweight="bold")
axes[0].set_ylim(0, 0.16)

# --- RIGHT: null distribution of the difference ----------------------------
d  = np.linspace(-0.06, 0.06, 2000)
yd = stats.norm.pdf(d, 0, se_diff)
axes[1].plot(d, yd, color="navy", lw=2, label="H0: difference = 0")
axes[1].fill_between(d, yd, where=(d >= abs(lift_abs)), color="darkorange", alpha=0.6)
axes[1].fill_between(d, yd, where=(d <= -abs(lift_abs)), color="darkorange", alpha=0.6,
                     label=f"p-value area = {p_ab:.4f}")
axes[1].axvline(lift_abs, color="darkorange", lw=2, ls="--")
axes[1].annotate(f"observed lift\n{lift_abs:+.2%}",
                 xy=(lift_abs, 12), xytext=(lift_abs + 0.012, 22),
                 arrowprops=dict(arrowstyle="->", color="darkorange"),
                 color="darkorange")
axes[1].set_title("Right — Observed lift vs the 'no difference' world")
axes[1].set_xlabel("Difference in conversion rate (variant − control)")
axes[1].set_ylabel("Probability density")
axes[1].legend()
axes[1].set_xlim(-0.06, 0.06)

plt.tight_layout()
plt.savefig("fig6_ab_test.png", dpi=150)
plt.show()
```

### Reading Figure 6

- **Left panel.** Each bar's height is the observed conversion rate. The **error bar** is the 95% confidence interval: a plausible range for that group's _true_ rate. The two error bars overlap somewhat — which is exactly why we need a formal test rather than eyeballing. Note that overlapping CIs do **not** automatically mean "not significant"; the correct comparison is the CI of the _difference_.
- **Right panel.** The navy curve is the H₀ world: a normal distribution centred on **zero difference**, with a width set by `se_diff`. The orange area is the p-value — the probability of a gap as large as ±3.3 points (or larger) if nothing had changed. It is small (1.8%), and the dashed line at +3.3% sits far out in the right tail. **Verdict: ship it.**
- The distribution on the right is centred at 0, **not** at the observed lift — a subtle but crucial point. The picture answers "where would my result sit if H₀ were true?", not "where is the truth likely to be?" (that's the CI's job).

---

<a name="14-graph7"></a>

## 14. Graph 7: Permutation Test (an Assumption-Free Alternative)

If the t-test formulas feel magical, this technique makes the logic concrete by **simulating** the null world directly.

**Idea:** if H₀ is true, group labels (control/variant) are meaningless. So shuffle the labels thousands of times, recompute the difference each time, and see how often random labelling produces a gap as big as the real one.

```python
# ============================================================
# 7. Permutation test on the A/B data — no formulas required
# ============================================================
control = np.array([1]*conv_control + [0]*(n_control - conv_control))
variant = np.array([1]*conv_variant + [0]*(n_variant - conv_variant))
obs_diff = variant.mean() - control.mean()          # +0.033

pooled = np.concatenate([control, variant])         # forget which group is which

n_perm = 5000
perm_diffs = np.empty(n_perm)
for i in range(n_perm):
    shuffled = np.random.permutation(pooled)        # randomly reassign labels
    perm_diffs[i] = shuffled[:n_control].mean() - shuffled[n_control:].mean()

p_perm = np.mean(np.abs(perm_diffs) >= abs(obs_diff))
print(f"observed difference : {obs_diff:+.4f}")
print(f"permutation p-value : {p_perm:.4f}")
```

**Line-by-line:**

- `[1]*92 + [0]*908` builds an array of 1s (converted) and 0s (not) — the raw outcomes, no rates needed.
- `np.random.permutation(pooled)` destroys any real relationship between user and group. Any difference that survives is pure luck.
- `np.abs(perm_diffs) >= np.abs(obs_diff)` counts how often luck produced something as extreme as our real result, in _either_ direction (two-tailed by symmetry).
- The mean of that boolean array **is** the p-value. You'll get ≈ 0.018 — very close to the formula-based 0.0177.

**Why beginners should love this:** it assumes almost nothing (no normality, no equal variances), works for medians, revenue-per-user, or any weird metric, and the mechanics are visible.

```python
# ============================================================
# Figure 7 — The permutation null distribution
# ============================================================
fig, ax = plt.subplots()
ax.hist(perm_diffs, bins=50, color="lightsteelblue", edgecolor="white",
        label="Null distribution from 5,000 shuffles")
ax.axvline(obs_diff,  color="darkorange", lw=2.5, ls="--",
           label=f"observed difference = {obs_diff:+.3%}")
ax.axvline(-obs_diff, color="darkorange", lw=2.5, ls="--")
ax.set_title("Figure 7 — Where our real result falls in a world of pure randomness")
ax.set_xlabel("Difference in conversion rate after shuffling labels")
ax.set_ylabel("Number of shuffles")
ax.legend()
plt.tight_layout()
plt.savefig("fig7_permutation.png", dpi=150)
plt.show()
```

**Reading Figure 7:** the histogram is centred on 0 (as it must be — shuffling wipes out any real effect) and is roughly bell-shaped, which is why the z-formula worked so well. The two dashed orange lines are our observed ±3.3% gap. The **p-value is the fraction of histogram bars beyond those lines** — visibly tiny. Because the histogram's shape is generated empirically rather than assumed, this graph doubles as a check that the normality assumption was reasonable.

---

<a name="15-graph8"></a>

## 15. Graph 8: Multiple Testing and False Discoveries

**The problem.** Run 20 independent A/B tests where nothing works. Each has a 5% chance of a false positive. The chance of at least one false "winner" is:

$$P(\text{at least one false positive}) = 1 - (1-\alpha)^m = 1 - 0.95^{20} \approx 64\%$$

Nearly two-thirds of the time, you ship a dud. This is the **multiple comparisons** problem.

```python
# ============================================================
# 8. Multiple testing: 20 experiments, all truly null
# ============================================================
np.random.seed(7)
m = 20
p_values = np.sort(np.random.uniform(0, 1, m))     # uniform under the global null

# --- Bonferroni: divide alpha by the number of tests -----------------------
alpha_bonf = alpha / m
sig_bonf   = p_values < alpha_bonf

# --- Benjamini-Hochberg (FDR control) --------------------------------------
rank  = np.arange(1, m + 1)                        # 1, 2, 3, ... 20
bh_threshold = alpha * rank / m                    # the BH critical line
below  = p_values <= bh_threshold
k      = np.max(np.where(below)[0] + 1) if below.any() else 0
sig_bh = rank <= k

print("sorted p-values:", np.round(p_values, 3))
print(f"Bonferroni threshold : {alpha_bonf:.4f}  -> {sig_bonf.sum()} significant")
print(f"BH: largest rank with p <= q*i/m is {k} -> {k} significant")
```

**The two corrections:**

- **Bonferroni:** require each p < α/m. Simple, very strict, controls the chance of _any_ false positive. With m = 20 the threshold is 0.0025 — brutal, and it kills real effects too.
- **Benjamini–Hochberg:** controls the **False Discovery Rate** — the expected _proportion_ of your declared discoveries that are wrong. More powerful and the usual choice when you're screening many features/metrics. The rule: sort p-values ascending, find the largest rank `i` where `p₍ᵢ₎ ≤ (i/m)·q`, declare all ranks ≤ i significant.

```python
# ============================================================
# Figure 8 — Sorted p-values against the BH threshold line
# ============================================================
fig, ax = plt.subplots()
ax.scatter(rank, p_values, color="steelblue", zorder=3, label="Sorted p-values")
ax.plot(rank, bh_threshold, color="red", lw=2, label=f"BH threshold line (q={alpha})")
ax.axhline(alpha, color="grey", ls=":", label=f"Naive α = {alpha} (ignores multiplicity)")

for i in rank[sig_bh]:
    ax.scatter(i, p_values[i-1], color="green", s=90, zorder=4)

ax.set_title("Figure 8 — Benjamini–Hochberg: which discoveries survive multiplicity?")
ax.set_xlabel("Rank of the p-value (smallest to largest)")
ax.set_ylabel("p-value")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("fig8_multiple_testing.png", dpi=150)
plt.show()
```

**Reading Figure 8:**

- **Blue dots** are your p-values sorted from smallest to largest. Under the global null they lie roughly on a diagonal from bottom-left to top-right.
- **The red line** is the BH threshold: it rises linearly from α/m to α. Because it starts very low and ends at α, it is strict about small discoveries but allows the largest p-values a fair chance.
- **Green dots** are the discoveries: ranks where the blue dot sits _below_ the red line. Everything after the last crossing is declared null.
- **The grey dotted line** shows the naive approach: "any p < 0.05 counts". Comparing the grey line with the red line shows exactly how much multiplicity protection costs you — and why the flat 0.05 rule is misleading when you're testing 20 metrics at once.

**Business rule:** if you have more than ~3 concurrent tests, use FDR/Bonferroni, or pre-register one primary metric with the rest as secondary/exploratory.

---

<a name="16-chi-square"></a>

## 16. Chi-Square Test: Categorical Data

Not every metric is an average. Sometimes you're counting categories.

**Scenario.** BrewBuddy compares **Standard** vs **Express** shipping on product **returns**.

```python
# ============================================================
# 9. Chi-square test of independence
# ============================================================
# rows = shipping speed, columns = [Returned, Kept]
observed = np.array([[120, 880],     # Standard shipping
                     [ 80, 920]])    # Express shipping

chi2, p_chi, dof, expected = stats.chi2_contingency(observed)

print("Observed counts:\n", observed)
print("\nExpected counts if shipping and returns were unrelated:\n",
      np.round(expected, 1))
print(f"\nchi-square = {chi2:.4f}")
print(f"degrees of freedom = {dof}")
print(f"p-value = {p_chi:.4f}")

# --- effect size for a 2x2 table: Cramer's V -------------------------------
n_total  = observed.sum()
cramers_v = np.sqrt(chi2 / (n_total * (min(observed.shape) - 1)))
print(f"Cramer's V = {cramers_v:.4f}")
```

**What the numbers mean:**

- Row totals are 1,000 each; the return column totals 200. So if shipping speed had _nothing_ to do with returns, each row should return `1000 × 200 / 2000 = 100` items. That's the `expected` matrix.
- Standard shipping actually returned **120** (20 above expectation) and Express returned **80** (20 below).
- `χ² = (120−100)²/100 + (80−100)²/100 + (880−900)²/900 + (920−900)²/900` = 4 + 4 + 0.44 + 0.44 ≈ **8.9**.
- `df = (2−1)(2−1) = 1`. The p-value ≈ **0.0029** → **strong evidence that return rates differ by shipping speed.**
- **Cramér's V** ≈ 0.067 — a _small_ association. So: statistically real, but modest in size. The business question becomes "is the cost of Express worth a 4-percentage-point reduction in returns?" — not "is it significant?"

```python
# ============================================================
# Figure 9 — Observed vs expected: the visual version of chi-square
# ============================================================
labels = ["Standard shipping", "Express shipping"]
x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots()
ax.bar(x - width/2, observed[:, 0], width, label="Observed returns",   color="indianred")
ax.bar(x + width/2, expected[:, 0], width, label="Expected returns (if independent)",
       color="lightgrey", edgecolor="black")

for i in range(len(labels)):
    diff = observed[i, 0] - expected[i, 0]
    ax.annotate(f"{diff:+.0f}", xy=(i, max(observed[i,0], expected[i,0]) + 4),
                ha="center", color="darkred" if diff > 0 else "darkgreen", fontweight="bold")

ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel("Number of returned orders")
ax.set_title(f"Figure 9 — More returns than expected under Standard shipping (χ²={chi2:.2f}, p={p_chi:.4f})")
ax.legend()
plt.tight_layout()
plt.savefig("fig9_chi_square.png", dpi=150)
plt.show()
```

**Reading Figure 9:** the red bars are what actually happened; the grey bars are what we'd expect if the two variables were unrelated. The **gap between them** is what χ² measures — and each gap is squared and divided by the expectation before summing. Positive annotations (red) mean "more returns than expected"; negative (green) means "fewer". This bar-pair view works for any contingency table and is much easier to explain in a meeting than a χ² value.

---

<a name="17-ci-effect-size"></a>

## 17. Confidence Intervals and Effect Size (the "so what?")

A p-value answers _"Is there an effect?"_ An effect size answers _"How big is it?"_, and a CI answers _"How precisely do we know?"_ You need all three.

```python
# ============================================================
# 10. Effect size (Cohen's d) + a full reporting template
# ============================================================
def cohens_d(a, b):
    """Standardised difference between two independent samples."""
    n1, n2   = len(a), len(b)
    s_pooled = np.sqrt(((n1-1)*a.std(ddof=1)**2 + (n2-1)*b.std(ddof=1)**2) / (n1+n2-2))
    return (a.mean() - b.mean()) / s_pooled

control_times = np.array([31.2, 30.8, 29.9, 32.4, 31.7, 30.1, 33.0, 29.4, 31.5, 30.6])
variant_times = np.array([28.9, 27.6, 29.4, 28.1, 27.9, 29.8, 28.4, 27.2, 29.1, 28.6])

t_stat, p_val = stats.ttest_ind(variant_times, control_times, equal_var=False)
d = cohens_d(variant_times, control_times)

# CI for the difference in means
diff = variant_times.mean() - control_times.mean()
se_d = np.sqrt(variant_times.var(ddof=1)/len(variant_times)
               + control_times.var(ddof=1)/len(control_times))
df_w = len(variant_times) + len(control_times) - 2
t_c  = stats.t.ppf(1 - alpha/2, df_w)
ci_d = (diff - t_c*se_d, diff + t_c*se_d)

print(f"Control mean : {control_times.mean():.2f} min")
print(f"Variant mean : {variant_times.mean():.2f} min")
print(f"Difference   : {diff:+.2f} min   95% CI [{ci_d[0]:.2f}, {ci_d[1]:.2f}]")
print(f"t = {t_stat:.3f},  p = {p_val:.4f}")
print(f"Cohen's d = {d:.2f}")
```

**How to label `d`:** |d| < 0.2 negligible · 0.2–0.5 small · 0.5–0.8 medium · > 0.8 large.

**Full reporting template** (use this in your write-ups):

> The new routing algorithm reduced mean delivery time from **31.2 min** to **28.6 min**, a difference of **−2.6 min (95% CI: −3.8 to −1.4)**. This was statistically significant, _t_(17.6) = −4.42, _p_ < 0.001, with a **large effect size (Cohen's d = 1.4)**. Given ~12,000 daily orders, this implies roughly **520 saved delivery-minutes per day**.

Notice how the last sentence converts statistics into **business value** — that is what gets decisions made.

---

<a name="18-assumptions"></a>

## 18. Assumption Checks

Every test silently assumes something. Check the important ones.

```python
# ============================================================
# 11. Assumption checks
# ============================================================
# (a) Normality of a small sample -> Shapiro-Wilk; visually -> Q-Q plot
shapiro_stat, shapiro_p = stats.shapiro(delivery_times)
print(f"Shapiro-Wilk normality: W = {shapiro_stat:.4f}, p = {shapiro_p:.4f}")
print("  -> p > 0.05 means: no evidence against normality (good for a t-test)")

# (b) Equal variances between two groups -> Levene's test
lev_stat, lev_p = stats.levene(control_times, variant_times)
print(f"Levene equal-variance:  W = {lev_stat:.4f}, p = {lev_p:.4f}")
print("  -> p < 0.05 means variances differ: use equal_var=False (Welch)")

# (c) Q-Q plot: do the points hug the red line?
fig, ax = plt.subplots(figsize=(6.5, 6))
stats.probplot(delivery_times, dist="norm", plot=ax)
ax.set_title("Figure 10 — Q-Q plot: points on the red line ⇔ normal data")
plt.tight_layout()
plt.savefig("fig10_qq_plot.png", dpi=150)
plt.show()
```

### Reading the Q-Q plot

- Each **blue dot** is one data point, plotted at (what a normal distribution predicts for its rank) versus (its actual value).
- The **red line** is perfect normality.
- Points hugging the line → the normality assumption is fine. Points curving away at the ends (**fat tails**) or bending in an S-shape (**skewness**) → plain t-tests are shaky. Remedies: use a **permutation test**, a **Mann-Whitney U** test (`stats.mannwhitneyu`), or analyse a transformed metric (e.g. log of revenue).
- **Important:** with large n (> 100 per group), the **Central Limit Theorem** makes t-tests robust to non-normality. The Q-Q plot matters most for _small_ samples.

**Other assumptions to keep in mind:**

- **Independence** — one user must appear in only one group, and observations must not influence each other. No test can detect this; it's a design issue.
- **Random assignment / random sampling** — the foundation of every p-value. A biased sample makes p meaningless.
- **Correct test for the data type** — counts → chi-square; means → t; rates → proportions z.

---

<a name="19-use-cases"></a>

## 19. Company Use Cases

### 19.1 E-commerce — A/B testing the checkout flow

- **Metric:** conversion rate. **Test:** two-proportion z-test (Section 13).
- **Decision rule:** ship if p < 0.05 **and** the CI's lower bound exceeds the +1 pp minimum detectable effect **and** guardrails (page load time, refund rate) show no regression.
- **Business value:** a +3.3 pp lift on 5M monthly sessions at $40 AOV ≈ **$6.6M extra monthly revenue** — the p-value is just the gate; the dollar figure is the argument.

### 19.2 SaaS — did the new onboarding reduce churn?

- **Metric:** 90-day churn rate. **Test:** two-proportion z-test, or **chi-square** on a cohort × churned/retained table.
- **Extra care:** run a **power analysis first**. Detecting a drop from 5% to 4.2% churn with 80% power needs tens of thousands of users per arm — worth knowing before you start, not after.
- **Business value:** 0.8 pp churn reduction on a 50k-user base at $30/month ≈ **$144k of retained annual revenue**, and it compounds because retained users expand.

### 19.3 Marketing — subject line and send-time tests

- **Metric:** open rate, click-through rate. **Test:** chi-square on the open/not-open × subject-line-A/B table (data is categorical, not continuous).
- **Multiplicity warning:** email teams often test 4–8 variants per send. Apply **Benjamini–Hochberg** or accept that one "winner" is probably noise.

### 19.4 Manufacturing / operations — quality control

- **Metric:** fill volume, tensile strength, defect rate. **Test:** one-sample t-test against the engineering spec, or a two-sample t-test comparing machine A vs machine B.
- **Business value:** if a line's mean fill is significantly _below_ spec, the company is giving away product; if significantly _above_, it may be violating labelling laws. Both are costly, and a **one-tailed** test in each direction is justified here because the spec has a hard bound.
- **Bonus:** Statistical Process Control (SPC) charts are hypothesis tests run continuously.

### 19.5 Product & Engineering — performance regression testing

- **Metric:** p95 API latency, bundle size. **Test:** Welch's two-sample t-test between the pre-release and post-release builds (or a permutation test, because latency is heavily right-skewed).
- **Business value:** catches a 50 ms regression before it costs conversion. Note that _statistical_ significance here is cheap with enough traffic — anchor the threshold to a **practical** significance level (e.g. "only alert if p95 worsens by >20 ms").

### 19.6 Finance & risk — fraud model evaluation

- **Question:** Is the fraud feature that flags "5+ transactions in 1 hour" actually informative, or did it fire by chance?
- **Test:** chi-square between the flag and confirmed fraud; or compare mean loss per flagged vs unflagged account with a t-test / Mann-Whitney.
- **Extra care:** fraud data is extremely imbalanced and autocorrelated, so p-values from naive tests are optimistic. Use **time-based backtests** and permutation tests that respect the time structure.

### 19.7 People analytics — pay and promotion equity

- **Question:** Are promotion rates equal across departments or demographic groups?
- **Test:** chi-square on promotion × group; two-proportion z-test for pairwise comparisons with **FDR correction**.
- **Responsible-use warning:** statistical significance is not proof of discrimination (there are always confounders like tenure and role), and non-significance is not proof of fairness (small samples lack power). Report effect sizes with CIs and be transparent about uncertainty.

### 19.8 Pharma / clinical trials

- **The strictest setting:** α, primary endpoint, sample size, and analysis plan are **pre-registered** with regulators. A p < 0.05 on a single pre-specified endpoint is the legal bar for efficacy; secondary endpoints and subgroup analyses are hypothesis-generating only.
- **Lesson for everyone else:** the greatest p-hacking risk is _choosing the hypothesis after seeing the data_. Pick your metric first.

### Summary table

| Domain        | Typical metric            | Recommended test                  |
| ------------- | ------------------------- | --------------------------------- |
| E-commerce    | Conversion rate           | Two-proportion z-test             |
| SaaS          | Churn / retention rate    | Two-proportion z-test, chi-square |
| Marketing     | Open / click rate         | Chi-square                        |
| Manufacturing | Mean measurement vs spec  | One-sample t-test                 |
| Product/Eng   | Latency, revenue per user | Welch's t-test, permutation test  |
| Finance       | Fraud flag vs outcome     | Chi-square, Mann-Whitney          |
| HR            | Promotion rate by group   | Chi-square + FDR correction       |
| Clinical      | Endpoint mean difference  | Pre-registered t-test / ANOVA     |

---

<a name="20-pitfalls"></a>

## 20. Common Pitfalls

1. **P-hacking / data dredging.** Testing 30 metrics and reporting the one that hit p = 0.04. Fix: pre-register the primary metric; correct for multiplicity.
2. **Peeking / early stopping.** Checking your A/B test every day and stopping when p < 0.05 inflates false positives to 20–30%. Fix: fix the duration in advance, or use sequential testing / alpha-spending methods.
3. **Confusing significance with importance.** With n = 1,000,000, a 0.01 pp lift is "significant" and worthless. Always ask "what's the minimum effect worth acting on?"
4. **Ignoring the confidence interval.** A p-value of 0.049 and a p-value of 0.0001 are not equally convincing — the CI shows you the difference.
5. **Absence of evidence ≠ evidence of absence.** p = 0.30 with n = 50 often means "we don't have enough data", not "there's no effect". Report power.
6. **Wrong test for the data.** t-tests on counts, chi-square on tiny expected counts (< 5 per cell), correlation on nonlinear data.
7. **Assuming independence.** Repeated measurements on the same user, or clustered data (all users from one city), require mixed models or cluster-robust SEs.
8. **Simpson's paradox.** A trend that holds in every subgroup can reverse when pooled — always segment before concluding.
9. **Multiple comparisons in subgroups.** "It works for users aged 25–34!" said after slicing 12 ways. That's a hypothesis, not a finding — confirm it with a fresh test.
10. **Ignoring that the world moved.** Novelty effects, seasonality, and outages can masquerade as treatment effects. Compare against historical baselines.

---

<a name="21-cheat-sheet"></a>

## 21. Decision Cheat Sheet & Glossary

### Which test should I use?

| Your data / question                | Test                           | Python                                   |
| ----------------------------------- | ------------------------------ | ---------------------------------------- |
| One sample mean vs a target         | One-sample t-test              | `stats.ttest_1samp(x, popmean)`          |
| Two independent group means         | Welch's t-test                 | `stats.ttest_ind(a, b, equal_var=False)` |
| Same subjects, before/after         | Paired t-test                  | `stats.ttest_rel(before, after)`         |
| Two conversion rates                | Two-proportion z-test          | `proportions_ztest(...)` or formula      |
| Two categorical variables           | Chi-square independence        | `stats.chi2_contingency(table)`          |
| Three or more group means           | One-way ANOVA                  | `stats.f_oneway(g1, g2, g3)`             |
| Association between two numbers     | Pearson / Spearman correlation | `stats.pearsonr(x, y)`                   |
| Ordinal data / non-normal, 2 groups | Mann-Whitney U                 | `stats.mannwhitneyu(a, b)`               |
| Any metric, no assumptions          | Permutation test               | Section 14                               |
| Many tests at once                  | FDR correction                 | Section 15                               |

### The 8-step workflow

1. **State the business question** in one sentence.
2. **Choose the metric** and the minimum effect worth acting on.
3. **Write H₀ and H₁** (two-tailed by default).
4. **Pick α** (usually 0.05) and compute the **required sample size** for 80% power.
5. **Collect data** with random assignment; don't peek.
6. **Check assumptions** (normality for small n, equal variances, independence).
7. **Run the test**; record the statistic, df, p-value, **effect size, and CI**.
8. **Decide and communicate** in business terms — money, minutes, users — not just p-values.

### Glossary

| Term                    | Meaning                                                            |
| ----------------------- | ------------------------------------------------------------------ |
| **H₀ / H₁**             | Null and alternative hypotheses                                    |
| **Test statistic**      | Standardised measure of how far data is from H₀ (t, z, χ², F)      |
| **Standard error (SE)** | Standard deviation of an estimate; `σ/√n` for a mean               |
| **p-value**             | P(result this extreme \| H₀ true)                                  |
| **α**                   | False-positive tolerance you choose in advance                     |
| **Type I error**        | Rejecting a true H₀ (false alarm)                                  |
| **Type II error (β)**   | Failing to reject a false H₀ (missed effect)                       |
| **Power (1 − β)**       | Probability of detecting a real effect                             |
| **df**                  | Degrees of freedom; for one-sample t, n − 1                        |
| **Effect size**         | Standardised magnitude of the effect (e.g. Cohen's d)              |
| **CI**                  | Range of plausible values for the true parameter                   |
| **FDR**                 | False Discovery Rate — share of "discoveries" expected to be wrong |

---

### Final takeaway

A p-value is a single, narrow sentence: _"How surprising is my data if nothing is going on?"_ It is powerful, but it is only one of three numbers you need. **Always report the p-value, the effect size, and the confidence interval** — and then translate them into the only language your stakeholders speak: _users, minutes, and money._

```python
# Save your own results as a tidy table for the report
import pandas as pd
results = pd.DataFrame({
    "test":       ["BrewBuddy delivery time", "Checkout A/B", "Shipping vs returns"],
    "statistic":  [round(t_obs, 3), round(z_ab, 3), round(chi2, 3)],
    "p_value":    [round(p_value, 4), round(p_ab, 4), round(p_chi, 4)],
    "effect":     [f"{x_bar - mu0:+.2f} min", f"{lift_abs:+.2%}", f"Cramer's V={cramers_v:.3f}"],
    "decision":   ["Reject H0", "Reject H0", "Reject H0"],
})
print(results.to_string(index=False))
```

_Happy testing — and remember: when the p-value is small, ask "so what?" before you ship._
