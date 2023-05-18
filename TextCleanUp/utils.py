import re 
import os
import sys
import json
import contractions
import numpy as np
import pandas as pd
import spacy
from typing import List, Tuple, Union
from bs4 import BeautifulSoup
import unicodedata
from textblob import TextBlob

from spacy.lang.en.stop_words import STOP_WORDS as stopwords
stopwords.discard('not')

nlp = spacy.load('en_core_web_sm')

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

abbreviations ={
    "₹" : "rupee",
    "€" : "euro",
    "¥" : "yen",
    "$" : "dollar",
    "4ao" : "for adults only",
    "a.m" : "before midday",
    "a3" : "anytime anywhere anyplace",
    "aamof" : "as a matter of fact",
    "acct" : "account",
    "adih" : "another day in hell",
    "afaic" : "as far as i am concerned",
    "afaict" : "as far as i can tell",
    "afaik" : "as far as i know",
    "afair" : "as far as i remember",
    "afk" : "away from keyboard",
    "app" : "application",
    "approx" : "approximately",
    "apps" : "applications",
    "asap" : "as soon as possible",
    "asl" : "age, sex, location",
    "atk" : "at the keyboard",
    "ave." : "avenue",
    "aymm" : "are you my mother",
    "ayor" : "at your own risk", 
    "b&b" : "bed and breakfast",
    "b+b" : "bed and breakfast",
    "b.c" : "before christ",
    "b2b" : "business to business",
    "b2c" : "business to customer",
    "b4" : "before",
    "b4n" : "bye for now",
    "b@u" : "back at you",
    "bae" : "before anyone else",
    "bak" : "back at keyboard",
    "bbbg" : "bye bye be good",
    "bbc" : "british broadcasting corporation",
    "bbias" : "be back in a second",
    "bbl" : "be back later",
    "bbs" : "be back soon",
    "be4" : "before",
    "bfn" : "bye for now",
    "blvd" : "boulevard",
    "bout" : "about",
    "brb" : "be right back",
    "bros" : "brothers",
    "brt" : "be right there",
    "bsaaw" : "big smile and a wink",
    "btw" : "by the way",
    "bwl" : "bursting with laughter",
    "c/o" : "care of",
    "cet" : "central european time",
    "cf" : "compare",
    "cia" : "central intelligence agency",
    "csl" : "can not stop laughing",
    "cu" : "see you",
    "cul8r" : "see you later",
    "cv" : "curriculum vitae",
    "cwot" : "complete waste of time",
    "cya" : "see you",
    "cyt" : "see you tomorrow",
    "dae" : "does anyone else",
    "dbmib" : "do not bother me i am busy",
    "diy" : "do it yourself",
    "dm" : "direct message",
    "dwh" : "during work hours",
    "e123" : "easy as one two three",
    "eet" : "eastern european time",
    "eg" : "example",
    "embm" : "early morning business meeting",
    "encl" : "enclosed",
    "encl." : "enclosed",
    "etc" : "and so on",
    "faq" : "frequently asked questions",
    "fawc" : "for anyone who cares",
    "fb" : "facebook",
    "fc" : "fingers crossed",
    "fig" : "figure",
    "fimh" : "forever in my heart", 
    "ft." : "feet",
    "ft" : "featuring",
    "ftl" : "for the loss",
    "ftw" : "for the win",
    "fwiw" : "for what it is worth",
    "fyi" : "for your information",
    "g9" : "genius",
    "gahoy" : "get a hold of yourself",
    "gal" : "get a life",
    "gcse" : "general certificate of secondary education",
    "gfn" : "gone for now",
    "gg" : "good game",
    "gl" : "good luck",
    "glhf" : "good luck have fun",
    "gmt" : "greenwich mean time",
    "gmta" : "great minds think alike",
    "gn" : "good night",
    "g.o.a.t" : "greatest of all time",
    "goat" : "greatest of all time",
    "goi" : "get over it",
    "gps" : "global positioning system",
    "gr8" : "great",
    "gratz" : "congratulations",
    "gyal" : "girl",
    "h&c" : "hot and cold",
    "hp" : "horsepower",
    "hr" : "hour",
    "hrh" : "his royal highness",
    "ht" : "height",
    "ibrb" : "i will be right back",
    "ic" : "i see",
    "icq" : "i seek you",
    "icymi" : "in case you missed it",
    "idc" : "i do not care",
    "idgadf" : "i do not give a damn fuck",
    "idgaf" : "i do not give a fuck",
    "idk" : "i do not know",
    "ie" : "that is",
    "i.e" : "that is",
    "ifyp" : "i feel your pain",
    "IG" : "instagram",
    "iirc" : "if i remember correctly",
    "ilu" : "i love you",
    "ily" : "i love you",
    "imho" : "in my humble opinion",
    "imo" : "in my opinion",
    "imu" : "i miss you",
    "iow" : "in other words",
    "irl" : "in real life",
    "j4f" : "just for fun",
    "jic" : "just in case",
    "jk" : "just kidding",
    "jsyk" : "just so you know",
    "l8r" : "later",
    "lb" : "pound",
    "lbs" : "pounds",
    "ldr" : "long distance relationship",
    "lmao" : "laugh my ass off",
    "lmfao" : "laugh my fucking ass off",
    "lol" : "laughing out loud",
    "ltd" : "limited",
    "ltns" : "long time no see",
    "m8" : "mate",
    "mf" : "motherfucker",
    "mfs" : "motherfuckers",
    "mfw" : "my face when",
    "mofo" : "motherfucker",
    "mph" : "miles per hour",
    "mr" : "mister",
    "mrw" : "my reaction when",
    "ms" : "miss",
    "mte" : "my thoughts exactly",
    "nagi" : "not a good idea",
    "nbc" : "national broadcasting company",
    "nbd" : "not big deal",
    "nfs" : "not for sale",
    "ngl" : "not going to lie",
    "nhs" : "national health service",
    "nrn" : "no reply necessary",
    "nsfl" : "not safe for life",
    "nsfw" : "not safe for work",
    "nth" : "nice to have",
    "nvr" : "never",
    "nyc" : "new york city",
    "oc" : "original content",
    "og" : "original",
    "ohp" : "overhead projector",
    "oic" : "oh i see",
    "omdb" : "over my dead body",
    "omg" : "oh my god",
    "omw" : "on my way",
    "p.a" : "per annum",
    "p.m" : "after midday",
    "pm" : "prime minister",
    "poc" : "people of color",
    "pov" : "point of view",
    "pp" : "pages",
    "ppl" : "people",
    "prw" : "parents are watching",
    "ps" : "postscript",
    "pt" : "point",
    "ptb" : "please text back",
    "pto" : "please turn over",
    "qpsa" : "what happens",
    "ratchet" : "rude",
    "rbtl" : "read between the lines",
    "rlrt" : "real life retweet", 
    "rofl" : "rolling on the floor laughing",
    "roflol" : "rolling on the floor laughing out loud",
    "rotflmao" : "rolling on the floor laughing my ass off",
    "rt" : "retweet",
    "ruok" : "are you ok",
    "sfw" : "safe for work",
    "sk8" : "skate",
    "smh" : "shake my head",
    "sq" : "square",
    "srsly" : "seriously", 
    "ssdd" : "same stuff different day",
    "tbh" : "to be honest",
    "tbs" : "tablespooful",
    "tbsp" : "tablespooful",
    "tfw" : "that feeling when",
    "thks" : "thank you",
    "tho" : "though",
    "thx" : "thank you",
    "tia" : "thanks in advance",
    "til" : "today i learned",
    "tl;dr" : "too long i did not read",
    "tldr" : "too long i did not read",
    "tmb" : "tweet me back",
    "tntl" : "trying not to laugh",
    "ttyl" : "talk to you later",
    "u" : "you",
    "u2" : "you too",
    "u4e" : "yours for ever",
    "utc" : "coordinated universal time",
    "w/" : "with",
    "w/o" : "without",
    "w8" : "wait",
    "wassup" : "what is up",
    "wb" : "welcome back",
    "wtf" : "what the fuck",
    "wtg" : "way to go",
    "wtpa" : "where the party at",
    "wuf" : "where are you from",
    "wuzup" : "what is up",
    "wywh" : "wish you were here",
    "yd" : "yard",
    "ygtr" : "you got that right",
    "ynk" : "you never know",
    "zzz" : "sleeping bored and tired",
	"to've": "to have",
	"wasn't": "was not",
	"ur": "your",
	"n": "and",
	"won't": "would not",
	"dis": "this",
	"brng": "bring"
}

