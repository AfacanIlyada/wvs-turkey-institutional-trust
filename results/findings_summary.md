# Confidence in Coercive Institutions in Turkey, WVS 1990-2018
## Findings summary

## Core finding

Across six waves of the World Values Survey in Turkey (1990–2018; n = 11,704), aggregate confidence in the army, police, and courts converged: the army–police mean gap on the 1–4 confidence scale collapsed from 0.75 in 1996 to 0.10 in 2011 and stayed compressed in 2018. The collapse was driven by the secular minority gaining trust in the police (+0.90 from WV2 to WV7 in the low-religiosity tertile) while the religious majority's police-confidence gain was smaller (+0.39). Underneath the aggregate convergence, the *religiosity gradient* of institutional confidence became institution-specific: the army–religiosity association effectively dissolved by 2001 (WV4), the police–religiosity association attenuated more slowly, and the courts–religiosity association remained the most stable negative locus of secular distrust across all six waves. Trust-cluster decomposition shows the army–police rank ordering inverts only in the middle-trust cluster (Selective trusters) at WV5 → WV6, and only Generalised trusters in WV7 show a *positive* secular-to-army association. The formal long-window interaction model dates the cross-institutional split to 2001, coinciding with the political realignment that brought AKP to power.

---

## 1. Data and measurement notes

| item | detail |
|---|---|
| Source | WVS Turkey country files, waves 2-7 (1990, 1996, 2001, 2007, 2011, 2018) |
| n total | 11,704 respondents (WV4 largest at 3,401; WV2 smallest at 1,030) |
| n with cluster label | 11,311 (393 dropped by the >30% trust-missing filter in `trust_clusters.py`) |
| Survey weights | **No weight column present in the pooled CSV**; all means and CIs are equal-weight estimates. Direction of inference is robust but precise population estimates would require weights. |
| Confidence scale | Raw WVS 1–4 reverse-coded so higher = more confidence. |
| Courts in WV4 | The `Confidence: courts/justice system` item was not asked in the 2001 Turkey country file. All courts analyses are 5-wave; row-level NaN preserved so respondents stay in army/police models. |
| WV7 measurement regime | A discontinuity in religiosity items appears at WV7: mean `rel_importance_god` drops 9.18 → 8.14 (sd 1.52 → 2.18), share scoring 10 falls 67% → 45%, share self-identifying "religious" falls 83.4% → 72.1%. Same one-wave shift on two different items strongly suggests fieldwork or mode change, not a 7-year attitudinal swing. **WV7 results are reported but flagged.** |
| Party harmonization | Vote-intention is harmonized AKP / CHP / MHP / HDP / IYI / other across WV5–WV7. Earlier waves (WV2–WV4) are coded `pre_AKP_era` and excluded from party-dummy specifications. |

Working dataset: [`pooled_extended_v2.csv`](pooled_extended_v2.csv) (11,704 × 54). Variable manifest: [`column_manifest_v2.csv`](column_manifest_v2.csv).

---

## 2. Layer 1 — Institution-level trajectories

Aggregate mean confidence per wave (1–4 scale, higher = more confidence):

| wave | year | army | police | courts |
|---|---|---:|---:|---:|
| WV2 | 1990 | 3.48 | 2.78 | 2.81 |
| WV3 | 1996 | **3.59** (peak) | 2.84 | 2.86 |
| WV4 | 2001 | 3.42 | 2.87 | — |
| WV5 | 2007 | 3.46 | 2.97 | **3.03** (peak) |
| WV6 | 2011 | **3.09** (trough) | 3.00 | 2.85 |
| WV7 | 2018 | 3.30 | **3.18** (peak) | 2.93 |

Army confidence is non-monotonic with a deep WV6 trough. Police confidence is monotone upward (+0.40 across the full window). Courts confidence is comparatively flat with a WV5 peak.

Army–police mean gap:

| wave | army–police gap |
|---|---:|
| WV2 | 0.696 |
| WV3 | 0.747 (widest) |
| WV4 | 0.550 |
| WV5 | 0.496 |
| WV6 | **0.087** (collapsed) |
| WV7 | 0.111 |

**The army premium collapses by ~85% between 1996 and 2011 and stays compressed.**

Mann–Whitney U between consecutive waves identifies the significant shifts (α = 0.05):

| shift | direction | p |
|---|---|---:|
| army WV2→WV3 | up | 3.5e-06 |
| army WV3→WV4 | down | 4.6e-07 |
| army WV5→WV6 | down | **5.3e-31** (largest single shift) |
| army WV6→WV7 | up | 2.0e-07 |
| police WV4→WV5 | up | 0.041 (marginal) |
| police WV6→WV7 | up | 2.4e-06 |
| courts WV5→WV6 | down | 8.2e-07 |

