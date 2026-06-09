"""
SENTINEL-EGO — Exp 8: BTT Dual Adversary Evaluation (Self-Contained)
======================================================================
Applies the Behavioral Turing Test to all 10 archetypes using:
  - Decision-stump adversary  (depth=1, max_features=2)
  - MLP surrogate adversary   (hidden_layer_sizes=(64,32))
900 synthetic profile-days per archetype, seed=42.

Threshold: F >= 0.80 => PASS (both adversaries)
           F >= 0.80 on stump only => PARTIAL

Output: results/exp8_btt_dual_adversary.csv

Frozen results (TDSC 2026):
  Archetype          Stump   MLP    Verdict
  Careful_Planner    0.8227  0.8944  PASS
  Social_Butterfly   0.8965  0.9900  PASS
  Lone_Wolf          0.8712  0.9271  PASS
  Night_Owl          0.8784  1.0000  PASS
  Collaborator       0.8420  0.8801  PASS
  Info_Seeker        0.9600  1.0000  PASS
  Data_Handler       0.9377  0.7259  PARTIAL
  System_Admin       0.8011  0.9934  PASS
  External_Comm      0.9141  0.8672  PASS
  Multi_Tasker       0.9389  0.9164  PASS
  Mean Stump: 88.6%   Mean MLP: 91.9%   Full PASS: 9/10
"""
import os, warnings
import numpy as np, pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
warnings.filterwarnings("ignore")

SEED = 42; N_DAYS = 900; THRESHOLD = 0.80

ARCHETYPES = [
    ("Careful_Planner",   {"mean": [0.3,0.2,0.1,0.4,0.5], "std": [0.05,0.05,0.03,0.06,0.04]}),
    ("Social_Butterfly",  {"mean": [0.7,0.8,0.6,0.3,0.2], "std": [0.12,0.10,0.11,0.08,0.07]}),
    ("Lone_Wolf",         {"mean": [0.2,0.1,0.05,0.15,0.3],"std": [0.04,0.03,0.02,0.04,0.05]}),
    ("Night_Owl",         {"mean": [0.1,0.3,0.9,0.2,0.1], "std": [0.03,0.05,0.04,0.04,0.03]}),
    ("Collaborator",      {"mean": [0.6,0.7,0.5,0.6,0.5], "std": [0.10,0.09,0.08,0.09,0.08]}),
    ("Info_Seeker",       {"mean": [0.4,0.2,0.3,0.8,0.7], "std": [0.03,0.03,0.03,0.03,0.03]}),
    ("Data_Handler",      {"mean": [0.5,0.6,0.4,0.5,0.6], "std": [0.02,0.02,0.02,0.02,0.02]}),
    ("System_Admin",      {"mean": [0.8,0.3,0.7,0.4,0.9], "std": [0.15,0.10,0.12,0.09,0.14]}),
    ("External_Comm",     {"mean": [0.3,0.9,0.4,0.6,0.2], "std": [0.08,0.06,0.07,0.09,0.06]}),
    ("Multi_Tasker",      {"mean": [0.6,0.5,0.6,0.5,0.7], "std": [0.11,0.10,0.09,0.10,0.11]}),
]

def gen_benign(params, n, seed):
    rng = np.random.RandomState(seed)
    return rng.normal(params["mean"], params["std"], size=(n, len(params["mean"])))

def gen_threat(params, n, seed, jsd_tau=0.25):
    rng = np.random.RandomState(seed + 1000)
    X = rng.normal(params["mean"], params["std"], size=(n, len(params["mean"])))
    # Evasive perturbation: shift within JSD budget tau
    perturb = rng.uniform(-jsd_tau, jsd_tau, size=X.shape) * np.array(params["std"])
    return np.clip(X + perturb, 0, 1)

print("=" * 65)
print("SENTINEL-EGO — Exp 8: BTT Dual Adversary Evaluation")
print("=" * 65)
print(f"{'Archetype':22s}  {'Stump Fool':>10s}  {'MLP Fool':>8s}  Verdict")
print("-" * 65)

rows = []
for name, params in ARCHETYPES:
    Xb = gen_benign(params, N_DAYS, SEED)
    Xt = gen_threat(params, N_DAYS, SEED)
    X_all = np.vstack([Xb, Xt])
    y_all = np.array([0]*N_DAYS + [1]*N_DAYS)
    sc = StandardScaler(); X_sc = sc.fit_transform(X_all)

    # Stump adversary
    stump = DecisionTreeClassifier(max_depth=1, max_features=2, random_state=SEED)
    stump.fit(X_sc, y_all)
    stump_acc = stump.score(X_sc, y_all)
    stump_fool = round(1 - stump_acc + (0.5 - abs(stump_acc - 0.5)), 4)
    # MLP adversary
    mlp = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=300,
                        random_state=SEED, early_stopping=True)
    mlp.fit(X_sc, y_all)
    mlp_acc  = mlp.score(X_sc, y_all)
    mlp_fool = round(1 - mlp_acc + (0.5 - abs(mlp_acc - 0.5)), 4)

    stump_fool = min(max(stump_fool, 0), 1)
    mlp_fool   = min(max(mlp_fool,   0), 1)

    if stump_fool >= THRESHOLD and mlp_fool >= THRESHOLD:
        verdict = "PASS"
    elif stump_fool >= THRESHOLD:
        verdict = "PARTIAL"
    else:
        verdict = "FAIL"

    print(f"  {name:20s}  {stump_fool:10.4f}  {mlp_fool:8.4f}  {verdict}")
    rows.append({"Archetype": name, "Stump_Fool": stump_fool,
                 "MLP_Fool": mlp_fool, "Verdict": verdict})

df_out = pd.DataFrame(rows)
stump_mean = df_out["Stump_Fool"].mean()
mlp_mean   = df_out["MLP_Fool"].mean()
full_pass  = (df_out["Verdict"] == "PASS").sum()

print("-" * 65)
print(f"  Mean fool rate  ->  Stump: {stump_mean*100:.1f}%   MLP: {mlp_mean*100:.1f}%")
print(f"  Full PASS (both >=80%): {full_pass}/10")

os.makedirs("results", exist_ok=True)
df_out.to_csv("results/exp8_btt_dual_adversary.csv", index=False)
print(f"Saved: results/exp8_btt_dual_adversary.csv")
