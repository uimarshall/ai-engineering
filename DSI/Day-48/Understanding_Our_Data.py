# -*- coding: utf-8 -*-

###########################################


# Pandas - Exploring & Understanding our Data

##########################################


import pandas as pd

# We intend to read the transactions sheet from our grocery_database which is stored as excel.

transactions = pd.read_excel("grocery_database.xlsx", sheet_name="transactions")

# Show how many rows and cols we have - We use the "shape" attribute to do this.


transactions.shape  # Out[2]: (38506, 6) - 38506 rows & 6 cols

# Get top 5 rows by default

transactions.head()

# Specify the first top 20m rows

transactions.head(20)

# Last 5 rows

transactions.tail()

# Last 10 rows

transactions.tail(10)

# Random sample data

transactions.sample()

transactions.sample(10)

# 10% sample of row

sample = transactions.sample(frac=0.1)  # 10% of 38506 is 3851

# Summary or overview of how the data is spread btw the higher value and the lower value.

transactions.describe()

# Give 5 rows where sales_cost was the highest

transactions.nlargest(5, "sales_cost")
transactions.nlargest(25, "sales_cost")

# smallest values of sales cost

transactions.nsmallest(25, "sales_cost")

# How many unique value in any particular col.

transactions.nunique()

customer_details = pd.read_excel("grocery_database.xlsx", sheet_name="customer_details")

# check for nullity

customer_details.isna()
customer_details.isna().sum()
