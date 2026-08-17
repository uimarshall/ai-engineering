# Day 47: Creating Pandas DataFrames And Importing Data (Python)

> **Prerequisite:** Day 46 (Introduction to Pandas). Companion practice file: `201_Creating_Pandas_DataFrames.py` — run it and compare its output with the blocks below.

Day 46 showed you *what* a DataFrame is. Today we cover *where the data comes from*. There are only two ways data ever enters a DataFrame:

1. **Create** it in Python (from lists, dicts, Series, NumPy arrays…)
2. **Import** it from the outside world (CSV, Excel, JSON, SQL, HTML, Parquet…)

Master these and you are self-sufficient: whatever file your company throws at you, you can turn it into a DataFrame you can analyze.

---

## 1. Why This Is The #1 Skill (Value to a Company)

Almost no data arrives "ready". It sits in:

- CSV exports from banking / ERP systems
- Excel sheets emailed by managers
- JSON responses from apps and APIs
- Tables inside SQL databases
- Parquet files in data warehouses

**Industry rule of thumb: 60–80% of a data analyst's time is spent getting data into a usable shape** (import + cleaning). The rest is actual analysis — so this topic is not a side quest, it is the job.

| Value to a company | What it means in practice |
| --- | --- |
| **No bottlenecks** | You don't wait for an engineer to pull data for every question — you import it yourself in two lines of code |
| **Reproducible reports** | "Import → clean → report" becomes a script you re-run every Monday, instead of copy-pasting in Excel |
| **Handles company-sized data** | A 50 MB CSV that crashes laptop Excel is read by Pandas in seconds — and in chunks if it is 5 GB |
| **One skill, every source** | The same `DataFrame` works whether it came from SQL, Excel or an API, so charts, ML and dashboards all plug into it |
| **Automated pipelines** | `read_csv` → transform → `to_excel` is the heart of the nightly jobs that produce the company's KPI reports |

---

## 2. Creating DataFrames (data that already lives in Python)

### 2.1 From a dictionary — each key becomes a COLUMN (the default way)

```python
import pandas as pd

df = pd.DataFrame({
    "Product": ["Laptop", "Monitor", "Mouse", "Laptop"],
    "Region":  ["North", "South", "North", "East"],
    "Units":   [10, 8, 60, 5],
    "Price":   [1200, 220, 24, 1250],
})
print(df)
```

**Output:**

```
  Product Region  Units  Price
0  Laptop  North     10   1200
1 Monitor  South      8    220
2   Mouse  North     60     24
3  Laptop   East      5   1250
```

> 💡 **Rule:** all the lists must be the **same length** (one value per row). Different lengths → `ValueError`.

### 2.2 From a list of dictionaries — each dict becomes a ROW

This is the shape data has when it arrives from **APIs and JSON** — a list of "records":

```python
rows = [
    {"name": "Asha",  "dept": "Sales", "sales": 42000},
    {"name": "Ravi",  "dept": "Sales", "sales": 51000},
    {"name": "Meera", "dept": "IT",    "sales": 0},
]
df = pd.DataFrame(rows)
print(df)
```

**Output:**

```
    name   dept  sales
0   Asha  Sales  42000
1   Ravi  Sales  51000
2  Meera     IT      0
```

Bonus: the rows don't even need the same keys — missing values simply become `NaN`, so messy API responses still load.

### 2.3 From a single list → one column

```python
df = pd.DataFrame([100, 200, 300], columns=["Score"])
```

```
   Score
0    100
1    200
2    300
```

### 2.4 From a list of lists → rows + your own column names

```python
df = pd.DataFrame(
    [["North", 120], ["South", 90], ["East", 150]],
    columns=["Region", "Orders"],
)
```

```
  Region  Orders
0  North     120
1  South      90
2   East     150
```

### 2.5 From a Series

```python
s = pd.Series({"A": 1, "B": 2, "C": 3}, name="Value")
df = pd.DataFrame(s)
print(df)
```

```
   Value
A      1
B      2
C      3
```

The Series' index (`A, B, C`) becomes the DataFrame's index, and the Series' name becomes the column name.

