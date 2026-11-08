"""
Euclidean Distance Calculations - Practical Examples for KNN
============================================================
This script demonstrates how to calculate distances in multi-dimensional space
and how these calculations form the basis of the KNN algorithm.

All code is heavily commented for beginner-level understanding.
"""

import math
import numpy as np
import pandas as pd
from collections import Counter

print("=" * 80)
print("EUCLIDEAN DISTANCE CALCULATIONS - BEGINNER TUTORIAL")
print("=" * 80)

# ============================================================================
# EXAMPLE 1: MANUAL DISTANCE CALCULATION
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 1: Manual Euclidean Distance Calculation")
print("=" * 80)

print("\n1. Calculate distance between two 2D points:")
print("-" * 40)

# Define two data points (coordinates on a 2D plot)
# These are the same points from the tutorial
point_green = (4, 4)  # Green point in the tutorial
point_red = (3, 2)    # Red (new) point in the tutorial

print(f"Green point (training data): {point_green}")
print(f"Red point (new data): {point_red}")

# Step 1: Calculate the difference in each dimension
diff_x = point_green[0] - point_red[0]  # Difference in X coordinate (input variable 1)
diff_y = point_green[1] - point_red[1]  # Difference in Y coordinate (input variable 2)

print(f"\nStep 1 - Calculate differences:")
print(f"  dx (diff_x) = {point_green[0]} - {point_red[0]} = {diff_x}")
print(f"  dy (diff_y) = {point_green[1]} - {point_red[1]} = {diff_y}")

# Step 2: Square each difference
squared_diff_x = diff_x ** 2
squared_diff_y = diff_y ** 2

print(f"\nStep 2 - Square the differences:")
print(f"  (dx)^2 = {diff_x}^2 = {squared_diff_x}")
print(f"  (dy)^2 = {diff_y}^2 = {squared_diff_y}")

# Step 3: Add the squared differences
sum_of_squares = squared_diff_x + squared_diff_y

print(f"\nStep 3 - Sum the squared differences:")
print(f"  Sum = {squared_diff_x} + {squared_diff_y} = {sum_of_squares}")

# Step 4: Take the square root
distance = math.sqrt(sum_of_squares)

print(f"\nStep 4 - Take the square root:")
print(f"  Distance = sqrt({sum_of_squares}) = {distance:.3f}")

print(f"\n[OK] Euclidean distance = {distance:.3f} units")


# ============================================================================
# EXAMPLE 2: FUNCTION FOR DISTANCE CALCULATION
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 2: Reusable Distance Function")
print("=" * 80)

print("\n1. Creating a function to calculate distance:")
print("-" * 40)

def euclidean_distance(point1, point2):
    """
    Calculate the Euclidean distance between two points.
    
    This is the straight-line distance between any two points,
    regardless of how many dimensions they have.
    
    Args:
        point1: tuple or list of coordinates (e.g., (x, y) or (x, y, z))
        point2: tuple or list of coordinates (same dimensions as point1)
    
    Returns:
        float: The distance between the two points
    
    Formula: distance = sqrt((x1-x2)^2 + (y1-y2)^2 + (z1-z2)^2 + ...)
    """
    # Check that both points have the same number of dimensions
    if len(point1) != len(point2):
        raise ValueError(f"Points must have same dimensions! Got {len(point1)} and {len(point2)}")
    
    # Calculate sum of squared differences for all dimensions
    sum_of_squares = 0
    for i in range(len(point1)):
        difference = point1[i] - point2[i]  # Calculate difference in this dimension
        sum_of_squares += difference ** 2   # Add squared difference to sum
    
    # Take square root of the sum to get the distance
    distance = math.sqrt(sum_of_squares)
    
    return distance

# Test with 2D points
print("\n2D Points (X, Y coordinates):")
p1 = (4, 4)
p2 = (3, 2)
dist_2d = euclidean_distance(p1, p2)
print(f"  Distance between {p1} and {p2}: {dist_2d:.3f}")

# Test with 3D points
print("\n3D Points (X, Y, Z coordinates):")
p3 = (1, 2, 3)
p4 = (4, 5, 6)
dist_3d = euclidean_distance(p3, p4)
print(f"  Distance between {p3} and {p4}: {dist_3d:.3f}")

