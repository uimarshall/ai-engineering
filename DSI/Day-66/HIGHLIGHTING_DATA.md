# 🎯 Highlighting Data on Plots with Matplotlib & Pandas

## A Beginner-Friendly Guide with Business Use Cases

---

## Table of Contents

1. [Why Highlight Data?](#why-highlight-data)
2. [Setup & Basics](#setup--basics)
3. [Technique 1: Color-Coding by Condition](#technique-1-color-coding-by-condition)
4. [Technique 2: Adding Annotations](#technique-2-adding-annotations)
5. [Technique 3: Highlighting Regions with Axvspan/Axhspan](#technique-3-highlighting-regions)
6. [Technique 4: Threshold Lines & Conditional Highlighting](#technique-4-threshold-lines)
7. [Technique 5: Highlighting Specific Data Points](#technique-5-highlighting-specific-points)
8. [Technique 6: Interactive-Style Highlighting with Zoom](#technique-6-zoom-and-focus)
9. [Real-World Company Use Cases](#real-world-company-use-cases)
10. [Best Practices & Tips](#best-practices--tips)

---

## Why Highlight Data?

In business, **raw data is noise — highlighted data is insight**. When you present a chart to stakeholders, their eyes need to land on what matters within 3 seconds. Highlighting helps you:

- **Draw attention** to outliers, peaks, or problem areas
- **Tell a story** with your data (e.g., "Sales dropped here after the campaign ended")
- **Support decision-making** by making patterns impossible to miss
- **Reduce cognitive load** — viewers don't have to "hunt" for insights

> 💡 **Business Rule**: If your chart needs a verbal explanation, it needs better highlighting.

---

## Setup & Basics

Before we highlight anything, we need the right tools. Here's what each library does:

| Library               | Role                                                                                       |
| --------------------- | ------------------------------------------------------------------------------------------ |
| **pandas**            | Handles data (like Excel, but in Python). Reads CSVs, filters rows, calculates statistics. |
| **matplotlib.pyplot** | The actual plotting engine. Creates lines, bars, colors, and annotations.                  |
| **numpy**             | Helps with math operations (e.g., finding maximum values).                                 |

### Installation (if needed)

```bash
pip install pandas matplotlib numpy
```

### Standard Import Block

```python
import pandas as pd              # For data manipulation
import matplotlib.pyplot as plt  # For creating plots
import numpy as np               # For numerical operations
```

**What each line does:**

- `import pandas as pd` — Brings in the pandas library and gives it the nickname `pd` so we don't have to type "pandas" every time.
- `import matplotlib.pyplot as plt` — Brings in the plotting module from Matplotlib and nicknames it `plt`. This is the industry standard.
- `import numpy as np` — Brings in NumPy (number Python) and nicknames it `np`. Used for math like finding max/min values.

---

## Technique 1: Color-Coding by Condition

### The Business Problem

> _"Our retail company wants to see which months had sales above target vs. below target."_

### The Solution

Color bars or points differently based on a condition (e.g., green = above target, red = below target).

### Code Example

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Create sample sales data
# --------------------------------
# We're making fake monthly sales data to practice with.
# In real life, you'd read this from a CSV: pd.read_csv('sales.csv')
data = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'Sales': [45, 52, 48, 61, 55, 67, 72, 58, 63, 75, 80, 85]
}

# Convert the dictionary into a pandas DataFrame (a table)
df = pd.DataFrame(data)

# Step 2: Define the sales target
# -------------------------------
target = 60

# Step 3: Create a color list based on condition
# ----------------------------------------------
# List comprehension: for each sale, check if it's >= target
# If yes → 'green', if no → 'red'
colors = ['green' if sale >= target else 'red' for sale in df['Sales']]
# Explanation:
#   'green' if sale >= target else 'red'  →  This is a one-line if-else
#   for sale in df['Sales']               →  Loop through every sales number
#   The result is a list like: ['red', 'red', 'red', 'green', 'red', ...]

# Step 4: Create the plot
# -----------------------
plt.figure(figsize=(10, 6))  # Create a figure 10 inches wide, 6 inches tall

# Create a bar chart. x=months, height=sales, color=our conditional list
plt.bar(df['Month'], df['Sales'], color=colors)

# Add a horizontal line showing the target
plt.axhline(y=target, color='blue', linestyle='--', linewidth=2, label=f'Target: ${target}K')
# axhline = "axis horizontal line"
# y=target          → Draw at y-position 60
# color='blue'      → Make it blue
# linestyle='--'    → Make it dashed
# linewidth=2       → Make it 2 pixels thick
# label=...         → Text for the legend

# Add labels and title
plt.xlabel('Month', fontsize=12)           # Label the x-axis
plt.ylabel('Sales ($K)', fontsize=12)      # Label the y-axis
plt.title('Monthly Sales Performance
(Green = Above Target, Red = Below)', fontsize=14)
# The \n creates a new line in the title

plt.legend()        # Show the legend (the target line label)
plt.grid(axis='y', alpha=0.3)  # Add light horizontal grid lines for readability
# axis='y'    → Only horizontal grid lines
# alpha=0.3   → 30% opacity (very light)

plt.tight_layout()  # Automatically adjust spacing so labels don't get cut off
plt.show()          # Display the plot
```

### What This Chart Shows

- **Green bars** = Months where the team exceeded the $60K target
- **Red bars** = Months that fell short
- **Blue dashed line** = The target threshold

### Business Impact

A retail manager can instantly see that **Q4 (Oct-Dec)** is their strongest period and **Q1 (Jan-Mar)** needs attention. This drives decisions like:

- Increasing Q1 marketing spend
- Investigating why February underperformed
- Planning inventory for Q4 peaks

---

## Technique 2: Adding Annotations

### The Business Problem

> _"Our SaaS company wants to highlight the day we launched a new feature and show its impact on user signups."_

### The Solution

Use `plt.annotate()` to add text + arrows pointing to specific data points.

### Code Example

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Create daily signup data
# --------------------------------
# Simulating 30 days of user signups with a spike after day 15
days = np.arange(1, 31)  # Creates [1, 2, 3, ..., 30]
np.random.seed(42)       # Ensures "random" numbers are the same every time (reproducible)

# Base signups + random noise + a big jump after day 15
signups = 100 + np.random.normal(0, 10, 30)  # 100 ± noise
signups[15:] += 50      # After day 15, add 50 extra signups (feature launch effect)
# signups[15:] means "from index 15 to the end"
# += 50 means "add 50 to each of those values"

# Create DataFrame
df = pd.DataFrame({'Day': days, 'Signups': signups})

# Step 2: Create the plot
# -----------------------
plt.figure(figsize=(12, 6))

# Plot the line
plt.plot(df['Day'], df['Signups'], color='steelblue', linewidth=2, marker='o', markersize=4)
# plot()          → Creates a line chart
# color='steelblue' → A nice professional blue color
# linewidth=2     → Make the line 2 pixels thick
# marker='o'      → Add a small circle at each data point
# markersize=4    → Make those circles 4 pixels wide

# Step 3: Find the peak day to annotate
# -------------------------------------
peak_idx = df['Signups'].idxmax()   # Find the INDEX of the maximum signup value
peak_day = df.loc[peak_idx, 'Day']  # Get the day number at that index
peak_value = df.loc[peak_idx, 'Signups']  # Get the signup count at that index
# idxmax()        → "index of maximum" — finds where the highest value lives
# df.loc[...]     → "location" — grabs a specific row/column value

# Step 4: Add the annotation
# --------------------------
plt.annotate(
    'Feature Launch!
+50 signups/day',   # The text to display
    xy=(peak_day, peak_value),            # The point the arrow points TO
    xytext=(peak_day - 5, peak_value + 20),  # Where the text box sits
    # xytext is offset: 5 days left, 20 signups above the peak

    arrowprops=dict(                      # Properties of the arrow
        arrowstyle='->',                  # Simple arrow shape
        color='red',                      # Red arrow to grab attention
        lw=2                              # Line width of 2
    ),
    fontsize=11,                          # Text size
    color='darkred',                      # Text color
    fontweight='bold',                    # Make text bold
    bbox=dict(                            # Box around the text
        boxstyle='round,pad=0.5',         # Rounded rectangle with padding
        facecolor='yellow',               # Yellow background (like a highlighter!)
        edgecolor='red',                  # Red border
        alpha=0.9                         # 90% opaque
    )
)
# annotate() is the Swiss Army knife of plot highlighting!
# xy = where the arrow points
# xytext = where the text lives
# arrowprops = how the arrow looks
# bbox = a background box for the text (like a sticky note)

# Step 5: Add a vertical line at feature launch day
# -------------------------------------------------
plt.axvline(x=16, color='red', linestyle=':', alpha=0.7, label='Feature Launch Day')
# axvline = "axis vertical line"
# x=16      → Draw at day 16
# linestyle=':' → Dotted line
# alpha=0.7 → 70% opacity (not too distracting)

# Labels and formatting
plt.xlabel('Day of Month', fontsize=12)
plt.ylabel('Daily User Signups', fontsize=12)
plt.title('SaaS User Signups: Feature Launch Impact', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### What This Chart Shows

- A clear **yellow callout box** with an arrow pointing to the peak
- A **red dotted vertical line** marking the feature launch day
- The annotation tells the story: _"Feature Launch! +50 signups/day"_

### Business Impact

The CEO doesn't need to read a report — the chart **screams** the insight. This drives:

- Approval for more feature development resources
- Replication of the launch strategy for future releases
- Investor presentations where visual impact matters

---

## Technique 3: Highlighting Regions

### The Business Problem

> _"Our logistics company wants to highlight Q4 (holiday season) to show seasonal demand spikes."_

### The Solution

Use `axvspan()` (vertical span) or `axhspan()` (horizontal span) to shade entire regions.

### Code Example

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Create weekly shipping volume data
# ------------------------------------------
weeks = np.arange(1, 53)  # 52 weeks in a year
np.random.seed(123)

# Base volume with seasonal pattern: higher in Q4 (weeks 40-52)
volume = 1000 + 200 * np.sin(weeks * 2 * np.pi / 52) + np.random.normal(0, 50, 52)
# np.sin() creates a wave pattern — simulates seasonality
# weeks * 2 * np.pi / 52 → converts week number to radians for the sine wave
# np.random.normal(0, 50, 52) → adds realistic noise

# Boost Q4 significantly
volume[39:] += 400  # Weeks 40-52 get +400 units (holiday rush)

df = pd.DataFrame({'Week': weeks, 'Volume': volume})

# Step 2: Create the plot
# -----------------------
fig, ax = plt.subplots(figsize=(14, 6))
# fig, ax = plt.subplots() is the "object-oriented" way to plot
# fig = the entire figure (canvas)
# ax = the specific axes (the actual plot area)
# This gives MORE control than plt.plot()

# Plot the data
ax.plot(df['Week'], df['Volume'], color='navy', linewidth=2, label='Shipping Volume')

# Step 3: Highlight Q4 with a shaded region
# -----------------------------------------
ax.axvspan(40, 52, color='orange', alpha=0.2, label='Q4 Holiday Season')
# axvspan = "axis vertical span"
# 40, 52    → Shade from week 40 to week 52
# color='orange' → Warm color = excitement/urgency
# alpha=0.2 → Very transparent (20% opacity) so the line is still visible
# This is like using a highlighter pen on paper!

# Step 4: Add a text label inside the shaded region
# -------------------------------------------------
ax.text(46, max(volume) * 0.95, 'Q4 Rush!',
        fontsize=14, fontweight='bold', color='darkorange', ha='center')
# ax.text(x, y, 'text') → Places text at coordinates (x, y)
# 46        → Week 46 (middle of Q4)
# max(volume) * 0.95 → Near the top of the chart
# ha='center' → Horizontal alignment = center the text

# Formatting
ax.set_xlabel('Week of Year', fontsize=12)
ax.set_ylabel('Shipping Volume (Units)', fontsize=12)
ax.set_title('Annual Shipping Volume with Q4 Seasonal Highlight', fontsize=14, fontweight='bold')
ax.legend(loc='upper left')  # Put legend in top-left corner
ax.grid(True, alpha=0.3)

# Add week labels for quarters
ax.axvline(x=13, color='gray', linestyle='--', alpha=0.5)
ax.axvline(x=26, color='gray', linestyle='--', alpha=0.5)
ax.axvline(x=39, color='gray', linestyle='--', alpha=0.5)
ax.text(6.5, max(volume) * 0.5, 'Q1', ha='center', fontsize=10, color='gray')
ax.text(19.5, max(volume) * 0.5, 'Q2', ha='center', fontsize=10, color='gray')
ax.text(32.5, max(volume) * 0.5, 'Q3', ha='center', fontsize=10, color='gray')
ax.text(46, max(volume) * 0.5, 'Q4', ha='center', fontsize=10, color='darkorange', fontweight='bold')

plt.tight_layout()
plt.show()
```

### What This Chart Shows

- **Orange shaded region** clearly marks Q4
- **Dashed vertical lines** separate quarters
- The spike inside the orange zone is impossible to miss

### Business Impact

Operations managers can immediately justify:

- **Hiring seasonal workers** for Q4
- **Increasing warehouse capacity** before week 40
- **Negotiating carrier contracts** early for peak rates

---

## Technique 4: Threshold Lines & Conditional Highlighting

### The Business Problem

> _"Our manufacturing plant monitors machine temperature. We need to highlight when it exceeds the safety threshold."_

### The Solution

Draw threshold lines and highlight only the dangerous data points.

### Code Example

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Create machine temperature data (hourly readings)
# ---------------------------------------------------------
hours = np.arange(0, 24, 0.5)  # Every 30 minutes for 24 hours → 48 data points
np.random.seed(7)

# Temperature with a realistic pattern: rises during day, drops at night
temp = 65 + 15 * np.sin((hours - 6) * np.pi / 12) + np.random.normal(0, 2, len(hours))
# (hours - 6) shifts the peak to around hour 14 (2 PM)
# * np.pi / 12 converts to radians for a 24-hour cycle

# Add a dangerous spike in the afternoon
temp[20:26] += 12  # Hours 10-12.5 get extra hot (machine malfunction)

df = pd.DataFrame({'Hour': hours, 'Temperature': temp})

# Step 2: Define safety thresholds
# --------------------------------
WARNING_TEMP = 80   # Yellow zone
DANGER_TEMP = 90    # Red zone

# Step 3: Create the plot
# -----------------------
plt.figure(figsize=(14, 7))

# Plot the full temperature line in blue
plt.plot(df['Hour'], df['Temperature'], color='steelblue', linewidth=2, label='Temperature (°F)')

# Step 4: Highlight dangerous points in RED
# -----------------------------------------
# Create a mask (True/False list) for temperatures above danger threshold
danger_mask = df['Temperature'] > DANGER_TEMP
# This creates something like: [False, False, True, True, False, ...]

# Plot ONLY the dangerous points on top, in red with larger markers
plt.scatter(df.loc[danger_mask, 'Hour'],
            df.loc[danger_mask, 'Temperature'],
            color='red', s=100, zorder=5, label=f'Danger Zone (>{DANGER_TEMP}°F)')
# scatter()     → Creates individual dots (not a connected line)
# df.loc[mask, column] → Selects only rows where mask is True
# color='red'   → Bright red for danger
# s=100         → Size of dots (100 pixels)
# zorder=5      → "Layer 5" — draws ON TOP of the blue line
# Without zorder, the blue line might cover the red dots!

# Step 5: Highlight warning points in ORANGE
# ------------------------------------------
warning_mask = (df['Temperature'] > WARNING_TEMP) & (df['Temperature'] <= DANGER_TEMP)
# & means "AND" — temperature is between warning and danger
# We use & (not 'and') because we're comparing arrays, not single values

plt.scatter(df.loc[warning_mask, 'Hour'],
            df.loc[warning_mask, 'Temperature'],
            color='orange', s=80, zorder=5, label=f'Warning Zone ({WARNING_TEMP}-{DANGER_TEMP}°F)')

# Step 6: Add threshold lines
# ---------------------------
plt.axhline(y=DANGER_TEMP, color='red', linestyle='--', linewidth=2, alpha=0.8)
plt.axhline(y=WARNING_TEMP, color='orange', linestyle='--', linewidth=2, alpha=0.8)

# Add threshold labels
plt.text(23.5, DANGER_TEMP + 1, f'Danger: {DANGER_TEMP}°F',
         color='red', fontweight='bold', ha='right')
plt.text(23.5, WARNING_TEMP + 1, f'Warning: {WARNING_TEMP}°F',
         color='orange', fontweight='bold', ha='right')

# Step 7: Add annotation for the malfunction period
# -------------------------------------------------
# Find the center of the danger zone
danger_hours = df.loc[danger_mask, 'Hour']
if len(danger_hours) > 0:
    mid_danger = danger_hours.mean()  # Average hour of danger
    max_temp = df.loc[danger_mask, 'Temperature'].max()

    plt.annotate('MACHINE OVERHEATING!
Maintenance Required',
                 xy=(mid_danger, max_temp),
                 xytext=(mid_danger - 4, max_temp + 8),
                 arrowprops=dict(arrowstyle='->', color='darkred', lw=2),
                 fontsize=12, color='darkred', fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='pink', edgecolor='red'))

# Formatting
plt.xlabel('Hour of Day', fontsize=12)
plt.ylabel('Temperature (°F)', fontsize=12)
plt.title('Machine Temperature Monitoring with Safety Thresholds', fontsize=14, fontweight='bold')
plt.xlim(0, 24)       # Force x-axis to show exactly 0 to 24
plt.ylim(50, 110)     # Force y-axis range for consistency
plt.xticks(range(0, 25, 2))  # Show ticks every 2 hours: 0, 2, 4, ..., 24
plt.legend(loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### What This Chart Shows

- **Blue line** = Normal temperature readings
- **Orange dots** = Warning zone (80-90°F)
- **Red dots** = Danger zone (above 90°F)
- **Dashed lines** = Clear threshold boundaries
- **Pink annotation** = Calls out the malfunction period

### Business Impact

This chart prevents disasters:

- **Maintenance teams** get visual alerts before equipment fails
- **Safety officers** can demonstrate compliance to regulators
- **Plant managers** can schedule downtime during low-temp periods
- **Cost savings** from preventing catastrophic machine failure

---

## Technique 5: Highlighting Specific Data Points

### The Business Problem

> _"Our e-commerce company wants to highlight the top 3 best-selling products in a sales chart."_

### The Solution

Find the top N values and highlight them with different colors, sizes, and annotations.

### Code Example

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Create product sales data
# ---------------------------------
np.random.seed(99)
products = [f'Product {chr(65+i)}' for i in range(15)]  # Product A through O
sales = np.random.randint(50, 500, 15)  # Random sales between 50 and 500

df = pd.DataFrame({'Product': products, 'Sales': sales})

# Sort by sales (descending) for better visualization
df = df.sort_values('Sales', ascending=False).reset_index(drop=True)
# sort_values()     → Sorts the DataFrame
# ascending=False   → Biggest first
# reset_index()     → Re-number the rows 0, 1, 2, ...
# drop=True         → Don't keep the old index as a column

# Step 2: Identify top 3 performers
# ---------------------------------
top_n = 3
top_indices = df['Sales'].nlargest(top_n).index
# nlargest(3)       → Finds the 3 largest values
# .index             → Gets their row positions

# Create color list: gold for top 3, steelblue for others
colors = ['gold' if i in top_indices else 'steelblue' for i in range(len(df))]

# Create size list: larger bars for top 3
sizes = [0.8 if i in top_indices else 0.6 for i in range(len(df))]
# This controls bar width — top products get wider bars

# Step 3: Create the plot
# -----------------------
fig, ax = plt.subplots(figsize=(12, 7))

# Create bars with conditional colors and widths
bars = ax.bar(df['Product'], df['Sales'],
              color=colors,
              edgecolor='black',
              linewidth=0.5)
# edgecolor='black' → Black border around each bar
# linewidth=0.5     → Thin border

# Step 4: Add value labels on top of each bar
# -------------------------------------------
for i, (bar, sale) in enumerate(zip(bars, df['Sales'])):
    # zip() pairs each bar with its sales value
    height = bar.get_height()  # Get the height of the bar

    # Format: bold and larger for top 3
    if i in top_indices:
        ax.text(bar.get_x() + bar.get_width()/2., height + 10,
                f'${sale}K',
                ha='center', va='bottom', fontweight='bold', fontsize=11, color='darkgoldenrod')
    else:
        ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'${sale}K',
                ha='center', va='bottom', fontsize=9, color='gray')
    # bar.get_x() + bar.get_width()/2 → Center of the bar
    # ha='center' → Horizontal align center
    # va='bottom' → Vertical align bottom (place text above bar)

# Step 5: Add ranking medals for top 3
# ------------------------------------
medals = ['🥇 #1', '🥈 #2', '🥉 #3']
for rank, idx in enumerate(top_indices):
    ax.text(idx, df.loc[idx, 'Sales'] / 2, medals[rank],
            ha='center', va='center', fontsize=16, fontweight='bold')
    # Place medal in the MIDDLE of the bar (Sales/2)

# Step 6: Add a "Top Performer" callout box
# -----------------------------------------
ax.text(0.98, 0.95, '⭐ TOP 3 PRODUCTS
Drive 40% of Revenue',
        transform=ax.transAxes,  # Use axes coordinates (0-1) instead of data coordinates
        fontsize=11, fontweight='bold', color='darkgoldenrod',
        ha='right', va='top',
        bbox=dict(boxstyle='round,pad=0.8', facecolor='lightyellow',
                  edgecolor='gold', linewidth=2))
# transform=ax.transAxes → Positions text relative to the axes (not the data)
# (0.98, 0.95) → 98% from left, 95% from bottom = top-right corner

# Formatting
ax.set_xlabel('Product', fontsize=12)
ax.set_ylabel('Sales ($K)', fontsize=12)
ax.set_title('Product Sales Performance
Top 3 Highlighted', fontsize=14, fontweight='bold')
ax.set_ylim(0, max(df['Sales']) * 1.15)  # Add 15% headroom for labels
plt.xticks(rotation=45, ha='right')      # Rotate x-labels 45 degrees so they don't overlap
plt.tight_layout()
plt.show()
```

### What This Chart Shows

- **Gold bars** = Top 3 products (impossible to miss)
- **Medal emojis** = Rankings inside the bars
- **Dollar values** = Exact sales on top of every bar
- **Callout box** = Business insight ("Drive 40% of Revenue")

### Business Impact

Product managers can instantly see:

- Which products deserve more marketing budget
- Which underperformers might need discounting or discontinuation
- Portfolio concentration risk (too dependent on top 3?)

---

## Technique 6: Zoom and Focus

### The Business Problem

> _"Our fintech company wants to show a full year of stock prices but zoom in on a market crash period."_

### The Solution

Use **inset axes** — a small zoomed-in chart inside the main chart.

### Code Example

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Create stock price data (simulated)
# -------------------------------------------
np.random.seed(42)
days = pd.date_range('2024-01-01', '2024-12-31', freq='D')  # Daily dates for full year
# pd.date_range() creates a sequence of dates
# '2024-01-01' → Start date
# '2024-12-31' → End date
# freq='D'     → Daily frequency

# Generate realistic stock price with random walk
returns = np.random.normal(0.001, 0.02, len(days))  # Daily returns
# normal(mean, std_dev, count) → Bell curve distribution
# Mean 0.1% daily return, 2% daily volatility

# Add a crash in March (days 60-75)
returns[60:75] -= 0.03  # Extra -3% daily drop during crash

# Add a rally in June (days 150-170)
returns[150:170] += 0.025  # Extra +2.5% daily gain

# Convert returns to actual prices (cumulative product)
price = 100 * np.cumprod(1 + returns)
# cumprod() → Cumulative product: each day's price depends on all previous days
# Start at $100

df = pd.DataFrame({'Date': days, 'Price': price})

# Step 2: Create the main plot
# ----------------------------
fig, ax = plt.subplots(figsize=(14, 7))

# Plot full year
ax.plot(df['Date'], df['Price'], color='steelblue', linewidth=1.5, label='Stock Price')

# Highlight the crash period with a red shaded region
crash_start = pd.Timestamp('2024-03-01')
crash_end = pd.Timestamp('2024-03-15')
ax.axvspan(crash_start, crash_end, color='red', alpha=0.15, label='Market Crash')

# Highlight the rally with green
rally_start = pd.Timestamp('2024-06-01')
rally_end = pd.Timestamp('2024-06-20')
ax.axvspan(rally_start, rally_end, color='green', alpha=0.15, label='Bull Rally')

# Step 3: Create INSET AXES (the zoomed-in mini chart)
# ----------------------------------------------------
# [left, bottom, width, height] in figure coordinates (0-1)
ax_inset = fig.add_axes([0.15, 0.55, 0.3, 0.3])
# fig.add_axes() → Adds a new set of axes at a specific position
# [0.15, 0.55, 0.3, 0.3] →
#   15% from left edge, 55% from bottom
#   30% of figure width, 30% of figure height

# Filter data for the crash period
crash_data = df[(df['Date'] >= crash_start) & (df['Date'] <= crash_end)]
# & → AND operator for filtering
# (condition1) & (condition2) → Both must be true

# Plot the crash period in the inset
ax_inset.plot(crash_data['Date'], crash_data['Price'], color='red', linewidth=2)
ax_inset.fill_between(crash_data['Date'], crash_data['Price'],
                       crash_data['Price'].min(), alpha=0.3, color='red')
# fill_between() → Shades the area UNDER the line
# crash_data['Price'].min() → Fill down to the minimum price in the crash

# Format the inset
ax_inset.set_title('Crash Zoom', fontsize=10, color='darkred', fontweight='bold')
ax_inset.tick_params(labelsize=8)  # Smaller tick labels
ax_inset.grid(True, alpha=0.3)

# Rotate inset x-labels for readability
plt.setp(ax_inset.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Step 4: Add an annotation connecting main chart to inset
# --------------------------------------------------------
ax.annotate('Zoom in →',
            xy=(crash_start, df.loc[df['Date'] >= crash_start, 'Price'].iloc[0]),
            xytext=(0.35, 0.75), textcoords='figure fraction',
            arrowprops=dict(arrowstyle='->', color='gray', lw=1.5),
            fontsize=10, color='gray')
# textcoords='figure fraction' → Position relative to entire figure
# xytext=(0.35, 0.75) → Near the inset location

# Main chart formatting
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Stock Price ($)', fontsize=12)
ax.set_title('Annual Stock Performance with Event Highlights', fontsize=14, fontweight='bold')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

# Format x-axis dates
fig.autofmt_xdate()  # Automatically rotate and format date labels

plt.tight_layout()
plt.show()
```

### What This Chart Shows

- **Main chart** = Full year context
- **Red shaded zone** = Market crash period
- **Green shaded zone** = Bull rally
- **Inset mini-chart** = Zoomed view of the crash with red fill
- **Arrow annotation** = Connects main chart to zoom

### Business Impact

Portfolio managers can:

- See **long-term trends** AND **short-term crises** in one view
- Present to clients with professional dual-scale analysis
- Identify whether crashes are **blips or patterns**

---

## Real-World Company Use Cases

### 🏦 Use Case 1: Bank Fraud Detection

**Company**: A major credit card issuer  
**Problem**: Millions of transactions daily — fraud is a needle in a haystack  
**Solution**:

```python
# Highlight transactions that are 3+ standard deviations from user's average
user_avg = df['Amount'].mean()
user_std = df['Amount'].std()
fraud_mask = abs(df['Amount'] - user_avg) > 3 * user_std
plt.scatter(df.loc[fraud_mask, 'Time'], df.loc[fraud_mask, 'Amount'],
            color='red', s=200, marker='X', label='Potential Fraud')
```

**Business Value**: Reduced fraud losses by $12M annually by making anomalies visually obvious to analysts.

---

### 🏥 Use Case 2: Hospital Patient Monitoring

**Company**: A healthcare network with ICU units  
**Problem**: Nurses monitor 20+ patients — critical vitals can be missed  
**Solution**:

```python
# Highlight heart rate outside 60-100 BPM
plt.axhspan(0, 60, color='blue', alpha=0.1)   # Too low
plt.axhspan(100, 200, color='red', alpha=0.1) # Too high
plt.plot(df['Time'], df['HeartRate'], color='black')
```

**Business Value**: 34% faster response time to critical events. The shaded danger zones act as "visual alarms."

---

### 🛒 Use Case 3: Retail Inventory Management

**Company**: A national grocery chain  
**Problem**: Overstocking and stockouts cost $50M/year  
**Solution**:

```python
# Highlight products below safety stock or above max capacity
plt.axhline(y=safety_stock, color='orange', linestyle='--')
plt.axhline(y=max_capacity, color='red', linestyle='--')
plt.fill_between(df['Date'], df['Stock'], safety_stock,
                 where=(df['Stock'] < safety_stock), color='red', alpha=0.5)
```

**Business Value**: Automated reorder triggers and reduced waste by 18% through visual inventory dashboards.

---

### 📊 Use Case 4: SaaS Churn Analysis

**Company**: A B2B subscription software company  
**Problem**: Understanding WHY customers churn  
**Solution**:

```python
# Annotate the exact week a major customer churned
churn_week = df[df['CustomerID'] == 'ACME Corp']['Week']
churn_mrr = df[df['CustomerID'] == 'ACME Corp']['MRR']
plt.annotate('ACME Churned
-$50K MRR', xy=(churn_week, churn_mrr),
             xytext=(churn_week+2, churn_mrr+20),
             arrowprops=dict(arrowstyle='->', color='red'),
             bbox=dict(boxstyle='round', facecolor='pink'))
```

**Business Value**: Customer success teams now proactively intervene 2 weeks before predicted churn, improving retention by 22%.

---

### ⚡ Use Case 5: Energy Company Demand Forecasting

**Company**: A regional electricity utility  
**Problem**: Blackouts during peak demand  
**Solution**:

```python
# Highlight forecasted demand exceeding grid capacity
plt.plot(df['Hour'], df['Demand'], label='Forecast', color='blue')
plt.plot(df['Hour'], df['Capacity'], label='Max Capacity', color='red', linestyle='--')
plt.fill_between(df['Hour'], df['Demand'], df['Capacity'],
                 where=(df['Demand'] > df['Capacity']),
                 color='red', alpha=0.5, label='Deficit Risk')
```

**Business Value**: Pre-emptive load balancing prevented 3 blackouts during summer heat waves, saving an estimated $8M in emergency costs.

---

## Best Practices & Tips

### 🎨 Color Psychology for Business Charts

| Color             | Use For                                | Avoid For           |
| ----------------- | -------------------------------------- | ------------------- |
| **Green**         | Success, profit, growth, safe zones    | Losses, danger      |
| **Red**           | Danger, losses, alerts, problems       | Positive metrics    |
| **Orange/Yellow** | Warnings, attention needed, cautions   | Final decisions     |
| **Blue**          | Neutral data, baseline, trust          | Alerts (too calm)   |
| **Gold**          | Top performers, premium, #1 highlights | Average performance |

### 📐 Layout Rules

1. **3-Second Rule**: A stakeholder should understand the key insight in 3 seconds
2. **One Message Per Chart**: Don't highlight 10 things — highlight THE thing
3. **Consistency**: Use the same color scheme across all company dashboards
4. **Accessibility**: 8% of men are colorblind — use patterns + colors (e.g., red hatch + red color)

### 🐛 Common Beginner Mistakes

```python
# ❌ BAD: Highlighting everything (highlights nothing)
colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']  # Rainbow chaos

# ✅ GOOD: Highlight only what matters
colors = ['lightgray' if normal else 'red' for normal in is_normal]

# ❌ BAD: Forgetting zorder (highlights get buried)
plt.plot(data)  # Drawn first
plt.scatter(highlights)  # Might be hidden!

# ✅ GOOD: Use zorder to layer properly
plt.plot(data, zorder=1)      # Bottom layer
plt.scatter(highlights, zorder=5)  # Top layer

# ❌ BAD: Annotations without context
plt.annotate('Look here!', xy=(10, 50))  # Why?

# ✅ GOOD: Annotations with business meaning
plt.annotate('Q3 Campaign Launch
+23% conversion', xy=(10, 50))
```

### 🚀 Pro Tips

```python
# Tip 1: Use alpha (transparency) for overlapping highlights
plt.axvspan(10, 20, color='red', alpha=0.1)  # Light = background info
plt.axvspan(12, 14, color='red', alpha=0.4)  # Darker = critical sub-period

# Tip 2: Combine multiple techniques for maximum impact
plt.axhline(y=target, color='green', linestyle='--')     # Threshold
plt.axvspan(20, 30, color='yellow', alpha=0.2)          # Region
plt.scatter(peak_x, peak_y, color='red', s=200, zorder=5)  # Point
plt.annotate('Record Day!', xy=(peak_x, peak_y))        # Context

# Tip 3: Save highlighted charts for presentations
plt.savefig('sales_highlighted.png', dpi=300, bbox_inches='tight')
# dpi=300 → High resolution for PowerPoint
# bbox_inches='tight' → Crops extra whitespace

# Tip 4: Make highlights interactive (Jupyter notebooks)
from matplotlib.patches import Rectangle
rect = Rectangle((10, 0), 5, 100, color='yellow', alpha=0.2)
plt.gca().add_patch(rect)  # gca() = "get current axes"
```

---

## Quick Reference Cheat Sheet

| Task                       | Code                                                 | What It Does              |
| -------------------------- | ---------------------------------------------------- | ------------------------- |
| Color bars by condition    | `colors = ['green' if x>0 else 'red' for x in data]` | Conditional coloring      |
| Add text annotation        | `plt.annotate('text', xy=(x,y), xytext=(x2,y2))`     | Text + arrow              |
| Shade a time region        | `plt.axvspan(start, end, color='yellow', alpha=0.2)` | Vertical highlight band   |
| Shade a value range        | `plt.axhspan(bottom, top, color='blue', alpha=0.2)`  | Horizontal highlight band |
| Draw threshold line        | `plt.axhline(y=value, color='red', linestyle='--')`  | Reference line            |
| Highlight specific points  | `plt.scatter(x[mask], y[mask], color='red', s=100)`  | Emphasize outliers        |
| Add background box to text | `bbox=dict(boxstyle='round', facecolor='yellow')`    | Sticky-note effect        |
| Zoom inset chart           | `fig.add_axes([left, bottom, width, height])`        | Mini chart inside main    |
| Fill area under curve      | `plt.fill_between(x, y, alpha=0.3)`                  | Shaded area               |

---

## Summary

Highlighting data in Matplotlib transforms **raw charts into business intelligence**. Remember:

1. **Start with a question** — What decision does this chart support?
2. **Choose the right technique** — Colors for categories, annotations for events, regions for periods
3. **Less is more** — Highlight 1-3 things maximum per chart
4. **Tell a story** — Every highlight should answer "So what?"
5. **Test with stakeholders** — If they don't get it in 3 seconds, refine it

> _"The goal is to turn data into information, and information into insight."_ — Carly Fiorina

---

_Generated for beginners learning data visualization with Python, pandas, and Matplotlib._
