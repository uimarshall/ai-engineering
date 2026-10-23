# =============================================================================
# understanding_pvalues.py
# Understanding p-values in Linear Regression (Practical) - companion script
#
# Run:  python understanding_pvalues.py
#
# Every figure is saved to ./plots/ BEFORE it is shown (plt.savefig then plt.show).
# Data is offline-safe: synthetic generators + sklearn's bundled diabetes dataset.
# =============================================================================

# -----------------------------------------------------------------------------
# Code block 1: imports and global configuration
# -----------------------------------------------------------------------------
import os  # for creating the plots folder
from importlib import import_module
from typing import Any, cast

import matplotlib.pyplot as plt  # plotting
import numpy as np  # numerical arrays
import pandas as pd  # tables (DataFrames)
from scipy import stats  # t-distribution -> p-values
from sklearn.datasets import load_diabetes  # bundled, offline-safe real data
from sklearn.utils import Bunch

sm: Any = None
try:  # statsmodels = classic summary tables
    sm = import_module("statsmodels.api")

    HAS_SM = True
except ImportError:  # optional: script still works without it
    HAS_SM = False
    print("tip: 'pip install statsmodels' gives you the classic OLS summary table.\n")

np.set_printoptions(suppress=True, precision=4)  # cleaner console output
pd.set_option("display.float_format", lambda v: f"{v:.4f}")  # tidy tables

os.makedirs("plots", exist_ok=True)  # make sure ./plots exists
plt.rcParams["figure.figsize"] = (10, 6)  # default figure size
plt.rcParams["axes.grid"] = True  # grid on every plot


# -----------------------------------------------------------------------------
# Code block 2: helper functions (they implement the formulas from the tutorial)
# -----------------------------------------------------------------------------


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
    n, k = X_design.shape  # k = intercept + number of predictors
    beta = np.linalg.lstsq(X_design, y, rcond=None)[0]  # solve normal equations
    resid = y - X_design @ beta  # residuals = what the model missed
    df_resid = n - k  # degrees of freedom left after fitting
    mse = resid @ resid / df_resid  # unbiased estimate of error variance
    cov = mse * np.linalg.inv(X_design.T @ X_design)  # covariance of coefficients
    se = np.sqrt(np.diag(cov))  # standard errors = sqrt of diagonal
    t = beta / se  # t-statistic for each coefficient
    p = 2 * (1 - stats.t.cdf(np.abs(t), df=df_resid))  # two-tailed p-value

    table = pd.DataFrame(
        {"coef": beta, "std_err": se, "t": t, "p_value": p}, index=names
    )  # one row per coefficient
    table["sig"] = [stars(pv) for pv in p]  # add the * markers
    return table


def print_statsmodels(X_design, y, names):
    """Print the classic statsmodels summary if the package is available."""
    if not HAS_SM:  # fallback if statsmodels missing
        print("(statsmodels not installed -> showing the manual table instead)")
        return
    X_df = pd.DataFrame(X_design, columns=names)  # give columns readable names
    print(sm.OLS(y, X_df).fit().summary())  # the famous regression summary


