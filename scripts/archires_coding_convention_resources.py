# -*- coding: utf-8 -*- 

# External import
import re
from unidecode import unidecode

def erase_trailing_slash(path: str):
    """Erase the last character if it's a slash or backslash.

    Return a string."""
    if path[-1:] in ["/", "\\"]:
        return path[:len(path)-1]
    else:
        return path

def define_logger_level(level: str):
    """Returns the logger level for the logging library.

    Defaults to INFO"""
    level = level.strip().upper()
    if level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        return "INFO"
    else:
        return level


def clean_string(_str: str, noise=True, diacritics=True, alphanum_only=False, multispaces=True, to_upper_case=False):
    """Returns a string without punctuation and/or multispaces stripped and in lower case.

    Takes as arguments :
        - _str [mandatory] : the string to edit
        - noise {bool, def True} : remove punctuation ?
        - diacritics {bool, def True} : remove diacritics
        - alphanum_only {bool, def False} : remove all character not in 0-9 a-zA-Z
        - multispaces {bool, def True} : remove multispaces ? (space = regex \s)
        - to_upper_case {bool, def False} : reutnr the string as upper case"""
    
    if noise:
        NOISE_LIST = [".", ",", "?", "!", ";","/",":","="]
        for car in NOISE_LIST:
            _str = _str.replace(car, " ")
    
    if diacritics:
        _str = unidecode(_str)

    if alphanum_only:
        _str = re.sub("[^a-zA-Z\d\s]", "", _str)

    if multispaces:
        _str = re.sub("\s+", " ", _str).strip()

    if to_upper_case:
        return _str.upper()
    return _str.lower()