'''
An outlier is just simply or reaaly just any valur that seems out of place in our data set.
But just because a number is very large or very small does not instantly mean that it shouldn't there.
The removal of outliers is something that needs careful consideration. Removing outliers should only be done if we think there is going to be 
a detrimental effect on the modelling process due to certain data points skewing things so much that the model can no longer generalise rules
for the majority of data points.
'''

import pandas as pd


my_df = pd.DataFrame({"input1" : [15,41,44,47,50,53,56,59,99],
                  "input2" : [29,41,44,47,50,53,56,59,66]
                      })

my_df.plot(kind = "box", vert = False) # Plot should be horizontal

'''
With "input1", we have some values which are quite close to each other. And then we have a couple of values spread out quite away from the rest.
So it will be interesting once we code up our outlier logic to see how it deals with these values.
'''

# Create variable names that we want to apply the outlier to

'''
In practice, this will mean we can pick and choose certain columns to have outliers removed or at least check for removal,
as it may be that we want to leave som columns as they are. Or it could be that some columns aren't just appriopriate for outlier removal.
For example, some columns which have categorical data in them.
'''
outlier_columns = ["input1", "input2"]


'''
# Boxplot appreoach

We'll loop through the outlier_columns, and the first thing we want to do is to calculate the lower and upper quartiles for the column
that we're currently looping through.
my_df[column] = the column we're currently looping through.
0.25 = 25th percentile. or what is commonly known as the lower quartile.
Next, calculate interquartile range: This is the range between the upper and lower quartiles.
Then extend the interquartile range by a factor of 1.5
Then apply the extended interquartile range to our lower and upper quartiles. And to do this, we will create two variables called 
min_border and max_border, and these will serve as boundaries at which data points will become considered outliers.

We can now query the data within the column that we're currently looping through to 
see if any of these data points do indeed fall outside of these boundaries.

Next, if any outlier is found we can then drop them or we say those rows are dropped from the DF.

Note that if we find an outlier in any column, we're removing the entire row of data.
We could equally instead just keep the values to be in line with our outlier borders, for example in a process known as Windsor Rising.

# Standard Deviation Approach

So within our loop, instaed of quartiles, this time we're going to calculate the mean and Standard Deviation 
of the column we are currently looping through. 

'''

# Boxplot appreoach

for column in outlier_columns:
    lower_quartile = my_df[column].quantile(0.25)
    upper_quartile = my_df[column].quantile(0.75)
    iqr = upper_quartile - lower_quartile
    iqr_extended = iqr * 1.5
    #Then apply the extended interquartile range to our lower and upper quartiles.
    min_border = lower_quartile - iqr_extended
    max_border = upper_quartile + iqr_extended
    
    # see if any of these data points do indeed fall outside of these boundaries.
    
    outliers = my_df[(my_df[column] < min_border) | (my_df[column] > max_border)].index # return the index values for any outliers
    print(f"{len(outliers)} outliers detected in column {column}")
    
    # Next, if any outlier is found we can then drop them
    my_df.drop(outliers, inplace=True)
    
    
# Standard Deviation Approach

my_df = pd.DataFrame({"input1" : [15,41,44,47,50,53,56,59,99],
                  "input2" : [29,41,44,47,50,53,56,59,66]
                      })
    

for column in outlier_columns:
    mean = my_df[column].mean()
    std_dev = my_df[column].std()
    min_border = mean - std_dev * 3
    max_border = mean + std_dev * 3
    
    
    # see if any of these data points do indeed fall outside of these boundaries.
    
    outliers = my_df[(my_df[column] < min_border) | (my_df[column] > max_border)].index # return the index values for any outliers
    print(f"{len(outliers)} outliers detected in column {column}")
    
    # Next, if any outlier is found we can then drop them
    my_df.drop(outliers, inplace=True)    