merged_contractions = contractions_list.copy()
merged_contractions.update(new_contractions_list)

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
    word_count = len(str(text).split())
    return word_count


def _get_char_count(text: str, char_count_with_whitespace=False) -> int:
    """
    This function takes a string as input and returns the count of non-whitespace characters in the string.
    
    Args:
        text (str): The input string for which non-whitespace character count is to be calculated.
        char_count_with_whitespace (bool, optional): If True, the function will return the total number
            of characters in the input string including whitespace. Default is False.

    Returns:
        int: The count of non-whitespace characters in the input string if `char_count_with_whitespace` is False.
             The total count of characters in the input string if `char_count_with_whitespace` is True.
    
    Example:
        >>> _get_char_count('The quick brown fox jumps over the lazy dog.')
        32
        >>> _get_char_count('The quick brown fox jumps over the lazy dog.', True)
        43
    
    Explanation:
        The regular expression '\s+' matches one or more whitespace characters including space, tab, newline, carriage return, etc.
        The 're.sub' function replaces all matching substrings with an empty string thereby removing them from the input string.
        The length of the resulting string gives us the count of non-whitespace characters in the input string.
        
        If `char_count_with_whitespace` is True, then simply return the length of the input string without any processing.
    """
    if char_count_with_whitespace:
        char_count = len(str(text))
        return char_count
    else:
        char_count = len(re.sub('\s+', "", str(text)))
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
    avg_wordlength = _get_char_count(str)/_get_word_count(str(text))
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
    words = [word.lower() for word in str(text).split()]

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
    hashtag_count = len(re.findall("#+\S+",str(text)))
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
    mentions_count = len(re.findall("@+\S+", str(text)))
    
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
    digit_count = len(re.findall(r'\b\d+\b', str(text)))
    
    return digit_count

