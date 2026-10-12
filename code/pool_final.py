"""
Final pooling pass — DEFINITIVE analysis dataset.

Outputs:
  WVS_TR_concept_crosswalk_v3.csv  (master variable map)
  results/pooled_extended_v2.csv   (the analysis dataset)
  results/integrity_report_v2.txt  (sanity + missingness report)
  results/column_manifest_v2.csv   (data dictionary)
"""
import os
import io
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
# STEP 1 — Crosswalk v3
# =========================================================================
# Columns: concept, WV2, WV3, WV4, WV5, WV6, WV7, notes
# "MISS" = confirmed absent.
ROWS = [
    # confidence items (already in v2)
    ("conf_military",         "V273","V136","V148","V132","V109","Q65",
        "Confidence: armed forces; reverse-coded to higher=more trust"),
    ("conf_police",           "V278","V141","V152","V136","V113","Q69",
        "Confidence: police; reverse-coded"),
    ("conf_courts",           "V275","V137","MISS","V137","V114","Q70",
        "Confidence: courts; WV4 missing; reverse-coded"),
    ("conf_parliament",       "V279","V144","V155","V140","V117","Q73",
        "Confidence: parliament; reverse-coded"),
    ("conf_government",       "V289","V142","V153","V138","V115","Q71",
        "Confidence: government; reverse-coded"),
    ("conf_civil_service",    "V280","V145","V156","V141","V118","Q74",
        "Confidence: civil services; reverse-coded"),
    # religion (already in v2)
    ("rel_person",            "V151","V182","V186","V187","V147","Q173",
        "Religious person self-id (raw 1=religious,2=not,3=atheist)"),
    ("rel_attendance",        "V147","V181","V185","V186","V145","Q171",
        "Religious attendance frequency (raw, higher=less often per WVS)"),
    ("rel_importance_god",    "V176","V190","V196","V192","V152","Q164",
        "Importance of God in life (raw 1-10)"),
    # politics & values (mix new and existing)
    ("left_right",            "V248","V123","V139","V114","V95", "Q240",
        "Self-placement left-right (raw 1=left .. 10=right)"),
    ("life_satisfaction",     "V96", "V65", "V81", "V22", "V23", "Q49",
        "Satisfaction with your life (raw 1-10)"),
    ("financial_satisfaction","V132","V64", "V80", "V68", "V59", "Q50",
        "Satisfaction with household financial situation (raw 1-10)"),
    ("happiness",             "V18", "V10", "V11", "V10", "V10", "Q46",
        "Feeling of happiness (raw 1=very happy .. 4=not at all)"),
    ("interpersonal_trust",   "V94", "V27", "V25", "V23", "V24", "Q57",
        "Most people can be trusted (raw 1=can be trusted,2=can't)"),
    ("political_interest",    "V241","V117","V133","V95", "V84", "Q199",
        "Interest in politics (raw 1=very interested .. 4=not at all)"),
    ("freedom_control",       "MISS","V66", "V82", "V46", "V55", "Q48",
        "How much freedom of choice and control (raw 1-10); WV2 missing"),
    ("democracy_importance",  "MISS","MISS","MISS","V162","V140","Q250",
        "Importance of democracy (raw 1-10); not asked WV2-4"),
    ("strong_leader",         "MISS","V154","V164","V148","V127","Q235",
        "Political system: strong leader (raw 1=very good .. 4=very bad); WV2 missing"),
    ("national_pride",        "V322","V205","V216","V209","V211","Q254",
        "How proud of nationality (raw 1=very .. 4=not at all proud)"),
    ("postmaterialism_index", "Y002","Y002","Y002","Y002","Y002","Y002",
        "Inglehart 4-item index (1=Materialist,2=Mixed,3=Postmaterialist)"),
    # demographics (already in v2 + new)
    ("age",                   "V355","V216","V225","V237","V242","Q262",
        "Age in years"),
    ("sex",                   "V353","V214","V223","V235","V240","Q260",
        "Sex (raw 1=male, 2=female)"),
    ("education_raw",         "V375","V217","V226","V238","V248","Q275",
        "Education attainment; WV2-6 use WVS X025 1-8/9 scale; WV7 uses "
        "ISCED 0-6; education_recode not directly comparable across WV7"),
    ("income_raw",            "V363","V227","V236","V253","V239","Q288",
        "Scale of incomes / subjective income decile (raw 1-10)"),
    ("marital_status",        "V181","V89", "V106","V55", "V57", "Q273",
        "Marital status (raw codes; 1=married, 2=living-together typical)"),
    ("social_class",          "MISS","V226","V235","V252","V238","Q287",
        "Subjective social class (raw 1=upper .. 5=lower per WVS); WV2 missing"),
    ("region",                "V370","V234","REGION_ISO","V257","V256","N_REGION_WVS",
        "Sub-national region where interview conducted (categorical, "
        "wave-specific codes)"),
    ("party_raw",             "V351","V210","V220","V231","V228","Q223",
        "Vote intention first choice (raw country-specific party codes)"),
    # membership battery — WV4 missing entirely; binary recode below
    ("member_org_church",     "MISS","V28", "MISS","V24", "V25", "Q94",
        "Active/Inactive membership of church or religious org"),
    ("member_org_sport",      "V29", "V29", "MISS","V25", "V26", "Q95",
        "Active/Inactive membership of sport or recreation"),
    ("member_org_labour",     "V22", "V31", "MISS","V27", "V28", "Q97",
        "Active/Inactive membership of labour unions"),
    ("member_org_political_party",
                              "V23", "V32", "MISS","V28", "V29", "Q98",
        "Active/Inactive membership of political party"),
    # justifiability raw (1-10) — WV3 + WV4 missing in Turkey country files
    ("justif_abortion",       "V309","MISS","MISS","V204","V204","Q184",
        "Justifiable: abortion (raw 1=never .. 10=always)"),
    ("justif_divorce",        "V310","MISS","MISS","V205","V205","Q185",
        "Justifiable: divorce (raw 1-10)"),
    ("justif_homosex",        "V307","MISS","MISS","V202","V203","Q182",
        "Justifiable: homosexuality (raw 1-10)"),
    # Welzel composites — present in all six waves; cross-wave harmonized
    ("welzel_abortlib",       "I_ABORTLIB",) * 6 + (
        "Welzel emancipative-values: abortion acceptance; column present in all 6 waves, "
        "but all-NaN in WV3 + WV4 (Turkey country files lack the raw justif item to compute it)",
    ),
    ("welzel_divorlib",       "I_DIVORLIB",) * 6 + (
        "Welzel emancipative-values: divorce acceptance; WV3/WV4 all-NaN",
    ),
    ("welzel_homolib",        "I_HOMOLIB",) * 6 + (
        "Welzel emancipative-values: homosexuality acceptance; WV3/WV4 all-NaN",
    ),
    # child qualities — binary mention/not
    ("child_independence",    "V227","V15", "V15", "V12", "V12", "Q8",
        "Important child qualities: independence (binary mention)"),
    ("child_obedience",       "V236","V24", "V24", "V21", "V21", "Q17",
        "Important child qualities: obedience (binary mention)"),
    # neighbor items — binary mention (1=would NOT like as neighbor)
    ("neighbor_immigrants",   "V77", "V57", "V73", "V37", "V39", "Q21",
        "Neighbours: immigrants/foreign workers (1=would not like, 0=fine)"),
    ("neighbor_religion",     "MISS","MISS","V77_03","V39", "V41", "Q23",
        "Neighbours: different religion (1=would not like); WV2/3 missing"),
]

