"""
Feature Scaling for Machine Learning — Practical Tutorial Script
=================================================================
Run with:  python feature_scaling_tutorial.py

Requirements: numpy, pandas, scikit-learn, matplotlib
Each line/section is commented for beginners.
"""

# ---------------------------------------------------------------
# Imports: the libraries we need for data + scaling + ML
# ---------------------------------------------------------------
import numpy as np                                   # numerical arrays
import pandas as pd                                  # dataframes (nice printing)
import matplotlib.pyplot as plt                      # plotting
from sklearn.preprocessing import (
    MinMaxScaler,        # rescales features to [0, 1]
    StandardScaler,      # mean=0, std=1 (z-score)
    RobustScaler,        # uses median & IQR (outlier-safe)
    MaxAbsScaler,        # divides by max absolute value
)
from sklearn.model_selection import train_test_split   # split data into train/test
from sklearn.neighbors import KNeighborsClassifier     # a distance-based model
from sklearn.linear_model import LogisticRegression    # gradient-descent-based model
from sklearn.pipeline import Pipeline                  # chains steps together safely
import joblib                                          # save objects to disk

# ---------------------------------------------------------------
# 1. CREATE A SMALL EXAMPLE DATASET
#    Two features on VERY different scales:
#    'age' (tens) and 'income' (tens of thousands)
# ---------------------------------------------------------------
data = pd.DataFrame({
    "age":    [25, 40, 60, 35, 50, 23, 45, 67, 31, 52],
    "income": [30000, 55000, 90000, 45000, 120000, 28000, 60000, 95000, 40000, 80000],
})
print("=== Raw data (note the huge scale difference) ===")
print(data)

# ---------------------------------------------------------------
# 2. APPLY EACH SCALER AND COMPARE THE OUTPUTS
#    fit_transform: learns the scaling stats (min/max, mean/std...)
#    from the data AND applies them in one call.
# ---------------------------------------------------------------
scalers = {
    "MinMax": MinMaxScaler(),       # output range [0, 1]
    "Standard": StandardScaler(),   # mean 0, std 1
    "Robust": RobustScaler(),       # median 0, based on IQR
    "MaxAbs": MaxAbsScaler(),       # range [-1, 1]
}

for name, scaler in scalers.items():
    scaled = scaler.fit_transform(data)            # fit on data, then transform it
    scaled_df = pd.DataFrame(scaled, columns=["age", "income"])
    print(f"\n=== {name}Scaler output ===")
    print(scaled_df.round(3))

# ---------------------------------------------------------------
# 3. SHOW WHY SCALE MATTERS: DISTANCE BETWEEN TWO PEOPLE
#    Euclidean distance should reflect both age AND income fairly.
# ---------------------------------------------------------------
person_a = np.array([[30, 50000]])
person_b = np.array([[35, 51000]])   # 5 years older, 1000 richer

raw_distance = np.linalg.norm(person_a - person_b)          # distance on raw data
std = StandardScaler().fit(data)                            # learn the stats
scaled_distance = np.linalg.norm(std.transform(person_a) - std.transform(person_b))

print("\n=== Distance between two similar people ===")
print(f"Raw distance:    {raw_distance:.4f}  (dominated by the 1000 income gap)")
print(f"Scaled distance: {scaled_distance:.4f}  (age gap now counts properly)")

# ---------------------------------------------------------------
# 4. PLOT: raw vs scaled features (visual intuition)
# ---------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].scatter(data["age"], data["income"])                 # raw scatter plot
axes[0].set_title("Raw data (income dwarfs age)")
axes[0].set_xlabel("age"); axes[0].set_ylabel("income")

scaled = StandardScaler().fit_transform(data)                # z-score the data
axes[1].scatter(scaled[:, 0], scaled[:, 1])                  # scaled scatter plot
axes[1].set_title("Standardized data (comparable scales)")
axes[1].set_xlabel("age (z-score)"); axes[1].set_ylabel("income (z-score)")

plt.tight_layout()
plt.savefig("/mnt/agents/output/scaling_comparison.png", dpi=120)  # save the figure
print("\nPlot saved to scaling_comparison.png")

