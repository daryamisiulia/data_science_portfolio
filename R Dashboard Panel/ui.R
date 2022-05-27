library(shiny)
library(shinythemes)
library(readr)
library(DT)
library(shinyWidgets)
library(shinyjs)
df <- read.csv("insurance.csv", header = TRUE, dec = ".")
#df <- iris 

shinyUI(fluidPage(theme = shinytheme("cerulean"),
        useShinyjs(),
        navbarPage(title = "Shiny App",
                   tabPanel("Data Explorer",
                            tabsetPanel(
                              tabPanel("Manage",
                                       sidebarLayout(
                                         sidebarPanel(
                                           selectInput(inputId = "dataset",
                                                       label = "Dataset:",
                                                       choices = c("income" = "df")),
                                           radioButtons(inputId = "display",
                                                        label = "Display:",
                                                        choices = list("Preview",
                                                                       "Summary",
                                                                       "Skim"),
                                                        selected = "Preview"),
                                           selectInput(inputId = "save_data1",
                                                       label = "Download type:",
                                                       choices = c("csv",
                                                                   "tsv" )),
                                           helpText("Click on the download button to download the dataset observations."),
                                           downloadButton("downloadData", "Download")
                                         ),
                                         mainPanel(
                                           h3(textOutput("caption", container = span)),
                                           verbatimTextOutput("summary"),
                                           tableOutput("view"),
                                           verbatimTextOutput("skimr")
                                         )
                                       )),
                              tabPanel("View",
                                       sidebarLayout(
                                         sidebarPanel(
                                           pickerInput(inputId = "select_col",
                                                          label = "Select variables to show:",
                                                          choices = names(df), selected = names(df), options = list('actions-box' = TRUE), multiple = TRUE),
                                           numericInput(inputId = "decimal", label = "Decimals:", value = 2, min = 0, max = 4),
                                           downloadButton("download_view", "Download Filtered Data")
                                         ),
                                         mainPanel(
                                           DT::dataTableOutput("view_table"),
                                           #verbatimTextOutput("filtered_row")
                                         )
                                       )),
                              tabPanel("Plot"),
                              tabPanel("Explotet"),
                              tabPanel("Transform")
                            )
                   ),
                   tabPanel("Model",
                            tabsetPanel(
                              tabPanel("Summary"),
                              tabPanel("Predict"),
                              tabPanel("Plot")
                            )),
                   navbarMenu("Info",
                            tabPanel("About application"),
                            tabPanel("Help")
                            ),
                   navbarMenu("Session",
                              tabPanel(actionLink("refresh", "Refresh")),
                              tabPanel(actionLink("stop", "Stop"))
                              )
                   
          
          
          
          
        )
  
  
  
))
        