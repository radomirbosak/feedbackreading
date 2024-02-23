#!/usr/bin/env python3

import warnings
from collections import Counter

import numpy as np

from jstring import katakana_to_hiragana
from kanji import Kanji

# fix pandas pyarrow warning
warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd


def load_all_kanji():
    df = pd.read_csv("joyo.csv")
    df = df.replace(np.nan, None)

    return [Kanji.from_series(k) for _, k in df.iterrows()]


allk = load_all_kanji()


def print_most_common_readings():
    reading_counter = Counter()

    for kanji in allk:
        # print(kanji.onyomi_text)
        readings = [katakana_to_hiragana(on) for on in kanji.onyomi_text]
        reading_counter.update(readings)

    for reading, frequency in reading_counter.most_common(20):
        print(reading, "\t", frequency)


def main():
    print_most_common_readings()


if __name__ == "__main__":
    main()
