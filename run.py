#!/usr/bin/env python3

import sys
import warnings
from time import time

import numpy as np
from termcolor import colored

from jstring import katakana_to_hiragana
from kanji import Kanji

# fix pandas pyarrow warning
warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd


def load_all_kanji():
    df = pd.read_csv("joyo.csv")
    df = df.replace(np.nan, None)

    return [Kanji.from_series(k) for _, k in df.iterrows()]


def load_kanji_list():
    allk = load_all_kanji()

    filtered = []
    removed = []
    for kanji in allk:
        if len(kanji.onyomi) == 0:
            removed.append(kanji)
            continue
        # if "セイ" not in kanji.onyomi_text and "ロウ" not in kanji.onyomi_text:
        #     removed.append(kanji)
        #     continue
        filtered.append(kanji)

    return filtered, removed


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
    for kanji in kanji_list:
        guess = guess_reading(kanji)
        correct_readings = [on.text for on in kanji.onyomi]
        correct_readings = [katakana_to_hiragana(on) for on in correct_readings]

        # colorize readings
        colored_readings = []
        for reading in correct_readings:
            if guess == reading:
                colored_readings.append(sfmt("good", reading))
            else:
                colored_readings.append(reading)
        colored_readings = " ".join(colored_readings)

        ctx = dict(
            char=kanji.character,
            rad=kanji.radical,
            guess=guess,
            good_guess=sfmt("good", guess),
            bad_guess=sfmt("bad", guess),
            correct=colored_readings,
        )
        if guess in correct_readings:
            line = "{char} ({rad}) {good_guess} -> {correct}"
            good_count += 1
        else:
            line = "{char} ({rad}) {bad_guess} -> {correct}"
            bad_count += 1
        print(line.format(**ctx))

    text = "{:>7.2%} complete".format(good_count / len(kanji_list))
    sprint("highlight", text)


def main():
    start = time()
    kanji_list, removed = load_kanji_list()
    if not kanji_list:
        sprint("warn", "No eligible kanji, {} removed".format(len(removed)))
        sys.exit(0)
    compare_guesses(kanji_list)

    # print various info
    sprint("note", "Total {} kanji".format(len(kanji_list) + len(removed)))
    sprint("note", "Removed {} kanji with no onyomi".format(len(removed)))

    # print total time
    sprint("note", "Finished in {:.2f}s".format(time() - start))


if __name__ == "__main__":
    main()
