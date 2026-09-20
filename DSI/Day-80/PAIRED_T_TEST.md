# Paired Sample T-Test in Python

### A beginner-friendly walkthrough with business use cases

---

## 1. What is a Paired Sample T-Test?

A paired sample t-test (also called a _dependent_ or _matched_ t-test) compares the
**means of two samples where every observation in one sample is linked to exactly one
observation in the other**.

| Paired (this test)                            | Independent (two-sample t-test)                                  |
| --------------------------------------------- | ---------------------------------------------------------------- |
| Same 100 customers measured in Jan and in Feb | 100 customers in group A vs 100 _different_ customers in group B |
| Same 20 stores before vs after a price change | 20 trial stores vs 20 different control stores                   |
| Same model before vs after retraining         | Model A vs Model B on different test sets                        |

**Why it matters:** the test works on the _difference within each pair_. Each subject is
its own control, so all the stable noise (a big spender is always a big spender, a busy
store is always busy) cancels out. That makes the paired test far more powerful than an
independent test on the same data — you can detect a smaller real effect with the same
number of observations.

**The one-line intuition:** instead of comparing two groups, you compute one new variable
— _the change per unit_ — and test whether its average is different from zero.

---

## 2. The sample file

```python
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel, norm

# 1. Mock data: 100 units measured "before" and "after"
before = norm.rvs(loc=500, scale=100, size=100, random_state=42).astype(int)

np.random.seed(42)
after = before + np.random.randint(low=-50, high=75, size=100)

# 2. Visualise
os.makedirs("plots", exist_ok=True)
plt.hist(before, density=True, alpha=0.5, label="Before")
plt.hist(after,  density=True, alpha=0.5, label="After")
plt.legend()
plt.savefig("plots/paired_sample_t_test.png", dpi=300, bbox_inches="tight")
plt.show()

# 3. Descriptives
before_mean, after_mean = before.mean(), after.mean()
print(before_mean, after_mean)

# 4. Hypotheses
null_hypothesis      = "The mean of the Before sample is equal to the mean of the After sample"
alternate_hypothesis = "The mean of the Before is different to the mean of the After"
acceptance_criteria  = 0.05

# 5. Test
t_statistic, p_value = ttest_rel(before, after)
print(t_statistic, p_value)

# 6. Decision
if p_value <= acceptance_criteria:
    print(f"p={p_value} <= {acceptance_criteria} -> reject H0: {alternate_hypothesis}")
else:
    print(f"p={p_value} > {acceptance_criteria} -> retain H0: {null_hypothesis}")
```

---

## 3. Line-by-line / block-by-block walkthrough

### 3.1 Imports

| Line                                      | What it does                                                                            |
| ----------------------------------------- | --------------------------------------------------------------------------------------- |
| `import os`                               | Standard library; creates the `plots/` folder so `savefig` never fails.                 |
| `import numpy as np`                      | Array maths + `np.random` for generating the mock data.                                 |
| `import matplotlib.pyplot as plt`         | Histograms, legends, saving and showing figures.                                        |
| `from scipy.stats import ttest_rel, norm` | `ttest_rel` is the paired t-test; `norm.rvs` fabricates normally-distributed fake data. |

### 3.2 Building the mock data (the conceptual heart of the file)

```python
before = norm.rvs(loc=500, scale=100, size=100, random_state=42).astype(int)
```

Draws 100 values from a Normal distribution with mean **500** and standard deviation
**100**, then truncates them to integers. `random_state=42` makes the result reproducible
— rerun the script and you get identical numbers, which is how you make a tutorial
verifiable.

```python
np.random.seed(42)
after = before + np.random.randint(low=-50, high=75, size=100)
```

This is where the _pairing_ is created. `randint(low=-50, high=75, size=100)` returns 100
whole numbers from **−50 to 74** (low inclusive, high exclusive), i.e. an average change
of about **+12**. Adding those changes to `before` — element by element — produces an
`after` sample whose _i_-th value is derived from the _i_-th `before` value. That shared
index is the pairing. If you shuffled `after` before testing, you would destroy it.

