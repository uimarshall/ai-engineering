# Matplotlib: A Comprehensive Beginner's Guide

## Table of Contents

1. [What is Matplotlib?](#what-is-matplotlib)
2. [Why Do Companies Use Data Visualization?](#why-do-companies-use-data-visualization)
3. [Getting Started: Your First Plot](#getting-started-your-first-plot)
4. [Core Concepts Every Beginner Must Know](#core-concepts-every-beginner-must-know)
5. [Types of Plots and When to Use Them](#types-of-plots-and-when-to-use-them)
6. [Styling and Customization](#styling-and-customization)
7. [Saving and Exporting Plots](#saving-and-exporting-plots)
8. [Real-World Company Use Cases](#real-world-company-use-cases)
9. [Best Practices for Business Visualizations](#best-practices-for-business-visualizations)
10. [Common Mistakes to Avoid](#common-mistakes-to-avoid)

---

## What is Matplotlib?

**Matplotlib** is Python's most popular library for creating static, animated, and interactive visualizations. Think of it as a digital art studio where your data is the paint and Matplotlib is the brush that turns numbers into pictures.

It was created by John D. Hunter in 2003 and has since become the foundation of Python's data visualization ecosystem. Many other libraries (like Seaborn and Pandas plotting) are actually built on top of Matplotlib.

### The Two Interfaces

Matplotlib has two ways of working — this confuses many beginners:

1. **`pyplot` (plt)** — The "easy" way. Great for quick, simple plots.
2. **Object-Oriented API** — The "professional" way. Gives you full control.

Think of `pyplot` like using a point-and-shoot camera, while the Object-Oriented API is like a professional DSLR with manual settings. We'll show you both!

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
```

---

## Why Do Companies Use Data Visualization?

Before we write code, let's understand **why** this matters in a real company:

| Business Need             | How Visualization Helps                           |
| ------------------------- | ------------------------------------------------- |
| **Track Revenue**         | Line charts show sales trends over time           |
| **Understand Customers**  | Bar charts compare customer segments              |
| **Find Problems**         | Scatter plots reveal unusual patterns (outliers)  |
| **Present to Leadership** | Clean charts communicate faster than spreadsheets |
| **Monitor Operations**    | Dashboards show real-time metrics                 |
| **Predict the Future**    | Trend lines help forecast next quarter's sales    |

> **The Golden Rule:** A picture is worth a thousand spreadsheet cells. Executives don't have time to read raw numbers — they need to _see_ the story.

---

## Getting Started: Your First Plot

### Example 1: The Simplest Line Chart

Imagine you tracked your company's monthly sales for 6 months:

```python
import matplotlib.pyplot as plt

# Data: months and sales in thousands
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
sales = [45, 52, 48, 61, 58, 67]

# Create the plot
plt.plot(months, sales)

# Add labels (always do this!)
plt.title('Company Sales - First Half 2024')
plt.xlabel('Month')
plt.ylabel('Sales ($ Thousands)')

# Show the plot
plt.show()
```

**What just happened?**

- `plt.plot()` draws a line connecting your data points
- `plt.title()`, `plt.xlabel()`, `plt.ylabel()` add text so people understand what they're looking at
- `plt.show()` displays the chart

---

### Example 2: Your First Bar Chart

Bar charts are perfect for comparing categories:

```python
products = ['Laptop', 'Phone', 'Tablet', 'Watch', 'Headphones']
units_sold = [120, 340, 180, 250, 410]

plt.bar(products, units_sold, color='steelblue')
plt.title('Units Sold by Product - Q3 2024')
plt.xlabel('Product')
plt.ylabel('Units Sold')
plt.show()
```

---

## Core Concepts Every Beginner Must Know

### 1. Figure and Axes (The Canvas and the Frame)

This is the **most important concept** in Matplotlib. Understand this, and everything else becomes easy.

```python
# Create a Figure (the blank canvas) and Axes (the drawing area)
fig, ax = plt.subplots(figsize=(8, 5))

# Now draw on the axes
ax.plot(months, sales, marker='o', linewidth=2, color='green')

# Add labels using the axes object
ax.set_title('Monthly Sales Performance', fontsize=14, fontweight='bold')
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Revenue ($K)', fontsize=12)

# Add grid for readability
ax.grid(True, linestyle='--', alpha=0.7)

plt.show()
```

**Analogy:**

- **Figure** = The entire sheet of paper
- **Axes** = The actual box where the graph is drawn (you can have multiple on one figure!)
- **Axis** = The x and y lines with numbers (not the same as Axes!)

---

### 2. Multiple Plots in One Figure

Companies often need to compare several metrics side by side:

```python
# Create 2 rows, 1 column of plots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# First plot: Sales trend
ax1.plot(months, sales, color='blue', marker='o')
ax1.set_title('Monthly Sales')
ax1.set_ylabel('Revenue ($K)')
ax1.grid(True, alpha=0.3)

# Second plot: Profit margin
profit_margin = [12, 15, 14, 18, 16, 20]
ax2.plot(months, profit_margin, color='green', marker='s')
ax2.set_title('Profit Margin %')
ax2.set_ylabel('Percentage (%)')
ax2.set_xlabel('Month')
ax2.grid(True, alpha=0.3)

# Adjust spacing between plots
plt.tight_layout()
plt.show()
```

---

### 3. Working with Pandas DataFrames

In real companies, your data comes from CSVs, Excel files, or databases — usually as a pandas DataFrame:

```python
# Sample company data
data = {
    'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    'revenue': [45000, 52000, 48000, 61000, 58000, 67000],
    'expenses': [32000, 35000, 33000, 38000, 36000, 40000],
    'customers': [1200, 1350, 1280, 1500, 1420, 1600]
}
df = pd.DataFrame(data)

# Plot directly from DataFrame
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(df['month'], df['revenue'], label='Revenue', marker='o', linewidth=2)
ax.plot(df['month'], df['expenses'], label='Expenses', marker='s', linewidth=2)

ax.set_title('Revenue vs Expenses - 2024', fontsize=14)
ax.set_xlabel('Month')
ax.set_ylabel('Amount ($)')
ax.legend()  # Shows the labels!
ax.grid(True, alpha=0.3)

plt.show()
```

---

## Types of Plots and When to Use Them

### 1. Line Plot — Trends Over Time

**Use when:** Tracking something that changes continuously (sales over months, stock prices, website traffic).

```python
# Company stock price over 30 days
days = range(1, 31)
stock_price = [100 + 2*d + np.random.normal(0, 5) for d in days]

plt.figure(figsize=(12, 5))
plt.plot(days, stock_price, color='navy', linewidth=1.5)
plt.fill_between(days, stock_price, alpha=0.2, color='navy')
plt.title('Stock Price Movement - 30 Days')
plt.xlabel('Day')
plt.ylabel('Price ($)')
plt.grid(True, alpha=0.3)
plt.show()
```

---

### 2. Bar Chart — Comparing Categories

**Use when:** Comparing values across different groups (sales by region, performance by employee).

```python
# Sales by region
regions = ['North', 'South', 'East', 'West', 'Central']
regional_sales = [450, 380, 520, 410, 290]

fig, ax = plt.subplots(figsize=(8, 5))

# Horizontal bar chart (great for long labels)
bars = ax.barh(regions, regional_sales, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])

# Add value labels on bars
for bar in bars:
    width = bar.get_width()
    ax.text(width + 10, bar.get_y() + bar.get_height()/2,
            f'${width}K', ha='left', va='center')

ax.set_title('Sales by Region - 2024', fontsize=14)
ax.set_xlabel('Sales ($ Thousands)')
ax.set_xlim(0, 600)
plt.show()
```

---

### 3. Scatter Plot — Relationships Between Variables

**Use when:** Exploring if two things are related (advertising spend vs sales, experience vs salary).

```python
# Marketing: Ad spend vs Sales generated
np.random.seed(42)
ad_spend = np.random.randint(1000, 10000, 50)
sales_generated = ad_spend * 3.5 + np.random.normal(0, 5000, 50)

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(ad_spend, sales_generated, alpha=0.6, color='purple', edgecolors='black')

ax.set_title('Advertising Spend vs Sales Generated')
ax.set_xlabel('Ad Spend ($)')
ax.set_ylabel('Sales Generated ($)')
ax.grid(True, alpha=0.3)

# Add trend line
z = np.polyfit(ad_spend, sales_generated, 1)
p = np.poly1d(z)
ax.plot(ad_spend, p(ad_spend), "r--", alpha=0.8, label='Trend')
ax.legend()

plt.show()
```

---

### 4. Histogram — Distribution of Data

**Use when:** Understanding how data is spread out (customer ages, order values, employee salaries).

```python
# Customer order values
np.random.seed(42)
order_values = np.random.normal(75, 25, 1000)  # Mean $75, Std $25

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(order_values, bins=30, color='teal', edgecolor='white', alpha=0.8)

ax.set_title('Distribution of Customer Order Values')
ax.set_xlabel('Order Value ($)')
ax.set_ylabel('Number of Orders')
ax.axvline(np.mean(order_values), color='red', linestyle='--', linewidth=2, label=f'Mean: ${np.mean(order_values):.2f}')
ax.legend()
plt.show()
```

---

### 5. Pie Chart — Proportions

**Use when:** Showing parts of a whole (market share, budget allocation, survey responses).

```python
# Market share
companies = ['Our Company', 'Competitor A', 'Competitor B', 'Competitor C', 'Others']
market_share = [35, 25, 20, 12, 8]
colors = ['#2ecc71', '#e74c3c', '#3498db', '#f39c12', '#95a5a6']

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(market_share, labels=companies, autopct='%1.1f%%',
                                   colors=colors, startangle=90, explode=(0.05, 0, 0, 0, 0))

ax.set_title('Q3 Market Share', fontsize=14, fontweight='bold')
plt.show()
```

> **⚠️ Warning:** Pie charts can be hard to read with many slices. Use them sparingly and only with 2-6 categories.

---

### 6. Box Plot — Statistical Summary

**Use when:** Comparing distributions and spotting outliers (salary ranges by department, delivery times by courier).

```python
# Delivery times by shipping method (in hours)
np.random.seed(42)
standard = np.random.normal(72, 12, 100)
express = np.random.normal(24, 4, 100)
overnight = np.random.normal(12, 2, 100)

fig, ax = plt.subplots(figsize=(8, 6))
ax.boxplot([standard, express, overnight], labels=['Standard', 'Express', 'Overnight'])
ax.set_title('Delivery Time by Shipping Method')
ax.set_ylabel('Hours')
ax.grid(True, alpha=0.3, axis='y')
plt.show()
```

---

## Styling and Customization

### Colors and Styles

```python
# Available styles
print(plt.style.available)
# ['Solarize_Light2', '_classic_test_patch', 'bmh', 'classic', 'dark_background',
#  'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn', ...]

# Apply a professional style
plt.style.use('seaborn-v0_8-whitegrid')

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(months, sales, marker='o', markersize=8, linewidth=2.5, color='#e74c3c')
ax.set_title('Sales with Professional Styling', fontsize=16)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Revenue ($K)', fontsize=12)
plt.show()
```

### Adding Annotations

```python
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(months, sales, marker='o', linewidth=2, color='blue')

# Highlight the best month
best_month_idx = sales.index(max(sales))
ax.annotate('Best Month!
Launch Campaign',
            xy=(months[best_month_idx], sales[best_month_idx]),
            xytext=(months[best_month_idx], sales[best_month_idx] + 10),
            arrowprops=dict(arrowstyle='->', color='red'),
            fontsize=11, color='red', fontweight='bold')

ax.set_title('Monthly Sales with Annotation')
ax.set_xlabel('Month')
ax.set_ylabel('Sales ($K)')
plt.show()
```

---

## Saving and Exporting Plots

In a company, you'll need to save plots for reports, presentations, and emails:

```python
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(months, sales, marker='o', linewidth=2)
ax.set_title('Monthly Sales Report')
ax.set_xlabel('Month')
ax.set_ylabel('Sales ($K)')

# Save as high-resolution PNG for reports
plt.savefig('monthly_sales.png', dpi=300, bbox_inches='tight')

# Save as PDF for presentations (vector format, never pixelates!)
plt.savefig('monthly_sales.pdf', bbox_inches='tight')

# Save as SVG for websites
plt.savefig('monthly_sales.svg', bbox_inches='tight')

plt.show()
```

**Key parameters:**

- `dpi=300` — High resolution for print quality
- `bbox_inches='tight'` — Removes extra white space around the plot
- `transparent=True` — Transparent background (great for presentations)

---

## Real-World Company Use Cases

### Use Case 1: Executive Dashboard — Monthly KPI Tracking

**Scenario:** The CEO wants a one-page dashboard showing key metrics every month.

```python
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Executive Dashboard - August 2024', fontsize=16, fontweight='bold')

# Revenue trend
months_full = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
revenue = [450, 480, 520, 510, 580, 620, 650, 680]
axes[0, 0].plot(months_full, revenue, marker='o', color='green', linewidth=2)
axes[0, 0].set_title('Revenue Trend ($K)')
axes[0, 0].grid(True, alpha=0.3)

# Customer acquisition
new_customers = [120, 135, 150, 142, 180, 195, 210, 225]
axes[0, 1].bar(months_full, new_customers, color='steelblue')
axes[0, 1].set_title('New Customers')
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Churn rate
churn_rate = [5.2, 4.8, 5.0, 4.5, 4.2, 3.9, 3.8, 3.5]
axes[1, 0].plot(months_full, churn_rate, marker='s', color='red', linewidth=2)
axes[1, 0].set_title('Churn Rate (%)')
axes[1, 0].grid(True, alpha=0.3)

# Top products
top_products = ['Laptop Pro', 'Phone X', 'Tablet Air', 'Watch Series']
product_sales = [320, 450, 180, 210]
axes[1, 1].pie(product_sales, labels=top_products, autopct='%1.0f%%', startangle=90)
axes[1, 1].set_title('Sales by Product')

plt.tight_layout(rect=[0, 0, 1, 0.96])  # Make room for the suptitle
plt.savefig('executive_dashboard.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

### Use Case 2: Sales Team — Regional Performance Comparison

**Scenario:** The sales director needs to compare quarterly performance across regions to decide where to allocate next year's budget.

```python
# Quarterly data by region
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
north = [120, 135, 150, 165]
south = [100, 110, 125, 140]
east = [140, 155, 170, 185]
west = [90, 95, 110, 125]

x = np.arange(len(quarters))
width = 0.2

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - 1.5*width, north, width, label='North', color='#1f77b4')
ax.bar(x - 0.5*width, south, width, label='South', color='#ff7f0e')
ax.bar(x + 0.5*width, east, width, label='East', color='#2ca02c')
ax.bar(x + 1.5*width, west, width, label='West', color='#d62728')

ax.set_title('Quarterly Sales by Region ($K)', fontsize=14)
ax.set_xlabel('Quarter')
ax.set_ylabel('Sales ($K)')
ax.set_xticks(x)
ax.set_xticklabels(quarters)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

plt.savefig('regional_performance.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

### Use Case 3: Marketing — A/B Test Results

**Scenario:** The marketing team ran two versions of an email campaign. They need to visualize which performed better.

```python
# A/B Test results
days = range(1, 8)
variant_a = [120, 145, 160, 155, 170, 185, 190]
variant_b = [110, 130, 175, 180, 195, 210, 225]

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(days, variant_a, marker='o', label='Variant A (Original)', linewidth=2, color='blue')
ax.plot(days, variant_b, marker='s', label='Variant B (New Design)', linewidth=2, color='green')

ax.fill_between(days, variant_a, variant_b, where=[b > a for a, b in zip(variant_a, variant_b)],
                alpha=0.2, color='green', label='B Advantage')

ax.set_title('Email Campaign A/B Test - Click-through Rates', fontsize=14)
ax.set_xlabel('Day')
ax.set_ylabel('Clicks')
ax.legend()
ax.grid(True, alpha=0.3)

plt.savefig('ab_test_results.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

### Use Case 4: Finance — Budget vs Actual Spending

**Scenario:** The finance department tracks whether departments are staying within budget.

```python
departments = ['HR', 'IT', 'Marketing', 'Sales', 'Operations', 'R&D']
budget = [200, 500, 400, 600, 350, 450]
actual = [195, 520, 380, 610, 340, 480]

x = np.arange(len(departments))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - width/2, budget, width, label='Budget', color='lightblue', edgecolor='navy')
bars2 = ax.bar(x + width/2, actual, width, label='Actual', color='salmon', edgecolor='darkred')

# Color actual bars red if over budget
for i, (b, a) in enumerate(zip(budget, actual)):
    if a > b:
        bars2[i].set_color('#e74c3c')
        bars2[i].set_edgecolor('darkred')

ax.set_title('Department Budget vs Actual Spending ($K)', fontsize=14)
ax.set_xlabel('Department')
ax.set_ylabel('Amount ($K)')
ax.set_xticks(x)
ax.set_xticklabels(departments)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
ax.axhline(0, color='black', linewidth=0.8)

plt.savefig('budget_vs_actual.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

### Use Case 5: Operations — Website Traffic Monitoring

**Scenario:** The operations team monitors website traffic to detect issues or viral moments.

```python
# Hourly website traffic over a day
hours = list(range(24))
traffic = [120, 80, 50, 30, 25, 40, 150, 450, 800, 950, 880, 920,
           850, 780, 820, 900, 1100, 1300, 1250, 1100, 950, 700, 450, 250]

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(hours, traffic, color='#3498db', linewidth=2)
ax.fill_between(hours, traffic, alpha=0.3, color='#3498db')

# Highlight peak hours
peak_start, peak_end = 17, 20
ax.axvspan(peak_start, peak_end, alpha=0.2, color='red', label='Peak Hours')

ax.set_title('Website Traffic - 24 Hour Overview', fontsize=14)
ax.set_xlabel('Hour of Day')
ax.set_ylabel('Visitors')
ax.set_xticks(hours)
ax.legend()
ax.grid(True, alpha=0.3)

plt.savefig('traffic_monitoring.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

### Use Case 6: Product — Feature Usage Analytics

**Scenario:** The product team wants to understand which app features users engage with most.

```python
features = ['Search', 'Profile', 'Messages', 'Settings', 'Checkout', 'Recommendations']
usage_percent = [95, 78, 65, 45, 82, 70]
colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(features)))

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(features, usage_percent, color=colors)

# Add percentage labels
for bar, pct in zip(bars, usage_percent):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            f'{pct}%', va='center', fontsize=11)

ax.set_title('Feature Usage Rate - Active Users (%)', fontsize=14)
ax.set_xlabel('Percentage of Users')
ax.set_xlim(0, 105)
ax.grid(True, alpha=0.3, axis='x')

plt.savefig('feature_usage.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

## Best Practices for Business Visualizations

### 1. Always Label Everything

```python
# ❌ Bad - What is this?
plt.plot(x, y)
plt.show()

# ✅ Good - Anyone can understand this
plt.plot(x, y, label='Monthly Revenue')
plt.title('Company Revenue Growth 2024')
plt.xlabel('Month')
plt.ylabel('Revenue ($ Millions)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 2. Choose the Right Chart Type

| What You Want to Show              | Best Chart Type           |
| ---------------------------------- | ------------------------- |
| Change over time                   | Line chart                |
| Compare categories                 | Bar chart                 |
| Parts of a whole                   | Pie chart (use sparingly) |
| Relationship between two variables | Scatter plot              |
| Distribution of data               | Histogram / Box plot      |
| Composition over time              | Stacked bar / Area chart  |

### 3. Keep It Simple

```python
# ❌ Bad - Chart junk
plt.plot(x, y, color='hotpink', linestyle='-.', marker='D', markersize=15,
         markerfacecolor='yellow', markeredgecolor='black', markeredgewidth=2)

# ✅ Good - Clean and professional
plt.plot(x, y, color='#2c3e50', linewidth=2, marker='o', markersize=6)
```

### 4. Use Consistent Colors

```python
# Define a company color palette
company_colors = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'danger': '#d62728',
    'neutral': '#7f7f7f'
}

# Use them consistently across all company reports
ax.plot(x, y, color=company_colors['primary'])
ax.axhline(target, color=company_colors['danger'], linestyle='--')
```

### 5. Add Context with Annotations

Always explain unusual data points:

```python
ax.annotate('Black Friday Sale', xy=(11, 950), xytext=(8, 1100),
            arrowprops=dict(arrowstyle='->', color='red'),
            fontsize=10, color='red')
```

---

## Common Mistakes to Avoid

| Mistake                     | Why It Hurts                                      | The Fix                                |
| --------------------------- | ------------------------------------------------- | -------------------------------------- |
| **No labels or title**      | Nobody knows what the chart means                 | Always add `title`, `xlabel`, `ylabel` |
| **Using 3D charts**         | They distort perception and look unprofessional   | Stick to 2D                            |
| **Too many colors**         | Looks chaotic and unprofessional                  | Use 2-4 colors maximum                 |
| **Wrong chart type**        | Bar charts for trends, line charts for categories | Match chart to data story              |
| **Missing legends**         | When multiple lines/bars exist                    | Always call `plt.legend()`             |
| **Not saving plots**        | Lost work, can't share                            | Use `plt.savefig()` with high DPI      |
| **Forgetting `plt.show()`** | Plot doesn't display in some environments         | Always include it                      |
| **Overloading one chart**   | Too much data = confusion                         | Use subplots or separate charts        |

---

## Quick Reference Cheat Sheet

```python
import matplotlib.pyplot as plt
import numpy as np

# BASIC PLOTS
plt.plot(x, y)              # Line plot
plt.scatter(x, y)           # Scatter plot
plt.bar(x, y)               # Vertical bar chart
plt.barh(x, y)              # Horizontal bar chart
plt.hist(data, bins=20)     # Histogram
plt.pie(values, labels=...)  # Pie chart
plt.boxplot(data)           # Box plot

# LABELS & TITLES
plt.title('Title')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.legend()
plt.grid(True)

# STYLING
plt.style.use('seaborn-v0_8-whitegrid')
plt.figure(figsize=(10, 6))
plt.savefig('plot.png', dpi=300, bbox_inches='tight')

# OBJECT-ORIENTED (RECOMMENDED)
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y)
ax.set_title('Title')
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.show()

# MULTIPLE PLOTS
fig, axes = plt.subplots(2, 2, figsize=(12, 10))  # 2 rows, 2 columns
axes[0, 0].plot(x, y)
axes[0, 1].bar(x, y)
axes[1, 0].scatter(x, y)
axes[1, 1].hist(data)
plt.tight_layout()
plt.show()
```

---

## Summary

Matplotlib is the backbone of data visualization in Python. For a beginner in a company setting, remember these key points:

1. **Start simple** — `plt.plot()` and `plt.bar()` will cover 80% of your needs
2. **Always label** — Unlabeled charts are useless in business
3. **Use the Object-Oriented API** — It gives you the control you need for professional reports
4. **Save in high resolution** — Your charts will end up in PowerPoint presentations
5. **Tell a story** — Every chart should answer a business question

> **The ultimate goal of business visualization:** Turn raw data into insights that drive decisions.

---

_Happy plotting! 📊_
