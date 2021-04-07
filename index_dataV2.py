# Import Elasticsearch package 
from elasticsearch import Elasticsearch 
import pandas as pd
import numpy as np
print("starting..")
# Connect to the elastic cluster
es2=Elasticsearch([{'host':'localhost','port':9200}])
#load the data
df = pd.read_csv("twitter_dataset.csv")
hdf = df.drop_duplicates('Text')
Reddit_df = pd.read_csv("reddit_dataset.csv")
def index_data(df, asset):
    for index, row in df.iterrows():
        #print(value)
        print(index)
        e = {
                "intent":row["Query"],
                "text": row["Text"],
				"vader": row["VADER"]
            }
        es2.index(index = asset,body = e)
fdf= Reddit_df.dropna()
index_data(Reddit_df, "reddit")
print("**********")
index_data(hdf, "twitter")

print("data indexing complete")