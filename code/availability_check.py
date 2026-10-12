"""
Variable availability matrix for the brief's Section 9 predictor list.

Approach:
  1. LITERAL SEARCH (as the brief codes them, e.g. E069_02): search every
     wave's column var_name AND label for the exact code as substring.
     Country-specific WVS Turkey files use V/Q codes, not the standard
     A/B/C/D/E/F/X concept codes, so this returns almost nothing.
  2. RESOLVE BY MEANING: use the existing project crosswalk plus a label
     search to identify the wave-specific V/Q column that *implements*
     the concept. This is what we actually need for analysis.

Outputs availability_matrix.csv with: code, concept, WV2..WV7, notes.
"""
import os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WAVES = ["WV2", "WV3", "WV4", "WV5", "WV6", "WV7"]
invs = {w: pd.read_csv(os.path.join(ROOT, f"wave_columns_{w}.csv"))
        for w in WAVES}


# ---------- Literal-search audit (for transparency) -----------------------
LITERAL_CODES = ["E069_02","E069_06","E069_17","E069_07","E069_11",
                 "F034","F028","F063","E179WVS","E033",
                 "X025R","X003","X001","A170","X047_WVS"]
print("LITERAL-CODE SEARCH (var_name or label contains the code as substring)")
print("-" * 78)
print(f"{'code':<10}  " + "  ".join(f"{w:>8}" for w in WAVES))
for c in LITERAL_CODES:
    row = []
    for w in WAVES:
        inv = invs[w]
        hay = inv["var_name"].astype(str) + " || " + inv["label"].astype(str)
        n = hay.str.contains(c, case=False, regex=False).sum()
        row.append(str(n) if n else "-")
    print(f"{c:<10}  " + "  ".join(f"{v:>8}" for v in row))


# ---------- Resolve concept -> wave-specific V/Q codes --------------------
# Sources:
#  - confidence items, religion items, demographics, life satisfaction:
#    from existing WVS_TR_concept_crosswalk.csv (verified entries)
#  - Importance of God (F063), party preference (E179WVS), left-right (E033),
#    income (X047/X047_WVS): from label search just performed
#
# For X025R and X047_WVS the brief asks for the *recoded* form. If only the
# raw is present we mark MISSING in the matrix and note the raw fallback.

