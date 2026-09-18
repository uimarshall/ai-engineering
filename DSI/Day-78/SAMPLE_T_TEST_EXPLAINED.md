# One-Sample T-Test — Beginner's Guide

This document explains `sample_t_test.py` line by line, in plain language, and
shows how the same technique is used inside real companies.

## What problem is this script solving?

We have a **population** (every single measurement that exists, e.g. every
customer's spend). We only have time/money to look at a **sample** (a small
slice of that population). A **one-sample t-test** answers the question:

> "Is the average of my small sample close enough to the average of the whole
> population, or is it actually different?"

---

## Imports

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, ttest_1samp
from typing import cast
```

| Name                           | What it is                                                                                                                                  | Why we need it                                                                                                                         |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `matplotlib.pyplot` (as `plt`) | A charting library.                                                                                                                         | Lets us draw histograms so we can _see_ the two distributions.                                                                         |
| `numpy` (as `np`)              | A numerical computing library — arrays + math + random number generation.                                                                   | Generates and manipulates the population/sample arrays.                                                                                |
| `norm`                         | An object from `scipy.stats` representing the **Normal distribution** (the classic bell curve), defined by a mean and a standard deviation. | We use it to fabricate a realistic, bell-shaped fake population.                                                                       |
| `ttest_1samp`                  | A function from `scipy.stats` that performs the one-sample t-test.                                                                          | This is the actual statistical test used in the script.                                                                                |
| `cast`                         | A `typing` helper.                                                                                                                          | Tells the type checker (Pylance) "trust me, this value is a `float`" — it does nothing at runtime, it only silences false type errors. |

---

## Creating the mock population

```python
population = np.asarray(
    norm.rvs(
        loc=500,
        scale=100,
        size=1000,
        random_state=42,
    )
).astype(int)
```

- **`norm`** — the Normal/Gaussian distribution object. Think of it as a
  "recipe" for a bell curve; on its own it doesn't produce numbers, it just
  describes the shape.
- **`.rvs(...)`** — short for **R**andom **V**ariate**S**. This method
  actually _draws_ random numbers from the distribution described above.
  - `loc=500` — the **location** parameter. For a Normal distribution this is
    the **mean** (the centre of the bell curve). Most generated values will
    cluster around 500.
  - `scale=100` — the **scale** parameter. For a Normal distribution this is
    the **standard deviation** (how "wide" the bell curve is). A bigger
    `scale` means values are more spread out from the mean.
  - `size=1000` — how many random numbers to generate. Here we're pretending
    our "entire population" has 1000 members.
  - `random_state=42` — the random seed. Computers don't generate _true_
    randomness; they use a formula seeded by a starting number. Fixing the
    seed (any number, `42` is just a common convention) means anyone who runs
    this script gets **exactly the same "random" numbers**, which makes the
    example reproducible and debuggable.
- **`np.asarray(...)`** — makes sure the result is a proper NumPy array (it
  already is one here; this mainly keeps type checkers happy and is a no-op
  otherwise).
- **`.astype(int)`** — converts the generated decimal numbers (e.g.
  `503.827`) into whole numbers (e.g. `503`), because our pretend population
  represents whole-number measurements (like an amount in whole currency
  units, or a count).

```python
np.random.seed(42)
sample = np.random.choice(population, 250)
```

- **`np.random.seed(42)`** — fixes NumPy's _global_ random generator seed
  (separate from the `random_state` used above), so the next random
  operation (`np.random.choice`) is also reproducible.
- **`np.random.choice(population, 250)`** — randomly selects 250 values out
  of the 1000-value `population` array. This represents drawing a smaller
  **sample** from the full population — exactly what you'd do in real life
  when you can't measure everyone/everything.

---

## Visualising the data

```python
plt.hist(population, density=True, alpha=0.5)
plt.hist(sample, density=True, alpha=0.5)
plt.show()
```

- **`plt.hist(data, ...)`** — draws a histogram: it buckets the numeric
  values into bins and draws a bar for how many values fall in each bin.
- **`density=True`** — instead of showing raw counts, scales the bars so the
  total area under the histogram equals 1. This makes it possible to fairly
  compare a histogram of 1000 population points against one of only 250
  sample points, since counts alone aren't comparable when group sizes differ.
- **`alpha=0.5`** — sets transparency (0 = invisible, 1 = solid), so when the
  two histograms overlap, both are still visible.
- **`plt.show()`** — opens the chart window and renders everything queued up
  by the `plt.hist(...)` calls above.

---

## Comparing the means

```python
population_mean = population.mean()
sample_mean = sample.mean()
print(population_mean, sample_mean)
```

- **`.mean()`** — a NumPy array method that computes the arithmetic average
  of all values in the array. We compute it for both groups so we can eyeball
  how close the sample's average is to the population's average before doing
  any formal statistics.

---

## Stating the hypothesis

```python
null_hypothesis = "The mean of the sample is eaqual to the mean of the population"
alternate_hypothesis = (
    "The mean of the sample is different to the mean of the population"
)
acceptance_criteria = 0.05
```

- **Null hypothesis (H0)** — the "boring", default assumption: there is _no_
  real difference; any gap we observe between `sample_mean` and
  `population_mean` is just random noise.
- **Alternate hypothesis (H1)** — the claim we're testing for: the sample
  mean really _is_ different from the population mean.
- **`acceptance_criteria = 0.05`** — this is **alpha (α)**, the significance
  level. It means "I'm willing to accept a 5% chance of wrongly rejecting the
  null hypothesis when it's actually true." 0.05 (5%) is the most common
  choice in statistics and business analytics.

---

## Running the test

```python
t_statistic, p_value = ttest_1samp(sample, population_mean)
t_statistic = cast(float, t_statistic)
p_value = cast(float, p_value)
print(t_statistic, p_value)
```

- **`ttest_1samp(sample, population_mean)`** — runs the one-sample t-test. It
  takes your sample data and a reference value (here, the known population
  mean) and tells you how likely it is that a sample like yours could have
  come from a population with that mean, purely by chance.
  - It returns two things:
    - **`t_statistic`** — a number summarising how many "standard errors"
      apart the sample mean is from the reference mean. Larger absolute
      values mean a bigger observed difference relative to the sample's
      natural variability.
    - **`p_value`** — the probability of seeing a difference this large (or
      larger) if the null hypothesis were actually true. Small p-values mean
      "this would be a very unlikely coincidence," which is evidence against
      the null hypothesis.
- **`cast(float, ...)`** — purely a type-checking hint (explained above);
  functionally identical to the original values.

---

## Making the decision

```python
if p_value <= acceptance_criteria:
    # reject the null hypothesis — conclude the alternate hypothesis
