# K-Nearest Neighbours (KNN) for Classification - Complete Tutorial

## Table of Contents

1. [What is KNN?](#what-is-knn)
2. [How KNN Works](#how-knn-works)
3. [Real-World Analogy](#real-world-analogy)
4. [Step-by-Step Explanation](#step-by-step-explanation)
5. [Python Implementation](#python-implementation)
6. [Practical Examples](#practical-examples)
7. [Choosing K](#choosing-k)
8. [Pros and Cons](#pros-and-cons)
9. [When to Use KNN](#when-to-use-knn)
10. [Best Practices](#best-practices)

---

## What is KNN?

**K-Nearest Neighbours (KNN)** is one of the simplest and most intuitive machine learning algorithms for classification.

**In Simple Terms:**
To predict what category something belongs to, KNN looks at the K closest examples it already knows about and uses their category as the prediction.

**K = Number of Neighbors**

- K is a number you choose (usually 3, 5, 7, etc.)
- The algorithm looks at the K closest neighbors
- It uses a vote from those neighbors to make a prediction

**Example:**
Imagine you're at a party and want to know if someone is a "sporty person" or "bookish person". You could look at the 5 people standing closest to them:

- If 4 of them are sporty and 1 is bookish → predict "sporty"
- If 3 are bookish and 2 are sporty → predict "bookish"

That's exactly how KNN works!

---

## How KNN Works

### The Basic Algorithm

```
1. Load training data (examples with known categories)
2. When you get a new point to classify:
   a. Calculate distance from new point to ALL training points
   b. Find the K closest points (smallest distances)
   c. Count votes from those K neighbors
   d. Assign the category that got the most votes
3. Return the prediction
```

### Distance Metrics

The most common way to measure "closeness" is **Euclidean Distance**:

```
Distance = √[(x₁ - x₂)² + (y₁ - y₂)² + ... + (xₙ - xₙ)²]
```

**In Plain English:**

- It's like measuring the straight-line distance between two points
- Larger distance = points are different
- Smaller distance = points are similar

---

## Real-World Analogy

### Movie Recommendation Example

Imagine Netflix wants to predict if YOU will like a movie:

1. **Netflix's Data:** They have 1,000 movies rated by 1,000,000 users
2. **Your Profile:** They know your age, the genres you like, your past ratings
3. **New Movie:** A new movie comes out. Will you like it?
4. **KNN Approach:**
   - Find 5 users most similar to you (by age, taste, etc.)
   - See what they rated the new movie
   - If 4 of them gave it 5 stars → Predict you'll like it
   - If 3 of them gave it 2 stars → Predict you won't like it

That's KNN in action!

---

## Step-by-Step Explanation

### Example: Classifying Iris Flowers

**Dataset:** We have measurements of 150 iris flowers in 3 species (Setosa, Versicolor, Virginica)

**Measurements (Features):**

- Sepal Length (cm)
- Sepal Width (cm)
- Petal Length (cm)
- Petal Width (cm)

**Goal:** Predict the species of a new iris flower based on its measurements

### Step 1: Training Phase (Loading the data)

```
Species       Sepal_L  Sepal_W  Petal_L  Petal_W
Setosa        5.1      3.5      1.4      0.2
Setosa        4.9      3.0      1.4      0.2
Versicolor    7.0      3.2      4.7      1.4
Versicolor    6.4      3.2      4.5      1.5
Virginica     7.1      3.0      5.9      2.1
Virginica     6.3      2.9      5.6      1.8
... (144 more flowers)
```

No "training" happens here! KNN just stores all the data.

### Step 2: New Flower Arrives

```
Unknown Iris:
  Sepal Length: 6.5 cm
  Sepal Width:  3.0 cm
  Petal Length: 5.5 cm
  Petal Width:  1.8 cm
  Species: ???
```

### Step 3: Calculate Distances to All Training Points

```
Distance to Setosa #1:     √[(6.5-5.1)² + (3.0-3.5)² + (5.5-1.4)² + (1.8-0.2)²] ≈ 4.1
Distance to Setosa #2:     √[(6.5-4.9)² + (3.0-3.0)² + (5.5-1.4)² + (1.8-0.2)²] ≈ 4.3
Distance to Versicolor #1: √[(6.5-7.0)² + (3.0-3.2)² + (5.5-4.7)² + (1.8-1.4)²] ≈ 0.9
Distance to Versicolor #2: √[(6.5-6.4)² + (3.0-3.2)² + (5.5-4.5)² + (1.8-1.5)²] ≈ 1.0
Distance to Virginica #1:  √[(6.5-7.1)² + (3.0-3.0)² + (5.5-5.9)² + (1.8-2.1)²] ≈ 0.7
Distance to Virginica #2:  √[(6.5-6.3)² + (3.0-2.9)² + (5.5-5.6)² + (1.8-1.8)²] ≈ 0.2
... (calculate for all 150)
```

### Step 4: Find K=5 Closest Neighbors (smallest distances)

```
Rank  Distance  Species
1     0.2       Virginica
2     0.7       Virginica
3     0.9       Versicolor
4     1.0       Versicolor
5     1.1       Virginica
```

### Step 5: Vote

```
Virginica:    3 votes (closest neighbors)
Versicolor:   2 votes
Setosa:       0 votes

PREDICTION: Virginica ✓
```

---

## Python Implementation

### Basic KNN from Scratch (Educational)

```python
import numpy as np
from collections import Counter

class SimpleKNN:
    """A basic KNN classifier to understand how it works"""

    def __init__(self, k=3):
        self.k = k
        self.X_train = None  # Training features
        self.y_train = None  # Training labels

    def fit(self, X, y):
        """Store training data (KNN doesn't really 'train')"""
        self.X_train = X
        self.y_train = y

    def distance(self, x1, x2):
        """Calculate Euclidean distance between two points"""
        return np.sqrt(np.sum((x1 - x2) ** 2))

    def predict(self, X):
        """Predict class for new data"""
        predictions = []

        for x in X:
            # Calculate distances to all training points
            distances = [self.distance(x, x_train) for x_train in self.X_train]

            # Find K nearest neighbors
            k_indices = np.argsort(distances)[:self.k]
            k_labels = self.y_train[k_indices]

            # Vote - find most common label
            most_common = Counter(k_labels).most_common(1)
            predictions.append(most_common[0][0])

        return np.array(predictions)
```

### Using Scikit-Learn (Practical)

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score

# Load data
iris = load_iris()
X = iris.data
y = iris.target

# Split into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create KNN classifier with K=5
knn = KNeighborsClassifier(n_neighbors=5)

# Train (KNN just stores the data)
knn.fit(X_train, y_train)

# Make predictions
y_pred = knn.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2%}")
```

---

## Practical Examples

### Example 1: Iris Flower Classification

**Problem:** Classify iris flowers into 3 species based on measurements

```python
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load the famous iris dataset
iris = load_iris()
X = iris.data  # Measurements: sepal/petal length and width
y = iris.target  # Species: 0=Setosa, 1=Versicolor, 2=Virginica

print("Dataset info:")
print(f"  Features: {iris.feature_names}")
print(f"  Species: {iris.target_names}")
print(f"  Samples: {X.shape[0]}")

# Split data (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create and train KNN
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# Make predictions
y_pred = knn.predict(X_test)

# Show results
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))
```

### Example 2: Predict a Single Flower

```python
# One unknown iris flower with measurements
new_flower = [[6.2, 2.9, 4.3, 1.3]]

# Predict its species
prediction = knn.predict(new_flower)
predicted_species = iris.target_names[prediction[0]]

print(f"\nNew flower measurements: {new_flower[0]}")
print(f"Predicted species: {predicted_species}")

# Also get the probability from K neighbors
distances, indices = knn.kneighbors(new_flower)
print(f"\nNearest {knn.n_neighbors} neighbors:")
for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
    print(f"  {i+1}. Distance: {dist:.2f} - {iris.target_names[y_train[idx]]}")
```

### Example 3: Testing Different Values of K

```python
import matplotlib.pyplot as plt

# Test accuracy with different K values
k_values = range(1, 21)
accuracies = []

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    accuracy = knn.score(X_test, y_test)
    accuracies.append(accuracy)
    print(f"K={k:2d}: Accuracy = {accuracy:.2%}")

# Find best K
best_k = k_values[accuracies.index(max(accuracies))]
print(f"\nBest K value: {best_k}")

# Plot results
plt.figure(figsize=(10, 5))
plt.plot(k_values, accuracies, marker='o')
plt.xlabel('K Value')
plt.ylabel('Accuracy')
plt.title('KNN Accuracy vs K Value')
plt.grid(True)
plt.show()
```

### Example 4: Simple Digit Recognition

```python
from sklearn.datasets import load_digits
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Load handwritten digits (0-9)
digits = load_digits()
X = digits.data  # 1797 images, 8x8 pixels each (64 features)
y = digits.target  # Labels: 0-9

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train KNN
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

# Test accuracy
accuracy = knn.score(X_test, y_test)
print(f"Digit Recognition Accuracy: {accuracy:.2%}")

# Predict a test digit
test_index = 0
test_image = X_test[test_index].reshape(8, 8)
test_label = y_test[test_index]
prediction = knn.predict([X_test[test_index]])[0]

print(f"\nActual digit: {test_label}")
print(f"Predicted digit: {prediction}")

# Show the digit
plt.figure(figsize=(4, 4))
plt.imshow(test_image, cmap='gray')
plt.title(f"Actual: {test_label}, Predicted: {prediction}")
plt.axis('off')
plt.show()
```

---

## Choosing K

### What Does K Mean?

| K Value    | Effect                           | Best For                  |
| ---------- | -------------------------------- | ------------------------- |
| K=1        | Only looks at 1 nearest neighbor | Can overfit; too specific |
| K=3        | Balanced approach                | Good starting point       |
| K=5        | More stable predictions          | Common choice             |
| K=7, 9, 11 | Smoother decision boundaries     | Larger datasets           |
| K=All      | Extremely biased                 | Never use                 |

### How to Choose K

**Rule of Thumb:**

- Start with K = √(number of samples)
- For 150 samples: √150 ≈ 12, so try K around 10-15
- Always try odd numbers to avoid ties

**Example:**

```python
import math

n_samples = 150
k_suggestion = int(math.sqrt(n_samples))
print(f"Dataset size: {n_samples}")
print(f"Suggested K: {k_suggestion}")

# Try range around suggestion
for k in range(max(1, k_suggestion-2), k_suggestion+3):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    score = knn.score(X_test, y_test)
    print(f"K={k}: {score:.2%}")
```

### Finding Optimal K

```python
from sklearn.model_selection import cross_val_score

# Test multiple K values using cross-validation
k_range = range(1, 30, 2)  # Test odd numbers from 1 to 29
cv_scores = []

for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X_train, y_train, cv=5)
    cv_scores.append(scores.mean())
    print(f"K={k:2d}: CV Score = {scores.mean():.3f}")

# Find best K
best_k = list(k_range)[cv_scores.index(max(cv_scores))]
print(f"\nBest K: {best_k}")
```

---

## Pros and Cons

### ✅ Advantages of KNN

| Advantage                     | Explanation                                        |
| ----------------------------- | -------------------------------------------------- |
| **Simple to understand**      | No complex math, just distance & voting            |
| **No training phase**         | Stores data and predicts immediately               |
| **Works for multi-class**     | Can handle 2, 3, 10+ classes easily                |
| **Non-parametric**            | Makes no assumptions about data distribution       |
| **Good baseline**             | Great starting algorithm to compare others against |
| **Flexible distance metrics** | Can use different distance measurements            |
| **Lazy learning**             | All the work happens at prediction time            |

### ❌ Disadvantages of KNN

| Disadvantage                | Explanation                                             |
| --------------------------- | ------------------------------------------------------- |
| **Slow predictions**        | Must calculate distance to ALL training points          |
| **Memory hungry**           | Stores entire training dataset in memory                |
| **Sensitive to scaling**    | Features must be normalized (1 unit difference matters) |
| **Curse of dimensionality** | Doesn't work well with many features (100+)             |
| **K selection**             | Need to manually choose K value                         |
| **Imbalanced data**         | Majority class can dominate predictions                 |
| **Noisy data**              | Outliers and errors affect predictions                  |

---

## When to Use KNN

### ✓ Good Use Cases

1. **Small to Medium Datasets** (< 10,000 samples)
   - Example: Iris flowers (150 samples)
2. **Few Features** (< 20 features)
   - Example: Age, Income, Years Experience (good for KNN)
   - Example: 1000+ features (bad for KNN)

3. **Non-Linear Problems**
   - Datasets where classes aren't separable by straight lines
   - Example: Spiral patterns, complex boundaries

4. **Multi-class Classification**
   - 3+ classes to predict
   - Example: Plant species (3), Digit recognition (10), Animal types (50)

5. **Quick Prototyping**
   - Need fast results to test an idea
   - Use as baseline before complex algorithms

6. **Recommendation Systems**
   - Finding similar users or items
   - Example: Netflix recommending movies

### ✗ Poor Use Cases

1. **Large Datasets** (> 100,000 samples)
   - Predictions become very slow
   - Use other algorithms instead

2. **High-Dimensional Data** (> 50 features)
   - All points become equally distant (curse of dimensionality)
   - Example: Image pixels (10,000+ features) - use deep learning

3. **Real-Time Requirements**
   - Need predictions in milliseconds
   - KNN is too slow

4. **Highly Imbalanced Data**
   - Majority class always wins
   - Would need special handling (weights, oversampling)

5. **When Features Are Categorical**
   - Distance metrics don't work well
   - Better to use Decision Trees or Random Forests

---

## Best Practices

### 1. Normalize/Scale Your Features

**Why:** Features with different ranges affect distance calculation

```python
from sklearn.preprocessing import StandardScaler

# Without scaling (BAD)
# Feature 1: Age (0-100)
# Feature 2: Income (0-1,000,000)
# Income dominates the distance calculation!

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)
```

### 2. Always Split Data

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### 3. Use Cross-Validation to Find Best K

```python
from sklearn.model_selection import cross_val_score

best_score = 0
best_k = 1

for k in range(1, 30, 2):
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X_train, y_train, cv=5)
    if scores.mean() > best_score:
        best_score = scores.mean()
        best_k = k

print(f"Best K: {best_k} (CV Score: {best_score:.3f})")
```

### 4. Handle Class Imbalance

```python
# If dataset has many more of one class
knn = KNeighborsClassifier(
    n_neighbors=5,
    weights='distance'  # Closer neighbors vote more
)
```

### 5. Remove Irrelevant Features

```python
# KNN with many irrelevant features performs poorly
# Use feature selection first

from sklearn.feature_selection import SelectKBest, f_classif

selector = SelectKBest(f_classif, k=4)  # Keep only 4 best features
X_train_selected = selector.fit_transform(X_train, y_train)
X_test_selected = selector.transform(X_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_selected, y_train)
```

### 6. Use Distance Weighting

```python
# Make closer neighbors vote more strongly

knn = KNeighborsClassifier(
    n_neighbors=5,
    weights='distance'  # Closer = stronger vote
)

# vs

knn = KNeighborsClassifier(
    n_neighbors=5,
    weights='uniform'  # All votes equal (default)
)
```

### 7. Try Different Distance Metrics

```python
# Euclidean (default) - straight-line distance
knn_euclidean = KNeighborsClassifier(
    n_neighbors=5,
    metric='euclidean'
)

# Manhattan - city-block distance (sum of absolute differences)
knn_manhattan = KNeighborsClassifier(
    n_neighbors=5,
    metric='manhattan'
)

# Minkowski - generalized distance
knn_minkowski = KNeighborsClassifier(
    n_neighbors=5,
    metric='minkowski'
)
```

---

## Summary Comparison

### KNN vs Other Algorithms

| Algorithm               | Speed        | Accuracy  | Complexity   | Best For                          |
| ----------------------- | ------------ | --------- | ------------ | --------------------------------- |
| **KNN**                 | Slow predict | Good      | Simple       | Small datasets, baseline          |
| **Decision Tree**       | Fast         | Good      | Simple       | Interpretability, mixed features  |
| **Random Forest**       | Fast         | Excellent | Medium       | Most general problems             |
| **Logistic Regression** | Very Fast    | Good      | Simple       | Linear problems, interpretability |
| **SVM**                 | Medium       | Excellent | Complex      | High-dimensional data             |
| **Neural Networks**     | Medium       | Excellent | Very Complex | Complex patterns, images          |

---

## Complete Workflow Example

```python
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load data
iris = load_iris()
X, y = iris.data, iris.target

# 2. Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# 4. Find best K
best_k = 5
for k in range(3, 11, 2):
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X_train, y_train, cv=5)
    print(f"K={k}: {scores.mean():.3f}")

# 5. Train best model
knn = KNeighborsClassifier(n_neighbors=best_k)
knn.fit(X_train, y_train)

# 6. Evaluate
y_pred = knn.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.2%}")

# 7. Detailed report
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# 8. Confusion matrix visualization
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('KNN Confusion Matrix')
plt.show()
```

---

## Key Takeaways

1. **KNN is Simple:** Look at K nearest points and vote
2. **No Real Training:** Just stores the data
3. **Choose K Carefully:** Use cross-validation to find best value
4. **Normalize Features:** Different scales confuse distance metrics
5. **Works Best:** Small datasets (< 10K), few features (< 20)
6. **Avoid When:** High-dimensional data, real-time predictions needed
7. **Good For:** Baseline model, recommendation systems, multi-class problems

---

## Common Mistakes to Avoid

❌ **Not normalizing features**

- Features with different scales dominate distance calculations

❌ **Using K that's too small**

- K=1 overfits; noise affects predictions too much

❌ **Using K that's too large**

- K=100 underfits; averaging out all nuances

❌ **Not splitting data**

- Testing on training data gives fake high accuracy

❌ **Keeping all features**

- Irrelevant features add noise, slow predictions

❌ **Using on large datasets**

- Predictions become very slow (O(n) complexity)

❌ **Ignoring class imbalance**

- Majority class always wins in voting

---

## Resources for Further Learning

- **Scikit-Learn KNN Documentation:** https://scikit-learn.org/stable/modules/neighbors.html
- **Distance Metrics:** Euclidean, Manhattan, Minkowski, Cosine
- **Advanced Topics:** KD-Trees for faster search, Ball Trees
- **Applications:** Recommendation systems, image recognition, medical diagnosis

---

**Next Steps:**

1. Run the `knn_classification_demo.py` file
2. Try different K values and observe changes
3. Apply KNN to your own dataset
4. Compare with other algorithms
5. Explore distance metrics and weighting strategies

Happy Learning! 🚀
