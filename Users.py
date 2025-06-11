import os
import re
import msvcrt
import sys
import time  # Add time import here
from colorama import Fore, Style
import projects as projects_module
import datetime

# Enable UTF-8 encoding
sys.stdout.recoding = "utf-8"


def goodbyemsg():
    print(Fore.RED + "Closing.")
    time.sleep(0.1)

    print(Fore.RED + "Closing..")
    time.sleep(0.1)

    print(Fore.RED + "Closing....")
    time.sleep(0.1)

    print(Fore.RED + "Goodbye <3......")
    time.sleep(0.4)

    print(Fore.RESET)


# -*- coding: utf-8 -*-
# Welcome message

Main_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(Main_DIR, "users")  # Path to users folder


# Registration ##########################################
def clear_screen():
    os.system("cls")


def userFnameInput():
    while True:
        Fname = input("Enter your first name:\n")
        if Fname.isalpha():
            return Fname
        else:
            print("Please enter a valid first name without numbers.")


def userLnameInput():
    while True:
        Lname = input("Enter your last name:\n")
        if Lname.isalpha():
            return Lname
        else:
            print("Please enter a valid last name without numbers.")


def userEmailInput():
    while True:
        Email = input("Enter your Email:\n")
        if re.match(r"[^@]+@[^@]+\.[^@]+", Email):
            return Email
        else:
            print("Please enter a valid email address.")


def get_password(prompt):
    print(prompt, end="", flush=True)
    password = ""
    while True:
        char = msvcrt.getch()
        if char == b"\r" or char == b"\n":
            print("")
            break
        elif char == b"\x08":
            if len(password) > 0:
                password = password[:-1]
                print("\b \b", end="", flush=True)
        else:
            password += char.decode("utf-8")
            print("*", end="", flush=True)
    return password


def DeleteAccount(email, password):
    """Delete user account"""
    # Get all files that match this email regardless of password
    matching_files = [f for f in os.listdir(BASE_DIR) if email.lower().strip() in f.lower()]

    if matching_files:
        try:
            # Delete all matching files except donation files
            for filename in matching_files:
                if "donations" not in filename:  # Skip donation files
                    filepath = os.path.join(BASE_DIR, filename)
                    if os.path.exists(filepath):
                        os.remove(filepath)
            return True
        except Exception as e:
            raise Exception(f"Failed to delete account: {str(e)}")
    else:
        raise Exception("Account not found")


def userPasswordInput():
    return get_password("Enter a new password:\n")


def userPasswordConfirmationInput():
    return get_password("Confirm your password:\n")


def userPhoneInput():
    while True:
        MobilePhone = input("Enter your MobilePhone:\n")
        # Validate Egyptian phone number format
        if re.match(r"^01[0-2,5]{1}[0-9]{8}$", MobilePhone):
            return MobilePhone
        else:
            print("Please enter a valid Egyptian mobile phone number.")


