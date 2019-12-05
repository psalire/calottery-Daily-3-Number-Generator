# calottery Daily 3 Number Generator

NOTE: calottery.com no longer provides the .txt file containing historical data. If you have an old copy of one, you may use ```--use-local [file]```.

Parses calottery's .txt of Daily 3 results to generate playable Daily 3 numbers using the "hot number" strategy, wherein the least played numbers over a certain amount of draws are considered playable.

## Dependencies

Python3, tkinter, requests

## Options

```
> python3 daily3generator.py --help

usage: daily3generator.py [-h] [--uselocal USELOCAL]

optional arguments:
  -h, --help           show this help message and exit
  --uselocal USELOCAL  Local file to read instead of fetching from
                       calottery.com

```

## Example output
![Example Output](imgs/example.png "Output")
