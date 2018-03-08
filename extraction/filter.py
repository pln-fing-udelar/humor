#!/usr/bin/env python
import random

import util

LIMIT = 12000


def main():
    for tweet in random.sample(util.read_tweets_from_input(), LIMIT):
        print(tweet)


if __name__ == '__main__':
    main()
