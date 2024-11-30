from auth import InvalidCredentialsError, TokenVerificationError, UserAuthentication, UsernameAlreadyExistsError
from car_parts import CarPartDatabase, ReportManager
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import csv
from logs import LogManager


class CarPartsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Parts Management System")
        self.database = CarPartDatabase()

        self.report_manager = ReportManager()
        self.auth = UserAuthentication()  # UserAuthentication

        # self.part_log_manager = PartLogManager()  # Create an instance for part logs
        self.log_manager = LogManager()  # Create an instance of LogManager
        self.current_user = None
        # Create UI elements
        self.create_widgets()

        # Check login status when the app starts
        self.check_login_status()

        # Bind the closing event to the on_closing method
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Set background color
        self.root.configure(bg="#f0f0f0")

        # Frame for login and registration
        frame_auth = tk.Frame(self.root, bg="#ffffff", padx=10, pady=10)
        frame_auth.pack(pady=5)

        # Username Label
        tk.Label(frame_auth, text="Username:", bg="#ffffff", font=(
            "central", 12)).grid(row=0, column=0, sticky="w")
        self.username_entry = tk.Entry(frame_auth)
        self.username_entry.grid(row=1, column=0, padx=5, pady=5)

        # Password Label
        tk.Label(frame_auth, text="Password:", bg="#ffffff", font=(
            "central", 12)).grid(row=0, column=1, sticky="w")
        self.password_entry = tk.Entry(frame_auth, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = tk.Button(
            frame_auth, text="Login", command=self.login, bg="#2196F3", fg="white", font=("central", 12))
        self.login_button.grid(row=1, column=2, padx=5, pady=5)

        self.register_button = tk.Button(
            frame_auth, text="Register", command=self.register_user, bg="#4CAF50", fg="white", font=("central", 12))
        self.register_button.grid(row=1, column=3, padx=5, pady=5)

        self.logout_button = tk.Button(
            frame_auth, text="Logout", command=self.logout, bg="#FF5722", fg="white", font=("central", 12))
        self.logout_button.grid(row=1, column=4, padx=5, pady=5)

        # Frame for adding parts
        frame_add = tk.Frame(self.root, bg="#ffffff",
                             padx=5, pady=5)
        frame_add.pack(pady=5)

        tk.Label(frame_add, text="Part Type:", bg="#ffffff", font=("central", 12)).grid(
            row=0, column=0, sticky="w")
        self.part_type_entry = tk.Entry(frame_add)
        self.part_type_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_add, text="Part Name:", bg="#ffffff", font=("central", 12)).grid(
            row=1, column=0, sticky="w")
        self.part_name_entry = tk.Entry(frame_add)
        self.part_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_add, text="Price:", bg="#ffffff", font=("central", 12)).grid(
            row=2, column=0, sticky="w")
        self.price_entry = tk.Entry(frame_add)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        self.add_part_button = tk.Button(
            frame_add, text="Add Part", command=self.add_part, bg="#4CAF50", fg="white", font=("central", 12))
        self.add_part_button.grid(row=3, columnspan=2, pady=5)

        # Frame for retrieving parts
        frame_retrieve = tk.Frame(self.root, bg="#ffffff", padx=5, pady=5)
        frame_retrieve.pack(pady=5)

        tk.Label(frame_retrieve, text="Retrieve Part:",
                 bg="#ffffff").grid(row=0, column=0, sticky="w")
        # self.database.validate_price(price)  # Validate price before adding
        self.retrieve_part_entry = tk.Entry(frame_retrieve)
        self.retrieve_part_entry.grid(row=0, column=1, padx=5, pady=5)

        self.retrieve_button = tk.Button(
            frame_retrieve, text="Get Price", command=self.get_price, bg="#2196F3", fg="white", font=("central", 12))
        self.retrieve_button.grid(row=0, column=2, padx=5, pady=5)

        # Frame for generating reports
        frame_report = tk.Frame(self.root, bg="#ffffff", padx=5, pady=5)
        frame_report.pack(pady=5)

        self.generate_report_button = tk.Button(
            frame_report, text="Generate Report", command=self.generate_report, bg="#FF9800", fg="white", font=("central", 12))
        self.generate_report_button.pack(pady=5)

        # Frame for viewing database
        frame_view = tk.Frame(self.root, bg="#ffffff", padx=10, pady=10)
        frame_view.pack(pady=5)

        self.view_database_button = tk.Button(
            frame_view, text="View Database", command=self.view_database, bg="#9C27B0", fg="white", font=("central", 12))
        self.view_database_button.pack(pady=5)

        # Help button
        self.help_button = tk.Button(
            self.root, text="Help", command=self.show_help, bg="#607D8B", fg="white", font=("central", 12))
        self.help_button.pack(pady=5)

        # Frame for data import/export
        frame_data = tk.Frame(self.root, bg="#ffffff", padx=5, pady=5)
        frame_data.pack(pady=5)

        self.export_button = tk.Button(
            frame_data, text="Export to CSV", command=self.export_data, bg="#FFC107", fg="white", font=("central", 12))
        self.export_button.pack(pady=5)
        self.export_button.grid(row=0, column=0, padx=5, pady=5)

        self.import_button = tk.Button(frame_data, text="Import from CSV",
                                       command=self.import_data, bg="#FF5722", fg="white", font=("central", 12))
        # self.import_button.pack(pady=5)
        self.import_button.grid(row=0, column=1, padx=5, pady=5)

        # Frame for logging
        frame_logging = tk.Frame(self.root, bg="#ffffff", padx=10, pady=10)
        frame_logging.pack(pady=5)

        # Log Activity button
        self.log_activity_button = tk.Button(
            frame_logging, text="Log Activity", command=self.show_logs, bg="#FF9800", fg="white", font=("central", 12))
        self.log_activity_button.pack(side=tk.LEFT, padx=5)

        # Log Registration button
        self.log_registration_button = tk.Button(
            frame_logging, text="Log Registration", command=self.show_registration_logs, bg="#4CAF50", fg="white", font=("central", 12))
        self.log_registration_button.pack(side=tk.LEFT, padx=5)

        # Clear Logs button
        self.clear_logs_button = tk.Button(
            self.root, text="Clear All Logs", command=self.clear_all_logs, bg="#FF5722", fg="white", font=("central", 12))
        self.clear_logs_button.pack(pady=5)

    def add_part(self):
        part_type = self.part_type_entry.get()
        part_name = self.part_name_entry.get()
        price = self.price_entry.get()

        if not part_type or not part_name or not price:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        try:
            price = float(price)
            # self.database.add_part(part_type, part_name, price)
            # self.part_log_manager.log_action(f"Added part: {part_name}, Type: {
            #                                  part_type}, Price: ${price:.2f}")
            messagebox.showinfo("Success", f"Part '{
                                part_name}' added successfully!")
            self.part_type_entry.delete(0, tk.END)
            self.part_name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Input Error", "Price must be a number!")

    def get_price(self):
        part_name = self.retrieve_part_entry.get()
        # Assuming we are retrieving Engine parts
        price = self.database.get_price("Engine", part_name)

        if price is not None:
            messagebox.showinfo("Price", f"The price of '{
                                part_name}' is {price}.")
        else:
            messagebox.showerror("Not Found", f"Part '{part_name}' not found.")

    def get_registration_logs(self):
        # Implement this method to return registration logs
        return []

    def edit_part(self):
        part_name = simpledialog.askstring(
            "Edit Part", "Enter the name of the part to edit:")
        if part_name:
            new_price = simpledialog.askfloat(
                "Edit Price", "Enter the new price:")
            if new_price is not None:
                success = self.database.edit_part(part_name, new_price)
                if success:
                    messagebox.showinfo("Success", f"Part '{
                                        part_name}' updated successfully!")
                else:
                    messagebox.showerror("Not Found", f"Part '{
                        part_name}' not found.")

    def delete_part(self):
        part_name = simpledialog.askstring(
            "Delete Part", "Enter the name of the part to delete:")
        if part_name:
            success = self.database.delete_part(part_name)
            if success:
                messagebox.showinfo("Success", f"Part '{
                                    part_name}'deleted successfully!")
            else:
                messagebox.showerror("Not Found", f"Part '{
                    part_name}' not found.")

    def show_logs(self):
        logs = self.log_manager.get_logs()
        log_window = tk.Toplevel(self.root)
        log_window.title("Log Details")
        log_window.geometry("600x400")

        log_text = tk.Text(log_window)
        log_text.pack(fill=tk.BOTH, expand=True)

        for log in logs:
            log_text.insert(tk.END, log)

        log_text.config(state=tk.DISABLED)  # Make the text widget read-only

        close_button = tk.Button(
            log_window, text="Close", command=log_window.destroy)
        close_button.pack(pady=10)

    def generate_report(self):
        report = self.report_manager.generate_report(self.database)
        messagebox.showinfo("Report", report)

    def show_help(self):
        help_message = (
            "Welcome to the Car Parts Management System!\n\n"
            "This application allows you to manage car parts easily.\n"
            "You can:\n"
            "- Add new car parts with their type, name, and price.\n"
            "- Retrieve the price of a specific part by its name.\n"
            "- Edit the price of an existing part.\n"
            "- Delete a part from the database.\n"
            "- Generate a report of all parts.\n\n"
            "To use the application, simply fill in the fields and click the corresponding buttons."
        )
        messagebox.showinfo("Help", help_message)

    def view_database(self):
        # Create a new window to display the database
        view_window = tk.Toplevel(self.root)
        view_window.title("Database View")
        view_window.geometry("600x400")  # Set a larger window size

        # Create a Treeview widget with additional columns
        tree = ttk.Treeview(view_window, columns=(
            "Type", "Name", "Price"), show='headings')
        tree.heading("Type", text="Part Type")
        tree.heading("Name", text="Part Name")
        tree.heading("Price", text="Price")

        # Set column widths
        tree.column("Type", width=150)
        tree.column("Name", width=250)
        tree.column("Price", width=100)

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(
            view_window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Pack the Treeview widget
        tree.pack(fill=tk.BOTH, expand=True)

        # Insert data into the Treeview
        for part_name, info in self.database.parts.items():
            tree.insert("", tk.END, values=(
                info['type'], part_name, f"${info['price']:.2f}"))

        # Add a button to close the window
        close_button = tk.Button(
            view_window, text="Close", command=view_window.destroy)
        close_button.pack(pady=10)

    def export_data(self):
        filename = DataExporter.export_to_csv(self.database)
        messagebox.showinfo("Export Successful",
                            f"Data exported to {filename}.")

    def import_data(self):
        # Open a file dialog to select a CSV file
        filename = filedialog.askopenfilename(
            title="Select a CSV file",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )

        if filename:  # Check if a file was selected
            result = DataImporter.import_from_csv(self.database, filename)
            messagebox.showinfo("Import Result", result)
        else:
            messagebox.showwarning(
                "No File Selected", "Please select a file to import.")

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            message = self.auth.register(username, password)
            messagebox.showinfo("Registration Successful", message)
        except UsernameAlreadyExistsError as e:
            messagebox.showerror("Registration Error", str(e))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            token = self.auth.login(username, password)
            messagebox.showinfo("2FA Token", f"Your 2FA token is: {token}")
            entered_token = simpledialog.askstring(
                "2FA Verification", "Enter your 2FA token:")
            if self.auth.verify_token(username, entered_token):
                messagebox.showinfo("Login Successful",
                                    f"Welcome, {username}!")
            else:
                messagebox.showerror("Login Error", "Invalid 2FA token.")
        except InvalidCredentialsError as e:
            messagebox.showerror("Login Error", str(e))
        except TokenVerificationError as e:
            messagebox.showerror("Token Verification Error", str(e))

    def logout(self):
        """Handle user logout process."""
        if self.current_user:
            try:
                # Attempt to log out the user
                message = self.auth.logout(self.current_user)
                self.log_manager.log_logout(self.current_user)
                self.current_user = None

                # Update UI elements
                self.logout_button.config(state=tk.DISABLED)
                self.login_button.config(state=tk.NORMAL)
                self.register_button.config(state=tk.NORMAL)

                # Provide feedback to the user
                messagebox.showinfo("Logout Successful", message)
            except Exception as e:
                # Handle any exceptions that occur during logout
                messagebox.showerror(
                    "Logout Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showwarning(
                "Logout Warning", "No user is currently logged in.")

    def on_closing(self):
        """Handle the closing event of the application."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

    def show_registration_logs(self):
        """Create a new window to display user login/logout logs."""
        reg_log_window = tk.Toplevel(self.root)
        reg_log_window.title("User  Login/Logout Log Details")
        reg_log_window.geometry("600x400")

        reg_log_text = tk.Text(reg_log_window)
        reg_log_text.pack(fill=tk.BOTH, expand=True)

        # Get only login/logout logs
        login_logout_logs = self.log_manager.get_login_logout_logs()

        # Check if there are any logs to display
        if login_logout_logs:
            for log in login_logout_logs:
                reg_log_text.insert(tk.END, log)
        else:
            reg_log_text.insert(tk.END, "No login/logout logs available.")

        # Make the text widget read-only
        reg_log_text.config(state=tk.DISABLED)

        close_button = tk.Button(
            reg_log_window, text="Close", command=reg_log_window.destroy)
        close_button.pack(pady=10)

    def check_login_status(self):
        """Check if the user is logged in; if not, prompt for login."""
        if self.current_user:
            # Provide a welcome message to the logged-in user
            messagebox.showinfo("Welcome", f"Welcome back, {
                                self.current_user}!")
        else:
            # Inform the user that they need to log in
            messagebox.showinfo(
                "Login Required", "You need to log in to access the Car Parts Management System. Please enter your credentials.")

    def clear_all_logs(self):
        """Clear all logs from both log files."""
        self.log_manager.clear_logs()  # Clear part activity logs
        messagebox.showinfo("Logs Cleared", "All logs have been cleared.")


class Inventory:
    def __init__(self):
        self.parts = {}

    def add_part(self, part_name, price):
        """Add a part to the inventory after validating the price."""
        if self.validate_price(price):

            self.parts[part_name] = float(price)
            print(f"Part '{part_name}' added with price {price}.")
        else:
            print("Invalid price. Please enter a positive number.")

    def validate_price(self, price):
        """Validate that the price is a positive number."""
        try:
            price = float(price)
            return price > 0
        except ValueError:
            return False

    def get_price(self, part_name):
        """Get the price of a part."""
        if part_name in self.parts:
            return self.parts[part_name]
        else:
            return None

    def delete_part(self, part_name):
        """Delete a part from the inventory."""
        if part_name in self.parts:
            del self.parts[part_name]
            return True
        else:
            return False


class CarPartDatabase:
    def __init__(self):
        self.parts = {}

    def add_part(self, part_type, part_name, price):
        if part_name in self.parts:
            raise ValueError("Part already exists.")
        self.parts[part_name] = {'type': part_type, 'price': price}

    def get_price(self, part_type, part_name):
        part = self.parts.get(part_name)
        if part and part['type'] == part_type:
            return part['price']
        return None

    def edit_part(self, part_name, new_price):
        if part_name in self.parts:
            self.parts[part_name]['price'] = new_price
            return True
        return False

    def delete_part(self, part_name):
        if part_name in self.parts:
            del self.parts[part_name]
            return True
        return False

    def list_parts(self):
        """Returns a list of all parts in the database."""
        return [(name, info['type'], info['price']) for name, info in self.parts.items()]

    def search_part(self, part_name):
        """Search for a part by name and return its details."""
        part = self.parts.get(part_name)
        if part:
            return part
        return None

    def validate_price(self, price):
        """Check if the price is a valid number."""
        if price < 0:
            raise ValueError("Price must be a non-negative number.")


class DataExporter:
    def export_to_csv(self, data, filename):
        """Export data to a CSV file."""
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
            messagebox.showinfo("Success", "Data exported successfully!")
        except Exception as e:
            messagebox.showerror(
                "Export Error", f"An error occurred while exporting data: {str(e)}")


class DataImporter:
    def import_from_csv(self, filename):
        """Import data from a CSV file."""
        try:
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                data = [row for row in reader]
            messagebox.showinfo("Success", "Data imported successfully!")
            return data
        except FileNotFoundError:
            messagebox.showerror(
                "Import Error", "The specified file was not found.")
        except Exception as e:
            messagebox.showerror(
                "Import Error", f"An error occurred while importing data: {str(e)}")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.validate_login(username, password):
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.destroy()
        else:
            messagebox.showerror(
                "Login Failed", "Invalid username or password.")

    def validate_login(self, username, password):

        return True

    def on_close(self):
        self.destroy()


class ReportManager:
    def generate_report(self, database):
        report = "Car Parts Report:\n"
        report += "\n".join([f"{name}: {info['type']} - ${info['price']
                                                          }" for name, info in database.parts.items()])
        return report if database.parts else "No parts available."


if __name__ == "__main__":
    root = tk.Tk()
    app = CarPartsApp(root)
    root.geometry("800x655")  # Increase the window size
    # label = tk.Label(root)
    # label.place(x=70, y=80)
    # Center the window using eval
    # root.eval('tk::PlaceWindow . center')
    root.mainloop()
