#!/usr/bin/env python3

import warnings

# import pandas as pd
import numpy as np
from termcolor import colored

from kanji import Kanji

# fix pandas pyarrow warning
warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd


KANJI_LIST = {
    "青": "せい",
    "清": "せい",
    "債": "さい",
}


def load_all_kanji():
    df = pd.read_csv("joyo.csv")
    df = df.replace(np.nan, None)

    return [Kanji.from_series(k) for _, k in df.iterrows()]


allk = load_all_kanji()


def load_kanji_list():
    return KANJI_LIST


# guessing algorithm
def guess_reading(kanji):
    return "せい"


def good(text):
    return colored(text, "light_green")


def bad(text):
    return colored(text, "red", attrs=["bold"])


def main():
    kanji_list = load_kanji_list()
    bad_count, good_count = 0, 0

    for kanji, correct_reading in kanji_list.items():
        guess = guess_reading(kanji)

        if guess == correct_reading:
            print(kanji, good(guess))
            good_count += 1
        else:
            print(kanji, bad(guess), "->", correct_reading)
            bad_count += 1

    print("{:.0%} complete".format(good_count / len(kanji_list)))

    from pprint import pprint

    # pprint(allk)

    for kanji in allk[:10]:
        print(kanji.character, kanji.onyomi)


if __name__ == "__main__":
    main()
