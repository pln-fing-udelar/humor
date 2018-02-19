#!/usr/bin/env python
import random
import re

from extraction import util

RE_LINK = re.compile(r'https?://')

LIMIT = 10000


def tweet_contains_link(tweet):
    return RE_LINK.search(tweet['text'])


def main():
    tweets = [tweet for tweet in util.read_tweets_from_input() if not tweet_contains_link(tweet)]

    tweets = random.sample(tweets, LIMIT)

    for tweet in tweets:
        print(tweet)


if __name__ == '__main__':
    main()
