"""
Latent trust-orientation typology via per-wave K-means clustering,
WVS Turkey waves 2-7.

Pipeline:
  1) Extract all 14 confidence items + national_pride + life_satisfaction
     for waves where they exist; per-(item, wave) min-max normalize to 0-1.
  2) Drop respondents missing >30% of available trust items in their wave.
  3) Per-wave: K-means k=2..5, elbow (WCSS) + silhouette; save elbow PNGs.
  4) Default k=3 for substantive analysis (matched across waves for
     consistent labels via Hungarian assignment vs a reference wave).
  5) Per-wave: cluster centroid profile (trust items) + sociodemographic
     profile (age, female, education, religiosity, gender egal,
     national pride, life satisfaction).
  6) Radar plot per wave; stacked-bar composition over time.
"""
import os, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.optimize import linear_sum_assignment

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
warnings.filterwarnings("ignore", category=FutureWarning)

FOLDER  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(FOLDER, "results")

WAVES = ["WV2", "WV3", "WV4", "WV5", "WV6", "WV7"]
YEARS = {"WV2":1990,"WV3":1996,"WV4":2001,"WV5":2007,"WV6":2011,"WV7":2018}
FILES = {
    "WV2": "F00008272-WV2_Data_Turkey_Excel_v1.6.1.xlsx",
    "WV3": "F00008135-WV3_Data_Turkey_Excel_v20221107.1.xlsx",
    "WV4": "F00008022-WV4_Data_Turkey_Excel_v20201117.1.xlsx",
    "WV5": "F00007873-WV5_Data_Turkey_Excel_v20201117.1.xlsx",
    "WV6": "F00007629-WV6_Data_Turkey_2011_Excel_v20180912.xlsx",
    "WV7": "F00013222-WVS_Wave_7_Turkey_Excel_v5.1.xlsx",
}

# 14 confidence items; 4 are already in pooled (relig, govt, parl, mil).
# "" = not asked in that wave.
TRUST_ALL = {
    "conf_religious":    {"WV2":"V272","WV3":"V135","WV4":"V147","WV5":"V131","WV6":"V108","WV7":"Q64"},
    "conf_military":     {"WV2":"V273","WV3":"V136","WV4":"V148","WV5":"V132","WV6":"V109","WV7":"Q65"},
    "conf_press":        {"WV2":"V276","WV3":"V138","WV4":"V149","WV5":"V133","WV6":"V110","WV7":"Q66"},
    "conf_tv":           {"WV2":"",    "WV3":"V139","WV4":"V150","WV5":"V134","WV6":"V111","WV7":"Q67"},
    "conf_unions":       {"WV2":"V277","WV3":"V140","WV4":"V151","WV5":"V135","WV6":"V112","WV7":"Q68"},
    "conf_police":       {"WV2":"V278","WV3":"V141","WV4":"V152","WV5":"V136","WV6":"V113","WV7":"Q69"},
    "conf_courts":       {"WV2":"V275","WV3":"V137","WV4":"",    "WV5":"V137","WV6":"V114","WV7":"Q70"},
    "conf_government":   {"WV2":"V289","WV3":"V142","WV4":"V153","WV5":"V138","WV6":"V115","WV7":"Q71"},
    "conf_parties":      {"WV2":"",    "WV3":"V143","WV4":"V154","WV5":"V139","WV6":"V116","WV7":"Q72"},
    "conf_parliament":   {"WV2":"V279","WV3":"V144","WV4":"V155","WV5":"V140","WV6":"V117","WV7":"Q73"},
    "conf_civilservice": {"WV2":"V280","WV3":"V145","WV4":"V156","WV5":"V141","WV6":"V118","WV7":"Q74"},
    "conf_companies":    {"WV2":"V281","WV3":"V146","WV4":"V157","WV5":"V142","WV6":"V120","WV7":"Q77"},
    "conf_un":           {"WV2":"",    "WV3":"V150","WV4":"V162","WV5":"V147","WV6":"V126","WV7":"Q83"},
    "conf_eu":           {"WV2":"V283B","WV3":"V149_00","WV4":"","WV5":"V146_00","WV6":"V125_00","WV7":"Q82_EU"},
}
TRUST_ITEMS = list(TRUST_ALL.keys())

