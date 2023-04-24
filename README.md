# TextCleanUp

#### TextCleanUp is a Python package for text preprocessing and cleaning. It provides functions to perform common text processing tasks such as converting text to lowercase, expanding contractions, removing emails and URLs, removing RTs, removing special characters, removing multiple spaces, removing HTML tags, removing accented characters, removing stop words, converting words to their base form, removing common and rare occurring words, generating word clouds, performing spelling correction, tokenization, and lemmatization.

#### The package also includes general feature extraction functions such as word count, character count, average characters per word, stop words count, count of hashtags and mentions, checking if numeric digits are present in tweets, and upper case word counts.

## Installation
To install TextCleanUp, use pip:

```
pip install git+ssh://git@github.com/Suraj-0-0-Yadav/TextCleanUp.git
```

## Uninstallation
To uninstall TextCleanUp, use pip:

```
pip uninstall TextCleanUp
```

## Example

```
#import the package
import TextCleanUp as tcu
```

```
def CompleteTextCleanUp(text):
    text = tcu.get_lower_case(text)
    text = tcu.get_contraction_to_expansion(text)
    text = str(tcu.get_spelling_correction(text))
    text = tcu.remove_accented_chars(text)
    text = tcu.remove_emails(text)
    text = tcu.remove_html_tags(text)
    text = tcu.remove_rt(text)
    text = tcu.remove_stopwords(text)
    text = tcu.remove_urls(text)
    text = tcu.remove_multiple_whitespaces(text)
    text = tcu.remove_special_characters(text)
    return text

>>> CompleteTextCleanUp("Hi, I'm leaning #DataScience and #MachineLearning what do you thing Im doing right ?")
'hi leaning datascience machinelearning thing right'
```