
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
  } else if (is.Date(end) == F){
    print("Invalid formatting for End Date")
  } 
  if (ymd(start) > ymd(end)){
    print("Invalid Start and End Date")
  }
}

