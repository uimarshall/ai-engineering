# Recursive Feature Elimination with Cross-Validation (RFECV)

### _Cleaning & Preparing Data for ML — Practical Guide #7_

> **One-line summary:** RFECV is a _wrapper_ feature-selection method that keeps
> training your model, deleting the least useful feature again and again, and uses
> cross-validation to decide **exactly how many features to keep**.

---

## 1. The problem: more features ≠ better model

Imagine you are predicting whether a customer will churn. You have 300 columns:
age, tenure, monthly spend … plus 280 columns of barely-relevant survey answers
and log counters.

Every extra feature:

| Cost            | Why it matters                                                              |
| --------------- | --------------------------------------------------------------------------- |
| **Noise**       | Irrelevant columns let the model memorise random quirks (overfitting).      |
| **Time**        | Training, tuning and scoring get slower.                                    |
| **Data hunger** | With n samples and p features you need roughly 10–20 samples _per_ feature. |
| **Fragility**   | Correlated columns make coefficients unstable and hard to explain.          |
| **Money**       | Every extra sensor/column can cost real money to collect and clean.         |

**Feature selection** = choosing the smallest subset of columns that keeps (or
improves) predictive performance.

### The three families of feature selection

| Family       | Idea                                                   | Examples                                                  | Speed               |
| ------------ | ------------------------------------------------------ | --------------------------------------------------------- | ------------------- |
| **Filter**   | Score each feature on its own, ignore the model        | variance threshold, univariate `SelectKBest`, correlation | ⚡ very fast        |
| **Wrapper**  | Use the model itself as the judge, try feature subsets | **RFE**, **RFECV**, forward/backward selection            | 🐢 slow, often best |
| **Embedded** | The model ranks features while training                | Lasso (L1), tree `feature_importances_`                   | ⚡🐢 medium         |

RFECV is a **wrapper**: it wraps _any_ scikit-learn estimator around a loop.

---

## 2. Step 1 — plain RFE (Recursive Feature Elimination)

**Plain RFE** = "you tell me how many features to keep; I'll tell you which."

### How the loop works

1. Fit the model on all `p` features.
2. Read each feature's importance from the fitted model.
3. Delete the `step` least-important feature(s).
4. Go back to step 1 with the survivors.
5. Stop when `n_features_to_select` remain.

### Where does "importance" come from?

```
Linear models (LogisticRegression, LinearSVC, Ridge):
        importance_j = |coef_j|                    (absolute size of the fitted weight)

Tree ensembles (RandomForest, GradientBoosting):
        importance_j = mean decrease in impurity (Gini/MDI) contributed by splits on feature j

Other models (SVM with RBF, KNN):
        importance undefined -> supply importance_getter="auto"       (uses coef_ / feature_importances_)
        or importance_getter="named_steps.clf.coef_" inside a Pipeline
        or importance_getter=lambda est: permutation_importance(...)  (permutation importance)
```

### Tiny worked example (p = 4 features)

| Iteration | Features alive | `                     | coef | ` ranking | Dropped | `ranking_` value |
| --------- | -------------- | --------------------- | ---- | --------- | ------- | ---------------- |
| 1         | f1 f2 f3 f4    | f2 > f1 > f3 > **f4** | f4   | 4         |
| 2         | f1 f2 f3       | f1 > f3 > **f2**      | f2   | 3         |
| 3         | f1 f3          | f1 > f3 (both kept)   | –    | 1, 1      |

`ranking_[j] = 1` means **kept**; `ranking_[j] = k` (>1) means "eliminated in
round k". So a _lower_ rank is a _better_ feature.

### The catch

RFE cannot tell you the right `n_features_to_select`. Pick 5 and you may throw
away signal; pick 50 and you keep junk. You need to **measure** it → that's the CV part.

---

## 3. Step 2 — RFECV: let cross-validation choose the size

**RFECV** runs the whole RFE path _inside_ cross-validation and keeps the subset
size that gave the best validation score.

### The objective it maximises

