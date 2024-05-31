from flask import Flask, request, jsonify
from datetime import datetime
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

@app.route('/log_water', methods=['POST'])
def log_water():
    """Endpoint to log water intake for a user."""
    users = load_user_data()
    username = request.json.get('username')
    amount = request.json.get('amount')
    date_str = request.json.get('date')
    try:
        date = datetime.strptime(date_str, '%m/%d/%Y')
    except ValueError:
        return jsonify({'status': 'Invalid date format'}), 400
    entry = {"date": date.strftime("%Y-%m-%d %H:%M:%S"), "amount": amount}
    users[username].append(entry)
    save_user_data(users)
    return jsonify({'status': 'Water intake logged successfully'}), 200

@app.route('/view_history', methods=['GET'])
def view_history():
    """Endpoint to view water intake history for a user."""
    users = load_user_data()
    username = request.args.get('username')
    if username not in users:
        return jsonify({'status': 'User not found'}), 404
    return jsonify(users[username]), 200

if __name__ == '__main__':
    app.run(debug=True, port=5002)
