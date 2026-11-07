"""
K-Nearest Neighbours (KNN) for Classification - Complete Working Demo
=====================================================================
This script demonstrates KNN classification with multiple examples and visualizations.
"""

import matplotlib  # Set backend before importing pyplot
import numpy as np  # For numerical operations
import pandas as pd  # For data manipulation

matplotlib.use("Agg")  # Use non-interactive backend (doesn't show plots)
from collections import Counter  # For counting votes in manual KNN
from typing import cast

import matplotlib.pyplot as plt  # For creating visualizations
import seaborn as sns  # For enhanced visualizations
from sklearn.datasets import load_digits, load_iris  # Load sample datasets
from sklearn.metrics import (  # For evaluating model performance
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
)
from sklearn.model_selection import (  # For data splitting and validation
    cross_val_score,
    train_test_split,
)
from sklearn.neighbors import KNeighborsClassifier  # The KNN classifier
from sklearn.preprocessing import StandardScaler  # For feature scaling
from sklearn.utils import Bunch

# Set random seed for reproducibility (ensures same results each run)
np.random.seed(42)

# ============================================================================
# SECTION 1: SIMPLE KNN IMPLEMENTATION FROM SCRATCH
# ============================================================================

print("=" * 80)
print("SECTION 1: K-NEAREST NEIGHBOURS FROM SCRATCH (Educational)")
print("=" * 80)


class SimpleKNN:
    """
    A basic KNN classifier implementation from scratch to understand how it works.
    This shows the core logic behind the algorithm.
    """

    def __init__(self, k=3):
        """
        Initialize KNN with K parameter.

        Args:
            k (int): Number of neighbors to consider (default 3)
        """
        self.k = k  # Store the K value
        self.X_train = None  # Will store training features
        self.y_train = None  # Will store training labels

    def fit(self, X, y):
        """
        Store training data. KNN doesn't actually "train" - it just memorizes.

        Args:
            X: Training features (numpy array of shape [n_samples, n_features])
            y: Training labels (numpy array of shape [n_samples])
        """
        self.X_train = X  # Store features
        self.y_train = y  # Store labels
        print(f"[OK] KNN fitted with {len(X)} training samples and K={self.k}")

    def euclidean_distance(self, x1, x2):
        """
        Calculate Euclidean distance between two points.
        Formula: sqrt((x1[0]-x2[0])^2 + (x1[1]-x2[1])^2 + ... + (x1[n]-x2[n])^2)

        Args:
            x1, x2: Two data points (numpy arrays)

        Returns:
            Distance (float): How different the two points are
        """
        # Calculate squared differences and sum them
        squared_diff = (x1 - x2) ** 2
        # Take the square root of the sum
        distance = np.sqrt(np.sum(squared_diff))
        return distance

    def predict(self, X):
        """
        Predict class labels for new data.
        For each new point:
        1. Calculate distance to all training points
        2. Find K nearest neighbors
        3. Vote on the most common class

        Args:
            X: New data to predict (shape [n_samples, n_features])

        Returns:
            predictions: Predicted class labels (numpy array)
        """
        X_train = self.X_train
        y_train = self.y_train
        if X_train is None or y_train is None:
            raise RuntimeError("The KNN classifier must be fitted before prediction.")

        predictions = []  # Store predictions for each point

        # For each new data point
        for x in X:
            # Step 1: Calculate distances to ALL training points
            distances = [self.euclidean_distance(x, x_train) for x_train in X_train]

            # Step 2: Find indices of K nearest neighbors (smallest distances)
            # argsort returns indices that would sort the array
            # [:self.k] gets the first K (smallest distance) indices
            k_indices = np.argsort(np.array(distances))[: self.k]

            # Get the labels of these K neighbors
            k_labels = y_train[k_indices]

            # Step 3: Vote - find most common label
            # Counter counts occurrences, most_common(1) gets the most frequent
            most_common = Counter(k_labels.tolist()).most_common(1)

            # The prediction is the label with most votes
            prediction = most_common[0][0]
            predictions.append(prediction)

        # Return all predictions as numpy array
        return np.array(predictions)


# Test our custom KNN implementation
print("\n1. Testing Custom KNN Implementation:")
print("-" * 40)

# Load iris dataset
iris = cast(Bunch, load_iris())
X_iris = iris.data  # Features: sepal/petal measurements
y_iris = iris.target  # Labels: species (0, 1, 2)

# Split data into training and testing (80/20 split)
X_train_custom, X_test_custom, y_train_custom, y_test_custom = train_test_split(
    X_iris, y_iris, test_size=0.2, random_state=42
)

# Create and train our custom KNN
my_knn = SimpleKNN(k=5)
my_knn.fit(X_train_custom, y_train_custom)

# Make predictions
y_pred_custom = my_knn.predict(X_test_custom)

