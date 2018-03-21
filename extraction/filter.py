#!/usr/bin/env python
import random

import util

LIMIT = 4500


def tweets_with_unique_text(tweets):
    return {tweet['text']: tweet for tweet in tweets}.values()


def tweets_from_database():
    connection = util.connection()
    try:
        with connection as cursor:
            cursor.execute('SELECT tweet_id, text FROM tweets')
            tweets = [{'id': id_, 'text': text} for id_, text in cursor.fetchall()]
            return {tweet['id'] for tweet in tweets}, {tweet['text'] for tweet in tweets}
    finally:
        connection.close()


def main():
    tweets = util.read_tweets_from_input()
    tweets = list(tweets_with_unique_text(tweets))

    db_tweets_ids, db_tweet_texts = tweets_from_database()

    for tweet in tweets:
        if tweet['id'] in db_tweets_ids:
            print(tweet)

    # for tweet in random.sample(tweets, LIMIT):
    #     print(tweet)


if __name__ == '__main__':
    main()
