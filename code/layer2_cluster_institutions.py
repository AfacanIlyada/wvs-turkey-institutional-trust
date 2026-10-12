"""
Layer 2: how the army / police / courts internal ordering shifts across
waves within each trust cluster, plus a WV7 measurement-regime flag.

Four sub-analyses (per the brief):
  1) cluster × wave × institution means + ranks + spread + army-police gap
  2) flip detection across consecutive waves
  3) within-cluster spread trajectory + WV2-vs-WV6 t-test
  4) army-police gap × cluster bridge table (vs Layer 1)
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")
WAVES = ["WV2","WV3","WV4","WV5","WV6","WV7"]
YEARS = {"WV2":1990,"WV3":1996,"WV4":2001,"WV5":2007,"WV6":2011,"WV7":2018}
CLUSTERS = [0, 1, 2]
CLUSTER_NAME = {0:"Distrusters", 1:"Selective trusters", 2:"Generalised trusters"}
INST_COLS = ["conf_military","conf_police","conf_courts"]
INST_SHORT = {"conf_military":"army","conf_police":"police","conf_courts":"courts"}

df = pd.read_csv(os.path.join(RESULTS, "pooled_extended_v2.csv"))
df = df.dropna(subset=["cluster"]).copy()
df["cluster"] = df["cluster"].astype(int)
df["wv7_flag"] = (df["wave"] == "WV7").astype(int)
print(f"After dropping cluster-NaN rows: {df.shape}")


# =========================================================================
# 1) cluster × wave × institution means + ranks + spread + gap
# =========================================================================
rows = []
for c in CLUSTERS:
    for w in WAVES:
        sub = df[(df["cluster"] == c) & (df["wave"] == w)]
        means = {col: sub[col].mean() for col in INST_COLS}
        # available (non-NaN) institutions
        avail = {k: v for k, v in means.items() if not np.isnan(v)}
        # rank within available items: higher mean = rank 1
        sorted_inst = sorted(avail.items(), key=lambda kv: -kv[1])
        ranks = {col: ("MISSING" if np.isnan(means[col]) else None)
                 for col in INST_COLS}
        for rank, (col, _) in enumerate(sorted_inst, start=1):
            ranks[col] = rank
        # spread
        if len(avail) >= 2:
            spread = max(avail.values()) - min(avail.values())
        else:
            spread = np.nan
        gap = means["conf_military"] - means["conf_police"]
        rows.append({
            "cluster": c, "cluster_name": CLUSTER_NAME[c],
            "wave": w, "year": YEARS[w],
            "n": len(sub),
            "conf_military_mean": round(means["conf_military"], 4),
            "conf_police_mean":   round(means["conf_police"], 4),
            "conf_courts_mean":  (round(means["conf_courts"], 4)
                                  if not np.isnan(means["conf_courts"]) else np.nan),
            "army_rank":   ranks["conf_military"],
            "police_rank": ranks["conf_police"],
            "courts_rank": ranks["conf_courts"],
            "spread":      (round(spread, 4) if not np.isnan(spread) else np.nan),
            "army_police_gap": round(gap, 4),
            "wv7_flag":    1 if w == "WV7" else 0,
        })
cwi = pd.DataFrame(rows)
cwi.to_csv(os.path.join(RESULTS, "layer2_cluster_wave_institution.csv"),
           index=False)
print("\n=== Analysis 1: cluster × wave × institution ===")
print(cwi.to_string(index=False))


# =========================================================================
# 2) Flip detection — rank changes across consecutive waves within cluster
# =========================================================================
flip_rows = []
print("\n\n=== Analysis 2: rank flips between consecutive waves ===")
for c in CLUSTERS:
    cl = cwi[cwi["cluster"] == c].sort_values("wave").reset_index(drop=True)
    for i in range(len(cl) - 1):
        a, b = cl.iloc[i], cl.iloc[i + 1]
        # Determine which institutions are available in BOTH waves
        common = []
        for col_short in ("army","police","courts"):
            r_a = a[f"{col_short}_rank"]
            r_b = b[f"{col_short}_rank"]
            if r_a != "MISSING" and r_b != "MISSING":
                common.append((col_short, r_a, r_b))
        # Among common institutions, has the relative ordering changed?
        # Re-rank within the subset to see if ordering of *common* items
        # differs across waves.
        a_inst = [(name, a[f"{name}_mean" if name=="conf_courts" else
                             {"army":"conf_military_mean",
                              "police":"conf_police_mean",
                              "courts":"conf_courts_mean"}[name]])
                  for name, _, _ in common]
        # Simpler: compare full rank tuples for the common items
        order_a = tuple(name for name, _, _ in
                        sorted([(n, ra, rb) for n, ra, rb in common],
                               key=lambda x: x[1]))
        order_b = tuple(name for name, _, _ in
                        sorted([(n, ra, rb) for n, ra, rb in common],
                               key=lambda x: x[2]))
        changed = order_a != order_b
        # describe the change
        if changed:
            desc = f"{a['wave']} order [{' > '.join(order_a)}]  ->  " \
                   f"{b['wave']} order [{' > '.join(order_b)}]"
        else:
            desc = f"ordering stable: [{' > '.join(order_a)}]"
        involves_wv7 = (a["wave"] == "WV7") or (b["wave"] == "WV7")
        robust = "WV7-flagged" if involves_wv7 else "robust (WV2-WV6)"
        flip_rows.append({
            "cluster": c, "cluster_name": CLUSTER_NAME[c],
            "wave_pair": f"{a['wave']}->{b['wave']}",
            "changed": changed,
            "what_changed": desc,
            "involves_wv7": int(involves_wv7),
            "regime": robust,
        })

flips = pd.DataFrame(flip_rows)
flips.to_csv(os.path.join(RESULTS, "layer2_flip_events.csv"), index=False)
print("\nAll consecutive wave-pairs (changed or stable):")
print(flips[["cluster","cluster_name","wave_pair","changed","regime",
             "what_changed"]].to_string(index=False))

print("\n--- Flips only (rank ordering changed) ---")
fonly = flips[flips["changed"]]
if fonly.empty:
    print("  (none)")
else:
    for _, r in fonly.iterrows():
        marker = "  ⚠ WV7 caveat" if r["involves_wv7"] else "  ✓ robust"
        print(f"  c{r['cluster']} {r['cluster_name']:<20} "
              f"{r['wave_pair']:<12} {r['what_changed']}{marker}")


# =========================================================================
# 3) Within-cluster institution spread trajectory + WV2 vs WV6 t-test
# =========================================================================
# Individual-level spread: per respondent, compute max(conf_*)-min(conf_*)
# across whichever of military/police/courts they answered.
def row_spread(row):
    vals = [row["conf_military"], row["conf_police"], row["conf_courts"]]
    vals = [v for v in vals if not pd.isna(v)]
    if len(vals) < 2:
        return np.nan
    return max(vals) - min(vals)

df["spread_indiv"] = df.apply(row_spread, axis=1)

print("\n\n=== Analysis 3: within-cluster institution spread over time ===")
print("(mean of individual-level max(conf)-min(conf) across army/police/courts)\n")
spread_rows = []
for c in CLUSTERS:
    print(f"\n-- Cluster {c} ({CLUSTER_NAME[c]}) --")
    print(f"{'wave':<6} {'n':>5}  {'mean_spread':>12}  bar")
    for w in WAVES:
        sub = df[(df["cluster"] == c) & (df["wave"] == w)]
        s = sub["spread_indiv"].dropna()
        if len(s) == 0:
            spread_rows.append({"cluster": c, "cluster_name": CLUSTER_NAME[c],
                                "wave": w, "year": YEARS[w], "n": 0,
                                "mean_spread": np.nan, "sd": np.nan})
            continue
        mn, sd = float(s.mean()), float(s.std(ddof=1))
        spread_rows.append({"cluster": c, "cluster_name": CLUSTER_NAME[c],
                            "wave": w, "year": YEARS[w], "n": len(s),
                            "mean_spread": round(mn, 4),
                            "sd": round(sd, 4)})
        bar = "█" * int(mn * 30)
        print(f"  {w:<4} {len(s):>5}  {mn:>10.3f}    {bar}")

    # WV2 vs WV6 t-test within this cluster
    a = df[(df["cluster"]==c) & (df["wave"]=="WV2")]["spread_indiv"].dropna()
    b = df[(df["cluster"]==c) & (df["wave"]=="WV6")]["spread_indiv"].dropna()
    if len(a) > 1 and len(b) > 1:
        t, p = stats.ttest_ind(a, b, equal_var=False)
        direction = "narrowed" if b.mean() < a.mean() else "widened"
        print(f"  WV2(mean={a.mean():.3f},n={len(a)}) vs "
              f"WV6(mean={b.mean():.3f},n={len(b)}): "
              f"t={t:.3f}  p={p:.3e}  ({direction})")

spread = pd.DataFrame(spread_rows)
spread.to_csv(os.path.join(RESULTS, "layer2_spread_trajectory.csv"),
              index=False)


# =========================================================================
# 4) Army-police gap × cluster bridge table
# =========================================================================
print("\n\n=== Analysis 4: army-police gap × cluster (Layer-1 bridge) ===")
bridge = cwi.pivot(index="wave", columns="cluster",
                   values="army_police_gap").reindex(WAVES)
bridge.columns = [f"cluster{c}_gap" for c in bridge.columns]
# Add aggregate (all-cluster) gap from cwi-weighted means
agg = (df.groupby("wave")
         .apply(lambda d: d["conf_military"].mean() - d["conf_police"].mean())
         .reindex(WAVES).round(4))
bridge["aggregate_gap"] = agg
bridge["year"] = [YEARS[w] for w in bridge.index]
print(bridge[["year","cluster0_gap","cluster1_gap","cluster2_gap",
              "aggregate_gap"]].to_string())

# WV6 - WV2 changes per cluster
print("\nWV2 -> WV6 change per cluster (robust window):")
for c in CLUSTERS:
    a = cwi[(cwi["cluster"]==c) & (cwi["wave"]=="WV2")]["army_police_gap"].iloc[0]
    b = cwi[(cwi["cluster"]==c) & (cwi["wave"]=="WV6")]["army_police_gap"].iloc[0]
    print(f"  cluster {c} ({CLUSTER_NAME[c]:<22}): "
          f"{a:+.3f}  ->  {b:+.3f}   Δ = {b-a:+.3f}")

print("\nFiles written:")
for f in ["layer2_cluster_wave_institution.csv",
          "layer2_flip_events.csv",
          "layer2_spread_trajectory.csv"]:
    print(f"  results/{f}")
