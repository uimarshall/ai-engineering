# =============================================================================
# DEALING WITH MISSING VALUES IN PANDAS — Practical Tutorial for ML
# =============================================================================
# This script accompanies the markdown tutorial.
# Run it top to bottom:  python dealing_with_missing_values_pandas.py
# =============================================================================

import numpy as np
import pandas as pd

# Pretty-print pandas tables
pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)


# -----------------------------------------------------------------------------
# 1. CREATE A REALISTIC MESSY DATASET
# -----------------------------------------------------------------------------
# np.nan is how pandas represents a missing numeric value
data = {
    "customer_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "age": [25, np.nan, 41, 33, np.nan, 52, 29, np.nan, 47, 36],
    "income": [50000, 62000, np.nan, 48000, 71000, np.nan, 54000, 39000, np.nan, 66000],
    "years_customer": [3, 5, np.nan, 1, 8, 12, 2, np.nan, 15, 7],
    "purchased": ["yes", "no", "yes", np.nan, "yes", "no", "yes", "no", np.nan, "yes"],
}

# Build the DataFrame
df = pd.DataFrame(data)

print("=" * 70)
print("ORIGINAL DATA (note the NaN values)")
print("=" * 70)
print(df)
print()


# -----------------------------------------------------------------------------
# 2. DETECT MISSING VALUES
# -----------------------------------------------------------------------------
print("=" * 70)
print("STEP 1 — DETECTION")
print("=" * 70)

# .isna() returns a True/False mask (True = value is missing)
print("\nBoolean mask of missing values (df.isna()):")
print(df.isna())

# .sum() on that mask counts the Trues per column
print("\nMissing count per column (df.isna().sum()):")
print(df.isna().sum())

# .mean() gives the fraction missing; x100 turns it into a percentage
print("\nMissing PERCENTAGE per column:")
print((df.isna().mean() * 100).round(2).astype(str) + "%")

# Which ROWS have at least one missing value?
print("\nRows containing at least one missing value:")
print(df[df.isna().any(axis=1)])
print()


# -----------------------------------------------------------------------------
# 3. DROPPING MISSING VALUES
# -----------------------------------------------------------------------------
print("=" * 70)
print("STEP 2 — DROPPING (use only when you can afford to lose data)")
print("=" * 70)

# Drop every ROW that has ANY missing value
df_drop_all = df.dropna()
print("\ndf.dropna() -> rows left:", len(df_drop_all), "out of", len(df))

# Drop rows only when a SPECIFIC column is missing
df_drop_age = df.dropna(subset=["age"])
print("dropna(subset=['age']) -> rows left:", len(df_drop_age))

# Drop COLUMNS that are mostly empty (e.g., more than half missing)
half_rows = int(0.5 * len(df))
df_drop_cols = df.dropna(axis=1, thresh=half_rows)
print("dropna(axis=1, thresh=half*rows) -> columns kept:", list(df_drop_cols.columns))
print()


# -----------------------------------------------------------------------------
# 4. BASIC IMPUTATION (FILLING) WITH PANDAS
# -----------------------------------------------------------------------------
print("=" * 70)
print("STEP 3 — BASIC IMPUTATION WITH PANDAS")
print("=" * 70)

df_filled = df.copy()  # work on a copy so the original stays intact

# 4a) Fill a categorical column with a constant string
df_filled["purchased"] = df_filled["purchased"].fillna("unknown")
print("\nAfter fillna('unknown') in 'purchased':")
print(df_filled["purchased"])

# 4b) Fill a numeric column with its MEAN
# Mean is fine for symmetric data with no extreme outliers
age_mean = df_filled["age"].mean()  # compute the mean
df_filled["age"] = df_filled["age"].fillna(age_mean)  # fill gaps with it
print("\nAge filled with the mean (%.2f):" % age_mean)
print(df_filled["age"])

# 4c) Fill a skewed numeric column with its MEDIAN (robust to outliers)
income_median = df_filled["income"].median()  # compute the median
df_filled["income"] = df_filled["income"].fillna(income_median)
print("\nIncome filled with the median (%.2f):" % income_median)
print(df_filled["income"])

# 4d) Forward fill — carry the LAST valid value forward (good for ordered data)
df_filled["years_customer"] = df_filled[
    "years_customer"
].ffill()  # same as fillna(method='ffill')
print("\n'years_customer' after forward fill (ffill):")
print(df_filled["years_customer"])

# 4e) Add a binary "was missing" INDICATOR column before filling
# Sometimes the fact a value is missing is itself predictive!
df_flag = df.copy()
df_flag["income_was_missing"] = (
    df_flag["income"].isna().astype(int)
)  # 1 if missing, else 0
df_flag["income"] = df_flag["income"].fillna(df_flag["income"].median())
print("\nIndicator column + imputed income:")
print(df_flag[["income", "income_was_missing"]])

