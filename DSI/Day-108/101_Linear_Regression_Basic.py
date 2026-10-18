############################################################

# Linear Regression - Basic Template

############################################################

# Import required packages


from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import pandas as pd


# Import the data

my_df = pd.read_csv("data/sample_data_regression.csv")


# Split data into input and output objects, this is because that is how sklearn want to receive thr data.

# Features (X): the input information you give the model. Example: house size, number of rooms, location.
X = my_df.drop(["output"], axis = 1)
# Target (y): the number you want the model to predict. Example: the house price.
y = my_df["output"]

# Split data into training and test sets

# Training set: the data the model learns from proportion of test data = 0.2 = 20%, (80%) of data will go into training.
# Test set: the data we use to check how well the model learned (data it has never seen before).

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Instantiate our model object

regressor = LinearRegression()


# Train our model: learn the best line from training data i.e. the model has now been trained by our training data.
regressor.fit(X_train, y_train)

# Assess model accuracy: Use the model to make predictions
y_pred = regressor.predict(X_test)

# y_test is the actual data set, y_pred is what the model predicted based on the actual data.
r2_score(y_test, y_pred)