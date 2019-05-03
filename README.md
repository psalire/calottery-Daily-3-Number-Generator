# calottery Daily 3 Number Generator

Parses calottery's .txt of Daily 3 results to generate playable Daily 3 numbers using the "hot number" strategy, wherein the least played numbers over a certain amount of draws are considered playable.

## Options

```
> python3 daily3generator.py --help

usage: daily3generator.py [-h] [--lookback LOOKBACK]
                          [--tothotnumbers TOTHOTNUMBERS] [--usedate USEDATE]
                          [--uselocal] [--middaydraw] [--includetriples]
                          [--showhistogram] [--savefile]

optional arguments:
  -h, --help            show this help message and exit
  --lookback LOOKBACK   Number of previous draws to calculate from. Default:
                        10
  --tothotnumbers TOTHOTNUMBERS
                        Number of "hot numbers" to use in generating playable
                        numbers. Max: 10 Default: 4
  --usedate USEDATE     Date to lookback from in format "%b %d, %Y". Default:
                        today's date
  --uselocal            Use local daily3results.txt file from --savefile,
                        instead of fetch. Default: False
  --middaydraw          Use midday draw. Default: False
  --includetriples      Include triples in playable numbers. Default: False
  --showhistogram       Print the frequency histogram. Default: False
  --savefile            Save the calottery .txt file as daily3results.txt.
                        Default: False

```

## Example output
```
> python3 daily3generator.py --middaydraw --showhistogram --usedate "Sep 24, 2018"

Lookback-size    : 10
Include Triples  : False
Using Midday Draw: True
Using Date       : Sep 24, 2018 (Draw #15464)

Frequency Histogram:
0: 4
1: 4
2: 4
3: 4
4: 2
5: 3
6: 2
7: 2
8: 2
9: 3

Numbers to play (4,6,7,8):
 1. 446
 2. 447
 3. 448
 4. 466
 5. 467
 6. 468
 7. 477
 8. 478
 9. 488
10. 667
11. 668
12. 677
13. 678
14. 688
15. 778
16. 788
```

