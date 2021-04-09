from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
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
from django.urls import reverse
import requests


from .models import Reddit
from .resources import RedditResource
from django.contrib import messages
from tablib import Dataset



# Connecting to the elastic cluster
es2=Elasticsearch([{'host':'localhost','port':9200}])

#Cleaning up Twitter Data
twitter_df = pd.read_csv("stockapp/twitter_dataset.csv")
twitter_df.drop("Unnamed: 0",axis=1, inplace=True)
twitter_df["VADER"].replace({ 0 : "Negative", 1 : "Neutral", 2 : "Positive"}, inplace = True)


#Clening up Reddit Data
reddit_df = pd.read_csv("stockapp/reddit_dataset.csv")
reddit_df.drop("Unnamed: 0",axis=1, inplace=True)
reddit_df["VADER"].replace({ 0 : "Negative", 1 : "Neutral", 2 : "Positive"}, inplace = True)



# Main Page to select source
def sourcepage(request):  

    #load the data

    #Once data has completed indexing 

    form = DataForm()
    form.fields['source'].initial = None
    

    if request.method == "POST":    # Checks if the form was posted
        form = DataForm(request.POST)
    else:
        form = DataForm()
        form.fields['source'].initial = None
    return render(request, 'sourcepage.html', {'form' : form})  # Giving template and data back to the view


# Search Query Page
def homepage(request):  

    reddit_flag = 0
    twitter_flag = 0

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
                query = text
                system = chosenSource
                
                x = do_search(query,system)
                xdisplay = pd.DataFrame()

                twitterVader = []
                twitterTopScore = pd.DataFrame()
                redditTopScore = pd.DataFrame()
                redditVader = []
                RedditQueryVader = [1,1,1]
                twitterQueryVader = [1,1,1]

                
                if system == "twitter":
                    twitter_flag = 1
                    reddit_flag = 0
                    xdisplay = x[["Tweet of: twitter", "tweet", "score"]]

                    twitterTopScore = x[["Tweet of: twitter", "tweet", "score"]].sort_values(by = ['score'], ascending = False).head(3)
                    for index, rows in x.iterrows():
                        twitterVader.append(rows["vader"])
                    twitterQueryVader.clear()
                    twitterQueryVader.append(twitterVader.count(0))
                    twitterQueryVader.append(twitterVader.count(1))
                    twitterQueryVader.append(twitterVader.count(2))


                if system == "reddit":
                    reddit_flag = 1
                    twitter_flag = 0
                    xdisplay = x[["Tweet of: reddit", "tweet", "score"]]

                    redditTopScore = x[["Tweet of: reddit", "tweet", "score"]].sort_values(by = ['score'], ascending = False).head(3)
                    for index, rows in x.iterrows():
                        redditVader.append(rows["vader"])
                    RedditQueryVader.clear()
                    RedditQueryVader.append(redditVader.count(0))
                    RedditQueryVader.append(redditVader.count(1))
                    RedditQueryVader.append(redditVader.count(2))


            return render(request, 'homepage.html', { 'source' : chosenSource ,'query' : text ,'form': form, 'form2': form2, 'result' : xdisplay.to_html(),
             'redditflag': reddit_flag, 'twitterflag': twitter_flag,
             'redditScore' : redditTopScore.to_html(),'twitterScore' : twitterTopScore.to_html(),
             'redditVaders' : RedditQueryVader, 'twitterVader' : twitterQueryVader}) 
        else:
            form = SearchForm()

    return HttpResponseRedirect(reverse(sourcepage))
               
  #  return render(request, 'homepage.html', {'form' : form, 'form2' : form2})
    # TO view in html, use the left side of the dict

# Search query function (Start)
def search(text,system):
    result_list = []
    intent_list = []
    word_list = []
    vader_list = []
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

    for hit in response.json()['hits']['hits']:
        score = hit['_score']
        result_list.append(score)
        intent = hit["_source"]["intent"]
        intent_list.append(intent)
        word = hit["_source"]["text"]
        word_list.append(word)
        vader = hit["_source"]["vader"]
        vader_list.append(vader)

    return intent_list,word_list,result_list,vader_list

def do_search(text,system):
    x, y,z,w = search(text, system)
    rdf = pd.DataFrame(list(zip(x, y,z,w)), 
               columns =['Tweet of: '+system,'tweet', 'score','vader'])
    return rdf
# Search query function (End)

# Just tryuing
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

