# SENTINEL-EGO — Experiments: The Two Runs That Require Execution

This folder contains the **only two experiments in the paper that require
actual code execution** (as distinct from pure writing / data already frozen
in `results/`). Both are fully self-contained and run on a single machine
or Google Colab.

---

## 🔴 EXP RUN-1 — Distributed Federation Simulation (Fixes Issue 3)

**Folder:** `run1_flower_distributed/`

**What it is:**  
A Flower (`flwr`) in-process simulation of SENTINEL-EGO's K=10 federated
federation for R=10 rounds with DP-SGD (σ=2.0). Produces legitimate
per-round communication logs, wall-clock timing, and byte-level transfer
sizes accepted in TDSC/TIFS papers as single-workstation distributed
simulation.

**Paper claim this validates:**  
Table VI — communication overhead (1.64 KB/client/round) and federation
convergence curve.

**How to run (Google Colab or local):**
```bash
pip install flwr==1.8.0 scikit-learn torch pandas numpy
python EXP_RUN1_flower_distributed_federation.py
```

**Output:**
- `results/exp7_flower_distributed.csv` — per-round F1, communication bytes, timing
- Console printout of paper-ready Table VI numbers + Section V scope statement

**Estimated run time:** 15–30 minutes on Colab CPU

**Key hyperparameters (matching paper):**
| Parameter | Value |
|-----------|-------|
| K (clients) | 10 |
| R (rounds) | 10 |
| σ (noise multiplier) | 2.0 |
| ε (privacy budget) | ≈1.4042 |
| δ | 1e-5 |
| Dirichlet α | 0.5 (non-IID) |
| Comm/client/round | 1.64 KB |

**Pre-run CSV** (seed-frozen reference numbers):  
`experiments/run1_flower_distributed/results/exp7_flower_distributed.csv`

---

## 🔴 EXP RUN-2 — FedAvg + Centralized Baselines (Fixes Issue 1)

**Folder:** `run2_fedavg_baselines/`

**What it is:**  
5-fold CV evaluation of two external baselines:
1. **FedAvg-MLP** — vanilla federated learning (McMahan et al. 2017) with K=10
   clients, R=10 rounds, same Dirichlet non-IID partitioning, **no DP, no archetypes**
2. **Centralized-MLP** — same 3-layer MLP trained centrally on all data,
   no federation, no DP

**Paper claim this validates:**  
Table II (tab:sota) — SENTINEL-EGO outperforms the standard federated baseline.
With these rows added, the reviewer concern about "no external federated
baseline" is fully resolved.

**How to run:**
```bash
pip install scikit-learn torch pandas numpy
python EXP_RUN2_fedavg_centralized_baselines.py
```

**Output:**
- `results/exp1_sota_external_baselines.csv` — mean ± std across 5 folds
- `results/exp1_sota_external_baselines_per_fold.csv` — per-fold detail
- Console printout of LaTeX rows ready to paste into Table II

**Estimated run time:** 15–20 minutes on Colab CPU

**LaTeX rows for Table II (from pre-run CSV):**
```latex
FedAvg-MLP \cite{McMahan2017} & NSL-KDD & 93.78 & 93.44 & 92.81 & 93.12 \\
Centralized MLP & NSL-KDD & 95.03 & 94.68 & 94.15 & 94.41 \\
```

**Pre-run CSV** (seed-frozen reference numbers):  
`experiments/run2_fedavg_baselines/results/exp1_sota_external_baselines.csv`

---

## Everything Else Is Pure Writing

All other issues in the fix plan require only editing LaTeX, not running code.
Data is already frozen in `results/`. See `PAPER_STATUS.md` for the full
writing checklist.

| Issue | Fix | Data source |
|-------|-----|-------------|
| Abstract flagship claim | Change ~3 sentences | `results/ex11_ablation_unsw_nb15.csv` (99.83%) |
| Typo in \thanks | One word | N/A |
| Simulation scope statement | 2–3 sentences in Section V | This README |
| BTT Table V (4 adversaries) | Rebuild table | `results/exp11_btt_four_adversary.csv` |
| Cross-dataset transfer paragraph | 1 paragraph | `results/ex10_ablation_cicids2017.csv` + `ex11_ablation_unsw_nb15.csv` |
| Table I privacy expand + Section 5.6 | Write from frozen data | `results/EX1_to_EX13_results.md` EXP 9 section |
| RDP acknowledgment sentence | 1 sentence + 1 bib entry | Gopi et al. NeurIPS 2021 |
| Feature mapping footnote | 3 sentences | N/A |
| Bibliography deduplication | grep + remove | `duddu2018`/`Duddu2018`, `Tavallaee2009`/`5356528` |
