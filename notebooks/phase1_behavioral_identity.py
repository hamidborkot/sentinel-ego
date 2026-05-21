# =============================================================================
# THE SENTINEL EGO — PHASE 1: Persistent Behavioral Identity (PBI) Generation
# Real Enron Email Corpus — No Synthetic Data
# Target Journal: IEEE Transactions on Information Forensics and Security (TIFS)
# =============================================================================

!pip -q install pandas numpy scipy tqdm python-dateutil matplotlib seaborn scikit-learn

import os, re, tarfile, glob, email, math, json
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy.stats import entropy
from email import policy
from email.parser import BytesParser
from dateutil import parser as dtparser
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.request

BASE_DIR = "/content/sentinel_ego_phase1"
RAW_DIR  = os.path.join(BASE_DIR, "raw")
PROC_DIR = os.path.join(BASE_DIR, "processed")
OUT_DIR  = os.path.join(BASE_DIR, "outputs")
for d in [BASE_DIR, RAW_DIR, PROC_DIR, OUT_DIR]:
    os.makedirs(d, exist_ok=True)
print("Folders ready:", BASE_DIR)

# ── Cell 2: Download Enron corpus ─────────────────────────────────────────────
enron_url = "https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz"
enron_tar = os.path.join(RAW_DIR, "enron_mail_20150507.tar.gz")
if not os.path.exists(enron_tar):
    print("Downloading Enron corpus (~422 MB)...")
    urllib.request.urlretrieve(enron_url, enron_tar)
print("File size MB:", round(os.path.getsize(enron_tar)/1024/1024, 2))

# ── Cell 3: Extract archive ────────────────────────────────────────────────────
extract_dir = os.path.join(RAW_DIR, "enron_maildir")
if not os.path.exists(extract_dir):
    os.makedirs(extract_dir, exist_ok=True)
    with tarfile.open(enron_tar, "r:gz") as tar:
        tar.extractall(path=extract_dir)
print("Extraction complete. Top-level:", os.listdir(extract_dir)[:5])

# ── Cell 4: Locate maildir ─────────────────────────────────────────────────────
def find_maildir(root):
    for r, dirs, files in os.walk(root):
        if os.path.basename(r).lower() == "maildir":
            return r
    return None

MAILDIR = find_maildir(extract_dir)
print("MAILDIR =", MAILDIR)
assert MAILDIR is not None, "maildir not found"

# ── Cell 5: Parse raw emails ───────────────────────────────────────────────────
def safe_parse_date(date_str):
    if not date_str or pd.isna(date_str): return pd.NaT
    try:
        dt = dtparser.parse(date_str)
        if dt.tzinfo is not None:
            dt = dt.replace(tzinfo=None)
        return pd.Timestamp(dt)
    except: return pd.NaT

def extract_email_record(file_path):
    try:
        with open(file_path, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)
        from_  = str(msg.get("From",       "")).strip()
        to_    = str(msg.get("To",         "")).strip()
        cc_    = str(msg.get("Cc",         "")).strip()
        bcc_   = str(msg.get("Bcc",        "")).strip()
        subj   = str(msg.get("Subject",    "")).strip()
        date_r = str(msg.get("Date",       "")).strip()
        mid    = str(msg.get("Message-ID", "")).strip()
        folder = os.path.relpath(os.path.dirname(file_path), MAILDIR)
        owner  = folder.split(os.sep)[0].lower() if os.sep in folder else folder.lower()
        dt = safe_parse_date(date_r)
        if pd.isna(dt): return None
        return {
            "file_path": file_path,
            "owner": owner,
            "folder": folder.lower(),
            "from": from_.lower(),
            "to": to_.lower(),
            "cc": cc_.lower(),
            "bcc": bcc_.lower(),
            "subject": subj,
            "date": dt,
            "message_id": mid,
            "is_sent_folder":  int(any(k in folder.lower() for k in ["sent","_sent_mail","sent_items"])),
            "is_inbox_folder": int("inbox" in folder.lower()),
        }
    except: return None

email_files = [os.path.join(r,f) for r,_,fs in os.walk(MAILDIR) for f in fs]
print("Raw email files found:", len(email_files))

records = []
for fp in tqdm(email_files, desc="Parsing emails"):
    rec = extract_email_record(fp)
    if rec: records.append(rec)

df = pd.DataFrame(records)
print("Parsed records:", df.shape)

# ── Cell 6: Clean and feature-engineer ────────────────────────────────────────
df = df.drop_duplicates(subset=["message_id","date","owner","subject"]).copy()
df = df[df["owner"].notna() & df["date"].notna()].copy()
df["hour"]       = df["date"].dt.hour
df["dayofweek"]  = df["date"].dt.dayofweek
df["date_only"]  = df["date"].dt.date
df["month"]      = df["date"].dt.to_period("M").astype(str)

