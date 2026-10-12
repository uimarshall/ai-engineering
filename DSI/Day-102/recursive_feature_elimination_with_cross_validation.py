"""
recursive_feature_elimination_with_cross_validation.py
======================================================
Companion script for the tutorial
"RECURSIVE_FEATURE_ELIMINATION_WT_CROSS_VALIDATION.md"
(Cleaning & Preparing Data for Machine Learning series).

What it does
------------
PART A - sklearn's bundled breast-cancer data (569 x 30, offline):
         1. baseline CV using all 30 features
         2. RFECV to find the best subset size
         3. the CV curve  -> "how many features should I keep?"
         4. the RFE ranking of every feature
         5. hold-out comparison: all features vs the RFECV subset
         6. plain RFE for contrast
PART B - synthetic data (25 columns) where we KNOW which 10 are real
PART C - a numeric demonstration of selection bias (why RFECV must be nested)

Everything is offline: only sklearn's bundled dataset + make_classification.
Every figure is written to ./plots/ (created automatically) and then shown.

Run:
    python recursive_feature_elimination_with_cross_validation.py
"""

# ---------------------------------------------------------------------------
# SECTION 0 - Imports and configuration
# ---------------------------------------------------------------------------
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
from sklearn.datasets import load_breast_cancer, make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE, RFECV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import (
    RepeatedStratifiedKFold,
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.utils import Bunch

PLOTS_DIR = "plots"  # every figure is written here
RANDOM_STATE = 42  # fixed seed -> reproducible splits and scores


def ensure_plots_dir():
    """Create ./plots once so every savefig() call has somewhere to write."""
    os.makedirs(PLOTS_DIR, exist_ok=True)


def save_fig(name):
    """Save the active figure to ./plots/<name> BEFORE plt.show() clears it."""
    path = os.path.join(PLOTS_DIR, name)
    plt.savefig(path, dpi=120, bbox_inches="tight")  # write the PNG to disk
    print(f"  [saved] {path}")


# ---------------------------------------------------------------------------
# SECTION 1 - Load the data and split it
# ---------------------------------------------------------------------------
def load_breast_cancer_data():
    """Load sklearn's bundled dataset as a DataFrame (works offline)."""
    bunch = load_breast_cancer(as_frame=True)  # 569 samples, 30 numeric features
    if not isinstance(bunch, Bunch):
        raise TypeError("Expected load_breast_cancer to return a dataset bunch.")
    X = bunch.data  # feature DataFrame
    y = bunch.target  # 1 = benign, 0 = malignant
    print(f"Dataset shape: {X.shape[0]} rows x {X.shape[1]} features")
    print(f"Class balance: {np.bincount(y)}  (0 = malignant, 1 = benign)")
    return X, y


def prepare_data(X, y, test_size=0.25):
    """Stratified train/test split, then scale - fitting the scaler on TRAIN only."""
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,  # hold out 25% of the rows
        stratify=y,  # keep the same class ratio in both parts
        random_state=RANDOM_STATE,
    )  # reproducible split

    scaler = StandardScaler()
    # fit_transform on TRAIN learns mean/std; transform on TEST reuses them
    X_train_s = pd.DataFrame(
        scaler.fit_transform(X_train), columns=X.columns, index=X_train.index
    )
    X_test_s = pd.DataFrame(
        scaler.transform(X_test), columns=X.columns, index=X_test.index
    )
    print(f"Train: {X_train_s.shape} | Test: {X_test_s.shape}")
    return X_train_s, X_test_s, y_train, y_test


# ---------------------------------------------------------------------------
# SECTION 2 - Baseline: what does "use every feature" score?
# ---------------------------------------------------------------------------
def baseline_cv(X_train, y_train, cv, scoring="roc_auc"):
    """Cross-validated score using every feature - our number to beat."""
    model = LogisticRegression(
        max_iter=5000, solver="liblinear"  # many iterations -> guaranteed convergence
    )  # robust solver for small data
    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring=scoring,  # metric we care about
        n_jobs=-1,
    )  # use all CPU cores
    print(
        f"Baseline (all {X_train.shape[1]} features) "
        f"{scoring} = {scores.mean():.4f} +/- {scores.std():.4f}"
    )
    return scores


# ---------------------------------------------------------------------------
# SECTION 3 - Run RFECV
# ---------------------------------------------------------------------------
def run_rfecv(X_train, y_train, cv, scoring="roc_auc", step=1):
    """Run RFECV with logistic regression and report what survived."""
    estimator = LogisticRegression(max_iter=5000, solver="liblinear")
    selector = RFECV(
        estimator=estimator,
        step=step,  # drop 1 feature per pruning round
        min_features_to_select=1,  # never prune below 1 feature
        cv=cv,  # inner cross-validation splitter
        scoring=scoring,  # metric RFECV maximises
        n_jobs=-1,
    )  # parallelise the folds
    selector.fit(X_train, y_train)  # explores every subset size

    support = selector.get_support()  # boolean mask: True = kept
    kept = list(X_train.columns[support])
    dropped = list(X_train.columns[~support])
    print(f"\nRFECV chose {len(kept)} of {X_train.shape[1]} features")
    print(f"  KEPT   ({len(kept)}): {', '.join(kept)}")
    print(f"  DROPPED({len(dropped)}): {', '.join(dropped)}")
    return selector


