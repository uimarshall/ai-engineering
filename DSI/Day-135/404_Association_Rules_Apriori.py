############################################################

# Association Rule Learning (using Apriori)

############################################################

###########################################################
# Import required packages
###########################################################

import pandas as pd
from apyori import apriori

##########################################################
# Import data
##########################################################

# Import

alcohol_transactions = pd.read_csv("data/sample_data_apriori.csv")

# drop ID column

alcohol_transactions.drop("transaction_id", axis=1, inplace=True)

# modify data for apriori algorithm

transactions_list = []

for index, row in alcohol_transactions.iterrows():
    transaction = list(row.dropna())  # drop any missing values in each row
    transactions_list.append(transaction)


#########################################################
# Apply the Apriori algorithm
#########################################################

apriori_rules = apriori(
    transactions_list,
    min_support=0.003,
    min_confidence=0.2,
    min_lift=3,
    max_length=2,
)

apriori_rules = list(apriori_rules)

if apriori_rules:
    apriori_rules[0]

########################################################
# Convert output to DataFrame
########################################################

if apriori_rules:
    apriori_rules[0][2][0][0]

    product1 = [list(rule[2][0][0])[0] for rule in apriori_rules]
    product2 = [list(rule[2][0][1])[0] for rule in apriori_rules]
    support = [rule[1] for rule in apriori_rules]
    confidence = [rule[2][0][2] for rule in apriori_rules]
    lift = [rule[2][0][3] for rule in apriori_rules]

    apriori_rules_df = pd.DataFrame(
        {
            "product1": product1,
            "product2": product2,
            "support": support,
            "confidence": confidence,
            "lift": lift,
        }
    )

    ########################################################
    # Sort rules by descending lift
    ########################################################

    apriori_rules_df = apriori_rules_df[
        apriori_rules_df["product1"].str.contains("New Zealand")
    ].sort_values("lift", ascending=False)
else:
    print("No rules found with the given minimum support and confidence thresholds.")
