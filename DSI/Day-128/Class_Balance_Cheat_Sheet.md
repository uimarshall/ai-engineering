# Class Balance - Quick Reference & Code Templates

## The Problem in 30 Seconds

Your dataset has way more of one class than another (e.g., 95% "No", 5% "Yes").
Model learns to say "No" all the time → High accuracy but useless model.

---

## Quick Detection

```python
# Check class distribution
print(data['target'].value_counts())
# Output:
# 0    9900
# 1     100

# Calculate ratio
ratio = 9900 / 100  # 99:1 (severely imbalanced!)
```

**Thresholds:**
- 1:1 = Perfectly balanced
- 10:1 = Moderate imbalance
- 100:1 = Severe imbalance (FIX IT!)
- 1000:1 = Extreme imbalance (definitely FIX IT!)

---

## Solution 1: Random Oversampling

```python
from sklearn.utils import resample

# Get majority and minority classes
majority = data[data['target'] == 0]
minority = data[data['target'] == 1]

# Oversample minority
minority_oversampled = resample(minority,
                                n_samples=len(majority),
                                replace=True,  # Allow duplicates
                                random_state=42)

# Combine
balanced_data = pd.concat([majority, minority_oversampled])
```

**Pros:** Simple, keeps all data
**Cons:** Duplicates can cause overfitting

---

## Solution 2: Random Undersampling

```python
from sklearn.utils import resample

# Get majority and minority classes
majority = data[data['target'] == 0]
minority = data[data['target'] == 1]

# Undersample majority
majority_downsampled = resample(majority,
                                n_samples=len(minority),
                                replace=False,  # No duplicates
                                random_state=42)

# Combine
balanced_data = pd.concat([majority_downsampled, minority])
```

**Pros:** Faster training, simpler model
**Cons:** Lose information, smaller dataset

---

## Solution 3: SMOTE (Recommended)

```python
from imblearn.over_sampling import SMOTE

# Create SMOTE object
smote = SMOTE(random_state=42)

# Apply SMOTE
X_balanced, y_balanced = smote.fit_resample(X_train, y_train)

# Now balanced!
```

**Pros:** Creates synthetic samples (not duplicates), better generalization
**Cons:** Slower, more complex

---

## Solution 4: Class Weights (Simplest)

```python
from sklearn.ensemble import RandomForestClassifier

# Tell model which class is more important
model = RandomForestClassifier(class_weight='balanced', random_state=42)
model.fit(X_train, y_train)  # No resampling needed!
```

**Pros:** No data manipulation, simple
**Cons:** Not as effective as resampling

---

## Which Solution to Use?

| Dataset Size | Imbalance Ratio | Best Method |
|--------------|-----------------|-------------|
| Small | Any | Class weights |
| Medium | <10:1 | Class weights |
| Medium | 10-100:1 | SMOTE |
| Large | Any | Undersampling |
| Very Large | >100:1 | Combination |

---

## Complete Example: End-to-End

```python
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 1. Load data
data = pd.read_csv('data.csv')

# 2. Check imbalance
print(data['target'].value_counts())

# 3. Split data
X_train, X_test, y_train, y_test = train_test_split(
    data.drop('target', axis=1), data['target'],
    test_size=0.2, random_state=42
)

# 4. Fix imbalance on TRAINING data only
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

# 5. Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train_balanced, y_train_balanced)

# 6. Evaluate on original TEST data
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
```

---

## Common Mistakes

### [WRONG] Apply SMOTE on entire dataset
```python
# BAD! Data leakage
smote = SMOTE()
X_balanced, y_balanced = smote.fit_resample(X, y)  # WRONG
X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced)
```

### [CORRECT] Apply SMOTE only on training data
```python
# GOOD!
X_train, X_test, y_train, y_test = train_test_split(X, y)
smote = SMOTE()
X_train, y_train = smote.fit_resample(X_train, y_train)  # CORRECT
```

---

## Evaluation: Use Right Metrics

### [WRONG] Only accuracy
```python
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)  # BAD for imbalanced
```

### [CORRECT] Use balanced metrics
```python
from sklearn.metrics import precision_score, recall_score, f1_score
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
```

Or:
```python
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))
```

---

**Key Takeaway:** Always check class balance first. Use SMOTE for most cases, class weights for simplicity! ✓
