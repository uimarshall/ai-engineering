# 🐼 Dealing with Duplicate Data in Pandas: A Beginner's Guide

> **Why this matters:** Clean data is the foundation of every great analysis and machine learning model. Duplicates and outliers are like weeds in a garden — they choke out the good stuff if you don't handle them.

---

## 📌 Table of Contents

1. [What Are Duplicates?](#what-are-duplicates)
2. [Finding Duplicates in Pandas](#finding-duplicates)
3. [Removing Duplicates](#removing-duplicates)
4. [How Duplicates Affect Machine Learning](#duplicates-and-ml)
5. [Real-World Company Use Cases](#company-use-cases)
6. [What About Outliers?](#what-about-outliers)
7. [Detecting Outliers in Pandas](#detecting-outliers)
8. [Handling Outliers](#handling-outliers)
9. [Best Practices Cheat Sheet](#best-practices)

---

## 1. What Are Duplicates? {#what-are-duplicates}

**Duplicate rows** are rows in your dataset that are exact copies of one another (or copies based on specific columns). They can sneak in from:

- Merging multiple data sources
- Data entry errors
- System glitches
- Web scraping
- Customer re-submissions

### Example of Duplicate Data

| customer_id | name    | email             | purchase_amount |
| ----------- | ------- | ----------------- | --------------- | ------------ |
| 101         | Alice   | alice@email.com   | 120.00          |
| 102         | Bob     | bob@email.com     | 85.50           |
| 101         | Alice   | alice@email.com   | 120.00          | ← Duplicate! |
| 103         | Charlie | charlie@email.com | 200.00          |

---

## 2. Finding Duplicates in Pandas {#finding-duplicates}

```python
import pandas as pd

# Sample data
data = {
    'customer_id': [101, 102, 101, 103],
    'name': ['Alice', 'Bob', 'Alice', 'Charlie'],
    'email': ['alice@email.com', 'bob@email.com', 'alice@email.com', 'charlie@email.com'],
    'purchase_amount': [120.00, 85.50, 120.00, 200.00]
}

df = pd.DataFrame(data)

# Check for duplicate rows (all columns must match)
print(df.duplicated())
# Output: [False, False, True, False]

# Check for duplicates based on specific columns
print(df.duplicated(subset=['customer_id', 'email']))

# Count total duplicates
duplicate_count = df.duplicated().sum()
print(f"Total duplicates: {duplicate_count}")

# View all duplicate rows
duplicates = df[df.duplicated(keep=False)]
print(duplicates)
```

### Key Parameters of `.duplicated()`

| Parameter | Description                                                       | Default     |
| --------- | ----------------------------------------------------------------- | ----------- |
| `subset`  | Columns to check for duplicates                                   | All columns |
| `keep`    | Which duplicate to mark as `False` (`'first'`, `'last'`, `False`) | `'first'`   |

---

## 3. Removing Duplicates {#removing-duplicates}

```python
# Remove duplicates (keeps first occurrence by default)
df_clean = df.drop_duplicates()

# Keep the last occurrence instead
df_clean = df.drop_duplicates(keep='last')

# Remove ALL duplicates (even the first one!)
df_no_duplicates = df.drop_duplicates(keep=False)

# Remove duplicates based on specific columns
df_clean = df.drop_duplicates(subset=['customer_id'])

# Remove duplicates and reset index
df_clean = df.drop_duplicates().reset_index(drop=True)

# In-place removal (modifies original DataFrame)
df.drop_duplicates(inplace=True)
```

### ⚠️ Important: Always Inspect Before Deleting!

```python
# See what you'll delete BEFORE deleting it
rows_to_drop = df[df.duplicated(keep='first')]
print(f"About to remove {len(rows_to_drop)} rows")
print(rows_to_drop)
```

---

## 4. How Duplicates Affect Machine Learning {#duplicates-and-ml}

### 🚨 The Hidden Danger

Duplicates can silently destroy your ML models. Here's why:

#### 1. **Data Leakage (The Silent Killer)**

When duplicates exist across train and test splits, your model "cheats" by seeing the same data twice. It gives you unrealistically high accuracy that crashes in production.

```python
# BAD: Duplicates leak from train to test
from sklearn.model_selection import train_test_split

# If row #5 and row #100 are duplicates...
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# Row #5 might be in train, row #100 in test → model already "knows" the answer!
```

#### 2. **Biased Training**

If duplicates are more common for certain classes, your model learns to favor those classes.

```python
# Example: Fraud detection dataset
# 1000 rows total, but 200 are duplicates of the same fraud case
# Your model thinks fraud is more common than it really is
```

#### 3. **Overfitting**

The model memorizes repeated patterns instead of learning general rules.

#### 4. **Inflated Performance Metrics**

Your accuracy, precision, and recall look great on paper but fail in the real world.

#### 5. **Wasted Compute**

Training on duplicate data = longer training times + higher cloud costs 💸

### ✅ Best Practice for ML

```python
# ALWAYS remove duplicates BEFORE splitting data!
df = df.drop_duplicates()

# Then split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

---

## 5. Real-World Company Use Cases {#company-use-cases}

### 🏦 **Use Case 1: Banking & Finance — Fraud Detection**

**Company:** A major retail bank

**Problem:** Transaction logs had duplicate entries due to retry mechanisms in payment processing. A single fraudulent transaction appeared 3-4 times.

**Impact on Business:**

- Fraud detection model flagged legitimate customers as high-risk (false positives)
- Customer complaints increased by 40%
- Compliance team wasted hours investigating phantom transactions

**Solution:**

```python
# Remove duplicates based on transaction_id + timestamp
transactions = transactions.drop_duplicates(
    subset=['transaction_id', 'timestamp', 'amount'],
    keep='first'
)
```

**Result:** False positives dropped by 35%, saving ~$2M annually in manual review costs.

---

### 🛒 **Use Case 2: E-Commerce — Customer Analytics**

**Company:** A global online marketplace

**Problem:** Customer database had duplicate profiles because users registered with different emails but the same phone number.

**Impact on Business:**

- Marketing emails sent multiple times to the same person → unsubscribes
- Customer Lifetime Value (CLV) calculations were inflated
- Recommendation engine suggested products the customer already bought

**Solution:**

```python
# Merge duplicates using phone number as the key
df = df.sort_values('registration_date')  # Keep oldest profile
df = df.drop_duplicates(subset=['phone_number'], keep='first')
```

**Result:** Email unsubscribe rate dropped by 22%. CLV predictions became 18% more accurate.

---

### 🏥 **Use Case 3: Healthcare — Patient Records**

**Company:** A hospital network

**Problem:** Patient records were duplicated when transferred between hospital systems. The same patient had 3-4 different IDs.

**Impact on Business:**

- Duplicate billing caused insurance claim rejections
- Doctors couldn't see complete medical history
- ML model for readmission risk gave wrong predictions

**Solution:**

```python
# Deduplicate using patient name + date_of_birth
df = df.drop_duplicates(
    subset=['first_name', 'last_name', 'date_of_birth'],
    keep='first'
)
```

**Result:** Billing errors reduced by 60%. Readmission prediction accuracy improved by 12%.

---

### 📊 **Use Case 4: SaaS — User Analytics & A/B Testing**

**Company:** A B2B software platform

**Problem:** Event tracking fired multiple times per user action (page load, button click). A/B test results were skewed.

**Impact on Business:**

- Wrong features shipped because A/B tests showed false improvements
- Product team made decisions based on inflated engagement metrics

**Solution:**

```python
# Deduplicate events within a time window
events = events.drop_duplicates(
    subset=['user_id', 'event_type', 'session_id'],
    keep='first'
)
```

**Result:** A/B test reliability improved. The company avoided shipping a feature that would have actually decreased conversion by 5%.

---

## 6. What About Outliers? {#what-about-outliers}

**Outliers** are data points that are significantly different from other observations. They can be:

- **Natural:** A genuine extreme value (e.g., a billionaire's net worth)
- **Error:** A data entry mistake (e.g., age = 250 years)

### Visual: Outliers in a Dataset

```
Normal Data:    ●  ●   ● ●    ●    ●  ●
Outlier:                              ★

Value:    0----10----20----30----40----500
```

### Why Outliers Matter

| Scenario                           | Effect                                        |
| ---------------------------------- | --------------------------------------------- |
| Calculating average salary         | One CEO earning $50M makes everyone look rich |
| Training a linear regression model | Outliers pull the line in their direction     |
| Fraud detection                    | Outliers ARE the fraud — don't remove them!   |

---

## 7. Detecting Outliers in Pandas {#detecting-outliers}

### Method 1: Statistical (Z-Score)

```python
from scipy import stats
import numpy as np

# Z-Score: How many standard deviations away from the mean?
df['z_score'] = np.abs(stats.zscore(df['purchase_amount']))

# Flag values where |z| > 3 (99.7% of data falls within 3 std devs)
outliers = df[df['z_score'] > 3]
print(outliers)
```

### Method 2: Interquartile Range (IQR)

```python
# IQR Method (more robust to outliers than Z-score)
Q1 = df['purchase_amount'].quantile(0.25)
Q3 = df['purchase_amount'].quantile(0.75)
IQR = Q3 - Q1

# Define bounds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Find outliers
outliers = df[(df['purchase_amount'] < lower_bound) |
              (df['purchase_amount'] > upper_bound)]

print(f"Lower bound: {lower_bound}")
print(f"Upper bound: {upper_bound}")
print(f"Outliers found: {len(outliers)}")
```

### Method 3: Visual Detection

```python
import matplotlib.pyplot as plt

# Box plot (shows outliers as dots beyond the whiskers)
df['purchase_amount'].plot(kind='box')
plt.title('Box Plot — Outlier Detection')
plt.show()

# Histogram
 df['purchase_amount'].plot(kind='hist', bins=50)
plt.title('Distribution — Look for the long tail!')
plt.show()
```

### Method 4: Percentile-Based

```python
# Simple percentile cutoffs
lower = df['purchase_amount'].quantile(0.01)  # Bottom 1%
upper = df['purchase_amount'].quantile(0.99)  # Top 1%

outliers = df[(df['purchase_amount'] < lower) |
              (df['purchase_amount'] > upper)]
```

---

## 8. Handling Outliers {#handling-outliers}

### Strategy 1: Remove Them

```python
# Using IQR method
Q1 = df['purchase_amount'].quantile(0.25)
Q3 = df['purchase_amount'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Keep only non-outliers
df_clean = df[(df['purchase_amount'] >= lower_bound) &
              (df['purchase_amount'] <= upper_bound)]
```

### Strategy 2: Cap Them (Winsorization)

```python
# Instead of removing, cap at percentiles
df['purchase_amount_capped'] = df['purchase_amount'].clip(
    lower=df['purchase_amount'].quantile(0.05),
    upper=df['purchase_amount'].quantile(0.95)
)
```

### Strategy 3: Transform Them

```python
# Log transformation reduces the impact of extreme values
import numpy as np

df['purchase_amount_log'] = np.log1p(df['purchase_amount'])
# log1p = log(1 + x), handles zeros safely
```

### Strategy 4: Keep Them (But Flag Them)

```python
# Sometimes outliers are valuable!
df['is_outlier'] = ((df['purchase_amount'] < lower_bound) |
                    (df['purchase_amount'] > upper_bound))

# Now your ML model can learn from the outlier flag
```

### ⚠️ When NOT to Remove Outliers

| Domain            | Why Keep Outliers?                   |
| ----------------- | ------------------------------------ |
| Fraud Detection   | Fraud IS an outlier                  |
| Network Security  | Attacks are rare but critical        |
| Medical Diagnosis | Rare diseases need detection         |
| Finance           | Market crashes are outliers but real |

---

## 9. Best Practices Cheat Sheet {#best-practices}

### For Duplicates

```python
# ✅ DO THIS
# 1. Always check for duplicates first
print(f"Duplicates: {df.duplicated().sum()}")

# 2. Inspect before dropping
print(df[df.duplicated(keep=False)].sort_values('customer_id'))

# 3. Drop duplicates BEFORE train/test split
df = df.drop_duplicates()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 4. Use subset when only certain columns matter
df = df.drop_duplicates(subset=['user_id', 'session_id'])

# ❌ DON'T DO THIS
# Don't drop duplicates blindly without inspecting
# Don't forget to reset_index after dropping
# Don't drop duplicates AFTER splitting (causes data leakage!)
```

### For Outliers

```python
# ✅ DO THIS
# 1. Always visualize first
 df['column'].plot(kind='box')

# 2. Understand the domain before removing
# In fraud detection: outliers = gold!

# 3. Document your decisions
# "Removed values > 3 std devs from mean in 'age' column"

# 4. Consider capping instead of removing
 df['column'] = df['column'].clip(lower, upper)

# ❌ DON'T DO THIS
# Don't remove outliers without understanding why they exist
# Don't use the same threshold for every column
# Don't forget that some models (tree-based) handle outliers naturally
```

---

## 🎯 Quick Reference: Duplicates vs. Outliers

| Aspect           | Duplicates                | Outliers                           |
| ---------------- | ------------------------- | ---------------------------------- |
| **What**         | Exact copies of rows      | Extreme values                     |
| **Detection**    | `.duplicated()`           | Z-score, IQR, visualization        |
| **Fix**          | `.drop_duplicates()`      | Remove, cap, transform, or flag    |
| **ML Impact**    | Data leakage, overfitting | Biased models, poor generalization |
| **When to Keep** | Never (in ML)             | Fraud, rare events, anomalies      |

---

## 📝 Summary

1. **Duplicates** are exact copies that cause data leakage in ML and skew business metrics. Always remove them _before_ splitting data for ML.

2. **Outliers** are extreme values that can distort analysis. Handle them carefully — sometimes they're errors, sometimes they're the most important data points.

3. **Always inspect first.** Never blindly drop data. Understand _why_ duplicates and outliers exist in your specific dataset.

4. **Document everything.** Your future self (and your team) will thank you.

---

> 💡 **Pro Tip:** Data cleaning takes 60-80% of a data scientist's time. Mastering duplicates and outliers early puts you ahead of 90% of beginners.

_Happy cleaning! 🧹_
