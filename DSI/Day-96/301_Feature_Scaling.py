'''
In Feature Scaling, we force the values from different columns within our data to exist on the same scale in order to enhance the learning
capabilities of a model.
'''

import pandas as pd

# Standardisation

from sklearn.preprocessing import StandardScaler

my_df = pd.DataFrame({"Height" : [1.98,1.77,1.76,1.80,1.64],
                      "Weight" : [99,81,70,86,82]})

# Instantiate the Standardization object

scale_standard = StandardScaler()

# Apply the "fit method" where our Standardization object will learn the rules for scaling
# And then we can apply the transform method to apply the scaling to our data.Or we can apply both at once using fit_transform.

scale_standard.fit_transform(my_df)

# convert back to Dataframe

my_df_standardised = pd.DataFrame(scale_standard.fit_transform(my_df), columns=my_df.columns)

# Normalisation

from sklearn.preprocessing import MinMaxScaler

scale_norm = MinMaxScaler()
scale_norm.fit_transform(my_df)
my_df_normalised = pd.DataFrame(scale_norm.fit_transform(my_df), columns=my_df.columns)
