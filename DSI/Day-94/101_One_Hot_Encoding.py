import pandas as pd
from sklearn.preprocessing import OneHotEncoder

X = pd.DataFrame({"input1" : [1,2,3,4,5],
                      "input2" : ["A","A","B","B","C"],
                      "input3" : ["X","X","X","Y","Y"]})

# The col we want to apply the encoding to, is put into a list because they're cat variables

# This means we can use this code as template and put in whichever variables it is that you need to run encoding on.
# And then the rest of code will run through as necessay.

categorical_vars = ["input2", "input3"]

# Instantiate OneHotEncoder object

'''
sparse_output=False, means This will return an array and not an object which is called a sparse matrix.

And an array is a bit easier to use and visualise
'''

one_hot_encoder = OneHotEncoder(sparse_output=False, drop = "first") 

'''
Let's get our object to both learn what it needs to do and apply the logic by using the fit_transform method.

We only want the OneHotEncoder to apply to the categorical_vars.
The result we get in running the code: encoder_vars_array, is an array with 5 columns, Each of these columns are the binary representation
for the unique categories that were found across both "input2" and "input3":

input2 - has 3 unique values (A,B, C)    
input3 - has 2 unique values (X,Y)

encoder_vars_array
Out[5]: 
array([[1., 0., 0., 1., 0.],
       [1., 0., 0., 1., 0.],
       [0., 1., 0., 1., 0.],
       [0., 1., 0., 0., 1.],
       [0., 0., 1., 0., 1.]])

Additionally, we'll like to know what each of these 5 columns represents in terms of which input variable it is and which category from
those input variables they are. To do this, we just need to access the get_feature_names_out method from the one_hot_encoder object.

It gives an output showing the input variable name with an underscore followed by the category itself:
    
encoder_feature_names
Out[4]: 
array(['input2_A', 'input2_B', 'input2_C', 'input3_X', 'input3_Y'],
      dtype=object)

encoder_feature_names
Out[2]: array(['input2_B', 'input2_C', 'input3_Y'], dtype=object) 

The next thing is to put this encoded data back with the other input variables that didn't need encoding. In our case, this was just the column
called "input1". 

we will store the output in "encoder_vars_df" and the columns names will be the encoder_feature_names
# as indicated in the parameter passed to the DF: columns=encoder_feature_names.

encoder_vars_df
Out[8]: 
   input2_A  input2_B  input2_C  input3_X  input3_Y
0       1.0       0.0       0.0       1.0       0.0
1       1.0       0.0       0.0       1.0       0.0
2       0.0       1.0       0.0       1.0       0.0
3       0.0       1.0       0.0       0.0       1.0
4       0.0       0.0       1.0       0.0       1.0  
    
Now we can concatenate this new data frame back onto our original input variables data Data frame to ensure we have everything together
in one place ready for modelling: X_new = pd.concat([X.reset_index(drop=True), encoder_vars_df.reset_index(drop=True)], axis=1).

# Original DF is "X" and the new DF is "encoder_vars_df".

The reason for the "reset_index" on both sets is that when concatenating, this will ensure that no rows are not aligned, as if they are,
we end up with missing values.

axis=1 - means we're we want let Pandas know we're concatenating columns and not rows.

So we now have our 3 original input variables (input 1-3) as well as the encoded variables.
X_new
Out[10]: 
   input1 input2 input3  input2_A  input2_B  input2_C  input3_X  input3_Y
0       1      A      X       1.0       0.0       0.0       1.0       0.0
1       2      A      X       1.0       0.0       0.0       1.0       0.0
2       3      B      X       0.0       1.0       0.0       1.0       0.0
3       4      B      Y       0.0       1.0       0.0       0.0       1.0
4       5      C      Y       0.0       0.0       1.0       0.0       1.0

The next thing that we need to do is to drop the original input2 and input3 columns as we no longer need them (they've been encoded).
X_new.drop(categorical_vars, axis=1, inplace=True) -  inplace=True, means that the changes are applied to the "X_new" object rather than
just printed to the console. axis=1 - means we're we dealing with columns and not rows.  

X_new.drop(categorical_vars, axis=1, inplace=True)

X_new
Out[12]: 
   input1  input2_A  input2_B  input2_C  input3_X  input3_Y
0       1       1.0       0.0       0.0       1.0       0.0
1       2       1.0       0.0       0.0       1.0       0.0
2       3       0.0       1.0       0.0       1.0       0.0
3       4       0.0       1.0       0.0       0.0       1.0
4       5       0.0       0.0       1.0       0.0       1.0 

## The Dummy Variable Trap

When using one hot encoding, depending on the type of model we're applying, we can fall into something called the "Dummy Variable Trap",
which is where input variables perfectly predict each each other, and this violates an assumption of something called multi-collinearity.

All we need to do is to `drop = "first"` as a second parameter to our "one_hot_encoder" object, This will ensure that one of the encoded
columns is always removed. 

After, we re-run our code beginning from the "one_hot_encoder", we see that it has dropped one of the encoded columns for input2 and one for 
input3. Tend to drop "input2_A" and "input2_X"

X_new
Out[15]: 
   input1  input2_B  input2_C  input3_Y
0       1       0.0       0.0       0.0
1       2       0.0       0.0       0.0
2       3       1.0       0.0       0.0
3       4       1.0       0.0       1.0
4       5       0.0       1.0       1.0                                                                                                        

We can then put this into our ML.
'''

encoder_vars_array = one_hot_encoder.fit_transform(X[categorical_vars])

# What each col represents

encoder_feature_names = one_hot_encoder.get_feature_names_out(categorical_vars)

# put this encoded data back with the other input variables that didn't need encoding, and the columns names will be the encoder_feature_names
# as indicated in the parameter passed to the DF: columns=encoder_feature_names.

encoder_vars_df = pd.DataFrame(encoder_vars_array, columns=encoder_feature_names)

# concatenate this new data frame back onto our original input variables data Data frame
# Original DF is "X" and the new DF is "encoder_vars_df".
X_new = pd.concat([X.reset_index(drop=True), encoder_vars_df.reset_index(drop=True)], axis=1)

# The next thing that we need to do is to drop the original input2 and input3 columns as we no longer need them

X_new.drop(categorical_vars, axis=1, inplace=True)
