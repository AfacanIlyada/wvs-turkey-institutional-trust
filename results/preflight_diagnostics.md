# Preflight diagnostics — WVS Turkey (SDL 2026)

Read-only session, 2026-07-16. No model fit or re-fit; no existing file modified; this report is the only new file. Numbers were read from files on disk or computed by loading `results/pooled_extended_v2.csv` and applying **subsetting only** (the sample-filter logic of the named scripts, replicated verbatim). Notebook cell indices are 0-based positions in the .ipynb JSON (markdown cells counted), matching the numbering used in `results/deck_numbers.md`.

## VERDICTS

1. **WEIGHTS: PARTIALLY PRESENT IN SOURCE** — non-constant respondent-level calibration weights exist in the source files for WV3 (`V236`/`V236A`), WV4 (`V245`/`V245A`), WV5 (`V259`/`V259A`, also `S019`), WV6 (`V258`/`V258A`); WV2 (`V376`) and WV7 (`W_WEIGHT`) are constant = 1.0 in the Turkey release. None was ever selected by the build script (never dropped — never requested). PSU identifier exists only in WV7 (`I_PSU`).
2. **WV4 non-religious n in the army analytic sample = 540**, and smallest conf_military cell within it = **32** (WV4 × not-religious × response level 2).
3. **Largest single source of attrition = `left_right`**, costing n = 782 in the script-order decomposition (737 rows missing it and nothing else), present in all six waves, largest counts in WV7 (170 sole-missing) and WV5 (163; WV5 is the hardest-hit wave relative to its size). The 8,915 → 8,777 step is `conf_parliament` (−67) then `conf_government` (−71, of which 43 in WV2).
4. **PLACEBO SEs: REFIT REQUIRED** — no SE, exact p, z, or CI for the full-sample parliament/government/civil_service models exists anywhere on disk; recoverable are coefficients at 3 dp + stars (`final_checks.ipynb` cells 4–5; `results/deck_fig_main.csv`), model n's (cell 3), and — only for the n=8,777 common-sample trio at WV5 — coef + SE for parliament and government (cell 15).
5. **Third measure = `rel_attendance`** ("Religious attendance frequency", 1–8, fielded in all six waves); used as a **control** in layer3_ordinal_regressions.py, layer4_pooled_interactions.py, layer4b_longwindow.py, pressure_tests.py, education_defense.ipynb, moderator_scan.ipynb, final_checks.ipynb; **never used as a religiosity grouping/split measure** in any file.

---

## 1. Survey weights

### 1a. Source files read by the build

`pooled_extended_v2.csv` is built by `pool_final.py` alone. Its `FILES` dict ([pool_final.py:23-30](../pool_final.py)) reads exactly these six workbooks:

| wave | source file |
|---|---|
| WV2 | `F00008272-WV2_Data_Turkey_Excel_v1.6.1.xlsx` |
| WV3 | `F00008135-WV3_Data_Turkey_Excel_v20221107.1.xlsx` |
| WV4 | `F00008022-WV4_Data_Turkey_Excel_v20201117.1.xlsx` |
| WV5 | `F00007873-WV5_Data_Turkey_Excel_v20201117.1.xlsx` |
| WV6 | `F00007629-WV6_Data_Turkey_2011_Excel_v20180912.xlsx` |
| WV7 | `F00013222-WVS_Wave_7_Turkey_Excel_v5.1.xlsx` |

The `cluster` column is merged in from `results/pooled_with_clusters.csv` ([pool_final.py:302-305](../pool_final.py)), whose ancestry (`column_inventory.py`, `trust_clusters.py`, reading `results/pooled_all_scales.csv`) also loads the xlsx files with explicit `usecols` lists — no weight column enters at any point. Confirmed: the 54 columns of `pooled_extended_v2.csv` contain no weight variable (full column list checked).

### 1b–1c. Weight-pattern columns in the source files

Patterns searched (case-insensitive, on the full "CODE: label" header): `S016, S017, S017A, S018, S019, W_WEIGHT, PWGHT, GWGHT, WEIGHT, WGHT, AGIR/AĞIR`. **`S016`, `S017`, `S017A`, `GWGHT` appear in no file.** All columns below are 100% non-null (non-null = full wave n). "Constant" = one unique value within the wave file.

**Survey/calibration weights:**

| wave | column (header) | n | min | max | mean | n_unique | constant within wave |
|---|---|---:|---:|---:|---:|---:|---|
| WV2 | `V376: Weight` | 1,030 | 1.0 | 1.0 | 1.0 | 1 | YES (≡1) |
| WV2 | `S018: Equilibrated weight-1000` | 1,030 | 0.970874 | 0.970874 | 0.970874 | 1 | YES |
| WV2 | `S019: Equilibrated weight-1500` | 1,030 | 1.45631 | 1.45631 | 1.45631 | 1 | YES |
| WV3 | `V236: Callibration weight` | 1,907 | 0.17862 | 5.35813 | 1.00021 | 48 | **NO** |
| WV3 | `V236A: Weight [with split ups]` | 1,907 | 0.17862 | 5.35813 | 1.00021 | 48 | **NO** (same distribution as V236) |
| WV3 | `S018: Equilibrated weight-1000` | 1,907 | 0.524384 | 0.524384 | 0.524384 | 1 | YES |
| WV4 | `V245: Calibration weights` | 3,401 | 0.316257 | 5.53614 | 1.00014 | 57 | **NO** |
| WV4 | `V245A: Weight [with split ups]` | 3,401 | 0.316257 | 5.53614 | 1.00014 | 57 | **NO** (same distribution as V245) |
| WV4 | `S018: Equilibrated weight-1000` | 3,401 | 0.294031 | 0.294031 | 0.294031 | 1 | YES |
| WV5 | `V259: Calibration weights` | 1,346 | 0.701417 | 1.73134 | 1.0000 | 24 | **NO** |
| WV5 | `V259A: Calibration weights [with split ups]` | 1,346 | 0.701417 | 1.73134 | 1.0000 | 24 | **NO** (same distribution as V259) |
| WV5 | `S018: Equilibrated weight-1000` | 1,346 | 0.742942 | 0.742942 | 0.742942 | 1 | YES |
| WV5 | `S019: Equilibrated weight-1500` | 1,346 | 0.781668 | 1.92943 | 1.11441 | 24 | **NO** |
| WV6 | `V258: Weight` | 1,605 | 0.656034 | 2.11325 | 1.0000 | 10 | **NO** |
| WV6 | `V258A: Weight with split ups` | 1,605 | 0.656034 | 2.11325 | 1.0000 | 10 | **NO** (same distribution as V258) |
| WV7 | `W_WEIGHT: Weight` | 2,415 | 1.0 | 1.0 | 1.0 | 1 | YES (≡1) |
| WV7 | `S018: Equilibration weight-1000` | 2,415 | 0.414079 | 0.414079 | 0.414079 | 1 | YES |
| WV7 | `PWGHT: Population size weight` | 2,415 | 34,095.2 | 34,095.2 | 34,095.2 | 1 | YES |

