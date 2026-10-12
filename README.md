# Institutional trust in Turkey: army, police and courts, WVS 1990-2018

**Authors:** İlayda Küçükafacan (Koç University) and Kağan Korkmaz (Charles University)

**Status:** Abstract submitted to the SDL Conference 2026 (Boğaziçi University). The paper is in preparation. The numbers below are working results, not final published results.

**License:** MIT for the code (see `LICENSE`). WVS data are not included and remain under the WVS terms of use.

## The question

In Turkey, did the public always see the army, the police and the courts as one "coercive" bloc, or did people start to trust them for different reasons as politics changed? In particular, we ask whether the link between being religious and trusting each institution changed, when it changed, and whether it changed in the same way for all three. We use six waves of the World Values Survey (WVS) for Turkey: 1990, 1996, 2001, 2007, 2011 and 2018 (WVS waves 2 to 7; 11,704 respondents in total).

## What the results show so far

All numbers come from the files in `results/`. Where a later check corrected an earlier statement, the corrected version is used. Wave 7 (2018) has a break in how religiosity was measured (for example, the share who say God is "very important" falls from 67% to 45% in one wave), so 2018 figures are only directionally comparable.

- **1990-1996.** Army, police and courts move together. People who say they are "not religious" trust all three less than religious people do (1990 coefficients: army -0.74, police -0.69, courts -0.50; all significant). The mean trust gap between army and police is about 0.70-0.75 on a 1-4 scale.
- **2001.** The gap between non-religious and religious people in army trust is gone (-0.36 in 1996, -0.02 in 2001). The police gap becomes smaller but stays significant (-0.24). The formal test against the 1990 baseline is significant for the army (+0.72, p < .001) and also for the police (+0.45, p = .011). The courts question was **not asked in the 2001 Turkey survey**, so nothing can be said about courts in 2001. The change is dated to "by the 2001 wave": the data cannot show what happened between 1996 and 2001.
- **The 2001 change is not army-specific.** The same drop appears for parliament (+0.84) and the civil service (+0.65), and partly for government (+0.37). What looks specific to the army is that the gap did not come back: it is statistically indistinguishable from zero in 2001, 2007 and 2018. It is not zero in 2011 (-0.33). Parliament, government and the civil service show a religiosity gap again from 2007 (government and civil service still in 2018; parliament not). A formal test that the army differs from parliament over 2007-2018 as a whole was **not supported**; the army differs clearly from government and the civil service.
- **2007.** The army gap is near zero (-0.10) while the police (-0.43) and courts (-0.42) gaps stay negative. The army-police difference in the religiosity gap is largest here.
- **2011.** The biggest single change in average army trust (from 3.46 to 3.09; p about 5e-31). The army-police average gap falls to 0.09. For respondents in the middle trust group, the police overtakes the army as the most trusted institution. 2011 is also an outlier on religiosity gaps (police gap 2.4 standard deviations off the trend), which is isolated and does not drive the 2001 result.
- **2018.** The army and police religiosity gaps are small (-0.09 and -0.13, not significant). Among army, police and courts, the courts gap (-0.43) is the only one still clearly negative in 2018; it is also -0.42 and -0.45 in 2007 and 2011. Courts were not asked in 2001, so the courts series has five waves, not six.
- **Measurement.** A multi-group factor analysis (2007, 2011, 2018; n = 5,066) finds the confidence items measure the same construct in each wave (metric invariance holds). Full scalar invariance fails narrowly; it holds when the army item's thresholds are freed. So comparing average army trust across waves needs a caveat.
- **Trust groups.** Respondents fall into three recurring groups (low, middle and high trust across institutions). Only the middle group shows the army-to-police switch in 2011, and the switch also appears under three other clustering methods. The group labels themselves depend on the method (agreement with the original groups 50-69%), so we describe the finding as "middle-trust respondents", not as stable social types.

Known limits stated in the project files: the 2018 religiosity break; unweighted main models (later notebooks compare weighted versions and find similar results, see `notebooks/party_axis.ipynb` and `notebooks/persistence_test.ipynb`); and the 2001 timing depends on the religiosity measure (a God-importance version gives +0.51, about 70% of the size, and a less sharp date). Two statements in the handoff were corrected by `docs/verification_pass.md` and the audit in `results/project_audit.md`: courts were not measured in 2001 (the 2001 courts row in `results/layer4b_total_effects_by_wave.csv` is the 1990 value carried forward and is not an estimate), and the 2011 army-police gap is 0.09, not 0.10.

## Data

The survey data are **not included** in this repository. They belong to the World Values Survey Association and must be downloaded by each user after free registration at https://www.worldvaluessurvey.org. Please follow their terms of use.

You need the six Turkey country files in Excel format, one per wave, with these exact file names:

| Wave | Year | File name expected by the scripts |
|---|---|---|
| WV2 | 1990 | `F00008272-WV2_Data_Turkey_Excel_v1.6.1.xlsx` |
| WV3 | 1996 | `F00008135-WV3_Data_Turkey_Excel_v20221107.1.xlsx` |
| WV4 | 2001 | `F00008022-WV4_Data_Turkey_Excel_v20201117.1.xlsx` |
| WV5 | 2007 | `F00007873-WV5_Data_Turkey_Excel_v20201117.1.xlsx` |
| WV6 | 2011 | `F00007629-WV6_Data_Turkey_2011_Excel_v20180912.xlsx` |
| WV7 | 2018 | `F00013222-WVS_Wave_7_Turkey_Excel_v5.1.xlsx` |

Place them in the **repository root** (the same folder as this README). If WVS publishes newer versions, the file names, and possibly the variable codes in the crosswalk, will differ. The `.gitignore` keeps these files out of git.

This repository also leaves out every file that holds one row per respondent: `results/pooled_*.csv` (the pooled analysis dataset) and `results/mgcfa_input.csv`. The scripts rebuild them locally. The aggregated results (coefficients, tables, figures) are included.

## Methods

- **Crosswalk.** Variable codes differ across waves. A table maps each concept (for example "confidence in the armed forces") to the variable in each wave (`results/variable_search/WVS_TR_concept_crosswalk_v3.csv`). Confidence items are reversed so higher means more trust (1-4 scale).
- **Trust orientations.** K-means clustering with three groups, run separately in each wave on the confidence items, then matched across waves to the 2001 solution (Hungarian algorithm). Checked against k-means with four groups, Ward clustering and a Gaussian mixture (`code/cluster_robustness.py`).
- **Ordinal regressions.** Ordered logit of confidence in each institution on a "not religious" indicator plus controls (religious attendance, importance of God, left-right position, age, gender, education, income, marital status), per wave and per trust group.
- **Pooled interactions.** One ordered logit over all waves with 1990 as the baseline and wave-by-religiosity interactions. This is the model that dates the change (`code/layer4b_longwindow.py`).
- **Measurement invariance.** Multi-group confirmatory factor analysis in R (lavaan, WLSMV estimator, ordinal items) for 2007, 2011 and 2018 (`code/mgcfa_runner.py` and `code/mgcfa_analysis.R`).
- **Robustness and later checks.** Pressure tests, placebo institutions, equivalence tests, bootstrap read-offs, education and party-axis checks are in `notebooks/`.

## How to run

Requirements: Python 3 (3.12 used) with `pip install -r requirements.txt`; R with the packages in `requirements-R.txt` (only for the factor analysis). Run everything **from the repository root**, with the WVS files placed there.

Scripts in `code/` (order of the original work):

1. Variable search: `crosswalk_expand.py`, `attribute_search.py`, `availability_check.py`, `resolve_candidates.py`. These write small lookup tables to the repository root. Copies of the versions used are in `results/variable_search/`.
2. Early clustering: `column_inventory.py`, `trust_clusters.py`.
3. Build the dataset: `pool_extended.py`, then `pool_final.py` (writes `results/pooled_extended_v2.csv`, the dataset used by everything after).
4. Layers: `layer1_trust_trajectories.py`, `layer1_by_religiosity.py`, `layer1_by_relperson.py`, `religiosity_composition.py`, `layer2_cluster_institutions.py`, `layer3_ordinal_regressions.py`, `layer4_pooled_interactions.py`, `layer4b_longwindow.py`.
5. Robustness: `cluster_robustness.py`, `mgcfa_runner.py` (calls `Rscript`), `pressure_tests.py`.
6. Notebooks in `notebooks/`, in this order of the original work: `moderator_scan`, `education_defense`, `final_checks` (7 July 2026); `preflight_refits`, `closing_checks`, `draws_readoff`, `draws_readoff2`, `party_axis`, `persistence_test` (16 July 2026).

**Important gap.** `column_inventory.py` and `trust_clusters.py` read `results/pooled_all_scales.csv`, a first pooled file made by an early script that is not in this repository. Because of this, the chain from raw data to `pooled_extended_v2.csv` cannot be re-run from scratch with the files here. The scripts from `layer1` onward only need `results/pooled_extended_v2.csv`. The authors should add the early script or document how that file was produced. The repository has not been re-run end to end after the path changes.

## Folder map

- `code/` analysis scripts (Python, one R script)
- `notebooks/` later checks and appendix analyses, with aggregated outputs only
- `results/` coefficient tables, figures and written summaries (`findings_summary.md`, `pressure_tests.md`, `project_audit.md`, `deck_numbers.md`, `deck_data_final.md`, `preflight_diagnostics.md`)
- `docs/` the partner handoff (`partner_handoff_v2.md`) and the verification pass (`verification_pass.md`)

## Planned and open work

Taken from the project files; these are not commitments.

- `results/findings_summary.md` proposes a "Layer 5": random-forest and SHAP models to describe the trust groups and test whether the religiosity pattern is captured by religiosity alone.
- `docs/partner_handoff_v2.md` says a full six-wave version of the factor analysis belongs in the appendix.
- Open writing decisions in the handoff: keep 2018 in the main models with a flag or move it to the appendix if space is short; the survey-weight limitation is to be stated in the data section.

## Citation

No citation is available yet. A preferred citation will be added when the paper is available.