def banner(title):
    """Print a section banner so demo output is easy to follow."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# -----------------------------------------------------------------------------
# Code block 3: Demo 1 - regression with known ground truth
# -----------------------------------------------------------------------------


def demo1_known_truth():
    """Fit OLS where the REAL coefficients are known, then interpret p-values."""
    banner("Demo 1 - Regression with known ground truth")

    rng = np.random.default_rng(42)  # fixed seed -> reproducible results
    n = 200  # 200 rows of data
    X = rng.normal(size=(n, 4))  # 4 standardised predictor columns
    true_coefs = np.array([0.0, 2.5, 0.0, -1.8])  # ONLY features 2 and 4 matter
    y = X @ true_coefs + rng.normal(scale=2.0, size=n)  # y = truth + noise

    names = ["intercept", "feature_1", "feature_2", "feature_3", "feature_4"]
    design = add_constant(X)  # prepend the intercept column

    print("True coefficients:", true_coefs)
    print("(only feature_2 and feature_4 truly affect y)\n")

    print(">>> statsmodels summary (the classic output):")
    print_statsmodels(design, y, names)  # full summary with P>|t| column

    print(">>> Same numbers computed by hand (for comparison):")
    table = fit_ols_table(design, y, names)  # our own OLS + p-values
    print(table.round(4).to_string())  # print the table

    print("\nHow to read this:")
    print(" - feature_2: coef ~ 2.5, huge t, p << 0.05   -> real effect.")
    print(" - feature_4: coef ~ -1.8, huge |t|, p << 0.05 -> real effect.")
    print(" - feature_1 / feature_3: true coefficient is 0.0 -> p is usually > 0.05,")
    print("   but by pure chance it will be < 0.05 about 5% of the time (Demo 8).")
    return table  # reuse the table in other demos if needed


# -----------------------------------------------------------------------------
# Code block 4: Demo 2 - the p-value as a shaded area under the t-distribution
# -----------------------------------------------------------------------------


def demo2_ttest_visual():
    """Draw the t-distribution and shade the two tails that define the p-value."""
    banner("Demo 2 - What the p-value actually IS (a shaded area)")

    df = 195  # 200 rows - 5 fitted coefficients
    t_obs = 2.1  # a moderate, realistic t-statistic
    p_value = 2 * (1 - stats.t.cdf(t_obs, df))  # two-tailed p-value formula
    print(f"For t = {t_obs} with df = {df}:  p-value = {p_value:.4f}")
    print("Interpretation: if the true coefficient were 0, a t this extreme")
    print(f"would occur by chance only {p_value * 100:.2f}% of the time.\n")

    t_grid = np.linspace(-6, 6, 800)  # smooth range of t values
    pdf = stats.t.pdf(t_grid, df)  # height of the t-curve at each t
    plt.figure()
    plt.plot(t_grid, pdf, lw=2, color="black", label=f"t-distribution (df={df})")

    left = t_grid <= -t_obs  # far-left tail (beyond -2.1)
    right = t_grid >= t_obs  # far-right tail (beyond +2.1)
    plt.fill_between(
        t_grid, pdf, where=left, color="red", alpha=0.6, label="p-value area"
    )
    plt.fill_between(t_grid, pdf, where=right, color="red", alpha=0.6)
    plt.axvline(t_obs, color="blue", ls="--", label=f"observed t = {t_obs}")
    plt.axvline(-t_obs, color="blue", ls="--")
    plt.title(f"Two-tailed p-value = shaded area = {p_value:.4f}")
    plt.xlabel("t")
    plt.ylabel("probability density")
    plt.legend()
    plt.savefig("plots/pvalue_t_distribution.png", dpi=130, bbox_inches="tight")
    plt.show()  # saved BEFORE showing

    # Reality check: the strong feature from Demo 1 has a much bigger t
    rng = np.random.default_rng(42)  # rebuild the same dataset
    X = rng.normal(size=(200, 4))
    y = X @ np.array([0.0, 2.5, 0.0, -1.8]) + rng.normal(scale=2.0, size=200)
    table = fit_ols_table(add_constant(X), y, ["intercept", "f1", "f2", "f3", "f4"])
    t_real = table.loc["f2", "t"]  # t of the strong feature
    p_real = table.loc["f2", "p_value"]  # its (tiny) p-value
    print(f"(Real example: feature_2 has t = {t_real:.2f} and p = {p_real:.3g} -")
    print(" that tiny p is an invisible sliver of shaded area!)")


# -----------------------------------------------------------------------------
# Code block 5: Demo 3 - bar chart of p-values vs alpha = 0.05
# -----------------------------------------------------------------------------


def demo3_pvalue_barchart():
    """Plot every coefficient's p-value with the alpha = 0.05 threshold line."""
    banner("Demo 3 - Bar chart of p-values for every coefficient")

    rng = np.random.default_rng(42)  # same data as Demo 1
    X = rng.normal(size=(200, 4))
    y = X @ np.array([0.0, 2.5, 0.0, -1.8]) + rng.normal(scale=2.0, size=200)
    names = ["intercept", "feature_1", "feature_2", "feature_3", "feature_4"]
    table = fit_ols_table(add_constant(X), y, names)  # fit + p-values

    feats = ["feature_1", "feature_2", "feature_3", "feature_4"]
    p_vals = table.loc[feats, "p_value"].to_numpy(dtype=float)  # p-values only

    plt.figure()
    colors = ["green" if p < 0.05 else "gray" for p in p_vals]  # colour by verdict
    plt.bar(feats, p_vals, color=colors)
    plt.axhline(0.05, color="red", ls="--", lw=2, label="alpha = 0.05")
    plt.yscale("log")  # p-values span orders of magnitude
    plt.ylabel("p-value (log scale)")
    plt.title("Coefficient p-values: green = significant (p < 0.05)")
    plt.legend()
    plt.savefig("plots/feature_pvalues.png", dpi=130, bbox_inches="tight")
    plt.show()
    print("feature_2 and feature_4 are green (real effects);")
    print("feature_1 and feature_3 are gray (their true coefficient is 0.0).")


