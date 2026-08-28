# -*- coding: utf-8 -*-

#####################################################

# Pandas - Plotting our Data using Pandas

#####################################################

import pandas as pd

# We intend to plot our data directly from the pandas DF
# Under the hood, pandas is using Matplotlib to make or create the plot

# The plot in pandas is majorly used to investigate the data, we might discover outliers or anomalies in the process.

transactions = pd.read_excel("grocery_database.xlsx", sheet_name="transactions")

customer_details = pd.read_excel("grocery_database.xlsx", sheet_name="customer_details")

product_areas = pd.read_excel("grocery_database.xlsx", sheet_name="product_areas")

customer_details.plot()

# Line plot is used for sequential data.

# Aggregate the data to make it plotable

daily_sales_summary = transactions.groupby("transaction_date")[["sales_cost","num_items"]].sum().reset_index()

# This will plot the sales_cost ( y-axis) against the index (x-axis)

daily_sales_summary["sales_cost"].plot()

# Plot transaction_date against sales_cost

daily_sales_summary.plot(x = "transaction_date", y = "sales_cost")

# The default type of graph is line graph

daily_sales_summary.plot(x = "transaction_date", y = "sales_cost", kind = "line")

daily_sales_summary.plot(x = "num_items", y = "sales_cost", kind = "scatter")

# In box plot, we only plot one variable

# The horizontal green line in the middle, shows the median (Also known as the 50th percentile) sales_cost
daily_sales_summary.plot(y = "sales_cost", kind = "box")
daily_sales_summary.plot(y = "sales_cost", kind = "hist")
daily_sales_summary.plot(y = "sales_cost", kind = "hist", bins = 25)

# We want to see each product margin bar for a given product_area_name

product_areas.plot(kind = "bar", y = "profit_margin", x = "product_area_name")


