"""
SimpleImputer tutorial - runnable practical script
Dealing with Missing Values for Machine Learning (beginner level)

How to run:
    1. Make sure you have pandas, numpy and scikit-learn installed:
         pip install pandas numpy scikit-learn
    2. Run:  python simpleimputer_tutorial.py

The script creates its own small dataset (customers.csv) so you can run it
as-is, step by step.
"""

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

# ----------------------------------------------------------------------------
# STEP 0: Create a small demo dataset so the script runs without external files
# ----------------------------------------------------------------------------
data = {
    "age":        [25, 30, np.nan, 40, 35, 51, np.nan, 29, 44, 33],
    "salary":     [50000, 60000, 55000, np.nan, 70000, 65000, 80000, 52000, np.nan, 61000],
    "country":    ["France", "Germany", "France", "Spain", np.nan, "Germany", "France", "Spain", "Germany", np.nan],
    "subscribed": ["yes", "yes", "no", "yes", np.nan, "no", "yes", "no", "yes", "no"],
}

# Build a DataFrame from the dictionary above
df = pd.DataFrame(data)

# Save it to a CSV file so we can practice loading data from a file (like real life)
df.to_csv("customers.csv", index=False)
print("Saved demo data to customers.csv\n")

# ----------------------------------------------------------------------------
# STEP 1: Load the data (as you would from any real CSV file)
# ----------------------------------------------------------------------------
df = pd.read_csv("customers.csv")

print("First 5 rows of the raw data:")
print(df.head(), "\n")

# ----------------------------------------------------------------------------
# STEP 2: Inspect - find out WHERE the missing values are
# ----------------------------------------------------------------------------
print("Missing values per column (count):")
print(df.isna().sum(), "\n")

print("Missing values per column (percentage):")
print((df.isna().mean() * 100).round(2), "\n")

# ----------------------------------------------------------------------------
# STEP 3: Strategy 1 - Simple example: fill ONE numeric column with the MEAN
# ----------------------------------------------------------------------------
imputer_mean = SimpleImputer(strategy="mean")          # create imputer that will use the mean
age_filled = imputer_mean.fit_transform(df[["age"]])   # learn mean from age, fill the NaNs
print("age column filled with the MEAN:")
print(age_filled.ravel(), "\n")                       # ravel() flattens to 1D just for printing

# ----------------------------------------------------------------------------
# STEP 4: Strategy 2 - MEDIAN (better when there are extreme values/outliers)
# ----------------------------------------------------------------------------
imputer_median = SimpleImputer(strategy="median")          # create imputer using the median
df[["age"]] = imputer_median.fit_transform(df[["age"]])    # overwrite the age column with filled values

print("age column after MEDIAN imputation (no more NaN):")
print(df["age"].tolist(), "\n")

# ----------------------------------------------------------------------------
# STEP 5: Strategy 3 - MOST FREQUENT (for categorical / text columns)
# ----------------------------------------------------------------------------
imputer_mode = SimpleImputer(strategy="most_frequent")         # fill with the most common value
df[["country"]] = imputer_mode.fit_transform(df[["country"]])  # overwrite country column

print("country column after MOST_FREQUENT imputation (no more NaN):")
print(df["country"].tolist(), "\n")

# ----------------------------------------------------------------------------
# STEP 6: Fill the remaining numeric column (salary) with the MEAN
# ----------------------------------------------------------------------------
imputer_salary = SimpleImputer(strategy="mean")               # create a mean imputer
df[["salary"]] = imputer_salary.fit_transform(df[["salary"]])  # fill missing salaries with the mean

print("salary column after MEAN imputation:")
print(df["salary"].tolist(), "\n")

# ----------------------------------------------------------------------------
# STEP 7: NEVER impute the target (label) column - drop those rows instead
# ----------------------------------------------------------------------------
df = df.dropna(subset=["subscribed"])   # remove rows where the label is missing

print("Data after cleaning - missing values remaining:")
print(df.isna().sum(), "\n")           # should be all zeros now

# ----------------------------------------------------------------------------
# STEP 8: The RIGHT way for ML - fit imputer on TRAIN data only (no leakage!)
# ----------------------------------------------------------------------------
X = df[["age", "salary", "country"]]    # features (inputs)
y = df["subscribed"]                    # target (what we predict)

# Split into 80% training and 20% testing data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Imputer for age: learn the median ONLY from the training data
age_imputer = SimpleImputer(strategy="median")
X_train["age"] = age_imputer.fit_transform(X_train[["age"]])  # fit + transform on train
X_test["age"]  = age_imputer.transform(X_test[["age"]])       # ONLY transform on test (no refit!)

print("Train and test sets for age (no NaN, no leakage):")
print("X_train['age']:", X_train["age"].tolist())
print("X_test['age']:", X_test["age"].tolist(), "\n")

# ----------------------------------------------------------------------------
# STEP 9: The PROFESSIONAL way - Pipeline + ColumnTransformer
# ----------------------------------------------------------------------------
numeric_features = ["age", "salary"]       # numeric columns list
categorical_features = ["country"]         # categorical columns list

# A small pipeline for numeric columns: just imputation
numeric_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median"))   # fill numbers with median
])

# A pipeline for categorical columns: imputation + one-hot encoding
categorical_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),        # fill text with most common
    ("encoder", OneHotEncoder(handle_unknown="ignore"))          # convert text to numbers
])

# Combine both pipelines: each handles its own columns
preprocessor = ColumnTransformer([
    ("num", numeric_pipe, numeric_features),
    ("cat", categorical_pipe, categorical_features)
])

# Final model = preprocessing + classifier, chained together
model = Pipeline([
    ("prep", preprocessor),
    ("clf", RandomForestClassifier(random_state=42))
])

model.fit(X_train, y_train)              # cleaning + encoding + training in ONE call
accuracy = model.score(X_test, y_test)   # evaluate on unseen test data

print(f"Model accuracy on the test set: {accuracy:.2f}")
print("\nDone! Your data was cleaned automatically inside the pipeline.")
