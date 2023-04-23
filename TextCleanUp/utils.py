import re 
import os
import sys
import contractions
import numpy as np
import pandas as pd
import spacy
from typing import List, Tuple
from bs4 import BeautifulSoup
import unicodedata
from textblob import TextBlob

from spacy.lang.en.stop_words import STOP_WORDS as stopwords
stopwords.discard('not')

nlp = spacy.load('en_core_web_sm')


def _get_word_count(text: str) -> int: 
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
    word_count = len(text.split())
    return word_count

def _get_char_count(text: str) -> int:
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
    char_count = len(re.sub('\s+', "", text))
    return char_count

def _get_avg_wordlength(text: str) -> float:
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
    avg_wordlength = _get_char_count(text)/_get_word_count(text)
    return avg_wordlength

def _get_stopwords_count(text: str) -> int:
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
    # Split the text into individual words and convert to lowercase
    words = [word.lower() for word in text.split()]

    # Count the number of words that appear in the stopwords list
    stopwords_count = len([word for word in words if word in stopwords])

    return stopwords_count

def _get_hashtag_count(text: str) -> int:
    """
    Returns the number of words that start with '#' in the given text.
    
    Parameters:
    - text (str): The text to search for hashtags.
    
    Returns:
    - int: The number of words that start with '#'.
    """
    # The regex pattern "#+\S+" matches one or more '#' characters followed by 
    # one or more non-whitespace characters. This will match any word starting 
    # with a '#' symbol.
    hashtag_count = len(re.findall("#+\S+",text))
    return hashtag_count

def _get_mentions_count(text: str) -> int:
    """
    Returns the number of words that start with '@' in the given text.
    
    Parameters:
    - text (str): The text to search for mentions.
    
    Returns:
     -int: The number of words that start with '@'.
    """
    # The regex pattern "@+\S+" matches one or more '@' characters followed by 
    # one or more non-whitespace characters. This will match any word starting 
    # with an '@' symbol.
    mentions_count = len(re.findall("@+\S+", text))
    
    return mentions_count

def _get_digit_count(text: str) -> int:
    """
    Returns the number of digits present in the given text.
    
    Parameters:
    - text (str): The text to search for digits.
    
    Returns:
    - int: The number of digits found in the text.
    """
    # The regex pattern r'\b\d+\b' matches one or more digits surrounded by word 
    # boundaries. This will match any sequence of consecutive digits in the text.
    # \b matches a word boundary, ensuring that the pattern only matches digits that
    # are not part of a larger word.
    digit_count = len(re.findall(r'\b\d+\b', text))
    
    return digit_count

def _get_uppercase_word_count(text:str) -> int:
    """
    This function takes a string as input and returns the count of uppercase words in it.
    
    Parameters:
    - text (str): A string containing words
    
    Returns:
    - An integer representing the count of uppercase words in the input text.
    
    Example:
    >>> get_uppercase_word_count("Hello WORLD! HOW are You?")
    2
    """
    # The regex used here is \b[A-Z]+\b
    # \b matches word boundaries
    # [A-Z]+ matches one or more consecutive uppercase letters
    # So, the regex matches all the uppercase words in the text
    uppercase_word_count = len(re.findall(r'\b[A-Z]+\b',text))

    return uppercase_word_count

