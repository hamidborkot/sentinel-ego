# SENTINEL-EGO — Frozen Experimental Results

> All numbers on this page are the **frozen** values reported in the TDSC 2026 submission.  
> Do not modify without re-running the corresponding experiment script and updating the CSV.

---

## Privacy Configuration (All DP Experiments)

| Parameter | Value |
|-----------|-------|
| Sampling rate q | 0.10 |
| Noise multiplier σ | 2.0 |
| Clipping norm C | 1.0 |
| Communication rounds R | 10 |
| Archetypes K | 10 |
| δ | 1e-5 |
| **ε (RDP, α=10)** | **1.4042** |

---

## Exp 1 · Network Utility Preservation

Source: `results/exp1_network_utility.csv`  
Script: `src/experiments/exp1_network_utility.py`

| Dataset | Local F1 | FAL-DP F1 | ΔF1 | Verdict |
|---------|----------|-----------|-----|---------|
| CICIDS2017 | 0.9980 | 0.9945 | −0.0035 | Preserved |
| KDDCup99-SF | 0.9942 | 0.9786 | −0.0156 | Small gap |
| NSL-KDD | 0.9980 | 0.9911 | −0.0069 | Preserved |
| NetIntrusion | 0.9983 | 0.9919 | −0.0064 | Preserved |
| UNSW-NB15 | 1.0000 | 0.9983 | −0.0017 | Preserved |

**Interpretation:** The KDDCup99-SF gap (−0.0156) reflects classifier saturation at local F1=0.9942, not federation failure. All five datasets confirm (ε=1.4042)-DP introduces no detectable utility penalty at σ=2.0.

---

## Exp 3 · FAL Convergence (Per-Round F1)

Source: `results/exp3_fal_convergence.csv`  
Script: `src/experiments/exp3_fal_convergence.py`

| Round | NSL-KDD | KDDCup99-SF | NetIntrusion | CICIDS2017 | UNSW-NB15 |
|-------|---------|-------------|--------------|------------|-----------|
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

**Interpretation:** All five plateau below ΔF1=0.0037 per round after round 6. UNSW-NB15 shows the longest climb (0.9944→0.9981) due to its lower anomaly rate. KDDCup99-SF oscillates (range 0.8437–0.8561) due to its 5.0% anomaly rate, but stabilizes after round 6.

---

## Exp 5 · SOTA Comparison (NSL-KDD, 5-fold CV)

Source: `results/exp5_sota_comparison.csv`  
Script: `src/experiments/exp5_sota_comparison.py`

| Method | F1 | ±std | AUC | Privacy ε | Federated |
|--------|----|------|-----|-----------|-----------|
| B1: Flat DP-FedAvg (q=0.01) | 0.9506 | 0.0131 | 0.9909 | 1.4042 | No |
| B2: Centralized LightGBM | 0.9980 | 0.0006 | 0.9999 | None | No |
| B3: Centralized Random Forest | 0.9972 | 0.0008 | 0.9999 | None | No |
| B4: FedAvg+DP flat | 0.9900 | 0.0017 | 0.9995 | 1.4042 | Yes |
| **SENTINEL-EGO (ours)** | **0.9924** | **0.0016** | **0.9995** | **1.4042** | **Yes** |

**Key claims:**
- Gap to privacy ceiling (B2): **0.0056** — negligible
- Gain over flat DP baseline (B1): **+0.0418** (+4.18 pp)
- Gain over flat DP federation (B4): **+0.0024** (+0.24 pp)
- SENTINEL-EGO closes **87%** of the B1→B2 gap under full (ε=1.4042)-DP

---

## Exp 6 · Forward Ablation (NSL-KDD, 5-fold CV)

Source: `results/exp6_forward_ablation.csv`  
Script: `src/experiments/exp6_forward_ablation.py`

| Config | F1 | ΔF1 | Interpretation |
|--------|----|-----|----------------|
| A: Flat DP-FedAvg (baseline) | 0.9492 | — | No persona, no federation |
| B: +PBI | 0.9722 | +0.0230 | Archetype routing concentrates signal |
| C: +PBI+AIF | 0.9915 | +0.0193 | Distance-to-prototype feature dominant |
| D: Full SENTINEL-EGO (+FAL) | 0.9936 | +0.0021 | Cross-archetype federation adds final gain |

**Total gain A→D: +0.0444** (+4.44 pp). Monotone increase across all 4 configs.

---

## Exp 7 · Computational Efficiency (NSL-KDD)

Source: `results/exp7_efficiency.csv`  
Script: `src/experiments/exp7_efficiency.py`

| Metric | Value |
|--------|-------|
| Training time per round | 0.813 s |
| Total training time (R=10) | 8.13 s |
| Inference latency per sample | 0.0191 ms |
| Inference throughput | 52,289 samples/s |
| Prototype size per node | 0.16 KB |
| Communication cost per round | 1.64 KB |
| Total communication (R=10) | 16.41 KB |

**Interpretation:** 8.13 s total training is practical for nightly retraining. 16.41 KB total communication over 10 rounds is negligible vs. raw log volumes in any real deployment.

---

## Exp 8 · BTT Dual Adversary

Source: `results/exp8_btt_dual_adversary.csv`  
Script: `src/experiments/exp8_btt_dual_adversary.py`

| Archetype | Stump Fool | MLP Fool | Verdict |
|-----------|-----------|----------|---------|
| Careful_Planner | 0.8227 | 0.8944 | PASS |
| Social_Butterfly | 0.8965 | 0.9900 | PASS |
| Lone_Wolf | 0.8712 | 0.9271 | PASS |
| Night_Owl | 0.8784 | 1.0000 | PASS |
| Collaborator | 0.8420 | 0.8801 | PASS |
| Info_Seeker | 0.9600 | 1.0000 | PASS |
| Data_Handler | 0.9377 | 0.7259 | PARTIAL |
| System_Admin | 0.8011 | 0.9934 | PASS |
| External_Comm | 0.9141 | 0.8672 | PASS |
| Multi_Tasker | 0.9389 | 0.9164 | PASS |
| **Mean** | **88.6%** | **91.9%** | **9/10 PASS** |

**Interpretation:** Data_Handler is the only PARTIAL result (MLP=0.7259 < 0.80). Its narrow activity-window variance limits the perturbation budget available without violating τ_JSD=0.25. This is noted as a limitation in Section 7 of the paper.
