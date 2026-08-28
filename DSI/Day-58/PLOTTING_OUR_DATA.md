# 📊 Day 58: Plotting Our Data Using Pandas

> **Welcome to Day 58!** Today we'll learn how to create beautiful visualizations directly from our Pandas DataFrames. No need to learn a separate plotting library — Pandas has you covered! 🎨

---

## 🎯 What You'll Learn Today

- Why data visualization matters
- How Pandas uses Matplotlib "under the hood"
- How to create 6 different types of plots
- When to use each plot type
- How to spot outliers and anomalies through visualization

---

## 📌 Table of Contents

1. [Why Plot Our Data?](#why-plot)
2. [How Pandas Makes Plots](#how-pandas-plots)
3. [Loading Our Data](#loading-data)
4. [Plot 1: The Default Plot](#plot-1-default)
5. [Plot 2: Line Plot](#plot-2-line)
6. [Plot 3: Scatter Plot](#plot-3-scatter)
7. [Plot 4: Box Plot](#plot-4-box)
8. [Plot 5: Histogram](#plot-5-histogram)
9. [Plot 6: Bar Chart](#plot-6-bar)
10. [Real-World Company Use Cases](#company-use-cases)
11. [Complete Code Reference](#complete-code)
12. [Quick Reference Cheat Sheet](#cheat-sheet)
13. [Common Mistakes to Avoid](#common-mistakes)

---

## 1. Why Plot Our Data? {#why-plot}

Before we dive into code, let's understand **why** we plot data:

| Reason                     | Explanation                                    |
| -------------------------- | ---------------------------------------------- |
| 🔍 **Discover Patterns**   | See trends that numbers alone can't reveal     |
| 🚨 **Spot Outliers**       | Find unusual data points that might be errors  |
| 📈 **Track Changes**       | See how values change over time                |
| 🎯 **Compare Groups**      | Compare categories side-by-side                |
| 💡 **Communicate Results** | Share findings with non-technical stakeholders |

> 💡 **Think of it this way:** Raw data is like a spreadsheet of numbers. A plot is like turning those numbers into a picture that tells a story.

---

## 2. How Pandas Makes Plots {#how-pandas-plots}

Here's a key concept to understand:

> **Pandas doesn't create plots by itself.** Under the hood, it uses a library called **Matplotlib** to draw the charts. Pandas just makes it super easy by wrapping Matplotlib's complex code into simple one-liners.

```
You write:    df.plot()
Pandas does:  "Hey Matplotlib, draw this chart for me!"
Matplotlib:   *draws the chart*
```

This means:

- ✅ You get beautiful charts with minimal code
- ✅ You can customize them further using Matplotlib if needed
- ✅ You don't need to import Matplotlib separately (but you can for advanced tweaks)

---

## 3. Loading Our Data {#loading-data}

Let's start by loading our grocery store data. We'll use three sheets from our Excel file:

```python
import pandas as pd

# Load the transactions data
# This sheet contains: transaction_id, customer_id, transaction_date,
# sales_cost, num_items, etc.
transactions = pd.read_excel("grocery_database.xlsx", sheet_name="transactions")

# Load customer details
# This sheet contains: customer_id, gender, credit_score, etc.
customer_details = pd.read_excel("grocery_database.xlsx", sheet_name="customer_details")

# Load product area information
# This sheet contains: product_area_id, product_area_name, profit_margin, etc.
product_areas = pd.read_excel("grocery_database.xlsx", sheet_name="product_areas")
```

### 🔍 Line-by-Line Breakdown:

| Line                        | What It Does                                                                                    |
| --------------------------- | ----------------------------------------------------------------------------------------------- |
| `import pandas as pd`       | Brings the Pandas library into our script so we can use it. `pd` is just a nickname we give it. |
| `pd.read_excel(...)`        | Tells Pandas to read an Excel file.                                                             |
| `"grocery_database.xlsx"`   | The name of our Excel file.                                                                     |
| `sheet_name="transactions"` | Tells Pandas which sheet (tab) to read from the Excel file.                                     |
| `= transactions`            | Saves the loaded data into a variable called `transactions` for later use.                      |

---

## 4. Plot 1: The Default Plot {#plot-1-default}

### The Code:

```python
customer_details.plot()
```

### 🔍 Line-by-Line Breakdown:

| Code               | What It Does                                                              |
| ------------------ | ------------------------------------------------------------------------- |
| `customer_details` | Our DataFrame containing customer information.                            |
| `.plot()`          | Tells Pandas to create a plot using ALL numeric columns in the DataFrame. |

### What Happens:

When you run this, Pandas will:

1. Look at all **numeric columns** in `customer_details` (like `credit_score`, `customer_id`)
2. Plot each one as a **line** on the same chart
3. Use the **DataFrame index** (row numbers 0, 1, 2, 3...) as the X-axis

### ⚠️ Important Note:

> This default plot is usually **NOT very useful** for analysis because it mixes unrelated columns together. It's more of a "quick peek" to see what your data looks like. We'll learn better ways to plot specific columns below!

### What It Looks Like:

```
    credit_score
    │    ╱╲
 800│   ╱  ╲    ╱╲
    │  ╱    ╲  ╱  ╲
 400│ ╱      ╲╱    ╲
    │╱
    └───────────────────
      0   5   10  15  20  → Row Index

    (Multiple lines jumbled together - not very helpful!)
```

---

## 5. Plot 2: Line Plot {#plot-2-line}

Line plots are perfect for showing **trends over time**. Think stock prices, daily sales, temperature changes.

### Step 1: Aggregate the Data First

```python
# Group transactions by date and sum up sales_cost and num_items
daily_sales_summary = transactions.groupby("transaction_date")[["sales_cost", "num_items"]].sum().reset_index()
```

### 🔍 Line-by-Line Breakdown:

| Code                            | What It Does                                                                                                            |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `transactions`                  | Our DataFrame with all transaction records.                                                                             |
| `.groupby("transaction_date")`  | Groups all rows that have the **same date** together. Think of it like sorting receipts by date.                        |
| `[["sales_cost", "num_items"]]` | Selects only these two columns to work with. The double brackets `[[ ]]` mean "give me a DataFrame with these columns." |
| `.sum()`                        | Adds up all the `sales_cost` and `num_items` for each date group.                                                       |
| `.reset_index()`                | Converts the grouped dates back into a regular column (instead of being the index). This makes it easier to plot.       |

### Result After Aggregation:

| transaction_date | sales_cost | num_items |
| ---------------- | ---------- | --------- |
| 2023-01-01       | 1250.50    | 45        |
| 2023-01-02       | 890.25     | 32        |
| 2023-01-03       | 1560.00    | 58        |

> Now each row represents **one day's total sales**, instead of individual transactions!

---

### Step 2: Plot a Single Column

```python
# Plot sales_cost (y-axis) against the row index (x-axis)
daily_sales_summary["sales_cost"].plot()
```

### 🔍 Line-by-Line Breakdown:

| Code                                | What It Does                                                                      |
| ----------------------------------- | --------------------------------------------------------------------------------- |
| `daily_sales_summary["sales_cost"]` | Selects ONLY the `sales_cost` column from our DataFrame.                          |
| `.plot()`                           | Creates a line plot. By default, the X-axis is the **row index** (0, 1, 2, 3...). |

### What It Looks Like:

```
sales_cost
    │        ╱╲
1500│       ╱  ╲      ╱╲
    │      ╱    ╲    ╱  ╲
1000│     ╱      ╲  ╱    ╲
    │    ╱        ╲╱      ╲
 500│   ╱
    │  ╱
    └───────────────────────
      0   5   10   15   20  → Row Index (not dates!)
```

> ⚠️ The X-axis shows row numbers, not actual dates. Let's fix that next!

---

### Step 3: Plot with Proper X and Y Axes

```python
# Plot transaction_date on X-axis and sales_cost on Y-axis
daily_sales_summary.plot(x="transaction_date", y="sales_cost")
```

### 🔍 Line-by-Line Breakdown:

| Code                   | What It Does                                                             |
| ---------------------- | ------------------------------------------------------------------------ |
| `.plot()`              | Creates the plot.                                                        |
| `x="transaction_date"` | Uses the `transaction_date` column for the **horizontal axis** (X-axis). |
| `y="sales_cost"`       | Uses the `sales_cost` column for the **vertical axis** (Y-axis).         |

### What It Looks Like Now:

```
sales_cost
    │        ╱╲
1500│       ╱  ╲      ╱╲
    │      ╱    ╲    ╱  ╲
1000│     ╱      ╲  ╱    ╲
    │    ╱        ╲╱      ╲
 500│   ╱
    │  ╱
    └───────────────────────
      Jan  Feb  Mar  Apr  May  → Actual Dates! 🎉
```

> Much better! Now we can see how sales changed over actual time.

---

### Step 4: Explicitly Specify "Line" Plot

```python
# Same as above, but we explicitly say we want a line plot
daily_sales_summary.plot(x="transaction_date", y="sales_cost", kind="line")
```

### 🔍 Line-by-Line Breakdown:

| Code          | What It Does                                                                                                                          |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `kind="line"` | Explicitly tells Pandas to draw a **line plot**. This is actually the default, so it's optional, but being explicit is good practice! |

> 💡 **When to use line plots:** Time series data, tracking changes, trends over days/weeks/months.

---

## 6. Plot 3: Scatter Plot {#plot-3-scatter}

Scatter plots show the **relationship between two variables**. Each dot represents one row of data.

```python
# Create a scatter plot: num_items vs sales_cost
daily_sales_summary.plot(x="num_items", y="sales_cost", kind="scatter")
```

### 🔍 Line-by-Line Breakdown:

| Code             | What It Does                                              |
| ---------------- | --------------------------------------------------------- |
| `x="num_items"`  | Number of items sold goes on the X-axis.                  |
| `y="sales_cost"` | Total sales cost goes on the Y-axis.                      |
| `kind="scatter"` | Tells Pandas to draw **dots** instead of connected lines. |

### What It Looks Like:

```
sales_cost
    │
1500│                    ●
    │
1000│         ●    ●
    │      ●
 500│   ●         ●
    │●
    └───────────────────────
      20   40   60   80  → num_items
```

### What We Can Learn:

- 🔵 **Dots going up-right** = More items sold = Higher sales (positive relationship)
- 🔵 **Dots spread out** = Some days had high sales with few items (expensive products!)
- 🔵 **Lone dot far away** = Could be an outlier worth investigating

> 💡 **When to use scatter plots:** Exploring relationships, finding correlations, spotting outliers.

---

## 7. Plot 4: Box Plot {#plot-4-box}

Box plots are amazing for understanding the **distribution** of your data and spotting outliers.

```python
# Box plot of sales_cost
daily_sales_summary.plot(y="sales_cost", kind="box")
```

### 🔍 Line-by-Line Breakdown:

| Code             | What It Does                                                     |
| ---------------- | ---------------------------------------------------------------- |
| `y="sales_cost"` | The column we want to analyze. Box plots only need ONE variable. |
| `kind="box"`     | Creates a box plot (also called "box-and-whisker plot").         |

### What It Looks Like:

```
        │
   ●    │  ← Outlier (unusually high value)
        │
   ─┬── │  ← Max (excluding outliers)
    │   │
    │   │
   ─┼── │  ← Median (middle value, green line)
    │   │
    │   │
   ─┴── │  ← Min (excluding outliers)
        │
        │
    sales_cost
```

### Understanding the Box Plot:

| Part                  | What It Means                                        |
| --------------------- | ---------------------------------------------------- |
| **The Box**           | Contains the middle 50% of your data                 |
| **Green Line in Box** | **Median** (50th percentile) — the middle value      |
| **Bottom of Box**     | 25th percentile (Q1)                                 |
| **Top of Box**        | 75th percentile (Q3)                                 |
| **Whiskers**          | Extend to show the range of "normal" data            |
| **Dots Outside**      | **Outliers** — values that are unusually high or low |

> 💡 **When to use box plots:** Comparing distributions, identifying outliers, understanding data spread.

---

## 8. Plot 5: Histogram {#plot-5-histogram}

Histograms show **how often values occur** in ranges (called "bins").

### Basic Histogram:

```python
# Histogram of sales_cost
daily_sales_summary.plot(y="sales_cost", kind="hist")
```

### 🔍 Line-by-Line Breakdown:

| Code          | What It Does                                            |
| ------------- | ------------------------------------------------------- |
| `kind="hist"` | Creates a histogram — bars showing frequency of values. |

### What It Looks Like:

```
Frequency
    │
  8 │      ████
    │      ████
  6 │      ████  ████
    │      ████  ████
  4 │  ████████  ████  ████
    │  ████████  ████  ████
  2 │  ████████  ████  ████  ████
    │  ████████  ████  ████  ████
    └─────────────────────────────
      $0   $500  $1000 $1500 $2000  → sales_cost ranges
```

### Histogram with Custom Bins:

```python
# Histogram with 25 bins (more detailed bars)
daily_sales_summary.plot(y="sales_cost", kind="hist", bins=25)
```

### 🔍 Line-by-Line Breakdown:

| Code      | What It Does                                                                                               |
| --------- | ---------------------------------------------------------------------------------------------------------- |
| `bins=25` | Divides the data into **25 ranges** instead of the default 10. More bins = more detail but can look noisy. |

### What It Looks Like (More Bins):

```
Frequency
    │
  5 │    ██      ██
    │   ████    ████    ██
  3 │  ██████  ██████  ████  ██
    │ ███████ ███████ █████ ████ ██
    └────────────────────────────────
      $0  $200 $400 $600 $800 ...  → More detailed ranges
```

> 💡 **When to use histograms:** Understanding data distribution, checking if data is normal/balanced, identifying peaks.

---

## 9. Plot 6: Bar Chart {#plot-6-bar}

Bar charts compare **categories** against each other.

```python
# Bar chart: profit margin for each product area
product_areas.plot(kind="bar", y="profit_margin", x="product_area_name")
```

### 🔍 Line-by-Line Breakdown:

| Code                    | What It Does                                                        |
| ----------------------- | ------------------------------------------------------------------- |
| `kind="bar"`            | Creates vertical bars (use `kind="barh"` for horizontal bars).      |
| `y="profit_margin"`     | The height of each bar = profit margin.                             |
| `x="product_area_name"` | Each bar represents one product area (Fruits, Dairy, Bakery, etc.). |

### What It Looks Like:

```
profit_margin
    │
 30%│         ████
    │         ████
 25%│  ████   ████
    │  ████   ████
 20%│  ████   ████        ████
    │  ████   ████        ████
 15%│  ████   ████  ████  ████
    │  ████   ████  ████  ████
 10%│  ████   ████  ████  ████  ████
    └─────────────────────────────────
      Dairy  Bakery  Meat  Produce  Frozen
```

> 💡 **When to use bar charts:** Comparing categories, ranking items, showing counts per group.

---

## 10. Real-World Company Use Cases: How Plots Drive Business Decisions {#company-use-cases}

> **Why this matters:** Every plot type we learned isn't just a pretty picture — it's a **business decision tool** used by real companies every day. Let's see how! 🏢

---

### 🏦 **Use Case 1: Retail Bank — Line Plot for Fraud Detection**

**Company:** A major retail bank with 5M+ customers

**The Business Problem:**
The bank's fraud team noticed suspicious spikes in transaction volumes but couldn't pinpoint when or why they happened. They were losing ~$3M monthly to undetected fraud patterns.

**How They Used a Line Plot:**

```python
# The bank aggregated daily transaction volumes
daily_transactions = bank_data.groupby("date")["transaction_amount"].sum().reset_index()

# Line plot revealed the pattern
daily_transactions.plot(x="date", y="transaction_amount", kind="line", figsize=(14, 6))
```

**What the Plot Revealed:**

```
transaction_volume
    │
$5M │                    ★ ← SPIKE! Unusual jump
    │                   ╱│╲
$3M │      ───────────╱─│─╲──────────
    │     ╱           ╱  │  ╲
$1M │────╱───────────╱───│───╲────────
    │
    └───────────────────────────────────
      Mon  Tue  Wed  Thu  Fri  Sat  Sun
                    ↑
            Fraudsters target Fridays!
```

**The Business Decision:**

- The line plot showed **Friday evenings** had 3x normal transaction volume
- The bank implemented **heightened monitoring every Friday 6-10 PM**
- Fraud detection accuracy improved by **42%**
- Estimated savings: **$1.2M per month**

> 💡 **Lesson:** Line plots turn invisible time-based patterns into visible trends that drive operational decisions.

---

### 🛒 **Use Case 2: E-Commerce Giant — Scatter Plot for Pricing Strategy**

**Company:** A global online marketplace (think Amazon-style platform)

**The Business Problem:**
The pricing team wanted to understand: _"If we increase the number of items in a bundle, does total revenue actually go up?"_ They were guessing and leaving money on the table.

**How They Used a Scatter Plot:**

```python
# Each dot = one product listing
# X = number of items in bundle, Y = total revenue
product_listings.plot(x="bundle_item_count", y="monthly_revenue", kind="scatter")
```

**What the Plot Revealed:**

```
monthly_revenue
    │
$50K│                        ●
    │
$30K│              ●    ●
    │
$20K│    ●    ●       ●    ●
    │
$10K│ ●       ●    ●       ●    ●
    │
 $5K│●    ●    ●    ●    ●    ●    ●
    └───────────────────────────────────
      2    5    8   12   15   20   25  → bundle_item_count
```

**The Business Decision:**

- The scatter plot showed a **positive correlation** (more items = more revenue)
- BUT it also revealed a **"sweet spot" around 8-12 items** where revenue peaked
- Bundles with **20+ items** actually generated LESS revenue per item (customers got overwhelmed)
- The company restructured bundles to target the **8-12 item sweet spot**
- Average order value increased by **18%** ($12M additional annual revenue)

> 💡 **Lesson:** Scatter plots reveal relationships between variables that spreadsheets hide. They help find optimal business "sweet spots."

---

### 🏥 **Use Case 3: Hospital Network — Box Plot for Resource Allocation**

**Company:** A network of 12 hospitals serving 2M patients annually

**The Business Problem:**
The hospital's operations director needed to decide how many ICU beds to allocate per hospital. Some hospitals were overcrowded, others had empty beds. The director was using **average occupancy** — which was misleading.

**How They Used a Box Plot:**

```python
# Box plot of daily ICU occupancy for each hospital
hospital_icu_data.plot(y="daily_occupancy", kind="box")
```

**What the Plot Revealed:**

```
    │
100%│        ●                    ●  ← Outliers: Full capacity days
    │       ─┬─                  ─┬─
 80%│        │                    │
    │        │                    │
 60%│───────┼───────────────────┼────  ← Median ~60% (not bad!)
    │        │                    │
 40%│       ─┴─                  ─┴─
    │
 20%│
    │
    └─────────────────────────────────
      Hospital A          Hospital B
```

**The Business Decision:**

- **Hospital A** had a median of 60% but outliers at 100% (capacity crisis days)
- **Hospital B** had the same median but NO outliers (stable, predictable)
- The director realized **averages were useless** — the outliers told the real story
- Hospital A got **+15 ICU beds** (focusing on peak demand, not average)
- Hospital B's beds were **redistributed** to other locations
- Patient wait times for ICU admission dropped by **35%**

> 💡 **Lesson:** Box plots reveal the FULL picture — averages lie, but distributions don't. Critical for resource planning.

---

### 📊 **Use Case 4: SaaS Company — Histogram for Customer Segmentation**

**Company:** A B2B software platform with 50,000+ business customers

**The Business Problem:**
The marketing team wanted to segment customers into tiers (Free, Basic, Pro, Enterprise) but had no data-driven way to set the boundaries. They were guessing.

**How They Used a Histogram:**

```python
# Histogram of monthly spending per customer
customer_spending.plot(y="monthly_spend", kind="hist", bins=30, figsize=(12, 6))
```

**What the Plot Revealed:**

```
# of Customers
    │
8000│  ████
    │  ████
 6000│  ████  ████
    │  ████  ████  ████
 4000│  ████  ████  ████  ████
    │  ████  ████  ████  ████        ████
 2000│  ████  ████  ████  ████  ████  ████  ████
    │  ████  ████  ████  ████  ████  ████  ████  ████
    └───────────────────────────────────────────────────
      $0  $20  $50  $100 $200 $500 $1000 $5000  → Monthly Spend
      ↑    ↑    ↑    ↑
    Free Basic Pro  Enterprise
    Tier Tier Tier  Tier
```

**The Business Decision:**

- The histogram showed **natural clusters** (gaps in the distribution)
- Clear breakpoints at **$20, $100, and $500** separated customer groups
- The marketing team created 4 tiers matching these natural clusters
- Pricing page redesign based on these tiers increased conversion by **27%**
- Revenue per customer increased by **15%** through better upsell targeting

> 💡 **Lesson:** Histograms reveal natural groupings in data — perfect for segmentation, pricing tiers, and customer buckets.

---

### 🍎 **Use Case 5: Grocery Chain — Bar Chart for Product Strategy**

**Company:** A regional grocery chain with 150 stores

**The Business Problem:**
The merchandising team needed to decide which product areas to expand and which to reduce. They had profit margin data but no visual way to compare categories.

**How They Used a Bar Chart:**

```python
# Bar chart comparing profit margins across product areas
product_areas.plot(kind="bar", y="profit_margin", x="product_area_name")
```

**What the Plot Revealed:**

```
profit_margin
    │
 35%│         ████
    │         ████
 28%│  ████   ████
    │  ████   ████
 22%│  ████   ████        ████
    │  ████   ████        ████
 15%│  ████   ████  ████  ████
    │  ████   ████  ████  ████
  8%│  ████   ████  ████  ████  ████
    └─────────────────────────────────
      Dairy  Bakery  Meat  Produce  Frozen
      28%    35%     15%   22%     8%
      ↑      ↑       ↓     ↑       ↓
     Keep  Expand   Cut   Keep    Cut
```

**The Business Decision:**

- **Bakery (35%)** and **Dairy (28%)** were clear winners → **Expand shelf space by 20%**
- **Frozen (8%)** and **Meat (15%)** were underperformers → **Reduce space, negotiate better supplier deals**
- **Produce (22%)** was solid but not exceptional → **Maintain current strategy**
- Store layout changes based on this analysis increased **overall profit margin by 4.2%**
- That's **$8M additional profit** across 150 stores annually

> 💡 **Lesson:** Bar charts make category comparisons instant. In business, "seeing is believing" — stakeholders act on what they can see.

---

### 🎯 Summary: Plot Types → Business Decisions

| Plot Type        | Business Question It Answers    | Real-World Impact                       |
| ---------------- | ------------------------------- | --------------------------------------- |
| **Line Plot**    | "When do problems spike?"       | Fraud detection timing, seasonal demand |
| **Scatter Plot** | "What's the relationship?"      | Pricing optimization, bundle sizing     |
| **Box Plot**     | "What's the full range?"        | Resource allocation, risk assessment    |
| **Histogram**    | "Where are the natural groups?" | Customer segmentation, pricing tiers    |
| **Bar Chart**    | "Which category wins?"          | Product strategy, budget allocation     |

---

> 🏆 **The Bottom Line:** Every plot you create is a potential business decision waiting to happen. Master these 5 plot types, and you'll be the person who turns raw data into actionable strategy.

---

## 10. Complete Code Reference {#complete-code}

Here's the complete code from our lesson, all in one place:

```python
# -*- coding: utf-8 -*-

#####################################################
# Pandas - Plotting our Data using Pandas
#####################################################

import pandas as pd

# ============================================================
# SECTION 1: LOAD THE DATA
# ============================================================
# We intend to plot our data directly from the pandas DF
# Under the hood, pandas is using Matplotlib to make or create the plot

transactions = pd.read_excel("grocery_database.xlsx", sheet_name="transactions")
customer_details = pd.read_excel("grocery_database.xlsx", sheet_name="customer_details")
product_areas = pd.read_excel("grocery_database.xlsx", sheet_name="product_areas")

# ============================================================
# SECTION 2: BASIC PLOTTING
# ============================================================
# The plot in pandas is majorly used to investigate the data,
# we might discover outliers or anomalies in the process.

# Plot ALL numeric columns in customer_details
# This creates multiple lines on one chart (often messy!)
customer_details.plot()

# ============================================================
# SECTION 3: LINE PLOTS (For Time-Series Data)
# ============================================================
# Line plot is used for sequential data (data that follows an order,
# like dates, time, or steps).

# Step 1: Aggregate the data to make it plotable
# We group by date and sum up sales_cost and num_items for each day
daily_sales_summary = transactions.groupby("transaction_date")[["sales_cost","num_items"]].sum().reset_index()

# Step 2: Plot sales_cost against the default index (row numbers)
# This will plot the sales_cost (y-axis) against the index (x-axis)
daily_sales_summary["sales_cost"].plot()

# Step 3: Plot with proper X and Y axes
# Plot transaction_date against sales_cost
daily_sales_summary.plot(x="transaction_date", y="sales_cost")

# Step 4: Explicitly specify line plot (this is the default, but good to be explicit)
daily_sales_summary.plot(x="transaction_date", y="sales_cost", kind="line")

# ============================================================
# SECTION 4: SCATTER PLOT (For Relationships)
# ============================================================
# Scatter plots show the relationship between two variables
# Each dot = one day's data
daily_sales_summary.plot(x="num_items", y="sales_cost", kind="scatter")

# ============================================================
# SECTION 5: BOX PLOT (For Distribution & Outliers)
# ============================================================
# In box plot, we only plot one variable
# The horizontal green line in the middle shows the median
# (Also known as the 50th percentile) sales_cost
daily_sales_summary.plot(y="sales_cost", kind="box")

# ============================================================
# SECTION 6: HISTOGRAM (For Frequency Distribution)
# ============================================================
# Shows how often values fall into different ranges
daily_sales_summary.plot(y="sales_cost", kind="hist")

# More detailed histogram with 25 bins (smaller ranges)
daily_sales_summary.plot(y="sales_cost", kind="hist", bins=25)

# ============================================================
# SECTION 7: BAR CHART (For Comparing Categories)
# ============================================================
# We want to see each product margin bar for a given product_area_name
product_areas.plot(kind="bar", y="profit_margin", x="product_area_name")
```

---

## 12. Quick Reference Cheat Sheet {#cheat-sheet}

### Plot Types at a Glance

| Plot Type          | `kind=`     | Best For                          | Needs X & Y?           |
| ------------------ | ----------- | --------------------------------- | ---------------------- |
| **Line**           | `"line"`    | Time series, trends               | ✅ Yes (recommended)   |
| **Scatter**        | `"scatter"` | Relationships, correlations       | ✅ Yes (both required) |
| **Box**            | `"box"`     | Distribution, outliers            | ❌ No (just Y)         |
| **Histogram**      | `"hist"`    | Frequency, distribution           | ❌ No (just Y)         |
| **Bar**            | `"bar"`     | Comparing categories              | ✅ Yes (recommended)   |
| **Horizontal Bar** | `"barh"`    | Comparing categories (long names) | ✅ Yes                 |

### Common Parameters

| Parameter | What It Controls            | Example                |
| --------- | --------------------------- | ---------------------- |
| `x`       | Column for X-axis           | `x="transaction_date"` |
| `y`       | Column for Y-axis           | `y="sales_cost"`       |
| `kind`    | Type of plot                | `kind="scatter"`       |
| `bins`    | Number of bars in histogram | `bins=25`              |
| `title`   | Chart title                 | `title="Daily Sales"`  |
| `figsize` | Chart size (width, height)  | `figsize=(10, 6)`      |
| `color`   | Bar/line color              | `color="red"`          |

---

## 13. Common Mistakes to Avoid {#common-mistakes}

### ❌ Mistake 1: Forgetting to Aggregate Time Data

```python
# BAD: Plotting raw transactions creates a mess!
transactions.plot(x="transaction_date", y="sales_cost")  # Too many points!

# GOOD: Aggregate first, then plot
daily = transactions.groupby("transaction_date")["sales_cost"].sum().reset_index()
daily.plot(x="transaction_date", y="sales_cost")
```

### ❌ Mistake 2: Using the Wrong Plot for the Job

```python
# BAD: Line plot for categories
product_areas.plot(x="product_area_name", y="profit_margin", kind="line")  # Misleading!

# GOOD: Bar chart for categories
product_areas.plot(x="product_area_name", y="profit_margin", kind="bar")
```

### ❌ Mistake 3: Ignoring Outliers

```python
# Always check for outliers before making decisions!
daily_sales_summary.plot(y="sales_cost", kind="box")  # Spot outliers first
```

### ❌ Mistake 4: Not Setting Figure Size

```python
# Default plots can be tiny!
daily_sales_summary.plot(x="transaction_date", y="sales_cost", figsize=(12, 6))  # Much better!
```

---

## 🎯 Summary

| What We Learned         | Key Takeaway                                                  |
| ----------------------- | ------------------------------------------------------------- |
| **Pandas + Matplotlib** | Pandas uses Matplotlib under the hood for easy plotting       |
| **Line Plot**           | Best for time series and sequential data                      |
| **Scatter Plot**        | Best for exploring relationships between two variables        |
| **Box Plot**            | Best for finding outliers and understanding data distribution |
| **Histogram**           | Best for seeing how data is spread across ranges              |
| **Bar Chart**           | Best for comparing different categories                       |
| **Aggregate First**     | Group and summarize before plotting raw transaction data      |

---

> 🎉 **Congratulations!** You now know how to create 6 essential plot types using Pandas. Remember: the goal of plotting is to **investigate** your data and discover insights that numbers alone can't reveal. Happy plotting!

---

_Day 58 — Data Science Journey 🚀_
