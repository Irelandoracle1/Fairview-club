import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS= Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Fairview_ Football_ All_Stars_Contributions')

players = SHEET.worksheet('players')
data = players.get_all_values()
print(data)

class player:
    """
    created a class to represents player
    which will include functions to initialize players names,
    function to increment player apperances, goals  scored, function to 
    add points to player total, deduct points for offences, add financial contributions
    """
    def _init_ (self, name):
        self.name = name
        self.appearance = 0
        self.goals_scored = 0
        self.points = 0
        self.contribution = 0

    def add_appearance(self):
        self.appearance += 1
        self.points += 1   

    def add_goals(self, goals):
        self.goals += goals

    def add_points(self, points):
        self.points += points

    def deduct_points(self, points):
        self.points -= points

    def add_contribution(self, amount):
        self.contribution += amount    

    def _str_(self):
        """
        this will return a string representing the players
        """
        return f"{self.name}: Appearances -{self.appearances} ,Goal Scored- {self.goals_scored}, Points{self.points}, Contribution{self.contribution} euros,"  


class RankingSystem:
    """
    This class is to manage  player rankings.
    """
    def _init_(self,player):
        """
        this will initialize the rankingSystem with the name of the 
        player sheet
        """
        self.players = {}
        self.player=player
        self.gc = self.authorize_google_sheets()

    def get_player_sheet(self):
        """
        this will get google sheet for player details
        """
        return self.gc.open(self.player_sheet_name).sheet1

    def add_player(self,name):
        """
        add player to file   
        """
        if name not in self.players:
            self.players[name]  = player(name) 

    def record_match_result(self, player_name, result):
        """
        this will record match results and update player stats
        """      
        for name in player_name:
            if name in self.players:
                player = self.players[name]
                player.add_appearance()
                if result == "win":
                    player.add_points(3)
                elif result == "draw":
                    player.add_points(2)  

    def record_offence(self,player_name):
        """
        This will record offense and remove from player points
        """
        if player_name in self.player:
            player = self.players[player_name]
            player.deduct_points(2)


    def update_player_sheet(self):
        """
        this will update google sheet with player data
        """
        sheet = self.get_player_sheet()
        sheet.clear()
        sheet.append_row(["player","appearance", "Goals Scored",
         "Points", "Contribution"])

        for player in self.players.values():
            sheet.append_row([player.name,player.appearance,
            player.goals_scored,player.points,player.contribution])


    def display_ranking(self):
        """
        this will display player ranking on table
        """
        sorted_player = sorted(self.player.values(), key = lambda x:
        x.points, reverse = True)
        print("Rankings")
        for i, players in enumerate(sorted_players, 1):
            print(f"{i}.{player}")


class ContributionSystem:
    """
    This class will manage player contributions and expenses 
    made by admin
    """
    def _init_(self, contributions):
        """
        this function will initialize contribution system 
        """
        self.contributions = contributions
        self.gc = self.authorize_google_sheets()

    def get_contribution_sheet(self):
        """
        gets the google sheet for 
        finalcial data
        """
        return self.gc.open(self.contributions).sheet1          


    def admin_enter_expenses(self):
        """
        This will allow admin to add expenses
        """
        if admin_login():
            expenses = float(input("Enter Total Expenses"))
            self.record_expenses(expenses)
            self.update_balance()
            print("Expenses record and deducted from total balance")

        else:
            print("Access Denied. Admin details required")     