# Flatten the welzel tuples into the same shape as others
xrows = []
for r in ROWS:
    if r[0].startswith("welzel"):
        concept, code, notes = r[0], r[1], r[-1]
        xrows.append([concept] + [code]*6 + [notes])
    else:
        xrows.append(list(r))
xwalk = pd.DataFrame(xrows, columns=["concept"] + WAVES + ["notes"])
xwalk["n_waves"] = (xwalk[WAVES] != "MISS").sum(axis=1)
xwalk = xwalk[["concept"] + WAVES + ["n_waves", "notes"]]
xwalk.to_csv(os.path.join(ROOT, "WVS_TR_concept_crosswalk_v3.csv"), index=False)
print("CROSSWALK v3")
print(xwalk.to_string(index=False))


# =========================================================================
# STEP 2 — Pool everything
# =========================================================================
# Build per-wave header maps (code -> full header)
def header_map(path):
    head = pd.read_excel(path, nrows=0)
    m = {}
    for full in head.columns:
        s = str(full).strip()
        code = s.split(":", 1)[0].strip() if ":" in s else s
        m[code] = full
    return m

HM = {w: header_map(os.path.join(ROOT, FILES[w])) for w in WAVES}
print("\n--- header maps built ---")

def load_wave(w):
    """Load one wave with all crosswalk-v3 concepts; rename to concept names."""
    hm   = HM[w]
    path = os.path.join(ROOT, FILES[w])
    want_full, want_concept, missing = [], [], []
    for _, r in xwalk.iterrows():
        code = r[w]
        if code == "MISS":
            continue
        if code in hm:
            want_full.append(hm[code]); want_concept.append(r["concept"])
        else:
            missing.append((r["concept"], code))
    if missing:
        print(f"  {w}: code-not-in-file -> {missing}")
    df = pd.read_excel(path, usecols=want_full)
    df = df.rename(columns=dict(zip(want_full, want_concept)))
    # Add NaN columns for concepts not present in this wave
    for c in xwalk["concept"]:
        if c not in df.columns:
            df[c] = np.nan
    return df[xwalk["concept"].tolist()]