def _get_contraction_to_expansion(text:str) -> str:
    """
    This function takes in a string parameter `text` and returns its expanded form by converting common English
    contractions to their corresponding expansions. It uses the `contractions` library to expand contractions.

    Parameters:
    - text (str): A string value containing English contractions that need to be expanded.

    Returns:
    - str: A string value that contains the expanded form of the input `text`.

    Example Usage:
    ```
    original_text = "I can't believe it's already Friday!"
    expanded_text = get_contraction_to_expansion(original_text)

    print("Original text: ", original_text)
    print("Expanded text: ", expanded_text)
    ```
    Output:
    ```
    Original text:  I can't believe it's already Friday!
    Expanded text:  I cannot believe it is already Friday!
    ```

    The `contractions` library is used to expand contractions like "I'm" to "I am", "you're" to "you are", etc.
    """
    contractions_list = { 
            "ain't": "am not",
            "aren't": "are not",
            "can't": "cannot",
            "can't've": "cannot have",
            "'cause": "because",
            "could've": "could have",
            "couldn't": "could not",
            "couldn't've": "could not have",
            "didn't": "did not",
            "doesn't": "does not",
            "don't": "do not",
            "hadn't": "had not",
            "hadn't've": "had not have",
            "hasn't": "has not",
            "haven't": "have not",
            "he'd": "he would",
            "he'd've": "he would have",
            "he'll": "he will",
            "he'll've": "he will have",
            "he's": "he is",
            "how'd": "how did",
            "how'd'y": "how do you",
            "how'll": "how will",
            "how's": "how does",
            "i'd": "i would",
            "i'd've": "i would have",
            "i'll": "i will",
            "i'll've": "i will have",
            "i'm": "i am",
            "i've": "i have",
            "isn't": "is not",
            "it'd": "it would",
            "it'd've": "it would have",
            "it'll": "it will",
            "it'll've": "it will have",
            "it's": "it is",
            "let's": "let us",
            "ma'am": "madam",
            "mayn't": "may not",
            "might've": "might have",
            "mightn't": "might not",
            "mightn't've": "might not have",
            "must've": "must have",
            "mustn't": "must not",
            "mustn't've": "must not have",
            "needn't": "need not",
            "needn't've": "need not have",
            "o'clock": "of the clock",
            "oughtn't": "ought not",
            "oughtn't've": "ought not have",
            "shan't": "shall not",
            "sha'n't": "shall not",
            "shan't've": "shall not have",
            "she'd": "she would",
            "she'd've": "she would have",
            "she'll": "she will",
            "she'll've": "she will have",
            "she's": "she is",
            "should've": "should have",
            "shouldn't": "should not",
            "shouldn't've": "should not have",
            "so've": "so have",
            "so's": "so is",
            "that'd": "that would",
            "that'd've": "that would have",
            "that's": "that is",
            "there'd": "there would",
            "there'd've": "there would have",
            "there's": "there is",
            "they'd": "they would",
            "they'd've": "they would have",
            "they'll": "they will",
            "they'll've": "they will have",
            "they're": "they are",
            "they've": "they have",
            "to've": "to have",
            "wasn't": "was not",
            " u ": " you ",
            " ur ": " your ",
            " n ": " and ",
            "won't": "would not",
            'dis': 'this',
            'bak': 'back',
            'brng': 'bring'}
    new_contractions_list={ 
            "ain't": "am not",
            "aren't": "are not",
            "can't": "cannot",
            "can't've": "cannot have",
            "'cause": "because",
            "could've": "could have",
            "couldn't": "could not",
            "couldn't've": "could not have",
            "didn't": "did not",
            "doesn't": "does not",
            "don't": "do not",
            "hadn't": "had not",
            "hadn't've": "had not have",
            "hasn't": "has not",
            "haven't": "have not",
            "he'd": "he had",
            "he'd've": "he would have",
            "he'll": "he will",
            "he'll've": "he will have",
            "he's": "he is",
            "how'd": "how did",
            "how'd'y": "how do you",
            "how'll": "how will",
            "how's": "how is",
            "I'd": "I had",
            "I'd've": "I would have",
            "I'll": "I will",
            "I'll've": "I will have",
            "I'm": "I am",
            "I've": "I have",
            "isn't": "is not",
            "it'd": "it had",
            "it'd've": "it would have",
            "it'll": "it will",
            "it'll've": "it will have",
            "it's": "it is",
            "let's": "let us",
            "ma'am": "madam",
            "mayn't": "may not",
            "might've": "might have",
            "mightn't": "might not",
            "mightn't've": "might not have",
            "must've": "must have",
            "mustn't": "must not",
            "mustn't've": "must not have",
            "needn't": "need not",
            "needn't've": "need not have",
            "o'clock": "of the clock",
            "oughtn't": "ought not",
            "oughtn't've": "ought not have",
            "shan't": "shall not",
            "sha'n't": "shall not",
            "shan't've": "shall not have",
            "she'd": "she had",
            "she'd've": "she would have",
            "she'll": "she will",
            "she'll've": "she will have",
            "she's": "she is",
            "should've": "should have",
            "shouldn't": "should not",
            "shouldn't've": "should not have",
            "so've": "so have",
            "so's": "so is",
            "that'd": "that would",
            "that'd've": "that would have",
            "that's": "that is",
            "there'd": "there would",
            "there'd've": "there would have",
            "there's": "there is",
            "they'd": "they would",
            "they'd've": "they would have",
            "they'll": "they will",
            "they'll've": "they will have",
            "they're": "they are",
            "they've": "they have",
            "to've": "to have",
            "wasn't": "was not",
            "we'd": "we would",
            "we'd've": "we would have",
            "we'll": "we will",
            "we'll've": "we will have",
            "we're": "we are",
            "we've": "we have",
            "weren't": "were not",
            "what'll": "what will",
            "what'll've": "what will have",
            "what're": "what are",
            "what's": "what is",
            "what've": "what have",
            "when's": "when is",
            "when've": "when have",
            "where'd": "where did",
            "where's": "where is",
            "where've": "where have",
            "who'll": "who will",
            "who'll've": "who will have",
            "who's": "who is",
            "who've": "who have",
            "why's": "why is",
            "why've": "why have",
            "will've": "will have",
            "won't": "will not",
            "won't've": "will not have",
            "would've": "would have",
            "wouldn't": "would not",
            "wouldn't've": "would not have",
            "y'all": "you all",
            "y'all'd": "you all would",
            "y'all'd've": "you all would have",
            "y'all're": "you all are",
            "y'all've": "you all have",
            "you'd": "you had",
            "you'd've": "you would have",
            "you'll": "you will",
            "you'll've": "you will have",
            "you're": "you are",
            "you've": "you have"}
    merged_contractions = contractions_list.copy()
    merged_contractions.update(new_contractions_list)

    if type(text) is str:
        text = contractions.fix(text)
        for key in merged_contractions:
            value = merged_contractions[key]
            text = text.replace(key,value)
        return text
    else:
        return text