> Real-world equivalent: a SQL join on customer_id, store_id or machine_id where the
> "before" row and "after" row carry the same key.

### 3.3 The histogram — how to read it

```python
plt.hist(before, density=True, alpha=0.5, label="Before")
plt.hist(after,  density=True, alpha=0.5, label="After")
plt.legend()
```

- `density=True` makes the y-axis a **probability density** (total bar area = 1), so the
  two shapes are directly comparable.
- `alpha=0.5` gives 50% transparency so the overlap region is visible in a blend of the
  two colours.
- What you see: two bell shapes whose centres are a little over 10 apart with a large
  overlapping area. **That overlap is the whole point of the graph** — looking only at the
  two distributions, the difference looks modest. The paired test becomes powerful
  precisely because it ignores the between-unit spread and looks at the shift _within_
  each pair.

`plt.savefig(..., dpi=300, bbox_inches="tight")` must come **before** `plt.show()`:
`show()` hands the figure to the GUI backend, and saving afterwards can write a blank
image. `dpi=300` = print/slide quality, `bbox_inches="tight"` crops the white margin.

### 3.4 Descriptives

```python
before_mean, after_mean = before.mean(), after.mean()
print(before_mean, after_mean)
```

Sanity check before any statistics: the gap between the two means is your _raw effect
size_ (expected ≈ +12 here). Mean difference alone is never enough — you still need to
know whether a gap that size could plausibly be noise.

### 3.5 Hypotheses and the decision rule

- **H₀ (null):** the before and after means are equal → any observed gap is chance.
- **H₁ (alternative):** the means are different → a _two-sided_ claim (the code would also
  say "different" if the number went down).
- **α = 0.05:** we accept a 5% risk of a false positive (declaring an effect that isn't
  there — a Type I error). The p-value is the probability of seeing a difference at least
  this extreme _if H₀ were true_.

Decision rule: `p ≤ 0.05 → reject H₀`; `p > 0.05 → retain H₀`.

### 3.6 The test itself

```python
t_statistic, p_value = ttest_rel(before, after)
print(t_statistic, p_value)
```

`ttest_rel(a, b)` tests whether `a − b` has a mean of zero, using `df = n − 1 = 99` and a
two-sided p-value. Reading the printed pair:

- **t statistic** — how many standard errors the average change sits away from zero.
  Sign = direction (negatively signed here because `before − after` averages ≈ −12).
- **p-value** — with this seed, ≈ **0.001**. Below 0.05, so the script rejects H₀ and
  prints the alternative hypothesis.

Note the printed wording: a small p-value means _the data are unlikely under H₀_, not that
H₁ is proven, and not that the effect is large or important.

---

## 4. Formula breakdown, piece by piece

The test is just a one-sample t-test applied to a new column of _differences_.

**Step 1 — the per-unit difference**

```
d_i = x_after,i − x_before,i          (one number per customer / store / machine)
```

**Step 2 — the average change (the effect)**

```
d̄ = (1 / n) · Σ d_i                    n = number of pairs
```

**Step 3 — the spread of the changes**

```
s_d = sqrt( Σ (d_i − d̄)² / (n − 1) )
```

Note what is _absent_: the spread of `before` and the spread of `after` themselves. Only
the variability of the **within-pair change** enters the formula. That is the mathematical
source of the paired test's extra power — the large 100-point between-customer spread in
our mock data gets differenced away.

**Step 4 — standard error and test statistic**

```
SE  = s_d / √n
t   = d̄ / SE  =  d̄ · √n / s_d          df = n − 1
```

**Step 5 — effect size (always report it next to the p-value)**

```
Cohen's d_z = d̄ / s_d        (~0.2 small, ~0.5 medium, ~0.8 large)
```

**Step 6 — confidence interval**

```
CI = d̄ ± t_crit(0.975, n−1) · SE
```

A useful shorthand: `t ≈ 2` at n ≈ 100 means roughly "the effect is about two standard
errors away from zero", which is generally the edge of significance.

