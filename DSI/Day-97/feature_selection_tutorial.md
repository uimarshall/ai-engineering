# Feature Selection in Machine Learning — A Practical Beginner's Guide

> Part of the *Cleaning and Preparing Data for ML* series. This note focuses on
> **feature selection**: choosing the most useful columns (features) from your
> dataset before training a model.

---

## 1. What is Feature Selection?

Your dataset often contains **many columns** (features), but not all of them are
useful. Some are:

- **Irrelevant** — e.g., a customer ID number tells the model nothing.
- **Redundant** — e.g., "height in cm" and "height in inches" repeat the same info.
- **Noisy** — e.g., random sensor errors that mislead the model.

**Feature selection = keeping only the features that actually help the model.**

### Why bother?

| Problem | How feature selection helps |
|---|---|
| **Overfitting** | Fewer features → simpler model → generalises better to new data. |
| **Slow training** | Less data to process → faster training and prediction. |
| **Hard to interpret** | A model using 5 features is easier to explain than one using 500. |
| **Curse of dimensionality** | With too many features and too few rows, models struggle to learn patterns. |

### The three families of methods

1. **Filter methods** — score each feature *independently* using statistics, then keep the best. Fast, but ignores feature interactions.
2. **Wrapper methods** — train the model, see which features it actually used, remove the useless ones, and repeat. More accurate, but slower.
3. **Embedded methods** — selection happens *during* training, built into the algorithm itself (e.g., Lasso, Random Forests). A nice middle ground.

---

## 2. Setup and a First Look at the Data

We use the **Breast Cancer Wisconsin** dataset built into scikit-learn. It has
569 patient records and 30 numeric features ( measurements of cell nuclei).

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler

# Load the built-in dataset and put it in a nice table (DataFrame)
cancer = load_breast_cancer(as_frame=True)
X = cancer.data          # the 30 feature columns
y = cancer.target        # the label: 0 = malignant, 1 = benign

print(f"Dataset shape: {X.shape}")   # (569, 30)
print(f"Any missing values? {X.isna().sum().sum()}")   # 0 -> data is already clean

# Split BEFORE selecting features so our choices are not biased by the test set.
# random_state=42 makes the split reproducible.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Many selection methods are sensitive to feature scale, so standardise
# (mean 0, std 1). We fit ONLY on the training data to avoid data leakage.
scaler = StandardScaler()
X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X.columns)
X_test_scaled  = pd.DataFrame(scaler.transform(X_test),  columns=X.columns)
```

**Key ideas in this block:**
- **Split first, select second.** If you select features using the whole
  dataset, information from the test set leaks into training and your results
  will look better than they really are.
- **Fit the scaler on the training set only** (`fit_transform` on train,
  `transform` on test) for the same reason.

---

## 3. Filter Methods (statistics-first, model-free)

### 3.1 Drop features with near-zero variance

A feature whose value barely changes (e.g., 98% identical values) carries
little information. `VarianceThreshold` removes them automatically.

```python
from sklearn.feature_selection import VarianceThreshold

selector = VarianceThreshold(threshold=0.01)        # drop features with variance < 0.01
X_train_var = selector.fit_transform(X_train_scaled)

kept = X.columns[selector.get_support()]            # columns that survived
print(f"Kept {len(kept)} of {X.shape[1]} features. Dropped: {set(X.columns) - set(kept)}")
```

On this dataset, nothing is dropped — all features vary enough. That's normal;
this tool shines on messier real-world data with constant ID-like columns.

### 3.2 Correlation — finding redundant features

When two features are highly correlated, they carry duplicate information.
A heatmap shows the full picture at a glance.

```python
corr = X_train_scaled.corr()

plt.figure(figsize=(12, 10))
plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar(label="correlation")
plt.xticks(range(len(corr)), corr.columns, rotation=90, fontsize=7)
plt.yticks(range(len(corr)), corr.columns, fontsize=7)
plt.title("Feature correlation matrix")
plt.tight_layout()
plt.show()
```

You'll notice some bright red blocks — e.g., `mean radius` correlates strongly
with `mean perimeter` and `mean area` (of course: they're all measures of size).
For linear models, one representative per block is often enough.

> ⚠️ High correlation is a problem mainly for *linear* models. Tree-based models
> don't mind it, but dropping duplicates still saves compute.

### 3.3 Mutual information — scoring each feature against the target

**Mutual information (MI)** measures how much knowing a feature reduces
uncertainty about the target. It catches **non-linear** relationships that
correlation misses. Values are ≥ 0; higher = more informative.

```python
from sklearn.feature_selection import mutual_info_classif, SelectKBest

# Compute MI between every feature and the label, using only TRAINING data
mi_scores = mutual_info_classif(X_train_scaled, y_train, random_state=42)
mi_series = pd.Series(mi_scores, index=X.columns).sort_values()

mi_series.plot.barh(figsize=(8, 8), title="Mutual information with target")
plt.xlabel("MI score")
plt.show()
```

Features like `worst concave points` and `worst perimeter` score high; features
like `fractal dimension (error)` score near zero and are candidates for removal.

To keep, say, the **top 10** features:

```python
top10 = SelectKBest(mutual_info_classif, k=10)
X_train_mi = top10.fit_transform(X_train_scaled, y_train)
X_test_mi  = top10.transform(X_test_scaled)