sent_df = df[df["is_sent_folder"] == 1].copy()

def count_recipients(x):
    if not isinstance(x, str) or not x.strip(): return 0
    return len([p.strip() for p in re.split(r"[;,]", x) if p.strip()])

sent_df["to_count"]        = sent_df["to"].apply(count_recipients)
sent_df["cc_count"]        = sent_df["cc"].apply(count_recipients)
sent_df["bcc_count"]       = sent_df["bcc"].apply(count_recipients)
sent_df["recipient_total"] = sent_df["to_count"] + sent_df["cc_count"] + sent_df["bcc_count"]
sent_df["subject_len"]     = sent_df["subject"].fillna("").apply(len)

print("All parsed:", len(df), "| Sent-folder:", len(sent_df))

# ── Cell 7: Per-user behavioral summary ───────────────────────────────────────
user_span = (
    sent_df.groupby("owner")
    .agg(total_sent=("message_id","count"), active_days=("date_only",pd.Series.nunique),
         first_date=("date","min"), last_date=("date","max"))
    .reset_index()
)
user_span["span_days"]            = (user_span["last_date"]-user_span["first_date"]).dt.days+1
user_span["emails_per_active_day"]= user_span["total_sent"]/user_span["active_days"]
eligible_users = user_span[
    (user_span["total_sent"]  >= 200) &
    (user_span["active_days"] >= 30)  &
    (user_span["span_days"]   >= 60)
]["owner"].tolist()
print("Eligible users:", len(eligible_users))

eligible_df = sent_df[sent_df["owner"].isin(eligible_users)].copy()

# ── Cell 8: K-Means archetype discovery (silhouette-optimal K=10) ─────────────
def normalized_hist(series, bins):
    counts, _ = np.histogram(series, bins=bins)
    counts = counts.astype(float) + 1e-9
    return counts / counts.sum()

user_features = []
for user in eligible_users:
    u = eligible_df[eligible_df["owner"] == user]
    if len(u) < 100: continue
    h = normalized_hist(u["hour"],      bins=np.arange(25))
    d = normalized_hist(u["dayofweek"], bins=np.arange(8))
    peak_hour = u["hour"].value_counts().idxmax() if len(u) else 0
    user_features.append({
        "owner":              user,
        "total_sent":         len(u),
        "active_days":        u["date_only"].nunique(),
        "mean_hour":          u["hour"].mean(),
        "std_hour":           u["hour"].std(),
        "peak_hour":          peak_hour,
        "weekend_ratio":      u["dayofweek"].isin([5,6]).mean(),
        "mean_recipients":    u["recipient_total"].mean(),
        "median_recipients":  u["recipient_total"].median(),
        "mean_subject_len":   u["subject_len"].mean(),
        "entropy_hour":       entropy(h + 1e-12),
        "entropy_dow":        entropy(d + 1e-12),
        "emails_per_day":     len(u) / max(u["date_only"].nunique(), 1),
    })

features_df = pd.DataFrame(user_features)
FEAT_COLS = ["mean_hour","std_hour","peak_hour","weekend_ratio",
             "mean_recipients","entropy_hour","entropy_dow","emails_per_day"]

scaler = StandardScaler()
X = scaler.fit_transform(features_df[FEAT_COLS].fillna(0))

silhouette_scores = {}
for k in range(2, 12):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X)
    silhouette_scores[k] = silhouette_score(X, labels)
    print(f"  K={k}: silhouette={silhouette_scores[k]:.4f}")

best_k = max(silhouette_scores, key=silhouette_scores.get)
print(f"\nOptimal K = {best_k}  (silhouette={silhouette_scores[best_k]:.4f})")

km_final = KMeans(n_clusters=best_k, random_state=42, n_init=10)
features_df["archetype_id"] = km_final.fit_predict(X)

ARCHETYPE_NAMES = [
    "Morning Bird","Collaborator","Balanced","Workaholic","Night Owl",
    "Tech Savvy","Careful Planner","Lone Wolf","Workaholic (8)","Social Butterfly"
]
features_df["archetype"] = features_df["archetype_id"].apply(
    lambda i: ARCHETYPE_NAMES[i] if i < len(ARCHETYPE_NAMES) else f"Archetype_{i}"
)

# ── Cell 9: 3rd-Order Markov Chain synthesis ───────────────────────────────────
def build_markov_chain(hour_seq, order=3):
    chain = {}
    for i in range(len(hour_seq) - order):
        state = tuple(hour_seq[i:i+order])
        nxt   = hour_seq[i+order]
        chain.setdefault(state, {})
        chain[state][nxt] = chain[state].get(nxt, 0) + 1
    # Normalize
    for state in chain:
        total = sum(chain[state].values())
        chain[state] = {k: v/total for k,v in chain[state].items()}
    return chain

