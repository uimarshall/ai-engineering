# Choosing the Optimal K Value for KNN - Complete Guide

## Quick Summary

The **K value** in KNN determines how many nearest neighbors to consider when making a prediction. Choosing the right K is crucial:

- **K too low** → Overfitting (sensitive to noise and outliers)
- **K too high** → Underfitting (loses important patterns)
- **Optimal K** → Best accuracy on test/validation data

---

## Files in This Guide

### 📚 Tutorial File
- **`What_Value_For_K.md`** - Comprehensive beginner-friendly tutorial with 12 detailed sections, visual examples, and practical guidance

### 💻 Code Examples
- **`finding_optimal_k.py`** - 10 complete, runnable Python examples with full explanations

### 📋 Additional Resources
- **`K_Selection_README.md`** - This file
- **`K_SELECTION_QUICK_REFERENCE.md`** - Cheat sheet and formulas

---

## Learning Path

### Beginner Path
1. Start with **Part 1** of `What_Value_For_K.md` - Understand how K affects predictions
2. Read **Part 2** - Learn about the trade-offs
3. Run **Example 1** and **Example 2** from `finding_optimal_k.py`
4. Answer: "Why is K=1 usually not the best choice?"

### Intermediate Path
1. Read **Part 5** - Learn the practical rules
2. Run **Example 3** - Finding the optimal K
3. Run **Example 4** - Cross-validation approach
4. Run **Example 9** - Common mistakes
5. Practice: Try these examples on your own dataset

### Advanced Path
1. Read **Part 8-12** - Edge cases and complete workflow
2. Run **Example 5** - Handling class imbalance
3. Run **Example 8** - Complete workflow with Digits dataset
4. Implement your own K selection loop

---

## Quick Start Guide

### The Simplest Approach (3 Steps)

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
import numpy as np

# Step 1: Use heuristic to start
k_start = int(np.sqrt(len(X_train)))
if k_start % 2 == 0:
    k_start += 1  # Make it odd

# Step 2: Test a range around the heuristic
k_values = range(max(1, k_start-4), k_start+5, 2)  # Test nearby odd values
scores = []

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    score = cross_val_score(knn, X_train, y_train, cv=5).mean()
    scores.append(score)

# Step 3: Pick the K with best score
best_k = list(k_values)[np.argmax(scores)]
print(f"Best K: {best_k}")
```

---

## Decision Tree for K Selection

```
START: Need to choose K

├─ Do you have a LOT of data (>1000 samples)?
│  ├─ YES → Use K = sqrt(n_samples), test nearby values
│  └─ NO → Use K = 3 to 9, avoid very large K
│
├─ Are your classes balanced?
│  ├─ YES (all classes have similar count)
│  │   └─ Use medium K (5-11)
│  └─ NO (some classes rare)
│      └─ Use smaller K (3-7) to catch minority classes
│
├─ Is your data noisy/has outliers?
│  ├─ YES → Use larger K (7-15) to smooth predictions
│  └─ NO → Can use smaller K (3-7)
│
└─ ALWAYS use ODD numbers for K!
   └─ K = 1, 3, 5, 7, 9, 11, 13, 15, ...
```

---

## Common K Value Choices

| Dataset Size | Balanced? | Noise Level | Recommended K |
|--------------|-----------|------------|----------------|
| <50 samples  | Yes | Low | 3-5 |
| <50 samples  | Yes | High | 5-7 |
| <50 samples  | No | Low | 3 |
| <50 samples  | No | High | 3-5 |
| 50-500 | Yes | Low | 5-9 |
| 50-500 | Yes | High | 7-11 |
| 50-500 | No | Low | 3-5 |
| 50-500 | No | High | 5-9 |
| 500+ | Yes | Low | 7-15 |
| 500+ | Yes | High | 11-21 |
| 500+ | No | Low | 5-9 |
| 500+ | No | High | 9-17 |

**Note:** Always verify with cross-validation on your specific data!

---

## The Heuristic Formula

```
K = sqrt(n_training_samples)

Then:
1. If K is even, add 1 to make it odd
2. Test K-2, K, K+2 to find the best
3. Validate with cross-validation
```

**Example:**
- If you have 100 training samples: K = sqrt(100) = 10 → round up to 11 (odd)
- Test K values: 9, 11, 13
- Pick the one with best cross-validation score

---

## How to Run the Code Examples

### Option 1: Run the Complete Demo
```bash
cd C:\Users\uimar\code\Githubfiles\ai-engineering\DSI\Day-130
python finding_optimal_k.py
```

This will run all 10 examples and show you the complete output with explanations.

### Option 2: Extract and Run Individual Examples
```python
# Copy Example 2 code from finding_optimal_k.py
# Modify it for your own dataset
# Run in your Python environment
```

---

## What Makes a Good K?

### Characteristics of Good K

✅ **Good K values:**
- Odd number (prevents ties)
- Produces high test/CV accuracy
- Generalizes to new data
- Balances all classes fairly (if imbalanced)
- Doesn't change predictions drastically with tiny data changes

### Characteristics of Bad K

❌ **Avoid:**
- K = 1 (overfits immediately)
- K = even number (ties in voting)
- Very large K (> n_samples / 3)
- K chosen from training data only
- K that ignores minority classes

---

## Step-by-Step Workflow

### The Production-Ready Process

```
1. DATA PREPARATION
   └─ Load dataset
   └─ Explore and understand it
   └─ Check class distribution
   └─ Handle any missing values

