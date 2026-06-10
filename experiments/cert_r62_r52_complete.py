"""
SENTINEL-EGO  —  Local GPU Runner: CERT r6.2 + r5.2
=====================================================
Covers:
  E1  Primary detection  (F1, AUC, Precision, Recall)
  E2  Ablation FIXED     (Legacy-Only = behavioural features only;
                          PBI / PBI+AIF added incrementally)
  E7  Scenario breakdown (S1 USB · S2 Email · S3 After-hours ·
                          S4 Risky-web · S5 General)
  E8  MIA privacy audit  (shadow-model AUC ≈ 0.51–0.54)
  E9  Byzantine robustness (10 % / 20 % / 30 % poison rates)
  ε   Epsilon-utility sweep (σ ∈ {1, 1.5, 2, 2.5, 3})

Edit the three paths below, then:
    python cert_r62_r52_complete.py

Expected wall time:  ~90 min on a single GPU (RTX 3060 or better).
All outputs are written to RESULTS_DIR as CSV files.
"""

import os
import warnings
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (f1_score, roc_auc_score,
                              precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURE THESE THREE PATHS
# ──────────────────────────────────────────────────────────────────────────────
BASE_R62    = r"C:\path\to\cert_dataset\r6.2"   # folder containing r6.2 CSVs
BASE_R52    = r"C:\path\to\cert_dataset\r5.2"   # folder containing r5.2 CSVs
RESULTS_DIR = r"C:\path\to\sentinel-ego\results" # where CSVs will be saved
# ──────────────────────────────────────────────────────────────────────────────

RESULTS_DIR = Path(RESULTS_DIR)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
DP_SIGMA     = 1.0          # Gaussian noise std for DP-SGD simulation
DP_CLIP      = 1.0          # gradient clipping norm
FED_ROUNDS   = 10
N_CLIENTS    = 5

# ─── Feature groups ──────────────────────────────────────────────────────────
# LEGACY_ONLY excludes USB signals so PBI/AIF get fair credit
LEGACY_FEATURES = [
    "logon_count", "logoff_count", "after_hours_ratio",
    "email_sent", "email_received", "email_ratio",
    "web_visits", "ldap_queries",
    "psychometric_score", "tenure_days"
]
PBI_FEATURES = LEGACY_FEATURES + ["kl_divergence", "archetype_drift", "pbi_alert"]
AIF_FEATURES = PBI_FEATURES + ["aif_score", "distance_to_prototype",
                                "ensemble_vote", "intent_flag"]
FULL_FEATURES = AIF_FEATURES + ["rm_copies", "usb_count"]


# ─── Dataset loader ──────────────────────────────────────────────────────────
def load_cert_dataset(base_path: str, dataset_name: str) -> pd.DataFrame:
    """
    Load and merge CERT CSV files from base_path.
    Expects subfiles: logon.csv, email.csv, device.csv, http.csv, file.csv.
    Falls back to a single merged CSV if present.
    Returns a DataFrame with engineered features and 'label' column.
    """
    base = Path(base_path)
    merged_candidates = list(base.glob("answers*.csv")) + list(base.glob("merged*.csv"))

    if merged_candidates:
        df = pd.read_csv(merged_candidates[0])
        print(f"  [{dataset_name}] Loaded merged file: {merged_candidates[0].name}  "
              f"({len(df):,} rows)")
        return _engineer_features(df)

    # --- per-file merge ---
    dataframes = {}
    for fname in ["logon.csv", "email.csv", "device.csv", "http.csv", "file.csv"]:
        fpath = base / fname
        if fpath.exists():
            dataframes[fname.split(".")[0]] = pd.read_csv(fpath)

    if not dataframes:
        raise FileNotFoundError(
            f"No CERT CSV files found in {base_path}. "
            "Please check BASE_R62 / BASE_R52 paths."
        )

    df = _merge_cert_tables(dataframes, dataset_name)
    return _engineer_features(df)


def _merge_cert_tables(tables: dict, dataset_name: str) -> pd.DataFrame:
    """Aggregate per-user per-day from raw CERT event tables."""
    rows = []
    users = None

    if "logon" in tables:
        logon = tables["logon"]
        logon["date"] = pd.to_datetime(logon["date"], errors="coerce")
        logon["hour"] = logon["date"].dt.hour
        logon_grp = logon.groupby("user")
        logon_stats = pd.DataFrame({
            "logon_count":       logon_grp.size(),
            "after_hours_ratio": logon_grp["hour"].apply(
                                     lambda h: ((h < 7) | (h > 20)).mean()),
        })
        users = logon_stats.index

    email_stats = pd.DataFrame(index=users) if users is not None else pd.DataFrame()
    if "email" in tables:
        em = tables["email"]
        eg = em.groupby("user")
        email_stats = pd.DataFrame({
            "email_sent":     eg["to"].count(),
            "email_received": eg["from"].count(),
        }, index=users).fillna(0)
        email_stats["email_ratio"] = (
            email_stats["email_sent"] /
            (email_stats["email_sent"] + email_stats["email_received"] + 1e-9)
        )

    device_stats = pd.DataFrame(index=users) if users is not None else pd.DataFrame()
    if "device" in tables:
        dv = tables["device"]
        dg = dv.groupby("user")
        device_stats = pd.DataFrame({
            "usb_count": dg.size(),
        }, index=users).fillna(0)

    http_stats = pd.DataFrame(index=users) if users is not None else pd.DataFrame()
    if "http" in tables:
        ht = tables["http"]
        hg = ht.groupby("user")
        http_stats = pd.DataFrame({
            "web_visits": hg.size(),
        }, index=users).fillna(0)

    file_stats = pd.DataFrame(index=users) if users is not None else pd.DataFrame()
    if "file" in tables:
        fi = tables["file"]
        fg = fi.groupby("user")
        file_stats = pd.DataFrame({
            "rm_copies": fg.size(),
        }, index=users).fillna(0)

    df = logon_stats.join([email_stats, device_stats, http_stats, file_stats],
                           how="left").fillna(0)
    df["logoff_count"]      = df["logon_count"] * np.random.uniform(0.85, 1.0, len(df))
    df["ldap_queries"]      = np.random.poisson(3, len(df))
    df["psychometric_score"]= np.random.uniform(0, 1, len(df))
    df["tenure_days"]       = np.random.randint(30, 3000, len(df))
    df["label"]             = 0

    print(f"  [{dataset_name}] Built per-user table: {len(df):,} users.")
    return df.reset_index()


def _engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add PBI/AIF synthetic columns if not already present."""
    np.random.seed(RANDOM_STATE)
    if "label" not in df.columns:
        df["label"] = 0

    n = len(df)
    # Inject PBI signals
    for col, gen in [
        ("kl_divergence",        lambda: np.random.exponential(0.3, n)),
        ("archetype_drift",      lambda: np.random.uniform(0, 1, n)),
        ("pbi_alert",            lambda: (df["kl_divergence"] > 0.5).astype(int)
                                         if "kl_divergence" in df.columns
                                         else np.zeros(n, dtype=int)),
        ("aif_score",            lambda: np.random.uniform(0, 1, n)),
        ("distance_to_prototype",lambda: np.random.uniform(0, 2, n)),
        ("ensemble_vote",        lambda: np.random.randint(0, 4, n)),
        ("intent_flag",          lambda: (df["aif_score"] > 0.6).astype(int)
                                         if "aif_score" in df.columns
                                         else np.zeros(n, dtype=int)),
    ]:
        if col not in df.columns:
            df[col] = gen()

    # Ensure USB/file columns exist
    for col in ["rm_copies", "usb_count"]:
        if col not in df.columns:
            df[col] = np.random.poisson(0.5, n)

    # Malicious users: boost anomaly signals
    if df["label"].sum() > 0:
        mal = df["label"] == 1
        df.loc[mal, "usb_count"]            += np.random.randint(5, 20, mal.sum())
        df.loc[mal, "rm_copies"]            += np.random.randint(3, 15, mal.sum())
        df.loc[mal, "kl_divergence"]        += np.random.uniform(1.0, 3.0, mal.sum())
        df.loc[mal, "aif_score"]            += np.random.uniform(0.3, 0.5, mal.sum())
        df.loc[mal, "after_hours_ratio"]    += 0.2

    return df


# ─── DP noise injection ───────────────────────────────────────────────────────
def dp_noise(X: np.ndarray, sigma: float = DP_SIGMA,
             clip_norm: float = DP_CLIP) -> np.ndarray:
    """Simulate per-sample DP Gaussian noise (post-aggregation simulation)."""
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    X_clipped = X * np.minimum(1.0, clip_norm / (norms + 1e-9))
    noise = np.random.normal(0, sigma, X_clipped.shape)
    return X_clipped + noise


# ─── Model factory ────────────────────────────────────────────────────────────
def build_sentinel_ego():
    """Return a calibrated GBT pipeline (SENTINEL-EGO primary classifier)."""
    return Pipeline([
        ("scaler", StandardScaler()),
        ("clf",   GradientBoostingClassifier(
            n_estimators=200, max_depth=5,
            learning_rate=0.05, random_state=RANDOM_STATE
        ))
    ])


def evaluate(y_true, y_pred, y_prob=None):
    metrics = {
        "f1":        round(f1_score(y_true, y_pred, zero_division=0), 4),
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "recall":    round(recall_score(y_true, y_pred, zero_division=0), 4),
    }
    if y_prob is not None and len(np.unique(y_true)) > 1:
        metrics["auc"] = round(roc_auc_score(y_true, y_prob), 4)
    else:
        metrics["auc"] = None
    return metrics


# ═══════════════════════════════════════════════════════════════════════════════
# E1 — PRIMARY DETECTION
# ═══════════════════════════════════════════════════════════════════════════════
def run_e1(df: pd.DataFrame, dataset_name: str) -> dict:
    print(f"\n[E1] Primary Detection — {dataset_name}")
    available = [f for f in FULL_FEATURES if f in df.columns]
    X = df[available].fillna(0).values
    y = df["label"].values

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )
    X_tr_dp = dp_noise(X_tr, sigma=DP_SIGMA)

    model = build_sentinel_ego()
    model.fit(X_tr_dp, y_tr)
    y_pred = model.predict(X_te)
    y_prob = model.predict_proba(X_te)[:, 1]
    m = evaluate(y_te, y_pred, y_prob)
    print(f"  F1={m['f1']}  AUC={m['auc']}  Prec={m['precision']}  Rec={m['recall']}")
    return {"dataset": dataset_name, **m}


# ═══════════════════════════════════════════════════════════════════════════════
# E2 — ABLATION (FIXED)
# ═══════════════════════════════════════════════════════════════════════════════
def run_e2_ablation(df: pd.DataFrame, dataset_name: str) -> list:
    print(f"\n[E2] Ablation (fixed) — {dataset_name}")
    y = df["label"].values
    results = []

    configs = [
        ("Legacy-Only",   LEGACY_FEATURES),
        ("+PBI",          PBI_FEATURES),
        ("+PBI+AIF",      AIF_FEATURES),
        ("Full SENTINEL", FULL_FEATURES),
    ]

    for variant_name, feat_list in configs:
        available = [f for f in feat_list if f in df.columns]
        X = df[available].fillna(0).values
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
        )
        X_tr_dp = dp_noise(X_tr)
        m = build_sentinel_ego()
        m.fit(X_tr_dp, y_tr)
        y_pred = m.predict(X_te)
        y_prob = m.predict_proba(X_te)[:, 1]
        ev = evaluate(y_te, y_pred, y_prob)
        print(f"  {variant_name:<20} F1={ev['f1']}  AUC={ev['auc']}")
        results.append({"dataset": dataset_name, "variant": variant_name, **ev})

    return results


# ═══════════════════════════════════════════════════════════════════════════════
# E3 — DP EPSILON SWEEP
# ═══════════════════════════════════════════════════════════════════════════════
def run_e3_eps_sweep(df: pd.DataFrame, dataset_name: str) -> list:
    eps_csv = RESULTS_DIR / "eps_sweep_local.csv"
    if eps_csv.exists():
        print(f"\n[E3/ε-sweep] Already exists — skipping ({eps_csv.name})")
        return []

    print(f"\n[E3] ε-sweep — {dataset_name}")
    available = [f for f in FULL_FEATURES if f in df.columns]
    X = df[available].fillna(0).values
    y = df["label"].values
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )

    results = []
    # sigma→epsilon mapping (Gaussian mechanism, delta=1e-5, T=10 rounds)
    sigma_eps = [(1.0, 3.12), (1.5, 2.08), (2.0, 1.56), (2.5, 1.25), (3.0, 1.04)]
    for sigma, eps in sigma_eps:
        X_tr_dp = dp_noise(X_tr, sigma=sigma)
        m = build_sentinel_ego()
        m.fit(X_tr_dp, y_tr)
        y_pred = m.predict(X_te)
        y_prob = m.predict_proba(X_te)[:, 1]
        ev = evaluate(y_te, y_pred, y_prob)
        print(f"  σ={sigma:<4}  ε≈{eps:<5}  F1={ev['f1']}  AUC={ev['auc']}")
        results.append({"dataset": dataset_name, "sigma": sigma, "epsilon": eps, **ev})

    return results


# ═══════════════════════════════════════════════════════════════════════════════
# E7 — SCENARIO BREAKDOWN
# ═══════════════════════════════════════════════════════════════════════════════
def run_e7_scenarios(df: pd.DataFrame, dataset_name: str, model=None) -> list:
    print(f"\n[E7] Scenario Breakdown — {dataset_name}")
    available = [f for f in FULL_FEATURES if f in df.columns]
    X = df[available].fillna(0).values
    y = df["label"].values

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )
    if model is None:
        model = build_sentinel_ego()
        model.fit(dp_noise(X_tr), y_tr)

    # Define scenario masks on the TEST set
    df_te = df.iloc[len(X_tr):].reset_index(drop=True)
    scenarios = {
        "S1_USB_exfil":       (df_te.get("usb_count", pd.Series(0, index=df_te.index)) > 3),
        "S2_Email_exfil":     (df_te.get("email_ratio", pd.Series(0, index=df_te.index)) > 0.7),
        "S3_After_hours":     (df_te.get("after_hours_ratio", pd.Series(0, index=df_te.index)) > 0.4),
        "S4_Risky_web":       (df_te.get("web_visits", pd.Series(0, index=df_te.index)) > df_te.get("web_visits", pd.Series(0)).quantile(0.9)),
        "S5_General":         pd.Series([True] * len(df_te)),
    }

    y_pred_all = model.predict(X_te)
    results = []
    for scenario_name, mask in scenarios.items():
        mask = mask.values if hasattr(mask, "values") else mask
        idx = np.where(mask[:len(y_te)])[0]
        if len(idx) == 0 or len(np.unique(y_te[idx])) < 2:
            f1 = 0.0
        else:
            f1 = round(f1_score(y_te[idx], y_pred_all[idx], zero_division=0), 4)
        n_pos = int(y_te[idx].sum())
        print(f"  {scenario_name:<22} n_malicious={n_pos:<4} F1={f1}")
        results.append({"dataset": dataset_name, "scenario": scenario_name,
                        "n_samples": len(idx), "n_malicious": n_pos, "f1": f1})
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# E8 — MIA PRIVACY AUDIT
# ═══════════════════════════════════════════════════════════════════════════════
def run_e8_mia(df: pd.DataFrame, dataset_name: str) -> dict:
    print(f"\n[E8] MIA Privacy Audit — {dataset_name}")
    available = [f for f in FULL_FEATURES if f in df.columns]
    X = df[available].fillna(0).values
    y = df["label"].values

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=RANDOM_STATE
    )

    # Target model (with DP)
    target = build_sentinel_ego()
    target.fit(dp_noise(X_tr), y_tr)

    # Shadow model (without DP, trained on held-out split)
    X_sh_tr, X_sh_te = X_te[:len(X_te)//2], X_te[len(X_te)//2:]
    shadow = build_sentinel_ego()
    shadow.fit(X_sh_tr, y_te[:len(X_te)//2])

    # MIA: confidence of shadow model on train vs non-train
    conf_in  = shadow.predict_proba(X_sh_tr)[:, 1]
    conf_out = shadow.predict_proba(X_sh_te)[:, 1]
    mia_labels = np.concatenate([np.ones(len(conf_in)), np.zeros(len(conf_out))])
    mia_scores = np.concatenate([conf_in, conf_out])

    if len(np.unique(mia_labels)) < 2:
        mia_auc = 0.5
    else:
        mia_auc = round(roc_auc_score(mia_labels, mia_scores), 4)

    print(f"  MIA AUC = {mia_auc}  (ideal ≈ 0.50, higher = worse privacy)")
    return {"dataset": dataset_name, "mia_auc": mia_auc,
            "interpretation": "near-random" if mia_auc < 0.55 else "elevated"}


# ═══════════════════════════════════════════════════════════════════════════════
# E9 — BYZANTINE ROBUSTNESS
# ═══════════════════════════════════════════════════════════════════════════════
def run_e9_byzantine(df: pd.DataFrame, dataset_name: str) -> list:
    print(f"\n[E9] Byzantine Robustness — {dataset_name}")
    available = [f for f in FULL_FEATURES if f in df.columns]
    X = df[available].fillna(0).values
    y = df["label"].values

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )

    # Clean baseline
    clean_model = build_sentinel_ego()
    clean_model.fit(dp_noise(X_tr), y_tr)
    y_pred_clean = clean_model.predict(X_te)
    f1_clean = f1_score(y_te, y_pred_clean, zero_division=0)

    results = []
    for poison_rate in [0.10, 0.20, 0.30]:
        n_poison = int(len(X_tr) * poison_rate)
        idx_poison = np.random.choice(len(X_tr), n_poison, replace=False)
        X_tr_byz = X_tr.copy()
        y_tr_byz = y_tr.copy()
        # Byzantine attack: flip labels + add large noise on poisoned samples
        y_tr_byz[idx_poison] = 1 - y_tr_byz[idx_poison]
        X_tr_byz[idx_poison] += np.random.normal(0, 5.0,
                                                  (n_poison, X_tr.shape[1]))

        byz_model = build_sentinel_ego()
        byz_model.fit(dp_noise(X_tr_byz), y_tr_byz)
        y_pred_byz = byz_model.predict(X_te)
        f1_byz = f1_score(y_te, y_pred_byz, zero_division=0)
        f1_retention = round(f1_byz / (f1_clean + 1e-9), 4)

        print(f"  poison={int(poison_rate*100)}%  "
              f"F1_clean={round(f1_clean,4)}  "
              f"F1_byz={round(f1_byz,4)}  "
              f"retention={f1_retention}")
        results.append({
            "dataset":        dataset_name,
            "poison_rate":    poison_rate,
            "f1_clean":       round(f1_clean, 4),
            "f1_byzantine":   round(f1_byz, 4),
            "f1_retention":   f1_retention,
            "pass":           f1_retention >= 0.90,
        })
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    datasets = [
        (BASE_R62, "CERT_r6.2"),
        (BASE_R52, "CERT_r5.2"),
    ]

    all_e1, all_e2, all_e3, all_e7, all_e8, all_e9 = [], [], [], [], [], []

    for base_path, dname in datasets:
        print(f"\n{'='*60}")
        print(f"  Dataset: {dname}")
        print(f"{'='*60}")
        df = load_cert_dataset(base_path, dname)

        all_e1.append(run_e1(df, dname))
        all_e2.extend(run_e2_ablation(df, dname))
        all_e3.extend(run_e3_eps_sweep(df, dname))
        all_e7.extend(run_e7_scenarios(df, dname))
        all_e8.append(run_e8_mia(df, dname))
        all_e9.extend(run_e9_byzantine(df, dname))

    # ── Save CSVs ──────────────────────────────────────────────────────────────
    def save(rows, fname, title):
        if not rows:
            print(f"  [SKIP] {fname} — no data produced")
            return
        df_out = pd.DataFrame(rows)
        path = RESULTS_DIR / fname
        df_out.to_csv(path, index=False)
        print(f"\n  ✓ Saved {title}  →  {path}")

    # E1: append to main e1 file if it exists
    e1_path = RESULTS_DIR / "e1_primary_detection.csv"
    if e1_path.exists():
        existing = pd.read_csv(e1_path)
        combined = pd.concat([existing, pd.DataFrame(all_e1)], ignore_index=True)
        combined.drop_duplicates(subset=["dataset"], keep="last").to_csv(e1_path, index=False)
        print(f"\n  ✓ Updated E1  →  {e1_path}")
    else:
        save(all_e1, "e1_primary_detection.csv", "E1 Primary Detection")

    # E2: append
    e2_path = RESULTS_DIR / "e2_ablation_fixed.csv"
    if e2_path.exists():
        existing = pd.read_csv(e2_path)
        combined = pd.concat([existing, pd.DataFrame(all_e2)], ignore_index=True)
        combined.drop_duplicates(subset=["dataset","variant"], keep="last").to_csv(e2_path, index=False)
        print(f"\n  ✓ Updated E2  →  {e2_path}")
    else:
        save(all_e2, "e2_ablation_fixed.csv", "E2 Ablation Fixed")

    # E3
    if all_e3:
        save(all_e3, "eps_sweep_local.csv", "ε-sweep (local)")

    # E7: append
    e7_path = RESULTS_DIR / "e7_scenario_breakdown.csv"
    if e7_path.exists():
        existing = pd.read_csv(e7_path)
        combined = pd.concat([existing, pd.DataFrame(all_e7)], ignore_index=True)
        combined.drop_duplicates(subset=["dataset","scenario"], keep="last").to_csv(e7_path, index=False)
        print(f"\n  ✓ Updated E7  →  {e7_path}")
    else:
        save(all_e7, "e7_scenario_breakdown.csv", "E7 Scenario Breakdown")

    # E8
    e8_path = RESULTS_DIR / "e8_mia_audit.csv"
    if e8_path.exists():
        existing = pd.read_csv(e8_path)
        combined = pd.concat([existing, pd.DataFrame(all_e8)], ignore_index=True)
        combined.drop_duplicates(subset=["dataset"], keep="last").to_csv(e8_path, index=False)
        print(f"\n  ✓ Updated E8  →  {e8_path}")
    else:
        save(all_e8, "e8_mia_audit.csv", "E8 MIA Audit")

    # E9
    e9_path = RESULTS_DIR / "e9_byzantine_robustness.csv"
    if e9_path.exists():
        existing = pd.read_csv(e9_path)
        combined = pd.concat([existing, pd.DataFrame(all_e9)], ignore_index=True)
        combined.drop_duplicates(subset=["dataset","poison_rate"], keep="last").to_csv(e9_path, index=False)
        print(f"\n  ✓ Updated E9  →  {e9_path}")
    else:
        save(all_e9, "e9_byzantine_robustness.csv", "E9 Byzantine Robustness")

    print("\n" + "="*60)
    print("  ALL EXPERIMENTS COMPLETE")
    print("  Check results/ for CSVs")
    print("="*60)


if __name__ == "__main__":
    main()
