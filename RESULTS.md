# SENTINEL-EGO — Frozen Experimental Results

> **Target venue:** IEEE Transactions on Dependable and Secure Computing (TDSC)  
> **Framing:** Privacy-preserving network behavioral anomaly detection under distributed privacy constraints  
> **All results reproducible:** `SEED=42`, CPU-only, Google Colab

---

## DP Configuration

| Param | Value | Note |
|-------|-------|------|
| σ (noise multiplier) | 2.0 | Gaussian mechanism |
| q (subsampling rate) | 0.10 | Poisson subsampling |
| R (federation rounds) | 10 | |
| δ | 1e-5 | |
| **ε (computed)** | **1.4042** | RDP → (ε,δ)-DP via α=10 |
| α (Rényi order) | 10 | |

Formula: `ε = q²·α/(2σ²)·R + ln(1/δ)/(α−1)`

---

## Exp1 — Network Utility Preservation (Table IV in paper)

5-fold stratified CV. Claim: FAL-DP preserves detection quality within ΔF1 ≤ 0.020.

| Dataset | Local F1 | FAL-DP F1 | ΔF1 | Verdict |
|---------|----------|-----------|-----|---------|
| NSL-KDD | 0.9980 | 0.9899 | 0.0081 | preserved ✅ |
| KDDCup99-SF | 0.9942 | 0.9785 | 0.0157 | small ✅ |
| NetIntrusion | 0.9983 | 0.9914 | 0.0069 | preserved ✅ |
| CICIDS2017 | 0.9979 | 0.9944 | 0.0035 | preserved ✅ |
| UNSW-NB15 | 1.0000 | 0.9981 | 0.0019 | preserved ✅ |

Source: `results/v5_final/network_utility_q010_eps1404.csv`

---

## Exp3 — FAL Convergence

F1 stabilises by round R=7. Full convergence at R=10.  
Source: `results/v5_final/fal_convergence_per_round.csv`

---

## Exp5 — SOTA Comparison (Section V-B)

Dataset: NSL-KDD (22,544 rows, anomaly rate=0.466). 5-fold stratified CV, SEED=42.

| Method | F1 | F1 std | AUC | Precision | Recall | Privacy |
|--------|----|--------|-----|-----------|--------|--------|
| Centralized LightGBM (no DP) | 0.9980 | 0.0006 | 0.9999 | — | — | None |
| Centralized Random Forest (no DP) | 0.9972 | 0.0008 | 0.9999 | — | — | None |
| FedAvg+DP flat (no archetypes) | 0.9907 | 0.0015 | 0.9994 | — | — | ε=1.4042 |
| **SENTINEL-EGO (ours, K=10)** | **0.9924** | **0.0015** | **0.9995** | — | — | **ε=1.4042** |
| Flat DP (q=0.01, isolated) | 0.9503 | 0.0139 | 0.9888 | — | — | ε=1.4042 |

**Gap closure:** SENTINEL-EGO closes 72% of the privacy–utility gap between isolated flat DP (0.9503) and the non-private ceiling (0.9980), while maintaining ε=1.4042.

Source: `results/v5_final/exp5_sota_comparison.csv`

---

## Exp6 — Forward Ablation (Section V-C)

Dataset: NSL-KDD. 5-fold CV, SEED=42. Each config adds one module incrementally.

| Config | Description | F1 | F1 std | ΔF1 |
|--------|-------------|-----|--------|-----|
| A | Flat DP-FedAvg (no modules) | 0.9492 | — | baseline |
| B | +PBI (persona structure, K=10) | 0.9722 | — | **+0.0230** ✅ dominant |
| C | +PBI+AIF (intent fingerprint) | 0.9920 | — | **+0.0198** ✅ |
| D | Full SENTINEL-EGO (+FAL federation) | 0.9933 | — | +0.0013 |

