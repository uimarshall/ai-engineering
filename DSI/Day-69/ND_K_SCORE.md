# The Normal Distribution & Z-Scores — A Beginner's Guide with Python

> **How to use this file:** run the Python code blocks in order (in Jupyter, VS Code, or as a script).
> Each figure is saved as a PNG in the same folder, and the image is linked below the code, so opening
> this file in any markdown viewer shows the graphs after you have run the code once.

---

## 1. What is the Normal Distribution?

The **normal distribution** (also called the _Gaussian_ or _bell curve_) is a continuous probability
distribution that describes data clustered symmetrically around a central value, with values becoming
rarer the further they are from the center.

A normal distribution is fully described by **two parameters**:

| Parameter          | Symbol    | What it controls                       | Example |
| ------------------ | --------- | -------------------------------------- | ------- |
| Mean               | μ (mu)    | The **center / location** of the curve | μ = 100 |
| Standard deviation | σ (sigma) | The **spread** of the curve            | σ = 15  |

Notation: `X ~ N(μ, σ²)` — read as _"X is normally distributed with mean μ and variance σ²"_.

Where does normality show up in business data?

- Measurement errors (factory machine tolerances)
- Sums / averages of many small independent effects (delivery times, call durations, test scores)
- Financial daily returns (as an approximation)
- Any metric where many independent factors add up — this is the **Central Limit Theorem** in action, which you'll see again in the confidence-interval tutorial.

---

## 2. Key properties (memorize these)

1. **Symmetric** around μ — the left half is a mirror image of the right half.
2. **Mean = median = mode** — the peak is also the average and the middle value.
3. **Total area under the curve = 1** — because the curve represents _all possible outcomes_ (100% of probability).
4. **The 68-95-99.7 rule:**
   - ≈ 68% of values lie within **±1σ** of the mean
   - ≈ 95% of values lie within **±2σ** of the mean
   - ≈ 99.7% of values lie within **±3σ** of the mean
5. **Tails never touch zero** — extreme values are rare, but never _impossible_.
6. **Probability of an exact value = 0** — for continuous data, probability only exists over _ranges_ (areas under the curve).

---

## 3. The Probability Density Function (PDF) — formula broken down

The shape of the bell curve is given by the **probability density function**:

```
                 1              (x − μ)²
f(x)  =   ───────────── · exp( − ─────── )
           σ · √(2π)              2σ²
```

### Piece-by-piece explanation

| Part                 | Meaning                                                                                                                                                                                                                      |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `x`                  | A specific value of the variable (e.g., "a delivery took 130 minutes")                                                                                                                                                       |
| `(x − μ)`            | How far `x` is from the mean — the **signed distance**                                                                                                                                                                       |
| `(x − μ)²`           | Squared distance, so a value 10 above or 10 below the mean contributes equally                                                                                                                                               |
| `− (x − μ)² / (2σ²)` | The further `x` is from μ, the more negative this exponent gets                                                                                                                                                              |
| `e^...`              | The exponential turns that negative number into a fraction between 0 and 1 → the curve **decays** as you move away from μ                                                                                                    |
| `2σ²`                | Divides by the _spread²_: a big σ means you must travel farther from μ before the curve meaningfully drops → wider, flatter bell                                                                                             |
| `1 / (σ·√(2π))`      | A **normalizing constant**: `√(2π)` comes from the famous Gaussian integral `∫ e^(−x²/2) dx = √(2π)`. This constant guarantees the _total area under the curve equals exactly 1_, making it a valid probability distribution |
| `f(x)`               | The **density** (height of the curve) at value x — **not** a probability                                                                                                                                                     |

**Why does bigger σ make the curve lower?** Look at the constant `1/σ`: if σ doubles, the peak height halves — the same 100% of probability must be spread over a wider range, so the curve gets flatter.

**Standard normal distribution:** if we set μ = 0 and σ = 1 we get `Z ~ N(0,1)`, with density
`φ(z) = (1/√(2π)) · e^(−z²/2)`. This special version is what z-scores map onto.

---

## 4. The Z-Score — formula broken down

A **z-score** answers: _"How many standard deviations is a value x away from the mean?"_

```
        x − μ
z  =   ───────
          σ
```

### Anatomy of the formula

- `x − μ` (numerator): the value's **distance from the mean**, with sign.
- `σ` (denominator): converts that distance into **standard-deviation units** (removes the original units — minutes, dollars, IQ points...).
- Result: **z is unit-free**. z = 0 means x equals the mean; z = +2 means x is 2 standard deviations **above** the mean; z = −1.5 means 1.5 standard deviations **below**.

