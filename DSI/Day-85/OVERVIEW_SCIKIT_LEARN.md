# Supervised Learning for Absolute Beginners

### A hands-on tutorial with runnable Python code, formulas broken down, real business use cases, and plots

**What you need**

```bash
pip install numpy pandas matplotlib scikit-learn scipy joblib
```

**How to use this tutorial**

1. Read the sections in order. Each one has: the idea → the formula explained piece by piece → what the code does → what the graph means.
2. At the end there is **one complete script**. Copy it into a file named `supervised_learning.py` and run `python supervised_learning.py`.
3. Every figure is saved to `plots/` **and** displayed on screen.
4. The script uses only bundled datasets (`make_regression`, `load_diabetes`, `load_breast_cancer`), so it runs offline in a few seconds.

---

## 1. What is supervised learning?

Supervised learning = **learning from examples where you already know the right answer.**

You give the algorithm pairs of `(input, correct answer)`. It learns a rule that maps input → answer. Then you use that rule on _new_ inputs where the answer is unknown.

| Everyday analogy                    | Machine learning term   |
| ----------------------------------- | ----------------------- |
| Flashcards with answers on the back | labeled training data   |
| The question side of the card       | features (X)            |
| The answer on the back              | label / target (y)      |
| A student studying the deck         | `model.fit(X, y)`       |
| The exam                            | test set                |
| The student's exam answers          | `model.predict(X_test)` |

### The two flavours

| Task               | You predict  | Target type                    | Example                           |
| ------------------ | ------------ | ------------------------------ | --------------------------------- |
| **Regression**     | a _number_   | continuous (`42.5`)            | house price, revenue, temperature |
| **Classification** | a _category_ | discrete (`fraud`/`not fraud`) | spam, churn, disease              |

### The universal workflow

```
raw data → clean & split (train/test) → choose model → fit on train → evaluate on test → improve → deploy
```

The single most important rule: **never evaluate on data the model has seen.** Otherwise you are grading a student on the exact questions they studied.

---

## 2. Regression, formula by formula

### 2.1 Simple linear regression

The model is a straight line:

```
ŷ = w0 + w1 · x
```

- `x` — the input feature (e.g. size in m²)
- `ŷ` — the predicted number (say "read as y-hat")
- `w1` — the **slope**: how much `ŷ` changes when `x` increases by 1
- `w0` — the **intercept**: the prediction when `x = 0`

### 2.2 How does it _learn_ w0 and w1?

It picks the line that minimises the **Mean Squared Error (MSE)**: the average of the squared vertical gaps between the real points and the line.

```
      1   n
MSE = ─ · Σ (yᵢ − ŷᵢ)²
      n  i=1
```

Broken down:

- `yᵢ − ŷᵢ` → **residual** for one point: how far off the guess was.
- `( … )²` → squaring makes misses positive and punishes big misses harder than small ones.
- `Σ` → add up all points.
- `1/n` → average, so the score doesn't depend on dataset size.

Because MSE is a smooth bowl-shaped function of `w0` and `w1`, there is a **closed-form solution** (the "normal equation"):

```
w = (Xᵀ X)⁻¹ Xᵀ y     where X has a column of 1s added for the intercept
```

`Xᵀ` means "transpose", `⁻¹` means "matrix inverse". Part 1 of the script computes both the library answer and this closed form, and they match to 3 decimals — good sanity check that the model really is just solving that equation.

### 2.3 With several features

```
ŷ = w0 + w1·x1 + w2·x2 + … + wp·xp
```

Each `wj` is "how much the prediction moves per unit of feature j, holding the others fixed". That is exactly what makes the model **interpretable** — you can read the coefficients as business insights (see Part 3).

### 2.4 Regression metrics, in plain words

| Metric | Formula              | Reads as                                     | Units                          |
| ------ | -------------------- | -------------------------------------------- | ------------------------------ | --------------------------------- | --------- |
| MAE    | `(1/n) Σ             | yᵢ − ŷᵢ                                      | `                              | typical miss, no big-miss penalty | same as y |
| MSE    | `(1/n) Σ (yᵢ − ŷᵢ)²` | squared typical miss                         | y²                             |
| RMSE   | `√MSE`               | typical miss, big misses punished            | same as y ✔ easiest to explain |
| R²     | `1 − SSE/SST`        | fraction of the target's variation explained | 0…1                            |

- `SSE = Σ(yᵢ − ŷᵢ)²` — error left over.
- `SST = Σ(yᵢ − ȳ)²` — total variation around the mean.
- `R² = 0` means "no better than always predicting the average", `R² = 1` is perfect, negative means worse than the average.

**Always report RMSE for the business conversation** ("we are typically off by ±£38k") and R² for the technical one.

---

## 3. Classification, formula by formula

### 3.1 Logistic regression — the workhorse

We need a probability, so the raw linear score is squashed into 0…1 by the **sigmoid**:

```
z = w0 + w1·x1 + … + wp·xp
p = σ(z) = 1 / (1 + e^(−z))
```

Piece by piece:

- `z` — a linear score (can be any number, negative or positive).
- `e^(−z)` — the exponential function; large `z` makes `e^(−z)` tiny.
- As `z → +∞`, `p → 1`; as `z → −∞`, `p → 0`; at `z = 0`, `p = 0.5`.

Training minimises **log loss** (binary cross-entropy):

```
Loss = −(1/n) Σ [ yᵢ·log(pᵢ) + (1 − yᵢ)·log(1 − pᵢ) ]
```

- When the true label `yᵢ = 1`, only `log(pᵢ)` counts → confident-and-wrong (`p ≈ 0`) is punished brutally.
- When `yᵢ = 0`, only `log(1 − pᵢ)` counts → symmetric.
- The minus sign flips the log (always ≤ 0) into a positive cost to minimise.

The decision: predict class 1 if `p ≥ 0.5` (you can move that threshold — see Part 4.6).

### 3.2 k-Nearest Neighbours (kNN)

No equation: to predict a new point, find its `k` nearest training points and take a majority vote (classification) or their average (regression). Distance is usually Euclidean:

```
d(a, b) = √( (a1−b1)² + (a2−b2)² + … + (ap−bp)² )
```

**Crucial**: kNN compares distances, so features must be on the same scale — otherwise `monthly_charge` (0–140) drowns out `support_calls` (0–8). Hence `StandardScaler`.

### 3.3 Decision trees

A tree asks yes/no questions ("is `worst concave points` ≤ 0.14?") and splits the data into ever-purer groups. "Purity" is measured by **Gini impurity**:

```
Gini(node) = 1 − Σ_k (p_k)²
```

where `p_k` is the fraction of the node's samples in class `k`.

- A pure node (all one class): `Gini = 1 − 1² = 0` ✔
- A 50/50 node with 2 classes: `1 − (0.5² + 0.5²) = 0.5` ✘

The tree greedily picks the split that reduces weighted Gini impurity the most. Depth controls complexity: deep trees memorise (overfit), shallow trees underfit. `max_depth=3` keeps ours readable and generalisable.

### 3.4 Classification metrics you must know

A **confusion matrix** for a "positive = fraud" problem:

|                     | predicted negative  | predicted positive  |
| ------------------- | ------------------- | ------------------- |
| **actual negative** | true negative (TN)  | false positive (FP) |
| **actual positive** | false negative (FN) | true positive (TP)  |

| Metric               | Formula                     | Plain English                                 |
| -------------------- | --------------------------- | --------------------------------------------- |
| Accuracy             | `(TP+TN)/n`                 | % correct — **misleading with imbalance**     |
| Precision            | `TP/(TP+FP)`                | when we say "yes", how often are we right?    |
| Recall (sensitivity) | `TP/(TP+FN)`                | of all real positives, how many did we catch? |
| F1                   | `2·(P·R)/(P+R)`             | harmonic mean; balances precision & recall    |
| ROC-AUC              | area under TPR-vs-FPR curve | ranking quality, threshold-free; 0.5 = random |

_ROC curve_: sweep the threshold from 1 → 0, plotting **TPR = TP/(TP+FN)** (recall) against **FPR = FP/(FP+TN)**. The better the curve hugs the top-left corner, the higher the AUC.

