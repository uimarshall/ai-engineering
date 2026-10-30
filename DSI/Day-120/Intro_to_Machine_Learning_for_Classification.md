# Introduction to Machine Learning for Classification (Practical)

Classification is a `supervised machine-learning` task in which a `model learns`
to `assign` an `observation` to a `category`. Examples include:

- deciding whether an email is spam or not spam;
- predicting whether a customer will churn;
- classifying a transaction as legitimate or fraudulent; and
- identifying whether a tumour is benign or malignant.

The categories are called **classes**, hence the name `Classification`. In a `binary classification` problem there
are two classes, while a multiclass problem has three or more classes.

This note uses the same practical workflow that we would use on a business
dataset:

1. understand the rows and the target;
2. separate the features (`X`) from the target (`y`);
3. split into training and test data **before fitting preprocessing**; -
4. handle missing values and transform features;
5. train more than one model;
6. evaluate the predictions with metrics that match the business problem; and
7. use the selected model to predict a new observation.

The complete runnable example is in
[`classification_practical.py`](classification_practical.py).

Now, **Fitting preprocessing** means letting a data-preparation step _learn what it needs from the training data_ before it prepares data for a model.

For example, suppose some values are missing. An imputer might learn the **median** from the training data, then use that median to fill in missing values. A scaler might learn the training data’s **average and spread**, then use them to put values on a similar scale.

The important order is:

1. Split the data into training and test sets.
2. **Fit** preprocessing using the training data.
3. Use those same learned settings to **transform** both the training data and the test data.

It’s a bit like learning a recipe from your practice ingredients, then using that same recipe on new ingredients. If the test data helps determine the recipe, the model has indirectly seen information from its test—which can make its evaluation unfairly optimistic.

In the example in `Intro_to_Machine_Learning_for_Classification.md`, the pipeline learns how to fill missing values and scale features during training. When you later predict on a new observation, the pipeline automatically applies those learned steps first.

## 1. Classification versus regression

Regression predicts a number, such as a house price:

```text
house features -> 385000.00
```

Classification predicts a label, often with a probability:

```text
patient features -> malignant (probability = 0.94)
```

The probability is useful because a business can choose a decision threshold.
For example, a medical screening system might prefer to flag more possible
cases, even if that creates more false alarms.

## 2. A practical dataset

The Python example uses scikit-learn's built-in breast-cancer dataset. It has
numeric measurements calculated from images of breast-cell nuclei:

- each row represents one tumour observation;
- each feature is a measurement such as radius, texture, or perimeter; and
- the target identifies the tumour class.

Using a built-in dataset makes the lesson reproducible: no download or API
credentials are needed. In a real project, replace the dataset-loading section
with a `pandas.read_csv(...)` call and inspect the schema first.

```python
from sklearn.datasets import load_breast_cancer

dataset = load_breast_cancer(as_frame=True)
data = dataset.frame
print(data.head())
print(data.shape)
print(data.isna().sum().sum())
```

The final expression counts all missing cells. Missing values must be checked
before training. Even when this particular dataset has no missing values, the
pipeline below includes an imputer so the workflow is safe for a future CSV
that does contain missing measurements.

## 3. Features and target

Let:

- `X` be the input columns, also called features or predictors; and
- `y` be the value we want to predict, also called the target or label.

Never include the target column in `X`. If the target accidentally becomes a
feature, the model can appear excellent while simply reading the answer.

```python
X = data.drop(columns="target")
y = data["target"]
```

## 4. Split before preprocessing

The test set represents future, unseen data. We must not allow information from
it to influence preprocessing decisions. Therefore, split first and fit the
imputer and scaler only on the training data.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)
```

`stratify=y` keeps a similar class balance in both sets. `random_state` makes
the example reproducible. In a time-dependent problem, use a chronological
split instead of a random split.

## 5. Build preprocessing pipelines

Two common preprocessing steps are:

1. **imputation**: replace missing numeric values with a statistic learned from
   the training data; and
2. **standardisation**: convert features to a similar scale.

Standardisation is especially important for logistic regression and K-nearest
neighbours. A feature measured in thousands should not dominate a feature
measured in decimals merely because of its unit.

`Pipeline` keeps preprocessing and modelling together. This prevents a common
mistake: fitting an imputer or scaler on all data before the split, which is a
form of data leakage.

```python
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