# ---------------------------------------------------------------------------
# SECTION 4 - Plot the CV curve (the whole point of RFECV)
# ---------------------------------------------------------------------------
def plot_cv_curve(selector, title, fname):
    """Mean +/- std validation score against the number of features kept."""
    scores = selector.cv_results_["mean_test_score"]  # one score per candidate size
    stds = selector.cv_results_["std_test_score"]  # its fold-to-fold spread
    min_f = selector.min_features_to_select
    n_feature_range = np.arange(min_f, min_f + len(scores))  # x-axis labels
    best_n = int(n_feature_range[np.argmax(scores)])  # the winning size
    best_score = scores.max()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.errorbar(
        n_feature_range,
        scores,
        yerr=stds,
        marker="o",
        capsize=3,
        linewidth=1.2,
        color="#264653",
    )  # curve + error bars
    ax.axvline(
        best_n,
        color="crimson",
        linestyle="--",
        label=f"best: {best_n} features (AUC {best_score:.3f})",
    )
    ax.set_xlabel("Number of features kept")
    ax.set_ylabel("Cross-validated ROC-AUC")
    ax.set_title(title)
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)
    save_fig(fname)  # write to ./plots/ first...
    plt.show()  # ...then display
    return best_n, best_score


# ---------------------------------------------------------------------------
# SECTION 5 - Plot the feature ranking
# ---------------------------------------------------------------------------
def plot_rankings(selector, feature_names, title, fname, top_k=20):
    """Horizontal bar chart of RFE ranks (1 = kept, higher = eliminated earlier)."""
    support = selector.get_support()  # True for the surviving features
    ranking = selector.ranking_  # 1 = kept, 2 = dropped first, ...

    order = np.argsort(ranking, kind="stable")[:top_k]  # best features first
    names = [feature_names[i] for i in order]
    ranks = ranking[order]
    colors = ["#2a9d8f" if support[i] else "#e76f51" for i in order]

    fig, ax = plt.subplots(figsize=(8, 0.34 * len(names) + 1.6))
    ax.barh(np.arange(len(names)), ranks, color=colors)  # one bar per feature
    ax.set_yticks(np.arange(len(names)))
    ax.set_yticklabels(names, fontsize=8)
    ax.invert_yaxis()  # best feature at the top
    ax.set_xlabel("RFE ranking  (1 = kept, 2 = dropped first, ...)")
    ax.set_title(title)
    ax.grid(alpha=0.3, axis="x")
    save_fig(fname)
    plt.show()


