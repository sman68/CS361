from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def load_user_data():
    try:
        with open("user_data.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(users):
    with open("user_data.json", "w") as file:
        json.dump(users, file, indent=4)

@app.route('/register', methods=['POST'])
def register_user():
    users = load_user_data()
    username = request.json.get('username')
    if username in users:
        return jsonify({'status': 'User already exists'}), 400
    users[username] = []
    save_user_data(users)
    return jsonify({'status': 'User registered successfully'}), 200

@app.route('/login', methods=['POST'])
def login_user():
    users = load_user_data()
    username = request.json.get('username')
    if username not in users:
        return jsonify({'status': 'User not found'}), 404
    return jsonify({'status': 'User logged in successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
