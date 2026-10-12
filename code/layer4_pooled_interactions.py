"""
Layer 4 — formal H3 test.

Pooled (across clusters) ordinal logit per institution on WV5/WV6/WV7 with
wave × predictor interactions for not_religious_dummy, AKP_dummy, left_right.

H3: the determinant-institution divergence sharpens over time. We test this
by (a) checking wave interaction significance, and (b) comparing the WV7
interaction on not_religious_dummy across the army vs police models.

Note: `wv7_flag` from the spec is perfectly collinear with `wave_WV7` and
is therefore not added separately.
"""
import os
import warnings
import numpy as np
import pandas as pd
from statsmodels.miscmodels.ordinal_model import OrderedModel
from scipy import stats

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")

YEARS = {"WV5":2007,"WV6":2011,"WV7":2018}

# =========================================================================
# Data prep — WV5/WV6/WV7 only, cluster non-NaN
# =========================================================================
df = pd.read_csv(os.path.join(RESULTS, "pooled_extended_v2.csv"))
df = df[df["wave"].isin(["WV5","WV6","WV7"])].copy()
df = df.dropna(subset=["cluster"]).copy()
df["cluster"] = df["cluster"].astype(int)

df["not_religious_dummy"] = df["rel_person"].map(
    lambda v: 1 if v in (2, 3) else (0 if v == 1 else np.nan))

df["AKP_dummy"]   = (df["party_recode"] == "AKP").astype(int)
df["MHP_dummy"]   = (df["party_recode"] == "MHP").astype(int)
df["HDP_dummy"]   = (df["party_recode"] == "HDP").astype(int)
df["other_dummy"] = (df["party_recode"].isin(["other","IYI"])).astype(int)
# CHP is the implicit reference (all four dummies = 0)

df["wave_WV6"] = (df["wave"] == "WV6").astype(int)
df["wave_WV7"] = (df["wave"] == "WV7").astype(int)

# Interactions
df["nr_x_wv6"]      = df["not_religious_dummy"] * df["wave_WV6"]
df["nr_x_wv7"]      = df["not_religious_dummy"] * df["wave_WV7"]
df["akp_x_wv6"]     = df["AKP_dummy"]           * df["wave_WV6"]
df["akp_x_wv7"]     = df["AKP_dummy"]           * df["wave_WV7"]
df["lr_x_wv6"]      = df["left_right"]          * df["wave_WV6"]
df["lr_x_wv7"]      = df["left_right"]          * df["wave_WV7"]

PREDICTORS = [
    "not_religious_dummy", "rel_attendance", "rel_importance_god",
    "AKP_dummy", "MHP_dummy", "HDP_dummy", "other_dummy",
    "left_right",
    "wave_WV6", "wave_WV7",
    "age", "female", "education_raw", "income_raw", "married_dummy",
    "nr_x_wv6", "nr_x_wv7",
    "akp_x_wv6", "akp_x_wv7",
    "lr_x_wv6", "lr_x_wv7",
]

INST = ["conf_military", "conf_police", "conf_courts"]


# =========================================================================
# Fit one model per institution
# =========================================================================
def fit_inst(outcome):
    needed = [outcome] + PREDICTORS
    sub = df[needed].dropna().copy()
    sub[outcome] = sub[outcome].astype(int)
    # drop zero-variance predictors (safety)
    keep = [p for p in PREDICTORS if sub[p].nunique() > 1]
    mod = OrderedModel(sub[outcome], sub[keep], distr="logit")
    res = mod.fit(method="bfgs", maxiter=300, disp=False)
    return res, len(sub), keep


results = {}
for inst in INST:
    print(f"Fitting {inst} ...")
    res, n, kept = fit_inst(inst)
    results[inst] = {"res": res, "n": n, "kept": kept}
    print(f"  n={n}, pseudo R²={res.prsquared:.4f}")


# =========================================================================
# Collect all coefficients into long-form CSV
# =========================================================================
rows = []
for inst in INST:
    r = results[inst]["res"]
    n = results[inst]["n"]
    for p in r.params.index:
        if p in PREDICTORS:  # exclude thresholds
            rows.append({
                "institution": inst,
                "predictor": p,
                "coef": float(r.params[p]),
                "se":   float(r.bse[p]),
                "p_value": float(r.pvalues[p]),
                "ci_lower": float(r.conf_int().loc[p, 0]),
                "ci_upper": float(r.conf_int().loc[p, 1]),
                "n_obs": n,
                "pseudo_r2": float(r.prsquared),
            })
