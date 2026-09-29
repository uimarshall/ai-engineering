# Dealing with Missing Values — SimpleImputer (Practical Guide)

**Level:** Beginner
**Tools:** Python, pandas, scikit-learn (`SimpleImputer`)

---

## 1. What Is a Missing Value?

A missing value is simply an empty cell in your data. In pandas it usually shows up as `NaN` (Not a Number), `None`, or sometimes a weird placeholder like `"?"`, `"N/A"`, or an empty string `""`.

Real-world datasets are almost never complete. People skip survey questions, sensors fail, forms get submitted half-empty. Machine learning models, however, **cannot work with missing values** — most scikit-learn models will crash with an error the moment they see a `NaN`.

So before training a model, you must decide what to do with those empty cells. The simplest and most common tool for this is **`SimpleImputer`**.

---

## 2. Your Options When You Find Missing Data

When you spot missing values, you basically have three choices:

| Option                                            | When to use it                                                         |
| ------------------------------------------------- | ---------------------------------------------------------------------- |
| **1. Delete** rows or columns with missing values | Very few missing values, or a column is mostly empty anyway            |
| **2. Fill (impute)** them with a sensible value   | The standard, recommended approach — this is what `SimpleImputer` does |
| **3. Predict** them with a model                  | Advanced; overkill for beginners                                       |

> Warning: Deleting rows sounds easy, but if your dataset is small, or the missingness is _not random_ (e.g., high-income people skip the salary question), you can seriously bias your data. **Imputation is usually safer.**

---

## 3. What Is `SimpleImputer`?

`SimpleImputer` is a scikit-learn class that replaces missing values with a single, fixed value derived from the data you give it. It supports four main strategies:

| Strategy          | What it does                                | Typical use                                                                |
| ----------------- | ------------------------------------------- | -------------------------------------------------------------------------- |
| `"mean"`          | Fill with the average of the column         | Numeric data, roughly symmetric distribution                               |
| `"median"`        | Fill with the middle value of the column    | Numeric data with outliers/skew (safer than mean)                          |
| `"most_frequent"` | Fill with the value that appears most often | Categorical data (e.g., fill missing country with the most common country) |
| `"constant"`      | Fill with a value you choose                | When you want "Unknown" for text, or `0` for counts                        |

---

## 4. Quick Start — Filling a Numeric Column with the Mean

```python
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

# A tiny dataset with a missing value (NaN)
df = pd.DataFrame({
    "age": [25, 30, np.nan, 40, 35]
})

imputer = SimpleImputer(strategy="mean")        # create the imputer
df["age"] = imputer.fit_transform(df[["age"]])  # learn the mean, fill NaN

print(df)
# age column: [25, 30, 32.5, 40, 35]  <- the NaN became 32.5 (the mean)
```

The key idea: `fit` **learns** the value to fill (here, the mean = 32.5), and `transform` **applies** the filling. `fit_transform` does both at once.

---

## 5. Step-by-Step Practical Example

Below is a realistic scenario. A CSV file of customers is loaded, inspected for missing values, and cleaned.

```python
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

# ---- 1. Load the data ----
df = pd.read_csv("customers.csv")
print(df.head())

# ---- 2. Find missing values ----
print(df.isna().sum())        # count of NaN per column
print(df.isna().mean() * 100) # same, as a percentage
```

Typical raw data:

```
      age   salary  country  subscribed
0  25.0  50000.0   France         NaN
1   NaN  60000.0  Germany         yes
2  30.0      NaN   France          no
3  40.0  70000.0      NaN         yes
```

| Column       | Plan                                                                           |
| ------------ | ------------------------------------------------------------------------------ |
| `age`        | Numeric → fill with **median** (robust to outliers)                            |
| `salary`     | Numeric → fill with **mean**                                                   |
| `country`    | Categorical → fill with **most frequent**                                      |
| `subscribed` | Tiny amount missing → drop those rows (it's the _label_ — never guess a label) |

### 5.1 Impute numeric columns

```python
num_imputer = SimpleImputer(strategy="median")
df[["age"]] = num_imputer.fit_transform(df[["age"]])
```

### 5.2 Impute categorical columns

```python
cat_imputer = SimpleImputer(strategy="most_frequent")
df[["country"]] = cat_imputer.fit_transform(df[["country"]])
```

### 5.3 Drop rows where the target label is missing

```python
df = df.dropna(subset=["subscribed"])
```

---

## 6. The Two Big Mistakes Beginners Make

### Mistake 1: Filling the target (label) column

Never impute your `y` (the thing you're trying to predict). If a row has no label, you can't train on it — drop it, or fix it at the source.

### Mistake 2: Leaking data — fitting the imputer on the full dataset

**This is the most important rule.** The imputer learns the mean/median from the data it `fit`s on. If you `fit` it on your _entire_ dataset (including the test set), information from the test set "leaks" into your training — and your model evaluation will be dishonestly optimistic.

Correct approach: fit the imputer on the **training data only**, then transform both train and test.

```python
from sklearn.model_selection import train_test_split

X = df[["age", "salary", "country"]]
y = df["subscribed"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

imputer = SimpleImputer(strategy="median")
X_train["age"] = imputer.fit_transform(X_train[["age"]])  # learn mean from TRAIN...
X_test["age"]  = imputer.transform(X_test[["age"]])       # ...apply same value to TEST
```

Notice: `fit_transform` on train, but only `transform` on test.

---

## 7. The Clean Way: `Pipeline` + `ColumnTransformer` (Recommended)

Once you have several columns with different types and strategies, doing it by hand gets messy. The professional way is to combine imputation with encoding in a preprocessing pipeline:

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

numeric_features = ["age", "salary"]
categorical_features = ["country"]

numeric_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median"))
])

categorical_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_pipe, numeric_features),
    ("cat", categorical_pipe, categorical_features)
])

model = Pipeline([
    ("prep", preprocessor),
    ("clf", RandomForestClassifier(random_state=42))
])

model.fit(X_train, y_train)     # imputation happens automatically inside
print(model.score(X_test, y_test))
```

Benefits:

- No manual leakage — everything is fit on training data only.
- The whole cleaning + training process is one object; just `fit` and `predict`.
- The same imputer is applied consistently to new data.

---

## 8. Bonus: When the Missing Value Isn't Written as `NaN`

Sometimes the file literally contains the string `"?"` or `"missing"`. pandas won't recognize those as missing automatically — convert them first:

```python
df = pd.read_csv("data.csv", na_values=["?", "missing", "N/A", ""])  # treat these as NaN
```

You can confirm what pandas sees as missing:

```python
print(df.isna().sum())
```

---

## 9. Summary Cheat Sheet

```python
from sklearn.impute import SimpleImputer

num = SimpleImputer(strategy="median")          # numeric, skewed data
num = SimpleImputer(strategy="mean")            # numeric, normal data
cat = SimpleImputer(strategy="most_frequent")   # categories/text
cat = SimpleImputer(strategy="constant", fill_value="Unknown")  # your own value

imputer.fit(X_train)      # learn fill values from training data ONLY
imputer.transform(X_test) # apply the same learned values to new data
```

**Golden rules:**

1. Inspect first: `df.isna().sum()` — know your enemy.
2. Never impute the target column.
3. Fit on train, transform on test (no data leakage).
4. Use a `Pipeline` + `ColumnTransformer` for anything beyond a toy project.
5. Median beats mean when outliers exist; `"most_frequent"` for categories.
