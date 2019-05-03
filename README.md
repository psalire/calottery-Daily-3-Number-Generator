# calottery Daily 3 Number Generator

Parses calottery's .txt of Daily 3 results to generate playable Daily 3 numbers using the "hot number" strategy, wherein the least played numbers over a certain amount of draws are considered playable.

## Options

```
   python3 daily3generator.py --help
   usage: daily3generator.py [-h] [--lookback LOOKBACK]
                             [--tothotnumbers TOTHOTNUMBERS] [--usedate USEDATE]
			                               [--middaydraw] [--includetriples] [--showhistogram]

						       optional arguments:
						         -h, --help            show this help message and exit
							   --lookback LOOKBACK   Number of previous draws to calculate from. Default:
							                           10
										     --tothotnumbers TOTHOTNUMBERS
										                             Number of "hot numbers" to use in generating playable
													                             numbers. Max: 10 Default: 4
																       --usedate USEDATE     Date to lookback from in format "%b %d, %Y". Default:
																                               today
																			         --middaydraw          Use midday draw. Default: False
																				   --includetriples      Include triples in playable numbers. Default: False
																				     --showhistogram       Print the frequency histogram. Default: False
```