def _get_uppercase_word_count(text:str, get_count_and_uppercase_words=False,get_only_uppercase_words=False) -> Union[int, Tuple[int,List[str]], List[str]]:
    """
    This function takes a string as input and returns the count of uppercase words in it.
    
    Parameters:
    - text (str): A string containing words
    
    Optional Parameters:
    - get_count_and_uppercase_words (bool): If True, returns a tuple consisting of the count of uppercase words and a list of the uppercase words. Default is False.
    - get_only_uppercase_words (bool): If True, returns a list of only the uppercase words found in the input text. Default is False.
    
    Returns:
    - An integer representing the count of uppercase words in the input text.
    - If `get_count_and_uppercase_words` is True, returns a tuple with the count of uppercase words and a list of uppercase words found in the input text.
    - If `get_only_uppercase_words` is True, returns a list of the uppercase words found in the input text.
    
    Example:
    >>> _get_uppercase_word_count("Hello WORLD! HOW are You?")
    2
    
    To get both the count of uppercase words and the uppercase words list:
    >>> _get_uppercase_word_count("Hello WORLD! HOW are You?", get_count_and_uppercase_words=True)
    (2, ['HELLO', 'WORLD', 'HOW', 'YOU'])
    
    To get only the uppercase words list:
    >>> _get_uppercase_word_count("Hello WORLD! HOW are You?", get_only_uppercase_words=True)
    ['HELLO', 'WORLD', 'HOW', 'YOU']
    """
    # The regex used here is \b[A-Z]+\b
    # \b matches word boundaries
    # [A-Z]+ matches one or more consecutive uppercase letters
    # So, the regex matches all the uppercase words in the text
    
    upper_case_words = re.findall(r'\b[A-Z]+\b',str(text))
    uppercase_word_count = len(upper_case_words)
    
    if get_count_and_uppercase_words:
        return (uppercase_word_count,upper_case_words)
    
    elif get_only_uppercase_words:
        return upper_case_words
    
    else:
        return uppercase_word_count
    
