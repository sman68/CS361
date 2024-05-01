"""CLI UI (to hopefully move to GUI Later)"""

def main_menu():
    print("\nWelcome to the Water Tracker App!")
    print("1. Login/Register")
    print("2. Enter Water Intake")
    print("3. View History")
    print("4. Undo Last Entry")
    print("5. Help")
    print("6. Exit")
    choice = input("Choose an option: ")
    return choice

def help_menu():
    print("\nHelp Menu:")
    print("1. Benefits of Logging Water Intake: Keeps you hydrated, improves health.")
    print("2. How to Use Features: Navigate using menu numbers to log and view water intake.")
    print("3. Undo Feature: Revert your last logged intake.")
    print("4. View Options: You can view detailed logs or summaries.")
    input("Press any key to return to the main menu...")

# Simple user management
users = {}
current_user = None

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

# Simple water intake tracking
def enter_water_intake():
    if current_user:
        amount = input("Enter water intake in milliliters: ")
        try:
            amount = int(amount)
            users[current_user].append(amount)
            print(f"Recorded {amount}ml of water intake.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    else:
        print("Please log in first.")

# Viewing history
def view_history():
    if current_user:
        if users[current_user]:
            print(f"\nWater Intake History for {current_user}:")
            for index, amount in enumerate(users[current_user], start=1):
                print(f"{index}. {amount}ml")
        else:
            print("No history to display.")
    else:
        print("Please log in first.")

# Undo functionality
def undo_last_entry():
    if current_user and users[current_user]:
        removed = users[current_user].pop()
        print(f"Removed last entry: {removed}ml")
    else:
        print("No entry to undo or please log in first.")

def user_session():
    while True:
        choice = main_menu()
        if choice == '1':
            register_login()
        elif choice == '2':
            enter_water_intake()
        elif choice == '3':
            view_history()
        elif choice == '4':
            undo_last_entry()
        elif choice == '5':
            help_menu()
        elif choice == '6':
            print("Thank you for using the Water Tracker App!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    user_session()