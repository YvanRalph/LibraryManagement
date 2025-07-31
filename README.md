# 📚Library Management CLI System
A simple, interactive command-line application for library employees to manage books, users, rentals, and returns.

Built with Python and SQLite, this tool helps small libraries keep track of their book inventory and customer activity efficiently — all through the terminal.

# Features
  * Add New Books  
  * Register New Users  
  * Rent and Return Books  
  * Search Books by Name or Author  
  * View Books Currently in Stock  
  * Track Rent History & Return Fines  
  * Handle Duplicates and Validation Gracefully


# Technologies Used
  * Python 3.x  
  * SQLite3 (via sqlite3 module)  
  * Date Handling with datetime module  
  * No external libraries required

# Getting Started

### 1. Clone the repository
  git clone https://github.com/your-username/library-cli-system.git
  cd library-cli-system
### 2. Run the app
  python library.py
  The SQLite database (library.db) will be created automatically.

# Usage
You’ll be greeted with a menu:
****** Welcome To Library System ********

1. Create account for new Customer  
2. Register new book in the Inventory  
3. Record book to be rented  
4. Record book being returned  
5. Search Book in the Inventory  
6. View Books in Stock  
7. Exit the system
Just enter the number corresponding to your task and follow the prompts.

# Return Fines
  Returned after 30 days: 1000 RWF  
  31–35 days: 5000 RWF  
  Over 35 days: 20,000 RWF

# File Structure
  library.py        # Main application script
  library.db        # SQLite database (auto-created)
  README.md         # Project overview

# Notes
  Input is validated throughout (no blank or duplicate usernames, phone numbers, book names, etc.)  
  Designed for single-terminal use (no web UI)  
  Fine logic is adjustable in record_bookreturn() function

## Contributions
Pull requests and suggestions are welcome. Feel free to fork the repo and improve the system!

© Allrights Reseverd 2025 YvanRalph
