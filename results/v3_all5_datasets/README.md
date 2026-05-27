# Results: v3 — Full Pipeline, All 5 Datasets

Generated: 2026-05-27  
Target: IEEE Transactions on Information Forensics and Security (TIFS)

## Dataset Summary

| Dataset | Rows | Features | Attack Rate |
|---|---|---|---|
| KDDCup99-SF | 73,237 | 5 | 4.5% |
| NSL-KDD | 125,973 | 42 | 46.5% |
| NetIntrusion | 25,000 | 42 | 80.1% |
| CICIDS2017 | 56,661 | 78 | 59.9% |
| UNSW-NB15 | 82,332 | 43 | 55.1% |

## Files

| File | Phase | Description |
|---|---|---|
| `phase1_kl_90day_fixed.csv` | Phase 1 | 90-day KL divergence consistency (10 archetypes, fixed 45-day windows) |
| `phase2_aif_all5.csv` | Phase 2 | AIF 42-feature profiler: F1 + AUC-ROC (4 models × 5 datasets) |
| `phase3_federation_all5.csv` | Phase 3 | FedAvg per-node F1: isolated vs. federated (10 nodes × 5 datasets) |
| `phase4_cde_evolution_all5.csv` | Phase 4 | CDE 15-round mutation: JSD drift + detection F1 (5 datasets) |
| `phase4_drs_scores_all5.csv` | Phase 4 | Detection Resistance Score per archetype × dataset |
| `phase5_5fold_cv_all5.csv` | Phase 5 | 5-fold CV: F1±std + AUC (3 models × 5 datasets) |
| `phase5_ablation_nslkdd.csv` | Phase 5 | Ablation study: Legacy IDS → Full Sentinel Ego pipeline |
| `phase5_mirror_defense_all5.csv` | Phase 5 | Mirror Defense: base vs. augmented F1 (5 datasets) |

## Key Results

### Phase 1 — Behavioral Identity Consistency
- Overall mean KL divergence: **0.0245** (threshold < 0.30)
- All 10 archetypes: **Strong** consistency across 90 days ✅
- Claim supported: behavioral identity persists across 90-day observation window

### Phase 2 — AIF 42-Feature Profiler (Best per Dataset)
| Dataset | Model | F1 | AUC |
|---|---|---|---|
| KDDCup99-SF | RandomForest | 0.9992 | 1.0000 |
| NSL-KDD | LightGBM | 0.9993 | 1.0000 |
| NetIntrusion | XGBoost | 0.9990 | 1.0000 |
| CICIDS2017 | LightGBM | 0.9972 | 0.9996 |
| UNSW-NB15 | LightGBM | 0.9802 | 0.9982 |

### Phase 3 — Federated Learning Node Gain
| Dataset | Mean Gain | Max Gain |
|---|---|---|
| KDDCup99-SF | −0.022% | +0.150% |
| NSL-KDD | −0.016% | +0.210% |
| NetIntrusion | +0.057% | +0.160% |
| CICIDS2017 | +0.010% | +0.150% |
| UNSW-NB15 | +0.065% | +0.170% |

### Phase 4 — CDE Evasion Impact
| Dataset | Base F1 | Final F1 | Impact | Mean DRS |
|---|---|---|---|---|
| KDDCup99-SF | 0.9995 | 0.9538 | −0.0457 | 0.7093 |
| NSL-KDD | 0.9989 | 0.7222 | −0.2767 | 0.6722 |
| NetIntrusion | 0.9998 | 0.5506 | −0.4492 | 0.6430 |
| CICIDS2017 | 0.9979 | 0.2313 | −0.7666 | 0.9382 |
| UNSW-NB15 | 0.9794 | 0.9774 | −0.0020 | 0.5219 |

### Phase 5 — Ablation Study (NSL-KDD)
| Component | F1 | ΔF1 |
|---|---|---|
| Legacy IDS (baseline) | 0.9744 | — |
| + PBI Behavioral Context | 0.9989 | +0.0245 |
| + AIF 42-Feature Profiling | 0.9989 | +0.0245 |
| + FAL Federation (10 nodes) | 0.9990 | +0.0246 |
| + CDE Evasion-Aware | 0.9990 | +0.0246 |
| Full Pipeline | 0.9988 | +0.0244 |
