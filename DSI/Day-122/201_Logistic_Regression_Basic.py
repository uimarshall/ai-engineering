############################################################

# Logistic Regression - Basic Template

############################################################

# Import required packages


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Import the data

my_df = pd.read_csv("data/sample_data_classification.csv")


# Split data into input and output objects, this is because that is how sklearn want to receive thr data.

# Features (X): the input information you give the model. Example: house size, number of rooms, location.
X = my_df.drop(["output"], axis = 1)
# Target (y): the number you want the model to predict. Example: the house price.
y = my_df["output"]

# Split data into training and test sets

# Training set: the data the model learns from proportion of test data = 0.2 = 20%, (80%) of data will go into training.
# Test set: the data we use to check how well the model learned (data it has never seen before).
# stratify=y means our test data and training set should contain the same proportion of 1s & 0s as the overall data.

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


# Instantiate our model object

clf = LogisticRegression(random_state=42)


# Train our model:  i.e. the model has now been trained by our training data.
clf.fit(X_train, y_train)

# Assess model accuracy: Use the model to make predictions
y_pred = clf.predict(X_test) # This return 0s & 1s.

# y_test is the actual data set, y_pred is what the model predicted based on the actual data.
'''
accuracy_score(y_test, y_pred)
Out[7]: 0.8 => This means that of the 20 data points in our test set (i.e the y_pred has 20 datas), we predicted the correct class for 16
of them. 80% correct prediction or classification.
'''
accuracy_score(y_test, y_pred)

y_pred_prob = clf.predict_proba(X_test) # This return a probability values that will fall under 0s & 1s.

# Confusion Matrix

conf_matrix = confusion_matrix(y_test, y_pred)
print(conf_matrix)

plt.style.available

plt.style.use("seaborn-v0_8-poster")
plt.matshow(conf_matrix, cmap = "coolwarm")
plt.gca().xaxis.tick_bottom()
plt.title("Confusion Matrix")
plt.ylabel("Actual Class")
plt.xlabel("Predicted Class")

for (i, j), corr_value in np.ndenumerate(conf_matrix):
    plt.text(j, i, corr_value, ha = "center", va = "center", fontsize = 20)
plt.show()    