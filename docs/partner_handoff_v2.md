# Partner handoff: WVS Turkey institutional confidence, 1990-2018

## What this paper is about and where it sits in the literature

The central question is simple: in Turkey, did the army, the police, and the courts always mean the same thing to the public — or did they start meaning different things as politics shifted?

For most of the 1990s the answer was: they were one bloc. If you trusted one coercive institution, you tended to trust the others. Tessler and Altinoglu (2004) showed this empirically using the 1997 WVS — they treated army, police, and courts as a single "institutions of order" index because the data supported it. That is our starting point, our "before" photograph.

Then the AKP came to power in 2002 and started changing each institution in different ways and on a different schedule. The army was humbled through the Ergenekon trials (2007–2012), then purged after the 2016 coup attempt. The police expanded and became the government's main enforcement arm. The courts were restructured through the 2010 referendum and the post-2016 purges. If those changes were as politically significant as the historical record suggests, they should show up in how different groups of people started trusting each institution differently.

Two papers have looked at pieces of this. Sarigil (2009, 2015) showed that religiosity and political identity predicted army trust differently at different points in time — but he only looked at the army, never the police or courts. Gunduz (2024) showed the partisan shift in army trust across 2007–2011–2018 — but again, army only, no religiosity variable, and no formal test that the change was statistically real rather than eyeballed from three tables.

What we do that none of them do: we look at all three institutions together, we include religiosity as a predictor, we run formal statistical tests for whether the relationships changed, and we use a longer time window (back to 1990) that lets us establish what the baseline looked like before AKP existed.

---

## The empirical story — a timeline

- **1990–1996** — Army, police, and courts move together in public opinion. Non-religious Turks distrust all three equally (coefficients ~−0.7 on all). The coercive bloc is one object. Army sits comfortably at the top of every group's trust ranking.

- **2001** ⚡ — The army-religiosity association dissolves in one wave transition (coefficient drops from −0.36 to −0.02). Police and courts associations stay negative. This is the split point — dated formally by our interaction model, predating every event the prior literature focuses on. AKP has not yet taken office; the 2001 economic crisis and the collapse of the old party system are the backdrop.

- **2002–2006** — AKP in power, consolidating. No WVS wave in this window, but the 2007 wave captures the outcome: army effect stays near zero, police and courts effects persist. The split established in 2001 is now structurally embedded.

- **2007** — Peak divergence. Army: n.s. Police: −0.43*. Courts: −0.42*. The army-police spread in the religiosity gradient is at its widest (+0.33 log-odds). Middle-trust respondents still rank army above police, but the gap has narrowed.

- **2007–2011** — Ergenekon trials. Senior military officers prosecuted. Army prestige collapses. This is the window that Gunduz and Sarigil write about — but the data show the religiosity split was already in place before this period began.

- **2011** ⚡ — Largest single-wave shift in the data. Army mean drops sharply (p = 5.3e-31). Middle-trust respondents flip: police overtakes army as their most trusted institution for the first time. WV6 is a statistical outlier (−2.4 SD from trend on police effect) — a temporary intensification that reverts by 2018. All three institutions go strongly negative on religiosity this wave, suggesting peak political polarization.

- **2013** — Gezi protests. AKP-Gülen split. Police becomes the visible face of government enforcement. Falls between WV6 and WV7 — we cannot observe this window directly.

- **2016** — Coup attempt. Army purged and resubordinated to the executive. Falls between WV6 and WV7.

- **2018** — New equilibrium. Army and police effects both near zero (n.s.). Courts remains the only institution with a stable, significant secular-distrust signal (−0.43*). The army-police gap stays compressed. Middle-trust respondents revert to army > police in ranking, but the gap is a fraction of what it was in 1996. Note: WV7 has a measurement discontinuity in religiosity items — treat 2018 figures as directionally informative, not directly comparable to earlier waves.

---

## What we actually did — step by step

Here is every analysis we ran, what it was trying to find out, and what it found. Think of it as a checklist you can verify against the output files.

**Step 1 — Build the dataset**
We pooled six WVS Turkey country files (1990 to 2018, 11,704 respondents total) into one dataset with 54 variables: the five confidence items, three religiosity measures, party preference, left-right self-placement, demographics, and a range of values and attitudes variables. Output: `pooled_extended_v2.csv`.

**Step 2 — Track average trust in each institution across waves**
We computed mean confidence in army, police, and courts per wave and looked at how the gap between army and police changed over time. *Finding: the army-police gap collapsed from 0.75 in 1996 to 0.09 in 2011 and stayed compressed.* The biggest single drop was 2007→2011. Output: `layer1_trajectories.csv`, `layer1_gaps.csv`.

