"""
Extend the WVS Turkey concept crosswalk, re-pool all six waves into a
single clean dataset, merge cluster labels, and run integrity checks.

Steps mirror the user's brief:
  1) Write WVS_TR_concept_crosswalk_v2.csv (extended); spot-check WV4 for
     concepts already in the existing pooled file.
  2) Re-pool. Recode female, reverse-code confidence, apply 3-group
     education recode, leave party_recode = NaN (print top-10 codes
     per wave for user verification).
  3) Save results/pooled_extended.csv; print shape, % missing,
     mean conf_* by cluster, value_counts of party_recode by wave.
"""
import os
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
warnings.filterwarnings("ignore", category=FutureWarning)

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")
WAVES   = ["WV2","WV3","WV4","WV5","WV6","WV7"]
YEARS   = {"WV2":1990,"WV3":1996,"WV4":2001,"WV5":2007,"WV6":2011,"WV7":2018}
FILES   = {
    "WV2": "F00008272-WV2_Data_Turkey_Excel_v1.6.1.xlsx",
    "WV3": "F00008135-WV3_Data_Turkey_Excel_v20221107.1.xlsx",
    "WV4": "F00008022-WV4_Data_Turkey_Excel_v20201117.1.xlsx",
    "WV5": "F00007873-WV5_Data_Turkey_Excel_v20201117.1.xlsx",
    "WV6": "F00007629-WV6_Data_Turkey_2011_Excel_v20180912.xlsx",
    "WV7": "F00013222-WVS_Wave_7_Turkey_Excel_v5.1.xlsx",
}

# =========================================================================
# Step 1: extended crosswalk
# =========================================================================
# Per user clarification: use raw V375 / V363 for WV2 (not the *R recodes).
# "MISS" markers indicate the variable is genuinely not asked in that wave.
CROSSWALK = [
    # concept              WV2     WV3     WV4     WV5     WV6     WV7     notes
    ("conf_military",     "V273", "V136", "V148", "V132", "V109", "Q65",  "Confidence: armed forces"),
    ("conf_police",       "V278", "V141", "V152", "V136", "V113", "Q69",  "Confidence: police"),
    ("conf_courts",       "V275", "V137", "MISS", "V137", "V114", "Q70",  "Confidence: courts; WV4 missing"),
    ("conf_parliament",   "V279", "V144", "V155", "V140", "V117", "Q73",  "Confidence: parliament"),
    ("conf_government",   "V289", "V142", "V153", "V138", "V115", "Q71",  "Confidence: government"),
    ("rel_person",        "V151", "V182", "V186", "V187", "V147", "Q173", "Religious person (=rel_id in pooled v1)"),
    ("rel_attendance",    "V147", "V181", "V185", "V186", "V145", "Q171", "Religious attendance"),
    ("rel_importance_god","V176", "V190", "V196", "V192", "V152", "Q164", "NEW: importance of God"),
    ("left_right",        "V248", "V123", "V139", "V114", "V95",  "Q240", "NEW: left-right self-placement"),
    ("life_satisfaction", "V96",  "V65",  "V81",  "V22",  "V23",  "Q49",  "Already in pooled"),
    ("age",               "V355", "V216", "V225", "V237", "V242", "Q262", "Already in pooled"),
    ("sex",               "V353", "V214", "V223", "V235", "V240", "Q260", "1=male,2=female; recode to female"),
    ("income_raw",        "V363", "V227", "V236", "V253", "V239", "Q288", "NEW raw income (full scale)"),
    ("education_raw",     "V375", "V217", "V226", "V238", "V248", "Q275", "NEW raw education (full scale)"),
    ("party_raw",         "V351", "V210", "V220", "V231", "V228", "Q223", "NEW raw vote-intention first choice"),
]
xwalk_v2 = pd.DataFrame(CROSSWALK,
    columns=["concept","WV2","WV3","WV4","WV5","WV6","WV7","notes"])
xwalk_v2["n_waves"] = (xwalk_v2[WAVES] != "MISS").sum(axis=1)
xwalk_v2 = xwalk_v2[["concept","WV2","WV3","WV4","WV5","WV6","WV7","n_waves","notes"]]
xwalk_v2.to_csv(os.path.join(ROOT, "WVS_TR_concept_crosswalk_v2.csv"), index=False)
print("Step 1: wrote WVS_TR_concept_crosswalk_v2.csv")
print(xwalk_v2.to_string(index=False))


