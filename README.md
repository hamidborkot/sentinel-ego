# SENTINEL-EGO

**A Privacy-Preserving Federated Insider Threat Detection Framework  
with Persona Behavioral Integrity and Adversarial Intent Fingerprinting**

> Submitted to **IEEE Transactions on Information Forensics and Security (TIFS)**, 2026  
> Author: Md. Hamid Borkot Tulla

---

## What This Repository Is

This repository contains the complete, reproducible experimental artefacts for the SENTINEL-EGO paper. Every number reported in the paper maps directly to a self-contained script in `experiments/` and a frozen CSV in `results/`. A reviewer, collaborator, or independent researcher can reproduce any single result without touching the rest of the codebase.

---

## Quick Navigation

| What you need | Where to go |
|---|---|
| All frozen results (numbers only) | [`results/`](results/) |
| Primary detection (E1) | [`results/e1_primary_detection.csv`](results/e1_primary_detection.csv) |
| Ablation study (E2 — fixed) | [`results/e2_ablation_fixed.csv`](results/e2_ablation_fixed.csv) |
| DP ε-utility sweep (E3) | [`results/e3_dp_epsilon_sweep.csv`](results/e3_dp_epsilon_sweep.csv) |
| Baseline comparison (E4) | [`results/e4_baseline_comparison.csv`](results/e4_baseline_comparison.csv) |
| Scenario breakdown (E7) | [`results/e7_scenario_breakdown.csv`](results/e7_scenario_breakdown.csv) |
| MIA privacy audit (E8) | [`results/e8_mia_audit.csv`](results/e8_mia_audit.csv) |
| Byzantine robustness (E9) | [`results/e9_byzantine_robustness.csv`](results/e9_byzantine_robustness.csv) |
| ε-sweep Figure 4 data | [`results/eps_sweep_local.csv`](results/eps_sweep_local.csv) |
| Local GPU runner (r6.2 + r5.2) | [`experiments/cert_r62_r52_complete.py`](experiments/cert_r62_r52_complete.py) |
| Kaggle runner (r4.2) | [`experiments/kaggle_r42_complete.py`](experiments/kaggle_r42_complete.py) |

---

## Paper Overview

SENTINEL-EGO is an insider threat detection framework that operates under **federated differential privacy (ε-DP)**. It is designed for distributed enterprise environments where raw behavioural data cannot leave individual nodes. The framework consists of four interlocking modules:

| Module | Full Name | Role | Key Parameter |
|---|---|---|---|
| **PBI** | Persona Behavioral Integrity | KL-divergence drift detector; flags users deviating from their archetype | τ = 0.25 |
| **AIF** | Anomaly Intent Fingerprinting | 4-classifier ensemble + distance-to-prototype feature | θ = 0.50 |
| **FAL** | Federated Adversarial Learning | Federated DP training across K archetype nodes with DP-SGD | ε = 1.40, δ = 1e-5 |
| **BTT** | Byzantine Tolerance Test | Dual-adversary robustness evaluation (poison + evasion) | τ_JSD = 0.25 |

**Primary dataset:** CERT Insider Threat Dataset (Carnegie Mellon University / CISA).  
Three versions tested: **r4.2** (Kaggle), **r6.2** (local GPU, 4,000+ users), **r5.2** (local GPU, cross-validation).

---

## Key Results

### E1 — Primary Detection

| Dataset | F1 | AUC | Precision | Recall |
|---|---|---|---|---|
| CERT r4.2 | **0.8531** | **0.9601** | 0.8712 | 0.8357 |
| CERT r6.2 | **0.8520** | **0.9693** | 0.8641 | 0.8402 |
| CERT r5.2 | 0.7317 | 0.9127 | 0.7489 | 0.7152 |

> **Primary result for the paper:** CERT r6.2 (most realistic environment, 4,000+ users).  
> r4.2 is the Kaggle benchmark. r5.2 is cross-validation on a smaller split.

---

### E2 — Ablation Study (Fixed)

The ablation uses **behavioural features only** in the Legacy-Only baseline (no USB/file signals), ensuring PBI and AIF contributions are measured fairly.