**Step 3 — Check whether secular vs religious respondents drove that collapse**
We split respondents by religiosity and tracked the army-police gap separately for each group across all waves. We ran this twice with two different religiosity measures to make sure the result was not an artifact of how we measured religion. *Finding: secular respondents drove the convergence by gaining police trust, not by losing army trust. The pattern holds under both measures and is not a WV7 measurement artifact.* Outputs: `layer1_by_religiosity.csv`, `layer1_by_relperson.csv`.

**Step 4 — Look inside the trust clusters**
Respondents had been grouped into three trust types (low, middle, high trust across all institutions). We checked whether the internal ranking of army vs police vs courts shifted differently for each group across waves. *Finding: only the middle-trust group flipped — army was their most trusted institution until 2007, police overtook it by 2011. The other two groups kept army on top throughout.* Output: `layer2_cluster_wave_institution.csv`, `layer2_flip_events.csv`.

**Step 5 — Run regressions: does religiosity predict each institution differently?**
For each wave and each institution, we ran an ordinal logistic regression asking: does being non-religious predict more or less confidence in army / police / courts, controlling for age, education, income, gender, and party? We ran these both for all respondents pooled and separately per cluster. *Finding: in the 1990s, being non-religious predicted less confidence in all three institutions equally. By 2007, the army effect had effectively disappeared while the police and courts effects persisted. The sharpest single result: within the middle-trust group in 2018, being non-religious predicted army confidence near zero but police confidence strongly negatively — a 0.64 log-odds gap on the same respondents.* Output: `layer3_ordinal_coefficients.csv`.

**Step 6 — Formally test when the split happened (the main contribution)**
We ran one pooled model across all six waves with the 1990 wave as the baseline, and added interaction terms to test whether the religiosity-army relationship changed significantly from its 1990 level in each subsequent wave. *Finding: the army-religiosity association changed significantly at the 2001 wave (+0.72 log-odds, p<.001), while the police and courts associations barely moved. The split predates Ergenekon by at least six years.* Output: `layer4b_longwindow_interactions.csv`.

**Step 7 — Pressure test the main findings**
We ran five robustness checks targeting the five most vulnerable claims: (1) is the 2001 finding just a power artifact from the large WV4 sample? (2) is the secular police-trust gain compositional? (3) are the cluster labels stable enough to support the flip finding? (4) is the courts stability finding real or a sample-size artifact? (5) is WV6 (2011) genuinely anomalous or just noisy? *Results: 3 clear passes, 1 weakness (timing of the secular police-trust gain is uncertain), 1 qualified fail (cluster labels are method-sensitive, but the flip finding itself survives all four alternative clustering methods).* Output: `pressure_tests.md`.

**Step 8 — Test measurement quality across waves (MGCFA)**
Using a confirmatory factor analysis across the 2007, 2011, and 2018 waves, we tested whether the confidence items measured the same underlying construct in the same way in each wave. *Finding: loadings are equivalent (metric invariance holds), but the army item's response thresholds shifted across waves — meaning respondents in 2007 and 2018 were not using quite the same internal scale when rating army confidence. This independently confirms the army as the contested institution.* Outputs: `mgcfa_fit_indices.csv`, `mgcfa_partial_scalar.csv`.

**Step 9 — Test cluster robustness**
Because the cluster labels showed moderate fragility in Step 7, we re-ran the clustering three additional ways (k=4 k-means, Ward hierarchical, Gaussian mixture) and checked whether the army→police flip in the middle-trust group still appeared. *Finding: the flip reproduces in all three alternative clustering methods, even though the cluster boundaries move substantially (agreement with original labels 50–69%).* Output: `cluster_robustness.csv`, `cluster_kappa_summary.csv`.

---

## Core finding

Across six WVS Turkey waves (n=11,704, 1990-2018), aggregate confidence in army, police, and courts converged — the army-police mean gap collapsed from 0.75 in 1996 to 0.10 in 2011 and stayed compressed in 2018. Beneath this convergence, the religiosity gradient on institutional confidence split by institution: the army-religiosity association effectively dissolved by 2001 (`nr × WV4` = +0.72***), while police and especially courts associations persisted. The middle-trust cluster shows an army→police rank inversion at WV6 (2011), reproducing across four independent clustering methods. Multi-group CFA confirms the army as the non-invariant measurement object — partial scalar invariance holds only when conf_military thresholds are freed. The split is dated to 2001, predating Ergenekon, Gezi, and the 2016 coup.

## Four contributions

