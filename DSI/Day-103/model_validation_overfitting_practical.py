"""
Model Validation and Over-fitting: Practical Demonstration
==========================================================
Companion to MODEL_VALIDATION_AND_OVERFITTING_PRACTICAL.md.

Run from the DSI project directory:
    uv run python Day-103\\model_validation_overfitting_practical.py

The script creates reproducible synthetic customer-renewal data, checks
missingness, splits before preprocessing, compares a baseline and overfit
model, tunes a decision tree with cross-validation, and evaluates a selected
model once on a held-out test set.
"""

import numpy as np  # Import NumPy to create reproducible missing-value masks.
import pandas as pd  # Import pandas to store and inspect the example table.
from sklearn.compose import ColumnTransformer  # Route feature columns through different preparation steps.
from sklearn.datasets import make_classification  # Generate example classification data without downloading a file.
from sklearn.impute import SimpleImputer  # Fill missing numeric and category values.
from sklearn.linear_model import LogisticRegression  # Provide a relatively simple baseline classifier.
from sklearn.metrics import (  # Import metrics that summarize classification performance.
    accuracy_score,  # Measure the fraction of all predictions that are correct.
    balanced_accuracy_score,  # Average recall across classes to reduce class-imbalance distortion.
    classification_report,  # Show precision, recall, and F1 for each class.
)
from sklearn.model_selection import (  # Import tools for fair splitting and model selection.
    GridSearchCV,  # Compare hyperparameter choices using training-only cross-validation.
    StratifiedKFold,  # Keep class proportions similar in each cross-validation fold.
    train_test_split,  # Divide rows into training, validation, and test partitions.
)
from sklearn.pipeline import Pipeline  # Keep preprocessing and prediction steps together.
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # Encode categories and scale numeric features.
from sklearn.tree import DecisionTreeClassifier  # Use a tree that can illustrate over-fitting.

RANDOM_STATE = 42  # Fix random choices so the example can be reproduced.


def make_example_data():  # Define a function that creates a small realistic-style example table.
    """Create offline binary-classification data with missing values and an outlier."""  # Explain the function's returned data.
    X_array, target_array = make_classification(  # Generate synthetic numeric features and a binary target.
        n_samples=1200,  # Create enough rows to make train, validation, and test sets useful.
        n_features=8,  # Create eight numeric input columns.
        n_informative=5,  # Make five columns carry useful signal about the target.
        n_redundant=1,  # Make one column redundant with other generated features.
        n_repeated=0,  # Do not add exact repeated feature columns.
        n_classes=2,  # Create a two-class target for renewal classification.
        weights=[0.72, 0.28],  # Make one class less common to motivate balanced metrics.
        class_sep=0.9,  # Set classes to overlap enough that prediction is not trivial.
        flip_y=0.03,  # Add a small amount of label noise to imitate imperfect real data.
        random_state=RANDOM_STATE,  # Make the generated examples repeatable.
    )  # Finish generating the synthetic data.
    feature_names = [f"feature_{number}" for number in range(1, 9)]  # Give the eight numeric columns readable names.
    frame = pd.DataFrame(X_array, columns=feature_names)  # Put the generated measurements into a labeled table.
    frame["region"] = np.where(  # Create a category from feature_1 as an example of a nominal feature.
        frame["feature_1"] > 0.75,  # Check whether the first feature is above the positive threshold.
        "north",  # Label values above the threshold as north.
        np.where(frame["feature_1"] < -0.75, "south", "central"),  # Label low values south and the remainder central.
    )  # Finish deriving the example category.
    rng = np.random.default_rng(RANDOM_STATE)  # Create a local random generator for missing-value positions.
    missing_numeric_rows = rng.choice(frame.index, size=55, replace=False)  # Select distinct rows with a missing numeric value.
    frame.loc[missing_numeric_rows, "feature_2"] = np.nan  # Represent absent numeric measurements as missing.
    missing_category_rows = rng.choice(frame.index, size=40, replace=False)  # Select distinct rows with an absent category.
    frame.loc[missing_category_rows, "region"] = np.nan  # Represent absent category values as missing.
    frame.loc[0, "feature_1"] = 25.0  # Add one deliberately extreme value to prompt investigation rather than blind deletion.
    frame["renewed"] = target_array  # Add the answer column that the classifier will learn to predict.
    return frame  # Return the complete example table.


