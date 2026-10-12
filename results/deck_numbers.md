# Deck numbers — SDL 2026 (locked from output files, 2026-07-16)

All values read directly from existing files; no models re-run. Star convention throughout
(from `final_checks.ipynb` cell 1, `stars()`): `***` p<.001, `**` p<.01, `*` p<.05, `.` p<.10.

Sources used:
- `results/layer4b_longwindow_interactions.csv` (army/police/courts, exact coef/SE/p)
- `results/layer4b_total_effects_by_wave.csv` (army/police/courts totals, exact)
- `final_checks.ipynb` (six-institution placebo run; **no CSV written** — cell 0 states the only
  new file output is `results/figs_final/pp_army.png`, so parliament/government/civil-service
  values are read from printed notebook outputs, which show coefficient + stars but not SE/p)
- `results/layer1_gaps.csv`, `results/pressure_tests.md`, `results/education_defense_table.csv`,
  `results/mgcfa_delta_fit.csv`, `results/mgcfa_fit_indices.csv`, `results/mgcfa_partial_scalar.csv`,
  `results/mgcfa_input.csv`, `results/cluster_kappa_summary.csv`, `results/moderator_scan_grid.csv`,
  `partner_handoff_v2.md`

---

## 1. 1990 baseline gradients (main-effect `not_religious_dummy`, WV2 reference)

| Institution | Coef | SE | p | Source |
|---|---:|---:|---:|---|
| Armed forces | -0.7363 | 0.1568 | 2.66e-06 | `layer4b_longwindow_interactions.csv` row `conf_military,not_religious_dummy` (line 2) |
| Police | -0.6918 | 0.1521 | 5.42e-06 | `layer4b_longwindow_interactions.csv` row `conf_police,not_religious_dummy` (line 21) |
| Courts | -0.5030 | 0.1549 | 0.00116 | `layer4b_longwindow_interactions.csv` row `conf_courts,not_religious_dummy` (line 40) |
| Parliament | -0.891*** | NOT FOUND | NOT FOUND (stars ⇒ p<.001) | `final_checks.ipynb` cell 5 output, WV2 row (cell 16 markdown quotes "−0.89") |
| Government | -0.425** | NOT FOUND | NOT FOUND (stars ⇒ p<.01) | `final_checks.ipynb` cell 5 output, WV2 row |
| Civil service | -0.761*** | NOT FOUND | NOT FOUND (stars ⇒ p<.001) | `final_checks.ipynb` cell 5 output, WV2 row |

Anchor check: parliament -0.891 ≈ expected -0.89. MATCH.
Note: exact SE/p for parliament, government, civil service exist only inside the fitted notebook
objects; they were never printed or written to CSV. NOT FOUND as exact numbers.

Placebo-run n's (final_checks cell 3 output): military 8,915; police 8,911; courts 6,231;
parliament 8,873; government 8,861; civil service 8,863. Gate passed: army `nr_x_WV4` = +0.716155,
identical to the published CSV value.

## 2. nr × wave interaction grid (WV2 reference)

Army/police/courts: exact values from `layer4b_longwindow_interactions.csv` (lines 16–20, 35–39, 53–56).
Parliament/government/civil service: `final_checks.ipynb` cell 4 printed output (coef + stars only;
SE and exact p NOT FOUND — not printed, no CSV written).

| nr × wave | Army | Police | Courts | Parliament | Government | Civil service |
|---|---:|---:|---:|---:|---:|---:|
| WV3 | +0.3746 (0.1997, p=.0607) . | +0.2825 (0.1905, p=.1382) | +0.2669 (0.1917, p=.1639) | +0.632** | +0.064 | +0.540** |
| WV4 | +0.7162 (0.1828, p=8.95e-05) *** | +0.4484 (0.1756, p=.0107) * | — not fielded | +0.841*** | +0.373* | +0.645*** |
| WV5 | +0.6352 (0.2235, p=.0045) ** | +0.2609 (0.2062, p=.2058) | +0.0875 (0.2101, p=.6770) | +0.410* | -0.160 | +0.461* |
| WV6 | +0.4023 (0.2061, p=.0509) . | +0.1552 (0.2008, p=.4394) | +0.0549 (0.2029, p=.7867) | +0.492* | -0.016 | +0.220 |
| WV7 | +0.6511 (0.1819, p=3.45e-04) *** | +0.5617 (0.1774, p=.0015) ** | +0.0759 (0.1776, p=.6692) | +0.810*** | -0.126 | +0.334. |

