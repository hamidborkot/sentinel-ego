# Exp5–Exp8 Frozen Results Record

Generated: June 2026  
SEED=42, CPU-only (Google Colab), NSL-KDD primary dataset

## Files in this directory

| File | Experiment | Key number |
|------|-----------|------------|
| `exp5_sota_comparison.csv` | SOTA comparison (5 methods) | SENTINEL-EGO F1=0.9924 |
| `exp6_forward_ablation.csv` | 4-step forward ablation | PBI gain=+0.0230 |
| `exp7_efficiency.csv` | Training/inference/comm. cost | 1.64 KB/round |
| `exp8_btt_dual_adversary.csv` | Dual adversary BTT | MLP fool=91.9%, 9/10 PASS |

## Reproducibility

All four experiments are self-contained Colab cells. They require only:
```
numpy, pandas, scikit-learn, lightgbm, requests
```
No local data files. NSL-KDD is fetched from GitHub at runtime; synthetic fallback activates automatically if the URL is unreachable.

## Do Not Re-Run

These numbers are frozen for the paper. Do not re-run experiments after this point unless a reviewer requests it. Any re-run must use SEED=42 and document the date.
