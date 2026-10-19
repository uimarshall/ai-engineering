# Finding the “Best” Line Using Least Squares — A Practical Tutorial

## 1. What problem are we solving?

Regression predicts a **continuous number**, such as:

- Predicting a student’s exam score from hours studied
- Predicting electricity use from temperature
- Predicting house price from floor area
- Predicting delivery time from distance

> When we have one input feature, we can draw the prediction as a line:

```text
predicted value = intercept + slope × input value
```

So `y` is seen as the `predicted value` or the `dependent variable` or the `output`.

Mathematically:

\[
\hat{y} = b + wx
\]

where:

- \(x\) is the input, such as hours studied
- \(\hat{y}\) (“y-hat”) is the prediction
- \(b\) is the **intercept**—the value predicted when \(x = 0\)
- \(w\) is the **slope**—how much the prediction changes when \(x\) increases by one unit

The `goal` is to choose \(b\) and \(w\) so the line describes the data as well as possible.

---

## 2. What does “best” mean?

A regression line will not pass through every data point. Each data point creates an **error**,
also called a **residual**:

\[
\text{residual} = \text{actual value} - \text{predicted value}
\]

For example, if a student studied for 4 hours and scored 75, but our model predicts 70, the
residual is:

```text
75 - 70 = 5
```

A positive residual means the model predicted too low. A negative residual means it predicted too high.

One common definition of “best” is the line that minimizes the **sum of squared errors** (SSE):

\[
SSE = \sum\_{i=1}^{n} (y_i - \hat{y}\_i)^2
\]

This is called **least squares regression**.

### Why square the errors?

1. It prevents positive and negative errors from canceling each other.
2. It penalizes large errors more strongly.
3. The resulting formulas are convenient and mathematically well-behaved.

---

## 3. The intuition with a simple example

Suppose these are our observations:

| Hours studied (\(x\)) | Exam score (\(y\)) |
| --------------------: | -----------------: |
|                     1 |                 52 |
|                     2 |                 58 |
|                     3 |                 61 |
|                     5 |                 73 |
|                     6 |                 79 |
|                     8 |                 86 |

A plausible line might be:

```text
predicted score = 45 + 5 × hours
```

For 6 hours of study:

```text
predicted score = 45 + 5 × 6 = 75
actual score = 79
error = 79 - 75 = 4
squared error = 4² = 16
```

Least squares checks many possible intercepts and slopes and keeps the combination with the
smallest total squared error.

---

## 4. How do we calculate the line?

For simple regression, least squares gives:

\[
w = \frac{\sum*{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}
{\sum*{i=1}^{n} (x_i - \bar{x})^2}
\]

and:

\[
b = \bar{y} - w\bar{x}
\]

where:

- \(\bar{x}\) is the mean of the inputs
- \(\bar{y}\) is the mean of the targets

### Example calculation

Using the study-hours data:

\[
\bar{x} = 4.167, \qquad \bar{y} \approx 68.167
\]

The slope is approximately:

\[
w \approx 4.99
\]

The intercept is approximately:

\[
b = 68.167 - 4.99(4.167) \approx 47.37
\]

So the fitted line is approximately:

\[
\hat{y} = 47.37 + 4.99x
\]

Interpretation:

- **Intercept ≈ 47.37:** the model predicts a score of about 47 for zero study hours.
- **Slope ≈ 4.99:** each extra study hour is associated with about 5 extra predicted points.

---

## 5. A complete NumPy example

NumPy makes the calculation concise and reliable.

### Load and inspect the data

```python
import numpy as np

x = np.array([1, 2, 3, 5, 6, 8], dtype=float)
y = np.array([52, 58, 61, 73, 79, 86], dtype=float)

print("Inputs x:", x)
print("Targets y:", y)
print("Mean of x:", x.mean())
print("Mean of y:", y.mean())
```

### Fit the line manually with least-squares formulas

```python
x_mean = x.mean()
y_mean = y.mean()

numerator = ((x - x_mean) * (y - y_mean)).sum()
denominator = ((x - x_mean) ** 2).sum()

slope = numerator / denominator
intercept = y_mean - slope * x_mean

print(f"Fitted line: y = {intercept:.2f} + {slope:.2f} * x")
```

### Predict a new value

```python
new_x = 7
new_prediction = intercept + slope * new_x

print(f"Predicted score after {new_x} hours: {new_prediction:.2f}")
```

Expected output:

```text
Fitted line: y = 47.37 + 4.99 * x
Predicted score after 7 hours: 82.31
```

---

## 6. The matrix version used by machine learning

In machine learning, it is common to place several observations in a matrix. Each row is one
observation, and each column is one feature.

For simple regression:

\[
X =
\begin{bmatrix}
1 & 1 \\
1 & 2 \\
1 & 3 \\
1 & 5 \\
1 & 6 \\
1 & 8
\end{bmatrix}
\]

The first column contains ones because it multiplies the intercept. The second column contains the study hours.

The normal equation is:

\[
\beta = (X^TX)^{-1}X^Ty
\]

where:

- \(X\) is the feature matrix
- \(y\) contains the target values
- \(\beta\) contains the fitted parameters
- \(X^T\) is the transpose of \(X\)

In practice, avoid calculating the matrix inverse directly. A numerically safer approach is to use
a solver such as `np.linalg.lstsq`.

```python
X = np.column_stack([np.ones_like(x), x])
beta, residuals, rank, singular_values = np.linalg.lstsq(X, y, rcond=None)

intercept_matrix = beta[0]
slope_matrix = beta[1]

print("Intercept:", intercept_matrix)
print("Slope:", slope_matrix)
print("Rank:", rank)
print("Singular values:", singular_values)
```

The rank tells us how many independent columns the design matrix has. If the rank is smaller than
the number of columns, the columns are not fully independent, so there may not be a unique
least-squares solution.

---

## 7. Check how well the line fits

The coefficient of determination, \(R^2\), compares the model with a baseline that always predicts the mean of \(y\).

\[
R^2 = 1 - \frac{\sum*{i=1}^{n} (y_i - \hat{y}\_i)^2}
{\sum*{i=1}^{n} (y_i - \bar{y})^2}
\]

- \(R^2 = 1\): predictions are perfect on the data used to calculate it.
- \(R^2 = 0\): model performs like predicting the mean.
- \(R^2 < 0\): model performs worse than predicting the mean on the evaluated data.

```python
predictions = intercept + slope * x
squared_errors = (y - predictions) ** 2
sse = squared_errors.sum()

total_variation = ((y - y_mean) ** 2).sum()
r_squared = 1 - sse / total_variation

print("Sum of squared errors:", sse)
print("R squared:", r_squared)
```

Another useful measure is root mean squared error (RMSE):

\[
RMSE = \sqrt{\frac{1}{n} \sum\_{i=1}^{n} (y_i - \hat{y}\_i)^2}
\]

RMSE is in the same units as the target. If the target is exam score, RMSE is also measured in points.

```python
rmse = np.sqrt(squared_errors.mean())
print("RMSE:", rmse)
```

For this small example, the RMSE will be less than one point, but real datasets are rarely this tidy.

---

## 8. Plot the fitted line

Visualization is especially helpful while learning.

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.scatter(x, y, color="tab:blue", label="Actual data", s=80)
plt.plot(x, predictions, color="tab:red", label="Least-squares line", linewidth=2)
plt.xlabel("Hours studied")
plt.ylabel("Exam score")
plt.title("Simple least-squares regression")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
```

Each vertical distance from a blue point to the red line is a residual. Least squares chooses the
red line so that the sum of squared vertical distances is as small as possible.

---

## 9. Compare with scikit-learn

For real machine-learning projects, you will normally use a library such as scikit-learn. The
fitted result should match the NumPy result.

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
X_one_feature = x.reshape(-1, 1)
model.fit(X_one_feature, y)

print("scikit-learn intercept:", model.intercept_)
print("scikit-learn slope:", model.coef_[0])
print("Prediction for 7 hours:", model.predict([[7]])[0])
print("R squared:", model.score(X_one_feature, y))
```

---

## 10. A practical house-price example

Now consider a slightly more realistic example. We will train on some observed sales and then
predict a new sale.

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

area = np.array([50, 65, 80, 90, 110, 120, 140, 155], dtype=float).reshape(-1, 1)
price = np.array([180, 215, 245, 270, 325, 350, 410, 455], dtype=float)

house_model = LinearRegression()
house_model.fit(area, price)

predicted_prices = house_model.predict(area)
rmse_price = np.sqrt(mean_squared_error(price, predicted_prices))
r2_price = r2_score(price, predicted_prices)

print("House price model")
print(f"Intercept: {house_model.intercept_:.2f}")
print(f"Slope: {house_model.coef_[0]:.2f}")
print(f"RMSE: {rmse_price:.2f}")
print(f"R squared: {r2_price:.3f}")

new_area = np.array([[100]])
predicted_new_price = house_model.predict(new_area)
print(f"Predicted price for 100 m²: {predicted_new_price[0]:.2f}")
```

Possible interpretation:

- The slope says how much predicted price changes for each additional square meter.
- The intercept represents the price predicted at an area of zero. In this example, that is mainly
  a mathematical anchor and should not be interpreted as the true price of a zero-square-meter
  property.

---

## 11. When should you be careful?

### Outliers

Least squares squares every error, so a very large error can strongly pull the line toward an
outlier.

Example: most houses might follow a clear pattern, but one incorrectly recorded mansion could
distort a simple model.

Possible actions include:

- Inspect and correct data-entry errors
- Use robust regression methods
- Investigate whether the outlier is valid and represents an important subgroup

### Extrapolation

Extrapolation means predicting far outside the range of the training data.

If the model was trained on students who studied 1–8 hours, predicting the score after 30 hours may
be unreliable. The relationship might flatten, change, or stop being valid.

### Correlation is not causation

A slope does not automatically prove that changing \(x\) causes \(y\).

For example, ice-cream sales and sunburn incidents may rise together because both are affected by
hot weather. Neither variable necessarily causes the other.

### Linear models do not capture every relationship

A straight line is useful when the relationship is approximately linear. If the data follows a
curve, a polynomial feature, decision tree, neural network, or another model may fit better.

### Training and testing

Fitting a line and evaluating it on the same observations can overstate performance. For a stronger
evaluation, split the data into:

- a training set, used to fit the parameters
- a test set, used to estimate performance on unseen data

For tiny teaching examples, splitting may not be practical. For real datasets, it usually is.

---

## 12. Common mistakes to avoid

### Mistake 1: Choosing the line by eye when exact code is available

A visual check is useful, but least squares provides a reproducible answer.

### Mistake 2: Ignoring units

If \(x\) is measured in thousands of dollars and \(y\) in dollars, the slope interpretation must
respect those units.

### Mistake 3: Assuming a large slope always matters

A slope’s practical importance depends on the units and scale of the data.

### Mistake 4: Focusing only on \(R^2\)

A high \(R^2\) does not guarantee that:

- the model will generalize
- the relationship is causal
- the errors have constant spread
- the line is appropriate across the whole input range

### Mistake 5: Interpreting the intercept too literally

The intercept is the prediction at \(x=0\), but \(x=0\) may be impossible, meaningless, or outside
the observed data range.

---

## 13. Key takeaway

Least-squares regression finds the intercept and slope that minimize:

\[
\sum\_{i=1}^{n} (\text{actual}\_i - \text{predicted}\_i)^2
\]

For one input feature, the fitted model is:

\[
\hat{y} = b + wx
\]

It is one of the simplest and most important methods in machine learning. It provides:

- an interpretable fitted line
- predictions for new inputs
- a baseline against which more complex models can be compared

The complete runnable Python file included with this tutorial demonstrates:

1. The least-squares formulas
2. The matrix form with `np.linalg.lstsq`
3. The scikit-learn implementation
4. Error metrics
5. Plotting
6. A practical house-price example
