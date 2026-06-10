# SENTINEL-EGO

**A Federated Behavioral Intelligence Framework for Privacy-Preserving Anomaly Detection in Distributed Networks**

> Submitted to IEEE Transactions on Dependable and Secure Computing (TDSC), 2026
> Author: Md. Hamid Borkot Tulla —

---

## What This Repository Is

This repository contains the **complete reproducible research artefacts** for the SENTINEL-EGO paper. Every number in the paper maps to a script and a frozen CSV in `results/`. The codebase is organised so that a reviewer, collaborator, or co-author can reproduce any single experiment independently without touching the rest.

---

## Quick Navigation

| What you want | Where to go |
|---|---|
| All final results (frozen) | [`RESULTS.md`](RESULTS.md) |
| Experiment-by-experiment index | [`EXPERIMENTS_INDEX.md`](EXPERIMENTS_INDEX.md) |
| Paper submission status | [`PAPER_STATUS.md`](PAPER_STATUS.md) |
| Reproduce a single experiment | `experiments/expN_*.py` |
| Framework source modules | `src/pbi/`, `src/aif/`, `src/fal/`, `src/cde/` |
| All result CSVs | `results/` |

---

## Paper Overview

SENTINEL-EGO detects network behavioral anomalies in distributed enterprise networks under federated differential privacy. It is built on four modules:

| Module | Role | Key Parameter |
|---|---|---|
| **PBI** — Persona Behavioral Integrity | KL-divergence drift detector; routes events to archetypes | tau=0.25 |
| **AIF** — Anomaly Intent Fingerprinting | 4-classifier ensemble; distance-to-prototype feature | theta=0.50 |
| **FAL** — Federated Adversarial Learning | Federated DP training across K=10 archetype nodes | eps=1.4042 |
| **CDE** — Covert Detection Evasion (BTT) | Dual-adversary robustness test | tau_JSD=0.25 |

**Datasets:** CICIDS2017, KDDCup99-SF, NSL-KDD, NetIntrusion, UNSW-NB15 (all standard network intrusion benchmarks — not insider threat datasets).

---

## Key Results at a Glance

| Experiment | Headline |
|---|---|
| EXP 1: Utility | FAL-DP max gap vs local = -0.0156 (KDDCup99), all others < -0.007 |
| EXP 3: Convergence | FAL plateaus by round 5 on all 5 datasets |
| EXP 5: SOTA | F1=0.9924 under eps=1.4042-DP; +4.18 pp over minimal DP baseline |
| EXP 6: Ablation | +4.44 pp total gain A→D; AIF single largest contributor (+1.93 pp) |
| EXP 7: Efficiency | 16.41 KB total communication; 0.0191 ms inference latency |
| EXP 8: Robustness | 9/10 archetypes PASS dual-adversary BTT (stump + MLP surrogate) |
| EXP 9: Tradeoff | F1 degrades only 2.27 pp across full privacy range eps=1.28→3.28 |

Full numbers with standard deviations: see [`RESULTS.md`](RESULTS.md).

---

## Reproducing the Experiments

### Requirements

```bash
pip install -r requirements.txt
```

### Run order (recommended — each is self-contained)

```bash
# Each script auto-downloads its dataset and saves a CSV to results/
python experiments/exp1_network_utility.py
python experiments/exp3_fal_convergence.py
python experiments/exp5_sota_comparison.py
python experiments/exp6_forward_ablation.py
python experiments/exp7_efficiency.py
python experiments/exp8_btt_dual_adversary.py
python experiments/exp9_privacy_utility.py
```

All scripts run in Google Colab or any local Python 3.9+ environment. Each script is **fully self-contained**: it imports nothing from `src/` — paste and run directly in Colab if needed.

**Expected total runtime:** ~60 minutes on a standard CPU (Google Colab free tier).

---

## Repository Structure

```
sentinel-ego/
├── README.md                  <- This file
├── RESULTS.md                 <- All frozen final results with exact numbers
├── EXPERIMENTS_INDEX.md       <- One-line summary of every experiment
├── PAPER_STATUS.md            <- Current paper edit status and checklist
├── CITATION.cff               <- Citation metadata
├── LICENSE                    <- MIT License
├── requirements.txt           <- Python dependencies
│
├── experiments/               <- Self-contained runnable experiment scripts
│   ├── exp1_network_utility.py
│   ├── exp3_fal_convergence.py
│   ├── exp5_sota_comparison.py
│   ├── exp6_forward_ablation.py
│   ├── exp7_efficiency.py
│   ├── exp8_btt_dual_adversary.py
│   └── exp9_privacy_utility.py
│
├── results/                   <- FROZEN CSVs — do not modify after paper submission
│   ├── exp1_network_utility.csv
│   ├── exp3_fal_convergence.csv
│   ├── exp5_sota_comparison.csv
│   ├── exp6_forward_ablation.csv
│   ├── exp7_efficiency.csv
│   ├── exp8_btt_dual_adversary.csv
│   └── exp9_privacy_utility.csv
│
├── src/                       <- Framework source modules (non-self-contained)
│   ├── pbi/                   <- Persona Behavioral Integrity module
│   ├── aif/                   <- Anomaly Intent Fingerprinting module
│   ├── fal/                   <- Federated Adversarial Learning module
│   └── cde/                   <- Covert Detection Evasion / BTT module
│
├── figures/                   <- Paper figures (PDF/PNG for LaTeX)
├── notebooks/                 <- Exploratory notebooks (not paper-final)
├── config/                    <- Hyperparameter configs
└── data/                      <- Dataset cache (auto-populated by scripts)
```

> **Note for reviewers:** The `experiments/` scripts are the paper-reproducible artefacts. The `src/` modules are the underlying framework implementation. The `results/` CSVs are the frozen outputs that match the paper tables exactly.

---

## Citation

If you use SENTINEL-EGO in your work, please cite:

```bibtex
@article{tulla2026sentinenego,
  title     = {{SENTINEL-EGO}: A Federated Behavioral Intelligence Framework
               for Privacy-Preserving Anomaly Detection in Distributed Networks},
  author    = {Tulla, Md. Hamid Borkot},
  journal   = {IEEE Transactions on Dependable and Secure Computing},
  year      = {2026},
  note      = {Under review}
}
```

---

## License

MIT License. See [`LICENSE`](LICENSE).
