#############################

# Import required packages
import pandas as pd
import pickle

# Import customers for scoring
to_be_scored = pickle.load(open("data/abc_regression_scoring.p", "rb"))

# Import model and model objects

regressor = pickle.load(open("data/random_forest_regression_model.p", "rb"))
one_hot_encoder = pickle.load(open("data/random_forest_regression_ohe.p", "rb"))

# Drop unused columns

to_be_scored.drop(["customer_id"], axis = 1, inplace = True)

# Drop missing values

to_be_scored.dropna(how = "any", inplace = True)

# Apply One Hot Encoding

categorical_vars = ["gender"]

encoder_vars_array = one_hot_encoder.transform(to_be_scored[categorical_vars])

# What each col represents

encoder_feature_names = one_hot_encoder.get_feature_names_out(categorical_vars)

# put this encoded data back with the other input variables that didn't need encoding, and the columns names will be the encoder_feature_names
# as indicated in the parameter passed to the DF: columns=encoder_feature_names.

encoder_vars_df = pd.DataFrame(encoder_vars_array, columns=encoder_feature_names)

# concatenate this new data frame back onto our original input variables data Data frame
# Original DF is "X" and the new DF is "encoder_vars_df".
to_be_scored = pd.concat([to_be_scored.reset_index(drop=True), encoder_vars_df.reset_index(drop=True)], axis=1)

# The next thing that we need to do is to drop the original input2 and input3 columns as we no longer need them

to_be_scored.drop(categorical_vars, axis=1, inplace=True)

# Make our predictions

loyalty_predictions = regressor.predict(to_be_scored)

