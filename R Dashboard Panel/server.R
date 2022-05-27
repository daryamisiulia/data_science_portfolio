library(shiny)
library(skimr)
library(dplyr)
library(readr)
library(DT)
library(shinyjs)
df <- read.csv("insurance.csv", header = TRUE, dec = ".")
#df <- iris

shinyServer(
  function(input, output){
    
    datasetInput <- reactive({
      get(input$dataset) 
    })
    
    output$caption <- renderText({
      input$display
    })
    
    output$view <- renderTable({
      if (input$display == "Preview"){
        head(datasetInput(), 10)
      }
    })
    
    output$summary <- renderPrint({
      if (input$display == "Summary"){
        dataset <- datasetInput()
        summary(dataset)
      }
    })
      
    output$skimr <- renderPrint({
      if (input$display == "Skim"){
        dataset <- datasetInput()
        dataset %>% 
        skim_without_charts()
      }
    })
    
    
    output$downloadData <- downloadHandler(
        filename = function(){
          paste(input$dataset, input$save_data1, sep = ".")
        },
        content = function(file){
          sep <- switch(input$save_data1, "csv" = ",", "tsv" = "\t")
          write.table(datasetInput(), file, sep = sep,
                      row.names = FALSE)
      
        }
    )
    
    output$view_table <- DT::renderDataTable({
      dataset <- datasetInput()
      dataset %>% 
        select(!!! rlang::syms(input$select_col)) %>% 
        mutate_if(is.numeric, round, digits = input$decimal) %>% 
        datatable(filter = 'top', options = list(
          pageLength = 10, autoWidth = TRUE))
    })
    
    
    output$download_view <- downloadHandler(
      filename = function(){
        paste("filtered_data", Sys.Date(), ".csv", sep = "")
      },
      content = function(file){
        s = input$ds_rows_all
        write.csv(datasetInput()[input[["ex1_rows_all"]], ], file)
      }
    )
    
    observeEvent(input$refresh, {
      refresh()
    })
    
    observeEvent(input$stop, {
      stopApp()
    })
    
  }
  
  
)