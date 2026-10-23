# Understanding p-values in Linear Regression — a Practical Guide for ML

> **Level:** Beginner · **Format:** intuition → formulas → runnable code → plots → business examples
> **Companion script:** `understanding_pvalues.py` — the **12 numbered code blocks** in this tutorial, taken in order, _are_ that script. Read the tutorial and run the code at the same time.

---

## 0. Setup

```bash
pip install numpy pandas matplotlib scipy scikit-learn statsmodels
```

- `statsmodels` gives the classic regression summary table (the one with `P>|t|`). If it is not installed, the script still runs — it computes every p-value by hand with `scipy`, so you can see exactly what is going on under the hood.
- All figures are saved to `./plots/` **before** they are shown (`plt.savefig(...)` then `plt.show()`).
- All data is either synthetic (we know the ground truth!) or bundled with scikit-learn — no internet downloads needed.

---

## 1. Why should an ML practitioner care about p-values?

In linear regression (and most of ML), you fit coefficients like

```
y = b0 + b1·x1 + b2·x2 + ... + noise
```

The boss asks: **"Which features actually matter?"** The p-value is the classical answer to: _"Could this coefficient be just noise?"_

Practical uses:

- **Feature filtering** — drop predictors that show no statistical evidence of an effect.
- **Model documentation / governance** — regulators and auditors expect you to justify which variables you kept.
- **Stakeholder communication** — "the campaign coefficient has p = 0.003" is a defensible way to say "the lift is real, not luck."
- **Avoiding overfitting** — a feature whose p-value is large is a candidate for removal (with caveats, see §16).

---

## 2. The big idea: what a p-value _really_ is

**Formal definition:** the p-value is the probability of observing a test statistic _at least as extreme_ as the one you got, **assuming the null hypothesis is true** (here: assuming the true coefficient is 0).

**Courtroom analogy.** In a trial, the defendant is _presumed innocent_ until proven guilty. In regression, every coefficient is _presumed to be 0_ until the data proves otherwise.

- The p-value is like the probability that the evidence would look this suspicious **if the defendant were innocent**.
- If that probability is tiny (p < 0.05), we say: "the evidence is too unlikely under innocence — declare the coefficient guilty (non-zero)."
- If the probability is large (p ≥ 0.05), we say: "not enough evidence to convict." **The defendant is not proven innocent — just not proven guilty.**

**Two things a p-value is NOT (read twice):**

- ❌ It is **not** the probability that the coefficient is 0.
- ❌ It is **not** the probability that you made a mistake, and it is **not** the effect size.

---

## 3. The hypothesis test behind every coefficient

For each coefficient βᵢ, linear-regression software tests:

|                        |                                           |
| ---------------------- | ----------------------------------------- |
| **Null hypothesis H₀** | βᵢ = 0 (the feature has _no_ effect on y) |
| **Alternative H₁**     | βᵢ ≠ 0 (the feature _does_ affect y)      |

**Decision rule** (with significance level α = 0.05 by convention):

| p-value  | What you say                    | Meaning                                       |
| -------- | ------------------------------- | --------------------------------------------- |
| p < 0.05 | "statistically significant"     | Reject H₀ — evidence the coefficient is not 0 |
| p ≥ 0.05 | "not statistically significant" | Fail to reject H₀ — not enough evidence       |

Classic significance stars (statsmodels style):

| p-value | Stars  | Strength of evidence |
| ------- | ------ | -------------------- |
| < 0.001 | `***`  | very strong          |
| < 0.01  | `**`   | strong               |
| < 0.05  | `*`    | moderate             |
| ≥ 0.05  | (none) | weak / inconclusive  |

**Alpha (α) is the false-positive budget you accept:** if you test 100 _pure-noise_ features, expect about `100 × 0.05 = 5` of them to look "significant" by pure chance. Demo 8 proves this empirically.

---

## 4. The formulas, broken down piece by piece

Every p-value in a regression summary comes from just three steps.

### Step 1 — the t-statistic: signal ÷ noise

```
t = coef / SE(coef)
```

- `coef` = the estimated slope (the **signal**: how much y moves per unit of x).
- `SE(coef)` = the standard error (the **noise**: how uncertain that estimate is).

A big |t| means the signal is large relative to the uncertainty.

