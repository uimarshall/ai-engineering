"""
Dealing with Categorical Variables (PRACTICAL)
==============================================
Beginner-friendly, fully runnable tutorial on encoding categorical data.
Run: python dealing_with_categorical_variables.py
Every section is commented line-by-line.
"""

import numpy as np  # numpy: used for numeric operations and NaN handling
import pandas as pd  # pandas: main library for tabular data
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    LabelEncoder,
    OneHotEncoder,
    OrdinalEncoder,
    StandardScaler,
)

# =============================================================================
print("\n" + "=" * 60)
# (In real life: df = pd.read_csv("your_file.csv"))
# =============================================================================

data = {
    "City": ["Lagos", "Accra", "Nairobi", "Lagos", "Accra", "Nairobi", "Lagos"],
    "Gender": ["Male", "Female", "Male", "Female", "Male", "Female", "Male"],
    "Education": [
        "Tertiary",
        "Secondary",
        "Primary",
        "Tertiary",
        "Secondary",
        "Primary",
        "Tertiary",
    ],
    "Satisfaction": ["Good", "Bad", "Okay", "Excellent", "Good", "Bad", "Okay"],
    "Age": [25, 30, 28, 35, 22, 40, 29],
    "Bought": [1, 0, 1, 0, 1, 0, 1],
}

df = pd.DataFrame(data)

print("=" * 60)
print("1. ORIGINAL DATASET")
print("=" * 60)
print(df)

print("\n" + "=" * 60)
# =============================================================================
# 2. EXPLORING CATEGORICAL COLUMNS (know your data before encoding!)
# =============================================================================
print("2. UNIQUE VALUES PER COLUMN")
print("=" * 60)
for col in ["City", "Gender", "Education", "Satisfaction"]:
    print(f"{col}: {df[col].unique()}  ({df[col].nunique()} unique)")

# =============================================================================
# 3. ONE-HOT ENCODING WITH PANDAS (get_dummies)
# =============================================================================
# The dummy variable trap: if we keep ALL one-hot columns, one column can be
# perfectly predicted from the others (City_Lagos + City_Accra + City_Nairobi = 1).
# For LINEAR models this causes perfect multicollinearity -> unstable coefficients.
# FIX: drop_first=True removes one column per feature (the baseline category).

print("\n" + "=" * 60)
# columns=[...] -> only encode these columns (Age and Bought stay numeric)
# drop_first=True -> drop one category per column to avoid collinearity
# dtype=int -> output 0/1 as integers instead of True/False

df_onehot = pd.get_dummies(
    df[["City", "Gender", "Education", "Satisfaction"]],
    drop_first=True,
    dtype=int,
)
print("3. ONE-HOT ENCODED (drop_first=True avoids the dummy variable trap)")
print("=" * 60)
print(df_onehot)

# =============================================================================
# 4. ORDINAL ENCODING (for categories WITH a natural order)
# =============================================================================
# WARNING: you must supply the order yourself! Wrong order = wrong model assumptions.

print("\n" + "=" * 60)

# Categories listed from LOWEST to HIGHEST
satisfaction_order = ["Bad", "Okay", "Good", "Excellent"]
education_order = [["Primary", "Secondary", "Tertiary"]]

ord_encoder = OrdinalEncoder(categories=[satisfaction_order])
df["Satisfaction_encoded"] = ord_encoder.fit_transform(df[["Satisfaction"]])

print("4. ORDINAL ENCODING ('Bad'->0, 'Okay'->1, 'Good'->2, 'Excellent'->3)")
print("=" * 60)
print(df[["Satisfaction", "Satisfaction_encoded"]])

# =============================================================================
# 5. LABEL ENCODING (USE WITH CAUTION - mostly for TARGET variables)
# =============================================================================
print("\n" + "=" * 60)
# "Lagos"=0, "Accra"=1, "Nairobi"=2 makes a linear model think Nairobi > Accra > Lagos.

le = LabelEncoder()
df["City_label"] = np.asarray(le.fit_transform(df["City"]))

print("5. LABEL ENCODING (arbitrary integers - DANGEROUS for nominal data)")
print("=" * 60)
print(df[["City", "City_label"]])

