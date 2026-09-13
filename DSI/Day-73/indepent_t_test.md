# Hypothesis Testing in Data Science: The Independent Samples T-Test

**A beginner-friendly, end-to-end guide with Python code, graphs, formula breakdowns, and real business use cases.**

---

## 0. What You Will Be Able To Do After Reading This

By the end of this guide you will be able to:

1. Explain what a **null hypothesis** and an **alternative hypothesis** are, in plain English.
2. Explain what a **t-statistic** is, why it is a "signal-to-noise" number, and how it leads to a conclusion.
3. Explain what a **critical value** is, where it comes from, and how to compare it against your t-statistic.
4. Run an **independent samples t-test** in Python using `scipy.stats.ttest_ind`.
5. Verify the result by calculating it **by hand** from the formula.
6. Draw and read **four different plots** that make the statistics visual.
7. Compute **effect size (Cohen's d)** and a **confidence interval**, which tell you whether the result _matters_, not just whether it is _real_.
8. Translate all of this into **business decisions** with real company scenarios.

**Notation used throughout:** `x̄` (read "x-bar") means a _sample mean_. `s` means a _sample standard deviation_. `n` means the number of observations in a sample. `α` is the Greek letter alpha.

---

## 1. The Business Problem That Starts Everything

Imagine you run the online store **StyleHub**.

Your A/B testing tool says:

| Landing page             | Visitors | Average order value (AOV) |
| ------------------------ | -------- | ------------------------- |
| Old page (**control**)   | 60       | $52.10                    |
| New page (**treatment**) | 65       | $57.40                    |

The new page's average is **$5.30 higher**. Your product manager says: _"Great — ship the new page to 100% of traffic!"_

Should you? **Not yet.** Here is the trap:

> Every time you take a random sample of 60 or 65 shoppers, you get slightly _different_ averages — even if the two pages are **exactly equally good**. The difference in averages could be pure luck (random noise), not a real effect of the page.

This is the whole reason hypothesis testing exists. It answers:

> **"Is the difference I observed bigger than what I would expect from random luck alone?"**

If yes → we call the result **statistically significant** and act on it.
If no → we do not have enough evidence; we wait for more data.

A t-test is a **standardized ruler** for measuring how surprising your difference is.

---

## 2. Core Vocabulary (Plain English First, Formal Definition Second)

| Term                                  | Plain English                                                                           | Formal version                                                 |
| ------------------------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Population**                        | "All shoppers, forever" — what you truly want to know about                             | Every unit you care about                                      |
| **Sample**                            | "The 125 shoppers we actually measured"                                                 | A subset of the population                                     |
| **Null hypothesis (H₀)**              | "Nothing is going on. The two pages perform the same."                                  | The true difference in population means is 0: H₀: μ₁ = μ₂      |
| **Alternative hypothesis (H₁ or Hₐ)** | "Something IS going on."                                                                | H₁: μ₁ ≠ μ₂ (two-sided) or μ₁ > μ₂ / μ₁ < μ₂ (one-sided)       |
| **Test statistic**                    | "How far did our data land from what H₀ predicts, measured in units of typical wobble?" | Here, the **t-statistic**                                      |
| **t-statistic (t)**                   | The signal-to-noise ratio for a difference in means                                     | t = (observed difference) ÷ (standard error of the difference) |
| **Standard error (SE)**               | The typical size of random wobble in that difference                                    | SE = s_p × √(1/n₁ + 1/n₂)                                      |
| **Degrees of freedom (df)**           | How much independent information your data carries; it shapes the curve                 | df = n₁ + n₂ − 2 (pooled version)                              |
| **Critical value (t\*)**              | The cutoff line on the t-curve. Cross it → significant                                  | t\* = value where α of the curve sits beyond it                |
| **Significance level (α)**            | Your risk tolerance for a false alarm. Usually 0.05 = 5%                                | P(reject H₀ \| H₀ true)                                        |
| **p-value**                           | "If H₀ were true, how often would luck alone produce a difference this big or bigger?"  | P(data this extreme or more \| H₀)                             |
| **Type I error**                      | False alarm — ship a change that does nothing (or hurts)                                | Rejecting a true H₀                                            |
| **Type II error**                     | Missed opportunity — kill a change that actually works                                  | Failing to reject a false H₀                                   |
| **Effect size (Cohen's d)**           | "OK it's real — but how _big_ is it?"                                                   | d = (difference in means) ÷ (pooled SD)                        |

### The two decision paths (they always agree)

There are two equivalent ways to reach a conclusion. You should understand both, because interviewers and senior stakeholders use both.

**Path A — Critical value method**

```
IF |t_observed| > t_critical   →  REJECT H₀  (statistically significant)
IF |t_observed| ≤ t_critical   →  FAIL TO REJECT H₀  (not significant)
```

**Path B — p-value method**

```
IF p_value < α   →  REJECT H₀  (statistically significant)
IF p_value ≥ α   →  FAIL TO REJECT H₀  (not significant)
```

They are **mathematically the same test**. The critical value is a fixed line you compute _before_ looking at data; the p-value asks the mirror-image question. This guide emphasises the critical value because it forces you to _see_ the geometry — the line on the curve — which builds far better intuition.

**Note on language:** we say "fail to reject H₀", never "accept H₀" or "prove H₀". A non-significant result means _insufficient evidence_, not _proof of no effect_. Absence of evidence is not evidence of absence.

---

## 3. What "Independent Samples" Means, and When to Use This Test

The **independent samples t-test** (also called the **two-sample t-test**, **unpaired t-test**, or **Student's t-test**) compares the **means of two separate, unrelated groups**.

- ✅ Independent: Group A shoppers are different people from Group B shoppers. Treated patients vs placebo patients. Supplier X bolts vs Supplier Y bolts.
- ❌ Not independent (use a **paired t-test** instead): Same people measured before and after. Same patient's left eye vs right eye. Same store in January vs February.

### The four assumptions (and how to check each)

| Assumption                                             | What it means                                                                                                           | How to check in code                      |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| **1. Independence**                                    | Each observation is unrelated to the others                                                                             | Study design (satisfied by randomization) |
| **2. Continuous outcome**                              | The variable measured is numeric/continuous                                                                             | Look at your data type                    |
| **3. Roughly normal** per group (or n ≥ ~30 per group) | The t-curve logic requires approximately normal data, or a large enough sample for the Central Limit Theorem to kick in | `stats.shapiro()`, histogram, Q-Q plot    |
| **4. Similar variances** (only for Student's version)  | Both groups have similar spread                                                                                         | `stats.levene()`                          |

**Two versions of the test:**

- **Student's t-test** — assumes _equal variances_ (pooled). Use when Levene's test p > 0.05.
- **Welch's t-test** — does _not_ assume equal variances. Use when Levene's p < 0.05. Many statisticians now recommend **Welch's by default**, because it performs well even when variances are equal.

In `scipy`: `equal_var=True` → Student's; `equal_var=False` → Welch's.

---

## 4. The Formula, Broken Down Piece by Piece

### 4.1 The main formula — Student's (pooled) t-test

$$
t = \frac{\bar{x}_1 - \bar{x}_2}{s_p\sqrt{\dfrac{1}{n_1} + \dfrac{1}{n_2}}}
$$

**Numerator — the signal:**

| Symbol  | Name                     | Meaning                                 | In our example             |
| ------- | ------------------------ | --------------------------------------- | -------------------------- |
| x̄₁      | Sample mean of group 1   | Average outcome for the control group   | $52.10                     |
| x̄₂      | Sample mean of group 2   | Average outcome for the treatment group | $57.40                     |
| x̄₁ − x̄₂ | Observed mean difference | The effect you _think_ you see          | 52.10 − 57.40 = **−$5.30** |

The sign is just about which group you subtracted from which. We care about the **absolute value** for a two-sided test.

**Denominator — the noise (standard error of the difference):**

The denominator has three parts. Start with the **pooled variance**:

$$
s_p^2 = \frac{(n_1 - 1)s_1^2 + (n_2 - 1)s_2^2}{n_1 + n_2 - 2}
$$

| Symbol      | Meaning                                                         |
| ----------- | --------------------------------------------------------------- |
| s₁²         | Variance of group 1 (spread of control orders, squared, in $²)  |
| s₂²         | Variance of group 2                                             |
| n₁ − 1      | Degrees of freedom contributed by group 1 (Bessel's correction) |
| n₂ − 1      | Degrees of freedom contributed by group 2                       |
| n₁ + n₂ − 2 | Total degrees of freedom for the test                           |

> **Why n − 1 and not n?** You estimated the mean from the same data you are using to measure spread. That costs you one degree of freedom, and dividing by n−1 makes the variance estimate unbiased (slightly larger, honestly reflecting your uncertainty). In pandas, `.std()` already uses n−1. In **numpy, `np.std()` defaults to n** — a classic beginner bug. Always pass `ddof=1` to numpy.

Then `s_p` is just the square root of the pooled variance — the **pooled standard deviation**, a single blended estimate of "spread" for both groups.

Finally the **standard error of the difference** multiplies by the sample-size term:

$$
SE = s_p\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}
$$

| Symbol         | Meaning                                                                           |
| -------------- | --------------------------------------------------------------------------------- |
| 1/n₁           | Uncertainty contributed by group 1's mean                                         |
| 1/n₂           | Uncertainty contributed by group 2's mean                                         |
| √(1/n₁ + 1/n₂) | Shrinks as either sample gets bigger. **Bigger samples → smaller SE → larger t.** |

**Putting it in words:**

> t = (how different the two averages are) ÷ (how different they would typically look just by luck)

- t near 0 → the difference is nothing special → don't reject H₀.
- t large in magnitude (roughly |t| > 2 for typical sample sizes) → the difference is unusual → reject H₀.

You can **never** judge significance from the raw difference ($5.30) alone, because the same $5.30 could be huge or trivial depending on the noise. That is exactly why we divide.

### 4.2 Welch's version (unequal variances)

$$
t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{\dfrac{s_1^2}{n_1} + \dfrac{s_2^2}{n_2}}}
$$

Each group contributes its own variance instead of a pooled one. The degrees of freedom use the **Welch–Satterthwaite approximation**:

$$
df = \frac{\left(\dfrac{s_1^2}{n_1} + \dfrac{s_2^2}{n_2}\right)^2}{\dfrac{\left(\dfrac{s_1^2}{n_1}\right)^2}{n_1 - 1} + \dfrac{\left(\dfrac{s_2^2}{n_2}\right)^2}{n_2 - 1}}
$$

Breaking that down: the numerator is (total variance of the difference)². The denominator adds up each group's variance-of-variance contribution, weighted by its own degrees of freedom. The result is a **non-integer df** (e.g. df = 118.7) — that is normal and completely fine.

### 4.3 Effect size — Cohen's d

$$
d = \frac{\bar{x}_1 - \bar{x}_2}{s_p}
$$

Same numerator, but divided by the **standard deviation** instead of the standard error. It therefore does **not** grow when you collect more data. It answers "how many standard deviations apart are these groups?"

Rough rule of thumb (Cohen, 1988):

| \|d\| | Interpretation |
| ----- | -------------- |
| 0.2   | Small          |
| 0.5   | Medium         |
| 0.8   | Large          |

### 4.4 Confidence interval for the difference

$$
(\bar{x}_1 - \bar{x}_2) \pm t^* \times SE
$$

where t\* is the same two-tailed critical value you use for the decision. This gives a **range of plausible values for the true difference**. If the interval contains 0, the result is not significant at level α — it is the same information, presented as a range instead of a yes/no.

**Worked mini-example by hand** (numbers rounded for readability):

```
Control:   n₁ = 60,   x̄₁ = 52.10,   s₁ = 11.80
Treatment: n₂ = 65,   x̄₂ = 57.40,   s₂ = 12.90

Numerator:    52.10 − 57.40 = −5.30

Pooled variance:
  s_p² = [(59)(11.80²) + (64)(12.90²)] / (60 + 65 − 2)
       = [59(139.24) + 64(166.41)] / 123
       = [8215.16 + 10650.24] / 123
       = 18865.40 / 123
       = 153.38
  s_p  = √153.38 = 12.38

Standard error:
  SE = 12.38 × √(1/60 + 1/65)
     = 12.38 × √(0.016667 + 0.015385)
     = 12.38 × √0.032051
     = 12.38 × 0.17903
     = 2.216

t-statistic:
  t = −5.30 / 2.216 = −2.39

Degrees of freedom:  df = 60 + 65 − 2 = 123

Critical value (two-tailed, α = 0.05):
  t* = 1.980   →  since |−2.39| = 2.39 > 1.980, REJECT H₀

Effect size:
  d = −5.30 / 12.38 = −0.43  (medium effect)

Confidence interval (95%):
  −5.30 ± (1.980 × 2.216) = −5.30 ± 4.39 = [−9.69, −0.91]
  The interval is entirely below 0 → consistent with significance.
```

Try this arithmetic yourself with a calculator once — the numbers become much less mysterious.

---

## 5. Deep Dive: The Critical Value

### 5.1 What it actually is

The **critical value** is the boundary line on the t-distribution. Everything more extreme than that line is called the **rejection region**.

For a **two-tailed test at α = 0.05**, we split the 5% risk into **2.5% in the left tail** and **2.5% in the right tail**, because an effect in either direction would be interesting.

```
                     t-distribution (df = 123)
                          _.-''''-._
                       ,-'          '-.
                     ,'                 `.
                   ,'    NOT             `.
                 ,'    SIGNIFICANT         `.
               ,'                            `.
   ▓▓▓▓▓▓▓▓▓▓,'                                ',▓▓▓▓▓▓▓▓▓▓
   ▓▓▓▓▓▓▓▓ -1.980            0           +1.980 ▓▓▓▓▓▓▓▓▓
     2.5%     ← 95% of the area →              2.5%
   reject H₀        fail to reject H₀       reject H₀
```

- Area beyond the cutoffs = α = 0.05 (your false-alarm budget).
- If your observed t lands **inside the shaded tails**, you reject H₀.
- In code: `stats.t.ppf(1 - alpha/2, df)` → the right-tail critical value (positive).
- The left critical value is simply its negative, because the t-distribution is **symmetric**.

### 5.2 Why t and not z?

The **normal (z) distribution** would be correct if you knew the true population standard deviation σ. You don't — you **estimate** it from your sample with s. That extra uncertainty makes the true sampling distribution slightly **wider in the tails**: a **Student's t-distribution**.

Key properties of the t-distribution:

- Symmetric, bell-shaped, centred on 0.
- **Heavier tails** than the normal distribution → critical values are bigger.
- Its exact shape depends on **degrees of freedom**. Small df → very heavy tails → larger critical values.
- As df → ∞, the t-distribution converges to the normal distribution.

### 5.3 How df changes the critical value (two-tailed, α = 0.05)

| df (n₁+n₂−2) | Approx. sample size | t\* critical value |
| ------------ | ------------------- | ------------------ |
| 2            | tiny                | 4.303              |
| 5            | tiny                | 2.571              |
| 10           | small               | 2.228              |
| 30           | moderate            | 2.042              |
| 60           | good                | 2.000              |
| 123          | our example         | **1.980**          |
| 1000         | very large          | 1.962              |
| ∞ (normal z) | infinite            | 1.960              |

This table is the whole intuition: **the less data you have, the further your t must travel before you are allowed to call the result real.** With few observations, a t of 2.0 is unremarkable. With 123 observations, 2.0 is already past the line.

### 5.4 Reading a printed t-table

Classic statistics textbooks print a table like this (two-tailed α):

| df  | 0.10  | 0.05  | 0.01  |
| --- | ----- | ----- | ----- |
| 10  | 1.812 | 2.228 | 3.169 |
| 30  | 1.697 | 2.042 | 2.776 |
| 60  | 1.671 | 2.000 | 2.660 |
| 120 | 1.658 | 1.980 | 2.617 |

To use it: find your df row, find your α column, read the number. That's t\*. Everything else (one-tailed tests, different α, odd df) is easier in Python with `stats.t.ppf`, which does the same lookup with infinite precision.

### 5.5 One-tailed vs two-tailed critical values

- **Two-tailed** (H₁: μ₁ ≠ μ₂): split α across both tails. Critical value = `ppf(1 − α/2, df)`.
- **One-tailed, greater** (H₁: μ₁ > μ₂): put all α in one tail. Critical value = `ppf(1 − α, df)` — a _smaller_, easier-to-cross threshold.

For α = 0.05 and df = 123: two-tailed t\* = 1.980, one-tailed t\* = 1.658.

⚠️ **Choose the tail BEFORE looking at the data.** Deciding afterwards to switch to a one-tailed test is a form of p-hacking, and it invalidates your α.

### 5.6 Comparing critical value vs t-statistic — the decision logic

```
t_observed = −2.39
t_critical = ±1.980

Is |t_observed| > t_critical ?
Is 2.39 > 1.980 ?  → YES  →  REJECT H₀

Conclusion: The difference in average order value is statistically significant
at the 5% level. Ship the new page (pending effect-size sanity check).
```

If instead the observed t had been **1.4**, we would say: _"1.4 does not cross 1.980, so this difference is easily explained by random variation. Do not roll out; keep collecting data."_

---

## 6. Deep Dive: The t-Statistic and How It Drives Conclusions

### 6.1 The one-line intuition

> **t = "how many standard errors away from zero is my observed difference?"**

If the two groups were truly identical, the difference between their sample means would wobble around zero with typical size = SE. So t is literally a **standardized distance from zero**.

### 6.2 What pushes t up or down

| Change                               | Effect on t    | Why                         |
| ------------------------------------ | -------------- | --------------------------- |
| Bigger true difference between means | ⬆️ t increases | Numerator grows             |
| More spread in the data (bigger s)   | ⬇️ t decreases | Denominator (noise) grows   |
| Larger samples (bigger n₁, n₂)       | ⬆️ t increases | 1/n terms shrink the SE     |
| More noise, same difference          | ⬇️ t decreases | Harder to detect the signal |

This is why two studies with the **same $5.30 difference** can reach opposite conclusions: the noisy small study has a t of 1.2; the large clean study has a t of 4.0.

### 6.3 From t to a conclusion — the full chain

```
Raw data → group means → difference → standard error → t-statistic
                                                          ↓
                          compare with critical value  ←  t-distribution (shape set by df)
                                                          ↓
                                          reject / fail to reject H₀
                                                          ↓
                                    check effect size + CI → business decision
```

### 6.4 The t-statistic and the p-value are the same thing

The p-value is the **area under the t-curve more extreme than your observed t** (both tails for a two-sided test). So:

- Large |t| → tiny tail area → tiny p-value → significant.
- Small |t| → big tail area → large p-value → not significant.

`t = 2.39` with df = 123 gives a two-tailed **p ≈ 0.019**. That is the area beyond ±2.39. Since 0.019 < 0.05, we reject H₀ — exactly the same decision the critical value method gave, as promised.

### 6.5 Statistical significance ≠ business significance

Your t can be "significant" simply because n is enormous, even when the difference is $0.02 of average order value. This is why **you always report three things together**:

1. **The t-statistic and p-value** → _Is the effect real (unlikely to be luck)?_
2. **The effect size (Cohen's d)** → _Is it large in practical terms?_
3. **The confidence interval in business units ($)** → _What is the plausible range of impact, and does it justify the cost?_

A senior data scientist's sentence looks like: _"The new page raised AOV by $5.30 (95% CI: $0.91 to $9.69), t(123) = 2.39, p = 0.019, d = 0.43 — a medium effect. At 200,000 monthly orders, that's roughly $180K–$1.9M in incremental monthly revenue, so it's worth the engineering days."_

---

## 7. Full Python Walkthrough

You need: `numpy`, `pandas`, `scipy`, `matplotlib`.

```
pip install numpy pandas scipy matplotlib
```

### Step 0 — Imports and settings

```python
# ============================================================
# STEP 0 — Imports and global plot settings
# ============================================================
import numpy as np                     # numbers and random data
import pandas as pd                    # tables (DataFrames)
from scipy import stats                # the statistics engine
import matplotlib.pyplot as plt        # plotting

np.random.seed(42)                     # makes the "random" data reproducible
plt.rcParams["figure.figsize"] = (9, 5)
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.3

print("Libraries loaded ✅")
```

- `np.random.seed(42)` fixes the random number generator so that anyone running this notebook gets **the same data**. In real life you would load a CSV instead.
- `plt.rcParams` lines just make every chart below look consistent and readable.

### Step 1 — Create (simulate) the data

```python
# ============================================================
# STEP 1 — Simulate two independent groups of shoppers
# ============================================================
# 60 shoppers saw the OLD landing page (control)
control = np.random.normal(loc=52.0, scale=12.0, size=60)

# 65 different shoppers saw the NEW landing page (treatment)
treatment = np.random.normal(loc=57.5, scale=13.0, size=65)

# Money is measured to the cent, not to 15 decimals
control   = np.round(control, 2)
treatment = np.round(treatment, 2)

# Put everything into ONE tidy DataFrame: one row per shopper
df = pd.DataFrame({
    "order_value": np.concatenate([control, treatment]),
    "group":       ["control"] * len(control) + ["treatment"] * len(treatment)
})

print(df.head())
print("\nRows:", len(df))
print(df["group"].value_counts())
```

**What each line does:**

| Line                                              | What it does                                                                                                                                |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `np.random.normal(loc=52.0, scale=12.0, size=60)` | Draws 60 numbers from a normal distribution with **mean 52** and **standard deviation 12**. This is our make-believe "old page" population. |
| `loc=57.5, scale=13.0, size=65`                   | The "new page" group: slightly higher mean (the real effect we planted), slightly more spread.                                              |
| `np.round(..., 2)`                                | Rounds to cents so the data looks realistic.                                                                                                |
| `np.concatenate([...])`                           | Glues the two arrays into one long column, the **tidy data** layout: one row per observation.                                               |
| `["control"] * 60 + ["treatment"] * 65`           | Creates the matching label column.                                                                                                          |

**Why the "long/tidy" format matters:** `ttest_ind` wants two separate arrays, `groupby` wants one column plus a label column. The tidy layout gives you both — you can always `.loc`-filter it into two arrays. Real-world data (CSV from your experiment platform) almost always arrives in this shape.

### Step 2 — Explore the data before testing anything

**Golden rule:** _always look at your data before you run a test._

```python
# ============================================================
# STEP 2 — Descriptive statistics per group
# ============================================================
summary = df.groupby("group")["order_value"].agg(
    n="count",
    mean="mean",
    std="std",
    median="median",
    min="min",
    max="max"
).round(2)

print(summary)
```

Expected output shape (your numbers will be close to these):

```
              n   mean    std  median    min     max
group
control      60  51.24  11.31   51.07  20.51   78.14
treatment    65  57.64  12.36   57.34  28.83   87.55
```

What each row/column tells you:

- **n** — 60 and 65 shoppers. Unequal group sizes are perfectly fine for a t-test.
- **mean** — the two averages we will compare (≈ $51.24 vs ≈ $57.64).
- **std** — the spread within each group (≈ 11.3 vs ≈ 12.4). These are similar-ish, hinting that Student's pooled test is defensible; Levene's test will confirm.
- **median** — the middle value. If median and mean are close, the distribution is roughly symmetric (a normality hint).
- **min / max** — the range. Useful for spotting impossible values (e.g. a negative order value would signal a data bug).

### Step 3 — Check the assumptions

```python
# ============================================================
# STEP 3 — Assumption checks
# ============================================================
# 3a) Normality within each group (Shapiro-Wilk test)
shapiro_c = stats.shapiro(control)
shapiro_t = stats.shapiro(treatment)
print(f"Shapiro control   : W={shapiro_c.statistic:.4f}, p={shapiro_c.pvalue:.4f}")
print(f"Shapiro treatment : W={shapiro_t.statistic:.4f}, p={shapiro_t.pvalue:.4f}")

# 3b) Equal variances? (Levene's test)
levene = stats.levene(control, treatment)
print(f"Levene            : W={levene.statistic:.4f}, p={levene.pvalue:.4f}")
```

**How to read these:**

- **Shapiro-Wilk**: H₀ is "the data is normally distributed". If **p > 0.05**, there is no evidence against normality → assumption OK. If p < 0.05, the data deviates from normal; with n ≈ 60 per group the t-test is still robust (Central Limit Theorem), but a Mann-Whitney U test would be the safer alternative.
- **Levene's test**: H₀ is "the two groups have equal variances". If **p > 0.05**, variances are similar → Student's t-test (`equal_var=True`) is fine. If p < 0.05 → use **Welch's** (`equal_var=False`).

### Step 4 — Run the independent samples t-test in one line

```python
# ============================================================
# STEP 4 — The test itself
# ============================================================
alpha = 0.05

t_stat, p_value = stats.ttest_ind(treatment, control, equal_var=True)

print(f"t-statistic : {t_stat:.4f}")
print(f"p-value     : {p_value:.4f}")

# The richer result object also gives you the degrees of freedom
res = stats.ttest_ind(treatment, control, equal_var=True)
print(res)
```

Output:

```
TtestResult(statistic=2.3905, pvalue=0.0184, df=123.0)
```

**Decoding the arguments:**

| Argument                            | Meaning                                                |
| ----------------------------------- | ------------------------------------------------------ |
| First array = `treatment`           | Group 2 (the one we subtract from)                     |
| Second array = `control`            | Group 1 (the one being subtracted)                     |
| `equal_var=True`                    | Use Student's pooled-variance formula                  |
| `equal_var=False`                   | Use Welch's formula (try it and compare the p-values!) |
| `alternative="two-sided"` (default) | H₁: means are different                                |
| `alternative="greater"`             | H₁: first group's mean is greater                      |
| `alternative="less"`                | H₁: first group's mean is smaller                      |

So a **positive t** here means the treatment mean is higher than the control mean — matching our sign convention.

```python
# Welch's version, for comparison
t_w, p_w = stats.ttest_ind(treatment, control, equal_var=False)
print(f"Welch: t={t_w:.4f}, p={p_w:.4f}, df={stats.ttest_ind(treatment, control, equal_var=False).df}")
```

### Step 5 — Verify by hand (never trust a black box you can't reproduce)

```python
# ============================================================
# STEP 5 — Manual calculation, step by step
# ============================================================
n1, n2 = len(control), len(treatment)
m1, m2 = control.mean(), treatment.mean()
s1, s2 = control.std(ddof=1), treatment.std(ddof=1)   # ddof=1 is critical!
var1, var2 = s1**2, s2**2

print(f"n1={n1}  n2={n2}")
print(f"mean1={m1:.4f}  mean2={m2:.4f}")
print(f"std1 ={s1:.4f}  std2 ={s2:.4f}")

# --- pooled variance ---
df_free   = n1 + n2 - 2
pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / df_free
pooled_sd  = np.sqrt(pooled_var)

# --- standard error of the difference ---
se = pooled_sd * np.sqrt(1/n1 + 1/n2)

# --- t-statistic ---
t_manual = (m2 - m1) / se

# --- critical value ---
t_crit = stats.t.ppf(1 - alpha/2, df_free)

# --- p-value from the t-distribution ---
p_manual = 2 * (1 - stats.t.cdf(abs(t_manual), df_free))

print(f"\nDegrees of freedom : {df_free}")
print(f"Pooled variance    : {pooled_var:.4f}")
print(f"Pooled SD          : {pooled_sd:.4f}")
print(f"Standard error     : {se:.4f}")
print(f"t (manual)         : {t_manual:.4f}")
print(f"t (scipy)          : {t_stat:.4f}")
print(f"Critical value t*  : ±{t_crit:.4f}")
print(f"p (manual)         : {p_manual:.4f}")
print(f"p (scipy)          : {p_value:.4f}")
```

**Key details:**

- `ddof=1` on `.std()` gives the **sample** standard deviation (divides by n−1). NumPy's `.std()` defaults to `ddof=0` — remember this or your manual answer will not match SciPy.
- `stats.t.ppf(1 - alpha/2, df_free)` is the inverse CDF: "give me the t value such that 97.5% of the curve lies to its left."
- `2 * (1 - stats.t.cdf(abs(t), df))` computes the two-tailed p-value: the right-tail area, doubled for symmetry.
- The manual numbers will match SciPy to several decimal places. If they do not, you have found a real bug — not a rounding issue.

### Step 6 — Effect size and confidence interval

```python
# ============================================================
# STEP 6 — Effect size (Cohen's d) and 95% CI
# ============================================================
diff = m2 - m1

cohens_d = diff / pooled_sd
ci_low  = diff - t_crit * se
ci_high = diff + t_crit * se

print(f"Mean difference : ${diff:.2f}")
print(f"Cohen's d       : {cohens_d:.3f}")
print(f"95% CI          : [${ci_low:.2f}, ${ci_high:.2f}]")
```

**Reading it:**

- `diff` — the raw effect in dollars. Easy for stakeholders to grasp.
- `cohens_d` — the effect in standard-deviation units, comparable across different metrics and studies.
- The CI — e.g. `[0.91, 9.69]`. Because 0 is **not** inside the interval, the result is significant at α = 0.05 (this is guaranteed to agree with the t-test). It also tells the business: _"the true uplift could be as small as 91 cents or as large as $9.69."_ That range is often what actually drives the go/no-go meeting.

### Step 7 — The critical-value decision, written out explicitly

```python
# ============================================================
# STEP 7 — Decision logic (critical value method)
# ============================================================
print("=" * 55)
print("HYPOTHESIS TEST DECISION")
print("=" * 55)
print(f"H0 : mean(treatment) == mean(control)")
print(f"H1 : mean(treatment) != mean(control)  (two-sided)")
print(f"alpha            = {alpha}")
print(f"df               = {df_free}")
print(f"critical value   = ±{t_crit:.4f}")
print(f"observed t       = {t_stat:.4f}")
print(f"|t| > t_critical ? {abs(t_stat):.4f} > {t_crit:.4f}  ->  {abs(t_stat) > t_crit}")
print("-" * 55)
if abs(t_stat) > t_crit:
    print("DECISION: REJECT H0 — the difference is statistically significant.")
else:
    print("DECISION: FAIL TO REJECT H0 — not enough evidence of a difference.")
print("=" * 55)
```

### Step 8 — Graph 1: Boxplot comparison

```python
# ============================================================
# GRAPH 1 — Boxplot + individual shopper dots
# ============================================================
fig, ax = plt.subplots()

data = [control, treatment]
bp = ax.boxplot(data, positions=[1, 2], widths=0.5, patch_artist=True,
                medianprops=dict(color="black", linewidth=2))

# Colour the two boxes
colors = ["#4C72B0", "#DD8452"]
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.55)

# Jittered individual points so you can see every shopper
for i, (group_data, color) in enumerate(zip(data, colors), start=1):
    x_jitter = np.random.normal(i, 0.045, size=len(group_data))
    ax.scatter(x_jitter, group_data, alpha=0.45, s=22, color=color, edgecolor="none")

# Mark the means
ax.scatter([1, 2], [m1, m2], marker="D", s=110, color="black",
           zorder=5, label="Group mean")

ax.set_xticks([1, 2])
ax.set_xticklabels([f"Control\n(old page)\nn={n1}", f"Treatment\n(new page)\nn={n2}"])
ax.set_ylabel("Order value ($)")
ax.set_title("Order value by landing page — boxplot with every shopper shown")
ax.legend()
plt.tight_layout()
plt.savefig("graph1_boxplot.png", dpi=150)
plt.show()
```

**How to read every element of this chart:**

| Element                                       | What it means                                                                             |
| --------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **The box**                                   | The middle 50% of shoppers (from the 25th to the 75th percentile, the IQR)                |
| **The black line inside the box**             | The **median** — the exact middle shopper                                                 |
| **The diamond marker**                        | The **mean** — what the t-test actually compares                                          |
| **The whiskers**                              | Extend to the most extreme values that are not outliers (1.5 × IQR rule)                  |
| **Dots beyond the whiskers**                  | Potential outliers — investigate, don't auto-delete                                       |
| **Each faint dot**                            | One real shopper. The vertical spread of dots = the noise the t-test must see through     |
| **The vertical offset between the two boxes** | The effect you are testing. Here the orange box sits higher → treatment has higher orders |
| **Box height comparison**                     | Spread. Similar heights → equal-variance assumption looks reasonable                      |

**The key visual lesson:** the boxes overlap a lot. If you only looked at the group means you would be impressed; looking at the spread reminds you that _many individual shoppers are identical across groups_. That overlap is exactly what the standard error quantifies, and it is why the t-test — not the raw mean difference — makes the decision.

### Step 9 — Graph 2: Histograms with means and the mean difference

```python
# ============================================================
# GRAPH 2 — Overlaid histograms with means and the gap
# ============================================================
fig, ax = plt.subplots()

bins = np.linspace(min(control.min(), treatment.min()),
                   max(control.max(), treatment.max()), 18)

ax.hist(control,   bins=bins, alpha=0.55, color="#4C72B0",
        edgecolor="white", label=f"Control (n={n1}, mean=${m1:.2f})")
ax.hist(treatment, bins=bins, alpha=0.55, color="#DD8452",
        edgecolor="white", label=f"Treatment (n={n2}, mean=${m2:.2f})")

# Vertical lines at the two means
ax.axvline(m1, color="#4C72B0", linestyle="--", linewidth=2)
ax.axvline(m2, color="#DD8452", linestyle="--", linewidth=2)

# Double-headed arrow showing the mean difference
top = ax.get_ylim()[1] * 0.88
ax.annotate("", xy=(m1, top), xytext=(m2, top),
            arrowprops=dict(arrowstyle="<->", color="black", lw=1.6))
ax.text((m1 + m2) / 2, top * 1.03,
        f"mean difference = ${m2 - m1:.2f}", ha="center", fontsize=11)

ax.set_xlabel("Order value ($)")
ax.set_ylabel("Number of shoppers")
ax.set_title("Distribution of order values: control vs treatment")
ax.legend()
plt.tight_layout()
plt.savefig("graph2_histograms.png", dpi=150)
plt.show()
```

**What to look for:**

- **Overlap region** — the wide grey area where both histograms sit on top of each other. Heavy overlap means the groups are similar _as individuals_.
- **Location shift** — the orange distribution is shifted slightly right. Small shift relative to width = moderate effect, which matches `d ≈ 0.43`.
- **Shape** — both look roughly bell-shaped → supports the normality assumption. Skewness or a second bump would be a red flag.
- **Spread** — the widths look comparable → equal-variance assumption plausible.
- **The arrow** — this is the **numerator** of the t-statistic: the entire "signal". The widths of the two histograms are the "noise". The t-statistic is literally signal ÷ noise.

### Step 10 — Graph 3: The t-distribution with the critical region (the star of the show)

```python
# ============================================================
# GRAPH 3 — t-distribution, critical values, observed t, p-value
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5.5))