### 2.6 From a NumPy array (fast, for numeric blocks)

```python
import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])
df = pd.DataFrame(arr, columns=["x", "y", "z"])
print(df)
```

```
   x  y  z
0  1  2  3
1  4  5  6
```

Useful when results come out of NumPy / scientific code and you want to attach column labels.

### 2.7 Custom index — real-world row labels

The default index is `0, 1, 2, …`, but real-world rows have **IDs**:

```python
df = pd.DataFrame(
    {"Product": ["Laptop", "Mouse"], "Units": [10, 60]},
    index=["SKU-001", "SKU-014"],
)
print(df)
```

```
        Product  Units
SKU-001  Laptop     10
SKU-014   Mouse     60
```

Now you can look up a row by its real ID: `df.loc["SKU-001"]`.

### 2.8 Controlling data types (dtype) at creation

By default Pandas **guesses** the type of every column:

```python
df = pd.DataFrame({"ID": [1, 2, 3], "Code": ["A", "B", "C"]})
print(df.dtypes)
```

```
ID      int64
Code      str        # pandas 3.x shows text columns as "str"
dtype: object
```

- **Whole frame:** `pd.DataFrame([[1, 2], [3, 4]], dtype="float32")`
- **Per column:** build first, then `.astype()` each column:

```python
df["ID"]   = df["ID"].astype("int8")
df["Code"] = df["Code"].astype("category")   # memory saver for repeated text
print(df.dtypes)
```

```
ID          int8
Code    category
dtype: object
```

> 💡 **Industry habit:** when *importing* a big file you can force per-column types directly with `pd.read_csv(..., dtype={"ID": "int8", "Region": "category"})` — much faster than converting after loading.

### 2.9 Building a DataFrame incrementally (the SAFE way)

**`df.append()` was removed in pandas 2.0.** The fast, safe pattern: **collect rows in a plain Python list, build the DataFrame ONCE at the end.**

```python
records = []
for order_id, amount in [(101, 250.50), (102, 80.00), (103, 410.25)]:
    records.append({"order_id": order_id, "amount": amount})

df = pd.DataFrame(records)   # build once, at the end
print(df)
```

```
   order_id  amount
0       101  250.50
1       102   80.00
2       103  410.25
```

Appending one row at a time inside a loop is slow (the whole table gets copied each time). The list-then-build pattern is what you'll see in real production code.

### 2.10 Which creation method do I use?

| Your data looks like… | Use |
| --- | --- |
| Columns: `{col: [values]}` | `pd.DataFrame(dict)` — the default choice |
| Records: `[{"a": 1}, {"a": 2}]` (API / JSON style) | `pd.DataFrame(list_of_dicts)` |
| One vector / list | `pd.DataFrame(list, columns=["name"])` |
| Rows as bare lists | `pd.DataFrame(list_of_lists, columns=[...])` |
| A NumPy array | `pd.DataFrame(array, columns=[...])` |
| Row labels matter (IDs, dates) | pass `index=[...]` |
| Growing over time / in a loop | collect in a list → build once |

---

## 3. Importing Data (reading files and sources)

### 3.1 CSV — the #1 business format

```python
df = pd.read_csv("sales_2026.csv")
print(df)
```

```
         Date  Product Region  Units  Unit_Price
0  2026-01-05   Laptop  North     10        1200
1  2026-01-12    Mouse  South     60          24
2  2026-02-03   Laptop   East      8        1250
3  2026-02-19  Monitor  North     15         220
4  2026-03-08    Mouse   East     40          25
5  2026-03-21   Laptop  South     12        1195
```

**The 7 `read_csv` options you'll actually use:**

| Option | What it does | Example |
| --- | --- | --- |
| `sep` | separator (default `,`) | `sep=";"` for European exports |
| `usecols` | read only some columns (faster, less RAM) | `usecols=["Product", "Region"]` |
| `parse_dates` | turn date columns into real dates at import | `parse_dates=["Date"]` |
| `dtype` | force column types | `dtype={"ID": "int8"}` |
| `encoding` | text encoding of the file | `encoding="latin-1"` |
| `na_values` | extra strings that count as missing | `na_values=["-", "N/A"]` |
| `chunksize` | read in pieces (huge files) | `chunksize=1000` |

