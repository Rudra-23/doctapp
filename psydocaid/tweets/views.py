from django.http.response import HttpResponse
from django.shortcuts import render

# fetching tweets
'''
import re
import tweepy
import json
import sys

from textblob import TextBlob

ttopic = ["python"]


def clean_tweet(self, tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) \|(\w+:\/\/\S+)", " ", tweet).split())


def deEmojify(text):
    if text:
        return text.encode('ascii', 'ignore').decode('ascii')
    else:
        return None

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        if status.retweeted:
            return True

        id_str = status.id_str
        created_at = status.created_at
        text = deEmojify(status.text)    # Pre-processing the text
        sentiment = TextBlob(text).sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity

        user_created_at = status.user.created_at
        user_location = deEmojify(status.user.location)
        user_description = deEmojify(status.user.description)
        user_followers_count = status.user.followers_count
        longitude = None
        latitude = None
        if status.coordinates:
            longitude = status.coordinates['coordinates'][0]
            latitude = status.coordinates['coordinates'][1]

        retweet_count = status.retweet_count
        favorite_count = status.favorite_count

        print('*'*30)
        
        print("idstr=", id_str)
        print("created_at=", created_at)
        print("text=", text)
        print("polarity=",polarity)
        print("subjectivity=", subjectivity)
        print("user_created_at=", user_created_at)
       # print("user_location=", user_location, "user_description=", user_description,"user_followers_count=", user_followers_count, longitude, latitude, retweet_count, favorite_count)
        print("*"*30) 
        

    def on_error(self, status_code):
        if status_code == 420:
            return False



def fetch():
    auth = tweepy.OAuthHandler("YBG8fQiOBIlN5vT1e59TQMXX6",
                               "nMO8kCaGFasW8PbqIXpwHA7Kq2snRpZlIxOCgibx18rBTgQT6L")  # api key,secret key

    auth.set_access_token("1135195310429523968-nSIULH9Qd00P1aToYjOlcXXGRTuiKr",
                      "syy1Xn9fn4wUbYoiujWZyL6zM8tfQ00UIOXTKvFDha5kh")  # acces_token,acess_token_secret
    api = tweepy.API(auth)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(languages=["en"], track=ttopic)
'''


import tweepy
import re
import os
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

import environ
env = environ.Env()
environ.Env.read_env()



def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) \|(\w+:\/\/\S+)", " ", tweet).split())


def deEmojify(text):
    if text:
        return text.encode('ascii', 'ignore').decode('ascii')
    else:
        return None

def fetch(userID):
    consumer_key = os.environ.get('consumer_key')
    consumer_key_secret = os.environ.get('consumer_key_secret')
    access_token = os.environ.get('access_token')
    access_token_secret = os.environ.get('access_token_secret')
    auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweets = api.user_timeline(screen_name=userID,count=10, include_rts=False, tweet_mode='extended')

    arr =[]
    pos = 0
    neg = 0
    for tweet in tweets:
        
        #print(tweet.full_text)
        clean = tweet.full_text
        clean = deEmojify(clean)
        clean = clean_tweet(clean)
        blob_object = TextBlob(clean, analyzer=NaiveBayesAnalyzer())
        analysis = blob_object.sentiment
        # sentiment = TextBlob(clean).sentiment
        # polarity = sentiment.polarity
        # subjectivity = sentiment.subjectivity
        if analysis.classification =='pos':
            pos+=1
        else:
            neg+=1
        arr.append([tweet.full_text,analysis.classification])
        
    
    return [arr,[pos,neg]]


def index(request):
    [arr, [pos, neg]] = fetch('MrBeast') # your name 
    return render(request,'tweets/index.html',{'arr':arr,'pos':pos,'neg':neg,'total':pos+neg})
