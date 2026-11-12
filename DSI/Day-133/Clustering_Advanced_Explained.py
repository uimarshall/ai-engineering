############################################################
# K Means Clustering - Advanced Template (WITH DETAILED EXPLANATIONS)
# 
# Purpose: This script performs customer segmentation using K-Means clustering
# on customer purchasing patterns across different grocery product categories
############################################################

# ============================================================
# SECTION 1: IMPORT REQUIRED PYTHON PACKAGES
# ============================================================
# These are libraries (pre-built code packages) that provide tools we need

import matplotlib.pyplot as plt  # For creating visualizations/plots
import pandas as pd              # For working with data in tables (like Excel)
from sklearn.cluster import KMeans  # Machine Learning algorithm for clustering (grouping similar items)
from sklearn.preprocessing import MinMaxScaler  # For normalizing data to a 0-1 scale


############################################################
# SECTION 2: CREATE AND PREPARE THE DATA
############################################################

# ============================================================
# Step 1: Import the data from Excel files
# ============================================================
# Read the "transactions" sheet from the Excel file
# This contains individual customer purchases with sales amounts
transactions = pd.read_excel("data/grocery_database.xlsx", sheet_name="transactions")

# Read the "product_areas" sheet from the Excel file
# This contains mapping of product area IDs to product area names (e.g., "Dairy", "Meat")
product_areas = pd.read_excel("data/grocery_database.xlsx", sheet_name="product_areas")


# ============================================================
# Step 2: Combine/Merge the two datasets
# ============================================================
# Use "inner join" to merge transactions with product_areas based on product_area_id
# This adds the product area name to each transaction
transactions = pd.merge(transactions, product_areas, how="inner", on="product_area_id")


# ============================================================
# Step 3: Clean the data - Remove Non-Food items
# ============================================================
# Remove all rows where product_area_name is "Non-Food"
# We only want food products for this analysis
transactions.drop(
    transactions[transactions["product_area_name"] == "Non-Food"].index, inplace=True
)


# ============================================================
# Step 4: Aggregate data to customer level
# ============================================================
# Group all purchases by customer_id and product_area_name, then sum the sales
# This shows how much each customer spent in each product category
transaction_summary = (
    transactions.groupby(["customer_id", "product_area_name"])["sales_cost"]
    .sum()
    .reset_index()
)


# ============================================================
# Step 5: Transform data into matrix format (Pivot Table)
# ============================================================
# Reshape data so:
#   - Rows = individual customers
#   - Columns = product areas (Dairy, Meat, Fruit, Vegetables, etc.)
#   - Values = total sales amount in each category
# aggfunc="sum" combines multiple purchases
# fill_value=0 replaces missing values with 0 (customer didn't buy that category)
# margins=True adds a "Total" column showing total spend per customer
transaction_summary_pivot = transactions.pivot_table(
    index="customer_id",
    columns="product_area_name",
    values="sales_cost",
    aggfunc="sum",
    fill_value=0,
    margins=True,
    margins_name="Total",
).rename_axis(None, axis=1)


# ============================================================
# Step 6: Convert spending amounts to percentages
# ============================================================
# Instead of absolute dollar amounts, convert to % of each customer's total spending
# This is important because it makes customers comparable
# (a $100 spender vs a $1000 spender should be treated fairly)
# div() divides each row by the "Total" column
transaction_summary_pivot = transaction_summary_pivot.div(
    transaction_summary_pivot["Total"], axis=0
)


# ============================================================
# Step 7: Drop the Total column (we don't need it for clustering)
# ============================================================
# Keep only the product area percentage columns for clustering
data_for_clustering = transaction_summary_pivot.drop(["Total"], axis=1)


######################################################
# SECTION 3: DATA PREPARATION & CLEANING
######################################################

# ============================================================
# Step 1: Check for missing values
# ============================================================
# Count how many missing values (NaN) exist in each column
# This helps identify data quality issues
data_for_clustering.isna().sum()


# ============================================================
# Step 2: Normalize the data (Scale to 0-1 range)
# ============================================================
# WHY? Different features might have different ranges
# MinMaxScaler converts all values to a 0-1 scale
# This prevents columns with larger numbers from dominating the algorithm

