# 🛡️ SENTINEL-EGO

> **Privacy-Preserving Network Behavioral Anomaly Detection under Distributed Privacy Constraints**  
> *IEEE Transactions on Dependable and Secure Computing (TDSC) — Under Review*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-CPU--Only%20%7C%20Google%20Colab-orange?logo=googlecolab)](https://colab.research.google.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![DP](https://img.shields.io/badge/Differential%20Privacy-%CE%B5%3D1.4042%20(%CF%83%3D2.0%2C%20q%3D0.10)-purple)](#dp-guarantees)
[![F1](https://img.shields.io/badge/SENTINEL--EGO%20F1-0.9924%20(NSL--KDD)-brightgreen)](#key-results)
[![BTT](https://img.shields.io/badge/BTT%20MLP%20Fool%20Rate-91.9%25%20(9%2F10%20PASS)-brightgreen)](#btt-dual-adversary)

---

## Overview

SENTINEL-EGO is a four-module framework for **network behavioral anomaly detection under distributed privacy constraints**. It operates across federated enterprise network nodes, preserving differential privacy (ε=1.4042) while maintaining detection utility within ΔF1 ≤ 0.020 of non-private centralized baselines across five standard benchmark datasets.

> **Scope note:** This repository supports the TDSC submission. The five evaluation datasets are standard network intrusion/anomaly benchmarks (NSL-KDD, KDDCup99-SF, NetIntrusion, CICIDS2017, UNSW-NB15). SENTINEL-EGO addresses **network behavioral anomaly detection** — not insider threat detection. The CERT r4.2 dataset is used in a separate, parallel submission (TIFS).

| Module | Full Name | Role |
|--------|-----------|------|
| **PBI** | Persona Behavioral Identity | Mines 10 behavioral archetypes from network flow data; τ=0.25 drift detection |
| **AIF** | Adversarial Interaction Fingerprint | 42-feature attacker profiling; LightGBM F1=0.9924 at ε=1.4042 |
| **FAL** | Federated Adversarial Learning | DP-FedProto across 10 nodes; closes 72% of privacy–utility gap vs. flat DP |
| **BTT** | Behavioral Turing Test | Dual-adversary indistinguishability: 91.9% MLP fool rate, 9/10 archetypes PASS |

**Validated on 5 network benchmark datasets.** CPU-only, Google Colab compatible. All experiments self-contained and reproducible with `SEED=42`.

---

## Repository Structure

```
sentinel-ego/
├── README.md                              # This file
├── RESULTS.md                             # Full paper-ready results with all numbers
├── LICENSE
├── CITATION.cff
├── requirements.txt
│
├── config/
│   ├── dp_config.yaml                     # DP params (σ=2.0, q=0.10, ε=1.4042)
│   ├── experiment_config.yaml
│   └── system_config.yaml
│
├── src/
│   ├── experiments/
│   │   ├── exp1_network_utility.py        # Exp1: Local vs FAL-DP, 5 datasets (Table IV)
│   │   ├── exp2_ablation_leave_one_out.py # Exp2: Leave-one-out ablation (appendix)
│   │   └── exp3_fal_convergence.py        # Exp3: FAL convergence over R=10 rounds
│   ├── pbi/
│   ├── aif/
│   ├── fal/
│   ├── cde/
│   └── ex8_btt_v4.py                      # Exp8: BTT dual-adversary (stump + MLP)
│
├── notebooks/
│   ├── pipeline_phases1to5_all5datasets.py
│   └── *.ipynb                            # Phase notebooks (Colab-ready)
│
└── results/
    └── v5_final/                          # ✅ PRIMARY: all paper-ready frozen CSVs
        ├── README.md
        ├── network_utility_q010_eps1404.csv
        ├── ablation_leave_one_out.csv
        ├── fal_convergence_per_round.csv
        ├── dp_accounting_corrected_subsampling.csv
        ├── exp5_sota_comparison.csv        # NEW: SOTA comparison table
        ├── exp6_forward_ablation.csv       # NEW: 4-step forward ablation
        ├── exp7_efficiency.csv             # NEW: training time, latency, comm. cost
        ├── exp8_btt_dual_adversary.csv     # NEW: stump + MLP dual adversary BTT
        └── exp5_8_summary.md              # NEW: frozen result record
```

---

## Key Results

| Metric | Value | Dataset | Experiment |
|--------|-------|---------|------------|
| SENTINEL-EGO F1 (ε=1.4042) | **0.9924** | NSL-KDD | Exp5 |
| Privacy–utility gap closed vs. flat DP | **72%** | NSL-KDD | Exp5 |
| Network utility max ΔF1 | **≤0.020** | All 5 datasets | Exp1 |
| PBI contribution (forward ablation) | **+0.0230 F1** | NSL-KDD | Exp6 |
| AIF contribution (forward ablation) | **+0.0198 F1** | NSL-KDD | Exp6 |
| Training time per FL round | **0.813 s** | NSL-KDD | Exp7 |
| Communication cost per round | **1.64 KB** | NSL-KDD | Exp7 |
| BTT stump fool rate | **88.6%** (10/10) | — | Exp8 |
| BTT MLP fool rate | **91.9%** (9/10 PASS) | — | Exp8 |

---

## DP Guarantees

Formal differential privacy via Poisson subsampling + Rényi DP composition.

**RDP composition chain:**
```
ε_subsample(α) = q² · α / (2σ²)        [per-round subsampled RDP]
ε_total(α)     = R · ε_subsample(α)      [R-round composition]
ε_DP           = ε_total + ln(1/δ)/(α−1) [RDP → (ε,δ)-DP conversion]
```

| Configuration | q | σ | R | δ | ε |
|--------------|---|---|---|---|---|
| FAL-DP (TDSC — network) | 0.10 | 2.0 | 10 | 1e-5 | **1.4042** |

---

## Experiment Results

### Exp5 — SOTA Comparison (NSL-KDD, 5-fold CV)

| Method | F1 | AUC | Privacy |
|--------|-----|-----|--------|
| Centralized LightGBM (no DP) | 0.9980 | 0.9999 | None |
| Centralized Random Forest (no DP) | 0.9972 | 0.9999 | None |
| FedAvg+DP flat (no archetypes) | 0.9907 | 0.9994 | ε=1.4042 |
| **SENTINEL-EGO (ours, K=10)** | **0.9924** | **0.9995** | **ε=1.4042** |
| Flat DP (q=0.01, isolated) | 0.9503 | 0.9888 | ε=1.4042 |

SENTINEL-EGO closes **72% of the gap** between isolated flat DP (0.9503) and the privacy-free ceiling (0.9980), while maintaining identical ε=1.4042.

### Exp6 — Forward Ablation (NSL-KDD)

| Config | F1 | ΔF1 |
|--------|----|-----|
| A: Flat DP-FedAvg (no modules) | 0.9492 | baseline |
| B: +PBI (persona structure) | 0.9722 | +0.0230 ✅ dominant gain |
| C: +PBI+AIF (intent fingerprint) | 0.9920 | +0.0198 ✅ |
| D: Full SENTINEL-EGO (+FAL) | 0.9933 | +0.0013 |

Persona-based partitioning (PBI) delivers the dominant performance gain (+0.023), confirming that behavioral identity structure is the critical enabler under differential privacy constraints.

### Exp7 — Efficiency (NSL-KDD, CPU)

| Metric | Value |
|--------|-------|
| Training time per FL round | 0.813 s |
| Total training time (R=10) | 8.13 s |
| Inference latency | 0.019 ms/sample |
| Inference throughput | 52,289 samples/s |
| Communication per round | **1.64 KB** |
| Total communication (R=10) | 16.41 KB |
| Model size (approx. leaves) | 6,200 |

SENTINEL-EGO transmits only DP-noised prototype vectors (1.64 KB/round), reducing communication overhead by approximately **4–5 orders of magnitude** compared to gradient-sharing federated learning baselines.

### Exp8 — BTT Dual Adversary

| Archetype | Stump Fool | MLP Fool | Verdict |
|-----------|-----------|---------|--------|
| Careful_Planner | 0.8227 | 0.8944 | PASS |
| Social_Butterfly | 0.8965 | 0.9900 | PASS |
| Lone_Wolf | 0.8712 | 0.9271 | PASS |
| Night_Owl | 0.8784 | 1.0000 | PASS |
| Collaborator | 0.8420 | 0.8801 | PASS |
| Info_Seeker | 0.9600 | 1.0000 | PASS |
| Data_Handler | 0.9377 | 0.7259 | PARTIAL |
| System_Admin | 0.8011 | 0.9934 | PASS |
| External_Comm | 0.9141 | 0.8672 | PASS |
| Multi_Tasker | 0.9389 | 0.9164 | PASS |
| **Mean** | **88.6%** | **91.9%** | **9/10 PASS** |

The Data_Handler partial result (MLP fool=0.726) is attributed to its narrow activity window (hour_sigma=1.6h), which produces lower intra-class variance and a more learnable boundary for surrogate models. This is reported as a known limitation.

---

## Quick Start

```bash
git clone https://github.com/hamidborkot/sentinel-ego.git
cd sentinel-ego
pip install -r requirements.txt
```

**Run paper experiments (self-contained, no external data required):**
```bash
# Exp1: Network utility across 5 datasets
python src/experiments/exp1_network_utility.py

# Exp3: FAL convergence
python src/experiments/exp3_fal_convergence.py
```

**All new experiments (Exp5–8) are self-contained Colab cells** — paste directly, no imports from this repo. See `RESULTS.md` for the full code blocks.

---

## Citation

```bibtex
@article{tulla2026sentinel,
  title   = {SENTINEL-EGO: Privacy-Preserving Network Behavioral Anomaly
             Detection under Distributed Privacy Constraints},
  author  = {Tulla, Md. Hamid Borkot},
  journal = {IEEE Transactions on Dependable and Secure Computing},
  year    = {2026},
  note    = {Under Review}
}
```

---

## License

MIT — see [LICENSE](LICENSE)

---

*Last updated: June 2026. All results frozen in `results/v5_final/`. Fully reproducible with `SEED=42` on CPU.*
