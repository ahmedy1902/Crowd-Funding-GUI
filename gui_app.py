import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
import os
import Users
import projects
import re  # Add this line with other imports
import time  # Add time import here
from tkcalendar import Calendar  # Add tkcalendar import
import matplotlib.pyplot as plt  # Add matplotlib
import datetime  # Add datetime import

__all__ = ["CrowdfundingApp"]

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users")


class CrowdfundingApp(tk.Tk):
    def __init__(self):
        # Create necessary directories
        if not os.path.exists(os.path.join(os.path.dirname(__file__), "users")):
            os.makedirs(os.path.join(os.path.dirname(__file__), "users"))
        if not os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "projects")):
            os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), "projects"))

        super().__init__()

        self.title("Crowd-Funding Platform")
        self.state("zoomed")

        # Improve colors and formatting
        self.style = {
            "bg_color": "#E0FFFF",  # Change background color to light cyan
            "button_color": "#0f3460",
            "button_hover": "#16213e",
            "text_color": "#000000",  # Change text color to black
            "secondary_text": "#ffffff",
            "frame_bg": "#B0E0E6",  # Change frame background to powderblue
            "title_font": tkfont.Font(family="Arial", size=40, weight="bold"),  # Increase title size
            "button_font": tkfont.Font(family="Arial", size=16, weight="bold"),
            "label_font": tkfont.Font(family="Arial", size=14),
        }

        # Apply main background
        self.configure(bg=self.style["bg_color"])

        # Create main frame
        self.main_frame = tk.Frame(self, bg=self.style["bg_color"], padx=50, pady=50)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Add current_user_email variable
        self.current_user_email = None

        self.create_main_menu()

    def create_main_menu(self):
        # Fix space to prevent flicker
        self.main_frame.pack_configure(expand=True, fill="both", padx=50, pady=50)

        # Clear previous elements
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Application title
        title = tk.Label(
            self.main_frame,
            text="Crowd-Funding Platform ",
            font=self.style["title_font"],
            bg=self.style["bg_color"],
            fg=self.style["text_color"],
            pady=30,
        )
        title.pack(pady=(10, 50))  # Increase top margin

        # Buttons frame
        button_frame = tk.Frame(self.main_frame, bg=self.style["bg_color"])
        button_frame.pack(pady=40)

        buttons = [
            ("📝 Register", self.show_register_form),
            ("🔑 Login", self.show_login_form),
            ("❌ Delete Account", self.show_delete_account_form),
            ("🚪 Exit", self.quit),
        ]

        for text, command in buttons:
            self.create_styled_button(button_frame, text, command)

    def create_styled_button(self, parent, text, command):
        # Store original font as constant
        original_font = self.style["button_font"]
        hover_font = tkfont.Font(size=17, weight="bold")  # Reduce font size difference on hover

        btn = tk.Button(
            parent,
            text=text,
            command=command,
            width=25,
            height=2,
            font=original_font,
            bg=self.style["button_color"],
            fg=self.style["secondary_text"],
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.style["button_hover"],
            activeforeground=self.style["secondary_text"],
            bd=0,
        )

        def on_enter(e):
            btn["background"] = self.style["button_hover"]
            btn["font"] = hover_font

        def on_leave(e):
            btn["background"] = self.style["button_color"]
            btn["font"] = original_font

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.pack(pady=10, ipady=5, padx=5)  # Add padx for more horizontal space

        return btn

    def clear_main_frame(self):
        """Clear main frame contents"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def create_scrollable_frame(self, parent):
        """Create a scrollable frame"""
        # Create Canvas for scrolling
        canvas = tk.Canvas(parent, bg=self.style["bg_color"])
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.style["bg_color"])

        # Bind scrolling
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add mouse wheel support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Unbind on window close
        def _on_frame_destroy(event):
            canvas.unbind_all("<MouseWheel>")

        scrollable_frame.bind("<Destroy>", _on_frame_destroy)

        # Organize scrolling elements
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        return scrollable_frame

    def show_register_form(self):
        """Display registration form"""
        # Clear previous content and show registration form in main frame
        self.clear_main_frame()

        form_frame = tk.Frame(self.main_frame, bg=self.style["frame_bg"])
        form_frame.pack(expand=True, fill="both", padx=50, pady=50)

        # Page title
        title = tk.Label(
            form_frame,
            text="Create New Account",
            font=self.style["title_font"],
            bg=self.style["frame_bg"],
            fg=self.style["text_color"],
        )
        title.pack(pady=(0, 30))

        # Registration fields
        fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Email:", "email"),
            ("Password:", "password"),
            ("Confirm Password:", "confirm_password"),
            ("Phone:", "phone"),
        ]

        entries = {}
        for i, (label_text, field_name) in enumerate(fields):
            frame = tk.Frame(form_frame, bg=self.style["frame_bg"])
            frame.pack(pady=10)

            label = tk.Label(
                frame,
                text=label_text,
                font=self.style["label_font"],
                bg=self.style["frame_bg"],
                fg=self.style["text_color"],
            )
            label.pack(side=tk.LEFT, padx=10)

            entry = tk.Entry(frame, width=30)
            if field_name in ["password", "confirm_password"]:
                entry.configure(show="*")
            entry.pack(side=tk.LEFT)
            entries[field_name] = entry

        def submit_registration():
            try:
                # Collect data
                data = {
                    "first_name": entries["first_name"].get().strip(),
                    "last_name": entries["last_name"].get().strip(),
                    "email": entries["email"].get().strip(),
                    "password": entries["password"].get(),
                    "confirm_password": entries["confirm_password"].get(),
                    "phone": entries["phone"].get().strip(),
                }

                # Check for empty fields
                if not all(data.values()):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                # Name validation
                if not data["first_name"].isalpha() or not data["last_name"].isalpha():
                    messagebox.showerror("Error", "Names must contain only letters!")
                    return

                # Email validation
                if not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
                    messagebox.showerror("Error", "Invalid email format!")
                    return

                # Password match
                if data["password"] != data["confirm_password"]:
                    messagebox.showerror("Error", "Passwords don't match!")
                    return

                # Phone number validation
                if not re.match(r"^01[0-2,5]{1}[0-9]{8}$", data["phone"]):
                    messagebox.showerror("Error", "Invalid Egyptian phone number!")
                    return

                # Check if email already exists
                existing_files = [f for f in os.listdir(BASE_DIR) if data["email"].lower() in f.lower()]
                if existing_files:
                    messagebox.showerror("Error", "Email already registered!")
                    return

                # Create user file
                filename = os.path.join(BASE_DIR, f"{data['email']}X_X{data['password']}X_X.txt")
                with open(filename, "w") as file:
                    file.write(f"First_name:{data['first_name']}\n")
                    file.write(f"Last_name:{data['last_name']}\n")
                    file.write(f"Email:{data['email']}\n")
                    file.write(f"Password:{'*' * len(data['password'])}\n")
                    file.write(f"Mobile phone:{data['phone']}\n")

                messagebox.showinfo("Success", "Registration successful!")
                self.create_main_menu()  # Return to main menu instead of dashboard

            except Exception as e:
                messagebox.showerror("Error", f"Registration failed: {str(e)}")
                print(f"Debug - Registration error: {str(e)}")

        def handle_enter(event):
            if event.widget == entries["first_name"]:
                entries["last_name"].focus()
            elif event.widget == entries["last_name"]:
                entries["email"].focus()
            elif event.widget == entries["email"]:
                entries["password"].focus()
            elif event.widget == entries["password"]:
                entries["confirm_password"].focus()
            elif event.widget == entries["confirm_password"]:
                entries["phone"].focus()
            elif event.widget == entries["phone"]:
                submit_registration()

        # Bind Enter key to each entry field
        for entry in entries.values():
            entry.bind("<Return>", handle_enter)

        # Register button
        submit_btn = tk.Button(
            form_frame,
            text="Register",
            command=submit_registration,
            width=20,
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg=self.style["text_color"],
            relief=tk.FLAT,
            cursor="hand2",
        )
        submit_btn.pack(pady=20)

        # Back button
        back_btn = tk.Button(
            form_frame,
            text="Back to Main Menu",
            command=self.create_main_menu,
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg=self.style["secondary_text"],
        )
        back_btn.pack(pady=10)

    def show_login_form(self):
        """Handle user login"""
        self.clear_main_frame()

        # Create main frame
        form_frame = tk.Frame(self.main_frame, bg=self.style["frame_bg"])
        form_frame.pack(expand=True, fill="both", padx=50, pady=50)

        # Page title
        title = tk.Label(
            form_frame,
            text="Login to Your Account",
            font=tkfont.Font(family="Arial", size=40, weight="bold"),
            bg=self.style["frame_bg"],
            fg=self.style["text_color"],
        )
        title.pack(pady=(20, 40))

        # Login fields
        entries = {}
        fields = [("Email:", "email"), ("Password:", "password")]

        for label_text, field_name in fields:
            frame = tk.Frame(form_frame, bg=self.style["frame_bg"])
            frame.pack(pady=20)

            label = tk.Label(
                frame,
                text=label_text,
                font=tkfont.Font(family="Arial", size=24),
                bg=self.style["frame_bg"],
                fg=self.style["text_color"],
            )
            label.pack(side=tk.LEFT, padx=30)

            entry = tk.Entry(frame, width=40, font=("Arial", 20))
            if field_name == "password":
                entry.configure(show="*")
            entry.pack(side=tk.LEFT)
            entries[field_name] = entry

        # Forgot password button
        forgot_password_btn = tk.Button(
            form_frame,
            text="Forgot Password?",
            command=self.show_reset_password_form,
            font=self.style["label_font"],
            bg=self.style["frame_bg"],
            fg="blue",
            relief=tk.FLAT,
            cursor="hand2",
        )
        forgot_password_btn.pack(pady=10)

        def submit_login():
            try:
                email = entries["email"].get().strip()
                password = entries["password"].get()

                if not email or not password:
                    messagebox.showerror("Error", "Please fill in all fields!")
                    return

                # Check if directory exists
                if not os.path.exists(BASE_DIR):
                    messagebox.showerror("Error", "Invalid email or password!")
                    return

                # Search for file
                filename = Users.AccountLogin(email, password)
                if not os.path.exists(filename):
                    messagebox.showerror("Error", "Invalid email or password!")
                    return

                # Validate file
                try:
                    with open(filename, "r") as file:
                        content = file.readlines()
                        if not any(line.startswith("Email:") for line in content):
                            messagebox.showerror("Error", "User data is corrupted!")
                            return

                    self.current_user_email = email
                    messagebox.showinfo("Success", "Login successful!")
                    self.show_user_dashboard(email)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to read user data: {str(e)}")
                    return

            except Exception as e:
                messagebox.showerror("Error", f"Login failed: {str(e)}")

        # Login button
        submit_btn = tk.Button(
            form_frame,
            text="Login",
            command=submit_login,
            width=20,
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.style["button_hover"],
            activeforeground="white",
        )
        submit_btn.pack(pady=20)

        # Back button
        back_btn = tk.Button(
            form_frame,
            text="Back to Main Menu",
            command=self.create_main_menu,
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg=self.style["secondary_text"],
        )
        back_btn.pack(pady=10)

        # Bind Enter key
        def handle_enter(event):
            if event.widget == entries["email"]:
                entries["password"].focus()
            elif event.widget == entries["password"]:
                submit_login()

        for entry in entries.values():
            entry.bind("<Return>", handle_enter)

    def show_reset_password_form(self):
        """Show password reset window"""
        reset_window = tk.Toplevel(self)
        reset_window.title("Reset Password")
        reset_window.geometry("400x400")
        reset_window.configure(bg=self.style["bg_color"])

        # Create scrollable frame
        canvas = tk.Canvas(reset_window, bg=self.style["bg_color"])
        scrollbar = tk.Scrollbar(reset_window, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg=self.style["bg_color"])

        # Bind scrolling
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add mouse wheel support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Unbind on window close
        def _on_frame_destroy(event):
            canvas.unbind_all("<MouseWheel>")

        frame.bind("<Destroy>", _on_frame_destroy)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Initial input fields
        entries = {}
        initial_widgets = []  # To store elements to be hidden later

        for field in [("Email", "email"), ("Phone", "phone")]:
            label = tk.Label(
                frame,
                text=f"Enter your {field[0]}:",
                font=self.style["label_font"],
                bg=self.style["bg_color"],
            )
            label.pack(pady=5)
            initial_widgets.append(label)

            entry = tk.Entry(frame, width=30)
            entry.pack(pady=5)
            entries[field[1]] = entry
            initial_widgets.append(entry)

        def show_password_fields():
            # Hide initial elements
            for widget in initial_widgets:
                widget.pack_forget()

            password_frame = tk.Frame(frame, bg=self.style["bg_color"])
            password_frame.pack(pady=10)

            # Add new password fields
            tk.Label(
                password_frame, text="New Password:", font=self.style["label_font"], bg=self.style["bg_color"]
            ).pack(pady=10)

            new_pass = tk.Entry(password_frame, show="*", width=30)
            new_pass.pack(pady=5)

            tk.Label(
                password_frame,
                text="Confirm Password:",
                font=self.style["label_font"],
                bg=self.style["bg_color"],
            ).pack(pady=10)

            confirm_pass = tk.Entry(password_frame, show="*", width=30)
            confirm_pass.pack(pady=5)

            def save_new_password():
                if not new_pass.get() or not confirm_pass.get():
                    messagebox.showerror("Error", "Please fill in all fields!")
                    return
                if new_pass.get() != confirm_pass.get():
                    messagebox.showerror("Error", "Passwords don't match!")
                    return

                try:
                    # Get email from entries
                    email = entries["email"].get().strip()

                    # Get the old file name
                    user_files = [f for f in os.listdir(BASE_DIR) if email.lower() in f.lower()]
                    if user_files:
                        old_file = os.path.join(BASE_DIR, user_files[0])

                        # Create new filename with new password
                        new_filename = os.path.join(BASE_DIR, f"{email}X_X{new_pass.get()}X_X.txt")

                        # Read old file content
                        with open(old_file, "r") as file:
                            lines = file.readlines()

                        # Write to new file
                        with open(new_filename, "w") as file:
                            for line in lines:
                                if line.startswith("Password:"):
                                    file.write(f"Password:{'*' * len(new_pass.get())}\n")
                                else:
                                    file.write(line)

                        # Remove old file
                        os.remove(old_file)

                        messagebox.showinfo("Success", "Password reset successful!")
                        reset_window.destroy()
                    else:
                        messagebox.showerror("Error", "User file not found!")

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to reset password: {str(e)}")

            save_btn = tk.Button(
                password_frame,
                text="Save New Password",
                command=save_new_password,
                font=self.style["button_font"],
                bg=self.style["button_color"],
                fg="white",
            )
            save_btn.pack(pady=20)

            # Add back button again
            self.add_back_button(password_frame, reset_window.destroy)

        def verify_and_reset():
            email = entries["email"].get().strip()
            phone = entries["phone"].get().strip()

            # ... existing verification code ...
            user_files = [f for f in os.listdir(BASE_DIR) if email.lower() in f.lower()]
            if not user_files:
                messagebox.showerror("Error", "Email not found!")
                return

            # Check phone number
            user_file = os.path.join(BASE_DIR, user_files[0])
            with open(user_file, "r") as file:
                content = file.readlines()
                stored_phone = next(
                    (line.split(":")[1].strip() for line in content if "Mobile phone:" in line), None
                )

                if stored_phone != phone:
                    messagebox.showerror("Error", "Incorrect phone number!")
                    return

            # If verification successful, show password fields
            verify_btn.pack_forget()  # Hide verify button
            show_password_fields()

        # Add verify button
        verify_btn = tk.Button(
            frame,
            text="Verify",
            command=verify_and_reset,
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg="white",
        )
        verify_btn.pack(pady=20)
        initial_widgets.append(verify_btn)

        # Add back button
        back_btn = self.add_back_button(frame, reset_window.destroy)
        initial_widgets.append(back_btn)

        # Bind Enter key
        def handle_enter(event):
            if event.widget == entries["email"]:
                entries["phone"].focus()
            elif event.widget == entries["phone"]:
                verify_and_reset()

        for entry in entries.values():
            entry.bind("<Return>", handle_enter)

    # ... rest of the code ...

    def show_delete_account_form(self):
        """Show account deletion window"""
        # Warning window
        delete_window = tk.Toplevel(self)
        delete_window.title("Delete Account")
        delete_window.geometry("400x300")
        delete_window.configure(bg=self.style["bg_color"])

        # Form frame
        form_frame = tk.Frame(delete_window, bg=self.style["bg_color"])
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Warning title
        warning_label = tk.Label(
            form_frame,
            text="⚠️ Warning: This action cannot be undone!",
            font=self.style["label_font"],
            bg=self.style["bg_color"],
            fg="red",
        )
        warning_label.pack(pady=(0, 20))

        # Input fields
        entries = {}
        fields = [("Email:", "email"), ("Password:", "password")]

        for label_text, field_name in fields:
            frame = tk.Frame(form_frame, bg=self.style["bg_color"])
            frame.pack(pady=10)

            label = tk.Label(
                frame,
                text=label_text,
                font=self.style["label_font"],
                bg=self.style["bg_color"],
                fg=self.style["text_color"],
            )
            label.pack(side=tk.LEFT, padx=10)

            entry = tk.Entry(frame, width=30)
            if field_name == "password":
                entry.configure(show="*")
            entry.pack(side=tk.LEFT)
            entries[field_name] = entry

        def confirm_deletion():
            email = entries["email"].get().strip()
            password = entries["password"].get().strip()

            if not email or not password:
                messagebox.showerror("Error", "Please fill in all fields!")
                return

            # First verify the credentials
            filename = os.path.join(BASE_DIR, f"{email}X_X{password}X_X.txt")
            if not os.path.exists(filename):
                messagebox.showerror("Error", "Invalid email or password!")
                return

            if messagebox.askyesno(
                "Confirm Deletion",
                "Are you sure you want to delete your account?\nThis action cannot be undone!",
            ):
                try:
                    # Delete the account and any associated files except donation files
                    if Users.DeleteAccount(email, password):
                        messagebox.showinfo("Success", "Account deleted successfully!")
                        delete_window.destroy()
                        self.create_main_menu()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        # Delete and cancel buttons
        button_frame = tk.Frame(form_frame, bg=self.style["bg_color"])
        button_frame.pack(pady=20)

        # Delete button
        delete_btn = tk.Button(
            button_frame,
            text="Delete Account",
            command=confirm_deletion,
            font=self.style["button_font"],
            bg="#e74c3c",  # Warning red color
            fg="white",
            width=15,
            relief=tk.FLAT,
            cursor="hand2",
        )
        delete_btn.pack(side=tk.LEFT, padx=10)

        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=delete_window.destroy,
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg="white",
            width=15,
            relief=tk.FLAT,
            cursor="hand2",
        )
        cancel_btn.pack(side=tk.LEFT, padx=10)

    def show_user_dashboard(self, email):
        """Display main control panel"""
        self.clear_main_frame()

        # Create main scrollable frame
        canvas = tk.Canvas(self.main_frame, bg=self.style["bg_color"])
        scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        container = tk.Frame(canvas, bg=self.style["bg_color"])

        # Bind scrolling
        container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=container, anchor="nw", width=self.main_frame.winfo_width())
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add mouse wheel support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Unbind on window close
        def _on_frame_destroy(event):
            canvas.unbind_all("<MouseWheel>")

        container.bind("<Destroy>", _on_frame_destroy)

        # Organize scrolling elements
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Get user's name from file
        user_files = [f for f in os.listdir(BASE_DIR) if email.lower() in f.lower()]
        first_name = ""
        last_name = ""
        if user_files:
            user_file = os.path.join(BASE_DIR, user_files[0])
            with open(user_file, "r") as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("First_name:"):
                        first_name = line.split(":", 1)[1].strip().capitalize()
                    elif line.startswith("Last_name:"):
                        last_name = line.split(":", 1)[1].strip().capitalize()

        # Welcome message with larger font
        welcome_text = "Hello"
        if first_name or last_name:
            welcome_text += f", {first_name} {last_name}"

        title = tk.Label(
            container,
            text=welcome_text,
            font=self.style["title_font"],
            bg=self.style["bg_color"],
            fg=self.style["text_color"],
        )
        title.pack(pady=(20, 30))

        # Buttons container
        buttons_container = tk.Frame(container, bg=self.style["bg_color"])
        buttons_container.pack(expand=True, fill="both")

        # Inner frame for buttons
        buttons_frame = tk.Frame(buttons_container, bg=self.style["bg_color"])
        buttons_frame.pack(expand=True)

        buttons = [
            ("👤 Show My Data", lambda: self.show_user_data(email)),
            ("📁 My Projects", lambda: self.show_my_projects(email)),
            ("➕ Create New Project", lambda: self.create_new_project(email)),
            ("🌐 Show All Projects", self.show_all_projects),
            ("💰 My Donations", lambda: self.show_my_donations(email)),
            ("✏️ Change My Data", lambda: self.change_user_data(email)),
            ("📝 Add Additional Info", lambda: self.add_user_info(email)),
            ("🚪 Logout", self.create_main_menu),
        ]

        for text, command in buttons:
            self.create_styled_button(buttons_frame, text, command)

        # Add back button at the bottom
        back_btn = tk.Button(
            container,
            text="Back to Main Menu",
            command=self.create_main_menu,
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg="white",
        )
        back_btn.pack(pady=(20, 10))

    def show_user_data(self, email):
        """Display user data and profile"""
        self.clear_main_frame()

        # Create scrollable frame
        canvas = tk.Canvas(self.main_frame, bg=self.style["bg_color"])
        scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        main_container = tk.Frame(canvas, bg=self.style["bg_color"])

        # Bind scrolling
        main_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=main_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add mouse wheel support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Remove binding when window closes
        def _on_frame_destroy(event):
            canvas.unbind_all("<MouseWheel>")

        main_container.bind("<Destroy>", _on_frame_destroy)

        # Organize scroll elements
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Split screen into two panels
        left_frame = tk.Frame(main_container, bg=self.style["bg_color"])
        left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=20)

        right_frame = tk.Frame(main_container, bg=self.style["bg_color"], width=300)
        right_frame.pack(side=tk.RIGHT, fill="y", padx=20)
        right_frame.pack_propagate(False)

        # Title in left panel
        title = tk.Label(
            left_frame, text="Your Profile", font=self.style["title_font"], bg=self.style["bg_color"]
        )
        title.pack(pady=10)

        # Data frame with vertical layout
        data_frame = tk.Frame(left_frame, bg=self.style["bg_color"])
        data_frame.pack(fill="both", expand=True, pady=20)

        try:
            user_files = [f for f in os.listdir(BASE_DIR) if email.lower() in f.lower()]
            if user_files:
                user_file = os.path.join(BASE_DIR, user_files[0])
                with open(user_file, "r") as file:
                    for line in file:
                        if ":" in line and not line.startswith("profile_picture:"):
                            key, value = line.strip().split(":", 1)
                            label_text = key.replace("_", " ").title()

                            # Frame for each field
                            field_frame = tk.Frame(data_frame, bg=self.style["bg_color"])
                            field_frame.pack(fill="x", pady=10)  # Add vertical spacing

                            # Field label
                            tk.Label(
                                field_frame,
                                text=f"{label_text}:",
                                font=("Arial", 14, "bold"),
                                bg=self.style["bg_color"],
                            ).pack(
                                anchor="w"
                            )  # Align to left

                            # Field value
                            tk.Label(
                                field_frame,
                                text=value,
                                font=("Arial", 12),
                                bg=self.style["bg_color"],
                            ).pack(
                                anchor="w", padx=20
                            )  # Indent value

                # Image frame in right panel
                profile_pic_frame = tk.Frame(right_frame, bg=self.style["bg_color"])
                profile_pic_frame.pack(pady=20)

                # Initialize pic_label with default empty frame
                pic_label = self._show_empty_profile_frame(profile_pic_frame)

                # Get and display profile picture if exists
                pic_path = self.get_profile_picture_path(user_file)
                if pic_path and os.path.exists(pic_path):
                    try:
                        img = self.load_and_resize_image(pic_path, (200, 200))
                        pic_label.configure(image=img)
                        pic_label.image = img
                    except Exception as e:
                        print(f"Error loading profile picture: {e}")

                # Add change picture button
                change_pic_btn = tk.Button(
                    right_frame,
                    text="Change Profile Picture",
                    command=lambda: self.change_profile_picture(email, pic_label),
                    font=self.style["button_font"],
                    bg=self.style["button_color"],
                    fg="white",
                )
                change_pic_btn.pack(pady=10)

                # Move back button here, below change picture button
                back_btn = tk.Button(
                    right_frame,
                    text="Back to Dashboard",
                    command=lambda: self.show_user_dashboard(email),
                    font=self.style["button_font"],
                    bg=self.style["button_color"],
                    fg="white",
                )
                back_btn.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load user data: {str(e)}")

    def get_profile_picture_path(self, user_file):
        """Get profile picture path from user file"""
        try:
            with open(user_file, "r") as file:
                for line in file:
                    if line.startswith("profile_picture:"):
                        return line.split(":", 1)[1].strip()
        except Exception:
            return None
        return None

    def load_and_resize_image(self, path, size):
        """Load and resize image
        Attempts to load original image first, falls back to default if needed"""
        from PIL import Image, ImageTk

        try:
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image: {e}")
            # If original image fails, try loading default
            try:
                img = Image.open("default_profile.png")
                img = img.resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading default profile picture: {e}")
                return None

    def _show_empty_profile_frame(self, parent):
        """Display empty profile picture frame"""
        empty_frame = tk.Frame(parent, width=200, height=200, bg="white", relief="solid", borderwidth=1)
        empty_frame.pack()
        empty_frame.pack_propagate(False)  # Keep frame size
        label = tk.Label(empty_frame, text="No Profile Picture", bg="white")
        label.place(relx=0.5, rely=0.5, anchor="center")
        return label

    def change_profile_picture(self, email, pic_label):
        """Change user profile picture"""
        from tkinter import filedialog
        import shutil

        try:
            file_path = filedialog.askopenfilename(
                title="Select Profile Picture", filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
            )

            if file_path:
                # Ensure pictures directory exists
                pictures_dir = os.path.join(BASE_DIR, "profile_pictures")
                os.makedirs(pictures_dir, exist_ok=True)

                # Copy image with unique name
                ext = os.path.splitext(file_path)[1]
                new_pic_name = f"{email}_profile_{int(time.time())}{ext}"
                new_pic_path = os.path.join(pictures_dir, new_pic_name)

                # Copy file
                shutil.copy2(file_path, new_pic_path)

                # Update user file
                user_files = [f for f in os.listdir(BASE_DIR) if email.lower() in f.lower()]
                if not user_files:
                    raise Exception("User file not found")

                user_file = os.path.join(BASE_DIR, user_files[0])

                # Read file content
                with open(user_file, "r") as file:
                    lines = file.readlines()

                # Write updated content
                with open(user_file, "w") as file:
                    profile_pic_found = False
                    for line in lines:
                        if line.startswith("profile_picture:"):
                            file.write(f"profile_picture:{new_pic_path}\n")
                            profile_pic_found = True
                        else:
                            file.write(line)

                    if not profile_pic_found:
                        file.write(f"profile_picture:{new_pic_path}\n")

                # Update display
                new_img = self.load_and_resize_image(new_pic_path, (200, 200))
                if new_img:
                    pic_label.configure(image=new_img)
                    pic_label.image = new_img  # Keep image reference
                    messagebox.showinfo("Success", "Profile picture updated successfully!")
                else:
                    messagebox.showerror("Error", "Failed to load the new image")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update profile picture: {str(e)}")
            print(f"Debug - Profile picture error: {str(e)}")

    def change_user_data(self, email):
        """Change user account data"""
        self.clear_main_frame()

        # Create change frame
        change_frame = tk.Frame(self.main_frame, bg=self.style["bg_color"])
        change_frame.pack(expand=True, fill="both", padx=50, pady=50)

        title = tk.Label(
            change_frame, text="Change Your Data", font=self.style["title_font"], bg=self.style["bg_color"]
        )
        title.pack(pady=20)

        # Add back button at the beginning
        back_btn = tk.Button(
            change_frame,
            text="Back to Dashboard",
            command=lambda: self.show_user_dashboard(email),
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg="white",
        )
        back_btn.pack(pady=10)

        def show_change_field(field_name, field_label):
            # Clear previous content except title and back button
            for widget in change_frame.winfo_children()[2:]:
                widget.destroy()

            if field_name == "Password":
                self.show_change_password_form(change_frame, email)
            else:
                # Other data change fields
                tk.Label(
                    change_frame,
                    text=f"New {field_label}:",
                    font=self.style["label_font"],
                    bg=self.style["bg_color"],
                ).pack(pady=5)

                entry = tk.Entry(change_frame, width=30)
                entry.pack(pady=5)

                def save_field():
                    new_value = entry.get().strip()
                    if not new_value:
                        messagebox.showerror("Error", "Field cannot be empty!")
                        return

                    try:
                        # Validate new value
                        if field_name in ["First_name", "Last_name"] and not new_value.isalpha():
                            messagebox.showerror("Error", "Name must contain only letters!")
                            return
                        elif field_name == "Mobile phone" and not re.match(
                            r"^01[0-2,5]{1}[0-9]{8}$", new_value
                        ):
                            messagebox.showerror("Error", "Invalid Egyptian phone number!")
                            return

                        # Update file
                        user_files = [f for f in os.listdir(BASE_DIR) if email.lower() in f.lower()]
                        if user_files:
                            file_path = os.path.join(BASE_DIR, user_files[0])
                            Users.update_file(file_path, field_name, new_value)
                            messagebox.showinfo("Success", f"{field_label} updated successfully!")
                            self.show_user_dashboard(email)
                        else:
                            messagebox.showerror("Error", "User file not found!")

                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to update {field_label}: {str(e)}")

                tk.Button(
                    change_frame,
                    text=f"Save {field_label}",
                    command=save_field,
                    font=self.style["button_font"],
                    bg=self.style["button_color"],
                    fg="white",
                ).pack(pady=20)

        # Field selection buttons
        fields = [
            ("First Name", "First_name"),
            ("Last Name", "Last_name"),
            ("Phone Number", "Mobile phone"),
            ("Password", "Password"),
        ]

        buttons_frame = tk.Frame(change_frame, bg=self.style["bg_color"])
        buttons_frame.pack(pady=20)

        for field_label, field_name in fields:
            tk.Button(
                buttons_frame,
                text=f"Change {field_label}",
                command=lambda fl=field_label, fn=field_name: show_change_field(fn, fl),
                font=self.style["button_font"],
                bg=self.style["button_color"],
                fg="white",
                width=20,
            ).pack(pady=5)

    def show_change_password_form(self, parent_frame, email):
        """Show password change form window"""
        # Clear previous content
        for widget in parent_frame.winfo_children()[2:]:  # Keep title and back button
            widget.destroy()

        # Frame for password fields
        password_frame = tk.Frame(parent_frame, bg=self.style["bg_color"])
        password_frame.pack(pady=20)

        labels = ["Current Password:", "New Password:", "Confirm New Password:"]
        entries = {}

        for label in labels:
            tk.Label(
                password_frame, text=label, font=self.style["label_font"], bg=self.style["bg_color"]
            ).pack(pady=5)

            entry = tk.Entry(password_frame, show="*", width=30)
            entry.pack(pady=5)
            entries[label] = entry

        def verify_and_change():
            current = entries["Current Password:"].get()
            new = entries["New Password:"].get()
            confirm = entries["Confirm New Password:"].get()

            # Check current password
            filename = os.path.join(BASE_DIR, f"{email}X_X{current}X_X.txt")
            if not os.path.exists(filename):
                messagebox.showerror("Error", "Current password is incorrect!")
                return

            if not new or new != confirm:
                messagebox.showerror("Error", "New passwords don't match or are empty!")
                return

            try:
                if Users.update_file(filename, "Password", new):
                    messagebox.showinfo("Success", "Password changed successfully!")
                    self.current_user_email = None  # Reset login state
                    self.create_main_menu()  # Return to main menu
                else:
                    messagebox.showerror("Error", "Failed to change password!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to change password: {str(e)}")

        # Save new password button
        tk.Button(
            password_frame,
            text="Save New Password",
            command=verify_and_change,
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg="white",
            width=20,
            height=2,
        ).pack(pady=20)

    def add_user_info(self, email):
        """Add additional user information"""
        try:
            # Create window for adding information
            info_window = tk.Toplevel(self)
            info_window.title("Add Additional Information")
            info_window.geometry("800x500")  # Increase window size
            info_window.configure(bg=self.style["bg_color"])

            # Large text box for information entry
            tk.Label(
                info_window,
                text="Enter additional information:",
                font=self.style["label_font"],  # Increase font size
                bg=self.style["bg_color"],
                fg=self.style["text_color"],
            ).pack(pady=20)

            # Enlarge text box
            text_area = tk.Text(
                info_window,
                height=10,
                width=20,  # Increase width
                font=("Arial", 14),  # Increase font size
                bg="white",
                fg="black",
            )
            text_area.pack(pady=20, padx=30)  # Increase margins

            def save_info():
                # Find user file and append information
                user_files = [f for f in os.listdir(BASE_DIR) if email.lower() in f.lower()]
                if user_files:
                    user_file = os.path.join(BASE_DIR, user_files[0])
                    with open(user_file, "a") as file:
                        file.write("\nAdditional Info: " + text_area.get("1.0", tk.END))
                    messagebox.showinfo("Success", "Information added successfully!")
                    info_window.destroy()

            tk.Button(
                info_window,
                text="Save Information",
                command=save_info,
                font=self.style["button_font"],
                bg=self.style["button_color"],
                fg="white",
                width=20,  # Enlarge button width
                height=2,  # Enlarge button height
            ).pack(pady=20)

        except Exception as e:
            messagebox.showerror("Error", f"Error adding information: {str(e)}")

    def handle_logout(self, dashboard_window):
        """Handle user logout"""
        dashboard_window.destroy()  # Close dashboard window
        self.create_main_menu()  # Return to main menu

    def add_back_button(self, window, command=None):
        """Add back button uniformly"""
        if command is None:
            command = window.destroy

        back_btn = tk.Button(
            window,
            text="Back",
            command=command,
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg=self.style["secondary_text"],
            relief=tk.FLAT,
            cursor="hand2",
            width=15,
        )
        back_btn.pack(pady=10)
        return back_btn

    def show_my_projects(self, email):
        try:
            all_projects = projects.load_projects()
            my_projects = [p for p in all_projects if p.email == email]

            projects_window = tk.Toplevel(self)
            projects_window.title("My Projects")
            projects_window.geometry("1000x800")
            projects_window.configure(bg=self.style["bg_color"])

            # Scrollable frame
            canvas = tk.Canvas(projects_window, bg=self.style["bg_color"])
            scrollbar = tk.Scrollbar(projects_window, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.style["bg_color"])

            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Add mouse wheel support
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            canvas.bind_all("<MouseWheel>", _on_mousewheel)

            # Unbind on window close
            def _on_frame_destroy(event):
                canvas.unbind_all("<MouseWheel>")

            projects_window.bind("<Destroy>", _on_frame_destroy)

            if not my_projects:
                tk.Label(
                    scrollable_frame,
                    text="You have no projects yet",
                    font=self.style["label_font"],
                    bg=self.style["bg_color"],
                    fg="black",
                ).pack(pady=20)
            else:
                for i, project in enumerate(my_projects, 1):
                    self.create_project_frame(scrollable_frame, project, i)

            # Organize scrolling elements
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Back button
            self.add_back_button(projects_window)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load projects: {str(e)}")

    def create_new_project(self, email):
        project_window = tk.Toplevel(self)
        project_window.title("Create New Project")
        project_window.geometry("600x700")
        project_window.configure(bg=self.style["bg_color"])

        # Main container frame
        main_frame = tk.Frame(project_window, bg=self.style["bg_color"])
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Back button at the top
        back_btn = tk.Button(
            main_frame,
            text="Back to Dashboard",
            command=lambda: [project_window.destroy(), self.show_user_dashboard(email)],
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg="white",
        )
        back_btn.pack(pady=(0, 20))

        # Form frame
        form_frame = tk.Frame(main_frame, bg=self.style["frame_bg"])
        form_frame.pack(expand=True, fill="both")

        # Project creation fields
        fields = [
            ("Title:", "title"),
            ("Details:", "details"),
            ("Category:", "category"),
            ("Target Amount:", "target"),
        ]

        entries = {}
        for label_text, field_name in fields:
            frame = tk.Frame(form_frame, bg=self.style["frame_bg"])
            frame.pack(pady=10)

            label = tk.Label(
                frame,
                text=label_text,
                font=self.style["label_font"],
                bg=self.style["frame_bg"],
                fg=self.style["text_color"],
            )
            label.pack(side=tk.LEFT, padx=10)

            if field_name == "details":
                entry = tk.Text(frame, width=30, height=4)
            else:
                entry = tk.Entry(frame, width=30)
            entry.pack(side=tk.LEFT, padx=5)
            entries[field_name] = entry

        # Add calendar for start date
        start_date_frame = tk.Frame(form_frame, bg=self.style["frame_bg"])
        start_date_frame.pack(pady=10)
        tk.Label(
            start_date_frame,
            text="Start Date:",
            font=self.style["label_font"],
            bg=self.style["frame_bg"],
            fg=self.style["text_color"],
        ).pack(side=tk.LEFT, padx=10)
        start_date_entry = tk.Entry(start_date_frame, width=30)
        start_date_entry.pack(side=tk.LEFT, padx=5)
        start_date_btn = tk.Button(
            start_date_frame,
            text="Select Date",
            command=lambda: self.show_calendar(start_date_entry),
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg="white",
        )
        start_date_btn.pack(side=tk.LEFT, padx=5)

        # Add calendar for end date
        end_date_frame = tk.Frame(form_frame, bg=self.style["frame_bg"])
        end_date_frame.pack(pady=10)
        tk.Label(
            end_date_frame,
            text="End Date:",
            font=self.style["label_font"],
            bg=self.style["frame_bg"],
            fg=self.style["text_color"],
        ).pack(side=tk.LEFT, padx=10)
        end_date_entry = tk.Entry(end_date_frame, width=30)
        end_date_entry.pack(side=tk.LEFT, padx=5)
        end_date_btn = tk.Button(
            end_date_frame,
            text="Select Date",
            command=lambda: self.show_calendar(end_date_entry),
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg="white",
        )
        end_date_btn.pack(side=tk.LEFT, padx=5)

        def submit_project():
            try:
                # Create project object directly
                project = projects.Project.__new__(projects.Project)
                project.email = email
                project.project_id = projects.get_next_project_id()
                project.title = entries["title"].get()
                project.details = entries["details"].get("1.0", tk.END).strip()
                project.category = entries["category"].get()

                try:
                    project.target = float(entries["target"].get())
                except ValueError:
                    messagebox.showerror("Error", "Target amount must be a number!")
                    return

                # Date validation
                try:
                    from datetime import datetime

                    project.start_time = datetime.strptime(start_date_entry.get(), "%Y-%m-%d")
                    project.end_time = datetime.strptime(end_date_entry.get(), "%Y-%m-%d")

                    if project.start_time < datetime.now():
                        messagebox.showerror("Error", "Start date cannot be in the past!")
                        return
                    if project.end_time <= project.start_time:
                        messagebox.showerror("Error", "End date must be after start date!")
                        return
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid dates in YYYY-MM-DD format!")
                    return

                # Default values
                project.donations = 0.0
                project.is_active = True

                # Save project
                project.save_to_file()
                messagebox.showinfo("Success", "Project created successfully!")
                project_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to create project: {str(e)}")
                print(f"Debug - Project creation error: {str(e)}")  # للتشخيص

        # Buttons in one frame
        button_frame = tk.Frame(form_frame, bg=self.style["frame_bg"])
        button_frame.pack(pady=20)

        # Create project button
        submit_btn = tk.Button(
            button_frame,
            text="Create Project",
            command=submit_project,
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg=self.style["secondary_text"],
            relief=tk.FLAT,
            cursor="hand2",
            width=15,
        )
        submit_btn.pack(side=tk.LEFT, padx=10)

        # Back button - Modify to use the same back function
        back_btn2 = tk.Button(
            button_frame,
            text="Back",
            command=lambda: [project_window.destroy(), self.show_user_dashboard(email)],
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg=self.style["secondary_text"],
            relief=tk.FLAT,
            cursor="hand2",
            width=15,
        )
        back_btn2.pack(side=tk.LEFT, padx=10)

    def show_calendar(self, entry):
        """Show date picker calendar"""
        calendar_window = tk.Toplevel(self)
        calendar_window.title("Select Date")
        calendar_window.geometry("300x300")
        calendar_window.configure(bg=self.style["bg_color"])

        cal = Calendar(calendar_window, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(pady=20)

        def select_date():
            entry.delete(0, tk.END)
            entry.insert(0, cal.get_date())
            calendar_window.destroy()

        select_btn = tk.Button(
            calendar_window,
            text="Select",
            command=select_date,
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg="white",
        )
        select_btn.pack(pady=10)

    def show_all_projects(self):
        """Display all available projects"""
        try:
            all_projects = projects.load_projects()

            projects_window = tk.Toplevel(self)
            projects_window.title("All Projects")
            projects_window.geometry("1000x800")  # نفس حجم نافذة مشاريعي
            projects_window.configure(bg=self.style["bg_color"])

            # إطار قابل للتمرير
            canvas = tk.Canvas(projects_window, bg=self.style["bg_color"])
            scrollbar = tk.Scrollbar(projects_window, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.style["bg_color"])

            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # إضافة دعم بكرة الماوس
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            canvas.bind_all("<MouseWheel>", _on_mousewheel)

            # إلغاء الربط عند إغلاق النافذة
            def _on_frame_destroy(event):
                canvas.unbind_all("<MouseWheel>")

            projects_window.bind("<Destroy>", _on_frame_destroy)

            if not all_projects:
                tk.Label(
                    scrollable_frame,
                    text="No projects available",
                    font=self.style["label_font"],
                    bg=self.style["bg_color"],
                ).pack(pady=20)
            else:
                for i, project in enumerate(all_projects, 1):
                    project_frame = self.create_project_frame(scrollable_frame, project, i)
                    if project.is_active:
                        donate_frame = tk.Frame(project_frame, bg=self.style["bg_color"])
                        donate_frame.pack(pady=10)

                        amount_entry = tk.Entry(donate_frame, width=15)
                        amount_entry.pack(side=tk.LEFT, padx=5)

                        donate_btn = tk.Button(
                            donate_frame,
                            text="Donate",
                            command=lambda p=project, e=amount_entry: self.make_donation(p, e),
                            font=self.style["button_font"],
                            bg=self.style["button_color"],
                            fg="white",
                        )
                        donate_btn.pack(side=tk.LEFT)

            # تنظيم عناصر التمرير
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # زر العودة
            self.add_back_button(projects_window)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load projects: {str(e)}")

    def make_donation(self, project, amount_entry):
        try:
            if not hasattr(self, "current_user_email") or not self.current_user_email:
                messagebox.showerror("Error", "Please log in to make a donation")
                return

            amount = float(amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than zero!")
                return

            if project.donations >= project.target:
                messagebox.showerror("Error", "This project has already reached its target!")
                return

            remaining = project.target - project.donations
            if amount > remaining:
                if messagebox.askyesno(
                    "Warning",
                    f"The project only needs {remaining:.2f} EGP more. "
                    f"Would you like to donate this amount instead?",
                ):
                    amount = remaining
                else:
                    return

            # إجراء التبرع باستخدام البريد الإلكتروني للمستخدم الحالي
            project.donate(amount, self.current_user_email)

            # تحديث مسار حفظ التبرعات ليكون في مجلد users/user_donations
            donation_file = os.path.join(
                BASE_DIR, "user_donations", f"{self.current_user_email}_donations.txt"
            )
            os.makedirs(os.path.dirname(donation_file), exist_ok=True)

            with open(donation_file, "a") as file:
                file.write(
                    f"Project: {project.title}\n"
                    f"Amount: {amount:.2f} EGP\n"
                    f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"{'=' * 50}\n"
                )

            messagebox.showinfo("Success", f"Successfully donated {amount:.2f} EGP to {project.title}")

            # إغلاق نافذة المشاريع والعودة للوحة التحكم
            for widget in self.winfo_children():
                if isinstance(widget, tk.Toplevel):
                    widget.destroy()
            self.show_user_dashboard(self.current_user_email)

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")
        except Exception as e:
            messagebox.showerror("Error", f"Donation failed: {str(e)}")

    def refresh_project_list(self):
        """تحديث قائمة المشاريع"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.show_all_projects()

    def show_my_donations(self, email):
        try:
            donations_file = os.path.join(BASE_DIR, "user_donations", f"{email}_donations.txt")

            donations_window = tk.Toplevel(self)
            donations_window.title("My Donations")
            donations_window.geometry("800x600")
            donations_window.configure(bg=self.style["bg_color"])

            # إضافة ScrolledText لعرض التبرعات
            from tkinter import scrolledtext

            text_area = scrolledtext.ScrolledText(
                donations_window,
                wrap=tk.WORD,
                width=70,
                height=20,
                font=self.style["label_font"],
                bg="white",
                fg="black",
            )
            text_area.pack(pady=20)

            if os.path.exists(donations_file):
                with open(donations_file, "r") as file:
                    content = file.read()
                    if content.strip():
                        text_area.insert(tk.END, content)
                    else:
                        text_area.insert(tk.END, "No donations found.")
            else:
                text_area.insert(tk.END, "No donations found.")

            text_area.configure(state="disabled")
            self.add_back_button(donations_window)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load donations: {str(e)}")

    def create_progress_bar(self, parent, progress, width=200):
        """Create progress bar visualization
        Shows completion percentage both graphically and numerically"""
        frame = tk.Frame(parent, bg=self.style["bg_color"])
        frame.pack(pady=5, fill="x")

        # Outer frame (white)
        bar_bg = tk.Canvas(
            frame, width=width, height=20, bg="white", highlightthickness=1, highlightbackground="gray"
        )
        bar_bg.pack(side=tk.LEFT, padx=10)

        # Filled portion (green)
        filled_width = (progress * width) / 100
        if filled_width > 0:  # Avoid drawing if width is 0
            bar_bg.create_rectangle(0, 0, filled_width, 20, fill="#2ecc71", width=0)  # Nice green color

        # Percentage as text
        percentage_label = tk.Label(
            frame,
            text=f"{progress:.1f}%",
            font=self.style["label_font"],
            bg=self.style["bg_color"],
            fg="black",
        )
        percentage_label.pack(side=tk.LEFT, padx=5)

        return frame

    def create_project_frame(self, parent, project, index=None):
        """Create frame to display project information with progress bar"""
        frame = tk.Frame(parent, bg=self.style["bg_color"], relief="solid", borderwidth=1)
        frame.pack(pady=10, padx=20, fill="x")

        # Project title and number in larger size and higher
        title_text = f"{index}. " if index else ""
        title_text += f"Project: {project.title}"

        title = tk.Label(
            frame,
            text=title_text,
            font=tkfont.Font(family="Arial", size=36, weight="bold"),  # Increase font size 3 times
            bg=self.style["bg_color"],
            fg="black",
        )
        title.pack(anchor="w", padx=10, pady=(20, 5))  # Increase top margin

        # Add project button
        project_button = tk.Button(
            frame,
            text="View Project Details",
            command=lambda p=project: self.show_project_details(p),
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg="white",
        )
        project_button.pack(pady=10)

        # Project details
        details = (
            f"Creator: {project.email}\n"
            f"Category: {project.category}\n"
            f"Target: {project.target:.2f} EGP\n"
            f"Current: {project.donations:.2f} EGP\n"
            f"Status: {'Active' if project.is_active else 'Inactive'}"
        )

        tk.Label(
            frame,
            text=details,
            font=self.style["label_font"],
            bg=self.style["bg_color"],
            fg="black",
            justify=tk.LEFT,
        ).pack(anchor="w", padx=10)

        # Add progress bar
        progress = (project.donations / project.target * 100) if project.target > 0 else 0
        self.create_progress_bar(frame, progress)

        return frame

    def show_project_details(self, project):
        """Display project details in a separate window"""
        details_window = tk.Toplevel(self)
        details_window.title(f"Project Details: {project.title}")
        details_window.geometry("800x600")
        details_window.configure(bg=self.style["bg_color"])

        details_frame = tk.Frame(details_window, bg=self.style["bg_color"])
        details_frame.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(
            details_frame,
            text=project.title,
            font=tkfont.Font(family="Arial", size=36, weight="bold"),
            bg=self.style["bg_color"],
        ).pack(pady=(0, 20))

        details = (
            f"Creator: {project.email}\n"
            f"Category: {project.category}\n"
            f"Details: {project.details}\n"
            f"Target: {project.target:.2f} EGP\n"
            f"Current: {project.donations:.2f} EGP\n"
            f"Start Date: {project.start_time}\n"
            f"End Date: {project.end_time}\n"
            f"Status: {'Active' if project.is_active else 'Inactive'}"
        )

        tk.Label(
            details_frame,
            text=details,
            font=self.style["label_font"],
            bg=self.style["bg_color"],
            justify=tk.LEFT,
        ).pack(anchor="w")

        progress = (project.donations / project.target * 100) if project.target > 0 else 0
        self.create_progress_bar(details_frame, progress, width=400)

        button_frame = tk.Frame(details_window, bg=self.style["bg_color"])
        button_frame.pack(side=tk.BOTTOM, pady=20)

        tk.Button(
            button_frame,
            text="View Donation History",
            command=lambda: self.show_donation_history(project),
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg="white",
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="Show Donation Graph",
            command=lambda: self.show_donation_graph(project),
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg="white",
        ).pack(side=tk.LEFT, padx=10)

        if hasattr(self, "current_user_email") and project.email == self.current_user_email:
            if project.donations < (0.25 * project.target):
                tk.Button(
                    button_frame,
                    text="Delete Project",
                    command=lambda: self.delete_project(project, details_window),
                    font=self.style["button_font"],
                    bg="#e74c3c",
                    fg="white",
                ).pack(side=tk.LEFT, padx=10)
            else:
                tk.Label(
                    button_frame,
                    text="Project cannot be deleted (>25% funded)",
                    font=self.style["label_font"],
                    bg=self.style["bg_color"],
                    fg="red",
                ).pack(side=tk.LEFT, padx=10)

        self.add_back_button(button_frame, details_window.destroy)

    def show_donation_graph(self, project):
        """Display a chart of donation activity"""
        try:
            with open(projects.DONATIONS_FILE, "r") as file:
                lines = file.readlines()
                project_donations = [line for line in lines if f"Project ID: {project.project_id}" in line]

                if project_donations:
                    dates = []
                    amounts = []
                    for donation in project_donations:
                        parts = donation.split(", ")
                        date_str = parts[-1].split(": ")[1].strip()
                        amount_str = parts[1].split(": ")[1].strip()
                        dates.append(datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"))
                        amounts.append(float(amount_str))

                    plt.figure(figsize=(10, 5))
                    plt.plot(dates, amounts, marker="o")
                    plt.title(f"Donation History for {project.title}")
                    plt.xlabel("Date")
                    plt.ylabel("Amount (EGP)")
                    plt.grid(True)
                    plt.show()
                else:
                    messagebox.showinfo("Info", "No donations found for this project.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load donation history: {str(e)}")

    def show_donation_history(self, project):
        """Display the project's donation history"""
        history_window = tk.Toplevel(self)
        history_window.title(f"Donation History: {project.title}")
        history_window.geometry("600x400")
        history_window.configure(bg=self.style["bg_color"])

        from tkinter import scrolledtext

        text_area = scrolledtext.ScrolledText(
            history_window,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=self.style["label_font"],
            bg="white",
            fg="black",
        )
        text_area.pack(pady=20)

        try:
            with open(projects.DONATIONS_FILE, "r") as file:
                lines = file.readlines()
                project_donations = [line for line in lines if f"Project ID: {project.project_id}" in line]

                if project_donations:
                    for donation in project_donations:
                        text_area.insert(tk.END, donation)
                else:
                    text_area.insert(tk.END, "No donations found for this project.")

        except FileNotFoundError:
            text_area.insert(tk.END, "No donations found for this project.")
        except Exception as e:
            text_area.insert(tk.END, f"Error loading donation history: {str(e)}")

        text_area.configure(state="disabled")
        self.add_back_button(history_window)

    def delete_project(self, project, window):
        """Delete project and refresh the current window"""
        if messagebox.askyesno(
            "Confirm Deletion", f"Are you sure you want to delete project '{project.title}'?"
        ):
            try:
                projects.delete_project(project)
                messagebox.showinfo("Success", "Project deleted successfully!")

                # Close the details window
                window.destroy()

                # Get all top level windows
                for widget in self.winfo_children():
                    if isinstance(widget, tk.Toplevel):
                        # Destroy the old projects window entirely
                        widget.destroy()

                # Show fresh projects window
                self.show_my_projects(self.current_user_email)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete project: {str(e)}")

    def show_donation_form(self, project, parent_window):
        """Display the donation form"""
        donation_window = tk.Toplevel(parent_window)
        donation_window.title(f"Donate to {project.title}")
        donation_window.geometry("400x200")
        donation_window.configure(bg=self.style["bg_color"])

        frame = tk.Frame(donation_window, bg=self.style["bg_color"])
        frame.pack(expand=True)

        tk.Label(
            frame, text="Enter donation amount:", font=self.style["label_font"], bg=self.style["bg_color"]
        ).pack(pady=10)

        amount_entry = tk.Entry(frame, width=20)
        amount_entry.pack(pady=10)

        def handle_enter(event):
            self.make_donation(project, amount_entry)
            donation_window.destroy()

        amount_entry.bind("<Return>", handle_enter)
        amount_entry.focus()

        donate_btn = tk.Button(
            frame,
            text="Donate",
            command=lambda: [self.make_donation(project, amount_entry), donation_window.destroy()],
            font=self.style["button_font"],
            bg=self.style["button_color"],
            fg="white",
        )
        donate_btn.pack(pady=10)

        self.add_back_button(frame, donation_window.destroy)

    def update_file(self, filename, field, new_value):
        """Update data in user file
        Handles both password changes and other field updates"""
        try:
            with open(filename, "r") as file:
                lines = file.readlines()

            email = None
            for line in lines:
                if line.startswith("Email:"):
                    email = line.split(":")[1].strip()
                    break

            if field == "Password":
                new_filename = os.path.join(BASE_DIR, f"{email}X_X{new_value}X_X.txt")

                with open(new_filename, "w") as file:
                    for line in lines:
                        if line.startswith("Password:"):
                            file.write(f"Password:{'*' * len(new_value)}\n")
                        else:
                            file.write(line)

                os.remove(filename)

                messagebox.showinfo("Success", "Password updated successfully!")
            else:
                with open(filename, "w") as file:
                    for line in lines:
                        if line.startswith(f"{field}:"):
                            file.write(f"{field}:{new_value}\n")
                        else:
                            file.write(line)

                messagebox.showinfo("Success", f"{field} updated successfully!")

            return True

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update {field}: {str(e)}")
            return False


if __name__ == "__main__":
    app = CrowdfundingApp()
    app.mainloop()
