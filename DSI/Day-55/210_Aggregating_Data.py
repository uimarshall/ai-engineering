# -*- coding: utf-8 -*-

#####################################################

# Pandas - Aggregating Data using GROUPBY

#####################################################

import numpy as np
import pandas as pd

"""
select
    product_area_id,
    count(*) as row_count
    sum(sales) as total_sales
    
from
    transactions

group by
      product_area_id  
    
"""

transactions = pd.read_excel("grocery_database.xlsx", sheet_name="transactions")
product_areas = pd.read_excel("grocery_database.xlsx", sheet_name="product_areas")

transactions["sales_cost"].sum()

# check which product area is driving most sales.

transactions.info()
product_areas.info()

# override transactions table

transactions = pd.merge(transactions, product_areas, how="inner", on="product_area_id")

# How many rows each product area name contains

transactions["product_area_name"].value_counts()

# Group By - Note what we're returned in GroupBy is a "Series" rather than a "DF".
# You can quickly confirm it in the "Variable Explorer" in Spyder
# Sum up sales cost by product_area_name.
transactions.groupby("product_area_name")["sales_cost"].sum()


transactions.groupby("product_area_name")["sales_cost"].quantile(
    np.array([0.25, 0.5, 0.75])
)

sales_summary = transactions.groupby("product_area_name")["sales_cost"].sum()

# To get DF as an output, use the index functionality to reset it.
sales_summary = (
    transactions.groupby("product_area_name")["sales_cost"].sum().reset_index()
)

# Group by multiple cols
sales_summary = (
    transactions.groupby(["product_area_name", "transaction_date"])["sales_cost"]
    .sum()
    .reset_index()
)

# grouping by product_area_name & transaction_date and have aggregations(sum - find aggregate)
# for both sales cost & num of items purchased.

sales_summary = (
    transactions.groupby(["product_area_name", "transaction_date"])[
        ["sales_cost", "num_items"]
    ]
    .sum()
    .reset_index()
)

# The "agg" function is incredible - we can pass multiple aggregation functions

sales_summary = (
    transactions.groupby("product_area_name")["sales_cost"].agg("sum").reset_index()
)
sales_summary_multiple_aggregation = (
    transactions.groupby("product_area_name")["sales_cost"]
    .agg(["sum", "mean"])
    .reset_index()
)

# Group by multiple cols and multiple aggregation types
sales_summary = (
    transactions.groupby(["product_area_name", "transaction_date"])[
        ["sales_cost", "num_items"]
    ]
    .agg(["sum", "mean"])
    .reset_index()
)

# Using Dict

sales_summary_dict = (
    transactions.groupby("product_area_name")
    .agg({"sales_cost": "sum", "num_items": "mean"})
    .reset_index()
)

sales_summary_dict = (
    transactions.groupby("product_area_name")
    .agg({"sales_cost": ["sum", "mean", "max", "std"], "num_items": "mean"})
    .reset_index()
)
