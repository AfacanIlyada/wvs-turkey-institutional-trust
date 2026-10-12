# Project audit — WVS Turkey "From Bloc to Split"

Audit date: 2026-07-07. Scope: read-only verification of `results/partner_handoff.md` against files on disk. No analysis re-run, no files modified (this report is the only new file).

## Verdict

- **(a) Internally consistent and presentation-ready: YES, with one wording fix.** Every headline number traces to an output file and matches; the analysis pipeline is complete and each handoff claim has a producing script.
- **(b) Discrepancies: one substantive, three cosmetic.** Substantive: the courts item was **not asked in WV4 (2001)** — the handoff's "courts coefficients −0.41 to −0.52 across WV4–WV7" overstates the wave range, and the WV4 courts row in `layer4b_total_effects_by_wave.csv` (−0.503) is the WV2 baseline carried forward, not an estimate. Cosmetic: the 2011 army–police gap is 0.087 (the core-finding paragraph's "0.10" should be "0.09"); the dataset has six confidence items, not the "five" the handoff states; a newer `partner_handoff_v2.md` exists alongside the declared source of truth.
- **(c) Before slides:** (1) restate the courts claim as "WV5–WV7 (−0.42 to −0.45, all significant; WV2 baseline −0.50); item not fielded in 2001" and cite the long-window model, not the per-wave models (per-wave WV5 courts is −0.14, n.s.); (2) use 0.09 for the 2011 gap everywhere; (3) decide whether the post-handoff moderator scan (run today — gender × police and education × army are strongly BH-significant) enters the deck or stays an appendix.

## 1. File inventory

All 20 files listed in the handoff's Files section exist on disk. No missing references.

### Data + analysis chain (current)

| File | Size | Modified | Role |
|---|---|---|---|
| `F00013222…WV7…xlsx` + 6 other `F000*.xlsx` | 0.8–3.0M | May 18–25 | raw WVS country files (WV2–WV7) |
| `F000*…pdf` ×5, `F00001374…2007.pdf` | 0.3–3.4M | May 25 | questionnaires / results docs |
| `pool_final.py` | 25K | May 25 22:07 | builds definitive dataset |
| `results/pooled_extended_v2.csv` | 2.3M | May 25 22:07 | **definitive dataset** (11,704 × 54) |
| `results/column_manifest_v2.csv` | 5.2K | May 25 22:07 | data dictionary |
| `results/integrity_report_v2.txt` | 6.8K | May 25 22:07 | missingness report (not listed in handoff Files) |
| layer/cluster/mgcfa scripts (see §4) | — | May 25 | analysis pipeline |
| `results/layer*.csv`, `cluster_*`, `mgcfa_*` | — | May 25 | outputs, all present |
| `results/findings_summary.md` | 17K | May 25 22:53 | per-layer narrative |
| `results/pressure_tests.md` | 12K | May 25 23:08 | 5 robustness verdicts |
| `results/partner_handoff.md` | 5.8K | May 25 23:24 | **declared source of truth** |

### Flags

| Flag | Files | Note |
|---|---|---|
| **Newer handoff exists** | `results/partner_handoff_v2.md` (15K, May 25 23:43) | Superset of v1: adds lit review, timeline, step-by-step map. All shared numbers identical to v1. Decide which one partners get; v2 is the more complete document. |
| **Post-handoff work (today)** | `moderator_scan.ipynb` (Jul 7 15:29), `results/moderator_scan_grid.csv` (Jul 7 15:30), `results/figs_scan/` ×5 PNG | Exploratory moderator scan, self-labelled "not new headline analysis". Not mentioned in either handoff. See §4. |
| Superseded datasets | `results/pooled_all_scales.csv`, `results/pooled_extended.csv` (v1), `results/pooled_with_clusters.csv` | v2 is definitive; `pooled_with_clusters.csv` is the intermediate that sourced the `cluster` column. Keep but don't ship. |
| Stale crosswalks | `WVS_TR_concept_crosswalk.csv`, `_v2.csv` | `_v3.csv` (May 25 22:07, written by `pool_final.py`) is current. |
| Exploration byproducts (orphans, root dir) | `attribute_search.csv/.py`, `availability_matrix.csv`, `availability_check.py`, `candidate_vars.csv`, `cluster_discrimination.csv`, `column_inventory.csv/.py`, `concept_coverage.csv`, `crosswalk_expand.py`, `resolve_candidates.py`, `wave_columns_WV2–WV7.csv` | Phase-0 variable-hunting; harmless, not referenced by handoff. |
| Script outputs not on disk | `cluster_elbow.csv`, `cluster_elbow_*.png`, `cluster_profiles_<wave>.csv`, radar PNGs for WV3–WV6 | `trust_clusters.py` writes these; only `cluster_profiles_all.csv` and WV2/WV7 radars remain. Presumably cleaned up; nothing downstream depends on them. |
| Duplicated code | `mgcfa_analysis.R` vs `mgcfa_runner.py` | The runner embeds the same lavaan code as the standalone .R file. Same outputs; not a conflict. |

