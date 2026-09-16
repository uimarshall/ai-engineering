# -*- coding: utf-8 -*-

#####################################################

# AB Testing - Our Task For ABC Grocery

#####################################################

# IMPORT REQUIRED PACKAGES
# pandas: used to read Excel files and create tables
# numpy: helps convert SciPy output into clean numbers
# scipy.stats: contains the chi-square test and the chi-square distribution functions
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, chi2_contingency

# IMPORT DATA
# This reads the Excel workbook and loads the campaign_data sheet
# We use __file__ to make sure the file path works no matter where the script is run from
base_path = Path(__file__).resolve().parent
campaign_data = pd.read_excel(
    base_path / "grocery_database.xlsx", sheet_name="campaign_data"
)


# FILTER OUR DATA
# We only want rows for the 'delivery_club' campaign, because we are testing
# whether different mailer types affected signup rates in that campaign.
campaign_data = campaign_data[campaign_data["campaign_name"] == "delivery_club"].copy()

# signup_flag is stored as a number like 0 or 1, so we convert it to int
# so it works correctly in the cross-tabulation and chi-square calculation.
campaign_data["signup_flag"] = campaign_data["signup_flag"].astype(int)


# SUMMARISE TO GET OUR OBSERVED FREQUENCIES
# A crosstab shows the count of people in each combination of:
# - mailer_type (Control, Mailer1, Mailer2)
# - signup_flag (0 = no signup, 1 = signup)
# This creates the observed frequency table used in the chi-square test.
observed_table = pd.crosstab(campaign_data["mailer_type"], campaign_data["signup_flag"])


# STATE HYPOTHESIS & SET ACCEPTANCE CRITERIA
# H0 (null hypothesis): mailer type and signup outcome are independent
# H1 (alternative hypothesis): mailer type and signup outcome are associated
# alpha = 0.05 means we reject H0 only if the result is very unlikely under H0.
alpha = 0.05


# CALCULATE EXPECTED FREQUENCIES & CHI SQUARE STATISTICS
# chi2_contingency() performs the chi-square test of independence.
# It returns:
# - chi-square statistic
# - p-value
# - degrees of freedom
# - expected counts table
chi2_result = chi2_contingency(observed_table)

# Convert the SciPy result values to clean Python float/int data types.
# This avoids type-checking issues and keeps the values easy to read and use.
chi2_stat: float = float(np.asarray(chi2_result[0]).item())
p_value: float = float(np.asarray(chi2_result[1]).item())
dof: int = int(np.asarray(chi2_result[2]).item())
expected_array = np.asarray(chi2_result[3], dtype=float)

# Build a DataFrame of the expected counts to compare with the observed counts.
expected_table = pd.DataFrame(
    expected_array, index=observed_table.index, columns=observed_table.columns
)


# FIND THE CRITICAL VALUE FOR OUR TEST
# The critical value is the cutoff point on the chi-square distribution.
# If the test statistic is larger than this value, the result is statistically significant.
critical_value = chi2.ppf(1 - alpha, dof)

# Print the observed and expected tables so we can inspect the pattern.
print("Observed counts (mailer type x signup_flag):")
print(observed_table)
print("\nExpected counts:")
print(expected_table.round(2))

# Show the key test outputs.
print(f"\nChi-square statistic: {chi2_stat:.4f}")
print(f"Degrees of freedom: {dof}")
print(f"P-value: {p_value:.10f}")
print(f"Critical value at alpha = {alpha}: {critical_value:.4f}")

# Decision rule:
# - If chi-square statistic > critical value, or p-value < alpha,
#   we reject H0 and say there is a relationship.
# - Otherwise, we fail to reject H0 and say there is not enough evidence of a relationship.
if chi2_stat > critical_value or p_value < alpha:
    decision = "Reject H0: mailer type and signup outcome are associated."
else:
    decision = "Fail to reject H0: no evidence of an association between mailer type and signup outcome."

print(f"\nDecision: {decision}")