# Additional sociodemographic items for cluster profiling
EXTRA = {
    "national_pride":    {"WV2":"V322","WV3":"V205","WV4":"V216","WV5":"V209","WV6":"V211","WV7":"Q254"},
    "life_satisfaction": {"WV2":"V96", "WV3":"V65", "WV4":"V81", "WV5":"V22", "WV6":"V23", "WV7":"Q49"},
}


def load_wave_columns(wave, fn, crosswalk):
    path = os.path.join(FOLDER, fn)
    raw = pd.read_excel(path, nrows=0)
    code_to_full = {}
    for full in raw.columns:
        s = str(full).strip()
        code = s.split(":", 1)[0].strip() if ":" in s else s
        code_to_full[code] = full
    wanted_full, wanted_concept = [], []
    for concept, mapping in crosswalk.items():
        code = mapping.get(wave, "")
        if code and code in code_to_full:
            wanted_full.append(code_to_full[code])
            wanted_concept.append(concept)
    if not wanted_full:
        return pd.DataFrame({c: np.nan for c in crosswalk},
                            index=range(len(pd.read_excel(path, usecols=[0]))))
    df = pd.read_excel(path, usecols=wanted_full)
    df = df.rename(columns=dict(zip(wanted_full, wanted_concept)))
    for c in crosswalk:
        if c not in df.columns:
            df[c] = np.nan
    return df[list(crosswalk.keys())]


# =====================================================================
# 1) Load + extract everything we need
# =====================================================================
pooled = pd.read_csv(os.path.join(RESULTS, "pooled_all_scales.csv"))
print(f"Loaded pooled_all_scales.csv: {len(pooled):,} rows")

# Trust items: existing 4 are already in pooled on 1-4 scale (reverse-coded
# so higher = more confidence). For the other 10 plus the 2 extras, we
# re-extract from source so they have the same recoding and direction.
print("\nExtracting additional trust + extra items per wave...")
all_extra = {**TRUST_ALL, **EXTRA}
frames = []
for w in WAVES:
    sub = load_wave_columns(w, FILES[w], all_extra)
    sub["_wave"] = w
    frames.append(sub)
addn = pd.concat(frames, ignore_index=True)
assert len(addn) == len(pooled)
assert (addn["_wave"].values == pooled["wave"].values).all()
addn = addn.drop(columns=["_wave"])

# Recode: drop negatives → NaN, restrict to valid range, reverse confidence
RAW = {}
for c in TRUST_ITEMS:
    v = pd.to_numeric(addn[c], errors="coerce")
    v[v < 0] = np.nan
    v[~v.isin([1, 2, 3, 4])] = np.nan
    RAW[c] = 5 - v                  # 1=Great→4, 4=None→1  (higher=more conf)
# national pride: 1=Very proud .. 4=Not at all → reverse so higher=more proud
v = pd.to_numeric(addn["national_pride"], errors="coerce"); v[v < 0] = np.nan
v[~v.isin([1,2,3,4])] = np.nan
RAW["national_pride"] = 5 - v
# life satisfaction: 1=Dissatisfied .. 10=Satisfied (no reverse)
v = pd.to_numeric(addn["life_satisfaction"], errors="coerce"); v[v < 0] = np.nan
v[~v.between(1, 10)] = np.nan
RAW["life_satisfaction"] = v

# Overwrite the trust items in pooled with the freshly recoded raw values
for c in TRUST_ITEMS:
    pooled[c] = RAW[c].values
pooled["national_pride"]    = RAW["national_pride"].values
pooled["life_satisfaction"] = RAW["life_satisfaction"].values

# Per-(item, wave) min-max normalize the trust items to 0-1
print("Normalizing trust items per (item, wave) to 0-1...")
for c in TRUST_ITEMS:
    cn = c + "_z"
    pooled[cn] = np.nan
    for w in WAVES:
        m = pooled["wave"] == w
        s = pooled.loc[m, c]
        valid = s.dropna()
        if len(valid) == 0 or valid.min() == valid.max():
            continue
        pooled.loc[m, cn] = (s - valid.min()) / (valid.max() - valid.min())
Z_ITEMS = [c + "_z" for c in TRUST_ITEMS]


# =====================================================================
# 2) Per-wave: drop respondents missing >30% of available items
# =====================================================================
print("\n--- Items available per wave (after extraction) ---")
avail_items = {}
for w in WAVES:
    sub = pooled[pooled["wave"] == w]
    items_w = [c for c in TRUST_ITEMS if sub[c].notna().sum() > 0]
    avail_items[w] = items_w
    print(f"  {w} ({YEARS[w]}): {len(items_w):>2} items — "
          f"{[c.replace('conf_','') for c in items_w]}")