### Step 2 — where the standard error comes from

```
SE(β̂) = sqrt( σ̂² · (XᵀX)⁻¹_diagonal )
σ̂²  = RSS / (n − k − 1)          (RSS = sum of squared residuals)
```

- `n` = number of rows, `k` = number of predictors (plus 1 for the intercept).
- `σ̂²` (MSE) = average squared error the model makes.
- `(XᵀX)⁻¹` = a matrix that encodes how much the data "spreads out" — more spread → smaller SE.
- More data → smaller SE. Correlated predictors → bigger SE (Demo 7).

### Step 3 — turning t into a p-value (two-tailed test)

```
p = 2 · (1 − T_{n−k−1}(|t|))
```

where `T_{df}` is the cumulative distribution function of Student's **t-distribution** with `df = n − k − 1` degrees of freedom. This simply computes the **area under both tails** of the t-curve beyond `|t|` — Demo 2 draws this area for you.

### Worked mini-example (do it by hand once)

- Suppose `coef = 0.5` and `SE = 0.2` → `t = 0.5 / 0.2 = 2.5`
- Suppose `df = 150` → the two-tailed area beyond ±2.5 is about `0.013`
- **Conclusion:** if the true coefficient were 0, we would see a t this extreme only ~1.3% of the time. Since 0.013 < 0.05 → **reject H₀**, the coefficient is statistically significant.

That is all the software does — the demos below reproduce it from scratch.

---

## 5. Demo 1 — Regression with known ground truth

We generate data where **we** decide the truth: only feature 2 and feature 4 affect y. Then we fit a regression and read the p-values. Features whose true coefficient is 0 should (usually) show large p-values; real effects should show tiny ones.

### Code block 1 — imports + configuration

```python
# Code block 1: imports and global configuration
import os                                   # for creating the plots folder

import numpy as np                          # numerical arrays
import pandas as pd                         # tables (DataFrames)
import matplotlib.pyplot as plt             # plotting
from scipy import stats                     # t-distribution -> p-values
from sklearn.datasets import load_diabetes  # bundled, offline-safe real data

try:                                        # statsmodels = classic summary tables
    import statsmodels.api as sm
    HAS_SM = True
except ImportError:                         # optional: script still works without it
    HAS_SM = False
    print("tip: 'pip install statsmodels' gives you the classic OLS summary table.\n")

np.set_printoptions(suppress=True, precision=4)   # cleaner console output
pd.set_option("display.float_format", lambda v: f"{v:.4f}")  # tidy tables

os.makedirs("plots", exist_ok=True)         # make sure ./plots exists
plt.rcParams["figure.figsize"] = (10, 6)    # default figure size
plt.rcParams["axes.grid"] = True            # grid on every plot
```

### Code block 2 — helper functions (the maths behind the scenes)

```python
# Code block 2: helpers - these implement Section 4's formulas exactly

def add_constant(X):
    """Add a column of 1s so the model can learn an intercept (b0)."""
    return np.column_stack([np.ones(len(X)), X])


def stars(p):
    """Turn a p-value into significance stars, statsmodels style."""
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return ""


def fit_ols_table(X_design, y, names):
    """Fit OLS by hand and return coef, std_err, t, p_value for every column.

    This is exactly what statsmodels does internally:
        beta    = (X'X)^-1 X'y            (least squares solution)
        MSE     = RSS / (n - k)           (error variance estimate)
        SE      = sqrt(MSE * diag((X'X)^-1))
        t       = beta / SE               (signal / noise)
        p       = 2 * (1 - T_{df}(|t|))   (two-tailed p-value)
    """
    n, k = X_design.shape                  # k = intercept + number of predictors
    beta = np.linalg.lstsq(X_design, y, rcond=None)[0]   # solve normal equations
    resid = y - X_design @ beta            # residuals = what the model missed
    df_resid = n - k                       # degrees of freedom left after fitting
    mse = resid @ resid / df_resid         # unbiased estimate of error variance
    cov = mse * np.linalg.inv(X_design.T @ X_design)     # covariance of coefficients
    se = np.sqrt(np.diag(cov))             # standard errors = sqrt of diagonal
    t = beta / se                          # t-statistic for each coefficient
    p = 2 * (1 - stats.t.cdf(np.abs(t), df=df_resid))    # two-tailed p-value

    table = pd.DataFrame({"coef": beta, "std_err": se, "t": t, "p_value": p},
                         index=names)      # one row per coefficient
    table["sig"] = [stars(pv) for pv in p]  # add the * markers
    return table


def print_statsmodels(X_design, y, names):
    """Print the classic statsmodels summary if the package is available."""
    if not HAS_SM:                          # fallback if statsmodels missing
        print("(statsmodels not installed -> showing the manual table instead)")
        return
    X_df = pd.DataFrame(X_design, columns=names)   # give columns readable names
    print(sm.OLS(y, X_df).fit().summary())  # the famous regression summary


def banner(title):
    """Print a section banner so demo output is easy to follow."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
```