WV6 carries no `S018`/`S019` (its only S0xx columns are `S024`, `S025`). The constant `S018`/`S019`/`PWGHT` values are wave-level scaling factors (sample-size/population equilibration); they carry no within-wave information.

**Welzel values-index construction weights** (matched the "weight" pattern; these weight *items within the secular/emancipative values composites*, not respondents — listed for completeness):

| wave | column | min | max | mean | n_unique | constant |
|---|---|---:|---:|---:|---:|---|
| WV2 | `SECVALWGT` | 0.66 | 1.0 | 0.959728 | 5 | no |
| WV2 | `RESEMAWEIGHT` | 0.745 | 0.915 | 0.901879 | 3 | no |
| WV2 | `WEIGHT1A` / `WEIGHT2A` / `WEIGHT3A` / `WEIGHT4A` | 0.66 | 1.0 | 0.973922 / 0.883146 / 0.994058 / 0.987786 | 2 each | no |
| WV2 | `WEIGHT1B` / `WEIGHT2B` | 1.0 / 0.66 | 1.0 / 0.66 | 1.0 / 0.66 | 1 each | YES |
| WV2 | `WEIGHT3B` / `WEIGHT4B` | 0.66 | 1.0 | 0.987126 / 0.960388 | 2 each | no |
| WV3 | `SACSECWGT` | 0.66 | 0.915 | 0.886652 | 4 | no |
| WV3 | `RESEMAWEIGHT` | 0.745 | 0.915 | 0.905372 | 3 | no |
| WV4 | `SECVALWGT` | 0.66 | 0.83 | 0.823277 | 3 | no |
| WV4 | `RESEMAWEIGHT` | 0.745 | 0.915 | 0.907802 | 3 | no |
| WV4 | `WEIGHT1A` / `WEIGHT2A` / `WEIGHT2B` / `WEIGHT4B` | 0.66 | 1.0 | 0.987404 / 0.985704 / 0.985104 / 0.986104 | 2 each | no |
| WV4 | `WEIGHT3A` / `WEIGHT4A` / `WEIGHT3B` (≡0.66); `WEIGHT1B` (≡1.0) | — | — | — | 1 each | YES |
| WV5 | `SECVALWGT` / `WEIGHTB` | 0.745 | 1.0 | 0.978782 / 0.988507 | 4 each | no |
| WV5 | `WEIGHT1A`–`WEIGHT4A` | 0.66 | 1.0 | 0.943923 / 0.989391 / 0.994695 / 0.987117 | 2 each | no |
| WV5 | `WEIGHT1B` (≡1.0) | 1.0 | 1.0 | 1.0 | 1 | YES |
| WV5 | `WEIGHT2B` / `WEIGHT3B` / `WEIGHT4B` | 0.66 | 1.0 | 0.978782 / 0.985854 / 0.989391 | 2 each | no |
| WV6 | `SECVALWGT` / `WEIGHTB` | 0.745 | 1.0 | 0.98533 / 0.989938 | 4 each | no |
| WV6 | `WEIGHT1A`–`WEIGHT4A` | 0.66 | 1.0 | 0.967165 / 0.989408 / 0.999153 / 0.985595 | 2 each | no |
| WV6 | `WEIGHT1B` (≡1.0) | 1.0 | 1.0 | 1.0 | 1 | YES |
| WV6 | `WEIGHT2B` / `WEIGHT3B` / `WEIGHT4B` | 0.66 | 1.0 | 0.986231 / 0.988561 / 0.98496 | 2 each | no |
| WV7 | `SECVALWGT` / `RESEMAVALWGT` | 0.66 | 1.0 | 0.977791 / 0.978424 | 5 each | no |
| WV7 | `SECVALBWGT` / `RESEMAVALBWGT` | 0.66 | 1.0 | 0.961636 / 0.985217 | 3 each | no |
| WV7 | `WEIGHT1A`–`WEIGHT4A` | 0.66 | 1.0 | 0.970294 / 0.952977 / 0.994369 / 0.993524 | 2 each | no |
| WV7 | `WEIGHT1B`–`WEIGHT4B` | 0.66 | 1.0 | 0.952555 / 0.983246 / 0.987188 / 0.990708 | 2 each | no |

### 1d. Build-script handling: never selected, not explicitly dropped

`pool_final.py` loads only the columns named in its crosswalk; there is no drop statement for weights anywhere. Selection logic ([pool_final.py:172-193](../pool_final.py)):

```python
def load_wave(w):
    """Load one wave with all crosswalk-v3 concepts; rename to concept names."""
    ...
    for _, r in xwalk.iterrows():
        code = r[w]
        if code == "MISS":
            continue
        if code in hm:
            want_full.append(hm[code]); want_concept.append(r["concept"])
        ...
    df = pd.read_excel(path, usecols=want_full)     # line 187 — only crosswalk codes are ever read
```

The crosswalk `ROWS` block ([pool_final.py:37-138](../pool_final.py)) contains no weight concept. `grep -in "weight|wght|S017|S018|S016|S019|psu|strat"` over `pool_final.py`, `pool_extended.py`, `column_inventory.py`, `trust_clusters.py` returns **zero weight-related matches** (only false positives: `fontweight` in trust_clusters.py:414; a phase-0 search regex containing "psu" in resolve_candidates.py:117). The earlier builds use the same `usecols` pattern (`pool_extended.py:100`, `column_inventory.py:72`, `trust_clusters.py:86`).