x = np.linspace(-4.5, 4.5, 2000)
y = stats.t.pdf(x, df_free)

# The t-curve
ax.plot(x, y, color="black", linewidth=2, label=f"t-distribution (df={df_free})")

# Shaded rejection regions (the tails beyond ±t*)
ax.fill_between(x, y, where=(x <= -t_crit), color="crimson", alpha=0.35,
                label=f"rejection region (α/2 = {alpha/2:.3f} each tail)")
ax.fill_between(x, y, where=(x >= t_crit), color="crimson", alpha=0.35)

# Critical value lines
ax.axvline(-t_crit, color="crimson", linestyle="--", linewidth=1.8)
ax.axvline(t_crit,  color="crimson", linestyle="--", linewidth=1.8)
ax.text(t_crit + 0.07, 0.02, f"t* = {t_crit:.3f}", color="crimson", fontsize=11)
ax.text(-t_crit - 0.95, 0.02, f"−t* = {-t_crit:.3f}", color="crimson", fontsize=11)

# p-value region: area beyond the observed t (both tails)
ax.fill_between(x, y, where=(x >= abs(t_stat)), color="navy", alpha=0.45)
ax.fill_between(x, y, where=(x <= -abs(t_stat)), color="navy", alpha=0.45)

# Observed t
ax.axvline(t_stat, color="navy", linewidth=2.6,
           label=f"observed t = {t_stat:.3f}  (p = {p_value:.4f})")

