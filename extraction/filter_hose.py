#!/usr/bin/env python
import fileinput
import random
import re

RE_LINK = re.compile(r'https?://')

LIMIT = 3


def tweet_contains_link(tweet):
    return RE_LINK.search(tweet['text'])


def read_tweets_from_input():
    return [eval(line) for line in fileinput.input()]


def main():
    tweets = [tweet for tweet in read_tweets_from_input() if not tweet_contains_link(tweet)]

    tweets = random.sample(tweets, LIMIT)

    for tweet in tweets:
        print(tweet)


if __name__ == '__main__':
    main()