### Code block 3 — Demo 1: fit on data where we know the truth

```python
# Code block 3: Demo 1 - known ground truth

def demo1_known_truth():
    """Fit OLS where the REAL coefficients are known, then interpret p-values."""
    banner("Demo 1 - Regression with known ground truth")

    rng = np.random.default_rng(42)         # fixed seed -> reproducible results
    n = 200                                 # 200 rows of data
    X = rng.normal(size=(n, 4))             # 4 standardised predictor columns
    true_coefs = np.array([0.0, 2.5, 0.0, -1.8])  # ONLY features 2 and 4 matter
    y = X @ true_coefs + rng.normal(scale=2.0, size=n)  # y = truth + noise

    names = ["intercept", "feature_1", "feature_2", "feature_3", "feature_4"]
    design = add_constant(X)                # prepend the intercept column

    print("True coefficients:", true_coefs)
    print("(only feature_2 and feature_4 truly affect y)\n")

    print(">>> statsmodels summary (the classic output):")
    print_statsmodels(design, y, names)     # full summary with P>|t| column

    print(">>> Same numbers computed by hand (for comparison):")
    table = fit_ols_table(design, y, names) # our own OLS + p-values
    print(table.round(4).to_string())       # print the table

    print("\nHow to read this:")
    print(" - feature_2: coef ~ 2.5, huge t, p << 0.05   -> real effect.")
    print(" - feature_4: coef ~ -1.8, huge |t|, p << 0.05 -> real effect.")
    print(" - feature_1 / feature_3: true coefficient is 0.0 -> p is usually > 0.05,")
    print("   but by pure chance it will be < 0.05 about 5% of the time (Demo 8).")
    return table                            # reuse the table in other demos if needed
```

**What you should see:** `feature_2` and `feature_4` have t-values around +17 and −12 (p ≈ 10⁻⁴⁰ and 10⁻²⁵ — astronomically small). `feature_1` and `feature_3` (true coefficient 0) usually show p > 0.05. The statsmodels table and the hand-computed table match to many decimals — proof that the math in §4 is the real thing.

---

## 6. Demo 2 — drawing the p-value as an area

The p-value is literally the **shaded area under both tails** of the t-distribution beyond the observed |t|. This demo draws that picture.

### Code block 4 — Demo 2: visualise the p-value

