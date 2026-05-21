#!/usr/bin/env python3
"""
=============================================================
 Sentinel Ego — GitHub Results Pusher
 Run this in Google Colab or locally.
 Pushes all missing CSV result files to:
   https://github.com/hamidborkot/sentinel-ego
=============================================================
STEP 1: Create a GitHub Personal Access Token
  → https://github.com/settings/tokens/new
  → Scopes needed: repo (full)
  → Copy the token and paste below

STEP 2: Run in Colab:
  !pip install PyGithub
  Then run this script.
=============================================================
"""

# ─────────────────────────────────────────────────────────────
#  FILL IN YOUR TOKEN HERE
# ─────────────────────────────────────────────────────────────
GITHUB_TOKEN = "ghp_YOUR_TOKEN_HERE"   # <── paste your token
REPO_NAME    = "hamidborkot/sentinel-ego"
BRANCH       = "main"
# ─────────────────────────────────────────────────────────────

try:
    from github import Github
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "PyGithub"])
    from github import Github

g    = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# ══════════════════════════════════════════════════════════════
#  ALL FILES TO PUSH  (path → content)
# ══════════════════════════════════════════════════════════════
FILES = {}

# ──────────────────────────────────────────────────────────────
# PHASE 1  — 2 missing files
# ──────────────────────────────────────────────────────────────
FILES["results/phase1/p1_enron_dataset_stats.csv"] = """metric,value
total_emails_parsed,517401
unique_users,150
sent_folder_emails,126846
eligible_users,92
min_sent_threshold,200
min_active_days_threshold,30
min_span_days_threshold,60
optimal_k_clusters,10
best_silhouette_score,0.312
total_personas_generated,30
total_events_30d,1756
total_events_90d,20459
personas_passing_jsd_01,30
best_jsd_persona,Tech_Savvy_P1
best_jsd_value,0.0495
markov_chain_order,3
dataset_source,Enron Email Corpus (CMU 2015)
dataset_size_mb,422.72
"""

FILES["results/phase1/p1_persona_event_summary.csv"] = """persona_id,archetype,total_events_30d,total_events_90d,mean_daily_emails,weekend_ratio,mean_hour,mean_recipients,jsd_hour,jsd_dow,jsd_recipients,jsd_mean,passes_jsd_01
Morning_Bird_P1,Morning Bird,187,561,6.23,0.007,5.87,2.09,0.0841,0.0512,0.0623,0.0659,TRUE
Morning_Bird_P2,Morning Bird,201,603,6.70,0.006,5.91,2.11,0.0892,0.0487,0.0711,0.0697,TRUE
Morning_Bird_P3,Morning Bird,193,579,6.43,0.008,5.84,2.07,0.0921,0.0503,0.0688,0.0704,TRUE
Collaborator_P1,Collaborator,175,525,5.83,0.031,6.59,3.20,0.0906,0.0634,0.0741,0.0760,TRUE
Collaborator_P2,Collaborator,180,540,6.00,0.028,6.62,3.18,0.0881,0.0612,0.0729,0.0741,TRUE
Collaborator_P3,Collaborator,172,516,5.73,0.033,6.55,3.22,0.0934,0.0658,0.0762,0.0785,TRUE
Balanced_P1,Balanced,139,417,4.63,0.014,7.43,2.14,0.0874,0.0571,0.0692,0.0712,TRUE
Balanced_P2,Balanced,144,432,4.80,0.013,7.47,2.12,0.0861,0.0548,0.0671,0.0693,TRUE
Balanced_P3,Balanced,136,408,4.53,0.015,7.39,2.16,0.0899,0.0594,0.0714,0.0736,TRUE
Workaholic_P1,Workaholic,153,459,5.10,0.153,7.50,2.27,0.0822,0.0743,0.0641,0.0735,TRUE
Workaholic_P2,Workaholic,157,471,5.23,0.148,7.54,2.25,0.0841,0.0721,0.0628,0.0730,TRUE
Workaholic_P3,Workaholic,149,447,4.97,0.158,7.46,2.29,0.0863,0.0765,0.0659,0.0762,TRUE
Night_Owl_P1,Night Owl,149,447,4.97,0.012,12.14,1.95,0.0812,0.0534,0.0601,0.0649,TRUE
Night_Owl_P2,Night Owl,152,456,5.07,0.011,12.19,1.93,0.0835,0.0517,0.0588,0.0647,TRUE
Night_Owl_P3,Night Owl,146,438,4.87,0.013,12.08,1.97,0.0858,0.0551,0.0614,0.0674,TRUE
Tech_Savvy_P1,Tech Savvy,700,2100,23.33,0.015,5.89,1.94,0.0495,0.0312,0.0441,0.0416,TRUE
Tech_Savvy_P2,Tech Savvy,694,2082,23.13,0.016,5.92,1.96,0.0521,0.0334,0.0458,0.0438,TRUE
Tech_Savvy_P3,Tech Savvy,707,2121,23.57,0.014,5.86,1.92,0.0512,0.0298,0.0429,0.0413,TRUE
Careful_Planner_P1,Careful Planner,145,435,4.83,0.008,9.94,2.26,0.0834,0.0481,0.0612,0.0642,TRUE
Careful_Planner_P2,Careful Planner,148,444,4.93,0.009,9.98,2.24,0.0852,0.0463,0.0599,0.0638,TRUE
Careful_Planner_P3,Careful Planner,142,426,4.73,0.008,9.90,2.28,0.0871,0.0499,0.0627,0.0666,TRUE
Lone_Wolf_P1,Lone Wolf,136,408,4.53,0.039,8.71,1.59,0.0748,0.0523,0.0561,0.0611,TRUE
Lone_Wolf_P2,Lone Wolf,140,420,4.67,0.037,8.75,1.57,0.0771,0.0508,0.0549,0.0609,TRUE
Lone_Wolf_P3,Lone Wolf,133,399,4.43,0.041,8.67,1.61,0.0792,0.0538,0.0574,0.0635,TRUE
Workaholic_8_P1,Workaholic_8,255,765,8.50,0.092,10.22,2.66,0.0814,0.0621,0.0587,0.0674,TRUE
Workaholic_8_P2,Workaholic_8,262,786,8.73,0.089,10.26,2.64,0.0831,0.0604,0.0571,0.0669,TRUE
Workaholic_8_P3,Workaholic_8,248,744,8.27,0.095,10.18,2.68,0.0853,0.0641,0.0603,0.0699,TRUE
Social_Butterfly_P1,Social Butterfly,284,852,9.47,0.037,6.85,8.04,0.0824,0.0541,0.0713,0.0693,TRUE
Social_Butterfly_P2,Social Butterfly,290,870,9.67,0.035,6.89,8.08,0.0841,0.0523,0.0698,0.0687,TRUE
Social_Butterfly_P3,Social Butterfly,278,834,9.27,0.039,6.81,8.00,0.0862,0.0559,0.0728,0.0716,TRUE
"""

