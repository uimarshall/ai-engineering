############################################################

# PCA - Code Template

############################################################

import matplotlib.pyplot as plt

# Import required packages
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Import data

data_for_model = pd.read_csv("data/sample_data_pca.csv")

# Drop unnecessary cols - e.g. "user_id" since it cannot serve as input variables

data_for_model.drop("user_id", axis=1, inplace=True)

# Shuffle data

data_for_model = data_for_model.sample(frac=1, random_state=42)

# Class Balance - To see the balance btw the 1s & 0s for the output variable, how proportionate they are.

data_for_model["purchased_album"].value_counts(normalize=True)

#############################################

# Deal with missing values

############################################

data_for_model.isna().sum().sum()  # check for missing values in the cols.
data_for_model.dropna(
    how="any", inplace=True
)  # drop the rows that have those missing values e.g index 576

##############################################

# Split Input Variables & Output Variable

##############################################

X = data_for_model.drop(["purchased_album"], axis=1)
y = data_for_model["purchased_album"]

# Split out Training & Test sets -
# stratify=y means Test &Train set should have the same proportion of 1s & 0s as the overall data

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

############################################################
# Feature Scaling
############################################################

scale_standard = StandardScaler()
X_train = scale_standard.fit_transform(X_train)
X_test = scale_standard.transform(X_test)


############################################################
# Apply PCA
############################################################


# Instantiate & Fit
pca = PCA(n_components=None, random_state=42)
pca.fit(X_train)

# Extract the explained variance across components
explained_variance = pca.explained_variance_ratio_
explained_variance_cummulative = pca.explained_variance_ratio_.cumsum()

############################################################
# Plot the explained variance across components
############################################################

# Create list for number of components

num_vars_list = list(range(1, 101))
plt.figure(figsize=(15, 10))

# Plot the explained variance by each component
plt.subplot(2, 1, 1)
plt.bar(num_vars_list, explained_variance)
plt.title("Variance across Principal Components")
plt.xlabel("Number of Components")
plt.ylabel("% Variance")
plt.tight_layout()

# Plot the cumulative variance
plt.subplot(2, 1, 2)
plt.plot(num_vars_list, explained_variance_cummulative)
plt.title("Cummulative Variance across Principal Components")
plt.xlabel("Number of Components")
plt.ylabel("Cummulative % Variance")
plt.tight_layout()
plt.show()

############################################################
# Apply PCA with selected number of components
############################################################

pca = PCA(n_components=0.75, random_state=42)
X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)

pca.n_components_

############################################################
# Apply PCA with selected number of components
############################################################

clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

############################################################
# Assess Model accuracy
############################################################

y_pred_class = clf.predict(X_test)
accuracy_score(y_test, y_pred_class)