```python
# Code block 4: Demo 2 - the p-value as a shaded area

def demo2_ttest_visual():
    """Draw the t-distribution and shade the two tails that define the p-value."""
    banner("Demo 2 - What the p-value actually IS (a shaded area)")

    df = 195                                # 200 rows - 5 fitted coefficients
    t_obs = 2.1                             # a moderate, realistic t-statistic
    p_value = 2 * (1 - stats.t.cdf(t_obs, df))   # two-tailed p-value formula
    print(f"For t = {t_obs} with df = {df}:  p-value = {p_value:.4f}")
    print("Interpretation: if the true coefficient were 0, a t this extreme")
    print(f"would occur by chance only {p_value * 100:.2f}% of the time.\n")

    t_grid = np.linspace(-6, 6, 800)        # smooth range of t values
    pdf = stats.t.pdf(t_grid, df)           # height of the t-curve at each t
    plt.figure()
    plt.plot(t_grid, pdf, lw=2, color="black", label=f"t-distribution (df={df})")

    left = t_grid <= -t_obs                 # far-left tail (beyond -2.1)
    right = t_grid >= t_obs                 # far-right tail (beyond +2.1)
    plt.fill_between(t_grid, pdf, where=left,  color="red", alpha=0.6, label="p-value area")
    plt.fill_between(t_grid, pdf, where=right, color="red", alpha=0.6)
    plt.axvline(t_obs,  color="blue", ls="--", label=f"observed t = {t_obs}")
    plt.axvline(-t_obs, color="blue", ls="--")
    plt.title(f"Two-tailed p-value = shaded area = {p_value:.4f}")
    plt.xlabel("t"); plt.ylabel("probability density")
    plt.legend()
    plt.savefig("plots/pvalue_t_distribution.png", dpi=130, bbox_inches="tight")
    plt.show()                              # saved BEFORE showing

    # Reality check: the strong feature from Demo 1 has a much bigger t
    rng = np.random.default_rng(42)         # rebuild the same dataset
    X = rng.normal(size=(200, 4))
    y = X @ np.array([0.0, 2.5, 0.0, -1.8]) + rng.normal(scale=2.0, size=200)
    table = fit_ols_table(add_constant(X), y,
                          ["intercept", "f1", "f2", "f3", "f4"])
    t_real = table.loc["f2", "t"]           # t of the strong feature
    p_real = table.loc["f2", "p_value"]     # its (tiny) p-value
    print(f"(Real example: feature_2 has t = {t_real:.2f} and p = {p_real:.3g} -")
    print(" that tiny p is an invisible sliver of shaded area!)")
```

**What you should see:** `plots/pvalue_t_distribution.png` — a bell-shaped t-curve with two red tails. The p-value is their combined area. Bigger t → smaller tails → smaller p. Real effects (t ≈ 17) have p-values so small they are effectively 0.

---

## 7. Demo 3 — p-value bar chart for every feature

A quick visual: bars below the α = 0.05 line are "statistically significant".

### Code block 5 — Demo 3: bar chart of p-values

```python
# Code block 5: Demo 3 - bar chart of p-values vs alpha = 0.05

def demo3_pvalue_barchart():
    """Plot every coefficient's p-value with the alpha = 0.05 threshold line."""
    banner("Demo 3 - Bar chart of p-values for every coefficient")

    rng = np.random.default_rng(42)         # same data as Demo 1
    X = rng.normal(size=(200, 4))
    y = X @ np.array([0.0, 2.5, 0.0, -1.8]) + rng.normal(scale=2.0, size=200)
    names = ["intercept", "feature_1", "feature_2", "feature_3", "feature_4"]
    table = fit_ols_table(add_constant(X), y, names)   # fit + p-values

    feats = ["feature_1", "feature_2", "feature_3", "feature_4"]
    p_vals = table.loc[feats, "p_value"].values       # p-values only

    plt.figure()
    colors = ["green" if p < 0.05 else "gray" for p in p_vals]  # colour by verdict
    plt.bar(feats, p_vals, color=colors)
    plt.axhline(0.05, color="red", ls="--", lw=2, label="alpha = 0.05")
    plt.yscale("log")                        # p-values span orders of magnitude
    plt.ylabel("p-value (log scale)")
    plt.title("Coefficient p-values: green = significant (p < 0.05)")
    plt.legend()
    plt.savefig("plots/feature_pvalues.png", dpi=130, bbox_inches="tight")
    plt.show()
    print("feature_2 and feature_4 are green (real effects);")
    print("feature_1 and feature_3 are gray (their true coefficient is 0.0).")
```

---

## 8. Demo 4 — the t ⇄ p curve

One curve to rule them all: as |t| grows, p collapses.

### Code block 6 — Demo 4: how t maps to p

