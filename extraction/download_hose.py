#!/usr/bin/env python
import argparse
import os
import re
import sys

import tweepy

RE_LINK = re.compile(r'https?://')


def status_is_retweet(status):
    return hasattr(status, 'retweeted_status')


def status_is_quote(status):
    return status.is_quote_status


def status_is_reply(status):
    return status.in_reply_to_status_id


def status_contains_a_link(status):
    return RE_LINK.search(status.text)


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if not status_is_retweet(status) and not status_is_quote(status) \
                and not status_is_reply(status) and not status_contains_a_link(status):
            print({
                'id': status.id,
                'text': status.text,
                'user_id': status.author.id,
            })

    def on_error(self, status_code):
        print("Error:", status_code, file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', default='es', help="language of the tweets to extract (default: es)")
    args = parser.parse_args()

    consumer_token = os.environ.get('CONSUMER_TOKEN')
    consumer_secret = os.environ.get('CONSUMER_SECRET')
    access_token = os.environ.get('ACCESS_TOKEN')
    access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    stream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
    stream.sample(languages=[args.language])


if __name__ == '__main__':
    main()
