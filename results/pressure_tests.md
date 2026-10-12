# Pressure tests — robustness checks against the main findings

Pass = main finding holds in direction and rough magnitude under the robustness condition.
Fail = main finding reverses or becomes non-significant.
Weak = direction holds but evidence is partially undermined.

## Headline verdicts

| Check | Vulnerability tested | Verdict |
|---|---|---|
| 1 | WV4 dating claim is power-driven by large n | **PASS** |
| 2 | Secular police-trust gain is compositional | **WEAK** |
| 3 | Cluster labels drift across waves | **FAIL** (with major qualifier) |
| 4 | Courts stability is restricted-sample artifact | **PASS** |
| 5 | WV6 anomaly drives the overall pattern | **PASS** |

---

## Check 1 — Power artifact in the WV4 dating claim

**Vulnerability**: the `nr × WV4` interaction on army (+0.716***) comes from the largest wave (n=3,401). Could it be sample size doing the work?

### 1a — Bootstrap WV4 down to n=1,030 (100 iterations, with replacement)

| metric | value |
|---|---:|
| original full-sample coef | **+0.716\*\*\*** |
| bootstrap mean coef | +0.755 |
| 95% simulation interval | [+0.419, +1.115] |
| % iterations significant at p<.05 | **94%** |

The downsampled bootstrap recovers the same effect with the same direction and roughly the same magnitude. The 95% simulation interval is well above zero.

### 1b — Cohen's d approximation (log-odds / 1.814)

| | d |
|---|---:|
| full-sample d | +0.395 (medium) |
| bootstrap mean d | +0.416 |

A medium standardized effect size. Not borderline.

### 1c — nr × WV4 vs nr × WV5 on army

Both interactions are significant and similar magnitude (+0.716\*\*\* vs +0.635\*\*). Consistent picture, not a single-wave artifact.

**Verdict: PASS**. The WV4 dating finding survives sample-size matching to the smallest wave; 94% of bootstrap iterations remain significant.

---

## Check 2 — Compositional artifact in the secular police-trust gain

**Vulnerability**: the low-religiosity tertile grew from n=184 (WV2) to n=825 (WV7); the +0.90 police-trust gain could be from new entrants rather than attitudinal updating.

### 2a — Restrict to rel_importance_god ∈ [1,5] (stable distribution floor)

| wave | police mean | n |
|---|---:|---:|
| WV2 1990 | 1.920 | 113 |
| WV3 1996 | 1.889 | 126 |
| WV4 2001 | 2.082 | 306 |
| WV5 2007 | 2.167 | 48 |
| WV6 2011 | 2.531 | 49 |
| WV7 2018 | **2.909** | 331 |

WV2 → WV7 change on the restricted-floor sample: **+0.989** (vs +0.906 on the full low tertile). Trajectory is monotone and even slightly larger than the headline number.

### 2b — Police trust by education tertile (per-wave qcut)

| wave | low | mid | high |
|---|---:|---:|---:|
| WV2 | 2.998 | 2.577 | 2.354 |
| WV3 | 3.073 | 2.716 | 2.376 |
| WV4 | 3.148 | 2.828 | 2.545 |
| WV5 | 3.198 | 2.824 | 2.550 |
| WV6 | 3.125 | 2.978 | 2.760 |
| WV7 | 3.230 | 3.154 | 3.079 |

Police trust rises in every education tertile. The low−high gradient collapses from 0.64 (WV2) to 0.15 (WV7), so police trust is converging across education levels — but the rise is broad-based, not concentrated in any single educational stratum.

### 2c — Within `rel_person = not religious`, WV5 vs WV6 police trust

| wave | mean | n |
|---|---:|---:|
| WV5 | 2.419 | 234 |
| WV6 | 2.529 | 255 |

Mann–Whitney U = 28,002; **p = 0.223 (n.s.)**, direction = up.

The WV5→WV6 step within the not-religious group does *not* clear significance — the within-group gain in the stable measurement window is modest. Most of the not-religious police-trust rise is concentrated WV6→WV7, which overlaps the WV7 measurement caveat.

**Verdict: WEAK**. The WV2→WV7 trajectory survives compositional restriction (2a) and is broad-based across education tertiles (2b). But the WV5→WV6 within-group step is not individually significant (2c), so the "secular updating in the stable measurement window" interpretation should be softened.

---

## Check 3 — Cluster label stability across waves

**Vulnerability**: "Selective trusters" (cluster 1) is assigned via Hungarian matching across waves; the WV5→WV6 army-police flip could be a labeling artifact.

### 3a — Cluster 1 profile across waves