# Build a code->full_header map per wave (so we can request by V-code)
def header_map(wave_file):
    head = pd.read_excel(wave_file, nrows=0)
    m = {}
    for full in head.columns:
        s = str(full).strip()
        code = s.split(":", 1)[0].strip() if ":" in s else s
        m[code] = full
    return m

print("\n--- Building per-wave header maps... ---")
HEADER_MAPS = {w: header_map(os.path.join(ROOT, FILES[w])) for w in WAVES}


def load_wave_concepts(w):
    """Return DataFrame for wave w with one column per concept in CROSSWALK
    (renamed to the concept name). MISS or unmapped codes -> column of NaN.
    """
    hm = HEADER_MAPS[w]
    path = os.path.join(ROOT, FILES[w])
    # which concepts have a valid code in this wave AND that code exists in
    # the file's column index?
    want_full, want_concept = [], []
    for row in CROSSWALK:
        concept = row[0]
        code = row[1 + WAVES.index(w)]
        if code == "MISS":
            continue
        if code in hm:
            want_full.append(hm[code])
            want_concept.append(concept)
        else:
            print(f"  ! {w}: code {code} (concept {concept}) not in file")
    df = pd.read_excel(path, usecols=want_full)
    df = df.rename(columns=dict(zip(want_full, want_concept)))
    # add NaN columns for any concept not present
    for c in [r[0] for r in CROSSWALK]:
        if c not in df.columns:
            df[c] = np.nan
    return df[[r[0] for r in CROSSWALK]]


# =========================================================================
# Step 1b: spot check vs existing pooled (WV4 sample)
# =========================================================================
print("\n\nSpot-check: 'already in pooled' concepts vs raw WV4 -----")
pooled_v1 = pd.read_csv(os.path.join(RESULTS, "pooled_with_clusters.csv"))
wv4_pos   = pooled_v1.index[pooled_v1["wave"] == "WV4"]
wv4_raw   = load_wave_concepts("WV4")
# pooled v1 retains the SAME row order as the source xlsx within each wave
# (proven in trust_clusters.py with the equality assert). So row i of
# wv4_raw maps to row wv4_pos[i] of pooled_v1.
assert len(wv4_raw) == len(wv4_pos), \
    f"WV4 length mismatch raw={len(wv4_raw)} pooled={len(wv4_pos)}"
wv4_raw_idx = wv4_raw.copy()
wv4_raw_idx.index = wv4_pos

CHECKS = [
    ("conf_military",   "conf_military",   True),   # reverse-coded in pooled
    ("conf_police",     None,              True),   # not in pooled v1 — should be absent
    ("conf_parliament", "conf_parliament", True),
    ("conf_government", "conf_government", True),
    ("rel_person",      "rel_id",          False),
    ("rel_attendance",  "rel_attendance",  False),
    ("life_satisfaction", None,            False),  # not in pooled v1 directly
    ("age",             "age",             False),
    ("sex",             "female",          False),  # we recoded direction
]
for concept, pooled_col, is_conf in CHECKS:
    print(f"\n[{concept}  vs pooled_v1.{pooled_col}]")
    raw = wv4_raw_idx[concept].head(5)
    if pooled_col and pooled_col in pooled_v1.columns:
        pv = pooled_v1.loc[wv4_pos[:5], pooled_col]
        cmp = pd.DataFrame({"raw_WV4": raw.values, "pooled_v1": pv.values})
        if is_conf:
            cmp["raw_reversed (5-x)"] = (5 - pd.to_numeric(cmp["raw_WV4"],
                                                          errors="coerce"))
        print(cmp.to_string(index=False))
    else:
        print(f"  (no pooled v1 column to compare; raw head: {raw.tolist()})")


# =========================================================================
# Step 2: inspect ranges/codes before recoding
# =========================================================================
print("\n\nStep 2 pre-flight: value ranges + party codes ----------")
prepool = {}
for w in WAVES:
    prepool[w] = load_wave_concepts(w)
    df = prepool[w]
    print(f"\n--- {w} ({YEARS[w]})  n={len(df)} ---")
    for c in ["education_raw", "income_raw", "sex", "left_right",
              "life_satisfaction"]:
        v = pd.to_numeric(df[c], errors="coerce")
        v = v[v >= 0]   # drop negative refused/DK sentinels for the range
        if v.notna().any():
            print(f"  {c:<18} min={v.min():>4.0f}  max={v.max():>4.0f}  "
                  f"n={v.notna().sum():>5}  unique={v.nunique():>3}")
        else:
            print(f"  {c:<18} (no valid data)")

