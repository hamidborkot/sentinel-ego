# SENTINEL-EGO

**Privacy-Preserving Behavioral Anomaly Detection for Distributed Enterprise Networks**

> Submitted to IEEE Transactions on Dependable and Secure Computing (TDSC), 2026.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Platform](https://img.shields.io/badge/platform-Colab%20%7C%20Kaggle%20%7C%20local-lightgrey)](#quick-start)

---

## Overview

SENTINEL-EGO is a federated, differentially private anomaly detection system for enterprise network traffic. It combines four co-designed modules:

| Module | Role |
|--------|------|
| **PBI** — Persona-Based Intelligence | Clusters network entities into K=10 behavioral archetypes; gates all learning on archetype identity |
| **AIF** — Anomalous Intent Fingerprinting | Ensemble classifier with distance-to-prototype feature as the primary discriminative signal |
| **FAL** — Federated Archetype Learning | Cross-archetype prototype federation under (ε=1.4042, δ=1e-5)-DP via RDP accountant (Mironov, 2017) |
| **CDE** — Covert Dynamic Evasion | Behavioral Turing Test: verifies that threat profiles are distributionally indistinguishable from benign traffic |

**The core architectural advantage** of SENTINEL-EGO over flat DP-FedAvg is not a single metric improvement but a three-dimensional gain: equivalent utility under equal privacy budget + 3.7× adversarial robustness + >100× communication efficiency.

---

## Experimental Results (Frozen — TDSC 2026)

### Exp 1 · Utility Preservation (5 Datasets, FAL-DP vs. Local)

> **(ε=1.4042, δ=1e-5)-DP** · K=10 · σ=2.0 · R=10 · 5-fold CV · seed=42

| Dataset | Local F1 | FAL-DP F1 | ΔF1 | Verdict |
|---------|----------|-----------|-----|---------|
| CICIDS2017 | 0.9980 | 0.9945 | −0.0035 | Preserved |
| KDDCup99-SF | 0.9942 | 0.9786 | −0.0156 | Small gap† |
| NSL-KDD | 0.9980 | 0.9911 | −0.0069 | Preserved |
| NetIntrusion | 0.9983 | 0.9919 | −0.0064 | Preserved |
| UNSW-NB15 | 1.0000 | 0.9983 | −0.0017 | Preserved |

†KDDCup99-SF gap reflects its 5.0% anomaly rate: DP subsampling reduces scarce anomaly signal proportionally more. This motivates PBI (see EXP 6).

---

### Exp 3 · FAL Convergence (F1 per Communication Round)

> All five datasets plateau below ΔF1=0.0037/round after round 6 — confirming stability, not just convergence speed.

| Round | NSL-KDD | KDDCup99-SF | NetIntrusion | CICIDS2017 | UNSW-NB15 |
|-------|---------|-------------|--------------|------------|-----------|
| 1 | 0.9911 | 0.8458 | 0.9905 | 0.9980 | 0.9944 |
| 5 | 0.9912 | 0.8519 | 0.9915 | 0.9992 | 0.9968 |
| 10 | 0.9904 | 0.8472 | 0.9888 | 0.9991 | 0.9981 |

---

### Exp 5 · SOTA Comparison (NSL-KDD, 5-fold CV)

| Method | F1 | ±std | AUC | Privacy ε | Federated |
|--------|----|------|-----|-----------|-----------|
| B1: Flat DP-FedAvg (q=0.01, isolated) | 0.9506 | 0.0131 | 0.9909 | 1.4042 | No |
| B2: Centralized LightGBM (no DP) | 0.9980 | 0.0006 | 0.9999 | None | No |
| B3: Centralized Random Forest (no DP) | 0.9972 | 0.0008 | 0.9999 | None | No |
| B4: FedAvg+DP flat (no archetypes) | 0.9900 | 0.0017 | 0.9995 | 1.4042 | Yes |
| **SENTINEL-EGO (ours, K=10)** | **0.9924** | **0.0016** | **0.9995** | **1.4042** | **Yes** |

SENTINEL-EGO closes **87%** of the B1→B2 gap under full (ε=1.4042, δ=1e-5)-DP.

---

### Exp 6 · Forward Ablation (NSL-KDD, 5-fold CV)

| Config | Description | F1 | ΔF1 |
|--------|-------------|-----|-----|
| A | Flat DP-FedAvg (no modules) | 0.9492 | — |
| B | +PBI: archetype routing | 0.9722 | +0.0230 |
| C | +PBI+AIF: distance feature | 0.9915 | +0.0193 |
| D | Full SENTINEL-EGO (+FAL) | 0.9936 | +0.0021 |

**Total gain A→D: +0.0444** (+4.44 pp). AIF is the largest single contributor.

---

### Exp 7 · Computational Efficiency

| Metric | Value |
|--------|-------|
| Training time per round | 0.813 s |
| Total training time (R=10) | 8.13 s |
| Inference latency | 0.0191 ms/sample |
| Throughput | 52,289 samples/s |
| Communication per round | 1.64 KB (K=10 nodes) |
| Total communication (R=10) | **16.41 KB** |

>100× communication reduction vs. gradient-sharing FL at equivalent utility.

---

### Exp 8 · BTT Dual Adversary (Gradient Inversion)

| Metric | Value |
|--------|-------|
| Archetypes tested | 10/10 |
| PASS (fool rate ≥ 0.80) | **9/10** |
| Mean Stump fool rate | 88.6% |
| Mean MLP fool rate | 91.9% |
| Only PARTIAL: Data_Handler | MLP=0.7259 |

---

### Exp 9 · Privacy–Utility Tradeoff ← NEW

> Sweeps σ ∈ {10.0, 5.0, 3.0, 2.0, 1.5, 1.0, 0.5, ∞} with privacy-proportional q.  
> Metrics: Macro-F1 and Detection Rate at FPR=1% (DR@1%FPR).

| Privacy Regime | σ | q | ε | F1 | DR@1%FPR |
|----------------|---|---|---|-----|----------|
| Extreme | 10.0 | 0.02 | 1.2794 | 0.9709 | 0.9602 |
| Strong | 5.0 | 0.04 | 1.2824 | 0.9813 | 0.9753 |
| High | 3.0 | 0.06 | 1.2992 | 0.9885 | 0.9880 |
| Moderate-High | 2.0 | 0.08 | 1.3592 | 0.9908 | 0.9908 |
| **Operating Point** | **1.5** | **0.10** | **1.5014** | **0.9921** | **0.9936** |
| Low | 1.0 | 0.10 | 1.7792 | 0.9917 | 0.9918 |
| Very Low | 0.5 | 0.10 | 3.2792 | 0.9936 | 0.9957 |
| No DP | ∞ | 0.10 | ∞ | 0.9919 | 0.9929 |

**F1 degrades gracefully: −2.27 pp over the full privacy range.  
DR@1%FPR: −3.55 pp — the more sensitive metric to privacy cost.  
Operating point sits on the utility plateau, not the degradation cliff.**

---

## Repository Structure

```
sentinel-ego/
├── README.md                          ← This file
├── RESULTS.md                         ← Full detailed results with interpretations
├── CITATION.cff
├── LICENSE
├── requirements.txt
├── config/
├── data/
├── figures/
├── notebooks/
├── results/
│   ├── exp1_network_utility.csv
│   ├── exp3_fal_convergence.csv
│   ├── exp5_sota_comparison.csv
│   ├── exp6_forward_ablation.csv
│   ├── exp7_efficiency.csv
│   ├── exp8_btt_dual_adversary.csv
│   └── exp9_final.csv                 ← NEW: privacy-utility tradeoff
└── src/
    └── experiments/
        ├── exp1_network_utility.py
        ├── exp2_ablation_leave_one_out.py
        ├── exp3_fal_convergence.py
        ├── exp5_sota_comparison.py
        ├── exp6_forward_ablation.py
        ├── exp7_efficiency.py
        ├── exp8_btt_dual_adversary.py
        └── exp9_privacy_utility.py    ← NEW
```

---

## Quick Start

```bash
pip install -r requirements.txt
```

Run all experiments sequentially (each is self-contained; datasets auto-downloaded):

```bash
python src/experiments/exp1_network_utility.py
python src/experiments/exp3_fal_convergence.py
python src/experiments/exp5_sota_comparison.py
python src/experiments/exp6_forward_ablation.py
python src/experiments/exp7_efficiency.py
python src/experiments/exp8_btt_dual_adversary.py
python src/experiments/exp9_privacy_utility.py   # NEW
```

Or paste all cells sequentially in a single Colab session (~65 min total).

---

## Privacy Guarantee

RDP accountant (Mironov, 2017), α=10:

```
ε = q² · α / (2σ²) · R  +  log(1/δ) / (α−1)
  = (0.10)² · 10 / (2·4.0) · 10  +  ln(1e5) / 9
  = 0.1250 + 1.2794
  = 1.4042
```

All DP methods operate at **(ε=1.4042, δ=1e-5)**. See EXP 9 for the full privacy-utility tradeoff curve across σ ∈ {0.5 … 10.0}.

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
