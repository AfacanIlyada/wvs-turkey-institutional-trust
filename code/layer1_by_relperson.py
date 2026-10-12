"""
Layer-1 robustness: replicate the religiosity-by-institution analysis using
rel_person (self-identification) instead of rel_importance_god tertiles.

Codes per WVS:
  1 = Religious person
  2 = Not a religious person
  3 = Convinced atheist
Per spec: collapse atheist (3) into not_religious if n < 100 per wave.
"""
import os
import numpy as np
import pandas as pd

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")
WAVES = ["WV2","WV3","WV4","WV5","WV6","WV7"]
YEARS = {"WV2":1990,"WV3":1996,"WV4":2001,"WV5":2007,"WV6":2011,"WV7":2018}

df = pd.read_csv(os.path.join(RESULTS, "pooled_extended_v2.csv"))


# ----------------------------- 1) rel_person crosstab --------------------
print("=" * 78)
print("rel_person value_counts per wave (raw codes 1/2/3)")
print("=" * 78)
cross = (df.groupby("wave")["rel_person"]
           .value_counts(dropna=False)
           .unstack(fill_value=0)
           .reindex(WAVES))
cross.columns = [f"code_{int(c)}" if pd.notna(c) else "NaN"
                 for c in cross.columns]
cross["total"] = cross.sum(axis=1)
print(cross.to_string())

print("\nRow percentages (of valid):")
valid_cols = [c for c in cross.columns if c not in ("total",)
              and c != "NaN"]
pct = cross[valid_cols].div(cross[valid_cols].sum(axis=1), axis=0) * 100
print(pct.round(1).to_string())


# ----------------------------- 2) Recode to groups -----------------------
# Per spec, collapse atheist (3) into not_religious (2) since n_atheist < 100
# in every wave. Confirm thresholds.
n_atheist_max = int(cross.get("code_3", pd.Series([0])).max())
print(f"\nMax atheist (code 3) count across waves: {n_atheist_max}")
print(f"  → < 100 in every wave: COLLAPSING atheist into not_religious")

def rel_group(v):
    if pd.isna(v):
        return np.nan
    if v == 1: return "religious"
    if v in (2, 3): return "not_religious"
    return np.nan
df["rel_group"] = df["rel_person"].apply(rel_group)


# ----------------------------- 3) Means + gap per cell -------------------
rows = []
for w in WAVES:
    for g in ("religious", "not_religious"):
        sub = df[(df["wave"] == w) & (df["rel_group"] == g)]
        n = len(sub)
        mil = sub["conf_military"].mean()
        pol = sub["conf_police"].mean()
        crt = sub["conf_courts"].mean() if sub["conf_courts"].notna().any() else np.nan
        rows.append({
            "wave": w, "year": YEARS[w], "rel_group": g, "n": n,
            "conf_military": round(mil, 4),
            "conf_police":   round(pol, 4),
            "conf_courts":   (round(crt, 4) if pd.notna(crt) else np.nan),
            "army_police_gap": round(mil - pol, 4),
        })
out = pd.DataFrame(rows)
out.to_csv(os.path.join(RESULTS, "layer1_by_relperson.csv"), index=False)
print(f"\nSaved results/layer1_by_relperson.csv ({len(out)} rows)")

print("\n" + "=" * 78)
print("Mean confidence by (wave × rel_group)")
print("=" * 78)
fmt = "{:<5} {:<14} {:>5} {:>9} {:>9} {:>9} {:>9}"
print(fmt.format("wave","group","n","army","police","courts","a-p gap"))
print("-" * 65)
for _, r in out.iterrows():
    crt = f"{r['conf_courts']:.3f}" if pd.notna(r["conf_courts"]) else "  —  "
    print(fmt.format(r["wave"], r["rel_group"], int(r["n"]),
                     f"{r['conf_military']:.3f}",
                     f"{r['conf_police']:.3f}",
                     crt,
                     f"{r['army_police_gap']:+.3f}"))
    if r["rel_group"] == "not_religious":
        print()


# ----------------------------- 4) Gap table ------------------------------
print("\n" + "=" * 78)
print("army-police gap by (wave × rel_group)")
print("=" * 78)
gap_wide = out.pivot(index="wave", columns="rel_group",
                     values="army_police_gap")[["religious","not_religious"]]
gap_wide["religious - not_religious"] = (gap_wide["religious"]
                                         - gap_wide["not_religious"]).round(4)
print(gap_wide.to_string())
