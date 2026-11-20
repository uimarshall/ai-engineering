# The Art of Turning Business Problems into Data Science Solutions

> A beginner-friendly, practical guide — from a vague business complaint to a
> production-grade machine learning service.

---

## 1. The Core Problem

Stakeholders rarely arrive saying _"I need a gradient-boosted classifier with a
0.85 AUC."_ They arrive saying things like:

| What the business says                       | What they actually mean                                       |
| -------------------------------------------- | ------------------------------------------------------------- |
| "We're losing customers left and right."     | Predict which customers will churn so we can intervene early. |
| "Marketing spend feels wasted."              | Measure the causal effect of each campaign on revenue.        |
| "Our delivery times are all over the place." | Forecast demand / route times to plan capacity.               |
| "Fraud is eating our margins."               | Detect anomalous transactions in real time.                   |
| "I need a report by Friday."                 | Aggregate, visualize, and explain — _not_ always a model.     |

The **art** is the translation: turning a fuzzy, emotional, business-language
problem into a **precise, measurable, technical** problem — and then building
something that actually ships.

> **Golden rule:** _If you can't write down how you will measure success before
> you build, you're not ready to build._

---

## 2. The Translation Framework (5 Questions)

Before writing a single line of code, answer these five questions with the
stakeholder. This is the single most valuable skill in applied data science.

### Q1. What decision will this change?

If the output won't change a decision, don't build it. "We want a churn model"
is weak. "We want to know which of our 5,000 at-risk customers to call this
month with a retention offer" is strong — it names the decision.

### Q2. What is the target metric, and is it measurable?

Translate the business goal into a **number**.

- Vague: "improve customer happiness" → Measurable: "reduce 30-day churn from 8% to 6%"
- Vague: "get more out of ads" → Measurable: "increase return on ad spend (ROAS) by 15%"

### Q3. What type of data science problem is this really?

Almost every business problem reduces to one of these buckets:

| Bucket                       | Question it answers     | Example                          | Typical algorithm                           |
| ---------------------------- | ----------------------- | -------------------------------- | ------------------------------------------- |
| **Classification**           | Which category?         | Will this customer churn?        | Logistic Regression, Random Forest, XGBoost |
| **Regression**               | How much?               | How many units will we sell?     | Linear Regression, Gradient Boosting        |
| **Clustering**               | Which group?            | Segment our customers            | K-Means, DBSCAN                             |
| **Forecasting**              | What's next in time?    | Next month's demand              | ARIMA, Prophet, LSTM                        |
| **Causal inference**         | Did X _cause_ Y?        | Did the campaign cause the lift? | CausalImpact, DiD, Uplift                   |
| **Ranking / Recommendation** | What should come first? | Which product to show?           | Learning-to-rank, collaborative filtering   |
| **Anomaly detection**        | What's unusual?         | Which transaction is fraud?      | Isolation Forest, autoencoders              |

### Q4. Do we have the data to answer it?

Check before you commit:

- **Volume:** enough rows for each class? (Churn with 50 examples won't generalize.)
- **Quality:** are the fields populated, consistent, trustworthy?
- **Availability:** is the data accessible _now_ and _at prediction time_?
- **Leakage:** does any feature secretly encode the answer (e.g., a `cancelled_date` column when predicting churn)?

### Q5. What is the cost of being wrong?

This drives everything downstream.

- **False negative** (miss a churner): lose a customer + their lifetime value.
- **False positive** (wrongly flag a loyal customer): wasted discount, annoyed customer.
  The relative cost determines your **decision threshold**, not the default 0.5.

---

## 3. Worked Example: From Complaint to Production Model

We'll follow one problem all the way through. This is the pattern you'll reuse.

### 3.1 The business complaint

> "Customers keep leaving after the first year and we don't know why or who."

### 3.2 The translation

| Step              | Result                                                                         |
| ----------------- | ------------------------------------------------------------------------------ |
| Decision          | Which customers should the retention team contact this month?                  |
| Metric            | Reduce 12-month churn by 20%                                                   |
| Problem type      | **Binary classification** (churn = 1, stay = 0)                                |
| Data needed       | Usage logs, billing, support tickets, demographics                             |
| Cost of error     | Miss a churner = lost LTV; false alarm = wasted incentive                      |
| Success criterion | Recall ≥ 0.70 on churners (catching churners matters more than precision here) |

Notice the success criterion is **recall**, not accuracy. With 8% churn, a model
that predicts "nobody churns" is 92% accurate and 100% useless. **Always pick
the metric that matches the business cost.**

### 3.3 Baseline first — always

Before any fancy model, compute the dumbest possible baseline. It frames what
"good" means.

```python
churn_rate = df["churn"].mean()
print(f"Baseline: always predict 'no churn' -> accuracy = {1 - churn_rate:.2%}")
# If a model can't beat 0.92 accuracy, it has added zero value.
```

### 3.4 A first, honest model

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

# Features: things we know BEFORE the customer decides to leave
feature_cols = ["tenure_months", "monthly_charges", "total_charges",
                "support_tickets", "num_products", "contract_type"]

X = pd.get_dummies(df[feature_cols], drop_first=True)  # encode categories
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42  # stratify keeps the 8% ratio
)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=300, class_weight="balanced",
                               random_state=42)