```
                    K
  best_k  =  argmax   (1/K) * SUM  score( f_Sk(TRAIN_i) , TEST_i )
               k        i=1
```

Broken down piece by piece:

| Symbol          | Meaning                                                                                  |
| --------------- | ---------------------------------------------------------------------------------------- |
| `k`             | number of features kept — the knob we are searching over                                 |
| `K`             | number of CV folds (e.g. 5 or 10)                                                        |
| `S_k`           | the subset of `k` surviving features after RFE has pruned down to `k`                    |
| `f_Sk(TRAIN_i)` | a **freshly fitted** model, using only subset `S_k`, trained on fold `i`'s training part |
| `TEST_i`        | fold `i`'s held-out part — never seen during fitting                                     |
| `score(...)`    | `scoring` parameter, e.g. `"roc_auc"`, `"accuracy"`, `"f1"`, `"neg_mean_squared_error"`  |
| `1/K * SUM`     | average over folds = the cross-validated score for size `k`                              |
| `argmax_k`      | choose the `k` whose average score is highest                                            |

Crucially, the model is **refit from scratch on every fold** — no leakage.

### The trick that makes it affordable

RFE already produces a _nested_ sequence of subsets:

```
p features  ⊃  (p - step) features  ⊃  (p - 2*step) features  ⊃ ... ⊃  min_features_to_select
```

Because each subset is a subset of the previous one, **one single RFE pass gives
you every candidate `k`**. RFECV only has to cross-validate the path once.

### Cost formula

```
number of model fits  ≈  ceil( (p - min_features_to_select) / step )  ×  K
```

Example: p = 30, step = 1, K = 5 → ~145 fits. p = 500, step = 1, K = 10 → ~5,000 fits.
That is why `step > 1` matters on wide datasets.

---

## 4. The RFECV API — the parameters that matter

| Parameter                | Default                  | What to set it to                                                                                                          |
| ------------------------ | ------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| `estimator`              | —                        | The model you will actually use. Must expose `coef_` **or** `feature_importances_` — or you must pass `importance_getter`. |
| `step`                   | `1`                      | `1` = finest & slowest. Use `3`–`10`, or a **float** like `0.1` to remove 10% of remaining features per round.             |
| `min_features_to_select` | `1`                      | Lowest `k` RFE is allowed to reach. Set `1` normally; set higher if you must ship ≥ N columns.                             |
| `cv`                     | `5` (or 5-fold in `1.5`) | An int or a `StratifiedKFold` object. **Use a shuffled stratified splitter for classification.**                           |
| `scoring`                | `estimator.score`        | Pick the metric that matches the business goal: `"roc_auc"`, `"average_precision"`, `"neg_mean_squared_error"`, `"r2"`…    |
| `n_jobs`                 | `None`                   | `-1` to parallelise the folds across CPU cores.                                                                            |
| `importance_getter`      | `"auto"`                 | For pipelines or exotic models.                                                                                            |

**Attributes you read afterwards**

| Attribute      | Meaning                                                                            |
| -------------- | ---------------------------------------------------------------------------------- |
| `support_`     | Boolean mask, `True` = kept feature (use with `X.columns[support_]`).              |
| `ranking_`     | Integer rank per feature; `1` = kept.                                              |
| `n_features_`  | Number of kept features (recent scikit-learn: prefer `get_support().sum()`).       |
| `cv_results_`  | `mean_test_score`, `std_test_score`, `split*_test_score` for every candidate size. |
| `estimator_`   | The estimator **already refit on the winning subset**.                             |
| `transform(X)` | Returns `X` with only the kept columns — drop-in pipeline step.                    |

---

## 5. Hands-on walkthrough

Install once: `pip install scikit-learn pandas numpy matplotlib`

The code blocks below are numbered, contiguous, and concatenate into the
companion script `recursive_feature_elimination_with_cross_validation.py`.
We use **sklearn's bundled breast-cancer dataset** (569 patients, 30 numeric
features, binary target) so nothing is downloaded.

### Block 1 — Imports and configuration