# Drop respondents with >30% missing among their wave's items
keep_mask = pd.Series(False, index=pooled.index)
for w in WAVES:
    items_w_z = [c + "_z" for c in avail_items[w]]
    sub = pooled[pooled["wave"] == w]
    frac_missing = sub[items_w_z].isna().mean(axis=1)
    keep_mask.loc[sub.index] = frac_missing <= 0.30
pooled_clu = pooled[keep_mask].copy()
print(f"\nDropped {(~keep_mask).sum():,} respondents (>30% trust missing). "
      f"Kept {len(pooled_clu):,} / {len(pooled):,}.")
print("Kept per wave:",
      pooled_clu.groupby("wave").size().reindex(WAVES).to_dict())


# =====================================================================
# 3) Elbow + silhouette per wave for k=2..5
# =====================================================================
print("\n" + "=" * 70)
print("Per-wave elbow + silhouette (k = 2..5)")
print("=" * 70)
elbow_rows = []
for w in WAVES:
    sub  = pooled_clu[pooled_clu["wave"] == w].copy()
    z_w  = [c + "_z" for c in avail_items[w]]
    X    = sub[z_w].copy()
    # Mean-impute remaining missings within wave
    X    = X.fillna(X.mean())
    Xv   = X.values
    print(f"\n{w} ({YEARS[w]}): n={len(Xv)}, p={Xv.shape[1]}")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    ks  = list(range(2, 6))
    wcss, sils = [], []
    for k in ks:
        km = KMeans(n_clusters=k, n_init=20, random_state=42)
        labels = km.fit_predict(Xv)
        wcss.append(km.inertia_)
        # silhouette can be slow; subsample to 2000 if larger
        if len(Xv) > 2000:
            rng = np.random.default_rng(42)
            idx = rng.choice(len(Xv), 2000, replace=False)
            sil = silhouette_score(Xv[idx], labels[idx])
        else:
            sil = silhouette_score(Xv, labels)
        sils.append(sil)
        elbow_rows.append({"wave": w, "year": YEARS[w], "k": k,
                           "n": len(Xv), "wcss": round(km.inertia_, 3),
                           "silhouette": round(sil, 4)})
        print(f"  k={k}:  WCSS={km.inertia_:>8.2f}   sil={sil:+.4f}")

    axes[0].plot(ks, wcss, "o-"); axes[0].set_title(f"{w} ({YEARS[w]}) — WCSS")
    axes[0].set_xlabel("k"); axes[0].set_ylabel("inertia"); axes[0].grid(alpha=0.3)
    axes[1].plot(ks, sils, "o-", color="tab:orange")
    axes[1].set_title(f"{w} ({YEARS[w]}) — silhouette")
    axes[1].set_xlabel("k"); axes[1].set_ylabel("score"); axes[1].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS, f"cluster_elbow_{w}.png"),
                dpi=140, bbox_inches="tight")
    plt.close(fig)
elbow_df = pd.DataFrame(elbow_rows)
elbow_df.to_csv(os.path.join(RESULTS, "cluster_elbow.csv"), index=False)


# =====================================================================
# 4) Fit final k=3 per wave; assign clusters
# =====================================================================
K_FINAL = 3
print(f"\nUsing k={K_FINAL} per wave for substantive clustering.")

cluster_centroids = {}     # wave -> DataFrame (k x items_w)
cluster_labels    = {}     # wave -> pd.Series of cluster id aligned to pooled_clu indices
for w in WAVES:
    sub = pooled_clu[pooled_clu["wave"] == w].copy()
    z_w = [c + "_z" for c in avail_items[w]]
    X = sub[z_w].fillna(sub[z_w].mean()).values
    km = KMeans(n_clusters=K_FINAL, n_init=30, random_state=42)
    raw_labels = km.fit_predict(X)
    centroids = pd.DataFrame(km.cluster_centers_,
                             columns=avail_items[w])
    cluster_centroids[w] = centroids
    cluster_labels[w] = pd.Series(raw_labels, index=sub.index, name="cluster_raw")


