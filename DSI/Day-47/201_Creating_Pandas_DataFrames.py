"""
Day 47 — Creating Pandas DataFrames And Importing Data (Python)
Companion practice file for CREATING_PANDAS_DATAfRAMES.md

Run from ANY folder:
    python 201_Creating_Pandas_DataFrames.py

Sample files (CSV / Excel / JSON) are created in a ./data folder next to this script.
"""
import json
import os
import sqlite3

import numpy as np
import pandas as pd

# Keep all sample files next to this script, no matter where you run from
BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
os.makedirs(DATA, exist_ok=True)


# =====================================================================
# PART 1 — CREATING DATAFRAMES (data that already lives in Python)
# =====================================================================
print("=" * 70)
print("PART 1 — CREATING DATAFRAMES")
print("=" * 70)

# ---------------------------------------------------------------
# 1. From a DICT  ->  each key = one COLUMN (the most common way)
# ---------------------------------------------------------------
df_dict = pd.DataFrame(
    {
        "Product": ["Laptop", "Monitor", "Mouse", "Laptop"],
        "Region": ["North", "South", "North", "East"],
        "Units": [10, 8, 60, 5],
        "Price": [1200, 220, 24, 1250],
    }
)
print("\n1) From a dictionary (keys become columns):")
print(df_dict)

# ---------------------------------------------------------------
# 2. From a LIST OF DICTS  ->  each dict = one ROW
#    (this is how data looks when it comes from an API / JSON)
# ---------------------------------------------------------------
rows = [
    {"name": "Asha", "dept": "Sales", "sales": 42000},
    {"name": "Ravi", "dept": "Sales", "sales": 51000},
    {"name": "Meera", "dept": "IT", "sales": 0},
]
df_rows = pd.DataFrame(rows)
print("\n2) From a list of dictionaries (each dict becomes a row):")
print(df_rows)

# ---------------------------------------------------------------
# 3. From a SINGLE LIST  ->  one column (name it yourself)
# ---------------------------------------------------------------
df_single = pd.DataFrame([100, 200, 300], columns=["Score"])
print("\n3) From a single list (one column):")
print(df_single)

# ---------------------------------------------------------------
# 4. From a LIST OF LISTS  ->  rows + your own column names
# ---------------------------------------------------------------
df_lists = pd.DataFrame(
    [["North", 120], ["South", 90], ["East", 150]],
    columns=["Region", "Orders"],
)
print("\n4) From a list of lists:")
print(df_lists)

# ---------------------------------------------------------------
# 5. From a SERIES  ->  one column, the Series name = column name
# ---------------------------------------------------------------
s = pd.Series({"A": 1, "B": 2, "C": 3}, name="Value")
df_series = pd.DataFrame(s)
print("\n5) From a Series:")
print(df_series)

# ---------------------------------------------------------------
# 6. From a NUMPY ARRAY  ->  fast, for numeric blocks of data
# ---------------------------------------------------------------
arr = np.array([[1, 2, 3], [4, 5, 6]])
df_np = pd.DataFrame(arr, columns=["x", "y", "z"])
print("\n6) From a NumPy array:")
print(df_np)

# ---------------------------------------------------------------
# 7. CUSTOM INDEX  ->  real-world row labels (SKUs, Employee IDs)
# ---------------------------------------------------------------
df_idx = pd.DataFrame(
    {"Product": ["Laptop", "Mouse"], "Units": [10, 60]},
    index=["SKU-001", "SKU-014"],
)
print("\n7) With a custom index:")
print(df_idx)

# ---------------------------------------------------------------
# 8. CONTROL DATA TYPES (dtype) AT CREATION
# ---------------------------------------------------------------
df_types = pd.DataFrame({"ID": [1, 2, 3], "Code": ["A", "B", "C"]})
print("\n8a) Default dtypes (Pandas guesses for you):")
print(df_types.dtypes)

