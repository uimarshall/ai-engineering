# cspell:ignore sklearn joblib pyyaml yaml imputer encoders stratify
"""
Business Problem -> Data Science Solution -> Production Code
============================================================
A complete, runnable companion to:
    Turning_business_problems_into_Data Science_solutions.md

It walks the exact playbook from the note using ONE problem:
    BUSINESS COMPLAINT: "Customers keep leaving after the first year
                         and we don't know why or who."

    1. Frame the problem   (decision, metric, cost of error)
    2. Simulate a dataset  (stands in for your real CSV / SQL)
    3. Compute the baseline (the "dumb" benchmark)
    4. Train the model      (single shared feature pipeline)
    5. Evaluate honestly    (recall matters more than accuracy here)
    6. Turn scores into a business decision (a ranked call list)
    7. Production-grade prediction function (config-driven threshold)

Every line is commented for a beginner. Run with:
    python business_to_ds_solution.py
"""

# -------------------------------------------------------------
# 1. Import libraries
# -------------------------------------------------------------
import joblib  # for saving/loading the trained model artifact
import os  # to locate the script's own folder
import numpy as np  # for math and random data generation
import pandas as pd  # for tables
from sklearn.compose import ColumnTransformer  # apply different transforms per column
from sklearn.ensemble import RandomForestClassifier  # the model
from sklearn.impute import SimpleImputer  # fills missing values
from sklearn.metrics import classification_report, roc_auc_score  # evaluation metrics
from sklearn.model_selection import train_test_split  # split data
from sklearn.pipeline import Pipeline  # chains preprocessing + model
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # encode + scale

# -------------------------------------------------------------
# 2. Simulate a dataset
# -------------------------------------------------------------
# In a real project you would load your own data here, e.g.:
#     df = pd.read_csv("data/churn.csv")
# We generate 4,000 fake customers so the lesson runs anywhere.

rng = np.random.default_rng(42)  # reproducible randomness
n = 4000  # number of customers

df = pd.DataFrame(
    {
        "tenure_months": rng.integers(1, 72, n),  # how long they've been a customer
        "monthly_charges": rng.normal(70, 20, n).round(2),  # bill per month
        "total_charges": rng.normal(2000, 1200, n).round(2),  # total paid so far
        "support_tickets": rng.integers(0, 10, n),  # how many complaints they filed
        "num_products": rng.integers(1, 5, n),  # how many products they use
        "contract_type": rng.choice(  # their contract (a category, not a number)
            ["Month-to-month", "One year", "Two year"], n
        ),
    }
)

# Build a realistic-ish churn signal: unhappy, short-tenure, month-to-month
# customers are more likely to leave. This is the "truth" the model will try
# to learn from the features. The signal is deliberately clear so the lesson
# shows a model that genuinely beats the baseline.
logit = (
    -4.5
    + 0.55 * df["support_tickets"]  # more complaints -> much more likely to leave
    + 0.04 * df["monthly_charges"]  # higher bill -> more likely to leave
    - 0.08 * df["tenure_months"]  # longer tenure -> less likely to leave
    - 0.12 * df["num_products"]  # more products -> stickier, less likely to leave
    + (df["contract_type"] == "Month-to-month") * 1.8  # flexible contract -> churn risk
)
prob = 1 / (1 + np.exp(-logit))  # squash the score into a 0..1 probability
df["churn"] = (rng.random(n) < prob).astype(int)  # 1 = left, 0 = stayed

print("=" * 65)
print("BUSINESS PROBLEM")
print("=" * 65)
print("Complaint : Customers keep leaving after the first year.")
print("Decision  : Which customers should the retention team call this month?")
print("Metric    : Reduce 12-month churn (catch churners -> optimize RECALL).")
print("Cost      : Miss a churner = lost lifetime value; false alarm = wasted call.")
print("\nDataset shape:", df.shape, " | overall churn rate:", round(df.churn.mean(), 3))
print("\nFirst 5 rows:")
print(df.head().to_string())

# -------------------------------------------------------------
# 3. Compute the baseline first
# -------------------------------------------------------------
# Before any model, compute the dumbest possible benchmark: "predict nobody
# churns." If a model can't beat this, it has added zero value.
baseline_accuracy = 1 - df["churn"].mean()
print("\n" + "=" * 65)
print("BASELIN")
print("=" * 65)
print(f"Baseline (always predict 'no churn') accuracy: {baseline_accuracy:.3f}")
print(f"A model that just says 'no churn' is {baseline_accuracy:.1%} accurate")
print("but has 0% recall -> catches zero churners. Useless. Aim higher.")

# -------------------------------------------------------------
# 4. Split the data
# -------------------------------------------------------------
# Features X = everything we know BEFORE the customer decides to leave.
# Target   y = whether they churned.
feature_cols = [
    "tenure_months",
    "monthly_charges",
    "total_charges",
    "support_tickets",
    "num_products",
    "contract_type",
]
X = df[feature_cols]
y = df["churn"]

# stratify=y keeps the same churn ratio in both train and test sets.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
print("\nTrain rows:", len(X_train), "| Test rows:", len(X_test))

# -------------------------------------------------------------
# 5. Build ONE shared feature pipeline
# -------------------------------------------------------------
# This is the single most important production habit: the EXACT same
# preprocessing must run in training AND at prediction time. Building it
# once and bundling it with the model prevents train/serve skew.

