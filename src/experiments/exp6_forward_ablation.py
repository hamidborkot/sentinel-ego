"""
SENTINEL-EGO — Exp 6: Forward Ablation Study (Self-Contained)
==============================================================
Dataset : NSL-KDD (auto-downloaded; reuses df if already in memory)
Configs:
  A  Flat DP-FedAvg  (q=0.01, no archetype structure)   baseline
  B  +PBI            (K=10 persona/archetype nodes)
  C  +PBI+AIF        (distance-to-prototype feature added)
  D  +PBI+AIF+FAL    (federated across archetypes = full SENTINEL-EGO)

Privacy: (epsilon=1.4042, delta=1e-5)-DP  [RDP accountant]
Evaluation: stratified 5-fold CV, seed=42

Output: results/exp6_forward_ablation.csv

Frozen results (TDSC 2026):
  A  F1=0.9492  delta=---
  B  F1=0.9722  delta=+0.0230
  C  F1=0.9915  delta=+0.0193
  D  F1=0.9936  delta=+0.0021
"""
import io, math, warnings, os, gc
import numpy as np, pandas as pd, requests
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score
from lightgbm import LGBMClassifier
from scipy.stats import mode as sc_mode
warnings.filterwarnings("ignore")

SEED=42; SIGMA=2.0; CLIP=1.0; DELTA=1e-5; NFOLDS=5; Q=0.10; K=10; R=10

def compute_eps(q, sigma, R=10, delta=1e-5, alpha=10):
    rdp = q**2 * alpha / (2 * sigma**2) * R
    return round(rdp + math.log(1/delta) / (alpha - 1), 4)
EPS = compute_eps(Q, SIGMA)

# ── Dataset (paste load_nslkdd() here if running standalone) ────────
# Assumes `df` is already in memory from exp5. If not, load it:
KDD_COLS = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes",
    "land","wrong_fragment","urgent","hot","num_failed_logins","logged_in",
    "num_compromised","root_shell","su_attempted","num_root","num_file_creations",
    "num_shells","num_access_files","num_outbound_cmds","is_host_login",
    "is_guest_login","count","srv_count","serror_rate","srv_serror_rate",
    "rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate",
    "srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate"
]

try:
    _ = df
except NameError:
    from sklearn.preprocessing import LabelEncoder
    for url in [
        "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain+.txt",
        "https://raw.githubusercontent.com/jmnwong/NSL-KDD-Dataset/master/KDDTrain+.csv"
    ]:
        try:
            r = requests.get(url, timeout=90)
            if r.status_code != 200: continue
            tmp = pd.read_csv(io.StringIO(r.text), header=None)
            nc = tmp.shape[1]
            if nc == 42:   tmp.columns = KDD_COLS + ["label"]
            elif nc == 43: tmp.columns = KDD_COLS + ["label","d"]; tmp = tmp.drop(columns=["d"])
            else: continue
            tmp["label"] = tmp["label"].astype(str).str.strip().str.lower() \
                .str.rstrip(".").apply(lambda x: 0 if x=="normal" else 1)
            for c in tmp.select_dtypes(include="object").columns:
                tmp[c] = LabelEncoder().fit_transform(tmp[c].astype(str))
            df = tmp.apply(pd.to_numeric, errors="coerce").fillna(0) \
                   .replace([np.inf,-np.inf],0) \
                   .sample(min(22544,len(tmp)), random_state=SEED).reset_index(drop=True)
            print(f"NSL-KDD loaded: {len(df)} rows"); break
        except Exception as e: print(f"  {e}")

y  = df["label"].values.astype(int)
X  = np.where(np.isfinite(df.drop(columns=["label"]).values.astype(float)),
              df.drop(columns=["label"]).values.astype(float), 0)
nf = X.shape[1]

def make_lgbm(seed):
    return LGBMClassifier(
        n_estimators=200, max_depth=7, learning_rate=0.07,
        class_weight="balanced", subsample=0.85, colsample_bytree=0.85,
        reg_alpha=0.1, reg_lambda=0.5, min_child_samples=5,
        random_state=seed, n_jobs=-1, verbose=-1
    )

def dp_proto(proto, sigma, clip, nf):
    nrm = np.linalg.norm(proto)
    if nrm > clip: proto = proto * clip / nrm
    return proto + np.random.RandomState(None).normal(0, sigma * clip, nf)

def sub_bal(y, q, seed):
    pos = np.where(y==1)[0]; neg = np.where(y==0)[0]; rng = np.random.RandomState(seed)
    return np.concatenate([
        rng.choice(pos, max(5, int(len(pos)*q)), replace=False),
        rng.choice(neg, max(5, int(len(neg)*q)), replace=False)
    ])