| wave | n | % religious | mean edu | mean age | % female | mean L-R |
|---|---:|---:|---:|---:|---:|---:|
| WV2 1990 | 436 | 76.4 | 3.44 | 37.1 | 48.2 | 5.70 |
| WV3 1996 | 514 | **58.0** | 4.53 | 35.1 | 37.0 | 6.55 |
| WV4 2001 | 1,472 | 78.9 | 4.61 | 37.0 | 48.9 | 6.06 |
| WV5 2007 | 506 | 86.8 | 4.81 | 37.5 | 50.8 | 6.76 |
| WV6 2011 | 650 | 83.2 | 5.28 | 38.9 | 50.9 | 6.52 |
| WV7 2018 | 898 | **63.3** | 2.26 | 38.7 | 48.6 | 6.76 |

Ranges across waves: pct_religious **28.8 pp**, mean_edu 3.02 (scale-change confounded by WV7 ISCED), mean_age 3.75 yr, pct_female 14 pp, mean L-R 1.06.

The religious-composition swing is substantial — WV3 (58%) and WV7 (63%) bracket a more religious core (78–87%). WV7's drop overlaps the religiosity measurement break; WV3's drop is harder to explain.

### 3b — Within cluster 1, OLS conf_military ~ wave dummies (WV2 ref)

| wave dummy | coef | p |
|---|---:|---:|
| WV3 | −0.191 | < .001 |
| WV4 | +0.042 | 0.245 |
| WV5 | +0.143 | < .001 |
| **WV6** | **−0.370** | **< .001** |
| WV7 | −0.167 | < .001 |

The WV6 negative shock on army confidence within cluster 1 is large and highly significant. **The flip is not a labeling artifact** — it shows up as a real attitudinal change within the cluster-1 cell defined by the same Hungarian matching procedure.

### 3c — K-means on WV5 conf_* items only vs Hungarian-matched labels

| metric | value |
|---|---:|
| n WV5 | 1,289 |
| agreement (best-matched) | **59.5%** |
| Cohen's κ | **0.384** |

A 6-item conf-only k-means agrees with the 14-item Hungarian-matched cluster only 60% of the time (κ = 0.38, moderate). The cluster definition is sensitive to which trust items are used as input.

**Verdict: FAIL — with a major qualifier**.

The substantive interpretation is more nuanced than the bare verdict:

- 3b is unambiguous evidence that the WV6 army flip is real within respondents grouped under the cluster-1 label (−0.37, p<.001).
- 3a shows the cluster's religious composition drifts substantially (29 pp range); WV3 and WV7 look compositionally distinct from WV4–WV6.
- 3c says limited-feature clustering recovers the Hungarian-matched labels only moderately well. That's partly mechanical — fewer features means more borderline assignments — but it does mean the cluster boundaries are not razor-sharp.

The honest reading: the *finding that cluster 1 shows the army flip* is robust (3b confirms it on the same labels), but the *interpretation of cluster 1 as a stable sociological type* is shakier than I implied. Layer 5 should explicitly check cluster-specific claims against alternative clustering choices.

---

## Check 4 — Courts stability on the no-WV4 restricted sample

**Vulnerability**: courts coefficients use a different sample (no WV4) than army and police. Could the courts stability finding disappear when army and police are run on the same sample?

### 4a — Refit Layer 4b on WV2/3/5/6/7 only

| interaction | army (n=6,246) | police (n=6,242) | courts (n=6,231) |
|---|---:|---:|---:|
| nr × WV3 | +0.402* | +0.299 | +0.267 |
| nr × WV5 | **+0.685\*\*** | +0.266 | +0.088 |
| nr × WV6 | +0.396. | +0.186 | +0.055 |
| nr × WV7 | +0.664\*\*\* | +0.654\*\*\* | +0.076 |

### 4b — Side-by-side, identical respondents

- Army interactions remain large and significant (+0.40 to +0.69)
- Courts interactions remain small and non-significant (+0.05 to +0.27, all n.s.)
- Police picks up the WV7 interaction (+0.654\*\*\*) but stays muted WV3–WV6

The courts-as-stable-locus finding **survives the same-sample comparison cleanly**. Courts interactions are if anything *more* uniformly close to zero on the 5-wave restricted sample.

**Verdict: PASS**. All three models converge on the restricted sample; courts interactions remain ~0; army interactions remain large and significant; the cross-institutional asymmetry holds.

---

## Check 5 — WV6 anomaly outlier and leave-one-wave-out

**Vulnerability**: I described WV6 as anomalous. Is it really a statistical outlier from trend, and does excluding WV6 change the other findings?