```python
# Only the columns you need:
pd.read_csv("sales_2026.csv", usecols=["Product", "Region"])

# Real dates at import time:
df = pd.read_csv("sales_2026.csv", parse_dates=["Date"])
print(df.dtypes)   # Date -> datetime64[us]  (not str!)

# Semicolon files (super common in Europe / Excel exports):
pd.read_csv("europe_sales.csv", sep=";")
```

**Output of `usecols`:**

```
   Product Region
0   Laptop  North
1    Mouse  South
2   Laptop   East
3  Monitor  North
4    Mouse   East
5   Laptop  South
```

### 3.2 Encoding problems — the classic beginner error

Old Windows/Excel files are often saved as **latin-1 (cp1252)**, not utf-8. Reading them the default way throws:

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 14: invalid continuation byte
```

**Fix: tell Pandas the real encoding**

```python
pd.read_csv("notes_latin1.csv", encoding="latin-1")
```

```
    item  note
0   Café  good
1  Müsli    ok
```

> 💡 If the error mentions bytes like `0xe9`, `0xe8`, `0xfc` — the file is almost certainly latin-1. Try `encoding="latin-1"` first; for Asian languages try `"utf-8-sig"`, `"cp932"` or `"gbk"`.

### 3.3 Excel — `read_excel` (needs `openpyxl`)

```python
# Install once:  pip install openpyxl

df = pd.read_excel("sales_2026.xlsx")                       # first sheet
df = pd.read_excel("sales_2026.xlsx", sheet_name="Regions") # pick a sheet
df = pd.read_excel("budget.xlsx", sheet_name=None)          # ALL sheets -> dict of DataFrames
```

Writing multiple sheets in one file:

```python
with pd.ExcelWriter("sales_2026.xlsx") as writer:
    df_csv.to_excel(writer, sheet_name="Sales", index=False)
    region_orders.to_excel(writer, sheet_name="Regions", index=False)
```

Reading the second sheet back:

```python
print(pd.read_excel("sales_2026.xlsx", sheet_name="Regions"))
```

```
  Region  Orders
0  North      25
1  South      18
2   East      33
```

> ⚠️ Excel is **slow** and caps at ~1,048,576 rows. For big data exchange CSV or Parquet — keep Excel for *sharing* results, not for *loading* raw data.

### 3.4 JSON — how APIs and app data arrive

An e-commerce order API typically returns **nested** data (orders → items):

```python
orders = [
    {"id": 101, "items": [{"sku": "LAP-01", "qty": 2}, {"sku": "MSE-01", "qty": 1}]},
    {"id": 102, "items": [{"sku": "MON-02", "qty": 3}]},
]
```

Plain `pd.read_json("orders.json")` gives one row per order and leaves the nested `items` as an unhelpful blob. **The pro move is `json_normalize`**, which flattens nested lists into rows:

```python
df = pd.json_normalize(orders, record_path="items", meta=["id"])
print(df)
```

```
      sku  qty   id
0  LAP-01    2  101
1  MSE-01    1  101
2  MON-02    3  102
```

- `record_path="items"` → "one output row per item"
- `meta=["id"]` → "copy the parent's `id` along with each row"

This single function solves the most common e-commerce/marketing data problem: **flattening order → line-item data** for dashboards and revenue analysis.

### 3.5 SQL — read straight from a database

```python
import sqlite3

con = sqlite3.connect("company.db")   # works with any DB: sqlite, MySQL, PostgreSQL...
df = pd.read_sql("SELECT Product, Units FROM products WHERE Units > 5", con)
print(df)
```

```
  Product  Units
