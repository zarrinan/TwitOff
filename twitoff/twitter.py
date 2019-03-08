"""Retrieve TWeets, embeddings, and persist in the database."""
import basilica
import tweepy
from decouple import config
from .models import DB, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))

#TODO: some useful methods
def add_or_update_user(username):
    """Add or update the user or their tweets"""
    try:
        tweeter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twiter_user.id) or
                   User(id = twitter_user.id, name=username))
        DB.session.add(db_user)
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False,
            tweet_mode='extended', since_id = db_user.newest_tweet_id)
        if tweets:
            db_user.newest_tweet_id = tweet[0].id
        for tweet in tweets:
            #get embedding for tweet, and store in db
            embedding = BASILICA.embed_sentence(tweet.full_text,
                                                mode="twitter")
            db_tweet = Tweet(id = tweet.id, tweet=tweet.full_text[:500],
                             embedding = embedding)
            db_user.tweets.append(db_tweet)
            B.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    else:
        DB.session.commit()


