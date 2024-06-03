from flask import Flask, request, jsonify
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

@app.route('/copy_last_entry', methods=['POST'])
def copy_last_entry():
    """Copies the last water intake entry for a user."""
    users = load_user_data()
    username = request.json.get("username")
    print(f"Received request to copy last entry for {username}")
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    if not users[username]:
        return jsonify({"error": "No entries to copy"}), 400
    last_entry = users[username][-1]
    users[username].append(last_entry)
    save_user_data(users)
    return jsonify({"status": "Last entry copied"}), 200

@app.route('/undo_last_entry', methods=['POST'])
def undo_last_entry():
    """Undoes the last water intake entry for a user."""
    users = load_user_data()
    username = request.json.get("username")
    print(f"Received request to undo last entry for {username}")
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    if not users[username]:
        return jsonify({"error": "No entries to undo"}), 400
    users[username].pop()
    save_user_data(users)
    return jsonify({"status": "Last entry undone"}), 200

@app.route('/delete_entry', methods=['POST'])
def delete_entry():
    """Deletes a specific water intake entry for a user."""
    users = load_user_data()
    username = request.json.get("username")
    entry_number = request.json.get("entry_number")
    print(f"Received request to delete entry number {entry_number} for {username}")
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    try:
        entry_number = int(entry_number)
    except ValueError:
        return jsonify({"error": "Invalid entry number"}), 400
    if entry_number < 1 or entry_number > len(users[username]):
        return jsonify({"error": "Entry number out of range"}), 400
    users[username].pop(entry_number - 1)
    save_user_data(users)
    return jsonify({"status": "Entry deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5003)
