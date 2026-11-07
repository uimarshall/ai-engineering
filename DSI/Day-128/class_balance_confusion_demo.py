"""
Class Balance & Confusion Matrix - Practical Python Examples
Demonstrates both concepts with real code
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, precision_score, recall_score, f1_score
from sklearn.utils import resample
from imblearn.over_sampling import SMOTE

print("=" * 80)
print("CLASS BALANCE & CONFUSION MATRIX - PRACTICAL GUIDE")
print("=" * 80)

# ============================================================================
# PART 1: CREATE IMBALANCED DATASET
# ============================================================================
print("\n" + "=" * 80)
print("PART 1: CREATING IMBALANCED DATASET")
print("=" * 80)

# Create imbalanced dataset (like real-world data)
X, y = make_classification(
    n_samples=1000,
    n_features=10,
    n_informative=5,
    n_redundant=2,
    weights=[0.95, 0.05],  # 95% class 0, 5% class 1 (imbalanced!)
    random_state=42
)

# Convert to DataFrame for easier handling
X_df = pd.DataFrame(X, columns=[f'Feature_{i}' for i in range(10)])

print(f"\nDataset Size: {len(X)} samples")
print(f"\nClass Distribution (IMBALANCED):")
print(f"  Class 0 (Majority): {(y == 0).sum()} samples ({(y == 0).sum()/len(y)*100:.1f}%)")
print(f"  Class 1 (Minority): {(y == 1).sum()} samples ({(y == 1).sum()/len(y)*100:.1f}%)")
print(f"\nImbalance Ratio: {(y == 0).sum() / (y == 1).sum():.1f}:1")
print("  (For every 1 minority sample, there are ~19 majority samples)")

# ============================================================================
# PART 2: TRAIN MODEL ON IMBALANCED DATA (WITHOUT FIXING)
# ============================================================================
print("\n" + "=" * 80)
print("PART 2: MODEL WITHOUT FIXING IMBALANCE")
print("=" * 80)

X_train, X_test, y_train, y_test = train_test_split(
    X_df, y, test_size=0.2, random_state=42
)

print(f"\nTraining set class distribution:")
print(f"  Class 0: {(y_train == 0).sum()}")
print(f"  Class 1: {(y_train == 1).sum()}")

# Train model
model_imbalanced = RandomForestClassifier(n_estimators=100, random_state=42)
model_imbalanced.fit(X_train, y_train)

# Get predictions
y_pred_imbalanced = model_imbalanced.predict(X_test)

# Create confusion matrix
cm_imbalanced = confusion_matrix(y_test, y_pred_imbalanced)

print(f"\n--- CONFUSION MATRIX (Imbalanced Data) ---\n")
print("                Predicted 0   Predicted 1")
print(f"Actual Class 0      {cm_imbalanced[0,0]}           {cm_imbalanced[0,1]}")
print(f"Actual Class 1      {cm_imbalanced[1,0]}           {cm_imbalanced[1,1]}")

# Calculate metrics
accuracy_imb = (cm_imbalanced[0,0] + cm_imbalanced[1,1]) / cm_imbalanced.sum()
precision_imb = cm_imbalanced[1,1] / (cm_imbalanced[1,1] + cm_imbalanced[0,1]) if (cm_imbalanced[1,1] + cm_imbalanced[0,1]) > 0 else 0
recall_imb = cm_imbalanced[1,1] / (cm_imbalanced[1,1] + cm_imbalanced[1,0]) if (cm_imbalanced[1,1] + cm_imbalanced[1,0]) > 0 else 0
f1_imb = 2 * (precision_imb * recall_imb) / (precision_imb + recall_imb) if (precision_imb + recall_imb) > 0 else 0

print(f"\n--- METRICS (Imbalanced) ---")
print(f"  Accuracy:  {accuracy_imb:.4f} (looks good!)")
print(f"  Precision: {precision_imb:.4f} (when predicting class 1, how often correct?)")
print(f"  Recall:    {recall_imb:.4f} (how many class 1 samples did we catch?)")
print(f"  F1-Score:  {f1_imb:.4f} (balance of precision & recall)")

# Explain the results
print(f"\nInterpretation:")
print(f"  - Accuracy is high, but model is barely finding Class 1!")
print(f"  - Precision: {precision_imb:.1%} - when we say 'Class 1', we're right only {precision_imb:.1%}")
print(f"  - Recall: {recall_imb:.1%} - we missed {(1-recall_imb):.1%} of actual Class 1 samples!")
print(f"  - Model is taking shortcuts (saying 'Class 0' most of the time)")

# ============================================================================
# PART 3: FIX IMBALANCE - METHOD 1: OVERSAMPLING
# ============================================================================
print("\n" + "=" * 80)
print("PART 3: FIX IMBALANCE - METHOD 1: OVERSAMPLING")
print("=" * 80)

# Separate classes
mask_0 = (y_train == 0)
mask_1 = (y_train == 1)

X_train_0 = X_train[mask_0].copy()
y_train_0 = y_train[mask_0].copy()
X_train_1 = X_train[mask_1].copy()
y_train_1 = y_train[mask_1].copy()

# Oversample minority class (Class 1)
X_train_1_oversampled, y_train_1_oversampled = resample(
    X_train_1, y_train_1,
    n_samples=len(X_train_0),  # Match majority class size
    replace=True,  # Allow duplicates
    random_state=42
)

# Combine arrays
X_train_balanced_os = np.vstack([X_train_0, X_train_1_oversampled])
y_train_balanced_os = np.hstack([y_train_0, y_train_1_oversampled])

print(f"\nAfter Oversampling:")
print(f"  Class 0: {(y_train_balanced_os == 0).sum()} samples")
print(f"  Class 1: {(y_train_balanced_os == 1).sum()} samples")
print(f"  Balanced? YES! Both classes now have equal samples")

# Train model on balanced data
model_oversampled = RandomForestClassifier(n_estimators=100, random_state=42)
model_oversampled.fit(X_train_balanced_os, y_train_balanced_os)

y_pred_oversampled = model_oversampled.predict(X_test)
cm_oversampled = confusion_matrix(y_test, y_pred_oversampled)

print(f"\n--- CONFUSION MATRIX (Oversampled Data) ---\n")
print("                Predicted 0   Predicted 1")
print(f"Actual Class 0      {cm_oversampled[0,0]}           {cm_oversampled[0,1]}")
print(f"Actual Class 1      {cm_oversampled[1,0]}           {cm_oversampled[1,1]}")

accuracy_os = (cm_oversampled[0,0] + cm_oversampled[1,1]) / cm_oversampled.sum()
precision_os = cm_oversampled[1,1] / (cm_oversampled[1,1] + cm_oversampled[0,1]) if (cm_oversampled[1,1] + cm_oversampled[0,1]) > 0 else 0
recall_os = cm_oversampled[1,1] / (cm_oversampled[1,1] + cm_oversampled[1,0]) if (cm_oversampled[1,1] + cm_oversampled[1,0]) > 0 else 0
f1_os = 2 * (precision_os * recall_os) / (precision_os + recall_os) if (precision_os + recall_os) > 0 else 0

print(f"\n--- METRICS (Oversampled) ---")
print(f"  Accuracy:  {accuracy_os:.4f} (lower, but more honest)")
print(f"  Precision: {precision_os:.4f} (improved!)")
print(f"  Recall:    {recall_os:.4f} (improved!)")
print(f"  F1-Score:  {f1_os:.4f} (much better!)")

# ============================================================================
# PART 4: FIX IMBALANCE - METHOD 2: SMOTE
# ============================================================================
print("\n" + "=" * 80)
print("PART 4: FIX IMBALANCE - METHOD 2: SMOTE (Synthetic Minority Oversampling)")
print("=" * 80)

# Apply SMOTE to training data
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

print(f"\nAfter SMOTE:")
print(f"  Class 0: {(y_train_smote == 0).sum()} samples")
print(f"  Class 1: {(y_train_smote == 1).sum()} samples")
print(f"  Method: Created synthetic minority samples (not just duplicates)")

# Train model
model_smote = RandomForestClassifier(n_estimators=100, random_state=42)
model_smote.fit(X_train_smote, y_train_smote)

y_pred_smote = model_smote.predict(X_test)
cm_smote = confusion_matrix(y_test, y_pred_smote)

print(f"\n--- CONFUSION MATRIX (SMOTE Data) ---\n")
print("                Predicted 0   Predicted 1")
print(f"Actual Class 0      {cm_smote[0,0]}           {cm_smote[0,1]}")
print(f"Actual Class 1      {cm_smote[1,0]}           {cm_smote[1,1]}")

accuracy_smote = (cm_smote[0,0] + cm_smote[1,1]) / cm_smote.sum()
precision_smote = cm_smote[1,1] / (cm_smote[1,1] + cm_smote[0,1]) if (cm_smote[1,1] + cm_smote[0,1]) > 0 else 0
recall_smote = cm_smote[1,1] / (cm_smote[1,1] + cm_smote[1,0]) if (cm_smote[1,1] + cm_smote[1,0]) > 0 else 0
f1_smote = 2 * (precision_smote * recall_smote) / (precision_smote + recall_smote) if (precision_smote + recall_smote) > 0 else 0

print(f"\n--- METRICS (SMOTE) ---")
print(f"  Accuracy:  {accuracy_smote:.4f}")
print(f"  Precision: {precision_smote:.4f}")
print(f"  Recall:    {recall_smote:.4f}")
print(f"  F1-Score:  {f1_smote:.4f}")

# ============================================================================
# PART 5: COMPARISON
# ============================================================================
print("\n" + "=" * 80)
print("PART 5: COMPARISON OF ALL METHODS")
print("=" * 80)

comparison_df = pd.DataFrame({
    'Method': ['Imbalanced Data', 'Oversampling', 'SMOTE'],
    'Accuracy': [accuracy_imb, accuracy_os, accuracy_smote],
    'Precision': [precision_imb, precision_os, precision_smote],
    'Recall': [recall_imb, recall_os, recall_smote],
    'F1-Score': [f1_imb, f1_os, f1_smote]
})

print("\n")
print(comparison_df.to_string(index=False))

# ============================================================================
# PART 6: UNDERSTANDING CONFUSION MATRIX
# ============================================================================
print("\n" + "=" * 80)
print("PART 6: UNDERSTANDING CONFUSION MATRIX")
print("=" * 80)

print(f"\nBest Model's Confusion Matrix (SMOTE):")
print(f"\n                Predicted 0   Predicted 1")
print(f"Actual Class 0      {cm_smote[0,0]}           {cm_smote[0,1]}")
print(f"Actual Class 1      {cm_smote[1,0]}           {cm_smote[1,1]}")

print(f"\nBreakdown:")
print(f"  True Negative (TN):  {cm_smote[0,0]} - Correctly predicted Class 0")
print(f"  False Positive (FP): {cm_smote[0,1]} - Wrongly predicted Class 0 as Class 1")
print(f"  False Negative (FN): {cm_smote[1,0]} - Wrongly predicted Class 1 as Class 0")
print(f"  True Positive (TP):  {cm_smote[1,1]} - Correctly predicted Class 1")

print(f"\nWhat these numbers mean:")
print(f"  Precision = TP / (TP + FP) = {cm_smote[1,1]} / ({cm_smote[1,1]} + {cm_smote[0,1]}) = {precision_smote:.1%}")
print(f"    When model says 'Class 1', it's right {precision_smote:.1%} of the time")
print(f"\n  Recall = TP / (TP + FN) = {cm_smote[1,1]} / ({cm_smote[1,1]} + {cm_smote[1,0]}) = {recall_smote:.1%}")
print(f"    We catch {recall_smote:.1%} of actual Class 1 samples")

# ============================================================================
# VISUALIZATION
# ============================================================================
print("\n" + "=" * 80)
print("PART 7: CREATING VISUALIZATIONS")
print("=" * 80)

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Plot confusion matrices
matrices = [cm_imbalanced, cm_oversampled, cm_smote]
titles = ['Imbalanced', 'Oversampling', 'SMOTE']
axes_flat = axes.flatten()

for idx, (cm, title) in enumerate(zip(matrices, titles)):
    ax = axes_flat[idx]
    im = ax.imshow(cm, cmap='Blues', aspect='auto')
    ax.set_title(f'{title}\nConfusion Matrix')
    ax.set_ylabel('Actual')
    ax.set_xlabel('Predicted')
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    
    # Add text annotations
    for i in range(2):
        for j in range(2):
            text = ax.text(j, i, cm[i, j], ha="center", va="center", color="black", fontsize=14)
    
    plt.colorbar(im, ax=ax)

# Plot metrics comparison
ax = axes_flat[3]
methods = ['Imbalanced', 'Oversampling', 'SMOTE']
precisions = [precision_imb, precision_os, precision_smote]
recalls = [recall_imb, recall_os, recall_smote]
f1s = [f1_imb, f1_os, f1_smote]

x = np.arange(len(methods))
width = 0.25

ax.bar(x - width, precisions, width, label='Precision', color='skyblue')
ax.bar(x, recalls, width, label='Recall', color='lightcoral')
ax.bar(x + width, f1s, width, label='F1-Score', color='lightgreen')

ax.set_ylabel('Score')
ax.set_title('Metrics Comparison')
ax.set_xticks(x)
ax.set_xticklabels(methods)
ax.legend()
ax.set_ylim([0, 1])
ax.grid(axis='y', alpha=0.3)

# Plot accuracy comparison
ax = axes_flat[4]
accuracies = [accuracy_imb, accuracy_os, accuracy_smote]
colors_acc = ['red', 'orange', 'green']
bars = ax.bar(methods, accuracies, color=colors_acc)
ax.set_ylabel('Accuracy Score')
ax.set_title('Accuracy: Imbalanced vs Fixed')
ax.set_ylim([0, 1])
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{accuracies[i]:.3f}',
            ha='center', va='bottom')

# Plot class distribution
ax = axes_flat[5]
ax.bar(['Imbalanced\n(Original)', 'Oversampled'], 
       [(y_train == 1).sum(), len(y_train_balanced_os[y_train_balanced_os == 1])],
       color=['red', 'green'])
ax.set_ylabel('Number of Minority Class Samples')
ax.set_title('Class Balance: Before vs After')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(r'C:\Users\uimar\code\Githubfiles\ai-engineering\DSI\Day-128\class_balance_confusion_demo.png',
            dpi=300, bbox_inches='tight')
print("\n[OK] Visualization saved as 'class_balance_confusion_demo.png'")
plt.close()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("SUMMARY & KEY TAKEAWAYS")
print("=" * 80)

print(f"\n1. PROBLEM IDENTIFIED:")
print(f"   Original dataset was highly imbalanced (95:5 ratio)")
print(f"   Model just learned to say 'Class 0' most of the time")

print(f"\n2. SOLUTION 1 - OVERSAMPLING:")
print(f"   Duplicated minority class to match majority")
print(f"   Result: Recall improved from {recall_imb:.1%} to {recall_os:.1%}")

print(f"\n3. SOLUTION 2 - SMOTE:")
print(f"   Created synthetic minority samples")
print(f"   Result: Recall improved from {recall_imb:.1%} to {recall_smote:.1%}")

print(f"\n4. CONFUSION MATRIX SHOWS:")
print(f"   - How many samples were correctly classified")
print(f"   - How many were misclassified and in which direction")
print(f"   - Where the model struggles")

print(f"\n5. ACCURACY IS MISLEADING:")
print(f"   Imbalanced accuracy: {accuracy_imb:.1%} (seems good but model fails!)")
print(f"   SMOTE accuracy: {accuracy_smote:.1%} (lower but model actually works!)")

print(f"\n6. BETTER METRICS FOR IMBALANCED DATA:")
print(f"   Use: Precision, Recall, F1-Score, Confusion Matrix")
print(f"   Not: Accuracy alone")

print("\n" + "=" * 80)
print("Demo complete! All concepts demonstrated with real code.")
print("=" * 80)
