"""
Layer 3: ordinal logistic (proportional-odds) regressions of confidence in
army / police / courts on religiosity, party preference, ideology, and
sociodemographic controls — per wave, pooled across clusters and separately
for each of the three trust clusters.

Specification per wave × institution × group:
  outcome ~ not_religious_dummy + rel_attendance + rel_importance_god
            + left_right + age + female + education_raw + income_raw
            + married_dummy [+ AKP_dummy + MHP_dummy + HDP_dummy + other_dummy
                              if wave in {WV5, WV6, WV7}]
  (wv7_flag is constant within a single-wave model and is dropped here;
   it would only be meaningful in cross-wave pooled models.)
"""
import os
import warnings
import numpy as np
import pandas as pd
from statsmodels.miscmodels.ordinal_model import OrderedModel

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")

WAVES  = ["WV2","WV3","WV4","WV5","WV6","WV7"]
YEARS  = {"WV2":1990,"WV3":1996,"WV4":2001,"WV5":2007,"WV6":2011,"WV7":2018}
PARTY_WAVES = {"WV5","WV6","WV7"}
INST  = ["conf_military","conf_police","conf_courts"]


# =========================================================================
# Data prep
# =========================================================================
df = pd.read_csv(os.path.join(RESULTS, "pooled_extended_v2.csv"))
df = df.dropna(subset=["cluster"]).copy()
df["cluster"] = df["cluster"].astype(int)
df["wv7_flag"] = (df["wave"] == "WV7").astype(int)

# not_religious_dummy: 1 if rel_person in {2,3}, else 0 (religious=1)
df["not_religious_dummy"] = df["rel_person"].map(
    lambda v: 1 if v in (2, 3) else (0 if v == 1 else np.nan))

# Party dummies (ref = CHP). IYI lumped into 'other' per user spec.
df["AKP_dummy"]   = (df["party_recode"] == "AKP").astype(int)
df["MHP_dummy"]   = (df["party_recode"] == "MHP").astype(int)
df["HDP_dummy"]   = (df["party_recode"] == "HDP").astype(int)
df["other_dummy"] = (df["party_recode"].isin(["other","IYI"])).astype(int)
# 0 across all four = CHP or pre_AKP_era; for pre-AKP rows, party_recode is
# 'pre_AKP_era' so all four are 0 (model uses CHP-equivalent baseline);
# we'll explicitly drop party dummies in WV2-4 regressions.

# Continuous / control predictor list
CONTROLS = ["age", "female", "education_raw", "income_raw", "married_dummy"]
RELIG    = ["not_religious_dummy", "rel_attendance", "rel_importance_god"]
IDEOL    = ["left_right"]
PARTY    = ["AKP_dummy", "MHP_dummy", "HDP_dummy", "other_dummy"]


def build_predictors(wave):
    cols = RELIG + IDEOL + CONTROLS[:]
    if wave in PARTY_WAVES:
        cols += PARTY
    return cols


# =========================================================================
# Fit one OrderedModel and pull out coefs+CIs
# =========================================================================
def fit_one(sub, outcome, predictors, model_type, institution, wave):
    rows = []
    # drop rows missing outcome / any predictor
    needed = [outcome] + predictors
    sub2 = sub[needed].dropna().copy()
    # also require the outcome to have variance and >=2 categories
    sub2[outcome] = sub2[outcome].astype(int)
    if sub2.shape[0] < 30 or sub2[outcome].nunique() < 2:
        return [{"model_type": model_type, "institution": institution,
                 "wave": wave, "year": YEARS[wave],
                 "predictor": "(skipped)",
                 "coef": np.nan, "se": np.nan, "p_value": np.nan,
                 "ci_lower": np.nan, "ci_upper": np.nan,
                 "pseudo_r2": np.nan, "n_obs": len(sub2),
                 "small_n_flag": 1, "note": "insufficient data"}]
    # drop zero-variance predictors
    keep = [p for p in predictors if sub2[p].nunique() > 1]
    dropped = [p for p in predictors if p not in keep]
    if not keep:
        return [{"model_type": model_type, "institution": institution,
                 "wave": wave, "year": YEARS[wave],
                 "predictor": "(no predictors with variance)",
                 "coef": np.nan, "se": np.nan, "p_value": np.nan,
                 "ci_lower": np.nan, "ci_upper": np.nan,
                 "pseudo_r2": np.nan, "n_obs": len(sub2),
                 "small_n_flag": 1, "note": "no variance"}]
    y = sub2[outcome]
    X = sub2[keep]
    try:
        mod = OrderedModel(y, X, distr="logit")
        res = mod.fit(method="bfgs", maxiter=200, disp=False)
        params = res.params
        bse    = res.bse
        pvals  = res.pvalues
        ci     = res.conf_int()
        pr2    = float(res.prsquared) if hasattr(res, "prsquared") else np.nan
        # Only report betas for predictor columns (not threshold/cutpoint params)
        for p in keep:
            if p in params.index:
                rows.append({
                    "model_type": model_type, "institution": institution,
                    "wave": wave, "year": YEARS[wave],
                    "predictor": p,
                    "coef": float(params[p]),
                    "se":   float(bse[p]),
                    "p_value": float(pvals[p]),
                    "ci_lower": float(ci.loc[p, 0]),
                    "ci_upper": float(ci.loc[p, 1]),
                    "pseudo_r2": pr2,
                    "n_obs": int(len(sub2)),
                    "small_n_flag": 1 if len(sub2) < 100 else 0,
                    "note": ("dropped: " + ",".join(dropped)) if dropped else "",
                })
        if not rows:
            rows.append({"model_type": model_type, "institution": institution,
                         "wave": wave, "year": YEARS[wave],
                         "predictor": "(no predictor params found)",
                         "coef": np.nan, "se": np.nan, "p_value": np.nan,
                         "ci_lower": np.nan, "ci_upper": np.nan,
                         "pseudo_r2": pr2,
                         "n_obs": len(sub2), "small_n_flag": 1,
                         "note": "fit ok but no predictor params"})
    except Exception as e:
        rows.append({"model_type": model_type, "institution": institution,
                     "wave": wave, "year": YEARS[wave],
                     "predictor": "(fit_failed)",
                     "coef": np.nan, "se": np.nan, "p_value": np.nan,
                     "ci_lower": np.nan, "ci_upper": np.nan,
                     "pseudo_r2": np.nan, "n_obs": len(sub2),
                     "small_n_flag": 1, "note": f"error: {type(e).__name__}: {e}"[:120]})
    return rows


