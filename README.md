# Fairview Football Application

## Overview

The Fairview Football Application is a Python-based system designed to manage player statistics and contributions for a football team. It integrates with Google Sheets to store and update player data.
The Python program illustrates a football ranking system and player statistics management application with a SQLite database and a Google Sheet for player information. An interactive command-line interface allows users to input match results and player contributions, update player rankings and statistics, and track player contributions. 

The following is the output of the Python program when executed:
```python
Welcome To Fairview Football Application

Select an option:
1. Record match result
2. Record player contribution
3. Exit
Enter your choice: 1
Enter player names (comma-separated): shaun,martina,sam
Enter match result (win/draw): draw
Enter goals scored by shaun: 1
Enter goals scored by martina: 0
Enter goals scored by sam: 1
```


### Here Is The Live Version

  ![App image ](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview9.jpg)

   ![App image](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview1.jpg)

   ![App image](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview2.jpg)

   ![App image](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview3.jpg)

   ![App image](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview4.jpg)

   ![GApp image](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview5.jpg)

   ![App image](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview6.jpg)

   ![App image](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview7.jpg)

   ![App image](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview8.jpg)


## Features

- Record match results and update player statistics.
- Record player contributions.
- Store data in an SQLite database.
- Sync data with Google Sheets.

## Requirements

- Python 3.9
- `gspread`
- `google-auth`
- `pandas`
- `sqlite3`
- Google Cloud service account with access to Google Sheets API.
- A Google Sheet named "Fairview_Football_All_Stars_Contributions" with a worksheet named "Players".

## Setup

### Google Cloud Setup

1. Create a Google Cloud project.
2. Enable the Google Sheets API and Google Drive API.
3. Create a service account and download the JSON key file.
4. Share the Google Sheet with the service account email.

### Environment Setup

1. Clone the repository.
2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Place the downloaded `creds.json` file in the root directory of the project.

## Deployment

These are the steps I followed in deploying the application to Heroku:

- Steps For Deployment 
  - Fork or Clone this repository
  - Create a new Heroku App
  - Set the buildpack for Python and Nodejs 
  - Linked the Heroku App to this repository 
  - Clicked on 'Deploy Branch'

The live link can be found here - https://fairview-app-ffc01770d1ed.herokuapp.com/

## Usage

Run the application locally:

```bash 



on running, you'll be prompted to log in as an admin and presented with options to record match results, record player contributions, or exit the application.

Admin Login
Default admin credentials:

Username: admin
Password: password
Main Menu Options
Record match result: Enter player names, match result, and goals scored by each player.
Record player contribution: Enter player name and contribution amount.
Exit: Exit the application.
Code Explanation
Google Sheets Setup
The application uses gspread and google-auth to connect to Google Sheets:


import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
Database Connection
The DatabaseConnection class manages the SQLite database connections:


import sqlite3 as sq
import os

current_dir = os.getcwd()
database_path = os.path.join(current_dir, r'data.db')

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
Player Table
The create_player_table function creates the players table if it doesn't exist:


def create_player_table() -> None:
    with DatabaseConnection(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS players (name text primary key, appearance integer, goals_scored integer, point integer, contribution integer)')
Ranking System
The RankingSystem class handles all player-related operations:


class RankingSystem:
    def __init__(self, player_sheet_name):
        self.player_sheet_name = player_sheet_name
        self.sheet = self.get_player_sheet()

    def get_player_sheet(self):
        return GSPREAD_CLIENT.open(self.player_sheet_name).worksheet('Players')

    def add_player(self, name, appearance, goals_scored, point):
        with DatabaseConnection(database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO players VALUES (?, ?, ?, ?, 0)', (name, appearance, goals_scored, point))

    def update_player(self, name, appearance, goals_scored, point, contribution):
        with DatabaseConnection(database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('UPDATE players SET appearance=?, goals_scored=?, point=?, contribution=? where name=?', (appearance, goals_scored, point, contribution, name))

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
            cursor.execute('SELECT * FROM players where name=?', (name,))
            rows = cursor.fetchall()

            if not rows:
                return None
    
            player = [{
                    'name': row[0], 'appearance': row[1], 'goals_scored': row[2],
                    'point': row[3], 'contribution': row[4]
                } for row in rows][0]
            return player

def post_contribution(self, name, amount):
        player = self.get_player(name)
        if player:
            player['contribution'] += amount
            self.update_player(name, player['appearance'], player['goals_scored'], player['point'], player['contribution'])
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
                player = [player for player in players if player['name']==name][0]
                if result == "win":
                    player['point'] += 3
                    player['goals_scored'] += goals_scored[name]
                    player['appearance'] += 1
                elif result == "draw":
                    player['point'] += 1
                    player['goals_scored'] += goals_scored[name]
                    player['appearance'] += 1
                self.update_player(name, player['appearance'], player['goals_scored'], player['point'], player['contribution'])
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
        df.columns = columns
        self.sheet.update([df.columns.values.tolist()] + df.values.tolist())
Admin Login
The admin_login function checks the admin credentials:


def admin_login():
    """
    Checks admin credentials.
    """
    username = input("Enter admin username:\n ")
    password = input("Enter admin password:\n ")

    # Add your desired admin username and password here
    admin_username = "admin"
    admin_password = "password"

    if username == admin_username and password == admin_password:
        return True
    else:
        return False
- Main Function
- The  main function runs the application and presents the admin with options:


def main():
    """
    Main function to run the application.
    """
    create_player_table()
    player_sheet_name = "Fairview_Football_All_Stars_Contributions"
    ranking_system = RankingSystem(player_sheet_name)

    if not admin_login():
        print("Invalid credentials. Access denied.")
        return

    while True:
        print("\nWelcome To Fairview Football Application")
        print("\nSelect an option:")
        print("1. Record match result")
        print("2. Record player contribution")
        print("3. Exit")
        choice = input("Enter your choice:\n ")

        if choice == "1":
            player_names = input("Enter player names (comma-separated):\n ").split(",")
            player_names = [name.strip() for name in player_names]
            result = input("Enter match result (win/draw):\n ")
            goals_scored = {}
            for name in player_names:
                goals = int(input(f"Enter goals scored by {name}:\n "))
                goals_scored[name] = goals
            ranking_system.post_match_result(player_names, result, goals_scored)
        elif choice == "2":
            player_name = input("Enter player name:\n ")
            player = ranking_system.get_player(player_name)
            if player:
                contribution_amount = int(input("Enter contribution amount:\n "))
                ranking_system.post_contribution(player_name, contribution_amount)
        elif choice == "3":
            print("Exiting...\n Press 'RUN PROGRAM' to continue updating")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

## Testing 
 I have manually tested this application through this process
- I inputed wrong values. Such as adding empty values, string values and adding the same coordinates twice
- I passed the code through the PEP8online.com test and confirmed there is no error on my code
- Tested the App in my local terminal and also my Heroku hosted terminal
 
### Validator Testing 
-PEP8
 - Errors originally returnd from PEP8online.com were all fixed
 - Final code testing returned with a message: ALL RIGHT
 
### Bugs
   -As at the point of development, I encountered errors in player game class where existing players were added twice  so i fixed it by removing the code which was adding double players

### Unfixed Bugs

- No Bug is left unfixed


## Credits 
- Code Institute for the sample development template and the Love sandwiches development guide and sample
- Wikipedia for information about the Battleship game and History
- w3schools
- Stack overflow




