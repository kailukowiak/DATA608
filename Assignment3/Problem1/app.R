library(shiny)
library(plotly)
library(tidyverse)
library(ggthemes)
library(gridExtra)

df <- read_csv('data.csv')
CoDChoice <- unique(df$ICD.Chapter)
yearChoice <- unique(df$Year)


stockGraph <- function(df, CoD, year, OrderPlot){
  df <- read_csv('data.csv')
  df <- df %>% 
    dplyr::filter(Year == year & ICD.Chapter == CoD) %>% 
    dplyr::arrange(Crude.Rate)
  
  p1 <- plot_ly(
    x = df$State,
    y = df$Crude.Rate,
    name = "Death Rate",
    type = "bar",
    marker = list(color = "#737373")
  ) 
  if (OrderPlot == 'Alphabetical'){
    p1 <- p1 %>% layout(tickmode = "array", yaxis = list(title = "", showgrid = F))
  } else if (OrderPlot == 'Descending'){
    xform <- list(categoryorder = "array",
                  categoryarray = rev(df$State))
    p1 <- p1 %>% layout(xaxis = xform, tickmode = "array", yaxis = list(title = "", showgrid = F))
  } else {
    xform <- list(categoryorder = "array",
                  categoryarray = df$State)
    p1 <- p1 %>% layout(xaxis = xform, tickmode = "array", yaxis = list(title = "", showgrid = F))
  }
  p1 
}

ui <-  fluidPage(
  fluidRow(
  headerPanel("Cause of Death by Year for American States")),
  plotlyOutput('plot', height = 300),
  hr(),
  fluidRow(
  sidebarPanel(
    selectInput('CoD', 'Cause of Death', choices = CoDChoice,
                selected = "Endocrine, nutritional and metabolic diseases"),
    selectInput('orderPlot', 'Order of Data', choices = c('Alphabetical', 'Ascending', 'Descending'),
                selected = "Assending"),
    selectInput('year', 'Year', choices = yearChoice, selected = 2010)
  ))
    
  )


# Define the server code
server <- function(input, output) {
  output$plot <- renderPlotly({stockGraph(df = input$df, 
                                          CoD = input$CoD, 
                                          year = input$year, 
                                          OrderPlot = input$orderPlot)})
}

# Return a Shiny app object
shinyApp(ui = ui, server = server)