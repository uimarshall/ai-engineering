# Probability, Odds, Log-Odds, and Logistic Regression

## What this tutorial covers

This note builds a beginner-friendly bridge from probability to odds, from odds
to log-odds, and from log-odds to logistic regression. It then applies the ideas
to a small, reproducible binary-classification example.

The accompanying [Python script](Probability_Odds_Log_Odds_Logistic_Regression_Practical.py)
generates synthetic customer data, trains a logistic-regression model, and
prints example probabilities and evaluation metrics. The data are invented for
learning; they do not describe real customers.

## 1. Probability

Probability describes how likely an event is. For an event with probability
\(p\):

- \(p=0\) means the event never occurs.
- \(p=1\) means the event always occurs.
- A value such as \(p=0.8\) means an 80% chance of the event.

In binary classification, we often call the event of interest the **positive
class**, such as a customer purchasing or an email being spam. The other outcome
is the **negative class**. A classifier may return a probability for the
positive class, but a probability is not yet a final class decision; a
decision threshold is needed to turn it into a label.

### Example: an 80% chance

If a model estimates a purchase probability of \(0.8\), it estimates an 80%
chance of purchase and a 20% chance of no purchase. The probabilities of the
two possible outcomes add to 1.

## 2. Odds

Odds compare the probability that an event happens with the probability that it
does not happen:

\[
\text{odds} = \frac{p}{1-p}
\]

Odds are a ratio, not a probability. They range from zero upward. If the odds
are 4, that means **4 to 1 in favor** of the event; it does not mean a 400%
probability.

| Probability of event | Probability of no event | Odds \(p/(1-p)\) | Read as |
|---:|---:|---:|---|
| 0.50 | 0.50 | 1 | 1 to 1 |
| 0.80 | 0.20 | 4 | 4 to 1 in favor |
| 0.20 | 0.80 | 0.25 | 1 to 4 in favor |
| 0.10 | 0.90 | about 0.111 | 1 to 9 in favor |

### Convert probability to odds and back

Starting with \(p=0.8\):

\[
\text{odds} = \frac{0.8}{1-0.8} = \frac{0.8}{0.2} = 4
\]

To convert odds \(o\) back to probability:

\[
p = \frac{o}{1+o}
\]

So odds of 4 give \(p=4/(1+4)=0.8\). This reverse conversion is useful
because a model's linear score can be converted into odds and then into a valid
probability.

### A small Python calculation

```python
probability = 0.8
odds = probability / (1 - probability)
probability_again = odds / (1 + odds)
print(f"Probability: {probability:.2f}; odds: {odds:.2f}; back to probability: {probability_again:.2f}")
```

This prints a probability of 0.80, odds of 4.00, and a converted probability
of 0.80. The calculation highlights why odds and probability should not be
treated as interchangeable.

## 3. Log-odds

Log-odds (also called the **logit**) are the natural logarithm of the odds:

\[
\text{log-odds} = \ln\left(\frac{p}{1-p}\right)
\]

Taking a logarithm transforms odds, which range from 0 to infinity, into a
number on the whole real line:

- \(p=0.5\) gives odds 1 and log-odds \(\ln(1)=0\).
- \(p>0.5\) gives positive log-odds.
- \(p<0.5\) gives negative log-odds.
- Probabilities near 0 or 1 correspond to large negative or positive
  log-odds.

For \(p=0.8\), the odds are 4, so the log-odds are
\(\ln(4)\approx1.386\).

The inverse transformation is the **sigmoid** (or logistic) function:

\[
p = \frac{1}{1+e^{-z}}
\]

Here \(z\) is the log-odds. This function maps any real-valued number to a
probability strictly between 0 and 1.

## 4. Logistic regression

Despite its name, logistic regression is commonly used for **classification**.
It first forms a linear score from the input features:

\[
z = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots + \beta_k x_k
\]

It interprets that score as the log-odds of the positive class:

\[
\ln\left(\frac{p}{1-p}\right) = z
\]

Then it applies the sigmoid function to get a probability:

\[
p = \frac{1}{1+e^{-z}}
\]

The model learns the intercept \(\beta_0\) and feature weights
\(\beta_1,\dots,\beta_k\) from labeled examples. A positive weight raises the
log-odds (and therefore the probability) as that feature increases, holding
other features fixed. A negative weight lowers them.

### Practical coefficient interpretation

