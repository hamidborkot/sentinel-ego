# ============================================================
# Phase 1: Behavioral Archetype Discovery
# K-Means clustering with silhouette-score optimization
# The Sentinel Ego — Persistent Behavioral Identity
# ============================================================

import numpy as np
import pandas as pd
from scipy.stats import entropy
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from typing import Tuple, List


ARCHETYPE_NAMES = [
    "Morning Bird", "Collaborator", "Balanced", "Workaholic",
    "Night Owl", "Tech Savvy", "Careful Planner", "Lone Wolf",
    "Workaholic_8", "Social Butterfly"
]


def normalized_hist(series, bins):
    counts, _ = np.histogram(series, bins=bins)
    counts = counts.astype(float) + 1e-9
    return counts / counts.sum()


def build_user_features(sent_df: pd.DataFrame, eligible_users: list) -> pd.DataFrame:
    """Build 8-feature behavioral vectors for each eligible user."""
    records = []
    for user in eligible_users:
        u = sent_df[sent_df["owner"] == user]
        if len(u) < 100:
            continue

        hour_dist = normalized_hist(u["hour"], bins=np.arange(25))
        dow_dist = normalized_hist(u["dayofweek"], bins=np.arange(8))

        peak_hour = u["hour"].mode().iloc[0] if len(u) > 0 else 9

        records.append({
            "owner": user,
            "total_sent": len(u),
            "active_days": u["date_only"].nunique(),
            "mean_hour": u["hour"].mean(),
            "std_hour": u["hour"].std(),
            "peak_hour": float(peak_hour),
            "weekend_ratio": u["dayofweek"].isin([5, 6]).mean(),
            "mean_recipients": u["recipient_total"].mean(),
            "median_recipients": u["recipient_total"].median(),
            "mean_subject_len": u["subject_len"].mean(),
            "entropy_hour": entropy(hour_dist + 1e-12),
            "entropy_dow": entropy(dow_dist + 1e-12),
            "emails_per_active_day": len(u) / max(u["date_only"].nunique(), 1),
        })

    return pd.DataFrame(records)


def find_optimal_k(features_df: pd.DataFrame,
                   feature_cols: List[str],
                   k_range: range = range(2, 12),
                   random_state: int = 42) -> Tuple[int, dict]:
    """Run silhouette-score optimization to find optimal K."""
    X = features_df[feature_cols].fillna(0).values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    scores = {}
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        labels = km.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels)
        scores[k] = score
        print(f"  K={k:2d}  silhouette={score:.4f}")

    optimal_k = max(scores, key=scores.get)
    print(f"\nOptimal K = {optimal_k} (silhouette={scores[optimal_k]:.4f})")
    return optimal_k, scores


def assign_archetypes(features_df: pd.DataFrame,
                      feature_cols: List[str],
                      k: int = 10,
                      random_state: int = 42) -> pd.DataFrame:
    """Assign archetype labels to users via K-Means."""
    X = features_df[feature_cols].fillna(0).values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    km = KMeans(n_clusters=k, random_state=random_state, n_init=10)
    labels = km.fit_predict(X_scaled)

    features_df = features_df.copy()
    features_df["cluster"] = labels

    # Name clusters by mean_hour centroid order
    cluster_means = features_df.groupby("cluster")["mean_hour"].mean().sort_values()
    name_map = {old: ARCHETYPE_NAMES[i] for i, old in enumerate(cluster_means.index)}
    features_df["archetype"] = features_df["cluster"].map(name_map)

    print("Archetype assignment complete:")
    print(features_df.groupby("archetype")["owner"].count().to_string())
    return features_df
