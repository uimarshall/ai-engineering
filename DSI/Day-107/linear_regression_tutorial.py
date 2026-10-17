"""
========================================================================
LINEAR REGRESSION — PRACTICAL TUTORIAL SCRIPT
========================================================================
.\DSI\.venv\Scripts\python.exe .\DSI\Day-107\linear_regression_tutorial.py
A beginner-friendly, fully-commented walkthrough of Linear Regression.

Run with:   python linear_regression_tutorial.py
Requires:   numpy, pandas, matplotlib, scikit-learn

Contents:
  Example 1: Simple linear regression (one feature) + plot
  Example 2: Multiple linear regression (three features)
  Example 3: Loading data from a CSV file
  Example 4: Linear regression "from scratch" (pure NumPy)
  Example 5: Full evaluation (MAE, MSE, RMSE, R^2) with train/test split
========================================================================
"""

import matplotlib  # matplotlib: for plotting charts

# ------------------------------------------------------------------------
# Imports — the tools we need for this tutorial
# ------------------------------------------------------------------------
import numpy as np  # numpy: fast numerical computing with arrays
import pandas as pd  # pandas: loading and working with tables (CSV files)

matplotlib.use("Agg")  # "Agg" backend = save charts to files instead of
# opening windows (important on servers/headless machines)
import matplotlib.pyplot as plt  # pyplot: the main plotting interface
from sklearn.linear_model import LinearRegression  # the linear regression model itself
from sklearn.metrics import mean_absolute_error  # MAE evaluation metric
from sklearn.metrics import mean_squared_error  # MSE evaluation metric
from sklearn.metrics import r2_score  # R^2 evaluation metric
from sklearn.model_selection import (  # helper to split data into train/test
    train_test_split,
)

# Make printed numbers easier to read
np.set_printoptions(suppress=True)  # suppress=True avoids scientific notation (1e+05)
plt.rcParams["figure.dpi"] = 100  # slightly sharper plots


# ========================================================================
# EXAMPLE 1 — Simple Linear Regression (ONE feature)
# Scenario: predict house price from house size
# ========================================================================
print("=" * 60)
print("EXAMPLE 1: House Price vs. Size (simple regression)")
print("=" * 60)

# --- Step 1: Prepare the data -------------------------------------------
# X = input feature (house size in m2). Must be 2D: (n_samples, n_features)
X = np.array([[50], [80], [100], [120], [150], [180], [200], [220]])

# y = target values (house price in $ thousands). Shape: (n_samples,)
y = np.array([120, 180, 230, 280, 340, 410, 460, 510])

# --- Step 2: Create the model and TRAIN it -------------------------------
model = LinearRegression()  # create an (empty) linear regression model
model.fit(X, y)  # "fit" = training: finds the best m (slope) and b (intercept)

# --- Step 3: Inspect what the model learned ------------------------------
print(
    "Slope (m):      ", model.coef_[0]
)  # coef_ = learned slope(s). [0] because one feature.
print("Intercept (b):  ", model.intercept_)  # intercept_ = the learned b value
print(
    "Meaning: each extra m2 adds ~$%.0fk; base price ~$%.0fk"
    % (model.coef_[0], model.intercept_)
)

# --- Step 4: Make a PREDICTION -------------------------------------------
new_house = np.array([[120]])  # a new house we want to price: 120 m2
predicted_price = model.predict(new_house)  # predict() applies y = m*x + b for us
print("Predicted price for a 120 m2 house: $%.1fk" % predicted_price[0])

# --- Step 5: Evaluate on training data (R^2: 1.0 = perfect fit) ----------
r2_train = model.score(X, y)  # score() returns the R^2 coefficient of determination
print("R^2 score on training data: %.4f" % r2_train)

