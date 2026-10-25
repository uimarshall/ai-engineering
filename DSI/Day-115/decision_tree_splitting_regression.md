# Splitting Criteria in Decision Trees for Regression (Practical Guide)

> A beginner-friendly, hands-on tutorial. Every concept is paired with working Python code.
> Run the accompanying `decision_tree_regression_splitting.py` to see everything in action.

---

## 1. The Big Picture: What Is a Splitting Criterion?

A regression decision tree answers one question over and over:

> **"Which feature, and which threshold, should I use to split the data so that the two resulting groups
> are as _predictable_ as possible?"**

After every split we make a naive but surprisingly good prediction: **the average of the target values
in that group** (called a _leaf value_).

The **splitting criterion** is the _score_ that tells the algorithm _how good_ a candidate split is.
The algorithm tries many candidate splits (every feature × many thresholds), scores each one with the
criterion, and picks the best.

**Practical analogy:** You are sorting houses into two bins to predict prices. A split on
`"number of bedrooms < 3"` might give bins with wildly varying prices (bad split). A split on
`"location == city center"` might give two tight clusters of prices (good split). The criterion is
the ruler that measures this "tightness" automatically.

---

## 2. The Core Idea: Reduce "Impurity" (Error)

For regression, "impurity" of a node = **how spread out the target values are** in that node.

The tree always picks the split that reduces this spread the most:

```javascript
Gain(split) = Impurity(parent) − weighted_average(Impurity(left_child), Impurity(right_child))
```

The split with the **largest gain** wins. Below are the three impurity measures you will actually
meet in practice.

---

## 3. Criterion 1: MSE / Variance Reduction (the default)

**MSE = Mean Squared Error**

```javascript
Impurity(node) = (1/n) Σ (yᵢ − ȳ)²        ← this is just the variance of the targets in the node
```

- `yᵢ` = each target value in the node
- `ȳ` = the mean of the targets in the node (the value the leaf would predict)
- `n` = number of samples in the node

**Intuition:** Squared error punishes large deviations heavily, so MSE-based splits push outliers
into their own regions of the tree and aim for _globally_ low error.

In scikit-learn this is `criterion="squared_error"` (formerly `"mse"`).

**Worked micro-example (computed by hand in the code file):**

Targets in parent node: `[3, 5, 7, 9]` → mean = 6, MSE = (9+1+1+9)/4 = **5.0**

Try split: values ≤ 5 go left.

- Left `[3, 5]`: mean = 4, MSE = (1+1)/2 = 1.0
- Right `[7, 9]`: mean = 8, MSE = (1+1)/2 = 1.0

```javascript
Gain = 5.0 − (2/4)·1.0 − (2/4)·1.0 = 4.0   ← excellent split!
```

The code demonstrates this exact calculation programmatically.

---

## 4. Criterion 2: MAE (a.k.a. "absolute_error" / Least Absolute Deviation)

**MAE = Mean Absolute Error**

```javascript
Impurity(node) = (1/n) Σ |yᵢ − median|
```

Note: it uses the **median**, not the mean, because the median minimises absolute error.

**Intuition:** Absolute error grows _linearly_ with deviations, so a few extreme values don't dominate.
Trees built with MAE are **robust to outliers** and their leaves predict the _median_ price of the group —
great when the business question is "what's the typical value?".

Trade-off: much slower to train (median computations at every candidate split).

In scikit-learn: `criterion="absolute_error"` (formerly `"mae"`).

---

## 5. Criterion 3: Friedman MSE ("poisson"-adjacent, best for counts)

**Friedman's mean squared error** uses a slightly different improvement score that accounts for
probability-weighted variance. It is the default criterion for gradient boosting (e.g. `HistGradientBoostingRegressor`)
because it tends to find splits that generalise well.

In scikit-learn: `criterion="friedman_mse"`.

**Rule of thumb:**

| Data situation                           | Start with       |
| ---------------------------------------- | ---------------- |
| General-purpose regression               | `squared_error`  |
| Heavy outliers / want median behaviour   | `absolute_error` |
| Gradient boosting / counts & skewed data | `friedman_mse`   |

