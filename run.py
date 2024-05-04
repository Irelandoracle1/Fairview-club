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


class RankingSystem:
    """
    Manages player rankings.
    """

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
        if name not in self.get_players():
            self.players[name] = Player(name)

    def get_players(self):
        """
        Get the list of players from the player sheet.
        """
        return [player[0] for player in self.sheet.get_all_values()[1:]]

    def record_match_result(self, player_names, result):
        """
        Record match results and update player stats.
        """
        for name in player_names:
            if name in self.players:
                player = self.players[name]
                player.add_appearance()
                if result == "win":
                    player.add_points(3)
                elif result == "draw":
                    player.add_points(1)

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
        self.sheet.clear()
        self.sheet.append_row(["Player", "Appearances", "Goals Scored", "Points", "Contribution"])
        for player in self.players.values():
            self.sheet.append_row([player.name, player.appearances, player.goals_scored, player.points, player.contribution])

    def display_rankings(self):
        """
        Display player rankings.
        """
        sorted_players = sorted(self.players.values(), key=lambda x: x.points, reverse=True)
        print("Rankings:")
        for i, player in enumerate(sorted_players, 1):
            print(f"{i}. {player}")

    def record_match_result(self, player_names, result):
        """
        Record match results and update player stats.
        If a player is not found, add them dynamically.
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
    player_sheet_name = "Fairview_Football_All_Stars_Contributions"
    contribution_sheet_name = "Fairview_Football_All_Stars_Contributions"

    ranking_system = RankingSystem(player_sheet_name)
    contribution_system = ContributionSystem(contribution_sheet_name)

    if not admin_login():
        print("Invalid credentials. Access denied.")
        return

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
            result = input("Enter match result (win/draw): ")
            ranking_system.record_match_result(player_names, result)
            ranking_system.update_player_sheet()  # Update player sheet after recording match result
        elif choice == "2":
            player_name = input("Enter player name: ")
            if player_name not in ranking_system.players:
                ranking_system.add_player(player_name)
            amount = float(input("Enter contribution amount: "))
            ranking_system.players[player_name].add_contribution(amount)
            contribution_system.record_contribution(player_name, amount)
            ranking_system.update_player_sheet()  # Update player sheet after recording contribution
        elif choice == "3":
            expenses = float(input("Enter expenses amount: "))
            contribution_system.record_expenses(expenses)
            contribution_system.update_balance()
        elif choice == "4":
            ranking_system.update_player_sheet()
            ranking_system.display_rankings()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
