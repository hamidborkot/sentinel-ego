# =============================================================================
# THE SENTINEL EGO — PHASE 4: Collective Deception Evolution (CDE)
# 15-Round Mutation (Evasive / Mimicry / Noise) + DRS Scoring
# Target Journal: IEEE Transactions on Information Forensics and Security (TIFS)
# =============================================================================

!pip -q install pandas numpy scipy scikit-learn lightgbm matplotlib seaborn

import os, json
import numpy as np
import pandas as pd
from scipy.stats import entropy
from scipy.spatial.distance import jensenshannon
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import f1_score, roc_auc_score, confusion_matrix
from lightgbm import LGBMClassifier
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = "/content/sentinel_ego_phase4"
OUT_DIR  = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

ARCHETYPE_NAMES = [
    "Morning Bird","Collaborator","Balanced","Workaholic","Night Owl",
    "Tech Savvy","Careful Planner","Lone Wolf","Workaholic_8","Social Butterfly"
]

# ── Load NSL-KDD ───────────────────────────────────────────────────────────────
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
df = pd.read_csv(
    "https://raw.githubusercontent.com/jmnwong/NSL-KDD-Dataset/master/KDDTrain+.csv",
    header=None, names=col_names
)
df["label"] = df["label"].apply(lambda x: 0 if x == "normal" else 1)
df = df.drop(columns=["difficulty"])
for col in df.select_dtypes(include="object").columns:
    df[col] = LabelEncoder().fit_transform(df[col].astype(str))

X_all = StandardScaler().fit_transform(df.drop("label", axis=1).fillna(0))
y_all = df["label"].values
X_tr, X_te, y_tr, y_te = train_test_split(X_all, y_all, test_size=0.2, random_state=42)

# ── Train base federated model ─────────────────────────────────────────────────
base_model = LGBMClassifier(n_estimators=200, random_state=42, verbose=-1)
base_model.fit(X_tr, y_tr)
base_f1  = f1_score(y_te, base_model.predict(X_te), average="weighted")
base_auc = roc_auc_score(y_te, base_model.predict_proba(X_te)[:,1])
print(f"Base federated model: F1={base_f1:.4f}  AUC={base_auc:.4f}")

# ── Mutation strategies ────────────────────────────────────────────────────────
MUTATION_RATE = 0.15

def mutate_evasive(X, rate, rng):
    """Maximize divergence by inverting high-activation features."""
    Xm = X.copy()
    n_mut = int(X.shape[1] * rate)
    top_cols = np.argsort(np.abs(X.mean(axis=0)))[::-1][:n_mut]
    Xm[:, top_cols] *= -1
    return Xm

def mutate_mimicry(X, X_normal, rate, rng):
    """Blend toward normal-traffic distribution."""
    Xm  = X.copy()
    n_mut = int(X.shape[1] * rate)
    cols  = rng.choice(X.shape[1], n_mut, replace=False)
    Xm[:, cols] = Xm[:, cols] * (1 - rate) + X_normal[:len(Xm), cols] * rate
    return Xm

def mutate_noise(X, rate, rng):
    """Add Gaussian noise proportional to feature standard deviation."""
    Xm = X.copy()
    noise = rng.normal(0, rate * np.std(X, axis=0), size=X.shape)
    return Xm + noise

STRATEGIES = ["evasive", "mimicry", "noise"]
N_ROUNDS   = 15
rng        = np.random.RandomState(42)

X_normal   = X_te[y_te == 0]  # Normal traffic reference for mimicry
X_attack   = X_te[y_te == 1].copy()

# ── CDE Evolution loop ─────────────────────────────────────────────────────────
cde_results = []
X_current   = X_attack.copy()

