"""Probability, Odds, log(Odds) and Logistic Regression - a beginner's practical demo.

Run with:  python logistic_regression_demo.py
Requires:  numpy, matplotlib, scikit-learn  (pip install numpy matplotlib scikit-learn)
Plots are saved as PNG files next to this script (no window pops up).
"""

from pathlib import Path  # Path lets us build file locations in a portable way

import matplotlib  # plotting library

matplotlib.use("Agg")  # use a non-interactive backend so the script works anywhere
import matplotlib.pyplot as plt  # the plotting interface
import numpy as np  # numerical arrays and maths
from sklearn.linear_model import LogisticRegression  # the ML model we will train

OUT_DIR = Path(__file__).parent  # save images in the same folder as this script


# ----------------------------------------------------------------------------
# Part 1: Probability (dice example)
# ----------------------------------------------------------------------------
def probability(ways_event_can_happen: int, total_outcomes: int) -> float:
    """probability = number of ways the event can happen / total number of outcomes."""
    return ways_event_can_happen / total_outcomes  # simple division


# ----------------------------------------------------------------------------
# Part 2: Odds
# ----------------------------------------------------------------------------
def odds(p: float) -> float:
    """odds = P(event happens) / P(event does not happen) = p / (1 - p)."""
    if p >= 1:  # p = 1 means the event is certain, so we divide by zero
        return float("inf")  # odds are infinite in that case
    return p / (1 - p)  # the odds formula


# ----------------------------------------------------------------------------
# Part 3: log(Odds), also called the "logit"
# ----------------------------------------------------------------------------
def log_odds(p: float) -> float:
    """log(odds) = ln(p / (1 - p)). Goes from -infinity (p=0) to +infinity (p=1)."""
    if p <= 0:  # impossible event
        return float("-inf")  # log of 0 is negative infinity
    if p >= 1:  # certain event
        return float("inf")  # log of infinity is positive infinity
    return float(np.log(odds(p)))  # natural log of the odds


# ----------------------------------------------------------------------------
# Part 4: Sigmoid - converts log(odds) BACK into a probability
# ----------------------------------------------------------------------------
def sigmoid(z):
    """probability = 1 / (1 + e^(-z)), where z is the log(odds)."""
    return 1 / (1 + np.exp(-z))  # works on single numbers and numpy arrays


def demo_dice() -> None:
    print("=== Part 1-2: Dice example ===")
    p_six = probability(1, 6)  # one way to roll a six, six outcomes in total
    print(f"Probability of rolling a 6 : {p_six:.3f} ({p_six:.1%})")  # 0.167
    print(f"Odds of rolling a 6        : {odds(p_six):.3f}")  # 1/5 = 0.2
    print(f"log(odds) of rolling a 6   : {log_odds(p_six):.3f}")  # ln(0.2) = -1.609
    print(f"Sigmoid(log-odds) -> prob  : {sigmoid(log_odds(p_six)):.3f}")  # back to 0.167
    print()


def demo_table_and_plots() -> None:
    print("=== Part 3: Probability vs Odds vs log(Odds) table ===")
    print(f"{'Prob':>5} {'Odds':>8} {'log(Odds)':>10}")  # table header
    for p in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:  # same values as the notes
        print(f"{p:>5.1f} {odds(p):>8.2f} {log_odds(p):>10.2f}")  # one row per probability
    print()

    probs = np.linspace(0.01, 0.99, 99)  # many probabilities, avoiding exactly 0 and 1
    odds_vals = probs / (1 - probs)  # vectorised odds
    log_odds_vals = np.log(odds_vals)  # vectorised log(odds)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))  # two charts side by side
    axes[0].plot(probs, odds_vals)  # odds curve shoots up after p = 0.5
    axes[0].set(title="Probability vs Odds", xlabel="Probability", ylabel="Odds", ylim=(0, 20))
    axes[1].plot(probs, log_odds_vals)  # log(odds) is symmetric around p = 0.5
    axes[1].axhline(0, color="grey", linestyle="--")  # log(odds) = 0 where p = 0.5
    axes[1].set(title="Probability vs log(Odds)", xlabel="Probability", ylabel="log(Odds)")
    fig.tight_layout()  # avoid overlapping labels
    fig.savefig(OUT_DIR / "prob_odds_logodds.png", dpi=120)  # save to disk
    plt.close(fig)  # free memory
    print("Saved prob_odds_logodds.png\n")


