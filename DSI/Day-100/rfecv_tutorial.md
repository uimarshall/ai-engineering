# RFECV: Recursive Feature Elimination with Cross-Validation

`RFECV = Recursive Feature Elimination + Cross-Validation`.

It repeatedly trains a model, removes the least useful feature(s), and measures how well the model would score for every possible number of features using 5-fold cross-validation. It then keeps the feature count that performs best.

```python
from sklearn.feature_selection import RFECV

selector = RFECV(estimator=model, step=1, cv=5, scoring="roc_auc")
selector.fit(X, y)
X_selected = selector.transform(X)  # only the winning features
```

Typical payoff: 30 features -> 10 features with the same or better AUC, plus a model that is faster, cheaper to collect data for, and easier to explain.

---

## 1. Where this fits in "Cleaning and Preparing Data for ML"

A data-preparation pipeline looks roughly like this:

```text
raw data -> clean -> handle missing values -> encode categoricals -> scale
 -> ✨ SELECT FEATURES ✨ -> train model -> evaluate
```

Feature selection comes after cleaning and scaling and before model training. Its job is to remove columns that add noise, cost, or redundancy without adding predictive power.

### Three families of selectors

| Family | Idea | Example |
| --- | --- | --- |
| Filter | Rank features by a statistical score and ignore the model | SelectKBest, correlation |
| Embedded | The model itself zeroes out useless features | Lasso, tree importance |
| Wrapper | Train with different feature subsets and keep the best | RFE / RFECV |

`RFECV` is a wrapper method. It is more expensive than the others, but usually the most accurate because it measures feature usefulness in the actual model you plan to deploy.

---

## 2. The problem RFECV solves

Imagine a churn model with 120 columns. With a linear model:

- many columns carry almost no signal and become noise the model can latch onto, causing overfitting;
- many columns are near-copies of each other, creating multicollinearity and unstable coefficients;
- every column costs money to collect and maintain;
- stakeholders cannot read a 120-coefficient model.

The key question is not "which features are non-zero?" (that is what Lasso does), but:

> If I keep exactly `k` features, which `k` features give the best model, and what is the best `k`?

RFE answers "which `k`" for a given `k`. RFECV answers "what is the best `k`" at the same time.

---

## 3. How RFE works (the intuition)

Think of a football squad. You have 30 players and can field only 11. You do not know who the weakest player is until you actually play matches.

RFE does this:

1. Train the model on all features.
2. Ask the model which features it uses least.
   - For a linear model: the smallest absolute coefficient.
   - For a tree: the lowest feature importance.
3. Delete the weakest one (or the weakest step of them).
4. Repeat until you reach `min_features_to_select`.

Every deleted feature gets a ranking:

- `ranking = 1` -> survived to the end (selected)
- `ranking = 2` -> removed in the last elimination round
- `ranking = 3` -> removed one round earlier
- and so on

So `ranking` is "elimination order, reversed": smaller numbers are better.

For a linear model, the importance of feature `j` is roughly:

```text
importance_j = |beta_j|
```

The weakest feature is:

```text
argmin_{j in S} |beta_j|
```

Then:

```text
S <- S \ {weakest}
```

where `beta_j` is the coefficient learned by the model and `|beta_j|` uses absolute value because a large negative coefficient is just as useful as a large positive one.

> Important: because we compare the size of coefficients, the features must be on the same scale. Standardize first. Otherwise a feature measured in cents could look 100x more important than the same feature measured in euros.

---

## 4. What RFECV adds: the CV loop

Plain RFE has a flaw: it gives you a ranking but not the number of features to keep. People often keep "the top 10" out of habit. RFECV instead scans the whole elimination path and scores every prefix.

For each candidate size `k`:

```text
score(k) = (1 / K) * sum_{i=1..K} AUC(f_{S_k^(i)}, X_{S_k^(i)}, y^(i))
```

where:

- `k` is the number of features kept;
- `K` is the number of CV folds (here, 5);
- `f_{S_k^(i)}` is a fresh model trained on the `k` best features using every fold except fold `i`;
- `X_{S_k^(i)}, y^(i)` are the hold-out data for fold `i`.

The average across folds is the estimate, and the spread becomes the error bars.

Then:

```text
k_hat = argmax_k score(k)
```

and the final model is refit on all training data using those `k_hat` features.

### Why the CV loop matters

With 30 features, the difference between 12 and 13 features is often tiny. The CV scan tells you whether that difference is genuine signal or noise. If the curve is flat between 8 and 15 features, choose 8 because it is simpler and cheaper while being equally good.

