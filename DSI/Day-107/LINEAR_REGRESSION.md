# Linear Regression — A Practical Tutorial for Beginners

> **Machine Learning · Supervised Learning · Regression**
> Difficulty: ⭐ Beginner-friendly | Time: ~45 min

---

## 1. What is Linear Regression?

Linear Regression is one of the simplest and most widely used machine learning algorithms. The core idea:

> **Find the straight line that best fits your data, so you can predict a number for new inputs.**

**Real-life intuition:** The more hours you study, the higher your exam score tends to be. Linear regression finds the exact mathematical relationship between _hours studied_ (input) and _exam score_ (output), then uses it to predict scores for any amount of study time.

### The equation

```javascript
y = mx + b;
```

| Symbol | Name                           | Meaning                                            |
| ------ | ------------------------------ | -------------------------------------------------- |
| `y`    | Target / dependent variable    | The number you want to predict (e.g., house price) |
| `x`    | Feature / independent variable | The input you know (e.g., house size)              |
| `m`    | Slope (coefficient / weight)   | How much `y` changes when `x` increases by 1       |
| `b`    | Intercept (bias)               | The value of `y` when `x` is 0                     |

With multiple features it becomes:

```javascript
y = b + w1·x1 + w2·x2 + ... + wn·xn
```

---

## 2. How Does It "Learn"?

The algorithm's job is to pick the best values for `m` and `b`. It does this by:

1. **Start with random** values for `m` and `b`.
2. **Measure the error** — for each data point, compute how far the predicted `y` is from the actual `y`. The most common error measure is **Mean Squared Error (MSE)**:

```javascript
   MSE = (1/n) Σ (y_actual - y_predicted)²
```

3. **Adjust `m` and `b`** slightly to reduce the error (using calculus — gradient descent).
4. **Repeat** until the error is as small as possible.

**Simple analogy:** You're blindfolded on a hilly field and want to reach the lowest point. You feel the slope under your feet and take a step downhill. Repeat until the ground is flat — that's gradient descent, and the "lowest point" is the best-fit line.

---

## 3. Key Terms Cheat Sheet

| Term                     | Plain-English meaning                                            |
| ------------------------ | ---------------------------------------------------------------- |
| **Feature**              | An input column (e.g., square footage)                           |
| **Target/Label**         | The output column you predict (e.g., price)                      |
| **Training**             | Fitting the line to your data                                    |
| **Inference/Prediction** | Using the fitted line on new data                                |
| **Overfitting**          | Line fits training data perfectly but fails on new data          |
| **R² score**             | How well the line explains the data (1.0 = perfect, 0 = useless) |
| **Residual**             | Actual value − predicted value (the "miss" distance)             |

---

## 4. Practical Example 1 — House Prices (One Feature)

**Scenario:** You have data on house sizes (m²) and prices. Predict the price of a 120 m² house.

### Step-by-step (see `linear_regression_tutorial.py` for full code)

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 1. Data: house sizes (m2) and prices (thousands of dollars)
X = np.array([[50], [80], [100], [120], [150], [180], [200], [220]])
y = np.array([[120], [180], [230], [280], [340], [410], [460], [510]])

# 2. Create and train the model
model = LinearRegression()
model.fit(X, y)

# 3. Inspect what the model learned
print("Slope (m):     ", model.coef_[0][0])      # ~ price increase per m2
print("Intercept (b): ", model.intercept_[0])    # base price

# 4. Predict for a 120 m2 house
prediction = model.predict([[120]])
print("Predicted price for 120 m2:", prediction[0][0])

# 5. Evaluate: R^2 score (1.0 = perfect fit)
print("R^2 score:", model.score(X, y))
```

### What you'd typically see

- **Slope** ≈ 2.4 → each extra m² adds ~$2,400 to the price
- **Intercept** ≈ 5 → the "base" price of a house
- **Prediction for 120 m²** ≈ $290k
- **R²** close to 1 → the line explains the data very well

---

## 5. Practical Example 2 — Multiple Features (Multiple Regression)

Real problems rarely depend on one thing. A house price depends on **size, number of bedrooms, and age** at once.

```python
from sklearn.model_selection import train_test_split