for rnd in range(1, N_ROUNDS + 1):
    strategy = STRATEGIES[(rnd - 1) % 3]

    if strategy == "evasive":
        X_mutated = mutate_evasive(X_current, MUTATION_RATE, rng)
    elif strategy == "mimicry":
        X_mutated = mutate_mimicry(X_current, X_normal, MUTATION_RATE, rng)
    else:
        X_mutated = mutate_noise(X_current, MUTATION_RATE, rng)

    # JSD between original and mutated feature distributions
    jsd_vals = []
    for col in range(X_attack.shape[1]):
        p = np.histogram(X_attack[:,  col], bins=30, density=True)[0] + 1e-9
        q = np.histogram(X_mutated[:, col], bins=30, density=True)[0] + 1e-9
        jsd_vals.append(jensenshannon(p/p.sum(), q/q.sum())**2)
    mean_jsd = float(np.mean(jsd_vals))

    # Detection performance on mutated attack traffic
    X_eval   = np.vstack([X_normal, X_mutated])
    y_eval   = np.concatenate([np.zeros(len(X_normal)), np.ones(len(X_mutated))])
    y_pred   = base_model.predict(X_eval)
    det_f1   = f1_score(y_eval, y_pred, average="weighted")
    det_auc  = roc_auc_score(y_eval, base_model.predict_proba(X_eval)[:,1])

    cde_results.append({
        "round": rnd, "strategy": strategy,
        "jsd_drift": round(mean_jsd, 4),
        "detection_f1": round(det_f1, 4),
        "detection_auc": round(det_auc, 4),
        "mutation_rate": MUTATION_RATE,
    })
    print(f"  Round {rnd:2d} [{strategy:8s}]: JSD={mean_jsd:.4f}  F1={det_f1:.4f}")
    X_current = X_mutated

cde_df = pd.DataFrame(cde_results)

# ── Per-archetype behavioral drift ────────────────────────────────────────────
N_NODES = 10
node_idx = np.array_split(np.arange(len(X_attack)), N_NODES)

drs_results = []
for i, idx in enumerate(node_idx):
    if len(idx) < 5: continue
    Xo = X_attack[idx]
    Xe = X_current[idx]  # After all 15 rounds of evolution

    jsd_v = []
    for col in range(Xo.shape[1]):
        p = np.histogram(Xo[:, col], bins=20, density=True)[0] + 1e-9
        q = np.histogram(Xe[:, col], bins=20, density=True)[0] + 1e-9
        jsd_v.append(jensenshannon(p/p.sum(), q/q.sum())**2)
    jsd_node = float(np.mean(jsd_v))

    # Confusion probability: how often does the detector mis-classify evolved samples
    y_pred_node = base_model.predict(Xe)
    confusion_prob = 1 - f1_score(np.ones(len(Xe)), y_pred_node, average="binary", zero_division=0)

    # Hour-equivalent shift (approximate using feature mean displacement)
    hour_shift = float(np.abs(Xe.mean(axis=0) - Xo.mean(axis=0)).mean() * 24)
    entropy_change = float(
        entropy(np.abs(Xe.mean(axis=0)) + 1e-9) -
        entropy(np.abs(Xo.mean(axis=0)) + 1e-9)
    )

    drs = float(np.clip(0.4 * jsd_node / 0.22 + 0.4 * confusion_prob + 0.2 * jsd_node, 0, 1))

    drs_results.append({
        "archetype":      ARCHETYPE_NAMES[i],
        "jsd_drift":      round(jsd_node, 4),
        "hour_shift":     round(hour_shift, 2),
        "entropy_change": round(entropy_change, 3),
        "confusion_prob": round(confusion_prob, 4),
        "drs_score":      round(drs, 4),
        "tier":           "High" if drs >= 0.75 else "Moderate" if drs >= 0.50 else "Low"
    })

drs_df = pd.DataFrame(drs_results).sort_values("drs_score", ascending=False)
print("\nDetection Resistance Scores:")
print(drs_df.to_string(index=False))
print(f"\nMean DRS: {drs_df['drs_score'].mean():.4f}")

# ── Save outputs ───────────────────────────────────────────────────────────────
cde_df.to_csv(os.path.join(OUT_DIR, "phase4_cde_evolution_rounds.csv"),  index=False)
drs_df.to_csv(os.path.join(OUT_DIR, "phase4_archetype_drs_scores.csv"),  index=False)
print("\nPhase 4 complete. All CSVs saved to:", OUT_DIR)
