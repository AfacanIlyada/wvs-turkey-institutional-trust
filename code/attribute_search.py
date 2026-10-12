"""
Concept search across wave_columns_WV{N}.csv. Each search term is one or
more regex patterns; AND means all must match the same column's label or
var_name (case-insensitive). Writes attribute_search.csv with one row per
hit, plus prints per-term hit counts.
"""
import os, re
import pandas as pd

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WAVES = ["WV2","WV3","WV4","WV5","WV6","WV7"]

invs = {w: pd.read_csv(os.path.join(ROOT, f"wave_columns_{w}.csv"))
        for w in WAVES}

# Each entry: term_key -> list of regex patterns (AND across patterns)
SEARCHES = {
    "1_interpersonal_trust":
        [r"most people can be trusted|people can be trusted"],
    "2_postmaterialism":
        [r"postmaterial|most important.*country|aims of country"],
    "3_strong_leader":
        [r"strong.*leader|strong leader"],
    "4_democracy_pref_suit_imp":
        [r"democra", r"prefer|suitable|important"],
    "5_marital_status":
        [r"\bmarital\b|\bmarried\b"],
    "6_region_province":
        [r"\bregion\b|\bprovince\b"],
    "7_civil_service":
        [r"civil service|civil servants"],
    "8_political_interest":
        [r"follow.*politic|interest.*politic|politic.*interest"],
    "9_member_org":
        [r"\bmember", r"organization|association|\bgroup\b"],
    "10_financial_satisfaction":
        [r"satisfy.*financ|financ.*satisf|household.*financ"],
    "11_freedom_control_life":
        [r"control.*life|choice.*control|freedom.*choice"],
    "12_national_pride":
        [r"proud.*country|national.*proud|proud.*nation"],
    "13_media_news":
        [r"newspaper|television|\btv\b|\bnews\b"],
    "14_child_independence":
        [r"\bindependence\b", r"child|quality|important"],
    "15_child_obedience":
        [r"\bobedience\b", r"child|quality|important"],
    "16_other_child_qualities":
        [r"autonomous|imagination|unselfishness"],
    "17_justifiability":
        [r"justif"],
    "18_homosexual":
        [r"homosexual|\bgay\b|same.?sex"],
    "19_abortion":
        [r"abort"],
    "20_neighbors":
        [r"neighbo[u]?r|live next"],
    "21_happiness":
        [r"\bhappy\b|happiness"],
    "22_religion_important_in_life":
        [r"important in life.*religion|religion.*important in life"],
    "23_interpersonal_trust_v2":
        [r"trust.*people|interpersonal"],
    "24_social_class":
        [r"social class|class.*belong|belong.*class"],
    "25_income_scale":
        [r"income.*scale|scale.*income|household.*income"],
}


def match(haystack: pd.Series, patterns):
    """All patterns must match (case-insensitive) for a row to be a hit."""
    mask = pd.Series(True, index=haystack.index)
    for p in patterns:
        m = haystack.str.contains(p, case=False, regex=True, na=False)
        mask &= m
    return mask


rows = []
counts = []
for term, patterns in SEARCHES.items():
    total = 0
    for w in WAVES:
        inv = invs[w]
        hay = inv["var_name"].astype(str) + " || " + inv["label"].astype(str)
        m = match(hay, patterns)
        for _, r in inv[m].iterrows():
            rows.append({"search_term": term, "wave": w,
                         "var_name": r["var_name"], "label": r["label"]})
        total += int(m.sum())
    counts.append((term, total))

out = pd.DataFrame(rows, columns=["search_term","wave","var_name","label"])
out.to_csv(os.path.join(ROOT, "attribute_search.csv"), index=False)
print(f"Saved attribute_search.csv ({len(out)} rows)")

print("\nHit counts per term (across all 6 waves):")
print(f"{'term':<40} {'total':>6}")
print("-" * 50)
for t, n in counts:
    flag = "  <-- ZERO" if n == 0 else ""
    print(f"{t:<40} {n:>6}{flag}")

# Per-term per-wave breakdown
print("\nHits per term × wave:")
mtx = (out.groupby(["search_term","wave"]).size().unstack(fill_value=0)
          .reindex(index=list(SEARCHES.keys()))
          .reindex(columns=WAVES, fill_value=0))
print(mtx.to_string())