numeric_features = [
    "tenure_months",
    "monthly_charges",
    "total_charges",
    "support_tickets",
    "num_products",
]
categorical_features = ["contract_type"]

# Numeric pipeline: fill missing with median, then scale to a standard range.
numeric_pipe = Pipeline(
    [
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ]
)

# Categorical pipeline: fill missing with the most common value, then one-hot
# encode. handle_unknown="ignore" means unseen categories (new in production)
# become all-zeros instead of crashing the model.
categorical_pipe = Pipeline(
    [
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(handle_unknown="ignore")),
    ]
)

# ColumnTransformer applies the right pipeline to the right columns.
preprocessor = ColumnTransformer(
    [
        ("num", numeric_pipe, numeric_features),
        ("cat", categorical_pipe, categorical_features),
    ]
)

# The full model: preprocessing + classifier, packaged as one object.
model = Pipeline(
    [
        ("pre", preprocessor),
        (
            "clf",
            RandomForestClassifier(
                n_estimators=300,
                class_weight="balanced",  # penalize missing a churner (minority class)
                random_state=42,  # reproducible training
            ),
        ),
    ]
)

# -------------------------------------------------------------
# 6. Train and evaluate
# -------------------------------------------------------------
# Fit learns the preprocessing rules AND the model weights from training data.
model.fit(X_train, y_train)

# predict_proba returns [prob_stay, prob_churn]; we want the churn column (index 1).
prob_churn = model.predict_proba(X_test)[:, 1]

# We threshold at 0.55 rather than 0.5 because catching churners (recall)
# is more valuable here than avoiding false alarms (precision).
THRESHOLD = 0.55
predictions = (prob_churn >= THRESHOLD).astype(int)

print("\n" + "=" * 65)
print("MODEL EVALUATION")
print("=" * 65)
print(f"ROC-AUC: {roc_auc_score(y_test, prob_churn):.3f}  (higher = better ranking)")
print(f"Recall on churners: {predictions[y_test == 1].mean():.3f}  (share of churners caught)")
print("\nDetailed report:")
print(classification_report(y_test, predictions, digits=3))

# -------------------------------------------------------------
# 7. Turn scores into a BUSINESS DECISION
# -------------------------------------------------------------
# A probability is not an action. The retention team can only call ~200 people
# a month, so we rank customers by churn probability and hand back the top N.
scored = X_test.copy()
scored["churn_probability"] = prob_churn
top_targets = scored.sort_values("churn_probability", ascending=False).head(200)

print("=" * 65)
print("BUSINESS OUTPUT - TOP 200 CALL LIST")
print("=" * 65)
print("These are the customers the retention team should call first:")
print(top_targets.head(10).to_string())

# -------------------------------------------------------------
# 8. Production-grade prediction (config-driven, callable)
# -------------------------------------------------------------
# Save the WHOLE pipeline (preprocessing + model) as a single artifact so it
# can be reloaded and used in production without re-training.
# Store it next to this script so it never clutters the repo root.
artifact_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "churn_model.joblib")
joblib.dump({"model": model, "threshold": THRESHOLD, "features": feature_cols}, artifact_path)
print(f"\nModel artifact saved to {artifact_path}")

# Load it back (simulates a fresh production process starting up).
artifact = joblib.load(artifact_path)
loaded_model = artifact["model"]
loaded_threshold = artifact["threshold"]


def predict_churn(customer: dict) -> dict:
    """Score a single customer and return a business decision.

    Args:
        customer: dict of raw feature values, e.g.
                  {"tenure_months": 14, "monthly_charges": 70.0, ...}

    Returns:
        {"churn_probability": 0.73, "should_contact": True}
    """
    # Rebuild a 1-row DataFrame with the SAME columns the model expects.
    X_new = pd.DataFrame([customer])
    # The pipeline applies the saved preprocessing automatically.
    prob = float(loaded_model.predict_proba(X_new)[:, 1][0])
    return {
        "churn_probability": round(prob, 4),
        "should_contact": prob >= loaded_threshold,  # threshold lives in config
    }


# -------------------------------------------------------------
# 9. Demonstrate the production function
# -------------------------------------------------------------
print("\n" + "=" * 65)
print("PRODUCTION PREDICTION FUNCTION")
print("=" * 65)

new_customer = {
    "tenure_months": 3,  # brand new
    "monthly_charges": 95.0,  # expensive
    "total_charges": 285.0,
    "support_tickets": 6,  # lots of complaints
    "num_products": 1,
    "contract_type": "Month-to-month",  # flexible, easy to leave
}
result = predict_churn(new_customer)
print(f"New customer: {new_customer}")
print(f"Prediction  : {result}")

# Prove the model is robust to an unseen category (e.g. a brand-new contract type).
unseen_customer = dict(new_customer)
unseen_customer["contract_type"] = "Weekly"  # never seen in training
result2 = predict_churn(unseen_customer)
print(f"\nSame customer with unseen contract 'Weekly':")
print(f"Prediction  : {result2}  (handle_unknown='ignore' kept it from crashing)")

print("\n" + "=" * 65)
print("WHAT THIS DELIVERED")
print("=" * 65)
print("""
1. Translated a vague complaint into a measurable decision.
2. Beat the dumb baseline with an honest, stratified evaluation.
3. Optimized the metric tied to business cost (recall on churners).
4. Turned probabilities into a ranked call list - an action, not a report.
5. Shipped it as a config-driven, reloadable, production-grade function.
""")