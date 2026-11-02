"""The formula for a sigmoid curve - a beginner's practical demo.

Run with:  python sigmoid_formula_demo.py
Requires:  numpy, matplotlib, scikit-learn  (pip install numpy matplotlib scikit-learn)
Plots are saved as PNG files next to this script (no window pops up).
"""

from pathlib import Path  # build file paths in a portable way

import matplotlib  # plotting library

matplotlib.use("Agg")  # non-interactive backend: save images instead of opening windows
import matplotlib.pyplot as plt  # plotting interface
import numpy as np  # arrays and maths (np.exp is Euler's number e raised to a power)
from sklearn.linear_model import LogisticRegression  # model used to learn m and c

OUT_DIR = Path(__file__).parent  # save images beside this script


def straight_line(x, m, c):
    """Linear part of logistic regression: y (the log-odds) = m*x + c."""
    return m * x + c  # slope times input plus intercept


def sigmoid(y):
    """Sigmoid function: p = 1 / (1 + e^(-y)). Squashes any number into (0, 1)."""
    return 1 / (1 + np.exp(-y))  # works for a single number or a numpy array


def predict_probability(x, m, c):
    """Substitute y = m*x + c into the sigmoid: p = 1 / (1 + e^(-(m*x + c)))."""
    return sigmoid(straight_line(x, m, c))  # line first, then sigmoid


def demo_squashing() -> None:
    print("=== 1. The sigmoid squashes any number into 0..1 ===")
    for y in [-10, -4, -2, 0, 2, 4, 10]:  # some log-odds values, from very negative to very positive
        print(f"log-odds y = {y:>3}  ->  probability p = {sigmoid(y):.4f}")  # one row per value
    print("Note: y = 0 gives exactly p = 0.5 (an even chance).\n")


def demo_round_trip() -> None:
    print("=== 2. Sigmoid undoes the log-odds ===")
    p = 0.8  # start with a probability
    odds = p / (1 - p)  # convert to odds (= 4)
    log_odds = np.log(odds)  # convert to log-odds (= 1.386); np.log is the natural log
    back = sigmoid(log_odds)  # convert back with the sigmoid
    print(f"p={p}  odds={odds:.2f}  log-odds={log_odds:.3f}  sigmoid(log-odds)={back:.2f}\n")


def demo_manual_predictions() -> None:
    print("=== 3. Plugging mx + c into the sigmoid by hand ===")
    m, c = 0.8, -3.5  # an example slope and intercept (log-odds go up 0.8 per hour)
    print(f"line: log-odds = {m}*hours + ({c})")
    print(f"{'Hours':>6} {'log-odds':>9} {'P(pass)':>8}")  # table header
    for hours in range(0, 10, 1):  # students who studied 0..9 hours
        y = straight_line(hours, m, c)  # predicted log-odds from the straight line
        p = predict_probability(hours, m, c)  # probability after the sigmoid
        print(f"{hours:>6} {y:>9.2f} {p:>8.3f}")  # print one row
    print(f"50% point is where m*x + c = 0  ->  x = -c/m = {-c / m:.2f} hours\n")


def demo_effect_of_m_and_c() -> None:
    print("=== 4. What do m and c do to the curve? ===")
    x = np.linspace(-1, 10, 300)  # hours from -1 to 10, finely spaced for smooth curves
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))  # two charts side by side

    for m in [0.4, 0.8, 2.0]:  # different slopes
        axes[0].plot(x, predict_probability(x, m, -4.0 * m), label=f"m={m}")  # c = -4m keeps midpoint at x=4
    axes[0].set(title="Bigger m = steeper S (midpoint fixed at 4 h)", xlabel="Hours", ylabel="P(pass)")
    axes[0].legend()

    for c in [-6.0, -3.5, -1.0]:  # different intercepts, same slope
        axes[1].plot(x, predict_probability(x, 0.8, c), label=f"c={c}")  # shifting c slides the curve
    axes[1].set(title="Changing c slides the curve left/right", xlabel="Hours", ylabel="P(pass)")
    axes[1].legend()

    fig.tight_layout()  # avoid overlapping labels
    fig.savefig(OUT_DIR / "sigmoid_m_and_c.png", dpi=120)  # save to disk
    plt.close(fig)  # free memory
    print("Saved sigmoid_m_and_c.png\n")


def demo_fit_exam_model() -> None:
    print("=== 5. Let scikit-learn find m and c, then rebuild the probabilities ===")
    hours = np.array([0.1, 0.3, 0.7, 1.0, 1.4, 1.8, 2.1, 2.7, 3.0, 3.6, 5.5,
                      1.5, 2.6, 4.3, 4.5, 5.3, 5.7, 6.1, 6.5, 6.7, 7.0, 8.0, 8.3])  # hours studied
    passed = np.array([0] * 11 + [1] * 12)  # 0 = failed, 1 = passed

    model = LogisticRegression()  # create the model
    model.fit(hours.reshape(-1, 1), passed)  # learn the line in log-odds space (needs a 2D input)
    m = model.coef_[0][0]  # learned slope
    c = model.intercept_[0]  # learned intercept
    print(f"Learned: m = {m:.3f}, c = {c:.3f}")

    # Our own formula must match the library's probabilities exactly
    ours = predict_probability(hours, m, c)  # p = 1 / (1 + e^-(mx + c)) for every student
    theirs = model.predict_proba(hours.reshape(-1, 1))[:, 1]  # sklearn's P(pass) column
    print(f"Formula matches scikit-learn: {np.allclose(ours, theirs)}")

    # Turn probabilities into pass/fail decisions with a 0.5 threshold
    predicted = (ours >= 0.5).astype(int)  # True -> 1, False -> 0
    print(f"Accuracy on training data: {(predicted == passed).mean():.0%}\n")

    grid = np.linspace(0, 9, 200)  # smooth range of hours for plotting
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))  # left: log-odds line, right: sigmoid
    axes[0].scatter(hours, passed, label="Students")  # raw 0/1 data
    axes[0].plot(grid, straight_line(grid, m, c), color="red", label="log-odds = mx + c")  # straight line
    axes[0].axhline(0, color="grey", linestyle="--")  # log-odds 0 means p = 0.5
    axes[0].set(title="Step 1: straight line in log-odds space", xlabel="Hours", ylabel="log-odds")
    axes[0].legend()
    axes[1].scatter(hours, passed, label="Students")  # same data
    axes[1].plot(grid, predict_probability(grid, m, c), color="red", label="sigmoid(mx + c)")  # S-curve
    axes[1].axhline(0.5, color="grey", linestyle="--")  # decision threshold
    axes[1].set(title="Step 2: sigmoid turns it into a probability", xlabel="Hours", ylabel="P(pass)")
    axes[1].legend()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "sigmoid_line_to_curve.png", dpi=120)  # save to disk
    plt.close(fig)
    print("Saved sigmoid_line_to_curve.png")


if __name__ == "__main__":  # run only when executed directly
    demo_squashing()
    demo_round_trip()
    demo_manual_predictions()
    demo_effect_of_m_and_c()
    demo_fit_exam_model()