# -----------------------------------------------------------------------------
# Code block 6: Demo 4 - the t <-> p relationship
# -----------------------------------------------------------------------------


def demo4_t_to_p_curve():
    """Show that bigger |t| always means smaller p (for a fixed df)."""
    banner("Demo 4 - Bigger |t| means smaller p")

    df = 195  # degrees of freedom used everywhere here
    t_grid = np.linspace(0, 5, 200)  # |t| from 0 to 5
    p_grid = 2 * (1 - stats.t.cdf(t_grid, df))  # two-tailed p for each t
    t_crit = float(stats.t.ppf(0.975, df))  # the t where p crosses 0.05
    print(f"The p-value hits 0.05 exactly when |t| = {t_crit:.3f} (df = {df})")
    print("=> |t| > 1.97 means p < 0.05 for this df.\n")

    plt.figure()
    plt.plot(t_grid, p_grid, lw=2, color="purple", label="p-value")
    plt.axhline(0.05, color="red", ls="--", lw=2, label="p = 0.05")
    plt.axvline(t_crit, color="orange", ls=":", lw=2, label=f"|t| = {t_crit:.2f}")
    plt.yscale("log")  # p is tiny for large t
    plt.xlabel("|t| statistic")
    plt.ylabel("p-value (log scale)")
    plt.title("p-value shrinks as |t| grows: t large -> strong evidence")
    plt.legend()
    plt.savefig("plots/t_to_p_curve.png", dpi=130, bbox_inches="tight")
    plt.show()


# -----------------------------------------------------------------------------
# Code block 7: Demo 5 - sample size: statistical vs practical significance
# -----------------------------------------------------------------------------


def demo5_sample_size():
    """Keep the effect fixed (slope = 0.3) and watch p shrink as n grows."""
    banner("Demo 5 - Sample size effect: same effect, different p-value")

    n_values = [20, 30, 50, 75, 100, 150, 200, 300, 500, 800, 1200]
    rows = []
    for n in n_values:  # loop over sample sizes
        rng = np.random.default_rng(n)  # different seed per n (reproducible)
        x = rng.normal(size=n)  # one predictor
        y = 0.3 * x + rng.normal(size=n)  # SMALL but REAL effect: slope 0.3
        t = fit_ols_table(add_constant(x), y, ["intercept", "x"])
        rows.append(
            (
                n,
                t.loc["x", "coef"],  # estimated slope (stays ~0.3)
                t.loc["x", "std_err"],  # uncertainty (shrinks with n)
                t.loc["x", "t"],  # t = coef / SE (grows)
                t.loc["x", "p_value"],
            )
        )  # p (shrinks)

    df = pd.DataFrame(rows, columns=["n", "coef", "std_err", "t", "p_value"])
    print(df.round(4).to_string(index=False))
    print("\nThe coefficient stays around 0.3 (the effect did NOT get bigger) -")
    print("only the standard error shrinks, so t grows and p drops.")

    plt.figure()
    plt.plot(df["n"], df["p_value"], marker="o", color="teal", label="p-value")
    plt.axhline(0.05, color="red", ls="--", lw=2, label="alpha = 0.05")
    plt.xscale("log")  # spread the n values out
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


