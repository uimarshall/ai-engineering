"""
=====================================================================
 Tutorial: Evaluating model fit using R-squared (R^2) -- PRACTICAL
=====================================================================

This script accompanies the markdown tutorial "Evaluating Model Fit
with R-squared". Each EXAMPLE below matches a section of the tutorial.

Contents
--------
1. Your first R^2: simple linear regression
2. Computing R^2 by hand from the formula
3. Multiple regression + adjusted R^2
4. Where R^2 misleads you: overfitting
5. What a NEGATIVE R^2 means
6. R^2 alongside MAE and RMSE

How to run
----------
    pip install numpy matplotlib scikit-learn
    python evaluating_r_squared.py

All data is synthetic (generated inside this script), so nothing
needs to be downloaded. Figures are saved as PNG files in the folder
you run the script from.
"""

import matplotlib.pyplot as plt  # simple plotting

# ----------------------------------------------------------------------
# Imports: the tools we need from the standard Python ML stack
# ----------------------------------------------------------------------
import numpy as np  # numerical computing (arrays, math)
from sklearn.linear_model import LinearRegression  # the regression model
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split  # train/test splitting
from sklearn.preprocessing import PolynomialFeatures  # build x, x^2, x^3, ...

np.random.seed(42)  # fix the random "seed" so the random numbers are the
# SAME every run -> results you can reproduce and discuss

# ======================================================================
# EXAMPLE 1 - Your first R^2: simple linear regression
# ======================================================================
print("=" * 60)
print("EXAMPLE 1: Simple linear regression")
print("=" * 60)

# Create fake data with a KNOWN true relationship:  y = 5 + 3x + noise
X = np.random.rand(100, 1) * 10  # 100 samples, 1 feature, values 0-10
y = 5 + 3 * X.ravel() + np.random.randn(100) * 3  # true line + random noise (std 3)

# Split the data: 80% to LEARN from, 20% to TEST on (kept hidden from training)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

model = LinearRegression()  # create a linear regression model
model.fit(X_train, y_train)  # "fit" = find the best line through the train points

print(
    "True slope was 3.0,     model learned:",
    round(float(np.asarray(model.coef_).flat[0]), 3),
)
print(
    "True intercept was 5.0,   model learned:",
    round(float(np.asarray(model.intercept_).item()), 3),
)

r2_train = model.score(X_train, y_train)  # R^2 on data the model has seen
r2_test = r2_score(y_test, model.predict(X_test))  # R^2 on UNSEEN data

print(f"R^2 on training data: {r2_train:.3f}")
print(f"R^2 on test data:     {r2_test:.3f}")
print(
    "-> Interpretation: about "
    f"{r2_test:.0%} of the variation in y is explained by our model on new data."
)
print(
    "   The remaining {0:.0%} is still 'unexplained' (mostly noise).".format(
        1 - r2_test
    )
)

# ======================================================================
# EXAMPLE 2 - Computing R^2 BY HAND (understand what it really is)
# ======================================================================
print("=" * 60)
print("EXAMPLE 2: Computing R^2 by hand")
print("=" * 60)

y_pred = model.predict(X_test)  # model guesses for the test set

ss_res = np.sum((y_test - y_pred) ** 2)  # SS_res: sum of squared ERRORS
#         (what the model got wrong)
ss_tot = np.sum((y_test - y_test.mean()) ** 2)  # SS_tot: TOTAL variation of y
#         around its own mean

r2_by_hand = 1 - ss_res / ss_tot  # the definition of R^2:
# 1 - (unexplained variation / total variation)

print(f"SS_res (unexplained) = {ss_res:.2f}")
print(f"SS_tot (total)       = {ss_tot:.2f}")
print(f"R^2 by hand          = {r2_by_hand:.3f}")
print(f"R^2 from sklearn     = {r2_score(y_test, y_pred):.3f}   (same thing!)")

# ======================================================================
# EXAMPLE 3 - Multiple regression + ADJUSTED R^2
# ======================================================================
print("=" * 60)
print("EXAMPLE 3: Multiple regression + adjusted R^2")
print("=" * 60)

n = 200  # number of samples (rows)
X_multi = np.random.rand(n, 5) * 10  # 5 features; only the first 3 truly matter
y_multi = (
    4
    + 2.0 * X_multi[:, 0]  # feature 0 pushes y up
    - 1.5 * X_multi[:, 1]  # feature 1 pushes y down
    + 0.5 * X_multi[:, 2]  # feature 2 pushes y up a little
    + np.random.randn(n) * 5
)  # random noise + features 3,4 are USELESS

Xm_train, Xm_test, ym_train, ym_test = train_test_split(
    X_multi, y_multi, test_size=0.25, random_state=1
)


def adjusted_r2(r2, n_samples, n_features):
    """Penalise R^2 for every extra predictor the model uses."""
    return 1 - (1 - r2) * (n_samples - 1) / (n_samples - n_features - 1)


# FULL model: throws in all 5 features (2 of them are useless junk)
full = LinearRegression().fit(Xm_train, ym_train)  # fit on train...
r2_full = full.score(Xm_test, ym_test)  # ...evaluate on test

# SMALL model: keeps only the 3 features that really matter
small = LinearRegression().fit(Xm_train[:, :3], ym_train)  # [:, :3] = first 3 columns
r2_small = small.score(Xm_test[:, :3], ym_test)

n_test = len(ym_test)  # number of test samples (needed by the formula)
print(
    f"5-feature model: R^2 = {r2_full:.3f} "
    f"-> adjusted R^2 = {adjusted_r2(r2_full, n_test, 5):.3f}"
)
print(
    f"3-feature model: R^2 = {r2_small:.3f} "
    f"-> adjusted R^2 = {adjusted_r2(r2_small, n_test, 3):.3f}"
)
print("-> Plain R^2 barely changed, but adjusted R^2 REWARDS the simpler model.")
print("   Use adjusted R^2 when comparing models with different numbers of features.")

