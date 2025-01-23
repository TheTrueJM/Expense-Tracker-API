# Expense Tracker API
A solution to the [Expense Tracker API](https://roadmap.sh/projects/expense-tracker-api) project available on [roadmap.sh](https://roadmap.sh).

This project is a simple RESTful API for expense tracking. Multiple users can authenticate to the application by username and password, with JSON Web Tokens (JWT) being used to handle user sessions. The API supports CRUD operations through HTTP request methods, for creating, reading, updating, and deleting expense data. The API is built using Flask and SQLAlchemy, interacting with an SQLite database.

## Features
- **User Sign-Up:** User's can sign up to the application with username and password
- **User Authentication:** User's can login to the application with their credentials, recieving a JWT to handle their session
- **Create Expense:** Create expense with a description, content, category, and cost amount
- **View Expenses:** All expenses of a user can be viewed with the expense details
- **Search Expenses:** Ability for a user to search for a specific expense by id, or filter expenses by specific time peroids
- **Update Expense:** Update the details of a user's existing expense
- **Delete Expense:** Delete a user's existing expense from the database

## Installation and Setup
```
git clone https://github.com/TheTrueJM/Expense-Tracker-API.git
cd Expense-Tracker-API
py -m venv .venv

# For Windows
source .venv/Scripts/activate
set FLASK_KEY=value # Set the application secret key to your choosing

# For Linux / MacOS
source .venv/bin/activate
export FLASK_KEY=value # Set the application secret key to your choosing

pip install -r requirements.txt
py ./main.py
```

## Usage
TODO
