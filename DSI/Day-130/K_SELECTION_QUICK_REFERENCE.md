# K Selection - Quick Reference Guide

## One-Line Summary
**K = odd number that maximizes cross-validation accuracy on test data**

---

## The Golden Rule
```
K = sqrt(n_training_samples)
Then test K-2, K, K+2
Pick the one with best cross-validation score
```

---

## Quick Decision Matrix

| Situation | Use This K | Why |
|-----------|-----------|-----|
| Small data (<100 samples) | 3-5 | Avoid overfitting |
| Medium data (100-1000) | 5-11 | Balance stability & sensitivity |
| Large data (>1000) | 7-15 or sqrt(n) | Smooth predictions |
| Imbalanced classes | 3-5 | Catch minority class |
| Very noisy data | 9-15 | Noise robustness |
| Clean data | 3-7 | Detect patterns |

---

## Must-Remember Rules

```
1. K MUST be ODD
   Bad:  K=2, K=4, K=6, K=8
   Good: K=1, K=3, K=5, K=7

2. NEVER use K=1
   K=1 overfits immediately

3. ALWAYS scale data first
   Use MinMaxScaler or StandardScaler

4. ALWAYS split BEFORE scaling
   Order: Split -> Scale -> Train

5. ALWAYS test on TEST set
   Not training set!

6. ALWAYS use cross-validation
   5-fold CV is standard
```

---

## Three-Line Code Template

```python
# Step 1: Try heuristic K
k_try = int(np.sqrt(len(X_train))) + 1  # Make odd

# Step 2: Grid search around it
best_k = find_best_k(X_train, y_train, k_try)

# Step 3: Use it
knn = KNeighborsClassifier(n_neighbors=best_k)
```

---

## Accuracy vs K Pattern

```
Accuracy
   |     /\
   |    /  \
   |   /    \    <- Peak (optimal K)
   |  /      \
   | /        \___
   |/              (too high K underfits)
   |_______________
   K: Small        Large
   (overfits)    (underfits)
```

---

## Quick Diagnostics

### High Accuracy = Good
- Celebrate! Your K works.

### K=1 gives best accuracy?
- Overfitting. Use K=3 or K=5 instead.

### Accuracy same for K=3-21?
- Dataset too simple or too easy.
- No significant improvement possible.

### Accuracy drops at high K?
- Normal! K=N_samples/2 is often too high.

### Minority class never predicted?
- Use smaller K (3-5).

---

## Formula Summary

### Heuristic K
```
K = sqrt(n_training_samples)
If even: K = K + 1
```

### Distance Calculation (Euclidean)
```
distance = sqrt((x1-x2)^2 + (y1-y2)^2 + ...)
```

### Normalization (before KNN)
```
x_normalized = (x - x_min) / (x_max - x_min)
Result: 0 <= x_normalized <= 1
```

### Cross-Validation
```
Average accuracy = mean of 5 folds
Standard deviation = how stable is this K
```

---

## Testing K - Pseudocode

```
1. For each K in [1, 3, 5, 7, 9, 11, 15, 21]:
   a) Create KNN with this K
   b) Run 5-fold cross-validation
   c) Record mean accuracy

2. Find K with highest mean accuracy

3. If std_deviation is high for this K:
   - Consider using slightly different K
   - Your choice might be unstable

4. Use this K in production
```

---

## Common K Values by Dataset

### Iris (150 samples, 3 classes, 4 features)
- sqrt(150) = 12 -> 11
- Optimal: Usually 3-7
- Why small? Easy dataset

### Digits (1797 samples, 10 classes, 64 features)
- sqrt(1797) = 42 -> 43
- Optimal: Usually 7-15
- Why medium? Harder dataset

### Titanic (800 samples, 2 classes)
- sqrt(800) = 28 -> 29
- Optimal: Usually 5-11
- Why medium? Binary classification

---

## Red Flags (Don't Do This!)

🚨 **Red Flag #1:** "K=1 gives perfect accuracy on training set"
- Problem: Severe overfitting
- Solution: Use cross-validation or test set

🚨 **Red Flag #2:** "All K values give 95% accuracy"
- Problem: Dataset too easy or features too predictive
- Solution: Check if problem is really just KNN

🚨 **Red Flag #3:** "My minority class is never predicted"
- Problem: K too large relative to minority class size
- Solution: Use K = 3 or 5

🚨 **Red Flag #4:** "Accuracy jumps around wildly for different K"
- Problem: Unstable model (small data or high noise)
- Solution: Use cross-validation, increase K slightly

