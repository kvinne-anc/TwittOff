"""Prediction of Users based on tweet modeling"""
"""Predictions of users based on tweet embeddings"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from twitoff.twitter import vectorize_tweet
from twitoff.models import User


def predict_user(user0_name, user1_name, hypo_tweet_text):
    """
    Determine and return which user is more likely to say a hypothetical tweet.
    Example run: predict_user("elonmusk", "jackblack", "School of rock really rocks")
    Returns 0 (user0_name = elonmusk) or 1 (user1name = jackblack)
    """

    # grabbing users from our database
    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()

    # grabbing vectors from each tweet in user.tweets
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # vertically stacking (combining vectors) to train model (x)
    vects = np.vstack([user0_vects, user1_vects])

    # generate labels for the vects array (y)
    labels = np.concatenate(
        [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

    # train model and instantiate
    log_reg = LogisticRegression().fit(vects, labels)

    # using nlp model to generate embeddings - vectorize_tweet() - and reshapes
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text).reshape(1, -1)

    # predicts and returns 0 or 1 depending upon Logistic Regression models prediction
    return log_reg.predict(hypo_tweet_vect)
    
