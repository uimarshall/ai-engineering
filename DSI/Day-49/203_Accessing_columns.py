# -*- coding: utf-8 -*-

######################################

# Pandas - Accessing Cols

#####################################

import pandas as pd

transactions = pd.read_excel("grocery_database.xlsx", sheet_name="transactions")

# A quick glance at the number of cols and col names.

transactions.info()

"""
SQL equivalent - select customer_id, sales_cost from transactions
"""

new_df = transactions.customer_id # This will select a single col - customer_id (1d Series)

new_df = transactions["customer_id"] # second method

new_df = transactions[["customer_id"]] # This is now a 2d DF.

new_df_2cols = transactions[["customer_id", "sales_cost"]] 





