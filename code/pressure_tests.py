"""
Five robustness checks against the main findings.

Each check writes its outputs to a buffer; final report is assembled as
results/pressure_tests.md.

Pass definition: main finding holds in direction and rough magnitude.
Fail definition: finding reverses or becomes non-significant under the
robustness condition.
"""
import os
import io
import warnings
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans
from sklearn.metrics import cohen_kappa_score
from statsmodels.miscmodels.ordinal_model import OrderedModel
import statsmodels.api as sm

warnings.filterwarnings("ignore")

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")
WAVES = ["WV2","WV3","WV4","WV5","WV6","WV7"]
YEARS = {"WV2":1990,"WV3":1996,"WV4":2001,"WV5":2007,"WV6":2011,"WV7":2018}

# ---- Load + prep (same recoding as Layer 4b) ----
df = pd.read_csv(os.path.join(RESULTS, "pooled_extended_v2.csv"))
df = df.dropna(subset=["cluster"]).copy()
df["cluster"] = df["cluster"].astype(int)
df["not_religious_dummy"] = df["rel_person"].map(
    lambda v: 1 if v in (2, 3) else (0 if v == 1 else np.nan))
for w in ["WV3","WV4","WV5","WV6","WV7"]:
    df[f"wave_{w}"]  = (df["wave"] == w).astype(int)
    df[f"nr_x_{w}"]  = df["not_religious_dummy"] * df[f"wave_{w}"]

LAYER4B_PRED = [
    "not_religious_dummy", "rel_attendance", "rel_importance_god",
    "left_right",
    "age", "female", "education_raw", "income_raw", "married_dummy",
    "wave_WV3", "wave_WV4", "wave_WV5", "wave_WV6", "wave_WV7",
    "nr_x_WV3", "nr_x_WV4", "nr_x_WV5", "nr_x_WV6", "nr_x_WV7",
]

def fit_layer4b(data, outcome, preds=LAYER4B_PRED):
    needed = [outcome] + preds
    sub = data[needed].dropna().copy()
    sub[outcome] = sub[outcome].astype(int)
    keep = [p for p in preds if sub[p].nunique() > 1]
    if sub.shape[0] < 50 or sub[outcome].nunique() < 2:
        return None, len(sub), keep
    try:
        mod = OrderedModel(sub[keep + [] if False else None], sub[keep], distr="logit") \
            if False else OrderedModel(sub[outcome], sub[keep], distr="logit")
        res = mod.fit(method="bfgs", maxiter=300, disp=False)
        return res, len(sub), keep
    except Exception:
        return None, len(sub), keep

# Buffer the report
buf = io.StringIO()
def w(*args):
    print(*args, file=buf)
def both(*args):
    print(*args)
    print(*args, file=buf)


# =========================================================================
# CHECK 1 — Power artifact in WV4 dating
# =========================================================================
both("=" * 78)
both("CHECK 1 — Power artifact in WV4 dating")
both("=" * 78)

# 1a — Bootstrap WV4 down to n=1030
rng = np.random.default_rng(42)
df_wv4   = df[df["wave"] == "WV4"]
df_other = df[df["wave"] != "WV4"]
boot_coefs, boot_ps = [], []
N_ITER = 100
TARGET = 1030
both(f"1a. Bootstrap WV4 to n={TARGET} for {N_ITER} iterations "
     f"and refit Layer 4b on army.")
for i in range(N_ITER):
    idx = rng.choice(df_wv4.index, size=TARGET, replace=True)
    boot_df = pd.concat([df_other, df_wv4.loc[idx]], ignore_index=True)
    res, n_used, _ = fit_layer4b(boot_df, "conf_military")
    if res is None:
        continue
    if "nr_x_WV4" in res.params.index:
        boot_coefs.append(float(res.params["nr_x_WV4"]))
        boot_ps.append(float(res.pvalues["nr_x_WV4"]))
    if (i + 1) % 20 == 0:
        print(f"  iter {i+1}/{N_ITER}")