### 5a/5b — Trend on WV2/3/4/5/7 (excluding WV6) predicts WV6

| outcome | trend slope | predicted WV6 | actual WV6 | deviation |
|---|---:|---:|---:|---:|
| army `nr_dummy` total | +0.021/yr (R²=0.58) | −0.080 | −0.334 | −1.32 SD |
| police `nr_dummy` total | +0.016/yr (R²=0.68) | −0.241 | −0.537 | **−2.44 SD** |

Both outcomes show negative WV6 residuals. The police effect is a clear outlier (>2 SD); the army deviation is meaningful but below the 2-SD bar I set as the formal criterion.

### 5c — Leave-one-wave-out refit of Layer 4b army model

| dropped wave | nr × WV3 | nr × WV4 | nr × WV5 | nr × WV6 | nr × WV7 |
|---|---:|---:|---:|---:|---:|
| WV2 | (model fails: WV2 was reference) |
| WV3 | dropped | +0.713 | +0.616 | +0.407 | +0.645 |
| WV4 | +0.402 | dropped | +0.685 | +0.396 | +0.664 |
| WV5 | +0.379 | +0.734 | dropped | +0.410 | +0.664 |
| **WV6** | **+0.386** | **+0.748** | **+0.652** | dropped | **+0.642** |
| WV7 | +0.349 | +0.654 | +0.598 | +0.390 | dropped |

Full sample reference: nr × WV4 = +0.716\*\*\*.

Dropping WV6 changes nr × WV4 from +0.716 to **+0.748** — almost no change. The WV4 dating finding is not driven by the WV6 anomaly. The other wave interactions also vary only modestly across the LOO refits.

**Verdict: PASS**. WV6 is a real outlier on police; excluding WV6 leaves the other wave interactions essentially unchanged. The WV6 anomaly is genuine but isolated.

(Note: dropping WV2 makes the model fail because WV2 is the omitted reference category. Mechanical, not substantive.)

---

## Summary and implications

| Check | Verdict | Implication |
|---|---|---|
| 1 (WV4 power) | PASS | The 2001 dating claim survives sample-size matching. Bootstrap mean (+0.76) ≈ full-sample (+0.72); 94% of iterations significant. |
| 2 (secular comp.) | WEAK | The overall WV2→WV7 secular police-trust gain is real and broad-based, but the within-group WV5→WV6 step is not individually significant — the gain leans more on WV6→WV7. |
| 3 (cluster stab.) | FAIL (qualified) | The WV6 army flip within cluster 1 is robust (3b, p<.001), but the cluster *definition* is moderately fuzzy (κ=0.38 vs full-feature clustering). Cluster-specific claims need sensitivity checks in Layer 5. |
| 4 (courts restricted) | PASS | The courts-as-stable-locus finding reproduces on the same-sample restricted model. Army interactions stay significant, courts stay ~0. |
| 5 (WV6 anomaly) | PASS | WV6 is an outlier on police (-2.4 SD from trend), but isolated — leave-one-out shows other wave interactions are stable when WV6 is excluded. |

### What this means for the findings summary

- The **WV4-as-divergence-onset** finding (Check 1) and the **courts-as-stable-locus** finding (Check 4) survive cleanly and can be stated firmly.
- The **secular convergence on police** finding (Check 2) is qualitatively correct — police trust rises across all education tertiles and on the restricted floor sample — but the precise WV5→WV6 within-group attribution should be softened. Most of the secular police-trust gain comes WV6→WV7, which overlaps the WV7 measurement caveat.
- The **Selective trusters cluster** finding (Check 3) is real as defined by the existing Hungarian-matched labels (3b confirms the army flip). But the cluster *definition itself* is moderately fragile to feature-set choices — a separate question that Layer 5 should address.
- The **WV6 anomaly** is a real outlier (Check 5) and treating it as "AKP consolidation wave with anomalous religiosity coefficients" is defensible. It does not contaminate the other findings.

### Net assessment

3 PASS, 1 WEAK (with reasonable qualification), 1 FAIL (largely a cluster-definition fragility rather than a flip-finding failure). The headline story — institutional differentiation along religious lines dated to 2001, courts as the persistent locus of secular distrust, aggregate army-police convergence driven by secular updating on police — survives in direction and magnitude.

Two qualifications to add to the main `findings_summary.md`:

1. The secular police-trust gain leans more on the WV6→WV7 transition than on the WV5→WV6 transition within the stable measurement window.
2. Cluster labels are moderately fragile to feature-set choices — direct cluster-specific quantitative claims should carry an "as defined by the 14-item Hungarian-matched clustering" disclaimer, and Layer 5 should verify with alternative clustering.
