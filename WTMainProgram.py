"""CLI UI (to hopefully move to GUI Later)"""

import json
from datetime import datetime

def load_user_data():
    try:
        with open("user_data.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(users):
    with open("user_data.json", "w") as file:
        json.dump(users, file, indent=4)

users = load_user_data()
current_user = None

def main_menu():
    print("\nWelcome to the Water Tracker App!")
    print("1. Login/Register")
    print("2. Enter Water Intake")
    print("3. Copy Last Entry")
    print("4. View Daily Average")
    print("5. View Weekly Average")
    print("6. View Monthly Average")
    print("7. View All History")
    print("8. Undo Last Entry")
    print("9. Delete a Specific Entry")
    print("10. Help")
    print("11. Exit")
    choice = input("Choose an option: ")
    return choice

def help_menu():
    print("\nHelp Menu:")
    print("1. Benefits of Logging Water Intake: Keeps you hydrated, improves health.")
    print("2. How to Use Features: Navigate using menu numbers to log and view water intake.")
    print("3. Undo Feature: Revert your last logged intake.")
    print("4. Delete Specific Entry: Remove a particular entry from your history.")
    print("5. Copy Last Entry: Repeat your last water intake entry.")
    print("6. View Options: You can view detailed logs or summaries.")
    print("7. Help Menu: Provides information about all features.")
    print("8. Exit: Safely close the application.")
    input("Press any key to return to the main menu...")

def register_login():
    global current_user
    print("\nRegister/Login")
    username = input("Enter username: ")
    if username in users:
        current_user = username
        print(f"Welcome back, {username}!")
    else:
        users[username] = []
        current_user = username
        print(f"Registration complete. Welcome, {username}!")
        save_user_data(users)

def enter_water_intake():
    if current_user:
        amount = input("Enter water intake in milliliters: ")
        try:
            amount = int(amount)
            entry = {"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "amount": amount}
            users[current_user].append(entry)
            print(f"Recorded {amount}ml of water intake on {entry['date']}.")
            save_user_data(users)
        except ValueError:
            print("Invalid input. Please enter a number.")
    else:
        print("Please log in first.")

def copy_last_entry():
    if current_user and users[current_user]:
        last_entry = users[current_user][-1]
        users[current_user].append(last_entry)
        print(f"Copied last entry: {last_entry['amount']}ml on {last_entry['date']}.")
        save_user_data(users)
    else:
        print("No entry to copy or please log in first.")

def view_history():
    if current_user:
        if users[current_user]:
            print(f"\nWater Intake History for {current_user}:")
            for index, entry in enumerate(users[current_user], start=1):
                print(f"{index}. {entry['date']}: {entry['amount']}ml")
        else:
            print("No history to display.")
    else:
        print("Please log in first.")

def undo_last_entry():
    if current_user and users[current_user]:
        removed = users[current_user].pop()
        print(f"Removed last entry: {removed['amount']}ml on {removed['date']}")
        save_user_data(users)
    else:
        print("No entry to undo or please log in first.")

def delete_specific_entry():
    if current_user:
        if users[current_user]:
            print("\nSelect an entry to delete:")
            for index, entry in enumerate(users[current_user], start=1):
                print(f"{index}. {entry['date']}: {entry['amount']}ml")
            selection = int(input("Enter the number of the entry to delete: "))
            if 1 <= selection <= len(users[current_user]):
                removed = users[current_user].pop(selection - 1)
                print(f"Deleted entry: {removed['amount']}ml on {removed['date']}")
                save_user_data(users)
            else:
                print("Invalid selection. No entry deleted.")
        else:
            print("No history to display.")
    else:
        print("Please log in first.")

import requests

def calculate_average(period, data):
    url = f'http://localhost:5000/average/{period}'  # Adjust this URL based on your microservice deployment
    response = requests.post(url, json={"data": data})
    if response.status_code == 200:
        return response.json()['average']
    else:
        print("Failed to calculate average:", response.json()['error'])
        return None

def view_average_history(period):
    if current_user:
        if users[current_user]:
            print(f"\nCalculating {period} average for {current_user}:")
            user_data = [{"date": entry['date'], "value": entry['amount']} for entry in users[current_user]]
            average = calculate_average(period, user_data)
            if average is not None:
                print(f"The {period} average water intake is: {average}ml")
        else:
            print("No data to calculate.")
    else:
        print("Please log in first.")


def user_session():
    while True:
        choice = main_menu()
        if choice == '1':
            register_login()
        elif choice == '2':
            enter_water_intake()
        elif choice == '3':
            copy_last_entry()
        elif choice == '4':
            view_average_history('daily')
        elif choice == '5':
            view_average_history('weekly')
        elif choice == '6':
            view_average_history('monthly')
        elif choice == '7':
            view_history()
        elif choice == '8':
            undo_last_entry()
        elif choice == '9':
            delete_specific_entry()
        elif choice == '10':
            help_menu()
        elif choice == '11':
            print("Thank you for using the Water Tracker App!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    user_session()