class User:
    def __init__(self):
        self.Fname = userFnameInput()
        self.Lname = userLnameInput()
        self.Email = userEmailInput()

        if self.is_email_registered(self.Email):
            print("This email is already registered. Please use a different email.")
            return

        self.Password = userPasswordInput()
        while True:
            self.PasswordConfirmation = userPasswordConfirmationInput()
            if self.PasswordConfirmation == self.Password:
                break
            else:
                print("Passwords don't match")
        self.MobilePhone = userPhoneInput()
        self.create_user_file()
        print(Fore.YELLOW + "Registration successful. Returning to main menu.")
        return

    def __str__(self):
        return self.Fname + " " + self.Lname

    def FileName(self):
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)
        return os.path.join(BASE_DIR, f"{self.Email}X_X{self.Password}X_X.txt")

    def create_user_file(self):
        filename = self.FileName()
        with open(filename, "w") as file:
            file.write(f"First_name:{self.Fname}\n")
            file.write(f"Last_name:{self.Lname}\n")
            file.write(f"Email:{self.Email}\n")
            file.write(f"Password:{self.Password}\n")  # Store actual password instead of asterisks
            file.write(f"Mobile phone:{self.MobilePhone}\n")

    def is_email_registered(self, email):
        email_files = os.listdir(BASE_DIR)
        for file in email_files:
            if email.lower().strip() in file.lower().strip():  # Check if email is already registered
                return True
        return False

    @staticmethod
    def passwordReset():
        email = userEmailInput()
        # filename = os.path.join(BASE_DIR, f"{email}X_X*.txt")
        matching_files = [f for f in os.listdir(BASE_DIR) if re.match(f"{email}X_X.*.txt", f)]
        if matching_files:
            user_data_file = matching_files[0]
            with open(os.path.join(BASE_DIR, user_data_file), "r") as file:
                content = file.read().split("\n")
                phone_line = [line for line in content if "Mobile phone:" in line][0]
                registered_phone = phone_line.split(":")[1]
                entered_phone = userPhoneInput()
                if entered_phone == registered_phone:
                    newPassword = userPasswordInput()
                    while True:
                        newPasswordConfirmation = userPasswordConfirmationInput()
                        if newPasswordConfirmation == newPassword:
                            with open(os.path.join(BASE_DIR, user_data_file), "w") as file:
                                file.write(f"First_name:{content[0].split(':')[1]}\n")
                                file.write(f"Last_name:{content[1].split(':')[1]}\n")
                                file.write(f"Email:{email}\n")
                                file.write(f"Password:{newPassword}\n")
                                file.write(f"Mobile phone:{entered_phone}\n")
                            print(Fore.YELLOW + "Password has been reset successfully.")
                            break
                        else:
                            print("Passwords don't match")
                else:
                    print("Invalid phone number")
        else:
            print("Invalid email")

    def update_user_file(self):
        filename = self.FileName()
        with open(filename, "w") as file:
            file.write(f"First_name:{self.Fname}\n")
            file.write(f"Last_name:{self.Lname}\n")
            file.write(f"Email:{self.Email}\n")
            file.write(f"Password:{self.Password}\n")
            file.write(f"Mobile phone:{self.MobilePhone}\n")


def loginInput():
    try:
        print(Fore.RED + "What would you like to do?" + Style.RESET_ALL)
        print("1. Show data")
        print("2. Show my projects only")
        print("3. Create a new project")
        print("4. Show ALL projects")
        print("5. Show my donations")
        print("6. Change your data")
        print("7. Add new info as you want")
        print(Fore.GREEN + "8. Back" + Style.RESET_ALL)

        func = int(input())
        if func not in [1, 2, 3, 4, 5, 6, 7, 8]:
            print("Invalid input")
            return None
        elif func == 8:
            return False
        else:
            return func
    except ValueError:
        print("Invalid input")
        return None


def loginSelection(email, password):
    filename = AccountLogin(email, password)
    while True:
        choosen = loginInput()
        if choosen is None:
            continue
        elif choosen == 1:
            with open(filename, "r") as file:
                content = file.read()
                print(content)
            if not Again():
                break
        elif choosen == 2:  # Show my projects only
            all_projects = projects_module.load_projects()  # Use the renamed module
            projects_module.list_my_projects_with_options(email, all_projects)
        elif choosen == 3:  # Create a new project
            try:
                project = projects_module.Project(email)
                project.save_to_file()
                print(Fore.YELLOW + "Project added successfully!\n" + Style.RESET_ALL)
            except Exception as e:
                print(f"Error adding project: {e}")
        elif choosen == 4:  # Show ALL projects
            all_projects = projects_module.load_projects()  # Use the renamed module
            projects_module.list_all_projects_and_donate(all_projects, email)
        elif choosen == 5:  # Show my donations
            projects_module.list_my_donations(email)  # Use the renamed module
        elif choosen == 6:  # Change your data
            if editSelection(filename):
                break
        elif choosen == 7:  # Add new info as you want
            with open(filename, "a") as file:
                file.write(input("\n" + "What do you want to add?\n") + "\n")
                print("Data added successfully.")
            if not Again():
                break
        elif choosen is False:
            break


def editSelection(filename):
    options = {
        1: "First_name",
        2: "Last_name",
        3: "Password",
        4: "Mobile phone",
        5: Fore.GREEN + "back" + Style.RESET_ALL,
    }
    print(Fore.RED + "What do you want to change?" + Style.RESET_ALL)
    for key, value in options.items():
        print(f"{key}. {value}")

    try:
        choice = int(input())
        if choice not in options:
            print("Invalid choice")
            return False

        if choice == 1:
            new_value = userFnameInput()
        elif choice == 2:
            new_value = userLnameInput()
        elif choice == 3:
            new_value = userPasswordInput()
            while new_value != userPasswordConfirmationInput():
                print("Passwords don't match")
                new_value = userPasswordInput()
            update_file(filename, options[choice], new_value)
            return True
        elif choice == 4:
            new_value = userPhoneInput()
        elif choice == 5:
            return False
        update_file(filename, options[choice], new_value)
        return False
    except ValueError:
        print("Invalid input")
        return False