**Which metric matters is a business decision.** Fraud screening favours recall (catch them all). A "send a discount" campaign favours precision (don't waste money). Accuracy alone tells you almost nothing on an imbalanced problem: predicting "never churns" is 95% accurate and 100% useless.

---

## 4. What the code does, section by section

### Part 1 — Simple linear regression (`plots/01_...png`)

`make_regression(n_features=1, noise=18)` builds 200 points along a hidden line plus noise. We split 75/25, fit, then print slope, intercept, MAE, RMSE, R².
_The graph_: grey/blue dots = train/test points, black line = learned rule. It looks like a mostly noise-free cloud because `noise=18` is modest relative to the target's spread — that's why R² is high. Bump `noise` to 60 and watch R² collapse; that is what "noisy target" feels like.

### Part 2 — Overfitting (`plots/02_...png`)

Same data, but we add `PolynomialFeatures(degree=d)` (i.e. x, x², x³…) and fit for degrees 1…10, recording **train RMSE** and **5-fold CV RMSE**.
_The graph_: two panels. Left = the classic X shape: train error only ever falls (the model can always bend harder), CV error falls then rises. The bottom of the CV curve is the sweet spot. Right = a degree-1 and a degree-9 fit drawn over the data, so you can _see_ the model tying itself in knots. The script prints the CV-optimal degree.

> **Rule of thumb**: train error going up = underfit (add complexity). Train error low, CV error rising = overfit (regularise, get more data, or simplify).

### Part 3 — Multiple regression on real data (`load_diabetes`)

442 patients, 10 standardised clinical features, target = disease progression after one year. A `Pipeline(StandardScaler → LinearRegression)` prints RMSE and R², then a bar chart of coefficients (`plots/03_...png`).
_Reading the chart_: because features are standardised, bar lengths are directly comparable — "bmi" and "s5" (log serum triglycerides) push progression up the most, "age" barely matters. In a business setting this chart _is_ the deliverable: which levers actually move the outcome.

### Part 4 — Classification on real data (`load_breast_cancer`)

569 tumours, 30 features, target = malignant (212) / benign (357). Stratified split so both sets keep that ratio.

- **4.1 Model bake-off** — logistic regression, kNN (k=5), depth-3 decision tree, all inside pipelines where scaling is needed. Prints accuracy, precision, recall, F1, ROC-AUC in one table. In this dataset they all land ~0.93–0.99 AUC; the lesson is _not_ "logistic regression wins forever", it's "start simple, compare honestly, then tune".
- **4.2 Confusion matrix** (heatmap in `plots/04_...png`) plus `classification_report` — this is where you see _which_ mistakes are being made.
- **4.3 ROC curves** for all three models overlaid (`plots/05_...png`) with AUC in the legend.
- **4.4 Decision tree picture** (`plots/06_...png`) — `plot_tree` shows the actual if/else rules. This is the single best way to build trust with non-technical stakeholders: they can read the model out loud.
- **4.5 Decision boundary** (`plots/07_...png`) — we refit logistic regression on just 2 features (mean radius, mean texture), predict `p` over a fine grid, and shade the plane. The white region is "benign territory", the shaded one "malignant"; dots are real patients. A boundary that cuts cleanly with few dots on the wrong side = learnable signal. Overlapping clouds = the two features aren't enough, so the full 30-feature model is justified.
- **4.6 Threshold tuning** — we print how precision/recall shift as we move the cut-off from 0.3 to 0.7. Lowering the threshold raises recall (catch more cancers, more false alarms); raising it raises precision. **The model outputs a probability; the threshold is a business choice, not a mathematical one.**

---

## 5. Practical, real-world use cases

| Use case                            | Task                          | Typical features                              | What the business does with it                             |
| ----------------------------------- | ----------------------------- | --------------------------------------------- | ---------------------------------------------------------- |
| **Customer churn**                  | Binary classification         | tenure, support calls, contract type, charges | Target retention offers at high-risk, high-value customers |
| **Credit / loan default**           | Binary classification         | income, debt ratio, repayment history         | Approve, decline, or price the interest rate               |
| **Insurance claim severity**        | Regression                    | vehicle age, region, policy type              | Set reserves and premiums                                  |
| **Demand forecasting**              | Regression                    | price, seasonality, promotions, holidays      | Plan stock and staffing                                    |
| **Spam filtering**                  | Binary classification         | word frequencies, sender reputation           | Route to inbox or junk                                     |
| **Product quality (manufacturing)** | Regression / classification   | sensor readings, machine age                  | Predict scrap before it happens                            |
| **Medical triage**                  | Classification (recall-first) | labs, vitals, history                         | Flag patients for human review                             |
| **Dynamic pricing**                 | Regression                    | demand signals, competitor prices             | Quote the right price per segment                          |
| **Lead scoring (B2B)**              | Classification (probability)  | firmographics, website behaviour              | Salespeople call the top 10% first                         |

**A worked business story.** A telecom has 19% churn. The supervised model outputs a churn _probability per customer_. The team multiplies probability × customer lifetime value to rank by **expected revenue at risk**. Marketing then offers a discount only to that top decile. The metric they track isn't accuracy; it's **recall at the chosen budget** ("of all customers who would have churned, what share did we catch?") and the **net margin of the saved revenue minus discounts given**. This is the pattern in almost every supervised deployment: _probability → expected value → action_.

---

## 6. Common beginner mistakes (and the fix)

1. **Evaluating on training data.** Fix: always `train_test_split`, or better cross-validation.
2. **Forgetting to scale** before kNN, SVM, logistic regression, PCA. Fix: put `StandardScaler` _inside_ a `Pipeline` so it's fit on train folds only.
3. **Data leakage** — e.g. scaling/imputing before splitting, or using a feature that encodes the answer. Fix: pipelines; ask "would I know this at prediction time?" for every column.
4. **Judging by accuracy on imbalanced data.** Fix: look at precision/recall/F1/AUC and the confusion matrix.
5. **Chasing 0.99 accuracy on a toy dataset.** Fix: test on data that resembles production, and check a **dummy baseline** (predict the majority class). If your model can't beat the dummy, you have no signal.
6. **Overfitting the test set** by tuning against it repeatedly. Fix: tune with cross-validation on the train set; touch the test set once, at the end.
7. **Ignoring cost asymmetry.** A missed fraud ≠ a false alarm. Fix: choose the threshold that minimises expected cost.

---

## 7. Exercises (answers are just "run it and look")

1. In Part 1, set `noise=60`. What happens to R² and to the scatter cloud?
2. In Part 2, change the split to `test_size=0.1`. Does the CV-optimal polynomial degree change?
3. In Part 4.1, add `Ridge`-style regularised logistic regression: `LogisticRegression(C=0.01)`. What happens to AUC? Why?
4. In Part 4.6, find the threshold that maximises recall while keeping precision ≥ 0.95. What would that policy cost in false alarms?
5. Drop `max_depth=3` from the decision tree and re-run. Compare train vs test accuracy. Overfit or not?

---

## 8. Cheat sheet

```python
# regression
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=.25, random_state=42)
model = Pipeline([("scaler", StandardScaler()), ("m", LinearRegression())]).fit(X_tr, y_tr)
rmse = np.sqrt(mean_squared_error(y_te, model.predict(X_te)))

# classification
model = Pipeline([("scaler", StandardScaler()),
                  ("m", LogisticRegression(max_iter=1000, class_weight="balanced"))])
model.fit(X_tr, y_tr)
proba = model.predict_proba(X_te)[:, 1]      # use this for ranking / thresholds
pred  = (proba >= 0.5).astype(int)           # threshold is yours to choose
print(roc_auc_score(y_te, proba), classification_report(y_te, pred))
```

**Default starting order**: logistic/linear regression → add regularisation → try a random forest / gradient boosting → tune hyperparameters → tune the threshold → interpret → deploy → monitor drift.

---

---

# Full runnable script — save as `supervised_learning.py`

```python
"""
supervised_learning_tutorial.py
A runnable tour of supervised learning: regression + classification.
Deps: numpy, pandas, matplotlib, scikit-learn
Run : python supervised_learning.py     (figures are saved to plots/)
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import make_regression, load_diabetes, load_breast_cancer
from sklearn.model_selection import (train_test_split, cross_val_score,
                                     KFold, StratifiedKFold)
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (mean_absolute_error, mean_squared_error, r2_score,
                             accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, ConfusionMatrixDisplay,
                             roc_curve, roc_auc_score, classification_report)

PLOTS = "plots"
os.makedirs(PLOTS, exist_ok=True)
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)


def banner(title):
    print("\n" + "=" * 72 + "\n" + title + "\n" + "=" * 72)


# =====================================================================
# PART 1 - SIMPLE LINEAR REGRESSION
# =====================================================================
banner("PART 1 - SIMPLE LINEAR REGRESSION:  y_hat = w0 + w1 * x")

X, y = make_regression(n_samples=200, n_features=1, noise=18.0,
                       random_state=RANDOM_STATE)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=RANDOM_STATE)

lin = LinearRegression().fit(X_train, y_train)
y_pred = lin.predict(X_test)

print(f"learned slope     w1 = {lin.coef_[0]:.3f}")
print(f"learned intercept w0 = {lin.intercept_:.3f}")
print(f"MAE  = {mean_absolute_error(y_test, y_pred):7.2f}")
print(f"MSE  = {mean_squared_error(y_test, y_pred):7.2f}")
print(f"RMSE = {np.sqrt(mean_squared_error(y_test, y_pred)):7.2f}")
print(f"R^2  = {r2_score(y_test, y_pred):7.3f}")

# same answer via the closed-form normal equation w = (X^T X)^-1 X^T y
Xb = np.c_[np.ones((X_train.shape[0], 1)), X_train]
w_closed = np.linalg.solve(Xb.T @ Xb, Xb.T @ y_train)
print("closed-form [intercept, slope] =", np.round(w_closed.ravel(), 3))

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(X_train, y_train, s=25, alpha=0.65, label="train data")
ax.scatter(X_test, y_test, s=25, alpha=0.65, label="test data")
grid = np.linspace(X.min(), X.max(), 200).reshape(-1, 1)
ax.plot(grid, lin.predict(grid), color="black", lw=2.5, label="fitted line")
ax.set_xlabel("feature x")
ax.set_ylabel("target y")
ax.set_title(f"Simple linear regression   (test RMSE = "
             f"{np.sqrt(mean_squared_error(y_test, y_pred)):.1f})")
ax.legend()
fig.tight_layout()
fig.savefig(f"{PLOTS}/01_linear_regression_fit.png", dpi=150)
plt.show()


# =====================================================================
# PART 2 - OVERFITTING: polynomial degree vs train/CV error
# =====================================================================
banner("PART 2 - OVERFITTING: train error vs cross-validation error")

degrees = list(range(1, 11))
train_rmse, cv_rmse = [], []
kf = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

for d in degrees:
    pipe = Pipeline([("poly", PolynomialFeatures(degree=d, include_bias=False)),
                     ("lin", LinearRegression())])
    pipe.fit(X_train, y_train)
    train_rmse.append(np.sqrt(mean_squared_error(y_train,
                                                 pipe.predict(X_train))))
    scores = -cross_val_score(pipe, X_train, y_train, cv=kf,
                              scoring="neg_root_mean_squared_error")
    cv_rmse.append(scores.mean())

best_degree = degrees[int(np.argmin(cv_rmse))]
for d, tr, cv in zip(degrees, train_rmse, cv_rmse):
    flag = "  <-- best CV" if d == best_degree else ""
    print(f"degree {d:2d} | train RMSE {tr:7.2f} | CV RMSE {cv:7.2f}{flag}")

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].plot(degrees, train_rmse, "o-", label="train RMSE")
axes[0].plot(degrees, cv_rmse, "s-", label="5-fold CV RMSE")
axes[0].axvline(best_degree, color="green", ls="--", alpha=0.6,
                label=f"best degree = {best_degree}")
axes[0].set_xlabel("polynomial degree (model complexity)")
axes[0].set_ylabel("RMSE")
axes[0].set_title("Underfitting on the left, overfitting on the right")
axes[0].legend()

grid = np.linspace(X.min(), X.max(), 300).reshape(-1, 1)
order = np.argsort(X_train.ravel())
axes[1].scatter(X_train, y_train, s=18, alpha=0.5, label="train data")
for d, colour in [(1, "tab:green"), (9, "tab:red")]:
    p = Pipeline([("poly", PolynomialFeatures(degree=d, include_bias=False)),
                  ("lin", LinearRegression())]).fit(X_train, y_train)
    axes[1].plot(grid, p.predict(grid), color=colour, lw=2, label=f"degree {d}")
axes[1].set_ylim(y_train.min() - 60, y_train.max() + 60)
axes[1].set_xlabel("x")
axes[1].set_ylabel("y")
axes[1].set_title("What the models actually look like")
axes[1].legend()
fig.tight_layout()
fig.savefig(f"{PLOTS}/02_overfitting_curve.png", dpi=150)
plt.show()


# =====================================================================
# PART 3 - MULTIPLE LINEAR REGRESSION ON REAL DATA
# =====================================================================
banner("PART 3 - MULTIPLE REGRESSION: diabetes disease progression")

diab = load_diabetes()
X = pd.DataFrame(diab.data, columns=diab.feature_names)
y = diab.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=RANDOM_STATE)

reg = Pipeline([("scaler", StandardScaler()),
                ("lin", LinearRegression())]).fit(X_train, y_train)
y_pred = reg.predict(X_test)
print(f"RMSE = {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}   "
      f"R^2 = {r2_score(y_test, y_pred):.3f}")

coefs = pd.Series(reg.named_steps["lin"].coef_,
                  index=diab.feature_names).sort_values()
print("\nstandardised coefficients (effect on target per 1 SD of the feature):")
print(coefs.round(2).to_string())

fig, ax = plt.subplots(figsize=(8, 5))
coefs.plot(kind="barh", ax=ax, color=["tab:red" if v < 0 else "tab:blue"
                                      for v in coefs])
ax.axvline(0, color="black", lw=0.8)
ax.set_xlabel("coefficient (standardised)")
ax.set_title("Which features move the outcome, and in which direction")
fig.tight_layout()
fig.savefig(f"{PLOTS}/03_regression_coefficients.png", dpi=150)
plt.show()


# =====================================================================
# PART 4 - CLASSIFICATION ON REAL DATA (breast cancer)
# =====================================================================
banner("PART 4 - CLASSIFICATION: malignant vs benign tumours")

data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target
print("shape:", X.shape, "| class counts:",
      dict(zip(*np.unique(y, return_counts=True))))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y)

models = {
    "Logistic regression": Pipeline([("scaler", StandardScaler()),
                                     ("clf", LogisticRegression(max_iter=2000))]),
    "kNN (k=5)": Pipeline([("scaler", StandardScaler()),
                           ("clf", KNeighborsClassifier(n_neighbors=5))]),
    "Decision tree (depth 3)": DecisionTreeClassifier(max_depth=3,
                                                      random_state=RANDOM_STATE),
}

rows, fitted = [], {}
for name, mdl in models.items():
    mdl.fit(X_train, y_train)
    fitted[name] = mdl
    pred = mdl.predict(X_test)
    proba = mdl.predict_proba(X_test)[:, 1]
    rows.append({"model": name,
                 "accuracy": accuracy_score(y_test, pred),
                 "precision": precision_score(y_test, pred),
                 "recall": recall_score(y_test, pred),
                 "f1": f1_score(y_test, pred),
                 "roc_auc": roc_auc_score(y_test, proba)})

print("\nmodel comparison on the held-out test set:")
print(pd.DataFrame(rows).round(3).to_string(index=False))

# ---- 4.2 confusion matrix + report for logistic regression
best_name = "Logistic regression"
best = fitted[best_name]
pred = best.predict(X_test)
proba = best.predict_proba(X_test)[:, 1]

print(f"\nconfusion matrix ({best_name}):\n{confusion_matrix(y_test, pred)}")
print("\nclassification report:")
print(classification_report(y_test, pred,
                            target_names=["benign (0)", "malignant (1)"]))

fig, ax = plt.subplots(figsize=(5.5, 4.5))
ConfusionMatrixDisplay.from_predictions(
    y_test, pred, display_labels=["benign", "malignant"],
    cmap="Blues", colorbar=False, ax=ax)
ax.set_title(f"Confusion matrix - {best_name}")
fig.tight_layout()
fig.savefig(f"{PLOTS}/04_confusion_matrix.png", dpi=150)
plt.show()

# ---- 4.3 ROC curves for every model
fig, ax = plt.subplots(figsize=(6.5, 5.5))
for name, mdl in fitted.items():
    p = mdl.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, p)
    ax.plot(fpr, tpr, lw=2,
            label=f"{name} (AUC = {roc_auc_score(y_test, p):.3f})")
ax.plot([0, 1], [0, 1], "k--", lw=1, label="random guessing (AUC = 0.5)")
ax.set_xlabel("false positive rate  =  FP / (FP + TN)")
ax.set_ylabel("true positive rate  =  TP / (TP + FN)  =  recall")
ax.set_title("ROC curves: higher and further left is better")
ax.legend(loc="lower right", fontsize=9)
fig.tight_layout()
fig.savefig(f"{PLOTS}/05_roc_curves.png", dpi=150)
plt.show()

# ---- 4.4 the decision tree, drawn as rules
tree = fitted["Decision tree (depth 3)"]
fig, ax = plt.subplots(figsize=(16, 8))
plot_tree(tree, feature_names=list(X.columns), class_names=["benign", "malignant"],
          filled=True, rounded=True, fontsize=9, ax=ax)
ax.set_title("A depth-3 decision tree - every stakeholder can read these rules")
fig.tight_layout()
fig.savefig(f"{PLOTS}/06_decision_tree.png", dpi=150)
plt.show()

# ---- 4.5 decision boundary using just two features
feat2 = ["mean radius", "mean texture"]
X2 = X[feat2].values
X2_train, X2_test, y2_train, y2_test = train_test_split(
    X2, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y)

clf2 = Pipeline([("scaler", StandardScaler()),
                 ("clf", LogisticRegression(max_iter=2000))]).fit(X2_train, y2_train)

pad = 1.0
xx, yy = np.meshgrid(
    np.linspace(X2[:, 0].min() - pad, X2[:, 0].max() + pad, 300),
    np.linspace(X2[:, 1].min() - pad, X2[:, 1].max() + pad, 300))
Z = clf2.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1].reshape(xx.shape)

fig, ax = plt.subplots(figsize=(8, 6))
cs = ax.contourf(xx, yy, Z, levels=20, cmap="RdBu_r", alpha=0.75)
fig.colorbar(cs, ax=ax, label="P(malignant)")
ax.scatter(X2[y == 0, 0], X2[y == 0, 1], s=25, edgecolor="k",
           facecolor="white", label="benign")
ax.scatter(X2[y == 1, 0], X2[y == 1, 1], s=25, edgecolor="k",
           facecolor="red", label="malignant")
ax.set_xlabel("mean radius")
ax.set_ylabel("mean texture")
ax.set_title("Decision boundary from only 2 of the 30 features")
ax.legend()
fig.tight_layout()
fig.savefig(f"{PLOTS}/07_decision_boundary.png", dpi=150)
plt.show()
print(f"AUC with only 2 features: {roc_auc_score(y2_test, clf2.predict_proba(X2_test)[:, 1]):.3f}"
      f"  (vs {roc_auc_score(y_test, proba):.3f} with all 30)")

# ---- 4.6 threshold is a business decision, not a maths result
print("\nhow the cut-off changes precision / recall / F1:")
for t in [0.3, 0.4, 0.5, 0.6, 0.7]:
    p = (proba >= t).astype(int)
    print(f"threshold {t:.1f} -> precision {precision_score(y_test, p):.3f} | "
          f"recall {recall_score(y_test, p):.3f} | f1 {f1_score(y_test, p):.3f}")

banner("DONE - look inside the plots/ folder")
print("Plots written: 01..07 in plots/")
print("Try: raise 'noise' in Part 1, change the polynomial degrees in Part 2,")
print("     or move the threshold in Part 4.6 and watch the trade-off.")
```

---

# FILE 2 of 3 — `unsupervised_learning.md`

`````markdown
# Unsupervised Learning for Absolute Beginners

### Clustering, dimensionality reduction, anomaly detection and association rules — with runnable Python code and plots

**Setup**

```bash
pip install numpy pandas matplotlib scikit-learn scipy
```

Run the script at the end (`unsupervised_learning.py`). Every figure is saved into `plots/` and shown, and it uses only bundled datasets (`make_blobs`, `make_moons`, `load_wine`) so it works offline in seconds.

---

## 1. What is unsupervised learning?

Supervised learning had answers on the flashcards. **Unsupervised learning has no answers at all.** You hand the algorithm raw inputs and ask it to find _structure_: groups, hidden dimensions, oddities, recurring patterns.

| Question you're asking               | Technique family         | Typical use                         |
| ------------------------------------ | ------------------------ | ----------------------------------- |
| "Which customers behave alike?"      | Clustering               | segmentation, targeting             |
| "Can I compress 300 columns into 5?" | Dimensionality reduction | visualisation, speed, noise removal |
| "Is this transaction weird?"         | Anomaly detection        | fraud, equipment faults             |
| "What gets bought together?"         | Association rules        | cross-sell, shelf layout            |

Key difference in mindset: **there is no "correct answer" to compare against**, so evaluation is about _usefulness_, not accuracy. A clustering is "right" if the business acts on it and it works.

---

## 2. Clustering

### 2.1 k-Means — the default starting point

**Objective**: minimise the **within-cluster sum of squares (inertia)**:

```
                K
inertia = Σ     Σ       ‖x − μ_k‖²
         k=1  x∈C_k
```

- `K` — number of clusters (you choose it).
- `C_k` — the set of points assigned to cluster k.
- `μ_k` — the **centroid** of cluster k = the mean of its points.
- `‖x − μ_k‖²` — squared Euclidean distance from a point to its centroid.

**Lloyd's algorithm** (what `KMeans` does):

1. Pick K initial centroids (sklearn's `k-means++` spreads them out smartly).
2. **Assign** each point to its nearest centroid.
3. **Update** each centroid to the mean of the points assigned to it.
4. Repeat 2–3 until assignments stop changing (or `max_iter` is hit).

Two things to internalise:

- k-Means assumes **round, similarly-sized clusters** — it draws straight boundaries, so it fails on crescents and rings.
- It minimises distance in **feature space**, so **scaling matters enormously**. Standardise first.

### 2.2 How do I choose K? Elbow + silhouette

**Elbow method**: plot inertia against K. Inertia always falls as K grows (K = n gives 0), so look for the "elbow" where the drop flattens. Subjective, but a useful first pass.

**Silhouette score** — a sharper, per-point measure of "how well am I placed?":

```
        b(i) − a(i)
s(i) = ─────────────
        max(a(i), b(i))
```

- `a(i)` = mean distance from point i to the other points **in its own cluster** (cohesion). Small is good.
- `b(i)` = mean distance from point i to the points of the **nearest other cluster** (separation). Large is good.
- Range −1 … +1: near **+1** = snugly in the right cluster; near **0** = on a boundary; **negative** = probably in the wrong cluster.
- The dataset-level silhouette is just the average of `s(i)`; the K with the highest average is a strong candidate.

### 2.3 Hierarchical (agglomerative) clustering

Build a **tree of merges** (a dendrogram) instead of picking K up front:

1. Start: every point is its own cluster.
2. Repeatedly merge the two closest clusters.
3. Stop when everything is one cluster; then **cut the dendrogram** horizontally to get any K you like.

Cluster distance is measured by **linkage**: `ward` (minimises within-cluster variance — the usual choice for compact clusters), `complete` (farthest points), `average` (mean pairwise), `single` (nearest points — good for chains, prone to chaining everything).

Great when you want to _see_ the structure and decide K afterwards, and when n is small-ish (cost grows roughly as n²).

### 2.4 DBSCAN — density-based clustering

Instead of "round blobs", DBSCAN asks: **is this point in a dense neighbourhood?**

- `eps` (ε) — radius of a neighbourhood.
- `minPts` — how many points (including itself) make a neighbourhood "dense".
- **Core point**: a point with ≥ `minPts` neighbours within `eps`.
- **Border point**: within `eps` of a core point but not itself core.
- **Noise point**: neither → labelled **−1**.

Clusters grow by connecting core points within `eps` of each other. Advantages: finds arbitrary shapes, **doesn't need K**, and explicitly labels outliers. Cost: `eps` and `minPts` are sensitive, and clusters of very different densities are hard.

### 2.5 How do I judge clustering without labels?

Use **internal** metrics: silhouette (↑ better), Davies–Bouldin (↓ better), inertia (only for k-Means, only for comparing same-scaled data).

If a labelled subset happens to exist, use **Adjusted Rand Index (ARI)**: it compares your clusters to the true labels, corrected for chance. 1.0 = perfect agreement, ~0 = random. The script prints ARI for the synthetic examples _only because we generated the ground truth_ — in real life you rarely have it.

### 2.6 Real use cases

| Use case                                   | What the clusters become                                                             |
| ------------------------------------------ | ------------------------------------------------------------------------------------ |
| Retail / telecom **customer segmentation** | "budget families", "loyal high-spenders", "churn-risk newbies" → different campaigns |
| **Product assortment**                     | groups of items bought together → bundling, planogram layout                         |
| **Document / ticket triage**               | support tickets grouped by topic → route to the right team                           |
| **Image colour compression**               | k-Means on pixel colours → 16-colour palette                                         |
| **Geo-demographics**                       | neighbourhoods grouped by census features → site selection                           |
| **Biology**                                | grouping cells/genes by expression profile                                           |
| **Infrastructure**                         | servers grouped by usage pattern → capacity planning                                 |

**Cautionary tale worth telling in the room**: clustering always returns clusters, even on pure noise. Always (a) check silhouette, (b) profile the clusters with human-readable averages, and (c) ask "would we spend money differently on these groups?" If not, it's decoration.

---

## 3. Dimensionality reduction

### 3.1 PCA — Principal Component Analysis

**Goal**: find the few directions along which your data varies most, and describe each point by those directions instead of the original columns.

Pipeline of maths:

1. **Standardise**: `z = (x − μ) / σ` for each feature (otherwise a feature measured in pennies dominates one measured in pounds).
2. **Covariance matrix**: `C = (1/(n−1)) · Zᵀ Z`. Diagonal = variances, off-diagonal = how features move together.
3. **Eigen-decomposition**: solve `C v = λ v`. Each eigenvector `v` is a direction; its eigenvalue `λ` is the variance captured along it.
4. **Sort** eigenvectors by `λ` descending → PC1, PC2, …
5. **Project**: `Z_new = Z · V_k`, keeping the top k eigenvectors.

**Explained variance ratio** of component j:

```
EVR_j = λ_j / (λ_1 + λ_2 + … + λ_p)
```

It tells you what share of the total variance that component carries. A scree plot (bars) plus a cumulative curve tells you how many components you need for, say, 90% of the variance.

**Two trade-offs to state out loud:**

- PCs are **linear combinations** — great for compression and visualisation, bad for interpretability ("PC1 is 0.4·radius + 0.3·texture − …").
- PCA is unsupervised: it keeps directions of **variance**, which are usually — but not always — the directions that predict your target. If you have a target, consider supervised alternatives (e.g. feature importance / LDA / PLS).

### 3.2 t-SNE and UMAP (in one paragraph)

Non-linear methods for **visualisation only** (2D/3D). t-SNE preserves local neighbourhoods: points that are close in high dimensions tend to be close in the plot. Do **not** read global distances ("cluster A is far from B") or cluster sizes off a t-SNE plot, and never feed t-SNE output into a downstream model. Use it to _look_, then verify with something else.

### 3.3 Real use cases

- **Visual QA of a pipeline**: project embeddings to 2D and check that classes/segments separate at all.
- **Compression & speed**: 300 correlated features → 20 PCs before fitting a slow model.
- **Noise removal**: dropping low-variance components often removes sensor noise.
- **Collinearity**: PCs are mutually uncorrelated by construction — handy before linear models.
- **Anomaly detection on images/spectra**: reconstruction error grows for odd inputs.

---

## 4. Anomaly detection

### 4.1 Isolation Forest

Idea: **anomalies are few and different, so they get isolated quickly.** Build many random trees; each tree repeatedly picks a random feature and a random split value until every point is alone. Then:

```
s(x) = 2^( −E[h(x)] / c(n) )
```

- `h(x)` = path length (number of splits) needed to isolate x in a tree.
- `E[h(x)]` = average path length across all trees.
- `c(n)` ≈ average path length of an unsuccessful search in a random tree of n points (a normalising constant).
- Short paths → `s(x)` near 1 → **anomaly**. Normal points need many splits → `s(x)` well below 0.5.

Why it works: a normal point sits inside a dense cloud and needs many cuts to be singled out; an outlier sits alone and is separated in 1–2 cuts.

### 4.2 Simpler cousins

- **Z-score**: flag anything with `|z| = |x − μ| / σ > 3`. Fine for one feature, assumes a bell shape.
- **IQR rule**: flag values outside `[Q1 − 1.5·IQR, Q3 + 1.5·IQR]`. Robust, still one feature at a time.
- **Mahalanobis distance**: multi-dimensional z-score that accounts for feature correlations.
- **Autoencoder reconstruction error**: for images/signals — normal inputs reconstruct well, weird ones don't.

### 4.3 Real use cases

| Domain            | What "anomaly" means                   | Consequence                         |
| ----------------- | -------------------------------------- | ----------------------------------- |
| Banking           | unusual card transaction               | block / 2FA / call the customer     |
| Manufacturing     | vibration or temperature signature off | schedule maintenance before failure |
| IT/security       | odd login location, traffic spike      | alert the SOC                       |
| Healthcare claims | implausible billing pattern            | audit                               |
| E-commerce        | bot-like browsing                      | block, protect inventory            |
| Energy            | meter readings that don't fit usage    | possible tampering/leak             |

**Key operational point**: anomaly detection produces _a ranked queue for humans_, not verdicts. Set the alert volume to what your team can actually review.

---

## 5. Association rules (market-basket analysis)

Three numbers make a rule `A → B` meaningful:

```
support(A → B)     = (baskets containing A and B) / (all baskets)
confidence(A → B)  = (baskets containing A and B) / (baskets containing A)
lift(A → B)        = confidence(A → B) / support(B)
```

- **Support** — how common the pattern is. Too low = noise or a niche you can't scale.
- **Confidence** — given A is in the basket, how often B follows. Reads like "70% of the time".
- **Lift** — how much better than chance. `lift = 1` = B is independent of A; `lift = 2` = B is twice as likely given A. **Lift is the one that creates value**; high-confidence rules can be trivially obvious (bread → milk simply because milk is in most baskets).

The classic Apriori loop: find frequent single items → build candidate pairs → keep the frequent ones → extend to triples → generate rules and rank by lift. (In the script we implement the pairwise version by hand so you can see the machinery; production code uses `mlxtend.apriori`.)

**Use cases**: "customers who buy X also buy Y" → bundle pricing, recommendation carousels, store layout, coupon targeting, churn-prevention offers ("you bought the router, here's the insurance").

---

## 6. What the code does, section by section

### Part 1 — k-Means on 4 blobs (`plots/u01_...png`)

`make_blobs(n_samples=500, centers=4)` creates four obvious groups _and_ their true labels. We fit `KMeans(n_clusters=4)`, then print inertia, silhouette, Davies–Bouldin, and ARI versus the truth.
_The graph_: two panels — true labels (left) versus what k-Means discovered (right), with centroids drawn as black ✕ markers. If the panels match, ARI ≈ 1. This is your "hello world" of clustering: a sanity check that the mechanics work before you point it at messy business data.

### Part 2 — Choosing K (`plots/u02_...png`)

We loop `K = 2…10`, recording inertia and average silhouette.
_The graph_: left = the elbow curve (look for the bend at K=4); right = silhouette vs K with a dashed line at the maximum. On this data silhouette peaks at 4. **In real data the two often disagree** — then favour the K that yields interpretable, actionable segments, and validate with a business owner.

### Part 3 — Shape matters: k-Means vs DBSCAN (`plots/u03_...png`)

We generate two interleaving moons. k-Means is forced to cut them with a straight line; DBSCAN (`eps=0.30, minPts=5`) walks along the density and separates them properly. We print ARI for both.
_The graph_: three panels — ground truth, k-Means, DBSCAN. This single figure is the best answer to "why not always use k-Means?". Note DBSCAN may also label a few lone points as noise (−1, drawn in grey) — that's a feature, not a bug.

### Part 4 — Hierarchical clustering + dendrogram (`plots/u04_...png`)

We take 60 points, compute `linkage(..., method="ward")` and draw the dendrogram.
_The graph_: the y-axis is the merge distance. Tall vertical jumps mean "these two groups really are different". The red dashed line shows where to cut to obtain 3 clusters; the script also fits `AgglomerativeClustering(n_clusters=3)` and prints its ARI against the truth, so you can connect "cutting the tree" with "getting labels".

### Part 5 — PCA on wine data (`plots/u05_...png`)

`load_wine`: 178 wines, 13 chemical measurements (alcohol, flavanoids, colour intensity…), 3 grape varieties. We standardise, fit `PCA()` with all components, and print how many components are needed for 80%/90% of the variance.
_The graph_: left = scree plot (bars = explained variance ratio per component, line = cumulative); right = the 2D projection coloured by true grape variety. Two components capture a large share of the chemistry, and the varieties largely separate — visual proof that the structure was real, not invented by the algorithm.

### Part 6 — Anomaly detection with Isolation Forest (`plots/u06_...png`)

We build 300 normal points in a tight cloud plus 20 deliberate outliers spread over a wide box, fit `IsolationForest(contamination=0.06)` and flag `predict == -1`.
_The graph_: grey = "normal", red = flagged. The red points sit outside the dense cloud as intended. `contamination` sets the _expected_ proportion of anomalies and directly controls alert volume — tune it to staffing, then look at the ranking score `decision_function()` rather than only the binary flag.

### Part 7 — Association rules by hand (no plot, printed table)

Ten grocery baskets, all pairs evaluated for support / confidence / lift, ranked by lift. You can see the classic `diapers → beer` style rule emerge with a lift well above 1. Change the baskets or add a third item to extend it to triples.

### Part 8 — Sanity checklist printed at the end

A short recap your team can paste into a runbook: scale first, check silhouette, label the clusters in plain English, validate with a stakeholder, and never present a 2D t-SNE plot as if it were the truth.

---

## 7. Common beginner mistakes

1. **Forgetting to scale** → one feature with big units hijacks the distances. Standardise (or use a method less sensitive to scale).
2. **Feeding correlated/duplicated columns** → implicitly weights that concept twice. Consider PCA or dropping duplicates.
3. **Believing K = "the number of groups that exist"** → K is a modelling choice, not an discovered truth.
4. **Reading cluster _sizes_ on a t-SNE plot**, or distances between far-apart t-SNE clusters. Don't.
5. **Treating anomalies as confirmed fraud** → they're a prioritised review queue.
6. **Evaluating with labels you'd never have in production** and forgetting that internal metrics (silhouette) can disagree with business value.
7. **Not naming the clusters.** A cluster without a business-readable profile will never be acted on.
8. **Stale segments.** Customer behaviour drifts; schedule refits (monthly/quarterly) and monitor segment stability.

---

## 8. Exercises

1. In Part 1, set `cluster_std=2.5` (blobs now overlap). How far does silhouette fall? Does ARI survive?
2. In Part 2, extend K to 15. Where does silhouette peak now, and how does ARI compare with the true K=4?
3. In Part 3, set `eps=0.15` and then `eps=0.6`. Describe what DBSCAN does — too many noise points vs everything merging into one cluster.
4. In Part 5, drop the standardisation step (use raw `wine.data`). Which components change most, and why?
5. In Part 6, set `contamination=0.20`. How many "anomalies" get flagged? What would that mean for an ops team?
6. In Part 7, add the item `chips` to a few baskets and re-run. Does any rule's lift break 1.5?

---

## 9. Cheat sheet

```python
from sklearn.preprocessing import StandardScaler
X_scaled = StandardScaler().fit_transform(X)          # ALWAYS first

from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score, adjusted_rand_score
kmeans = KMeans(n_clusters=4, n_init="auto", random_state=42).fit(X_scaled)
print(silhouette_score(X_scaled, kmeans.labels_))

from sklearn.decomposition import PCA
pca = PCA(n_components=0.90)                           # keep 90% of variance
Z = pca.fit_transform(X_scaled)
print(pca.explained_variance_ratio_)

from sklearn.ensemble import IsolationForest
flags = IsolationForest(contamination=0.05, random_state=42) \
        .fit_predict(X_scaled)                          # -1 == anomaly
```

**Order of operations for a real project**: explore → scale → cluster with several Ks → pick K by silhouette **plus** interpretability → profile each cluster with plain-English averages → PCA/t-SNE for a 2D health check → validate with the business → operationalise the labels → monitor drift.

---

---

# Full runnable script — save as `unsupervised_learning.py`

```python
"""
unsupervised_learning_tutorial.py
Clustering, PCA, anomaly detection and association rules - all runnable.
Deps: numpy, pandas, matplotlib, scikit-learn, scipy
Run : python unsupervised_learning.py      (figures are saved to plots/)
"""
import os
from itertools import combinations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

from sklearn.datasets import make_blobs, make_moons, load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (silhouette_score, davies_bouldin_score,
                             adjusted_rand_score)

PLOTS = "plots"
os.makedirs(PLOTS, exist_ok=True)
RANDOM_STATE = 42
rng = np.random.RandomState(RANDOM_STATE)


def banner(title):
    print("\n" + "=" * 72 + "\n" + title + "\n" + "=" * 72)


def scatter_clusters(ax, X, labels, title, centroids=None):
    uniq = sorted(set(labels))
    for k in uniq:
        m = labels == k
        if k == -1:
            ax.scatter(X[m, 0], X[m, 1], s=22, c="lightgrey",
                       edgecolor="k", label="noise (-1)")
        else:
            ax.scatter(X[m, 0], X[m, 1], s=22, cmap="tab10",
                       c=np.full(m.sum(), k % 10), alpha=0.8, label=f"cluster {k}")
    if centroids is not None:
        ax.scatter(centroids[:, 0], centroids[:, 1], marker="X", s=220,
                   c="black", zorder=5, label="centroids")
    ax.set_title(title)
    ax.legend(fontsize=8, loc="best")


# =====================================================================
# PART 1 - k-MEANS ON SYNTHETIC BLOBS
# =====================================================================
banner("PART 1 - k-MEANS: does the algorithm rediscover the true groups?")

X, y_true = make_blobs(n_samples=500, centers=4, cluster_std=1.1,
                       random_state=RANDOM_STATE)
km = KMeans(n_clusters=4, n_init=10, random_state=RANDOM_STATE).fit(X)

print(f"inertia (WCSS)        = {km.inertia_:.1f}")
print(f"silhouette score      = {silhouette_score(X, km.labels_):.3f}  (higher is better)")
print(f"davies-bouldin score  = {davies_bouldin_score(X, km.labels_):.3f}  (lower is better)")
print(f"adjusted Rand index   = {adjusted_rand_score(y_true, km.labels_):.3f}  (1.0 = perfect)")

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
scatter_clusters(axes[0], X, y_true, "Ground truth (we know the answer here)")
scatter_clusters(axes[1], X, km.labels_, "k-Means with K=4 (what it found)",
                 centroids=km.cluster_centers_)
fig.tight_layout()
fig.savefig(f"{PLOTS}/u01_kmeans_blobs.png", dpi=150)
plt.show()


# =====================================================================
# PART 2 - CHOOSING K: ELBOW + SILHOUETTE
# =====================================================================
banner("PART 2 - HOW MANY CLUSTERS? elbow curve + silhouette score")

ks = list(range(2, 11))
inertias, sils = [], []
for k in ks:
    km_k = KMeans(n_clusters=k, n_init=10, random_state=RANDOM_STATE).fit(X)
    inertias.append(km_k.inertia_)
    sils.append(silhouette_score(X, km_k.labels_))

best_k = ks[int(np.argmax(sils))]
for k, i, s in zip(ks, inertias, sils):
    flag = "  <-- best silhouette" if k == best_k else ""
    print(f"K={k:2d} | inertia {i:8.1f} | silhouette {s:.3f}{flag}")

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].plot(ks, inertias, "o-", color="tab:blue")
axes[0].set_xlabel("number of clusters K")
axes[0].set_ylabel("inertia (within-cluster sum of squares)")
axes[0].set_title("Elbow curve: look for the bend")
axes[0].axvline(4, color="green", ls="--", alpha=0.6, label="true K = 4")
axes[0].legend()

