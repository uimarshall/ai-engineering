"""Changing the classification threshold: TPR, FPR, ROC curve, AUC and best-threshold search."""

# matplotlib: plotting library (non-interactive backend so the script also works without a display)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
# numpy: numerical arrays
import numpy as np
# make_classification: builds a fake dataset we can control
from sklearn.datasets import make_classification
# RandomForestClassifier: second model to compare against logistic regression
from sklearn.ensemble import RandomForestClassifier
# LogisticRegression: our main classifier
from sklearn.linear_model import LogisticRegression
# metrics: evaluation tools
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)
# train_test_split: splits data into training and test parts
from sklearn.model_selection import train_test_split

# ---------------------------------------------------------------
# 1. Tiny example from the lecture: 8 data points (4 positive, 4 negative)
# ---------------------------------------------------------------
y_true = np.array([0, 0, 0, 0, 1, 1, 1, 1])  # the real classes
# predicted probability of being positive for each point (sorted for readability)
probs_small = np.array([0.05, 0.10, 0.20, 0.60, 0.30, 0.55, 0.70, 0.90])


def rates_at(threshold):
    """Return (TPR, FPR) when probabilities >= threshold are called positive."""
    y_pred = (probs_small >= threshold).astype(int)  # turn probabilities into 0/1
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()  # unpack the 4 counts
    tpr = tp / (tp + fn)  # recall: of real positives, how many found
    fpr = fp / (fp + tn)  # of real negatives, how many wrongly flagged
    return tpr, fpr


print("--- Lecture example: TPR and FPR at different thresholds ---")
for t in [0.0, 0.25, 0.5, 0.75, 1.01]:  # 1.01 = unreachable, so nothing is positive
    tpr, fpr = rates_at(t)
    print(f"threshold={t:.2f}  TPR={tpr:.2f}  FPR={fpr:.2f}")

# ---------------------------------------------------------------
# 2. Realistic data: a balanced dataset
# ---------------------------------------------------------------
X, y = make_classification(
    n_samples=2000,  # number of rows
    n_features=10,  # number of columns
    n_informative=5,  # columns that carry real signal
    class_sep=0.8,  # how separable the classes are
    random_state=42,  # repeatable results
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42  # stratify keeps class ratio
)

# Train two models
log_reg = LogisticRegression(max_iter=1000).fit(X_train, y_train)
forest = RandomForestClassifier(n_estimators=200, random_state=42).fit(X_train, y_train)

# predict_proba returns [P(class 0), P(class 1)]; we keep column 1
probs_lr = log_reg.predict_proba(X_test)[:, 1]
probs_rf = forest.predict_proba(X_test)[:, 1]

# ---------------------------------------------------------------
# 3. Effect of moving the threshold on the confusion matrix
# ---------------------------------------------------------------
print("\n--- Logistic regression at different thresholds ---")
for t in [0.2, 0.5, 0.8]:
    y_pred = (probs_lr >= t).astype(int)  # apply the custom threshold
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    print(f"threshold={t:.1f}  TP={tp} FP={fp} FN={fn} TN={tn}  "
          f"TPR={tp / (tp + fn):.2f}  FPR={fp / (fp + tn):.2f}")

# ---------------------------------------------------------------
# 4. ROC curve, AUC and the best threshold (Youden's J = TPR - FPR)
# ---------------------------------------------------------------
fpr_lr, tpr_lr, thr_lr = roc_curve(y_test, probs_lr)  # one point per threshold
fpr_rf, tpr_rf, thr_rf = roc_curve(y_test, probs_rf)
auc_lr = roc_auc_score(y_test, probs_lr)  # area under the ROC curve
auc_rf = roc_auc_score(y_test, probs_rf)

best = np.argmax(tpr_lr - fpr_lr)  # point furthest above the diagonal
print("\n--- AUC comparison ---")
print(f"Logistic regression AUC: {auc_lr:.3f}")
print(f"Random forest AUC      : {auc_rf:.3f}")
print(f"Best ROC threshold (LR): {thr_lr[best]:.3f} "
      f"(TPR={tpr_lr[best]:.2f}, FPR={fpr_lr[best]:.2f})")

plt.figure(figsize=(6, 5))  # new figure
plt.plot(fpr_lr, tpr_lr, label=f"Logistic regression (AUC={auc_lr:.2f})")
plt.plot(fpr_rf, tpr_rf, label=f"Random forest (AUC={auc_rf:.2f})")
plt.plot([0, 1], [0, 1], "k--", label="Random guessing")  # the diagonal baseline
plt.scatter(fpr_lr[best], tpr_lr[best], c="red", zorder=5, label="Best threshold")
plt.xlabel("False positive rate")  # x-axis label
plt.ylabel("True positive rate")  # y-axis label
plt.title("ROC curve")
plt.legend()
plt.savefig("roc_curve.png", dpi=120)  # save instead of show so it runs anywhere
plt.close()

# ---------------------------------------------------------------
# 5. Imbalanced data: choose the threshold that maximises F1
# ---------------------------------------------------------------
Xi, yi = make_classification(
    n_samples=5000, n_features=10, n_informative=5,
    weights=[0.95, 0.05],  # 5% positives -> imbalanced
    class_sep=1.0, random_state=1,
)
Xi_tr, Xi_te, yi_tr, yi_te = train_test_split(
    Xi, yi, test_size=0.25, stratify=yi, random_state=1
)
imb_model = LogisticRegression(max_iter=1000).fit(Xi_tr, yi_tr)
imb_probs = imb_model.predict_proba(Xi_te)[:, 1]

# precision and recall for every possible threshold
precision, recall, thresholds = precision_recall_curve(yi_te, imb_probs)
# F1 for each threshold (last precision/recall point has no threshold, so drop it)
f1_scores = 2 * precision[:-1] * recall[:-1] / (precision[:-1] + recall[:-1] + 1e-12)
best_i = np.argmax(f1_scores)  # index of the highest F1
best_t = thresholds[best_i]  # the threshold that gave it

default_f1 = f1_score(yi_te, (imb_probs >= 0.5).astype(int))  # F1 at the usual 0.5
tuned_f1 = f1_score(yi_te, (imb_probs >= best_t).astype(int))  # F1 at the tuned threshold
print("\n--- Imbalanced data: F1-optimal threshold ---")
print(f"F1 at threshold 0.50 : {default_f1:.3f}")
print(f"Best threshold       : {best_t:.3f}")
print(f"F1 at best threshold : {tuned_f1:.3f}")