---

## 6. Practical Example 1 — Manual Split Evaluation (from scratch)

The Python file `decision_tree_regression_splitting.py` implements `mse`, `mae`, and `split_gain`
with plain numpy — no sklearn needed — so you can see _exactly_ what the criterion computes.

It evaluates two candidate splits on a tiny dataset of 6 houses
(`price = [120, 135, 180, 210, 260, 330]`):

```javascript
Parent MSE = 5236.81

Split 'bedrooms <= 2':   gain = 3975.35   ← chosen (largest gain)
Split 'size_sqm <= 80':  gain ≈ 3700.7
```

The from-scratch logic mirrors scikit-learn's `DecisionTreeRegressor` exactly: the script
verifies `tree_.impurity[0]` (root MSE stored by sklearn) equals the manually computed parent MSE,
and that sklearn picks the same winning feature/threshold (`bedrooms ≤ 2.5`).

---

## 7. Practical Example 2 — Full scikit-learn Workflow (California Housing)

The classic real-world dataset. Key practical pattern:

```python
from sklearn.datasets import fetch_california_housing
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

for crit in ["squared_error", "friedman_mse", "absolute_error"]:
    tree = DecisionTreeRegressor(criterion=crit, max_depth=4, random_state=42)
    tree.fit(X_train, y_train)
    print(crit, tree.score(X_test, y_test))   # R²
```

Typical findings (your numbers will match the script's output):

- `squared_error` and `friedman_mse` give similar accuracy; friedman sometimes edges ahead.
- `absolute_error` trains slower but can be _more stable_ when targets are skewed.
- **Unrestricted depth overfits badly** — always control with `max_depth`, `min_samples_leaf`,
  or `ccp_alpha` (cost-complexity pruning).

Also demonstrated in the code: **visualising the tree** with `plot_tree` and reading the
`criterion` value printed in every node = the impurity (MSE/MAE) of that node.

---

## 8. Practical Example 3 — Grid Search Over Splitting Criteria

Never guess which criterion fits your data — let cross-validation decide:

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    "criterion": ["squared_error", "friedman_mse", "absolute_error"],
    "max_depth": [3, 5, 8, None],
    "min_samples_leaf": [1, 5, 10],
}
gs = GridSearchCV(DecisionTreeRegressor(random_state=42), param_grid, cv=5,
                  scoring="neg_root_mean_squared_error", n_jobs=-1)
gs.fit(X_train, y_train)
print(gs.best_params_)
```

The script prints the best combination — this is how you choose a splitting criterion **in practice**.

---

## 9. Practical Example 4 — Outlier Robustness Shootout

We inject 5% extreme outliers (houses worth $2M+) into California housing targets and compare
`squared_error` vs `absolute_error` with identical hyperparameters.

On California housing you will typically see the MAE tree degrade far less (lower RMSE on the
_clean_ test set), illustrating section 5's intuition: linear error growth ⇒ outlier-resistant splits.

---

## 10. Key Takeaways

1. A splitting criterion is just a **score for "how spread out targets are"** after a candidate split.
2. The tree greedily picks the split with maximum **impurity reduction**.
3. `squared_error` (MSE/variance reduction) is the default and best first choice.
4. `absolute_error` (MAE) is slower but **robust to outliers** and predicts medians.
5. `friedman_mse` shines in boosting setups and on skewed/count data.
6. The criterion matters far less than **regularisation** (`max_depth`, `min_samples_leaf`, pruning).
7. Verify your understanding: root impurity printed by `plot_tree` == manual MSE of the training targets.

---

## 11. Further Reading

- scikit-learn `DecisionTreeRegressor` docs (criteria & parameters)
- Breiman et al., _Classification and Regression Trees_ (1984) — the original CART criterion
- Géron, _Hands-On Machine Learning_, Ch. 6 — decision trees chapter

_Files: this note (`decision_tree_splitting_regression.md`) + runnable script (`decision_tree_regression_splitting.py`)._
