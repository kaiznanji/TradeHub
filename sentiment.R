library(SentimentAnalysis)

files <- list.files(path="/Users/Kaiz Nanji/Desktop/AlgorithmicStockBot/cleantexts", pattern="*.csv", full.names=TRUE, recursive=FALSE)
lapply(files, function(x) {
  table <- read.csv(x, header=TRUE)
  text <- table[6]
  ticker <- table[1, 5]
  
  # Sentiment Analysis on text 
  sentiment <- analyzeSentiment(text)
  sentimentdata <- sentiment$SentimentQDAP
  table$SentimentQDAP <- sentimentdata
  df <- subset(table, select = -c(text.body))
  
  # Send QDAP scores in df to csv path
  mainDir <- "/Users/Kaiz Nanji/Desktop/AlgorithmicStockBot"
  subDir <- "sentiment_dfs"
  dir.create(file.path(mainDir, subDir), showWarnings = FALSE)
  setwd(file.path(mainDir, subDir))
  write.csv(df,paste(mainDir,"/",subDir,"/",ticker,".csv", sep=""), row.names = FALSE)
  
})