Hand-check on the mock data (approximate): `d̄ ≈ −12`, `s_d ≈ 36`, `n = 100`,
so `SE ≈ 3.6`, `t ≈ −3.3`, `p ≈ 0.001`, `d_z ≈ 0.33`.

### Assumptions to check before trusting the result

1. **Pairs are genuinely matched** — the same unit measured twice. This is a design
   property, not something the test can verify for you.
2. **The differences are approximately normally distributed** — check the histogram of
   `after - before`. With n = 100 the Central Limit Theorem covers mild violations; with
   n < 30 check properly. For badly skewed counts use the Wilcoxon signed-rank test
   (`scipy.stats.wilcoxon`).
3. **No serious outliers in the differences** — one extreme pair can drive the whole
   result; inspect and, if needed, report the test with and without it.
4. **Independence between pairs** — pair 1 shouldn't influence pair 2.

### Quick power-planning numbers

Detecting a paired effect of `d_z = 0.3` at α = 0.05 with 80% power needs roughly
**90 pairs**; `d_z = 0.5` needs roughly **34 pairs**. Because pairing absorbs noise, the
paired test usually needs a fraction of the sample an independent test would require.

---

## 5. Real company use cases

The pattern is always the same: **one business unit, two moments in time, one KPI.**
Join the two measurements on the unit key, then run the paired test on the difference.

| #   | Industry / function   | Paired unit                        | Before vs After                                                              | Business decision it informs              |
| --- | --------------------- | ---------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------- |
| 1   | E-commerce / growth   | The same 5,000 customers           | Average order value 4 weeks before vs 4 weeks after a free-shipping campaign | Keep, scale or kill the campaign          |
| 2   | Retail / pricing      | The same 300 stores                | Weekly units sold before vs after a price change                             | Confirm the price rise didn't dent volume |
| 3   | SaaS / product        | The same accounts                  | Seats per account before vs after a new onboarding wizard                    | Ship the feature to all tenants           |
| 4   | HR / L&D              | The same 120 employees             | Test score before vs after a training programme                              | Justify the training budget               |
| 5   | Manufacturing / ops   | The same 40 production lines       | Defect rate before vs after a retooling / maintenance change                 | Approve rollout to remaining lines        |
| 6   | Marketing / brand     | The same 500 respondents           | Brand-awareness score before vs after an ad flight                           | Renegotiate or renew the media buy        |
| 7   | Call centre / service | The same 60 agents                 | Average handle time before vs after a new script                             | Standardise the script across the floor   |
| 8   | Clinical / pharma     | The same 80 patients               | Biomarker at baseline vs at week 12                                          | Primary endpoint in a single-arm trial    |
| 9   | Data science / ML     | The same test set                  | Model error before vs after retraining                                       | Promote the new model to production       |
| 10  | Finance / collections | The same 1,000 delinquent accounts | Balance before vs after a new reminder SMS                                   | Roll the reminder out portfolio-wide      |

### Worked use case 1 — Campaign uplift for an e-commerce team

**Setup.** The CRM team sent a personalised voucher to 4,000 existing customers. They
recorded each customer's spend in the 30 days before and the 30 days after the send.
**Why paired.** Comparing these 4,000 customers against the whole customer base would be
misleading: voucher recipients are self-selected high-value customers. Measuring the same
customers across two windows removes that selection bias from the comparison.

```python
import pandas as pd
from scipy.stats import ttest_rel

df = pd.read_csv("campaign_before_after.csv")   # columns: customer_id, before, after

t, p = ttest_rel(df["after"], df["before"])
lift   = (df["after"] - df["before"]).mean()
lift_% = lift / df["before"].mean() * 100

print(f"Lift: {lift:.2f} per customer ({lift_%:.1f}%),  t={t:.2f}, p={p:.4f}")
```

**Decision.** If p ≤ 0.05 and the lift comfortably exceeds the cost of the voucher, the
campaign scales. The size of the lift (`lift`, `lift_%`) is what drives the ROI number you
present; the p-value only tells you it isn't noise.

