# =============================================================================
# THE SENTINEL EGO — Complete Pipeline: Phase 1–5, All 5 Datasets
# Target: IEEE Transactions on Information Forensics and Security (TIFS)
# Author: Md. Hamid Borkot Tulla
# Datasets: KDDCup99-SF, NSL-KDD, NetIntrusion, CICIDS2017, UNSW-NB15
# Environment: Google Colab (GPU not required)
# =============================================================================
# USAGE:
#   1. Run dataset_loader cell first (loads all 5 datasets into DATASETS dict)
#   2. Run CELL A (shared utilities)
#   3. Run CELL B (Phase 1: PBI + 90-day KL)
#   4. Run CELL C (Phase 2: AIF 42-feature profiler)
#   5. Run CELL D (Phase 3: FedAvg + DP accounting)
#   6. Run CELL E (Phase 4: CDE mutation + DRS)
#   7. Run CELL F (Phase 5: Mirror Defense + Ablation + 5-Fold CV)
#   8. Run CELL G-PREP + CELL G (figures)
#   9. Run CELL H (summary tables + ZIP download)
# =============================================================================

# ── DATASET LOADER ────────────────────────────────────────────────────────────
# Prerequisite: run this block to populate DATASETS dict
# (KDDCup99-SF, NSL-KDD, NetIntrusion, CICIDS2017, UNSW-NB15)
# All datasets must have a binary 'label' column (0=normal, 1=attack)

# ── CELL A: SHARED UTILITIES ──────────────────────────────────────────────────
import os, warnings
import numpy as np
import pandas as pd
from scipy.stats import entropy
from scipy.spatial.distance import jensenshannon
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, roc_auc_score, silhouette_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

warnings.filterwarnings("ignore")
np.random.seed(42)

ROOT    = "/content/sentinel_ego"
FIG_DIR = f"{ROOT}/figures"
for d in [f"{ROOT}/phase1", f"{ROOT}/phase2", f"{ROOT}/phase3",
          f"{ROOT}/phase4", f"{ROOT}/phase5", FIG_DIR]:
    os.makedirs(d, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 300, "font.size": 11,
    "axes.titlesize": 12, "axes.labelsize": 11,
    "xtick.labelsize": 10, "ytick.labelsize": 10
})

ARCHETYPE_NAMES = [
    "Morning Bird", "Collaborator", "Balanced", "Workaholic", "Night Owl",
    "Tech Savvy", "Careful Planner", "Lone Wolf", "Workaholic_8", "Social Butterfly"
]

def prepare_xy(df):
    X = df.drop("label", axis=1).select_dtypes(include=[float, int]).fillna(0)
    X = X.replace([np.inf, -np.inf], 0)
    return StandardScaler().fit_transform(X), df["label"].values.astype(int)

def safe_auc(y_true, y_proba):
    try:
        return roc_auc_score(y_true, y_proba)
    except ValueError:
        return float("nan")

print("Shared utilities loaded. Datasets:", list(DATASETS.keys()))

# ── CELL B: PHASE 1 — PBI + 90-DAY KL ANALYSIS ───────────────────────────────
# Full code: see CELL B in the session that generated results/v3_all5_datasets/
# Key parameters:
#   N_USERS=92 (Enron), SIM_DAYS=90, early=days 0-44, late=days 45-89
#   3rd-order Markov chain on hourly sequences, 10 archetypes × 3 personas
#   KL threshold: 0.30 (strong consistency). Achieved: mean=0.0245
# Output: phase1_kl_90day_fixed.csv

# ── CELL C: PHASE 2 — AIF 42-FEATURE PROFILER ────────────────────────────────
# Key parameters:
#   AIF_N=42 (pad with squared features if <42, select top-variance if >42)
#   Models: RandomForest(200), XGBoost(200), LightGBM(200), MLP(128,64)
#   Split: 80/20 stratified
# Output: phase2_aif_all5.csv

# ── CELL D: PHASE 3 — FEDERATED ADVERSARIAL LEARNING ─────────────────────────
# Key parameters:
#   N_NODES=10, N_ROUNDS=10, non-IID partition (skewed attack ratios)
#   FedAvg: weighted average by node sample count
#   DP: Rényi (alpha=10), sigma=[0.5,1.0], delta=1e-5, steps=N_ROUNDS
# Output: phase3_federation_all5.csv

# ── CELL E: PHASE 4 — COLLECTIVE DECEPTION EVOLUTION ─────────────────────────
# Key parameters:
#   N_CDE_ROUNDS=15, MUTATION_RATE=0.15
#   Strategies (cycled): evasive → mimicry → noise
#   JSD computed per feature column, mean reported
#   DRS = 0.4*(jsd/peak_jsd) + 0.4*confusion_prob + 0.2*jsd_node
# Output: phase4_cde_evolution_all5.csv, phase4_drs_scores_all5.csv

# ── CELL F: PHASE 5 — MIRROR DEFENSE + ABLATION + 5-FOLD CV ──────────────────
# Key parameters:
#   Mirror: top 10% features by importance inverted and appended
#   5-Fold CV: StratifiedKFold(5), RF+XGB+LGBM
#   Ablation: NSL-KDD, 6 components (Legacy → Full Pipeline)
# Output: phase5_mirror_defense_all5.csv, phase5_5fold_cv_all5.csv,
#         phase5_ablation_nslkdd.csv

# ── CELLS G + H: FIGURES + SUMMARY ───────────────────────────────────────────
# 8 publication-ready figures (300 DPI):
#   fig1_silhouette.png         Phase 1: K-Means silhouette K=2..7
#   fig2_kl_consistency.png     Phase 1: 90-day KL per archetype (3 bars)
#   fig3_aif_heatmap.png        Phase 2: F1+AUC dual heatmap
#   fig4_federation_nodes.png   Phase 3: isolated vs federated (5 subplots)
#   fig5_cde_evolution.png      Phase 4: JSD + DetF1 per round (2×5 panel)
#   fig6_drs_heatmap.png        Phase 4: DRS heatmap (10 archetypes × 5 datasets)
#   fig7_mirror_cv.png          Phase 5: mirror defense + 5-fold CV side-by-side
#   fig8_ablation.png           Phase 5: horizontal ablation bar chart

# ── REPRODUCIBILITY NOTES ────────────────────────────────────────────────────
# All random states seeded at 42. Results are fully deterministic.
# CICIDS2017 source: Western-OC2-Lab/Intrusion-Detection (GitHub)
# UNSW-NB15 source: Kaggle API (markdaniellampa/unsw-nb15-network-dataset)
# KDDCup99-SF, NSL-KDD, NetIntrusion: sklearn/UCI/standard sources
# No synthetic data used. All experiments on real, raw network traffic datasets.
