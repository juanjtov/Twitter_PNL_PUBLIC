import tweepy
import pandas as pd
from textblob import TextBlob
import re

from db_tech import storage, extracting_tweets
from config import Credentials, Settings
from data_analysis import clean_transform_data, plot_results, pnl_module, geo_distr_data


#Authentication
auth  = tweepy.OAuthHandler(Credentials.API_KEY, \
                            Credentials.API_SECRET_KEY)
auth.set_access_token(Credentials.ACCESS_TOKEN,  \
                      Credentials.ACCESS_TOKEN_SECRET)

#CREATE THE API OBJECT
api = tweepy.API(auth)

#CREATE DATABASE TABLES
#FIRST EXECUTE DB.PY

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        
        # if status.retweeted:
        # # Avoid retweeted info, and only original tweets will 
        # # be received
        #     return True

        # Clean The text
        text = deEmojify(status.text)
        cleaned_text = clean_tweet(text)
        print(cleaned_text)
        tweet_info(status, cleaned_text, word=Settings.TRACK_WORDS, table=Settings.TABLE_NAME)

      
    def on_error(self, status_code):
        '''
        Since Twitter API has rate limits, 
        stop scraping data as it exceed to the thresold.
        '''
        if status_code == 420:
            # return False to disconnect the stream
            return False


def tweet_info(status, cleaned_text, word, table):
    '''
    Extract all the information from the streamed tweet
    '''
    tweet_dict = {}
    tweet_dict['tracked_word'] = word
    tweet_dict['id_tweet'] = status.id_str
    tweet_dict['created_at'] = status.created_at
    tweet_dict['cleaned_tweet'] = cleaned_text
    tweet_dict['user_created_at'] = status.user.created_at

    #SENTIMENT ANALYSIS
    tweet_dict['sentiment'] = TextBlob(cleaned_text).sentiment
    tweet_dict['polarity'] = tweet_dict['sentiment'].polarity
    tweet_dict['subjectivity'] = tweet_dict['sentiment'].subjectivity

    tweet_dict['user_created_at'] = status.user.created_at
    tweet_dict['user_location'] = deEmojify(status.user.location)
    tweet_dict['user_description'] = deEmojify(status.user.description)
    tweet_dict['user_followers_count'] =status.user.followers_count
    
    tweet_dict['longitude'] = None
    tweet_dict['latitude'] = None

    if status.coordinates:
        tweet_dict['longitude'] = status.coordinates['coordinates'][0]
        tweet_dict['latitude'] = status.coordinates['coordinates'][1]

    tweet_dict['retweet_count'] = status.retweet_count
    tweet_dict['favorite_count'] = status.favorite_count

    print(tweet_dict)
    storage(table, tweet_dict['tracked_word'], tweet_dict['id_tweet'], \
            tweet_dict['created_at'], \
            tweet_dict['cleaned_tweet'], tweet_dict['polarity'], \
            tweet_dict['subjectivity'], tweet_dict['user_created_at'],\
            tweet_dict['user_location'], tweet_dict['user_description'], \
            tweet_dict['user_followers_count'], tweet_dict['longitude'], \
            tweet_dict['latitude'], tweet_dict['retweet_count'], \
            tweet_dict['favorite_count'])

    return 'ok'

#preprocessing text
def deEmojify(text):
    '''
    Strip all non-ASCII characters to remove emoji characters
    '''
    if text:
        return text.encode('ascii', 'ignore').decode('ascii')
    else:
        return None

def clean_tweet(tweet): 
    ''' 
    Use sumple regex statemnents to clean tweet text by removing links and special characters
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) \
                                |(\w+:\/\/\S+)", " ", tweet).split()) 



#CREATE THE STREAM LISTENER
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)
myStream.filter(languages=['en'], track = [Settings.TRACK_WORDS], is_async=True)


