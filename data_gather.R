



opts_list <- get_options()

tick <- opts_list[1]
st <- opts_list[2]
en <- opts_list[3]

check_opts(tick, st, en)

series <- getseries(tick)

daily_returns <- getdailyreturns(series)
stock_identity <- makeidentity(tick, st, en)
divs <- getdividends(tick)

stock_df <- makestockdf(series)

stock_df <- process_stockdf(stock_df, dailyreturns, divs)

stock_identity$div_yield_percentage <- tail(stock_df$div_yield_percentage, 1)[[1]]