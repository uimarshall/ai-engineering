"""
====================================================================
Introduction to Machine Learning for Regression - runnable examples
====================================================================
Each section is self-contained. Run the whole file, or copy a section
into an interactive session.

Requirements:
    pip install numpy pandas matplotlib scikit-learn

Note: Example 2 downloads the California Housing dataset from the
internet the first time it runs. If you are offline, it will fail;
Examples 1 and 3 will still work.
"""

import matplotlib.pyplot as plt  # plotting library
from typing import cast

# ======================================================================
# Imports shared by the examples
# ======================================================================
import numpy as np  # numerical computing library
import pandas as pd  # data tables / dataframes
from sklearn.ensemble import RandomForestRegressor  # powerful tree-based model
from sklearn.linear_model import LinearRegression  # simple regression model
from sklearn.metrics import mean_absolute_error  # average size of errors
from sklearn.metrics import mean_squared_error  # squared errors (punishes big ones)
from sklearn.metrics import r2_score  # 1.0 = perfect, 0 = no skill
from sklearn.model_selection import train_test_split  # split data into train/test
from sklearn.preprocessing import StandardScaler  # scale features to mean 0, std 1
from sklearn.utils import Bunch

# ======================================================================
# Example 1: Simple Linear Regression on a synthetic dataset
# (Hours studied -> Exam score)
# ======================================================================
print("=" * 60)
print("EXAMPLE 1: Simple Linear Regression")
print("=" * 60)

# 1. Create a simple synthetic dataset: hours studied vs exam score
np.random.seed(42)                                       # make random numbers reproducible
hours = np.random.rand(100, 1) * 10                      # 100 random study hours (0-10)
scores = (50 + 5 * hours + np.random.randn(100, 1) * 5).ravel()  # true pattern + noise

# 2. Split the data: 80% for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(
    hours, scores, test_size=0.2, random_state=42
)

# 3. Choose the model and train it
model = LinearRegression()      # create a linear regression model
model.fit(X_train, y_train)     # "fit" = learn the best line from the training data

# 4. Evaluate on the test set (data the model has never seen)
y_pred = model.predict(X_test)                      # predict scores for test data
mae = mean_absolute_error(y_test, y_pred)           # average error, in exam points
r2 = r2_score(y_test, y_pred)                       # how well the line explains the data

# model.coef_ = learned slope (w), model.intercept_ = learned offset (b)
print(f"Learned formula: score = {model.coef_[0]:.2f} * hours + {model.intercept_:.2f}")
print(f"MAE: {mae:.2f} points    R2: {r2:.3f}")

# 5. Visualize: training data, test data, and the learned line
plt.figure(figsize=(7, 5))
plt.scatter(X_train, y_train, color="blue", label="Training data")   # data the model saw
plt.scatter(X_test, y_test, color="green", label="Test data")        # unseen data
plt.plot(X_test, y_pred, color="red", linewidth=2, label="Learned line")  # the model
plt.xlabel("Hours studied")
plt.ylabel("Exam score")
plt.legend()
plt.title("Linear Regression: Hours vs Score")
plt.savefig("example1_simple_linear.png", dpi=100)   # save figure to a file
plt.show()


# ======================================================================
# Example 2: Real dataset - California Housing Prices (8 features)
# ======================================================================
print()
print("=" * 60)
print("EXAMPLE 2: California Housing Prices")
print("=" * 60)

# This downloads the dataset on first run (needs internet)
from sklearn.datasets import fetch_california_housing

# 1. Load the dataset
housing = cast(
    Bunch, fetch_california_housing(as_frame=True, return_X_y=False)
)
X = housing.data                    # the 8 input features (income, rooms, age, ...)
y = housing.target * 100_000        # the target: median house value, scaled to dollars

print("Feature names:", list(X.columns))
print("Dataset size (rows, columns):", X.shape)

# 2. Quick exploration: summary statistics of every feature
print(X.describe())

# 3. Split into train (80%) and test (20%) sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Scale features (mean=0, std=1) - important for linear models and k-NN
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # learn scaling FROM TRAIN data only
X_test_scaled = scaler.transform(X_test)        # apply the SAME scaling to test data

# 5. Train a Linear Regression model (our baseline)
lr = LinearRegression()
lr.fit(X_train_scaled, y_train)                 # train on scaled training data
lr_pred = lr.predict(X_test_scaled)             # predict on scaled test data

print("\n--- Linear Regression ---")
print(f"MAE:  ${mean_absolute_error(y_test, lr_pred):,.0f}")              # avg error in dollars
print(f"RMSE: ${mean_squared_error(y_test, lr_pred) ** 0.5:,.0f}")        # punishes big errors
print(f"R2:   {r2_score(y_test, lr_pred):.3f}")                           # closer to 1 = better

# 6. Train a Random Forest (usually more accurate; handles non-linear patterns)
rf = RandomForestRegressor(n_estimators=100,     # build 100 decision trees
                           random_state=42,      # reproducible results
                           n_jobs=-1)            # use all CPU cores for speed
rf.fit(X_train, y_train)                         # trees do NOT need scaled data
rf_pred = rf.predict(X_test)

print("\n--- Random Forest ---")
print(f"MAE:  ${mean_absolute_error(y_test, rf_pred):,.0f}")
print(f"RMSE: ${mean_squared_error(y_test, rf_pred) ** 0.5:,.0f}")
print(f"R2:   {r2_score(y_test, rf_pred):.3f}")

# 7. Which features matter most? (Random Forest feature importances)
importances = pd.Series(rf.feature_importances_, index=X.columns)
importances.sort_values().plot(kind="barh", figsize=(7, 5),
                               title="Feature Importance (Random Forest)")
plt.tight_layout()
plt.savefig("example2_feature_importance.png", dpi=100)
plt.show()

# 8. Predicted vs Actual plot: points on the red dashed line = perfect prediction
plt.figure(figsize=(6, 6))
plt.scatter(y_test, rf_pred, alpha=0.3)          # alpha makes dense areas darker
plt.plot([y_test.min(), y_test.max()],           # diagonal "perfect prediction" line
         [y_test.min(), y_test.max()], "r--")
plt.xlabel("Actual price ($)")
plt.ylabel("Predicted price ($)")
plt.title("Random Forest: Predicted vs Actual")
plt.savefig("example2_pred_vs_actual.png", dpi=100)
plt.show()

# ======================================================================
# Example 3: Making a prediction on new data
# ======================================================================
print()
print("=" * 60)
print("EXAMPLE 3: Predicting on new districts")
print("=" * 60)

# Grab the first 5 districts from the test set
sample = X_test.head(5)                  # 5 rows of feature values
predicted = rf.predict(sample)           # ask the trained model for predictions

# Compare each prediction with the true price
for i, (idx, row) in enumerate(sample.iterrows()):
    actual = y_test.loc[idx]             # the true price for this district
    print(f"District {i+1}: predicted ${predicted[i]:,.0f} | actual ${actual:,.0f}")

print("\n--- Done! Check the saved PNG plots in this folder. ---")