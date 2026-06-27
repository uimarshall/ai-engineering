## What is machine learning?

Machine learning is the process whereby:

Computers are given the ability to learn to make decisions from data without being explicitly programmed.

Machine learning with scikit-learn
This lesson introduces the fundamentals of supervised learning, a key skill for building models that make predictions from data—an essential step toward making data-driven decisions in your work.

> Can you give me a quick summary?
> Certainly! Here's a quick summary:

- Supervised learning involves training models on labeled data to predict outcomes.

- It uses features to predict a target variable, like predicting house prices or spam emails.

- The data must be clean, numeric, and in the right format before modeling.

- The scikit-learn workflow includes importing a model, fitting it to data, and making predictions.

- The course focuses on understanding these concepts and applying them to real datasets.

## Can you give me a real-life example?

Sure! A real-life example is predicting whether a bank transaction is fraudulent. The model uses features like transaction amount, location, and time to classify each transaction as either fraudulent or not. This helps banks detect suspicious activity automatically.

### What is machine learning?

Machine learning is the process whereby computers learn to make decisions from data without being explicitly programmed.

### Examples of machine learning

For example, learning to predict whether an email is spam or not spam given its content and sender. Or learning to cluster books into different categories based on the words they contain, then assigning any new book to one of the existing clusters.

### Unsupervised learning

Unsupervised learning is the process of uncovering hidden patterns and structures from unlabeled data. For example, a business may wish to group its customers into distinct categories based on their purchasing behavior without knowing in advance what these categories are. This is known as clustering, one branch of unsupervised learning.

### Supervised learning

Supervised learning is a type of machine learning where the values to be predicted are already known, and a model is built with the aim of accurately predicting values of previously unseen data. Supervised learning uses features to predict the value of a target variable, such as predicting a basketball player's position based on their points per game. This course will exclusively focus on supervised learning.

### Types of supervised learning

There are two types of supervised learning. Classification is used to predict the label, or category, of an observation. For example, we can predict whether a bank transaction is fraudulent or not. As there are two outcomes here - a fraudulent transaction, or non-fraudulent transaction, this is known as binary classification. Regression is used to predict continuous values. For example, a model can use features such as number of bedrooms, and the size of a property, to predict the target variable, price of the property.

### Naming conventions

Note that what we call a feature throughout the course, others may call a predictor variable or independent variable. Also, what we call the target variable, others may call dependent variable or response variable.

### Before you use supervised learning

There are some requirements to satisfy before performing supervised learning. Our data must not have missing values, must be in numeric format, and stored as pandas DataFrames or Series, or NumPy arrays. This requires some exploratory data analysis first to ensure data is in the correct format. Various pandas methods for descriptive statistics, along with appropriate data visualizations, are useful in this step.

### scikit-learn syntax

scikit-learn follows the same syntax for all supervised learning models, which makes the workflow repeatable. Let's familiarize ourselves with the general scikit-learn workflow syntax, before we explore using real data later in the chapter. We import a Model, which is a type of algorithm for our supervised learning problem, from an sklearn module. For example, the k-Nearest Neighbors model uses distance between observations to predict labels or values. We create a variable named model, and instantiate the Model. A model is fit to the data, where it learns patterns about the features and the target variable. We fit the model to X, an array of our features, and y, an array of our target variable values. We then use the model's dot-predict method, passing six new observations, X_new. For example, if feeding features from six emails to a spam classification model, an array of six values is returned. A one indicates the model predicts that email is spam, and a zero represents a prediction of not spam.