axes[1].plot(ks, sils, "s-", color="tab:orange")
axes[1].axvline(best_k, color="green", ls="--", alpha=0.6,
                label=f"best K = {best_k}")
axes[1].set_xlabel("number of clusters K")
axes[1].set_ylabel("average silhouette score")
axes[1].set_title("Silhouette: pick the peak")
axes[1].legend()
fig.tight_layout()
fig.savefig(f"{PLOTS}/u02_elbow_silhouette.png", dpi=150)
plt.show()


# =====================================================================
# PART 3 - CLUSTER SHAPE MATTERS: k-MEANS vs DBSCAN
# =====================================================================
banner("PART 3 - k-MEANS vs DBSCAN on crescent-shaped data")

Xm, ym = make_moons(n_samples=500, noise=0.06, random_state=RANDOM_STATE)
Xm = StandardScaler().fit_transform(Xm)

labels_km = KMeans(n_clusters=2, n_init=10, random_state=RANDOM_STATE).fit_predict(Xm)
labels_db = DBSCAN(eps=0.30, minPts=5).fit_predict(Xm)

print(f"k-Means  ARI vs truth = {adjusted_rand_score(ym, labels_km):.3f}")
print(f"DBSCAN   ARI vs truth = {adjusted_rand_score(ym, labels_db):.3f}")
print(f"DBSCAN found {len(set(labels_db)) - (1 if -1 in labels_db else 0)} clusters "
      f"and flagged {(labels_db == -1).sum()} noise points")

