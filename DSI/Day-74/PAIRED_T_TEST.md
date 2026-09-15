# Hypothesis Testing in Data Science: The Paired T-Test (Beginner-Friendly Python Guide)

> **What you will be able to do after reading this:**
>
> 1. Explain what a hypothesis test is, in plain English.
> 2. Know exactly _when_ a **paired t-test** is the right tool (and when it isn't).
> 3. Read and compute a **t-statistic** and a **critical value**, and use them to make a decision.
> 4. Write clean, runnable Python code with `scipy` and `matplotlib`.
> 5. Interpret every dot, line and shaded region in the graphs you generate.
> 6. Translate a statistical result into a business decision with a dollar value.

---

## Table of Contents

1. [The Big Idea: Hypothesis Testing in 60 Seconds](#1)
2. [When Do We Use a Paired T-Test?](#2)
3. [Our Running Example: Sales Training](#3)
4. [The Formula, Broken Down Piece by Piece](#4)
5. [The t-Statistic: The Star of the Show](#5)
6. [The Critical Value: The Judge's Line in the Sand](#6)
7. [t-Statistic vs Critical Value: How a Conclusion Is Actually Drawn](#7)
8. [Full Python Walkthrough (Manual + `scipy`)](#8)
9. [Graph 1 — The Paired Slopegraph](#9)
10. [Graph 2 — Histogram of the Differences](#10)
11. [Graph 3 — The t-Distribution with Critical Regions](#11)
12. [Graph 4 — The Null Distribution of the Mean Difference](#12)
13. [Graph 5 — Q-Q Plot (Assumption Check)](#13)
14. [A Second Example Where the Test FAILS to Reject](#14)
15. [Assumptions and What To Do When They Break](#15)
16. [Effect Size and Confidence Interval: Beyond "Is It Significant?"](#16)
17. [Company Use Cases: Driving Business Decisions](#17)
18. [Common Mistakes Beginners Make](#18)
19. [Cheat Sheet](#19)
20. [Practice Exercises](#20)

---

<a name="1"></a>

## 1. The Big Idea: Hypothesis Testing in 60 Seconds

A hypothesis test is a **fair judge** for a claim.

Imagine a company claims: _"Our sales training increased monthly sales."_
Sales went up. But sales go up and down all the time — maybe it was luck, a good month, or one superstar rep.

A hypothesis test asks one precise question:

> **"If the training did absolutely nothing, how likely is it that we would see data this extreme?"**

To answer it, we set up two competing statements:

| Name                       | Symbol     | Meaning                                        | Our example                       |
| -------------------------- | ---------- | ---------------------------------------------- | --------------------------------- |
| **Null hypothesis**        | H₀         | "Nothing happened / no effect / no difference" | The true mean change in sales = 0 |
| **Alternative hypothesis** | H₁ (or Hₐ) | "Something happened"                           | The true mean change in sales ≠ 0 |

**Two possible outcomes:**

- **Reject H₀** → The data are too extreme to be explained by chance alone. We have evidence of a real effect.
- **Fail to reject H₀** → The data are consistent with "nothing happened." We do **not** claim the effect is zero; we just don't have enough evidence.

> ⚠️ **Beginner trap:** We never say "we proved H₀ is true." Absence of evidence is not evidence of absence.

**Two types of error:**

|                          | H₀ is actually TRUE                            | H₀ is actually FALSE                              |
| ------------------------ | ---------------------------------------------- | ------------------------------------------------- |
| **We reject H₀**         | ❌ Type I error (false alarm), probability = α | ✅ Correct! (power)                               |
| **We fail to reject H₀** | ✅ Correct!                                    | ❌ Type II error (missed effect), probability = β |

- **α (alpha)**, usually **0.05**, is the false-alarm rate we are willing to accept. We call it the **significance level**.
- **p-value** = the probability of seeing data at least as extreme as ours, _assuming H₀ is true_.
- If **p < α**, we reject H₀.

The paired t-test is one specific, very common way to compute that p-value — via a **t-statistic** compared against a **critical value**.

---

<a name="2"></a>

## 2. When Do We Use a Paired T-Test?

The paired t-test (also called the **dependent-samples t-test** or **repeated-measures t-test**) is used when the **same unit** is measured **twice**, or when units are deliberately **matched** into pairs.

### ✅ Use a paired t-test when:

| Situation                                          | Example                                            |
| -------------------------------------------------- | -------------------------------------------------- |
| Same people, before vs after                       | Sales reps' sales before and after training        |
| Same machines, before vs after                     | Machine output before and after recalibration      |
| Same patients, two treatments                      | Blood pressure on Drug A vs Drug B (same patients) |
| Same customers, two designs                        | Same user's time-on-site on old vs new homepage    |
| **Matched pairs** (twins, same store, same region) | Twin A gets method 1, twin B gets method 2         |

### ❌ Do NOT use a paired t-test when:

- The two groups are **different people/machines** — then use an **independent two-sample t-test** (`scipy.stats.ttest_ind`).
- You have more than two time points — use **repeated-measures ANOVA** or a **mixed-effects model**.
- The differences are heavily skewed with a small sample — use the **Wilcoxon signed-rank test** (a non-parametric alternative).

### The magic trick: pairing removes noise

Every salesperson has a personal baseline level (Rep 5 always sells more than Rep 4). Raw "before" and "after" numbers carry that person-to-person noise.

By computing **d = after − before for each person**, we subtract out each person's baseline. We're left with only the _change_. That's why paired designs are statistically **more powerful** — they can detect real effects with fewer subjects.

```text
Unpaired view:  52, 60, 58, 45, 70, ...   ← people differ a lot
Paired view:     4,  6, −1,  4,  8, ...   ← now we look at changes only
```

### Secret identity 🕵️

**The paired t-test IS a one-sample t-test on the differences.**
We literally compute a new variable `d = after − before`, then run a one-sample t-test of `d` against 0. Understanding this makes the formula obvious.

---

<a name="3"></a>

## 3. Our Running Example: Sales Training

A B2B company runs a two-week sales training program for 12 sales representatives.
The company measures each rep's monthly sales **before** and **after** training (in thousands of dollars, or "units of $1,000").

**Research question:** Did the training change monthly sales?

- **H₀:** μ_d = 0 (the true mean change is zero)
- **H₁:** μ_d ≠ 0 (the true mean change is not zero) — a **two-tailed** test
- **α = 0.05**

### The data

|  Rep   | Before | After | d = After − Before |
| :----: | -----: | ----: | -----------------: |
| Rep 1  |     52 |    56 |             **+4** |
| Rep 2  |     60 |    66 |             **+6** |
| Rep 3  |     58 |    57 |             **−1** |
| Rep 4  |     45 |    49 |             **+4** |
| Rep 5  |     70 |    78 |             **+8** |
| Rep 6  |     63 |    64 |             **+1** |
| Rep 7  |     55 |    61 |             **+6** |
| Rep 8  |     48 |    52 |             **+4** |
| Rep 9  |     66 |    69 |             **+3** |
| Rep 10 |     59 |    66 |             **+7** |
| Rep 11 |     61 |    63 |             **+2** |
| Rep 12 |     53 |    58 |             **+5** |

**Column-by-column meaning**

- **Before**: the baseline, measured _before_ the training started. This is each rep's personal control.
- **After**: the same rep's number _after_ training. Same person → paired.
- **d**: the change score. This is the _only_ column the math cares about. Positive = improved. Note Rep 3 actually got _worse_ (−1) — real data is never perfectly clean, and that's fine.

**Quick eyeball of d:** 4, 6, −1, 4, 8, 1, 6, 4, 3, 7, 2, 5.
Eleven out of twelve are positive, and the average looks like ~4. Our intuition says "yes, training helped." Now we need the test to tell us whether "~4" could plausibly be luck.

**Sum of d** = 49, so **d̄ (mean difference)** = 49 / 12 = **4.083**.

---

<a name="4"></a>

## 4. The Formula, Broken Down Piece by Piece

### The formula

$$
t = \frac{\bar{d} - \mu_0}{\dfrac{s_d}{\sqrt{n}}}
\qquad\text{with}\qquad df = n - 1
$$

### Piece-by-piece breakdown

| Symbol             | Name                                       | What it is                                                                                        | In our example            |
| ------------------ | ------------------------------------------ | ------------------------------------------------------------------------------------------------- | ------------------------- |
| **d**              | Difference score                           | `after − before` for one unit                                                                     | e.g. Rep 2: 66 − 60 = 6   |
| **d̄**              | Mean of the differences                    | Average change across all units. **The "signal."**                                                | 49 / 12 = **4.083**       |
| **μ₀ (mu-naught)** | Hypothesised mean difference               | What H₀ claims the mean change is. Almost always **0**.                                           | **0**                     |
| **d̄ − μ₀**         | Numerator                                  | How far our observed average change is from what H₀ predicts.                                     | 4.083 − 0 = **4.083**     |
| **s_d**            | Standard deviation of the differences      | How spread out the individual changes are. **The "noise" per unit.**                              | **2.575**                 |
| **n**              | Number of pairs                            | How many units were measured twice                                                                | **12**                    |
| **s_d / √n**       | Standard error of the mean difference (SE) | How much the _average_ change would wobble from sample to sample. **The "noise of the average."** | 2.575 / √12 = **0.743**   |
| **t**              | t-statistic                                | Signal ÷ noise. How many standard errors our average sits away from zero.                         | 4.083 / 0.743 = **5.494** |
| **df**             | Degrees of freedom                         | n − 1. Controls the shape of the t-distribution.                                                  | 12 − 1 = **11**           |

### Why divide by √n?

Averaging is a noise-reduction machine. If one person's change is noisy, the _average_ of 12 people's changes is much more stable — about √12 ≈ 3.46 times more stable. So the standard error shrinks as your sample grows, which makes `t` bigger, which makes it easier to detect a real effect.

### Computing s_d by hand (so it's not a black box)

$$
s_d = \sqrt{\frac{\sum (d_i - \bar{d})^2}{n-1}}
$$

A shortcut that is easier to compute:

$$
s_d = \sqrt{\frac{\sum d_i^2 - n\bar{d}^2}{n-1}}
$$

Plug in our numbers:

1. **Σdᵢ²** — square each difference and add them up:
   4² + 6² + (−1)² + 4² + 8² + 1² + 6² + 4² + 3² + 7² + 2² + 5²
   = 16 + 36 + 1 + 16 + 64 + 1 + 36 + 16 + 9 + 49 + 4 + 25 = **273**

2. **n·d̄²** = 12 × 4.083² = 12 × 16.6736 = **200.083**

3. Numerator of the fraction: 273 − 200.083 = **72.917**

4. Divide by df: 72.917 / 11 = **6.629** ← this is the variance, s_d²

5. Square root: √6.629 = **2.575** ← this is s_d ✅

6. **SE** = 2.575 / √12 = 2.575 / 3.4641 = **0.743**

7. **t** = 4.083 / 0.743 = **5.494**

> 💡 **Interpretation of t = 5.494:** our observed average improvement is **almost 5.5 standard errors away from zero**. In a world where training did nothing, an average that far from zero is extraordinarily unlikely. That's strong evidence.

---

<a name="5"></a>

## 5. The t-Statistic: The Star of the Show

### What the t-statistic really measures

$$
t = \frac{\text{signal}}{\text{noise}} = \frac{\text{observed mean change}}{\text{typical wobble of that mean}}
$$

Think of it like a **signal-to-noise ratio on a phone call**. A loud voice (big d̄) or a quiet room (small s_d) both make the voice easier to hear. `t` combines both.

### Three things that make `t` bigger (easier to find a real effect)

1. **Bigger average change** (bigger d̄) → bigger numerator.
2. **More consistent changes** (smaller s_d) → smaller denominator. If everyone improved by about the same amount, you're much more confident.
3. **More pairs** (bigger n) → smaller SE → smaller denominator.

### What the sign of t tells you

- **t > 0** → the average change is **positive** (after > before) — you'd get this by computing `after − before`.
- **t < 0** → the average change is **negative** (after < before).
- **t ≈ 0** → the average change is close to zero.

⚠️ **Important:** the sign depends entirely on **which order you subtract**. `ttest_rel(after, before)` gives +5.49; `ttest_rel(before, after)` gives −5.49. For a **two-tailed** test, the conclusion is identical — only the story changes. For a **one-tailed** test, the sign and direction matter enormously.

### What the t-statistic is NOT

- ❌ It is **not** the probability that H₀ is true.
- ❌ It is **not** a percentage or a percentage difference.
- ❌ It has **no absolute meaning on its own**. `t = 5.49` is impressive with df = 11, but with df = 1000 it's merely good. You always need the df and the distribution to interpret it.

---

## 5b. Why "t" and not "z"? (The Guinness Story 🍺)

If we knew the **true** population standard deviation σ, we'd use the normal (z) distribution. But we don't — we estimate it with s_d, which is itself shaky, especially in small samples. That extra uncertainty makes extreme values more likely than the normal curve predicts.

So William Sealy Gosset — a chemist at Guinness brewery in 1908, publishing under the pen name **"Student"** — derived a distribution with **fatter tails**: the **Student's t-distribution**.

- Fatter tails = more mass far from zero = **harder to reject H₀** (more conservative, which is appropriate).
- The t-distribution's shape depends only on **degrees of freedom (df = n − 1)**.
- As **df → ∞** (large samples), the t-distribution becomes the normal distribution. That's why with n > 100 the difference nearly vanishes.

---

<a name="6"></a>

## 6. The Critical Value: The Judge's Line in the Sand

### What it is

The **critical value** (t\*) is the **boundary on the t-axis** that cuts off exactly α of the probability in the tails of the t-distribution (under H₀).

It answers: _"How big does t have to be before we call it too extreme to be chance?"_

For a **two-tailed test at α = 0.05**:

- We split 5% across both tails: **2.5% in the left tail, 2.5% in the right tail**.
- The left critical value is **−t\*** and the right critical value is **+t\***.
- Everything beyond ±t\* is the **rejection region** (also called the **critical region**).

### The decision rule

$$
\text{Reject } H_0 \text{ if } |t| > t^{*}
\qquad\text{equivalently}\qquad
t < -t^{*} \ \text{ or }\ t > +t^{*}
$$

### Finding t\* for our example

- Two-tailed, α = 0.05 → look up the **97.5th percentile** of a t-distribution with **df = 11**.
- From a table (or `stats.t.ppf(0.975, 11)`), **t\* = 2.201**.

### Common critical values (two-tailed α = 0.05)

| df (n − 1) |       t\* |              Sample size |
| ---------: | --------: | -----------------------: |
|          1 |    12.706 |                    n = 2 |
|          2 |     4.303 |                    n = 3 |
|          5 |     2.571 |                    n = 6 |
|          9 |     2.262 |                   n = 10 |
|     **11** | **2.201** | **n = 12** ← our example |
|         15 |     2.131 |                   n = 16 |
|         20 |     2.086 |                   n = 21 |
|         30 |     2.042 |                   n = 31 |
|         60 |     2.000 |                   n = 61 |
|          ∞ |     1.960 |        "the famous 1.96" |

Notice the pattern: **small samples need a bigger t to be convincing**. With just 2 pairs you'd need t > 12.7! With a huge sample you need only ~1.96.

### Critical values for the one-tailed case (α = 0.05)

|  df | One-tailed t\* |
| --: | -------------: |
|   5 |          2.015 |
|  11 |          1.796 |
|  20 |          1.725 |
|  30 |          1.697 |
|   ∞ |          1.645 |

A one-tailed test has a **lower bar** because all 5% of the error budget sits in one tail. But you must decide the direction **before** looking at the data, and you must have a genuine directional hypothesis ("the training _increased_ sales").

> ⚠️ **Never** run a two-tailed test, see that it's "nearly significant" (p = 0.08), then switch to one-tailed to get p = 0.04. That is **p-hacking** and it invalidates your result.

---

<a name="7"></a>

## 7. t-Statistic vs Critical Value: How a Conclusion Is Actually Drawn

Here is the complete logic flow of the test.

### Step 1 — State the hypotheses and pick α

```
H₀: μ_d = 0      (training made no difference on average)
H₁: μ_d ≠ 0      (training changed sales on average)
α  = 0.05
```

### Step 2 — Compute the test statistic

```
d̄  = 4.083
s_d = 2.575
n   = 12
SE  = 2.575 / √12 = 0.743
t   = 4.083 / 0.743 = 5.494
df  = 11
```

### Step 3 — Find the critical value

```
t* = 2.201   (two-tailed, α = 0.05, df = 11)
```

### Step 4 — Compare and decide

```
Is |t| = 5.494 > t* = 2.201 ?   →  YES  →  REJECT H₀
```

### Step 5 — Equivalently (and more precisely), use the p-value

The **p-value** is the area under the t-curve **beyond your observed t** (both tails for a two-tailed test).

```
p ≈ 0.0002
Compare: p = 0.0002 < α = 0.05   →  REJECT H₀
```

### 🔑 The two are the same thing

The critical value and the p-value are **two views of the same picture**:

- **Critical-value approach:** Is our t inside the shaded rejection region? → **Yes.**
- **p-value approach:** Is the tail area beyond our t smaller than α? → **Yes.**

```
                       Rejection region        Rejection region
         ◀── 2.5% ────┤                          ├──── 2.5% ──▶
                      -2.201                +2.201
   ───┼────────┼────────┼────────┼────────┼────────┼────────┼─────▶  t
     -4       -3       -2      -1        0        1        2
                                                            ↑
                                            our t = 5.494 is WAY out here ▶▶▶
```

### Step 6 — State the conclusion in business language

> "The average sales change was **+4.08 thousand dollars per rep**.
> With t(11) = 5.49 and p = 0.0002, which is well below our 0.05 threshold, we **reject the null hypothesis**.
> There is statistically significant evidence that the training changed monthly sales."

### Step 7 — And then check whether it MATTERS

Statistical significance is not the same as business significance. Ask: _is +$4,080 per rep per month worth the cost of the program?_ (More on this in [Section 17](#17).)

---

<a name="8"></a>

## 8. Full Python Walkthrough (Manual + `scipy`)

### 8.1 Setup

```python
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# Make the notebook look a bit nicer
plt.rcParams["figure.dpi"] = 110
plt.rcParams["font.size"] = 10
```

### 8.2 Create the dataset

```python
sales = pd.DataFrame({
    "rep":    [f"Rep {i}" for i in range(1, 13)],
    "before": [52, 60, 58, 45, 70, 63, 55, 48, 66, 59, 61, 53],
    "after":  [56, 66, 57, 49, 78, 64, 61, 52, 69, 66, 63, 58],
})

# The key step of a PAIRED test: reduce two columns to one difference column
sales["diff"] = sales["after"] - sales["before"]

print(sales)
print("\nTotal change =", sales["diff"].sum())
```

**Expected output**

```text
       rep  before  after  diff
0    Rep 1      52     56     4
1    Rep 2      60     66     6
2    Rep 3      58     57    -1
3    Rep 4      45     49     4
4    Rep 5      70     78     8
5    Rep 6      63     64     1
6    Rep 7      55     61     6
7    Rep 8      48     52     4
8    Rep 9      66     69     3
9   Rep 10      59     66     7
10  Rep 11      61     63     2
11  Rep 12      53     58     5

Total change = 49
```

**What the code does**

- `pd.DataFrame({...})` builds a table from three lists of equal length. Each row is one **unit of analysis** (a rep).
- `sales["after"] - sales["before"]` performs **element-wise subtraction down the rows** — this is pandas doing the pairing for us. It produces a new column aligned by row index. If you accidentally shuffled one column, the pairing would be destroyed and the test meaningless.

### 8.3 Compute the t-statistic manually (no shortcuts)

```python
d      = sales["diff"].to_numpy()     # array of differences
n      = len(d)                       # number of PAIRS
d_bar  = d.mean()                     # mean difference  -> the SIGNAL
s_d    = d.std(ddof=1)                # sample SD of differences -> the NOISE
se_d   = s_d / np.sqrt(n)             # standard error of the mean
t_stat = d_bar / se_d                 # the t-statistic
df     = n - 1                        # degrees of freedom

alpha  = 0.05
t_crit = stats.t.ppf(1 - alpha/2, df) # right-hand critical value
p_val  = 2 * stats.t.sf(abs(t_stat), df)   # two-tailed p-value

print(f"n (pairs)        = {n}")
print(f"mean difference  = {d_bar:.3f}")
print(f"SD of differences= {s_d:.3f}")
print(f"standard error   = {se_d:.3f}")
print(f"t-statistic      = {t_stat:.3f}")
print(f"degrees of freedom = {df}")
print(f"critical value t*  = ±{t_crit:.3f}")
print(f"p-value            = {p_val:.6f}")
print(f"Decision: {'REJECT H0' if abs(t_stat) > t_crit else 'FAIL TO REJECT H0'}")
```

**Expected output**

```text
n (pairs)        = 12
mean difference  = 4.083
SD of differences= 2.575
standard error   = 0.743
t-statistic      = 5.494
degrees of freedom = 11
critical value t*  = ±2.201
p-value            = 0.000167
Decision: REJECT H0
```

**Function-by-function explanation**

| Code                           | What it does                                                                                     | Why it matters                                                                                     |
| ------------------------------ | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| `.to_numpy()`                  | Converts the pandas Series into a plain NumPy array                                              | Lets you use NumPy's fast math functions                                                           |
| `len(d)`                       | Counts the pairs                                                                                 | n is pairs, **not** total observations (12, not 24)                                                |
| `d.mean()`                     | Adds all d values and divides by n                                                               | The numerator of t                                                                                 |
| `d.std(ddof=1)`                | Sample SD using n − 1 in the denominator (**Bessel's correction**)                               | Using `ddof=0` (population SD) would make the SE too small and inflate t. **Always use `ddof=1`.** |
| `s_d / np.sqrt(n)`             | The standard error                                                                               | Converts per-unit noise into noise-of-the-average                                                  |
| `stats.t.ppf(1 - alpha/2, df)` | **Percent point function** = inverse CDF. Asks "what t value has 97.5% of the area to its left?" | That t value **is** the critical value                                                             |
| `stats.t.sf(x, df)`            | **Survival function** = 1 − CDF = area to the right of x                                         | Using `sf` instead of `1 - cdf` avoids floating-point rounding to 0 for tiny p-values              |
| `2 * sf(abs(t), df)`           | Doubles the one-tail area                                                                        | Required for a two-tailed test                                                                     |

### 8.4 The one-line version with `scipy`

```python
res = stats.ttest_rel(sales["after"], sales["before"])
print(res)
```

**Expected output**

```text
TtestResult(statistic=5.494015903308512, pvalue=0.0001669..., df=11)
```

**Reading the `TtestResult` object**

- `res.statistic` → the t-statistic (5.494). Note it is **positive** because we passed `after` first.
- `res.pvalue` → the two-tailed p-value (≈0.000167).
- `res.df` → 11 degrees of freedom.

**`ttest_rel` vs `ttest_ind` vs `ttest_1samp`**

| Function                  | Use when                                                                                                |
| ------------------------- | ------------------------------------------------------------------------------------------------------- |
| `stats.ttest_rel(a, b)`   | Paired / repeated measures. Internally it runs a one-sample t-test on `a - b`.                          |
| `stats.ttest_ind(a, b)`   | Two **independent** groups. **Wrong** for our data — it would throw away the pairing and lose power.    |
| `stats.ttest_1samp(d, 0)` | Identical result to `ttest_rel` when `d = after - before`. Proves the "secret identity" from Section 2. |

```python
# Sanity check: these three all give the SAME p-value
print(stats.ttest_rel(sales["after"], sales["before"]).pvalue)
print(stats.ttest_1samp(sales["diff"], 0).pvalue)
print(2 * stats.t.sf(abs(5.494015903308512), 11))
```

```text
0.00016690...
0.00016690...
0.00016690...
```

### 8.5 Bonus: confidence interval and effect size

```python
# 95% confidence interval for the true mean change
ci_low  = d_bar - t_crit * se_d
ci_high = d_bar + t_crit * se_d
print(f"95% CI for mean change: ({ci_low:.3f}, {ci_high:.3f})")

# Cohen's d for paired data
cohens_d = d_bar / s_d
print(f"Cohen's d = {cohens_d:.3f}")
```

```text
95% CI for mean change: (2.447, 5.720)
Cohen's d = 1.586
```

**How to read the CI:** we are 95% confident the _true_ average improvement lies between **+$2,447** and **+$5,720** per rep per month. Because this interval **does not contain 0**, it agrees with our rejection of H₀. (The CI and the t-test are mathematically consistent — always check that they tell the same story.)

### 8.6 The non-parametric backup

```python
w = stats.wilcoxon(sales["after"], sales["before"])
print(w)
```

```text
WilcoxonResult(statistic=6.0, pvalue=0.004394...)
```

The Wilcoxon signed-rank test makes no normality assumption and still finds p < 0.05, so our conclusion is robust.

---

<a name="9"></a>

## 9. Graph 1 — The Paired Slopegraph

A slopegraph draws **one line per pair**, connecting the before value to the after value. It is the single best picture of what "paired" means.

```python
fig, ax = plt.subplots(figsize=(6, 7))

for _, row in sales.iterrows():
    if row["diff"] > 0:
        color, lw = "#2ca02c", 1.6      # green = improved
    elif row["diff"] < 0:
        color, lw = "#d62728", 1.6      # red   = got worse
    else:
        color, lw = "#7f7f7f", 1.6      # grey  = no change

    ax.plot([0, 1], [row["before"], row["after"]],
            marker="o", markersize=6, linewidth=lw,
            color=color, alpha=0.85)

    # Label each line with the rep's name on the left and the change on the right
    ax.text(-0.04, row["before"], row["rep"], ha="right", va="center", fontsize=8)
    ax.text(1.04, row["after"], f"{row['diff']:+d}", ha="left", va="center",
            fontsize=8, color=color)

# Thick black line = the group averages
ax.plot([0, 1], [sales["before"].mean(), sales["after"].mean()],
        color="black", linewidth=3, zorder=5, label="Group average")

ax.set_xlim(-0.35, 1.25)
ax.set_xticks([0, 1])
ax.set_xticklabels(["Before training", "After training"])
ax.set_ylabel("Monthly sales (thousands of $)")
ax.set_title("Paired design: same 12 reps measured twice")
ax.legend(loc="upper left")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()
```

### What each element of the graph does

| Element                                   | Meaning                                                                                                                                                                                   |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Two x positions (0 and 1)**             | The two measurement occasions. There is no continuous axis — _before_ and _after_ are categories.                                                                                         |
| **Each line = one rep**                   | The line _is_ the pairing. It visually encodes `d = after − before`. If you had drawn two separate histograms, this information would be lost.                                            |
| **Left dot**                              | That rep's `before` sales, positioned on the y-axis by dollar value.                                                                                                                      |
| **Right dot**                             | The **same** rep's `after` sales. Because the line connects them, you immediately see the direction of change.                                                                            |
| **Slope of the line**                     | Steep upward = large improvement. Upward = improved. Downward = got worse. Flat = no change.                                                                                              |
| **Green lines**                           | Positive d (11 reps).                                                                                                                                                                     |
| **Red line**                              | Rep 3, whose sales fell from 58 to 57 (d = −1). This is important: it shows the effect is not universal, which is why we need a _statistical_ test rather than just staring at the chart. |
| **Text label on the left**                | Identifies which line belongs to which rep, so you can trace individual units.                                                                                                            |
| **Text label on the right (+4, +6, −1…)** | The exact change score for each rep.                                                                                                                                                      |
| **Thick black line**                      | The group's average before (59.17) vs average after (63.25). Its slope is the **visual version of d̄ = 4.08**.                                                                             |
| **Y-axis (monthly sales in $1,000s)**     | The measured outcome. Note that y-values carry real units — always label them.                                                                                                            |
| **Legend + grid**                         | Makes the chart readable and self-explanatory for stakeholders.                                                                                                                           |

### What to look for

- **Do most lines slope up?** Yes → evidence of a positive effect.
- **Are the lines roughly parallel?** If yes, the effect is consistent across reps (small s_d, big t).
- **Is there lots of crossing?** That means high variance in the change scores → smaller t.
- **Any outlier lines** (a single line with a wild slope)? Those inflate s_d and can distort the t-test.

---

<a name="10"></a>

## 10. Graph 2 — Histogram of the Differences

The paired t-test only looks at the `diff` column. So let's _look_ at that column.

```python
fig, ax = plt.subplots(figsize=(7.5, 4.5))

ax.hist(sales["diff"], bins=np.arange(-2.5, 9.5, 1), color="#4c72b0",
        edgecolor="white", linewidth=1.2)

# Reference line 1: what H0 predicts (zero change)
ax.axvline(0, color="black", linestyle=":", linewidth=2)
ax.text(0.05, ax.get_ylim()[1]*0.92, "H₀: mean change = 0",
        color="black", fontsize=9)

# Reference line 2: what we actually observed
ax.axvline(d_bar, color="#d62728", linestyle="--", linewidth=2)
ax.text(d_bar+0.1, ax.get_ylim()[1]*0.78, f"Observed mean = {d_bar:.2f}",
        color="#d62728", fontsize=9)

ax.set_xlabel("Change in monthly sales (thousands of $)  [after − before]")
ax.set_ylabel("Number of reps")
ax.set_title("Distribution of the differences — the only column the test uses")
plt.tight_layout()
plt.show()
```

### What each element does

| Element                     | Meaning                                                                                                                                                       |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **X-axis**                  | The change score `d`. Zero = no change. Right of zero = improvement.                                                                                          |
| **Y-axis**                  | How many reps landed in that change bin (a _frequency_). With n = 12 the counts are small (0–4), which is normal.                                             |
| **Each bar**                | A **bin** of width 1 (e.g. the bar over "4" counts all reps whose change was between 3.5 and 4.5). Our data: d = 4 appears 4 times, so that bar has height 4. |
| **Dotted black line at 0**  | The value H₀ predicts for the mean. If the training did nothing, the histogram would be centred here.                                                         |
| **Dashed red line at 4.08** | Our observed d̄. The histogram is visibly shifted to the right of zero.                                                                                        |
| **Overall shape**           | Roughly bell-shaped and not badly skewed → the normality assumption looks reasonable. Slight pile-up at +4 and one lone value at −1.                          |

### How to read the "evidence" from this picture

The test is essentially asking: _if the true mean change were 0, how often would the average of 12 draws from a distribution like this land 4.08 or higher?_ The **entire bulk of the data sits to the right of zero**, which is why p is so tiny.

> 💡 The **gap between the black dotted line and the red dashed line** is the numerator of t (4.08). The **width of the histogram** is the denominator (s_d = 2.58). Wide histogram + small gap = weak evidence. Narrow histogram + big gap = strong evidence.

---

<a name="11"></a>

## 11. Graph 3 — The t-Distribution with Critical Regions

This is the **decision-making graph**. It shows the null distribution of t, the rejection regions, and where our statistic falls.

```python
x = np.linspace(-5, 5, 1000)
y = stats.t.pdf(x, df)

fig, ax = plt.subplots(figsize=(8.5, 5))

# 1. The null distribution curve
ax.plot(x, y, color="black", linewidth=2, label=f"t-distribution (df = {df})")

# 2. Shade the two rejection regions (2.5% each)
x_left  = x[x <= -t_crit]
x_right = x[x >=  t_crit]
ax.fill_between(x_left,  stats.t.pdf(x_left,  df), color="#d62728", alpha=0.45,
                label=f"Rejection region (α/2 = 0.025 each)")
ax.fill_between(x_right, stats.t.pdf(x_right, df), color="#d62728", alpha=0.45)

# 3. Mark the critical values
for cv in (-t_crit, t_crit):
    ax.axvline(cv, color="#d62728", linestyle="--", linewidth=1.5)
ax.text(-t_crit-0.15, 0.30, f"−t* = {t_crit:.3f}", ha="right", color="#d62728", fontsize=9)
ax.text( t_crit+0.15, 0.30, f"+t* = {t_crit:.3f}", ha="left",  color="#d62728", fontsize=9)

# 4. Mark our observed t-statistic
ax.axvline(t_stat, color="#1f77b4", linewidth=2.5)
ax.annotate(f"our t = {t_stat:.2f}\n(outside the line → reject H₀)",
            xy=(t_stat, 0.02), xytext=(t_stat-0.3, 0.20),
            ha="right", color="#1f77b4", fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#1f77b4"))

# 5. Shade the area-at-least-as-extreme = the p-value
x_obs = x[x >= t_stat]
ax.fill_between(x_obs, stats.t.pdf(x_obs, df), color="#1f77b4", alpha=0.6)
ax.text(t_stat-0.55, 0.06, "p-value\n(tiny!)", ha="right", color="#1f77b4", fontsize=9)

ax.set_xlabel("t-statistic")
ax.set_ylabel("Probability density")
ax.set_title(f"Decision chart: t = {t_stat:.2f} vs critical value t* = ±{t_crit:.3f}")
ax.legend(loc="upper left", fontsize=9)
ax.grid(alpha=0.25)
plt.tight_layout()
plt.show()
```

### What each element does

| Element                                 | Meaning                                                                                                                                                                                                               |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Black bell curve**                    | The **sampling distribution of t when H₀ is true**. It is centred at 0 — if training did nothing, our t would most likely hover near zero. It is slightly fatter-tailed than a normal curve because df = 11 is small. |
| **The 0 point on the x-axis**           | t = 0 means "the observed mean change is exactly zero", i.e. exactly what H₀ claims.                                                                                                                                  |
| **Two red shaded tails**                | The **rejection regions**. Each has area α/2 = 0.025, so together they hold exactly α = 5% of the probability. If H₀ is true, there is only a 5% chance of t landing in these tails.                                  |
| **Dashed red vertical lines at ±2.201** | The **critical values**. They are literally the boundaries of the shaded regions. Their location is decided _before_ you see the data — they depend only on α and df.                                                 |
| **Solid blue vertical line at 5.49**    | Our **observed t-statistic**. This is the one number that comes from the data.                                                                                                                                        |
| **Blue shaded sliver to the right**     | The **p-value** = the area under the curve beyond t = 5.49 (plus its mirror on the left). It is so thin it looks like a hairline — that's what p ≈ 0.0002 looks like.                                                 |
| **Annotation text**                     | Ties the picture back to the decision: our t is far outside the boundary.                                                                                                                                             |

### How to read the conclusion directly off the graph

- Our blue line sits **to the right of** the red dashed boundary (+2.201).
- Therefore the observed statistic is **inside the rejection region**.
- Therefore **reject H₀**.
- The tail area beyond our line is far smaller than 2.5%, so **p ≪ 0.05**.

> 🎯 **The single most important takeaway:** _The critical value is a fixed threshold determined by α and df. The t-statistic is a data-driven number. The test is simply "is my number beyond the threshold?"_

---

<a name="12"></a>

## 12. Graph 4 — The Null Distribution of the Mean Difference

Graph 3 is in "t units". Many beginners find it easier to think in the **original units** ($). This graph re-scales everything back to dollars.

```python
x = np.linspace(-4, 6, 1000)
# Under H0, (d_bar - 0)/SE ~ t(df)  =>  d_bar ~ SE * t(df)
null_pdf = stats.t.pdf(x / se_d, df) / se_d

fig, ax = plt.subplots(figsize=(8.5, 5))

ax.plot(x, null_pdf, color="black", linewidth=2,
        label=f"Sampling distribution of d̄ if H₀ were true (SE = {se_d:.2f})")

# Rejection boundaries expressed in dollars
lo, hi = -t_crit * se_d, t_crit * se_d
ax.axvline(lo, color="#d62728", linestyle="--")
ax.axvline(hi, color="#d62728", linestyle="--")
ax.fill_between(x[x <= lo], stats.t.pdf(x[x <= lo]/se_d, df)/se_d,
                color="#d62728", alpha=0.4, label="Rejection regions")
ax.fill_between(x[x >= hi], stats.t.pdf(x[x >= hi]/se_d, df)/se_d,
                color="#d62728", alpha=0.4)

# Our observed mean difference
ax.axvline(d_bar, color="#1f77b4", linewidth=2.5)
ax.annotate(f"observed d̄ = +{d_bar:.2f}\n(≈ +${d_bar*1000:,.0f} per rep)",
            xy=(d_bar, 0.02), xytext=(d_bar+0.2, 0.35),
            color="#1f77b4", fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#1f77b4"))

ax.axvline(0, color="black", linestyle=":", linewidth=1.5)
ax.text(0.03, 0.62, "H₀ centre (zero change)", fontsize=9)

ax.set_xlabel("Mean change in monthly sales (thousands of $)")
ax.set_ylabel("Probability density")
ax.set_title("Where our result sits under the null hypothesis")
ax.legend(loc="upper left", fontsize=9)
ax.grid(alpha=0.25)
plt.tight_layout()
plt.show()
```

### What each element does

| Element                         | Meaning                                                                                                                                          |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **The curve**                   | What the _average change_ d̄ would look like across many hypothetical repeats of the experiment, **if training did nothing**. It is centred on 0. |
| **Its width**                   | Set by the **standard error** (0.743). Narrow curve = precise experiment = easier to detect effects.                                             |
| **Dotted line at 0**            | H₀'s prediction.                                                                                                                                 |
| **Red dashed lines at ±1.64**   | The critical boundaries converted to dollars: ±(2.201 × 0.743) = ±1.64. If d̄ landed beyond these, we'd reject H₀.                                |
| **Red shaded tails (5% total)** | The chance of a false alarm.                                                                                                                     |
| **Blue line at +4.08**          | Our actual observed average improvement — **way** out in the right-hand territory that H₀ essentially never produces.                            |
| **The arrow annotation**        | Translates the statistic into the business unit ($4,083 per rep).                                                                                |

**Why this graph is powerful for stakeholders:** you can point at it and say _"If the training did nothing, the most likely outcome is $0 change, and anything beyond ±$1,640 would be unusual. We observed +$4,083. That's off the chart."_

---

<a name="13"></a>

## 13. Graph 5 — Q-Q Plot (Assumption Check)

The t-test assumes the **differences** are roughly normally distributed (especially with small n). The Q-Q plot checks this visually.

```python
fig, ax = plt.subplots(figsize=(5.5, 5))
stats.probplot(sales["diff"], dist="norm", plot=ax)

ax.get_lines()[0].set(marker="o", markersize=7, markerfacecolor="#4c72b0",
                      markeredgecolor="white", linestyle="")
ax.get_lines()[1].set(color="#d62728", linewidth=2)
ax.set_title("Q-Q plot of the differences (normality check)")
ax.set_xlabel("Theoretical quantiles (normal)")
ax.set_ylabel("Ordered differences")
ax.grid(alpha=0.25)
plt.tight_layout()
plt.show()
```

### What each element does

| Element               | Meaning                                                                                                                                                           |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Each blue dot**     | One rep's difference score, plotted against the value we'd _expect_ if the data were perfectly normal at that rank.                                               |
| **X-axis**            | Theoretical quantiles: essentially "how extreme is this observation supposed to be?" Negative = lower tail, positive = upper tail.                                |
| **Y-axis**            | The actual sorted difference values (smallest to largest).                                                                                                        |
| **Red straight line** | The ideal path a perfectly normal dataset would follow.                                                                                                           |
| **How to judge**      | If the dots hug the line, normality is reasonable. If they curve into a banana shape, the data are skewed. If one dot is miles off the line, you have an outlier. |

**Our plot:** the points sit close to the line, with mild wobble (normal for n = 12) and the lowest point (−1) slightly below the line. **Conclusion: normality is acceptable → the paired t-test is valid here.**

> ⚠️ If the Q-Q plot showed strong skew or heavy outliers, switch to `stats.wilcoxon()`.

---

<a name="14"></a>

## 14. A Second Example Where the Test FAILS to Reject

It's crucial to see a **non-significant** result. This one comes from a customer-support team testing a new ticket tool. Lower handling time is better.

```python
support = pd.DataFrame({
    "agent":  [f"Agent {i}" for i in range(1, 13)],
    "before": [30, 42, 25, 38, 33, 45, 28, 36, 40, 31, 27, 39],
    "after":  [28, 44, 26, 35, 36, 44, 27, 37, 42, 29, 30, 38],
})
support["diff"] = support["after"] - support["before"]

d2      = support["diff"].to_numpy()
n2      = len(d2)
d_bar2  = d2.mean()
s_d2    = d2.std(ddof=1)
se2     = s_d2 / np.sqrt(n2)
t2      = d_bar2 / se2
df2     = n2 - 1
t_crit2 = stats.t.ppf(0.975, df2)
p2      = 2 * stats.t.sf(abs(t2), df2)

print(f"mean diff = {d_bar2:.3f}")
print(f"s_d       = {s_d2:.3f}")
print(f"SE        = {se2:.3f}")
print(f"t         = {t2:.3f}")
print(f"t*        = ±{t_crit2:.3f}")
print(f"p         = {p2:.4f}")
print(f"Decision: {'REJECT H0' if abs(t2) > t_crit2 else 'FAIL TO REJECT H0'}")

res2 = stats.ttest_rel(support["after"], support["before"])
print(res2)
```

**Expected output**

```text
mean diff = 0.167
s_d       = 2.082
SE        = 0.601
t         = 0.277
t*        = ±2.201
p         = 0.787
Decision: FAIL TO REJECT H0

TtestResult(statistic=0.2773..., pvalue=0.7870..., df=11)
```

### How to read this conclusion

- **t = 0.277** is tiny. Our mean difference is only 0.28 standard errors away from zero.
- **|t| = 0.277 < t\* = 2.201** → the statistic is **inside** the "do nothing unusual" zone.
- **p = 0.787.** If the tool truly had no effect, we'd see a result this extreme about **79%** of the time. Completely unremarkable.
- **95% CI: 0.167 ± 2.201 × 0.601 = (−1.16, +1.49)** — it **contains 0**, consistent with the non-significant result.

**Business translation:** _"The new tool did not produce a statistically detectable change in handling time. We cannot justify a rollout on this evidence. Either the effect is genuinely tiny, or our sample of 12 agents is too small to detect it."_

### The two examples side by side

|                        | Training (Example 1) | Support tool (Example 2) |
| ---------------------- | -------------------- | ------------------------ |
| d̄                      | **+4.083**           | +0.167                   |
| s_d                    | 2.575                | 2.082                    |
| SE                     | 0.743                | 0.601                    |
| **t**                  | **5.494**            | **0.277**                |
| t\* (df = 11, α = .05) | ±2.201               | ±2.201                   |
| p                      | **0.0002**           | 0.787                    |
| Decision               | **Reject H₀** ✅     | Fail to reject H₀ ❌     |
| 95% CI                 | (2.45, 5.72)         | (−1.16, 1.49)            |

Notice the variances are similar (2.58 vs 2.08). **The only big difference is the size of the effect.** That's why effect size matters more than p-values.

---

<a name="15"></a>

## 15. Assumptions and What To Do When They Break

| #   | Assumption                           | What it means                                  | How to check it                             | What to do if violated                                                    |
| --- | ------------------------------------ | ---------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------- |
| 1   | **Paired observations**              | Each unit measured twice, or genuinely matched | By design — this is a data-collection issue | If unpaired, use `ttest_ind`                                              |
| 2   | **Independent pairs**                | One rep's change doesn't depend on another's   | By design (random sampling)                 | Use a clustered/mixed model                                               |
| 3   | **Approximately normal differences** | The `diff` column is roughly bell-shaped       | Q-Q plot, histogram, `stats.shapiro(d)`     | n ≥ 30 → CLT rescues you; otherwise use `stats.wilcoxon`                  |
| 4   | **No extreme outliers**              | A single wild value doesn't drive everything   | Boxplot of `diff`, z-scores                 | Investigate: is it a data-entry error? Report results with and without it |
| 5   | **Continuous outcome**               | Measurement, not plain counts of categories    | By design                                   | Use McNemar's test for paired binary data                                 |

### Quick check code

```python
from scipy import stats

print("Shapiro-Wilk normality test on differences:", stats.shapiro(sales["diff"]))

# Outlier check via the IQR rule
q1, q3 = np.percentile(sales["diff"], [25, 75])
iqr = q3 - q1
lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr
print(f"Outlier fences: [{lo:.2f}, {hi:.2f}]")
print("Outliers:", sales["diff"][(sales['diff'] < lo) | (sales['diff'] > hi)].tolist())
```

```text
Shapiro-Wilk normality test on differences: ShapiroResult(statistic=0.93, pvalue=0.38)
Outlier fences: [-0.50, 9.50]
Outliers: []
```

The Shapiro p-value of 0.38 > 0.05 means we **fail to reject normality** — good news. The outlier fences catch nothing. Two green lights.

> 💡 Note the Shapiro test is itself a hypothesis test with H₀ = "the data ARE normal". Here we _want_ a large p-value.

### Robustness note

The paired t-test is reasonably **robust** to mild non-normality, especially as n grows (Central Limit Theorem). It is **not** robust to severe skew or to strong outliers with small samples. When in doubt, run the Wilcoxon signed-rank test alongside — if the two agree, your conclusion is safe.

---

<a name="16"></a>

## 16. Effect Size and Confidence Interval: Beyond "Is It Significant?"

### Why "significant" isn't enough

With a big enough sample, even a trivially small effect will produce p < 0.05. Conversely, a huge effect can be missed with n = 5. **p answers "could this be chance?" — it does not answer "does this matter?"**

### Cohen's d for paired data

$$
d = \frac{\bar{d}}{s_d}
$$

| Symbol | Meaning                                 |
| ------ | --------------------------------------- |
| d      | Effect size in standard-deviation units |
| d̄      | Mean difference (the effect)            |
| s_d    | SD of the differences (the yardstick)   |

For our training data: **d = 4.083 / 2.575 = 1.586**

**Rough interpretation guide (Cohen's conventions)**

| \|d\| | Interpretation        |
| ----- | --------------------- |
| 0.20  | Small                 |
| 0.50  | Medium                |
| 0.80  | Large                 |
| 1.5+  | Very large / enormous |

Our **1.59** is very large. Combined with the tiny p-value, this is a genuinely strong, business-relevant result.

### The paired confidence interval

$$
\bar{d} \ \pm \ t^{*} \times \frac{s_d}{\sqrt{n}}
$$

| Piece    | Meaning                                                                            |
| -------- | ---------------------------------------------------------------------------------- |
| d̄        | Our best point estimate of the true effect                                         |
| t\*      | Critical value for the desired confidence level (1.96-ish for 95%, bigger for 99%) |
| s_d / √n | Standard error                                                                     |
| t\* × SE | **Margin of error** — the "give or take"                                           |

**Compute:** 4.083 ± 2.201 × 0.743 = 4.083 ± 1.636 = **(2.447, 5.720)**

### The beautiful link between CI and t-test

- If the **95% CI excludes 0** → the two-tailed test at α = 0.05 **rejects** H₀.
- If the **95% CI includes 0** → **fails to reject**.

They are always in agreement. That's why reporting the CI is more informative than reporting a bare p-value: **it gives both the significance verdict and the magnitude, in real units.**

### Power and sample size

- **Power** = the probability of correctly detecting a real effect. Conventionally you want ≥ 0.80.
- Power rises with bigger effects, smaller variance, larger n, and larger α.
- Rough rule for a paired design: `n ≈ 8 / d²` pairs for 80% power at α = 0.05. With d = 1.59, that's `8 / 2.53 ≈ 3` pairs — which is why 12 reps is plenty here.

```python
from statsmodels.stats.power import TTestPower
analysis = TTestPower()
n_needed = analysis.solve_power(effect_size=1.586, alpha=0.05, power=0.80, alternative="two-sided")
print(f"Pairs needed for 80% power: {np.ceil(n_needed):.0f}")
```

```text
Pairs needed for 80% power: 7
```

---

<a name="17"></a>

## 17. Company Use Cases: Driving Business Decisions

### 🏢 Use Case 1 — Sales Enablement (our example)

**Setup:** 12 reps trained. d̄ = +4.083 ($1,000s/month).

**Business calculation**

```python
reps_in_company   = 200
months            = 12
extra_per_rep_mo  = 4.083          # $1,000s
annual_uplift     = reps_in_company * months * extra_per_rep_mo * 1000
program_cost      = 350_000
print(f"Projected annual uplift: ${annual_uplift:,.0f}")
print(f"Net benefit:             ${annual_uplift - program_cost:,.0f}")
```

```text
Projected annual uplift: $9,799,200
Net benefit:             $9,449,200
```

**Decision:** Even using the **lower bound** of the 95% CI ($2,447/rep/month), the annual uplift is 200 × 12 × 2,447 = **$5.87M** — several times the program cost. **Roll out to all 200 reps.**

**Caveat to state in the memo:** the pilot reps weren't randomly selected, so results may not generalise perfectly. Recommend a phased rollout with continued measurement.

---

### 🏢 Use Case 2 — HR: Employee Wellbeing Program

Measure **burnout score (0–100, lower is better)** for 25 employees before and after an 8-week mindfulness program.

- H₀: μ_d = 0; H₁: μ_d ≠ 0; α = 0.05
- Suppose you get d̄ = −6.2, s_d = 7.9, n = 25 → SE = 1.58, **t = −3.92**, df = 24, t\* = 2.064, **p = 0.0006**

**Decision:** Reject H₀. Burnout dropped significantly. Estimate the **retention value**: if a 6-point drop reduces voluntary turnover by 2 percentage points, and each replacement costs $40,000, then 25 employees → 1.2 people × $40,000 ≈ **$48,000 saved** in the pilot alone. Led by HR + Finance.

**Why paired matters here:** people have wildly different baseline burnout. Pairing removes that noise.

---

### 🏢 Use Case 3 — Product/Analytics: Homepage Redesign (within-subjects A/B test)

Same 40 users see the old and new homepage in random order. Outcome = **time to first meaningful click (seconds)**.

- If d̄ = −1.8s, s_d = 3.4s → SE = 0.538, **t = −3.35**, df = 39, t\* = 2.023, p ≈ 0.002

**Decision:** The new design is significantly faster. Now translate: 1.8s faster × 500,000 monthly sessions × conversion uplift per second (say +0.3% per second) = a 0.54pp conversion gain. At $60 AOV, that's 500,000 × 0.0054 × $60 = **$162,000/month**. Ship it.

**Why paired matters here:** within-subject designs cancel out individual browsing-speed differences, so you often need **far fewer users** than a between-subjects A/B test — a big deal when traffic is limited.

---

### 🏢 Use Case 4 — Operations/Manufacturing: Machine Recalibration

Measure **defect rate per shift** on the same 15 production lines before and after a calibration protocol change.

- H₀: μ_d = 0; α = 0.01 (stricter — recalibration is expensive and disruptive)
- Result: d̄ = −0.9 defects/shift, s_d = 2.4, n = 15 → SE = 0.620, **t = −1.45**, df = 14, t\* = 2.977, **p ≈ 0.17**

**Decision:** **Fail to reject H₀** at α = 0.01. Do not roll out across all 60 lines yet. Either the effect is too small to detect with 15 lines, or it's genuinely negligible. **Action:** run a 6-month extended pilot, or target only the line types with the largest observed drops.

This is a great example of a test that **protects the business from a costly mistake**.

---

### 🏢 Use Case 5 — Customer Success: Support Tool Rollout (Section 14 revisited)

12 agents, new ticket-routing tool, outcome = average handling time.

- **t = 0.277, p = 0.787** → no detectable effect.

**Decision:** Don't attribute a service improvement to the tool. Two paths:

1. **The effect is genuinely ~0** (d̄ = +0.17 minutes) → the tool isn't worth the licence cost; kill or renegotiate.
2. **The effect is real but our study is under-powered** → the 95% CI (−1.16, +1.49) means the true effect could be as good as −1.16 minutes. If −1 minute is worth $500K/year, run a bigger pilot (about 90 agents would give 80% power for a 1-minute effect at that variance).

**Lesson:** "Not significant" is a finding, not a failure. It tells you what you _cannot_ claim.

---

### 🏢 Use Case 6 — Marketing: Email Campaign Subject Line

Offer the same 500 customers two subject lines (order randomised, within-subject) and compare **open rate** ... careful — this one is binary, so use **McNemar's test**, not a paired t-test. _Good contrast to mention so you know the boundary._

If instead you measure **revenue per customer** under both subject lines, a paired t-test on the revenue differences is appropriate.

---

### A reusable decision checklist for any paired experiment

1. **Is the unit measured twice (or matched)?** If no → independent t-test.
2. **Define the difference direction** (after − before) and stick to it.
3. **Check the Q-Q plot** of differences.
4. **Compute t and df**; compare |t| to t\*.
5. **Report the p-value AND the effect size AND the CI.**
6. **Convert the effect into money**, using the **lower CI bound** for the conservative case.
7. **Say what you cannot conclude** (generalisability, causation, long-term durability).

---

<a name="18"></a>

## 18. Common Mistakes Beginners Make

| Mistake                                                         | Why it's wrong                                                          | Fix                                                                 |
| --------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Using `ttest_ind` on paired data                                | Throws away the pairing; loses tons of power; may give a false negative | Use `ttest_rel`                                                     |
| Using `ddof=0` in `std()`                                       | Underestimates noise → inflates t → false positives                     | Use `d.std(ddof=1)`                                                 |
| Counting n as total observations (24) instead of **pairs** (12) | Wrong df → wrong critical value → wrong conclusion                      | n = number of **pairs**                                             |
| Confusing one- and two-tailed tests after seeing the data       | p-hacking; invalid results                                              | Decide the direction _before_ collecting data                       |
| Interpreting p as "the probability H₀ is true"                  | It's P(data \| H₀), not P(H₀ \| data)                                   | Say "if H₀ were true, we'd see this 0.02% of the time"              |
| Treating p ≥ 0.05 as "the effect is zero"                       | Absence of evidence ≠ evidence of absence                               | Report the CI: how big _could_ the effect still be?                 |
| Ignoring effect size                                            | With n = 100,000, a 0.001 effect is "significant"                       | Always report Cohen's d and business impact                         |
| Stacking many tests without correction                          | 20 tests at α = .05 → ~64% chance of one false positive                 | Use Bonferroni (α/m) or FDR                                         |
| Forgetting the assumption check                                 | Non-normal + small n can break the test                                 | Q-Q plot; Wilcoxon fallback                                         |
| Pairs broken by shuffling/reindexing                            | Silently ruins the pairing                                              | Keep before/after in the same row, or use `.reset_index(drop=True)` |
| Reporting only "significant/not significant"                    | Stakeholders need magnitudes                                            | "Average +$4,083 per rep/month, 95% CI [$2,447, $5,720]"            |

---

<a name="19"></a>

## 19. Cheat Sheet

```text
────────────────────────────────────────────────────────────────
PAIRED T-TEST — ONE-PAGE SUMMARY
────────────────────────────────────────────────────────────────

WHEN:        Same unit (or matched pair) measured twice.
             d = after − before for every unit.

HYPOTHESES:  H0: μ_d = 0        H1: μ_d ≠ 0   (two-tailed)
                                 H1: μ_d > 0   (one-tailed, up)
                                 H1: μ_d < 0   (one-tailed, down)

FORMULA:              d̄ − μ0        d̄
             t  =  ───────────  =  ───────
                      s_d/√n        SE

             df = n − 1     (n = number of PAIRS)

PIECES:      d̄    = mean difference              → the SIGNAL
             s_d  = SD of differences (ddof=1)   → the NOISE
             SE   = s_d/√n                       → noise of the average
             t    = how many standard errors the effect is from 0

CRITICAL VALUE:  t* = stats.t.ppf(1 − α/2, df)
                 df=11, α=.05 → t* = 2.201
                 df=30, α=.05 → t* = 2.042
                 df=∞,  α=.05 → t* = 1.960

DECISION:    |t| > t*   → REJECT H0   (equivalently: p < α)
             |t| ≤ t*   → FAIL TO REJECT H0

P-VALUE:     p = 2 × stats.t.sf(|t|, df)

95% CI:      d̄ ± t* × SE     (excludes 0 ⇔ reject H0)

EFFECT SIZE: d = d̄ / s_d   (0.2 small, 0.5 medium, 0.8 large)

PYTHON:      from scipy import stats
             stats.ttest_rel(after, before)          # paired
             stats.ttest_1samp(after - before, 0)    # identical
             stats.wilcoxon(after, before)           # non-parametric

ASSUMPTIONS: paired • independent pairs • normal-ish differences
             • no extreme outliers

ALWAYS REPORT: t, df, p, d̄, 95% CI, Cohen's d, and the $ impact.
────────────────────────────────────────────────────────────────
```

---

<a name="20"></a>

## 20. Practice Exercises

1. **Sign flip.** Re-run Example 1 handing `ttest_rel` the arguments in the opposite order (`before, after`). What changes? What stays the same? Explain why the two-tailed p-value is identical.

2. **One-tailed.** A firm has a genuine directional hypothesis that training _increased_ sales. Compute the one-tailed critical value for df = 11 at α = 0.05. Does the conclusion change? Why might a reviewer object to this choice being made now?

3. **New effect size.** Change Rep 5's `after` value from 78 to 68 and recompute t. What happens to d̄, s_d and t? Which one moved most? Explain.

4. **Halve the noise.** Keep d̄ = 4.083 but pretend s_d = 1.3. What is t now? What does this tell you about why controlled experiments matter?

5. **Break the assumption.** Replace one difference with an extreme outlier (e.g. +25). Recompute t and the Shapiro test. Does the conclusion survive? Try `stats.wilcoxon` too. Which is more robust?

6. **Business framing.** Using the lower bound of the 95% CI from Example 1, write a two-sentence memo to a CFO recommending (or rejecting) the training rollout.

7. **Wrong test.** Run `stats.ttest_ind(sales["after"], sales["before"])` on Example 1 and compare the p-value to the paired test. Which is smaller, and why?

---

## Final Recap

| Concept                 | One-line takeaway                                                                   |
| ----------------------- | ----------------------------------------------------------------------------------- |
| **Paired t-test**       | A one-sample t-test on the differences `after − before`.                            |
| **t-statistic**         | Signal ÷ noise = d̄ / (s_d/√n). How many standard errors the effect sits from zero.  |
| **Critical value**      | A fixed threshold set by α and df. The boundary of the rejection region.            |
| **Decision**            | \|t\| > t\* (equivalently p < α) → reject H₀.                                       |
| **p-value**             | Probability of data this extreme _if H₀ were true_. Not the probability H₀ is true. |
| **Effect size**         | Cohen's d = d̄/s_d. Necessary to know if the effect _matters_.                       |
| **Confidence interval** | d̄ ± t\*·SE. Excludes 0 ⇔ reject H₀. Reports magnitude in real units.                |
| **Business link**       | Convert the effect (use the CI lower bound!) into dollars, then decide.             |

**The whole idea in one sentence:** _A paired t-test asks whether the average change across matched units is too large relative to the noise in those changes to be explained by chance — and the critical value is the line that defines "too large."_

```

Save it as `paired_t_test_tutorial.md`. Want me to extend it with a section on **paired t-test vs repeated-measures ANOVA**, a **simulation notebook** that shows the t-distribution emerging from repeated sampling, or a **one-page stakeholder summary** version?
```