# -----------------------------------------------------------------------------
# Code block 8: Demo 6 - polynomial terms: is the curvature real?
# -----------------------------------------------------------------------------


def demo6_polynomial():
    """Show that the x^2 term's p-value reveals whether curvature is real."""
    banner("Demo 6 - Polynomial terms: is the curvature real?")

    rng = np.random.default_rng(5)
    n = 150
    x = rng.uniform(-3, 3, size=n)  # predictor spread over [-3, 3]
    y = 1 + 2 * x - 0.6 * x**2 + rng.normal(scale=1.2, size=n)  # TRUE curve

    print(">>> Linear model (x only):")
    lin = fit_ols_table(add_constant(x), y, ["intercept", "x"])
    print(lin.round(4).to_string())

    x2 = x**2  # quadratic term
    quad = fit_ols_table(
        np.column_stack([np.ones(n), x, x2]), y, ["intercept", "x", "x_squared"]
    )
    print("\n>>> Quadratic model (x + x^2):")
    print(quad.round(4).to_string())
    print("\nThe p-value of x_squared is the key number:")
    print("p < 0.05 -> the bend is real, keep the quadratic term.")

    grid = np.linspace(-3, 3, 200)  # dense grid for smooth curves
    plt.figure()
    plt.scatter(x, y, alpha=0.5, s=25, label="data")
    lin_coefs = lin["coef"].to_numpy(dtype=float)
    # straight line from the linear model
    plt.plot(
        grid,
        lin_coefs[0] + lin_coefs[1] * grid,
        color="orange",
        lw=2,
        label="linear fit",
    )
    # parabola from the quadratic model
    quad_coefs = quad["coef"].to_numpy(dtype=float)
    b0, b1, b2 = quad_coefs
    plt.plot(
        grid,
        b0 + b1 * grid + b2 * grid**2,
        color="blue",
        lw=2,
        label=f"quadratic fit (p(x^2) = {quad.loc['x_squared', 'p_value']:.4f})",
    )
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("A straight line misses the curve - the x^2 p-value tells you")
    plt.legend()
    plt.savefig("plots/polynomial_pvalues.png", dpi=130, bbox_inches="tight")
    plt.show()


# -----------------------------------------------------------------------------
# Code block 9: Demo 7 - multicollinearity
# -----------------------------------------------------------------------------


def demo7_multicollinearity():
    """Correlated predictors inflate standard errors and therefore p-values."""
    banner("Demo 7 - Multicollinearity: p-values when predictors are twins")

    rng = np.random.default_rng(7)
    n = 150
    x1 = rng.normal(size=n)  # first predictor
    x2 = x1 + rng.normal(scale=0.25, size=n)  # x2 = x1 + tiny noise
    y = 1.5 * x1 + rng.normal(scale=1.5, size=n)  # only x1 truly matters
    print(f"correlation(x1, x2) = {np.corrcoef(x1, x2)[0, 1]:.3f}")

    alone = fit_ols_table(add_constant(x1), y, ["intercept", "x1"])
    together = fit_ols_table(
        np.column_stack([np.ones(n), x1, x2]), y, ["intercept", "x1", "x2"]
    )

    print("\n>>> x1 ALONE:")
    print(alone.round(4).to_string())
    print("\n>>> x1 and its twin x2 TOGETHER:")
    print(together.round(4).to_string())
    print("\nx1 still matters, but its standard error jumps (the model cannot")
    print("decide which twin deserves the credit) -> p(x1) rises.")

    plt.figure()
    labels = ["x1 alone", "x1 (with twin)", "x2 (twin)"]
    p_vals = np.array(
        [
            alone.loc["x1", "p_value"],
            together.loc["x1", "p_value"],
            together.loc["x2", "p_value"],
        ],
        dtype=float,
    )
    plt.bar(labels, p_vals, color=["green", "orange", "orange"])
    plt.axhline(0.05, color="red", ls="--", lw=2, label="alpha = 0.05")
    plt.yscale("log")
    plt.ylabel("p-value (log scale)")
    plt.title("Adding a correlated twin inflates p-values")
    plt.legend()
    plt.savefig("plots/multicollinearity_pvalues.png", dpi=130, bbox_inches="tight")
    plt.show()


