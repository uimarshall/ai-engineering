# Dealing with Missing Values — KNNImputer (Practical Guide)

> **Topic:** Data Cleaning & Preparation for Machine Learning
> **Tool:** `KNNImputer` from scikit-learn
> **Level:** Beginner

---

## 1. Why Do We Care About Missing Values?

Real-world data is messy. Surveys go unanswered, sensors fail, people skip form fields.
The result is **missing values** (`NaN` — "Not a Number") in your dataset.

Most machine learning models (linear regression, logistic regression, SVM, neural networks, etc.)
**cannot handle missing values at all** — they will either crash or silently produce garbage results.

So before training any model, you must **clean** the data. The main strategies are:

| Strategy                       | What it does                                            | When it works well                  |
| ------------------------------ | ------------------------------------------------------- | ----------------------------------- |
| **Drop rows**                  | Delete any row with a missing value                     | Very few rows are missing           |
| **Drop columns**               | Delete a column that is mostly empty                    | A column is mostly useless          |
| **Fill with mean/median/mode** | Replace missing values with a simple statistic          | Quick and dirty baseline            |
| **KNNImputer**                 | Fill each missing value using the _K most similar rows_ | Numeric data where rows are related |
| **IterativeImputer**           | Model each column from the others                       | Complex relationships (slower)      |

This tutorial focuses on **KNNImputer**.

---

## 2. What Is KNNImputer? (The Intuition)

KNN stands for **K-Nearest Neighbors**. You may have heard of it as a _classification_ algorithm —
but here we use the same idea for **filling in gaps**.

### The core idea, in plain English:

> _"Find the K rows that are most similar to this row (ignoring the missing values),
> and fill the gap with a weighted average of those neighbors."_

### A tiny example

Imagine a dataset of houses:

| House | Size (m²) | Bedrooms | Price ($)       |
| ----- | --------- | -------- | --------------- |
| A     | 100       | 3        | **?** ← missing |
| B     | 98        | 3        | 250,000         |
| C     | 105       | 3        | 260,000         |
| D     | 40        | 1        | 90,000          |

House A is missing its price. Which rows look most like A?
Clearly **B** and **C** (similar size, same bedrooms) — not D.

With `n_neighbors=2`, KNNImputer takes the prices of B and C and fills in:

```
Price(A) = (250,000 + 260,000) / 2 = 255,000
```

That's the whole trick. It repeats this for every missing value in every column.

### How is "similarity" measured?

By **distance** between rows. The default is the **Euclidean distance**, computed using
only the columns that are **not** missing in either row. Rows that are close in value
across the available features are "neighbors."

**Important:** distances are affected by scale. A column measured in _millimeters_ will dominate
a column measured in _millions_. So we usually **scale the data first** (e.g., with
`StandardScaler` inside a `Pipeline`). More on this in Section 6.

---

## 3. When Should You Use KNNImputer?

**Use it when:**

- Your data is **numeric** (KNNImputer does not handle text/categorical columns directly).
- Rows in your data are **related to each other** (similar patients, similar customers, similar houses).
- Missing data is **not completely random** but follows patterns from other features.

**Avoid it when:**

- Data is mostly categorical → use `SimpleImputer(strategy='most_frequent')` or encode first.
- The dataset is **huge** → KNNImputer is slow (it compares every row to every other row).
- Columns are on wildly different scales and you don't want to scale them.

---

## 4. Pros and Cons

| ✅ Pros                                                               | ❌ Cons                                                     |
| --------------------------------------------------------------------- | ----------------------------------------------------------- |
| Uses the _actual structure_ of the data, not just a blanket statistic | Slow on large datasets (O(n²) distance computation)         |
| Often more accurate than mean/median imputation                       | Sensitive to feature scaling                                |
| Simple to use, fully integrated with scikit-learn `Pipeline`          | Only works with numeric data                                |
| `n_neighbors` gives you a knob to tune                                | Too small `n_neighbors` → noise; too large → over-smoothing |

---

## 5. Practical Example 1 — The Basics

Let's build a small dataset by hand so you can _see exactly what happens_.

