############################################################
# MACHINE LEARNING PIPELINE - DETAILED EXPLANATION
# A Complete Guide to Building, Training, and Using ML Pipelines
############################################################

"""
WHAT IS A PIPELINE?
A pipeline is like an assembly line in a factory. Raw materials (data) go in,
get processed through different stages, and come out as finished products (predictions).
In machine learning, it automates data preprocessing and model training.
"""

# ============================================================
# SECTION 1: IMPORTING REQUIRED MODULES
# ============================================================

"""
A module is a file that contains reusable Python code.
We import modules to use pre-built functions and classes.
Think of it like importing tools to your workshop.
"""

# NUMPY LIBRARY
# Purpose: Used for numerical computing and working with arrays
# (arrays are like lists but optimized for math operations)
# 'np' is a shorter alias for numpy
import numpy as np

# PANDAS LIBRARY
# Purpose: Used for working with data in table format (like Excel spreadsheets)
# 'pd' is a shorter alias we use instead of writing 'pandas' every time
import pandas as pd

# SCIKIT-LEARN: ColumnTransformer
# Purpose: Applies different transformations to different columns
# Example: Some columns might need number scaling, others need text encoding
from sklearn.compose import ColumnTransformer

# SCIKIT-LEARN: RandomForestClassifier
# Purpose: Uses multiple decision trees to make predictions (ensemble method)
# Better accuracy than single models; handles both numbers and categories well
from sklearn.ensemble import RandomForestClassifier

# SCIKIT-LEARN: SimpleImputer
# Purpose: Handles missing values (e.g., empty cells in your data)
# Strategy: fills empty cells with average, median, or a constant value
from sklearn.impute import SimpleImputer

# SCIKIT-LEARN: LogisticRegression
# Purpose: A classification algorithm that predicts YES/NO or category outcomes
# "Logistic" = works well for binary/multi-class classification problems
from sklearn.linear_model import LogisticRegression

# SCIKIT-LEARN: accuracy_score
# Purpose: Calculates how many predictions were correct
# Formula: (correct predictions / total predictions) × 100%
from sklearn.metrics import accuracy_score

# SCIKIT-LEARN: train_test_split
# Purpose: Splits your data into training and testing portions
# Training data = data the model learns from
# Testing data = data we use to verify the model works on new data
from sklearn.model_selection import train_test_split

# SCIKIT-LEARN: Pipeline
# Purpose: Creates automated workflows that combine data preprocessing and model training
# This prevents mistakes and makes code cleaner
from sklearn.pipeline import Pipeline

# SCIKIT-LEARN: OneHotEncoder
# Purpose: Converts text categories into numbers that algorithms can understand
# Example: "Red", "Green", "Blue" becomes [1,0,0], [0,1,0], [0,0,1]
# SCIKIT-LEARN: StandardScaler
# Purpose: Scales numbers to have a similar range (usually -1 to 1 or 0 to 1)
# Why? Some algorithms work better when numbers are on similar scales
# Example: Converting age (0-100) and salary (0-1,000,000) to comparable scales
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# JOBLIB LIBRARY (imported later)
# Purpose: Saves and loads machine learning models to/from files
# Use case: Train a model once, save it, use it many times without retraining


# ============================================================
# SECTION 2: LOADING THE DATA
# ============================================================

"""
Every machine learning project starts with data.
We need to load data from a file and convert it to a format Python can work with.
"""

# Read CSV file (Comma-Separated Values)
# CSV is like an Excel spreadsheet saved as text
# pd.read_csv() loads the file into a pandas DataFrame (table-like structure)
# "my_df" stands for "my dataframe"

my_df = pd.read_csv("data/pipeline_data.csv")

# At this point, my_df contains all your data in a table format
# Each row = one data sample
# Each column = one feature (like age, gender, credit_score, purchase)


# ============================================================
# SECTION 3: SEPARATING FEATURES (X) AND TARGET (y)
# ============================================================

