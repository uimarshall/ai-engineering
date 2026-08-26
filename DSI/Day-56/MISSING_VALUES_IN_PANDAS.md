# 📓 A Beginner's Guide to Missing Values in Pandas

## What Are Missing Values?

In real-world data, **missing values** are empty or unavailable data points. In pandas, these appear as:

- `NaN` (Not a Number) — for numeric columns
- `None` — for object/string columns
- `NaT` (Not a Time) — for datetime columns
- Sometimes empty strings `""` or placeholders like `"?"`, `"N/A"`, `0`, `-999`

---

## Why Do Missing Values Happen?

| Reason                           | Example                                                |
| -------------------------------- | ------------------------------------------------------ |
| **User didn't fill a field**     | A customer skipped "phone number" on a signup form     |
| **Data collection failure**      | A sensor went offline for 3 hours                      |
| **Merge/join mismatches**        | Combining two datasets where one lacks certain records |
| **Data corruption**              | A CSV import dropped some cells                        |
| **Intentionally not applicable** | "Spouse name" for a single person                      |

---

## 🔍 Detecting Missing Values

```python
import pandas as pd
import numpy as np

# Create sample data with missing values
df = pd.DataFrame({
    'customer_id': [101, 102, 103, 104, 105],
    'age': [25, np.nan, 30, 45, np.nan],
    'income': [50000, 60000, np.nan, 80000, 55000],
    'city': ['New York', 'Los Angeles', 'Chicago', None, 'Houston'],
    'purchased': ['Yes', 'No', 'Yes', 'No', 'Yes']
})

print(df)
```

Output:

```
   customer_id   age   income       city purchased
0          101  25.0  50000.0   New York       Yes
1          102   NaN  60000.0  Los Angeles       No
2          103  30.0      NaN    Chicago       Yes
3          104  45.0  80000.0       None        No
4          105   NaN  55000.0    Houston       Yes
```

### Methods to Detect Missing Values

```python
# 1. Check which cells are missing (True = missing)
print(df.isnull())

# 2. Count missing values per column
print(df.isnull().sum())

# 3. Total missing values in entire DataFrame
print(df.isnull().sum().sum())

# 4. Percentage of missing values per column
print((df.isnull().sum() / len(df)) * 100)

# 5. Show rows with ANY missing values
print(df[df.isnull().any(axis=1)])

# 6. Show rows with ALL values missing
print(df[df.isnull().all(axis=1)])
```

---

## 🛠️ Handling Missing Values

### Option 1: Remove Missing Data (Deletion)

**Best for:** When missing data is small (<5%) and random.

```python
# Drop rows with ANY missing values
df_clean = df.dropna()

# Drop rows where ALL values are missing
df_clean = df.dropna(how='all')

# Drop columns with more than 30% missing
threshold = 0.3
df_clean = df.dropna(thresh=len(df) * (1 - threshold), axis=1)

# Drop only specific columns
df_clean = df.dropna(subset=['age', 'income'])
```

> ⚠️ **Warning:** Dropping too much data can bias your analysis and reduce statistical power.

---

### Option 2: Fill Missing Values (Imputation)

**Best for:** When you want to preserve as much data as possible.

```python
# Fill with a constant value
df['age'] = df['age'].fillna(0)

# Fill with the mean (for numeric data)
df['age'] = df['age'].fillna(df['age'].mean())

# Fill with the median (better when outliers exist)
df['income'] = df['income'].fillna(df['income'].median())

# Fill with the mode (most frequent value — good for categorical)
df['city'] = df['city'].fillna(df['city'].mode()[0])

# Forward fill (use previous row's value) — great for time series
df['age'] = df['age'].ffill()

# Backward fill (use next row's value)
df['age'] = df['age'].bfill()

# Fill with a custom message
df['city'] = df['city'].fillna('Unknown')

# Fill different columns with different strategies
df['age'] = df['age'].fillna(df['age'].median())
df['income'] = df['income'].fillna(df['income'].mean())
df['city'] = df['city'].fillna('Unknown')
```

---

### Option 3: Advanced Imputation

```python
# Interpolation (estimates values based on neighbors)
df['temperature'] = df['temperature'].interpolate(method='linear')

# Group-based imputation (fill based on another category)
# Fill missing income with the average income of that city
df['income'] = df.groupby('city')['income'].transform(
    lambda x: x.fillna(x.mean())
)
```

---

## 🏢 Real-World Company Use Cases

### 1. **E-Commerce (Amazon, Shopify)**

- **Problem:** Customers abandon carts; product ratings are sparse
- **Business Impact:** Missing ratings make recommendation engines fail
- **Solution:** Use collaborative filtering or fill with product category averages
- **ML Relevance:** Recommender systems (Netflix, Amazon "You might also like") need complete user-item matrices. Missing values are predicted as ratings.

```python
# Example: Fill missing product ratings with category average
df['rating'] = df.groupby('category')['rating'].transform(
    lambda x: x.fillna(x.mean())
)
```

---

### 2. **Banking & Finance (JPMorgan, Capital One)**

- **Problem:** Loan applicants skip fields (e.g., "years at current job")
- **Business Impact:** Can't approve/reject loans without complete profiles
- **Solution:** Impute using similar customer segments; flag missing fields as a risk signal
- **ML Relevance:** Credit scoring models. A missing "income" field might itself be predictive of default risk!

```python
# Example: Flag missing values as a feature + impute
df['income_missing'] = df['income'].isnull().astype(int)  # New feature!
df['income'] = df['income'].fillna(df['income'].median())
```

