from TextCleanUp import utils

__version__ = '0.0.2'

def get_word_count(text: str) -> int: 
    """
    This function takes a string of text as input and returns the word count in the input string.
    
    Parameters:
    - text (str): The input string whose word count is to be computed.
    
    Returns:
    - int: The number of words in the input string.
    
    Example:
    >>> get_word_count("Hello, this is a sample sentence.")
    6
    """
    return utils._get_word_count(text)

def get_char_count(text: str) -> int:
    """
    This function takes a string as input and returns the count of non-whitespace characters in the string.

    Parameters:
    - text (str): The input string for which non-whitespace character count is to be calculated. 

    Returns:
    - int: The count of non-whitespace characters in the input string.

    Example:
    >>> get_char_count('The quick brown fox jumps over the lazy dog.')
    32

    Explanation:
    The regular expression '\s+' matches one or more whitespace characters including space, tab, newline, carriage return, etc.
    The 're.sub' function replaces all matching substrings with an empty string thereby removing them from the input string.
    The length of the resulting string gives us the count of non-whitespace characters in the input string.
    """
    return utils._get_char_count(text)

def get_avg_wordlength(text: str) -> float:
    """
    Returns the average length of words in a given text.

    Parameters:
    - text (str): The input string from which to calculate the average word length.

    Returns:
    - float: The average length of words in the input text.

    Example:
    >>> text = "The quick brown fox jumps over the lazy dog"
    >>> get_avg_wordlength(text)
    3.5
    """
    return utils._get_avg_wordlength(text)

def get_stopwords_count(text: str) -> int:
    """
    Calculates the count of stopwords in the given text.

    Parameters:
        - text (str): A string of text to analyze for stopwords.

    Returns:
        - int: The count of stopwords found in the text.

    Example usage:
    >>> text = "The quick brown fox jumps over the lazy dog"
    >>> get_stopwords_count(text)
    4
    """
    return utils._get_stopwords_count(text)

def get_hashtag_count(text: str) -> int:
    """
    Returns the number of words that start with '#' in the given text.
    
    Parameters:
    - text (str): The text to search for hashtags.
    
    Returns:
    - int: The number of words that start with '#'.
    """
    return utils._get_hashtag_count(text)

def get_mentions_count(text):
    """
     Returns the number of words that start with '@' in the given text.
    
    Parameters:
    - text (str): The text to search for mentions.
    
    Returns:
     -int: The number of words that start with '@'.
    """
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