"""
FEATURES (X): Input variables - what we know about the data
Example: age, gender, credit_score

TARGET (y): Output variable - what we want to predict
Example: purchase (did they buy or not?)

WHY SEPARATE THEM?
Machine learning algorithms need inputs (X) and outputs (y) separate.
The model learns the relationship: X → y
"""

# DROP: Remove a column from the dataframe
# axis=1 means "remove by column name" (axis=0 would mean remove by row)
# We drop "purchase" because that's what we want to PREDICT (the target)
# X contains: age, gender, credit_score (everything except purchase)

X = my_df.drop(["purchase"], axis=1)

# Extract the "purchase" column into y
# y contains only the target values we want to predict
# The double brackets ["purchase"] return a DataFrame;
# without brackets my_df["purchase"] returns a Series (1D array)

y = my_df["purchase"]


# ============================================================
# SECTION 4: SPLITTING DATA INTO TRAINING AND TESTING
# ============================================================

"""
WHY SPLIT DATA?
Imagine studying for a test using the same practice problems that will be on the test.
You'd memorize answers instead of learning concepts.
Same principle: we need unseen data to truly test the model.

TRAIN: Model learns patterns from this data (80% in this case)
TEST: We verify the model works on new data it hasn't seen (20% in this case)
"""

# train_test_split() divides data into training and testing sets
# Parameters explanation:
#   X, y: The features and target to split
#   test_size=0.2: Use 20% for testing, 80% for training
#   random_state=42: Seed value for reproducibility
#                    (same seed = same split every time you run the code)
#   stratify=y: Ensures both train/test have same proportion of each class
#              Example: If 70% of data is "purchase=Yes",
#              both train and test will have ~70% "Yes"

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,  # 20% for testing
    random_state=42,  # Makes results reproducible
    stratify=y,  # Maintains class balance
)

# After split, we have 4 datasets:
# X_train: features for training (80% of original X)
# y_train: targets for training (80% of original y)
# X_test: features for testing (20% of original X)
# y_test: targets for testing (20% of original y)


# ============================================================
# SECTION 5: IDENTIFYING NUMERIC VS CATEGORICAL FEATURES
# ============================================================

"""
NUMERIC FEATURES: Numbers that represent quantities
Examples: age (20, 30, 50), credit_score (200, 500, 800)
These need scaling (making numbers comparable in magnitude)

CATEGORICAL FEATURES: Text/categories that represent groups
Examples: gender ("M", "F"), city ("NYC", "LA", "Boston")
These need encoding (converting text to numbers)
"""

# List of numeric column names
# These columns contain numbers (integers or decimals)
numeric_features = ["age", "credit_score"]

# List of categorical column names
# These columns contain text/categories
categorical_features = ["gender"]

# Why list them?
# So we can apply different transformations to each type
# Numeric columns → missing value handling + scaling
# Categorical columns → missing value handling + encoding


# ============================================================
# SECTION 6: SETTING UP TRANSFORMERS (DATA PREPROCESSING)
# ============================================================

"""
TRANSFORMER: A tool that changes (transforms) data
PIPELINE: A chain of transformers that work together

Think of it like a car wash:
1. Rinse (SimpleImputer handles missing values)
2. Soap (StandardScaler or OneHotEncoder transforms the data)
3. Dry (output is ready for the model)
"""

# --- NUMERIC TRANSFORMER (for numeric_features) ---

"""
Purpose: Prepare numeric columns for machine learning

Two steps:
1. Impute missing values: If data is missing (NaN/null), fill it with a value
2. Scale: Convert numbers to a standard range for better model performance
"""

numeric_transformer = Pipeline(
    steps=[
        # Step 1: IMPUTER
        # SimpleImputer() fills missing values (NaN) with mean by default
        # Example: If ages are [25, NaN, 35], it fills NaN with (25+35)/2 = 30
        # Default strategy='mean' works well for numbers
        ("imputer", SimpleImputer()),
        # Step 2: SCALER
        # StandardScaler() rescales numbers to mean=0 and standard deviation=1
        # Formula: (value - mean) / standard_deviation
        # Why? Algorithms like Logistic Regression work better with scaled numbers
        ("scaler", StandardScaler()),
    ]
)

