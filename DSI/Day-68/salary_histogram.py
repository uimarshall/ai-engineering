"""Plot salary histogram showing mean vs median (Figure 1, Top-Left)."""

import matplotlib.pyplot as plt
import numpy as np

salaries = [
    45,
    52,
    55,
    58,
    60,
    62,
    65,
    68,
    70,
    72,
    75,
    80,
    85,
    90,
    95,
    100,
    110,
    120,
    150,
    200,
]

mean_salary = np.mean(salaries)
median_salary = np.median(salaries)

fig, ax = plt.subplots(figsize=(8, 6))
ax.hist(salaries, bins=10, color="steelblue", edgecolor="black", alpha=0.7)

ax.axvline(
    mean_salary,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Mean: ${mean_salary:.1f}k",
)
ax.axvline(
    median_salary,
    color="green",
    linestyle="--",
    linewidth=2,
    label=f"Median: ${median_salary:.1f}k",
)

ax.set_title("Employee Salary Distribution")
ax.set_xlabel("Salary ($k)")
ax.set_ylabel("Number of Employees")
ax.legend()

plt.tight_layout()
plt.savefig("salary_histogram.png", dpi=150)
plt.show()
