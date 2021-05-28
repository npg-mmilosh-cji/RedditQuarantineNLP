import gensim
import gensim.corpora as corpora
import numpy as np
import utils
import os
import pandas as pd
from pprint import pprint


# data_path = '/home/mmilosh/RedditQuarantineNLP/BigQuery/'

# for file_ in os.listdir(data_path):
#     print(file_)
# df = pd.read_csv(data_path + file_, low_memory = False)
df = pd.read_csv('/home/mmilosh/RedditQuarantineNLP/combined_bigquery_processed.csv',
 low_memory = False, usecols = ["selftext"])

df['selftext'] = df['selftext'].str.lower()
df['selftext'] = df['selftext'].apply(utils.remove_non_words)
print('removed non words')
df['tokenized_text'] = df['selftext'].apply(utils.word_tokenize)
print('tokenized text')
df['normalized_text'] = df['tokenized_text'].apply(utils.normalize_tokens)
print('normalized text')
df = df[['normalized_text']]
# df[['selftext', 'tokenized_text', 'normalized_text']].head()

# Create corpus
id2word = corpora.Dictionary(df['normalized_text'])
corpus = [id2word.doc2bow(text) for text in df['normalized_text']]

# Build LDA model 
print('building lda')
num_topics = 10
lda_model = gensim.models.LdaMulticore(corpus = corpus,
                                    id2word = id2word,
                                    num_topics = num_topics,
                                    workers = 30)
pprint(lda_model.print_topics())
doc_lda = lda_model[corpus]

# modname = str('lda_model_' + file_)
modname = str('lda_model')
lda_model.save(modname)