# 3 features per house: [size_m2, bedrooms, age_years]
X = np.array([
    [50, 1, 30], [80, 2, 20], [100, 2, 15], [120, 3, 10],
    [150, 3, 8],  [180, 4, 5], [200, 4, 3], [220, 5, 1],
])
y = np.array([120, 180, 230, 280, 340, 410, 460, 510])

# Split data: 75% for training, 25% for testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

print("Feature weights:", model.coef_)   # e.g. [2.2, 15.0, -3.1]
print("Test R^2 score:", model.score(X_test, y_test))
```

**Reading the weights:** e.g., `[-3.1]` for age means each extra year of age _reduces_ price by ~$3,100 — negative weights are perfectly normal and meaningful.

---

## 6. Practical Example 3 — Salary vs. Experience (with Data Loading)

In practice, data comes from CSV files. Let's use pandas.

```python
import pandas as pd

# Load data (file included: salaries.csv)
df = pd.read_csv("salaries.csv")

X = df[["years_experience"]]   # double brackets = keep it 2D
y = df["salary"]

model = LinearRegression()
model.fit(X, y)

# Predict salary for someone with 7 years of experience
print(model.predict([[7]]))
```

The accompanying Python file generates a synthetic `salaries.csv` first, so everything runs out of the box.

---

## 7. Practical Example 4 — Under the Hood (Pure NumPy)

Understanding _what sklearn does for you_ makes you a better practitioner. Here is linear regression "from scratch" using the **Normal Equation**:

```python
# Add a column of 1s to X so the intercept (b) is learned automatically
X_b = np.c_[np.ones((len(X), 1)), X]

# The famous normal equation: w = (X^T X)^-1 X^T y
w = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y

b, m = w[0], w[1]   # intercept and slope
```

This computes the exact best-fit line with no iterations — for small datasets it's all you need.

---

## 8. Evaluating Your Model — Don't Just Eyeball It

| Metric                        | What it tells you                          | Good value         |
| ----------------------------- | ------------------------------------------ | ------------------ |
| **R² score**                  | % of variance explained                    | Close to 1         |
| **MAE** (Mean Absolute Error) | Average prediction miss, in target units   | As low as possible |
| **MSE**                       | Average squared miss (punishes big errors) | As low as possible |
| **RMSE**                      | √MSE — same units as target                | As low as possible |

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

y_pred = model.predict(X_test)
print("MAE :", mean_absolute_error(y_test, y_pred))
print("MSE :", mean_squared_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R^2 :", r2_score(y_test, y_pred))
```

---

## 9. Common Beginner Mistakes (and Fixes)

1. **❌ Passing a 1D array to `fit`.**
   `model.fit(X, y)` expects `X` with shape `(n_samples, n_features)`. Use `df[["col"]]` not `df["col"]`. Fix: `X = X.reshape(-1, 1)`.
2. **❌ Evaluating on training data only.**
   A model can memorize. Always split into train/test with `train_test_split`.
3. **❌ Using linear regression for yes/no questions.**
   That's classification — use Logistic Regression instead.
4. **❌ Ignoring outliers.**
   Linear regression is sensitive to extreme points (they dominate the squared error). Plot your data first!
5. **❌ Skipping the plot.**
   Always visualize `y` vs `y_pred`. If the points curve away from the diagonal line, a straight line is the wrong shape — try Polynomial Regression.

---

## 10. When to Use (and Not Use) Linear Regression

✅ **Use it when:**

- The relationship looks roughly like a straight line
- You need a fast, interpretable baseline model
- You want to _explain_ which factors matter (via coefficients)

❌ **Avoid it when:**

- The data clearly curves (use polynomial or tree models)
- The target is a category (use classification)
- Features strongly interact in complex ways

---

## 11. Summary

| Concept     | Takeaway                                                                      |
| ----------- | ----------------------------------------------------------------------------- |
| Goal        | Find the line `y = mx + b` that minimizes squared error                       |
| Learning    | Iterative error reduction (gradient descent) or closed-form (normal equation) |
| sklearn API | `model.fit(X, y)` → `model.predict(X)` → `model.score(X, y)`                  |
| Evaluation  | R², MAE, RMSE on a held-out test set                                          |
| Strength    | Simple, fast, interpretable, great baseline                                   |

**Next steps:** Polynomial Regression → Regularization (Ridge/Lasso) → Logistic Regression for classification.

---

_Companion code: `linear_regression_tutorial.py` — run it with `python linear_regression_tutorial.py`. It is fully commented line by line._
