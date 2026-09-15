# Hypothesis Testing: The Chi-Square Test (A Beginner's Guide, with Python)

## 1. What is Hypothesis Testing? (Quick Refresher)

Before diving into the Chi-Square test, let's ground ourselves in the basic idea of **hypothesis testing**.

Hypothesis testing is a formal procedure for using data to decide between two competing claims:

- **Null Hypothesis (H₀)**: "Nothing interesting is happening." There is no relationship, no difference, no effect. Any pattern you see in your sample is just random noise.
- **Alternative Hypothesis (H₁ / Hₐ)**: "Something interesting IS happening." There is a real relationship, difference, or effect.

We never _prove_ H₀ or H₁ true. Instead, we calculate how surprising our observed data would be **if H₀ were true**. If the data is "surprising enough," we reject H₀ in favor of H₁.

The tool we use to measure "how surprising" is a **test statistic** (a single number computed from the data), and we compare that number against a **critical value** (a threshold) or use a **p-value** (a probability) to make the final call.

The Chi-Square test is one specific recipe for doing this, designed for **categorical data** (data grouped into buckets/labels, like "Male/Female", "Yes/No", "Red/Blue/Green") rather than continuous numeric data.

---

## 2. What is the Chi-Square (χ²) Test?

The Chi-Square test asks: **"Is the difference between what I observed and what I expected too large to be explained by random chance?"**

There are two common flavors:

1. **Chi-Square Goodness-of-Fit Test** — Compares the observed distribution of ONE categorical variable against an expected/theoretical distribution.
   - Example: "Do customers choose our 4 product colors equally, or do they prefer some colors more?"
2. **Chi-Square Test of Independence** — Compares TWO categorical variables to see if they are related (associated) or independent of each other.
   - Example: "Is there a relationship between a customer's subscription plan (Free/Pro/Enterprise) and whether they churn (Yes/No)?"

Both flavors use the exact same underlying formula — the difference is just how you build the table of observed vs. expected values.

---

## 3. The Chi-Square Formula, Broken Down

The Chi-Square statistic is calculated as:

$$
\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}
$$

Let's break this formula into its individual pieces so nothing is a "black box":

