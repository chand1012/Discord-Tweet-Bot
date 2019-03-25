import tweepy
import discord
from lib import get_keys, get_list
from random import choice
from json import dumps

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
    valid_tweets = []
    for tweet in some_tweets:
        if (not 'http' in tweet.text) and (not 'RT' in tweet.text) and (not '@' in tweet.text):
            valid_tweets += [tweet.text]
            
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
            msg = "From {}:\n{}".format(person, tweet)
            print("Posting tweet....")
            print("Author: {}".format(person))
            print(tweet)
            print("------")
            await client.send_message(channel, content=msg, tts=True)
        else:
            msg = None
            count = 0
            person = recv[7:]
    
            while True:
                count+=1
                tweet = get_tweet(person)
                if not tweet==None:
                    msg = "From {}:\n{}".format(person, tweet)
                    break
                if count>=10:
                    print("Cannot find acceptable tweet for user {}".format(person))
                    print("------")
                    msg = "Cannot find acceptable tweet. Please try another user."
                    break
            await client.send_message(channel, content=msg, tts=True)

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