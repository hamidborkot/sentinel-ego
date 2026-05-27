# 🛡️ The Sentinel Ego

> **A Federated Adversarial Deception Framework for Insider Threat Detection**  
> IEEE Transactions on Information Forensics and Security (TIFS) — 2026 Submission

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-CPU--Only%20%7C%20Google%20Colab-orange?logo=googlecolab)](https://colab.research.google.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Phase](https://img.shields.io/badge/Pipeline-Phase%201--5%20Complete-brightgreen)](#pipeline-phases-1--5)
[![Datasets](https://img.shields.io/badge/Datasets-5%20Benchmarks-blue)](#-datasets)
[![KL](https://img.shields.io/badge/KL%20Consistency-0.0245%20%3C%200.30-brightgreen)](#table-v--phase-1-90-day-kl-consistency)
[![F1](https://img.shields.io/badge/Best%20F1-0.9993%20(NSL--KDD)-brightgreen)](#table-i--phase-2-best-aif-model-per-dataset)
[![DP](https://img.shields.io/badge/Differential%20Privacy-%CE%B5%3D51.28%20(%CF%83%3D1.0)-purple)](#table-ii--phase-3-federated-learning)

---

## 📋 Overview

The **Sentinel Ego** is a novel cybersecurity framework of ten persistent synthetic employee personas ("Ego nodes"), each possessing a unique behavioral identity grounded in real Enron email data. Together they form a federated honeypot collective that:

- 🎭 **Deceives attackers** using behaviorally realistic, temporally consistent synthetic identities
- 🔍 **Profiles adversaries** via a 42-feature Adversarial Interaction Fingerprint (AIF)
- 🤝 **Shares threat intelligence** through privacy-preserving Federated Adversarial Learning (FedAvg + DP)
- 🧬 **Evolves deception strategies** via Collective Deception Evolution (CDE) across 15 mutation rounds
- 🪞 **Intercepts spear-phishing** pre-click using Mirror Ego behavioral risk scoring

**Full pipeline validated on 5 real benchmark datasets** — CPU-only, Google Colab compatible. No GPU required.

---

## 🗂️ Repository Structure

```
sentinel-ego/
├── README.md                                    # This file
├── LICENSE
├── requirements.txt
├── RESULTS.md
├── config/
│
├── notebooks/
│   ├── pipeline_phases1to5_all5datasets.py      # ✅ Complete reproducible pipeline (NEW)
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
│   └── mirror/                                  # Mirror Defense
│
├── figures/                                     # 8 publication-ready figures (300 DPI)
│   ├── fig1_silhouette.png
│   ├── fig2_kl_consistency.png
│   ├── fig3_aif_heatmap.png
│   ├── fig4_federation_nodes.png
│   ├── fig5_cde_evolution.png
│   ├── fig6_drs_heatmap.png
│   ├── fig7_mirror_cv.png
│   └── fig8_ablation.png
│
├── results/
│   ├── EX1_to_EX13_results.md
│   ├── phase1/ | phase2/ | phase3/ | phase4/ | phase5/
│   ├── v2_cicids_unsw/
│   └── v3_all5_datasets/                        # ✅ Full pipeline CSVs (NEW)
│       ├── README.md
│       ├── phase1_kl_90day_fixed.csv
│       ├── phase2_aif_all5.csv
│       ├── phase3_federation_all5.csv
│       ├── phase4_cde_evolution_all5.csv
│       ├── phase4_drs_scores_all5.csv
│       ├── phase5_5fold_cv_all5.csv
│       ├── phase5_ablation_nslkdd.csv
│       └── phase5_mirror_defense_all5.csv
│
└── data/
    ├── raw/
    └── processed/
```

---

## 🔬 Datasets

| Dataset | Source | Rows | Features | Attack Rate |
|---------|--------|------|----------|-------------|
| KDDCup99-SF | [Kaggle](https://www.kaggle.com/datasets/galaxyh/kdd-cup-1999-data) | 73,237 | 5 | 4.5% |
| NSL-KDD | [UNB](https://www.unb.ca/cic/datasets/nsl.html) | 125,973 | 42 | 46.5% |
| NetIntrusion | UCI | 25,000 | 42 | 80.1% |
| CICIDS2017 | [UNB CIC](https://www.unb.ca/cic/datasets/ids-2017.html) | 56,661 | 78 | 59.9% |
| UNSW-NB15 | [UNSW](https://research.unsw.edu.au/projects/unsw-nb15-dataset) | 82,332 | 43 | 55.1% |
| Enron Email | [CMU](https://www.cs.cmu.edu/~enron/) | 517,401 emails | — | PBI mining |

> All datasets are **real, raw network traffic** — no synthetic data used.

---

## Pipeline: Phases 1 – 5

### TABLE I — Phase 2: Best AIF Model per Dataset

| Dataset | Best Model | F1-Score | AUC-ROC |
|---------|------------|----------|---------|
| KDDCup99-SF | RandomForest | 0.9992 | 1.0000 |
| NSL-KDD | LightGBM | **0.9993** | 1.0000 |
| NetIntrusion | XGBoost | 0.9990 | 1.0000 |
| CICIDS2017 | LightGBM | 0.9972 | 0.9996 |
| UNSW-NB15 | LightGBM | 0.9802 | 0.9982 |

> Full 4-model × 5-dataset results: [`results/v3_all5_datasets/phase2_aif_all5.csv`](results/v3_all5_datasets/phase2_aif_all5.csv)

---

### TABLE II — Phase 3: Federated Learning

| Dataset | Mean Node Gain | Max Node Gain | DP ε (σ=1.0) | DP ε (σ=0.5) |
|---------|---------------|--------------|--------------|--------------|
| KDDCup99-SF | −0.022% | +0.150% | 51.2792 | 201.2792 |
| NSL-KDD | −0.016% | +0.210% | 51.2792 | 201.2792 |
| NetIntrusion | +0.057% | +0.160% | 51.2792 | 201.2792 |
| CICIDS2017 | +0.010% | +0.150% | 51.2792 | 201.2792 |
| UNSW-NB15 | +0.065% | +0.170% | 51.2792 | 201.2792 |

> δ = 1×10⁻⁵ for all. Full per-node data: [`results/v3_all5_datasets/phase3_federation_all5.csv`](results/v3_all5_datasets/phase3_federation_all5.csv)

---

### TABLE III — Phase 4: CDE Evasion Impact

| Dataset | Base F1 | Final DetF1 | Impact | Peak JSD | Mean DRS |
|---------|---------|-------------|--------|----------|----------|
| KDDCup99-SF | 0.9995 | 0.9538 | −0.0457 | 0.5222 | 0.7093 |
| NSL-KDD | 0.9989 | 0.7222 | −0.2767 | 0.4413 | 0.6722 |
| NetIntrusion | 0.9998 | 0.5506 | −0.4492 | 0.5518 | 0.6430 |
| CICIDS2017 | 0.9979 | 0.2313 | **−0.7666** | 0.4132 | **0.9382** |
| UNSW-NB15 | 0.9794 | 0.9774 | −0.0020 | 0.3749 | 0.5219 |

> 15-round CDE evolution: [`results/v3_all5_datasets/phase4_cde_evolution_all5.csv`](results/v3_all5_datasets/phase4_cde_evolution_all5.csv)  
> DRS per archetype × dataset: [`results/v3_all5_datasets/phase4_drs_scores_all5.csv`](results/v3_all5_datasets/phase4_drs_scores_all5.csv)

---

### TABLE IV — Phase 5: 5-Fold CV (LightGBM, Best per Dataset)

| Dataset | F1 Mean | F1 Std | AUC Mean |
|---------|---------|--------|----------|
| KDDCup99-SF | 0.9995 | ±0.0001 | 0.9998 |
| NSL-KDD | 0.9991 | ±0.0003 | 1.0000 |
| NetIntrusion | 0.9993 | ±0.0002 | 1.0000 |
| CICIDS2017 | 0.9979 | ±0.0003 | 0.9998 |
| UNSW-NB15 | 0.9801 | ±0.0003 | 0.9980 |

> Full 3-model × 5-dataset CV: [`results/v3_all5_datasets/phase5_5fold_cv_all5.csv`](results/v3_all5_datasets/phase5_5fold_cv_all5.csv)

---

### TABLE V — Phase 1: 90-Day KL Consistency (10 Archetypes)

| Archetype | KL Hour | KL DOW | KL Rcpt | KL Mean | Status |
|-----------|---------|--------|---------|---------|--------|
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

> **Overall Mean KL = 0.0245** — All 10/10 archetypes below threshold 0.30 ✅  
> **Claim SUPPORTED:** Behavioral identity persists across 90-day observation window  
> Source: [`results/v3_all5_datasets/phase1_kl_90day_fixed.csv`](results/v3_all5_datasets/phase1_kl_90day_fixed.csv)

---

### TABLE VI — Phase 5: Ablation Study (NSL-KDD)

| Component | F1 | AUC | ΔF1 |
|-----------|----|-----|-----|
| W/o Sentinel (Legacy IDS) | 0.9744 | 0.9987 | — |
| + PBI Behavioral Context | 0.9989 | 1.0000 | +0.0245 |
| + AIF 42-Feature Profiling | 0.9989 | 1.0000 | +0.0245 |
| + FAL Federation (10 nodes) | 0.9990 | 1.0000 | +0.0246 |
| + CDE Evasion-Aware | 0.9990 | 1.0000 | +0.0246 |
| **Full Pipeline (all components)** | **0.9988** | **1.0000** | **+0.0244** |

> PBI alone delivers the largest single jump (+0.0245 F1 over Legacy IDS baseline).  
> Source: [`results/v3_all5_datasets/phase5_ablation_nslkdd.csv`](results/v3_all5_datasets/phase5_ablation_nslkdd.csv)

---

### Mirror Defense (Phase 5)

| Dataset | Base F1 | Mirror F1 | Δ |
|---------|---------|-----------|---|
| KDDCup99-SF | 0.9995 | 0.9996 | +0.0001 |
| NSL-KDD | 0.9989 | 0.9988 | −0.0001 |
| NetIntrusion | 0.9998 | 0.9996 | −0.0002 |
| CICIDS2017 | 0.9979 | 0.9978 | −0.0001 |
| UNSW-NB15 | 0.9794 | 0.9794 | +0.0001 |

> Mirror Defense has negligible performance impact (max Δ = ±0.0002) while providing pre-click spear-phishing interception.  
> Source: [`results/v3_all5_datasets/phase5_mirror_defense_all5.csv`](results/v3_all5_datasets/phase5_mirror_defense_all5.csv)

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

*Last updated: May 2026 — Full pipeline (Phase 1–5) complete across all 5 datasets. All 6 paper tables validated. 8 publication-ready figures generated.*
