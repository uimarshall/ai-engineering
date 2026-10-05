"""
outliers_tutorial.py
====================
Practical tutorial: detecting and handling outliers for Machine Learning.
Every line is commented for beginners. Run with:  python outliers_tutorial.py
"""

import matplotlib.pyplot as plt  # matplotlib: plotting library
import numpy as np  # numpy: fast numerical arrays / math functions
import pandas as pd  # pandas: dataframes, the main tool for tabular data
from sklearn.ensemble import (  # IsolationForest: ML model that finds multivariate outliers
    IsolationForest,
)

np.random.seed(42)  # fix the random generator so results are reproducible

# -----------------------------------------------------------------------------
# SECTION 1 — Visual inspection (ALWAYS your first step)
# -----------------------------------------------------------------------------
print("=" * 60)
print("SECTION 1: Visual inspection")
print("=" * 60)

# Build a demo dataset: 100 house sizes (roughly normal around 2000 sq ft)
sizes = np.random.normal(loc=2000, scale=300, size=100)
# Inject 3 outliers: two huge houses and one impossibly small one
sizes = np.append(sizes, [12000, 15000, 50])

# Put the data into a pandas DataFrame (a table with named columns)
df = pd.DataFrame({"house_size_sqft": sizes})

# A boxplot draws a box around the middle 50% of the data; dots outside the
# "whiskers" are outliers. You can see them instantly.
df.boxplot(column="house_size_sqft")
plt.title("Boxplot reveals outliers instantly")
plt.savefig("section1_boxplot.png")  # save the figure instead of showing it
plt.close()  # close the figure to free memory

# A histogram shows the distribution shape; extreme values sit far to the side
df["house_size_sqft"].hist(bins=30)
plt.title("Histogram also shows the extreme values")
plt.savefig("section1_histogram.png")
plt.close()
print("Saved plots: section1_boxplot.png, section1_histogram.png")

# -----------------------------------------------------------------------------
# SECTION 2 — IQR method (recommended default detector)
# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("SECTION 2: IQR method")
print("=" * 60)


def iqr_outlier_bounds(series: pd.Series, k: float = 1.5):
    """Return (lower, upper) bounds. Values outside them are IQR outliers."""
    q1 = series.quantile(0.25)  # first quartile = 25th percentile of the data
    q3 = series.quantile(0.75)  # third quartile = 75th percentile of the data
    iqr = q3 - q1  # interquartile range: width of the middle 50%
    lower = q1 - k * iqr  # lower fence (default 1.5x IQR below Q1)
    upper = q3 + k * iqr  # upper fence (default 1.5x IQR above Q3)
    return lower, upper  # anything outside [lower, upper] is flagged


# Apply the function to our house-size column
lower, upper = iqr_outlier_bounds(df["house_size_sqft"])
print(f"Valid range: [{lower:.0f}, {upper:.0f}]")  # show the allowed range

# Build a boolean mask: True where the value is BELOW lower OR ABOVE upper
outlier_mask = (df["house_size_sqft"] < lower) | (df["house_size_sqft"] > upper)
# Use the mask to select and print only the outlier rows
outliers = df[outlier_mask]
print(f"Found {len(outliers)} outliers out of {len(df)} rows")
print(outliers)

# -----------------------------------------------------------------------------
# SECTION 3 — Z-score method (only for roughly normal data!)
# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("SECTION 3: Z-score method")
print("=" * 60)


def zscore_outliers(series: pd.Series, threshold: float = 3.0):
    """Return a boolean mask: True where |z-score| > threshold (default 3)."""
    mean = series.mean()  # average of the column
    std = series.std()  # standard deviation (spread of the column)
    z = (series - mean) / std  # z-score: how many std-devs each value is from the mean
    return z.abs() > threshold  # flag values more than `threshold` std-devs away


z_mask = zscore_outliers(df["house_size_sqft"])  # run it on our column
print(f"Z-score found {z_mask.sum()} outliers")  # .sum() counts True values in the mask

# -----------------------------------------------------------------------------
# SECTION 4 — Percentile method (simplest)
# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("SECTION 4: Percentile method")
print("=" * 60)

low, high = df["house_size_sqft"].quantile([0.01, 0.99])  # 1st and 99th percentiles
p_mask = (df["house_size_sqft"] < low) | (df["house_size_sqft"] > high)
print(f"Percentile method found {p_mask.sum()} outliers")

# -----------------------------------------------------------------------------
# SECTION 5 — Multivariate outliers with Isolation Forest
# (a row can look normal in every column yet still be weird overall)
# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("SECTION 5: Isolation Forest (multivariate)")
print("=" * 60)

rng = np.random.default_rng(0)  # a second random generator for this section
n = 300  # number of normal rows to create
sqft = rng.normal(2000, 300, n)  # house sizes, normally distributed
bedrooms = sqft / 500 + rng.normal(
    0, 0.4, n
)  # bedrooms correlate with size (bigger house -> more bedrooms)
df2 = pd.DataFrame({"sqft": sqft, "bedrooms": bedrooms})  # combine into a dataframe