# --- CATEGORICAL TRANSFORMER (for categorical_features) ---

"""
Purpose: Prepare categorical (text) columns for machine learning

Two steps:
1. Impute missing values: Fill empty cells with a category
2. Encode: Convert categories to numbers
"""

categorical_transformer = Pipeline(
    steps=[
        # Step 1: IMPUTER for CATEGORICAL data
        # strategy="constant": Fill missing values with a constant value
        # fill_value="U": Use "U" (Unknown) for missing gender values
        # Why not mean? Mean doesn't work for text; use constant instead
        ("imputer", SimpleImputer(strategy="constant", fill_value="U")),
        # Step 2: ONE-HOT ENCODER
        # Converts categories to numbers that algorithms understand
        # Example: gender ["M", "F", "U"] becomes:
        #   gender_M: [1, 0, 0]
        #   gender_F: [0, 1, 0]
        #   gender_U: [0, 0, 1]
        # handle_unknown="ignore": If a new category appears, ignore it (don't crash)
        ("ohe", OneHotEncoder(handle_unknown="ignore")),
    ]
)

# --- COMBINE INTO COLUMN TRANSFORMER ---

"""
Purpose: Apply different transformers to different columns automatically

ColumnTransformer is like a director telling each column what to do:
- Numeric columns: use numeric_transformer
- Categorical columns: use categorical_transformer
"""

preprocessing_pipeline = ColumnTransformer(
    transformers=[
        # Transformer 1: Numeric
        ("numeric", numeric_transformer, numeric_features),
        # Arguments:
        #   "numeric": Name/label for this transformer
        #   numeric_transformer: The pipeline we created above
        #   numeric_features: ["age", "credit_score"] - which columns to apply it to
        # Transformer 2: Categorical
        ("categorical", categorical_transformer, categorical_features),
        # Arguments:
        #   "categorical": Name/label for this transformer
        #   categorical_transformer: The pipeline we created above
        #   categorical_features: ["gender"] - which columns to apply it to
    ]
)


# ============================================================
# SECTION 7: CREATING FULL PIPELINES (PREPROCESSING + MODEL)
# ============================================================

"""
Now we combine preprocessing + the actual machine learning model
into ONE PIPELINE. This ensures:
1. Data is always transformed the same way
2. No data leakage (test data isn't used during preprocessing)
3. Easy to save and reuse
"""

# --- MODEL 1: LOGISTIC REGRESSION ---

"""
Logistic Regression:
- Simplest classification algorithm
- Fast and easy to understand
- Outputs: Probability between 0 and 1
  Example: 0.8 = 80% chance of "Yes", 20% chance of "No"
"""

# Create full pipeline: preprocessing → logistic regression model
clf = Pipeline(
    steps=[
        # Step 1: Preprocessing
        ("preprocessing", preprocessing_pipeline),
        # Arguments:
        #   "preprocessing": Label for this step
        #   preprocessing_pipeline: The ColumnTransformer we created
        # Step 2: Classifier (the actual ML model)
        ("classifier", LogisticRegression(random_state=42)),
        # Arguments:
        #   "classifier": Label for this step
        #   LogisticRegression(random_state=42): The model
        #   random_state=42: Seed for reproducibility
    ]
)

# TRAIN THE MODEL
# clf.fit() learns patterns from training data
# It automatically:
# 1. Applies preprocessing_pipeline to X_train
# 2. Learns relationship between transformed X_train and y_train
clf.fit(X_train, y_train)

# MAKE PREDICTIONS
# clf.predict() predicts the target for test data
# It automatically:
# 1. Applies the same preprocessing to X_test
# 2. Uses learned patterns to predict
y_pred_class = clf.predict(X_test)

# EVALUATE THE MODEL
# accuracy_score() calculates percentage of correct predictions
# Example: If 95 out of 100 predictions are correct → 0.95 (95%)
accuracy_class = accuracy_score(y_test, y_pred_class)
print(f"Logistic Regression Accuracy: {accuracy_class}")


