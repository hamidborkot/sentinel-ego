# SENTINEL-EGO — Experimental Results

> **Paper**: SENTINEL-EGO: Federated Behavioral Intelligence for Privacy-Preserving Insider Threat Detection
> **Venue**: IEEE Transactions on Information Forensics and Security (TIFS)
> **Author**: MD Hamid Borkot Tulla, Université de Bourgogne

---

## Table II — AIF Detection Performance and FAL Federation Gains

5-Fold CV, K=10 Nodes, R=10 Rounds, (1.28, 1e-5)-DP
Best Model = top-performing classifier per dataset.

| Dataset | Best Model | F1 | Std | AUC | Prec | Rec | Isolated | Federated |
|---|---|---|---|---|---|---|---|---|
| CICIDS2017 | XGBoost | 0.9448 | 0.0012 | 0.9767 | 0.9761 | 0.9154 | 0.9210 | 0.9306 |
| KDDCup99-SF | RF | 0.9471 | 0.0034 | 0.9536 | 0.9954 | 0.9033 | 0.9638 | 0.9661 |
| NSL-KDD | LightGBM | 0.9565 | 0.0025 | 0.9848 | 0.9867 | 0.9281 | 0.9538 | 0.9791 |
| NetIntrusion | LightGBM | 0.9528 | 0.0021 | 0.9831 | 0.9832 | 0.9244 | 0.9395 | 0.9692 |
| UNSW-NB15 | LightGBM | 0.8856 | 0.0038 | 0.9598 | 0.9791 | 0.8085 | 0.8952 | 0.8978 |
| **CERT r4.2** | **DP-FedProto** | **0.4812** | **0.0617** | **0.9160** | **0.6180** | **0.3670** | **0.0457** | **0.4812** |

> Source: `results/v5_final/cert_r42_fedproto_results.csv` — exact 5-fold CV output, seed=42, q=0.01, σ=2.0, (1.28, 1e-5)-DP. No SMOTE. Consistent with all other experiments.

---

## CERT r4.2 — Version Record

| Version | F1 | Std | Isolated | Gap Closed | q | DP | Status |
|---|---|---|---|---|---|---|---|
| v5 | **0.4812** | **0.0617** | **0.0457** | **57.6%** | 0.01 | (1.28, 1e-5) | ✅ Confirmed — used in paper |
| v6 | not confirmed | — | 0.000 | — | 0.05 | (1.90, 1e-5) | ❌ Not used — breaks DP consistency |

**v5 is the paper version.** v6 was a development branch that raised q=0.05 and added SMOTE, changing the DP budget to ε=1.90 and breaking uniformity with all other experiments. v5 uses identical hyperparameters (q=0.01, σ=2.0, seed=42) across all six datasets.

---

## Table III — Differential Privacy Accounting

(ε, 1e-5)-DP, α=10, K=10, R=10, q=0.01

| σ | RDP(α=10) | ε | Assessment |
|---|---|---|---|
| 0.5 | 0.200 | 3.28 | Weak |
| 1.0 | 0.050 | 1.33 | Acceptable |
| 1.5 | 0.022 | 1.29 | Good |
| **2.0** | **0.00125** | **1.28** | **Operational** |
| 3.0 | 0.00056 | 1.28 | Strong |

---

## Table IV — Ablation Study (CICIDS2017)

| Config | Macro-F1 | ΔF1 | Gain Source |
|---|---|---|---|
| Legacy IDS baseline | 0.8989 | — | — |
| + PBI module | 0.9168 | +0.0179 | Persona stability filtering |
| + AIF module | 0.9489 | +0.0321 | Intent fingerprinting (dominant) |
| + FAL module | 0.9502 | +0.0013 | Federated generalisation |
| **Full SENTINEL-EGO** | **0.9502** | **+0.0513** | **End-to-end pipeline** |

---

## Table V — Leave-One-Out Ablation

| Configuration | CICIDS F1 | UNSW F1 | Δ vs Full |
|---|---|---|---|
| Full pipeline | 0.9502 | 0.8896 | — |
| Full − PBI | 0.9381 | 0.8712 | −0.0121, −0.0184 |
| Full − AIF | 0.9168 | 0.8091 | −0.0334, −0.0805 |
| Full − FAL | 0.9489 | 0.8869 | −0.0013, −0.0027 |
| Full − CDE | 0.9606 | 0.9012 | +0.0104, +0.0116 |
| Legacy only | 0.8989 | 0.8091 | −0.0513, −0.0805 |

---

## CDE Adversarial Resilience (15 Rounds)

| Dataset | SENTINEL-EGO F1 trough | Legacy IDS F1 trough | Advantage |
|---|---|---|---|
| CICIDS2017 | 0.9187 | 0.8340 | +0.0847 |
| KDDCup99-SF | 0.9448 | 0.8901 | +0.0547 |
| NSL-KDD | 0.9327 | 0.8512 | +0.0815 |
| NetIntrusion | 0.9215 | 0.8476 | +0.0739 |
| **UNSW-NB15** | **0.8584** | **0.7665** | **+0.0919** |

---

## BTT Fool Rates — All 10 Archetypes

| Archetype | Attacker Acc. | Fool Rate | Pass (≥0.80) |
|---|---|---|---|
| Morning Bird | 0.5887 | 0.8227 | ✓ |
| Social Butterfly | 0.5518 | 0.8965 | ✓ |
| Lone Wolf | 0.5644 | 0.8712 | ✓ |
| Night Owl | 0.5608 | 0.8784 | ✓ |
| Collaborator | 0.5790 | 0.8420 | ✓ |
| Info Seeker | 0.5200 | 0.9600 | ✓ |
| Balanced | 0.5311 | 0.9377 | ✓ |
| Workaholic | 0.5994 | 0.8011 | ✓ |
| Tech Savvy | 0.5429 | 0.9141 | ✓ |
| Careful Planner | 0.5306 | 0.9389 | ✓ |
| **Mean** | **0.5569** | **0.8863** | **10/10** |

---

## Reproducibility

| Item | Value |
|---|---|
| Python | 3.10 |
| scikit-learn | 1.3 |
| LightGBM | 4.x |
| PyTorch | 2.1 |
| Random seed | 42 (all folds, all models) |
| Hardware | Intel Core i7, 32 GB RAM |

All experiments use stratified 5-fold CV with fixed seed=42, q=0.01, σ=2.0, K=10, R=10.
All results are exact confirmed outputs. No estimated values.
