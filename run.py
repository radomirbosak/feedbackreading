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
    return load_all_kanji()


# guessing algorithm
def guess_reading(kanji):
    return "せい"


def good(text):
    return colored(text, "light_green")


def bad(text):
    return colored(text, "red", attrs=["bold"])


def compare_guesses(kanji_list):
    bad_count, good_count = 0, 0

    for kanji in kanji_list:
        guess = guess_reading(kanji)
        try:
            correct_reading = kanji.onyomi[0]
        except IndexError:
            continue

        if guess == correct_reading:
            print(kanji.character, good(guess))
            good_count += 1
        else:
            print(kanji.character, bad(guess), "->", correct_reading)
            bad_count += 1

    print("{:.2%} complete".format(good_count / len(kanji_list)))


def main():
    kanji_list = load_kanji_list()

    compare_guesses(kanji_list)


if __name__ == "__main__":
    main()
