# Machine Learning Pipeline - Complete Beginner's Guide

## 📚 Table of Contents

1. [What is a Pipeline?](#what-is-a-pipeline)
2. [Module Imports & Their Roles](#module-imports--their-roles)
3. [Data Preparation](#data-preparation)
4. [Data Transformers](#data-transformers)
5. [Building Models](#building-models)
6. [Training & Evaluation](#training--evaluation)
7. [Saving & Loading Models](#saving--loading-models)
8. [Complete Workflow Summary](#complete-workflow-summary)

---

## What is a Pipeline?

### Simple Definition

A **pipeline** is like an assembly line in a factory:

- **Input**: Raw materials (messy data)
- **Processing**: Multiple stations (transformers)
- **Output**: Finished products (predictions)

### Why Use Pipelines?

1. **Automation**: Preprocessing happens automatically
2. **Consistency**: Training and prediction use identical transformations
3. **Prevents Data Leakage**: Test data isn't used during preprocessing
4. **Reproducibility**: Same results every time you run
5. **Production-Ready**: Easy to save and reuse

### Real-World Analogy

```
Raw Coffee Beans → Roast → Grind → Brew → Serve Coffee
Raw Data → Impute → Scale → Encode → Train Model → Predict
```

---

## Module Imports & Their Roles

### 1. **pandas** (`import pandas as pd`)

**What it does**: Works with tabular data (like Excel spreadsheets)

**Key functions**:

- `pd.read_csv()` - Loads CSV files into a DataFrame
- DataFrame - A 2D table with rows and columns

**Example**:

```python
import pandas as pd
my_df = pd.read_csv("data.csv")  # Load data
X = my_df.drop(["target"], axis=1)  # Remove target column
y = my_df["target"]  # Extract target column
```

### 2. **numpy** (`import numpy as np`)

**What it does**: Mathematical and numerical operations

**Key features**:

- Arrays (like lists, optimized for math)
- NaN (np.nan) - represents missing values
- Mathematical functions

**Example**:

```python
import numpy as np
arr = np.array([1, 2, 3, np.nan, 5])  # Array with missing value
```

### 3. **sklearn.pipeline.Pipeline**

**What it does**: Chains multiple transformers together

**Real analogy**: Recipe with multiple steps

**Example**:

```python
from sklearn.pipeline import Pipeline
pipeline = Pipeline(steps=[
    ("step1", Transformer1()),
    ("step2", Transformer2()),
    ("step3", Model())
])
```

### 4. **sklearn.compose.ColumnTransformer**

**What it does**: Applies different transformations to different columns

**Why needed?**

- Numeric columns need scaling
- Categorical columns need encoding
- Can't use same transformation for both!

**Example**:

```python
from sklearn.compose import ColumnTransformer
ct = ColumnTransformer(transformers=[
    ("numeric", numeric_pipeline, ["age", "income"]),
    ("categorical", categorical_pipeline, ["gender", "city"])
])
```

### 5. **sklearn.model_selection.train_test_split**

**What it does**: Splits data into training and testing portions

**Parameters**:

- `test_size=0.2` → 20% for testing, 80% for training
- `random_state=42` → Makes split reproducible
- `stratify=y` → Maintains class balance

**Why important?** Never test on data used for training!

**Example**:

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

### 6. **sklearn.impute.SimpleImputer**

**What it does**: Handles missing values (NaN, empty cells)

**Strategies**:

- `strategy='mean'` → Fill with average (for numbers)
- `strategy='median'` → Fill with middle value
- `strategy='constant'` → Fill with specific value

**Example**:

```python
from sklearn.impute import SimpleImputer
# For numeric data
imputer = SimpleImputer(strategy='mean')

# For categorical data
imputer_cat = SimpleImputer(strategy='constant', fill_value='Unknown')
```

**Before & After**:

```
Before: [25, NaN, 35, 40]
After:  [25, 33.33, 35, 40]  # NaN filled with mean (25+35+40)/3
```

### 7. **sklearn.preprocessing.StandardScaler**

**What it does**: Scales numbers to have mean=0 and std=1

**Formula**: `(value - mean) / standard_deviation`

**Why needed?** Algorithms like Logistic Regression prefer similar-scale numbers

**Example**:

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

# Before: [10, 50, 100] (wide range)
# After: [-1.22, -0.38, 1.60] (standardized)
```

### 8. **sklearn.preprocessing.OneHotEncoder**

**What it does**: Converts categories to numbers

**Process**:

```
Input:  ["Red", "Green", "Blue"]
        ["Red", "Green", "Red"]

Output (One-Hot Encoding):
        Red: [1, 0, 0]
        Green: [0, 1, 0]
        Blue: [0, 0, 1]
        Red: [1, 0, 0]
```

**Why needed?** Machine learning algorithms understand numbers, not text

**Parameters**:

- `handle_unknown='ignore'` → Don't crash if new category appears

### 9. **sklearn.linear_model.LogisticRegression**

**What it does**: Classification algorithm that predicts probabilities

**Output**: Values between 0 and 1

- 0.2 = 20% confidence of "Yes"
- 0.8 = 80% confidence of "Yes"

**Pros**: Fast, interpretable, works well for binary classification

### 10. **sklearn.ensemble.RandomForestClassifier**

**What it does**: Uses multiple decision trees, combines predictions

**How it works**:

1. Creates 100 decision trees (by default)
2. Each tree makes a prediction
3. Combines predictions (voting)
4. Final answer = most voted prediction

**Pros**: More accurate than single models, handles missing data well

### 11. **sklearn.metrics.accuracy_score**

**What it does**: Measures how many predictions are correct

**Formula**: `Correct Predictions / Total Predictions`

**Example**:

```
95 correct out of 100 = 0.95 (95% accuracy)
```

### 12. **joblib**

**What it does**: Saves and loads Python objects (especially ML models)

**Why needed?** Training takes time; save and reuse!

**Functions**:

- `joblib.dump(model, filepath)` → Save model
- `joblib.load(filepath)` → Load model

---

## Data Preparation

### Step 1: Load Data

```python
import pandas as pd
my_df = pd.read_csv("data/pipeline_data.csv")
# Result: DataFrame with all rows and columns
```

### Step 2: Separate Features and Target

```python
X = my_df.drop(["purchase"], axis=1)  # Features (input)
y = my_df["purchase"]                  # Target (output)
```

**Analogy**:

```
House Prediction Example:
X = [size, rooms, location]  (what we know)
y = [price]                  (what we predict)
```

### Step 3: Split into Train and Test

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

**Split Distribution**:

```
Original Data (100 samples)
├─ Training (80 samples) → Model learns
└─ Testing (20 samples)  → Model is evaluated
```

### Step 4: Identify Feature Types

```python
numeric_features = ["age", "credit_score"]      # Numbers
categorical_features = ["gender"]                # Text/Categories
```

---

## Data Transformers

### Numeric Transformer Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer()),           # Fill missing
    ("scaler", StandardScaler())            # Scale to standard range
])
```

**Visual Example**:

```
Input:  [25, NaN, 35, 100]
        ↓ (Impute)
        [25, 33.33, 35, 100]
        ↓ (Scale)
        [-1.2, -0.8, -0.5, 2.5]
```

### Categorical Transformer Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="constant", fill_value="U")),
    ("ohe", OneHotEncoder(handle_unknown="ignore"))
])
```

**Visual Example**:

```
Input:  ["M", "F", NaN, "M"]
        ↓ (Impute with "U")
        ["M", "F", "U", "M"]
        ↓ (One-Hot Encode)
        [[1,0,0], [0,1,0], [0,0,1], [1,0,0]]
```

### Column Transformer

```python
from sklearn.compose import ColumnTransformer

preprocessing_pipeline = ColumnTransformer(transformers=[
    ("numeric", numeric_transformer, numeric_features),
    ("categorical", categorical_transformer, categorical_features)
])
```

**What happens**:

```
Original Data
├─ Numeric columns → numeric_transformer
└─ Categorical columns → categorical_transformer
                ↓
            Preprocessed Data
```

---

## Building Models

### Model 1: Logistic Regression

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

clf = Pipeline(steps=[
    ("preprocessing", preprocessing_pipeline),
    ("classifier", LogisticRegression(random_state=42))
])
```

**Advantages**:

- Fast to train
- Easy to understand
- Works well for yes/no decisions

**Disadvantages**:

- Less accurate on complex patterns
- Assumes linear relationship

### Model 2: Random Forest

```python
from sklearn.ensemble import RandomForestClassifier

clf_rf = Pipeline(steps=[
    ("preprocessing", preprocessing_pipeline),
    ("classifier", RandomForestClassifier(random_state=42))
])
```

**Advantages**:

- More accurate
- Handles non-linear patterns
- Robust to outliers

**Disadvantages**:

- Slower
- Harder to interpret

---

## Training & Evaluation

### Training

```python
clf.fit(X_train, y_train)
```

**What happens internally**:

```
X_train → Preprocessing Pipeline → Preprocessed X_train
                                         ↓
                                    LogisticRegression learns
                                         ↓
                                    Model is trained
```

### Making Predictions

```python
y_pred = clf.predict(X_test)
```

**Process**:

```
X_test → Same Preprocessing → Preprocessed X_test
                                    ↓
                            Trained Model predicts
                                    ↓
                                y_pred = [0, 1, 0, ...]
```

### Evaluation

```python
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2%}")  # 85.50%
```

---

## Saving & Loading Models

### Save Model

```python
import joblib
joblib.dump(clf, "data/model.joblib")
# Creates a file containing:
# - Preprocessing rules (mean, std, categories)
# - Trained model weights
```

### Load Saved Model

```python
import joblib
clf_loaded = joblib.load("data/model.joblib")
```

### Use on New Data

```python
import pandas as pd
import numpy as np

new_data = pd.DataFrame({
    "age": [25, np.nan, 50],
    "gender": ["M", "F", np.nan],
    "credit_score": [200, 100, 500]
})

predictions = clf_loaded.predict(new_data)
# Automatically handles:
# - Missing values (imputation)
# - Scaling (for numeric)
# - Encoding (for categorical)
```

### Get Prediction Confidence

```python
probabilities = clf_loaded.predict_proba(new_data)
# Output: [[0.2, 0.8], [0.6, 0.4], [0.1, 0.9]]
# Interpretation: 80%, 40%, 90% confidence respectively
```

---

## Complete Workflow Summary

### Visual Flow

```
┌─────────────────────────────────────────────┐
│ 1. LOAD DATA                                │
│    read_csv() → DataFrame                   │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 2. PREPARE DATA                             │
│    - Split into X (features) & y (target)   │
│    - Split into train (80%) & test (20%)    │
│    - Identify numeric vs categorical        │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 3. CREATE TRANSFORMERS                      │
│    - Numeric: Impute + Scale                │
│    - Categorical: Impute + Encode           │
│    - Combine: ColumnTransformer             │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 4. BUILD PIPELINES (Models)                 │
│    Option A: Logistic Regression (fast)     │
│    Option B: Random Forest (accurate)       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 5. TRAIN MODELS                             │
│    model.fit(X_train, y_train)              │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 6. EVALUATE MODELS                          │
│    model.predict(X_test)                    │
│    accuracy_score(y_test, predictions)      │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 7. SAVE MODEL                               │
│    joblib.dump(model, filepath)             │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 8. LOAD & USE MODEL                         │
│    model = joblib.load(filepath)            │
│    predictions = model.predict(new_data)    │
└─────────────────────────────────────────────┘
```

### Code Template

```python
# 1. Load
import pandas as pd
df = pd.read_csv("data.csv")

# 2. Prepare
X, y = df.drop(["target"], axis=1), df["target"]
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 3-4. Transform & Build
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
# ... create transformers and pipelines ...

# 5. Train
model.fit(X_train, y_train)

# 6. Evaluate
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, model.predict(X_test)))

# 7. Save
import joblib
joblib.dump(model, "model.joblib")

# 8. Use
model_loaded = joblib.load("model.joblib")
print(model_loaded.predict(new_data))
```

---

## Key Takeaways

1. **Pipelines automate preprocessing** - No manual steps needed
2. **Always split data** - Train on different data than you test on
3. **Different data types need different treatment** - Numbers vs categories
4. **Simple models first** - Start with Logistic Regression, try Random Forest if needed
5. **Always evaluate on test data** - Never evaluate on training data
6. **Save your models** - Reuse without retraining
7. **Handle missing values** - Don't ignore them, impute them
8. **Scale your numbers** - Similar ranges help algorithms learn better

---

## Common Mistakes to Avoid

❌ **Don't**: Evaluate model on training data
✅ **Do**: Use separate test data for evaluation

❌ **Don't**: Use different preprocessing for train and test
✅ **Do**: Use pipeline for consistency

❌ **Don't**: Leave missing values unhandled
✅ **Do**: Use SimpleImputer to fill them

❌ **Don't**: Mix numeric and categorical features
✅ **Do**: Apply different transformations with ColumnTransformer

❌ **Don't**: Train and test on same data
✅ **Do**: Split with train_test_split()
