def only_sei(kanji):
    """
    1.70% (35/2059)
    """
    return "せい"


RADICAL_MAP = {"肉": "わん"}


def radical(kanji):
    """
    1.75% (36/2059)
    """
    guess = RADICAL_MAP.get(kanji.radical, "せい")
    return guess
