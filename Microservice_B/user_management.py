from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def load_user_data():
    """Loads user data from a JSON file."""
    try:
        with open("user_data.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(users):
    """Saves user data to a JSON file."""
    with open("user_data.json", "w") as file:
        json.dump(users, file, indent=4)

@app.route('/register', methods=['POST'])
def register():
    """Endpoint to register a new user."""
    users = load_user_data()
    username = request.json.get('username')
    if username in users:
        return jsonify({'status': 'User already exists'}), 400
    users[username] = []
    save_user_data(users)
    return jsonify({'status': 'User registered successfully'}), 200

@app.route('/login', methods=['POST'])
def login():
    """Endpoint to log in an existing user."""
    users = load_user_data()
    username = request.json.get('username')
    if username not in users:
        return jsonify({'status': 'User not found'}), 404
    return jsonify({'status': 'User logged in successfully'}), 200

if __name__ == '__main__':
    # Run the Flask application on port 5001
    app.run(debug=True, port=5001)
