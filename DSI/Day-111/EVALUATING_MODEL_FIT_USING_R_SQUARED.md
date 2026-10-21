# Evaluating Model Fit Using R-Squared

In the previous tutorial we learned about the **least squares method** for finding the optimal regression line: the line that fits the data better than any other, based on the **sum of squared residuals (SSR)**. There is another metric for assessing how well a line represents the data: **R-squared**.

## What is R?

R is the same as **correlation** (also called the _coefficient of correlation_). It expresses the strength and direction of the relationship between two variables.

| Correlation (r) | Meaning                                                                                            |
| --------------- | -------------------------------------------------------------------------------------------------- |
| 0 (or near 0)   | No / extremely weak relationship; a change in x does not lead to a related change in y             |
| +1              | Perfect positive correlation                                                                       |
| +0.75           | Strong, not perfect, positive: as x increases y tends to increase, but not always at the same rate |
| -1              | Perfect negative correlation                                                                       |
| -0.75           | Strong, not perfect, negative: as x increases y tends to decrease                                  |

Correlation ranges from -1 to +1.

## Why use R-squared instead of R?

1. **Squaring makes values positive**, so comparisons are easier. R-squared ranges from 0 to 1.
   - r = -0.75 → R² = 0.56
   - r = +0.75 → R² = 0.56
   - Both lines fit their data equally well, so they should get the same goodness-of-fit score.
2. **Multiple input variables.** Most real models have many inputs (e.g. house age, number of bedrooms, size). Treating each as a positive or negative correlation is tricky; positive squared values are much easier to combine into an overall goodness of fit. (Multiple linear regression is covered in an upcoming tutorial.)

## What R-squared means

R-squared shows the **percentage of variance in the output variable (y) that is explained by the input variable(s) (x)**. It is also called the **coefficient of determination**.

## How it is calculated

Modelling software always calculates it for you, but it is worth understanding.

R² compares the fit of our regression line against a baseline: a flat line at the **mean of y**.

```
R² = (SSR_mean - SSR_fit) / SSR_mean
```

- `SSR_mean`: sum of squared residuals for the mean line
- `SSR_fit`: sum of squared residuals for the optimal regression line

### Worked example

From the least squares tutorial, the mean line (y = 2.2) had SSR = 6.88, and the optimal regression line had SSR = 4.30.

```
R² = (6.88 - 4.30) / 6.88 = 2.58 / 6.88 = 0.375  →  37.5%
```

So x explains 37.5% of the variance in y. For a real-world model you would probably hope for 70%+, but this model is still 37.5% better at predicting y than using the mean of y alone.

The mean line is the baseline because it shows how well we can predict y using only the y values and nothing else. R² therefore tells us the **additional benefit of including the input variable(s)** in the model.

### Lucy's lemonade stand

The regression line fits well: R² = 0.876 (≈ 88%). Daily temperature explains 88% of the variation in lemonade sales; other variables must account for the remaining ~12%.

## Summary

- R² tells us how well the input variables explain variation in the output variable.
- It is the correlation squared: always between 0 and 1.
- It needs two things: SSR for the mean line and SSR for the optimal regression line.

## Practical use: training vs test sets

Calculate R² on the **training**, **test** and **validation** sets. Ideally the scores are similar. A far higher R² on training than on test is a sure sign of **overfitting**: the model has learned the training data's trends so well that it struggles on new data.

Ways to address overfitting in linear regression:

- Get more data for a more varied representation of the real world.
- Reduce the number of variables, especially those with very weak relationships to the output or high p-values in the output summary.
- Apply **cross-validation** techniques, which help reveal signs of overfitting.

Knowing what R² represents and how to interpret it is essential when assessing model performance.
