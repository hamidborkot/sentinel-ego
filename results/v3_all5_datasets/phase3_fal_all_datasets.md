# Phase 3 — FAL: Federated Learning (All 5 Datasets)

**Runner:** v3 | **Nodes:** 10 Ego archetypes | **Rounds:** 10 | **Algorithm:** FedAvg

---

## KDDCup99-SF  `⚠️ Ceiling effect — ablation excluded`

| Archetype | Isolated | Federated | Gain |
|---|---|---|---|
| Morning Bird | 0.9384 | 0.9632 | +0.0249 |
| Collaborator | 0.9569 | 0.9670 | +0.0101 |
| Balanced | 0.9385 | 0.9483 | +0.0098 |
| Workaholic | 0.9598 | 0.9668 | +0.0069 |
| Night Owl | 0.9613 | 0.9654 | +0.0041 |
| Tech Savvy | 0.9627 | 0.9709 | +0.0082 |
| Careful Planner | 0.9725 | 0.9680 | −0.0045 |
| Lone Wolf | 0.9804 | 0.9696 | −0.0108 |
| Workaholic-8 | 0.9882 | 0.9743 | −0.0139 |
| Social Butterfly | 0.9789 | 0.9672 | −0.0117 |

**Mean gain:** +0.0023 | **Best node gain:** +0.0249 | **R1→R10:** 0.9669→0.9656

---

## NSL-KDD

| Archetype | Isolated | Federated | Gain |
|---|---|---|---|
| Morning Bird | 0.9333 | 0.9487 | +0.0154 |
| Collaborator | 0.9231 | 0.9519 | +0.0288 |
| Balanced | 0.9490 | 0.9848 | +0.0358 |
| Workaholic | 0.9415 | 0.9670 | +0.0254 |
| Night Owl | 0.9650 | 0.9853 | +0.0203 |
| Tech Savvy | 0.9424 | 0.9882 | **+0.0458** |
| Careful Planner | 0.9635 | 0.9875 | +0.0240 |
| Lone Wolf | 0.9649 | 0.9895 | +0.0247 |
| Workaholic-8 | 0.9790 | 0.9944 | +0.0154 |
| Social Butterfly | 0.9767 | 0.9939 | +0.0172 |

**Mean gain:** +0.0253 | **Best node gain:** +0.0458 | **R1→R10:** 0.9747→0.9794

---

## NetIntrusion

| Archetype | Isolated | Federated | Gain |
|---|---|---|---|
| Morning Bird | 0.8738 | 0.9259 | **+0.0521** |
| Collaborator | 0.9171 | 0.9462 | +0.0291 |
| Balanced | 0.9474 | 0.9745 | +0.0272 |
| Workaholic | 0.9159 | 0.9582 | +0.0423 |
| Night Owl | 0.9375 | 0.9744 | +0.0369 |
| Tech Savvy | 0.9315 | 0.9677 | +0.0362 |
| Careful Planner | 0.9377 | 0.9714 | +0.0337 |
| Lone Wolf | 0.9656 | 0.9881 | +0.0224 |
| Workaholic-8 | 0.9811 | 0.9912 | +0.0101 |
| Social Butterfly | 0.9868 | 0.9945 | +0.0076 |

**Mean gain:** +0.0298 | **Best node gain:** +0.0521 | **R1→R10:** 0.9683→0.9660

---

## CICIDS2017  ✅ Primary

| Archetype | Isolated | Federated | Gain |
|---|---|---|---|
| Morning Bird | 0.8278 | 0.8418 | +0.0140 |
| Collaborator | 0.8699 | 0.8963 | +0.0265 |
| Balanced | 0.8938 | 0.9155 | +0.0216 |
| Workaholic | 0.9076 | 0.9320 | +0.0244 |
| Night Owl | 0.9265 | 0.9327 | +0.0062 |
| Tech Savvy | 0.9334 | 0.9448 | +0.0114 |
| Careful Planner | 0.9480 | 0.9527 | +0.0047 |
| Lone Wolf | 0.9592 | 0.9566 | −0.0026 |
| Workaholic-8 | 0.9689 | 0.9625 | −0.0064 |
| Social Butterfly | 0.9747 | 0.9713 | −0.0033 |

**Mean gain:** +0.0096 | **Best node gain:** +0.0265 | **R1→R10:** 0.9370→0.9400

---

## UNSW-NB15  ✅ Primary

| Archetype | Isolated | Federated | Gain |
|---|---|---|---|
| Morning Bird | 0.8136 | 0.8534 | +0.0399 |
| Collaborator | 0.8462 | 0.8699 | +0.0237 |
| Balanced | 0.8657 | 0.8687 | +0.0030 |
| Workaholic | 0.8671 | 0.8849 | +0.0178 |
| Night Owl | 0.9012 | 0.9018 | +0.0006 |
| Tech Savvy | 0.9168 | 0.9031 | −0.0137 |
| Careful Planner | 0.9244 | 0.9122 | −0.0122 |
| Lone Wolf | 0.9163 | 0.9106 | −0.0058 |
| Workaholic-8 | 0.9441 | 0.9344 | −0.0097 |
| Social Butterfly | 0.9564 | 0.9394 | −0.0170 |

**Mean gain:** +0.0027 | **Best node gain:** +0.0399 | **R1→R10:** 0.8927→0.8959
