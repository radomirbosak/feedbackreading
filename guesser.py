def only_sei(kanji):
    """1.70%"""
    return "せい"


RADICAL_MAP = {"肉": "わん"}


def radical(kanji):
    """1.75%"""
    guess = RADICAL_MAP.get(kanji.radical, "せい")
    return guess
