# `results/v5_final/` — SENTINEL-EGO Final Experiment Results

All files in this directory are the **paper-ready, verified results** used in the IEEE TIFS submission.  
Every number in the manuscript maps directly to one of these CSVs.

## File Index

| File | Paper Location | Key Claim |
|------|---------------|----------|
| `network_utility_q010_eps1404.csv` | Table IV | FAL-DP (ε=1.4042) preserves F1 within ΔF1≤0.016 on all 5 datasets |
| `ablation_leave_one_out.csv` | Table IV-B | Leave-one-out: each module independently verified in full pipeline |
| `fal_convergence_per_round.csv` | Fig. (FAL convergence) | Stability from Round 1–3; R=10 rounds, K=10 nodes |
| `dp_accounting_corrected_subsampling.csv` | Table II | Corrected DP accounting with Poisson subsampling q=0.01 |
| `cert_r42_fedproto_results.csv` | Section V-C, Table III | DP-FedProto closes 57.6% of isolation-to-global gap on CERT r4.2 |
| `cert_r42_scenario_ablation.csv` | Section V-C | Per-scenario F1: Isolated vs DP-FedProto |
| `btt_3tier_v4_fool_rates.csv` | Table VII (BTT) | 3-tier adversary ladder: Tier-1=91.5%, Tier-2=83.3%, Tier-3=77.0% |
| `pbi_tau_sweep.csv` | Section V-B | τ=0.25 optimal (F1=0.9953), grid search over [0.10–0.50] |

## Reproducibility

All experiments run on CPU only (Google Colab compatible).  
Seeds are fixed (`SEED=42`) and documented in each experiment script under `src/experiments/`.  
Datasets are loaded from public URLs; fallback to reproducible synthetic data if unavailable.

## DP Guarantees

| Experiment | q | σ | R | ε |
|-----------|---|---|---|---|
| Exp A — CERT FedProto | 0.01 | 2.0 | 10 | **1.2805** |
| Exp B — Network Utility | 0.10 | 2.0 | 10 | **1.4042** |
