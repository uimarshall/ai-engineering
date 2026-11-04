"""Beginner-friendly classification tree example using synthetic student data."""

# NumPy provides random-number generation and numeric operations.
import numpy as np
# Path builds a stable output path beside this script.
from pathlib import Path
# Pandas stores the example features in a readable table.
import pandas as pd
# Matplotlib draws the fitted decision tree.
import matplotlib.pyplot as plt
# SimpleImputer fills missing numeric feature values from the training data.
from sklearn.impute import SimpleImputer
# DummyClassifier creates a simple baseline that ignores the input features.
from sklearn.dummy import DummyClassifier
# DecisionTreeClassifier learns the classification rules.
from sklearn.tree import DecisionTreeClassifier, plot_tree
# train_test_split separates training examples from held-out test examples.
from sklearn.model_selection import train_test_split
# Pipeline ensures imputation is learned on training data and reused consistently.
from sklearn.pipeline import Pipeline
# These metrics summarize classification performance in complementary ways.
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

# Fix the random generator seed so the synthetic example is repeatable.
RANDOM_STATE = 42
# Create a random number generator that we will reuse throughout the example.
rng = np.random.default_rng(RANDOM_STATE)
# Define the names of the input columns that the tree will use.
FEATURE_NAMES = ["study_hours", "exam_1_passed", "attendance_percent"]
# Define readable names for the integer-encoded target classes.
CLASS_NAMES = ["Fail", "Pass"]


# Print the slide's small example and show how one leaf probability is calculated.
print("--- Slide example: interpreting a leaf ---")
# Store the Exam 2 class counts for students who studied at most 4.2 hours and passed Exam 1.
exam_1_pass_leaf = {"Pass": 11, "Fail": 7}
# Calculate the observed Exam 2 pass rate in that leaf.
leaf_pass_rate = exam_1_pass_leaf["Pass"] / sum(exam_1_pass_leaf.values())
# Report the sample counts and estimated probability for the leaf.
print(f"Exam 1-pass leaf: {exam_1_pass_leaf}")
# Show the probability as a percentage, rounded to the nearest whole number.
print(f"Estimated Exam 2 pass rate: {leaf_pass_rate:.0%}")
# Explain the predicted class when the binary decision threshold is 50%.
print(f"Predicted class at a 50% threshold: {'Pass' if leaf_pass_rate >= 0.5 else 'Fail'}")

# Set the number of fictional student records to generate.
number_of_students = 1200
# Generate each student's study hours as a value from 0 to 10 hours per week.
study_hours = rng.uniform(0, 10, size=number_of_students)
# Generate whether each student passed Exam 1, with 1 meaning pass and 0 meaning fail.
exam_1_passed = rng.binomial(1, 0.52, size=number_of_students)
# Generate attendance percentages between 50 and 100 percent.
attendance_percent = rng.uniform(50, 100, size=number_of_students)
# Give each student a starting log-odds of passing Exam 2.
log_odds_of_passing = -3.2
# Add a positive study-hours contribution to the log-odds.
log_odds_of_passing += 0.62 * study_hours
# Add a contribution from passing Exam 1.
log_odds_of_passing += 1.15 * exam_1_passed
# Add a modest contribution from attendance relative to 75 percent.
log_odds_of_passing += 0.04 * (attendance_percent - 75)
# Convert the log-odds into a probability between zero and one.
probability_of_passing = 1 / (1 + np.exp(-log_odds_of_passing))
# Generate the binary Exam 2 result from each student's probability of passing.
exam_2_passed = rng.binomial(1, probability_of_passing)

# Assemble the input feature values into a table with descriptive column names.
features = pd.DataFrame(
    {
        "study_hours": study_hours,
        "exam_1_passed": exam_1_passed,
        "attendance_percent": attendance_percent,
    }
)
# Store the target labels separately so they cannot accidentally become an input feature.
target = pd.Series(exam_2_passed, name="exam_2_passed")

# Select about two percent of rows in each feature column to demonstrate missing data.
missing_mask = rng.random(size=features.shape) < 0.02
# Replace the selected feature values with NaN, leaving the target labels intact.
features = features.mask(missing_mask)
# Print the number of missing values per feature before preprocessing.
print("\n--- Generated data checks ---")
# Show feature missingness so the imputation step is transparent.
print("Missing values by feature:")
# Display how many values are missing in each input column.
print(features.isna().sum())
# Show the class counts so we can see the target distribution.
print("\nTarget class counts (0=Fail, 1=Pass):")
# Print the number of examples in each target class.
print(target.value_counts().sort_index())

# Split the data before fitting any imputer or classifier to prevent data leakage.
X_train, X_test, y_train, y_test = train_test_split(
    features,
    target,
    test_size=0.25,
    stratify=target,
    random_state=RANDOM_STATE,
)
# Report the sizes of the training and held-out test partitions.
print(f"\nTraining rows: {len(X_train)}")
# Display the number of examples reserved for final evaluation.
print(f"Test rows: {len(X_test)}")

# Create a baseline pipeline that imputes missing values then predicts the most common class.
baseline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", DummyClassifier(strategy="most_frequent")),
    ]
)
# Fit the baseline using training data only.
baseline.fit(X_train, y_train)

