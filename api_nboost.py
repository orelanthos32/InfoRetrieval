import flask
from flask import request, jsonify, render_template
import pandas as pd
import numpy as np
import re
import requests
from elasticsearch import Elasticsearch 
import os

es2=Elasticsearch([{'host':'localhost','port':9200}])
def index_data(file, overwrite = 0):
    print("read data")
    df = pd.read_csv(file)
    print("read success")
    df.drop_duplicates('IntentDesc',inplace=True)
    print("removed duplicate")
    df["combine"] = df["IntentDesc"] +" "+ df["KBResponseText"]
    if overwrite == 1:
        delete_sys = df.iloc[0]["CampaignID"]
        #delete current index
        try:
            os.system("curl -X DELETE 'http://localhost:9200/" + str(delete_sys) + "'")
        except:
            pass
    elif overwrite == 2:
        os.system("curl -X DELETE 'http://localhost:9200/_all")
    print("start indexing")
    for index, row in df.iterrows():
        print(index)
        e = {
                "intent":row["IntentDesc"],
                #"text": row["CategoryDesc"] + " " + row["IntentDesc"]+ " " + row["SubCategoryDesc"]
                "text": row["combine"],
                "intentID":row["IntentID"]

            }
        es2.index(index =row["CampaignID"], doc_type= "miki",id = row["IntentID"], body = e)
        print("index success")


    

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#read file
def search(text, system):
    result_list = []
    intent_list = []
    word_list = []
    response = requests.get(url='http://localhost:8000/' + system +'/_search',
        json={
            'nboost': {
                'uhost': 'db1',
                'uport': 9200,
                'query_path': 'body.query.match.text',
                'topk_path': 'body.size',
                'default_topk': 100,
                'topn': 100,
                'choices_path': 'body.hits.hits',
                'cvalues_path': '_source.text'
            },
            'size': 100,
            'query': {
                'match': {'text': text}
            }
        })

#    print(type(response.json()))
    for hit in response.json()['hits']['hits']:
        score = hit['_score']
        result_list.append(score)
        intent = hit["_source"]["intent"]
        intent_list.append(intent)
        word = hit["_source"]["text"]
        word_list.append(word)

    return intent_list,word_list,result_list

#get list of intents from database
#database not get set up so its manually filled in

def do_search(text,system):
    x, y,z = search(text, system)
    rdf = pd.DataFrame(list(zip(x, y,z)), 
               columns =['Tweet of:'+system,'tweet', 'score'])
    return rdf
    
@app.route('/upload', methods = ['GET', 'POST'])
def upload_start():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        try:
            index_data(f, overwrite = 1)
            return 'file uploaded successfully'
        except:
            return "file upload unsuccessful"
@app.route('/overwrite', methods = ['GET', 'POST'])
def overwrite_start():
    return render_template('overwrite.html')
        
@app.route('/overwriten', methods = ['GET', 'POST'])
def overwrite_file():
    if request.method == 'POST':
        f= request.files['file']
        try:
            index_data(f,overwrite = 2)
            return 'file uploaded successfully'
        except:
#            os.system("python3 index_dataV2.py")
            return "file upload unsuccessful"

@app.route('/', methods=['GET',"POST"])
def home():
    return render_template('index.html', title='Home')

@app.route('/action_page',methods = ['POST', 'GET'])
def action():
    if request.method == 'POST':
        query = request.form["fname"]
        system = request.form["system"]
    x = do_search(query,system)
    return render_template('index2.html', result = x.to_html(), search = query)

@app.route('/api/v1', methods=['GET'])
def api_id():
    if 'term' in request.args:
        query = (request.args['term'])
        system = (request.args['system'])
    else:
        return "Error: No id field provided. Please specify an id."
    x = do_search(query, system)
    return x.to_html()
	
@app.route('/api/v1/json', methods=['GET'])
def api_json():
    if 'term' in request.args:
        query = (request.args['term'])
        system = (request.args['system'])
    else:
        return "Error: No id field provided. Please specify an id."
    x = do_search(query, system)
    return x.to_json()



app.run(host = '0.0.0.0', port = 5000)