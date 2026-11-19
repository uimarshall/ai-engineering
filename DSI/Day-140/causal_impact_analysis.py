# cspell:ignore statsmodels causalimpact altime matplotlib
"""
Causal Impact Analysis - Beginner Practical Example
===================================================
Question this script answers:
    "We launched a new checkout flow on 2024-06-28. Did it actually
     increase orders, or would orders have changed anyway?"

The script:
  1. Simulates 240 days of business data (orders + 3 control metrics)
  2. Injects a known +15% lift after the intervention (so we can check the math)
  3. Trains a counterfactual model on the PRE-intervention period
  4. Predicts what WOULD have happened without the intervention
  5. Impact = Observed - Counterfactual
  6. Tests statistical significance
  7. Draws the classic 3-panel CausalImpact plot
  8. Runs a placebo test to prove the method is trustworthy

Every line is commented for a beginner.
"""

# -------------------------------------------------------------
# 1. Import libraries
# -------------------------------------------------------------
import matplotlib.pyplot as plt  # for all charts
import numpy as np  # for random numbers and math
import pandas as pd  # for tables and dates
import statsmodels.api as sm  # for the regression (counterfactual model)
from scipy import stats  # for the significance test (t-test)

# -------------------------------------------------------------
# 2. Simulate realistic business data
# -------------------------------------------------------------
# In a real project this is your CSV / SQL / API data.
# We simulate it so the lesson is self-contained and reproducible.

np.random.seed(42)  # makes the random numbers identical on every run

n_days = 240  # total days of history (180 before + 60 after)
dates = pd.date_range("2024-01-01", periods=n_days, freq="D")  # one row per day

# Position (0..239) of each day - used to build a slow upward trend
t = np.arange(n_days)

# --- Control variables (things that affect orders but were NOT changed) ---
# Advertising spend: drifts around 1000 with noise
ad_spend = 1000 + 150 * np.sin(2 * np.pi * t / 30) + np.random.normal(0, 40, n_days)

# Website traffic: partly driven by ad spend, plus its own noise
web_traffic = 5000 + 0.8 * ad_spend + np.random.normal(0, 300, n_days)

# Competitor price: slowly changing market condition
competitor_price = 100 + 0.02 * t + np.random.normal(0, 0.5, n_days)

# --- Target variable: daily orders ---
# Business-as-usual behaviour: trend + weekly seasonality + control effects
orders = (
    200  # baseline level (intercept)
    + 0.05 * t  # slow organic growth
    + 8 * np.sin(2 * np.pi * t / 7)  # weekly seasonality (weekends dip)
    + 0.08 * ad_spend  # ads bring orders
    + 0.01 * web_traffic  # traffic brings orders
    - 0.5 * competitor_price  # higher competitor price -> we win some
    + np.random.normal(0, 6, n_days)  # random noise (unexplained variance)
)

# Assemble everything into a DataFrame indexed by date
df = pd.DataFrame(
    {
        "orders": orders,
        "ad_spend": ad_spend,
        "web_traffic": web_traffic,
        "competitor_price": competitor_price,
        "day_index": t,  # 0,1,2,...  -> lets the model capture organic growth
    },
    index=dates,
)

# -------------------------------------------------------------
# 3. Inject the intervention and the true effect
# -------------------------------------------------------------
INTERVENTION_DATE = pd.Timestamp("2024-06-28")  # the day the new checkout launched
TRUE_LIFT = 0.15  # the REAL effect we baked in: +15% orders

post_mask = df.index >= INTERVENTION_DATE  # True for every day after launch

# Apply the +15% lift only to the post-intervention period.
# In real life you would NOT know this number - we only know it here so
# we can verify the model recovers it.
df.loc[post_mask, "orders"] = df.loc[post_mask, "orders"] * (1 + TRUE_LIFT)

print("=" * 65)
print("RAW DATA - first 5 rows")
print("=" * 65)
print(df.head().to_string())
print(f"\nIntervention date: {INTERVENTION_DATE.date()}")
print(f"Days before: {(~post_mask).sum()}  |  Days after: {post_mask.sum()}")

# -------------------------------------------------------------
# 4. Split into pre-intervention and post-intervention
# -------------------------------------------------------------
pre = df[~post_mask]  # training window: what happened normally
post = df[post_mask]  # evaluation window: what happened after the change

# -------------------------------------------------------------
# 5. Train the counterfactual model on the PRE period
# -------------------------------------------------------------
# The idea: learn the relationship "orders ~ controls" using ONLY the
# clean pre-intervention data. Then use it to predict the post period.
#
# We use Ordinary Least Squares (OLS) linear regression.

# y = the thing we want to predict (orders)
y_pre = pre["orders"]