# --- MODEL 2: RANDOM FOREST CLASSIFIER ---

"""
Random Forest:
- Uses multiple decision trees
- Each tree votes on the prediction
- More complex but often more accurate than single models
"""

# Create second pipeline with Random Forest
clf_rf = Pipeline(
    steps=[
        ("preprocessing", preprocessing_pipeline),
        ("classifier", RandomForestClassifier(random_state=42)),
        # Arguments:
        #   n_estimators: Default 100 (number of decision trees)
        #   random_state=42: Seed for reproducibility
    ]
)

# Train Random Forest model
clf_rf.fit(X_train, y_train)

# Predict using Random Forest
y_pred_rf = clf_rf.predict(X_test)

# Evaluate Random Forest
accuracy_rf = accuracy_score(y_test, y_pred_rf)
print(f"Random Forest Accuracy: {accuracy_rf}")


# ============================================================
# SECTION 8: SAVING THE MODEL (PERSISTENCE)
# ============================================================

"""
WHY SAVE?
Training a model takes time and computation.
We want to save the trained model and reuse it later
without retraining every time.

Think of it like baking a cake:
- First time: ingredients + time = cake (save it!)
- Next time: take cake from fridge (don't bake again!)
"""

# Import joblib library
# joblib is specialized for saving Python objects (especially ML models)
import joblib

# Save the trained model to a file
# dump(object, filepath): Saves the model
# "data/model.joblib": File path where the model is saved
# This creates a file containing all learned weights and preprocessing rules
joblib.dump(clf_rf, "data/model.joblib")
print("Model saved to data/model.joblib")


# ============================================================
# SECTION 9: LOADING AND USING A SAVED MODEL
# ============================================================

"""
This section demonstrates using a previously saved model.
In real applications, you might:
1. Train model on server (one time)
2. Save model
3. Load model on multiple clients to make predictions
"""

# Import required packages (again, since we're in a new section)
import joblib
import numpy as np
import pandas as pd

# LOAD THE SAVED MODEL
# joblib.load() retrieves the saved model from file
# Returns the complete pipeline ready to make predictions
clf_loaded = joblib.load("data/model.joblib")

# CREATE NEW DATA FOR PREDICTION
# This simulates data from new customers/samples we've never seen
# Note: It can include missing values (NaN) - the pipeline handles them!

new_data = pd.DataFrame(
    {
        "age": [25, np.nan, 50],  # Three ages; one is missing
        "gender": ["M", "F", np.nan],  # Three genders; one is missing
        "credit_score": [200, 100, 500],  # Three credit scores (all present)
    }
)

# MAKE PREDICTIONS ON NEW DATA
# clf_loaded.predict() automatically:
# 1. Applies the same preprocessing (imputing + encoding)
# 2. Uses the learned model to predict
# Output: Array of predictions (likely [0 or 1] for binary classification)

predictions = clf_loaded.predict(new_data)
print("Predictions for new data:", predictions)

# ADDITIONAL: GET PREDICTION PROBABILITIES
# predict_proba() returns confidence scores instead of just 0/1
# Useful to know "how confident" the model is in its prediction
probabilities = clf_loaded.predict_proba(new_data)
print("Prediction probabilities:", probabilities)

# Example interpretation:
# If prediction is [0.2, 0.8], model is 80% confident about class 1

