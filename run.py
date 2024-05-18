import gspread
from google.oauth2.service_account import Credentials
import pandas as pd 
import sqlite3 as sq
import os


current_dir = os.getcwd()
database_path = os.path.join(current_dir, r'data.db')
print(database_path)


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load Google Sheets credentials
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

class DatabaseConnection:
    def __init__(self, host) -> None:
        self.connection = None
        self.host = host

    def __enter__(self) -> sq.Connection:
        self.connection = sq.connect(self.host)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type or exc_val or exc_tb:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()

def create_player_table() -> None:
    with DatabaseConnection(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS players (name text primary key, appearance integer, goals_scored integer, point integer, contribution integer)')


class Player:
    """
    Represents a player in the football team.
    """

    def __init__(self, name):
        self.name = name
        self.appearances = 0
        self.goals_scored = 0
        self.points = 0
        self.contribution = 0

    def add_appearance(self):
        """
        Increment player's appearance count.
        """
        self.appearances += 1
        self.points += 1

    def add_goals(self, goals):
        """
        Add goals scored by the player.
        """
        self.goals_scored += goals
        self.points += goals  # Update points when goals are scored

    def add_points(self, points):
        """
        Add points to the player's total.
        """
        self.points += points

    def deduct_points(self, points):
        """
        Deduct points from the player's total.
        """
        self.points -= points

    def add_contribution(self, amount):
        """
        Add financial contribution made by the player.
        """
        self.contribution += amount

    def __str__(self):
        """
        String representation of the player.
        """
        return f"{self.name}: Appearances - {self.appearances}, Goals Scored - {self.goals_scored}, Points - {self.points}, Contribution - {self.contribution} euros"

class RankingSystem_v2:
    def __init__(self, player_sheet_name):
        self.player_sheet_name = player_sheet_name
        self.sheet = self.get_player_sheet()

    def get_player_sheet(self):
        return GSPREAD_CLIENT.open(self.player_sheet_name).worksheet('Players')

    def add_player(self, name, appearance, goals_scored, point):
        with DatabaseConnection(database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO players VALUES (?, ?, ?, ?, 0)', (name, appearance, goals_scored, point))

    def update_player(self, name, appearance, goals_scored, point):
        with DatabaseConnection(database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('UPDATE players SET appearance=?, goals_scored=?, point=? where name=?', (appearance, goals_scored, point, name))

    def get_all_players(self):
        with DatabaseConnection(database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM players')
            players = [{
                'name': row[0], 'appearance': row[1], 'goals_scored': row[2],
                'point': row[3], 'contribution': row[4]
            } for row in cursor.fetchall()]
        return players

    def get_player(self, name):
        with DatabaseConnection(database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM player where name=?', (name,))
            player = [{
                'name': row[0], 'appearance': row[1], 'goals_scored': row[2],
                'point': row[3], 'contribution': row[4]
            } for row in cursor.fetchone()]
            return player

    def post_contribution(self, name):
        player = self.get_player(name)
        pass
    
    def record_match_result_v2(self, player_names, result, goals_scored):
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
                player = [player for player in players if player['name']==name][0]
                if result == "win":
                    player['point'] += 3
                    player['goals_scored'] += goals_scored[name]
                    player['appearance'] += 1
                elif result == "draw":
                    player['point'] += 1
                    player['goals_scored'] += goals_scored[name]
                    player['appearance'] += 1
                self.update_player(name, player['appearance'], player['goals_scored'], player['point'])
        self.push_to_sheet()

    def push_to_sheet(self):
        """
        Update Google Sheet with player data.
        """
        columns = ["Player", "Appearances", "Goals Scored", "Points", "Contribution"]
        players = self.get_all_players()
        df = pd.DataFrame([{
            'name': player['name'], 
            'appearance': player['appearance'], 
            'goals_scored': player['goals_scored'], 
            'point': player['point'], 
            'contribution': player['contribution']} for player in players]).sort_values(by=['point'], ascending=False)
        print(df)
        self.sheet.update([df.columns.values.tolist()] + df.values.tolist())



class RankingSystem:
    """
    Manages player rankings.
    """
    #PLAYERS = {}

    def __init__(self, player_sheet_name):
        """
        Initialize the RankingSystem with the player sheet name.
        """
        self.players = {}
        self.player_sheet_name = player_sheet_name
        self.sheet = self.get_player_sheet()

    def get_player_sheet(self):
        """
        Get the Google Sheets object for player details.
        """
        return GSPREAD_CLIENT.open(self.player_sheet_name).worksheet('Players')

    def add_player(self, name):
        """
        Add a player to the team.
        """
        #if name not in self.get_players():
        self.players[name] = Player(name)

    def get_players(self):
        """
        Get the list of players from the player sheet.
        """
        return [player[0] for player in self.sheet.get_all_values()[1:]]

    def record_match_result(self, player_names, result, goals_scored):
        """
        Record match results, update player stats, and record goals scored.
        """
        for name in player_names:
            if name not in self.players:
                self.add_player(name)
            player = self.players[name]
            player.add_appearance()
            if result == "win":
                player.add_points(3)
            elif result == "draw":
                player.add_points(1)
            player.add_goals(goals_scored[name])  # Record goals scored by the player
        self.update_player_sheet()  # Update player sheet after recording match result

    def record_match_result_v2(self, player_names, result, goals_scored):
        """
        Record match results, update player stats, and record goals scored.
        """
        players = self.get_players()
        for name in player_names:
            if name not in players:
                self.add_player(name)
                player = self.players[name]
                player.add_appearance()
                if result == "win":
                    player.add_points(3)
                elif result == "draw":
                    player.add_points(1)
                player.add_goals(goals_scored[name])  # Record goals scored by the player
            elif name in players:
                print('player exists!!!')
                player = self.players[name]
                player.add_appearance()
                if result == "win":
                    player.add_points(3)
                elif result == "draw":
                    player.add_points(1)
                player.add_goals(goals_scored[name])

        print(self.players)
        self.update_player_sheet()

    def record_offence(self, player_name):
        """
        Record offense and remove points from the player's total.
        """
        if player_name in self.players:
            player = self.players[player_name]
            player.deduct_points(2)

    def update_player_sheet(self):
        """
        Update Google Sheet with player data.
        """
        df = pd.DataFrame(self.sheet.get_all_records())
        print(df)
        columns = ["Player", "Appearances", "Goals Scored", "Points", "Contribution"]
        if df.empty:
            for player in self.players.values():
                df = pd.concat([pd.DataFrame([[player.name, player.appearances, player.goals_scored, player.points, player.contribution]], columns=columns), df], ignore_index=True)
            #self.sheet.update([df.columns.values.tolist()] + df.values.tolist())
        else:
            for player in self.players.values():
                print([player.name, player.appearance, player.goals_scored, player.points, player.contribution])
                if player.name in df.Player:
                    df.loc[df.Player == player.name, columns] = [player.name, player.appearance, player.goals_scored, player.points, player.contribution]
                else:
                    df = pd.concat([pd.DataFrame([[player.name, player.appearances, player.goals_scored, player.points, player.contribution]], columns=columns), df], ignore_index=True)
        self.sheet.update([df.columns.values.tolist()] + df.values.tolist()) 


    def display_rankings(self):
        """
        Display player rankings.
        """
        sorted_players = sorted(self.players.values(), key=lambda x: x.points, reverse=True)
        print("Rankings:")
        for i, player in enumerate(sorted_players, 1):
            print(f"{i}. {player}")


class ContributionSystem:
    """
    Manages player contributions and expenses.
    """

    def __init__(self, contribution_sheet_name):
        """
        Initialize the ContributionSystem with the contribution sheet name.
        """
        self.contribution_sheet_name = contribution_sheet_name
        self.sheet = self.get_contribution_sheet()

    def get_contribution_sheet(self):
        """
        Get the Google Sheets object for contribution details.
        """
        return GSPREAD_CLIENT.open(self.contribution_sheet_name).worksheet('Contributions')

    def record_contribution(self, player_name, amount):
        """
        Record player's financial contribution.
        """

        self.sheet.append_row([player_name, amount])

    def record_expenses(self, expenses):
        """
        Record team expenses.
        """
        self.sheet.append_row(["Expenses", expenses])

    def update_balance(self):
        """
        Update the balance after deducting expenses.
        """
        contributions = self.sheet.col_values(2)[1:]
        expenses = float(self.sheet.acell('B2').value)
        total_balance = sum(map(float, contributions)) - expenses
        self.sheet.append_row(["Balance", total_balance])


def admin_login():
    """
    Checks admin credentials.
    """
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    # Add your desired admin username and password here
    admin_username = "admin"
    admin_password = "password"

    if username == admin_username and password == admin_password:
        return True
    else:
        return False


def main():
    """
    Main function to run the application.
    """
    create_player_table()
    player_sheet_name = "Fairview_Football_All_Stars_Contributions"
    contribution_sheet_name = "Fairview_Football_All_Stars_Contributions"


    ranking_system = RankingSystem_v2(player_sheet_name)
    contribution_system = ContributionSystem(contribution_sheet_name)

    # if not admin_login():
    #     print("Invalid credentials. Access denied.")
    #     return

    while True:
        print("\nSelect an option:")
        print("1. Record match result")
        print("2. Record player contribution")
        print("3. Record team expenses")
        print("4. Update player rankings")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            player_names = input("Enter player names (comma-separated): ").split(",")
            player_names = [name.strip() for name in player_names]
            result = input("Enter match result (win/draw): ")
            goals_scored = {}
            for name in player_names:
                goals = int(input(f"Enter goals scored by {name}: "))
                goals_scored[name] = goals
            ranking_system.record_match_result_v2(player_names, result, goals_scored)
        elif choice == "2":
            player_name = input("Enter player name: ")
            player_name = [name.strip() for name in player_name][0]
            ranking_system.post_contribution(player_name)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