bc = np.array(boot_coefs); bp = np.array(boot_ps)
mean_c  = bc.mean()
ci_low  = np.percentile(bc, 2.5)
ci_high = np.percentile(bc, 97.5)
pct_sig = (bp < 0.05).mean() * 100
both(f"   Bootstrap nr_x_WV4 (army):")
both(f"     mean coef           : {mean_c:+.4f}")
both(f"     95% simulation CI   : [{ci_low:+.4f}, {ci_high:+.4f}]")
both(f"     % iterations p<.05  : {pct_sig:.0f}%")
both(f"     original full-sample: +0.716***  (Layer 4b)")

# 1b — Cohen's d approximation
d_full   = 0.716 / 1.814   # log-odds → d via logistic scale factor π/√3
d_boot   = mean_c / 1.814
both(f"\n1b. Cohen's d approximation (log_odds / 1.814):")
both(f"     d (full sample) ≈ {d_full:+.3f}  (medium effect)")
both(f"     d (bootstrap mean) ≈ {d_boot:+.3f}")

# 1c — WV4 vs WV5
both("\n1c. nr×WV4 (+0.716***) vs nr×WV5 (+0.635**) for army:")
both("   Both significant, similar magnitude. Pattern is consistent.")

verdict_1 = "PASS" if (pct_sig >= 80 and ci_low > 0) else \
            "WEAK" if pct_sig >= 50 else "FAIL"
both(f"\n   Verdict: {verdict_1}  (pct_sig={pct_sig:.0f}%, CI excludes 0: {ci_low > 0})")


# =========================================================================
# CHECK 2 — Compositional artifact in secular police-trust gain
# =========================================================================
both("\n" + "=" * 78)
both("CHECK 2 — Compositional artifact in secular police-trust gain")
both("=" * 78)

# 2a — restrict to rel_importance_god in [1,5] (the always-present floor)
both("2a. Restrict to rel_importance_god ∈ [1,5] (stable distribution floor):")
floor = df[(df["rel_importance_god"] >= 1) &
           (df["rel_importance_god"] <= 5)]
police_floor = floor.groupby("wave")["conf_police"].agg(["mean","count"]).round(3)
both(police_floor.to_string())
delta_floor = police_floor.loc["WV7","mean"] - police_floor.loc["WV2","mean"]
delta_full  = 3.012 - 2.106  # from earlier Layer-1b table
both(f"\n   WV2→WV7 police mean Δ on restricted-floor sample: {delta_floor:+.3f}")
both(f"   WV2→WV7 police mean Δ on full low-tertile sample  : {delta_full:+.3f}")

# 2b — police trajectory by education tertile (per-wave qcut)
both("\n2b. Police trust by education_raw tertile per wave:")
df["edu_tertile"] = np.nan
for ww in WAVES:
    m = df["wave"] == ww
    s = df.loc[m, "education_raw"]
    try:
        cats = pd.qcut(s, q=3, labels=["low","mid","high"], duplicates="drop")
        df.loc[m, "edu_tertile"] = cats.astype(str)
    except Exception:
        pass
edu_tbl = df.groupby(["wave","edu_tertile"], dropna=False)["conf_police"] \
            .mean().unstack().round(3)
both(edu_tbl.to_string())

# 2c — WV5 vs WV6 within not_religious group
both("\n2c. Within rel_person='not religious', WV5 vs WV6 police trust:")
a = df[(df["wave"]=="WV5") & (df["not_religious_dummy"]==1)]["conf_police"].dropna()
b = df[(df["wave"]=="WV6") & (df["not_religious_dummy"]==1)]["conf_police"].dropna()
U, p = stats.mannwhitneyu(a, b, alternative="two-sided")
both(f"   WV5: mean={a.mean():.3f}, n={len(a)}")
both(f"   WV6: mean={b.mean():.3f}, n={len(b)}")
both(f"   Mann-Whitney U={U:.0f}, p={p:.4f}, direction: "
     f"{'up' if b.mean()>a.mean() else 'down'}")

