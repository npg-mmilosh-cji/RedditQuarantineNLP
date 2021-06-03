# RedditQuarantineNLP
Investigating the effects of Reddit quarantines on user sentiment and recruitment 


The goal of this project is to use NLP techniques to understand the impact of a Reddit “quarantine”. The project will focus on the language used within the quarantined subreddits before and after quarantine took place.

Our dataset was obtained using Google BigQuery. The dataset contains 10,015,586 records, where each record is a comment (which we refer to as “posts”) posted in r/The_Donald (TD) in 2019. 

(see: https://www.reddit.com/r/bigquery/comments/3cej2b/17_billion_reddit_comments_loaded_on_bigquery/)

We applied machine learning models to the text in order to produce meaningful summaries about the content of posts in TD and to determine whether there are any observable changes in the data around the time of quarantine. This is primarily an unsupervised learning problem since we do not have labels that are helpful in answering this question. 


We use pretrained **sentiment analysis** models to examine the polarity of posts (positive, negative, or neutral). We then use **topic modeling** to examine themes within the posts. The output of the sentiment and topic analysis become input to our clustering approach, which attempts to find similar groups of posts along a variety of interesting features.


**Language Requirements:**
Python 3.7

**Required Libraries:**
See [requirements.txt](requirements.txt)

To create our environment:
1. create a venv (must have venv installed): `PYTHON -m venv env`
2. activate env: `source env/bin/activate`
3. install packages from requirements.txt: `pip install -r requirements.txt`
