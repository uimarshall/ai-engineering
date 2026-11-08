# Euclidean Distance - Quick Reference Guide

## The Formula

### 2D Distance (Most Common)
```
distance = sqrt((x1 - x2)^2 + (y1 - y2)^2)
```

### 3D Distance
```
distance = sqrt((x1 - x2)^2 + (y1 - y2)^2 + (z1 - z2)^2)
```

### N-Dimensional Distance (General Formula)
```
distance = sqrt(SUM of (xi - xj)^2 for all dimensions)
```

---

## Python Implementation

### Method 1: Manual (Learning)
```python
import math

point1 = (4, 4)
point2 = (3, 2)

distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
print(f"Distance: {distance:.3f}")  # Output: 2.236
```

### Method 2: NumPy (Recommended)
```python
import numpy as np

point1 = np.array([4, 4])
point2 = np.array([3, 2])

distance = np.linalg.norm(point1 - point2)
print(f"Distance: {distance:.3f}")  # Output: 2.236
```

### Method 3: Reusable Function
```python
import math

def euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))

# Works with any number of dimensions
dist_2d = euclidean_distance((4, 4), (3, 2))      # 2.236
dist_3d = euclidean_distance((1, 2, 3), (4, 5, 6))  # 5.196
dist_4d = euclidean_distance((0, 0, 0, 0), (1, 1, 1, 1))  # 2.000
```

---

## Key Concepts

| Concept | Explanation |
|---------|-------------|
| **Euclidean Distance** | Straight-line distance between two points |
| **Based on** | Pythagorean theorem (a² + b² = c²) |
| **Used in KNN** | To identify the K nearest neighbors |
| **Dimensions** | Works in 2D, 3D, or any number of dimensions |
| **Order** | Distance from A to B = Distance from B to A |
| **Sign** | Squared differences eliminate negative values |

---

## Common Calculations

### Example 1: 2D Space
```
Point A: (1, 1)
Point B: (4, 5)

distance = sqrt((4-1)^2 + (5-1)^2)
distance = sqrt(3^2 + 4^2)
distance = sqrt(9 + 16)
distance = sqrt(25)
distance = 5.0
```

### Example 2: 3D Space
```
Point X: (0, 0, 0)
Point Y: (3, 4, 0)

distance = sqrt((3-0)^2 + (4-0)^2 + (0-0)^2)
distance = sqrt(9 + 16 + 0)
distance = sqrt(25)
distance = 5.0
```

### Example 3: High Dimensions
```
Point P: (1, 2, 3, 4, 5)
Point Q: (2, 3, 4, 5, 6)

distance = sqrt((2-1)^2 + (3-2)^2 + (4-3)^2 + (5-4)^2 + (6-5)^2)
distance = sqrt(1 + 1 + 1 + 1 + 1)
distance = sqrt(5)
distance = 2.236
```

---

## KNN Algorithm Steps

### Using Euclidean Distance for Classification

1. **Calculate distances** from new point to ALL training points
2. **Sort** distances from smallest to largest
3. **Select K** smallest distances (K nearest neighbors)
4. **Count classes** among these K neighbors
5. **Predict** the class with the highest count

### Pseudo-code
```python
def knn_classify(new_point, training_data, k=3):
    # Step 1: Calculate distances
    distances = []
    for train_point, train_class in training_data:
        dist = euclidean_distance(new_point, train_point)
        distances.append((dist, train_class))
    
    # Step 2 & 3: Sort and select K nearest
    distances.sort(key=lambda x: x[0])
    k_nearest = distances[:k]
    
    # Step 4 & 5: Vote and predict
    classes = [cls for _, cls in k_nearest]
    prediction = max(set(classes), key=classes.count)
    
    return prediction
```

---

## Distance Comparison Table