# --- Step 6: VISUALIZE the fit -------------------------------------------
plt.figure(figsize=(8, 5))  # create a new figure 8x5 inches
plt.scatter(
    X, y, color="blue", label="Actual data", s=60
)  # plot raw data points as blue dots
plt.plot(
    X, model.predict(X), color="red", linewidth=2, label="Best-fit line (model)"
)  # plot the model's line in red
plt.scatter(
    new_house,
    predicted_price,
    color="green",
    marker="*",
    s=250,
    label="Our prediction (120 m2)",
)  # show the prediction as a green star
plt.title("Example 1: House Price vs. Size")  # chart title
plt.xlabel("House size (m2)")  # x-axis label
plt.ylabel("Price ($ thousands)")  # y-axis label
plt.legend()  # show the legend
plt.grid(alpha=0.3)  # light grid for readability
plt.tight_layout()  # tidy up spacing
plt.savefig("example1_house_prices.png")  # save chart to a PNG file
plt.close()  # close figure to free memory
print("Chart saved -> example1_house_prices.png")


# ========================================================================
# EXAMPLE 2 — Multiple Linear Regression (SEVERAL features)
# Scenario: price depends on size, bedrooms AND age at the same time
# ========================================================================
print()
print("=" * 60)
print("EXAMPLE 2: Multiple regression (size + bedrooms + age)")
print("=" * 60)

# Each row is one house; columns are [size_m2, bedrooms, age_years]
X_multi = np.array(
    [
        [50, 1, 30],
        [80, 2, 20],
        [100, 2, 15],
        [120, 3, 10],
        [150, 3, 8],
        [180, 4, 5],
        [200, 4, 3],
        [220, 5, 1],
    ]
)
y_multi = np.array([120, 180, 230, 280, 340, 410, 460, 510])

# Split: 75% of data for training, 25% for testing.
# random_state=42 makes the split identical every run (reproducibility).
X_train, X_test, y_train, y_test = train_test_split(
    X_multi, y_multi, test_size=0.25, random_state=42
)

model_multi = LinearRegression()  # a fresh model
model_multi.fit(X_train, y_train)  # train ONLY on the training portion

print("Learned weights (m per feature):", model_multi.coef_)
print("  -> size:     +$%.1fk per m2" % model_multi.coef_[0])
print("  -> bedrooms: +$%.1fk each" % model_multi.coef_[1])
print(
    "  -> age:      $%.1fk per year (negative = older houses cheaper)"
    % model_multi.coef_[2]
)
print("Intercept (b):", model_multi.intercept_)

# Evaluate on the UNSEEN test set — the honest measure of performance
test_score = model_multi.score(X_test, y_test)
print("R^2 on test set: %.4f" % test_score)


# ========================================================================
# EXAMPLE 3 — Loading data from a CSV file
# Scenario: predict salary from years of experience (real-world workflow)
# ========================================================================
print()
print("=" * 60)
print("EXAMPLE 3: Salary vs. Experience (CSV data)")
print("=" * 60)

# First, create a small CSV file so this script runs standalone.
# In real life you would already have a file like this.
rows = 40  # number of data points to generate
rng = np.random.default_rng(seed=7)  # seeded random generator (reproducible)
years = np.linspace(0, 15, rows, retstep=False)  # experience from 0 to 15 years
noise = rng.normal(0, 8, rows)  # realistic noise (+/- around the line)
salaries = 30 + 4 * years + noise  # true pattern: $30k base + $4k/year + noise

df = pd.DataFrame(
    {  # build a table (DataFrame)
        "years_experience": years,  # column 1: feature
        "salary": salaries,  # column 2: target
    }
)
df.to_csv("salaries.csv", index=False)  # save the table as salaries.csv
print("Created salaries.csv with", len(df), "rows")

# --- Now load it back the way you would with real data --------------------
df = pd.read_csv("salaries.csv")  # load CSV into a pandas DataFrame
print(df.head(3))  # preview the first 3 rows

X_sal = df[["years_experience"]]  # feature: use DOUBLE brackets -> stays 2D
y_sal = df["salary"]  # target: single brackets -> 1D is fine here

