from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
ma = Marshmallow(app)

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='FitnessCenter',
            user='user',  # Replace with your MySQL username
            password='password'  # Replace with your MySQL password
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

class MemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'phone')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

class WorkoutSessionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'member_id', 'session_date', 'duration', 'activity', 'notes')

workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

connection = create_connection()

@app.route('/members', methods=['POST'])
def add_member():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')

        # Check if all required fields are provided
        if not name or not email or not phone:
            print("Missing required member information.")
            return jsonify({"error": "Missing required member information."}), 400

        cursor = connection.cursor()
        query = "INSERT INTO Members (name, email, phone) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, phone))
        connection.commit()
        return member_schema.jsonify(data)
    except Error as e:
        print(f"Database Error: {e}")  # Log the database error
        return jsonify({"error": "An error occurred while adding the member."}), 500
    except Exception as e:
        print(f"Unexpected Error: {e}")  # Log any unexpected errors
        return jsonify({"error": "An unexpected error occurred."}), 500
    finally:
        cursor.close()

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM Members WHERE id = %s"
        cursor.execute(query, (id,))
        member = cursor.fetchone()
        if member:
            result = {'id': member[0], 'name': member[1], 'email': member[2], 'phone': member[3]}
            return jsonify(result)
        return jsonify({"error": "Member not found"}), 404
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while fetching the member."}), 500
    finally:
        cursor.close()

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    try:
        data = request.json
        name = data['name']
        email = data['email']
        phone = data['phone']
        cursor = connection.cursor()
        query = "UPDATE Members SET name = %s, email = %s, phone = %s WHERE id = %s"
        cursor.execute(query, (name, email, phone, id))
        connection.commit()
        return member_schema.jsonify(data)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while updating the member."}), 500
    finally:
        cursor.close()

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM Members WHERE id = %s"
        cursor.execute(query, (id,))
        connection.commit()
        return jsonify({"message": "Member deleted successfully"})
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while deleting the member."}), 500
    finally:
        cursor.close()

@app.route('/workouts', methods=['POST'])
def add_workout():
    cursor = None
    try:
        data = request.json
        member_id = data['member_id']
        session_date = data.get('session_date')  # Safely get 'session_date' key
        duration = data.get('duration')
        activity = data.get('activity')
        notes = data.get('notes', '')  # Default to empty string if 'notes' is not provided

        # Ensure that session_date, duration, and activity are provided
        if not session_date or not duration or not activity:
            return jsonify({"error": "Missing required workout session information."}), 400

        cursor = connection.cursor()
        query = "INSERT INTO WorkoutSessions (member_id, session_date, duration, activity, notes) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (member_id, session_date, duration, activity, notes))
        connection.commit()
        return workout_session_schema.jsonify(data)
    except Error as e:
        print(f"Database Error: {e}")  # Log the database error
        return jsonify({"error": "An error occurred while adding the workout session."}), 500
    except Exception as e:
        print(f"Unexpected Error: {e}")  # Log any unexpected errors
        return jsonify({"error": "An unexpected error occurred."}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/workouts/<int:member_id>', methods=['GET'])
def get_workouts(member_id):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM WorkoutSessions WHERE member_id = %s"
        cursor.execute(query, (member_id,))
        workouts = cursor.fetchall()
        results = []
        for workout in workouts:
            results.append({
                'id': workout[0],
                'member_id': workout[1],
                'session_date': workout[2],
                'duration': workout[3],
                'activity': workout[4],
                'notes': workout[5]
            })
        return jsonify(results)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while fetching the workout sessions."}), 500
    finally:
        cursor.close()

if __name__ == '__main__':
    app.run(debug=True)
