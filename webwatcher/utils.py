import re


RE_VALID_FILENAME = re.compile(r'(?u)[^-\w.]')


def normalize_filename(text):
    """
    ORIGIN: https://github.com/django/django/blob/master/django/utils/text.py

    Returns the given string converted to a string that can be used for a clean
    filename. Specifically, leading and trailing spaces are removed; other
    spaces are converted to underscores; and anything that is not a unicode
    alphanumeric, dash, underscore, or dot, is removed.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    return RE_VALID_FILENAME.sub('', text.strip().replace(' ', '_'))
