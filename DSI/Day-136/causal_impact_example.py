import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# ----------------------------------------------------------------------
# 1. Create the dataset
# ----------------------------------------------------------------------
# Simulate 8 months of sales data for two regions.
# Region A: received a marketing campaign (intervention).
# Region B: did not receive the campaign (control).

data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"],
    "Region_A_Sales": [1000, 1050, 1020, 1080, 1100, 1300, 1350, 1320],
    "Region_B_Sales": [950, 980, 960, 1000, 1020, 1050, 1080, 1070],
}
df = pd.DataFrame(data)
print("Original Data:")
print(df)
print("\n" + "=" * 50 + "\n")

# ----------------------------------------------------------------------
# 2. Split into pre- and post-intervention periods
# ----------------------------------------------------------------------
# The intervention (campaign) started in June.
# Pre-intervention: Jan - May (used to train the model).
# Post-intervention: Jun - Aug (used to evaluate the impact).

pre = df[df["Month"].isin(["Jan", "Feb", "Mar", "Apr", "May"])]
post = df[df["Month"].isin(["Jun", "Jul", "Aug"])]
print("Pre-intervention data (Jan-May):")
print(pre)
print("\nPost-intervention data (Jun-Aug):")
print(post)
print("\n" + "=" * 50 + "\n")

# ----------------------------------------------------------------------
# 3. Train a linear regression model on pre-intervention data
# ----------------------------------------------------------------------
# We predict Region_A_Sales (target) from Region_B_Sales (control).
# This model captures the relationship between the two regions
# before the intervention.

model = LinearRegression()
model.fit(pre[["Region_B_Sales"]], pre["Region_A_Sales"])

# Extract the model's parameters (slope and intercept)
slope = model.coef_[0]
intercept = model.intercept_
print(f"Model trained: Region_A_Sales = {slope:.4f} * Region_B_Sales + {intercept:.4f}")
print("\n" + "=" * 50 + "\n")

# ----------------------------------------------------------------------
# 4. Generate counterfactual predictions for the post-intervention period
# ----------------------------------------------------------------------
# Using the control (Region B), predict what Region A's sales
# would have been if the campaign had NOT happened.

counterfactual = model.predict(post[["Region_B_Sales"]])

# Create a comparison DataFrame
comparison = pd.DataFrame(
    {
        "Month": post["Month"],
        "Observed": post["Region_A_Sales"].values,
        "Counterfactual": counterfactual,
    }
)
print("Observed vs. Counterfactual (Post-intervention):")
print(comparison)
print("\n" + "=" * 50 + "\n")

# ----------------------------------------------------------------------
# 5. Calculate the causal impact
# ----------------------------------------------------------------------
# Causal impact = Observed - Counterfactual
# Positive impact: the intervention increased the outcome.
# Negative impact: the intervention decreased the outcome.

comparison["Impact"] = comparison["Observed"] - comparison["Counterfactual"]
print("Causal Impact per month:")
print(comparison)
print("\n" + "=" * 50 + "\n")

# Total impact across all post-intervention months
total_impact = comparison["Impact"].sum()
print(f"Total Causal Impact (sum over Jun-Aug): {total_impact:.2f}")
print("\n" + "=" * 50 + "\n")

# ----------------------------------------------------------------------
# 6. Estimate credible intervals (simplified)
# ----------------------------------------------------------------------
# Calculate the standard deviation of the residuals (errors)
# from the pre-intervention period. This represents the model's uncertainty.

residuals = pre["Region_A_Sales"] - model.predict(pre[["Region_B_Sales"]])
residual_std = residuals.std()

# 95% credible interval: ±1.96 * residual_std
comparison["CI_Lower"] = comparison["Counterfactual"] - 1.96 * residual_std
comparison["CI_Upper"] = comparison["Counterfactual"] + 1.96 * residual_std

print("With 95% Credible Intervals:")
print(comparison)
print("\n" + "=" * 50 + "\n")

# ----------------------------------------------------------------------
# 7. Visualize the results
# ----------------------------------------------------------------------
# Plot observed vs. counterfactual, with credible intervals.

plt.figure(figsize=(10, 6))

# Observed data (post-intervention)
plt.plot(
    comparison["Month"],
    comparison["Observed"],
    label="Observed",
    marker="o",
    color="blue",
)

# Counterfactual (predicted without intervention)
plt.plot(
    comparison["Month"],
    comparison["Counterfactual"],
    label="Counterfactual",
    linestyle="--",
    color="orange",
)

# Credible interval (shaded area)
plt.fill_between(
    comparison["Month"],
    comparison["CI_Lower"],
    comparison["CI_Upper"],
    color="blue",
    alpha=0.1,
    label="95% Credible Interval",
)

# Mark the intervention point (June, the first categorical position)
plt.axvline(x=0, color="red", linestyle=":", label="Intervention (Jun)")

plt.title("Causal Impact Analysis: Marketing Campaign on Sales")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ----------------------------------------------------------------------
# 8. Interpret the results
# ----------------------------------------------------------------------
print("\n" + "=" * 50 + "\n")
print("INTERPRETATION:")
print("----------------")
print("If the observed sales in June, July, and August are consistently")
print("higher than the counterfactual (and outside the credible interval),")
print("we conclude that the marketing campaign caused a positive increase in sales.")
print(
    "In this example, the total causal impact is approximately {:.0f} units.".format(
        total_impact
    )
)
