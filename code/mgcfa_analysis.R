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