---

## 5. Key parameters and attributes

### Parameters

| Parameter | Meaning | Practical advice |
| --- | --- | --- |
| `estimator` | The model used to judge importance | Must expose `coef_` or `feature_importances_` |
| `step` | How many features to drop each round | `1` is most accurate but slowest; `0.1` or `5` is faster but coarser |
| `min_features_to_select` | Lower bound | Set to `1` for exploration; a higher value forces a minimum |
| `cv` | Cross-validation strategy | Use `5`, `StratifiedKFold`, or `GroupKFold` |
| `scoring` | Metric to maximize | Examples: `roc_auc`, `f1`, `average_precision`, `neg_mean_squared_error` |
| `n_jobs` | Parallelism | `-1` uses all cores |
| `importance_getter` | Where to read importances from | Example: `"named_steps.clf.coef_"` for pipelines |

### Attributes after `.fit()`

| Attribute | Meaning |
| --- | --- |
| `selector.support_` | Boolean mask, `True` for kept features |
| `selector.ranking_` | `1` = kept, `2`, `3`, ... = elimination order |
| `selector.n_features_` | Number of features kept |
| `selector.cv_results_` | Table with mean score, std score, n_features, params |
| `selector.estimator_` | The refit model |

---

## 6. Practical example 1: breast cancer data (Logistic Regression)

We use `sklearn.datasets.load_breast_cancer`. This is a dataset with 569 patients, 30 numeric measurements, and a binary label. It ships with scikit-learn, so no internet is required.

### Code block 01 — imports, configuration, helpers

```python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer, make_classification
from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score,
)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFECV
from sklearn.metrics import roc_auc_score

RANDOM_STATE = 42
PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)


def save_and_show(fig, filename, dpi=150):
    """Save a matplotlib figure into ./plots/ and show it."""
    path = os.path.join(PLOTS_DIR, filename)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    plt.show()
    print(f"[saved] {path}")


def banner(title):
    """Print a clearly visible section header."""
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)
```

### Code block 02 — load, split, scale (in that order)

```python
def load_scaled_breast_cancer():
    """Load the breast-cancer data, split it, and standardize the features."""
    data = load_breast_cancer(as_frame=True)
    X = data.data
    y = data.target

    print(f"Rows x columns        : {X.shape[0]} x {X.shape[1]}")
    print(f"Missing values (total): {int(X.isna().sum().sum())}")
    print(f"Class balance         : {y.value_counts().to_dict()}")

    # Split BEFORE any scaling or selection -> test set stays untouched.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.25,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    scaler = StandardScaler()
    scaler.fit(X_train)

    X_train_s = pd.DataFrame(
        scaler.transform(X_train), columns=X.columns, index=X_train.index
    )
    X_test_s = pd.DataFrame(
        scaler.transform(X_test), columns=X.columns, index=X_test.index
    )
    return X_train_s, X_test_s, y_train, y_test
```

> Leakage alert: fitting the scaler on all data (or selecting features before splitting) leaks test information into training and makes your scores look better than reality. Always split first.

### Code block 03 — baseline: how good is "use everything"?

```python
def demo_1_breast_cancer():
    """RFECV with a logistic regression on the breast-cancer dataset."""
    banner("DEMO 1 - RFECV on breast-cancer data (Logistic Regression)")
    X_train, X_test, y_train, y_test = load_scaled_breast_cancer()

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    baseline = LogisticRegression(max_iter=5000, random_state=RANDOM_STATE)
    baseline_cv = cross_val_score(
        baseline, X_train, y_train,
        cv=cv,
        scoring="roc_auc",
        n_jobs=-1,
    )
    print(
        f"Baseline (30 features) -> CV AUC "
        f"{baseline_cv.mean():.4f} +/- {baseline_cv.std():.4f}"
    )
```

Expected output: roughly `0.994 ± 0.005`, which is already very high. This is exactly why RFECV's fine-grained curve matters more than eyeballing the model.

### Code block 04 — run RFECV

```python
rfecv = RFECV(
    estimator=LogisticRegression(max_iter=5000, random_state=RANDOM_STATE),
    step=1,
    min_features_to_select=1,
    cv=cv,
    scoring="roc_auc",
    n_jobs=-1,
)

rfecv.fit(X_train, y_train)

selected_features = X_train.columns[rfecv.support_].tolist()
n_selected = int(rfecv.support_.sum())
print(f"\nRFECV kept {n_selected} of {X_train.shape[1]} features:")
print(selected_features)
```

