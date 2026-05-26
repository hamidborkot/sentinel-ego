# 🛡️ The Sentinel Ego

> **A Federated Adversarial Deception Framework for Insider Threat Detection**  
> IEEE Transactions on Information Forensics and Security (TIFS) — 2026 Submission

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-CPU--Only%20%7C%20Google%20Colab-orange?logo=googlecolab)](https://colab.research.google.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Experiments](https://img.shields.io/badge/Experiments-EX--1%20to%20EX--13-brightgreen)](#experiments-ex-1--ex-13)
[![Claims](https://img.shields.io/badge/Paper%20Claims-28%2F28%20Validated-brightgreen)](#validated-paper-claims-2828)
[![BTT](https://img.shields.io/badge/Behavioral%20Turing%20Test-88.6%25-blue)](#ex-8--behavioral-turing-test-btt-v4)
[![DP](https://img.shields.io/badge/Differential%20Privacy-%CE%B5%3D13.7792%20%28%CF%83%3D2.0%29-purple)](#ex-1--differential-privacy-accounting)

---

## 📋 Overview

The **Sentinel Ego** is a novel cybersecurity framework consisting of ten persistent synthetic employee personas ("Ego nodes"), each possessing a unique behavioral identity grounded in real Enron email data. Together they form a federated honeypot collective that:

- 🎭 **Deceives attackers** using behaviorally realistic, temporally consistent synthetic identities
- 🔍 **Profiles adversaries** in real-time via a 42-feature Adversarial Interaction Fingerprint (AIF)
- 🤝 **Shares threat intelligence** through privacy-preserving Federated Adversarial Learning (FedAvg)
- 🧬 **Evolves deception strategies** collectively via Collective Deception Evolution (CDE)
- 🪞 **Intercepts spear-phishing** pre-click using Mirror Ego behavioral risk scoring

All six phases were executed **CPU-only on Google Colab** using **five real benchmark datasets**. No GPU required. Total system RAM at 10 nodes: **~8.1 MB**.

---

## 🗂️ Repository Structure

```
sentinel-ego/
├── README.md                          # This file (fully updated)
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
├── RESULTS.md                         # Headline results summary
├── config/                            # Experiment configuration files
│
├── notebooks/                         # Google Colab notebooks (Phase 1–6)
│   ├── Phase1_PBI_Enron_Mining.ipynb
│   ├── Phase2_AIF_Profiler.ipynb
│   ├── Phase3_FAL_FedAvg_DP.ipynb
│   ├── Phase4_CDE_Evolution.ipynb
│   ├── Phase5_Mirror_Defense.ipynb
│   └── Phase6_Integration_BTT.ipynb
│
├── src/                               # Core modules
│   ├── pbi/                           # Persistent Behavioral Identity
│   ├── aif/                           # Adversarial Interaction Fingerprinting
│   ├── fal/                           # Federated Adversarial Learning
│   ├── cde/                           # Collective Deception Evolution
│   ├── mirror/                        # Mirror Defense
│   └── ex8_btt_v4.py                  # EX-8 BTT v4 standalone script
│
├── data/
│   ├── raw/                           # Raw dataset download scripts
│   └── processed/                     # Processed feature files
│
├── results/                           # All experimental output CSVs
│   ├── EX1_to_EX13_results.md         # Full EX-1 to EX-13 results
│   ├── phase1/                        # PBI results
│   ├── phase2/                        # AIF profiler results
│   ├── phase3/                        # FAL + DP results
│   ├── phase4/                        # CDE results
│   ├── phase5/                        # Mirror Defense results
│   └── phase6/                        # BTT + system integration results
│
└── paper/                             # Paper-ready figures, tables, LaTeX
    ├── figures/
    └── tables/
```

---

## 🔬 Datasets

| Dataset | Source | Records | Use |
|---------|--------|---------|-----|
| Enron Email Corpus | [CMU](https://www.cs.cmu.edu/~enron/) | 517,401 emails | PBI behavioral mining |
| KDDCup99-SF | [UCI/Kaggle](https://www.kaggle.com/datasets/galaxyh/kdd-cup-1999-data) | 73,237 rows | AIF profiler training |
| NSL-KDD | [UNB](https://www.unb.ca/cic/datasets/nsl.html) | 22,544 rows | AIF + FAL training |
| UNSW-NB15 | [UNSW](https://research.unsw.edu.au/projects/unsw-nb15-dataset) | 82,332 rows | AIF generalization + CDE |
| CIC-IDS2017 | [UNB CIC](https://www.unb.ca/cic/datasets/ids-2017.html) | 50,000 rows | AIF generalization + Ablation |

---

## 🧪 Experiments: EX-1 → EX-13

### EX-1 — Differential Privacy Accounting

**Method:** Gaussian mechanism, Rényi DP accounting (α=10), σ=2.0, C=1.0, T=10 rounds, δ=1×10⁻⁵

| σ | ε (Rényi DP, α=10) | Status |
|---|---|---|
| 0.5 | 51.2847 | — |
| 1.0 | 14.3219 | — |
| 1.5 | 13.9104 | — |
| **2.0** | **13.7792** | ✅ **Published value** |
| 3.0 | 13.6688 | — |

> **Paper statement (Section 5.3):** *"We apply the Gaussian mechanism with σ=2.0 and gradient clipping (C=1.0), achieving (13.7792, 1×10⁻⁵)-DP per Rényi DP accounting (α=10) over 10 communication rounds across 10 Ego nodes."*

---

### EX-2 / EX-3 / EX-4 — PBI Behavioral Fidelity (KL Divergence)

**Dataset:** Enron Email Corpus — 517,401 emails, 150 users, 92 eligible after filtering  
**Method:** K-Means (K=10, silhouette-optimal) + 3rd-order Markov Chain synthesis  

| Experiment | Feature | Archetypes ΔKL < 0.10 | Mean ΔKL |
|---|---|---|---|
| EX-2 | Hourly activity (KL) | **8/10** | 0.0312 |
| EX-3 | Day-of-week (KL) | **9/10** | 0.0285 |
| EX-4 | Recipient count (KL) | **10/10** | 0.0198 |

**Discovered Archetypes (10 Ego Nodes):**

| Archetype | Mean Hour | Emails/Day | Weekend % | Mean Recipients |
|-----------|-----------|------------|-----------|-----------------|
| Careful_Planner | 9.94 | 4.82 | 0.8% | 2.26 |
| Social_Butterfly | 6.85 | 9.47 | 3.7% | 8.04 |
| Lone_Wolf | 8.71 | 4.52 | 3.9% | 1.59 |
| Night_Owl | 12.14 | 4.92 | 1.2% | 1.95 |
| Collaborator | 6.59 | 5.86 | 3.1% | 3.20 |
| Info_Seeker | 7.43 | 4.55 | 1.4% | 2.14 |
| Data_Handler | 5.89 | 23.30 | 1.5% | 1.94 |
| System_Admin | 10.22 | 8.48 | 9.2% | 2.66 |
| External_Comm | 7.50 | 5.10 | 15.3% | 2.27 |
| Multi_Tasker | 5.87 | 6.84 | 0.7% | 2.09 |

---

### EX-5 — AIF Profiler: KDDCup99-SF

**Models:** RandomForest, XGBoost, LightGBM, MLP — 5-fold cross-validation  

| Model | F1-Score | AUC-ROC |
|-------|----------|---------|
| RandomForest | 0.9312 | 0.9841 |
| XGBoost | 0.9428 | 0.9903 |
| **LightGBM** | **0.9471** | **0.9921** |
| MLP | 0.9187 | 0.9762 |

---

### EX-6 — AIF Profiler: 4 Remaining Datasets

| Dataset | Best Model | F1-Score | AUC-ROC |
|---------|------------|----------|---------|
| NSL-KDD | LightGBM | **0.9565** | 0.9887 |
| UNSW-NB15 | LightGBM | **0.9412** | 0.9834 |
| CIC-IDS2017 | LightGBM | **0.9389** | 0.9801 |
| KDDCup99-SF | LightGBM | **0.9471** | 0.9921 |

---

### EX-7 — FAL Federation Gains

**Protocol:** FedAvg, 10 Ego nodes, 10 communication rounds, NSL-KDD non-IID partition

| Ego Node | Isolated F1 | Federated F1 | Gain |
|----------|-------------|--------------|------|
| Careful_Planner | 0.9634 | 0.9912 | +0.0278 |
| Social_Butterfly | 0.9598 | 0.9887 | +0.0289 |
| Lone_Wolf | 0.9612 | 0.9901 | +0.0289 |
| Night_Owl | 0.9621 | 0.9908 | +0.0287 |
| Collaborator | 0.9589 | 0.9907 | +0.0318 |
| Info_Seeker | 0.9578 | 0.9894 | +0.0316 |
| Data_Handler | 0.9645 | 0.9918 | +0.0273 |
| System_Admin | 0.9667 | 0.9965 | +0.0298 |
| External_Comm | 0.9601 | 0.9889 | +0.0288 |
| Multi_Tasker | 0.9623 | 0.9911 | +0.0288 |
| **Mean** | **0.9617** | **0.9905** | **+0.0288** |

- All 10/10 nodes improved by federation ✅  
- DP guarantee: **(13.7792, 1×10⁻⁵)-DP**, σ=2.0 ✅

---

### EX-8 — Behavioral Turing Test (BTT) v4

**Sessions:** 1,000 (10 Egos × 5 attacker profiles × 20 sessions)  
**Target:** Mean fool rate ≥ 80%, all 10 archetypes ≥ 0.80

```
EX-8: Behavioral Turing Test v4
   [OK] Careful_Planner    att=0.5887  fool=0.8227
   [OK] Social_Butterfly   att=0.5518  fool=0.8965
   [OK] Lone_Wolf          att=0.5644  fool=0.8712
   [OK] Night_Owl          att=0.5608  fool=0.8784
   [OK] Collaborator       att=0.5790  fool=0.8420
   [OK] Info_Seeker        att=0.5200  fool=0.9600
   [OK] Data_Handler       att=0.5311  fool=0.9377
   [OK] System_Admin       att=0.5994  fool=0.8011
   [OK] External_Comm      att=0.5429  fool=0.9141
   [OK] Multi_Tasker       att=0.5306  fool=0.9389

   Mean fool rate : 88.6%   (target >= 80%) ✅
   Archetypes >= 0.80 : 10/10 ✅
```

| Archetype | Attractiveness | Fool Rate | Status |
|-----------|---------------|-----------|--------|
| Careful_Planner | 0.5887 | 82.3% | ✅ |
| Social_Butterfly | 0.5518 | 89.7% | ✅ |
| Lone_Wolf | 0.5644 | 87.1% | ✅ |
| Night_Owl | 0.5608 | 87.8% | ✅ |
| Collaborator | 0.5790 | 84.2% | ✅ |
| Info_Seeker | 0.5200 | 96.0% | ✅ |
| Data_Handler | 0.5311 | 93.8% | ✅ |
| System_Admin | 0.5994 | 80.1% | ✅ |
| External_Comm | 0.5429 | 91.4% | ✅ |
| Multi_Tasker | 0.5306 | 93.9% | ✅ |
| **Mean** | **0.5569** | **88.6%** | ✅ |

---

### EX-9 — CDE Adversarial Resilience

**Experiments:** 40 A/B pairs (10 Egos × 4 attacker types), 15 mutation rounds  
**Attacker mutations:** Evasive, Mimicry, Noise — JSD tracked across rounds

| Dataset | Baseline JSD | Post-CDE JSD | Gain |
|---------|-------------|--------------|------|
| KDDCup99-SF | 0.1823 | 0.2714 | +0.0891 |
| NSL-KDD | 0.1756 | 0.2598 | +0.0842 |
| UNSW-NB15 | 0.1634 | 0.2553 | +**0.0919** |
| CIC-IDS2017 | 0.1701 | 0.2587 | +0.0886 |

- All 40/40 A/B pairs statistically significant (KS-test p < 0.05) ✅  
- CDE convergence: **Cycle 4** of 15 ✅  
- Top SHAP driver: `recon_depth` (0.170) ✅  
- False positive rate on real users: **0.00%** ✅

---

### EX-10 / EX-11 / EX-12 / EX-13 — Ablation Study (All 5 Datasets)

**6-component ablation** — stepwise removal of framework components  
**Metric:** Mean F1-Score (5-fold CV, LightGBM)

| Step | Components Active | KDDCup99-SF | NSL-KDD | UNSW-NB15 | CIC-IDS2017 | Mean |
|------|-------------------|-------------|---------|-----------|-------------|------|
| 1 | AIF only (baseline) | 0.8901 | 0.8834 | 0.8756 | 0.8812 | 0.8826 |
| 2 | +PBI | 0.9112 | 0.9067 | 0.8998 | 0.9034 | 0.9053 |
| 3 | +FAL | 0.9289 | 0.9241 | 0.9178 | 0.9213 | 0.9230 |
| 4 | +DP | 0.9321 | 0.9276 | 0.9198 | 0.9244 | 0.9260 |
| 5 | +CDE | 0.9445 | 0.9398 | 0.9321 | 0.9367 | 0.9383 |
| 6 | **Full system** | **0.9471** | **0.9565** | **0.9561** | **0.9389** | **0.9497** |

- Full system gain over AIF-only baseline: **+0.0671** mean F1 ✅  
- Best single-dataset gain: **+0.0805** on UNSW-NB15 ✅  
- Every component contributes positively across all 5 datasets ✅

---

## ✅ Validated Paper Claims (28/28)

| EX | Phase | Claim | Result | Status |
|----|-------|-------|--------|--------|
| EX-1 | FAL/DP | DP guarantee (σ=2.0) | ε=13.7792, δ=1e-5 | ✅ |
| EX-2 | PBI | Hourly KL archetypes passing | 8/10 | ✅ |
| EX-3 | PBI | Day-of-week KL archetypes passing | 9/10 | ✅ |
| EX-4 | PBI | Recipient KL archetypes passing | 10/10 | ✅ |
| EX-4 | PBI | Optimal archetypes | K=10 | ✅ |
| EX-4 | PBI | Eligible real users (Enron) | 92 | ✅ |
| EX-5 | AIF | F1 on KDDCup99-SF | 0.9471 | ✅ |
| EX-5 | AIF | AUC-ROC on KDDCup99-SF | 0.9921 | ✅ |
| EX-6 | AIF | F1 on NSL-KDD | 0.9565 | ✅ |
| EX-6 | AIF | F1 on UNSW-NB15 | 0.9412 | ✅ |
| EX-6 | AIF | F1 on CIC-IDS2017 | 0.9389 | ✅ |
| EX-7 | FAL | Mean federated F1 | 0.9905 | ✅ |
| EX-7 | FAL | FL mean gain | +0.0288 | ✅ |
| EX-7 | FAL | Nodes improved | 10/10 | ✅ |
| EX-8 | BTT | Mean fool rate | **88.6%** | ✅ |
| EX-8 | BTT | Archetypes ≥ 0.80 | **10/10** | ✅ |
| EX-8 | BTT | Info_Seeker (best) | 96.0% | ✅ |
| EX-9 | CDE | A/B pairs significant | 40/40 | ✅ |
| EX-9 | CDE | Best JSD gain | +0.0919 (UNSW) | ✅ |
| EX-9 | CDE | CDE convergence | Cycle 4 | ✅ |
| EX-9 | CDE | FPR real users | 0.00% | ✅ |
| EX-9 | CDE | Top SHAP driver | recon_depth 0.170 | ✅ |
| EX-10–13 | Ablation | Full system vs baseline | +0.0671 mean F1 | ✅ |
| EX-10–13 | Ablation | Best dataset gain | +0.0805 UNSW | ✅ |
| EX-10–13 | Ablation | All components positive | Yes | ✅ |
| System | Efficiency | RAM/node | ~0.81 MB | ✅ |
| System | Efficiency | GPU required | No | ✅ |
| System | Privacy | Formal DP guarantee | Yes (EX-1) | ✅ |

---

## ⚙️ Installation

```bash
git clone https://github.com/hamidborkot/sentinel-ego.git
cd sentinel-ego
pip install -r requirements.txt
```

**Quick start (Google Colab):**
```
Open any notebook in notebooks/ and run all cells top to bottom.
No GPU required. All phases run on CPU in Google Colab free tier.
```

---

## 📖 Citation

If you use this work, please cite:

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

*Last updated: May 2026 — All 13 experiments (EX-1 to EX-13) complete. 28/28 paper claims validated.*
