"""
=====================================================================
 Dealing with Outliers — Practical Examples for ML Data Preparation
=====================================================================
This script is fully self-contained: it generates its own sample data,
so you can run it as-is without downloading anything.

Run with:  python outliers_practical.py
Sections:
    0. Setup & sample data
    1. Visual detection (boxplot / histogram / scatter)
    2. IQR detection method
    3. Z-score detection method
    4. Isolation Forest (multivariate detection)
    5. Fixing: deletion
    6. Fixing: capping (Winsorization)
    7. Fixing: log transformation
    8. Fixing: imputation with median
    9. Fixing: flagging
   10. End-to-end pipeline + model comparison (no data leakage)
=====================================================================
"""

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")  # use a non-interactive backend so plots save to files
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PowerTransformer, StandardScaler

sns.set_theme(style="whitegrid")  # nicer-looking plots
rng = np.random.default_rng(42)  # reproducible random numbers


# ----------------------------------------------------------------------
# 0. SETUP — create sample data WITH known outliers
# ----------------------------------------------------------------------
# np.random.normal draws from a bell curve: loc = centre, scale = spread, size = count
ages = rng.normal(loc=35, scale=8, size=200).round(1)  # 200 realistic ages
ages = np.append(ages, [150, 3, 220, -10])  # inject obvious outliers
df = pd.DataFrame({"age": ages})  # put the column in a DataFrame

income_vals = rng.normal(loc=50000, scale=12000, size=200)  # realistic incomes
income_vals = np.append(
    income_vals, [10_000_000, -5000, 999_999, 8]
)  # 4 outliers, same count as ages
df["income"] = income_vals

print("=" * 60)
print("SECTION 0 — Raw data (head)")
print("=" * 60)
print(df.head())


# ----------------------------------------------------------------------
# 1. VISUAL DETECTION — always look at your data first!
# ----------------------------------------------------------------------
# A boxplot draws the box (middle 50% of data), the median line, whiskers,
# and plots every value beyond the whiskers as an individual dot.
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)  # first of two side-by-side plots
sns.boxplot(x=df["age"])  # boxplot of the age column
plt.title("Boxplot of age (dots = outliers)")

plt.subplot(1, 2, 2)  # second plot
sns.histplot(data=df, x="age", bins=30, kde=True)  # histogram + smooth density curve
plt.title("Histogram of age")

plt.tight_layout()  # avoid overlapping labels
plt.savefig("section1_visuals.png", dpi=100)  # save figure to a file
plt.close()  # free memory
print("\n[Saved] section1_visuals.png  — open it to see the outliers visually")


# ----------------------------------------------------------------------
# 2. IQR METHOD — the most common outlier rule
# ----------------------------------------------------------------------
def detect_outliers_iqr(data, column, factor=1.5):
    """Return rows of `data` where `column` is outside the IQR fences."""
    q1 = data[column].quantile(0.25)  # 25th percentile (bottom of box)
    q3 = data[column].quantile(0.75)  # 75th percentile (top of box)
    iqr = q3 - q1  # interquartile range = box height
    lower = q1 - factor * iqr  # lower fence (factor=1.5 is Tukey's rule)
    upper = q3 + factor * iqr  # upper fence
    mask = (data[column] < lower) | (data[column] > upper)  # True where outlier
    return data[mask], lower, upper  # return outlier rows + the fences


outliers_iqr, lb, ub = detect_outliers_iqr(df, "age")
print("\n" + "=" * 60)
print("SECTION 2 — IQR detection on 'age'")
print("=" * 60)
print(f"Acceptable range: [{lb:.2f}, {ub:.2f}]")
print(f"Outliers found: {len(outliers_iqr)}")
print(outliers_iqr[["age"]])


# ----------------------------------------------------------------------
# 3. Z-SCORE METHOD — how many standard deviations from the mean?
# ----------------------------------------------------------------------
# z = (value - mean) / std ; |z| > 3 means "more than 3 std devs away"
z_scores = np.abs(np.asarray(stats.zscore(df["age"])))  # absolute z-score for every row
outliers_z = df[z_scores > 3]  # keep only rows with |z| > 3

