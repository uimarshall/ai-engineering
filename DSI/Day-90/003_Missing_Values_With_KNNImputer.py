"""
The KNNImputer looks to other available numerical data and makes the assumption that other similar looking data points
will give a better estimation of what the missing value is likely to be.

It uses the K nearest neighbours algorithm to plot data over a number of dimensions, data points that are close together
are deemed to be of a similar nature.
And it is then assumed that an unknown data point in space could have its value estimated based on what other values exist near it.

The K in the K nearest neighbours represents the number of neighbours that we want to assess in order to guess what the value for our
missing data point might be.

"""

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer

my_df = pd.DataFrame(
    {"A": [1, 2, 3, 4, 5], "B": [1, 1, 3, 3, 4], "C": [1, 2, 9, np.nan, 20]}
)


"""
Aim: Ask KNNImputer to estimate a value for the missing value in col "C", For a SimpleImputer, it will be the mean of that col "C".
The KNNImputer will not rely solely on Col "C", it will take into account the values from other numeric cols, in this case, cols A&B.
It will plot these values as positions in space based on their values, so the row of index zero would be at coordinate (1,1), 
and it will do the same for every row.

For the row index3 which contains the missing value, it will look to find which of these plotted data points (coordinates) are closest to this one,
and depending on what value we set for "K", it will assess the closest K neighbours and average their col "C" values in order to 
estimate what the missing value should be.

"""

# Instantiate the imputer object

knn_imputer = KNNImputer()
knn_imputer = KNNImputer(
    n_neighbors=1
)  # With n_neighbors=1, the knn_imputer.fit_transform(my_df) gives a vlaue of 9
knn_imputer = KNNImputer(
    n_neighbors=2
)  # With n_neighbors=1, the knn_imputer.fit_transform(my_df) gives a vlaue of 14.4(ave. of 9&20)
knn_imputer = KNNImputer(n_neighbors=2)
knn_imputer.fit_transform(
    my_df
)  # Default behaviour, give a value of 8 for the missing number

"""

knn_imputer.fit_transform(my_df)
Out[10]: 
array([[ 1. ,  1. ,  1. ],
       [ 2. ,  1. ,  2. ],
       [ 3. ,  3. ,  9. ],
       [ 4. ,  3. , 14.5],
       [ 5. ,  4. , 20. ]])
In theory, using this approach should provide much more realistic imputation values than what the SimpleImputer provided or applied,
as now it's focusing on what it believes are similar rows to the one in question, rather than just generically using all rows.
"""
# The weight parameter in KNNImputer(weigths = "uniform")

"""
weigths = "uniform" has a default value of "uniform", which means that each of the closest neighbours will be given the same(uniform) weight
when calcaulating the imputed value. If we were to change this weight so it equal to distance instead (weights = "distance"),
we should see it give more weight to closer neighbours than those that are further away.
"""
knn_imputer = KNNImputer(
    n_neighbors=2, weights="distance"
)  # outputed missing value = 13.55634919
knn_imputer.fit_transform(my_df)

"""
Out[11]: 
array([[ 1.        ,  1.        ,  1.        ],
       [ 2.        ,  1.        ,  2.        ],
       [ 3.        ,  3.        ,  9.        ],
       [ 4.        ,  3.        , 13.55634919],
       [ 5.        ,  4.        , 20.        ]])
Why it gives a value of 13.55634919 is because the corrdinate (3,3) is closer in N Dimensional space to coordinates (4,3) than the
coordinates (5,4) which is below (4,3), this means the value 9 in the (3,3) dimensional space gets a higher weighting than 20 in (5,4)
when we calculate the imputation value. They're both considered to be neighbours, but one is given more weight than the other.
So the imputed value (13.55634919) here is closer to 9 than 20.
"""

# An array is always returned when we apply the KNNImputer, If we want a DF returned, do the following:
my_df1 = pd.DataFrame(knn_imputer.fit_transform(my_df), columns=my_df.columns)
