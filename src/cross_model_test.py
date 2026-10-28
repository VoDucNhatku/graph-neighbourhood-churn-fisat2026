"""
cross_model_test.py

Recomputes Table 2 of the paper (cross-model comparisons) from the committed
per-fold scores in results/significance_folds.csv. No model is refitted.

Group (a) changes classifier and feature tier together; group (b) holds the tier
fixed and changes only the classifier. The statistics are the ones used in
src/significance_test.py: Nadeau-Bengio corrected resampled t-test over the 50
paired folds, and a 10,000-sample bootstrap CI (seed 42) given for magnitude only.

Output:
    results/cross_model_summary.csv

Run:  python src/cross_model_test.py [folds.csv] [summary.csv]
"""

import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "results", "significance_folds.csv")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "results", "cross_model_summary.csv")

N_SPLITS, SEED = 5, 42
LR, GB = "Logistic Regression", "LightGBM"
TIERS = ["RFM", "LRFM", "B-LRFM", "B-LRFM+Seg", "Graph-Enhanced"]


def nadeau_bengio(d):
    d = np.asarray(d, float)
    J = len(d)
    t = d.mean() / np.sqrt((1.0 / J + 1.0 / (N_SPLITS - 1)) * d.var(ddof=1))
    return t, 2 * stats.t.sf(abs(t), df=J - 1)


def bootstrap_ci(d, n_boot=10000, alpha=0.05):
    rng = np.random.default_rng(SEED)
    d = np.asarray(d, float)
    means = rng.choice(d, size=(n_boot, len(d)), replace=True).mean(axis=1)
    return np.percentile(means, [100 * alpha / 2, 100 * (1 - alpha / 2)])


df = pd.read_csv(FOLDS)
piv = df.pivot_table(index="FoldId", columns=["Model", "Tier"], values="AUC")

pairs = [("a", (LR, "B-LRFM"), (GB, "Graph-Enhanced")),
         ("a", (LR, "RFM"), (GB, "Graph-Enhanced"))]
pairs += [("b", (LR, t), (GB, t)) for t in TIERS]

rows = []
print(f"{len(piv)} paired folds")
for group, a, b in pairs:
    d = piv[a].values - piv[b].values
    lo, hi = bootstrap_ci(d)
    t, p = nadeau_bengio(d)
    rows.append({"Group": group, "A_Model": a[0], "A_Tier": a[1],
                 "B_Model": b[0], "B_Tier": b[1], "Delta_AUC": d.mean(),
                 "CI95_low": lo, "CI95_high": hi,
                 "t_NadeauBengio": t, "p_NadeauBengio": p})
    print(f"({group}) {a[0][:6]}/{a[1]:<15s} vs {b[0][:6]}/{b[1]:<15s} "
          f"delta={d.mean():+.4f}  CI=[{lo:+.4f}, {hi:+.4f}]  p_NB={p:.3f}")

pd.DataFrame(rows).to_csv(OUT, index=False)
print(f"\n[OUTPUT] {OUT}")