# Create a constrained tree to demonstrate a smaller, more interpretable model.
shallow_tree = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        (
            "classifier",
            DecisionTreeClassifier(
                criterion="gini",
                max_depth=3,
                min_samples_leaf=15,
                random_state=RANDOM_STATE,
            ),
        ),
    ]
)
# Fit the shallow tree and its imputer on training data only.
shallow_tree.fit(X_train, y_train)

# Create an unconstrained tree to illustrate how a deep tree can overfit.
deep_tree = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", DecisionTreeClassifier(random_state=RANDOM_STATE)),
    ]
)
# Fit the deep tree and its imputer on the same training rows for a fair comparison.
deep_tree.fit(X_train, y_train)


# Define a helper that prints training and test metrics for a fitted model.
def report_model(name, model):
    """Print accuracy, positive-class metrics, and confusion matrices."""
    # Generate predictions on the training data to help identify overfitting.
    train_predictions = model.predict(X_train)
    # Generate predictions on held-out data for generalization evaluation.
    test_predictions = model.predict(X_test)
    # Print the model label to make the following metrics easy to identify.
    print(f"\n--- {name} ---")
    # Report training accuracy, which is not a substitute for test performance.
    print(f"Training accuracy: {accuracy_score(y_train, train_predictions):.3f}")
    # Report held-out accuracy as the share of test predictions that are correct.
    print(f"Test accuracy:     {accuracy_score(y_test, test_predictions):.3f}")
    # Report pass precision: among predicted passes, the fraction that passed.
    print(f"Pass precision:    {precision_score(y_test, test_predictions, zero_division=0):.3f}")
    # Report pass recall: among actual passes, the fraction identified.
    print(f"Pass recall:       {recall_score(y_test, test_predictions, zero_division=0):.3f}")
    # Report the harmonic mean of pass precision and pass recall.
    print(f"Pass F1:           {f1_score(y_test, test_predictions, zero_division=0):.3f}")
    # Label the confusion matrix's row and column order.
    print("Confusion matrix [[true fail predicted fail, true fail predicted pass],")
    # Complete the explanation of the confusion matrix layout.
    print("                  [true pass predicted fail, true pass predicted pass]]:")
    # Print counts with Fail=0 first and Pass=1 second.
    print(confusion_matrix(y_test, test_predictions, labels=[0, 1]))
    # Print per-class precision, recall, F1, and support for the test examples.
    print("Classification report:")
    # Include readable class labels in the report.
    print(
        classification_report(
            y_test,
            test_predictions,
            labels=[0, 1],
            target_names=CLASS_NAMES,
            zero_division=0,
        )
    )


# Evaluate the majority-class baseline to set a minimum useful reference point.
report_model("Majority-class baseline", baseline)
# Evaluate the regularized tree to see its test performance and training-test gap.
report_model("Depth-limited tree", shallow_tree)
# Evaluate the unconstrained tree to demonstrate the potential overfitting gap.
report_model("Unconstrained tree", deep_tree)

# Build one new fictional student's feature row using the same feature names as training.
new_student = pd.DataFrame(
    {
        "study_hours": [3.5],
        "exam_1_passed": [1],
        "attendance_percent": [85.0],
    }
)
# Ask the shallow tree for the predicted class for this student.
predicted_class = shallow_tree.predict(new_student)[0]
# Retrieve the class probability estimates from the leaf reached by this student.
class_probabilities = shallow_tree.predict_proba(new_student)[0]
# Find the position of the Pass class in the model's learned class list.
pass_class_index = list(shallow_tree.classes_).index(1)
# Print the predicted class in a readable form.
print("\n--- Example prediction for a new student ---")
# Convert the encoded prediction back to its class label.
print(f"Predicted Exam 2 result: {CLASS_NAMES[predicted_class]}")
# Show the model's estimated probability for passing Exam 2.
print(f"Estimated probability of Pass: {class_probabilities[pass_class_index]:.1%}")

# Extract the fitted decision tree from the preprocessing pipeline for plotting.
fitted_tree = shallow_tree.named_steps["classifier"]
# Create a figure and axes with enough space for the tree's labels.
figure, axes = plt.subplots(figsize=(16, 8))
# Draw up to three levels of the tree using readable feature and class names.
plot_tree(
    fitted_tree,
    feature_names=FEATURE_NAMES,
    class_names=CLASS_NAMES,
    filled=True,
    rounded=True,
    proportion=True,
    max_depth=3,
    ax=axes,
)
# Add a title that reminds readers this is a constrained synthetic-data example.
axes.set_title("Depth-limited classification tree for synthetic student data")
# Adjust spacing so labels are not cut off.
figure.tight_layout()
# Build a path for the generated tree image in the same folder as this script.
plot_path = Path(__file__).with_name("decision_tree_classification_tree.png")
# Save the tree plot so the script also works in non-interactive terminals.
figure.savefig(plot_path, dpi=150, bbox_inches="tight")
# Tell the user where the generated tree visualization was saved.
print(f"\nTree plot saved to: {plot_path}")
# Close the figure to release graphical resources after saving it.
plt.close(figure)