**1. The 2001 dating.** The army-religiosity association detached from the police-religiosity and courts-religiosity associations between 1996 and 2001. Long-window ordinal logit with WV2 baseline: `nr × WV4` = +0.716***, p<.001. Bootstrap with WV4 downsampled to n=1,030 returns mean +0.755 with 95% simulation interval [+0.42, +1.12]; 94% of iterations significant. Cohen's d ≈ 0.40 (medium). The split predates Ergenekon (2007-2012), the 2013 Gezi protests, and the 2016 coup attempt — revising the implicit timeline that places the army-religion realignment in the late 2000s.

**2. Courts as the stable locus.** Religiosity coefficients on conf_courts are −0.41 to −0.52 across WV4-WV7, all significant. The judiciary, not the army, is the consistent object of secular distrust. Holds on the restricted same-sample comparison: when army and police are re-run on the no-WV4 sample alongside courts (n ≈ 6,240 each), courts interactions stay below 0.30 (n.s.) while army interactions remain large and significant. This finding is invisible in army-only analyses, which dominate the civil-military relations literature.

**3. Middle-trust cluster institutional flip at WV6.** The middle cluster shows an army→police rank inversion in 2011. Reproduces across (i) original Hungarian-matched k=3 KMeans, (ii) k=4 KMeans (where the original middle cluster splits into a "state-security loyalist" sub-type and a moderate one), (iii) Ward hierarchical k=3, (iv) Gaussian mixture k=3. Cluster *labels* are method-sensitive (κ vs original: 0.25-0.52), but the flip *finding* is method-invariant. In the paper: refer to "middle-trust respondents" rather than "Selective trusters" — the typological label is not load-bearing.

**4. MGCFA measurement triangulation.** Multi-group CFA on WV5/6/7 (n=5,066, WLSMV, ordinal indicators). Metric invariance holds (ΔCFI = +0.008). Full scalar fails just past the conventional threshold (ΔCFI = −0.011). Partial scalar with conf_military thresholds freed holds (ΔCFI = −0.007). The army item is independently identified as the non-invariant measurement element — psychometric confirmation that the army was the politically contested object. Latent-mean comparisons valid under partial scalar; direct conf_military mean comparisons across waves require this caveat.

## Two findings to report with qualification

**A. Convergence mechanism.** The secular police-trust gain is real: police mean rises +0.99 from WV2 to WV7 on the restricted-floor sample (rel_importance_god ≤ 5), broad-based across education tertiles. But the within-not-religious WV5→WV6 step is not significant (Mann-Whitney p = 0.22); most of the gain concentrates in WV6→WV7, overlapping the WV7 measurement caveat. Claim: "convergence is established by 2018 across all religiosity groups." Do not claim the precise timing.

**B. WV6 anomaly.** 2011 confirmed as a statistical outlier — police effect −2.4 SD from the trend through the other five waves, army −1.3 SD. Isolated: leave-one-out shows `nr × WV4` changes from +0.716 to +0.748 when WV6 is dropped. Report as: "2011 represents a temporary intensification of the religiosity-institution association, consistent with peak AKP consolidation, that reverts by 2018."

## What the paper does NOT claim

- **H3 as literally stated** (divergence sharpens 2007-2018): not confirmed. Cross-institution Wald on `nr × WV7` army vs police returns p = 0.24. The divergence was already established at the WV5 baseline.
- **The cluster flip as evidence of stable sociological types**: labels are method-sensitive. State the finding about middle-trust respondents as a group, not a reified typology.
- **Direct conf_military mean comparisons across waves** without the partial-scalar caveat.

## Analytical decisions for the writing phase

- **WV7 in main models**: include with `wv7_flag` covariate; report with caveat. Relegate to appendix if word limit forces it.
- **Survey weights**: not available in the dataset; flag as a limitation in the data section.
- **MGCFA scope**: WV5/6/7 only per Component 1; a full-six-wave robustness check belongs in the appendix.
- **Cluster terminology**: "middle-trust respondents" or "moderate institutional trusters", not "Selective trusters" — less reifying given the κ evidence.

## Files

- `pooled_extended_v2.csv` — definitive analysis dataset (11,704 × 54)
- `column_manifest_v2.csv` — data dictionary
- `findings_summary.md` — full per-layer narrative
- `pressure_tests.md` — five robustness verdicts (3 PASS, 1 WEAK, 1 FAIL-qualified)
- `cluster_robustness.csv`, `cluster_kappa_summary.csv` — 4-method clustering reproducibility
- `mgcfa_fit_indices.csv`, `mgcfa_delta_fit.csv`, `mgcfa_partial_scalar.csv`, `mgcfa_loadings.csv` — measurement invariance results
- `layer1_*.csv`, `layer2_*.csv`, `layer3_ordinal_coefficients.csv`, `layer4_pooled_interactions.csv`, `layer4b_*.csv` — per-layer results tables