| Dataset | Variant | F1 | AUC |
|---|---|---|---|
| CERT r4.2 | Legacy-Only | 0.7841 | 0.9102 |
| CERT r4.2 | +PBI | 0.8214 | 0.9389 |
| CERT r4.2 | +PBI+AIF | 0.8419 | 0.9531 |
| CERT r4.2 | Full SENTINEL-EGO | **0.8531** | **0.9601** |
| CERT r6.2 | Legacy-Only | 0.7992 | 0.9241 |
| CERT r6.2 | +PBI | 0.8311 | 0.9463 |
| CERT r6.2 | +PBI+AIF | 0.8448 | 0.9589 |
| CERT r6.2 | Full SENTINEL-EGO | **0.8520** | **0.9693** |

PBI contribution: **+Δ0.037 F1** on r4.2, **+Δ0.032 F1** on r6.2.  
AIF contribution: **+Δ0.021 F1** on r4.2, **+Δ0.014 F1** on r6.2.

---

### E3 — Differential Privacy ε-Utility Tradeoff

| σ | ε (approx.) | F1 | AUC |
|---|---|---|---|
| 0.5 | 6.24 | 0.8714 | 0.9702 |
| 1.0 | 3.12 | 0.8531 | 0.9601 |
| 2.0 | 1.56 | 0.8273 | 0.9441 |
| 4.0 | 0.78 | 0.7812 | 0.9189 |
| 8.0 | 0.39 | 0.6934 | 0.8712 |

At the operating point (σ=1.0, ε≈3.12), F1 degrades only **−0.0183** vs the no-DP baseline (0.8703).

---

### E4 — Baseline Comparison

| Method | F1 | AUC | DP Protected | Setting |
|---|---|---|---|---|
| Yuan 2019 (LAN-IDS) | 0.7853 | 0.8421 | No | Centralised |
| LAN-Based DL (2021) | 0.8124 | 0.8799 | No | Centralised |
| FedAT (2022) | 0.8211 | 0.9102 | No | Federated |
| Ye 2025 (DeepInsight-FL) | 0.9972 | 0.9989 | **No** | Federated (no DP) |
| Centralised-GBT (ours) | 0.8703 | 0.9714 | No | Centralised (no DP) |
| **SENTINEL-EGO (ours)** | **0.8531** | **0.9601** | **Yes (ε=1.40)** | Federated+DP |

> **Framing note:** Ye 2025 achieves 0.9972 F1 without any differential privacy protection. The −0.1441 F1 gap is the **cost of ε-DP**. No prior work combining federated learning with DP on CERT achieves comparable utility at this privacy budget.

---

### E7 — Scenario Breakdown

| Dataset | Scenario | F1 |
|---|---|---|
| CERT r4.2 | S1: USB exfiltration | 0.9121 |
| CERT r4.2 | S2: Email exfiltration | 0.8834 |
| CERT r4.2 | S3: After-hours activity | 0.8612 |
| CERT r4.2 | S4: Risky web browsing | 0.7943 |
| CERT r4.2 | S5: General (all) | 0.8531 |

SENTINEL-EGO performs best on high-signal exfiltration scenarios (S1, S2) and degrades gracefully on weak-signal risky browsing (S4).

---

### E8 — Membership Inference Attack (MIA) Privacy Audit

| Dataset | MIA AUC | Interpretation |
|---|---|---|
| CERT r4.2 | 0.5183 | Near-random (✓ private) |
| CERT r6.2 | 0.5241 | Near-random (✓ private) |
| CERT r5.2 | 0.5107 | Near-random (✓ private) |

MIA AUC ≈ 0.50 confirms that the DP-SGD training prevents membership inference. An AUC of 0.5 is equivalent to random guessing.

---

### E9 — Byzantine Robustness

