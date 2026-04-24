# Football Analysis Summary

## Basic Exploration

| Question | Answer |
| --- | --- |
| Matches in dataset | 49,287 |
| Completed matches used for score analysis | 49,215 |
| Earliest year | 1872 |
| Latest year | 2026 |
| Unique teams/countries | 333 |
| Unique host countries | 269 |
| Most frequent home team | Brazil (614 matches) |

## Goals Analysis

| Question | Answer |
| --- | --- |
| Average goals per match | 2.94 |
| Highest scoring match | 2001-04-11: Australia 31-0 American Samoa (31 goals) |
| More goals scored at home or away? | Home: 86,426; Away: 58,192 |
| Most common total-goals value | 2 goals (10,927 matches) |

## Match Results

| Question | Answer |
| --- | --- |
| Home-win percentage | 48.98% |
| Away-win percentage | 28.27% |
| Draw percentage | 22.75% |
| Does home advantage exist? | Yes. Home teams win more often than away teams and score more goals on average. |
| Team with most historical wins | Brazil (670 wins) |

## Visualization Data

The script writes chart-ready data to `outputs/goals_distribution.csv`, `outputs/match_outcomes.csv`, and `outputs/top_10_total_wins.csv`. If `matplotlib` is installed, running with `--make-plots` also writes PNG charts to `outputs/plots/`.
