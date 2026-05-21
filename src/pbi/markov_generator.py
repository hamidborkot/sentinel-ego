# ============================================================
# Phase 1: 3rd-Order Markov Chain PBI Trajectory Generator
# The Sentinel Ego — Persistent Behavioral Identity
# ============================================================

import numpy as np
import pandas as pd
from collections import defaultdict
from scipy.stats import entropy as scipy_entropy
from typing import Dict, List, Tuple
import json


MARKOV_ORDER = 3
HOURS = list(range(24))


def train_markov_chain(hour_sequences: List[List[int]], order: int = 3) -> dict:
    """
    Train an N-th order Markov chain on sending-hour sequences.
    Returns a transition probability dict: {(h1,h2,...,hN) -> {next_hour: prob}}
    """
    transitions = defaultdict(lambda: defaultdict(int))

    for seq in hour_sequences:
        if len(seq) <= order:
            continue
        for i in range(len(seq) - order):
            state = tuple(seq[i:i + order])
            next_h = seq[i + order]
            transitions[state][next_h] += 1

    # Normalize to probabilities
    probs = {}
    for state, counts in transitions.items():
        total = sum(counts.values())
        probs[state] = {h: c / total for h, c in counts.items()}

    print(f"  Markov chain: {len(probs):,} unique {order}-gram states")
    return probs


def sample_next_hour(state: tuple, probs: dict, rng: np.random.Generator) -> int:
    """Sample next hour from Markov chain; fallback to uniform if state unseen."""
    if state in probs:
        dist = probs[state]
        hours = list(dist.keys())
        weights = list(dist.values())
        return int(rng.choice(hours, p=weights))
    else:
        return int(rng.integers(6, 20))  # business-hours fallback


def generate_persona_trajectory(
    archetype_name: str,
    persona_id: int,
    markov_probs: dict,
    archetype_params: dict,
    n_days: int = 90,
    seed: int = None
) -> pd.DataFrame:
    """
    Generate a full N-day behavioral trajectory for one persona.
    Uses Markov chain for hour sequences and Poisson for daily email counts.
    """
    rng = np.random.default_rng(seed if seed is not None else persona_id * 1000)

    mean_emails_per_day = archetype_params.get("emails_per_active_day", 5.0)
    weekend_ratio = archetype_params.get("weekend_ratio", 0.02)
    mean_recipients = archetype_params.get("mean_recipients", 2.0)
    peak_hour = int(archetype_params.get("peak_hour", 9))

    # Anchor starting sequence from peak hour
    current_state = tuple([peak_hour] * MARKOV_ORDER)

    events = []
    base_date = pd.Timestamp("2003-01-01")

    for day_idx in range(n_days):
        current_date = base_date + pd.Timedelta(days=day_idx)
        dow = current_date.dayofweek
        is_weekend = dow >= 5

        # Weekend suppression
        if is_weekend and rng.random() > weekend_ratio * 10:
            continue

        n_emails = max(1, int(rng.poisson(mean_emails_per_day)))

        for _ in range(n_emails):
            hour = sample_next_hour(current_state, markov_probs, rng)
            recipients = max(1, int(rng.poisson(mean_recipients)))
            subject_len = max(5, int(rng.normal(35, 12)))

            events.append({
                "persona_id": f"{archetype_name}_P{persona_id}",
                "archetype": archetype_name,
                "date": current_date,
                "day_idx": day_idx,
                "hour": hour,
                "dayofweek": dow,
                "recipients": recipients,
                "subject_len": subject_len,
                "is_weekend": int(is_weekend),
            })

            # Advance Markov state
            current_state = tuple(list(current_state[1:]) + [hour])

    return pd.DataFrame(events)


def compute_jsd(p: np.ndarray, q: np.ndarray) -> float:
    """Jensen-Shannon Divergence between two distributions."""
    p = np.asarray(p, dtype=float) + 1e-12
    q = np.asarray(q, dtype=float) + 1e-12
    p /= p.sum()
    q /= q.sum()
    m = 0.5 * (p + q)
    return float(0.5 * scipy_entropy(p, m) + 0.5 * scipy_entropy(q, m))


def validate_persona_consistency(
    trajectory_df: pd.DataFrame,
    early_frac: float = 0.4,
    late_frac: float = 0.4
) -> dict:
    """Compute JSD between early and late behavioral distributions."""
    n = len(trajectory_df)
    early = trajectory_df.iloc[: int(n * early_frac)]
    late = trajectory_df.iloc[int(n * (1 - late_frac)) :]

    def hist24(series):
        h, _ = np.histogram(series, bins=np.arange(25))
        return h.astype(float) + 1e-9

    def hist8(series):
        h, _ = np.histogram(series, bins=np.arange(8))
        return h.astype(float) + 1e-9

    jsd_hour = compute_jsd(hist24(early["hour"]), hist24(late["hour"]))
    jsd_dow = compute_jsd(hist8(early["dayofweek"]), hist8(late["dayofweek"]))
    jsd_rec = compute_jsd(
        np.histogram(early["recipients"].clip(0, 20), bins=np.arange(22))[0].astype(float) + 1e-9,
        np.histogram(late["recipients"].clip(0, 20), bins=np.arange(22))[0].astype(float) + 1e-9,
    )

    jsd_mean = np.mean([jsd_hour, jsd_dow, jsd_rec])

    return {
        "jsd_hour": round(jsd_hour, 4),
        "jsd_dow": round(jsd_dow, 4),
        "jsd_recipients": round(jsd_rec, 4),
        "jsd_mean": round(jsd_mean, 4),
        "passes_target": jsd_mean < 0.10,
    }
