# Import Elasticsearch package 
from elasticsearch import Elasticsearch 
import pandas as pd
import numpy as np
# Connect to the elastic cluster
es2=Elasticsearch([{'host':'localhost','port':9200}])
#load the data
df = pd.read_csv("stockticker10-tweets(5-3-21).csv")
#hdf = df.drop_duplicates('Text')
def index_data(df, index):
    for index, row in df.iterrows():
        #print(value)
        print(index)
        e = {
                "intent":row["Query"],
                "text": row["Text"]

            }
        es2.index(index = index, doc_type= "word",id =index,body = e)
index_data(df, "Twitter")
Reddit_df = pd.read_csv("MAIN_Reddit_Manual - gme1616872068 (1)")
index_data(Reddit_df, "Reddit")

print("data indexing complete")