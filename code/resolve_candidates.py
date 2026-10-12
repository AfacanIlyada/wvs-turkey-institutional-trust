"""
Three-step concept resolution before final pooling pass.

Step 1: democracy canonical (Importance of democracy, 1-10 single item)
        in WV5/6/7.
Step 2: postmaterialism — prefer pre-computed Inglehart index Y002 if
        present; else raw aims-of-country battery (first/second choice).
Step 3: candidate_vars.csv — one row per (concept, wave). MULTIPLE-flag
        when more than one column plausibly matches.
"""
import os, re
import pandas as pd

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WAVES = ["WV2","WV3","WV4","WV5","WV6","WV7"]
invs  = {w: pd.read_csv(os.path.join(ROOT, f"wave_columns_{w}.csv"))
         for w in WAVES}


def find_rows(w, patterns, exclude=None):
    """All patterns (case-insensitive) must match label OR var_name.
    exclude is an optional regex; any matching row is dropped.
    Returns DataFrame slice with columns var_name, label."""
    inv = invs[w]
    hay = (inv["var_name"].astype(str) + " || "
           + inv["label"].astype(str))
    mask = pd.Series(True, index=inv.index)
    for p in patterns:
        mask &= hay.str.contains(p, case=False, regex=True, na=False)
    if exclude:
        mask &= ~hay.str.contains(exclude, case=False, regex=True, na=False)
    return inv.loc[mask, ["var_name", "label"]]


# =========================================================================
# Step 1: "Importance of democracy" — single 1-10 item
# =========================================================================
print("=" * 78)
print("Step 1: Importance of democracy (single 1-10 item)")
print("=" * 78)
DEMOC_PATTERNS = [
    r"\bimportance of democracy\b",
    r"how important.*live in a democracy",
]
for w in WAVES:
    hits = find_rows(w, [r"|".join(DEMOC_PATTERNS)])
    if hits.empty:
        # Broader fallback: any "democra" + "importan(t|ce)"
        hits = find_rows(w, [r"democra", r"importan"])
    label_str = f"{w}: "
    if hits.empty:
        print(f"{label_str}MISSING")
    else:
        for _, r in hits.iterrows():
            print(f"{label_str}{r.var_name:<10} {r.label}")
            label_str = "    "  # indent continuation rows


# =========================================================================
# Step 2: postmaterialism — Inglehart index Y002 if present, else
#         aims-of-country battery
# =========================================================================
print("\n" + "=" * 78)
print("Step 2: postmaterialism / Inglehart index / aims of country")
print("=" * 78)
for w in WAVES:
    print(f"\n--- {w} ---")
    # pre-computed index Y002 (literal code search)
    inv = invs[w]
    y002 = inv[inv["var_name"].astype(str).str.fullmatch(r"Y002\w*", na=False)]
    if not y002.empty:
        for _, r in y002.iterrows():
            print(f"  INDEX: {r.var_name:<10} {r.label}")
    # label-based pre-computed index search
    idx_hits = find_rows(w, [r"postmaterial|inglehart|materialist"])
    if not idx_hits.empty:
        for _, r in idx_hits.iterrows():
            if r.var_name not in y002["var_name"].values:
                print(f"  INDEX: {r.var_name:<10} {r.label}")
    # raw aims-of-country battery
    raw = find_rows(w, [r"most important.*aims|aims.*country|"
                        r"first choice.*important|second choice.*important|"
                        r"second most important"])
    if raw.empty:
        print(f"  (no raw aims-of-country items in label)")
    else:
        for _, r in raw.iterrows():
            print(f"  RAW:   {r.var_name:<10} {r.label}")