# Calculate accuracy (percentage of correct predictions)
accuracy_custom = accuracy_score(y_test_custom, y_pred_custom)
print(f"[OK] Custom KNN Accuracy: {accuracy_custom:.2%}")
print(
    f"[OK] Correct predictions: {np.sum(y_pred_custom == y_test_custom)}/{len(y_test_custom)}"
)


# ============================================================================
# SECTION 2: USING SCIKIT-LEARN KNN (Practical)
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 2: SCIKIT-LEARN KNN (Production Ready)")
print("=" * 80)

print("\n1. Basic Iris Classification:")
print("-" * 40)

# Create KNN classifier with K=5 neighbors
knn_iris = KNeighborsClassifier(n_neighbors=5)

# Train on training data (actually just stores the data)
knn_iris.fit(X_train_custom, y_train_custom)

# Make predictions
y_pred_iris = knn_iris.predict(X_test_custom)

# Evaluate accuracy
accuracy_iris = accuracy_score(y_test_custom, y_pred_iris)
print(f"Iris Dataset - KNN Accuracy: {accuracy_iris:.2%}")

# Show detailed classification report
print("\nDetailed Classification Report:")
print(classification_report(y_test_custom, y_pred_iris, target_names=iris.target_names))


# ============================================================================
# SECTION 3: FINDING OPTIMAL K VALUE
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 3: FINDING THE OPTIMAL K VALUE")
print("=" * 80)

print("\n1. Testing Different K Values (1 to 20):")
print("-" * 40)

# Test different K values and store accuracies
k_values = range(1, 21)
train_accuracies = []
test_accuracies = []

# Test each K value
for k in k_values:
    # Create KNN with current K
    knn = KNeighborsClassifier(n_neighbors=k)

    # Train the model
    knn.fit(X_train_custom, y_train_custom)

    # Evaluate on training and test data
    train_acc = knn.score(X_train_custom, y_train_custom)
    test_acc = knn.score(X_test_custom, y_test_custom)

    train_accuracies.append(train_acc)
    test_accuracies.append(test_acc)

    # Print results every few iterations
    if k in [1, 5, 10, 15, 20]:
        print(f"K={k:2d}: Train={train_acc:.3f}, Test={test_acc:.3f}")

# Find best K based on test accuracy
best_k = k_values[test_accuracies.index(max(test_accuracies))]
print(f"\n[OK] Best K value: {best_k} (Test Accuracy: {max(test_accuracies):.3f})")

# Visualize how accuracy changes with K
plt.figure(figsize=(12, 5))

# Plot 1: Accuracy vs K
plt.subplot(1, 2, 1)
plt.plot(k_values, train_accuracies, marker="o", label="Training Accuracy", linewidth=2)
plt.plot(k_values, test_accuracies, marker="s", label="Test Accuracy", linewidth=2)
plt.axvline(x=best_k, color="red", linestyle="--", alpha=0.7, label=f"Best K={best_k}")
plt.xlabel("K Value")
plt.ylabel("Accuracy")
plt.title("Iris Dataset: KNN Accuracy vs K")
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 2: Zoomed view
plt.subplot(1, 2, 2)
plt.plot(k_values, test_accuracies, marker="s", linewidth=2, color="green")
plt.axvline(x=best_k, color="red", linestyle="--", alpha=0.7, label=f"Best K={best_k}")
plt.xlabel("K Value")
plt.ylabel("Test Accuracy")
plt.title("Test Accuracy Detailed View")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("knn_k_optimization.png", dpi=150, bbox_inches="tight")
print("[OK] Visualization saved as 'knn_k_optimization.png'")
# plt.show() - saved to file instead


# ============================================================================
# SECTION 4: CROSS-VALIDATION FOR K SELECTION
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 4: CROSS-VALIDATION FOR K SELECTION")
print("=" * 80)

print("\n1. Using 5-Fold Cross-Validation:")
print("-" * 40)

# Test K values using cross-validation
k_values_cv = range(1, 21, 2)  # Test odd numbers only
cv_scores_mean = []
cv_scores_std = []

# For each K value
for k in k_values_cv:
    # Create KNN classifier
    knn = KNeighborsClassifier(n_neighbors=k)

    # Calculate cross-validation scores (5 folds)
    # Each fold uses different training/test split
    cv_scores = cross_val_score(knn, X_train_custom, y_train_custom, cv=5)

    # Store mean and standard deviation
    cv_scores_mean.append(cv_scores.mean())
    cv_scores_std.append(cv_scores.std())

# Find best K
best_k_cv = list(k_values_cv)[cv_scores_mean.index(max(cv_scores_mean))]

