# Expense Tracker API
A solution to the [Expense Tracker API](https://roadmap.sh/projects/expense-tracker-api) project available on [roadmap.sh](https://roadmap.sh).

This project is a simple RESTful API for expense tracking. Multiple users can authenticate to the application by a username and password, with JSON Web Tokens (JWT) being used to handle user sessions. The API supports CRUD operations through HTTP request methods, for creating, reading, updating, and deleting expense data. The API is built using Flask and SQLAlchemy, interacting with an SQLite database.

## Features
- **User Sign Up:** User's can sign up to the application with username and password
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
### User Sign Up
```
POST http://localhost:5000/signup
Content-Type: application/json

{
  "username": "NewUser",
  "password": "MyPassword"
}
```
> HTTP Responses: 201, 400, 401
```json
{
  "message": "Successful new user sign up"
}
```

### User Login
```
POST http://localhost:5000/login
Content-Type: application/json

{
  "username": "NewUser",
  "password": "MyPassword"
}
```
> HTTP Responses: 200, 400, 401
```json
{
  "jwt-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Ik5ld1VzZXIiLCJleHAiOjE3Mzc2OTE3ODl9.QSjceDdq4-ikURxai3VX9mcUxuf4AdC9Z9df9jfQ92Y",
  "message": "Successful user login"
}
```

### Create Expense
```
POST http://localhost:5000/expenses
jwt-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Ik5ld1VzZXIiLCJleHAiOjE3Mzc2OTE3ODl9.QSjceDdq4-ikURxai3VX9mcUxuf4AdC9Z9df9jfQ92Y
Content-Type: application/json

{
  "description": "Lunch Ingredients",
  "category": "Groceries",
  "amount": 20.0
}
```
> HTTP Responses: 201, 400, 401
```json
{
  "expense": {
    "amount": 20.0,
    "category": "Groceries",
    "date": "Fri, 24 Jan 2025 00:00:00 GMT",
    "description": "Lunch Ingredients",
    "id": 1,
    "username": "NewUser"
  }
}
```

### View and Filter Expenses
```
GET http://localhost:5000/expenses
jwt-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Ik5ld1VzZXIiLCJleHAiOjE3Mzc2OTE3ODl9.QSjceDdq4-ikURxai3VX9mcUxuf4AdC9Z9df9jfQ92Y
```
> Optional Time Parameters
```
?time-period=week # month three-months
?time-start=2025-01-24
?time-end=2025-01-24
```
> HTTP Responses: 200, 400, 401
```json
{
  "expenses": [
    {
      "amount": 20.0,
      "category": "Groceries",
      "date": "Fri, 24 Jan 2025 00:00:00 GMT",
      "description": "Lunch Ingredients",
      "id": 1,
      "username": "NewUser"
    },
    {
      "amount": 87.5,
      "category": "Electronics",
      "date": "Fri, 26 Jan 2025 00:00:00 GMT",
      "description": "New Headset",
      "id": 4,
      "username": "NewUser"
    },
  ]
}
```

### View Expense
```
GET http://localhost:5000/expenses/1
jwt-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Ik5ld1VzZXIiLCJleHAiOjE3Mzc2OTE3ODl9.QSjceDdq4-ikURxai3VX9mcUxuf4AdC9Z9df9jfQ92Y
```
> HTTP Responses: 200, 400, 401, 404
```json
{
  "expense": {
    "amount": 20.0,
    "category": "Groceries",
    "date": "Fri, 24 Jan 2025 00:00:00 GMT",
    "description": "Lunch Ingredients",
    "id": 1,
    "username": "NewUser"
  }
}
```


### Update Expense
```
PUT http://localhost:5000/expenses/14
jwt-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Ik5ld1VzZXIiLCJleHAiOjE3Mzc2OTE3ODl9.QSjceDdq4-ikURxai3VX9mcUxuf4AdC9Z9df9jfQ92Y
Content-Type: application/json

{
  "description": "Family Lunch Supplies",
  "category": "Groceries",
  "amount": 35.0
}
```
> HTTP Responses: 200, 400, 401, 404
```json
{
  "expense": {
    "amount": 35.0,
    "category": "Groceries",
    "date": "Fri, 24 Jan 2025 00:00:00 GMT",
    "description": "Family Lunch Supplies",
    "id": 1,
    "username": "NewUser"
  }
}
```


### Delete Expense
```
DELETE http://localhost:5000/expenses/1
jwt-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Ik5ld1VzZXIiLCJleHAiOjE3Mzc2OTE3ODl9.QSjceDdq4-ikURxai3VX9mcUxuf4AdC9Z9df9jfQ92Y
```
> HTTP Responses: 204, 400, 401, 404
