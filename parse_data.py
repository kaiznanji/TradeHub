# In this file we plan to scrape the SEC database to obtain publically
# available 10-K and 10-Q documents through recent activity in filings and store
# the cleaned data in a database for cosine similarity tests and sentiment analysis

# Importing libraries
import bs4 as bs
import requests
from joblib import dump, load
import datetime as dt
import time
import pandas as pd
import re
import os
import string as s
from string import digits


# Get the recent filings in the past day
def get_filing_links():
    main_url = 'https://www.sec.gov/'
    url = 'https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=&owner=include&count=100&action=getcurrent'
    filing_links = []
    boolean = True
    # Run loop until date is not yesterday or no more recent filings
    while boolean:
        links = []
        resp = requests.get(url).text
        soup = bs.BeautifulSoup(resp, features='html.parser')

        # Get all links for filings on each page
        for x in soup.find_all("a"):
            link = x.text + 'https://www.sec.gov' + x.get('href')
            if "cgi-bin/browse-edgar?action=getcompany&CIK=" in link:
                links.append(link)

        # Narrow the search by Issuer and if date corresponds to yesterday
        for element in range(len(links)):
            if ("Issuer" in links[element]): 
                filing_links.append(links[element].split("(Issuer)",1)[1])
          
        # Pagination process
        try:
            form = soup.find_all('input', {'value' : 'Next 100'})[0]      
            url = form.get('onclick').split("'")[1]
            url = main_url + url
        except:
            boolean = False

    filing_links = list(dict.fromkeys(filing_links))
    return filing_links
    

# Make an array with all 10-k and 10-q links for each filing link
def filings_10k_q():
    filings = get_filing_links()
    main_url = 'https://www.sec.gov/'
    file_links = []
    before_date = dt.datetime(2016, 1, 1)
    
    # Get 10-k links in the past two years and 10-q links after last 10-k form
    for file in filings:
        company_10k_links = []
        company_10q_links = []
        last_10k_date = []
        url_k = file[:73] + '&type=10-k&dateb=' + file[73:] + '&search_text='
        resp_k = requests.get(url_k)
        soup_k = bs.BeautifulSoup(resp_k.text, 'html.parser')
        table_k = soup_k.find('table', {'class' : 'tableFile2'})
        
        # Track file creation
        if file == filings[round(len(filings)/4)]:
            print("********* 25% completed *********")
        if file == filings[round(len(filings)/2)]:
            print("********* 50% completed *********")
        if file == filings[round(3*len(filings)/4)]:
            print("********* 75% completed *********")

        # Get 10-k filing links 
        for row in table_k.find_all('tr')[1:]:
            try:
                date = row.find_all('td')[3].text
                filing_date = dt.datetime.strptime(date, '%Y-%m-%d')

                if row.find('td').text == '10-K' and  filing_date >= before_date:
                    href = row.find_all('a')[0]['href']
                    link = main_url + href
                    file_resp = requests.get(link)
                    file_soup = bs.BeautifulSoup(file_resp.text, 'html.parser')
                    file_table = file_soup.find('table', {'class' : 'tableFile'})

                    # Get end date for last 10-k form
                    info = file_soup.find('div', {'class' : 'formContent'})
                    last_date = info.find_all('div')[2].text
                    last_10k_date.append(last_date)

                    # Find link to complete submission text file for 10-k filing
                    for tr in file_table.find_all('tr')[1:]:
                        if tr.find_all('td')[1].text == 'Complete submission text file':
                            file_href = tr.find_all('a')[0]['href']
                            file_link = main_url + file_href
                            company_10k_links.append(file_link)
            except:
                print("filing did not have available 10-K documents")
        
        # Get 10-q filing links
        url_q = file[:73] + '&type=10-q&dateb=' + file[73:] + '&search_text='
        resp_q = requests.get(url_q)
        soup_q = bs.BeautifulSoup(resp_q.text, 'html.parser')
        table_q = soup_q.find('table', {'class' : 'tableFile2'})
        for row in table_q.find_all('tr')[1:]:
            try:
                end_date = dt.datetime.strptime(last_10k_date[0], '%Y-%m-%d')
                date = row.find_all('td')[3].text
                filing_date = dt.datetime.strptime(date, '%Y-%m-%d')

                if row.find('td').text == '10-Q' and  filing_date >= end_date:
                    href = row.find_all('a')[0]['href']
                    link = main_url + href
                    file_resp = requests.get(link)
                    file_soup = bs.BeautifulSoup(file_resp.text, 'html.parser')
                    file_table = file_soup.find('table', {'class' : 'tableFile'})

                    # Find link to complete submission text file for 10-q filing
                    for tr in file_table.find_all('tr')[1:]:
                       if tr.find_all('td')[1].text == 'Complete submission text file':
                            file_href = tr.find_all('a')[0]['href']
                            file_link = main_url + file_href
                            company_10q_links.append(file_link)
            except:
                print("filing did not have available 10-Q")
        
        file_links.append(company_10q_links + company_10k_links)
    print("********* File Created *********")
    dump(file_links, "filings")
    

