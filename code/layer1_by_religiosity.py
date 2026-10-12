"""
Layer-1 by religiosity tertile.

Religiosity tertile is computed per wave on rel_importance_god (1-10
'Importance of God in life'), via pd.qcut with q=3. Ties at integer
boundaries are handled with duplicates='drop'.

Reports mean institutional confidence by (wave, rel_tertile) and asks:
does the army-police gap collapse symmetrically across tertiles, or is
it driven by the high-religiosity group?
"""
import os
import numpy as np
import pandas as pd

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")
WAVES = ["WV2","WV3","WV4","WV5","WV6","WV7"]
YEARS = {"WV2":1990,"WV3":1996,"WV4":2001,"WV5":2007,"WV6":2011,"WV7":2018}

df = pd.read_csv(os.path.join(RESULTS, "pooled_extended_v2.csv"))
print(f"Loaded: {df.shape}")

# --- Build religiosity grouping ------------------------------------------
# Fixed substantive cuts on rel_importance_god (1-10):
#   low  = 1-7  (importance below ceiling-cluster)
#   mid  = 8-9  (high but not maxed)
#   high = 10   (ceiling group)
# Chosen because the 1/3 and 2/3 quantiles both land at 10 in WV2-WV6 due
# to a 67-81% supermajority answering 10, which makes quantile tertiles
# uninformative. These cuts isolate the substantive "ceiling" group.
def rel_group(v):
    if pd.isna(v):       return np.nan
    if v <= 7:           return "low"
    if v <= 9:           return "mid"
    if v == 10:          return "high"
    return np.nan
df["rel_tertile"] = df["rel_importance_god"].apply(rel_group)

print("\nrel_tertile counts per wave (fixed cuts 1-7 / 8-9 / 10):")
print(df.groupby("wave")["rel_tertile"]
        .value_counts(dropna=False).unstack(fill_value=0)
        [["low","mid","high"]].to_string())


# --- Mean institutional confidence by (wave, rel_tertile) ----------------
rows = []
TERTILE_ORDER = ["low", "mid", "high"]
for w in WAVES:
    for t in TERTILE_ORDER:
        sub = df[(df["wave"] == w) & (df["rel_tertile"] == t)]
        n = len(sub)
        row = {"wave": w, "year": YEARS[w], "rel_tertile": t, "n": n}
        for c in ["conf_military", "conf_police", "conf_courts"]:
            row[c] = round(sub[c].mean(), 4) if sub[c].notna().any() \
                     else np.nan
        rows.append(row)
out = pd.DataFrame(rows)
out.to_csv(os.path.join(RESULTS, "layer1_by_religiosity.csv"), index=False)
print(f"\nSaved results/layer1_by_religiosity.csv ({len(out)} rows)")


# --- Side-by-side table per wave: low vs high --------------------------
print("\n=== Mean confidence by (wave × religiosity tertile) ===")
print("Higher value = more confidence (1-4 scale)\n")
fmt = "{:<5} {:<5} {:>5} {:>9} {:>9} {:>9}"
print(fmt.format("wave","tert","n","army","police","courts"))
print("-" * 50)
for _, r in out.iterrows():
    crt = f"{r['conf_courts']:.3f}" if pd.notna(r["conf_courts"]) else "  —  "
    print(fmt.format(
        r["wave"], r["rel_tertile"], int(r["n"]),
        f"{r['conf_military']:.3f}",
        f"{r['conf_police']:.3f}",
        crt))
    if r["rel_tertile"] == "high":
        print()  # blank line between waves


# --- Key question: army-police gap by tertile across waves -------------
print("\n=== army-police gap by religiosity tertile ===")
gap = out.copy()
gap["army_police_gap"] = (gap["conf_military"] - gap["conf_police"]).round(4)
gap_wide = gap.pivot(index="wave", columns="rel_tertile",
                     values="army_police_gap")[TERTILE_ORDER]
gap_wide["spread (high-low)"] = (gap_wide["high"] - gap_wide["low"]).round(4)
print(gap_wide.to_string())

print("\n=== police mean by tertile (asks: did high-rel pull TOWARD police?) ===")
police_wide = out.pivot(index="wave", columns="rel_tertile",
                        values="conf_police")[TERTILE_ORDER]
police_wide["high - low"] = (police_wide["high"] - police_wide["low"]).round(4)
print(police_wide.round(3).to_string())

print("\n=== army mean by tertile (asks: did high-rel pull AWAY from army?) ===")
army_wide = out.pivot(index="wave", columns="rel_tertile",
                      values="conf_military")[TERTILE_ORDER]
army_wide["high - low"] = (army_wide["high"] - army_wide["low"]).round(4)
print(army_wide.round(3).to_string())
