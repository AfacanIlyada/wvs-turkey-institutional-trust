# Secular segment on the army — party decomposition (descriptive only)

Run 2026-07-17. Source: `results/pooled_extended_v2.csv`, WV5–WV7, full file, no models.
nr = `rel_person` 2/3 vs 1. Party grouping uses the corrected `party_raw` codes established in
`party_axis.ipynb` (AKP 792008, CHP 792002, MHP 792006, pro-Kurdish per wave: DTP 792049 / BDP
792054 / HDP 792005; "other" = any other stated party; "none-stated" = non-response codes +
missing) — note `party_recode` itself buries DTP/BDP in "other" and carries İYİ as its own label.
High confidence = categories 3–4 of the reverse-coded item. † flags cell n < 30.

## 1. Party composition of seculars (nr = 1) by wave — % (n)

| wave | n | CHP | AKP | MHP | pro-Kurdish | other | none-stated |
|---|---|---|---|---|---|---|---|
| WV5 2007 | 237 | 28.7 (68) | 9.3 (22) | 6.3 (15) | 11.4 (27) | 6.3 (15) | 38.0 (90) |
| WV6 2011 | 261 | 43.3 (113) | 23.4 (61) | 5.4 (14) | 5.4 (14) | 0.0 (0) | 22.6 (59) |
| WV7 2018 | 615 | 39.5 (243) | 24.6 (151) | 14.8 (91) | 11.2 (69) | 5.7 (35) | 4.2 (26) |

**WV7 "other" composition (wave-level, `party_raw`):** 792050 (İYİ) n = 113 and 792051 n = 8 —
**İYİ does appear in "other" under this grouping**; in `party_recode` itself İYİ is a separate
category and the WV7 "other" label holds only n = 8. WV6 "other" is empty: the WV6 file carries
no stated-party code outside AKP/CHP/MHP/BDP.

**Direction:** among seculars the none-stated share falls from 38.0% (2007) to 4.2% (2018) while
every stated-party share grows — CHP remains the largest stated bloc (28.7 → 43.3 → 39.5%) and
the secular-AKP share rises from 9.3% to 24.6%.

## 2. % high army confidence among seculars (nr = 1), by party group — % (n)

| wave | CHP | AKP | MHP | pro-Kurdish | other | none-stated |
|---|---|---|---|---|---|---|
| WV5 2007 | 88.2 (68) | 90.9 (22)† | 100.0 (15)† | 18.5 (27)† | 100.0 (15)† | 75.6 (90) |
| WV6 2011 | 68.1 (113) | 65.6 (61) | 71.4 (14)† | 14.3 (14)† | — (0) | 62.5 (56) |
| WV7 2018 | 81.4 (242) | 90.0 (150) | 90.1 (91) | 50.7 (67) | 82.9 (35) | 76.0 (25)† |

**Direction:** within the secular segment, army high-confidence is high (65–100%) in every party
group except pro-Kurdish identifiers (18.5† / 14.3† / 50.7); all groups dip at 2011 and recover
by 2018, with the secular-CHP segment running 88.2 → 68.1 → 81.4.

## 3. Mirror: % high army confidence among religious respondents (nr = 0) — % (n)

| wave | CHP | AKP | MHP | pro-Kurdish | other | none-stated |
|---|---|---|---|---|---|---|
| WV5 2007 | 96.4 (84) | 88.6 (420) | 95.8 (71) | 18.4 (38) | 89.4 (66) | 91.2 (387) |
| WV6 2011 | 83.0 (271) | 77.3 (568) | 84.3 (108) | 27.7 (47) | — (0) | 77.3 (291) |
| WV7 2018 | 83.0 (229) | 89.7 (891) | 89.7 (155) | 77.0 (113) | 86.5 (74) | 91.7 (121) |

**Direction:** the religious mirror shows the same shape at higher levels (77–96% outside the
pro-Kurdish group, same 2011 dip and 2018 recovery); the pro-Kurdish group is again the low
outlier and rises to 77.0% by 2018, so by 2018 party groups differ little within either
religiosity segment except on the pro-Kurdish side.
