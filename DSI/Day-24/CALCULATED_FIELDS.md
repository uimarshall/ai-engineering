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

| Operator     | Description                             | Example                                                   |
| ------------ | --------------------------------------- | --------------------------------------------------------- |
| `AND`        | True if both conditions are true        | `IF [Sales] > 1000 AND [Profit] > 0 THEN "Good"`          |
| `OR`         | True if at least one is true            | `IF [Region] = "East" OR [Region] = "West" THEN`          |
| `NOT`        | Reverses boolean value                  | `IF NOT [IsReturned] THEN "Active" END`                   |
| `IF`         | Conditional branching                   | `IF [Sales] > 500 THEN "High" ELSE "Low" END`             |
| `ELSEIF`     | Additional condition in IF block        | `IF ... ELSEIF ... ELSE ... END`                          |
| `CASE`       | Switch/match on specific values         | `CASE [Region] WHEN "East" THEN 1 WHEN "West" THEN 2 END` |
| `IIF`        | Inline conditional (like Excel IF)      | `IIF([Sales] > 0, "Profitable", "Loss")`                  |
| `END`        | Closes IF / CASE blocks                 | Required at the end of every IF or CASE block             |
| `THEN`       | Specifies result when condition is true | `IF [Sales] > 1000 THEN "High" END`                       |
| `WHEN`       | Used inside CASE for each value check   | `CASE [Status] WHEN "Active" THEN 1 END`                  |
| `ELSE`       | Fallback when no condition matches      | `IF ... ELSE "Other" END`                                 |
| `IS NULL`    | Checks if a value is null               | `[Region] IS NULL`                                        |
| `ISNULL`     | Function version of null check          | `ISNULL([Region])`                                        |
| `IFNULL`     | Replaces null with a default value      | `IFNULL([Discount], 0)`                                   |
| `ZN`         | Returns zero if null, else the value    | `ZN([Profit])`                                            |
| `MIN`        | Returns minimum value                   | `MIN([Sales])`                                            |
| `MAX`        | Returns maximum value                   | `MAX([Sales])`                                            |
| `CONTAINS`   | Checks if string contains substring     | `CONTAINS([Product Name], "Table")`                       |
| `STARTSWITH` | Checks if string starts with pattern    | `STARTSWITH([Customer Name], "A")`                        |
| `ENDSWITH`   | Checks if string ends with pattern      | `ENDSWITH([Email], ".com")`                               |

### IF vs CASE — When to Use Which

| Situation                          | Use    | Example                                                                 |
| ---------------------------------- | ------ | ----------------------------------------------------------------------- |
| Range/condition logic (>, <, >=)   | `IF`   | `IF [Sales] > 1000 THEN "High" ELSE "Low" END`                          |
| Exact value matching (few values)  | `CASE` | `CASE [Region] WHEN "East" THEN 1 WHEN "West" THEN 2 ELSE 3 END`        |
| Complex logic with multiple fields | `IF`   | `IF [Sales] > 1000 AND [Profit] > 0 THEN "High Value" END`              |
| Simple value lookup (readable)     | `CASE` | `CASE [Segment] WHEN "Consumer" THEN "C" WHEN "Corporate" THEN "B" END` |

---

### Number Functions

| Function  | Description                                 | Example           | Result |
| --------- | ------------------------------------------- | ----------------- | ------ |
| `CEILING` | Rounds a number **up** to nearest integer   | `CEILING(4.2)`    | 5      |
| `FLOOR`   | Rounds a number **down** to nearest integer | `FLOOR(4.8)`      | 4      |
| `ROUND`   | Rounds to specified decimal places          | `ROUND(4.257, 2)` | 4.26   |
| `ABS`     | Returns absolute (positive) value           | `ABS(-150)`       | 150    |
| `POWER`   | Raises number to a power                    | `POWER(5, 3)`     | 125    |
| `SQRT`    | Square root                                 | `SQRT(16)`        | 4      |
| `INT`     | Converts to integer (truncates decimal)     | `INT(7.9)`        | 7      |
| `SIGN`    | Returns -1, 0, or 1 based on sign           | `SIGN(-25)`       | -1     |
| `DIV`     | Integer division (no remainder)             | `DIV(17, 5)`      | 3      |
| `MOD`     | Remainder after division (modulo)           | `MOD(17, 5)`      | 2      |

---

### String Functions