out = pd.DataFrame(rows)
out.to_csv(os.path.join(RESULTS, "layer4_pooled_interactions.csv"), index=False)
print(f"\nSaved layer4_pooled_interactions.csv  ({len(out)} rows)")


# =========================================================================
# H3 divergence table — main + wave-interaction effects
# =========================================================================
def get(inst, predictor):
    """Return (coef, se, p) for predictor in institution model; or NaN."""
    r = results[inst]["res"]
    if predictor in r.params.index:
        return (float(r.params[predictor]),
                float(r.bse[predictor]),
                float(r.pvalues[predictor]))
    return (np.nan, np.nan, np.nan)


def fmt(c, p):
    if np.isnan(c):
        return "       —      "
    stars = "***" if p < 0.001 else "** " if p < 0.01 else \
            "*  " if p < 0.05  else ".  " if p < 0.10 else "   "
    return f"{c:+.3f}{stars}"


WAVE_KEYS = {
    "WV5 (baseline)": {"main": "{p}",         "x":   None},
    "WV6 interaction": {"main": "{p}_x_wv6_term", "x":   "x_wv6"},
    "WV7 interaction": {"main": "{p}_x_wv7_term", "x":   "x_wv7"},
}

KEY_PREDS = {
    "not_religious_dummy": {"main": "not_religious_dummy",
                            "x6":   "nr_x_wv6", "x7":   "nr_x_wv7"},
    "AKP_dummy":           {"main": "AKP_dummy",
                            "x6":   "akp_x_wv6", "x7":   "akp_x_wv7"},
    "left_right":          {"main": "left_right",
                            "x6":   "lr_x_wv6",  "x7":   "lr_x_wv7"},
}

print("\n" + "=" * 110)
print("H3 DIVERGENCE TABLE — main + wave-interaction effects (pooled across clusters)")
print("=" * 110)
print("Cell format: coefficient + significance stars  (*** p<.001  ** p<.01  * p<.05  . p<.10)")
print("'total WV6/WV7 effect' = main effect + wave interaction")
print()

header_fmt = "{:<22} {:<15} {:>14} {:>14} {:>14} {:>14}"
print(header_fmt.format("predictor","wave","army","police","courts","army-police"))
print("-" * 96)

H3_rows = []
for predictor, keymap in KEY_PREDS.items():
    # WV5 row: just main effect
    cells = {}
    for inst in INST:
        c, _, p = get(inst, keymap["main"])
        cells[inst] = (c, p)
    army_c = cells["conf_military"][0]
    pol_c  = cells["conf_police"][0]
    spread = army_c - pol_c if not np.isnan(army_c) and not np.isnan(pol_c) else np.nan
    print(header_fmt.format(
        predictor, "WV5 (baseline)",
        fmt(*cells["conf_military"]),
        fmt(*cells["conf_police"]),
        fmt(*cells["conf_courts"]),
        f"{spread:+.3f}" if not np.isnan(spread) else "   —    "))
    H3_rows.append({"predictor": predictor, "wave": "WV5",
                    "army_coef": army_c, "police_coef": pol_c,
                    "courts_coef": cells["conf_courts"][0],
                    "army_police_spread": spread})

    # WV6 interaction + total WV6 effect
    inter_cells = {}
    total_cells = {}
    for inst in INST:
        c_int, _, p_int = get(inst, keymap["x6"])
        c_main, _, _    = get(inst, keymap["main"])
        inter_cells[inst] = (c_int, p_int)
        total_cells[inst] = (c_main + c_int if not np.isnan(c_main + c_int) else np.nan,
                             p_int)  # p of interaction
    army_int = inter_cells["conf_military"][0]
    pol_int  = inter_cells["conf_police"][0]
    spread = (total_cells["conf_military"][0] - total_cells["conf_police"][0]
              if not any(np.isnan([total_cells["conf_military"][0],
                                   total_cells["conf_police"][0]])) else np.nan)
    print(header_fmt.format(
        "", "WV6 interaction",
        fmt(*inter_cells["conf_military"]),
        fmt(*inter_cells["conf_police"]),
        fmt(*inter_cells["conf_courts"]),
        ""))
    print(header_fmt.format(
        "", "  total WV6 effect",
        fmt(*total_cells["conf_military"]),
        fmt(*total_cells["conf_police"]),
        fmt(*total_cells["conf_courts"]),
        f"{spread:+.3f}" if not np.isnan(spread) else "   —    "))
    H3_rows.append({"predictor": predictor, "wave": "WV6",
                    "army_coef": total_cells["conf_military"][0],
                    "police_coef": total_cells["conf_police"][0],
                    "courts_coef": total_cells["conf_courts"][0],
                    "army_police_spread": spread})

    # WV7 interaction + total WV7 effect
    inter_cells = {}
    total_cells = {}
    for inst in INST:
        c_int, _, p_int = get(inst, keymap["x7"])
        c_main, _, _    = get(inst, keymap["main"])
        inter_cells[inst] = (c_int, p_int)
        total_cells[inst] = (c_main + c_int if not np.isnan(c_main + c_int) else np.nan,
                             p_int)
    army_int = inter_cells["conf_military"][0]
    pol_int  = inter_cells["conf_police"][0]
    spread = (total_cells["conf_military"][0] - total_cells["conf_police"][0]
              if not any(np.isnan([total_cells["conf_military"][0],
                                   total_cells["conf_police"][0]])) else np.nan)
    print(header_fmt.format(
        "", "WV7 interaction",
        fmt(*inter_cells["conf_military"]),
        fmt(*inter_cells["conf_police"]),
        fmt(*inter_cells["conf_courts"]),
        ""))
    print(header_fmt.format(
        "", "  total WV7 effect",
        fmt(*total_cells["conf_military"]),
        fmt(*total_cells["conf_police"]),
        fmt(*total_cells["conf_courts"]),
        f"{spread:+.3f}" if not np.isnan(spread) else "   —    "))
    H3_rows.append({"predictor": predictor, "wave": "WV7",
                    "army_coef": total_cells["conf_military"][0],
                    "police_coef": total_cells["conf_police"][0],
                    "courts_coef": total_cells["conf_courts"][0],
                    "army_police_spread": spread})
    print()  # blank between predictors


