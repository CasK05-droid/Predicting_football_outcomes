import pandas as pd

# ======================================
# LOAD DATA
# ======================================

df = pd.read_csv(r"C:\cas\project end\elo data.csv")

df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
df = df.sort_values("Date").reset_index(drop=True)

# ======================================
# INITIAL STRUCTURES
# ======================================

teams = pd.concat([df["HomeTeam"], df["AwayTeam"]]).unique()

# Track cumulative stats
team_stats = {
    team: {
        "games": 0,
        "goals_scored": 0,
        "goals_conceded": 0
    }
    for team in teams
}

home_attack_list = []
home_defence_list = []
away_attack_list = []
away_defence_list = []

# ======================================
# MAIN LOOP (Chronological)
# ======================================

for index, row in df.iterrows():

    home = row["HomeTeam"]
    away = row["AwayTeam"]

    # ---- LEAGUE AVERAGE (before this match) ----
    total_goals = sum(team_stats[t]["goals_scored"] for t in teams)
    total_games = sum(team_stats[t]["games"] for t in teams)

    # Avoid division by zero (start of season)
    if total_games == 0:
        league_avg_goals = 1.35  # typical EPL average per team per game
    else:
        league_avg_goals = total_goals / total_games

    # ---- HOME TEAM STRENGTH BEFORE MATCH ----
    if team_stats[home]["games"] == 0:
        home_attack = 1
        home_defence = 1
    else:
        home_attack = (
            (team_stats[home]["goals_scored"] / team_stats[home]["games"])
            / league_avg_goals
        )
        home_defence = (
            (team_stats[home]["goals_conceded"] / team_stats[home]["games"])
            / league_avg_goals
        )

    # ---- AWAY TEAM STRENGTH BEFORE MATCH ----
    if team_stats[away]["games"] == 0:
        away_attack = 1
        away_defence = 1
    else:
        away_attack = (
            (team_stats[away]["goals_scored"] / team_stats[away]["games"])
            / league_avg_goals
        )
        away_defence = (
            (team_stats[away]["goals_conceded"] / team_stats[away]["games"])
            / league_avg_goals
        )

    # Store pre-match values
    home_attack_list.append(home_attack)
    home_defence_list.append(home_defence)
    away_attack_list.append(away_attack)
    away_defence_list.append(away_defence)

    # ======================================
    # UPDATE STATS AFTER MATCH
    # ======================================

    home_goals = row["FTHG"]
    away_goals = row["FTAG"]

    team_stats[home]["games"] += 1
    team_stats[home]["goals_scored"] += home_goals
    team_stats[home]["goals_conceded"] += away_goals

    team_stats[away]["games"] += 1
    team_stats[away]["goals_scored"] += away_goals
    team_stats[away]["goals_conceded"] += home_goals

# ======================================
# ADD COLUMNS
# ======================================

df["HomeAttackStrength"] = home_attack_list
df["HomeDefenceStrength"] = home_defence_list
df["AwayAttackStrength"] = away_attack_list
df["AwayDefenceStrength"] = away_defence_list

# ======================================
# SAVE
# ======================================

df.to_excel(r"C:\cas\project end\elo_data_with_strength.xlsx", index=False)

print("Attack and Defence Strength added successfully.")
