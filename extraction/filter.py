#!/usr/bin/env python
import random

import util

LIMIT = 12000


def main():
    # FIXME: We should remove repeated tweets as well, as the hose can yield them.
    for tweet in random.sample(util.read_tweets_from_input(), LIMIT):
        print(tweet)


if __name__ == '__main__':
    main()
