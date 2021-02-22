"""Retrieve tweets and users then create embeddings and populate DB"""

import os
from os import getenv 
import pdb 
import flask
import flask_sqlalchemy
import tweepy
import spacy 
import dotenv 
from .models import DB, Tweet, User
#from dotenv import load_dotenv

TWITTER_API_KEY = getenv("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = getenv("TWITTER_API_KEY_SECRET")
#ToDo - Don't have raw secrets in our code (make .env file)  
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET) 
TWITTER = tweepy.API(TWITTER_AUTH)

#nlp model
path = os.path.join('/'.join(os.path.realpath(__file__).split('/')[:-2]), 'my_model')
nlp = spacy.load(path) 

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector 

def add_or_update_user(username): 
    try: 
        twitter_user = TWITTER.get_user(username) #grabs user from twitter db^
        #adds or updates user
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, name=username)
        DB.session.add(db_user)

        #grabs tweets from twitter_user
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False, 
            tweet_mode="extended"
        )

        #adds newest tweet to db_user.newest tweet_id
        if tweets:
            db_user.newest_tweet_id = tweets[0].id


        for tweet in tweets: 
            #stores numerical representations
            vectorized_tweet = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text, vect=vectorized_tweet) #iterating over our users and tweets
            db_user.tweets.append(db_tweet) #going to the database and pulling out that particular id and pulling the tweets for that id and then going back to the user and assigning those tweets to the user on our end. #https://www.youtube.com/watch?v=xAAgrHm_EYQ&feature=youtu.be&ab_channel=LambdaSchool if ref needed. 1h.15m in. 
            DB.session.add(db_tweet)
            
    except Exception as e:
        #prints error to user and raises throughout app
        print('Error processing(): ()'.format(username, e))
        raise e 

    #commits changes after try has completed:
    else: 
        DB.session.commit()

def update_all_users():
    """Update all tweets for all users in the user table."""
    for user in User.query.all():
        add_or_update_user(user.name) 



    


     