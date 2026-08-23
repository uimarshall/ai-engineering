# -*- coding: utf-8 -*-
#####################################################

# Pandas - Renaming Columns

#####################################################

import pandas as pd

transactions = pd.read_excel("grocery_database.xlsx", sheet_name="transactions")


list(transactions)

# inplace = True is used to ensure that the changes actually takes place in the "transactions" DF.

transactions.rename(columns = {"customer_id" : "friend_id"}, inplace = True)
list(transactions)

column_names = ['friend_id',
 'transaction_date',
 'purchase_id',
 'product_region_id',
 'num_items',
 'sales_cost']

# Another mtd of renaming cols
transactions.columns = column_names
list(transactions)

# Removing spaces

column_names = ['friend id',
 'transaction date',
 'purchase id',
 'product region id',
 'num items',
 'sales cost']

transactions.columns = column_names
list(transactions)

transactions.columns = transactions.columns.str.replace(" ", "_")
list(transactions)
