# ============================================================
# Phase 1: Enron Email Corpus Parser
# The Sentinel Ego — Persistent Behavioral Identity
# ============================================================

import os
import re
import tarfile
import urllib.request
from email import policy
from email.parser import BytesParser
from dateutil import parser as dtparser
import pandas as pd
import numpy as np
from tqdm import tqdm


ENRON_URL = "https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz"


def download_enron(raw_dir: str) -> str:
    """Download the official CMU Enron corpus tarball."""
    os.makedirs(raw_dir, exist_ok=True)
    tar_path = os.path.join(raw_dir, "enron_mail_20150507.tar.gz")
    if not os.path.exists(tar_path):
        print(f"Downloading Enron corpus from {ENRON_URL} ...")
        urllib.request.urlretrieve(ENRON_URL, tar_path)
        size_mb = os.path.getsize(tar_path) / 1024 / 1024
        print(f"Downloaded: {size_mb:.2f} MB")
    return tar_path


def extract_enron(tar_path: str, extract_dir: str) -> str:
    """Extract tarball and return path to the maildir root."""
    os.makedirs(extract_dir, exist_ok=True)
    if not os.listdir(extract_dir):
        print("Extracting archive...")
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(path=extract_dir)
    maildir = find_maildir(extract_dir)
    assert maildir is not None, "maildir not found after extraction"
    print(f"MAILDIR: {maildir}")
    return maildir


def find_maildir(root: str) -> str:
    """Recursively locate the maildir directory."""
    for current_root, dirs, _ in os.walk(root):
        if os.path.basename(current_root).lower() == "maildir":
            return current_root
    return None


def safe_parse_date(date_str: str):
    """Parse email date string to pandas Timestamp."""
    if not date_str or pd.isna(date_str):
        return pd.NaT
    try:
        dt = dtparser.parse(date_str)
        if dt.tzinfo is not None:
            dt = dt.replace(tzinfo=None)
        return pd.Timestamp(dt)
    except Exception:
        return pd.NaT


def count_recipients(x: str) -> int:
    """Count recipients in a To/CC/BCC field."""
    if not isinstance(x, str) or not x.strip():
        return 0
    parts = re.split(r"[;,]", x)
    return len([p.strip() for p in parts if p.strip()])


def parse_email_file(file_path: str, maildir: str) -> dict:
    """Parse a single email file into a record dict."""
    try:
        with open(file_path, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)

        from_ = str(msg.get("From", "")).strip().lower()
        to_ = str(msg.get("To", "")).strip().lower()
        cc_ = str(msg.get("Cc", "")).strip().lower()
        bcc_ = str(msg.get("Bcc", "")).strip().lower()
        subject_ = str(msg.get("Subject", "")).strip()
        date_raw = str(msg.get("Date", "")).strip()
        message_id = str(msg.get("Message-ID", "")).strip()

        folder = os.path.relpath(os.path.dirname(file_path), maildir)
        owner = folder.split(os.sep)[0].lower() if os.sep in folder else folder.lower()
        dt = safe_parse_date(date_raw)

        if pd.isna(dt):
            return None

        to_count = count_recipients(to_)
        cc_count = count_recipients(cc_)
        bcc_count = count_recipients(bcc_)

        return {
            "file_path": file_path,
            "owner": owner,
            "folder": folder.lower(),
            "from": from_,
            "to": to_,
            "cc": cc_,
            "bcc": bcc_,
            "subject": subject_,
            "date": dt,
            "message_id": message_id,
            "to_count": to_count,
            "cc_count": cc_count,
            "bcc_count": bcc_count,
            "recipient_total": to_count + cc_count + bcc_count,
            "subject_len": len(subject_),
            "is_sent_folder": int(any(k in folder.lower() for k in ["sent", "_sent_mail", "sent_items"])),
            "is_inbox_folder": int("inbox" in folder.lower()),
        }
    except Exception:
        return None


def parse_maildir(maildir: str) -> pd.DataFrame:
    """Walk the entire maildir and parse all email files."""
    email_files = []
    for root, _, files in os.walk(maildir):
        for f in files:
            email_files.append(os.path.join(root, f))

    print(f"Found {len(email_files):,} raw email files.")

    records = []
    for fp in tqdm(email_files, desc="Parsing emails"):
        rec = parse_email_file(fp, maildir)
        if rec is not None:
            records.append(rec)

    df = pd.DataFrame(records)
    df = df.drop_duplicates(subset=["message_id", "date", "owner", "subject"]).copy()
    df = df[df["owner"].notna() & df["date"].notna()].copy()

    df["hour"] = df["date"].dt.hour
    df["dayofweek"] = df["date"].dt.dayofweek
    df["date_only"] = df["date"].dt.date
    df["month"] = df["date"].dt.to_period("M").astype(str)

    print(f"Parsed {len(df):,} valid emails from {df['owner'].nunique()} users.")
    return df


def filter_eligible_users(df: pd.DataFrame,
                          min_sent: int = 200,
                          min_active_days: int = 30,
                          min_span_days: int = 60) -> list:
    """Return list of users meeting eligibility criteria."""
    sent = df[df["is_sent_folder"] == 1]
    stats = (
        sent.groupby("owner")
        .agg(
            total_sent=("message_id", "count"),
            active_days=("date_only", pd.Series.nunique),
            first_date=("date", "min"),
            last_date=("date", "max"),
        )
        .reset_index()
    )
    stats["span_days"] = (stats["last_date"] - stats["first_date"]).dt.days + 1

    eligible = stats[
        (stats["total_sent"] >= min_sent)
        & (stats["active_days"] >= min_active_days)
        & (stats["span_days"] >= min_span_days)
    ]["owner"].tolist()

    print(f"Eligible users: {len(eligible)} (out of {len(stats)})")
    return eligible
