import re

import nltk
import textnorm
import unidecode
from nltk.corpus import stopwords

# Import nltk for stopwords

try:
    stop_words = set(stopwords.words("english"))
except LookupError:  # pragma: no cover
    nltk.download("stopwords", quiet=True)
    stop_words = set(stopwords.words("english"))


def strong_normalizer(
    string,
    remove_numbers=True,
    remove_punctuations=True,
    remove_extraspaces=True,
    remove_allspaces=False,
):
    """
    This is a very strong string normalizer that remove almost anything
    except words

    Parameters
    ----------
    string: str
        String to get normalized
    remove_numbers: bool
        If the algorithm should remove numbers (Default: True)
    remove_punctuations: bool
        If the algorithm should remove punctuations symbols (Default: True)
    remove_extraspaces: bool
        If the algorithm should remove spaces (Default: True)
    remove_allspaces: bool
        If the algorithm should remove all spaces (Default: False)

    Return
    ------
    string: str
        String already normalized
    """

    global stop_words

    # Normalize unicode
    string = textnorm.normalize_unicode(string)

    # Normalize spaces
    string = textnorm.normalize_space(string)

    # Apply unidecode to plain string
    string = unidecode.unidecode(string)

    # Lower it
    string = string.lower()

    # Remove numbers
    if remove_numbers:
        string = re.sub(r"\d+", " ", string)

    # Remove all punctuation except words and space
    if remove_punctuations:
        string = re.sub(r"[^\w\s]", "", string)

    # Remove white spaces
    if remove_extraspaces:
        string = string.strip()

    # Convert string to list of words
    lst_string = [string][0].split()

    # Remove stopwords
    clean_string = ""
    for i in lst_string:
        if i not in stop_words:
            clean_string += i + " "

    # Removing last space
    string = clean_string[:-1]

    # Remove all spaces
    if remove_allspaces:
        string = string.replace(" ", "")

    # Return result
    return string
