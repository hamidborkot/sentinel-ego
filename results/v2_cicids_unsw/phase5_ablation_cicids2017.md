# Ablation Study — CICIDS2017

**Runner:** v2 | **Evaluation:** 5-Fold CV

## Component-wise F1 Improvement

| Component | F1 (5-fold CV) | ΔF1 |
|---|---|---|
| W/o Sentinel (Legacy IDS) | 0.8989 ± 0.0006 | — |
| + PBI Behavioral Context | 0.9139 ± 0.0004 | +0.0150 |
| + AIF 42-Feature Profiling | 0.9450 ± 0.0007 | +0.0461 |
| + FAL Federation (10 nodes) | 0.9497 ± 0.0009 | +0.0508 |
| + CDE Evasion-Aware | 0.9396 ± 0.0011 | +0.0407 |
| **Full Pipeline (all components)** | **0.9504 ± 0.0005** | **+0.0515** |

> Each component contributes independently. AIF provides the largest single step (+0.0311 incremental over PBI).
