# Verification pass — WVS Turkey (frozen analysis)

Run 2026-07-16. Refit + extract + print only; no new analyses, no spec changes. Every
number below is produced by refitting the frozen layer4b specification or by extracting
stored values (each such extraction is labelled with its file). Precision: 3 decimals for
estimates/CIs (4 where the gate demands it), full precision for p-values.

## 1. Replication gate

Refit army layer4b spec (full layer4b sample): `nr x WV4` = **+0.7162** (SE **0.1828**), p = **8.953e-05**, n = **8,915**.
Published (`layer4b_longwindow_interactions.csv`): +0.7162 (0.1828), p = 8.953e-05, n = 8,915.
Programmatic assertion to 4 decimals: **PASSED** (|dcoef| = 0.0e+00, |dSE| = 5.6e-17).

## 2. Six-institution x six-wave LEVEL table

Basis: the cell-15 **common sample** (non-missing on military + parliament + government
+ all layer4b predictors; n = 8,777); each institution fit on its own
outcome-non-missing subset of it — the basis of the paper's main result table and of every
number verified in section 3. LEVEL = baseline + interaction, delta-method SE, normal 95% CI.
Courts WV4: **0 non-null values** among the 3,401 WV4 rows of
`pooled_extended_v2.csv` -> marked N/A (item not fielded in 2001).
All WV7 cells carry the WV7 measurement caveat (religiosity-item discontinuity;
`partner_handoff_v2.md`).

| institution (n) | WV2 | WV3 | WV4 | WV5 | WV6 | WV7 (caveat) |
|---|---|---|---|---|---|---|
| military (8,777) | -0.763 (0.162) [-1.080, -0.446] | -0.336 (0.131) [-0.594, -0.079] | -0.025 (0.102) [-0.224, +0.174] | -0.089 (0.164) [-0.410, +0.233] | -0.332 (0.139) [-0.604, -0.060] | -0.081 (0.097) [-0.270, +0.109] |
| police (8,748) | -0.760 (0.156) [-1.067, -0.454] | -0.405 (0.122) [-0.643, -0.167] | -0.240 (0.095) [-0.428, -0.053] | -0.449 (0.145) [-0.732, -0.165] | -0.535 (0.136) [-0.802, -0.269] | -0.138 (0.095) [-0.324, +0.049] |
| courts (6,110) | -0.527 (0.159) [-0.839, -0.215] | -0.222 (0.124) [-0.465, +0.021] | N/A (not fielded) | -0.438 (0.150) [-0.732, -0.145] | -0.450 (0.138) [-0.721, -0.179] | -0.437 (0.093) [-0.619, -0.255] |
| parliament (8,777) | -0.926 (0.159) [-1.238, -0.614] | -0.257 (0.122) [-0.497, -0.017] | -0.053 (0.095) [-0.238, +0.133] | -0.486 (0.143) [-0.766, -0.206] | -0.401 (0.131) [-0.659, -0.144] | -0.076 (0.089) [-0.251, +0.098] |
| government (8,777) | -0.429 (0.157) [-0.737, -0.121] | -0.350 (0.123) [-0.592, -0.108] | -0.053 (0.097) [-0.242, +0.136] | -0.596 (0.144) [-0.879, -0.313] | -0.473 (0.132) [-0.732, -0.215] | -0.555 (0.090) [-0.732, -0.378] |
| civil_service (8,711) | -0.783 (0.156) [-1.089, -0.477] | -0.218 (0.123) [-0.458, +0.023] | -0.121 (0.095) [-0.308, +0.066] | -0.294 (0.146) [-0.580, -0.008] | -0.541 (0.135) [-0.805, -0.277] | -0.433 (0.094) [-0.616, -0.249] |

Reconciliation — **full layer4b sample** basis (each institution's own listwise sample on
the full pooled file; the basis of `layer4b_total_effects_by_wave.csv` and the deck's main
figure). Values differ slightly from the common-sample table above (e.g. army WV5 −0.101
here vs −0.089 above); neither is wrong — different frozen bases:

| institution (n) | WV2 | WV3 | WV4 | WV5 | WV6 | WV7 (caveat) |
|---|---|---|---|---|---|---|
| military (8,915) | -0.736 (0.157) [-1.044, -0.429] | -0.362 (0.130) [-0.617, -0.107] | -0.020 (0.101) [-0.219, +0.179] | -0.101 (0.163) [-0.421, +0.219] | -0.334 (0.138) [-0.605, -0.063] | -0.085 (0.096) [-0.273, +0.103] |
| police (8,911) | -0.692 (0.152) [-0.990, -0.394] | -0.409 (0.120) [-0.645, -0.173] | -0.243 (0.095) [-0.429, -0.058] | -0.431 (0.143) [-0.712, -0.150] | -0.537 (0.135) [-0.801, -0.272] | -0.130 (0.095) [-0.315, +0.055] |
| courts (6,231) | -0.503 (0.155) [-0.807, -0.199] | -0.236 (0.123) [-0.476, +0.004] | N/A (not fielded) | -0.415 (0.149) [-0.707, -0.124] | -0.448 (0.137) [-0.718, -0.179] | -0.427 (0.092) [-0.608, -0.246] |
| parliament (8,873) | -0.891 (0.155) [-1.196, -0.586] | -0.260 (0.122) [-0.499, -0.020] | -0.050 (0.094) [-0.234, +0.135] | -0.481 (0.143) [-0.761, -0.201] | -0.399 (0.131) [-0.655, -0.142] | -0.081 (0.089) [-0.255, +0.093] |
| government (8,861) | -0.425 (0.157) [-0.732, -0.119] | -0.361 (0.123) [-0.602, -0.121] | -0.052 (0.096) [-0.240, +0.136] | -0.586 (0.144) [-0.868, -0.303] | -0.441 (0.131) [-0.699, -0.184] | -0.552 (0.090) [-0.728, -0.375] |
| civil_service (8,863) | -0.761 (0.151) [-1.058, -0.464] | -0.221 (0.121) [-0.459, +0.017] | -0.116 (0.095) [-0.301, +0.070] | -0.300 (0.145) [-0.584, -0.016] | -0.541 (0.134) [-0.804, -0.278] | -0.427 (0.093) [-0.609, -0.244] |