def build_preprocessor(numeric_features, categorical_features):  # Define preprocessing using only the named feature groups.
    """Create numeric and categorical transforms that will be fitted on training folds only."""  # Explain the preprocessor's purpose.
    numeric_steps = Pipeline(  # Create an ordered sequence for numeric columns.
        steps=[  # Begin listing the numeric preparation steps.
            ("impute", SimpleImputer(strategy="median", add_indicator=True)),  # Fill numeric gaps with training medians and preserve missingness signals.
            ("scale", StandardScaler()),  # Scale numbers using training-fold means and standard deviations.
        ]  # Finish listing numeric preparation steps.
    )  # Finish creating the numeric pipeline.
    categorical_steps = Pipeline(  # Create an ordered sequence for category columns.
        steps=[  # Begin listing the category preparation steps.
            ("impute", SimpleImputer(strategy="most_frequent")),  # Fill gaps with the most common category in the current training fold.
            ("encode", OneHotEncoder(handle_unknown="ignore")),  # Convert category labels into indicator columns and tolerate new labels.
        ]  # Finish listing category preparation steps.
    )  # Finish creating the category pipeline.
    return ColumnTransformer(  # Combine transformations and preserve their connection to the correct columns.
        transformers=[  # Begin listing column groups and their transformations.
            ("numeric", numeric_steps, numeric_features),  # Impute and scale all named numeric columns.
            ("categorical", categorical_steps, categorical_features),  # Impute and one-hot encode the category columns.
        ]  # Finish listing column transformations.
    )  # Return the combined feature-preparation object.


def build_pipeline(classifier, numeric_features, categorical_features):  # Bundle data preparation with a selected classifier.
    """Build a full model so each fit learns preprocessing from its own training rows."""  # Explain the leakage-prevention purpose.
    return Pipeline(  # Return a pipeline that can be safely fitted within cross-validation.
        steps=[  # Begin the ordered preparation and prediction steps.
            ("prepare", build_preprocessor(numeric_features, categorical_features)),  # Learn imputations, categories, and scaling inside each fit.
            ("classifier", classifier),  # Train the supplied prediction algorithm after preprocessing.
        ]  # Finish the pipeline steps.
    )  # Finish creating the complete model pipeline.


def score_model(model, X_rows, y_rows):  # Calculate the two metrics used in the comparison.
    """Return balanced accuracy and ordinary accuracy for one set of rows."""  # Document the returned metric pair.
    row_predictions = model.predict(X_rows)  # Predict class labels using the already-fitted pipeline.
    balanced = balanced_accuracy_score(y_rows, row_predictions)  # Measure average recall across both classes.
    accuracy = accuracy_score(y_rows, row_predictions)  # Measure the overall fraction of correct predictions.
    return balanced, accuracy  # Return metrics in a stable order for reporting.