print("\n--- loading waves ---")
frames = []
for w in WAVES:
    print(f"  loading {w}...")
    df = load_wave(w)
    df.insert(0, "wave", w)
    df.insert(1, "year", YEARS[w])
    df.insert(2, "row_in_wave", np.arange(len(df)))
    frames.append(df)
pool = pd.concat(frames, ignore_index=True)
print(f"\nStacked shape: {pool.shape}")


# --------------------- Transformations ------------------------------------
# 1. Sentinel-drop: WVS negatives (and -2,-1,-3,-4,-5) → NaN for numeric items
NUMERIC = [c for c in xwalk["concept"]
           if c not in ("region", "party_raw", "marital_status")]
for c in NUMERIC:
    v = pd.to_numeric(pool[c], errors="coerce")
    pool[c] = v.where(v >= 0, np.nan)
# Marital and party: only drop the most-negative refusal codes < -5 just in case
for c in ("marital_status", "party_raw"):
    v = pd.to_numeric(pool[c], errors="coerce")
    pool[c] = v  # keep -1/-2 etc. as-is; mapping below handles them

# 2. Reverse-code confidence items (raw 1=Great deal .. 4=None -> 5-x)
CONF = ["conf_military","conf_police","conf_courts","conf_parliament",
        "conf_government","conf_civil_service"]
for c in CONF:
    v = pool[c].where(pool[c].isin([1,2,3,4]), np.nan)
    pool[c] = 5 - v

# 3. female dummy (sex: 1=male,2=female -> 0,1)
pool["female"] = pool["sex"].map({1: 0, 2: 1})

# 4. education_recode 3-group: low/med/high
def edu_recode(v):
    if pd.isna(v): return np.nan
    if v <= 2: return 1
    if v <= 5: return 2
    if v <= 8: return 3
    return np.nan
pool["education_recode"] = pool["education_raw"].apply(edu_recode)

# 5. married_dummy from marital_status; WVS codes: 1=Married, 2=Living together
pool["married_dummy"] = pool["marital_status"].apply(
    lambda v: 1 if v in (1, 2) else (0 if v in (3, 4, 5, 6) else np.nan))

# 6. party_recode per spec
PARTY_MAP_678 = {792008:"AKP", 792002:"CHP", 792006:"MHP",
                 792005:"HDP"}
NAN_CODES = {-1, -2, 5, 2}
def party_recode(row):
    w = row["wave"]
    if w in ("WV2","WV3","WV4"):
        return "pre_AKP_era"
    p = row["party_raw"]
    if pd.isna(p):
        return np.nan
    p = int(p)
    if p in NAN_CODES:
        return np.nan
    if p in PARTY_MAP_678:
        return PARTY_MAP_678[p]
    if p == 792050:
        return "IYI" if w == "WV7" else "other"
    return "other"
pool["party_recode"] = pool.apply(party_recode, axis=1)

# 7. member_org_*: recode to binary, wave-dependent (codings differ).
#    WV2: 1=Mentioned (belongs), 2=Not mentioned   -> 1->1, 2->0
#    WV3: 1=Active, 2=Inactive, 3=Don't belong    -> {1,2}->1, 3->0
#    WV5/6/7: 0=Not a member, 1=Inactive, 2=Active -> 0->0, {1,2}->1
MEMBER_COLS = ["member_org_church","member_org_sport","member_org_labour",
               "member_org_political_party"]
def member_bin(v, wave):
    if pd.isna(v):
        return np.nan
    if wave == "WV2":
        return 1.0 if v == 1 else (0.0 if v == 2 else np.nan)
    if wave == "WV3":
        return 1.0 if v in (1, 2) else (0.0 if v == 3 else np.nan)
    # WV5, WV6, WV7
    return 1.0 if v in (1, 2) else (0.0 if v == 0 else np.nan)
