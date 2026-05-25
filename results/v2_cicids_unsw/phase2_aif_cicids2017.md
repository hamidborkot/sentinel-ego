# AIF Phase 2 — CICIDS2017

**Runner:** v2 (CICIDS2017 + UNSW-NB15)  
**Shape:** (150000, 42) | **Attack ratio:** 0.462

## Model Performance (5-Fold CV)

| Model | F1 Mean | F1 Std | AUC | Precision | Recall |
|---|---|---|---|---|---|
| RandomForest | 0.9209 | ±0.0006 | 0.9757 | 0.9800 | 0.8684 |
| **XGBoost** | **0.9451** | **±0.0008** | **0.9767** | **0.9766** | **0.9155** |
| LightGBM | 0.9442 | ±0.0010 | 0.9767 | 0.9764 | 0.9140 |
| MLP | 0.9308 | ±0.0043 | 0.9520 | 0.9236 | 0.9380 |

> **Best model:** XGBoost — F1=0.9451 ± 0.0008
