# Togetherly Flask
=====================

A simple Flask application for user registration, login, and profile management.

## Features

* User registration with email and password
* User login with email and password
* User profile management with name, username, email, and bio
* Post creation and management

## Requirements

* Python 3.8+
* Flask 2.0+
* Flask-SQLAlchemy 2.5+
* SQLite 3.30+

## Installation

1. Clone the repository: `git clone https://github.com/Kashish2314/togetherly-flask.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (on Linux/Mac) or `venv\Scripts\activate` (on Windows)
4. Install the required packages: `pip install -r requirements.txt`
5. Create the database: `python app.py db init`
6. Run the application: `python app.py`

## Usage

1. Open a web browser and navigate to `http://localhost:5000`
2. Register a new user by filling out the registration form
3. Log in with your email and password
4. Create a new post by filling out the post form
5. View and manage your profile by clicking on your username

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

* Flask: A lightweight web framework for Python
* Flask-SQLAlchemy: A SQL toolkit for Flask
* SQLite: A self-contained, file-based database
