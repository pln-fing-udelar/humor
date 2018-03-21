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

        # Use different lists for the current ones and the new ones so deleted tweets preserve their text in the DB.
        tweets_to_update = []

        api = util.tweepy_api()

        with tqdm(total=len(tweets_in_db), desc="Downloading statuses") as progress_bar:
            for tweet_group in util.chunks(tweets_in_db, MAX_STATUSES_COUNT_PER_STATUSES_LOOKUP):
                tweet_group_by_id = {tweet['id']: tweet for tweet in tweet_group}

                statuses = api.statuses_lookup(tweet_group_by_id.keys(), map_=False)

                for status in statuses:
                    if status.text != tweet_group_by_id[status.id]['text']:
                        print(status.text)
                        tweets_to_update.append(util.status_to_dict(status))

                time.sleep(DELAY_PER_USER_AUTH_STATUSES_LOOKUP_REQUEST)

                progress_bar.update(len(tweet_group))

        print('')
        print(len(tweets_to_update), "tweets to update")
        print('')

        with connection as cursor:
            # There is no simple way to do a batch update in MySQL. One option would be to use
            # INSERT ... ON DUPLICATE KEY UPDATE, but it makes compulsory to specify the rest of the fields if not null.
            # Maybe it could have been done with REPLACE.
            for tweet in tweets_to_update:
                cursor.execute('UPDATE tweets SET text = %(text)s WHERE tweet_id = %(id)s', tweet)

        connection.commit()

        # Check that everything is alright.
        with connection as cursor:
            cursor.execute('SELECT tweet_id, text FROM tweets')
            tweet_text_by_id = {t[0]: t[1] for t in cursor.fetchall()}

        for tweet in tweets_to_update:
            assert tweet['text'] == tweet_text_by_id[tweet['id']]
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == '__main__':
    main()