def _get_lower_case(text: str) -> str:
    """
    Convert all uppercase characters in the input string to lowercase.

    Parameters:
       - text (str): The input string to convert.
        
    Returns:
       - str: The input string with all uppercase characters converted to lowercase.
        
    Example:
        >>> get_lower_case("HeLLo WoRLd!")
        'hello world!'
    """
    return text.lower()


def _get_emails(text: str) -> Tuple[int, List[str]]:
    """
    Extract email addresses from the input string.

    Args:
        text (str):
            The input string to extract email addresses from.

    Returns:
        tuple:
            A tuple containing two elements:
                - An integer representing the total number of unique email addresses found in the input string.
                - A list of strings representing each of the unique email addresses found in the input string.

    Example:
        >>> text = "Please contact me at john@example.com or jane.doe@gmail.com"
        >>> get_emails(text)
        (2, ['john@example.com', 'jane.doe@gmail.com'])

    Notes:
        - This function uses regular expressions to find email addresses in the input string. The regular expression used should match most common email formats, but may not match some less common formats.
        - If the input string contains non-email strings that appear similar to email addresses, they may be mistakenly identified as email addresses by this function.
    """
    emails = re.findall('[\w.\-\+]+@[\w.\-\+]+\.[a-z]{2,}', text)
    email_count = len(set(emails))
    email_list = list(set(emails))

    return email_count, email_list