# Test with 4D points
print("\n4D Points (higher dimensional space):")
p5 = (0, 0, 0, 0)
p6 = (1, 1, 1, 1)
dist_4d = euclidean_distance(p5, p6)
print(f"  Distance between {p5} and {p6}: {dist_4d:.3f}")

# Test with 5D points
print("\n5D Points (even higher dimensional space):")
p7 = (1, 2, 3, 4, 5)
p8 = (2, 3, 4, 5, 6)
dist_5d = euclidean_distance(p7, p8)
print(f"  Distance between {p7} and {p8}: {dist_5d:.3f}")

print("\n[OK] Function works with any number of dimensions!")


# ============================================================================
# EXAMPLE 3: UNDERSTANDING THE FORMULA WITH DIFFERENT SCENARIOS
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 3: Understanding Different Distance Scenarios")
print("=" * 80)

print("\nScenario 1 - Points on same horizontal line (dy = 0):")
print("-" * 40)
# If points have same Y coordinate, B = 0
same_y_p1 = (0, 5)
same_y_p2 = (3, 5)
same_y_dist = euclidean_distance(same_y_p1, same_y_p2)
print(f"Points: {same_y_p1} and {same_y_p2}")
print(f"Distance = sqrt((3-0)^2 + (5-5)^2) = sqrt(9 + 0) = {same_y_dist:.3f}")
print(f"Distance equals the absolute difference in X: {abs(same_y_p2[0] - same_y_p1[0])}")

print("\nScenario 2 - Points on same vertical line (dx = 0):")
print("-" * 40)
# If points have same X coordinate, A = 0
same_x_p1 = (2, 0)
same_x_p2 = (2, 4)
same_x_dist = euclidean_distance(same_x_p1, same_x_p2)
print(f"Points: {same_x_p1} and {same_x_p2}")
print(f"Distance = sqrt((2-2)^2 + (4-0)^2) = sqrt(0 + 16) = {same_x_dist:.3f}")
print(f"Distance equals the absolute difference in Y: {abs(same_x_p2[1] - same_x_p1[1])}")

print("\nScenario 3 - Identical points (distance = 0):")
print("-" * 40)
# Distance between identical points should be 0
same_p1 = (3, 4)
same_p2 = (3, 4)
same_dist = euclidean_distance(same_p1, same_p2)
print(f"Points: {same_p1} and {same_p2}")
print(f"Distance = sqrt((3-3)^2 + (4-4)^2) = sqrt(0 + 0) = {same_dist:.3f}")


# ============================================================================
# EXAMPLE 4: COMPARING DISTANCES (FINDING NEAREST NEIGHBOR)
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 4: Finding the Nearest Neighbor")
print("=" * 80)

print("\n1. Create training data (known points with classes):")
print("-" * 40)

# Training data - points we already know the class for
training_points = {
    'Point A': (1, 1),  # Class: Red
    'Point B': (2, 2),  # Class: Red
    'Point C': (2, 4),  # Class: Blue
    'Point D': (3, 3),  # Class: Red
    'Point E': (4, 4),  # Class: Blue
    'Point F': (4, 2),  # Class: Blue
}

classes = {
    'Point A': 'Red',
    'Point B': 'Red',
    'Point C': 'Blue',
    'Point D': 'Red',
    'Point E': 'Blue',
    'Point F': 'Blue',
}

# New point we want to classify
new_point = (3, 2)

print(f"Training data:")
for name, coords in training_points.items():
    print(f"  {name}: {coords} -> Class: {classes[name]}")

print(f"\nNew point to classify: {new_point}")

# Calculate distance from new point to all training points
print("\n2. Calculate distances:")
print("-" * 40)

distances_dict = {}
for name, coords in training_points.items():
    dist = euclidean_distance(new_point, coords)
    distances_dict[name] = dist
    print(f"  Distance to {name} {coords}: {dist:.3f}")

# Find nearest neighbor (smallest distance)
nearest_point = min(distances_dict, key=distances_dict.get)
nearest_distance = distances_dict[nearest_point]
nearest_class = classes[nearest_point]