**Why is this useful?**

1. **Comparability** — we can compare a 130-minute delivery to an $85 transaction because both are now in the same "standard deviation units".
2. **Probability** — if the data is (approximately) normal, a z-score maps to a probability via the standard normal curve: z = 2 → 97.72% of values are below it.

_Example:_ IQ scores have μ = 100, σ = 15. A score of 118 gives
z = (118 − 100)/15 = **1.2**, i.e., 1.2 standard deviations above average.

---

## 5. Python: simulate data and visualize the bell curve

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# --- Simulate 10,000 values from a normal distribution -------------------
mu, sigma = 100, 15
rng = np.random.default_rng(42)          # fixed seed -> reproducible results
data = rng.normal(loc=mu, scale=sigma, size=10_000)

# --- Figure 1: histogram of sample + theoretical PDF ----------------------
fig, ax = plt.subplots(figsize=(10, 6))

# Histogram: density=True makes the total area = 1, like a probability curve
ax.hist(data, bins=60, density=True, alpha=0.55, color="#4C72B0",
        edgecolor="white", label="Histogram of 10,000 simulated values")

# Theoretical PDF over a smooth grid of x values (from mu-4sigma to mu+4sigma)
x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 500)
pdf = stats.norm.pdf(x, mu, sigma)
ax.plot(x, pdf, color="#C44E52", lw=2.5, label="Theoretical normal PDF")

# Shade the middle 68% band (mu ± 1 sigma)
ax.axvspan(mu - sigma, mu + sigma, color="gray", alpha=0.2, label="μ ± 1σ (≈68% of data)")

# Dashed reference lines at mu ± 1σ, ± 2σ, ± 3σ, and a solid line at mu
for k in (1, 2, 3):
    ax.axvline(mu + k * sigma, color="gray", ls="--", lw=0.9)
    ax.axvline(mu - k * sigma, color="gray", ls="--", lw=0.9)
ax.axvline(mu, color="black", lw=1.2)

ax.set_xlabel("Value of X (e.g. IQ score or delivery time in minutes)")
ax.set_ylabel("Density (proportion of data per unit of X)")
ax.set_title(f"Normal Distribution: μ = {mu}, σ = {sigma}")
ax.legend()
plt.savefig("normal_distribution_histogram.png", dpi=150, bbox_inches="tight")
plt.show()

# --- Empirical check of the 68-95-99.7 rule on our simulated sample -------
for k in (1, 2, 3):
    share = np.mean((data >= mu - k * sigma) & (data <= mu + k * sigma))
    print(f"{share*100:.2f}% of the 10,000 values lie within ±{k}σ")
```

![Histogram of a normal distribution with overlay PDF](normal_distribution_histogram.png)

**What the code does, line by line:**

- `rng.normal(loc, scale, size)` draws 10,000 random numbers from N(100, 15). The seed (`42`) makes the output reproducible — anyone running this gets the same "random" data.
- `ax.hist(..., density=True)` builds the blue bars. `density=True` rescales the bars so their **total area is 1**, which lets us overlay the theoretical curve on the same scale. Each bar's height × width = the fraction of data points in that bin.
- `np.linspace(μ − 4σ, μ + 4σ, 500)` creates 500 evenly spaced x-values covering essentially the whole distribution (99.99% of a normal lies within ±4σ).
- `stats.norm.pdf(x, mu, sigma)` evaluates the PDF formula from Section 3 at those 500 points — the red curve.
- `ax.axvspan(μ − σ, μ + σ)` shades the region between one standard deviation below and above the mean.
- The final loop counts what fraction of the 10,000 points actually fall inside each ±kσ band and prints it — you should see roughly **68.3%, 95.4%, 99.7%**, matching the rule.

**What the graph shows you:**

- The **blue bars** are the empirical data: each bar is the proportion of simulated observations falling in that small value range.
- The **red curve** is the mathematical ideal. With 10,000 samples the bars hug the curve almost perfectly — if you used only 30 samples, the bars would look jagged and lumpy. That visual gap between "sample" and "theory" is _sampling error_.
- The **black line** at 100 marks the mean = the peak. The **dashed lines** mark μ ± 1, 2, 3σ; note how quickly the curve approaches zero beyond ±3σ.
- The **gray shaded band** covers 68% of the data — the classic "most things are within one standard deviation" intuition.

---

## 6. Python: z-scores, probabilities (CDF), and percentiles (PPF)

Business example: an e-commerce warehouse measures delivery times as `X ~ N(100, 15)` minutes.
Management promised: _"your order arrives within 130 minutes."_ What percentage of orders actually
meet that promise?

```python
# --- 1) Manual z-score calculation ---------------------------------------
mu, sigma, x_target = 100, 15, 130
z = (x_target - mu) / sigma
print(f"z = ({x_target} − {mu}) / {sigma} = {z:.2f}")      # z = 2.00

