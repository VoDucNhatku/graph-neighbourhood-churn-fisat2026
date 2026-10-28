# When Graph-Derived Neighbourhood Features Do Not Help: A Leakage-Controlled Evaluation of Behavioural-LRFM Churn Prediction in Non-Contractual Retail

**Duc Nhat Vo, Gia Bao Duong, Nguyen Minh Hai Tran** (Võ Đức Nhật, Dương Gia Bảo, Trần Nguyễn Minh Hải)  
FPT University, Ho Chi Minh City, Vietnam

Short paper at **EAI FISAT 2026**, the 1st EAI FPT International Conference on Intelligent
Systems and Advanced Technologies (Ho Chi Minh City, 25–27 November 2026), to appear in
EAI/Springer Innovations in Communication and Computing. Paper #366956.

[Paper (PDF)](paper/main.pdf) · [Citation](#citation) · [Reproduce](#running-the-pipeline) · [License](#license)

| Version | Tag | What it is |
|---|---|---|
| Camera-ready | [`v1.1`](../../tree/v1.1) | The version cited in the paper's reproducibility statement |
| Submitted for review | [`v1.0-submission`](../../tree/v1.0-submission) | Unchanged reviewed version |

Both versions use the same code and the same result files; the camera-ready changes are in
the manuscript only, plus `src/cross_model_test.py`, which recomputes Table 2 from the
committed per-fold scores.

### Abstract

Customer similarity graphs are an appealing addition to RFM-style churn models. If churn
spreads through behavioural peer groups, the churn rate among a customer's nearest
neighbours should help predict that customer's own churn. We test that idea on the Online
Retail II dataset under two controls. First, the neighbourhood and community churn rates
are recomputed inside every training fold, so no test label reaches the feature matrix.
Second, every comparison runs over ten repetitions of five-fold cross-validation and is
judged by the corrected resampled t-test rather than by a single split. Under these
controls the idea does not hold. With the classifier fixed, no feature tier beats a plain
three-variable RFM baseline, on either ROC-AUC or PR-AUC, for either classifier, at any
graph degree from 5 to 20. The graph-enhanced tier gains +0.0033 ROC-AUC on one fold
partition and reverses sign across ten. Every significant difference involves a change of
classifier, so none speaks to the graph features. Attribution and contribution also come
apart: the neighbourhood churn rate ranks third by SHAP, yet removing the graph features
costs nothing. Because the k-NN graph is built on the features the classifier already
uses, its neighbourhood churn rate largely restates existing information by construction;
a graph built from co-purchase or referral links may behave differently. We argue that
single-split evaluation cannot separate an effect this small from fold noise.

### Citation

```bibtex
@inproceedings{vo2026graphneighbourhood,
  author    = {Vo, Duc Nhat and Duong, Gia Bao and Tran, Nguyen Minh Hai},
  title     = {When Graph-Derived Neighbourhood Features Do Not Help: A Leakage-Controlled
               Evaluation of Behavioural-{LRFM} Churn Prediction in Non-Contractual Retail},
  booktitle = {Proceedings of the 1st EAI FPT International Conference on Intelligent
               Systems and Advanced Technologies (FISAT 2026)},
  series    = {EAI/Springer Innovations in Communication and Computing},
  publisher = {Springer},
  year      = {2026},
  note      = {To appear}
}
```

GitHub's "Cite this repository" button reads the same entry from [`CITATION.cff`](CITATION.cff).
The DOI will be added once the proceedings are published.

---

## Vietnamese study documents

The [Vietnamese document index](docs/vietnamese/README.md) provides four PDFs with
editable sources: a detailed knowledge handbook, the research process, a complete
translation of the accepted paper, and an updated audit/reproduction report.
The first two explain the topic, problem, objectives, methods and current progress
for readers familiar with basic Python and machine learning.

See the [Colab notebook](notebooks/366956-reproduce.ipynb),
[running instructions](notebooks/HUONG_DAN_COLAB.md), and
[actual 2026-10-12 reproduction outputs](results/reproduction-20261012).
The translation retains the accepted paper's wording; the other documents explain
method-description discrepancies and limits of the evidence. The accepted paper
and experiment source files are preserved.

---

## Overview

This repository implements a complete machine learning pipeline for customer churn prediction in non-contractual e-commerce settings. The framework extends classical RFM analysis into a **Behavioral-LRFM** feature space, constructs a **customer similarity graph**, and applies **Louvain/Leiden community detection** to discover cohesive behavioral communities. Graph-derived node features — including **NeighborChurnRate** and **CommunityChurnRate** — are evaluated with LightGBM and logistic regression (XGBoost appears only in the auxiliary variants). Finally, **SHAP analysis at the community level** generates actionable, segment-specific retention strategies.

**Honest finding.** The pipeline is fully implemented and leak-free, but it does not beat
its own baseline. Under repeated cross-validation the graph-derived features add nothing
measurable to churn prediction. The only significant differences are between classifiers
(logistic regression beats LightGBM), not between feature sets. This repository is
therefore reported as a **negative result with a working, reproducible pipeline**, not as
a performance improvement. See [Key Results](#key-results).

---

## Key Results

> **Headline finding.** Under repeated cross-validation with a variance-corrected test,
> graph-derived features do **not** improve churn prediction. No feature tier differs
> significantly from plain RFM. Some cross-model comparisons favor logistic regression:
> **logistic regression on the three raw RFM variables outperforms the LightGBM
> graph-enhanced pipeline** (ΔAUC = +0.0099, p = 0.010). This comparison changes both
> classifier and feature tier; it does not isolate a feature-engineering effect.

### Churn prediction — repeated CV (10 x 5-fold, paired, LightGBM)

Baseline = RFM. All tiers share the same fold partition within each repeat, so the
differences are properly paired. `p` is the corrected resampled t-test
(Nadeau & Bengio, 2003); the naive paired t-test is **not** reported, because repeated
folds reuse training data and inflate significance.

| Feature Set | ROC-AUC (mean) | Δ vs RFM | p (Nadeau-Bengio) | Significant |
|---|---:|---:|---:|---|
| RFM (baseline) | 0.8066 | — | — | — |
| LRFM | 0.8074 | +0.0009 | 0.755 | no |
| Behavioral-LRFM | 0.8054 | −0.0012 | 0.742 | no |
| B-LRFM + Segment | 0.8044 | −0.0022 | 0.561 | no |
| Graph-Enhanced (leak-free) | 0.8044 | −0.0021 | 0.590 | no |

The same holds for PR-AUC and for logistic regression as the classifier. Full table with
bootstrap CIs and Wilcoxon: `results/significance_summary.csv`; per-fold scores:
`results/significance_folds.csv`.

*Run-to-run stability:* re-executing `src/significance_test.py` on the same machine and
seeds moves these means by about 1e-4 ROC-AUC and the p-values in the third decimal
(e.g. Graph-Enhanced Δ ranged −0.0020 to −0.0021, p 0.59 to 0.61 across two runs). That
jitter is an order of magnitude smaller than any difference discussed here and does not
change a single conclusion, but it is worth stating rather than presenting these digits
as exact. Numbers above are from the 2026-08-07 run
(`results_rerun/full-2026-08-07/significance_test.log`).

### Cross-model comparisons (classifier effects, not feature effects)

| Comparison (same 50 paired folds) | Δ ROC-AUC | 95% CI | p (NB) |
|---|---:|---:|---:|
| *(a) classifier and tier both change* | | | |
| LogReg / B-LRFM vs LightGBM / Graph-Enhanced | +0.0113 | [+0.0096, +0.0130] | **0.001** |
| LogReg / RFM vs LightGBM / Graph-Enhanced | +0.0099 | [+0.0080, +0.0119] | **0.010** |
| *(b) same tier, classifier only* | | | |
| LogReg vs LightGBM, both on RFM | +0.0078 | [+0.0056, +0.0100] | 0.068 |
| LogReg vs LightGBM, both on Graph-Enhanced | +0.0108 | [+0.0091, +0.0126] | **0.002** |

Rows (a) change the classifier and the feature tier at once, so they say nothing about
the graph features (38 features = 9 B-LRFM + 4 static graph + 23 one-hot
segment/community + NeighborChurnRate + CommunityChurnRate). Rows (b) isolate the
classifier: logistic regression leads at every tier (+0.0062 to +0.0108), significantly
at the three tiers with nine or more features. Evidence about features comes from the
same-classifier table above. All rows, including the LRFM, B-LRFM and B-LRFM+Seg ones
not shown here, are in `results/cross_model_summary.csv` (`src/cross_model_test.py`).

### Single-split reference (seed 42, 5-fold, LightGBM)

Kept only for traceability against `results/churn_results_v2.csv`. This is **one** fold
partition and is not evidence: the RFM -> Graph-Enhanced gap of +0.0033 shown here has a
bootstrap 95% CI of [−0.0025, +0.0099] — it contains zero — and its sign reverses across
the 10 repeats above.

| Feature Set | ROC-AUC | PR-AUC | F1 | Recall |
|---|---|---|---|---|
| RFM (baseline) | 0.8065 | 0.8685 | 0.7927 | 0.7610 |
| LRFM | 0.8071 | 0.8673 | 0.8011 | 0.7775 |
| Behavioral-LRFM | 0.8067 | 0.8679 | 0.8036 | 0.7857 |
| B-LRFM + Segment | 0.8073 | 0.8687 | 0.8044 | 0.7881 |
| Graph-Enhanced (leak-free) | 0.8098 | 0.8689 | 0.8108 | 0.8009 |

### Graph Structure
- **5,038 customers** (nodes) · **33,426 edges** (k=10 NN)
- **Louvain:** 20 communities · Modularity = **0.8385**
- **Leiden:** 20 communities · Modularity = **0.8323**

### Top SHAP Features (Global)
| Rank | Feature | Mean \|SHAP\| | Group |
|---|---|---|---|
| 1 | Recency (R) | 1.087 | RFM |
| 2 | Monetary (M) | 0.560 | RFM |
| 3 | **NeighborChurnRate** | 0.250 | Graph |
| 4 | InterpurchaseTime | 0.224 | Behavioral |
| 5 | **CommunityChurnRate** | 0.215 | Graph |

Note the dissociation: `NeighborChurnRate` and `CommunityChurnRate` rank 3rd and 5th by
mean |SHAP|, yet removing them costs nothing in ROC-AUC (table above). SHAP attributes
how a fitted model *uses* a feature; it does not measure whether that feature adds
predictive information over the rest. Reading SHAP rank as evidence of contribution is a
mistake this project made and corrected.

---

## Repository Structure

```
├── src/
│   ├── run_pipeline_v2.py        # main pipeline: features, graph, communities, SHAP
│   ├── compare_methods_v2.py     # clustering comparison against Vianna Filho (2026)
│   ├── improvements_pipeline.py  # auxiliary variants (ensembles, PCA, Leiden)
│   ├── significance_test.py      # repeated CV + Nadeau-Bengio corrected test
│   ├── cross_model_test.py       # Table 2 from the committed per-fold scores
│   ├── make_paper_figures.py     # builds the paper figure from the result files
│   └── audit_paper.py            # checks every number in the paper against results/
├── results/                      # every file here is produced by a script above
├── results_rerun/                # raw run logs, kept as provenance
├── paper/
│   ├── main.tex, refs.bib        # LNCS camera-ready manuscript, 17 verified references
│   ├── main.pdf                  # compiled, 12 pages
│   └── figures/                  # generated, not hand-drawn
├── data/.gitkeep                 # dataset not tracked; see Dataset below
├── requirements.txt              # pinned to the environment that produced results/
└── README.md
```

### Which script produces which result

| Script | Outputs in `results/` |
|---|---|
| `run_pipeline_v2.py` | `churn_results_v2.csv`, `segment_profiles_v2.csv`, `shap_global_v2.csv`, `shap_global_v2.png`, `shap_per_community_v2.csv` |
| `compare_methods_v2.py` | `comparison_v2.csv`, `comparison_v2.png` |
| `improvements_pipeline.py` | `improvements_results.csv`, `improvements_summary.png` |
| `significance_test.py` | `significance_folds.csv`, `significance_summary.csv`; with `LRFM_KNN_K` set, the `*_k5/10/15/20` sweep files |
| `cross_model_test.py` | `cross_model_summary.csv` (reads `significance_folds.csv`; no model is refitted) |

No orphan outputs are kept: if a file is in `results/`, one of these scripts
regenerates it. Run all four in the order above to rebuild the directory from
the raw dataset; the whole chain takes under ten minutes on a laptop with no GPU.

---

## Dataset

**Online Retail II** — UCI Machine Learning Repository  
Download: https://archive.ics.uci.edu/dataset/502/online+retail+ii

Place the downloaded `.xlsx` file as `online_retail_II.xlsx` in the project root before running the pipeline.

```
1,067,371 transaction rows in two worksheets (525,461 + 541,910) | UK-based online retailer | Dec 2009 – Dec 2011
```

---

## Setup & Installation

```bash
git clone https://github.com/VoDucNhatku/graph-neighbourhood-churn-fisat2026.git
cd graph-neighbourhood-churn-fisat2026

pip install -r requirements.txt

# Optional: Leiden community detection
pip install leidenalg igraph
```

---

## Running the Pipeline

```bash
# Step 1: Download dataset and place in project root
# Step 2: Run main pipeline
python src/run_pipeline_v2.py

# Step 3 (optional): Run clustering comparison with VF2026
python src/compare_methods_v2.py
```

Output files will be saved to `results/`.

---

## Methodology

### 1. Data Split (No Leakage)
```
Observation window : 2009-12-01 → 2011-06-30 00:00  (feature computation)
Prediction window  : 2011-06-30 00:00 → 2011-09-30 00:00, 92 days  (churn label)
Analysis date      : 2011-07-01  (reference date for L and R)
```

### 2. Behavioral-LRFM Features
| Feature | Formula | Description |
|---|---|---|
| L | AnalysisDate − FirstPurchaseDate | Customer tenure |
| R | AnalysisDate − LastPurchaseDate | Days since last purchase |
| F | count(unique InvoiceNo) | Purchase frequency |
| M | Σ(Quantity × Price) | Total monetary value |
| AOV | M / F | Average order value |
| BasketSize | mean(unique SKUs per invoice) | Basket richness |
| ProductDiversity | count(unique StockCode) | Product variety |
| CancellationRate | cancels / (cancels + normals) ∈ [0,1] | Return behaviour |
| InterpurchaseTime | mean(days between invoices) | Purchase regularity |

### 3. Graph Construction
- Undirected k-NN graph (k=10), metric = Euclidean distance on standardized B-LRFM
- Edge weight: `w(i,j) = 1 / (1 + dist(i,j))` — higher = more similar

### 4. Community Detection
- **Louvain** (Blondel et al., 2008)
- **Leiden** (Traag et al., 2019)

### 5. Graph Node Features
| Feature | Description |
|---|---|
| Degree | Number of neighbors |
| WeightedDegree | Sum of edge weights |
| PageRank | Structural centrality |
| ClusteringCoeff | Local neighborhood density |
| **NeighborChurnRate** | Mean churn rate of k-NN neighbors (computed on training fold only — no leakage) |
| **CommunityChurnRate** | Mean churn rate within Louvain community (training fold only) |

### 6. Churn Prediction
- **Models:** Logistic Regression (baseline), Decision Tree, Random Forest, XGBoost, LightGBM
- **CV:** Stratified 5-fold, `StandardScaler` inside `sklearn.Pipeline`
- **Key fix:** `NeighborChurnRate` and `CommunityChurnRate` are recomputed **within each fold** on training labels only, preventing target leakage

### 7. Explainability
- **Global SHAP:** Overall feature importance ranking
- **Per-community SHAP:** Top-3 drivers of churn per Louvain community
- **ERV = P(churn) × Monetary:** Prioritization score for retention campaigns

---

## Leakage Fixes Applied

| Fix | Issue | Solution |
|---|---|---|
| FIX-A | CancellationRate included future cancellations | Filter `InvoiceDate <= OBS_END` |
| FIX-B | NCR/CCR used full churn labels in CV | Recompute per fold on training data only |
| FIX-C | StandardScaler fit on full dataset | Wrap scaler in `sklearn.Pipeline` |
| FIX-D | Cluster IDs treated as ordinal numbers | One-hot encode KMeans/Louvain labels |
| FIX-E | Leiden missing from main pipeline | Added alongside Louvain |
| FIX-F | SHAP only global | Added per-community SHAP analysis |

---

## Relation to Vianna Filho et al. (2026)

VF2026 is the starting point of this work, not a competitor. It segments customers on
discrete 1-5 RFM scores; this work predicts churn on a 9-dimensional continuous
Behavioral-LRFM space. **Silhouette scores are not comparable across different feature
spaces** — a low-dimensional discrete space yields tighter clusters as a property of the
space, not as a property of the algorithm — so no head-to-head clustering-quality claim
is made here.

| Dimension | VF2026 | This work |
|---|---|---|
| Task | Segmentation (unsupervised) | Churn prediction (supervised) + segmentation |
| Features | RFM, discrete 1-5 scores, 3-D | Behavioral-LRFM, continuous, 9-D |
| Graph method | Max-k-cut on the reduced graph (Gurobi) | k-NN graph + Louvain / Leiden |
| Silhouette (own space, k=4) | 0.398 (as published) | 0.219 (K-means, 9-D B-LRFM) |
| Churn prediction | out of scope | ROC-AUC 0.810 (LightGBM, single split) |
| Per-segment explanation | out of scope | SHAP over 20 communities |
| Retention strategy | cluster profiling | ERV-based prioritization |

The contribution of this work is **scope extension** — carrying an RFM-style graph
representation into a supervised, explainable churn setting — not a better clustering of
the same data. On its own scoring space VF2026 reaches a higher silhouette than anything
produced here, and that is reported rather than reframed.

---

## References

Key references (full list in Research Proposal):

1. Blondel et al. (2008). *Fast unfolding of communities in large networks.* J. Stat. Mech.
2. Chen & Guestrin (2016). *XGBoost.* KDD 2016.
3. Ke et al. (2017). *LightGBM.* NeurIPS 2017.
4. Lundberg & Lee (2017). *A unified approach to interpreting model predictions.* NeurIPS 2017.
5. Wei et al. (2022). *LRFMV.* PLOS One.
6. Vianna Filho et al. (2026). *RFM model customer segmentation from a graph theory perspective.* Quality & Quantity.

---

## License

Code and result files are released under the [MIT License](LICENSE).
The manuscript in `paper/` is the authors' own version; copyright in the published
version is transferred to EAI.  
Dataset: [Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii) — UCI ML Repository, CC BY 4.0
(not redistributed here).