```python
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer

# A tiny dataset with 3 rows and 3 numeric columns
# Notice the missing value (np.nan) in row 1, column 'study_hours'
df = pd.DataFrame({
    'age':         [20, 21, 22],
    'study_hours': [4, np.nan, 6],   # <- student 1 didn't report study hours
    'score':       [70, 85, 90]
})

print("BEFORE imputation:")
print(df)

# Create the imputer: use the 2 most similar rows to fill each gap
imputer = KNNImputer(n_neighbors=2)

# fit_transform computes distances, finds neighbors, and fills the gaps
df_filled = pd.DataFrame(
    imputer.fit_transform(df),   # returns a NumPy array
    columns=df.columns           # put the column names back
)

print("\nAFTER imputation:")
print(df_filled)
```

**What just happened?**

Row 1 (`age=21, score=85`) was missing `study_hours`.
The imputer found the 2 most similar rows and averaged their `study_hours`:

```
study_hours(1) = (4 + 6) / 2 = 5.0
```

You should see `5.0` filled into the gap.

---

## 6. Practical Example 2 — Realistic Workflow (with Scaling + Pipeline)

This is the **correct, leakage-free workflow** you would use in a real ML project.
The golden rule: **fit the imputer only on the training data**, then apply it to the test data.

```python
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# ---------------------------------------------------------------
# STEP 1: Create a realistic dataset with missing values
# ---------------------------------------------------------------
rng = np.random.RandomState(42)                      # seed for reproducibility
n = 200                                              # 200 rows

age        = rng.normal(35, 10, n).round(1)          # age, mean 35, std 10
income     = age * 900 + rng.normal(0, 5000, n)      # income correlates with age
spend      = income * 0.05 + rng.normal(0, 300, n)   # spending correlates with income

df = pd.DataFrame({'age': age, 'income': income, 'spend': spend})

# Randomly hide 10% of values to simulate real-world missing data
mask = rng.rand(*df.shape) < 0.10
df[mask] = np.nan

print(f"Missing values per column:\n{df.isna().sum()}\n")

# ---------------------------------------------------------------
# STEP 2: Split into train/test BEFORE any imputation
# ---------------------------------------------------------------
X = df.drop(columns='spend')     # features: age, income
y = df['spend']                  # target: spend

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------------------------------------------------------
# STEP 3: Build a Pipeline = scale first, THEN impute, THEN model
# Why scale first? KNN uses distances; income (thousands) would
# otherwise completely dominate age (tens). Scaling puts every
# feature on the same footing.
# ---------------------------------------------------------------
pipe = Pipeline([
    ('scaler',   StandardScaler()),   # 1. put features on equal scales
    ('imputer',  KNNImputer(n_neighbors=5)),  # 2. fill missing values
    ('model',    LinearRegression())  # 3. train the model
])

# ---------------------------------------------------------------
# STEP 4: Train and evaluate
# ---------------------------------------------------------------
pipe.fit(X_train, y_train)
preds = pipe.predict(X_test)
rmse = mean_squared_error(y_test, preds) ** 0.5
print(f"Test RMSE with KNNImputer: {rmse:.2f}")
```

### Why the Pipeline matters

A pipeline guarantees that:

1. **No data leakage** — the test set never influences how training gaps are filled.
2. **Scale before distance** — `StandardScaler` runs _before_ `KNNImputer`, so no single
   feature dominates the neighbor search.
3. **One-line prediction** — `pipe.predict(X_test)` applies all steps automatically.

> **Rule of thumb:** _always_ wrap imputers + scalers + models in a `Pipeline` in real projects.

---

## 7. Practical Example 3 — Comparing Imputation Strategies

How do you know KNNImputer is actually better than just filling with the median?
Test it. Here we compare three strategies side by side.

