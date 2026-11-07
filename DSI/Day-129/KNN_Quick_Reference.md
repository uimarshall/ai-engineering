# KNN Quick Reference Guide

## One-Line Summary

**KNN:** Look at the K closest data points and use their category to predict.

---

## The Algorithm in 4 Steps

```
1. Calculate distance from new point to ALL training points
2. Find the K points with smallest distances
3. Count votes from those K points (majority rule)
4. Return the category that got the most votes
```

---

## Quick Code Template

### Basic Usage

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create and train
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# Predict
y_pred = knn.predict(X_test)

# Evaluate
accuracy = knn.score(X_test, y_test)
```

### With Scaling

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
```

### Find Best K

```python
from sklearn.model_selection import cross_val_score

best_k = None
best_score = 0

for k in range(1, 30, 2):
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X_train, y_train, cv=5)
    if scores.mean() > best_score:
        best_score = scores.mean()
        best_k = k
```

---

## Key Parameters

| Parameter         | Typical Value           | What It Does                               |
| ----------------- | ----------------------- | ------------------------------------------ |
| `n_neighbors` (K) | 3, 5, 7                 | Number of neighbors to check               |
| `weights`         | 'uniform' or 'distance' | How neighbors vote (equal or by closeness) |
| `metric`          | 'euclidean'             | How to measure distance                    |
| `p`               | 2                       | For Minkowski distance formula             |

---

## Choosing K

| K Value      | Pros                     | Cons                           |
| ------------ | ------------------------ | ------------------------------ |
| **1-3**      | Simple, captures details | Overfits, sensitive to noise   |
| **5-7**      | Balanced, good default   | May miss patterns              |
| **10+**      | Smooth, generalizes well | May oversmooth patterns        |
| **Too High** | Very stable              | Underfits, all same prediction |

**Rule of Thumb:** K = √(number of training samples), then adjust based on cross-validation.

---

## Pros and Cons Cheat Sheet

### ✅ Pros

- Super simple to understand
- No training phase (fast to deploy)
- Works for multi-class naturally
- No assumptions about data

### ❌ Cons

- Slow predictions (check all points)
- Memory hungry (stores all data)
- Sensitive to feature scaling
- Bad with high-dimensional data (many features)

---

## When to Use / Avoid

### ✓ Use KNN When:

- Dataset is small (< 10,000 samples)
- Few features (< 20)
- Need quick baseline
- Non-linear patterns
- Multi-class classification (3+ classes)

### ✗ Avoid KNN When:

- Dataset is huge (> 100,000 samples)
- Many features (> 50)
- Real-time predictions needed
- Class imbalance is severe
- Need interpretability

---

## Common Gotchas

| Mistake                  | Fix                         |
| ------------------------ | --------------------------- |
| Not scaling features     | Use StandardScaler()        |
| Using K=1                | Try K=3,5,7,9               |
| Using on high-dim data   | Use feature selection first |
| Testing on training data | Always use test set         |
| Imbalanced classes       | Use class_weight='balanced' |
| Too many features        | Remove irrelevant ones      |

---

## Distance Metrics

### Euclidean (most common)

- Straight-line distance
- √[(x₁-x₂)² + (y₁-y₂)²]
- Use for: continuous features

### Manhattan

- City-block distance
- |x₁-x₂| + |y₁-y₂|
- Use for: when coordinate independence matters

### Minkowski

- Generalized distance
- Can adjust with p parameter
- Use for: fine-tuning distances

---

## Comparison with Other Algorithms

| Algorithm           | Speed     | Accuracy  | Training | Best For                  |
| ------------------- | --------- | --------- | -------- | ------------------------- |
| KNN                 | Slow      | Good      | None     | Small datasets, baseline  |
| Decision Tree       | Fast      | Good      | Yes      | Interpretable, mixed data |
| Random Forest       | Fast      | Excellent | Yes      | Most cases                |
| Logistic Regression | Very Fast | Good      | Yes      | Linear, interpretable     |
| SVM                 | Medium    | Excellent | Yes      | High-dim data             |

---

## Evaluation Metrics

### Accuracy

```python
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)
# Percentage of correct predictions
```

### Precision & Recall

