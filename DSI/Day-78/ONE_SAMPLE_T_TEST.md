I'll simplify the write-up, add runnable code for each company use case, and include `savefig` lines — then save your plot-saving preference to memory.

# One-Sample T-Test — Super Simple Beginner's Guide

---

## 1. What is this thing in one sentence?

You have a big pile of numbers (the **population**). You can only afford to look at a small handful of them (the **sample**). The one-sample t-test asks:

> "Is my small handful's average close to the big pile's average, or is it really different?"

**Everyday analogy:** You taste one spoon of soup. Is it the same soup as the whole pot, or did someone add too much salt? The spoon is your sample, the pot is your population.

---

## 2. The whole story in 5 steps

| Step | What you do                                  | Why                                      |
| ---- | -------------------------------------------- | ---------------------------------------- |
| 1    | Make/find your **population** (all the data) | This is your "truth"                     |
| 2    | Pull a small **sample** from it              | Real life = you can't measure everything |
| 3    | Compare the two averages                     | A quick eyeball check                    |
| 4    | Run `ttest_1samp`                            | Does the maths properly                  |
| 5    | Look at the **p-value**                      | Decides your answer                      |

---

## 3. The imports — plain English

```python
import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, ttest_1samp
```

| Name                | Plain-English meaning                                                                                                                     |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `os`                | Lets us create folders (so we can save the plot to disk).                                                                                 |
| `matplotlib.pyplot` | The drawing tool — makes charts.                                                                                                          |
| `numpy`             | The maths toolbox — arrays of numbers + random number generation.                                                                         |
| `norm`              | A "recipe" for a bell curve (the classic hill shape), described by a mean and a spread.                                                   |
| `ttest_1samp`       | The actual one-sample t-test function.                                                                                                    |
| `cast`              | Ignore this if it confuses you — it only tells VS Code's type checker "trust me, this is a float". It changes nothing when the code runs. |

---

## 4. Step 1 — Make a pretend population

```python
population = norm.rvs(loc=500, scale=100, size=1000, random_state=42).astype(int)
```

Think of `norm.rvs(...)` as a **number-generating machine**:

- `loc=500` → the **centre** (mean). Most numbers land near 500.
- `scale=100` → the **width** (standard deviation). Bigger = more spread out.
- `size=1000` → how many numbers to make. Pretend "everyone" = 1000 things.
- `random_state=42` → the **seed**. Computers fake randomness with a formula. Fixing the seed means everyone gets the _exact same_ "random" numbers → reproducible.
- `.astype(int)` → turn `503.827` into `503`, because our pretend measurements are whole numbers (money, counts, hours).

## 5. Step 2 — Take a small sample

```python
sample = np.random.choice(population, 250, replace=False)
```

- `np.random.choice(...)` → randomly grab **250** values out of the 1000.
- `replace=False` → don't pick the same item twice.
- This is you doing the real-life thing: measuring a few things, not everything.

## 6. Step 3 — Draw the picture (and save it to a file!)

```python
os.makedirs("plots", exist_ok=True)          # make the folder if it isn't there

plt.figure(figsize=(8, 5))
plt.hist(population, bins=30, density=True, alpha=0.5, label="population (1000)")
plt.hist(sample,     bins=30, density=True, alpha=0.5, label="sample (250)")
plt.xlabel("value")
plt.ylabel("density")
plt.title("Population vs Sample")
plt.legend()

plt.savefig("plots/one_sample_t_test.png", dpi=300, bbox_inches="tight")  # ← writes the file
plt.show()                                                                 # ← shows the window
plt.close()                                                                # ← frees memory
```