RESOLVED = {
    # ---- Outcomes (confidence items) ----
    "E069_02": {
        "concept": "Confidence: armed forces",
        "wv": {"WV2":"V273","WV3":"V136","WV4":"V148","WV5":"V132",
               "WV6":"V109","WV7":"Q65"},
        "notes": "",
    },
    "E069_06": {
        "concept": "Confidence: police",
        "wv": {"WV2":"V278","WV3":"V141","WV4":"V152","WV5":"V136",
               "WV6":"V113","WV7":"Q69"},
        "notes": "",
    },
    "E069_17": {
        "concept": "Confidence: courts / justice system",
        "wv": {"WV2":"V275","WV3":"V137","WV4":"MISSING","WV5":"V137",
               "WV6":"V114","WV7":"Q70"},
        "notes": "Not asked in Turkey WV4",
    },
    "E069_07": {
        "concept": "Confidence: parliament",
        "wv": {"WV2":"V279","WV3":"V144","WV4":"V155","WV5":"V140",
               "WV6":"V117","WV7":"Q73"},
        "notes": "",
    },
    "E069_11": {
        "concept": "Confidence: government",
        "wv": {"WV2":"V289","WV3":"V142","WV4":"V153","WV5":"V138",
               "WV6":"V115","WV7":"Q71"},
        "notes": "WV6 has V125_17 as alternate per existing crosswalk",
    },
    # ---- Religiosity ----
    "F034": {
        "concept": "Religious person (self-identification)",
        "wv": {"WV2":"V151","WV3":"V182","WV4":"V186","WV5":"V187",
               "WV6":"V147","WV7":"Q173"},
        "notes": "",
    },
    "F028": {
        "concept": "Religious attendance",
        "wv": {"WV2":"V147","WV3":"V181","WV4":"V185","WV5":"V186",
               "WV6":"V145","WV7":"Q171"},
        "notes": "",
    },
    "F063": {
        "concept": "Importance of God in life",
        "wv": {"WV2":"V176","WV3":"V190","WV4":"V196","WV5":"V192",
               "WV6":"V152","WV7":"Q164"},
        "notes": "",
    },
    # ---- Politics ----
    "E179WVS": {
        "concept": "Party preference (vote intention, first choice)",
        "wv": {"WV2":"V351","WV3":"V210","WV4":"V220","WV5":"V231",
               "WV6":"V228","WV7":"Q223"},
        "notes": ("Country-specific party codes; the WVS-harmonized recode "
                  "E179WVS is not present in country files, use V*_LOCAL / "
                  "Q223_LOCAL for raw Turkish parties."),
    },
    "E033": {
        "concept": "Self-positioning on left-right political scale",
        "wv": {"WV2":"V248","WV3":"V123","WV4":"V139","WV5":"V114",
               "WV6":"V95","WV7":"Q240"},
        "notes": "",
    },
    # ---- Demographics ----
    "X025R": {
        "concept": "Education (highest level attained, recoded 3 groups)",
        "wv": {"WV2":"V375R","WV3":"V217R","WV4":"V226R","WV5":"V238R",
               "WV6":"MISSING","WV7":"Q275R"},
        "notes": "WV6 lacks the 3-group recode; raw fallback V248",
    },
    "X003": {
        "concept": "Age",
        "wv": {"WV2":"V355","WV3":"V216","WV4":"V225","WV5":"V237",
               "WV6":"V242","WV7":"Q262"},
        "notes": "",
    },
    "X001": {
        "concept": "Sex",
        "wv": {"WV2":"V353","WV3":"V214","WV4":"V223","WV5":"V235",
               "WV6":"V240","WV7":"Q260"},
        "notes": "",
    },
    "A170": {
        "concept": "Life satisfaction",
        "wv": {"WV2":"V96","WV3":"V65","WV4":"V81","WV5":"V22",
               "WV6":"V23","WV7":"Q49"},
        "notes": "",
    },
    "X047_WVS": {
        "concept": "Income scale (recoded 10-step harmonized)",
        "wv": {"WV2":"V363R","WV3":"MISSING","WV4":"MISSING","WV5":"V253R",
               "WV6":"MISSING","WV7":"Q288R"},
        "notes": ("Recoded form available only WV2/WV5/WV7. Raw 'Scale of "
                  "incomes' equivalents: V363/V227/V236/V253/V239/Q288."),
    },
}

# Build the matrix
rows = []
for code, info in RESOLVED.items():
    row = {"code": code, "concept": info["concept"]}
    for w in WAVES:
        row[w] = info["wv"].get(w, "MISSING") or "MISSING"
    row["notes"] = info["notes"]
    rows.append(row)
mat = pd.DataFrame(rows, columns=["code","concept"] + WAVES + ["notes"])
mat.to_csv(os.path.join(ROOT, "availability_matrix.csv"), index=False)

# Verify resolved codes actually exist in each wave's column list
print("\n\nVERIFICATION (does the resolved V/Q code actually exist in the file?)")
print("-" * 78)
problems = []
for _, r in mat.iterrows():
    for w in WAVES:
        v = r[w]
        if v == "MISSING":
            continue
        names = set(invs[w]["var_name"].astype(str))
        if v not in names:
            problems.append((r["code"], w, v))
            print(f"  ! {r['code']:<10} {w}: '{v}' NOT FOUND in {w} columns")
if not problems:
    print("  OK — every non-MISSING entry exists as a column in its wave file.")

# Coverage summary
print("\n\nAVAILABILITY MATRIX")
print("=" * 100)
print(mat.to_string(index=False))

# Per-wave coverage count
print("\nCoverage (count of non-MISSING per wave):")
covered = (mat[WAVES] != "MISSING").sum()
print(covered.to_string())

print(f"\nSaved availability_matrix.csv  ({len(mat)} rows)")