# =========================================================================
# Step 3: candidate_vars.csv
# =========================================================================
# Each concept: (description, AND-list-of-patterns, optional exclude regex)
CONCEPTS = {
    "interpersonal_trust": (
        "Most people can be trusted (A165)",
        [r"most people can be trusted"], None),
    "happiness": (
        "Feeling of happiness / taking things together",
        [r"feeling of happiness|taking all things together"], None),
    "financial_satisfaction": (
        "Satisfaction with financial situation of household",
        [r"satisf.*financial.*household|financial situation of household"],
        None),
    "strong_leader": (
        "Political system: having a strong leader",
        [r"strong leader"], None),
    "political_interest": (
        "How interested in politics / interest in politics",
        [r"interest.*polit|polit.*interest"], None),
    "marital_status": (
        "Marital status",
        [r"\bmarital status\b"], None),
    "region": (
        "Geographic region (not urban/rural)",
        [r"\bregion\b"], r"urban|rural|settlement|psu|town"),
    "social_class": (
        "Social class (subjective)",
        [r"social class"], None),
    "national_pride": (
        "How proud of nationality",
        [r"proud.*nation|how proud"], None),
    "civil_service": (
        "Confidence: civil services",
        [r"civil service"], None),
    "member_org_church": (
        "Membership: church / religious organization",
        [r"church", r"belong|member"], None),
    "member_org_sport": (
        "Membership: sport / recreational club",
        [r"sport|recreation", r"belong|member"], None),
    "member_org_labour": (
        "Membership: labour union",
        [r"labour|labor|union", r"belong|member"], None),
    "member_org_political_party": (
        "Membership: political party",
        [r"political part", r"belong|member"], None),
    "justif_abortion": (
        "Justifiable: Abortion",
        [r"justif", r"abortion"], None),
    "justif_divorce": (
        "Justifiable: Divorce",
        [r"justif", r"divorce"], None),
    "justif_homosex": (
        "Justifiable: Homosexuality",
        [r"justif", r"homosex"], None),
    "welzel_abortlib": (
        "Welzel ABORTLIB (WV4 substitute for justif_abortion)",
        [r"ABORTLIB"], None),
    "welzel_divorlib": (
        "Welzel DIVORLIB",
        [r"DIVORLIB"], None),
    "welzel_homolib": (
        "Welzel HOMOLIB",
        [r"HOMOLIB"], None),
    "child_independence": (
        "Important child qualities: independence",
        [r"child", r"independence"], None),
    "child_obedience": (
        "Important child qualities: obedience",
        [r"child", r"obedience"], None),
    "neighbor_immigrants": (
        "Neighbours: immigrants / foreign workers",
        [r"neighbo[u]?r|live next", r"immigr|foreign worker"], None),
    "neighbor_religion": (
        "Neighbours: different religion",
        [r"neighbo[u]?r|live next", r"different religion|other religion"],
        None),
    "freedom_control": (
        "Freedom of choice / control over own life",
        [r"freedom of choice|control over.*life|choice and control"], None),
}

rows = []
for cname, (descr, pats, excl) in CONCEPTS.items():
    for w in WAVES:
        hits = find_rows(w, pats, exclude=excl)
        if hits.empty:
            rows.append({"concept": cname, "wave": w,
                         "var_name": "MISSING", "label": "",
                         "notes": descr})
            continue
        if len(hits) == 1:
            r = hits.iloc[0]
            rows.append({"concept": cname, "wave": w,
                         "var_name": r.var_name, "label": r.label,
                         "notes": descr})
        else:
            # Multiple — pick the shortest var_name as canonical, list others
            ordered = hits.assign(_len=hits["var_name"].astype(str).str.len()
                                 ).sort_values("_len")
            top = ordered.iloc[0]
            others = [f"{r.var_name}: {r.label[:60]}"
                      for _, r in ordered.iloc[1:].iterrows()]
            note = f"{descr} | MULTIPLE ({len(hits)}): also " \
                   + " ; ".join(others)
            rows.append({"concept": cname, "wave": w,
                         "var_name": top.var_name, "label": top.label,
                         "notes": note})

cands = pd.DataFrame(rows, columns=["concept","wave","var_name","label","notes"])
cands.to_csv(os.path.join(ROOT, "candidate_vars.csv"), index=False)
print(f"\n\nSaved candidate_vars.csv ({len(cands)} rows)")

# Coverage summary
print("\n=== Coverage (non-MISSING per concept) ===")
covered = (cands[cands["var_name"] != "MISSING"]
           .groupby("concept").size().reindex(list(CONCEPTS.keys()),
                                              fill_value=0))
multi = (cands["notes"].str.contains("MULTIPLE", na=False)
         .groupby(cands["concept"]).sum()
         .reindex(list(CONCEPTS.keys()), fill_value=0))
summary = pd.DataFrame({"covered_in_n_waves": covered,
                        "waves_with_multi": multi.astype(int)})
print(summary.to_string())

# Show every concept resolution per wave
print("\n=== Per-concept-per-wave picks ===")
for c in CONCEPTS:
    print(f"\n[{c}]")
    sub = cands[cands["concept"] == c]
    for _, r in sub.iterrows():
        flag = "  ⚠MULTI" if "MULTIPLE" in str(r.notes) else ""
        print(f"  {r.wave}: {r.var_name:<14} {str(r.label)[:90]}{flag}")
