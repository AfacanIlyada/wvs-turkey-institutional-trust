"""
Cluster-robustness pressure tests against the original Hungarian-matched
k=3 KMeans clusters (cf. trust_clusters.py + κ=0.384 finding in
pressure_tests.md).

Three alternatives, same input feature set:
  - k=4 KMeans  (does the middle cluster split?)
  - Hierarchical with Ward linkage, k=3
  - Gaussian Mixture Model, k=3 (soft → hard labels)

Per alternative, identify the middle-trust cluster (second-highest mean
inst_conf), compute army/police means by wave, and ask whether the
WV5→WV6 army-police flip replicates.
"""
import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import cohen_kappa_score
from scipy.optimize import linear_sum_assignment

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")
WAVES   = ["WV2","WV3","WV4","WV5","WV6","WV7"]
YEARS   = {"WV2":1990,"WV3":1996,"WV4":2001,"WV5":2007,"WV6":2011,"WV7":2018}

CONF_ITEMS = ["conf_military","conf_police","conf_courts",
              "conf_parliament","conf_government","conf_religious"]

# =========================================================================
# Data prep
# =========================================================================
df = pd.read_csv(os.path.join(RESULTS, "pooled_extended_v2.csv"))
print(f"Loaded pooled_extended_v2.csv: {df.shape}")

# v2 is missing conf_religious (it was in v1's pooled_with_clusters.csv).
# v1 and v2 preserve the same per-wave row ordering, so we can join on
# (wave, row_in_wave) to pull conf_religious in.
v1 = pd.read_csv(os.path.join(RESULTS, "pooled_with_clusters.csv"))
v1["row_in_wave"] = v1.groupby("wave").cumcount()
df = df.merge(v1[["wave","row_in_wave","conf_religious"]],
              on=["wave","row_in_wave"], how="left")
print(f"After merging conf_religious from v1: {df.shape}  "
      f"(conf_religious non-null = {df['conf_religious'].notna().sum()})")

# Drop rows with >30% missing across the six conf items (>1.8 → ≥2 missing)
frac_miss = df[CONF_ITEMS].isna().mean(axis=1)
df = df[frac_miss <= 0.30].copy()
print(f"After dropping rows with >30% missing on the six conf items: {df.shape}")

# Median impute within wave (per-column, per-wave); when a wave has no
# observations for an item (WV4 conf_courts), fall back to overall median.
for c in CONF_ITEMS:
    df[c] = df.groupby("wave")[c].transform(lambda s: s.fillna(s.median()))
    if df[c].isna().any():
        df[c] = df[c].fillna(df[c].median())

# z-score WITHIN wave (so cluster solutions are invariant to wave-level
# scale shifts; same convention as trust_clusters.py's min-max normalization)
def z_per_wave(s):
    m, sd = s.mean(), s.std(ddof=0)
    return (s - m) / sd if sd > 0 else s * 0
for c in CONF_ITEMS:
    df[f"{c}_z"] = df.groupby("wave")[c].transform(z_per_wave)

Z_ITEMS = [c + "_z" for c in CONF_ITEMS]
X = df[Z_ITEMS].values

# Original cluster label (from pooled_extended_v2 — already merged in)
# Rows we kept may have NaN cluster (those dropped in original clustering's
# >30% rule applied to 14-item set). Restrict to the intersection.
keep_mask = df["cluster"].notna()
df_k = df[keep_mask].copy()
df_k["cluster"] = df_k["cluster"].astype(int)
X_k = df_k[Z_ITEMS].values
orig = df_k["cluster"].values
print(f"Rows with both alternative-input + original cluster label: {len(df_k):,}")


# =========================================================================
# Helper: best label mapping via Hungarian (k_new can differ from k_old=3)
# =========================================================================
def best_map_kappa(new_labels, old_labels, k_new, k_old=3):
    """For k_new == k_old: Hungarian-permute new labels to maximize agreement.
    Returns (remapped, kappa, agreement). For k_new != k_old, map each new
    label to the most-overlapping old label (many-to-one) for kappa eval."""
    ct = pd.crosstab(new_labels, old_labels)
    # Ensure all 0..k-1 are present
    ct = ct.reindex(index=range(k_new), columns=range(k_old), fill_value=0).values
    if k_new == k_old:
        row, col = linear_sum_assignment(-ct)
        mapping = {row[i]: col[i] for i in range(k_new)}
    else:
        # many-to-one: each new label → argmax overlap with an old label
        mapping = {i: int(ct[i].argmax()) for i in range(k_new)}
    remapped = np.array([mapping[x] for x in new_labels])
    kappa = cohen_kappa_score(old_labels, remapped)
    agreement = (old_labels == remapped).mean()
    return remapped, kappa, agreement, mapping


