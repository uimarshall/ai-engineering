"""
Practical examples for finding the best line using least squares.

Run with:
    python least_squares_regression_examples.py

The examples use only NumPy, Matplotlib, and scikit-learn.
"""

# Import NumPy for numerical arrays and calculations.
import numpy as np

# Import Matplotlib's pyplot module for plotting.
import matplotlib.pyplot as plt

# Import the ordinary least-squares model from scikit-learn.
from sklearn.linear_model import LinearRegression

# Import error and score functions for model evaluation.
from sklearn.metrics import mean_squared_error, r2_score


def demonstrate_least_squares_formulas():
    """Fit a simple regression line using the standard least-squares formulas."""

    # Create the input feature, hours studied, as a floating-point NumPy array.
    x = np.array([1, 2, 3, 5, 6, 8], dtype=float)

    # Create the target values, exam scores, as a floating-point NumPy array.
    y = np.array([52, 58, 61, 73, 79, 86], dtype=float)

    # Calculate the mean of the input values.
    x_mean = x.mean()

    # Calculate the mean of the target values.
    y_mean = y.mean()

    # Calculate the numerator of the least-squares slope formula.
    numerator = ((x - x_mean) * (y - y_mean)).sum()

    # Calculate the denominator of the least-squares slope formula.
    denominator = ((x - x_mean) ** 2).sum()

    # Calculate the slope that minimizes squared errors.
    slope = numerator / denominator

    # Calculate the intercept from the means and the slope.
    intercept = y_mean - slope * x_mean

    # Predict all training targets with the fitted line.
    predictions = intercept + slope * x

    # Calculate each residual: actual target minus predicted target.
    residuals = y - predictions

    # Square every residual before combining them.
    squared_errors = residuals ** 2

    # Calculate the sum of squared errors.
    sse = squared_errors.sum()

    # Calculate the total variation around the target mean.
    total_variation = ((y - y_mean) ** 2).sum()

    # Calculate R squared from SSE and total variation.
    r_squared = 1 - sse / total_variation

    # Calculate root mean squared error in the target's units.
    rmse = np.sqrt(squared_errors.mean())

    # Print the fitted intercept and slope.
    print("1. Least-squares formulas")
    print(f"   Intercept: {intercept:.2f}")
    print(f"   Slope: {slope:.2f}")
    print(f"   Fitted line: score = {intercept:.2f} + {slope:.2f} * hours")
    print(f"   Sum of squared errors: {sse:.2f}")
    print(f"   RMSE: {rmse:.2f}")
    print(f"   R squared: {r_squared:.3f}")

    # Choose a new input for which we want a prediction.
    new_x = 7

    # Apply the fitted line to the new input.
    new_prediction = intercept + slope * new_x

    # Print the prediction for seven hours of study.
    print(f"   Predicted score after {new_x} hours: {new_prediction:.2f}\n")

    # Create a new plotting window with a useful size.
    plt.figure(figsize=(8, 5))

    # Draw the observed points as blue circles.
    plt.scatter(x, y, color="tab:blue", label="Actual data", s=80)

    # Draw the fitted least-squares line in red.
    plt.plot(x, predictions, color="tab:red", label="Least-squares line", linewidth=2)

    # Draw a thin line from each point to its prediction to show residuals.
    for actual_x, actual_y, predicted_y in zip(x, y, predictions):
        # Plot one vertical residual line at the current observation.
        plt.plot(
            [actual_x, actual_x],
            [actual_y, predicted_y],
            color="gray",
            linestyle="--",
            linewidth=1,
        )

    # Label the horizontal axis.
    plt.xlabel("Hours studied")

    # Label the vertical axis.
    plt.ylabel("Exam score")

    # Give the chart a clear title.
    plt.title("Simple least-squares regression")

    # Add a light grid to make values easier to read.
    plt.grid(True, alpha=0.3)

    # Add a legend that identifies the data and fitted line.
    plt.legend()

    # Automatically improve spacing around labels and title.
    plt.tight_layout()

    # Display the chart when the script runs interactively.
    plt.show()

    # Return the fitted values for optional reuse.
    return x, y, intercept, slope, predictions


def demonstrate_matrix_solution():
    """Fit the same line using the matrix form and NumPy's stable solver."""

    # Create the input feature as a floating-point NumPy array.
    x = np.array([1, 2, 3, 5, 6, 8], dtype=float)

    # Create the target values as a floating-point NumPy array.
    y = np.array([52, 58, 61, 73, 79, 86], dtype=float)

    # Build an intercept column containing one value per observation.
    intercept_column = np.ones_like(x)

    # Combine the intercept column and feature column into a design matrix.
    X = np.column_stack([intercept_column, x])

    # Solve the least-squares problem without directly inverting X.T @ X.
    beta, residuals, rank, singular_values = np.linalg.lstsq(X, y, rcond=None)

    # Extract the fitted intercept from the solution vector.
    intercept = beta[0]

    # Extract the fitted slope from the solution vector.
    slope = beta[1]

    # Print the parameters and useful numerical information.
    print("2. Matrix solution with np.linalg.lstsq")
    print(f"   Intercept: {intercept:.2f}")
    print(f"   Slope: {slope:.2f}")
    print(f"   Rank: {rank}")
    print(f"   Singular values: {singular_values}\n")


