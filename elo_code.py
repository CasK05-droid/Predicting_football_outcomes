import pandas as pd

# ======================================
# CONFIG
# ======================================

HOME_ADVANTAGE = 100
K = 20

INITIAL_ELOS = {
    "Man United": 2090,
    "Fulham": 1970,
    "Aston Villa": 2098,
    "Liverpool": 2221,
    "Arsenal": 2245,
    "Brentford": 1982,
    "Everton": 1983,
    "Brighton": 2029,
    "Newcastle": 2070,
    "Ipswich": 1858,
    "Bournemouth": 1963,
    "Nott'm Forest": 1900,
    "West Ham": 2003,
    "Southampton": 1858,
    "Wolves": 1960,
    "Crystal Palace": 2003,
    "Chelsea": 2091,
    "Man City": 2332,
    "Leicester": 1911,
    "Tottenham": 2075
}

# ======================================
# ELO FUNCTIONS
# ======================================

def expected_score(team_elo, opp_elo):
    return 1 / (1 + 10 ** ((opp_elo - team_elo) / 400))


def update_elo(home_elo, away_elo, home_goals, away_goals):

    home_adj = home_elo + HOME_ADVANTAGE
    home_exp = expected_score(home_adj, away_elo)
    away_exp = 1 - home_exp

    if home_goals > away_goals:
        home_score, away_score = 1, 0
    elif home_goals < away_goals:
        home_score, away_score = 0, 1
    else:
        home_score, away_score = 0.5, 0.5

    new_home_elo = home_elo + K * (home_score - home_exp)
    new_away_elo = away_elo + K * (away_score - away_exp)

    return new_home_elo, new_away_elo


# ======================================
# MAIN FUNCTION
# ======================================

def add_elo_columns(df):

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df = df.sort_values("Date").reset_index(drop=True)

    team_elos = INITIAL_ELOS.copy()

    home_before = []
    away_before = []
    home_after = []
    away_after = []

    for _, row in df.iterrows():

        home = row["HomeTeam"]
        away = row["AwayTeam"]

        home_goals = row["FTHG"]
        away_goals = row["FTAG"]

        # Elo BEFORE match
        current_home_elo = team_elos.get(home, 1500)
        current_away_elo = team_elos.get(away, 1500)

        home_before.append(current_home_elo)
        away_before.append(current_away_elo)

        # Calculate updated Elo
        new_home_elo, new_away_elo = update_elo(
            current_home_elo,
            current_away_elo,
            home_goals,
            away_goals
        )

        # Store AFTER values
        home_after.append(new_home_elo)
        away_after.append(new_away_elo)

        # Update dictionary so next match uses new ratings
        team_elos[home] = new_home_elo
        team_elos[away] = new_away_elo

    # Add columns
    df["HomeEloBefore"] = home_before
    df["AwayEloBefore"] = away_before
    df["HomeEloAfter"] = home_after
    df["AwayEloAfter"] = away_after

    return df


# ======================================
# RUN
# ======================================

df = pd.read_csv(r"C:\cas\project end\elo data.csv")

df_with_elo = add_elo_columns(df)

df_with_elo.to_excel(r"C:\cas\project end\elo data_with_elo.xlsx", index=False)

print("Elo columns (Before & After) successfully added.")