# 4f) Fill with a GROUP statistic (smarter than a global value)
# Fill each missing age with the average age of that purchased-group
df_group = df.copy()
df_group["age"] = df_group["age"].fillna(
    df_group.groupby("purchased")["age"].transform(
        "mean"
    )  # group mean broadcast to each row
)
print("\nAge filled with the mean of each 'purchased' group:")
print(df_group[["age", "purchased"]])
print()


# -----------------------------------------------------------------------------
# 5. THE ML-GRADE WAY: SimpleImputer (scikit-learn)
# -----------------------------------------------------------------------------
print("=" * 70)
print("STEP 4 — SimpleImputer (the ML-grade approach)")
print("=" * 70)

from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

# Split into features (X) and target (y)
X = df.drop(columns=["purchased"])  # features
y = df["purchased"]  # target column

# IMPORTANT: rows where the TARGET itself is missing carry no training signal,
# so we drop them BEFORE splitting (you cannot learn from an unlabeled row).
labeled = y.notna()  # True where the target label exists
X = X[labeled]  # keep only rows with a label
y = y[labeled]

# Create a train/test split (80% train, 20% test) with a fixed random seed
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Imputer for NUMERIC columns: median strategy (robust to outliers)
num_imputer = SimpleImputer(strategy="median")

# Imputer for CATEGORICAL columns: fill with the most frequent value
cat_imputer = SimpleImputer(strategy="most_frequent")

# Columns we will impute
num_cols = ["age", "income", "years_customer"]

# IMPORTANT: fit ONLY on the training data to avoid data leakage,
# then use that fitted imputer to transform the test data.
X_train[num_cols] = num_imputer.fit_transform(
    X_train[num_cols]
)  # learn medians from TRAIN
X_test[num_cols] = num_imputer.transform(
    X_test[num_cols]
)  # apply the SAME medians to TEST

print("\nX_train after median imputation:")
print(X_train)
print("\nX_test after median imputation (no leakage):")
print(X_test)


# -----------------------------------------------------------------------------
# 6. KNN IMPUTATION (smarter, uses similar rows)
# -----------------------------------------------------------------------------
print("=" * 70)
print("STEP 5 — KNNImputer (fill from similar rows)")
print("=" * 70)

from sklearn.impute import KNNImputer

# KNN imputer: fills a missing value using the average of the 3 nearest rows
knn_imputer = KNNImputer(n_neighbors=3)

X_train_knn = X_train.copy()
X_train_knn[num_cols] = knn_imputer.fit_transform(X_train[num_cols])

print("\nX_train after KNN imputation (k=3):")
print(X_train_knn)


# -----------------------------------------------------------------------------
# 7. FULL PIPELINE (best practice for real ML projects)
# -----------------------------------------------------------------------------
print("=" * 70)
print("STEP 6 — Pipeline with imputation built in (best practice)")
print("=" * 70)

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

numeric_features = ["age", "income", "years_customer"]

# ColumnTransformer applies the imputer only to the numeric columns
preprocessor = ColumnTransformer(
    transformers=[("num", SimpleImputer(strategy="median"), numeric_features)]
)

# A Pipeline chains preprocessing + model into one object
pipe = Pipeline(
    steps=[
        ("preprocess", preprocessor),  # step 1: impute missing values
        ("model", RandomForestClassifier(random_state=42)),  # step 2: train the model
    ]
)

# Fit the whole pipeline on the raw (still messy) training data —
# the imputation happens automatically, inside the pipeline, leak-free.
pipe.fit(X_train, y_train)

# Evaluate on the test set
accuracy = pipe.score(X_test, y_test)
print("\nPipeline accuracy on test set: %.2f" % accuracy)
print("(A random train/test split on tiny demo data — value is not meaningful here,")
print(" it simply proves the pipeline runs end-to-end.)")


# -----------------------------------------------------------------------------
# 8. FINAL CHECK — VERIFY NO MISSING VALUES REMAIN
# -----------------------------------------------------------------------------
print("=" * 70)
print("FINAL CHECK")
print("=" * 70)

print("\nMissing values left in X_train:", int(X_train.isna().sum().sum()))
print("Missing values left in X_test: ", int(X_test.isna().sum().sum()))

print("\nDone! Key takeaways:")
print(" 1. Detect with isna().sum() / isna().mean()")
print(" 2. Drop only if you can afford to lose rows")
print(" 3. Median for skewed numbers, mean for symmetric, frequent for categories")
print(" 4. In ML: use SimpleImputer inside a Pipeline, fit on train data only")
