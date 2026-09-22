# Supervised Learning: A Beginner's Guide

### With real-world use cases, formula breakdowns, and runnable Python

> **What you'll be able to do by the end of this tutorial**
>
> 1. Explain what supervised learning is and when to use it.
> 2. Build, evaluate, and _interpret_ both a regression and a classification model.
> 3. Avoid the 6 mistakes that break most beginner projects.
> 4. Tie a model to money, so a business will actually use it.

**Files in this tutorial**

```
supervised-learning-tutorial/
├── supervised_learning_tutorial.md    <- you are here
├── supervised_learning_tutorial.py    <- runnable code for every demo
└── plots/                             <- every figure is saved here automatically
```

**Setup**

```bash
pip install numpy pandas scikit-learn matplotlib
python supervised_learning_tutorial.py
```

Requires `scikit-learn >= 1.0`, `matplotlib >= 3.5`, `pandas >= 1.3`.

---

## Table of contents

- [Supervised Learning: A Beginner's Guide](#supervised-learning-a-beginners-guide)
  - [With real-world use cases, formula breakdowns, and runnable Python](#with-real-world-use-cases-formula-breakdowns-and-runnable-python)
  - [Table of contents](#table-of-contents)
  - [1. What is supervised learning?](#1-what-is-supervised-learning)
    - [Two flavours you'll also hear about](#two-flavours-youll-also-hear-about)
  - [2. Regression vs. classification](#2-regression-vs-classification)
  - [3. The 7-step supervised learning workflow](#3-the-7-step-supervised-learning-workflow)
  - [4. Vocabulary cheat sheet](#4-vocabulary-cheat-sheet)
  - [5. Splitting data and cross-validation](#5-splitting-data-and-cross-validation)
  - [6. Regression, built piece by piece](#6-regression-built-piece-by-piece)
    - [6.1 The model](#61-the-model)
    - [6.2 The loss: mean squared error (MSE), broken down](#62-the-loss-mean-squared-error-mse-broken-down)
    - [6.3 How training actually happens: gradient descent](#63-how-training-actually-happens-gradient-descent)
    - [6.4 The code (Demo 1 in the script)](#64-the-code-demo-1-in-the-script)
    - [6.5 Regression metrics, decoded](#65-regression-metrics-decoded)
  - [7. Classification, built piece by piece](#7-classification-built-piece-by-piece)
    - [7.1 From a line to a probability: the sigmoid](#71-from-a-line-to-a-probability-the-sigmoid)
    - [7.2 The loss: log loss (binary cross-entropy)](#72-the-loss-log-loss-binary-cross-entropy)
    - [7.3 The decision threshold — the most under-used knob in ML](#73-the-decision-threshold--the-most-under-used-knob-in-ml)
    - [7.4 The confusion matrix, decoded](#74-the-confusion-matrix-decoded)
    - [7.5 Precision, recall, F1 — piece by piece](#75-precision-recall-f1--piece-by-piece)
    - [7.6 ROC curve and AUC](#76-roc-curve-and-auc)
    - [7.7 The code (Demo 2 in the script)](#77-the-code-demo-2-in-the-script)
  - [8. Beyond the linear models](#8-beyond-the-linear-models)
  - [9. Overfitting, underfitting, and regularization](#9-overfitting-underfitting-and-regularization)
  - [10. Comparing models properly](#10-comparing-models-properly)
  - [11. Business case 1: customer churn (classification)](#11-business-case-1-customer-churn-classification)
  - [12. Business case 2: house prices (regression)](#12-business-case-2-house-prices-regression)
  - [13. Use-case catalogue by industry](#13-use-case-catalogue-by-industry)
  - [14. Common pitfalls and a pre-flight checklist](#14-common-pitfalls-and-a-pre-flight-checklist)
  - [15. Glossary](#15-glossary)
  - [16. Exercises](#16-exercises)
  - [Where to go next](#where-to-go-next)

---

## 1. What is supervised learning?

**Supervised learning = learning a mapping from inputs to known answers.**

You have a table of historical examples. Each row has **features** (what you know)
and a **target/label** (what you want to predict). The algorithm finds a rule that
turns features into the target. Then you use that rule on new rows where the target
is unknown.

**The everyday analogy: learning from a labelled photo album.**
A child learns "dog" not from a definition but from you pointing at hundreds of
pictures saying "dog", "not a dog", "dog". Supervised learning is exactly that:
show enough labelled examples and the machine generalises the pattern.

```text
   TRAINING PHASE (you have the answers)
   ┌──────────────┬──────────────┬─────────┐
   │ tenure_months│ monthly_charge│ churned │   <- "churned" is the label
   ├──────────────┼──────────────┼─────────┤
   │ 2            │ 89.50         │ 1       │
   │ 61           │ 45.00         │ 0       │
   │ 14           │ 72.30         │ 1       │
   └──────────────┴──────────────┴─────────┘
                    │
                    ▼  algorithm finds the pattern
   PREDICTION PHASE (you do NOT have the answer)
   ┌──────────────┬──────────────┬─────────┐
   │ 8            │ 95.10         │   ?     │ -> model says P(churn) = 0.81
   └──────────────┴──────────────┴─────────┘
```

### Two flavours you'll also hear about

|                    | Supervised                                                                        | Unsupervised                                              | Reinforcement                           |
| ------------------ | --------------------------------------------------------------------------------- | --------------------------------------------------------- | --------------------------------------- |
| Answers available? | Yes, labels provided                                                              | No labels                                                 | No labels; reward signal                |
| Goal               | Predict the label                                                                 | Find structure                                            | Learn a policy by trial and error       |
| Typical task       | Churn, price, spam, fraud                                                         | Segmentation, anomaly detection, dimensionality reduction | Game playing, robot control, ad bidding |
| Algorithms         | Linear/logistic regression, trees, random forest, boosting, SVM, kNN, neural nets | K-means, DBSCAN, PCA, autoencoders                        | Q-learning, policy gradients            |

**Rough rule:** if a human could label past cases and you can afford a bit of
labeling effort, start with supervised learning. It is by far the most common
type of ML in production business systems.

**When supervised learning is a bad fit:** you have no labels and cannot get them;
the world changes so fast that history is useless; or the decision needs a
human-readable legal justification that the model cannot provide.

---

## 2. Regression vs. classification

The _only_ thing that decides this is the **type of the label**.

|                   | **Regression**                                                  | **Classification**                                      |
| ----------------- | --------------------------------------------------------------- | ------------------------------------------------------- |
| Label type        | Continuous number                                               | A category                                              |
| Examples          | Price = 412,500<br>Demand = 1,840 units<br>Wait time = 12.4 min | Churn = yes/no<br>Digit = 0–9<br>Risk = low/medium/high |
| Output            | A number                                                        | A class, usually + a probability                        |
| Typical metrics   | MAE, RMSE, R²                                                   | Accuracy, precision, recall, F1, ROC-AUC                |
| Business question | "How much?"                                                     | "Which one?" / "Will it happen?"                        |

> **Watch out:** "predict how many items a customer will buy" is regression
> (0, 1, 2, 3 …), while "predict whether they buy at all" is classification.
> Same data, different question, different tool.

Everything else in the workflow — cleaning, splitting, cross-validating,
regularizing — is shared.

---

## 3. The 7-step supervised learning workflow

```text
 1. Frame the question      → what decision does this model change?
 2. Collect & clean data    → features (X), label (y), handle missing values
 3. Split the data          → train / validation / test (NEVER touch test early)
 4. Train baseline          → simplest model first (mean, or logistic regression)
 5. Evaluate honestly       → cross-validation + the right metric
 6. Tune & compare          → hyperparameters, model families, feature engineering
 7. Ship & monitor          → threshold choice, drift checks, retraining
```

The step beginners skip is **1**, and it is the step that decides whether the
project matters. "Predict churn" is not a goal. "Rank the 5% of customers most
likely to churn so the retention team can call 200 people per day" is a goal —
and it immediately tells you the metric (recall at a fixed capacity) and the
threshold (call 200 people, not "use 0.5").

Steps 2–4 in code, the shortest possible version:

```python
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("customers.csv")
X = df.drop(columns=["churned"])     # features
y = df["churned"]                    # label

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0, stratify=y)   # stratify keeps the churn rate equal
```

---

## 4. Vocabulary cheat sheet

| Term                     | Plain-English meaning                                                                                              |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| **Feature** (`X`)        | An input column, e.g. `tenure_months`. Also called predictor, attribute, independent variable.                     |
| **Label / target** (`y`) | The answer you predict, e.g. `churned`.                                                                            |
| **Sample / row**         | One example (one customer, one house, one transaction).                                                            |
| **Model**                | The learned rule that maps `X` → `y`.                                                                              |
| **Training**             | The process of fitting the model to labelled data.                                                                 |
| **Hyperparameter**       | A setting you choose _before_ training (tree depth, `k` in k-NN). Learned numbers are **parameters** (weights).    |
| **Loss / cost function** | A number that measures how wrong the model is; training minimises it.                                              |
| **Gradient descent**     | The algorithm that walks downhill on the loss surface.                                                             |
| **Overfitting**          | Memorising the training data; great on train, poor on new data.                                                    |
| **Underfitting**         | Too simple to capture the pattern; poor everywhere.                                                                |
| **Regularization**       | A penalty that discourages complexity (L1/lasso, L2/ridge).                                                        |
| **Inference**            | Using a trained model to make a prediction.                                                                        |
| **Pipeline**             | A container that chains preprocessing + model so the same steps are applied at train and predict time.             |
| **Leakage**              | Accidentally giving the model information it would not have in production (e.g. fitting a scaler on the test set). |

---

## 5. Splitting data and cross-validation

Your model must be judged on data it has **never seen**. Otherwise you are
grading a student on the exact questions they memorised.

```text
   All labelled data (100%)
   ├──────────────────────────── Train (60–70%)  → fit the weights
   ├──────────────────────────── Validation (15–20%) → tune hyperparameters, pick the model
   └──────────────────────────── Test (15–20%)  → touched ONCE, at the very end
```

**Why a separate validation set or cross-validation?**
If you tune on the test set, your test score becomes optimistic and your model
will disappoint in production. Cross-validation solves this efficiently:

```text
   5-fold cross-validation (on the training portion)
   fold 1: [VALID][train][train][train][train]  -> score 0.94
   fold 2: [train][VALID][train][train][train]  -> score 0.95
   fold 3: [train][train][VALID][train][train]  -> score 0.93
   fold 4: [train][train][train][VALID][train]  -> score 0.96
   fold 5: [train][train][train][train][VALID]  -> score 0.94
   final score = 0.944 ± 0.010   <- the spread matters as much as the mean
```

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)   # use KFold for regression
scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
print(f"{scores.mean():.4f} +/- {scores.std():.4f}")
```

**Golden rule:** every preprocessing step that _learns_ something (scaling,
imputation, encoding, feature selection) must be fitted **inside** the
cross-validation fold. `sklearn`'s `Pipeline` does this for you — always use it.

**Time-series warning:** never split randomly on time-ordered data. Train on the
past, test on the future (`TimeSeriesSplit`), or you are effectively predicting
yesterday using tomorrow's news.

---

## 6. Regression, built piece by piece

### 6.1 The model

Simple linear regression with one feature:

```text
   ŷ = w · x + b

   ŷ  = the prediction                  ("y-hat")
   x  = the input feature
   w  = the weight (slope): how much ŷ changes when x grows by 1
   b  = the bias (intercept): the prediction when x = 0
```

With several features it becomes `ŷ = w₁x₁ + w₂x₂ + … + wₙxₙ + b`, which in
matrix form is `ŷ = Xw + b`. Nothing conceptually changes — each weight is
"the effect of that feature, holding the others fixed".

### 6.2 The loss: mean squared error (MSE), broken down

```text
   MSE = (1/n) · Σ (yᵢ - ŷᵢ)²

   yᵢ - ŷᵢ      → the residual: how far off we were on example i
   (…)²         → square it: makes all errors positive and punishes big misses hard
   Σ            → add up over all n examples
   (1/n)        → average, so the score doesn't depend on dataset size
```

Why square instead of absolute value? It is smooth and differentiable
everywhere, which makes the maths (and gradient descent) clean. The cost is
sensitivity to outliers — one huge error dominates. Use **MAE** if outliers are
a real feature of your data.

### 6.3 How training actually happens: gradient descent

We compute the slope of the loss with respect to each parameter and step
_downhill_:

```text
   w ← w - α · ∂MSE/∂w
   b ← b - α · ∂MSE/∂b

   α (alpha) = learning rate: how big a step we take
   ∂MSE/∂w   = 2 · mean( (ŷ - y) · x )
   ∂MSE/∂b   = 2 · mean( (ŷ - y) )
```

| Piece                      | Meaning                    | If it's wrong                              |
| -------------------------- | -------------------------- | ------------------------------------------ |
| `α` too small              | Tiny steps                 | Training crawls, may never converge        |
| `α` too large              | Huge steps                 | Loss bounces or explodes (NaN)             |
| `∂MSE/∂w`                  | Direction + steepness      | This is the "which way is downhill" signal |
| Repeat for many **epochs** | Whole passes over the data | Stop when the loss flattens                |

That is the whole of "training a model" for linear regression. Neural networks
use exactly the same loop — just many more parameters and a chain rule to
compute the gradients.

### 6.4 The code (Demo 1 in the script)

```python
import numpy as np
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(42)
x = rng.uniform(0, 10, 300)
y = 3.0 * x + 5.0 + rng.normal(0, 2.5, 300)      # true rule + noise

# Standardise: gradient descent converges much faster on a ~N(0,1) feature
x_mean, x_std = x.mean(), x.std()
xs = (x - x_mean) / x_std

w, b, lr, epochs = 0.0, 0.0, 0.1, 400
history = []
for _ in range(epochs):
    y_hat = w * xs + b
    error = y_hat - y
    history.append(np.mean(error ** 2))          # MSE, for the plot
    w -= lr * 2 * np.mean(error * xs)            # ∂MSE/∂w
    b -= lr * 2 * np.mean(error)                 # ∂MSE/∂b

# Convert the standardised weights back to original units
slope = w / x_std
intercept = b - w * x_mean / x_std
print(f"learned: y = {slope:.3f}x + {intercept:.3f}   (true: 3.000x + 5.000)")

# Sanity check against scikit-learn
sk = LinearRegression().fit(xs.reshape(-1, 1), y)
print(f"sklearn: y = {sk.coef_[0] / x_std:.3f}x + {sk.intercept_ - sk.coef_[0] * x_mean / x_std:.3f}")
```

Expected output:

```text
learned: y = 2.988x + 5.179   (true: 3.000x + 5.000)
sklearn: y = 2.988x + 5.179
final MSE: 6.34  (noise variance ~ 6.25)
```

Two lessons from that output:

1. The model recovers the true rule almost exactly — a good sign your pipeline works.
2. The final MSE lands near the noise variance (2.5² ≈ 6.25). You can never beat
   the irreducible noise; chasing a lower training loss just means overfitting.

**Graph walkthrough (saved as `plots/01_gradient_descent.png`)**

- _Left panel, loss vs. epoch:_ a steep drop then a long flat tail. The elbow is
  where the model has essentially converged. If the curve is still falling, train
  longer; if it oscillates, lower `α`.
- _Right panel, data + fitted line:_ the red fitted line should sit right on top
  of the dashed true line. A visibly different slope means the learning rate or
  the number of epochs is off — not that the algorithm is broken.

### 6.5 Regression metrics, decoded

```text
   MAE  = (1/n) · Σ |yᵢ - ŷᵢ|
          "average miss, in the same units as y" — easy to explain, outlier-tolerant

   RMSE = √( (1/n) · Σ (yᵢ - ŷᵢ)² )
          "average miss, but big errors hurt disproportionately" — same units as y

   R²   = 1 - SS_res / SS_tot
          SS_res = Σ (yᵢ - ŷᵢ)²          (your model's squared error)
          SS_tot = Σ (yᵢ - ȳ)²           (the error of always predicting the mean)

          R² = 1.0  -> perfect
          R² = 0.0  -> exactly as good as predicting the mean
          R² < 0.0  -> WORSE than predicting the mean (yes, this happens)
```

Piece by piece for R²: the denominator is your **baseline** — the dumbest
possible model (always guess the average). The numerator is your model's error.
So R² answers: _"what fraction of the variation did I explain away?"_

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

pred = model.predict(X_test)
print("MAE ", mean_absolute_error(y_test, pred))
print("RMSE", np.sqrt(mean_squared_error(y_test, pred)))   # use np.sqrt for version safety
print("R2  ", r2_score(y_test, pred))
```

> **Reporting tip:** always give MAE or RMSE _in currency_ ("on average we are
> £28,400 off") rather than only R². Stakeholders cannot act on 0.83.

---

## 7. Classification, built piece by piece

### 7.1 From a line to a probability: the sigmoid

Logistic regression computes a linear score, then squashes it into [0, 1]:

```text
   z = w·x + b                  (the same linear score as regression)
   p = σ(z) = 1 / (1 + e^(-z))  (the sigmoid function)

   z = 0    -> p = 0.50   (coin flip)
   z = +2   -> p = 0.88
   z = -2   -> p = 0.12
   z = ±10  -> p ≈ 1 or 0  (confident, but never exactly 0 or 1)
```

Piece by piece:

- `e^(-z)` — the exponential; makes the output positive and lets negative scores
  map into a shrinking denominator.
- `1/(1+…)` — forces the result into the interval (0, 1), which is exactly what a
  probability needs.
- The curve is S-shaped: near z = 0, small changes in z move the probability a
  lot; far out, changes barely matter. It compresses confidence at the extremes
  instead of going infinite like a straight line would.

### 7.2 The loss: log loss (binary cross-entropy)

```text
   LogLoss = -(1/n) · Σ [ yᵢ·log(pᵢ) + (1 - yᵢ)·log(1 - pᵢ) ]

   If the true label yᵢ = 1:  only  -log(pᵢ)  survives  -> punished when p is small
   If the true label yᵢ = 0:  only  -log(1-pᵢ) survives -> punished when p is large
```

The two terms are "switches": whichever one is not active is multiplied by zero.
Piece by piece, for a true positive:

- `p = 0.99` → `-log(0.99) = 0.01` → almost no penalty. Good.
- `p = 0.01` → `-log(0.01) = 4.6` → heavy penalty. Confidently wrong is expensive.
- The `-` sign flips the concave `log` into a loss we can minimise.

This is why accuracy is a bad training objective (it has zero gradient almost
everywhere) while log loss gives smooth, informative feedback.

### 7.3 The decision threshold — the most under-used knob in ML

A classifier outputs a probability. To act, you must cut it:

```text
   predict "churn" if  p ≥ t            t = 0.5 by default

   Lower t  -> flag more people -> higher recall, lower precision
   Higher t -> flag fewer people -> lower recall, higher precision
```

The "right" threshold is a **business** decision, not a statistical one. If a
retention call costs £50 and saves £300, you may be happy with 40% precision.

### 7.4 The confusion matrix, decoded

```text
                        PREDICTED
                     no           yes
              ┌─────────────┬─────────────┐
   ACTUAL no  │     TN      │     FP      │  FP = false alarm
              │  (correct)  │  (annoying) │
              ├─────────────┼─────────────┤
   ACTUAL yes │     FN      │     TP      │  FN = the one you missed
              │  (missed!)  │  (correct)  │
              └─────────────┴─────────────┘
```

| Cell | Name           | Cost in the churn example                  |
| ---- | -------------- | ------------------------------------------ |
| TN   | True negative  | Nothing; correctly left alone              |
| FP   | False positive | Wasted offer + a slightly annoyed customer |
| FN   | False negative | A customer silently walks away             |
| TP   | True positive  | A saved customer                           |

Which error is worse is _entirely_ problem-dependent: in cancer screening a
false negative can kill someone, so you accept many false positives. In spam
filtering a false positive is worse (a lost business email). Always ask before
tuning.

### 7.5 Precision, recall, F1 — piece by piece

```text
   Precision = TP / (TP + FP)
       "of everyone I flagged, what fraction really churned?"
       Precision is about the QUALITY of the alarm.

   Recall (sensitivity) = TP / (TP + FN)
       "of everyone who really churned, what fraction did I catch?"
       Recall is about the COVERAGE of the alarm.

   F1 = 2 · (Precision · Recall) / (Precision + Recall)
       The harmonic mean: high only if BOTH are high.
       Use it when you have no currency to convert errors into.

   Accuracy = (TP + TN) / (TP + TN + FP + FN)
       Can be 91% and completely useless if only 9% of rows are positive.
```

Why the harmonic mean and not the plain average? The arithmetic mean of
precision = 1.0 and recall = 0.0 is 0.5, which sounds acceptable but is a
disaster (the model predicts one positive and misses everything else). The
harmonic mean correctly collapses to 0.

> **Class imbalance example (Demo 4 in the code):** with a 24% churn rate, a model
> that predicts "nobody churns" scores 76% accuracy and finds 0 churners.
> Accuracy is fine for balanced problems; for rare events use precision/recall,
> F1, or ROC-AUC / PR-AUC.

### 7.6 ROC curve and AUC

```text
   Sweep the threshold from 1 down to 0.
   At each threshold plot:
       x-axis: False Positive Rate = FP / (FP + TN)   <- cost of false alarms
       y-axis: True Positive Rate  = TP / (TP + FN)   <- same as recall

   AUC = area under that curve
       0.5 = random guessing (the diagonal)
       0.7 = weak, 0.8 = decent, 0.9 = strong
       1.0 = perfect separation
```

Reading it: AUC is **threshold-free** — it answers "if I pick one random churner
and one random non-churner, how often does the model score the churner higher?"
That makes it great for ranking models, but it says nothing about whether your
chosen threshold earns money. Use AUC to _choose_ the model, precision/recall at
the operating threshold to _run_ it.

### 7.7 The code (Demo 2 in the script)

```python
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score

X, y = load_breast_cancer(as_frame=True, return_X_y=True)   # 0 = malignant, 1 = benign
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0, stratify=y)

model = Pipeline([
    ("scaler", StandardScaler()),                 # scale INSIDE the pipeline (no leakage)
    ("clf", LogisticRegression(max_iter=5000)),
]).fit(X_train, y_train)

y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]       # column 1 = P(benign)

print(classification_report(y_test, y_pred, target_names=["malignant", "benign"], digits=3))
print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")
```

**Graph walkthrough (saved as `plots/02_classification_metrics.png`)**

- _Panel 1 (sigmoid):_ the S-curve. The dashed horizontal line at 0.5 is the
  default threshold; the dashed vertical line is the decision boundary in score
  space.
- _Panel 2 (confusion matrix):_ read it row by row. Row 0 = malignant. Anything
  in the top-right (malignant predicted as benign) is a clinically dangerous
  false negative — this is the number a doctor cares about.
- _Panel 3 (ROC curve):_ the closer the curve hugs the top-left corner, the
  better. The diagonal is coin-flipping. A steep initial rise means the model
  finds real positives long before it starts firing false alarms.

Deep-dive: the log-loss and coefficient math that makes logistic regression
interpretable-as-odds is in the script's printed output — a coefficient of +1.2
means the odds of the positive class multiply by `e^1.2 ≈ 3.3` per unit increase
in that feature.

---

## 8. Beyond the linear models

You do not need to master all of these. Know **what they are, when they win, and
their cost**, then try two or three per project.

| Model                                                    | Core idea                                                               | Wins when                                          | Watch out for                                                     |
| -------------------------------------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------- |
| **Linear / logistic regression**                         | A weighted sum of features                                              | Few features, need explainability, strong baseline | Cannot capture interactions unless you build them                 |
| **k-NN**                                                 | "You are the average of your k nearest neighbours" (Euclidean distance) | Tiny data, weird shapes, no training time          | Slow at prediction; scaling is mandatory; curse of dimensionality |
| **Decision tree**                                        | Recursively split on the feature that reduces impurity most             | You need human-readable rules                      | Overfits by default; unstable                                     |
| **Random forest**                                        | Average many decorrelated trees (bagging + feature subsampling)         | Tabular data, little tuning, robust default        | Large and slow to explain; smooths away extremes                  |
| **Gradient boosting** (XGBoost / LightGBM / sklearn GBM) | Fit trees to the _residuals_ of the previous trees, sequentially        | Best accuracy on most tabular problems             | More tuning; can overfit noisy labels                             |
| **SVM (RBF kernel)**                                     | Find the max-margin boundary in a high-dimensional space                | Small/medium data, many features, clear margin     | O(n²)+ scaling, opaque, no native probabilities                   |
| **Neural network**                                       | Layers of learned non-linear transformations                            | Images, text, audio, huge data                     | Needs lots of data and compute; least interpretable               |

**Decision-tree splitting math (piece by piece — it underlies all the forests):**

```text
   Gini impurity of a node = 1 - Σ pₖ²
       pₖ = fraction of samples in the node belonging to class k
       0.0 = perfectly pure (all one class), 0.5 = maximally mixed (binary case)
       Example: 70% churn / 30% no-churn -> 1 - (0.7² + 0.3²) = 1 - 0.58 = 0.42

   Information gain = impurity(parent) - Σ (n_child / n_parent) · impurity(child)

   The tree tries every feature and every split point, and keeps the split with
   the largest gain. Repeat recursively, then stop by depth / leaf size / gain.
```

A tree that splits until every leaf is pure has memorised the training set —
which is exactly why the forest (averaging many such trees) is the practical tool.

**Practical ranking for tabular business data:**
`logistic/linear regression (baseline) → random forest → gradient boosting → (only if needed) neural nets`.

---

## 9. Overfitting, underfitting, and regularization

The central tension of all machine learning:

```text
   error
     │  \                      total error
     │   \                    /
     │    \                  /
     │     \________________/
     │      \  validation   /
     │       \            /
     │        \          /   training error keeps falling ->
     │         \________/
     └──────────────────────────────────────► model complexity
          underfitting   |   overfitting
          (too simple)   |   (too complex)
                     sweet spot
```

| Symptom                               | Diagnosis                      | Fix                                                                                 |
| ------------------------------------- | ------------------------------ | ----------------------------------------------------------------------------------- |
| Train 0.99, test 0.68                 | Overfitting                    | More data, simpler model, regularization, pruning, early stopping, fewer features   |
| Train 0.71, test 0.70                 | Underfitting                   | More features, more complex model, less regularization, better features             |
| Train 0.99, CV 0.98 ± 0.01, test 0.62 | Distribution shift or leakage  | Check how the test set was built; check for features unavailable at prediction time |
| Huge variance between folds           | Small dataset / unstable model | More folds, repeated CV, simpler model                                              |

**Regularization piece by piece:**

```text
   Ridge  (L2):  loss + λ · Σ wᵢ²          -> shrinks weights smoothly toward 0
   Lasso  (L1):  loss + λ · Σ |wᵢ|         -> can set weights exactly to 0 (feature selection)
   ElasticNet  :  a mix of both

   λ (lambda, called C in scikit-learn for its INVERSE) controls the trade-off:
       λ = 0        -> no penalty, maximum overfitting risk
       λ → ∞        -> weights forced to 0, maximum underfitting
```

`scikit-learn` note: `Ridge(alpha=...)` and `LogisticRegression(C=...)` — in
logistic regression **`C` is the inverse of λ**, so _smaller C = stronger
penalty_. This trips up almost everybody once.

```python
from sklearn.linear_model import RidgeCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# RidgeCV picks the best alpha via internal cross-validation
model = Pipeline([("scaler", StandardScaler()), ("ridge", RidgeCV(alphas=[0.01, 0.1, 1, 10, 100]))])
```

**Reading a learning curve** (produced by Demo 3):

- Two curves far apart, training high and validation low → **variance problem**:
  add data or regularize.
- Both curves low and flat, converging together → **bias problem**: the model is
  too simple; get better features.
- Curves converged and high → you are done; more data won't help much.

---

## 10. Comparing models properly

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

models = {
    "Logistic regression": Pipeline([("s", StandardScaler()), ("m", LogisticRegression(max_iter=5000))]),
    "k-NN (k=5)":          Pipeline([("s", StandardScaler()), ("m", KNeighborsClassifier(5))]),
    "Random forest":       RandomForestClassifier(n_estimators=300, random_state=0),
    "Gradient boosting":   GradientBoostingClassifier(random_state=0),
}
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
    print(f"{name:22s} {scores.mean():.4f} +/- {scores.std():.4f}")
```

Rules for a fair comparison:

1. **Same folds for every model.** `StratifiedKFold(shuffle=True, random_state=0)`.
2. **Same preprocessing, fitted inside the pipeline.**
3. **Report the spread, not just the mean.** A 0.005 difference with ±0.02 noise
   is not a winner.
4. **Prefer the simpler model** when scores are within noise — it is cheaper to
   run, easier to explain, and less likely to break.
5. **Tune honestly:** nested cross-validation or a validation split, not the test set.

---

## 11. Business case 1: customer churn (classification)

**Scenario.** A subscription business loses 24% of customers a year. A retention
team can make 200 calls a day. Which customers should they call?

**Why supervised learning fits.** You have years of labelled history (who churned,
who stayed) and the decision — who to call — is exactly a ranking problem.

**The dataset** (generated in the script, so it runs offline): 4,000 customers
with tenure, monthly charges, total charges, support calls, contract type,
internet service, senior flag, plus 120 missing `total_charges` values so you get
to see imputation in action.

**The full pipeline, as you would build it at work:**

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

num_cols = ["tenure_months", "monthly_charges", "total_charges", "support_calls"]
cat_cols = ["contract", "internet_service", "is_senior"]

preprocess = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                      ("scale", StandardScaler())]), num_cols),
    ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                      ("encode", OneHotEncoder(handle_unknown="ignore"))]), cat_cols),
])

clf = Pipeline([("preprocess", preprocess),
                ("model", LogisticRegression(max_iter=5000, class_weight="balanced"))])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0, stratify=y)
clf.fit(X_train, y_train)
```

Five things this snippet encodes, and why each matters:

1. **`ColumnTransformer`** — numeric and categorical columns need different
   treatment; doing it inline is how leakage and production bugs happen.
2. **`SimpleImputer(median)`** — numeric missing values get the median (robust to
   outliers). Then **`StandardScaler`** puts features on comparable scales.
3. **`OneHotEncoder(handle_unknown="ignore")`** — turns `"month-to-month"` into a
   0/1 column and, crucially, does not crash when production sends a contract
   type it never saw in training.
4. **`class_weight="balanced"`** — with 24% churn, the model otherwise ignores the
   minority class.
5. **Everything inside one `Pipeline`** — the exact same transformations are
   applied at predict time. No "but it worked in my notebook".

**Then convert probabilities into money.**

```python
proba = clf.predict_proba(X_test)[:, 1]

VALUE_RETAINED = 300.0   # net value of saving a true churner
COST_OF_OFFER  = 50.0    # cost of a wasted retention offer

for t in [0.2, 0.3, 0.4, 0.5, 0.6]:
    pred = (proba >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, pred, labels=[0, 1]).ravel()
    value = VALUE_RETAINED * tp - COST_OF_OFFER * fp
    print(f"t={t:.1f}  TP={tp:4d}  FP={fp:4d}  expected value = ${value:,.0f}")
```

**Graph walkthrough (saved as `plots/04a_churn_thresholds.png`)**

- _Left panel:_ precision rises with the threshold, recall falls, F1 peaks in the
  middle. This picture shows why "0.5" is arbitrary.
- _Right panel:_ expected value in dollars versus threshold. The peak is your
  operating point. The caption to show your manager: _"Moving the threshold from
  0.50 to 0.25 adds $X of expected value per 1,000 customers at risk."_

**Graph walkthrough (saved as `plots/04b_churn_drivers.png`)**

- _Left panel:_ the confusion matrix at the profit-maximising threshold — read the
  false negatives as "revenue quietly walking out of the door".
- _Right panel:_ logistic-regression coefficients. Positive red bars increase
  churn odds, blue bars decrease them. In the generated data the honest drivers
  are short tenure, month-to-month contracts, fibre internet, more support calls
  and higher monthly charges — the model reproduces them, which is the sanity
  check you should always run before presenting coefficients as "insights".

**How you would actually ship this:** score all customers nightly, take the top
N by probability (a capacity constraint, not a threshold), route them to the
retention team, and log outcomes so you can retrain with the _true_ counterfactual
("would they have churned if we hadn't called?") — a subtle problem known as
uplift modelling.

---

## 12. Business case 2: house prices (regression)

**Scenario.** An estate agency wants an instant valuation before a human agent
visits. Same workflow, different label type: a number, not a class.

The script generates 1,500 houses with a known price formula plus noise, then
compares a linear model with a random forest:

```python
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

lin = LinearRegression().fit(X_train, y_train)
rf  = RandomForestRegressor(n_estimators=400, random_state=0).fit(X_train, y_train)

for name, model in [("linear regression", lin), ("random forest", rf)]:
    pred = model.predict(X_test)
    print(f"{name:18s} MAE={mean_absolute_error(y_test, pred):,.0f}"
          f"  RMSE={np.sqrt(mean_squared_error(y_test, pred)):,.0f}"
          f"  R2={r2_score(y_test, pred):.3f}")
```

Typical result: the forest wins on RMSE (it can capture mild non-linearity), but
the linear model is within a few percent — and it tells you _why_, in pounds per
square foot. For a valuation tool that has to be explained to a client, the
linear model may be the better business choice even when it loses on paper.

**Graph walkthrough (saved as `plots/05_house_price_regression.png`)**

- _Panel 1 (predicted vs. actual):_ points should hug the 45° dashed line. A fan
  shape (wider at high prices) means errors grow with the target — consider
  predicting `log(price)`.
- _Panel 2 (residuals vs. predicted):_ you want a shapeless cloud centred on 0. A
  curve means the model is missing a non-linear effect; a funnel means
  heteroscedasticity; clusters mean a missing categorical feature.
- _Panel 3 (feature importance):_ square footage dominates, as it should. If
  "distance to city centre" came out at ~0 importance while you know it matters,
  suspect a data problem, not a modelling one.

**Business framing:** report "we are on average £18,400 off, and 90% of estimates
are within £35,000" — not "R² = 0.94".

---

## 13. Use-case catalogue by industry

Every row is a supervised problem. Notice how often the _frame_ is
"predict a number" versus "predict a class".

| Industry        | Use case                  | Type                        | Label                    | Typical features                    |
| --------------- | ------------------------- | --------------------------- | ------------------------ | ----------------------------------- |
| Telecom         | Churn prediction          | Classification              | Churned?                 | Tenure, contract, support calls     |
| Banking         | Credit default scoring    | Classification              | Defaulted?               | Income, debt ratio, payment history |
| Banking         | Loan amount / LTV         | Regression                  | Amount                   | Collateral, income                  |
| Insurance       | Claim severity            | Regression                  | Claim £                  | Vehicle, region, history            |
| Insurance       | Fraud flagging            | Classification              | Fraudulent?              | Claim pattern, timing, network      |
| Retail / e-comm | Demand forecasting        | Regression                  | Units sold               | Seasonality, promos, price          |
| Retail / e-comm | Purchase propensity       | Classification              | Will buy?                | Browsing history, recency           |
| Retail          | Customer lifetime value   | Regression                  | CLV £                    | Frequency, monetary value           |
| Marketing       | Ad click-through rate     | Classification              | Clicked?                 | User, ad, context                   |
| Healthcare      | Readmission risk          | Classification              | Readmitted in 30 days?   | Diagnoses, labs, length of stay     |
| Healthcare      | Length of stay / dosage   | Regression                  | Days / mg                | Vitals, demographics                |
| Manufacturing   | Predictive maintenance    | Classification              | Will fail within 7 days? | Sensor streams, vibration           |
| Manufacturing   | Yield / scrap prediction  | Regression                  | Units produced           | Machine settings                    |
| Logistics       | Delivery ETA              | Regression                  | Minutes                  | Distance, traffic, weather          |
| Logistics       | Package damage risk       | Classification              | Damaged?                 | Route, packaging, handling          |
| Energy          | Load forecasting          | Regression                  | MW                       | Weather, calendar, history          |
| HR              | Attrition risk            | Classification              | Will leave?              | Tenure, comp ratio, engagement      |
| Real estate     | Automated valuation       | Regression                  | Price                    | Size, location, age                 |
| Security        | Spam / phishing detection | Classification              | Malicious?               | Text, sender, headers               |
| Media           | Recommendation relevance  | Classification / Regression | Rating or click          | User-item history                   |
| Public sector   | Tax evasion screening     | Classification              | Non-compliant?           | Declared vs. modelled income        |
| SaaS            | Lead scoring              | Classification              | Will convert?            | Firmographics, activity             |
| SaaS            | Support ticket volume     | Regression                  | Tickets                  | Release cycle, users                |

**Pattern to notice:** the _framing_ step ("what decision does this change?") is
where the business value is created, and it is the same reasoning every time —
even though the algorithms barely change.

---

## 14. Common pitfalls and a pre-flight checklist

**The six that break beginner projects**

1. **Leakage.** Fitting a scaler or imputer on the full dataset before splitting;
   including a feature recorded _after_ the outcome (e.g. `cancellation_reason`
   when predicting churn). Symptom: suspiciously perfect scores.
2. **Accuracy on imbalanced data.** 76% accuracy can mean "predicts nothing".
3. **Tuning on the test set.** Your test score quietly becomes a training score.
4. **Ignoring the baseline.** Always beat "predict the mean" (regression) or
   "predict the majority class" (classification).
5. **Correlation-is-not-causation in coefficients.** A model finds associations.
   Acting on them ("raising price reduces churn") requires an experiment.
6. **Train/serve skew.** Notebook uses a pandas `OneHotEncoder` manually; the
   service uses different logic. Fix: one serialised `Pipeline` used everywhere.

**Pre-flight checklist**

- [ ] I can state the decision this model changes and who takes it.
- [ ] The label is defined at a point in time and available at prediction time.
- [ ] I split before I transformed anything.
- [ ] All preprocessing lives inside a `Pipeline` / `ColumnTransformer`.
- [ ] I have a dumb baseline number written down.
- [ ] I used cross-validation and reported mean ± std.
- [ ] I know which error (FP or FN) costs more, and my threshold reflects that.
- [ ] I evaluated on the test set exactly once.
- [ ] I looked at residuals / confusion matrix, not just a single score.
- [ ] I wrote down how I'll detect drift and when I'll retrain.

---

## 15. Glossary

| Term                        | Definition                                                             |
| --------------------------- | ---------------------------------------------------------------------- |
| **Bias (in bias–variance)** | Error from an overly simple model; underfitting.                       |
| **Variance**                | Error from sensitivity to the training sample; overfitting.            |
| **Cross-validation**        | Rotating hold-out splits to estimate generalisation.                   |
| **Epoch**                   | One full pass over the training data during optimisation.              |
| **Feature engineering**     | Creating informative inputs (ratios, dates, aggregates, interactions). |
| **Hyperparameter**          | A configuration chosen before training (depth, `k`, `C`, `λ`).         |
| **Imputation**              | Filling missing values (median, most frequent, model-based).           |
| **Label**                   | The target value you are predicting.                                   |
| **Learning rate**           | Step size in gradient descent.                                         |
| **Log loss**                | Loss for probabilistic classification; punishes confident errors.      |
| **One-hot encoding**        | Turning a category into binary columns.                                |
| **Pipeline**                | Chain of preprocessing + model applied identically at fit and predict. |
| **Precision / Recall**      | Quality / coverage of positive predictions.                            |
| **Regularization**          | Penalising complexity to reduce overfitting.                           |
| **Residual**                | `actual − predicted`.                                                  |
| **ROC-AUC**                 | Threshold-free ranking quality of a classifier.                        |
| **Stratified split**        | A split that preserves class proportions.                              |
| **Train/test split**        | The wall that keeps evaluation honest.                                 |

---

## 16. Exercises

1. In Demo 1, set the learning rate to `0.001` and then `1.5`. Plot both loss
   curves. Explain what you see in terms of the gradient step size.
2. In Demo 2, move the threshold from 0.5 to 0.2. Which metric improves most, and
   which gets worse? Would you do this for cancer screening? For spam?
3. In Demo 3, add a `DecisionTreeClassifier(max_depth=15)`. Where does it land on
   the bar chart, and is its learning-curve gap different from the forest's?
4. In Demo 4, change `COST_OF_OFFER` to 200 and re-run. Why does the optimal
   threshold move? What does that mean operationally?
5. In Demo 4, remove `total_charges` (it leaks future information about tenure).
   Does the score change much? Which is the more trustworthy model?
6. In Demo 5, replace the random forest with `GradientBoostingRegressor`. Compare
   MAE and the residual plot.

---

## Where to go next

1. **Feature engineering** — usually worth more than any model swap.
2. **Gradient boosting** (XGBoost / LightGBM) — the workhorse for tabular data.
3. **Calibration** (`CalibratedClassifierCV`) — if you quote probabilities to anyone.
4. **Causal inference / uplift modelling** — if your decision is "should I intervene?"
   rather than "who is at risk?"
5. **MLOps** — versioning, monitoring, retraining, drift detection.
6. **Responsible ML** — fairness metrics, explainability (SHAP), documentation.
