# USEFUL TIPS & TRICKS (VOLUME 1)

---

## 1. Using Sub-Queries

### What is a Sub-Query?

A **sub-query** (also called an inner query or nested query) is a SQL query embedded inside another query.
The inner query runs first, returns a result, and the outer query uses that result as a filter or value.

Sub-queries are essential when you need a dynamically calculated value — such as the highest profit margin —
rather than hardcoding a number. This ensures your reports always reflect the current state of the business.

---

### Business Scenario

> **Goal:** The grocery chain's leadership team wants to identify **which product departments are achieving
> the highest profit margins** so they can double down on marketing those categories, negotiate better
> supplier contracts, and replicate success across underperforming departments.

---

```sql
SELECT
    product_area_name,   -- The name of the product department (e.g., "Bakery", "Produce", "Dairy")
    profit_margin        -- The calculated profit margin for that department (e.g., 0.35 means 35%)

FROM
    grocery_db.product_areas   -- Source table containing all product departments and their financial metrics

WHERE
    -- Filter to return only the department(s) with the single highest profit margin.
    -- The sub-query (inner SELECT) runs first:
    --   it sorts all rows in product_areas by profit_margin in descending order (highest first)
    --   LIMIT 1 picks only the very top value
    -- The outer query then returns every row whose profit_margin equals that top value.
    -- NOTE: Using ORDER BY + LIMIT 1 handles ties better than MAX() alone,
    -- because MAX() also handles ties — but this pattern is explicit and readable.
    profit_margin = (
        SELECT profit_margin          -- Return only the profit_margin column value
        FROM grocery_db.product_areas -- Same table as the outer query
        ORDER BY profit_margin DESC   -- Sort highest margin to the top
        LIMIT 1                       -- Take only the single highest value
    );
```

### Line-by-Line Breakdown

| Line                                      | Purpose                                                                       |
| ----------------------------------------- | ----------------------------------------------------------------------------- |
| `SELECT product_area_name, profit_margin` | Choose which columns to display in the final result                           |
| `FROM grocery_db.product_areas`           | Specify the table containing product department data                          |
| `WHERE profit_margin = (...)`             | Filter rows — only keep departments whose margin matches the sub-query result |
| `SELECT profit_margin` _(inner)_          | Return the margin value from inside the sub-query                             |
| `FROM grocery_db.product_areas` _(inner)_ | Same table — the sub-query looks within the same data                         |
| `ORDER BY profit_margin DESC`             | Sort all margins from highest to lowest                                       |
| `LIMIT 1`                                 | Take only the top (highest) value                                             |

### Business Impact

- Instantly surfaces the **most profitable departments** without manually checking numbers.
- If margins change weekly (e.g., seasonal produce), re-running this query always returns the current leader.
- Leadership can benchmark all other departments against the top performer to set profitability targets.

---

## 2. Using LEAD & LAG (Window Functions for Time-Based Analysis)

### What are LEAD & LAG?

`LAG()` looks **backwards** in time — it retrieves a value from a previous row within the same partition.  
`LEAD()` looks **forwards** in time — it retrieves a value from a future row within the same partition.

Both are **window functions**, meaning they calculate across a set of rows related to the current row
without collapsing the result into a single grouped value.

---

### Business Scenario

> **Goal:** The analytics team wants to understand **customer purchase frequency and shopping gaps**.
> By knowing how many days pass between visits, the company can:
>
> - Identify customers who are shopping less frequently (churn risk)
> - Trigger personalised promotions before customers drift to a competitor
> - Measure the impact of loyalty campaigns on visit cadence

---

### Step 1 — Build the Temporary Table

```sql
-- Create a temporary table to hold a clean, deduplicated transaction log
-- for specific customers. Temp tables exist only for the current session.
CREATE TEMP TABLE cust_trans AS (

    SELECT
        DISTINCT                  -- Remove duplicate rows (same customer + transaction + date)
        customer_id,              -- Unique identifier for each customer
        transaction_id,           -- Unique identifier for each individual transaction/visit
        transaction_date          -- The calendar date the transaction occurred

    FROM grocery_db.transactions  -- Source table containing all store transactions

    WHERE
        customer_id IN (1, 2)     -- Filter to only two customers for this analysis (scalable to all)
);
```

