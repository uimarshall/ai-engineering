# Feature Selection with the Correlation Matrix — A Practical Beginner's Guide

> Part of the series: _Cleaning and Preparing Data for Machine Learning_

## 1. What you will learn

By the end of this note you will be able to:

1. Explain what a correlation matrix is, in plain language.
2. Use it to **remove redundant features** (features that say the same thing).
3. Use it to **screen features that are actually related to your target**.
4. Turn the idea into a **reusable function** you can drop into any project.
5. Know the **pitfalls** so you don't misuse it.

---

## 2. The intuition (no math panic, promise)

**Correlation** measures how strongly two variables move together:

- **+1** → when one goes up, the other goes up (perfectly).
- **0** → they move independently — no linear relationship.
- **−1** → when one goes up, the other goes down (perfectly).

A **correlation matrix** is simply a table that shows the correlation between **every pair of columns** in your dataset. It always has 1.0 on the diagonal (a column is perfectly correlated with itself) and is mirrored top-left to bottom-right.

```javascript
            age    income   height
age         1.00   0.85     0.05
income      0.85   1.00     0.02
height      0.05   0.02     1.00
```

Reading it: `age` and `income` are strongly correlated (0.85) — they carry overlapping information. `height` is correlated with neither.

---

## 3. Why this matters for feature selection

Two practical problems in ML are solved with this one tool:

### Problem A — Redundant features (feature vs. feature)

If two input features are almost perfectly correlated, they are (almost) the same information twice. Keeping both:

- adds **no new signal**, but adds noise and training time,
- causes **multicollinearity** in linear models (unstable, hard-to-interpret coefficients),
- makes your model harder to explain and deploy.

**Fix:** from each highly correlated pair, keep one and drop the other.

### Problem B — Irrelevant features (feature vs. target)

If a feature has ~0 correlation with the target, it probably isn't helping a linear-style model predict anything.

**Fix:** rank features by absolute correlation with the target and keep the useful ones.

> ⚠️ **Heads up:** correlation only captures **linear** relationships. A feature can be hugely informative in a non-linear way yet show ~0 correlation. That's why this technique is a _screening/filter_, not a final verdict — and why tree-based models (which catch non-linearity) sometimes disagree with it.

---

## 4. The practical workflow

```javascript
Raw data
   │
   ├── 1. Compute correlation matrix (on numeric features)
   │
   ├── 2. Visualize as a heatmap → eyeball the structure
   │
   ├── 3. Drop redundant features  (|corr| between FEATURES > threshold, e.g. 0.8)
   │
   ├── 4. Rank features by |corr| with TARGET → drop the useless ones (optional)
   │
   └── 5. Train model BEFORE vs AFTER → confirm you didn't lose performance
```

**Golden rule: compute everything on the TRAINING SET ONLY.** If you compute the correlation matrix on the full dataset (including test data), information from your test set leaks into feature selection and your evaluation becomes optimistically biased.

---

## 5. Example 1 — Synthetic data (so you can _see_ the redundancy)

We build a small dataset with 5 features, where `x2` is just `x1` plus noise, `x4` is `x3` plus noise — deliberate redundancy — plus one informative feature `signal` and one useless one `noise`.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Reproducibility: same "random" numbers every run
rng = np.random.default_rng(seed=42)

n = 300                                          # number of rows

signal = rng.normal(0, 1, n)                     # genuinely informative feature
x1 = rng.normal(5, 2, n)                         # base feature
x2 = x1 + rng.normal(0, 0.1, n)                  # x2 ≈ x1 + tiny noise (REDUNDANT with x1)
x3 = rng.normal(10, 3, n)                        # another base feature
x4 = x3 + rng.normal(0, 0.1, n)                  # x4 ≈ x3 (REDUNDANT with x3)
noise = rng.normal(0, 1, n)                      # pure noise, tells us nothing

target = 3 * signal + 0.5 * x1 + rng.normal(0, 0.5, n)   # target depends on signal & x1

df = pd.DataFrame({"signal": signal, "x1": x1, "x2": x2,
                   "x3": x3, "x4": x4, "noise": noise,
                   "target": target})
```

**Step 1 — compute the matrix:**

```python
corr = df.corr()                    # Pearson correlation for every pair of columns
print(corr.round(2))                # .round(2) makes the table readable
```

**Step 2 — visualize it:**

```python
plt.figure(figsize=(7, 5))
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Correlation matrix")
plt.tight_layout()
plt.show()
```

You will literally see dark red squares at (x1, x2) and (x3, x4) — the redundancy jumps out of the picture.

**Step 3 — auto-drop redundant features:**

```python
def drop_correlated_features(data, threshold=0.8):
    # Drop one feature from every pair whose |correlation| exceeds threshold.
    corr_matrix = data.corr().abs()                             # absolute values: strength, not sign
    upper = corr_matrix.where(                                  # keep only the UPPER triangle...
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))  # ...so each pair is counted ONCE
    to_drop = [col for col in upper.columns                     # any column...
               if any(upper[col] > threshold)]                  # ...that correlates strongly with an earlier column
    return data.drop(columns=to_drop), to_drop                  # return clean data + what we dropped