2. PREPROCESSING
   └─ Scale features (MinMaxScaler or StandardScaler)
   └─ Split into train/test (70/30 or 80/20)

3. HEURISTIC STARTING POINT
   └─ Calculate K = sqrt(n_training_samples)
   └─ Round to nearest odd number

4. GRID SEARCH
   └─ Test K values: K-4, K-2, K, K+2, K+4
   └─ (or wider range if needed)
   └─ Record cross-validation accuracy for each

5. SELECTION
   └─ Choose K with highest CV accuracy
   └─ Verify it makes sense for your problem

6. VALIDATION
   └─ Train final model on full training set
   └─ Evaluate on test set
   └─ Document the chosen K

7. DEPLOYMENT
   └─ Use this K consistently
   └─ Retrain periodically with new data
   └─ Monitor performance over time
```

---

## Important Tips

### ✓ DO THIS
- ✅ Use odd numbers for K
- ✅ Scale your data before KNN
- ✅ Split data BEFORE scaling
- ✅ Evaluate on test set, not training set
- ✅ Use cross-validation for robustness
- ✅ Consider class distribution in imbalanced datasets
- ✅ Test multiple K values
- ✅ Visualize accuracy vs K to see the pattern

### ✗ DON'T DO THIS
- ❌ Use K = 1 (overfits)
- ❌ Use even K values
- ❌ Choose K based on training accuracy
- ❌ Evaluate K on same data used to scale
- ❌ Use K > n_training_samples / 2
- ❌ Use K larger than a few percent of your dataset
- ❌ Ignore class imbalance
- ❌ Skip cross-validation

---

## Troubleshooting

### Problem: All K values give same accuracy
- Your dataset might be too simple
- Try larger K range (1 to 51)
- Check if features are properly scaled

### Problem: Best K = 1
- Likely overfitting on this data
- Increase test set size
- Try cross-validation instead
- Use K = 3 or 5 anyway (more robust)

### Problem: Minority class never predicted
- Use smaller K (3-5 instead of 11-21)
- Check cross-validation by class
- Consider class weights

### Problem: Accuracy drops dramatically with K change
- Your model is unstable
- Check for outliers in data
- Try stronger feature scaling
- Increase dataset size

---

## When to Use Which Approach

### Use **Train/Test Split** if:
- You have lots of data (>1000 samples)
- You want quick results
- You're in a time crunch

### Use **Cross-Validation** if:
- You have limited data
- You want reliable estimates
- You need to be thorough
- You're building production models

**Recommended:** Always use cross-validation for final K selection!

---

## Next Steps After Choosing K

Once you've found your optimal K:

1. **Train Final Model**
   ```python
   knn = KNeighborsClassifier(n_neighbors=best_k)
   knn.fit(X_train, y_train)
   ```

2. **Evaluate on Test Set**
   ```python
   accuracy = knn.score(X_test, y_test)
   print(f"Test accuracy: {accuracy:.1%}")
   ```

3. **Make Predictions**
   ```python
   predictions = knn.predict(X_new)
   ```

4. **Consider Alternatives**
   - Is this good enough?
   - Should you try other algorithms?
   - Can you improve features?

---

## Additional Resources

📖 **In the Markdown tutorial:**
- Part 1-4: Understanding K effect
- Part 5-7: Practical rules and finding optimal K
- Part 8: Code examples preview
- Part 9-12: Key takeaways and decision trees

🐍 **In the Python file:**
- Example 1: K effect visualization
- Example 2-3: Systematic testing and optimal K
- Example 4: Cross-validation approach
- Example 5: Imbalanced classes
- Example 6: Heuristic formula
- Example 7: Small datasets
- Example 8: Complete workflow
- Example 9: Common mistakes
- Example 10: Best practices checklist

---

## Remember

> **The perfect K doesn't exist universally.** Different datasets need different K values. Your job is to systematically test options and find what works best for YOUR specific data.

**Key phrase to remember:** *"Test, measure, validate, deploy!"*

---

## Checklist Before Using Your Model

- [ ] Did you scale your data?
- [ ] Did you split before scaling?
- [ ] Did you choose an odd K?
- [ ] Did you test multiple K values?
- [ ] Did you use test/validation data (not training)?
- [ ] Did you use cross-validation?
- [ ] Is your K reasonable for dataset size?
- [ ] Have you checked against class imbalance?
- [ ] Does K make sense for your problem domain?
- [ ] Have you validated on new data?

If you answered YES to all, you're ready to deploy! 🚀

---

**Happy K selection! Remember: small K = detailed, large K = smooth. Find your balance!**