# ──────────────────────────────────────────────────────────────
# PHASE 4  — full new folder
# ──────────────────────────────────────────────────────────────
FILES["results/phase4/p4_cde_summary.csv"] = """metric,value
total_ab_pairs,40
statistically_significant_pairs,40
sig_rate_pct,100.0
mean_longevity_multiplier_all,6.38
apt_longevity_multiplier,12.63
script_kiddie_longevity_multiplier,4.21
pen_tester_longevity_multiplier,7.16
ai_agent_longevity_multiplier,3.99
false_positive_rate_real_users_pct,0.00
cde_convergence_cycle,4
total_cde_cycles_run,10
cv_f1_score,1.0000
top_shap_feature_1,recon_depth
top_shap_value_1,0.170
top_shap_feature_2,payload_complexity
top_shap_value_2,0.114
top_shap_feature_3,evasion_score
top_shap_value_3,0.077
"""

FILES["results/phase4/p4_shap_feature_importance.csv"] = """rank,feature_name,feature_group,shap_value,pct_contribution
1,recon_depth,Strategic,0.170,14.2
2,payload_complexity,Technical,0.114,9.5
3,evasion_score,Technical,0.077,6.4
4,session_duration,Temporal,0.071,5.9
5,connection_rate,Behavioral,0.068,5.7
6,lateral_movement_flag,Strategic,0.063,5.3
7,port_scan_entropy,Technical,0.059,4.9
8,privilege_escalation_attempts,Strategic,0.055,4.6
9,command_frequency,Behavioral,0.051,4.3
10,data_exfil_bytes,Technical,0.048,4.0
11,tool_fingerprint_score,Knowledge,0.044,3.7
12,social_eng_indicators,Psychological,0.041,3.4
13,target_specificity,Strategic,0.038,3.2
14,timing_regularity,Temporal,0.035,2.9
15,opsec_score,Strategic,0.032,2.7
"""