def update_file(filename, field, new_value):
    """Update user data securely"""
    try:
        # Read current data and keep it
        with open(filename, "r") as file:
            lines = file.readlines()

        # Extract email
        email = None
        current_data = {}
        for line in lines:
            if ":" in line:
                key, value = line.strip().split(":", 1)
                current_data[key] = value
                if key == "Email":
                    email = value.strip()

        if field == "Password":
            # Create new file with same data but new password
            new_filename = os.path.join(BASE_DIR, f"{email}X_X{new_value}X_X.txt")

            try:
                # Write data to new file
                with open(new_filename, "w") as file:
                    for key, value in current_data.items():
                        if key == "Password":
                            file.write(f"Password:{new_value}\n")
                        else:
                            file.write(f"{key}:{value}\n")

                # Make sure new file was created successfully
                if os.path.exists(new_filename):
                    os.remove(filename)  # Only delete old file after successful creation
                    print("Password updated successfully!")
                    return True

            except Exception as e:
                # If error occurs, delete new file if created
                if os.path.exists(new_filename):
                    os.remove(new_filename)
                raise e
        else:
            # Update other data in same file
            current_data[field] = new_value
            with open(filename, "w") as file:
                for key, value in current_data.items():
                    file.write(f"{key}:{value}\n")
            print(f"{field} updated successfully!")
            return True

    except Exception as e:
        print(f"Error updating {field}: {e}")
        return False


def AccountLogin(email, password):
    filename = os.path.join(BASE_DIR, email + "X_X" + password + "X_X.txt")
    return filename


def UserLogin(email=None, password=None):
    """User login supporting both GUI and console modes"""
    if email is None and password is None:
        email = userEmailInput()
        password = get_password("Enter your password:\n")

    # Check if users folder exists
    if not os.path.exists(BASE_DIR):
        return False

    # Search for user files
    matching_files = [f for f in os.listdir(BASE_DIR) if email.lower().strip() in f.lower()]

    if not matching_files:
        return False

    # Search for file matching password
    filename = os.path.join(BASE_DIR, f"{email}X_X{password}X_X.txt")

    # Verify file exists
    if not os.path.exists(filename):
        return False

    try:
        # Try reading file to verify validity
        with open(filename, "r") as file:
            content = file.readlines()
            if not any(line.startswith("Email:") for line in content):
                return False
    except Exception:
        return False

    if email is None or password is None:
        loginSelection(email, password)
    return True


def functionInput():
    try:
        print(Fore.RED + "What would you like to do?" + Style.RESET_ALL)
        print("1. Register")
        print("2. Login")
        print("3. Delete account")
        print(Fore.GREEN + "4. Exit" + Style.RESET_ALL)

        func = int(input())
        if func not in [1, 2, 3, 4]:
            print("Invalid input")
            return functionInput()
        elif func == 4:
            goodbyemsg()
            # print("Goodbye <3")
            return False
        else:
            return func
    except ValueError:
        print("Invalid input")
        return functionInput()


def Again():
    while True:
        again = input(Fore.YELLOW + "Do you need another function? (Y,N)\n" + Style.RESET_ALL)
        if again == "Y" or again == "y":
            return True
        elif again == "N" or again == "n":
            goodbyemsg()
            # print("Goodbye <3")
            return False
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")


# Record donation details
def record_donation(email, amount, project_name):
    # filename = os.path.join(BASE_DIR, f"{email}X_X*.txt")
    matching_files = [f for f in os.listdir(BASE_DIR) if re.match(f"{email}X_X.*.txt", f)]

    if matching_files:
        user_data_file = matching_files[0]
        donation_details = f"Donation Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        donation_details += f"Project: {project_name}\n"
        donation_details += f"Amount Donated: {amount}\n"

        with open(os.path.join(BASE_DIR, user_data_file), "a") as file:
            file.write(donation_details)
        print(Fore.GREEN + f"Your donation of {amount} for {project_name} has been recorded successfully!")
    else:
        print("User file not found. Donation not recorded.")


# Make a donation
def make_donation(email):
    project_name = input(Fore.CYAN + "Enter the project name you want to donate to:\n")
    try:
        amount = float(input("Enter the donation amount:\n"))
        if amount > 0:
            # Record the donation
            record_donation(email, amount, project_name)
        else:
            print("Donation amount must be positive.")
    except ValueError:
        print("Invalid amount entered.")
