# 🛡️ SENTINEL-EGO

> **A Federated Adversarial Deception Framework for Insider Threat Detection**  
> *IEEE Transactions on Information Forensics and Security — Under Review*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-CPU--Only%20%7C%20Google%20Colab-orange?logo=googlecolab)](https://colab.research.google.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![DP](https://img.shields.io/badge/Differential%20Privacy-%CE%B5%3D1.28%20(%CF%83%3D2.0%2C%20q%3D0.01)-purple)](#dp-guarantees)
[![F1](https://img.shields.io/badge/Best%20F1-0.9993%20(NSL--KDD)-brightgreen)](#key-results)
[![BTT](https://img.shields.io/badge/BTT%20Fool%20Rate-91.5%25%20(Tier--1)-brightgreen)](#btt-adversary-ladder)

---

## Overview

SENTINEL-EGO is a four-module cybersecurity framework that creates ten persistent synthetic employee personas ("Ego nodes") grounded in real Enron email data. Together they form a federated honeypot collective:

| Module | Full Name | Role |
|--------|-----------|------|
| **PBI** | Persona Behavioral Identity | Mines 10 behavioral archetypes from Enron; τ=0.25 drift detection |
| **AIF** | Adversarial Interaction Fingerprint | 42-feature attacker profiling; LightGBM F1=0.9993 |
| **FAL** | Federated Adversarial Learning | DP-FedProto across 10 nodes; closes 57.6% isolation-to-global gap on CERT r4.2 |
| **CDE** | Collective Deception Evolution | 15-round evasion-aware mutation; F1=0.8584 under full evasion vs. 0.7665 baseline |

**Validated on 6 benchmark datasets** (5 network + CERT r4.2 insider threat). CPU-only, Google Colab compatible.

---

## Repository Structure

```
sentinel-ego/
├── README.md                          # This file
├── RESULTS.md                         # Full paper-ready results with all numbers
├── LICENSE
├── CITATION.cff
├── requirements.txt
│
├── config/
│   ├── dp_config.yaml                 # DP params (σ=2.0, q=0.01, ε=1.2805)
│   ├── experiment_config.yaml
│   └── system_config.yaml
│
├── src/
│   ├── experiments/
│   │   ├── exp1_network_utility.py    # Network utility: Local vs FAL-DP (ε=1.4042)
│   │   ├── exp2_ablation_leave_one_out.py  # Leave-one-out ablation Table IV-B
│   │   └── exp3_fal_convergence.py   # FAL convergence figure (R=10 rounds)
│   ├── pbi/
│   ├── aif/
│   ├── fal/
│   ├── cde/
│   ├── mirror/
│   └── ex8_btt_v4.py                 # BTT 3-tier adversary ladder
│
├── notebooks/
│   ├── pipeline_phases1to5_all5datasets.py
│   ├── Phase1_PBI_Enron_Mining.ipynb
│   ├── Phase2_AIF_Profiler.ipynb
│   ├── Phase3_FAL_FedAvg_DP.ipynb
│   ├── Phase4_CDE_Evolution.ipynb
│   └── Phase5_Mirror_Defense.ipynb
│
├── results/
│   ├── v5_final/                      # ✅ PRIMARY: all paper-ready CSVs
│   │   ├── README.md                  # File index and reproducibility notes
│   │   ├── network_utility_q010_eps1404.csv
│   │   ├── ablation_leave_one_out.csv
│   │   ├── fal_convergence_per_round.csv
│   │   ├── dp_accounting_corrected_subsampling.csv
│   │   ├── cert_r42_fedproto_results.csv
│   │   ├── cert_r42_scenario_ablation.csv
│   │   ├── btt_3tier_v4_fool_rates.csv
│   │   └── pbi_tau_sweep.csv
│   └── v3_all5_datasets/              # Historical: earlier experiment runs
│
└── figures/
```

---

## Key Results

| Metric | Value | Dataset | Source |
|--------|-------|---------|--------|
| Best AIF F1 | **0.9993** | NSL-KDD | `v3_all5_datasets/phase2_aif_all5.csv` |
| DP guarantee (CERT) | **ε=1.2805** | CERT r4.2 | `v5_final/dp_accounting_corrected_subsampling.csv` |
| DP guarantee (Network) | **ε=1.4042** | All 5 networks | `v5_final/dp_accounting_corrected_subsampling.csv` |
| FAL gap closure | **57.6%** | CERT r4.2 | `v5_final/cert_r42_fedproto_results.csv` |
| Network utility (max ΔF1) | **0.0157** | KDDCup99-SF | `v5_final/network_utility_q010_eps1404.csv` |
| CDE resilience | **F1=0.8584** at round 15 | UNSW-NB15 | `v3_all5_datasets/phase4_cde_evolution_all5.csv` |
| BTT fool rate (Tier-1) | **91.5%** (10/10 ≥80%) | — | `v5_final/btt_3tier_v4_fool_rates.csv` |
| PBI optimal threshold | **τ=0.25**, F1=0.9953 | Enron | `v5_final/pbi_tau_sweep.csv` |

---

## DP Guarantees

Formal differential privacy via Poisson subsampling + Rényi DP composition.

**RDP composition chain:**
```
ε_subsample(α) = q² · α / (2σ²)            [per-round subsampled RDP]
ε_total(α)     = R · ε_subsample(α)          [R-round composition]
ε_DP           = ε_total + ln(1/δ)/(α−1)     [RDP → (ε,δ)-DP conversion]
```

| Experiment | q | σ | R | ε |
|-----------|---|---|---|---|
| Exp A — CERT FedProto | 0.01 | 2.0 | 10 | **1.2805** |
| Exp B — Network Utility | 0.10 | 2.0 | 10 | **1.4042** |

---

## FAL: Federation Results

### CERT r4.2 — Cross-Scenario Knowledge Transfer

| Config | F1 | Gap Closed |
|--------|----|------------|
| Isolated (no federation) | 0.0457 | 0% |
| Plain-Fed (no DP) | 0.7699 | 95.8% |
| **DP-FedProto (ε=1.2805)** | **0.4812** | **57.6%** |
| Global (centralised) | 0.8013 | 100% |

### Network Datasets — Utility Preservation (ε=1.4042)

| Dataset | Local F1 | FAL-DP F1 | ΔF1 |
|---------|----------|-----------|-----|
| NSL-KDD | 0.9980 | 0.9899 | 0.0081 ✅ |
| KDDCup99-SF | 0.9942 | 0.9785 | 0.0157 |
| NetIntrusion | 0.9983 | 0.9914 | 0.0069 ✅ |
| CICIDS2017 | 0.9979 | 0.9944 | 0.0035 ✅ |
| UNSW-NB15 | 1.0000 | 0.9981 | 0.0019 ✅ |

---

## BTT Adversary Ladder

Three-tier black-box adversary following Biggio et al. (2013):

| Tier | Classifier | Mean Fool Rate | Pass ≥80% |
|------|-----------|--------------|----------|
| Tier-1 | Decision Stump (depth=1) | **91.5%** | 10/10 |
| Tier-2 | Logistic Regression | **83.3%** | 8/10 |
| Tier-3 | Random Forest (depth=3) | **77.0%** | 3/10 |

JSD (behavioral indistinguishability): Mean=0.0011, Max=0.0025 — all ≪ 0.25 threshold. ✅

---

## Datasets

| Dataset | n | Features | Attack Rate | Source |
|---------|---|----------|------------|--------|
| NSL-KDD | 22,544 | 41 | 46.6% | [UNB](https://www.unb.ca/cic/datasets/nsl.html) |
| KDDCup99-SF | 70,885 | 5 | 5.0% | [Kaggle](https://www.kaggle.com/datasets/galaxyh/kdd-cup-1999-data) |
| NetIntrusion | 25,000 | 41 | 46.7% | UCI |
| CICIDS2017 | 56,661 | 77 | 59.9% | [UNB CIC](https://www.unb.ca/cic/datasets/ids-2017.html) |
| UNSW-NB15 | 82,332 | 42 | 32.6% | [UNSW](https://research.unsw.edu.au/projects/unsw-nb15-dataset) |
| CERT r4.2 | 103,000 | 30 | 0.73% | [CMU CERT](https://kilthub.cmu.edu/articles/dataset/CERT_Insider_Threat_Dataset/12687840) |

---

## Quick Start

```bash
git clone https://github.com/hamidborkot/sentinel-ego.git
cd sentinel-ego
pip install -r requirements.txt
```

**Run the three paper experiments:**
```bash
python src/experiments/exp1_network_utility.py
python src/experiments/exp2_ablation_leave_one_out.py
python src/experiments/exp3_fal_convergence.py
```

**Run full pipeline (Google Colab):**
```python
# Open notebooks/pipeline_phases1to5_all5datasets.py in Colab
# Run cells A → B → C → D → E → F → G → H  (no GPU required)
```

---

## Citation

```bibtex
@article{tulla2026sentinel,
  title   = {SENTINEL-EGO: A Federated Adversarial Deception Framework
             for Insider Threat Detection},
  author  = {Tulla, Md. Hamid Borkot},
  journal = {IEEE Transactions on Information Forensics and Security},
  year    = {2026},
  note    = {Under Review}
}
```

---

## License

MIT — see [LICENSE](LICENSE)

---

*Last updated: June 2026. All v5 results in `results/v5_final/`. Reproducible with `SEED=42` on CPU.*
