"""
Column inventory + ANOVA discrimination of pooled_all_scales.csv against
the trust-orientation cluster assignment.

Step A: reproduce per-respondent cluster labels from trust_clusters.py
        (the source CSV does not carry a cluster column).
Step B: column inventory -> column_inventory.csv
Step C: one-way ANOVA F/p vs cluster -> cluster_discrimination.csv
"""
import os
import warnings
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
from scipy.optimize import linear_sum_assignment

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
warnings.filterwarnings("ignore", category=FutureWarning)

FOLDER  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(FOLDER, "results")
OUT_DIR = FOLDER

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


# =========================================================================
# A) Reproduce cluster labels (mirror of trust_clusters.py logic)
# =========================================================================
pooled = pd.read_csv(os.path.join(RESULTS, "pooled_all_scales.csv"))
print(f"Loaded pooled_all_scales.csv: {pooled.shape}")

print("\nRe-extracting trust items per wave to attach cluster labels...")
frames = []
for w in WAVES:
    sub = load_wave_columns(w, FILES[w], TRUST_ALL)
    sub["_wave"] = w
    frames.append(sub)
addn = pd.concat(frames, ignore_index=True)
assert len(addn) == len(pooled)
assert (addn["_wave"].values == pooled["wave"].values).all()
addn = addn.drop(columns=["_wave"])

RAW = {}
for c in TRUST_ITEMS:
    v = pd.to_numeric(addn[c], errors="coerce")
    v[v < 0] = np.nan
    v[~v.isin([1, 2, 3, 4])] = np.nan
    RAW[c] = 5 - v
for c in TRUST_ITEMS:
    pooled[c] = RAW[c].values

# Per-(item, wave) min-max
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

avail_items = {}
for w in WAVES:
    sub = pooled[pooled["wave"] == w]
    avail_items[w] = [c for c in TRUST_ITEMS if sub[c].notna().sum() > 0]

keep_mask = pd.Series(False, index=pooled.index)
for w in WAVES:
    items_w_z = [c + "_z" for c in avail_items[w]]
    sub = pooled[pooled["wave"] == w]
    frac_missing = sub[items_w_z].isna().mean(axis=1)
    keep_mask.loc[sub.index] = frac_missing <= 0.30
pooled_clu = pooled[keep_mask].copy()
print(f"Kept {len(pooled_clu):,} / {len(pooled):,} respondents for clustering.")

K_FINAL = 3
cluster_centroids = {}
cluster_labels = {}
for w in WAVES:
    sub = pooled_clu[pooled_clu["wave"] == w].copy()
    z_w = [c + "_z" for c in avail_items[w]]
    X = sub[z_w].fillna(sub[z_w].mean()).values
    km = KMeans(n_clusters=K_FINAL, n_init=30, random_state=42)
    raw_labels = km.fit_predict(X)
    cluster_centroids[w] = pd.DataFrame(km.cluster_centers_, columns=avail_items[w])
    cluster_labels[w] = pd.Series(raw_labels, index=sub.index, name="cluster_raw")

ALWAYS = sorted(set.intersection(*[set(v) for v in avail_items.values()]))
REF = "WV4"
ref_cents = cluster_centroids[REF][ALWAYS].values
ref_order = np.argsort(ref_cents.mean(axis=1))
ref_cents = ref_cents[ref_order]
remap_ref = {old: new for new, old in enumerate(ref_order)}
cluster_labels[REF] = cluster_labels[REF].map(remap_ref)

canonical_labels = {REF: cluster_labels[REF]}
for w in WAVES:
    if w == REF:
        continue
    cents = cluster_centroids[w][ALWAYS].values
    cost = np.zeros((K_FINAL, K_FINAL))
    for i in range(K_FINAL):
        for j in range(K_FINAL):
            cost[i, j] = np.linalg.norm(cents[i] - ref_cents[j])
    row_ind, col_ind = linear_sum_assignment(cost)
    remap = {row_ind[i]: col_ind[i] for i in range(K_FINAL)}
    canonical_labels[w] = cluster_labels[w].map(remap)

# Attach cluster to ORIGINAL pooled (without the _z helper columns)
orig = pd.read_csv(os.path.join(RESULTS, "pooled_all_scales.csv"))
orig["cluster"] = np.nan
for w in WAVES:
    orig.loc[canonical_labels[w].index, "cluster"] = canonical_labels[w].values
# integer where present, NaN otherwise -> nullable Int
orig["cluster"] = orig["cluster"].astype("Int64")

print(f"\nCluster distribution (across all waves, respondents with label):")
print(orig["cluster"].value_counts(dropna=False).sort_index())