Typical result: around 14-17 features kept with a CV AUC around 0.995 — roughly half the columns but equivalent performance.

### Code block 05 — read the CV curve

```python
mean_scores = rfecv.cv_results_["mean_test_score"]
std_scores = rfecv.cv_results_["std_test_score"]

# x-axis values: number of features at each step
n_features = np.arange(1, len(mean_scores) + 1)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(n_features, mean_scores, marker="o", color="#1f77b4")
ax.fill_between(
    n_features,
    mean_scores - std_scores,
    mean_scores + std_scores,
    alpha=0.15,
)
ax.set_xlabel("Number of features")
ax.set_ylabel("CV ROC AUC")
ax.set_title("RFECV cross-validation curve")
ax.grid(True, linestyle="--", alpha=0.4)
save_and_show(fig, "rfecv_cv_curve_logreg.png")
```

This plot is often the most useful output. It shows the exact trade-off between size and score, making the final decision easy to justify in a presentation or report.

---

## 7. What RFECV is actually selecting

A good selector should:

- keep the informative features;
- allow some redundant features because they duplicate real signal;
- reject pure noise.

This is the central idea behind feature selection: we want a compact feature set that preserves predictive information without carrying useless complexity.

### Code block 08 — synthetic data + RFECV with a Random Forest

```python
def make_synthetic_data(n_samples=1200, n_informative=8, n_redundant=6,
                       n_noise=16, random_state=RANDOM_STATE):
    """Build a classification dataset where we know which features matter."""
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_informative + n_redundant + n_noise,
        n_informative=n_informative,
        n_redundant=n_redundant,
        n_repeated=0,
        n_clusters_per_class=2,
        class_sep=1.0,
        flip_y=0.02,
        shuffle=False,
        random_state=random_state,
    )

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
    """Check whether RFECV can recover the truly informative features."""
    banner("DEMO 2 - Can RFECV recover the ground-truth features?")
    X, y = make_synthetic_data()
    print(f"Dataset: {X.shape[0]} rows, {X.shape[1]} columns "
          f"(8 informative, 6 redundant, 16 noise)")

    rfecv = RFECV(
        estimator=RandomForestClassifier(
            n_estimators=150,
            random_state=RANDOM_STATE,
            n_jobs=1,
        ),
        step=2,
        min_features_to_select=2,
        cv=5,
        scoring="roc_auc",
        n_jobs=-1,
    )
    rfecv.fit(X, y)

    support = pd.Series(rfecv.support_, index=X.columns)
    kept = support[support].index.tolist()

    informative_kept = sum(name.startswith("informative") for name in kept)
    redundant_kept = sum(name.startswith("redundant") for name in kept)
    noise_kept = sum(name.startswith("noise") for name in kept)

    print(f"\nKept {len(kept)} features total:")
    print(f"  informative : {informative_kept}/8   <- the real signal")
    print(f"  redundant   : {redundant_kept}/6   <- duplicates of the signal")
    print(f"  noise       : {noise_kept}/16  <- pure randomness")
    print(f"Recall on the true drivers: {informative_kept / 8:.0%}")
    return informative_kept, redundant_kept, noise_kept, len(kept)
```

> Parallelism note: nesting `n_jobs=-1` inside RFECV and inside the RandomForest can cause thread oversubscription, which is slower, not faster. Parallelize at one level only — here, the folds.

### Code block 09 — plot the recovery

```python
categories = ["informative\n(true signal)", "redundant\n(signal copies)", "noise\n(useless)"]
totals = [8, 6, 16]
kept_counts = [informative_kept, redundant_kept, noise_kept]

x = np.arange(len(categories))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(x - width / 2, totals, width, label="available", color="#c7c7c7")
ax.bar(x + width / 2, kept_counts, width, label="kept by RFECV", color="#2ca02c")
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.set_ylabel("Number of features")
ax.set_title("RFECV keeps the signal and discards most of the noise")
ax.legend()
save_and_show(fig, "rfecv_synthetic_recovery.png")
```

Typical output: 8/8 informative kept, about 4/6 redundant kept, and 0-3/16 noise kept. That is the whole point: RFECV is aggressive with pure noise and conservative with anything correlated to the target.

---

## 8. The professional way: leakage-free nested CV

In example 1, we picked features on `X_train` and scored them on `X_test`. That is honest only because the test set never touched the selection process. But if you report "CV score after selection," the selection has already seen all the CV folds and your estimate becomes optimistically biased.