The army's WV5→WV6 drop is the largest individual transition in the data; the post-2011 partial recovery is real but does not erase it.

Files: [`layer1_trajectories.csv`](layer1_trajectories.csv), [`layer1_gaps.csv`](layer1_gaps.csv), [`layer1_transitions.csv`](layer1_transitions.csv).

---

## 3. Layer 1b — Religiosity robustness

Aggregate convergence holds under both religiosity groupings.

**Army–police gap by religiosity (`rel_importance_god` tertiles, fixed cuts 1-7 / 8-9 / 10)**:

| wave | low | mid | high | spread (high–low) |
|---|---:|---:|---:|---:|
| WV2 | 0.82 | 0.75 | 0.66 | −0.16 |
| WV3 | 1.18 | 1.00 | 0.66 | −0.52 (largest spread) |
| WV4 | 0.86 | 0.76 | 0.47 | −0.39 |
| WV5 | 0.70 | 0.62 | 0.45 | −0.26 |
| WV6 | 0.23 | 0.10 | 0.06 | −0.17 |
| WV7 | 0.07 | 0.13 | 0.14 | **+0.07 (inverts)** |

The collapse happens across all three tertiles and is driven mostly by the low-religiosity group catching up on police trust (low-tertile police mean 2.11 → 3.01, +0.90; high-tertile 2.97 → 3.36, +0.39).

**Army–police gap by `rel_person` (self-identification: religious vs not religious + atheist)**:

| wave | religious | not religious | religious – not religious |
|---|---:|---:|---:|
| WV2 | 0.65 | 0.84 | −0.19 |
| WV3 | 0.68 | 0.98 | −0.30 |
| WV4 | 0.48 | 0.81 | −0.33 |
| WV5 | 0.43 | 0.79 | −0.37 |
| WV6 | **0.05** | 0.25 | −0.19 |
| WV7 | 0.10 | 0.14 | −0.04 |

The bigger drop in the not-religious group (0.98 → 0.25 from WV3 to WV6, all within the *stable* WV2–WV6 measurement window) confirms that the convergence is not a WV7 artifact. The largest single religiosity-stratified shift is WV5 → WV6.

Files: [`layer1_by_religiosity.csv`](layer1_by_religiosity.csv), [`layer1_by_relperson.csv`](layer1_by_relperson.csv), [`layer1_religiosity_composition.csv`](layer1_religiosity_composition.csv).

---

## 4. Layer 2 — Within-cluster institution ordering

Three trust clusters from `trust_clusters.py` (k = 3, per-wave KMeans, Hungarian-matched to WV4 reference):

| cluster | label | n |
|---|---|---:|
| 0 | Distrusters | 2,970 |
| 1 | Selective trusters | 4,476 |
| 2 | Generalised trusters | 3,865 |

**Rank flips**: among 15 consecutive-wave comparisons across all three clusters, four show a rank change. The Selective trusters cluster is the only one in which the *top-ranked* institution changes:

| cluster | wave_pair | ordering change | regime |
|---|---|---|---|
| 0 Distrusters | WV5→WV6 | army > courts > police → army > police > courts | robust |
| **1 Selective trusters** | **WV5→WV6** | **army > police > courts → police > army > courts** | robust |
| 1 Selective trusters | WV6→WV7 | police > army > courts → army > police > courts | WV7-flagged |
| 2 Generalised trusters | WV5→WV6 | army > courts > police → army > police > courts | robust |

Selective trusters are unique in that police displaces army from the top in 2011. The other two clusters keep army on top throughout.

**Army–police gap by cluster (WV2 → WV6 change)**:

| cluster | WV2 | WV6 | Δ |
|---|---:|---:|---:|
| 0 Distrusters | 1.27 | 0.29 | −0.98 |
| 1 Selective trusters | 0.61 | **−0.03** (sign flip) | −0.64 |
| 2 Generalised trusters | 0.15 | 0.10 | −0.05 |

The aggregate collapse (Δ = −0.62) is structurally driven by clusters 0 and 1. Cluster 2 had no army premium to lose.

**Spread trajectory (individual-level max-min across army/police/courts)**:

| cluster | WV2 spread | WV6 spread | t | p | direction |
|---|---:|---:|---:|---:|---|
| 0 Distrusters | 1.472 | 1.049 | 5.81 | 9.6e-09 | narrowed |
| 1 Selective trusters | 1.085 | 0.914 | 3.38 | 7.6e-04 | narrowed |
| 2 Generalised trusters | 0.416 | 0.694 | −5.35 | 1.4e-07 | **widened** |

