import os
import requests
import time
import random
import pandas as pd
from datetime import datetime
from core.data.raw.subreddit_info import subreddit_info
from core.util import basic_io
from pushshift_py import PushshiftAPI

SIZE = 100
SECONDS_PER_WEEK = 604800
number_of_weeks = 52
WEEKS_IN_SECONDS = 604800 * number_of_weeks

# time period for pushshift api
TIME_PERIOD = 60
API_LIMIT = 200

api = PushshiftAPI()


def get_posts(subreddit, before):
    '''
    Gets the subreddit posts.
    Input:
        subreddit (string): name of the subreddit
        before (int): timestamp to limit the search
    '''
    url = 'https://api.pushshift.io/reddit/search/submission?'
    url += f'subreddit={subreddit}&before={before}&size={SIZE}&sort=desc'
    print('scraping before:', datetime.fromtimestamp(before))
    resp = requests.get(url, timeout=200)
    status_code = resp.status_code
    if status_code == 200:
        return resp.json()['data']
    else:
        print('no output; sleeping for 1 min before retrying...')
        time.sleep(60 * 1)
        return get_posts(subreddit, before)


def get_subreddit(subreddit, quarantine_date_str):
    '''
    Downloads posts and writes them into databases.
    Input:
        subreddit: (str) name of subreddit
        quarantine_date: (str) date of quarantine as string
    '''
    quarantine_date = int(datetime.strptime(quarantine_date_str, '%Y-%m-%d').timestamp())
    print(f"q date {datetime.fromtimestamp(quarantine_date)}")

    end_date = quarantine_date + WEEKS_IN_SECONDS
    print(f"end date {datetime.fromtimestamp(end_date)}")

    begin_date = quarantine_date - WEEKS_IN_SECONDS
    print(f"begin date {datetime.fromtimestamp(begin_date)}")

    print(f"begin date: {datetime.fromtimestamp(begin_date)}, end date: {datetime.fromtimestamp(end_date)}")

    submission_list = list(api.search_submissions(
        # after=begin_date,
        # before=end_date,
        after=quarantine_date,
        subreddit=subreddit))

    print(len(submission_list))

    dict_list = [x._asdict() for x in submission_list]
    print(len(dict_list))
    submission_df = pd.DataFrame(dict_list, columns=dict_list[0].keys())

    return submission_df


def go():
    '''
    Runs the code.
    Output:
        None, writes csv
    '''
    for subreddit, quarantine_date in subreddit_info.items():
        subreddit_posts_df = get_subreddit(subreddit, quarantine_date)
        file_name = f"{subreddit}_weeks_{number_of_weeks}.csv"
        file_path = os.path.join(os.getcwd(), "core", "data", "raw", file_name)
        subreddit_posts_df.to_csv(file_path)

