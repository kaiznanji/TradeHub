# TradeHub

TradeHub is an algorithmic ticker signal that analyzes earnings reports from the SEC to predict future returns. 

## How it works

[Webscraping](https://github.com/kaiznanji/TradeHub/blob/main/parse_data.py): The bot automates webscraping from the SEC(Securities and Exchange Commission) using the library BeautifulSoup. It looks for recent filings reported by issuing companies in the past 24 hours. It then scrapes 10-K and 10-Q reports of each company in the past 4 years for data cleaning and analysis.

[Pre-Proccessing](https://github.com/kaiznanji/TradeHub/blob/main/parse_data.py): After loading the important data into a dataframe using pandas, the text of the reports is extracted and cleansed for further natural language proccessing methods. 

[Analysis](https://github.com/kaiznanji/TradeHub): With the cleaned text the bot performs sentiment analysis and cosine similarity tests to track changes in reporting languages over each report and correlates positive and negative QDAP(Polarity) scores with future investement returns. The result is hypothesized to be the following:

#### Difference in Reporting Language(DIRL) and Sentiment Correlation to Returns

* Sentiment > 0% and DIRL > average difference  --->  at least +5% return

* Sentiment > 0% and DIRL < average difference  --->  0% to 5% return
                        
* Sentiment < 0% and DIRL < average difference  --->  -5% to 0% return

* Sentiment < 0% and DIRL > average difference  --->  less than -5% return


<p align="center">
  <img src="https://github.com/kaiznanji/TradeHub/blob/main/sample_data/results/graph.png?raw=true",width=550,height=450/>
</p>
 


## Results

Looking at the graph for the company *Ameresco Inc.* we can see a correlation between identifying changes in the market when reporting language and sentiment changes in earnings reports. To identify whether the bot made better predictions in the short run or long run I ran accuracy tests. I computed investement returns in 1 week, 1 month, 3 months, and 6 months achieved the following accuracy in predicting potential future returns.


<p align="center">
  <img src="https://github.com/kaiznanji/TradeHub/blob/main/sample_data/results/predictions.png?raw=true", width=700, height=100/>
</p>


## Improvements
This bot serves as an suitable foundation to predicting long term investement returns, specifically 3-6 months. For improvements I might decide to investigate the transfers of securities(Form 4), which provide signals to predicting short term returns in the market.