def _get_expand_abbreviations(text: str, abbreviations: dict=abbreviations) -> str:
    """
    Replaces all abbreviations in the given text with their expanded forms from the provided dictionary or the custom
    dictionary if provided by the user.
    Args:
       - text (str): The input text to expand abbreviations in.
       - abbreviations (dict, optional): A dictionary containing abbreviations and their corresponding expansions.
                                        Defaults to the pre-defined 'abbreviations' dictionary.

    Returns:
        str: The text with all abbreviations expanded.

    Examples:
        >>> abbreviations = {"btw": "by the way", "irl": "in real life"}
        >>> text = "I met him irl btw"
        >>> expand_abbreviations(text, abbreviations)
        'I met him in real life by the way'

        >>> abbreviations = {"lol": "laughing out loud", "btw": "by the way", "idk": "I do not know"}
        >>> text = "I have no idea what he meant lol btw idk"
        >>> expand_abbreviations(text, abbreviations)
        'I have no idea what he meant laughing out loud by the way I do not know'
    """
    # Split the text into tokens using whitespace as separator
    tokens = text.split()
    # Iterate over each token and replace it with its expansion if it is an abbreviation
    for i in range(len(tokens)):
        if tokens[i] in abbreviations:
            tokens[i] = abbreviations[tokens[i]]
    # Join the expanded tokens back into a string and return it
    return ' '.join(tokens)


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
    
    text = str(text)
    text = contractions.fix(text)
    text = _get_expand_abbreviations(text)
    for key in merged_contractions:
        value = merged_contractions[key]
        text = text.replace(key,value)
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
    return str(text).lower()


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
    emails = re.findall('[\w.\-\+]+@[\w.\-\+]+\.[a-z]{2,}', str(text))
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
    return re.sub('[\w.\-\+]+@[\w.\-\+]+\.[a-z]{2,}', '', str(text))


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
    urls = re.findall('(?:https|http|ssh|ftp)://\S+', str(text))
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
    return re.sub(r'(?:https|http|ssh|ftp)://\S+', '', str(text))



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
    return re.sub(r'\brt\b', '', str(text))



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
    return re.sub(r'[^\w\s]', '', str(text))



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
    return re.sub(r'\s+', ' ', str(text)).strip()


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
    return BeautifulSoup(str(text),'html.parser').get_text().strip()


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
    text = unicodedata.normalize('NFKD',str(text)).encode('ascii','ignore').decode('utf-8','ignore')
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

    return ' '.join([word for word in str(text).split() if word.lower() not in stopwords])



def _get_lemmatize_text(text: str) -> str:
    """
    Lemmatizes the input text string using the spaCy library and returns the lemmatized version.

    Args:
        text (str): The input text string to be lemmatized.

    Returns:
        str: The lemmatized version of the input text string.

    Examples:
        >>> lemmatize_text("I am running in the park")
        'I be run in the park'
        
        >>> lemmatize_text("The quick brown foxes are jumping over the lazy dog")
        'the quick brown fox be jump over the lazy dog'
        
        >>> lemmatize_text("My cat is sleeping on the couch")
        'my cat be sleep on the couch'
    """

    # Process the input text string with the pipeline to obtain a spaCy Doc object
    text = str(text)
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
    filtered_words = [word for word in str(text).split() if word.lower() not in top_n]
    
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
    cleaned_text = ' '.join([word for word in str(text).split() if word not in rare_n])

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
    return TextBlob(str(text)).correct()

def _remove_repeated_chars(text: str) -> str:
    """Removes repeated characters from a string.

    Args:
        text (str): The input string to modify.

    Returns:
        str: The modified string with all repeated characters removed.

    Examples:
        >>> remove_repeated_chars("hello")
        'helo'

        >>> remove_repeated_chars("The meeting was scheduled for Tuesday at 10am.")
        'The meting was scheduled for Tuesday at 10am.'

        >>> remove_repeated_chars("Mississippi")
        'Misisipi.'

    Regex Steps:
    -------------
    Here are the steps involved in applying this regex to a string:

    1. The re.sub() function takes the pattern and replacement string as arguments, along with the input string.
    2. The pattern r"(.)\1+" searches for any character that is repeated one or more times in a row. For example, if the input string is "hello", the pattern will match "ll" because it consists of the same character repeated twice.
    3. The pattern uses a backreference \1 to refer to the first captured group (the single character in parentheses). This ensures that the replacement only removes repeated instances of the same character.
    4. The replacement string r"\1" replaces the matched substring (e.g., "ll") with the first captured group (e.g., "l"). This effectively removes the repeated characters, leaving only one instance of each character in the final output.
    5. The re.sub() function returns the modified string with all repeated characters removed.
    """
    # pattern = r"(.)\1+"  # Matches any character repeated one or more times
    pattern = "(.)\\1{2,}"  # Matches any character repeated two or more times
    repl = "\\1"  # Replaces the match with the first (and only) captured group
    return re.sub(pattern, repl, str(text))

