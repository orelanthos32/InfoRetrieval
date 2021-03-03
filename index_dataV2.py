# Import Elasticsearch package 
from elasticsearch import Elasticsearch 
import pandas as pd
import numpy as np
# Connect to the elastic cluster
es2=Elasticsearch([{'host':'localhost','port':9200}])
#load the data
df = pd.read_csv("stockticker10-tweets(dataset 23-2-21).csv")
#hdf = df.drop_duplicates('IntentDesc')
#hdf["combine"] = hdf["IntentDesc"] +" "+ hdf["KBResponseText"]
def index_data(df):
    for index, row in df.iterrows():
        #print(value)
        print(index)
        e = {
                "intent":row["Query"],
                #"text": row["CategoryDesc"] + " " + row["IntentDesc"]+ " " + row["SubCategoryDesc"]
                "text": row["Text"]

            }
        es2.index(index = "first", doc_type= "word",id =index,body = e)
index_data(df)
print("data indexing complete")