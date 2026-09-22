"""
supervised_learning_tutorial.py
===============================
Companion code for "Supervised Learning: A Beginner's Guide".

Five self-contained demos:
    1. Linear regression from scratch with gradient descent
    2. Classification and the metrics that actually matter
    3. Comparing six models with cross-validation (+ learning curves)
    4. End-to-end business case: customer churn (classification)
    5. End-to-end business case: house prices (regression)

Every figure is saved to ./plots/ AND displayed on screen.

Install / run
-------------
    pip install numpy pandas scikit-learn matplotlib
    python supervised_learning_tutorial.py

Requires scikit-learn >= 1.0 and matplotlib >= 3.5.
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import (
    StratifiedKFold,
    cross_val_score,
    learning_curve,
    train_test_split,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

RANDOM_STATE = 0
PLOT_DIR = "plots"
os.makedirs(PLOT_DIR, exist_ok=True)


def finish(fig, filename: str) -> None:
    """Save the figure to disk, show it, then free the memory."""
    path = os.path.join(PLOT_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"  [saved] {path}")
    plt.show()
    plt.close(fig)


def banner(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


# ---------------------------------------------------------------------------
# DEMO 1 - Regression from scratch
# ---------------------------------------------------------------------------
def demo_01_regression_from_scratch() -> None:
    banner("DEMO 1 - Linear regression from scratch (gradient descent)")

    rng = np.random.default_rng(42)
    n = 300
    x = rng.uniform(0, 10, n)
    y = 3.0 * x + 5.0 + rng.normal(0.0, 2.5, n)  # true rule + irreducible noise

    # Standardising the feature makes gradient descent converge in far fewer steps.
    x_mean, x_std = x.mean(), x.std()
    xs = (x - x_mean) / x_std

    w, b = 0.0, 0.0  # parameters start at zero
    learning_rate = 0.1
    epochs = 400
    history = []

    for _ in range(epochs):
        y_hat = w * xs + b
        error = y_hat - y
        history.append(float(np.mean(error**2)))  # MSE, kept for the plot
        dw = 2.0 * np.mean(error * xs)  # d(MSE)/dw
        db = 2.0 * np.mean(error)  # d(MSE)/db
        w -= learning_rate * dw
        b -= learning_rate * db

    # Convert weights from standardised space back to original units
    slope = w / x_std
    intercept = b - w * x_mean / x_std
    print(f"  learned rule  : y = {slope:.3f} * x + {intercept:.3f}")
    print("  true rule     : y = 3.000 * x + 5.000")
    print(
        f"  final MSE     : {history[-1]:.3f}   "
        f"(irreducible noise variance ~ {2.5 ** 2:.3f})"
    )

    sk = LinearRegression().fit(xs.reshape(-1, 1), y)
    print(
        f"  sklearn check : y = {sk.coef_[0] / x_std:.3f} * x "
        f"+ {sk.intercept_ - sk.coef_[0] * x_mean / x_std:.3f}"
    )

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    axes[0].plot(range(1, epochs + 1), history, color="crimson", lw=2)
    axes[0].set_xlabel("epoch")
    axes[0].set_ylabel("MSE (training loss)")
    axes[0].set_title("Gradient descent: loss falls, then flattens")
    axes[0].grid(alpha=0.3)

    axes[1].scatter(x, y, s=14, alpha=0.5, color="steelblue", label="data")
    grid = np.linspace(x.min(), x.max(), 100)
    axes[1].plot(
        grid, slope * grid + intercept, color="crimson", lw=2.5, label="learned line"
    )
    axes[1].plot(
        grid, 3.0 * grid + 5.0, color="black", ls="--", lw=1.5, label="true line"
    )
    axes[1].set_xlabel("feature x")
    axes[1].set_ylabel("target y")
    axes[1].set_title("Fitted line vs. ground truth")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    fig.tight_layout()
    finish(fig, "01_gradient_descent.png")


# ---------------------------------------------------------------------------
# DEMO 2 - Classification metrics
# ---------------------------------------------------------------------------
def demo_02_classification_metrics() -> None:
    banner("DEMO 2 - Classification and the metrics that matter")

    X, y = load_breast_cancer(
        as_frame=True, return_X_y=True
    )  # 0 = malignant, 1 = benign
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y
    )

    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=5000)),
        ]
    ).fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]  # P(benign)

    print(
        classification_report(
            y_test, y_pred, target_names=["malignant", "benign"], digits=3
        )
    )
    print(f"  accuracy : {accuracy_score(y_test, y_pred):.4f}")
    print(f"  ROC-AUC  : {roc_auc_score(y_test, y_proba):.4f}")

    print("\n  What happens as we move the decision threshold?")
    print("  threshold  precision  recall      F1")
    for t in np.arange(0.1, 1.0, 0.1):
        pred_t = (y_proba >= t).astype(int)
        print(
            f"  {t:9.1f}  {precision_score(y_test, pred_t, zero_division=0):9.3f}"
            f"  {recall_score(y_test, pred_t, zero_division=0):6.3f}"
            f"  {f1_score(y_test, pred_t, zero_division=0):6.3f}"
        )

    fig, axes = plt.subplots(1, 3, figsize=(16.5, 5))

    # (a) the sigmoid
    z = np.linspace(-8, 8, 200)
    axes[0].plot(z, 1 / (1 + np.exp(-z)), color="navy", lw=2.5)
    axes[0].axhline(0.5, color="grey", ls="--", lw=1)
    axes[0].axvline(0, color="grey", ls="--", lw=1)
    axes[0].set_xlabel("raw score  z = w.x + b")
    axes[0].set_ylabel("P(y = 1)")
    axes[0].set_title("Sigmoid: score -> probability")
    axes[0].grid(alpha=0.3)

    # (b) confusion matrix
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
    im = axes[1].imshow(cm, cmap="Blues")
    axes[1].set_xticks([0, 1])
    axes[1].set_xticklabels(["malignant", "benign"])
    axes[1].set_yticks([0, 1])
    axes[1].set_yticklabels(["malignant", "benign"])
    axes[1].set_xlabel("predicted")
    axes[1].set_ylabel("actual")
    axes[1].set_title("Confusion matrix")
    for i in range(2):
        for j in range(2):
            axes[1].text(
                j,
                i,
                str(cm[i, j]),
                ha="center",
                va="center",
                color="white" if cm[i, j] > cm.max() / 2 else "black",
                fontsize=13,
            )
    fig.colorbar(im, ax=axes[1], fraction=0.046)

    # (c) ROC curve
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    auc = roc_auc_score(y_test, y_proba)
    axes[2].plot(fpr, tpr, lw=2.5, color="darkgreen", label=f"AUC = {auc:.3f}")
    axes[2].plot([0, 1], [0, 1], ls="--", color="grey", label="random guessing")
    axes[2].set_xlabel("False positive rate")
    axes[2].set_ylabel("True positive rate (recall)")
    axes[2].set_title("ROC curve: ranking quality")
    axes[2].legend(loc="lower right")
    axes[2].grid(alpha=0.3)

    fig.tight_layout()
    finish(fig, "02_classification_metrics.png")


# ---------------------------------------------------------------------------
# DEMO 3 - Model comparison and learning curves
# ---------------------------------------------------------------------------
def demo_03_model_comparison() -> None:
    banner("DEMO 3 - Comparing six models with 5-fold cross-validation")

    X, y = load_breast_cancer(as_frame=True, return_X_y=True)
    X, y = np.asarray(X), np.asarray(y)

    models = {
        "Logistic regression": Pipeline(
            [("s", StandardScaler()), ("m", LogisticRegression(max_iter=5000))]
        ),
        "k-NN (k=5)": Pipeline(
            [("s", StandardScaler()), ("m", KNeighborsClassifier(n_neighbors=5))]
        ),
        "Decision tree (depth 3)": DecisionTreeClassifier(
            max_depth=3, random_state=RANDOM_STATE
        ),
        "Random forest (300)": RandomForestClassifier(
            n_estimators=300, random_state=RANDOM_STATE
        ),
        "Gradient boosting (200)": GradientBoostingClassifier(
            random_state=RANDOM_STATE
        ),
        "SVM (RBF kernel)": Pipeline([("s", StandardScaler()), ("m", SVC())]),
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    names, means, stds = [], [], []
    for name, model in models.items():
        scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
        names.append(name)
        means.append(scores.mean())
        stds.append(scores.std())
        print(f"  {name:26s} accuracy = {scores.mean():.4f} +/- {scores.std():.4f}")

    lc_result = learning_curve(
        RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE),
        X,
        y,
        cv=cv,
        scoring="accuracy",
        train_sizes=np.linspace(0.1, 1.0, 8),
        n_jobs=1,
    )
    # learning_curve's inferred return type covers the return_times=True case too (5 items)
    sizes, train_scores, test_scores = lc_result[0], lc_result[1], lc_result[2]

    fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))

    order = np.argsort(means)
    axes[0].barh(
        [names[i] for i in order],
        [means[i] for i in order],
        xerr=[stds[i] for i in order],
        color="steelblue",
        capsize=4,
    )
    axes[0].set_xlim(0.85, 1.005)
    axes[0].set_xlabel("cross-validated accuracy (5-fold)")
    axes[0].set_title("Model comparison: mean +/- std")
    axes[0].grid(axis="x", alpha=0.3)

    train_mu, train_sd = train_scores.mean(axis=1), train_scores.std(axis=1)
    test_mu, test_sd = test_scores.mean(axis=1), test_scores.std(axis=1)
    axes[1].plot(sizes, train_mu, "-o", color="crimson", label="training score")
    axes[1].fill_between(
        sizes, train_mu - train_sd, train_mu + train_sd, color="crimson", alpha=0.15
    )
    axes[1].plot(sizes, test_mu, "-o", color="navy", label="cross-validation score")
    axes[1].fill_between(
        sizes, test_mu - test_sd, test_mu + test_sd, color="navy", alpha=0.15
    )
    axes[1].set_xlabel("number of training examples")
    axes[1].set_ylabel("accuracy")
    axes[1].set_title("Learning curve (random forest)")
    axes[1].legend(loc="lower right")
    axes[1].grid(alpha=0.3)

    fig.tight_layout()
    finish(fig, "03_model_comparison.png")


# ---------------------------------------------------------------------------
# DEMO 4 - End-to-end classification business case: churn
# ---------------------------------------------------------------------------
def demo_04_churn_end_to_end() -> None:
    banner("DEMO 4 - Business case: predicting customer churn (classification)")

    rng = np.random.default_rng(7)
    n = 4000

    tenure = rng.integers(1, 73, n)
    monthly = np.clip(rng.normal(70, 25, n), 20, 150).round(2)
    support_calls = rng.poisson(1.2, n)
    contract = rng.choice(
        ["month-to-month", "one year", "two year"], n, p=[0.55, 0.25, 0.20]
    )
    internet = rng.choice(["DSL", "Fibre", "None"], n, p=[0.35, 0.45, 0.20])
    senior = rng.integers(0, 2, n)
    total = (tenure * monthly * rng.normal(1.0, 0.05, n)).round(2)

    # The (hidden) churn mechanism we want the model to rediscover
    logit = (
        -0.9
        + 0.95 * (contract == "month-to-month")
        - 0.20 * (contract == "two year")
        + 0.35 * (internet == "Fibre")
        - 0.045 * tenure
        + 0.30 * support_calls
        + 0.012 * monthly
        + 0.35 * senior
    )
    churned = rng.binomial(1, 1.0 / (1.0 + np.exp(-logit)))

    df = pd.DataFrame(
        {
            "tenure_months": tenure,
            "monthly_charges": monthly,
            "total_charges": total,
            "support_calls": support_calls,
            "contract": contract,
            "internet_service": internet,
            "is_senior": senior,
            "churned": churned,
        }
    )
    df.loc[rng.choice(n, size=120, replace=False), "total_charges"] = np.nan

    print(f"  dataset   : {df.shape[0]} customers x {df.shape[1] - 1} features")
    print(f"  churn rate: {df['churned'].mean():.1%}")
    print(
        f"  missing   : {int(df['total_charges'].isna().sum())} rows in total_charges"
    )

    X = df.drop(columns=["churned"])
    y = df["churned"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y
    )

    num_cols = ["tenure_months", "monthly_charges", "total_charges", "support_calls"]
    cat_cols = ["contract", "internet_service", "is_senior"]

    preprocess = ColumnTransformer(
        [
            (
                "num",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="median")),
                        ("scale", StandardScaler()),
                    ]
                ),
                num_cols,
            ),
            (
                "cat",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="most_frequent")),
                        ("encode", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                cat_cols,
            ),
        ]
    )
    clf = Pipeline(
        [
            ("preprocess", preprocess),
            ("model", LogisticRegression(max_iter=5000, class_weight="balanced")),
        ]
    ).fit(X_train, y_train)

    proba = clf.predict_proba(X_test)[:, 1]
    y_pred = (proba >= 0.5).astype(int)

    print("\n  Performance at the default 0.5 threshold")
    print(classification_report(y_test, y_pred, digits=3))
    print(
        f"  do-nothing baseline accuracy (never predict churn) = "
        f"{1 - y_test.mean():.3f}   <- why accuracy alone is not enough"
    )

    # ---------------- threshold tuning with money ----------------
    VALUE_RETAINED = 300.0  # net value of saving one true churner
    COST_OF_OFFER = 50.0  # cost of a wasted retention offer

    rows = []
    for t in np.arange(0.05, 0.96, 0.05):
        pred = (proba >= t).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_test, pred, labels=[0, 1]).ravel()
        rows.append(
            {
                "threshold": round(float(t), 2),
                "precision": precision_score(y_test, pred, zero_division=0),
                "recall": recall_score(y_test, pred, zero_division=0),
                "f1": f1_score(y_test, pred, zero_division=0),
                "TP": int(tp),
                "FP": int(fp),
                "expected_value_$": VALUE_RETAINED * tp - COST_OF_OFFER * fp,
            }
        )
    tune = pd.DataFrame(rows)
    best = tune.loc[tune["expected_value_$"].idxmax()].to_dict()

    print(
        "\n  Top 5 thresholds by expected value (assumes $300 saved per true "
        "churner, $50 per wasted offer)"
    )
    print(
        tune.sort_values("expected_value_$", ascending=False)
        .head(5)
        .to_string(index=False)
    )
    print(
        f"\n  Profit-maximising threshold: {best['threshold']:.2f}  "
        f"->  expected value ~ ${best['expected_value_$']:,.0f} "
        f"on {len(y_test)} test customers"
    )

    pred_best = (proba >= float(best["threshold"])).astype(int)

    # ---------------- figure 04a: thresholds ----------------
    fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))
    axes[0].plot(tune["threshold"], tune["precision"], "-o", label="precision")
    axes[0].plot(tune["threshold"], tune["recall"], "-o", label="recall")
    axes[0].plot(tune["threshold"], tune["f1"], "-o", label="F1")
    axes[0].axvline(0.5, color="grey", ls="--", lw=1, label="default 0.50")
    axes[0].set_xlabel("decision threshold")
    axes[0].set_ylabel("score")
    axes[0].set_title("Precision / recall / F1 vs. threshold")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    axes[1].plot(tune["threshold"], tune["expected_value_$"], "-o", color="darkgreen")
    axes[1].axvline(
        float(best["threshold"]),
        color="crimson",
        ls="--",
        label=f"best = {best['threshold']:.2f}",
    )
    axes[1].axvline(0.5, color="grey", ls=":", label="default = 0.50")
    axes[1].set_xlabel("decision threshold")
    axes[1].set_ylabel("expected value ($)")
    axes[1].set_title("Money is the metric: expected value vs. threshold")
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    fig.tight_layout()
    finish(fig, "04a_churn_thresholds.png")

    # ---------------- figure 04b: confusion matrix + drivers ----------------
    feature_names = clf.named_steps["preprocess"].get_feature_names_out()
    coefs = clf.named_steps["model"].coef_[0]
    coef_df = (
        pd.DataFrame({"feature": feature_names, "coefficient": coefs})
        .assign(abs_coef=lambda d: d["coefficient"].abs())
        .sort_values("abs_coef", ascending=False)
        .head(12)
        .sort_values("coefficient")
    )

    print("\n  Most influential features (log-odds coefficients)")
    print(coef_df[["feature", "coefficient"]].to_string(index=False))

    fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))

    cm_best = confusion_matrix(y_test, pred_best, labels=[0, 1])
    im = axes[0].imshow(cm_best, cmap="Blues")
    axes[0].set_xticks([0, 1])
    axes[0].set_xticklabels(["stays", "churns"])
    axes[0].set_yticks([0, 1])
    axes[0].set_yticklabels(["stays", "churns"])
    axes[0].set_xlabel("predicted")
    axes[0].set_ylabel("actual")
    axes[0].set_title(f"Confusion matrix @ threshold {best['threshold']:.2f}")
    for i in range(2):
        for j in range(2):
            axes[0].text(
                j,
                i,
                str(cm_best[i, j]),
                ha="center",
                va="center",
                color="white" if cm_best[i, j] > cm_best.max() / 2 else "black",
                fontsize=13,
            )
    fig.colorbar(im, ax=axes[0], fraction=0.046)

    colors = np.where(coef_df["coefficient"] > 0, "crimson", "steelblue")
    axes[1].barh(coef_df["feature"], coef_df["coefficient"], color=colors)
    axes[1].axvline(0, color="black", lw=1)
    axes[1].set_xlabel("log-odds coefficient (positive = more likely to churn)")
    axes[1].set_title("What drives churn?")
    axes[1].grid(axis="x", alpha=0.3)

    fig.tight_layout()
    finish(fig, "04b_churn_drivers.png")


# ---------------------------------------------------------------------------
# DEMO 5 - End-to-end regression business case: house prices
# ---------------------------------------------------------------------------
def demo_05_house_price_regression() -> None:
    banner("DEMO 5 - Business case: house prices (regression)")

    rng = np.random.default_rng(3)
    n = 1500
    sqft = np.clip(rng.normal(1800, 550, n), 500, 5000).round(0)
    bedrooms = rng.integers(1, 6, n)
    age = rng.integers(0, 60, n)
    distance_km = rng.gamma(2.0, 2.5, n).round(2)
    garage = rng.integers(0, 3, n)

    price = (
        60_000
        + 155 * sqft
        + 12_000 * bedrooms
        - 900 * age
        - 9_500 * distance_km
        + 15_000 * garage
        + rng.normal(0, 30_000, n)
    )
    price = np.clip(price, 50_000, None).round(0)

    df = pd.DataFrame(
        {
            "sqft": sqft,
            "bedrooms": bedrooms,
            "age_years": age,
            "distance_km": distance_km,
            "garage_spaces": garage,
            "price": price,
        }
    )
    print(
        f"  dataset: {df.shape[0]} houses, "
        f"median price ${df['price'].median():,.0f}"
    )

    X = df.drop(columns=["price"])
    y = df["price"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=RANDOM_STATE
    )

    lin = LinearRegression().fit(X_train, y_train)
    rf = RandomForestRegressor(n_estimators=400, random_state=RANDOM_STATE).fit(
        X_train, y_train
    )

    print(f"\n  {'model':18s} {'MAE':>10s} {'RMSE':>10s} {'R2':>8s}")
    for name, model in [("linear regression", lin), ("random forest", rf)]:
        pred = model.predict(X_test)
        print(
            f"  {name:18s} {mean_absolute_error(y_test, pred):10,.0f}"
            f" {np.sqrt(mean_squared_error(y_test, pred)):10,.0f}"
            f" {r2_score(y_test, pred):8.3f}"
        )

    true_effect = {
        "sqft": 155,
        "bedrooms": 12_000,
        "age_years": -900,
        "distance_km": -9_500,
        "garage_spaces": 15_000,
    }
    print("\n  Linear model: learned vs. true effect (dollars per +1 unit)")
    for feat, coef in zip(X.columns, lin.coef_):
        print(f"    {feat:14s} learned {coef:9,.0f}    true {true_effect[feat]:9,.0f}")

    pred_rf = rf.predict(X_test)
    resid_rf = y_test - pred_rf

    fig, axes = plt.subplots(1, 3, figsize=(17, 5))

    axes[0].scatter(y_test, pred_rf, s=12, alpha=0.5, color="navy")
    lo, hi = float(y_test.min()), float(y_test.max())
    axes[0].plot([lo, hi], [lo, hi], color="crimson", ls="--")
    axes[0].set_xlabel("actual price")
    axes[0].set_ylabel("predicted price")
    axes[0].set_title(
        f"Predicted vs. actual (forest), R2 = {r2_score(y_test, pred_rf):.3f}"
    )
    axes[0].grid(alpha=0.3)

    axes[1].scatter(pred_rf, resid_rf, s=12, alpha=0.5, color="darkgreen")
    axes[1].axhline(0, color="black", lw=1)
    axes[1].set_xlabel("predicted price")
    axes[1].set_ylabel("residual (actual - predicted)")
    axes[1].set_title("Residuals: look for patterns, not clouds")
    axes[1].grid(alpha=0.3)

    importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values()
    axes[2].barh(importances.index, importances.values, color="steelblue")
    axes[2].set_xlabel("relative importance")
    axes[2].set_title("Random forest feature importance")
    axes[2].grid(axis="x", alpha=0.3)

    fig.tight_layout()
    finish(fig, "05_house_price_regression.png")


if __name__ == "__main__":
    demo_01_regression_from_scratch()
    demo_02_classification_metrics()
    demo_03_model_comparison()
    demo_04_churn_end_to_end()
    demo_05_house_price_regression()
    print(f"\nAll demos complete. Figures saved in ./{PLOT_DIR}/")
