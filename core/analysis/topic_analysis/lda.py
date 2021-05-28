
import pandas as pd
import gensim
import gensim.corpora as corpora

def save_models(named_models):
    for num_topics, model in named_models.items():
        # set your path to models:
        model_path = 'lda_models/lda_' + num_topics + '_topics'
        model.save(model_path, separately = False)


posts_df = pd.read_pickle('sampled_processed_extant_posts_june_july.pkl')

id2word = corpora.Dictionary(posts_df['tokens_lemma'])
print('Making corpus...')
corpus = [id2word.doc2bow(text) for text in posts_df['tokens_lemma']]

trained_models = dict()
for num_topics in range(5, 30, 2):
    print("Training LDA(k=%d)" % num_topics)
    lda = gensim.models.LdaMulticore(corpus = corpus, id2word = id2word,
                                     num_topics = num_topics, workers = 3,
                                     passes=10, iterations=100, random_state=0, eval_every=None)
    trained_models[num_topics] = lda

save_models(trained_models)