fig, axes = plt.subplots(1, 3, figsize=(17, 5))
scatter_clusters(axes[0], Xm, ym, "Ground truth (two interleaving moons)")
scatter_clusters(axes[1], Xm, labels_km, "k-Means: straight-line boundary fails")
scatter_clusters(axes[2], Xm, labels_db, "DBSCAN: follows the density")
fig.tight_layout()
fig.savefig(f"{PLOTS}/u03_kmeans_vs_dbscan.png", dpi=150)
plt.show()


# =====================================================================
# PART 4 - HIERARCHICAL CLUSTERING + DENDROGRAM
# =====================================================================
banner("PART 4 - HIERARCHICAL CLUSTERING: the dendrogram")

idx = rng.choice(len(X), 60, replace=False)
Xs, ys = X[idx], y_true[idx]

Z = linkage(Xs, method="ward")
cut_height = (Z[-3, 2] + Z[-2, 2]) / 2.0          # height that yields 3 clusters
agg = AgglomerativeClustering(n_clusters=3, linkage="ward").fit(Xs)
print(f"Agglomerative (K=3) ARI vs truth = {adjusted_rand_score(ys, agg.labels_):.3f}")

fig, ax = plt.subplots(figsize=(11, 5))
dendrogram(Z, ax=ax, no_labels=True, color_threshold=cut_height)
ax.axhline(cut_height, color="red", ls="--", lw=1.5,
           label=f"cut here -> 3 clusters (height = {cut_height:.2f})")