The fix is to put the scaler and RFECV inside a pipeline and then cross-validate the whole pipeline. Now selection happens afresh inside every outer fold in a nested cross-validation setup.

### Code block 10 — nested CV comparison

```python
def demo_3_nested_cv():
    """Compare 'all features' vs 'RFECV' inside a leak-proof pipeline."""
    banner("DEMO 3 - Leakage-free (nested) comparison of the two strategies")
    data = load_breast_cancer(as_frame=True)
    X, y = data.data, data.target
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    pipe_all = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=5000, random_state=RANDOM_STATE)),
    ])

    pipe_rfecv = Pipeline([
        ("scaler", StandardScaler()),
        ("rfecv", RFECV(
            estimator=LogisticRegression(max_iter=5000, random_state=RANDOM_STATE),
            step=1,
            min_features_to_select=1,
            cv=5,
            scoring="roc_auc",
        )),
        ("clf", LogisticRegression(max_iter=5000, random_state=RANDOM_STATE)),
    ])

    scores_all = cross_val_score(pipe_all, X, y, cv=cv, scoring="roc_auc", n_jobs=-1)
    scores_rfecv = cross_val_score(pipe_rfecv, X, y, cv=cv, scoring="roc_auc", n_jobs=-1)

    print(f"All 30 features : AUC {scores_all.mean():.4f} +/- {scores_all.std():.4f}")
    print(f"With RFECV      : AUC {scores_rfecv.mean():.4f} +/- {scores_rfecv.std():.4f}")
    print(f"Per-fold RFECV scores: {np.round(scores_rfecv, 4)}")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.boxplot([scores_all, scores_rfecv], tick_labels=["All features", "RFECV inside pipeline"])
    ax.scatter(np.ones_like(scores_all) + np.random.uniform(-0.05, 0.05, len(scores_all)),
               scores_all, color="#1f77b4", zorder=3)
    ax.scatter(np.ones_like(scores_rfecv) * 2 + np.random.uniform(-0.05, 0.05, len(scores_rfecv)),
               scores_rfecv, color="#2ca02c", zorder=3)
    ax.set_ylabel("ROC AUC")
    ax.set_title("Nested CV: honest estimate of the RFECV benefit")
    save_and_show(fig, "rfecv_nested_cv.png")

    return scores_all.mean(), scores_rfecv.mean()
```

The lesson: the nested numbers are usually a touch lower than the naive ones. That is not a failure — it is the truth, and it is the number you should put in a report or stakeholder deck.

---

## 9. Business / company use cases

| Company type | Problem | How RFECV helps |
| --- | --- | --- |
| Bank / fintech | Credit-scoring model on 200+ bureau variables; regulators demand interpretability | Shrink to 12-20 features, creating a readable scorecard and documented justification for each variable |
| Telco | Churn prediction from call records, app usage, support tickets | Fewer features means a cheaper nightly scoring job; a flat CV curve helps justify dropping expensive-to-compute features |
| Hospital / diagnostics | Predict disease from 40 possible lab tests | RFECV picks the 6 tests that actually matter, lowering cost per patient and turnaround time |
| Manufacturing | Predictive maintenance with 300 vibration/temperature sensors | Keep only the sensors that carry signal; fewer sensors to install and maintain |
| E-commerce | Conversion model using clickstream aggregates | Reduce to a small feature set and lower latency at prediction time |
| Insurance | Claims-severity regression | Use `scoring="neg_mean_squared_error"` to trim pricing variables |
| SaaS | Churn / upsell scoring inside a pipeline | Embed RFECV in a pipeline so retraining is automatic and leak-proof |

The recurring theme: RFECV pays for itself twice — once in model quality and robustness, and once in the cost of collecting and serving features.

---

## 10. Pitfalls, and how to avoid them