The handoff statement "Survey weights: not available in the dataset" (`results/partner_handoff_v2.md:101`) is accurate for `pooled_extended_v2.csv` but **not for the WV3–WV6 source files**.

### 1e. Design variables (PSU / cluster / stratum / settlement)

Patterns searched: `PSU, CLUSTER, STRAT*, SETTLEMENT, SAMPLING, TOWN, URBAN, RURAL, REGION, X049` ("demonstrations" false positives excluded).

| wave | design variables present in source | notes |
|---|---|---|
| WV2 | `V370: Region where the interview was conducted`, `N_REGION_ISO` | no PSU/stratum; V370 selected into pooled as `region` |
| WV3 | `V234: Region`, `N_REGION_ISO` | no PSU/stratum; V234 → `region` |
| WV4 | `REGION_ISO: Region ISO` | no PSU/stratum; → `region` |
| WV5 | `V257: Region where the interview was conducted`, `N_REGION_ISO` | no PSU/stratum; V257 → `region` |
| WV6 | `V253: Size of town`, `V253_CS: Size of town (country specific)`, `V256`/`V256B`/`V256C: Region (levels 1–3)` | no PSU/stratum; V256 → `region`; town size never selected |
| WV7 | `I_PSU: Primary Sampling Unit ID` (n=2,415 non-null, **201 unique PSUs**, codes 1–203), `G_TOWNSIZE` (8 groups), `G_TOWNSIZE2` (5 groups), `H_SETTLEMENT` (4 types), `H_URBRURAL`, `N_REGION_ISO`, `N_REGION_WVS` | only wave with a PSU identifier; only `N_REGION_WVS` → `region` was selected |

No stratum identifier in any wave. `S016` absent from all six files.

**Verdict: PARTIALLY PRESENT** — non-constant calibration weights in source for **WV3 (V236/V236A), WV4 (V245/V245A), WV5 (V259/V259A + S019), WV6 (V258/V258A)**; WV2 (V376) and WV7 (W_WEIGHT) constant ≡ 1.0, so weighted = unweighted for those two waves by construction. PSU only in WV7.

---

## 2. Non-religious cell counts

`not_religious_dummy` derived exactly as [layer4b_longwindow.py:37-38](../layer4b_longwindow.py): `rel_person` 2/3 → 1, 1 → 0, else NaN. All tables computed from `results/pooled_extended_v2.csv`.

### 2a. not_religious_dummy × wave — full pooled file (n = 11,704)

Raw n:

| nr | WV2 | WV3 | WV4 | WV5 | WV6 | WV7 | total |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 (religious) | 747 | 1,091 | 2,602 | 1,084 | 1,314 | 1,593 | 8,431 |
| 1 (not religious) | 255 | 362 | 718 | 237 | 261 | 615 | 2,448 |
| missing | 28 | 454 | 81 | 25 | 30 | 207 | 825 |
| wave total | 1,030 | 1,907 | 3,401 | 1,346 | 1,605 | 2,415 | 11,704 |

Column % (share of wave):

| nr | WV2 | WV3 | WV4 | WV5 | WV6 | WV7 |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 72.52 | 57.21 | 76.51 | 80.53 | 81.87 | 65.96 |
| 1 | 24.76 | 18.98 | 21.11 | 17.61 | 16.26 | 25.47 |
| missing | 2.72 | 23.81 | 2.38 | 1.86 | 1.87 | 8.57 |

Row % (share of category across waves):

| nr | WV2 | WV3 | WV4 | WV5 | WV6 | WV7 |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 8.86 | 12.94 | 30.86 | 12.86 | 15.59 | 18.89 |
| 1 | 10.42 | 14.79 | 29.33 | 9.68 | 10.66 | 25.12 |
| missing | 3.39 | 55.03 | 9.82 | 3.03 | 3.64 | 25.09 |

### 2b. Same cross-tab in the layer4b **army analytic sample**

Filter replicated from layer4b_longwindow.py (subsetting only): (i) `df.dropna(subset=["cluster"])` (line 35) → 11,311 rows; (ii) listwise `dropna()` over `[conf_military] + PREDICTORS_BASE` (lines 57-60), i.e. non-missing on conf_military, not_religious_dummy, rel_attendance, rel_importance_god, left_right, age, female, education_raw, income_raw, married_dummy (wave dummies never missing; interactions missing only where the nr dummy is). **Resulting n = 8,915 — confirmed**, equal to `layer4b_longwindow_interactions.csv` `n_obs` and `final_checks.ipynb` cell 3 output ("fitted conf_military n=8915").

Raw n:

| nr | WV2 | WV3 | WV4 | WV5 | WV6 | WV7 | total |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 559 | 938 | 2,129 | 866 | 1,103 | 1,303 | 6,898 |
| 1 | 200 | 328 | **540** | 198 | 224 | 527 | 2,017 |
| wave total | 759 | 1,266 | 2,669 | 1,064 | 1,327 | 1,830 | 8,915 |

Column %: nr = 26.35 / 25.91 / 20.23 / 18.61 / 16.88 / 28.80 by wave. Row % (nr row): 9.92 / 16.26 / 26.77 / 9.82 / 11.11 / 26.13. (Missing category: zero by construction.)

### 2c. Three-way: not_religious_dummy × wave × conf_military, army analytic sample (n = 8,915)

conf_military levels 1–4 (reverse-coded, 4 = a great deal):

| wave | nr | 1 | 2 | 3 | 4 |
|---|---|---:|---:|---:|---:|
| WV2 | 0 | **3** | 18 | 159 | 379 |
| WV2 | 1 | 11 | 27 | 90 | 72 |
| WV3 | 0 | 14 | 33 | 230 | 661 |
| WV3 | 1 | 14 | 29 | 124 | 161 |
| WV4 | 0 | 125 | 122 | 478 | 1,404 |
| WV4 | 1 | 58 | **32** | 150 | 300 |
| WV5 | 0 | 38 | 74 | 178 | 576 |
| WV5 | 1 | 21 | 25 | 42 | 110 |
| WV6 | 0 | 96 | 155 | 331 | 521 |
| WV6 | 1 | 33 | 49 | 73 | 69 |
| WV7 | 0 | 24 | 133 | 487 | 659 |
| WV7 | 1 | 24 | 58 | 230 | 215 |