"""
Let me explain this clearly with concrete examples from your purchase prediction data.

## Understanding Classes in Binary Classification

### What is "Class 1"?

In machine learning with **two possible outcomes** (binary classification), we have:

```
Class 0 = "No" / Negative outcome
Class 1 = "Yes" / Positive outcome
```

### In Your Purchase Prediction Data

Remember your target variable is `"purchase"` - this contains YES/NO (or 1/0) values:

```python
y = my_df["purchase"]
# Values could be: [1, 0, 1, 1, 0, 1, ...]
# Where: 1 = Customer PURCHASED
#        0 = Customer DID NOT purchase
```

So in your specific case:
- **Class 0** = Customer did **NOT** purchase
- **Class 1** = Customer **DID** purchase

---

## What Does [0.2, 0.8] Actually Mean?

When the model outputs `[0.2, 0.8]`, it's giving **probability scores**:

```
[0.2, 0.8]
 ↓    ↓
 │    └─→ 0.8 = 80% confidence for Class 1 (WILL purchase)
 └──────→ 0.2 = 20% confidence for Class 0 (WON'T purchase)
```

**Always remember**: The two numbers must add up to 1.0 (100%)
```
0.2 + 0.8 = 1.0 ✓
```

---

## Real-World Example with Purchase Data

Let's say we load 3 new customers and make predictions:

```python
import pandas as pd
import numpy as np

new_customers = pd.DataFrame({
    "age": [25, 50, 35],
    "gender": ["M", "F", "M"],
    "credit_score": [750, 300, 600]
})

# Get predictions with probabilities
probabilities = clf_loaded.predict_proba(new_customers)
print(probabilities)

# Output:
# [[0.15, 0.85]   ← Customer 1
#  [0.92, 0.08]   ← Customer 2
#  [0.40, 0.60]]  ← Customer 3
```

### Interpretation:

| Customer | Age | Gender | Credit Score | Class 0 (Won't Buy) | Class 1 (Will Buy) | Prediction |
|----------|-----|--------|--------------|--------------------|--------------------|-----------|
| 1 | 25 | M | 750 | 15% | **85%** | ✅ WILL PURCHASE |
| 2 | 50 | F | 300 | **92%** | 8% | ❌ WON'T PURCHASE |
| 3 | 35 | M | 600 | 40% | **60%** | ✅ WILL PURCHASE |

---

## How to Extract and Use This Information

### Get Only the Predicted Class (0 or 1)
```python
predictions = clf_loaded.predict(new_customers)
print(predictions)  # Output: [1, 0, 1]
# Meaning: Buy, Don't Buy, Buy
```

### Get Probabilities with Labels
```python
probabilities = clf_loaded.predict_proba(new_customers)

# Customer 1 details:
customer_1_class_0_prob = probabilities[0][0]  # 0.15 (won't buy)
customer_1_class_1_prob = probabilities[0][1]  # 0.85 (will buy)

print(f"Customer 1 probability of NOT purchasing: {customer_1_class_0_prob:.1%}")
print(f"Customer 1 probability of PURCHASING: {customer_1_class_1_prob:.1%}")

# Output:
# Customer 1 probability of NOT purchasing: 15.0%
# Customer 1 probability of PURCHASING: 85.0%
```

### Make a Decision with Confidence Threshold
```python
# Only target customers with >70% probability of purchase
confidence_threshold = 0.70

for i, probs in enumerate(probabilities):
    purchase_probability = probs[1]  # Class 1 probability
    
    if purchase_probability >= confidence_threshold:
        print(f"Customer {i+1}: High likelihood to purchase ({purchase_probability:.1%})")
        # Take action: Send marketing campaign
    else:
        print(f"Customer {i+1}: Low likelihood to purchase ({purchase_probability:.1%})")
        # Don't waste marketing budget
```

---

## Why Use Probabilities Instead of Just 0 or 1?

### ❌ Simple Prediction (0 or 1)
```python
predictions = [1, 0, 1]  # Buy, Don't Buy, Buy
# Problem: We don't know how confident the model is
```

### ✅ Probability Prediction ([0.x, 0.y])
```python
probabilities = [[0.15, 0.85], [0.92, 0.08], [0.40, 0.60]]

# Now we know:
# Customer 1: Very confident (85% vs 15%)
# Customer 2: Very confident (92% vs 8%)
# Customer 3: Somewhat confident (60% vs 40%)

# Business decision:
# - Follow up hard on Customers 1 & 2 (high confidence predictions)
# - Investigate Customer 3 more (borderline case)
```

---

## Complete Code Example

```python
import pandas as pd
import joblib

# Load your trained model
model = joblib.load("data/model.joblib")

# New customers data
new_customers = pd.DataFrame({
    "age": [28, 45, 32],
    "gender": ["M", "F", "M"],
    "credit_score": [700, 550, 800]
})

# Get predictions
hard_predictions = model.predict(new_customers)
soft_predictions = model.predict_proba(new_customers)

print("=" * 60)
print("PURCHASE PREDICTION RESULTS")
print("=" * 60)

for i in range(len(new_customers)):
    customer = new_customers.iloc[i]
    pred = hard_predictions[i]
    prob_no_buy = soft_predictions[i][0]  # Class 0
    prob_buy = soft_predictions[i][1]      # Class 1
    
    print(f"\nCustomer {i+1}:")
    print(f"  Age: {customer['age']}, Gender: {customer['gender']}, Credit: {customer['credit_score']}")
    print(f"  Probability of NOT purchasing: {prob_no_buy:.1%} (Class 0)")
    print(f"  Probability of PURCHASING:     {prob_buy:.1%} (Class 1)")
    print(f"  Final Prediction: {'✅ WILL BUY' if pred == 1 else '❌ WON\'T BUY'}")

# Output Example:
# ============================================================
# PURCHASE PREDICTION RESULTS
# ============================================================
#
# Customer 1:
#   Age: 28, Gender: M, Credit: 700
#   Probability of NOT purchasing: 12.3% (Class 0)
#   Probability of PURCHASING:     87.7% (Class 1)
#   Final Prediction: ✅ WILL BUY
#
# Customer 2:
#   Age: 45, Gender: F, Credit: 550
#   Probability of NOT purchasing: 65.2% (Class 0)
#   Probability of PURCHASING:     34.8% (Class 1)
#   Final Prediction: ❌ WON'T BUY
#
# Customer 3:
#   Age: 32, Gender: M, Credit: 800
#   Probability of NOT purchasing: 8.5% (Class 0)
#   Probability of PURCHASING:     91.5% (Class 1)
#   Final Prediction: ✅ WILL BUY
```

---

## Key Takeaways

| Concept | Meaning |
|---------|---------|
| **Class 0** | Negative class = "WON'T purchase" |
| **Class 1** | Positive class = "WILL purchase" |
| **[0.2, 0.8]** | 20% no, 80% yes |
| **predict()** | Returns 0 or 1 (hard decision) |
| **predict_proba()** | Returns [0.x, 0.y] (confidence scores) |
| **0.8** | 80% confident about Class 1 (purchase) |

The comment in your code means: **"The model is 80% sure this customer WILL make a purchase (Class 1)"** ✅
"""