for c in MEMBER_COLS:
    pool[c + "_bin"] = [member_bin(v, w) for v, w in zip(pool[c], pool["wave"])]

# 8. neighbor items: 1=Mentioned (would NOT like as neighbour), 2=Not
# mentioned (fine). Binary: 1->1, 2->0.
NEIGHBOR_COLS = ["neighbor_immigrants","neighbor_religion"]
for c in NEIGHBOR_COLS:
    v = pool[c]
    pool[c] = np.where(v == 1, 1.0,
                       np.where(v == 2, 0.0, np.nan))

# 9. child quality items: 1=Mentioned (important), 2=Not mentioned.
# Binary: 1->1, 2->0.
CHILD_COLS = ["child_independence","child_obedience"]
for c in CHILD_COLS:
    v = pool[c]
    pool[c] = np.where(v == 1, 1.0,
                       np.where(v == 2, 0.0, np.nan))

# justifiability, freedom_control, democracy_importance: already cleaned
# (1-10 raw, negatives dropped above)

# 10. Cluster merge on (wave, row_in_wave)
v1 = pd.read_csv(os.path.join(RESULTS, "pooled_with_clusters.csv"))
v1["row_in_wave"] = v1.groupby("wave").cumcount()
pool = pool.merge(v1[["wave","row_in_wave","cluster"]],
                  on=["wave","row_in_wave"], how="left")

# Save
out_path = os.path.join(RESULTS, "pooled_extended_v2.csv")
pool.to_csv(out_path, index=False)
print(f"\nSaved {out_path}  shape={pool.shape}")


# =========================================================================
# STEP 3 — Integrity report
# =========================================================================
buf = io.StringIO()
p = lambda *a: print(*a, file=buf)

p("=" * 78)
p("WVS Turkey pooled_extended_v2 — Integrity report")
p("=" * 78)
p(f"\nShape: {pool.shape}")
p(f"\nWave distribution:")
p(pool["wave"].value_counts().sort_index().to_string())

p("\n\n--- Per-column summary ---")
for c in pool.columns:
    s = pool[c]
    miss = round(100 * s.isna().mean(), 2)
    dt   = str(s.dtype)
    if pd.api.types.is_numeric_dtype(s) and s.notna().any():
        mn, mx = np.nanmin(s.values), np.nanmax(s.values)
        nu = int(s.nunique(dropna=True))
        descr = f"min={mn:.3g}  max={mx:.3g}  n_unique={nu}"
    else:
        vc = s.value_counts(dropna=False).head(3)
        descr = "top3: " + "; ".join(f"{k}={v}" for k, v in vc.items())
    p(f"  {c:<32} miss%={miss:>5}  dtype={dt:<10}  {descr}")

# Sanity check: cluster means of conf items
p("\n\n--- Sanity check: mean confidence by cluster ---")
p("(Expected from earlier profiling — military: 2.755 / 3.518 / 3.709)")
labelled = pool.dropna(subset=["cluster"]).copy()
labelled["cluster"] = labelled["cluster"].astype(int)
p(labelled.groupby("cluster")[["conf_military","conf_police","conf_courts"]]
        .mean().round(3).to_string())

# Party crosstab
p("\n\n--- party_recode × wave (WV5/WV6/WV7 only) ---")
recent = pool[pool["wave"].isin(["WV5","WV6","WV7"])]
ct = pd.crosstab(recent["party_recode"], recent["wave"], dropna=False)
p(ct.to_string())

# membership binary check
p("\n\n--- member_org_*_bin rates by wave ---")
mem_bins = [c + "_bin" for c in MEMBER_COLS]
p(pool.groupby("wave")[mem_bins].mean().round(3).to_string())

# write
report = buf.getvalue()
report_path = os.path.join(RESULTS, "integrity_report_v2.txt")
with open(report_path, "w") as fh:
    fh.write(report)
print(report)
print(f"\nSaved {report_path}")