---

### 3. **Healthcare (Epic Systems, Cerner)**

- **Problem:** Patient records have gaps (missed lab tests, unreadable handwriting)
- **Business Impact:** Incomplete data leads to wrong diagnoses or treatment delays
- **Solution:** Multiple imputation, domain-knowledge filling (e.g., normal ranges)
- **ML Relevance:** Disease prediction models. Missing lab values are often **not random** — sicker patients miss more tests. Ignoring this biases models.

```python
# Example: Fill blood pressure with normal range if test wasn't done
df['blood_pressure'] = df['blood_pressure'].fillna(120)  # Normal systolic
```

---

### 4. **Real Estate (Zillow, Redfin)**

- **Problem:** Property listings miss square footage, year built, or bedroom counts
- **Business Impact:** Price estimation models fail; bad valuations
- **Solution:** Impute from neighborhood averages or similar properties
- **ML Relevance:** Automated Valuation Models (AVMs). Missing "square footage" is filled using median of homes in same ZIP code.

```python
# Example: Fill missing sqft using neighborhood median
df['sqft'] = df.groupby('zip_code')['sqft'].transform(
    lambda x: x.fillna(x.median())
)
```

---

### 5. **Manufacturing & IoT (Siemens, GE)**

- **Problem:** Sensor data has gaps due to network failures
- **Business Impact:** Can't predict machine failures; production stops
- **Solution:** Time-series interpolation, forward-fill for short gaps
- **ML Relevance:** Predictive maintenance. Missing sensor readings are interpolated to maintain continuous monitoring.

```python
# Example: Time series interpolation for sensor data
df['sensor_temp'] = df['sensor_temp'].interpolate(method='time')
```

---

### 6. **Marketing & CRM (Salesforce, HubSpot)**

- **Problem:** Lead forms have optional fields (company size, job title)
- **Business Impact:** Incomplete lead scoring; poor targeting
- **Solution:** Fill with "Unknown" category; use email domain to infer company size
- **ML Relevance:** Lead scoring models. Missing job titles are categorized as "Unknown" — sometimes these leads convert differently!

```python
# Example: Categorize missing job titles
df['job_title'] = df['job_title'].fillna('Unknown')
df['job_title_category'] = df['job_title'].apply(
    lambda x: 'Executive' if 'CEO' in str(x) or 'CTO' in str(x) else 'Other'
)
```

---

## 🤖 Why Missing Values Matter for Machine Learning

| Issue                                   | Explanation                                                                                                                           |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Most ML algorithms can't handle NaN** | Scikit-learn models will throw errors if you pass NaN values                                                                          |
| **Bias in predictions**                 | If you drop rows with missing values, you might lose important patterns (e.g., high-income people are less likely to disclose income) |
| **Loss of information**                 | Deleting data reduces your training set size                                                                                          |
| **Feature engineering opportunity**     | "Is missing" can itself be a powerful predictive feature                                                                              |
| **Distorted statistics**                | Mean, correlation, and variance calculations are wrong with missing data                                                              |

---

## ✅ Best Practices Checklist

```
□ Always check for missing values first: df.isnull().sum()
□ Understand WHY data is missing (random or systematic?)
□ Never blindly drop rows — check how much data you lose
□ Document your imputation strategy
□ Create a "_missing" flag column before filling
□ Use different strategies for different data types:
    - Numeric → mean, median, or model-based imputation
    - Categorical → mode or "Unknown"
    - Time series → interpolation or forward-fill
□ Validate: Compare model performance with different strategies
```

---

## 🧪 Complete Working Example

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Sample customer churn dataset with missing values
df = pd.DataFrame({
    'customer_id': range(1, 11),
    'tenure_months': [12, 24, np.nan, 36, 6, 18, np.nan, 48, 3, 60],
    'monthly_charges': [29.85, 56.95, 53.85, np.nan, 42.30, 70.70,
                        89.10, 104.65, 20.15, np.nan],
    'contract_type': ['Month-to-month', 'One year', 'Month-to-month',
                      'Two year', np.nan, 'One year', 'Month-to-month',
                      'Two year', 'Month-to-month', 'Two year'],
    'churn': ['No', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No']
})

print("=== Original Data ===")
print(df)
print(f"
Missing values:
{df.isnull().sum()}")

# Step 1: Create missing indicator features
df['tenure_missing'] = df['tenure_months'].isnull().astype(int)
df['charges_missing'] = df['monthly_charges'].isnull().astype(int)

# Step 2: Impute missing values
df['tenure_months'] = df['tenure_months'].fillna(df['tenure_months'].median())
df['monthly_charges'] = df['monthly_charges'].fillna(df['monthly_charges'].mean())
df['contract_type'] = df['contract_type'].fillna('Unknown')

# Step 3: Encode categorical variables
df_encoded = pd.get_dummies(df, columns=['contract_type'], drop_first=True)

# Step 4: Prepare for ML
X = df_encoded.drop(['customer_id', 'churn'], axis=1)
y = df_encoded['churn'].map({'Yes': 1, 'No': 0})

# Step 5: Train a simple model
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

print(f"
=== Model Accuracy: {accuracy_score(y_test, predictions):.2f} ===")
print("
=== Cleaned Data ===")
print(df)
```

---

## 🎯 Key Takeaway

> **Missing values are not just holes in your data — they are signals.**  
> Whether you fill them, flag them, or remove them, always understand _why_ they're missing and _how_ your choice affects both business decisions and machine learning models. The "missingness" itself often tells a story! 📖