Cells with n < 10: **one** — WV2 × religious × level 1 (n = 3). All WV4 cells ≥ 32. Smallest cell inside the WV4 non-religious row: 32 (level 2).

### 2d. Same three-way for conf_police and conf_courts

**conf_police within the army analytic sample (n = 8,915; "MISS" = conf_police missing on those rows):**

| wave | nr | 1 | 2 | 3 | 4 | MISS |
|---|---|---:|---:|---:|---:|---:|
| WV2 | 0 | 49 | 115 | 199 | 194 | 2 |
| WV2 | 1 | 61 | 57 | 58 | 23 | 1 |
| WV3 | 0 | 96 | 139 | 394 | 306 | 3 |
| WV3 | 1 | 95 | 70 | 109 | 53 | 1 |
| WV4 | 0 | 286 | 264 | 723 | 846 | 10 |
| WV4 | 1 | 155 | 88 | 154 | 139 | 4 |
| WV5 | 0 | 69 | 135 | 312 | 348 | 2 |
| WV5 | 1 | 42 | 62 | 62 | 32 | 0 |
| WV6 | 0 | 92 | 149 | 405 | 454 | 3 |
| WV6 | 1 | 44 | 61 | 76 | 42 | 1 |
| WV7 | 0 | 36 | 134 | 588 | 544 | 1 |
| WV7 | 1 | 33 | 75 | 260 | 157 | 2 |

No cell < 10. Smallest: 23 (WV2 × nr × level 4). In the police model's **own** analytic sample (same filter with conf_police as outcome; n = 8,911, matches final_checks cell 3), counts differ by ≤ 4 per cell and the smallest cell is the same 23; no cell < 10.

**conf_courts within the army analytic sample (n = 8,915):**

| wave | nr | 1 | 2 | 3 | 4 | MISS |
|---|---|---:|---:|---:|---:|---:|
| WV2 | 0 | 52 | 117 | 209 | 179 | 2 |
| WV2 | 1 | 32 | 71 | 68 | 28 | 1 |
| WV3 | 0 | 108 | 158 | 363 | 302 | 7 |
| WV3 | 1 | 48 | 86 | 140 | 54 | 0 |
| WV4 | 0 | 0 | 0 | 0 | 0 | **2,129** |
| WV4 | 1 | 0 | 0 | 0 | 0 | **540** |
| WV5 | 0 | 64 | 135 | 329 | 328 | 10 |
| WV5 | 1 | 29 | 54 | 75 | 39 | 1 |
| WV6 | 0 | 103 | 195 | 455 | 346 | 4 |
| WV6 | 1 | 39 | 68 | 74 | 43 | 0 |
| WV7 | 0 | 71 | 211 | 638 | 382 | 1 |
| WV7 | 1 | 46 | 124 | 297 | 60 | 0 |

WV4 rows are all-missing (item not fielded in 2001 — consistent with `findings_summary.md` and `project_audit.md` §2). In the courts model's **own** analytic sample (n = 6,231, matches final_checks cell 3; WV4 absent entirely), no cell < 10; smallest = 28 (WV2 × nr × level 4):

| wave | nr | 1 | 2 | 3 | 4 |
|---|---|---:|---:|---:|---:|
| WV2 | 0 | 52 | 117 | 209 | 179 |
| WV2 | 1 | 32 | 71 | 68 | **28** |
| WV3 | 0 | 108 | 158 | 363 | 302 |
| WV3 | 1 | 49 | 86 | 140 | 54 |
| WV5 | 0 | 64 | 136 | 332 | 328 |
| WV5 | 1 | 29 | 54 | 75 | 39 |
| WV6 | 0 | 105 | 195 | 457 | 346 |
| WV6 | 1 | 39 | 69 | 74 | 43 |
| WV7 | 0 | 72 | 211 | 638 | 382 |
| WV7 | 1 | 46 | 124 | 297 | 60 |

### 2e. rel_importance_god low-cut (≤ 7) variant

Coding replicated from `final_checks.ipynb` cell 8: `nr_god = int(rel_importance_god <= 7)`; cut matches `layer1_by_religiosity.py` lines 25-35 ("low = 1-7"). Analytic sample = cluster filter + listwise on `[conf_military] + PRED_GOD` (rel_importance_god removed from controls, per cell 8): **n = 9,082 — matches cell 8's printed n**.

nr_god × wave, full pooled file (n = 11,704):

| nr_god | WV2 | WV3 | WV4 | WV5 | WV6 | WV7 | total |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 (god 8–10) | 842 | 1,290 | 2,963 | 1,212 | 1,388 | 1,573 | 9,268 |
| 1 (god ≤ 7) | 184 | 177 | **422** | 127 | 186 | 825 | 1,921 |
| missing | 4 | 440 | 16 | 7 | 31 | 17 | 515 |

nr_god × wave, god-variant analytic sample (n = 9,082):

| nr_god | WV2 | WV3 | WV4 | WV5 | WV6 | WV7 | total |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 637 | 1,118 | 2,395 | 972 | 1,183 | 1,255 | 7,560 |
| 1 | 138 | 157 | **314** | 102 | 156 | 655 | 1,522 |

Three-way nr_god × wave × conf_military, god-variant analytic sample:

| wave | nr_god | 1 | 2 | 3 | 4 |
|---|---|---:|---:|---:|---:|
| WV2 | 0 | **3** | 24 | 193 | 417 |
| WV2 | 1 | 12 | 26 | 63 | 37 |
| WV3 | 0 | 16 | 46 | 289 | 767 |
| WV3 | 1 | 12 | 16 | 69 | 60 |
| WV4 | 0 | 138 | 132 | 540 | 1,585 |
| WV4 | 1 | 49 | **25** | 99 | 141 |
| WV5 | 0 | 46 | 84 | 199 | 643 |
| WV5 | 1 | 13 | 17 | 21 | 51 |
| WV6 | 0 | 108 | 178 | 368 | 529 |
| WV6 | 1 | 23 | 27 | 43 | 63 |
| WV7 | 0 | 32 | 90 | 440 | 693 |
| WV7 | 1 | 19 | 105 | 305 | 226 |

