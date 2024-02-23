# Kanji reading predictor

## Predictor results

| predictor | precision | correct predictions | comments |
| --------- | --------- | ------------------- | -------- |
| constant こう | 3.25% | 67 / 2059 | |
| ideal radical predictor | 14.62% | 301 / 2059 | data in [ideal_radical_map.py](ideal_radical_map.py) |

## Usage

Run
```
./loop.sh
```
for development loop using [entr](https://github.com/eradman/entr).

or simply

```
./run.py
```
For a single evaluation.

## Screenshot

![screenshot](screenshot.png)