print("\nCross-Validation Results:")
for k, mean, std in zip(k_values_cv, cv_scores_mean, cv_scores_std):
    print(f"K={k:2d}: CV Score = {mean:.3f} (+/- {std:.3f})")

print(f"\n[OK] Best K by Cross-Validation: {best_k_cv}")


# ============================================================================
# SECTION 5: PREDICTING SINGLE SAMPLES
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 5: PREDICTING INDIVIDUAL SAMPLES")
print("=" * 80)

print("\n1. Predict a Single Iris Flower:")
print("-" * 40)

# Create a test flower with specific measurements
test_flower = np.array([[6.2, 2.9, 4.3, 1.3]])  # One sample with 4 features

# Predict using best K
knn_best = KNeighborsClassifier(n_neighbors=best_k)
knn_best.fit(X_train_custom, y_train_custom)

prediction = knn_best.predict(test_flower)
predicted_species = iris.target_names[prediction[0]]

print(f"Test flower measurements:")
print(f"  Sepal Length: {test_flower[0, 0]} cm")
print(f"  Sepal Width:  {test_flower[0, 1]} cm")
print(f"  Petal Length: {test_flower[0, 2]} cm")
print(f"  Petal Width:  {test_flower[0, 3]} cm")
print(f"\nPredicted species: {predicted_species}")

# Get K nearest neighbors and their distances
distances, indices = knn_best.kneighbors(test_flower)

print(f"\nK={best_k} Nearest Neighbors:")
for i, (dist, idx) in enumerate(zip(distances[0], indices[0]), 1):
    species = iris.target_names[y_train_custom[idx]]
    print(f"  {i}. Distance: {dist:.3f} - Species: {species}")


# ============================================================================
# SECTION 6: FEATURE SCALING IMPORTANCE
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 6: FEATURE SCALING (Why It Matters)")
print("=" * 80)

print("\n1. Comparing Scaled vs Unscaled Features:")
print("-" * 40)

# Without scaling
knn_unscaled = KNeighborsClassifier(n_neighbors=5)
knn_unscaled.fit(X_train_custom, y_train_custom)
accuracy_unscaled = knn_unscaled.score(X_test_custom, y_test_custom)

# With scaling
scaler = StandardScaler()  # Normalize features to mean=0, std=1
X_train_scaled = scaler.fit_transform(X_train_custom)
X_test_scaled = scaler.transform(X_test_custom)

knn_scaled = KNeighborsClassifier(n_neighbors=5)
knn_scaled.fit(X_train_scaled, y_train_custom)
accuracy_scaled = knn_scaled.score(X_test_scaled, y_test_custom)

print(f"Accuracy WITHOUT Scaling: {accuracy_unscaled:.3f}")
print(f"Accuracy WITH Scaling:    {accuracy_scaled:.3f}")
print(f"Difference: {abs(accuracy_scaled - accuracy_unscaled):.3f}")


# ============================================================================
# SECTION 7: DIGIT RECOGNITION (More Complex Example)
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 7: HANDWRITTEN DIGIT RECOGNITION")
print("=" * 80)

print("\n1. Loading Digit Dataset:")
print("-" * 40)

# Load handwritten digits dataset
X_digits, y_digits = load_digits(return_X_y=True, as_frame=False)
# X_digits: 1797 8x8 images (64 pixel values each); y_digits: labels 0-9

print(f"Dataset: {X_digits.shape[0]} images of {X_digits.shape[1]} pixels each")
print(f"Classes: {len(np.unique(y_digits))} digit classes (0-9)")

# Split data
X_train_digits, X_test_digits, y_train_digits, y_test_digits = train_test_split(
    X_digits, y_digits, test_size=0.2, random_state=42
)

# Scale features (important for digits)
scaler_digits = StandardScaler()
X_train_digits_scaled = scaler_digits.fit_transform(X_train_digits)
X_test_digits_scaled = scaler_digits.transform(X_test_digits)

print("\n2. Training KNN for Digit Recognition:")
print("-" * 40)

# Train KNN on digits
knn_digits = KNeighborsClassifier(n_neighbors=5)
knn_digits.fit(X_train_digits_scaled, y_train_digits)

# Evaluate
accuracy_digits = knn_digits.score(X_test_digits_scaled, y_test_digits)
print(f"[OK] Digit Recognition Accuracy: {accuracy_digits:.2%}")

# Show predictions for first 10 test images
y_pred_digits = knn_digits.predict(X_test_digits_scaled)

print("\n3. Sample Predictions (First 10 Test Samples):")
print("-" * 40)
for i in range(10):
    actual = y_test_digits[i]
    predicted = y_pred_digits[i]
    match = "[OK]" if actual == predicted else "[X]"
    print(f"  {match} Sample {i}: Actual={actual}, Predicted={predicted}")