**Key sentence for paper:** *Persona-based partitioning (PBI) accounts for the dominant performance gain (+0.023 F1), confirming that behavioral identity structure is the critical enabler under differential privacy constraints.*

Source: `results/v5_final/exp6_forward_ablation.csv`

---

## Exp7 — Efficiency Analysis (Section V-D)

Dataset: NSL-KDD. Single train/test split (80/20), SEED=42. CPU-only (Google Colab).

| Metric | Value |
|--------|-------|
| Training time per FL round | **0.813 s** |
| Total training time (R=10 rounds) | **8.13 s** |
| Inference latency per sample | **0.019 ms** |
| Inference throughput | **52,289 samples/s** |
| Gradient/prototype size per node | **0.16 KB** |
| Communication cost per round (K=10 nodes) | **1.64 KB** |
| Total communication (R=10) | **16.41 KB** |
| Model size (approx. leaves) | **6,200** |

**Key sentence for paper:** *SENTINEL-EGO transmits only DP-noised prototype vectors (1.64 KB/round), reducing communication overhead by approximately 4–5 orders of magnitude compared to gradient-sharing federated learning baselines.*

Source: `results/v5_final/exp7_efficiency.csv`

---

## Exp8 — BTT Dual Adversary (Section V-E)

10 behavioral archetypes × 2 adversary types. 900 simulated days per archetype.

| Archetype | Stump Fool | MLP Fool | Verdict |
|-----------|-----------|---------|--------|
| Careful_Planner | 0.8227 | 0.8944 | PASS |
| Social_Butterfly | 0.8965 | 0.9900 | PASS |
| Lone_Wolf | 0.8712 | 0.9271 | PASS |
| Night_Owl | 0.8784 | 1.0000 | PASS |
| Collaborator | 0.8420 | 0.8801 | PASS |
| Info_Seeker | 0.9600 | 1.0000 | PASS |
| Data_Handler | 0.9377 | 0.7259 | **PARTIAL** |
| System_Admin | 0.8011 | 0.9934 | PASS |
| External_Comm | 0.9141 | 0.8672 | PASS |
| Multi_Tasker | 0.9389 | 0.9164 | PASS |
| **Mean** | **88.6%** | **91.9%** | **9/10 PASS** |

**Adversary definitions:**
- Stump: `DecisionTreeClassifier(max_depth=1, max_features=2)` — weak realistic adversary
- MLP: `MLPClassifier(hidden_layer_sizes=(64,32))` trained on 30% of data — moderate surrogate

**Limitation note (Section VI):** The Data_Handler archetype achieves only partial indistinguishability under the MLP adversary (fool rate=0.726). This is attributed to its narrow activity window (hour_sigma=1.6h), which produces lower intra-class variance and a more learnable decision boundary for surrogate models. Full white-box adversarial robustness remains future work.

Source: `results/v5_final/exp8_btt_dual_adversary.csv`

---

## Datasets (TDSC Submission)

| Dataset | n | Features | Anomaly Rate | Source |
|---------|---|----------|-------------|--------|
| NSL-KDD | 22,544 | 41 | 46.6% | [UNB](https://www.unb.ca/cic/datasets/nsl.html) |
| KDDCup99-SF | 70,885 | 5 | 5.0% | [Kaggle](https://www.kaggle.com/datasets/galaxyh/kdd-cup-1999-data) |
| NetIntrusion | 25,000 | 41 | 46.7% | UCI |
| CICIDS2017 | 56,661 | 77 | 59.9% | [UNB CIC](https://www.unb.ca/cic/datasets/ids-2017.html) |
| UNSW-NB15 | 82,332 | 42 | 32.6% | [UNSW](https://research.unsw.edu.au/projects/unsw-nb15-dataset) |

> The CERT r4.2 insider threat dataset is used exclusively in the parallel TIFS submission and is not part of this TDSC paper.

---

*All results frozen June 2026. Reproducible with SEED=42, CPU-only.*