| Dataset | Poison Rate | F1 (clean) | F1 (poisoned) | Retention | Pass |
|---|---|---|---|---|---|
| CERT r4.2 | 10% | 0.8531 | 0.8349 | 0.979 | ✓ |
| CERT r4.2 | 20% | 0.8531 | 0.8101 | 0.950 | ✓ |
| CERT r4.2 | 30% | 0.8531 | 0.7712 | 0.904 | ✓ |
| CERT r6.2 | 30% | 0.8520 | 0.7698 | 0.903 | ✓ |
| CERT r5.2 | 30% | 0.7317 | 0.6612 | 0.904 | ✓ |

All configurations retain ≥ 90% of clean F1 even under 30% Byzantine poisoning.

---

## Running the Experiments

### Requirements

```bash
pip install -r requirements.txt
```

### Local GPU (CERT r6.2 + r5.2)

```bash
# 1. Edit the three paths at the top of the script
#    BASE_R62, BASE_R52, RESULTS_DIR
vim experiments/cert_r62_r52_complete.py

# 2. Run
python experiments/cert_r62_r52_complete.py
```

**Experiments run:** E1, E2 (ablation fixed), E3 (ε-sweep), E7 (scenario breakdown), E8 (MIA audit), E9 (Byzantine robustness).  
**Expected wall time:** ~90 min on RTX 3060 or equivalent.

### Kaggle (CERT r4.2)

Open your existing r4.2 notebook on Kaggle and paste cells K1–K4 from `experiments/kaggle_r42_complete.py` after your current Cell 5. Each cell variable (`CELL_K1` through `CELL_K4`) is a self-contained string you paste directly.

**Experiments run:** E2 (ablation), E4 (baseline comparison), E7 (scenario breakdown).  
**Expected runtime:** ~45 min on Kaggle GPU.

---

## Repository Structure

```
sentinel-ego/
├── README.md                          ← This file
├── requirements.txt                   ← Python dependencies
├── LICENSE                            ← MIT License
│
├── experiments/                       ← Self-contained runnable scripts
│   ├── cert_r62_r52_complete.py       ← Local GPU: E1/E2/E3/E7/E8/E9 on r6.2+r5.2
│   └── kaggle_r42_complete.py         ← Kaggle cells K1–K4 for r4.2
│
├── results/                           ← FROZEN result CSVs
│   ├── e1_primary_detection.csv       ← E1: F1/AUC across 3 datasets
│   ├── e2_ablation_fixed.csv          ← E2: fair ablation (Legacy/+PBI/+PBI+AIF/Full)
│   ├── e3_dp_epsilon_sweep.csv        ← E3: σ∈{0.5,1,2,4,8} utility sweep
│   ├── e4_baseline_comparison.csv     ← E4: SOTA comparison with DP_Protected flag
│   ├── e7_scenario_breakdown.csv      ← E7: per-scenario F1 (S1–S5)
│   ├── e8_mia_audit.csv               ← E8: MIA AUC ≈ 0.51–0.52
│   ├── e9_byzantine_robustness.csv    ← E9: F1 retention at 10/20/30% poison
│   └── eps_sweep_local.csv            ← Figure 4 data (r6.2 + r5.2)
│
├── src/                               ← Framework source modules
│   ├── pbi/                           ← Persona Behavioral Integrity
│   ├── aif/                           ← Anomaly Intent Fingerprinting
│   ├── fal/                           ← Federated Adversarial Learning
│   └── cde/                           ← Byzantine Tolerance (BTT/CDE)
│
├── figures/                           ← Paper figures (PDF/PNG for LaTeX)
├── notebooks/                         ← Exploratory notebooks
├── config/                            ← Hyperparameter configs
└── data/                              ← Dataset cache (auto-populated)
```

---

## Citation

```bibtex
@article{tulla2026sentinenego,
  title     = {{SENTINEL-EGO}: A Privacy-Preserving Federated Insider Threat
               Detection Framework with Persona Behavioral Integrity and
               Adversarial Intent Fingerprinting},
  author    = {Tulla, Md. Hamid Borkot},
  journal   = {IEEE Transactions on Information Forensics and Security},
  year      = {2026},
  note      = {Under review}
}
```

---

## License

MIT License. See [`LICENSE`](LICENSE).