# X = the control variables (ad spend, traffic, competitor price)
# sm.add_constant() adds the intercept term (the "baseline level")
X_pre = sm.add_constant(
    pre[["ad_spend", "web_traffic", "competitor_price", "day_index"]]
)

model = sm.OLS(y_pre, X_pre).fit()  # fit the model

print("\n" + "=" * 65)
print("COUNTERFACTUAL MODEL (trained only on pre-intervention data)")
print("=" * 65)
print(model.summary().tables[1])  # shows the coefficient for each control
print(f"R-squared: {model.rsquared:.4f}  ->  share of order variance explained")

# -------------------------------------------------------------
# 6. Predict the counterfactual for the POST period
# -------------------------------------------------------------
# Build the same feature matrix, but for the post-intervention days
X_post = sm.add_constant(
    post[["ad_spend", "web_traffic", "competitor_price", "day_index"]]
)

# predict() returns the expected number of orders on each post day
# IF the intervention had never happened
post["counterfactual"] = model.predict(X_post)

# get_prediction() also gives a confidence interval around each prediction
prediction = model.get_prediction(X_post)
summary_frame = prediction.summary_frame(alpha=0.05)  # 95% interval

# Copy the interval bounds onto our post dataframe
post["ci_lower"] = summary_frame["obs_ci_lower"]
post["ci_upper"] = summary_frame["obs_ci_upper"]

# -------------------------------------------------------------
# 7. Calculate the causal impact
# -------------------------------------------------------------
# Impact = what actually happened - what would have happened
post["impact"] = post["orders"] - post["counterfactual"]

# Total impact = sum of the daily differences
total_impact = post["impact"].sum()

# Average daily impact
avg_impact = post["impact"].mean()

print("\n" + "=" * 65)
print("RESULTS")
print("=" * 65)
print(f"Observed total orders    (post): {post['orders'].sum():,.0f}")
print(f"Counterfactual total orders   : {post['counterfactual'].sum():,.0f}")
print(f"Total causal impact           : {total_impact:,.0f}")
print(f"Average daily impact          : {avg_impact:,.1f} orders/day")

# Recovered percentage lift - compare with the TRUE_LIFT we injected
recovered_lift = post["orders"].sum() / post["counterfactual"].sum() - 1
print(f"\nRecovered lift     : {recovered_lift * 100:.1f}%")
print(f"True baked-in lift : {TRUE_LIFT * 100:.1f}%")
print("(A good model lands close to the true value.)")

# -------------------------------------------------------------
# 8. Statistical significance
# -------------------------------------------------------------
# We test: "Is the average post-intervention residual (impact) different from 0?"
# H0 (null hypothesis): the intervention had no effect (mean impact == 0)
# If p < 0.05 we reject H0 -> the effect is statistically significant.

t_stat, p_value = stats.ttest_1samp(post["impact"].dropna(), popmean=0)

print("\n" + "=" * 65)
print("STATISTICAL SIGNIFICANCE")
print("=" * 65)
print(f"t-statistic : {t_stat:.3f}")
print(f"p-value     : {p_value:.2e}")
if p_value < 0.05:
    print("Conclusion  : SIGNIFICANT - the intervention caused a real change.")
else:
    print("Conclusion  : NOT SIGNIFICANT - cannot rule out chance.")

# -------------------------------------------------------------
# 9. Plot the classic 3-panel CausalImpact chart
# -------------------------------------------------------------
fig, axes = plt.subplots(3, 1, figsize=(11, 11), sharex=True)

# --- Panel 1: Observed vs Counterfactual ---
ax = axes[0]
# Show the whole timeline, but shade the pre-period lightly
ax.plot(df.index, df["orders"], label="Observed", color="#1f77b4", linewidth=1.8)
ax.plot(
    post.index,
    post["counterfactual"],
    label="Counterfactual (no intervention)",
    color="#ff7f0e",
    linestyle="--",
)
# Fill the confidence interval of the counterfactual
ax.fill_between(
    post.index,
    post["ci_lower"],
    post["ci_upper"],
    color="#ff7f0e",
    alpha=0.15,
    label="95% interval",
)
# Vertical line marks the intervention day
ax.axvline(
    INTERVENTION_DATE,
    color="red",
    linestyle=":",
    linewidth=2,
    label="Intervention (2024-06-28)",
)
ax.set_ylabel("Daily orders")
ax.set_title("1. Observed vs Counterfactual")
ax.legend(loc="upper left", fontsize=8)
ax.grid(alpha=0.3)