```python
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer, make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE, RFECV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.model_selection import (RepeatedStratifiedKFold, StratifiedKFold,
                                     cross_val_score, train_test_split)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

PLOTS_DIR = "plots"
RANDOM_STATE = 42


def ensure_plots_dir():
    """Create ./plots once so every savefig() call has somewhere to write."""
    os.makedirs(PLOTS_DIR, exist_ok=True)


def save_fig(name):
    """Save the active figure to ./plots/<name> BEFORE plt.show() clears it."""
    path = os.path.join(PLOTS_DIR, name)
    plt.savefig(path, dpi=120, bbox_inches="tight")
    print(f"  [saved] {path}")
```

### Block 2 — Load the data and split it

```python
def load_breast_cancer_data():
    """Load sklearn's bundled dataset as a DataFrame (works offline)."""
    bunch = load_breast_cancer(as_frame=True)
    X = bunch.data          # 569 rows x 30 numeric features
    y = bunch.target        # 1 = benign, 0 = malignant
    print(f"Dataset shape: {X.shape[0]} rows x {X.shape[1]} features")
    print(f"Class balance: {np.bincount(y)}  (0 = malignant, 1 = benign)")
    return X, y


def prepare_data(X, y, test_size=0.25):
    """Stratified train/test split, then scale - fitting the scaler on TRAIN only."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=RANDOM_STATE)

    scaler = StandardScaler()
    X_train_s = pd.DataFrame(scaler.fit_transform(X_train),
                             columns=X.columns, index=X_train.index)
    X_test_s = pd.DataFrame(scaler.transform(X_test),
                            columns=X.columns, index=X_test.index)
    print(f"Train: {X_train_s.shape} | Test: {X_test_s.shape}")
    return X_train_s, X_test_s, y_train, y_test
```

> **Why scale?** RFE reads `|coef_|`, and unscaled columns (one has range
> 0–2500, another 0–0.1) produce coefficients on incomparable scales. Scaling
> first makes the ranking fair. Logistic regression also converges faster.

### Block 3 — Baseline: what does _all 30 features_ score?

```python
def baseline_cv(X_train, y_train, cv, scoring="roc_auc"):
    """Cross-validated score using every feature - our number to beat."""
    model = LogisticRegression(max_iter=5000, solver="liblinear")
    scores = cross_val_score(model, X_train, y_train, cv=cv,
                             scoring=scoring, n_jobs=-1)
    print(f"Baseline (all {X_train.shape[1]} features) "
          f"{scoring} = {scores.mean():.4f} +/- {scores.std():.4f}")
    return scores
```

### Block 4 — Run RFECV

```python
def run_rfecv(X_train, y_train, cv, scoring="roc_auc", step=1):
    """Run RFECV with logistic regression and report what survived."""
    estimator = LogisticRegression(max_iter=5000, solver="liblinear")
    selector = RFECV(estimator=estimator,
                     step=step,                      # drop 1 feature per round
                     min_features_to_select=1,       # never go below 1
                     cv=cv,                          # inner cross-validation
                     scoring=scoring,                # metric RFECV maximises
                     n_jobs=-1)                      # parallel folds
    selector.fit(X_train, y_train)

    support = selector.get_support()
    kept = list(X_train.columns[support])
    dropped = list(X_train.columns[~support])
    print(f"\nRFECV chose {len(kept)} of {X_train.shape[1]} features")
    print(f"  KEPT   ({len(kept)}): {', '.join(kept)}")
    print(f"  DROPPED({len(dropped)}): {', '.join(dropped)}")
    return selector
```

### Block 5 — Plot the CV curve (the whole point of RFECV)

```python
def plot_cv_curve(selector, title, fname):
    """Mean +/- std validation score against the number of features kept."""
    scores = selector.cv_results_["mean_test_score"]
    stds = selector.cv_results_["std_test_score"]
    min_f = selector.min_features_to_select
    n_feature_range = np.arange(min_f, min_f + len(scores))
    best_n = int(n_feature_range[np.argmax(scores)])
    best_score = scores.max()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.errorbar(n_feature_range, scores, yerr=stds, marker="o", capsize=3,
                linewidth=1.2, color="#264653")
    ax.axvline(best_n, color="crimson", linestyle="--",
               label=f"best: {best_n} features (AUC {best_score:.3f})")
    ax.set_xlabel("Number of features kept")
    ax.set_ylabel("Cross-validated ROC-AUC")
    ax.set_title(title)
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)
    save_fig(fname)
    plt.show()
    return best_n, best_score
```

