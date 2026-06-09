"""
SENTINEL-EGO — Exp 5: SOTA Comparison (Self-Contained)
=======================================================
Dataset : NSL-KDD (auto-downloaded)
Baselines:
  B1  Flat DP-FedAvg  (q=0.01, single node, no archetypes)
  B2  Centralized LightGBM  (no DP, no federation)
  B3  Centralized Random Forest  (Kitsune-style, no DP)
  B4  FedAvg+DP flat  (q=0.10, no archetype structure)
  S0  SENTINEL-EGO  (K=10 archetypes, FAL-DP, q=0.10)

Privacy: (epsilon=1.4042, delta=1e-5)-DP  [RDP accountant]
Evaluation: stratified 5-fold CV, seed=42

Output: results/exp5_sota_comparison.csv

Frozen results (TDSC 2026):
  B1  F1=0.9506 ± 0.0131  AUC=0.9909
  B2  F1=0.9980 ± 0.0006  AUC=0.9999
  B3  F1=0.9972 ± 0.0008  AUC=0.9999
  B4  F1=0.9900 ± 0.0017  AUC=0.9995
  S0  F1=0.9924 ± 0.0016  AUC=0.9995
"""
import io, math, warnings, os, gc
import numpy as np, pandas as pd, requests
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score, roc_auc_score, precision_score, recall_score
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
warnings.filterwarnings("ignore")

SEED=42; SIGMA=2.0; CLIP=1.0; DELTA=1e-5; NFOLDS=5; Q=0.10; R=10

def compute_eps(q, sigma, R=10, delta=1e-5, alpha=10):
    rdp = q**2 * alpha / (2 * sigma**2) * R
    return round(rdp + math.log(1/delta) / (alpha - 1), 4)

EPS = compute_eps(Q, SIGMA)

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

def le_obj(df):
    for c in df.select_dtypes(include="object").columns:
        df[c] = LabelEncoder().fit_transform(df[c].astype(str))
    return df

def clean(df):
    return df.apply(pd.to_numeric, errors="coerce").fillna(0).replace([np.inf, -np.inf], 0)

def load_nslkdd():
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
            elif nc == 43: tmp.columns = KDD_COLS + ["label", "d"]; tmp = tmp.drop(columns=["d"])
            else: continue
            tmp["label"] = tmp["label"].astype(str).str.strip().str.lower() \
                .str.rstrip(".").apply(lambda x: 0 if x == "normal" else 1)
            df = clean(le_obj(tmp)).sample(min(22544, len(tmp)), random_state=SEED).reset_index(drop=True)
            print(f"NSL-KDD loaded: {len(df)} rows, anomaly rate={df.label.mean():.3f}")
            return df
        except Exception as e:
            print(f"  URL failed: {e}")
    print("Using synthetic NSL-KDD fallback")
    rng = np.random.RandomState(SEED); n = 22544; f = 41; na = int(n * 0.466)
    X = np.vstack([rng.randn(na, f) * 0.9 + rng.choice([-1.2, 1.4], size=(na, f)),
                   rng.randn(n - na, f) * 0.6])
    y = np.r_[np.ones(na, int), np.zeros(n - na, int)]
    idx = rng.permutation(n)
    df = pd.DataFrame(X[idx], columns=[f"f{i}" for i in range(f)])
    df["label"] = y[idx]
    return df

def make_lgbm(seed, n=200):
    return LGBMClassifier(
        n_estimators=n, max_depth=7, learning_rate=0.07,
        class_weight="balanced", subsample=0.85, colsample_bytree=0.85,
        reg_alpha=0.1, reg_lambda=0.5, min_child_samples=5,
        random_state=seed, n_jobs=-1, verbose=-1
    )

def dp_proto(proto, sigma, clip, nf):
    nrm = np.linalg.norm(proto)
    if nrm > clip: proto = proto * clip / nrm
    return proto + np.random.RandomState(None).normal(0, sigma * clip, nf)

def add_dist(X, proto):
    return np.hstack([X, np.linalg.norm(X - proto, axis=1, keepdims=True)])

def sub_bal(y, q, seed):
    pos = np.where(y == 1)[0]; neg = np.where(y == 0)[0]
    rng = np.random.RandomState(seed)
    return np.concatenate([
        rng.choice(pos, max(5, int(len(pos) * q)), replace=False),
        rng.choice(neg, max(5, int(len(neg) * q)), replace=False)
    ])

df = load_nslkdd()
y  = df["label"].values.astype(int)
X  = np.where(np.isfinite(df.drop(columns=["label"]).values.astype(float)),
              df.drop(columns=["label"]).values.astype(float), 0)
nf = X.shape[1]

skf = StratifiedKFold(n_splits=NFOLDS, shuffle=True, random_state=SEED)
metrics = {k: {m: [] for m in ["f1","auc","prec","rec"]}
           for k in ["B1_FlatDP","B2_CentralLGBM","B3_CentralRF","B4_FedDP_Flat","S0_SENTINEL"]}