# =========================================================================
# Run all models
# =========================================================================
all_rows = []
for inst in INST:
    for w in WAVES:
        if inst == "conf_courts" and w == "WV4":
            continue
        preds = build_predictors(w)
        sub_wave = df[df["wave"] == w]
        # Model A — pooled across clusters
        print(f"  fitting {inst} {w} POOLED  n={len(sub_wave)}")
        all_rows.extend(fit_one(sub_wave, inst, preds, "pooled",
                                inst, w))
        # Model B — per cluster
        for c in (0, 1, 2):
            sub_c = sub_wave[sub_wave["cluster"] == c]
            print(f"    fitting {inst} {w} cluster{c}  n={len(sub_c)}")
            all_rows.extend(fit_one(sub_c, inst, preds, f"cluster{c}",
                                    inst, w))

out = pd.DataFrame(all_rows)
out_path = os.path.join(RESULTS, "layer3_ordinal_coefficients.csv")
out.to_csv(out_path, index=False)
print(f"\nSaved {out_path}  ({len(out)} rows)")


# =========================================================================
# Tables A and B — not_religious_dummy coefficient matrices
# =========================================================================
def stars(p):
    if pd.isna(p): return ""
    if p < 0.001:  return "***"
    if p < 0.01:   return "**"
    if p < 0.05:   return "*"
    if p < 0.10:   return "."
    return ""


def matrix_for(model_type):
    sub = out[(out["model_type"] == model_type) &
              (out["predictor"] == "not_religious_dummy")]
    pivot_coef = sub.pivot(index="wave", columns="institution", values="coef")
    pivot_p    = sub.pivot(index="wave", columns="institution", values="p_value")
    pivot_n    = sub.pivot(index="wave", columns="institution", values="n_obs")
    insts_order = ["conf_military","conf_police","conf_courts"]
    pivot_coef = pivot_coef.reindex(columns=insts_order)
    pivot_p    = pivot_p.reindex(columns=insts_order)
    pivot_n    = pivot_n.reindex(columns=insts_order)
    pivot_coef = pivot_coef.reindex(WAVES)
    pivot_p    = pivot_p.reindex(WAVES)
    pivot_n    = pivot_n.reindex(WAVES)
    # Build pretty display
    disp = pd.DataFrame(index=WAVES, columns=insts_order, dtype=object)
    for w in WAVES:
        for i in insts_order:
            c = pivot_coef.loc[w, i]
            p = pivot_p.loc[w, i]
            n = pivot_n.loc[w, i]
            if pd.isna(c):
                disp.loc[w, i] = "    —    "
            else:
                disp.loc[w, i] = f"{c:+.3f}{stars(p):<3}(n={int(n)})"
    return disp


print("\n" + "=" * 78)
print("Table A — POOLED models: coefficient of not_religious_dummy")
print("=" * 78)
print("Higher coef = non-religious respondents report MORE confidence in this institution.")
print("Stars: . p<.10  * p<.05  ** p<.01  *** p<.001\n")
tA = matrix_for("pooled")
# print with column widths
print(f"{'wave':<5}  " + "  ".join(f"{i.replace('conf_',''):<22}" for i in tA.columns))
print("-" * 75)
for w in WAVES:
    cells = [tA.loc[w, i] for i in tA.columns]
    print(f"{w:<5}  " + "  ".join(f"{c:<22}" for c in cells))

print("\n" + "=" * 78)
print("Table B — CLUSTER 1 (Selective trusters) models: not_religious_dummy")
print("=" * 78)
tB = matrix_for("cluster1")
print(f"{'wave':<5}  " + "  ".join(f"{i.replace('conf_',''):<22}" for i in tB.columns))
print("-" * 75)
for w in WAVES:
    cells = [tB.loc[w, i] for i in tB.columns]
    print(f"{w:<5}  " + "  ".join(f"{c:<22}" for c in cells))


# =========================================================================
# Quick supplementary: cluster 0 and cluster 2 too for context
# =========================================================================
for c in (0, 2):
    print(f"\n--- Supplementary: cluster {c} not_religious_dummy ---")
    t = matrix_for(f"cluster{c}")
    print(f"{'wave':<5}  " + "  ".join(f"{i.replace('conf_',''):<22}" for i in t.columns))
    print("-" * 75)
    for w in WAVES:
        cells = [t.loc[w, i] for i in t.columns]
        print(f"{w:<5}  " + "  ".join(f"{cc:<22}" for cc in cells))

# Convergence summary
print("\n--- Per-model n + small_n flags (cluster models) ---")
small = (out.groupby(["model_type","institution","wave"])
            .agg(n=("n_obs","first"), small=("small_n_flag","first"))
            .reset_index())
flagged = small[(small["small"] == 1) &
                (small["model_type"].str.startswith("cluster"))]
if flagged.empty:
    print("  none")
else:
    print(flagged.to_string(index=False))
