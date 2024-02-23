#!/usr/bin/env python3
"""
TODO:
* print errors as last
"""
import sys
import warnings
from pathlib import Path
from time import time

import numpy as np
from termcolor import colored

import guesser
from jstring import katakana_to_hiragana
from kanji import Kanji

# fix pandas pyarrow warning
warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd

CORRECT_FILEPATH = Path(".last_correct")


def load_last_correct():
    if not CORRECT_FILEPATH.exists():
        return None
    return int(CORRECT_FILEPATH.read_text())


def save_last_correct(correct_num):
    with CORRECT_FILEPATH.open("w") as fp:
        fp.write(str(correct_num))


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
    # return guesser.only_sei(kanji)
    return guesser.constant_kou(kanji)


def sfmt(style, text):
    if style == "good":
        return colored(text, "light_green")
    if style == "bad":
        return colored(text, "red", attrs=["bold"])
    if style == "note":
        return colored(text, "dark_grey")
    if style == "highlight":
        return colored(text, "white", "on_blue")
    raise ValueError(f"Unknown style {style!r}")


def sprint(style, text):
    print(sfmt(style, text))


def print_kanji_status(kanji, guess, correct_readings, is_correct):
    # colorize readings
    colored_readings = []
    for reading in correct_readings:
        if guess == reading:
            colored_readings.append(sfmt("good", reading))
        else:
            colored_readings.append(reading)
    colored_readings = " ".join(colored_readings)
    colored_guess = sfmt("good" if is_correct else "bad", guess)
    colored_index = sfmt("note", f"{kanji.index:>4}.")

    ctx = dict(
        idx=colored_index,
        char=kanji.character,
        rad=kanji.radical,
        guess=colored_guess,
        correct=colored_readings,
    )
    line = "{idx} {char} ({rad}) {guess} -> {correct}"
    print(line.format(**ctx))


def get_prec_diff_str(good, total):
    before = load_last_correct()
    if before is None:
        return ""
    delta = good - before
    percent = delta / total
    text = f"{percent:+.2%} ({delta:+d})"
    if delta < 0:
        return sfmt("bad", text)
    if delta > 0:
        return sfmt("good", text)
    if delta == 0:
        return sfmt("note", text)


def compare_guesses(kanji_list):
    bad_count, good_count = 0, 0
    for kanji in kanji_list:
        guess = guess_reading(kanji)
        correct_readings = [on.text for on in kanji.onyomi]
        correct_readings = [katakana_to_hiragana(on) for on in correct_readings]

        is_correct = guess in correct_readings
        if is_correct:
            good_count += 1
        else:
            bad_count += 1

        print_kanji_status(kanji, guess, correct_readings, is_correct)

    total = len(kanji_list)
    percent = "{:.2%}".format(good_count / total)

    # highlight
    mainline = sfmt("highlight", f"{percent:>7} complete")
    diff_str = get_prec_diff_str(good_count, total)
    print(mainline, diff_str)
    save_last_correct(good_count)

    sprint("note", f"{percent} ({good_count}/{total})")


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
