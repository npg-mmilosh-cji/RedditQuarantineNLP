import gensim
# from gensim.utils import simple_preprocess
# from gensim.parsing.preprocessing import STOPWORDS
import gensim.corpora as corpora
# from nltk.stem import WordNetLemmatizer, SnowballStemmer
# from nltk.stem.porter import *
import numpy as np
import utils
import os
import pandas as pd
from pprint import pprint


# np.random.seed(2018)
for file_ in os.listdir():
    print(file_)
    df = pd.read_csv('BigQuery/TD_Apr19.csv', low_memory=False)

    df['body'] = df['body'].str.lower()
    df['body'] = df['body'].apply(utils.remove_non_words)
    print('removed non words')
    df['tokenized_text'] = df['body'].apply(utils.word_tokenize)
    print('tokenized text')
    df['normalized_text'] = df['tokenized_text'].apply(utils.normalize_tokens)
    print('normalized text')
    # df[['body', 'tokenized_text', 'normalized_text']].head()

    # Create corpus
    id2word = corpora.Dictionary(df['normalized_text'])
    corpus = [id2word.doc2bow(text) for text in df['normalized_text']]

    # Build LDA model 
    print('building lda')
    num_topics = 10
    lda_model = gensim.models.LdaMulticore(corpus = corpus,
                                        id2word = id2word,
                                        num_topics = num_topics)
    pprint(lda_model.print_topics())
    doc_lda = lda_model[corpus]

    modname = str('lda.model' + file_)
    lda_model.save(modname)