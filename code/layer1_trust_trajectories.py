"""
Layer-1 analysis: institutional confidence trajectories across WVS Turkey
waves 2-7. Army / Police / Courts, with pairwise gaps and Mann-Whitney
tests of consecutive-wave shifts.
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")

WAVES = ["WV2","WV3","WV4","WV5","WV6","WV7"]
YEARS = {"WV2":1990,"WV3":1996,"WV4":2001,"WV5":2007,"WV6":2011,"WV7":2018}
INST  = {"conf_military":"army", "conf_police":"police", "conf_courts":"courts"}

df = pd.read_csv(os.path.join(RESULTS, "pooled_extended_v2.csv"))
print(f"Loaded pooled_extended_v2.csv: {df.shape}")
print(f"No survey weight column present — using equal weights (note).\n")


# =========================================================================
# 1) Trajectories — mean + 95% CI per (wave, institution)
# =========================================================================
rows = []
for col, inst in INST.items():
    for w in WAVES:
        s = df.loc[df["wave"] == w, col].dropna()
        if len(s) == 0:
            rows.append({"wave": w, "year": YEARS[w], "institution": inst,
                         "mean": np.nan, "ci_lower": np.nan,
                         "ci_upper": np.nan, "n": 0,
                         "note": "not asked / missing"})
            continue
        m  = float(s.mean())
        sd = float(s.std(ddof=1))
        n  = int(len(s))
        se = sd / np.sqrt(n)
        rows.append({"wave": w, "year": YEARS[w], "institution": inst,
                     "mean": round(m, 4),
                     "ci_lower": round(m - 1.96 * se, 4),
                     "ci_upper": round(m + 1.96 * se, 4),
                     "n": n, "note": ""})
traj = pd.DataFrame(rows)
traj.to_csv(os.path.join(RESULTS, "layer1_trajectories.csv"), index=False)
print("=== Trajectories (mean ± 95% CI, equal-weight) ===")
print(traj.to_string(index=False))


# =========================================================================
# 2) Pairwise gaps per wave (army - police, army - courts)
# =========================================================================
gap_rows = []
for w in WAVES:
    sub = df[df["wave"] == w]
    mil = sub["conf_military"].mean()
    pol = sub["conf_police"].mean()
    crt = sub["conf_courts"].mean()
    gap_rows.append({
        "wave": w, "year": YEARS[w],
        "mean_army": round(mil, 4),
        "mean_police": round(pol, 4),
        "mean_courts": round(crt, 4) if not np.isnan(crt) else np.nan,
        "army_police_gap": round(mil - pol, 4),
        "army_courts_gap": (round(mil - crt, 4)
                            if not np.isnan(crt) else np.nan),
    })
gaps = pd.DataFrame(gap_rows)
gaps[["wave","year","army_police_gap","army_courts_gap"]].to_csv(
    os.path.join(RESULTS, "layer1_gaps.csv"), index=False)
print("\n=== Pairwise institution gaps per wave ===")
print(gaps.to_string(index=False))


# =========================================================================
# 3) Mann-Whitney U between consecutive waves per institution
# =========================================================================
trans_rows = []
for col, inst in INST.items():
    series_by_wave = {w: df.loc[df["wave"] == w, col].dropna().values
                      for w in WAVES}
    for i in range(len(WAVES) - 1):
        w_a, w_b = WAVES[i], WAVES[i + 1]
        a, b = series_by_wave[w_a], series_by_wave[w_b]
        if len(a) == 0 or len(b) == 0:
            trans_rows.append({
                "institution": inst, "wave_pair": f"{w_a}->{w_b}",
                "n_a": len(a), "n_b": len(b),
                "mean_a": np.nan, "mean_b": np.nan,
                "U_stat": np.nan, "p_value": np.nan,
                "direction": "skipped (one wave missing)",
            })
            continue
        U, p = stats.mannwhitneyu(a, b, alternative="two-sided")
        ma, mb = float(np.mean(a)), float(np.mean(b))
        if p < 0.05:
            arrow = "▲ up" if mb > ma else "▼ down"
        else:
            arrow = "n.s."
        trans_rows.append({
            "institution": inst, "wave_pair": f"{w_a}->{w_b}",
            "n_a": len(a), "n_b": len(b),
            "mean_a": round(ma, 4), "mean_b": round(mb, 4),
            "U_stat": round(float(U), 1),
            "p_value": float(p),
            "direction": arrow,
        })

trans = pd.DataFrame(trans_rows)
# CSV keeps just the requested columns; full table printed
trans[["institution","wave_pair","U_stat","p_value","direction"]].to_csv(
    os.path.join(RESULTS, "layer1_transitions.csv"), index=False)

print("\n=== Mann-Whitney U between consecutive waves ===")
# Format p_value nicely for the console
disp = trans.copy()
disp["p_value"] = disp["p_value"].apply(
    lambda p: "—" if pd.isna(p) else (f"{p:.2e}" if p < 1e-3 else f"{p:.4f}"))
print(disp.to_string(index=False))

print("\nFiles written:")
for f in ["layer1_trajectories.csv","layer1_gaps.csv","layer1_transitions.csv"]:
    print(f"  results/{f}")
