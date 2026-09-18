# -*- coding: utf-8 -*-  # Tell Python which text encoding this file uses.

# #####################################################  # Decorative separator for readability.

# AB Testing - Our Task For ABC Grocery  # Describe the business experiment in this file.


# #####################################################  # Decorative separator for readability.

# IMPORT REQUIRED PACKAGES  # Load tools provided by external Python libraries.

from pathlib import Path  # Import Path for building portable file paths.
from typing import cast  # Import cast to narrow types for the type checker only.

import pandas as pd  # Import pandas for reading and organising table-shaped data.
from scipy.stats import (  # Import chi-square testing tools from SciPy.
    chi2,
    chi2_contingency,
)

# IMPORT DATA  # Start loading the campaign results used in the test.

campaign_data = (
    pd.read_excel(  # Read one worksheet from the Excel workbook into a DataFrame.
        Path(__file__).with_name(
            "grocery_database.xlsx"
        ),  # Find the workbook beside this Python file.
        sheet_name="campaign_data",  # Select the worksheet containing campaign results.
    )
)


# FILTER OUR DATA  # Remove the control group from this two-mailer comparison.

campaign_data = campaign_data.loc[  # Use .loc to select only rows matching a condition.
    campaign_data["mailer_type"]
    != "Control"  # Keep rows whose mailer type is not Control.
]


# SUMMARISE TO GET OUR OBSERVED FREQUENCIES  # Count the outcomes actually found in each mailer group.

observed_values = pd.crosstab(
    campaign_data[
        "mailer_type"
    ],  # Put each mailer type into a row of the summary table.
    campaign_data[
        "signup_flag"
    ],  # Put each signup outcome into a column of the summary table.
).values  # Extract only the counts as an array for SciPy.

mailer1_signup_rate = 123 / (
    252 + 123
)  # Calculate Mailer 1 signups divided by all Mailer 1 recipients.
mailer2_signup_rate = 127 / (
    209 + 127
)  # Calculate Mailer 2 signups divided by all Mailer 2 recipients.
print(
    mailer1_signup_rate, mailer2_signup_rate
)  # Display both signup rates for comparison.


# STATE HYPOTHESIS & SET ACCEPTANCE CRITERIA  # Define what the statistical test will evaluate.

null_hypothesis = "There is no relationship between mailer type and signup rate. They are independent"  # The default assumption: mailer type does not affect signups.
alternate_hypothesis = "There is a relationship between mailer type and signup rate. They are dependent"  # The competing claim: mailer type and signups are related.
acceptance_criteria = 0.05  # Set alpha to 5%, the tolerated false-positive risk.


# CALCULATE EXPECTED FREQUENCIES & CHI SQUARE STATISTICS  # Compare observed counts with counts expected under the null hypothesis.

chi2_statistic, p_value, dof, expected_values = chi2_contingency(
    observed_values,  # Supply the observed count table to the chi-square test.
    correction=False,  # Do not apply Yates' continuity correction to this test.
)
chi2_statistic = cast(
    float, chi2_statistic
)  # Narrow the type from the generic tuple element to float.
p_value = cast(
    float, p_value
)  # Narrow the type from the generic tuple element to float.
print(chi2_statistic, p_value)  # Print the statistic and p-value returned by SciPy.


# FIND THE CRITICAL VALUE FOR OUR TEST  # Find the cutoff for the statistic-based decision.

critical_value = chi2.ppf(
    1 - acceptance_criteria, dof
)  # ppf is the inverse CDF; it finds the chi-square cutoff for this probability and degrees of freedom.
print(critical_value)  # Display the threshold for statistical significance.

# PRINT THE RESULTS (Chi Square Statistics)  # Compare the statistic with its critical value.

if (
    chi2_statistic >= critical_value
):  # A statistic at or above the cutoff gives evidence against the null hypothesis.
    print(
        f"As our chi-square statistic of {chi2_statistic} is greater than our critical value of {critical_value} - we reject the NH, and conclude that: {alternate_hypothesis}"  # Print the significant result.
    )

else:  # A statistic below the cutoff is not strong enough evidence to reject the null hypothesis.
    print(
        f"As our chi-square statistic of {chi2_statistic} is less than our critical value of {critical_value} - we retain the NH, and conclude that: {null_hypothesis}"  # Print the non-significant result.
    )

# PRINT THE RESULTS (p-value)  # Make the same decision using the p-value approach.

if (
    p_value <= acceptance_criteria
):  # A p-value at or below alpha is statistically significant.
    print(
        f"As our p-value of {p_value} is less than our acceptance_criteria of {acceptance_criteria} - we reject the NH, and conclude that: {alternate_hypothesis}"  # Print the significant p-value result.
    )

else:  # A p-value above alpha is not strong enough evidence to reject the null hypothesis.
    print(
        f"As our p-value of {p_value} is greater than our acceptance_criteria of {acceptance_criteria} - we retain the NH, and conclude that: {null_hypothesis}"  # Print the non-significant p-value result.
    )
