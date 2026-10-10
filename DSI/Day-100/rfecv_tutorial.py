"""
RFECV: Recursive Feature Elimination with Cross-Validation
==========================================================
A beginner-friendly, runnable companion to `rfecv_tutorial.md`.

Topic in the series: Cleaning and Preparing Data for Machine Learning
-> Feature selection with RFECV (practical, wrapper-method approach)

What it does
------------
1. Trains a baseline model on all 30 breast-cancer features.
2. Runs RFECV to find (a) which features to keep and (b) how many.
3. Plots the cross-validated score curve and the feature ranking.
4. Tests RFECV on synthetic data with known ground-truth features.
5. Shows the leak-proof way: RFECV nested inside a Pipeline + CV.

Runs offline (sklearn's bundled datasets only).
All figures are saved to ./plots/ and then displayed.

Usage
-----
    pip install "scikit-learn>=1.0" pandas matplotlib numpy
    python rfecv_tutorial.py
"""

# ===========================================================================
# 01 - Imports, configuration and small helpers
# ===========================================================================
import os  # to create the plots/ folder

import matplotlib.pyplot as plt  # plotting
import numpy as np  # numeric arrays (argmax, arange...)
import pandas as pd  # DataFrames for readable feature tables
from sklearn.datasets import load_breast_cancer, make_classification
from sklearn.ensemble import RandomForestClassifier  # a non-linear model
from sklearn.feature_selection import RFECV  # <- the star of the show
from sklearn.linear_model import LogisticRegression  # a simple, linear model
from sklearn.metrics import roc_auc_score  # evaluation metric
from sklearn.model_selection import (
    StratifiedKFold,  # keeps the class ratio in every fold
)
from sklearn.model_selection import (
    cross_val_score,  # quick CV scores for a whole pipeline
)
from sklearn.model_selection import train_test_split  # hold-out split
from sklearn.pipeline import Pipeline  # chain steps correctly
from sklearn.preprocessing import StandardScaler  # z-score scaling

RANDOM_STATE = 42  # fixed seed => reproducible results
PLOTS_DIR = "plots"  # every figure goes into ./plots/
os.makedirs(PLOTS_DIR, exist_ok=True)  # create the folder if it does not exist


def save_and_show(fig, filename, dpi=150):
    """Save a matplotlib figure into ./plots/ and then display it."""
    path = os.path.join(PLOTS_DIR, filename)  # e.g. plots/rfecv_cv_curve.png
    fig.savefig(path, dpi=dpi, bbox_inches="tight")  # write the PNG to disk
    plt.show()  # show it interactively
    print(f"[saved] {path}")  # log where it went


def banner(title):
    """Print a clearly visible section header in the console output."""
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


# ===========================================================================
# 02 - Load the breast-cancer data, split it, and scale it
# ===========================================================================
def load_scaled_breast_cancer():
    """Load the breast-cancer data, split it, and standardise the features.

    Returns (X_train, X_test, y_train, y_test) where X_* are DataFrames.
    """
    data = load_breast_cancer(as_frame=True)  # as_frame=True -> pandas objects
    X = data.data  # 569 rows x 30 columns
    y = data.target  # 0 = malignant, 1 = benign

    print(f"Rows x columns        : {X.shape[0]} x {X.shape[1]}")
    print(f"Missing values (total): {int(X.isna().sum().sum())}")
    print(f"Class balance         : {y.value_counts().to_dict()}")

    # Split BEFORE any scaling or selection -> the test set stays untouched.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,  # 25% held out for the final honest check
        stratify=y,  # keep the same class ratio in both parts
        random_state=RANDOM_STATE,
    )

    # StandardScaler makes every column mean=0, std=1. Needed because RFE
    # compares coefficient magnitudes and LogisticRegression penalises them.
    scaler = StandardScaler()
    scaler.fit(X_train)  # learn mean/std ONLY from the training set

    # transform() applies the learned mean/std -> no leakage from the test set
    X_train_s = pd.DataFrame(
        scaler.transform(X_train), columns=X.columns, index=X_train.index
    )
    X_test_s = pd.DataFrame(
        scaler.transform(X_test), columns=X.columns, index=X_test.index
    )
    return X_train_s, X_test_s, y_train, y_test