print("\n" + "=" * 60)
print("SECTION 3 — Z-score detection on 'age' (threshold |z| > 3)")
print("=" * 60)
print(outliers_z[["age"]])


# ----------------------------------------------------------------------
# 4. ISOLATION FOREST — detect outliers across MULTIPLE columns at once
# ----------------------------------------------------------------------
# Build 300 normal (income, spending) pairs that are correlated
n = 300
inc = rng.normal(50000, 12000, n)  # incomes
spd = inc * 0.4 + rng.normal(0, 3000, n)  # spending tracks income
X_multi = pd.DataFrame({"income": inc, "spend": spd})

# Inject two rows that are weird only in COMBINATION
X_multi.loc[n] = [500000, 5000]  # huge income, tiny spend
X_multi.loc[n + 1] = [5000, 200000]  # tiny income, huge spend

iso = IsolationForest(contamination=0.02, random_state=42)
# fit_predict returns -1 for outliers and +1 for normal rows
X_multi["is_outlier"] = iso.fit_predict(X_multi[["income", "spend"]])

print("\n" + "=" * 60)
print("SECTION 4 — Isolation Forest (multivariate)")
print("=" * 60)
print(X_multi[X_multi["is_outlier"] == -1])  # show only the flagged rows

plt.figure(figsize=(6, 4))
sns.scatterplot(
    data=X_multi,
    x="income",
    y="spend",
    hue="is_outlier",
    palette={1: "steelblue", -1: "red"},
)
plt.title("Isolation Forest: red = outlier")
plt.savefig("section4_isoforest.png", dpi=100)
plt.close()
print("[Saved] section4_isoforest.png")


# ----------------------------------------------------------------------
# 5. FIXING BY DELETION — only for impossible / erroneous values
# ----------------------------------------------------------------------
# Human ages must be between 0 and 120; anything else MUST be an error
mask_possible = (df["age"] >= 0) & (df["age"] <= 120)
df_deleted = df[mask_possible].copy()  # keep only physically possible rows

print("\n" + "=" * 60)
print("SECTION 5 — Deletion of impossible values")
print("=" * 60)
print(
    f"Rows before: {len(df)}, after: {len(df_deleted)} "
    f"(removed {len(df) - len(df_deleted)})"
)


# ----------------------------------------------------------------------
# 6. FIXING BY CAPPING (WINSORIZATION) — clamp extremes to the fences
# ----------------------------------------------------------------------
def cap_column(data, column, factor=1.5):
    """Add a new column with values clipped to the IQR fences."""
    q1 = data[column].quantile(0.25)  # lower quartile
    q3 = data[column].quantile(0.75)  # upper quartile
    iqr = q3 - q1  # spread of the middle 50%
    lower, upper = q1 - factor * iqr, q3 + factor * iqr  # fences
    # .clip() forces every value into [lower, upper]; extremes become the fence
    data[column + "_capped"] = data[column].clip(lower=lower, upper=upper)
    return data


df = cap_column(df, "income")  # creates df['income_capped']

print("\n" + "=" * 60)
print("SECTION 6 — Capping (largest values, before vs after)")
print("=" * 60)
print(df[["income", "income_capped"]].sort_values("income", ascending=False).head(4))


# ----------------------------------------------------------------------
# 7. FIXING BY TRANSFORMATION — log-compress skewed features like income
# ----------------------------------------------------------------------
# np.log1p(x) = log(1 + x); the +1 keeps it safe when x = 0.
# NOTE: we log the CAPPED column — log() cannot handle negatives,
# so always remove/cap invalid values BEFORE transforming.
df["income_log"] = np.log1p(df["income_capped"])

# Yeo-Johnson is an automatic transformation that also works with negatives
pt = PowerTransformer(method="yeo-johnson")
df["age_yj"] = pt.fit_transform(df[["age"]])

print("\n" + "=" * 60)
print("SECTION 7 — Transformation")
print("=" * 60)
print(f"Raw income skew:    {df['income'].skew():.2f}")
print(f"Log income skew:    {df['income_log'].skew():.2f}  (closer to 0 = better)")

