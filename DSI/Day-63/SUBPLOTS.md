I can't save files outside of chart/data outputs, but I can give you the complete, ready-to-copy markdown content below. You can paste it into a file named `matplotlib_subplots_guide.md`.

---

````markdown
# 📊 Matplotlib Subplots: A Beginner-Friendly Comprehensive Guide

## Table of Contents

1. [What Are Subplots?](#what-are-subplots)
2. [Why Use Subplots?](#why-use-subplots)
3. [The Two Main Approaches](#the-two-main-approaches)
4. [Method 1: `plt.subplot()` — The Simple Way](#method-1-pltsubplot--the-simple-way)
5. [Method 2: `plt.subplots()` — The Professional Way](#method-2-pltsubplots--the-professional-way)
6. [Method 3: `fig.add_subplot()` — The Object-Oriented Way](#method-3-figadd_subplot--the-object-oriented-way)
7. [Advanced Layouts](#advanced-layouts)
8. [Business Use Cases by Industry](#business-use-cases-by-industry)
9. [Common Beginner Mistakes](#common-beginner-mistakes)
10. [Quick Reference Cheat Sheet](#quick-reference-cheat-sheet)

---

## What Are Subplots?

A **subplot** is simply a smaller plot that lives inside a larger figure. Think of a figure as a blank canvas, and subplots as individual charts you place on that canvas.

Instead of generating four separate PNG files for four charts, you can arrange them in a **2×2 grid** inside one figure. This makes reports cleaner, presentations more professional, and dashboards easier to read.

---

## Why Use Subplots?

| Benefit          | Explanation                                               |
| ---------------- | --------------------------------------------------------- |
| **Comparison**   | Put two charts side-by-side to compare trends instantly.  |
| **Context**      | Show a zoomed-in view next to a full overview.            |
| **Efficiency**   | One figure = one file = one slide. Less clutter.          |
| **Storytelling** | Guide the viewer's eye from left to right, top to bottom. |

---

## The Two Main Approaches

Matplotlib gives you multiple ways to create subplots. As a beginner, you only need to know these three:

| Approach            | Best For                    | Syntax Style    |
| ------------------- | --------------------------- | --------------- |
| `plt.subplot()`     | Quick, simple grids         | MATLAB-style    |
| `plt.subplots()`    | Professional, flexible work | Object-oriented |
| `fig.add_subplot()` | Fine-grained control        | Object-oriented |

---

## Method 1: `plt.subplot()` — The Simple Way

This is the fastest way to throw a few charts together. It uses a **3-digit notation**: `plt.subplot(nrows, ncols, index)`.

### Sample Code

```python
import matplotlib.pyplot as plt
import numpy as np

# Generate sample data
x = np.linspace(0, 10, 100)   # 100 evenly spaced numbers from 0 to 10
y1 = np.sin(x)                # sine wave
y2 = np.cos(x)                # cosine wave

# Create the first subplot
plt.subplot(2, 1, 1)          # 2 rows, 1 column, select plot 1
plt.plot(x, y1, 'r-')         # plot y1 in red solid line
plt.title('Sine Wave')        # add a title to this subplot
plt.xlabel('Time')            # label the x-axis
plt.ylabel('Amplitude')       # label the y-axis

# Create the second subplot
plt.subplot(2, 1, 2)          # 2 rows, 1 column, select plot 2
plt.plot(x, y2, 'b-')         # plot y2 in blue solid line
plt.title('Cosine Wave')      # add a title to this subplot
plt.xlabel('Time')            # label the x-axis
plt.ylabel('Amplitude')       # label the y-axis

plt.tight_layout()            # auto-adjust spacing so labels don't overlap
plt.show()                    # display the figure
```
````

### Line-by-Line Explanation

| Line                              | What It Does                                                                                 |
| --------------------------------- | -------------------------------------------------------------------------------------------- |
| `import matplotlib.pyplot as plt` | Imports the plotting library and renames it `plt` for convenience.                           |
| `import numpy as np`              | Imports NumPy, a library for numerical operations and generating sample data.                |
| `x = np.linspace(0, 10, 100)`     | Creates 100 evenly spaced numbers between 0 and 10. Think of it as the time axis.            |
| `y1 = np.sin(x)`                  | Computes the sine of every number in `x`.                                                    |
| `y2 = np.cos(x)`                  | Computes the cosine of every number in `x`.                                                  |
| `plt.subplot(2, 1, 1)`            | Tells Matplotlib: "I want a grid with 2 rows and 1 column. Activate the **first** cell."     |
| `plt.plot(x, y1, 'r-')`           | Draws a line plot. `r` = red color, `-` = solid line style.                                  |
| `plt.title('Sine Wave')`          | Adds a title to the **currently active** subplot.                                            |
| `plt.xlabel('Time')`              | Labels the x-axis of the active subplot.                                                     |
| `plt.ylabel('Amplitude')`         | Labels the y-axis of the active subplot.                                                     |
| `plt.subplot(2, 1, 2)`            | Activates the **second** cell in the 2×1 grid.                                               |
| `plt.plot(x, y2, 'b-')`           | Draws the cosine wave in blue.                                                               |
| `plt.tight_layout()`              | **Crucial!** Automatically adds padding between subplots so titles and labels don't collide. |
| `plt.show()`                      | Renders the figure to your screen.                                                           |

---

## Method 2: `plt.subplots()` — The Professional Way

This is the approach you will see in real companies and data science teams. It returns two objects: a **Figure** (the canvas) and an array of **Axes** (the individual plots).

### Sample Code

```python
import matplotlib.pyplot as plt
import numpy as np

# Generate sample data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
revenue = [120, 135, 148, 162, 175, 190]
expenses = [90, 95, 100, 110, 115, 125]
profit = [30, 40, 48, 52, 60, 65]

# Create a figure and a 2x2 grid of subplots
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
# fig   = the entire canvas
# axes  = a 2x2 numpy array containing 4 Axes objects

# --- Subplot 1: Revenue Trend (Top-Left) ---
axes[0, 0].bar(months, revenue, color='green', alpha=0.7)
# axes[0, 0] targets the top-left subplot
# .bar() creates a bar chart
# alpha=0.7 makes the color slightly transparent
axes[0, 0].set_title('Monthly Revenue ($K)')
axes[0, 0].set_xlabel('Month')
axes[0, 0].set_ylabel('Revenue')

# --- Subplot 2: Expenses Trend (Top-Right) ---
axes[0, 1].bar(months, expenses, color='red', alpha=0.7)
axes[0, 1].set_title('Monthly Expenses ($K)')
axes[0, 1].set_xlabel('Month')
axes[0, 1].set_ylabel('Expenses')

# --- Subplot 3: Profit Trend (Bottom-Left) ---
axes[1, 0].plot(months, profit, marker='o', color='blue', linewidth=2)
# marker='o' puts a circle on every data point
# linewidth=2 makes the line thicker
axes[1, 0].set_title('Monthly Profit ($K)')
axes[1, 0].set_xlabel('Month')
axes[1, 0].set_ylabel('Profit')
axes[1, 0].grid(True, linestyle='--', alpha=0.5)
# grid(True) adds gridlines
# linestyle='--' makes them dashed
# alpha=0.5 makes them faint

# --- Subplot 4: Profit Margin (Bottom-Right) ---
margin = [(p / r) * 100 for p, r in zip(profit, revenue)]
# list comprehension: calculates profit margin % for each month
axes[1, 1].bar(months, margin, color='purple', alpha=0.7)
axes[1, 1].set_title('Profit Margin (%)')
axes[1, 1].set_xlabel('Month')
axes[1, 1].set_ylabel('Margin %')
axes[1, 1].axhline(y=25, color='orange', linestyle='--')
# axhline draws a horizontal reference line at y=25

# Adjust layout and add a super-title
plt.tight_layout()
fig.suptitle('Q1-Q2 Financial Dashboard', fontsize=16, y=1.02)
# suptitle adds a title for the ENTIRE figure
# y=1.02 pushes it slightly above the subplots
# fontsize=16 makes it larger than subplot titles

plt.show()
```

### Line-by-Line Explanation

| Line                                              | What It Does                                                                              |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `fig, axes = plt.subplots(2, 2, figsize=(10, 8))` | Creates a figure with a 2×2 grid. `figsize=(10, 8)` means 10 inches wide, 8 inches tall.  |
| `axes[0, 0]`                                      | Accesses the subplot in **row 0, column 0** (top-left).                                   |
| `.bar(months, revenue, ...)`                      | Draws vertical bars. `months` = x-positions, `revenue` = bar heights.                     |
| `.set_title(...)`                                 | Sets the title **on that specific Axes object**.                                          |
| `.set_xlabel(...)` / `.set_ylabel(...)`           | Labels the axes of that specific subplot.                                                 |
| `marker='o'`                                      | Adds circular markers at each data point on a line plot.                                  |
| `linewidth=2`                                     | Makes the plotted line 2 points thick.                                                    |
| `.grid(True, ...)`                                | Turns on background grid lines with custom style.                                         |
| `[(p / r) * 100 for ...]`                         | Python list comprehension — a compact loop that calculates profit margin for every month. |
| `.axhline(y=25, ...)`                             | Draws a horizontal dashed line at 25% to show a target benchmark.                         |
| `fig.suptitle(...)`                               | Adds one big title across the entire figure, not just one subplot.                        |
| `y=1.02`                                          | Moves the super-title slightly above the normal title area so it doesn't overlap.         |

---

## Method 3: `fig.add_subplot()` — The Object-Oriented Way

This method is useful when you want to add subplots **one at a time** or mix different grid sizes.

### Sample Code

```python
import matplotlib.pyplot as plt
import numpy as np

# Create a blank figure
fig = plt.figure(figsize=(10, 6))
# figure() creates an empty canvas with no subplots yet

# Add subplot 1: spans the top half (1 row, 2 columns, position 1)
ax1 = fig.add_subplot(1, 2, 1)
x = np.arange(5)
sales = [200, 220, 250, 270, 300]
ax1.bar(x, sales, color='teal')
ax1.set_xticks(x)
ax1.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])
ax1.set_title('Quarterly Sales')
ax1.set_ylabel('Sales ($K)')

# Add subplot 2: spans the bottom half (1 row, 2 columns, position 2)
ax2 = fig.add_subplot(1, 2, 2)
growth = [10, 13.6, 8, 11.1]
ax2.pie(growth, labels=['Q1→Q2', 'Q2→Q3', 'Q3→Q4', 'Q4→Q5'],
        autopct='%1.1f%%', startangle=90)
# pie() creates a pie chart
# autopct='%1.1f%%' prints the percentage inside each slice
# startangle=90 rotates the pie so the first slice starts at the top
ax2.set_title('Quarter-over-Quarter Growth')

plt.tight_layout()
plt.show()
```

### Line-by-Line Explanation

| Line                                | What It Does                                                            |
| ----------------------------------- | ----------------------------------------------------------------------- |
| `fig = plt.figure(figsize=(10, 6))` | Creates an empty figure canvas. No subplots exist yet.                  |
| `ax1 = fig.add_subplot(1, 2, 1)`    | Adds a subplot to the figure: 1 row, 2 columns, position 1 (left side). |
| `ax1.set_xticks(x)`                 | Explicitly tells the x-axis where to place tick marks.                  |
| `ax1.set_xticklabels([...])`        | Replaces numeric tick labels with custom text ('Q1', 'Q2', etc.).       |
| `ax2.pie(...)`                      | Creates a pie chart on the second Axes object.                          |
| `autopct='%1.1f%%'`                 | Formats the percentage text inside each slice to 1 decimal place.       |
| `startangle=90`                     | Rotates the pie chart so it starts at 12 o'clock.                       |

---

## Advanced Layouts

### Uneven Grids with `subplot2grid`

Sometimes you want one chart to be bigger than the others.

```python
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(10, 6))

# Create a 3x3 grid, but make this subplot span 2 rows and 2 columns
ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=2, rowspan=2)
x = np.linspace(0, 10, 100)
ax1.plot(x, np.sin(x))
ax1.set_title('Main Trend (Large)')

# Smaller subplot on the right
ax2 = plt.subplot2grid((3, 3), (0, 2), rowspan=1)
ax2.plot(x, np.cos(x), color='orange')
ax2.set_title('Cosine')

# Smaller subplot bottom-right
ax3 = plt.subplot2grid((3, 3), (1, 2), rowspan=1)
ax3.plot(x, np.tan(x), color='green')
ax3.set_title('Tangent')

# Bottom row spanning all columns
ax4 = plt.subplot2grid((3, 3), (2, 0), colspan=3)
ax4.bar(['A', 'B', 'C'], [10, 20, 15], color='purple')
ax4.set_title('Summary Bar Chart')

plt.tight_layout()
plt.show()
```

### Line-by-Line Explanation

| Line                                                     | What It Does                                                                                              |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `plt.subplot2grid((3, 3), (0, 0), colspan=2, rowspan=2)` | Creates a 3×3 invisible grid. Starts the subplot at row 0, col 0, and makes it span 2 columns and 2 rows. |
| `(3, 3)`                                                 | Defines a 3×3 grid of cells.                                                                              |
| `(0, 0)`                                                 | The starting cell (top-left).                                                                             |
| `colspan=2`                                              | The subplot stretches across 2 columns.                                                                   |
| `rowspan=2`                                              | The subplot stretches across 2 rows.                                                                      |

---

## Business Use Cases by Industry

### 1. E-Commerce / Retail

**Dashboard:** Website traffic, conversion rate, average order value, and cart abandonment rate in one view.

```python
fig, axes = plt.subplots(2, 2)
axes[0,0].plot(dates, traffic);      axes[0,0].set_title('Daily Visitors')
axes[0,1].plot(dates, conversion);    axes[0,1].set_title('Conversion Rate %')
axes[1,0].plot(dates, aov);           axes[1,0].set_title('Avg Order Value')
axes[1,1].plot(dates, abandonment); axes[1,1].set_title('Cart Abandonment %')
```

**Business Value:** Marketing teams spot correlations instantly. If traffic spikes but conversion drops, the landing page might be broken.

---

### 2. SaaS / Technology

**Dashboard:** Monthly Recurring Revenue (MRR), churn rate, new signups, and support ticket volume.

```python
fig, axes = plt.subplots(2, 2)
axes[0,0].bar(months, mrr);           axes[0,0].set_title('MRR ($)')
axes[0,1].bar(months, churn);         axes[0,1].set_title('Churn Rate %')
axes[1,0].plot(weeks, signups);      axes[1,0].set_title('New Signups')
axes[1,1].plot(weeks, tickets);      axes[1,1].set_title('Support Tickets')
```

**Business Value:** Executives see if growth is healthy. High churn + high tickets = product quality issue.

---

### 3. Finance / Banking

**Dashboard:** Stock price, trading volume, moving averages, and volatility.

```python
fig, axes = plt.subplots(2, 1, sharex=True)
axes[0].plot(dates, price);           axes[0].set_title('Stock Price')
axes[1].bar(dates, volume);           axes[1].set_title('Volume')
```

**Business Value:** Traders identify volume spikes that confirm price breakouts. `sharex=True` keeps both x-axes aligned perfectly.

---

### 4. Healthcare / Pharma

**Dashboard:** Patient admissions, treatment outcomes, cost per patient, and readmission rates by department.

```python
fig, axes = plt.subplots(2, 2)
axes[0,0].bar(depts, admissions);     axes[0,0].set_title('Admissions')
axes[0,1].bar(depts, outcomes);       axes[0,1].set_title('Success Rate %')
axes[1,0].bar(depts, cost);           axes[1,0].set_title('Cost per Patient')
axes[1,1].bar(depts, readmission);    axes[1,1].set_title('Readmission %')
```

**Business Value:** Hospital administrators identify departments where high costs do not correlate with better outcomes.

---

### 5. Manufacturing / Supply Chain

**Dashboard:** Production output, defect rate, machine downtime, and raw material cost.

```python
fig, axes = plt.subplots(2, 2)
axes[0,0].plot(days, output);          axes[0,0].set_title('Units Produced')
axes[0,1].plot(days, defects);        axes[0,1].set_title('Defect Rate %')
axes[1,0].barh(machines, downtime);  axes[1,0].set_title('Downtime (hrs)')
axes[1,1].plot(days, material_cost);  axes[1,1].set_title('Material Cost')
```

**Business Value:** Plant managers see if defect spikes align with specific machines or material cost increases.

---

## Common Beginner Mistakes

| Mistake                       | Why It Happens                                     | The Fix                                                               |
| ----------------------------- | -------------------------------------------------- | --------------------------------------------------------------------- |
| **Titles overlap**            | Subplots are too close together.                   | Always call `plt.tight_layout()` before `plt.show()`.                 |
| **All charts look the same**  | Forgetting to target the correct `axes` index.     | Double-check `axes[row, col]` matches the subplot you want.           |
| **X-axis labels are crowded** | Too many categories in a small space.              | Rotate labels: `ax.set_xticklabels(labels, rotation=45)`.             |
| **One subplot is empty**      | You created a grid but forgot to plot in one cell. | Ensure every `axes[r, c]` has a `.plot()`, `.bar()`, or similar call. |
| **Legend is cut off**         | The figure size is too small.                      | Increase `figsize=(width, height)` or use `plt.legend(loc='best')`.   |

---

## Quick Reference Cheat Sheet

```python
# --- BASIC SETUP ---
import matplotlib.pyplot as plt
import numpy as np

# --- CREATE SUBPLOTS ---
fig, axes = plt.subplots(2, 3, figsize=(12, 8))   # 2 rows, 3 cols
# axes is a 2D array: axes[row, col]

# --- PLOT ON A SPECIFIC SUBPLOT ---
axes[0, 0].plot(x, y)
axes[0, 0].bar(x, y)
axes[0, 0].scatter(x, y)
axes[0, 0].pie(values)
axes[0, 0].hist(data)

# --- LABELING ---
axes[0, 0].set_title('Title')
axes[0, 0].set_xlabel('X Axis')
axes[0, 0].set_ylabel('Y Axis')
axes[0, 0].legend(['Line 1', 'Line 2'])

# --- STYLING ---
axes[0, 0].grid(True, linestyle='--', alpha=0.5)
axes[0, 0].axhline(y=10, color='red', linestyle='--')   # horizontal line
axes[0, 0].axvline(x=5, color='blue', linestyle='--')   # vertical line

# --- SHARE AXES ---
fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)
# sharex=True: all subplots use the same x-axis scale
# sharey=True: all subplots use the same y-axis scale

# --- ADJUST SPACING ---
plt.tight_layout()          # automatic
plt.subplots_adjust(hspace=0.4, wspace=0.3)  # manual (height/width space)

# --- SUPER TITLE ---
fig.suptitle('Overall Dashboard Title', fontsize=16)

# --- SAVE INSTEAD OF SHOW ---
plt.savefig('dashboard.png', dpi=300, bbox_inches='tight')
# dpi=300 = high resolution for printing
# bbox_inches='tight' = trims extra whitespace

# --- SHOW ---
plt.show()
```

---

## Summary Checklist for Beginners

- [ ] Import `matplotlib.pyplot as plt` and `numpy as np`
- [ ] Prepare your data before plotting
- [ ] Choose your method: `plt.subplot()` for quick tests, `plt.subplots()` for real work
- [ ] Use `axes[row, col]` to target the correct subplot
- [ ] Add `.set_title()`, `.set_xlabel()`, and `.set_ylabel()` to every subplot
- [ ] Call `plt.tight_layout()` before `plt.show()`
- [ ] Use `fig.suptitle()` for an overall figure title
- [ ] Use `figsize=(width, height)` to control the total figure size

---

_Happy Plotting! 🎨_

```

```