def _remove_emails(text: str) -> str:
    """
    Removes all email addresses from the input string.

    Args:
        text (str):
            The input string to remove email addresses from.

    Returns:
        str:
            A new string with all email addresses removed.

    Example:
        >>> text = "Please contact me at john@example.com or jane.doe@gmail.com"
        >>> remove_emails(text)
        "Please contact me at  or "

    Notes:
        - This function uses regular expressions to identify and remove email addresses from the input string.
          The regular expression used should match most common email formats, but may not match some less common formats.
        - If the input string contains non-email strings that appear similar to email addresses,
          they may be mistakenly identified as email addresses by this function and removed.
    """
    return re.sub('[\w.\-\+]+@[\w.\-\+]+\.[a-z]{2,}', '', text)


def _get_urls(text: str) -> Tuple[int, List[str]]:
    """
    Extracts all URLs from the given string and returns them as a tuple.

    Args:
        text (str):
            The input string to extract URLs from.

    Returns:
        tuple:
            A tuple containing two elements:
                - An integer representing the total number of unique URLs found in the input string.
                - A list of strings representing each of the unique URLs found in the input string.

    Example:
        >>> text = "Please visit our website at https://www.example.com or http://example.org/index.html"
        >>> get_urls(text)
        (2, ['https://www.example.com', 'http://example.org/index.html'])

    Notes:
        - This function uses regular expressions to identify URLs in the input string.
          The regular expression used is designed to match most common URL formats, but may not match some less common formats.
        - The returned URLs are limited to those that begin with either "http", "https", "ssh", or "ftp".
        - If the input string contains non-URL strings that appear similar to URLs,
          they may be mistakenly identified as URLs by this function.
    """
    urls = re.findall('(?:https|http|ssh|ftp)://\S+', text)
    url_counts = len(set(urls))
    url_list = list(set(urls))

    return url_counts, url_list


def _remove_urls(text: str) -> str:
    """
    Removes all URLs from the input string.

    Args:
        text (str):
            The input string to remove URLs from.

    Returns:
        str:
            A new string with all URLs removed.

    Example:
        >>> text = "Please visit our website at https://www.example.com or http://example.org/index.html"
        >>> remove_urls(text)
        "Please visit our website at  or "

    Notes:
        - This function uses regular expressions to identify and remove URLs from the input string.
          The regular expression used is designed to match most common URL formats, but may not match some less common formats.
        - If the input string contains non-URL strings that appear similar to URLs,
          they may be mistakenly identified as URLs by this function and removed.
    """
    return re.sub(r'(?:https|http|ssh|ftp)://\S+', '', text)



def _remove_rt(text: str) -> str:
    """
    Removes all instances of "RT" (retweet) from the input string.

    Args:
        text (str):
            The input string to remove "RT" instances from.

    Returns:
        str:
            A new string with all "RT" instances removed.

    Example:
        >>> text = "RT @john_doe: Check out this article!"
        >>> remove_rt(text)
        " @john_doe: Check out this article!"

    Notes:
        - This function uses regular expressions to identify and remove instances of "RT" from the input string.
          The regular expression used is designed to match most common variations of "RT", such as in tweets or social media posts.
        - If the input string contains non-"RT" strings that appear similar to "RT",
          they may be mistakenly identified as "RT" by this function and removed.
    """
    return re.sub(r'\brt\b', '', text)



def _remove_special_characters(text: str) -> str:
    """
    Removes all special characters from the input string.

    Args:
        text (str):
            The input string to remove special characters from.

    Returns:
        str:
            A new string with all special characters removed.

    Example:
        >>> text = "Here are some special characters: !#$%&*+-/<=>?@[]^_`{|}~"
        >>> remove_special_characters(text)
        "Here are some special characters "

    Notes:
        - This function uses regular expressions to identify and remove special characters from the input string.
          The regular expression used matches any character that is not a word character or whitespace,
          including punctuation, symbols, and other non-letter/digit characters.
        - If the input string contains non-special characters that are not letters or digits,
          they may be mistakenly identified as special characters by this function and removed.
    """
    return re.sub(r'[^\w\s]', '', text)



