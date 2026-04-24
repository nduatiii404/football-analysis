from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "results.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
PLOTS_DIR = OUTPUT_DIR / "plots"


def load_results(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["home_score"] = pd.to_numeric(df["home_score"], errors="coerce")
    df["away_score"] = pd.to_numeric(df["away_score"], errors="coerce")
    return df


def completed_matches(df: pd.DataFrame) -> pd.DataFrame:
    completed = df.dropna(subset=["home_score", "away_score"]).copy()
    completed["home_score"] = completed["home_score"].astype(int)
    completed["away_score"] = completed["away_score"].astype(int)
    completed["total_goals"] = completed["home_score"] + completed["away_score"]
    completed["result"] = completed.apply(match_result, axis=1)
    return completed


def match_result(row: pd.Series) -> str:
    if row["home_score"] > row["away_score"]:
        return "Home Win"
    if row["home_score"] < row["away_score"]:
        return "Away Win"
    return "Draw"


def total_wins(completed: pd.DataFrame) -> pd.Series:
    home_winners = completed.loc[
        completed["home_score"] > completed["away_score"], "home_team"
    ]
    away_winners = completed.loc[
        completed["away_score"] > completed["home_score"], "away_team"
    ]
    winners = pd.concat([home_winners, away_winners], ignore_index=True)
    return winners.value_counts()


def build_summary(df: pd.DataFrame, completed: pd.DataFrame) -> tuple[str, dict[str, pd.DataFrame]]:
    all_teams = pd.concat([df["home_team"], df["away_team"]], ignore_index=True)
    home_team_counts = df["home_team"].value_counts()
    outcome_counts = completed["result"].value_counts()
    outcome_percent = (outcome_counts / len(completed) * 100).round(2)
    goals_distribution = completed["total_goals"].value_counts().sort_index()
    wins = total_wins(completed)

    highest = completed.sort_values(
        ["total_goals", "date"], ascending=[False, True]
    ).iloc[0]

    home_goals = int(completed["home_score"].sum())
    away_goals = int(completed["away_score"].sum())
    avg_home_goals = completed["home_score"].mean()
    avg_away_goals = completed["away_score"].mean()
    home_win_pct = outcome_percent.get("Home Win", 0.0)
    away_win_pct = outcome_percent.get("Away Win", 0.0)

    home_advantage = (
        "Yes. Home teams win more often than away teams and score more goals on average."
        if home_win_pct > away_win_pct and avg_home_goals > avg_away_goals
        else "The evidence is mixed in this dataset."
    )

    summary = f"""# Football Analysis Summary

## Basic Exploration

| Question | Answer |
| --- | --- |
| Matches in dataset | {len(df):,} |
| Completed matches used for score analysis | {len(completed):,} |
| Earliest year | {int(df["date"].dt.year.min())} |
| Latest year | {int(df["date"].dt.year.max())} |
| Unique teams/countries | {all_teams.nunique():,} |
| Unique host countries | {df["country"].nunique():,} |
| Most frequent home team | {home_team_counts.index[0]} ({home_team_counts.iloc[0]:,} matches) |

## Goals Analysis

| Question | Answer |
| --- | --- |
| Average goals per match | {completed["total_goals"].mean():.2f} |
| Highest scoring match | {highest["date"].date()}: {highest["home_team"]} {highest["home_score"]}-{highest["away_score"]} {highest["away_team"]} ({int(highest["total_goals"])} goals) |
| More goals scored at home or away? | Home: {home_goals:,}; Away: {away_goals:,} |
| Most common total-goals value | {int(goals_distribution.idxmax())} goals ({int(goals_distribution.max()):,} matches) |

## Match Results

| Question | Answer |
| --- | --- |
| Home-win percentage | {home_win_pct:.2f}% |
| Away-win percentage | {away_win_pct:.2f}% |
| Draw percentage | {outcome_percent.get("Draw", 0.0):.2f}% |
| Does home advantage exist? | {home_advantage} |
| Team with most historical wins | {wins.index[0]} ({int(wins.iloc[0]):,} wins) |

## Visualization Data

The script writes chart-ready data to `outputs/goals_distribution.csv`, `outputs/match_outcomes.csv`, and `outputs/top_10_total_wins.csv`. If `matplotlib` is installed, running with `--make-plots` also writes PNG charts to `outputs/plots/`.
"""

    tables = {
        "goals_distribution": goals_distribution.rename_axis("total_goals")
        .reset_index(name="matches"),
        "match_outcomes": outcome_counts.rename_axis("result").reset_index(name="matches"),
        "top_10_total_wins": wins.head(10).rename_axis("team").reset_index(name="wins"),
    }
    return summary, tables


def write_outputs(summary: str, tables: dict[str, pd.DataFrame]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "analysis_summary.md").write_text(summary, encoding="utf-8")
    for name, table in tables.items():
        table.to_csv(OUTPUT_DIR / f"{name}.csv", index=False)


def make_plots(completed: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is not installed; skipped PNG plot generation.")
        return

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    completed["total_goals"].hist(bins=15)
    plt.title("Distribution of Goals Per Match")
    plt.xlabel("Total goals")
    plt.ylabel("Matches")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "goals_histogram.png", dpi=150)
    plt.close()

    outcomes = tables["match_outcomes"].set_index("result")["matches"]
    outcomes.plot(kind="bar", color=["#3b82f6", "#f97316", "#22c55e"])
    plt.title("Match Outcomes")
    plt.xlabel("Outcome")
    plt.ylabel("Matches")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "match_outcomes.png", dpi=150)
    plt.close()

    top_wins = tables["top_10_total_wins"].set_index("team")["wins"].sort_values()
    top_wins.plot(kind="barh", color="#2563eb")
    plt.title("Top 10 Teams by Total Wins")
    plt.xlabel("Wins")
    plt.ylabel("Team")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "top_10_total_wins.png", dpi=150)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze international football results.")
    parser.add_argument("--make-plots", action="store_true", help="Generate PNG charts.")
    args = parser.parse_args()

    df = load_results()
    completed = completed_matches(df)
    summary, tables = build_summary(df, completed)
    write_outputs(summary, tables)

    if args.make_plots:
        make_plots(completed, tables)

    print(summary)


if __name__ == "__main__":
    main()
