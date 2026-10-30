"""A beginner-friendly, runnable classification example."""

# Import the built-in dataset so the example does not need a file download.
from sklearn.datasets import load_breast_cancer

# Import four common supervised classification algorithms.
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

# Import metrics used to evaluate both class predictions and probabilities.
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

# Import the tools that keep preprocessing safely attached to each model.
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_models() -> dict[str, Pipeline]:
    """Create comparable preprocessing and model pipelines."""

    # Define preprocessing that learns its values only from training data.
    scaled_preprocessing = Pipeline(
        steps=[
            # Replace a missing numeric value with the training median.
            ("imputer", SimpleImputer(strategy="median")),
            # Put numeric features on a comparable scale.
            ("scaler", StandardScaler()),
        ]
    )

    # Return one pipeline for each model we want to compare.
    return {
        # Logistic regression is a strong, interpretable baseline.
        "Logistic regression": Pipeline(
            steps=[
                # Apply imputation and scaling before fitting the model.
                ("preprocessing", scaled_preprocessing),
                # Increase iterations so the optimiser has time to converge.
                ("model", LogisticRegression(max_iter=2_000, random_state=42)),
            ]
        ),
        # A shallow tree is easier to interpret and less likely to overfit.
        "Decision tree": Pipeline(
            steps=[
                # Keep the same preprocessing for a fair comparison.
                ("preprocessing", scaled_preprocessing),
                # Limit the number of decision levels.
                ("model", DecisionTreeClassifier(max_depth=4, random_state=42)),
            ]
        ),
        # A forest averages many trees to obtain a more robust prediction.
        "Random forest": Pipeline(
            steps=[
                # Keep preprocessing inside the pipeline.
                ("preprocessing", scaled_preprocessing),
                # Build 200 trees and use all available CPU cores.
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=200,
                        random_state=42,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
        # KNN predicts from the classes of nearby observations.
        "K-nearest neighbours": Pipeline(
            steps=[
                # Scaling is important because KNN uses distances.
                ("preprocessing", scaled_preprocessing),
                # Use the seven nearest training observations.
                ("model", KNeighborsClassifier(n_neighbors=7)),
            ]
        ),
    }


def main() -> None:
    """Load data, train models, evaluate them, and predict one new row."""

    # Load the dataset as a pandas DataFrame with readable column names.
    dataset = load_breast_cancer(as_frame=True)
    data = dataset.frame

    # Print the shape so a beginner can see the number of rows and columns.
    print(f"Dataset shape: {data.shape}")

    # Count missing cells before deciding how they should be handled.
    print(f"Missing cells before preprocessing: {data.isna().sum().sum()}")

    # Keep every feature column in X and keep the target column in y.
    X = data.drop(columns="target")
    y = data["target"]

    # Split before fitting the imputer or scaler to prevent data leakage.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # Build all candidate models with identical preprocessing.
    models = build_models()

    # Store F1 scores so the example can identify a candidate model.
    f1_scores: dict[str, float] = {}

    # Train and evaluate each candidate using the same test observations.
    for name, model in models.items():
        # Fit preprocessing and the classifier using training data only.
        model.fit(X_train, y_train)

        # Convert the test features into predicted class labels.
        predictions = model.predict(X_test)

        # Get the probability assigned to class 1 for ROC-AUC.
        probabilities = model.predict_proba(X_test)[:, 1]

        # Calculate the F1 score for later model selection.
        f1_scores[name] = f1_score(y_test, predictions)

        # Print a readable evaluation section for this model.
        print(f"\n=== {name} ===")
        print(f"Accuracy:  {accuracy_score(y_test, predictions):.3f}")
        print(f"Precision: {precision_score(y_test, predictions):.3f}")
        print(f"Recall:    {recall_score(y_test, predictions):.3f}")
        print(f"F1 score:  {f1_scores[name]:.3f}")
        print(f"ROC-AUC:   {roc_auc_score(y_test, probabilities):.3f}")
        print("Confusion matrix:")
        print(confusion_matrix(y_test, predictions))
        print("Detailed classification report:")
        print(classification_report(y_test, predictions))

    # Select the highest-F1 model for the final demonstration.
    best_name = max(f1_scores, key=f1_scores.get)
    best_model = models[best_name]

    # Select one held-out row while preserving its two-dimensional shape.
    new_observation = X_test.iloc[[0]]

    # Predict the class of the held-out observation with the selected model.
    predicted_class = best_model.predict(new_observation)[0]

    # Extract the selected model's probability for class 1.
    predicted_probability = best_model.predict_proba(new_observation)[0, 1]

    # Report the selected model and its example prediction.
    print(f"\nSelected model by F1 score: {best_name}")
    print(f"Example predicted class: {predicted_class}")
    print(f"Example probability for class 1: {predicted_probability:.3f}")


if __name__ == "__main__":
    # Run the example when this file is executed directly.
    main()
