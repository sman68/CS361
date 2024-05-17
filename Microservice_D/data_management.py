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

@app.route('/copy_last_entry', methods=['POST'])
def copy_last_entry():
    users = load_user_data()
    username = request.json.get('username')
    if username not in users or not users[username]:
        return jsonify({'status': 'No entry to copy'}), 404
    last_entry = users[username][-1]
    users[username].append(last_entry)
    save_user_data(users)
    return jsonify({'status': 'Last entry copied successfully'}), 200

@app.route('/undo_last_entry', methods=['POST'])
def undo_last_entry():
    users = load_user_data()
    username = request.json.get('username')
    if username not in users or not users[username]:
        return jsonify({'status': 'No entry to undo'}), 404
    removed = users[username].pop()
    save_user_data(users)
    return jsonify({'status': f'Removed entry: {removed["amount"]}ml on {removed["date"]}'}), 200

@app.route('/delete_entry', methods=['POST'])
def delete_entry():
    users = load_user_data()
    username = request.json.get('username')
    entry_number = request.json.get('entry_number')
    if username not in users or entry_number > len(users[username]):
        return jsonify({'status': 'Entry not found'}), 404
    removed = users[username].pop(entry_number - 1)
    save_user_data(users)
    return jsonify({'status': f'Entry deleted: {removed["amount"]}ml on {removed["date"]}'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5003)