model.fit(X_train, y_train)

pred = model.predict(X_test)
prob = model.predict_proba(X_test)[:, 1]
print(classification_report(y_test, pred))
print(f"ROC-AUC: {roc_auc_score(y_test, prob):.3f}")
```

**Why `class_weight="balanced"`?** It tells the model that missing a churner
(the minority class) is more costly, so it doesn't just predict the majority.

### 3.5 Turn scores into a business decision

A probability is not an action. The retention team can only call ~200 people a
month. So we rank by probability and take the top N:

```python
results = X_test.copy()
results["churn_probability"] = prob
top_targets = results.sort_values("churn_probability", ascending=False).head(200)
# -> this exact list is what the retention team calls on Monday.
```

This is the difference between a notebook and a solution: **the output is a
ranked call list, not a confusion matrix.**

---

## 4. Common Ways This Goes Wrong (and the fix)

| Trap                             | Why it happens                                                 | The fix                                                   |
| -------------------------------- | -------------------------------------------------------------- | --------------------------------------------------------- |
| **Solving the wrong problem**    | You built what was technically interesting, not what was asked | Write the decision + metric down first (§2 Q1–Q2)         |
| **Data leakage**                 | A feature secretly contains the answer                         | Ask: "Would we know this _at prediction time_?"           |
| **Optimizing the wrong metric**  | Accuracy on imbalanced data                                    | Use the metric tied to business cost (recall, ROAS, etc.) |
| **Ignoring the baseline**        | No point of comparison                                         | Always compute the dumb baseline first                    |
| **Overfitting the test set**     | Tuning until the test score looks good                         | Use a separate validation set; touch test once            |
| **Model that can't be deployed** | Needs 12 fragile joins at scoring time                         | Design features to be reproducible in production          |
| **No monitoring plan**           | Model silently degrades                                        | Log predictions; track drift and business KPIs            |
| **Perfect is the enemy of good** | Six months of tuning, zero shipped value                       | Ship a v1 in weeks, iterate on real feedback              |

---

## 5. From Notebook to Production-Grade Code

A notebook proves an idea works. Production code makes it **reliable, repeatable,
and testable**. Here is the gap, concretely.

### 5.1 What "production-grade" actually means

| Notebook style                 | Production standard                                 | Why it matters                               |
| ------------------------------ | --------------------------------------------------- | -------------------------------------------- |
| `df = pd.read_csv("data.csv")` | Configurable, validated input                       | Paths change; schema drifts                  |
| `model.fit(X, y)` in a cell    | Reproducible pipeline                               | Must produce the same result on rebuild      |
| No error handling              | Explicit validation + logging                       | Fail loudly and informatively                |
| Hardcoded thresholds           | Config-driven                                       | Business changes shouldn't need code changes |
| One giant script               | Modular: config / data / features / train / predict | Testable and maintainable                    |
| `print()` debugging            | Structured logging                                  | Searchable, leveled output                   |
| Model in memory only           | Persisted artifact + version                        | Reproducible, auditable                      |

### 5.2 The reference structure

```
project/
├── config.yaml            # paths, thresholds, hyperparameters (not in code)
├── src/
│   ├── config.py          # load + validate config
│   ├── data.py            # load, validate, split
│   ├── features.py        # feature engineering (single source of truth)
│   ├── train.py           # train, evaluate, persist
│   ├── predict.py         # load model, score new data
│   └── utils.py           # logging, helpers
└── models/
    └── churn_model.joblib # versioned artifact
```

**The most important file is `features.py`.** The _exact same_ feature code must
run in training and at prediction time. Duplicating it differently is the #1
cause of "great in the notebook, garbage in production."

### 5.3 Config over constants

```python
# config.yaml
data_path: data/churn.csv
target: churn
test_size: 0.2
random_state: 42
model:
  n_estimators: 300
  class_weight: balanced
decision_threshold: 0.55   # tuned to business cost, not 0.5
```

```python
# src/config.py
import yaml
from dataclasses import dataclass

