CREATE OR REPLACE MODEL `stackproject-348415.stackoverflow.KMEANS_MODEL_2`
OPTIONS(model_type='kmeans', num_clusters=10, standardize_features = true) AS
WITH TAG_ANS_USR AS (
SELECT A.id ID,CAST(SPLIT(Q.TAGS,'|') AS ARRAY<STRING>) TAGS, A.owner_user_id AUTHOR_ID  FROM `bigquery-public-data.stackoverflow.posts_questions` Q
LEFT JOIN `bigquery-public-data.stackoverflow.posts_answers` A ON Q.accepted_answer_id=A.id
WHERE Q.last_activity_date between TIMESTAMP("2021-01-01") AND TIMESTAMP("2022-04-01")),
USR_TAG AS (
SELECT TAGS,AUTHOR_ID,1 COUNTS FROM TAG_ANS_USR, UNNEST(TAGS) TAGS
WHERE ID IS NOT NULL AND AUTHOR_ID IS NOT NULL AND AUTHOR_ID != 0)
SELECT DISTINCT AUTHOR_ID,TAGS,SUM(COUNTS) TOTAL_Q_ANS FROM USR_TAG
GROUP BY TAGS,AUTHOR_ID;