**How to read it:** flat-left → you removed features that carried no signal.
Rising-right → you were drowning in noise features. A steep drop at the very
right → the last few features are genuinely useful. The peak is the sweet spot,
and the error bars tell you whether a difference of 1–2 features is even real.

### Block 6 — Plot the feature ranking

```python
def plot_rankings(selector, feature_names, title, fname, top_k=20):
    """Horizontal bar chart of RFE ranks (1 = kept, higher = eliminated earlier)."""
    support = selector.get_support()
    ranking = selector.ranking_

    order = np.argsort(ranking, kind="stable")[:top_k]   # best features first
    names = [feature_names[i] for i in order]
    ranks = ranking[order]
    colors = ["#2a9d8f" if support[i] else "#e76f51" for i in order]

    fig, ax = plt.subplots(figsize=(8, 0.34 * len(names) + 1.6))
    ax.barh(np.arange(len(names)), ranks, color=colors)
    ax.set_yticks(np.arange(len(names)))
    ax.set_yticklabels(names, fontsize=8)
    ax.invert_yaxis()                                    # best at the top
    ax.set_xlabel("RFE ranking  (1 = kept, 2 = dropped first, ...)")
    ax.set_title(title)
    ax.grid(alpha=0.3, axis="x")
    save_fig(fname)
    plt.show()
```

### Block 7 — Refit on the subset and compare on the held-out test set

```python
def compare_full_vs_selected(X_train_s, X_test_s, y_train, y_test, selector):
    """Two models, same test set: all features vs the RFECV subset."""
    support = selector.get_support()
    X_train_sel = X_train_s.loc[:, support]
    X_test_sel = X_test_s.loc[:, support]

    rows = []
    for label, Xtr, Xte in [("all features", X_train_s, X_test_s),
                            ("RFECV subset", X_train_sel, X_test_sel)]:
        clf = LogisticRegression(max_iter=5000, solver="liblinear")
        clf.fit(Xtr, y_train)
        proba = clf.predict_proba(Xte)[:, 1]
        pred = clf.predict(Xte)
        rows.append({"model": f"{label} ({Xtr.shape[1]} feats)",
                     "accuracy": accuracy_score(y_test, pred),
                     "roc_auc": roc_auc_score(y_test, proba)})

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
    ax.set_ylim(0.85, 1.005)
    ax.set_ylabel("Score on held-out test set")
    ax.set_title("Fewer features, same (or better) accuracy")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")
    save_fig("05_full_vs_selected.png")
    plt.show()
    return df
```

### Block 8 — Sanity check on data where we KNOW the answer