ax.set_xlabel("samples (order chosen by the algorithm)")
ax.set_ylabel("merge distance (ward linkage)")
ax.set_title("Dendrogram: tall jumps separate genuinely different groups")
ax.legend()
fig.tight_layout()
fig.savefig(f"{PLOTS}/u04_dendrogram.png", dpi=150)
plt.show()


# =====================================================================
# PART 5 - PCA ON WINE CHEMISTRY
# =====================================================================
banner("PART 5 - PCA: compressing 13 chemical features")

wine = load_wine()
Xw = StandardScaler().fit_transform(wine.data)
y_wine = wine.target

pca_full = PCA().fit(Xw)
evr = pca_full.explained_variance_ratio_
cum = np.cumsum(evr)

for target in (0.80, 0.90):
    n_needed = int(np.searchsorted(cum, target) + 1)
    print(f"{int(target*100)}% of the variance needs {n_needed} components "
          f"(out of {Xw.shape[1]})")
print("first five explained variance ratios:",
      np.round(evr[:5], 3), "| cumulative:", np.round(cum[:5], 3))

Z2 = PCA(n_components=2, random_state=RANDOM_STATE).fit_transform(Xw)

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
axes[0].bar(range(1, len(evr) + 1), evr, alpha=0.8, label="individual")
axes[0].plot(range(1, len(evr) + 1), cum, "o-", color="tab:red",
             label="cumulative")
axes[0].axhline(0.90, color="green", ls="--", alpha=0.7, label="90% line")
axes[0].set_xlabel("principal component")
axes[0].set_ylabel("explained variance ratio")
axes[0].set_title("Scree plot: how much information each PC carries")
axes[0].legend(fontsize=9)

for cls, name in enumerate(wine.target_names):
    m = y_wine == cls
    axes[1].scatter(Z2[m, 0], Z2[m, 1], s=30, alpha=0.8, label=name)
axes[1].set_xlabel(f"PC1 ({evr[0]*100:.0f}% of variance)")
axes[1].set_ylabel(f"PC2 ({evr[1]*100:.0f}% of variance)")
axes[1].set_title("Wines in 2D: the varieties largely separate")
axes[1].legend()
fig.tight_layout()
fig.savefig(f"{PLOTS}/u05_pca_wine.png", dpi=150)
plt.show()


# =====================================================================
# PART 6 - ANOMALY DETECTION WITH ISOLATION FOREST
# =====================================================================
banner("PART 6 - ANOMALY DETECTION: Isolation Forest")

normal = rng.normal(loc=0.0, scale=1.0, size=(300, 2))
outliers = rng.uniform(low=-6.0, high=6.0, size=(20, 2))
Xa = np.vstack([normal, outliers])

iso = IsolationForest(n_estimators=200, contamination=0.06,
                      random_state=RANDOM_STATE).fit(Xa)
flags = iso.predict(Xa)                       # +1 normal, -1 anomaly
scores = iso.decision_function(Xa)            # higher = more normal

print(f"flagged anomalies: {(flags == -1).sum()} of {len(Xa)} "
      f"(contamination=0.06 targets ~6%)")
print("5 most anomalous points (lowest score):")
order = np.argsort(scores)[:5]
for i in order:
    print(f"  point {Xa[i]}  score {scores[i]:+.3f}"
          f"{'  <- a real injected outlier' if i >= 300 else ''}")

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(Xa[flags == 1, 0], Xa[flags == 1, 1], s=25, c="lightsteelblue",
           edgecolor="k", label="normal")
ax.scatter(Xa[flags == -1, 0], Xa[flags == -1, 1], s=60, c="crimson",
           edgecolor="k", label="flagged anomaly")
ax.set_title("Isolation Forest: anomalies are few, different, and isolated fast")
ax.legend()
fig.tight_layout()
fig.savefig(f"{PLOTS}/u06_isolation_forest.png", dpi=150)
plt.show()


# =====================================================================
# PART 7 - ASSOCIATION RULES, IMPLEMENTED BY HAND
# =====================================================================
banner("PART 7 - ASSOCIATION RULES: support, confidence, lift")

transactions = [
    {"bread", "milk"},
    {"bread", "diapers", "beer", "eggs"},
    {"milk", "diapers", "beer", "cola"},
    {"bread", "milk", "diapers", "beer"},
    {"bread", "milk", "diapers", "cola"},
    {"bread", "milk", "beer", "cola"},
    {"bread", "milk", "diapers", "beer", "cola"},
    {"milk", "diapers", "beer"},
    {"bread", "diapers", "beer"},
    {"bread", "milk", "diapers", "beer"},
]
items = sorted(set().union(*transactions))
N = len(transactions)


def support(itemset):
    s = set(itemset)
    return sum(1 for t in transactions if s <= t) / N


rows = []
for a, b in combinations(items, 2):
    s_ab = support({a, b})
    if s_ab == 0:
        continue
    rows.append({"rule": f"{a} -> {b}", "support": s_ab,
                 "confidence": s_ab / support({a}),
                 "lift": (s_ab / support({a})) / support({b})})
    rows.append({"rule": f"{b} -> {a}", "support": s_ab,
                 "confidence": s_ab / support({b}),
                 "lift": (s_ab / support({b})) / support({a})})

rules = pd.DataFrame(rows).sort_values("lift", ascending=False)
print(f"{len(transactions)} baskets, {len(items)} distinct items, "
      f"{len(rules)} pairwise rules\n")
print("top 10 rules by lift (lift > 1 means 'better than chance'):")
print(rules.head(10).round(3).to_string(index=False))


# =====================================================================
# PART 8 - SANITY CHECKLIST
# =====================================================================
banner("SANITY CHECKLIST BEFORE YOU SHIP ANYTHING UNSUPERVISED")
for line in [
    "1. Scale features before anything distance-based.",
    "2. Never trust a clustering you cannot describe in plain English.",
    "3. Use silhouette / Davies-Bouldin to compare, but decide with the business.",
    "4. Profile each cluster: means, medians, top categories, size, revenue.",
    "5. Anomalies are a ranked review queue, not verdicts - size it to your team.",
    "6. A t-SNE picture is for looking, not for measuring.",
    "7. Re-fit on a schedule and watch for segment drift.",
]:
    print(line)
