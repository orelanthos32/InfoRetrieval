import pandas as pd
import json

twitter_stats_df = pd.read_csv("stockticker10-tweets(5-3-21) label.csv")
twitter_stats_df = twitter_stats_df[["Query","Text", "Username", "RT Count", "Fav Count"]]

#Based on Fav tweets
mostfavtwt = twitter_stats_df.sort_values(by=['Fav Count'], ascending = False)
mostfavtwt = mostfavtwt.head(10)
mostfavtwt = mostfavtwt.reset_index(drop=True)
mostfavusernames = mostfavtwt.groupby(by=["Username"]).size().rename('count').reset_index().sort_values(by = ['count'], ascending = False)
mostfavusernames = mostfavusernames.reset_index(drop=True)

#print(mostfavusernames)

#for index, rows in mostfavusernames.iterrows():
 #   if index < 3:
   #     print(rows["Username"])

mostrttwt = twitter_stats_df.sort_values(by=['RT Count','Fav Count'], ascending = False)
mostrttwt = mostrttwt.head(10)
mostrttwt = mostrttwt.reset_index(drop=True)
mostrtusernames = mostrttwt.groupby(by=["Username"]).size().rename('count').reset_index().sort_values(by = ['count'], ascending = False)
mostrtusernames = mostrtusernames.reset_index(drop=True)


test = twitter_stats_df.sort_values(by=['Query','RT Count'], ascending = False)
test = test.drop_duplicates(['Query', 'Username']).groupby('Query').head(3)
test = test.reset_index(drop=True)
print(test)

print(test.groupby("Query")['Username'].apply(lambda tags: ', '.join(tags)).to_frame().to_html())

for i in range(len(test["Query"].unique())):
    print(test["Query"].unique()[i])

# Prints out the query and the most relevant username
for i in test["Query"].unique():
    print("")
    print(i)
    for index,rows in test.iterrows():
        if rows["Query"] == i:
            print(rows["Username"])
        
    







