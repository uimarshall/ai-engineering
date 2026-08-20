# -*- coding: utf-8 -*-

#####################################################

# Pandas - Adding & Dropping Columns

#####################################################

import pandas as pd

customer_details = pd.read_excel("grocery_database.xlsx", sheet_name="customer_details")
product_areas = pd.read_excel("grocery_database.xlsx", sheet_name="product_areas")


# MAP

# Maps used to transform values in a column or technically a Pandas Series  into another value.

# Map the "M" and "F" values in "gender" column of the customer_details sheet into "0s" & "1s" and store it a new col called "gender_numeric"

customer_details["gender_numeric"] = customer_details["gender"].map({"M" : 0, "F" : 1})

# If mapping in not provided for all the values in the col or Series selected, it will return "nan" for unspecified field.

# NB: Map is only applicable to the Series Data structure. It will throw error for DF.

customer_details["gender_numeric"] = customer_details["gender"].map({"M" : 0})


# REPLACE

# Replace is somewhat similar to "Map", but "Repalce" will preserve original values if the values you want to replace with is not specified.

customer_details["gender_numeric"] = customer_details["gender"].replace({"M" : 0, "F" : 1})

# Unlike "Map", "Replace" will not return a "nan", hence the name "Replace"

customer_details["gender_numeric"] = customer_details["gender"].replace({"M" : 0})




# APPLY

# Apply Means we can call a function and apply it to every value in our Series or DF.

# Apply the len function to the "product_area_name" Series or Column.

product_areas["product_area_name"].apply(len) # Returns the length of the str within the "product_area_name" rows.

# Custom func with apply

def update_profit_margin(profit_margins):
    if profit_margins > 0.2:
        return profit_margins * 1.2
    else:
        return profit_margins * 0.8
    
product_areas["profit_margin_updated"] = product_areas["profit_margin"].apply(update_profit_margin) 

x = pd.DataFrame({"A" : [1,2], "B" : [3,4], "C" : [5,6]}) 

x.apply(max) # returns max of cols by default because axis = 0 is the default

x.apply(max, axis=1) # returns max of rows
    

# APPLYMAP

# It applies a function to every element in the DF

def square(n):
    return n ** 2

x.apply(square)

