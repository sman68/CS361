import requests

def register_user(username):
    """Registers a new user."""
    print(f"Registering user: {username}")
    response = requests.post('http://localhost:5001/register', json={"username": username})
    return response.status_code == 200

def login_user(username):
    """Logs in an existing user."""
    print(f"Logging in user: {username}")
    response = requests.post('http://localhost:5001/login', json={"username": username})
    return response.status_code == 200

def log_water_intake(username, amount, date):
    """Logs water intake for a user."""
    data = {"username": username, "amount": amount, "date": date}
    print(f"Logging water intake for {username}: {amount}ml on {date}")
    response = requests.post('http://localhost:5002/log_water', json=data)
    return response.status_code == 200

def copy_last_entry(username):
    """Copies the last water intake entry for a user."""
    print(f"Copying last entry for {username}")
    response = requests.post('http://localhost:5003/copy_last_entry', json={"username": username})
    return response.status_code == 200

def undo_last_entry(username):
    """Undoes the last water intake entry for a user."""
    print(f"Undoing last entry for {username}")
    response = requests.post('http://localhost:5003/undo_last_entry', json={"username": username})
    return response.status_code == 200

def delete_entry(username, entry_number):
    """Deletes a specific water intake entry for a user."""
    print(f"Deleting entry number {entry_number} for {username}")
    response = requests.post('http://localhost:5003/delete_entry', json={"username": username, "entry_number": entry_number})
    return response.status_code == 200

def view_history(username):
    """Views the water intake history for a user."""
    print(f"Viewing history for {username}")
    response = requests.get('http://localhost:5002/view_history', params={"username": username})
    if response.status_code == 200:
        return response.json()
    return None

def calculate_average(period, data):
    """Calculates the average water intake for a given period."""
    print(f"Calculating {period} average")
    url = f'http://localhost:5004/average/{period}'
    response = requests.post(url, json={"data": data})
    if response.status_code == 200:
        return response.json()['average']
    return None

def get_random_quote():
    """Fetches a random inspirational quote."""
    print("Fetching a random quote")
    response = requests.get('http://localhost:5000/quotes')
    if response.status_code == 200:
        return response.json()["quote"]
    return None

def get_favorite_quotes():
    """Fetches the favorite quotes for a user."""
    print("Fetching favorite quotes")
    response = requests.get('http://localhost:5000/favorites')
    if response.status_code == 200:
        return response.json()
    return None

def favorite_quote(quote):
    """Favorites a quote for a user."""
    print(f"Favoriting quote: {quote}")
    response = requests.post('http://localhost:5000/favorite', json={"quote": quote})
    return response.status_code == 200