def Diagram(dataframe, datalist, datalistcol1, datalist2, datalistcol2):
        json_records = dataframe.reset_index().to_json()
        results = json.loads(json_records)
        for i in range(len(results[datalistcol1])):
            datalist.append(str(results[datalistcol1][str(i)]))
        for j in range(len(results[datalistcol2])):
            datalist2.append(float(results[datalistcol2][str(j)]))

def transformColumn(s,col, type):
        if col == 'Last Sale':
            s[col] = s[col].str.replace('$', '')
        if col == '% Change':
            s[col] = s[col].str.replace('%', '')
        s[col] = s[col].astype(type)

# View for 'Stat Comparison'
def comparison(request):

    reddit_stats_df = pd.read_csv("stockapp/RedditStonks.csv")
    twitter_stats_df = pd.read_csv("stockapp/stockticker10-tweets(5-3-21) label.csv")
    

    transformColumn(reddit_stats_df, 'Last Sale', float)
    transformColumn(reddit_stats_df, 'Term', 'str')
    transformColumn(reddit_stats_df, 'Country', str)
    transformColumn(reddit_stats_df, '% Change', float)

    

    #Start of bar Visualisation ( Chart.js)
    # Best and Worst Last Sale
    bestsalesdf = reddit_stats_df.sort_values(by = 'Last Sale', ascending = False)
    bestsalesdf = bestsalesdf[["Term", "Last Sale"]]
    bestsalesdf = bestsalesdf.head(10)
    bestdata = []
    bestdata2 = []
    Diagram(bestsalesdf,bestdata, "Term", bestdata2, "Last Sale")

   # json_records = bestsalesdf.reset_index().to_json()
    #results = json.loads(json_records)
    #bestdata = []
    #for i in range(len(results["Term"])):
     #   bestdata.append(str(results["Term"][str(i)]))
    #bestdata2 = []
    #for j in range(len(results["Last Sale"])):
    #    bestdata2.append(float(results["Last Sale"][str(j)]))
    #print(bestdata2)



    worstsalesdf = reddit_stats_df.sort_values(by = 'Last Sale', ascending = True)
    worstsalesdf = worstsalesdf[["Term", "Last Sale"]]
    worstsalesdf = worstsalesdf.head(10)

    worstdata = []
    worstdata2 = []
    Diagram(worstsalesdf,worstdata, "Term", worstdata2, "Last Sale")







    # Bets and Worst Net Change
    bestnetchange = reddit_stats_df.sort_values(by = '% Change', ascending = False)
    bestnetchange = bestnetchange.head(10)
    
    json_records = bestnetchange.reset_index().to_json()
    results = json.loads(json_records)
    bestnetdata = []
    for i in range(len(results["Term"])):
        bestnetdata.append(str(results["Term"][str(i)]))
    bestnetdata2 = []
    for j in range(len(results["% Change"])):
        bestnetdata2.append(float(results["% Change"][str(j)]))



    worstnetchange = reddit_stats_df.sort_values(by = '% Change', ascending = True)
    worstnetchange = worstnetchange.head(10)

    json_records = worstnetchange.reset_index().to_json()
    results = json.loads(json_records)
    worstnetdata = []
    for i in range(len(results["Term"])):
        worstnetdata.append(str(results["Term"][str(i)]))
    worstnetdata2 = []
    for j in range(len(results["% Change"])):
        worstnetdata2.append(float(results["% Change"][str(j)]))


    # Diagram to display Best and WorstVolume
    bestStockVolume = reddit_stats_df.sort_values(by = 'Volume', ascending = False)
    bestStockVolume = bestStockVolume.head(10)
    bestStockVolumeData = []
    bestStockVolumeData2 = []
    Diagram(bestStockVolume,bestStockVolumeData, "Term", bestStockVolumeData2, "Volume")

    worstStockVolume = reddit_stats_df.sort_values(by = 'Volume', ascending = True)
    worstStockVolume = worstStockVolume.head(10)
    worstStockVolumeData = []
    worstStockVolumeData2 = []
    Diagram(worstStockVolume,worstStockVolumeData, "Term", worstStockVolumeData2, "Volume")



    #Twitter:
    # Top Username for RT Count and Fav Count
    # 

    #Start of WordCloud Visualisation (Plotly)
    """
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

    'urii': uri}
    """



    ##################################################
    #Twitter
    twitter_stats_df = pd.read_csv("stockapp/stockticker10-tweets(5-3-21) label.csv")
    twitter_stats_df = twitter_stats_df[["Query","Text", "Username", "RT Count", "Fav Count"]]

    #Based on Fav tweets
    mostfavtwt = twitter_stats_df.sort_values(by=['Fav Count'], ascending = False)
    mostfavtwt = mostfavtwt.head(10)
    mostfavusernames = mostfavtwt.groupby(by=["Username"]).size().rename('count').reset_index().sort_values(by = ['count'], ascending = False)
    mostfavtwt = mostfavtwt.reset_index(drop=True)

    #Based on RT Tweets
    mostrttwt = twitter_stats_df.sort_values(by=['RT Count'], ascending = False)
    mostrttwt = mostrttwt.head(10)
    mostrtusernames = mostrttwt.groupby(by=["Username"]).size().rename('count').reset_index().sort_values(by = ['count'], ascending = False)
    mostrttwt = mostrttwt.reset_index(drop=True)

    trustedUsers = twitter_stats_df.sort_values(by=['Query','RT Count'], ascending = False)
    trustedUsers = trustedUsers.drop_duplicates(['Query', 'Username']).groupby('Query').head(3)
    trustedUsers = trustedUsers.reset_index(drop=True)
    trustedUsers = trustedUsers.groupby("Query")['Username'].apply(lambda tags: ', '.join(tags)).to_frame()


    return render(request, 'comparison.html', context = {'best_data' : bestdata, 'best2_data': bestdata2, 'worst_data' : worstdata, 'worst2_data': worstdata2, 
    'bestnet_data' : bestnetdata, 'bestnet2_data' : bestnetdata2, 'worstnet_data' : worstnetdata, 'worstnet2_data' : worstnetdata2,
    'mostfavtwtTable' : mostfavtwt.to_html(), 'mostrttwtTable' : mostrttwt.to_html(),
    'bestvolterm': bestStockVolumeData, 'bestvoldata' : bestStockVolumeData2,
    'worstvolterm': worstStockVolumeData, 'worstvoldata': worstStockVolumeData2, 'twitterTrustedUsers' : trustedUsers.to_html()} )