- Correlated features make rankings unstable. If "radius" and "perimeter" are 0.99 correlated, RFECV may drop one almost at random. Before RFECV, consider dropping pairs with `|corr| > 0.95`.
- Always scale before RFE with a linear model. Coefficient magnitude is scale-dependent.
- Never select features on the full dataset before splitting. That is textbook leakage. Use the pipeline approach from block 10.
- `step=1` is expensive. Cost is roughly `n_features * cv * model_fit`. For 500 features, use `step=0.05` or `step=10` to get a coarse curve first, then zoom in.
- Do not blindly trust "the best CV score." A plateau means "any of these are fine." Pick the smallest set. Reporting a 0.0005 AUC gain for 15 more features rarely survives contact with a new data batch.
- Tree importances are biased toward continuous/high-cardinality features. If that is a concern, try permutation-based approaches or a linear model / `SelectFromModel` with L1 (Lasso) as a cross-check.
- Grouped data needs grouped CV. Multiple visits per patient or orders per customer should use `GroupKFold`; otherwise the same entity can leak across folds.
- RFECV does not fix bad data. Missing values, unit errors, or leakage in the columns are upstream problems; clean first.
- Small datasets give noisy rankings. With a few hundred rows, the curve's error bars overlap heavily. Prefer domain knowledge plus a simple filter.
- Grid mismatch: do not select with `scoring="roc_auc"` and then deploy a model tuned for accuracy. Select using the metric you actually care about.

---

## 11. RFECV vs the alternatives

| Method | Cost | Uses the model? | Handles interactions? | Gives a feature count? | Best when |
| --- | --- | --- | --- | --- | --- |
| Correlation / SelectKBest | Very low | No | No | Manual | Quick first pass, 1000s of columns |
| SelectFromModel + Lasso | Low | Yes (embedded) | Partly | Manual / heuristic | Many features, want speed |
| Tree feature importances | Low | Yes (embedded) | Yes | Manual | Non-linear, quick ranking |
| RFE | Medium | Yes (wrapper) | Yes | No (you choose `k`) | You know roughly how many features you want |
| RFECV | High | Yes (wrapper) | Yes | Yes | Few hundred features, quality matters |
| Boruta | High | Yes (wrapper) | Yes | Yes | You want statistical "all-relevant" selection |

Interview-ready one-liner:

> "RFECV wraps RFE in a cross-validated search over the number of features, so the model itself decides both which features to keep and how many — at the cost of `n_features × cv` model fits."

---

## 12. Cheat sheet

```python
from sklearn.feature_selection import RFECV
from sklearn.linear_model import LogisticRegression

selector = RFECV(
    estimator=LogisticRegression(max_iter=5000),
    step=1,
    min_features_to_select=1,
    cv=5,
    scoring="roc_auc",
    n_jobs=-1,
)
selector.fit(X_train, y_train)

X_train_sel = selector.transform(X_train)
print(selector.support_)
print(selector.ranking_)
print(selector.n_features_)
print(selector.cv_results_)
```

### Checklist before you run it

- Data cleaned, missing values handled, categoricals encoded.
- Split done first; scaler fitted on training data only.
- Features on a comparable scale if using a linear model.
- Highly correlated pairs considered for removal.
- CV respects groups or time if your data has them.
- Final performance reported from nested CV or an untouched hold-out set.

---

## 13. How to run the script

```bash
pip install "scikit-learn>=1.0" pandas matplotlib numpy
python rfecv_tutorial.py
```

This works on Windows, macOS, and Linux, and no internet is required because both datasets are bundled with scikit-learn. Five PNG figures are saved under `./plots/`:

- `plots/rfecv_cv_curve_logreg.png` — score vs number of features
- `plots/rfecv_feature_ranking_logreg.png` — elimination order of every feature
- `plots/baseline_vs_rfecv_auc.png` — full vs reduced model
- `plots/rfecv_synthetic_recovery.png` — signal vs redundant vs noise
- `plots/rfecv_nested_cv.png` — leak-proof comparison

### Code block 11 — main entry point

```python
if __name__ == "__main__":
    summary = demo_1_breast_cancer()

    print("\n" + "-" * 72)
    print("SUMMARY - Demo 1")
    print(f"  features kept          : {summary['n_selected']} (from 30)")
    print(f"  CV AUC, all features   : {summary['cv_full']:.4f}")
    print(f"  CV AUC, RFECV features : {summary['cv_selected']:.4f}")
    print(f"  test AUC, all features : {summary['test_full']:.4f}")
    print(f"  test AUC, RFECV        : {summary['test_selected']:.4f}")
    print(f"  kept: {summary['selected_features']}")
    print("-" * 72)

    demo_2_synthetic()
    demo_3_nested_cv()

    print("\nAll figures were saved to ./plots/")
```

---

## Summary

RFECV is one of the most practical feature-selection tools when you want a model to decide both which variables matter and how many should remain. It is computationally heavier than simpler filtering methods, but for moderate-sized datasets it often delivers the best trade-off between performance, interpretability, and cost.

Use it when the feature set is moderate, the metric matters, and you want a defensible, data-driven answer to the question: "What is the smallest set of features that still performs well?"