# --- 2) Probability via the CDF ------------------------------------------
# P(X <= 130) using the original distribution, and via the standard normal
p_below = stats.norm.cdf(x_target, mu, sigma)
p_below_z = stats.norm.cdf(z)               # same thing, Z ~ N(0,1)
print(f"P(X ≤ 130) = {p_below:.4f}  (via z-table style: P(Z ≤ 2.00) = {p_below_z:.4f})")
print(f"P(X > 130) = {1 - p_below:.4f}  -> {100*(1-p_below):.2f}% of orders miss the SLA")

# --- 3) Graph: standard normal with the shaded area for z = 2 -------------
z_grid = np.linspace(-4, 4, 800)
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(z_grid, stats.norm.pdf(z_grid), color="black", lw=2, label="Standard normal N(0,1)")
ax.fill_between(z_grid, stats.norm.pdf(z_grid), where=(z_grid <= z),
                color="#4C72B0", alpha=0.7, label=f"Area = P(Z ≤ {z:.2f}) = 0.9772")
ax.axvline(z, color="#C44E52", lw=2, ls="--")
ax.set_xlabel("z (standard deviations from the mean)")
ax.set_ylabel("Density φ(z)")
ax.set_title("The z-score z = 2.00 and the probability it represents")
ax.legend()
plt.savefig("standard_normal_cdf.png", dpi=150, bbox_inches="tight")
plt.show()

# --- 4) Inverse direction: percentiles with PPF ---------------------------
print(f"95th percentile of delivery times: {stats.norm.ppf(0.95, mu, sigma):.1f} min")
print(f"Middle 95% band: {stats.norm.ppf(0.025, mu, sigma):.1f} to "
      f"{stats.norm.ppf(0.975, mu, sigma):.1f} min")