### Line-by-Line Breakdown (CREATE TEMP TABLE)

| Line                                    | Purpose                                                                                                         |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `CREATE TEMP TABLE cust_trans AS (...)` | Creates a temporary table named `cust_trans` from the query result; exists only this session                    |
| `SELECT DISTINCT`                       | Eliminates duplicate records — ensures one row per unique customer + transaction + date combination             |
| `customer_id`                           | The customer being tracked                                                                                      |
| `transaction_id`                        | Identifies each shopping trip uniquely                                                                          |
| `transaction_date`                      | The date of each visit — required for time-based lag/lead calculations                                          |
| `FROM grocery_db.transactions`          | Pull raw transaction data from the main transactions table                                                      |
| `WHERE customer_id IN (1, 2)`           | Scope the analysis to two specific customers; replace with any customer list or remove filter for all customers |

---

### Step 2 — Apply LEAD & LAG

```sql
SELECT
    *,                            -- Return all existing columns from cust_trans

    -- LAG offset 1: The transaction date of the PREVIOUS visit (1 row back)
    -- Useful to calculate "days since last visit"
    LAG(transaction_date, 1) OVER (
        PARTITION BY customer_id              -- Restart the window for each customer independently
        ORDER BY transaction_date, transaction_id  -- Order visits chronologically; use transaction_id as tiebreaker
    ) AS transaction_date_lag1,

    -- LAG offset 2: The transaction date TWO visits ago (2 rows back)
    -- Useful for identifying whether a customer's visit frequency is accelerating or slowing
    LAG(transaction_date, 2) OVER (
        PARTITION BY customer_id
        ORDER BY transaction_date, transaction_id
    ) AS transaction_date_lag2,

    -- LEAD offset 1: The transaction date of the NEXT visit (1 row ahead)
    -- Useful for calculating "days until next visit" or flagging customers who never returned
    LEAD(transaction_date, 1) OVER (
        PARTITION BY customer_id
        ORDER BY transaction_date, transaction_id
    ) AS transaction_date_lead1

FROM cust_trans;   -- Query from the temporary table built in Step 1
```

### Line-by-Line Breakdown (LEAD & LAG Query)

| Line                                        | Purpose                                                                                  |
| ------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `SELECT *`                                  | Include all original columns (customer_id, transaction_id, transaction_date)             |
| `LAG(transaction_date, 1) OVER (...)`       | Pull the transaction date from 1 row behind — i.e., the previous visit                   |
| `LAG(transaction_date, 2) OVER (...)`       | Pull the transaction date from 2 rows behind — the visit before last                     |
| `LEAD(transaction_date, 1) OVER (...)`      | Pull the transaction date from 1 row ahead — the next future visit                       |
| `PARTITION BY customer_id`                  | Ensures the window resets per customer — Customer 1's rows don't bleed into Customer 2's |
| `ORDER BY transaction_date, transaction_id` | Sort visits in chronological order; transaction_id breaks ties on same-day visits        |
| `AS transaction_date_lag1`                  | Alias the column with a descriptive name                                                 |
| `FROM cust_trans`                           | Use the cleaned temp table from Step 1                                                   |

### Business Impact

- Calculate **days between visits**: `transaction_date - transaction_date_lag1`
- Flag customers whose visit gap is **growing** (potential churn) vs. shrinking (engagement improving)
- Power **re-engagement campaigns**: if `transaction_date_lead1` is NULL, the customer never returned — trigger a win-back offer
- Compare visit frequency before and after a promotion to measure campaign ROI

---

## 3. Rounding Data

### What is ROUND()?

`ROUND(value, decimal_places)` rounds a numeric value to a specified number of decimal places.

- Positive integer: round to that many decimal places (e.g., `ROUND(3.456, 1)` → `3.5`)
- Zero: round to the nearest whole number (e.g., `ROUND(3.456, 0)` → `3`)

---

### Business Scenario

> **Goal:** The finance team needs a **clean, readable sales report** for the board of directors.
> Raw transaction data often contains long decimal values (e.g., £12.3748291) that are difficult
> to read in dashboards and reports. Rounding ensures:
>
> - Consistent formatting across all financial outputs
> - Easier mental arithmetic when comparing figures
> - Cleaner exports to Excel or BI tools like Power BI / Tableau

