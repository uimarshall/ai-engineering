# Model Validation & Over-fitting (Practical)

### Cleaning and Preparing Data for Machine Learning

> **In one sentence:** Model validation is how we estimate whether a model has
> learned patterns that will work on new data; over-fitting happens when it
> learns the training examples too closely, including their noise.

This beginner-friendly guide uses a small customer-renewal example. The labels
and measurements are generated for demonstration, so no external data files or
downloads are needed. The companion script,
[`model_validation_overfitting_practical.py`](./model_validation_overfitting_practical.py),
contains the full runnable example, with comments explaining the code.

## 1. The basic idea: learn versus remember

Imagine showing a student practice questions and then asking new questions on
the same topic.

- A model that has not learned enough will do poorly on both the examples it
  studied and new examples. This is **under-fitting**.
- A model that has memorized the practice examples may score extremely well on
  those exact examples, but poorly on new ones. This is **over-fitting**.
- A useful model learns patterns that continue to work on examples it has not
  seen. This is **generalization**.

| Training score | Validation score | Likely explanation |
| --- | --- | --- |
| Low | Low | Under-fitting, weak features, or a difficult/noisy task |
| Very high | Much lower | Over-fitting, leakage, or a validation split unlike the real task |
| Good | Similar and good | The model may generalize; confirm once on the test set |

The difference between training and validation performance is often called the
**generalization gap**. A large gap is a warning, not a diagnosis by itself:
also check for data leakage, small datasets, class imbalance, and an
unrepresentative split.

## 2. Know which data has which job

For a typical supervised-learning project, split the rows into three parts:

| Part | What it is for | May it influence model or preprocessing choices? |
| --- | --- | --- |
| **Training set** | Learn model parameters and preprocessing values | Yes |
| **Validation set** | Compare models and choose settings | Yes, for choices |
| **Test set** | One final estimate after choices are finished | No; keep it aside until the end |

A common starting point is 60% training, 20% validation, and 20% test. The best
split depends on the amount and structure of data. For a small dataset,
cross-validation can use the training portion more efficiently.

The target is the answer to predict (here, whether a customer renews). Features
are the information available to make that prediction. Split the rows before
fitting an imputer, encoder, scaler, feature selector, or model.

```python
# First set aside the final test rows; keep their labels out of training and tuning.
X_train_and_validation, X_test, y_train_and_validation, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=42
)

# Split the remaining rows again to make a validation set.
X_train, X_validation, y_train, y_validation = train_test_split(
    X_train_and_validation, y_train_and_validation,
    test_size=0.25, stratify=y_train_and_validation, random_state=42
)
```

The two fractions above create 60% training, 20% validation, and 20% test
overall. `stratify=y` keeps the class proportions similar in each partition,
which is helpful for classification when each class has enough examples.

### When a random split is the wrong split

- **Time-based prediction:** Train on earlier dates, validate on later dates,
  and test on the latest dates. Randomly mixing future and past can make
  forecasting unrealistically easy.
- **Repeated people, devices, or locations:** Keep each group in only one split
  when the goal is to predict for entirely new groups. Otherwise, a model may
  recognize the same person in both training and test data.
- **Rare classes:** Use stratified splits when feasible, and report metrics
  that reveal mistakes on the less common class.

## 3. Data preparation can accidentally leak the answers

**Data leakage** means information from outside the allowed training data
influences model fitting or evaluation. It makes scores look better than the
model's real-world performance.

Common examples:

1. **Fit preprocessing on all rows:** A scaler learns the test-set average, or
   an imputer learns the test-set median. Even without using test labels, this
   lets test data influence training.
2. **Use a future or post-outcome column:** A cancellation date may reveal the
   renewal outcome when the intended prediction happens before cancellation.
3. **Split after duplicating or resampling:** Copies of one record can land in
   both training and test sets.
4. **Select features using all labels:** Looking at the full dataset's
   relationship between each feature and the target before splitting lets test
   answers influence feature selection.

Avoid manually fitting preprocessing on the full dataset:

```python
# LEAKAGE: this learns the scaling statistics from training AND test rows.
X_scaled = StandardScaler().fit_transform(X)
```

Instead, put the preparation steps and model in a scikit-learn `Pipeline`.
Calling `.fit()` on the training data learns the imputation values, category
mapping, scaling statistics, and model parameters from training only. During
validation or testing, the same learned transformations are applied without
being refitted.

## 4. Clean carefully, then put learned preparation inside a pipeline

Cleaning is not a contest to delete every odd value. First ask what each row
means, what a feature measures, and whether its value can be known at
prediction time.

For the example script:

- It reports missing-value counts before handling gaps.
- It includes missing numeric data, missing categories, and one deliberately
  extreme measurement for discussion.
- A median imputer fills numeric gaps; a most-frequent imputer fills category
  gaps. These values are learned from training rows only.
- Numeric columns are scaled for logistic regression. Scaling is especially
  useful for many linear and distance-based models; tree models generally do
  not need it.
- A one-hot encoder turns the category into indicator columns. An unfamiliar
  category at prediction time is safely ignored.
- The example extreme value is **not automatically deleted or clipped**.
  Check units, source systems, and business meaning first. It could be a
  recording error or a real event.

The central pattern is:

