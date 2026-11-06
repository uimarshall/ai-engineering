# Random Forests for Classification: A Practical Beginner's Guide

This tutorial explains how to train, evaluate, and improve a random forest
classifier with scikit-learn. The runnable companion script,
[Random_Forests_for_Classification_Practical.py](Random_Forests_for_Classification_Practical.py),
uses a small dataset bundled with scikit-learn, so it does not download data.

The example classifies breast-tumor measurements as malignant or benign. This
is a public teaching dataset, **not a diagnostic tool**. The workflow and
metrics are for learning and must not be used to make medical decisions.

## 1. What classification means

Classification predicts a category (a **class**) from input information
(**features**). Examples include labeling an email as spam or not spam, or
flagging a transaction as potentially fraudulent.

For this example:

- Each row describes one example in the dataset.
- The 30 numeric measurements are the input features, conventionally written
  \(X\).
- The target \(y\) says whether the example is malignant or benign.
- We define **malignant** as the positive class (`1`) and benign as `0` to make
  the later precision and recall discussion explicit.

The dataset is intentionally small and already numeric. A production workflow
must also understand the meaning, quality, permissions, and limitations of its
own data.

## 2. How a random forest makes a prediction

A decision tree repeatedly splits the data using feature thresholds. For
example, a tree might ask whether a measurement is below a certain value, then
ask a different question for each branch. A leaf at the end of a path predicts
a class.

A random forest combines many decision trees. During training, each tree:

1. Usually receives a bootstrap sample of the training rows: rows are sampled
   with replacement, so a row may appear more than once or be omitted.
2. Considers a random subset of features when looking for a split.
3. Grows its own decision-tree structure from those sampled rows and features.

For classification, the forest aggregates the trees' votes. Its predicted
class is generally the class with the most votes. It can also return class
probabilities based on the trees' estimates.

The randomness makes trees less alike. Combining their predictions typically
reduces the instability of a single tree. The number of trees is controlled by
`n_estimators`; `max_features` controls the candidate features per split.

## 3. Why random forests are useful

- They can model nonlinear patterns and feature interactions without requiring
  the user to specify them in advance.
- They usually need little preprocessing for numeric data. In particular,
  numeric features generally do **not** need standardization.
- They work for binary and multiclass classification.
- They provide class probabilities and several ways to inspect feature
  importance.

There are trade-offs: forests can use more memory and take longer to train or
predict than a single tree; their predictions are less straightforward to
explain; and they do not automatically solve poor data quality, leakage, class
imbalance, or unfairness.

## 4. Set up a sound evaluation

The script follows this pattern:

1. Load and inspect the dataset and target classes.
2. Check missing-value counts and class balance.
3. Split rows into training and held-out test sets using stratification.
4. Fit a simple majority-class baseline on the training set.
5. Tune a random forest using cross-validation **only within the training set**.
6. Evaluate the selected model once on the held-out test set.
7. Inspect permutation importance on that held-out set.

The test set should represent unseen examples. Do not repeatedly tune the model
or choose thresholds based on test results; that leaks information from the
test set into model selection. For a real project, keep a separate validation
set or use cross-validation for model and threshold choices, then evaluate once
on the test set. When records are grouped (for example, multiple visits per
person) or time-ordered, split by group or time instead of randomly.

### Missing values and preprocessing

The bundled example dataset has no missing feature values, but the code still
checks for them and places a median imputer inside the model pipeline. This
shows a safe pattern for data that may have missing numeric entries. The
imputer learns medians only from each training fold when cross-validation is
running, and from the complete training set when the final model is fit. Never
fit preprocessing on test data.

Trees do not need feature scaling, so the example does not standardize values.
For categorical, text, date, or other real-world feature types, choose
appropriate transformations inside the pipeline and fit them on training data
only.

## 5. Metrics: choose according to the mistake that matters

The script reports several test metrics:

- **Confusion matrix:** counts actual versus predicted classes. With malignant
  as the positive class, a false negative is a malignant case predicted
  benign; a false positive is a benign case predicted malignant.
- **Precision:** among cases predicted malignant, the proportion that are
  malignant.
- **Recall (sensitivity):** among actual malignant cases, the proportion found
  by the model.
- **F1-score:** the harmonic mean of precision and recall.
- **Balanced accuracy:** the average of recall for each class, useful when
  class counts differ.
- **ROC-AUC:** measures how well the model ranks positive cases above negative
  cases across possible thresholds. It does not by itself select a threshold
  or ensure calibrated probabilities.
- **Log loss:** evaluates the predicted probabilities, penalizing confident
  incorrect predictions.

Accuracy alone can be misleading when one class is much more common than the
other. For high-cost false negatives, recall may be especially important; for
high-cost false alarms, precision may matter more. In a real application,
choose metrics and thresholds with domain experts and the actual costs of
errors.

## 6. Important settings to understand

The script searches a small grid of settings using stratified five-fold
cross-validation on training data, selecting by ROC-AUC:

- `n_estimators`: number of trees. More trees can stabilize results but cost
  more computation; adding trees does not guarantee better generalization.
- `max_features`: number of candidate features considered at each split.
  `sqrt` is a common classification default; `log2` provides a smaller
  candidate set.
- `max_depth`: maximum tree depth. A limit can reduce complexity; `None`
  allows trees to continue splitting subject to other settings.
- `min_samples_leaf`: minimum number of training examples in a leaf. Larger
  values can smooth predictions and reduce overfitting.
- `class_weight`: the script uses `balanced_subsample`, which adjusts class
  weights separately for each tree's bootstrap sample. This may help with
  imbalance, but is not guaranteed to improve the metric that matters.
- `random_state`: fixes randomness to make the experiment more repeatable.
- `n_jobs`: lets scikit-learn use available CPU cores for parallel work.

The best cross-validation score is a model-selection estimate, not the final
test result. A very large hyperparameter search can overfit cross-validation
scores too, so tune deliberately.

## 7. Understanding feature importance

The script computes **permutation importance** after final test evaluation. It
shuffles one feature column at a time and measures how much the chosen ROC-AUC
score drops. A larger drop suggests the fitted model relied more on that
feature for this dataset and score.

Importance is not causation, and it does not show whether a feature increases
or decreases the target. Correlated features can share or mask importance, and
the result can vary across samples. Use domain knowledge and further analysis
before drawing conclusions.

Random forests also expose impurity-based `feature_importances_`; these can
favor features with many possible split points. Permutation importance is a
useful alternative, but it too has limitations and should be interpreted with
care.

## 8. Out-of-bag (OOB) estimates

Since bootstrap sampling leaves some training rows out of each individual
tree's sample, those omitted rows are called that tree's **out-of-bag** rows.
Setting `bootstrap=True` and `oob_score=True` can provide an OOB estimate in
scikit-learn. It is a convenient training-data diagnostic, but it is not a
replacement for a final evaluation on a held-out test set, especially when
choosing models or making important decisions.

## 9. Run the example

Install NumPy and scikit-learn in your project's Python environment if they
are not already available. From the repository root, run:

```powershell
python DSI\Day-127\Random_Forests_for_Classification_Practical.py
```

The script prints the dataset shape and class balance, majority-class baseline,
cross-validation score and selected settings, test metrics, a confusion matrix,
and the top permutation importances. Exact results can vary slightly across
library versions or platforms.

## Takeaways

A random forest is a collection of randomized decision trees whose predictions
are combined by voting. It is a strong practical baseline for many tabular
classification problems, with limited scaling needs and the ability to model
nonlinear patterns. Good evaluation still depends on sound splitting,
training-only preprocessing and tuning, metrics that reflect the cost of
mistakes, and careful interpretation of feature importance. The companion
script demonstrates these practices without modifying any existing notes or
examples.
