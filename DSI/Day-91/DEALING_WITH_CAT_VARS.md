# Dealing with Categorical Variables (PRACTICAL)

## A Beginner's Guide to Encoding Categorical Data for Machine Learning

---

## 📌 What You Will Learn

By the end of this tutorial you will be able to:

1. Understand **why** ML models need numbers, not text
2. Choose the right encoding method for each situation:
   - **One-Hot Encoding** (nominal variables)
   - **Ordinal Encoding** (variables with a natural order)
   - **Label Encoding** (and when NOT to use it)
3. Understand the **dummy variable trap** (collinearity) and how to avoid it
4. Handle **high-cardinality** variables (columns with many categories)
5. Use scikit-learn pipelines (`OneHotEncoder`, `OrdinalEncoder`, `ColumnTransformer`) the professional way
6. Interpret models after one-hot encoding (feature names, multicollinearity checks)

---

## 🧩 1. What Are Categorical Variables?

Categorical variables are columns containing **labels** instead of numbers. They come in two types:

| Type        | Meaning             | Example                                           |
| ----------- | ------------------- | ------------------------------------------------- |
| **Nominal** | No natural order    | `City`: "Lagos", "Accra", "Nairobi"               |
| **Ordinal** | Has a natural order | `Education`: "Primary" < "Secondary" < "Tertiary" |
| **Binary**  | Only two categories | `Gender`: "Male", "Female"                        |

> Machines do math on numbers. A model cannot compute `"Lagos" × 2.5`. So we must **convert categories into numbers** — a process called **encoding**.

---

## 🗺️ 2. Choosing the Right Encoding — The Decision Map

```
Is there a natural order?
├── YES → Ordinal Encoding (rank-based numbers: 0, 1, 2, ...)
└── NO  → How many unique categories?
          ├── Few (e.g. < 15) → One-Hot Encoding ✅
          ├── Many (e.g. 15–50) → One-Hot + grouping rare categories
          └── Very many (e.g. > 50) → Target/Mean encoding or embeddings (advanced)
```

**Rule of thumb for beginners:** one-hot for unordered variables, ordinal encoding for ordered ones, and never plain label encoding for nominal features in linear models.

---

## 🔥 3. One-Hot Encoding (The Most Important Technique)

### The idea

One-hot encoding creates a **new binary column (0/1) for every category**. Each row gets a `1` in the column of its category and `0` everywhere else.

**Before:**

| City    |
| ------- |
| Lagos   |
| Accra   |
| Nairobi |

**After one-hot:**

| City_Lagos | City_Accra | City_Nairobi |
| ---------- | ---------- | ------------ |
| 1          | 0          | 0            |
| 0          | 1          | 0            |
| 0          | 0          | 1            |

```python
import pandas as pd
import numpy as np

data = {
    "City":       ["Lagos", "Accra", "Nairobi", "Lagos", "Accra"],
    "Gender":     ["Male", "Female", "Male", "Female", "Male"],
    "Education":  ["Tertiary", "Secondary", "Primary", "Tertiary", "Secondary"],
    "Age":        [25, 30, 28, 35, 22],
    "Bought":     [1, 0, 1, 0, 1],
}
df = pd.DataFrame(data)

# pandas way: get_dummies()
df_encoded = pd.get_dummies(df, columns=["City", "Gender"], dtype=int)
print(df_encoded)
```

### ⚠️ The Dummy Variable Trap (Collinearity) — THIS IS IMPORTANT

If you keep **ALL** the one-hot columns, they become **perfectly correlated**. Example:

```
City_Lagos + City_Accra + City_Nairobi = 1  (always!)
```

This means one column is exactly predictable from the others — a problem called **perfect multicollinearity**. For **linear models** (linear regression, logistic regression), this makes coefficients unstable and uninterpretable.

**The fix: drop one category** (called the _reference_ or _baseline_ category).

```python
# drop_first=True removes one column per feature to avoid perfect collinearity
df_encoded = pd.get_dummies(df, columns=["City", "Gender"], drop_first=True, dtype=int)
print(df_encoded)
```

> **Note:** Tree-based models (Random Forest, XGBoost) don't suffer from the dummy variable trap — keeping all columns is harmless for them (but still slightly wasteful). For linear models, **always drop one**.

> **scikit-learn tip:** modern `OneHotEncoder` uses `drop="first"` for the same purpose, and `handle_unknown="ignore"` so new categories at prediction time don't crash the model.

---

## 📏 4. Ordinal Encoding (For Ordered Categories)

When categories have a natural order, replace them with **ordered integers**:

```python
from sklearn.preprocessing import OrdinalEncoder

# The ORDER of categories must be specified explicitly (most important line!)
education_order = [["Primary", "Secondary", "Tertiary"]]

encoder = OrdinalEncoder(categories=education_order)
df["Education_encoded"] = encoder.fit_transform(df[["Education"]])

print(df[["Education", "Education_encoded"]])
```

**Output:**

| Education | Education_encoded |
| --------- | ----------------- |
| Tertiary  | 2                 |
| Secondary | 1                 |
| Primary   | 0                 |

**When to use:** education level, satisfaction ratings ("Bad" < "Okay" < "Good" < "Excellent"), age groups, T-shirt sizes (S/M/L/XL).

**⚠️ Caution:** If you give the wrong order (or encode an unordered variable this way), the model assumes false mathematical relationships ("Accra" is 2× "Lagos" — nonsense!).

