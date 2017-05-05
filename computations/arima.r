#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("At least one argument must be supplied (input file)", call.=FALSE)
} else{
  data <- read.table(args[1], header=FALSE)
  print(data)
  require(forecast)
  ARIMAfit = auto.arima(data, approximation=FALSE,trace=FALSE)
  summary(ARIMAfit)
  pred = predict(ARIMAfit, n.ahead = 1)
  pred$pred[1]
}