salary_model = LinearRegression()
salary_model.fit(X_sal.to_numpy(), y_sal.to_numpy())  # train with NumPy arrays

print(
    "Learned: salary = %.2f + %.2f x years"
    % (salary_model.intercept_, salary_model.coef_[0])
)
salary_pred = salary_model.predict(np.array([[7]]))  # predict for 7 years of experience
print("Predicted salary at 7 years experience: $%.2fk" % salary_pred[0])

# Plot data + fitted line
plt.figure(figsize=(8, 5))
plt.scatter(X_sal, y_sal, color="teal", alpha=0.7, label="Employees (data)")
plt.plot(
    X_sal,
    salary_model.predict(X_sal.values),
    color="orange",
    linewidth=2,
    label="Best-fit line",
)
plt.title("Example 3: Salary vs. Years of Experience")
plt.xlabel("Years of experience")
plt.ylabel("Salary ($ thousands)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("example3_salaries.png")
plt.close()
print("Chart saved -> example3_salaries.png")


# ========================================================================
# EXAMPLE 4 — Under the hood: Linear Regression from scratch (pure NumPy)
# Uses the Normal Equation:  w = (X^T X)^-1 X^T y
# ========================================================================
print()
print("=" * 60)
print("EXAMPLE 4: From scratch with the Normal Equation")
print("=" * 60)

X_scratch = X.copy()  # reuse the house-size data from Example 1
y_scratch = y.copy().reshape(-1, 1)  # reshape y to a column vector (n,1)

ones_column = np.ones((X_scratch.shape[0], 1))  # a column of 1s, one per data point
X_b = np.hstack([ones_column, X_scratch])  # add it so the intercept b is learned too
# X_b now looks like: [1, size] per row

# Normal Equation — the exact, closed-form solution (no iterations needed)
XtX = X_b.T @ X_b  # X^T multiplied by X      (matrix product)
XtX_inv = np.linalg.inv(XtX)  # inverse of that matrix
XtY = X_b.T @ y_scratch  # X^T multiplied by y
w = XtX_inv @ XtY  # w = (X^T X)^-1 X^T y  -> best weights

b_scratch = w[0][0]  # first weight = intercept (b)
m_scratch = w[1][0]  # second weight = slope (m)
print("From scratch -> intercept b: %.3f, slope m: %.3f" % (b_scratch, m_scratch))
print(
    "sklearn      -> intercept b: %.3f, slope m: %.3f"
    % (model.intercept_, model.coef_[0])
)
print("(Both approaches give the same answer.)")

manual_pred = m_scratch * 120 + b_scratch  # hand-computed prediction for 120 m2
print("Manual prediction for 120 m2: $%.1fk" % manual_pred)


# ========================================================================
# EXAMPLE 5 — Full evaluation: MAE, MSE, RMSE, R^2
# ========================================================================
print()
print("=" * 60)
print("EXAMPLE 5: Proper evaluation with a test set")
print("=" * 60)

X_train5, X_test5, y_train5, y_test5 = train_test_split(
    X_multi, y_multi, test_size=0.25, random_state=42
)  # same split as Example 2

eval_model = LinearRegression()
eval_model.fit(X_train5, y_train5)  # train on train set only

y_pred5 = eval_model.predict(X_test5)  # predictions for the unseen test set

mae = mean_absolute_error(y_test5, y_pred5)  # average absolute miss (in $k)
mse = mean_squared_error(y_test5, y_pred5)  # average squared miss (punishes big errors)
rmse = np.sqrt(mse)  # root MSE: back in original units ($k)
r2 = r2_score(y_test5, y_pred5)  # R^2: share of variance explained

print("Test set predictions:", np.round(y_pred5, 1))
print("Actual test values:  ", y_test5)
print("MAE : %.2f  (avg miss, in $k)" % mae)
print("MSE : %.2f" % mse)
print("RMSE: %.2f  (typical miss, in $k)" % rmse)
print("R^2 : %.4f" % r2)

print()
print("All examples finished successfully!")
