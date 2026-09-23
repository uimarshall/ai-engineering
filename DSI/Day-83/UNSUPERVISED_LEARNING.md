# Unsupervised Learning: Finding Structure in Unlabelled Data

Unsupervised learning is a branch of machine learning that learns from data **without a target label**. Instead of being told the correct answer for each row, an algorithm looks for useful structure such as groups, compressed representations, or unusual observations.

For example, a supervised model might learn from customer records labelled `churned` or `active`. An unsupervised model receives the customer records without those labels and may discover several natural customer segments.

The runnable companion for this lesson is [unsupervised_learning.py](unsupervised_learning.py). It creates a small synthetic customer dataset, clusters customers, reduces the data to two dimensions for visualisation, and detects deliberately added anomalies.

## Learning goals

By the end of this tutorial, you should be able to:

- explain how unsupervised learning differs from supervised learning;
- choose between clustering, dimensionality reduction, and anomaly detection;
- prepare numerical features so distance-based algorithms behave sensibly;
- train and inspect a K-Means model;
- evaluate clusters with internal metrics and business interpretation;
- use PCA to visualise high-dimensional data;
- use Isolation Forest to flag unusual records; and
- recognise common failure modes and ethical considerations.

## 1. Supervised versus unsupervised learning

| Question      | Supervised learning                    | Unsupervised learning                                   |
| ------------- | -------------------------------------- | ------------------------------------------------------- |
| Training data | Features plus known labels             | Features only                                           |
| Main goal     | Predict a known target                 | Discover structure or unusual behaviour                 |
| Typical tasks | Classification, regression             | Clustering, dimensionality reduction, anomaly detection |
| Example       | Predict whether a transaction is fraud | Find unusual transactions without fraud labels          |
| Evaluation    | Compare predictions with true labels   | Use internal metrics, stability, and domain knowledge   |

Unsupervised learning does not automatically discover the “truth”. It finds patterns according to the features, scale, algorithm, and parameters you provide. A discovered cluster is a mathematical grouping first; it becomes a useful business segment only after someone interprets and validates it.

## 2. Three important unsupervised tasks

### Clustering

Clustering assigns similar observations to groups. Common algorithms include:

- **K-Means:** chooses a requested number of centres and assigns each row to its nearest centre. It is fast and a good first choice for compact, roughly round groups.
- **Hierarchical clustering:** builds a tree of nested groups. It is useful when you want to inspect structure at multiple levels.
- **DBSCAN:** identifies dense regions and can label sparse points as noise. It can find irregularly shaped groups, but its distance parameters need care.

Practical uses include customer segmentation, grouping products by behaviour, grouping documents by topic after text vectorisation, and identifying similar support tickets.

### Dimensionality reduction

Dimensionality reduction represents many features with fewer features while trying to preserve important information.

- **PCA (Principal Component Analysis):** creates linear combinations called principal components. It is useful for visualisation, noise reduction, and speeding up downstream models.
- **t-SNE and UMAP:** often produce useful two-dimensional visualisations of complex data. They are primarily visualisation tools and should not automatically be treated as proof of real clusters.

Practical uses include visualising image embeddings, compressing sensor data, and exploring whether a dataset contains broad structure.

### Anomaly detection

Anomaly detection identifies observations that differ substantially from the majority. Algorithms include Isolation Forest, Local Outlier Factor, and One-Class SVM.

Practical uses include spotting suspicious transactions, equipment faults, unusual network traffic, and data-quality errors. An anomaly is a candidate for investigation, not automatically a confirmed incident.

## 3. A practical workflow

### Step 1: Define the decision

Start with the action the result should support. “Find clusters” is incomplete. A better question is: “Can we create useful customer groups for selecting different retention campaigns?” The intended action affects which features, algorithm, and validation method are appropriate.

### Step 2: Inspect the data

Check data types, missing values, duplicate rows, impossible values, and feature distributions. Unsupervised algorithms will use errors as if they were meaningful patterns.

```python
print(data.info())
print(data.isna().sum())
print(data.describe())
```

### Step 3: Select meaningful features

Use features related to the question. For customer segmentation, useful features might include monthly spend, purchase frequency, and average order value. Avoid an identifier such as `customer_id`: its numeric value has no meaningful distance relationship.

### Step 4: Preprocess carefully

Many algorithms use distance or variance. A feature measured in dollars can overwhelm a feature measured in counts. Standardisation transforms each feature approximately to mean 0 and standard deviation 1:

$$z = \frac{x - \mu}{\sigma}$$

Fit the scaler on training or analysis data only, and apply the same transformation to future data. Handle missing values explicitly, and encode categorical values appropriately rather than pretending category codes are numeric distances.

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

