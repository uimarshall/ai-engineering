#####################################################

# Paired Sample T - Test

# In Paired Sample T Test, we compare the means in scenarios where you have two samples of observations.
# A common use case for the Paired samples T Test is comparing the results before and after an event.

#####################################################
# Paired Sample T-Test
#
# WHAT IT IS: a hypothesis test for two samples of observations that
# are LINKED ("paired") - each observation in sample 1 has exactly one
# partner in sample 2 (same person, same store, same machine, same day).
# Because we test the per-pair DIFFERENCE, each subject acts as its own
# control, which removes between-subject noise and makes the test much
# more sensitive than an independent two-sample t-test.
# Typical use case: comparing results BEFORE and AFTER an event.
#####################################################

# ---------------- IMPORT REQUIRED PACKAGES ----------------

import os  # stdlib; used here to create the "plots/" output folder

import matplotlib.pyplot as plt  # plotting: plt.hist(), plt.legend(), plt.show(), plt.savefig()
import numpy as np  # numerical arrays + random-number generation (np.random)
from scipy.stats import norm, ttest_rel

# ttest_rel  -> the paired (related-samples) t-test function itself
# norm       -> the normal distribution object; norm.rvs() draws random normal values
#               (we use it only to fabricate realistic-looking mock data)


# ---------------- CREATE MOCK DATA ----------------
# In a real project "before"/"after" would come from a database, CSV or API.
# Here we simulate them so the script is runnable end-to-end.

# Before & After population sample
before = np.asarray(norm.rvs(loc=500, scale=100, size=100, random_state=42)).astype(int)
# norm.rvs(...)  = draw random samples from a Normal (Gaussian) distribution
#   loc=500      = mean (average spending / score / KPI level "before")
#   scale=100    = standard deviation (how spread out the values are)
#   size=100     = 100 observations  -> 100 "units" (e.g. 100 customers or 100 stores)
#   random_state=42 -> fixed seed, so everyone running this gets the SAME numbers (reproducible)
# .astype(int)   -> truncate the floats to whole numbers (looks like real integer KPI values,
#                   e.g. purchases in $ or units; note: this TRUNCATES, it does not round)

np.random.seed(42)
# Seeds NumPy's GLOBAL random generator, so the next np.random.* call is reproducible too.
# (It is separate from random_state=42 above, which scipy uses internally.)

after = before + np.random.randint(low=-50, high=75, size=100)
# np.random.randint(low=-50, high=75, size=100) -> 100 random WHOLE numbers from -50 up to 74
#        (low is inclusive, high is exclusive, so each unit changes by -50 ... +74;
#         the average change is therefore about (+12))
# before + (...): this is the KEY line - the "after" value of unit i is built FROM the
#        "before" value of the same unit i. That dependency is exactly what makes these
#        two samples PAIRED (matched), not independent. Value i in `after` and value i in
#        `before` belong to the same customer / store / machine.

# ---------------- VISUALISE THE TWO SAMPLES ----------------
os.makedirs(
    "plots", exist_ok=True
)  # make sure the output folder exists (no error if it does)

plt.hist(before, density=True, alpha=0.5, label="Before")
# plt.hist draws a histogram of the `before` sample
#   density=True -> the y-axis is a probability density (area under the bars = 1), so the
#                   two histograms are comparable even if sample sizes differed
#   alpha=0.5    -> 50% transparency, so overlapping bars of both colours remain visible
#   label="Before" -> text used by the legend
plt.hist(after, density=True, alpha=0.5, label="After")  # same for the "after" sample
plt.legend()  # draw the legend box (uses the labels given above)
plt.savefig("plots/paired_sample_t_test.png", dpi=300, bbox_inches="tight")
# FIXED: save BEFORE show(). In the original file plt.show() came first and plt.savefig()
#        second, which can save a blank/closed figure with some backends.
#   dpi=300         -> high resolution, good for docs and slides
#   bbox_inches="tight" -> crops the whitespace border around the plot
plt.show()  # display the figure in a window / notebook

# ---------------- DESCRIPTIVE STATISTICS ----------------
before_mean = before.mean()  # arithmetic average of the "before" sample
after_mean = after.mean()  # arithmetic average of the "after" sample
print(before_mean, after_mean)  # eyeball check: how big is the raw difference?
# Expected here: the "after" mean sits ~12 points above the "before" mean,
# because the random increments run from -50 to +74 (average ≈ +12).


# ---------------- STATE HYPOTHESIS & SET ACCEPTANCE CRITERIA ----------------

null_hypothesis = (
    "The mean of the Before sample is eaqual to the mean of the After sample"
)
# H0 (the "boring" default): no real effect; before and after have the same mean
# (typo "eaqual" kept from the original file - worth fixing to "equal")

alternate_hypothesis = "The mean of the Before is different to the mean of the After"
# H1: there IS a difference (note this is a TWO-SIDED alternative - "different from",
# not "greater than" or "less than")

acceptance_criteria = 0.05
# Alpha = our risk tolerance for a false positive (Type I error) = 5%.
# If the p-value we compute is at or below this bar, we reject H0.

# ---------------- EXECUTE THE HYPOTHESIS TEST ----------------

t_statistic, p_value = ttest_rel(before, after)
# ttest_rel = paired/related-samples t-test. Internally it:
#   1) computes the per-unit differences  d_i = before_i - after_i
#   2) averages them:                     d_bar = mean(d_i)
#   3) computes their standard deviation: s_d
#   4) t = d_bar / (s_d / sqrt(n))        -> the test statistic
#   5) converts t into a two-sided p-value (df = n - 1 = 99)
# It returns a tuple: (t statistic, p-value). Here d_bar is negative (~-12),
# so the t statistic is negative - the sign just tells you the DIRECTION.
print(t_statistic, p_value)  # inspect both numbers before judging

# ---------------- PRINT THE RESULTS (p-value) ----------------

if p_value <= acceptance_criteria:
    # p <= alpha -> the observed difference is too unlikely under H0 -> reject H0
    print(
        f"As our p-value of {p_value} is less than our acceptance_criteria of {acceptance_criteria} - we reject the NH, and conclude that: {alternate_hypothesis}"
    )

else:
    # p > alpha -> we cannot rule out chance -> we fail to reject (retain) H0
    print(
        f"As our p-value of {p_value} is greater than our acceptance_criteria of {acceptance_criteria} - we retain the NH, and conclude that: {null_hypothesis}"
    )