```python
# Code block 6: Demo 4 - the t <-> p relationship

def demo4_t_to_p_curve():
    """Show that bigger |t| always means smaller p (for a fixed df)."""
    banner("Demo 4 - Bigger |t| means smaller p")

    df = 195                                # degrees of freedom used everywhere here
    t_grid = np.linspace(0, 5, 200)         # |t| from 0 to 5
    p_grid = 2 * (1 - stats.t.cdf(t_grid, df))     # two-tailed p for each t
    t_crit = stats.t.ppf(0.975, df)         # the t where p crosses 0.05
    print(f"The p-value hits 0.05 exactly when |t| = {t_crit:.3f} (df = {df})")
    print("=> |t| > 1.97 means p < 0.05 for this df.\n")

    plt.figure()
    plt.plot(t_grid, p_grid, lw=2, color="purple", label="p-value")
    plt.axhline(0.05, color="red", ls="--", lw=2, label="p = 0.05")
    plt.axvline(t_crit, color="orange", ls=":", lw=2, label=f"|t| = {t_crit:.2f}")
    plt.yscale("log")                        # p is tiny for large t
    plt.xlabel("|t| statistic")
    plt.ylabel("p-value (log scale)")
    plt.title("p-value shrinks as |t| grows: t large -> strong evidence")
    plt.legend()
    plt.savefig("plots/t_to_p_curve.png", dpi=130, bbox_inches="tight")
    plt.show()
```

---

## 9. Demo 5 — sample size: statistical vs practical significance

This is the most important _business_ lesson: **the same real effect becomes "significant" simply by collecting more data.** The coefficient does not change; its standard error shrinks with √n, so t grows and p drops.

### Code block 7 — Demo 5: sample-size effect

```python
# Code block 7: Demo 5 - sample size effect

def demo5_sample_size():
    """Keep the effect fixed (slope = 0.3) and watch p shrink as n grows."""
    banner("Demo 5 - Sample size effect: same effect, different p-value")

    n_values = [20, 30, 50, 75, 100, 150, 200, 300, 500, 800, 1200]
    rows = []
    for n in n_values:                       # loop over sample sizes
        rng = np.random.default_rng(n)       # different seed per n (reproducible)
        x = rng.normal(size=n)               # one predictor
        y = 0.3 * x + rng.normal(size=n)     # SMALL but REAL effect: slope 0.3
        t = fit_ols_table(add_constant(x), y, ["intercept", "x"])
        rows.append((n,
                     t.loc["x", "coef"],     # estimated slope (stays ~0.3)
                     t.loc["x", "std_err"],  # uncertainty (shrinks with n)
                     t.loc["x", "t"],        # t = coef / SE (grows)
                     t.loc["x", "p_value"])) # p (shrinks)

    df = pd.DataFrame(rows, columns=["n", "coef", "std_err", "t", "p_value"])
    print(df.round(4).to_string(index=False))
    print("\nThe coefficient stays around 0.3 (the effect did NOT get bigger) -")
    print("only the standard error shrinks, so t grows and p drops.")

    plt.figure()
    plt.plot(df["n"], df["p_value"], marker="o", color="teal", label="p-value")
    plt.axhline(0.05, color="red", ls="--", lw=2, label="alpha = 0.05")
    plt.xscale("log")                        # spread the n values out
    plt.yscale("log")
    plt.xlabel("sample size n (log scale)")
    plt.ylabel("p-value (log scale)")
    plt.title("Same real effect (slope = 0.3): more data -> smaller p")
    plt.legend()
    plt.savefig("plots/sample_size_effect.png", dpi=130, bbox_inches="tight")
    plt.show()
    print("\nBusiness takeaway: with n = 1,000,000 almost EVERYTHING is")
    print("'statistically significant'. Always ask: is the SIZE of the effect")
    print("practically meaningful, or just statistically detectable?")
```

**What you should see:** with n = 20 the effect (p ≈ 0.2) is invisible; with n = 1200 the identical slope 0.3 has p ≈ 0.0001. The _effect size never changed_ — only our ability to detect it did.

---

## 10. Demo 6 — polynomial terms: is the curvature real?

When you add `x²` to a model, its p-value tells you whether the bend in the data is a real pattern or just noise.

### Code block 8 — Demo 6: p-values for polynomial terms

