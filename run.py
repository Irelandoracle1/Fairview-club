import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load Google Sheets credentials
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)


class Player:
    """
    Represents a player in the football team.
    """
    def __init__(self, name):
        """Initializes a player with their name."""
        self.name = name
        self.appearance = 0
        self.goals_scored = 0
        self.points = 0
        self.contribution = 0

    def add_appearance(self):
        """Increments the player's appearance count and points."""
        self.appearance += 1
        self.points += 1

    def add_goals(self, goals):
        """Increments the player's goals scored."""
        self.goals_scored += goals

    def add_points(self, points):
        """Adds points to the player's total."""
        self.points += points

    def deduct_points(self, points):
        """Deducts points from the player's total."""
        self.points -= points

    def add_contribution(self, amount):
        """Adds a financial contribution to the player's total."""
        self.contribution += amount

    def __str__(self):
        """Returns a string representation of the player."""
        return f"{self.name}: Appearances - {self.appearance}, Goals Scored - {self.goals_scored}, Points - {self.points}, Contribution - {self.contribution} euros"


class RankingSystem:
    """
    Manages player rankings and statistics.
    """
    def __init__(self, player_sheet_name):
        """Initializes the RankingSystem with the name of the player sheet."""
        self.players = {}
        self.player_sheet_name = player_sheet_name

    def get_player_sheet(self):
        """Gets the Google Sheet for player data."""
        return GSPREAD_CLIENT.open(self.player_sheet_name).sheet1

    def add_player(self, name):
        """Adds a new player to the system."""
        if name not in self.players:
            self.players[name] = Player(name)

    def record_match_result(self, player_names, result):
        """Records match results and updates player stats."""
        for name in player_names:
            if name in self.players:
                player = self.players[name]
                player.add_appearance()
                if result == "win":
                    player.add_points(3)
                elif result == "draw":
                    player.add_points(2)

    def record_offense(self, player_name):
        """Records offenses and deducts points from player's total."""
        if player_name in self.players:
            player = self.players[player_name]
            player.deduct_points(2)

    def update_player_sheet(self):
        """Updates Google Sheet with player data."""
        sheet = self.get_player_sheet()
        sheet.clear()
        sheet.append_row(["Player", "Appearance", "Goals Scored", "Points", "Contribution"])
        for player in self.players.values():
            sheet.append_row([player.name, player.appearance, player.goals_scored, player.points, player.contribution])

    def display_rankings(self):
        """Displays player rankings."""
        sorted_players = sorted(self.players.values(), key=lambda x: x.points, reverse=True)
        print("Rankings:")
        for i, player in enumerate(sorted_players, 1):
            print(f"{i}. {player}")


class ContributionSystem:
    """
    Manages player contributions and expenses.
    """
    def __init__(self, contribution_sheet_name):
        """Initializes the ContributionSystem with the name of the contribution sheet."""
        self.contribution_sheet_name = contribution_sheet_name

    def get_contribution_sheet(self):
        """Gets the Google Sheet for financial data."""
        return GSPREAD_CLIENT.open(self.contribution_sheet_name).sheet1

    def admin_enter_expenses(self):
        """Allows admin to add expenses."""
        if self.admin_login():
            expenses = float(input("Enter Total Expenses: "))
            self.record_expenses(expenses)
            self.update_balance()
            print("Expenses recorded and deducted from total balance.")
        else:
            print("Access Denied. Admin credentials required.")

    def record_expenses(self, expenses):
        """Records expenses in the contribution sheet."""
        sheet = self.get_contribution_sheet()
        expenses_cell = sheet.acell("C2")
        expenses_cell.value = str(expenses)

    def update_balance(self):
        """Updates the total balance after deducting expenses."""
        sheet = self.get_contribution_sheet()
        contributions = sheet.col_values(2)[1:]
        expenses = float(sheet.acell('C2').value)
        total_balance = sum(map(float, contributions)) - expenses
        balance_cell = sheet.acell('D2')
        balance_cell.value = str(total_balance)

    def admin_login(self):
        """Checks admin credentials."""
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        return username == "admin" and password == "password"

    def record_contribution(self, player_name, amount):
        """Records a financial contribution made by a player."""
        sheet = self.get_contribution_sheet()
        contributions = sheet.get_all_values()[1:]  # Exclude header row
        for row in contributions:
            if row[0] == player_name:
                row[1] = str(float(row[1]) + amount)
                break
        else:
            sheet.append_row([player_name, amount])


def main():
    """Runs the application."""
    player_sheet_name = "Players"
    contribution_sheet_name = "Fairview_ Football_ All_Stars_Contributions"
    ranking_system = RankingSystem(player_sheet_name)
    contribution_system = ContributionSystem(contribution_sheet_name)

    if not contribution_system.admin_login():
        print("Invalid credentials. Access denied.")
        return

    num_players = int(input("Enter the number of players: "))
    player_names = [input(f"Enter name for player {i+1}: ") for i in range(num_players)]

    for name in player_names:
        ranking_system.add_player(name)

    num_matches = int(input("Enter the number of matches played: "))
    for i in range(num_matches):
        players_involved = input(f"Enter player names involved in match {i+1} (comma-separated): ").split(',')
        result = input("Enter match result (win/draw): ")
        ranking_system.record_match_result(players_involved, result)

    num_offenses = int(input("Enter the number of offenses: "))
    for i in range(num_offenses):
        player_name = input(f"Enter the name of the player committing offense {i+1}: ")
        ranking_system.record_offense(player_name)

    num_contributions = int(input("Enter the number of contributions: "))
    for i in range(num_contributions):
        player_name = input(f"Enter the name of the player making contribution {i+1}: ")
        amount = float(input("Enter the amount of contribution: "))
        contribution_system.record_contribution(player_name, amount)

    contribution_system.admin_enter_expenses()
    contribution_system.update_balance()
    ranking_system.update_player_sheet()
    ranking_system.display_rankings()


if __name__ == "__main__":
    main()