0  Laptop     10
1 Monitor      8
2   Mouse     60
```

Bonus: you can run the **SQL query inside `read_sql`** — filter in the database, not in memory.

### 3.6 Parquet — the modern workhorse

```python
df = pd.read_parquet("big_data.parquet")   # install once: pip install pyarrow
df.to_parquet("big_data.parquet")
```

Parquet is **column-based, compressed and typed** — typically 5–10× faster and much smaller than CSV for big data. If your company has a data warehouse (BigQuery, Snowflake, Databricks), this is the format it speaks natively.

### 3.7 Other readers you'll meet

```python
pd.read_html("https://example.com/league-table")  # scrape a table from a webpage
pd.read_clipboard()                               # paste straight from Excel!
pd.read_stata("panel.dta")                        # social-science / government data
pd.read_sas("claims.sas7bdat")                    # insurance / legacy data
pd.read_fwf("mainframe.txt")                      # fixed-width (old banking systems)
```

`read_clipboard()` is a lifesaver: select a table in Excel → Ctrl+C → `pd.read_clipboard()` in your notebook.

### 3.8 Huge files — read in CHUNKS

A 10 GB CSV will not fit in your laptop's RAM. `chunksize` makes `read_csv` yield **pieces** you process one by one:

```python
total = 0
for chunk in pd.read_csv("big_orders.csv", chunksize=1000):  # 1000 rows at a time
    total += chunk["amount"].sum()

print(total)    # 88500  (a 3000-row file processed in 3 chunks)
```

The same pattern works for a 5 GB file — RAM stays tiny because each chunk is discarded after processing.

### 3.9 The first 30 seconds after ANY import

Before touching the data, run the "sanity-check four":

```python
df.head()        # do the rows look right?
df.dtypes        # are the types right? (dates as text? numbers as text?)
df.shape         # rows x columns — what you expected?
df.isna().sum()  # how much is missing, per column?
```

If `Date` shows as `str` but you need dates → either re-import with `parse_dates=["Date"]` or convert with `pd.to_datetime(df["Date"])`.

---

## 4. Exporting Data (closing the loop)

Same names, `to_` instead of `read_`:

```python
df.to_csv("cleaned.csv", index=False)      # index=False: skip the 0,1,2... column
df.to_excel("report.xlsx", index=False)
df.to_json("data.json", orient="records")
df.to_parquet("data.parquet")
df.to_sql("table_name", connection, index=False)
df.to_string()                             # pretty text (for logs / emails)
df.to_clipboard()                          # paste straight into Excel
```

> ⚠️ **Beginner trap:** forgetting `index=False` in `to_csv` writes the row numbers into the file — the next person's import gets a useless `Unnamed: 0` column.

---

## 5. Use Cases: A Day in a Company's Life

| Company / team | The real task | What Pandas does |
| --- | --- | --- |
| **Bank / fintech** | Core banking system dumps a transactions CSV every night | `read_csv(chunksize=…)` → filter fraud candidates → `to_excel` for the compliance team |
| **Retail chain** | 50 stores email their Excel sales sheets every Monday | loop over files → `read_excel` each → `pd.concat` into one table → groupby report |
| **E-commerce** | Order API returns nested JSON (orders → items → addresses) | `requests` → `json_normalize` → line-item table ready for the dashboard |
| **Healthcare** | Patient + doctor + visit data live in 3 separate SQL tables | `read_sql` each table → `merge` on patient_id → cohort analysis |
| **Logistics** | 5 GB delivery-trips CSV from the fleet system | `read_csv(chunksize=…)` → per-driver stats without melting the server |
| **HR / Ops (EU offices)** | Payroll export with `;` separators and latin-1 encoding | `read_csv(sep=";", encoding="latin-1")` → headcount & attrition report |
| **Marketing** | Ad platforms export campaign data with different columns per platform | import each → rename/align columns → `concat` → one ROI table |
| **Data engineering** | Nightly ETL feeding the data warehouse | `read_csv` → clean → `to_parquet` — this exact pattern, at scale |

**The common thread:** every single one of these starts with *creating or importing a DataFrame*. Get that step right and 80% of the job is done.

---

## 6. End-to-End Mini Project: Monthly Sales Report

The exact flow of a real analyst task: **import → create → transform → combine → export.** (Full runnable version: `201_Creating_Pandas_DataFrames.py`, Part 3 — it creates the `data/` files for you.)

```python
import numpy as np
import pandas as pd

