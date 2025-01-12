# Fairview Football Application

The **Fairview Football Application** is a Python-based program designed to simplify the management of player statistics and financial contributions for the Fairview Football team. By integrating with Google Sheets and utilizing an SQLite database, this application ensures robust data handling and easy access for tracking and reporting purposes. It features an interactive command-line interface for user-friendly operations and offers tools to manage match results, player rankings, and contribution records efficiently.

---

## Features

### **Core Functionalities**
- **Record Match Results**:  
  Input match details, including the players involved, goals scored, and match outcomes, to automatically update player statistics and rankings.
  
- **Track Player Contributions**:  
  Log player contributions such as monetary donations or supplies, ensuring a transparent and well-maintained record of team support.

- **SQLite Database Integration**:  
  Player data is stored locally in an SQLite database for quick access and reliability, even when offline.

- **Google Sheets Synchronization**:  
  Automatically sync player statistics and contributions with a Google Sheet for backup, team management, or sharing with stakeholders.

### **Additional Features**
- **User Authentication**:  
  A basic authentication system to protect sensitive data from unauthorized access.

- **Data Validation**:  
  Input validation ensures accurate data entry, avoiding errors or duplication.

- **Dynamic Ranking System**:  
  Generate a ranking table based on player performance, including goals scored and other metrics.

- **Error Handling and Logging**:  
  Comprehensive error handling to manage invalid inputs or system failures, with detailed logs for debugging.

---

## Screenshots

Here are some screenshots showcasing the application's functionalities:

1. **Main Menu**  
   ![App Menu](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview4.jpg)

2. **Recording Match Results**  
   ![Match Result Recording](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview1.jpg)

3. **Viewing Player Statistics**  
   ![Player Stats Overview](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview2.jpg)

4. **Logging Player Contributions**  
   ![Contribution Recording](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview3.jpg)

5. **Overall App Workflow**  
   ![Fairview Football App](https://github.com/Irelandoracle1/Fairview-club/blob/main/images/fairview9.jpg)

For more images, visit the [GitHub repository images folder](https://github.com/Irelandoracle1/Fairview-club/tree/main/images).

---

## Prerequisites

### **Software and Libraries**
1. **Python**: Version 3.9 or higher.
2. **Python Libraries**:
   - `gspread` (Google Sheets integration)
   - `google-auth` (Authentication for Google APIs)
   - `pandas` (Data manipulation)
   - `sqlite3` (Local database management)

### **Google Cloud Configuration**
1. **Service Account**:  
   Set up a service account on Google Cloud to access the **Google Sheets API**. Download the JSON credentials file (`creds.json`).
2. **Google Sheet**:  
   Create a Google Sheet named `Fairview_Football_All_Stars_Contributions` with a worksheet titled `Players`. Share the sheet with the service account email.

---

## Setup

### **Step 1: Clone the Repository**
Clone the project repository to your local machine:
```bash
git clone https://github.com/Irelandoracle1/Fairview-club.git
Step 2: Create a Virtual Environment
Navigate to the project directory and set up a Python virtual environment:


cd Fairview-club
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
Step 3: Install Dependencies
Install all required Python libraries:


pip install -r requirements.txt
Step 4: Add Credentials
Place the creds.json file in the project root directory. Ensure it has the proper permissions.

Step 5: Run the Application
Execute the program from the command line:


python3 run.py
Usage
Logging In
Start the application.
Use the default admin credentials:
Username: admin
Password: password
Navigating the App
The app provides the following options in its main menu:

Record Match Results:
Enter player names, goals scored, and match details to update statistics.
Track Player Contributions:
Log contributions with details such as amount, type, and player name.
Exit Application:
Safely close the program, ensuring all data is saved locally and synced to Google Sheets.
Deployment
Local Deployment
Follow the setup instructions above to run the application locally on your machine.

Heroku Deployment
Fork or clone the repository.
Create a new app on Heroku.
Add the necessary buildpacks for Python and Node.js.
Deploy the application using the Heroku CLI or directly via the GitHub repository.
🔗 Live Demo: Fairview Football Application on Heroku

Testing
Manual Testing
The application was manually tested using the following scenarios:

Valid and Invalid Inputs:
Entered correct and incorrect data types (e.g., text in numeric fields).
Tested empty input scenarios.
Database Operations:
Verified that player data is saved correctly in SQLite and updated upon edits.
Google Sheets Integration:
Confirmed that changes in the app reflect accurately in the linked Google Sheet.
Error Handling:
Simulated network errors and missing files to ensure proper error messages.
PEP8 Validation
The codebase was validated for compliance with Python's PEP8 style guide using PEP8 Validator.
Result: No errors or warnings found.

Known Issues
Unfixed Bugs: None reported.
Resolved Bugs:
Fixed an issue with duplicate player entries caused by redundant database queries.
Credits
Code Institute: Provided templates and learning resources.
Online Resources:
Wikipedia
W3Schools
Stack Overflow
Contributors:
Oluwaseyi Badero
For more details, visit the GitHub repository.