"""
Dealing with Missing Categorical Variables (PRACTICAL)
=======================================================
Beginner-friendly, fully runnable tutorial.
Run this file: python dealing_with_missing_categorical.py
Every section is commented line-by-line.
"""

import numpy as np  # numpy is used here to create NaN values easily
import pandas as pd  # pandas is the main library for tabular data

# =============================================================================
# 1. CREATE A SMALL SAMPLE DATASET (in real life you would read a CSV with
#    pd.read_csv("your_file.csv") instead)
# =============================================================================

data = {
    "Gender": ["Male", "Female", np.nan, "Female", "Male", np.nan, "Male"],
    "City": ["Lagos", "Accra", "Nairobi", np.nan, "Accra", "Lagos", np.nan],
    "Product_Type": [
        "Electronics",
        "Clothing",
        np.nan,
        "Food",
        "Electronics",
        "Clothing",
        "Food",
    ],
    "Education": [
        "Tertiary",
        "Secondary",
        np.nan,
        "Primary",
        "Tertiary",
        "Secondary",
        "Primary",
    ],
    "Age": [25, 30, 28, 35, 22, 40, 29],  # numeric column, no missing values here
    "Bought_Product": [1, 0, 1, 0, 1, 0, 1],  # target variable for ML (0 = no, 1 = yes)
}

df = pd.DataFrame(data)  # build the DataFrame from the dictionary

print("=" * 60)
print("1. ORIGINAL DATASET")
print("=" * 60)
print(df)

# =============================================================================
# 2. DETECT MISSING VALUES
# =============================================================================

print("\n" + "=" * 60)
print("2. MISSING VALUES PER COLUMN")
print("=" * 60)
print(df.isna().sum())  # counts how many NaN values each column has

print("\nPercentage missing per column:")
print(
    (df.isna().mean() * 100).round(2)
)  # converts counts to percentages (rounded to 2 decimals)

print("\nUnique values in the 'Gender' column:")
print(
    df["Gender"].unique()
)  # shows all distinct values - useful to spot hidden placeholders like '?' or 'NA'

# =============================================================================
# 3. TECHNIQUE 1: DROP ROWS (only when very few rows are missing)
# =============================================================================

df_dropped = df.dropna(subset=["City"])  # keeps only rows where 'City' is NOT missing
print("\n" + "=" * 60)
print("3. AFTER DROPPING ROWS WITH MISSING 'City':")
print("=" * 60)
print(df_dropped)

# =============================================================================
# 4. TECHNIQUE 2: FILL WITH THE MODE (most frequent value)
# =============================================================================

mode_gender = df["Gender"].mode()[
    0
]  # .mode() returns a Series of most frequent values; [0] takes the first
print("\n" + "=" * 60)
print("4. Mode (most frequent value) of 'Gender':", mode_gender)
print("=" * 60)

df["Gender"] = df["Gender"].fillna(
    mode_gender
)  # replace every NaN in 'Gender' with the mode
print(df[["Gender"]])

# =============================================================================
# 5. TECHNIQUE 3: FILL WITH A PLACEHOLDER CATEGORY ("Unknown")
# =============================================================================

# This preserves the fact that the value was missing - missingness itself can be
# useful information (e.g. people who skipped a survey question).
df["Product_Type"] = df["Product_Type"].fillna("Unknown")
print("\n" + "=" * 60)
print("5. AFTER FILLING 'Product_Type' WITH 'Unknown':")
print("=" * 60)
print(df[["Product_Type"]])

# =============================================================================
# 6. TECHNIQUE 4: FILL BASED ON ANOTHER COLUMN (group mode imputation)
# =============================================================================
# We simulate a 'Region' column to demonstrate the idea: each person's city is
# filled with the most common city WITHIN THEIR REGION.

df["Region"] = [
    "West",
    "West",
    "East",
    "East",
    "West",
    "East",
    "West",
]  # extra column for the demo

# groupby("Region") splits the data by region
# transform applies the lambda to each group and returns a result aligned with the original index
df["City"] = df.groupby("Region")["City"].transform(
    lambda x: x.fillna(x.mode()[0] if not x.mode().empty else "Unknown")
)
# Explanation of the lambda: for each region-group x,
#   x.mode()[0]                    -> the most frequent city in that region
#   if not x.mode().empty else ... -> if the whole group is NaN (no mode), fall back to "Unknown"

