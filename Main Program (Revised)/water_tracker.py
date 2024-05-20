"""CLI UI (to hopefully move to GUI Later)"""

import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime

class WaterTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Tracker App")
        self.current_user = None

        self.main_frame = tk.Frame(root)
        self.main_frame.pack()

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame(self.main_frame)

        title_font = ("Helvetica", 16, "bold")
        button_font = ("Helvetica", 12, "bold")

        tk.Label(self.main_frame, text="Welcome to the Water Tracker App!", font=title_font).pack()
        
        tk.Button(self.main_frame, text="Login/Register", command=self.register_login, font=button_font).pack()
        tk.Button(self.main_frame, text="Enter Water Intake", command=self.enter_water_intake, font=button_font).pack()
        tk.Button(self.main_frame, text="Copy Last Entry", command=self.copy_last_entry, font=button_font).pack()
        tk.Button(self.main_frame, text="View Daily Average", command=lambda: self.view_average_history('daily'), font=button_font).pack()
        tk.Button(self.main_frame, text="View Weekly Average", command=lambda: self.view_average_history('weekly'), font=button_font).pack()
        tk.Button(self.main_frame, text="View Monthly Average", command=lambda: self.view_average_history('monthly'), font=button_font).pack()
        tk.Button(self.main_frame, text="View All History", command=self.view_history, font=button_font).pack()
        tk.Button(self.main_frame, text="Undo Last Entry", command=self.undo_last_entry, font=button_font).pack()
        tk.Button(self.main_frame, text="Delete a Specific Entry", command=self.delete_specific_entry, font=button_font).pack()
        tk.Button(self.main_frame, text="Help", command=self.help_menu, font=button_font).pack()
        tk.Button(self.main_frame, text="Exit", command=self.root.quit, font=button_font).pack()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def help_menu(self):
        self.clear_frame(self.main_frame)
        
        tk.Label(self.main_frame, text="Help Menu").pack()
        help_text = """
        1. Benefits of Logging Water Intake: Keeps you hydrated, improves health.
        2. How to Use Features: Navigate using menu numbers to log and view water intake.
        3. Undo Feature: Revert your last logged intake.
        4. Delete Specific Entry: Remove a particular entry from your history.
        5. Copy Last Entry: Repeat your last water intake entry.
        6. View Options: You can view detailed logs or summaries.
        7. Help Menu: Provides information about all features.
        8. Exit: Safely close the application.
        """
        tk.Label(self.main_frame, text=help_text, justify=tk.LEFT).pack()
        tk.Button(self.main_frame, text="Back", command=self.create_main_menu).pack()

    def register_login(self):
        self.clear_frame(self.main_frame)
        
        tk.Label(self.main_frame, text="Register/Login").pack()
        tk.Label(self.main_frame, text="Username:").pack()
        username_entry = tk.Entry(self.main_frame)
        username_entry.pack()

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

        tk.Button(self.main_frame, text="Submit", command=submit).pack()
        tk.Button(self.main_frame, text="Back", command=self.create_main_menu).pack()

    def enter_water_intake(self):
        if self.current_user:
            self.clear_frame(self.main_frame)
            
            tk.Label(self.main_frame, text="Enter Water Intake").pack()
            tk.Label(self.main_frame, text="Amount (ml):").pack()
            amount_entry = tk.Entry(self.main_frame)
            amount_entry.pack()
            
            tk.Label(self.main_frame, text="Date (mm/dd/yyyy):").pack()
            date_entry = tk.Entry(self.main_frame)
            date_entry.pack()

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

            tk.Button(self.main_frame, text="Submit", command=submit).pack()
            tk.Button(self.main_frame, text="Back", command=self.create_main_menu).pack()
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
            
            tk.Label(self.main_frame, text="Delete Specific Entry").pack()
            tk.Label(self.main_frame, text="Entry Number:").pack()
            entry_number_entry = tk.Entry(self.main_frame)
            entry_number_entry.pack()

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

            tk.Button(self.main_frame, text="Submit", command=submit).pack()
            tk.Button(self.main_frame, text="Back", command=self.create_main_menu).pack()
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def view_history(self):
        if self.current_user:
            response = requests.get('http://localhost:5002/view_history', params={"username": self.current_user})
            if response.status_code == 200:
                history = response.json()
                self.clear_frame(self.main_frame)
                tk.Label(self.main_frame, text=f"Water Intake History for {self.current_user}:").pack()
                if history:
                    for index, entry in enumerate(history, start=1):
                        tk.Label(self.main_frame, text=f"{index}. {entry['date']}: {entry['amount']}ml").pack()
                else:
                    tk.Label(self.main_frame, text="No history to display.").pack()
                tk.Button(self.main_frame, text="Back", command=self.create_main_menu).pack()
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

if __name__ == "__main__":
    root = tk.Tk()
    app = WaterTrackerApp(root)
    root.mainloop()
