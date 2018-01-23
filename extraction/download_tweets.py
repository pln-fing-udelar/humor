#!/usr/bin/env python
import argparse
import os
import re

from dotenv import load_dotenv, find_dotenv
import tweepy

RE_RETWEET = re.compile(r'RT @[^:]+: ', re.UNICODE)


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if not RE_RETWEET.match(status.text):
            print({
                'id': status.id,
                'text': status.text,
                'user_id': status.author.id,
                'favorite_count': status.favorite_count,
                'retweet_count': status.retweet_count,
            })


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', default='es', help="language of the tweets to extract (default: es)")
    args = parser.parse_args()

    load_dotenv(find_dotenv())

    consumer_token = os.environ.get('CONSUMER_TOKEN')
    consumer_secret = os.environ.get('CONSUMER_SECRET')

    access_token = os.environ.get('ACCESS_TOKEN')
    access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    stream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())

    stream.sample(languages=[args.language])
