"""Train and evaluate a beginner-friendly logistic regression classifier."""

# sklearn.datasets contains sample datasets and functions for loading them.
# Load a small, well-known dataset included with the scikit-learn package.
from sklearn.datasets import load_breast_cancer

# sklearn.impute provides ways to replace missing feature values.
from sklearn.impute import SimpleImputer

# sklearn.linear_model contains linear models; this one estimates class probabilities.
from sklearn.linear_model import LogisticRegression

# sklearn.metrics provides functions for evaluating predictions and probabilities.
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

# sklearn.model_selection contains data-splitting and model-selection tools.
from sklearn.model_selection import train_test_split

# sklearn.pipeline chains preprocessing and a classifier into one estimator.
from sklearn.pipeline import Pipeline

# sklearn.preprocessing provides feature transformations such as standardization.
from sklearn.preprocessing import StandardScaler


def main() -> None:
    """Load data, fit the pipeline, evaluate it, and predict one example."""

    # Load the dataset as a DataFrame with readable feature names.
    dataset = load_breast_cancer(as_frame=True)
    # Keep the feature columns and target together for a quick inspection.
    data = dataset.frame
    # Print the number of observations and total columns, including the target.
    print(f"Dataset shape (rows, columns): {data.shape}")
    # Count missing cells before deciding how preprocessing should handle them.
    print(f"Missing cells: {data.isna().sum().sum()}")
    # Keep measurements in X and the answer to predict in y.
    X = data.drop(columns="target")
    # Map numeric target codes to readable class names without adding them to X.
    # target_names contains the text labels; tolist() makes a regular Python list.
    # enumerate pairs each numeric code (0, 1) with its label; dict makes a lookup.
    # map() replaces each numeric target code with its readable class name.
    y = data["target"].map(dict(enumerate(dataset.target_names.tolist())))
    # Show the class names to make the prediction labels understandable.
    print(f"Classes: {sorted(set(y))}")

    # Split before fitting any imputer, scaler, or classifier.
    X_train, X_test, y_train, y_test = train_test_split(
        X,  # Provide feature rows to divide into training and test sets.
        y,  # Keep each class label paired with its feature row.
        test_size=0.2,  # Reserve 20 percent of observations for final evaluation.
        random_state=42,  # Make the split reproducible when the script is rerun.
        stratify=y,  # Preserve a similar class balance in each split.
    )  # Finish creating the four train/test objects.
    # Print split sizes so it is clear which data is used for learning.
    print(f"Training rows: {len(X_train)}; test rows: {len(X_test)}")

    # Define a pipeline that learns preprocessing values from training data.
    model = Pipeline(
        steps=[
            # Fill missing numeric inputs with the median learned during fit.
            ("imputer", SimpleImputer(strategy="median")),
            # Standardize features using the training mean and standard deviation.
            ("scaler", StandardScaler()),
            # Fit a logistic regression classifier with enough solver iterations.
            ("classifier", LogisticRegression(max_iter=2_000, random_state=42)),
        ]  # Run these steps in order as one model pipeline.
    )  # Finish assembling preprocessing and classification.
    # Learn the imputation values, scaling values, and classifier coefficients.
    model.fit(X_train, y_train)
    # Predict class names for the held-out test observations.
    predictions = model.predict(X_test)
    # Measure the fraction of all test predictions that are correct.
    accuracy = accuracy_score(y_test, predictions)
    # Print accuracy as a simple first summary, not the only metric.
    print(f"\nAccuracy: {accuracy:.3f}")
    # Print precision, recall, and F1 score for each class.
    print(
        classification_report(
            y_test,  # Supply the known test-set classes.
            predictions,  # Supply the model's predicted test-set classes.
            labels=["benign", "malignant"],  # Print both classes in this order.
            zero_division=0,  # Report zero instead of a warning for undefined scores.
        )  # Create the readable per-class metric report.
    )  # Print the report to the console.
    # Count correct and incorrect predictions in a consistent class order.
    matrix = confusion_matrix(
        y_test,  # Supply the known test-set classes.
        predictions,  # Supply the model's predicted test-set classes.
        labels=["benign", "malignant"],  # Keep matrix row/column order explicit.
    )  # Count actual versus predicted classes.
    # Label the matrix axes so its counts can be interpreted correctly.
    print("Confusion matrix (rows = actual; columns = predicted; benign, malignant):")
    # Display the confusion matrix counts.
    print(matrix)
    # Find the model probability column corresponding to the malignant class.
    # classes_ lists the classifier's known labels in probability-column order.
    # Find the position of "malignant" so we select the correct probability column.
    malignant_index = list(model.named_steps["classifier"].classes_).index("malignant")
    # Extract the estimated malignant probability for every test observation.
    # predict_proba gives one row per observation and one column per class.
    # [:, malignant_index] selects the malignant probability from every row.
    malignant_probabilities = model.predict_proba(X_test)[:, malignant_index]
    # Measure how well the model ranks malignant cases above benign cases.
    auc = roc_auc_score(y_test == "malignant", malignant_probabilities)
    # Print ROC-AUC, which evaluates ranking across possible thresholds.
    print(f"ROC-AUC: {auc:.3f}")

    # Select one held-out observation while keeping it in a one-row DataFrame.
    new_observation = X_test.iloc[[0]]
    # Predict the class for the selected observation.
    predicted_class = model.predict(new_observation)[0]
    # Get the selected observation's estimated probability for each class.
    class_probabilities = model.predict_proba(new_observation)[0]
    # Select the probability associated with the malignant class.
    malignant_probability = class_probabilities[malignant_index]
    # Print the predicted label for this example observation.
    print(f"\nExample predicted class: {predicted_class}")
    # Print the estimated probability that the example is malignant.
    print(f"Example estimated malignant probability: {malignant_probability:.3f}")
    # Clarify that the teaching example must not be used for medical decisions.
    print("Teaching example only; not a medical diagnostic tool.")


# Run the example only when this file is executed directly.
if __name__ == "__main__":
    # Start the tutorial workflow.
    main()