print("\nPlots written to plots/: u01..u06")
```

---

# FILE 3 of 3 — `scikit_learn_tutorial.md`

````markdown
# scikit-learn for Absolute Beginners

### One library, one API, an end-to-end project — with runnable Python code and plots

**Setup**

```bash
pip install numpy pandas matplotlib scikit-learn joblib
```

Everything below runs from the single script at the end (`sklearn_tutorial.py`). Figures go into `plots/` and are also displayed.

---

## 1. Why scikit-learn?

- **One consistent API** for 50+ algorithms: `fit`, `predict`, `transform`, `score`.
- **Everything batteries-included**: train/test splitting, cross-validation, pipelines, preprocessing, metrics, hyper-parameter search, model persistence, inspection tools.
- **Consistent, non-leaky train/test behaviour**: scalers and encoders inside a `Pipeline` are refit on each cross-validation fold automatically. This alone prevents the most common beginner bug.
- **Documentation with runnable examples** for every class, and a stable API you can standardise a team on.

It is not for deep learning (use PyTorch/TensorFlow) or heavy statistical inference (use statsmodels). For "classic" ML on tabular data, it is the default tool.

---

## 2. The mental model: three objects

| Object type           | Examples                                                           | What it does                                                 |
| --------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------ |
| **Transformer**       | `StandardScaler`, `SimpleImputer`, `OneHotEncoder`, `PCA`          | learns something from X, then changes X — `fit_transform(X)` |
| **Estimator / model** | `LogisticRegression`, `RandomForestClassifier`, `KMeans`           | learns to predict — `fit(X, y)`, then `predict(X)`           |
| **Meta-tools**        | `Pipeline`, `ColumnTransformer`, `GridSearchCV`, `cross_val_score` | glue and evaluation — they _also_ implement `fit`/`predict`  |

### The API contract

```python
model.fit(X_train, y_train)      # learn
model.predict(X_test)            # predict labels / values
model.predict_proba(X_test)      # predict class probabilities (classifiers)
model.transform(X)               # apply a learned transformation (transformers)
model.score(X_test, y_test)      # default metric: R² for regressors, accuracy for classifiers
model.get_params()               # introspection -> powers GridSearchCV
```

Three conventions that make everything composable:

1. `X` is always **2D** (`n_samples × n_features`) — a DataFrame or a 2-D array. `y` is 1-D.
2. **Every estimator follows the same two method names**, so you can swap `LogisticRegression` for `RandomForestClassifier` without touching the rest of the code.
3. **`random_state=42`** anywhere a result is random (splits, forests, k-means, t-SNE) — otherwise your "improvement" might be luck.

---

## 3. Why pipelines decide whether your project succeeds

A model is almost never just an algorithm. It's: impute missing values → scale numbers → one-hot encode categories → fit model. Two ways to do it:

```python
# A) WRONG when combined with cross-validation / test sets
X_train_scaled = scaler.fit_transform(X_train)   # scaler learns the mean of ALL train data
...
# B) RIGHT
pipe = Pipeline([("scaler", StandardScaler()), ("model", LogisticRegression())])
```

In (A), if you scale _before_ splitting or _before_ cross-validation, the scaler's mean/std has seen data that the model is later tested on — **data leakage**. The model looks better in testing than it will ever be in production. Pipelines make leakage structurally impossible because `fit` only ever touches the training fold.

`ColumnTransformer` extends the idea to mixed column types: different preprocessing per column group, all inside one object.

---

## 4. The end-to-end workflow this tutorial demonstrates

We build a **telecom churn** dataset from scratch with realistic properties:

- numeric columns (`age`, `tenure_months`, `monthly_charge`, `support_calls`),
- categorical columns (`contract`, `internet_service`, `paperless_billing`),
- **missing values** (real data always has them),
- **class imbalance** (~19% churn).

Then we do the full professional loop:

```
1. Load & explore                 -> what does churn look like by contract type?
2. Split train/test (stratified)  -> keep the churn ratio in both halves
3. Dummy baseline                 -> the score to beat
4. Preprocessing + model pipeline -> impute, scale, one-hot, random forest
5. Cross-validated comparison     -> logistic regression vs random forest
6. Hyper-parameter search         -> GridSearchCV over the pipeline
7. Final evaluation               -> confusion matrix, ROC, classification report
8. Threshold tuning               -> precision/recall trade-off in business terms
9. Interpretation                 -> permutation importance
10. Learning curve                -> more data, or a better model?
11. Persist & serve               -> joblib save/load, score new customers
```

---

## 5. Formulas, broken down (the ones you actually need here)

### Stratified splitting

Instead of a random split, keep the class proportion:
`churn rate in train ≈ churn rate in test ≈ 19%`. Without this, a small dataset can end up with wildly different churn rates across halves and your evaluation becomes noise.

### Cross-validation (k-fold)

Split the training data into k folds; train on k−1, validate on the held-out fold; repeat k times; report mean ± std of the metric. **Every** point is used for validation exactly once. The standard deviation tells you how stable the model is — a mean AUC of 0.80 ± 0.07 is much less trustworthy than 0.80 ± 0.01.

### Dummy baseline

`DummyClassifier(strategy="most_frequent")` predicts "no churn" for everyone. Its accuracy equals the majority-class share (~81%), and its ROC-AUC is 0.5 by construction. **Any model that can't clearly beat the dummy is worthless**, no matter how respectable the accuracy looks.

### ROC-AUC (area, not accuracy)

AUC = the probability that the model gives a random churner a higher churn score than a random non-churner. Because it's rank-based, it's independent of the 0.5 threshold and of the class balance — which is exactly why it's the right metric for imbalanced problems like churn.

### Random forest in two sentences

Fit many decorrelated decision trees on bootstrap samples with random feature subsets at each split, then **average their probabilities**. Averaging cancels much of the variance of individual trees, which is why forests massively out-perform a single deep tree. Its knobs: `n_estimators` (more = more stable, then diminishing returns), `max_depth` (deeper = more overfitting), `min_samples_leaf` (higher = smoother, more conservative rules), `class_weight="balanced"` (ups-weight the minority class).

### Permutation importance

For each feature j: shuffle column j, re-score the model, and record how much the score drops. If shuffling a feature barely hurts, the model didn't rely on it. Model-agnostic, and it works on the _original_ columns even though the pipeline expanded them into one-hot dummies. Caveat: when two features are correlated, shuffling one may not hurt (the other covers for it) — so read it as "reliance", not "causation".

### Learning curve

Plot training score and validation score against training-set size. The shape tells you your next move:

- Both curves still rising, big gap → **more data will help**.
- Both curves flat and close → **more data won't help**; get better features or a stronger model.
- Train high, validation low → **overfitting**; regularise/simplify or add data.

---

## 6. What the code does, section by section

### Part 0 — The API tour (printed output, 15 lines)

`load_iris` → `train_test_split` → `StandardScaler().fit_transform` → `LogisticRegression().fit/predict/score`. Nine lines of code that touch every concept in section 2. Read this first if the rest looks intimidating.

### Part 1 — Building the churn dataset

A seeded `numpy` generator creates 1500 customers. Churn is drawn from a **logistic model**, so the relationship is realistically noisy rather than deterministic:

```
logit = −2.2 + 0.030·support_calls + 0.011·monthly_charge − 0.028·tenure_months
        + 1.15·(contract = month-to-month) + 0.45·(internet = fiber) + 0.20·(paperless = yes)
p = 1 / (1 + e^(−logit))
```

Reading the coefficients as the business story: month-to-month contracts (+1.15 on the log-odds) push churn up hard, long tenure pulls it down, fibre customers complain more, support calls signal trouble. We then punch holes: 4% missing `monthly_charge`, 3% missing `internet_service`, 2% missing `tenure_months`. The script prints shape, churn rate and missing counts so you always see the data you're working with.

### Part 2 — EDA in ten lines + one plot (`plots/s01_...png`)

A bar chart of **churn rate by contract type**. This is the plot you show a stakeholder 30 seconds into the meeting, and it already hints at what the model will find. _Reading it_: month-to-month bars tower over the one-/two-year bars — the feature the model will lean on most.

### Part 3 — Split + dummy baseline

`train_test_split(..., stratify=y, test_size=0.25)` then `DummyClassifier`. Prints the dummy's accuracy (~0.81) and AUC (0.500). Memorise that 0.81: **it is the floor**. From here on, "accuracy" is a trap and AUC is the target.

### Part 4 — The pipeline

- Numeric branch: `SimpleImputer(strategy="median")` → `StandardScaler()`. Median imputation is robust to outliers; scaling matters for the logistic-regression comparison.
- Categorical branch: `SimpleImputer(strategy="most_frequent")` → `OneHotEncoder(handle_unknown="ignore")`. The `handle_unknown` flag means an unseen category at prediction time produces all-zeros instead of crashing your production endpoint.
- `ColumnTransformer` wires branches to column names; `Pipeline` appends `RandomForestClassifier`.
- `class_weight="balanced"` compensates for the 19/81 imbalance so the minority class isn't ignored.

### Part 5 — Honest comparison with `cross_validate`

Logistic regression and random forest, both inside the _same_ `ColumnTransformer`, compared with 5-fold stratified CV on accuracy, precision, recall, F1 and ROC-AUC, plus **fit time**. Because it's cross-validated, you also get the spread, so you can tell a real improvement from noise. _Expect_: logistic regression gets decent AUC fast; the forest edges ahead on AUC thanks to non-linear interactions (e.g. high support calls _only_ matter for month-to-month customers), at a much higher compute cost.

### Part 6 — `GridSearchCV`

Search over `model__n_estimators`, `model__max_depth`, `model__min_samples_leaf` — 8 combinations × 5 folds = 40 fits. Note the **double-underscore** `step__parameter` naming: it means "parameter of the step named `model`", so the search can reach inside a pipeline. It prints the best parameters, the best CV AUC, and then confirms the choice on the untouched test set.

### Part 7 — Final evaluation (`plots/s02_confusion_matrix.png`, `s03_roc_curve.png`)

Confusion matrix + `classification_report`, then the ROC curve with AUC in the legend. Read the confusion matrix in business language: one cell is "customers we'd have saved", another is "discounts wasted on people who'd have stayed anyway". Those two numbers, multiplied by money, decide whether the project is worth deploying.

### Part 8 — Threshold tuning (`plots/s04_threshold_tuning.png`)

Sweep the cut-off 0.05 → 0.95 and plot precision, recall and F1. The default 0.5 is arbitrary. The script prints the threshold that maximises F1 and a "recall-first" threshold that keeps precision ≥ 0.60 — because a retention team would rather make 60 good calls than 100 random ones. **A model outputs a probability; the business owns the threshold.** (Technical note: the script tunes on the test set for teaching clarity; in production tune on a validation set or with cross-validated predictions, then touch the test set once.)

### Part 9 — Permutation importance (`plots/s05_permutation_importance.png`)

Box plots of AUC loss per shuffled feature, on the test set. The chart is the report to the business: "these four levers explain almost all of the model's ranking power". It also validates the domain story — if `customer_id` showed up at the top, something would be wrong with your pipeline.

### Part 10 — Learning curve (`plots/s06_learning_curve.png`)

Train vs CV AUC against training-set size. If they've converged and both are flat, adding rows won't help — the value now comes from new _features_ (usage trends, complaint text, competitor offers), not more of the same data.

### Part 11 — `joblib` persistence and scoring new customers

`joblib.dump(best_model, "churn_pipeline.joblib")`, reload, and call `predict_proba` on a hand-written DataFrame of six new customers. **Because the whole pipeline (imputer + scaler + encoder + model) was saved as one object, raw new rows are enough — no manual preprocessing.** That property is the real payoff of pipelines: the training-time transformation and serving-time transformation can never drift apart.

### Part 12 — Cheat sheet, printed

The exact snippets for split / scale / encode / CV / tune / evaluate / save, so you don't have to remember the imports.

---

## 7. Practical, real-world use cases

| Problem                           | sklearn pieces you'd combine                                                                           |
| --------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Churn scoring (this tutorial)** | `ColumnTransformer` + `RandomForestClassifier` + `GridSearchCV` + threshold tuning                     |
| **Credit decisioning**            | `LogisticRegression` (interpretable, regulators accept it) + `class_weight` + calibrated probabilities |
| **Demand forecasting**            | `HistGradientBoostingRegressor` + `TimeSeriesSplit` (never a random split on time series)              |
| **Fraud detection**               | `IsolationForest` for candidate screening, then a supervised model on reviewed cases                   |
| **Document routing**              | `TfidfVectorizer` + `LinearSVC` inside a pipeline                                                      |
| **Customer segmentation**         | `StandardScaler` + `KMeans` + silhouette analysis                                                      |
| **Price prediction**              | `HistGradientBoostingRegressor` + `TransformedTargetRegressor` (log-target) + `KFold`                  |
| **Any production model**          | `Pipeline` + `joblib` + `cross_validate` in CI to catch performance regressions before deployment      |

The recurring theme: **preprocessing and model are one artifact, evaluated by cross-validation, tuned by search, interpreted by inspection, and shipped as a single file.**

---

## 8. Common beginner mistakes

1. **Scaling/encoding outside a pipeline** → leakage and a model that underperforms in production.
2. **Not stratifying** on imbalanced classification → meaningless evaluation.
3. **Reporting accuracy** on imbalanced data → your model "achieves 81%" by predicting nothing.
4. **`fit_transform` on the test set** (it must be `transform` only). It's an easy typo; pipelines remove the temptation.
5. **GridSearchCV on the test set.** Search with CV on train, then evaluate once on test.
6. **Overlapping train/test after shuffling time series.** Use `TimeSeriesSplit` or split by date.
7. **Forgetting `random_state`**, then "discovering" improvements that don't reproduce.
8. **Ignoring the dummy baseline.** Always print it.
9. **Tuning the threshold until the test set looks good.** Tune it on validation data, and justify it with a business cost, not a metric.
10. **Letting the pipeline grow silently.** Print `best.named_steps` and `get_feature_names_out()` once; know what you're feeding the model.

---

## 9. Exercises

1. Remove `class_weight="balanced"` and rerun Part 5. What happens to recall and to precision?
2. Add `("pca", PCA(n_components=5))` to the random-forest pipeline. Does CV AUC improve, and by how much does fit time change?
3. Extend the grid with `model__max_features` in `[None, "sqrt", 0.5]` and `model__class_weight` in `[None, "balanced"]`. What wins?
4. Change the split to `test_size=0.1`. Does the chosen threshold move? Why is a smaller test set a bad idea for threshold tuning?
5. Save the model, then delete the training data from your notebook and score the six new customers using only the `.joblib` file. This is exactly what production does.
6. Swap the forest for `HistGradientBoostingClassifier(random_state=42)`. Compare AUC and fit time with `cross_validate`.

---

## 10. Cheat sheet

```python
# ---- split
from sklearn.model_selection import train_test_split
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=.25,
                                          stratify=y, random_state=42)