## 2. Dataset check — `pooled_extended_v2.csv`

Shape **11,704 × 54** — matches the handoff exactly.

| Wave | Year | n | conf items (of 6) | 3 religiosity | party_recode | left_right | demographics |
|---|---|---:|---|---|---|---|---|
| WV2 | 1990 | 1,030 | all 6 | .97–1.00 | 1.00 | .87 | complete |
| WV3 | 1996 | 1,907 | all 6 | .75–.77 | 1.00 | .92 | complete |
| WV4 | 2001 | 3,401 | **5 — courts absent** | .98–1.00 | 1.00 | .96 | complete |
| WV5 | 2007 | 1,346 | all 6 | .98–1.00 | .63 | .85 | complete |
| WV6 | 2011 | 1,605 | all 6 | .98 | .77 | .91 | complete |
| WV7 | 2018 | 2,415 | all 6 | .91–.99 | .92 | .89 | complete |

Wave n's sum to 11,704. Coverage of key variables is ≥85% everywhere except religiosity in WV3 (~75%) and party in WV5/WV6 (.63/.77) — known, not flagged in handoff but visible in `integrity_report_v2.txt`. Note the dataset carries **six** confidence items (military, police, courts, parliament, government, civil_service); the handoff text says "five".

### Resolved: WV4 courts

**The early session was right: WV4 (2001) does NOT have the confidence-in-courts item.** Evidence:

- `pooled_extended_v2.csv`: 0 non-null `conf_courts` values in WV4 (all other waves ≥1,007).
- `findings_summary.md` line 19 states it explicitly: "The `Confidence: courts/justice system` item was not asked in the 2001 Turkey country file. All courts analyses are 5-wave."
- `layer1_transitions.csv`: courts WV3→WV4 and WV4→WV5 rows say "skipped (one wave missing)".
- `layer4b_longwindow_interactions.csv`: the courts model has no `wave_WV4` or `nr_x_WV4` terms (n=6,231 vs 8,915 for army).

The handoff's "courts coefficients across WV4–WV7" is therefore a drafting error. Its likely source: `layer4b_total_effects_by_wave.csv` lists a WV4 courts total effect of −0.503 — but that value is identical to the WV2 baseline row, i.e., the missing interaction was treated as zero when tabulating. It is not an estimate of anything in 2001.

## 3. Results verification

| # | Handoff claim | File | On disk | Result |
|---|---|---|---|---|
| 1 | Army–police gap 0.75 (1996) → 0.09/0.10 (2011) | `layer1_gaps.csv` | WV3 = 0.7465; WV6 = **0.0866** | **MATCH** (as 0.75 → 0.09; the "0.10" in the core-finding paragraph is a rounding slip) |
| 2 | `nr × WV4` army interaction +0.716, p<.001 | `layer4b_longwindow_interactions.csv` | coef = +0.7162, p = 8.95e-05 | **MATCH** |
| 3 | Courts religiosity coefficients −0.41 to −0.52 across WV4–WV7, all significant | `layer3_ordinal_coefficients.csv` / `layer4b_total_effects_by_wave.csv` | Layer 3 per-wave: WV2 −0.414*, WV3 −0.255·, WV4 **absent**, WV5 **−0.136 n.s.**, WV6 −0.517***, WV7 −0.484***. Layer 4b total effects: WV5 −0.4155**, WV6 −0.4481**, WV7 −0.4271*** (WV4 row = phantom baseline) | **MISMATCH** on the wave range and on which model supports it. True statement: long-window total effects −0.42 to −0.45 across **WV5–WV7**, all significant, with WV2 baseline −0.50; courts not measured in WV4; the per-wave WV5 model does not reach significance on its own |
| 4 | Middle-cluster army→police flip at WV6 | `layer2_flip_events.csv` | Cluster 1 (Selective trusters), WV5→WV6: [army > police > courts] → [police > army > courts], regime "robust (WV2–WV6)"; reverts WV6→WV7 (WV7-flagged) | **MATCH** |
| 5a | MGCFA metric holds, ΔCFI = +0.008 | `mgcfa_delta_fit.csv` | ΔCFI_scaled metric vs configural = +0.0077 | **MATCH** (scaled index) |
| 5b | Full scalar fails, ΔCFI = −0.011 | `mgcfa_delta_fit.csv` | ΔCFI_scaled scalar vs metric = −0.0109 | **MATCH** |
| 5c | Partial scalar holds with conf_military freed, ΔCFI = −0.007 | `mgcfa_partial_scalar.csv` | CFI_scaled 0.9623 (free military) vs metric 0.9689 → −0.0065; freeing military is the best of the 5 partial variants | **MATCH** |

