# Compositional check on the secular category — descriptive only

Run 2026-07-17. Source: `results/pooled_extended_v2.csv` (full file, no cluster filter); nr = `rel_person` 2/3 vs 1. No models. Weighted columns use the per-wave calibration weights via the validated positional merge (V376/V236/V245/V259/V258/W_WEIGHT; WV2/WV7 ≡ 1.0, so weighted = unweighted there). High confidence = categories 3–4 of the reverse-coded 1–4 item.

## 1. Secular share by wave (% nr = 1 among non-missing rel_person)

| wave | year | n (non-missing rel_person) | % secular (unweighted) | % secular (weighted) |
|---|---|---|---|---|
| WV2 | 1990 | 1,002 | 25.45 | 25.45 |
| WV3 | 1996 | 1,453 | 24.91 | 21.54 |
| WV4 | 2001 | 3,320 | 21.63 | 19.43 |
| WV5 | 2007 | 1,321 | 17.94 | 17.43 |
| WV6 | 2011 | 1,575 | 16.57 | 15.00 |
| WV7 | 2018 | 2,208 | 27.85 | 27.85 |

**Drift:** the secular share declines monotonically from 25.5% (1990) to 16.6% (2011), then jumps to 27.9% in 2018; weighting shifts the 1996–2011 values 1–3 pp lower but leaves the same U-shaped path.

## 2. Profile of seculars (nr = 1) by wave, with nr = 0 reference

Means over non-missing values within group × wave. `lowgod%` = share with rel_importance_god ≤ 7. **Education caveat:** `education_raw` is on the WVS 1–8 scale in WV2–WV6 but ISCED 0–6 in WV7 — WV7 education means are not comparable to earlier waves (education_recode 1–3 carries the same break).

| group | wave | n | mean left_right (n) | mean rel_attendance | % god ≤ 7 | mean education_raw | mean education_recode | mean age |
|---|---|---|---|---|---|---|---|---|
| nr=1 | WV2 | 255 | 4.34 (240) | 5.52 | 44.3 | 4.47 | 2.13 | 33.0 |
| nr=1 | WV3 | 362 | 4.68 (348) | 5.15 | 32.7 | 5.48 | 2.38 | 34.0 |
| nr=1 | WV4 | 718 | 4.35 (697) | 5.13 | 34.0 | 5.64 | 2.32 | 35.5 |
| nr=1 | WV5 | 237 | 4.44 (214) | 5.37 | 30.2 | 6.24 | 2.51 | 33.1 |
| nr=1 | WV6 | 261 | 4.73 (248) | 5.19 | 24.5 | 6.42 | 2.62 | 35.0 |
| nr=1 | WV7 | 615 | 5.57 (588) | 4.59 | 49.2 | 2.62* | 1.68* | 37.4 |
| nr=0 | WV2 | 747 | 5.81 (635) | 4.11 | 8.0 | 3.28 | 1.85 | 37.6 |
| nr=0 | WV3 | 1,091 | 6.25 (1,003) | 3.62 | 5.1 | 4.36 | 2.16 | 37.1 |
| nr=0 | WV4 | 2,602 | 6.19 (2,476) | 4.12 | 6.1 | 4.22 | 2.05 | 37.5 |
| nr=0 | WV5 | 1,084 | 6.56 (912) | 3.99 | 4.3 | 4.52 | 2.16 | 37.3 |
| nr=0 | WV6 | 1,314 | 6.53 (1,185) | 3.96 | 9.1 | 5.19 | 2.26 | 39.2 |
| nr=0 | WV7 | 1,593 | 6.68 (1,414) | 3.39 | 29.0 | 2.19* | 1.53* | 40.0 |

\* WV7 ISCED scale — not comparable to WV2–WV6.

**Drift:** secular observables are broadly stable from 1990 to 2011 (left-right 4.3–4.7, attendance 5.1–5.5), then move in 2018 — mean left-right rises to 5.57, attendance falls to 4.59, and % god ≤ 7 doubles to 49.2 — the same wave in which the secular share jumps from 16.6% to 27.9% (the religious reference group also shows a 2018 jump in % god ≤ 7, 9.1 → 29.0, consistent with the flagged WV7 religiosity-item discontinuity).

## 3. Police: % high confidence among seculars (nr = 1), by left_right band

Cells: % high (n). Cells with n < 30 are flagged †unstable.

| wave | LR 1–4 | LR 5–6 | LR 7–10 |
|---|---|---|---|
| WV2 1990 | 18.7 (107) | 53.9 (102) | 65.5 (29)† |
| WV3 1996 | 27.7 (159) | 64.3 (112) | 75.7 (74) |
| WV4 2001 | 32.0 (328) | 65.0 (246) | 76.7 (116) |
| WV5 2007 | 31.9 (116) | 52.8 (53) | 75.0 (44) |
| WV6 2011 | 42.5 (113) | 57.5 (73) | 68.3 (60) |
| WV7 2018 | 64.5 (200) | 72.5 (153) | 92.7 (232) |

**Drift:** secular police confidence rises within every left-right band by 2018 (left band 18.7 → 64.5; middle 53.9 → 72.5; right 65.5† → 92.7), and at the same time the secular category's right band grows from 29† to 232 respondents — both within-band increases and recomposition toward the right band are present in the raw cells.

## 4. Courts: % high confidence among seculars (nr = 1), by left_right band

| wave | LR 1–4 | LR 5–6 | LR 7–10 |
|---|---|---|---|
| WV2 1990 | 39.8 (108) | 52.0 (100) | 44.8 (29)† |
| WV3 1996 | 54.4 (160) | 58.9 (112) | 68.9 (74) |
| WV4 2001 | — (0) | — (0) | — (0) |
| WV5 2007 | 50.9 (116) | 56.6 (53) | 79.5 (44) |
| WV6 2011 | 35.7 (112) | 62.2 (74) | 66.7 (60) |
| WV7 2018 | 48.3 (201) | 61.8 (152) | 83.2 (232) |

Courts 2001: all cells empty — item not fielded in the WV4 Turkey file (confirmed, no imputation).

**Drift (contrast with police):** for the courts, left-band seculars show no comparable rise (39.8 in 1990 → 48.3 in 2018, dipping to 35.7 in 2011) while the right band rises (44.8† → 83.2) — so the within-band left–right spread widens for the courts, unlike police, where all three bands rise together.
