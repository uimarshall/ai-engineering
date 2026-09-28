# Dealing with Missing Values in Pandas (PRACTICAL Guide)

> **Topic:** Data Cleaning & Preparation for Machine Learning
> **Level:** Beginner
> **Tools:** Python 3, pandas, scikit-learn

---

## 1. Why Do Missing Values Matter for ML?

Missing values are one of the most common problems in real-world datasets. **Machine learning models cannot handle `NaN` values directly** — if you feed them raw data with gaps, most algorithms will throw an error or silently produce bad predictions.

Common causes of missing data:

- A survey question was left blank
- A sensor failed to record a reading
- A data entry error was deleted (turned into `NaN`)
- A column doesn't apply to some rows (e.g., "spouse's income" for unmarried people)

**Types of missingness (good to know):**

- **MCAR** (Missing Completely At Random) – gaps unrelated to anything
- **MAR** (Missing At Random) – gaps depend on _other_ observed data
- **MNAR** (Missing Not At Random) – gaps depend on the missing value itself

For a beginner: don't worry about the theory yet. Focus on the practical workflow:

```
1. Detect  -> find where the missing values are
2. Understand -> how much is missing, and why?
3. Treat  -> drop, fill (impute), or flag
4. Validate -> check the result is sensible
```

---

## 2. Setup

```python
import pandas as pd
import numpy as np

pd.set_option('display.width', 120)   # nicer table printing
```

---

## 3. Step 1 — Detecting Missing Values

pandas represents missing values as `NaN` (for numbers), `NaT` (for dates), or `None` (for objects).

### 3.1 Create a realistic messy dataset

```python
data = {
    'customer_id':   [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'age':           [25, np.nan, 41, 33, np.nan, 52, 29, np.nan, 47, 36],
    'income':        [50000, 62000, np.nan, 48000, 71000, np.nan, 54000, 39000, np.nan, 66000],
    'years_customer':[3, 5, np.nan, 1, 8, 12, 2, np.nan, 15, 7],
    'purchased':     ['yes', 'no', 'yes', np.nan, 'yes', 'no', 'yes', 'no', np.nan, 'yes']
}
df = pd.DataFrame(data)
```

### 3.2 The essential detection toolkit

```python
df.isna()                 # Boolean mask: True where value is missing
df.isna().sum()           # Count of missing values per column
df.isna().mean() * 100    # Missing values as a PERCENTAGE (very important!)
df.isna().any(axis=1)     # Which ROWS have at least one missing value
```

**Practical rule of thumb (beginner version):**

| % missing in a column | Recommended action                            |
| --------------------- | --------------------------------------------- |
| 0–5%                  | Impute (fill) — safe                          |
| 5–30%                 | Impute + add a "was missing" indicator column |
| 30–60%                | Consider advanced imputation, or flag-only    |
| >60%                  | Consider dropping the column entirely         |

---

## 4. Step 2 — Drop Missing Values (quick & simple)

When you have _plenty_ of data and only a few gaps, dropping rows is the simplest option.

```python
# Drop ROWS that contain ANY missing value
df_dropped = df.dropna()

# Drop rows only if a SPECIFIC column is missing
df_dropped = df.dropna(subset=['age'])

# Drop COLUMNS with too many missing values (>50% missing)
threshold = 0.5 * len(df)
df_dropped = df.dropna(axis=1, thresh=threshold)
```

⚠️ **Caution:** `dropna()` deletes data. With small datasets this can hurt your model. Only drop when you can afford to lose rows.

---

## 5. Step 3 — Imputation (Filling In the Gaps)

Imputation means replacing missing values with sensible estimates. This is the **preferred approach for ML** in most cases.

### 5.1 Fill with a constant

```python
df['purchased'] = df['purchased'].fillna('unknown')
```

### 5.2 Fill numeric columns with statistics (mean / median / mode)

- **Mean** — good when data is roughly symmetric and has no extreme outliers
- **Median** — more robust; use this when there are outliers (e.g., income, house prices)
- **Mode** — most common value; typical for categories

```python
df['age'].fillna(df['age'].mean(), inplace=False)
df['income'].fillna(df['income'].median())       # income often skewed -> median
```

### 5.3 Fill using neighboring values (time series / ordered data)

```python
# forward fill: use the previous valid value
df['years_customer'].ffill()

# backward fill: use the next valid value
df['years_customer'].bfill()
```

### 5.4 Fill with an indicator column (recommended for ML!)

Sometimes _the fact that a value is missing_ carries information (MNAR).
Keep a flag before filling:

```python
df['income_was_missing'] = df['income'].isna().astype(int)
df['income'] = df['income'].fillna(df['income'].median())
```

### 5.5 Fill groups by category — very practical!

Filling with the _global_ mean can be crude. Fill with the **group mean** instead:

