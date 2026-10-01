# Dealing with Missing Categorical Variables (PRACTICAL)

## A Beginner's Guide to Cleaning and Preparing Categorical Data for Machine Learning

---

## 📌 What You Will Learn

By the end of this tutorial you will be able to:

1. Detect missing values in categorical columns
2. Understand **why** we handle them (not just _how_)
3. Apply the most common, practical techniques:
   - Mode imputation (most frequent value)
   - Imputation with a placeholder category (e.g., `"Unknown"`)
   - Imputation based on another column
4. Compare simple approaches vs. **scikit-learn** pipelines (`SimpleImputer`, `ColumnTransformer`, `Pipeline`)
5. Know which technique to choose and when

---

## 🧩 1. What Are Categorical Variables?

Categorical variables are columns that contain **labels/categories**, not numbers. Examples:

| Column            | Example values                     |
| ----------------- | ---------------------------------- |
| `Gender`          | "Male", "Female"                   |
| `City`            | "Lagos", "Accra", "Nairobi"        |
| `Product_Type`    | "Electronics", "Clothing", "Food"  |
| `Education_Level` | "Primary", "Secondary", "Tertiary" |

Unlike numbers (e.g. age = 25), you **cannot average** categories. So missing values need special treatment.

---

## ⚠️ 2. Why Do We Care About Missing Values?

Most machine learning algorithms (e.g. logistic regression, random forests, XGBoost) **cannot handle `NaN`** in categorical columns, or treat them badly:

- They either **crash** with an error
- Or they **silently ignore** rows with missing values (you lose data!)

So we must decide: **fill them in, remove them, or encode them specially.**

---

## 🔍 3. Detecting Missing Values

In pandas, missing values can appear as:

- `NaN` (standard missing value)
- `None`
- Empty string `""`
- Placeholders like `"?"`, `"NA"`, `"-999"` (common in real-world datasets!)

```python
import pandas as pd
import numpy as np

# Create a tiny sample dataset with missing values
data = {
    "Gender":      ["Male", "Female", np.nan, "Female", "Male"],
    "City":        ["Lagos", "Accra", "Nairobi", np.nan, "Accra"],
    "Product_Type":["Electronics", "Clothing", np.nan, "Food", "Electronics"],
    "Age":         [25, 30, 28, 35, 22],
}
df = pd.DataFrame(data)

# 1. Standard detection
print(df.isna().sum())

# 2. Percentage of missing per column
print((df.isna().mean() * 100).round(2))

# 3. Checking for hidden missing values (placeholders)
print(df["Gender"].unique())   # look for '?' or 'NA'
```

> **Beginner tip:** Always run `.isna().sum()` and also check the _actual unique values_ in each column. Many real datasets use strings like `"?"` instead of `NaN`.

---

## 🛠️ 4. The Practical Techniques

### Technique 1: Drop rows (only if very few are missing)

```python
# Keep only rows where 'Gender' is NOT missing
df_clean = df.dropna(subset=["Gender"])
```

**When to use:** If less than ~1–2% of rows are missing and dropping them doesn't bias your data.

---

### Technique 2: Fill with the **mode** (most frequent value)

The mode is the most common category. It is the standard for categorical imputation.

```python
# Compute the mode (most frequent value) of the 'Gender' column
mode_gender = df["Gender"].mode()[0]
print("Mode of Gender:", mode_gender)

# Fill missing values with the mode
df["Gender"] = df["Gender"].fillna(mode_gender)
```

**When to use:** Good default when missing values are **random** and you want to preserve all rows.

---

### Technique 3: Fill with a **placeholder category** — e.g. `"Unknown"`

This keeps the "missingness" as information, which is often meaningful (e.g. people who didn't answer a survey question).

```python
df["City"] = df["City"].fillna("Unknown")
```

**When to use:** When missingness itself may carry signal. This is often **better than mode imputation** in practice!

---

### Technique 4: Fill based on another column (group imputation)

Example: fill a person's `City` using the most common city _for their region_.

```python
df["City"] = df.groupby("Region")["City"].transform(
    lambda x: x.fillna(x.mode()[0] if not x.mode().empty else "Unknown")
)
```

**When to use:** When a related column can give a smarter guess.

---

### Technique 5: The professional approach — scikit-learn pipelines

Instead of filling values _by hand_ before training, ML practitioners use `SimpleImputer` inside a `Pipeline`. This is cleaner, avoids data leakage, and applies the same steps to new data automatically.

```python
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Separate features (X) and target (y)
X = df.drop("Bought_Product", axis=1)
y = df["Bought_Product"]

# Identify categorical and numerical columns
cat_cols = X.select_dtypes(include="object").columns.tolist()
num_cols = X.select_dtypes(include="number").columns.tolist()

# Build a preprocessing pipeline:
#   1. SimpleImputer(strategy="most_frequent")  -> fills NaN with the mode
#   2. OneHotEncoder                            -> converts categories to numbers
cat_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot",  OneHotEncoder(handle_unknown="ignore")),
])

num_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
])

# Combine both pipelines
preprocessor = ColumnTransformer([
    ("cat", cat_pipeline, cat_cols),
    ("num", num_pipeline, num_cols),
])

# Full pipeline = preprocessing + model
model = Pipeline([
    ("preprocess", preprocessor),
    ("clf", RandomForestClassifier(random_state=42)),
])

# Train / test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Fit and evaluate
model.fit(X_train, y_train)
preds = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))
```

> **Key idea:** Everything is inside the pipeline, so the imputation is learned **only from the training data** and applied consistently to test/new data. This prevents _data leakage_.

---

## 📊 5. Technique Comparison (quick reference)

| Technique                    | Pros                         | Cons                        | When to use                    |
| ---------------------------- | ---------------------------- | --------------------------- | ------------------------------ |
| **Drop rows**                | Simple, no distortion        | Loses data, may bias        | <2% missing, random            |
| **Mode imputation**          | Preserves all rows, easy     | May over-represent the mode | Random missingness             |
| **"Unknown" placeholder**    | Keeps missingness as signal  | Adds a new category         | Missingness may be informative |
| **Group-based imputation**   | Smarter guesses              | Needs a good related column | Strong column relationships    |
| **Pipeline (SimpleImputer)** | No leakage, production-ready | Slightly more setup         | Real ML projects ✅            |

---

## ✅ 6. Practical Recommendations

1. **Always inspect first** — use `.isna().sum()`, `.unique()`, and look for placeholder strings.
2. **Default choice:** `SimpleImputer(strategy="most_frequent")` inside a `Pipeline`.
3. If missingness looks meaningful (e.g. survey non-response), try `fillna("Unknown")` instead.
4. Never impute using information from your test set (avoid leakage) — pipelines handle this for you.
5. After imputation, **verify** with `df.isna().sum()` again.

---

## 🏁 Summary

- Missing categorical values are common and must be handled before training ML models.
- Simplest options: drop rows, fill with mode, or fill with `"Unknown"`.
- The professional approach is `SimpleImputer` + `OneHotEncoder` inside a scikit-learn `Pipeline`, combined with `ColumnTransformer`.
- Choosing a technique depends on **how much** is missing and **whether missingness itself is informative**.

Happy data cleaning! 🧹
