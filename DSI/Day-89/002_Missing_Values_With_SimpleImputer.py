# The "scikit-learn" library contains all sorts of machine learning algorithms but it also contains a whole lot of useful data
# data processing and preparation techniques.

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer


my_df = pd.DataFrame({"A" : [1,4,7,10,13],
                      "B" : [3,6,9,np.nan,15],
                      "C" : [2,5,np.nan,11,np.nan]})

# To get started with SimpleImputer, we first need to instantiate our imputer object using the SimpleImputer class that we imported above.

imputer = SimpleImputer()

'''
We now need to do 2 things

First we need to calculate the values we want to impute, So in this case, that would be the mean value of each column. And then we need it to apply
that logic onto our data. In scikit-learn lingo, these steps are known as "fit" and "transform".
'''

# Using fit

# Within the parenthesis of fit, we pass in the data that we want it to learn from, In this case i.e the Dataframe (my_df).
# Once it is run, the object will store this information, and we can apply it to our DataFrame, or even to new data in the future.

imputer.fit(my_df)

# Next, we want to apply our logic to our data - transform

imputer.transform(my_df)

my_df1 = imputer.transform(my_df)

# Using fit & transform simultaneously

imputer.fit_transform(my_df)

'''
Note: Only use fit_transform on training data. If you're going to apply the same logic to test data or to new data, use fir & transform separately.
The reason for this is that we want imputation rules to be based off our training data.
If we fit our imputation rules off the training data and test data separately, then they would end up getting slightly different imputation rules.
And whilenot a huge issue in some cases, it can mean that the training and test results are not completely comparable. 

And thus our assumptions about how well the model will perform on new data in the real world can be somewhat flawed.
'''
# Convert the my_df1 array back to DataFrame
my_df2 = pd.DataFrame(imputer.fit_transform(my_df), columns=my_df.columns)

# Apply the imputer object to a specified col

imputer.fit_transform(my_df[["B"]])

# override the values of B
my_df["B"] = imputer.fit_transform(my_df[["B"]])
