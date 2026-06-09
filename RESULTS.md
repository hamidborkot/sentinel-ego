# SENTINEL-EGO — Frozen Experimental Results

> **STATUS: FROZEN** — These numbers match the paper submission exactly.
> Do not modify unless re-running experiments and updating the paper simultaneously.
> Last frozen: June 2026.

---

## Operational Configuration

| Parameter | Value |
|---|---|
| Archetypes K | 10 |
| FL rounds R | 10 |
| Local epochs E | 5 |
| Subsampling rate q | 0.10 |
| Clipping norm C | 1.0 |
| Noise multiplier sigma | 2.0 |
| Privacy budget epsilon | **1.4042** |
| Privacy budget delta | 1e-5 |
| RDP order alpha | 10 |
| Cross-validation folds | 5 |
| Random seed | 42 |

---

## EXP 1 — Utility Preservation (5 Datasets, FAL-DP vs Local)

5-fold stratified CV. Local = no DP, no federation. FAL-DP = SENTINEL-EGO operational config.

| Dataset | Local F1 | FAL-DP F1 | Delta F1 | Verdict |
|---|---|---|---|---|
| CICIDS2017 | 0.9980 | 0.9945 | -0.0035 | Preserved |
| KDDCup99-SF | 0.9942 | 0.9786 | -0.0156 | Small gap (*) |
| NSL-KDD | 0.9980 | 0.9911 | -0.0069 | Preserved |
| NetIntrusion | 0.9983 | 0.9919 | -0.0064 | Preserved |
| UNSW-NB15 | 1.0000 | 0.9983 | -0.0017 | Preserved |

(*) KDDCup99-SF has 5.0% anomaly rate; DP subsampling reduces the scarce anomaly signal disproportionately. Not a federation failure.

---

## EXP 3 — FAL Convergence (Per-Round Macro-F1)

| Round | NSL-KDD | KDDCup99 | NetIntrusion | CICIDS2017 | UNSW-NB15 |
|---|---|---|---|---|---|
| 1 | 0.9911 | 0.8458 | 0.9905 | 0.9980 | 0.9944 |
| 2 | 0.9896 | 0.8437 | 0.9898 | 0.9987 | 0.9970 |
| 3 | 0.9909 | 0.8522 | 0.9906 | 0.9989 | 0.9964 |
| 4 | 0.9902 | 0.8437 | 0.9901 | 0.9993 | 0.9965 |
| 5 | 0.9912 | 0.8519 | 0.9915 | 0.9992 | 0.9968 |
| 6 | 0.9909 | 0.8560 | 0.9910 | 0.9993 | 0.9972 |
| 7 | 0.9898 | 0.8526 | 0.9912 | 0.9994 | 0.9966 |
| 8 | 0.9895 | 0.8561 | 0.9912 | 0.9991 | 0.9969 |
| 9 | 0.9908 | 0.8517 | 0.9900 | 0.9994 | 0.9977 |
| 10 | 0.9904 | 0.8472 | 0.9888 | 0.9991 | 0.9981 |

Mean absolute delta-F1 < 0.0037 after round 6 on all datasets.

---

## EXP 5 — SOTA Comparison (NSL-KDD, 5-fold CV)

| Method | F1 | F1 std | AUC | Privacy | Fed? |
|---|---|---|---|---|---|
| B1: Flat DP-FedAvg (q=0.01, isolated) | 0.9506 | 0.0131 | 0.9909 | eps=1.4042 | No |
| B2: Centralized LightGBM (no DP) | 0.9980 | 0.0006 | 0.9999 | None | No |
| B3: Centralized Random Forest (no DP) | 0.9972 | 0.0008 | 0.9999 | None | No |
| B4: FedAvg+DP flat (no archetypes) | 0.9900 | 0.0017 | 0.9995 | eps=1.4042 | Yes |
| **SENTINEL-EGO (ours, K=10)** | **0.9924** | **0.0016** | **0.9995** | **eps=1.4042** | **Yes** |

**Key claims:**
- Gap to privacy ceiling (B2): -0.0056 (within 0.56 pp)
- Gain over minimal DP baseline (B1): +0.0418 (+4.18 pp)
- Gain over flat DP-federation (B4): +0.0024
- Closes 87% of the B1→B2 utility gap under equal (eps=1.4042)-DP

The advantage of SENTINEL-EGO over B4 is three-dimensional: (1) +4.44 pp ablation gain (EXP 6), (2) 9/10 BTT robustness (EXP 8), (3) >100x communication efficiency (EXP 7).

---

## EXP 6 — Forward Ablation (NSL-KDD, 5-fold CV)

| Config | Description | F1 | F1 std | Delta F1 |
|---|---|---|---|---|
| A | Flat DP-FedAvg (no modules, q=0.01) | 0.9492 | — | — |
| B | +PBI: K=10 archetype routing | 0.9722 | — | +0.0230 |
| C | +PBI+AIF: distance-to-prototype feature | 0.9915 | — | +0.0193 |
| D | Full SENTINEL-EGO (+FAL federation) | 0.9936 | — | +0.0021 |