```python
def demo_synthetic_ground_truth(n_samples=800, n_features=25,
                                n_informative=5, n_redundant=5):
    """Synthetic data with 10 relevant + 15 pure-noise features.

    shuffle=False keeps the layout predictable: columns 0..4 are informative,
    columns 5..9 are linear combinations of them, columns 10..24 are noise.
    """
    X_arr, y = make_classification(
        n_samples=n_samples, n_features=n_features,
        n_informative=n_informative, n_redundant=n_redundant, n_repeated=0,
        n_clusters_per_class=1, class_sep=1.0, flip_y=0.01,
        shuffle=False, random_state=RANDOM_STATE)
    features = [f"f{i:02d}" for i in range(n_features)]
    X = pd.DataFrame(X_arr, columns=features)

    relevant = np.zeros(n_features, dtype=bool)
    relevant[: n_informative + n_redundant] = True        # the 10 "true" features

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    selector = RFECV(estimator=RandomForestClassifier(n_estimators=200,
                                                      random_state=RANDOM_STATE),
                     step=1, min_features_to_select=1, cv=cv,
                     scoring="roc_auc", n_jobs=-1)
    selector.fit(X, y)
    selected = selector.get_support()

    tp = int((selected & relevant).sum())
    fp = int((selected & ~relevant).sum())
    fn = int((~selected & relevant).sum())
    print(f"\nSynthetic ground truth: {n_features} columns, "
          f"{relevant.sum()} truly relevant")
    print(f"  correctly kept : {tp}")
    print(f"  spurious kept  : {fp}")
    print(f"  missed relevant: {fn}")
    print(f"  correctly dropped noise: {int((~selected & ~relevant).sum())}")

    # Four-way coloured bar chart: TP / FP / FN / TN
    colours = []
    for i in range(n_features):
        if selected[i] and relevant[i]:
            colours.append("#2a9d8f")     # kept a real feature
        elif selected[i] and not relevant[i]:
            colours.append("#e9c46a")     # kept noise (false positive)
        elif not selected[i] and relevant[i]:
            colours.append("#e76f51")     # missed a real feature
        else:
            colours.append("#adb5bd")     # correctly dropped noise

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.bar(range(n_features), np.ones(n_features), color=colours)
    ax.axvline(n_informative + n_redundant - 0.5, color="black",
               linestyle="--", linewidth=1)
    ax.text(n_features - 0.5, 1.08, "pure noise ->", ha="right", fontsize=8)
    ax.set_yticks([])
    ax.set_xticks(range(n_features))
    ax.set_xticklabels(features, rotation=90, fontsize=8)
    ax.set_title("RFECV on synthetic data: what it kept vs. what is truly relevant")
    ax.grid(alpha=0.3, axis="x")

    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="#2a9d8f", label="real & kept"),
                       Patch(color="#e9c46a", label="noise & kept (false positive)"),
                       Patch(color="#e76f51", label="real & dropped (missed)"),
                       Patch(color="#adb5bd", label="noise & dropped")],
              loc="upper center", ncol=4, fontsize=8, bbox_to_anchor=(0.5, -0.35))
    save_fig("04_synthetic_ground_truth.png")
    plt.show()
    return selector, selected, relevant
```

### Block 9 — The trap: selection must happen INSIDE the CV loop

```python
def demo_selection_bias():
    """Show numerically why you must not select features on the full dataset first.

    Many noise features + few samples = the selection step can 'peek' at the
    labels of the points it is later scored on. The score you get is then
    optimistic and will not reproduce in production.
    """
    X_arr, y = make_classification(
        n_samples=200, n_features=60, n_informative=2, n_redundant=0,
        n_repeated=0, n_clusters_per_class=1, class_sep=0.8, flip_y=0.10,
        random_state=RANDOM_STATE)
    X = pd.DataFrame(X_arr, columns=[f"f{i:02d}" for i in range(X_arr.shape[1])])

    outer_cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3,
                                       random_state=RANDOM_STATE)
    inner_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    base = LogisticRegression(max_iter=5000, solver="liblinear")

    # ---- (A) HONEST: the whole scaler + RFECV + model chain lives inside each fold
    honest_pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("rfecv", RFECV(estimator=LogisticRegression(max_iter=5000,
                                                     solver="liblinear"),
                        step=5, min_features_to_select=1, cv=inner_cv,
                        scoring="roc_auc", n_jobs=-1)),
        ("clf", LogisticRegression(max_iter=5000, solver="liblinear")),
    ])
    honest = cross_val_score(honest_pipe, X, y, cv=outer_cv,
                             scoring="roc_auc", n_jobs=-1)

    # ---- (B) OPTIMISTIC (WRONG): pick features on ALL data, then cross-validate
    peek_pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("rfecv", RFECV(estimator=LogisticRegression(max_iter=5000,
                                                     solver="liblinear"),
                        step=5, min_features_to_select=1, cv=inner_cv,
                        scoring="roc_auc", n_jobs=-1)),
    ])
    X_selected = peek_pipe.fit_transform(X, y)     # <-- leaks: used every label
    optimistic = cross_val_score(base, X_selected, y, cv=outer_cv,
                                 scoring="roc_auc", n_jobs=-1)

    print("\nSelection-bias demo (60 features, only 2 informative, n=200)")
    print(f"  honest  (RFECV inside each fold) : {honest.mean():.4f} "
          f"+/- {honest.std():.4f}")
    print(f"  leaked  (RFECV before the folds): {optimistic.mean():.4f} "
          f"+/- {optimistic.std():.4f}")
    print(f"  inflated by                     : "
          f"{(optimistic.mean() - honest.mean()):+.4f} ROC-AUC")
    print("  -> The leaked number is fiction. Always nest the selector.")

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.boxplot([honest, optimistic], labels=["honest\n(selector nested)",
                                             "leaked\n(selector outside CV)"])
    ax.set_ylabel("Cross-validated ROC-AUC")
    ax.set_title("Feature selection inside vs. outside the CV loop")
    ax.grid(alpha=0.3, axis="y")
    save_fig("06_selection_bias.png")
    plt.show()
    return honest, optimistic
```

