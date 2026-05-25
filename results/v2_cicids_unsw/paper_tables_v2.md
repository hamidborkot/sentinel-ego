# Paper Tables — Runner v2 (CICIDS2017 + UNSW-NB15)

> Source: `THE SENTINEL EGO — FULL EXPERIMENT RUNNER v2`  
> Use **v3 tables** for final IEEE TIFS submission. These are the v2 reference run.

---

## Table: Cross-Dataset AIF Results (Best Model)

| Dataset | Model | F1 Mean | F1 Std | AUC | Precision | Recall |
|---|---|---|---|---|---|---|
| CICIDS2017 | XGBoost | 0.945067 | 0.000820 | 0.976722 | 0.976650 | 0.915463 |
| UNSW-NB15 | XGBoost | 0.886021 | 0.003649 | 0.960156 | 0.976886 | 0.810633 |

---

## Table: Federation Gains

| Dataset | Isolated Mean | Federated Mean | Mean Gain | Best Node Gain |
|---|---|---|---|---|
| CICIDS2017 | 0.9257 | 0.9371 | +0.0113 | +0.0387 |
| UNSW-NB15 | 0.9000 | 0.9027 | +0.0026 | +0.0243 |

---

## Table: CDE Adversarial Resilience (Core Claim)

| Dataset | Baseline | Sentinel Trough | Legacy Trough | Peak JSD | Advantage |
|---|---|---|---|---|---|
| CICIDS2017 | 0.9499 | 0.9201 | 0.9000 | 0.1320 | **+0.0201** |
| UNSW-NB15 | 0.8938 | 0.8678 | 0.7733 | 0.1814 | **+0.0945** |
