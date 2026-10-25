"""
================================================================================
Splitting Criteria in Decision Trees for Regression — Practical Demo
================================================================================
Companion code for the tutorial note. Each section is self-contained.
Run with:  python decision_tree_regression_splitting.py
Requires:  numpy, scikit-learn, matplotlib
================================================================================
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import fetch_california_housing, make_regression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.tree import DecisionTreeRegressor, plot_tree

# ----------------------------------------------------------------------------
# PART 1 — Implement the splitting criteria FROM SCRATCH
# ----------------------------------------------------------------------------
# Why? Seeing the math run line-by-line demystifies what sklearn does internally.
# ----------------------------------------------------------------------------


def mse(targets):
    """Mean Squared Error (= variance) of target values in a node.

    MSE = (1/n) * sum( (y_i - mean(y))^2 )

    Args:
        targets: 1-D numpy array of target values in the node.
    Returns:
        float: the MSE impurity. A perfectly pure node (all same value) -> 0.0
    """
    n = len(targets)  # number of samples in this node
    if n == 0:  # guard: empty node has no impurity
        return 0.0
    mean_y = np.mean(targets)  # the value a leaf would predict here
    squared_deviations = (targets - mean_y) ** 2  # (y_i - mean)^2 for each sample
    return float(np.mean(squared_deviations))  # average -> mean squared error


def mae(targets):
    """Mean Absolute Error of target values around the MEDIAN.

    MAE = (1/n) * sum( |y_i - median(y)| )

    Uses the median (not the mean) because the median minimises absolute error.
    """
    n = len(targets)
    if n == 0:
        return 0.0
    median_y = np.median(targets)  # centre point of the data
    absolute_deviations = np.abs(targets - median_y)  # |y_i - median| for each sample
    return float(np.mean(absolute_deviations))


def split_gain(parent_targets, left_targets, right_targets, criterion="mse"):
    """Compute the impurity reduction (gain) of a candidate binary split.

    gain = impurity(parent) - [w_left * impurity(left) + w_right * impurity(right)]

    where w_left = n_left / n_parent  (weighted by sample count, so big
    child nodes count more than tiny ones).

    A LARGER gain = a BETTER split.
    """
    impurity_fn = mse if criterion == "mse" else mae  # pick the error measure

    n_parent = len(parent_targets)
    n_left = len(left_targets)
    n_right = len(right_targets)

    impurity_parent = impurity_fn(parent_targets)  # spread BEFORE the split
    impurity_left = impurity_fn(left_targets)  # spread of left child
    impurity_right = impurity_fn(right_targets)  # spread of right child

    # weighted average impurity of the children (weight = fraction of samples)
    weighted_children = (n_left / n_parent) * impurity_left + (
        n_right / n_parent
    ) * impurity_right

    return impurity_parent - weighted_children  # reduction in spread


print("=" * 70)
print("PART 1 — Manual splitting-criterion calculation (no sklearn)")
print("=" * 70)

# Tiny house-price dataset: size_sqm, bedrooms -> price in thousands
size_sqm = np.array([50, 60, 80, 100, 120, 150])
bedrooms = np.array([1, 1, 2, 2, 3, 3])
price = np.array([120, 135, 180, 210, 260, 330])  # target, in $1000s

# Candidate split 1: size_sqm <= 80  -> left = smallest 3 houses, right = biggest 3
mask1 = size_sqm <= 80
gain1 = split_gain(price, price[mask1], price[~mask1], criterion="mse")

# Candidate split 2: bedrooms <= 2
mask2 = bedrooms <= 2
gain2 = split_gain(price, price[mask2], price[~mask2], criterion="mse")

print(f"Parent price MSE: {mse(price):.2f}\n")
print(f"Split 'size_sqm <= 80':   MSE gain = {gain1:.2f}")
print(f"Split 'bedrooms <= 2':    MSE gain = {gain2:.2f}")
print("\n=> Decision tree would choose the split with the LARGEST gain.")

# Same comparison using MAE (robust alternative)
print(f"\nMAE parent: {mae(price):.2f}")
print(
    f"MAE gain, size split: {split_gain(price, price[mask1], price[~mask1], 'mae'):.2f}"
)
print(
    f"MAE gain, bedroom split: {split_gain(price, price[mask2], price[~mask2], 'mae'):.2f}"
)

# Micro-example straight from the tutorial note: targets [3,5,7,9]
print("\nWorked micro-example: targets [3, 5, 7, 9], split on <=5")
demo = np.array([3, 5, 7, 9])
print(f"  parent MSE = {mse(demo)}  (expected 5.0)")
print(
    f"  gain       = {split_gain(demo, demo[demo <= 5], demo[demo > 5]):.1f}  (expected 4.0)"
)

# ----------------------------------------------------------------------------
# PART 2 — sklearn: verify the criterion matches the manual math
# ----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("PART 2 — Verify sklearn's 'criterion' with our from-scratch math")
print("=" * 70)

X = np.column_stack([size_sqm, bedrooms])  # features as a 2-D array
tree = DecisionTreeRegressor(criterion="squared_error", max_depth=1, random_state=0)
tree.fit(X, price)  # fit a depth-1 tree (single split)

root_mse = getattr(tree.tree_, "impurity")[0]  # impurity stored in the root node
print(f"sklearn root impurity (MSE): {root_mse:.2f}")
print(f"Our manual MSE of targets:    {mse(price):.2f}   <- should match!")

# Which split did sklearn pick?  (feature 0 = size_sqm, 1 = bedrooms)
feat = getattr(tree.tree_, "feature")[0]
thr = getattr(tree.tree_, "threshold")[0]
print(
    f"sklearn chose: feature {feat} ({'size_sqm' if feat == 0 else 'bedrooms'}) <= {thr:.1f}"
)
print("(matches whichever candidate had the highest gain in Part 1)")

# Visualise the tiny tree — every node shows the criterion (MSE) value
fig, ax = plt.subplots(figsize=(8, 4))
plot_tree(
    tree,
    feature_names=["size_sqm", "bedrooms"],
    filled=True,
    ax=ax,
    rounded=True,
    precision=1,
)
ax.set_title("Depth-1 regression tree (node values = MSE impurity)")
plt.tight_layout()
plt.savefig("tiny_tree.png", dpi=120)
print("Saved visualisation -> tiny_tree.png")

# ----------------------------------------------------------------------------
# PART 3 — Real dataset: California housing, compare both criteria
# ----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("PART 3 — California housing: squared_error vs absolute_error")
print("=" * 70)

try:
    # Classic regression dataset (downloads ~2 MB on first run; needs internet).
    # 8 features, target = house value ($100k)
    X_all, y_all = fetch_california_housing(return_X_y=True)
    print("(Using California housing dataset)")
except OSError:
    # Fallback: synthetic data with the same shape, so the script always runs.
    print("(No internet - using synthetic fallback dataset)")
    X_all, y_all = make_regression(
        n_samples=16512, n_features=8, noise=20.0, random_state=42
    )[:2]

X_tr, X_te, y_tr, y_te = train_test_split(
    X_all, y_all, test_size=0.2, random_state=42
)  # 80/20 split, fixed seed

results: dict[str, float] = {}
criteria: list[Literal["squared_error", "absolute_error"]] = [
    "squared_error",
    "absolute_error",
]
for crit in criteria:
    reg = DecisionTreeRegressor(
        criterion=crit, max_depth=5, min_samples_leaf=5, random_state=42
    )
    reg.fit(X_tr, y_tr)  # train
    pred = reg.predict(X_te)  # predict
    rmse = np.sqrt(mean_squared_error(y_te, pred))  # error metric
    results[crit] = rmse
    print(f"{crit:<18} RMSE = {rmse:.4f}   (R2 = {reg.score(X_te, y_te):.4f})")

best = min(results, key=lambda name: results[name])
print(f"\nBest criterion on this data: {best}")

# Show the danger of NO regularisation (the criterion can't save an overfit tree)
overfit = DecisionTreeRegressor(
    criterion="squared_error", random_state=42
)  # no max_depth!
overfit.fit(X_tr, y_tr)
print(
    f"\nUnrestricted tree: train R2 = {overfit.score(X_tr, y_tr):.4f} "
    f"vs test R2 = {overfit.score(X_te, y_te):.4f}  <- classic overfitting"
)

# ----------------------------------------------------------------------------
# PART 4 — GridSearchCV: let cross-validation pick the criterion
# ----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("PART 4 — GridSearchCV over criterion + regularisation hyperparameters")
print("=" * 70)

param_grid = {
    "criterion": ["squared_error", "absolute_error"],
    "max_depth": [3, 5, 8, None],
    "min_samples_leaf": [1, 5, 10],
}
grid = GridSearchCV(
    DecisionTreeRegressor(random_state=42),  # model to tune
    param_grid,  # search space
    cv=5,  # 5-fold cross-validation
    scoring="neg_root_mean_squared_error",  # metric to optimise
    n_jobs=-1,  # use all CPU cores
)
# NOTE: 'absolute_error' trees are slow to train, so we grid-search on a
# 3000-row subsample for speed; the workflow is identical on full data.
gs_X, _, gs_y, _ = train_test_split(X_tr, y_tr, train_size=3000, random_state=42)
grid.fit(gs_X, gs_y)
print("Best parameters:", grid.best_params_)
print(f"Best CV RMSE: {-grid.best_score_:.4f}")

# ----------------------------------------------------------------------------
# PART 5 — Outlier robustness shootout: MSE vs MAE
# ----------------------------------------------------------------------------
print("\n" + "=" * 70)
print("PART 5 — Inject 5% outliers: which criterion survives better?")
print("=" * 70)

rng = np.random.default_rng(42)
n_out = int(0.05 * len(y_tr))  # 5% of training rows
out_idx = rng.choice(len(y_tr), size=n_out, replace=False)
y_tr_dirty = y_tr.copy()
y_tr_dirty[out_idx] += rng.uniform(10, 20, n_out)  # add $1M-$2M junk values

from typing import Literal  # noqa: E402

criteria: list[Literal["squared_error", "absolute_error"]] = [
    "squared_error",
    "absolute_error",
]
for crit in criteria:
    reg = DecisionTreeRegressor(
        criterion=crit, max_depth=5, min_samples_leaf=5, random_state=42
    )
    reg.fit(X_tr, y_tr_dirty)  # train on POLLUTED targets
    pred = reg.predict(X_te)
    rmse = np.sqrt(mean_squared_error(y_te, pred))  # evaluate on CLEAN test set
    print(f"Trained on data with outliers | {crit:<18} clean-test RMSE = {rmse:.4f}")

print("\nExpected: the MAE ('absolute_error') tree degrades much less,")
print("because absolute error grows linearly and resists outlier domination.")

print("\nAll parts finished successfully. See tiny_tree.png for the visual.")
