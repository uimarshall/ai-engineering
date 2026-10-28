"""
Random Forest for Regression — Practical Beginner Tutorial
==========================================================

This script accompanies the tutorial note "random_forest_regression_tutorial.md".

What it does:
  1. Loads a real dataset (California Housing — predicting median house values)
  2. Explores the data briefly
  3. Splits into train/test sets
  4. Trains a RandomForestRegressor
  5. Evaluates it with MAE, MSE, RMSE, and R²
  6. Shows sample predictions vs actual values
  7. Tunes max_depth to show the bias/variance trade-off
  8. Plots feature importances and prediction scatter plots

Run with:  python random_forest_regression.py
Requires:  scikit-learn, matplotlib (install with: pip install scikit-learn matplotlib)
"""

# ---------- STEP 0: Imports ----------
# sklearn.datasets  -> gives us ready-made real datasets to practice with
# sklearn.model_selection -> tools to split data and tune hyperparameters
# sklearn.ensemble    -> the RandomForestRegressor lives here
# sklearn.metrics     -> functions to measure how good our predictions are
# matplotlib.pyplot   -> for making plots
import matplotlib

matplotlib.use("Agg")  # use a non-interactive backend so plots save to files
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.utils import Bunch

# ---------- STEP 1: Load the dataset ----------
# fetch_california_housing downloads a real dataset with 20,640 California
# census districts. Each row = one district, target = median house value
# (in units of $100,000, e.g. 2.0 means $200,000).
housing = cast(Bunch, fetch_california_housing(as_frame=True))

X = housing.data  # X = the INPUT features (size, age, location, etc.)
y = housing.target  # y = the TARGET we want to predict (median house value)

print("=== California Housing Dataset ===")
print("Dataset shape:", X.shape)  # (20640, 8) -> 20640 rows, 8 features
print("Features:", list(X.columns))
print("Target: median house value (in $100,000s)\n")


# ---------- STEP 2: Split into training and testing sets ----------
# We train on 70% of the data and test on the remaining 30% which the model
# has NEVER seen. This tells us how the model performs on new, unseen data.
# random_state=42 fixes the random split so results are reproducible.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42
)

print(f"Training samples: {X_train.shape[0]}")
print(f"Testing samples:  {X_test.shape[0]}\n")


# ---------- STEP 3: Create and train the Random Forest ----------
# n_estimators=100  -> build 100 decision trees
# random_state=42   -> reproducible results
# n_jobs=-1         -> use all CPU cores to train trees in parallel (faster)
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)

print("Training the random forest (this may take ~30-60 seconds)...")
model.fit(X_train, y_train)  # fit() = "learn" from the training data
print("Done!\n")


# ---------- STEP 4: Make predictions on the test set ----------
# predict() applies every tree to each test row and averages the results.
y_pred = model.predict(X_test)

# The final prediction for a row is literally the average of all 100 trees:
# y_pred[i] = mean(tree1_pred, tree2_pred, ..., tree100_pred)


# ---------- STEP 5: Evaluate the model ----------
# MAE  = average |prediction - actual|  -> "on average, how far off are we?"
# MSE  = average squared error          -> punishes big mistakes more
# RMSE = sqrt(MSE)                      -> same units as the target ($100k)
# R²   = fraction of variance explained -> 1.0 = perfect, 0 = no skill
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("--- Model performance on unseen test data ---")
print(f"MAE  = {mae:.3f}  (average error ~ ${mae*100000:,.0f})")
print(f"MSE  = {mse:.3f}")
print(f"RMSE = {rmse:.3f}  (~ ${rmse*100000:,.0f} for larger errors)")
print(f"R²   = {r2:.3f}  (explains {r2*100:.1f}% of the variance)\n")


# ---------- STEP 6: Look at some individual predictions ----------
# Convert back to dollars by multiplying by 100,000 for readability.
print("Sample predictions vs actual (in $100k):")
for i in range(5):
    print(f"  Predicted: ${y_pred[i]:.2f},  Actual: ${y_test.iloc[i]:.2f}")


# ---------- STEP 7: Tune max_depth (bias vs variance trade-off) ----------
# Full-depth trees can memorize noise (overfitting). Shallower trees are
# simpler but may underfit. We test several depths and compare R².
print("\n--- Tuning max_depth ---")
for depth in [None, 5, 10, 20]:
    m = RandomForestRegressor(
        n_estimators=100, max_depth=depth, random_state=42, n_jobs=-1
    )
    m.fit(X_train, y_train)
    score = m.score(X_test, y_test)  # R² score
    label = "full trees" if depth is None else f"depth={depth}"
    print(f"max_depth={label:<12} -> R² = {score:.4f}")


# ---------- STEP 8: Feature importances ----------
# The model tells us which input features mattered most when making splits.
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]  # sort from most to least important

print("\n--- Feature importances (most to least important) ---")
for idx in indices:
    print(f"  {X.columns[idx]:<12}: {importances[idx]*100:.1f}%")

# Plot the feature importances as a horizontal bar chart
plt.figure(figsize=(8, 5))
plt.barh(
    [X.columns[i] for i in indices][::-1],
    importances[indices][::-1],
    color="forestgreen",
)
plt.xlabel("Importance")
plt.title("Random Forest Feature Importances")
plt.tight_layout()
plt.savefig("/mnt/agents/output/feature_importances.png", dpi=120)
print("\nSaved plot: feature_importances.png")


# ---------- STEP 9: Prediction quality plot ----------
# A "perfect" model would place all points exactly on the diagonal line.
plt.figure(figsize=(6, 6))
plt.scatter(y_test, y_pred, s=3, alpha=0.3, color="steelblue")
plt.plot([0, 5], [0, 5], "r--", linewidth=1, label="perfect predictions")
plt.xlabel("Actual value ($100k)")
plt.ylabel("Predicted value ($100k)")
plt.title("Predicted vs Actual House Values")
plt.legend()
plt.tight_layout()
plt.savefig("/mnt/agents/output/predicted_vs_actual.png", dpi=120)
print("Saved plot: predicted_vs_actual.png")


# ---------- STEP 10: Predicting brand-new houses ----------
# Use the trained model on rows it has never seen (we take 3 rows from X).
new_houses = X.iloc[[0, 100, 500]]
predictions = model.predict(new_houses)
print("\n--- Predicting new (unseen) districts ---")
for i, (_, row) in enumerate(new_houses.iterrows()):
    print(f"  Predicted median value: ${predictions[i]*100000:,.0f}")
    print(
        f"    (features: MedInc={row['MedInc']}, HouseAge={row['HouseAge']}, "
        f"AveRooms={row['AveRooms']:.2f})\n"
    )

print("All done! Check the saved PNG plots in the output folder.")