# Whole-frame dtype with the dtype argument:
df_floats = pd.DataFrame([[1, 2], [3, 4]], dtype="float32")
print("\n8b) One dtype for the whole frame (dtype='float32'):")
print(df_floats.dtypes)

# Per-column: build first, then .astype() each column
df_types2 = pd.DataFrame({"ID": [1, 2, 3], "Code": ["A", "B", "C"]})
df_types2["ID"] = df_types2["ID"].astype("int8")
df_types2["Code"] = df_types2["Code"].astype("category")
print("\n8c) Per-column dtypes with .astype():")
print(df_types2.dtypes)

# ---------------------------------------------------------------
# 9. BUILDING A DATAFRAME INCREMENTALLY (the SAFE way)
#    df.append() is REMOVED in pandas 2.0+ -> collect in a list,
#    then create the DataFrame ONCE at the end (much faster).
# ---------------------------------------------------------------
records = []
for order_id, amount in [(101, 250.50), (102, 80.00), (103, 410.25)]:
    records.append({"order_id": order_id, "amount": amount})
df_grow = pd.DataFrame(records)  # build once, at the end
print("\n9) Collected rows -> one DataFrame at the end:")
print(df_grow)
# =====================================================================
# PART 2 — IMPORTING DATA (loading files and sources)
# =====================================================================
print("\n" + "=" * 70)
print("PART 2 — IMPORTING DATA")
print("=" * 70)

# ---------------------------------------------------------------
# 2.1 CSV — the #1 business format. First: create a sample file.
# ---------------------------------------------------------------
sales_csv = os.path.join(DATA, "sales_2026.csv")
sales_rows = [
    ["Date", "Product", "Region", "Units", "Unit_Price"],
    ["2026-01-05", "Laptop", "North", 10, 1200],
    ["2026-01-12", "Mouse", "South", 60, 24],
    ["2026-02-03", "Laptop", "East", 8, 1250],
    ["2026-02-19", "Monitor", "North", 15, 220],
    ["2026-03-08", "Mouse", "East", 40, 25],
    ["2026-03-21", "Laptop", "South", 12, 1195],
]
with open(sales_csv, "w") as f:
    f.write("\n".join(",".join(str(v) for v in row) for row in sales_rows))

print("\n2.1) pd.read_csv — the workhorse:")
df_csv = pd.read_csv(sales_csv)
print(df_csv)
print("\nColumn types (Pandas guessed them):")
print(df_csv.dtypes)

# ---------------------------------------------------------------
# 2.2 Useful read_csv options
# ---------------------------------------------------------------
print("\n2.2a) usecols -> read only the columns you need (faster):")
print(pd.read_csv(sales_csv, usecols=["Product", "Region"]))

print("\n2.2b) parse_dates -> real dates, not text, at import time:")
df_dates = pd.read_csv(sales_csv, parse_dates=["Date"])
print(df_dates.dtypes)

# A delimited file where the separator is ';' (very common in Europe)
semi_csv = os.path.join(DATA, "europe_sales.csv")
with open(semi_csv, "w", encoding="utf-8") as f:
    f.write("City;Units\nMunich;45\nBerlin;80\nParis;62\n")
print("\n2.2c) sep=';' -> read a semicolon file:")
print(pd.read_csv(semi_csv, sep=";"))

# ---------------------------------------------------------------
# 2.3 Encoding problems (the classic beginner error)
# ---------------------------------------------------------------
notes_csv = os.path.join(DATA, "notes_latin1.csv")
with open(notes_csv, "w", encoding="latin-1") as f:  # old Windows/Excel encoding
    f.write("item,note\nCafé,good\nMüsli,ok\n")

print("\n2.3) Encoding — reading a latin-1 file with the default (utf-8):")
try:
    pd.read_csv(notes_csv)  # default encoding is utf-8 -> will fail here
except UnicodeDecodeError as e:
    print("Expected error ->", str(e).split("\n")[0])

