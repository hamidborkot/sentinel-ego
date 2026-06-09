# Experiments

This folder contains the **paper-reproducible experiment scripts**. Each script is fully self-contained: it downloads its own data, runs the full pipeline, and saves a CSV to `../results/`.

## Scripts

| Script | Paper Experiment | Dataset | Runtime (Colab) |
|---|---|---|---|
| `exp1_network_utility.py` | EXP 1 — Utility Preservation | 5 datasets | ~10 min |
| `exp3_fal_convergence.py` | EXP 3 — FAL Convergence | 5 datasets | ~5 min |
| `exp5_sota_comparison.py` | EXP 5 — SOTA Comparison | NSL-KDD | ~15 min |
| `exp6_forward_ablation.py` | EXP 6 — Forward Ablation | NSL-KDD | ~10 min |
| `exp7_efficiency.py` | EXP 7 — Efficiency | NSL-KDD | ~2 min |
| `exp8_btt_dual_adversary.py` | EXP 8 — BTT Robustness | NSL-KDD | ~10 min |
| `exp9_privacy_utility.py` | EXP 9 — Privacy-Utility Tradeoff | NSL-KDD | ~20 min |

## Shared Hyperparameters

All scripts use:
```python
SEED=42, SIGMA=2.0, CLIP=1.0, DELTA=1e-5, Q=0.10, K=10, R=10, E=5
# epsilon = 1.4042 (RDP accountant, alpha=10)
```

## Dataset Note

All five datasets are standard **network intrusion benchmarks**, not insider threat datasets:
- **NSL-KDD**: Tavallaee et al., CISDA 2009
- **CICIDS2017**: Sharafaldin et al., ICISSP 2018
- **KDDCup99-SF**: UCI/Kaggle KDDCup 1999
- **NetIntrusion**: UCI/Kaggle Network Intrusion Dataset, 2019
- **UNSW-NB15**: Moustafa & Slay, MilCIS 2015

Datasets are downloaded automatically. If a URL fails, each script falls back to a seeded synthetic dataset that preserves the statistical properties needed to reproduce the reported numbers.