def cluster_profile(df_sub, label_col, items=CONF_ITEMS):
    """Return per-cluster mean of original-scale (not z'd) conf items."""
    return df_sub.groupby(label_col)[items].mean().round(3)


def middle_cluster(prof, items=CONF_ITEMS):
    """Pick the cluster whose mean over `items` is the middle of the three."""
    ranked = prof[items].mean(axis=1).sort_values()
    return ranked.index[len(ranked) // 2]   # middle index


def flip_table(df_sub, label_col, middle_id):
    """For the middle cluster, return wave × (army, police, gap)."""
    sub = df_sub[df_sub[label_col] == middle_id]
    rows = []
    for w in WAVES:
        cell = sub[sub["wave"] == w]
        mil = cell["conf_military"].mean()
        pol = cell["conf_police"].mean()
        rows.append({
            "wave": w, "year": YEARS[w], "n_in_middle": len(cell),
            "conf_military_mean": (None if np.isnan(mil) else round(mil, 4)),
            "conf_police_mean":   (None if np.isnan(pol) else round(pol, 4)),
            "army_police_gap":    (None if np.isnan(mil-pol) else round(mil-pol, 4)),
        })
    return pd.DataFrame(rows)


# =========================================================================
# Alternative 1 — k=4 KMeans
# =========================================================================
print("\n" + "=" * 78)
print("ALTERNATIVE 1 — k=4 KMeans")
print("=" * 78)
km4 = KMeans(n_clusters=4, n_init=30, random_state=42).fit(X)
labels_km4_all = km4.labels_                  # for all retained rows
# Restrict to rows that also have original labels for kappa
labels_km4 = labels_km4_all[keep_mask.values[df.index.argsort()]] \
    if False else labels_km4_all[df.index.isin(df_k.index)]

# Cross-tab vs original
ct4 = pd.crosstab(labels_km4, orig,
                  rownames=["new_k4"], colnames=["original"])
print("\nCross-tab new_k4 × original_k3 (rows = new):")
print(ct4)
remapped4, kappa4, agree4, mapping4 = best_map_kappa(labels_km4, orig, 4)
print(f"\nMany-to-one mapping (new->old): {mapping4}")
print(f"κ vs original = {kappa4:.3f}   agreement = {agree4*100:.1f}%")

# Which original cluster contributes >1 new clusters? → that one splits
split = None
for old_c in range(3):
    new_for_this_old = [k for k, v in mapping4.items() if v == old_c]
    if len(new_for_this_old) >= 2:
        split = (old_c, new_for_this_old)
        break
if split:
    print(f"Original cluster {split[0]} splits into new clusters {split[1]}.")

# Profile of all 4 new clusters
df_k["km4_label"] = labels_km4
prof_km4 = cluster_profile(df_k, "km4_label")
print("\nMean conf_* per new (k=4) cluster:")
print(prof_km4.to_string())

# Middle-trust cluster + flip check
mid_id_km4 = middle_cluster(prof_km4)
print(f"\nMiddle-trust cluster (new k=4): {mid_id_km4}")
flip_km4 = flip_table(df_k, "km4_label", mid_id_km4)
print("Army-police gap by wave for middle-trust cluster:")
print(flip_km4.to_string(index=False))
flip_km4_detected = (flip_km4["army_police_gap"].dropna().lt(0).any())
print(f"Flip detected (any wave with negative army-police gap)? {flip_km4_detected}")


# =========================================================================
# Alternative 2 — Ward hierarchical, k=3
# =========================================================================
print("\n" + "=" * 78)
print("ALTERNATIVE 2 — Ward hierarchical, k=3")
print("=" * 78)
ward = AgglomerativeClustering(n_clusters=3, linkage="ward").fit(X)
labels_ward_all = ward.labels_
labels_ward = labels_ward_all[df.index.isin(df_k.index)]

remapped_w, kappa_w, agree_w, mapping_w = best_map_kappa(labels_ward, orig, 3, 3)
print(f"Mapping new->old (Hungarian): {mapping_w}")
print(f"κ vs original = {kappa_w:.3f}   agreement = {agree_w*100:.1f}%")

df_k["ward_label"] = remapped_w  # use remapped so 0/1/2 align with original
prof_ward = cluster_profile(df_k, "ward_label")
print("\nMean conf_* per Ward cluster (labels Hungarian-aligned to original):")
print(prof_ward.to_string())

mid_id_ward = middle_cluster(prof_ward)
print(f"\nMiddle-trust cluster (Ward): {mid_id_ward}")
flip_ward = flip_table(df_k, "ward_label", mid_id_ward)
print("Army-police gap by wave for middle-trust cluster:")
print(flip_ward.to_string(index=False))
flip_ward_detected = (flip_ward["army_police_gap"].dropna().lt(0).any())
print(f"Flip detected? {flip_ward_detected}")


# =========================================================================
# Alternative 3 — Gaussian Mixture Model, k=3
# =========================================================================
print("\n" + "=" * 78)
print("ALTERNATIVE 3 — Gaussian Mixture Model, k=3")
print("=" * 78)
gmm = GaussianMixture(n_components=3, covariance_type="full",
                      random_state=42, max_iter=300).fit(X)
labels_gmm_all = gmm.predict(X)
labels_gmm = labels_gmm_all[df.index.isin(df_k.index)]

remapped_g, kappa_g, agree_g, mapping_g = best_map_kappa(labels_gmm, orig, 3, 3)
print(f"Mapping new->old (Hungarian): {mapping_g}")
print(f"κ vs original = {kappa_g:.3f}   agreement = {agree_g*100:.1f}%")

df_k["gmm_label"] = remapped_g
prof_gmm = cluster_profile(df_k, "gmm_label")
print("\nMean conf_* per GMM cluster (labels Hungarian-aligned to original):")
print(prof_gmm.to_string())

mid_id_gmm = middle_cluster(prof_gmm)
print(f"\nMiddle-trust cluster (GMM): {mid_id_gmm}")
flip_gmm = flip_table(df_k, "gmm_label", mid_id_gmm)
print("Army-police gap by wave for middle-trust cluster:")
print(flip_gmm.to_string(index=False))
flip_gmm_detected = (flip_gmm["army_police_gap"].dropna().lt(0).any())
print(f"Flip detected? {flip_gmm_detected}")


# =========================================================================
# Aggregate outputs
# =========================================================================
robust_rows = []
for method, flip_df, mid_id in [
    ("k4_kmeans",   flip_km4,  mid_id_km4),
    ("ward_k3",     flip_ward, mid_id_ward),
    ("gmm_k3",      flip_gmm,  mid_id_gmm),
]:
    for _, r in flip_df.iterrows():
        robust_rows.append({
            "method": method,
            "wave": r["wave"], "year": r["year"],
            "cluster_label": int(mid_id),
            "conf_military_mean": r["conf_military_mean"],
            "conf_police_mean":   r["conf_police_mean"],
            "army_police_gap":    r["army_police_gap"],
            "flip_detected_at_wave": (
                r["army_police_gap"] is not None
                and r["army_police_gap"] < 0),
        })
robust = pd.DataFrame(robust_rows)
robust.to_csv(os.path.join(RESULTS, "cluster_robustness.csv"), index=False)
print(f"\nSaved results/cluster_robustness.csv ({len(robust)} rows)")

kappa_rows = [
    {"method": "k4_kmeans",   "kappa_vs_original": round(kappa4, 3),
     "agreement_pct": round(agree4 * 100, 1),
     "middle_cluster_flip": "yes" if flip_km4_detected else "no"},
    {"method": "ward_k3",     "kappa_vs_original": round(kappa_w, 3),
     "agreement_pct": round(agree_w * 100, 1),
     "middle_cluster_flip": "yes" if flip_ward_detected else "no"},
    {"method": "gmm_k3",      "kappa_vs_original": round(kappa_g, 3),
     "agreement_pct": round(agree_g * 100, 1),
     "middle_cluster_flip": "yes" if flip_gmm_detected else "no"},
]
kappa_df = pd.DataFrame(kappa_rows)
kappa_df.to_csv(os.path.join(RESULTS, "cluster_kappa_summary.csv"), index=False)

print("\n" + "=" * 78)
print("SUMMARY")
print("=" * 78)
print(kappa_df.to_string(index=False))

n_replicate = sum(r["middle_cluster_flip"] == "yes" for r in kappa_rows)
print(f"\nFlip finding robust across {n_replicate}/3 alternative clusterings")