| Function     | Description                             | Example                             | Result     |
| ------------ | --------------------------------------- | ----------------------------------- | ---------- |
| `LEN`        | Returns length of a string              | `LEN("Tableau")`                    | 7          |
| `LEFT`       | Extracts first N characters             | `LEFT("Tableau", 3)`                | "Tab"      |
| `RIGHT`      | Extracts last N characters              | `RIGHT("Tableau", 4)`               | "leau"     |
| `MID`        | Extracts from position N for length L   | `MID("Tableau", 3, 4)`              | "blea"     |
| `UPPER`      | Converts to uppercase                   | `UPPER("tableau")`                  | "TABLEAU"  |
| `LOWER`      | Converts to lowercase                   | `LOWER("TABLEAU")`                  | "tableau"  |
| `TRIM`       | Removes leading and trailing spaces     | `TRIM("  data  ")`                  | "data"     |
| `REPLACE`    | Replaces all occurrences of substring   | `REPLACE("Cat Dog", "Dog", "Bird")` | "Cat Bird" |
| `CONTAINS`   | Checks if string contains a substring   | `CONTAINS([Product], "Pro")`        | True/False |
| `STARTSWITH` | Checks if string starts with pattern    | `STARTSWITH([Name], "Dr.")`         | True/False |
| `ENDSWITH`   | Checks if string ends with pattern      | `ENDSWITH([Email], ".com")`         | True/False |
| `SPLIT`      | Splits string on delimiter              | `SPLIT("a-b-c", "-", 2)`            | "b"        |
| `FIND`       | Returns position of substring (0-based) | `FIND("Tableau", "bl")`             | 3          |

---

### Date Functions

| Function       | Description                                | Example                            | Result              |
| -------------- | ------------------------------------------ | ---------------------------------- | ------------------- |
| `TODAY()`      | Returns current date                       | `TODAY()`                          | 2026-01-15          |
| `NOW()`        | Returns current date and time              | `NOW()`                            | 2026-01-15 10:30:00 |
| `DATE`         | Converts string/number to date             | `DATE("2026-01-15")`               | 2026-01-15          |
| `DATEPART`     | Extracts part of a date (as number)        | `DATEPART('month', [Order Date])`  | 1, 2, 3...          |
| `DATENAME`     | Extracts part of a date (as string)        | `DATENAME('month', [Order Date])`  | "January"           |
| `DATEADD`      | Adds/subtracts time units to a date        | `DATEADD('day', 30, [Order Date])` | Date + 30 days      |
| `DATEDIFF`     | Difference between two dates in given unit | `DATEDIFF('day', [Start], [End])`  | Number of days      |
| `DATETRUNC`    | Truncates date to specified precision      | `DATETRUNC('month', [Order Date])` | First of month      |
| `MAKEDATE`     | Creates date from year, month, day         | `MAKEDATE(2026, 1, 15)`            | 2026-01-15          |
| `MAKEDATETIME` | Creates datetime from date and time        | `MAKEDATETIME([Date], #12:00:00#)` | Combined datetime   |
| `ISDATE`       | Checks if a string is a valid date         | `ISDATE("2026-01-15")`             | True/False          |

#### Common Date Parts

| Part        | Description         | Example                             | Result        |
| ----------- | ------------------- | ----------------------------------- | ------------- |
| `'year'`    | Year (4 digits)     | `DATEPART('year', #2026-01-15#)`    | 2026          |
| `'quarter'` | Quarter (1-4)       | `DATEPART('quarter', #2026-04-01#)` | 2             |
| `'month'`   | Month (1-12)        | `DATEPART('month', #2026-01-15#)`   | 1             |
| `'day'`     | Day of month (1-31) | `DATEPART('day', #2026-01-15#)`     | 15            |
| `'week'`    | Week number         | `DATEPART('week', #2026-01-15#)`    | 3             |
| `'weekday'` | Day of week (Sun=1) | `DATEPART('weekday', #2026-01-15#)` | 4 (Wednesday) |

---

### Aggregate Functions

