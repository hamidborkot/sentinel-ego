# CDE Phase 4 — Adversarial Evolution: CICIDS2017

**Runner:** v2 | **Rounds:** 15 | **Strategies:** evasive / mimicry / noise

## Baselines

- Sentinel baseline F1: **0.9499**
- Legacy baseline F1: **0.9000**

## Round-by-Round Results

| Round | Strategy | Sentinel F1 | Legacy F1 | JSD |
|---|---|---|---|---|
| R01 | evasive | 0.9318 | 0.9000 | 0.0288 |
| R02 | mimicry | 0.9303 | 0.9001 | 0.0206 |
| R03 | noise | 0.9548 | 0.9001 | **0.1320** |
| R04 | evasive | 0.9288 | 0.9000 | 0.0692 |
| R05 | mimicry | 0.9292 | 0.9001 | 0.0255 |
| R06 | noise | 0.9548 | 0.9003 | 0.0623 |
| R07 | evasive | 0.9259 | 0.9000 | 0.0288 |
| R08 | mimicry | 0.9273 | 0.9001 | 0.0514 |
| R09 | noise | 0.9562 | 0.9003 | 0.0785 |
| R10 | evasive | 0.9234 | 0.9000 | 0.0645 |
| R11 | mimicry | 0.9253 | 0.9002 | 0.0787 |
| R12 | noise | 0.9563 | 0.9001 | 0.0376 |
| R13 | evasive | **0.9201** | 0.9000 | 0.0248 |
| R14 | mimicry | 0.9233 | 0.9001 | 0.0267 |
| R15 | noise | 0.9563 | 0.9003 | 0.0490 |

## Summary

| Metric | Value |
|---|---|
| Sentinel trough F1 | **0.9201** (Δ = −0.0297) |
| Legacy trough F1 | **0.9000** (Δ = +0.0000) |
| Peak JSD drift | **0.1320** |
| **Resilience advantage** | **+0.0201** |

> This is a primary paper claim for Table IV (v2 run). Use v3 run for final paper tables.