| Piece                      | Meaning                                                                                                    |
| -------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `plt.hist(...)`            | Draws a histogram: groups numbers into bins, draws a bar per bin.                                          |
| `density=True`             | Bars are scaled so total area = 1. Needed to compare a group of 1000 with a group of 250 fairly.           |
| `alpha=0.5`                | Transparency, so overlapping bars are both visible.                                                        |
| `plt.savefig("plots/...")` | **Saves the chart as an image file.** Must come _before_ `plt.show()`, because `show()` clears the figure. |
| `dpi=300`                  | High resolution (print quality).                                                                           |
| `bbox_inches="tight"`      | Crops the empty white border.                                                                              |
| `plt.close()`              | After showing, close it so your loop/examples don't overlap figures.                                       |

## 7. Step 4 — Compare the averages

```python
population_mean = population.mean()
sample_mean = sample.mean()
print(population_mean, sample_mean)
```

`.mean()` is just the arithmetic average of an array. Doing this first lets you _eyeball_ how big the gap is before doing any formal statistics.

## 8. Step 5 — Write down the two hypotheses

```python
null_hypothesis = "The sample mean IS the same as the population mean"
alternate_hypothesis = "The sample mean is DIFFERENT from the population mean"
acceptance_criteria = 0.05
```

- **Null (H0)** = the boring default: no real difference; any gap is just luck.
- **Alternate (H1)** = what we're testing for: there really _is_ a difference.
- **`acceptance_criteria = 0.05`** = **alpha (α)** = "I accept a 5% risk of being wrong when I say there's a difference." 0.05 is the standard in business.

## 9. Step 6 — Run the test

```python
t_statistic, p_value = ttest_1samp(sample, population_mean)
print(f"t = {t_statistic:.3f}, p = {p_value:.4f}")
```

The function gives you two numbers:

- **`t_statistic`** → how many "standard errors" away the sample mean is from the target mean. Bigger (in either direction) = bigger gap.
- **`p_value`** → "if there were really no difference, how likely was a gap this large just by luck?" **Small p = suspicious = the difference is probably real.**

## 10. Step 7 — Make the decision

```python
if p_value <= acceptance_criteria:
    print("REJECT the null hypothesis → the means ARE different")
else:
    print("RETAIN the null hypothesis → no proven difference")
```

- `p ≤ 0.05` → statistically significant → reject H0.
- `p > 0.05` → not enough evidence → keep H0.

---

## 11. Two helper functions (so every use case below is only 3 lines)

```python
def one_sample_t_test(sample, target_mean, alpha=0.05, label="Test"):
    """Run a one-sample t-test and print a beginner-friendly verdict."""
    t_stat, p_value = ttest_1samp(sample, target_mean)
    print(f"\n=== {label} ===")
    print(f"sample mean = {np.mean(sample):.2f} | target = {target_mean}")
    print(f"t = {t_stat:.3f} | p = {p_value:.4f}")
    if p_value <= alpha:
        print("Result: REJECT H0 → the average IS significantly different.")
    else:
        print("Result: RETAIN H0 → no significant difference found.")
    return t_stat, p_value


def plot_sample(sample, target_mean, filename, title):
    """Draw the sample histogram, mark the target, and save it to plots/."""
    os.makedirs("plots", exist_ok=True)
    plt.figure(figsize=(7, 4))
    plt.hist(sample, bins=20, alpha=0.6, color="steelblue", edgecolor="black")
    plt.axvline(np.mean(sample), color="red",   linestyle="--", linewidth=2,
                label=f"sample mean = {np.mean(sample):.1f}")
    plt.axvline(target_mean, color="green", linestyle="-", linewidth=2,
                label=f"target = {target_mean}")
    plt.title(title)
    plt.xlabel("value")
    plt.ylabel("count")
    plt.legend()
    plt.savefig(f"plots/{filename}", dpi=300, bbox_inches="tight")   # saves the plot
    plt.close()
```

---

## 12. Real-world company use cases — with code

### Case 1 — Quality control: light bulbs

Spec = 1000 hours. QC weighs 50 bulbs from today's batch.

```python
np.random.seed(1)
bulbs = np.random.normal(985, 60, 50)                # today's batch
one_sample_t_test(bulbs, target_mean=1000, label="Bulb lifespan (hours)")
plot_sample(bulbs, 1000, "bulbs.png", "Light bulb lifespan vs 1000h spec")
```

