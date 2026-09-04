# 📊 Comprehensive Guide to Scatter Plots with Matplotlib & Pandas

> **Perfect for beginners** — every concept explained step-by-step with real business use cases.

---

## Table of Contents

1. [What is a Scatter Plot?](#1-what-is-a-scatter-plot)
2. [When Should You Use a Scatter Plot?](#2-when-should-you-use-a-scatter-plot)
3. [Setting Up Your Environment](#3-setting-up-your-environment)
4. [Your First Scatter Plot with Matplotlib](#4-your-first-scatter-plot-with-matplotlib)
5. [Scatter Plots with Pandas DataFrames](#5-scatter-plots-with-pandas-dataframes)
6. [Customizing Your Scatter Plot](#6-customizing-your-scatter-plot)
7. [Advanced: Multiple Data Series](#7-advanced-multiple-data-series)
8. [Real-World Business Use Cases](#8-real-world-business-use-cases)
9. [Common Mistakes to Avoid](#9-common-mistakes-to-avoid)
10. [Quick Reference Cheat Sheet](#10-quick-reference-cheat-sheet)

---

## 1. What is a Scatter Plot?

A **scatter plot** (also called a scatter diagram or scatter graph) is a type of data visualization that displays values for **two variables** as a collection of points on a 2D plane.

- Each point represents a single observation (e.g., one customer, one product, one day).
- The **horizontal axis (X-axis)** represents one variable.
- The **vertical axis (Y-axis)** represents another variable.

### Why Scatter Plots Matter

Scatter plots help you:

- **Identify relationships** between two variables (correlation)
- **Spot outliers** or unusual data points
- **Detect patterns** or clusters in your data
- **Communicate findings** to stakeholders visually

> 💡 **Think of it like this:** If you plotted every student's "hours studied" vs. "exam score," a scatter plot would instantly show you whether studying more leads to better grades.

---

## 2. When Should You Use a Scatter Plot?

| ✅ Use a Scatter Plot When...                   | ❌ Don't Use a Scatter Plot When...                           |
| ----------------------------------------------- | ------------------------------------------------------------- |
| You have **two continuous numeric variables**   | You have only **one variable** (use a histogram or bar chart) |
| You want to see if variables are **related**    | You want to show **parts of a whole** (use a pie chart)       |
| You want to **compare groups** using color/size | You want to show **trends over time** (use a line chart)      |
| You want to **find outliers** in your data      | Your data is **categorical** (use a bar chart)                |

---

## 3. Setting Up Your Environment

Before we start plotting, you need to install and import the required libraries.

### Step 1: Install Libraries (if not already installed)

```bash
pip install matplotlib pandas numpy
```

### Step 2: Import Libraries

```python
import matplotlib.pyplot as plt   # For creating plots
import pandas as pd               # For data manipulation
import numpy as np                # For numerical operations
```

| Library             | Purpose                                                           |
| ------------------- | ----------------------------------------------------------------- |
| `matplotlib.pyplot` | The main plotting library in Python. `plt` is the standard alias. |
| `pandas`            | Handles data in tables (like Excel). `pd` is the standard alias.  |
| `numpy`             | Works with arrays and math. `np` is the standard alias.           |

---

## 4. Your First Scatter Plot with Matplotlib

Let's start with the simplest possible scatter plot.

### Complete Code Example

```python
# Step 1: Import the plotting library
import matplotlib.pyplot as plt

# Step 2: Create sample data
# x-values: hours of study
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# y-values: exam scores
y = [45, 50, 55, 60, 65, 70, 75, 85, 90, 95]

# Step 3: Create the scatter plot
plt.scatter(x, y)

# Step 4: Add labels and title
plt.xlabel("Hours Studied")
plt.ylabel("Exam Score")
plt.title("Study Hours vs Exam Score")

# Step 5: Display the plot
plt.show()
```

### 🔍 Line-by-Line Explanation

| Line | Code                                     | What It Does                                                                                                                       |
| ---- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 1    | `import matplotlib.pyplot as plt`        | Imports Matplotlib's plotting module and gives it the short name `plt` so we don't have to type the full name every time.          |
| 4    | `x = [1, 2, 3, ...]`                     | Creates a Python **list** containing the X-axis values (hours studied).                                                            |
| 6    | `y = [45, 50, 55, ...]`                  | Creates a Python **list** containing the Y-axis values (exam scores). Each value pairs with the corresponding X value.             |
| 9    | `plt.scatter(x, y)`                      | **The core command.** Tells Matplotlib to create a scatter plot using `x` for horizontal positions and `y` for vertical positions. |
| 12   | `plt.xlabel("Hours Studied")`            | Adds a text label below the X-axis to explain what the horizontal values represent.                                                |
| 13   | `plt.ylabel("Exam Score")`               | Adds a text label beside the Y-axis to explain what the vertical values represent.                                                 |
| 14   | `plt.title("Study Hours vs Exam Score")` | Adds a title at the top of the plot to describe what the chart is about.                                                           |
| 17   | `plt.show()`                             | **Renders and displays** the plot in a window. Without this, the plot won't appear!                                                |

### What the Output Looks Like

You'll see a graph with 10 dots. Each dot represents one student. The dots trend upward from left to right, showing that more study hours correlate with higher exam scores.

---

## 5. Scatter Plots with Pandas DataFrames

In the real world, data comes in tables — not simple lists. That's where **pandas** shines.

### What is a DataFrame?

A **DataFrame** is like an Excel spreadsheet in Python. It has:

- **Rows** = individual records (e.g., each customer)
- **Columns** = variables or features (e.g., age, salary, purchases)

### Complete Code Example

```python
# Step 1: Import libraries
import pandas as pd
import matplotlib.pyplot as plt

# Step 2: Create a DataFrame with sample data
data = {
    "Employee_ID": [101, 102, 103, 104, 105, 106, 107, 108],
    "Years_Experience": [1, 2, 3, 4, 5, 6, 7, 8],
    "Salary_Thousands": [35, 40, 48, 55, 62, 70, 78, 85],
    "Department": ["Sales", "Sales", "IT", "IT", "HR", "HR", "Sales", "IT"]
}

df = pd.DataFrame(data)

# Step 3: Create a scatter plot from the DataFrame
plt.scatter(df["Years_Experience"], df["Salary_Thousands"])

# Step 4: Add labels and title
plt.xlabel("Years of Experience")
plt.ylabel("Salary (in Thousands)")
plt.title("Experience vs Salary")

# Step 5: Show the plot
plt.show()
```

### 🔍 Line-by-Line Explanation

| Line | Code                                                          | What It Does                                                                                                                                                   |
| ---- | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1-2  | `import pandas as pd`                                         | Imports pandas for data handling. `pd` is the standard shortcut.                                                                                               |
| 5-11 | `data = {...}`                                                | Creates a Python **dictionary** where keys are column names and values are lists of data.                                                                      |
| 13   | `df = pd.DataFrame(data)`                                     | Converts the dictionary into a pandas **DataFrame** — a structured table. Now `df` holds all our data.                                                         |
| 16   | `plt.scatter(df["Years_Experience"], df["Salary_Thousands"])` | Extracts the "Years_Experience" column as X-values and "Salary_Thousands" as Y-values, then plots them. The `df["ColumnName"]` syntax selects a single column. |
| 19   | `plt.xlabel("Years of Experience")`                           | Labels the X-axis.                                                                                                                                             |
| 20   | `plt.ylabel("Salary (in Thousands)")`                         | Labels the Y-axis.                                                                                                                                             |
| 21   | `plt.title("Experience vs Salary")`                           | Adds a descriptive title.                                                                                                                                      |
| 24   | `plt.show()`                                                  | Displays the final plot.                                                                                                                                       |

### 💡 Pro Tip: Using DataFrame's Built-in Plot Method

Pandas DataFrames have a built-in `.plot()` method that uses Matplotlib behind the scenes:

```python
# Alternative way — shorter and cleaner!
df.plot(kind="scatter", x="Years_Experience", y="Salary_Thousands",
        title="Experience vs Salary", xlabel="Years of Experience",
        ylabel="Salary (in Thousands)")
plt.show()
```

| Parameter                  | What It Does                                                   |
| -------------------------- | -------------------------------------------------------------- |
| `kind="scatter"`           | Tells pandas to make a scatter plot (not a line or bar chart). |
| `x="Years_Experience"`     | Specifies which column goes on the X-axis.                     |
| `y="Salary_Thousands"`     | Specifies which column goes on the Y-axis.                     |
| `title=...`                | Sets the chart title directly.                                 |
| `xlabel=...`, `ylabel=...` | Sets axis labels directly.                                     |

---

## 6. Customizing Your Scatter Plot

Plain scatter plots are informative, but **customization** makes them professional and easier to read.

### 6.1 Changing Point Color and Size

```python
import matplotlib.pyplot as plt

# Data
x = [10, 20, 30, 40, 50, 60, 70, 80]
y = [15, 25, 35, 30, 55, 60, 75, 85]

# Create scatter plot with customizations
plt.scatter(x, y,
            color="red",           # Point color
            s=100,                 # Point size (pixels)
            alpha=0.7,             # Transparency (0 = invisible, 1 = fully opaque)
            edgecolors="black",    # Border color around each point
            linewidths=1.5)        # Border thickness

plt.xlabel("Marketing Spend ($000s)")
plt.ylabel("Revenue ($000s)")
plt.title("Marketing Spend vs Revenue")
plt.show()
```

### 🔍 Customization Parameters Explained

| Parameter        | Value Example                  | What It Controls                                                                       |
| ---------------- | ------------------------------ | -------------------------------------------------------------------------------------- |
| `color` (or `c`) | `"red"`, `"#FF5733"`, `"blue"` | The fill color of each point. Can be a color name, hex code, or RGB value.             |
| `s`              | `100`, `50`, `200`             | The **size** of each point in square pixels. Larger number = bigger dot.               |
| `alpha`          | `0.0` to `1.0`                 | **Transparency.** `0.7` means 70% opaque, 30% see-through. Useful when points overlap. |
| `edgecolors`     | `"black"`, `"white"`           | The **outline color** of each point. Helps points stand out.                           |
| `linewidths`     | `1`, `2`, `0.5`                | The **thickness** of the point's outline.                                              |
| `marker`         | `"o"`, `"s"`, `"^"`, `"D"`     | The **shape** of the point. `"o"` = circle, `"s"` = square, `"^"` = triangle.          |

### 6.2 Common Marker Styles

```python
plt.scatter(x, y, marker="s")   # Square
plt.scatter(x, y, marker="^")   # Triangle (pointing up)
plt.scatter(x, y, marker="D")   # Diamond
plt.scatter(x, y, marker="*")   # Star
plt.scatter(x, y, marker="x")   # X shape
```

### 6.3 Adding a Grid for Readability

```python
plt.scatter(x, y, color="blue", s=80)
plt.grid(True, linestyle="--", alpha=0.5)  # Adds a dashed, semi-transparent grid
plt.xlabel("X Values")
plt.ylabel("Y Values")
plt.title("Scatter Plot with Grid")
plt.show()
```

| `plt.grid()` Parameter | Effect                                                                 |
| ---------------------- | ---------------------------------------------------------------------- |
| `True` / `False`       | Turns the grid on or off.                                              |
| `linestyle="--"`       | Makes grid lines dashed. Other options: `"-"` (solid), `":"` (dotted). |
| `alpha=0.5`            | Makes grid lines 50% transparent so they don't overpower the data.     |

---

## 7. Advanced: Multiple Data Series

Often, you want to compare **groups** on the same plot. For example: comparing Sales vs. IT department salaries.

### Method 1: Using Separate `plt.scatter()` Calls

```python
import matplotlib.pyplot as plt
import pandas as pd

# Create sample data
df = pd.DataFrame({
    "Experience": [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
    "Salary": [35, 42, 50, 58, 65, 38, 48, 60, 72, 85],
    "Department": ["Sales", "Sales", "Sales", "Sales", "Sales",
                   "IT", "IT", "IT", "IT", "IT"]
})

# Filter data by department
sales = df[df["Department"] == "Sales"]
it = df[df["Department"] == "IT"]

# Plot each department separately
plt.scatter(sales["Experience"], sales["Salary"],
            color="blue", label="Sales", s=100, marker="o")
plt.scatter(it["Experience"], it["Salary"],
            color="red", label="IT", s=100, marker="s")

# Add legend, labels, and title
plt.legend()                              # Shows the color key (Sales vs IT)
plt.xlabel("Years of Experience")
plt.ylabel("Salary ($000s)")
plt.title("Salary Comparison: Sales vs IT")
plt.grid(True, alpha=0.3)
plt.show()
```

### 🔍 Line-by-Line Explanation

| Line | Code                                                                                  | What It Does                                                                                                                                          |
| ---- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| 11   | `sales = df[df["Department"] == "Sales"]`                                             | **Filters** the DataFrame to keep ONLY rows where Department is "Sales". This creates a smaller DataFrame called `sales`.                             |
| 12   | `it = df[df["Department"] == "IT"]`                                                   | Same filtering, but for the IT department.                                                                                                            |
| 15   | `plt.scatter(sales["Experience"], sales["Salary"], color="blue", label="Sales", ...)` | Plots the Sales data points in **blue circles**. The `label` parameter is crucial — it tells the legend what to call this series.                     |
| 17   | `plt.scatter(it["Experience"], it["Salary"], color="red", label="IT", ...)`           | Plots the IT data points in **red squares**.                                                                                                          |
| 21   | `plt.legend()`                                                                        | **Creates the legend box** that maps colors/shapes to their labels ("Sales" and "IT"). Without this, your audience won't know which color means what! |

### Method 2: Using a Color Map (Automatic Coloring)

```python
import matplotlib.pyplot as plt
import pandas as pd

# Data with a numeric category
df = pd.DataFrame({
    "Ad_Spend": [10, 20, 30, 40, 50, 15, 25, 35, 45, 55],
    "Revenue": [12, 28, 35, 48, 60, 18, 32, 42, 55, 70],
    "Customer_Satisfaction": [3, 4, 5, 6, 7, 4, 5, 6, 7, 8]  # 3rd variable!
})

# Color points by Customer Satisfaction score
scatter = plt.scatter(df["Ad_Spend"], df["Revenue"],
                      c=df["Customer_Satisfaction"],   # Color based on this column
                      cmap="viridis",                   # Color scheme
                      s=150,
                      edgecolors="black")

# Add a color bar (legend for continuous colors)
plt.colorbar(scatter, label="Customer Satisfaction Score")

plt.xlabel("Ad Spend ($000s)")
plt.ylabel("Revenue ($000s)")
plt.title("Ad Spend vs Revenue (Colored by Satisfaction)")
plt.show()
```

### 🔍 Explanation of Color Mapping

| Parameter                       | What It Does                                                                                                                              |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `c=df["Customer_Satisfaction"]` | Sets the **color** of each point based on the value in the "Customer_Satisfaction" column. Low values = one color, high values = another. |
| `cmap="viridis"`                | Chooses the **color palette**. Popular options: `"viridis"`, `"plasma"`, `"coolwarm"`, `"RdYlGn"`.                                        |
| `plt.colorbar(scatter, ...)`    | Adds a **vertical color scale** on the side showing what color corresponds to what value.                                                 |

---

## 8. Real-World Business Use Cases

Scatter plots aren't just academic exercises — they drive real business decisions. Here are practical examples:

### 🏢 Use Case 1: Retail — Price vs. Sales Volume

**Question:** Does lowering the price always increase sales?

```python
import pandas as pd
import matplotlib.pyplot as plt

# Product data
products = pd.DataFrame({
    "Product": ["A", "B", "C", "D", "E", "F", "G", "H"],
    "Price": [10, 15, 20, 25, 30, 35, 40, 45],
    "Units_Sold": [500, 450, 400, 350, 300, 200, 150, 100]
})

plt.scatter(products["Price"], products["Units_Sold"],
            color="green", s=120, edgecolors="black")
plt.xlabel("Price ($)")
plt.ylabel("Units Sold")
plt.title("Product Price vs Units Sold")
plt.grid(True, alpha=0.3)
plt.show()
```

**Business Insight:** The downward trend shows that as price increases, units sold decrease. This helps the pricing team find the **optimal price point** that maximizes total revenue (Price × Units).

---

### 🏢 Use Case 2: Marketing — Ad Spend vs. Customer Acquisition

**Question:** Are we spending our marketing budget efficiently?

```python
import pandas as pd
import matplotlib.pyplot as plt

# Monthly marketing data
marketing = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Ad_Spend": [5000, 7000, 6000, 9000, 8000, 10000],
    "New_Customers": [120, 180, 150, 250, 210, 280]
})

plt.scatter(marketing["Ad_Spend"], marketing["New_Customers"],
            color="purple", s=150, marker="D", edgecolors="black")

# Add month labels to each point
for i, month in enumerate(marketing["Month"]):
    plt.annotate(month,
                 (marketing["Ad_Spend"][i], marketing["New_Customers"][i]),
                 textcoords="offset points",
                 xytext=(0, 10),
                 ha='center')

plt.xlabel("Ad Spend ($)")
plt.ylabel("New Customers Acquired")
plt.title("Marketing Spend vs Customer Acquisition")
plt.grid(True, alpha=0.3)
plt.show()
```

**Business Insight:** The strong upward trend indicates good ROI on ad spend. The annotation shows which month performed best (June). If a point fell far below the trend line, it would signal a problem to investigate.

---

### 🏢 Use Case 3: HR — Employee Engagement vs. Performance Rating

**Question:** Does employee engagement correlate with performance?

```python
import pandas as pd
import matplotlib.pyplot as plt

# Employee survey data
employees = pd.DataFrame({
    "Employee": ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"],
    "Engagement_Score": [3.2, 4.1, 2.8, 4.5, 3.9, 2.5, 4.8, 3.5],
    "Performance_Rating": [3.0, 4.2, 2.5, 4.8, 4.0, 2.2, 4.9, 3.6],
    "Department": ["Sales", "IT", "Sales", "HR", "IT", "Sales", "HR", "IT"]
})

# Color by department
colors = {"Sales": "red", "IT": "blue", "HR": "green"}
for dept in employees["Department"].unique():
    subset = employees[employees["Department"] == dept]
    plt.scatter(subset["Engagement_Score"], subset["Performance_Rating"],
                color=colors[dept], label=dept, s=120, edgecolors="black")

plt.legend(title="Department")
plt.xlabel("Engagement Score (1-5)")
plt.ylabel("Performance Rating (1-5)")
plt.title("Employee Engagement vs Performance by Department")
plt.grid(True, alpha=0.3)
plt.show()
```

**Business Insight:** The tight clustering along the diagonal shows that higher engagement scores strongly predict better performance. HR can use this to justify investment in engagement programs. The color coding reveals whether any department is an outlier.

---

### 🏢 Use Case 4: E-Commerce — Website Traffic vs. Conversion Rate

**Question:** Does more traffic always mean more sales?

```python
import pandas as pd
import matplotlib.pyplot as plt

# Daily website data
daily_data = pd.DataFrame({
    "Day": range(1, 31),
    "Visitors": [1200, 1500, 1100, 1800, 2000, 1700, 1300, 1600, 1900, 2200,
                 1400, 2100, 2300, 1800, 1600, 2000, 2400, 1700, 1500, 1900,
                 2100, 2500, 1800, 1600, 1400, 2000, 2200, 2600, 1900, 1700],
    "Conversion_Rate": [2.1, 2.5, 1.9, 2.8, 3.0, 2.6, 2.0, 2.4, 2.9, 3.2,
                        2.2, 3.1, 3.3, 2.7, 2.5, 3.0, 3.4, 2.6, 2.3, 2.8,
                        3.1, 3.5, 2.7, 2.4, 2.1, 2.9, 3.2, 3.6, 2.8, 2.5]
})

plt.scatter(daily_data["Visitors"], daily_data["Conversion_Rate"],
            color="orange", s=80, alpha=0.7, edgecolors="black")
plt.xlabel("Daily Website Visitors")
plt.ylabel("Conversion Rate (%)")
plt.title("Website Traffic vs Conversion Rate")
plt.grid(True, alpha=0.3)
plt.show()
```

**Business Insight:** If the points form an upward trend, it means higher traffic days also have better conversion. If they're scattered randomly, traffic quality (not quantity) might be the issue.

---

### 🏢 Use Case 5: Finance — Risk vs. Return on Investment

**Question:** What's the risk-return profile of our investments?

```python
import pandas as pd
import matplotlib.pyplot as plt

# Portfolio data
portfolio = pd.DataFrame({
    "Asset": ["Stock A", "Stock B", "Stock C", "Bond A", "Bond B",
              "REIT A", "Crypto", "Gold", "Fund A", "Fund B"],
    "Risk": [15, 22, 18, 5, 4, 12, 45, 8, 14, 16],
    "Return": [8, 12, 10, 3, 2.5, 7, 25, 4, 9, 11]
})

# Size points by a 3rd variable (investment amount)
investment_size = [100, 150, 80, 200, 180, 120, 50, 90, 130, 110]

plt.scatter(portfolio["Risk"], portfolio["Return"],
            s=[x * 3 for x in investment_size],  # Scale for visibility
            c=portfolio["Return"],
            cmap="RdYlGn",
            alpha=0.7,
            edgecolors="black")

# Label each point
for i, asset in enumerate(portfolio["Asset"]):
    plt.annotate(asset,
                 (portfolio["Risk"][i], portfolio["Return"][i]),
                 textcoords="offset points",
                 xytext=(5, 5),
                 fontsize=8)

plt.xlabel("Risk (Volatility %)")
plt.ylabel("Annual Return (%)")
plt.title("Investment Risk vs Return")
plt.colorbar(label="Return (%)")
plt.grid(True, alpha=0.3)
plt.show()
```

**Business Insight:** Investors want assets in the **top-left** (high return, low risk). Assets in the **bottom-right** (low return, high risk) are poor investments. Bubble size shows how much capital is allocated to each asset.

---

## 9. Common Mistakes to Avoid

| Mistake                                     | Why It's Wrong                                                              | How to Fix It                                                     |
| ------------------------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| **Forgetting `plt.show()`**                 | The plot code runs but nothing appears on screen.                           | Always end with `plt.show()`.                                     |
| **Mismatched X and Y lengths**              | `x` has 5 values but `y` has 6. Matplotlib throws an error.                 | Ensure both lists/arrays have the same number of elements.        |
| **Using strings for numeric axes**          | Numbers stored as text (e.g., `"10"` instead of `10`) won't plot correctly. | Convert to numeric: `df["column"] = pd.to_numeric(df["column"])`. |
| **Overlapping points without transparency** | When many points overlap, you can't see density.                            | Use `alpha=0.5` to make points semi-transparent.                  |
| **No labels or title**                      | Stakeholders can't understand what the chart shows.                         | Always add `plt.xlabel()`, `plt.ylabel()`, and `plt.title()`.     |
| **Wrong chart type**                        | Using a scatter plot for time-series data.                                  | Use a line chart (`plt.plot()`) for data over time.               |

---

## 10. Quick Reference Cheat Sheet

```python
import matplotlib.pyplot as plt
import pandas as pd

# BASIC SCATTER PLOT
plt.scatter(x, y)

# WITH PANDAS
plt.scatter(df["column_x"], df["column_y"])

# CUSTOMIZATION
plt.scatter(x, y,
            color="red",        # Point color
            s=100,              # Point size
            alpha=0.7,          # Transparency (0-1)
            marker="o",         # Shape: o, s, ^, D, *, x
            edgecolors="black", # Border color
            linewidths=1)       # Border width

# MULTIPLE SERIES
plt.scatter(x1, y1, color="blue", label="Group A")
plt.scatter(x2, y2, color="red", label="Group B")
plt.legend()

# COLOR MAP (3rd variable)
plt.scatter(x, y, c=z, cmap="viridis")
plt.colorbar(label="Z Values")

# LABELS & TITLE
plt.xlabel("X Axis Label")
plt.ylabel("Y Axis Label")
plt.title("Chart Title")

# GRID
plt.grid(True, linestyle="--", alpha=0.5)

# DISPLAY
plt.show()
```

---

## Summary

| Concept             | Key Takeaway                                                                 |
| ------------------- | ---------------------------------------------------------------------------- |
| **Scatter plots**   | Show relationships between two numeric variables.                            |
| **Matplotlib**      | Use `plt.scatter(x, y)` to create the plot.                                  |
| **Pandas**          | Use `df.plot(kind="scatter", x="col1", y="col2")` for DataFrames.            |
| **Customization**   | Control color, size, transparency, and shape with parameters.                |
| **Multiple series** | Call `plt.scatter()` multiple times and use `plt.legend()`.                  |
| **Business value**  | Scatter plots reveal correlations, outliers, and optimization opportunities. |

---

> 🎓 **Practice Exercise:** Try creating a scatter plot with your own data. Start simple, then add one customization at a time (color, then size, then a legend). The best way to learn is by doing!

---

_Happy Plotting! 📈_
