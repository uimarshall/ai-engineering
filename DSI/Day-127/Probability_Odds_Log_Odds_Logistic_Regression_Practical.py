"""Practical beginner example of probability, odds, and logistic regression."""

# Import NumPy for reproducible random data generation and numerical calculations.
import numpy as np
# Import the tools used to build a data-safe preprocessing and modeling pipeline.
from sklearn.pipeline import make_pipeline
# Import logistic regression, the binary classification model used in this example.
from sklearn.linear_model import LogisticRegression
# Import a scaler that standardizes features using training-set statistics.
from sklearn.preprocessing import StandardScaler
# Import metrics for evaluating labels and predicted probabilities.
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, log_loss, roc_auc_score
# Import a stratified train/test splitter so both sets retain similar class proportions.
from sklearn.model_selection import train_test_split


# Define the program entry point so this example runs when executed as a script.
def main():
    # Create a random number generator with a fixed seed so results are repeatable.
    rng = np.random.default_rng(42)
    # Set the number of fictional customer records to generate.
    sample_count = 1200
    # Generate integer website-visit counts from zero through ten for each customer.
    website_visits = rng.integers(0, 11, size=sample_count)
    # Generate discount percentages from zero through thirty for each customer.
    discount_percent = rng.integers(0, 31, size=sample_count)
    # Generate previous-purchase counts from zero through five for each customer.
    previous_purchases = rng.integers(0, 6, size=sample_count)
    # Combine the three input columns into a two-dimensional feature matrix.
    features = np.column_stack((website_visits, discount_percent, previous_purchases))
    # Name the input columns so printed coefficients are easy to understand.
    feature_names = ("website_visits", "discount_percent", "previous_purchases")
    # Calculate an illustrative true log-odds score from the generated features.
    true_log_odds = (  # Start the illustrative formula that creates purchase log-odds.
        -4.2  # Set the baseline log-odds before adding customer features.
        + 0.35 * website_visits  # Add a positive contribution for website visits.
        + 0.045 * discount_percent  # Add a positive contribution for the discount.
        + 0.65 * previous_purchases  # Add a positive contribution for prior purchases.
    )  # Finish the log-odds formula.
    # Convert the log-odds score into a probability with the sigmoid function.
    true_probability = 1 / (1 + np.exp(-true_log_odds))
    # Draw a binary purchase outcome using each customer's generated probability.
    purchased = rng.binomial(1, true_probability)
    # Print a heading for the probability, odds, and log-odds demonstration.
    print("Probability, odds, and log-odds example")
    # Set an example probability to demonstrate the conversions by hand.
    example_probability = 0.8
    # Convert probability to odds by dividing by the chance of no event.
    example_odds = example_probability / (1 - example_probability)
    # Convert odds back to probability to check the inverse calculation.
    probability_from_odds = example_odds / (1 + example_odds)
    # Convert the odds to log-odds using the natural logarithm.
    example_log_odds = np.log(example_odds)
    # Print the example probability, odds, and log-odds with readable precision.
    print(
        f"p={example_probability:.2f} -> odds={example_odds:.2f} "  # Format probability and odds.
        f"-> log-odds={example_log_odds:.3f} "  # Append the natural log of the odds.
        f"-> p={probability_from_odds:.2f}"  # Append the converted-back probability.
    )
    # Print a blank line to separate the math example from model training output.
    print()
    # Split the data before any scaler is fitted to prevent test-data leakage.
    X_train, X_test, y_train, y_test = train_test_split(
        features,  # Provide all generated customer features to the splitter.
        purchased,  # Provide the binary outcome labels to the splitter.
        test_size=0.25,  # Reserve one quarter of examples for final testing.
        random_state=42,  # Make the train/test partition reproducible.
        stratify=purchased,  # Preserve class proportions in both partitions.
    )  # Finish creating the training and test partitions.
    # Build a pipeline that fits scaling and logistic regression on training data.
    model = make_pipeline(
        StandardScaler(),  # Standardize features using training-set means and scales.
        LogisticRegression(  # Create the regularized binary logistic classifier.
            C=1.0,  # Set the inverse regularization strength.
            max_iter=1000,  # Allow enough optimization iterations for convergence.
            random_state=42,  # Fix model randomness where the solver uses it.
        ),  # Finish configuring the classifier.
    )  # Finish assembling preprocessing and model into one pipeline.
    # Fit the scaler and classifier using training examples only.
    model.fit(X_train, y_train)
    # Predict positive-class probabilities for the held-out test examples.
    test_probabilities = model.predict_proba(X_test)[:, 1]
    # Convert test probabilities to class labels using the usual 0.5 threshold.
    test_predictions = (test_probabilities >= 0.5).astype(int)
    # Print the evaluation section heading.
    print("Held-out test results")
    # Print accuracy, the fraction of test labels predicted correctly.
    print(f"Accuracy: {accuracy_score(y_test, test_predictions):.3f}")
    # Print the confusion matrix with rows as actual and columns as predicted labels.
    print("Confusion matrix (rows=actual [0, 1], columns=predicted [0, 1]):")
    # Display the confusion matrix values.
    print(confusion_matrix(y_test, test_predictions))
    # Print precision, recall, F1-score, and sample counts for both classes.
    print("Classification report:")
    # Display the formatted per-class metrics.
    print(classification_report(y_test, test_predictions, zero_division=0))
    # Print ROC-AUC to describe ranking quality across classification thresholds.
    print(f"ROC-AUC: {roc_auc_score(y_test, test_probabilities):.3f}")
    # Print log loss to evaluate the quality of predicted probabilities.
    print(f"Log loss: {log_loss(y_test, test_probabilities):.3f}")
    # Retrieve the fitted logistic-regression step from the pipeline.
    classifier = model.named_steps["logisticregression"]
    # Print a heading to explain the scale of the learned weights.
    print("\nLearned coefficients (per one training-set standard deviation):")
    # Pair each feature name with its fitted standardized coefficient.
    for name, coefficient in zip(feature_names, classifier.coef_[0]):
        # Convert the coefficient into an odds ratio for a one-standard-deviation increase.
        odds_ratio = np.exp(coefficient)
        # Print the coefficient and odds ratio for this feature.
        print(f"{name}: coefficient={coefficient:.3f}, odds ratio={odds_ratio:.3f}")
    # Define a fictional customer with six visits, a ten-percent discount, and one prior purchase.
    example_customer = np.array([[6, 10, 1]])
    # Estimate the example customer's probability of purchase using the fitted pipeline.
    customer_probability = model.predict_proba(example_customer)[0, 1]
    # Convert the estimated probability into odds.
    customer_odds = customer_probability / (1 - customer_probability)
    # Apply the 0.5 threshold to produce the example customer's predicted class.
    customer_prediction = int(customer_probability >= 0.5)
    # Print a heading for the single-customer example.
    print("\nExample customer")
    # Print the estimated probability, odds, and thresholded label.
    print(
        f"Estimated purchase probability: {customer_probability:.3f}; "  # Format the estimated probability.
        f"odds: {customer_odds:.3f}; predicted class at threshold 0.5: "  # Add odds and threshold context.
        f"{customer_prediction}"  # Add the final binary prediction.
    )
    # Remind the reader that generated outcomes are illustrative, not real evidence.
    print("Reminder: this example uses synthetic data and is for learning only.")


# Run the program entry point only when this file is executed directly.
if __name__ == "__main__":
    # Start the example workflow.
    main()