```python
# Code block 8: Demo 6 - polynomial terms

def demo6_polynomial():
    """Show that the x^2 term's p-value reveals whether curvature is real."""
    banner("Demo 6 - Polynomial terms: is the curvature real?")

    rng = np.random.default_rng(5)
    n = 150
    x = rng.uniform(-3, 3, size=n)           # predictor spread over [-3, 3]
    y = 1 + 2 * x - 0.6 * x**2 + rng.normal(scale=1.2, size=n)  # TRUE curve

    print(">>> Linear model (x only):")
    lin = fit_ols_table(add_constant(x), y, ["intercept", "x"])
    print(lin.round(4).to_string())

    x2 = x ** 2                              # quadratic term
    quad = fit_ols_table(np.column_stack([np.ones(n), x, x2]), y,
                         ["intercept", "x", "x_squared"])
    print("\n>>> Quadratic model (x + x^2):")
    print(quad.round(4).to_string())
    print("\nThe p-value of x_squared is the key number:")
    print("p < 0.05 -> the bend is real, keep the quadratic term.")

    grid = np.linspace(-3, 3, 200)           # dense grid for smooth curves
    plt.figure()
    plt.scatter(x, y, alpha=0.5, s=25, label="data")
    # straight line from the linear model
    plt.plot(grid,
             lin.loc["intercept", "coef"] + lin.loc["x", "coef"] * grid,
             color="orange", lw=2, label="linear fit")
    # parabola from the quadratic model
    b0 = quad.loc["intercept", "coef"]
    b1 = quad.loc["x", "coef"]
    b2 = quad.loc["x_squared", "coef"]
    plt.plot(grid, b0 + b1 * grid + b2 * grid**2, color="blue", lw=2,
             label=f"quadratic fit (p(x^2) = {quad.loc['x_squared', 'p_value']:.4f})")
    plt.xlabel("x"); plt.ylabel("y")
    plt.title("A straight line misses the curve - the x^2 p-value tells you")
    plt.legend()
    plt.savefig("plots/polynomial_pvalues.png", dpi=130, bbox_inches="tight")
    plt.show()
```

**What you should see:** in the linear fit, `x` looks significant but the fit is visibly bad. In the quadratic fit, `x_squared` has p ≈ 10⁻⁹ — overwhelming evidence the curvature is real. **Pitfall:** in the linear-only model the residuals would show a U-shape — always check residual plots, not just p-values.

---

## 11. Demo 7 — multicollinearity: when twins confuse the model

If two predictors are almost the same (e.g., `income` and `income_tax`), the model cannot decide who deserves the credit. Standard errors explode, t-values shrink, and p-values rise — even for a feature that truly matters.

### Code block 9 — Demo 7: multicollinearity

```python
# Code block 9: Demo 7 - multicollinearity

def demo7_multicollinearity():
    """Correlated predictors inflate standard errors and therefore p-values."""
    banner("Demo 7 - Multicollinearity: p-values when predictors are twins")

    rng = np.random.default_rng(7)
    n = 150
    x1 = rng.normal(size=n)                          # first predictor
    x2 = x1 + rng.normal(scale=0.25, size=n)         # x2 = x1 + tiny noise
    y = 1.5 * x1 + rng.normal(scale=1.5, size=n)     # only x1 truly matters
    print(f"correlation(x1, x2) = {np.corrcoef(x1, x2)[0, 1]:.3f}")

    alone = fit_ols_table(add_constant(x1), y, ["intercept", "x1"])
    together = fit_ols_table(np.column_stack([np.ones(n), x1, x2]), y,
                             ["intercept", "x1", "x2"])

    print("\n>>> x1 ALONE:")
    print(alone.round(4).to_string())
    print("\n>>> x1 and its twin x2 TOGETHER:")
    print(together.round(4).to_string())
    print("\nx1 still matters, but its standard error jumps (the model cannot")
    print("decide which twin deserves the credit) -> p(x1) rises.")

    plt.figure()
    labels = ["x1 alone", "x1 (with twin)", "x2 (twin)"]
    p_vals = [alone.loc["x1", "p_value"],
              together.loc["x1", "p_value"],
              together.loc["x2", "p_value"]]
    plt.bar(labels, p_vals, color=["green", "orange", "orange"])
    plt.axhline(0.05, color="red", ls="--", lw=2, label="alpha = 0.05")
    plt.yscale("log")
    plt.ylabel("p-value (log scale)")
    plt.title("Adding a correlated twin inflates p-values")
    plt.legend()
    plt.savefig("plots/multicollinearity_pvalues.png", dpi=130, bbox_inches="tight")
    plt.show()
```

**What you should see:** x1's t drops from ~12 to ~3 and its p jumps from ~10⁻²⁵ to ~0.003, _even though x1 is the only feature that truly matters_. With even tighter correlation, the effect can vanish entirely. **Rule of thumb:** if two features have correlation > 0.9, combine or drop one (or use regularization like Ridge/Lasso).

