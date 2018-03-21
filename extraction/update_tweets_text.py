#!/usr/bin/env python
import time

from tqdm import tqdm

import util

USER_AUTH_STATUSES_LOOKUP_RATE_LIMIT_PER_WINDOW = 900
SECS_IN_A_MINUTE = 60
DELAY_PER_USER_AUTH_STATUSES_LOOKUP_REQUEST = 15 * SECS_IN_A_MINUTE / USER_AUTH_STATUSES_LOOKUP_RATE_LIMIT_PER_WINDOW
MAX_STATUSES_COUNT_PER_STATUSES_LOOKUP = 100


def main():
    connection = util.connection()
    try:
        with connection as cursor:
            cursor.execute('SELECT tweet_id, text FROM tweets')
            tweets_in_db = [{'id': t[0], 'text': t[1]} for t in cursor.fetchall()]

        # Use different lists for the current ones and the new ones because so deleted tweets preserve their text.
        tweets_to_update = []

        api = util.tweepy_api()

        with tqdm(total=len(tweets_in_db), desc="Downloading statuses") as progress_bar:
            for tweet_group in util.chunks(tweets_in_db, MAX_STATUSES_COUNT_PER_STATUSES_LOOKUP):
                statuses = api.statuses_lookup((tweet['id'] for tweet in tweet_group), map_=False)

                for status in statuses:
                    # TODO: diff the actual tweet text with the downloaded one so we can see the changes.
                    tweets_to_update.append(util.status_to_dict(status))

                time.sleep(DELAY_PER_USER_AUTH_STATUSES_LOOKUP_REQUEST)

                progress_bar.update(len(tweet_group))

        cursor.executemany('INSERT INTO tweets (tweet_id, text)'
                           ' VALUES (%(id)s, %(text)s)'
                           ' ON DUPLICATE KEY UPDATE text = VALUES(text)',
                           tweets_to_update)

        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == '__main__':
    main()