# =====================================================================
# 4b) Cross-wave cluster matching via Hungarian assignment
# Reference = WV4 (largest sample); match on items present in both.
# Always-present items = intersection of all six wave item lists.
# =====================================================================
ALWAYS = sorted(set.intersection(*[set(v) for v in avail_items.values()]))
print(f"\nItems present in all 6 waves (used for cross-wave matching): "
      f"{len(ALWAYS)} → {[c.replace('conf_','') for c in ALWAYS]}")

REF = "WV4"
ref_cents = cluster_centroids[REF][ALWAYS].values    # k × p_shared
# Order the reference clusters by mean trust (low → high)
ref_order = np.argsort(ref_cents.mean(axis=1))
ref_cents = ref_cents[ref_order]                     # reorder reference
# Rebuild cluster_labels for WV4 so id 0=low-trust, k-1=high-trust
remap_ref = {old: new for new, old in enumerate(ref_order)}
cluster_labels[REF] = cluster_labels[REF].map(remap_ref)
cluster_centroids[REF] = (cluster_centroids[REF]
                          .iloc[ref_order].reset_index(drop=True))

# Match other waves to the reference via Hungarian on ALWAYS items
canonical_labels = {REF: cluster_labels[REF]}
for w in WAVES:
    if w == REF:
        continue
    cents = cluster_centroids[w][ALWAYS].values
    # cost matrix [i, j] = distance(other_i, ref_j)
    cost = np.zeros((K_FINAL, K_FINAL))
    for i in range(K_FINAL):
        for j in range(K_FINAL):
            cost[i, j] = np.linalg.norm(cents[i] - ref_cents[j])
    row_ind, col_ind = linear_sum_assignment(cost)
    # row_ind[i] is the wave's cluster id; col_ind[i] is the matched ref id
    remap = {row_ind[i]: col_ind[i] for i in range(K_FINAL)}
    canonical_labels[w] = cluster_labels[w].map(remap)
    # also reorder centroids df rows for printing
    inv = {v: k for k, v in remap.items()}
    cluster_centroids[w] = (cluster_centroids[w]
                            .iloc[[inv[i] for i in range(K_FINAL)]]
                            .reset_index(drop=True))

# Attach canonical cluster label to pooled_clu
pooled_clu["cluster"] = np.nan
for w in WAVES:
    pooled_clu.loc[canonical_labels[w].index, "cluster"] = canonical_labels[w].values
pooled_clu["cluster"] = pooled_clu["cluster"].astype(int)


# =====================================================================
# 5) Centroid profiles per wave (trust items) — also save per-wave CSV
# =====================================================================
print("\n" + "=" * 70)
print("Cluster centroid profiles (trust items)")
print("=" * 70)
CLUSTER_NAMES = {0: "Distrusters", 1: "Selective trusters", 2: "Generalised trusters"}
all_profiles = []
for w in WAVES:
    sub  = pooled_clu[pooled_clu["wave"] == w]
    items_w = avail_items[w]
    rows = []
    for k in range(K_FINAL):
        cl = sub[sub["cluster"] == k]
        row = {"cluster": k, "cluster_name": CLUSTER_NAMES[k],
               "n": len(cl), "pct": round(100 * len(cl) / len(sub), 1)}
        for it in TRUST_ITEMS:
            row[it] = round(cl[it].mean(), 3) if it in items_w else np.nan
        rows.append(row)
        all_profiles.append({**row, "wave": w, "year": YEARS[w]})
    prof = pd.DataFrame(rows)
    prof.to_csv(os.path.join(RESULTS, f"cluster_profiles_{w}.csv"), index=False)
    print(f"\n--- {w} ({YEARS[w]}), n={len(sub):,} ---")
    print(prof.set_index("cluster_name")
              [["n","pct"] + [c for c in TRUST_ITEMS if c in items_w]]
              .to_string())
pd.DataFrame(all_profiles).to_csv(
    os.path.join(RESULTS, "cluster_profiles_all.csv"), index=False)


# =====================================================================
# 6) Sociodemographic profiles
# =====================================================================
SOCIO = ["age", "female", "education", "religiosity_scale",
         "gender_egal_scale", "national_pride", "life_satisfaction"]
print("\n" + "=" * 70)
print("Sociodemographic profile of each cluster per wave")
print("=" * 70)
socio_rows = []
for w in WAVES:
    sub = pooled_clu[pooled_clu["wave"] == w]
    for k in range(K_FINAL):
        cl = sub[sub["cluster"] == k]
        row = {"wave": w, "year": YEARS[w], "cluster": k,
               "cluster_name": CLUSTER_NAMES[k], "n": len(cl),
               "pct": round(100 * len(cl) / len(sub), 1)}
        for v in SOCIO:
            if v in cl.columns:
                row[v + "_mean"] = round(cl[v].mean(), 3)
        socio_rows.append(row)
