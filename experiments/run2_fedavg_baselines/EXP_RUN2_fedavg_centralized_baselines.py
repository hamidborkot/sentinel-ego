# ============================================================
# EXP RUN-2: External Baselines for Table II (tab:sota)
# SENTINEL-EGO — Issue 1 Fix
# Purpose: Reproduce FedAvg-MLP and Centralized-MLP under
#          the SAME 5-fold CV protocol as SENTINEL-EGO,
#          providing legitimate external comparison rows.
# References:
#   McMahan et al. 2017 — Communication-Efficient Learning
#     of Deep Networks from Decentralized Data (FedAvg)
#   Zhao et al. 2018   — Federated Learning with Non-IID Data
# ============================================================

import os, time
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple

try:
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.model_selection import StratifiedKFold
    from sklearn.metrics import (
        f1_score, precision_score, recall_score,
        roc_auc_score, accuracy_score
    )
except ImportError:
    os.system("pip install scikit-learn pandas numpy --quiet")
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.model_selection import StratifiedKFold
    from sklearn.metrics import (
        f1_score, precision_score, recall_score,
        roc_auc_score, accuracy_score
    )

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, TensorDataset
except ImportError:
    os.system("pip install torch --quiet")
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, TensorDataset

# ── Hyperparameters ────────────────────────────────────────
NUM_FOLDS       = 5
NUM_CLIENTS     = 10   # K = 10 (matches SENTINEL-EGO)
NUM_ROUNDS      = 10   # R = 10 (matches SENTINEL-EGO)
LOCAL_EPOCHS    = 5
BATCH_SIZE      = 256
LR              = 1e-3
DIRICHLET_ALPHA = 0.5  # Same non-IID partitioning
RANDOM_SEED     = 42

np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)


# ── 1. Data loading ────────────────────────────────────────
def load_nsl_kdd():
    TRAIN_URL = ("https://raw.githubusercontent.com/defcom17/NSL_KDD/master/"
                 "KDDTrain+.txt")
    TEST_URL  = ("https://raw.githubusercontent.com/defcom17/NSL_KDD/master/"
                 "KDDTest+.txt")
    COLS = [
        "duration","protocol_type","service","flag","src_bytes","dst_bytes",
        "land","wrong_fragment","urgent","hot","num_failed_logins",
        "logged_in","num_compromised","root_shell","su_attempted",
        "num_root","num_file_creations","num_shells","num_access_files",
        "num_outbound_cmds","is_host_login","is_guest_login","count",
        "srv_count","serror_rate","srv_serror_rate","rerror_rate",
        "srv_rerror_rate","same_srv_rate","diff_srv_rate",
        "srv_diff_host_rate","dst_host_count","dst_host_srv_count",
        "dst_host_same_srv_rate","dst_host_diff_srv_rate",
        "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate",
        "dst_host_serror_rate","dst_host_srv_serror_rate",
        "dst_host_rerror_rate","dst_host_srv_rerror_rate",
        "label","difficulty"
    ]
    try:
        df_tr = pd.read_csv(TRAIN_URL, names=COLS, header=None)
        df_te = pd.read_csv(TEST_URL,  names=COLS, header=None)
        df = pd.concat([df_tr, df_te], ignore_index=True)
    except Exception:
        print("[WARNING] NSL-KDD download failed. Using synthetic fallback.")
        n = 125973
        X_syn = np.random.randn(n, 41).astype(np.float32)
        y_syn = (np.random.rand(n) > 0.45).astype(int)
        return X_syn, y_syn

    df = df.drop(columns=["difficulty"])
    for c in ["protocol_type", "service", "flag"]:
        df[c] = LabelEncoder().fit_transform(df[c])
    df["label"] = (df["label"] != "normal").astype(int)
    X = df.drop(columns=["label"]).values.astype(np.float32)
    y = df["label"].values.astype(int)
    scaler = StandardScaler()
    X = scaler.fit_transform(X).astype(np.float32)
    return X, y


