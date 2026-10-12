"""
Multi-group CFA of the WVS Turkey confidence battery (WV5/6/7).

Python prepares the input CSV, writes the R script, calls Rscript via
subprocess, then parses the result CSVs and prints verdicts.
"""
import os
import subprocess
import textwrap
import pandas as pd

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")

# =========================================================================
# 1) Prepare input data (Python side)
# =========================================================================
df = pd.read_csv(os.path.join(RESULTS, "pooled_extended_v2.csv"))
df = df[df["wave"].isin(["WV5","WV6","WV7"])].copy()
items = ["conf_military","conf_police","conf_courts",
         "conf_parliament","conf_government"]
df = df[items + ["wave"]].dropna()
df.to_csv(os.path.join(RESULTS, "mgcfa_input.csv"), index=False)
print(f"Input prepared: {df.shape}  -> results/mgcfa_input.csv")
print("n per wave after filtering:")
print(df["wave"].value_counts().sort_index().to_string())


# =========================================================================
# 2) Write the R script
# =========================================================================
R_SCRIPT = textwrap.dedent(r"""
    library(lavaan)
    library(semTools)

    dat <- read.csv("results/mgcfa_input.csv")
    dat$wave <- as.factor(dat$wave)

    items <- c("conf_military","conf_police","conf_courts",
               "conf_parliament","conf_government")
    for (v in items) dat[[v]] <- ordered(dat[[v]])

    model <- '
      inst_conf =~ conf_military + conf_police + conf_courts +
                   conf_parliament + conf_government
    '

    fit_configural <- cfa(model, data=dat, group="wave",
                          estimator="WLSMV",
                          ordered=items)

    fit_metric <- cfa(model, data=dat, group="wave",
                      estimator="WLSMV",
                      group.equal=c("loadings"),
                      ordered=items)

    fit_scalar <- cfa(model, data=dat, group="wave",
                      estimator="WLSMV",
                      group.equal=c("loadings","intercepts","thresholds"),
                      ordered=items)

    get_fit <- function(fit, label) {
      fi <- fitMeasures(fit, c("cfi","cfi.scaled",
                               "rmsea","rmsea.scaled",
                               "srmr","chisq","chisq.scaled",
                               "df","df.scaled","pvalue","pvalue.scaled"))
      data.frame(model=label,
                 CFI       = unname(fi["cfi"]),
                 CFI_scaled= unname(fi["cfi.scaled"]),
                 RMSEA     = unname(fi["rmsea"]),
                 RMSEA_scaled = unname(fi["rmsea.scaled"]),
                 SRMR      = unname(fi["srmr"]),
                 chisq     = unname(fi["chisq"]),
                 df        = unname(fi["df"]),
                 p         = unname(fi["pvalue"]))
    }

    fit_table <- rbind(
      get_fit(fit_configural, "configural"),
      get_fit(fit_metric,     "metric"),
      get_fit(fit_scalar,     "scalar")
    )
    write.csv(fit_table, "results/mgcfa_fit_indices.csv", row.names=FALSE)

    delta <- data.frame(
      comparison = c("metric_vs_configural", "scalar_vs_metric"),
      delta_CFI  = c(fit_table$CFI[2]-fit_table$CFI[1],
                     fit_table$CFI[3]-fit_table$CFI[2]),
      delta_CFI_scaled = c(fit_table$CFI_scaled[2]-fit_table$CFI_scaled[1],
                            fit_table$CFI_scaled[3]-fit_table$CFI_scaled[2]),
      delta_RMSEA= c(fit_table$RMSEA[2]-fit_table$RMSEA[1],
                     fit_table$RMSEA[3]-fit_table$RMSEA[2]),
      delta_RMSEA_scaled = c(fit_table$RMSEA_scaled[2]-fit_table$RMSEA_scaled[1],
                              fit_table$RMSEA_scaled[3]-fit_table$RMSEA_scaled[2])
    )
    write.csv(delta, "results/mgcfa_delta_fit.csv", row.names=FALSE)

    # Partial scalar — free one item's thresholds (ordinal => thresholds, not
    # intercepts, drive scalar invariance). We try freeing each item in turn.
    partial_rows <- list()
    partial_rows[[1]] <- get_fit(fit_scalar, "scalar_full")
    for (it in items) {
      th_free <- paste0(it, c("|t1", "|t2", "|t3"))   # 3 thresholds for 4-cat
      fit_part <- tryCatch(
        cfa(model, data=dat, group="wave",
            estimator="WLSMV",
            group.equal=c("loadings","intercepts","thresholds"),
            group.partial=th_free,
            ordered=items),
        error = function(e) NULL)
      if (!is.null(fit_part)) {
        partial_rows[[length(partial_rows)+1]] <-
          get_fit(fit_part, paste0("partial_free_", sub("conf_", "", it)))
      }
    }
    partial_table <- do.call(rbind, partial_rows)
    write.csv(partial_table, "results/mgcfa_partial_scalar.csv",
              row.names=FALSE)

    loadings_out <- parameterEstimates(fit_configural, standardized=TRUE)
    loadings_out <- loadings_out[loadings_out$op=="=~",
                    c("lhs","rhs","group","est","std.all","pvalue")]
    write.csv(loadings_out, "results/mgcfa_loadings.csv", row.names=FALSE)

    cat("\n=== FIT INDICES ===\n");  print(fit_table)
    cat("\n=== DELTA FIT  ===\n");   print(delta)
    cat("\n=== PARTIAL SCALAR ===\n"); print(partial_table)
""").strip()

