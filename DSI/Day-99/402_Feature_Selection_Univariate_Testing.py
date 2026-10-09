"""
here we're going to look at applying univariate testing approaches from Scikit Learn to help us understand the strength of relationships
between each individual input variable and our output variables code in a way that means you have a
template for the practical tutorials as well as any machine projects you work on in your data science career.
"""

import numpy as np
import pandas as pd

my_df = pd.read_csv("feature_selection_sample_data.csv")

"""
so as we learned in the theory tutorial Univariate testing for feature selection uses statistical tests to show which inputs variable have 
the strongest relationship with the output variable. 
In Scikit-learn, we use something called SelectKBest which can be used in conjunction with many of the common tests for relationships
strength, both for the classification tasks and regression tasks.

It's called SelectKBest as we can tell it to select a specified number of features based on the relationship strengths that it calculates. 
This pre specified number is referred to as K. 
Let's start building a template for a regression task, or in other words, where our output variable is numeric.
"""

# Regression Template

#  f_regression - is a linear model that tests the individual effect of each of our input variables.

from sklearn.feature_selection import SelectKBest, f_regression

"""
Now, as the aim of this approach is to understand the relationships between input variables and the output variable, 
we need to separate out the inputs from the output and have them installed as two separate objects. 
It's very common to label these new objects as an uppercase "X" and a lowercase "y".
"""

X = my_df.drop(["output"], axis=1)
y = my_df["output"]

"""
Next is to instantiate our feature_selection object using the SelectKBS imported.
And then within parentheses we want to specify the statistical test that we want it to apply for regression tasks 
we'll use f_regression that we also imported.

regression assesses the range between each input variable and output, providing us with an f-score and P-value, 
which both essentially tell us how confident we can be that there is a true and robust relationship between the input and the output. 
After this, we can also specify a value four K, which is a number of variables that you'd like to select.

Now the "K" value defaults to ten, but in our case we only have four input variables in total,so let's just put the value as "all" 
for now, so "K" equals "all". 
In many cases we won't actually know the value four K and there's no right or wrong answer for it.

"""
feature_selector = SelectKBest(f_regression, k="all")

"""
Next, Let's use the fit_method so it calculates the relationship scores for each input variable.

X object which just contains our input variables and then our Y object which just contains our output variable. 
Let's run this and get it to learn what those relationships are.

Now that we've run the "fit" method, if we want to assess the relationship scores, we can do this using some key attributes of 
our fit object for p-values. we can see the p-value for each one of our input variables, and a lower p value here is better,
or it means that there is more confidence that the relationship is robust. Input variables 3 & 4 are slightly larger.

If "e" is Scientific Notation (× 10)

• 2e-2 = 0.02
• 2e-5 = 0.00002
• 0.02 is much larger than 0.00002 

fit.pvalues_
Out[6]: array([6.41321253e-14, 3.11971032e-14, 3.28616228e-01, 5.11901492e-01])

For the f-scores, we can see again that input 1 & 2 have very high values here, whereas input 3 and 4 have very low values.
in the case of f scores, a higher value indicates a stronger relationship.

fit.scores_
Out[7]: array([96.13254595, 99.97291167,  0.97062608,  0.43552725])
"""
fit = feature_selector.fit(X, y)

fit.pvalues_
fit.scores_

"""
Let's turn these into something more useful. Let's create a data frame with the information for each. 
"""
p_values = pd.DataFrame(np.asarray(fit.pvalues_))
scores = pd.DataFrame(np.asarray(fit.scores_))
input_variable_names = pd.DataFrame(X.columns)

"""
we can now concatenate these together into a single data frame - we concatenate the cols(axis=1) rather than the rows.
"""
summary_stats = pd.concat([input_variable_names, p_values, scores], axis=1)

"""
Name the cols
we now have a really useful DF which gives us the summary statistics for each of our input variables in terms of their 
relationship strength with our output.
"""

summary_stats.columns = ["input_variable", "p_value", "f_score"]

