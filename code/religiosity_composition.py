"""
Is the growth of the low-religiosity tertile from 184 (WV2) to 825 (WV7)
a real secularization trend, a sampling shift, or a scale-wording shift?

Three diagnostics:
  1) rel_importance_god distribution per wave (mean, sd, % <=7, % =10)
  2) rel_person crosstab × wave (% not-religious, % convinced atheist)
  3) Low-tertile demographic profile (age, female%, education) — WV2 vs WV7
"""
import os
import numpy as np
import pandas as pd

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")
WAVES = ["WV2","WV3","WV4","WV5","WV6","WV7"]
YEARS = {"WV2":1990,"WV3":1996,"WV4":2001,"WV5":2007,"WV6":2011,"WV7":2018}

df = pd.read_csv(os.path.join(RESULTS, "pooled_extended_v2.csv"))


# =========================================================================
# 1) rel_importance_god distribution per wave
# =========================================================================
rows = []
print("=" * 78)
print("1) rel_importance_god — distribution per wave")
print("=" * 78)
print(f"{'wave':<6}{'year':<7}{'n':>6}{'mean':>9}{'sd':>8}"
      f"{'% <=7':>10}{'% = 10':>10}")
print("-" * 56)
for w in WAVES:
    s = df.loc[df["wave"] == w, "rel_importance_god"].dropna()
    n = len(s)
    m = s.mean()
    sd = s.std(ddof=1)
    pct_low  = 100 * (s <= 7).mean()
    pct_ceil = 100 * (s == 10).mean()
    rows.append({"wave": w, "year": YEARS[w], "n_valid_rel": n,
                 "mean_rel": round(m, 3), "sd_rel": round(sd, 3),
                 "pct_rel_le_7": round(pct_low, 2),
                 "pct_rel_eq_10": round(pct_ceil, 2)})
    print(f"{w:<6}{YEARS[w]:<7}{n:>6}{m:>9.3f}{sd:>8.3f}"
          f"{pct_low:>9.1f}%{pct_ceil:>9.1f}%")


# =========================================================================
# 2) rel_person × wave  (1=religious, 2=not religious, 3=convinced atheist)
# =========================================================================
print("\n" + "=" * 78)
print("2) rel_person — % not-religious, % convinced atheist by wave")
print("=" * 78)
print(f"{'wave':<6}{'year':<7}{'n':>6}{'% relig':>10}"
      f"{'% not relig':>14}{'% atheist':>12}")
print("-" * 56)
for w in WAVES:
    s = df.loc[df["wave"] == w, "rel_person"].dropna()
    n = len(s)
    pct1 = 100 * (s == 1).mean()
    pct2 = 100 * (s == 2).mean()
    pct3 = 100 * (s == 3).mean()
    # append to the existing row for this wave
    for r in rows:
        if r["wave"] == w:
            r["n_valid_relperson"] = n
            r["pct_religious"] = round(pct1, 2)
            r["pct_not_religious"] = round(pct2, 2)
            r["pct_atheist"] = round(pct3, 2)
            break
    print(f"{w:<6}{YEARS[w]:<7}{n:>6}{pct1:>9.1f}%{pct2:>13.1f}%{pct3:>11.1f}%")


# =========================================================================
# 3) Demographics of low-religiosity tertile (rel_importance_god <= 7)
#    WV2 vs WV7
# =========================================================================
print("\n" + "=" * 78)
print("3) Low-religiosity tertile (rel_importance_god ≤ 7) demographics")
print("=" * 78)
df["low_rel"] = (df["rel_importance_god"] <= 7)

profile_rows = []
print(f"{'wave':<6}{'year':<7}{'n_low':>7}{'mean_age':>11}"
      f"{'pct_female':>13}{'mean_edu':>12}")
print("-" * 56)
for w in WAVES:
    sub = df[(df["wave"] == w) & df["low_rel"]]
    n = len(sub)
    mean_age = sub["age"].mean()
    pct_fem  = 100 * sub["female"].mean()
    mean_edu = sub["education_raw"].mean()
    profile_rows.append({"wave": w, "year": YEARS[w],
                         "n_low_rel": n,
                         "low_rel_mean_age": round(mean_age, 2),
                         "low_rel_pct_female": round(pct_fem, 2),
                         "low_rel_mean_education_raw": round(mean_edu, 3)})
    print(f"{w:<6}{YEARS[w]:<7}{n:>7}{mean_age:>11.1f}"
          f"{pct_fem:>12.1f}%{mean_edu:>12.2f}")

# Also compute overall sample demographics for comparison (sampling drift check)
print("\nReference — overall-sample demographics per wave:")
print(f"{'wave':<6}{'year':<7}{'n':>6}{'mean_age':>11}"
      f"{'pct_female':>13}{'mean_edu':>12}")
print("-" * 56)
overall_rows = []
for w in WAVES:
    sub = df[df["wave"] == w]
    n = len(sub)
    ma = sub["age"].mean()
    pf = 100 * sub["female"].mean()
    me = sub["education_raw"].mean()
    overall_rows.append({"wave": w, "year": YEARS[w],
                         "overall_mean_age": round(ma, 2),
                         "overall_pct_female": round(pf, 2),
                         "overall_mean_education_raw": round(me, 3)})
    print(f"{w:<6}{YEARS[w]:<7}{n:>6}{ma:>11.1f}{pf:>12.1f}%{me:>12.2f}")

print("\n--- WV2 vs WV7 direct comparison ---")
prof_df = pd.DataFrame(profile_rows).set_index("wave")
overall_df = pd.DataFrame(overall_rows).set_index("wave")
print("\nLow-religiosity tertile profile:")
print(prof_df.loc[["WV2","WV7"]].to_string())
print("\nOverall sample profile:")
print(overall_df.loc[["WV2","WV7"]].to_string())


# =========================================================================
# Merge into one CSV
# =========================================================================
base = pd.DataFrame(rows)
prof = pd.DataFrame(profile_rows)
ovr  = pd.DataFrame(overall_rows)
out = base.merge(prof, on=["wave","year"]).merge(ovr, on=["wave","year"])
out.to_csv(os.path.join(RESULTS, "layer1_religiosity_composition.csv"),
           index=False)
print(f"\nSaved results/layer1_religiosity_composition.csv ({len(out)} rows)")
