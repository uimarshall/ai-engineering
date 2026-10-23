############################################################

# Linear Regression - ABC Grocery Task

############################################################

import pickle

import matplotlib.pyplot as plt
import numpy as np

# Import required packages
import pandas as pd
from sklearn.feature_selection import RFECV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils import shuffle

# Import data

data_for_model = pickle.load(open("data/abc_regression_modelling.p", "rb"))

# Drop unnecessary cols - e.g. "customer_id" since it cannot serve as input variables

data_for_model.drop("customer_id", axis=1, inplace=True)

# Shuffle data

data_for_model = pd.DataFrame(shuffle(data_for_model, random_state=42))

# Deal with missing values

data_for_model.isna().sum()  # check for missing values in the cols.
data_for_model.dropna(
    how="any", inplace=True
)  # drop the rows that have those missing values e.g index 576

# Deal with outliers

outlier_investigation = data_for_model.describe()

outlier_columns = ["distance_from_store", "total_sales", "total_items"]


# Boxplot appreoach

for column in outlier_columns:
    lower_quartile = data_for_model[column].quantile(0.25)
    upper_quartile = data_for_model[column].quantile(0.75)
    iqr = upper_quartile - lower_quartile
    iqr_extended = iqr * 2
    # Then apply the extended interquartile range to our lower and upper quartiles.
    min_border = lower_quartile - iqr_extended
    max_border = upper_quartile + iqr_extended

    # see if any of these data points do indeed fall outside of these boundaries.

    outliers = data_for_model[
        (data_for_model[column] < min_border) | (data_for_model[column] > max_border)
    ].index  # return the index values for any outliers
    print(f"{len(outliers)} outliers detected in column {column}")

    # Next, if any outlier is found we can then drop them
    data_for_model.drop(outliers, inplace=True)

# Split Input Variables & Output Variable

X = data_for_model.drop(["customer_loyalty_score"], axis=1)
y = data_for_model["customer_loyalty_score"]

# Split out Training & Test sets

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Dealing with categorical variables

categorical_vars = ["gender"]

one_hot_encoder = OneHotEncoder(sparse_output=False, drop="first")

X_train_encoded = one_hot_encoder.fit_transform(X_train[categorical_vars])
X_test_encoded = one_hot_encoder.transform(X_test[categorical_vars])

# What each col represents

encoder_feature_names = one_hot_encoder.get_feature_names_out(categorical_vars)

X_train_encoded = pd.DataFrame(
    np.asarray(X_train_encoded), columns=encoder_feature_names
)
X_train = pd.concat(
    [X_train.reset_index(drop=True), X_train_encoded.reset_index(drop=True)], axis=1
)
X_train.drop(categorical_vars, axis=1, inplace=True)

X_test_encoded = pd.DataFrame(np.asarray(X_test_encoded), columns=encoder_feature_names)
X_test = pd.concat(
    [X_test.reset_index(drop=True), X_test_encoded.reset_index(drop=True)], axis=1
)
X_test.drop(categorical_vars, axis=1, inplace=True)

# Feature Selection

regressor = LinearRegression()
feature_selector = RFECV(regressor)

fit = feature_selector.fit(X_train, y_train)

optimal_feature_count = feature_selector.n_features_
print(f"Optimal number of features: {optimal_feature_count}")

X_train = X_train.loc[:, feature_selector.get_support()]
X_test = X_test.loc[:, feature_selector.get_support()]


plt.plot(
    range(1, len(fit.cv_results_["mean_test_score"]) + 1),
    fit.cv_results_["mean_test_score"],
    marker="o",
)
plt.ylabel("Model Score")
plt.xlabel("Number of Features")
plt.title(
    f"Feature Selection using RFE \n Optimal number of features is {optimal_feature_count} (at score of {round(max(fit.cv_results_['mean_test_score']),4)})"
)
plt.tight_layout()
plt.show()

# Model training

regressor = LinearRegression()
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
adjusted_r_squared = 1 - (1 - r_squared) * (num_data_points - 1) / (
    num_data_points - num_input_vars - 1
)
print(adjusted_r_squared)

# Extract Model Coefficients

coefficients = pd.DataFrame(regressor.coef_)
input_variable_names = pd.DataFrame(X_train.columns)
summary_stats = pd.concat([input_variable_names, coefficients], axis=1)
summary_stats.columns = ["input_variable", "coefficient"]

# Extract Model Intercept

regressor.intercept_