### Worked use case 2 — Process change in operations

**Setup.** A plant introduced a new calibration routine in 50 production lines and records
the defect rate per shift before and after.
**Paired analysis** asks: "did each line improve?" rather than "is the average defect rate
different from some other group?" — which is exactly the question the plant manager is
asked in the review meeting. Because lines with a natural low defect rate stay low, pairing
removes that baseline variation and lets a 0.4 pp improvement show up as significant.

### Worked use case 3 — Model retraining for a data team

**Setup.** Old model vs retrained model on the same 2,000 labelled test cases
(**same cases = paired**).
**Paired test on per-case errors / losses** checks whether the retrained model really is
better, not merely lucky on a different sample. This is the standard way to justify a
production model swap when the accuracy gain looks small (e.g. +0.6 pp) — pairing is what
makes such a small gain detectable.

### Worked use case 4 — Pricing / revenue management

**Setup.** 500 SKUs had a price increase. Compare units sold in the 8 weeks before vs after.
**Caveat to state in the deck:** a before/after paired test has no control group, so it
cannot separate the price effect from seasonality, promotions or market shifts. Pair it
with a holdout set of unchanged SKUs, or use a difference-in-differences design, if you
need causal proof rather than directional evidence.

---

## 6. Reporting template for a business audience

> _"We compared the same N units before and after the change. The average KPI moved from
> X to Y, a change of Z (W%). A paired sample t-test gives t = …, p = … . Since p is below
> / above our 0.05 threshold, we conclude the change is likely real / indistinguishable
> from normal variation. Effect size (Cohen's d_z) = …, 95% CI on the change = […, …]."_

Three things to always include: **the direction and size of the change**, **the p-value**,
and **the confidence interval** (a wide CI means "we know it moved up, but not by how
much" — which matters more to the business than the p-value itself).

---

## 7. Common pitfalls

1. **Using `ttest_ind` on paired data** — the single most common mistake. It throws away
   the pairing and can turn a real effect into a non-significant one.
2. **Breaking the pairing** by shuffling, sorting or dropping rows from only one side.
   Keep both columns in the same row order and drop incomplete pairs together.
3. **Treating p < 0.05 as "big"** — with n = 10,000 even a trivial 0.1% change is
   significant. Always look at the effect size.
4. **Reporting p > 0.05 as "no effect"** — it means "not proven", which is not the same.
5. **Ignoring the assumption of normality on the differences** for small n.
6. **Saving the figure after `plt.show()`** — always `savefig` first (fixed in this file).
7. **Confusing the paired test with a true experiment** — before/after with no control
   group cannot rule out everything else that changed at the same time.

---

## 8. Try-it-yourself extensions

- Swap `ttest_rel` for `scipy.stats.wilcoxon(before, after)` — the non-parametric version
  for skewed differences.
- Add the effect size and a 95% CI:

  ```python
  from scipy import stats
  d = after - before
  t, p = stats.ttest_rel(after, before)
  se   = d.std(ddof=1) / len(d) ** 0.5
  ci   = stats.t.interval(0.95, len(d) - 1, loc=d.mean(), scale=se)
  print(f"mean change={d.mean():.2f}, 95% CI={ci}, p={p:.4f}")
  ```

- Replace the mock data with your own CSV and join on the unit key:

  ```python
  df = pd.read_csv("your_data.csv")
  t, p = ttest_rel(df["after"], df["before"])
  ```

- Re-run the simulation with `size=20` or `size=10` to see how quickly a paired test loses
  power as the number of pairs shrinks.

---

## 9. Key takeaways

1. Use a paired t-test when the same unit is measured twice — it is a one-sample t-test on
   the differences.
2. Pairing removes between-unit noise, so it detects smaller real effects than an
   independent test on the same data.
3. Report the p-value **and** the effect size **and** the confidence interval.
4. Before/after with no control group proves association, not causation — say so in the
   business write-up.
5. The output of this analysis is a decision: keep, scale, or kill the change.
