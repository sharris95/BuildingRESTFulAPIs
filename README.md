Fitness Center Management System
Overview
This project is a basic Flask web application created to manage a fitness center's database. It focuses on handling information about members and their workout sessions. This project is a practical exercise to learn about building RESTful APIs, working with databases using MySQL, and implementing CRUD functionalities.

Features
Members Management:

Add new members
Retrieve member details
Update member information
Delete members
Workout Sessions Management:

Schedule new workout sessions for members
Retrieve all workout sessions for a specific member
Technologies Used
Python: For the backend logic
Flask: For building the web APIs
MySQL: For storing data about members and workout sessions
Flask-Marshmallow: For easy serialization/deserialization of data
Project Structure
app.py: The main file containing all the routes and database operations.
requirements.txt: Lists the packages required to run the application.
README.md: This document, providing an overview and instructions.
Setup Instructions
Prerequisites
Python 3.x installed on your machine
MySQL server setup and running
Installation
Clone the repository:


git clone <repository-url>
cd <repository-folder>
Create a virtual environment:

python -m venv flask_stage_venv
source flask_stage_venv/bin/activate  # On Windows, use `flask_stage_venv\Scripts\activate`
Install dependencies:


pip install -r requirements.txt
Set up the MySQL database:

Create a database called FitnessCenter.

Run these SQL commands to set up the tables:


CREATE TABLE Members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL
);

CREATE TABLE WorkoutSessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    session_date DATE NOT NULL,
    duration INT NOT NULL,
    activity VARCHAR(100) NOT NULL,
    notes TEXT,
    FOREIGN KEY (member_id) REFERENCES Members(id)
);
Run the Flask application:


python app.py
The app should now be running at http://127.0.0.1:5000.

API Endpoints
Members
POST /members: Add a new member

Request Body: JSON with name, email, and phone
GET /members/int:id: Get details of a specific member

PUT /members/int:id: Update member details

Request Body: JSON with name, email, and phone
DELETE /members/int:id: Remove a member

Workout Sessions
POST /workouts: Add a new workout session

Request Body: JSON with member_id, session_date, duration, activity, and notes
GET /workouts/int:member_id: Get all workout sessions for a member

Error Handling
The app includes error handling for issues like missing data or database errors. It will return appropriate messages and HTTP status codes if something goes wrong.

Contribution
If you want to improve this project, feel free to fork the repository and submit a pull request.

License
This project is open-source and is available under the MIT License.

Acknowledgements
This project was created as part of a coding bootcamp assignment to practice building RESTful APIs and working with databases using Flask and MySQL.