# sorting the DF
"""
Remember we are just dealing with 3 input variables here but in a scenario where we're dealing with something like 100 input variables, 
it would be really tricky to figure out which variables had strong relationships and which didn't, sorting will help in this regard.

summary_stats
Out[18]: 
  input_variable       p_value    f_score
1         input2  3.119710e-14  99.972912
0         input1  6.413213e-14  96.132546
2         input3  3.286162e-01   0.970626
3         input4  5.119015e-01   0.435527

it now has sorted it by lowest p-value to highest p-value so the input variable which had the strongest relationship 
in theory with the output variable is input2 and then input1 and then input3 and then input4 as seen above.

"""
summary_stats.sort_values(by="p_value", inplace=True)

"""
With the Information in this format we could manually just select the variables with p-values under some specified threshold may be 0.05, for example, 
but I want to make all of our lives a bit easier. So let's write a couple of lines of code we can use to create an 
updated X object that just contains the columns with p-values that fall under some specified threshold.
"""
# Let's create a threshold for the p value.

p_value_threshold = 0.05
score_threshold = 5

"""
Now let's use the "loc" functionality from Pandas to only select the rows from our DF that we want. 
Essentially, the input variables where the f-score and the p-value that meet the thresholds that we have set.
"""
selected_variables = summary_stats.loc[
    (summary_stats["f_score"] >= score_threshold)
    & (summary_stats["p_value"] <= p_value_threshold)
]

"""
we can see that we have this selected_variables DF, which now only contains the two variables that meet those thresholds.

selected_variables
Out[21]: 
  input_variable       p_value    f_score
1         input2  3.119710e-14  99.972912
0         input1  6.413213e-14  96.132546 

Now, to dynamically update our X object to only contain those two input variables, 
we need to grab the column names from our selected variables data frame and put them into a list. 
"""
# To overwrite our selected variables and make it a list
selected_variables = selected_variables["input_variable"].tolist()

"""
we can now create an object which is an updated version of our X object, our input variables, 
which only contains those two input variables.
"""
X_new = X[selected_variables]

"""
Our new X object but only with the two input variables that we deem to have a strong and robust relationship with our output variable. 
So now if we use this approach, we'd be ready to build our model based on only the variables we believe to be important, 
or at least have a significant relationship with the output variable that we're looking to predict.
"""
# Using K = 2 instead of "all"

"""
remember that when we instantiated our Select K best object above, we specified a value of K equals "all" 
if we instead wanted a specific number of the best input variables, we could input this number.So instead of K = all, let's put K = 2

we instantiate our object and fit it to our data. Once we've done that, we could then use the transform method to create our 
new X object and it would automatically just select the two best input variables.

we can see that we are again returned just two columns, and these would be input1 and input2 just as we saw before, 
but it's returned an array, and with an array we only have values we don't know what these columns actually are, 
but we can find this out using a method called get_support().
"""

feature_selector = SelectKBest(f_regression, k=2)
fit = feature_selector.fit(X, y)
X_new1 = feature_selector.transform(X)
feature_selector.get_support()
X_new1 = X.loc[:, feature_selector.get_support()]

# Classification Template

from sklearn.feature_selection import SelectKBest, chi2

X = my_df.drop(["output"], axis=1)
y = my_df["output"]

feature_selector = SelectKBest(chi2, k="all")

fit = feature_selector.fit(X, y)

p_values = pd.DataFrame(np.asarray(fit.pvalues_))
scores = pd.DataFrame(np.asarray(fit.scores_))
input_variable_names = pd.DataFrame(X.columns)

"""
we can now concatenate these together into a single data frame - we concatenate the cols(axis=1) rather than the rows.
"""
summary_stats = pd.concat([input_variable_names, p_values, scores], axis=1)

"""
Name the cols
we now have a really useful DF which gives us the summary statistics for each of our input variables in terms of their 
relationship strength with our output.
"""

summary_stats.columns = ["input_variable", "p_value", "chi2_score"]

# sorting the DF

summary_stats.sort_values(by="p_value", inplace=True)

# Let's create a threshold for the p value.

p_value_threshold = 0.05
score_threshold = 5

"""
Now let's use the "loc" functionality from Pandas to only select the rows from our DF that we want. 
Essentially, the input variables where the f-score and the p-value that meet the thresholds that we have set.
"""
selected_variables = summary_stats.loc[
    (summary_stats["chi2_score"] >= score_threshold)
    & (summary_stats["p_value"] <= p_value_threshold)
]

# To overwrite our selected variables and make it a list
selected_variables = selected_variables["input_variable"].tolist()


X_new = X[selected_variables]