print("\n--- party_raw top-10 codes per wave (raw, includes negatives) ---")
for w in WAVES:
    v = prepool[w]["party_raw"]
    vc = v.value_counts(dropna=False).head(10)
    print(f"\n  {w} ({YEARS[w]}):")
    for k, n in vc.items():
        print(f"    code={k!r:>6}  n={n}")


# =========================================================================
# Step 2b: build the pooled_extended dataframe
# =========================================================================
print("\n\nStep 2b: stacking and recoding ----------")
frames = []
for w in WAVES:
    df = prepool[w].copy()
    df.insert(0, "wave", w)
    df.insert(1, "year", YEARS[w])
    df.insert(2, "row_in_wave", np.arange(len(df)))
    frames.append(df)
ext = pd.concat(frames, ignore_index=True)
print(f"Stacked shape: {ext.shape}")

# Drop WVS sentinels (<0) -> NaN for numeric concepts
NUMERIC_CONCEPTS = ["conf_military","conf_police","conf_courts",
                    "conf_parliament","conf_government","rel_person",
                    "rel_attendance","rel_importance_god","left_right",
                    "life_satisfaction","age","sex","income_raw",
                    "education_raw"]
for c in NUMERIC_CONCEPTS:
    v = pd.to_numeric(ext[c], errors="coerce")
    v = v.where(v >= 0, np.nan)
    ext[c] = v

# Reverse-code confidence items so higher = more confidence (raw is
# 1=Great deal .. 4=None; reverse: new = 5 - x).
CONF_COLS = ["conf_military","conf_police","conf_courts",
             "conf_parliament","conf_government"]
for c in CONF_COLS:
    v = ext[c]
    v = v.where(v.isin([1,2,3,4]), np.nan)
    ext[c] = 5 - v

# Sex -> female dummy (WVS: 1=Male, 2=Female  ->  0=male, 1=female)
ext["female"] = ext["sex"].map({1: 0, 2: 1})
# keep original sex too for transparency
# (drop nothing — leave both)

# Education 3-group recode (after sentinel drop)
# WVS X025 raw scale is 1..8 (1=no formal .. 8=higher tertiary).
# Brief: 1-2 → 1 low, 3-5 → 2 medium, 6-8 → 3 high.
def edu_recode(v):
    if pd.isna(v): return np.nan
    if v <= 2:    return 1
    if v <= 5:    return 2
    if v <= 8:    return 3
    return np.nan
ext["education_recode"] = ext["education_raw"].apply(edu_recode)

# Party recode left as NaN per user request (codebook verification needed)
ext["party_recode"] = np.where(
    ext["wave"].isin(["WV2","WV3","WV4"]),
    "pre_AKP_era",
    np.nan,
)

# Cluster merge on (wave, row_in_wave). Reconstruct row_in_wave for pooled_v1
pooled_v1 = pooled_v1.copy()
pooled_v1["row_in_wave"] = pooled_v1.groupby("wave").cumcount()
ext = ext.merge(pooled_v1[["wave","row_in_wave","cluster"]],
                on=["wave","row_in_wave"], how="left")
print(f"After cluster merge: {ext.shape}")
print(f"Cluster non-null: {ext['cluster'].notna().sum()} / {len(ext)}")

ext.to_csv(os.path.join(RESULTS, "pooled_extended.csv"), index=False)
print(f"\nSaved results/pooled_extended.csv ({ext.shape})")


# =========================================================================
# Step 3: integrity checks
# =========================================================================
print("\n\n" + "=" * 72)
print("Step 3: integrity checks")
print("=" * 72)
print(f"\nShape: {ext.shape}")
print(f"\nWave distribution:\n{ext['wave'].value_counts().sort_index().to_string()}")

print("\n% missing per column:")
miss = (ext.isna().mean() * 100).round(2).sort_index()
print(miss.to_string())

print("\nMean confidence by cluster (raw 1-4, higher = more confidence):")
with_label = ext.dropna(subset=["cluster"]).copy()
with_label["cluster"] = with_label["cluster"].astype(int)
print(with_label.groupby("cluster")[CONF_COLS].mean().round(3).to_string())

print("\nReference (from earlier profiling): military expected ~2.0/3.5/3.7")

print("\nparty_recode value counts by wave:")
print(ext.groupby("wave")["party_recode"]
        .value_counts(dropna=False).to_string())

print("\nfemale value counts by wave (sanity: ~50/50):")
print(ext.groupby("wave")["female"]
        .value_counts(dropna=False).to_string())

print("\neducation_recode value counts by wave:")
print(ext.groupby("wave")["education_recode"]
        .value_counts(dropna=False).sort_index().to_string())
