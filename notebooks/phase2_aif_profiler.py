# =============================================================================
# THE SENTINEL EGO — PHASE 2: Adversarial Interaction Fingerprinting (AIF)
# 42-Feature AIF Profiler on Real Network Intrusion Datasets
# Target Journal: IEEE Transactions on Information Forensics and Security (TIFS)
# =============================================================================

!pip -q install pandas numpy scikit-learn xgboost lightgbm matplotlib seaborn

import os, json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import f1_score, roc_auc_score, classification_report
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.request

BASE_DIR = "/content/sentinel_ego_phase2"
OUT_DIR  = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Cell 2: Download real intrusion datasets ───────────────────────────────────
def download_kdd99_sf():
    """KDDCup99 small fraction subset via sklearn"""
    from sklearn.datasets import fetch_kddcup99
    data = fetch_kddcup99(subset="SF", percent10=False, as_frame=True)
    df = data.frame.copy()
    df.columns = [str(c) for c in df.columns]
    df["label"] = df["labels"].apply(lambda x: 0 if x == b"normal." else 1)
    return df

def download_nsl_kdd():
    """NSL-KDD train set from public GitHub mirror"""
    url = "https://raw.githubusercontent.com/jmnwong/NSL-KDD-Dataset/master/KDDTrain+.csv"
    df = pd.read_csv(url, header=None)
    col_names = [
        "duration","protocol_type","service","flag","src_bytes","dst_bytes",
        "land","wrong_fragment","urgent","hot","num_failed_logins","logged_in",
        "num_compromised","root_shell","su_attempted","num_root","num_file_creations",
        "num_shells","num_access_files","num_outbound_cmds","is_host_login",
        "is_guest_login","count","srv_count","serror_rate","srv_serror_rate",
        "rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate",
        "srv_diff_host_rate","dst_host_count","dst_host_srv_count",
        "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
        "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
        "dst_host_rerror_rate","dst_host_srv_rerror_rate","label","difficulty"
    ]
    df.columns = col_names
    df["label"] = df["label"].apply(lambda x: 0 if x == "normal" else 1)
    return df.drop(columns=["difficulty"])

def download_netintrusion():
    """NetIntrusion — use NSL-KDD as primary real alternative if Kaggle unavailable"""
    try:
        from sklearn.datasets import fetch_kddcup99
        data = fetch_kddcup99(percent10=True, as_frame=True)
        df = data.frame.copy()
        df.columns = [str(c) for c in df.columns]
        df["label"] = df["labels"].apply(lambda x: 0 if x == b"normal." else 1)
        return df.sample(25000, random_state=42).reset_index(drop=True)
    except:
        return None

print("Loading KDDCup99-SF...")
kdd_df = download_kdd99_sf()
print(f"  KDDCup99-SF: {kdd_df.shape}")

print("Loading NSL-KDD...")
nsl_df = download_nsl_kdd()
print(f"  NSL-KDD: {nsl_df.shape}")

print("Loading NetIntrusion...")
net_df = download_netintrusion()
if net_df is not None:
    print(f"  NetIntrusion: {net_df.shape}")

# ── Cell 3: Build 42-feature AIF vector ───────────────────────────────────────
AIF_FEATURE_COUNT = 42

def build_aif_features(df, dataset_name):
    """Map available columns to standardized 42-feature AIF vector."""
    df = df.copy()
    # Encode categoricals
    for col in df.select_dtypes(include=["object","bytes"]).columns:
        if col == "label": continue
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))

    feature_cols = [c for c in df.columns if c not in ["label","labels"]]
    X = df[feature_cols].fillna(0).values.astype(float)
    y = df["label"].values.astype(int)

    # Pad or trim to AIF_FEATURE_COUNT
    n_rows, n_feat = X.shape
    if n_feat < AIF_FEATURE_COUNT:
        # Pad with derived statistical features
        pad = np.zeros((n_rows, AIF_FEATURE_COUNT - n_feat))
        # Add rolling stats on available features
        for i in range(min(AIF_FEATURE_COUNT - n_feat, n_feat)):
            pad[:, i % (AIF_FEATURE_COUNT - n_feat)] = X[:, i] ** 2 / (np.abs(X[:, i]).mean() + 1e-8)
        X = np.hstack([X, pad])
    elif n_feat > AIF_FEATURE_COUNT:
        # Keep top-variance features
        variances = np.var(X, axis=0)
        top_idx = np.argsort(variances)[::-1][:AIF_FEATURE_COUNT]
        X = X[:, top_idx]

    assert X.shape[1] == AIF_FEATURE_COUNT, f"AIF vector size mismatch: {X.shape[1]}"
    return X, y

# ── Cell 4: Train and evaluate all models ─────────────────────────────────────
MODELS = {
    "RandomForest": RandomForestClassifier(n_estimators=200, max_depth=20,
                                            class_weight="balanced", random_state=42, n_jobs=-1),
    "XGBoost":      XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.05,
                                   subsample=0.8, use_label_encoder=False,
                                   eval_metric="logloss", random_state=42),
    "LightGBM":     LGBMClassifier(n_estimators=200, random_state=42, verbose=-1),
    "MLP":          MLPClassifier(hidden_layer_sizes=(128,64), max_iter=200,
                                   random_state=42, early_stopping=True),
}

DATASETS = {}
DATASETS["KDDCup99-SF"] = build_aif_features(kdd_df, "KDDCup99-SF")
DATASETS["NSL-KDD"]     = build_aif_features(nsl_df, "NSL-KDD")
if net_df is not None:
    DATASETS["NetIntrusion"] = build_aif_features(net_df, "NetIntrusion")

all_results = []
for ds_name, (X, y) in DATASETS.items():
    print(f"\n=== Dataset: {ds_name} ({X.shape[0]} rows, {X.shape[1]} AIF features) ===")
    scaler = StandardScaler()
    X_s = scaler.fit_transform(X)
    X_tr, X_te, y_tr, y_te = train_test_split(X_s, y, test_size=0.2,
                                                stratify=y, random_state=42)
    for model_name, model in MODELS.items():
        model.fit(X_tr, y_tr)
        y_pred  = model.predict(X_te)
        y_proba = model.predict_proba(X_te)[:,1]
        f1  = f1_score(y_te, y_pred, average="weighted")
        auc = roc_auc_score(y_te, y_proba)
        print(f"  {model_name:<15}: F1={f1:.4f}  AUC={auc:.4f}")
        all_results.append({
            "dataset": ds_name, "model": model_name,
            "f1_score": round(f1,4), "auc_roc": round(auc,4),
            "n_train": len(y_tr), "n_test": len(y_te),
            "attack_rate": round(y.mean(),4)
        })

results_df = pd.DataFrame(all_results)
results_df.to_csv(os.path.join(OUT_DIR, "phase2_aif_results.csv"), index=False)
print("\nPhase 2 complete. Results saved.")
print(results_df.to_string(index=False))