# Inject 5 weird rows: enormous houses with only 1-3 bedrooms (unrealistic combo)
weird = pd.DataFrame(
    {"sqft": [9000, 9500, 10000, 8500, 12000], "bedrooms": [1, 1, 2, 1, 3]}
)
df2 = pd.concat(
    [df2, weird], ignore_index=True
)  # stack the weird rows under the normal ones

# IsolationForest randomly splits features; outliers need few splits to isolate,
# so it scores them as "anomalous". contamination = expected fraction of outliers.
iso = IsolationForest(contamination=0.02, random_state=42)
df2["is_outlier"] = iso.fit_predict(
    df2[["sqft", "bedrooms"]]
)  # +1 = normal, -1 = outlier
print(df2[df2["is_outlier"] == -1])  # show only the rows flagged as outliers

# -----------------------------------------------------------------------------
# SECTION 6 — Handling outliers: four options
# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("SECTION 6: Handling outliers")
print("=" * 60)

# Option A: CORRECT the value (best case — it was a data-entry error).
# E.g. a "50 sq ft" house was probably measured in different units or mistyped.
df.loc[df["house_size_sqft"] < 500, "house_size_sqft"] = 500
print("Option A: corrected impossibly small house size to 500")


# Option B: DROP the outlier rows (fine when there are very few of them).
def drop_iqr_outliers(dataframe: pd.DataFrame, column: str):
    """Return a copy of the dataframe with IQR outliers in `column` removed."""
    lower, upper = iqr_outlier_bounds(dataframe[column])  # compute the fences
    # Keep only rows inside the fences (>= lower AND <= upper)
    kept = dataframe[(dataframe[column] >= lower) & (dataframe[column] <= upper)]
    return kept  # return the cleaned copy


df_clean = drop_iqr_outliers(
    df, "house_size_sqft"
)  # drop outliers from house_size_sqft
print(f"Option B: before = {len(df)} rows, after = {len(df_clean)} rows")


# Option C: CAP the values (Winsorization) — usually the best default.
# Instead of deleting rows, replace extreme values with the fence values.
def cap_iqr_outliers(dataframe: pd.DataFrame, column: str):
    """Cap values to the IQR fences. Returns a modified copy of the dataframe."""
    lower, upper = iqr_outlier_bounds(dataframe[column])  # compute the fences
    result = dataframe.copy()  # work on a copy, don't touch original
    # clip() swaps any value below `lower` -> `lower`, and above `upper` -> `upper`
    result[column] = result[column].clip(lower=float(lower), upper=float(upper))
    return result


df_capped = cap_iqr_outliers(df, "house_size_sqft")
print("Option C: summary after capping:")
print(df_capped["house_size_sqft"].describe())  # describe() shows min/max/mean etc.

# Option D: TRANSFORM with log — great for skewed data (income, prices).
# log1p = log(1 + x); the "+1" makes log(0) safe (log(0) is undefined).
df["house_size_log"] = np.log1p(df["house_size_sqft"])
print("Option D: added log-transformed column 'house_size_log'")

# -----------------------------------------------------------------------------
# SECTION 7 — Complete mini-pipeline (bring it all together)
# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("SECTION 7: Complete mini-pipeline")
print("=" * 60)

np.random.seed(42)  # reset the seed for reproducibility

# 1) Create a messy dataset (in real life use: pd.read_csv("your_data.csv"))
n = 500  # 500 normal rows
data = pd.DataFrame(
    {
        "income": np.random.lognormal(
            mean=10, sigma=0.5, size=n
        ),  # lognormal = right-skewed like real income
        "age": np.random.randint(18, 70, size=n),  # random ages 18-69
        "house_age": np.random.exponential(
            scale=20, size=n
        ),  # exponential = many young, few old houses
    }
)
data.loc[10, "age"] = 250  # inject a typo outlier (age 250)
data.loc[20, "income"] = 9_999_999  # inject an extreme-but-real income
# inject two near-zero house ages (suspicious records)
data = pd.concat(
    [
        data,
        pd.DataFrame({"income": [2e6, 3e6], "age": [45, 52], "house_age": [0.2, 0.1]}),
    ],
    ignore_index=True,
)


# 2) Report outliers in every numeric column using IQR
def report_outliers(dataframe: pd.DataFrame):
    """Print the IQR valid range and outlier count for each numeric column."""
    numeric_cols = dataframe.select_dtypes(
        include="number"
    ).columns  # get numeric columns only
    for col in numeric_cols:  # loop over them
        lower, upper = iqr_outlier_bounds(dataframe[col])  # compute fences
        count = (
            (dataframe[col] < lower) | (dataframe[col] > upper)
        ).sum()  # count flags
        print(
            f"{col:10s} -> valid range [{lower:>12,.1f}, {upper:>12,.1f}]  | {count} outliers"
        )


print("Before cleaning:")
report_outliers(data)

# 3) Handle each column with the RIGHT tool for its situation:
data["age"] = data["age"].clip(upper=100)  # age typo -> cap at realistic max (100)
data["income_log"] = np.log1p(data["income"])  # income is skewed -> log transform
data["house_age"] = data["house_age"].clip(
    lower=0.5
)  # near-zero ages -> cap at a small floor

print("\nAfter cleaning:")
report_outliers(
    data[["age", "income_log", "house_age"]]
)  # re-check the cleaned columns

print("\nDone! Check the saved plots to see the outliers visually.")