🚨 **Red Flag #5:** "I chose K based on training accuracy"
- Problem: You'll overfit
- Solution: ALWAYS use test/CV accuracy

---

## Comparison: Train vs Test

| Metric | Train Accuracy | Test Accuracy |
|--------|---|---|
| Shows | How model memorized training data | How model generalizes |
| For choosing K? | **NEVER** | **YES** |
| K=1 | Usually 100% | Often 70-90% |
| K=opt | Usually 95-98% | Usually 95-98% |
| K=high | Usually 85-95% | Usually 85-95% |

**Rule:** If train >> test, you're overfitting. Increase K.

---

## Five Common Mistakes

### ❌ Mistake 1: Using K=1
```python
# WRONG
knn = KNeighborsClassifier(n_neighbors=1)

# BETTER
knn = KNeighborsClassifier(n_neighbors=5)
```

### ❌ Mistake 2: Even K with 2 classes
```python
# WRONG (can tie)
knn = KNeighborsClassifier(n_neighbors=4)

# RIGHT (no tie)
knn = KNeighborsClassifier(n_neighbors=5)
```

### ❌ Mistake 3: Choosing K from training data
```python
# WRONG - evaluates on training set
train_acc = knn.score(X_train, y_train)

# RIGHT - evaluates on test set
test_acc = knn.score(X_test, y_test)
```

### ❌ Mistake 4: Not scaling
```python
# WRONG - features have different ranges
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_unscaled, y)

# RIGHT - all features same range [0, 1]
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_train)
knn.fit(X_scaled, y)
```

### ❌ Mistake 5: Large K with few samples
```python
# WRONG - K=21 but only 30 training samples
knn = KNeighborsClassifier(n_neighbors=21)
knn.fit(X_train, y_train)  # X_train has 30 samples!

# RIGHT - K < n_samples / 2
knn = KNeighborsClassifier(n_neighbors=7)
```

---

## When to Revisit K Selection

- [ ] Got new data? Test K again
- [ ] Data distribution changed? Reselect K
- [ ] Different time period? Validate K
- [ ] Adding new features? Test new K
- [ ] Dropping outliers? Might change K

---

## Python Code Snippets

### Find Optimal K (Simple)
```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
import numpy as np

k_values = range(1, 20, 2)  # Odd numbers only
scores = []

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    score = cross_val_score(knn, X, y, cv=5).mean()
    scores.append(score)

best_k = list(k_values)[np.argmax(scores)]
print(f"Best K: {best_k} with accuracy {max(scores):.1%}")
```

### Using Optimal K
```python
knn = KNeighborsClassifier(n_neighbors=best_k)
knn.fit(X_train, y_train)
accuracy = knn.score(X_test, y_test)
predictions = knn.predict(X_new)
```

### With Grid Search (sklearn)
```python
from sklearn.model_selection import GridSearchCV

params = {'n_neighbors': [1, 3, 5, 7, 9, 11, 15]}
knn = KNeighborsClassifier()
grid = GridSearchCV(knn, params, cv=5)
grid.fit(X_train, y_train)

print(f"Best K: {grid.best_params_['n_neighbors']}")
print(f"Best CV score: {grid.best_score_:.1%}")
```

---

## Exam-Style Questions

**Q: Why use odd K for 2-class problem?**
A: Prevents ties when voting (e.g., K=4 gives 2-2 tie)

**Q: What's better: K=1 or K=21?**
A: Depends on data, but usually something in between. Test both.

**Q: Should I scale before splitting data?**
A: NO! Split first, then fit scaler on training set only.

**Q: Can I use K = sqrt(n_samples) always?**
A: It's a good starting point, but always test to verify.

**Q: What if I have 10 training samples?**
A: K should be 3-5. sqrt(10)=3.16->3 is fine.

---

## The Ultimate Checklist

Before using your K:
- [ ] K is odd number
- [ ] K < n_training_samples
- [ ] K not equal to 1
- [ ] Data was scaled
- [ ] Split before scaling
- [ ] Tested on test set (not training)
- [ ] Used cross-validation
- [ ] Considered class imbalance
- [ ] Plotted or viewed results
- [ ] Validated on new data

**Score 10/10?** Deploy with confidence! 🚀

---

## Key Takeaway

> Finding K is like tuning an instrument. Too tight (K too small) = harsh. Too loose (K too large) = muted. Just right = beautiful harmony. Test systematically!

**Time to find K:** Usually 5-15 minutes with automation. Worth it! ✨
