# Dealing with Outliers — A Practical Guide to Cleaning Data for Machine Learning

> **Level:** Beginner
> **Goal:** Learn what outliers are, why they matter, and how to find and handle them with real code.

---

## 1. What is an outlier?

An **outlier** is a data point that is unusually far from the rest of the data.

**Example:** Imagine you are collecting the ages of students in a class:
`18, 19, 20, 21, 17, 190`

`190` is clearly an outlier — it's probably a typo (`19` + an extra `0`). A machine learning model trained on this data might treat age 190 as a "normal" value, which distorts the patterns it learns.

Outliers can be:

- **Errors** — typos, sensor glitches, unit mistakes (e.g. height recorded in cm vs meters).
- **Genuine but rare** — a billionaire's income in a salary dataset is real, just extreme.

Both types can harm a model, so you need strategies for both.

---

## 2. Why do outliers matter for ML?

1. **Distort statistics:** Mean, standard deviation, and correlation get skewed.
2. **Break certain models:** Linear regression, k-means, and anything based on distance or averages is very sensitive to outliers.
3. **Tree-based models** (Random Forest, XGBoost) are more robust, but extreme values can still hurt split quality.

---

## 3. Step-by-step practical workflow

```
1. Load data
2. Visualize the data (boxplots / scatterplots)  <-- ALWAYS do this first
3. Detect outliers (IQR, Z-score, percentile, isolation forest)
4. Decide: fix, cap, drop, or leave them?
5. Validate the result
```

---

## 4. Detecting outliers

### 4.1 Visual inspection (always start here!)

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)  # so results are reproducible

# Build a demo dataset of 100 house sizes (sq ft) + some outliers
sizes = np.random.normal(loc=2000, scale=300, size=100)
sizes = np.append(sizes, [12000, 15000, 50])  # inject 3 outliers

df = pd.DataFrame({"house_size_sqft": sizes})

df.boxplot(column="house_size_sqft")
plt.title("Boxplot reveals outliers instantly")
plt.show()

df["house_size_sqft"].hist(bins=30)
plt.title("Histogram also shows the extreme values")
plt.show()
```

### 4.2 The IQR method (most common, robust)

For any column, compute:

- Q1 = 25th percentile
- Q3 = 75th percentile
- IQR = Q3 − Q1
- Lower bound = Q1 − 1.5 × IQR
- Upper bound = Q3 + 1.5 × IQR

Anything below the lower bound or above the upper bound is an outlier.

```python
def iqr_outlier_bounds(series: pd.Series, k: float = 1.5):
    """Return lower and upper bounds beyond which values are flagged as outliers."""
    q1 = series.quantile(0.25)          # first quartile (25th percentile)
    q3 = series.quantile(0.75)          # third quartile (75th percentile)
    iqr = q3 - q1                       # interquartile range
    lower = q1 - k * iqr                # lower fence
    upper = q3 + k * iqr                # upper fence
    return lower, upper

lower, upper = iqr_outlier_bounds(df["house_size_sqft"])
print(f"Valid range: [{lower:.0f}, {upper:.0f}]")

# Flag the outliers
outliers = df[(df["house_size_sqft"] < lower) | (df["house_size_sqft"] > upper)]
print(f"Found {len(outliers)} outliers out of {len(df)} rows")
print(outliers)
```

### 4.3 The Z-score method (assumes roughly normal data)

Z-score = (value − mean) / standard deviation. Values with |z| > 3 are usually flagged.

```python
def zscore_outliers(series: pd.Series, threshold: float = 3.0):
    """Return a boolean mask: True where the value is an outlier."""
    mean, std = series.mean(), series.std()
    z = (series - mean) / std          # how many standard deviations from the mean
    return z.abs() > threshold

mask = zscore_outliers(df["house_size_sqft"])
print(f"Z-score found {mask.sum()} outliers")
```

⚠️ **Warning:** The Z-score uses the mean and std — both are themselves distorted by outliers. Prefer IQR for skewed data.

### 4.4 Percentile / Tukey trimming

Simplest approach: flag anything below the 1st or above the 99th percentile.

```python
low, high = df["house_size_sqft"].quantile([0.01, 0.99])
mask = (df["house_size_sqft"] < low) | (df["house_size_sqft"] > high)
print(f"Percentile method found {mask.sum()} outliers")
```

### 4.5 Multivariate outliers — Isolation Forest

Sometimes a row looks fine in every column but is weird overall (e.g. a house that is huge but has 1 bedroom). Tree-based **Isolation Forest** catches these.

```python
from sklearn.ensemble import IsolationForest

rng = np.random.default_rng(0)
# Two "normal" features that are correlated
n = 300
sqft = rng.normal(2000, 300, n)
bedrooms = sqft / 500 + rng.normal(0, 0.4, n)
df2 = pd.DataFrame({"sqft": sqft, "bedrooms": bedrooms})
# Inject 5 weird rows: huge sqft but tiny bedroom count
df2 = pd.concat([df2, pd.DataFrame({"sqft": [9000, 9500, 10000, 8500, 12000],
                                     "bedrooms": [1, 1, 2, 1, 3]})],
                ignore_index=True)