orig.to_csv(os.path.join(RESULTS, "pooled_with_clusters.csv"), index=False)
print(f"\nSaved results/pooled_with_clusters.csv")


# =========================================================================
# Step 1: shape + wave distribution
# =========================================================================
print("\n" + "=" * 70)
print("Step 1: shape + wave distribution")
print("=" * 70)
print(f"Shape: {orig.shape}")
print("\nWave value counts:")
print(orig["wave"].value_counts().sort_index())


# =========================================================================
# Step 2: per-column inventory
# =========================================================================
print("\n" + "=" * 70)
print("Step 2: building column inventory")
print("=" * 70)
n = len(orig)
inv_rows = []
for col in orig.columns:
    s = orig[col]
    dtype = str(s.dtype)
    pct_missing = round(100 * s.isna().mean(), 3)
    n_unique = int(s.nunique(dropna=True))
    is_numeric = pd.api.types.is_numeric_dtype(s)
    row = {
        "column": col,
        "dtype": dtype,
        "pct_missing": pct_missing,
        "n_unique": n_unique,
        "min": np.nan, "max": np.nan, "mean": np.nan,
        "top_values": "",
    }
    if is_numeric and n_unique > 0:
        row["min"]  = float(np.nanmin(s.values))
        row["max"]  = float(np.nanmax(s.values))
        row["mean"] = float(np.nanmean(s.values))
    if (not is_numeric) or n_unique <= 20:
        vc = s.value_counts(dropna=False).head(5)
        row["top_values"] = "; ".join(f"{k}={v}" for k, v in vc.items())
    inv_rows.append(row)

inv = pd.DataFrame(inv_rows)
inv.to_csv(os.path.join(OUT_DIR, "column_inventory.csv"), index=False)
print(f"Saved column_inventory.csv ({len(inv)} rows)")
print(inv.to_string(index=False))


# =========================================================================
# Step 3: ANOVA vs cluster (excluding scale composites, raw conf items,
# wave identifiers, cluster itself)
# =========================================================================
print("\n" + "=" * 70)
print("Step 3: one-way ANOVA against cluster")
print("=" * 70)

EXCLUDE_EXACT = {
    # wave identifiers
    "wave", "year",
    # scale composites
    "inst_trust_scale", "religiosity_scale", "gender_egal_scale",
    # cluster
    "cluster",
}
# Raw conf_ items used to build inst_trust (per user instruction: name pattern)
def is_excluded(col: str) -> bool:
    if col in EXCLUDE_EXACT:
        return True
    if col.startswith("conf_"):           # raw + normalized confidence items
        return True
    return False

with_label = orig.dropna(subset=["cluster"]).copy()
with_label["cluster"] = with_label["cluster"].astype(int)
print(f"Rows with cluster label for ANOVA: {len(with_label):,}")

cols_for_anova = [c for c in with_label.columns if not is_excluded(c)]
print(f"Columns evaluated: {len(cols_for_anova)}")

results = []
for col in cols_for_anova:
    s = with_label[col]
    if not pd.api.types.is_numeric_dtype(s):
        s = pd.to_numeric(s, errors="coerce")
    sub = pd.DataFrame({"x": s, "g": with_label["cluster"]}).dropna()
    if sub["g"].nunique() < 2 or len(sub) < 3:
        results.append({"column": col, "F": np.nan, "p": np.nan,
                        "n": len(sub), "n_groups": sub["g"].nunique(),
                        "note": "insufficient data"})
        continue
    groups = [g["x"].values for _, g in sub.groupby("g") if len(g) >= 2]
    if len(groups) < 2:
        results.append({"column": col, "F": np.nan, "p": np.nan,
                        "n": len(sub), "n_groups": len(groups),
                        "note": "insufficient groups"})
        continue
    # Skip constant series
    if sub["x"].nunique() < 2:
        results.append({"column": col, "F": np.nan, "p": np.nan,
                        "n": len(sub), "n_groups": len(groups),
                        "note": "constant"})
        continue
    F, p = stats.f_oneway(*groups)
    results.append({"column": col, "F": float(F), "p": float(p),
                    "n": int(len(sub)), "n_groups": int(len(groups)),
                    "note": ""})

disc = pd.DataFrame(results).sort_values("F", ascending=False, na_position="last")
disc.to_csv(os.path.join(OUT_DIR, "cluster_discrimination.csv"), index=False)
print(f"Saved cluster_discrimination.csv ({len(disc)} rows)")

print("\nTop 30 discriminating variables:")
print(disc.head(30).to_string(index=False))