# ---------------------------------------------------------------------------
# SECTION 6 - Refit on the subset and compare on the held-out test set
# ---------------------------------------------------------------------------
def compare_full_vs_selected(X_train_s, X_test_s, y_train, y_test, selector):
    """Two models, same test set: all features vs the RFECV subset."""
    support = selector.get_support()
    X_train_sel = X_train_s.loc[:, support]  # keep only selected columns
    X_test_sel = X_test_s.loc[:, support]

    rows = []
    for label, Xtr, Xte in [
        ("all features", X_train_s, X_test_s),
        ("RFECV subset", X_train_sel, X_test_sel),
    ]:
        clf = LogisticRegression(max_iter=5000, solver="liblinear")
        clf.fit(Xtr, y_train)  # train on the training part
        proba = clf.predict_proba(Xte)[:, 1]  # probability of the positive class
        pred = clf.predict(Xte)  # hard 0/1 prediction
        rows.append(
            {
                "model": f"{label} ({Xtr.shape[1]} feats)",
                "accuracy": accuracy_score(y_test, pred),
                "roc_auc": roc_auc_score(y_test, proba),
            }
        )

    df = pd.DataFrame(rows)
    print("\nHold-out comparison")
    print(df.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    x = np.arange(len(df))
    width = 0.35
    ax.bar(x - width / 2, df["accuracy"], width, label="Accuracy", color="#2a9d8f")
    ax.bar(x + width / 2, df["roc_auc"], width, label="ROC-AUC", color="#e9c46a")
    ax.set_xticks(x)
    ax.set_xticklabels(df["model"])
    ax.set_ylim(0.85, 1.005)  # zoom in: both models are already good
    ax.set_ylabel("Score on held-out test set")
    ax.set_title("Fewer features, same (or better) accuracy")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")
    save_fig("05_full_vs_selected.png")
    plt.show()
    return df


# ---------------------------------------------------------------------------
# SECTION 7 - Sanity check on data where we KNOW the answer
# ---------------------------------------------------------------------------
def demo_synthetic_ground_truth(
    n_samples=800, n_features=25, n_informative=5, n_redundant=5
):
    """Synthetic data with 10 relevant + 15 pure-noise features.

    shuffle=False keeps the layout predictable: columns 0..4 are informative,
    columns 5..9 are linear combinations of them, columns 10..24 are noise.
    """
    X_arr, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_informative,  # 5 features that truly drive the label
        n_redundant=n_redundant,  # 5 linear combos of the informative ones
        n_repeated=0,  # no duplicated columns
        n_clusters_per_class=1,
        class_sep=1.0,  # class separation
        flip_y=0.01,  # 1% random label noise
        shuffle=False,  # keep informative columns first
        random_state=RANDOM_STATE,
    )
    features = [f"f{i:02d}" for i in range(n_features)]
    X = pd.DataFrame(X_arr, columns=features)

    relevant = np.zeros(n_features, dtype=bool)
    relevant[: n_informative + n_redundant] = True  # the 10 "true" features

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    selector = RFECV(
        estimator=RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE),
        step=1,  # remove one feature per round
        min_features_to_select=1,
        cv=cv,
        scoring="roc_auc",
        n_jobs=-1,
    )
    selector.fit(X, y)
    selected = selector.get_support()  # what RFECV actually kept

    tp = int((selected & relevant).sum())  # real feature, kept
    fp = int((selected & ~relevant).sum())  # noise, kept
    fn = int((~selected & relevant).sum())  # real feature, missed
    print(
        f"\nSynthetic ground truth: {n_features} columns, "
        f"{relevant.sum()} truly relevant"
    )
    print(f"  correctly kept : {tp}")
    print(f"  spurious kept  : {fp}")
    print(f"  missed relevant: {fn}")
    print(f"  correctly dropped noise: {int((~selected & ~relevant).sum())}")

    colours = []
    for i in range(n_features):
        if selected[i] and relevant[i]:
            colours.append("#2a9d8f")  # kept a real feature
        elif selected[i] and not relevant[i]:
            colours.append("#e9c46a")  # kept noise (false positive)
        elif not selected[i] and relevant[i]:
            colours.append("#e76f51")  # missed a real feature
        else:
            colours.append("#adb5bd")  # correctly dropped noise

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.bar(range(n_features), np.ones(n_features), color=colours)
    ax.axvline(
        n_informative + n_redundant - 0.5, color="black", linestyle="--", linewidth=1
    )  # border of "real"
    ax.text(n_features - 0.5, 1.08, "pure noise ->", ha="right", fontsize=8)
    ax.set_yticks([])
    ax.set_xticks(range(n_features))
    ax.set_xticklabels(features, rotation=90, fontsize=8)
    ax.set_title("RFECV on synthetic data: what it kept vs. what is truly relevant")
    ax.grid(alpha=0.3, axis="x")
    ax.legend(
        handles=[
            Patch(color="#2a9d8f", label="real & kept"),
            Patch(color="#e9c46a", label="noise & kept (false positive)"),
            Patch(color="#e76f51", label="real & dropped (missed)"),
            Patch(color="#adb5bd", label="noise & dropped"),
        ],
        loc="upper center",
        ncol=4,
        fontsize=8,
        bbox_to_anchor=(0.5, -0.35),
    )
    save_fig("04_synthetic_ground_truth.png")
    plt.show()
    return selector, selected, relevant


