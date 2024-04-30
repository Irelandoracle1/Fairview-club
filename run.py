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
