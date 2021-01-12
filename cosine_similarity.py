# In this file we will perform cosine similarity tests on the cleaned texts 

# Importing libraries 
import numpy as np
import pandas as pd
import os
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Path to csv files in folder
def pathing():
    file = "cleantexts"
    filing_links = []
    for path in os.listdir(file):
        full_path = os.path.join(file, path)
        if os.path.isfile(full_path):
            filing_links.append(full_path)
    
    return filing_links

# Computes cosine similarity matrix 
def vectorize(path):
    df = pd.read_csv(path)
    texts = df['text body'].values
    vectorizer = CountVectorizer()
    matrix = vectorizer.fit_transform(texts)
    cosine_sim = cosine_similarity(matrix)
    return cosine_sim
        
# Path cosine similarity scores to analyzed df's
def add_to_dfs():
    filing_links = pathing()
    for file in filing_links[6:7]:
        matrix = vectorize(file)
        df = pd.read_csv(file.replace("cleantexts", "sentiment_dfs"))
  
        # Change cosine similarity data to change so it is more visually accurate(track difference between each report)
        df_cosine = list(matrix[0])
        this_item = df_cosine[0]
        cosine_values = []
        for item in df_cosine:
            prev_item = np.array(this_item)
            this_item = np.array(item)
            cosine_values.append(abs(this_item-prev_item))
        df['cosine similarity'] = cosine_values


        # Send back to folder
        df.to_csv(os.path.join("sentiment_dfs", file.replace("cleantexts\\", "")))

add_to_dfs()