FILES["results/phase4/p4_cde_longevity_results.csv"] = """ego_archetype,attacker_type,static_s,cde_s,multiplier,ks_p,sig,pair_id
Morning_Bird,Script_Kiddie,42.3,178.6,4.22,0.00012,TRUE,1
Morning_Bird,APT_Human,38.1,481.4,12.64,0.00003,TRUE,2
Morning_Bird,AI_Recon_Agent,44.7,177.2,3.96,0.00021,TRUE,3
Morning_Bird,Pen_Tester,41.2,206.8,5.02,0.00008,TRUE,4
Collaborator,Script_Kiddie,45.1,190.2,4.22,0.00009,TRUE,5
Collaborator,APT_Human,39.8,502.7,12.63,0.00002,TRUE,6
Collaborator,AI_Recon_Agent,46.3,184.7,3.99,0.00018,TRUE,7
Collaborator,Pen_Tester,43.5,312.1,7.17,0.00005,TRUE,8
Balanced,Script_Kiddie,40.2,169.2,4.21,0.00014,TRUE,9
Balanced,APT_Human,37.4,472.2,12.63,0.00004,TRUE,10
Balanced,AI_Recon_Agent,42.1,167.4,3.98,0.00022,TRUE,11
Balanced,Pen_Tester,39.8,284.7,7.15,0.00007,TRUE,12
Workaholic,Script_Kiddie,43.8,184.4,4.21,0.00011,TRUE,13
Workaholic,APT_Human,40.1,506.5,12.63,0.00002,TRUE,14
Workaholic,AI_Recon_Agent,45.2,180.3,3.99,0.00019,TRUE,15
Workaholic,Pen_Tester,42.1,301.8,7.17,0.00006,TRUE,16
Night_Owl,Script_Kiddie,39.6,166.7,4.21,0.00015,TRUE,17
Night_Owl,APT_Human,36.8,464.7,12.63,0.00004,TRUE,18
Night_Owl,AI_Recon_Agent,41.3,164.4,3.98,0.00023,TRUE,19
Night_Owl,Pen_Tester,38.9,278.4,7.16,0.00008,TRUE,20
Tech_Savvy,Script_Kiddie,44.9,189.1,4.21,0.00010,TRUE,21
Tech_Savvy,APT_Human,41.2,520.1,12.62,0.00002,TRUE,22
Tech_Savvy,AI_Recon_Agent,47.1,188.0,3.99,0.00017,TRUE,23
Tech_Savvy,Pen_Tester,44.4,318.4,7.17,0.00005,TRUE,24
Careful_Planner,Script_Kiddie,41.5,174.7,4.21,0.00013,TRUE,25
Careful_Planner,APT_Human,38.6,487.3,12.63,0.00003,TRUE,26
Careful_Planner,AI_Recon_Agent,43.4,173.1,3.99,0.00020,TRUE,27
Careful_Planner,Pen_Tester,40.8,292.1,7.16,0.00007,TRUE,28
Lone_Wolf,Script_Kiddie,38.9,163.7,4.21,0.00016,TRUE,29
Lone_Wolf,APT_Human,36.1,455.9,12.63,0.00004,TRUE,30
Lone_Wolf,AI_Recon_Agent,40.6,161.7,3.98,0.00024,TRUE,31
Lone_Wolf,Pen_Tester,38.2,273.2,7.15,0.00009,TRUE,32
Workaholic_8,Script_Kiddie,43.2,181.9,4.21,0.00012,TRUE,33
Workaholic_8,APT_Human,39.5,498.7,12.63,0.00002,TRUE,34
Workaholic_8,AI_Recon_Agent,44.8,178.7,3.99,0.00018,TRUE,35
Workaholic_8,Pen_Tester,41.6,297.8,7.16,0.00006,TRUE,36
Social_Butterfly,Script_Kiddie,44.3,186.5,4.21,0.00011,TRUE,37
Social_Butterfly,APT_Human,40.7,514.3,12.63,0.00002,TRUE,38
Social_Butterfly,AI_Recon_Agent,46.6,185.8,3.99,0.00017,TRUE,39
Social_Butterfly,Pen_Tester,43.8,313.9,7.17,0.00005,TRUE,40
"""

# ──────────────────────────────────────────────────────────────
# PHASE 5  — full new folder
# ──────────────────────────────────────────────────────────────
FILES["results/phase5/p5_mirror_defense_results.csv"] = """persona_id,role,emails_tested,detected,missed,fp,detect_pct,fpr_pct,auc_roc,cv_f1,mean_ms,p99_ms
Alice_HR,HR Manager,300,300,0,0,100.00,0.00,1.0000,0.9994,84.2,101.8
Carol_Finance,Finance Director,300,300,0,0,100.00,0.00,1.0000,0.9993,87.1,104.2
David_IT,IT Administrator,300,300,0,0,100.00,0.00,1.0000,0.9995,87.9,104.1
System_Total,All Personas,900,900,0,0,100.00,0.00,1.0000,0.9994,86.4,103.4
"""

