from TextCleanUp import utils

__version__ = '0.0.2'

def get_word_count(text):
    return utils._get_word_count(text)

def get_char_count(text):
    return utils._get_char_count(text)

def get_avg_wordlength(text):
    return utils._get_avg_wordlength(text)

def get_stopwords_count(text):
    return utils._get_stopwords_count(text)

def get_hashtag_count(text):
    return utils._get_hashtag_count(text)

def get_mentions_count(text):
    return utils._get_mentions_count(text)

def get_digit_count(text):
    return utils._get_digit_count(text)

def get_uppercase_word_count(text):
    return utils._get_uppercase_word_count(text)

def get_contraction_to_expansion(text):
    return utils._get_contraction_to_expansion(text)

def get_lower_case(text):
    return utils._get_lower_case(text)

def get_emails(text):
    return utils._get_emails(text)

def remove_emails(text):
    return utils._remove_emails(text)

def get_urls(text):
    return utils._get_urls(text)

def remove_urls(text):
    return utils._remove_urls(text)

def remove_rt(text):
    return utils._remove_rt(text)

def remove_special_characters(text):
    return utils._remove_special_characters(text)

def remove_multiple_whitespaces(text):
    return utils._remove_multiple_whitespaces(text)

def remove_html_tags(text):
    return utils._remove_html_tags(text)

def remove_accented_chars(text):
    return utils._remove_accented_chars(text)

def remove_stopwords(text):
    return utils._remove_stopwords(text)

def lemmatize_text(text):
    return utils._lemmatize_text(text)

def get_value_counts(df, col):
    return utils._get_value_counts(df,col)

def remove_common_word(df, freq, n):
    return utils._remove_common_word(df,freq,n)

def remove_rarewords(df, freq, n):
    return utils._remove_rarewords(df,freq,n)

def get_spelling_correction(text):
    return utils._get_spelling_correction(text)