def sentimentanalysis(request):


    #Seniment Analysis
    # For Sentiment: 2 Positive, 1 Neutral, 0 Negative
    # For Subjectivity: 1 Opinion, 0 Fact
    twitter_dfs = twitter_df
    twitter_dfs = twitter_dfs.dropna(axis=0, subset=['Sentiment'])
    twitter_dfs = twitter_dfs.dropna(axis=0, subset=['Subjectivity'])
    twitter_dfs["Sentiment"].replace({ 0.0 : "Negative", 1.0 : "Neutral", 2.0 : "Positive"}, inplace = True)
    twitter_dfs["Subjectivity"].replace({ 0.0 : "Fact", 1.0 : "Opinion"}, inplace = True)
 

    #reddit_df = reddit_df.dropna(axis=0, subset=['Sentiment'])
    reddit_dfs = reddit_df
    reddit_dfs = reddit_dfs.dropna(axis=0, subset=['Subjectivity'])
    sentiment = [0,1, 2]
    subjective = [0, 1]
    reddit_dfs2 = reddit_dfs[reddit_dfs['Sentiment'].isin(sentiment)]
    reddit_dfs = reddit_dfs2[reddit_dfs2['Subjectivity'].isin(subjective)]
    reddit_dfs["Sentiment"].replace({ 0: "Negative", 1 : "Neutral", 2 : "Positive"}, inplace = True)
    reddit_dfs["Subjectivity"].replace({ 0 : "Fact", 1 : "Opinion"}, inplace = True)


   # Concating both Twitter and Reddit Sentiment Analysis
    twittersub = twitter_df[["VADER"]]
    redditsub = reddit_df[["VADER"]]
    twitter_reddit_df = twittersub.append(redditsub, ignore_index= True)
    twittersub2 = twitter_dfs[["Sentiment", "Subjectivity"]]
    redditsub2 = reddit_dfs[["Sentiment", "Subjectivity"]]
    twitter_reddit_dfs = twittersub2.append(redditsub2, ignore_index= True)

    #based on SUBJECTIVITY


    # Different types of dataframe for different uses
    # Need to check the first 2
    opinionFactDf = twitter_reddit_dfs.groupby(by=["Subjectivity"]).size().rename('count').reset_index()
    categorisedDf = twitter_reddit_dfs.groupby(["Subjectivity", "Sentiment"]).size().rename('count').reset_index()
    posNeuNegDf =  twitter_reddit_df.groupby(by=["VADER"]).size().rename('count').reset_index()
    

    # For the Positive, Neutral and Negative Labels
    # For Positive, Neutral and Negative Diagram  (Polarity Visuaisation)
    negativeData = posNeuNegDf["count"].iloc[0]
    neutralData = posNeuNegDf["count"].iloc[1]
    positiveData = posNeuNegDf["count"].iloc[2]
    countData = []  
    countData2 = []
    Diagram(posNeuNegDf,countData, "VADER", countData2, "count")
    twitter_data = twittersub.groupby(by=["VADER"]).size().rename('count').reset_index()
    reddit_data = redditsub.groupby(by=["VADER"]).size().rename('count').reset_index()
    twitter_posneuneg = []
    reddit_posneuneg = []
    
    for index,rows in twitter_data.iterrows():
        twitter_posneuneg.append(float(rows['count']))
    for index,rows in reddit_data.iterrows():
        reddit_posneuneg.append(float(rows['count']))
    

    # For Opinions vs Facts Diagram
    subjectiveLabels = []
    SubjectiveCount = []
    Diagram(opinionFactDf,subjectiveLabels, "Subjectivity", SubjectiveCount, "count")


    # For facts only
    # No. of positive
   # json_records = categorisedDf.reset_index().to_json()
    #results = json.loads(json_records)
    factLabel = []
    factData = []
    for index,rows in categorisedDf.iterrows():
        if rows["Subjectivity"] == "Fact":
            factLabel.append(str(rows["Sentiment"]))
            factData.append(int(rows["count"]))
    
    #for i in range(len(results["Sentiment"])):
     #   if results["Subjectivity"][str(i)] == "Fact":
        #    factLabel.append(str(results["Sentiment"][str(i)]))
         #   factData.append(str(results["count"][str(i)]))

    # For opinions only
    opinionLabel = []
    opinionData = []
    for index,rows in categorisedDf.iterrows():
        if rows["Subjectivity"] == "Opinion":
            opinionLabel.append(str(rows["Sentiment"]))
            opinionData.append(int(rows["count"]))

    # Can re use the same data to make pies/bars




    # totalCountData, totalCountData2, positive, neutral, negative, opionated, facts
    return render(request, 'sentimentanalysis.html', context = {'totalCountData' : countData, 'totalCountData2': countData2, 'positive': positiveData, 'neutral':  neutralData, 'negative' : negativeData,
    'twitter_data' : twitter_posneuneg, 'reddit_data': reddit_posneuneg,
    'subLabels': subjectiveLabels, 'subCounts' : SubjectiveCount,
    'factLabels' : factLabel, "factDatas" : factData, "opinionLabels" : opinionLabel, "opinionDatas" : opinionData })

     
