import spacy
import re
import nltk
# nltk.download('wordnet')

NLP = spacy.load('en_core_web_sm')

def remove_non_words(text):
    '''
    removes non-words from a string
    '''
    # Remove words with numbers
    if text != text:
        return ''
    new_text = re.sub('[a-zA-Z]*[0-9]+[a-zA-Z]*', '', text)
    # Replace non-alphanumeric characters with spaces
    new_text = re.sub('[^A-Za-z0-9 ]+', ' ', new_text)
    # Remove remaining words composed by one letter or number
    new_text = ' '.join( [w for w in new_text.split() if len(w)>1] )
    return new_text

def normalize_tokens(words):
    '''
    takes a string, normalizes into a list of tokens. This includes removing punctuation,
    numbers, converting to lowercase and singular, and using
    the infinitive form of verbs
    '''
    if type(words) == list:
        words = ' '.join(words)
    lemmatizer = WordNetLemmatizer()
    word_list = nltk.word_tokenize(words)
    words = ' '.join(word_list)
    doc = NLP(words)
    normalized = []
    for token in doc:
        punct = token.is_punct
        number = token.like_num
        stop_word = token.is_stop
        currency = token.is_currency
        if punct or number or stop_word or currency:
            pass
        else:
            normalized.append(token.lemma_.lower())
    return normalized

def word_tokenize(words):
    '''
    reads a string and returns a list of tokens, removing
    punctuation tokens
    '''
    doc = NLP(words)
    tokenized = []
    for word in doc:
        if not word.is_punct and len(word.text.strip()) > 0:
            tokenized.append(word.text)
    return tokenized