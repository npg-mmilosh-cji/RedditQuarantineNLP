import os
import requests
import time
import random
from datetime import datetime
from core.data.raw.subreddit_info import subreddit_info
from core.util import basic_io

SIZE = 100
SECONDS_PER_WEEK = 604800
number_of_weeks = 2
WEEKS_IN_SECONDS = 604800 * number_of_weeks


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
    all_posts = []
    quarantine_date = int(datetime.strptime(quarantine_date_str, '%Y-%m-%d').timestamp())
    next_6_weeks = quarantine_date + WEEKS_IN_SECONDS
    prev_6_weeks = quarantine_date - WEEKS_IN_SECONDS
    get_farthest = next_6_weeks
    output_length = 100

    while output_length == 100 and get_farthest >= prev_6_weeks:
        posts = get_posts(subreddit, get_farthest)
        output_length = len(posts)
        all_posts.extend(posts)

        for post in posts:
            post_date = post['created_utc']

        if get_farthest != post_date:
            get_farthest = post_date
        else:
            get_farthest -= 1

        time.sleep(1 + random.randint(0, 1))

    print(len(all_posts))
    return all_posts


def go(mode='scrape'):
    '''
    Runs the code.
    Input:
        mode: if not specified or 'scrape', it will use subreddits
        from subreddits.txt
        if specified to anithing other than 'scrape', asks for
        a subreddit to test on.
    Output:
        None, writes an .sql file.
    '''
    if mode == 'scrape':
        for subreddit, quarantine_date in subreddit_info.items():
            subreddit_posts = get_subreddit(subreddit, quarantine_date)
            file_name = f"{subreddit}_weeks_{number_of_weeks}.json"
            file_path = os.path.join(os.getcwd(), "core", "data", "raw", file_name)
            basic_io.write_dict_to_json(file_path, subreddit_posts)
    else:
        subreddit = 'uchicago'
        quarantine_date = '2021-01-15'
        subreddit_posts = get_subreddit(subreddit, quarantine_date)
        file_name = f"{subreddit}_weeks_{number_of_weeks}.json"
        file_path = os.path.join(os.getcwd(), "core", "data", "raw", file_name)
        basic_io.write_dict_to_json(file_path, subreddit_posts)