### Case 2 — Call centre: average handling time

Company target = 6 minutes per call. Test last week's sample.

```python
np.random.seed(2)
calls = np.random.normal(6.6, 1.5, 120)              # 120 calls from last week
one_sample_t_test(calls, target_mean=6, label="Call handling time (min)")
plot_sample(calls, 6, "calls.png", "Call handling time vs 6-min target")
```

### Case 3 — Finance / auditing: transaction values

Reported ledger average = 250. Audit a sample of 80 transactions.

```python
np.random.seed(3)
transactions = np.random.normal(268, 70, 80)         # sampled ledger entries
one_sample_t_test(transactions, target_mean=250, label="Transaction value ($)")
plot_sample(transactions, 250, "transactions.png", "Transactions vs reported $250")
```

### Case 4 — HR: department salary vs company average

Company-wide average salary = 55,000. Check one department.

```python
np.random.seed(4)
dept_salaries = np.random.normal(52800, 9000, 40)    # 40 people in the dept
one_sample_t_test(dept_salaries, target_mean=55000, label="Department salary ($)")
plot_sample(dept_salaries, 55000, "salaries.png", "Dept salary vs company average")
```

### Case 5 — Marketing: time on page after a redesign

Historical baseline = 45 seconds.

```python
np.random.seed(5)
visits = np.random.normal(48, 12, 200)               # one week of visits
one_sample_t_test(visits, target_mean=45, label="Time on page (seconds)")
plot_sample(visits, 45, "time_on_page.png", "Time on page vs 45s baseline")
```

### Case 6 — Healthcare: drug reduces blood pressure

Target = 120 mmHg. Trial sample of 60 patients.

```python
np.random.seed(6)
patients = np.random.normal(123, 10, 60)
one_sample_t_test(patients, target_mean=120, label="Blood pressure (mmHg)")
plot_sample(patients, 120, "blood_pressure.png", "Trial BP vs 120 mmHg target")
```

**The pattern is always the same:**
`known target mean → sample → ttest_1samp → compare p-value to 0.05 → decision + save chart.`

---

## 13. Full copy-paste script

```python
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, ttest_1samp


def one_sample_t_test(sample, target_mean, alpha=0.05, label="Test"):
    t_stat, p_value = ttest_1samp(sample, target_mean)
    print(f"\n=== {label} ===")
    print(f"sample mean = {np.mean(sample):.2f} | target = {target_mean}")
    print(f"t = {t_stat:.3f} | p = {p_value:.4f}")
    if p_value <= alpha:
        print("Result: REJECT H0 → the average IS significantly different.")
    else:
        print("Result: RETAIN H0 → no significant difference found.")
    return t_stat, p_value


def plot_sample(sample, target_mean, filename, title):
    os.makedirs("plots", exist_ok=True)
    plt.figure(figsize=(7, 4))
    plt.hist(sample, bins=20, alpha=0.6, color="steelblue", edgecolor="black")
    plt.axvline(np.mean(sample), color="red", linestyle="--", linewidth=2,
                label=f"sample mean = {np.mean(sample):.1f}")
    plt.axvline(target_mean, color="green", linestyle="-", linewidth=2,
                label=f"target = {target_mean}")
    plt.title(title)
    plt.xlabel("value")
    plt.ylabel("count")
    plt.legend()
    plt.savefig(f"plots/{filename}", dpi=300, bbox_inches="tight")
    plt.close()


# --- the original example -------------------------------------------------
population = norm.rvs(loc=500, scale=100, size=1000, random_state=42).astype(int)
sample = np.random.choice(population, 250, replace=False)

population_mean = population.mean()
one_sample_t_test(sample, target_mean=population_mean, label="Sample vs population")

plot_sample(sample, population_mean, "sample_vs_population.png", "Sample vs population mean")
```

**Reminder:** `plt.savefig(...)` must always sit _before_ `plt.show()`, otherwise you'll save an empty image.
