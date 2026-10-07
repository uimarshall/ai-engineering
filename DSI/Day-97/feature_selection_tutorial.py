"""
Feature Selection in Machine Learning - Practical Tutorial Code
================================================================
Companion to feature_selection_tutorial.md.

Every block below corresponds to one section of the tutorial.
Run it top to bottom:  python feature_selection_tutorial.py
Each line/statement has a comment explaining what it does.
"""

# ---------------------------------------------------------------------------
# Section 2: Setup and first look at the data
# ---------------------------------------------------------------------------

from typing import cast  # tells type checkers the guaranteed dataset return types

import matplotlib.pyplot as plt  # matplotlib: drawing charts
import numpy as np  # NumPy: numerical arrays and math
import pandas as pd  # pandas: tables (DataFrames) for our data
from sklearn.datasets import (
    load_breast_cancer,  # built-in medical dataset (no download needed)
)
from sklearn.model_selection import (  # data splitting + evaluation
    cross_val_score,
    train_test_split,
)
from sklearn.preprocessing import StandardScaler  # scales features to mean 0 / std 1

# Load the dataset directly as feature and label pandas objects. Explicitly
# unpack the return_X_y=True tuple so type checkers know these are X and y.
X, y = cast(
    tuple[pd.DataFrame, pd.Series],
    load_breast_cancer(as_frame=True, return_X_y=True),
)  # X = 30 feature columns; y = labels (0=malignant, 1=benign)

print(f"Dataset shape: {X.shape}")  # prints (rows, columns) = (569, 30)
print(
    f"Any missing values? {pd.isna(X).sum().sum()}"
)  # counts NaNs; 0 means the data is already clean

# Split into 80% training / 20% testing, keeping the class ratio (stratify)
# random_state=42 fixes the random shuffling so we get the SAME split every run
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# StandardScaler learns the mean/std from TRAINING data only (fit_transform),
# then applies the SAME transformation to the test set (transform) - no leakage.
scaler = StandardScaler()  # create the scaler object
X_train_scaled = pd.DataFrame(
    scaler.fit_transform(X_train), columns=X.columns
)  # fit on train, transform train
X_test_scaled = pd.DataFrame(
    scaler.transform(X_test), columns=X.columns
)  # transform test with train stats

# ---------------------------------------------------------------------------
# Section 3.1: Filter method - VarianceThreshold (drop near-constant columns)
# ---------------------------------------------------------------------------

from sklearn.feature_selection import (
    VarianceThreshold,  # removes features with tiny variance
)

selector = VarianceThreshold(threshold=0.01)  # drop any feature whose variance < 0.01
X_train_var = selector.fit_transform(
    X_train_scaled
)  # learn variances on train, drop weak columns

kept = X.columns[
    selector.get_support()
]  # get_support() -> True/False mask of surviving columns
dropped = set(X.columns) - set(
    kept
)  # the set difference shows which columns were removed
print(
    f"Variance threshold: kept {len(kept)} of {X.shape[1]} features. Dropped: {dropped}"
)

# ---------------------------------------------------------------------------
# Section 3.2: Filter method - correlation heatmap (spot redundant features)
# ---------------------------------------------------------------------------

corr = X_train_scaled.corr()  # compute pairwise Pearson correlation of all features

plt.figure(figsize=(12, 10))  # create a wide figure for the heatmap
plt.imshow(
    corr, cmap="coolwarm", vmin=-1, vmax=1
)  # draw the correlation matrix as colours (-1 blue .. +1 red)
plt.colorbar(label="correlation")  # add a colour scale legend
plt.xticks(
    range(len(corr)), corr.columns.tolist(), rotation=90, fontsize=7
)  # label x-axis with feature names, vertical
plt.yticks(
    range(len(corr)), corr.columns.tolist(), fontsize=7
)  # label y-axis with feature names
plt.title("Feature correlation matrix")  # chart title
plt.tight_layout()  # tighten margins so nothing is cut off
plt.show()  # display the chart

# ---------------------------------------------------------------------------
# Section 3.3: Filter method - Mutual Information + SelectKBest
# ---------------------------------------------------------------------------

from sklearn.feature_selection import (  # MI scorer + "keep top-k" wrapper
    SelectKBest,
    mutual_info_classif,
)

# Compute how much each feature tells us about the label (train data only)
mi_scores = mutual_info_classif(
    X_train_scaled, y_train, random_state=42
)  # array of 30 MI scores
mi_series = pd.Series(
    mi_scores, index=X.columns
).sort_values()  # put scores in a Series, sorted low->high

mi_series.plot.barh(
    figsize=(8, 8), title="Mutual information with target"
)  # horizontal bar chart of MI scores
plt.xlabel("MI score")  # x-axis label
plt.show()  # display the chart