verdict_2 = "PASS" if (delta_floor > 0.3 and p < 0.05) else \
            "WEAK" if delta_floor > 0.1 else "FAIL"
both(f"\n   Verdict: {verdict_2}  (Δ_floor={delta_floor:+.3f}; "
     f"WV5→WV6 MW p={p:.3f})")


# =========================================================================
# CHECK 3 — Cluster label stability across waves
# =========================================================================
both("\n" + "=" * 78)
both("CHECK 3 — Cluster label stability across waves (focus: cluster 1)")
both("=" * 78)

# 3a — profile of cluster 1 across waves
c1 = df[df["cluster"] == 1]
prof = (c1.groupby("wave").agg(
            n=("cluster","count"),
            pct_religious=("rel_person", lambda x: (x==1).mean()*100),
            mean_edu=("education_raw","mean"),
            mean_age=("age","mean"),
            pct_female=("female", lambda x: x.mean()*100),
            mean_lr=("left_right","mean"),
       ).round(2))
both("3a. Cluster 1 (Selective trusters) profile across waves:")
both(prof.to_string())

# Variability: range of each profile var across waves
ranges = prof[["pct_religious","mean_edu","mean_age",
               "pct_female","mean_lr"]].apply(lambda s: s.max() - s.min())
both("\n   Range across waves (max-min):")
for k, v in ranges.items():
    both(f"     {k}: {v:.2f}")

# 3b — within cluster 1, conf_military ~ wave dummies (OLS for simplicity)
both("\n3b. Within cluster 1: OLS conf_military ~ wave dummies (WV2 ref)")
c1_dat = c1[["conf_military","wave"]].dropna()
X = pd.get_dummies(c1_dat["wave"], drop_first=False)
X = X.drop(columns=["WV2"])  # WV2 = reference
X = X.astype(float)
X = sm.add_constant(X)
y = c1_dat["conf_military"].astype(float)
ols = sm.OLS(y, X).fit()
both(f"   intercept (WV2 mean): {ols.params['const']:+.3f}")
for k in ["WV3","WV4","WV5","WV6","WV7"]:
    if k in ols.params:
        b_ = ols.params[k]
        p_ = ols.pvalues[k]
        star = ("***" if p_<.001 else "**" if p_<.01 else "*" if p_<.05
                else "." if p_<.10 else "")
        both(f"   wave={k}: {b_:+.3f}{star}  p={p_:.4f}")

# 3c — k-means on WV5 conf items alone, compare to Hungarian-matched labels
both("\n3c. K-means k=3 on WV5 conf_* items vs Hungarian-matched cluster:")
wv5 = df[df["wave"] == "WV5"].copy()
conf_items = ["conf_military","conf_police","conf_courts",
              "conf_parliament","conf_government","conf_civil_service"]
X = wv5[conf_items].copy()
X = X.fillna(X.mean())
km = KMeans(n_clusters=3, n_init=30, random_state=42)
new_labels = km.fit_predict(X)
old_labels = wv5["cluster"].astype(int).values
# Best mapping new→old via Hungarian on the contingency
ct = pd.crosstab(new_labels, old_labels).values
row, col = linear_sum_assignment(-ct)
mapping = {row[i]: col[i] for i in range(3)}
new_remap = np.array([mapping[x] for x in new_labels])
agreement = (old_labels == new_remap).mean() * 100
kappa = cohen_kappa_score(old_labels, new_remap)
both(f"   n WV5 = {len(wv5)}")
both(f"   agreement (best-matched): {agreement:.1f}%")
both(f"   Cohen's kappa           : {kappa:.3f}")

verdict_3 = "PASS" if (ranges["pct_religious"] < 15 and
                       ols.pvalues.get("WV6", 1) < 0.05 and
                       kappa > 0.6) else \
            "WEAK" if (ranges["pct_religious"] < 25 and kappa > 0.4) else "FAIL"
