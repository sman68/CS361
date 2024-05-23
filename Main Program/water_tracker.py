import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime

class WaterTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Tracker App")
        self.root.geometry("800x600")
        self.root.configure(bg="lightblue")
        self.current_user = None

        self.main_frame = tk.Frame(root, bg="lightblue")
        self.main_frame.pack()

        self.custom_font = ("Helvetica", 12)
        self.custom_title_font = ("Helvetica", 16, "bold")

        self.create_main_menu()
        self.bind_keys()

    def bind_keys(self):
        self.root.bind('1', lambda event: self.register_login())
        self.root.bind('2', lambda event: self.enter_water_intake())
        self.root.bind('3', lambda event: self.copy_last_entry())
        self.root.bind('4', lambda event: self.view_average_history('daily'))
        self.root.bind('5', lambda event: self.view_average_history('weekly'))
        self.root.bind('6', lambda event: self.view_average_history('monthly'))
        self.root.bind('7', lambda event: self.view_history())
        self.root.bind('8', lambda event: self.undo_last_entry())
        self.root.bind('9', lambda event: self.delete_specific_entry())
        self.root.bind('0', lambda event: self.help_menu())
        self.root.bind('<Escape>', lambda event: self.root.quit())
        self.root.bind('I', lambda event: self.inspiration_menu())

    def create_main_menu(self):
        self.clear_frame(self.main_frame)

        tk.Label(self.main_frame, text="Welcome to the Water Tracker App!", font=self.custom_title_font, bg="lightblue").pack(pady=10)
        
        tk.Button(self.main_frame, text="1. Login/Register", command=self.register_login, font=self.custom_font, bg="white").pack(pady=5)
        tk.Button(self.main_frame, text="2. Enter Water Intake", command=self.enter_water_intake, font=self.custom_font, bg="white").pack(pady=5)
        tk.Button(self.main_frame, text="3. Copy Last Entry", command=self.copy_last_entry, font=self.custom_font, bg="white").pack(pady=5)
        tk.Button(self.main_frame, text="4. View Daily Average", command=lambda: self.view_average_history('daily'), font=self.custom_font, bg="white").pack(pady=5)
        tk.Button(self.main_frame, text="5. View Weekly Average", command=lambda: self.view_average_history('weekly'), font=self.custom_font, bg="white").pack(pady=5)
        tk.Button(self.main_frame, text="6. View Monthly Average", command=lambda: self.view_average_history('monthly'), font=self.custom_font, bg="white").pack(pady=5)
        tk.Button(self.main_frame, text="7. View All History", command=self.view_history, font=self.custom_font, bg="white").pack(pady=5)
        tk.Button(self.main_frame, text="8. Undo Last Entry", command=self.undo_last_entry, font=self.custom_font, bg="white").pack(pady=5)
        tk.Button(self.main_frame, text="9. Delete a Specific Entry", command=self.delete_specific_entry, font=self.custom_font, bg="white").pack(pady=5)
        tk.Button(self.main_frame, text="I. Inspiration", command=self.inspiration_menu, font=self.custom_font, bg="white").pack(pady=5)
        tk.Button(self.main_frame, text="0. Help", command=self.help_menu, font=self.custom_font, bg="white").pack(pady=5)
        tk.Button(self.main_frame, text="Esc. Exit", command=self.root.quit, font=self.custom_font, bg="white").pack(pady=5)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def help_menu(self):
        self.clear_frame(self.main_frame)
        
        tk.Label(self.main_frame, text="Help Menu", font=self.custom_title_font, bg="lightblue").pack(pady=10)
        help_text = """
        1. Login/Register
        2. Enter Water Intake
        3. Copy Last Entry
        4. View Daily Average
        5. View Weekly Average
        6. View Monthly Average
        7. View All History
        8. Undo Last Entry
        9. Delete a Specific Entry
        I. Inspiration
        0. Help
        Esc. Exit
        """
        tk.Label(self.main_frame, text=help_text, justify=tk.LEFT, bg="lightblue", font=self.custom_font).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.create_main_menu, font=self.custom_font, bg="white").pack(pady=5)

    def register_login(self):
        self.clear_frame(self.main_frame)
        
        tk.Label(self.main_frame, text="Register/Login", font=self.custom_title_font, bg="lightblue").pack(pady=10)
        tk.Label(self.main_frame, text="Username:", bg="lightblue", font=self.custom_font).pack()
        username_entry = tk.Entry(self.main_frame)
        username_entry.pack(pady=5)

        def submit():
            username = username_entry.get()
            response = requests.post('http://localhost:5001/register', json={"username": username})
            if response.status_code == 200:
                self.current_user = username
                messagebox.showinfo("Success", f"Registration complete. Welcome, {username}!")
                self.create_main_menu()
            elif response.status_code == 400:
                response = requests.post('http://localhost:5001/login', json={"username": username})
                if response.status_code == 200:
                    self.current_user = username
                    messagebox.showinfo("Success", f"Welcome back, {username}!")
                    self.create_main_menu()
                else:
                    messagebox.showerror("Error", "User not found.")
            else:
                messagebox.showerror("Error", "Unable to register or login.")

        tk.Button(self.main_frame, text="Submit", command=submit, font=self.custom_font, bg="white").pack(pady=5)
        tk.Button(self.main_frame, text="Back", command=self.create_main_menu, font=self.custom_font, bg="white").pack(pady=5)

    def enter_water_intake(self):
        if self.current_user:
            self.clear_frame(self.main_frame)
            
            tk.Label(self.main_frame, text="Enter Water Intake", font=self.custom_title_font, bg="lightblue").pack(pady=10)
            tk.Label(self.main_frame, text="Amount (ml):", bg="lightblue", font=self.custom_font).pack()
            amount_entry = tk.Entry(self.main_frame)
            amount_entry.pack(pady=5)
            
            tk.Label(self.main_frame, text="Date (mm/dd/yyyy):", bg="lightblue", font=self.custom_font).pack()
            date_entry = tk.Entry(self.main_frame)
            date_entry.pack(pady=5)

            def submit():
                amount = amount_entry.get()
                date_str = date_entry.get()
                try:
                    amount = int(amount)
                    datetime.strptime(date_str, '%m/%d/%Y')
                    data = {"username": self.current_user, "amount": amount, "date": date_str}
                    response = requests.post('http://localhost:5002/log_water', json=data)
                    if response.status_code == 200:
                        messagebox.showinfo("Success", f"Recorded {amount}ml of water intake on {date_str}.")
                        self.create_main_menu()
                    else:
                        messagebox.showerror("Error", response.json()['status'])
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please enter the correct values.")

            tk.Button(self.main_frame, text="Submit", command=submit, font=self.custom_font, bg="white").pack(pady=5)
            tk.Button(self.main_frame, text="Back", command=self.create_main_menu, font=self.custom_font, bg="white").pack(pady=5)
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def copy_last_entry(self):
        if self.current_user:
            response = requests.post('http://localhost:5003/copy_last_entry', json={"username": self.current_user})
            if response.status_code == 200:
                messagebox.showinfo("Success", response.json()['status'])
            else:
                messagebox.showerror("Error", response.json()['status'])
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def undo_last_entry(self):
        if self.current_user:
            response = requests.post('http://localhost:5003/undo_last_entry', json={"username": self.current_user})
            if response.status_code == 200:
                messagebox.showinfo("Success", response.json()['status'])
            else:
                messagebox.showerror("Error", response.json()['status'])
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def delete_specific_entry(self):
        if self.current_user:
            self.clear_frame(self.main_frame)
            
            tk.Label(self.main_frame, text="Delete Specific Entry", font=self.custom_title_font, bg="lightblue").pack(pady=10)
            tk.Label(self.main_frame, text="Entry Number:", bg="lightblue", font=self.custom_font).pack()
            entry_number_entry = tk.Entry(self.main_frame)
            entry_number_entry.pack(pady=5)

            def submit():
                entry_number = entry_number_entry.get()
                try:
                    entry_number = int(entry_number)
                    response = requests.post('http://localhost:5003/delete_entry', json={"username": self.current_user, "entry_number": entry_number})
                    if response.status_code == 200:
                        messagebox.showinfo("Success", response.json()['status'])
                        self.create_main_menu()
                    else:
                        messagebox.showerror("Error", response.json()['status'])
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please enter a number.")

            tk.Button(self.main_frame, text="Submit", command=submit, font=self.custom_font, bg="white").pack(pady=5)
            tk.Button(self.main_frame, text="Back", command=self.create_main_menu, font=self.custom_font, bg="white").pack(pady=5)
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def view_history(self):
        if self.current_user:
            response = requests.get('http://localhost:5002/view_history', params={"username": self.current_user})
            if response.status_code == 200:
                history = response.json()
                self.clear_frame(self.main_frame)
                tk.Label(self.main_frame, text=f"Water Intake History for {self.current_user}:", font=self.custom_title_font, bg="lightblue").pack(pady=10)
                if history:
                    for index, entry in enumerate(history, start=1):
                        tk.Label(self.main_frame, text=f"{index}. {entry['date']}: {entry['amount']}ml", bg="lightblue", font=self.custom_font).pack()
                else:
                    tk.Label(self.main_frame, text="No history to display.", bg="lightblue", font=self.custom_font).pack()
                tk.Button(self.main_frame, text="Back", command=self.create_main_menu, font=self.custom_font, bg="white").pack(pady=5)
            else:
                messagebox.showerror("Error", response.json()['status'])
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def view_average_history(self, period):
        if self.current_user:
            response = requests.get('http://localhost:5002/view_history', params={"username": self.current_user})
            if response.status_code == 200:
                user_data = self.prepare_data_for_average(response.json())
                average = self.calculate_average(period, user_data)
                if average is not None:
                    messagebox.showinfo("Average", f"The {period} average water intake is: {average}ml")
            else:
                messagebox.showerror("Error", response.json()['status'])
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def prepare_data_for_average(self, user_entries):
        return [{"date": entry['date'], "amount": entry['amount']} for entry in user_entries]

    def calculate_average(self, period, data):
        url = f'http://localhost:5000/average/{period}'
        response = requests.post(url, json={"data": data})
        if response.status_code == 200:
            return response.json()['average']
        else:
            print("Failed to calculate average:", response.text)
            return None

    def inspiration_menu(self):
        self.clear_frame(self.main_frame)
        
        tk.Label(self.main_frame, text="Inspiration Menu", font=self.custom_title_font, bg="lightblue").pack(pady=10)
        tk.Button(self.main_frame, text="Get Random Quote", command=self.get_random_quote, font=self.custom_font, bg="white").pack(pady=5)
        tk.Button(self.main_frame, text="View Favorite Quotes", command=self.get_favorite_quotes, font=self.custom_font, bg="white").pack(pady=5)
        tk.Button(self.main_frame, text="Back", command=self.create_main_menu, font=self.custom_font, bg="white").pack(pady=5)

    def get_random_quote(self):
        response = requests.get('http://localhost:5000/quotes')
        if response.status_code == 200:
            quote = response.json()["quote"]
            favorite = messagebox.askyesno("Random Quote", f"{quote}\n\nDo you want to favorite this quote?")
            if favorite:
                self.favorite_quote(quote)
        else:
            messagebox.showerror("Error", "Could not retrieve quote")

    def get_favorite_quotes(self):
        response = requests.get('http://localhost:5000/quotes/favorites')
        if response.status_code == 200:
            favorites = response.json()
            self.clear_frame(self.main_frame)
            tk.Label(self.main_frame, text=f"Favorite Quotes:", font=self.custom_title_font, bg="lightblue").pack(pady=10)
            if favorites:
                for index, favorite in enumerate(favorites, start=1):
                    tk.Label(self.main_frame, text=f"{index}. {favorite['quote']}", bg="lightblue", font=self.custom_font).pack()
            else:
                tk.Label(self.main_frame, text="No favorite quotes to display.", bg="lightblue", font=self.custom_font).pack()
            tk.Button(self.main_frame, text="Back", command=self.inspiration_menu, font=self.custom_font, bg="white").pack(pady=5)
        else:
            messagebox.showerror("Error", "Could not retrieve favorite quotes")

    def favorite_quote(self, quote):
        response = requests.post('http://localhost:5000/quotes/favorite', json={"quote": quote})
        if response.status_code == 201:
            messagebox.showinfo("Success", "Quote favorited successfully")
        else:
            messagebox.showerror("Error", "Could not favorite quote")

if __name__ == "__main__":
    root = tk.Tk()
    app = WaterTrackerApp(root)
    root.mainloop()
