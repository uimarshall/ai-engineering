import numpy as np
import pandas as pd

my_df = pd.DataFrame(
    {"A": [1, 2, 4, np.nan, 5, np.nan, 7], "B": [4, np.nan, 7, np.nan, 1, np.nan, 2]}
)

# The very first thing we always want to understand in "Dealing with missing values" is how big of a problem is it within our data.

# If there's a problem at all, the easiest way to check for missing values is to use the "isna" method Pandas library to find the missing value.

my_df.isna()  # will generate True & False (True mean data is missing)

# Count or get the number of missing values in each col

my_df.isna().sum()  # col A has 2 missing values

# Several ways to deal with the missing values

# 1. Dropping the Missing values with Pandas

my_df.dropna()  # Since no parameter was specified within the parenthesis, it will drop any row where a missing value was present in one of the cols.

# Drop the row if every value in that row is a missing value

my_df.dropna(how="any")  # Default behaviour is "any"

my_df.dropna(
    how="all"
)  # Actually Drop the row if every value in that row is a missing value

# Using "subset" -  The dropping logic will only look at the col listed in the subset parameter, and if any those values are missing, it will drop the row

my_df.dropna(how="all", subset=["A"])

# Commit the changes to the DataFrame such that df actually changes and indicate that those values have been dropped.

my_df.dropna(how="any", inplace=True)


# 2. Fill in the missing values with a value of choice with Pandas

# Recommendation is to drop rows rather filling them if you can.
# But in a situation where we don't have enough data to work with, filling values can be very useful.

my_df = pd.DataFrame(
    {"A": [1, 2, 4, np.nan, 5, np.nan, 7], "B": [4, np.nan, 7, np.nan, 1, np.nan, 2]}
)

# Any data missing will be filled with a value of 100

my_df.fillna(value=100)
# You must critique any value you're using to fill in for missing data so as not to adversely impact the result,
# e.g. Using a value of zero to fill in for a missing value if you're looking at distance between two points may not be ideal.
# In the case of string or text, replacing the missing values with "unknown" is quite good idea atimes as it allows us to avoid throwing away data

# A more common solution to filling numeric values is to use the mean or median value of the col as it's likely to be more representative
# of what the value should be.

mean_value = my_df["A"].mean()
my_df["A"].fillna(value=mean_value)

# Fill all cols

my_df.fillna(value=my_df.mean(), inplace=True)
