"""
Layer 4b — long-window pooled ordinal logit, WV2-WV7, with WV2 baseline.

Tests when the cross-institutional religiosity differentiation emerged.
Three separate models (army / police / courts), each with wave dummies +
not_religious_dummy × wave interactions.

Notes:
- wv7_flag from the spec is perfectly collinear with wave_WV7 and is
  dropped to avoid singularity; the wave_WV7 dummy already absorbs the
  WV7 measurement regime shift.
- conf_courts is NaN for WV4; those rows naturally drop only from the
  courts model.
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
WAVES = ["WV2","WV3","WV4","WV5","WV6","WV7"]
YEARS = {"WV2":1990,"WV3":1996,"WV4":2001,"WV5":2007,"WV6":2011,"WV7":2018}


# =========================================================================
# Data prep
# =========================================================================
df = pd.read_csv(os.path.join(RESULTS, "pooled_extended_v2.csv"))
df = df.dropna(subset=["cluster"]).copy()

df["not_religious_dummy"] = df["rel_person"].map(
    lambda v: 1 if v in (2, 3) else (0 if v == 1 else np.nan))

# Wave dummies (ref=WV2)
for w in ["WV3","WV4","WV5","WV6","WV7"]:
    df[f"wave_{w}"] = (df["wave"] == w).astype(int)

# Interactions
for w in ["WV3","WV4","WV5","WV6","WV7"]:
    df[f"nr_x_{w}"] = df["not_religious_dummy"] * df[f"wave_{w}"]

PREDICTORS_BASE = [
    "not_religious_dummy", "rel_attendance", "rel_importance_god",
    "left_right",
    "age", "female", "education_raw", "income_raw", "married_dummy",
    "wave_WV3", "wave_WV4", "wave_WV5", "wave_WV6", "wave_WV7",
    "nr_x_WV3", "nr_x_WV4", "nr_x_WV5", "nr_x_WV6", "nr_x_WV7",
]


def fit_outcome(outcome):
    needed = [outcome] + PREDICTORS_BASE
    sub = df[needed].dropna().copy()
    sub[outcome] = sub[outcome].astype(int)
    keep = [p for p in PREDICTORS_BASE if sub[p].nunique() > 1]
    mod = OrderedModel(sub[outcome], sub[keep], distr="logit")
    res = mod.fit(method="bfgs", maxiter=400, disp=False)
    return res, len(sub), keep


INST = ["conf_military", "conf_police", "conf_courts"]
results = {}
for inst in INST:
    print(f"Fitting {inst} ...")
    res, n, kept = fit_outcome(inst)
    results[inst] = {"res": res, "n": n, "kept": kept}
    print(f"  n={n}, pseudo R²={res.prsquared:.4f}")


# =========================================================================
# Save long CSV of all coefs
# =========================================================================
rows = []
for inst in INST:
    r = results[inst]["res"]
    n = results[inst]["n"]
    for p in r.params.index:
        if p in PREDICTORS_BASE:
            rows.append({
                "institution": inst, "predictor": p,
                "coef": float(r.params[p]),
                "se":   float(r.bse[p]),
                "p_value": float(r.pvalues[p]),
                "ci_lower": float(r.conf_int().loc[p, 0]),
                "ci_upper": float(r.conf_int().loc[p, 1]),
                "n_obs": n,
                "pseudo_r2": float(r.prsquared),
            })
out = pd.DataFrame(rows)
out.to_csv(os.path.join(RESULTS,
    "layer4b_longwindow_interactions.csv"), index=False)
print(f"\nSaved layer4b_longwindow_interactions.csv  ({len(out)} rows)")


# =========================================================================
# Total wave effect = main + interaction (with delta-method SE)
# =========================================================================
def stars(p):
    if pd.isna(p):  return ""
    if p < 0.001:   return "***"
    if p < 0.01:    return "** "
    if p < 0.05:    return "*  "
    if p < 0.10:    return ".  "
    return "   "


def wave_total(res, wave):
    """For not_religious_dummy total effect at given wave (WV2 = baseline,
    so total = main + nr_x_{wave}). Returns (coef, se, p).
    Uses the model's covariance matrix for the linear combination's SE.
    """
    main = "not_religious_dummy"
    inter = f"nr_x_{wave}" if wave != "WV2" else None

    if inter is None or inter not in res.params.index:
        if main not in res.params.index:
            return np.nan, np.nan, np.nan
        c = float(res.params[main])
        se = float(res.bse[main])
        # z = c/se; p two-sided
        from scipy import stats as _s
        p = 2 * (1 - _s.norm.cdf(abs(c / se)))
        return c, se, p

    # Linear combination main + inter
    L = np.zeros(len(res.params))
    L[res.params.index.get_loc(main)]  = 1.0
    L[res.params.index.get_loc(inter)] = 1.0
    c = float(L @ res.params)
    cov = res.cov_params()
    var = float(L @ cov @ L)
    se  = float(np.sqrt(var)) if var > 0 else np.nan
    from scipy import stats as _s
    p = 2 * (1 - _s.norm.cdf(abs(c / se))) if se and not np.isnan(se) else np.nan
    return c, se, p


print("\n" + "=" * 96)
print("Long-window: not_religious_dummy TOTAL effect (main + wave interaction)")
print(" baseline WV2; later waves show (main + nr × wave) with delta-method SE")
print("=" * 96)
hdr = "{:<6}{:>22}{:>22}{:>22}{:>14}"
print(hdr.format("wave","army (coef ± stars)","police","courts","army−police"))
print("-" * 86)

table_rows = []
for w in WAVES:
    cells = {}
    for inst in INST:
        c, se, p = wave_total(results[inst]["res"], w)
        cells[inst] = (c, se, p)
    army_c = cells["conf_military"][0]
    pol_c  = cells["conf_police"][0]
    crt_c  = cells["conf_courts"][0]
    spread = (army_c - pol_c
              if not np.isnan(army_c) and not np.isnan(pol_c) else np.nan)
    sign_change = ""
    print(hdr.format(
        w,
        f"{army_c:+.3f}{stars(cells['conf_military'][2])}",
        f"{pol_c:+.3f}{stars(cells['conf_police'][2])}",
        f"{crt_c:+.3f}{stars(cells['conf_courts'][2])}",
        f"{spread:+.3f}",
    ))
    table_rows.append({
        "wave": w, "year": YEARS[w],
        "army_total":   round(army_c, 4),  "army_p":   round(cells["conf_military"][2], 5),
        "police_total": round(pol_c, 4),   "police_p": round(cells["conf_police"][2], 5),
        "courts_total": round(crt_c, 4),   "courts_p": round(cells["conf_courts"][2], 5),
        "army_police_spread": round(spread, 4),
    })

tot = pd.DataFrame(table_rows)
tot.to_csv(os.path.join(RESULTS,
    "layer4b_total_effects_by_wave.csv"), index=False)


# =========================================================================
# Specific hypothesis tests
# =========================================================================
print("\n" + "=" * 96)
print("Specific tests")
print("=" * 96)

# A. Is the WV5 interaction significant in the army model?
army = results["conf_military"]["res"]
for inst_name, res in [("army", results["conf_military"]["res"]),
                       ("police", results["conf_police"]["res"]),
                       ("courts", results["conf_courts"]["res"])]:
    if "nr_x_WV5" in res.params.index:
        c = float(res.params["nr_x_WV5"])
        se = float(res.bse["nr_x_WV5"])
        p = float(res.pvalues["nr_x_WV5"])
        print(f"  {inst_name:<7}  nr_x_WV5 = {c:+.3f}  SE={se:.3f}  p={p:.4f}  {stars(p)}")
    else:
        print(f"  {inst_name:<7}  nr_x_WV5: not in model")

# B. First wave where army-police spread changes sign
prev_sign = None
print("\nFirst wave where army-police spread crosses zero / changes sign:")
for r in table_rows:
    sgn = np.sign(r["army_police_spread"]) if not np.isnan(r["army_police_spread"]) else 0
    if prev_sign is not None and sgn != prev_sign and sgn != 0:
        print(f"  → at {r['wave']} (spread = {r['army_police_spread']:+.3f}, "
              f"prev was {prev_sign:+.0f})")
    prev_sign = sgn if sgn != 0 else prev_sign

# C. All wave interaction terms with significance — both models side by side
print("\nWave interaction terms (nr × wave_X), army vs police vs courts:")
print(f"{'interaction':<12}{'army':>20}{'police':>20}{'courts':>20}")
print("-" * 72)
for w in ["WV3","WV4","WV5","WV6","WV7"]:
    key = f"nr_x_{w}"
    line = [f"  {key:<10}"]
    for inst in INST:
        res = results[inst]["res"]
        if key in res.params.index:
            c = float(res.params[key])
            p = float(res.pvalues[key])
            line.append(f"{c:+.3f}{stars(p):>5}")
        else:
            line.append("   —    ")
    print("{:<12}{:>20}{:>20}{:>20}".format(*line))

print("\n n_obs per model: " + ", ".join(
    f"{inst}={results[inst]['n']}" for inst in INST))
print("Files written:")
print("  results/layer4b_longwindow_interactions.csv  (all coefs)")
print("  results/layer4b_total_effects_by_wave.csv    (per-wave totals)")
