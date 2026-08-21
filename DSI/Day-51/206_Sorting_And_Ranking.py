# -*- coding: utf-8 -*-

#####################################################

# Pandas - Sorting & Ranking

#####################################################

import pandas as pd

import numpy as np

customer_details = pd.read_excel("grocery_database.xlsx", sheet_name="customer_details")
product_areas = pd.read_excel("grocery_database.xlsx", sheet_name="product_areas")

# SORTING

# By default, it sorts from smallest to highest - Ascending (Going from low to high measures) - Single col

customer_details.sort_values(by = "distance_from_store", inplace = True)

# Descending - Coming down from high to low

customer_details.sort_values(by = "distance_from_store", inplace = True, ascending = False)

# Multiple cols sorting

customer_details.sort_values(by = ["distance_from_store", "credit_score"], inplace = True)

# Missing values - Listed at the top

customer_details.sort_values(by = "distance_from_store", inplace = True, na_position = "first")


# RANKING

x = pd.DataFrame({"column1" : [1,1,1,2,3,4,5,np.nan,6,8]})

x["column1"].rank()

# Create cols

x["column1_rank"] = x["column1"].rank()

x["average_rank"] = x["column1"].rank(method = "average")
x["min_rank"] = x["column1"].rank(method = "min")
x["max_rank"] = x["column1"].rank(method = "max")
x["first_rank"] = x["column1"].rank(method = "first")
x["dense_rank"] = x["column1"].rank(method = "dense")

x["dense_rank_na_top"] = x["column1"].rank(method = "dense", na_option = "top")

x["dense_rank_na_bottom"] = x["column1"].rank(method = "dense", na_option = "bottom")