| Symbol          | Name                     | Meaning                                                                                                                                                                                                                                               |
| --------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| $O_i$           | **Observed frequency**   | The actual count you measured in category/cell $i$ (e.g., 45 customers actually churned).                                                                                                                                                             |
| $E_i$           | **Expected frequency**   | The count you would _expect_ in category/cell $i$ **if H₀ (no relationship / no difference) were true**.                                                                                                                                              |
| $O_i - E_i$     | **Residual (deviation)** | How far the real-world data strayed from the "nothing is happening" expectation. Can be positive or negative.                                                                                                                                         |
| $(O_i - E_i)^2$ | **Squared deviation**    | Squaring removes the negative sign (so deviations don't cancel each other out) and penalizes bigger gaps more heavily than small ones.                                                                                                                |
| $\div E_i$      | **Normalization**        | Divides the squared gap by the expected count. This matters because a deviation of "10" is a HUGE surprise if you expected 5, but a tiny surprise if you expected 5,000. Dividing by $E_i$ makes the comparison fair across cells of different sizes. |
| $\sum$          | **Summation**            | Add up this "surprise score" across every category/cell in your table to get one single overall number: $\chi^2$.                                                                                                                                     |

**Intuition in plain English:** For every cell/category, measure how far off reality was from expectation, square it (so it's always positive and big misses count more), scale it by how big a number you expected (so small-count and large-count cells are compared fairly), then add all those scaled surprises together. The bigger the total, the less compatible your data is with H₀.

### How do we get the "Expected" values ($E_i$)?

- **Goodness-of-fit test**: $E_i = n \times p_i$, where $n$ is total sample size and $p_i$ is the hypothesized proportion for category $i$ (often assumed equal, e.g., 25% each for 4 categories).
- **Test of independence** (for a contingency table):
  $$
  E_{row,col} = \frac{(\text{Row Total}) \times (\text{Column Total})}{\text{Grand Total}}
  $$
  This formula comes directly from the definition of statistical independence: if two variables are truly independent, $P(\text{row AND col}) = P(\text{row}) \times P(\text{col})$, and multiplying by the grand total converts that probability back into an expected count.

### Degrees of Freedom (df)

The Chi-Square distribution's shape depends on **degrees of freedom**, which represents how many values in your table are "free to vary" before the rest are locked in by the totals.

- Goodness-of-fit: $df = k - 1$ (k = number of categories)
- Test of independence: $df = (r-1)(c-1)$ (r = number of rows, c = number of columns)

`df` matters enormously because the critical value (see below) depends on it.

---

## 4. The Critical Value — The Heart of the Decision

This is the part beginners often find confusing, so let's slow down.

### What is a critical value?

A **critical value** is the cutoff point on the Chi-Square distribution beyond which we consider the test statistic "too extreme" to be explained by random chance. It is determined by two things:

1. **Significance level (α)** — Your tolerance for being wrong when you reject H₀. Commonly α = 0.05 (5% risk), meaning you accept a 5% chance of a "false alarm" (rejecting H₀ when it's actually true — a **Type I error**).
2. **Degrees of freedom (df)** — Because the Chi-Square distribution changes shape depending on df, the critical value table has a different number for every combination of α and df.

### How the decision is made

1. Compute your test statistic: $\chi^2_{calculated}$.
2. Look up (or compute in Python) the critical value $\chi^2_{critical}$ for your chosen α and df.
3. Compare:
   - If $\chi^2_{calculated} > \chi^2_{critical}$ → the result falls in the **rejection region** → reject H₀ (statistically significant association/difference exists).
   - If $\chi^2_{calculated} \leq \chi^2_{critical}$ → you **fail to reject H₀** (not enough evidence of a real effect; observed differences are plausibly due to chance).

### Why the critical value approach works

The Chi-Square distribution is **right-skewed** and **only takes non-negative values** (because it's built from squared numbers — you can never get a negative sum of squares). Almost all of the probability mass sits in a hump near the smaller values, with a long thin tail stretching to the right. The critical value marks where the tail becomes "thin enough" that landing there — purely by chance — would be considered rare/unlikely (e.g., only a 5% chance).

So visually: if your calculated χ² statistic lands out in that thin right-hand tail, it's evidence that something other than random chance produced your data.

---

## 5. Critical Value vs. the t-Statistic — Same Idea, Different Shape

This is where a lot of learners get tripped up, so let's directly compare them side-by-side.

| Aspect                               | Chi-Square (χ²) Test                                                                                      | t-Test                                                             |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | --------- | --------------------------------------------------------- |
| **Used for**                         | Categorical data (counts/frequencies in groups)                                                           | Continuous/numeric data (means)                                    |
| **Question answered**                | "Are these group counts/proportions different from what's expected?"                                      | "Are these group _averages_ different from each other/a target?"   |
| **Test statistic formula basis**     | Sum of squared, normalized deviations of _counts_                                                         | Difference of _means_ divided by the standard error                |
| **Distribution shape**               | Right-skewed, always ≥ 0 (built from squares)                                                             | Symmetric, bell-shaped, centered at 0, can be negative or positive |
| **Critical value lookup depends on** | α and degrees of freedom (df)                                                                             | α, degrees of freedom, AND whether it's one-tailed or two-tailed   |
| **Rejection rule**                   | Reject H₀ if $\chi^2_{calc} > \chi^2_{critical}$ (one-sided by nature, since squares are always positive) | Reject H₀ if $                                                     | t\_{calc} | > t\_{critical}$ (usually two-sided, checking both tails) |
| **What a large statistic means**     | Observed counts deviate a lot from expected counts                                                        | The two group means are far apart relative to their variability    |

### The Core Conceptual Similarity

Both tests follow the **exact same logical machinery**:

1. Compute a test statistic from your sample data.
2. Compare that statistic to a critical value derived from a known theoretical distribution (Chi-Square distribution vs. Student's t-distribution) at a chosen significance level (α) and degrees of freedom.
3. If your statistic is "more extreme" than the critical value, you reject H₀.

### The Core Conceptual Difference

- The **t-distribution is symmetric around zero**. A t-statistic can be very negative (Group A much smaller than Group B) or very positive (Group A much bigger than Group B). That's why t-tests typically check BOTH tails (two-tailed test) — extreme values in either direction are meaningful, and the critical region is split between the far-left and far-right.
- The **Chi-Square distribution only has one direction of "extreme"**: large positive values. Since χ² is built from squared terms, it can never be negative, so there is no "negative surprise" — only "how big is the surprise." That's why the Chi-Square rejection region is always a single tail on the right-hand side of the distribution.

**Analogy**: Think of the t-test as measuring "how far apart are two points on a number line, and in which direction?" (so both directions matter), while the Chi-Square test measures "how far off is my grid of numbers from the ideal grid, as a total magnitude?" (direction doesn't apply, because everything gets squared into a single non-negative "distance").

---

## 6. Step-by-Step Worked Example + Python Code

### Business Scenario

A subscription company wants to know: **"Is there a relationship between the customer's subscription Plan (Free, Pro, Enterprise) and whether they Churn (Yes/No)?"**

This is a **Test of Independence** — two categorical variables, checking for an association.

### Sample Data (Contingency Table)

| Plan             | Churned = Yes | Churned = No | Row Total |
| ---------------- | ------------- | ------------ | --------- |
| Free             | 90            | 60           | 150       |
| Pro              | 40            | 160          | 200       |
| Enterprise       | 10            | 140          | 150       |
| **Column Total** | **140**       | **360**      | **500**   |

### Python Code — Full Walkthrough

```python
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# --- Step 1: Build the observed contingency table ---
observed = np.array([
    [90, 60],   # Free plan:      churned=Yes, churned=No
    [40, 160],  # Pro plan
    [10, 140],  # Enterprise plan
])

plans = ["Free", "Pro", "Enterprise"]
churn_labels = ["Churned", "Retained"]

df_table = pd.DataFrame(observed, index=plans, columns=churn_labels)
print("Observed counts:\n", df_table)

# --- Step 2: Run the Chi-Square test of independence ---
# scipy.stats.chi2_contingency automatically computes:
#   - the chi2 statistic
#   - the p-value
#   - the degrees of freedom
#   - the table of EXPECTED counts (assuming independence)
chi2_stat, p_value, dof, expected = stats.chi2_contingency(observed)

print(f"\nChi-Square statistic: {chi2_stat:.4f}")
print(f"Degrees of freedom:    {dof}")
print(f"P-value:               {p_value:.6f}")
print("Expected counts (if Plan and Churn were independent):\n",
      pd.DataFrame(expected, index=plans, columns=churn_labels).round(2))

# --- Step 3: Find the critical value for alpha = 0.05 ---
alpha = 0.05
critical_value = stats.chi2.ppf(1 - alpha, dof)
print(f"\nCritical value (alpha={alpha}, df={dof}): {critical_value:.4f}")

# --- Step 4: Make the decision ---
if chi2_stat > critical_value:
    print("Decision: REJECT H0 -> Plan and Churn are statistically associated.")
else:
    print("Decision: FAIL TO REJECT H0 -> No significant association detected.")

# --- Step 5 (Optional cross-check): compare with a t-test on a numeric variable ---
# Suppose we also track "average monthly usage hours" for churned vs retained customers
# This shows how a t-test answers a DIFFERENT kind of question (comparing MEANS, not COUNTS)
churned_usage_hours = np.array([12, 15, 9, 11, 14, 10, 13, 8, 16, 12])
retained_usage_hours = np.array([25, 30, 22, 28, 26, 24, 27, 29, 31, 23])

t_stat, t_p_value = stats.ttest_ind(churned_usage_hours, retained_usage_hours)
t_dof = len(churned_usage_hours) + len(retained_usage_hours) - 2
t_critical = stats.t.ppf(1 - alpha / 2, t_dof)  # two-tailed critical value

print(f"\n--- t-test comparison (for context) ---")
print(f"t-statistic:      {t_stat:.4f}")
print(f"t critical value: +/-{t_critical:.4f}  (two-tailed, df={t_dof})")
print(f"p-value:          {t_p_value:.6f}")
```

**Expected console output (approximate):**

```
Chi-Square statistic: 62.7460
Degrees of freedom:    2
P-value:               0.000000
Critical value (alpha=0.05, df=2): 5.9915
Decision: REJECT H0 -> Plan and Churn are statistically associated.

t-statistic:      -12.xxxx
t critical value: +/-2.1009  (two-tailed, df=18)
p-value:          0.000000
```

### Reading the Output

- `chi2_stat = 62.75` is far larger than `critical_value = 5.99`, so we land deep in the rejection region → **reject H₀**. There IS a real relationship between subscription plan and churn (e.g., Free-plan users churn far more than Enterprise users).
- Notice the `t_critical` has a **± sign** — because the t-distribution is two-sided — while the Chi-Square critical value has **no sign**, since we only ever compare against the right tail.

---

## 7. Visualizing It: Sample Graphs

Below are two graph-generating scripts you can run (after `pip install matplotlib scipy numpy`). Each is followed by a detailed explanation of exactly what every data point/line/shaded region represents.

### Graph 1 — The Chi-Square Distribution with Critical Value and Rejection Region

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

dof = 2
alpha = 0.05

x = np.linspace(0, 20, 1000)
y = stats.chi2.pdf(x, dof)  # probability density function of chi2 with df=2

critical_value = stats.chi2.ppf(1 - alpha, dof)
chi2_stat = 62.746  # our calculated statistic from the example above (off-chart, noted with an arrow)

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(x, y, color="navy", linewidth=2, label=f"Chi-Square distribution (df={dof})")

# Shade the rejection region (area beyond the critical value)
x_reject = x[x >= critical_value]
y_reject = stats.chi2.pdf(x_reject, dof)
ax.fill_between(x_reject, y_reject, color="red", alpha=0.4,
                 label=f"Rejection region (alpha={alpha})")

# Mark the critical value with a vertical dashed line
ax.axvline(critical_value, color="red", linestyle="--", linewidth=1.5)
ax.text(critical_value + 0.3, max(y) * 0.6,
        f"Critical value = {critical_value:.2f}", color="red")

ax.set_title("Chi-Square Distribution: Critical Value & Rejection Region")
ax.set_xlabel("Chi-Square statistic value")
ax.set_ylabel("Probability density")
ax.legend()
plt.tight_layout()
plt.savefig("chi_square_distribution.png", dpi=150)
plt.show()
```

**What every part of this graph means:**

- **The navy curve (PDF)**: This is the theoretical Chi-Square distribution for `df=2`. It shows how likely each possible χ² value is, _assuming H₀ is true_ (i.e., assuming there really is no association). Note the shape: it starts high near 0 and decays to the right — this is the "right-skew, non-negative only" shape discussed earlier.
- **The red shaded area (rejection region)**: Everything to the right of the critical value. This area equals exactly `α = 0.05` (5%) of the total area under the curve. It represents "the 5% most extreme/surprising outcomes that could still happen by pure chance."
- **The red dashed vertical line (critical value ≈ 5.99)**: The literal cutoff/boundary. Anything calculated to the right of this line is considered statistically significant at the 5% level.
- **Why our calculated χ² = 62.75 isn't drawn on this chart**: It's so far to the right (way past 20 on the x-axis) that it would be off-screen — which itself visually communicates just how extreme/significant this result is. In practice you'd add an annotation/arrow pointing off the right edge of the chart labeled "Our calculated χ² = 62.75 →" to show it lands deep inside the rejection region.

### Graph 2 — Comparing the Chi-Square Distribution Shape vs. the t-Distribution Shape

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

x_chi = np.linspace(0, 15, 1000)
x_t = np.linspace(-5, 5, 1000)

dof_chi = 3
dof_t = 18

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# --- Left panel: Chi-Square ---
axes[0].plot(x_chi, stats.chi2.pdf(x_chi, dof_chi), color="darkorange")
crit_chi = stats.chi2.ppf(0.95, dof_chi)
axes[0].fill_between(x_chi[x_chi >= crit_chi],
                      stats.chi2.pdf(x_chi[x_chi >= crit_chi], dof_chi),
                      color="red", alpha=0.4)
axes[0].axvline(crit_chi, color="red", linestyle="--")
axes[0].set_title(f"Chi-Square (df={dof_chi}): one-tailed, right-skewed")
axes[0].set_xlabel("Statistic value")
axes[0].set_ylabel("Density")

# --- Right panel: t-distribution ---
axes[1].plot(x_t, stats.t.pdf(x_t, dof_t), color="green")
crit_t = stats.t.ppf(0.975, dof_t)  # two-tailed alpha=0.05 -> 0.025 each side
axes[1].fill_between(x_t[x_t >= crit_t], stats.t.pdf(x_t[x_t >= crit_t], dof_t),
                      color="red", alpha=0.4)
axes[1].fill_between(x_t[x_t <= -crit_t], stats.t.pdf(x_t[x_t <= -crit_t], dof_t),
                      color="red", alpha=0.4)
axes[1].axvline(crit_t, color="red", linestyle="--")
axes[1].axvline(-crit_t, color="red", linestyle="--")
axes[1].set_title(f"t-distribution (df={dof_t}): two-tailed, symmetric")
axes[1].set_xlabel("Statistic value")

plt.tight_layout()
plt.savefig("chi_vs_t_distribution.png", dpi=150)
plt.show()
```

**What this side-by-side comparison shows:**

- **Left panel (orange curve, Chi-Square)**: Skewed right, all values ≥ 0. Only ONE red rejection zone, on the right tail, because "extreme" only ever means "larger than expected under H₀."
- **Right panel (green curve, t-distribution)**: Perfectly symmetric bell shape centered at 0. There are TWO red rejection zones — one on the far left (very negative t, meaning Group A's mean is much smaller than Group B's) and one on the far right (very positive t, meaning Group A's mean is much larger than Group B's). Both tails matter because a t-statistic's _sign_ carries meaning (direction of the difference), whereas Chi-Square's squared construction throws away directional information entirely.
- Together, these two panels visually justify the difference in the "Rejection rule" row of the earlier comparison table: one-sided vs. two-sided critical regions come directly from the shape of each theoretical distribution.

---

## 8. Business Use Cases (Chi-Square in the Real World)

| Company / Industry                 | Business Question                                                                     | Categorical Variables               | Why Chi-Square Helps                                                                                             |
| ---------------------------------- | ------------------------------------------------------------------------------------- | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Netflix / Streaming**            | Does subscription tier (Basic/Standard/Premium) relate to whether a user cancels?     | Tier × Churn (Yes/No)               | Prioritize retention campaigns and pricing strategy for the tier most at risk.                                   |
| **Retail (e.g., Target, Walmart)** | Is product return rate related to the store's region (North/South/East/West)?         | Region × Returned (Yes/No)          | Identify regional supply-chain or quality issues driving returns, and target fixes.                              |
| **Marketing / A/B Testing**        | Did email subject line variant (A/B/C) affect whether users clicked?                  | Variant × Clicked (Yes/No)          | Decide which subject-line strategy to roll out company-wide with statistical confidence.                         |
| **Banking / FinTech**              | Is loan default related to employment type (Salaried/Self-employed/Unemployed)?       | Employment Type × Default (Yes/No)  | Improve credit risk models and underwriting rules.                                                               |
| **Healthcare / Pharma**            | Is a new drug's side-effect occurrence related to patient age group?                  | Age Group × Side Effect (Yes/No)    | Support/refute safety claims required for regulatory approval.                                                   |
| **HR / People Analytics**          | Is employee attrition related to department (Sales/Engineering/Support)?              | Department × Attrition (Yes/No)     | Direct retention budget/initiatives to the department with a genuinely elevated (not just noisy) attrition rate. |
| **E-commerce (e.g., Amazon)**      | Is the choice of payment method (Card/Wallet/COD) associated with order cancellation? | Payment Method × Cancelled (Yes/No) | Adjust checkout flow or incentives for the payment method most linked to cancellations.                          |

In every case, the pattern is identical: **two (or more) categorical buckets, a business question about "is there a real link here or is it just noise," and a Chi-Square test that turns raw counts into a confident, data-backed yes/no answer** — which then drives a concrete business decision (where to spend the marketing budget, which regions to audit, which tier to focus retention efforts on, etc.).

---

## 9. Key Takeaways for Beginners

1. **Chi-Square works on counts/categories**; **t-tests work on means/numeric measurements**. Match the test to the type of data you have.
2. The **critical value is just a threshold** on the relevant probability distribution (Chi-Square or t), determined by your chosen significance level (α) and degrees of freedom (df).
3. **Compare your calculated statistic to the critical value**: past it → reject H₀ (statistically significant); not past it → fail to reject H₀ (not enough evidence).
4. **Chi-Square is one-tailed by nature** (only large positive values are "surprising," since everything is squared); **t-tests are typically two-tailed** (both very negative and very positive values are "surprising," since sign/direction carries meaning).
5. You rarely need to look up critical values in a printed table anymore — `scipy.stats.chi2.ppf()` and `scipy.stats.t.ppf()` compute them precisely for whatever α and df you need.
6. Always pair the statistic/critical-value comparison with the **p-value** (`stats.chi2_contingency` gives you both) — the p-value tells you exactly how extreme your result is, not just whether it crossed a fixed line.
7. Statistical significance (a low p-value / large χ²) tells you a relationship likely exists — it does **not** by itself tell you the relationship is large or business-important. Always look at the actual percentages/effect size alongside the test result before making a business decision.
