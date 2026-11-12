# K-Means Clustering for Customer Segmentation - Complete Beginner Guide

## 📚 Table of Contents
1. [What is Clustering?](#what-is-clustering)
2. [What is K-Means Clustering?](#what-is-k-means-clustering)
3. [Understanding the Code Step-by-Step](#understanding-the-code-step-by-step)
4. [Modules Explained](#modules-explained)
5. [The Complete Workflow](#the-complete-workflow)
6. [Real-World Analogy](#real-world-analogy)

---

## What is Clustering?

**Clustering** is a technique in machine learning that groups similar items together.

### Simple Example:
Imagine you have a basket of mixed fruit:
- 🍎 Red apples
- 🍏 Green apples
- 🍊 Oranges
- 🍌 Bananas

Clustering would automatically group them as:
- **Cluster 1**: Apples (red and green together)
- **Cluster 2**: Oranges
- **Cluster 3**: Bananas

The algorithm finds items that are similar and puts them in the same group **without you telling it what to look for**.

---

## What is K-Means Clustering?

**K-Means** is one of the most popular clustering algorithms. Here's how it works:

### The "K" Means "Number of Clusters"
- You decide how many groups (clusters) you want
- If K=3, you want 3 groups
- The algorithm finds the best way to divide data into 3 groups

### How K-Means Works (Simple Version):

1. **Pick K random starting points** → These are called "centroids" (cluster centers)
2. **Assign each item to the closest centroid** → Each customer joins the nearest cluster
3. **Move the centroids** → Find the center of each group that formed
4. **Repeat steps 2-3** → Keep adjusting until clusters don't change anymore

### Why Use K-Means?
- ✅ Simple and fast
- ✅ Easy to understand
- ✅ Works well for customer segmentation
- ✅ Widely used in industry

---

## Understanding the Code Step-by-Step

### **PART 1: Import Required Libraries**

```python
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
```

| Library | Purpose | What It Does |
|---------|---------|-------------|
| `matplotlib.pyplot` | Visualization | Creates charts and graphs to visualize data |
| `pandas` | Data manipulation | Works with data in table format (like Excel) |
| `sklearn.cluster.KMeans` | Machine Learning | The K-Means clustering algorithm |
| `sklearn.preprocessing.MinMaxScaler` | Data normalization | Scales all values to 0-1 range |

---

### **PART 2: Load and Explore Data**

```python
transactions = pd.read_excel("data/grocery_database.xlsx", sheet_name="transactions")
product_areas = pd.read_excel("data/grocery_database.xlsx", sheet_name="product_areas")
```

**What's happening:**
- Load transaction data (what customers bought, how much they spent)
- Load product area data (mapping of product IDs to names like "Dairy", "Meat")

**Data Structure:**
```
Transactions Table:
customer_id | product_area_id | sales_cost
    101     |       1         |    $50
    101     |       2         |    $30
    102     |       1         |    $25

Product Areas Table:
product_area_id | product_area_name
       1        |     "Dairy"
       2        |     "Meat"
```

---

### **PART 3: Merge and Clean Data**

```python
transactions = pd.merge(transactions, product_areas, how="inner", on="product_area_id")
```

**What's happening:**
- Combine the two tables using `product_area_id` as the key
- After merge, each transaction has both the product_area_id AND product_area_name

```python
transactions.drop(
    transactions[transactions["product_area_name"] == "Non-Food"].index, inplace=True
)
```

**What's happening:**
- Remove all "Non-Food" products
- We only want food items for this analysis
- `inplace=True` means modify the original table (don't create a new one)

---

### **PART 4: Aggregate Data to Customer Level**

```python
transaction_summary = (
    transactions.groupby(["customer_id", "product_area_name"])["sales_cost"]
    .sum()
    .reset_index()
)
```

**What's happening:**
- Instead of individual transactions, combine all purchases by:
  - Customer ID
  - Product area name
- Sum up total spending in each category per customer

**Result:**
```
customer_id | product_area_name | sales_cost
    101     |     "Dairy"       |   $150
    101     |     "Meat"        |   $80
    102     |     "Dairy"       |   $200
```

---

### **PART 5: Create a Pivot Table (Reshape Data)**

```python
transaction_summary_pivot = transactions.pivot_table(
    index="customer_id",
    columns="product_area_name",
    values="sales_cost",
    aggfunc="sum",
    fill_value=0,
    margins=True,
    margins_name="Total"
)
```

**What's happening:**
- Reshape data from long format to wide format
- Rows = customers
- Columns = product categories
- Values = total spending

**Visual transformation:**

**Before (Long Format):**
```
customer_id | category    | amount
    101     | Dairy       |  $150
    101     | Meat        |  $80
    102     | Dairy       |  $200
    102     | Meat        |  $50
```

**After (Wide Format - Pivot):**
```
customer_id | Dairy | Meat | Vegetables | Total
    101     | $150  | $80  |    $20     | $250
    102     | $200  | $50  |    $30     | $280
```

---

### **PART 6: Convert to Percentages**

```python
transaction_summary_pivot = transaction_summary_pivot.div(
    transaction_summary_pivot["Total"], axis=0
)
```

**What's happening:**
- Convert dollar amounts to percentages of total spending
- This makes customers comparable regardless of spending amount

**Why?**
- Customer A: Spends $1,000 total (80% on Dairy = $800)
- Customer B: Spends $100 total (80% on Dairy = $80)
- Without percentages, the algorithm would treat them as very different
- With percentages, they're similar (both 80% on Dairy)

**Before:**
```
customer_id | Dairy | Meat | Total
    101     | $150  | $80  | $250
    102     | $200  | $50  | $280
```

**After (Percentages):**
```
customer_id | Dairy | Meat  | Total
    101     | 0.60  | 0.32  | 1.00
    102     | 0.71  | 0.18  | 1.00
```

---

### **PART 7: Check for Missing Values**

```python
data_for_clustering.isna().sum()
```

**What's happening:**
- Count how many empty cells (NaN = Not a Number) exist
- Missing data can cause problems with machine learning
- This check helps ensure data quality

---

### **PART 8: Normalize Data (MinMaxScaler)**

```python
scale_norm = MinMaxScaler()
data_for_clustering_scaled = pd.DataFrame(
    scale_norm.fit_transform(data_for_clustering),
    columns=data_for_clustering.columns
)
```

**What's happening:**
- Scale all values to a 0-1 range
- All percentages are already 0-1, so this might not change much here
- But it's important for other data types

**Why Normalize?**
- Prevents features with larger numbers from dominating
- Ensures fair comparison between all features

**Example:**
```
If we have: Weight (0-200 kg) and Price (0-100 dollars)
Without scaling:
  - Weight differences would be 100x bigger
  - Price would be mostly ignored

After MinMaxScaler (0-1):
  - Both weighted equally
```

---

### **PART 9: Find Optimal K (Elbow Method)**

```python
k_values = list(range(1, 10))
wcss_list = []

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data_for_clustering_scaled)
    wcss_list.append(kmeans.inertia_)
```

**What's happening:**
- Test K values from 1 to 9 clusters
- For each K, train a model and measure WCSS (Within Cluster Sum of Squares)
- WCSS = how tightly packed each cluster is (lower = better/tighter groups)

**What is WCSS?**
- Measures distance from each point to its cluster center
- Lower WCSS = tighter, better-defined clusters
- But more clusters = always lower WCSS (with more groups, things are tighter)

```python
plt.plot(k_values, wcss_list)
plt.title("Within Cluster Sum of Squares - by k")
plt.xlabel("K (Number of Clusters)")
plt.ylabel("WCSS Score")
plt.show()
```

**What's happening:**
- Plot WCSS values for each K
- Look for the "elbow" - where the curve bends significantly
- The elbow point is usually the best K value

**Example Graph:**
```
WCSS
  |
  |     •
  |    /
  |   / <- Steep decline (good to go from K=1 to K=2)
  |  /
  | •
  |  \
  |   \ <- Flat (diminishing returns after K=3)
  |    •___•___•
  |_________________ K
  1 2 3 4 5 6
```

The elbow is around K=3 (where it stops being steep and starts flattening)

---

### **PART 10: Train Final Model**

```python
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(data_for_clustering_scaled)
```

**What's happening:**
- Create a K-Means model with 3 clusters (from our elbow analysis)
- Train it on the normalized data
- `random_state=42` ensures reproducibility (same results every time)

**What the model learned:**
- The 3 best cluster centers
- Which cluster each customer belongs to

---

### **PART 11: Apply Cluster Labels**

```python
data_for_clustering["cluster"] = kmeans.labels_
```

**What's happening:**
- Add a new column "cluster" showing which cluster (0, 1, or 2) each customer belongs to
- `kmeans.labels_` contains the cluster assignment for each customer

**Result:**
```
customer_id | Dairy | Meat | Vegetables | cluster
    101     | 0.60  | 0.32 |   0.08     |   0
    102     | 0.71  | 0.18 |   0.11     |   1
    103     | 0.45  | 0.45 |   0.10     |   0
```

---

### **PART 12: Check Cluster Sizes**

```python
data_for_clustering["cluster"].value_counts()
```

**What's happening:**
- Count how many customers are in each cluster
- Shows if clusters are balanced or if one is much larger

**Example Output:**
```
2    250  <- Cluster 2 has 250 customers
0    200  <- Cluster 0 has 200 customers
1    150  <- Cluster 1 has 150 customers
```

---

### **PART 13: Profile the Clusters**

```python
cluster_summary = (
    data_for_clustering.groupby("cluster")[["Dairy", "Fruit", "Meat", "Vegetables"]]
    .mean()
    .reset_index()
)
```

**What's happening:**
- Calculate average spending % for each product category per cluster
- Shows what each cluster's customer type likes to buy

**Example Result:**
```
cluster | Dairy | Fruit | Meat | Vegetables
   0    | 0.35  | 0.25  | 0.25 |   0.15    <- "Balanced buyers"
   1    | 0.60  | 0.10  | 0.15 |   0.15    <- "Dairy lovers"
   2    | 0.20  | 0.30  | 0.40 |   0.10    <- "Meat lovers"
```

**Business Insights:**
- **Cluster 0**: Balanced buyers - target with variety promotions
- **Cluster 1**: Dairy lovers - promote milk, cheese, yogurt
- **Cluster 2**: Meat lovers - promote steak, chicken, processed meats

---

## Modules Explained

### `matplotlib.pyplot` (Plotting/Visualization)
**What it does:** Creates charts and graphs

**Common functions:**
- `plt.plot()` - Creates a line plot
- `plt.scatter()` - Creates a scatter plot
- `plt.bar()` - Creates a bar chart
- `plt.title()` - Adds title
- `plt.xlabel()`, `plt.ylabel()` - Adds axis labels
- `plt.show()` - Displays the plot

---

### `pandas` (Data Manipulation)
**What it does:** Works with data in table format (like Excel)

**Common functions:**
- `pd.read_excel()` - Read data from Excel file
- `pd.merge()` - Combine two tables
- `groupby()` - Group data and perform calculations
- `pivot_table()` - Reshape data
- `isna()` - Check for missing values

---

### `sklearn.cluster.KMeans` (Clustering Algorithm)
**What it does:** Implements the K-Means clustering algorithm

**Common parameters:**
- `n_clusters` - Number of clusters (K)
- `random_state` - Random seed for reproducibility
- `fit()` - Train the model
- `labels_` - Get cluster assignments
- `inertia_` - Get WCSS value

---

### `sklearn.preprocessing.MinMaxScaler` (Data Normalization)
**What it does:** Scales data to 0-1 range

**Common functions:**
- `fit_transform()` - Learn scaling and apply it
- Ensures all features have equal importance

---

## The Complete Workflow

```
┌─────────────────────────────────────────────┐
│ 1. LOAD DATA                                │
│    - Read transactions.xlsx                 │
│    - Read product_areas.xlsx                │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│ 2. CLEAN & PREPARE                          │
│    - Merge tables                           │
│    - Remove non-food                        │
│    - Aggregate by customer                  │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│ 3. RESHAPE DATA                             │
│    - Create pivot table                     │
│    - Convert to percentages                 │
│    - Check for missing values               │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│ 4. NORMALIZE DATA                           │
│    - Scale to 0-1 range using MinMaxScaler  │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│ 5. FIND OPTIMAL K (Elbow Method)            │
│    - Test K = 1 to 9                        │
│    - Calculate WCSS for each K              │
│    - Plot elbow curve                       │
│    - Choose K = 3 (from elbow)              │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│ 6. TRAIN MODEL                              │
│    - Create KMeans with K=3                 │
│    - Fit on normalized data                 │
│    - Learn 3 cluster centers                │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│ 7. ASSIGN CLUSTERS                          │
│    - Add cluster labels to data             │
│    - Each customer assigned to 0, 1, or 2   │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│ 8. ANALYZE RESULTS                          │
│    - Check cluster sizes                    │
│    - Profile each cluster                   │
│    - Extract business insights              │
└─────────────────────────────────────────────┘
```

---

## Real-World Analogy

**Scenario: Sorting customers at a grocery store**

Imagine you own a grocery store and want to group customers by their shopping habits:

### Initial Data (Before Clustering):
You have transaction records:
- Customer A: Buys lots of dairy and meat
- Customer B: Buys lots of vegetables and fruit
- Customer C: Similar to A (dairy and meat)
- Customer D: Similar to B (vegetables and fruit)
- Customer E: Buys everything equally

### Using K-Means with K=3:

**Step 1: Initialize**
- Pick 3 random customer profiles as starting centers
- Center 1: "Healthy eater" (lots of vegetables/fruit)
- Center 2: "Meat lover" (lots of meat)
- Center 3: "Dairy fan" (lots of dairy)

**Step 2: Assign Customers**
- A → Most similar to "Meat lover" (Center 2)
- B → Most similar to "Healthy eater" (Center 1)
- C → Most similar to "Meat lover" (Center 2)
- D → Most similar to "Healthy eater" (Center 1)
- E → Most similar to "Dairy fan" (Center 3)

**Step 3: Recalculate Centers**
- Look at all customers in "Meat lover" cluster (A, C)
- Calculate their average profile
- Move Center 2 to this average point
- Repeat for other clusters

**Step 4: Repeat Until Stable**
- Re-assign customers based on new centers
- Keep adjusting until clusters stop changing

### Final Result:
```
Cluster 0 (Healthy Eaters): B, D
  → Target: Organic/healthy product promotions

Cluster 1 (Meat Lovers): A, C
  → Target: Meat sale promotions

Cluster 2 (Dairy Enthusiasts): E
  → Target: Dairy product deals
```

---

## Key Takeaways for Beginners

1. **Clustering groups similar items together** without being told what to look for
2. **K-Means is one of the simplest clustering algorithms** - easy to understand and implement
3. **The "K" is the number of clusters** you want to create
4. **The Elbow Method helps find the best K** by plotting WCSS vs K
5. **Data normalization is crucial** - ensures all features are weighted equally
6. **The algorithm iterates** - moving centers and re-assigning points until stable
7. **Business insights** come from analyzing what each cluster likes/buys

---

## Practice Questions to Test Understanding

1. **What does WCSS stand for?** → Within Cluster Sum of Squares
2. **Why do we convert spending to percentages?** → To make customers comparable regardless of total spending
3. **What does MinMaxScaler do?** → Scales values to 0-1 range
4. **How many times does the elbow method usually stop?** → At the "elbow" where the curve flattens
5. **What does kmeans.labels_ contain?** → Cluster assignment (0, 1, 2, etc.) for each customer
6. **Why use random_state=42?** → To get reproducible results

---

## Next Steps to Deepen Understanding

1. **Try changing K value** - See how results change with different cluster numbers
2. **Visualize clusters** - Use 2D/3D plots to see cluster separation
3. **Experiment with different datasets** - Try clustering on iris, digits, or your own data
4. **Learn other clustering algorithms** - Hierarchical clustering, DBSCAN, etc.
5. **Study distance metrics** - Why K-Means uses Euclidean distance

---

**Happy Learning! 🎓**
