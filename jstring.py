hiragana = (
    'ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴ ふぶぷへべぺほぼぽ'
    'まみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖ゙゚゛゜ゝゞゟ'
)

katakana = (
    '゠ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモ'
    'ャヤュユョヨラリルレロヮワヰヱヲンヴヵヶヷヸヹヺ・ーヽヾヿ'
)


_kanji_ranges = ['㐀䶵', '一鿋', '豈頻']


def _kanji_generator():
    for startchar, stopchar in _kanji_ranges:
        coderange = range(ord(startchar), ord(stopchar) + 1)
        yield from (chr(charcode) for charcode in coderange)


kanji = ''.join(_kanji_generator())
