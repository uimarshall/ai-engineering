# Evaluating Model Fit Using R-Squared

## Recap: Least Squares

The least squares method finds the regression line that fits the data better than any other line, based on the **sum of squared residuals (SSR)**. Another metric used to assess how well the line represents the data is **R-squared**.

## What is R?

**R** is the **correlation** (also called the _coefficient of correlation_). It expresses the strength and direction of the relationship between two variables.

| Correlation (r) | Meaning                                                                                                         |
| --------------- | --------------------------------------------------------------------------------------------------------------- |
| 0               | No relationship. A change in X doesn't lead to a related change in Y. Scores near 0 are very weak correlations. |
| +1              | Perfect positive correlation. A positive change in X gives the exact same positive change in Y.                 |
| +0.75           | Fairly strong positive correlation. As X increases, Y tends to increase, but not always at the same rate.       |
| -1              | Perfect negative correlation. As X increases, Y decreases by the same amount.                                   |
| -0.75           | Fairly strong negative correlation. As X increases, Y tends to decrease, but not always at the same rate.       |

Correlation ranges from -1 to +1.

## Why use R² instead of R?

1. **Squaring makes values positive.** R² ranges from 0 to 1, which makes comparison easier.
   - r = -0.75 → R² = 0.5625 ≈ 0.56
   - r = +0.75 → R² = 0.5625 ≈ 0.56
   - Both lines fit their data equally well, so they should get the same score.
2. **Multiple input variables.** Most real applications have many inputs (e.g. house age, bedrooms, size). Handling many correlations that may be positive or negative is tricky. Positive R² values are easier to combine into an overall goodness of fit. (Multiple linear regression is covered in the next tutorial.)

## What is R²?

R² shows the **percentage of variance in the output variable Y that is explained by the input variable(s) X**. It is also called the **coefficient of determination**.

## How R² is calculated

Modelling software always calculates it for you, but it helps to understand what it is made of.

Use two quantities:

- **SSR (mean line)**: sum of squared residuals for a flat line at the mean of Y. This is the baseline, i.e. how well we could predict Y using only the Y values themselves.
- **SSR (regression line)**: sum of squared residuals for the optimal regression line.

$$R^2 = \frac{SSR_{mean} - SSR_{regression}}{SSR_{mean}}$$

### Worked example

Five data points; the mean of Y is 2.2.

- SSR (mean line, y = 2.2) = 6.88
- SSR (optimal line) = 4.30

$$R^2 = \frac{6.88 - 4.30}{6.88} = \frac{2.58}{6.88} = 0.375 \;(37.5\%)$$

Input X explains 37.5% of the variance in Y. The model is 37.5% better at predicting Y than using the mean of Y alone.

Is 37.5% good? In the real world you would typically hope for something upwards of ~70%, but this model is still better than the baseline.

The mean line is the baseline because R² tells us the **additional benefit** gained by including the input variable(s) in the model.

### Another example (Lucy and Elimina's stand)

Temperature vs. number of lemonades sold gives R² = 0.876 (≈ 88%). Temperature explains about 88% of the variation in sales; other variables account for the remaining ~12%.

## Summary

- R² measures how well the input variables explain the variation in the output variable.
- It is the correlation squared, so it is always between 0 and 1.
- Calculating it needs the SSR of the mean line and the SSR of the optimal regression line.

## Train vs. test/validation R²

Calculate R² on the training data **and** on the test and validation sets.

- Ideally the scores are similar.
- A much higher R² on training than on test is a sure sign of **overfitting**: the model has learned the training trends so well that it struggles on new data.

Ways to address overfitting in linear regression:

- Get more (and more varied) data that better represents the real world.
- Reduce the number of variables, especially those with very weak relationships to the output or with high p-values in the model summary.
- Apply cross-validation, which helps reveal signs of overfitting.

Understanding what R² represents and how to interpret it is essential, even though software computes it in a fraction of a second.
