# SENTINEL-EGO — Experiments Index

Every experiment in the paper, in one place. Use this to find the script, the frozen CSV, and the paper section for any result.

---

| Exp | Name | Script | Frozen CSV | Paper Section | Status |
|---|---|---|---|---|---|
| EXP 1 | Utility Preservation | `experiments/exp1_network_utility.py` | `results/exp1_network_utility.csv` | Section V-B | FROZEN |
| EXP 3 | FAL Convergence | `experiments/exp3_fal_convergence.py` | `results/exp3_fal_convergence.csv` | Section V-D | FROZEN |
| EXP 5 | SOTA Comparison | `experiments/exp5_sota_comparison.py` | `results/exp5_sota_comparison.csv` | Section V-B | FROZEN |
| EXP 6 | Forward Ablation | `experiments/exp6_forward_ablation.py` | `results/exp6_forward_ablation.csv` | Section V-C | FROZEN |
| EXP 7 | Efficiency | `experiments/exp7_efficiency.py` | `results/exp7_efficiency.csv` | Section V-E | FROZEN |
| EXP 8 | BTT Dual Adversary | `experiments/exp8_btt_dual_adversary.py` | `results/exp8_btt_dual_adversary.csv` | Section V-E | FROZEN |
| EXP 9 | Privacy-Utility Tradeoff | `experiments/exp9_privacy_utility.py` | `results/exp9_privacy_utility.csv` | Section IV + V-F | FROZEN |

---

## Why EXP 2 and EXP 4 are absent

- **EXP 2** (leave-one-out ablation) was superseded by EXP 6 (forward ablation), which provides a cleaner monotone contribution story. EXP 2 results are in `notebooks/` for reference.
- **EXP 4** was an early architecture exploration notebook, not used in the final paper.

---

## Self-Contained Execution

Every `experiments/expN_*.py` script:
1. Auto-downloads its dataset (NSL-KDD, CICIDS2017, etc.) from public URLs
2. Falls back to a seeded synthetic dataset if the URL is unavailable
3. Runs end-to-end and saves output to `results/expN_*.csv`
4. Imports nothing from `src/` — paste and run directly in Google Colab

## Key Hyperparameters (same across all experiments)

```python
SEED  = 42
SIGMA = 2.0    # DP noise multiplier
CLIP  = 1.0    # gradient clipping norm
DELTA = 1e-5   # DP delta
Q     = 0.10   # Poisson subsampling rate
K     = 10     # number of archetype nodes
R     = 10     # FL rounds
E     = 5      # local epochs
# Resulting epsilon (RDP accountant, alpha=10): 1.4042
```
