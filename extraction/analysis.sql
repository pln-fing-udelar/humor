CREATE TEMPORARY TABLE good_quality AS
SELECT
  tweet_id, v.session_id, vote, date
FROM votes v
  LEFT JOIN (SELECT session_id
             FROM votes
             WHERE tweet_id = 965857626843172864 AND vote = 'x') s1
    ON v.session_id = s1.session_id
  LEFT JOIN (SELECT session_id
             FROM votes
             WHERE tweet_id = 965758586747047936 AND vote = 'x') s2
    ON v.session_id = s2.session_id
  LEFT JOIN (SELECT session_id
             FROM votes
             WHERE tweet_id = 301481614033170432) s3
    ON v.session_id = s3.session_id
WHERE vote != 'n'
      AND s1.session_id IS NOT NULL
      AND s2.session_id IS NOT NULL
      AND (s3.session_id IS NULL OR (s3.session_id != 'x' AND s3.session_id != 'n'));

SELECT COUNT(*)
FROM good_quality;

SELECT COUNT(*)
FROM good_quality
WHERE tweet_id = 965857626843172864
      OR tweet_id = 965758586747047936
      OR tweet_id = 301481614033170432
      OR tweet_id = 968699034540978176;
