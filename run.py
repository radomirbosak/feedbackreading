#!/usr/bin/env python3

import warnings
from time import time

import numpy as np
from termcolor import colored

from jstring import katakana_to_hiragana
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


def load_kanji_list():
    return load_all_kanji()


# guessing algorithm
def guess_reading(kanji):
    return "せい"


def sfmt(style, text):
    if style == "good":
        return colored(text, "light_green")
    if style == "bad":
        return colored(text, "red", attrs=["bold"])
    if style == "note":
        return colored(text, "dark_grey")
    if style == "highlight":
        return colored(text, "white", "on_blue")


def sprint(style, text):
    print(sfmt(style, text))


def compare_guesses(kanji_list):
    bad_count, good_count = 0, 0
    no_onyomi_count = 0
    for kanji in kanji_list:
        guess = guess_reading(kanji)
        try:
            correct_reading = kanji.onyomi[0].text
            # correct_reading = ",".join([on.text for on in kanji.onyomi])
            # print(type(correct_reading))
            correct_reading = katakana_to_hiragana(correct_reading)
        except IndexError:
            no_onyomi_count += 1
            continue

        ctx = dict(
            char=kanji.character,
            guess=guess,
            good_guess=sfmt("good", guess),
            bad_guess=sfmt("bad", guess),
            correct=correct_reading,
        )
        if guess == correct_reading:
            line = "{char} {good_guess}"
            good_count += 1
        else:
            line = "{char} {bad_guess} -> {correct}"
            bad_count += 1
        print(line.format(**ctx))

    print("Kanji without any onyomi: {}/{}".format(no_onyomi_count, len(kanji_list)))
    total_eligible = len(kanji_list) - no_onyomi_count

    text = "{:>7.2%} complete".format(good_count / total_eligible)
    sprint("highlight", text)


def main():
    start = time()
    kanji_list = load_kanji_list()
    compare_guesses(kanji_list)

    # print total time
    sprint("note", "Finished in {:.2f}s".format(time() - start))


if __name__ == "__main__":
    main()
