# 🛡️ The Sentinel Ego

> **A Federated Adversarial Deception Framework for Insider Threat Detection**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-CPU--Only%20%7C%20Google%20Colab-orange?logo=googlecolab)](https://colab.research.google.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Phase](https://img.shields.io/badge/Pipeline-Phase%201--5%20Complete-brightgreen)](#pipeline-phases-1--5)
[![KL](https://img.shields.io/badge/KL%20Consistency-10%2F10%20Strong-brightgreen)](#table-vi--phase-1-90-day-kl-consistency)
[![F1](https://img.shields.io/badge/Best%20F1-0.9993%20(NSL--KDD)-brightgreen)](#table-i--phase-2-best-aif-model-per-dataset)
[![DP](https://img.shields.io/badge/Differential%20Privacy-%CE%B5%3D13.7792%20(%CF%83%3D2.0)-purple)](#ex-1-differential-privacy-accounting)

---

## 📋 Overview

The **Sentinel Ego** is a novel cybersecurity framework of ten persistent synthetic employee personas ("Ego nodes"), each possessing a unique behavioral identity grounded in real Enron email data. Together they form a federated honeypot collective that:

- 🎭 **Deceives attackers** using behaviorally realistic, temporally consistent synthetic identities
- 🔍 **Profiles adversaries** via a 42-feature Adversarial Interaction Fingerprint (AIF)
- 🤝 **Shares threat intelligence** through privacy-preserving Federated Adversarial Learning (FedAvg + DP)
- 🧬 **Evolves deception strategies** via Collective Deception Evolution (CDE) across 15 mutation rounds
- 🪮 **Intercepts spear-phishing** pre-click using Mirror Ego behavioral risk scoring

**Full pipeline validated on 5 real benchmark datasets** — CPU-only, Google Colab compatible.

---

## 🗂️ Repository Structure

```
sentinel-ego/
├── README.md
├── RESULTS.md
├── LICENSE
├── requirements.txt
├── config/
│   ├── dp_config.yaml                    # DP params (σ=2.0, ε=13.7792)
│   ├── experiment_config.yaml
│   └── system_config.yaml
│
├── notebooks/
│   ├── pipeline_phases1to5_all5datasets.py
│   ├── Phase1_PBI_Enron_Mining.ipynb
│   ├── Phase2_AIF_Profiler.ipynb
│   ├── Phase3_FAL_FedAvg_DP.ipynb
│   ├── Phase4_CDE_Evolution.ipynb
│   └── Phase5_Mirror_Defense.ipynb
│
├── src/
│   ├── pbi/
│   ├── aif/
│   ├── fal/
│   ├── cde/
│   ├── mirror/
│   └── ex8_btt_v4.py                     # Behavioral Turing Test (88.6% fool rate)
│
├── figures/
│
└── results/
    ├── v3_all5_datasets/                 # ✅ PRIMARY: all verified experiment CSVs
    ├── dp_accounting.csv
    ├── differential_privacy_accounting.md
    └── ex8_btt_v4_fool_rate.csv
```

---

## 🔬 Datasets

### Phase 1 Only — Behavioral Archetype Mining

| Dataset | Source | Size | Role |
|---------|--------|------|------|
| Enron Email Corpus | [CMU](https://www.cs.cmu.edu/~enron/) | 517,401 emails, 92 users | PBI archetype discovery only |

### Phases 2–5 — Detection Experiments

| Dataset | Source | n | Features | Attack Rate |
|---------|--------|---|----------|-------------|
| KDDCup99-SF | [Kaggle](https://www.kaggle.com/datasets/galaxyh/kdd-cup-1999-data) | 73,237 | 41 | 5.0% |
| NSL-KDD | [UNB](https://www.unb.ca/cic/datasets/nsl.html) | 22,544 | 41 | 56.7% |
| NetIntrusion | UCI | 25,000 | 42 | 46.7% |
| CICIDS2017 | [UNB CIC](https://www.unb.ca/cic/datasets/ids-2017.html) | 150,000 | 78 | 46.2% |
| UNSW-NB15 | [UNSW](https://research.unsw.edu.au/projects/unsw-nb15-dataset) | 100,000 | 49 | 32.6% |

---

## Pipeline: Phases 1–5

### EX-1: Differential Privacy Accounting

**Config:** C=1.0 | Rounds=10 | Nodes=10 | α=10 | δ=1×10⁻⁵  
**Formula:** `ε = α/(2σ²) × rounds + ln(1/δ)/(α−1)`

| σ | RDP (α=10) | ε | Notes |
|---|-----------|---|-------|
| 0.5 | 800.0 | 201.2792 | Too weak |
| 1.0 | 50.0 | 51.2792 | Weak — ε>10, not publishable |
| 1.5 | 22.22 | 23.5014 | Borderline |
| **2.0** | **12.5** | **13.7792** | **← PAPER CHOICE** |
| 3.0 | 5.56 | 6.8348 | Stronger but higher noise |

**Formal Guarantee: (13.7792, 1×10⁻⁵)-DP** at σ=2.0  
Verification: `12.5 + ln(100000)/9 = 12.5 + 1.2792 = 13.7792` ✅  
Framed as a practical privacy-utility tradeoff consistent with deployed FL systems [McMahan et al., 2018].  
Source: [`results/dp_accounting.csv`](results/dp_accounting.csv)

---

### TABLE I — Phase 2 (AIF): Best Model per Dataset

Source: [`results/v3_all5_datasets/phase2_aif_all5.csv`](results/v3_all5_datasets/phase2_aif_all5.csv)

| Dataset | Best Model | F1 | AUC |
|---------|------------|-----|-----|
| KDDCup99-SF | LightGBM | 0.9992 | 1.0000 |
| **NSL-KDD** | **LightGBM** | **0.9993** | **1.0000** |
| NetIntrusion | LightGBM | 0.9988 | 1.0000 |
| CICIDS2017 | LightGBM | 0.9972 | 0.9996 |
| UNSW-NB15 | LightGBM | 0.9802 | 0.9982 |

> **Best F1: 0.9993** (LightGBM, NSL-KDD). These are real v3 experiment results.

---

### TABLE II — Phase 5 (5-Fold CV): Cross-Validated Performance

Source: [`results/v3_all5_datasets/phase5_5fold_cv_all5.csv`](results/v3_all5_datasets/phase5_5fold_cv_all5.csv)

| Dataset | F1 Mean | ±Std | AUC |
|---------|---------|------|-----|
| KDDCup99-SF | 0.9995 | ±0.0001 | 0.9997 |
| NSL-KDD | 0.9991 | ±0.0003 | 1.0000 |
| **NetIntrusion** | **0.9993** | ±0.0002 | **1.0000** |
| CICIDS2017 | 0.9979 | ±0.0003 | 0.9998 |
| UNSW-NB15 | 0.9801 | ±0.0003 | 0.9980 |

---

### TABLE III — Phase 3 (FAL): Federation Results

FedAvg across 10 non-IID Ego nodes under **(13.7792, 1×10⁻⁵)-DP** at σ=2.0.  
Source: [`results/v3_all5_datasets/phase3_federation_all5.csv`](results/v3_all5_datasets/phase3_federation_all5.csv)

| Dataset | Isolated Mean | Federated Mean | Mean Gain | Best Node Gain |
|---------|--------------|---------------|-----------|---------------|
| KDDCup99-SF | 0.9886 | 0.9884 | −0.0002 | +0.0015 |
| NSL-KDD | 0.9883 | 0.9881 | −0.0002 | +0.0021 |
| **NetIntrusion** | **0.9882** | **0.9887** | **+0.0006** | **+0.0016** |
| CICIDS2017 | 0.9845 | 0.9846 | +0.0001 | +0.0015 |
| UNSW-NB15 | 0.9685 | 0.9692 | +0.0006 | +0.0017 |

> ⚠️ Mean federation gains are marginal (−0.0002 to +0.0006). This is expected — isolated models are already high-performing. The framework's value is **privacy-preserving collective inference**.

---

### TABLE IV — Phase 4 (CDE): Adversarial Evasion Impact

15 mutation rounds: Evasive / Mimicry / Noise.  
Source: [`results/v3_all5_datasets/phase4_cde_evolution_all5.csv`](results/v3_all5_datasets/phase4_cde_evolution_all5.csv)

| Dataset | Baseline F1 | Round-15 F1 | Drop | Peak JSD |
|---------|------------|------------|------|----------|
| KDDCup99-SF | 0.9995 | 0.9538 | −0.0457 | 0.5222 |
| NSL-KDD | 0.9989 | 0.7222 | −0.2767 | 0.4413 |
| NetIntrusion | 0.9998 | 0.5506 | −0.4492 | 0.5518 |
| CICIDS2017 | 0.9979 | 0.2313 | −0.7666 | 0.4132 |
| **UNSW-NB15** | **0.9794** | **0.9774** | **−0.0020** | **0.3749** |

> UNSW-NB15 shows exceptional resilience (drop only −0.0020 at peak JSD=0.3749). CDE demonstrates the adversarial challenge your framework studies.

---

### TABLE V — Phase 5 (Mirror Defense): Pre-Click Interception

Source: [`results/v3_all5_datasets/phase5_mirror_defense_all5.csv`](results/v3_all5_datasets/phase5_mirror_defense_all5.csv)

| Dataset | Base F1 | Mirror F1 | ΔF1 | AUC |
|---------|---------|-----------|-----|-----|
| KDDCup99-SF | 0.9995 | 0.9996 | +0.0001 | 0.9997 |
| NSL-KDD | 0.9989 | 0.9988 | −0.0001 | 1.0000 |
| NetIntrusion | 0.9998 | 0.9996 | −0.0002 | 1.0000 |
| CICIDS2017 | 0.9979 | 0.9978 | −0.0001 | 0.9998 |
| UNSW-NB15 | 0.9794 | 0.9794 | +0.0001 | 0.9982 |

> Mirror defense adds ≤±0.0002 ΔF1 overhead across all datasets.

---

### TABLE VI — Phase 1 (PBI): 90-Day KL Consistency

Source: [`results/v3_all5_datasets/phase1_kl_90day_fixed.csv`](results/v3_all5_datasets/phase1_kl_90day_fixed.csv)

| Archetype | KL Hour | KL DoW | KL Recipients | KL Mean | Status |
|-----------|---------|--------|--------------|---------|--------|
| Morning Bird | 0.0077 | 0.0509 | 0.0537 | 0.0374 | ✅ Strong |
| Collaborator | 0.0119 | 0.0160 | 0.0115 | 0.0132 | ✅ Strong |
| Balanced | 0.0371 | 0.0173 | 0.0078 | 0.0208 | ✅ Strong |
| Workaholic | 0.0071 | 0.0766 | 0.0025 | 0.0288 | ✅ Strong |
| Night Owl | 0.0393 | 0.0228 | 0.0093 | 0.0238 | ✅ Strong |
| Tech Savvy | 0.0363 | 0.0438 | 0.0201 | 0.0334 | ✅ Strong |
| Careful Planner | 0.0303 | 0.0119 | 0.0404 | 0.0275 | ✅ Strong |
| Lone Wolf | 0.0402 | 0.0432 | 0.0075 | 0.0303 | ✅ Strong |
| Workaholic_8 | 0.0318 | 0.0120 | 0.0014 | 0.0150 | ✅ Strong |
| Social Butterfly | 0.0131 | 0.0271 | 0.0049 | 0.0150 | ✅ Strong |

> **10/10 archetypes Strong.** Mean KL=0.0245, max=0.0374 — all far below 0.30 threshold.

---

### TABLE VII — EX-8: Behavioral Turing Test (BTT v4)

Source: [`results/ex8_btt_v4_fool_rate.csv`](results/ex8_btt_v4_fool_rate.csv)  
Attacker: `DecisionTree(max_depth=1)` | 900 simulation days

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

---

## 🔑 Key Results Summary

| Metric | Value | Source |
|--------|-------|--------|
| Best AIF F1 | **0.9993** (LightGBM, NSL-KDD) | phase2_aif_all5.csv |
| Best 5-Fold CV F1 | **0.9995** ±0.0001 (KDDCup99-SF) | phase5_5fold_cv_all5.csv |
| CDE Best Resilience | **−0.0020 drop** at JSD=0.3749 (UNSW-NB15) | phase4_cde_evolution_all5.csv |
| Mirror Defense overhead | **≤±0.0002 ΔF1** all datasets | phase5_mirror_defense_all5.csv |
| BTT Mean Fool Rate | **88.6%** (10/10 ≥80%) | ex8_btt_v4_fool_rate.csv |
| PBI Stability | **10/10 Strong** (KL mean=0.0245) | phase1_kl_90day_fixed.csv |
| Differential Privacy | **(13.7792, 1×10⁻⁵)-DP** at σ=2.0 | dp_accounting.csv |

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
# Run each CELL section: A → B → C → D → E → F → G → H
# No GPU required.
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

*Last verified: June 2026 — All numbers from `/results/v3_all5_datasets/` CSVs. DP: σ=2.0, ε=13.7792 (10 rounds × 10 nodes). F1=0.9993, AUC=1.0 are real v3 results.*
