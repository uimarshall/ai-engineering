"""
================================================================================
FINDING THE OPTIMAL K VALUE FOR KNN - BEGINNER TUTORIAL
================================================================================

This Python script demonstrates how to systematically find the best K value
for your KNN classification model. We'll explore different K values, visualize
their effects, and learn why some K values work better than others.

Author: ML Beginner Tutorial
Date: 2025
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris, load_digits, make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib to use non-interactive backend for Windows compatibility
plt.switch_backend('Agg')

print("="*80)
print("FINDING THE OPTIMAL K VALUE FOR KNN - BEGINNER TUTORIAL")
print("="*80)

# ==============================================================================
# EXAMPLE 1: Visualizing How K Affects Classification
# ==============================================================================
print("\n" + "="*80)
print("EXAMPLE 1: Understanding How K Affects Predictions")
print("="*80)

# Create a simple 2D dataset for visualization
np.random.seed(42)
print("\n1. Creating a simple 2-class dataset:")
print("-" * 40)

# Generate two clusters (two classes)
class_0 = np.random.randn(30, 2) + [2, 2]      # Class 0: cluster around (2, 2)
class_1 = np.random.randn(30, 2) + [8, 8]      # Class 1: cluster around (8, 8)
X_simple = np.vstack([class_0, class_1])       # Combine all points
y_simple = np.hstack([np.zeros(30), np.ones(30)])  # Class labels

print(f"  Class 0: 30 points around (2, 2)")
print(f"  Class 1: 30 points around (8, 8)")
print(f"  Total: {len(X_simple)} data points")

# Choose a new point to classify
new_point = np.array([[5, 5]])  # Point between the two clusters
print(f"\n2. New point to classify: {new_point[0]}")
print("-" * 40)

# Calculate distances to all points
print("\n3. Calculating distances to all training points:")
print("-" * 40)
distances = np.sqrt(np.sum((X_simple - new_point)**2, axis=1))
sorted_indices = np.argsort(distances)  # Get indices of nearest points
print(f"  Closest 1 neighbor: class {y_simple[sorted_indices[0]].astype(int)}")
print(f"  Closest 3 neighbors: {y_simple[sorted_indices[:3]].astype(int)} -> Class {int(np.round(np.mean(y_simple[sorted_indices[:3]])))}")
print(f"  Closest 5 neighbors: {y_simple[sorted_indices[:5]].astype(int)} -> Class {int(np.round(np.mean(y_simple[sorted_indices[:5]])))}")
print(f"  Closest 7 neighbors: {y_simple[sorted_indices[:7]].astype(int)} -> Class {int(np.round(np.mean(y_simple[sorted_indices[:7]])))}")

# Show how K=3 vs K=5 changes the prediction
print("\n4. Prediction comparison:")
print("-" * 40)
k3_neighbors = y_simple[sorted_indices[:3]]
k5_neighbors = y_simple[sorted_indices[:5]]
print(f"  With K=3: {np.sum(k3_neighbors == 0)} zeros, {np.sum(k3_neighbors == 1)} ones -> Predict Class {int(np.round(np.mean(k3_neighbors)))}")
print(f"  With K=5: {np.sum(k5_neighbors == 0)} zeros, {np.sum(k5_neighbors == 1)} ones -> Predict Class {int(np.round(np.mean(k5_neighbors)))}")
print("\n  Notice: K=3 and K=5 can give DIFFERENT predictions!")

# ==============================================================================
# EXAMPLE 2: Testing K Values Systematically
# ==============================================================================
print("\n" + "="*80)
print("EXAMPLE 2: Testing Different K Values Systematically")
print("="*80)

# Load the Iris dataset
print("\n1. Loading Iris dataset:")
print("-" * 40)
iris = load_iris()
X_iris = iris.data
y_iris = iris.target

# Scale the data (important for KNN!)
scaler = MinMaxScaler()
X_iris_scaled = scaler.fit_transform(X_iris)

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X_iris_scaled, y_iris, test_size=0.3, random_state=42
)

print(f"  Total samples: {len(X_iris)}")
print(f"  Number of features: {X_iris.shape[1]}")
print(f"  Number of classes: {len(np.unique(y_iris))}")
print(f"  Training samples: {len(X_train)}")
print(f"  Test samples: {len(X_test)}")

# Test different K values
print("\n2. Testing K values from 1 to 21:")
print("-" * 40)

k_values = range(1, 22)
train_accuracies = []
test_accuracies = []

print(f"{'K':>3} | {'Train Acc':>9} | {'Test Acc':>9} | {'Odd?':>4}")
print("-" * 40)

for k in k_values:
    # Create KNN model with this K
    knn = KNeighborsClassifier(n_neighbors=k)
    
    # Train on training data
    knn.fit(X_train, y_train)
    
    # Evaluate on both training and test data
    train_acc = knn.score(X_train, y_train)
    test_acc = knn.score(X_test, y_test)
    
    train_accuracies.append(train_acc)
    test_accuracies.append(test_acc)
    
    # Mark odd K values
    is_odd = "YES" if k % 2 == 1 else "NO"
    
    print(f"{k:3d} | {train_acc:9.1%} | {test_acc:9.1%} | {is_odd:>4}")

# ==============================================================================
# EXAMPLE 3: Finding the Optimal K
# ==============================================================================
print("\n" + "="*80)
print("EXAMPLE 3: Finding the Optimal K Value")
print("="*80)

# Find K with highest test accuracy
optimal_k = k_values[np.argmax(test_accuracies)]
optimal_accuracy = np.max(test_accuracies)

print(f"\n1. Optimal K value:")
print("-" * 40)
print(f"  Best K: {optimal_k}")
print(f"  Accuracy at K={optimal_k}: {optimal_accuracy:.1%}")

# Compare to other K values
print(f"\n2. Comparison to nearby K values:")
print("-" * 40)
for k in [optimal_k - 2, optimal_k - 1, optimal_k, optimal_k + 1, optimal_k + 2]:
    if 1 <= k <= 21:
        idx = k - 1
        acc = test_accuracies[idx]
        marker = " <-- BEST" if k == optimal_k else ""
        print(f"  K={k:2d}: {acc:.1%}{marker}")

# Verify K is odd
print(f"\n3. Verification:")
print("-" * 40)
if optimal_k % 2 == 1:
    print(f"  [OK] K={optimal_k} is odd (good for 2-3 classes)")
else:
    print(f"  [WARNING] K={optimal_k} is even (might cause ties)")

# ==============================================================================
# EXAMPLE 4: Cross-Validation Approach (More Robust)
# ==============================================================================
print("\n" + "="*80)
print("EXAMPLE 4: Using Cross-Validation for Robust K Selection")
print("="*80)

print("\n1. Testing K values with 5-fold cross-validation:")
print("-" * 40)

cv_scores = []
k_values_cv = range(1, 22)

print(f"{'K':>3} | {'CV Score':>9} | {'Std Dev':>8}")
print("-" * 40)

for k in k_values_cv:
    knn = KNeighborsClassifier(n_neighbors=k)
    # cross_val_score uses k-fold cross-validation (default k=5)
    scores = cross_val_score(knn, X_iris_scaled, y_iris, cv=5)
    cv_scores.append(scores.mean())
    print(f"{k:3d} | {scores.mean():9.1%} | {scores.std():8.4f}")

# Find best K from cross-validation
best_k_cv = list(k_values_cv)[np.argmax(cv_scores)]
best_cv_score = np.max(cv_scores)

print(f"\n2. Best K from cross-validation:")
print("-" * 40)
print(f"  Best K: {best_k_cv}")
print(f"  CV Accuracy: {best_cv_score:.1%}")

# ==============================================================================
# EXAMPLE 5: Handling Class Imbalance
# ==============================================================================
print("\n" + "="*80)
print("EXAMPLE 5: Choosing K with Imbalanced Classes")
print("="*80)

# Create imbalanced dataset (90% class 0, 10% class 1)
print("\n1. Creating imbalanced dataset:")
print("-" * 40)

X_imb, y_imb = make_classification(
    n_samples=100,
    n_features=5,
    n_informative=3,
    n_redundant=1,
    n_classes=2,
    weights=[0.9, 0.1],  # 90% class 0, 10% class 1
    random_state=42
)

# Scale data
scaler_imb = MinMaxScaler()
X_imb_scaled = scaler_imb.fit_transform(X_imb)

# Split
X_train_imb, X_test_imb, y_train_imb, y_test_imb = train_test_split(
    X_imb_scaled, y_imb, test_size=0.3, random_state=42
)

print(f"  Class 0 samples: {np.sum(y_imb == 0)} ({np.sum(y_imb == 0)/len(y_imb)*100:.0f}%)")
print(f"  Class 1 samples: {np.sum(y_imb == 1)} ({np.sum(y_imb == 1)/len(y_imb)*100:.0f}%)")

# Test K values on imbalanced data
print("\n2. Testing K values on imbalanced data:")
print("-" * 40)

imb_accuracies = []
imb_k_values = [1, 3, 5, 7, 9, 11, 15, 21]

print(f"{'K':>3} | {'Test Acc':>9} | {'Class 1 Recall':>15}")
print("-" * 40)

for k in imb_k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_imb, y_train_imb)
    
    # Accuracy
    acc = knn.score(X_test_imb, y_test_imb)
    imb_accuracies.append(acc)
    
    # Recall for minority class (class 1)
    y_pred = knn.predict(X_test_imb)
    cm = confusion_matrix(y_test_imb, y_pred)
    if len(cm) > 1:
        recall_class1 = cm[1, 1] / (cm[1, 0] + cm[1, 1]) if (cm[1, 0] + cm[1, 1]) > 0 else 0
    else:
        recall_class1 = 0
    
    print(f"{k:3d} | {acc:9.1%} | {recall_class1:15.1%}")

print("\n3. Key insight with imbalanced data:")
print("-" * 40)
print("  Smaller K values: Better at detecting minority class")
print("  Larger K values: Better overall accuracy (biased to majority)")
print("  Choose K=3-5 if minority class is important!")

# ==============================================================================
# EXAMPLE 6: Heuristic Approach (K = sqrt(n_samples))
# ==============================================================================
print("\n" + "="*80)
print("EXAMPLE 6: Using the Heuristic K = sqrt(n_samples)")
print("="*80)

print("\n1. Heuristic formula: K = sqrt(n_samples)")
print("-" * 40)

n_samples = len(X_train)
heuristic_k = int(np.sqrt(n_samples))

# Make it odd if even
if heuristic_k % 2 == 0:
    heuristic_k += 1

print(f"  Training samples: {n_samples}")
print(f"  Calculated K: sqrt({n_samples}) = {int(np.sqrt(n_samples))}")
print(f"  Rounded to odd: K = {heuristic_k}")

# Evaluate at heuristic K
knn_heuristic = KNeighborsClassifier(n_neighbors=heuristic_k)
knn_heuristic.fit(X_train, y_train)
heuristic_accuracy = knn_heuristic.score(X_test, y_test)

print(f"\n2. Performance at heuristic K:")
print("-" * 40)
print(f"  Accuracy at K={heuristic_k}: {heuristic_accuracy:.1%}")

# Compare to optimal K from earlier
print(f"\n3. Comparison:")
print("-" * 40)
print(f"  Heuristic K={heuristic_k}: {heuristic_accuracy:.1%}")
print(f"  Optimal K={optimal_k}: {optimal_accuracy:.1%}")
print(f"  Difference: {abs(optimal_accuracy - heuristic_accuracy):.1%}")
print(f"\n  Conclusion: Heuristic is a good starting point!")

# ==============================================================================
# EXAMPLE 7: Small Dataset Challenge
# ==============================================================================
print("\n" + "="*80)
print("EXAMPLE 7: Choosing K for Small Datasets")
print("="*80)

print("\n1. Creating small dataset:")
print("-" * 40)

X_small, y_small = make_classification(
    n_samples=20,  # Very small!
    n_features=4,
    n_informative=2,
    n_redundant=1,
    n_classes=2,
    random_state=42
)

X_train_small, X_test_small, y_train_small, y_test_small = train_test_split(
    X_small, y_small, test_size=0.3, random_state=42
)

print(f"  Total samples: {len(X_small)}")
print(f"  Training samples: {len(X_train_small)}")
print(f"  Test samples: {len(X_test_small)}")

# For small datasets, we can't use very large K
print(f"\n2. Maximum useful K for small datasets:")
print("-" * 40)
print(f"  Rule of thumb: K should be < n_training_samples / 2")
print(f"  Max K: {len(X_train_small) // 2}")

# Test smaller K values only
print(f"\n3. Testing K values for small dataset:")
print("-" * 40)

small_k_values = [1, 3, 5, 7]
print(f"{'K':>3} | {'Test Acc':>9}")
print("-" * 40)

for k in small_k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_small, y_train_small)
    acc = knn.score(X_test_small, y_test_small)
    print(f"{k:3d} | {acc:9.1%}")

print(f"\n4. Recommendation for small datasets:")
print("-" * 40)
print(f"  Use K = 3 or 5")
print(f"  Test both odd and even values if necessary")
print(f"  Use cross-validation instead of train/test split")

# ==============================================================================
# EXAMPLE 8: Complete Workflow
# ==============================================================================
print("\n" + "="*80)
print("EXAMPLE 8: Complete K Selection Workflow")
print("="*80)

print("\n1. Starting with Digits dataset (more complex than Iris):")
print("-" * 40)

digits = load_digits()
X_digits = digits.data
y_digits = digits.target

# Normalize
scaler_digits = MinMaxScaler()
X_digits_scaled = scaler_digits.fit_transform(X_digits)

# Split
X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(
    X_digits_scaled, y_digits, test_size=0.2, random_state=42
)

print(f"  Dataset: Handwritten digits (0-9)")
print(f"  Total samples: {len(X_digits)}")
print(f"  Features: {X_digits.shape[1]}")
print(f"  Classes: {len(np.unique(y_digits))}")

# Step 1: Calculate heuristic
print(f"\n2. Step 1: Calculate heuristic K")
print("-" * 40)
heuristic = int(np.sqrt(len(X_train_d)))
if heuristic % 2 == 0:
    heuristic += 1
print(f"  Heuristic: K = sqrt({len(X_train_d)}) = {int(np.sqrt(len(X_train_d)))} -> {heuristic} (odd)")

# Step 2: Test range around heuristic
print(f"\n3. Step 2: Test K values around heuristic")
print("-" * 40)

test_k_range = range(max(1, heuristic - 4), heuristic + 5, 2)  # ±4, odd only
print(f"  Testing K in range: {list(test_k_range)}")

print(f"\n{'K':>3} | {'Test Acc':>9}")
print("-" * 40)

best_k_digits = None
best_acc_digits = 0

for k in test_k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_d, y_train_d)
    acc = knn.score(X_test_d, y_test_d)
    print(f"{k:3d} | {acc:9.1%}")
    
    if acc > best_acc_digits:
        best_acc_digits = acc
        best_k_digits = k

# Step 3: Verify with cross-validation
print(f"\n4. Step 3: Verify best K with cross-validation")
print("-" * 40)

knn_final = KNeighborsClassifier(n_neighbors=best_k_digits)
cv_scores_final = cross_val_score(knn_final, X_digits_scaled, y_digits, cv=5)

print(f"  Best K from grid search: {best_k_digits}")
print(f"  Test accuracy: {best_acc_digits:.1%}")
print(f"  CV scores: {[f'{s:.1%}' for s in cv_scores_final]}")
print(f"  CV mean: {cv_scores_final.mean():.1%} (+/- {cv_scores_final.std():.3f})")

# Step 4: Summary
print(f"\n5. Step 4: Summary and Recommendation")
print("-" * 40)
print(f"  [OK] Selected K = {best_k_digits}")
print(f"  [OK] Is odd number: {best_k_digits % 2 == 1}")
print(f"  [OK] Test accuracy: {best_acc_digits:.1%}")
print(f"  [OK] Cross-validated: {cv_scores_final.mean():.1%}")
print(f"\n  Ready for production with K = {best_k_digits}")

# ==============================================================================
# EXAMPLE 9: Common Mistakes
# ==============================================================================
print("\n" + "="*80)
print("EXAMPLE 9: Common Mistakes to Avoid")
print("="*80)

# Mistake 1: Choosing K based on training data
print("\n1. MISTAKE: Evaluating K on training data")
print("-" * 40)

train_only_acc = []
for k in [1, 3, 5, 7, 11, 21]:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    acc = knn.score(X_train, y_train)  # WRONG! Using training data
    train_only_acc.append(acc)
    print(f"  K={k:2d}: Training accuracy = {acc:.1%}")

print(f"\n  [WARNING] If you pick based on training data,")
print(f"  you'd choose K=1 (perfect training accuracy)")
print(f"  But K=1 overfits and won't generalize!")

# Mistake 2: Using even K
print("\n2. MISTAKE: Using even K with binary classification")
print("-" * 40)

X_binary, y_binary = make_classification(
    n_samples=50, n_features=5, n_informative=3, n_redundant=1,
    n_classes=2, random_state=42
)
X_train_b, X_test_b, y_train_b, y_test_b = train_test_split(
    X_binary, y_binary, test_size=0.3, random_state=42
)

print(f"  Using K=4 (even) with 2 classes:")

# Manually simulate K=4
knn_4 = KNeighborsClassifier(n_neighbors=4)
knn_4.fit(X_train_b, y_train_b)
y_pred_4 = knn_4.predict(X_test_b[:3])
print(f"    Predictions: {y_pred_4}")

knn_3 = KNeighborsClassifier(n_neighbors=3)
knn_3.fit(X_train_b, y_train_b)
y_pred_3 = knn_3.predict(X_test_b[:3])
print(f"\n  Using K=3 (odd) with 2 classes:")
print(f"    Predictions: {y_pred_3}")
print(f"  [OK] Always use odd numbers!")

# Mistake 3: Not scaling data
print("\n3. MISTAKE: Not scaling before KNN")
print("-" * 40)

X_unscaled, y_unscaled = make_classification(
    n_samples=50,
    n_features=5,
    n_informative=3,
    n_redundant=1,
    n_classes=2,
    random_state=42
)

# Feature ranges are very different
feature_ranges = [(X_unscaled[:, i].min(), X_unscaled[:, i].max()) for i in range(4)]
print(f"  Feature ranges (unscaled):")
for i, (min_val, max_val) in enumerate(feature_ranges):
    range_val = max_val - min_val
    print(f"    Feature {i}: [{min_val:7.2f}, {max_val:7.2f}] range={range_val:7.2f}")

print(f"\n  [WARNING] Feature 0 range is ~100x larger!")
print(f"  [WARNING] KNN will ignore small-range features!")

X_train_u, X_test_u, y_train_u, y_test_u = train_test_split(
    X_unscaled, y_unscaled, test_size=0.3, random_state=42
)

# Without scaling
knn_no_scale = KNeighborsClassifier(n_neighbors=5)
knn_no_scale.fit(X_train_u, y_train_u)
acc_no_scale = knn_no_scale.score(X_test_u, y_test_u)

# With scaling
scaler_u = MinMaxScaler()
X_train_u_scaled = scaler_u.fit_transform(X_train_u)
X_test_u_scaled = scaler_u.transform(X_test_u)

knn_scaled = KNeighborsClassifier(n_neighbors=5)
knn_scaled.fit(X_train_u_scaled, y_train_u)
acc_scaled = knn_scaled.score(X_test_u_scaled, y_test_u)

print(f"\n  Accuracy without scaling: {acc_no_scale:.1%}")
print(f"  Accuracy with scaling: {acc_scaled:.1%}")
print(f"  Difference: {abs(acc_scaled - acc_no_scale):.1%}")
print(f"  [OK] Always scale for KNN!")

# ==============================================================================
# EXAMPLE 10: Summary and Best Practices
# ==============================================================================
print("\n" + "="*80)
print("EXAMPLE 10: Summary of K Selection Best Practices")
print("="*80)

print("\nCHECKLIST FOR CHOOSING K:")
print("-" * 80)

checklist = [
    ("Always use odd numbers", "Avoids ties in voting"),
    ("Start with heuristic", "K = sqrt(n_samples), rounded to odd"),
    ("Test a range", "Test K values like 3, 5, 7, 9, 11, 15, 21"),
    ("Use test set", "Never evaluate K on training data"),
    ("Plot accuracy vs K", "Find the peak of the curve"),
    ("Use cross-validation", "More robust than train/test split"),
    ("Check class distribution", "Small K if imbalanced classes"),
    ("Scale your data", "CRITICAL for distance-based algorithm"),
    ("Don't use K=1", "Too sensitive to noise/outliers"),
    ("Validate choice", "Re-check with new test data if possible"),
]

for i, (rule, reason) in enumerate(checklist, 1):
    print(f"  {i:2d}. [OK] {rule:30s} - {reason}")

print("\n" + "="*80)
print("OPTIMAL K SELECTION WORKFLOW:")
print("="*80)

workflow = """
  1. Load and explore data
     | Check sample count
     | Check feature count
     | Check class distribution

  2. Scale data (IMPORTANT!)
     | Use MinMaxScaler or StandardScaler

  3. Split train/test
     | 70% train, 30% test (or 80/20)

  4. Calculate heuristic K
     | K = sqrt(n_training_samples), round to odd

  5. Test range of K values
     | Start from K=1
     | Test odd numbers
     | Go up to ~21 or until underfitting obvious

  6. Plot results
     | X-axis: K values
     | Y-axis: Test accuracy
     | Find peak (optimal K)

  7. Verify with cross-validation
     | Use 5-fold CV
     | Confirm peak
     | Check standard deviation

  8. Use optimal K
     | Train final model on all data
     | Test on held-out validation set
     | Deploy with confidence!
"""

print(workflow)

print("="*80)
print("[OK] DEMO COMPLETE - Finding Optimal K Explained!")
print("="*80)