---

## 12. Demo 8 — the p-hacking warning

Generate 100 _pure-noise_ features and regress y (also pure noise) on all of them. There is **no signal anywhere** — yet about 5 features will still get p < 0.05. That is α = 0.05 doing exactly what it promises: a 5% false-positive rate.

### Code block 10 — Demo 8: noise features

```python
# Code block 10: Demo 8 - noise features and false positives

def demo8_noise_features():
    """Test 100 pure-noise features: ~5 will look significant by pure chance."""
    banner("Demo 8 - P-hacking warning: noise features waving flags")

    rng = np.random.default_rng(123)
    n, m = 200, 100                          # 200 rows, 100 noise features
    X_noise = rng.normal(size=(n, m))        # every feature is pure noise
    y = rng.normal(size=n)                   # outcome is pure noise too

    names = ["intercept"] + [f"noise_{i+1}" for i in range(m)]
    table = fit_ols_table(np.column_stack([np.ones(n), X_noise]), y, names)

    p_vals = table.loc[[nm for nm in names if nm != "intercept"], "p_value"]
    flagged = p_vals[p_vals < 0.05]          # features that 'passed' by chance
    print(f"Tested {m} pure-noise features: {len(flagged)} had p < 0.05 by chance")
    print(f"(expected about {0.05 * m:.0f} with alpha = 0.05)\n")
    print("Flagged features (false positives):")
    print(flagged.round(4).to_string() if len(flagged) else "none")

    plt.figure()
    plt.hist(p_vals, bins=20, color="steelblue", edgecolor="white")
    plt.axvline(0.05, color="red", ls="--", lw=2, label="alpha = 0.05")
    plt.xlabel("p-value of noise features")
    plt.ylabel("number of features")
    plt.title("p-values of pure-noise features are roughly uniform - ~5% < 0.05")
    plt.legend()
    plt.savefig("plots/noise_pvalue_histogram.png", dpi=130, bbox_inches="tight")
    plt.show()
```

**What you should see:** the histogram is roughly flat (uniform p-values under the null), and ~5 of 100 bars fall left of the red line. **This is why you should never test 500 features and keep only the "significant" ones without multiple-testing corrections** (Bonferroni, Benjamini–Hochberg/FDR) or proper cross-validation.

---

## 13. Demo 9 — real data: diabetes progression

Finally, a real (but offline) dataset: 442 patients, 10 clinical features, target = disease progression. We fit all 10 features and read the p-values.

### Code block 11 — Demo 9: real sklearn dataset

```python
# Code block 11: Demo 9 - real dataset (bundled with scikit-learn)

def demo9_diabetes():
    """Fit a 10-feature regression on the diabetes dataset and read p-values."""
    banner("Demo 9 - Real data: diabetes progression (sklearn, offline)")

    data = load_diabetes()                   # bundled dataset, no download
    X, y = data.data, data.target            # features and target
    names = ["intercept"] + list(data.feature_names)   # column names
    design = add_constant(X)                 # add intercept column
    print(f"n = {len(y)} patients, {len(data.feature_names)} clinical features\n")

    print_statsmodels(design, y, names)      # full statsmodels summary (if available)
    table = fit_ols_table(design, y, names)  # manual table (always available)
    print("\n>>> Manual table (same p-values):")
    print(table.round(4).to_string())

    sig = table[table["p_value"] < 0.05]     # rows that are significant
    print("\nFeatures with p < 0.05:", ", ".join(sig.index.tolist()))
    print("These predictors carry real signal *in this sample*.")
```

**What you should see:** on this dataset the strongly significant predictors are typically `bmi`, `bp` and `s5` (p ≪ 0.05), while several others (e.g., `age`, `sex`, `s3`) show p ≥ 0.05 — candidates for removal or further investigation. Notice how in the statsmodels summary the same information appears as the `P>|t|` column plus stars.

---

## 14. How to read a statsmodels `P>|t|` column

A typical summary row looks like:

```
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
bmi            0.3242      0.065      5.007      0.000       0.197       0.452
age           -0.0100      0.059     -0.170      0.865      -0.127       0.106
==============================================================================
```

