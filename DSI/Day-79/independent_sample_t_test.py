#####################################################

# Independent Sample T - Test

# Independent Sample T Test, we compare the means of two independent samples and look to assess whether there is evidence that the associated
# population means are significantly different.

#####################################################

# IMPORT REQUIRED PACKAGES

from typing import (
    cast,  # Import cast to narrow types for the type checker only (no effect at runtime).
)

import matplotlib.pyplot as plt  # Import pyplot, a module for drawing charts such as histograms.
import numpy as np  # Import NumPy, the library that gives us fast arrays and random-sampling helpers.
from scipy.stats import (
    norm,  # norm represents the Normal (Gaussian/"bell curve") probability distribution.
)
from scipy.stats import (
    ttest_ind,  # Import statistics tools from SciPy's stats module.; ttest_ind runs an independent (two-sample) t-test comparing the means of two separate groups.
)

# CREATE MOCK DATA
# 2 Independent population sample
sample_A = np.asarray(  # Wrap the output in an array so its type is explicit for later calls like .astype().
    norm.rvs(  # .rvs() draws "Random VariateS" - i.e. random sample values - from the norm (normal) distribution object.
        loc=500,  # loc is the mean (centre) of sample A's underlying distribution - here, 500.
        scale=100,  # scale is the standard deviation (spread) of sample A's underlying distribution - here, 100.
        size=250,  # size is how many random values to generate for sample A - here, 250 values.
        random_state=42,  # random_state fixes the random seed so sample A is reproducible every run.
    )
).astype(
    int
)  # Convert the generated decimal values into whole numbers.
sample_B = np.asarray(  # Wrap the output in an array so its type is explicit for later calls like .astype().
    norm.rvs(  # Draw random values from a second, differently-shaped normal distribution to represent an independent group.
        loc=550,  # loc is the mean (centre) of sample B's underlying distribution - here, 550 (deliberately different from sample A).
        scale=150,  # scale is the standard deviation (spread) of sample B's underlying distribution - here, 150 (wider than sample A).
        size=100,  # size is how many random values to generate for sample B - here, 100 values (a different group size than sample A, which is fine for this test).
        random_state=42,  # random_state fixes the random seed so sample B is also reproducible every run.
    )
).astype(
    int
)  # Convert the generated decimal values into whole numbers.


plt.hist(
    sample_A, density=True, alpha=0.5
)  # Plot a histogram of sample A; density=True scales bars so their area sums to 1, alpha=0.5 makes bars semi-transparent.
plt.hist(
    sample_B, density=True, alpha=0.5
)  # Overlay a histogram of sample B on the same chart so we can visually compare the two groups' shapes.
plt.show()  # Render the chart window so both histograms become visible.

sample_A_mean = (
    sample_A.mean()
)  # Calculate the arithmetic mean of sample A into its own variable, keeping the original array intact for the t-test below.
sample_B_mean = (
    sample_B.mean()
)  # Calculate the arithmetic mean of sample B into its own variable, keeping the original array intact for the t-test below.
print(
    sample_A_mean, sample_B_mean
)  # Print both means so we can eyeball how different the two groups look before doing any formal statistics.

# # STATE HYPOTHESIS & SET ACCEPTANCE CRITERIA

null_hypothesis = "The mean of the sample A is eaqual to the mean of the sample B"  # The default assumption: both groups' true means are the same (no real difference).
alternate_hypothesis = "The mean of the sample A is different to the mean of the sample B"  # The competing claim: the two groups' true means are genuinely different.
acceptance_criteria = 0.05  # Set alpha to 5%, the tolerated false-positive risk for rejecting the null hypothesis.

# EXECUTE THE HYPOTHESIS TEST
t_statistic, p_value = ttest_ind(
    sample_A, sample_B
)  # Compare the two full arrays' means; returns the t-statistic and the p-value. NOTE: this must receive the original arrays, not their already-reduced means, or every group looks like a single-value sample.
t_statistic = cast(
    float, t_statistic
)  # Narrow the type from the generic tuple element to float.
p_value = cast(
    float, p_value
)  # Narrow the type from the generic tuple element to float.
print(t_statistic, p_value)  # Print the test statistic and p-value returned by SciPy.

# PRINT THE RESULTS (p-value)

if (
    p_value <= acceptance_criteria
):  # A p-value at or below alpha is statistically significant.
    print(
        f"As our p-value of {p_value} is less than our acceptance_criteria of {acceptance_criteria} - we reject the NH, and conclude that: {alternate_hypothesis}"  # Print the significant result.
    )

else:  # A p-value above alpha is not strong enough evidence to reject the null hypothesis.
    print(
        f"As our p-value of {p_value} is greater than our acceptance_criteria of {acceptance_criteria} - we retain the NH, and conclude that: {null_hypothesis}"  # Print the non-significant result.
    )

# WELCH'S T-TEST - More accurate
# Welch's t-test is a variant of the independent-samples t-test that does NOT assume the two groups have equal variance (spread) or equal sample size.
# Our two samples are built with different scale values (100 vs 150) and different sizes (250 vs 100), so this assumption-free version is the more trustworthy choice here.

# EXECUTE THE HYPOTHESIS TEST
t_statistic, p_value = ttest_ind(
    sample_A, sample_B, equal_var=False
)  # equal_var=False switches SciPy from the standard (Student's) t-test to Welch's t-test, which calculates the standard error using each group's own variance separately instead of pooling them into one shared estimate.
t_statistic = cast(
    float, t_statistic
)  # Narrow the type from the generic tuple element to float.
p_value = cast(
    float, p_value
)  # Narrow the type from the generic tuple element to float.
print(
    t_statistic, p_value
)  # Print the Welch's-test statistic and p-value returned by SciPy.

# PRINT THE RESULTS (p-value)

if (
    p_value <= acceptance_criteria
):  # A p-value at or below alpha is statistically significant.
    print(
        f"As our p-value of {p_value} is less than our acceptance_criteria of {acceptance_criteria} - we reject the NH, and conclude that: {alternate_hypothesis}"  # Print the significant result.
    )

else:  # A p-value above alpha is not strong enough evidence to reject the null hypothesis.
    print(
        f"As our p-value of {p_value} is greater than our acceptance_criteria of {acceptance_criteria} - we retain the NH, and conclude that: {null_hypothesis}"  # Print the non-significant result.
    )