# ----------------------------------------------------------------------------
# Part 5: Practical logistic regression - exam pass/fail from hours studied
# ----------------------------------------------------------------------------
def demo_exam_model() -> None:
    print("=== Part 4-5: Logistic regression on exam data ===")
    # Hours studied by 22 students (similar to the scatter plot in the notes)
    hours = np.array([0.1, 0.3, 0.7, 1.0, 1.4, 1.8, 2.1, 2.7, 3.0, 3.6, 5.5,
                      1.5, 2.6, 4.3, 4.5, 5.3, 5.7, 6.1, 6.5, 6.7, 7.0, 8.0, 8.3])
    # 0 = failed, 1 = passed (first 11 failed, remaining 12 passed)
    passed = np.array([0] * 11 + [1] * 12)

    X = hours.reshape(-1, 1)  # scikit-learn expects a 2D array: rows = students, columns = features
    model = LogisticRegression()  # create the model with default settings
    model.fit(X, passed)  # learn the best-fit line in log(odds) space

    b0 = model.intercept_[0]  # intercept: log(odds) when hours = 0
    b1 = model.coef_[0][0]  # slope: change in log(odds) per extra hour
    print(f"log(odds) = {b0:.3f} + {b1:.3f} * hours")
    print(f"Each extra hour multiplies the odds of passing by e^{b1:.3f} = {np.exp(b1):.2f}")
    print(f"Break-even point (p = 0.5): {-b0 / b1:.2f} hours\n")  # where log(odds) = 0

    print(f"{'Hours':>6} {'log(odds)':>10} {'Odds':>8} {'P(pass)':>8}")  # table header
    for h in [1, 2, 3, 4, 5, 6, 7, 8]:  # a few example students
        z = b0 + b1 * h  # predicted log(odds) from the straight line
        p = sigmoid(z)  # convert log(odds) -> probability
        print(f"{h:>6} {z:>10.2f} {np.exp(z):>8.2f} {p:>8.2f}")
    print()

    # Check our manual sigmoid agrees with scikit-learn's own prediction
    manual = sigmoid(b0 + b1 * 4.0)  # our calculation for 4 hours
    sklearn_p = model.predict_proba([[4.0]])[0][1]  # library calculation (column 1 = P(pass))
    print(f"4 hours: manual P(pass)={manual:.4f}, sklearn P(pass)={sklearn_p:.4f}")
    print(f"Predicted class for 4 hours (threshold 0.5): {model.predict([[4.0]])[0]}")
    print(f"Training accuracy: {model.score(X, passed):.0%}\n")  # fraction predicted correctly

    # Plot: data points, and the sigmoid curve the model learned
    grid = np.linspace(0, 9, 200)  # hours from 0 to 9 for a smooth curve
    curve = model.predict_proba(grid.reshape(-1, 1))[:, 1]  # P(pass) for each grid value
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(hours, passed, label="Students (0=fail, 1=pass)")  # raw data
    ax.plot(grid, curve, color="red", label="Sigmoid curve")  # fitted probability
    ax.axhline(0.5, color="grey", linestyle="--")  # decision threshold
    ax.set(xlabel="Hours of study", ylabel="Probability of passing",
           title="Logistic regression: exam pass probability")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "exam_sigmoid.png", dpi=120)  # save to disk
    plt.close(fig)
    print("Saved exam_sigmoid.png")


if __name__ == "__main__":  # run everything only when executed directly
    demo_dice()
    demo_table_and_plots()
    demo_exam_model()
