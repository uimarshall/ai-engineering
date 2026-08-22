# -*- coding: utf-8 -*-

#####################################################

# Pandas - LOC & ILOC

#####################################################

import numpy as np
import pandas as pd

transactions = pd.read_excel("grocery_database.xlsx", sheet_name="transactions")

# transactions.loc[row_labels, column_labels]

# transactions.iloc[row_indexes, column_indexes]

"""

So often we will have DataFrames that have a lot of rows and columns. 
And for some specific task, we will only want to consider certain rows or columns as these are the ones that are relevant to us.

To do this, we need to learn about two key pandas functions (LOC & ILOC).

LOC is a method for specifying conditions on rows and columns, primarily using labels or names.

ILOC is a method for specifying conditions on rows and columns, primarily using indexes or index positions.

The "I" in the front of ILOC means "Index".

"""


# ILOC

# Return the rows of the first index - 0
transactions.iloc[0]
transactions.iloc[0:4]

transactions.iloc[[0, 30, 51]]  # return the rows specified.

transactions.iloc[0:4, [0, 3, -1]]  # rows & cols
transactions.iloc[:, [0, 3, -1]]  # rows & cols

# LOC
transactions.loc[0]

# Set another index as labels

transactions.set_index("customer_id", inplace=True)
transactions.loc[642]

transactions.reset_index(inplace=True)

# show col names
list(transactions)

transactions.loc[0:10, "customer_id"]

# row 0-10 with 3 cols specified in square brackets

transactions.loc[0:10, ["customer_id", "product_area_id", "sales_cost"]]

# Reorder the cols

transactions.loc[0:10, ["sales_cost", "customer_id", "product_area_id"]]


# CONDITIONAL LOGIC

transactions["customer_id"] == 642

# Filter rows based on some condition or criteria

# Filter out rows where "customer_id" = 642
transactions.loc[transactions["customer_id"] == 642]

# We can also specify the cols we want returned.

transactions.loc[
    transactions["customer_id"] == 642, ["customer_id", "sales_cost", "product_area_id"]
]

transactions.loc[(transactions["customer_id"] == 642) & (transactions["num_items"] > 5)]
transactions.loc[(transactions["customer_id"] == 642) | (transactions["num_items"] > 5)]

transactions.loc[transactions["customer_id"].isin([642, 700])]
transactions.loc[
    ~transactions["customer_id"].isin([642, 700])
]  # return where condition is False by using tilde
