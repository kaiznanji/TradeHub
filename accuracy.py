# In this file we test the program's accuracy for short term and long term predictions

# Import libraries
import pandas as pd
import datetime as dt
import os
import holidays


# Test the accuracy of the model for recent earnings reports
def test_accuracy():
    full_path_df = "C:\\Users\\Kaiz Nanji\\Desktop\\AlgorithmicStockBot\\sentiment_dfs\\"
    full_path_stocks = full_path_df.replace("sentiment_dfs", "stockdata")
    week_count = 0
    month_count = 0
    three_month_count = 0
    six_month_count = 0
    count_row = 0

    for path in os.listdir("sentiment_dfs"):
        df = pd.read_csv(full_path_df + path, parse_dates=True, index_col=3)
        count_row += df.shape[0]
        dates = df.index
        sentiment = df['SentimentQDAP'].values
        similarity = df['cosine similarity'].values
        avg_similarity = sum(similarity)/len(similarity)
        stocks = pd.read_csv(full_path_stocks+path, parse_dates=True, index_col=0)

        for date in dates:
            
            # Remove stocks that don't have enough stock data
            if date not in stocks.index:
                os.remove(full_path_df+path)
                os.remove(full_path_stocks+path)
                os.remove("C:\\Users\\Kaiz Nanji\\Desktop\\AlgorithmicStockBot\\cleantexts\\"+path)
                break

            price1 = stocks[stocks.index == date]['Adj Close'][0]
            week, month = date + pd.DateOffset(days=7), date + pd.DateOffset(days=30)
            three_month, six_month = date + pd.DateOffset(days=90), date + pd.DateOffset(days=180)

            # Check if the return dates exist
            return_dates = []
            for x in [week,month,three_month,six_month]:
                if x < pd.to_datetime('today').normalize():
                    # If date doesnt exist or on date where market is close return most recent day
                    while x not in stocks.index:
                        x = x - pd.DateOffset(days=1)
                    return_dates.append(x)
                else:
                    x = pd.to_datetime(stocks.index[-1])
                    return_dates.append(x)
        
            

        for x,y in zip(sentiment, similarity):
            for return_date in return_dates:
                price2 = stocks[stocks.index == return_date]['Adj Close'][0]
                net_return = price2 - price1
                current_value = stocks['Adj Close'][-1]
                roi = net_return/current_value
                if y > 0 and x > avg_similarity and roi > 0:
                    if return_date == return_dates[0]: week_count += 1 
                    if return_date == return_dates[1]: month_count+=1 
                    if return_date == return_dates[2]: three_month_count+=1 
                    if return_date == return_dates[3]: six_month_count+=1 
                    
                elif y > 0 and x <= avg_similarity and roi >= 0:
                    if return_date == return_dates[0]: week_count+=1 
                    if return_date == return_dates[1]: month_count+=1 
                    if return_date == return_dates[2]: three_month_count+=1 
                    if return_date == return_dates[3]: six_month_count+=1 
                     
                elif y < 0 and x > avg_similarity and roi < 0:
                    if return_date == return_dates[0]: week_count+=1 
                    if return_date == return_dates[1]: month_count+=1 
                    if return_date == return_dates[2]: three_month_count+=1 
                    if return_date == return_dates[3]: six_month_count+=1 

                elif y < 0 and x <= avg_similarity and roi < 0:
                    if return_date == return_dates[0]: week_count+=1 
                    if return_date == return_dates[1]: month_count+=1 
                    if return_date == return_dates[2]: three_month_count+=1 
                    if return_date == return_dates[3]: six_month_count+=1 
    

    print("Bot had a "+str((week_count/count_row)*100) +"% accuracy rate when predicting in the short term(1 WEEK)")
    print("Bot had a "+str((month_count/count_row)*100)+"% accuracy rate when predicting in the short term(1 MONTH)")
    print("Bot had a "+str((three_month_count/count_row)*100)+"% accuracy rate when predicting in the long term(3 MONTHS)")
    print("Bot had a "+str((six_month_count/count_row)*100)+"% accuracy rate when predicting in the long term(6 MONTHS)")



test_accuracy()




    