Courts has no WV4 row in the model output (item not fielded in WV4) — confirmed: no `nr_x_WV4`
row for `conf_courts` in the CSV and "—" in the notebook grid.

Anchor checks: army × WV4 +0.716*** MATCH; parliament × WV4 +0.841*** MATCH; civil service × WV4
+0.645*** MATCH. Army × WV5 / parliament × WV5 / government × WV5 anchors: see DISCREPANCIES —
they match the common-sample Wald run (final_checks cell 15), not this full-sample grid.

Common-sample values (final_checks cell 15 output, trio fit on n=8,777 common sample):
army × WV5 = +0.675 (SE 0.228); parliament × WV5 = +0.440 (SE 0.211); government × WV5 = -0.167 (SE 0.210).

## 3. Total effects by wave (baseline + interaction, delta-method)

Army/police/courts: exact from `results/layer4b_total_effects_by_wave.csv` (coef, p).
Parliament/government/civil service: `final_checks.ipynb` cell 5 printed output (coef + stars; SE/p NOT FOUND).

| Wave (year) | Army | Police | Courts | Parliament | Government | Civil service |
|---|---:|---:|---:|---:|---:|---:|
| WV2 (1990) | -0.7363 (p=.000) | -0.6918 (p=1e-05) | -0.5030 (p=.00116) | -0.891*** | -0.425** | -0.761*** |
| WV3 (1996) | -0.3617 (p=.0054) | -0.4093 (p=.00068) | -0.2361 (p=.05412) | -0.260* | -0.361** | -0.221. |
| WV4 (2001) | -0.0201 (p=.84284) | -0.2433 (p=.01012) | — EXCLUDED (see note) | -0.050 | -0.052 | -0.116 |
| WV5 (2007) | -0.1011 (p=.53558) | -0.4309 (p=.00267) | -0.4155 (p=.00517) | -0.481*** | -0.586*** | -0.300* |
| WV6 (2011) | -0.3339 (p=.01571) | -0.5366 (p=7e-05) | -0.4481 (p=.00111) | -0.399** | -0.441*** | -0.541*** |
| WV7 (2018) | -0.0851 (p=.37578) | -0.1300 (p=.16891) | -0.4271 (p=.000) | -0.081 | -0.552*** | -0.427*** |

**Phantom exclusion:** `layer4b_total_effects_by_wave.csv` line 4 (WV4 row) carries
`courts_total = -0.503, courts_p = 0.00116` — identical to the WV2 baseline (line 2). The courts
item was not fielded in WV4, so this is the baseline carried forward with no interaction term.
Excluded. The notebook grid (cell 5) correctly prints "—" for courts at WV4.

Anchor checks: courts WV5/WV6/WV7 = -0.4155 / -0.4481 / -0.4271 MATCH exactly; civil service
WV5 -0.300* MATCH (-0.30). Army/parliament/government WV5 anchors (-0.089 / -0.486 / -0.596):
those are the common-sample cell 15 values — full-sample values are -0.1011 / -0.481 / -0.586.
See DISCREPANCIES.

## 4. Plotting series for the main figure (slide 7)

Written to `results/deck_fig_main.csv` (tidy: institution, wave, year, total_effect, stars, source, note).
Full-sample series throughout: army/police/courts at 4 dp from `layer4b_total_effects_by_wave.csv`;
parliament/government/civil service at 3 dp from `final_checks.ipynb` cell 5 (only precision available).

| Institution | 1990 | 1996 | 2001 | 2007 | 2011 | 2018 |
|---|---:|---:|---:|---:|---:|---:|
| Army | -0.7363 | -0.3617 | -0.0201 | -0.1011 | -0.3339 | -0.0851 |
| Police | -0.6918 | -0.4093 | -0.2433 | -0.4309 | -0.5366 | -0.1300 |
| Courts | -0.5030 | -0.2361 | **GAP** | -0.4155 | -0.4481 | -0.4271 |
| Parliament | -0.891 | -0.260 | -0.050 | -0.481 | -0.399 | -0.081 |
| Government | -0.425 | -0.361 | -0.052 | -0.586 | -0.441 | -0.552 |
| Civil service | -0.761 | -0.221 | -0.116 | -0.300 | -0.541 | -0.427 |