### Block 10 — A plain RFE for comparison, and the `__main__` driver

```python
def demo_plain_rfe(X_train, y_train, n_features_to_select=10):
    """Plain RFE: you choose the size, it chooses the features."""
    rfe = RFE(estimator=LogisticRegression(max_iter=5000, solver="liblinear"),
              n_features_to_select=n_features_to_select, step=1)
    rfe.fit(X_train, y_train)
    kept = list(X_train.columns[rfe.get_support()])
    print(f"\nPlain RFE with n_features_to_select={n_features_to_select}")
    print(f"  kept: {', '.join(kept)}")
    print("  (RFE has no idea whether 10 is the RIGHT number - that is RFECV's job.)")
    return rfe


def main():
    ensure_plots_dir()
    pd.set_option("display.width", 140)

    print("=" * 72)
    print("PART A - RFECV on the breast-cancer dataset")
    print("=" * 72)
    X, y = load_breast_cancer_data()
    X_train_s, X_test_s, y_train, y_test = prepare_data(X, y)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    baseline_cv(X_train_s, y_train, cv)

    selector = run_rfecv(X_train_s, y_train, cv, scoring="roc_auc", step=1)
    best_n, best_score = plot_cv_curve(
        selector,
        "RFECV: validation ROC-AUC vs. number of features (breast cancer)",
        "01_cv_curve.png")
    print(f"  -> peak at {best_n} features, mean ROC-AUC {best_score:.4f}")

    plot_rankings(selector, list(X_train_s.columns),
                  "RFE ranking of all 30 features (green = kept)",
                  "02_feature_ranking.png")
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
```

---

## 6. Reading your results like a practitioner

| What you see                            | What it means                                                          | What to do                                                    |
| --------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------- |
| CV curve flat from k = 8 to 30          | Features 9–30 add nothing                                              | Ship the 8-feature model; it is cheaper and more stable       |
| CV curve still climbing at the far left | You may have over-pruned (or the metric is noisy)                      | Re-run with `min_features_to_select=5`, use repeated CV       |
| Peak at `k = 1`                         | Warning sign: your CV is noisy or the task is nearly unpredictable     | Switch to repeated stratified CV, check for label leakage     |
| `ranking_` full of ties at 1            | Correlated/duplicate columns                                           | Handle collinearity first (drop one of each pair > 0.95 corr) |
| RFECV keeps an absurd feature           | That feature is a proxy for a data leak (an ID, a post-outcome column) | Audit the column, not the algorithm                           |
| Huge run time                           | `step=1` on hundreds of features                                       | Use `step=5`, or float `step=0.1`; use a cheaper estimator    |

### Pitfalls to memorise

1. **Always nest the selector.** Scale, impute and select **inside** the CV
   fold (a `Pipeline` does this for you). Selecting on all data inflates every
   downstream score — see Block 9.
2. **RFECV is not a hyper-parameter search for your model.** It selects a
   _subset size_. Tune your model's C / max_depth separately (inner loop or
   `GridSearchCV` around the pipeline).
