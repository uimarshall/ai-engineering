# Hypothesis Testing: The Independent Samples T-Test in Python

### A Beginner-Friendly, End-to-End Guide

> **What you will be able to do after this guide**
>
> 1. Explain, in plain English, what a hypothesis test actually decides.
> 2. Write down the null and alternative hypotheses for a two-group comparison.
> 3. Compute a **t-statistic** by hand from the formula _and_ with one line of Python.
> 4. Find a **critical value**, draw it on a graph, and use it to make a decision.
> 5. Run the test on realistic business data and correctly interpret every number.
> 6. Draw six diagnostic/interpretation graphs and explain what each element means.
> 7. Avoid the classic beginner mistakes (wrong tail, ignoring assumptions, peeking).

---

## Table of Contents

1. [The Big Picture](#1-the-big-picture)
2. [The Business Scenario We Will Use](#2-the-business-scenario-we-will-use)
3. [Core Vocabulary in Plain English](#3-core-vocabulary-in-plain-english)
4. [When Do You Use an Independent Samples T-Test?](#4-when-do-you-use-an-independent-samples-t-test)
5. [Null and Alternative Hypotheses (One-Tailed vs Two-Tailed)](#5-null-and-alternative-hypotheses)
6. [The Formulas, Broken Down Piece by Piece](#6-the-formulas-broken-down-piece-by-piece)
7. [The Critical Value — The Referee's Line](#7-the-critical-value--the-referees-line)
8. [The t-Statistic — How It Drives Your Conclusion](#8-the-t-statistic--how-it-drives-your-conclusion)
9. [Assumptions and How to Check Them](#9-assumptions-and-how-to-check-them)
10. [The Complete Runnable Python Script](#10-the-complete-runnable-python-script)
11. [The Graphs, Explained Point by Point](#11-the-graphs-explained-point-by-point)
12. [Writing the Conclusion Like a Professional](#12-writing-the-conclusion-like-a-professional)
13. [Effect Size: Is the Difference _Big_ or Just _Real_?](#13-effect-size)
14. [Power and Sample Size: How Many Users Do I Need?](#14-power-and-sample-size)
15. [Common Beginner Mistakes](#15-common-beginner-mistakes)
16. [When Assumptions Fail: Alternatives](#16-when-assumptions-fail-alternatives)
17. [Company Use Cases That Drive Business Decisions](#17-company-use-cases-that-drive-business-decisions)
18. [One-Page Cheat Sheet](#18-one-page-cheat-sheet)
19. [Practice Exercises](#19-practice-exercises)

---

## 1. The Big Picture

### 1.1 The problem every data scientist faces

You work for an online store. Marketing changed the checkout page.
Revenue per visitor _looks_ higher now. But "looks higher" is not proof — random
luck can produce a difference even if nothing really changed.

**Hypothesis testing is a formal courtroom procedure for deciding whether an
observed difference is real signal or just random noise.**

- **The defendant** = "Nothing changed." (the _null hypothesis_)
- **The evidence** = your sample data.
- **The verdict** = reject the null, or fail to reject it.
- **The standard of proof** = the significance level α (like "beyond reasonable doubt").
- **The test statistic** = the strength of the evidence, converted to one number.
- **The critical value** = the exact line the evidence must cross to convict.

A hypothesis test never says "there is a 95% chance the new page is better."
It says: _"If nothing had changed, data this extreme would be very unlikely."_
That is a subtle but crucial difference.

### 1.2 Why the t-test specifically?

We almost always compare **means of two groups** and we almost never know the
true population standard deviation σ. When σ is unknown and we estimate it from
the sample, the maths introduces extra uncertainty. That uncertainty follows the
**t-distribution** instead of the normal distribution.

So: **z-test = you know σ (rare). t-test = you estimate σ from data (normal).**

The independent samples t-test compares the means of **two separate, unrelated
groups** — hence "independent" (also called _unpaired_, _between-subjects_, or
_two-sample_).

---

## 2. The Business Scenario We Will Use

> **A/B Test: Checkout Page Redesign**
>
> - **Group A – Control:** 80 visitors saw the _old_ checkout page.
> - **Group B – Treatment:** 80 visitors saw the _new_ checkout page.
> - **Metric:** amount spent per visitor, in dollars.
> - **Question:** Did the new page change average spend per visitor?

This is exactly how real A/B tests work: two independent groups, one continuous
metric, one decision to make.

**Why the samples are independent:** a visitor appears in exactly one group, and
one visitor's spending does not mathematically determine another's. (If instead
you measured the _same_ 80 people before and after the redesign, that would be a
**paired t-test**, a different test.)

---

## 3. Core Vocabulary in Plain English

| Term                        | Plain-English meaning                                                                     | In our A/B test                         |
| --------------------------- | ----------------------------------------------------------------------------------------- | --------------------------------------- |
| **Population**              | Every unit you care about                                                                 | All visitors who will ever see the page |
| **Sample**                  | The subset you actually measured                                                          | Our 80 + 80 visitors                    |
| **Parameter**               | A number describing the population (usually unknown)                                      | True mean spend μ_A, μ_B                |
| **Statistic**               | A number computed from the sample (our estimate)                                          | Sample means x̄_A, x̄_B                   |
| **H₀ (null hypothesis)**    | The boring default: no effect, no difference                                              | μ_A = μ_B                               |
| **H₁ (alternative)**        | What you want to prove                                                                    | μ_A ≠ μ_B (or μ_B > μ_A)                |
| **α (significance level)**  | Your tolerance for a false alarm. Chosen _before_ the test                                | α = 0.05                                |
| **t-statistic**             | Difference in means divided by its standard error = **signal ÷ noise**                    | e.g. t = 2.63                           |
| **Standard error (SE)**     | How much a statistic would wobble across repeated samples                                 | SE of the mean difference               |
| **Critical value**          | The t-value that marks the edge of the rejection region                                   | ±1.99 for α = 0.05, df ≈ 158            |
| **Rejection region**        | The extreme zone where H₀ is too implausible                                              | Both tails for a two-sided test         |
| **p-value**                 | Probability of seeing data this extreme _if H₀ were true_                                 | e.g. p = 0.009                          |
| **Degrees of freedom (df)** | How much independent information the data carry; controls the shape of the t-distribution | ≈ n_A + n_B − 2                         |
| **Type I error (α)**        | False positive: rejecting a true H₀                                                       | Shipping a useless page                 |
| **Type II error (β)**       | False negative: keeping a good page                                                       | Losing money by not shipping            |
| **Power (1 − β)**           | Chance of detecting a real effect                                                         | Usually aim for ≥ 0.80                  |
| **Effect size**             | How _big_ the difference is, in standard units                                            | Cohen's d                               |

**Memory hook:** α is your **false-alarm budget**. You spend it in the tails of
the distribution. The smaller you make α, the harder it is to convict H₀ — and
the more likely you are to miss a real effect.

---

## 4. When Do You Use an Independent Samples T-Test?

Use it when **all** of these hold:

1. You compare **exactly two groups**.
2. The groups are **independent** (different people/units, no pairing).
3. The outcome is **continuous** (dollars, seconds, scores, ratings).
4. You care about the **mean** of that outcome.
5. The data are roughly **normally distributed** within each group _or_ each group
   has a reasonably large sample (n ≳ 30). The test is fairly robust to mild
   non-normality but **not** to extreme outliers.

Do **not** use it when:

- The groups are the same units measured twice → use a **paired t-test**.
- You compare **three or more** groups → use **ANOVA**.
- The outcome is yes/no (converted / not converted) → use a **two-proportion z-test**
  or a chi-square test.
- The data are heavily skewed with outliers and small n → use the
  **Mann–Whitney U test** (the non-parametric cousin of the t-test).

---

## 5. Null and Alternative Hypotheses

### 5.1 Two-sided (non-directional)

```

H₀: μ_B − μ_A = 0 (the new page changes nothing)
H₁: μ_B − μ_A ≠ 0 (the new page changes something, either way)

```

This is the default and the safest choice when you don't have strong prior
reason to expect one direction. It splits α across both tails.

### 5.2 One-sided (directional)

```

H₀: μ_B − μ_A ≤ 0 (new page is not better)
H₁: μ_B − μ_A > 0 (new page IS better)

```

Use this only when **you would not act on the opposite result anyway**. It is
more powerful (all of α sits in one tail), but you must decide the direction
_before_ seeing the data. Choosing the tail afterwards is a form of cheating
called _p-hacking_.

> **Rule of thumb for business:** start with two-sided. Switch to one-sided only
> when a result in the "wrong" direction would lead to no action whatsoever.

---

## 6. The Formulas, Broken Down Piece by Piece

### 6.1 The master formula: every t-statistic has the same shape

```

              estimate − hypothesised value
     t   =   ────────────────────────────────
                    standard error

```

```

              (x̄_B − x̄_A)  −  0
     t   =   ─────────────────────
                  SE(x̄_B − x̄_A)

```

Read it as **signal ÷ noise**:

| Piece           | Meaning                                                                     |
| --------------- | --------------------------------------------------------------------------- |
| `x̄_B − x̄_A`     | **Signal** — the observed difference in sample means (the treatment effect) |
| `0`             | The value H₀ claims the difference should be. Usually 0, so it vanishes     |
| `SE(x̄_B − x̄_A)` | **Noise** — the typical random wobble of that difference                    |
| `t`             | How many "noise units" the signal is worth                                  |

A t of 2 means "the difference is twice as large as the typical random wobble."
The larger |t|, the stronger the evidence against H₀. **A t near 0 means the data
look exactly like what H₀ predicts.**

### 6.2 The numerator: the difference in means

```

     x̄_B = (1/n_B) · Σ x_Bi        x̄_A = (1/n_A) · Σ x_Ai

```

- `x̄_B` and `x̄_A` are the **sample means** of the treatment and control groups.
- `n_A`, `n_B` are the group sizes.
- `Σ` means "add up every value."

We compare means because, under the central limit theorem, the _sampling
distribution of the mean_ is close to normal even when the raw data are not —
which is what makes the t-test so widely usable.

### 6.3 The denominator: the standard error of the difference

For independent groups, **variances add**:

```

     SE(x̄_B − x̄_A)  =  √( s²_B / n_B  +  s²_A / n_A )

```

| Piece        | Meaning                                                                  |
| ------------ | ------------------------------------------------------------------------ |
| `s²_B`       | Sample variance of group B (the spread of spend values, squared units)   |
| `s²_B / n_B` | Variance of group B's _mean_ — bigger samples make the mean steadier     |
| `s²_A / n_A` | Variance of group A's mean                                               |
| `√( … )`     | Combine, then take the square root to return to original units (dollars) |

`n` appears in the denominator, so **bigger samples shrink the SE**, which
inflates t and makes real effects easier to detect. That is why "statistically
significant" often just means "we had a lot of data."

Sample variance formula:

```

     s² = Σ(x_i − x̄)² / (n − 1)

```

The `n − 1` (Bessel's correction) is used because we estimated x̄ from the same
data, which "uses up" one degree of freedom.

### 6.4 Two versions of the test

#### Welch's t-test (unequal variances) — **use this by default**

```

             x̄_B − x̄_A
     t  =  ────────────────────────
            √( s²_B/n_B + s²_A/n_A )

```

No assumption that the two groups have equal variance. It is slightly less
powerful when variances really are equal, but far safer when they are not —
and you can never be sure in advance.

#### Student's pooled t-test (equal variances)

```

             x̄_B − x̄_A
     t  =  ────────────────────        where     s²_p = ────────────────────
            s_p · √(1/n_B + 1/n_A)                        n_A + n_B − 2
                                                     (n_A−1)s²_A + (n_B−1)s²_B

```

| Piece              | Meaning                                                                                                   |
| ------------------ | --------------------------------------------------------------------------------------------------------- |
| `s²_p`             | **Pooled variance** — a weighted average of the two group variances, weighted by their degrees of freedom |
| `s_p`              | The pooled standard deviation                                                                             |
| `√(1/n_B + 1/n_A)` | Converts the pooled SD into the standard error of the _difference_                                        |

If the two group sizes and variances are equal, pooled and Welch give identical
results. Otherwise they differ.

### 6.5 Degrees of freedom

**Pooled:** simple and exact.

```

     df = n_A + n_B − 2

```

**Welch:** messy but accurate (Welch–Satterthwaite approximation):

```

                   ( s²_A/n_A + s²_B/n_B )²
     df  =  ─────────────────────────────────────────
             (s²_A/n_A)² / (n_A − 1)  +  (s²_B/n_B)² / (n_B − 1)

```

| Piece       | Meaning                                                                                |
| ----------- | -------------------------------------------------------------------------------------- |
| Numerator   | Squared total variance of the difference                                               |
| Denominator | The same quantity split by each group's information, each divided by its `n − 1`       |
| Result      | Usually between `min(n_A, n_B) − 1` and `n_A + n_B − 2`. Non-integer is perfectly fine |

You rarely compute this by hand — `scipy` reports it — but you must understand
that **df controls the shape of the t-distribution**, and therefore the critical
value. Small df → fatter tails → larger critical value → harder to reject H₀.

### 6.6 The critical value formula

The critical value is the **inverse** of the t-distribution's cumulative
distribution function (CDF):

```

     t_crit  =  t.ppf(1 − α/2, df)        ← two-sided
     t_crit  =  t.ppf(1 − α,   df)        ← one-sided (right tail)

```

| Piece     | Meaning                                                                                         |
| --------- | ----------------------------------------------------------------------------------------------- |
| `ppf`     | "Percent point function" = the inverse CDF: give me the x-value whose area to the left equals q |
| `1 − α/2` | For α = 0.05 two-sided, that is 0.975 — the point with 97.5% of the area to its left            |
| `df`      | The degrees of freedom from §6.5                                                                |

### 6.7 From t to p-value

```

     p (two-sided)  =  2 × P(T ≥ |t|)          P(T ≥ |t|) = t.sf(|t|, df)
     p (right tail) =  P(T ≥ t)     =  t.sf(t, df)

```

- `sf` = **survival function** = the area to the right of a value = 1 − CDF.
- Because the t-distribution is symmetric, the two-sided p is just twice the
  one-sided p in the direction of the observed effect.

### 6.8 Confidence interval for the difference

```

     (x̄_B − x̄_A)  ±  t_crit × SE(x̄_B − x̄_A)

```

A 95% CI that does **not** contain 0 is mathematically equivalent to rejecting
H₀ at α = 0.05. The CI is usually more useful for business because it shows the
**range of plausible effect sizes** in dollars, not just a yes/no.

### 6.9 Effect size: Cohen's d

```

             x̄_B − x̄_A
     d  =  ─────────────
                s_p

```

Interpretation: 0.2 = small, 0.5 = medium, 0.8 = large (Cohen's conventions).
It converts the dollar difference into "how many standard deviations did we move?"

---

## 7. The Critical Value — The Referee's Line

### 7.1 The idea

If H₀ is true, the t-statistic is not a fixed number — it is _random_, and it
follows a **t-distribution with df degrees of freedom**. Most of the time it
lands near 0. Occasionally it lands far out by pure luck.

The **critical value** is the cutoff you set in advance: _"If the t-statistic
lands beyond this line, I will conclude that luck alone is too unlikely an
explanation."_

### 7.2 The three things that determine it

1. **α** — how strict you are. Smaller α pushes the line further out.
2. **Two-sided vs one-sided** — two-sided splits α across both tails, pushing the
   line further out than a one-sided test at the same α.
3. **df** — fewer degrees of freedom means fatter tails, hence a larger cutoff.

### 7.3 Reading a classic table (two-sided, α = 0.05)

| df  | Critical value | df  | Critical value |
| --- | -------------- | --- | -------------- |
| 1   | 12.706         | 20  | 2.086          |
| 2   | 4.303          | 25  | 2.060          |
| 3   | 3.182          | 30  | 2.042          |
| 5   | 2.571          | 40  | 2.021          |
| 10  | 2.228          | 60  | 2.000          |
| 12  | 2.179          | 120 | 1.980          |
| 15  | 2.131          | ∞   | **1.960**      |

Notice the table converging to **1.96** — that is the famous z-value from the
normal distribution. With lots of data, the t-test and z-test agree. With small
samples, the t critical value is noticeably bigger.

### 7.4 Finding it in Python

```python
from scipy import stats

alpha = 0.05
df    = 158                     # example

t_crit_two = stats.t.ppf(1 - alpha / 2, df)   # 1.9752  (two-sided)
t_crit_one = stats.t.ppf(1 - alpha,     df)   # 1.6547  (one-sided, right)
print(t_crit_two, t_crit_one)
```

`stats.t.ppf(0.975, 158)` answers the question _"which t-value has 97.5% of the
distribution to its left?"_ That value, on the positive side, is +1.975. By
symmetry the negative cutoff is −1.975.

### 7.5 The decision rule (critical-value method)

```
     if |t_observed|  >  t_crit        →  REJECT H₀        (statistically significant)
     if |t_observed|  ≤  t_crit        →  FAIL TO REJECT H₀ (not significant)
```

For a one-sided right-tail test, drop the absolute value:

```
     if t_observed  >  t_crit_one      →  REJECT H₀
```

**Key insight:** the critical value and the p-value are two views of the same
fact. They always agree. The critical value is a _threshold on the t-scale_; the
p-value is the _probability beyond your t_. Saying "t = 2.63 exceeds 1.975" and
saying "p = 0.009 is below 0.05" are logically identical statements.

---

## 8. The t-Statistic — How It Drives Your Conclusion

### 8.1 What the t-statistic is really telling you

`t = signal ÷ noise`. Concretely:

| t value    | Plain-English reading                                                       |
| ---------- | --------------------------------------------------------------------------- |
| ≈ 0        | The group means are practically identical. Data look exactly like H₀        |
| ±1         | The difference is one standard-error unit. Very common by chance (p ≈ 0.32) |
| ±1.96      | Right at the two-sided α = 0.05 frontier for large samples                  |
| ±2.6       | About 2.6 SEs out. Unlikely under H₀ (p ≈ 0.01)                             |
| ±4 or more | Almost impossible by chance. Very strong evidence                           |

### 8.2 The sign of t is not "strength" — it is _direction_

```
     t > 0   →   group listed FIRST has the larger mean
     t < 0   →   group listed SECOND has the larger mean
```

> ⚠️ **Beginner trap:** `stats.ttest_ind(a, b)` computes `(mean of a) − (mean of b)`.
> If you swap the argument order, t flips sign and a one-sided p-value changes
> completely. Always know which group you passed first.

### 8.3 The full decision procedure, step by step

1. State H₀ and H₁ **before** looking at the data.
2. Choose α (usually 0.05) and decide two- or one-sided.
3. Check assumptions (normality, variance homogeneity — §9).
4. Compute the t-statistic and df.
5. Find the critical value from α and df.
6. Compute the p-value (or just compare t to the critical value).
7. Decide: reject or fail to reject.
8. Report the effect size and a confidence interval — the business-relevant part.
9. Translate into a decision: ship, iterate, or gather more data.

### 8.4 Why a big t can still mean a tiny effect

```
     t  =  (x̄_B − x̄_A) / SE          and      SE  ∝  1/√n
```

Double the sample size and SE shrinks by ~29%, so t grows by ~41% **without any
change in the real effect**. A statistically significant result therefore says
"the effect is probably not zero" — never "the effect is large." Always pair the
p-value with an effect size and a dollar value (see §13).

---

## 9. Assumptions and How to Check Them

| Assumption                             | What it means                             | How to check in Python            | What to do if violated                                  |
| -------------------------------------- | ----------------------------------------- | --------------------------------- | ------------------------------------------------------- |
| **Independence**                       | One observation doesn't influence another | Study design, not a test          | Fix the design; consider mixed-effects models           |
| **Normality within groups**            | Each group's data is roughly bell-shaped  | Q–Q plot, histogram, Shapiro–Wilk | Large n (≥30/group) → usually fine; else Mann–Whitney U |
| **Equal variances** (pooled test only) | Both groups share a variance              | Levene's test (`center="median"`) | Use **Welch's** test (`equal_var=False`)                |
| **No extreme outliers**                | Means aren't dragged around               | Boxplot, z-scores                 | Investigate, Winsorise, or use robust/rank tests        |

```python
from scipy import stats

# 1) Normality, per group (Shapiro-Wilk works well for n < 5000)
print("Control :", stats.shapiro(group_A))
print("Treatment:", stats.shapiro(group_B))

# 2) Equal variances (median-centred = Brown–Forsythe, the robust version)
print("Levene:", stats.levene(group_A, group_B, center="median"))
```

**How to read these tests**

- Shapiro–Wilk p < 0.05 → evidence the group is **not** normal.
- Levene p < 0.05 → variances differ → use `equal_var=False` (Welch).
- Levene p ≥ 0.05 → no evidence variances differ → pooled is acceptable.

**Important caveat:** with small samples these tests have low power (they miss
real problems); with huge samples they are over-sensitive (they flag trivial
deviations). Use them as _one input alongside graphs_, never as the sole judge.
Because Welch performs well in almost all situations, many practitioners simply
always use `equal_var=False`.

---

## 10. The Complete Runnable Python Script

Save this as `ttest_ab_test.py` and run it top to bottom. It produces six
figures and prints a full report.

```python
# ==============================================================
# INDEPENDENT SAMPLES T-TEST  —  COMPLETE WORKED EXAMPLE
# Scenario: A/B test of an e-commerce checkout page
# Metric  : spend per visitor (USD)
# ==============================================================
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

plt.rcParams["figure.dpi"]   = 110
plt.rcParams["axes.grid"]    = True
plt.rcParams["grid.alpha"]   = 0.30
plt.rcParams["axes.titlesize"] = 13

# ------------------------------------------------------------------
# 1. SIMULATE THE EXPERIMENT
#    In real life you would load a CSV:  df = pd.read_csv("ab_test.csv")
# ------------------------------------------------------------------
rng = np.random.default_rng(seed=42)

n_A, n_B = 80, 80                                  # 80 visitors per group
group_A = np.clip(rng.normal(48.0, 12.0, n_A), 0, None)   # control
group_B = np.clip(rng.normal(53.5, 13.5, n_B), 0, None)   # treatment

# Build a tidy DataFrame (the shape real datasets come in)
df = pd.DataFrame({
    "spend": np.concatenate([group_A, group_B]),
    "group": ["Control (A)"] * n_A + ["Treatment (B)"] * n_B,
})

# ------------------------------------------------------------------
# 2. DESCRIPTIVE STATISTICS
# ------------------------------------------------------------------
summary = (df.groupby("group")["spend"]
             .agg(n="count", mean="mean", std="std", median="median")
             .round(2))
summary["variance"] = df.groupby("group")["spend"].var().round(2)
print("\n=== Descriptive statistics ===")
print(summary)

# ------------------------------------------------------------------
# 3. ASSUMPTION CHECKS
# ------------------------------------------------------------------
shapiro_A = stats.shapiro(group_A)
shapiro_B = stats.shapiro(group_B)
levene    = stats.levene(group_A, group_B, center="median")

print("\n=== Assumption checks ===")
print(f"Shapiro-Wilk  Control   : W = {shapiro_A.statistic:.3f}, p = {shapiro_A.pvalue:.3f}")
print(f"Shapiro-Wilk  Treatment : W = {shapiro_B.statistic:.3f}, p = {shapiro_B.pvalue:.3f}")
print(f"Levene (Brown-Forsythe) : stat = {levene.statistic:.3f}, p = {levene.pvalue:.3f}")

# ------------------------------------------------------------------
# 4. THE T-TEST ITSELF  (one line!)
#    equal_var=False  ->  Welch's t-test (recommended default)
#    order matters: t = (mean(group_B) - mean(group_A))
# ------------------------------------------------------------------
alpha = 0.05
t_stat, p_two = stats.ttest_ind(group_B, group_A, equal_var=False)
# grab Welch's degrees of freedom from the result object
result = stats.ttest_ind(group_B, group_A, equal_var=False)
df_welch = result.df

print("\n=== scipy result ===")
print(f"t = {t_stat:.4f},  df = {df_welch:.2f},  p (two-sided) = {p_two:.4f}")

# ------------------------------------------------------------------
# 5. THE SAME TEST, COMPUTED BY HAND  (so nothing is a black box)
# ------------------------------------------------------------------
mean_A, mean_B = group_A.mean(), group_B.mean()
var_A,  var_B  = group_A.var(ddof=1), group_B.var(ddof=1)

se_A = var_A / n_A          # variance of the control mean
se_B = var_B / n_B          # variance of the treatment mean
se_diff = np.sqrt(se_A + se_B)          # standard error of the difference

t_manual = (mean_B - mean_A) / se_diff  # signal / noise

df_manual = (se_A + se_B) ** 2 / (se_A**2 / (n_A - 1) + se_B**2 / (n_B - 1))

p_two_manual  = 2 * stats.t.sf(abs(t_manual), df_manual)   # two-sided
p_one_manual  =     stats.t.sf(t_manual,     df_manual)    # right-tailed

print("\n=== Hand calculation ===")
print(f"mean_A = {mean_A:.3f}   mean_B = {mean_B:.3f}")
print(f"var_A  = {var_A:.3f}   var_B  = {var_B:.3f}")
print(f"SE(diff) = {se_diff:.4f}")
print(f"t (Welch) = {t_manual:.4f}   df = {df_manual:.2f}")
print(f"p two-sided = {p_two_manual:.4f}   p right-tailed = {p_one_manual:.4f}")

# ------------------------------------------------------------------
# 6. CRITICAL VALUES AND THE DECISION
# ------------------------------------------------------------------
t_crit_two = stats.t.ppf(1 - alpha / 2, df_manual)   # two-sided cutoff
t_crit_one = stats.t.ppf(1 - alpha,     df_manual)   # one-sided cutoff

reject_two = abs(t_manual) > t_crit_two
reject_one = t_manual >  t_crit_one

print("\n=== Decision (two-sided, alpha = 0.05) ===")
print(f"critical values : +/- {t_crit_two:.4f}")
print(f"observed t      : {t_manual:.4f}")
print(f"|t| > t_crit ?  : {reject_two}   -> "
      f"{'REJECT H0' if reject_two else 'FAIL TO REJECT H0'}")
print(f"p = {p_two_manual:.4f} < alpha ? : {p_two_manual < alpha}")

# ------------------------------------------------------------------
# 7. CONFIDENCE INTERVAL + EFFECT SIZE
# ------------------------------------------------------------------
diff_means = mean_B - mean_A
ci_low  = diff_means - t_crit_two * se_diff
ci_high = diff_means + t_crit_two * se_diff

pooled_var = ((n_A - 1) * var_A + (n_B - 1) * var_B) / (n_A + n_B - 2)
cohens_d   = diff_means / np.sqrt(pooled_var)

print("\n=== Effect size and interval ===")
print(f"Difference in means : {diff_means:+.3f} USD")
print(f"95% CI              : [{ci_low:.3f}, {ci_high:.3f}]")
print(f"Cohen's d           : {cohens_d:.3f}")

# annualised business impact (illustrative): 1,000,000 visitors / year
annual_impact = diff_means * 1_000_000
print(f"Projected annual impact at 1M visitors: {annual_impact:+,.0f} USD")

# ==================================================================
# FIGURE 1 — The t-distribution, critical values, and observed t
# ==================================================================
fig, ax = plt.subplots(figsize=(11, 5.5))
x = np.linspace(-5, 5, 2000)
y = stats.t.pdf(x, df_manual)

ax.plot(x, y, color="black", lw=2,
        label=f"t-distribution (df = {df_manual:.0f})")
ax.fill_between(x, y, where=(x <= -t_crit_two), color="crimson", alpha=0.35,
                label=f"Rejection region (alpha/2 = {alpha/2:.3f} each tail)")
ax.fill_between(x, y, where=(x >=  t_crit_two), color="crimson", alpha=0.35)

ax.axvline(-t_crit_two, color="crimson", ls="--", lw=1.6)
ax.axvline( t_crit_two, color="crimson", ls="--", lw=1.6)
ax.axvline(t_manual,    color="royalblue", lw=2.6,
           label=f"Observed t = {t_manual:.2f}")

ax.annotate(f"critical value\n{t_crit_two:.2f}",
            xy=(t_crit_two, stats.t.pdf(t_crit_two, df_manual)),
            xytext=(t_crit_two + 0.55, 0.20),
            arrowprops=dict(arrowstyle="->", color="crimson"), color="crimson")
ax.annotate(f"observed t\n{t_manual:.2f}",
            xy=(t_manual, stats.t.pdf(t_manual, df_manual)),
            xytext=(t_manual + 0.45, 0.28),
            arrowprops=dict(arrowstyle="->", color="royalblue"), color="royalblue")

ax.set_title("Figure 1 — Where the evidence lands on the t-distribution")
ax.set_xlabel("t value")
ax.set_ylabel("Probability density")
ax.legend(loc="upper left", fontsize=9)
plt.tight_layout()
plt.savefig("fig1_t_distribution.png", bbox_inches="tight")
plt.show()

# ==================================================================
# FIGURE 2 — Both group distributions with their means
# ==================================================================
fig, ax = plt.subplots(figsize=(11, 5.5))
bins = np.linspace(0, 90, 26)

ax.hist(group_A, bins=bins, density=True, alpha=0.55,
        color="steelblue", edgecolor="white", label="Control (A)")
ax.hist(group_B, bins=bins, density=True, alpha=0.55,
        color="darkorange", edgecolor="white", label="Treatment (B)")

xs = np.linspace(0, 90, 400)
ax.plot(xs, stats.gaussian_kde(group_A)(xs), color="steelblue", lw=2.2)
ax.plot(xs, stats.gaussian_kde(group_B)(xs), color="darkorange", lw=2.2)

ax.axvline(mean_A, color="steelblue", ls="--", lw=2,
           label=f"Mean A = {mean_A:.2f}")
ax.axvline(mean_B, color="darkorange", ls="--", lw=2,
           label=f"Mean B = {mean_B:.2f}")

ax.annotate("", xy=(mean_A, 0.030), xytext=(mean_B, 0.030),
            arrowprops=dict(arrowstyle="<->", color="black", lw=1.8))
ax.text((mean_A + mean_B) / 2, 0.032,
        f"gap = {diff_means:+.2f} USD", ha="center", fontsize=10)

ax.set_title("Figure 2 — Two independent samples: distributions, means and the gap")
ax.set_xlabel("Spend per visitor (USD)")
ax.set_ylabel("Density (share of visitors per dollar bucket)")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("fig2_group_distributions.png", bbox_inches="tight")
plt.show()

# ==================================================================
# FIGURE 3 — Boxplot with every raw data point overlaid
# ==================================================================
fig, ax = plt.subplots(figsize=(8.5, 5.5))
bp = ax.boxplot([group_A, group_B], patch_artist=True, widths=0.5,
                medianprops=dict(color="black", lw=2))
for patch, color in zip(bp["boxes"], ["steelblue", "darkorange"]):
    patch.set_facecolor(color)
    patch.set_alpha(0.55)

jitter = np.random.default_rng(0)
ax.scatter(1 + jitter.normal(0, 0.055, n_A), group_A, s=18,
           color="steelblue", alpha=0.75, label="Control visitors")
ax.scatter(2 + jitter.normal(0, 0.055, n_B), group_B, s=18,
           color="darkorange", alpha=0.75, label="Treatment visitors")
ax.scatter([1, 2], [mean_A, mean_B], marker="D", s=110, color="black",
           zorder=5, label="Group mean")

ax.set_xticks([1, 2], ["Control (A)", "Treatment (B)"])
ax.set_title("Figure 3 — Boxplot + every data point (spread, median, outliers)")
ax.set_ylabel("Spend per visitor (USD)")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("fig3_boxplot.png", bbox_inches="tight")
plt.show()

# ==================================================================
# FIGURE 4 — Q-Q plots to check normality
# ==================================================================
fig, axes = plt.subplots(1, 2, figsize=(11.5, 5))
for ax, data, name in zip(axes, [group_A, group_B],
                          ["Control (A)", "Treatment (B)"]):
    stats.probplot(data, dist="norm", plot=ax)
    ax.get_lines()[0].set_markerfacecolor("steelblue" if "Control" in name else "darkorange")
    ax.get_lines()[0].set_markeredgecolor("none")
    ax.get_lines()[1].set_color("crimson")
    ax.set_title(f"Figure 4 — Q-Q plot: {name}")
plt.tight_layout()
plt.savefig("fig4_qq_plots.png", bbox_inches="tight")
plt.show()

# ==================================================================
# FIGURE 5 — Confidence interval for the difference in means
# ==================================================================
fig, ax = plt.subplots(figsize=(9.5, 4.2))
ax.errorbar(diff_means, 1,
            xerr=[[diff_means - ci_low], [ci_high - diff_means]],
            fmt="o", color="purple", capsize=9, markersize=11, lw=2.2)
ax.axvline(0, color="crimson", ls="--", lw=2, label="No effect (0 USD)")
ax.set_yticks([])
ax.set_ylim(0.7, 1.3)
ax.set_xlabel("Difference in mean spend:  Treatment - Control (USD)")
ax.set_title(f"Figure 5 — 95% CI for the difference: "
             f"{diff_means:+.2f}  [{ci_low:.2f}, {ci_high:.2f}]")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("fig5_confidence_interval.png", bbox_inches="tight")
plt.show()

# ==================================================================
# FIGURE 6 — Permutation distribution: a simulation of "H0 is true"
# ==================================================================
perm_rng = np.random.default_rng(7)
pooled   = np.concatenate([group_A, group_B])
n_total  = len(pooled)
perm_t   = np.empty(10_000)

for i in range(10_000):
    shuffled = perm_rng.permutation(pooled)   # shuffle group labels
    a, b = shuffled[:n_A], shuffled[n_A:]
    perm_t[i] = ((b.mean() - a.mean()) /
                 np.sqrt(b.var(ddof=1) / n_B + a.var(ddof=1) / n_A))

p_perm = np.mean(np.abs(perm_t) >= abs(t_manual))

fig, ax = plt.subplots(figsize=(11, 5.2))
ax.hist(perm_t, bins=60, color="lightsteelblue", edgecolor="white",
        label="t values when H0 is TRUE (10,000 label shuffles)")
mask = np.abs(perm_t) >= abs(t_manual)
ax.hist(perm_t[mask], bins=60, color="crimson", edgecolor="white",
        label=f"Area beyond our t  ->  p = {p_perm:.4f}")
ax.axvline(t_manual,  color="royalblue", lw=2.5, label=f"Observed t = {t_manual:.2f}")
ax.axvline(-t_manual, color="royalblue", lw=2.5, ls=":")
ax.set_title("Figure 6 — If H0 were true, how extreme is our result?")
ax.set_xlabel("t statistic")
ax.set_ylabel("Number of shuffles")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("fig6_permutation.png", bbox_inches="tight")
plt.show()

print(f"\nPermutation p-value = {p_perm:.4f}  (should be close to {p_two_manual:.4f})")
```

**What this script does, block by block**

| Block | Purpose                                                                                                       |
| ----- | ------------------------------------------------------------------------------------------------------------- |
| 1     | Creates two independent samples. `np.clip(..., 0, None)` removes negative spends, mimicking real revenue data |
| 2     | `groupby().agg()` produces the classic n / mean / std / median table you would put in a report                |
| 3     | Shapiro–Wilk (normality) and Levene (equal variance) checks the assumptions                                   |
| 4     | `stats.ttest_ind(..., equal_var=False)` runs Welch's test and returns t, p and df                             |
| 5     | Recomputes everything manually so you can see the formula in action and confirm the library is not magic      |
| 6     | Uses `stats.t.ppf` to get critical values, then applies the decision rule                                     |
| 7     | Adds the confidence interval, Cohen's d, and a dollar-value business projection                               |

---

## 11. The Graphs, Explained Point by Point

### Figure 1 — The t-distribution with critical values and observed t

**What is plotted**

- The black curve is the **probability density of the t-distribution with df ≈ 158**.
  Its height at any x shows how plausible that t-value is when H₀ is true. It is
  symmetrical and bell-shaped, but with slightly fatter tails than a normal curve
  (because df is finite).
- The two **red shaded tails** are the **rejection regions**. Each contains
  α/2 = 0.025 of the total area, so together they hold 5%. The area _is_ the
  probability budget.
- The two **red dashed vertical lines** sit exactly at ±t*crit (≈ ±1.975). These
  are the boundaries of the rejection regions. Their position is \_chosen by you*
  before the test, via α and df.
- The **blue solid vertical line** is the observed t-statistic from our data.
- The annotation arrows label both the boundary and the observation.

**How to read the conclusion from it**

- If the blue line falls **inside red shading** → the observation is in the
  rejection region → **reject H₀**.
- If it falls **in the white middle** → **fail to reject H₀**.
- In our run, t = 2.63 sits to the right of 1.975, clearly inside the right-hand
  red tail, so we reject H₀ at α = 0.05.
- The visual also shows _how close_ the call was: a line hugging the boundary
  means a fragile result that might flip with more data.

**Why this graph matters:** it makes the abstract phrase "statistically
significant" concrete — it is literally "did the blue line land in the red zone?"

### Figure 2 — Two overlapping distributions with the means

**What is plotted**

- Each **bar** of the histogram is a one-dollar spend bucket (25 buckets from
  $0 to $90) and its height is the **density** of visitors in that bucket, i.e.
  the share of the group that spent that amount. Blue = control, orange = treatment.
- The **smooth curves** are kernel density estimates (KDEs) — smoothed versions of
  the histograms that make the shape of each group's spend distribution easy to
  compare. Where the orange curve shifts right relative to blue, the treatment
  group spends more.
- The **dashed vertical lines** mark each group's sample mean (x̄_A, x̄_B) — the two
  numbers that go into the numerator of the t-statistic.
- The **double-headed arrow and "gap" label** show the raw difference in means,
  e.g. +5.2 USD. That arrow is the entire signal.

**What the individual data points do:** every visitor is one observation inside a
bar. A visitor who spent $57 lands in the $57 bucket and slightly raises that
bar. Several hundred such contributions build up the whole shape.

**How to read it**

- Look at the **horizontal shift** between the two means — that's the effect.
- Look at the **width and overlap** of the two distributions. Heavy overlap with
  a small shift suggests noise; widely separated peaks suggest a real effect.
- Notice that here the distributions overlap a lot even though the means differ.
  That is normal: individual behaviour is noisy, but _averages_ can still differ
  reliably. This is exactly the distinction between individual and statistical
  variation, and it is why the t-test exists.

### Figure 3 — Boxplot with raw points and the mean

**What is plotted**

- The **box** spans the interquartile range (IQR): from the 25th percentile (Q1)
  to the 75th percentile (Q3). It contains the middle 50% of visitors. A narrow
  box = consistent spending; a wide box = variable spending.
- The **thick black line** inside the box is the **median** (the 50th percentile).
- The **whiskers** extend to the most extreme data points within 1.5 × IQR of the
  box. Points beyond that are drawn as **outliers**.
- The **translucent dots** are every actual visitor's spend, jittered slightly
  left/right so identical values don't overlap. Blue = control, orange = treatment.
- The **black diamonds** mark each group's **mean** — the value the t-test actually
  compares.

**Why show raw points and not just a box?** A boxplot can hide whether a group is
bimodal, or how many points sit far out. Seeing the cloud of dots tells you at a
glance whether an outlier is driving the difference. If the whiskers overlap
heavily but one or two dots sit far out, be suspicious.

**Beginner comparison:** the boxplot is the "summary" view, Figure 2 is the
"shape" view, and Figure 3's dots are the "truth" view.

### Figure 4 — Q–Q plots for normality

**What is plotted**

- The **x-axis** holds theoretical quantiles from a perfect normal distribution.
- The **y-axis** holds your actual sorted data values.
- Each **dot** is one visitor's spend, plotted against where that value _would_
  sit if the data were perfectly normal.
- The **straight red line** is the ideal reference: if the dots lie exactly on it,
  the data are exactly normal.

**How to read it**

- Dots neatly on the line → normality is satisfied.
- Dots forming an **S-shape** (or curving away at the ends) → skewed, heavier or
  lighter tails than normal.
- A few dots jumping off at the extremes → outliers.
- Because our simulated data were generated from normal distributions (and only
  mildly clipped at zero), the points should track the line closely — evidence
  that the t-test's normality assumption is reasonable here.

### Figure 5 — Confidence interval for the difference

**What is plotted**

- The **purple dot** is the point estimate of the difference in means (e.g.
  +5.2 USD). This is the same number that sits in the numerator of the t-statistic.
- The **horizontal purple bar with caps** is the 95% confidence interval,
  computed as `difference ± t_crit × SE`. It shows the range of values that are
  consistent with the data.
- The **red dashed line at 0** is the "no effect" reference line — the world H₀
  describes.

**How to read it (the most business-friendly graph of all)**

- If the **bar does not cross the red line**, H₀ is rejected at α = 0.05. Our bar
  sits entirely to the right of 0, matching the t-test's rejection.
- The bar's **width** shows precision: a long bar means "we have a rough idea,"
  a short bar means "we know the effect well."
- The bar's **position** shows magnitude in dollars, which is what the business
  actually cares about: "we estimate the new page is worth between +$1 and +$9
  per visitor."
- If the bar crosses zero, the honest conclusion is "we cannot rule out no effect."

### Figure 6 — Permutation distribution (a simulation of H₀ being true)

**What is plotted**

- The 10,000 light-blue bars form the **distribution of the t-statistic under the
  null hypothesis**, built not from a formula but from brute force: randomly
  shuffle the group labels 10,000 times, recompute t each time, and record it.
  Because shuffling destroys any real treatment effect, every one of these t
  values was generated by pure chance.
- The **red bars** are the shuffles whose |t| was at least as extreme as our real
  observation. Their height relative to the whole histogram _is_ the p-value.
- The **blue vertical lines** mark our observed t (solid) and its mirror image
  (dotted), showing the symmetry the two-sided p-value exploits.

**What the individual bars do:** each bar counts how many of the 10,000
shuffles produced t-values in that narrow range. A tall bar near 0 means "random
label shuffles usually produce a tiny difference." The bars thin out drastically
past ±2: extreme t-values are rare when H₀ is true.

**Why include this graph?** It gives you an intuitive, formula-free answer to the
question _"what would the world look like if nothing were going on?"_ — and it
should give a p-value very close to the one `scipy` reported, which builds trust
in the analytic test.

---

## 12. Writing the Conclusion Like a Professional

Bad conclusions are ambiguous. Good ones contain five parts:
**direction, size, uncertainty, statistic, and decision.**

> ❌ "The p-value is 0.009 so the new page works."
>
> ✅ "The new checkout page increased average spend per visitor by **+$5.20**
> (95% CI: +$1.30 to +$9.10), a small-to-medium effect (Cohen's d = 0.41).
> A Welch independent-samples t-test found this difference statistically
> significant, **t(157.8) = 2.63, p = 0.009**, so we reject the null hypothesis
> at α = 0.05. Projected across one million annual visitors, this is worth
> roughly **+$5.2M**. Recommendation: roll out the new page and monitor for a
> novelty effect over the next two weeks."

Notice what "p = 0.009" contributes: _only_ the confidence that the effect is not
zero. Everything a manager cares about comes from the effect size and the CI.

---

## 13. Effect Size

Statistical significance answers _"is it real?"_ Effect size answers _"is it big?"_
A massive sample can make a $0.01 difference statistically significant.

| Measure        | Formula           | What it tells you                                                         |
| -------------- | ----------------- | ------------------------------------------------------------------------- |
| Raw difference | x̄_B − x̄_A         | Dollars per user — the business number                                    |
| **Cohen's d**  | (x̄_B − x̄_A) / s_p | Difference in standard-deviation units; comparable across metrics         |
| Relative lift  | (x̄_B − x̄_A) / x̄_A | Percentage improvement — what executives ask for                          |
| Glass's Δ      | (x̄_B − x̄_A) / s_A | Uses only the control group's SD (useful when treatment changed variance) |

**Cohen's d rules of thumb:** 0.2 small · 0.5 medium · 0.8 large.

```python
relative_lift = (mean_B - mean_A) / mean_A
print(f"Relative lift: {relative_lift:.2%}")
```

In our example, a +$5.20 lift on a $48 baseline is roughly an **11% relative
improvement** — meaningful for an e-commerce business with thin margins.

---

## 14. Power and Sample Size

**Power** = the probability of detecting a real effect. Low power is why so many
A/B tests "fail" even when the change genuinely works.

Four quantities are locked together — fix any three and the fourth is determined:

1. **Sample size (n)** — more data → more power.
2. **Effect size (d)** — bigger true effects are easier to see.
3. **α** — a stricter threshold reduces power.
4. **Power (1 − β)** — conventionally targeted at 0.80.

```python
# pip install statsmodels   (only needed for this section)
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()

# How many users per group to detect d = 0.41 with 80% power at alpha = 0.05?
n_needed = analysis.solve_power(effect_size=0.41, alpha=0.05,
                                power=0.80, ratio=1.0, alternative="two-sided")
print(f"Needed per group: {np.ceil(n_needed):.0f}")

# What power did our n = 80 actually give us?
power_achieved = analysis.power(effect_size=0.41, nobs1=80,
                                alpha=0.05, ratio=1.0)
print(f"Achieved power: {power_achieved:.2%}")

# What is the smallest effect we could detect with n = 80?
mde = analysis.solve_power(effect_size=None, nobs1=80, alpha=0.05, power=0.80)
print(f"Minimum detectable effect size (Cohen's d): {mde:.3f}")
```

**Key habit:** compute the required sample size _before_ running the test. Peeking
at results daily and stopping the moment p < 0.05 inflates the Type I error rate
far above 5% — a very common and very expensive mistake in industry.

---

## 15. Common Beginner Mistakes

| Mistake                                                | Why it's wrong                                                 | Fix                                                                    |
| ------------------------------------------------------ | -------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Interpreting p as "probability H₀ is true"             | p is the probability of the _data_, given H₀ — not the reverse | Say: "If H₀ were true, data this extreme would occur 0.9% of the time" |
| Saying "we proved H₀" when p is large                  | Absence of evidence ≠ evidence of absence                      | Say "failed to reject," and check power                                |
| Choosing the tail after seeing the data                | That's p-hacking; it doubles your false-positive rate          | Pre-register the hypothesis                                            |
| Running the test on the wrong argument order           | Flips the sign of t and inverts one-sided p-values             | Always document which group is first                                   |
| Ignoring assumption checks                             | Big variance differences can badly distort the pooled test     | Use Welch, inspect Q–Q and boxplots                                    |
| Reporting only p, not effect size                      | A significant $0.02 lift is worthless                          | Always report the CI and Cohen's d                                     |
| Running 20 t-tests and reporting the one with p < 0.05 | With α = 0.05, ~1 in 20 tests is a false positive by design    | Apply Bonferroni (`α/k`) or Benjamini–Hochberg                         |
| Stopping the A/B test the moment it hits significance  | Inflates Type I error dramatically                             | Pre-compute the sample size and wait                                   |
| Confusing statistical with practical significance      | Huge samples make trivial effects significant                  | Tie results to dollars and business thresholds                         |
| Using a t-test on binary metrics                       | The normal model is wrong for proportions                      | Use a two-proportion z-test                                            |

**Multiple-comparison correction in one line:**

```python
from statsmodels.stats.multitest import multipletests
p_values = [0.001, 0.013, 0.041, 0.38, 0.62]
rejected, p_adjusted, _, _ = multipletests(p_values, alpha=0.05, method="fdr_bh")
print(list(zip(p_values, p_adjusted.round(3), rejected)))
```

---

## 16. When Assumptions Fail: Alternatives

```python
# Non-parametric alternative: Mann-Whitney U (rank-based, no normality needed)
u_stat, p_mwu = stats.mannwhitneyu(group_B, group_A, alternative="two-sided")
print(f"Mann-Whitney U = {u_stat:.1f}, p = {p_mwu:.4f}")

# Rank-biserial correlation — the effect size for Mann-Whitney
n1, n2 = len(group_B), len(group_A)
rank_biserial = 1 - (2 * u_stat) / (n1 * n2)
print(f"Rank-biserial correlation: {rank_biserial:.3f}")

# Bootstrap CI for the difference in means — no distributional assumptions at all
boot_rng = np.random.default_rng(123)
boot_diffs = [
    boot_rng.choice(group_B, n_B, replace=True).mean()
    - boot_rng.choice(group_A, n_A, replace=True).mean()
    for _ in range(10_000)
]
boot_ci = np.percentile(boot_diffs, [2.5, 97.5])
print(f"Bootstrap 95% CI for the difference: [{boot_ci[0]:.2f}, {boot_ci[1]:.2f}]")
```

| Situation                         | Use instead                             |
| --------------------------------- | --------------------------------------- |
| Non-normal, small n               | Mann–Whitney U                          |
| Very small n and strong skew      | Permutation / bootstrap test            |
| Same units measured twice         | Paired t-test or Wilcoxon signed-rank   |
| Binary outcome (converted yes/no) | Two-proportion z-test or Fisher's exact |
| More than two groups              | One-way ANOVA, then Tukey HSD post-hoc  |
| Unequal variances                 | Welch's t-test (already our default)    |

---

## 17. Company Use Cases That Drive Business Decisions

Each row is a real decision that an independent-samples t-test can settle.

| #   | Company type              | The two groups                  | Metric (continuous)                | H₀                        | Business decision if rejected                    | Cost of a Type I error                                                      | Cost of a Type II error                    |
| --- | ------------------------- | ------------------------------- | ---------------------------------- | ------------------------- | ------------------------------------------------ | --------------------------------------------------------------------------- | ------------------------------------------ |
| 1   | **E-commerce**            | Old vs new checkout page        | Spend per visitor                  | μ_new = μ_old             | Ship the redesign to 100% of traffic             | Pay developers to maintain a page that adds nothing; possible UX regression | Miss a multi-million-dollar revenue lift   |
| 2   | **SaaS / Product**        | Two onboarding flows            | Trial-to-paid revenue per signup   | μ_A = μ_B                 | Redirect the whole funnel to the winning flow    | Lose engineering time and confuse existing users                            | Slow growth; churn stays high              |
| 3   | **Digital marketing**     | Ad creative A vs B              | Revenue per 1,000 impressions      | μ_A = μ_B                 | Reallocate the ad budget to the winner           | Waste budget on a flat creative                                             | Keep burning money on the worse ad         |
| 4   | **Pharmaceutical**        | Drug vs placebo                 | Reduction in blood pressure (mmHg) | μ_drug = μ_placebo        | Submit for regulatory approval / continue trials | Approve an ineffective drug — safety and legal risk                         | Abandon a drug that works; patients suffer |
| 5   | **Fintech / Banking**     | Two loan-approval workflows     | Minutes to decision                | μ_manual = μ_automated    | Automate the faster process                      | Automate something slower or less accurate                                  | Poor customer experience; abandonment      |
| 6   | **Customer support**      | Chatbot-first vs human-first    | Average handling time (minutes)    | μ_bot = μ_human           | Scale the faster channel                         | Degrade service quality for a small speed gain                              | Keep paying for the slower channel         |
| 7   | **Manufacturing**         | Two suppliers' raw material     | Tensile strength (MPa)             | μ_supplier1 = μ_supplier2 | Switch suppliers or renegotiate                  | Production failures from weak material                                      | Overpay for equivalent material            |
| 8   | **HR / People Ops**       | Two training programmes         | Post-training productivity score   | μ_A = μ_B                 | Standardise the effective programme company-wide | Waste training budget and employee time                                     | Keep an ineffective programme for years    |
| 9   | **Healthcare operations** | Two triage protocols            | Patient wait time (minutes)        | μ_A = μ_B                 | Adopt the faster protocol hospital-wide          | Clinical risk from an inferior protocol                                     | Slower care; patient dissatisfaction       |
| 10  | **Education / EdTech**    | Two teaching methods            | Standardised test score            | μ_A = μ_B                 | Roll out the higher-scoring method               | Ineffective curriculum adopted at scale                                     | Students miss out on a better method       |
| 11  | **Subscription retail**   | Monthly vs annual-first pricing | Revenue per new subscriber         | μ_monthly = μ_annual      | Change the default plan presented                | Chase higher revenue at the cost of churn                                   | Leave ARPU on the table                    |
| 12  | **Logistics**             | Two route-planning algorithms   | Average delivery time (hours)      | μ_A = μ_B                 | Deploy the faster algorithm fleet-wide           | Retraining and rollout costs for no gain                                    | Fuel and labour costs stay high            |

### 17.1 A miniature end-to-end case: the marketing team's question

> **Situation.** An email marketing team ran two subject-line variants on 120
> recipients each. The metric is revenue per recipient (RPR).
>
> **Question.** Does variant B beat variant A?
>
> **Setup.**
>
> - H₀: μ_B = μ_A · H₁: μ_B ≠ μ_A (two-sided, because a loss would also be actionable)
> - α = 0.05
>
> ```python
> from scipy import stats
>
> variant_A = [12.4, 0.0, 8.9,  ...]   # revenue per recipient, group A
> variant_B = [17.1, 9.5, 22.3, ...]   # revenue per recipient, group B
>
> result = stats.ttest_ind(variant_B, variant_A, equal_var=False)
> print(result.statistic, result.pvalue, result.df)
> ```
>
> **Interpretation walkthrough.** Suppose the output is
> `t = 2.41, p = 0.017, df = 236`.
>
> 1. **t = 2.41** — the difference in mean RPR is 2.41 standard errors away from
>    zero. That is > 1.97, the critical value for α = 0.05 with large df.
> 2. **p = 0.017** — if the subject lines were truly equivalent, we would see a
>    gap this large in only about 1.7% of campaigns.
> 3. **Decision** — 0.017 < 0.05, so we reject H₀.
> 4. **Business translation** — combined with the CI (say +$1.10 to +$6.90 per
>    recipient) and Cohen's d ≈ 0.31, the team rolls out variant B.
> 5. **Caveat** — one campaign is one sample. Rerun on the next send to confirm
>    the effect is not a one-off.

---

## 18. One-Page Cheat Sheet

```
PURPOSE   Compare the MEANS of two INDEPENDENT groups.

HYPO      H0: mu_A = mu_B            (two-sided)
          H1: mu_A != mu_B
          or  H1: mu_B > mu_A        (one-sided, decide BEFORE the test)

FORMULA              (x̄_B − x̄_A) − 0          signal
          t  =  ─────────────────────────  =  ──────────
          ␣␣␣␣␣␣ SE(x̄_B − x̄_A)               noise

          SE = sqrt( s²_B/n_B + s²_A/n_A )      <- Welch (default)
          df = Welch–Satterthwaite formula
          (pooled version: s_p·sqrt(1/n_B + 1/n_A), df = n_A + n_B − 2)

CRITICAL  t_crit = stats.t.ppf(1 − alpha/2, df)     two-sided
VALUE     t_crit = stats.t.ppf(1 − alpha,   df)     one-sided

DECIDE    |t| > t_crit   (or  p < alpha)  ->  REJECT H0
          |t| <= t_crit  (or  p >= alpha) ->  FAIL TO REJECT H0

EFFECT    diff = x̄_B − x̄_A
          CI   = diff ± t_crit × SE      (no 0 in CI  <=>  significant)
          d    = diff / s_pooled         (0.2 small, 0.5 medium, 0.8 large)

PYTHON
          from scipy import stats
          t, p = stats.ttest_ind(group_B, group_A, equal_var=False)
          t_crit = stats.t.ppf(0.975, df)
          shapiro = stats.shapiro(group_A)              # normality
          levene  = stats.levene(group_A, group_B, center="median")  # equal var

CHECK     Independence (design) · Normality (Q-Q, Shapiro) ·
          Equal variance (Levene -> if p < .05 use Welch) · Outliers (boxplot)
```

---

## 19. Practice Exercises

1. **Swap the argument order.** Run `stats.ttest_ind(group_A, group_B, equal_var=False)`
   and confirm the t-statistic flips sign and the two-sided p-value does not change.
   Then run a one-sided test both ways and explain why the p-values differ.

2. **Change α.** Rerun the analysis with α = 0.01 and α = 0.10. Does the decision
   change? Replot Figure 1 for each α and observe how the red regions move.

3. **Starve the data.** Set `n_A = n_B = 8` and rerun. How do the critical value,
   the width of the confidence interval, and the p-value change? Why?

4. **Break the assumption.** Generate `group_B` from an exponential distribution.
   Compare the Welch t-test, the Mann–Whitney U test, and a bootstrap CI. Which
   agrees best with the others?

5. **Quantify the business.** Assume 500,000 monthly visitors and a 3% margin
   improvement threshold. Using the confidence interval, argue for or against
   shipping the new page.

6. **Add a third variant.** Simulate a group C and explain why you now need ANOVA
   plus a post-hoc test rather than three t-tests.

---

### Final thoughts

The independent samples t-test is one of the most-used tools in applied data
science, and it is essentially three ideas stacked together:

1. **Signal ÷ noise.** The t-statistic measures the difference in means in units
   of the noise that randomness alone would create.
2. **A pre-declared line.** The critical value, fixed by α and the degrees of
   freedom, defines how much evidence counts as "enough."
3. **A decision with a size attached.** Rejecting H₀ tells you an effect is
   probably non-zero; the confidence interval and Cohen's d tell you whether
   anyone should care.

Master those three ideas, and every more advanced test — ANOVA, regression,
mixed models — becomes a variation on a familiar theme.

```

**How to save it**

- Copy everything from `# Hypothesis Testing: The Independent Samples T-Test in Python` down to the end, paste it into a new file, and save it as `independent_samples_t_test.md`.
- Or, in a terminal: `pbpaste > independent_samples_t_test.md` (macOS) / use any editor's "Save As".
- Run the Python script in Section 10 to produce the six `.png` figures referenced in Section 11 — the filenames in `plt.savefig(...)` match the figure numbers, so the images and the explanations line up directly.
```