# ===========================================================================
# 03 - DEMO 1: baseline model on all features
# ===========================================================================
def demo_1_breast_cancer():
    """RFECV with a logistic regression on the breast-cancer dataset."""
    banner("DEMO 1 - RFECV on breast-cancer data (Logistic Regression)")
    X_train, X_test, y_train, y_test = load_scaled_breast_cancer()

    # One shared CV splitter, so every model is compared on identical folds.
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    # --- Baseline: keep all 30 features -----------------------------------
    baseline = LogisticRegression(max_iter=5000, random_state=RANDOM_STATE)
    baseline_cv = cross_val_score(
        baseline,
        X_train,
        y_train,  # data used for CV
        cv=cv,  # the 5 folds defined above
        scoring="roc_auc",  # metric we want to maximise
        n_jobs=-1,  # use all CPU cores
    )
    print(
        f"Baseline (30 features) -> CV AUC "
        f"{baseline_cv.mean():.4f} +/- {baseline_cv.std():.4f}"
    )

    # =======================================================================
    # 04 - Run RFECV
    # =======================================================================
    # --- RFECV: find the best number of features automatically ------------
    rfecv = RFECV(
        estimator=LogisticRegression(max_iter=5000, random_state=RANDOM_STATE),
        step=1,  # drop the single worst feature each round
        min_features_to_select=1,  # scan all the way down to 1 feature
        cv=cv,  # 5-fold cross-validation
        scoring="roc_auc",  # maximise AUC
        n_jobs=-1,  # parallelise the folds
    )

    # fit() runs the whole elimination path and scores every prefix.
    # Cost = n_features * cv model fits (here 30 * 5 = 150 fits).
    rfecv.fit(X_train, y_train)

    selected_features = X_train.columns[rfecv.support_].tolist()  # kept names
    n_selected = int(rfecv.support_.sum())  # how many kept
    print(f"\nRFECV kept {n_selected} of {X_train.shape[1]} features:")
    print(selected_features)

    # =======================================================================
    # 05 - Plot: CV score versus number of features
    # =======================================================================
    # --- Plot the CV score versus the number of features -------------------
    mean_scores = rfecv.cv_results_["mean_test_score"]  # mean AUC per subset size
    std_scores = rfecv.cv_results_["std_test_score"]  # spread across the 5 folds

    # x-axis values: number of features used at each step.
    # Recent scikit-learn stores them directly in cv_results_["n_features"].
    if "n_features" in rfecv.cv_results_:
        k_values = list(rfecv.cv_results_["n_features"])
    else:  # fallback for very old versions
        k_values = list(
            range(
                rfecv.min_features_to_select,
                rfecv.min_features_to_select + len(mean_scores),
            )
        )

    best_idx = int(np.argmax(mean_scores))  # index of the highest mean score
    best_k = k_values[best_idx]  # the winning feature count

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.errorbar(
        k_values,
        mean_scores,
        yerr=std_scores,
        fmt="-o",
        capsize=3,
        color="#1f77b4",
        label="mean CV AUC +/- 1 std",
    )
    ax.axvline(
        best_k, color="crimson", linestyle="--", label=f"best = {best_k} features"
    )
    ax.scatter([best_k], [mean_scores[best_idx]], color="crimson", zorder=5)
    ax.set_xlabel("Number of features kept")
    ax.set_ylabel("Cross-validated ROC AUC")
    ax.set_title("RFECV: how many features do we actually need?")
    ax.grid(alpha=0.3)
    ax.legend()
    save_and_show(fig, "rfecv_cv_curve_logreg.png")  # saves then shows

    # =======================================================================
    # 06 - Plot: feature ranking
    # =======================================================================
    # --- Feature ranking ---------------------------------------------------
    ranking_df = (
        pd.DataFrame({"feature": X_train.columns, "ranking": rfecv.ranking_})
        .sort_values(["ranking", "feature"])  # best features first
        .reset_index(drop=True)
    )

    fig, ax = plt.subplots(figsize=(9, 8))
    colors = ["#2ca02c" if r == 1 else "#d62728" for r in ranking_df["ranking"]]
    ax.barh(ranking_df["feature"], ranking_df["ranking"], color=colors)
    ax.invert_yaxis()  # rank 1 at the top
    ax.set_xlabel("RFECV ranking (1 = kept, higher = eliminated earlier)")
    ax.set_title("Which features survived, and which were eliminated first?")
    save_and_show(fig, "rfecv_feature_ranking_logreg.png")

    print("\nTop 12 features by ranking:")
    print(ranking_df.head(12).to_string(index=False))

    # =======================================================================
    # 07 - Final model, hold-out score, side-by-side comparison
    # =======================================================================
    # --- Refit on the selected features and evaluate on the hold-out set ---
    final_model = LogisticRegression(max_iter=5000, random_state=RANDOM_STATE)
    final_model.fit(X_train[selected_features], y_train)
    test_auc_selected = roc_auc_score(
        y_test, final_model.predict_proba(X_test[selected_features])[:, 1]
    )

    # Same thing with all features, for a fair comparison
    full_model = LogisticRegression(max_iter=5000, random_state=RANDOM_STATE)
    full_model.fit(X_train, y_train)
    test_auc_full = roc_auc_score(y_test, full_model.predict_proba(X_test)[:, 1])

    # Cross-validated score of the reduced model on the training data
    selected_cv = cross_val_score(
        LogisticRegression(max_iter=5000, random_state=RANDOM_STATE),
        X_train[selected_features],
        y_train,
        cv=cv,
        scoring="roc_auc",
        n_jobs=-1,
    )

    print(f"\nHold-out test AUC, all features   : {test_auc_full:.4f}")
    print(
        f"Hold-out test AUC, RFECV features : {test_auc_selected:.4f} "
        f"({n_selected} columns)"
    )

    # --- Bar chart: full vs reduced ---------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    cv_labels = ["All features", f"RFECV ({n_selected})"]
    cv_means = [baseline_cv.mean(), selected_cv.mean()]
    cv_stds = [baseline_cv.std(), selected_cv.std()]
    axes[0].bar(
        cv_labels, cv_means, yerr=cv_stds, capsize=6, color=["#7f7f7f", "#2ca02c"]
    )
    axes[0].set_ylim(min(cv_means) - 0.02, 1.0)  # zoom in on the differences
    axes[0].set_ylabel("ROC AUC")
    axes[0].set_title("5-fold CV on training data")

    test_labels = ["All features", f"RFECV ({n_selected})"]
    test_values = [test_auc_full, test_auc_selected]
    axes[1].bar(test_labels, test_values, color=["#7f7f7f", "#2ca02c"])
    axes[1].set_ylim(min(test_values) - 0.02, 1.0)
    axes[1].set_ylabel("ROC AUC")
    axes[1].set_title("Hold-out test set (untouched during selection)")

    fig.suptitle("Does dropping features hurt? (usually not)")
    save_and_show(fig, "baseline_vs_rfecv_auc.png")

    return {
        "n_selected": n_selected,
        "selected_features": selected_features,
        "cv_full": baseline_cv.mean(),
        "cv_selected": selected_cv.mean(),
        "test_full": test_auc_full,
        "test_selected": test_auc_selected,
    }