3. **Correlated features**: RFE drops one of a twin pair, seemingly at random.
   That is fine for prediction, dangerous for _interpretation_ — use
   `feature_importances_` or permutation importance for the story.
4. **Non-linear importance ≠ linear importance.** `coef_`-driven RFE can miss
   features that only matter in interaction. Try a RandomForest estimator and
   compare the two selected subsets.
5. **Selection is data-dependent.** If you retrain monthly, store the selected
   column list and the metric; a re-run on new data may pick a different subset.
6. **Wrong metric, wrong subset.** Using `accuracy` on a 1:100 imbalanced
   dataset will happily keep features that predict the majority class only. Use
   `roc_auc`/`average_precision`.

---

## 7. Business / company use cases

| Company type                     | Scenario                                                  | Why RFECV earns its keep                                                                                     |
| -------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Retail bank / credit scoring** | 800 bureau + transaction columns → default risk           | Regulatory models must be _explainable and small_; RFECV trims to a defensible scorecard while tracking AUC. |
| **Telecom / SaaS**               | Churn prediction from 400 usage + support-ticket columns  | Cuts ETL, scoring cost and latency; fewer features = fewer things to break in production.                    |
| **Hospital / medtech**           | Sepsis early-warning from 200 lab values & vitals         | Fewer inputs = simpler clinician-facing dashboards and fewer false alarms.                                   |
| **Manufacturing (Industry 4.0)** | Predicting defects from 500 sensor channels               | Each extra sensor costs money and maintenance; RFECV tells you which 20 actually matter.                     |
| **Pharma / genomics**            | 20,000 gene-expression columns, 200 patients              | Wrapper methods handle correlated gene blocks better than univariate filters.                                |
| **Ad-tech / e-commerce**         | Click-through-rate with hundreds of embeddings/aggregates | Trims the feature-engineering pipeline so online inference latency stays inside the SLA.                     |
| **Insurance**                    | Claims fraud detection with heavily imbalanced labels     | With `scoring="average_precision"`, RFECV selects the subset that actually surfaces fraud.                   |

**Rule of thumb for a stakeholder conversation:** _"We can keep 97–100 % of the
model's accuracy with ~30 % of the columns — that is 30 % less data engineering,
30 % faster scoring, and a model your analysts can explain."_

---

## 8. Cheat sheet

```
Filter (variance, SelectKBest)      -> quick triage on 10,000+ columns
Embedded (Lasso, tree importances)  -> fast ranking + regularisation while training
RFE                                 -> you know how many features you can ship
RFECV                               -> you want the DATA to choose the subset size  <-- this note
Permutation importance              -> final model-free explanation for stakeholders
```

**Recommended production recipe**

```python
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("rfecv",  RFECV(LogisticRegression(max_iter=5000),
                     step=1, cv=StratifiedKFold(5, shuffle=True, random_state=0),
                     scoring="roc_auc", n_jobs=-1)),
    ("clf",    LogisticRegression(max_iter=5000)),
])
scores = cross_val_score(pipe, X, y, cv=StratifiedKFold(5, shuffle=True,
                                                        random_state=1),
                         scoring="roc_auc")
```

Selector **nested** inside the pipeline, pipeline **nested** inside the outer
CV → the score you report is the score you will get.

---

## 9. Key takeaways

1. RFE prunes features one round at a time using the model's own importances.
2. RFECV adds cross-validation to answer _"how many?"_ — it maximises the mean
   validation score along the pruning path.
3. One RFE path yields every candidate subset size, so RFECV costs
   `ceil((p - min)/step) x K` model fits, not a brute-force search.
4. Read `support_`, `ranking_`, `cv_results_` and the CV curve — the curve is
   the deliverable you show your team.
5. **Never** select features before the CV loop; always nest the selector in a
   pipeline.
6. Fewer features usually means faster, cheaper, more explainable models — and
   RFECV proves it with numbers instead of intuition.

---

_Previous: Univariate Feature Selection · Next: Feature Extraction vs. Feature Selection (PCA + LDA)_