---

## 🏷️ 5. Label Encoding (Use With Caution!)

Assigns each category an arbitrary integer (0, 1, 2, 3...):

```python
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df["City_label"] = le.fit_transform(df["City"])
print(df[["City", "City_label"]])
```

**The problem:** it imposes a fake order. If Lagos=0, Accra=1, Nairobi=2, a linear model thinks Nairobi > Accra > Lagos numerically. That's usually **wrong for nominal data**.

**When label encoding IS fine:**

- The **target variable** in classification (e.g. "Yes"/"No" → 1/0)
- Tree-based models are somewhat tolerant, but one-hot is still safer for nominal features

---

## 🃏 6. High-Cardinality Variables (Too Many Categories)

If a column has 50+ unique values (e.g. `Zip_Code`, `Product_ID`), one-hot creates 50+ new columns — slow models, sparse data, overfitting risk.

**Practical solutions:**

1. **Group rare categories** into `"Other"` before encoding:

```python
# Keep the top 2 most frequent cities; everything else becomes "Other"
top_cities = df["City"].value_counts().nlargest(2).index
df["City_grouped"] = df["City"].where(df["City"].isin(top_cities), "Other")
```

2. **Use only the top-K categories** and bucket the rest.
3. **(Advanced)** Target encoding / mean encoding — replace each category with the average target value of rows in that category. Powerful but risky (causes data leakage if done wrong — only use inside pipelines with cross-validation).

---

## 🏗️ 7. The Professional Pipeline Approach

Just like with missing values, the clean way is to put encoding **inside a scikit-learn `Pipeline`** with `ColumnTransformer`:

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Define which encoding applies to which columns
nominal_cols = ["City", "Gender"]           # unordered -> one-hot
ordinal_cols = ["Education"]                # ordered -> ordinal
numeric_cols = ["Age"]

preprocessor = ColumnTransformer([
    ("nominal", OneHotEncoder(drop="first", handle_unknown="ignore"), nominal_cols),
    ("ordinal", OrdinalEncoder(categories=[["Primary", "Secondary", "Tertiary"]]), ordinal_cols),
    ("numeric", StandardScaler(), numeric_cols),
])

# Full pipeline: preprocess + model (drop="first" avoids the dummy variable trap for linear models)
model = Pipeline([
    ("prep", preprocessor),
    ("clf", LogisticRegression(max_iter=1000)),
])

X = df.drop("Bought", axis=1)
y = df["Bought"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)
print("Score:", model.score(X_test, y_test))
```

**Why this is the professional way:**

- Encoding is fit on training data only (no leakage)
- New/unseen categories at prediction time are handled gracefully (`handle_unknown="ignore"`)
- One object = preprocess + model, easy to save and deploy
- `drop="first"` protects linear models from collinearity automatically

---

## 🔬 8. Inspecting the Encoded Features (Feature Names)

After one-hot, it's useful to see which column corresponds to which category:

```python
# Get the feature names after transformation (works on scikit-learn >= 1.0)
feature_names = model.named_steps["prep"].get_feature_names_out()
print(feature_names)
```

**Interpreting coefficients in linear models:** with `drop="first"`, the dropped category is the _baseline_. A coefficient of +0.8 on `City_Accra` means "Accra vs the baseline city changes the log-odds by +0.8".

---

## ⚠️ 9. Common Beginner Mistakes (Checklist)

| Mistake                                       | Why it's bad                               | Fix                                     |
| --------------------------------------------- | ------------------------------------------ | --------------------------------------- |
| Label-encoding nominal data for linear models | Fake order imposed                         | Use one-hot                             |
| Keeping ALL one-hot columns in linear models  | Perfect collinearity (dummy variable trap) | `drop_first=True` / `drop="first"`      |
| Encoding before train/test split              | Data leakage                               | Encode inside a Pipeline                |
| One-hot encoding high-cardinality columns     | Thousands of sparse columns                | Group rare values / target encoding     |
| Wrong order in `OrdinalEncoder`               | False assumptions about distances          | Always pass explicit `categories=[...]` |
| Forgetting `handle_unknown="ignore"`          | Crash on new categories at prediction      | Add it to `OneHotEncoder`               |

---

## ✅ 10. Quick Decision Guide

| Situation                         | Recommended encoding                           |
| --------------------------------- | ---------------------------------------------- |
| Unordered, few categories         | One-hot (`drop="first"` for linear models)     |
| Ordered categories                | Ordinal encoding with explicit order           |
| Target variable in classification | Label encoding                                 |
| Many categories (50+)             | Group rare ones, or target encoding (advanced) |
| Tree models (RF, XGBoost)         | One-hot fine; ordinal also acceptable          |
| Linear/logistic regression        | One-hot with `drop="first"` **mandatory**      |

---

## 🏁 Summary

- Categorical data must be converted to numbers before ML — this is called **encoding**.
- **One-hot encoding** is the workhorse for unordered categories; watch out for the **dummy variable trap** (drop one column for linear models).
- **Ordinal encoding** fits naturally ordered categories — always specify the order yourself.
- **Label encoding** is mainly for target variables — avoid it for nominal features in linear models.
- Put everything in a scikit-learn `Pipeline` + `ColumnTransformer` to avoid leakage and handle new categories gracefully.

Happy encoding! 🎯
