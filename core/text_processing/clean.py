import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
stop_words.update([word.translate(str.maketrans('', '', string.punctuation))
                   for word in stop_words])

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
