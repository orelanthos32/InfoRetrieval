# ABOUT ####
# The script uses pushshift, a big-data storage and analytics project.
# Pushshift has archived past data from Reddit and is open-sourced and free to use.
# https://github.com/pushshift
# https://pushshift.io/api-parameters/
# Unfortunately Reddits own API, PRAW, limits the number of post you can get from the current time of the request,
# making large data pulls impossible with this method. Reddit has since removed "submissions" endpoint,
# which previously allowed to query for posts at certain timestamps.
import requests
from datetime import datetime
import traceback
import time
import json
import sys
import pandas as pd

username = ""  # put the username you want to download in the quotes
subreddit = "wallstreetbets"  # put the subreddit you want to download in the quotes
# leave either one blank to download an entire user's or subreddit's history
# or fill in both to download a specific users history from a specific subreddit

filter_string = None
if username == "" and subreddit == "":
    print("Fill in either username or subreddit")
    sys.exit(0)
elif username == "" and subreddit != "":
    filter_string = f"subreddit={subreddit}"
elif username != "" and subreddit == "":
    filter_string = f"author={username}"
else:
    filter_string = f"author={username}&subreddit={subreddit}"

# EDIT TICKER NAME BELOW
url = "https://api.pushshift.io/reddit/{}/search?q=gme&limit=1000&sort=desc&{}&before="
# The plan was to exe invididual csvs of each ticker (to be able to label them)
# and sitch them together in a master csv

# We call the invidividual ticker names by editing the query above
# do all individually then string tgt in a csv
# where "q=<insert ticker name>"

# you may query multiple ticker names at a time but identifying the ticker names from post will be harder
# "q=gme|nvda|goog|googl|amc|rkt|pltr|tsla|amzn|uwmc|appl"

start_time = datetime.utcnow()  # appends at the end of the url

TARGET = 2  # change the target to decide how much data to generate for the query
# e.g. 10 = search through past 1000 reddit submissions
# (note this is before flitering), so it is usually ~ 500 hit results
def downloadFromUrl(filename, object_type):
    print(f"Saving {object_type}s to {filename}")

    target_posts = []
    count = 0
    stop = 0
    handle = open(filename, "w")
    previous_epoch = int(start_time.timestamp())
    while stop < TARGET:
        stop += 1
        new_url = url.format(object_type, filter_string) + str(previous_epoch)
        json_text = requests.get(new_url, headers={"User-Agent": "Post downloader"})
        time.sleep(
            1
        )  # pushshift has a rate limit, if we send requests too fast it will start returning error messages
        try:
            json_data = json_text.json()
        except json.decoder.JSONDecodeError:
            time.sleep(1)
            continue

        if "data" not in json_data:
            break
        objects = json_data["data"]
        if len(objects) == 0:
            break

        for object in objects:
            previous_epoch = object["created_utc"] - 1
            count += 1
            if object_type == "comment":
                try:
                    handle.write(str(object["score"]))
                    handle.write(" : ")
                    handle.write(
                        datetime.fromtimestamp(object["created_utc"]).strftime(
                            "%Y-%m-%d %h:%m:%s"
                        )
                    )
                    handle.write("\n")
                    handle.write(
                        object["body"]
                        .encode(encoding="ascii", errors="ignore")
                        .decode()
                    )
                    handle.write("\n-------------------------------\n")
                except Exception as err:
                    print(
                        f"Couldn't print comment: https://www.reddit.com{object['permalink']}"
                    )
                    print(traceback.format_exc())
            elif object_type == "submission":
                if object["is_self"]:
                    if "selftext" not in object:
                        continue
                    try:
                        created_at = datetime.fromtimestamp(
                            object["created_utc"]
                        ).strftime("%Y-%m-%d %h:%m:%s")
                        title = object["title"]
                        text = (
                            object["selftext"]
                            .encode(encoding="ascii", errors="ignore")
                            .decode()
                        )
                        score = str(object["score"])
                        # upvote_ratio = object['upvote_ratio']
                        # total_awards_received = object['total_awards_received']
                        # the_url = object['url']
                        target_posts.append([created_at, title, text, score])
                    except Exception as err:
                        print(f"Couldn't print post: {object['url']}")
                        print(traceback.format_exc())

        print(
            "Saved {} {}s through {}".format(
                count,
                object_type,
                datetime.fromtimestamp(previous_epoch).strftime("%Y-%m-%d"),
            )
        )

    target_posts_df = pd.DataFrame(
        target_posts, columns=["created_at", "title", "text", "score"]
    )
    filename = "reddit_scrapper_ticker" + str(int(time.time())) + ".csv"
    print(f"Saving to file {filename}")
    target_posts_df.to_csv(filename, index=False)


downloadFromUrl("posts.txt", "submission")
# downloadFromUrl("comments.txt", "comment")
