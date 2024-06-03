from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def load_users():
    """Loads user data from JSON file."""
    try:
        with open("user_data.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    """Saves user data to JSON file."""
    with open("user_data.json", "w") as file:
        json.dump(users, file, indent=4)

@app.route('/register', methods=['POST'])
def register():
    """Registers a new user."""
    users = load_users()
    username = request.json.get("username")
    print(f"Received request to register user: {username}")
    if username in users:
        return jsonify({"error": "User already exists"}), 400
    users[username] = []
    save_users(users)
    return jsonify({"status": "User registered"}), 200

@app.route('/login', methods=['POST'])
def login():
    """Logs in an existing user."""
    users = load_users()
    username = request.json.get("username")
    print(f"Received request to log in user: {username}")
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"status": "User logged in"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)