Cells with n < 10: one — WV2 × nr_god=0 × level 1 (n = 3), same cell as the headline measure. Comparison of the WV4 non-religious cell: god-cut **smaller** — 314 vs 540 in the analytic samples (422 vs 718 full-file); smallest WV4 nr cell 25 vs 32. (WV7 reverses: nr_god 655 vs nr 527.)

**Verdict: WV4 non-religious n in the army analytic sample = 540; smallest conf_military cell within it = 32 (level 2).**

---

## 3. Missingness accounting: 11,704 → 8,915 → 8,777

### 3a. Per-variable missingness by wave, full pooled file (n missing / % of wave)

Source: `results/pooled_extended_v2.csv`. The layer4b spec ([layer4b_longwindow.py:48-54](../layer4b_longwindow.py)) contains conf_military (outcome), not_religious_dummy, rel_attendance, rel_importance_god, left_right, age, female, education_raw, income_raw, married_dummy + wave dummies/interactions; `cluster` acts as a pre-filter (line 35). The other five confidence items are outcomes of the placebo/parallel models; **party_recode is NOT in the layer4b spec** (listed because requested; layer3 uses it, layer4b does not).

| variable | WV2 | WV3 | WV4 | WV5 | WV6 | WV7 | total n (%) |
|---|---|---|---|---|---|---|---|
| conf_military | 14 (1.4) | 25 (1.3) | 49 (1.4) | 18 (1.3) | 35 (2.2) | 25 (1.0) | 166 (1.4) |
| conf_police | 19 (1.8) | 31 (1.6) | 51 (1.5) | 23 (1.7) | 21 (1.3) | 18 (0.7) | 163 (1.4) |
| conf_courts | 23 (2.2) | 41 (2.1) | 3,401 (100.0) | 31 (2.3) | 47 (2.9) | 27 (1.1) | 3,570 (30.5) |
| conf_parliament | 45 (4.4) | 66 (3.5) | 82 (2.4) | 68 (5.1) | 62 (3.9) | 67 (2.8) | 390 (3.3) |
| conf_government | 122 (11.8) | 46 (2.4) | 59 (1.7) | 42 (3.1) | 41 (2.6) | 39 (1.6) | 349 (3.0) |
| conf_civil_service | 26 (2.5) | 46 (2.4) | 70 (2.1) | 57 (4.2) | 64 (4.0) | 68 (2.8) | 331 (2.8) |
| rel_person (= not_religious_dummy) | 28 (2.7) | 454 (23.8) | 81 (2.4) | 25 (1.9) | 30 (1.9) | 207 (8.6) | 825 (7.0) |
| rel_attendance | 13 (1.3) | 476 (25.0) | 74 (2.2) | 25 (1.9) | 25 (1.6) | 196 (8.1) | 809 (6.9) |
| rel_importance_god | 4 (0.4) | 440 (23.1) | 16 (0.5) | 7 (0.5) | 31 (1.9) | 17 (0.7) | 515 (4.4) |
| left_right | 132 (12.8) | 147 (7.7) | 151 (4.4) | 203 (15.1) | 152 (9.5) | 264 (10.9) | 1,049 (9.0) |
| age | 6 (0.6) | 13 (0.7) | 4 (0.1) | 0 | 0 | 1 (0.0) | 24 (0.2) |
| female | 0 | 0 | 0 | 0 | 0 | 0 | 0 (0.0) |
| education_raw | 70 (6.8) | 41 (2.1) | 234 (6.9) | 0 | 0 | 9 (0.4) | 354 (3.0) |
| income_raw | 23 (2.2) | 42 (2.2) | 207 (6.1) | 27 (2.0) | 34 (2.1) | 86 (3.6) | 419 (3.6) |
| married_dummy | 2 (0.2) | 24 (1.3) | 2 (0.1) | 0 | 0 | 3 (0.1) | 31 (0.3) |
| cluster (pre-filter) | 70 (6.8) | 61 (3.2) | 78 (2.3) | 57 (4.2) | 65 (4.0) | 62 (2.6) | 393 (3.4) |
| party_recode (not in layer4b spec) | 0 | 0 | 0 | 493 (36.6) | 374 (23.3) | 196 (8.1) | 1,063 (9.1) |

### 3b. Sequential attrition, in script order

layer4b applies (1) the cluster dropna (line 35), then (2) one **simultaneous** listwise dropna (line 59: `sub = df[needed].dropna()`); the table decomposes step 2 in the column order of the `needed` list. Wave dummies and interactions cause no additional drops (interactions are NaN only where not_religious_dummy is NaN).

| step | n remaining | dropped (by wave) |
|---|---:|---|
| start `pooled_extended_v2.csv` | 11,704 | — |
| dropna cluster | 11,311 | 393 (WV2:70 WV3:61 WV4:78 WV5:57 WV6:65 WV7:62) |
| dropna conf_military | 11,271 | 40 (WV2:3 WV3:3 WV4:16 WV5:7 WV6:6 WV7:5) |
| dropna not_religious_dummy | 10,515 | 756 (WV2:20 **WV3:423** WV4:79 WV5:20 WV6:26 WV7:188) |
| dropna rel_attendance | 10,277 | 238 (WV2:10 WV3:33 WV4:54 WV5:15 WV6:15 WV7:111) |
| dropna rel_importance_god | 10,229 | 48 (WV2:1 WV3:5 WV4:12 WV5:3 WV6:25 WV7:2) |
| dropna left_right | 9,447 | **782** (WV2:98 WV3:84 WV4:124 WV5:171 WV6:119 WV7:186) |
| dropna age | 9,439 | 8 (WV2:2 WV3:1 WV4:4 WV7:1) |
| dropna female | 9,439 | 0 |
| dropna education_raw | 9,160 | 279 (WV2:57 WV3:16 **WV4:203** WV7:3) |
| dropna income_raw | 8,923 | 237 (WV2:10 WV3:9 **WV4:160** WV5:9 WV6:22 WV7:27) |
| dropna married_dummy | **8,915** | 8 (WV3:6 WV4:2) |

Order-independent attribution — rows (post-cluster, n = 11,311) missing **only** that one model variable:

| variable | sole-missing n | by wave |
|---|---:|---|
| left_right | **737** | WV2:92 WV3:80 WV4:116 WV5:163 WV6:116 WV7:170 |
| education_raw | 256 | WV2:54 WV3:16 WV4:184 WV7:2 |
| income_raw | 236 | WV2:10 WV3:8 WV4:160 WV5:9 WV6:22 WV7:27 |
| rel_attendance | 201 | WV2:8 WV3:29 WV4:41 WV5:15 WV6:10 WV7:98 |
| not_religious_dummy | 167 | WV2:16 WV3:9 WV4:40 WV5:10 WV6:12 WV7:80 |
| rel_importance_god | 35 | WV2:1 WV3:2 WV4:10 WV5:1 WV6:21 |
| conf_military | 26 | WV3:1 WV4:14 WV5:4 WV6:5 WV7:2 |
| age | 7 | WV2:2 WV4:4 WV7:1 |
| married_dummy | 8 | WV3:6 WV4:2 |
| ≥ 2 model variables missing jointly | 723 | (largely the WV3 religiosity block: rel_person/rel_attendance/rel_importance_god co-missing, see 3a) |

Total post-cluster listwise loss: 2,396 = 11,311 − 8,915 ✓.

**Largest single source: `left_right`** — 782 in the sequential decomposition, 737 sole-missing; present in every wave, largest counts in WV7 (170) and WV5 (163); relative to wave size, WV5 is hit hardest (163/1,346 = 12.1% of the wave). Runner-up: the religiosity block, whose loss is concentrated in WV3 (~23–25% wave missingness on all three measures, co-missing — the sequential nr drop of 423 in WV3).

**8,915 → 8,777 (common sample).** Defined in `final_checks.ipynb` cell 15: `common = df.dropna(subset=TRIO + PREDICTORS)`, TRIO = [conf_military, conf_parliament, conf_government] — conf_police/conf_courts are NOT part of it. Decomposition from the army sample:

| step | n remaining | dropped (by wave) |
|---|---:|---|
| army analytic sample | 8,915 | — |
| + dropna conf_parliament | 8,848 | 67 (WV2:4 WV3:9 WV4:19 WV5:13 WV6:10 WV7:12) |
| + dropna conf_government | **8,777** | 71 (**WV2:43** WV3:7 WV4:8 WV5:4 WV6:3 WV7:6) |

Direct one-shot check `dropna(TRIO + PREDICTORS)` = 8,777 ✓ (final_checks cell 15 printed "common sample n = 8777"). The WV2 concentration in the government step reflects WV2's 11.8% conf_government missingness (3a). Note: the placebo models themselves use their **own** listwise samples (cell 3: parliament 8,873, government 8,861, civil_service 8,863), not the 8,777 common sample.

### 3c. Wave composition: pooled vs army sample vs common sample

| wave | pooled n | army n | common n | pooled % | army % | common % | army shift (pp) | common shift (pp) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| WV2 | 1,030 | 759 | 712 | 8.80 | 8.51 | 8.11 | −0.29 | −0.69 |
| WV3 | 1,907 | 1,266 | 1,250 | 16.29 | 14.20 | 14.24 | **−2.09** | **−2.05** |
| WV4 | 3,401 | 2,669 | 2,642 | 29.06 | 29.94 | 30.10 | +0.88 | +1.04 |
| WV5 | 1,346 | 1,064 | 1,047 | 11.50 | 11.93 | 11.93 | +0.43 | +0.43 |
| WV6 | 1,605 | 1,327 | 1,314 | 13.71 | 14.89 | 14.97 | +1.18 | +1.26 |
| WV7 | 2,415 | 1,830 | 1,812 | 20.63 | 20.53 | 20.64 | −0.10 | +0.01 |

Flag (> 2 pp): **WV3 only**, in both samples (−2.09 / −2.05 pp), driven by the WV3 religiosity-block missingness (3a/3b).

### 3d. Kept (8,915) vs dropped (2,789) rows — full-file baseline, simple proportions

| dimension | category | kept % | dropped % | diff (pp) |
|---|---|---:|---:|---:|
| wave | WV2 | 8.51 | 9.72 | −1.21 |
| | WV3 | 14.20 | 22.98 | −8.78 |
| | WV4 | 29.94 | 26.25 | +3.69 |
| | WV5 | 11.93 | 10.11 | +1.82 |
| | WV6 | 14.89 | 9.97 | +4.92 |
| | WV7 | 20.53 | 20.98 | −0.45 |
| not_religious_dummy | 0 | 77.38 | 54.97 | +22.41 |
| | 1 | 22.62 | 15.45 | +7.17 |
| | missing | 0.00 | 29.58 | −29.58 |
| education_recode (1=low,2=med,3=high) | 1 | 21.45 | 24.70 | −3.25 |
| | 2 | 44.42 | 36.18 | +8.24 |
| | 3 | 25.66 | 19.51 | +6.15 |
| | missing | 8.47 | 19.61 | −11.14 |
| female | 0 (male) | 51.54 | 44.42 | +7.12 |
| | 1 (female) | 48.46 | 55.58 | −7.12 |

Among dropped rows with a known nr status, the nr share is 15.45/(54.97+15.45) = 21.9% vs 22.62% among kept — nearly identical; the nr contrast above is dominated by the 29.58% of dropped rows whose religiosity is itself missing. ("education" reported on `education_recode` (3-group); the model enters `education_raw`.)

**Verdict: largest single source of attrition = left_right, costing n = 782 (737 rows missing it alone), spread over all six waves, largest in WV7 and WV5 (WV5 hardest hit relative to wave size).**

---

## 4. Placebo model statistics (parliament / government / civil_service)

### 4a. Search coverage

