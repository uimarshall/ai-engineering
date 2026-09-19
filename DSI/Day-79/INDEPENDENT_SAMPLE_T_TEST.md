# Independent-Samples T-Test — Beginner's Guide

This document explains `independent_sample_t_test.py` line by line, in plain
language, describes the bug that was causing `nan` results, and shows how the
same technique is used inside real companies.

## What problem is this script solving?

Sometimes you have **two separate, unrelated groups** (e.g. Group A never
interacts with or overlaps with Group B) and you want to know:

> "Is the average of Group A actually different from the average of Group B,
> or could the difference we see just be random chance?"

This is different from the one-sample t-test (Day-78), which compares one
sample against a single known reference value. Here we compare **two
samples** against **each other**.

---

## Imports

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, ttest_ind
from typing import cast
```

| Name                           | What it is                                                                                                                    | Why we need it                                                                                                          |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `matplotlib.pyplot` (as `plt`) | A charting library.                                                                                                           | Draws histograms so we can _see_ both groups' distributions.                                                            |
| `numpy` (as `np`)              | A numerical computing library — arrays + math + random number generation.                                                     | Builds and manipulates the sample arrays.                                                                               |
| `norm`                         | An object from `scipy.stats` representing the **Normal distribution** (bell curve), defined by a mean and standard deviation. | Fabricates two realistic, bell-shaped fake samples.                                                                     |
| `ttest_ind`                    | A function from `scipy.stats` that performs the **independent two-sample t-test**.                                            | The actual statistical test comparing Group A's mean to Group B's mean.                                                 |
| `cast`                         | A `typing` helper.                                                                                                            | Tells the type checker (Pylance) "trust me, this is a `float`" — no effect at runtime, only silences false type errors. |

---

## Creating the two mock samples

```python
sample_A = np.asarray(
    norm.rvs(loc=500, scale=100, size=250, random_state=42)
).astype(int)
sample_B = np.asarray(
    norm.rvs(loc=550, scale=150, size=100, random_state=42)
).astype(int)
```

- **`norm`** — the Normal/Gaussian distribution "recipe", described by a mean
  and a standard deviation.
- **`.rvs(...)`** — short for **R**andom **V**ariate**S**; actually draws
  random numbers from the distribution.
  - `loc` — the mean (centre) of that group's bell curve. Sample A is
    centred on 500, Sample B on 550 — deliberately different, so we'd expect
    the test to detect a real difference.
  - `scale` — the standard deviation (spread) of that group's bell curve.
    Sample A has `scale=100`, Sample B has `scale=150` (more spread out) —
    the two groups don't need equal spread or equal size for this test.
  - `size` — how many random values to generate for that group (250 for A,
    100 for B). Independent-samples t-tests do **not** require equal group
    sizes.
  - `random_state=42` — fixes the seed so the "random" numbers are the same
    every run (reproducibility).
- **`np.asarray(...)`** — ensures the result is treated as a proper array
  (already is; mainly keeps type checkers happy).
- **`.astype(int)`** — converts the decimal values into whole numbers, since
  these represent whole-number measurements.

---

## Visualising the data

```python
plt.hist(sample_A, density=True, alpha=0.5)
plt.hist(sample_B, density=True, alpha=0.5)
plt.show()
```

- **`plt.hist(data, ...)`** — buckets numeric values into bins and draws a
  bar per bin.
- **`density=True`** — scales bars so the total area equals 1, making it fair
  to compare two histograms of different group sizes (250 vs 100 points).
- **`alpha=0.5`** — 50% transparency, so overlapping bars from both
  histograms remain visible.
- **`plt.show()`** — renders the chart window.

---

## The bug that caused `nan`

The original code did this **before** running the t-test:

```python
sample_A = sample_A.mean()   # ❌ overwrites the array with a single number
sample_B = sample_B.mean()   # ❌ overwrites the array with a single number
...
t_statistic, p_value = ttest_ind(sample_A, sample_B)  # now receives 2 scalars, not 2 arrays
```

`sample_A.mean()` returns a single number (e.g. `501.2`). By reassigning that
number back into `sample_A`, the original 250-value array was **destroyed**
and replaced by one lone value. The same happened to `sample_B`.

`ttest_ind` then received two "samples" that each contained exactly **one
data point**. A t-test needs to estimate each group's internal variance
(how spread out its values are) to work out the standard error — but variance
of a single number is undefined (there's no spread to measure), which SciPy
represents as `nan` (Not a Number). Once variance is `nan`, every downstream
calculation (the t-statistic and the p-value) becomes `nan` too — that's
exactly why `print(t_statistic, p_value)` printed `nan nan`.

**The fix:** keep the full arrays intact for the t-test, and store the means
in separate variables (`sample_A_mean`, `sample_B_mean`) purely for the
`print()` sanity check:

```python
sample_A_mean = sample_A.mean()
sample_B_mean = sample_B.mean()
print(sample_A_mean, sample_B_mean)