def _remove_multiple_whitespaces(text: str) -> str:
    """
    Removes all multiple consecutive whitespaces from the input string.

    Args:
        text (str):
            The input string to remove multiple consecutive whitespaces from.

    Returns:
        str:
            A new string with all multiple consecutive whitespaces removed.

    Example:
        >>> text = "This      string has   too many      spaces"
        >>> remove_multiple_whitespaces(text)
        "This string has too many spaces"

    Notes:
        - This function uses regular expressions to identify and remove multiple consecutive whitespaces from the input string.
          The regular expression used matches one or more consecutive whitespace characters,
          including spaces, tabs, line breaks, and other whitespace characters.
        - If the input string contains non-whitespace strings that appear similar to whitespace,
          they may be mistakenly identified as whitespace by this function and removed.
        - The resulting string will also have any leading or trailing whitespaces removed by using the built-in method "strip()".
    """
    return re.sub(r'\s+', ' ', text).strip()


def _remove_html_tags(text: str) -> str:
    """
    Removes HTML tags from the input text string and returns a cleaned version.

    Args:
        text: A string containing HTML code and/or plain text to be cleaned.

    Returns:
        A string with all HTML tags removed from the input text.
        

    Examples:
        >>> text = "<p>This is an example <b>HTML</b> text.</p>"
        >>> remove_html_tags(text)
        'This is an example HTML text.'
    """
    return BeautifulSoup(text,'lxml').get_text().strip()


def _remove_accented_chars(text: str) -> str:
    """
    Removes accented characters (such as é, ç, ü) from the input text string and replaces them with their ASCII equivalents.

    Args:
        text: A string containing accented characters to be replaced with their ASCII equivalents.

    Returns:
        A cleaned version of the input text string with all accented characters removed and replaced by their ASCII equivalents.


    Examples:
        >>> text = "L'été est une saison agréable pour se promener dans la nature."
        >>> remove_accented_chars(text)
        "L'ete est une saison agreable pour se promener dans la nature."

        >>> text = "El niño juega en el jardín con un pequeño perro."
        >>> remove_accented_chars(text)
        "El nino juega en el jardin con un pequeno perro."
    """
    text = unicodedata.normalize('NFKD',text).encode('ascii','ignore').decode('utf-8','ignore')
    return text


def _remove_stopwords(text: str) -> str:
    """
    Removes stop words from the input text string and returns a cleaned version.

    Args:
        text (str): The input text string containing stop words to be removed.

    Returns:
        str: A cleaned version of the input text string with all stop words removed.

    Example:
        >>> text = "The quick brown fox jumps over the lazy dog."
        >>> remove_stopwords(text)
        'quick brown fox jumps lazy dog.'

        >>> text = "In the summer, we like to swim in the cool water."
        >>> remove_stopwords(text)
        'summer, like swim cool water.'
    """

    return ' '.join([word for word in text.split() if word.lower() not in stopwords])



def _lemmatize_text(text: str) -> str:
    """
    Lemmatizes the input text string using the spaCy library and returns the lemmatized version.

    Args:
        text (str): The input text string to be lemmatized.

    Returns:
        str: The lemmatized version of the input text string.

    Raises:
        None

    Examples:
        >>> lemmatize_text("I am running in the park")
        'I be run in the park'
        
        >>> lemmatize_text("The quick brown foxes are jumping over the lazy dog")
        'the quick brown fox be jump over the lazy dog'
        
        >>> lemmatize_text("My cat is sleeping on the couch")
        'my cat be sleep on the couch'
    """

    # Process the input text string with the pipeline to obtain a spaCy Doc object
    doc = nlp(text)

    # Iterate over each token in the Doc object and lemmatize it, storing it in a list
    lemmas = [token.lemma_ if token.lemma_ not in ['-PRON-', 'be'] else token.text for token in doc]

    # Join the lemmatized tokens back into a string and return it
    return ' '.join(lemmas)


