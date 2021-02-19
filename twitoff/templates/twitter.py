"""Retrieve tweets and users then create embeddings and populate DB"""
import flask
import flask_sqlalchemy
import tweepy
import spacy 
from .models import DB, Tweet, User

#ToDo - Don't have raw secrets in our code (make .env file) 
TWITTER_API_KEY = "H6Kdts6pmXuQ0QCyk2U3Nkf7k"
TWITTER_API_KEY_SECRET = "9VFblJEam7U1wqKzuxfihZNJfxsSZVDNXNkNUKWOpVubTv71Oh" 
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET) 
TWITTER = tweepy.API(TWITTER_AUTH)

def add_or_update_user(username): 
    twitter_user = TWITTER.get_user(username)
    db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, name=username)
    DB.session.add(db_user)

    tweets = twitter_user.timeline(
        count=200, exclude_replies=True, include_rts=False, 
        tweet_mode="extended"
    )

    for tweet in tweets: 
        db_tweet = Tweet(id=tweet.id, text=tweet.full_text) #iterating over our users and tweets
        db_user.tweets.append(db_tweet) #going to the database and pulling out that particular id and pulling the tweets for that id and then going back to the user and assigning those tweets to the user on our end. #https://www.youtube.com/watch?v=xAAgrHm_EYQ&feature=youtu.be&ab_channel=LambdaSchool if ref needed. 1h.15m in. 
        DB.session.add(db_tweet)

    DB.session.commit()



    


     