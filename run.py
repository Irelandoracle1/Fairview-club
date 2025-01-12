import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import sqlite3 as sq
import os

current_dir = os.getcwd()
database_path = os.path.join(current_dir, r'data.db')

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load Google Sheets credentials with error handling
try:
    CREDS = Credentials.from_service_account_file('creds.json')
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
except Exception as e:
    print(f"Error loading Google Sheets credentials: {e}")
    exit(1)


class DatabaseConnection:
    def __init__(self, host) -> None:
        self.connection = None
        self.host = host

    def __enter__(self) -> sq.Connection:
        try:
            self.connection = sq.connect(self.host)
        except sq.Error as e:
            print(f"Error connecting to database: {e}")
            exit(1)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type or exc_val or exc_tb:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()


def create_player_table() -> None:
    try:
        with DatabaseConnection(database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS players '
                '(name text primary key, appearance integer, '
                'goals_scored integer, point integer, contribution integer)'
            )
    except sq.Error as e:
        print(f"Error creating player table: {e}")


class RankingSystem:
    def __init__(self, player_sheet_name):
        self.player_sheet_name = player_sheet_name
        self.sheet = self.get_player_sheet()

    def get_player_sheet(self):
        try:
            return GSPREAD_CLIENT.open(self.player_sheet_name).worksheet('Players')
        except gspread.SpreadsheetNotFound as e:
            print(f"Error: Google Sheet '{self.player_sheet_name}' not found. {e}")
            exit(1)

    def add_player(self, name, appearance, goals_scored, point):
        try:
            with DatabaseConnection(database_path) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    'INSERT INTO players VALUES (?, ?, ?, ?, 0)',
                    (name, appearance, goals_scored, point)
                )
        except sq.Error as e:
            print(f"Error inserting player into database: {e}")

    def update_player(self, name, appearance, goals_scored, point,
                      contribution):
        try:
            with DatabaseConnection(database_path) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    'UPDATE players SET appearance=?, goals_scored=?, point=?, '
                    'contribution=? WHERE name=?',
                    (appearance, goals_scored, point, contribution, name)
                )
        except sq.Error as e:
            print(f"Error updating player data: {e}")

    def get_all_players(self):
        try:
            with DatabaseConnection(database_path) as connection:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM players')
                players = [
                    {
                        'name': row[0], 'appearance': row[1],
                        'goals_scored': row[2],
                        'point': row[3], 'contribution': row[4]
                    } for row in cursor.fetchall()
                ]
            return players
        except sq.Error as e:
            print(f"Error fetching all players: {e}")
            return []

    def get_player(self, name):
        try:
            with DatabaseConnection(database_path) as connection:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM players WHERE name=?', (name,))
                rows = cursor.fetchall()

                if not rows:
                    return None

                player = [
                    {
                        'name': row[0], 'appearance': row[1],
                        'goals_scored': row[2],
                        'point': row[3], 'contribution': row[4]
                    } for row in rows
                ][0]
                return player
        except sq.Error as e:
            print(f"Error fetching player: {e}")
            return None

    def post_contribution(self, name, amount):
        player = self.get_player(name)
        if player:
            player['contribution'] += amount
            self.update_player(
                name, player['appearance'], player['goals_scored'],
                player['point'], player['contribution']
            )
        self.push_to_sheet()

    def post_match_result(self, player_names, result, goals_scored):
        """
        Record match results, update player stats, and record goals scored.
        """
        players = self.get_all_players()
        for name in player_names:
            if len(players) == 0:
                if result == "win":
                    self.add_player(name, 1, goals_scored[name], 3)
                elif result == "draw":
                    self.add_player(name, 1, goals_scored[name], 1)
            elif name not in [player['name'] for player in players]:
                if result == "win":
                    self.add_player(name, 1, goals_scored[name], 3)
                elif result == "draw":
                    self.add_player(name, 1, goals_scored[name], 1)
            elif name in [player['name'] for player in players]:
                player = [
                    player for player in players if player['name'] == name
                ][0]
                if result == "win":
                    player['point'] += 3
                    player['goals_scored'] += goals_scored[name]
                    player['appearance'] += 1
                elif result == "draw":
                    player['point'] += 1
                    player['goals_scored'] += goals_scored[name]
                    player['appearance'] += 1
                self.update_player(
                    name, player['appearance'], player['goals_scored'],
                    player['point'], player['contribution']
                )
        self.push_to_sheet()

    def push_to_sheet(self):
        """
        Update Google Sheet with player data.
        """
        columns = [
            "Player", "Appearances", "Goals Scored", "Points", "Contribution"
        ]
        players = self.get_all_players()
        df = pd.DataFrame([{
            'name': player['name'],
            'appearance': player['appearance'],
            'goals_scored': player['goals_scored'],
            'point': player['point'],
            'contribution': player['contribution']
        } for player in players]).sort_values(by=['point'], ascending=False)
        df.columns = columns
        try:
            self.sheet.update([df.columns.values.tolist()] + df.values.tolist())
        except gspread.GSpreadException as e:
            print(f"Error updating Google Sheet: {e}")

# Error handling for admin login
def admin_login():
    """
    Checks admin credentials.
    """
    username = input("Enter admin username:\n ")
    password = input("Enter admin password:\n ")

    
    admin_username = "admin"
    admin_password = "password"

    if username == admin_username and password == admin_password:
        return True
    else:
        print("Invalid credentials. Access denied. Please click on Run Program again to re-enter details.")
        return False

# Input validation and error handling in main
def main():
    """
    Main function to run the application.
    """
    create_player_table()
    player_sheet_name = "Fairview_Football_All_Stars_Contributions"
    ranking_system = RankingSystem(player_sheet_name)

    if not admin_login():
        return

    while True:
        print("\nWelcome To Fairview Football Application")
        print("\nSelect an option:")
        print("1. Record match result")
        print("2. Record player contribution")
        print("3. Exit")
        choice = input("Enter your choice:\n ")

        if choice == "1":
            player_names = input(
                "Enter player names (comma-separated):\n "
            ).split(",")
            player_names = [name.strip() for name in player_names]
            result = input("Enter match result (win/draw):\n ")
            goals_scored = {}
            for name in player_names:
                try:
                    goals = int(input(f"Enter goals scored by {name}:\n "))
                    goals_scored[name] = goals
                except ValueError:
                    print("Invalid input for goals. Please enter a number.")
                    continue
            ranking_system.post_match_result(player_names, result, goals_scored)

        elif choice == "2":
            player_name = input("Enter player name:\n ")
            try:
                contribution_amount = float(input("Enter contribution amount:\n "))
                ranking_system.post_contribution(player_name, contribution_amount)
            except ValueError:
                print("Invalid input. Contribution amount should be a number.")
                continue

        elif choice == "3":
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