# =========================================================================
# Cross-institution test: not_religious_dummy × WV7 interaction —
# army vs police difference, with conservative SE assuming independence
# (true SE smaller because same respondents → positive cross-model
#  residual correlation; if z is significant under indep, the difference
#  is robust)
# =========================================================================
ca, sa, pa = get("conf_military", "nr_x_wv7")
cp, sp, pp = get("conf_police",   "nr_x_wv7")
diff = ca - cp
se_diff_indep = np.sqrt(sa**2 + sp**2)
z = diff / se_diff_indep
p_two = 2 * (1 - stats.norm.cdf(abs(z)))

print("=" * 96)
print("Cross-institution test: not_religious_dummy × WV7 interaction")
print("  army interaction coef  : {:+.4f}  (SE {:.4f})".format(ca, sa))
print("  police interaction coef: {:+.4f}  (SE {:.4f})".format(cp, sp))
print(f"  difference (army - police): {diff:+.4f}")
print(f"  SE under independence (upper bound): {se_diff_indep:.4f}")
print(f"  z = {z:.3f}   p_two-sided = {p_two:.4f}")
print("  (same respondents in both models → true SE smaller, so this is")
print("   conservative; significance here implies a robust divergence.)")

# Same test for AKP × WV7
print()
ca, sa, _ = get("conf_military", "akp_x_wv7")
cp, sp, _ = get("conf_police",   "akp_x_wv7")
diff = ca - cp
se_diff_indep = np.sqrt(sa**2 + sp**2)
z = diff / se_diff_indep
p_two = 2 * (1 - stats.norm.cdf(abs(z)))
print("Cross-institution test: AKP_dummy × WV7 interaction")
print("  army  : {:+.4f}  (SE {:.4f})".format(ca, sa))
print("  police: {:+.4f}  (SE {:.4f})".format(cp, sp))
print(f"  difference (army - police): {diff:+.4f}    z = {z:.3f}   p = {p_two:.4f}")

print()
ca, sa, _ = get("conf_military", "lr_x_wv7")
cp, sp, _ = get("conf_police",   "lr_x_wv7")
diff = ca - cp
se_diff_indep = np.sqrt(sa**2 + sp**2)
z = diff / se_diff_indep
p_two = 2 * (1 - stats.norm.cdf(abs(z)))
print("Cross-institution test: left_right × WV7 interaction")
print("  army  : {:+.4f}  (SE {:.4f})".format(ca, sa))
print("  police: {:+.4f}  (SE {:.4f})".format(cp, sp))
print(f"  difference (army - police): {diff:+.4f}    z = {z:.3f}   p = {p_two:.4f}")