# ===========================================================================
# 08 - DEMO 2: synthetic data with a known answer key
# ===========================================================================
def make_synthetic_data(
    n_samples=1200,
    n_informative=8,
    n_redundant=6,
    n_noise=16,
    random_state=RANDOM_STATE,
):
    """Build a classification dataset where we KNOW which features matter."""
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_informative + n_redundant + n_noise,  # 8 + 6 + 16 = 30
        n_informative=n_informative,  # real signal columns
        n_redundant=n_redundant,  # linear copies of the signal
        n_repeated=0,  # exact duplicates: none, keep it simple
        n_clusters_per_class=2,
        class_sep=1.0,  # how separable the classes are
        flip_y=0.02,  # 2% label noise -> realistic
        shuffle=False,  # keep informative columns FIRST
        random_state=random_state,
    )

    # Give the columns human-readable names so we can check RFECV's work.
    names = []
    for i in range(X.shape[1]):
        if i < n_informative:
            names.append(f"informative_{i + 1}")
        elif i < n_informative + n_redundant:
            names.append(f"redundant_{i - n_informative + 1}")
        else:
            names.append(f"noise_{i - n_informative - n_redundant + 1}")

    return pd.DataFrame(X, columns=names), pd.Series(y, name="target")


def demo_2_synthetic():
    """Check whether RFECV can find the truly informative features."""
    banner("DEMO 2 - Can RFECV recover the ground-truth features?")
    X, y = make_synthetic_data()
    print(
        f"Dataset: {X.shape[0]} rows, {X.shape[1]} columns "
        f"(8 informative, 6 redundant, 16 noise)"
    )

    # Random forests do not need scaling, so we can use the raw data here.
    rfecv = RFECV(
        estimator=RandomForestClassifier(
            n_estimators=150,  # 150 trees per fit: stable importances
            random_state=RANDOM_STATE,
            n_jobs=1,  # keep inside-fit threads off (see note)
        ),
        step=2,  # drop 2 features per round -> ~2x faster
        min_features_to_select=2,  # do not go below 2 features
        cv=5,
        scoring="roc_auc",
        n_jobs=-1,  # parallelise across folds instead
    )
    rfecv.fit(X, y)

    support = pd.Series(rfecv.support_, index=X.columns)  # True = kept
    kept = support[support].index.tolist()  # kept column names

    informative_kept = sum(name.startswith("informative") for name in kept)
    redundant_kept = sum(name.startswith("redundant") for name in kept)
    noise_kept = sum(name.startswith("noise") for name in kept)

    print(f"\nKept {len(kept)} features total:")
    print(f"  informative : {informative_kept}/8   <- the real signal")
    print(f"  redundant   : {redundant_kept}/6   <- duplicates of the signal")
    print(f"  noise       : {noise_kept}/16  <- pure randomness")
    print(f"Recall on the true drivers: {informative_kept / 8:.0%}")

    # =======================================================================
    # 09 - Plot: how each category was treated
    # =======================================================================
    # --- Visualise how the selector treated each category ------------------
    categories = [
        "informative\n(true signal)",
        "redundant\n(signal copies)",
        "noise\n(useless)",
    ]
    totals = [8, 6, 16]  # how many columns exist per category
    kept_counts = [informative_kept, redundant_kept, noise_kept]

    x = np.arange(len(categories))  # x positions of the groups
    width = 0.35  # bar width

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width / 2, totals, width, label="available", color="#c7c7c7")
    ax.bar(x + width / 2, kept_counts, width, label="kept by RFECV", color="#2ca02c")
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel("Number of features")
    ax.set_title("RFECV keeps the signal and discards most of the noise")
    ax.legend()
    save_and_show(fig, "rfecv_synthetic_recovery.png")

    return informative_kept, redundant_kept, noise_kept, len(kept)


