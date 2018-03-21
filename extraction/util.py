import fileinput
import os
import re

import MySQLdb
import tweepy

RE_LINK = re.compile(r'https?://')


def read_tweets_from_input():
    return read_tweets(fileinput.input())


def read_tweets(file):
    return [eval(line) for line in file]


def status_is_retweet(status):
    return hasattr(status, 'retweeted_status')


def status_is_quote(status):
    return status.is_quote_status


def status_is_reply(status):
    return status.in_reply_to_status_id


def status_contains_a_link(status):
    return RE_LINK.search(status.text)


def status_is_valid(status):
    return \
        not status_is_retweet(status) \
        and not status_is_quote(status) \
        and not status_is_reply(status) \
        and not status_contains_a_link(status)


def status_to_dict(status):
    return {
        'id': status.id,
        'text': status.text,
        'user_id': status.author.id,
    }


def tweepy_api(app_only_auth=False):
    consumer_token = os.environ['CONSUMER_TOKEN']
    consumer_secret = os.environ['CONSUMER_SECRET']

    if app_only_auth:
        auth = tweepy.AppAuthHandler(consumer_token, consumer_secret)
    else:
        access_token = os.environ['ACCESS_TOKEN']
        access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def connection():
    return MySQLdb.connect(host=os.environ['DB_HOST'], user=os.environ['DB_USER'], password=os.environ['DB_PASS'],
                           database=os.environ['DB_NAME'], charset='utf8mb4')
