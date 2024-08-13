library(tidyverse)
library(quantmod)
library(getopt)
library(ggplot2)


get_options <- function(){
  ticker = readline(prompt = "Ticker Option: ")
  start_date = readline(prompt = "Start Date (yyyy-mm-dd): ")
  end_date = readline(prompt = "End Date (yyyy-mm-dd): ")
  
  opts_list <- data.frame(Ticker = ticker, Start = start_date, End = end_date)
  
  return(c(ticker, start_date, end_date))
}

is.Date <- function(date) {
  if (sapply(date, function(x)
    ! all(is.na(as.Date(
      as.character(x),
      format = c("%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%Y-%m-%d")
    ))))) {
    return(TRUE)
  } else{
    return(FALSE)
  }
}

check_opts <- function(ticker, start, end){
  if (is.Date(start) == F){
    print("Invalid formatting for Start Date")
    return (F)
  } else if (is.Date(end) == F){
    print("Invalid formatting for End Date")
    return (F)
  } 
  if (ymd(start) > ymd(end)){
    print("Invalid Start and End Date")
    return (F)
  }
  
  return (T)
}

makeidentity <- function(tick, st, en){
  
  stock_identity <- c(
    Ticker = tick,
    Start_Date = st,
    End_Date = en,
    div_yield_percentage = 0
  )
  
  return (stock_identity)
}

getdailyreturns <- function(series){
  daily_returns <- data.frame(dailyReturn(series)) %>%
    rownames_to_column("Dates") %>%
    mutate(Dates = ymd(Dates))
  
  return (daily_returns)
}

getdividends <- function(tick){
  
  divs <- data.frame(getDividends(Symbol = tick, src = 'yahoo', from = st, to = en)) %>%
    rownames_to_column("Dates") %>%
    rename("Dividend" = 2) %>%
    group_by(year(Dates)) %>%
    summarise(Dividend = sum(Dividend)) %>%
    mutate(year =`year(Dates)`) %>%
    ungroup()
  
  return (divs)
}

getseries <- function(tick){
  series <- getSymbols(Symbols = tick, src='yahoo', auto.assign=FALSE, from=st, to=en)
  return (series)
}

makestockdf <- function(series){
  
  stock_df <- as.data.frame(series)
  
  colnames(stock_df)[1] <- "Open"
  colnames(stock_df)[2] <- "High"
  colnames(stock_df)[3] <- "Low"
  colnames(stock_df)[4] <- "Close"
  colnames(stock_df)[5] <- "Volume"
  colnames(stock_df)[6] <- "Adjusted"
  
  return (stock_df)
}


process_stockdf <- function(stock_df, daily_returns, divs) {
  
  stock_df <- stock_df %>%
    rownames_to_column("Dates") %>%
    mutate(Dates = ymd(Dates)) %>%
    left_join(daily_returns, by = join_by(Dates)) %>%
    mutate(year = year(Dates)) %>%
    left_join(divs, by = join_by(year == year)) %>%
    mutate(div_yield = Dividend / `Close`) %>%
    mutate(div_yield_percentage = div_yield * 100) %>% 
    ungroup() %>%
    group_by(year(Dates)) %>%
    mutate(sd_returns = sd(daily.returns)) %>%
    mutate(volatility = sd_returns*sqrt(252)) %>%
    ungroup() %>%
    select(-'year(Dates)') %>%
    mutate(volatility_avg = mean(volatility))
  
  
  return (stock_df)
}

opts_list <- get_options()

tick <- opts_list[1]
st <- opts_list[2]
en <- opts_list[3]

if (check_opts(tick, st, en) == F){
  quit(status = 1)
}

series <- getseries(tick)

daily_returns <- getdailyreturns(series)
stock_identity <- makeidentity(tick, st, en)
divs <- getdividends(tick)

stock_df <- makestockdf(series)
stock_df <- process_stockdf(stock_df, daily_returns, divs)

stock_identity$div_yield_percentage <- tail(stock_df$div_yield_percentage, 1)[[1]]
stock_identity <- data.frame(stock_identity)

wd <- getwd()

stock_df_filename <- paste0(wd, "/stock_df.csv")
write.csv(stock_df, stock_df_filename, row.names = F)

stock_identity_filename <- paste0(wd, "/stock_identity.csv")
write.csv(stock_identity, stock_identity_filename, row.names = F)













