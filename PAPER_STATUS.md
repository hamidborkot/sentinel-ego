# SENTINEL-EGO — Paper Submission Status

> **Venue:** IEEE Transactions on Dependable and Secure Computing (TDSC), 2026
> **Page limit:** 10 pages (hard)
> **Current estimated length:** ~9.85 pages after planned edits

---

## Submission Checklist

### Experiments
- [x] EXP 1: Utility preservation (5 datasets)
- [x] EXP 3: FAL convergence
- [x] EXP 5: SOTA comparison (4 baselines)
- [x] EXP 6: Forward ablation (4 configs)
- [x] EXP 7: Computational efficiency
- [x] EXP 8: BTT dual-adversary (stump + MLP surrogate)
- [ ] EXP 9: Privacy-utility tradeoff — **run and freeze CSV, then update paper**

### Paper Edits Needed (in order)

1. **Abstract** — Replace BET-IDS comparison with EXP 9 graceful degradation stat (-2.27 pp)
2. **Section I Introduction** — Add EXP 9 to Contribution 4 bullet
3. **Section IV Privacy Analysis** — Replace `tab:privacy` (5-row) with new 8-row `tab:tradeoff` from EXP 9
4. **Section IV** — Add reference to new `fig:tradeoff` at end of section
5. **Section V** — Add Subsection 5.6 Privacy-Utility Tradeoff (~8 lines)
6. **New figure** — `fig5_tradeoff`: dual y-axis line plot, F1 and DR@1%FPR vs regime
7. **Section VI Discussion** — Add fourth principal finding from EXP 9
8. **Section VI Conclusion** — Update FAL summary sentence to include tradeoff claim
9. **Bibliography** — Unify `duddu2018`/`Duddu2018` duplicates; check `Tavallaee2009`/`5356528`

### Tables and Figures

| # | Label | Status |
|---|---|---|
| Table 1 | `tab:privacy` → rename to `tab:tradeoff`, expand to 8 rows | **NEEDS UPDATE** |
| Table 2 | `tab:datasets` | Done |
| Table 3 | `tab:sota` | Done |
| Table 4 | `tab:utility` | Done |
| Table 5 | `tab:btt` | Done |
| Table 6 | `tab:efficiency` | Done |
| Fig 1 | `fig:motivation` | Done |
| Fig 2 | `fig:architecture` | Done |
| Fig 3 | `fig:ablation` | Done |
| Fig 4 | `fig:convergence` | Done |
| Fig 5 | `fig:tradeoff` | **NEEDS CREATION** |

---

## Page Management

If adding Section 5.6 + Fig 5 pushes past 10 pages, apply in this order:

1. **First:** Drop the Verdict column from `tab:utility` (fold into a footnote)
2. **Second:** Remove the AUC column from `tab:sota` (cite AUC=0.9995 inline; both SENTINEL and B4 are identical)
3. **Third:** Move `tab:efficiency` numbers inline in Section 5.5 prose and delete the table

---

## Framing Note (Critical)

This paper is about **network behavioral anomaly detection** under federated differential privacy.
The five datasets (NSL-KDD, CICIDS2017, KDDCup99-SF, NetIntrusion, UNSW-NB15) are all standard
**network intrusion benchmarks**. They are NOT insider threat datasets.
Do NOT use the phrase "insider threat" anywhere in the TDSC paper.
The correct framing is: "privacy-preserving behavioral anomaly detection for distributed enterprise networks."
