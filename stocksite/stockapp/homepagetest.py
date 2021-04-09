import pandas as pd
import json

twitter_df = pd.read_csv("stockapp/twitter_dataset.csv")
twitter_df.drop("Unnamed: 0",axis=1, inplace=True)
twitter_df["VADER"].replace({ 0 : "Negative", 1 : "Neutral", 2 : "Positive"}, inplace = True)

twitterVader = []
# What visualisation I wanna add in
twitterTopScore = x.sort_values(by = ['score'], ascending = False).head(3)
for index, rows in x.iterrows():
    for ind,row in twitter_df.iterrows():
        if rows["Text"] == row["Text"] and rows["Query"] == row["Query"]:
            twitterVader.append(row["VADER"])
twitterQueryVader = []
twitterQueryVader.append(twitterVader.count("Negative"))
twitterQueryVader.append(twitterVader.count("Neutral"))
twitterQueryVader.append(twitterVader.count("Positive"))