# ---------------------------------------------------------------------------
# SECTION 8 - The trap: selection must happen INSIDE the CV loop
# ---------------------------------------------------------------------------
def demo_selection_bias():
    """Show numerically why you must not select features on the full dataset first.

    Many noise features + few samples = the selection step can 'peek' at the
    labels of the points it is later scored on. The resulting score is
    optimistic and will not reproduce in production.
    """
    X_arr, y = make_classification(
        n_samples=200,
        n_features=60,
        n_informative=2,
        n_redundant=0,
        n_repeated=0,
        n_clusters_per_class=1,
        class_sep=0.8,
        flip_y=0.10,
        random_state=RANDOM_STATE,
    )
    X = pd.DataFrame(X_arr, columns=[f"f{i:02d}" for i in range(X_arr.shape[1])])

    outer_cv = RepeatedStratifiedKFold(
        n_splits=5, n_repeats=3, random_state=RANDOM_STATE
    )  # honest evaluator
    inner_cv = StratifiedKFold(
        n_splits=5, shuffle=True, random_state=RANDOM_STATE
    )  # inside RFECV
    base = LogisticRegression(max_iter=5000, solver="liblinear")

    # ---- (A) HONEST: the scaler + RFECV + model chain lives inside each fold
    honest_pipe = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "rfecv",
                RFECV(
                    estimator=LogisticRegression(max_iter=5000, solver="liblinear"),
                    step=5,
                    min_features_to_select=1,
                    cv=inner_cv,
                    scoring="roc_auc",
                    n_jobs=-1,
                ),
            ),
            ("clf", LogisticRegression(max_iter=5000, solver="liblinear")),
        ]
    )
    honest = cross_val_score(
        honest_pipe, X, y, cv=outer_cv, scoring="roc_auc", n_jobs=-1
    )

    # ---- (B) OPTIMISTIC (WRONG): pick features on ALL data, then cross-validate
    peek_pipe = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "rfecv",
                RFECV(
                    estimator=LogisticRegression(max_iter=5000, solver="liblinear"),
                    step=5,
                    min_features_to_select=1,
                    cv=inner_cv,
                    scoring="roc_auc",
                    n_jobs=-1,
                ),
            ),
        ]
    )
    X_selected = peek_pipe.fit_transform(X, y)  # <-- leaks: it saw every label
    optimistic = cross_val_score(
        base, X_selected, y, cv=outer_cv, scoring="roc_auc", n_jobs=-1
    )

    print("\nSelection-bias demo (60 features, only 2 informative, n=200)")
    print(
        f"  honest  (RFECV inside each fold) : {honest.mean():.4f} "
        f"+/- {honest.std():.4f}"
    )
    print(
        f"  leaked  (RFECV before the folds): {optimistic.mean():.4f} "
        f"+/- {optimistic.std():.4f}"
    )
    print(
        f"  inflated by                     : "
        f"{(optimistic.mean() - honest.mean()):+.4f} ROC-AUC"
    )
    print("  -> The leaked number is fiction. Always nest the selector.")

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.boxplot(
        [honest, optimistic],
        tick_labels=["honest\n(selector nested)", "leaked\n(selector outside CV)"],
    )
    ax.set_ylabel("Cross-validated ROC-AUC")
    ax.set_title("Feature selection inside vs. outside the CV loop")
    ax.grid(alpha=0.3, axis="y")
    save_fig("06_selection_bias.png")
    plt.show()
    return honest, optimistic


# ---------------------------------------------------------------------------
# SECTION 9 - Plain RFE for contrast
# ---------------------------------------------------------------------------
def demo_plain_rfe(X_train, y_train, n_features_to_select=10):
    """Plain RFE: you choose the size, it chooses the features."""
    rfe = RFE(
        estimator=LogisticRegression(max_iter=5000, solver="liblinear"),
        n_features_to_select=n_features_to_select,  # YOU decide the size
        step=1,
    )  # drop one per round
    rfe.fit(X_train, y_train)
    kept = list(X_train.columns[rfe.get_support()])
    print(f"\nPlain RFE with n_features_to_select={n_features_to_select}")
    print(f"  kept: {', '.join(kept)}")
    print("  (RFE has no idea whether 10 is the RIGHT number - that is RFECV's job.)")
    return rfe


# ---------------------------------------------------------------------------
# SECTION 10 - Driver
# ---------------------------------------------------------------------------
def main():
    ensure_plots_dir()  # make ./plots/ if it is missing
    pd.set_option("display.width", 140)  # keep printed tables readable

    print("=" * 72)
    print("PART A - RFECV on the breast-cancer dataset")
    print("=" * 72)
    X, y = load_breast_cancer_data()
    X_train_s, X_test_s, y_train, y_test = prepare_data(X, y)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    baseline_cv(X_train_s, y_train, cv)  # all 30 features
    selector = run_rfecv(X_train_s, y_train, cv, scoring="roc_auc", step=1)

    best_n, best_score = plot_cv_curve(
        selector,
        "RFECV: validation ROC-AUC vs. number of features (breast cancer)",
        "01_cv_curve.png",
    )
    print(f"  -> peak at {best_n} features, mean ROC-AUC {best_score:.4f}")

    plot_rankings(
        selector,
        list(X_train_s.columns),
        "RFE ranking of all 30 features (green = kept)",
        "02_feature_ranking.png",
    )

    compare_full_vs_selected(X_train_s, X_test_s, y_train, y_test, selector)
    demo_plain_rfe(X_train_s, y_train, n_features_to_select=10)

    print("\n" + "=" * 72)
    print("PART B - Does RFECV find features we KNOW are real?")
    print("=" * 72)
    demo_synthetic_ground_truth()

    print("\n" + "=" * 72)
    print("PART C - Why the selector must live inside the CV loop")
    print("=" * 72)
    demo_selection_bias()

    print("\nDone. All figures are in ./plots/")


if __name__ == "__main__":
    main()
