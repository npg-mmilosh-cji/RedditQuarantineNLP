# RedditQuarantineNLP
Investigating the effects of Reddit quarantines on user sentiment and recruitment 


The goal of this project is to use NLP techniques to understand the impact of a Reddit “quarantine”. The project will focus on the language used within the quarantined subreddits before and after quarantine took place.

Our dataset was obtained using Google BigQuery. The dataset contains 10,015,586 records, where each record is a comment (which we refer to as “posts”) posted in r/The_Donald (TD) in 2019. (see https://www.reddit.com/r/bigquery/comments/3cej2b/17_billion_reddit_comments_loaded_on_bigquery/)

**Language Requirements:**
Python 3.7

**Required Libraries:**
See [requirements.txt](requirements.txt)

To create our environment:
1. create a venv (must have venv installed): `PYTHON -m venv env`
2. activate env: `source env/bin/activate`
3. install packages from requirements.txt: `pip install -r requirements.txt`
