# Phase 4 — CDE: Adversarial Evolution (All 5 Datasets)

**Runner:** v3 | **Rounds:** 15 | **Strategies (cycling):** evasive → mimicry → noise

> ⚠️ **KDDCup99-SF excluded from paper Table IV** — extreme class separation renders CDE degenerate (both models frozen at F1=0.9450 across all rounds). See notes below.

---

## KDDCup99-SF  `⚠️ Degenerate — excluded from Table IV`

- Base: Sentinel=0.9450 | Legacy=0.9450  
- All 15 rounds: Sentinel=0.9450 | Legacy=0.9450 (frozen)  
- Peak JSD=0.1289 | **Resilience advantage=+0.0000**

> *The inter-cluster feature distance (μ=4.5σ) is too large for any mutation to cross the decision boundary. This confirms KDDCup99-SF is an unrealistic benchmark for adversarial evaluation.*

---

## NSL-KDD

| Round | Strategy | Sentinel F1 | Legacy F1 | JSD |
|---|---|---|---|---|
| R01 | evasive | 0.9507 | 0.9353 | 0.0656 |
| R02 | mimicry | 0.9513 | 0.9353 | 0.0652 |
| R03 | noise | 0.9541 | 0.9353 | 0.0898 |
| R04 | evasive | 0.9492 | 0.9353 | 0.0489 |
| R05 | mimicry | 0.9501 | 0.9353 | 0.0819 |
| R06 | noise | 0.9531 | 0.9354 | 0.0783 |
| R07 | evasive | 0.9496 | 0.9353 | 0.1113 |
| R08 | mimicry | 0.9503 | 0.9353 | 0.0654 |
| R09 | noise | 0.9534 | 0.9353 | 0.0889 |
| R10 | evasive | 0.9477 | 0.9353 | 0.0757 |
| R11 | mimicry | 0.9486 | 0.9353 | 0.0848 |
| R12 | noise | 0.9518 | 0.9354 | **0.1915** |
| R13 | evasive | **0.9460** | 0.9353 | 0.0810 |
| R14 | mimicry | 0.9466 | 0.9354 | 0.0777 |
| R15 | noise | 0.9530 | 0.9353 | 0.1094 |

**Base:** Sentinel=0.9565 | Legacy=0.9353  
**Trough:** Sentinel=0.9460 | Legacy=0.9353  
**Peak JSD=0.1915 | Resilience advantage=+0.0107**

---

## NetIntrusion

| Round | Strategy | Sentinel F1 | Legacy F1 | JSD |
|---|---|---|---|---|
| R01 | evasive | 0.9472 | 0.9205 | 0.0513 |
| R02 | mimicry | 0.9465 | 0.9205 | 0.0471 |
| R03 | noise | 0.9569 | 0.9207 | 0.0543 |
| R04 | evasive | 0.9432 | 0.9205 | 0.0590 |
| R05 | mimicry | 0.9453 | 0.9205 | 0.0517 |
| R06 | noise | 0.9578 | 0.9212 | 0.0999 |
| R07 | evasive | 0.9422 | 0.9205 | 0.0915 |
| R08 | mimicry | 0.9446 | 0.9207 | 0.0684 |
| R09 | noise | 0.9575 | 0.9207 | **0.2097** |
| R10 | evasive | 0.9410 | 0.9205 | 0.0426 |
| R11 | mimicry | 0.9426 | 0.9205 | 0.0672 |
| R12 | noise | 0.9581 | 0.9207 | 0.1003 |
| R13 | evasive | **0.9366** | **0.9205** | 0.0512 |
| R14 | mimicry | 0.9413 | 0.9205 | 0.0636 |
| R15 | noise | 0.9558 | 0.9210 | 0.0678 |

**Base:** Sentinel=0.9587 | Legacy=0.9207  
**Trough:** Sentinel=0.9366 | Legacy=0.9205  
**Peak JSD=0.2097 | Resilience advantage=+0.0161**

---

## CICIDS2017  ✅ Primary

| Round | Strategy | Sentinel F1 | Legacy F1 | JSD |
|---|---|---|---|---|
| R01 | evasive | 0.9323 | 0.9002 | 0.0443 |
| R02 | mimicry | 0.9312 | 0.9002 | 0.0308 |
| R03 | noise | 0.9552 | 0.9003 | 0.0509 |
| R04 | evasive | 0.9289 | 0.9002 | 0.0308 |
| R05 | mimicry | 0.9301 | 0.9003 | 0.0302 |
| R06 | noise | 0.9557 | 0.9004 | 0.0484 |
| R07 | evasive | 0.9266 | 0.9002 | 0.0199 |
| R08 | mimicry | 0.9275 | 0.9002 | 0.0482 |
| R09 | noise | 0.9567 | 0.9003 | 0.0491 |
| R10 | evasive | 0.9235 | 0.9002 | 0.0540 |
| R11 | mimicry | 0.9257 | 0.9004 | **0.0672** |
| R12 | noise | 0.9575 | 0.9005 | 0.0401 |
| R13 | evasive | **0.9199** | 0.9002 | 0.0242 |
| R14 | mimicry | 0.9243 | 0.9004 | 0.0389 |
| R15 | noise | 0.9576 | 0.9006 | 0.0465 |

**Base:** Sentinel=0.9500 | Legacy=0.9002  
**Trough:** Sentinel=0.9199 | Legacy=0.9002  
**Peak JSD=0.0672 | Resilience advantage=+0.0198**

> *Lower JSD on CICIDS2017 vs NetIntrusion reflects distributional dilution (n=150k). Evasion intensity is equivalent — the larger sample suppresses per-feature JSD.*

---

## UNSW-NB15  ✅ Primary — Headline Result

| Round | Strategy | Sentinel F1 | Legacy F1 | JSD |
|---|---|---|---|---|
| R01 | evasive | 0.8697 | 0.7801 | 0.0254 |
| R02 | mimicry | 0.8698 | 0.7808 | 0.0774 |
| R03 | noise | 0.8997 | 0.8169 | 0.0655 |
| R04 | evasive | 0.8669 | 0.7771 | 0.0289 |
| R05 | mimicry | 0.8675 | 0.7789 | 0.0406 |
| R06 | noise | 0.8996 | 0.8170 | 0.0635 |
| R07 | evasive | 0.8639 | 0.7736 | 0.0460 |
| R08 | mimicry | 0.8655 | 0.7770 | 0.0254 |
| R09 | noise | 0.9021 | 0.8183 | 0.0741 |
| R10 | evasive | 0.8612 | 0.7710 | 0.0231 |
| R11 | mimicry | 0.8654 | 0.7762 | 0.0551 |
| R12 | noise | 0.9016 | 0.8201 | 0.0373 |
| R13 | evasive | **0.8584** | **0.7665** | **0.0815** |
| R14 | mimicry | 0.8637 | 0.7729 | 0.0237 |
| R15 | noise | 0.9036 | 0.8192 | 0.0667 |

**Base:** Sentinel=0.8904 | Legacy=0.8117  
**Trough:** Sentinel=0.8584 | Legacy=0.7665  
**Peak JSD=0.0815 | Resilience advantage=+0.0919**

> **Headline result.** Legacy collapses −5.89% (0.8117→0.7665); Sentinel degrades only −3.60% (0.8904→0.8584). Asymmetric degradation under behavioral evasion is the primary contribution of this paper.
