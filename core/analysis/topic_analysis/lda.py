import pandas as pd
import gensim
import gensim.corpora as corpora


pkl_path = 'processed_extant_posts_full.pkl'
posts_df = pd.read_pickle(pkl_path)

tokens = posts_df['tokens_lemma']
del posts_df

id2word = corpora.Dictionary(tokens)
corpus = [id2word.doc2bow(text) for text in tokens]

# Write models
# Won't keep results in memory
path_to_box = ''
for num_topics in range(5, 30, 2):
    print("k = " + str(num_topics))
    lda = gensim.models.LdaMulticore(corpus = corpus, id2word = id2word,
                                     num_topics = num_topics, workers = 30,
                                     iterations=100, random_state=0)
    model_path = path_to_box + 'lda_models/lda_' + str(num_topics) + '_topics'
    lda.save(model_path, separately = False)


# Load results for k=17 and add index to it
trained_models = dict()
num_topics = 17
trained_models[num_topics] = gensim.models.LdaMulticore.load('lda_models/lda_' + str(num_topics) + '_topics')

res = list(trained_models[num_topics][corpus])
out = {k:[] for k in range(0, num_topics)}
for l in res:
    topics = dict(l)
    for i in range(0, num_topics):
        if i in topics.keys():
            out[i].append(topics[i])
        else:
            out[i].append(None)

out = pd.DataFrame(out, columns = range(0, num_topics))
tokens_df = pd.concat([tokens.reset_index(), out.reset_index().drop("index", axis = 1)],
                      axis = 1).fillna(0)
tokens_df.to_pickle("lda_probs/topic_distr_" + str(num_topics) + "_index.pkl")


