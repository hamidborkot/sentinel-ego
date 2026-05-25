# Experiment Results

This directory contains all experiment outputs for **The Sentinel Ego** (IEEE TIFS 2026).

## Directory Structure

```
results/
├── v2_cicids_unsw/                    ← Runner v2: CICIDS2017 + UNSW-NB15 only
│   ├── phase2_aif_cicids2017.md
│   ├── phase2_aif_unsw_nb15.md
│   ├── phase3_fal_cicids2017.md
│   ├── phase3_fal_unsw_nb15.md
│   ├── phase4_cde_cicids2017.md
│   ├── phase4_cde_unsw_nb15.md
│   ├── phase5_ablation_cicids2017.md
│   ├── phase5_ablation_unsw_nb15.md
│   └── paper_tables_v2.md
│
├── v3_all5_datasets/                  ← Runner v3: All 5 datasets (FINAL)
│   ├── phase1_pbi_kl_divergence.md
│   ├── phase2_aif_all_datasets.md
│   ├── phase3_fal_all_datasets.md
│   ├── phase4_cde_all_datasets.md
│   ├── phase5_ablation_all_datasets.md
│   └── paper_tables_v3_final.md       ← ✅ USE THIS FOR IEEE TIFS SUBMISSION
│
└── differential_privacy_accounting.md ← DP guarantee, σ comparison, paper text
```

## Which Tables to Use for the Paper

| Paper Table | Source File | Notes |
|---|---|---|
| Table II (AIF) | `v3_all5_datasets/paper_tables_v3_final.md` | Best model per dataset |
| Table III (FAL) | `v3_all5_datasets/paper_tables_v3_final.md` | All 5 datasets |
| Table IV (CDE) | `v3_all5_datasets/paper_tables_v3_final.md` | KDDCup99-SF excluded |
| Table V (Ablation) | `v3_all5_datasets/paper_tables_v3_final.md` | KDDCup99-SF excluded |
| DP Section 5.3 | `differential_privacy_accounting.md` | σ=2.0, ε=13.78 |

## Key Exclusions (Documented)

| Dataset | Excluded From | Reason |
|---|---|---|
| KDDCup99-SF | Table IV (CDE) | Degenerate: both models frozen at F1=0.9450 across all 15 rounds |
| KDDCup99-SF | Table V (Ablation) | Ceiling effect: Legacy already at F1=0.9471, zero improvement headroom |

## Headline Results

- **CDE Resilience (UNSW-NB15):** Sentinel F1=0.8584 vs Legacy F1=0.7665 → **advantage +0.0919**
- **CDE Resilience (CICIDS2017):** Sentinel F1=0.9199 vs Legacy F1=0.9002 → **advantage +0.0198**
- **Ablation (UNSW-NB15):** Full pipeline +0.0805 over legacy IDS
- **DP Guarantee:** (13.7792, 1×10⁻⁵)-DP | σ=2.0 | 10 rounds | 10 nodes
- **PBI Consistency:** 9/10 archetypes KL_DoW < 0.3 | 10/10 KL_Rec < 0.3