def _get_value_counts(df: pd.DataFrame, col: str) -> pd.Series:
    """
    Returns a pandas Series containing the frequency count of each value in a specified column of a DataFrame.

    Args:
        df: A pandas DataFrame.
        col: A string representing the name of the column to be analyzed.

    Returns:
        A pandas Series containing the frequency count of each value in the specified column.

    Example 1:
        >>> import pandas as pd
        >>> data = {'name': ['Alice', 'Bob', 'Charlie', 'Alice', 'David']}
        >>> df = pd.DataFrame(data)
        >>> get_value_counts(df, 'name')
        Alice      2
        Bob        1
        Charlie    1
        David      1
        dtype: int64

    Example 2:
        >>> data = {'fruit': ['apple', 'banana', 'cherry', 'apple', 'apple', 'banana', 'date', 'elderberry']}
        >>> df = pd.DataFrame(data)
        >>> get_value_counts(df, 'fruit')
        apple         3
        banana        2
        cherry        1
        date          1
        elderberry    1
        dtype: int64
    """
    
    # Combine all rows of the specified column into a single string
    text = ' '.join(df[col])
    
    # Split the string into a list of words
    text = text.split()
    
    # Count the frequency of each word and return the results as a pandas Series
    frequency_count = pd.Series(text).value_counts()
    
    return frequency_count


def _remove_common_word(text: str, freq: pd.Series, n: int = 20) -> str:
    """
    Removes the most common words from a text string and returns the modified string.
    
    Args:
        text (str): The input text string.
        freq (pd.Series): A pandas series containing word frequencies.
        n (int): The number of most common words to remove. Default is 20.
        
    Returns:
        str: The modified input text string with the most common words removed.
    
    Example:
        >>> import pandas as pd
        >>> freq = pd.Series({'the': 100, 'and': 50, 'to': 30, 'a': 20, 'in': 15})
        >>> text = "The quick brown fox jumps over the lazy dog"
        >>> filtered_text = remove_common_word(text, freq, 2)
        >>> print(filtered_text)
        quick brown fox jumps over lazy dog
    """
    # Get the top n most frequent words
    top_n = freq[:n]
    # Convert the words to lowercase for case insensitivity
    top_n = [word.lower() for word in top_n.index]
    
    # Split the input text into individual words and remove the top n most frequent words
    filtered_words = [word for word in text.split() if word.lower() not in top_n]
    
    # Join the remaining words back into a single string and return it
    filtered_text = ' '.join(filtered_words)
    
    return filtered_text


def _remove_rarewords(text: str, freq: pd.Series, n: int = 20) -> str:
    """
    Returns the input text with the 'n' rarest words removed based on their frequency distribution.

    Args:
        text (str): The input text to be processed.
        freq (pd.Series): A Pandas Series containing the frequency count of each word in the text corpus.
        n (int, optional): The number of rarest words to be removed from the text. Defaults to 20.

    Returns:
        str: The processed text with rare words removed.

    Examples:
        >>> import pandas as pd
        >>> freq = pd.Series({'the': 100, 'and': 50, 'a': 25, 'of': 10, 'it': 5})
        >>> text = 'The quick brown fox jumps over a lazy dog. It is one of the wonders of the world.'
        >>> remove_rarewords(text, freq, 2)
        'The quick brown fox jumps over lazy dog. is one wonders world.'
    """
    
    # Get the n rarest words based on their frequency distribution
    rare_n = freq.tail(n)
    # Convert the words to lowercase for case insensitivity
    rare_n = [word.lower() for word in rare_n.index]
    
    # Remove the rare words from the text
    cleaned_text = ' '.join([word for word in text.split() if word not in rare_n])

    return cleaned_text


def _get_spelling_correction(text: str) -> str:
    """
    This function takes in a string 'text' and returns the spelling-corrected version of the same text using TextBlob library.

    Args:
    - text (str): The input string to be spelling-corrected

    Returns:
    - (str): The spelling-corrected version of the input text
    
    Example:
    >>> get_spelling_correction("teh cat iz on teh mat")
    'the cat is on the mat'
    
    """
    return TextBlob(text).correct()