# Histogram before vs after log transform
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
sns.histplot(data=df, x="income", bins=30, kde=True)
plt.title("Income (raw, heavily skewed)")
plt.subplot(1, 2, 2)
sns.histplot(data=df, x="income_log", bins=30, kde=True)
plt.title("Income (log-transformed)")
plt.tight_layout()
plt.savefig("section7_transform.png", dpi=100)
plt.close()
print("[Saved] section7_transform.png")


# ----------------------------------------------------------------------
# 8. FIXING BY IMPUTATION — replace bad values with the MEDIAN
# ----------------------------------------------------------------------
# The median is robust: extreme values barely move it (unlike the mean)
median_age = df["age"].median()

df["age_imputed"] = df["age"]  # copy column
bad = (df["age"] < 0) | (df["age"] > 120)  # mask of bad rows
df.loc[bad, "age_imputed"] = median_age  # overwrite bad rows

print("\n" + "=" * 60)
print("SECTION 8 — Imputation with median")
print("=" * 60)
print(f"Median age used for imputation: {median_age}")
print(df[df["age"] != df["age_imputed"]][["age", "age_imputed"]])


# ----------------------------------------------------------------------
# 9. FIXING BY FLAGGING — keep the value, tell the model "this is weird"
# ----------------------------------------------------------------------
df["age_is_outlier"] = ((df["age"] < 0) | (df["age"] > 120)).astype(int)

print("\n" + "=" * 60)
print("SECTION 9 — Flagging outliers")
print("=" * 60)
print(df[df["age_is_outlier"] == 1][["age", "age_is_outlier"]])


# ----------------------------------------------------------------------
# 10. END-TO-END: train a model DIRTY vs CLEAN (with NO data leakage)
# ----------------------------------------------------------------------
# Build a regression problem where the target genuinely depends on income,
# then pollute a few income values with typos (extra zeros).
np.random.seed(7)
X_clean_vals = rng.normal(50000, 10000, 400)  # clean incomes
noise = rng.normal(0, 5000, 400)  # random noise
y_vals = 2.5 * X_clean_vals + noise  # target = f(income) + noise

# Pollute 3% of rows: multiply income by 100 (classic typo)
dirty = X_clean_vals.copy()
idx = rng.choice(400, size=12, replace=False)  # pick 12 random rows
dirty[idx] = dirty[idx] * 100  # blow them up x100

X_dirty = pd.DataFrame({"income": dirty})
X_cleaned = pd.DataFrame({"income": X_clean_vals})

# --- leak-free cleaning pattern: compute bounds on TRAIN only ---
X_tr_d, X_te_d, y_tr, y_te = train_test_split(
    X_dirty, y_vals, test_size=0.2, random_state=42
)  # split dirty data

# Learn the IQR fences from the TRAINING split only
q1, q3 = X_tr_d["income"].quantile([0.25, 0.75])
iqr = q3 - q1
low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
X_tr_d["income"] = X_tr_d["income"].clip(low, high)  # cap TRAIN with its own fences
X_te_d["income"] = X_te_d["income"].clip(low, high)  # cap TEST with TRAIN's fences

# Same split for the already-clean version (fair comparison)
X_tr_c, X_te_c, _, _ = train_test_split(
    X_cleaned, y_vals, test_size=0.2, random_state=42
)

# Linear regression is very sensitive to outliers -> the difference shows
model_dirty = make_pipeline(StandardScaler(), LinearRegression())
model_clean = make_pipeline(StandardScaler(), LinearRegression())

# Train on training data, score on held-out test data
model_dirty.fit(X_tr_d, y_tr)
model_clean.fit(X_tr_c, y_tr)
r2_dirty = model_dirty.score(X_te_d, y_te)  # R² on test set (dirty version)
r2_clean = model_clean.score(X_te_c, y_te)  # R² on test set (clean version)

print("\n" + "=" * 60)
print("SECTION 10 — Model comparison (test-set R², higher is better)")
print("=" * 60)
print(f"R² with outlier-polluted data: {r2_dirty:.3f}")
print(f"R² with clean data:            {r2_clean:.3f}")
print(f"Improvement from cleaning:     {r2_clean - r2_dirty:+.3f}")

print("\nDone! Check the .png files for the visualisations.")
