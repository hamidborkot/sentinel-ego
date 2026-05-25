# Ablation Study — UNSW-NB15

**Runner:** v2 | **Evaluation:** 5-Fold CV

## Component-wise F1 Improvement

| Component | F1 (5-fold CV) | ΔF1 |
|---|---|---|
| W/o Sentinel (Legacy IDS) | 0.8263 ± 0.0047 | — |
| + PBI Behavioral Context | 0.8669 ± 0.0032 | +0.0406 |
| + AIF 42-Feature Profiling | 0.8870 ± 0.0026 | +0.0608 |
| + FAL Federation (10 nodes) | 0.8903 ± 0.0024 | +0.0640 |
| + CDE Evasion-Aware | 0.8822 ± 0.0030 | +0.0559 |
| **Full Pipeline (all components)** | **0.8910 ± 0.0033** | **+0.0647** |

> Strongest ablation story: every component contributes 0.040–0.064 ΔF1 because UNSW-NB15 is hard enough to expose differential improvement.
