"""
Feature Selection with the Correlation Matrix - runnable tutorial code
======================================================================

Companion script to the markdown tutorial. Every step is commented line by
line. It generates its own data, so it runs offline with no downloads.

Run with:  python feature_selection_correlation.py

Outputs (saved in ./correlation_tutorial_plots/):
    1_correlation_matrix_synthetic.png   - heatmap of the synthetic example
    2_feature_correlation_diabetes.png   - heatmap of the real dataset
"""

# ----------------------------- Imports -----------------------------------
import os  # os: talk to the file system (make output folder)

import matplotlib  # matplotlib: plotting library
import numpy as np  # numpy: fast numerical arrays
import pandas as pd  # pandas: tables / DataFrames

matplotlib.use("Agg")  # "Agg" = save plots to files (no display window needed)
import matplotlib.pyplot as plt  # pyplot: the plotting interface
import seaborn as sns  # seaborn: prettier statistical plots (heatmaps)

# scikit-learn: datasets + model + evaluation tools
from sklearn.datasets import (
    load_diabetes,  # small real regression dataset, bundled with sklearn
)
from sklearn.ensemble import RandomForestRegressor  # a solid default model
from sklearn.metrics import r2_score  # R^2 = how well the model explains the target
from sklearn.model_selection import train_test_split  # split data into train/test

# Where to save the figures this script produces
OUTPUT_DIR = "correlation_tutorial_plots"  # name of the output folder
os.makedirs(OUTPUT_DIR, exist_ok=True)  # create the folder if it does not exist yet


# ----------------------- Reusable helper function -------------------------
def drop_correlated_features(data, threshold=0.8):
    """Drop one feature from every pair whose |correlation| exceeds `threshold`.

    Args:
        data      : DataFrame of numeric features (target column already removed).
        threshold : correlation cutoff, e.g. 0.8 (default) or 0.9 (conservative).

    Returns:
        (cleaned DataFrame, list of dropped column names)
    """
    corr_matrix = data.corr().abs()  # 1. absolute Pearson correlation of every pair
    #    (.abs(): strength matters, sign does not)
    upper = corr_matrix.where(  # 2. build a mask that keeps ONLY the upper triangle
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )  #    k=1 skips the diagonal (self-correlation = 1)
    #    -> each pair appears exactly ONCE, no double counting
    to_drop = [
        col
        for col in upper.columns  # 3. for every column...
        if any(upper[col] > threshold)
    ]  #    ...if it is strongly correlated with ANY
    #       earlier column, mark it for removal
    return (
        data.drop(columns=to_drop),
        to_drop,
    )  # 4. return cleaned data + what was dropped


# ===========================================================================
# EXAMPLE 1 - Synthetic data: SEE the redundancy
# ===========================================================================
print("=" * 70)
print("EXAMPLE 1: synthetic dataset with deliberate redundancy")
print("=" * 70)

rng = np.random.default_rng(seed=42)  # seeded generator -> identical data every run

n = 300  # number of rows we will generate

signal = rng.normal(0, 1, n)  # genuinely informative feature
x1 = rng.normal(5, 2, n)  # base feature
x2 = x1 + rng.normal(0, 0.1, n)  # x2 = x1 + tiny noise  -> REDUNDANT copy of x1
x3 = rng.normal(10, 3, n)  # another base feature
x4 = x3 + rng.normal(0, 0.1, n)  # x4 = x3 + tiny noise  -> REDUNDANT copy of x3
noise = rng.normal(0, 1, n)  # pure noise: carries no information at all

target = (
    3 * signal + 0.5 * x1 + rng.normal(0, 0.5, n)
)  # target depends on signal and x1 (plus small noise)

df = pd.DataFrame(
    {  # bundle everything into a DataFrame
        "signal": signal,
        "x1": x1,
        "x2": x2,
        "x3": x3,
        "x4": x4,
        "noise": noise,
        "target": target,
    }
)

# --- Step 1: compute the correlation matrix --------------------------------
corr = df.corr()  # Pearson correlation for every pair of columns
print("\nCorrelation matrix (rounded):")
print(corr.round(2))  # .round(2): two decimals so it is easy to read