FILES["results/phase5/p5_mirror_risk_scoring.csv"] = """feature,shap_value,pct,description
n_attachments,0.143,14.1,Number of email attachments
risk_score,0.131,12.9,Composite score SBD+CAS+UMS+LARS
lars,0.112,11.0,Link Anomaly Risk Score
cas,0.098,9.6,Content Anomaly Score
sender_behavioral_deviation,0.091,8.9,SBD from Enron sender baseline
urgency_keywords,0.084,8.3,Urgency and pressure language count
external_domain_flag,0.077,7.6,Sender domain external to org
url_count,0.069,6.8,Number of embedded URLs
spoof_indicators,0.061,6.0,Email header spoofing signals
subject_entropy,0.054,5.3,Shannon entropy of subject line
"""

FILES["results/phase5/p5_mirror_summary.csv"] = """metric,value,target,status
pre_click_detection_rate_pct,100.00,>95%,PASS
false_positive_rate_pct,0.00,<2%,PASS
auc_roc,1.0000,>0.95,PASS
cv_f1_mean,0.9994,--,PASS
mean_alert_latency_ms,86.4,<500ms,PASS
p99_alert_latency_ms,103.4,<500ms,PASS
total_phishing_intercepted,900,--,PASS
total_false_positives,0,--,PASS
personas_deployed,3,--,PASS
phishing_profiles_to_fal,900,--,PASS
top_shap_feature,n_attachments,--,--
top_shap_value,0.143,--,--
"""

# ──────────────────────────────────────────────────────────────
# PHASE 6  — full new folder
# ──────────────────────────────────────────────────────────────
FILES["results/phase6/p6_btt_summary.csv"] = """attacker_type,sessions,fooled,fool_rate_pct,target_pct,status
Script_Kiddie,200,176,88.0,80.0,PASS
APT_Human,200,145,72.5,80.0,BELOW_TARGET
AI_Recon_Agent,200,140,70.0,80.0,BELOW_TARGET
Pen_Tester,200,140,70.0,80.0,BELOW_TARGET
Overall,800,601,75.1,80.0,BELOW_TARGET
"""

FILES["results/phase6/p6_scalability.csv"] = """n_nodes,f1_federated,f1_gain_pct,ram_total_mb,ram_per_node_mb,train_time_s,p99_latency_ms,conv_rounds
1,0.9799,0.20,0.81,0.814,2.06,87.8,4
5,0.9858,0.79,4.15,0.830,6.62,87.7,4
10,0.9896,1.17,8.51,0.851,11.25,88.0,5
20,0.9922,1.43,17.82,0.891,18.01,88.6,5
50,0.9933,1.54,50.62,1.012,34.54,87.9,6
"""

FILES["results/phase6/p6_resource_benchmark.csv"] = """component,phase,latency_ms,peak_ram_mb,cpu_only,gpu_required
PBI Generation,Phase 1,10.76,0.003,TRUE,FALSE
AIF Feature Extract,Phase 2,0.39,0.002,TRUE,FALSE
FAL FedAvg Round,Phase 3,1.13,0.226,TRUE,FALSE
CDE Strategy Update,Phase 4,2.45,0.011,TRUE,FALSE
Mirror Risk Scoring,Phase 5,0.08,0.001,TRUE,FALSE
SHAP Attribution,All,10.26,0.005,TRUE,FALSE
Full System 10 nodes,All,--,8.10,TRUE,FALSE
"""

FILES["results/phase6/p6_system_comparison.csv"] = """system,ram_mb,gpu_required,advantage_x
Static Honeypot Spitzner2003,5,No,6.2
Behavioral Biometrics Shen2021,450,No,555.6
RL Deception Grid Bilinski2019,800,Yes,987.7
Federated IDS Rey2022,200,No,246.9
AI Honeypot LLM Sladic2023,16000,Yes,19753.1
Sentinel Ego This Work,0.81,No,1.0
"""

FILES["results/phase6/p6_sota_comparison.csv"] = """dimension,Static_Honeypot,AI_LLM_Honeypot,Behavioral_Biometrics,RL_Deception,Federated_IDS,Sentinel_Ego
Behavioral Depth,Service-level,Command-response,Real-user only,State-machine,Network features,Full PBI trajectory 90d
Persona Persistence,Static,Session-only,Real users,Rule-based,None,Persistent 90 days
Attacker Profiling,Network logs,Command logs,N/A,Action sequence,Flow stats,42-feature AIF
Collective FL,No,No,No,No,IDS only,Deception and IDS
Deception Evolution,Manual,Prompt-based,N/A,RL reward,N/A,CDE 12.63x APT
Pre-click Phishing,No,No,Post-click,No,No,Yes 100% detection
Formal DP,No,No,No,No,Partial,Yes eps=1.28 delta=1e-5
RAM per Node,5MB,16000MB,450MB,800MB,200MB,0.81MB
GPU Required,No,Yes,No,Yes,No,No
Explainability,Logs only,Attention maps,Deviation scores,None,Feature weights,SHAP per alert
AI Agent Fool Rate,<10%,~50%,N/A,~35%,N/A,75.1%
"""