```python
# Define the transformations for numeric and category columns.
preprocessor = ColumnTransformer(
    transformers=[
        ("numbers", numeric_pipeline, numeric_features),
        ("categories", categorical_pipeline, categorical_features),
    ]
)

# Keep data preparation and prediction together to prevent fit/transform mix-ups.
model = Pipeline(
    steps=[
        ("prepare", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000)),
    ]
)

# Learn the imputation, encoding, scaling, and model parameters from training data.
model.fit(X_train, y_train)

# Apply the already-learned steps to held-out rows; do not fit them again.
validation_predictions = model.predict(X_validation)
```

In a real dataset, also check for invalid units, inconsistent category
spelling, duplicate records, missing targets, identifiers that should not be
features, and columns created after the event you are predicting. Decide
whether to correct, impute, exclude, or retain a value based on what it means.

## 5. Validation, cross-validation, and model choice

The validation set helps answer questions such as:

- Is a simple model already good enough?
- Does a deep decision tree perform much better on training than validation?
- Does limiting tree depth, increasing the minimum leaf size, or regularizing
  a linear model improve generalization?

**Cross-validation (CV)** repeatedly divides the training portion into folds.
For example, in 5-fold CV, each fold takes a turn as the temporary validation
fold while the other four folds are used for fitting. The average score is
usually more stable than a single split.

Use CV **only on the training portion** when comparing model settings. After
choosing a setting, fit the selected model on all training rows and inspect the
separate validation set. Keep the test set untouched. If you repeatedly try
models and settings based on validation scores, you can over-fit to the
validation set too; CV or a fresh final test set helps address that.

The runnable example does this:

1. Fits logistic regression as a simple baseline.
2. Fits an unrestricted decision tree to expose the over-fitting pattern.
3. Uses 5-fold CV on training rows to choose a more constrained tree.
4. Compares all three on the validation rows using **balanced accuracy**.
5. Selects the best validation candidate and reports test metrics once.

### Choose a metric that matches the question

Accuracy is the fraction of predictions that are right. It can be misleading
when one outcome is much more common than another. If only 5% of customers
renew, predicting “did not renew” for every customer is 95% accurate but finds
no renewals.

- **Precision:** Among the predicted positives, how many are truly positive?
- **Recall:** Among the true positives, how many did the model find?
- **F1:** A combined measure of precision and recall.
- **Balanced accuracy:** Average recall across classes; useful when class sizes
  differ.
- **ROC-AUC / PR-AUC:** Measures ranking quality across thresholds; PR-AUC is
  often informative when the positive class is rare.

For regression, consider measures such as mean absolute error (MAE) or root
mean squared error (RMSE), in units and costs meaningful to the problem. Choose
metrics before model comparison, based on the impact of false positives,
false negatives, or prediction errors.

## 6. Read the example output

Run the companion script from the `DSI` project directory:

```powershell
uv run python Day-103\model_validation_overfitting_practical.py
```

The script prints:

- dataset size, missing-value counts, and target class counts;
- the cross-validated score and selected decision-tree settings;
- training and validation balanced accuracy for each candidate, plus the
  training-minus-validation gap;
- final accuracy, balanced accuracy, and a per-class precision/recall/F1
  report on the untouched test set.

The unrestricted tree will commonly have a perfect or near-perfect training
score. If its validation score is lower, that is a concrete over-fitting
signal. A depth-limited tree may narrow the gap, but it is not guaranteed to
win on every generated dataset. A small validation difference may also be
random variation; do not treat one decimal place as certainty.

For example, a run in the current DSI environment produced:

| Candidate | Training balanced accuracy | Validation balanced accuracy | Gap |
| --- | ---: | ---: | ---: |
| Logistic regression baseline | 0.723 | 0.677 | 0.046 |
| Unrestricted decision tree | 1.000 | 0.749 | 0.251 |
| Cross-validated decision tree | 0.790 | 0.733 | 0.057 |

The unrestricted tree memorizes the training rows much more closely, as shown
by its larger gap. Yet it also wins among these three candidates on this
particular validation split, so the script selects it. The separate test
balanced accuracy was 0.833 in that run. This is a useful reminder that
validation scores are estimates based on finite samples, not guarantees: a
validation winner can still over-fit the model-selection process, and its test
score can be higher or lower. For a high-stakes decision, prefer repeated or
nested cross-validation, adequate sample sizes, and an evaluation split that
matches real deployment.

The code is deterministic (`random_state=42`), so its synthetic data splits
and results are repeatable with the same compatible library versions. Run it
from the `DSI` project, whose existing `uv` environment includes the required
dependencies.

## 7. A practical checklist

Before trusting a model's score, ask:

- What does each row represent, and when would the model make its prediction?
- Have missing values, invalid values, duplicates, and extreme measurements
  been checked and handled for a reason?
- Is the target separated from features? Are there identifiers or future
  information that should not be used?
- Did I split before fitting preprocessing, selecting features, or resampling?
- Are preprocessing and model steps fitted together in a pipeline?
- Does the split match the real use case (time, groups, and class balance)?
- Did I compare training and validation performance and investigate a large
  gap?
- Is the metric appropriate for the business cost of different mistakes?
- Did I leave the test set alone until model choices were finished?
- Can the result be reproduced and the same pipeline be used at prediction
  time?

## Takeaway

Good validation is part of data preparation, not an afterthought. Clean
according to the data's meaning, split rows before learning transformations,
fit preprocessing only on training data, compare models using validation or
cross-validation, and save the test set for one final check. A model is useful
not because it memorizes its training examples, but because it performs
reliably on new examples it has not seen.