@dataclass(frozen=True)               # frozen = cannot be mutated by accident
class Config:
    data_path: str
    target: str
    test_size: float
    random_state: int
    n_estimators: int
    class_weight: str
    decision_threshold: float

def load_config(path: str) -> Config:
    """Load and validate configuration so failures happen at startup, not mid-run."""
    with open(path) as f:
        raw = yaml.safe_load(f)
    required = ["data_path", "target", "test_size", "random_state"]
    missing = [k for k in required if k not in raw]
    if missing:
        raise ValueError(f"Config missing keys: {missing}")
    return Config(
        data_path=raw["data_path"],
        target=raw["target"],
        test_size=raw["test_size"],
        random_state=raw["random_state"],
        n_estimators=raw.get("model", {}).get("n_estimators", 300),
        class_weight=raw.get("model", {}).get("class_weight", "balanced"),
        decision_threshold=raw.get("decision_threshold", 0.5),
    )
```

### 5.4 Validation at the boundary

Trust nothing that crosses into your system. Validate the schema early so you
get a clear error instead of a cryptic one 3 steps later.

```python
# src/data.py
import pandas as pd
from sklearn.model_selection import train_test_split

REQUIRED_COLUMNS = {"tenure_months", "monthly_charges", "support_tickets",
                    "num_products", "contract_type", "churn"}

def load_and_validate(path: str, target: str) -> pd.DataFrame:
    """Load the dataset and fail fast if the schema is wrong."""
    df = pd.read_csv(path)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Dataset missing required columns: {sorted(missing)}")

    if df[target].isna().any():
        raise ValueError(f"Target column '{target}' contains missing values")

    if not set(df[target].unique()).issubset({0, 1}):
        raise ValueError(f"Target '{target}' must be binary (0/1)")

    return df

def split_data(df: pd.DataFrame, target: str, test_size: float, seed: int):
    """Stratified split preserves the churn ratio in both sets."""
    X = df.drop(columns=[target])
    y = df[target]
    return train_test_split(X, y, test_size=test_size, stratify=y, random_state=seed)
```

### 5.5 One shared feature pipeline

This is what prevents train/serve skew — different results because features were
computed differently in two places.

```python
# src/features.py
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def build_preprocessor(numeric: list[str], categorical: list[str]):
    """
    Build ONE preprocessing pipeline used identically in train and predict.
    Fitting happens only on training data to avoid leakage.
    """
    num_pipe = Pipeline([
        ("impute", SimpleImputer(strategy="median")),  # fill missing numbers
        ("scale", StandardScaler()),                    # normalize ranges
    ])
    cat_pipe = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),  # fill missing cats
        ("encode", OneHotEncoder(handle_unknown="ignore")),   # unseen categories -> all zeros
    ])
    return ColumnTransformer([
        ("num", num_pipe, numeric),
        ("cat", cat_pipe, categorical),
    ])
```

**Why `handle_unknown="ignore"`?** In production you WILL meet a category never
seen in training. Without this, the model crashes; with it, that field is safely
encoded as all-zeros.

### 5.6 A training entry point that is reproducible

```python
# src/train.py
import logging
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score

from config import load_config
from data import load_and_validate, split_data
from features import build_preprocessor

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

NUMERIC = ["tenure_months", "monthly_charges", "total_charges",
           "support_tickets", "num_products"]
CATEGORICAL = ["contract_type"]

def train(config_path: str = "config.yaml") -> dict:
    cfg = load_config(config_path)

    df = load_and_validate(cfg.data_path, cfg.target)
    X_train, X_test, y_train, y_test = split_data(
        df, cfg.target, cfg.test_size, cfg.random_state
    )

    pre = build_preprocessor(NUMERIC, CATEGORICAL)
    model = Pipeline([
        ("pre", pre),                     # preprocessing baked into the model
        ("clf", RandomForestClassifier(
            n_estimators=cfg.n_estimators,
            class_weight=cfg.class_weight,
            random_state=cfg.random_state,
        )),
    ])

    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]

    log.info("ROC-AUC: %.3f", roc_auc_score(y_test, prob))
    log.info("\n%s", classification_report(y_test, prob >= cfg.decision_threshold))

    # Persist the WHOLE pipeline (preprocessing + model) as one artifact
    joblib.dump({"model": model, "config": cfg}, "models/churn_model.joblib")
    log.info("Saved model to models/churn_model.joblib")
    return {"roc_auc": roc_auc_score(y_test, prob)}

if __name__ == "__main__":
    train()