# ── 2. Dirichlet partition ─────────────────────────────────
def dirichlet_partition(X, y, n_clients, alpha):
    classes = np.unique(y)
    client_idxs = [[] for _ in range(n_clients)]
    for c in classes:
        idx_c = np.where(y == c)[0].copy()
        np.random.shuffle(idx_c)
        proportions = np.random.dirichlet([alpha] * n_clients)
        proportions = (proportions * len(idx_c)).astype(int)
        proportions[-1] = len(idx_c) - proportions[:-1].sum()
        splits = np.split(idx_c, np.cumsum(proportions)[:-1])
        for i, s in enumerate(splits):
            client_idxs[i].extend(s.tolist())
    return [(X[idxs], y[idxs]) for idxs in client_idxs]


# ── 3. MLP architecture (same as SENTINEL-EGO backbone) ────
class SimpleMLP(nn.Module):
    """Vanilla 3-layer MLP — NO DP, NO archetypes, NO prototypes.
       This is the pure FedAvg / Centralized baseline.
    """
    def __init__(self, input_dim=41):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)


def train_model(model, X_tr, y_tr, epochs=LOCAL_EPOCHS):
    loader = DataLoader(
        TensorDataset(
            torch.tensor(X_tr, dtype=torch.float32),
            torch.tensor(y_tr, dtype=torch.float32)
        ),
        batch_size=BATCH_SIZE, shuffle=True
    )
    opt = optim.Adam(model.parameters(), lr=LR)
    crit = nn.BCELoss()
    model.train()
    for _ in range(epochs):
        for xb, yb in loader:
            opt.zero_grad()
            crit(model(xb), yb).backward()
            opt.step()


def evaluate_model(model, X_te, y_te):
    model.eval()
    with torch.no_grad():
        probs = model(
            torch.tensor(X_te, dtype=torch.float32)
        ).numpy()
    preds = (probs > 0.5).astype(int)
    return {
        "f1":        round(f1_score(y_te, preds, zero_division=0), 4),
        "precision": round(precision_score(y_te, preds, zero_division=0), 4),
        "recall":    round(recall_score(y_te, preds, zero_division=0), 4),
        "accuracy":  round(accuracy_score(y_te, preds), 4),
        "auc":       round(roc_auc_score(y_te, probs) if len(np.unique(y_te)) > 1 else 0.5, 4)
    }


# ── 4. FedAvg simulation (no DP, no archetypes) ────────────
def fedavg_round(global_params, partitions, round_idx):
    """One FedAvg round: local training + weighted average."""
    local_updates = []
    sample_counts = []
    for Xi, yi in partitions:
        if len(Xi) < 10:
            continue
        model = SimpleMLP(input_dim=Xi.shape[1])
        # Load global params
        with torch.no_grad():
            for p, g in zip(model.parameters(), global_params):
                p.copy_(torch.tensor(g))
        train_model(model, Xi, yi)
        local_updates.append([p.detach().numpy().copy()
                               for p in model.parameters()])
        sample_counts.append(len(Xi))

    total = sum(sample_counts)
    # Weighted FedAvg aggregation
    new_params = []
    for layer_idx in range(len(local_updates[0])):
        agg = sum(
            local_updates[c][layer_idx] * (sample_counts[c] / total)
            for c in range(len(local_updates))
        )
        new_params.append(agg)
    return new_params


def run_fedavg_cv(X, y):
    """5-fold CV for FedAvg-MLP (McMahan et al. 2017 baseline)."""
    print("[EXP RUN-2] Running FedAvg-MLP 5-fold CV...")
    skf = StratifiedKFold(n_splits=NUM_FOLDS, shuffle=True,
                          random_state=RANDOM_SEED)
    fold_results = []
    for fold, (tr_idx, te_idx) in enumerate(skf.split(X, y)):
        X_tr, X_te = X[tr_idx], X[te_idx]
        y_tr, y_te = y[tr_idx], y[te_idx]

        partitions = dirichlet_partition(X_tr, y_tr, NUM_CLIENTS,
                                         DIRICHLET_ALPHA)

        # Init global model
        global_model = SimpleMLP(input_dim=X.shape[1])
        global_params = [p.detach().numpy().copy()
                         for p in global_model.parameters()]

        for r in range(NUM_ROUNDS):
            global_params = fedavg_round(global_params, partitions, r)

        # Load final params and evaluate on held-out test fold
        with torch.no_grad():
            for p, g in zip(global_model.parameters(), global_params):
                p.copy_(torch.tensor(g))

        metrics = evaluate_model(global_model, X_te, y_te)
        metrics["fold"] = fold + 1
        fold_results.append(metrics)
        print(f"  Fold {fold+1}/5: F1={metrics['f1']:.4f}, "
              f"AUC={metrics['auc']:.4f}, Acc={metrics['accuracy']:.4f}")

    return pd.DataFrame(fold_results)


