############################################################

# Random Forest For Regression - ABC Grocery Task

# The customer_loyalty_score is the output variable we want to predict.

############################################################

# Import required packages
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import OneHotEncoder
from sklearn.inspection import permutation_importance



# Import data

data_for_model = pickle.load(open("data/abc_regression_modelling.p", "rb"))

# Drop unnecessary cols - e.g. "customer_id" since it cannot serve as input variables

data_for_model.drop("customer_id", axis = 1, inplace = True)

# Shuffle data

data_for_model = data_for_model.sample(frac=1, random_state=42)

# Deal with missing values

data_for_model.isna().sum() # check for missing values in the cols.
data_for_model.dropna(how = "any", inplace = True) # drop the rows that have those missing values e.g index 576

    
# Split Input Variables & Output Variable

X = data_for_model.drop(["customer_loyalty_score"], axis = 1) # input variables
y = data_for_model["customer_loyalty_score"]

# Split out Training & Test sets

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Dealing with categorical variables

categorical_vars = ["gender"]

one_hot_encoder = OneHotEncoder(sparse_output=False, drop = "first") 

X_train_encoded = one_hot_encoder.fit_transform(X_train[categorical_vars])
X_test_encoded = one_hot_encoder.transform(X_test[categorical_vars])

if not isinstance(X_train_encoded, np.ndarray):
    raise TypeError("OneHotEncoder returned sparse output despite sparse_output=False")
if not isinstance(X_test_encoded, np.ndarray):
    raise TypeError("OneHotEncoder returned sparse output despite sparse_output=False")

# What each col represents

encoder_feature_names = one_hot_encoder.get_feature_names_out(categorical_vars)

X_train_encoded = pd.DataFrame(X_train_encoded, columns=encoder_feature_names)
X_train = pd.concat([X_train.reset_index(drop=True), X_train_encoded.reset_index(drop=True)], axis=1)
X_train.drop(categorical_vars, axis=1, inplace=True)

X_test_encoded = pd.DataFrame(X_test_encoded, columns=encoder_feature_names)
X_test = pd.concat([X_test.reset_index(drop=True), X_test_encoded.reset_index(drop=True)], axis=1)
X_test.drop(categorical_vars, axis=1, inplace=True) 


# Model training

regressor = RandomForestRegressor(random_state=42)
regressor.fit(X_train, y_train)

#########################################

# Model Assessment

#########################################

# Predict On the test Set
y_pred = regressor.predict(X_test)

# Calcualte R-Squared
r_squared = r2_score(y_test, y_pred)
print(r_squared)

# Cross Validation

cv = KFold(n_splits=4, shuffle=True, random_state=42)
cv_scores = cross_val_score(regressor, X_train, y_train, cv=cv, scoring="r2")
cv_scores.mean()

# Calcualte Adjusted R-Squared

num_data_points, num_input_vars = X_test.shape
adjusted_r_squared = 1 - (1 - r_squared) * (num_data_points - 1) / (num_data_points - num_input_vars - 1)
print(adjusted_r_squared)

# Feature Importance (What features are we looking at to predict the importance)


feature_importance = pd.DataFrame(regressor.feature_importances_)
feature_names = pd.DataFrame(X.columns)
feature_importance_summary = pd.concat([feature_names, feature_importance], axis=1)
feature_importance_summary.columns = ["input_variable", "feature_importance"]
feature_importance_summary.sort_values(by = "feature_importance", inplace = True)

plt.barh(feature_importance_summary["input_variable"], feature_importance_summary["feature_importance"])
plt.title("Feature Importance of Random Forest")
plt.xlabel("Feature importance")
plt.tight_layout()
plt.show()

# Permutation Importance

# Each of our input variable is run 10m times using the n_repeats params 

result = permutation_importance(regressor, X_test, y_test, n_repeats=10, random_state=42)

permutation_importance = pd.DataFrame(result["importances_mean"])
feature_names = pd.DataFrame(X.columns)
permutation_importance_summary = pd.concat([feature_names, permutation_importance], axis=1)
permutation_importance_summary.columns = ["input_variable", "permutation_importance"]
permutation_importance_summary.sort_values(by = "permutation_importance", inplace = True)

plt.barh(permutation_importance_summary["input_variable"], permutation_importance_summary["permutation_importance"])
plt.title("Permutation Importance of Random Forest")
plt.xlabel("Permutation importance")
plt.tight_layout()
plt.show()

# Predictions under the hood

y_pred[0]
new_data = [X_test.iloc[0]]
regressor.estimators_

predictions = []
tree_count = 0
for tree in regressor.estimators_:
    prediction = tree.predict(new_data)[0]
    predictions.append(prediction)
    tree_count +=1
    
print(predictions)    

print(sum(predictions) / tree_count)

import pickle
pickle.dump(regressor, open("data/random_forest_regression_model.p", "wb"))
pickle.dump(one_hot_encoder, open("data/random_forest_regression_ohe.p", "wb"))
