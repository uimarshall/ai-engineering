"""
Feature Importance in Random Forest Regression - Practical Guide
Demonstrates both Impurity Decrease and Permutation Importance methods
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_squared_error, r2_score

# ============================================================================
# STEP 1: Create a sample dataset
# ============================================================================
print("=" * 70)
print("STEP 1: Creating Sample Data")
print("=" * 70)

# Generate synthetic regression data
X, y = make_regression(
    n_samples=200,
    n_features=5,
    n_informative=3,  # Only 3 features actually drive the predictions
    noise=10,
    random_state=42
)

# Create a DataFrame for better readability
feature_names = ['Feature_A', 'Feature_B', 'Feature_C', 'Feature_D', 'Feature_E']
X_df = pd.DataFrame(X, columns=feature_names)

# In this dataset:
# - Features A, B, C are important (they actually predict the target)
# - Features D, E are noise (random, not useful)

print(f"\nDataset shape: {X_df.shape}")
print(f"Features: {feature_names}")
print(f"\nFirst few rows:")
print(X_df.head())
print(f"\nTarget (y) first few values: {y[:5]}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_df, y, test_size=0.2, random_state=42
)

# ============================================================================
# STEP 2: Train Random Forest Model
# ============================================================================
print("\n" + "=" * 70)
print("STEP 2: Training Random Forest Regressor")
print("=" * 70)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"\nModel Performance:")
print(f"  R² Score: {r2:.4f}")
print(f"  RMSE: {rmse:.4f}")

# ============================================================================
# METHOD 1: Mean Decrease in Impurity (Built-in Feature Importance)
# ============================================================================
print("\n" + "=" * 70)
print("METHOD 1: Mean Decrease in Impurity")
print("=" * 70)

impurity_importance = model.feature_importances_

importance_df_1 = pd.DataFrame({
    'Feature': feature_names,
    'Importance': impurity_importance,
    'Importance_%': (impurity_importance / impurity_importance.sum()) * 100
}).sort_values('Importance', ascending=False)

print("\nImpurity-based Feature Importance:")
print(importance_df_1.to_string(index=False))

print("\nHow it works:")
print("  - Measures: How much each feature reduces impurity when splitting data")
print("  - Based on: Gini impurity decrease across all trees")
print("  - Interpretation: Higher = more useful for decision-making")

# ============================================================================
# METHOD 2: Permutation Importance (Modern Approach)
# ============================================================================
print("\n" + "=" * 70)
print("METHOD 2: Permutation Importance")
print("=" * 70)

# Calculate permutation importance on TEST set
perm_result = permutation_importance(
    model,
    X_test,
    y_test,
    n_repeats=10,  # Shuffle and test 10 times for stability
    random_state=42,
    n_jobs=-1
)

importance_df_2 = pd.DataFrame({
    'Feature': feature_names,
    'Importance': perm_result.importances_mean,
    'Std_Dev': perm_result.importances_std,
    'Importance_%': (perm_result.importances_mean / perm_result.importances_mean.sum()) * 100
}).sort_values('Importance', ascending=False)

print("\nPermutation-based Feature Importance:")
print(importance_df_2.to_string(index=False))

print("\nHow it works:")
print("  1. Measure model performance (RMSE) on test data")
print("  2. Shuffle each feature randomly")
print("  3. Measure new performance on scrambled data")
print("  4. Calculate: Original RMSE - Scrambled RMSE")
print("  5. Higher difference = more important feature")

# ============================================================================
# WHAT HAPPENS WHEN YOU SHUFFLE A FEATURE?
# ============================================================================
print("\n" + "=" * 70)
print("STEP 3: Understanding Permutation Importance - Detailed View")
print("=" * 70)

original_rmse = rmse
print(f"\nOriginal Model RMSE (before shuffling): {original_rmse:.4f}\n")

# Shuffle each feature and measure impact
print("Performance when each feature is shuffled:\n")

for feature in feature_names:
    X_test_shuffled = X_test.copy()
    # Shuffle just this feature
    X_test_shuffled[feature] = np.random.permutation(X_test_shuffled[feature].values)
    
    # Get predictions with shuffled feature
    y_pred_shuffled = model.predict(X_test_shuffled)
    shuffled_rmse = np.sqrt(mean_squared_error(y_test, y_pred_shuffled))
    
    # Calculate importance
    importance_score = shuffled_rmse - original_rmse
    
    print(f"  {feature}:")
    print(f"    RMSE when shuffled: {shuffled_rmse:.4f}")
    print(f"    Importance score: {importance_score:.4f}")
    print()

# ============================================================================
# COMPARISON VISUALIZATION
# ============================================================================
print("=" * 70)
print("STEP 4: Comparing Both Methods Visually")
print("=" * 70)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Impurity Importance
ax1 = axes[0]
colors_1 = ['#2ecc71' if x > importance_df_1['Importance'].mean() else '#e74c3c' 
            for x in importance_df_1['Importance']]
ax1.barh(importance_df_1['Feature'], importance_df_1['Importance_%'], color=colors_1)
ax1.set_xlabel('Importance (%)', fontsize=11, fontweight='bold')
ax1.set_title('METHOD 1: Mean Decrease in Impurity\n(Built-in)', 
              fontsize=12, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)

# Plot 2: Permutation Importance
ax2 = axes[1]
colors_2 = ['#2ecc71' if x > importance_df_2['Importance'].mean() else '#e74c3c' 
            for x in importance_df_2['Importance']]
ax2.barh(importance_df_2['Feature'], importance_df_2['Importance_%'], 
         xerr=importance_df_2['Std_Dev'] / importance_df_2['Importance'].sum() * 100,
         color=colors_2, capsize=5)
ax2.set_xlabel('Importance (%)', fontsize=11, fontweight='bold')
ax2.set_title('METHOD 2: Permutation Importance\n(Recommended)', 
              fontsize=12, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(
    r'C:\Users\uimar\code\Githubfiles\ai-engineering\DSI\Day-28\feature_importance_comparison.png',
    dpi=300,
    bbox_inches='tight'
)
print("\n[OK] Comparison plot saved as 'feature_importance_comparison.png'")
plt.close()

# ============================================================================
# KEY INSIGHTS
# ============================================================================
print("\n" + "=" * 70)
print("KEY INSIGHTS & LEARNINGS")
print("=" * 70)

print("\n1. WHEN METHODS AGREE:")
print("   Both methods identified the same top features")
top_feature_method1 = importance_df_1.iloc[0]['Feature']
top_feature_method2 = importance_df_2.iloc[0]['Feature']
print(f"   Method 1 top feature: {top_feature_method1}")
print(f"   Method 2 top feature: {top_feature_method2}")

print("\n2. WHICH METHOD IS BETTER FOR STAKEHOLDERS?")
print("   [GOOD] Permutation Importance is easier to explain:")
print("     'When we scramble this feature, predictions get worse by X%'")
print("   [HARD] Impurity is harder to explain:")
print("     'This feature reduced Gini impurity by Y'")

print("\n3. PRACTICAL IMPLICATIONS:")
print(f"   - Focus on: {importance_df_2.iloc[0]['Feature']}, {importance_df_2.iloc[1]['Feature']}, {importance_df_2.iloc[2]['Feature']}")
print(f"   - These have the most impact on predictions")
print(f"   - De-prioritize: {importance_df_2.iloc[-1]['Feature']}, {importance_df_2.iloc[-2]['Feature']}")
print(f"   - These barely affect predictions")

print("\n[OK] Demo complete! Check the visualization for side-by-side comparison")
print("=" * 70)
