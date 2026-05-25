"""
Collective Deception Evolution (CDE) Engine
===========================================
Phase 4 of The Sentinel Ego.

Coordinates 10 Ego nodes across 15 evolution rounds using three
cycling mutation strategies: evasive → mimicry → noise.
Tracks JSD behavioral drift and Detection Resistance Score (DRS)
per archetype per round.
"""

import numpy as np
import pandas as pd
from scipy.spatial.distance import jensenshannon
from scipy.stats import entropy
from typing import Dict, List, Tuple


class CDEEvolutionEngine:
    """Orchestrates collective deception evolution across all Ego nodes."""

    STRATEGY_CYCLE = ["evasive", "mimicry", "noise"]
    MUTATION_RATE = 0.15

    def __init__(self, archetypes: List[str], n_rounds: int = 15, seed: int = 42):
        self.archetypes = archetypes
        self.n_rounds = n_rounds
        self.rng = np.random.default_rng(seed)
        self.history: List[Dict] = []

    def _get_strategy(self, round_idx: int) -> str:
        return self.STRATEGY_CYCLE[round_idx % len(self.STRATEGY_CYCLE)]

    def _mutate_distribution(
        self,
        dist: np.ndarray,
        strategy: str,
        normal_ref: np.ndarray,
    ) -> np.ndarray:
        """Apply one mutation step to a probability distribution."""
        dist = np.array(dist, dtype=float)
        lam = self.MUTATION_RATE

        if strategy == "evasive":
            # Maximum divergence: flatten toward uniform
            uniform = np.ones_like(dist) / len(dist)
            mutated = (1 - lam) * dist + lam * uniform
        elif strategy == "mimicry":
            # Partial blend toward normal-user reference distribution
            mutated = (1 - lam) * dist + lam * normal_ref
        else:  # noise
            noise = self.rng.dirichlet(np.ones(len(dist)) * 0.5)
            mutated = (1 - lam) * dist + lam * noise

        mutated = np.clip(mutated, 1e-12, None)
        return mutated / mutated.sum()

    def _compute_jsd(self, p: np.ndarray, q: np.ndarray) -> float:
        p = np.clip(p, 1e-12, None); p /= p.sum()
        q = np.clip(q, 1e-12, None); q /= q.sum()
        return float(jensenshannon(p, q))

    def _compute_drs(
        self,
        jsd: float,
        detection_f1: float,
        behavioral_entropy: float,
    ) -> float:
        """Detection Resistance Score: weighted combination of drift, detection drop, entropy."""
        jsd_score = min(jsd / 0.3, 1.0)           # normalized; 0.3 = empirical ceiling
        det_score = 1.0 - detection_f1             # higher evasion = lower F1
        ent_score = min(behavioral_entropy / np.log(24), 1.0)  # normalized entropy
        return round(0.4 * jsd_score + 0.4 * det_score + 0.2 * ent_score, 4)

    def run(
        self,
        initial_distributions: Dict[str, np.ndarray],
        normal_reference: np.ndarray,
        base_model_f1: float = 0.9992,
    ) -> pd.DataFrame:
        """
        Run CDE for n_rounds across all archetypes.

        Parameters
        ----------
        initial_distributions : dict mapping archetype name → initial hour distribution (24-bin)
        normal_reference      : 24-bin normal user reference distribution for mimicry strategy
        base_model_f1         : F1 of the base detection model before evolution

        Returns
        -------
        pd.DataFrame with columns: round, strategy, archetype, jsd, f1, drs, entropy
        """
        current = {k: np.array(v, dtype=float) for k, v in initial_distributions.items()}
        for k in current:
            current[k] = np.clip(current[k], 1e-12, None)
            current[k] /= current[k].sum()

        original = {k: v.copy() for k, v in current.items()}
        normal_reference = np.clip(normal_reference, 1e-12, None)
        normal_reference /= normal_reference.sum()

        records = []
        for r in range(self.n_rounds):
            strategy = self._get_strategy(r)
            round_jsds = []

            for arch in self.archetypes:
                prev = current[arch].copy()
                mutated = self._mutate_distribution(prev, strategy, normal_reference)
                current[arch] = mutated

                jsd = self._compute_jsd(original[arch], mutated)
                round_jsds.append(jsd)
                ent = float(entropy(mutated))

                # Simulate detection F1 degradation proportional to cumulative drift
                f1_drop = min(jsd * 0.25, 0.05)  # empirical: max 5% drop per archetype
                sim_f1 = max(base_model_f1 - f1_drop - self.rng.uniform(0, 0.002), 0.90)
                drs = self._compute_drs(jsd, sim_f1, ent)

                records.append({
                    "round": r + 1,
                    "strategy": strategy,
                    "archetype": arch,
                    "jsd": round(jsd, 4),
                    "f1": round(sim_f1, 4),
                    "entropy": round(ent, 4),
                    "drs": drs,
                })

        self.history = records
        return pd.DataFrame(records)

    def summary(self) -> pd.DataFrame:
        """Per-archetype final-round summary statistics."""
        df = pd.DataFrame(self.history)
        last = df[df["round"] == df["round"].max()]
        return last.groupby("archetype").agg(
            final_jsd=("jsd", "mean"),
            final_f1=("f1", "mean"),
            mean_drs=("drs", "mean"),
        ).reset_index().sort_values("final_jsd", ascending=False)
