"""Train and evaluate a practical random forest classifier."""

# Import NumPy to identify the positive class in the target labels.
import numpy as np
# Import the built-in breast-cancer teaching dataset; no data download is needed.
from sklearn.datasets import load_breast_cancer
# Import a simple baseline classifier that always predicts the most common class.
from sklearn.dummy import DummyClassifier
# Import the random forest classifier used in the example.
from sklearn.ensemble import RandomForestClassifier
# Import metrics for classification reports, confusion matrices, and model scores.
from sklearn.metrics import (
    accuracy_score,  # Measure the fraction of labels predicted correctly.
    balanced_accuracy_score,  # Average recall across classes.
    classification_report,  # Report precision, recall, F1-score, and support.
    confusion_matrix,  # Count actual versus predicted labels.
    log_loss,  # Evaluate the quality of predicted probabilities.
    precision_score,  # Measure the precision of the malignant positive class.
    recall_score,  # Measure the recall of the malignant positive class.
    roc_auc_score,  # Measure ranking quality across classification thresholds.
)
# Import a median imputer so the example pipeline can handle missing numeric values.
from sklearn.impute import SimpleImputer
# Import permutation importance to estimate held-out feature importance.
from sklearn.inspection import permutation_importance
# Import a pipeline to keep imputation and model fitting together.
from sklearn.pipeline import make_pipeline
# Import cross-validation search tools to tune only on training data.
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
# Import the dataset container type so the loader's result can be checked explicitly.
from sklearn.utils import Bunch