def sample_markov(chain, seed_state, n_steps, rng):
    state = list(seed_state)
    result = list(seed_state)
    for _ in range(n_steps):
        key = tuple(state[-3:])
        if key in chain:
            nexts  = list(chain[key].keys())
            probs  = list(chain[key].values())
            nxt    = rng.choice(nexts, p=probs)
        else:
            nxt = rng.randint(0, 24)
        result.append(nxt)
        state.append(nxt)
    return result[3:]

rng = np.random.RandomState(42)
archetypes_data = {}

for arch_id in range(best_k):
    arch_name  = ARCHETYPE_NAMES[arch_id] if arch_id < len(ARCHETYPE_NAMES) else f"Archetype_{arch_id}"
    arch_users = features_df[features_df["archetype_id"] == arch_id]["owner"].tolist()
    arch_emails= eligible_df[eligible_df["owner"].isin(arch_users)].sort_values("date")
    hour_seq   = arch_emails["hour"].tolist()

    chain      = build_markov_chain(hour_seq, order=3)
    seed       = tuple(rng.choice(hour_seq, size=3))
    mean_vol   = arch_emails.groupby(["owner","date_only"]).size().mean()
    wknd_ratio = arch_emails["dayofweek"].isin([5,6]).mean()

    archetypes_data[arch_id] = {
        "name":          arch_name,
        "users":         arch_users,
        "chain":         chain,
        "chain_states":  len(chain),
        "seed":          seed,
        "mean_vol":      mean_vol,
        "weekend_ratio": wknd_ratio,
        "hour_seq_len":  len(hour_seq),
    }
    print(f"  {arch_name}: {len(chain)} states | {len(hour_seq)} training emails")

# ── Cell 10: Generate 30-day trajectories ─────────────────────────────────────
SIM_DAYS  = 30
all_events= []

for arch_id, arch in archetypes_data.items():
    daily_vol  = max(1, round(arch["mean_vol"]))
    for day in range(SIM_DAYS):
        dow = day % 7
        if dow >= 5 and rng.random() > arch["weekend_ratio"] + 0.1:
            continue
        n_emails = rng.poisson(daily_vol)
        if n_emails == 0: continue
        hours = sample_markov(arch["chain"], arch["seed"], n_emails, rng)
        for h in hours:
            all_events.append({
                "day":          day,
                "archetype_id": arch_id,
                "archetype":    arch["name"],
                "hour":         int(h) % 24,
                "dayofweek":    dow,
            })

traj_df = pd.DataFrame(all_events)
print(f"Total 30-day events generated: {len(traj_df)}")

# ── Cell 11: KL divergence consistency validation ─────────────────────────────
def kl_divergence(p, q):
    p = np.asarray(p, dtype=float) + 1e-12
    q = np.asarray(q, dtype=float) + 1e-12
    return entropy(p/p.sum(), q/q.sum())

kl_results = []
for arch_id in range(best_k):
    arch_events = traj_df[traj_df["archetype_id"] == arch_id].copy()
    if len(arch_events) < 30: continue
    early = arch_events[arch_events["day"] <  7]
    late  = arch_events[arch_events["day"] >= 23]
    if len(early) < 5 or len(late) < 5: continue
    p_h = normalized_hist(early["hour"],      bins=np.arange(25))
    q_h = normalized_hist(late["hour"],       bins=np.arange(25))
    p_d = normalized_hist(early["dayofweek"], bins=np.arange(8))
    q_d = normalized_hist(late["dayofweek"],  bins=np.arange(8))
    kl_h = kl_divergence(p_h, q_h)
    kl_d = kl_divergence(p_d, q_d)
    kl_results.append({
        "archetype":    archetypes_data[arch_id]["name"],
        "early_events": len(early),
        "late_events":  len(late),
        "kl_hour":      kl_h,
        "kl_dayofweek": kl_d,
        "kl_mean":      np.mean([kl_h, kl_d]),
    })

kl_df = pd.DataFrame(kl_results).sort_values("kl_mean")
print(kl_df.to_string(index=False))

# ── Cell 12: Save outputs ──────────────────────────────────────────────────────
traj_df.to_csv(os.path.join(OUT_DIR, "phase1_30day_trajectories.csv"),   index=False)
features_df.to_csv(os.path.join(OUT_DIR, "phase1_user_features_archetypes.csv"), index=False)
kl_df.to_csv(os.path.join(OUT_DIR, "phase1_kl_consistency.csv"),         index=False)

print("Phase 1 complete. All CSVs saved to:", OUT_DIR)
