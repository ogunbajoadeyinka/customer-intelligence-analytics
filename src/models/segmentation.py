"""Validated K-Means customer segmentation using behavioral features."""
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ["recency", "frequency", "monetary"]


def prepare_features(rfm: pd.DataFrame) -> pd.DataFrame:
    x = rfm[FEATURES].copy().clip(lower=0)
    # Log transform controls the heavy tails typical of retail spend/frequency.
    return np.log1p(x)


def choose_k(rfm: pd.DataFrame, k_values=range(2, 9), random_state: int = 42):
    x = prepare_features(rfm)
    scaled = StandardScaler().fit_transform(x)
    results = []
    for k in k_values:
        model = KMeans(n_clusters=k, n_init=20, random_state=random_state)
        labels = model.fit_predict(scaled)
        results.append({"k": k, "silhouette": silhouette_score(scaled, labels), "inertia": model.inertia_})
    scores = pd.DataFrame(results)
    best_k = int(scores.loc[scores["silhouette"].idxmax(), "k"])
    return best_k, scores


def fit_segmentation(rfm: pd.DataFrame, k: int | None = None, random_state: int = 42):
    x = prepare_features(rfm)
    if k is None:
        k, scores = choose_k(rfm, random_state=random_state)
    else:
        scores = None
    pipe = Pipeline([
        ("scale", StandardScaler()),
        ("cluster", KMeans(n_clusters=k, n_init=20, random_state=random_state)),
    ])
    labels = pipe.fit_predict(x)
    output = rfm.copy()
    output["cluster"] = labels
    profile = output.groupby("cluster").agg(
        customers=("customer_id", "nunique"),
        median_recency=("recency", "median"),
        median_frequency=("frequency", "median"),
        median_monetary=("monetary", "median"),
        total_revenue=("monetary", "sum"),
    ).reset_index()
    profile["revenue_share"] = profile["total_revenue"] / profile["total_revenue"].sum()
    return output, profile, pipe, scores