R_PATH = os.path.join(ROOT, "code", "mgcfa_analysis.R")
with open(R_PATH, "w") as fh:
    fh.write(R_SCRIPT + "\n")
print(f"\nWrote R script: {R_PATH}")


# =========================================================================
# 3) Execute via Rscript
# =========================================================================
print("\nRunning Rscript mgcfa_analysis.R ...")
proc = subprocess.run(
    ["Rscript", R_PATH],
    cwd=ROOT,
    capture_output=True, text=True,
)
print("--- R stdout (tail) ---")
print("\n".join(proc.stdout.splitlines()[-80:]))
if proc.returncode != 0:
    print("--- R STDERR ---")
    print(proc.stderr[-2000:])
    raise SystemExit(f"Rscript exited with code {proc.returncode}")


# =========================================================================
# 4) Parse and report verdicts
# =========================================================================
fit  = pd.read_csv(os.path.join(RESULTS, "mgcfa_fit_indices.csv"))
delt = pd.read_csv(os.path.join(RESULTS, "mgcfa_delta_fit.csv"))
part = pd.read_csv(os.path.join(RESULTS, "mgcfa_partial_scalar.csv"))

# Use the SCALED indices for WLSMV (these are the right ones to report);
# fall back to unscaled if scaled missing.
def pick(row, scaled, unscaled):
    return row[scaled] if scaled in row and pd.notna(row[scaled]) else row[unscaled]

print("\n" + "=" * 78)
print("VERDICT TABLE — multi-group CFA, WV5/6/7, WLSMV (ordinal)")
print("=" * 78)
print(f"{'model':<14}{'CFI':>8}{'RMSEA':>10}{'SRMR':>8}    verdict")
print("-" * 70)

# Configural pass criterion: CFI > .90 and RMSEA < .08 (classical)
configural = fit.iloc[0]
cfi_c = pick(configural, "CFI_scaled", "CFI")
rms_c = pick(configural, "RMSEA_scaled", "RMSEA")
srmr_c = configural["SRMR"]
config_pass = (cfi_c > 0.90) and (rms_c < 0.08)
print(f"{'configural':<14}{cfi_c:>8.3f}{rms_c:>10.3f}{srmr_c:>8.3f}    "
      f"{'PASS' if config_pass else 'FAIL'}")