...
t_statistic, p_value = ttest_ind(sample_A, sample_B)  # ✅ full arrays, real variance
```

---

## Stating the hypothesis

```python
null_hypothesis = "The mean of the sample A is eaqual to the mean of the sample B"
alternate_hypothesis = (
    "The mean of the sample A is different to the mean of the sample B"
)
acceptance_criteria = 0.05
```

- **Null hypothesis (H0)** — the default assumption: Group A's true mean
  equals Group B's true mean; any observed gap is just random noise.
- **Alternate hypothesis (H1)** — the claim being tested: the two groups'
  true means really are different.
- **`acceptance_criteria = 0.05`** — alpha (α), the significance level: a 5%
  tolerated risk of wrongly rejecting a true null hypothesis. The standard
  default in business and scientific analytics.

---

## Running the test

```python
t_statistic, p_value = ttest_ind(sample_A, sample_B)
t_statistic = cast(float, t_statistic)
p_value = cast(float, p_value)
print(t_statistic, p_value)
```

- **`ttest_ind(sample_A, sample_B)`** — runs the independent two-sample
  t-test. It looks at the difference between the two group means relative to
  how much natural variability exists _within_ each group, and returns:
  - **`t_statistic`** — how many "standard errors" apart the two group means
    are. Larger absolute values mean a bigger difference relative to the
    data's natural spread.
  - **`p_value`** — the probability of seeing a difference this large (or
    larger) if the null hypothesis (no real difference) were true. A small
    p-value is evidence against the null hypothesis.
- **`cast(float, ...)`** — a type-checking hint only (explained above).

---

## Making the decision

```python
if p_value <= acceptance_criteria:
    # reject the null hypothesis — conclude the alternate hypothesis
else:
    # retain the null hypothesis
```

- If `p_value <= 0.05`, the difference between Group A and Group B is
  statistically significant, so we **reject H0** and conclude the two group
  means are genuinely different.
- Otherwise, we **retain H0** — there isn't enough evidence of a real
  difference.

---

## Welch's t-test — a more accurate variant

```python
# WELCH'S T-TEST - More accurate
t_statistic, p_value = ttest_ind(sample_A, sample_B, equal_var=False)
```

The standard (`Student's`) t-test used above makes an assumption: that both
groups share the **same population variance** (spread). To satisfy that
assumption, it "pools" (blends) both groups' variances into one shared
estimate of the standard error.

Our two mock samples don't actually meet that assumption — they were built
with `scale=100` for Sample A and `scale=150` for Sample B (different
spreads), and different sizes (250 vs 100). Pooling variances that are
genuinely different can distort the t-statistic and make the p-value less
trustworthy.

- **`equal_var=False`** — this single argument switches `ttest_ind` from
  Student's t-test to **Welch's t-test**. Instead of pooling, Welch's t-test
  calculates the standard error using each group's **own** variance
  separately, and also adjusts the degrees of freedom to account for the
  mismatch. This makes it robust even when the two groups have unequal
  variances and/or unequal sample sizes.
- Everything else about running and interpreting the test is identical: it
  still returns a `t_statistic` and `p_value`, which are still compared
  against `acceptance_criteria` the same way.

**Rule of thumb:** unless you have a specific, verified reason to believe two
groups have equal variance, `equal_var=False` (Welch's t-test) is the safer
default — it's very rarely worse than Student's t-test, but it protects you
from misleading results when the equal-variance assumption doesn't hold.

---

## Real-world use cases in a company

An independent-samples t-test is used whenever you have **two separate,
unrelated groups** and want to compare their averages:

1. **A/B testing (marketing/product)** — Compare average conversion rate,
   time-on-page, or revenue-per-user between users who saw "Version A" of a
   webpage/email versus users who saw "Version B", to decide which version
   performs better.

2. **Sales channel comparison** — Compare the average deal size closed by
   Sales Team East vs. Sales Team West to see whether one team's approach or
   territory is genuinely producing bigger deals, or if the difference is
   just noise.

3. **Manufacturing/supplier comparison** — Compare the average defect rate or
   component lifespan from Supplier X vs. Supplier Y before deciding which
   supplier to standardize on.

4. **HR/compensation analysis** — Compare the average salary or bonus of one
   demographic/department group against another to check for statistically
   meaningful pay gaps (as opposed to gaps that could just be random
   variation in a small sample).

5. **Customer support** — Compare the average resolution time between
   tickets handled by an in-house team vs. an outsourced team, to evaluate
   whether outsourcing is actually slower or faster.

6. **Clinical trials/pharma** — Compare the average outcome (e.g. blood
   pressure reduction) between a treatment group and a control group to
   assess whether a drug has a real effect.

In each case, the pattern mirrors this script: gather two independent groups,
run `ttest_ind`, and compare the resulting p-value against an acceptance
criteria (commonly 0.05) to decide whether the difference between the two
groups' averages is real or just random noise — while making sure both
groups' **full raw data** (not pre-reduced means) is passed into the test.
