# FAL Phase 3 — Federated Learning: CICIDS2017

**Runner:** v2 | **Nodes:** 10 | **Rounds:** 10

## Per-Node Federation Results

| Archetype | Isolated F1 | Federated F1 | Gain |
|---|---|---|---|
| Morning Bird | 0.8642 | 0.8667 | +0.0025 |
| Collaborator | 0.8491 | 0.8878 | +0.0387 |
| Balanced | 0.9049 | 0.9300 | +0.0251 |
| Workaholic | 0.9136 | 0.9373 | +0.0237 |
| Night Owl | 0.9111 | 0.9324 | +0.0213 |
| Tech Savvy | 0.9478 | 0.9541 | +0.0063 |
| Careful Planner | 0.9545 | 0.9568 | +0.0023 |
| Lone Wolf | 0.9639 | 0.9628 | −0.0011 |
| Workaholic-8 | 0.9675 | 0.9672 | −0.0003 |
| Social Butterfly | 0.9806 | 0.9755 | −0.0051 |

## Summary

- **Mean federation gain:** +0.0113
- **Best node gain:** +0.0387 (Collaborator)
- **Round trajectory R1→R10:** 0.9390 → 0.9378

> **Note:** Nodes with high isolated performance (Lone Wolf, Workaholic-8, Social Butterfly) exhibit minor negative transfer (−0.0003 to −0.0051), a known FedAvg characteristic on non-IID data.
