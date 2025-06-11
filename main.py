import os
import sys
import Users

from colorama import Fore, Style

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)


def main():
    try:
        # Import GUI app
        from gui_app import CrowdfundingApp
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()  # Hide the root window

        app = CrowdfundingApp()  # Create the main application window
        app.mainloop()  # Start the GUI event loop

    except ImportError:
        print("Running in console mode...")

        # Show welcome message
        welcome_msg = "Welcome To Crowd-Funding App App  <3"
        colors = [Style.RESET_ALL, Fore.RED, Fore.YELLOW, Fore.BLUE]
        for color in colors:
            print(color + welcome_msg + Style.RESET_ALL)

        # Run console mode
        while True:
            selection = Users.functionInput()
            if selection == 1:
                Users.User()
            elif selection == 2:
                Users.UserLogin()
            elif selection == 3:
                email = Users.userEmailInput()
                password = Users.get_password("Enter your password:\n")
                Users.DeleteAccount(email, password)
                if not Users.Again():
                    break
            elif selection is False:
                break


# if __name__ == "__main__":
#     init()  # Initialize colorama
#     main()
welcome_msg = "Welcome To Crowd-Funding App <3"
colors = [Style.RESET_ALL, Fore.RED, Fore.YELLOW, Fore.BLUE]
for color in colors:
    print(color + welcome_msg + Style.RESET_ALL)

    # Run console mode
    while True:
        selection = Users.functionInput()
        if selection == 1:
            Users.User()
        elif selection == 2:
            Users.UserLogin()
        elif selection == 3:
            email = Users.userEmailInput()
            password = Users.get_password("Enter your password:\n")
            Users.DeleteAccount(email, password)
            if not Users.Again():
                break
        elif selection is False:
            break
