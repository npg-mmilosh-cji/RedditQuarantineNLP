"""
File for processing csvs from BigQuery
"""
import os
import gc
import pandas as pd
import numpy as np
from datetime import datetime
from core.util.basic_io import *

headers = set()
data = []
row_count_check = 0
BIG_QUERY_DIR = os.path.join("core", "data", "raw", "BigQuery")
for dir_name, subdir_list, file_list in os.walk(BIG_QUERY_DIR):
        for fname in file_list:
            if '.csv' in fname and 'Processed' not in fname:
                print("---------- " + fname + " -----------------------")
                this_data = read_csv_to_list(os.path.join(BIG_QUERY_DIR, fname))
                header = tuple(this_data.pop(0))
                headers.add(header)
                row_count_check += len(this_data)
                data.extend(this_data)

assert len(headers) == 1
assert row_count_check == len(data)
print(f"rows in data: {len(data)}")

output_filename = os.path.join("core", "data", "raw", "combined_bigquery_raw.csv")
header = list(header)
combined = [header]
combined.extend(data)
assert len(combined) == (len(data)+1)
write_list_to_csv(data, output_filename)

del combined
gc.collect()

df = pd.DataFrame(data, columns=header)

df['created_date'] = pd.to_datetime(
    df['created_utc'].apply(
        lambda x: None if np.isnan(int(x)) else datetime.fromtimestamp(int(x))),
    errors='coerce')
df['created_date'] = df['created_date'].dt.date
print(df.created_date.min())
print(df.created_date.max())

df.rename(columns={'body':'selftext'}, inplace=True)
df['post_type'] = np.select(
    [
        df['selftext'] == '[removed]',
        df['selftext'] == '[deleted]',
        df['selftext'] == '',
        pd.isna(df['selftext'])
    ],
    [
        'removed',
        'deleted',
        'blank',
        'nan'
    ],
    default='extant'
)

print(df.groupby('post_type')['post_type'].count())
proc_output_filename = os.path.join("core", "data", "raw", "combined_bigquery_processed.csv")
df.to_csv(proc_output_filename, index=False)
