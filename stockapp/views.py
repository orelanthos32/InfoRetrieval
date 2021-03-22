from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
#from django.template import loader
from django.shortcuts import render
from elasticsearch import Elasticsearch
import pandas as pd
import numpy as np
import json
from os import path
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import io
import urllib, base64
from .forms import DataForm, SearchForm
#takes web request and returns web response

from .models import RedditCsvModel;
es2=Elasticsearch([{'host':'localhost','port':9200}])


# Main Page to select source
def sourcepage(request):  

    df = pd.read_csv("stockticker10-tweets(5-3-21).csv")
    #hdf = df.drop_duplicates('IntentDesc')
    #hdf["combine"] = hdf["IntentDesc"] +" "+ hdf["KBResponseText"]
    def index_data(df):
        for index, row in df.iterrows():
            print(index)
            e = { "intent":row["Query"],
                    "text": row["Text"]
                }
            es2.index(index = "first", doc_type= "word",id =index,body = e)
    index_data(df)
    print("Index Completed")


    if request.method == "POST":    # Checks if the form was posted
        form = DataForm(request.POST)
    else:
        form = DataForm()
    return render(request, 'sourcepage.html', {'form' : form})  # Giving template and data back to the view


# Search Query Page
# Integrate api here
def homepage(request):  

    if request.method == "POST":
        form2 = DataForm(request.POST)  # Form to change source, maybe can change to get?
        form = SearchForm(request.POST)

        if request.POST.get('source'):
            chosenSource = request.POST['source']
            request.session['chosenSource'] = chosenSource
            
            return render(request, 'homepage.html', {'source' : chosenSource, 'form': form, 'form2': form2})
        else:
            form2 = DataForm()

        if request.POST.get('searchtext'):
            chosenSource = request.session['chosenSource']
            if form.is_valid():
                text = form.cleaned_data['searchtext']  # Search text is found under FOmrs
            return render(request, 'homepage.html', { 'source' : chosenSource ,'query' : text ,'form': form, 'form2': form2}) # Working but drop down not helping
        else:
            form = SearchForm()
               
    return render(request, 'homepage.html', {'form' : form, 'form2' : form2})
    # TO view in html, use the left side of the dict
    

def results(request):
    df = pd.read_csv("stockapp/RedditStonks.csv")
    freqdf = df.sort_values(by = 'Frequency', ascending = False)
    freqdf = freqdf.head(10)
    #pasrsing dataframe into json format
    json_records = freqdf.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data}
    
    return render(request, 'results.html', context)


def words(request):
    df = pd.read_csv("stockapp/RedditStonks.csv")
    transformColumn(df, 'clearLast Sale', float)
    transformColumn(df, 'Term', 'str')
    transformColumn(df, 'Country', str)


    #Start of bar Visualisation ( Chart.js)
    bestsalesdf = df.sort_values(by = 'Last Sale', ascending = False)
    bestsalesdf = bestsalesdf[["Term", "Last Sale"]]
    bestsalesdf = bestsalesdf.head(10)

    worstsalesdf = df.sort_values(by = 'Last Sale', ascending = True)
    worstsalesdf = worstsalesdf.head(10)

    def transformColumn(s,col, type):
        if col == 'Last Sale':
            s[col] = s[col].str.replace('$', '')
        s[col] = s[col].astype(type)
        

    # Whatever data comes here
    # Pass through json form
    # Then create the data by appeninding it all into a list
    # to display
    

    json_records = bestsalesdf.reset_index().to_json()
    results = json.loads(json_records)
    bestdata = []
    for i in range(len(results["Term"])):
        bestdata.append(str(results["Term"][str(i)]))
    bestdata2 = []
    for j in range(len(results["Last Sale"])):
        bestdata2.append(float(results["Last Sale"][str(j)]))
    print(bestdata2)

    json_records = worstsalesdf.reset_index().to_json(orient='records')
    data2 = []
    data2 = json.loads(json_records) # Worst sales df

    #End of Bar Visualisation



    #Start of WordCloud Visualisation (Plotly)
    
    wordlist = []
    for ind in df.index:
        wordlist.append(df['Country'][ind] + " ")

    Countries = ''.join(wordlist)
    wordcloud = WordCloud().generate(Countries)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)





    return render(request, 'words.html', context = {'best_data' : bestdata, 'best2_data': bestdata2, 'urii': uri} )

  








"""

form = SearchForm()
    return render(request, 'homepage.html', {'form' : form}) # Form is working
"""


"""
def homepage(request):

    form = SearchForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            text = form.cleaned_data['searchtext']  # Search text is found under FOmrs

            print(text)


    form = SearchForm()
    return render(request, 'homepage.html', {'form' : form}) # Form is working
"""
