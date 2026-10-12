# Deck data final — extraction and verification (SDL 2026, conference eve)

**SAMPLE BASIS: all LEVEL figure data in `results/deck_fig_data.csv` uses the cell-15
common sample (n = 8,777; civil service on its 8,711 subset, courts on its 6,110 subset),
with bootstrap-percentile CIs from `closing_checks_table.csv`. The CHP-arc block uses the
party_axis WV5–WV7 sample (n = 4,221) with delta-method SEs. No cell required the
full-sample basis.** Read-only extraction: no model fit, no notebook executed, no new test
computed; every value is read from the named file (arithmetic limited to sums/rounding
comparisons).

## VERIFICATION SUMMARY: 64 MATCH / 1 MISMATCH / 0 NOT FOUND (of 65 checks)

## Item 1 — deck number list, checked cell by cell

| # | claim | stored value | source | verdict | note |
|---|---|---|---|---|---|
| 1 | pooled n = 11,704 | 11704 | pooled_extended_v2.csv (row count) | **MATCH** |  |
| 2 | army model n = 8,915 | 8915 | layer4b_longwindow_interactions.csv | **MATCH** |  |
| 3 | common sample n = 8,777 | 8777 | placebo_models_full.csv | **MATCH** |  |
| 4 | 1990 gradient: government -0.43 | -0.429194 | closing_checks_table.csv | **MATCH** |  |
| 5 | 1990 gradient: parliament -0.93 | -0.925932 | closing_checks_table.csv | **MATCH** |  |
| 6 | 1990 heterogeneity chi2(5) = 11.4 | 11.4265 | draws_readoff2_table.csv | **MATCH** |  |
| 7 | 1990 heterogeneity p = .044 | 0.0435494 | draws_readoff2_table.csv | **MATCH** |  |
| 8 | 1996 change parliament +0.669 | 0.66919 | draws_readoff_table.csv | **MATCH** |  |
| 9 | 1996 change parliament p=0.002 | 0.002 | draws_readoff_table.csv | **MATCH** |  |
| 10 | 1996 change civil_service +0.565 | 0.565366 | draws_readoff_table.csv | **MATCH** |  |
| 11 | 1996 change civil_service p=0.002 | 0.002002 | draws_readoff_table.csv | **MATCH** |  |
| 12 | 1996 change military +0.427 | 0.426583 | draws_readoff_table.csv | **MATCH** |  |
| 13 | 1996 change military p=0.016 | 0.015984 | draws_readoff_table.csv | **MATCH** |  |
| 14 | 1996 change police p=0.054 | 0.0541082 | draws_readoff_table.csv | **MATCH** |  |
| 15 | 1996 change courts p=0.106 | 0.105894 | draws_readoff_table.csv | **MATCH** |  |
| 16 | 1996 change government p=0.644 | 0.644 | draws_readoff_table.csv | **MATCH** |  |
| 17 | 1996 DiD army vs police p=0.77 | 0.765531 | draws_readoff_table.csv | **MATCH** |  |
| 18 | 1996 DiD army vs parliament p=0.27 | 0.274 | draws_readoff_table.csv | **MATCH** |  |
| 19 | 1996 DiD army vs government p=0.16 | 0.156 | draws_readoff_table.csv | **MATCH** |  |
| 20 | 1996 DiD army vs civil_service p=0.53 | 0.526527 | draws_readoff_table.csv | **MATCH** |  |
| 21 | 2001 army interaction +0.716 | 0.716155 | layer4b_longwindow_interactions.csv | **MATCH** |  |
| 22 | 2001 army SE 0.183 | 0.182816 | layer4b_longwindow_interactions.csv | **MATCH** |  |
| 23 | 2001 army p = 8.95e-05 | 8.953e-05 | layer4b_longwindow_interactions.csv | **MATCH** |  |
| 24 | 2001 parliament +0.841 | 0.841479 | placebo_models_full.csv | **MATCH** |  |
| 25 | 2001 civil service +0.645 | 0.645353 | placebo_models_full.csv | **MATCH** |  |
| 26 | 2011 army LEVEL -0.332 | -0.332033 | closing_checks_table.csv | **MATCH** |  |
| 27 | 2011 army bootstrap 90% CI [-0.552, -0.095] | [-0.552, -0.095] | closing_checks_table.csv | **MATCH** |  |
| 28 | 2011 army delta 90% CI [-0.560, -0.104] | [-0.560, -0.104] | verification_pass.md | **MATCH** |  |
| 29 | 2011/1990 ratio 0.435 | 0.435125 | draws_readoff_table.csv | **MATCH** |  |
| 30 | 2011 neighbours chi2(2) = 2.44 | 2.43991 | draws_readoff2_table.csv | **MATCH** |  |
| 31 | 2011 neighbours p = .295 | 0.295244 | draws_readoff2_table.csv | **MATCH** |  |
| 32 | parliament 2007 LEVEL -0.486 | -0.486163 | closing_checks_table.csv | **MATCH** |  |
| 33 | parliament 2018 bootstrap 95% CI [-0.202, +0.053] | [-0.202, +0.053] | closing_checks_table.csv | **MATCH** |  |
| 34 | parliament 2018 delta 95% CI [-0.251, +0.098] | [-0.251, +0.098] | verification_pass.md | **MATCH** |  |
| 35 | parliament decline +0.410 | 0.409805 | closing_checks_table.csv | **MATCH** |  |
| 36 | parliament decline bootstrap p = .004 | 0.004 | closing_checks_table.csv | **MATCH** |  |
| 37 | parliament decline delta p = .014 | 0.0139 | verification_pass.md | **MATCH** | 0.0139 rounds to .014 |
| 38 | persistence army vs government chi2(3) = 31.12 | 31.1153 | persistence_test_table.csv | **MATCH** |  |
| 39 | persistence army vs government p < 1e-5 | 8.04e-07 | persistence_test_table.csv | **MATCH** |  |
| 40 | persistence army vs civil chi2(3) = 16.21 | 16.2096 | persistence_test_table.csv | **MATCH** |  |
| 41 | persistence army vs civil p = .001 | 0.00102711 | persistence_test_table.csv | **MATCH** |  |
| 42 | courts 2007-2018 LEVELs -0.42 to -0.45 | -0.4155/-0.4481/-0.4271 | layer4b_total_effects_by_wave.csv (FULL-sample basis) | **MATCH** | on the common-sample basis (closing_checks) the range is -0.437 to -0.450 -> '-0.44 to -0.45' |
| 43 | CHP LEVEL army 2018 = -0.389 | -0.388745 | party_axis_table.csv | **MATCH** |  |
| 44 | CHP LEVEL army 2018 p = .005 | 0.00511593 | party_axis_table.csv | **MATCH** |  |
| 45 | CHP x WV7 interaction p = 4.7e-12 | 4.65e-12 | party_axis_table.csv | **MATCH** |  |
| 46 | corr(nr, CHP) = 0.247 | 0.246971 | party_axis_table.csv | **MATCH** |  |
| 47 | condition number 5.9 | 5.88948 | party_axis_table.csv | **MATCH** |  |
| 48 | VIF <= 6.1 | max VIF = 6.12 | party_axis.ipynb cell 8 stored output | **MISMATCH** | max VIF is 6.12 (CHP_dummy): strictly > 6.1; deck should say 'max VIF 6.1' (1 dp) or '<= 6.2' |
| 49 | 2018 joint-model religious gradients -0.37 to -0.41, p <= .0003 | -0.3830/-0.3658/-0.4130; p max 0.0003 | closing_checks_table.csv (3_rotation) | **MATCH** |  |
| 50 | delta_courts = 0.42 | 0.42 | closing_checks_table.csv / closing_checks.ipynb | **MATCH** |  |
| 51 | delta_base = 0.7631 | 0.7631 | verification_pass.md / closing_checks.ipynb | **MATCH** |  |
| 52 | robustness baseline +0.716 | 0.716155 | layer4b_longwindow_interactions.csv | **MATCH** |  |
| 53 | robustness weighted +0.776 | 0.776024 | preflight_refits_table.csv | **MATCH** |  |
| 54 | robustness common +0.738 | 0.737946 | placebo_models_full.csv | **MATCH** |  |
| 55 | robustness no-attendance +0.726 | 0.72614 | preflight_refits_table.csv | **MATCH** |  |
| 56 | robustness no-left-right +0.681 | 0.680739 | preflight_refits_table.csv | **MATCH** |  |
| 57 | robustness binary +1.323 | 1.32281 | preflight_refits_table.csv | **MATCH** |  |
| 58 | robustness joint-with-education +0.636 | 0.6365 | education_defense_table.csv | **MATCH** |  |
| 59 | robustness god-importance +0.509 p=.014 | +0.509* (p = .014) | deck_numbers.md <- final_checks.ipynb cell 9 markdown | **MATCH** | known last-digit caveat: cell 8 printed table shows +0.508* (deck_numbers DISCREPANCIES #2) |
| 60 | robustness bootstrap mean +0.755 [+0.419, +1.115] | +0.755, SI [+0.419, +1.115] | pressure_tests.md | **MATCH** |  |
| 61 | Gunduz six CHP cells to <= 0.006 | max diff 0.0055 over 6 cells | party_axis.ipynb cell 5 stored output | **MATCH** |  |
| 62 | Gunduz Ns 1,269 / 1,525 / 2,324 | [1269, 1525, 2324] | party_axis_table.csv | **MATCH** |  |
| 63 | MGCFA metric holds | delta CFI_scaled metric vs configural = +0.0077 | mgcfa_delta_fit.csv | **MATCH** |  |
| 64 | MGCFA partial scalar: conf_military freed is best variant | partial_free_military | mgcfa_partial_scalar.csv | **MATCH** |  |
| 65 | MGCFA n = 5,066 | 5066 | mgcfa_input.csv (row count) | **MATCH** |  |

## Item 2 — the party reference category

**2a.** From `party_axis.ipynb` step-2 code (stored source, cell 7): dummies in the joint
model are `AKP_dummy`, `CHP_dummy`, `MHP_dummy`, `PK_dummy` (DTP 792049 in WV5 / BDP 792054
in WV6 / HDP 792005 in WV7), and `other_dummy` (any *stated* party outside those four,
incl. IYI). The dummy-construction lines:

```python
d2["AKP_dummy"] = (d2["party_raw"] == 792008).astype(int)
d2["CHP_dummy"] = (d2["party_raw"] == 792002).astype(int)
d2["MHP_dummy"] = (d2["party_raw"] == 792006).astype(int)
d2["PK_dummy"] = (d2["wave"].map(PK_CODE) == d2["party_raw"]).astype(int)
stated = d2["party_raw"].notna() & (d2["party_raw"] > 100000)
d2["other_dummy"] = (stated & (d2[["AKP_dummy", "CHP_dummy", "MHP_dummy", "PK_dummy"]
for a, b in [("nr", "not_religious_dummy"), ("chp", "CHP_dummy"), ("lr", "left_right")]:
PARTY5 = ["AKP_dummy", "CHP_dummy", "MHP_dummy", "PK_dummy", "other_dummy"]
KEY = ["not_religious_dummy", "nr_x_wv6", "nr_x_wv7", "CHP_dummy", "chp_x_wv6", "chp_x_wv7"]
                       ("CHP", "CHP_dummy", "chp_x_wv6", "chp_x_wv7")]:
```

**The omitted (reference) category is respondents with NO stated party preference** —
party_raw non-response codes (-1, -2, 2, 5: don't know / no answer / would-not-vote per
the WVS results-book categories) plus true missing. It contains non-voters, DK/no-answer,
AND missing — but NOT 'other' parties (those carry `other_dummy`).

**2b.** Raw n of the reference category per wave (full pooled file; from the
`party_axis_table.csv` INVENTORY cross-tab, summing over nr categories):

| wave | reference n (raw, full file) |
|---|---|
| WV5 | 495 |
| WV6 | 374 |
| WV7 | 196 |

In the fitted joint-model sample (n = 4,221), the reference totals **658** across the three waves (derived: 4,221 minus stated-party counts {'AKP_dummy': '1834', 'CHP_dummy': '898', 'MHP_dummy': '416', 'PK_dummy': '252', 'other_dummy': '163'} from party_axis.ipynb cell 7 stored output). **Per-wave in-model reference n: NOT FOUND** — not stored in any file; it would require re-deriving the
analytic sample (checked: party_axis_table.csv, party_axis.ipynb outputs).

**2c.** Full party grid from the joint model (`party_axis_table.csv`, model OURS_2c),
**descriptive**. Structural note: only CHP carries wave interactions — AKP/MHP/PK/other
LEVELs are constrained constant across WV5–WV7 by the model's design. **Testing CHP vs
AKP (or any cross-party difference) would require the model's covariance matrix, which
was not stored.**

| party dummy | WV5 (2007) | WV6 (2011) | WV7 (2018) | SE | p |
|---|---|---|---|---|---|
| AKP | -0.0310 | (constant) | (constant) | 0.0996 | 0.7559 |
| CHP | +1.3465 (0.2340) p=8.73e-09 | +0.5449 (0.1429) p=0.000137 | -0.3887 (0.1389) p=0.00512 | per-wave | per-wave |
| MHP | +0.0412 | (constant) | (constant) | 0.1305 | 0.7524 |
| pro-Kurdish (DTP/BDP/HDP) | -1.6428 | (constant) | (constant) | 0.1505 | 0 |
| other stated | +0.1353 | (constant) | (constant) | 0.1814 | 0.4556 |

**2d.** CHP arc +1.35 / +0.54 / -0.39: **CONFIRMED as LEVELs from the joint model**
(main effect + CHP x wave interaction, delta-method SE; `party_axis_table.csv`,
terms CHP_total_WV5/WV6/WV7):

| wave | CHP LEVEL | SE | p | individually significant |
|---|---|---|---|---|
| WV5 (2007) | +1.3465 | 0.2340 | 8.73e-09 | yes |
| WV6 (2011) | +0.5449 | 0.1429 | 0.000137 | yes |
| WV7 (2018) | -0.3887 | 0.1389 | 0.00512 | yes |

## Item 3 — WV7 fieldwork dates

Header scan of all six source workbooks; matches restricted to genuine date/fieldwork
variables (code match on S011/S012/S013/S025/J_INTDATE/INTDATE/A_YEAR/FW_START/FW_END/
TARIH or a 'date of interview'/'fieldwork' label; questionnaire items mentioning 'month'
were screened out as false positives).

**WV2** (`F00008272-WV2_Data_Turkey_Excel_v1.6.1.xlsx`):
- `S025: Country - year` — country-year code (792 = Turkey + year; constant); n non-null = 1,030, min = 7921990, max = 7921990

**WV3** (`F00008135-WV3_Data_Turkey_Excel_v20221107.1.xlsx`):
- `FW_START: Fieldwork month/year Start` — wave-level fieldwork YYYYMM (constant); n non-null = 1,907, min = 199612, max = 199612
- `FW_END: Fieldwork month/year End` — wave-level fieldwork YYYYMM (constant); n non-null = 1,907, min = 199701, max = 199701

**WV4** (`F00008022-WV4_Data_Turkey_Excel_v20201117.1.xlsx`):
- `FW_START: Fieldwork month/year Start` — wave-level fieldwork YYYYMM (constant); n non-null = 3,401, min = 200112, max = 200112
- `FW_END: Fieldwork month/year End` — wave-level fieldwork YYYYMM (constant); n non-null = 3,401, min = 200201, max = 200201

**WV5** (`F00007873-WV5_Data_Turkey_Excel_v20201117.1.xlsx`):
- `S025: Country - year` — country-year code (792 = Turkey + year; constant); n non-null = 1,346, min = 7922007, max = 7922007
- `FW_START: Fieldwork month/year Start` — wave-level fieldwork YYYYMM (constant); n non-null = 1,346, min = 200701, max = 200701
- `FW_END: Fieldwork month/year End` — wave-level fieldwork YYYYMM (constant); n non-null = 1,346, min = 200703, max = 200703

**WV6** (`F00007629-WV6_Data_Turkey_2011_Excel_v20180912.xlsx`):
- `V261: Date of interview` — per-respondent date (YYYYMMDD); n non-null = 1,605, min = 20110630, max = 20110825
  - month distribution (month: n): {6: 19, 7: 1373, 8: 213}
- `S025: Nation Year` — country-year code (792 = Turkey + year; constant); n non-null = 1,605, min = 7922012, max = 7922012

**WV7** (`F00013222-WVS_Wave_7_Turkey_Excel_v5.1.xlsx`):
- `A_YEAR: Year of survey` — year (constant); n non-null = 2,415, min = 2018, max = 2018
- `J_INTDATE: Date of interview` — per-respondent date (YYYYMMDD); n non-null = 2,415, min = 20180331, max = 20180521
  - month distribution (month: n): {3: 16, 4: 1468, 5: 931}
- `FW_START: Year/month of start-fieldwork` — wave-level fieldwork YYYYMM (constant); n non-null = 2,415, min = 201803, max = 201803
- `FW_END: Year/month of end-fieldwork` — wave-level fieldwork YYYYMM (constant); n non-null = 2,415, min = 201805, max = 201805

Cross-check notes: **WV7 fieldwork window = 2018-03-31 to 2018-05-21** (J_INTDATE;
consistent with FW_START 201803 / FW_END 201805 and A_YEAR 2018). WV6 carries a
per-respondent date too: 2011-06-30 to 2011-08-25 — while its `S025` nation-year code
reads 792-2012 (the WVS results book likewise titles the file 'Turkey 2012'); the project
labels this wave 2011, matching the interview dates. WV2 has **no month-level fieldwork
variable in the source** (year only, via S025 = 792-1990); WV3/WV4/WV5 carry wave-level
FW_START/FW_END only (WV3: 1996-12 to 1997-01; WV4: 2001-12 to 2002-01; WV5: 2007-01 to
2007-03), no per-respondent dates.

## Item 4 — figure data export

**4a/4b.** `results/deck_fig_data.csv` written: 39 rows — 36 `levels` rows
(6 institutions x 6 waves, common-sample basis, bootstrap-percentile CIs, courts WV4 as a
null row with notes='not fielded', all WV7 rows carrying the measurement caveat) + 3
`chp_arc` rows (delta SEs, reference category stated per row).

**4c.** Per-wave n (source: `preflight_diagnostics.md` section 3c table):

| wave | pooled file | army analytic (8,915) | common sample (8,777) |
|---|---|---|---|
| WV2 | 1,030 | 759 | 712 |
| WV3 | 1,907 | 1,266 | 1,250 |
| WV4 | 3,401 | 2,669 | 2,642 |
| WV5 | 1,346 | 1,064 | 1,047 |
| WV6 | 1,605 | 1,327 | 1,314 |
| WV7 | 2,415 | 1,830 | 1,812 |

**4d.** Plot completeness: (i) the six x six LEVEL plot with CIs needs institution, wave,
year, level, ci95 (and ci90) — **all present** in the `levels` block. (ii) the CHP arc
needs party, wave, year, level and an error bar — level/SE/p present; **explicit CI bounds
for the CHP arc are not stored anywhere** (only delta SEs were exported by party_axis);
a plotter must form normal-approximation bars as level +/- 1.96 x SE. Nothing else is
missing.

## DISCREPANCIES

1. **MISMATCH** — VIF <= 6.1: stored = max VIF = 6.12 (party_axis.ipynb cell 8 stored output). max VIF is 6.12 (CHP_dummy): strictly > 6.1; deck should say 'max VIF 6.1' (1 dp) or '<= 6.2'
2. **NOT FOUND** — per-wave in-model reference-category n (item 2b): not stored; only the three-wave total (658) is derivable from stored outputs.
3. **BASIS NOTE** — the courts '-0.42 to -0.45' range is the FULL-sample layer4b series (-0.4155/-0.4481/-0.4271); on the deck's common-sample basis the courts range is -0.437/-0.450/-0.437 ('-0.44 to -0.45'). One basis should be named on the slide.
4. **CI-SOURCE NOTE** — item-1 CIs quoted for 2011 army and 2018 parliament are bootstrap percentile intervals; the delta-method intervals differ (both stored in verification_pass.md) and the slide should not mix the two without labels.