# always cover at least subjectivity detection and polarity detection
# first categorise data as neutral vs opinionated then classify the resulting poinionated data as potive versus negative

# Twitter Api



def testing(request):

    # Putting csv into a model
  #s  Twitter_df = pd.read_csv("stockapp/stockticker10-tweets(5-3-21) label.csv")

    reddit_resource = RedditResource()
    dataset = Dataset()
    imported_data = pd.read_csv("stockapp/MAIN_reddit.csv")
    imported_data.insert(0,'id','')
    imported_data.drop("Unnamed: 7",axis=1, inplace=True)
    imported_data.drop("Unnamed: 8",axis=1, inplace=True)
    imported_data.drop("Unnamed: 9",axis=1, inplace=True)
    
    imported_data.to_csv(r'C:\Users\munir\OneDrive\Desktop\NTU Y3S2\IR\Assignment\stocksite\stockapp\reddit.csv', index=False)
   
    with open('stockapp/reddit.csv', 'r',encoding="utf8") as fh:
        imported_data = dataset.load(fh)

    result = reddit_resource.import_data(imported_data, dry_run = True)
   
   
    
    if not result.has_errors():
        reddit_resource.import_data(imported_data, dry_run = False)
        complete = "Load Complete!"
        print(result.errors)
    else:
        complete = " Not Load Complete!"
    # for index, row in imported_data.iterrows():
     
     #  value = Reddit(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
      #  value.save() 

    
    return render(request, "testing.html", context = {"complete" : complete})
