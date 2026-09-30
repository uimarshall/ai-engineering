"""
=============================================================
Dealing with Missing Values - KNNImputer (PRACTICAL)
Data Cleaning & Preparation for Machine Learning
=============================================================

WHAT THIS SCRIPT DOES:
    Example 1: See KNNImputer in action on a tiny hand-made dataset
    Example 2: A realistic, leakage-free ML workflow (scale -> impute -> model)
    Example 3: Compare KNNImputer vs median-fill vs dropping rows
    Example 4: Tune n_neighbors with GridSearchCV

HOW TO RUN:
    python knnimputer_practical.py

REQUIREMENTS:
    pip install numpy pandas scikit-learn
"""

import numpy as np  # numerical computing (arrays, random numbers)
import pandas as pd  # data tables (DataFrames)
from sklearn.impute import KNNImputer, SimpleImputer  # the missing-value tools
from sklearn.linear_model import LinearRegression  # a simple model for demo
from sklearn.metrics import mean_squared_error  # evaluation metric
from sklearn.model_selection import (  # splitting & tuning tools
    GridSearchCV,
    cross_val_score,
    train_test_split,
)
from sklearn.pipeline import Pipeline  # chains steps together
from sklearn.preprocessing import StandardScaler  # feature scaling

# =================================================================
# EXAMPLE 1 - KNNImputer basics on a tiny dataset
# =================================================================
print("=" * 60)
print("EXAMPLE 1: KNNImputer basics")
print("=" * 60)

# Build a tiny dataset: 3 students, 3 numeric columns
df = pd.DataFrame(
    {
        "age": [20, 21, 22],
        "study_hours": [4, np.nan, 6],  # student 1 didn't report study hours (missing)
        "score": [70, 85, 90],
    }
)

print("\nBEFORE imputation:")
print(df)  # show the table with the NaN gap

imputer = KNNImputer(n_neighbors=2)  # use the 2 most similar rows to fill each gap

# fit_transform(): learns the distances from the data AND fills the gaps
# (returns a NumPy array, so we wrap it back into a DataFrame)
df_filled = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

print("\nAFTER imputation (study_hours filled with average of 2 neighbors):")
print(df_filled)


# =================================================================
# EXAMPLE 2 - Realistic workflow: scale -> impute -> model (Pipeline)
# =================================================================
print("\n" + "=" * 60)
print("EXAMPLE 2: Realistic workflow with scaling and a Pipeline")
print("=" * 60)

rng = np.random.RandomState(42)  # random seed so results repeat
n = 200  # number of rows

age = rng.normal(35, 10, n).round(1)  # age ~ normal(mean=35, std=10)
income = age * 900 + rng.normal(0, 5000, n)  # income depends on age
spend = income * 0.05 + rng.normal(0, 300, n)  # spending depends on income

df = pd.DataFrame({"age": age, "income": income, "spend": spend})

# Randomly hide 10% of the values in the FEATURE columns only.
# (The target column 'spend' must stay complete - models can't train on NaN targets.)
mask = rng.rand(n, 2) < 0.10  # boolean mask for age & income
df.loc[mask[:, 0], "age"] = np.nan  # hide some 'age' values
df.loc[mask[:, 1], "income"] = np.nan  # hide some 'income' values

print("\nMissing values per column after hiding 10% of the features:")
print(df.isna().sum())  # count NaNs in each column

X = df[["age", "income"]]  # features = age, income
y = df["spend"]  # target  = spend (no NaNs)

# Split BEFORE imputing so the test set never influences training
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Pipeline = scale first, then impute, then model.
# Scaling first is crucial: income (thousands) would otherwise dominate
# the distance calculation over age (tens).
pipe = Pipeline(
    [
        ("scaler", StandardScaler()),  # step 1: equalize feature scales
        ("imputer", KNNImputer(n_neighbors=5)),  # step 2: fill missing values
        ("model", LinearRegression()),  # step 3: train the model
    ]
)

pipe.fit(X_train, y_train)  # fit ALL steps on training data only
preds = pipe.predict(X_test)  # predict applies all steps automatically
rmse = mean_squared_error(y_test, preds) ** 0.5  # root mean squared error
print(f"\nTest RMSE with KNNImputer pipeline: {rmse:.2f}")


# =================================================================
# EXAMPLE 3 - Compare strategies: drop rows vs median vs KNN
# =================================================================
print("\n" + "=" * 60)
print("EXAMPLE 3: Comparing imputation strategies (5-fold CV)")
print("=" * 60)

# Recreate a clean dataset (same seed = same numbers as Example 2 setup)
rng = np.random.RandomState(42)
n = 200
df = pd.DataFrame({"age": rng.normal(35, 10, n).round(1)})
df["income"] = df["age"] * 900 + rng.normal(0, 5000, n)  # income correlated with age
df["spend"] = df["income"] * 0.05 + rng.normal(0, 300, n)

# Hide values only in the feature columns (age, income), keep target intact
mask = rng.rand(n, 2) < 0.10
df.loc[mask[:, 0], "age"] = np.nan  # hide some 'age' values
df.loc[mask[:, 1], "income"] = np.nan  # hide some 'income' values

X = df[["age", "income"]]  # feature matrix
y = df["spend"]  # target vector

strategies = {
    "Drop rows": "drop",  # baseline: delete incomplete rows
    "Median fill": SimpleImputer(strategy="median"),  # baseline: simple statistic
    "KNN (k=3)": KNNImputer(n_neighbors=3),  # our method
}

for name, imputer in strategies.items():
    if imputer == "drop":
        # For the drop baseline, remove rows with NaNs before cross-validation
        Xc, yc = X.dropna(), y[X.dropna().index]
        scores = cross_val_score(
            LinearRegression(),
            Xc,
            yc,
            cv=5,
            scoring="neg_root_mean_squared_error",  # negative RMSE (higher is better)
        )
    else:
        # Wrap imputer + model in a pipeline for fair comparison
        p = Pipeline(
            [
                ("scaler", StandardScaler()),
                ("imputer", imputer),
                ("model", LinearRegression()),
            ]
        )
        scores = cross_val_score(p, X, y, cv=5, scoring="neg_root_mean_squared_error")
    # scores are negative RMSE, so negate them back for reporting
    print(f"{name:15s} -> RMSE: {-scores.mean():.2f} (+/- {scores.std():.2f})")


# =================================================================
# EXAMPLE 4 - Tuning n_neighbors with GridSearchCV
# =================================================================
print("\n" + "=" * 60)
print("EXAMPLE 4: Tuning n_neighbors")
print("=" * 60)

pipe = Pipeline(
    [
        ("scaler", StandardScaler()),
        ("imputer", KNNImputer()),  # k left blank; GridSearchCV will set it
        ("model", LinearRegression()),
    ]
)

# 'imputer__n_neighbors' means: the parameter n_neighbors inside
# the pipeline step named 'imputer' (double underscore syntax)
grid = GridSearchCV(
    pipe,
    param_grid={"imputer__n_neighbors": [2, 3, 5, 7, 10, 15]},
    cv=5,  # 5-fold cross-validation
    scoring="neg_root_mean_squared_error",
)
grid.fit(X, y)  # search all k values

print("Best n_neighbors:", grid.best_params_["imputer__n_neighbors"])
print(f"Best cross-validated RMSE: {-grid.best_score_:.2f}")

print("\nDone! KNNImputer: fill gaps using the most similar rows.")
