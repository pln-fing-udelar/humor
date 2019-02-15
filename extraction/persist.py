#!/usr/bin/env python
import util


def insert_accounts(connection, account_ids):
    with connection as cursor:
        cursor.executemany('INSERT INTO accounts (account_id) VALUES (%s)'
                           ' ON DUPLICATE KEY UPDATE account_id = account_id;',
                           account_ids)


def insert_tweets(connection, tweets):
    with connection as cursor:
        # Consider that there are duplicate tweets in sample sometimes.
        # Also, consider that the key names may vary between 'tweet_id' or 'id', and `account_id or 'user_id',
        #   depending on the input file.
        cursor.executemany('INSERT INTO tweets (tweet_id, text, account_id, origin, lang)'
                           ' VALUES (%(tweet_id)s, %(text)s, %(account_id)s, %(origin)s, %(lang)s)'
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

    connection = util.connection()

    try:
        # Consider that the key name may vary between 'account_id' or 'user_id' depending on the input file.
        insert_accounts(connection, {tweet['account_id'] for tweet in tweets})
        insert_tweets(connection, tweets)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == '__main__':
    main()