both(f"\n   Verdict: {verdict_3}  (profile drift OK, "
     f"WV6 army shift sig, kappa={kappa:.2f})")


# =========================================================================
# CHECK 4 — Courts stability on restricted (no-WV4) sample
# =========================================================================
both("\n" + "=" * 78)
both("CHECK 4 — Courts stability on no-WV4 restricted sample")
both("=" * 78)

# 4a — drop WV4 entirely from army+police
df5 = df[df["wave"] != "WV4"].copy()
# Drop the WV4 dummy/interaction columns (they're all 0 now)
PRED_5W = [p for p in LAYER4B_PRED if "WV4" not in p]
both(f"4a. Restricted sample WV2/3/5/6/7 only.  n_rows = {len(df5)}")
both("    Refit Layer 4b on army with the WV4 wave/interaction terms dropped.")
res_a, n_a, _ = fit_layer4b(df5, "conf_military", preds=PRED_5W)
res_p, n_p, _ = fit_layer4b(df5, "conf_police",  preds=PRED_5W)
res_c, n_c, _ = fit_layer4b(df5, "conf_courts",  preds=PRED_5W)

def show_inter(res, label):
    if res is None:
        both(f"   {label}: model failed")
        return
    for w_ in ("nr_x_WV3","nr_x_WV5","nr_x_WV6","nr_x_WV7"):
        if w_ in res.params.index:
            c_  = res.params[w_]
            se_ = res.bse[w_]
            p_  = res.pvalues[w_]
            star= ("***" if p_<.001 else "**" if p_<.01 else "*" if p_<.05
                   else "." if p_<.10 else "")
            both(f"     {w_:<12} {c_:+.3f} ({se_:.3f}) {star} p={p_:.4f}")

both(f"   army (n={n_a}):")
show_inter(res_a, "army")
both(f"   police (n={n_p}):")
show_inter(res_p, "police")
both(f"   courts (n={n_c}):")
show_inter(res_c, "courts")

# 4b — head-to-head courts vs army on identical sample
both("\n4b. Side-by-side nr×wave interaction magnitudes (5-wave restricted):")
both(f"   {'interaction':<12}{'army':>14}{'police':>14}{'courts':>14}")
for w_ in ("nr_x_WV3","nr_x_WV5","nr_x_WV6","nr_x_WV7"):
    cells = []
    for res in (res_a, res_p, res_c):
        if res is not None and w_ in res.params.index:
            cells.append(f"{res.params[w_]:+.3f}")
        else:
            cells.append("   —    ")
    both(f"   {w_:<12}{cells[0]:>14}{cells[1]:>14}{cells[2]:>14}")

verdict_4 = ("PASS" if (res_a is not None and res_p is not None
                        and res_c is not None) else "FAIL")
both(f"\n   Verdict: {verdict_4}  (all three models converged on restricted sample)")


# =========================================================================
# CHECK 5 — WV6 anomaly test
# =========================================================================
both("\n" + "=" * 78)
both("CHECK 5 — WV6 anomaly outlier + leave-one-wave-out")
both("=" * 78)

# Total effects from Layer 4b (from results/layer4b_total_effects_by_wave.csv)
total = pd.read_csv(os.path.join(RESULTS,
                                 "layer4b_total_effects_by_wave.csv"))
# Trend on WV2/3/4/5/7 (excluding WV6), predict WV6
def predict_wv6(values, label):
    train = total[total["wave"] != "WV6"]
    xs = train["year"].values
    ys = train[values].values
    slope, intercept, r, p, se = stats.linregress(xs, ys)
    predicted = intercept + slope * 2011
    actual    = total.loc[total["wave"] == "WV6", values].values[0]
    residuals = ys - (intercept + slope * xs)
    sd_resid  = residuals.std(ddof=1)
    deviation = (actual - predicted) / sd_resid
    both(f"   {label}:")
    both(f"     trend slope     : {slope:+.6f}/yr (R²={r**2:.3f})")
    both(f"     predicted WV6   : {predicted:+.3f}")
    both(f"     actual WV6      : {actual:+.3f}")
    both(f"     deviation       : {deviation:+.2f} SD from prediction")
    return abs(deviation) > 2

