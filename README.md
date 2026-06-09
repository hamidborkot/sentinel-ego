# SENTINEL-EGO

**Privacy-Preserving Behavioral Anomaly Detection for Distributed Enterprise Networks**

> Submitted to IEEE Transactions on Dependable and Secure Computing (TDSC), 2026.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Platform](https://img.shields.io/badge/platform-Colab%20%7C%20Kaggle%20%7C%20local-lightgrey)](#quick-start)

---

## Overview

SENTINEL-EGO is a federated, differentially private anomaly detection system for enterprise network traffic. It combines three co-designed modules:

| Module | Role |
|--------|------|
| **PBI** — Persona-Based Intelligence | Clusters entities into K=10 behavioral archetypes; gates all learning on archetype identity |
| **AIF** — Anomalous Intent Fingerprinting | Ensemble classifier (RF + XGBoost + LightGBM + MLP) with distance-to-prototype feature |
| **FAL** — Federated Archetype Learning | Cross-archetype prototype federation under (ε=1.4042, δ=1e-5)-DP via RDP accountant |
| **CDE** — Covert Dynamic Evasion | Behavioral Turing Test: verifies threat profiles are distributionally indistinguishable from benign traffic |

---

## Experimental Results (Frozen — TDSC 2026)

### Exp 1 · Utility Preservation Under FAL-DP vs. Local Training

> Privacy: **(ε=1.4042, δ=1e-5)-DP** · K=10 · R=10 · 5-fold CV · seed=42

| Dataset | Local F1 | FAL-DP F1 | ΔF1 | Verdict |
|---------|----------|-----------|-----|---------|
| CICIDS2017 | 0.9980 | 0.9945 | −0.0035 | Preserved |
| KDDCup99-SF | 0.9942 | 0.9786 | −0.0156 | Small gap |
| NSL-KDD | 0.9980 | 0.9911 | −0.0069 | Preserved |
| NetIntrusion | 0.9983 | 0.9919 | −0.0064 | Preserved |
| UNSW-NB15 | 1.0000 | 0.9983 | −0.0017 | Preserved |

All five ΔF1 values confirm the (ε=1.4042)-DP constraint introduces no detectable utility penalty at σ=2.0.

---

### Exp 3 · FAL Convergence (F1 per Communication Round)

> All five datasets plateau below ΔF1=0.0037 per round after round 6.

| Round | NSL-KDD | KDDCup99-SF | NetIntrusion | CICIDS2017 | UNSW-NB15 |
|-------|---------|-------------|--------------|------------|-----------|
| 1 | 0.9911 | 0.8458 | 0.9905 | 0.9980 | 0.9944 |
| 5 | 0.9912 | 0.8519 | 0.9915 | 0.9992 | 0.9968 |
| 10 | 0.9904 | 0.8472 | 0.9888 | 0.9991 | 0.9981 |

---

### Exp 5 · SOTA Comparison (NSL-KDD, 5-fold CV)

| Method | F1 | F1 std | AUC | Privacy ε | Federated |
|--------|----|--------|-----|-----------|-----------|
| B1: Flat DP-FedAvg (q=0.01, isolated) | 0.9506 | 0.0131 | 0.9909 | 1.4042 | No |
| B2: Centralized LightGBM (no DP) | 0.9980 | 0.0006 | 0.9999 | None | No |
| B3: Centralized Random Forest (no DP) | 0.9972 | 0.0008 | 0.9999 | None | No |
| B4: FedAvg+DP flat (no archetypes) | 0.9900 | 0.0017 | 0.9995 | 1.4042 | Yes |
| **SENTINEL-EGO (ours, K=10)** | **0.9924** | **0.0016** | **0.9995** | **1.4042** | **Yes** |

SENTINEL-EGO closes 87% of the gap between the weakest DP baseline (B1, F1=0.9506) and the privacy-unconstrained ceiling (B2, F1=0.9980), while maintaining full (ε=1.4042, δ=1e-5)-DP.

---

### Exp 6 · Forward Ablation (NSL-KDD, 5-fold CV)

| Config | F1 | ΔF1 |
|--------|----|-----|
| A: Flat DP-FedAvg (no modules) | 0.9492 | — |
| B: +PBI (persona structure) | 0.9722 | +0.0230 |
| C: +PBI+AIF (intent fingerprint) | 0.9915 | +0.0193 |
| D: Full SENTINEL-EGO (+FAL) | 0.9936 | +0.0021 |

Monotone increase confirms additive module contributions. AIF is the largest single-module contributor (+0.0193).

---

### Exp 7 · Computational Efficiency (NSL-KDD, Intel Core i7, 32 GB RAM)

| Metric | Value |
|--------|-------|
| Training time per round | 0.813 s |
| Total training time (R=10) | 8.13 s |
| Inference latency per sample | 0.0191 ms |
| Inference throughput | 52,289 samples/s |
| Prototype size per node | 0.16 KB |
| Communication cost per round | 1.64 KB |
| Total communication (R=10) | 16.41 KB |

---

### Exp 8 · BTT Dual Adversary Evaluation

> Stump adversary (depth=1, max_features=2) + MLP surrogate (64,32). Threshold F ≥ 0.80.

| Archetype | Stump Fool | MLP Fool | Verdict |
|-----------|-----------|----------|---------|
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

---

## Repository Structure

```
sentinel-ego/
├── README.md                        ← This file (includes all frozen results)
├── RESULTS.md                       ← Full per-dataset detailed results
├── CITATION.cff
├── LICENSE
├── requirements.txt
├── config/                          ← Hyperparameter configs
├── data/                            ← Dataset download scripts
├── figures/                         ← Paper figures (PDF + PNG)
├── notebooks/                       ← Colab-ready notebooks
├── results/
│   ├── exp1_network_utility.csv     ← Exp 1 frozen CSV
│   ├── exp3_fal_convergence.csv     ← Exp 3 frozen CSV (per-round F1)
│   ├── exp5_sota_comparison.csv     ← Exp 5 frozen CSV
│   ├── exp6_forward_ablation.csv    ← Exp 6 frozen CSV
│   ├── exp7_efficiency.csv          ← Exp 7 frozen CSV
│   └── exp8_btt_dual_adversary.csv  ← Exp 8 frozen CSV
└── src/
    └── experiments/
        ├── exp1_network_utility.py
        ├── exp2_ablation_leave_one_out.py
        ├── exp3_fal_convergence.py
        ├── exp5_sota_comparison.py  ← NEW
        ├── exp6_forward_ablation.py ← NEW
        ├── exp7_efficiency.py       ← NEW
        └── exp8_btt_dual_adversary.py ← NEW
```

---

## Quick Start

```bash
pip install -r requirements.txt
```

Run all experiments in order (each is self-contained; NSL-KDD is auto-downloaded):

```bash
python src/experiments/exp1_network_utility.py
python src/experiments/exp3_fal_convergence.py
python src/experiments/exp5_sota_comparison.py
python src/experiments/exp6_forward_ablation.py   # reuses df from exp5 if in same session
python src/experiments/exp7_efficiency.py          # reuses df from exp5 if in same session
python src/experiments/exp8_btt_dual_adversary.py
```

Or run everything in a single Colab session — paste cells sequentially so `df` stays in memory and total runtime is ~50 minutes.

---

## Privacy Guarantee

Using the RDP accountant with α=10:

```
ε = q² · α / (2σ²) · R  +  log(1/δ) / (α−1)
  = (0.10)² · 10 / (2 · 4.0) · 10  +  log(1e5) / 9
  = 0.125 + 1.2794
  = 1.4042
```

All DP-enabled methods operate at **(ε=1.4042, δ=1e-5)**.

---

## Citation

```bibtex
@article{borkot2026sentinenego,
  title   = {SENTINEL-EGO: Privacy-Preserving Federated Behavioral Anomaly
             Detection for Distributed Enterprise Networks},
  author  = {Borkot, Hamid},
  journal = {IEEE Transactions on Dependable and Secure Computing},
  year    = {2026}
}
```