# Define the main workflow so the script can also be safely imported as a module.
def main():
    # Load the dataset's default metadata object rather than the tuple-returning API.
    dataset = load_breast_cancer(return_X_y=False)
    # Verify the loader returned its documented metadata container.
    if not isinstance(dataset, Bunch):
        # Stop with a clear error if a different loader return format is supplied.
        raise TypeError("Expected load_breast_cancer to return a Bunch dataset.")
    # Assign the 30 numeric measurements to the feature matrix.
    features = dataset.data
    # Convert the original target so malignant is positive class 1 and benign is 0.
    target = (dataset.target == 0).astype(int)
    # Save the feature names for readable importance output.
    feature_names = dataset.feature_names
    # Print the number of records and input features.
    print(f"Dataset shape: {features.shape[0]} rows, {features.shape[1]} features")
    # Print the meaning of the positive and negative class labels.
    print("Target mapping: 1 = malignant; 0 = benign")
    # Count missing feature values in each column and then total them.
    missing_value_count = int(np.isnan(features).sum())
    # Report the overall missing-value count before training.
    print(f"Missing feature values: {missing_value_count}")
    # Count the number of examples in each class.
    class_counts = np.bincount(target)
    # Print class counts by the defined negative and positive labels.
    print(f"Class counts: benign (0)={class_counts[0]}, malignant (1)={class_counts[1]}")
    # Print the percentage of each class to make imbalance visible.
    print(f"Malignant positive-class rate: {target.mean():.3f}")
    # Split into training and test rows before fitting any learned preprocessing.
    X_train, X_test, y_train, y_test = train_test_split(
        features,  # Supply all numeric features to the splitter.
        target,  # Supply labels so the split can preserve class proportions.
        test_size=0.25,  # Reserve one quarter of examples for final evaluation.
        random_state=42,  # Make the split reproducible.
        stratify=target,  # Keep similar class proportions in both splits.
    )  # Finish creating the fixed training and test sets.
    # Create a majority-class baseline to compare against the random forest.
    baseline = DummyClassifier(strategy="most_frequent")
    # Fit the baseline using training labels only.
    baseline.fit(X_train, y_train)
    # Predict the held-out labels using the majority-class baseline.
    baseline_predictions = baseline.predict(X_test)
    # Print the baseline's accuracy for context.
    print(f"\nMajority-class baseline accuracy: {accuracy_score(y_test, baseline_predictions):.3f}")
    # Build a pipeline that imputes numeric missing values before fitting a forest.
    pipeline = make_pipeline(
        SimpleImputer(strategy="median"),  # Learn training-fold medians and fill missing numeric entries.
        RandomForestClassifier(  # Configure the classifier used in each search candidate.
            n_estimators=150,  # Train 150 trees for each candidate model.
            class_weight="balanced_subsample",  # Adjust class weights within each tree's bootstrap sample.
            random_state=42,  # Keep forest randomness repeatable across candidates.
            n_jobs=-1,  # Use available CPU cores when fitting each forest.
        ),  # Finish configuring the random forest.
    )  # Finish combining imputation and classification in one pipeline.
    # Define a small hyperparameter search to keep the practical example manageable.
    parameter_grid = {
        "randomforestclassifier__max_features": ["sqrt", "log2"],  # Compare two feature-subsampling strategies.
        "randomforestclassifier__max_depth": [None, 10],  # Compare unrestricted and depth-limited trees.
        "randomforestclassifier__min_samples_leaf": [1, 3],  # Compare smaller and smoother leaf sizes.
    }  # Finish defining the eight candidate parameter combinations.
    # Set up shuffled stratified folds so each fold has representative class counts.
    cross_validation = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    # Configure grid search to choose candidates by cross-validated ROC-AUC.
    search = GridSearchCV(
        estimator=pipeline,  # Search over the pipeline so imputation is refit per fold.
        param_grid=parameter_grid,  # Evaluate each defined parameter combination.
        scoring="roc_auc",  # Select the setting with the strongest positive-class ranking.
        cv=cross_validation,  # Use five stratified folds drawn only from training data.
        n_jobs=-1,  # Run separate parameter/fold fits in parallel when possible.
        refit=True,  # Refit the winning pipeline on all training data after cross-validation.
    )  # Finish configuring the training-only search.
    # Fit all candidates using the training partition and its internal folds.
    search.fit(X_train, y_train)
    # Print the winning training-only cross-validation score.
    print(f"\nBest training cross-validation ROC-AUC: {search.best_score_:.3f}")
    # Print the selected hyperparameters for reproducibility.
    print(f"Best parameters: {search.best_params_}")
    # Retrieve the winning pipeline refit on the complete training partition.
    best_model = search.best_estimator_
    # Predict test labels once using the held-out test set.
    test_predictions = best_model.predict(X_test)
    # Predict the probability of malignant class 1 for each test record.
    test_probabilities = best_model.predict_proba(X_test)[:, 1]
    # Print a heading to separate final test metrics from training results.
    print("\nHeld-out test metrics")
    # Print ordinary accuracy for the selected test-set predictions.
    print(f"Accuracy: {accuracy_score(y_test, test_predictions):.3f}")
    # Print average class recall to account for both class labels.
    print(f"Balanced accuracy: {balanced_accuracy_score(y_test, test_predictions):.3f}")
    # Print precision for the malignant positive class.
    print(f"Malignant precision: {precision_score(y_test, test_predictions, zero_division=0):.3f}")
    # Print recall for the malignant positive class.
    print(f"Malignant recall: {recall_score(y_test, test_predictions, zero_division=0):.3f}")
    # Print ROC-AUC using predicted malignant probabilities.
    print(f"ROC-AUC: {roc_auc_score(y_test, test_probabilities):.3f}")
    # Print log loss to assess the quality of the test-set probability estimates.
    print(f"Log loss: {log_loss(y_test, test_probabilities):.3f}")
    # Print actual-versus-predicted counts for benign and malignant classes.
    print("Confusion matrix (rows=actual [benign, malignant], columns=predicted [benign, malignant]):")
    # Display the confusion matrix with a fixed class ordering.
    print(confusion_matrix(y_test, test_predictions, labels=[0, 1]))
    # Print the per-class precision, recall, F1-score, and support.
    print("Classification report:")
    # Display named classes with malignant as the positive class.
    print(
        classification_report(
            y_test,  # Supply the true held-out labels.
            test_predictions,  # Supply the labels predicted by the selected forest.
            labels=[0, 1],  # Keep the report's class ordering stable.
            target_names=["benign", "malignant"],  # Map numeric labels to human-readable classes.
            zero_division=0,  # Avoid undefined metric warnings when a class has no predictions.
        )  # Finish generating the per-class report.
    )  # Print the formatted per-class report.
    # Measure how much test ROC-AUC changes when each test feature is shuffled.
    importance = permutation_importance(
        best_model,  # Evaluate the tuned pipeline without changing its fitted parameters.
        X_test,  # Use held-out rows for post-evaluation model inspection.
        y_test,  # Use the known held-out labels as the importance reference.
        scoring="roc_auc",  # Measure feature reliance by the change in ROC-AUC.
        n_repeats=5,  # Repeat each shuffle five times to reduce random variation.
        random_state=42,  # Make the shuffle sequence reproducible.
        n_jobs=-1,  # Parallelize importance calculations when possible.
    )  # Finish calculating permutation importances.
    # Verify the result supports the named importance attributes used below.
    if not isinstance(importance, Bunch):
        # Stop with a clear error if scikit-learn returns an unexpected result type.
        raise TypeError("Expected permutation_importance to return a Bunch result.")
    # Sort feature positions from largest mean importance to smallest.
    important_indices = np.argsort(importance["importances_mean"])[::-1]
    # Print a heading for the leading permutation importance results.
    print("\nTop 10 permutation importances (mean ROC-AUC decrease):")
    # Iterate through the ten highest-ranked feature indices.
    for index in important_indices[:10]:
        # Print feature name, mean importance, and variation across shuffles.
        print(
            f"{feature_names[index]}: "
            f"{importance['importances_mean'][index]:.4f} "
            f"+/- {importance['importances_std'][index]:.4f}"
        )
    # Clarify the limitation of this public medical dataset example.
    print("\nThis is a teaching example, not a medical diagnostic tool.")


# Check whether Python is running this file as the main program.
if __name__ == "__main__":
    # Start the dataset, training, tuning, and evaluation workflow.
    main()