def main():  # Define the program entry point.
    """Run the validation example from data inspection through final test scoring."""  # Summarize the sequence of the demonstration.
    frame = make_example_data()  # Create the synthetic customer-renewal table.
    target_name = "renewed"  # Name the column whose value the model should predict.
    numeric_features = [column for column in frame.columns if column.startswith("feature_")]  # Identify the eight numeric input columns.
    categorical_features = ["region"]  # Identify the nominal region column.
    print("DATA CHECKS")  # Mark the start of the dataset-inspection output.
    print(f"Rows: {len(frame)} | Columns: {frame.shape[1]}")  # Print the number of example records and columns.
    print("Missing values by column:")  # Explain the missingness summary that follows.
    print(frame.isna().sum().to_string())  # Count missing cells before choosing imputation.
    print(f"Target class counts: {frame[target_name].value_counts().sort_index().to_dict()}")  # Show whether renewal outcomes are balanced.
    features = frame.drop(columns=target_name)  # Separate model inputs from the answer column.
    target = frame[target_name]  # Keep the answer labels separate from model inputs.
    X_train_and_validation, X_test, y_train_and_validation, y_test = train_test_split(  # Set aside the final test rows before fitting transformations.
        features,  # Pass input columns, not the target, to the split function.
        target,  # Pass labels so their rows stay aligned with the inputs.
        test_size=0.20,  # Reserve 20 percent of all rows for the final test.
        stratify=target,  # Preserve approximate class proportions in both partitions.
        random_state=RANDOM_STATE,  # Make the split repeatable.
    )  # Finish the first split into development data and final test data.
    X_train, X_validation, y_train, y_validation = train_test_split(  # Split development data into training and validation portions.
        X_train_and_validation,  # Use only rows that are not in the final test set.
        y_train_and_validation,  # Keep labels aligned with those development rows.
        test_size=0.25,  # Make validation 25 percent of development data, or 20 percent overall.
        stratify=y_train_and_validation,  # Preserve class proportions in training and validation.
        random_state=RANDOM_STATE,  # Make the second split repeatable too.
    )  # Finish the 60/20/20 train/validation/test split.
    print(f"Training feature_1 1st/99th percentiles: {X_train['feature_1'].quantile([0.01, 0.99]).round(2).to_dict()}")  # Inspect a robust range using training rows only.
    print("\nDATA SPLIT")  # Mark the split summary.
    print(f"Training rows: {len(X_train)} | Validation rows: {len(X_validation)} | Test rows: {len(X_test)}")  # Confirm the split sizes.
    baseline = build_pipeline(  # Create a simple model with all preparation inside its pipeline.
        LogisticRegression(max_iter=1000, class_weight="balanced", random_state=RANDOM_STATE),  # Use regularized logistic regression and account for class imbalance.
        numeric_features,  # Tell the preprocessing pipeline which columns are numeric.
        categorical_features,  # Tell the preprocessing pipeline which columns are categories.
    )  # Finish creating the logistic-regression baseline.
    baseline.fit(X_train, y_train)  # Learn preprocessing and classifier parameters from training rows only.
    deep_tree = build_pipeline(  # Create a flexible tree as a deliberate over-fitting comparison.
        DecisionTreeClassifier(random_state=RANDOM_STATE),  # Allow the tree to grow without a depth limit.
        numeric_features,  # Tell the preparation pipeline which columns are numeric.
        categorical_features,  # Tell the preparation pipeline which columns are categories.
    )  # Finish creating the unrestricted-tree pipeline.
    deep_tree.fit(X_train, y_train)  # Fit the unrestricted tree using training rows only.
    cross_validation = StratifiedKFold(  # Define repeatable, class-aware cross-validation folds.
        n_splits=5,  # Use five folds for a modest, practical search.
        shuffle=True,  # Shuffle rows before forming folds because this example is not time ordered.
        random_state=RANDOM_STATE,  # Make fold assignments repeatable.
    )  # Finish defining the cross-validation splitter.
    search = GridSearchCV(  # Compare a small collection of tree complexities using training-only CV.
        estimator=build_pipeline(  # Search over a complete pipeline, refitting preparation separately inside each fold.
            DecisionTreeClassifier(random_state=RANDOM_STATE),  # Use decision trees for the depth and leaf-size search.
            numeric_features,  # Send numeric columns through numeric preparation inside each fold.
            categorical_features,  # Send region through category preparation inside each fold.
        ),  # Finish defining the estimator that GridSearchCV evaluates.
        param_grid={  # List model-complexity settings to compare.
            "classifier__max_depth": [1, 2, 3, 4, 6, None],  # Try shallow through unrestricted tree depths.
            "classifier__min_samples_leaf": [1, 5, 10],  # Try requiring more observations in each leaf to reduce memorization.
        },  # Finish the search space.
        scoring="balanced_accuracy",  # Choose a metric that gives each class equal importance.
        cv=cross_validation,  # Use the same defined folds for each candidate setting.
        n_jobs=-1,  # Run independent candidate fits using available CPU cores.
        refit=True,  # Refit the best pipeline on all training rows after selecting settings.
    )  # Finish configuring the cross-validation search.
    search.fit(X_train, y_train)  # Choose settings using training rows and their CV folds, never validation or test labels.
    tuned_tree = search.best_estimator_  # Retrieve the best tree pipeline refitted on all training rows.
    candidates = {  # Store fitted models under readable names for consistent score reporting.
        "Logistic regression baseline": baseline,  # Include the regularized linear baseline.
        "Unrestricted decision tree": deep_tree,  # Include the flexible tree to reveal a possible training/validation gap.
        "Cross-validated decision tree": tuned_tree,  # Include the tree complexity selected by training-only CV.
    }  # Finish collecting fitted model candidates.
    print("\nCROSS-VALIDATION")  # Mark the hyperparameter-search results.
    print(f"Best CV balanced accuracy: {search.best_score_:.3f}")  # Show the mean CV score for the selected settings.
    print(f"Selected tree settings: {search.best_params_}")  # Show the tree settings selected without looking at test rows.
    print("\nTRAINING AND VALIDATION COMPARISON")  # Mark the model comparison table.
    print(f"{'Model':34} {'Train bal.acc.':>14} {'Valid bal.acc.':>14} {'Gap':>9}")  # Print column headings.
    validation_scores: dict[str, float] = {}  # Keep named validation scores for type-safe model selection.
    for model_name, candidate in candidates.items():  # Evaluate each already-fitted candidate on the same partitions.
        train_balanced, _ = score_model(candidate, X_train, y_train)  # Measure training performance to reveal memorization.
        validation_balanced, _ = score_model(candidate, X_validation, y_validation)  # Measure performance on rows not used to fit this model.
        validation_scores[model_name] = validation_balanced  # Save validation balanced accuracy for selecting a candidate.
        gap = train_balanced - validation_balanced  # Calculate the training-minus-validation generalization gap.
        print(f"{model_name:34} {train_balanced:14.3f} {validation_balanced:14.3f} {gap:9.3f}")  # Display both scores and the gap.
    selected_name = max(validation_scores, key=lambda name: validation_scores[name])  # Select the candidate with the highest validation balanced accuracy.
    selected_model = candidates[selected_name]  # Retrieve the chosen, already-fitted model pipeline.
    print(f"\nSelected using validation data: {selected_name}")  # State which model was selected before test evaluation.
    test_balanced, test_accuracy = score_model(selected_model, X_test, y_test)  # Make the final test predictions and calculate metrics once.
    test_predictions = selected_model.predict(X_test)  # Retain predictions to print a per-class test report.
    print("\nFINAL HELD-OUT TEST RESULTS")  # Mark the final estimate on previously untouched rows.
    print(f"Test balanced accuracy: {test_balanced:.3f}")  # Report equal-weight average recall across test classes.
    print(f"Test accuracy:          {test_accuracy:.3f}")  # Report the overall fraction of correct test predictions.
    print(classification_report(y_test, test_predictions, target_names=["not renewed", "renewed"], zero_division=0))  # Report class-specific precision, recall, and F1.
    print("Interpretation: compare the unrestricted tree's training and validation scores for an over-fitting signal.")  # Tell a beginner how to read the generalization gap.
    print("The final test result estimates performance after model selection; do not use it to tune the next model.")  # Reinforce the rule that protects the test estimate.


if __name__ == "__main__":  # Run the demonstration only when this file is executed directly.
    main()  # Start the end-to-end example.