# ---------------------------------------------------------------
# 5. REAL-DEMO: KNN WITH AND WITHOUT SCALING
#    We generate a synthetic dataset where BOTH features matter,
#    then show scaling improves a distance-based model.
# ---------------------------------------------------------------
from sklearn.datasets import make_classification            # built-in synthetic data generator

X, y = make_classification(
    n_samples=500,          # 500 rows
    n_features=2,           # 2 input features
    n_informative=2,        # both features are actually useful
    n_redundant=0,          # no useless copies
    weights=[0.5, 0.5],     # balanced classes
    random_state=42,        # reproducible results
)

# Give feature 1 a much larger scale than feature 0 (mimics age vs income)
X[:, 1] = X[:, 1] * 1000

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42   # 70% train / 30% test
)

# --- WRONG way: scale everything BEFORE splitting (leakage!) ---
# (Shown commented out so you don't copy it by accident)
# bad_scaler = StandardScaler().fit(X)   # <- fits on ALL data including test

# --- CORRECT way: fit scaler on TRAIN ONLY ---
scaler = StandardScaler()                       # create the scaler
X_train_scaled = scaler.fit_transform(X_train)  # learn stats from train, transform train
X_test_scaled = scaler.transform(X_test)        # apply SAME stats to test (no refitting!)

# Train KNN on raw data
knn_raw = KNeighborsClassifier(n_neighbors=5)   # 5-neighbor classifier
knn_raw.fit(X_train, y_train)                   # fit on unscaled training data
acc_raw = knn_raw.score(X_test, y_test)         # accuracy on unscaled test data

# Train KNN on scaled data
knn_scaled = KNeighborsClassifier(n_neighbors=5)
knn_scaled.fit(X_train_scaled, y_train)         # fit on scaled training data
acc_scaled = knn_scaled.score(X_test_scaled, y_test)  # accuracy on scaled test data

print("\n=== KNN accuracy comparison (synthetic demo dataset) ===")
print(f"Without scaling: {acc_raw:.3f}")
print(f"With scaling:    {acc_scaled:.3f}")

# ---------------------------------------------------------------
# 6. LOGISTIC REGRESSION ALSO BENEFITS (gradient descent converges faster)
# ---------------------------------------------------------------
logreg_raw = LogisticRegression(max_iter=10)    # deliberately few iterations
logreg_raw.fit(X_train, y_train)                # may struggle to converge
print(f"\nLogisticRegression (raw, 10 iters):  {logreg_raw.score(X_test, y_test):.3f}")

logreg_scaled = LogisticRegression(max_iter=10)
logreg_scaled.fit(X_train_scaled, y_train)      # converges faster on scaled data
print(f"LogisticRegression (scaled, 10 iters): {logreg_scaled.score(X_test_scaled, y_test):.3f}")

# ---------------------------------------------------------------
# 7. BEST PRACTICE: PIPELINE (scaler + model in one leak-proof object)
# ---------------------------------------------------------------
pipe = Pipeline([
    ("scaler", StandardScaler()),                    # step 1: scale (fits on train only)
    ("knn", KNeighborsClassifier(n_neighbors=5)),    # step 2: the model
])
pipe.fit(X_train, y_train)                           # train the whole pipeline
print(f"\nPipeline (scaler + KNN) accuracy: {pipe.score(X_test, y_test):.3f}")

# The pipeline can even scale a SINGLE new sample for prediction
new_person = np.array([[35, 62000]])                 # e.g., age=35, income=62000
prediction = pipe.predict(new_person)                # scaling happens automatically inside
print(f"Prediction for new sample {new_person.tolist()}: {prediction}")

# ---------------------------------------------------------------
# 8. SAVE THE FITTED PIPELINE FOR LATER USE (deployment)
# ---------------------------------------------------------------
joblib.dump(pipe, "/mnt/agents/output/scaling_pipeline.joblib")
print("\nPipeline saved to scaling_pipeline.joblib")
print("Load it later with: pipe = joblib.load('scaling_pipeline.joblib')")

# ---------------------------------------------------------------
# 9. BONUS: inverse_transform (turn scaled values back to originals)
# ---------------------------------------------------------------
original_back = scaler.inverse_transform(X_test_scaled[:3])  # undo the scaling
print("\nFirst 3 test rows restored to original scale:")
print(np.round(original_back, 1))

print("\nDone! You now know how and when to scale features.")