Additional spot-checks, all confirmed: MGCFA n = 5,066 (`mgcfa_input.csv`, WV5/6/7 = 1,242/1,507/2,317); bootstrap +0.755, 95% SI [+0.419, +1.115], 94% significant (`pressure_tests.md`); WV6 police effect −2.44 SD from trend, LOO +0.716 → +0.748 (`pressure_tests.md`); κ = 0.245–0.524, agreement 50.1–69.3%, flip reproduced in all 3 alternative methods (`cluster_kappa_summary.csv` — note GMM also flags a WV7 flip); restricted no-WV4 sample n = 6,246/6,242/6,231 ≈ handoff's "≈6,240" (`pressure_tests.md`); army mean drop at WV6 p = 5.25e-31 (`layer1_transitions.csv`); layer4b model n's 8,915/8,911/6,231 as cited.

## 4. Analysis map

| Script | Models / tests fit | Output |
|---|---|---|
| `column_inventory.py` | KMeans k=3 (initial clustering) | `column_inventory.csv`, `cluster_discrimination.csv`, `results/pooled_with_clusters.csv` |
| `trust_clusters.py` | KMeans k=2–6 elbow + final k=3 per wave | `cluster_composition.csv`, `cluster_profiles_all.csv`, `cluster_sociodemographic_profiles.csv`, radar/composition PNGs |
| `pool_extended.py` → `pool_final.py` | dataset builds (no models) | `pooled_extended.csv` → **`pooled_extended_v2.csv`**, `column_manifest_v2.csv`, `integrity_report_v2.txt`, crosswalk v2/v3 |
| `layer1_trust_trajectories.py` | wave means; Mann-Whitney U per transition | `layer1_trajectories.csv`, `layer1_gaps.csv`, `layer1_transitions.csv` |
| `layer1_by_religiosity.py` / `layer1_by_relperson.py` | group-mean trajectories, 2 religiosity measures | `layer1_by_religiosity.csv`, `layer1_by_relperson.csv` |
| `religiosity_composition.py` | composition shares per wave | `layer1_religiosity_composition.csv` |
| `layer2_cluster_institutions.py` | Welch t-tests; rank orderings per cluster × wave | `layer2_cluster_wave_institution.csv`, `layer2_flip_events.csv`, `layer2_spread_trajectory.csv` |
| `layer3_ordinal_regressions.py` | 70 ordered logits (3 institutions × 6 waves × pooled + 3 clusters; courts 5-wave) | `layer3_ordinal_coefficients.csv` (732 rows) |
| `layer4_pooled_interactions.py` | WV5-baseline ordered logit with wave interactions (formal H3 test; nr, AKP, left-right) | `layer4_pooled_interactions.csv` |
| `layer4b_longwindow.py` | WV2-baseline ordered logit × 3 institutions (**headline 2001 dating**) | `layer4b_longwindow_interactions.csv`, `layer4b_total_effects_by_wave.csv` |
| `pressure_tests.py` | downsampled bootstrap; tertile decomposition; KMeans re-fit; restricted-sample refits; OLS trend + leave-one-out | `pressure_tests.md` |
| `cluster_robustness.py` | KMeans k=4, Ward k=3, GMM k=3; Cohen's κ vs original | `cluster_robustness.csv`, `cluster_kappa_summary.csv` |
| `mgcfa_runner.py` (embeds `mgcfa_analysis.R`) | lavaan WLSMV MGCFA: configural/metric/scalar + 5 partial-scalar variants, WV5–WV7 | `mgcfa_input.csv`, `mgcfa_fit_indices.csv`, `mgcfa_delta_fit.csv`, `mgcfa_partial_scalar.csv`, `mgcfa_loadings.csv` |
| `moderator_scan.ipynb` — **post-handoff, run 2026-07-07** | 15 ordered logits: 5 moderators (gender, cohort, education, income, left-right) × 3 institutions, WV2 baseline, BH correction over 70 interaction tests | `results/moderator_scan_grid.csv`, `results/figs_scan/*.png` |
| Phase-0 exploration (`availability_check.py`, `attribute_search.py`, `crosswalk_expand.py`, `resolve_candidates.py`) | variable discovery, no models | root-level CSVs |

**Exploratory results that never made the handoff** (from the Jul 7 moderator scan; 25 of 70 interactions BH-significant): gender × police is negative WV3–WV7 (women's relative police confidence declined, β ≈ −0.88/−0.80 in WV6/WV7 — the notebook notes the handoff's police-trust convergence is concentrated among men); education × army positive WV3–WV7 (β +0.65 to +1.02, partially proxying the religiosity realignment); left-right × all three institutions positive at WV7 (all WV7-caveated); cohort × army mid-period only; income × army one borderline cell. The notebook self-labels these as exploratory appendix material — but gender × police is a strong, six-wave-robust pattern a reviewer could reasonably ask about.
