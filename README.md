# TradeHub

TradeHub is an algorithmic stock bot that analyzes earnings reports from the SEC to predict future returns. 

# How it works

Webscraping: The bot automates webscraping from the SEC(Securities and Exchange Commission) using the library BeautifulSoup! It looks for recent filings reported by issuing companies in the past 24 hours. It then scrapes 10-K and 10-Q reports of each company in the past 4 years for data cleaning and analysis.

Pre-Proccessing: After loading the important data into a dataframe using pandas, the text of the reports is extracted and cleansed for further natural language proccessing methods. 

Analysis: With the cleaned text the bot performs sentiment analysis and cosine similarity tests to track changes in reporting languages over each report and correlates positive and negative QDAP(Polarity) scores with future investement returns.




![alt text](https://github.com/kaiznanji/TradeHub/?raw=true)