ax.axvline(0, color="grey", linewidth=1)
ax.text(0.02, max(y) * 0.93, "H₀ says the difference is 0 here",
        fontsize=9, color="grey")

ax.set_xlabel("t-statistic (standard errors away from zero)")
ax.set_ylabel("Probability density")
ax.set_title(f"Where our result lands on the t-distribution (df={df_free})")
ax.legend(loc="upper right", fontsize=9)
plt.tight_layout()
plt.savefig("graph3_t_distribution.png", dpi=150)
plt.show()
```

**This single chart contains the entire logic of the test. Read it slowly:**

| Element                            | Meaning                                                                                                                                 |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **The black bell curve**           | The distribution of the t-statistic **if H₀ were true** — i.e. if the two pages were genuinely identical                                |
| **Zero in the middle**             | "No difference". If H₀ is true, our t would most often land near here                                                                   |
| **Red shaded tails**               | The **rejection regions** — the 5% of the curve where we agree to call a result "real". Anything landing here is too extreme to be luck |
| **Red dashed lines at ±t\***       | The **critical values**, e.g. ±1.980. These lines are the decision boundary                                                             |
| **Navy vertical line at t = 2.39** | Our **observed** t-statistic, drawn on the same ruler                                                                                   |
| **Navy shaded area**               | The **p-value** (≈ 0.019) — the probability of landing this far out or further, under H₀                                                |

**The conclusion reads directly off the picture:** the navy line is _to the right of_ the red dashed line, i.e. it sits **inside the red rejection region** → **REJECT H₀**.

If the navy line had landed at, say, 1.4 — between the centre and the red line, in the white "do not reject" zone — the p-value area would have been much larger than 0.05 and we would keep H₀.

### Step 11 — Graph 4: Building intuition with a simulation

This is the graph that makes beginners finally "get" the standard error.

```python
# ============================================================
# GRAPH 4 — Simulating H0: what "pure luck" looks like
# ============================================================
n_sims = 20000
sim_diffs = np.empty(n_sims)