Column by column:

| Column          | Meaning                                     | Our example                                                           |
| --------------- | ------------------------------------------- | --------------------------------------------------------------------- |
| `coef`          | estimated slope β̂                           | 0.324 (each +1 unit of bmi adds ~0.32 to progression)                 |
| `std err`       | uncertainty of the estimate (SE)            | 0.065                                                                 |
| `t`             | `coef / std err` = signal/noise             | 0.324/0.065 ≈ 5.0                                                     |
| `P>\|t\|`       | two-tailed p-value                          | 0.000 → < 0.001 → `***`                                               |
| `[0.025 0.975]` | 95% confidence interval for the coefficient | (0.197, 0.452) — does **not** contain 0, consistent with rejecting H₀ |

Also watch the top of the summary:

- **`Prob (F-statistic)`** — p-value for the _whole model_ (H₀: all coefficients = 0). If it's tiny, the model as a whole beats an intercept-only baseline.
- **`R-squared` / `Adj. R-squared`** — how much variance the model explains. Not a p-value; report it alongside.

---

## 15. Business / company use cases

1. **Marketing attribution.** "Does TV spend significantly predict revenue?" Fit `revenue ~ tv_spend + digital_spend`; if the TV coefficient has p < 0.05, the channel earns its budget. If p = 0.4, the "lift" you saw is within the range of pure luck.
2. **Credit scoring & model governance.** Regulators (e.g., model-risk management) expect documented justification for every variable. Significant coefficients + sensible signs = defensible, explainable models.
3. **Pricing analytics.** "Does the discount rate significantly affect revenue?" The discount coefficient's p-value tells you whether the observed effect is real before you roll out a company-wide promotion.
4. **Churn & retention.** With 50 candidate features, p-values (plus cross-validation) help you shortlist the ones that genuinely predict churn — saving engineering time and keeping the model simple.
5. **A/B testing.** A regression `conversion ~ treatment_dummy + controls` gives the _same_ p-value as a classic t-test, but with covariate adjustment (smaller SE = more power). Companies report p + confidence interval + effect size together.
6. **Healthcare / pharma.** "Does dosage significantly affect the outcome?" p < 0.05 is part of regulatory evidence — but so is effect size. A statistically significant 0.1% improvement may be practically worthless.

---

## 16. Common mistakes and a best-practice checklist

| ❌ Mistake                                         | ✅ Do this instead                                                                                   |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| "p = 0.04 means 96% chance the effect is real"     | p is **not** a probability about the coefficient; it's a probability about the data under H₀         |
| "p = 0.08 means there is no effect"                | Absence of evidence ≠ evidence of absence; maybe the sample is too small (Demo 5)                    |
| Remove every feature with p ≥ 0.05, re-fit, repeat | Stepwise p-value selection overfits; use cross-validation or regularization; prefer domain knowledge |
| Run 100 tests, report the 5 winners                | Correct for multiple testing (Bonferroni / FDR) or use held-out validation (Demo 8)                  |
| Ignore correlated features                         | Check correlations / VIF — multicollinearity inflates p-values (Demo 7)                              |
| Trust p-values with tiny samples                   | Report confidence intervals and power; small n → unstable p-values                                   |
| Treat p < 0.05 as "important"                      | Report effect size + CI; with huge n, trivial effects are "significant" (Demo 5)                     |
| Forget the model assumptions                       | p-values assume roughly normal errors; check residuals (Q-Q plot, residual vs fitted)                |

---

## 17. TL;DR — what to remember

1. **p-value = P(data this extreme | coefficient truly 0)** — evidence _against_ the "no effect" story.
2. **p < 0.05** → statistically significant → reject H₀ → the feature shows a real effect (in this sample, at α = 0.05).
3. **p ≥ 0.05** → not enough evidence → _fail to reject_ — that is **not** proof of no effect.
4. The machinery: `t = coef / SE`, and `p = 2·(1 − T_{df}(|t|))` — just a shaded area under a t-curve.
5. Big n → small p (Demo 5); correlated features → big p (Demo 7); many tests → fake p (Demo 8).
6. **Always pair the p-value with the effect size and confidence interval** — significance is not importance.

Now go run `understanding_pvalues.py` and see all of this with your own data!