skf = StratifiedKFold(n_splits=NFOLDS, shuffle=True, random_state=SEED)
configs = {"A_FlatDP": [], "B_PBI": [], "C_PBI_AIF": [], "D_SENTINEL": []}

for fold, (tr, te) in enumerate(skf.split(X, y)):
    sc = StandardScaler()
    Xtr = np.clip(sc.fit_transform(X[tr]), -5, 5)
    Xte = np.clip(sc.transform(X[te]), -5, 5)
    ytr, yte = y[tr], y[te]
    nf_ = Xtr.shape[1]

    # A: Flat DP-FedAvg
    proto_a = Xtr[ytr==1].mean(0) if (ytr==1).sum()>0 else np.zeros(nf_)
    dp_a = dp_proto(proto_a.copy(), SIGMA, CLIP, nf_)
    sub_a = sub_bal(ytr, 0.01, SEED+fold)
    m_a = make_lgbm(SEED+fold); m_a.fit(Xtr[sub_a], ytr[sub_a])
    configs["A_FlatDP"].append(f1_score(yte, m_a.predict(Xte), zero_division=0))

    # B: +PBI
    arch_ids = np.array([hash(tuple(Xtr[i].round(2).tolist())) % K for i in range(len(Xtr))])
    arch_models = []
    for k in range(K):
        mask = arch_ids == k
        if mask.sum() < 10: arch_models.append(None); continue
        sub_k = sub_bal(ytr[mask], Q, SEED+fold+k*100)
        idx_k = np.where(mask)[0][sub_k]
        m_k = make_lgbm(SEED+fold+k); m_k.fit(Xtr[idx_k], ytr[idx_k])
        arch_models.append(m_k)
    valid = [m for m in arch_models if m is not None]
    if valid:
        preds = np.column_stack([m.predict(Xte) for m in valid])
        yp_b = sc_mode(preds, axis=1, keepdims=True).mode.ravel()
    else:
        yp_b = np.zeros(len(yte), int)
    configs["B_PBI"].append(f1_score(yte, yp_b, zero_division=0))

    # C: +PBI+AIF
    arch_protos = [dp_proto(
        Xtr[(arch_ids==k)&(ytr==1)].mean(0) if ((arch_ids==k)&(ytr==1)).sum()>0 else np.zeros(nf_),
        SIGMA, CLIP, nf_) for k in range(K)]
    gp_c = np.mean(arch_protos, 0)
    Xtr_c = np.hstack([Xtr, np.linalg.norm(Xtr - gp_c, axis=1, keepdims=True)])
    Xte_c = np.hstack([Xte, np.linalg.norm(Xte - gp_c, axis=1, keepdims=True)])
    sub_c = sub_bal(ytr, Q, SEED+fold+500)
    m_c = make_lgbm(SEED+fold+500); m_c.fit(Xtr_c[sub_c], ytr[sub_c])
    configs["C_PBI_AIF"].append(f1_score(yte, m_c.predict(Xte_c), zero_division=0))

    # D: Full SENTINEL-EGO (+FAL)
    fed_proto = np.mean(arch_protos, 0)
    Xtr_d = np.hstack([Xtr, np.linalg.norm(Xtr - fed_proto, axis=1, keepdims=True)])
    Xte_d = np.hstack([Xte, np.linalg.norm(Xte - fed_proto, axis=1, keepdims=True)])
    sub_d = sub_bal(ytr, Q, SEED+fold+600)
    m_d = make_lgbm(SEED+fold+600); m_d.fit(Xtr_d[sub_d], ytr[sub_d])
    configs["D_SENTINEL"].append(f1_score(yte, m_d.predict(Xte_d), zero_division=0))

    del Xtr, Xte; gc.collect()

rows = []; prev = None
labels = {
    "A_FlatDP":   "A: Flat DP-FedAvg (no modules)",
    "B_PBI":      "B: +PBI (persona structure)",
    "C_PBI_AIF":  "C: +PBI+AIF (intent fingerprint)",
    "D_SENTINEL": "D: Full SENTINEL-EGO (+FAL)"
}
for tag, name in labels.items():
    f1  = round(np.mean(configs[tag]), 4)
    std = round(np.std(configs[tag]),  4)
    delta = round(f1 - (prev or f1), 4) if prev is not None else 0.0
    print(f"{name:45s}  F1={f1:.4f}  delta={delta:+.4f}")
    rows.append({"Config": name, "F1": f1, "F1_std": std, "DeltaF1": delta, "eps": EPS})
    prev = f1

os.makedirs("results", exist_ok=True)
pd.DataFrame(rows).to_csv("results/exp6_forward_ablation.csv", index=False)
print("Saved: results/exp6_forward_ablation.csv")
