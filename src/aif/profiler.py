# ============================================================
# Phase 2: AIF Attacker Profiler — Multi-model Training
# The Sentinel Ego — Adversarial Interaction Fingerprinting
# ============================================================

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import f1_score, roc_auc_score, classification_report
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import lightgbm as lgb
import shap
from typing import Dict, Tuple


MODEL_CONFIGS = {
    "RandomForest": RandomForestClassifier(
        n_estimators=200, max_depth=20, class_weight="balanced", n_jobs=-1, random_state=42
    ),
    "XGBoost": xgb.XGBClassifier(
        n_estimators=200, max_depth=6, learning_rate=0.05, subsample=0.8,
        use_label_encoder=False, eval_metric="logloss", random_state=42, verbosity=0
    ),
    "LightGBM": lgb.LGBMClassifier(
        n_estimators=200, verbose=-1, random_state=42
    ),
    "MLP": MLPClassifier(
        hidden_layer_sizes=(256, 128, 64), max_iter=500, random_state=42
    ),
}


def train_and_evaluate(
    X: np.ndarray,
    y: np.ndarray,
    dataset_name: str,
    use_smote: bool = True,
    test_size: float = 0.20,
    random_state: int = 42,
) -> pd.DataFrame:
    """Train all 4 AIF models and return evaluation metrics."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    if use_smote:
        try:
            sm = SMOTE(random_state=random_state)
            X_train_s, y_train = sm.fit_resample(X_train_s, y_train)
            print(f"  SMOTE applied. New train size: {len(y_train):,}")
        except Exception as e:
            print(f"  SMOTE skipped: {e}")

    results = []
    for model_name, model in MODEL_CONFIGS.items():
        print(f"  Training {model_name}...")
        model.fit(X_train_s, y_train)
        y_pred = model.predict(X_test_s)
        y_prob = (
            model.predict_proba(X_test_s)[:, 1]
            if hasattr(model, "predict_proba") else y_pred.astype(float)
        )

        f1_macro = f1_score(y_test, y_pred, average="macro")
        f1_weighted = f1_score(y_test, y_pred, average="weighted")
        auc = roc_auc_score(y_test, y_prob)

        results.append({
            "dataset": dataset_name,
            "model": model_name,
            "f1_macro": round(f1_macro, 4),
            "f1_weighted": round(f1_weighted, 4),
            "auc_roc": round(auc, 4),
            "n_train": len(y_train),
            "n_test": len(y_test),
        })
        print(f"    F1={f1_macro:.4f}  AUC={auc:.4f}")

    return pd.DataFrame(results)


def compute_shap_importance(
    model,
    X_sample: np.ndarray,
    feature_names: list,
    max_samples: int = 500
) -> pd.DataFrame:
    """Compute SHAP feature importance for the best model."""
    X_s = X_sample[:max_samples]
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_s)

    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    importance = np.abs(shap_values).mean(axis=0)
    return pd.DataFrame({
        "feature": feature_names,
        "shap_importance": importance
    }).sort_values("shap_importance", ascending=False).reset_index(drop=True)
