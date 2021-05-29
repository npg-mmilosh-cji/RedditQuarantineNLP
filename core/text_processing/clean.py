import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
stop_words.update([word.translate(str.maketrans('', '', string.punctuation))
                   for word in stop_words])
stop_words.add("like")
stop_words.add("would")
stop_words.add("see")
stop_words.add("get")
stop_words.add("im")
stop_words.add("thats")
stop_words.add("may")
stop_words.add("got")

printable = set(string.printable)
wnl = WordNetLemmatizer()


def remove_multiple_spaces(doc):
    """
    Remove multiple space, tab, etc replace with single space
    """
    try:
        return " ".join(doc.split())
    except:
        print(doc)
        return ""


def process_text(doc):
    text_clean_space = remove_multiple_spaces(doc)
    text_clean_space = ''.join(
        filter(lambda x: x in printable, text_clean_space))
    strip_punc_lower = text_clean_space.translate(
        str.maketrans('', '', string.punctuation)).lower()
    len_clean_str = len(strip_punc_lower)
    has_long_token = False
    tokens = []
    clean_tokens = []
    lemmatized_tokens = []
    bigrams = []
    try:
        for token in word_tokenize(strip_punc_lower):
            tokens.append(token)
            if token not in stop_words and 1 < len(token) < 21:
                clean_tokens.append(token)
                lemmatized_tokens.append(wnl.lemmatize(token))
            elif len(token) >= 21:
                has_long_token = True

        bigrams = list(nltk.bigrams(lemmatized_tokens))

    except Exception as e:
        print(e)

    return (doc,
            has_long_token,
            text_clean_space,
            strip_punc_lower,
            len_clean_str,
            tokens,
            clean_tokens,
            lemmatized_tokens,
            bigrams)


def process_text_minimal(doc):
    text_clean_space = remove_multiple_spaces(doc)
    text_clean_space = ''.join(
        filter(lambda x: x in printable, text_clean_space))
    len_clean_str = len(text_clean_space)

    return (doc,
            text_clean_space,
            len_clean_str)
