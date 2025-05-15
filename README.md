# 🧾 Tkinter Expense Tracker

A simple and user-friendly **Expense Tracker** desktop application built using **Python's Tkinter library**. This tool allows users to log daily expenses with date, amount, and category, and automatically saves the data into a CSV file. Perfect for managing personal budgets locally without the need for an internet connection.

---

## 📸 Screenshots

| Main Window | View Expenses | Statistics  |
|-------------|-------------------|--------------------|
| ![Main Window](screenshots/main_window.png) | ![View Expenses](screenshots/view_expenses.png) | [Statistics](screenshots/statistics.png)


---

## ✨ Features

- Easy-to-use Tkinter-based GUI
- Add expense with **date**, **amount**, and **description/category**
- Data automatically saved in a CSV file
- Calendar picker for selecting the date (via `tkcalendar`)
- View all entries in a table-like format
- Portable — runs on any system with Python installed

---

## 🗂️ Project Structure

Expense-Tracker-/
│
├── expense_tracker.py # Main Python script with UI and logic
├── expenses.csv # CSV file where expenses are saved (auto-created)
├── requirements.txt # List of dependencies (optional, shown below)
├── README.md # Project documentation
└── screenshots/ # Folder for storing UI screenshots


---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jebarson-caleb/Expense-Tracker-.git
   cd Expense-Tracker-
(Optional but recommended) Create a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Or install manually:

bash
Copy
Edit
pip install tkcalendar
Note: tkinter is bundled with most Python installations (especially on Windows). If not, install it via your OS package manager.

▶️ How to Run
bash
Copy
Edit
python expense_tracker.py
📄 Sample CSV Output (expenses.csv)
yaml
Copy
Edit
Date,Amount,Category
2025-05-15,500,Groceries
2025-05-16,250,Transportation
The CSV file is automatically created on first run in the project directory.

🛠️ Future Improvements
Edit and delete individual entries

Filter expenses by date range

Monthly summary charts

Export to Excel

Dark mode theme

📦 Dependencies
tkinter – Built-in GUI library in Python

tkcalendar – For date picking functionality

You can install everything with:

bash
Copy
Edit
pip install -r requirements.txt
🤝 Contributing
Contributions are welcome! Please fork this repository and submit a pull request for any improvements or bug fixes. You can also open issues if you find any problems.

📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

👤 Author
Developed by Your jebarson-caleb.
For queries or collaborations, feel free to open an issue or connect via GitHub.