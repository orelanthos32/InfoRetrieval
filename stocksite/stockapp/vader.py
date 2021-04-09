import pandas as pd
import json

twitter_df = pd.read_csv("twitter_dataset.csv")
#twitter_df = twitter_df.dropna(axis=0, subset=['Sentiment'])
#twitter_df = twitter_df.dropna(axis=0, subset=['Subjectivity'])
twitter_df.drop("Unnamed: 0",axis=1, inplace=True)
#twitter_df["Sentiment"].replace({ 0.0 : "Negative", 1.0 : "Neutral", 2.0 : "Positive"}, inplace = True)
#twitter_df["Subjectivity"].replace({ 0.0 : "Fact", 1.0 : "Opinion"}, inplace = True)
twitter_df["VADER"].replace({ 0 : "Negative", 1 : "Neutral", 2 : "Positive"}, inplace = True)



#Clening up Reddit Data
reddit_df = pd.read_csv("reddit_dataset.csv")
#reddit_df = reddit_df.dropna(axis=0, subset=['Sentiment'])
#reddit_df = reddit_df.dropna(axis=0, subset=['Subjectivity'])
reddit_df.drop("Unnamed: 0",axis=1, inplace=True)
#sentiment = [0,1, 2]
subjective = [0, 1]
#reddit_df2 = reddit_df[reddit_df['Sentiment'].isin(sentiment)]
#reddit_df = reddit_df[reddit_df['Subjectivity'].isin(subjective)]
#reddit_df["Sentiment"].replace({ 0: "Negative", 1 : "Neutral", 2 : "Positive"}, inplace = True)
#reddit_df["Subjectivity"].replace({ 0 : "Fact", 1 : "Opinion"}, inplace = True)
reddit_df["VADER"].replace({ 0 : "Negative", 1 : "Neutral", 2 : "Positive"}, inplace = True)

twittersub = twitter_df[["VADER"]]
redditsub = reddit_df[["VADER"]]
twitter_reddit_df = twittersub.append(redditsub, ignore_index= True)

#posNeuNegDf =  twitter_reddit_df.groupby(by=["VADER"]).size().rename('count').reset_index()
posneuneg = twitter_reddit_df.groupby(by=["VADER"]).size().rename('count').reset_index()
print()
print("*******REDDIT*****")
print(posneuneg)
