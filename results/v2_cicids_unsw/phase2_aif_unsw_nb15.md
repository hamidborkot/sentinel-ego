# AIF Phase 2 — UNSW-NB15

**Runner:** v2 (CICIDS2017 + UNSW-NB15)  
**Shape:** (100000, 42) | **Attack ratio:** 0.325

## Model Performance (5-Fold CV)

| Model | F1 Mean | F1 Std | AUC | Precision | Recall |
|---|---|---|---|---|---|
| RandomForest | 0.8709 | ±0.0033 | 0.9542 | 0.9848 | 0.7807 |
| **XGBoost** | **0.8860** | **±0.0036** | **0.9602** | **0.9769** | **0.8106** |
| LightGBM | 0.8859 | ±0.0030 | 0.9603 | 0.9781 | 0.8096 |
| MLP | 0.8437 | ±0.0055 | 0.9265 | 0.8370 | 0.8505 |

> **Best model:** XGBoost — F1=0.8860 ± 0.0036