print("\nFix -> tell Pandas the real encoding:")
print(pd.read_csv(notes_csv, encoding="latin-1"))

# ---------------------------------------------------------------
# 2.4 EXCEL — needs the openpyxl engine (pip install openpyxl)
# ---------------------------------------------------------------
xlsx_path = os.path.join(DATA, "sales_2026.xlsx")
region_orders = pd.DataFrame(
    {"Region": ["North", "South", "East"], "Orders": [25, 18, 33]}
)
with pd.ExcelWriter(xlsx_path) as writer:  # write TWO sheets
    df_csv.to_excel(writer, sheet_name="Sales", index=False)
    region_orders.to_excel(writer, sheet_name="Regions", index=False)

print("\n2.4a) pd.read_excel — default (first) sheet:")
print(pd.read_excel(xlsx_path, nrows=3))

print("\n2.4b) sheet_name='Regions' -> pick another sheet:")
print(pd.read_excel(xlsx_path, sheet_name="Regions"))
# ---------------------------------------------------------------
# 2.5 JSON — how APIs and app data arrive
# ---------------------------------------------------------------
orders_json = [
    {"id": 101, "items": [{"sku": "LAP-01", "qty": 2}, {"sku": "MSE-01", "qty": 1}]},
    {"id": 102, "items": [{"sku": "MON-02", "qty": 3}]},
]
json_path = os.path.join(DATA, "orders.json")
with open(json_path, "w") as f:
    json.dump(orders_json, f)

print("\n2.5a) pd.read_json — one row per order (nested 'items' stays a blob):")
print(pd.read_json(json_path))

print("\n2.5b) pd.json_normalize — flatten the nested 'items' (the pro move):")
print(pd.json_normalize(orders_json, record_path="items", meta=["id"]))

# ---------------------------------------------------------------
# 2.6 SQL — read straight from a database (here: in-memory SQLite)
# ---------------------------------------------------------------
con = sqlite3.connect(":memory:")
df_dict.to_sql("products", con, index=False)  # load our table into the DB
print("\n2.6) pd.read_sql — query the database directly:")
print(pd.read_sql("SELECT Product, Units FROM products WHERE Units > 5", con))

# ---------------------------------------------------------------
# 2.7 HUGE FILES — read in CHUNKS so memory never explodes
# ---------------------------------------------------------------
big_csv = os.path.join(DATA, "big_orders.csv")
big = pd.DataFrame(
    {"order_id": range(1, 3001), "amount": [(i % 50) + 5 for i in range(3000)]}
)
big.to_csv(big_csv, index=False)

total = 0
for chunk in pd.read_csv(big_csv, chunksize=1000):  # 1000 rows at a time
    total += chunk["amount"].sum()
print("\n2.7) Chunked read of 3000 rows (3 chunks) -> total amount:")
print(total)


# =====================================================================
# PART 3 — MINI PROJECT: MONTHLY SALES REPORT
# import -> create -> transform -> combine -> export
# =====================================================================
print("\n" + "=" * 70)
print("PART 3 — MINI PROJECT: MONTHLY SALES REPORT")
print("=" * 70)

# 1. IMPORT (CSV, dates parsed on the fly)
sales = pd.read_csv(sales_csv, parse_dates=["Date"])

# 2. CREATE (monthly targets, built in plain Python)
targets = pd.DataFrame(
    {
        "Month": [1, 2, 3],
        "Target_Revenue": [12000, 15000, 15000],
    }
)

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
print("\nMonthly report:")
print(report)

report_csv = os.path.join(DATA, "monthly_report.csv")
report.to_csv(report_csv, index=False)
report.to_excel(os.path.join(DATA, "monthly_report.xlsx"), index=False)
print(f"\nSaved: {report_csv}")
print(f"Saved: {os.path.join(DATA, 'monthly_report.xlsx')}")
print("\nDone — all sample files are in the ./data folder for you to explore.")