| Function | Description                       | Example                    | Use Case                    |
| -------- | --------------------------------- | -------------------------- | --------------------------- |
| `SUM`    | Adds all values                   | `SUM([Sales])`             | Total sales                 |
| `AVG`    | Average of values                 | `AVG([Price])`             | Average product price       |
| `COUNT`  | Count of non-null rows            | `COUNT([Order ID])`        | Number of orders            |
| `COUNTD` | Count of unique (distinct) values | `COUNTD([Customer ID])`    | Unique customers            |
| `MIN`    | Minimum value                     | `MIN([Sales])`             | Lowest sale                 |
| `MAX`    | Maximum value                     | `MAX([Sales])`             | Highest sale                |
| `MEDIAN` | Median value                      | `MEDIAN([Salary])`         | Middle salary value         |
| `STDEV`  | Standard deviation (sample)       | `STDEV([Price])`           | Price variability           |
| `VAR`    | Variance (sample)                 | `VAR([Profit])`            | Profit spread               |
| `COVAR`  | Covariance (sample)               | `COVAR([Sales], [Profit])` | Relationship between fields |

---

### Type Conversion Functions

| Function   | Description                           | Example                        | Result              |
| ---------- | ------------------------------------- | ------------------------------ | ------------------- |
| `STR`      | Converts a number/date to a string    | `STR([Sales])`                 | "123.45"            |
| `INT`      | Converts a string/float to an integer | `INT("123")`                   | 123                 |
| `FLOAT`    | Converts to a decimal number          | `FLOAT("45.67")`               | 45.67               |
| `DATE`     | Converts to a date                    | `DATE("2026-01-15")`           | 2026-01-15          |
| `DATETIME` | Converts to a date & time             | `DATETIME("2026-01-15 14:30")` | 2026-01-15 14:30:00 |

---

### Table Calculation Functions

| Function         | Description                                       | Example                             |
| ---------------- | ------------------------------------------------- | ----------------------------------- |
| `RUNNING_SUM`    | Cumulative sum over the partition                 | `RUNNING_SUM(SUM([Sales]))`         |
| `RUNNING_AVG`    | Cumulative average                                | `RUNNING_AVG(SUM([Sales]))`         |
| `WINDOW_SUM`     | Sum over a specified window                       | `WINDOW_SUM(SUM([Sales]), -2, 2)`   |
| `WINDOW_AVG`     | Average over a window                             | `WINDOW_AVG(SUM([Sales]))`          |
| `TOTAL`          | Total over entire partition                       | `TOTAL(SUM([Sales]))`               |
| `RANK`           | Rank values (1 = highest)                         | `RANK(SUM([Sales]))`                |
| `RANK_DENSE`     | Dense rank (no gaps)                              | `RANK_DENSE(SUM([Sales]))`          |
| `RANK_UNIQUE`    | Unique rank (no ties)                             | `RANK_UNIQUE(SUM([Sales]))`         |
| `FIRST`          | Index from first row (0, -1, -2...)               | `FIRST()`                           |
| `LAST`           | Index from last row (0, -1, -2...)                | `LAST()`                            |
| `INDEX`          | Row index (1, 2, 3...)                            | `INDEX()`                           |
| `LOOKUP`         | Value from an offset row                          | `LOOKUP(SUM([Sales]), -1)`          |
| `PREVIOUS_VALUE` | Previous value in the partition                   | `PREVIOUS_VALUE(SUM([Sales]))`      |
| `SCRIPT_INT`     | Pass expression to an external service (R/Python) | `SCRIPT_INT("result", SUM([arg1]))` |

---

## Practical Examples Combining Multiple Functions

### Example: Discounted Profit

```tableau
SUM([Profit]) - (SUM([Profit]) * [Discount])
```

### Example: Customer Tenure (Years as Customer)

```tableau
DATEDIFF('year', [First Purchase Date], TODAY())
```

### Example: Sales Tier with Multiple Conditions

```tableau
IF [Sales] > 5000 THEN "Platinum"
ELSEIF [Sales] > 1000 AND [Sales] <= 5000 THEN "Gold"
ELSEIF [Sales] > 500 AND [Sales] <= 1000 THEN "Silver"
ELSE "Bronze"
END
```

### Example: YoY Growth Rate

```tableau
(SUM([Sales]) - LOOKUP(SUM([Sales]), -1)) / ABS(LOOKUP(SUM([Sales]), -1))
```

### Example: Dynamic Date Filter — Last 30 Days

```tableau
[Order Date] >= DATEADD('day', -30, TODAY())
```

### Example: Cleaned & Formatted Customer Name

```tableau
UPPER(TRIM([First Name])) + " " + UPPER(TRIM([Last Name]))
```

### Example: Profit Flag using IIF

```tableau
IIF(SUM([Profit]) > 0, "Profitable", "Loss")
```