model = make_pipeline(
	StandardScaler(),
	KMeans(n_clusters=3, n_init=20, random_state=42),
)
model.fit(data[features])
```

### Step 5: Fit a baseline and inspect it

Begin with a simple, interpretable algorithm. For K-Means, inspect cluster sizes and the average feature values in each cluster. A label such as `cluster 0` has no inherent meaning; describe the group using its characteristics.

```python
data["cluster"] = model.predict(data[features])
print(data.groupby("cluster")[features].mean().round(1))
print(data["cluster"].value_counts().sort_index())
```

### Step 6: Evaluate from two angles

**Technical evaluation** asks whether the grouping is coherent and stable:

- **Silhouette score:** ranges from -1 to 1. Higher values generally mean each row is closer to its own cluster than to other clusters.
- **Inertia:** the sum of squared distances to cluster centres. It always decreases as more K-Means clusters are added, so use it with an elbow plot rather than alone.
- **Stability:** refit with different seeds or samples and check whether similar groups appear.

**Domain evaluation** asks whether the groups are useful, understandable, large enough to act on, and fair. A technically neat cluster can still be operationally useless.

```python
from sklearn.metrics import silhouette_score

score = silhouette_score(transformed_features, labels)
print(f"Silhouette score: {score:.3f}")
```

### Step 7: Communicate uncertainty

Document the chosen features, preprocessing, algorithm, parameters, random seed, evaluation results, and limitations. Re-check the analysis when the population or data-generation process changes.

## 4. Complete runnable example

The companion script uses `make_blobs` to generate three customer-like groups. It then:

1. adds two extreme records to act as unusual observations;
2. standardises the features;
3. uses the silhouette score to compare candidate K-Means values;
4. fits the selected K-Means model;
5. uses PCA to create a two-dimensional plot; and
6. uses Isolation Forest to flag possible anomalies.

Run it from the `DSI` directory:

```bash
python Day-83/unsupervised_learning.py
```

The script prints cluster summaries, silhouette scores, and anomaly rows. It also writes `Day-83/unsupervised_learning_results.png`. The image is ignored by Git if your repository already ignores generated files; otherwise, remove it after inspecting it.

The code deliberately uses generated data so it is reproducible and does not require a database, API key, or downloaded dataset. To use real data, replace the `make_customer_data` function with a DataFrame load and keep the preprocessing, validation, and interpretation steps.

## 5. Interpreting the example

After running the script, look at the cluster summary rather than the numeric labels. You might see groups such as:

- customers with high spend and frequent purchases;
- customers with lower spend and occasional purchases; and
- customers with moderate spend but high purchase frequency.

The exact values are generated for teaching, so they are not a real market insight. In a production analysis, test whether the segments persist over time and whether a different action for each segment improves a measurable outcome.

## 6. Common mistakes

### Choosing the number of clusters because it looks convenient

K-Means requires `n_clusters`. Compare a sensible range with silhouette scores and an elbow plot, then use domain knowledge. There is no universal automatic answer.

### Forgetting scale

Without standardisation, a large-unit feature can dominate the distance calculation. This may make clusters reflect measurement units rather than behaviour.

### Including IDs or leakage

An ID can create arbitrary separation. A feature created using future information can also produce impressive but invalid structure. Keep identifiers for joining results, not for learning.

### Treating PCA components as original features

PCA components are combinations of the original columns. Inspect component loadings before assigning a human meaning to them.

### Assuming every anomaly is bad

An unusual observation may be a fraud case, a new customer type, a sensor fault, or simply a legitimate rare event. Send candidates for review and measure false positives.

### Clustering sensitive attributes without safeguards

Groups can reproduce historical inequities or act as proxies for protected characteristics. Consider privacy, fairness, explainability, and whether the proposed use is appropriate before acting on segments.

## 7. Choosing an algorithm quickly

| Situation                                                       | Reasonable first experiment      |
| --------------------------------------------------------------- | -------------------------------- |
| Compact numeric groups and a known approximate number of groups | K-Means                          |
| Unknown number of groups, varying density, or noise             | DBSCAN or a density-based method |
| Need to inspect nested group relationships                      | Hierarchical clustering          |
| Need a simple two-dimensional view of many numeric features     | PCA                              |
| Need a shortlist of unusual records                             | Isolation Forest                 |

These are starting points, not rules. Compare alternatives on the same carefully prepared data and validate against the real decision.

## 8. Key takeaways

- Unsupervised learning discovers patterns; it does not provide labelled truth.
- Feature choice and scaling often matter as much as algorithm choice.
- Use metrics such as silhouette score to guide exploration, not to replace domain validation.
- PCA is useful for compression and visualisation, while anomaly detectors produce candidates for investigation.
- A useful result is stable, interpretable, actionable, and appropriate for the people affected by it.
