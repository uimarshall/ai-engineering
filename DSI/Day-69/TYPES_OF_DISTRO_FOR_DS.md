# 📊 Probability Distributions in Data Science — A Beginner's Guide (with Python)

> **What you will learn:** what a distribution is, discrete vs. continuous distributions, the famous **Normal distribution** (and why it is called "normal"), its formula broken down piece by piece, how to plot distributions in Python, what the graphs and data points really mean, and how real companies use these ideas to make money and save money.

---

## Table of contents

1. [What is a distribution, anyway?](#1-what-is-a-distribution-anyway)
2. [Key vocabulary (read this once, use it forever)](#2-key-vocabulary)
3. [Discrete distributions](#3-discrete-distributions)
4. [Continuous distributions & the star: the Normal distribution](#4-continuous-distributions)
5. [The graphs — Python code, explained line by line](#5-the-graphs--python-code-explained-line-by-line)
6. [Choosing the right distribution (cheat sheet)](#6-choosing-the-right-distribution-cheat-sheet)
7. [Real company use cases](#7-real-company-use-cases)
8. [Summary & next steps](#8-summary--next-steps)
9. [Glossary](#9-glossary)
10. [Further reading](#10-further-reading)

---

## 1. What is a distribution, anyway?

Imagine you measure the height of **1,000 customers** in a store. You don't just care about one number — you care about the **whole pattern**: how many are 150 cm, how many are 170 cm, how many are 190 cm, and so on.

If you draw that pattern as a **histogram** (bars showing how many people fall in each height range), you get a shape. That shape — _which values are possible, and how likely each one is_ — is the **distribution** of the data.

Formally: a **probability distribution** describes how probability is spread across all possible values of a **random variable** (a number whose value depends on chance, like the height of the next customer).

**Why data scientists care:** almost every business question is really a question about a distribution:

- _How many orders will arrive tomorrow?_ → distribution of demand
- _How long do users spend on our app?_ → distribution of session time
- _What fraction of clicks will convert?_ → distribution of a proportion
- _Is the new version of our website actually better?_ → compare two distributions

If you can describe the distribution, you can **predict the future with a measure of uncertainty** — which is the whole job of statistics.

### Two families of distributions

| Family         | What it describes                    | Example                        | Plotted with                           |
| -------------- | ------------------------------------ | ------------------------------ | -------------------------------------- |
| **Discrete**   | Countable values (0, 1, 2, …)        | Number of purchases per day    | **PMF** (Probability Mass Function)    |
| **Continuous** | Any value in a range (1.72, 1.73, …) | Customer height, delivery time | **PDF** (Probability Density Function) |

- **PMF**: gives the probability of an _exact_ value, e.g. P(X = 3 orders) = 0.2.
- **PDF**: gives a _density_ at each point. For continuous data, probabilities only make sense over a **range**, e.g. P(170 cm < height < 175 cm). You get that by measuring the **area under the curve** between the two values.
- **CDF** (Cumulative Distribution Function): the probability that X is _less than or equal to_ a value, e.g. P(X ≤ 5) = 0.85. Every distribution has one.

### The 4 numbers that summarize any distribution

1. **Mean (μ)** — the average; the "center of mass".
2. **Variance (σ²) / Standard deviation (σ)** — how spread out the values are.
3. **Skewness** — asymmetry. Right-skewed = long tail on the right (mean > median).
4. **Kurtosis** — how heavy the tails are (how often extreme values occur).

> 💡 **Mindset shift:** a distribution is not "math for math's sake". It is the **answer to the question "what can happen, and how likely?"** Businesses run on exactly that question.

---

## 2. Key vocabulary

| Term                            | Meaning (no jargon)                                                                                                                                                 |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Random variable (X)**         | A number produced by chance: next order count, next delivery time                                                                                                   |
| **Parameter**                   | A number that shapes the distribution (e.g. mean μ, std σ). Different parameters = different bell curves                                                            |
| **Support**                     | The set of values the variable can take (e.g. 0, 1, 2… for counts)                                                                                                  |
| **PDF / PMF**                   | Function giving likelihood at a value (continuous / discrete)                                                                                                       |
| **CDF**                         | P(X ≤ x), the "less-than-or-equal-to" probability                                                                                                                   |
| **Quantile / percentile**       | The value below which a given % of data falls (median = 50th percentile)                                                                                            |
| **IID**                         | Independent, identically distributed — samples don't influence each other and come from the same distribution                                                       |
| **Sample vs. population**       | Population = everyone/ everything; sample = the few you measure; statistics estimate the population from samples                                                    |
| **Central Limit Theorem (CLT)** | Averages of many independent samples become **Normal**-shaped, no matter what the original data looks like (this is the superpower behind the Normal distribution!) |

---

## 3. Discrete distributions

### 3.1 Bernoulli — "one biased coin flip"

A single trial with two outcomes: success (1) with probability **p**, failure (0) with probability **1 − p**.

**Formula:** P(X = 1) = p, P(X = 0) = 1 − p

**Example:** "Will this ad be clicked?" — a user either clicks or doesn't.

**Python:**

```python
from scipy.stats import bernoulli
p = 0.3
print(bernoulli.pmf(1, p))   # P(X=1) = 0.3
print(bernoulli.pmf(0, p))   # P(X=0) = 0.7
```

### 3.2 Binomial — "n independent coin flips"

Count the number of successes in **n** independent Bernoulli trials, each with success probability **p**.

**Formula:**

```
P(X = k) = C(n, k) · pᵏ · (1 − p)ⁿ⁻ᵏ

C(n, k) = n! / (k! · (n − k)!)   ← "n choose k": number of ways to pick k successes out of n trials
```

**Breaking the formula down:**

- **pᵏ** — probability that the k successes _all_ happen (each with probability p, multiplied k times)
- **(1 − p)ⁿ⁻ᵏ** — probability that the n − k failures _all_ happen
- **C(n, k)** — how many different orderings give the same result (e.g. 2 successes in 3 flips can be S S F, S F S, or F S S → 3 ways)

**Example:** 20 emails sent; each has a 30% chance of being opened. X = number opened ~ Binomial(n=20, p=0.3).

**Properties:** mean = n·p, variance = n·p·(1 − p)

```python
from scipy.stats import binom
n, p = 20, 0.3
k = 6
print(f"P(exactly {k} opens) = {binom.pmf(k, n, p):.3f}")      # 0.191
print(f"P({k} or fewer)     = {binom.cdf(k, n, p):.3f}")      # 0.608
```

### 3.3 Poisson — "counting rare events in time"

Counts how many events happen in a **fixed interval** (hour, day, square meter) when events occur **independently at a constant average rate λ** ("lambda").

**Formula:**

```
P(X = k) = e⁻ᵏ? No—careful! →   P(X = k) = (λᵏ · e⁻ᵏ?...)

Let's write it properly:
P(X = k) = e^(−λ) · λᵏ / k!
```

**Breaking the formula down:**

- **λ** — the average number of events per interval (e.g. 5 support tickets/hour)
- **λᵏ** — the rate "scaled up" for exactly k events
- **k!** (k factorial) — divides out the many orderings in which events could arrive
- **e^(−λ)** — makes everything sum to 1 (it's the normalizing factor), and it also shrinks the probability for large λ

**Example:** a server gets λ = 5 requests per second. What is P(exactly 3 requests in a second)? → e^(−5)·5³/3! ≈ 0.14.

**Trick worth knowing:** for a Poisson, **mean = variance = λ**. If you measure counts and the variance is much larger than the mean, plain Poisson won't fit (that happens with "bursty" data).

```python
from scipy.stats import poisson
lam = 5
print(f"P(3 requests) = {poisson.pmf(3, lam):.3f}")     # 0.140
print(f"P(≤ 3)        = {poisson.cdf(3, lam):.3f}")     # 0.265
```

---

## 4. Continuous distributions

### 4.1 Uniform — "everything equally likely"

Every value between **a** and **b** has the same density: a flat rectangle.

**Formula:** f(x) = 1 / (b − a), for a ≤ x ≤ b

**Example:** a random arrival time between 9:00 and 10:00; `np.random.uniform(a, b, size=1000)`.

### 4.2 The Normal (Gaussian) distribution — the superstar ⭐

This is the famous **bell curve**. Its PDF:

```
f(x) = 1 / (σ · √(2π))  ·  e^( −(x − μ)² / (2σ²) )
```

Notation: X ~ N(μ, σ²) means "X follows a Normal distribution with mean μ and variance σ²".

#### Why is it called "normal"?

The short answer: **because it became the standard ("the norm") that all other distributions are compared to.** But the history is a story:

1. **1733 — Abraham de Moivre** discovered the curve while approximating binomial probabilities for coin flips. His work was mostly ignored.
2. **1809 — Carl Friedrich Gauss** re-discovered it while studying measurement errors in astronomy and used it to justify the method of least squares. That is why scientists often call it the **Gaussian distribution**.
3. **1830s — Adolphe Quetelet** applied the curve to human data (heights, chest sizes of soldiers) and promoted the idea of _"l'homme moyen"_ (the average man), pushing the curve into the public imagination.
4. **~1893 — Karl Pearson** gave it the name **"normal curve"**. Later (1920) he publicly apologized: _"Many years ago I called the Laplace–Gaussian curve the normal curve, which name, while it avoids an international question of priority, has the disadvantage of leading people to believe that all other distributions are abnormal."_

There is also a deeper mathematical reason it feels "normal":

> **The Central Limit Theorem (CLT):** if you add up (or average) enough independent random influences — no matter what their individual shapes are — the result looks **more and more Normal**. Coin flips, dice throws, tiny measurement errors… thousands of small independent effects add up into one bell shape.

So the Normal distribution is the "default" of nature for anything that is the **sum of many small independent effects** — measurement error, IQ test scores, the average of samples. That's why it earned the title "normal": it is the standard reference curve, the benchmark ("the norm"). But as Pearson warned, other distributions are **not** "abnormal" — they are simply the right tool for other jobs (counts, waiting times, incomes…).

#### The formula, symbol by symbol 🧩

```
f(x) = ( 1 / (σ · √(2π)) ) · e^( −(x − μ)² / (2σ²) )
```

| Piece              | Meaning                               | Intuition                                                                                                                                                                            |
| ------------------ | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **x**              | The value where we evaluate the curve | "How tall is the density at x?"                                                                                                                                                      |
| **μ (mu)**         | The **mean**                          | Location: where the bell is centered. The peak sits exactly at x = μ                                                                                                                 |
| **σ (sigma)**      | The **standard deviation**            | Scale: how wide the bell is. Big σ → wide, flat; small σ → narrow, tall                                                                                                              |
| **(x − μ)**        | Signed distance from the mean         | Far from center → smaller probability                                                                                                                                                |
| **(x − μ)²**       | Squared distance                      | Squaring removes the sign → the curve is perfectly symmetric around μ                                                                                                                |
| **2σ²**            | Twice the variance                    | Converts the squared distance into "standard-deviation units", making the exponent dimensionless                                                                                     |
| **−** (minus sign) | Negative exponent                     | e^(negative) < 1 → probability decays away from the center                                                                                                                           |
| **e^(…)**          | Exponential function                  | Gives the bell its shape: decays faster and faster as you move away from μ                                                                                                           |
| **1/(σ√(2π))**     | The **normalizing constant**          | Guarantees the total area under the whole curve equals exactly 1 (total probability = 1). √(2π) comes from the famous integral ∫e^(−z²/2)dz = √(2π); dividing by σ adjusts the scale |

**A cleaner way to see it:** let **z = (x − μ)/σ** (the _z-score_ — how many standard deviations x is from the mean). Then the exponent becomes **−z²/2**, and the curve is simply:

```
f(z) = (1/√(2π)) · e^(−z²/2)      ← the Standard Normal (μ = 0, σ = 1)
```

The **peak height** is 1/(σ√2π) ≈ 0.399/σ — higher when data is tightly packed around the mean.

#### The 68-95-99.7 rule (empirical rule)

For ANY normal distribution:

| Range  | Share of data | Business translation                                                             |
| ------ | ------------- | -------------------------------------------------------------------------------- |
| μ ± 1σ | ≈ 68%         | Most values live within one std dev of the average                               |
| μ ± 2σ | ≈ 95%         | Nearly everything is within two std devs                                         |
| μ ± 3σ | ≈ 99.7%       | Beyond 3σ is genuinely rare — this is the basis of **Six Sigma** quality control |

**Example:** delivery time ~ Normal(μ = 2 days, σ = 0.5 days) → ~95% of orders arrive within 2 ± 1 days, i.e. between 1 and 3 days.

**Why the z-score matters in business:** if you standardize data (subtract μ, divide by σ), different teams and products can compare "how unusual is this?" on one common scale. A z-score of 2.5 means "this value is 2.5 std devs above the average — quite unusual."

### 4.3 Exponential — "time until the next event"

Models **waiting time** between events of a Poisson process (the continuous cousin of Poisson).

**Formula:** f(x) = λ · e^(−λx), for x ≥ 0; mean = 1/λ

**Example:** if support tickets arrive at λ = 5/hour on average, the waiting time until the next ticket is Exponential with mean 1/5 h = 12 min.

**Famous property — memorylessness:** the time already waited doesn't change the expected remaining wait. (A bus that is "due any minute" is, on average, still 10 minutes away.)

### 4.4 Log-normal — "multiplicative growth"

X is log-normal if **ln(X)** is Normal. Because money, prices, salaries, file sizes, and response times grow by _multiplying_ (10% growth, 2× traffic), they end up right-skewed — the classic **long tail** — and are well described by log-normal.

**Example:** stock prices in the famous **Black–Scholes** model are assumed log-normal (returns are normal, prices are log-normal — prices can never go below 0, and big up-moves happen more often than big down-moves).

### 4.5 Student's t — "normal with fatter tails, for small samples"

Looks like the bell curve but with heavier tails. Used when the sample is small and you don't know the true σ — e.g. **A/B tests** that compare two group means with a t-test. As the degrees of freedom grow, t → Normal.

---

## 5. The graphs — Python code, explained line by line

### Setup (run once)

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, binom, poisson, expon, lognorm, uniform

np.random.seed(42)          # same "randomness" every run → reproducible graphs
plt.rcParams["figure.figsize"] = (9, 5)   # default graph size
plt.rcParams["axes.grid"] = True          # light grid behind plots
plt.rcParams["grid.alpha"] = 0.3          # subtle grid
```

**What each line does:** `numpy` generates numbers, `matplotlib.pyplot` draws, `scipy.stats` contains ready-made distribution functions. The `seed` makes the results repeatable — the "random" numbers are actually the output of an algorithm, and the seed fixes its starting point. The `rcParams` are global style settings so every plot looks neat.

---

### Graph 1 — Binomial PMF: what does a distribution of "success counts" look like?

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))          # 1 row, 2 columns of plots

for ax, p in zip(axes, [0.3, 0.7]):                      # left: p=0.3, right: p=0.7
    n = 20                                               # 20 trials per graph
    k_values = np.arange(0, n + 1)                       # possible counts: 0..20
    probabilities = binom.pmf(k_values, n, p)            # P(X=k) for every k

    ax.stem(k_values, probabilities, basefmt=" ")        # draw one "needle" per k
    ax.set_title(f"Binomial(n={n}, p={p})")
    ax.set_xlabel("Number of successes k")
    ax.set_ylabel("P(X = k)")
    ax.axvline(n * p, color="red", ls="--", label=f"mean = np = {n * p:.0f}")
    ax.legend()

plt.tight_layout()                                       # prevent overlapping labels
plt.show()
```

**What the code does, line by line:** `subplots(1, 2)` creates a 1×2 grid of axes and returns them as a list. The `zip` loop runs the same drawing instructions twice with different success probabilities p. `np.arange(0, 21)` builds the k-axis (integers 0 to 20 — the possible numbers of successes). `binom.pmf(k_values, n, p)` computes the whole probability vector in one call (SciPy broadcasts over the array). `ax.stem` draws each (k, P(X=k)) pair as a vertical needle — the standard way to visualize a PMF, because probabilities exist _only at integer points_, not in between. `axvline` draws a dashed red vertical line at the theoretical mean n·p so you can see the distribution is centered on it.

**What the data points in the graph mean:** every needle is one "story": the needle above k = 6 (left panel) sits at height ≈ 0.19, meaning "if each of 20 people has a 30% chance to buy, the chance that exactly 6 buy is about 19%." If you added up the heights of all 21 needles you'd get exactly 1.0 — that is the PMF's "probability budget". Notice the p=0.3 graph is **right-skewed** (long right tail) and p=0.7 is its mirror image: success is common, so the mass shifts right and skewness flips.

---

### Graph 2 — Poisson PMF: rare events at different rates

```python
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

for ax, lam in zip(axes, [2, 5, 10]):                    # λ = 2, 5, 10 events/interval
    k_values = np.arange(0, 25)                          # counts 0..24
    probs = poisson.pmf(k_values, lam)                   # P(X=k) for each k

    ax.stem(k_values, probs, basefmt=" ")
    ax.set_title(f"Poisson(λ={lam})")
    ax.set_xlabel("Number of events k")
    ax.set_ylabel("P(X = k)")
    ax.axvline(lam, color="red", ls="--", label=f"mean = λ = {lam}")
    ax.legend()

plt.tight_layout()
plt.show()
```

**What the code does:** identical structure to Graph 1, but the probability model is now `poisson.pmf` with rate λ, and the k-axis is 0..24 (events can theoretically be any non-negative integer; we just cut the graph where probability is essentially 0).

**What the data points mean:** each needle at integer k is the probability of seeing exactly k events in one interval. In the λ=2 panel, the needle at k=0 is ≈ 0.135 — "when the average is 2 events per hour, about 13.5% of hours have zero events." That counter-intuitive fact (the _most likely_ count is not guaranteed to happen) is visible directly in the graph. The three panels together show the **central insight**: as λ grows, the Poisson looks more and more symmetric — in fact it approaches the Normal distribution. That is the CLT sneaking in again.

---

### Graph 3 — The Normal PDF: μ moves it, σ stretches it

```python
x = np.linspace(-6, 6, 500)                               # dense x-axis from -6 to 6

fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

# Left: different means (same spread)
for mu in [-2, 0, 2]:
    axes[0].plot(x, norm.pdf(x, mu, 1), label=f"μ = {mu}, σ = 1")
axes[0].set_title("Changing the mean μ slides the bell")
axes[0].set_xlabel("x"); axes[0].set_ylabel("density f(x)"); axes[0].legend()

# Right: different standard deviations (same mean)
for sigma in [0.5, 1, 2]:
    axes[1].plot(x, norm.pdf(x, 0, sigma), label=f"σ = {sigma}, μ = 0")
axes[1].set_title("Changing the std σ widens/flattens the bell")
axes[1].set_xlabel("x"); axes[1].set_ylabel("density f(x)"); axes[1].legend()

plt.tight_layout()
plt.show()
```

**What the code does:** `np.linspace(-6, 6, 500)` creates 500 evenly spaced x values — the "canvas" of the curve. Each `norm.pdf(x, mu, sigma)` call evaluates the Normal formula from Section 4.2 at all 500 points at once, returning 500 densities that `plot` connects into a smooth line.

**What the data points mean:** every point on a curve is a (x, f(x)) pair: "the density at x is f(x)". The left panel shows that **μ is a location parameter** — it only slides the bell left/right. The right panel shows **σ is a scale parameter** — small σ piles probability tightly near the mean (tall, skinny bell), large σ spreads it out (short, wide bell). Because the total area must always be 1, making the bell wider _forces_ it to be shorter. The curves never touch zero: mathematically the Normal extends to ±∞, though in practice probability beyond μ ± 4σ is negligible.

---

### Graph 4 — Real data vs. the fitted Normal curve (heights)

```python
np.random.seed(7)
heights = np.random.normal(loc=170, scale=7, size=1000)   # 1000 simulated heights (cm)

fig, ax = plt.subplots()
ax.hist(heights, bins=30, density=True, alpha=0.65,
        color="steelblue", edgecolor="white",
        label="Sample histogram (1000 people)")
ax.set_xlabel("Height (cm)"); ax.set_ylabel("Density")

x_grid = np.linspace(heights.min(), heights.max(), 300)   # fine x-axis for the curve
mu_hat, sigma_hat = heights.mean(), heights.std(ddof=1)   # estimate μ and σ from the data
ax.plot(x_grid, norm.pdf(x_grid, mu_hat, sigma_hat), "r-", lw=2,
        label=f"Fitted Normal(μ={mu_hat:.1f}, σ={sigma_hat:.1f})")
ax.set_title("Histogram of heights with fitted Normal curve")
ax.legend()
plt.show()
```

**What the code does:** `np.random.normal(170, 7, 1000)` _simulates_ 1,000 heights from a true Normal with mean 170 cm and std 7 cm (real survey data would come from a CSV instead). `hist(..., density=True)` turns counts into **densities** (bar area sums to 1), so the histogram and the PDF are on the same scale and can be overlaid. `heights.mean()` and `heights.std(ddof=1)` estimate the parameters from the data (ddof=1 uses the sample standard deviation formula with n−1). Finally the red curve plots the theoretical Normal built from those estimates.

**What the data points mean:** each **bar** is a _count of people_ — its height shows how many of the 1000 people fell in that height bin (e.g. the bar around 170 cm is the tallest because 170 cm is the most common region). Each **point on the red curve** is the density predicted by the Normal _formula_ for that height. The graph teaches a core data-science lesson: **the formula (theory) and the histogram (data) agree almost perfectly** — that's what "the data follows a Normal distribution" looks like. Real-world data never matches exactly (sampling noise), so we ask "close enough?" rather than "identical?".

---

### Graph 5 — The Central Limit Theorem in action 🎩

```python
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

for ax, n in zip(axes, [1, 5, 30]):
    sample_means = [np.random.uniform(0, 1, n).mean() for _ in range(10_000)]

    ax.hist(sample_means, bins=40, density=True, alpha=0.7,
            color="mediumseagreen", edgecolor="white")
    ax.set_title(f"Mean of n = {n} Uniform(0,1) samples")
    ax.set_xlabel("Sample mean"); ax.set_ylabel("Density")

plt.tight_layout()
plt.show()
```

**What the code does:** we take a **flat** (uniform) distribution — as far from Normal as you can get — and repeatedly draw samples of size n. `np.random.uniform(0, 1, n)` gives one sample of n numbers; `.mean()` averages them; the list comprehension repeats that 10,000 times; the histogram shows the distribution of those 10,000 averages.

**What the data points mean:** the left panel (n = 1) is just the original uniform shape — flat, no bell. With n = 5 the histogram already shows a gentle dome. With n = 30 it is a clean bell — _even though the source data was completely flat!_ Each bar counts how many of the 10,000 experiments produced an average in that narrow range. This is the CLT made visible: **averages of many small random pieces converge to Normal**, which is why companies can treat the _average_ of anything (average spend per user, average delivery time per route) as Normal even when individual values are skewed. The bell also gets _narrower_ as n grows — averaging more data shrinks uncertainty (the standard error = σ/√n).

---

### Graph 6 — Skewness: why "average" can lie (Normal vs Exponential vs Log-normal)

```python
x = np.linspace(0.001, 8, 500)                            # positive x-axis only

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, norm.pdf(x, 4, 1), label="Normal(μ=4, σ=1) — symmetric")
ax.plot(x, expon.pdf(x, scale=1.5), label="Exponential(λ=1/1.5) — right-skewed")
ax.plot(x, lognorm.pdf(x, s=0.8, scale=1), label="Log-normal(s=0.8) — right-skewed")
ax.set_xlim(0, 8); ax.set_ylim(0, 0.75)
ax.set_xlabel("Value"); ax.set_ylabel("Density")
ax.set_title("Same-ish support, very different shapes → different business conclusions")
ax.legend()
plt.show()
```

**What the code does:** plots three PDFs on one axis. `expon.pdf(x, scale=1.5)` uses SciPy's convention where `scale = 1/λ` (so mean = 1.5). `lognorm.pdf(x, s=0.8, scale=1)` uses shape parameter `s` (the σ of the underlying Normal).

**What the data points mean:** the Normal is a symmetric mound — mean = median = mode. The Exponential crashes down from its highest point at 0 and decays — the _most common_ value is near zero, yet the _average_ is 1.5: most values are small, a few are large. The Log-normal peaks away from zero with a long right tail. This is why, for skewed business data (income, purchase amounts, claim costs), the **median** is often the more honest summary than the mean, and why assuming "Normal" on skewed data produces wrong forecasts and wrong risk estimates. Points near the right tail look harmless on the graph but are _huge_ in money terms — that is the essence of tail risk.

---

## 6. Choosing the right distribution (cheat sheet)

| Your data…                               | Use             | Real-world question                     |
| ---------------------------------------- | --------------- | --------------------------------------- |
| Yes/no outcome of one trial              | **Bernoulli**   | Will this visitor click?                |
| Count of successes in n trials           | **Binomial**    | How many of 100 emails get opened?      |
| Count of events in time/space            | **Poisson**     | How many orders arrive this hour?       |
| Time until next event                    | **Exponential** | How long until the next support ticket? |
| Anything in a range, all equally likely  | **Uniform**     | Random A/B test assignment              |
| Sum/average of many effects; measurement | **Normal**      | Height, test scores, delivery time      |
| Positive, right-skewed, multiplicative   | **Log-normal**  | Income, prices, claim sizes, latency    |
| Small samples, unknown σ                 | **Student's t** | A/B test significance testing           |

**Quick test for normality (informal):** histogram roughly symmetric with a single peak, mean ≈ median, ~68% of data within ±1 std of the mean, and a **Q-Q plot** (data quantiles vs. theoretical normal quantiles) forming a straight line. Formal tests exist (Shapiro–Wilk), but for big samples they flag tiny deviations — always _look at the plot first_.

---

## 7. Real company use cases

### 🛒 Amazon / retail — demand forecasting & safety stock

Retailers must decide _how much inventory to keep_. Daily demand is modeled as a distribution (often Normal for steady sellers, Log-normal or Poisson-like for spiky categories). The **safety stock** formula is directly built on the Normal:

```
safety stock = z · σ_demand · √(lead time)
```

where z comes from the service level (z ≈ 1.65 for 95%). **Why it matters:** too little stock = lost sales; too much = warehousing costs. Distributions let Amazon pick the number that maximizes profit instead of guessing.

### 🚗 Uber / Lyft — Poisson arrivals & surge pricing

Trip requests arriving at a zone behave like a **Poisson process**; idle drivers and wait times relate to the **Exponential** distribution. Forecasters predict request _rates per zone per minute_, then set **surge pricing** so supply catches up with demand. **Why it matters:** pricing is a direct function of a predicted distribution, not a gut feeling. Uber's engineering blog has described trip segments as approximately **log-normal** — heavy right tail from traffic outliers.

### 🎬 Netflix / Google — A/B testing with the Normal & t-distributions

When Netflix tests two recommendation algorithms, it splits users randomly and compares average watch time. By the CLT, the _difference of the two group averages_ is approximately Normal, so a **t-test** (Student's t) computes: "if the true effect were zero, how likely is this observed difference?" If p < 5%, the difference is unlikely to be chance. **Why it matters:** teams ship only changes with statistically convincing wins — avoiding both missed wins (false negatives) and costly bad launches (false positives).

### 🏦 Insurance & banks — Poisson frequency + Log-normal severity

The classic **collective risk model** splits claims into two distributions: _how many_ claims arrive (Poisson) and _how big_ each claim is (Log-normal or Gamma — skewed, never negative, with rare enormous claims). Adding them up gives the total loss distribution, from which the insurer reads the **99.5th percentile** to set premiums and reserves. Stock-option pricing uses the **log-normal** assumption inside Black–Scholes. **Why it matters:** an insurer that models severity as Normal would under-price catastrophic claims and go bankrupt; the log-normal tail _is_ the business risk.

### ☎️ Call centers — Erlang formulas (Poisson built-in)

Call arrivals per minute are modeled as Poisson; service times as Exponential. The **Erlang C** formula then predicts how many agents are needed so that, say, 80% of callers wait under 20 seconds. **Why it matters:** staffing cost is the call center's biggest expense; the model finds the minimum agents that hit the service target — millions saved per year at large operators.

### 🏭 Manufacturing — Six Sigma quality control

Process measurements (bottle fill volume, bolt diameter) are treated as Normal around a target μ with spread σ. **Six Sigma** means the nearest specification limit is 6σ away from μ, so defects occur at ~3.4 per million. Control charts flag points beyond μ ± 3σ as "out of control". **Why it matters:** Motorola and Toyota-style lean operations use exactly this Normal-based reasoning to drive defect rates toward zero.

### 💳 Fraud & payments — rare-event monitoring

Fraud is rare: per merchant, fraudulent transactions per day can be modeled with a **Poisson** or **Binomial** baseline. When observed counts exceed the distribution's expected range (e.g. above the 99th percentile), an alert fires and a case is opened. **Why it matters:** distribution-aware anomaly detection catches spikes early while avoiding alert fatigue from normal randomness.

**The pattern in all of these:** a company translates a business process into a random variable, fits (or assumes) a distribution, then answers a money question — how much stock, what price, is the change real, how many staff, what reserve, is this anomalous?

---

## 8. Summary & next steps

**One-paragraph summary:** A distribution tells you what values can occur and how likely each is. Discrete data (counts) uses PMFs and distributions like Bernoulli, Binomial, and Poisson. Continuous data uses PDFs and distributions like Uniform, Normal, Exponential, and Log-normal. The Normal is the benchmark — literally "the standard" — partly because of history (Gauss, Quetelet, Pearson) and partly because the Central Limit Theorem makes averages of almost anything bell-shaped. Its formula is just an exponential bell controlled by μ (center) and σ (spread) and normalized so its area equals 1.

**Next steps to practice:**

1. Run every code block in this guide and change the parameters (p, λ, μ, σ) — feel how the shape reacts.
2. Take one real dataset (e.g. `sklearn.datasets` or any CSV) and check which distribution each column resembles.
3. Fit distributions with SciPy: `norm.fit(data)` returns (μ, σ); compare fits visually with `stats.probplot(data, dist="norm")`.
4. Learn the **t-test / chi-squared** machinery — they are just distribution comparisons.
5. Build a tiny business sim: simulate daily demand, add a Normal noise, compute the safety stock, and watch profit change.

---

## 9. Glossary

| Term                       | Definition                                                                            |
| -------------------------- | ------------------------------------------------------------------------------------- |
| **PMF**                    | Probability Mass Function: P(X = k) for discrete X                                    |
| **PDF**                    | Probability Density Function: f(x) for continuous X; probabilities are areas under it |
| **CDF**                    | F(x) = P(X ≤ x); always starts at 0 and rises to 1                                    |
| **Mean (μ)**               | Long-run average; the balance point of the distribution                               |
| **Variance (σ²)**          | Average squared distance from the mean                                                |
| **Standard deviation (σ)** | √variance; the natural unit of spread                                                 |
| **Skewness**               | Asymmetry: right-skewed → long right tail, mean > median                              |
| **Kurtosis**               | Tail heaviness; high kurtosis = frequent extremes                                     |
| **Quantile**               | Value below which a given fraction of data falls                                      |
| **z-score**                | (x − μ)/σ: distance from mean in std-dev units                                        |
| **CLT**                    | Averages of many independent draws → Normal                                           |
| **68-95-99.7 rule**        | Share of Normal data within 1/2/3 std devs of the mean                                |
| **Degrees of freedom**     | Effective sample size minus parameters estimated; shapes the t-distribution           |

---

## 10. Further reading

- NIST/SEMATECH e-Handbook of Statistical Methods (free, authoritative)
- "The Normal Distribution" — Karl Pearson's 1920 note on the name (history)
- SciPy docs: `scipy.stats.norm`, `binom`, `poisson`, `expon`, `lognorm`
- Matplotlib gallery — histograms and probability plots
- Uber Engineering, Netflix TechBlog, Google Research blog: real posts on A/B testing, forecasting, and arrivals modeling

_Remember: the Normal distribution is the most famous, but not the only, tool — the right distribution is the one that matches how your data is actually produced._ 🎯