---

```sql
SELECT
    *,                                    -- Return all original columns from the transactions table

    ROUND(sales_cost, 1) AS sales_cost_round1,
    -- Round sales_cost to 1 decimal place (e.g., 12.3748 → 12.4)
    -- Good for operational reports where some precision is needed but full decimals are noisy

    ROUND(sales_cost, 0) AS sales_cost_round0
    -- Round sales_cost to 0 decimal places / nearest whole number (e.g., 12.3748 → 12)
    -- Good for executive summaries, KPI dashboards, or comparing £ values at a high level

FROM grocery_db.transactions   -- Source table with individual transaction line items

WHERE customer_id = 1;         -- Filter to a single customer; remove this line to apply across all customers
```

### Line-by-Line Breakdown

| Line                           | Purpose                                                           |
| ------------------------------ | ----------------------------------------------------------------- |
| `SELECT *`                     | Include all original transaction columns for full context         |
| `ROUND(sales_cost, 1)`         | Rounds the `sales_cost` value to 1 decimal place                  |
| `AS sales_cost_round1`         | Names the new column clearly to distinguish it from the raw value |
| `ROUND(sales_cost, 0)`         | Rounds to nearest whole number — drops all decimals               |
| `AS sales_cost_round0`         | Names the whole-number rounded column                             |
| `FROM grocery_db.transactions` | The source table for transaction-level sales data                 |
| `WHERE customer_id = 1`        | Narrows the result to one specific customer's purchase history    |

### Business Impact

- Produce **board-ready reports** without post-processing in Excel
- Standardise rounding rules across all SQL queries to avoid inconsistent figures in different reports
- Reduce cognitive load when analysts review hundreds of transaction rows

---

## 4. Random Sampling

### What is Random Sampling in SQL?

`ORDER BY RANDOM()` assigns a random sort value to each row, shuffling the dataset.
Combined with `LIMIT`, it returns a random subset of rows — a statistical sample.

---

### Business Scenario

> **Goal:** The data science team wants to run a **customer survey or A/B marketing test**
> but cannot contact all 500,000 customers. They need a representative random sample of 100 customers to:
>
> - Test a new loyalty programme offer without full rollout risk
> - Validate a predictive churn model on unseen data
> - Survey customers about product satisfaction before a competitor launches a rival product

---

```sql
SELECT
    *                              -- Return all columns for the selected customers
                                   -- (e.g., customer_id, age, location, loyalty_tier)

FROM
    grocery_db.customer_details    -- Source table containing customer demographic and profile data

ORDER BY
    RANDOM()                       -- Assign a random value to each row, effectively shuffling all rows
                                   -- Every time this query runs, the order (and therefore the sample) is different

LIMIT
    100;                           -- After shuffling, take only the first 100 rows
                                   -- This gives a random sample of 100 customers
```

### Line-by-Line Breakdown

| Line                               | Purpose                                                                     |
| ---------------------------------- | --------------------------------------------------------------------------- |
| `SELECT *`                         | Retrieve all customer attributes for each sampled customer                  |
| `FROM grocery_db.customer_details` | The table holding customer profiles and demographic data                    |
| `ORDER BY RANDOM()`                | Randomises the row order — each execution produces a different shuffle      |
| `LIMIT 100`                        | Caps the result at 100 rows, taking the first 100 from the randomised order |

### Business Impact

- Enables **statistically valid A/B testing** without expensive third-party tools
- Avoids selection bias — no human pattern influences which customers are chosen
- Can be extended: `WHERE loyalty_tier = 'Gold' ORDER BY RANDOM() LIMIT 50` for stratified sampling by customer tier
- Protects against competitors noticing patterns if you always contact the same group

---

## 5. Extracting Parts of a Date

### What is DATE_PART()?

`DATE_PART('unit', date_column)` extracts a specific component of a date/timestamp.
Common units: `'day'`, `'month'`, `'year'`, `'dow'` (day of week: 0=Sunday, 6=Saturday), `'hour'`, `'quarter'`

---

### Business Scenario