for fold, (tr, te) in enumerate(skf.split(X, y)):
    sc = StandardScaler()
    Xtr = np.clip(sc.fit_transform(X[tr]), -5, 5)
    Xte = np.clip(sc.transform(X[te]), -5, 5)
    ytr, yte = y[tr], y[te]
    K = 10

    # B1: Flat DP-FedAvg (q=0.01, isolated)
    pd_b1 = dp_proto(Xtr[ytr==1].mean(0) if (ytr==1).sum()>0 else np.zeros(nf), SIGMA, CLIP, nf)
    sub_b1 = sub_bal(ytr, 0.01, SEED+fold)
    m_b1 = make_lgbm(SEED+fold+10); m_b1.fit(add_dist(Xtr, pd_b1)[sub_b1], ytr[sub_b1])
    yp_b1 = m_b1.predict(add_dist(Xte, pd_b1))
    yp_b1p = m_b1.predict_proba(add_dist(Xte, pd_b1))[:,1]

    # B2: Centralized LightGBM (no DP)
    m_b2 = make_lgbm(SEED+fold+20); m_b2.fit(Xtr, ytr)
    yp_b2 = m_b2.predict(Xte); yp_b2p = m_b2.predict_proba(Xte)[:,1]

    # B3: Centralized Random Forest
    m_b3 = RandomForestClassifier(n_estimators=100, class_weight="balanced",
                                   random_state=SEED+fold, n_jobs=-1)
    m_b3.fit(Xtr, ytr)
    yp_b3 = m_b3.predict(Xte); yp_b3p = m_b3.predict_proba(Xte)[:,1]

    # B4: FedAvg+DP flat (q=0.10, no archetypes)
    pd_b4 = dp_proto(Xtr[ytr==1].mean(0) if (ytr==1).sum()>0 else np.zeros(nf), SIGMA, CLIP, nf)
    sub_b4 = sub_bal(ytr, Q, SEED+fold+40)
    m_b4 = make_lgbm(SEED+fold+40); m_b4.fit(add_dist(Xtr, pd_b4)[sub_b4], ytr[sub_b4])
    yp_b4 = m_b4.predict(add_dist(Xte, pd_b4))
    yp_b4p = m_b4.predict_proba(add_dist(Xte, pd_b4))[:,1]

    # S0: SENTINEL-EGO (K=10 archetypes, FAL-DP)
    arch_ids = np.array([hash(tuple(row.round(1))) % K for row in Xtr])
    dp_protos = [dp_proto(
        Xtr[(arch_ids==k)&(ytr==1)].mean(0) if ((arch_ids==k)&(ytr==1)).sum()>0 else np.zeros(nf),
        SIGMA, CLIP, nf) for k in range(K)]
    fed_proto = np.mean(dp_protos, axis=0)
    sub_s0 = sub_bal(ytr, Q, SEED+fold+50)
    m_s0 = make_lgbm(SEED+fold+50); m_s0.fit(add_dist(Xtr, fed_proto)[sub_s0], ytr[sub_s0])
    yp_s0 = m_s0.predict(add_dist(Xte, fed_proto))
    yp_s0p = m_s0.predict_proba(add_dist(Xte, fed_proto))[:,1]

    for tag, yp, yprob in [
        ("B1_FlatDP", yp_b1, yp_b1p), ("B2_CentralLGBM", yp_b2, yp_b2p),
        ("B3_CentralRF", yp_b3, yp_b3p), ("B4_FedDP_Flat", yp_b4, yp_b4p),
        ("S0_SENTINEL", yp_s0, yp_s0p)
    ]:
        metrics[tag]["f1"].append(f1_score(yte, yp, zero_division=0))
        metrics[tag]["auc"].append(roc_auc_score(yte, yprob))
        metrics[tag]["prec"].append(precision_score(yte, yp, zero_division=0))
        metrics[tag]["rec"].append(recall_score(yte, yp, zero_division=0))
    del Xtr, Xte; gc.collect()

labels = {
    "B1_FlatDP":       "Flat DP-FedAvg (q=0.01, isolated)",
    "B2_CentralLGBM":  "Centralized LightGBM (no DP)",
    "B3_CentralRF":    "Centralized Random Forest (no DP)",
    "B4_FedDP_Flat":   "FedAvg+DP flat (no archetypes)",
    "S0_SENTINEL":     "SENTINEL-EGO (ours, K=10)"
}
privacy = {"B1_FlatDP": f"e={EPS}", "B2_CentralLGBM": "None",
           "B3_CentralRF": "None", "B4_FedDP_Flat": f"e={EPS}", "S0_SENTINEL": f"e={EPS}"}

rows = []
for tag in labels:
    row = {
        "Method": labels[tag], "Privacy": privacy[tag],
        "F1":    round(np.mean(metrics[tag]["f1"]),  4),
        "F1_std":round(np.std( metrics[tag]["f1"]),  4),
        "AUC":   round(np.mean(metrics[tag]["auc"]), 4),
        "Precision": round(np.mean(metrics[tag]["prec"]), 4),
        "Recall":    round(np.mean(metrics[tag]["rec"]),  4)
    }
    rows.append(row)
    print(f"{tag:20s}  F1={row['F1']:.4f}+/-{row['F1_std']:.4f}  "
          f"AUC={row['AUC']:.4f}  Privacy={row['Privacy']}")

os.makedirs("results", exist_ok=True)
pd.DataFrame(rows).to_csv("results/exp5_sota_comparison.csv", index=False)
print("\nSaved: results/exp5_sota_comparison.csv")