def demonstrate_scikit_learn():
    """Fit and evaluate the example with scikit-learn's LinearRegression class."""

    # Create the input feature as a floating-point NumPy array.
    x = np.array([1, 2, 3, 5, 6, 8], dtype=float)

    # Create the target values as a floating-point NumPy array.
    y = np.array([52, 58, 61, 73, 79, 86], dtype=float)

    # Convert x to a two-dimensional column because scikit-learn expects 2D features.
    X = x.reshape(-1, 1)

    # Create an ordinary least-squares regression object.
    model = LinearRegression()

    # Fit the model's intercept and slope to the observed data.
    model.fit(X, y)

    # Predict the targets for the same observations used for fitting.
    predictions = model.predict(X)

    # Calculate the root mean squared error from scikit-learn's MSE.
    rmse = np.sqrt(mean_squared_error(y, predictions))

    # Calculate R squared on the fitted data.
    r_squared = r2_score(y, predictions)

    # Print the learned parameters and evaluation metrics.
    print("3. Scikit-learn LinearRegression")
    print(f"   Intercept: {model.intercept_:.2f}")
    print(f"   Slope: {model.coef_[0]:.2f}")
    print(f"   RMSE: {rmse:.2f}")
    print(f"   R squared: {r_squared:.3f}")

    # Create a new input row containing seven hours.
    new_X = np.array([[7]])

    # Predict the exam score for seven hours using the fitted model.
    predicted_score = model.predict(new_X)[0]

    # Print the prediction for seven hours.
    print(f"   Predicted score after 7 hours: {predicted_score:.2f}\n")


def demonstrate_house_price_example():
    """Fit a simple house-price model and interpret its predictions."""

    # Create property areas in square meters as a column vector.
    area = np.array([50, 65, 80, 90, 110, 120, 140, 155], dtype=float).reshape(-1, 1)

    # Create corresponding prices in thousands of currency units.
    price = np.array([180, 215, 245, 270, 325, 350, 410, 455], dtype=float)

    # Create an ordinary least-squares regression model.
    house_model = LinearRegression()

    # Fit the house-price model to the observed areas and prices.
    house_model.fit(area, price)

    # Predict prices for the observations used to fit the model.
    predicted_prices = house_model.predict(area)

    # Calculate RMSE in the same units as the target price.
    rmse_price = np.sqrt(mean_squared_error(price, predicted_prices))

    # Calculate R squared for the fitted house-price model.
    r2_price = r2_score(price, predicted_prices)

    # Print the fitted model and evaluation metrics.
    print("4. Practical house-price example")
    print(f"   Intercept: {house_model.intercept_:.2f}")
    print(f"   Slope: {house_model.coef_[0]:.2f}")
    print(f"   RMSE: {rmse_price:.2f}")
    print(f"   R squared: {r2_price:.3f}")

    # Explain what one unit of slope means for this dataset.
    print(f"   Interpretation: each extra square meter adds about {house_model.coef_[0]:.2f} price units.")

    # Create a new input row for a 100-square-meter property.
    new_area = np.array([[100]])

    # Predict the price of the new property.
    predicted_new_price = house_model.predict(new_area)[0]

    # Print the model's prediction for the new property.
    print(f"   Predicted price for 100 m²: {predicted_new_price:.2f}\n")


def demonstrate_outlier_effect():
    """Show how one outlier can move an ordinary least-squares line."""

    # Create study-hour values without an outlier.
    x_normal = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float).reshape(-1, 1)

    # Create exam-score values that follow an approximately linear pattern.
    y_normal = np.array([50, 57, 62, 69, 74, 81, 86, 92], dtype=float)

    # Fit a line to the data without the outlier.
    normal_model = LinearRegression().fit(x_normal, y_normal)

    # Add an extreme, low-score observation to the inputs.
    x_with_outlier = np.vstack([x_normal, [[9]]])

    # Add an extreme, low-score observation to the targets.
    y_with_outlier = np.append(y_normal, 20)

    # Fit a second line to the same data plus the outlier.
    outlier_model = LinearRegression().fit(x_with_outlier, y_with_outlier)

    # Print the slopes to show how much the outlier changes the model.
    print("5. Why outliers matter")
    print(f"   Slope without outlier: {normal_model.coef_[0]:.2f}")
    print(f"   Slope with outlier: {outlier_model.coef_[0]:.2f}")
    print("   The outlier pulls the ordinary least-squares line downward.\n")


# Run the NumPy formula example when this file is executed directly.
demonstrate_least_squares_formulas()

# Run the matrix-form example when this file is executed directly.
demonstrate_matrix_solution()

# Run the scikit-learn example when this file is executed directly.
demonstrate_scikit_learn()

# Run the practical house-price example when this file is executed directly.
demonstrate_house_price_example()

# Run the outlier demonstration when this file is executed directly.
demonstrate_outlier_effect()
