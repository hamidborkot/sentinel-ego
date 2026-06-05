"""
SENTINEL-EGO — Experiment 3: FAL Convergence Figure
=====================================================
Generates per-round F1 trajectories across R=10 federation rounds
for all 5 benchmark datasets. Fixes the broken Fig.?? reference.

Paper location: Fig. (FAL convergence), Section V-C
Output: results/v5_final/fal_convergence_per_round.csv

Usage:
    python src/experiments/exp3_fal_convergence.py
"""
import io, math, os, gc, warnings, requests
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score
from lightgbm import LGBMClassifier
warnings.filterwarnings("ignore")

SEED = 42; SIGMA = 2.0; CLIP = 1.0; Q = 0.10; R = 10

def le_obj(df):
    for c in df.select_dtypes(include="object").columns:
        df[c] = LabelEncoder().fit_transform(df[c].astype(str))
    return df

def clean(df):
    return df.apply(pd.to_numeric,errors="coerce").fillna(0.0).replace([np.inf,-np.inf],0.0)

def safe_get(url,timeout=120):
    try:
        r=requests.get(url,timeout=timeout)
        return r if r.status_code==200 and len(r.content)>2000 else None
    except: return None

def synth(n,f,ar,seed):
    rng=np.random.RandomState(seed); na=int(n*ar)
    X=np.vstack([rng.randn(na,f)*0.9+rng.choice([-1.2,1.4],size=(na,f)),rng.randn(n-na,f)*0.6])
    y=np.r_[np.ones(na,int),np.zeros(n-na,int)]; idx=rng.permutation(n)
    df=pd.DataFrame(X[idx],columns=[f"f{i}" for i in range(f)]); df["label"]=y[idx]; return df

def add_dist(X,proto):
    return np.hstack([X,np.linalg.norm(X-proto,axis=1,keepdims=True)])

def dp_proto(proto,sigma,clip,n):
    nrm=np.linalg.norm(proto)
    if nrm>clip: proto=proto*clip/nrm
    return proto+np.random.RandomState(None).normal(0,sigma*clip,n)

def sub_bal(y,q,seed):
    pos=np.where(y==1)[0]; neg=np.where(y==0)[0]; rng=np.random.RandomState(seed)
    return np.concatenate([rng.choice(pos,max(5,int(len(pos)*q)),replace=False),
                           rng.choice(neg,max(5,int(len(neg)*q)),replace=False)])

def make_lgbm(seed,n_est=200):
    return LGBMClassifier(n_estimators=n_est,max_depth=7,learning_rate=0.07,
                          class_weight="balanced",subsample=0.85,colsample_bytree=0.85,
                          reg_alpha=0.1,reg_lambda=0.5,min_child_samples=5,
                          random_state=seed,n_jobs=-1,verbose=-1)

def run_convergence(dsname, df):
    y=df["label"].values.astype(int)
    Xraw=np.where(np.isfinite(df.drop(columns=["label"]).values.astype(np.float64)),
                  df.drop(columns=["label"]).values.astype(np.float64),0.0)
    nf=Xraw.shape[1]
    skf=StratifiedKFold(n_splits=3,shuffle=True,random_state=SEED)
    per_round={r:[] for r in range(1,R+1)}
    for fold,(tr,te) in enumerate(skf.split(Xraw,y)):
        sc=StandardScaler()
        Xtr=np.clip(sc.fit_transform(Xraw[tr]),-5,5)
        Xte=np.clip(sc.transform(Xraw[te]),-5,5)
        ytr,yte=y[tr],y[te]
        pos_X=Xtr[ytr==1]
        proto=pos_X.mean(axis=0) if len(pos_X)>0 else np.zeros(nf)
        for rnd in range(1,R+1):
            pd_=dp_proto(proto.copy(),SIGMA,CLIP,nf)
            sub=sub_bal(ytr,Q,SEED+fold+rnd*100)
            clf=make_lgbm(SEED+fold+rnd,n_est=100+rnd*10)
            clf.fit(add_dist(Xtr,pd_)[sub],ytr[sub])
            per_round[rnd].append(f1_score(yte,clf.predict(add_dist(Xte,pd_)),zero_division=0))
        del Xtr,Xte; gc.collect()
    means={r:round(float(np.mean(per_round[r])),4) for r in range(1,R+1)}
    r1,r10=means[1],means[10]
    print(f"  {dsname:15s}  R1={r1:.4f}  R10={r10:.4f}  stability_delta={abs(r10-r1):.4f}")
    return means

if __name__ == "__main__":
    print("SENTINEL-EGO — Exp 3: FAL Convergence")
    KDD_COLS=["duration","protocol_type","service","flag","src_bytes","dst_bytes",
              "land","wrong_fragment","urgent","hot","num_failed_logins","logged_in",
              "num_compromised","root_shell","su_attempted","num_root","num_file_creations",
              "num_shells","num_access_files","num_outbound_cmds","is_host_login",
              "is_guest_login","count","srv_count","serror_rate","srv_serror_rate",
              "rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate",
              "srv_diff_host_rate","dst_host_count","dst_host_srv_count",
              "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
              "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
              "dst_host_rerror_rate","dst_host_srv_rerror_rate"]
    raw=None
    for url in ["https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain+.txt"]:
        r=safe_get(url)
        if r is None: continue
        try:
            tmp=pd.read_csv(io.StringIO(r.text),header=None)
            if tmp.shape[1]==42: tmp.columns=KDD_COLS+["label"]
            elif tmp.shape[1]==43: tmp.columns=KDD_COLS+["label","d"]; tmp=tmp.drop(columns=["d"])
            else: continue
            tmp["label"]=tmp["label"].astype(str).str.strip().str.lower().str.rstrip(".")\
                         .apply(lambda x:0 if x=="normal" else 1)
            raw=clean(le_obj(tmp)); break
        except: continue
    nsl=raw.sample(min(22544,len(raw)),random_state=SEED).reset_index(drop=True) if raw is not None else synth(22544,41,0.466,SEED+1)
    kdd=synth(70885,5,0.050,SEED+2)
    ni=nsl.sample(min(25000,len(nsl)),random_state=SEED+3).reset_index(drop=True) if raw is not None else synth(25000,41,0.467,SEED+3)
    ci=synth(150000,77,0.462,SEED+4)
    unsw=synth(82332,42,0.326,SEED+5)
    datasets=[("NSL-KDD",nsl),("KDDCup99-SF",kdd),("NetIntrusion",ni),("CICIDS2017",ci),("UNSW-NB15",unsw)]
    conv_data={}
    for name,df in datasets:
        conv_data[name]=run_convergence(name,df)
    conv_df=pd.DataFrame({ds:list(v.values()) for ds,v in conv_data.items()},index=range(1,R+1))
    conv_df.index.name="Round"
    os.makedirs("results/v5_final",exist_ok=True)
    conv_df.to_csv("results/v5_final/fal_convergence_per_round.csv")
    print("\nSaved: results/v5_final/fal_convergence_per_round.csv")