# Demonstrating WHY it's dangerous: the mapping is arbitrary, not meaningful
print(
    "\nMapping learned by LabelEncoder:",
    dict(zip(le.classes_.tolist(), range(len(le.classes_)))),
)

# =============================================================================
# 6. HIGH-CARDINALITY FIX: GROUP RARE CATEGORIES INTO "Other"
# =============================================================================
# One-hot on a column with 50+ categories creates 50+ columns (slow, overfits).
# Solution: keep only the most frequent categories, bucket the rest as "Other".

top_cities = df["City"].value_counts().nlargest(2).index
# .where(condition, other) keeps the value where the condition is True,
# otherwise replaces it with "Other"
df["City_grouped"] = df["City"].where(df["City"].isin(top_cities), "Other")

print("\n" + "=" * 60)
print("6. GROUPED RARE CATEGORIES (top 2 cities, rest -> 'Other')")
print("=" * 60)
print(df[["City", "City_grouped"]])

# =============================================================================
# 7. THE PROFESSIONAL PIPELINE APPROACH (scikit-learn)
# =============================================================================
# Encoding inside a Pipeline means: no data leakage, unseen categories handled,
# and one object that does preprocess + model together.

# --- Step A: define feature groups ---
nominal_cols = ["City", "Gender"]
ordinal_cols = ["Education"]
numeric_cols = ["Age"]

# --- Step B: build the preprocessor ---
preprocessor = ColumnTransformer(
    transformers=[
        (
            "nominal",
            OneHotEncoder(drop="first", handle_unknown="ignore"),
            nominal_cols,
        ),
        (
            "ordinal",
            OrdinalEncoder(categories=education_order),
            ordinal_cols,
        ),
        (
            "numeric",
            StandardScaler(),
            numeric_cols,
        ),
    ],
)

# --- Step C: full pipeline = preprocessing + classifier ---
model = Pipeline(
    steps=[
        ("prep", preprocessor),
        ("clf", LogisticRegression(max_iter=1000)),
    ]
)

# --- Step D: split features (X) and target (y), then train/test split ---
X = df[["City", "Gender", "Education", "Age"]]
y = df["Bought"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
)

# --- Step E: fit the pipeline (learns encodings from TRAIN data only) ---
model.fit(X_train, y_train)

print("\n" + "=" * 60)
# --- Step F: evaluate ---
print("7. PIPELINE TEST ACCURACY:", round(model.score(X_test, y_test), 4))
print("=" * 60)

# =============================================================================
# 8. INSPECT THE ENCODED FEATURE NAMES
# =============================================================================
# After one-hot, column names tell you which category each 0/1 column represents.
feature_names = model.named_steps["prep"].get_feature_names_out()
print("\nEncoded feature names:")
for name in feature_names:
    print("  -", name)

# =============================================================================
# 9. PREDICT ON BRAND-NEW DATA (unseen category handled gracefully)
# =============================================================================
print("\nDone! You now understand one-hot, ordinal, and label encoding -")
new_customer = pd.DataFrame(
    {
        "City": ["Kigali"],
        "Gender": ["Female"],
        "Education": ["Secondary"],
        "Age": [33],
    }
)

pred = model.predict(new_customer)
prob = model.predict_proba(new_customer)

print("\n" + "=" * 60)
print("9. PREDICTION FOR NEW CUSTOMER (unseen city 'Kigali')")
print("=" * 60)
print("Predicted class (1=bought, 0=not bought):", pred[0])
print("Probability [not bought, bought]:", np.round(prob[0], 3))

# =============================================================================
# 10. DUMMY VARIABLE TRAP - NUMERIC DEMONSTRATION
# =============================================================================
# Proof that keeping ALL one-hot columns creates perfect collinearity:
# the sum of all city dummies equals 1 for every single row.

dummies_full = pd.get_dummies(df["City"], dtype=int)
print("\n" + "=" * 60)
print("10. DUMMY VARIABLE TRAP DEMONSTRATION")
print("=" * 60)
print(dummies_full)
print("\nRow sums of all city dummies (always 1 -> perfect collinearity):")
print(dummies_full.sum(axis=1).tolist())

print("\nDone! You now understand one-hot, ordinal, and label encoding -")
print("plus the dummy variable trap and how pipelines solve it.")
