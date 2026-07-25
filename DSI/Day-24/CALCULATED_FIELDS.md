# Calculated Fields in Tableau

## What is a Calculated Field?

A **Calculated Field** is a new field created from existing data using formulas or expressions. Instead of just using raw columns from your dataset, calculated fields allow you to transform, combine, aggregate, or conditionally compute values on the fly.

In simple terms: If your data has `Sales` and `Profit`, but you want `Profit Margin %` — that's a calculated field. You create it using Tableau's calculation language.

---

## Why Use Calculated Fields?

| Reason                  | Example                                     |
| ----------------------- | ------------------------------------------- |
| Data cleaning           | Extract first name from full name           |
| Business logic          | Flag high-value customers                   |
| Aggregation             | Running total or moving average             |
| Conditional logic       | Profitability status (Profitable / Loss)    |
| Date manipulation       | Extract month name, calculate age, etc.     |
| String manipulation     | Combine first and last name, fix formatting |
| Performance improvement | Pre-compute a metric instead of many calcs  |

---

## Basic Types of Calculated Fields

### 1. Row-Level Calculations (Per-row)

These operate on each individual row of data.

- `[Profit] - [Discount]` → Net value per row
- `[Sales] * 1.1` → Sales with 10% increase
- `[First Name] + " " + [Last Name]` → Full name

### 2. Aggregate Calculations (Grouped)

These operate on aggregated data.

- `SUM([Sales]) / SUM([Quantity])` → Average price per unit
- `AVG([Profit])` → Average profit across all rows

### 3. Table Calculations (Over the view)

These compute on the data visible in the chart.

- `RUNNING_SUM(SUM([Sales]))` → Cumulative sales
- `WINDOW_AVG(SUM([Sales]))` → Average over a window

---

## Simple Examples of Calculated Fields

### Example 1: Profit Ratio

```
SUM([Profit]) / SUM([Sales])
```

Use: Measures how much profit is made per dollar of sales.

### Example 2: Discounted Sales

```
[Sales] * (1 - [Discount])
```

Use: Shows actual revenue after discount.

### Example 3: Full Name

```
[First Name] + " " + [Last Name]
```

Use: Combines first and last name columns into one.

### Example 4: Age from Birth Date

```
DATEDIFF('year', [Birth Date], TODAY())
```

Use: Calculates a person's current age.

### Example 5: High Value Customer Flag

```
IF [Sales] > 1000 THEN "High Value" ELSE "Standard" END
```

Use: Classifies customers into segments.

### Example 6: Month Name from Date

```
DATENAME('month', [Order Date])
```

Use: Extracts "January", "February", etc. from a date.

### Example 7: Sales Range

```
IF [Sales] < 100 THEN "Low"
ELSEIF [Sales] >= 100 AND [Sales] < 500 THEN "Medium"
ELSE "High"
END
```

Use: Groups sales into tiers for analysis.

---

## Common Logical & Calculation Terms in Tableau

Below are frequently used functions/operators organized by category.

---

### Logical Operators

| Operator | Description                      | Example                                          |
| -------- | -------------------------------- | ------------------------------------------------ |
| `AND`    | True if both conditions are true | `IF [Sales] > 1000 AND [Profit] > 0 THEN "Good"` |
| `OR`     | True if at least one is true     | `IF [Region] = "East" OR [Region] = "West" THEN` |
| `NOT`    | Reverses boolean value           | `IF NOT [IsReturned] THEN "Active" END`          |
