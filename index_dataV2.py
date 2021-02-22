# Import Elasticsearch package 
from elasticsearch import Elasticsearch 
import pandas as pd
import numpy as np
# Connect to the elastic cluster
es2=Elasticsearch([{'host':'localhost','port':9200}])
#load the data
df = pd.read_excel("Intern.xlsx")
hdf = df.drop_duplicates('IntentDesc')
hdf["combine"] = hdf["IntentDesc"] +" "+ hdf["KBResponseText"]
def index_data(df):
    for index, row in df.iterrows():
        #print(value)
        print(index)
        e = {
                "intent":row["IntentDesc"],
                #"text": row["CategoryDesc"] + " " + row["IntentDesc"]+ " " + row["SubCategoryDesc"]
                "text": row["combine"]

            }
        es2.index(index =row["CampaignName"].lower(),doc_type= "miki",id =index,body = e)
index_data(hdf)
print("data indexing complete")