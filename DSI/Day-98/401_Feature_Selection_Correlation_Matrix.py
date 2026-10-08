# Feature Selection using a simple Correlation Matrix
'''
we're simply going to look at using a correlation matrix to try and understand the strength of relationships 
between our input variables and our output variable.

'''
import pandas as pd

my_df = pd.read_csv("feature_selection_sample_data.csv")

correlation_matrix = my_df.corr()

'''
we have four input variables labeled input one input two input three and input four. 
So the easiest way to understand which variables might be good to include in a model is a simple test of their correlation. 
Firstly, with the output or target variable, and secondly with each other, 
we don't want input variables that are highly correlated with each other. 
In some types of models, such as linear regression, as it can field the multicolinearity assumption, 
it means that we can't really trust the output statistics and makes it hard to understand if: 

    A.  the model is any good and 
B.  what amount of impact each input variable has on predicting the output.

ALong the top row here we can see that both input one and input two have quite a strong correlation with our output variable, 
whereas input three and input four seem to have very weak correlations. Based on this, 
we might think that we only want to include input one and input two in our model and discard input three and four, 
but there is one other thing to consider input one and input two are actually quite highly correlated with each other as we 
can see here with a score of zero point six one, which is not anywhere near a perfect correlation, 
but there definitely is a relationship there should include both in the model or 
should we just include one or the other well this is where the correlation matrix is somewhat limited it doesn't really give us 
those answers. We need the combinations and see what provided us the best performance on our test set, perhaps. 
And this is where a more advanced approach like recursive feature dimension with solidation, like we talked about in the in really handy.
'''