else:
    # retain the null hypothesis
```

- If `p_value` is **less than or equal to** `acceptance_criteria` (0.05), the
  observed difference is considered statistically significant, so we
  **reject the null hypothesis** and conclude the sample mean really differs
  from the population mean.
- Otherwise, we don't have enough evidence, so we **retain (fail to reject)
  the null hypothesis**.

---

## Real-world use cases in a company

A one-sample t-test is useful whenever you have **one group** and want to
compare its average against a **known or target value**:

1. **Quality control / manufacturing** — A factory's spec says light bulbs
   should last 1,000 hours on average. QC pulls a sample of 50 bulbs from
   today's batch and tests whether their average lifespan is significantly
   different from 1,000 hours, to decide if the production line needs
   recalibration.

2. **Call centre performance** — Company policy targets an average call
   handling time of 6 minutes. A sample of last week's calls is tested
   against that 6-minute benchmark to see if a new team is significantly
   slower or faster than the company standard.

3. **Finance / auditing** — An auditor expects the average transaction value
   in a ledger to match a reported figure. A sample of transactions is
   t-tested against the reported average to flag possible bookkeeping errors
   or fraud.

4. **HR / compensation analysis** — HR wants to check whether the average
   salary in a specific department differs significantly from the
   company-wide average salary (the "population mean"), to spot potential pay
   inequities.

5. **Marketing/website analytics** — A company knows their historical average
   "time on page" is 45 seconds. After a redesign, they sample a week of
   visits and test whether the new average time-on-page is significantly
   different from the historical 45-second baseline.

6. **Healthcare/pharma** — A drug is supposed to reduce blood pressure to a
   target level on average. Clinical trial samples are tested against that
   target value to check the drug's real-world effect size.

In each case, the pattern is identical to this script: define a known/target
mean (the population mean), collect a sample, run `ttest_1samp`, and use the
p-value against an acceptance criteria (commonly 0.05) to decide whether the
observed difference is real or just random noise.
