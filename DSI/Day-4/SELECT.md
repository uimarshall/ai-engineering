# SQL SELECT Statement Guide

---

## THE SELECT STATEMENT

The `SELECT` statement is the foundation of querying in SQL. It is used to retrieve data from one or more tables in a database. The `*` wildcard means "all columns" — so the query below returns every column and every row from the `product_areas` table.

```sql
SELECT * FROM grocery_db.product_areas;
```

> **When to use it:** Use `SELECT *` for quick exploration of a table's contents. In production code, it's best practice to name only the columns you need to avoid fetching unnecessary data.

---

## LIMIT

The `LIMIT` clause restricts how many rows are returned by a query. This is useful when you only need a sample of the data, or when working with very large tables where returning all rows would be slow and expensive.

The query below returns only the **first 3 rows** from the `product_areas` table.

```sql
SELECT * FROM grocery_db.product_areas LIMIT 3;
```

> **When to use it:** Use `LIMIT` when previewing data, debugging a query, or when you only need a top-N result set.

---

## ORDER BY

The `ORDER BY` clause sorts the result set by one or more columns. By default, sorting is **ascending (ASC)** — smallest to largest. Adding `DESC` reverses the order to **descending** — largest to smallest.

The query below sorts the `customer_details` table first by `distance_from_store` in **ascending** order (default). If two customers share the same `distance_from_store` value (a tie), they are then sorted by `credit_score` in **descending** order — so the customer with the higher credit score appears first.

```sql
SELECT *
FROM grocery_db.customer_details
ORDER BY distance_from_store, credit_score DESC;
```

> **Key points:**
>
> - Multiple sort columns are separated by commas.
> - `ASC`/`DESC` applies only to the column it directly follows.
> - The first column in `ORDER BY` is the **primary sort**; subsequent columns are **tiebreakers**.

---

## DISTINCT

The `DISTINCT` keyword filters the results so that only **unique (non-duplicate) values** are returned. It eliminates all duplicate rows from the output.

The query below returns all unique values of the `gender` column from `customer_details` — for example, just `Male` and `Female`, rather than repeating those values for every customer row.

```sql
SELECT DISTINCT gender FROM grocery_db.customer_details;
```

> **When to use it:** Use `DISTINCT` to understand what unique categories or values exist in a column, or when you need a deduplicated list.

---

## GIVING COLUMNS AN ALIAS

An **alias** gives a column a temporary, more readable name in the query output. Aliases are defined using the `AS` keyword. They do not change the actual column name in the database — they only affect how the column is labelled in the result set.

The query below renames `distance_from_store` to `distance_to_store` and `customer_id` to `customer_number` in the output.

```sql
SELECT
  distance_from_store AS distance_to_store,
  customer_id         AS customer_number
FROM grocery_db.customer_details;
```

> **When to use it:** Aliases improve readability, are essential when the column name is a computed expression, and are required when two joined tables share the same column name.

---

## CREATING NEW COLUMNS

SQL allows you to create **derived (calculated) columns** on the fly within a `SELECT` statement — they do not need to exist in the database. You can use:

- A **constant value** (e.g. `1 AS new_col`) — useful for adding a fixed flag or placeholder column.
- A **mathematical expression** (e.g. `distance_from_store * 1.5`) — useful for unit conversions, calculations, or transformations.

The query below returns the original columns with aliases, adds a constant column `new_col` with the value `1` in every row, and calculates a new column `distance_from_store_km` by multiplying `distance_from_store` by `1.5`.

```sql
SELECT
  distance_from_store AS distance_to_store,
  customer_id         AS customer_number,
  1                   AS new_col,
  distance_from_store * 1.5 AS distance_from_store_km
FROM grocery_db.customer_details;
```

> **Key points:**
>
> - Derived columns only exist in the query result — they are never written back to the table.
> - You can use any arithmetic operator (`+`, `-`, `*`, `/`) to build expressions.
> - Always give calculated columns a meaningful alias so the output is self-documenting.

---

## DISTINCT — Returning Unique Values from a Specific Column

Building on the `DISTINCT` concept above, you can use it on any column to retrieve a clean list of all unique values that exist in that column across the entire table.

The query below returns a list of every **unique `credit_score` value** present in the `customer_details` table — with no duplicates.

```sql
SELECT DISTINCT credit_score FROM grocery_db.customer_details;
```

> **Practical use case:** This is a quick way to audit what values are actually stored in a column before writing filter conditions (e.g. in a `WHERE` clause), or to understand the range and variety of data without running an aggregation.

---