print("\n" + "=" * 60)
print("6. AFTER GROUP-BASED IMPUTATION OF 'City' BY 'Region':")
print("=" * 60)
print(df[["Region", "City"]])

# =============================================================================
# 7. VERIFY: CHECK NO MISSING VALUES REMAIN
# =============================================================================

print("\n" + "=" * 60)
print("7. REMAINING MISSING VALUES:")
print("=" * 60)
print(df.isna().sum())  # every column should now show 0

# =============================================================================
# 8. THE PROFESSIONAL APPROACH: SCIKIT-LEARN PIPELINE
# =============================================================================
# Instead of filling values by hand (as above), real projects put imputation
# INSIDE a Pipeline so it is learned from training data only (no data leakage)
# and applied automatically to new data.

from sklearn.compose import (
    ColumnTransformer,  # applies different pipelines to different column types
)
from sklearn.ensemble import (
    RandomForestClassifier,  # an ML model that works well out of the box
)
from sklearn.impute import SimpleImputer  # fills missing values automatically
from sklearn.metrics import accuracy_score  # measures how good our predictions are
from sklearn.model_selection import (
    train_test_split,  # splits data into train and test sets
)
from sklearn.pipeline import Pipeline  # chains preprocessing + model into one object
from sklearn.preprocessing import (
    OneHotEncoder,  # converts categories into numbers (0/1 columns)
)

# ---- Step A: separate features (X) from the target (y) ----
X = df.drop("Bought_Product", axis=1)  # X = all columns EXCEPT the target
y = df["Bought_Product"]  # y = the column we want to predict

# ---- Step B: identify which columns are categorical vs numeric ----
cat_cols = X.select_dtypes(
    include="object"
).columns.tolist()  # columns with text/categories
num_cols = X.select_dtypes(include="number").columns.tolist()  # columns with numbers

print("\nCategorical columns:", cat_cols)
print("Numerical columns:", num_cols)

# ---- Step C: build a preprocessing pipeline for categorical columns ----
cat_pipeline = Pipeline(
    [
        (
            "imputer",
            SimpleImputer(strategy="most_frequent"),
        ),  # fill NaN with the MODE of each column
        (
            "onehot",
            OneHotEncoder(handle_unknown="ignore"),
        ),  # turn each category into 0/1 columns;
        # 'ignore' prevents errors on unseen categories
    ]
)

# ---- Step D: build a pipeline for numerical columns ----
num_pipeline = Pipeline(
    [
        (
            "imputer",
            SimpleImputer(strategy="median"),
        ),  # fill numeric NaN with the median (robust to outliers)
    ]
)

# ---- Step E: combine both pipelines with ColumnTransformer ----
preprocessor = ColumnTransformer(
    [
        (
            "cat",
            cat_pipeline,
            cat_cols,
        ),  # apply cat_pipeline to all categorical columns
        ("num", num_pipeline, num_cols),  # apply num_pipeline to all numerical columns
    ]
)

# ---- Step F: build the final model = preprocessing + classifier ----
model = Pipeline(
    [
        ("preprocess", preprocessor),  # first, impute and encode
        (
            "clf",
            RandomForestClassifier(random_state=42),
        ),  # then, train the model (random_state = reproducibility)
    ]
)

# ---- Step G: split data into training (80%) and testing (20%) sets ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---- Step H: train the model ----
model.fit(
    X_train, y_train
)  # learns imputation values + encodings + the classifier, all from TRAIN data only

# ---- Step I: evaluate on the test set ----
predictions = model.predict(X_test)  # make predictions on unseen test data
print("\n" + "=" * 60)
print("8. MODEL ACCURACY ON TEST SET:", accuracy_score(y_test, predictions))
print("=" * 60)

# ---- Step J: predict on brand-new data (the pipeline handles imputation + encoding automatically) ----
new_customer = pd.DataFrame(
    {
        "Gender": ["Female"],
        "City": [
            "Unknown"
        ],  # never seen by the model - OneHotEncoder(handle_unknown="ignore") handles it
        "Product_Type": ["Unknown"],
        "Education": ["Secondary"],
        "Age": [27],
        "Region": ["East"],
    }
)

new_prediction = model.predict(new_customer)
print(
    "\nPrediction for new customer (1 = will buy, 0 = will not buy):", new_prediction[0]
)

print("\nDone! You have learned to detect and handle missing categorical variables.")