A coefficient is an additive change in log-odds, not a fixed change in
probability. If a feature's coefficient is \(0.7\), increasing that feature by
one unit multiplies the odds by \(e^{0.7}\approx2.01\), assuming other features
stay constant. It does **not** double the probability.

For example, if the original probability is 0.20, the odds are 0.25. Doubling
those odds gives 0.50, which converts to a probability of
\(0.50/(1+0.50)\approx0.333\), not 0.40.

The exponentiated coefficient \(e^{\beta_j}\) is called an **odds ratio** for a
one-unit increase in feature \(j\). In the script, features are standardized,
so one unit means a one-standard-deviation increase in that feature, based on
the training data.

## 5. Practical binary-classification example

The script models whether a fictional customer purchases, using three
features:

1. Number of website visits.
2. Discount offered, as a percentage.
3. Number of previous purchases.

It creates a reproducible synthetic dataset, splits it into training and test
sets, fits scaling and logistic regression using the training split only, and
evaluates the held-out test split. Using a pipeline helps avoid accidentally
fitting preprocessing on test data.

### Run the script

The script requires Python, NumPy, and scikit-learn. From the repository root,
run it with the Python environment that has those packages installed:

```powershell
python DSI\Day-127\Probability_Odds_Log_Odds_Logistic_Regression_Practical.py
```

It prints model metrics and the estimated purchase probability, odds, and
predicted label for one example customer. Because the data are synthetic, use
the output to learn how the workflow behaves, not as evidence about real
purchases.

### What the evaluation tells you

- **Confusion matrix:** counts correct and incorrect predictions for each
  class. False negatives are actual purchases the model missed; false positives
  are predicted purchases that did not occur.
- **Precision:** among customers predicted to purchase, the fraction who did.
- **Recall:** among actual purchasers, the fraction the model found.
- **F1-score:** a combined measure of precision and recall.
- **ROC-AUC:** measures how well the scores rank positive cases above negative
  cases across thresholds; 0.5 is chance ranking and 1.0 is perfect ranking.
- **Log loss:** evaluates probability quality and penalizes confident,
  incorrect predictions.

Accuracy is the share of labels predicted correctly, but can hide poor
performance on a rare class. Select metrics based on the consequences of
mistakes in the application.

## 6. Probabilities are not decisions: choosing a threshold

Many classifiers use a threshold of 0.5 by default: predict positive when the
estimated probability is at least 0.5. This is a convention, not a law. If
missing a positive case is costly, a lower threshold may improve recall while
also increasing false positives. If false alarms are costly, a higher
threshold may improve precision while missing more positives.

Choose a threshold with validation data and the application's error costs.
Keep the test set for final evaluation rather than repeatedly adjusting the
threshold based on test results.

## 7. Practical cautions

- **Data leakage:** split before fitting imputers, scalers, encoders, feature
  selection, or other learned preprocessing. Fit them on training data only;
  apply the fitted transformations to validation and test data.
- **Missing values:** inspect how many values are missing and why. Decide
  whether to impute or exclude them based on the data context. If imputing,
  learn imputation values from the training set.
- **Class imbalance:** use stratified splits where appropriate and inspect
  per-class precision, recall, F1-score, and the confusion matrix. Consider
  class weights or threshold adjustment when justified.
- **Feature relationships:** logistic regression models a linear relationship
  between each input and log-odds. Nonlinear patterns may require feature
  engineering, transformations, interactions, or a different model.
- **Correlated features:** when predictors are strongly correlated, individual
  coefficients can be unstable and should not be interpreted as causal effects.
- **Regularization:** scikit-learn's logistic regression uses regularization by
  default. The `C` setting controls its strength: smaller values mean stronger
  regularization.
- **Interpretation is not causation:** a model's association between a feature
  and outcome does not prove that changing the feature causes the outcome.
- **Privacy and fairness:** assess whether features are appropriate for the
  task and investigate performance differences across relevant groups.

## Summary

Probability describes the chance of an event. Odds compare that chance with
the chance of the event not happening, and log-odds are the natural logarithm
of the odds. Logistic regression adds feature-weighted contributions on the
log-odds scale, then uses the sigmoid function to return a probability between
0 and 1. A threshold turns that probability into a class label.

To use logistic regression responsibly, split data before fitting preprocessing,
evaluate probabilities and class decisions with suitable metrics, choose a
threshold based on the cost of errors, and interpret coefficients as changes
in log-odds (or multiplicative changes in odds), not direct changes in
probability.
