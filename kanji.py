from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional

import pandas as pd

from jstring import hiragana, katakana


def is_onyomi(reading):
    pivot = reading[0]
    if pivot == "（":
        pivot = reading[1]
    return pivot in katakana


def is_kunyomi(reading):
    pivot = reading[0]
    if pivot == "（":
        pivot = reading[1]
    return pivot in hiragana


class ReadingCat(Enum):
    Kunyomi = auto()
    Onyomi = auto()
    Unknown = auto()

    @staticmethod
    def from_text(text):
        if text[0] in katakana:
            return ReadingCat.Onyomi
        if text[0] in hiragana:
            return ReadingCat.Kunyomi
        return ReadingCat.Unknown


class Reading:
    def __init__(self, text: str):
        # self.original_text = text
        self.rare = text.startswith("（")
        text = text.strip("（）")

        suffix = ""
        if "-" in text:
            text, suffix = text.split("-", maxsplit=2)

        self.text = text
        self.okurigana = suffix
        self.category = ReadingCat.from_text(self.text)

    def __str__(self):
        return self.with_okurigana

    def __repr__(self):
        return repr(self.with_okurigana)

    @property
    def with_okurigana(self):
        if not self.okurigana:
            return self.text
        return f"{self.text}-{self.okurigana}"


@dataclass
class Kanji:
    index: int = field(repr=False)
    character: str
    character_old: Optional[str] = field(repr=False)
    radical: str
    strokes: int
    grade: str
    year_added: Optional[int] = field(repr=False)
    meaning: str
    readings: list[str]

    @property
    def kunyomi(self):
        return [r for r in self.readings if r.category == ReadingCat.Kunyomi]

    @property
    def onyomi(self):
        return [r for r in self.readings if r.category == ReadingCat.Onyomi]

    @property
    def kunyomi_text(self):
        return [r.text for r in self.kunyomi]

    @property
    def onyomi_text(self):
        return [r.text for r in self.onyomi]

    @classmethod
    def from_series(cls, row: pd.Series):
        readings, _ = row["Readings"].split("\n", maxsplit=2)
        readings = [Reading(r) for r in readings.split("、")]

        year = row["Year added"]
        return cls(
            row["#"],
            row["New (Shinjitai)"],
            row["Old (Kyūjitai)"],
            row["Radical"],
            row["Strokes"],
            row["Grade"],
            int(year) if year else None,
            row["English meaning"],
            readings,
        )