```python
from sklearn.metrics import precision_score, recall_score
precision = precision_score(y_test, y_pred)  # Avoid false alarms
recall = recall_score(y_test, y_pred)        # Catch all positives
```

### Confusion Matrix

```python
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
# Shows TP, TN, FP, FN
```

### Classification Report

```python
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))
# Shows precision, recall, f1 for each class
```

---

## Example Workflow

```python
# 1. Load data
from sklearn.datasets import load_iris
iris = load_iris()
X, y = iris.data, iris.target

# 2. Normalize
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = scaler.fit_transform(X)

# 3. Split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 4. Find best K
from sklearn.model_selection import cross_val_score
best_k = 5
for k in range(1, 20, 2):
    knn = KNeighborsClassifier(n_neighbors=k)
    if cross_val_score(knn, X_train, y_train, cv=5).mean() > 0.95:
        best_k = k
        break

# 5. Train
knn = KNeighborsClassifier(n_neighbors=best_k)
knn.fit(X_train, y_train)

# 6. Evaluate
from sklearn.metrics import accuracy_score, classification_report
y_pred = knn.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2%}")
print(classification_report(y_test, y_pred))

# 7. Predict new data
new_sample = [[5.1, 3.5, 1.4, 0.2]]
prediction = knn.predict(new_sample)
print(f"Prediction: {prediction}")
```

---

## Performance Tips

### Speed Up Predictions

- Use smaller K
- Reduce features via feature selection
- Use KD-Tree or Ball-Tree (leaf_size parameter)

### Improve Accuracy

- Try different K values
- Scale features
- Remove outliers
- Use distance weighting
- Feature engineering

### Handle Class Imbalance

- Use weights='distance'
- Oversample minority class
- Undersample majority class
- Use SMOTE

---

## When Results Are Bad

| Problem                            | Solution                                   |
| ---------------------------------- | ------------------------------------------ |
| Too low accuracy                   | Try different K, scale features, more data |
| Overfitting (train good, test bad) | Increase K, remove features                |
| Underfitting (both bad)            | Decrease K, add features                   |
| Slow predictions                   | Use feature selection, smaller K           |
| Memory issues                      | Use smaller dataset, feature selection     |

---

## Real-World Example: Movie Recommendation

```
Goal: Recommend movies to a user

Data: 1000 movies, 100,000 users
Features: Genre, Rating, Runtime, Year, Director, etc.

KNN Approach:
1. Find 5 users most similar to target user
2. See which movies they rated highly
3. Recommend those movies

Why KNN?
- Simple to implement
- Captures user taste naturally
- Works with mixed features
- Can use different similarity metrics
```

---

## Key Formulas

### Euclidean Distance

```
d = √[(x₁-x₂)² + (y₁-y₂)² + ... + (xₙ-xₙ)²]
```

### Prediction

```
Predicted Class = argmax(votes) where votes are from K nearest neighbors
```

### Accuracy

```
Accuracy = (# Correct Predictions) / (# Total Predictions)
```

### Precision

```
Precision = TP / (TP + FP)
TP = True Positives, FP = False Positives
```

### Recall

```
Recall = TP / (TP + FN)
FN = False Negatives
```

---

## Testing Your Understanding

Test yourself:

- [ ] Explain why KNN is "lazy learning"
- [ ] Why does feature scaling matter?
- [ ] How to choose K?
- [ ] When should you NOT use KNN?
- [ ] What's the difference between Euclidean and Manhattan distance?
- [ ] Why might K=1 give 100% training accuracy but bad test accuracy?
- [ ] How would you handle class imbalance with KNN?

---

## Further Learning

- Try different datasets (Iris, Digits, Wine, Breast Cancer)
- Experiment with distance metrics
- Implement KNN from scratch
- Use on your own data
- Compare with Decision Trees and Random Forests
- Learn advanced: KD-Trees, Ball-Trees for efficiency

---

## Quick Checklist Before Using KNN

- [ ] Dataset < 10,000 samples?
- [ ] Features < 20?
- [ ] Features scaled?
- [ ] Train/test split done?
- [ ] K value optimized via cross-validation?
- [ ] No severe class imbalance?
- [ ] Evaluation metrics chosen?
- [ ] Visualizations ready?

✓ If yes to all, KNN is a good choice!