# -----------------------------------------------------------------------------
# Code block 10: Demo 8 - noise features and false positives (p-hacking warning)
# -----------------------------------------------------------------------------


def demo8_noise_features():
    """Test 100 pure-noise features: ~5 will look significant by pure chance."""
    banner("Demo 8 - P-hacking warning: noise features waving flags")

    rng = np.random.default_rng(123)
    n, m = 200, 100  # 200 rows, 100 noise features
    X_noise = rng.normal(size=(n, m))  # every feature is pure noise
    y = rng.normal(size=n)  # outcome is pure noise too

    names = ["intercept"] + [f"noise_{i+1}" for i in range(m)]
    table = fit_ols_table(np.column_stack([np.ones(n), X_noise]), y, names)

    p_vals = table.loc[[nm for nm in names if nm != "intercept"], "p_value"]
    flagged = p_vals[p_vals < 0.05]  # features that 'passed' by chance
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


# -----------------------------------------------------------------------------
# Code block 11: Demo 9 - real sklearn dataset (diabetes, bundled offline)
# -----------------------------------------------------------------------------


def demo9_diabetes():
    """Fit a 10-feature regression on the diabetes dataset and read p-values."""
    banner("Demo 9 - Real data: diabetes progression (sklearn, offline)")

    data = cast(Bunch, load_diabetes(return_X_y=False))  # bundled dataset, no download
    X, y = data.data, data.target  # features and target
    names = ["intercept"] + list(data.feature_names)  # column names
    design = add_constant(X)  # add intercept column
    print(f"n = {len(y)} patients, {len(data.feature_names)} clinical features\n")

    print_statsmodels(design, y, names)  # full statsmodels summary (if available)
    table = fit_ols_table(design, y, names)  # manual table (always available)
    print("\n>>> Manual table (same p-values):")
    print(table.round(4).to_string())

    sig = table[table["p_value"] < 0.05]  # rows that are significant
    print("\nFeatures with p < 0.05:", ", ".join(sig.index.tolist()))
    print("These predictors carry real signal *in this sample*.")


# -----------------------------------------------------------------------------
# Code block 12: main driver - run every demo in order
# -----------------------------------------------------------------------------


def main():
    """Run every demo; each figure lands in ./plots/ before it pops up."""
    print("Understanding p-values in Linear Regression - practical demos")
    demo1_known_truth()  # fit on known truth, compare statsmodels vs manual
    demo2_ttest_visual()  # draw the p-value as shaded tails of a t-curve
    demo3_pvalue_barchart()  # bar chart: which p-values beat alpha = 0.05
    demo4_t_to_p_curve()  # the t <-> p relationship
    demo5_sample_size()  # same effect, bigger n -> smaller p
    demo6_polynomial()  # is the x^2 curvature real? ask its p-value
    demo7_multicollinearity()  # correlated twins inflate p-values
    demo8_noise_features()  # ~5% of noise features look significant by chance
    demo9_diabetes()  # real dataset: which clinical features matter?
    print("\nAll figures have been saved to ./plots/  ")


if __name__ == "__main__":
    main()
