# Exporting Data with Pandas: A Beginner's Guide

## Table of Contents

1. [What Does "Exporting Data" Mean?](#what-does-exporting-data-mean)
2. [Why Do We Export Data?](#why-do-we-export-data)
3. [Common Export Formats](#common-export-formats)
4. [Code Examples](#code-examples)
5. [Real-World Company Use Cases](#real-world-company-use-cases)
6. [Best Practices](#best-practices)
7. [Common Mistakes to Avoid](#common-mistakes-to-avoid)

---

## What Does "Exporting Data" Mean?

Imagine you have a spreadsheet full of sales numbers, customer names, and product details. You've been cleaning it up, filtering it, and doing calculations in Python using **pandas** (a powerful data tool). Now you need to share that cleaned data with your boss, upload it to a database, or send it to another program.

**Exporting data** simply means: _taking the data from Python/pandas and saving it into a file that other people or programs can read._

Think of it like baking a cake (your analysis) and then putting it in a box (the file format) so you can deliver it to someone else.

---

## Why Do We Export Data?

In a real company, you rarely work alone with data. Here's why exporting matters:

| Reason                    | Example                                                     |
| ------------------------- | ----------------------------------------------------------- |
| **Sharing results**       | Send a clean Excel file to your manager                     |
| **Feeding other systems** | Upload processed data to a company database                 |
| **Creating reports**      | Generate monthly sales CSVs for the finance team            |
| **Backup**                | Save cleaned data before making more changes                |
| **Automation**            | Schedule a script that exports a daily report automatically |

---

## Common Export Formats

Pandas can export to many file types. Here are the most common ones you'll see in a company:

| Format      | File Extension  | Best For                                    | When to Use It                                 |
| ----------- | --------------- | ------------------------------------------- | ---------------------------------------------- |
| **CSV**     | `.csv`          | Simple tables, universal compatibility      | Sharing data between teams, loading into Excel |
| **Excel**   | `.xlsx`         | Formatted spreadsheets with multiple sheets | Management reports, presentations              |
| **JSON**    | `.json`         | Web applications, APIs                      | Sending data to websites or mobile apps        |
| **SQL**     | Database tables | Storing in company databases                | Permanent storage, other apps can query it     |
| **Parquet** | `.parquet`      | Big data, fast reading/writing              | Large datasets, data engineering pipelines     |
| **Pickle**  | `.pkl`          | Saving Python objects exactly as they are   | Temporary storage between Python scripts       |

---

## Code Examples

### Setup: Creating Sample Data

Before we export anything, let's create a simple dataset to work with. Imagine this is customer sales data from an online store:

```python
import pandas as pd

# Create sample data (imagine this came from a database or CSV you cleaned)
data = {
    'customer_id': [101, 102, 103, 104, 105],
    'name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 'Evan Wright'],
    'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Laptop'],
    'quantity': [1, 2, 1, 1, 1],
    'price': [1200.00, 25.99, 89.50, 300.00, 1150.00],
    'purchase_date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19']
}

df = pd.DataFrame(data)

# Convert date column to proper date format
df['purchase_date'] = pd.to_datetime(df['purchase_date'])

print(df)
print(f"\nOur DataFrame has {len(df)} rows and {len(df.columns)} columns.")
```

---

### 1. Exporting to CSV

**CSV (Comma-Separated Values)** is the most common format. It's just text with commas separating each value. Every program can read it.

```python
# Basic CSV export
df.to_csv('sales_data.csv', index=False)

# What does index=False mean?
# Pandas adds row numbers (0, 1, 2...) by default.
# index=False says "don't save those numbers as a column."
```

**Common options you should know:**

```python
# Export with custom separator (use semicolon instead of comma)
df.to_csv('sales_data_semicolon.csv', sep=';', index=False)

# Export only specific columns
df[['name', 'product', 'price']].to_csv('customer_summary.csv', index=False)

# Export without the header row (useful for appending to existing files)
df.to_csv('sales_data_no_header.csv', header=False, index=False)

# Handle special characters (like names with accents)
df.to_csv('sales_data_utf8.csv', encoding='utf-8', index=False)
```

**💡 Beginner Tip:** Always use `index=False` unless you specifically need row numbers. It keeps your file cleaner.

---

### 2. Exporting to Excel

**Excel files (.xlsx)** are what your manager probably wants to see. Pandas can create real Excel spreadsheets.

```python
# Basic Excel export
df.to_excel('sales_report.xlsx', sheet_name='January Sales', index=False)
```

**Multiple sheets in one Excel file** (very common in companies!):

```python
# Create two DataFrames (imagine one is for January, one for February)
january_sales = df.copy()
february_sales = df.copy()
february_sales['purchase_date'] = february_sales['purchase_date'] + pd.DateOffset(months=1)

# Write multiple sheets to one Excel file
with pd.ExcelWriter('quarterly_sales.xlsx', engine='openpyxl') as writer:
    january_sales.to_excel(writer, sheet_name='January', index=False)
    february_sales.to_excel(writer, sheet_name='February', index=False)

print("Excel file with multiple sheets created!")
```

**What is `ExcelWriter`?**
Think of it like a pen that can write on multiple pages of a notebook. The `with` statement makes sure the file is properly closed when done.

---

### 3. Exporting to JSON

**JSON (JavaScript Object Notation)** is the language of the web. If your company has a website or mobile app, they probably use JSON to move data around.

```python
# Basic JSON export
df.to_json('sales_data.json', orient='records', indent=4)

# orient='records' creates: [{"column": "value"}, {"column": "value"}]
# indent=4 makes it pretty and readable (with spaces)
```

**Different JSON formats:**

```python
# 'records' format - list of objects (most common for APIs)
df.to_json('sales_records.json', orient='records', indent=2)

# 'index' format - each row number is a key
df.to_json('sales_index.json', orient='index', indent=2)

# 'columns' format - each column is a key
df.to_json('sales_columns.json', orient='columns', indent=2)
```

**Example of what `orient='records'` looks like:**

```json
[
  { "customer_id": 101, "name": "Alice Johnson", "product": "Laptop" },
  { "customer_id": 102, "name": "Bob Smith", "product": "Mouse" }
]
```

---

### 4. Exporting to SQL (Databases)

In companies, data often lives in databases like **MySQL**, **PostgreSQL**, or **SQLite**. Pandas can send your DataFrame directly into a database table.

```python
from sqlalchemy import create_engine

# For SQLite (a simple file-based database - great for learning!)
engine = create_engine('sqlite:///company_database.db')

# Export DataFrame to SQL table
df.to_sql('sales_table', engine, if_exists='replace', index=False)

print("Data saved to SQLite database!")
```

**The `if_exists` parameter is important:**

| Option      | What It Does                          | When to Use                                          |
| ----------- | ------------------------------------- | ---------------------------------------------------- |
| `'fail'`    | Raises an error if table exists       | Safety first - don't overwrite accidentally          |
| `'replace'` | Deletes old table and creates new one | When you want fresh data                             |
| `'append'`  | Adds rows to existing table           | When building up data over time (like daily imports) |

**Real company example with PostgreSQL:**

```python
# For a real company database (you'll need the connection details from IT)
# engine = create_engine('postgresql://username:password@host:port/database')

# df.to_sql('daily_sales', engine, if_exists='append', index=False)
```

---

### 5. Exporting to Parquet

**Parquet** is a modern format designed for big data. It's smaller and faster than CSV, but not every program can read it. Data teams love it.

```python
# Export to Parquet
df.to_parquet('sales_data.parquet', engine='pyarrow', index=False)

# You can also compress it to save space
df.to_parquet('sales_data_compressed.parquet', engine='pyarrow', compression='snappy')
```

**When to use Parquet:**

- Your file is very large (millions of rows)
- You're working in a data pipeline (like Apache Spark)
- You need to preserve data types exactly (dates stay as dates, not text)

---

### 6. Exporting to Pickle

**Pickle** saves the exact Python object. It's like putting your DataFrame in a time capsule.

```python
# Save DataFrame as pickle
df.to_pickle('sales_data.pkl')

# Later, you can load it back EXACTLY as it was
df_loaded = pd.read_pickle('sales_data.pkl')
```

**⚠️ Warning:** Only use pickle for temporary storage between your own Python scripts. Don't share pickle files with others - they can contain malicious code.

---

## Real-World Company Use Cases

### Use Case 1: The Daily Sales Report

**Scenario:** Every morning at 8 AM, the sales database is updated. The sales manager wants an Excel file in their inbox.

```python
import pandas as pd
from sqlalchemy import create_engine

# Connect to company database
engine = create_engine('postgresql://user:pass@company-db:5432/sales')

# Pull yesterday's data
query = """
SELECT * FROM transactions
WHERE date = CURRENT_DATE - INTERVAL '1 day'
"""
yesterday_sales = pd.read_sql(query, engine)

# Export to Excel for the manager
yesterday_sales.to_excel(f"daily_report_{pd.Timestamp.today().strftime('%Y-%m-%d')}.xlsx",
                         index=False)
```

---

### Use Case 2: The Marketing Email List

**Scenario:** The marketing team needs a clean CSV of customer emails for a newsletter campaign.

```python
# Assume we have a customer DataFrame with some missing emails
customers = pd.read_csv('all_customers.csv')

# Clean the data
email_list = customers[['email', 'first_name', 'last_name']].dropna()

# Export only what marketing needs
email_list.to_csv('marketing_email_list.csv', index=False)

print(f"Exported {len(email_list)} valid email addresses for marketing.")
```

---

### Use Case 3: The API Data Feed

**Scenario:** Your company's mobile app needs product data in JSON format.

```python
# Get latest product information
products = pd.read_sql("SELECT * FROM products WHERE active = 1", engine)

# Export as JSON for the app developers
products.to_json('api_products.json', orient='records', indent=2)

# The app team can now read this file and display products in the mobile app
```

---

### Use Case 4: The Monthly Financial Backup

**Scenario:** Finance needs all transactions from last month saved permanently.

```python
# Get last month's data
last_month = pd.Timestamp.now() - pd.DateOffset(months=1)
month_name = last_month.strftime('%B_%Y')

# Export to Parquet for efficient storage
monthly_data.to_parquet(f'finance_backup_{month_name}.parquet', index=False)

# Also create a human-readable Excel summary for auditors
summary = monthly_data.groupby('department')['amount'].sum().reset_index()
summary.to_excel(f'finance_summary_{month_name}.xlsx', index=False)
```

---

### Use Case 5: The Data Pipeline Handoff

**Scenario:** Your script cleans data, then another script analyzes it. They need to pass data between them.

```python
# Script 1: clean_data.py
raw_data = pd.read_csv('messy_data.csv')
cleaned = raw_data.dropna().drop_duplicates()
cleaned.to_parquet('cleaned_data.parquet', index=False)  # Fast and type-safe

# Script 2: analyze_data.py (runs later)
cleaned = pd.read_parquet('cleaned_data.parquet')
# Now do analysis...
```

---

## Best Practices

### 1. Always Check Your File After Exporting

```python
# After exporting, read it back to make sure it worked!
df.to_csv('myfile.csv', index=False)

# Verify
df_check = pd.read_csv('myfile.csv')
print(df_check.head())  # Does it look right?
```

### 2. Use Meaningful File Names

```python
# Bad
df.to_csv('data.csv')

# Good
df.to_csv('sales_q1_2024_cleaned.csv')
```

### 3. Handle Dates Carefully

Dates can be tricky. Excel and CSV store dates as text by default.

```python
# When exporting to CSV, dates become text. That's usually fine.
# When exporting to Excel, pandas preserves date formatting.
# When exporting to Parquet, dates stay as real dates.
```

### 4. Be Careful with Large Files

```python
# If your DataFrame has millions of rows, CSV will be slow
# Use Parquet instead for large datasets
big_df.to_parquet('big_data.parquet', index=False)
```

### 5. Create Output Folders

```python
import os

# Create a folder for exports if it doesn't exist
os.makedirs('output', exist_ok=True)
df.to_csv('output/sales_data.csv', index=False)
```

---

## Common Mistakes to Avoid

| Mistake                                     | Why It Happens                             | How to Fix                                                        |
| ------------------------------------------- | ------------------------------------------ | ----------------------------------------------------------------- |
| **Forgetting `index=False`**                | Pandas saves row numbers as a column       | Always add `index=False` unless you need row numbers              |
| **Overwriting important files**             | Using `if_exists='replace'` carelessly     | Use `if_exists='fail'` first to check, or backup your data        |
| **Encoding issues with special characters** | Names like "José" or "北京" get garbled    | Add `encoding='utf-8'` to CSV exports                             |
| **Losing date formats**                     | Dates become plain text in CSV             | Use Excel or Parquet if dates must stay formatted                 |
| **Memory errors with huge files**           | Trying to export millions of rows to Excel | Excel has a ~1 million row limit. Use CSV or Parquet for big data |
| **Not closing database connections**        | Using `to_sql` without proper cleanup      | Use `with` statements or explicitly close connections             |

---

## Quick Reference Cheat Sheet

```python
# CSV
df.to_csv('file.csv', index=False)

# Excel
df.to_excel('file.xlsx', sheet_name='Sheet1', index=False)

# JSON
df.to_json('file.json', orient='records', indent=2)

# SQL
from sqlalchemy import create_engine
engine = create_engine('sqlite:///database.db')
df.to_sql('table_name', engine, if_exists='replace', index=False)

# Parquet
df.to_parquet('file.parquet', index=False)

# Pickle
df.to_pickle('file.pkl')
```

---

## Summary

Exporting data with pandas is like choosing the right envelope for your letter:

- **CSV** = The standard white envelope (everyone can open it)
- **Excel** = The fancy envelope with a window (managers love it)
- **JSON** = The digital envelope for apps and websites
- **SQL** = The safety deposit box (permanent company storage)
- **Parquet** = The compression bag (for big, heavy data)
- **Pickle** = The sealed time capsule (Python-only temporary storage)

**Remember:** The goal of exporting is to make your data useful to others. Always think about _who_ will use the file and _what program_ they'll open it with. That will tell you which format to choose.

---

_Happy exporting! 🚀_
