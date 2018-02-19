#!/usr/bin/env python
import random

from extraction import util

LIMIT = 10000


def main():
    for tweet in random.sample(util.read_tweets_from_input(), LIMIT):
        print(tweet)


if __name__ == '__main__':
    main()