Courts 2001 is an explicit gap (item not fielded; phantom CSV row excluded). Note for the slide:
the army 2007 point plotted here is the full-sample -0.1011 (n.s., p=.536), not the common-sample
-0.089 quoted in the slide 6/Wald annotations — both are non-significant, but they are different fits.

## 5. Predicted probability series (slide 6 annotation)

Source: `final_checks.ipynb` cell 11 output (baseline layer4b army model; P(high confidence) =
categories 3–4, covariates at estimation-sample modes).

| Wave (year) | Religious % | Not religious % | Gap (pp) |
|---|---:|---:|---:|
| WV2 (1990) | 90.2 | 81.6 | 8.7 |
| WV3 (1996) | 90.7 | 87.2 | 3.5 |
| WV4 (2001) | 87.8 | 87.6 | 0.2 |
| WV7 (2018) | 81.2 | 79.8 | 1.3 |

Anchor checks: 8.7 / 3.5 / 0.2 / 1.3 — all MATCH.

**WV5 and WV6: NOT FOUND.** Cell 11 hard-codes `PP_WAVES = ["WV2", "WV3", "WV4", "WV7"]`; the
predicted probabilities were never computed for WV5 or WV6 and no file stores them.

Modal covariate profile (cell 13): religious-attendance mode, God-importance 10, left-right 5,
age 27, male, married. Ceiling caveat (cell 13): baseline P(high) ≈ 90%, so pp gaps compress the
log-odds story.

## 6. Supporting numbers

| Claim | Value in file | Source (row/location) | Verdict |
|---|---|---|---|
| Army–police gap WV3 = 0.7465 | 0.7465 | `layer1_gaps.csv`, WV3 row, `army_police_gap` | MATCH |
| Army–police gap WV6 = 0.0866 | 0.0866 | `layer1_gaps.csv`, WV6 row, `army_police_gap` | MATCH |
| Bootstrap mean +0.755 | +0.755 | `pressure_tests.md`, Check 1a table | MATCH |
| Bootstrap 95% SI [+0.419, +1.115] | [+0.419, +1.115] | `pressure_tests.md`, Check 1a table | MATCH |
| 94% of iterations significant | 94% | `pressure_tests.md`, Check 1a table | MATCH |
| Education joint +0.636, p=.001 | nr_joint_coef = 0.6365, nr_joint_p = 0.001 | `education_defense_table.csv`, row `conf_military,WV4` (line 3) | MATCH (0.6365 rounds to 0.637 half-up; ".636" is truncation — see DISCREPANCIES) |
| Baseline-on-joint-sample +0.694 | nr_base_jsample_coef = 0.6935 (p=.0003) | `education_defense_table.csv`, row `conf_military,WV4` (line 3) | MATCH |
| God-importance +0.509, p=.014 | markdown (cell 9): "+0.509* (p = .014)"; printed table (cell 8): "+0.508*" | `final_checks.ipynb` cells 8–9 | MATCH the markdown; last-digit inconsistency inside the notebook — see DISCREPANCIES |
| Wald army–government interaction +0.841, p=.007 | diff = +0.841, z = 2.71, p = 0.0066 | `final_checks.ipynb` cell 15 output, "army vs government / nr x WV5 interaction" | MATCH |
| Wald army–government levels p=.020 | diff = +0.507, z = 2.32, p = 0.0202 | `final_checks.ipynb` cell 15 output, "army vs government / nr total effect at WV5" | MATCH |
| Wald army–parliament p=.068 | diff = +0.398, z = 1.83, p = 0.0677 | `final_checks.ipynb` cell 15 output, "army vs parliament / nr total effect at WV5" | MATCH |
| Wald common sample n=8,777 | common sample n = 8777 | `final_checks.ipynb` cell 15 output | MATCH |
| MGCFA ΔCFI +0.0077 (metric vs configural) | delta_CFI_scaled = +0.00770 | `mgcfa_delta_fit.csv`, row `metric_vs_configural` | MATCH |
| MGCFA ΔCFI -0.0109 (scalar vs metric) | delta_CFI_scaled = -0.01095 | `mgcfa_delta_fit.csv`, row `scalar_vs_metric` | MATCH |
| MGCFA ΔCFI -0.0065 (partial scalar, military freed, vs metric) | 0.962335 - 0.968852 = -0.00652 | derived: `mgcfa_partial_scalar.csv` row `partial_free_military` CFI_scaled minus `mgcfa_fit_indices.csv` row `metric` CFI_scaled — not stored as a delta in any file | MATCH (derived) |
| MGCFA n = 5,066 | 5,066 rows | `mgcfa_input.csv` (5,066 data rows); also stated in `results/project_audit.md` line 81 | MATCH |
| MGCFA wave n's 1,242 / 1,507 / 2,317 | WV5=1,242, WV6=1,507, WV7=2,317 | counted from `mgcfa_input.csv` `wave` column; also `project_audit.md` line 81 | MATCH |
| κ range 0.245–0.524 | 0.524 (k4_kmeans), 0.41 (ward_k3), 0.245 (gmm_k3) | `cluster_kappa_summary.csv` | MATCH |
| 2011 police -2.44 SD from trend | −2.44 SD | `pressure_tests.md`, Check 5a/5b table, police row | MATCH |
| LOO +0.716 → +0.748 | drop-WV6 row: nr × WV4 = +0.748 (full-sample ref +0.716) | `pressure_tests.md`, Check 5c table | MATCH |
| Gender × police range -0.57 to -0.88 | WV3 -0.6144, WV4 -0.5737, WV5 -0.5676, WV6 -0.8836, WV7 -0.7989 (all BH-significant) | `moderator_scan_grid.csv`, rows `gender,conf_police,WV3..WV7` (lines 7–11) | MATCH (min -0.568 ≈ -0.57, max -0.884 ≈ -0.88) |

