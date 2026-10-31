"""A beginner-friendly, runnable classification example."""

# cast informs the type checker about a type guaranteed by the loader argument.
from typing import cast

# sklearn.datasets contains sample datasets and tools for loading them.
# load_breast_cancer() loads the built-in breast-cancer classification data.
from sklearn.datasets import load_breast_cancer

# sklearn.ensemble contains models that combine multiple estimators.
# RandomForestClassifier combines the predictions of many decision trees.
from sklearn.ensemble import RandomForestClassifier

# sklearn.impute provides ways to fill missing feature values.
# SimpleImputer learns a replacement, such as a median from training data.
from sklearn.impute import SimpleImputer

# sklearn.linear_model contains models based on linear relationships.
# LogisticRegression is a commonly used probability-based classifier.
from sklearn.linear_model import LogisticRegression

# sklearn.metrics contains functions that measure model performance.
from sklearn.metrics import (  # Fraction of predictions that match the known labels.; Text summary of precision, recall, and F1 for each class.; Counts actual versus predicted classes.; Fraction of predicted positives that are truly positive.; Fraction of actual positives that the model finds.; Combines precision and recall into one score.; Measures how well probabilities rank positive examples above negatives.
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

# sklearn.model_selection contains tools for preparing model evaluations.
# train_test_split separates data into training and held-out test subsets.
from sklearn.model_selection import train_test_split

# sklearn.neighbors contains models that compare nearby observations.
# KNeighborsClassifier predicts from the labels of its nearest neighbors.
from sklearn.neighbors import KNeighborsClassifier

# sklearn.pipeline chains preparation steps and a model into one estimator.
from sklearn.pipeline import Pipeline

# sklearn.preprocessing contains transformations to prepare feature values.
# StandardScaler centers numeric columns and scales their variation.
from sklearn.preprocessing import StandardScaler

# sklearn.tree contains decision-tree models.
# DecisionTreeClassifier learns feature-based questions to classify rows.
from sklearn.tree import DecisionTreeClassifier

# Bunch is the dictionary-like object returned when return_X_y=False.
from sklearn.utils import Bunch


def build_models() -> dict[str, Pipeline]:
    """Create comparable preprocessing and model pipelines.

    dict[str, Pipeline] says the result is a dictionary from text names to
    scikit-learn Pipeline objects.
    """

    # Define preprocessing that learns its values only from training data.
    scaled_preprocessing = Pipeline(
        steps=[
            # SimpleImputer learns the median from training data and fills gaps.
            ("imputer", SimpleImputer(strategy="median")),
            # StandardScaler centers features and scales their standard deviation.
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
                # max_iter allows more training iterations; random_state makes
                # any estimator randomness repeatable.
                ("model", LogisticRegression(max_iter=2_000, random_state=42)),
            ]
        ),
        # A shallow tree is easier to interpret and less likely to overfit.
        "Decision tree": Pipeline(
            steps=[
                # Keep the same preprocessing for a fair comparison.
                ("preprocessing", scaled_preprocessing),
                # max_depth limits tree levels; random_state makes randomized
                # behavior repeatable.
                ("model", DecisionTreeClassifier(max_depth=4, random_state=42)),
            ]
        ),
        # A forest averages many trees to obtain a more robust prediction.
        "Random forest": Pipeline(
            steps=[
                # Keep preprocessing inside the pipeline.
                ("preprocessing", scaled_preprocessing),
                # n_estimators chooses the tree count; random_state makes the
                # example repeatable; n_jobs=-1 uses available CPU cores.
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
                # n_neighbors sets how many nearby training rows vote.
                ("model", KNeighborsClassifier(n_neighbors=7)),
            ]
        ),
    }


def main() -> None:
    """Load data, train models, evaluate them, and predict one new row.

    -> None means this function performs actions and does not return a value.
    """

    # as_frame=True asks scikit-learn for pandas data with readable column names.
    # cast clarifies the documented Bunch return type; it does not change runtime data.
    dataset = cast(
        Bunch,
        load_breast_cancer(as_frame=True, return_X_y=False),
    )
    data = dataset.frame

    # Print the shape so a beginner can see the number of rows and columns.
    # Print the dimensions as (number of observations, number of columns).
    print(f"Dataset shape: {data.shape}")

    # isna() marks missing cells; sum() counts them by column, then in total.
    print(f"Missing cells before preprocessing: {data.isna().sum().sum()}")

    # Keep every feature column in X and keep the target column in y.
    X = data.drop(columns="target")
    y = data["target"]

    # Split before fitting the imputer or scaler to prevent data leakage.
    # Split first so test rows cannot influence what the imputer or scaler learns.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,  # Reserve 20% for evaluation; train on the other 80%.
        random_state=42,  # Repeat the same random split each time.
        stratify=y,  # Keep similar proportions of each class in both subsets.
    )

    # Build all candidate models with identical preprocessing.
    models = build_models()

    # Store F1 scores so the example can identify a candidate model.
    f1_scores: dict[str, float] = {}

    # Train and evaluate each candidate using the same test observations.
    for name, model in models.items():
        # fit() learns preprocessing settings and model patterns from training data.
        model.fit(X_train, y_train)

        # predict() returns one class label for each held-out test row.
        predictions = model.predict(X_test)

        # predict_proba() returns a probability per class; [:, 1] takes the
        # probability of class 1 for every test row.
        probabilities = model.predict_proba(X_test)[:, 1]

        # Calculate the F1 score for later model selection.
        f1_scores[name] = float(f1_score(y_test, predictions))

        # Print a readable evaluation section for this model.
        print(f"\n=== {name} ===")  # Start a section after a blank line.
        # :.3f formats the score with three digits after the decimal point.
        print(f"Accuracy:  {accuracy_score(y_test, predictions):.3f}")
        print(f"Precision: {precision_score(y_test, predictions):.3f}")
        print(f"Recall:    {recall_score(y_test, predictions):.3f}")
        print(f"F1 score:  {f1_scores[name]:.3f}")
        print(f"ROC-AUC:   {roc_auc_score(y_test, probabilities):.3f}")
        print("Confusion matrix:")  # Add a label before printing the matrix.
        print(confusion_matrix(y_test, predictions))
        print("Detailed classification report:")  # Label per-class metrics.
        print(classification_report(y_test, predictions))

    # Select the highest-F1 model for the final demonstration.
    # max() finds the dictionary key whose stored F1 score is largest.
    best_name = max(f1_scores, key=lambda model_name: f1_scores[model_name])
    best_model = models[best_name]

    # .iloc selects by row position; [[0]] keeps a one-row DataFrame with
    # feature names, rather than reducing the selection to a one-dimensional Series.
    new_observation = X_test.iloc[[0]]

    # predict() returns an array; [0] takes the prediction for this one row.
    predicted_class = best_model.predict(new_observation)[0]

    # predict_proba() returns rows by classes; [0, 1] selects row 0, class 1.
    predicted_probability = best_model.predict_proba(new_observation)[0, 1]

    # Report the selected model and its example prediction.
    print(f"\nSelected model by F1 score: {best_name}")
    print(f"Example predicted class: {predicted_class}")
    print(f"Example probability for class 1: {predicted_probability:.3f}")


if __name__ == "__main__":
    # Python sets __name__ to "__main__" when this file is run directly.
    # The guard prevents the example from running if another file imports it.
    main()
