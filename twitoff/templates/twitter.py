"""Retrieve tweets and users then create embeddings and populate DB"""

#TWITTER_API_KEY = getenv("TWITTER_API_KEY")
#TWITTER_API_KEY_SECRET = getenv("TWITTER_API_KEY_SECRET")
#ToDo - Don't have raw secrets in our code (make .env file)  
#TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
#TWITTER = tweepy.API(TWITTER_AUTH)

"""Retrieve Tweets, embeddings, and push to our database"""
from os import getenv
import tweepy  # to interact with the twitter API
import spacy  # will use later
from .models import DB, Tweet, User


TWITTER_AUTH = tweepy.OAuthHandler(
    getenv("TWITTER_API_KEY"), getenv("TWITTER_API_KEY_SECRET"))
TWITTER = tweepy.API(TWITTER_AUTH)

nlp = spacy.load("my_model")


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):
    try:
        """Adds user with username 'username' to our database"""
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, name=username)
        DB.session.add(db_user)

        # TODO - fix assumption on continuously new tweets
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False, tweet_mode="extended")

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            vectorized_tweet = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[0:300],
                             vect=vectorized_tweet)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print("Error processing {}: {}".format(username, e))
        raise e

    else:
        DB.session.commit()