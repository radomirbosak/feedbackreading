from ideal_radical_map import ideal_radical_map


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


def smallmap_radical(kanji):
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


def ideal_radical_mapper(kanji):
    """
    Best radical predictor.
    See analyze.most_common_reading_for_radical for human-readable analysis
    Or analyze.print_radical_to_reading_table for resulting table
    14.62% (301/2059)
    """
    return ideal_radical_map[kanji.radical]
