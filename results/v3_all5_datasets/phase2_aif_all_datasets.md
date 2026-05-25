# Phase 2 — AIF: 5-Fold CV Model Performance (All 5 Datasets)

**Runner:** v3 | **Models:** RandomForest, XGBoost, LightGBM, MLP

---

## KDDCup99-SF  
`n=73,237 | attack ratio=0.050 | ⚠️ Legacy benchmark — ceiling effect`

| Model | F1 Mean | F1 Std | AUC | Precision | Recall |
|---|---|---|---|---|---|
| **RandomForest** | **0.9471** | **±0.0034** | **0.9536** | **0.9954** | **0.9033** |
| XGBoost | 0.9471 | ±0.0034 | 0.9510 | 0.9954 | 0.9033 |
| LightGBM | 0.9471 | ±0.0034 | 0.9513 | 0.9954 | 0.9033 |
| MLP | 0.9410 | ±0.0035 | 0.9503 | 0.9821 | 0.9033 |

---

## NSL-KDD  
`n=22,544 | attack ratio=0.567 | ⚠️ Retired benchmark`

| Model | F1 Mean | F1 Std | AUC | Precision | Recall |
|---|---|---|---|---|---|
| RandomForest | 0.9425 | ±0.0023 | 0.9829 | 0.9894 | 0.8998 |
| XGBoost | 0.9550 | ±0.0018 | 0.9847 | 0.9864 | 0.9256 |
| **LightGBM** | **0.9565** | **±0.0025** | **0.9848** | **0.9867** | **0.9281** |
| MLP | 0.9493 | ±0.0023 | 0.9768 | 0.9481 | 0.9506 |

---

## NetIntrusion  
`n=25,000 | attack ratio=0.467`

| Model | F1 Mean | F1 Std | AUC | Precision | Recall |
|---|---|---|---|---|---|
| RandomForest | 0.9313 | ±0.0027 | 0.9815 | 0.9846 | 0.8836 |
| XGBoost | 0.9520 | ±0.0025 | 0.9830 | 0.9840 | 0.9220 |
| **LightGBM** | **0.9528** | **±0.0021** | **0.9831** | **0.9832** | **0.9244** |
| MLP | 0.9507 | ±0.0028 | 0.9767 | 0.9487 | 0.9528 |

---

## CICIDS2017  ✅ Primary benchmark
`n=150,000 | attack ratio=0.462`

| Model | F1 Mean | F1 Std | AUC | Precision | Recall |
|---|---|---|---|---|---|
| RandomForest | 0.9206 | ±0.0020 | 0.9759 | 0.9797 | 0.8683 |
| **XGBoost** | **0.9448** | **±0.0012** | **0.9767** | **0.9761** | **0.9154** |
| LightGBM | 0.9443 | ±0.0015 | 0.9767 | 0.9765 | 0.9141 |
| MLP | 0.9314 | ±0.0035 | 0.9517 | 0.9284 | 0.9345 |

---

## UNSW-NB15  ✅ Primary benchmark
`n=100,000 | attack ratio=0.326`

| Model | F1 Mean | F1 Std | AUC | Precision | Recall |
|---|---|---|---|---|---|
| RandomForest | 0.8671 | ±0.0040 | 0.9533 | 0.9865 | 0.7735 |
| XGBoost | 0.8852 | ±0.0038 | 0.9594 | 0.9771 | 0.8091 |
| **LightGBM** | **0.8856** | **±0.0038** | **0.9598** | **0.9791** | **0.8085** |
| MLP | 0.8441 | ±0.0029 | 0.9235 | 0.8409 | 0.8476 |