- **Serialized objects:** `find` over the whole project for `*.pkl, *.pickle, *.joblib, *.npz, *.npy, *.h5, *.parquet, *.feather, *.rds, *.RData, *.json` → **none exist** (no model object was ever persisted).
- **`final_checks.ipynb` writes:** zero `to_csv` calls in the notebook; cell 0 states the only new file output is `results/figs_final/pp_army.png` (confirmed: that directory holds only `pp_army.png`).
- **Model-output CSVs:** `layer3_ordinal_coefficients.csv`, `layer4_pooled_interactions.csv`, `layer4b_longwindow_interactions.csv`, `moderator_scan_grid.csv`, `education_defense_table.csv` — institution column checked in each: **only conf_military / conf_police / conf_courts**. `layer4b_total_effects_by_wave.csv`: army/police/courts columns only.
- **Files that do contain the placebo-institution strings** (checked, none holds ordinal-logit statistics): `pooled_*.csv` (raw data), `column_manifest_v2.csv` (dictionary), `integrity_report_v2.txt` (missingness), `cluster_profiles_all.csv` (cluster means of the items), `mgcfa_input.csv` / `mgcfa_loadings.csv` / `mgcfa_partial_scalar.csv` (CFA measurement parameters for a 5-item model incl. conf_parliament and conf_government — factor loadings/thresholds, not regression estimates), `results/deck_fig_main.csv` (see 4b).
- **Other notebooks:** `education_defense.ipynb` and `moderator_scan.ipynb` contain **zero** cells mentioning parliament/government/civil (sources and stored outputs scanned).

### 4b. Everything recoverable, with exact provenance

**(i) Model n's — `final_checks.ipynb` cell 3, stream outputs 0–5:** military 8,915; police 8,911; courts 6,231; **parliament 8,873; government 8,861; civil_service 8,863**. Gate line: `nr_x_WV4 (army) = +0.716155 == published +0.716155`.

**(ii) nr × wave interactions, full sample — cell 4, output 0 (execute_result; 3 dp + stars, no SE/p):**

| interaction | parliament | government | civil_service |
|---|---:|---:|---:|
| nr × WV3 | +0.632** | +0.064 | +0.540** |
| nr × WV4 | +0.841*** | +0.373* | +0.645*** |
| nr × WV5 | +0.410* | −0.160 | +0.461* |
| nr × WV6 | +0.492* | −0.016 | +0.220 |
| nr × WV7 | +0.810*** | −0.126 | +0.334. |

**(iii) Total nr effects per wave, full sample — cell 5, output 0 (3 dp + stars, no SE/p):**

| wave | parliament | government | civil_service |
|---|---:|---:|---:|
| WV2 | −0.891*** | −0.425** | −0.761*** |
| WV3 | −0.260* | −0.361** | −0.221. |
| WV4 | −0.050 | −0.052 | −0.116 |
| WV5 | −0.481*** | −0.586*** | −0.300* |
| WV6 | −0.399** | −0.441*** | −0.541*** |
| WV7 | −0.081 | −0.552*** | −0.427*** |

Star convention from cell 1 `stars()`: *** p<.001, ** p<.01, * p<.05, . p<.10.

**(iv) Common-sample trio at WV5 (n = 8,777) — cell 15, outputs 0–1. The only placebo coefficients on disk WITH standard errors** (SE in parentheses; this is a different fit from the full-sample grid — do not mix):

| quantity | army | parliament | government |
|---|---:|---:|---:|
| nr × WV5 interaction | +0.675 (0.228) | +0.440 (0.211) | −0.167 (0.210) |
| nr total effect at WV5 | −0.089 (0.164) | −0.486 (0.143) | −0.596 (0.144) |

Wald contrasts (independence SE), same output: army vs parliament interaction diff +0.235, SE 0.310, z 0.76, p 0.4493; army vs parliament WV5 level diff +0.398, SE 0.218, z 1.83, p 0.0677; army vs government interaction diff +0.841, SE 0.310, z 2.71, p 0.0066; army vs government WV5 level diff +0.507, SE 0.218, z 2.32, p 0.0202.

**(v) `results/deck_fig_main.csv` lines 20–37** (file lines, header = line 1) (institution ∈ {parliament, government, civil_service}): the same cell 5 totals in tidy form, 3 dp + stars, `source` column = "final_checks.ipynb cell 5 output". No SE/p columns.

**(vi) Markdown restatements** (no added precision): cell 0 (+0.84***, +0.65***), cell 6 (−0.48***, −0.59***, −0.30*), cell 16 (parliament baseline "−0.89"; Wald numbers as in (iv)).

### 4c. NOT recoverable without refitting

