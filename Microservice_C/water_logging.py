from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

def load_user_data():
    """Loads user data from JSON file."""
    try:
        with open("user_data.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(users):
    """Saves user data to JSON file."""
    with open("user_data.json", "w") as file:
        json.dump(users, file, indent=4)

@app.route('/log_water', methods=['POST'])
def log_water():
    """Logs water intake for a user."""
    users = load_user_data()
    username = request.json.get("username")
    amount = request.json.get("amount")
    date_str = request.json.get("date")
    print(f"Received request to log water intake for {username}: {amount}ml on {date_str}")
    try:
        date = datetime.strptime(date_str, '%m/%d/%Y')
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    entry = {"date": date.strftime("%Y-%m-%d %H:%M:%S"), "amount": amount}
    users[username].append(entry)
    save_user_data(users)
    return jsonify({"status": "Water intake logged"}), 200

@app.route('/view_history', methods=['GET'])
def view_history():
    """Views the water intake history for a user."""
    users = load_user_data()
    username = request.args.get("username")
    print(f"Received request to view history for {username}")
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify(users[username]), 200

if __name__ == "__main__":
    app.run(debug=True, port=5002)
