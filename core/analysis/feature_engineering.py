import pandas as pd
import math
from flashtext import KeywordProcessor

def log_nword(str):
    '''
    Returns the log base 10 of the number of words in a post
    '''
    return math.log10(len(str.split()))


def flashtext_init(keyword_path):
    kp = KeywordProcessor()
    kp.add_keyword_from_file(keyword_path)
    return kp


def flashtext_count(processor, bodytext):
    rv_dict = processor.extract_keywords(bodytext)
    return pd.Series(rv_dict).value_counts().to_dict()
