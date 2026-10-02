# Dealing with Outliers — A Practical Guide for ML Data Preparation

## Table of Contents

- [Dealing with Outliers — A Practical Guide for ML Data Preparation](#dealing-with-outliers--a-practical-guide-for-ml-data-preparation)
  - [Table of Contents](#table-of-contents)
  - [1. What is an outlier?](#1-what-is-an-outlier)
  - [2. Why do outliers matter for ML?](#2-why-do-outliers-matter-for-ml)
  - [3. Step 1: Detecting outliers](#3-step-1-detecting-outliers)
    - [3.1 Visual methods (always do this first!)](#31-visual-methods-always-do-this-first)
    - [3.2 The IQR method (most common, robust)](#32-the-iqr-method-most-common-robust)
    - [3.3 The Z-score method (works for roughly normal data)](#33-the-z-score-method-works-for-roughly-normal-data)
    - [3.4 Isolation Forest (multivariate — many columns at once)](#34-isolation-forest-multivariate--many-columns-at-once)
  - [4. Step 2: Deciding what to do](#4-step-2-deciding-what-to-do)
  - [5. Step 3: Fixing outliers](#5-step-3-fixing-outliers)
    - [5.1 Deletion (only when you are sure it's an error)](#51-deletion-only-when-you-are-sure-its-an-error)
    - [5.2 Capping / Winsorization (clamp extreme values to a bound)](#52-capping--winsorization-clamp-extreme-values-to-a-bound)
    - [5.3 Transformation (compress the scale so big values matter less)](#53-transformation-compress-the-scale-so-big-values-matter-less)
    - [5.4 Imputation (replace outliers with a "typical" value)](#54-imputation-replace-outliers-with-a-typical-value)
    - [5.5 Flagging (keep the value, add a "this is weird" indicator)](#55-flagging-keep-the-value-add-a-this-is-weird-indicator)
  - [6. A complete end-to-end example](#6-a-complete-end-to-end-example)
  - [7. Common mistakes beginners make](#7-common-mistakes-beginners-make)
  - [8. Quick reference cheat sheet](#8-quick-reference-cheat-sheet)

---

## 1. What is an outlier?

An **outlier** is a data point that is very different from the rest of your data.

**Simple example:** Imagine you are collecting the ages of students in a class:

```
[18, 19, 20, 21, 19, 20, 18, 95]
```

Almost everyone is between 18 and 21... but there is a **95-year-old**. That value of 95
is an outlier. It _could_ be a real person (maybe a grandparent auditing the class),
or it could be a typo (maybe someone meant to type `19` and hit `9` twice).

**Common causes of outliers:**

- **Data entry errors** — typing mistakes (`10000` instead of `100.0`)
- **Measurement errors** — a broken sensor reading `-999`
- **Genuine extreme values** — the income of a billionaire in a salary dataset
- **Different units** — heights recorded in centimeters vs. meters mixed together

> **Key idea:** An outlier is not automatically "wrong." Your job is to detect it,
> understand _why_ it exists, and then decide the right treatment.

---

## 2. Why do outliers matter for ML?

Many machine learning models are **sensitive to outliers**:

| Model type                         | Sensitive to outliers? | Why                                                |
| ---------------------------------- | ---------------------- | -------------------------------------------------- |
| Linear Regression                  | ✅ Yes a lot           | Outliers pull the regression line toward them      |
| Logistic Regression                | ✅ Yes                 | Outliers distort the learned weights               |
| K-Means clustering                 | ✅ Yes a lot           | K-Means uses distances; outliers distort centroids |
| Neural Networks                    | ⚠️ Somewhat            | Can slow learning or destabilize training          |
| Decision Trees                     | ❌ No                  | Splits are based on thresholds, not distances      |
| Random Forests / Gradient Boosting | ❌ Mostly no           | Tree-based models are robust                       |

**Example:** If you fit a linear regression on house prices and one house was
mistakenly listed at **$900 million** instead of **$900,000**, the model line will
tilt dramatically to get closer to that one point, making predictions worse for
_all the normal houses_.

---

## 3. Step 1: Detecting outliers

You cannot fix what you cannot see. Let's look at the main detection methods.

### 3.1 Visual methods (always do this first!)

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Create sample data with some obvious outliers
np.random.seed(42)
ages = np.random.normal(loc=35, scale=8, size=200).round(1)   # normal ages
ages = np.append(ages, [150, 3, 220, -10])                    # injected outliers
df = pd.DataFrame({'age': ages})

# Boxplot: points beyond the "whiskers" are candidate outliers
plt.figure(figsize=(6, 3))
sns.boxplot(x=df['age'])
plt.title('Boxplot of age — dots beyond whiskers are outliers')
plt.show()
```

**How to read a boxplot (beginner friendly):**

- The **box** contains the middle 50% of the data.
- The **line inside the box** is the median (middle value).
- The **whiskers** extend to "reasonable" extremes.
- Any **dot beyond the whiskers** is flagged as a potential outlier.

### 3.2 The IQR method (most common, robust)

**IQR** = Interquartile Range = the height of the box in the boxplot.

```
Q1  = 25th percentile (bottom of the box)
Q3  = 75th percentile (top of the box)
IQR = Q3 - Q1

Lower bound = Q1 - 1.5 × IQR
Upper bound = Q3 + 1.5 × IQR

Anything below the lower bound or above the upper bound = outlier
```

Why `1.5`? It's a convention (from statistician John Tukey) that works well for
roughly bell-shaped data. You can use `3.0` for a stricter rule.

```python
def detect_outliers_iqr(data, column, factor=1.5):
    q1 = data[column].quantile(0.25)      # 25th percentile
    q3 = data[column].quantile(0.75)      # 75th percentile
    iqr = q3 - q1                          # interquartile range
    lower_bound = q1 - factor * iqr        # lower fence
    upper_bound = q3 + factor * iqr        # upper fence
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    return outliers, lower_bound, upper_bound

outliers, lb, ub = detect_outliers_iqr(df, 'age')
print(f"Bounds: [{lb:.2f}, {ub:.2f}]")
print(f"Found {len(outliers)} outliers:")
print(outliers)
```

### 3.3 The Z-score method (works for roughly normal data)

The **Z-score** tells you how many standard deviations a value is from the mean:

```
z = (value - mean) / standard deviation
```

- `|z| > 3` → value is more than 3 standard deviations away → outlier
- (A common convention; some people use `|z| > 2.5` or `4`)

```python
from scipy import stats

df['age_zscore'] = np.abs(stats.zscore(df['age']))
z_outliers = df[df['age_zscore'] > 3]
print(z_outliers[['age', 'age_zscore']])
```

**⚠️ Warning:** Z-scores use the **mean** and **standard deviation**, which are
_themselves_ distorted by outliers. Prefer the IQR method for skewed data.

### 3.4 Isolation Forest (multivariate — many columns at once)

All the methods above look at **one column at a time**. But sometimes a point is
only weird in _combination_: a 25-year-old earning $500k/year may be fine on each
axis alone but suspicious together.

```python
from sklearn.ensemble import IsolationForest

# Sample multivariate data
np.random.seed(0)
n = 300
income = np.random.normal(50000, 12000, n)
spend   = income * 0.4 + np.random.normal(0, 3000, n)
X = pd.DataFrame({'income': income, 'spend': spend})

# Inject a few weird combos
X.loc[n]     = [500000, 5000]     # huge income, tiny spend
X.loc[n + 1] = [5000, 200000]     # tiny income, huge spend

iso = IsolationForest(contamination=0.02, random_state=42)
X['is_outlier'] = iso.fit_predict(X[['income', 'spend']])  # -1 = outlier, 1 = normal

print(X[X['is_outlier'] == -1])
```

---

## 4. Step 2: Deciding what to do

Before changing anything, ask these questions:

1. **Is it an error?** (impossible value, typo, broken sensor)
   → **Fix it** (correct, impute, or remove).
2. **Is it a genuine but extreme value?** (a real billionaire's income)
   → **Keep it, but soften it** (cap it, transform it, or flag it).
3. **Is it from a different population?** (an entry measured in different units)
   → **Fix the units** or remove the row.
4. **Does the model care?** (linear models: yes; tree models: no)
   → If using a robust model, you may not need heavy treatment.

> **Golden rule:** Never delete data blindly. Document every decision.
> In a real project, write down _why_ you removed or changed each value.

---

## 5. Step 3: Fixing outliers

### 5.1 Deletion (only when you are sure it's an error)

```python
# Remove rows where age is outside a *physically impossible* range
df_clean = df[(df['age'] >= 0) & (df['age'] <= 120)]
print(f"Removed {len(df) - len(df_clean)} impossible rows")
```

✅ Good for: impossible values (`age = -10`, `age = 500`)
❌ Bad for: genuine extreme values — you lose real information

### 5.2 Capping / Winsorization (clamp extreme values to a bound)

Instead of deleting, you **pull extreme values back to the fence**. Information is
kept, but its harmful influence is reduced.

```python
def cap_outliers(data, column, factor=1.5):
    q1 = data[column].quantile(0.25)
    q3 = data[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - factor * iqr
    upper = q3 + factor * iqr
    # np.clip forces all values into the [lower, upper] range
    data[column + '_capped'] = data[column].clip(lower=lower, upper=upper)
    return data

df = cap_outliers(df, 'age')
print(df[['age', 'age_capped']].sort_values('age', ascending=False).head(6))
```

### 5.3 Transformation (compress the scale so big values matter less)

A **log transformation** is perfect for right-skewed data like income:

```python
import numpy as np

income = np.array([30000, 35000, 40000, 45000, 50000, 10_000_000])  # one billionaire

# Raw: the billionaire dominates everything
print("Raw mean:  ", income.mean().round(0))

# Log-transformed: values get compressed, skewness reduced
income_log = np.log1p(income)          # log1p = log(1 + x), safe for zeros
print("Log mean:  ", income_log.mean().round(2))
```

Rule of thumb: **log transform** for right-skewed positive data (income, prices,
population). **Box-Cox / Yeo-Johnson** are automatic alternatives:

```python
from sklearn.preprocessing import PowerTransformer

pt = PowerTransformer(method='yeo-johnson')  # works even with zeros/negatives
df['age_transformed'] = pt.fit_transform(df[['age']])
```

### 5.4 Imputation (replace outliers with a "typical" value)

```python
median_age = df['age'].median()          # median is robust to outliers (unlike mean)

# Replace only the impossible values with the median
df['age_imputed'] = df['age']
df.loc[(df['age'] < 0) | (df['age'] > 120), 'age_imputed'] = median_age
```

### 5.5 Flagging (keep the value, add a "this is weird" indicator)

Some outliers carry _signal_ (e.g., a huge transaction might indicate fraud).
Instead of destroying the information, **add a binary flag column** and let the
model decide:

```python
df['age_is_outlier'] = ((df['age'] < 0) | (df['age'] > 120)).astype(int)
```

This works especially well with **tree-based models** (Random Forest, XGBoost).

---

## 6. A complete end-to-end example

The full runnable version of this pipeline is in `outliers_practical.py`.
Here is the outline:

```python
# 1. Load / create data
# 2. Explore visually (boxplot, histogram)
# 3. Detect outliers with IQR
# 4. Decide: errors -> remove; extremes -> cap; skewed feature -> transform
# 5. Add an outlier flag for the model
# 6. Verify the result with new plots
# 7. (Optional) Compare model performance before vs after cleaning
```

Quick model-comparison snippet:

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# Dirty data
score_dirty = cross_val_score(
    make_pipeline(StandardScaler(), LinearRegression()),
    X_dirty, y, cv=5, scoring='r2'
).mean()

# Cleaned data
score_clean = cross_val_score(
    make_pipeline(StandardScaler(), LinearRegression()),
    X_clean, y, cv=5, scoring='r2'
).mean()

print(f"R² before cleaning: {score_dirty:.3f}")
print(f"R² after cleaning:  {score_clean:.3f}")
```

---

## 7. Common mistakes beginners make

| Mistake                                             | Why it's bad                               | Do this instead                                |
| --------------------------------------------------- | ------------------------------------------ | ---------------------------------------------- |
| Deleting every outlier automatically                | You may delete real, valuable data         | Ask _why_ the outlier exists first             |
| Using the mean for imputation                       | The mean itself is distorted by outliers   | Use the **median**                             |
| Detecting outliers on the test set and leaking info | Data leakage → overly optimistic scores    | Fit bounds/scalers on **train only**           |
| Cleaning before the train/test split                | Same leakage problem                       | Split first, then clean using train statistics |
| Applying one rule to every column                   | Income and age behave differently          | Treat each feature based on its distribution   |
| Ignoring outliers because "my model is robust"      | Even tree models can waste splits on noise | At minimum, visualize and sanity-check         |

**Proper pipeline pattern (no leakage):**

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Compute bounds ONLY from training data
q1, q3 = X_train['age'].quantile([0.25, 0.75])
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr

# Apply those same bounds to test data
X_train['age'] = X_train['age'].clip(lower, upper)
X_test['age']  = X_test['age'].clip(lower, upper)
```

---

## 8. Quick reference cheat sheet

```
DETECT
  ├── Visual first:      boxplot, histogram, scatter plot
  ├── One column:        IQR rule  (Q1-1.5·IQR, Q3+1.5·IQR)
  ├── Normal-ish column: Z-score   (|z| > 3)
  └── Many columns:      Isolation Forest, DBSCAN

DECIDE
  ├── Error?             → remove or correct
  ├── Genuine extreme?   → cap / transform / flag
  └── Different units?   → fix units or remove row

FIX
  ├── Remove:      df = df[(df.col >= low) & (df.col <= high)]
  ├── Cap:         df.col = df.col.clip(low, high)
  ├── Transform:   np.log1p(x)  or  PowerTransformer
  ├── Impute:      replace with median
  └── Flag:        df['col_outlier'] = is_outlier.astype(int)

REMEMBER
  ├── Fit everything on TRAIN data only (no leakage)
  ├── Median > mean when outliers are around
  ├── Document every change you make
  └── Tree models (RF, XGBoost) need less outlier treatment
```

---

_Happy cleaning! Remember: outliers are not the enemy — unexplained outliers are._
