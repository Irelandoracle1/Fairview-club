# Fairview Football Application

## Overview

The Fairview Football Application is a Python-based system designed to manage player statistics and contributions for a football team. It integrates with Google Sheets to store and update player data. The Python program illustrates a football ranking system and player statistics management application with a SQLite database and a Google Sheet for player information. An interactive command-line interface allows users to input match results and player contributions, update player rankings and statistics, and track player contributions.

The following is the output of the Python program when executed:

Welcome To Fairview Football Application

Select an option:

Record match result
Record player contribution
Exit
Enter your choice: 1
Enter player names (comma-separated): shaun,martina,sam
Enter match result (win/draw): draw
Enter goals scored by shaun: 1
Enter goals scored by martina: 0
Enter goals scored by sam: 1


### Here Is The Live Version

![App image](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview9.jpg)
![App image](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview1.jpg)
![App image](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview2.jpg)
![App image](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview3.jpg)
![App image](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview4.jpg)
![App image](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview5.jpg)
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



pip install -r requirements.txt
Place the downloaded creds.json file in the root directory of the project.
Deployment
These are the steps I followed in deploying the application to Heroku:

Steps For Deployment
Fork or Clone this repository.
Create a new Heroku App.
Set the buildpack for Python and Node.js.
Link the Heroku App to this repository.
Click on 'Deploy Branch'.
The live link can be found here: https://fairview-app-ffc01770d1ed.herokuapp.com/

Usage
Run the application locally:


python main.py
On running, you'll be prompted to log in as an admin and presented with options to record match results, record player contributions, or exit the application.
Admin Login
Default admin credentials:

Username: admin
Password: password
Main Menu Options
Record match result: Enter player names, match result, and goals scored by each player.
Record player contribution: Enter player name and contribution amount.
Exit: Exit the application.
Testing
I have manually tested this application:

I inputted wrong values, such as adding empty values, string values, and adding the same coordinates twice.
I passed the code through the PEP8online.com test and confirmed there is no error in my code.
Tested the App in my local terminal and also my Heroku hosted terminal.
Validator Testing
pep8ci.herokuapp.com
Errors originally returned from pep8ci.herokuapp.com were fixed.
Final code testing returned with a message: "All clear, no errors found."
Bugs
During development, I encountered errors in the player game class where existing players were added twice. I fixed this by removing the code which was adding double players.
Unfixed Bugs
None
Credits
Code Institute for the sample development template and the Love sandwiches development guide and sample.
Wikipedia for information about the Battleship game and History.
w3schools
Stack Overflow