# --- Step 2: visualize it as a heatmap -------------------------------------
plt.figure(figsize=(7, 5))  # create a figure 7x5 inches
sns.heatmap(
    corr,  # draw the correlation matrix as a colored grid
    annot=True,  # print the numbers inside the cells
    cmap="coolwarm",  # blue = negative, white = 0, red = positive
    vmin=-1,
    vmax=1,
)  # fix the color scale to the full -1..+1 range
plt.title("Example 1 - correlation matrix (synthetic data)")
plt.tight_layout()  # tighten spacing so labels do not get cut off
plt.savefig(os.path.join(OUTPUT_DIR, "1_correlation_matrix_synthetic.png"), dpi=120)
plt.close()  # close figure to free memory (headless backend)

# --- Step 3: automatically drop redundant features --------------------------
X = df.drop(columns="target")  # features only (remove the target column)
X_reduced, dropped = drop_correlated_features(
    X, threshold=0.8
)  # drop pairs above |r| = 0.8
print("\nDropped redundant features:", dropped)  # expect ['x2', 'x4']
print(
    "Remaining features:       ", list(X_reduced.columns)
)  # expect ['signal', 'x1', 'x3', 'noise']

# --- Step 4: rank features by usefulness to the target ----------------------
target_corr = (
    df.corr()["target"].abs().sort_values(ascending=False)
)  # |corr| with target, biggest first
print("\nAbsolute correlation with target (high = promising, low = probably useless):")
print(target_corr.round(2))  # expect 'signal' on top, 'noise' near the bottom


# ===========================================================================
# EXAMPLE 2 - Real data: model performance BEFORE vs AFTER selection
# ===========================================================================
print("\n" + "=" * 70)
print("EXAMPLE 2: diabetes dataset - does selection hurt the model?")
print("=" * 70)

X, y = load_diabetes(
    return_X_y=True, as_frame=True
)  # load features and target directly as DataFrames
print(f"\nDataset: {X.shape[0]} rows x {X.shape[1]} features")

# --- Split FIRST: the correlation matrix must only ever see training data ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)  # 80% train / 20% test, reproducible split


def evaluate(X_tr, X_te, y_tr, y_te):
    """Train a fresh RandomForest on X_tr and return its R^2 on X_te."""
    model = RandomForestRegressor(
        n_estimators=300, random_state=42
    )  # 300 trees, seeded for reproducibility
    model.fit(X_tr, y_tr)  # learn patterns from the training features
    return r2_score(
        y_te, model.predict(X_te)
    )  # score predictions on the unseen test set


# --- Visualize the real dataset's correlation matrix ------------------------
plt.figure(figsize=(8, 6))
sns.heatmap(X_train.corr(), annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f")
plt.title("Example 2 - feature correlation matrix (diabetes, training set)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "2_feature_correlation_diabetes.png"), dpi=120)
plt.close()

# --- Model A: use ALL features ----------------------------------------------
r2_all = evaluate(X_train, X_test, y_train, y_test)

# --- Select features using the TRAINING set only ----------------------------
X_train_small, dropped_cols = drop_correlated_features(X_train, threshold=0.8)
X_test_small = X_test[
    X_train_small.columns
]  # apply the SAME kept columns to the test set

# --- Model B: use the REDUCED feature set -----------------------------------
r2_reduced = evaluate(X_train_small, X_test_small, y_train, y_test)

print(f"\nR^2 with all features      ({X.shape[1]:>2} features): {r2_all:.4f}")
print(
    f"R^2 with reduced features  ({X_train_small.shape[1]:>2} features): {r2_reduced:.4f}"
)
print("Dropped columns:", dropped_cols)

# --- Takeaway message --------------------------------------------------------
if r2_reduced >= r2_all - 0.02:  # within 2% counts as "no meaningful loss"
    print("\n>> Selection kept the performance while simplifying the model - win!")
else:
    print("\n>> Performance dropped: lower the threshold or keep more features.")

print(f"\nPlots saved in: {os.path.abspath(OUTPUT_DIR)}")
