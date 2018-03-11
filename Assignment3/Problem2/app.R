library(shiny)
library(tidyverse)
library(ggthemes)
library(devtools)
#install_github("leeper/slopegraph")#install Leeper's package from Github
library(slopegraph)

df <- read_csv('data.csv')
CoDChoice <- unique(df$ICD.Chapter)
yearChoice <- unique(df$Year)


stockGraph <- function(CoD, year1, year2){
  df <- read_csv('data.csv')
  avg1 <- df %>% 
    filter(Year == year1 | Year == year2) %>% 
    filter(ICD.Chapter == CoD) %>% 
    group_by(Year) %>% 
    summarise(usaMean = mean(Deaths) / mean(Population) * 100000) %>% t()
  
  
  df1 <- df %>% 
    filter(Year == year1 | Year == year2) %>% 
    filter(ICD.Chapter == CoD) %>% 
    select(State, Year, Crude.Rate) %>% 
    spread(key = Year, value = Crude.Rate)
  df1 <- rbind(df1, c('USA', avg1[2,]))
  df1 <- data.frame(df1, row.names = df1$State) %>% 
    select(-State)
  df1[, 1] <- as.numeric(df1[, 1])
  df1[, 2] <- as.numeric(df1[, 2])
  cols <- `[<-`(rep("grey30", nrow(df1) - 1), nrow(df1), "red")
  slopegraph(df1, 
             main = paste("Delta Death Rate for", 
                          CoD, "\n Between", 
                          year1, 'and', year2),
             col.lines = cols,
             col.lab = cols,
             leftlabels = rownames(df1),
             rightlabels = rownames(df1),
             decimals = 2)
}

ui <-  fluidPage(
  headerPanel("Change in Death Rates Between Any Two Years"),
  sidebarPanel(
    selectInput('CoD', 'Cause of Death', choices = CoDChoice,
                selected = "Endocrine, nutritional and metabolic diseases"),
    selectInput('year1', 'Year 1', choices = yearChoice, selected = 2000),
    selectInput('year2', 'Year 2', choices = yearChoice, selected = 2010)
  ),
  mainPanel(
    plotOutput('plot', height = 1000)
  )
)


# Define the server code
server <- function(input, output) {
  output$plot <- renderPlot({stockGraph(CoD = input$CoD, 
                                          year1 = input$year1, 
                                          year2 = input$year2)})
}

# Return a Shiny app object
shinyApp(ui = ui, server = server)