# ---- preprocess + model, always one object
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
prep = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")),
                      ("sc", StandardScaler())]), num_cols),
    ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                      ("oh", OneHotEncoder(handle_unknown="ignore"))]), cat_cols)])

# ---- cross-validated comparison
from sklearn.model_selection import cross_validate, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
models = {"logreg": LogisticRegression(max_iter=1000, class_weight="balanced"),
          "forest": RandomForestClassifier(n_estimators=300, random_state=42,
                                           class_weight="balanced")}
for name, m in models.items():
    pipe = Pipeline([("prep", prep), ("model", m)])
    res = cross_validate(pipe, X_tr, y_tr, cv=StratifiedKFold(5, shuffle=True,
                        random_state=42), scoring=["roc_auc", "f1"])

# ---- tune
from sklearn.model_selection import GridSearchCV
search = GridSearchCV(pipe, {"model__max_depth": [None, 8, 16],
                             "model__min_samples_leaf": [1, 3]},
                      scoring="roc_auc", cv=5, n_jobs=-1).fit(X_tr, y_tr)
print(search.best_params_, search.best_score_)

# ---- evaluate + persist
from sklearn.metrics import classification_report, roc_auc_score
proba = search.best_estimator_.predict_proba(X_te)[:, 1]
print(roc_auc_score(y_te, proba))
print(classification_report(y_te, (proba >= 0.4).astype(int)))
import joblib; joblib.dump(search.best_estimator_, "model.joblib")
```

---

---

# Full runnable script — save as `sklearn_tutorial.py`

```python
"""
sklearn_tutorial.py
An end-to-end scikit-learn project: telecom churn with mixed data types,
missing values, class imbalance, pipelines, CV, tuning, interpretation,
threshold tuning, learning curves and model persistence.

Deps: numpy, pandas, matplotlib, scikit-learn, joblib
Run : python sklearn_tutorial.py          (figures saved to plots/)
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.datasets import load_iris
from sklearn.model_selection import (train_test_split, StratifiedKFold,
                                     cross_validate, GridSearchCV,
                                     learning_curve)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import (roc_auc_score, roc_curve, classification_report,
                             confusion_matrix, ConfusionMatrixDisplay,
                             accuracy_score, precision_score, recall_score,
                             f1_score, precision_recall_curve)

PLOTS = "plots"
os.makedirs(PLOTS, exist_ok=True)
RANDOM_STATE = 42
RNG = np.random.default_rng(7)


def banner(title):
    print("\n" + "=" * 74 + "\n" + title + "\n" + "=" * 74)


# =====================================================================
# PART 0 - THE 9-LINE API TOUR
# =====================================================================
banner("PART 0 - THE scikit-learn API IN NINE LINES")

iris = load_iris(as_frame=True)
Xi_tr, Xi_te, yi_tr, yi_te = train_test_split(
    iris.data, iris.target, test_size=0.25, stratify=iris.target,
    random_state=RANDOM_STATE)

scaler = StandardScaler().fit(Xi_tr)            # transformers learn, then transform
Xi_tr_s, Xi_te_s = scaler.transform(Xi_tr), scaler.transform(Xi_te)

clf = LogisticRegression(max_iter=1000).fit(Xi_tr_s, yi_tr)
print("iris test accuracy:", round(clf.score(Xi_te_s, yi_te), 3))
print("predicted labels   :", clf.predict(Xi_te_s)[:12])
print("class probabilities:", np.round(clf.predict_proba(Xi_te_s)[:3], 3))


# =====================================================================
# PART 1 - BUILD A REALISTIC CHURN DATASET
# =====================================================================
banner("PART 1 - A SYNTHETIC BUT REALISTIC TELECOM CHURN DATASET")

n = 1500
df = pd.DataFrame({
    "age": RNG.integers(18, 75, n),
    "tenure_months": RNG.integers(1, 73, n),
    "monthly_charge": np.round(RNG.normal(68, 22, n).clip(15, 140), 2),
    "support_calls": RNG.poisson(1.6, n),
    "contract": RNG.choice(["month-to-month", "one_year", "two_year"], n,
                           p=[0.55, 0.25, 0.20]),
    "internet_service": RNG.choice(["fiber", "dsl", "none"], n,
                                   p=[0.45, 0.40, 0.15]),
    "paperless_billing": RNG.choice(["yes", "no"], n, p=[0.6, 0.4]),
})

logit = (-2.20
         + 0.030 * df["support_calls"]
         + 0.011 * df["monthly_charge"]
         - 0.028 * df["tenure_months"]
         + 1.15 * (df["contract"] == "month-to-month")
         + 0.45 * (df["internet_service"] == "fiber")
         + 0.20 * (df["paperless_billing"] == "yes"))
df["churn"] = RNG.binomial(1, 1 / (1 + np.exp(-logit)))

# punch realistic holes in the data
for col, frac in [("monthly_charge", 0.04), ("internet_service", 0.03),
                  ("tenure_months", 0.02)]:
    df.loc[RNG.random(n) < frac, col] = np.nan

print("shape:", df.shape)
print("churn rate: {:.1%}".format(df["churn"].mean()))
print("missing values per column:\n", df.isna().sum().to_string())

numerical_features = ["age", "tenure_months", "monthly_charge", "support_calls"]
categorical_features = ["contract", "internet_service", "paperless_billing"]
target = "churn"


# =====================================================================
# PART 2 - QUICK EDA
# =====================================================================
banner("PART 2 - EXPLORATORY DATA ANALYSIS")

rate_by_contract = df.groupby("contract")["churn"].mean().sort_values(ascending=False)
print("churn rate by contract type:\n", (rate_by_contract * 100).round(1).to_string())
print("\nmean monthly charge by churn status:\n",
      df.groupby("churn")["monthly_charge"].mean().round(2).to_string())

fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(rate_by_contract.index, rate_by_contract.values * 100,
              color=["firebrick", "darkorange", "seagreen"][:len(rate_by_contract)])
ax.bar_label(bars, fmt="%.1f%%")
ax.set_ylabel("churn rate (%)")
ax.set_title("Churn rate by contract type - 30 seconds into the meeting")
fig.tight_layout()
fig.savefig(f"{PLOTS}/s01_churn_by_contract.png", dpi=150)
plt.show()


# =====================================================================
# PART 3 - SPLIT + DUMMY BASELINE
# =====================================================================
banner("PART 3 - TRAIN/TEST SPLIT AND THE BASELINE TO BEAT")

X = df.drop(columns=target)
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=RANDOM_STATE)
print(f"train {X_train.shape}  churn {y_train.mean():.1%}")
print(f"test  {X_test.shape}  churn {y_test.mean():.1%}")

dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
d_pred = dummy.predict(X_test)
d_proba = dummy.predict_proba(X_test)[:, 1]
print(f"\nDUMMY baseline -> accuracy {accuracy_score(y_test, d_pred):.3f} | "
      f"F1 {f1_score(y_test, d_pred):.3f} | AUC {roc_auc_score(y_test, d_proba):.3f}")
print("Remember 0.81 accuracy: any model must clearly beat this to be useful.")


# =====================================================================
# PART 4 - PREPROCESSING + MODEL AS ONE PIPELINE
# =====================================================================
banner("PART 4 - ColumnTransformer + Pipeline (leakage-proof)")

numeric_pipe = Pipeline([("imputer", SimpleImputer(strategy="median")),
                         ("scaler", StandardScaler())])
categorical_pipe = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                             ("onehot", OneHotEncoder(handle_unknown="ignore"))])

preprocessor = ColumnTransformer([
    ("num", numeric_pipe, numerical_features),
    ("cat", categorical_pipe, categorical_features)])

rf_pipeline = Pipeline([
    ("prep", preprocessor),
    ("model", RandomForestClassifier(n_estimators=300, min_samples_leaf=3,
                                     class_weight="balanced",
                                     random_state=RANDOM_STATE))])
lr_pipeline = Pipeline([
    ("prep", preprocessor),
    ("model", LogisticRegression(max_iter=2000, class_weight="balanced"))])

print("random-forest pipeline steps:", [name for name, _ in rf_pipeline.steps])


# =====================================================================
# PART 5 - HONEST MODEL COMPARISON WITH CROSS-VALIDATION
# =====================================================================
banner("PART 5 - CROSS-VALIDATED COMPARISON")

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
scoring = ["roc_auc", "accuracy", "precision", "recall", "f1"]

comparison = []
for name, pipe in [("logistic regression", lr_pipeline),
                   ("random forest", rf_pipeline)]:
    res = cross_validate(pipe, X_train, y_train, cv=cv, scoring=scoring,
                         n_jobs=-1)
    row = {"model": name, "fit_time_s": res["fit_time"].mean()}
    for metric in scoring:
        row[metric] = res[f"test_{metric}"].mean()
        row[metric + "_std"] = res[f"test_{metric}"].std()
    comparison.append(row)

comp = pd.DataFrame(comparison).set_index("model")
print(comp.round(3).to_string())
print("\nmean +/- std ROC-AUC:")
for name in comp.index:
    print(f"  {name:20s} {comp.loc[name, 'roc_auc']:.3f} "
          f"+/- {comp.loc[name, 'roc_auc_std']:.3f}")
print("A std this small means the ranking is stable across folds, not luck.")


# =====================================================================
# PART 6 - HYPER-PARAMETER SEARCH
# =====================================================================
banner("PART 6 - GridSearchCV (note the step__parameter naming)")

param_grid = {
    "model__n_estimators": [200, 400],
    "model__max_depth": [None, 10],
    "model__min_samples_leaf": [1, 4],
}
search = GridSearchCV(rf_pipeline, param_grid, scoring="roc_auc", cv=cv,
                      n_jobs=-1, refit=True)
search.fit(X_train, y_train)

print("best params :", search.best_params_)
print(f"best CV AUC : {search.best_score_:.3f}  "
      f"({len(search.cv_results_['params'])} candidates x 5 folds)")
tuned_auc = roc_auc_score(y_test, search.best_estimator_.predict_proba(X_test)[:, 1])
print(f"test AUC of tuned model: {tuned_auc:.3f}  (touched the test set once)")

best = search.best_estimator_
print("expanded feature names from the pipeline:",
      list(best.named_steps["prep"].get_feature_names_out()))


# =====================================================================
# PART 7 - FINAL EVALUATION
# =====================================================================
banner("PART 7 - FINAL EVALUATION ON THE HOLD-OUT TEST SET")

proba = best.predict_proba(X_test)[:, 1]
pred = (proba >= 0.5).astype(int)

print(f"accuracy {accuracy_score(y_test, pred):.3f} | "
      f"precision {precision_score(y_test, pred):.3f} | "
      f"recall {recall_score(y_test, pred):.3f} | "
      f"f1 {f1_score(y_test, pred):.3f} | "
      f"AUC {roc_auc_score(y_test, proba):.3f}")
print("\nclassification report:")
print(classification_report(y_test, pred, target_names=["stayed", "churned"]))

fig, ax = plt.subplots(figsize=(5.5, 4.5))
ConfusionMatrixDisplay.from_predictions(y_test, pred,
                                        display_labels=["stayed", "churned"],
                                        cmap="Blues", colorbar=False, ax=ax)
ax.set_title("Confusion matrix (threshold = 0.5)")
fig.tight_layout()
fig.savefig(f"{PLOTS}/s02_confusion_matrix.png", dpi=150)
plt.show()

fig, ax = plt.subplots(figsize=(6.5, 5.5))
for name, p in [("tuned random forest", proba),
                ("dummy baseline", d_proba)]:
    fpr, tpr, _ = roc_curve(y_test, p)
    ax.plot(fpr, tpr, lw=2, label=f"{name} (AUC = {roc_auc_score(y_test, p):.3f})")
ax.plot([0, 1], [0, 1], "k--", lw=1, label="random guessing")
ax.set_xlabel("false positive rate")
ax.set_ylabel("true positive rate (recall)")
ax.set_title("ROC curve: the model vs the baseline")
ax.legend(loc="lower right")
fig.tight_layout()
fig.savefig(f"{PLOTS}/s03_roc_curve.png", dpi=150)
plt.show()


# =====================================================================
# PART 8 - THRESHOLD TUNING: A BUSINESS DECISION
# =====================================================================
banner("PART 8 - WHERE SHOULD THE CHURN CUT-OFF BE?")

thresholds = np.linspace(0.05, 0.95, 19)
prec = [precision_score(y_test, (proba >= t).astype(int), zero_division=0)
        for t in thresholds]
rec = [recall_score(y_test, (proba >= t).astype(int), zero_division=0)
       for t in thresholds]
f1s = [f1_score(y_test, (proba >= t).astype(int), zero_division=0)
       for t in thresholds]

best_f1_t = thresholds[int(np.argmax(f1s))]
candidates = [(t, p, r) for t, p, r in zip(thresholds, prec, rec) if p >= 0.60]
recall_first_t = candidates[0][0] if candidates else best_f1_t

print(f"max-F1 threshold          : {best_f1_t:.2f} "
      f"(F1 = {max(f1s):.3f})")
print(f"recall-first threshold    : {recall_first_t:.2f} "
      f"(precision >= 0.60, recall = {recall_score(y_test, (proba >= recall_first_t).astype(int)):.3f})")
print(f"customers flagged at 0.50 : {(proba >= 0.50).sum()} of {len(proba)}")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(thresholds, prec, "o-", label="precision (of those flagged, how many churn)")
ax.plot(thresholds, rec, "s-", label="recall (of real churners, how many caught)")
ax.plot(thresholds, f1s, "^--", label="F1 (balance of the two)")
ax.axvline(0.5, color="grey", ls=":", label="scikit-learn default 0.5")
ax.axvline(best_f1_t, color="green", ls="--", alpha=0.7,
           label=f"max-F1 threshold {best_f1_t:.2f}")
ax.set_xlabel("probability threshold")
ax.set_ylabel("score")
ax.set_title("The threshold is a business lever, not a mathematical answer")
ax.legend(fontsize=9)
fig.tight_layout()
fig.savefig(f"{PLOTS}/s04_threshold_tuning.png", dpi=150)
plt.show()


# =====================================================================
# PART 9 - INTERPRETATION: PERMUTATION IMPORTANCE
# =====================================================================
banner("PART 9 - WHICH FEATURES DOES THE MODEL RELY ON?")

perm = permutation_importance(best, X_test, y_test, n_repeats=10,
                              random_state=RANDOM_STATE, scoring="roc_auc",
                              n_jobs=-1)
order = perm.importances_mean.argsort()
feature_names = list(X_test.columns)

print("feature reliance (drop in test AUC when the column is shuffled):")
for i in reversed(order):
    print(f"  {feature_names[i]:20s} {perm.importances_mean[i]:+.4f} "
          f"+/- {perm.importances_std[i]:.4f}")

fig, ax = plt.subplots(figsize=(8, 5))
ax.boxplot(perm.importances[order].T, vert=False)
ax.set_yticks(range(len(order)))
ax.set_yticklabels([feature_names[i] for i in order])
ax.axvline(0, color="black", lw=0.8)
ax.set_xlabel("drop in test ROC-AUC when the feature is shuffled")
ax.set_title("Permutation importance: the report you show the business")
fig.tight_layout()
fig.savefig(f"{PLOTS}/s05_permutation_importance.png", dpi=150)
plt.show()


# =====================================================================
# PART 10 - LEARNING CURVE: MORE DATA OR A BETTER MODEL?
# =====================================================================
banner("PART 10 - LEARNING CURVE")

sizes, train_scores, val_scores = learning_curve(
    best, X_train, y_train, cv=cv, scoring="roc_auc",
    train_sizes=np.linspace(0.1, 1.0, 6), n_jobs=-1)

tr_mean, tr_std = train_scores.mean(1), train_scores.std(1)
va_mean, va_std = val_scores.mean(1), val_scores.std(1)

for s, tm, vm in zip(sizes, tr_mean, va_mean):
    print(f"train size {s:5d} | train AUC {tm:.3f} | validation AUC {vm:.3f}")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(sizes, tr_mean, "o-", label="training score")
ax.fill_between(sizes, tr_mean - tr_std, tr_mean + tr_std, alpha=0.15)
ax.plot(sizes, va_mean, "s-", label="cross-validation score")
ax.fill_between(sizes, va_mean - va_std, va_mean + va_std, alpha=0.15)
ax.set_xlabel("training set size")
ax.set_ylabel("ROC-AUC")
ax.set_title("Learning curve: converging curves mean more rows won't help")
ax.legend()
fig.tight_layout()
fig.savefig(f"{PLOTS}/s06_learning_curve.png", dpi=150)
plt.show()


# =====================================================================
# PART 11 - PERSIST AND SCORE NEW CUSTOMERS
# =====================================================================
banner("PART 11 - SAVE, RELOAD, SCORE NEW CUSTOMERS")

joblib.dump(best, "churn_pipeline.joblib")
print("saved pipeline -> churn_pipeline.joblib")

loaded = joblib.load("churn_pipeline.joblib")
new_customers = pd.DataFrame([
    {"age": 24, "tenure_months": 2,  "monthly_charge": 95.0, "support_calls": 4,
     "contract": "month-to-month", "internet_service": "fiber", "paperless_billing": "yes"},
    {"age": 61, "tenure_months": 68, "monthly_charge": 40.0, "support_calls": 0,
     "contract": "two_year", "internet_service": "dsl", "paperless_billing": "no"},
    {"age": 35, "tenure_months": 14, "monthly_charge": np.nan, "support_calls": 2,
     "contract": "one_year", "internet_service": None, "paperless_billing": "yes"},
])

new_proba = loaded.predict_proba(new_customers)[:, 1]
out = new_customers.assign(churn_probability=np.round(new_proba, 3))
out["action"] = np.where(new_proba >= recall_first_t,
                         "high risk -> retention offer", "monitor")
print(out[["tenure_months", "contract", "churn_probability", "action"]].to_string(index=False))
print("\nNote: raw rows with missing values and unseen categories -> no manual")
print("preprocessing needed, because the whole pipeline was saved as one object.")


# =====================================================================
# PART 12 - CHEAT SHEET
# =====================================================================
banner("CHEAT SHEET")
for line in [
    "split      : train_test_split(X, y, test_size=.25, stratify=y, random_state=42)",
    "preprocess : ColumnTransformer([...numeric..., ...categorical...])",
    "combine    : Pipeline([('prep', preprocessor), ('model', estimator)])",
    "compare    : cross_validate(pipe, X, y, cv=StratifiedKFold(5), scoring=[...])",
    "baseline   : DummyClassifier(strategy='most_frequent')",
    "tune       : GridSearchCV(pipe, {'model__param': [...]}, scoring='roc_auc', cv=5)",
    "threshold  : choose it from a precision/recall curve, not by default",
    "interpret  : permutation_importance(model, X_test, y_test)",
    "diagnose   : learning_curve(...) -> more data or a better model?",
    "ship       : joblib.dump(pipe, 'model.joblib')  /  joblib.load('model.joblib')",
]:
    print(line)
print("\nPlots written to plots/: s01..s06")
print("DONE - you have now shipped a complete, honest, interpretable ML pipeline.")
```

---

## How the three files fit together

| Order | File                               | Question it answers                                                |
| ----- | ---------------------------------- | ------------------------------------------------------------------ |
| 1     | `supervised_learning.md` / `.py`   | How do I predict a number or a class when I have labelled answers? |
| 2     | `unsupervised_learning.md` / `.py` | How do I find structure when I have **no** answers?                |
| 3     | `scikit_learn_tutorial.md` / `.py` | How do I build, tune, interpret and ship any of it professionally? |

Each `.md` ends with a standalone, dependency-light script: save the fenced block as the matching `.py` file and run it. Every script writes its figures into `plots/` before displaying them, and each one finishes in a few seconds to about a minute (the scikit-learn one is the slowest, because of the grid search and learning curve — reduce `n_estimators` or the number of `train_sizes` if you want it faster).
````
`````