def _get_complete_text_clean_up(text: str, 
                                lower_case=True,
                                contraction_to_expansion=True,
                                spelling_correction=False,
                                remove_accented_chars=True,
                                remove_emails=True,
                                remove_urls=True,
                                remove_html_tags=True,
                                remove_rt=False,
                                remove_stopwords=True,
                                remove_special_characters=True,
                                lemmatize_text=True,
                                remove_multiple_whitespaces=True,
                                remove_repeated_chars=False) -> str:
    """
    This function takes in a string of text and performs a series of text cleaning operations on it. The cleaning operations include lowercasing, expanding contractions, optional spelling correction, removing accented characters, emails, URLs, HTML tags, RT (retweet) mentions, stopwords, special characters, lemmatization, and multiple whitespaces. 

    Args:
        text (str): A string of text to be cleaned up.
        lower_case (bool): Flag to enable lowercasing. Default is True.
        contraction_to_expansion (bool): Flag to enable contraction expansion. Default is True.
        spelling_correction (bool): Flag to enable spelling correction. Default is False.
        remove_accented_chars (bool): Flag to enable removal of accented characters. Default is True.
        remove_emails (bool): Flag to enable removal of email addresses. Default is True.
        remove_urls (bool): Flag to enable removal of URLs. Default is True.
        remove_html_tags (bool): Flag to enable removal of HTML tags. Default is True.
        remove_rt (bool): Flag to enable removal of retweets. Default is False.
        remove_stopwords (bool): Flag to enable removal of stopwords. Default is True.
        remove_special_characters (bool): Flag to enable removal of special characters. Default is True.
        lemmatize_text (bool): Flag to enable lemmatization. Default is True.
        remove_multiple_whitespaces (bool): Flag to enable removal of multiple whitespaces. Default is True.
        remove_repeated_chars (bool): Flag to enable removal of repeated characters. Default is False.

    Returns:
        str: A cleaned-up version of the input text.

    Example:
        _get_complete_text_clean_up("Hi, I'm leaning #DataScience and #MachineLearning what do you thing Im doing right ?")
        'hi learn datascience machinelearning thing right'
    """
    text = str(text)
    if lower_case:
        text = _get_lower_case(text)
    
    if remove_repeated_chars:
        text = _remove_repeated_chars(text)

    if contraction_to_expansion:
        text = _get_contraction_to_expansion(text)

    if spelling_correction:
        text = str(_get_spelling_correction(text))

    if remove_accented_chars:
        text = _remove_accented_chars(text)

    if remove_emails:
        text = _remove_emails(text)

    if remove_urls:
        text = _remove_urls(text)

    if remove_html_tags:
        text = _remove_html_tags(text)

    if remove_rt:
        text = _remove_rt(text)

    if remove_stopwords:
        text = _remove_stopwords(text)

    if remove_special_characters:
        text = _remove_special_characters(text)

    if lemmatize_text:
        text = _get_lemmatize_text(text)

    if remove_multiple_whitespaces:
        text = _remove_multiple_whitespaces(text)

    return text

def _get_basic_features(df: pd.core.frame.DataFrame,
                        col: str, 
                        get_char_count: bool = True,
                        get_word_count: bool = True, 
                        get_avg_wordlength: bool = True,
                        get_stopwords_count: bool = True, 
                        get_hashtag_count: bool = True,
                        get_mentions_count: bool = True, 
                        get_digit_count: bool = True,
                        get_uppercase_word_count: bool = True) -> pd.core.frame.DataFrame:
    """
    Computes basic text features for a given column in a Pandas DataFrame.
    Features that this function calculate :
       - Character count
       - Word count
       - Average word length
       - Stopwords count
       - Hashtag count
       - Mentions count
       - Digit count
       - Uppercase word count

    Args:
        df: The input DataFrame.
        col: The name of the column containing the text data.
        get_char_count: If True, computes the character count. Default is True.
        get_word_count: If True, computes the word count. Default is True.
        get_avg_wordlength: If True, computes the average word length. Default is True.
        get_stopwords_count: If True, computes the stopwords count. Default is True.
        get_hashtag_count: If True, computes the hashtag count. Default is True.
        get_mentions_count: If True, computes the mentions count. Default is True.
        get_digit_count: If True, computes the digit count. Default is True.
        get_uppercase_word_count: If True, computes the uppercase word count. Default is True.

    Returns:
        A new DataFrame with the added text features.
    """
    if type(df) == pd.core.frame.Dataframe:
        if get_char_count:    
            df['char_counts'] = df[col].apply(_get_char_count)
        if get_word_count:
            df['word_counts'] = df[col].apply(_get_word_count)
        if get_avg_wordlength:
            df['avg_wordlength'] = df[col].apply(_get_avg_wordlength)
        if get_stopwords_count:
            df['stopwords_counts'] = df[col].apply(_get_stopwords_count)
        if get_hashtag_count:
            df['hashtag_counts'] = df[col].apply(_get_hashtag_count)
        if get_mentions_count:
            df['mention_counts'] = df[col].apply(_get_mentions_count)
        if get_digit_count:
            df['digit_counts'] = df[col].apply(_get_digit_count)
        if get_uppercase_word_count:
            df['uppercase_counts'] = df[col].apply(_get_uppercase_word_count)
        
        return df
    else:
        print('ERROR: This function takes only Pandas DataFrame')


