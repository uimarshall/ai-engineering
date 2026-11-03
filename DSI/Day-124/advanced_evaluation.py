"""Advanced evaluation: accuracy vs precision, recall and F1 on imbalanced data."""

# numpy: numerical arrays
import numpy as np
# make_classification: builds a fake dataset we can control
from sklearn.datasets import make_classification
# train_test_split: splits data into training and test parts
from sklearn.model_selection import train_test_split
# LogisticRegression: the classifier we will evaluate
from sklearn.linear_model import LogisticRegression
# DummyClassifier: a "model" that ignores the data (baseline)
from sklearn.dummy import DummyClassifier
# metrics: the evaluation tools
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
)

# ---------------------------------------------------------------
# 1. The tutorial's example, calculated by hand from the confusion matrix
# ---------------------------------------------------------------
tp, fp, fn, tn = 1, 1, 1, 97  # 100 patients: 2 sick, 1 found, 1 false alarm

accuracy = (tp + tn) / (tp + tn + fp + fn)  # share of all predictions that were right
precision = tp / (tp + fp)  # of those predicted sick, how many really were
recall = tp / (tp + fn)  # of those really sick, how many we found
f1 = 2 * precision * recall / (precision + recall)  # harmonic mean of the two

print("--- Worked example (by hand) ---")
print(f"Accuracy : {accuracy:.2f}")  # 0.98 - looks great but misleading
print(f"Precision: {precision:.2f}")  # 0.50
print(f"Recall   : {recall:.2f}")  # 0.50
print(f"F1 score : {f1:.2f}")  # 0.50


# ---------------------------------------------------------------
# 2. Why F1 punishes imbalance between precision and recall
# ---------------------------------------------------------------
def f1_from(p, r):
    """Return the F1 score for a given precision p and recall r."""
    return 2 * p * r / (p + r)  # harmonic mean formula


print("\n--- F1 for different precision/recall pairs ---")
for p, r in [(0.5, 0.5), (0.6, 0.4), (0.8, 0.25)]:  # loop over the three cases
    print(f"precision={p:.2f} recall={r:.2f} -> F1={f1_from(p, r):.2f}")

# ---------------------------------------------------------------
# 3. A real model on imbalanced data (about 2% positive class)
# ---------------------------------------------------------------
X, y = make_classification(
    n_samples=5000,  # number of patients
    n_features=10,  # number of measurements per patient
    n_informative=5,  # features that really carry signal
    weights=[0.98, 0.02],  # 98% healthy, 2% diseased -> imbalanced
    flip_y=0.01,  # a little label noise to make it realistic
    random_state=42,  # makes results repeatable
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,  # 20% of data kept for testing
    stratify=y,  # keep the 2% ratio in both splits
    random_state=42,
)

# Baseline: always predicts the most common class ("healthy")
baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
# Real model: logistic regression trained on the training data
model = LogisticRegression(max_iter=1000).fit(X_train, y_train)


def evaluate(name, clf):
    """Print the confusion matrix and the four metrics for a fitted model."""
    y_pred = clf.predict(X_test)  # predicted classes for the test set
    print(f"\n=== {name} ===")
    print("Confusion matrix [[TN FP] [FN TP]]:")
    print(confusion_matrix(y_test, y_pred))  # counts of each outcome type
    print(f"Accuracy : {accuracy_score(y_test, y_pred):.3f}")
    # zero_division=0 avoids a warning when nothing is predicted positive
    print(f"Precision: {precision_score(y_test, y_pred, zero_division=0):.3f}")
    print(f"Recall   : {recall_score(y_test, y_pred):.3f}")
    print(f"F1 score : {f1_score(y_test, y_pred):.3f}")


evaluate("Baseline (always 'healthy')", baseline)
evaluate("Logistic Regression", model)

# class_weight="balanced" makes mistakes on the rare class cost more
balanced_model = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X_train, y_train)
evaluate("Logistic Regression (class_weight='balanced')", balanced_model)

# ---------------------------------------------------------------
# 4. Precision/recall trade-off: move the decision threshold
# ---------------------------------------------------------------
probs = model.predict_proba(X_test)[:, 1]  # predicted probability of disease

print("\n--- Threshold trade-off ---")
for threshold in [0.1, 0.3, 0.5, 0.7]:
    y_pred = (probs >= threshold).astype(int)  # 1 if probability passes threshold
    p = precision_score(y_test, y_pred, zero_division=0)
    r = recall_score(y_test, y_pred)
    f = f1_score(y_test, y_pred)
    print(f"threshold={threshold:.1f} precision={p:.2f} recall={r:.2f} F1={f:.2f}")

# ---------------------------------------------------------------
# 5. One-shot summary report
# ---------------------------------------------------------------
print("\n--- Classification report ---")
print(classification_report(y_test, model.predict(X_test), zero_division=0))