- **SE, exact p, z, and CI for every full-sample placebo coefficient** — WV2 baselines, all nr × wave interactions, all wave totals, for parliament, government, and civil_service. Only 3-dp coefficients + stars were printed; nothing was written to CSV; no model objects persisted.
- Coefficients at more than 3 dp for those models (the army/police/courts equivalents are in `layer4b_longwindow_interactions.csv` at full precision; no placebo counterpart exists).
- Control coefficients, thresholds, pseudo-R², and convergence diagnostics for the placebo fits (never printed).
- Any **civil_service common-sample** quantity (cell 15's TRIO excludes it) and any common-sample quantity at waves other than WV5.
- Predicted probabilities at WV5/WV6 (cell 11 hard-codes `PP_WAVES = ["WV2","WV3","WV4","WV7"]`).
- Exact SE/p per wave for the nr_god (≤7) army model in cell 8 (3-dp coef + stars only; cell 9 markdown quotes p = .014 for WV4, and the printed table shows +0.508* vs the markdown's +0.509 — the unrounded value exists nowhere).

**Verdict: PLACEBO SEs REFIT REQUIRED** — missing: SE/exact p/CI for all full-sample parliament/government/civil_service coefficients (baselines, interactions, totals); civil_service common-sample fit; non-WV5 common-sample quantities. Recoverable without refit: 3-dp coefficients + stars, model n's, and the cell 15 WV5 common-sample coef+SE pairs listed above.

---

## 5. Third religiosity measure

### 5a. Religiosity-related columns

From `results/column_manifest_v2.csv` (rows quoted) and `results/pooled_extended_v2.csv` (non-null counts; wave n's 1,030 / 1,907 / 3,401 / 1,346 / 1,605 / 2,415). Source codes from crosswalk v3 ([pool_final.py:52-57](../pool_final.py)).

| column | manifest label / coding | source codes WV2..WV7 | WV2 | WV3 | WV4 | WV5 | WV6 | WV7 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| rel_person | "1=religious, 2=not religious, 3=convinced atheist" (1..3, higher = less religious) | V151, V182, V186, V187, V147, Q173 | 1,002 | 1,453 | 3,320 | 1,321 | 1,575 | 2,208 |
| **rel_attendance** | "1=more than once a week .. 8=never (per WVS)" (1..8, higher = less frequent) | V147, V181, V185, V186, V145, Q171 | 1,017 | 1,431 | 3,327 | 1,321 | 1,580 | 2,219 |
| rel_importance_god | "Importance of God in life" (1..10, higher = more important) | V176, V190, V196, V192, V152, Q164 | 1,026 | 1,467 | 3,385 | 1,339 | 1,574 | 2,398 |

Observed value sets in the pooled file: rel_person {1,2,3}; rel_attendance {1..8}; rel_importance_god {1..10}.

Religion-adjacent columns that are **not** religiosity measures (membership / attitude items, listed for completeness): `member_org_church` / `member_org_church_bin` (non-null 0 / 1,878 / 0 / 1,346 / 1,601 / 2,387 — WV2 and WV4 not fielded), `neighbor_religion` (0 / 0 / 3,401 / 1,346 / 1,605 / 2,363 — WV2/WV3 not fielded).

### 5b. The third measure and its usage

The two accounted measures are rel_person (→ `not_religious_dummy`) and rel_importance_god (tertile cuts / ≤7 low cut). **The third is `rel_attendance`.** Grep of every .py/.ipynb/.R in the project:

| file | how rel_attendance is used |
|---|---|
| pool_final.py / pool_extended.py | dataset build only (crosswalk selection + sentinel cleaning) |
| layer3_ordinal_regressions.py | **control** — `RELIG = ["not_religious_dummy", "rel_attendance", "rel_importance_god"]` (line 57; spec in docstring line 8) |
| layer4_pooled_interactions.py | **control** (predictor list, line 59) |
| layer4b_longwindow.py | **control in the headline model** (`PREDICTORS_BASE`, line 50) |
| pressure_tests.py | **control** (predictor list, line 41) |
| education_defense.ipynb | **control** (cell 1, `BASE` list) |
| moderator_scan.ipynb | **control** (cell 9, `CONTROLS` list) |
| final_checks.ipynb | **control** in all six placebo fits (cell 1, `PREDICTORS`) and in the nr_god variant (cell 8, `PRED_GOD`) |
| layer1_by_religiosity.py | not used (splits on rel_importance_god, fixed cuts 1–7 / 8–9 / 10, lines 25–38) |
| layer1_by_relperson.py | not used (splits on rel_person) |
| religiosity_composition.py | not used (describes rel_importance_god and rel_person only, lines 6–7) |
| mgcfa_analysis.R / mgcfa_runner.py | not used (confidence items only) |

So rel_attendance is a **control in every regression spec** and is **never** used as a religiosity grouping/split variable, and no descriptive output tabulates it (religiosity_composition.py covers only the other two measures).

### 5c. Per-wave availability

Fielded in **all six waves** (source codes and non-null counts in 5a). Coverage ≥ 97% of wave n everywhere except WV3 (1,431/1,907 = 75.0%) and WV7 (2,219/2,415 = 91.9%) — the same WV3 religiosity-block gap visible in §3a.

### 5d. Spearman correlations among the three measures

Pairwise-complete, raw codings (orientations as in 5a: rel_person ↑ = less religious; rel_attendance ↑ = less frequent attendance; rel_importance_god ↑ = more important — hence positive rp–ra and negative correlations with god-importance are directionally concordant). Computed from `pooled_extended_v2.csv`.

| sample | rp–ra | rp–god | ra–god | pairwise n (rp–ra / rp–god / ra–god) |
|---|---:|---:|---:|---|
| pooled | +0.221 | −0.325 | −0.210 | 10,624 / 10,823 / 10,835 |
| WV2 | +0.229 | −0.437 | −0.307 | 992 / 1,001 / 1,015 |
| WV3 | +0.281 | −0.376 | −0.369 | 1,420 / 1,447 / 1,425 |
| WV4 | +0.183 | −0.362 | −0.232 | 3,264 / 3,308 / 3,314 |
| WV5 | +0.231 | −0.356 | −0.231 | 1,306 / 1,318 / 1,318 |
| WV6 | +0.211 | −0.269 | −0.239 | 1,559 / 1,548 / 1,553 |
| WV7 | +0.281 | −0.203 | −0.141 | 2,083 / 2,201 / 2,210 |

(Pooled pairwise n's computed directly on the pooled file; they equal the sums of the per-wave pairwise n's.)

**Verdict: third measure = rel_attendance; used as a control in layer3_ordinal_regressions.py, layer4_pooled_interactions.py, layer4b_longwindow.py, pressure_tests.py, education_defense.ipynb, moderator_scan.ipynb, final_checks.ipynb; never used as a grouping/split measure in any file.**

---

## BLOCKERS (unresolvable without a fitting session)

1. **Full-sample placebo statistics.** SE / exact p / z / CI for every parliament, government, and civil_service coefficient (WV2 baselines, all nr × wave interactions, all per-wave totals). On disk: 3-dp coefficients + stars only (`final_checks.ipynb` cells 4–5; `deck_fig_main.csv`). Requires re-running the cell 3 fits (spec and sample logic fully specified in cells 1+3; the army gate value +0.716155 is stored for verification).
2. **Civil_service common-sample fit and non-WV5 common-sample quantities.** Cell 15's TRIO = {military, parliament, government} and computes WV5 contrasts only; nothing else on the 8,777 sample exists.
3. **Predicted probabilities at WV5 and WV6.** Cell 11 hard-codes `PP_WAVES = ["WV2","WV3","WV4","WV7"]`; no file stores WV5/WV6 values.
4. **Exact nr_god (≤7) statistics.** Cell 8 printed 3-dp coefficients + stars; exact p exists only as the cell 9 markdown quote for WV4 (p = .014), with an unresolved last-digit inconsistency (+0.509 markdown vs +0.508 printed table).
5. **Any weighted estimate.** Non-constant calibration weights exist in the source files for WV3–WV6 (§1) but were never carried into `pooled_extended_v2.csv`; producing any weighted number requires a rebuild (add V236/V245/V259/V258 to the pool) plus refits. For WV2 and WV7 the released weight is constant 1.0, so weighted = unweighted in those waves by construction.

Resolved read-only (no refit needed): weight presence in source (§1), all cell counts (§2), the full attrition accounting (§3), the identity and usage of the third religiosity measure (§5).
