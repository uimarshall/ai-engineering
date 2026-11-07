# Confusion Matrix - Quick Reference & Code Templates

## The 4x2 Matrix in 30 Seconds

```
                Predicted YES   Predicted NO
Actually YES       TP (64)         FN (16)
Actually NO        FP (8)          TN (912)
```

- **TP (True Positive):** Correct "YES" → Good!
- **TN (True Negative):** Correct "NO" → Good!
- **FP (False Positive):** Wrong "YES" → False alarm
- **FN (False Negative):** Wrong "NO" → Missed it

---

## Quick Code: Generate Confusion Matrix

```python
from sklearn.metrics import confusion_matrix
import numpy as np

# Get predictions
y_pred = model.predict(X_test)

# Create matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

# Extract values
tn, fp, fn, tp = cm.ravel()
# or: tn = cm[0,0], fp = cm[0,1], fn = cm[1,0], tp = cm[1,1]
```

---

## Calculate All Metrics

```python
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

# Extract from matrix
tn, fp, fn, tp = cm.ravel()

# Manual calculation
accuracy = (tp + tn) / (tp + tn + fp + fn)
precision = tp / (tp + fp)          # When we say YES, how often right?
recall = tp / (tp + fn)             # How many actual YES did we catch?
specificity = tn / (tn + fp)        # How many actual NO did we catch?
f1 = 2 * (precision * recall) / (precision + recall)

# Or use sklearn (easier)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)
```

---

## Simple Example

**Dataset:** 1000 emails
- 950 are actually "Not Spam"
- 50 are actually "Spam"

**Model predicts:**
- 150 emails as Spam
- 850 emails as Not Spam

**Confusion Matrix:**

```
                Predicted Spam   Predicted Not Spam
Actually Spam         35                 15
Actually Not Spam    115                835
```

**Extract values:**
- TP = 35 (caught spam correctly)
- FN = 15 (missed spam)
- FP = 115 (false alarms - marked not spam as spam)
- TN = 835 (correctly allowed not spam)

**Calculate metrics:**
```python
accuracy = (35 + 835) / 1000 = 87.0%
precision = 35 / (35 + 115) = 23.3%  (only 23% of spam predictions are right!)
recall = 35 / (35 + 15) = 70%        (caught 70% of spam)
```

---

## Visualize Confusion Matrix

```python
import matplotlib.pyplot as plt
import seaborn as sns

cm = confusion_matrix(y_test, y_pred)

# Create heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['No', 'Yes'],
            yticklabels=['No', 'Yes'])
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title('Confusion Matrix')
plt.show()
```

---

## Get Full Report

```python
from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred))

# Output:
#           precision  recall  f1-score  support
#        0      0.88    0.99      0.93      950
#        1      0.23    0.70      0.35       50
# accuracy                       0.87     1000
```

---

## Choosing the Right Metric

### Focus on Precision
When **False Positives are costly**:
- Spam filter (don't mark legit as spam)
- Fraud detection (don't block legit transactions)

```python
print(f"Precision: {precision:.2%}")
# "Only X% of our alerts are correct"
```

### Focus on Recall
When **False Negatives are costly**:
- Disease detection (don't miss sick patients)
- Security (don't miss intruders)
- Quality control (don't ship defects)

```python
print(f"Recall: {recall:.2%}")
# "We catch X% of all actual positives"
```

### Focus on F1-Score
When **both errors matter equally**:
- Most balanced performance

```python
print(f"F1-Score: {f1:.2%}")
# "Overall balance of precision and recall"
```

### Focus on Accuracy
When **balanced dataset and both errors cost same**:
- Not recommended for imbalanced data!

```python
print(f"Accuracy: {accuracy:.2%}")
# "X% overall correct" - can be misleading!
```

---

## Common Mistakes

### [WRONG] Using accuracy on imbalanced data
```python
accuracy = (tp + tn) / (tp + tn + fp + fn)
# 99% looks good but you missed all positives!
```

### [CORRECT] Check precision AND recall
```python
print(f"Accuracy: {accuracy:.2%}")  # Overview
print(f"Precision: {precision:.2%}")  # How sure about YES predictions
print(f"Recall: {recall:.2%}")        # How many YES did we catch
```

### [WRONG] Ignoring off-diagonal elements
```
Matrix shows mostly diagonal? Good!
Matrix shows mostly off-diagonal? Bad!
```

### [CORRECT] Analyze the mistakes
```python
# Where does model fail?
print(f"False Positives: {fp} (saying YES when should be NO)")
print(f"False Negatives: {fn} (saying NO when should be YES)")
```

---

## Complete Example: End-to-End

```python
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Create data
X, y = make_classification(n_samples=1000, n_features=10,
                           weights=[0.8, 0.2], random_state=42)

# 2. Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 3. Train
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 4. Predict
y_pred = model.predict(X_test)

# 5. Get confusion matrix
cm = confusion_matrix(y_test, y_pred)

# 6. Print detailed report
print(classification_report(y_test, y_pred))

# 7. Visualize
sns.heatmap(cm, annot=True, fmt='d')
plt.show()

# 8. Extract metrics
tn, fp, fn, tp = cm.ravel()
print(f"TP: {tp}, TN: {tn}, FP: {fp}, FN: {fn}")
```

---

## Quick Decision Table

| You Care About | Use Metric | Interpretation |
|----------------|-----------|-----------------|
| Overall correctness | Accuracy | % of all predictions correct |
| Avoiding false alarms | Precision | % of YES predictions that are correct |
| Catching all positives | Recall | % of actual YES that we caught |
| Balanced approach | F1-Score | Harmonic mean of precision & recall |
| Specificity | TN / (TN + FP) | % of actual NO that we correctly identified |

---

**Key Takeaway:** Always look at the full confusion matrix! Accuracy alone is misleading. ✓
