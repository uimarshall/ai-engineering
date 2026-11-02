"""Maximum Likelihood Estimation for Logistic Regression - practical demo.

Run:  python mle_logistic_regression_demo.py
Needs: numpy, scipy, scikit-learn, matplotlib
"""

import numpy as np  # numerical arrays and maths
import matplotlib.pyplot as plt  # plotting
from scipy.optimize import minimize  # general-purpose optimiser
from sklearn.linear_model import LogisticRegression  # library implementation

# ---------------------------------------------------------------------------
# 1. Data (approximated from the slides): hours studied and pass (1) / fail (0)
# ---------------------------------------------------------------------------
hours_passed = np.array([1.5, 2.6, 4.3, 4.55, 5.3, 5.75, 6.1, 6.45, 6.7, 7.0, 8.0, 8.25])
hours_failed = np.array([0.1, 0.35, 0.65, 1.0, 1.4, 1.75, 2.15, 2.7, 3.0, 3.6, 5.5])

x = np.concatenate([hours_passed, hours_failed])  # all hours in one array
y = np.concatenate([np.ones(len(hours_passed)), np.zeros(len(hours_failed))])  # labels


# ---------------------------------------------------------------------------
# 2. Building blocks
# ---------------------------------------------------------------------------
def sigmoid(z):
    """Turn log-odds (any real number) into a probability between 0 and 1."""
    return 1.0 / (1.0 + np.exp(-z))


def total_log_likelihood(intercept, slope, x, y):
    """Total log likelihood of a candidate line (log-odds = intercept + slope * x)."""
    log_odds = intercept + slope * x  # project points onto the line
    p_pass = sigmoid(log_odds)  # predicted probability of passing
    # Passers use p, failers use 1 - p (probability of the class they really are)
    likelihood = np.where(y == 1, p_pass, 1.0 - p_pass)
    return np.sum(np.log(likelihood))  # log each value, then add them up


# ---------------------------------------------------------------------------
# 3. Step by step for ONE candidate line (the slides' idea)
# ---------------------------------------------------------------------------
b0, b1 = -3.0, 0.8  # a guessed intercept and slope
p = sigmoid(b0 + b1 * x)  # predicted P(pass) for every student
lik = np.where(y == 1, p, 1 - p)  # likelihood of each student's TRUE class
print("Likelihoods (passers):", np.round(lik[y == 1], 2))
print("Likelihoods (failers):", np.round(lik[y == 0], 2))
print("Log likelihoods (passers):", np.round(np.log(lik[y == 1]), 2))
print("Log likelihoods (failers):", np.round(np.log(lik[y == 0]), 2))
print(f"Total log likelihood for line ({b0}, {b1}): {np.log(lik).sum():.2f}\n")

# ---------------------------------------------------------------------------
# 4. Compare a few candidate lines - highest total log likelihood wins
# ---------------------------------------------------------------------------
candidates = {"blue": (-2.0, 0.4), "red": (-3.0, 0.7), "orange": (-3.0, 0.82), "bad": (1.0, -0.5)}
for name, (c0, c1) in candidates.items():
    print(f"{name:7s} intercept={c0:5.2f} slope={c1:5.2f} "
          f"-> total log likelihood = {total_log_likelihood(c0, c1, x, y):7.2f}")

# ---------------------------------------------------------------------------
# 5. Let a computer find the maximum (minimise the NEGATIVE log likelihood)
# ---------------------------------------------------------------------------
result = minimize(
    lambda w: -total_log_likelihood(w[0], w[1], x, y),  # optimisers minimise, so flip sign
    x0=[0.0, 0.0],  # starting guess
)
mle_intercept, mle_slope = result.x  # best-fitting parameters
print(f"\nMLE (scipy):   intercept={mle_intercept:.2f}, slope={mle_slope:.2f}, "
      f"log likelihood={-result.fun:.2f}")

# ---------------------------------------------------------------------------
# 6. Same thing with scikit-learn (C=inf => no regularisation => pure MLE)
# ---------------------------------------------------------------------------
model = LogisticRegression(C=np.inf)  # huge C switches the regularisation penalty off
model.fit(x.reshape(-1, 1), y)  # sklearn wants a 2-D feature matrix
print(f"MLE (sklearn): intercept={model.intercept_[0]:.2f}, slope={model.coef_[0][0]:.2f}")

# ---------------------------------------------------------------------------
# 7. Visualise: log-odds line and the sigmoid curve
# ---------------------------------------------------------------------------
grid = np.linspace(0, 9, 200)  # x values for drawing
log_odds_line = mle_intercept + mle_slope * grid  # straight line in log-odds space
curve = sigmoid(log_odds_line)  # same line squashed into probabilities

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))  # two side-by-side charts
ax1.plot(grid, log_odds_line, color="orange", lw=3)  # best-fit line
ax1.axhline(0, color="grey", ls="--", lw=0.8)  # log-odds 0 means 50% probability
ax1.set(xlabel="Hours Studied", ylabel="Log Odds of Passing",
        title=f"y = {mle_slope:.2f}x {mle_intercept:+.2f}")
ax2.plot(grid, curve, color="orange", lw=3)  # best-fit sigmoid
ax2.scatter(x, y, color="blue", alpha=0.5, s=80)  # original data
ax2.set(xlabel="Hours Studied", ylabel="Probability of Passing", title="Sigmoid curve")
plt.tight_layout()
plt.savefig("mle_logistic_regression_result.png", dpi=120)  # save beside the script
print("Saved mle_logistic_regression_result.png")

# ---------------------------------------------------------------------------
# 8. Likelihood surface: see the "peak" that MLE climbs
# ---------------------------------------------------------------------------
b0_grid = np.linspace(-8, 2, 120)  # intercept values to try
b1_grid = np.linspace(-0.5, 2.0, 120)  # slope values to try
ll = np.array([[total_log_likelihood(a, b, x, y) for a in b0_grid] for b in b1_grid])

plt.figure(figsize=(6, 5))
plt.contourf(b0_grid, b1_grid, ll, levels=30, cmap="viridis")  # coloured heat map
plt.colorbar(label="Total log likelihood")
plt.scatter([mle_intercept], [mle_slope], color="red", label="MLE (peak)")  # best point
plt.xlabel("Intercept")
plt.ylabel("Slope")
plt.legend()
plt.title("Log-likelihood surface")
plt.tight_layout()
plt.savefig("mle_likelihood_surface.png", dpi=120)
print("Saved mle_likelihood_surface.png")
