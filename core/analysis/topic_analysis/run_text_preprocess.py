import os
import pandas as pd
import gc

from core.text_processing import clean

# read all data
posts_pkl_path = os.path.join('..', '..', "combined_bigquery_processed.pkl")
posts_df = pd.read_pickle(posts_pkl_path)

posts_df = posts_df[(posts_df["created_date"] > '2019-05-31') & (posts_df["created_date"] < '2019-08-01')]
print(f"num rows in sample {len(posts_df)}")
print(posts_df.created_date.min())
print(posts_df.created_date.max())
# num rows in sample 1760263
# 2019-06-01
# 2019-07-31

# take extant post subset
extant_posts = posts_df[posts_df['post_type'] == 'extant']
print(f"nrow in extant posts: {len(extant_posts)}")
# 8,983,413
extant_posts.head()

# remove unnecesary large data obj, since we have extant_posts
del posts_df
gc.collect()

# run clean
# add column names
processed_text_columns = extant_posts.apply(
    lambda row: clean.process_text(row['selftext']), axis='columns', result_type='expand')

# add column names
processed_text_columns.columns = ['text_clean_space',
                                  'text_clean_punc_lower',
                                  'len_clean',
                                  'tokens',
                                  'tokens_clean',
                                  'tokens_lemma',
                                  'bigrams',
                                  'trigrams']

# attach new columns back to larger df
extant_posts = pd.concat([extant_posts, processed_text_columns],
                         axis='columns')

# pickle new cols only
processed_text_columns.to_pickle("../../sampled_processed_extant_posts_june_july.pkl")

# pickle all extant data (new columns and orig)
# extant_posts.to_pickle("../../sampled_full_extant_posts_1perc.pkl")