"""A runnable introduction to clustering, PCA, and anomaly detection."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42


def make_customer_data() -> pd.DataFrame:
    """Create reproducible customer-like data with two unusual records."""
    blob_result = make_blobs(
        n_samples=300,
        centers=np.array([(30, 3, 25), (70, 8, 60), (45, 15, 35)]),
        cluster_std=[4.0, 6.0, 5.0],
        random_state=RANDOM_STATE,
    )
    features = blob_result[0]
    data = pd.DataFrame(
        features,
        columns=["monthly_spend", "orders_per_month", "average_order_value"],
    )
    unusual = pd.DataFrame(
        [
            {"monthly_spend": 145, "orders_per_month": 1, "average_order_value": 140},
            {"monthly_spend": 5, "orders_per_month": 24, "average_order_value": 2},
        ]
    )
    return pd.concat([data, unusual], ignore_index=True)


def choose_cluster_count(transformed: np.ndarray) -> tuple[int, dict[int, float]]:
    """Compare candidate K-Means sizes and return the best silhouette score."""
    scores: dict[int, float] = {}
    for cluster_count in range(2, 7):
        candidate = KMeans(
            n_clusters=cluster_count,
            n_init=20,
            random_state=RANDOM_STATE,
        )
        labels = candidate.fit_predict(transformed)
        scores[cluster_count] = float(silhouette_score(transformed, labels))
    best_count = max(scores, key=lambda count: scores[count])
    return best_count, scores


def main() -> None:
    data = make_customer_data()
    feature_names = list(data.columns)
    scaler = StandardScaler()
    transformed = scaler.fit_transform(data[feature_names])

    # Keep the deliberately unusual rows from deciding the normal group count.
    cluster_count, scores = choose_cluster_count(transformed[:-2])
    cluster_model = KMeans(
        n_clusters=cluster_count,
        n_init=20,
        random_state=RANDOM_STATE,
    )
    data["cluster"] = cluster_model.fit_predict(transformed)
    data["cluster_distance"] = cluster_model.transform(transformed).min(axis=1)

    anomaly_model = IsolationForest(
        contamination=2 / len(data),
        random_state=RANDOM_STATE,
    )
    data["anomaly"] = anomaly_model.fit_predict(transformed) == -1

    print("Silhouette scores by candidate cluster count:")
    for count, score in scores.items():
        print(f"  k={count}: {score:.3f}")
    print(f"\nSelected k: {cluster_count}")
    print("\nCluster sizes:")
    print(data["cluster"].value_counts().sort_index().to_string())
    print("\nCluster feature means:")
    print(data.groupby("cluster", sort=True)[feature_names].mean().round(1).to_string())
    print("\nPossible anomalies:")
    print(data.loc[data["anomaly"], feature_names].round(1).to_string(index=False))

    principal_components = PCA(n_components=2, random_state=RANDOM_STATE).fit_transform(
        transformed
    )
    figure, axes = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)
    cluster_plot = axes[0].scatter(
        principal_components[:, 0],
        principal_components[:, 1],
        c=data["cluster"],
        cmap="viridis",
        alpha=0.8,
    )
    axes[0].set_title("Customer clusters shown with PCA")
    axes[0].set_xlabel("Principal component 1")
    axes[0].set_ylabel("Principal component 2")
    figure.colorbar(cluster_plot, ax=axes[0], label="Cluster")

    axes[1].scatter(
        principal_components[:, 0],
        principal_components[:, 1],
        c=np.where(data["anomaly"], "crimson", "steelblue"),
        alpha=0.8,
    )
    axes[1].set_title("Possible anomalies")
    axes[1].set_xlabel("Principal component 1")
    axes[1].set_ylabel("Principal component 2")

    output_path = Path(__file__).with_name("unsupervised_learning_results.png")
    figure.savefig(output_path, dpi=150)
    print(f"\nPlot saved to: {output_path}")


if __name__ == "__main__":
    main()