top10 = SelectKBest(
    mutual_info_classif, k=10
)  # selector that keeps the 10 features with highest MI
X_train_mi = top10.fit_transform(
    X_train_scaled, y_train
)  # score features on TRAIN set, keep best 10
X_test_mi = top10.transform(X_test_scaled)  # apply the SAME selection to the test set

print("Top 10 features by mutual information:", list(X.columns[top10.get_support()]))

# ---------------------------------------------------------------------------
# Section 4.1: Wrapper method - Recursive Feature Elimination (RFE)
# ---------------------------------------------------------------------------

from sklearn.feature_selection import RFE  # removes weakest features one at a time
from sklearn.linear_model import (
    LogisticRegression,  # simple linear classifier used as the "judge"
)

model = LogisticRegression(
    max_iter=5000
)  # create the model (max_iter raised so it always converges)

rfe = RFE(
    estimator=model, n_features_to_select=10, step=1
)  # eliminate 1 feature per round until 10 remain
rfe.fit(X_train_scaled, y_train)  # run the train -> rank -> remove loop

rfe_features = X.columns[rfe.get_support()]  # the 10 features RFE decided to keep
print("RFE selected:", list(rfe_features))

# ---------------------------------------------------------------------------
# Section 4.2: Choosing k - sweep the number of features with cross-validation
# ---------------------------------------------------------------------------

results = {}  # will store mean F1 score for each k
for k in [5, 10, 15, 20, 30]:  # try keeping 5, 10, 15, 20, or all 30 features
    rfe_k = RFE(
        LogisticRegression(max_iter=5000), n_features_to_select=k
    )  # fresh RFE for this k
    scores = cross_val_score(
        rfe_k, X_train_scaled, y_train, cv=5, scoring="f1"
    )  # 5-fold CV F1 score
    results[k] = scores.mean()  # record the average F1 for this k
    print(f"k={k:2d} -> F1 = {scores.mean():.4f}")  # :.4f prints 4 decimal places

# ---------------------------------------------------------------------------
# Section 5.1: Embedded method - Lasso (L1) zeroes out weak features
# ---------------------------------------------------------------------------

# penalty="l1" = Lasso-style penalty that pushes useless coefficients to exactly 0
lasso = LogisticRegression(penalty="l1", solver="liblinear", C=0.1, max_iter=5000)
lasso.fit(X_train_scaled, y_train)  # train; weak features end with coefficient 0

lasso_coefs = pd.Series(
    np.abs(lasso.coef_[0]), index=X.columns
).sort_values()  # size of each coefficient
lasso_coefs.plot.barh(
    figsize=(8, 8), title="|Lasso coefficients| (0 = dropped)"
)  # bar chart; zero bars = dropped
plt.show()  # display the chart

print("Features kept by Lasso (non-zero):", int((lasso.coef_[0] != 0).sum()), "of 30")

# ---------------------------------------------------------------------------
# Section 5.2: Embedded method - Random Forest feature importances
# ---------------------------------------------------------------------------

from sklearn.ensemble import RandomForestClassifier  # an ensemble of decision trees

forest = RandomForestClassifier(
    n_estimators=200, random_state=42
)  # 200 trees, fixed seed for reproducibility
forest.fit(X_train, y_train)  # fit on the UNSCALED data (trees don't need scaling)

importances = pd.Series(
    forest.feature_importances_, index=X.columns
).sort_values()  # built-in importance score
importances.plot.barh(
    figsize=(8, 8), title="Random Forest feature importance"
)  # bar chart of importances
plt.show()  # display the chart

# ---------------------------------------------------------------------------
# Section 6: Production-style Pipeline (scale -> select -> model), leak-free
# ---------------------------------------------------------------------------

from sklearn.metrics import classification_report  # precision/recall/f1 summary
from sklearn.pipeline import Pipeline  # chains steps so they run together inside CV

pipe = Pipeline(
    [
        (
            "scaler",
            StandardScaler(),
        ),  # step 1: scale features (fit inside the pipeline)
        (
            "select",
            SelectKBest(mutual_info_classif, k=10),
        ),  # step 2: keep top-10 features by mutual information
        ("model", LogisticRegression(max_iter=5000)),  # step 3: train the classifier
    ]
)

pipe.fit(X_train, y_train)  # train all three steps end-to-end on the training set
print(
    classification_report(  # compare predictions vs true test labels
        y_test,  # true labels of the test set
        pipe.predict(X_test),  # predictions made by the fitted pipeline
        target_names=[
            "malignant",
            "benign",
        ],  # human-readable names for classes 0 and 1
    )
)

# Cross-validate the WHOLE pipeline on all data -> honest estimate of real performance
cv_score = cross_val_score(
    pipe, X, y, cv=5, scoring="f1"
).mean()  # mean F1 across 5 folds
print(f"Cross-validated F1 of pipeline: {cv_score:.4f}")

print(
    "\nTutorial complete! Compare the bar charts to see how the methods agree (or disagree)."
)
