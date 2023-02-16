import re


def collapse_whitespace(text):
    return re.sub(r"\s+", " ", text)


def remove_roman_numerals(text):
    return re.sub(r"[ivxlcdm]{2,}", "", text)


def remove_punctuation(text):
    return re.sub(r"[^\w\s\']", " ", text)
