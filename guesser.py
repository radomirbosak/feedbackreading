def only_sei(kanji):
    """
    1.70% (35/2059)
    """
    return "せい"


RADICAL_MAP = {
    "肉": "わん",
    "水": "わん",
    # "心": "わく",
}


def radical(kanji):
    """
    1.75% (36/2059)
    """
    guess = RADICAL_MAP.get(kanji.radical, "せい")
    return guess


def constant_kou(kanji):
    """
    Best constant predictor.
    See analyze.print_most_common_readings for most common readings
    3.25% (67/2059)
    """
    return "こう"