for i in range(n_sims):
    # Both groups drawn from the SAME distribution -> H0 is true by construction
    g1 = np.random.normal(0, pooled_sd, n1)
    g2 = np.random.normal(0, pooled_sd, n2)
    sim_diffs[i] = g2.mean() - g1.mean()

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.hist(sim_diffs, bins=70, color="#6C8EBF", alpha=0.75, edgecolor="white",
        density=True, label=f"{n_sims:,} simulated experiments under H₀")

# The theoretical null distribution (normal with SE as its SD)
xs = np.linspace(sim_diffs.min(), sim_diffs.max(), 500)
ax.plot(xs, stats.norm.pdf(xs, 0, se), color="black", linewidth=2,
        label=f"theory: Normal(0, SE=${se:.2f})")

# Critical boundaries expressed in DOLLARS (this is the visual 'aha')
ax.axvline(-t_crit * se, color="crimson", linestyle="--", linewidth=2,
           label=f"critical boundaries (±t*×SE = ±${t_crit*se:.2f})")
ax.axvline( t_crit * se, color="crimson", linestyle="--", linewidth=2)

# Our actual observed difference
ax.axvline(diff, color="navy", linewidth=2.8,
           label=f"our observed difference = ${diff:.2f}")

ax.set_xlabel("Difference in average order value ($) under H₀ (no real effect)")
ax.set_ylabel("Density")
ax.set_title("What pure luck looks like: 20,000 experiments where both pages are identical")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("graph4_null_simulation.png", dpi=150)
plt.show()
```

**Why this graph is powerful:**

- Every simulated experiment drew **both** groups from the **same** distribution. So we _know_ there is no real effect. Any difference in the chart is pure luck.
- The histogram's spread shows the natural wobble: differences of ±$2–3 appear all the time just by chance.
- The red dashed lines are the **critical values translated back into dollars**. They say: _"95% of the time, pure luck produces a difference smaller than about ±$4.4."_
- Our observed difference (navy line) sits **outside** those boundaries → random luck would rarely do that → we reject H₀.
- The histogram's standard deviation should be ≈ `se`, confirming that the standard error really is "the typical size of random wobble".

> **Try this experiment:** change `n1` and `n2` to 10 and re-run. The histogram becomes much wider → the critical boundaries move outward → bigger samples make it _easier_ to detect the same difference. That is statistical power, visualised.

---

## 8. Reporting the Result — The Sentence That Goes in the Deck

```
An independent samples t-test compared average order value between the
control (old landing page, n = 60) and treatment (new landing page, n = 65)
groups. The new page produced a statistically significant increase in AOV
of $6.40 (95% CI: $1.10 to $11.70), t(123) = 2.39, p = 0.018, Cohen's d = 0.43.