# ============================================================
# SUMMARY: FULL PIPELINE WORKFLOW
# ============================================================

"""
1. LOAD DATA
   ├─ Read CSV file into DataFrame

2. PREPARE DATA
   ├─ Split into X (features) and y (target)
   ├─ Split into train (80%) and test (20%)
   └─ Identify numeric vs categorical columns

3. CREATE TRANSFORMERS
   ├─ Numeric: impute missing values + scale
   ├─ Categorical: impute missing values + one-hot encode
   └─ Combine using ColumnTransformer

4. CREATE MODELS
   ├─ Logistic Regression (simple, fast)
   └─ Random Forest (complex, accurate)

5. TRAIN MODELS
   ├─ clf.fit(X_train, y_train)
   └─ Automatically applies preprocessing

6. EVALUATE MODELS
   ├─ clf.predict(X_test)
   └─ accuracy_score(y_test, predictions)

7. SAVE MODEL
   └─ joblib.dump(clf, filepath)

8. LOAD AND USE SAVED MODEL
   ├─ clf_loaded = joblib.load(filepath)
   ├─ clf_loaded.predict(new_data)
   └─ Works on new data automatically (handles missing values!)

KEY BENEFIT OF PIPELINES:
- No manual preprocessing needed for new data
- Preprocessing matches exactly what training used
- Reproducible and production-ready
"""
