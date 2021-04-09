import pandas as pd
import json

#Cleaning up Twitter Data
twitter_df = pd.read_csv("twitter_dataset.csv")
twitter_df = twitter_df.rename(columns={"Sentiment (2pos/1neu/0neg)": "Sentiment", "Subjectivity (1opinion/0fact)": "Subjectivity"})
twitter_df = twitter_df.dropna(axis=0, subset=['Sentiment'])
twitter_df = twitter_df.dropna(axis=0, subset=['Subjectivity'])
twitter_df.drop("Unnamed: 0",axis=1, inplace=True)
twitter_df["Sentiment"].replace({ 0.0 : "Negative", 1.0 : "Neutral", 2.0 : "Positive"}, inplace = True)
twitter_df["Subjectivity"].replace({ 0.0 : "Fact", 1.0 : "Opinion"}, inplace = True)


#Clening up Reddit Data
reddit_df = pd.read_csv("reddit_dataset.csv")
reddit_df = reddit_df.dropna(axis=0, subset=['Sentiment'])
reddit_df = reddit_df.dropna(axis=0, subset=['Subjectivity'])
reddit_df.drop("Unnamed: 0",axis=1, inplace=True)
sentiment = [0,1, 2]
subjective = [0, 1]
reddit_df2 = reddit_df[reddit_df['Sentiment'].isin(sentiment)]
reddit_df3 = reddit_df2[reddit_df2['Subjectivity'].isin(subjective)]
reddit_df3["Sentiment"].replace({ 0 : "Negative", 1 : "Neutral", 2 : "Positive"}, inplace = True)
reddit_df3["Subjectivity"].replace({ 0 : "Fact", 1 : "Opinion"}, inplace = True)

# Concating both Twitter and Reddit Sentiment Analysis
twittersub = twitter_df[["Sentiment", "Subjectivity"]]
redditsub = reddit_df3[["Sentiment","Subjectivity"]]
twitter_reddit_df = twittersub.append(redditsub, ignore_index= True)

# twitter_reddit_df["Sentiment"].replace({ 0.0 : "Negative", 1.0 : "Neutral", 2.0 : "Positive"}, inplace = True) 
#twitter_reddit_df["Subjectivity"].replace({ 0.0 : "Fact", 1.0 : "Opinion"}, inplace = True)

# Different types of dataframe for different uses
opinionFactDf = twitter_reddit_df.groupby(by=["Subjectivity"]).size().rename('count').reset_index()
categorisedDf = twitter_reddit_df.groupby(["Subjectivity", "Sentiment"]).size().rename('count').reset_index()
posNeuNegDf = twitter_reddit_df.groupby(by=["Sentiment"]).size().rename('count').reset_index()

print(categorisedDf)