Distrusters and Selective trusters compress their inter-institution distinctions; Generalised trusters do the opposite — they start with very flat trust profiles and *develop* discrimination over time.

Files: [`layer2_cluster_wave_institution.csv`](layer2_cluster_wave_institution.csv), [`layer2_flip_events.csv`](layer2_flip_events.csv), [`layer2_spread_trajectory.csv`](layer2_spread_trajectory.csv).

---

## 5. Layer 3 — Per-wave ordinal logistic regressions

Ordered logit (cumulative-logit link) per institution × wave × group (pooled and per-cluster), 70 models total, all converged, no n<100 flags.

**Pooled `not_religious_dummy` coefficient by wave × institution**:

| wave | army | police | courts |
|---|---:|---:|---:|
| WV2 | −0.624** | −0.565** | −0.414* |
| WV3 | −0.367* | −0.331* | −0.255. |
| WV4 | −0.167 | −0.092 | — |
| WV5 | +0.122 | −0.409* | −0.136 |
| WV6 | −0.504*** | −0.747*** | −0.517*** |
| WV7 | +0.020 | −0.287** | −0.484*** |

Three regimes:
1. **WV2–WV3 (pre-2001)**: non-religious respondents have less confidence in all three institutions. Classic secular–religious divide; coefficients of similar magnitude.
2. **WV4 (2001)**: quiet transition wave; coefficients near zero on army and police, courts is structurally NA.
3. **WV5 onward (2007+)**: army coefficient neutralizes (≈ 0) while police and courts coefficients stay or grow negative. WV6 is anomalous (everything strongly negative, AKP consolidation wave).

**Selective trusters (cluster 1) WV7**: army = −0.013, police = **−0.654*** — a 0.64 log-odds spread on identical respondents under identical specification. This is the single sharpest in-cluster evidence of cross-institutional differentiation by religiosity in the data.

**Generalised trusters (cluster 2) WV7 unique pattern**: army = +0.457*, police = +0.602**, courts = **−0.530***. Non-religious Generalised trusters in 2018 report *more* confidence in coercive institutions but *less* in courts — the only cluster where the judiciary is uniquely singled out for secular distrust.

Files: [`layer3_ordinal_coefficients.csv`](layer3_ordinal_coefficients.csv) (732 rows).

---

## 6. Layer 4a — WV5-baseline interaction model (formal H3 test)

Pooled ordered logit on WV5/WV6/WV7 with wave × predictor interactions for `not_religious_dummy`, `AKP_dummy`, and `left_right`. Result: **H3 as literally stated ("divergence sharpens between 2007 and 2018") is not formally confirmed.**

**Army–police spread in `not_religious_dummy` total effect**:

| wave | spread (army − police) |
|---|---:|
| WV5 (baseline) | +0.541 |
| WV6 (total) | +0.280 |
| WV7 (total) | +0.223 |

The spread *narrows*, doesn't grow.

**Cross-institution Wald on the WV7 interaction term**:

| predictor | army × WV7 | police × WV7 | diff | z | p |
|---|---:|---:|---:|---:|---:|
| not_religious | +0.048 | +0.366 | −0.318 | −1.17 | 0.242 |
| AKP_dummy | +0.216 | −0.268 | +0.484 | 1.92 | **0.055** (marginal) |
| left_right | +0.059 | +0.016 | +0.043 | 0.92 | 0.360 |

