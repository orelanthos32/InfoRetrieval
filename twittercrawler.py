import tweepy
import pandas as pd
import time

# Credentials

consumer_key="PM"
consumer_secret="ME"
access_token="FOR"
access_token_secret="KEY"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

#900 request every 15mins, will sleep eitherwise

tweets = []
tweets_list = []

def text_query_to_csv(text_query,count):
    try:
        # Creation of query method using parameters , mixed/recent/popular
        tweets = tweepy.Cursor(api.search,q=text_query,lang='en',result_type='recent',tweet_mode='extended').items(count)

        # Pulling information from tweets iterable object for retweet and normal tweet full text
        for tweet in tweets:
            print("G")
            try:
                tweets_list.append([text_query, tweet.created_at, tweet.id, tweet.retweeted_status.full_text, tweet.user.screen_name , "Y", tweet.retweet_count,tweet.favorite_count])
            except AttributeError:
                tweets_list.append([text_query, tweet.created_at, tweet.id, tweet.full_text, tweet.user.screen_name, "N", tweet.retweet_count,tweet.favorite_count])

    except BaseException as e:
        print('failed on_status,',str(e))
        time.sleep(1)

if __name__ == "__main__":
    text_list = ['$GME','$FB','$GOOG','$AMC','$RKT','$PLTR','$TSLA','$AMZN','$UWMC','$AAPL']
    count = 1000
    for text_query in text_list:
        text_query_to_csv(text_query, count)
        print(text_query,"done")

    # Creation of dataframe from tweets list
    # Add or remove columns as you remove tweet information
    tweets_df = pd.DataFrame(tweets_list,columns=['Query', 'Datetime(UTC)', 'Tweet ID', 'Text', 'Username','RT','RT Count','Fav Count'])

    # Converting dataframe to CSV 
    tweets_df.to_csv('{}-tweets.csv'.format("stockticker10"), sep=',', index = False)

