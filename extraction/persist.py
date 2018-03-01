#!/usr/bin/env python
import argparse
import os

import MySQLdb

import util


def insert_accounts(db, account_ids):
    with db.cursor() as cursor:
        cursor.executemany('INSERT INTO accounts (account_id) VALUES (%s)'
                           ' ON DUPLICATE KEY UPDATE account_id = account_id;',
                           account_ids)


def insert_tweets(db, tweets):
    with db.cursor() as cursor:
        # Consider that there are duplicate tweets in sample sometimes.
        cursor.executemany('INSERT INTO tweets (tweet_id, text, account_id, origin, lang)'
                           ' VALUES (%(id)s, %(text)s, %(user_id)s, \'hose\', \'es\')'
                           ' ON DUPLICATE KEY UPDATE tweet_id = tweet_id',
                           tweets)


def main():
    # The args (language and origin) are being hardcoded right now.

    # parser = argparse.ArgumentParser()
    # parser.add_argument('--language', default='es', help="language of the tweets to extract (default: es)")
    # parser.add_argument('origin', choices=['hose', 'humorous account'], help="origin of the tweets")
    # parser.add_argument('file', nargs='?', help="file to load (default: stdin)")
    # args = parser.parse_args()

    tweets = util.read_tweets_from_input()

    # for tweet in tweets:
    #     tweet['lang'] = args.language

    db = MySQLdb.connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'),
                         password=os.getenv('MYSQL_ROOT_PASSWORD'),
                         database=os.getenv('DB_NAME'), charset='utf8mb4')

    try:
        insert_accounts(db, {tweet['user_id'] for tweet in tweets})
        insert_tweets(db, tweets)
        db.commit()
    except Exception:
        db.rollback()
        raise


if __name__ == '__main__':
    main()