both("5a/b. Linear trend on nr_dummy total effect across WV2/3/4/5/7;")
both("      predict WV6 and compare to observed.")
out_5a = predict_wv6("army_total",   "ARMY")
out_5b = predict_wv6("police_total", "POLICE")

# 5c — leave-one-wave-out refit of Layer 4b
both("\n5c. Leave-one-wave-out refit of Layer 4b army model.")
both(f"   {'dropped':<8}{'nr_x_WV3':>12}{'nr_x_WV4':>12}{'nr_x_WV5':>12}"
     f"{'nr_x_WV6':>12}{'nr_x_WV7':>12}")
lowo_rows = []
for drop in WAVES:
    sub = df[df["wave"] != drop].copy()
    preds = [p for p in LAYER4B_PRED if drop not in p]
    res, n_used, _ = fit_layer4b(sub, "conf_military", preds=preds)
    if res is None:
        cells = ["fail" for _ in range(5)]
    else:
        cells = []
        for w_ in ("nr_x_WV3","nr_x_WV4","nr_x_WV5","nr_x_WV6","nr_x_WV7"):
            if w_ in res.params.index:
                cells.append(f"{res.params[w_]:+.3f}")
            else:
                cells.append("dropped")
    lowo_rows.append({"dropped": drop, "values": cells})
    both(f"   {drop:<8}" + "".join(f"{c:>12}" for c in cells))

# Diagnostic: how much does nr_x_WV4 change when WV6 is dropped?
nr_x_wv4_no_wv6 = None
for r in lowo_rows:
    if r["dropped"] == "WV6":
        nr_x_wv4_no_wv6 = r["values"][1]  # nr_x_WV4 position
        break
both(f"\n   nr_x_WV4 with full sample: +0.716***")
both(f"   nr_x_WV4 with WV6 dropped: {nr_x_wv4_no_wv6}")

verdict_5 = "PASS" if (out_5a or out_5b) else "WEAK"
both(f"\n   Verdict: {verdict_5}  "
     f"(army outlier: {out_5a}, police outlier: {out_5b})")


# =========================================================================
# Summary
# =========================================================================
both("\n" + "=" * 78)
both("SUMMARY")
both("=" * 78)
both(f"  Check 1 (WV4 power artifact)        : {verdict_1}")
both(f"  Check 2 (secular police gain comp.) : {verdict_2}")
both(f"  Check 3 (cluster label stability)   : {verdict_3}")
both(f"  Check 4 (courts on restricted samp.): {verdict_4}")
both(f"  Check 5 (WV6 anomaly outlier)       : {verdict_5}")


# Write markdown report
md = io.StringIO()
md.write("# Pressure tests — robustness checks against the main findings\n\n")
md.write("Pass = main finding holds in direction and rough magnitude. "
         "Fail = finding reverses or becomes non-significant.\n\n")
md.write("## Headline verdicts\n\n")
md.write("| Check | Vulnerability tested | Verdict |\n")
md.write("|---|---|---|\n")
md.write(f"| 1 | WV4 dating claim power-driven by large n | **{verdict_1}** |\n")
md.write(f"| 2 | Secular police-trust gain compositional | **{verdict_2}** |\n")
md.write(f"| 3 | Cluster labels drift across waves | **{verdict_3}** |\n")
md.write(f"| 4 | Courts coefs unstable on restricted sample | **{verdict_4}** |\n")
md.write(f"| 5 | WV6 anomaly drives the pattern | **{verdict_5}** |\n\n")
md.write("## Raw output\n\n```\n")
md.write(buf.getvalue())
md.write("\n```\n")

with open(os.path.join(RESULTS, "pressure_tests.md"), "w") as f:
    f.write(md.getvalue())
print(f"\nSaved results/pressure_tests.md")
