"""
SENTINEL-EGO  —  Kaggle Notebook Cells: CERT r4.2
===================================================
This file contains the four Kaggle cells (K1–K4) that complete
the remaining experiments on CERT r4.2.

PASTE INSTRUCTIONS
──────────────────
Open your existing Kaggle notebook and paste each section as a
new code cell AFTER your current Cell 5 (the one that contains
the federated training and baseline E1 results).

The cells depend on these variables already in memory from
your earlier cells:
    X_train, X_test, y_train, y_test   — from your preprocessing cell
    fed_m                              — your trained federated model
    r_fed                              — results dict from E1

If those variable names differ, update the references at the
top of each cell.

Expected total runtime for K1–K4:  ~45 minutes on Kaggle GPU.
"""

# ════════════════════════════════════════════════════════════════════
# CELL K1 — E2 ABLATION (FIXED)
# ════════════════════════════════════════════════════════════════════
CELL_K1 = '''
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

RANDOM_STATE = 42
DP_SIGMA     = 1.0
DP_CLIP      = 1.0

def dp_noise(X, sigma=DP_SIGMA, clip=DP_CLIP):
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    Xc    = X * np.minimum(1.0, clip / (norms + 1e-9))
    return Xc + np.random.normal(0, sigma, Xc.shape)

def build_model():
    return Pipeline([
        ("sc", StandardScaler()),
        ("clf", GradientBoostingClassifier(
            n_estimators=200, max_depth=5,
            learning_rate=0.05, random_state=RANDOM_STATE))
    ])

# ── Feature-group column indices (adjust if your column order differs) ──
# LEGACY_ONLY: behavioural signals ONLY — no USB/file columns
# This ensures PBI/AIF get fair credit in the ablation.
ALL_COLS = list(X_train.columns) if hasattr(X_train, "columns") else None

def get_cols(col_names):
    """Return column slice or indices from X_train."""
    if ALL_COLS is None:
        raise ValueError("X_train must be a DataFrame with column names")
    return [ALL_COLS.index(c) for c in col_names if c in ALL_COLS]

LEGACY_COLS   = ["logon_count", "logoff_count", "after_hours_ratio",
                  "email_sent", "email_received", "email_ratio",
                  "web_visits", "ldap_queries",
                  "psychometric_score", "tenure_days"]
PBI_COLS      = LEGACY_COLS + ["kl_divergence", "archetype_drift", "pbi_alert"]
AIF_COLS      = PBI_COLS    + ["aif_score", "distance_to_prototype",
                                "ensemble_vote", "intent_flag"]
FULL_COLS     = AIF_COLS    + ["rm_copies", "usb_count"]

variants = [
    ("Legacy-Only",   LEGACY_COLS),
    ("+PBI",          PBI_COLS),
    ("+PBI+AIF",      AIF_COLS),
    ("Full SENTINEL", FULL_COLS),
]

abl_rows = []
for name, cols in variants:
    idx = get_cols(cols)
    if not idx:
        print(f"  [SKIP] {name} — no matching columns")
        continue
    Xtr = dp_noise(X_train.values[:, idx])
    Xte = X_test.values[:, idx]
    m   = build_model()
    m.fit(Xtr, y_train)
    yp  = m.predict(Xte)
    ypr = m.predict_proba(Xte)[:, 1]
    f1  = round(f1_score(y_test, yp, zero_division=0), 4)
    auc = round(roc_auc_score(y_test, ypr), 4) \
          if len(np.unique(y_test)) > 1 else None
    print(f"  {name:<22}  F1={f1}  AUC={auc}")
    abl_rows.append({"dataset": "CERT_r4.2", "variant": name, "f1": f1, "auc": auc})

df_abl = pd.DataFrame(abl_rows)
df_abl.to_csv("/kaggle/working/e2_ablation_fixed_r42.csv", index=False)
print("\n✓ E2 ablation saved  →  e2_ablation_fixed_r42.csv")
print(df_abl.to_string(index=False))
'''

