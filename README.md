# Progress Report
Please find the required dataset in the link below. The dataset size was large hence uploaded to google cloud.
https://drive.google.com/drive/folders/1C5gI3WY4aV3RvVojjpuKX4rjXacQH36g?usp=sharing

# Similar Post detection on Stack overflow
Ayush Gupta (agupt69 | ayushgupta97)\
Devansh Patel (dpate336 | pateldevansh2612)\
Naman Jain (njain34 |njain2208)\
Akash Sunda (asunda23 | asunda23)\
Afnan Waseem (mwasee3 | mwasee3)
## Problem Statement
Repetitive questions on various programming forums such as Stack Overflow, tend to have a variety
of solutions that work well, would not work in some scenarios or do not work at all. This off puts a lot
of users as well as lends to solutions that are either messy or ones that do not function at all.\
Our goal is to bring in insight for veteran and novice users users by showing them the most frequented
errors in that domain, the best solutions for the problem they are facing or to help them by finding an
expert who could help resolve their query. In addition to this, it would be interesting to see different
trends in such a varied and large dataset.
### Hypothesis:
1. When a problem has multiple possible solutions, ranking the solutions would help users find their solutions in a much easier way.
2. Finding an expert for those users in need of assistance would inturn help users save time and protect them from messy solutions.
3. Probability of getting an answer for your query with a time estimate would help a user plan accordingly.
## Data
### Data Sources:
1. Stack Exchange data explorer
2. Stack Exchange APIs
The above data sources give us easy accessibility to the
required data, and we won’t need to spend a whole lot of time
to collect the data.
### Data Size:
1. 22 Million questions
2. 33 Million answers
3. 84 Million comments
4. 63K tags
### Few Features of the Questions Data:
1. Score of the question
2. Time of each question
3. Comma separated technology tags
4. Number of views
5. Number of answers
6. Score of the answer
7. Time of the answer
## Solution
1. Our initial steps would be to do a comprehensive clean up of the data and since this kind of data includes a lot of free text, we would aim to clean it up by removing the stop words, lemmitizations, etc.
2. Our vision for this project is of two parts, one is to create an interactive query module that would help users get answers for the hypothesis and the other would be a dashboard for trend visualization.
3. We hope to have our dataset cleaned and completed a comprehensive EDA to discover various trends and put them up on a dashboard. Along with this, we would aim to create a framework for query module