> **Goal:** The commercial team wants to analyse **seasonal and weekly shopping patterns** to:
>
> - Stock shelves more efficiently before peak days (e.g., Saturdays, December)
> - Plan promotions around high-traffic periods to maximise basket size
> - Benchmark year-over-year revenue growth to prove the business is staying competitive
> - Identify the quietest trading days to schedule store maintenance or staff training

---

```sql
SELECT
    DISTINCT                                        -- Return each unique date once (no duplicates)

    transaction_date,                               -- The full original date (e.g., 2024-03-15)

    DATE_PART('day', transaction_date)   AS day,
    -- Extract the day number of the month (1–31)
    -- e.g., 2024-03-15 → 15
    -- Use: identify which days of the month are busiest (e.g., around payday)

    DATE_PART('month', transaction_date) AS month,
    -- Extract the month number (1–12)
    -- e.g., 2024-03-15 → 3 (March)
    -- Use: monthly trend analysis, seasonal stocking, year-on-year comparison

    DATE_PART('year', transaction_date)  AS year,
    -- Extract the 4-digit year
    -- e.g., 2024-03-15 → 2024
    -- Use: year-over-year growth analysis, multi-year trend reporting

    DATE_PART('dow', transaction_date)   AS dayofweek
    -- Extract the day of week as a number (0=Sunday, 1=Monday, ..., 6=Saturday)
    -- e.g., a Friday → 5
    -- Use: identify peak shopping days, optimise staffing rotas, plan weekend promotions

FROM
    grocery_db.transactions   -- Source table with all transaction records

ORDER BY
    transaction_date;         -- Sort results chronologically for clean, readable output
```

### Line-by-Line Breakdown

| Line                                              | Purpose                                                              |
| ------------------------------------------------- | -------------------------------------------------------------------- |
| `SELECT DISTINCT`                                 | Deduplicate — return each date once rather than once per transaction |
| `transaction_date`                                | Keep the full original date for reference and context                |
| `DATE_PART('day', transaction_date) AS day`       | Extract just the day-of-month number                                 |
| `DATE_PART('month', transaction_date) AS month`   | Extract just the month number                                        |
| `DATE_PART('year', transaction_date) AS year`     | Extract just the year                                                |
| `DATE_PART('dow', transaction_date) AS dayofweek` | Extract numeric day of week (0=Sun through 6=Sat)                    |
| `FROM grocery_db.transactions`                    | Raw transaction data source                                          |
| `ORDER BY transaction_date`                       | Present results in date order for easy chronological review          |

### Business Impact

- Build **monthly revenue reports** by grouping on the extracted `month` and `year`
- Create **heatmaps of busy trading hours/days** to optimise staffing and avoid costly understaffing on peak days
- Run year-over-year comparisons: `WHERE year IN (2023, 2024)` to measure growth and maintain competitive positioning
- Identify **seasonal demand patterns** (e.g., December spikes) to negotiate better bulk-buy supplier contracts

---

## 6. Working with Strings / Text

### What are String Functions?

SQL provides a rich set of functions to manipulate and transform text data stored in columns.
These are critical for **data cleaning**, **standardisation**, and **presentation**.

| Function        | Description                          | Example                                                     |
| --------------- | ------------------------------------ | ----------------------------------------------------------- |
| `UPPER()`       | Convert text to ALL CAPS             | `'dairy'` → `'DAIRY'`                                       |
| `LOWER()`       | Convert text to all lowercase        | `'DAIRY'` → `'dairy'`                                       |
| `CHAR_LENGTH()` | Count the number of characters       | `'Bakery'` → `6`                                            |
| `CONCAT()`      | Join two or more strings together    | `'Bakery' + ' - ' + 'Department'` → `'Bakery - Department'` |
| `SUBSTRING()`   | Extract part of a string by position | `'Bakery'` from pos 3, length 3 → `'ker'`                   |
| `REPEAT()`      | Repeat a string N times              | `'Bakery'` × 2 → `'BakeryBakery'`                           |

---

### Business Scenario

> **Goal:** The marketing team is building a **product catalogue export** for:
>
> - A new e-commerce website where category names must be consistently formatted
> - Integration with a third-party loyalty platform that requires UPPERCASE department codes
> - A printed in-store signage system that has character-length restrictions per label
> - Branded department headers that follow a standard "Name - Department" format

---