```

![Standard normal curve with area left of z=2 shaded](standard_normal_cdf.png)

**What the code does, line by line:**

- The z-score calculation converts the _raw_ value 130 into standard-deviation units: (130 − 100)/15 = **2.00**.
- `stats.norm.cdf(130, 100, 15)` computes the **CDF** (cumulative distribution function) = the area under the bell curve from −∞ up to 130. The CDF is what old printed "z-tables" contained; `stats.norm.cdf(z)` on the standard normal is the modern equivalent. Both return **0.9772**.
- `fill_between(..., where=(z_grid <= z))` shades everything to the left of z = 2 under the standard normal curve.
- `stats.norm.ppf(probability)` is the **inverse** of the CDF: give it a probability, get the x-value back. It answers _"which delivery time is so fast that 95% of orders beat it?"_

**What the graph shows you:**

- The **curve** is the standard normal N(0,1) — μ = 0 on the horizontal axis is the peak.
- The **shaded blue area** is exactly 97.72% of the total area under the curve → 97.72% of deliveries arrive within 130 minutes.
- The **red dashed line** at z = 2 marks our order. The tiny unshaded right tail (2.28%) is the share of orders that would be late — about 228 out of every 10,000.
- Reading backwards: the 95th percentile comes back at μ + 1.645σ ≈ **124.7 minutes**, and the middle 95% of deliveries fall between roughly **70.6 and 129.4 minutes** — that "±1.96σ" idea will reappear in the confidence-interval tutorial.

---

## 7. Company use cases (how businesses actually use this)

### 🛒 E-commerce & logistics — SLA compliance (Amazon-style)

- **Problem:** management promises 2-hour delivery; how many orders will miss it?
- **Approach:** model delivery time as approximately normal, compute the z-score of the SLA limit, read the tail probability.
- **Decision:** if 2.3% of orders exceed the SLA, the ops team can simulate "what if we cut mean time by 5 minutes" (shift μ) and see the late rate drop — before spending money on extra couriers.

### 🏦 Banking & fintech — anomaly/fraud detection (Chase, PayPal-style)

- **Problem:** spot unusual transactions among millions of daily payments.
- **Approach:** model a customer's _typical_ transaction amount per category (normal-ish for routine spending) and compute each transaction's z-score. A z-score > 3 means the amount is more than 3σ above their normal behavior (a once-in-~370-event).
- **Decision:** auto-flag those transactions for review or step-up verification — dramatically shrinking the pool humans must inspect, with fewer false positives than a naive "above $500" rule. (In practice this is combined with ML models.)

### 🏭 Manufacturing — quality control (Toyota, Motorola "Six Sigma")

- **Problem:** a machine fills 500 ml bottles; if fill volume drifts, you under-fill (fines, complaints) or over-fill (lost margin).
- **Approach:** sample bottles every hour, compute the z-score of the sample mean vs. target. Control charts flag an alarm when z crosses ±3σ (action limit). A process running at "6σ" quality produces only ~3.4 defects per million opportunities.
- **Decision:** stop the line and re-calibrate _immediately_ when flagged, instead of shipping thousands of bad units.

### 👥 HR & people analytics — pay-equity screening

- **Problem:** is a given employee's salary fair within their job family?
- **Approach:** compute the z-score of each salary relative to the job family's mean and standard deviation.
- **Decision:** salaries with |z| > 2 are investigated — either justified outliers (tenure, location, performance) or potential pay-equity issues, giving HR a defensible, data-driven shortlist.

### 📈 Finance — risk measurement (Value at Risk)

- **Problem:** how much could a portfolio lose on a bad day?
- **Approach:** if daily returns are roughly normal with mean μ and std σ, the 5% worst-case return is roughly `μ − 1.645σ` (z = −1.645 cuts off the worst 5% tail). That number _is_ a 95% one-day VaR.
- **Decision:** banks hold capital against this number; regulators (Basel rules) require it. **Caveat:** real returns have fatter tails than a normal — which is exactly why VaR models got blamed in 2008 and why firms add stress testing.

### 🎬 Streaming & marketing — user segmentation (Netflix-style)

- **Problem:** compare engagement across users who watch wildly different amounts.
- **Approach:** standardize each user's watch time into z-scores; segment users into heavy (> +1σ), typical (±1σ), light (< −1σ) viewers.
- **Decision:** tailor retention campaigns per segment; heavy users get "prestige" content pushes, light users get re-engagement offers.

> ⚠️ **Reality check:** real business data is rarely _perfectly_ normal. The normal model is a useful approximation — validate it with histograms and QQ-plots, and remember that averages of many observations become normal even when the raw data isn't (Central Limit Theorem).

---

## 8. Common mistakes to avoid

1. **Treating the density f(x) as a probability** — f(x) can exceed 1; only _areas_ under the curve are probabilities.
2. **Claiming "z = 2 means 2% chance"** — no: z = 2 means the value is 2σ above the mean, and the chance of a value _that high or higher_ is ~2.28% (right tail).
3. **Applying the 68-95-99.7 rule blindly** — it only holds for normal data. For skewed data (income, home prices), ±1σ is not symmetric and the rule is wrong.
4. **Thinking z-scores require normal data** — a z-score is _always computable_ as a standardization. What requires normality is converting that z into probability statements.

---

## 9. Practice exercises

1. Draw 5,000 samples from N(50, 10) and verify the % inside ±1σ, ±2σ, ±3σ yourself.
2. A call center's handle time is N(300, 45) seconds. Compute the z-score of a 400-second call, then use `stats.norm.cdf` to find the % of calls under 400 s and over 400 s.
3. Plot two PDFs on one chart: N(100, 5) and N(100, 20). Explain why the narrow one is taller.
4. Use `stats.norm.ppf` to find the value that separates the top 10% of deliveries from the rest (μ = 100, σ = 15).

---

## Recap

- The normal distribution is defined by **μ** (center) and **σ** (spread); ~68/95/99.7% of data sits within ±1/2/3σ.
- Its PDF formula has two jobs: the exponential part shapes the bell, the `1/(σ√2π)` part makes the total area = 1.
- A **z-score** `z = (x − μ)/σ` expresses any value as "standard deviations from the mean" — universal, comparable units.
- `cdf` turns values into probabilities; `ppf` turns probabilities back into values.
- Businesses use z-scores for anomaly detection, quality control, SLA forecasting, risk measurement, and fair-pay analysis.