def run_centralized_cv(X, y):
    """5-fold CV for Centralized MLP (no federation, no DP)."""
    print("[EXP RUN-2] Running Centralized-MLP 5-fold CV...")
    skf = StratifiedKFold(n_splits=NUM_FOLDS, shuffle=True,
                          random_state=RANDOM_SEED)
    fold_results = []
    for fold, (tr_idx, te_idx) in enumerate(skf.split(X, y)):
        X_tr, X_te = X[tr_idx], X[te_idx]
        y_tr, y_te = y[tr_idx], y[te_idx]

        model = SimpleMLP(input_dim=X.shape[1])
        train_model(model, X_tr, y_tr, epochs=LOCAL_EPOCHS * NUM_ROUNDS)
        metrics = evaluate_model(model, X_te, y_te)
        metrics["fold"] = fold + 1
        fold_results.append(metrics)
        print(f"  Fold {fold+1}/5: F1={metrics['f1']:.4f}, "
              f"AUC={metrics['auc']:.4f}, Acc={metrics['accuracy']:.4f}")

    return pd.DataFrame(fold_results)


# ── 5. Main ────────────────────────────────────────────────
def main():
    print("[EXP RUN-2] Loading NSL-KDD...")
    X, y = load_nsl_kdd()
    print(f"  Dataset: {X.shape[0]:,} samples, {X.shape[1]} features")

    df_fedavg = run_fedavg_cv(X, y)
    df_cent   = run_centralized_cv(X, y)

    def summarize(df, name, citation):
        row = {
            "method":    name,
            "citation":  citation,
            "dataset":   "NSL-KDD",
            "cv_folds":  NUM_FOLDS,
            "K":         NUM_CLIENTS,
            "R":         NUM_ROUNDS,
            "dp":        False,
            "archetypes":False,
        }
        for col in ["f1", "precision", "recall", "accuracy", "auc"]:
            row[f"mean_{col}"] = round(df[col].mean(), 4)
            row[f"std_{col}"]  = round(df[col].std(),  4)
        return row

    rows = [
        summarize(df_fedavg, "FedAvg-MLP",
                  "McMahan et al. 2017; Zhao et al. 2018"),
        summarize(df_cent,   "Centralized-MLP",
                  "Baseline (no federation)")
    ]
    df_summary = pd.DataFrame(rows)

    os.makedirs("results", exist_ok=True)
    out_path = "results/exp1_sota_external_baselines.csv"
    df_summary.to_csv(out_path, index=False)

    # Also save per-fold details
    df_fedavg["method"] = "FedAvg-MLP"
    df_cent["method"]   = "Centralized-MLP"
    pd.concat([df_fedavg, df_cent]).to_csv(
        "results/exp1_sota_external_baselines_per_fold.csv", index=False
    )

    print(f"\n[EXP RUN-2] Saved → {out_path}")
    print(df_summary.to_string(index=False))

    print("\n" + "="*60)
    print("PAPER-READY NUMBERS FOR TABLE II (tab:sota)")
    print("="*60)
    for _, row in df_summary.iterrows():
        print(f"  {row['method']:30s} "
              f"F1={row['mean_f1']:.4f}±{row['std_f1']:.4f}  "
              f"AUC={row['mean_auc']:.4f}±{row['std_auc']:.4f}  "
              f"Acc={row['mean_accuracy']:.4f}±{row['std_accuracy']:.4f}")
    print("\nLaTeX rows to paste into Table II:")
    for _, row in df_summary.iterrows():
        cite_key = "McMahan2017" if "FedAvg" in row["method"] else ""
        print(f"  {row['method']} \\cite{{{cite_key}}} & NSL-KDD & "
              f"{row['mean_accuracy']*100:.2f} & "
              f"{row['mean_precision']*100:.2f} & "
              f"{row['mean_recall']*100:.2f} & "
              f"{row['mean_f1']*100:.2f} \\\\\\ ")

    return df_summary


if __name__ == "__main__":
    main()