socio_df = pd.DataFrame(socio_rows)
socio_df.to_csv(
    os.path.join(RESULTS, "cluster_sociodemographic_profiles.csv"), index=False)
print(socio_df.to_string(index=False))


# =====================================================================
# 7) Radar charts per wave
# =====================================================================
print("\nPlotting radar charts per wave...")
RADAR_COLORS = {0: "#d62728", 1: "#ff7f0e", 2: "#2ca02c"}     # red / orange / green
for w in WAVES:
    items_w = avail_items[w]
    cats = [c.replace("conf_", "") for c in items_w]
    n_cat = len(cats)
    angles = np.linspace(0, 2*np.pi, n_cat, endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(7.5, 7.5), subplot_kw=dict(polar=True))
    for k in range(K_FINAL):
        vals = cluster_centroids[w].iloc[k][items_w].values.tolist()
        vals += vals[:1]
        cl_n = (pooled_clu[(pooled_clu["wave"]==w) &
                           (pooled_clu["cluster"]==k)].shape[0])
        pct = 100 * cl_n / pooled_clu[pooled_clu["wave"]==w].shape[0]
        ax.plot(angles, vals, "o-", linewidth=2,
                color=RADAR_COLORS[k],
                label=f"{CLUSTER_NAMES[k]} (n={cl_n}, {pct:.0f}%)")
        ax.fill(angles, vals, alpha=0.12, color=RADAR_COLORS[k])
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(cats, fontsize=8)
    ax.set_ylim(0, 1); ax.set_rgrids([0.25, 0.5, 0.75], angle=0, fontsize=7)
    ax.set_title(f"Trust profile centroids — {w} ({YEARS[w]})", y=1.08)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.18), fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS, f"cluster_radar_{w}.png"),
                dpi=140, bbox_inches="tight")
    plt.close(fig)


# =====================================================================
# 8) Stacked-bar cluster composition over time (consistent colors)
# =====================================================================
comp_rows = []
for w in WAVES:
    sub = pooled_clu[pooled_clu["wave"] == w]
    n   = len(sub)
    for k in range(K_FINAL):
        comp_rows.append({"wave": w, "year": YEARS[w], "cluster": k,
                          "cluster_name": CLUSTER_NAMES[k],
                          "n": int((sub["cluster"] == k).sum()),
                          "pct": 100 * (sub["cluster"] == k).sum() / n})
comp = pd.DataFrame(comp_rows)
comp.to_csv(os.path.join(RESULTS, "cluster_composition.csv"), index=False)
print("\n=== Cluster composition (% of sample) per wave ===")
print(comp.pivot(index="wave", columns="cluster_name", values="pct")
          .round(1).to_string())

# Stacked-bar
fig, ax = plt.subplots(figsize=(9, 5.5))
bottoms = np.zeros(len(WAVES))
xs = [YEARS[w] for w in WAVES]
for k in range(K_FINAL):
    heights = [comp[(comp["wave"]==w) & (comp["cluster"]==k)]["pct"].iloc[0]
               for w in WAVES]
    ax.bar(xs, heights, bottom=bottoms, width=2.5,
           color=RADAR_COLORS[k], label=CLUSTER_NAMES[k],
           edgecolor="white")
    for i, (x, h, b) in enumerate(zip(xs, heights, bottoms)):
        if h > 4:
            ax.text(x, b + h/2, f"{h:.0f}%", ha="center", va="center",
                    fontsize=9, color="white", fontweight="bold")
    bottoms += np.array(heights)
ax.set_xlabel("Year"); ax.set_ylabel("Share of sample (%)")
ax.set_ylim(0, 100); ax.set_xticks(xs)
ax.set_title("Trust-orientation cluster composition over time, Turkey (WVS 2-7)")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.20), ncol=K_FINAL)
fig.tight_layout()
fig.savefig(os.path.join(RESULTS, "cluster_composition_over_time.png"),
            dpi=140, bbox_inches="tight")
plt.close(fig)
print("\nSaved: cluster_composition_over_time.png")
print("\nAll outputs in results/")
