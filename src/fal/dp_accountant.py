# ============================================================
# Phase 3: Differential Privacy Accounting
# Rényi DP → (ε, δ)-DP conversion
# The Sentinel Ego — Federated Adversarial Learning
# ============================================================

import numpy as np
import math
from typing import Tuple, List


def compute_rdp_gaussian(
    sigma: float,
    sensitivity: float,
    alpha: float
) -> float:
    """
    Compute Rényi DP (RDP) for the Gaussian mechanism.
    RDP(alpha) = alpha * sensitivity^2 / (2 * sigma^2)
    """
    return (alpha * (sensitivity ** 2)) / (2 * (sigma ** 2))


def rdp_to_dp(
    rdp_epsilon: float,
    alpha: float,
    delta: float
) -> float:
    """
    Convert RDP guarantee to (ε, δ)-DP.
    ε = rdp_epsilon + log(1 - 1/alpha) - log(delta * (1 - 1/alpha)) / (alpha - 1)
    Simplified standard conversion.
    """
    if alpha <= 1:
        raise ValueError("alpha must be > 1")
    epsilon = rdp_epsilon + (math.log(1 - 1 / alpha) - math.log(delta) -
                             math.log(1 - 1 / alpha)) / (alpha - 1)
    # Standard tighter conversion (Proposition 3 in Mironov 2017)
    epsilon_tight = rdp_epsilon + math.log(alpha / (alpha - 1)) + \
                    math.log((alpha - 1) / alpha) - (math.log(delta) + math.log(alpha)) / (alpha - 1)
    return min(epsilon, abs(epsilon_tight))


def compute_dp_budget(
    sigma: float,
    clipping_norm: float = 1.0,
    n_rounds: int = 10,
    n_nodes: int = 10,
    delta: float = 1e-5,
    alpha: int = 10
) -> dict:
    """
    Compute full (ε, δ)-DP bu