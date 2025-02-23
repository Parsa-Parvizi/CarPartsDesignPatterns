from tkinter import *
from tkinter import ttk, messagebox, simpledialog, filedialog
import tkinter as tk
import csv
from utils.singleton import SingletonMeta
from core import CarPartDatabase, Engine, Color
from core.CarPartDatabase import ReportManager
from security.auth import UserAuthentication, InvalidCredentialsError, TokenVerificationError, UsernameAlreadyExistsError
# from logs import LogManager


# Temporary LogManager class until we implement the real one
class LogManager:
    def __init__(self):
        pass
    
    def log_logout(self, username):
        pass
        
    def get_login_logout_logs(self):
        return []
        
    def clear_logs(self):
        pass


class CarPartsApp:
    def __init__(self, root):
        """Initialize the application and create the user interface"""
        self.root = root
        self.root.title("Car Parts Management System")
        
        # Initialize components
        self.database = CarPartDatabase()
        self.report_manager = ReportManager()
        self.auth = UserAuthentication()
        self.log_manager = LogManager()  # Now using temporary LogManager
        self.current_user = None
        
        # Create UI
        self.create_widgets()
        
        # Check login status at startup
        self.check_login_status()

        # Bind the closing event to the on_closing method
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Create main container frame
        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True)
        container.grid_columnconfigure(0, weight=1)  # Center content horizontally

        # Create scroll area
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        scrollable_frame.grid_columnconfigure(0, weight=1)  # Center content horizontally

        canvas.create_window((400, 0), window=scrollable_frame, anchor="n")  # Center point
        canvas.configure(yscrollcommand=scrollbar.set)

        # Initialize entry widgets
        self.part_type_entry = ttk.Entry(scrollable_frame)
        self.part_name_entry = ttk.Entry(scrollable_frame)
        self.price_entry = ttk.Entry(scrollable_frame)
        self.retrieve_part_entry = ttk.Entry(scrollable_frame)

        # Login Frame
        login_frame = ttk.LabelFrame(scrollable_frame, text="Login")
        login_frame.pack(fill="x", padx=20, pady=5)
        
        # Center login frame contents
        login_frame.grid_columnconfigure(1, weight=1)
        
        # Login widgets with center alignment
        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Center login buttons
        button_frame = ttk.Frame(login_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Button(button_frame, text="Login", command=self.login).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Register", command=self.register_user).grid(row=0, column=1, padx=5)

        # Parts Management Frame
        parts_frame = ttk.LabelFrame(scrollable_frame, text="Parts Management")
        parts_frame.pack(fill="x", padx=20, pady=5)
        
        # Center parts frame contents
        parts_frame.grid_columnconfigure(1, weight=1)

        # Add part section with center alignment
        current_row = 0
        
        # Create labels and entries
        ttk.Label(parts_frame, text="Part Type:").grid(row=current_row, column=0, padx=5, pady=5)
        self.part_type_entry = ttk.Entry(parts_frame)
        self.part_type_entry.grid(row=current_row, column=1, padx=5, pady=5, sticky="ew")
        current_row += 1

        ttk.Label(parts_frame, text="Part Name:").grid(row=current_row, column=0, padx=5, pady=5)
        self.part_name_entry = ttk.Entry(parts_frame)
        self.part_name_entry.grid(row=current_row, column=1, padx=5, pady=5, sticky="ew")
        current_row += 1

        ttk.Label(parts_frame, text="Price:").grid(row=current_row, column=0, padx=5, pady=5)
        self.price_entry = ttk.Entry(parts_frame)
        self.price_entry.grid(row=current_row, column=1, padx=5, pady=5, sticky="ew")
        current_row += 1

        # Search section
        ttk.Label(parts_frame, text="Search Part:").grid(row=current_row, column=0, padx=5, pady=5)
        self.retrieve_part_entry = ttk.Entry(parts_frame)
        self.retrieve_part_entry.grid(row=current_row, column=1, padx=5, pady=5, sticky="ew")
        current_row += 1

        # Center all buttons
        buttons = [
            ("Add Part", self.add_part),
            ("Search Part", self.get_price),
            ("Generate Report", self.generate_report),
            ("View Database", self.view_database),
            ("Help", self.show_help),
            ("Clear All Logs", self.clear_all_logs)
        ]

        for button_text, command in buttons:
            ttk.Button(parts_frame, text=button_text, command=command).grid(
                row=current_row, column=0, columnspan=2, pady=5, sticky="ew", padx=20
            )
            current_row += 1

        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Update window size based on content
        self.root.update_idletasks()
        content_width = scrollable_frame.winfo_reqwidth() + scrollbar.winfo_reqwidth() + 40
        content_height = min(scrollable_frame.winfo_reqheight() + 40, 800)  # Max height of 800px
        
        # Set minimum dimensions
        width = max(content_width, 500)  # Minimum width of 500px
        height = max(content_height, 400)  # Minimum height of 400px
        
        # Center the window on screen
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        
        # Set the window size and position
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def add_part(self):
        part_type = self.part_type_entry.get()
        part_name = self.part_name_entry.get()
        price = self.price_entry.get()

        if not part_type or not part_name or not price:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        try:
            price = float(price)
            self.database.add_part(part_type, part_name, price)
            messagebox.showinfo("Success", f"Part '{part_name}' added successfully!")
            self.part_type_entry.delete(0, ttk.END)
            self.part_name_entry.delete(0, ttk.END)
            self.price_entry.delete(0, ttk.END)
        except ValueError:
            messagebox.showerror("Input Error", "Price must be a number!")

    def get_price(self):
        """Search for a part and display its details"""
        part_name = self.retrieve_part_entry.get()
        if not part_name:
            messagebox.showerror("Error", "Please enter a part name")
            return

        # Try to find in different categories
        for part_type in ["engines", "colors", "tires", "wheels", "seats"]:
            price = self.database.get_part(part_type, part_name)
            if price is not None:
                specs = f"Type: {part_type}\nName: {part_name}\nPrice: ${price}"
                if part_type == "colors":
                    specs += f"\nColor Code: #{price}"
                messagebox.showinfo("Part Details", specs)
                return
        
        messagebox.showerror("Not Found", f"Part '{part_name}' not found in any category")

    def get_registration_logs(self):
        # Implement this method to return registration logs
        return []

    def edit_part(self):
        part_name = simpledialog.askstring(
            "Edit Part", "Enter part name:")
        if part_name:
            new_price = simpledialog.askfloat(
                "Edit Price", "Enter new price:")
            if new_price is not None:
                success = self.database.edit_part(part_name, new_price)
                if success:
                    messagebox.showinfo("Success", f"Part '{part_name}' updated successfully!")
                else:
                    messagebox.showerror("Not Found", f"Part '{part_name}' not found.")

    def delete_part(self):
        part_name = simpledialog.askstring(
            "Delete Part", "Enter part name:")
        if part_name:
            success = self.database.delete_part(part_name)
            if success:
                messagebox.showinfo("Success", f"Part '{part_name}' deleted successfully!")
            else:
                messagebox.showerror("Not Found", f"Part '{part_name}' not found.")

    def show_logs(self):
        # Create and center new window
        log_window = Toplevel(self.root)
        log_window.title("Log Details")
        
        # Center the window
        window_width = 600
        window_height = 400
        x = (log_window.winfo_screenwidth() // 2) - (window_width // 2)
        y = (log_window.winfo_screenheight() // 2) - (window_height // 2)
        log_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Center content
        container = ttk.Frame(log_window)
        container.pack(fill="both", expand=True)
        container.grid_columnconfigure(0, weight=1)

        log_text = tk.Text(container)
        log_text.pack(fill="both", expand=True, padx=20, pady=10)

        close_button = ttk.Button(container, text="Close", command=log_window.destroy)
        close_button.pack(pady=10)

    def generate_report(self):
        """Generate and display a detailed report"""
        report_window = Toplevel(self.root)
        report_window.title("Car Parts Report")
        report_window.geometry("600x400")

        # Create text widget
        report_text = Text(report_window, wrap=WORD)
        report_text.pack(expand=True, fill=BOTH, padx=10, pady=10)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(report_window, orient=VERTICAL, command=report_text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        report_text.configure(yscrollcommand=scrollbar.set)

        # Generate report content
        report_content = "=== Car Parts Inventory Report ===\n\n"
        
        for category, parts in self.database.parts.items():
            report_content += f"\n{category.upper()}:\n"
            report_content += "-" * 30 + "\n"
            for name, value in parts.items():
                if category == "colors":
                    report_content += f"{name}: Color Code #{value}\n"
                else:
                    report_content += f"{name}: ${value}\n"

        # Add timestamp
        from datetime import datetime
        report_content += f"\n\nReport generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        # Insert report content
        report_text.insert(END, report_content)
        report_text.config(state=DISABLED)  # Make read-only

        # Add export button
        def export_report():
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(report_content)
                messagebox.showinfo("Success", "Report exported successfully!")

        ttk.Button(report_window, text="Export Report", command=export_report).pack(pady=10)

    def show_help(self):
        """Display help information"""
        help_text = """
Car Parts Management System Help

1. Adding Parts:
   - Enter part type (engines, colors, tires, etc.)
   - Enter part name
   - Enter price
   - Click 'Add Part'

2. Searching Parts:
   - Enter part name in search field
   - Click 'Search Part'
   - View part details in popup

3. Reports:
   - Click 'Generate Report' for full inventory
   - Export reports to file
   - View historical reports

4. Database Management:
   - View all parts in database
   - Edit existing parts
   - Delete parts
   - Track inventory

5. User Management:
   - Login/Logout
   - Register new users
   - View activity logs

For additional help or support:
Contact: support@carparts.com
Version: 1.0.0
        """
        
        help_window = Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("500x600")

        # Create text widget with scrollbar
        help_text_widget = Text(help_window, wrap=WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(help_window, orient=VERTICAL, command=help_text_widget.yview)
        
        help_text_widget.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        help_text_widget.configure(yscrollcommand=scrollbar.set)
        help_text_widget.insert(END, help_text)
        help_text_widget.config(state=DISABLED)  # Make read-only

    def view_database(self):
        # Create and center new window
        view_window = Toplevel(self.root)
        view_window.title("View Database")
        
        # Center the window
        window_width = 600
        window_height = 400
        x = (view_window.winfo_screenwidth() // 2) - (window_width // 2)
        y = (view_window.winfo_screenheight() // 2) - (window_height // 2)
        view_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Center content
        container = ttk.Frame(view_window)
        container.pack(fill="both", expand=True)
        container.grid_columnconfigure(0, weight=1)

        # Create centered treeview
        tree = ttk.Treeview(container, columns=("Type", "Name", "Price"), show="headings")
        
        # Configure columns
        for col in ("Type", "Name", "Price"):
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center", width=150)

        tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Add centered close button
        close_button = ttk.Button(container, text="Close", command=view_window.destroy)
        close_button.pack(pady=10)

    def export_data(self):
        filename = DataExporter.export_to_csv(self.database)
        messagebox.showinfo("خروج به CSV موفق",
                            f"دیتا با موفقیت به فایل {filename} خروج داده شد.")

    def import_data(self):
        # Open a file dialog to select a CSV file
        filename = filedialog.askopenfilename(
            title="انتخاب فایل CSV",
            filetypes=(("فایل‌های CSV", "*.csv"), ("فایل‌های دیگر", "*.*"))
        )

        if filename:  # Check if a file was selected
            result = DataImporter.import_from_csv(self.database, filename)
            messagebox.showinfo("نتیجه وارد کردن", result)
        else:
            messagebox.showwarning(
                "فایل انتخاب نشده", "لطفا یک فایل برای وارد کردن انتخاب کنید.")

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            message = self.auth.register(username, password)
            messagebox.showinfo("ثبت‌نام موفق", message)
        except UsernameAlreadyExistsError as e:
            messagebox.showerror("خطا در ثبت‌نام", str(e))

    def login(self):
        """مدیریت ورود کاربر"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            token = self.auth.login(username, password)
            if token:
                # نمایش توکن دو مرحله‌ای و تأیید آن
                messagebox.showinfo("توکن دو مرحله‌ای", f"توکن شما: {token}")
                entered_token = simpledialog.askstring(
                    "تأیید دو مرحله‌ای", "توکن را وارد کنید:")
                if entered_token and self.auth.verify_token(username, entered_token):
                    self.current_user = username
                    self.log_manager.log_login(username)
                    messagebox.showinfo("ورود موفق", f"خوش آمدید، {username}!")
                    
                    # به‌روزرسانی وضعیت دکمه‌ها
                    self.clear_logs_button.config(state=ttk.NORMAL)
                    self.log_activity_button.config(state=ttk.DISABLED)
                    self.log_registration_button.config(state=ttk.DISABLED)
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
                self.clear_logs_button.config(state=ttk.DISABLED)
                self.log_activity_button.config(state=ttk.NORMAL)
                self.log_registration_button.config(state=ttk.NORMAL)

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
        reg_log_window = Toplevel(self.root)
        reg_log_window.title("جزئیات لاگ ورود/خروج کاربران")
        reg_log_window.geometry("600x400")

        reg_log_text = tk.Text(reg_log_window)
        reg_log_text.pack(fill=tk.BOTH, expand=True)

        # Get only login/logout logs
        login_logout_logs = self.log_manager.get_login_logout_logs()

        # Check if there are any logs to display
        if login_logout_logs:
            for log in login_logout_logs:
                reg_log_text.insert(END, log)
        else:
            reg_log_text.insert(END, "هیچ لاگ ورود/خروجی موجود نیست.")

        # Make the text widget read-only
        reg_log_text.config(state=DISABLED)

        close_button = tk.Button(
            reg_log_window, text="بستن", command=reg_log_window.destroy)
        close_button.pack(pady=10)

    def check_login_status(self):
        """Check if the user is logged in; if not, prompt for login."""
        if self.current_user:
            # Provide a welcome message to the logged-in user
            messagebox.showinfo("Welcome", f"Welcome back, {self.current_user}!")
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


class CarPartDatabase(metaclass=SingletonMeta):
    def __init__(self):
        # Dictionary to store different types of parts and their prices
        self.parts = {
            "engines": {"V8": 500, "V6": 300},  # Engines and their prices
            "colors": {"red": "FF0000", "blue": "0000FF"},  # Colors and their codes
            "tires": {"Pirelli": 100, "Michelin": 150},  # Tires and their prices
            "wheels": {"alloy": 200, "steel": 50},  # Wheels and their prices
            "seats": {"leather": 300, "cloth": 100}  # Seats and their prices
        }

    def get(self, part_type, part_name):
        """Get a part instance based on type and name"""
        if part_type == "Engine":
            return Engine(part_name)
        elif part_type == "Color":
            return Color(part_name)
        return None

    def get_part(self, part_type, part_name):
        """Get part price based on type and name"""
        try:
            part_price = self.parts.get(part_type, {}).get(part_name)
            if part_price is None:
                raise ValueError(f"Part '{part_name}' of type '{part_type}' not found.")
            return part_price
        except Exception as e:
            print(f"Error retrieving part: {e}")
            return None


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
        report += "\n".join([f"{name}: {info['type']} - ${info['price']}"] for name, info in database.parts.items())
        return report if database.parts else "No parts available."


def main():
    root = Tk()
    app = CarPartsApp(root)
    
    # Set minimum window size
    root.minsize(500, 400)
    
    root.mainloop()


if __name__ == "__main__":
    main()