# --- Panel 2: Point-wise impact ---
ax = axes[1]
ax.plot(post.index, post["impact"], color="#2ca02c", linewidth=1.5)
ax.axhline(0, color="black", linewidth=1)  # zero line = no effect
ax.fill_between(post.index, post["impact"], 0, color="#2ca02c", alpha=0.2)
ax.axvline(INTERVENTION_DATE, color="red", linestyle=":", linewidth=2)
ax.set_ylabel("Daily impact")
ax.set_title("2. Point-wise Impact (Observed - Counterfactual)")
ax.grid(alpha=0.3)

# --- Panel 3: Cumulative impact ---
ax = axes[2]
cumulative = post["impact"].cumsum()  # running total of the impact
ax.plot(post.index, cumulative, color="#9467bd", linewidth=2)
ax.fill_between(post.index, cumulative, 0, color="#9467bd", alpha=0.2)
ax.axvline(INTERVENTION_DATE, color="red", linestyle=":", linewidth=2)
ax.set_ylabel("Cumulative impact")
ax.set_xlabel("Date")
ax.set_title(f"3. Cumulative Impact (total = {total_impact:,.0f} extra orders)")
ax.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# -------------------------------------------------------------
# 10. Placebo test - the most important sanity check
# -------------------------------------------------------------
# Trick: pretend the intervention happened on a date in the PRE period
# where nothing actually changed. A trustworthy method must find NO effect.
# If it finds a big effect here, your model is picking up noise, not causation.
#
# IMPORTANT beginner lesson: with hundreds of rows, even a tiny random
# deviation can look "statistically significant" (p < 0.05) because the
# test has huge power. So we judge the placebo by its SIZE relative to
# the real effect, not only by its p-value.

PLACEBO_DATE = pd.Timestamp("2024-04-01")  # a fake intervention date

# Redefine the split as if the launch had happened on the placebo date
placebo_post_mask = (df.index >= PLACEBO_DATE) & (
    ~post_mask
)  # fake post, still before real launch
placebo_pre = df[(df.index < PLACEBO_DATE)]  # data before the fake date
placebo_post = df[placebo_post_mask].copy()  # data between fake date and real launch

# Train a fresh model on the shorter pre-period
X_placebo_pre = sm.add_constant(
    placebo_pre[["ad_spend", "web_traffic", "competitor_price", "day_index"]]
)
placebo_model = sm.OLS(placebo_pre["orders"], X_placebo_pre).fit()

# Predict the counterfactual over the fake post period
X_placebo_post = sm.add_constant(
    placebo_post[["ad_spend", "web_traffic", "competitor_price", "day_index"]]
)
placebo_post["counterfactual"] = placebo_model.predict(X_placebo_post)
placebo_post["impact"] = placebo_post["orders"] - placebo_post["counterfactual"]

# Test the placebo impact
_, placebo_p = stats.ttest_1samp(placebo_post["impact"].dropna(), popmean=0)

# Express both effects as a percentage of the baseline level for fair comparison
baseline = placebo_pre["orders"].mean()
placebo_pct = placebo_post["impact"].mean() / baseline * 100  # placebo lift, %
real_pct = recovered_lift * 100  # real lift, %

print("\n" + "=" * 65)
print("PLACEBO TEST (fake intervention date: %s)" % PLACEBO_DATE.date())
print("=" * 65)
print(f"Baseline daily orders      : {baseline:.1f}")
print(f"Placebo average impact     : {placebo_post['impact'].mean():.2f} orders/day")
print(f"Placebo lift               : {placebo_pct:.2f}%")
print(f"Placebo p-value            : {placebo_p:.3f}")
print(f"Real intervention lift     : {real_pct:.1f}%")
if abs(real_pct) > 3 * max(abs(placebo_pct), 1.0):
    print("Result: the real effect is far larger than the placebo noise")
    print("        -> the method is trustworthy.")
else:
    print("Warning: placebo effect is close to the real effect")
    print("         -> check model specification before trusting results.")

# -------------------------------------------------------------
# 11. Final summary for a stakeholder
# -------------------------------------------------------------
print("\n" + "=" * 65)
print("EXECUTIVE SUMMARY")
print("=" * 65)
print(f"""
Intervention   : New checkout flow launched {INTERVENTION_DATE.date()}
Analysis window: {post.index[0].date()} to {post.index[-1].date()} ({len(post)} days)

Observed orders      : {post['orders'].sum():>10,.0f}
Expected (no change) : {post['counterfactual'].sum():>10,.0f}
Net extra orders     : {post['orders'].sum() - post['counterfactual'].sum():>10,.0f}
Estimated lift       : {recovered_lift * 100:>9.1f}%
Statistically valid  : {"YES (p < 0.05)" if p_value < 0.05 else "NO (p >= 0.05)"}
""")
