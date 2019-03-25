from json import loads
from random import choice

import discord
import tweepy

def get_keys(filename="keys.json"):
    parsed = None
    with open(filename) as keyfile:
        raw = keyfile.read()
        parsed = loads(raw)
    return parsed
   
def get_list(filename="list.txt"):
    clist = []
    with open(filename) as listfile:
        clist = listfile.readlines()
    return clist

keys = get_keys()
people = get_list()

tconsumer = keys["consumer_key"]
tsecret = keys["consumer_secret"]
taccess = keys["access_token"]
tsaccess = keys["access_secret"]
token = keys["discord_token"]

auth = tweepy.OAuthHandler(tconsumer, tsecret)
auth.set_access_token(taccess, tsaccess)
api = tweepy.API(auth)

def get_tweet(person):
    some_tweets = api.user_timeline(screen_name=person, count=200)
    #some_tweets = tweepy.Cursor(api.user_timeline, screen_name=person, count=200, include_entities=True)
    valid_tweets = []
    for tweet in some_tweets:
        if (not 'http' in tweet.text) and (not 'RT' in tweet.text):
            if 'Wendys' in person or not tweet.text.startswith('@'):
                valid_tweets += [[tweet.text, tweet.created_at]]
            
    print(person)
    return choice(valid_tweets)

client = discord.Client()

@client.event
async def on_message(message):
    recv = message.content
    channel = message.channel
    if message.author == client.user:
        pass
    if recv.startswith("!tweet"):
        if recv[7:] is '':
            person = choice(people)
            tweet = get_tweet(person)
            msg = "From {} at {}:\n{}".format(person, tweet[1], tweet[0])
            print("Posting tweet....")
            print("Author: {}".format(person))
            print(tweet[0])
            print("From: {}".format(tweet[1]))
            print("------")
            await client.send_message(channel, content=msg, tts=False)
        else:
            msg = None
            count = 0
            person = recv[7:]
    
            while True:
                count+=1
                tweet = get_tweet(person)
                if not tweet==None:
                    msg = "From {} at {}:\n{}".format(person, tweet[1], tweet[0])
                    print("Posting tweet....")
                    print("Author: {}".format(person))
                    print(tweet[0])
                    print("From: {}".format(tweet[1]))
                    print("------")
                    break
                if count>=10:
                    print("Cannot find acceptable tweet for user {}".format(person))
                    print("------")
                    msg = "Cannot find acceptable tweet. Please try another user."
                    break
            await client.send_message(channel, content=msg, tts=False)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

while True:
    try:
        client.run(token)
    except Exception as e:
        if "Event loop" in str(e):
            print("\nStopping bot....")
            break
        else:
            print(e)
            continue
