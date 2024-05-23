import requests

def register_user(username):
    response = requests.post('http://localhost:5001/register', json={"username": username})
    return response.status_code == 200

def login_user(username):
    response = requests.post('http://localhost:5001/login', json={"username": username})
    return response.status_code == 200

def log_water_intake(username, amount, date):
    data = {"username": username, "amount": amount, "date": date}
    response = requests.post('http://localhost:5002/log_water', json=data)
    return response.status_code == 200

def copy_last_entry(username):
    response = requests.post('http://localhost:5003/copy_last_entry', json={"username": username})
    return response.status_code == 200

def undo_last_entry(username):
    response = requests.post('http://localhost:5003/undo_last_entry', json={"username": username})
    return response.status_code == 200

def delete_entry(username, entry_number):
    response = requests.post('http://localhost:5003/delete_entry', json={"username": username, "entry_number": entry_number})
    return response.status_code == 200

def view_history(username):
    response = requests.get('http://localhost:5002/view_history', params={"username": username})
    if response.status_code == 200:
        return response.json()
    return None

def calculate_average(period, data):
    url = f'http://localhost:5000/average/{period}'
    response = requests.post(url, json={"data": data})
    if response.status_code == 200:
        return response.json()['average']
    return None

def get_random_quote():
    response = requests.get('http://localhost:5000/quotes')
    if response.status_code == 200:
        return response.json()["quote"]
    return None

def get_favorite_quotes():
    response = requests.get('http://localhost:5000/quotes/favorites')
    if response.status_code == 200:
        return response.json()
    return None

def favorite_quote(quote):
    response = requests.post('http://localhost:5000/quotes/favorite', json={"quote": quote})
    return response.status_code == 201