```python
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression

# Recreate the dataset from Example 2 (same code, shortened)
rng = np.random.RandomState(42)
n = 200
df = pd.DataFrame({'age': rng.normal(35, 10, n).round(1)})
df['income'] = df['age'] * 900 + rng.normal(0, 5000, n)   # income correlated with age
df['spend']  = df['income'] * 0.05 + rng.normal(0, 300, n)
mask = rng.rand(n, 2) < 0.10            # hide values only in age & income
df.loc[mask[:, 0], 'age'] = np.nan
df.loc[mask[:, 1], 'income'] = np.nan

X = df[['age', 'income']]
y = df['spend']

# Three competing strategies, each wrapped in the same pipeline shape
strategies = {
    'Drop rows':      'drop',                              # no imputation at all
    'Median fill':    SimpleImputer(strategy='median'),    # simple statistic
    'KNN (k=3)':      KNNImputer(n_neighbors=3),           # our method
}

for name, imputer in strategies.items():
    if imputer == 'drop':
        # Drop rows manually for the baseline comparison
        Xc, yc = X.dropna(), y[X.dropna().index]
        scores = cross_val_score(LinearRegression(), Xc, yc, cv=5,
                                 scoring='neg_root_mean_squared_error')
    else:
        pipe = Pipeline([
            ('scaler',  StandardScaler()),
            ('imputer', imputer),
            ('model',   LinearRegression())
        ])
        scores = cross_val_score(pipe, X, y, cv=5,
                                 scoring='neg_root_mean_squared_error')

    print(f"{name:15s} -> RMSE: {-scores.mean():.2f} (+/- {scores.std():.2f})")
```

**Typical takeaway:** KNNImputer usually beats median-fill when features are correlated
(which they are here — income drives spend, age drives income) and loses much less data
than dropping rows.

---

## 8. Tuning `n_neighbors`

`n_neighbors` controls how many rows vote on each missing value:

- **Small k (e.g., 1–3):** very local, fits the data closely, but can capture noise.
- **Large k (e.g., 10–20):** smoother, more stable, but may blur real structure.

Use cross-validation to pick k, the same way you'd tune any hyperparameter:

```python
from sklearn.model_selection import GridSearchCV

pipe = Pipeline([
    ('scaler',  StandardScaler()),
    ('imputer', KNNImputer()),
    ('model',   LinearRegression())
])

# Search over several neighbor counts
grid = GridSearchCV(pipe,
                    {'imputer__n_neighbors': [2, 3, 5, 7, 10, 15]},
                    cv=5,
                    scoring='neg_root_mean_squared_error')
grid.fit(X, y)

print("Best k:", grid.best_params_['imputer__n_neighbors'])
print("Best RMSE:", -grid.best_score_)
```

Note the syntax `imputer__n_neighbors` — the double underscore tells GridSearchCV
to look _inside_ the pipeline step named `'imputer'`.

---

## 9. Important Details & Common Pitfalls

1. **Only numeric data.** KNNImputer cannot process strings or categories.
   Impute/encode categoricals separately (e.g., `SimpleImputer(strategy='most_frequent')`).
2. **Scale first.** Unscaled features with big magnitudes will dominate distances.
   Put `StandardScaler` before the imputer in a pipeline.
3. **Weights.** By default all K neighbors count equally (`weights='uniform'`).
   Try `weights='distance'` to give closer neighbors more influence.
4. **Speed.** Complexity grows with the square of the number of rows.
   For datasets with 100k+ rows, consider sampling or `IterativeImputer` alternatives.
5. **Don't impute the target (y).** Impute features (X). If the target has missing
   values, either drop those rows or treat it as a separate problem.
6. **Keep the leakage rule:** `fit` on train, only `transform` on test.
   A `Pipeline` handles this automatically.

---

## 10. Key Takeaways

- **KNNImputer fills a missing value by averaging that value across the K most similar rows.**
- "Similar" is measured by distance over the _available_ (non-missing) features —
  so **scale your features first**.
- Always use it inside a **`Pipeline`** fitted on the training data only, to avoid leakage.
- Tune `n_neighbors` with cross-validation; typical good values are 3–10.
- It shines with **correlated numeric features** and moderate dataset sizes.

---

## 11. Quick Reference

```python
from sklearn.impute import KNNImputer

KNNImputer(
    n_neighbors=5,        # how many rows vote on each missing value
    weights='uniform',    # 'uniform' (equal) or 'distance' (closer = stronger)
    metric='nan_euclidean' # distance that ignores NaNs (leave as default)
)
```

_Happy cleaning! Clean data beats clever models, every time._