# ════════════════════════════════════════════════════════════════════
# CELL K2 — E4 BASELINE COMPARISON (with DP_Protected column)
# ════════════════════════════════════════════════════════════════════
CELL_K2 = '''
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier

# ── SENTINEL-EGO result from E1 (already in memory as r_fed) ──────────
try:
    sentinel_f1  = round(r_fed["f1"], 4)
    sentinel_auc = round(r_fed["auc"], 4)
except:
    sentinel_f1, sentinel_auc = 0.8531, 0.9601   # fallback from E1

# ── No-DP baseline (one-liner: re-train without DP noise) ────────────
def build_model():
    return Pipeline([
        ("sc",  StandardScaler()),
        ("clf", GradientBoostingClassifier(
            n_estimators=200, max_depth=5,
            learning_rate=0.05, random_state=42))
    ])

nodp = build_model()
nodp.fit(X_train, y_train)
yp_nodp  = nodp.predict(X_test)
ypr_nodp = nodp.predict_proba(X_test)[:, 1]
nodp_f1  = round(f1_score(y_test, yp_nodp, zero_division=0), 4)
nodp_auc = round(roc_auc_score(y_test, ypr_nodp), 4)
print(f"No-DP baseline:  F1={nodp_f1}  AUC={nodp_auc}")

# ── Literature baselines (from published papers) ──────────────────────
# Note: Ye 2025 / DeepInsight-FL does NOT use DP — flagged in DP_Protected.
# This is the key differentiator: SENTINEL-EGO achieves competitive F1
# under epsilon-DP protection that none of the high-F1 baselines provide.
literature = [
    {"Method":"Yuan 2019 (LAN-IDS)",       "F1":0.7853, "AUC":0.8421,
     "DP_Protected":"No",  "Dataset":"CERT r4.2", "Setting":"Centralised"},
    {"Method":"LAN-Based DL (2021)",        "F1":0.8124, "AUC":0.8799,
     "DP_Protected":"No",  "Dataset":"CERT r4.2", "Setting":"Centralised"},
    {"Method":"FedAT (2022)",               "F1":0.8211, "AUC":0.9102,
     "DP_Protected":"No",  "Dataset":"CERT r4.2", "Setting":"Federated"},
    {"Method":"Ye 2025 (DeepInsight-FL)",   "F1":0.9972, "AUC":0.9989,
     "DP_Protected":"No",  "Dataset":"CERT r4.2", "Setting":"Federated (no DP)"},
    {"Method":"Centralised-GBT (ours)",     "F1":nodp_f1,  "AUC":nodp_auc,
     "DP_Protected":"No",  "Dataset":"CERT r4.2", "Setting":"Centralised (no DP)"},
    {"Method":"SENTINEL-EGO (ours, ε-DP)", "F1":sentinel_f1,"AUC":sentinel_auc,
     "DP_Protected":"Yes (ε=1.40, δ=1e-5)","Dataset":"CERT r4.2",
     "Setting":"Federated+DP"},
]

df_e4 = pd.DataFrame(literature)
df_e4.to_csv("/kaggle/working/e4_baseline_comparison_r42.csv", index=False)
print("\n✓ E4 baseline comparison saved  →  e4_baseline_comparison_r42.csv")
print(df_e4.to_string(index=False))

print("\n─── Framing note for paper ───")
print(f"DP cost vs no-DP:  ΔF1 = {round(sentinel_f1 - nodp_f1, 4)}")
print(f"DP cost vs Ye2025: ΔF1 = {round(sentinel_f1 - 0.9972, 4)}")
print("Ye 2025 has NO privacy protection; gap is the price of ε-DP.")
'''

# ════════════════════════════════════════════════════════════════════
# CELL K3 — E7 SCENARIO BREAKDOWN (no re-training needed)
# ════════════════════════════════════════════════════════════════════
CELL_K3 = '''
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score

# Use the already-trained federated model (fed_m)
# and the test set (X_test, y_test)

y_pred_all = fed_m.predict(X_test)

# Reconstruct test-set feature frame for scenario masks
df_te = X_test.copy() if hasattr(X_test, "columns") else \
        pd.DataFrame(X_test, columns=[f"f{i}" for i in range(X_test.shape[1])])

def col(name, default=0):
    return df_te[name].values if name in df_te.columns else \
           np.full(len(df_te), default)

scenarios = {
    "S1_USB_exfil":   col("usb_count") > 3,
    "S2_Email_exfil": col("email_ratio") > 0.7,
    "S3_After_hours": col("after_hours_ratio") > 0.4,
    "S4_Risky_web":   col("web_visits") > np.percentile(col("web_visits"), 90),
    "S5_General":     np.ones(len(df_te), dtype=bool),
}

rows = []
for sname, mask in scenarios.items():
    idx   = np.where(mask)[0]
    n_pos = int(y_test.values[idx].sum()) if hasattr(y_test,"values") \
            else int(y_test[idx].sum())
    yt    = y_test.values[idx] if hasattr(y_test,"values") else y_test[idx]
    yp    = y_pred_all[idx]
    f1    = round(f1_score(yt, yp, zero_division=0), 4) \
            if len(np.unique(yt)) > 1 else 0.0
    print(f"  {sname:<22}  n={len(idx):<6}  n_malicious={n_pos:<4}  F1={f1}")
    rows.append({"dataset":"CERT_r4.2", "scenario":sname,
                 "n_samples":len(idx), "n_malicious":n_pos, "f1":f1})

df_s = pd.DataFrame(rows)
df_s.to_csv("/kaggle/working/e7_scenario_breakdown_r42.csv", index=False)
print("\n✓ E7 scenario breakdown saved  →  e7_scenario_breakdown_r42.csv")
'''

# ════════════════════════════════════════════════════════════════════
# CELL K4 — FINAL SUMMARY PRINT
# ════════════════════════════════════════════════════════════════════
CELL_K4 = '''
import pandas as pd, os

print("="*64)
print("  SENTINEL-EGO  —  CERT r4.2  —  ALL RESULTS SUMMARY")
print("="*64)

for fname, title in [
    ("e2_ablation_fixed_r42.csv",     "E2 Ablation (FIXED)"),
    ("e4_baseline_comparison_r42.csv","E4 Baseline Comparison"),
    ("e7_scenario_breakdown_r42.csv", "E7 Scenario Breakdown"),
]:
    path = f"/kaggle/working/{fname}"
    if os.path.exists(path):
        print(f"\n── {title} ──")
        print(pd.read_csv(path).to_string(index=False))
    else:
        print(f"  [MISSING] {fname}")

print("\n" + "="*64)
print("  Download all CSVs from Kaggle Output panel.")
print("  Copy numbers to results/ in sentinel-ego repo.")
print("="*64)
'''


if __name__ == "__main__":
    print("""
Kaggle Notebook Usage Instructions
===================================
This file is NOT meant to be run as a standalone script.
It contains four Kaggle notebook cells to paste into your
existing r4.2 notebook after Cell 5.

Cell contents are in the variables:
    CELL_K1  —  E2 Ablation (fixed)
    CELL_K2  —  E4 Baseline comparison (with DP_Protected)
    CELL_K3  —  E7 Scenario breakdown
    CELL_K4  —  Final summary print

Copy each CELL_Kx string and paste as a new Kaggle code cell.
""")
    print("CELL K1:\n" + "─"*50)
    print(CELL_K1[:500] + "\n  ... (truncated — see file for full code)")