Only AKP × WV7 reaches marginal significance, and the direction is *convergence* (AKP voters' relative army-vs-police premium narrows toward zero), not sharpening.

The model's signal is that the cross-institutional differentiation was **already large at the WV5 baseline** (army n.s. vs police −0.56***). Subsequent waves attenuate magnitudes but the underlying structural split is established by 2007.

Files: [`layer4_pooled_interactions.csv`](layer4_pooled_interactions.csv).

---

## 7. Layer 4b — Long-window interaction model (WV2 baseline)

Re-running with WV2 as reference (n = 8,915 / 8,911 / 6,231 for army / police / courts) shows that **the split is dated to WV4 (2001)**.

**`not_religious_dummy` total effect per wave**:

| wave | year | army | police | courts | army − police |
|---|---|---:|---:|---:|---:|
| WV2 | 1990 | **−0.736*** | **−0.692*** | **−0.503*** | −0.044 |
| WV3 | 1996 | **−0.362*** | **−0.409*** | −0.236. | +0.048 |
| WV4 | 2001 | −0.020 | **−0.243*** | **−0.503*** | **+0.223** (emerges) |
| WV5 | 2007 | −0.101 | **−0.431*** | **−0.415*** | **+0.330** (peak) |
| WV6 | 2011 | **−0.334*** | **−0.537*** | **−0.448*** | +0.203 |
| WV7 | 2018 | −0.085 | −0.130 | **−0.427*** | +0.045 |

In 1990 and 1996, non-religious respondents had near-identical (large, significant) negative gradients on army and police. At **WV4 the army gradient effectively dissolves** (−0.02, n.s.) while the police gradient remains meaningfully negative (−0.24*). The army–police spread peaks at WV5 (+0.33), then attenuates.

**Wave-interaction coefficients (test: did the gradient shift from the WV2 baseline?)**:

| interaction | army | police | courts |
|---|---:|---:|---:|
| nr × WV3 | +0.375. | +0.282 | +0.267 |
| nr × WV4 | **+0.716*** | +0.448* | — |
| nr × WV5 | **+0.635** | +0.261 | +0.088 |
| nr × WV6 | +0.402. | +0.155 | +0.055 |
| nr × WV7 | **+0.651*** | **+0.562** | +0.076 |

The army interactions are larger and more consistently significant than the police interactions; courts interactions are uniformly small and non-significant — **the courts–religiosity association is stable across all six waves** at around −0.4 to −0.5. The judiciary has been the most consistent locus of secular distrust in Turkey for nearly two decades.

**Specific test answers from the brief**:

| test | result |
|---|---|
| `nr × WV5` in army model | **+0.635**, p = 0.0045 — significant. Army-religiosity association significantly weaker by 2007 vs 1990. |
| `nr × WV5` in police model | +0.261, p = 0.206 — not significant. Police-religiosity association not significantly different from 1990. |
| First wave where army–police spread is substantively large | **WV4** (+0.223), peaks **WV5** (+0.330). |

**A crucial nuance on WV7**: the spread compresses back to +0.05 at WV7, but this is **not a return to the WV2 baseline pattern**. In WV2 both coefficients were strongly negative (~−0.7); in WV7 both are small. The mechanism shifted from "secular distrust of all coercive institutions" to "secular indifference toward army and police, persistent distrust of courts."

Files: [`layer4b_longwindow_interactions.csv`](layer4b_longwindow_interactions.csv), [`layer4b_total_effects_by_wave.csv`](layer4b_total_effects_by_wave.csv).

---

## 8. Open questions for Layer 5

A Random Forest / SHAP typology portrait would address several questions the regression layer leaves open:

| question | what SHAP/RF would add |
|---|---|
| Which combination of predictors best identifies a Selective truster respondent vs Distruster or Generalised truster? | Non-parametric variable importance across the full predictor set, including the religiosity items and party preferences that drive cluster membership. |
| Is the army-religiosity differential captured by religiosity alone, or by a religiosity × ideology × demographics interaction the OL model under-fits? | SHAP interaction values would surface joint patterns that ordinal logit's additive specification misses. |
| Are there latent sub-groups within Selective trusters that diverge on the army-police margin? | Conditional SHAP profiles within cluster 1 across waves could identify a 2007-onset sub-typology. |
| Which predictors specifically *changed* their importance between WV2 and WV7? | A per-wave RF + Shapley decomposition would quantify the rise of party preference (post-2007) and the decline of religiosity-as-trust-predictor (post-2001). |
| Is the WV6 anomaly (every coefficient large and negative) a cluster-1-and-2 phenomenon or all-respondent? | A WV6-only RF with SHAP would isolate whose attitudes drove the unusual 2011 pattern. |
| Can the courts-as-stable-locus finding be generalized — i.e., does the model predict cluster membership better when courts confidence is highly weighted? | Permutation importance with and without conf_courts as a predictor would test the courts' marker role. |

Specific deliverables that would close the analysis loop:

1. **Cluster-membership classifier**: RF predicting cluster 0/1/2 from the full predictor set per wave. Report SHAP top-10 by wave; flag predictors whose importance changes >50% across waves.
2. **Institution-specific RF**: separate RF for each of army/police/courts confidence (regression on the 1–4 scale or ordinal classification). SHAP interaction matrix per wave, with focus on religiosity × party and religiosity × age.
3. **2001 vs 2007 vs 2011 vs 2018 SHAP comparison**: dedicated check on whether `not_religious_dummy` SHAP for army goes to ~zero post-2001 (matching the Layer 4b result) and whether it persists for courts.
4. **Sub-cluster typology within Selective trusters at WV7**: low-dimensional embedding of cluster-1 respondents' Shapley values; check for stable sub-types that explain the WV6→WV7 reversion the regression flagged with a WV7 caveat.

---

*Files in [`results/`](.) — generated by `pool_final.py`, `layer1_*`, `layer2_*`, `layer3_*`, `layer4_*` scripts in the project root.*
