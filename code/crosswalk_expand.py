"""
Wave label inventory + concept coverage search.

Step 2: For each raw WVS Turkey wave file, write wave_columns_WV{N}.csv with
        (var_name, label). The xlsx column headers come as "V4: Important in
        life: Work" — we split on the FIRST colon to separate code from label.
        We also probe row-0 of the data body to detect any second header row;
        if found, prefer that as the label.

Step 3: For each concept keyword set, find matching (wave, var, label) and
        write concept_coverage.csv.
"""
import os, re, warnings
import pandas as pd

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
warnings.filterwarnings("ignore", category=FutureWarning)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WAVES = ["WV2", "WV3", "WV4", "WV5", "WV6", "WV7"]
FILES = {
    "WV2": "F00008272-WV2_Data_Turkey_Excel_v1.6.1.xlsx",
    "WV3": "F00008135-WV3_Data_Turkey_Excel_v20221107.1.xlsx",
    "WV4": "F00008022-WV4_Data_Turkey_Excel_v20201117.1.xlsx",
    "WV5": "F00007873-WV5_Data_Turkey_Excel_v20201117.1.xlsx",
    "WV6": "F00007629-WV6_Data_Turkey_2011_Excel_v20180912.xlsx",
    "WV7": "F00013222-WVS_Wave_7_Turkey_Excel_v5.1.xlsx",
}

# Pattern: WVS column header is "<CODE>: <LABEL>". Split on the FIRST colon.
def split_header(h: str):
    s = str(h).strip()
    if ":" in s:
        code, label = s.split(":", 1)
        return code.strip(), label.strip()
    return s, ""


# =========================================================================
# Step 2: per-wave column inventory
# =========================================================================
wave_inv = {}
for w in WAVES:
    path = os.path.join(ROOT, FILES[w])
    # read header + first row to detect if first data row is actually a label row
    head = pd.read_excel(path, nrows=1)
    cols = list(head.columns)
    first_row = head.iloc[0].tolist() if len(head) else []

    # Heuristic: if first data row is mostly non-numeric strings that look
    # like sentences (rare in WVS — values are usually integers), treat as label row.
    looks_like_label_row = False
    if first_row:
        n_str = sum(isinstance(v, str) and len(str(v)) > 6 for v in first_row)
        looks_like_label_row = n_str > 0.5 * len(first_row)

    rows = []
    for i, c in enumerate(cols):
        code, label = split_header(c)
        if looks_like_label_row and label == "":
            label = str(first_row[i]).strip()
        rows.append({"var_name": code, "label": label})

    inv = pd.DataFrame(rows)
    out = os.path.join(ROOT, f"wave_columns_{w}.csv")
    inv.to_csv(out, index=False)
    wave_inv[w] = inv
    print(f"{w}: {len(inv)} columns -> wave_columns_{w}.csv "
          f"(second-row labels used: {looks_like_label_row})")

print("\n--- WV4 first 30 (V-coded) ---")
print(wave_inv["WV4"].head(30).to_string(index=False))
print("\n--- WV7 first 30 (Q-coded) ---")
print(wave_inv["WV7"].head(30).to_string(index=False))


# =========================================================================
# Step 3: concept coverage search
#
# Each concept = list of (any-of) regex patterns. A column matches if its
# label OR var_name matches any pattern. All matches retained per wave.
# =========================================================================
CONCEPTS = {
    "important_in_life": [r"important in life"],
    "happiness":         [r"\bhappy\b", r"happiness", r"feeling of happiness"],
    "life_satisfaction": [r"satisfaction with (your )?life", r"life satisfaction",
                          r"satisfied with your life"],
    "income_financial":  [r"\bincome\b", r"financial", r"\bscale of incomes\b",
                          r"satisfaction with .*financial"],
    "social_class":      [r"social class"],
    "national_pride":    [r"national pride", r"\bproud\b", r"how proud"],
    "interpersonal_trust": [r"most people can be trusted",
                            r"interpersonal trust", r"people can be trusted",
                            r"\btrust(?!.*confidence)"],
    "democracy":         [r"democra"],
    "strong_leader":     [r"strong leader"],
    "left_right_scale":  [r"political.*\b(left|right|scale|self.placement)\b",
                          r"\b(left|right).*political",
                          r"self.position.*political", r"left.right"],
    "post_materialism":  [r"most important", r"post.?material",
                          r"aims of (this )?country", r"aim of (this )?country"],
    "justifiability":    [r"\bjustif"],
    "neighbors":         [r"\bneighbo[u]?r"],
    "child_qualities":   [r"child qualities", r"children should",
                          r"qualities.*children", r"important.*child"],
    "freedom_security":  [r"\bfreedom\b", r"\bsecurity\b"],
    "media_traditional": [r"\bmedia\b", r"television", r"newspaper",
                          r"\bradio\b", r"news source"],
    "internet":          [r"internet", r"e.mail", r"online", r"social media"],
    "immigration":       [r"immigra"],
    "environment":       [r"environment", r"pollut", r"climate"],
    "corruption":        [r"corrupt"],
}

rows = []
for concept, patterns in CONCEPTS.items():
    regex = re.compile("|".join(patterns), re.I)
    for w in WAVES:
        inv = wave_inv[w]
        haystack = (inv["var_name"].astype(str) + " :: "
                    + inv["label"].astype(str))
        hits = inv[haystack.str.contains(regex, na=False)]
        for _, r in hits.iterrows():
            rows.append({"concept": concept, "wave": w,
                         "var_name": r["var_name"], "label": r["label"]})

cov = pd.DataFrame(rows)
cov.to_csv(os.path.join(ROOT, "concept_coverage.csv"), index=False)
print(f"\nSaved concept_coverage.csv  ({len(cov)} rows)")

# Per-concept summary: hits per wave
print("\n=== Concept coverage matrix (count of matching columns per wave) ===")
mtx = (cov.groupby(["concept", "wave"]).size().unstack(fill_value=0)
          .reindex(columns=WAVES, fill_value=0)
          .reindex(index=list(CONCEPTS.keys())))
print(mtx.to_string())

# Show a peek per concept (first 2 hits per wave so the user can eyeball)
print("\n=== Sample matches per concept (first match per wave) ===")
for concept in CONCEPTS:
    sub = cov[cov["concept"] == concept]
    if sub.empty:
        print(f"\n[{concept}]   NO MATCHES")
        continue
    print(f"\n[{concept}]")
    for w in WAVES:
        ws = sub[sub["wave"] == w].head(1)
        if not ws.empty:
            r = ws.iloc[0]
            print(f"  {w}: {r['var_name']:<14} {r['label'][:110]}")
        else:
            print(f"  {w}: —")