Cross-check of the army/police/courts full-sample LEVELs against `layer4b_total_effects_by_wave.csv` (all fielded cells, 4-dp): **MATCH**.

## 3. Specific numbers: confirmed / corrected

The quoted CIs originated as **bootstrap percentile intervals** (closing_checks bootstrap,
B = 1,000). A refit reproduces the point estimates and delta-method intervals; the quoted
intervals are verified below against the stored draws (`results/bootstrap_draws.parquet` —
extraction, not a summary), with the refit delta-method interval printed alongside.

- **Army WV5 LEVEL ~ -0.08**: refit = **-0.089** -> **CONFIRMED**.
  Refit delta CIs: 95% [-0.410, +0.233], 90% [-0.358, +0.181].
  Stored bootstrap percentile CIs: 95% [-0.451, +0.285], 90% [-0.390, +0.216].
- **Army WV6 LEVEL = -0.332, 90% CI [-0.552, -0.095]**: refit point = **-0.332** -> **CONFIRMED**. The quoted 90% CI is the bootstrap percentile interval: stored draws give [-0.552, -0.095] -> **CONFIRMED (bootstrap CI)**; refit delta 90% CI = [-0.560, -0.104] (same verdicts either way, see section 4).
- **Army WV7 LEVEL ~ 0**: refit = **-0.081** (delta 95% [-0.270, +0.109]; p = 0.403) -> **CONFIRMED** (small and not distinguishable from zero).
- **Parliament WV7 95% CI [-0.202, +0.053]**: this is the bootstrap percentile CI — stored draws give [-0.202, +0.053] -> **CONFIRMED (bootstrap CI)**. Refit: point -0.076, delta 95% CI [-0.251, +0.098] — wider than the bootstrap interval (delta SE 0.089 vs bootstrap SE 0.067); both intervals exclude parliament's WV5 gradient (-0.486).
- **Parliament WV7-WV5 decline p = .004**: stored-draws paired percentile p = **0.0040** -> **CONFIRMED** (change = +0.410). Refit delta-method equivalent (nr_x_WV7 - nr_x_WV5 in the parliament model): +0.410 (SE 0.167), p = 0.0139 — same conclusion.

## 4. TOST verdicts, army, 90% CIs explicit

TOST at alpha = .05 uses the **90% CI**; the 95% CI is for reporting only. Margins:
delta = +/-0.42 (pre-specified courts margin) and delta = +/-0.7631 (= |army WV2 LEVEL|,
refit). Two interval constructions shown; **each verdict column states the interval it
uses**. Verdict rule: EQUIVALENT iff the 90% CI lies entirely inside (-delta, +delta).

| wave | refit delta 90% CI | bootstrap 90% CI (stored draws) | verdict @0.42 (delta 90%) | verdict @0.42 (boot 90%) | verdict @0.7631 (delta 90%) | verdict @0.7631 (boot 90%) |
|---|---|---|---|---|---|---|
| WV4 | [-0.192, +0.142] | [-0.189, +0.147] | EQ | EQ | EQ | EQ |
| WV5 | [-0.358, +0.181] | [-0.390, +0.216] | EQ | EQ | EQ | EQ |
| WV6 | [-0.560, -0.104] | [-0.552, -0.095] | NON-EQ | NON-EQ | EQ | EQ |
| WV7 | [-0.240, +0.078] | [-0.231, +0.074] | EQ | EQ | EQ | EQ |

**Resolution of the suspected inconsistency:** the final tables in draws_readoff/closing
print the **95% CI** in the cell (reporting convention) while every equivalence decision was
made on the **90% CI** (TOST convention, stated in the closing_checks margins cell). No
decision used a 95% interval. Redone here with 90% intervals explicit, the verdicts are
**identical under both the refit-delta and bootstrap constructions (all four columns agree)**:
army EQUIVALENT at +/-0.42 in WV4, WV5, WV7; NON-EQUIVALENT at WV6; EQUIVALENT at
+/-0.7631 in all of WV4-WV7.

## 5. Phantom WV4 courts row

Raw CSV lines from `layer4b_total_effects_by_wave.csv`:

```
wave,year,army_total,army_p,police_total,police_p,courts_total,courts_p,army_police_spread
WV2,1990,-0.7363,0.0,-0.6918,1e-05,-0.503,0.00116,-0.0445
WV4,2001,-0.0201,0.84284,-0.2433,0.01012,-0.503,0.00116,0.2232
```

`courts_total` field: WV2 = `-0.503`, WV4 = `-0.503` -> byte-identical: **True**.
`courts_p` field: WV2 = `0.00116`, WV4 = `0.00116` -> byte-identical: **True**.
With 0 non-null WV4 courts values in the source and no `nr_x_WV4`/`wave_WV4`
terms in the refit courts model (dropped as zero-variance), the WV4 row is confirmed as the
**WV2 baseline carried forward, not an estimate** -> **CONFIRMED**.