# Create a MinMaxScaler object (a normalizer tool)
scale_norm = MinMaxScaler()

# Apply the scaler to our data and convert back to a DataFrame
# fit_transform() learns the min/max values from the data and applies the scaling
data_for_clustering_scaled = pd.DataFrame(
    scale_norm.fit_transform(data_for_clustering), 
    columns=data_for_clustering.columns  # Keep original column names
)


#####################################################
# SECTION 4: FIND OPTIMAL NUMBER OF CLUSTERS (k) USING ELBOW METHOD
#####################################################
# WHY? K-Means requires us to specify the number of clusters beforehand
# We use the "Elbow Method" to find the best k value

# ============================================================
# Step 1: Create a list of k values to test (1 through 9 clusters)
# ============================================================
k_values = list(range(1, 10))

# ============================================================
# Step 2: Calculate WCSS for each k value
# ============================================================
# WCSS = Within Cluster Sum of Squares
# It measures how tightly packed clusters are (lower = better/tighter clusters)
# We'll calculate WCSS for each k value to see how it changes

wcss_list = []  # Empty list to store WCSS values

# Loop through each k value
for k in k_values:
    # Create a KMeans model with k clusters and random_state=42 for reproducibility
    kmeans = KMeans(n_clusters=k, random_state=42)
    
    # Train the model on our normalized data
    kmeans.fit(data_for_clustering_scaled)
    
    # Get the WCSS value (inertia_) and add it to our list
    wcss_list.append(kmeans.inertia_)


# ============================================================
# Step 3: Plot the Elbow Curve
# ============================================================
# Create a line plot showing WCSS vs K
plt.plot(k_values, wcss_list)
plt.title("Within Cluster Sum of Squares - by k")
plt.xlabel("K (Number of Clusters)")
plt.ylabel("WCSS Score")
plt.tight_layout()
plt.show()

# HOW TO READ: Look for the "elbow" - where the curve bends
# The point where the curve flattens out is usually the best k value
# (In this case, it appears k=3 is a good choice)


#####################################################
# SECTION 5: TRAIN THE FINAL K-MEANS MODEL
#####################################################

# ============================================================
# Step 1: Create and train the K-Means model
# ============================================================
# Create a KMeans model with 3 clusters (from our elbow method analysis)
# random_state=42 ensures we get the same results every time (for reproducibility)
kmeans = KMeans(n_clusters=3, random_state=42)

# Train the model on our normalized scaled data
# This finds the 3 best cluster centers and assigns each customer to a cluster
kmeans.fit(data_for_clustering_scaled)


#####################################################
# SECTION 6: APPLY AND ANALYZE CLUSTER RESULTS
#####################################################

# ============================================================
# Step 1: Add cluster labels to our original data
# ============================================================
# kmeans.labels_ gives us cluster assignments (0, 1, or 2) for each customer
# Add this as a new column to our data
data_for_clustering["cluster"] = kmeans.labels_


# ============================================================
# Step 2: Check cluster sizes
# ============================================================
# Count how many customers are in each cluster
# value_counts() shows the frequency of each cluster label
data_for_clustering["cluster"].value_counts()


#####################################################
# SECTION 7: PROFILE THE CLUSTERS
#####################################################

# ============================================================
# Step 1: Calculate average spending % per product area for each cluster
# ============================================================
# Group by cluster and calculate the mean (average) for each product category
# This tells us what each cluster likes to buy
cluster_summary = (
    data_for_clustering.groupby("cluster")[["Dairy", "Fruit", "Meat", "Vegetables"]]
    .mean()
    .reset_index()
)

# Display the summary
print("\n=== CLUSTER PROFILES ===")
print(cluster_summary)

# HOW TO INTERPRET:
# - Cluster 0: Shows what % on average each product category these customers buy
# - Cluster 1: Different spending pattern
# - Cluster 2: Another different spending pattern
# 
# EXAMPLE: If Cluster 0 has high "Dairy" and low "Vegetables", 
# it's a dairy-loving customer segment!
