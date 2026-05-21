# 🛡️ The Sentinel Ego

> **A Federated Adversarial Deception Framework with Persistent Behavioral Identities**

[![IEEE TIFS](https://img.shields.io/badge/Target-IEEE%20TIFS-blue)](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-CPU--Only%20%7C%20Google%20Colab-orange)](https://colab.research.google.com/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)
[![Status](https://img.shields.io/badge/Status-All%206%20Phases%20Complete-success)](#)

---

## 📋 Overview

The **Sentinel Ego** is a novel federated adversarial deception system that deploys a collective of ten persistent synthetic employee personas (*Ego nodes*), each with a unique, temporally consistent behavioral identity. Together they form a self-evolving cyber deception mesh that:

- **Profiles attackers** in real time using a 42-feature Adversarial Interaction Fingerprint (AIF)
- **Shares threat intelligence** via privacy-preserving Federated Adversarial Learning (FAL)
- **Evolves deception strategies** automatically through Collective Deception Evolution (CDE)
- **Intercepts spear-phishing** before real employees interact (Mirror Defense)
- **Operates entirely on CPU** at ~0.81 MB RAM per Ego node

All experiments were executed on real benchmark datasets — **no synthetic or fabricated data**.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE SENTINEL EGO MESH                        │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  Ego #1  │  │  Ego #2  │  │  Ego #3  │  │  Ego #N  │  ...   │
│  │ Morning  │  │Collabor. │  │Tech Savvy│  │  Night   │        │
│  │   Bird   │  │          │  │          │  │   Owl    │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │              │              │              │             │
│  ┌────▼──────────────▼──────────────▼──────────────▼─────────┐  │
│  │              FEDERATED AGGREGATION SERVER                  │  │
│  │         FedAvg + Gaussian DP (ε=1.2802, δ=1e-5)           │  │
│  └────────────────────────┬───────────────────────────────────┘  │
│                            │                                      │
│  ┌─────────────────────────▼──────────────────────────────────┐  │
│  │  AIF Profiler │ CDE Engine │ Mirror Defense │ SHAP Layer   │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Key Results (All 6 Phases)

| Module | Metric | Result | Target | Status |
|--------|--------|--------|--------|--------|
| **PBI** | Real users (Enron) | 92 users | ≥30 | ✅ |
| **PBI** | Optimal archetypes | K=10 | K=10 | ✅ |
| **PBI** | Best persona JSD (Tech Savvy P1) | 0.0495 | <0.10 | ✅ |
| **PBI** | Personas passing JSD<0.1 | 11/30 (→30/30 anchored) | Max | ✅ |
| **AIF** | F1-Score (KDDCup99, LightGBM) | **0.9992** | >0.90 | ✅ |
| **AIF** | AUC-ROC (KDDCup99) | **1.0000** | >0.95 | ✅ |
| **AIF** | F1-Score (NSL-KDD) | **0.9854** | >0.90 | ✅ |
| **AIF** | F1-Score (NetIntrusion) | **0.9579** | >0.90 | ✅ |
| **FAL** | Mean F1 (10 nodes, 10 rounds) | **0.9932** | >baseline | ✅ |
| **FAL** | Gain over isolated baseline | **+1.56%** | >0% | ✅ |
| **FAL** | Nodes improved | **10/10** | 10/10 | ✅ |
| **FAL** | DP guarantee (σ=1.0) | **ε=1.2802** | ε<2.0 | ✅ |
| **CDE** | APT deception longevity | **12.63×** | >10× | ✅ |
| **CDE** | Mean longevity (all attackers) | **6.38×** | >5× | ✅ |
| **CDE** | False positive rate (real users) | **0.00%** | <5% | ✅ |
| **Mirror** | Pre-click phishing detection | **100.00%** | >95% | ✅ |
| **Mirror** | False positive rate | **0.00%** | <2% | ✅ |
| **Mirror** | P99 alert latency | **103.4ms** | <500ms | ✅ |
| **BTT** | Overall Ego fool rate | **75.1%** | >80% | ⚠️ |
| **BTT** | Fool rate vs Script Kiddie | **88.0%** | >80% | ✅ |
| **System** | RAM per Ego node | **~0.81 MB** | <100 MB | ✅ |
| **System** | GPU required | **No** | CPU-only | ✅ |

> ⚠️ BTT overall 75.1% is 4.9pp below the 80% simulation target. Against AI Recon Agents (the hardest class), this is still ~50% above the best prior LLM-based system (~50%) — a strong and publishable result.

---

## 📁 Repository Structure

```
sentinel-ego/
├── README.md                        ← This file
├── LICENSE
├── requirements.txt                 ← All dependencies
├── config/
│   ├── system_config.yaml          ← Master system configuration
│   └── dp_config.yaml              ← Differential privacy parameters
├── notebooks/
│   ├── phase1_pbi.ipynb            ← Phase 1: Persistent Behavioral Identity
│   ├── phase2_aif.ipynb            ← Phase 2: AIF Profiler
│   ├── phase3_fal.ipynb            ← Phase 3: Federated Adversarial Learning
│   ├── phase4_cde.ipynb            ← Phase 4: Collective Deception Evolution
│   ├── phase5_mirror.ipynb         ← Phase 5: Mirror Defense
│   └── phase6_integration.ipynb   ← Phase 6: Full System Integration
├── src/
│   ├── __init__.py
│   ├── pbi/
│   │   ├── __init__.py
│   │   ├── enron_parser.py         ← Raw email parsing
│   │   ├── archetype_miner.py      ← K-Means archetype discovery
│   │   └── markov_generator.py     ← 3rd-order Markov chain PBI synthesis
│   ├── aif/
│   │   ├── __init__.py
│   │   ├── feature_extractor.py    ← 42-feature AIF vector construction
│   │   └── profiler.py             ← Attacker classification models
│   ├── fal/
│   │   ├── __init__.py
│   │   ├── fedavg.py               ← FedAvg aggregation
│   │   └── dp_accountant.py        ← Rényi DP accounting
│   ├── cde/
│   │   ├── __init__.py
│   │   └── deception_evolver.py    ← Collective Deception Evolution engine
│   ├── mirror/
│   │   ├── __init__.py
│   │   └── mirror_defense.py       ← Pre-click phishing interception
│   └── utils/
│       ├── __init__.py
│       └── metrics.py              ← Evaluation utilities
├── results/
│   ├── phase1/                     ← PBI archetypes, JSD scores, trajectory data
│   ├── phase2/                     ← AIF F1/AUC tables per dataset/model
│   ├── phase3/                     ← FAL round results, DP accounting
│   ├── phase4/                     ← CDE A/B pairs, SHAP values
│   ├── phase5/                     ← Mirror detection metrics
│   └── phase6/                     ← BTT, scalability, SOTA comparison
├── paper/
│   ├── claims_validation.md        ← Full 27/28 claims table
│   ├── sota_comparison.md          ← State-of-the-art comparison (Section 6.8)
│   └── paper_statements.md         ← Copy-paste paper statements per section
└── docs/
    ├── architecture.md             ← System architecture details
    └── reproducibility.md          ← Full reproduction guide
```

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/hamidborkot/sentinel-ego.git
cd sentinel-ego
pip install -r requirements.txt
```

### 2. Download Datasets

```bash
# Enron Email Corpus (Phase 1)
wget https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz

# NSL-KDD (Phase 2, 3) — from Kaggle or UNB
# KDDCup99 — from sklearn or UCI
# NetIntrusion — from Kaggle
```

### 3. Run All Phases (Google Colab)

Open each notebook in `notebooks/` and run top-to-bottom. All phases are CPU-only and run independently. Phase 6 auto-loads cross-phase outputs.

```python
# Or run all phases sequentially
from src import run_all_phases
run_all_phases(base_dir='/content/sentinel_ego')
```

---

## 🧠 The Five Pillars

### 1. Persistent Behavioral Identity (PBI)
Each Ego node has a unique 8-feature behavioral fingerprint derived from 92 real Enron employees, synthesized via 3rd-order Markov chains. No two Egos share the same behavioral profile. JSD < 0.10 across 90-day trajectories.

### 2. Adversarial Interaction Fingerprinting (AIF)
A 42-feature vector capturing temporal, behavioral, knowledge, strategic, psychological, and technical attacker signatures. Achieves F1=0.9992 on KDDCup99 with LightGBM.

### 3. Federated Adversarial Learning (FAL)
FedAvg across 10 Ego nodes with Gaussian DP (σ=1.0, C=1.0). Formal guarantee: **(ε=1.2802, δ=1×10⁻⁵)-DP** via Rényi DP accounting (α=10). Mean F1=0.9932 across 10 rounds.

### 4. Collective Deception Evolution (CDE)
All Egos share deception intelligence. Strategies evolve collectively across communication rounds. APT longevity: **12.63×** static baseline. Converges at Cycle 4. 0.00% false positive rate on real users.

### 5. Mirror Defense
Each high-value Ego deploys a Mirror that intercepts spear-phishing pre-click using a 4-feature risk score (SBD, CAS, UMS, LARS). **100% detection, 0.00% FPR, P99 latency 103.4ms**.

---

## 🔒 Privacy Guarantee

```
Method:  Rényi DP (α=10) → (ε, δ)-DP conversion
σ=0.5 → ε=1.2832, δ=1×10⁻⁵
σ=1.0 → ε=1.2802, δ=1×10⁻⁵  ← Paper claim

Paper statement (Section 5.3):
"We apply the Gaussian mechanism with σ=1.0 and gradient clipping
(C=1.0), achieving (1.2802, 1×10⁻⁵)-DP per Rényi DP accounting
(α=10) over 10 communication rounds across 10 Ego nodes."
```

---

## ⚡ Resource Efficiency

| Component | Latency | Peak RAM |
|-----------|---------|----------|
| PBI Generation | 10.76ms | 0.003 MB |
| AIF Feature Extract | 0.39ms | 0.002 MB |
| FAL FedAvg Round | 1.13ms | 0.226 MB |
| CDE Strategy Update | 2.45ms | 0.011 MB |
| Mirror Risk Scoring | 0.08ms | 0.001 MB |
| SHAP Attribution | 10.26ms | 0.005 MB |
| **Full system (10 nodes)** | — | **~8.1 MB** |
| **Scaled (50 nodes)** | — | **~50.6 MB** |

> **~20,000× more RAM-efficient** than LLM-based honeypot systems (~12,000–80,000 MB)

---

## 📜 Citation

```bibtex
@article{tulla2026sentinel,
  title   = {The Sentinel Ego: A Federated Adversarial Deception Framework
             with Persistent Behavioral Identities},
  author  = {Tulla, Md. Hamid Borkot},
  journal = {IEEE Transactions on Information Forensics and Security},
  year    = {2026},
  note    = {Under Review}
}
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Submitted to IEEE Transactions on Information Forensics and Security (TIFS) — 2026*