X_reduced, dropped = drop_correlated_features(df.drop(columns="target"), threshold=0.8)
print("Dropped:", dropped)          # -> ['x2', 'x4']
print("Kept:  ", list(X_reduced.columns))
```

**Step 4 — rank what remains by usefulness to the target:**

```python
target_corr = df.corr()["target"].abs().sort_values(ascending=False)
print(target_corr)
```

Expect `signal` and `x1`/`x3` near the top and `noise` near the bottom. Drop anything below your relevance floor (e.g. < 0.05) if you want an even leaner set.

---

## 6. Example 2 — Real dataset: before vs. after model performance

Let's prove the selection didn't hurt (or even helped). We use scikit-learn's built-in **diabetes** regression dataset (10 numeric features — no downloading needed), train a `RandomForestRegressor` with ALL features vs. with the de-correlated subset, and compare R² on a held-out test set.

```python
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# --- Load data as a DataFrame ---
diabetes = load_diabetes(as_frame=True)
X, y = diabetes.data, diabetes.target

# --- Split FIRST: the correlation matrix must only ever see training data ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

def evaluate(X_tr, X_te, y_tr, y_te):
    # Train a fresh RandomForest and return its test-set R^2.
    model = RandomForestRegressor(n_estimators=300, random_state=42)
    model.fit(X_tr, y_tr)
    return r2_score(y_te, model.predict(X_te))

# --- Model A: all 10 features ---
r2_all = evaluate(X_train, X_test, y_train, y_test)

# --- Select features using the TRAINING set only ---
X_train_small, dropped_cols = drop_correlated_features(X_train, threshold=0.8)
X_test_small  = X_test[X_train_small.columns]        # apply the SAME columns to the test set

# --- Model B: reduced feature set ---
r2_reduced = evaluate(X_train_small, X_test_small, y_train, y_test)

print(f"R2 all features ({X.shape[1]}):       {r2_all:.4f}")
print(f"R2 reduced features ({X_train_small.shape[1]}):  {r2_reduced:.4f}")
print("Dropped:", dropped_cols)
```

Typical result: nearly identical R² with fewer features — a smaller, faster, easier-to-explain model for free. (Your exact numbers may vary slightly by version, the story will be the same: no meaningful loss, sometimes a small gain from reduced noise.)

---

## 7. Practical tips & common pitfalls

| Tip                                                    | Why it matters                                                                                                                            |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Fit the matrix on training data only**               | Prevents test-set leakage and over-optimistic scores.                                                                                     |
| **Start with threshold 0.8–0.9**                       | 0.7 is aggressive, 0.95 is conservative. Tune, don't dogma.                                                                               |
| **Use absolute correlation**                           | A feature at −0.9 is just as redundant as +0.9.                                                                                           |
| **Correlation ≠ causation**                            | Two features may correlate via a third variable. Keep domain knowledge in the loop.                                                       |
| **Pearson catches linear only**                        | For monotonic non-linear links, also try `df.corr(method="spearman")`.                                                                    |
| **Don't blindly drop low-target-correlation features** | Non-linear models (trees, GBMs) may still exploit them. Prefer the "train before vs. after" check.                                        |
| **Scale doesn't matter**                               | Correlation is scale-invariant — no need to standardize first.                                                                            |
| **Categorical features**                               | Correlation is for numeric data. Encode categories (e.g. one-hot, target encoding) _before_ screening, or use mutual information instead. |
| **When in doubt, keep it simple**                      | If two features are 0.85 correlated but one is far cheaper to collect in production, keep the cheap one.                                  |

---

## 8. Cheat sheet

```python
corr = df.corr()                                   # 1. matrix
sns.heatmap(corr, annot=True, cmap="coolwarm")     # 2. look at it
X_small, dropped = drop_correlated_features(X_train, 0.8)   # 3. drop redundancy
target_corr = df.corr()["target"].abs().sort_values()       # 4. rank vs target
# 5. train before vs after and compare scores               # prove it works
```

---

## 9. Summary

- The correlation matrix is a **free X-ray of your dataset**: it exposes redundancy and irrelevance at a glance.
- Use it to (a) drop one feature from every near-duplicate pair, and (b) rank features by their relationship with the target.
- It's a **filter for intuition and simplification**, not proof of importance — always confirm with a before/after model comparison.
- Fit it on the **training set only**, prefer absolute values, remember its linear blind spot, and let domain knowledge override the numbers when they disagree.

Happy (cleaner) modeling!
