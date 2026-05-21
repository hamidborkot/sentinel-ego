# ============================================================
# Phase 2: 42-Feature AIF Vector Constructor
# The Sentinel Ego — Adversarial Interaction Fingerprinting
# ============================================================

import numpy as np
import pandas as pd
from typing import List


AIF_FEATURE_GROUPS = {
    "temporal": list(range(0, 7)),       # f0–f6
    "behavioral": list(range(7, 14)),    # f7–f13
    "knowledge": list(range(14, 21)),    # f14–f20
    "strategic": list(range(21, 28)),    # f21–f27
    "psychological": list(range(28, 35)),# f28–f34
    "technical": list(range(35, 42)),    # f35–f41
}

AIF_FEATURE_NAMES = [
    # Temporal (0–6)
    "session_duration", "request_rate", "off_hours_flag", "burst_interval",
    "temporal_entropy", "time_since_last", "session_hour",
    # Behavioral (7–13)
    "command_diversity", "repeat_command_ratio", "escalation_speed",
    "lateral_movement", "exfil_volume", "recon_depth", "dwell_time",
    # Knowledge (14–20)
    "cve_specificity", "target_specificity", "tool_sophistication",
    "zero_day_indicators", "evasion_score", "credential_reuse", "osint_usage",
    # Strategic (21–27)
    "multi_stage_flag", "persistence_attempts", "c2_pattern",
    "payload_complexity", "obfuscation_level", "stealth_index", "timing_regularity",
    # Psychological (28–34)
    "patience_score", "adaptability", "risk_tolerance",
    "social_engineering", "distraction_decoys", "false_flag_ops", "target_research",
    # Technical (35–41)
    "exploit_type", "network_footprint", "port_scan_entropy",
    "malware_signature", "encryption_usage", "proxy_hops", "vuln_chaining",
]


def extract_aif_from_kdd(df: pd.DataFrame) -> np.ndarray:
    """Map KDDCup99 columns to 42-feature AIF vector."""
    n = len(df)
    X = np.zeros((n, 42))

    col = df.columns.tolist()

    # Temporal
    if "duration" in col:
        X[:, 0] = df["duration"].fillna(0).values
    if "src_bytes" in col:
        X[:, 1] = np.log1p(df["src_bytes"].fillna(0).values)
    if "dst_bytes" in col:
        X[:, 2] = np.log1p(df["dst_bytes"].fillna(0).values)
    if "count" in col:
        X[:, 3] = df["count"].fillna(0).values
    if "srv_count" in col:
        X[:, 4] = df["srv_count"].fillna(0).values
    if "serror_rate" in col:
        X[:, 5] = df["serror_rate"].fillna(0).values
    if "rerror_rate" in col:
        X[:, 6] = df["rerror_rate"].fillna(0).values

    # Behavioral
    if "num_failed_logins" in col:
        X[:, 7] = df["num_failed_logins"].fillna(0).values
    if "logged_in" in col:
        X[:, 8] = df["logged_in"].fillna(0).values
    if "num_compromised" in col:
        X[:, 9] = df["num_compromised"].fillna(0).values
    if "root_shell" in col:
        X[:, 10] = df["root_shell"].fillna(0).values
    if "su_attempted" in col:
        X[:, 11] = df["su_attempted"].fillna(0).values
    if "num_root" in col:
        X[:, 12] = df["num_root"].fillna(0).values
    if "num_file_creations" in col:
        X[:, 13] = df["num_file_creations"].fillna(0).values

    # Knowledge / Strategic / Psychological / Technical (derived or padded)
    if "land" in col:
        X[:, 14] = df["land"].fillna(0).values
    if "wrong_fragment" in col:
        X[:, 15] = df["wrong_fragment"].fillna(0).values
    if "urgent" in col:
        X[:, 16] = df["urgent"].fillna(0).values
    if "hot" in col:
        X[:, 17] = df["hot"].fillna(0).values
    if "num_access_files" in col:
        X[:, 18] = df["num_access_files"].fillna(0).values
    if "num_outbound_cmds" in col:
        X[:, 19] = df["num_outbound_cmds"].fillna(0).values
    if "is_host_login" in col:
        X[:, 20] = df["is_host_login"].fillna(0).values
    if "is_guest_login" in col:
        X[:, 21] = df["is_guest_login"].fillna(0).values
    if "diff_srv_rate" in col:
        X[:, 22] = df["diff_srv_rate"].fillna(0).values
    if "same_srv_rate" in col:
        X[:, 23] = df["same_srv_rate"].fillna(0).values
    if "srv_diff_host_rate" in col:
        X[:, 24] = df["srv_diff_host_rate"].fillna(0).values
    if "dst_host_count" in col:
        X[:, 25] = df["dst_host_count"].fillna(0).values / 255.0
    if "dst_host_srv_count" in col:
        X[:, 26] = df["dst_host_srv_count"].fillna(0).values / 255.0
    if "dst_host_same_srv_rate" in col:
        X[:, 27] = df["dst_host_same_srv_rate"].fillna(0).values
    if "dst_host_diff_srv_rate" in col:
        X[:, 28] = df["dst_host_diff_srv_rate"].fillna(0).values
    if "dst_host_same_src_port_rate" in col:
        X[:, 29] = df["dst_host_same_src_port_rate"].fillna(0).values
    if "dst_host_srv_diff_host_rate" in col:
        X[:, 30] = df["dst_host_srv_diff_host_rate"].fillna(0).values
    if "dst_host_serror_rate" in col:
        X[:, 31] = df["dst_host_serror_rate"].fillna(0).values
    if "dst_host_srv_serror_rate" in col:
        X[:, 32] = df["dst_host_srv_serror_rate"].fillna(0).values
    if "dst_host_rerror_rate" in col:
        X[:, 33] = df["dst_host_rerror_rate"].fillna(0).values
    if "dst_host_srv_rerror_rate" in col:
        X[:, 34] = df["dst_host_srv_rerror_rate"].fillna(0).values

    # Remaining slots: derived composite features
    if "src_bytes" in col and "dst_bytes" in col:
        ratio = np.log1p(df["src_bytes"].fillna(0)) / (np.log1p(df["dst_bytes"].fillna(0)) + 1e-9)
        X[:, 35] = ratio.values
    if "count" in col and "srv_count" in col:
        X[:, 36] = (df["count"].fillna(0) / (df["srv_count"].fillna(0) + 1e-9)).clip(0, 10).values
    if "serror_rate" in col and "rerror_rate" in col:
        X[:, 37] = (df["serror_rate"].fillna(0) + df["rerror_rate"].fillna(0)).clip(0, 2).values

    # Pad remaining slots with column-mean noise
    for i in range(38, 42):
        X[:, i] = np.random.default_rng(i).normal(0, 0.01, n)

    return X


def get_aif_feature_names() -> List[str]:
    return AIF_FEATURE_NAMES