print(f"\n[OK] Nearest neighbor: {nearest_point}")
print(f"[OK] Distance: {nearest_distance:.3f}")
print(f"[OK] Class: {nearest_class}")
print(f"[OK] Predicted class for {new_point}: {nearest_class}")


# ============================================================================
# EXAMPLE 5: K-NEAREST NEIGHBORS (K=3)
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 5: K-Nearest Neighbors (K=3)")
print("=" * 80)

print("\n1. Find K=3 nearest neighbors:")
print("-" * 40)

# Sort distances to find K nearest
K = 3
sorted_distances = sorted(distances_dict.items(), key=lambda x: x[1])

print(f"Finding K={K} nearest neighbors:\n")

# Store the K nearest neighbors
k_nearest = []
for i, (name, dist) in enumerate(sorted_distances[:K], 1):
    coords = training_points[name]
    class_label = classes[name]
    k_nearest.append(class_label)
    print(f"  {i}. {name} {coords}")
    print(f"     Distance: {dist:.3f}")
    print(f"     Class: {class_label}\n")

# Perform majority vote
print("2. Majority vote among K=3 neighbors:")
print("-" * 40)

# Count votes
vote_counts = Counter(k_nearest)
print(f"Vote counts: {dict(vote_counts)}")

# Get predicted class (most common)
predicted_class = vote_counts.most_common(1)[0][0]
vote_count = vote_counts.most_common(1)[0][1]

print(f"\n[OK] Predicted class: {predicted_class} ({vote_count} votes out of {K})")


# ============================================================================
# EXAMPLE 6: USING NUMPY FOR EFFICIENCY
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 6: Using NumPy for Efficient Calculations")
print("=" * 80)

print("\n1. NumPy approach (vectorized):")
print("-" * 40)

# Convert to numpy arrays
point_a = np.array([4, 4])
point_b = np.array([3, 2])

# Method 1: Using np.linalg.norm (recommended)
distance_numpy = np.linalg.norm(point_a - point_b)
print(f"Method 1 (np.linalg.norm): {distance_numpy:.3f}")

# Method 2: Manual with numpy operations
distance_manual = np.sqrt(np.sum((point_a - point_b)**2))
print(f"Method 2 (manual numpy): {distance_manual:.3f}")

# Verify it matches our manual calculation
distance_math = euclidean_distance((4, 4), (3, 2))
print(f"Method 3 (manual math): {distance_math:.3f}")

print(f"\n[OK] All methods give the same result: {distance_numpy:.3f}")

print("\n2. Computing distances to multiple points at once:")
print("-" * 40)

# Create array of all training points
training_array = np.array([
    [1, 1],  # Point A
    [2, 2],  # Point B
    [2, 4],  # Point C
    [3, 3],  # Point D
    [4, 4],  # Point E
    [4, 2],  # Point F
])

new_point_array = np.array([3, 2])

# Calculate distances to all points at once
distances_all = np.linalg.norm(training_array - new_point_array, axis=1)

print(f"New point: {new_point_array}")
print("\nDistances to all training points:")
for i, dist in enumerate(distances_all, 1):
    print(f"  Point {i}: {dist:.3f}")

# Find K nearest
k = 3
k_nearest_indices = np.argsort(distances_all)[:k]
print(f"\nK={k} nearest neighbors (indices): {k_nearest_indices}")
print(f"K={k} nearest distances: {distances_all[k_nearest_indices]}")


# ============================================================================
# EXAMPLE 7: DISTANCE COMPARISON TABLE
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 7: Distance Comparison Table")
print("=" * 80)

print("\n1. Create distance table:")
print("-" * 40)

# Create a more detailed comparison
data_for_table = []
for i, (name, coords) in enumerate(training_points.items(), 1):
    dist = euclidean_distance(new_point, coords)
    class_label = classes[name]
    data_for_table.append({
        'Rank': i,
        'Point': name,
        'Coordinates': str(coords),
        'Distance': round(dist, 3),
        'Class': class_label
    })

# Create DataFrame and sort by distance
df = pd.DataFrame(data_for_table)
df_sorted = df.sort_values('Distance').reset_index(drop=True)
df_sorted['Rank'] = range(1, len(df_sorted) + 1)

print(f"All points sorted by distance from {new_point}:\n")
print(df_sorted.to_string(index=False))