# ======================================================================
# EXAMPLE 4 - Where R^2 MISLEADS you: overfitting
# ======================================================================
print("=" * 60)
print("EXAMPLE 4: Where R^2 misleads - overfitting")
print("=" * 60)

# Fresh dataset: only 30 samples, so a very flexible curve has enough
# freedom to "hug" the training points instead of finding the true line
np.random.seed(10)  # seed chosen so this demo is dramatic
Xof = np.random.rand(30, 1) * 10  # 30 samples, feature 0-10
yof = 5 + 3 * Xof.ravel() + np.random.randn(30) * 2.0  # true line y = 5 + 3x + noise
Xof_train, Xof_test, yof_train, yof_test = train_test_split(
    Xof, yof, test_size=0.25, random_state=1
)

print(f"{'degree':>8} {'R^2 train':>10} {'R^2 test':>10}")
for degree in [1, 2, 5, 15]:
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    Xtr_p = poly.fit_transform(Xof_train)  # expand x into x, x^2, ..., x^degree
    Xte_p = poly.transform(Xof_test)  # apply the SAME expansion to test data
    m = LinearRegression().fit(Xtr_p, yof_train)
    # model.score() for regression models returns exactly R^2
    print(
        f"{degree:>8} {m.score(Xtr_p, yof_train):>10.3f} {m.score(Xte_p, yof_test):>10.3f}"
    )
print("-> Training R^2 rises (0.98 -> 0.985) while test R^2 COLLAPSES to ~0.5.")
print("   A high R^2 on TRAINING data alone proves nothing!")

# Draw the degree-15 curve so you can SEE the overfitting
poly15 = PolynomialFeatures(degree=15, include_bias=False)
m15 = LinearRegression().fit(poly15.fit_transform(Xof_train), yof_train)
x_grid = np.linspace(0, 10, 300).reshape(-1, 1)  # dense x-grid for a smooth curve
y_grid = m15.predict(poly15.transform(x_grid))  # curve predictions on that grid

r2_tr15 = m15.score(poly15.transform(Xof_train), yof_train)  # R^2 on train
r2_te15 = m15.score(poly15.transform(Xof_test), yof_test)  # R^2 on test

plt.figure(figsize=(7, 5))
plt.scatter(Xof_train, yof_train, color="steelblue", alpha=0.6, label="train data")
plt.scatter(Xof_test, yof_test, color="orange", alpha=0.8, label="test data")
plt.plot(x_grid, 5 + 3 * x_grid.ravel(), "g--", linewidth=2, label="true line")
plt.plot(
    x_grid,
    y_grid,
    "r-",
    linewidth=1.5,
    label=f"degree-15 fit (R^2 train={r2_tr15:.3f}, test={r2_te15:.3f})",
)
plt.title("Training R^2 improved, yet the model got WORSE on new data")
plt.ylim(yof.min() - 3, yof.max() + 3)
plt.legend()
plt.tight_layout()
plt.savefig("example4_overfitting.png", dpi=120)  # save figure next to this script
plt.close()
print("Figure saved: example4_overfitting.png")

# ======================================================================
# EXAMPLE 5 - What a NEGATIVE R^2 means
# ======================================================================
print("=" * 60)
print("EXAMPLE 5: What a NEGATIVE R^2 means")
print("=" * 60)

y_pred = model.predict(X_test)

# Baseline 1: ignore the model, just predict the average of the training targets
mean_pred = np.full_like(y_test, y_train.mean())
print(
    f"R^2 of 'always predict the mean': "
    f"{r2_score(y_test, mean_pred):.3f}  (roughly 0, as expected)"
)

# Baseline 2: a deliberately terrible prediction (always 10 units too high)
bad_pred = np.full_like(y_test, y_test.mean() + 10)
print(f"R^2 of a deliberately bad model:  " f"{r2_score(y_test, bad_pred):.3f}")

print("-> Negative R^2 means: the model performs WORSE than simply")
print("   predicting the average value of y. Seen often on test data")
print("   when a model overfits or the data shifts.")

# ======================================================================
# EXAMPLE 6 - R^2 alongside MAE and RMSE
# ======================================================================
print("=" * 60)
print("EXAMPLE 6: R^2 alongside MAE and RMSE")
print("=" * 60)

mae = mean_absolute_error(y_test, y_pred)  # average |error|, in y's units
rmse = np.sqrt(mean_squared_error(y_test, y_pred))  # like MAE but big errors hurt more

print(
    f"R^2  = {r2_score(y_test, y_pred):.3f}   (unit-less: share of variance explained)"
)
print(f"MAE  = {mae:.3f}   (average error, in the same units as y)")
print(f"RMSE = {rmse:.3f}   (typical 'big' error, same units as y)")
print("-> R^2 tells you 'how well overall', MAE/RMSE tell you 'how wrong, on average'.")

# A quick predicted-vs-actual plot: points near the dashed line = good fit
plt.figure(figsize=(5, 5))
plt.scatter(y_test, y_pred, color="steelblue", alpha=0.7)
lims = [y_test.min() - 2, y_test.max() + 2]  # range for the diagonal
plt.plot(lims, lims, "r--", label="perfect predictions")
plt.xlabel("actual y")
plt.ylabel("predicted y")
plt.title("Predicted vs actual")
plt.legend()
plt.tight_layout()
plt.savefig("example6_predicted_vs_actual.png", dpi=120)
plt.close()
print("Figure saved: example6_predicted_vs_actual.png")