# Metric: Δscaled CFI > -.010, Δscaled RMSEA < .015
metric = fit.iloc[1]
cfi_m = pick(metric, "CFI_scaled", "CFI")
rms_m = pick(metric, "RMSEA_scaled", "RMSEA")
srmr_m = metric["SRMR"]
dcfi_m = delt.iloc[0].get("delta_CFI_scaled", delt.iloc[0]["delta_CFI"])
drmse_m = delt.iloc[0].get("delta_RMSEA_scaled", delt.iloc[0]["delta_RMSEA"])
metric_holds = (dcfi_m > -0.010) and (drmse_m < 0.015)
print(f"{'metric':<14}{cfi_m:>8.3f}{rms_m:>10.3f}{srmr_m:>8.3f}    "
      f"{'HOLDS' if metric_holds else 'FAILS'}   "
      f"(ΔCFI={dcfi_m:+.3f}, ΔRMSEA={drmse_m:+.3f})")

# Scalar
scalar = fit.iloc[2]
cfi_s = pick(scalar, "CFI_scaled", "CFI")
rms_s = pick(scalar, "RMSEA_scaled", "RMSEA")
srmr_s = scalar["SRMR"]
dcfi_s = delt.iloc[1].get("delta_CFI_scaled", delt.iloc[1]["delta_CFI"])
drmse_s = delt.iloc[1].get("delta_RMSEA_scaled", delt.iloc[1]["delta_RMSEA"])
scalar_holds = (dcfi_s > -0.010) and (drmse_s < 0.015)
print(f"{'scalar':<14}{cfi_s:>8.3f}{rms_s:>10.3f}{srmr_s:>8.3f}    "
      f"{'HOLDS' if scalar_holds else 'FAILS'}   "
      f"(ΔCFI={dcfi_s:+.3f}, ΔRMSEA={drmse_s:+.3f})")

# Partial models — pick the one with highest scaled CFI (excluding scalar_full row)
print("\n--- Partial scalar candidates (one item's thresholds freed at a time) ---")
print(part.to_string(index=False))

partial_subset = part[~part["model"].astype(str).str.startswith("scalar_full")].copy()
if not partial_subset.empty:
    cfi_col = "CFI_scaled" if "CFI_scaled" in partial_subset.columns else "CFI"
    rms_col = "RMSEA_scaled" if "RMSEA_scaled" in partial_subset.columns else "RMSEA"
    partial_subset = partial_subset.sort_values(cfi_col, ascending=False)
    best = partial_subset.iloc[0]
    best_cfi = best[cfi_col]; best_rms = best[rms_col]
    # Compare to metric — does this partial recover invariance?
    dcfi_best = best_cfi - cfi_m
    drmse_best = best_rms - rms_m
    partial_holds = (dcfi_best > -0.010) and (drmse_best < 0.015)
    print(f"\nBest partial: {best['model']}")
    print(f"  CFI={best_cfi:.3f}  RMSEA={best_rms:.3f}  SRMR={best['SRMR']:.3f}")
    print(f"  Δ vs metric: ΔCFI={dcfi_best:+.3f}  ΔRMSEA={drmse_best:+.3f}  "
          f"→ {'HOLDS' if partial_holds else 'STILL FAILS'}")

print("\n" + "=" * 78)
print("INTERPRETATION")
print("=" * 78)
if not config_pass:
    print("• Configural model fails baseline fit — the one-factor structure is")
    print("  not supported in even the most flexible specification. Reconsider")
    print("  the latent-construct assumption before proceeding.")
elif not metric_holds:
    print("• Metric invariance fails: loadings are not equivalent across waves.")
    print("  Latent-construct relationships are NOT comparable across WV5/6/7.")
elif not scalar_holds:
    print("• Metric holds, scalar fails: loadings equivalent but thresholds/")
    print("  intercepts differ. You CAN compare latent relationships across")
    print("  waves but CANNOT directly compare latent means.")
    print("  → Use partial scalar with the most non-invariant item's thresholds")
    print("    freed. Mean comparisons valid under the partial-scalar caveat.")
else:
    print("• Full scalar invariance holds. Latent means are comparable across")
    print("  waves. Both relationship and mean comparisons valid.")
print()