print(f"\nK=3 Nearest Neighbors:")
print(df_sorted.head(3).to_string(index=False))


# ============================================================================
# EXAMPLE 8: PERFORMANCE COMPARISON
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 8: Performance Comparison - Manual vs NumPy")
print("=" * 80)

import time

print("\n1. Small dataset (6 points):")
print("-" * 40)

# Time manual calculation
start = time.time()
for _ in range(10000):
    for coords in training_points.values():
        euclidean_distance(new_point, coords)
manual_time = time.time() - start

# Time NumPy calculation
start = time.time()
for _ in range(10000):
    np.linalg.norm(training_array - np.array(new_point), axis=1)
numpy_time = time.time() - start

print(f"Manual method (10,000 iterations): {manual_time:.4f} seconds")
print(f"NumPy method (10,000 iterations): {numpy_time:.4f} seconds")
print(f"NumPy is {manual_time/numpy_time:.1f}x faster for this dataset")

print("\n[Note] For larger datasets, the difference is even more dramatic!")


# ============================================================================
# EXAMPLE 9: UNDERSTANDING WHEN DISTANCES MATTER
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 9: Why Distance Calculations Matter for KNN")
print("=" * 80)

print("\n1. The impact of K value on predictions:")
print("-" * 40)

# Use our sorted distances
print(f"New point: {new_point}")
print(f"\nNeighbors sorted by distance:")

for k_test in [1, 3, 5]:
    print(f"\n--- Using K={k_test} ---")
    
    k_neighbors = df_sorted.head(k_test)
    classes_k = k_neighbors['Class'].tolist()
    votes = Counter(classes_k)
    
    print("Classes of K neighbors:", classes_k)
    print("Vote count:", dict(votes))
    
    predicted = votes.most_common(1)[0][0]
    print(f"Predicted class: {predicted}")


# ============================================================================
# EXAMPLE 10: PRACTICAL EXERCISE
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 10: Practical Exercise - Classify Multiple Points")
print("=" * 80)

print("\n1. Classify 3 new points with K=3:")
print("-" * 40)

# Multiple new points to classify
new_points_to_classify = [
    (1, 1),   # Should be close to Point A (Red)
    (4, 4),   # Should be close to Point E (Blue)
    (3, 2),   # The one we've been using
]

for test_point in new_points_to_classify:
    print(f"\nClassifying: {test_point}")
    
    # Calculate distances
    distances = []
    for name, coords in training_points.items():
        dist = euclidean_distance(test_point, coords)
        class_label = classes[name]
        distances.append((name, dist, class_label))
    
    # Sort by distance and take K=3 nearest
    distances.sort(key=lambda x: x[1])
    k_nearest = distances[:3]
    
    # Vote
    classes_voted = [item[2] for item in k_nearest]
    vote = Counter(classes_voted).most_common(1)[0][0]
    
    print(f"  3 nearest: {', '.join([f'{name}({d:.2f})' for name, d, _ in k_nearest])}")
    print(f"  Predicted class: {vote}")


# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("SUMMARY - KEY CONCEPTS")
print("=" * 80)

summary_text = """
1. EUCLIDEAN DISTANCE
   • Formula: distance = sqrt((x1-x2)^2 + (y1-y2)^2 + ... + (xn-xn)^2)
   • Used by KNN to find "nearest" neighbors
   • Works in any number of dimensions

2. KNN ALGORITHM
   • Calculate distances to all known points
   • Sort by distance (smallest first)
   • Select K nearest neighbors
   • Predict class by majority vote

3. KEY PARAMETERS
   • K: Number of neighbors to consider
   • Too small (K=1): Can overfit
   • Too large (K=n): Can underfit
   • Often K = sqrt(number of samples)

4. IMPLEMENTATION METHODS
   • Manual: Best for learning, slower
   • NumPy: Vectorized, much faster
   • Scikit-Learn: Production-ready, easiest

5. IMPORTANT NOTES
   • Order of subtraction doesn't matter (squared differences)
   • Distances always positive
   • Feature scaling is critical (more on this next!)
   • Works with any number of dimensions
"""

print(summary_text)

print("=" * 80)
print("[OK] DEMO COMPLETE - All examples executed successfully!")
print("=" * 80)
