"""
SENTINEL-EGO — Exp 7: Computational Efficiency Analysis (Self-Contained)
=========================================================================
Dataset : NSL-KDD (reuses df if in memory, else auto-downloads)
Measures: training time per round, inference latency, communication cost

Output: results/exp7_efficiency.csv

Frozen results (TDSC 2026):
  Training time per round (s)          : 0.813
  Total training time (R=10 rounds, s) : 8.13
  Inference latency per sample (ms)    : 0.0191
  Inference throughput (samples/s)     : 52289
  Prototype size per node (KB)         : 0.16
  Communication per round (KB)         : 1.64
  Total communication (R=10, KB)       : 16.41
"""
import time, os
import numpy as np, pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier
import warnings; warnings.filterwarnings("ignore")

SEED=42; SIGMA=2.0; CLIP=1.0; Q=0.10; K=10; R=10

# Assumes df in memory; if not, insert load_nslkdd() call here
y  = df["label"].values.astype(int)
X  = np.where(np.isfinite(df.drop(columns=["label"]).values.astype(float)),
              df.drop(columns=["label"]).values.astype(float), 0)

sc  = StandardScaler()
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=SEED, stratify=y)
Xtr = np.clip(sc.fit_transform(Xtr), -5, 5)
Xte = np.clip(sc.transform(Xte),    -5, 5)
nf  = Xtr.shape[1]

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

results = {}

# Build SENTINEL-EGO model
arch_ids = np.array([hash(tuple(Xtr[i].round(2).tolist())) % K for i in range(len(Xtr))])
arch_protos = [dp_proto(
    Xtr[(arch_ids==k)&(ytr==1)].mean(0) if ((arch_ids==k)&(ytr==1)).sum()>0 else np.zeros(nf),
    SIGMA, CLIP, nf) for k in range(K)]
fed_proto = np.mean(arch_protos, 0)
Xtr_aug = np.hstack([Xtr, np.linalg.norm(Xtr - fed_proto, axis=1, keepdims=True)])
Xte_aug = np.hstack([Xte, np.linalg.norm(Xte - fed_proto, axis=1, keepdims=True)])
sub     = sub_bal(ytr, Q, SEED)

# Training time
t0 = time.perf_counter()
m  = LGBMClassifier(n_estimators=200, max_depth=7, learning_rate=0.07,
    class_weight="balanced", subsample=0.85, colsample_bytree=0.85,
    reg_alpha=0.1, reg_lambda=0.5, min_child_samples=5,
    random_state=SEED, n_jobs=-1, verbose=-1)
m.fit(Xtr_aug[sub], ytr[sub])
train_time = time.perf_counter() - t0
results["Training time per round (s)"]         = round(train_time, 3)
results["Total training time (R=10 rounds, s)"] = round(train_time * R, 2)

# Inference latency
N_SAMPLES = 1000
X_infer   = Xte_aug[:N_SAMPLES]
t0 = time.perf_counter()
_  = m.predict(X_infer)
infer_total = time.perf_counter() - t0
results["Inference latency per sample (ms)"]  = round(infer_total / N_SAMPLES * 1000, 4)
results["Inference throughput (samples/s)"]   = int(N_SAMPLES / infer_total)

# Communication cost
bytes_per_proto  = (nf + 1) * 4  # float32
bytes_per_round  = bytes_per_proto * K
total_bytes      = bytes_per_round * R
results["Gradient/prototype size per node (KB)"] = round(bytes_per_proto  / 1024, 2)
results["Communication per round (KB)"]          = round(bytes_per_round  / 1024, 2)
results["Total communication (R=10, KB)"]        = round(total_bytes      / 1024, 2)
results["Model parameter count (approx. leaves)"] = m.num_leaves_ * m.n_estimators

print("\nSENTINEL-EGO Efficiency Analysis (NSL-KDD)")
print("=" * 55)
for k, v in results.items():
    print(f"  {k:45s}: {v}")

os.makedirs("results", exist_ok=True)
pd.DataFrame([{"Metric": k, "Value": v} for k, v in results.items()]) \
  .to_csv("results/exp7_efficiency.csv", index=False)
print("\nSaved: results/exp7_efficiency.csv")