# =========================================================================
# STEP 4 — Column manifest (data dictionary)
# =========================================================================
# scale_range, higher_means per analytical column
MANIFEST = [
    # wave/respondent meta
    ("wave",                   "wave",                "WV2..WV7",        "later wave",          "all",   "Wave identifier"),
    ("year",                   "year",                "1990..2018",      "later year",          "all",   "Fieldwork year"),
    ("row_in_wave",            "row_in_wave",         "0..n_wave-1",     "n/a",                 "all",   "Original row index within source xlsx (for joins)"),
    ("cluster",                "cluster",             "0,1,2 or NaN",    "more trust (0->2)",   "all",   "Trust-orientation cluster from trust_clusters.py (k=3); NaN if >30% trust missing"),
    # confidence items
    ("conf_military",          "conf_military",       "1..4",            "more confidence",     "all",   "Reverse-coded from raw WVS 1=Great deal..4=None"),
    ("conf_police",            "conf_police",         "1..4",            "more confidence",     "all",   "Reverse-coded"),
    ("conf_courts",            "conf_courts",         "1..4",            "more confidence",     "all except WV4", "Reverse-coded; WV4 not asked"),
    ("conf_parliament",        "conf_parliament",     "1..4",            "more confidence",     "all",   "Reverse-coded"),
    ("conf_government",        "conf_government",     "1..4",            "more confidence",     "all",   "Reverse-coded"),
    ("conf_civil_service",     "conf_civil_service",  "1..4",            "more confidence",     "all",   "Reverse-coded"),
    # religion
    ("rel_person",             "rel_person",          "1..3",            "less religious",      "all",   "1=religious, 2=not religious, 3=convinced atheist"),
    ("rel_attendance",         "rel_attendance",      "1..8",            "less frequent",       "all",   "1=more than once a week .. 8=never (per WVS)"),
    ("rel_importance_god",     "rel_importance_god",  "1..10",           "more important",      "all",   "Importance of God in life"),
    # politics / values
    ("left_right",             "left_right",          "1..10",           "more right-wing",     "all",   "Self-placement: 1=left, 10=right"),
    ("life_satisfaction",      "life_satisfaction",   "1..10",           "more satisfied",      "all",   "Satisfaction with your life"),
    ("financial_satisfaction", "financial_satisfaction","1..10",         "more satisfied",      "all",   "Satisfaction with household finances"),
    ("happiness",              "happiness",           "1..4",            "less happy",          "all",   "1=very happy .. 4=not at all happy (WVS raw)"),
    ("interpersonal_trust",    "interpersonal_trust", "1..2",            "more distrust",       "all",   "1=most can be trusted, 2=can't be too careful"),
    ("political_interest",     "political_interest",  "1..4",            "less interested",     "all",   "1=very interested .. 4=not at all"),
    ("freedom_control",        "freedom_control",     "1..10",           "more freedom/control","WV3-WV7","Freedom of choice and control over life; WV2 missing"),
    ("democracy_importance",   "democracy_importance","1..10",           "more important",      "WV5-WV7","Importance of democracy; not asked WV2-WV4"),
    ("strong_leader",          "strong_leader",       "1..4",            "less favorable",      "WV3-WV7","1=very good political system .. 4=very bad; WV2 missing"),
    ("national_pride",         "national_pride",      "1..4",            "less proud",          "all",   "1=very proud .. 4=not at all proud (WVS raw)"),
    ("postmaterialism_index",  "postmaterialism_index","1..3",           "more postmaterialist","all",   "Y002: 1=Materialist, 2=Mixed, 3=Postmaterialist"),
    # demographics
    ("age",                    "age",                 "17..95",          "older",               "all",   "Age in years"),
    ("sex",                    "sex",                 "1,2",             "—",                   "all",   "1=male, 2=female (raw)"),
    ("female",                 "sex",                 "0,1",             "is female",           "all",   "Derived dummy: 1=female, 0=male"),
    ("education_raw",          "education_raw",       "WV2-6: 1..8/9; WV7: 0..6", "more education", "all", "WV2-6 use WVS X025 scale; WV7 uses ISCED — NOT directly comparable to earlier waves"),
    ("education_recode",       "education_raw",       "1..3",            "more education",      "all",   "Low(1-2)/Med(3-5)/High(6-8); CAVEAT: WV7 ISCED 0-6 mapped via same cutoffs — interpretation differs"),
    ("income_raw",             "income_raw",          "1..10",           "higher income",       "all",   "Scale of incomes (subjective decile)"),
    ("marital_status",         "marital_status",      "1..6",            "—",                   "all",   "1=Married,2=Living together,3=Divorced,4=Separated,5=Widowed,6=Single (raw)"),
    ("married_dummy",          "marital_status",      "0,1",             "married",             "all",   "Derived: 1 if marital_status in {1,2}, else 0"),
    ("social_class",           "social_class",        "1..5",            "lower class",         "WV3-WV7","1=upper..5=lower (subjective); WV2 missing"),
    ("region",                 "region",              "categorical",     "n/a",                 "all",   "Sub-national region (wave-specific codes); use as categorical only"),
    ("party_raw",              "party_raw",           "country-specific",         "n/a",        "all",   "Vote intention first choice (raw)"),
    ("party_recode",           "party_raw",           "AKP/CHP/MHP/HDP/IYI/other/pre_AKP_era/NaN", "n/a", "all", "Mapped per spec; -1/-2/2/5 -> NaN; WV2-4 -> pre_AKP_era; 792050 = IYI in WV7, 'other' in WV5"),
    # membership (binary + raw)
    ("member_org_church",      "member_org_church",   "0..2",            "more involved",       "WV3,5,6,7","Raw active/inactive code"),
    ("member_org_church_bin",  "member_org_church",   "0,1",             "member",              "WV3,5,6,7","1 if active or inactive member; WV4 missing battery"),
    ("member_org_sport",       "member_org_sport",    "0..2 (or 0/1 in WV2)","more involved",   "WV2,3,5,6,7","Raw membership code"),
    ("member_org_sport_bin",   "member_org_sport",    "0,1",             "member",              "WV2,3,5,6,7","Binary"),
    ("member_org_labour",      "member_org_labour",   "0..2 (or 0/1 in WV2)","more involved",   "WV2,3,5,6,7","Raw"),
    ("member_org_labour_bin",  "member_org_labour",   "0,1",             "member",              "WV2,3,5,6,7","Binary"),
    ("member_org_political_party","member_org_political_party","0..2 (or 0/1 in WV2)","more involved","WV2,3,5,6,7","Raw"),
    ("member_org_political_party_bin","member_org_political_party","0,1","member",              "WV2,3,5,6,7","Binary"),
    # justifiability + welzel
    ("justif_abortion",        "justif_abortion",     "1..10",           "more justifiable",    "WV2,5,6,7","WV3+WV4 missing in Turkey country files"),
    ("justif_divorce",         "justif_divorce",      "1..10",           "more justifiable",    "WV2,5,6,7","WV3+WV4 missing"),
    ("justif_homosex",         "justif_homosex",      "1..10",           "more justifiable",    "WV2,5,6,7","WV3+WV4 missing"),
    ("welzel_abortlib",        "welzel_abortlib",     "0..1 (9 steps)",  "more accepting",      "WV2,5,6,7","Welzel composite; WV3/WV4 have column but all NaN (raw justif missing)"),
    ("welzel_divorlib",        "welzel_divorlib",     "0..1 (9 steps)",  "more accepting",      "WV2,5,6,7","Welzel composite; WV3/WV4 have column but all NaN"),
    ("welzel_homolib",         "welzel_homolib",      "0..1 (9 steps)",  "more accepting",      "WV2,5,6,7","Welzel composite; WV3/WV4 have column but all NaN"),
    # child + neighbor (binary derived from raw 1=mentioned / 2=not mentioned)
    ("child_independence",     "child_independence",  "0,1",             "mentioned",           "all",   "1 if raw==1 (mentioned as important), 0 if raw==2 (not mentioned)"),
    ("child_obedience",        "child_obedience",     "0,1",             "mentioned",           "all",   "1 if raw==1 (mentioned as important), 0 if raw==2"),
    ("neighbor_immigrants",    "neighbor_immigrants", "0,1",             "would not want",      "all",   "1 if raw==1 (would NOT like as neighbour), 0 if raw==2"),
    ("neighbor_religion",      "neighbor_religion",   "0,1",             "would not want",      "WV4-WV7","1 if raw==1, 0 if raw==2; WV2/3 missing"),
]
manifest = pd.DataFrame(MANIFEST, columns=["col_name","concept","scale_range",
                                           "higher_means","waves_available","notes"])
manifest_path = os.path.join(RESULTS, "column_manifest_v2.csv")
manifest.to_csv(manifest_path, index=False)
print(f"\nSaved {manifest_path}  ({len(manifest)} rows)")

# Quick check: every analytical col in manifest also in pool?
analytical_cols = set(manifest["col_name"]) - {"wave","year","row_in_wave"}
missing_in_pool = analytical_cols - set(pool.columns)
extra_in_pool   = set(pool.columns) - set(manifest["col_name"])
if missing_in_pool:
    print(f"  !! manifest cols not in pooled data: {missing_in_pool}")
if extra_in_pool:
    print(f"  (cols in pool not in manifest: {sorted(extra_in_pool)})")