```sql
SELECT
    product_area_name,
    -- Original department name exactly as stored in the database (e.g., "Bakery", "Fresh Produce")

    UPPER(product_area_name) AS pan_upper,
    -- Convert the name to ALL UPPERCASE letters
    -- e.g., "Bakery" → "BAKERY"
    -- Use: generate department codes for external systems, headers in printed reports

    LOWER(product_area_name) AS pan_lower,
    -- Convert the name to all lowercase letters
    -- e.g., "Fresh Produce" → "fresh produce"
    -- Use: URL slugs for the e-commerce website, case-insensitive comparison/matching

    CHAR_LENGTH(product_area_name) AS pan_length,
    -- Count the total number of characters in the name (including spaces)
    -- e.g., "Bakery" → 6, "Fresh Produce" → 13
    -- Use: validate names against character limits (e.g., signage label max 10 chars),
    --      flag departments with excessively long names that need shortening

    CONCAT(product_area_name, ' - ', 'Department') AS pan_concat,
    -- Combine the department name with a fixed suffix string
    -- e.g., "Bakery" → "Bakery - Department"
    -- Use: generate standardised display labels for dashboards and customer-facing menus

    SUBSTRING(product_area_name, 3, 6) AS pan_substring,
    -- Extract a portion of the text: start at character position 3, take 6 characters
    -- e.g., "Bakery" → starting at 'k' (pos 3), take 6 chars → "kery" (fewer if string is shorter)
    -- Use: generate abbreviated department codes, extract standardised prefixes from product SKUs

    REPEAT(product_area_name, 2) AS pan_repeat
    -- Repeat the department name twice (concatenated with no separator)
    -- e.g., "Bakery" → "BakeryBakery"
    -- Use: niche formatting tasks, generating test/dummy data, creating visual separators

FROM
    grocery_db.product_areas;
    -- Source table containing one row per product department with name and financial metrics
```

### Line-by-Line Breakdown

| Line                                                           | Purpose                                                                |
| -------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `product_area_name`                                            | The raw, unmodified department name — kept as a reference baseline     |
| `UPPER(product_area_name) AS pan_upper`                        | Uppercase version — for systems requiring standardised caps formatting |
| `LOWER(product_area_name) AS pan_lower`                        | Lowercase version — for URLs, slugs, or case-insensitive joins         |
| `CHAR_LENGTH(product_area_name) AS pan_length`                 | Number of characters — useful for validation and truncation checks     |
| `CONCAT(product_area_name, ' - ', 'Department') AS pan_concat` | Builds a formatted label by joining strings with a separator           |
| `SUBSTRING(product_area_name, 3, 6) AS pan_substring`          | Extracts 6 characters starting from position 3 of the name             |
| `REPEAT(product_area_name, 2) AS pan_repeat`                   | Duplicates the name string twice end-to-end                            |
| `FROM grocery_db.product_areas`                                | The product departments reference table                                |

### Business Impact

- **Standardise data** before loading into downstream systems (e.g., CRM, e-commerce platform, ERP)
- Catch **data quality issues** using `CHAR_LENGTH` — flag departments whose names are too long or too short
- Generate **consistent formatted labels** for automated reporting pipelines without manual Excel cleanup
- Enable **reliable text-based joins** using `LOWER()` to avoid mismatches due to inconsistent casing across systems

---

## Summary Reference Table

| Technique        | Key Function(s)                        | Primary Business Use                                                       |
| ---------------- | -------------------------------------- | -------------------------------------------------------------------------- |
| Sub-Queries      | Nested `SELECT`                        | Dynamically find top/bottom performers without hardcoding values           |
| Lead & Lag       | `LAG()`, `LEAD()`                      | Track customer visit frequency, detect churn risk, measure campaign impact |
| Rounding         | `ROUND()`                              | Clean financial reporting for boards, dashboards, and exports              |
| Random Sampling  | `ORDER BY RANDOM() LIMIT n`            | A/B testing, surveys, model validation without full dataset                |
| Date Parts       | `DATE_PART()`                          | Seasonal analysis, staffing optimisation, year-over-year benchmarking      |
| String Functions | `UPPER()`, `LOWER()`, `CONCAT()`, etc. | Data standardisation, catalogue formatting, downstream system integration  |
