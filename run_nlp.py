import tweepy
import GetOldTweets3 as got
import pandas as pd

from main import tweet_info, clean_tweet
from config import Credentials
from db import extracting_tweets
from data_analysis import clean_transform_data

#Authentication
auth  = tweepy.OAuthHandler(Credentials.API_KEY, \
                            Credentials.API_SECRET_KEY)
auth.set_access_token(Credentials.ACCESS_TOKEN,  \
                      Credentials.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

query = "Rappi"
language = "es"
date_since = "01-09-2020"
date_since_pro = "202009010000"
num_tweets = 200


# tweets = api.search_full_archive(environment_name=fullfileenv, \
#                         q=query, lang=language, \
#                         fromDate=date_since_pro, \
#                         maxResults=num_tweets)

tweets = api.search(q=query, lang=language)
                     
print(tweet.user.screen_name,"Tweeted:",tweet.text)
for tweet in tweets:
    cleaned_text = clean_tweet(tweet.text)
    tweet_info(tweet, cleaned_text, query, table='fulltweetfile')
   # printing the text stored inside the tweet object
    print(tweet.user.screen_name,"Tweeted:",tweet.text)


# df = extracting_tweets()
# print(df)

# result = clean_transform_data(df)
# print(result)

# fd = pnl_module(df)
# print(fd)

# gd = geo_distr_data(df)
# print(gd)

#MAKE THE PLOTt
# plot_results(result[0], result[1], fd, gd) 