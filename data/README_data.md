# Datasets Used in The Sentinel Ego

All experiments in this repository use **publicly available, real-world datasets**. No synthetic or fabricated data is used in any phase. Follow the instructions below to download and place each dataset before running the notebooks.

---

## Phase 1 — Enron Email Corpus (PBI Module)

| Property | Details |
|---|---|
| **Name** | Enron Email Dataset (CMU Release, May 2015) |
| **Size** | ~422 MB compressed, ~2.6 GB extracted |
| **Records** | ~517,401 parsed email records, 150 users |
| **Source** | Carnegie Mellon University |
| **License** | Public domain (released by FERC) |

**Download:**
```bash
wget https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz -P data/raw/
tar -xzf data/raw/enron_mail_20150507.tar.gz -C data/raw/
```

After extraction, your directory should contain:
```
data/raw/enron_mail_20150507/maildir/<username>/
```

---

## Phase 2 — Network Intrusion Detection Datasets (AIF Module)

### 1. NSL-KDD (2009)
| Property | Details |
|---|---|
| **Name** | NSL-KDD |
| **Records** | 125,973 train / 22,544 test |
| **Features** | 41 raw network features |
| **Source** | University of New Brunswick ISCX |

**Download:**
```bash
# Direct CSV download from UNB
wget https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain+.txt -P data/raw/nsl_kdd/
wget https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest+.txt -P data/raw/nsl_kdd/
```

### 2. KDDCup99-SF Subset (1999)
| Property | Details |
|---|---|
| **Name** | KDDCup99 (SF subset) |
| **Records** | 73,237 rows |
| **Source** | UCI Machine Learning Repository |

```python
# Loaded automatically via sklearn in Phase 2 notebook:
from sklearn.datasets import fetch_kddcup99
data = fetch_kddcup99(subset='SF', as_frame=True)
```

### 3. NetIntrusion (Kaggle)
| Property | Details |
|---|---|
| **Name** | Network Intrusion Detection |
| **Records** | 25,000 rows |
| **Source** | Kaggle |

```bash
# Requires Kaggle API
kaggle datasets download -d sampadab17/network-intrusion-detection -p data/raw/netintrusion/
unzip data/raw/netintrusion/network-intrusion-detection.zip -d data/raw/netintrusion/
```

---

## Recommended Additional Datasets (for extended TIFS revision)

The following modern datasets are recommended for the Phase 6 extended evaluation to address TIFS reviewer expectations for contemporary benchmark coverage:

| Dataset | Year | Download |
|---|---|---|
| **CICIDS2017** | 2017 | https://www.unb.ca/cic/datasets/ids-2017.html |
| **UNSW-NB15** | 2015 | https://research.unsw.edu.au/projects/unsw-nb15-dataset |
| **CIC-IoT2023** | 2023 | https://www.unb.ca/cic/datasets/iotdataset-2023.html |

---

## Directory Structure After Download

```
data/
├── raw/
│   ├── enron_mail_20150507/
│   │   └── maildir/
│   ├── nsl_kdd/
│   │   ├── KDDTrain+.txt
│   │   └── KDDTest+.txt
│   └── netintrusion/
│       └── Train_data.csv
└── README_data.md
```

> **Note:** The `data/raw/` directory is listed in `.gitignore` to avoid uploading large raw files. Only processed result CSVs in `results/` are tracked by git.
