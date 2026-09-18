#####################################################

# One Sample T - Test

# In Sample T Test, we compare the mean of the sample with the mean of the overall sample of the population.

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
    ttest_1samp,  # Import statistics tools from SciPy's stats module.; ttest_1samp runs a one-sample t-test to compare a sample's mean against a known value.
)

# CREATE MOCK DATA
# Total population
population = np.asarray(  # Wrap the output in an array so its type is explicit for later calls like .astype().
    norm.rvs(  # .rvs() draws "Random VariateS" - i.e. random sample values - from the norm (normal) distribution object.
        loc=500,  # loc is the distribution's mean (its centre point) - here, 500.
        scale=100,  # scale is the distribution's standard deviation (how spread out values are) - here, 100.
        size=1000,  # size is how many random values to generate in this call - here, 1000 values.
        random_state=42,  # random_state fixes the random number generator's seed so we get the same "random" numbers every time we run this (reproducibility).
    )
).astype(
    int
)  # Round/convert every generated value to a whole number, since our mock population represents whole-number measurements.

np.random.seed(
    42
)  # Fix NumPy's own global random seed too, so np.random.choice below also gives reproducible results.
# sample population
sample = np.random.choice(
    population, 250
)  # Randomly pick 250 values out of the population array to represent a smaller sample group.

plt.hist(
    population, density=True, alpha=0.5
)  # Plot a histogram of the population; density=True scales bars so their area sums to 1 (a probability density curve), alpha=0.5 makes bars semi-transparent.
plt.hist(
    sample, density=True, alpha=0.5
)  # Overlay a histogram of the sample on the same chart so we can visually compare the two distributions' shapes.
plt.show()  # Render the chart window so both histograms become visible.

population_mean = (
    population.mean()
)  # Calculate the arithmetic mean (average) of every value in the population.
sample_mean = (
    sample.mean()
)  # Calculate the arithmetic mean (average) of just the smaller sample.
print(
    population_mean, sample_mean
)  # Print both means so we can compare how close the sample's average is to the population's average.

# # STATE HYPOTHESIS & SET ACCEPTANCE CRITERIA

null_hypothesis = "The mean of the sample is eaqual to the mean of the population"  # The default assumption: the sample mean matches the population mean (no real difference).
alternate_hypothesis = "The mean of the sample is different to the mean of the population"  # The competing claim: the sample mean is genuinely different from the population mean.
acceptance_criteria = 0.05  # Set alpha to 5%, the tolerated false-positive risk for rejecting the null hypothesis.

# EXECUTE THE HYPOTHESIS TEST
t_statistic, p_value = ttest_1samp(
    sample, population_mean
)  # Compare the sample's mean against the known population_mean; returns the t-statistic and the p-value.
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