Interpretation: the effect looks real and is medium-sized. Estimated monthly
impact at 200,000 orders is roughly $220K, with a plausible range of $50K
to $2.3M. Recommendation: roll out to 50% of traffic for two more weeks to
tighten the confidence interval before a full launch.
```

Notice the structure — **statistic → effect size → CI → business impact → recommendation**. That is the professional format.

---

## 9. Real Company Use Cases

Each scenario below follows the same template: **metric → groups → hypotheses → decision → cost of being wrong**.

### Use Case 1 — E-commerce (conversion _value_, not conversion rate)

**Company:** StyleHub, an online fashion retailer.
**Question:** Does the redesigned checkout page increase average order value?
**Metric:** Order value in dollars (continuous ✅ suitable for a t-test).
**Groups:** 12,000 shoppers randomly split — old checkout vs new checkout.
**Hypotheses:**

- H₀: μ_new = μ_old (no difference in AOV)
- H₁: μ_new ≠ μ_old (two-sided — we would also want to know if it _hurts_)
- α = 0.05

**Decision:** If t crosses the critical value **and** Cohen's d ≥ 0.2, roll out to 100%.

**Cost of a Type I error (false positive):** You ship a checkout page that does not actually help. You pay engineering and QA costs, and may even lose revenue if the sample was a fluke.
**Cost of a Type II error (false negative):** You keep the old page, leaving an estimated $200K+/month on the table.

> ⚠️ **Important nuance:** if your metric were **conversion rate** (a percentage: ordered / didn't order), the independent t-test is the _wrong_ tool — use a **chi-square test** or a **two-proportion z-test** instead. t-tests are for continuous outcomes (revenue per user, order value, time on site).

### Use Case 2 — SaaS onboarding (time-to-value)

**Company:** CloudDesk, a B2B dashboard tool.
**Question:** Does the new guided onboarding wizard reduce the time it takes a new user to reach their "first value moment"?
**Metric:** Minutes from signup to first dashboard created.
**Groups:** 400 new signups — self-serve onboarding vs guided wizard.
**Hypotheses:** H₀: μ_guided = μ_self; H₁: μ_guided < μ_self (**one-sided**, because faster is the only direction that matters and we want more statistical power).

**Business link:** CloudDesk knows from past analysis that every 24 hours saved in onboarding correlates with a 4-percentage-point lift in 90-day retention. A statistically significant reduction of, say, 35 minutes looks small in isolation but compounds across thousands of signups.

**Why the critical value matters here:** because the test is one-sided, the critical value is `ppf(1−0.05, df)` ≈ 1.65 instead of ~1.96. A smaller hurdle — deliberately chosen _before_ the data was seen, in exchange for giving up the ability to detect "guided is worse".

### Use Case 3 — Clinical / Pharmaceutical (the highest-stakes version)

**Company:** a biotech firm running a Phase III trial.
**Question:** Does the new drug lower systolic blood pressure more than placebo?
**Metric:** Change in systolic BP (mmHg) after 12 weeks.
**Groups:** 500 patients randomized to drug vs placebo (independent groups — a patient cannot be in both arms).
**Hypotheses:** H₀: μ_drug = μ_placebo; H₁: μ_drug ≠ μ_placebo. **α = 0.05 is often tightened to 0.01 or lower**, and regulators require pre-registered analysis plans.

**What changes versus a business A/B test:**

- The **consequences of error are asymmetric and severe** — a false positive could harm patients; a false negative could deny them a working treatment.
- The **confidence interval matters more than the p-value** — regulators want to know the _range_ of plausible effect sizes.
- **Statistical significance alone is never enough** — a 1 mmHg reduction could be "significant" with 50,000 patients while being clinically meaningless. Minimum clinically important difference (MCID) thresholds are set in advance.
- Assumption checks (normality, variance) are documented rigorously, and non-parametric backups are pre-specified.

### Use Case 4 — Manufacturing quality control

**Company:** Northwind Components, which buys steel bolts from two suppliers.
**Question:** Do bolts from Supplier A and Supplier B have the same mean tensile strength?
**Metric:** Tensile strength in kN (continuous).
**Groups:** 40 randomly sampled bolts from each supplier's latest batch.
**Hypotheses:** H₀: μ_A = μ_B; H₁: μ_A ≠ μ_B.
**Extra check:** **Levene's test** is critical here — manufacturing processes often produce unequal variances, and a pooled t-test would then be misleading. If Levene's p < 0.05, use **Welch's** test.

**Business action:** A significant difference with a large effect size justifies renegotiating the contract, tightening incoming inspection, or switching suppliers. A significant difference with a tiny effect size (d = 0.05) might be statistically real but irrelevant — the bolts are both within engineering tolerance, and switching suppliers would cost more than it saves.

### Use Case 5 — People analytics / retail operations

**Company:** MartSave, a supermarket chain.
**Question:** Did the new sales training program improve performance?
**Metric:** Weekly sales per sales representative, in dollars.
**Groups:** 25 reps who completed the training vs 30 reps in matched stores who did not.
**Hypotheses:** H₀: μ_trained = μ_untrained; H₁: μ_trained > μ_untrained (one-sided).

**The independence trap:** if you had measured each rep's sales _before and after_ training, the observations would be **paired**, and you would need a **paired t-test**. Here the two groups are different people, so the independent t-test is correct.

**Business link:** Suppose the difference is $620/week/report with d = 0.55. Across 900 reps in the chain, that is ~$558K/week in attributable sales. Compare that to the program's cost — that comparison, not the p-value, is what funds the program next quarter.

### Use Case 6 — A "not significant" result that is still valuable

**Company:** CallWave, a telecom provider.
**Question:** Does a new call-centre script reduce average handling time?
**Result:** t = 1.21, df = 178, critical value (two-sided, α = 0.05) = 1.973, p = 0.23. **Fail to reject H₀.**

**How a beginner might misread this:** "The script does nothing."
**How a professional reads it:** "We have no evidence that the script changes handling time. Either the effect is genuinely zero, or it exists but our sample is too small to detect it."

**The follow-up analysis** is exactly what the CI is for: if the 95% CI is [−8 seconds, +41 seconds], the data is compatible with a meaningful improvement _and_ a meaningful regression. The correct business call is **not** "abandon" but "we need a larger sample to resolve this range" — and you can compute the required sample size using a **power analysis**.

**Lesson:** a non-significant p-value is a statement about _evidence_, not about _truth_. Always pair it with the confidence interval.

---

## 10. When NOT to Use the Independent Samples T-Test

| Situation                                                                | Correct test instead                                                                               |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| Same subjects measured twice (before/after)                              | **Paired t-test** (`stats.ttest_rel`)                                                              |
| Comparing **proportions / conversion rates**                             | **Two-proportion z-test** or **chi-square**                                                        |
| Three or more groups                                                     | **One-way ANOVA** (`stats.f_oneway`) + post-hoc tests                                              |
| Data badly skewed, or many outliers, small n                             | **Mann-Whitney U test** (`stats.mannwhitneyu`)                                                     |
| You already looked at the data and kept testing until it was significant | Nothing — your α is invalid. Pre-register and re-run                                               |
| Repeatedly checking the p-value as data arrives                          | Use **sequential testing** or **always-valid** methods; peeking inflates Type I error dramatically |
| Testing 20 metrics at once and celebrating the one with p < 0.05         | Apply a **multiple-testing correction** (Bonferroni or Benjamini–Hochberg)                         |

---

## 11. Common Beginner Mistakes Checklist

1. **Using `np.std()` instead of `np.std(ddof=1)`** — your manual t will be wrong. pandas' `.std()` is already correct.
2. **Comparing p to the t-statistic** — p is a probability (0 to 1); t is a distance (can be any size, negative or positive). Compare p to α, and |t| to t\*.
3. **Forgetting that t can be negative** — the sign just tells you which group is bigger. For a two-sided test, always use the absolute value.
4. **Confusing "not significant" with "no effect"** — check the confidence interval width before concluding anything.
5. **Ignoring effect size** — with a huge n, a trivial difference becomes "significant".
6. **Skipping assumption checks** — especially Levene's test when group sizes are unequal.
7. **Choosing the tail after seeing the data** — that silently doubles your false-positive rate.
8. **Testing conversion rates with a t-test** — the metric must be continuous.
9. **Stopping the experiment the moment p < 0.05** — peeking without correction is the single most common cause of A/B tests that fail to replicate.
10. **Confusing statistical significance with business significance** — always translate to dollars, patients, or minutes.

---

## 12. Quick Reference Cheat Sheet

```python
from scipy import stats
import numpy as np