print("Top 10 features:", list(X.columns[top10.get_support()]))
```

---

## 4. Wrapper Methods (let the model decide)

Wrappers repeatedly train a model on different feature subsets and keep the
combination that performs best.

### 4.1 Recursive Feature Elimination (RFE)

RFE works like this:

1. Train the model on all features.
2. Rank features by importance; **remove the weakest one**.
3. Retrain on the remaining features. Repeat until only `n_features_to_select` remain.

```python
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=5000)

rfe = RFE(estimator=model, n_features_to_select=10, step=1)
rfe.fit(X_train_scaled, y_train)

rfe_features = X.columns[rfe.get_support()]
print("RFE selected:", list(rfe_features))
```

`step=1` removes one feature per round (safe, slower). Use `step=5` to remove
five at a time on very wide datasets.

### 4.2 How many features should I keep?

Instead of guessing, try a range and evaluate with cross-validation:

```python
results = {}
for k in [5, 10, 15, 20, 30]:
    rfe_k = RFE(LogisticRegression(max_iter=5000), n_features_to_select=k)
    scores = cross_val_score(rfe_k, X_train_scaled, y_train, cv=5, scoring="f1")
    results[k] = scores.mean()
    print(f"k={k:2d} -> F1 = {scores.mean():.4f}")
```

Pick the smallest `k` whose score is close to the best — a nice accuracy/
simplicity trade-off.

---

## 5. Embedded Methods (selection during training)

### 5.1 L1 regularisation (Lasso) — shrink useless features to exactly zero

Lasso adds a penalty that forces the coefficients of weak features to become
**exactly zero**, effectively selecting features for you. Works for
classification (`penalty="l1"`) and regression (`Lasso`).

```python
lasso = LogisticRegression(penalty="l1", solver="liblinear", C=0.1, max_iter=5000)
lasso.fit(X_train_scaled, y_train)

lasso_coefs = pd.Series(np.abs(lasso.coef_[0]), index=X.columns).sort_values()
lasso_coefs.plot.barh(figsize=(8, 8), title="|Lasso coefficients| (0 = dropped)")
plt.show()

print("Features kept (non-zero):", int((lasso.coef_[0] != 0).sum()), "of 30")
```

Smaller `C` = stronger penalty = fewer features kept. Tune it carefully!

### 5.2 Tree-based feature importance

Random Forests rank features by how much they reduce impurity (Gini) across
all trees. It's built in — no extra step needed.

```python
from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier(n_estimators=200, random_state=42)
forest.fit(X_train, y_train)   # trees don't need scaling

importances = pd.Series(forest.feature_importances_, index=X.columns).sort_values()
importances.plot.barh(figsize=(8, 8), title="Random Forest feature importance")
plt.show()
```

> ⚠️ Tree importances favour **continuous, high-cardinality** features. Treat
> them as a hint, not gospel — compare with MI or RFE.

---

## 6. Putting It All Together — A Clean, Leak-Free Pipeline

The professional way: wrap selection *inside* a scikit-learn `Pipeline`, so
scaling → selection → modelling happen inside each cross-validation fold.
No leakage, no manual steps.

```python
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

pipe = Pipeline([
    ("scaler",   StandardScaler()),                              # 1. scale
    ("select",   SelectKBest(mutual_info_classif, k=10)),        # 2. keep top 10 by MI
    ("model",    LogisticRegression(max_iter=5000)),             # 3. classify
])

pipe.fit(X_train, y_train)                       # train end-to-end
print(classification_report(y_test, pipe.predict(X_test),
                            target_names=["malignant", "benign"]))

# Cross-validated score of the WHOLE pipeline (honest estimate)
cv_score = cross_val_score(pipe, X, y, cv=5, scoring="f1").mean()
print(f"Cross-validated F1 of pipeline: {cv_score:.4f}")
```

---

## 7. Quick Reference — Which Method When?

| Situation | Recommended method |
|---|---|
| Very wide data (10,000+ features) | Variance threshold + mutual info (`SelectKBest`) |
| You suspect many redundant features | Correlation analysis / Lasso |
| You have time and want best accuracy | RFE or Sequential Feature Selector |
| You need an explainable model | Lasso or L1 logistic regression |
| Using Random Forest / Gradient Boosting | Built-in `feature_importances_` |
| Want a production-safe, leak-free setup | `Pipeline` with any selector above |

### Golden rules

1. **Always split before selecting**, or your evaluation will be dishonest.
2. **Fit selectors on training data only** — use `.transform()` on test data.
3. **Don't chase tiny accuracy gains** — 5 good features beat 30 messy ones.
4. **Domain knowledge beats statistics** — if a feature is medically/business
   meaningless, drop it regardless of its score.

---

## 8. Further Reading

- scikit-learn user guide: *Feature selection*
  (https://scikit-learn.org/stable/modules/feature_selection.html)
- Guyon & Elisseeff (2003), *"An Introduction to Variable and Feature Selection"*
- `mlxtend` library: `SequentialFeatureSelector`, handy feature-selection plots

*Companion code: every snippet above is collected, in order, in
`feature_selection_tutorial.py` with line-by-line comments.*