scaled_preprocessing = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)
```

## 6. Four useful classification algorithms

### Logistic regression

Despite its name, logistic regression is a classification algorithm. It
estimates a probability using a logistic function and then converts that
probability into a class. It is often an excellent interpretable baseline.

### Decision tree

A decision tree repeatedly asks questions such as “is radius less than this
value?” Trees are easy to explain, but a deep tree can memorise the training
data. `max_depth` limits its complexity.

### Random forest

A random forest combines many decision trees. The trees see different samples
and feature subsets, so their combined prediction is usually more robust than a
single tree.

### K-nearest neighbours (KNN)

KNN finds the closest training observations and predicts the most common class
among them. It is intuitive, but it is sensitive to feature scale and can be
slower when the dataset is large.

## 7. Train and compare models

The example compares all four models using the same fixed train/test split.
That makes the comparison fair.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

models = {
    "Logistic regression": Pipeline(
        steps=[
            ("preprocessing", scaled_preprocessing),
            ("model", LogisticRegression(max_iter=2_000, random_state=42)),
        ]
    ),
    "Decision tree": Pipeline(
        steps=[
            ("preprocessing", scaled_preprocessing),
            ("model", DecisionTreeClassifier(max_depth=4, random_state=42)),
        ]
    ),
    "Random forest": Pipeline(
        steps=[
            ("preprocessing", scaled_preprocessing),
            ("model", RandomForestClassifier(
                n_estimators=200, random_state=42, n_jobs=-1
            )),
        ]
    ),
    "K-nearest neighbours": Pipeline(
        steps=[
            ("preprocessing", scaled_preprocessing),
            ("model", KNeighborsClassifier(n_neighbors=7)),
        ]
    ),
}

for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    print(name, predictions[:5])
```

## 8. Evaluate more than accuracy

Accuracy is the proportion of correct predictions:

```text
accuracy = correct predictions / all predictions
```

It can be misleading when one class is much more common than the other. The
confusion matrix gives a fuller picture:

|                       |  Predicted negative |  Predicted positive |
| --------------------- | ------------------: | ------------------: |
| **Actually negative** |  True negative (TN) | False positive (FP) |
| **Actually positive** | False negative (FN) |  True positive (TP) |

Important metrics include:

- **precision**: of the observations predicted positive, how many were truly
  positive?
- **recall**: of the truly positive observations, how many did we find?
- **F1 score**: a balance between precision and recall;
- **ROC-AUC**: how well the model ranks positive observations above negative
  observations; and
- **confusion matrix**: the actual counts of each type of outcome.

Which metric matters most depends on the cost of mistakes. For fraud detection,
recall may matter because missed fraud is expensive. For an expensive manual
review process, precision may matter because false alarms consume staff time.

The script prints accuracy, precision, recall, F1, ROC-AUC, and a confusion
matrix for every model:

```python
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

print(accuracy_score(y_test, predictions))
print(classification_report(y_test, predictions))
print(confusion_matrix(y_test, predictions))
print(roc_auc_score(y_test, probabilities))
```

Do not choose a model only because it has the highest accuracy. Check whether
its errors are acceptable for the application and whether the model is
maintainable, fast enough, and understandable to its users.

## 9. Predicting a new observation

Once a model has been selected, pass a new row with exactly the same feature
columns used during training. The pipeline automatically applies the fitted
imputer and scaler before making the prediction.

```python
best_model = models["Logistic regression"]
new_observation = X_test.iloc[[0]]
predicted_class = best_model.predict(new_observation)[0]
predicted_probability = best_model.predict_proba(new_observation)[0, 1]

print(predicted_class)
print(predicted_probability)
```

Use double brackets in `iloc[[0]]` so the result remains a one-row table with
the expected feature names.

## 10. Common beginner mistakes

1. **Preprocessing before splitting**: fit transformations on training data
   only.
2. **Using accuracy as the only metric**: inspect precision, recall, F1, and
   the confusion matrix.
3. **Ignoring missing values**: count missing values and choose an approach
   appropriate for the domain.
4. **Forgetting feature scale**: KNN and many linear models need comparable
   feature scales.
5. **Overfitting a decision tree**: limit depth or use regularisation.
6. **Changing several things at once**: use a fixed split and compare models
   systematically.
7. **Treating a probability as a certainty**: probabilities estimate model
   confidence; they are not guarantees.

## 11. Run the example

From the repository root, run:

```powershell
python DSI\Day-120\classification_practical.py
```

The script uses `numpy`, `pandas`, and `scikit-learn`. If they are not already
available in your Python environment, install them using the repository's
existing dependency workflow rather than installing packages globally.

## Summary

Classification learns a mapping from features to discrete classes. A reliable
workflow splits the data before fitting preprocessing, handles missing values,
trains multiple candidate models, and evaluates errors using metrics that match
the real cost of false positives and false negatives. The most useful first
model is not always the most complicated one: a well-evaluated logistic
regression baseline can be easier to explain and operate than a more complex
alternative.