# ============================================================================
# SECTION 8: CONFUSION MATRIX AND DETAILED METRICS
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 8: CONFUSION MATRIX & METRICS")
print("=" * 80)

print("\n1. Iris Dataset Confusion Matrix:")
print("-" * 40)

# Get predictions for iris test set
knn_final = KNeighborsClassifier(n_neighbors=best_k)
knn_final.fit(X_train_custom, y_train_custom)
y_pred_final = knn_final.predict(X_test_custom)

# Calculate confusion matrix
cm = confusion_matrix(y_test_custom, y_pred_final)

# Print confusion matrix
print("\nConfusion Matrix:")
print("(Rows=Actual, Columns=Predicted)")
print(cm)

# Create DataFrame for better visualization
cm_df = pd.DataFrame(
    cm,
    index=[f"Actual {name}" for name in iris.target_names],
    columns=[f"Pred {name}" for name in iris.target_names],
)
print("\n" + str(cm_df))

# Calculate and print detailed metrics
print("\n2. Detailed Metrics per Class:")
print("-" * 40)

for i, class_name in enumerate(iris.target_names):
    # Calculate metrics for this class
    tp = cm[i, i]  # Correctly predicted as this class
    fp = cm[:, i].sum() - tp  # Incorrectly predicted as this class
    fn = cm[i, :].sum() - tp  # Missed predictions of this class
    tn = cm.sum() - tp - fp - fn  # Correctly predicted as NOT this class

    # Calculate rates
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    print(f"\n{class_name}:")
    print(
        f"  Precision: {precision:.3f} (when we predict {class_name}, how often correct)"
    )
    print(f"  Recall:    {recall:.3f} (what % of actual {class_name} did we catch)")
    print(f"  F1-Score:  {f1:.3f} (balanced measure)")

# Visualize confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=iris.target_names,
    yticklabels=iris.target_names,
    cbar_kws={"label": "Count"},
)
plt.title(f"KNN Confusion Matrix (K={best_k})")
plt.ylabel("Actual Species")
plt.xlabel("Predicted Species")
plt.tight_layout()
plt.savefig("knn_confusion_matrix.png", dpi=150, bbox_inches="tight")
print("\n[OK] Confusion matrix visualization saved as 'knn_confusion_matrix.png'")
# plt.show() - saved to file instead


# ============================================================================
# SECTION 9: COMPARING K VALUES VISUALLY
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 9: VISUAL COMPARISON OF K VALUES")
print("=" * 80)

# Test different weighting strategies
k_test = 5
print(f"\n1. Comparing Distance Weighting (K={k_test}):")
print("-" * 40)

# Uniform weights (all neighbors vote equally)
knn_uniform = KNeighborsClassifier(n_neighbors=k_test, weights="uniform")
knn_uniform.fit(X_train_custom, y_train_custom)
acc_uniform = knn_uniform.score(X_test_custom, y_test_custom)

# Distance weights (closer neighbors vote more)
knn_distance = KNeighborsClassifier(n_neighbors=k_test, weights="distance")
knn_distance.fit(X_train_custom, y_train_custom)
acc_distance = knn_distance.score(X_test_custom, y_test_custom)

print(f"Uniform Weights:   {acc_uniform:.3f} (all neighbors equal)")
print(f"Distance Weights:  {acc_distance:.3f} (closer = more influence)")


# ============================================================================
# SECTION 10: COMPLETE WORKFLOW SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 10: COMPLETE WORKFLOW SUMMARY")
print("=" * 80)

print("""
KNN Classification Workflow:
1. [OK] Load Data
2. [OK] Explore Dataset
3. [OK] Scale Features (StandardScaler)
4. [OK] Split into Train/Test (80/20)
5. [OK] Find Optimal K (using cross-validation)
6. [OK] Train KNN Model
7. [OK] Make Predictions
8. [OK] Evaluate Performance (Accuracy, Precision, Recall)
9. [OK] Visualize Results (Confusion Matrix)
10. [OK] Deploy Model for New Predictions

Key Parameters to Tune:
- K: Number of neighbors (try 3, 5, 7, 9 for small datasets)
- weights: 'uniform' or 'distance'
- metric: 'euclidean', 'manhattan', 'minkowski'
- leaf_size: For performance optimization with large datasets
""")

# Final statistics
print("\nFinal Model Statistics:")
print(f"  Dataset: Iris Flowers")
print(f"  Samples: {len(X_train_custom)} training, {len(X_test_custom)} testing")
print(f"  Features: {X_train_custom.shape[1]}")
print(f"  Optimal K: {best_k}")
print(f"  Test Accuracy: {accuracy_iris:.2%}")
print(f"  Training Time: < 1ms (KNN is lazy learning)")

print("\n" + "=" * 80)
print("[OK] DEMO COMPLETE - All examples executed successfully!")
print("=" * 80)