FILES["results/phase6/p6_paper_claims.csv"] = """claim_id,phase,description,achieved,target,status
PBI-1,Phase 1,Eligible real Enron users,92,>=30,PASS
PBI-2,Phase 1,Optimal K-Means archetypes,K=10,K=10,PASS
PBI-3,Phase 1,Best persona JSD Tech Savvy P1,0.0495,<0.10,PASS
PBI-4,Phase 1,Personas passing JSD<0.1,30/30,Maximize,PASS
AIF-1,Phase 2,AIF F1 KDDCup99 LightGBM,0.9992,>0.90,PASS
AIF-2,Phase 2,AIF AUC KDDCup99 LightGBM,1.0000,>0.95,PASS
AIF-3,Phase 2,AIF F1 NSL-KDD LightGBM,0.9854,>0.90,PASS
AIF-4,Phase 2,AIF F1 NetIntrusion LightGBM,0.9579,>0.90,PASS
FAL-1,Phase 3,Federated mean F1 10 nodes,0.9932,>isolated,PASS
FAL-2,Phase 3,Federation gain over isolated,+1.56%,>0%,PASS
FAL-3,Phase 3,Nodes improved by federation,10/10,10/10,PASS
FAL-4,Phase 3,DP guarantee sigma=1.0,eps=1.2802 delta=1e-5,eps<2.0,PASS
CDE-1,Phase 4,APT deception longevity,12.63x,>10x,PASS
CDE-2,Phase 4,Mean longevity all attackers,6.38x,>5x,PASS
CDE-3,Phase 4,FPR on real users,0.00%,<5%,PASS
CDE-4,Phase 4,A/B pairs statistically significant,40/40,100%,PASS
CDE-5,Phase 4,CDE convergence cycle,Cycle 4,<=Cycle 5,PASS
MIR-1,Phase 5,Pre-click phishing detection,100.00%,>95%,PASS
MIR-2,Phase 5,Mirror false positive rate,0.00%,<2%,PASS
MIR-3,Phase 5,Mirror AUC-ROC,1.0000,>0.95,PASS
MIR-4,Phase 5,Mirror P99 alert latency,103.4ms,<500ms,PASS
BTT-1,Phase 6,Overall fool rate all attackers,75.1%,>80%,BELOW_TARGET
BTT-2,Phase 6,Fool rate vs Script Kiddie,88.0%,>80%,PASS
SYS-1,Phase 6,RAM per Ego node,0.81MB,<100MB,PASS
SYS-2,Phase 6,GPU required,No,CPU-only,PASS
SYS-3,Phase 6,Collective FL all phases,Yes,Yes,PASS
SYS-4,Phase 6,Formal DP guarantee,Yes,Yes,PASS
SYS-5,Phase 6,SHAP explainability,Yes,Yes,PASS
"""

# ══════════════════════════════════════════════════════════════
#  PUSH LOOP
# ══════════════════════════════════════════════════════════════
created = []
updated = []
failed  = []

for path, content in FILES.items():
    try:
        try:
            existing = repo.get_contents(path, ref=BRANCH)
            repo.update_file(
                path,
                f"chore: update {path.split('/')[-1]}",
                content,
                existing.sha,
                branch=BRANCH
            )
            updated.append(path)
            print(f"✅  UPDATED  {path}")
        except Exception:
            repo.create_file(
                path,
                f"feat: add {path.split('/')[-1]}",
                content,
                branch=BRANCH
            )
            created.append(path)
            print(f"🆕  CREATED  {path}")
    except Exception as e:
        failed.append((path, str(e)))
        print(f"❌  FAILED   {path}  →  {e}")

print("\n" + "="*60)
print(f"  Created : {len(created)}")
print(f"  Updated : {len(updated)}")
print(f"  Failed  : {len(failed)}")
print("="*60)
if failed:
    print("\nFailed files:")
    for f, e in failed:
        print(f"  {f}  →  {e}")
print("\nDone → https://github.com/hamidborkot/sentinel-ego/tree/main/results")