iso = IsolationForest(contamination=0.02, random_state=42)  # expect ~2% outliers
df2["is_outlier"] = iso.fit_predict(df2[["sqft", "bedrooms"]])
# fit_predict returns +1 = normal, -1 = outlier
print(df2[df2["is_outlier"] == -1])
```

---

## 5. Handling outliers

Once found, you have **four options**. Which one you pick depends on _why_ the outlier exists.

### Option A — Correct it (if it's a data-entry error)

Best case. Fix the root cause.

```python
# 190 was clearly meant to be 19
df.loc[df["house_size_sqft"] < 500, "house_size_sqft"] = df["house_size_sqft"] / 10
```

### Option B — Remove the rows (if few and clearly bad)

```python
def drop_iqr_outliers(dataframe: pd.DataFrame, column: str):
    """Return a copy of the dataframe with IQR outliers in `column` removed."""
    lower, upper = iqr_outlier_bounds(dataframe[column])
    kept = dataframe[(dataframe[column] >= lower) & (dataframe[column] <= upper)]
    return kept

df_clean = drop_iqr_outliers(df, "house_size_sqft")
print(f"Before: {len(df)}, after: {len(df_clean)}")
```

### Option C — Cap it (Winsorization) — often the best default

Replace extreme values with the boundary values instead of deleting data. You keep the rows, so you lose no information.

```python
def cap_iqr_outliers(dataframe: pd.DataFrame, column: str):
    """Cap values to the IQR fences (winsorize). Returns a modified copy."""
    lower, upper = iqr_outlier_bounds(dataframe[column])
    result = dataframe.copy()
    # clip() replaces anything below `lower` with `lower`, anything above `upper` with `upper`
    result[column] = result[column].clip(lower=lower, upper=upper)
    return result

df_capped = cap_iqr_outliers(df, "house_size_sqft")
print(df_capped["house_size_sqft"].describe())
```

### Option D — Transform the data

For skewed distributions (income, house prices, page views), a **log transform** pulls in extreme values naturally.

```python
# log1p = log(1 + x); the +1 handles zeros safely
df["house_size_log"] = np.log1p(df["house_size_sqft"])
df["house_size_log"].hist(bins=30)
plt.title("After log transform — much more symmetric")
plt.show()
```

---

## 6. A complete, realistic mini-pipeline

```python
import numpy as np
import pandas as pd

np.random.seed(42)

# ---- 1. Create a messy dataset (in real life: pd.read_csv("your_data.csv")) ----
n = 500
data = pd.DataFrame({
    "income":    np.random.lognormal(mean=10, sigma=0.5, size=n),
    "age":       np.random.randint(18, 70, size=n),
    "house_age": np.random.exponential(scale=20, size=n),
})
data.loc[10, "age"] = 250          # typo outlier
data.loc[20, "income"] = 9_999_999 # extreme but real
data = pd.concat([data, pd.DataFrame({"income": [2e6, 3e6], "age": [45, 52], "house_age": [0.2, 0.1]})],
                 ignore_index=True)

# ---- 2. Detect per column with IQR ----
def report_outliers(dataframe: pd.DataFrame):
    for col in dataframe.select_dtypes(include="number").columns:
        lower, upper = iqr_outlier_bounds(dataframe[col])
        count = ((dataframe[col] < lower) | (dataframe[col] > upper)).sum()
        print(f"{col:10s} -> valid range [{lower:>12,.1f}, {upper:>12,.1f}]  | {count} outliers")

report_outliers(data)

# ---- 3. Handle each column appropriately ----
# 'age' typo -> cap to a sensible max
data["age"] = data["age"].clip(upper=100)
# 'income' is skewed -> log transform
data["income_log"] = np.log1p(data["income"])
# 'house_age' near zero looks like bad records -> cap at a small floor
data["house_age"] = data["house_age"].clip(lower=0.5)

print("\nAfter cleaning:")
report_outliers(data[["age", "income_log", "house_age"]])
```

---

## 7. Key takeaways for beginners

1. **Always visualize first.** Never delete data blindly.
2. **Ask why the outlier exists** — typo, error, or genuine rare value? The answer determines the fix.
3. **IQR method** is your safe default for detection.
4. **Capping (winsorization)** is usually better than deleting rows — you keep data.
5. **Log-transform** skewed numeric features like income and prices.
6. **Track what you did.** Fit your outlier rules on the _training set only_ and apply them to the test set, so no information leaks.
7. If outliers are genuine and meaningful (fraud detection!), **keep them** — they may be exactly what you're looking for.

---

## 8. Quick reference table

| Situation                                | Recommended action                                          |
| ---------------------------------------- | ----------------------------------------------------------- |
| Obvious typo (age = 250)                 | Correct or drop the row                                     |
| Few extreme values, skewed data          | Cap (winsorize) or log-transform                            |
| Many outliers (>5–10%)                   | Don't drop — investigate; maybe wrong model or bad features |
| Multivariate weirdness                   | Isolation Forest                                            |
| Outliers are the signal (fraud, defects) | Keep them!                                                  |

Run the companion file `outliers_tutorial.py` to see all of this in action.