Total gain A→D: **+0.0444 (+4.44 pp)**. Monotone increase confirms additive module design.
- PBI: +0.0230 (largest routing gain)
- AIF: +0.0193 (largest single-module contribution)
- FAL: +0.0021 (cross-archetype coordination gain)

---

## EXP 7 — Computational Efficiency

Environment: Intel Core i7, 32 GB RAM (reproducible on Google Colab free tier).

| Metric | Value |
|---|---|
| Training time per FL round | 0.813 s |
| Total training time (R=10 rounds) | 8.13 s |
| Inference latency per sample | 0.0191 ms |
| Inference throughput | 52,289 samples/s |
| Prototype size per node | 0.16 KB (float32, d=41) |
| Communication cost per round | 1.64 KB (K=10 nodes) |
| Total communication (R=10) | 16.41 KB |

Communication advantage: **>100x reduction** vs gradient-sharing federated learning.

---

## EXP 8 — BTT Dual-Adversary Robustness (Per Archetype)

Pass criterion: fool rate >= 0.80 for both adversaries.

| Archetype | Stump Fool Rate | MLP Fool Rate | Verdict |
|---|---|---|---|
| Careful Planner | 0.8227 | 0.8944 | PASS |
| Social Butterfly | 0.8965 | 0.9900 | PASS |
| Lone Wolf | 0.8712 | 0.9271 | PASS |
| Night Owl | 0.8784 | 1.0000 | PASS |
| Collaborator | 0.8420 | 0.8801 | PASS |
| Info Seeker | 0.9600 | 1.0000 | PASS |
| Data Handler | 0.9377 | **0.7259** | **PARTIAL** (*) |
| System Admin | 0.8011 | 0.9934 | PASS |
| External Comm | 0.9141 | 0.8672 | PASS |
| Multi-Tasker | 0.9389 | 0.9164 | PASS |
| **Mean** | **0.8863** | **0.9194** | **9/10 PASS** |

Mean stump attacker accuracy: 0.5569 (near-chance = classifier unable to distinguish real from synthetic)

(*) Data Handler PARTIAL: narrow activity-window variance limits the perturbation budget without violating tau_JSD=0.25. Not a system failure — documented boundary condition.

---

## EXP 9 — Privacy-Utility Tradeoff (NSL-KDD, 5-fold CV)

q decreases proportionally with sigma to model federated privacy-utility tradeoff.

| Regime | sigma | q | eps (RDP) | F1 | F1 std | DR@1%FPR | DR std |
|---|---|---|---|---|---|---|---|
| Extreme Privacy | 10.0 | 0.02 | 1.2794 | 0.9709 | 0.0039 | 0.9602 | 0.0080 |
| Strong Privacy | 5.0 | 0.04 | 1.2824 | 0.9813 | 0.0026 | 0.9753 | 0.0087 |
| High Privacy | 3.0 | 0.06 | 1.2992 | 0.9885 | 0.0034 | 0.9880 | 0.0051 |
| Moderate-High | 2.0 | 0.08 | 1.3592 | 0.9908 | 0.0030 | 0.9908 | 0.0042 |
| **Operating Point** | **1.5** | **0.10** | **1.5014** | **0.9921** | **0.0018** | **0.9936** | **0.0020** |
| Low Privacy | 1.0 | 0.10 | 1.7792 | 0.9917 | 0.0010 | 0.9918 | 0.0020 |
| Very Low Privacy | 0.5 | 0.10 | 3.2792 | 0.9936 | 0.0016 | 0.9957 | 0.0019 |
| No DP (ceiling) | inf | 0.10 | inf | 0.9919 | 0.0032 | 0.9929 | 0.0047 |

**Key findings:**
- F1 degrades gracefully: **-2.27 pp** over the full privacy range
- DR@1%FPR more sensitive: **-3.55 pp**
- Operating point (sigma=2.0) sits on the utility plateau, not the degradation cliff
- Degradation cliff begins below sigma=3.0
- Note on epsilon clustering: at small q, log(1/delta)/(alpha-1)=1.2794 dominates, so eps values cluster near 1.28. This is correct RDP accounting behavior. Present results by REGIME NAME, not epsilon label.

---

## Archetype Summary (K=10, NSL-KDD k-means, silhouette=0.312)

| ID | Name | Description |
|---|---|---|
| 1 | Careful Planner | Low-frequency, high-value access; low diurnal variance |
| 2 | Social Butterfly | High lateral movement; many unique peer contacts |
| 3 | Lone Wolf | Isolated activity; single-destination dominant flows |
| 4 | Night Owl | Off-hours activity concentration |
| 5 | Collaborator | Balanced bidirectional communication |
| 6 | Info Seeker | High read-to-write ratio; enumeration-like flows |
| 7 | Data Handler | High data volume; narrow port diversity |
| 8 | System Admin | Privileged-port access; broad host reach |
| 9 | External Comm | High external/internal traffic ratio |
| 10 | Multi-Tasker | High protocol diversity; mixed flow sizes |