```python
df['age'] = df['age'].fillna(df.groupby('purchased')['age'].transform('mean'))
```

`transform('mean')` broadcasts each group's mean back to every row in that group.

---

## 6. Step 4 — The ML-Grade Approach: `SimpleImputer`

For machine learning pipelines, use scikit-learn's `SimpleImputer` so the **same imputation strategy is applied consistently** to training and test data.

```python
from sklearn.impute import SimpleImputer

# Numeric columns -> median imputation
num_imputer = SimpleImputer(strategy='median')

# Categorical columns -> most frequent value
cat_imputer = SimpleImputer(strategy='most_frequent')
```

### 6.1 The proper train/test workflow

```python
from sklearn.model_selection import train_test_split

X = df.drop(columns=['purchased'])
y = df['purchased']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# FIT the imputer on TRAIN data only, then apply to both
num_cols = ['age', 'income', 'years_customer']
X_train[num_cols] = num_imputer.fit_transform(X_train[num_cols])
X_test[num_cols]  = num_imputer.transform(X_test[num_cols])   # NOTE: transform, not fit_transform!

cat_cols = ['purchased']
```

⚠️ **One more essential step:** drop rows where the _target label itself_ is missing **before** splitting — you can't train on a row with no answer:

```python
labeled = y.notna()
X, y = X[labeled], y[labeled]
```

**Why `fit_transform` on train but only `transform` on test?**
If you fit on the test set, information from the test data "leaks" into your preprocessing — your evaluation becomes overly optimistic. **Fit only on training data. Always.**

### 6.2 KNN Imputation — smarter, still easy

`KNNImputer` fills a missing value using the average of the _k nearest neighbors_ (rows most similar to it). Good when rows are genuinely similar to each other.

```python
from sklearn.impute import KNNImputer

knn_imputer = KNNImputer(n_neighbors=3)
X_train[num_cols] = knn_imputer.fit_transform(X_train[num_cols])
```

⚠️ KNN imputation requires scaling first (it is distance-based), and is slower on big datasets.

---

## 7. Step 5 — Integration with a Pipeline (best practice)

Never do imputation "by hand" and then split data — instead, bundle it into a `Pipeline` so it happens automatically and leak-free:

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier

numeric_features = ['age', 'income', 'years_customer']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', SimpleImputer(strategy='median'), numeric_features),
    ]
)

pipe = Pipeline(steps=[
    ('preprocess', preprocessor),
    ('model', RandomForestClassifier(random_state=42))
])

pipe.fit(X_train, y_train)
score = pipe.score(X_test, y_test)
```

With a `Pipeline`, preprocessing is applied _inside_ cross-validation too — no leakage possible.

---

## 8. Converting Categorical Missing Values for ML

ML models need numbers. Missing strings can be encoded too:

```python
df['purchased'] = df['purchased'].astype('category')
df['purchased_encoded'] = df['purchased'].cat.codes   # -1 for NaN... fill first!
```

Better workflow: fill missing categoricals with a string like `'missing'`, **then** encode:

```python
df['purchased'] = df['purchased'].fillna('missing')
```

---

## 9. Quick Reference Cheat Sheet

| Situation                     | Recommended technique                                            |
| ----------------------------- | ---------------------------------------------------------------- |
| Few missing rows, big dataset | `dropna()`                                                       |
| Numeric column, no outliers   | `fillna(df[col].mean())`                                         |
| Numeric column, has outliers  | `fillna(df[col].median())`                                       |
| Ordered / time-series data    | `.ffill()` or `.bfill()`                                         |
| Missingness is informative    | Add indicator column, then impute                                |
| Categorical column            | `fillna('missing')` or `SimpleImputer(strategy='most_frequent')` |
| ML pipeline (best practice)   | `SimpleImputer` / `KNNImputer` inside a `Pipeline`               |

---

## 10. Common Beginner Mistakes

1. **Fitting imputers on the full dataset before splitting** → data leakage. Fit on train only.
2. **Using mean for skewed data (income, prices)** → median is more robust.
3. **Dropping columns just because they have some NaNs** → you may lose valuable signal.
4. **Forgetting categorical NaNs** → they often slip through and break encoding.
5. **Not keeping an indicator column** → sometimes _missingness itself_ predicts the target.

---

## 11. Summary

- **Detect first:** `isna().sum()` and `isna().mean()`
- **Dropping** is fine when data is abundant; otherwise **impute**
- **Median** for skewed numbers, **mean** for symmetric ones, **mode/frequent** for categories
- For ML: use **`SimpleImputer` in a `Pipeline`**, fit on training data only
- When missingness itself is informative, add a **binary indicator column**

_Next steps: learn about `IterativeImputer` (multivariate imputation) and handling outliers!_
