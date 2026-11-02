"""Evaluating classification accuracy (confusion matrix) - practical demo.

Run:  python evaluating_classification_accuracy_demo.py
Needs: numpy, scikit-learn, matplotlib
"""

import numpy as np  # numerical arrays
import matplotlib.pyplot as plt  # plotting
from sklearn.linear_model import LogisticRegression  # the classifier
from sklearn.model_selection import train_test_split  # honest train/test split
from sklearn.metrics import (  # evaluation tools
    confusion_matrix,
    accuracy_score,
    ConfusionMatrixDisplay,
)

# ---------------------------------------------------------------------------
# 1. Data approximated from the slides: 12 students passed, 11 failed (23 total)
# ---------------------------------------------------------------------------
passed = np.array([1.5, 2.6, 4.0, 4.3, 5.3, 5.75, 6.1, 6.45, 6.7, 7.0, 8.0, 8.25])
failed = np.array([0.1, 0.35, 0.65, 1.0, 1.4, 1.75, 2.15, 2.7, 3.0, 3.6, 5.5])
X = np.concatenate([passed, failed]).reshape(-1, 1)  # sklearn needs a 2-D feature matrix
y = np.concatenate([np.ones(len(passed)), np.zeros(len(failed))]).astype(int)  # 1=pass, 0=fail

# ---------------------------------------------------------------------------
# 2. Fit the model and turn probabilities into class predictions
# ---------------------------------------------------------------------------
model = LogisticRegression(C=np.inf)  # no regularisation (plain maximum likelihood)
model.fit(X, y)  # learn intercept and slope

probs = model.predict_proba(X)[:, 1]  # probability of passing for each student
print("P(pass) after 4 hours of study:", round(model.predict_proba([[4.0]])[0, 1], 2))
print("P(pass) after 6 hours of study:", round(model.predict_proba([[6.0]])[0, 1], 2))

threshold = 0.5  # the "line in the sand"
y_pred = (probs >= threshold).astype(int)  # above threshold -> predict pass (1)

# ---------------------------------------------------------------------------
# 3. Confusion matrix. sklearn layout: rows = ACTUAL, columns = PREDICTED
#    with class order [0, 1] -> [[TN, FP], [FN, TP]]
# ---------------------------------------------------------------------------
cm = confusion_matrix(y, y_pred)  # 2x2 table of counts
tn, fp, fn, tp = cm.ravel()  # unpack the four cells
print("\nConfusion matrix (rows=actual [fail, pass], cols=predicted [fail, pass]):")
print(cm)
print(f"TP={tp} (predicted pass, did pass)")
print(f"TN={tn} (predicted fail, did fail)")
print(f"FP={fp} (predicted pass, actually failed)  -> Type I error")
print(f"FN={fn} (predicted fail, actually passed)  -> Type II error")

# ---------------------------------------------------------------------------
# 4. Accuracy = correct predictions / all predictions
# ---------------------------------------------------------------------------
accuracy_manual = (tp + tn) / (tp + tn + fp + fn)  # by hand from the matrix
accuracy_sklearn = accuracy_score(y, y_pred)  # same thing via sklearn
print(f"\nAccuracy (manual)  : {tp + tn}/{len(y)} = {accuracy_manual:.0%}")
print(f"Accuracy (sklearn) : {accuracy_sklearn:.0%}")

# ---------------------------------------------------------------------------
# 5. Reproduce the slide's numbers exactly: TP=8, FN=4, FP=1, TN=10
# ---------------------------------------------------------------------------
slide_cm = np.array([[10, 1], [4, 8]])  # [[TN, FP], [FN, TP]]
slide_acc = np.trace(slide_cm) / slide_cm.sum()  # diagonal = correct predictions
print(f"\nSlide example: correct={np.trace(slide_cm)}, total={slide_cm.sum()}, "
      f"accuracy={slide_acc:.0%}")  # 18/23 = 78%

# ---------------------------------------------------------------------------
# 6. Training accuracy is optimistic - evaluate on held-out test data too
# ---------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y  # keep pass/fail ratio in both parts
)
test_model = LogisticRegression(C=np.inf).fit(X_train, y_train)  # train on training part only
print(f"\nTrain accuracy: {test_model.score(X_train, y_train):.0%}")  # score() = accuracy
print(f"Test accuracy : {test_model.score(X_test, y_test):.0%}  (small data -> noisy!)")

# ---------------------------------------------------------------------------
# 7. Effect of the threshold on the errors
# ---------------------------------------------------------------------------
print("\nThreshold  FP  FN  Accuracy")
for t in (0.3, 0.5, 0.7):
    pred_t = (probs >= t).astype(int)  # re-classify with a different cut-off
    tn_t, fp_t, fn_t, tp_t = confusion_matrix(y, pred_t).ravel()
    print(f"   {t:.1f}     {fp_t:2d}  {fn_t:2d}   {accuracy_score(y, pred_t):.0%}")

# ---------------------------------------------------------------------------
# 8. Multi-class: 3x3 confusion matrix from the insurance slide
#    (rows = predicted on the slide, columns = actual)
# ---------------------------------------------------------------------------
labels = ["High Risk", "Medium Risk", "Low Risk"]
multi = np.array([[94, 16, 22], [12, 76, 8], [28, 22, 61]])  # slide values
multi_acc = np.trace(multi) / multi.sum()  # diagonal / total
print(f"\n3-class accuracy: {np.trace(multi)}/{multi.sum()} = {multi_acc:.0%}")

# ---------------------------------------------------------------------------
# 9. Plot both confusion matrices
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))  # two panels
ConfusionMatrixDisplay(cm, display_labels=["Fail", "Pass"]).plot(ax=axes[0], cmap="Blues")
axes[0].set_title("Our model (rows=actual, cols=predicted)")
ConfusionMatrixDisplay(multi, display_labels=labels).plot(ax=axes[1], cmap="Greens")
axes[1].set_title("3-class insurance example (rows=predicted)")
plt.tight_layout()
plt.savefig("confusion_matrices.png", dpi=120)  # save next to the script
print("Saved confusion_matrices.png")
