# Crowd-Funding Platform

A desktop application built with Python/Tkinter that allows users to create and manage fundraising projects.

Repository: [Crowd-Funding-GUI](https://github.com/ahmedy1902/Crowd-Funding-GUI)

## Features

- 👤 User Authentication
  - Register new account
  - Login/Logout functionality 
  - Reset password
  - Delete account
  - Profile picture management

- 💰 Project Management
  - Create fundraising projects
  - View all projects
  - Track project progress with visual progress bars
  - Delete projects (if less than 25% funded)

- 📊 Donations
  - Make donations to active projects
  - View donation history
  - Visual graphs showing donation activity
  - Track personal donations

- 🎨 Modern UI
  - Clean and intuitive interface
  - Progress bars and visualizations
  - Responsive scrollable views
  - Consistent styling throughout

## Technical Details

- Built with Python 3.x
- GUI implemented using Tkinter
- Data stored in text files
- Dependencies:
  - tkcalendar
  - matplotlib
  - PIL
  - colorama

## Project Structure

```
Crowd-Funding GUI/
│
├── gui_app.py      # Main GUI application
├── Users.py        # User management functionality  
├── projects.py     # Project management functionality
├── main.py         # Application entry point
│
└── users/          # User data storage
    ├── profile_pictures/
    └── user_donations/
```

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/ahmedy1902/Crowd-Funding-GUI.git
cd Crowd-Funding-GUI
```

2. Install dependencies:
```bash
pip install tkcalendar matplotlib pillow colorama
```

3. Run the application:
```bash
python main.py
```

## Contributors

Created by [Ahmed Yasser] as part of the ITI Python Projects

## License

This project is licensed under the MIT License - see the LICENSE file for details