```

**Two deliberate choices here:**

1. **Preprocessing inside the pipeline** — so the saved artifact is self-contained.
   You can't accidentally forget to scale at prediction time.
2. **Save the config alongside the model** — so a model always knows the threshold
   and settings it was trained with.

### 5.7 Prediction as a clean, callable service

```python
# src/predict.py
import joblib
import pandas as pd

_ARTIFACT = None  # module-level cache so we load the model once, not per request

def load_artifact(path: str = "models/churn_model.joblib"):
    """Load the model once and cache it (loading is expensive)."""
    global _ARTIFACT
    if _ARTIFACT is None:
        _ARTIFACT = joblib.load(path)
    return _ARTIFACT

def predict_churn(customer: dict) -> dict:
    """
    Score a single customer.

    Args:
        customer: dict of raw feature values, e.g.
                  {"tenure_months": 14, "monthly_charges": 70.0, ...}

    Returns:
        {"churn_probability": 0.73, "should_contact": True}
    """
    artifact = load_artifact()
    model, cfg = artifact["model"], artifact["config"]

    # Rebuild a 1-row DataFrame with the SAME columns the model expects
    X = pd.DataFrame([customer])

    prob = float(model.predict_proba(X)[:, 1][0])
    return {
        "churn_probability": round(prob, 4),
        "should_contact": prob >= cfg.decision_threshold,  # business rule, config-driven
    }
```

This shape is what you expose as an API, a batch job, or a notebook widget.
Note the return is a **decision**, not just a number — the threshold lives in
config, so the business can tune it without a code change.

### 5.8 The habits that separate production code from a notebook

| Habit                       | Concrete action                                                      |
| --------------------------- | -------------------------------------------------------------------- |
| **Log, don't print**        | `logging.info(...)` with timestamps and levels                       |
| **Fail fast**               | Validate inputs at the boundary (§5.4)                               |
| **Never hardcode**          | Paths, seeds, thresholds → config (§5.3)                             |
| **Keep one feature path**   | Same `features.py` for train and predict (§5.5)                      |
| **Version artifacts**       | `churn_model_v3.joblib`, plus the git commit that made it            |
| **Type hints + docstrings** | IDE help + self-documenting contracts                                |
| **Determinism**             | Fix `random_state` everywhere; log library versions                  |
| **Monitor in production**   | Track prediction distribution and business KPI drift                 |
| **Test the plumbing**       | Unit-test `load_and_validate` and `predict_churn` with tiny fixtures |

### 5.9 A tiny test that catches real bugs

```python
# tests/test_predict.py
from src.predict import predict_churn

def test_predict_returns_business_decision():
    sample = {"tenure_months": 3, "monthly_charges": 95.0, "total_charges": 285.0,
              "support_tickets": 6, "num_products": 1, "contract_type": "Month-to-month"}
    out = predict_churn(sample)
    assert 0.0 <= out["churn_probability"] <= 1.0
    assert isinstance(out["should_contact"], bool)
```

---

## 6. The Full Playbook (End-to-End Checklist)

Use this every time, in order:

1. **Frame** — decision, metric, success criterion, cost of error (§2)
2. **Feasibility** — do we have (or can we get) the data, at prediction time?
3. **Baseline** — compute the dumb benchmark (§3.3)
4. **Explore** — distributions, missingness, correlations, leakage check
5. **Model v1** — simplest thing that could work; get it _working_, then _better_
6. **Evaluate honestly** — the right metric, on a validation set you don't tune on
7. **Translate to action** — rank, threshold, or decision rule (§3.5)
8. **Productionize** — modular, config-driven, tested, logged (§5)
9. **Deploy + monitor** — track drift and the business KPI the model was meant to move
10. **Iterate** — feed real outcomes back into the next version

---

## 7. Cheat Sheet

```
Business language      ->  Data Science translation
-----------------------------------------------------------------
"We're losing X"       ->  Binary classification + recall metric
"How many will Y?"     ->  Regression / time-series forecast
"Did our change work?" ->  Causal inference (CausalImpact, DiD)
"Group our customers"  ->  Clustering (K-Means)
"Find the weird ones"  ->  Anomaly detection (Isolation Forest)
"Show the best first"  ->  Ranking / recommendation

Always do first        ->  Baseline + write the decision + pick the metric
Always avoid           ->  Leakage, wrong metric, duplicated feature code
Production minimum     ->  Config, validation, one feature path,
                          logged, tested, versioned artifact, monitoring
```

---

## 8. One-Line Takeaway

**Turning a business problem into a data science solution is the discipline of
converting a vague complaint into a measurable decision, building the simplest
honest model that beats a baseline, and shipping it as tested, config-driven,
observable code — because a notebook only proves it works, while production
code is what actually delivers the value.**
