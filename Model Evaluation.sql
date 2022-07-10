WITH TAG_ANS_USR AS (
SELECT A.id ID,CAST(SPLIT(Q.TAGS,'|') AS ARRAY<STRING>) TAGS, A.owner_user_id AUTHOR_ID  FROM `bigquery-public-data.stackoverflow.posts_questions` Q
LEFT JOIN `bigquery-public-data.stackoverflow.posts_answers` A ON Q.accepted_answer_id=A.id
WHERE Q.last_activity_date between TIMESTAMP("2020-01-01") AND TIMESTAMP("2021-04-01")),
USR_TAG AS (
SELECT TAGS,AUTHOR_ID,1 COUNTS FROM TAG_ANS_USR, UNNEST(TAGS) TAGS
WHERE ID IS NOT NULL AND AUTHOR_ID IS NOT NULL),
FINAL AS (
SELECT DISTINCT TAGS,AUTHOR_ID,SUM(COUNTS) TOTAL_Q_ANS FROM USR_TAG
GROUP BY TAGS,AUTHOR_ID
LIMIT 100000)
SELECT * EXCEPT(nearest_centroids_distance) 
FROM ML.PREDICT(MODEL `stackproject-348415.stackoverflow.KMEANS_MODEL_2`, (SELECT * FROM FINAL))