# --- The test ---
t, p = stats.ttest_ind(group2, group1, equal_var=True)      # Student's
t, p = stats.ttest_ind(group2, group1, equal_var=False)     # Welch's
t, p = stats.ttest_ind(group2, group1, alternative="greater")  # one-sided

# --- Critical value ---
df   = n1 + n2 - 2
tcrit = stats.t.ppf(1 - alpha/2, df)     # two-sided
tcrit = stats.t.ppf(1 - alpha,   df)     # one-sided

# --- Decision ---
significant = abs(t) > tcrit             # identical to: p < alpha

# --- Effect size ---
d = (m2 - m1) / pooled_sd

# --- Confidence interval ---
se = pooled_sd * np.sqrt(1/n1 + 1/n2)
ci = (m2 - m1) + np.array([-1, 1]) * tcrit * se

# --- Assumption checks ---
stats.shapiro(group)                 # normality (p > .05 = OK)
stats.levene(group1, group2)         # equal variances (p > .05 = OK)
```

**The decision table, one more time:**

|           | \|t\| > t\*                | \|t\| ≤ t\*                            |
| --------- | -------------------------- | -------------------------------------- |
| **p < α** | ✅ Reject H₀ — significant | _(impossible — they always agree)_     |
| **p ≥ α** | _(impossible)_             | ❌ Fail to reject H₀ — not significant |

---

## 13. Practice Exercises

**Exercise 1 — Direction of the difference**
You run `stats.ttest_ind(control, treatment)` and get `t = -3.1`. Which group has the higher mean, and what would the t-statistic be if you swapped the argument order?

**Exercise 2 — Same difference, different samples**
Study A: difference = $5.00, SE = $4.00. Study B: difference = $5.00, SE = $1.20.
Compute both t-statistics. With df = 100 (t\* = 1.984), which is significant? What does this teach you about sample size?

**Exercise 3 — Critical value reasoning**
For a two-sided test with α = 0.01 and df = 20, would `t*` be larger or smaller than 2.086 (the α = 0.05 value)? Verify with `stats.t.ppf`.

**Exercise 4 — The p-hacking trap**
You test 10 different metrics on the same experiment. You only report the one with p = 0.04. Using α = 0.05, roughly how likely is it that at least one metric shows p < 0.05 by chance alone? (Hint: 1 − 0.95¹⁰.)

**Exercise 5 — Real-world framing**
A test returns t = 2.05, df = 500, t\* = 1.965, p = 0.041, d = 0.03, CI = [0.02, 1.10] dollars. Do you ship it? Write the two-sentence recommendation you would send to a VP.

<details>
<summary><b>Answers (click to expand)</b></summary>

1. `t = -3.1` with `control` first means control's mean is **higher** by 3.1 standard errors. Swapping the order flips the sign: `t = +3.1`. The p-value and the conclusion are unchanged.
2. Study A: t = 5.00/4.00 = **1.25** → not significant. Study B: t = 5.00/1.20 = **4.17** → significant. Same dollar difference, opposite conclusions. Smaller standard error (achieved with larger n or less noisy data) makes real effects detectable.
3. **Larger** — a smaller α needs more extreme evidence. `stats.t.ppf(0.995, 20) = 2.845`.
4. 1 − 0.95¹⁰ ≈ **0.40** — a 40% chance of at least one false positive. This is why corrections like Benjamini–Hochberg exist.
5. Technically significant, but d = 0.03 is negligible and the CI bottom is $0.02. Ship only if it is essentially free to implement. Example: _"The difference is statistically significant but tiny in practice (d = 0.03, CI $0.02–$1.10). I would not prioritise a rollout unless the change costs nothing to maintain; our engineering time is better spent elsewhere."_

</details>

---

## 14. Final Recap — The Five Things to Remember

1. **A difference in sample means is not automatically a real effect.** The t-test asks whether it is too large to be luck.
2. **The t-statistic is signal ÷ noise.** Numerator = mean difference. Denominator = standard error of that difference.
3. **The critical value is the line on the t-distribution.** For a two-sided α = 0.05 test it is around 2 (a bit more for small samples, a bit less for huge ones). |t| > t\* → reject H₀.
4. **The p-value and the critical value are the same decision.** One is an area, the other is a boundary. Report p, but _think_ in curves.
5. **Significance is not importance.** Always report effect size (Cohen's d) and the confidence interval, then translate into dollars, minutes, or patients before recommending action.

---

_End of tutorial. Files generated when you run the code: `graph1_boxplot.png`, `graph2_histograms.png`, `graph3_t_distribution.png`, `graph4_null_simulation.png`._

```

**How to use this file:** paste it into `independent_samples_ttest.md`, run the code blocks in order (top to bottom) in Jupyter or VS Code, and the four PNGs will appear in your working folder. If you'd like, I can also produce a **paired t-test** or **Mann-Whitney U** companion guide in the same structure.
```
