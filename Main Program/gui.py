import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from services import (
    register_user,
    login_user,
    log_water_intake,
    copy_last_entry,
    undo_last_entry,
    delete_entry,
    view_history,
    calculate_average,
    get_random_quote,
    get_favorite_quotes,
    favorite_quote
)

class WaterTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Tracker App")
        self.root.geometry("1280x720")
        self.root.configure(bg="lightblue")
        self.current_user = None

        self.main_frame = tk.Frame(root, bg="lightblue")
        self.main_frame.pack()

        self.custom_font = ("Helvetica", 12)
        self.custom_title_font = ("Helvetica", 16, "bold")

        self.create_main_menu()
        self.bind_keys()

    def bind_keys(self):
        """Bind keys to menu options for easy navigation."""
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
        self.root.bind('I', lambda event: self.inspiration_menu())
        self.root.bind('<Escape>', lambda event: self.root.quit())

    def unbind_keys(self):
        """Unbind keys when focus is needed in entry fields."""
        self.root.unbind('1')
        self.root.unbind('2')
        self.root.unbind('3')
        self.root.unbind('4')
        self.root.unbind('5')
        self.root.unbind('6')
        self.root.unbind('7')
        self.root.unbind('8')
        self.root.unbind('9')
        self.root.unbind('0')
        self.root.unbind('I')

    def create_main_menu(self):
        """Create the main menu interface."""
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
        """Clears all widgets from the given frame."""
        for widget in frame.winfo_children():
            widget.destroy()

    def help_menu(self):
        """Displays the help menu."""
        self.clear_frame(self.main_frame)
        
        tk.Label(self.main_frame, text="Help Menu", font=self.custom_title_font, bg="lightblue").pack(pady=10)
        help_text = """
        1. Login/Register: Allows you to create a new user account or log in to an existing one. This ensures your data is personalized and secure.
        2. Enter Water Intake: Record the amount of water you've consumed. You can enter the date and amount to track your hydration.
        3. Copy Last Entry: Quickly duplicate your most recent water intake entry. Useful for days when your intake is consistent.
        4. View Daily Average: Calculate and view your average daily water intake. Helps you monitor your daily hydration levels.
        5. View Weekly Average: Calculate and view your average weekly water intake. Provides insights into your weekly hydration habits.
        6. View Monthly Average: Calculate and view your average monthly water intake. Offers a broader perspective on your hydration patterns.
        7. View All History: Display a complete history of your water intake entries. Allows you to review and analyze your past hydration data.
        8. Undo Last Entry: Remove the most recent water intake entry. Useful if you made a mistake or need to correct an entry.
        9. Delete a Specific Entry: Select and delete a specific entry from your history. Helps you manage and clean up your data.
        I. Inspiration: Generate a random inspiring quote or view your favorite quotes. Adds motivation and positivity to your hydration journey.
        0. Help: Display this help menu to learn about each feature and how to use it.
        Esc. Exit: Close the application safely.
        """
        tk.Label(self.main_frame, text=help_text, justify=tk.LEFT, bg="lightblue", font=self.custom_font).pack(pady=10)
        tk.Button(self.main_frame, text="Back", command=self.create_main_menu, font=self.custom_font, bg="white").pack(pady=5)

    def register_login(self):
        """Displays the login/register interface."""
        self.clear_frame(self.main_frame)
        
        tk.Label(self.main_frame, text="Register/Login", font=self.custom_title_font, bg="lightblue").pack(pady=10)
        tk.Label(self.main_frame, text="Username:", bg="lightblue", font=self.custom_font).pack()
        username_entry = tk.Entry(self.main_frame)
        username_entry.pack(pady=5)
        username_entry.bind("<FocusIn>", lambda event: self.unbind_keys())
        username_entry.bind("<FocusOut>", lambda event: self.bind_keys())

        def submit():
            username = username_entry.get()
            if register_user(username):
                self.current_user = username
                messagebox.showinfo("Success", f"Registration complete. Welcome, {username}!")
                self.create_main_menu()
            elif login_user(username):
                self.current_user = username
                messagebox.showinfo("Success", f"Welcome back, {username}!")
                self.create_main_menu()
            else:
                messagebox.showerror("Error", "Unable to register or login.")

        tk.Button(self.main_frame, text="Submit", command=submit, font=self.custom_font, bg="white").pack(pady=5)
        tk.Button(self.main_frame, text="Back", command=self.create_main_menu, font=self.custom_font, bg="white").pack(pady=5)

    def enter_water_intake(self):
        """Displays the interface to enter water intake."""
        if self.current_user:
            self.clear_frame(self.main_frame)
            
            tk.Label(self.main_frame, text="Enter Water Intake", font=self.custom_title_font, bg="lightblue").pack(pady=10)
            tk.Label(self.main_frame, text="Amount (ml):", bg="lightblue", font=self.custom_font).pack()
            amount_entry = tk.Entry(self.main_frame)
            amount_entry.pack(pady=5)
            amount_entry.bind("<FocusIn>", lambda event: self.unbind_keys())
            amount_entry.bind("<FocusOut>", lambda event: self.bind_keys())
            
            tk.Label(self.main_frame, text="Date (mm/dd/yyyy):", bg="lightblue", font=self.custom_font).pack()
            date_entry = tk.Entry(self.main_frame)
            date_entry.pack(pady=5)
            date_entry.bind("<FocusIn>", lambda event: self.unbind_keys())
            date_entry.bind("<FocusOut>", lambda event: self.bind_keys())

            def submit():
                amount = amount_entry.get()
                date_str = date_entry.get()
                try:
                    amount = int(amount)
                    datetime.strptime(date_str, '%m/%d/%Y')
                    if log_water_intake(self.current_user, amount, date_str):
                        messagebox.showinfo("Success", f"Recorded {amount}ml of water intake on {date_str}.")
                        self.create_main_menu()
                    else:
                        messagebox.showerror("Error", "Could not log water intake.")
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please enter the correct values.")

            tk.Button(self.main_frame, text="Submit", command=submit, font=self.custom_font, bg="white").pack(pady=5)
            tk.Button(self.main_frame, text="Back", command=self.create_main_menu, font=self.custom_font, bg="white").pack(pady=5)
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def copy_last_entry(self):
        """Copies the last water intake entry."""
        if self.current_user:
            if copy_last_entry(self.current_user):
                messagebox.showinfo("Success", "Copied last entry successfully.")
            else:
                messagebox.showerror("Error", "Could not copy last entry.")
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def undo_last_entry(self):
        """Undoes the last water intake entry."""
        if self.current_user:
            if undo_last_entry(self.current_user):
                messagebox.showinfo("Success", "Undid last entry successfully.")
            else:
                messagebox.showerror("Error", "Could not undo last entry.")
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def delete_specific_entry(self):
        """Deletes a specific water intake entry."""
        if self.current_user:
            self.clear_frame(self.main_frame)
            
            tk.Label(self.main_frame, text="Delete Specific Entry", font=self.custom_title_font, bg="lightblue").pack(pady=10)
            tk.Label(self.main_frame, text="Entry Number:", bg="lightblue", font=self.custom_font).pack()
            entry_number_entry = tk.Entry(self.main_frame)
            entry_number_entry.pack(pady=5)
            entry_number_entry.bind("<FocusIn>", lambda event: self.unbind_keys())
            entry_number_entry.bind("<FocusOut>", lambda event: self.bind_keys())

            def submit():
                entry_number = entry_number_entry.get()
                try:
                    entry_number = int(entry_number)
                    if delete_entry(self.current_user, entry_number):
                        messagebox.showinfo("Success", "Deleted entry successfully.")
                        self.create_main_menu()
                    else:
                        messagebox.showerror("Error", "Could not delete entry.")
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please enter a number.")

            tk.Button(self.main_frame, text="Submit", command=submit, font=self.custom_font, bg="white").pack(pady=5)
            tk.Button(self.main_frame, text="Back", command=self.create_main_menu, font=self.custom_font, bg="white").pack(pady=5)
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def view_history(self):
        """Displays the user's water intake history."""
        if self.current_user:
            history = view_history(self.current_user)
            if history is not None:
                self.clear_frame(self.main_frame)
                tk.Label(self.main_frame, text=f"Water Intake History for {self.current_user}:", font=self.custom_title_font, bg="lightblue").pack(pady=10)
                if history:
                    for index, entry in enumerate(history, start=1):
                        tk.Label(self.main_frame, text=f"{index}. {entry['date']}: {entry['amount']}ml", bg="lightblue", font=self.custom_font).pack()
                else:
                    tk.Label(self.main_frame, text="No history to display.", bg="lightblue", font=self.custom_font).pack()
                tk.Button(self.main_frame, text="Back", command=self.create_main_menu, font=self.custom_font, bg="white").pack(pady=5)
            else:
                messagebox.showerror("Error", "Could not retrieve history.")
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def view_average_history(self, period):
        """Displays the average water intake for a given period (daily, weekly, monthly)."""
        if self.current_user:
            history = view_history(self.current_user)
            if history is not None:
                user_data = self.prepare_data_for_average(history)
                average = calculate_average(period, user_data)
                if average is not None:
                    messagebox.showinfo("Average", f"The {period} average water intake is: {average}ml")
                else:
                    messagebox.showerror("Error", "Could not calculate average.")
            else:
                messagebox.showerror("Error", "Could not retrieve history.")
        else:
            messagebox.showwarning("Warning", "Please log in first.")

    def prepare_data_for_average(self, user_entries):
        """Prepares user entries for average calculation."""
        return [{"date": entry['date'], "amount": entry['amount']} for entry in user_entries]

    def inspiration_menu(self):
        """Displays the inspiration menu."""
        self.clear_frame(self.main_frame)
        
        tk.Label(self.main_frame, text="Inspiration Menu", font=self.custom_title_font, bg="lightblue").pack(pady=10)
        tk.Button(self.main_frame, text="Get Random Quote", command=self.get_random_quote, font=self.custom_font, bg="white").pack(pady=5)
        tk.Button(self.main_frame, text="View Favorite Quotes", command=self.get_favorite_quotes, font=self.custom_font, bg="white").pack(pady=5)
        tk.Button(self.main_frame, text="Back", command=self.create_main_menu, font=self.custom_font, bg="white").pack(pady=5)

    def get_random_quote(self):
        """Fetches and displays a random inspirational quote."""
        quote = get_random_quote()
        if quote:
            favorite = messagebox.askyesno("Random Quote", f"{quote}\n\nDo you want to favorite this quote?")
            if favorite:
                self.favorite_quote(quote)
        else:
            messagebox.showerror("Error", "Could not retrieve quote")

    def get_favorite_quotes(self):
        """Displays the user's favorite quotes."""
        favorites = get_favorite_quotes()
        if favorites is not None:
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
        """Favorites a quote."""
        if favorite_quote(quote):
            messagebox.showinfo("Success", "Quote favorited successfully")
        else:
            messagebox.showerror("Error", "Could not favorite quote")

if __name__ == "__main__":
    root = tk.Tk()
    app = WaterTrackerApp(root)
    root.mainloop()
