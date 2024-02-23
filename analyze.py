#!/usr/bin/env python3

import warnings
from collections import Counter, defaultdict

import numpy as np

from jstring import fw_ljust, katakana_to_hiragana
from kanji import Kanji
from krad import get_krads

# fix pandas pyarrow warning
warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd


def load_all_kanji():
    df = pd.read_csv("joyo.csv")
    df = df.replace(np.nan, None)

    return [Kanji.from_series(k) for _, k in df.iterrows()]


allk = load_all_kanji()
allkrads = get_krads()


def print_most_common_readings():
    reading_counter = Counter()

    for kanji in allk:
        # print(kanji.onyomi_text)
        readings = [katakana_to_hiragana(on) for on in kanji.onyomi_text]
        reading_counter.update(readings)

    for reading, frequency in reading_counter.most_common(20):
        print(reading, "\t", frequency)


def print_most_common_radicals():
    radical_counter = Counter([kanji.radical for kanji in allk])

    for radical, frequency in radical_counter.most_common(20):
        print(radical, "\t", frequency)


def get_radical_counters():
    radical_counters = defaultdict(Counter)
    for kanji in allk:
        readings = [katakana_to_hiragana(on) for on in kanji.onyomi_text]
        radical_counters[kanji.radical].update(readings)
    return radical_counters


def most_common_reading_for_radical():
    radical_counters = get_radical_counters()
    radical_influence = get_radical_influence()

    for radical, influence in radical_influence[:20]:
        counter = radical_counters[radical]
        readingpart = ""
        for reading, frequency in counter.most_common(3):
            readingpart += f" {reading}({frequency})\t"
        radicalpart = f"{radical}({influence})"
        print(radicalpart, readingpart)


def get_radical_influence():
    """
    Return (radical, frequency) pairs, e.g.
    {'水': 118, '人': 98, '手': 95, ...}
    """
    all_radicals = set(kanji.radical for kanji in allk)
    radical_influence = {
        radical: len([1 for kanji in allk if kanji.radical == radical])
        for radical in all_radicals
    }
    return sorted(radical_influence.items(), key=lambda x: -x[1])


def print_most_influental_radicals():

    srads = dict(get_radical_influence())
    for radical, influence in list(srads.items())[:20]:
        print(radical, influence)


def print_radical_to_reading_table():
    radical_counters = get_radical_counters()
    radical_influence = get_radical_influence()

    table = {}
    print("{")
    for radical, influence in radical_influence:
        counter = radical_counters[radical]
        reading, count = counter.most_common(1)[0]
        # print(radical, influence, reading)
        # table[radical] = reading
        print("  {!r}: {!r},  # {}/{}".format(radical, reading, count, influence))
    print("}")

    print("{} radicals printed".format(len(radical_influence)))


def print_all_krad_parts():
    allparts = set()
    for kanji, parts in allkrads.items():
        allparts.update(parts)

    print("".join(allparts))
    print("Found", len(allparts), "parts")


def print_parts_to_readings():
    # 253 parts
    # 十戈冫⺾匚禸冊魚至宀亀并丶瓜殳儿マ鼠鼓韋谷｜大頁門邑入鳥革ヨ止鬲厶黹虫口干色矢廾子足犭米甘凵也夕巾彳乙屮長隶巛人毛刂艮二癶又髟岡灬龠久母鹿麦食肉豆井毋貝玄王禾鼻面耒牛麻冖刀高鬥ハ音臼广手木罒斤歹火竜鬯彑而羽亅黒舌西虍⺹山骨豸支曰巴糸氏冂卩亠⺌血亡辰瓦五牙勿士厂日文立走世角石欠黄囗衣寸疋里尤一𠆢水免田爻匕白攵幺及犬生ノ車滴几隹韭屯雨卜已羊皮無忄品女行目戸缶臣疒風比ユ青言川九尢舟爪首方衤舛斗土爿弓自釆聿弋辛无身金皿礻黍用馬鹵父元⻏扌氵⺅彡非斉夂酉巨心力香豕⻖气穴辶赤尸乃月奄歯飛矛鼎黽齊工竹見廴勹鬼小片示耳
    for kanji in allk[:20]:
        parts = allkrads[kanji.character]
        parts_str = "".join(parts)
        parts_str = fw_ljust(parts_str, 16)
        readings_str = " ".join(kanji.onyomi_text)
        print(
            f"{kanji.index:>4}.", parts_str, "->", kanji.character, "->", readings_str
        )


def main():
    # print_most_common_readings()
    # print_most_common_radicals()
    # print_most_influental_radicals()
    # most_common_reading_for_radical()
    # print_radical_to_reading_table()
    # print_all_krad_parts()
    print_parts_to_readings()


if __name__ == "__main__":
    main()