# 1. IMPORT (CSV, dates parsed on the fly)
sales = pd.read_csv("data/sales_2026.csv", parse_dates=["Date"])

# 2. CREATE (monthly targets, built in plain Python)
targets = pd.DataFrame({
    "Month": [1, 2, 3],
    "Target_Revenue": [12000, 15000, 15000],
})

# 3. TRANSFORM
sales["Revenue"] = sales["Units"] * sales["Unit_Price"]
sales["Month"] = sales["Date"].dt.month
monthly = sales.groupby("Month")["Revenue"].sum().reset_index()

# 4. COMBINE (merge on the common column)
report = monthly.merge(targets, on="Month", how="left")
report["Status"] = np.where(
    report["Revenue"] >= report["Target_Revenue"], "Met", "Below"
)

# 5. REPORT + EXPORT
print(report)
report.to_csv("data/monthly_report.csv", index=False)
report.to_excel("data/monthly_report.xlsx", index=False)
```

**Output:**

```
   Month  Revenue  Target_Revenue Status
0      1    13440           12000    Met
1      2    13300           15000  Below
2      3    15340           15000    Met
```

Two files for the manager — one CSV for the data team, one Excel for the meeting — produced by ~15 lines of code you can re-run next month.

---

## 7. Common Pitfalls for Beginners

1. **`Unnamed: 0` column after import** — someone saved the file with row numbers. Fix: import with `index_col=0` or just drop the column.
2. **`UnicodeDecodeError`** — wrong text encoding; try `encoding="latin-1"` (see 3.2).
3. **Numbers read as text** — values like `"1,234"` or `"$500"` are text to Pandas. Clean them first: `df["x"].str.replace(",", "").str.replace("$", "").astype(float)`, or use `thousands=","` in `read_csv`.
4. **Dates stay as text** — `Date` shows as `str` in `.dtypes`. Re-import with `parse_dates=["Date"]` or convert with `pd.to_datetime(df["Date"])`.
5. **`df.append()` in a loop** — removed in pandas 2.0+. Collect rows in a list, build the DataFrame once (see 2.9).
6. **`read_excel` fails with "No module named 'openpyxl'"** — install it: `pip install openpyxl`.
7. **Excel silently caps at 1,048,576 rows** — for bigger files use CSV or Parquet.
8. **Wrong separator** — a `;`-separated file reads as one giant column. If everything landed in a single column, try `sep=";"`.
9. **`pd.DataFrame({...}, dtype={col: type})`** — a per-column dtype **dict is not supported by the DataFrame constructor** (it's a `read_csv` feature). Use `dtype="float32"` for the whole frame, or `.astype()` per column.

---

## 8. Quick Reference Cheat Sheet

```text
CREATE
  pd.DataFrame(dict)                    # keys = columns
  pd.DataFrame(list_of_dicts)           # each dict = one row
  pd.DataFrame(list, columns=[...])     # one column
  pd.DataFrame(list_of_lists, columns=[...])
  pd.DataFrame(series)                  # from a Series
  pd.DataFrame(numpy_array, columns=[...], index=[...])
  dtype="float32"  /  .astype("category")

IMPORT
  pd.read_csv(f, sep=, usecols=, parse_dates=, dtype=, encoding=, chunksize=)
  pd.read_excel(f, sheet_name=)         # + pip install openpyxl
  pd.read_json(f)  /  pd.json_normalize(data, record_path=, meta=)
  pd.read_sql(query, connection)
  pd.read_parquet(f)                    # + pip install pyarrow
  pd.read_html(url)   pd.read_clipboard()

SANITY CHECK (always, first 30 seconds)
  .head()  .dtypes  .shape  .isna().sum()

EXPORT
  .to_csv(f, index=False)   .to_excel(f, index=False)   .to_json(f)
  .to_parquet(f)            .to_sql(table, con, index=False)   .to_clipboard()
```

---

## 9. One-Line Takeaway

**Data only becomes "analysis" the moment it is inside a DataFrame — so "create it in Python, or import it from wherever it lives" is the gate every real data project walks through, and it is the single most-used skill of the entire course.**






