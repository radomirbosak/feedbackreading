# /usr/bin/env python3

from pathlib import Path

KRADFILE = Path("kradfile-u")


def get_krads(kradfile_path=KRADFILE):
    kanjis = {}

    for line in KRADFILE.open("r"):
        if line.startswith("#"):
            continue
        kanji, rest = line.rstrip().split(" : ")
        kanjis[kanji] = rest.split(" ")
    return kanjis


def main():
    kanjis = get_krads()
    for kanji, rest in list(kanjis.items())[:21]:
        print(kanji, rest)


if __name__ == "__main__":
    main()
