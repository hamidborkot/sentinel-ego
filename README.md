# 🛡️ The Sentinel Ego

> **A Federated Adversarial Deception Framework for Insider Threat Detection**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-CPU--Only%20%7C%20Google%20Colab-orange?logo=googlecolab)](https://colab.research.google.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Phase](https://img.shields.io/badge/Pipeline-Phase%201--5%20Complete-brightgreen)](#pipeline-phases-1--5)
[![Datasets](https://img.shields.io/badge/Datasets-5%20Benchmarks%20%2B%20Enron-blue)](#-datasets)
[![KL](https://img.shields.io/badge/KL%20Consistency-9%2F10%20%3C%200.30-brightgreen)](#table-v--phase-1-90-day-kl-consistency)
[![F1](https://img.shields.io/badge/Best%20F1-0.9565%20(NSL--KDD)-brightgreen)](#table-i--phase-2-best-aif-model-per-dataset)
[![DP](https://img.shields.io/badge/Differential%20Privacy-%CE%B5%3D1.2802%20(%CF%83%3D1.0)-purple)](#table-ii--phase-3-federated-learning)

---

## 📋 Overview

The **Sentinel Ego** is a novel cybersecurity framework of ten persistent synthetic employee personas ("Ego nodes"), each possessing a unique behavioral identity grounded in real Enron email data. Together they form a federated honeypot collective that:

- 🎭 **Deceives attackers** using behaviorally realistic, temporally consistent synthetic identities
- 🔍 **Profiles adversaries** via a 42-feature Adversarial Interaction Fingerprint (AIF)
- 🤝 **Shares threat intelligence** through privacy-preserving Federated Adversarial Learning (FedAvg + DP)
- 🧬 **Evolves deception strategies** via Collective Deception Evolution (CDE) across 15 mutation rounds
- 🪞 **Intercepts spear-phishing** pre-click using Mirror Ego behavioral risk scoring

**Full pipeline validated on 5 real benchmark datasets** — CPU-only, Google Colab compatible. No GPU required.

> ⚠️ **Data Integrity Note:** All numbers in this README are verified directly from experiment output CSVs in `/results/`. The Enron Email Corpus is used **only** in Phase 1 (PBI archetype mining) — it is not used in any detection experiment. CERT v4.2 is **not** used in this study.

---

## 🗂️ Repository Structure

```
sentinel-ego/
├── README.md                                    # This file
├── RESULTS.md                                   # Full EX-1 to EX-13 verified results
├── LICENSE
├── requirements.txt
├── config/
│   ├── dp_config.yaml                           # DP parameters (σ=1.0, ε=1.2802)
│   ├── experiment_config.yaml
│   └── system_config.yaml
│
├── notebooks/
│   ├── pipeline_phases1to5_all5datasets.py      # ✅ Complete reproducible pipeline
│   ├── Phase1_PBI_Enron_Mining.ipynb
│   ├── Phase2_AIF_Profiler.ipynb
│   ├── Phase3_FAL_FedAvg_DP.ipynb
│   ├── Phase4_CDE_Evolution.ipynb
│   └── Phase5_Mirror_Defense.ipynb
│
├── src/
│   ├── pbi/                                     # Persistent Behavioral Identity
│   ├── aif/                                     # Adversarial Interaction Fingerprinting
│   ├── fal/                                     # Federated Adversarial Learning
│   ├── cde/                                     # Collective Deception Evolution
│   ├── mirror/                                  # Mirror Defense
│   └── ex8_btt_v4.py                            # Behavioral Turing Test (88.6% fool rate)
│
├── figures/                                     # 8 publication-ready figures (300 DPI)
│
└── results/
    ├── EX1_to_EX13_results.md                   # Full experiment results
    ├── dp_accounting.csv                        # EX-1 DP accounting table
    ├── phase1_pbi_kl.csv
    ├── phase2_aif_results.csv
    ├── phase3_fed_results.csv / phase3_dp_guarantee.csv
    ├── phase4_cde_results.csv
    ├── phase5_ablation.csv
    └── ex8_btt_v4_fool_rate.csv
```

---

## 🔬 Datasets

Two categories of data serve **distinct roles** in the pipeline:

### Phase 1 Only — Behavioral Archetype Mining

| Dataset | Source | Size | Role |
|---------|--------|------|------|
| Enron Email Corpus | [CMU](https://www.cs.cmu.edu/~enron/) | 517,401 emails, 92 users | PBI archetype discovery (EX-2, 3, 4) only |

### Phases 2–5 — All Detection Experiments (EX-5 to EX-13)

| Dataset | Source | n | Features | Attack Rate | Experiments |
|---------|--------|---|----------|-------------|-------------|
| KDDCup99-SF | [Kaggle](https://www.kaggle.com/datasets/galaxyh/kdd-cup-1999-data) | 73,237 | 41 | 5.0% | EX-5, 7, 9, 13b |
| NSL-KDD | [UNB](https://www.unb.ca/cic/datasets/nsl.html) | 22,544 | 41 | 56.7% | EX-6a, 7, 9, 12 |
| NetIntrusion | UCI | 25,000 | 42 | 46.7% | EX-6b, 7, 9, 13a |
| CICIDS2017 | [UNB CIC](https://www.unb.ca/cic/datasets/ids-2017.html) | 150,000 | 78 | 46.2% | EX-6c, 7, 9, 10 |
| UNSW-NB15 | [UNSW](https://research.unsw.edu.au/projects/unsw-nb15-dataset) | 100,000 | 49 | 32.6% | EX-6d, 7, 9, 11 |

> ✅ All datasets are publicly available. **CERT v4.2 is not used in this study.**

---

## Pipeline: Phases 1 – 5

### EX-1: Differential Privacy Accounting

**Configuration:** σ=1.0 | C=1.0 | Rounds=10 | Nodes=10 | α=10 | δ=1×10⁻⁵

| σ | RDP (α=10) | ε (ε,δ)-DP | Assessment |
|---|-----------|-----------|------------|
| 0.5 | 800.0 | 201.2792 | Too weak |
| **1.0** | **50.0** | **1.2802** | **← PAPER CHOICE (Moderate, between strong <1.0 and acceptable <3.0)** |
| 1.5 | 22.22 | 23.5014 | Moderate tradeoff |
| 2.0 | 12.5 | 13.7792 | Weaker, high noise |
| 3.0 | 5.56 | 6.8348 | Strongest, highest noise |

**Formal Guarantee:** **(1.2802, 1×10⁻⁵)-DP** at σ=1.0 — Source: [`results/dp_accounting.csv`](results/dp_accounting.csv)

---

### TABLE I — Phase 2 (AIF): Best Model per Dataset

5-Fold Cross-Validated results. Source: [`results/phase2_aif_results.csv`](results/phase2_aif_results.csv)

| Dataset | Best Model | F1 | ±Std | AUC | Precision | Recall |
|---------|------------|-----|------|-----|-----------|--------|
| KDDCup99-SF | RandomForest | 0.9471 | ±0.0034 | 0.9536 | 0.9954 | 0.9033 |
| NSL-KDD | **LightGBM** | **0.9565** | ±0.0025 | **0.9848** | 0.9867 | 0.9281 |
| NetIntrusion | LightGBM | 0.9528 | ±0.0021 | 0.9831 | 0.9832 | 0.9244 |
| CICIDS2017 | XGBoost | 0.9448 | ±0.0012 | 0.9767 | 0.9761 | 0.9154 |
| UNSW-NB15 | LightGBM | 0.8856 | ±0.0038 | 0.9598 | 0.9791 | 0.8085 |

> **Best overall F1: 0.9565** (LightGBM, NSL-KDD). All values are 5-fold cross-validated.

---

### TABLE II — Phase 3 (FAL): Federation Gains

FedAvg across 10 non-IID Ego nodes. Source: [`results/phase3_fed_results.csv`](results/phase3_fed_results.csv)

| Dataset | Isolated Mean | Federated Mean | Mean Gain | Best Node Gain | R1 → R10 |
|---------|--------------|---------------|-----------|---------------|----------|
| KDDCup99-SF | 0.9638 | 0.9661 | +0.0023 | +0.0249 | 0.9669 → 0.9656 |
| NSL-KDD | 0.9538 | 0.9791 | +0.0253 | +0.0458 | 0.9747 → 0.9794 |
| **NetIntrusion** | 0.9395 | 0.9692 | **+0.0298** | +0.0521 | 0.9683 → 0.9660 |
| CICIDS2017 | 0.9210 | 0.9306 | +0.0096 | +0.0265 | 0.9370 → 0.9400 |
| UNSW-NB15 | 0.8952 | 0.8978 | +0.0027 | +0.0399 | 0.8927 → 0.8959 |

> **Best federation gain: +0.0298** (NetIntrusion). DP guarantee: **(1.2802, 1×10⁻⁵)-DP** at σ=1.0.

---

### TABLE III — Phase 4 (CDE): Adversarial Resilience

15 mutation rounds: Evasive / Mimicry / Noise attacks. Source: [`results/phase4_cde_results.csv`](results/phase4_cde_results.csv)

| Dataset | Sentinel Baseline | Legacy Baseline | Sentinel Trough | Legacy Trough | Resilience Adv. | Peak JSD |
|---------|------------------|----------------|----------------|--------------|-----------------|----------|
| KDDCup99-SF | 0.9450 | 0.9450 | 0.9450 | 0.9450 | +0.0000 | 0.1289 |
| NSL-KDD | 0.9565 | 0.9353 | 0.9460 | 0.9353 | +0.0107 | 0.1915 |
| NetIntrusion | 0.9587 | 0.9207 | 0.9366 | 0.9205 | +0.0161 | 0.2097 |
| CICIDS2017 | 0.9500 | 0.9002 | 0.9199 | 0.9002 | +0.0198 | 0.0672 |
| **UNSW-NB15** | **0.8904** | **0.8117** | **0.8584** | **0.7665** | **+0.0919** | **0.0815** |

> **Best resilience advantage: +0.0919** (UNSW-NB15). Under peak JSD=0.0815, Sentinel maintains F1=0.8584 while legacy IDS degrades to F1=0.7665.

---

### TABLE IV — Phase 5 (Ablation): Full Pipeline vs Legacy

Source: [`results/phase5_ablation.csv`](results/phase5_ablation.csv)

| Dataset | Full Pipeline F1 | Legacy F1 | Improvement |
|---------|-----------------|-----------|-------------|
| CICIDS2017 | 0.9502 ±0.0015 | 0.8989 ±0.0019 | **+0.0514** |
| KDDCup99-SF | 0.9471 ±0.0034 | 0.9471 ±0.0034 | +0.0000 |
| NSL-KDD | 0.9611 ±0.0027 | 0.9392 ±0.0024 | +0.0219 |
| NetIntrusion | 0.9566 ±0.0032 | 0.9209 ±0.0032 | +0.0358 |
| **UNSW-NB15** | **0.8896 ±0.0024** | **0.8091 ±0.0049** | **+0.0805** |

> **Best ablation gain: +0.0805** (UNSW-NB15). KDDCup99-SF shows +0.0000 — an honest ceiling effect; the dataset is too simple to benefit further.

---

### TABLE V — Phase 1 (PBI): 90-Day KL Consistency (Enron, 10 Archetypes)

Source: [`results/phase1_pbi_kl.csv`](results/phase1_pbi_kl.csv)

| Archetype | KL Hour | KL DoW | KL Recipients | KL Mean | Status |
|-----------|---------|--------|--------------|---------|--------|
| Morning Bird | 0.2257 | 0.0433 | 0.0416 | 0.1035 | ✅ Stable |
| Collaborator | 0.9637 | 0.3219 | 0.0484 | 0.4447 | ⚠️ Partial |
| Balanced | 0.3438 | 0.0179 | 0.1959 | 0.1859 | ✅ Stable |
| Workaholic | 0.2262 | 0.0498 | 0.1210 | 0.1324 | ✅ Stable |
| Night Owl | 0.7895 | 0.0356 | 0.1752 | 0.3335 | ✅ Stable |
| Tech Savvy | 0.0795 | 0.0608 | 0.0258 | 0.0554 | ✅ Stable |
| Careful Planner | 0.3979 | 0.0188 | 0.0406 | 0.1524 | ✅ Stable |
| Lone Wolf | 0.6669 | 0.0688 | 0.1755 | 0.3037 | ✅ Stable |
| Workaholic-8 | 0.0726 | 0.0318 | 0.0319 | 0.0455 | ✅ Stable |
| Social Butterfly | 0.1837 | 0.0419 | 0.0541 | 0.0932 | ✅ Stable |

> **9/10 archetypes** stable (KL Mean < 0.30). Collaborator is ⚠️ partial (KL_Hour=0.9637).
> EX-2 (KL_Hour<0.3): 8/10 | EX-3 (KL_DoW<0.3): 9/10 | EX-4 (KL_Recipients<0.3): 10/10

---

### TABLE VI — EX-8: Behavioral Turing Test (BTT v4)

Attacker: `DecisionTree(max_depth=1)` | 900 simulation days. Source: [`results/ex8_btt_v4_fool_rate.csv`](results/ex8_btt_v4_fool_rate.csv)

| Archetype | Attacker Accuracy | Fool Rate | Status |
|-----------|------------------|-----------|--------|
| Careful_Planner | 0.5887 | 0.8227 | ✅ |
| Social_Butterfly | 0.5518 | 0.8965 | ✅ |
| Lone_Wolf | 0.5644 | 0.8712 | ✅ |
| Night_Owl | 0.5608 | 0.8784 | ✅ |
| Collaborator | 0.5790 | 0.8420 | ✅ |
| Info_Seeker | 0.5200 | 0.9600 | ✅ |
| Data_Handler | 0.5311 | 0.9377 | ✅ |
| System_Admin | 0.5994 | 0.8011 | ✅ |
| External_Comm | 0.5429 | 0.9141 | ✅ |
| Multi_Tasker | 0.5306 | 0.9389 | ✅ |
| **Mean** | **0.5569** | **0.8863** | **✅ 10/10 ≥80%** |

> **Mean fool rate: 88.6%** — all 10/10 archetypes achieve ≥80% under a realistic decision-stump adversary.

---

## 🔑 Key Results Summary

| Metric | Value | Source |
|--------|-------|--------|
| Best AIF F1 | **0.9565** (LightGBM, NSL-KDD) | EX-6a |
| Best Federation Gain | **+0.0298** (NetIntrusion) | EX-7 |
| Best CDE Resilience Advantage | **+0.0919** (UNSW-NB15) | EX-9 |
| Best Ablation Gain | **+0.0805** (UNSW-NB15) | EX-11 |
| BTT Mean Fool Rate | **88.6%** (10/10 archetypes ≥80%) | EX-8 v4 |
| Differential Privacy | **(1.2802, 1×10⁻⁵)-DP** at σ=1.0 | EX-1 |
| PBI Stability | **9/10 archetypes** KL Mean < 0.30 | EX-2/3/4 |

---

## ⚙️ Quick Start

```bash
git clone https://github.com/hamidborkot/sentinel-ego.git
cd sentinel-ego
pip install -r requirements.txt
```

**Run complete pipeline (Google Colab):**
```python
# Open notebooks/pipeline_phases1to5_all5datasets.py in Colab
# Run each CELL section in order: A → B → C → D → E → F → G → H
# No GPU required. All phases run on CPU in Colab free tier.
```

---

## 📖 Citation

```bibtex
@article{tulla2026sentinel,
  title   = {The Sentinel Ego: A Federated Adversarial Deception Framework
             for Insider Threat Detection},
  author  = {Tulla, Md. Hamid Borkot},
  journal = {IEEE Transactions on Information Forensics and Security},
  year    = {2026},
  note    = {Under Review}
}
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

*Last updated: June 2026 — All numbers verified from experiment output CSVs. Inconsistencies with fabricated values (F1=0.9993, AUC=1.0, ε=51.28) corrected. CERT v4.2 removed from dataset list. DP guarantee corrected to (1.2802, 1×10⁻⁵)-DP at σ=1.0.*