| Scenario | Formula | Result |
|----------|---------|--------|
| Horizontal line (dy=0) | sqrt(dx^2 + 0) | distance = \|dx\| |
| Vertical line (dx=0) | sqrt(0 + dy^2) | distance = \|dy\| |
| Diagonal | sqrt(dx^2 + dy^2) | Full formula |
| Same point (dx=0, dy=0) | sqrt(0 + 0) | distance = 0 |
| Pythagorean triple (3,4) | sqrt(9 + 16) | distance = 5 |

---

## Why Sign Doesn't Matter

Since we square all differences:
- (4 - 3)² = 1² = 1
- (3 - 4)² = (-1)² = 1

**Both give the same result!** This is why the order of subtraction doesn't matter.

---

## Important Notes for KNN

✓ **Always use consistent dimensions** - All points must have same number of features
✓ **Feature scaling matters** - Different ranges (age 0-100 vs income 0-1,000,000) can skew distances
✓ **K selection is critical** - Too small = overfit, Too large = underfit
✓ **Works with any metric** - Euclidean is most common, but Manhattan, Minkowski also work

---

## Performance Tips

| Method | Speed | Best For | Note |
|--------|-------|----------|------|
| Manual Loop | Slowest | Learning | Most educational |
| NumPy Vectorized | 10-100x faster | Medium datasets | Recommended |
| Scikit-Learn | 100-1000x faster | Production | Most optimized |

For **small datasets (< 1000 samples)**: Manual or NumPy
For **large datasets (> 100K)**: Always use Scikit-Learn

---

## Common Mistakes to Avoid

❌ Forgetting the square root: sqrt() is required!
❌ Using absolute value: Use (a-b)^2, not |a-b|
❌ Not scaling features: Will skew distance calculations
❌ Confusing distance with similarity: They're opposites (small = similar)
❌ Wrong K value: Test multiple values (1-20 typically)

---

## Formula Breakdown - Step by Step

```
Given: Point A (4, 4) and Point B (3, 2)

Step 1: Identify coordinates
  A = (x1=4, y1=4)
  B = (x2=3, y2=2)

Step 2: Calculate differences
  dx = x1 - x2 = 4 - 3 = 1
  dy = y1 - y2 = 4 - 2 = 2

Step 3: Square the differences
  dx² = 1² = 1
  dy² = 2² = 4

Step 4: Sum the squares
  dx² + dy² = 1 + 4 = 5

Step 5: Take square root
  distance = sqrt(5) = 2.236
```

---

## Comparison with Other Distance Metrics

| Metric | Formula | Use Case |
|--------|---------|----------|
| **Euclidean** | sqrt(sum of (xi-xj)^2) | Most common, general purpose |
| **Manhattan** | sum of \|xi-xj\| | City block distance |
| **Minkowski** | (sum of \|xi-xj\|^p)^(1/p) | Generalized distance |
| **Cosine** | 1 - (A·B)/(norm(A)norm(B)) | Text/high-dimensional data |

---

## When to Use Euclidean Distance

✓ Continuous numerical features
✓ Features with similar scales
✓ Low to medium dimensional data
✓ When interpretability matters (it's intuitive)
✓ Default choice for KNN

---

## Learning Resources

1. **Understand the concept first** - Visualize in 2D before going to 3D+
2. **Code it manually** - Build from scratch to understand deeply
3. **Try different datasets** - See how distance changes
4. **Experiment with K values** - See how predictions change
5. **Compare with other metrics** - Understand why Euclidean is standard

---

## Practice Exercises

### Easy
- Calculate distance between (0,0) and (3,4)
- Calculate distance between (1,1,1) and (2,2,2)

### Medium
- Create a function to find 5 nearest neighbors
- Classify a new point using majority vote

### Hard
- Implement KNN from scratch
- Compare performance across different K values
- Test with real dataset (iris, digits)

---

## Summary

- **Formula:** distance = sqrt((x1-x2)^2 + (y1-y2)^2 + ...)
- **Purpose:** Find similar points for KNN classification
- **Key:** Works in any number of dimensions
- **Important:** Feature scaling affects distances
- **Next:** Learn about feature scaling in Day-131

Happy learning! 🎓
