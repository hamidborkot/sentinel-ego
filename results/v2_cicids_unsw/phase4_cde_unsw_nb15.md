# CDE Phase 4 — Adversarial Evolution: UNSW-NB15

**Runner:** v2 | **Rounds:** 15 | **Strategies:** evasive / mimicry / noise

## Baselines

- Sentinel baseline F1: **0.8938**
- Legacy baseline F1: **0.8323**

## Round-by-Round Results

| Round | Strategy | Sentinel F1 | Legacy F1 | JSD |
|---|---|---|---|---|
| R01 | evasive | 0.8750 | 0.7937 | 0.0301 |
| R02 | mimicry | 0.8756 | 0.7943 | 0.0505 |
| R03 | noise | 0.9049 | 0.8364 | 0.0729 |
| R04 | evasive | 0.8735 | 0.7891 | 0.0391 |
| R05 | mimicry | 0.8741 | 0.7909 | 0.0392 |
| R06 | noise | 0.9020 | 0.8374 | 0.0684 |
| R07 | evasive | 0.8706 | 0.7836 | 0.0528 |
| R08 | mimicry | 0.8732 | 0.7876 | 0.0279 |
| R09 | noise | 0.9035 | 0.8380 | 0.0528 |
| R10 | evasive | 0.8693 | 0.7786 | 0.0350 |
| R11 | mimicry | 0.8719 | 0.7860 | 0.0354 |
| R12 | noise | 0.9052 | 0.8378 | **0.1814** |
| R13 | evasive | **0.8678** | **0.7733** | 0.0312 |
| R14 | mimicry | 0.8709 | 0.7818 | 0.0474 |
| R15 | noise | 0.9071 | 0.8387 | 0.1176 |

## Summary

| Metric | Value |
|---|---|
| Sentinel trough F1 | **0.8678** (Δ = −0.0260) |
| Legacy trough F1 | **0.7733** (Δ = −0.0589) |
| Peak JSD drift | **0.1814** |
| **Resilience advantage** | **+0.0945** |

> **Headline result of the paper.** Legacy IDS collapses −5.89% while Sentinel holds with only −2.60% degradation.
