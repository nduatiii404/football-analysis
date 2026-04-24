# International Football Results Analysis

This repository contains the solution for Artificial Intelligence Exercise 1. The project analyzes the international football results dataset referenced in the assignment PDF.

## Dataset

Source: [martj42/international_results](https://github.com/martj42/international_results)

The downloaded CSV is stored at:

```text
data/results.csv
```

The current public dataset includes completed matches plus scheduled future fixtures. The analysis script keeps all rows for dataset-size and date-range questions, then uses only rows with numeric home and away scores for goals, match outcomes, and wins.

## Project Structure

```text
football-analysis/
  data/
    results.csv
  notebooks/
    Football_Analysis.ipynb
  outputs/
    analysis_summary.md
    goals_distribution.csv
    match_outcomes.csv
    top_10_total_wins.csv
  scripts/
    football_analysis.py
  README.md
  requirements.txt
```

## How To Run

Clone and enter the project folder:

```bash
git clone https://github.com/nduatiii404/football-analysis.git
cd football-analysis
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the analysis:

```bash
python scripts/football_analysis.py
```

Run with plots:

```bash
python scripts/football_analysis.py --make-plots
```

Open the notebook:

```bash
jupyter notebook notebooks/Football_Analysis.ipynb
```

## Assignment Questions Covered

- Total number of matches
- Earliest and latest year in the data
- Unique teams and host countries
- Most frequent home team
- Average goals per match
- Highest scoring match
- Home vs away goal totals
- Most common total-goals value
- Match outcome percentages
- Evidence of home advantage
- Country/team with most historical wins
- Histogram of goals
- Bar chart of match outcomes
- Top 10 teams by total wins

## Key Observation

Home advantage is evaluated using both outcome share and goal totals. In the downloaded dataset, home teams score more total goals and win more often than away teams among completed matches.
