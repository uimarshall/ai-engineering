# -*- coding: utf-8 -*-

################################################

# Pandas - Adding & Dropping Cols

import pandas as pd

import numpy as np

# Manipulating our data

transactions = pd.read_excel("grocery_database.xlsx", sheet_name="transactions")

# Adding new cols

transactions["store_id"] = 1

# Add profit margin col, which is 20% of sales_cost

transactions["profit"] = transactions["sales_cost"] * 0.2

# If else - If sales_cost is greater than 20, apply a value of "Large" else "Small" to the new col called "sales_type"

transactions["sales_type"] = np.where(transactions["sales_cost"] > 20, "Large", "Small")

# Set of conditions

condition_rules = [transactions["sales_cost"] > 50, transactions["sales_cost"] > 20, transactions["sales_cost"] > 10]
outcomes = ["X-Large", "Large", "Medium"]

# Default value will "Small", that is anything not covered in our conditions, e.g. sales_cost < 10

transactions["sales_type"] = np.select(condition_rules, outcomes, default="Small")

# Dropping Cols

# axis =1 means you want to drop a col, and axis = 0, means you want to drop a row.

new_df_drop_col = transactions.drop(["sales_cost"], axis = 1)