## 7. Literature check — Gündüz

**Full citation NOT FOUND.** The reference appears only as an in-text mention, no bibliography or
.bib file exists in the project:

- `partner_handoff_v2.md` line 11 (identical copy at `results/partner_handoff_v2.md` line 11):
  "Gunduz (2024) showed the partisan shift in army trust across 2007–2011–2018 — but again, army
  only, no religiosity variable, and no formal test that the change was statistically real rather
  than eyeballed from three tables."
- Also mentioned alongside Sarigil (2009, 2015) at line 27 (Ergenekon-window context).

No title, journal, or author initials anywhere in the project files. The citation must be
completed from outside the project before the deck is locked.

---

## DISCREPANCIES

1. **The six WV5 anchors come from a different model than the full-sample grid.** The anchors
   army × WV5 = +0.675, parliament × WV5 = +0.440, government × WV5 = -0.167, and totals
   army WV5 = -0.089, parliament WV5 = -0.486, government WV5 = -0.596 all match the
   **common-sample Wald trio** (`final_checks.ipynb` cell 15, army/parliament/government refit on
   the n=8,777 common sample). The full-sample values (layer4b CSV + placebo grid) are:
   army × WV5 = +0.6352, parliament × WV5 = +0.410, government × WV5 = -0.160; totals
   army WV5 = -0.1011, parliament WV5 = -0.481, government WV5 = -0.586. Neither set is wrong,
   but the deck must not mix them in one table: the main figure (item 4) uses the full-sample
   series; the Wald annotations (slide 6) use the common-sample ones.
2. **God-importance coefficient: internal notebook inconsistency.** The anchor +0.509 (p=.014)
   matches the cell 9 markdown; the printed comparison table in cell 8 shows **+0.508***. One
   unit in the last digit; the exact unrounded value was not printed anywhere. If the deck quotes
   three decimals, this needs resolving from the notebook state (not possible read-only).
3. **Education joint +0.636.** File value is 0.6365 (p = .001) — conventional half-up rounding
   gives +0.637. The anchor matches under truncation. Everything else in that row matches exactly.
4. **Not a mismatch, but NOT FOUND items to flag before lock:** exact SE and p for parliament,
   government, and civil-service baselines (item 1) and interactions (item 2) — only coef + stars
   were printed and final_checks wrote no CSV; predicted probabilities at WV5/WV6 (item 5) — never
   computed (`PP_WAVES` excludes them); full Gündüz citation (item 7).

All other anchors matched their files exactly.
