# Results Directory — The Sentinel Ego

## File Index

| File | Phase | Description |
|------|-------|-------------|
| `phase4_cde_evolution.csv` | 4 | CDE evolution: JSD drift + F1 per round (15 rounds, 3 strategies) |
| `phase4_archetype_drift.csv` | 4 | Per-archetype JSD drift, hour shift, entropy change |
| `phase4_drs_scores.csv` | 4 | Detection Resistance Score per archetype (sorted descending) |
| `phase4_node_partitions.csv` | 4 | Non-IID NSL-KDD partition sizes per Ego node |
| `phase4_behavioral_baselines.csv` | 4 | Baseline mean_hour and hourly entropy per archetype |
| `phase5_mirror_defense.csv` | 5 | Mirror Defense: Base vs Mirror F1/AUC across 3 datasets |
| `phase5_cv_results.csv` | 5 | 5-Fold CV: F1 mean±std, AUC mean±std — 3 models × 3 datasets |
| `phase5_ablation.csv` | 5 | Ablation: F1/AUC/precision/recall per system component |
| `phase3_federated_per_node.csv` | 3 | Per-node isolated vs federated F1 and gain % |
| `privacy_analysis.csv` | 3 | RDP differential privacy budget: σ=0.5 and σ=1.0 |

## Key Results

```
Phase 4 — CDE
  Peak JSD drift     : 0.2200 (Round 15)
  Mean DRS           : 0.7334
  Best DRS           : Morning Bird — 0.9437
  DRS ≥ 0.50         : 9/10 archetypes

Phase 5 — Final Evaluation
  5-Fold CV best F1  : 0.9991 ± 0.0003 (LightGBM, NSL-KDD)
  Mirror Defense ΔF1 : +0.0003 mean across 3 datasets
  Ablation gain      : +0.0018 (Legacy IDS → Full Pipeline)

Phase 3 — Federated Learning
  Isolated baseline  : 0.9779
  Federated mean F1  : 0.9932  (+1.56%)
  DP guarantee       : (1.2802, 1e-5)-DP  [σ=1.0, RDP α=10]
```
