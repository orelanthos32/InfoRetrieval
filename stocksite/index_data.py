from elasticsearch import Elasticsearch 
import pandas as pd
import numpy as np
es2=Elasticsearch([{'host':'localhost','port':9200}])
df = pd.read_csv("stockapp/twitter_dataset.csv")
hdf = df.drop_duplicates('Text')
Reddit_df = pd.read_csv("stockapp/reddit_dataset.csv")
def index_data(df, asset):
    for index, row in df.iterrows():
        print(index)
        e = {
                "intent": row["Query"],
                "text": row["Text"],
                "vader": row["VADER"]

            }
        es2.index(index = asset,body = e)
fdf= Reddit_df.dropna()
index_data(Reddit_df, "reddit")
print("**********")
index_data(hdf, "twitter")
print("data indexing complete")
