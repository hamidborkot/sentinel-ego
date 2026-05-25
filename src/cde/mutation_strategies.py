"""
Mutation Strategies for CDE
===========================
Defines the three behavioral mutation modes used in Phase 4:
  - Evasive   : maximum divergence from baseline (flatten toward uniform)
  - Mimicry   : partial blend toward normal-user reference distribution
  - Noise     : stochastic Dirichlet perturbation
"""

import numpy as np
from enum import Enum


class MutationStrategy(str, Enum):
    EVASIVE = "evasive"
    MIMICRY = "mimicry"
    NOISE   = "noise"


def apply_mutation(
    distribution: np.ndarray,
    strategy: MutationStrategy,
    normal_reference: np.ndarray,
    mutation_rate: float = 0.15,
    rng: np.random.Generator = None,
) -> np.ndarray:
    """
    Apply a single mutation step to a probability distribution.

    Parameters
    ----------
    distribution     : Current behavioral distribution (normalized, length N)
    strategy         : One of MutationStrategy.EVASIVE / MIMICRY / NOISE
    normal_reference : Reference distribution for mimicry (same length N)
    mutation_rate    : λ — mixing coefficient (default 0.15)
    rng              : numpy Generator for reproducibility

    Returns
    -------
    Mutated and renormalized distribution of same shape.
    """
    if rng is None:
        rng = np.random.default_rng(42)

    dist = np.clip(distribution, 1e-12, None).astype(float)
    dist /= dist.sum()
    lam = mutation_rate

    if strategy == MutationStrategy.EVASIVE:
        uniform = np.ones_like(dist) / len(dist)
        mutated = (1 - lam) * dist + lam * uniform

    elif strategy == MutationStrategy.MIMICRY:
        ref = np.clip(normal_reference, 1e-12, None).astype(float)
        ref /= ref.sum()
        mutated = (1 - lam) * dist + lam * ref

    else:  # NOISE
        noise = rng.dirichlet(np.ones(len(dist)) * 0.5)
        mutated = (1 - lam) * dist + lam * noise

    mutated = np.clip(mutated, 1e-12, None)
    return mutated / mutated.sum()