# ===========================================================================
# 10 - DEMO 3: leakage-free nested CV with RFECV inside a Pipeline
# ===========================================================================
def demo_3_nested_cv():
    """Compare 'all features' vs 'RFECV' inside a fully leak-proof pipeline."""
    banner("DEMO 3 - Leakage-free (nested) comparison of the two strategies")
    data = load_breast_cancer(as_frame=True)
    X, y = data.data, data.target  # raw data, no manual scaling
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    # Strategy A: scale + model (all features)
    pipe_all = Pipeline(
        [
            ("scaler", StandardScaler()),  # fitted inside each fold
            ("clf", LogisticRegression(max_iter=5000, random_state=RANDOM_STATE)),
        ]
    )

    # Strategy B: scale + SELECT + model. RFECV sits in the middle as a
    # transformer: it shrinks the column set, then the classifier is trained.
    pipe_rfecv = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "rfecv",
                RFECV(
                    estimator=LogisticRegression(
                        max_iter=5000, random_state=RANDOM_STATE
                    ),
                    step=1,
                    min_features_to_select=1,
                    cv=5,  # inner CV, run inside every outer fold
                    scoring="roc_auc",
                ),
            ),
            ("clf", LogisticRegression(max_iter=5000, random_state=RANDOM_STATE)),
        ]
    )

    # cross_val_score clones and refits the WHOLE pipeline per fold:
    # scaling, selection and training all happen on the training part only.
    scores_all = cross_val_score(pipe_all, X, y, cv=cv, scoring="roc_auc", n_jobs=-1)
    scores_rfecv = cross_val_score(
        pipe_rfecv, X, y, cv=cv, scoring="roc_auc", n_jobs=-1
    )

    print(f"All 30 features : AUC {scores_all.mean():.4f} +/- {scores_all.std():.4f}")
    print(
        f"With RFECV      : AUC {scores_rfecv.mean():.4f} +/- {scores_rfecv.std():.4f}"
    )
    print(f"Per-fold RFECV scores: {np.round(scores_rfecv, 4)}")

    # --- Box plot of the per-fold scores ----------------------------------
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.boxplot(
        [scores_all, scores_rfecv],
        tick_labels=["All features", "RFECV inside pipeline"],
    )
    ax.scatter(
        np.ones_like(scores_all) + np.random.uniform(-0.05, 0.05, len(scores_all)),
        scores_all,
        color="#1f77b4",
        zorder=3,
    )  # show each fold
    ax.scatter(
        np.ones_like(scores_rfecv) * 2
        + np.random.uniform(-0.05, 0.05, len(scores_rfecv)),
        scores_rfecv,
        color="#2ca02c",
        zorder=3,
    )
    ax.set_ylabel("ROC AUC")
    ax.set_title("Nested CV: honest estimate of the RFECV benefit")
    save_and_show(fig, "rfecv_nested_cv.png")

    return scores_all.mean(), scores_rfecv.mean()


# ===========================================================================
# 11 - Entry point
# ===========================================================================
if __name__ == "__main__":
    # Each demo prints its findings and saves its figures into ./plots/.
    summary = demo_1_breast_cancer()

    print("\n" + "-" * 72)
    print("SUMMARY - Demo 1")
    print(f"  features kept          : {summary['n_selected']} " f"(from 30)")
    print(f"  CV AUC, all features   : {summary['cv_full']:.4f}")
    print(f"  CV AUC, RFECV features : {summary['cv_selected']:.4f}")
    print(f"  test AUC, all features : {summary['test_full']:.4f}")
    print(f"  test AUC, RFECV        : {summary['test_selected']:.4f}")
    print(f"  kept: {summary['selected_features']}")
    print("-" * 72)

    demo_2_synthetic()  # do we recover the true informative features?
    demo_3_nested_cv()  # honest, leakage-free evaluation

    print("\nAll figures were saved to ./plots/")
