import tweepy
#import discord
from lib import *
from random import choice
from json import dumps

keys = get_keys()
#people = get_list()

tconsumer = keys["consumer_key"]
tsecret = keys["consumer_secret"]
taccess = keys["access_token"]
tsaccess = keys["access_secret"]

auth = tweepy.OAuthHandler(tconsumer, tsecret)
auth.set_access_token(taccess, tsaccess)
api = tweepy.API(auth)

def get_tweet(person):
    some_tweets = api.user_timeline(screen_name=person, count=200)
    valid_tweets = []
    for tweet in some_tweets:
        if (not 'http' in tweet.text) and (not 'RT' in tweet.text):
            valid_tweets += [tweet.text]
            
    return choice(valid_tweets)
    
print(get_tweet('officialjaden'))
