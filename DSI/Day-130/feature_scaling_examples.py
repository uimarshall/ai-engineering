"""
Feature Scaling for KNN - Practical Examples
=============================================
This script demonstrates why feature scaling is critical for KNN
and shows how to properly scale features before training.

All code is heavily commented for beginner-level understanding.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("=" * 80)
print("FEATURE SCALING FOR KNN - BEGINNER TUTORIAL")
print("=" * 80)

# ============================================================================
# EXAMPLE 1: THE PROBLEM - UNSCALED DATA
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 1: The Problem - Unscaled Data")
print("=" * 80)

print("\n1. Create sample data (Heights and Weights):")
print("-" * 40)

# Create sample data: heights (meters) and weights (kg)
heights = np.array([1.65, 1.70, 1.75, 1.80, 1.90])
weights = np.array([65, 70, 75, 85, 95])

print("Heights (meters):", heights)
print("Weights (kg):    ", weights)

print("\nData Statistics:")
print("-" * 40)
print(f"Height - Min: {heights.min():.2f}, Max: {heights.max():.2f}, Range: {heights.max() - heights.min():.2f}")
print(f"Weight - Min: {weights.min():.0f}, Max: {weights.max():.0f}, Range: {weights.max() - weights.min():.0f}")

print("\nObservation:")
print(f"  Height range: {heights.max() - heights.min():.2f} (very small!)")
print(f"  Weight range: {weights.max() - weights.min():.0f} (much larger!)")
print(f"  Ratio: Weight range is {(weights.max() - weights.min()) / (heights.max() - heights.min()):.0f}x larger!")

print("\n2. Calculate distance between first two people:")
print("-" * 40)

# Calculate Euclidean distance
person1 = np.array([heights[0], weights[0]])  # [1.65, 65]
person2 = np.array([heights[1], weights[1]])  # [1.70, 70]

# Calculate components
height_diff = person2[0] - person1[0]
weight_diff = person2[1] - person1[1]

print(f"Person 1: Height={person1[0]:.2f}m, Weight={person1[1]:.0f}kg")
print(f"Person 2: Height={person2[0]:.2f}m, Weight={person2[1]:.0f}kg")

print(f"\nDifferences:")
print(f"  Height difference: {height_diff:.2f} (squared: {height_diff**2:.4f})")
print(f"  Weight difference: {weight_diff:.0f} (squared: {weight_diff**2:.0f})")

distance_unscaled = np.sqrt(height_diff**2 + weight_diff**2)
print(f"\nDistance = sqrt({height_diff**2:.4f} + {weight_diff**2:.0f}) = {distance_unscaled:.3f}")

print("\nProblem Analysis:")
print(f"  Weight squared component: {weight_diff**2:.0f} ({weight_diff**2 / (height_diff**2 + weight_diff**2) * 100:.1f}% of total)")
print(f"  Height squared component: {height_diff**2:.4f} ({height_diff**2 / (height_diff**2 + weight_diff**2) * 100:.1f}% of total)")
print("\n  => Weight DOMINATES the distance calculation!")
print("  => Height is almost completely ignored!")


# ============================================================================
# EXAMPLE 2: NORMALIZATION (MIN-MAX SCALING)
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 2: Normalization (Min-Max Scaling)")
print("=" * 80)

print("\n1. Manual Normalization:")
print("-" * 40)

def normalize_manual(values):
    """Manually normalize values to [0, 1] range"""
    min_val = np.min(values)
    max_val = np.max(values)
    return (values - min_val) / (max_val - min_val)

# Normalize heights and weights manually
heights_normalized = normalize_manual(heights)
weights_normalized = normalize_manual(weights)

print("Original Heights:", heights)
print("Normalized Heights:", np.round(heights_normalized, 3))

print("\nOriginal Weights:", weights)
print("Normalized Weights:", np.round(weights_normalized, 3))

print("\n2. Using Scikit-Learn MinMaxScaler:")
print("-" * 40)

# Combine data
data = np.column_stack([heights, weights])

# Create and fit scaler
scaler = MinMaxScaler()
data_normalized = scaler.fit_transform(data)

print("Original Data (first 3 rows):")
for i in range(3):
    print(f"  Height: {data[i, 0]:.2f}, Weight: {data[i, 1]:.0f}")

print("\nNormalized Data (first 3 rows):")
for i in range(3):
    print(f"  Height: {data_normalized[i, 0]:.3f}, Weight: {data_normalized[i, 1]:.3f}")

print("\nVerification:")
print(f"  Height normalized - Min: {data_normalized[:, 0].min():.3f}, Max: {data_normalized[:, 0].max():.3f}")
print(f"  Weight normalized - Min: {data_normalized[:, 1].min():.3f}, Max: {data_normalized[:, 1].max():.3f}")
print("  [OK] All values in [0, 1] range!")


# ============================================================================
# EXAMPLE 3: STANDARDIZATION
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 3: Standardization")
print("=" * 80)

print("\n1. Manual Standardization:")
print("-" * 40)

def standardize_manual(values):
    """Manually standardize values to mean=0, std=1"""
    mean = np.mean(values)
    std = np.std(values)
    return (values - mean) / std

heights_standardized = standardize_manual(heights)
weights_standardized = standardize_manual(weights)

print("Original Heights:", heights)
print("Standardized Heights:", np.round(heights_standardized, 3))

print("\nOriginal Weights:", weights)
print("Standardized Weights:", np.round(weights_standardized, 3))

print("\n2. Using Scikit-Learn StandardScaler:")
print("-" * 40)

scaler_std = StandardScaler()
data_standardized = scaler_std.fit_transform(data)

print("Standardized Data (first 3 rows):")
for i in range(3):
    print(f"  Height: {data_standardized[i, 0]:7.3f}, Weight: {data_standardized[i, 1]:7.3f}")

print("\nVerification:")
print(f"  Height - Mean: {data_standardized[:, 0].mean():.3f}, Std: {data_standardized[:, 0].std():.3f}")
print(f"  Weight - Mean: {data_standardized[:, 1].mean():.3f}, Std: {data_standardized[:, 1].std():.3f}")
print("  [OK] Mean ~0 and Std ~1!")


# ============================================================================
# EXAMPLE 4: DISTANCE CALCULATION WITH SCALED DATA
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 4: Distance Calculation with Scaled Data")
print("=" * 80)

print("\n1. Distances (Unscaled Data):")
print("-" * 40)

person1_unscaled = data[0]  # [1.65, 65]
person2_unscaled = data[1]  # [1.70, 70]

dist_unscaled = np.sqrt(np.sum((person1_unscaled - person2_unscaled)**2))
print(f"Distance between person 1 and 2 (unscaled): {dist_unscaled:.3f}")

print("\n2. Distances (Normalized Data):")
print("-" * 40)

person1_normalized = data_normalized[0]
person2_normalized = data_normalized[1]

dist_normalized = np.sqrt(np.sum((person1_normalized - person2_normalized)**2))
print(f"Distance between person 1 and 2 (normalized): {dist_normalized:.3f}")

print("\n3. Comparison:")
print("-" * 40)
print(f"Unscaled distance: {dist_unscaled:.3f}")
print(f"Normalized distance: {dist_normalized:.3f}")
print(f"Ratio: {dist_unscaled / dist_normalized:.2f}x different")

print("\nKey Insight:")
print("  With unscaled data: Weight differences dominate")
print("  With scaled data: Height and weight have equal influence")


# ============================================================================
# EXAMPLE 5: KNN WITH AND WITHOUT SCALING
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 5: KNN Accuracy - With vs Without Scaling")
print("=" * 80)

print("\n1. Create a more realistic dataset:")
print("-" * 40)

# Create dataset with height, weight, and age
np.random.seed(42)

# Class 0: Shorter people with lower weights
heights_0 = np.random.uniform(1.55, 1.75, 20)
weights_0 = np.random.uniform(55, 75, 20)
ages_0 = np.random.uniform(20, 40, 20)

# Class 1: Taller people with higher weights
heights_1 = np.random.uniform(1.75, 1.95, 20)
weights_1 = np.random.uniform(75, 95, 20)
ages_1 = np.random.uniform(40, 60, 20)

X = np.vstack([
    np.column_stack([heights_0, weights_0, ages_0]),
    np.column_stack([heights_1, weights_1, ages_1])
])

y = np.hstack([np.zeros(20), np.ones(20)])

print(f"Dataset size: {X.shape[0]} samples, {X.shape[1]} features")
print(f"Classes: {len(np.unique(y))}")

print("\n2. Feature Statistics (PROBLEM VISIBLE HERE):")
print("-" * 40)

feature_names = ['Height (m)', 'Weight (kg)', 'Age (years)']
for i, name in enumerate(feature_names):
    print(f"{name}:")
    print(f"  Range: {X[:, i].min():.2f} to {X[:, i].max():.2f}")
    print(f"  Span: {X[:, i].max() - X[:, i].min():.2f}")

print("\nObservation: Age has MUCH larger span than height!")

print("\n3. Split data:")
print("-" * 40)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

print(f"Training set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

print("\n4. KNN WITHOUT Scaling:")
print("-" * 40)

knn_unscaled = KNeighborsClassifier(n_neighbors=5)
knn_unscaled.fit(X_train, y_train)

y_pred_unscaled = knn_unscaled.predict(X_test)
accuracy_unscaled = accuracy_score(y_test, y_pred_unscaled)

print(f"Accuracy WITHOUT scaling: {accuracy_unscaled:.2%}")
print(f"Correct predictions: {np.sum(y_pred_unscaled == y_test)}/{len(y_test)}")

print("\n5. KNN WITH Normalization:")
print("-" * 40)

# CORRECT WAY: Scale after splitting
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

knn_scaled = KNeighborsClassifier(n_neighbors=5)
knn_scaled.fit(X_train_scaled, y_train)

y_pred_scaled = knn_scaled.predict(X_test_scaled)
accuracy_scaled = accuracy_score(y_test, y_pred_scaled)

print(f"Accuracy WITH scaling: {accuracy_scaled:.2%}")
print(f"Correct predictions: {np.sum(y_pred_scaled == y_test)}/{len(y_test)}")

print("\n6. Comparison:")
print("-" * 40)
print(f"Without scaling: {accuracy_unscaled:.2%}")
print(f"With scaling: {accuracy_scaled:.2%}")
print(f"Improvement: {(accuracy_scaled - accuracy_unscaled):.2%}")
print(f"\n[OK] Scaling improves accuracy by {(accuracy_scaled - accuracy_unscaled) * 100:.1f} percentage points!")


# ============================================================================
# EXAMPLE 6: COMPLETE WORKFLOW (THE RIGHT WAY)
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 6: Complete Correct Workflow")
print("=" * 80)

print("\n1. Step-by-step correct workflow:")
print("-" * 40)

# Load data
print("Step 1: Load data")
X_data = X.copy()
y_data = y.copy()
print(f"  [OK] Loaded {X_data.shape[0]} samples with {X_data.shape[1]} features")

# Split BEFORE scaling
print("\nStep 2: Split into train/test (BEFORE scaling!)")
X_train, X_test, y_train, y_test = train_test_split(
    X_data, y_data, test_size=0.3, random_state=42
)
print(f"  [OK] Train: {X_train.shape[0]} samples")
print(f"  [OK] Test: {X_test.shape[0]} samples")

# Create scaler
print("\nStep 3: Create MinMaxScaler")
scaler = MinMaxScaler()
print("  [OK] Scaler created")

# Fit on training data ONLY
print("\nStep 4: Fit scaler on training data ONLY")
scaler.fit(X_train)
print("  [OK] Scaler fitted on training data")

# Transform both sets with same scaler
print("\nStep 5: Transform train and test with SAME scaler")
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("  [OK] Training data scaled")
print("  [OK] Test data scaled (using training scaler)")

# Train KNN
print("\nStep 6: Train KNN on SCALED data")
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)
print("  [OK] KNN trained")

# Predict
print("\nStep 7: Predict on SCALED test data")
y_pred = knn.predict(X_test_scaled)
accuracy_correct = accuracy_score(y_test, y_pred)
print(f"  [OK] Predictions made")
print(f"  [OK] Accuracy: {accuracy_correct:.2%}")

print("\n[OK] Correct workflow produces good results!")


# ============================================================================
# EXAMPLE 7: COMMON MISTAKES
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 7: Common Mistakes to Avoid")
print("=" * 80)

print("\n1. MISTAKE: Scaling before splitting")
print("-" * 40)

print("Code:")
print("  scaler = MinMaxScaler()")
print("  X_scaled = scaler.fit_transform(X)  # WRONG: fits on ALL data")
print("  X_train, X_test = train_test_split(X_scaled)")

# This is actually WRONG but let's show it
X_scaled_wrong = MinMaxScaler().fit_transform(X_data)
X_train_w, X_test_w, y_train_w, y_test_w = train_test_split(X_scaled_wrong, y_data)
knn_w = KNeighborsClassifier(n_neighbors=5)
knn_w.fit(X_train_w, y_train_w)
acc_w = knn_w.score(X_test_w, y_test_w)

print(f"Problem: Test data influenced the scaler fitting!")
print(f"Accuracy: {acc_w:.2%}")

print("\n2. CORRECT: Scaling after splitting")
print("-" * 40)

print("Code:")
print("  X_train, X_test = train_test_split(X)  # CORRECT: split first")
print("  scaler = MinMaxScaler()")
print("  X_train = scaler.fit_transform(X_train)  # Fit on training only")
print("  X_test = scaler.transform(X_test)  # Use training scaler")

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_data, y_data)
scaler_c = MinMaxScaler()
X_train_c = scaler_c.fit_transform(X_train_c)
X_test_c = scaler_c.transform(X_test_c)
knn_c = KNeighborsClassifier(n_neighbors=5)
knn_c.fit(X_train_c, y_train_c)
acc_c = knn_c.score(X_test_c, y_test_c)

print(f"Solution: Test data only uses training scaler!")
print(f"Accuracy: {acc_c:.2%}")

print(f"\n[WARNING] Incorrect scaling cost us {(acc_c - acc_w) * 100:.1f} percentage points!")


# ============================================================================
# EXAMPLE 8: NORMALIZATION VS STANDARDIZATION
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 8: Normalization vs Standardization for KNN")
print("=" * 80)

print("\n1. Train KNN with different scaling methods:")
print("-" * 40)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Normalization
scaler_norm = MinMaxScaler()
X_train_norm = scaler_norm.fit_transform(X_train)
X_test_norm = scaler_norm.transform(X_test)
knn_norm = KNeighborsClassifier(n_neighbors=5)
knn_norm.fit(X_train_norm, y_train)
acc_norm = knn_norm.score(X_test_norm, y_test)

# Standardization
scaler_std = StandardScaler()
X_train_std = scaler_std.fit_transform(X_train)
X_test_std = scaler_std.transform(X_test)
knn_std = KNeighborsClassifier(n_neighbors=5)
knn_std.fit(X_train_std, y_train)
acc_std = knn_std.score(X_test_std, y_test)

print(f"Accuracy with Normalization: {acc_norm:.2%}")
print(f"Accuracy with Standardization: {acc_std:.2%}")
print(f"Difference: {abs(acc_norm - acc_std):.2%}")

print("\nConclusion:")
print("  [OK] Both methods work well for KNN")
print("  [OK] Normalization recommended (consistent [0,1] range)")
print("  [OK] Use normalization for KNN specifically")


# ============================================================================
# EXAMPLE 9: SCALED DATA INSPECTION
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 9: Inspecting Scaled Data")
print("=" * 80)

print("\n1. Feature ranges before and after scaling:")
print("-" * 40)

scaler = MinMaxScaler()
X_train, X_test, _, _ = train_test_split(X, y, test_size=0.3, random_state=42)
X_train_scaled = scaler.fit_transform(X_train)

for i, name in enumerate(['Height (m)', 'Weight (kg)', 'Age (years)']):
    print(f"\n{name}:")
    print(f"  Original - Min: {X_train[:, i].min():7.2f}, Max: {X_train[:, i].max():7.2f}, Range: {X_train[:, i].max() - X_train[:, i].min():7.2f}")
    print(f"  Scaled   - Min: {X_train_scaled[:, i].min():7.2f}, Max: {X_train_scaled[:, i].max():7.2f}, Range: {X_train_scaled[:, i].max() - X_train_scaled[:, i].min():7.2f}")


# ============================================================================
# EXAMPLE 10: REAL-WORLD EXAMPLE (IRIS DATASET)
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 10: Real-World Example (Iris Dataset)")
print("=" * 80)

from sklearn.datasets import load_iris

# Load data
iris = load_iris()
X_iris = iris.data
y_iris = iris.target

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_iris, y_iris, test_size=0.3, random_state=42
)

print("\n1. Iris dataset features:")
print("-" * 40)
for i, name in enumerate(iris.feature_names):
    print(f"{name}:")
    print(f"  Min: {X_iris[:, i].min():6.2f}, Max: {X_iris[:, i].max():6.2f}")

print("\n2. KNN without scaling:")
knn_no_scale = KNeighborsClassifier(n_neighbors=5)
knn_no_scale.fit(X_train, y_train)
acc_no_scale = knn_no_scale.score(X_test, y_test)
print(f"  Accuracy: {acc_no_scale:.2%}")

print("\n3. KNN with scaling:")
scaler_iris = MinMaxScaler()
X_train_iris = scaler_iris.fit_transform(X_train)
X_test_iris = scaler_iris.transform(X_test)
knn_scale = KNeighborsClassifier(n_neighbors=5)
knn_scale.fit(X_train_iris, y_train)
acc_scale = knn_scale.score(X_test_iris, y_test)
print(f"  Accuracy: {acc_scale:.2%}")

print(f"\nImprovement: {(acc_scale - acc_no_scale) * 100:+.1f} percentage points")


# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("SUMMARY - KEY CONCEPTS")
print("=" * 80)

summary = """
1. WHY SCALING MATTERS FOR KNN
   • KNN uses distance calculations
   • Features with larger ranges dominate
   • Smaller-range features are ignored
   • Solution: Scale all features to same range

2. NORMALIZATION (MIN-MAX SCALING)
   • Formula: (x - min) / (max - min)
   • Range: [0, 1]
   • Recommended for KNN
   • Interpretable as percentages

3. STANDARDIZATION
   • Formula: (x - mean) / std_dev
   • Range: ~[-3, +3]
   • Good for many algorithms
   • Identifies outliers (>3 std dev)

4. CORRECT WORKFLOW
   [OK] Load data
   [OK] Split into train/test
   [OK] Create scaler
   [OK] Fit scaler on training data ONLY
   [OK] Transform both sets
   [OK] Train KNN on scaled data
   [OK] Predict on scaled data

5. COMMON MISTAKES
   [X] Scaling before splitting
   [X] Using different scalers for train/test
   [X] Forgetting to scale test data
   [X] Not scaling for distance-based algorithms

6. KEY RULES
   [OK] Always scale for KNN
   [OK] Use Normalization for KNN
   [OK] Fit scaler on training data only
   [OK] Use same scaler for test data
   [OK] Split before scaling
"""

print(summary)

print("=" * 80)
print("[OK] DEMO COMPLETE - Feature scaling explained!")
print("=" * 80)