### Example: Running Total of Sales by Month

```tableau
RUNNING_SUM(SUM([Sales]))
```

> **Note**: Table calculations like `RUNNING_SUM` depend on the dimensions present in the view and the **compute using** setting (Table Across, Pane Down, etc.).

---

## How to Create a Calculated Field in Tableau

1. **Right-click** in the **Data pane** (left sidebar) → **Create Calculated Field**
2. Or go to the top menu: **Analysis → Create Calculated Field**
3. Name your field (e.g., "Profit Ratio")
4. Enter the formula (e.g., `SUM([Profit]) / SUM([Sales])`)
5. Click **OK**
6. The new field appears in the Data pane under Measures or Dimensions (depending on what it returns)
7. Drag and drop it like any other field into your view

---

## Important Rules & Tips

| Rule                             | Why                                                             |
| -------------------------------- | --------------------------------------------------------------- |
| Use **square brackets** `[]`     | Tableau requires field names in brackets: `[Sales]`             |
| Match **field names exactly**    | Case-sensitive in Tableau: `[Sales]` ≠ `[sales]`                |
| Aggregation **mixing** is tricky | Can't mix aggregate and non-aggregate without proper wrapping   |
| Test with **small data** first   | Validate logic before applying on large datasets                |
| Use **comments** with `//`       | `// This is a comment` — helps document complex formulas        |
| Color-coded **editor**           | Tableau highlights syntax: blue for functions, green for fields |
| **No trailing semicolons**       | Tableau does not use `;` at the end of expressions              |
| Dimension vs Measure **output**  | A calculated field can return either, depending on the formula  |

---

## Common Beginner Mistakes

| Mistake                                                       | Correct Approach                                               |
| ------------------------------------------------------------- | -------------------------------------------------------------- |
| Using `IF [Sales] > AVG([Sales])` (mixes aggregate & row)     | Use `IF [Sales] > {AVG([Sales])}` (use LOD or window function) |
| Forgetting `END` in IF or CASE                                | Always close with `END`                                        |
| Using `=` instead of `==` (unlike SQL, Tableau uses `=` too)  | In Tableau, `=` works for equality in IF conditions            |
| Using `NULL` instead of `null` or `NULL` (not case-sensitive) | Tableau treats `NULL`, `Null`, `null` the same way             |
| Not handling nulls                                            | Use `IFNULL([Field], 0)` or `ZN([Field])` to avoid errors      |

---

## Summary

```
Calculated Field = Formula + Existing Data → New Insight
```

Calculated fields are one of the most powerful features in Tableau. They allow you to:

- Create new metrics not present in raw data
- Apply business logic and conditional rules
- Manipulate strings and dates
- Perform complex aggregations and table calculations
- Clean and transform data directly inside Tableau

**Key terms to remember:**

| Term                              | Category   | Purpose                  |
| --------------------------------- | ---------- | ------------------------ |
| `AND`                             | Logical    | Combine conditions       |
| `OR`                              | Logical    | Alternative conditions   |
| `IF / ELSEIF / ELSE / END`        | Logical    | Conditional branching    |
| `CASE / WHEN / THEN / ELSE / END` | Logical    | Exact value matching     |
| `IIF`                             | Logical    | Inline conditional       |
| `CEILING`                         | Number     | Round up                 |
| `FLOOR`                           | Number     | Round down               |
| `ROUND`                           | Number     | Round to decimal places  |
| `ABS`                             | Number     | Absolute value           |
| `SUM`                             | Aggregate  | Total                    |
| `AVG`                             | Aggregate  | Average                  |
| `COUNTD`                          | Aggregate  | Distinct count           |
| `DATEDIFF`                        | Date       | Difference between dates |
| `DATENAME`                        | Date       | Extract date name        |
| `RUNNING_SUM`                     | Table Calc | Cumulative total         |
| `IFNULL`                          | Logical    | Replace null with value  |
| `ZN`                              | Logical    | Null → Zero              |

---

> **Next Step**: Try creating a calculated field in Tableau using Sample Superstore:
>
> 1. Create `Profit Ratio` → `SUM([Profit]) / SUM([Sales])`
> 2. Create `Sales Tier` → `IF [Sales] > 1000 THEN "High" ELSE "Low" END`
> 3. Create `Order Month` → `DATENAME('month', [Order Date])`
> 4. Drag them into views and observe how they behave