# Get database with cleaned text given a list of 10-q and 10-k links to SEC filing texts
def clean_text():
    file = load("filings")
    folder = "cleantexts"
    counter = 20
    for links in file[20:]:
        cleaned_text = []
        dates = []
        tickers = []
        CIKs = []
        filing_types = []
        # Create directory for csv files
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Process only filings that have sufficient 10-k and 10-q documents
        if len(links) > 6:
            # Get ticker, CIK for building the dataframe
            resp = requests.get(links[0])
            soup = bs.BeautifulSoup(resp.text, 'lxml')
            ticker = soup.find('filename').text.split('-')[0].upper()
            split_link = links[0].split('data/')[1]
            CIK = split_link[:split_link.find('/')]
            tick = []

            # Function to obtain the right ticker
            for char in list(ticker):
                if char.isalpha():
                    tick.append(char)
                else:
                    break
            ticker = ''.join(tick)

            # Loop through links and build database with cleaned text for each link
            for link in links:
                response = requests.get(link)
                try:
                    s = bs.BeautifulSoup(response.text, 'html.parser')
                except:
                    s = bs.BeautifulSoup(response.content, 'lxml')

                header = s.find('acceptance-datetime').text
                filing_type = header[82:86]
                date = header[:8]
                main_text = s.find('text').text 
                
                # Cleansing proccess
                main_text = re.sub(r'[0-9]+', '', main_text)
                main_text = re.sub(r'\W+', ' ', main_text)
                main_text = re.sub(r'\b\w{,3}\b', '', main_text)
                main_text = re.sub(r'\b\w{13,}\b', '', main_text)
                main_text = re.sub(r'\b(\w+)( \1\b)+', r'\1', main_text)
                main_text = main_text.replace("_", '')
                main_text = main_text.replace("gaap", "")
                main_text = main_text.replace(ticker.lower(), "")
                main_text = re.sub(' +', ' ', main_text)
                

                # Remove additional repeating words
                main_text = re.sub(r"\b(\w+)( \1\b)+", r"\1", main_text)
                
                # Preproccessing lists for dataframe
                cleaned_text.append(main_text)
                dates.append(date)
                tickers.append(ticker)
                CIKs.append(CIK)
                filing_types.append(filing_type)
            
            # Create dataframe of recent company 10-k and 10-q cleaned text
            df = pd.DataFrame({'CIK' : CIKs, 'Filing Type' : filing_types,
                             'Date': dates, 'Ticker' : tickers, 'text body' : cleaned_text}) 
            path = str(ticker) + ".csv"                     
            df.to_csv(os.path.join(folder, path))
            print('********* '+ path +' (' + str(counter) + ') file created *********')
            counter += 1





