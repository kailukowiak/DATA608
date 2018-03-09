# Question 1:
# As a researcher, you frequently compare mortality rates from particular causes across
# different States. You need a visualization that will let you see (for 2010 only) the crude
# mortality rate, across all States, from one cause (for example, Neoplasms, which are
# effectively cancers). Create a visualization that allows you to rank States by crude mortality
# for each cause of death.




# Global variables can go here
library(tidyquant)
library(tidyr)
library(dplyr)
library(ggplot2)
library(ggthemes)
library(knitr)
library(gridExtra)
n <- 'AAPL'

stockGraph <- function(name){
  from <- today() - years(1)
  df <- tq_get(name, get = "stock.prices", from = from)
  x <- cbind(runVar(df$close, y = NULL, n = 10, sample = TRUE, cumulative = FALSE), df$date) %>% 
    # t() %>% # To transpose the matrix into a virticle column. %>% 
    data.frame()
  
  x$X2 <- x$X2 %>% as.Date()
  x = x %>% rename(Date = X2) %>% rename(Variance = X1)
  varGraph <- ggplot(x, aes(x = Date, y = Variance)) + 
    geom_line()
  avgGraph <- df %>%
    tq_mutate(ohlc_fun = Cl, mutate_fun = SMA, n = 5) %>%
    rename(SMA.5 = SMA) %>%
    tq_mutate(ohlc_fun = Cl, mutate_fun = SMA, n = 20) %>%
    rename(SMA.20 = SMA) %>% 
    ggplot( aes(x = date)) + 
    geom_line(aes(y = SMA.5, colour = "5 Day Average")) + 
    geom_line(aes(y = SMA.20, colour = "20 Day Average")) +
    geom_line(aes(y = close, colour = "Closing Price")) +
    xlab('Date') +
    ylab('Price') + 
    ggtitle('Moving Averages')
  bbGraph <- df %>%
    ggplot(aes(x = date, y = close)) +
    geom_line() + 
    geom_bbands(aes(high = high, low = low, close = close), ma_fun = SMA, n = 20) 
  grid.arrange(varGraph,avgGraph, bbGraph, ncol=1)
  
}
# Define the UI
ui <- bootstrapPage(
  textInput('n', 'Enter a stock', n),
  plotOutput('plot')
)


# Define the server code
server <- function(input, output) {
  output$plot <- renderPlot({
    stockGraph(input$n)
    
  })
}

# Return a Shiny app object
shinyApp(ui = ui, server = server)